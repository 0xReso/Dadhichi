# Kafka Consumer Groups

By the end you will understand how Kafka lets several copies of a program share the reading of one stream of messages, so that each message is handled once, and what happens when one of those copies fails.

## A stream too fast for one reader

Kafka is software that stores streams of messages and hands them to any program that wants to read them. One program writes a message, such as "order 1042 was placed, total 38 euros", and Kafka adds it to the end of a list, after every message written before it. Kafka runs on a cluster of servers, so the list survives one machine failing.

Reading a message does not remove it. Kafka keeps every message for a set period, seven days unless someone changes it, and any number of programs can read the same messages in that time. This is the main difference from a classic message queue, where a message disappears once someone takes it.

Each named stream in Kafka is called a topic. Take an online shop that writes every new order into a topic called orders. On a normal afternoon that is a few orders a second; during a big sale it reaches about 150 orders a second.

The shop's billing program reads the orders topic and charges each customer's card. Each charge needs a call to the payment provider and takes about 20 milliseconds, so one copy of the program can charge about 50 orders a second. During the sale it falls behind by 100 orders every second, which is 6,000 unpaid orders after one minute.

The obvious fix is to run three copies of the billing program. But if each copy reads the whole topic, every customer is charged three times. What the shop needs is a way for the three copies to split the orders between them, so each order is charged exactly once, and for the others to take over the share of any copy that dies. Kafka's answer is the consumer group, and it rests on the way a topic is stored.

## How a topic is cut into pieces

The shop now has a stream of orders arriving faster than one billing program can charge them, and needs several copies to share the work without overlapping. To share it, the work first has to be divided into pieces.

Kafka stores each topic as several separate lists rather than one. Each of these lists is called a partition. The orders topic has six partitions, numbered 0 to 5. A new message goes into exactly one of them. The program writing the order usually chooses the partition from a value attached to the message, here the customer's ID, so that all of one customer's orders land in the same partition.

Within one partition, messages stay in the order they were written. Across partitions there is no shared order: Kafka cannot tell you whether a message in partition 2 came before one in partition 4. This is why the shop keeps each customer in one partition: that customer's orders and refunds are then always read in the sequence they happened.

Every message in a partition has a position number, counting up from 0 as messages are added. That number is called the offset. "Partition 3, offset 5,000" points at exactly one order, and a reader that has finished offset 5,000 knows its next message is offset 5,001.

So the topic is now six independent lists, each with numbered positions. How do three billing programs divide those six lists between them?

## How a group divides the work

The orders topic is split into six partitions, each an ordered list with numbered offsets, and the shop wants three copies of the billing program to share them. This is the job consumer groups do.

A program that reads messages from Kafka is called a consumer. Each copy of the billing program is one consumer, and when it connects to Kafka it gives a group name, here "billing".

Consumers that give the same group name form a consumer group. Kafka treats the group as a single reader of the topic and gives each partition to exactly one member of it. With three billing consumers, each gets two partitions: say the first gets 0 and 1, the second 2 and 3, the third 4 and 5. Every order sits in one partition and every partition has one reader in the group, so every order is charged once. Three consumers at 50 orders a second each handle 150 a second, which keeps up with the sale.

A second group reads the same topic without affecting the first. The shop also runs an email program that sends order confirmations, using the group name "email". It is a single consumer, so Kafka gives it all six partitions. It sees every order too, at its own pace, because the messages stay in the topic regardless of who has read them. Inside a group, members share the messages; between groups, each group gets all of them.

The common mistake comes next. If three consumers keep up, it seems that ten would be faster still. They are not. Kafka never gives one partition to two members of the same group, because two readers of one list would break its order, and with six partitions there are only six pieces of work to hand out. A seventh billing consumer gets no partition at all and sits idle, waiting to replace a member that leaves. The number of partitions is the ceiling on how many consumers in a group can work at once, which is why teams choose it with future load in mind. Partitions can be added later, but that changes which partition each customer ID maps to, so a customer's new orders stop landing where the old ones did.

The work is now divided. But each consumer has to know where it stopped, and that knowledge has to outlive the consumer. How does the group keep track of its progress?

