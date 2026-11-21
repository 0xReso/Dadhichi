# Kafka Consumer Groups

By the end you will know how Kafka lets several copies of a program share the work of reading one stream of data, why that sharing has a hard ceiling, and what happens when one of the copies fails.

## One reader cannot keep up

Kafka is a system for passing streams of messages between programs. One program writes a message, such as "order 1042 was placed", and Kafka stores it in order on its servers. Other programs read it whenever they are ready. The writer and the readers never talk to each other directly, so each can work at its own pace, and a reader that falls behind does not slow the writer down.

Say you run an online shop. Every order your website takes becomes a message in Kafka: about 3,000 an hour on a quiet day, and about 30,000 an hour during a sale. A program you wrote, the invoice service, reads each order and emails the customer a PDF invoice. In Kafka's vocabulary, any program that reads messages is a consumer, so the invoice service is a consumer.

Making and sending one invoice takes about half a second, so one copy of the invoice service handles about 7,200 orders an hour. On a quiet day that is plenty. During a sale the backlog grows by almost 23,000 orders every hour, and customers wait half a day for an invoice.

The natural fix is to run several copies of the invoice service. That raises two problems at once. If three copies all read the same stream, something has to stop every customer from receiving three invoices. And if the copies split the work, each one needs to know which orders are its own and where it left off.

How can Kafka hand one stream to several readers without any order being read twice?

## Topics, partitions and offsets

You have a stream of orders that one copy of the invoice service cannot keep up with, and you want several copies to share it without doubling up. The answer starts with how Kafka lays a stream out.

Kafka keeps messages in named streams called topics. Your shop writes every order to a topic named `orders`. You create a topic once, and any number of programs can then write to it or read from it.

A topic is not stored as one long line. It is split into several independent lines called partitions, each an ordered sequence of messages kept on disk. When you created `orders` you gave it six partitions, numbered 0 to 5. Each new order goes onto exactly one of them. Your website labels each order with the customer's ID, and by default Kafka sends every message with the same label to the same partition, so one customer's orders always sit in one line. Kafka keeps messages in order within a partition, but makes no promise about order across different partitions.

Each message in a partition gets a position number, starting at 0 and rising by one for every new message. That number is called the offset. Partition 3 of `orders` might hold offsets 0 to 48,999, and the next order to arrive there becomes offset 49,000. Offsets are counted separately in each partition, so partition 4 has its own offset 0, its own offset 1, and so on.

Reading a message does not remove it. Kafka keeps messages for a set period, seven days by default, whether anyone has read them or not. This is the main difference from a traditional queue, where taking a message out means it is gone. A Kafka consumer instead asks for something like "partition 3, starting at offset 48,500", and Kafka sends back the messages from that point on. What a reader owns is a position in a line, not a share of a pile that empties.

With six partitions to hand out and several copies of the invoice service asking for work, who decides which copy reads which partition?

## How a group divides the work

The `orders` topic is six partitions, each an ordered line of messages with numbered offsets, and reading a message leaves it in place. What is still missing is a way for several copies of the invoice service to divide those six lines between them.

Each copy of the invoice service is started with the same name in its settings: `invoice-service`. That shared name is called the group ID.

Consumers that share a group ID form a consumer group, and Kafka treats the whole group as one reader of the topic. Within a group, Kafka assigns each partition to exactly one member. A member can hold several partitions, but a partition belongs to one member of the group at a time. With three copies running, each gets two: the first copy reads partitions 0 and 1, the second reads 2 and 3, the third reads 4 and 5. No order is handled twice, because each partition has a single reader, and the group now handles about 21,600 orders an hour.

The bookkeeping is done by one of Kafka's servers, which acts as the group coordinator for this group. It keeps the list of current members and makes sure each one receives its share of partitions. Every group has a coordinator, and different groups can have different servers in that role.

Sale day brings 30,000 orders an hour, so you run six copies. Each now holds one partition, and the group can handle about 43,200 orders an hour. To be safe you start a seventh copy, and here is where many people's picture of Kafka goes wrong. The seventh copy receives nothing, because there are only six partitions to give out and each can have only one reader in the group. It sits idle. Adding consumers to a group speeds it up only until there is one consumer per partition; past that point, extra members are spare capacity waiting for someone to fail. The number of partitions is the ceiling on how many consumers in one group can work at once, which is why it is worth choosing that number generously when a topic is created. You can add partitions later, but doing so changes which partition each customer's orders land on from then on.

