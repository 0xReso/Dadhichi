# Kafka consumer groups

You’ll understand how Kafka divides work among consumers, how they resume after a restart, and why adding more consumers can leave some idle.

## One stream, two jobs

When an online shop receives an order, its shipping software needs to arrange delivery. Its reporting software needs to count the sale. Both need to see the same order, while two copies of the shipping software should ordinarily split the orders between them.

Kafka gives the shop a place to keep those order records. Kafka runs on servers and stores records so that programs can read them independently. A named stream of records is called a *topic*. The shop calls this topic `orders`. Reading an order leaves the record in the topic, where it remains available under Kafka’s storage rules.

A topic is divided into numbered sequences called *partitions*. Each new record goes at the end of one partition. Suppose `orders` has three, numbered 0, 1, and 2. Kafka gives records a definite order within each partition. Across all three partitions, there is no single Kafka reading order.

A program that reads records from Kafka is called a *consumer*. The shop can run several copies of its shipping software, each with a consumer that fetches orders and hands them to the software for processing.

The shipping consumers identify themselves to Kafka with the same name, `shipping`. That name is their *group ID*, and the consumers working under it form a *consumer group*. The reporting software uses a different group ID, `reporting`. Kafka can now distinguish consumers that share a job from consumers that each need their own read of the topic.

How does Kafka divide three partitions among the shipping consumers?

## Who reads which partition

The shop has three partitions in `orders`. Its shipping consumers share the group ID `shipping`, so they share the job of reading those partitions.

Within a consumer group, each partition is assigned to one consumer at a time when the group is settled. With two shipping consumers, one might be assigned partitions 0 and 1, and the other partition 2. Each consumer fetches records from the partitions assigned to it. Kafka divides up whole partitions, so partition 0 stays together even if it contains most of the orders.

The reporting group gets its own assignments. If it has one consumer, that consumer can read all three partitions. An order in partition 0 is available to the reporting consumer and to whichever shipping consumer has partition 0. Each group can read at its own pace.

This is where adding consumers can produce a surprise. A third shipping consumer can take one of the three partitions, leaving each consumer with one. A fourth shipping consumer has no partition to read while the other three hold their assignments. For a group reading this topic alone, three partitions allow at most three consumers to read at once. Even with three active consumers, an unusually busy partition still belongs to one of them.

Assignments can change when a consumer joins or leaves the group, or when Kafka detects that it has stopped responding. The group adjusts who reads which partitions in a process called a *rebalance*. If the shipping consumer assigned partition 2 stops, a surviving consumer can pick it up.

When partition 2 changes hands, how does its new consumer know where to start?

## How a consumer picks up the work

A rebalance can give partition 2 to a different shipping consumer. To resume the work, that consumer needs a reading position that survives the handover.

Kafka gives every record a number marking its position in its partition. That number is called an *offset*. The partition number matters too. Offset 41 in partition 2 identifies a different record from offset 41 in partition 0.

A consumer can save a reading position by sending it to Kafka. This is called *committing an offset*. The committed offset normally marks where reading should resume. If the shipping consumer finishes processing through offset 41 in partition 2, it can commit offset 42 for that partition.

Kafka stores committed offsets separately for each group and partition. When a new shipping consumer takes over partition 2, it can resume from the `shipping` group’s committed offset of 42. The `reporting` group has its own committed offset for partition 2. It might still be working through records in the thirties, and the shipping group’s progress has no effect on where it resumes.

The timing of a commit matters because processing an order and saving a position are separate actions. Suppose the shipping consumer creates a shipment for the order at offset 42, then stops before it commits offset 43. The replacement consumer resumes at 42 and sees that order again. If the shipping software can recognize that the shipment already exists, it can handle the repeat without creating another one.

The reverse order has a cost too. If the consumer commits offset 43 before it creates the shipment for offset 42, a crash in between leaves the group set to resume at 43. The order is still in Kafka, but the group’s saved position takes it past the unfinished work. The committed offset records where to resume. Whether a shipment exists is something the shipping software has to establish.

## The whole picture

A Kafka consumer group lets several consumers share one reading job while giving each independent job its own progress. The group ID tells Kafka which consumers belong to that job. Partition assignments determine who reads each part of the topic now, and committed offsets determine where the group can resume when a consumer takes over. In the shop, shipping can redistribute its work and reporting can read the same orders at its own pace. The shipping software still has to account for the gap between creating a shipment and saving its place.

## Going further

- `auto.offset.reset` controls the starting position when a consumer has no usable committed offset for a partition.
- `enable.auto.commit` controls whether a consumer automatically commits offsets at intervals.
- A *partition assignor* is a strategy for deciding which consumers receive which partitions.