# Kafka consumer groups

By the end, you’ll understand how Kafka divides work among copies of an app, what happens when a copy stops, and why some work can happen twice.

## One stream of orders, two jobs

An online shop needs to reserve stock each time a customer places an order. It also needs to count orders for its sales dashboard. On a busy day, several copies of the stock app should be able to share the work. The sales app still needs to see every order, whichever copy of the stock app handles it.

Kafka gives the shop a place to keep those orders so both apps can read them at their own pace. Each order is written as a **record**, a stored entry that contains the order details. Kafka keeps the record after an app reads it, so another app can come along and read it too.

The shop puts its order records in a named stream called a **topic**. Both apps read the `orders` topic. The topic tells them where to find the records. It leaves open which copies of an app should share the work.

A running program that reads records from Kafka is called a **consumer**. The shop starts two consumers for the stock app. Both can reserve stock, so the shop wants them to divide the orders between them. The sales app starts a consumer of its own, which needs to count all the orders.

Consumers that share a job join the same **consumer group**. Each consumer names its group when it connects to Kafka. Both stock consumers join the `stock` group, and the sales consumer joins the `sales` group. The groups read the same topic independently. An order can therefore reach the `stock` group for reserving stock and the `sales` group for counting, without either group taking it away from the other.

What does Kafka divide between the two stock consumers?

## Kafka assigns partitions

The two stock consumers belong to the same group, so they share the job of reading `orders`. To understand which orders each consumer gets, start with how the topic stores its records.

The `orders` topic has three **partitions**. A partition is a sequence of records that Kafka adds to at the end. Each order record goes into one partition. There is a definite order among the records in any given partition, and the three partitions can be read at the same time.

Kafka divides the work by assigning whole partitions. Within a consumer group, a partition is assigned to one consumer at a time. In the shop, one stock consumer gets partitions 0 and 1, and the other gets partition 2. The sales group has one consumer, so that consumer gets all three partitions. Partition 2 can be assigned to a stock consumer and a sales consumer at the same time because the assignments belong to different groups.

Adding a third stock consumer can give each stock consumer a partition of its own. A fourth stock consumer would have no partition to read in this topic while the other three are active. Three partitions give the group three pieces of work it can assign independently. The consumer assigned partition 2 reads its records even when that partition happens to receive more orders than the others.

Now suppose the stock consumer assigned partition 2 stops. How does its replacement know which order to read first?

## Where a replacement starts

The stock consumer assigned partition 2 has stopped. Once Kafka detects that it has gone, the group can assign partition 2 to the surviving stock consumer. A change in how partitions are assigned among a group’s consumers is called a **rebalance**. The sales consumer keeps its own assignment because it belongs to a different group.

Each record has a number that marks its position in its partition. That number is called an **offset**. An order at offset 42 in partition 2 is identified by both the partition and the offset. Partition 0 can have a record at offset 42 as well. The numbers describe positions within each partition.

Kafka can store a group’s place in each partition. Saving that place is called **committing an offset**. The committed offset gives the position where the group should resume. If a stock consumer finishes handling the order at offset 41 in partition 2 and commits offset 42, its replacement starts reading there. The `sales` group has its own committed offset for partition 2, so its progress can be ahead of or behind the `stock` group’s.

Suppose the stock consumer successfully reserves stock for the order at offset 42 and then stops before committing offset 43. The committed offset is still 42. The surviving consumer takes over the partition, reads the order at offset 42, and may try to reserve the same stock again.

The assignment tells you which consumer is responsible for reading a partition at a given time. It can be tempting to read that as a promise that an order will be handled exactly once. The two consumers in this example handle the order at different times, each while it is responsible for the partition. Kafka’s saved reading position and the shop’s stock update are separate actions, so the saved position can lag behind a completed reservation. The stock app can make a retry safe by recording the order identifier as part of the same stock update. If the order comes through again, the app can see that the reservation already exists.

## The whole picture

A Kafka consumer group lets several copies of an app share a topic by giving each copy whole partitions to read. Each group has its own assignments and saved reading positions, so the stock and sales apps can read the same orders at different speeds. When a stock consumer stops, another can take over its partition and resume from the group’s committed offset. Any reservation completed after that offset was saved may be attempted again.

## Going further

- **Consumer lag** is how far a group’s reading position is behind the end of a partition.
- **Offset reset policy** determines where a consumer starts when the group has no usable committed offset.
- **Partition assignment strategy** determines how a group distributes its partitions among its consumers.