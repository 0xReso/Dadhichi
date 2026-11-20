# Kafka Consumer Groups

By the end you will know how several copies of a program share the reading of one Kafka data stream without doing the same work twice, what happens when one of them fails, and why adding more copies sometimes speeds nothing up.

## One reader is not enough

Picture an online shop that records every order the moment a customer pays. Several services care about those orders. Billing has to charge the card, and analytics wants to count sales by region. The shop does not want the checkout page to call each of these services directly, because if billing is slow or down, checkout would stall with it.

So the shop puts the orders somewhere in between. Checkout writes each order down and moves on, and the other services read the orders at their own pace. The system that does this holding-in-between is Apache Kafka, an open-source program that runs on a cluster of servers and keeps streams of messages for other programs to read.

Kafka keeps messages in named streams. The shop's stream of orders is called `orders`, and a named stream like this is called a topic. Programs that write into a topic are called producers; here, checkout is the producer.

A topic is not one long line. Kafka splits it into several separate lines that can sit on different servers and be written and read independently. Each of these lines is called a partition. The shop created `orders` with 6 partitions, numbered 0 to 5. Every new order goes into exactly one of them, and inside a partition the orders stay in the order they arrived.

Kafka does not delete a message when someone reads it. Each message keeps its place in its partition for as long as the topic is configured to keep data, often days. Each place has a number, counting up from zero: the first order in partition 3 is at position 0, the next at position 1, and so on. That position number is called an offset. A reader keeps track of where it is by remembering, for each partition, the offset of the next message it wants.

A program that reads from a topic is called a consumer. Now the problem arrives. On a busy evening the shop takes 3,000 orders a minute, and charging a card takes billing about 50 milliseconds per order, quicker than a blink but adding up. One copy of billing can handle about 1,200 orders a minute. It falls further behind every minute. The obvious fix is to run three copies of billing. But if all three read the whole topic, every customer is charged three times. What is needed is a way for the three copies to divide the orders between them.

## How a group divides the work

You now have a topic of 6 partitions, a growing pile of orders in it, and three copies of billing that must split those orders without overlap.

Kafka's answer is to let consumers declare that they belong together. Each copy of billing starts with the same setting, a group name, here `billing`. Consumers that share a group name form a consumer group, and Kafka treats the group as one logical reader of the topic.

Inside a group, the unit of sharing is the partition, not the single message. Kafka hands each partition to exactly one member of the group. With 6 partitions and three billing consumers, a typical split gives the first consumer partitions 0 and 1, the second partitions 2 and 3, and the third partitions 4 and 5. Each consumer reads only its own partitions, so no order is charged twice, and the three together handle about 3,600 orders a minute, enough to keep up with 3,000.

Handing partitions to members is called assignment. It is worked out when the group forms and again whenever its membership changes. A consumer can hold several partitions, but within one group a partition never has two readers at the same time.

This partition-sized sharing has a useful side effect. Because all orders in partition 2 are read by one consumer in sequence, they are processed in the order they arrived. Producers usually choose the partition by a key, such as the customer's ID, so that all of one customer's orders land in the same partition and are handled in order. Across different partitions there is no ordering promise at all.

Analytics is a separate service, so it runs its consumers under a different group name, `analytics`. Kafka keeps a separate record of progress for each group. The `analytics` group therefore reads every one of the 3,000 orders a minute, just as `billing` does, and neither group's reading affects the other. Within a group, consumers divide the topic; between groups, each one gets the whole topic. This is how Kafka covers both styles of messaging people usually treat as separate: a work queue, where each job goes to one worker, and broadcast, where everyone hears everything.

That record of progress lives in Kafka itself. When a consumer has finished with some orders, it reports to Kafka: "for group `billing`, partition 2, the next offset to read is 8,412." This report is called committing an offset. The committed offset belongs to the group, not to the individual consumer, which matters the moment a consumer disappears and another must pick up its partitions.

## When a member comes or goes

So far you have three billing consumers, each holding two of the six partitions and committing its progress to Kafka under the group name. Now one of them fails.

