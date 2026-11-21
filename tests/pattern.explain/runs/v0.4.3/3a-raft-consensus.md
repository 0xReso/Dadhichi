# Raft: How a Group of Servers Agrees on One History

By the end you will know what problem the Raft consensus algorithm solves, how its servers elect a leader and copy a shared list of commands, and why "a majority" is the number the whole design rests on.

## Copies that must not disagree

Suppose you run the ticketing service for a small concert hall. Somewhere in its database sits one number that matters more than any other: how many seats are left. Tonight it reads 40. If that database lives on a single server and the server dies, ticket sales stop. So you keep copies on five servers, in five separate racks, and you call them S1 to S5. If one fails, the other four carry on.

Copies bring a problem of their own. Two customers buy at the same moment, and their requests land on different servers. Messages between servers arrive late, out of order, or not at all, and a server can crash halfway through an update. Without something coordinating them, the five copies drift apart: one says 39 seats left, another says 38, a third still says 40. Worse, nothing tells you which one is right.

Raft is a set of rules that stops this drift. It was published in 2014 by two researchers at Stanford University, with the stated aim of being easier to understand than the methods that came before it, and it now runs inside many widely used databases and coordination services. A group of servers running Raft together is called a cluster. Yours has five members.

The central move is to stop sharing the number and share the list of changes instead. Each server keeps an ordered list of commands: "set seats_left to 40", then "set seats_left to 39", and so on, in a fixed order. This list is called the log. If every server holds the same log and carries out its commands in the same order, starting from the same empty database, every server ends up with the same database. Nobody has to compare the numbers themselves; agreeing on the log is enough.

The program on each server that carries out the commands, here the ticket database, is called the state machine. Many servers each running their own copy of it, all fed from the same log, is called a replicated state machine. It is the arrangement Raft exists to serve.

That reduces the whole problem to one question: how do five servers agree on what goes into the log, and in what order, while some of them crash and some messages go missing? Getting a group of machines to agree on something despite failures is called consensus, and Raft is a consensus algorithm.

The number Raft leans on is a majority: more than half the cluster. With five servers, a majority is three. Raft never needs all five to agree on anything; any three will do. This works because any two groups of three, drawn from the same five servers, must share at least one member, since two separate groups of three would need six servers. That shared server is a witness that carries each decision from one group to the next. It also sets how much failure the cluster survives: as long as three servers are working, two can be down.

Agreement among any three still leaves something open, though: who proposes what goes into the log next?

## Choosing a leader

You now hold a cluster of five servers, each with a log, and the rule that any three of them can make a decision. What remains is who decides the order of new commands.

Raft's answer is that one server at a time is in charge. Every new command goes to it, it decides where in the log the command goes, and it tells the others. That server is the leader. Every other server is a follower: it accepts what the leader sends, and if a customer's request reaches it, it points the request at the leader. When your story starts, S1 is the leader and S2 to S5 are followers.

A leader has to keep proving it is alive. Even when no tickets are selling, it sends every follower a short "still here" message many times a second, every 50 milliseconds for instance. These messages are called heartbeats.

Each follower runs a timer that restarts whenever a heartbeat arrives. If the timer runs out with no heartbeat, the follower concludes the leader is gone. This waiting period is called the election timeout. The Raft paper's example picks it at random between 150 and 300 milliseconds, about the length of a blink, and each server draws a fresh random value every time it restarts its timer. The randomness matters: it makes it unlikely that several followers give up on the leader at the same instant.

Raft also divides time into numbered stretches. Each stretch begins with an election and has at most one leader, and the number of the stretch only ever goes up. This number is called the term. Every server remembers the highest term it has seen, and every message a server sends carries that number. S1 is leader in term 1.

Now S1 crashes. The heartbeats stop. S3's timer happens to run out first, at 180 milliseconds, while S2's is set for 240, S4's for 270 and S5's for 210. S3 raises its term to 2, votes for itself, and asks the others to vote for it. A server in this in-between state, asking for votes, is called a candidate.

The request goes out in a message called RequestVote. Each server gives at most one vote per term, to the first candidate that asks, and writes that vote to disk before replying, so that a restart cannot trick it into voting twice. S2, S4 and S5 have not voted in term 2 yet, so all three say yes.

S3 now has four votes, its own and three others, which is more than the three it needs. It becomes the leader of term 2 and starts sending heartbeats, which reset everyone else's timers before they can start elections of their own. Because each server votes once per term and a win takes three votes, two candidates can never both win the same term: their two groups of three voters would have to share a server that voted twice.

Sometimes nobody wins. If two followers time out almost together, the votes can split, say two and two with one server down, and neither candidate reaches three. Each candidate's timer then runs out again, with a new random value, and the first to expire starts a fresh election in the next term. The randomness makes a repeat tie unlikely, so this usually settles within one or two rounds.

