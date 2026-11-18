# Kafka Consumer Groups

By the end you will know how several programs share the work of reading one stream of Kafka messages, why a group can only grow so far, and what happens when one of its members fails.

## One reader is not enough

Picture an online shop that records every order the moment it is placed. Several other systems need to hear about each order: billing has to charge the card, and another system has to send the confirmation email. At a busy hour the shop takes about 3,000 orders a second, far more than one program can charge cards for.

The shop passes these orders around using Kafka. Kafka is a system that stores messages in the order they arrive and lets other programs read them back, at their own pace, as many times as they like. A program that writes messages into Kafka never has to know who will read them.

Messages in Kafka are filed under a name, such as "orders". That named stream is called a topic. The shop's checkout writes every new order into the orders topic, and that is the last the checkout sees of it.

A program that reads messages from a topic is called a consumer. The billing system is a consumer of the orders topic, and so is the email system.

Here is the problem. If billing is one consumer reading the topic from start to end, it handles one order after another, and at 3,000 a second it falls behind and never catches up. The obvious fix is to run several copies of billing. But if three copies all read the whole topic, each order is charged three times. What billing needs is a way for its copies to split the orders between them, so that each order is handled by exactly one copy. That raises the question of what, inside a topic, there is to split.

## The pieces a topic is made of

Billing needs to divide the orders topic among several copies of itself without any order being handled twice. Kafka makes that possible by building every topic out of smaller pieces.

A topic is divided into a fixed number of separate lanes, each one an independent, ordered list of messages. Each lane is called a partition. The shop created its orders topic with 6 partitions, numbered 0 to 5. Every new order lands in one of them.

Which partition a message lands in usually depends on a value attached to the message, called its key. The shop uses the customer's ID as the key, and Kafka sends every message with the same key to the same partition. So all of one customer's orders sit in one partition, in the order they were placed. Kafka keeps messages in order within a partition, but makes no promise about order across different partitions.

Inside a partition, each message has a position number, counting up from zero: the first order in partition 3 is at position 0, the next at position 1, and so on. That position number is called an offset. A consumer keeps track of where it has got to in each partition by remembering an offset, much as you would keep your place in a book with a page number.

One more fact matters here. Reading a message does not remove it. Kafka keeps messages for a set period, often days, whether or not anyone has read them. Many people arrive expecting Kafka to behave like a to-do queue, where a task disappears once someone takes it. In Kafka, a message stays put, and each reader only moves its own bookmark forward. That is why billing and email can both read every order without getting in each other's way.

So a topic is a set of partitions, and a reader's progress is a set of offsets. The question now is how several copies of billing agree on who reads which partition.

## How a group shares the work

The orders topic has 6 partitions, each an ordered list of messages, and a consumer keeps its place in each with an offset. Billing wants three copies of itself to divide those partitions between them.

Each consumer, when it starts, declares a name for the team it belongs to. Every consumer that declares the same name is treated by Kafka as one team reading the topic together. That team is called a consumer group, and the name it shares is called the group ID. All three billing copies start with the group ID "billing".

Kafka then hands each partition of the topic to exactly one member of the group. This handing-out is called partition assignment. With 6 partitions and 3 billing consumers, each consumer gets 2 partitions: the first might own partitions 0 and 1, the second 2 and 3, the third 4 and 5. Each consumer reads only its own partitions. No order is read by two billing consumers, and every order is read by one of them.

Because one partition always belongs to one consumer in the group, the ordering promise survives the split. All of one customer's orders sit in one partition, so one billing consumer handles them, one after another, in order.

The email system starts its own consumers with a different group ID, "email". Kafka treats that as a separate team with its own assignment and its own offsets. Say email runs 2 consumers: each gets 3 of the 6 partitions. Billing and email both see every order, and neither notices the other. Within a group the work is divided; across groups the whole topic is delivered to each one.

That gives the rule that people most often get wrong. A partition is never split between two members of the same group. So the number of partitions is the ceiling on how many consumers in one group can do useful work. If billing panics at a sale and starts 8 consumers on a 6-partition topic, 6 of them get one partition each and the other 2 get nothing at all. They sit idle, connected and waiting. Adding consumers beyond the partition count buys no extra speed. To go further, the topic needs more partitions, which is a decision best made early, because adding partitions later changes which partition each key goes to, and breaks the guarantee that one customer's orders stay together.

