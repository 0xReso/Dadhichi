# Kafka Consumer Groups

By the end you will know how Kafka lets several programs share the work of reading one stream of messages, what happens when one of them stops, and why adding more of them sometimes changes nothing.

## The problem: one stream, too much to read

Picture an online shop. Every time someone places an order, the website writes a short record of it, the order number, the items, the price, and hands it to a system that keeps these records in order so other programs can read them. On a busy day that might be 3,000 orders a minute, fifty every second.

The system doing the keeping is Apache Kafka, open-source software that stores streams of records and lets programs read them back. Kafka runs on a handful of servers working together, and each of those servers is called a broker. Each record is called a message.

Messages about the same subject are kept together in a named stream called a topic. The shop's topic is called `orders`. A program that writes messages into a topic is a producer; the shop's website is the producer here. A program that reads them is a consumer.

Now the trouble. The billing program, a consumer that charges each customer's card, needs about 60 milliseconds per order, roughly the time of a blink. That works out to about 16 orders a second, well short of the fifty arriving. One copy of the billing program falls further behind every second.

The obvious fix is to run three copies of it. But if all three read the whole `orders` topic, every customer gets charged three times. What you need is a way for the three copies to split the topic between them so that each order is handled by exactly one. That is what a consumer group does. Before seeing how it does it, two more pieces of Kafka need to be in place.

## Partitions and offsets

A topic is not one long line. Kafka splits it into several separate lines, each kept in strict order, and each of these lines is called a partition. The shop created `orders` with six partitions, numbered 0 to 5. When the website writes an order, Kafka puts it in one of the six. Usually the choice comes from a key attached to the message, such as the customer ID, so all orders from the same customer land in the same partition and stay in the order they were placed.

Inside a partition, every message gets a position number, starting at 0 and counting up: 0, 1, 2, and so on. That number is called the offset. Partition 3 might hold messages at offsets 0 through 41,207, with the newest at the end.

Reading a partition does not remove anything from it. Kafka keeps messages for a set period, often seven days by default, whether or not anyone has read them. A consumer tracks its place by remembering the offset of the next message it wants, like a bookmark. This is the first place people often go wrong: Kafka is not a queue where a message disappears once it is taken. Every reader has its own bookmark into the same unchanging log.

With partitions in hand, the splitting problem has an obvious shape: hand different partitions to different copies of the billing program. So how do the copies agree on who gets which?

## How a consumer group divides the work

You now know that `orders` is six ordered partitions, and that a reader keeps its place with an offset. A consumer group is the arrangement that lets several consumers share those partitions without overlap.

Each copy of the billing program starts up with the same name, set in its configuration, for example `billing`. That name is the group ID, and every consumer that uses it is a member of the same consumer group. Kafka treats the group as a single logical reader of the topic, made of several workers.

One broker takes charge of each group. It is called the group coordinator. It keeps the list of current members and makes sure the partitions are divided among them.

The division follows one rule: within a group, each partition is read by exactly one member at a time. A member may hold several partitions, but no partition is shared. With three members and six partitions, a typical split is two each: the first copy reads partitions 0 and 1, the second reads 2 and 3, the third reads 4 and 5. This split is called the partition assignment. Each order now sits in exactly one partition, and that partition belongs to exactly one billing copy, so each order is charged once. Three copies at 16 orders a second each give about 48 a second, close to the fifty arriving.

The same rule produces the most common misunderstanding of consumer groups. Suppose the team, still a little behind, starts ten copies of billing. Only six of them get work. There are only six partitions, and a partition cannot be split between two members of the same group, so four copies sit idle, connected and doing nothing. The number of partitions is the ceiling on how many members of one group can work at once. If you expect to need more readers later, you create the topic with more partitions from the start; partitions can be added afterwards, but doing so changes which partition each customer's key maps to, which can disturb per-customer ordering.

The rule also explains what ordering you get. Because one member reads each partition from start to end, orders within a partition are processed in sequence. Across partitions there is no ordering at all: partition 0 and partition 4 are read in parallel by different machines. Kafka promises order per partition, not per topic.

The split works while all three members stay healthy. What happens when one of them crashes in the middle of the afternoon?

