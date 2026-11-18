# Kafka consumer groups

You’ll understand how Kafka divides reading work among consumers, how they resume after a restart, and why adding more consumers can leave some idle.

## One stream of orders, several readers

When an online shop receives an order, its inventory service needs to reserve the items, and its reporting service needs to count the sale. Both services need to see the order. If the shop runs two copies of the inventory service to handle a busy afternoon, those copies need to share the work. Sending every order to both copies could have them reserve the same items twice.

Apache Kafka stores records that programs can read at their own pace. Each order in the shop’s stream is a record, and the named stream that holds those records is a **topic**. The shop calls its topic `orders`. Reading a record leaves it in the topic, where another program can read it too.

A topic is divided into independently readable sequences called **partitions**. The `orders` topic has four, numbered 0 through 3. Kafka appends records to the end of each partition. A reader can follow the order of records within a partition, while readers of different partitions can make progress at different speeds.

A program that reads records from Kafka is a **consumer**. The shop’s two running copies of its inventory service each act as a consumer. The reporting service runs a third consumer with a different job.

Consumers that want to share the work use the same group name, called a **group ID**. Together they form a **consumer group**. Both inventory consumers use the group ID `inventory`, while the reporting consumer uses `reporting`. How does Kafka divide four partitions among those consumers?

## How partitions are assigned

The shop has four partitions in `orders` and two groups that read them. The `inventory` group has two consumers to share the work, and the `reporting` group has one.

A group’s division of partitions among its consumers is called an **assignment**. Within a group, each partition is assigned to one consumer at a time. In one possible assignment, the first inventory consumer reads partitions 0 and 1, and the second reads partitions 2 and 3. The consumers share the topic by taking whole partitions.

The reporting consumer gets its own assignment. Since it is the only member of `reporting`, it reads all four partitions. It can read the same order from partition 2 that the second inventory consumer reads. The group ID determines who shares an assignment. Each group can read the full topic on its own schedule.

Suppose the shop adds a third inventory consumer. One possible assignment gives two partitions to the first consumer and one each to the other two. With four inventory consumers, each can read one partition. A fifth has no partition to read from `orders` while the other four are working. Four partitions give the group four units of work it can assign independently.

This also matters when one partition gets much busier than the others. If most new orders land in partition 2, the consumer assigned to it has most of the work. An extra consumer can take over a different partition, but partition 2 still goes to a single consumer in the group. When a partition changes hands, how does its new consumer know where to start?

## How a group remembers its place

Partition 2 belongs to one inventory consumer at a time. The reporting consumer can read it independently, so Kafka needs a way to remember a different place in the same partition for each group.

Every record has a position in its partition, called an **offset**. Offset 70 in partition 2 refers to a different record from offset 70 in partition 0. To identify a record by position, the consumer needs both the partition and the offset.

A consumer can ask Kafka to save the position its group should resume from. This is called **committing an offset**. Suppose the second inventory consumer has reserved stock for the order at offset 70 in partition 2. It can commit offset 71, meaning that 71 is the next offset its group should read. The committed offset belongs to `inventory` for that partition, so another member of `inventory` can use it.

Each group saves its position separately for each partition. The reporting consumer might have committed offset 90 in partition 2 while the inventory consumer has committed 71. Reporting may already have counted orders that inventory still needs to act on. Neither group’s progress moves the other’s saved position.

There can also be a gap between the records a consumer has read and the work it has finished. The inventory consumer can receive several orders while it is still reserving stock for the first one. Kafka uses the committed offset as the group’s saved reading position. The service decides when its work is far enough along to save that position. What happens if the consumer stops between reserving stock and committing the offset?

## What happens when a consumer stops

The inventory group has saved offset 71 for partition 2. Its second consumer can now work on the order at 71, and the saved position stays there until the group commits a later offset.

Suppose that consumer reserves the stock for order 71 and then crashes before committing offset 72. Once Kafka detects that the consumer has dropped out, the group updates its assignment. This process is called a **rebalance**. With the first inventory consumer still running, it can take over partitions 2 and 3 alongside the two it already had.

The surviving consumer starts partition 2 at the committed offset, 71. It reads order 71 again because the last saved position says to start there. Kafka has no record in that offset of whether the inventory database already changed.

This is where it is easy to read too much into the assignment rule. Giving partition 2 to one consumer at a time controls who reads it for the group. The same order can still be handled by successive owners of the partition. If a repeated reservation would be harmful, the inventory service can record the order’s unique identifier as part of the same database change that reserves the stock. When it sees the order again, it can tell that the reservation already happened.

Saving offset 72 before reserving the stock creates the opposite risk. If the consumer crashes after saving 72 and before updating inventory, its replacement resumes at 72 and passes over an order that still needs a reservation. The timing of the commit determines what work the consumer may be asked to repeat or may leave unfinished after a failure. How do the assignment and the saved position work together?

## The whole picture

A Kafka consumer group gives several consumers one shared reading job. The group ID says which consumers share it, the partition assignment says who reads each part of the topic now, and the committed offsets say where the group should resume when that work changes hands. That lets the shop run inventory and reporting at their own speeds, add inventory consumers up to the number of available partitions, and carry the inventory group’s progress from one consumer to another. The inventory service still decides when a reservation is complete enough to commit and how to handle an order it encounters again.

## Going further

- **`auto.offset.reset`** sets where a consumer starts when the group has no valid committed offset for a partition.
- **`enable.auto.commit`** controls whether the consumer periodically commits offsets automatically.
- **Assignment strategies** determine how partitions are distributed among the consumers in a group.