# Kafka Consumer Groups

By the end you will understand how Apache Kafka lets several copies of a program share the work of reading one stream of data, and what happens when one of them fails.

## The problem

Picture an online shop. Every time a customer places an order, a small message describing it is written to a central system, and other programs read those messages to do their jobs: one sends the invoice, another sends the confirmation email. On a quiet day one copy of the invoicing program keeps up easily. On a sale day the shop takes 600 orders a second, and one copy cannot keep up. You want to run three copies and have them split the orders between them, with no order invoiced twice and none missed, and with the survivors picking up the slack if one copy crashes.

That is the problem consumer groups solve in Apache Kafka, an open-source system for moving streams of messages between programs. A consumer group is a set of programs that agree to share the reading of one stream, so that each message is handled by one member of the group, and the group keeps working when members join or leave.

To see how it works, you need three ideas about Kafka itself first.

## Topics: a log that nobody empties

Kafka runs as a cluster of servers called brokers. Programs that write messages are called producers; programs that read them are called consumers. Each message is called a record.

Records are grouped by subject into named streams called topics. The shop's orders go into a topic called `orders`.

A topic is not a queue that empties as it is read. It is a log: records are appended to the end and stay there, in order, for a set retention period (a week is a common default) whether anyone reads them or not. Reading a record does not remove it. This matters for everything that follows, because it means several different programs can read the same records, each at its own pace.

## Partitions: splitting the log so it can be shared

A single log has a single end, which makes it hard for several readers to share without stepping on each other. So Kafka splits each topic into a fixed number of pieces called partitions. Each partition is its own independent log, stored on a broker.

The shop's `orders` topic has 6 partitions, numbered 0 to 5. When the producer writes an order, it chooses a partition by taking the record's key, here the customer ID, and hashing it, turning it into a number in a repeatable way. The same customer therefore always lands in the same partition. At 600 orders a second spread evenly, each partition receives about 100 a second.

Ordering in Kafka holds only inside a partition. All of one customer's orders are in sequence because they share a partition; orders from different customers in different partitions have no guaranteed order relative to each other.

## Offsets: a reader's bookmark

Every record in a partition gets a sequence number when it is appended: the first is 0, the next 1, and so on. That number is called its offset. Offsets are counted separately in each partition, so partition 3 and partition 4 can each have a record at offset 8,400.

Because records stay put, a reader's progress is fully described by one number per partition: the offset of the next record it wants. That number is the reader's bookmark, and keeping track of it is the reader's job, not the log's.

## The group and its one rule

Now the consumer group itself. Every consumer is started with a setting called the group ID, a name such as `invoicing`. All consumers that share a group ID form one group, and Kafka divides the topic's partitions among them under one rule: each partition is read by exactly one consumer in the group at a time. One consumer may hold several partitions.

The shop starts three invoicing consumers, call them inv-1, inv-2 and inv-3. Kafka hands out the 6 partitions two apiece: inv-1 gets partitions 0 and 1, inv-2 gets 2 and 3, inv-3 gets 4 and 5. Each consumer now handles about 200 orders a second, and because no partition is shared, no two consumers ever see the same order. A customer's orders are still processed in sequence, since they all sit in one partition owned by one consumer.

This rule produces the most common misunderstanding about consumer groups. It is natural to think that more consumers always means more speed. It does not. The partition is the unit of sharing, so the number of partitions is the ceiling on how many consumers in a group can do useful work. The shop can grow the invoicing group to 6 consumers, one partition each. A seventh consumer gets no partition at all and sits idle, connected and doing nothing, waiting in reserve. To go wider than 6, the topic needs more partitions, which is why choosing the partition count is a real design decision made with growth in mind. Adding partitions later is possible, but it changes which partition each key hashes to, so one customer's new orders can land in a different partition from their old ones.

## A second group reads everything again

The email program also needs every order. It runs as its own group, `emails`, with two consumers, em-1 and em-2, which take three partitions each.

The `emails` group and the `invoicing` group do not compete. Each group gets the whole topic and keeps its own bookmarks. If the email service is slow and falls an hour behind, invoicing is unaffected; the email consumers are simply reading older offsets of the same log. This is the second half of the design: within a group, records are shared out; between groups, every group sees every record. One topic can feed many independent services this way, because the log is never emptied by reading.

## Who decides the assignment

