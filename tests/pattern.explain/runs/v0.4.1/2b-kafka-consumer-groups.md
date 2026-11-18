# Kafka Consumer Groups

By the end you will know how several copies of a program share the work of reading one Kafka stream, how they keep their place, and why adding more copies sometimes does nothing at all.

## One reader is not enough

Picture an online shop. Every time a customer places an order, the shop's website writes a short record describing it: who bought what, for how much. Those records go into Apache Kafka, an open-source system for storing streams of events and letting other programs read them as they arrive. On a busy day the shop produces a few thousand order records every second.

Several other programs care about those orders. A billing service has to charge each card. An email service has to send each confirmation. Neither should miss an order, and the billing service in particular must not charge the same order twice without good reason.

A program that reads records out of Kafka is called a consumer. One consumer running on one machine can only work so fast. If charging a card takes 20 milliseconds, one billing consumer handles about 50 orders a second, nowhere near a few thousand. The obvious fix is to run many copies of the billing service side by side. That raises the real question: how do those copies split the orders between them so that each order is charged once, none is skipped, and the work carries on when one copy crashes?

Kafka's answer is the consumer group.

## How Kafka stores the stream

The shop's problem is that one billing consumer is too slow, and many copies need some way to share the work. To see how they share it, you first need the shape of what they are reading.

Kafka keeps records in named streams called topics. The shop has one topic, called `orders`. A topic is a log: new records are added to the end, existing records are never edited, and reading a record does not remove it. It stays in the topic until a retention limit is reached, such as seven days or a size cap. This matters for everything that follows, because many readers can read the same records without getting in each other's way.

A single log on a single machine would become a bottleneck of its own, so each topic is split into several independent logs called partitions. The shop's `orders` topic has 6 partitions, numbered 0 to 5. When the website writes an order, Kafka places it in one of the six, usually chosen from the record's key, such as the customer ID, so that all orders from one customer land in the same partition. Order is guaranteed inside a partition, but not across partitions.

The machines that hold these partitions are called brokers. A Kafka installation, known as a cluster, is a handful of brokers, with the partitions of each topic spread across them so the load and the storage are shared.

Every record in a partition has a position number called its offset. The first record in partition 0 has offset 0, the next has offset 1, and so on, counting up forever. Partition 3 has its own offsets starting from 0. A consumer reading a partition is really saying "give me the records from offset 4,812 onward", so an offset is all it needs to know where it is.

So the stream is six ordered logs, each with numbered positions, spread over a few machines. The question is how a group of billing consumers divides those six logs between them.

## How a group divides the work

You now hold the picture of the `orders` topic as six partitions, each an ordered log where every record has an offset. The billing service wants to run several copies and have them share those six partitions.

Each copy of the billing service is started with the same name, a setting called the group ID, here `billing`. Every consumer that shares a group ID belongs to the same consumer group. Kafka treats the group as one logical reader of the topic, made up of several members.

The central rule is this: within one group, each partition is assigned to exactly one member at a time. Run three billing consumers and each gets two partitions. One might read partitions 0 and 1, the next 2 and 3, the last 4 and 5. Since each order sits in exactly one partition, and each partition has exactly one reader in the group, each order is handled by exactly one billing consumer. Nobody has to coordinate order by order; the split happens once, at the level of whole partitions.

The work of deciding who gets which partition is run by one broker acting as the group coordinator. Members tell the coordinator they want to join the group, the coordinator settles on an assignment, and each member is told which partitions are now its own. In the classic version of the protocol one member, the group leader, computes the assignment and hands it back through the coordinator; newer Kafka versions, from 4.0, can let the coordinator compute it directly. Either way, the outcome is the same kind of map from partitions to members.

Now bring in the email service. It starts its own consumers with a different group ID, `email`. That group gets its own, entirely separate assignment of the same six partitions. Both groups read every order, each at its own pace, because reading does not remove a record from the topic. This is how Kafka gives you both behaviours people want from a messaging system: inside a group, the records are shared out like jobs in a queue; across groups, every group receives everything, like subscribers to a broadcast.

Here is where most people go wrong. It is tempting to think that if three billing consumers are too slow, ten will be faster. They will not. With 6 partitions and the rule of one reader per partition, at most six consumers in the `billing` group can have work. The seventh, eighth, ninth and tenth join the group, receive no partitions, and sit idle. The number of partitions is the ceiling on how many members of one group can read in parallel. Teams that expect to scale a service widely therefore choose a generous partition count when they create the topic, since raising it later changes which partition each key lands in.

Splitting the partitions gives each member its share of the stream. What it does not yet explain is how the group remembers how far it has read, and what happens when a member disappears halfway through its share.

## Keeping its place and surviving failure

So far, the `billing` group has three members, each reading two of the six partitions, and the group as a whole sees each order once. The missing piece is memory: a running program can track its offset in its own memory, but that is lost the moment it stops.

To survive restarts, a consumer regularly records, back in Kafka, the offset it has reached in each of its partitions. This is called committing an offset. The committed offset for a partition is the position of the next record the group should read there. Kafka stores these numbers in an internal topic of its own, keyed by group ID, topic and partition, so the `billing` group and the `email` group each keep a separate set.

Commits are what let work move between members. Suppose the billing consumer reading partitions 4 and 5 crashes. Members send small "still alive" messages to the coordinator, called heartbeats, every few seconds. When the coordinator stops hearing from one for longer than a timeout, by default 45 seconds in recent versions, it declares that member gone.

The coordinator then reshuffles the partitions among the members still standing. This reshuffle is called a rebalance. After it, the two surviving billing consumers might hold three partitions each. The one that inherits partition 5 looks up the `billing` group's committed offset for partition 5 and starts reading there. The same thing happens in reverse when you add a member: a rebalance hands it some partitions taken from the others.

The timing of commits decides what happens to the records in flight. Say the crashed consumer had processed orders up to offset 1,207 in partition 5, but its last commit said 1,200. Its replacement starts at 1,200 and charges orders 1,200 to 1,206 a second time. If instead a consumer commits an offset before it has finished the work, and then crashes, the records in between are never processed at all. Kafka's default is to commit automatically every five seconds in the background, which in practice gives this first behaviour: after a crash, a few seconds of records can be read twice. This is called at-least-once delivery, and it is why careful consumers are written so that handling the same record twice does no harm, for example by checking an order ID before charging.

Rebalances also have a cost. In the classic protocol, every member of the group pauses reading while partitions are reassigned, so a group whose members keep crashing or timing out can spend more time reshuffling than working. Newer assignment strategies and the newer group protocol move only the partitions that need to change, which shortens that pause.

## The whole picture

A Kafka consumer group is a set of consumers sharing a group ID that together read a topic, with each partition owned by exactly one member at a time, so the work scales out across machines and each record is handled once per group. Partitions are what make the split possible, and their number caps how many members can usefully work at once. Committed offsets are what make the split durable: they let any member pick up exactly where another left off. The coordinator, heartbeats and rebalances tie the two together, moving partitions to whoever is alive and pointing them at the last committed position. Separate groups get separate assignments and separate offsets, which is how one stream of orders can feed billing, email and anything else, each at its own pace.

## Going further

- Consumer lag: the gap between the newest offset in a partition and the group's committed offset, the main number people watch to see whether a group is keeping up.
- `auto.offset.reset`: the setting that decides where a brand-new group starts reading, at the oldest retained record or only at new ones.
- Static membership (`group.instance.id`): lets a consumer restart under the same identity without triggering a rebalance.
- Exactly-once processing: Kafka transactions, which tie offset commits to the consumer's own output so records are neither lost nor repeated, within Kafka.