Meanwhile your analytics team wants to see every order too. Their program uses a different group ID, `analytics`. Because it is a separate group, Kafka assigns it all six partitions as well, with no regard for what `invoice-service` is doing. This is the second half of the design. Within one group, each message goes to one member, so the members share the work. Across groups, every group receives every message, so several unrelated programs can each read the full stream without disturbing one another.

Each member now reads its own partitions, but how does it remember where it stopped, and what happens to its partitions if it crashes?

## Keeping your place, and recovering from failure

Your six copies of the invoice service each hold one partition of `orders`, a seventh waits idle, and the analytics group reads the same six partitions on its own. Two things remain: how each member keeps its place, and what happens when a member disappears.

As a member works through its partition, it regularly tells Kafka how far it has got, along the lines of "group `invoice-service` should resume partition 3 at offset 48,500". That stored position is the committed offset. Kafka keeps one committed offset for each group on each partition, so on partition 3 `analytics` might be at 30,000 while `invoice-service` is at 48,500, and neither affects the other. By default the consumer software commits automatically every five seconds; many applications switch that off and commit themselves after the work is truly finished.

Each member also sends the coordinator a small "still here" signal every few seconds. These signals are called heartbeats. If the coordinator hears none from a member for a set time, 45 seconds by default in recent versions, it declares that member gone.

Whenever a member joins, leaves, or is declared gone, the group redistributes its partitions. This is called a rebalance. Suppose the copy holding partition 3 crashes after handling orders up to offset 48,619, while its last commit said 48,500. About 45 seconds later the coordinator notices the silence and starts a rebalance. Partition 3 goes to the idle seventh copy. That copy asks Kafka for the group's committed offset on partition 3, gets 48,500, and starts reading from there.

The crashed copy had already sent invoices for offsets 48,500 to 48,619, but never committed them, so the new owner handles all 120 of those orders again and 120 customers get a second invoice. Under the usual setup, where work is done first and the offset committed afterwards, this is the trade Kafka makes: no message is skipped after a failure, but some may be processed twice. That guarantee is called at-least-once delivery. The common defence is to make the work safe to repeat, for example by checking whether an invoice for that order ID has already gone out. Committing before doing the work flips the risk: no duplicates, but a crash can lose orders that were committed and never invoiced.

A rebalance has a cost of its own. With the classic way of rebalancing, members of the group pause reading while partitions are reassigned. A member that takes too long between requests for new messages, five minutes by default, is also treated as stuck and removed, which triggers another rebalance. A service whose individual jobs are slow can therefore fall into a cycle of being removed, rejoining, and pausing the whole group, and this is one of the most common problems teams run into with consumer groups in production.

## The whole picture

A Kafka topic is split into partitions, each an ordered line of messages with numbered offsets that stay put after being read. A consumer group is a set of consumers sharing a group ID, and Kafka, through a group coordinator, gives each partition to exactly one member, so the members share the work while one customer's orders still arrive in order. Because a partition cannot be split within a group, the partition count caps how many members can do useful work, and every extra member waits as a spare. Each group keeps its own committed offset per partition, which lets separate groups read the same stream independently and lets a new member pick up exactly where the last commit left off after a rebalance. The price of that recovery is that work done after the last commit may be done again, so consumers are built to handle the same message twice safely.

## Going further

- Cooperative rebalancing: an assignment strategy in which only the partitions that actually need to move are taken away, so the other members keep reading during a rebalance.
- Static membership: giving each consumer a fixed identity in its settings, so that a quick restart within the timeout does not trigger a rebalance at all.
- Consumer lag: the gap between the newest offset in a partition and the group's committed offset, which is the usual number for checking whether a group is keeping up.
- Share groups: a newer kind of group in which several consumers can read from the same partition, queue-style, which removes the one-reader-per-partition ceiling at the cost of the per-partition ordering.