## When members come and go

The `billing` group now has three members, each holding two of the six partitions. Each member keeps signalling to the group coordinator that it is alive, a small message sent every few seconds called a heartbeat.

If the coordinator stops hearing heartbeats from a member for long enough, it decides that member is gone. The same happens if a member keeps sending heartbeats but stops asking Kafka for new messages for too long, which usually means it is stuck. Either way the coordinator must hand the dead member's partitions to someone else. Redistributing partitions among the current members is called a rebalance. It also happens when a new member joins, or when one shuts down cleanly. After the third copy crashes, a rebalance might leave the first copy with partitions 0, 1 and 4, and the second with 2, 3 and 5.

That raises a question. The surviving copy that now owns partition 4 has never read it. Where should it start? It cannot use the crashed copy's bookmark, because that lived in the crashed copy's memory.

The answer is that members periodically write their bookmarks into Kafka itself. A member tells Kafka, in effect, "for group `billing`, partition 4, I have finished everything before offset 18,530." That saved position is called a committed offset. Kafka stores committed offsets in a special internal topic, so they survive any one consumer or broker going down. When a member takes over a partition, it asks for the group's committed offset and starts reading from there.

The gap between processing and committing is where duplicates come from. Suppose the crashed copy had charged the cards for orders at offsets 18,530 through 18,560 but had not yet committed. Its last committed offset still says 18,530. The new owner starts there and charges those thirty-one customers again. By default, then, a consumer group gives at-least-once processing: no message is skipped, but after a failure some can be handled twice. The common practice is to make the processing safe to repeat, for instance by having billing check whether an order number has already been charged before charging it. Committing before processing flips the risk the other way, so a crash can lose messages instead.

Rebalances have a cost too. In the classic form of the protocol, every member stops reading while partitions are reassigned, so the whole group pauses for a moment, often seconds. Newer versions of Kafka reduce this so that only the partitions actually moving are paused. Either way, a group whose members keep dropping out and rejoining spends a lot of time rebalancing instead of working.

So far there has been one group. The shop has other programs that care about orders, and they raise a different question: what happens when a second group reads the same topic?

## Many groups, one topic

You now know that one consumer group splits a topic's partitions among its members, and keeps its place with committed offsets stored in Kafka. Those committed offsets are kept per group, which is the last piece.

The shop also runs an email program that sends each customer a confirmation. It joins with the group ID `emails`. Kafka treats `emails` as a completely separate reader. It gets its own partition assignment among its own members, and its own committed offsets. It receives every order, all six partitions' worth, independently of `billing`.

So the two groups do not compete. If billing is far behind and email is caught up, each simply sits at a different offset in the same partitions. If the email program is switched off for an hour, its committed offsets wait where they were, and when it returns it picks up from there, as long as the messages are still within the topic's retention period.

This is how Kafka covers two patterns with one mechanism. Inside a group, members share the work, each message going to one member. Across groups, every group sees every message. Adding a new kind of reader, say a fraud checker, means starting it under a new group ID; nothing about billing or email changes.

## The whole picture

A Kafka topic is a set of ordered partitions that nobody empties, and a consumer group is a named team of consumers that reads that topic as one: the group coordinator gives each partition to exactly one member, which is why each order is billed once and why members beyond the partition count sit idle; heartbeats tell the coordinator who is alive, a rebalance moves partitions when that changes, and committed offsets stored in Kafka let the new owner resume where the old one left off, at the price of possibly repeating the last uncommitted stretch; and because offsets belong to the group, any number of groups can read the same topic in full without touching each other.

## Going further

- **Consumer lag**: how far a group's committed offsets trail the newest message in each partition; the standard number for telling whether a group is keeping up.
- **Cooperative rebalancing and the new consumer group protocol**: newer approaches, the latter arriving with Kafka 4.0, that move only the affected partitions and, in the newer protocol, let the broker compute the assignment instead of the consumers.
- **Static membership**: giving each member a fixed identity so a quick restart does not trigger a rebalance.
- **auto.offset.reset**: the setting that decides where a brand-new group starts when it has no committed offset, at the oldest retained message or only at new ones.
