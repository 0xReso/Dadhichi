# Kafka Consumer Groups

By the end you will understand how Kafka lets several programs share the work of reading one stream of messages, how they keep their place, and why adding more readers does not always make things faster.

## One stream, too much work

Picture an online shop. Every time a customer places an order, the shop's website writes a short message describing it: who bought what, for how much. Several other systems care about those messages. Billing needs to charge the card. Another system needs to send a confirmation email. On a busy day there might be a few thousand orders a minute, far more than one billing program can keep up with.

The shop sends these messages through Apache Kafka. Kafka is a system that stores streams of messages on a cluster of servers and lets other programs read them. The servers that make up the cluster are called brokers. Programs that write messages are called producers, and programs that read them are called consumers.

Kafka keeps related messages together under a name. All the shop's order messages go into one named stream called `orders`. A named stream like this is called a topic.

Unlike a traditional message queue, Kafka does not delete a message once someone has read it. It keeps every message for a set period, often days, whether or not anyone has read it. Reading is closer to reading a log file than to taking a letter out of a mailbox: the message stays where it is, and each reader keeps track of how far it has got.

That leaves the shop with two needs that pull in different directions. Billing wants to run several copies of its program so that together they can handle the load, and it wants each order charged exactly once, not once per copy. Meanwhile the email system wants to see every order too, entirely independently of billing. How does Kafka let a team share a stream among several copies of one program without stepping on another team reading the same stream?

## Partitions and offsets

The shop has a topic called `orders` and wants many readers on it. To make sharing possible, Kafka first splits the topic into pieces.

A topic is divided into a fixed number of separate logs, each stored on a broker. Each of these logs is called a partition. The shop created `orders` with six partitions, numbered 0 to 5. When the website writes an order, it lands in one of the six. Usually the producer picks the partition from a key on the message, such as the customer's ID, so every order from the same customer goes to the same partition.

Inside a partition, messages sit in the order they arrived, and each one gets a number: 0 for the first, then 1, 2, 3 and upwards. That position number is called an offset. A consumer reading partition 3 remembers "I have handled everything up to offset 4,812", and next time it asks for offset 4,813 onwards.

Kafka promises that messages within one partition are read in the order they were written. It makes no such promise across partitions: an order in partition 1 may be handled before an earlier one in partition 4. Because each customer's orders share a partition, the shop still sees each customer's orders in sequence, which is usually the ordering that matters.

Partitions are the unit Kafka hands out. A whole partition goes to one reader; Kafka does not split a single partition's messages among several readers. That rule is what makes the next part work, and it is also where its limits come from. So how does Kafka decide which billing program reads which of the six partitions?

## How a group divides the work

The `orders` topic is now six ordered partitions, each read by position. The question is how several copies of billing share them.

Each copy of the billing program, when it starts, tells Kafka a name: `billing`. Every consumer that gives the same name joins the same team, and Kafka treats that team as a single reader of the topic. That team is called a consumer group, and the name is its group ID.

Kafka then hands out the partitions among the group's members so that each partition goes to exactly one member. With three billing consumers and six partitions, each gets two. Consumer A might read partitions 0 and 1, consumer B partitions 2 and 3, consumer C partitions 4 and 5. Every order is seen by exactly one billing consumer, and the work is spread three ways. Handing out partitions like this is called partition assignment.

The email system starts its own consumers with a different group ID, `email`. Kafka keeps a separate assignment for that group. Its consumers read all six partitions among themselves, at their own pace, with no effect on billing. This is the second half of what the shop wanted: within a group, the work is split; between groups, each gets the whole stream. If the shop later adds a fraud-checking system under a third group ID, it too receives every order, with no change to billing or email.

Here is where people most often go wrong. It is natural to think of a consumer group as a pool of workers where adding workers always adds speed. That is true only up to the number of partitions. Suppose billing scales from three consumers to seven. Six partitions can go to at most six consumers, so the seventh is given nothing and sits idle, waiting. It is not wasted entirely, because it can take over if another member fails, but it adds no throughput. The number of partitions is the ceiling on how many consumers in one group can work at once, which is why teams usually choose a partition count with future growth in mind. Adding partitions later is possible but moves which keys land where, which breaks the per-customer ordering for messages already written.