## Remembering where the group stopped

The three billing consumers each read two of the six partitions, and the email group reads all six on its own. Each consumer moves forward through its partitions offset by offset, and that position needs to be stored somewhere safer than the consumer's own memory.

So a consumer regularly reports its position back to Kafka: "group billing has finished partition 3 up to offset 5,000". This is called committing an offset. Kafka stores one committed offset for each group and each partition, which is why billing and email can be at completely different points in the same partition without disturbing each other.

By default the consumer software commits automatically every five seconds. Many teams turn that off and have the program commit after it has finished processing a batch, because then a commit always means the work is actually done.

Committed offsets are what make stopping safe. If the shop shuts down all three billing consumers for an hour of maintenance, the orders keep arriving and Kafka keeps storing them. When the consumers start again, each one asks Kafka for the group's committed offsets and carries on from there, working through the backlog of the past hour.

That covers a planned stop of the whole group. What happens when a single member stops without warning, in the middle of its work?

## When a member joins or leaves

Each billing consumer owns two partitions and commits its progress to Kafka as it goes. The remaining question is what keeps this arrangement correct when consumers crash, restart or are added.

For each group, one of Kafka's servers takes charge of membership. That server is called the group coordinator. It keeps the list of members and decides, or in older versions oversees, which partitions each one owns.

Each member sends the coordinator a small "still here" message every few seconds. These messages are called heartbeats. If a member's heartbeats stop for longer than a timeout, 45 seconds by default in recent versions, the coordinator declares it dead. A member that is alive but takes too long between requests for new messages is treated the same way, so a consumer stuck on very slow work can be removed even though it never crashed.

When a member is declared dead, or a new one joins, the coordinator hands the partitions out again across the members that remain. This is called a rebalance. Suppose the second billing consumer, which owns partitions 2 and 3, crashes during the sale. After the rebalance, the first consumer might own 0, 1 and 2, and the third might own 3, 4 and 5. No partition is left unread, but two consumers now handle 100 orders a second against 150 arriving, so billing falls behind by 50 orders a second until a replacement starts and a second rebalance gives it two partitions back. In the original design of the protocol the whole group pauses while a rebalance runs; newer versions of Kafka shorten or avoid that pause.

A rebalance cannot recover work that was done but not committed. Say the crashed consumer's last commit recorded partition 3 as done up to offset 5,000, but it had charged another 40 orders, up to offset 5,040, before it died. The third consumer, taking over partition 3, starts after offset 5,000, because that is all Kafka knows. Those 40 customers are charged a second time.

This behaviour has a name: at-least-once delivery. When a consumer commits after processing, a crash can cause some messages to be processed twice, but none to be skipped. Committing before processing flips the risk: after a crash, messages that were committed but not yet processed are never processed at all. For billing, double charges are the lesser problem, so the shop commits after charging and makes the billing program check whether an order has already been paid before charging it. Writing the program so that handling the same message twice does no harm is standard practice with Kafka.

## The whole picture

A Kafka topic is a set of ordered partitions that keep their messages after they are read, and a consumer group is a set of consumers sharing a name that Kafka treats as one reader of that topic: each partition goes to one member, so the group divides the messages without duplicating them, while other groups read the same messages independently. The partition count sets how many members can work at once. Committed offsets, stored per group and partition, let any member pick up where another stopped, and the coordinator's heartbeats and rebalances move partitions when members come and go. Because progress is only as current as the last commit, a failure can mean some messages are handled twice, which is why consumers are written to tolerate repeats.

## Going further

- Cooperative rebalancing and the new consumer group protocol: newer ways of running rebalances that move only the partitions that need to move, the latter generally available from Kafka 4.0, with the coordinator doing the assignment.
- Consumer lag: the gap between the newest offset in a partition and the group's committed offset, the main number teams watch to see whether a group is keeping up.
- Static membership: a setting that gives each consumer a fixed identity, so a quick restart does not trigger a rebalance.
- auto.offset.reset: the setting that decides where a group with no committed offset starts, at the oldest stored message or only at new ones.