Someone has to hand out partitions and notice when consumers come and go. For each group, one broker in the cluster takes the role of group coordinator.

Each consumer keeps telling the coordinator it is alive by sending a small message every few seconds, called a heartbeat. The coordinator also expects each consumer to keep coming back for more records. If a consumer stops heartbeating for longer than its session timeout, which is tens of seconds in recent versions, or goes too long without asking for records (five minutes by default), the coordinator declares it gone.

Whenever membership changes, because a consumer joined, left cleanly, or was declared gone, the group's partitions are redistributed. This is called a rebalance. The same thing happens if the topic gains partitions.

How a rebalance runs differs by Kafka version. In the long-standing design, consumers pause, one of them works out the new assignment and reports it through the coordinator, and everyone resumes. A newer protocol, standard from Kafka 4.0, moves the calculation onto the coordinator and lets unaffected consumers keep reading throughout. The outcome is the same either way: every partition ends up with exactly one owner again.

## Committing the bookmark

A rebalance moves partitions to new owners, and a new owner needs to know where to start. That is why consumers save their bookmarks in Kafka itself. Saving a bookmark is called committing an offset, and the saved value is the committed offset: the offset of the next record the group should read from that partition. Kafka stores committed offsets in an internal topic of its own, keyed by group, topic and partition, so each group's bookmarks live alongside the data.

Consumers commit periodically rather than after every record, because writing a bookmark for each of 100 records a second would be wasteful. By default the consumer library commits automatically every five seconds; applications can instead commit themselves at moments they choose.

## When a consumer dies

Now the full sequence, using the shop. Midway through the sale, inv-2 crashes.

1. On partition 3, inv-2 last committed offset 8,400. It then processed 50 more orders, offsets 8,400 to 8,449, and sent their invoices, but crashed before its next commit.
2. Its heartbeats stop. After the session timeout, the coordinator declares inv-2 gone.
3. A rebalance runs. Partition 2 moves to inv-1 and partition 3 moves to inv-3, so the two survivors now hold three partitions each and about 300 orders a second each.
4. inv-3 looks up the committed offset for partition 3, finds 8,400, and starts reading there.
5. inv-3 processes offsets 8,400 to 8,449 again. Those 50 customers receive a second invoice.

Nothing was lost, and nothing was handled by two consumers at the same moment, but 50 records were processed twice. This is not a fault in the setup; it is the normal behaviour of committing after processing, and it is called at-least-once delivery: every record is handled at least once, sometimes more. The alternative, committing before processing, swaps duplicates for gaps, because a crash after the commit but before the work skips those records for good. That is called at-most-once.

So the practical lesson is to write consumers that tolerate seeing a record twice. The invoicing service can check whether it has already issued an invoice for an order ID before issuing another. An operation that is safe to repeat like this is called idempotent. Kafka can offer stronger guarantees when both the input and the output stay inside Kafka, but a consumer that sends emails or calls outside services should be built assuming duplicates will happen.

The `emails` group, meanwhile, noticed nothing. Its consumers, assignments and committed offsets are its own, and inv-2's crash triggered no rebalance there.

## The whole picture

A Kafka topic is a log split into partitions, and records stay in it after they are read, so each reader tracks its own position as an offset. A consumer group is a set of consumers sharing one group ID, and Kafka gives each partition to exactly one of them, which spreads the load, keeps each partition in order, and caps useful consumers at the number of partitions. A broker acting as group coordinator watches members through heartbeats and rebalances the partitions when anyone joins or disappears, and the new owner of a partition resumes from the group's committed offset. Because work done since the last commit is repeated after a failure, consumers must be able to handle the same record twice. Separate groups never interfere, each reading the whole topic at its own pace, which is how one stream of orders can feed invoicing, email and anything else the shop adds later.

## Going further

Consumer lag: the gap between the newest offset in a partition and a group's committed offset, the main number people watch to see whether a group is keeping up.

Partition assignment strategies: the rules for dividing partitions among consumers, such as range, round-robin and cooperative sticky, which differ in how evenly they spread load and how much they move during a rebalance.

Static group membership: giving each consumer a fixed instance ID so that a quick restart does not trigger a rebalance.

Exactly-once semantics: Kafka's transactions feature, which lets a consumer read, process and write back to Kafka with its offset commit in the same transaction, avoiding duplicates within Kafka.
