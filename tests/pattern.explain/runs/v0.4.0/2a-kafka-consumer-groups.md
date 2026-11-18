# Kafka Consumer Groups

By the end you will understand how Kafka lets many programs share the work of reading one stream of messages, how they recover when one of them fails, and why adding more readers sometimes does nothing.

## One reader is not enough

Picture an online shop that records every order as a short message the moment it is placed: who bought what, for how much. Those messages are stored in Kafka, a system that keeps streams of messages on a cluster of servers so that other programs can read them. Each server in that cluster is called a broker.

A program that reads messages from Kafka and does something with them is called a consumer. In the shop, one consumer is a billing service: it reads each order and charges the customer's card.

On a quiet day, a single billing consumer keeps up. Then a sale starts and orders arrive at 3,000 a second, while one copy of the billing service can handle about 1,000. Messages pile up faster than they are read, and customers wait longer and longer to be charged.

The obvious fix is to run three copies of the billing service. But that creates two new problems. If all three read every order, every customer is charged three times. And if one copy crashes halfway through, someone has to notice and pick up exactly where it stopped. A Kafka consumer group is the mechanism that solves both: it lets several consumers split one stream between them, each message handled by one of them, with the split repaired automatically when a member comes or goes.

Before seeing how the split works, it helps to know how Kafka stores the stream in the first place, because the split follows that storage exactly.

## Topics, partitions and offsets

The shop's problem is three billing consumers that must share a stream of orders without doubling up. The shape of that stream inside Kafka decides how they can share it.

Kafka groups messages by subject into a named stream called a topic. The shop writes all its orders to a topic called `orders`. A topic is a log: new messages are added at the end and existing ones are never edited.

A topic is cut into several smaller logs, each called a partition. The shop's `orders` topic has six partitions, numbered 0 to 5. When the shop writes an order, Kafka places it in one of the six. Usually the choice comes from a key attached to the message, such as the customer's ID, so that all orders from the same customer land in the same partition. Each partition lives on a broker, so the six can be read from in parallel.

Within a partition, each message has a position number, counting up from zero, called its offset. If partition 2 holds 5,000 orders, they sit at offsets 0 to 4,999, in the order they arrived. Kafka keeps messages in order within one partition, but makes no promise about order across partitions.

One fact about this log matters a great deal: reading a message does not remove it. Kafka keeps messages for a set time, often a week by default in many setups, whether or not anyone has read them. A consumer's progress is just a note of which offset it has reached. This is the main difference from a traditional message queue, where a message disappears once someone takes it, and people coming from queues often expect Kafka to behave that way.

So the stream is six ordered logs, and a reader's position in each one is a single number. That raises the question of how three consumers decide which logs each of them reads.

## How a group splits the work

You now hold the stream as six partitions, each an ordered log where a reader's place is an offset. The consumer group decides who reads which partition.

A consumer joins a group by stating a name for it when it starts, called the group ID. All three copies of the billing service start with the group ID `billing`. Kafka treats every consumer with the same group ID as one team sharing one job.

Kafka then hands out the topic's partitions among the members. This handing out is called partition assignment. With six partitions and three consumers, each consumer gets two: the first might read partitions 0 and 1, the second 2 and 3, the third 4 and 5. The rule that makes billing safe is this: within one group, each partition is read by exactly one consumer at a time. Since every order lives in exactly one partition, every order is read by exactly one billing consumer, and no card is charged twice through normal operation.

This rule has a consequence that catches many people out. The partition is the smallest unit of work a group can hand out, so a group can never have more busy members than the topic has partitions. Suppose the sale grows and the shop runs six billing consumers: each now reads one partition, and throughput roughly doubles. Now it starts a seventh. There is no partition left to give it, so it sits idle, connected and waiting, doing nothing. Adding consumers stops helping at the partition count. If the shop expects to need more than six readers, it has to give the topic more partitions, and that is best planned early, because adding partitions later changes which partition a given customer's key maps to, which breaks the per-customer ordering for a while.

