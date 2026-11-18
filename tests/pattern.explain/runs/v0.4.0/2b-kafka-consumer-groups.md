# Kafka Consumer Groups

By the end you will know how Kafka lets several copies of a program share the reading of one stream of messages, how each copy knows where to pick up, and why adding more copies sometimes changes nothing.

## One stream, too much work

Picture an online shop that records every order the moment it is placed: who bought what, and for how much. At a busy moment that is around 900 orders a second, and more than one part of the business needs to see each of them. Billing has to charge the card. A separate system has to send the confirmation email.

The shop keeps these orders in Apache Kafka, a system that stores streams of messages on disk, in the order they arrived, so that other programs can read them whenever they are ready. The checkout service writes each new order into Kafka as one message.

Kafka sorts messages into named streams called topics. All of the shop's orders go into a topic named `orders`.

A program that reads messages from a topic is called a consumer. Billing is one consumer; the email sender is another. Reading a message in Kafka does not remove it. Messages stay in the topic for a set period, often seven days, whether anyone has read them or not. That is different from a traditional message queue, where a message disappears once one reader takes it, and it is what allows billing and email to both see every order.

Now the difficulty. One copy of the billing program can handle about 400 orders a second, well short of the 900 arriving. The obvious fix is to run three copies. But if three copies each read the whole topic, every customer is charged three times. What the shop needs is a way to split the stream so that each order reaches exactly one copy of billing, while the email sender, running separately, still sees every order. A consumer group is Kafka's answer, and it starts with how a topic is cut into pieces that can be handed out.

## Partitions and offsets

You now have a topic full of orders, two jobs that each need every order, and one of those jobs too heavy for a single copy to carry. To share the work, Kafka needs units it can hand out.

Those units are partitions. A topic is made of one or more partitions, each a separate log that only ever grows at the end. The `orders` topic has six partitions, numbered 0 to 5, and each new order is appended to one of them. If a message carries a key, such as the customer's ID, every message with that key lands in the same partition. Order is guaranteed inside a partition, but not across the topic as a whole.

Each message in a partition has a position number, starting at 0 and counting up by one for each new message. That number is called the offset. Because a partition is append-only, a reader's progress through it fits in a single number: "on partition 2, the next message I need is at offset 1,205."

So the topic is six independent logs, and progress through each is one number. The remaining question is how a set of consumers divides those six logs among themselves.

## How a group shares the work

A topic is split into partitions, and a reader's place in each partition is an offset. A consumer group is the layer that turns those two facts into shared work.

Every consumer is started with a group name. Consumers that start with the same name form a consumer group, and Kafka treats the whole group as a single reader of the topic. Together, the members see every message, and each message goes to only one member. All three copies of billing are started with the group name `billing`.

Kafka achieves this by giving each partition to exactly one member of the group at a time. A member may own several partitions, but no partition is shared inside a group. With three billing copies and six partitions, each copy owns two. Together they can handle around 1,200 orders a second, comfortably above the 900 arriving. This mapping of partitions to members is called the partition assignment.

The email sender runs as a single copy in its own group, called `email`, and that one copy owns all six partitions. The two groups never interfere. Each group reads the entire topic at its own pace, so if billing falls behind during a sale, email carries on unaffected. One topic can feed many groups, and each group is one job.

Here is where people most often go wrong. Suppose a big sale is coming and someone scales billing up to eight copies, expecting even more speed. Six of the copies get one partition each. The other two get nothing and sit idle, because a partition cannot be split between members of the same group; that rule is what keeps the messages in a partition in order. The number of partitions is therefore the ceiling on how many members of one group can do useful work at once. The idle copies are not entirely wasted, since they take over if a working copy fails, but they add no speed. Partition counts can be raised later, but doing so changes which partition a given key lands in, so it is usually planned for in advance.

All of this assumes the members stay put. Real programs crash, restart, and get added, which raises the question of how the group notices, and how a member taking over a partition knows where to start.

## When members come and go

Within a group, each partition belongs to one member, and the partition count caps how many members can be busy. What keeps that arrangement correct as members change is a piece of Kafka's own machinery.

For each group, one of the Kafka servers takes the role of group coordinator. It keeps the list of members and knows which member owns which partition.

Each member proves it is still alive by sending the coordinator a small message every few seconds, called a heartbeat. If the heartbeats from a member stop for longer than a set timeout, which in recent versions defaults to 45 seconds, the coordinator treats that member as gone. A member that leaves cleanly, such as during a planned restart, tells the coordinator directly instead.

Whenever a member joins or leaves, the group redistributes its partitions. This is called a rebalance. Say billing is back to three copies and one of them crashes while it owns partitions 2 and 3. After the rebalance, the two survivors own three partitions each. In the long-standing version of this process, every member pauses reading during a rebalance, which is why frequent rebalances in large groups hurt. Kafka 4.0 made a newer protocol generally available, in which the coordinator works out the assignment itself and only the partitions that actually move are paused; which behaviour you get depends on your Kafka and client versions.

The survivor that takes over partition 2 still needs to know where to begin. It finds out because members regularly record, inside Kafka, the next offset they need on each partition they own. Recording that position is called committing an offset. Kafka keeps committed offsets per group and per partition, so `billing` and `email` each hold their own bookmark on partition 2 without touching each other's. The new owner reads the group's last committed offset for the partition and carries on from there.

The timing of commits decides what can go wrong. Suppose the crashed copy's last commit on partition 2 said "next is 1,205", but it had already charged orders up to offset 1,230 before it died. The new owner starts at 1,205 and charges those 26 orders a second time. Committing before processing avoids repeats but risks the opposite: a copy that commits and then crashes skips orders it never handled. Most systems commit after processing and accept occasional repeats, an approach known as at-least-once delivery, and make the processing safe to repeat, for example by checking whether an order ID has already been charged. By default, the standard Java client commits automatically every five seconds in the background, which narrows the window but does not close it.

## The whole picture

A consumer group exists so that one job, such as billing, can be spread across several copies without any message being handled twice by that job, while other jobs read the same stream independently. Kafka makes this work by cutting each topic into partitions, giving every partition to exactly one member of a group, and letting each group record its own committed offset per partition. The group coordinator watches heartbeats, and when a member arrives or disappears it triggers a rebalance that hands partitions to the remaining members, who resume from the last committed offsets. Two consequences follow from that design: a group can never have more busy members than the topic has partitions, and a crash between processing and committing means some messages are processed again, which is why careful consumers are built to tolerate repeats.

## Going further

Consumer lag: the gap between the newest offset in a partition and a group's committed offset, the main number people watch to see whether a group is keeping up.

`auto.offset.reset`: the setting that decides where a brand-new group with no committed offsets starts reading, either at the oldest retained message or at the newest.

Static membership (`group.instance.id`): a way to give each member a fixed identity so that a quick restart does not trigger a rebalance.

KIP-848: the Kafka Improvement Proposal behind the newer consumer group protocol, worth reading alongside the older "eager" and "cooperative" rebalancing strategies it replaces.