So far the group has had a fixed set of members. The real test is what happens when one of them crashes, or when a fourth one joins.

## When members come and go

A consumer group splits a topic's partitions among its members, one owner per partition, and each member tracks its place with offsets. Now suppose the billing consumer that owns partitions 4 and 5 crashes.

Someone has to notice, and someone has to decide who takes over. Kafka runs on a cluster of servers, and each of those servers is called a broker. The brokers store the partitions and serve them to consumers.

For each consumer group, one of the brokers takes on the job of keeping track of the group's members. That broker is called the group coordinator. Every billing consumer stays in touch with billing's coordinator by sending it a small "still here" signal every few seconds. That signal is called a heartbeat.

When the coordinator stops receiving heartbeats from a consumer for long enough, typically somewhere between ten and forty-five seconds depending on version and settings, it decides that consumer is gone. A consumer is also treated as gone if it keeps sending heartbeats but stops asking for new messages for too long, which is how Kafka catches a program that is stuck rather than dead.

The group then redistributes the partitions among the members still standing. This redistribution is called a rebalance. With one billing consumer gone, the remaining two take three partitions each, perhaps 0, 1, 4 for one and 2, 3, 5 for the other. A rebalance also happens when a member joins or leaves on purpose: start a fourth billing consumer, and the coordinator reshuffles so that two consumers own two partitions and two own one. In older versions of Kafka, every member paused all its reading during a rebalance; newer versions move only the partitions that need to change hands, so the others keep working.

The consumer that takes over partitions 4 and 5 has to know where to start. If it began at the very beginning, it would charge every customer in those partitions again. So consumers regularly report their position to Kafka: "in partition 5, I have finished everything before offset 1,200." That report is called committing an offset, and the committed offset always points at the next message to read. Kafka stores these commits for each group, in a special internal topic named `__consumer_offsets`, so that any member that inherits a partition can look up where the group had got to.

Commits happen every so often, not after every single message. By default the standard client commits automatically every few seconds, and a program can instead commit by hand after it finishes its work. Either way there is a gap. Say the crashed consumer had charged the cards for orders up to offset 1,250 in partition 5, but its last commit said 1,200. The new owner starts at 1,200 and charges orders 1,200 to 1,249 a second time. This is the second thing people get wrong: a consumer group does not, on its own, guarantee that each message is processed exactly once. The usual behaviour is called at-least-once delivery: nothing is skipped, but a message can be handled twice after a failure. Teams usually design their processing so that a repeat does no harm, for instance by having billing record each order ID it has charged and skip any it has seen before.

The opposite mistake is possible too. If a consumer commits an offset before doing the work and then crashes, the new owner starts past messages that were never handled, and they are lost to that group. That is why the safer habit is to finish the work first and commit after.

## The whole picture

A consumer group exists so that many copies of one program can read a Kafka topic together as if they were a single reader. The topic is split into partitions; the group gives each partition to exactly one of its members, so the work is divided and the order within each partition is kept, while every other group receives the whole topic for itself. Because a partition cannot be shared inside a group, the partition count caps how many members can be busy. A group coordinator watches the members through heartbeats and, when one appears or disappears, rebalances the partitions among those present. The new owner of a partition resumes from the group's last committed offset, which is why nothing is lost when the work is committed after it is done, and why a few messages can be processed twice.

## Going further

- **Consumer lag**: how far a group's committed offsets trail the newest messages in each partition; the usual number to watch to see whether a group is keeping up.
- **Partition assignment strategies**: the rules for which member gets which partitions, such as range, round-robin and sticky assignment, set through the `partition.assignment.strategy` setting.
- **The new consumer rebalance protocol**: a redesign, generally available from Kafka 4.0, in which the coordinator itself computes assignments and rebalances happen incrementally; enabled on the client with `group.protocol=consumer`.
- **Static membership**: giving each consumer a fixed `group.instance.id` so that a quick restart does not trigger a rebalance.