One more rule ties terms together. Whenever a server receives a message carrying a higher term than its own, it adopts that term at once, and if it was a leader or a candidate, it becomes a follower. A message carrying a lower term than the receiver's is rejected. This is how a leader that was cut off or frozen for a while learns, the moment it hears from anyone, that it has been replaced.

S3 now leads term 2. How does it get a new command into the other servers' logs?

## Copying a command across the cluster

S3 has won the election for term 2. S1 is still down, and S2, S4 and S5 are following S3's heartbeats. All four running servers hold the same six commands in their logs, and the database on each says 40 seats left.

A customer buys a seat. The request arrives at S3 as the command "set seats_left to 39". S3 adds it to the end of its own log and records next to it the current term, 2. A command stored together with the term in which the leader received it is called a log entry, or entry.

Every entry also has a position in the log, counted from 1. This new one sits at position 7. That position is called the entry's index.

S3 sends the new entry to each follower in a message called AppendEntries. It is the same message type as a heartbeat: a heartbeat is an AppendEntries that carries no entries. Each follower that receives the entry writes it to its own log on disk and replies that it has done so. At that moment, S5's network connection drops, and S5 never receives the message.

S2 and S4 both reply. Counting itself, S3 now knows that entry 7 is stored on three of the five servers, a majority. At that point the entry is committed. Raft guarantees that a committed entry will stay at its index for good and will eventually be carried out by every server in the cluster. Inside one data centre a network round trip takes well under a millisecond, so with the disk writes included, the whole exchange typically takes a few milliseconds.

Only now does S3 carry out the command on its own database, which drops seats_left to 39, and tell the customer the sale went through. Carrying out a committed entry's command on the state machine is called applying it.

S2 and S4 have entry 7 in their logs, but they do not yet know it is committed, so they have not applied it. The leader keeps track of the highest index it knows is committed and includes that number in every AppendEntries it sends, heartbeats included. When S2 and S4 see that entries up to index 7 are committed, they apply entry 7, and their databases also read 39. A follower applies an entry only once it knows the entry is committed, never merely because the entry is stored.

This is where most people's picture of Raft goes wrong. "Committed" sounds like "every server has it". It means a majority has it. Right now S5 still says 40 seats left, and for a few milliseconds S2 and S4 may say 40 as well, because they have stored entry 7 but not yet applied it. An application that reads from whichever server happens to be nearest can tell a customer a seat is free after it has been sold. The current answer comes from the leader. Reading from a follower is safe only when the application can accept an answer that lags a little behind.

S5 has missed entry 7, and S3 is the one server that knows exactly what has been committed. What happens if S3 crashes now?

## Changing leaders without losing anything

You hold the normal path now: the leader appends an entry, a majority stores it, and it becomes committed. Entry 7, "set seats_left to 39", sits on S2, S3 and S4; S5 missed it; S1 is still down.

Now S3 crashes, and S5's network connection comes back. Three servers are running: S2, S4 and S5. Three is a majority, so they can elect a new leader. But S5's log ends at index 6. If S5 became leader, its log would become the cluster's truth, and entry 7, a sale the customer was told had succeeded, would disappear.

Raft blocks this with one extra condition on voting. Every RequestVote carries the index and term of the candidate's last entry. A voter refuses if its own log is more up to date than the candidate's, meaning its own last entry has a higher term, or the same term and a higher index. This condition is called the election restriction.

Watch it work. S5 hears no heartbeats, so its timer runs out first. It moves to term 3 and asks for votes. Its last entry is at index 6 with term 1. The last entry on S2 and on S4 is at index 7 with term 2, a higher term, so both refuse. S5 has only its own vote. S2 and S4 do adopt term 3, because the request carried it, but there is still no leader.

Next, S2's timer runs out. It moves to term 4 and asks. Its last entry is at index 7 with term 2. S4's log ends at the same place, so S4 has no reason to refuse and says yes. S5's log is behind S2's, so S5 says yes too. S2 becomes the leader of term 4 with three votes.

This outcome is not luck. A committed entry is stored on a majority of servers. A winning candidate needs votes from a majority. The two majorities share at least one server, and that server holds the committed entry and refuses any candidate whose log is missing it. The Raft paper proves that, as a result, every new leader already holds every committed entry. Elections can pick different winners, but none of them can erase a sale that was confirmed.

S2 still has to bring S5 up to date. Every AppendEntries names the index and term of the entry just before the new ones it carries, and a follower accepts the message only if its own log has an entry at that index with that term. If not, it rejects the message. This is called the consistency check.

S2 starts by assuming S5 is up to date and sends a heartbeat that says, in effect, "the entry before this point is index 7, term 2". S5 has no index 7, so it rejects. S2 steps back one place and sends entry 7 itself, labelled "the entry before this is index 6, term 1". S5 has exactly that, so it accepts and appends entry 7. Once it sees from S2 that index 7 is committed, it applies it, and its database finally reads 39.

