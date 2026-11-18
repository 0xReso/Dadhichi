# Kafka consumer groups

You’ll understand how Kafka divides work among copies of an app, how a replacement picks up that work, and why it can process the same event twice.

## Why readers need a group

An online shop records paid orders as they arrive. Its packing app reads those records and creates packing jobs. When orders arrive faster than one copy of the app can handle them, the shop can run a second copy. The two copies need a way to divide the orders between them. Otherwise, each copy could read every order and send the warehouse two jobs for the same parcel.

Kafka is a system that stores records like these and lets apps read them. An app can read a record while new records are still arriving. Reading leaves the record in Kafka, so another app can read it for its own purpose.

Kafka brings records of the same kind together under a name. The shop writes its paid orders to a *topic* called `paid-orders`. Both copies of the packing app read from that topic.

Each running copy that reads records from Kafka is a *consumer*. The two consumers run the same packing code. Kafka needs to know they’re doing the same job before it can share out the work.

The shop gives both consumers the same group ID, a name that identifies their shared job. With the group ID `packing`, they belong to the same *consumer group*. If the shop also runs a sales reporting app, it gives that app a different group ID. The reporting group can read the same paid orders and keep its own place as it goes.

What does Kafka hand to each consumer when it divides the packing work?

## How Kafka divides the work

The two packing consumers share a group ID, so Kafka treats them as members of the same group. To see what each member gets, look at how the shop’s topic stores its orders.

Kafka organizes a topic into one or more ordered sequences called *partitions*. The `paid-orders` topic has three, numbered 0, 1, and 2. Each paid order goes into one partition, at the end of that partition’s sequence. A consumer reads the records of a partition in the order they were stored. Across all three partitions, the group can be working on several orders at once, and there’s no overall processing order.

Within a consumer group, Kafka assigns each partition to one consumer at a time. For example, one packing consumer might get partitions 0 and 1, and the other might get partition 2. The first consumer reads from two sequences. The second reads from one. Kafka assigns whole partitions, so a busy partition stays with its assigned consumer even when another consumer has less work.

If the shop adds a third packing consumer, Kafka can give each member a partition. If it adds a fourth, one member will have no partition to read from. That’s why adding consumers can help only up to the number of partitions the group can read from. With three partitions, at most three members can have packing work assigned to them at once.

Kafka revisits the assignments when group membership changes. This is called a *rebalance*. When the third consumer joins, partition 1 might move from the first consumer to the new member. If a consumer stops and Kafka detects its absence, its partitions can move to members that are still running.

When a partition changes hands, how does its new consumer know where to start?

## How a new consumer finds its place

After the third packing consumer joins, it takes over partition 1. That partition contains orders the previous consumer already handled as well as orders still waiting. To pick up the work, the new consumer needs a position in the sequence.

Each record has a numbered position within its partition, called an *offset*. Suppose partition 1 contains three consecutive paid orders at offsets 40, 41, and 42. The numbers apply to partition 1. Partition 0 can also have a record at offset 42, and that record is a different paid order.

The packing consumer reads orders 40 and 41 and creates a packing job for each. It can then save offset 42 as the group’s next position in partition 1. Saving that position is called *committing an offset*. The committed offset says where to resume. It points to the next record to read.

Kafka stores committed offsets separately for each group and each partition. When the new packing consumer takes over partition 1, it can start from the packing group’s committed offset of 42. The sales reporting group can be at a different position in that partition, because its progress is stored under its own group ID.

The position a consumer has reached while reading can be ahead of the position the group has saved. The new packing consumer can read order 42 while the committed offset is still 42. That gap matters if the consumer goes away, because the next member can recover the saved position.

What happens if the consumer creates the packing job during that gap and then crashes?

## Why an order can be processed twice

The new consumer started at offset 42, the position saved for partition 1. It reads order 42 and creates the packing job. Then it crashes before committing offset 43.

Kafka detects that the consumer is gone and reassigns partition 1 to a surviving member. The group’s committed offset is still 42. The surviving consumer starts there, sees the same order, and may create a second packing job. From Kafka’s point of view, 42 is where the packing group asked to resume.

This is the common trap. A partition has one assigned reader in the group at a time, and two readers can still handle the same record in succession. The assignment tells each consumer what to read. The committed offset tells a replacement where to resume. Neither records whether the warehouse already has a packing job for that order.

Saving offset 43 before creating the packing job would expose the opposite failure. If the consumer crashed after saving 43 and before creating the job, the replacement would resume at 43 and skip the unfinished order. With a separate packing system, creating a job and saving an offset are two actions, and a crash can come between them.

The shop can make the repeated read safe by having the packing system enforce one job per order ID. When the replacement submits order 42 again, the packing system uses the existing job. The app can then commit offset 43 and move on without sending another job to the warehouse.

## The whole picture

A Kafka consumer group lets several running copies share a job by assigning whole partitions to its members. Each group commits its own place in each partition, so another app can read the same topic independently and a surviving consumer can resume after a handover. The saved place and the work done outside Kafka can diverge if a consumer crashes between the two actions. In the shop, the committed offset gets the replacement back to the order, and the order ID keeps that second read from creating a second packing job.

## Going further

- **Offset reset policy** determines where a consumer starts when there is no usable committed offset.
- **Partition assignment strategy** governs how partitions are distributed among members of a group.
- **Automatic offset commits** let the consumer library save offsets periodically. Check how that timing relates to when your app finishes processing a record.