The opposite case is fine. If billing ran only two consumers, each would take three partitions; one consumer alone would take all six. Fewer consumers than partitions only means each one does more.

Members of a group come and go: a copy crashes, a new one is deployed, a server restarts. So what happens to a consumer's partitions, and its place in them, when the membership changes?

## Keeping place and surviving change

Billing now has three consumers, each owning two of the six partitions, and the email group reads the same partitions independently. What remains is how the group remembers its progress and how it reacts when members change.

Each consumer tells Kafka how far it has got in each partition it owns, by sending the offset it has finished with. This is called committing an offset. Kafka stores the committed offsets per group, in an internal topic of its own, so the `billing` group and the `email` group each have their own record of progress in every partition. This is also how two groups can read the same messages independently: the messages are shared, but the bookmarks are not.

One broker in the cluster is responsible for keeping track of each group: who its members are, and which partitions each owns. That broker is called the group coordinator. Every consumer sends it a small "I'm still here" signal every few seconds, called a heartbeat.

Now say consumer B crashes while it owns partitions 2 and 3. Its heartbeats stop. After a timeout, typically somewhere between ten and forty-five seconds depending on the Kafka version and settings, the coordinator declares B gone and redistributes the partitions among the members that remain. Redistributing partitions after a change in membership is called a rebalance. After it, A and C might own three partitions each.

The consumer that takes over partition 2 has to know where to start. It looks up the `billing` group's committed offset for partition 2 and resumes from the message after it. This is the point of committing: progress belongs to the group, not to any one consumer, so the work continues wherever it was left.

That handover has a sharp edge, which is when the commit happens relative to the work. Suppose B had charged the cards for offsets 900 to 950 in partition 2 but had last committed offset 899 before crashing. Its replacement starts at 900 and charges those fifty customers again. Committing after processing means a crash can repeat work but never skip it; this is called at-least-once delivery. Committing before processing flips the risk: nothing is repeated, but messages handled after the commit and before the crash are lost from billing's point of view. Most systems choose at-least-once and make the processing safe to repeat, for example by recording each order ID that has been charged and skipping duplicates.

Rebalances also happen in calmer moments: when a new consumer joins, when one shuts down cleanly, or when partitions are added. In the original design, every member of the group stopped reading during a rebalance until the new assignment was settled, so frequent rebalances could stall a group noticeably. Newer versions of Kafka reduce this by moving only the partitions that need to move, while the rest keep flowing; the exact behaviour depends on the version and settings in use.

## The whole picture

A Kafka consumer group lets several copies of one program share the reading of a topic while other programs read the same topic separately. The topic is split into partitions, each an ordered log read by offset. Consumers that share a group ID form one group, and Kafka assigns each partition to exactly one member, so the work divides cleanly and the partition count sets the ceiling on useful members. Each group commits its own offsets, so different groups read the whole stream independently, and within a group, progress survives any one consumer. A broker acting as group coordinator watches members through heartbeats and triggers a rebalance when they change, handing partitions to the survivors, who resume from the committed offsets. When the commit happens relative to the work decides whether a crash repeats messages or loses them.

## Going further

- **Cooperative rebalancing**: the incremental style of rebalance where only reassigned partitions pause, chosen through the consumer's partition assignment strategy setting.
- **Static membership**: giving each consumer a fixed instance ID (`group.instance.id`) so a quick restart does not trigger a rebalance.
- **`auto.offset.reset`**: the setting that decides where a group with no committed offset starts, at the oldest message (`earliest`) or only new ones (`latest`).
- **The new consumer group protocol**: a redesign in recent Kafka versions (proposal KIP-848, generally available from Kafka 4.0) that moves assignment work to the coordinator and makes rebalances less disruptive.