One match is enough because of a guarantee Raft keeps: if two logs hold an entry with the same index and the same term, every entry before it is identical too. So when S5 confirms it has index 6 with term 1, it has also confirmed that indexes 1 to 5 agree, and nobody has to compare whole logs.

What happens when a follower holds entries the leader has never seen, and which failures can Raft not survive at all?

## Where Raft stops: partitions, outages and its other limits

You now hold the full cycle: elections ordered by terms, replication that commits on a majority, and the voting rule and consistency check that keep committed entries safe when the leader changes. S2 leads term 4, S1 and S3 have restarted and been caught up the same way S5 was, and all five servers hold entries 1 to 7.

Then a network fault splits the cluster in two. S2 and S5 can still reach each other, but neither can reach S1, S3 or S4, and those three can reach only each other. A split like this is called a network partition.

On the small side, S2 still believes it is the leader of term 4, because nothing has told it otherwise. A customer's request reaches it: "set seats_left to 38". S2 stores it at index 8 with term 4 and sends it to S5, which stores it too. That makes two copies out of five, never a majority, so the entry is never committed, and the customer waits without ever receiving a confirmation. This is deliberate: the minority side stalls rather than accepting writes it cannot make safe.

On the large side, S1, S3 and S4 stop hearing heartbeats. S4's timer runs out first; it moves to term 5 and wins with votes from S1 and S3. Another customer buys through S4, and "set seats_left to 38" goes in at index 8 with term 5, is stored on all three, and is committed. For a while two servers each think they are leader, but in different terms, and only the one with a majority behind it can commit anything.

Then the network heals. S4's next heartbeat, carrying term 5, reaches S2. S2 sees the higher term and becomes a follower. When S4 sends entry 8, the consistency check passes at index 7, but S2 already holds a different entry at index 8, one with term 4 rather than 5. Raft's rule here is that a follower deletes a conflicting entry, and everything after it, and takes the leader's instead. S2 and S5 drop their uncommitted index 8 and store S4's. Nothing that was promised is lost: the customer who wrote to S2 never got a confirmation and needs to try again.

The partition also shows the trap from the replication step in a sharper form. While it was cut off, S2 could have answered a read with "39 seats left" when the true figure, on S4's side, was 38. Here the stale answer comes from a leader, not a follower, because it does not know it has been replaced. The Raft paper's remedy is that before answering a read, a leader exchanges heartbeats with a majority to confirm no newer leader exists. S2 could not reach a majority, so under that rule it would have refused to answer. Systems built on Raft usually offer this checked kind of read, sometimes alongside a faster unchecked one, so it is worth knowing which one your application uses.

The majority rule also sets a hard limit on outages. Five servers survive two failures. If three are down, the two that remain can neither elect a leader nor commit an entry, and the cluster stops accepting writes until enough servers return. It stops rather than giving wrong answers, but it does stop. Even sizes buy nothing extra: four servers need three for a majority, so they survive only one failure, the same as three servers. This is why clusters of this kind usually have three or five members.

Raft's safety also depends on its disk writes. Every server saves its current term, its vote and its log to disk before replying to anyone. A server that crashes and restarts with its disk intact rejoins as a follower and is caught up through the consistency check, as S1 and S3 were.

Raft assumes servers fail by stopping, going silent or running slowly, and that messages can be delayed or lost. It does not assume servers lie. A server with a serious bug, or one controlled by an attacker, that sends false terms or forged entries can break its guarantees. Defending against servers that actively misbehave takes a different family of algorithms, which are more complex and slower.

Finally, agreement has a price. Every write waits for a majority to store it on disk, so it costs at least one network round trip plus disk writes before the customer hears back. Inside one data centre that is a few milliseconds. Spread the five servers across continents and each write takes tens to a couple of hundred milliseconds, which is why such clusters are usually kept within one region.

## The whole picture

Raft exists so that several servers can behave like one reliable machine, and it does that by having them agree on a single ordered log of commands, which each server applies to its own copy of the state machine. One leader at a time decides the order; it is chosen by election, with randomised timeouts to avoid ties and numbered terms so that an old leader can always be recognised and stood down. The leader copies each entry to the followers and counts it committed once a majority has stored it, and only committed entries are applied. Because any two majorities share a server, the election restriction ensures every new leader already holds every committed entry, and the consistency check then repairs any follower that fell behind or holds entries that never committed. The same majority rule marks the limits: the cluster survives a minority of failures and stalls without one, committed is not the same as present everywhere, and a read is current only when it comes from a leader that has confirmed it is still the leader.

## Going further

- Snapshots, also called log compaction: a way for each server to replace the old part of its log with a saved copy of the database, so the log does not grow forever.
- Membership changes: the procedure for adding or removing servers in a running cluster without ever letting two different majorities make decisions at once.
- Paxos: an older and widely used consensus algorithm solving the same problem, known for being harder to understand, which is the difficulty Raft set out to remove.
- etcd: a widely used open-source store of settings and coordination data that keeps its copies in agreement using Raft, and a readable place to see the ideas here in production code.