Something has to notice. For every group, one of Kafka's servers takes on the job of keeping track of who is in it. That server is called the group coordinator. Each consumer sends it a small "still alive" message every few seconds, called a heartbeat. If the coordinator stops hearing from a consumer for longer than a set timeout, it decides that consumer is gone. A consumer that is alive but stuck can also be dropped: if it goes too long without asking for new messages, it is treated as failed even though its heartbeats continue.

Suppose the third billing consumer, holding partitions 4 and 5, crashes at 19:02. The coordinator notices the missing heartbeats and redistributes the partitions among the two remaining members. This redistribution is called a rebalance. Afterwards the first consumer might hold partitions 0, 1 and 2, and the second partitions 3, 4 and 5. A rebalance also happens when a consumer joins, when one shuts down cleanly, and when the topic gains partitions.

The consumer that inherits partitions 4 and 5 has no memory of what the crashed one was doing. It asks Kafka for the group's committed offsets for those partitions and starts reading there. This is why the committed offset belongs to the group: it lets work move between members without anyone starting over.

Here is the limit of that arrangement. Say the crashed consumer had charged the orders at offsets 5,000 to 5,040 in partition 4 but had last committed offset 5,000 before crashing. The new owner starts at 5,000 and charges those 40 orders again. With the usual habit of committing after processing, a crash can cause messages to be handled twice, but none are skipped. This is called at-least-once delivery. Committing before processing flips the risk: no duplicates, but orders in flight at the moment of the crash are never charged. For a service that takes money, the common practice is to commit after processing and make the work safe to repeat, for instance by having billing check whether an order ID has already been charged.

Rebalances also cost time. In the long-standing way Kafka groups work, consumers stop reading while partitions are being moved, so the whole group pauses for a moment, usually seconds. Newer versions reduce this by moving only the partitions that need to change hands. Either way, a group whose members keep joining and leaving, for example because they keep missing the timeout, spends much of its time rebalancing instead of reading.

Now billing is down to two consumers, handling about 2,400 orders a minute against 3,000 arriving, so it is falling behind again. The tempting response is to add many more consumers at once, and that is where people most often go wrong.

## More consumers is not always more speed

You hold the whole mechanism now: a group shares a topic by giving each partition to one member, it tracks progress with committed offsets, and it rebalances when membership changes. The last piece is what that partition rule implies for scaling.

Say the team, worried about the coming holiday rush, starts nine billing consumers. The coordinator rebalances and assigns the 6 partitions to six of them, one each. The other three receive nothing. They stay connected, send heartbeats, and sit idle, because a partition cannot be read by two members of one group at once. Billing's capacity is now about 7,200 orders a minute, six consumers at 1,200 each, exactly what six consumers would give. The three extra cost money and add nothing.

This is the common misconception: that a consumer group scales with the number of consumers. It scales with the number of consumers only up to the number of partitions. The partition count is the ceiling on how many members of one group can work at the same time, so it is chosen when a topic is designed, with expected growth in mind. Partitions can be added later, but doing so changes which partition a given key maps to, which breaks the per-customer ordering for keys that move.

The idle consumers are not entirely useless. If one of the six working consumers crashes, a rebalance hands its partition to one of the idle ones, which picks up from the committed offset. Some teams keep a spare or two for this reason. But as a way to go faster, consumers beyond the partition count do nothing.

## The whole picture

A Kafka consumer group lets several copies of a program act as one reader of a topic. The topic is split into partitions, and the group's coordinator assigns each partition to exactly one member, so the members divide the messages without overlap while each partition is still read in order. Progress is stored in Kafka as committed offsets that belong to the group, so when a member dies or a new one joins, a rebalance moves partitions to other members, which resume from those offsets, at the price of a short pause and possible repeated messages. Separate groups keep separate offsets, so every group receives the full stream. And because a partition has at most one reader per group, the number of partitions sets the limit on how far one group can spread its work.

## Going further

- Consumer lag: the gap between the newest offset in a partition and a group's committed offset, the standard measure of whether a group is keeping up.
- `__consumer_offsets`: the internal Kafka topic where committed offsets are stored.
- Partition assignment strategies: the rules a group uses to decide which member gets which partition, such as range, round-robin, and cooperative sticky, the last of which moves as few partitions as possible during a rebalance.
- The newer consumer group protocol: a redesign in recent Kafka versions in which the coordinator computes assignments itself and rebalances are less disruptive.
