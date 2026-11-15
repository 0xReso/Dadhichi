# Kafka Consumer Groups

By the end you will know how Apache Kafka lets many copies of a program share a stream of messages without doing the same work twice, and where that arrangement tends to surprise people.

## The problem: one stream, too much work

Picture an online grocery shop. Every time a customer checks out, the shop's website announces it: "order 81,442 was placed, three items, 24 euros." Several other programs care about that announcement. One produces the invoice. One sends the confirmation email. One updates the warehouse stock count. On a busy evening the shop takes about 1,200 orders a minute, twenty every second.

The website should not have to call each of those programs directly, wait for each one, and retry when one is down. It would rather drop the announcement somewhere durable and move on, and let each interested program pick it up in its own time. That "somewhere" is the job Apache Kafka does. Kafka is a system of servers that stores streams of messages and hands them to whoever wants to read them.

Now the hard part. Suppose producing an invoice takes a quarter of a second. One copy of the invoice program can then manage four orders a second, and orders arrive at twenty. You need about five copies running side by side. The moment you have five copies, you have two new questions. How do they split the orders so that each order is invoiced exactly once and not five times? And when one copy crashes halfway through the evening, who picks up its share?

A consumer group is Kafka's answer to both questions. Before it makes sense, you need three ideas about how Kafka stores messages.

## How Kafka stores a stream

Kafka keeps messages in a named stream called a topic. The shop's checkout announcements go into a topic called "orders". A program that writes messages into a topic is a producer; here, the website. A program that reads them is a consumer; here, the invoice, email and stock programs.

The first thing that surprises newcomers is that reading a message does not remove it. A topic behaves like a log book that only ever gets new lines added at the end. Messages stay for as long as the topic is configured to keep them, commonly seven days, whether or not anyone has read them. This is different from a classic message queue, where a message is taken off the queue once someone handles it. Hold onto this, because the rest of the design depends on it.

The second idea is that a topic is split into several independent logs, called partitions. The "orders" topic might have six partitions, numbered 0 to 5. Each new order goes into exactly one of them. Usually the producer chooses the partition from a key attached to the message; if the shop uses the customer's ID as the key, every order from the same customer lands in the same partition. Partitions exist so that the work can be spread out: different partitions can live on different Kafka servers, and, as you will see, different consumers can read them at the same time.

Kafka guarantees order only within a partition. Within partition 3, messages come out in the order they went in. Across partitions there is no overall order at all. Keying by customer ID is what makes sure one customer's orders are seen in sequence.

The third idea is the offset. Every message in a partition gets a sequence number, starting at 0 and counting up: the first message in partition 3 is offset 0, the next is offset 1, and so on. An offset only means something together with its partition; offset 500 in partition 3 and offset 500 in partition 4 are unrelated messages.

Because messages are not removed on reading, a consumer has to keep track of where it is, the way you keep a bookmark in a book that other people are also reading. That bookmark is an offset. "I have handled partition 3 up to offset 499" means the next thing to read is offset 500.

So a topic is a set of partitions, each partition is an ordered log, and a reader's position is an offset per partition. With those in hand, the consumer group is almost a direct consequence.

## What a consumer group is

The shop now has five copies of the invoice program and wants them to act as one team. Each copy is configured with the same name, say "billing". Every consumer that starts up with the group name "billing" joins the same consumer group. The group name is the only thing that ties them together; there is no separate registration step.

Kafka then applies one rule: within a group, each partition is read by exactly one consumer at a time. The partitions are dealt out among the members like cards. With six partitions and three consumers, each consumer gets two partitions. That handing-out is called partition assignment.

That one rule answers the first question from the start. Every order sits in exactly one partition, and every partition has exactly one reader in the group, so every order is handed to exactly one member of "billing". Nobody needs to coordinate per message. The split happens once, per partition, and then each consumer reads its own partitions independently and as fast as it can.

It also keeps the ordering promise intact. Since one customer's orders all live in one partition, and one partition has one reader in the group, a single consumer sees that customer's orders in order.

## Many groups, one topic