A second consequence is that groups are independent of each other. Say the shop also has an email service that sends a receipt for every order. It runs with the group ID `email`. Kafka treats it as a separate team, so the `email` group gets its own assignment of all six partitions and receives every order too, while `billing` receives every order as well. Within a group, the work is split; across groups, each group gets the whole stream. Because reading does not delete anything, the two groups can even read at different speeds without affecting each other.

That covers the happy path: a fixed set of consumers, each owning its partitions. Real services crash, restart and get scaled up and down, so the remaining question is how the group notices and how a replacement knows where to start.

## Remembering progress and recovering from failure

At this point you have three billing consumers splitting six partitions, two each, with every partition owned by exactly one member. Now one of them fails.

For a replacement to continue, the group needs a record of how far each partition has been processed. A consumer provides this by periodically telling Kafka the offset of the next message it intends to read in each of its partitions. This is called committing an offset, and the stored number is the committed offset. Kafka keeps committed offsets per group and per partition, in an internal topic of its own. So the `billing` group might have committed offset 1,041 for partition 2, meaning orders 0 to 1,040 are done, while the `email` group has its own, unrelated number for the same partition.

Someone has to watch the members. For each group, one broker takes on that duty, and in this role it is called the group coordinator. Every consumer sends it a small "I am still alive" signal every few seconds, called a heartbeat. If the coordinator stops hearing from a consumer for long enough, typically tens of seconds depending on settings, it declares that consumer dead. A consumer that keeps sending heartbeats but stops asking for new messages for too long, for example because it is stuck on a slow job, is also treated as gone.

When membership changes, the group redistributes partitions. This is called a rebalance. Say the consumer that owned partitions 2 and 3 crashes. The coordinator notices, and the two survivors are given the orphaned partitions, so each now owns three. The same thing happens in reverse when a new consumer joins: some partitions are taken away from existing members and given to the newcomer. During a rebalance, the partitions being moved are not processed. In older setups the whole group pauses; newer versions and settings narrow the pause to only the partitions that move.

The new owner of partition 2 asks Kafka for the `billing` group's committed offset, gets 1,041, and starts reading there. This is where a subtle but important consequence appears. Suppose the crashed consumer had actually charged orders 1,041 to 1,060 but crashed before committing the new offset. The new owner starts at 1,041 and charges those twenty customers a second time. Committed offsets mark the last point that was recorded, not the last thing that was done.

This is why the usual arrangement, processing a message and then committing, is called at-least-once delivery: nothing is lost, but some messages may be processed twice after a failure. The opposite order, committing before processing, risks losing messages instead, because a crash after the commit skips work that never happened. Teams commonly handle this by making processing idempotent, meaning that doing it twice has the same effect as doing it once. The billing service, for example, could record each order ID it has charged and skip any it has seen before.

## The whole picture

A Kafka consumer group exists so that several copies of a program can share the reading of one topic, each message handled once per group, while the group heals itself when copies fail or are added. It rests on how Kafka stores a topic: as partitions, each an ordered log where a reader's progress is just an offset and reading deletes nothing. Consumers that share a group ID divide the partitions among themselves, one owner per partition, which is why the partition count caps the useful number of consumers and why a different group, such as `email`, receives the whole stream independently. Each member commits the offset it has reached, a broker acting as group coordinator watches heartbeats, and when a member disappears a rebalance hands its partitions to the others, who resume from the committed offsets. Because the commit always trails slightly behind the real work, a crash can replay a few messages, so the design gives you at-least-once processing, and making that safe is left to the consumer.

## Going further

- `auto.offset.reset`: the setting that decides where a group starts in a partition when it has no committed offset yet, either the oldest retained message (`earliest`) or only new ones (`latest`).
- Assignment strategies: the different rules for dividing partitions among members, such as range, round-robin and cooperative sticky, which differ in how evenly they spread work and how much they move during a rebalance.
- Static membership (`group.instance.id`): lets a consumer that restarts quickly keep its partitions instead of triggering a rebalance.
- The new consumer group protocol (KIP-848): a redesign, generally available in Kafka 4.0, that moves assignment to the broker and makes rebalances incremental by default.
