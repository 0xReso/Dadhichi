# Kafka Consumer Groups

By the end you will understand how Kafka lets several copies of a program share the work of reading one stream of events, what happens when one of them crashes, and why adding more copies stops helping past a certain point.

## One stream, too much to read

Picture an online shop. Every time a customer places an order, the shop's website writes down a small record of it: the order number, the items, the address. Many other programs in the company want those records, and they want them as they happen, not in a nightly batch.

Kafka is a system built to carry records like these. Programs send it events, Kafka stores them in the order they arrived and keeps them on disk, and other programs read them back whenever they are ready. It sits between the programs that produce data and the programs that use it, so neither side has to know about the other.

Events in Kafka are written into named streams. Each stream is called a topic. The shop writes every new order into a topic called "orders".

A program that reads from a topic is called a consumer. The shop's shipping service is a consumer of "orders": for each order it reads, it prints a shipping label.

Now the problem. On an ordinary day the shop takes a few hundred orders a second, and one copy of the shipping service, handling about 500 a second, keeps up. On Black Friday orders arrive at 3,000 a second, six times what one copy can manage. Every second it falls further behind, and customers wait longer for their parcels.

The obvious fix is to run several copies of the shipping service. But that raises two awkward questions. How do the copies split the orders so that no label is printed twice and no order is missed? And when a separate analytics service also wants to see every order, how does it read them without stealing work from shipping? Kafka's answer to both is the consumer group, and it rests on how a topic is laid out inside.

## Partitions and offsets

So far you have a topic called "orders", one shipping consumer that cannot keep up, and the need to split the work without losing or repeating anything. The split begins with how Kafka stores a topic.

A topic is not one long line of events. It is divided into several separate lines, each called a partition. The "orders" topic has six partitions, numbered 0 to 5. Each new event goes into exactly one of them. Usually the event carries a key, here the order number, and Kafka sends every event with the same key to the same partition. Events within one partition stay in the order they were written, so everything that happens to one order is read in the right sequence.

Partitions live on servers that run Kafka. Each such server is called a broker. A real deployment has several brokers, and the six partitions of "orders" are spread across them, so no single machine carries the whole topic.

Within a partition, every event has a position number, counting up from zero: the first event is 0, the next is 1, and so on. That number is called the offset. A consumer reading partition 3 might be at offset 10,200, meaning it has dealt with everything before that point.

Reading an event does not remove it. Kafka keeps events for a set time, often seven days, whether anyone has read them or not. It is the consumer's job to remember where it is, by remembering its offset in each partition. This is what lets two different services read the same events independently: each keeps its own place.

With the topic cut into six numbered lines, each with its own position counter, the question becomes how several shipping consumers decide who reads which line.

## How a group divides the work

You now hold a topic split into six partitions, each a separate ordered line of events with offsets marking positions. Here is how several consumers share them.

When you start a consumer, you give it a group name. Consumers that share a name form a consumer group. The shipping service's copies all start with the group name "shipping", and Kafka treats them as one reader whose work is spread over several machines.

The rule that makes it work is this: within one group, each partition is handed to one member at a time. Start three copies of the shipping service and Kafka gives each of them two partitions. Together they handle 1,500 orders a second, which is better but still short of the 3,000 arriving. Start three more and each of the six copies gets one partition. Now the group can process 3,000 a second and keeps up. Because a partition never has two readers from the same group, no order reaches two shipping copies, and no label is printed twice.

The analytics service starts its own consumers with a different group name, "analytics". Kafka treats that as a completely separate reader. It also gets all six partitions, divided among its own members, and keeps its own offsets. Shipping and analytics each see every order, and neither slows the other down. That is how one topic feeds many services at once.

This is where people most often go wrong. When the shipping group falls behind again, the instinct is to add more copies: a seventh, an eighth. But there are only six partitions, and each can go to only one member of the group. The seventh and eighth copies get nothing and sit idle, waiting for a partition to free up. The number of partitions is the ceiling on how many consumers in one group can do useful work. To go beyond six, the topic needs more partitions, and that is best decided when the topic is created, because adding partitions later changes which partition each key lands in, which can break the ordering of events for keys that were already in flight.

That leaves the question of who hands out the partitions, and what happens to a partition when the copy reading it dies.

## Crashes, rebalances and committed offsets

You now know that a group's members split the partitions between them, one reader per partition, and that a separate group reads everything again on its own. What remains is how that split is kept up to date as copies come and go.

For every group, one of the brokers takes on the job of keeping track of who is in it. That broker is called the group coordinator. When a new shipping copy starts, it introduces itself to the coordinator; when a copy shuts down cleanly, it says goodbye.

Copies do not always shut down cleanly. So each member sends the coordinator a small "still here" message every few seconds, called a heartbeat. If the coordinator hears nothing from a member for long enough, 45 seconds by default in recent versions of Kafka, it declares that member dead.

Whenever a member joins or leaves, the partitions have to be shared out again. That reshuffle is called a rebalance. Suppose the six-copy shipping group is running and the copy reading partition 3 crashes. After the coordinator notices, a rebalance gives partition 3 to one of the five survivors, which now reads two partitions. How disruptive a rebalance is depends on the version: in the older approach every member pauses its reading while partitions are reassigned, while newer versions move only the partitions that actually need a new owner.

The new owner of partition 3 needs to know where to start. For that, each consumer regularly tells Kafka how far it has got in each partition, a step called committing, and the recorded position is called the committed offset. Kafka stores it per group and per partition. Many consumer libraries commit automatically every few seconds; the official Java client does it every five seconds by default. The new owner reads the committed offset for "shipping" on partition 3 and picks up from there.

Committed offsets are not always up to date, and this is a limit worth knowing. Say the crashed copy had printed labels up to offset 10,250 but had last committed 10,200. The new owner starts at 10,200, so the 50 orders in between are processed a second time and get a second label. Nothing is lost, but some things happen twice. This guarantee is called at-least-once delivery, and it is what you get when a consumer commits after doing its work. Committing before the work flips the risk: a crash could then skip orders instead of repeating them. In practice, services that consume Kafka events are usually written so that handling the same event twice is harmless, for instance by checking whether a label for that order number already exists.

## The whole picture

A consumer group is Kafka's way of letting several copies of one program act as a single reader of a topic. The topic is split into partitions; within a group each partition has exactly one reader at a time, so the work is divided without overlap, and the partition count sets how many readers can be busy. Each group keeps its own committed offsets, so different services read the same events independently, and a group coordinator watches heartbeats and triggers a rebalance when a member appears or vanishes, handing its partitions to someone who resumes from the last committed offset. That resumption is what makes the system survive crashes, and the gap between the last commit and the crash is why an event can occasionally be handled twice.

## Going further

- Consumer lag: the distance between the newest offset in a partition and a group's committed offset, the main number people watch to see whether a group is keeping up.
- Cooperative rebalancing and the newer consumer group protocol: the changes, culminating in the protocol made generally available in Kafka 4.0, that let a rebalance move only the affected partitions instead of pausing the whole group.
- Exactly-once processing: Kafka's transactions feature, which ties a consumer's offset commit to the results it writes so an event's effects are recorded once, within limits worth reading about.
- Share groups: a newer, queue-like kind of group in recent Kafka versions where several consumers can read from the same partition, lifting the one-reader-per-partition rule.