The email program and the stock program also want every order. They each form their own group: "emails" and "stock". Here the rule works the other way round. Different groups do not share anything. Each group gets the entire topic, every partition, and keeps its own bookmarks.

This is the second half of the idea, and the part people new to Kafka most often miss. Within a group, messages are divided. Between groups, messages are copied. "billing" invoices each order once; "emails" sends one email per order; "stock" adjusts the count once per order; and none of them affects the others. If the email program falls an hour behind because the mail provider is slow, billing carries on at full speed, because the two groups have separate offsets on the same unchanging log.

That is possible only because reading does not remove messages. A fourth team could start a new group next week called "fraud-check", tell it to begin from the oldest message still kept, and work through the last seven days of orders without anyone else noticing.

So a consumer group behaves like a queue for its members, where work is shared out, and like a broadcast between groups, where everyone gets everything. Kafka gets both behaviours from the same mechanism.

## The trap: more consumers than partitions

Back to the invoice program. It is falling behind, so someone scales "billing" from three copies to ten. Throughput barely moves.

The reason is the rule from earlier. A partition is read by one consumer in the group at a time, and the "orders" topic has six partitions. Six consumers get one partition each. The other four get nothing and sit idle, connected and healthy but doing no work. They are not useless, since they take over if an active member dies, but they add no speed.

The number of partitions is therefore the ceiling on how many consumers in one group can work at once. This is the most common misunderstanding about consumer groups: that adding consumers always adds capacity. It only does until you have one consumer per partition. Past that, you need more partitions, and that is a decision best made early. You can add partitions to an existing topic, but doing so changes which partition a given key maps to, so new orders for a customer may start landing in a different partition from their older ones, and the per-customer ordering you were relying on can break across the change.

The opposite situation is fine. With six partitions and two consumers, each consumer reads three partitions. Fewer consumers than partitions simply means each one carries more.

## Bookmarks that survive a crash

You now know how a group splits the work. The second question from the start was what happens when a member fails. The answer begins with where the bookmarks live.

A consumer keeps its current position in memory while it runs, but memory vanishes in a crash. So from time to time the consumer tells Kafka, "for group billing, partition 3, I am done up to here." That act is called committing an offset. Kafka stores committed offsets in a special internal topic named "__consumer_offsets", keyed by group, topic and partition. Because they are stored by group and not by individual consumer, whoever reads partition 3 for "billing" next can look up where the group left off.

When a consumer is given a partition, it reads the group's committed offset for that partition and starts from there. If the group has never committed anything for that partition, for example a brand-new group, a setting called auto.offset.reset decides: "earliest" means start from the oldest message still kept, and "latest", the default, means ignore the history and start with whatever arrives next. The "fraud-check" team reading the past week would set it to "earliest".

One detail of wording trips people up. The committed offset is the offset of the next message to read, not the last one handled. A consumer that has finished offset 499 commits 500. Client libraries normally take care of this for you, but it explains why the numbers in monitoring tools look one higher than expected.

## When you commit decides what can go wrong

When to commit is the decision that matters most in practice, because a crash can always land between handling a message and committing it.

By default, the standard Java client commits automatically in the background, every five seconds, for the messages it has handed to your code. That is convenient but loose. Suppose a billing consumer reads orders up to offset 520 in partition 3, the automatic commit records 521, and then the consumer crashes while still working on order 515. The next reader starts at 521. Orders 515 to 520 were never invoiced, and nothing will retry them.

The safer common pattern is to turn automatic committing off and commit yourself, only after the work is done. Now the failure goes the other way. The consumer finishes invoices 500 to 520, crashes a moment before committing, and the next reader starts again from the last committed offset, 500. Twenty-one invoices are produced twice.

Those two outcomes have names. Committing before or regardless of the work gives at-most-once delivery: nothing is repeated, but things can be lost. Committing after the work gives at-least-once delivery: nothing is lost, but things can repeat. At-least-once is the usual choice, and the program is then written so that a repeat does no harm, for instance by having the invoice program check whether an invoice for that order already exists before creating one. A program that can safely handle the same message twice is called idempotent.

Consumer groups on their own do not give you exactly-once processing. Kafka does offer transactions that can make reading, processing and writing results back into Kafka happen as one unit, but that guarantee covers results that stay inside Kafka. Once your consumer sends an email or charges a card in some other system, avoiding duplicates is your program's job.

## How the group notices a failure

The last piece is how membership changes are detected and handled.

For each group, one of the Kafka servers takes the role of group coordinator. Every consumer in the group sends it small "still alive" signals, called heartbeats, every few seconds. If the coordinator hears nothing from a consumer for longer than the session timeout, 45 seconds by default in recent versions, it declares that consumer dead.

There is a second check, because a consumer can be alive yet stuck. Consumers fetch messages in a loop by calling a function named poll. If your code takes longer than max.poll.interval.ms between two polls, five minutes by default, the consumer is considered to have stalled and is removed from the group even though its heartbeats were fine. This catches a billing consumer that has hung on a slow payment service. It also catches a healthy consumer that grabbed too large a batch of slow messages, which is a frequent cause of mysterious group churn.

## Rebalancing

Whenever membership changes, the partitions have to be dealt out again. A consumer joins, a consumer leaves cleanly, a consumer is declared dead, or the topic gains partitions: in each case the group goes through a rebalance, a fresh round of partition assignment.

Take the shop's three billing consumers, A, B and C, two partitions each. C crashes. After the timeout, the coordinator starts a rebalance, and C's partitions 4 and 5 go to A and B. Each of them looks up the group's committed offsets for its new partitions and carries on from there, re-reading anything C handled but never committed. This is the at-least-once behaviour from before, now seen from the side of the consumer taking over.

How disruptive a rebalance is depends on the version and settings, and this is an area that has changed a lot.

In the original scheme, often called eager rebalancing, every consumer in the group gives up all its partitions, the group agrees on a new assignment, and then everyone resumes. During that pause the whole group reads nothing, even consumers whose partitions end up unchanged. In a large group this stop-the-world pause can last seconds or longer, and a group that keeps rebalancing can make very little progress.

The newer cooperative, or incremental, rebalancing only takes away the partitions that actually need to move. In the example, A and B keep reading their own partitions throughout, and only partitions 4 and 5 are handed over. In the classic protocol the actual assignment is calculated by one of the consumers, elected as group leader, and the coordinator passes the result on. Kafka 4.0 made a redesigned consumer group protocol generally available in which the coordinator itself computes assignments and changes them incrementally, so consumers no longer need to stop together. Which behaviour you get depends on your Kafka version and client settings, so it is worth checking rather than assuming.

There is also a way to avoid needless rebalances during planned restarts. Normally a consumer that restarts comes back as a new member, which triggers two rebalances: one for leaving, one for rejoining. With static membership, each consumer is given a fixed identity through a setting called group.instance.id. A consumer that disappears and returns with the same identity within the session timeout simply gets its old partitions back, and the rest of the group is undisturbed.

## The whole picture

Kafka stores each topic as a set of partitions, each one an ordered log that is kept whether or not anyone reads it, so every reader needs its own bookmark, an offset per partition. A consumer group is a set of consumers sharing a name and a set of bookmarks. Kafka gives each partition to exactly one member of the group, which shares the work out without per-message coordination, keeps ordering within a partition, and caps useful group size at the partition count. Separate groups read the same log independently, so one topic can feed billing, email and stock at once. Committed offsets in "__consumer_offsets" let a replacement pick up where a failed member stopped, and the group coordinator's heartbeats and rebalances make that hand-over automatic, at the cost of possible repeats that your code must be ready to tolerate.

## Going further

Consumer lag: how far a group's committed offsets trail the newest messages in each partition, the main number people watch to see whether a group is keeping up.

Partition assignment strategies: the rules that decide which consumer gets which partitions, such as range, round-robin, sticky and cooperative-sticky in the classic protocol.

Kafka transactions and exactly-once semantics: the producer and consumer features that let a read-process-write cycle inside Kafka commit as a single unit.

KIP-848: the Kafka Improvement Proposal behind the newer consumer group protocol, worth reading when you need to know exactly how rebalancing works in your version.
