# Raft: How a Group of Servers Agrees on One History

By the end you will know what Raft is, why it exists, how it elects a leader and copies changes safely across several servers, and the mistake people most often make about it.

## One copy is fragile, several copies disagree

Suppose you run an online shop, and one small program holds the settings everything else depends on: how many umbrellas are in stock, which warehouse is open, which payment provider is switched on. If that program lives on a single machine and the machine dies, the shop stops. The obvious fix is to keep copies on several machines.

Copies bring a new problem. Two requests arrive a moment apart: one sets the umbrella stock to 40, the other to 35. If one machine applies them in one order and another machine in the opposite order, the two now disagree, and nobody can say which is right. Messages between machines can also be delayed, lost, or delivered to a machine that crashed and restarted in the meantime. Getting several machines to settle on the same answer despite all of that is called consensus.

Raft is a set of rules for reaching consensus. It was designed at Stanford University and published in 2014, with the stated aim of being easier to understand than the older methods that did the same job. Today it runs inside many databases and coordination services that have to keep working when a machine fails.

The machines that run Raft together form a cluster. A cluster usually has three or five servers. The example in this article has five, which we will call A, B, C, D and E.

Raft leans on an old and simple idea. If every server starts from the same data, and every server carries out the same commands in the same order, every server ends up with the same data. A program that changes its data only by carrying out commands in this way is called a state machine, where "state" means the data the program is holding at any moment. In the shop, the state machine is a small store of settings, and a command is something like "set umbrellas to 40".

That shrinks the whole problem to a single question: how do five servers, any of which may be crashed or unreachable at a given moment, agree on one ordered list of commands?

## The log and the leader

You now have five servers that will stay identical as long as they carry out the same commands in the same order. Raft's work is to give them that order.

Each server keeps the commands it has received in an ordered list, written to disk so that it survives a restart. This list is called the log.

One command in the log, together with a little bookkeeping that travels with it, is called an entry.

Entries are numbered from 1 upward, and an entry's number is its index. When two servers both hold an entry at index 7, Raft's goal is that it is the same command on both.

Raft does not let all five servers accept commands. One server at a time is the leader, and every change goes through it. Putting one server in charge of the order settles the argument from the opening: whichever of "40" and "35" reaches the leader first gets the lower index, and that order becomes everyone's order.

The other servers are followers. The programs that want to read or change settings, here the shop's website, are called clients, and followers do not take commands from them. If a client contacts a follower, the follower normally tells it which server is the leader. A follower's job is to receive entries from the leader, store them, and reply.

The leader sends new entries to the followers in a message called AppendEntries. One message can carry several entries, and the leader keeps resending to any follower that has not answered.

Here is the cluster at work. A is the leader, and every server's log holds the same six entries. The website sends "set umbrellas to 40" to A. A writes it into its own log at index 7 and sends an AppendEntries carrying that entry to B, C, D and E.

A cannot tell the website the change is done the moment it writes it down, because A might crash a second later holding the only copy. So when is an entry safe?

## Majorities and commitment

A, the leader, has written "set umbrellas to 40" at index 7 of its log and sent it to the four followers. Now it waits for replies.

Raft's measure of safety is a majority: more than half of the servers in the cluster. The count is always against the cluster's full membership, never against whoever happens to be running at the moment. In a five-server cluster, a majority is three. Practitioners often call this number a quorum.

Majorities matter because any two majorities of the same cluster share at least one server. Three plus three is six, and there are only five servers, so some server must be in both groups. Whatever one majority did, at least one member of any other majority was there for it.

Back to the example. B and C store the entry and reply within a few milliseconds. D runs on an overloaded machine, and A's message to it has been lost; A will retry. E is switched off for maintenance. A counts the servers that hold index 7: itself, B and C. That is three of five.

Once an entry is stored on a majority, the leader marks it committed. Committed is Raft's central promise: the entry will never be lost or replaced, and every server will eventually hold it at that same index.

Only a committed entry may change anyone's data. Carrying out an entry's command on a server's own copy of the settings is called applying it. A applies index 7, so its store now says umbrellas are 40, and only then does it answer the website: done. Each AppendEntries also tells the followers the highest index the leader has committed, so B and C learn with A's next message that index 7 is committed, and apply it then.

The whole exchange takes a few milliseconds inside one data centre, since a round trip there is well under a millisecond and the main cost is each server writing the entry to disk.

The majority rule also sets how many failures a cluster can survive. Five servers keep working with two down, because the remaining three are still a majority. Three servers survive one failure. Four servers need three for a majority, so they also survive only one, which is why clusters almost always have an odd number of servers.

All of this depends on A being the leader. What happens when A is the one that fails?

## Choosing a leader

Index 7, "set umbrellas to 40", is committed and stored on A, B and C, while D missed it and E is switched off. Followers only take entries from a leader, so without one the cluster can store nothing new. And now, before A's retry reaches D, A's machine loses power.

Followers need a way to notice that the leader has gone. While it is alive, the leader sends AppendEntries to every follower several times a second, empty when there is nothing new, meaning only "I am still here". This regular empty message is called a heartbeat.

Each follower runs a timer that restarts whenever a message arrives from the leader. If the timer runs out, commonly after somewhere between 150 and 300 milliseconds, a few blinks of an eye, the follower concludes the leader is gone. This waiting period is the election timeout. Each server picks its timeout at random within the range, afresh every time, so one server's timer usually runs out well before the others'.

Raft divides time into numbered periods, each beginning with an election. The number is called the term. Every server remembers the highest term it has seen, and every message carries its sender's term. A server that receives a higher term than its own adopts it at once, and if it was acting as leader, it goes back to being a follower. Our cluster has been in term 3, with A as its leader.

Each entry records the term in which a leader first added it to the log. Index 7, "set umbrellas to 40", is a term 3 entry, and so are the six before it.

When a follower's election timeout runs out, it raises its term by one, votes for itself, and starts asking the others for their votes. A server in this state is called a candidate. Every Raft server is always in one of three roles: follower, candidate or leader.

The candidate asks for votes in a message called RequestVote, which carries the candidate's term and the index and term of the last entry in its log.

Each server votes at most once per term, for the first candidate that asks, and records its vote on disk so that a restart cannot make it vote twice. A candidate that collects votes from a majority becomes the leader for that term. Since each server votes once per term and any two majorities share a server, two candidates can never both win the same term.

There is one more condition. A server refuses its vote to any candidate whose log is less up to date than its own. To compare, it looks at the last entry in each log: the log whose last entry has the higher term is more up to date, and if the terms are equal, the longer log is.

Watch it work. D's timer happens to run out first. D moves to term 4 and sends RequestVote, saying its last entry is index 6, term 3. B and C both end with index 7, term 3, so D's log is behind theirs, and both refuse. A is dead and E is off. D has only its own vote, one of five, and the election fails. B and C still adopt term 4, because they saw it in D's request.

A moment later C's timer runs out. C moves to term 5 and asks for votes, saying its last entry is index 7, term 3. B's log ends at the same place, so C's log is as up to date as B's, and B votes for C. D has not voted in term 5, and C's log is ahead of D's, so D votes for C too. C now holds three votes, its own, B's and D's, and becomes leader for term 5. Its first heartbeats reach D, and D receives the missing index 7.

The committed entry survived, and not by luck. Being committed meant index 7 sat on a majority. Winning meant collecting votes from a majority. Those two majorities had to share a server, and that server held index 7 and would refuse any candidate missing it. So any server that wins an election already holds every committed entry. The formal proof in the original paper needs a little more care than this, but this is its heart.

Sometimes two timers run out almost together, the votes split, and nobody reaches a majority. The candidates' timers then run out again, at fresh random times, and a new term begins. The random spread usually settles it within a round or two.

You now have a leader, a log and majorities. What happens when the network splits, and the old leader has no way to learn that it has been replaced?

## Two leaders, one history

You now hold Raft's full cycle: the leader copies entries out, a majority makes them committed, and when the leader goes quiet a follower runs in a higher term, winning only if it holds every committed entry. The hardest case for these rules is a leader that is alive but cut off.

Time has passed. A has restarted and rejoined as a follower, E has been switched back on, and both have caught up. All five servers are in term 5, with C as leader.

Then a network switch fails, leaving C and D able to reach each other but not the other three, while A, B and E can still reach one another. A split like this, where both sides keep running but cannot talk across the gap, is called a network partition.

On its side, C has no idea anything changed. It keeps sending heartbeats, and only D answers. The website, still connected to C, sends "set umbrellas to 35". C writes it at index 8, in term 5, and D stores it. That is two servers of five, not a majority, so the entry is never committed. C never applies it and never tells the website it succeeded; the website waits, and eventually gives up or retries elsewhere.

On the other side, A, B and E stop hearing heartbeats. B's timer runs out first. It moves to term 6 and wins the votes of A and E, three of five, so B becomes leader. Another part of the website reaches B and sends "set umbrellas to 38". B writes it at index 8, in term 6, A and E store it, and it is committed.

For these few seconds, C and B both believe they are the leader. This is where people most often go wrong about Raft: they believe it guarantees exactly one leader at any moment. It cannot, because C has no way to learn it was replaced while it is cut off. What Raft guarantees is narrower: at most one leader per term, and only a leader that reaches a majority can commit anything. C, stuck on the smaller side, can accept entries but can never commit them, so the committed history has one author at a time even when two servers hold the title.

The switch is repaired. B's next heartbeat reaches C carrying term 6. C sees a term higher than its own 5 and steps down to follower. But C's index 8 says "35" from term 5, while B's index 8 says "38" from term 6, and the logs must be made to match.

Raft repairs logs with a check built into every AppendEntries. Each one carries the index and term of the entry that sits just before the new entries. A follower accepts the message only if its own log holds an entry with that same index and term. If not, it refuses, and the leader tries again starting one entry earlier, stepping back until it finds the last point where the two logs agree. The follower then deletes everything after that point and takes the leader's entries in their place.

In the example, B's heartbeat to C says "the entry before this point is index 8, term 6". C's index 8 is from term 5, so C refuses. B steps back and sends index 8 itself, saying "the entry before this is index 7, term 3". C's index 7 matches, so C deletes its "35" and stores "38". The same happens on D. Throwing away "35" is safe because it was never committed, and the website was never told it succeeded.

The partition also shows Raft's limits. During the split, if the website had asked C how many umbrellas there were, C would have answered 40 from its own copy, although the committed value was already 38. The rules above protect writes; systems built on Raft usually protect reads too, by having the leader confirm with a majority that it is still the leader before it answers.

Raft also needs a majority to be running and reachable. The smaller side of a partition cannot accept changes at all, and a five-server cluster with three servers down stops taking writes until enough return.

Raft assumes servers fail by stopping or going silent, never by lying. A server that sends false messages, through a bug or an attacker, can break its guarantees, and handling that needs a different and much costlier kind of protocol.

Every change passes through one leader and waits for a majority, so a Raft cluster is kept small, usually three, five or seven servers. Adding servers adds fault tolerance but makes each write wait on more replies.

## The whole picture

Raft lets a small cluster of servers keep one agreed, ordered log of commands, so that every server carrying out that log reaches the same data even when servers crash or the network splits. A single leader decides the order and copies entries out with AppendEntries; an entry becomes committed once a majority stores it, and only then is it applied. When heartbeats stop, a follower's randomised timeout makes it a candidate in a new term, and it wins only with a majority of votes from servers whose logs are no more up to date than its own. Because any two majorities overlap, every new leader already holds every committed entry, and because a leader cut off in a minority can never commit, a stale leader can cause delay and stale reads but never a second history. The consistency check in every AppendEntries then trims away anything uncommitted that a stale leader left behind.

## Going further

- Log compaction and snapshots: a log cannot grow forever, so servers periodically save a copy of their current data and discard the entries that produced it, and a leader can send that snapshot to a follower that has fallen far behind.
- Membership changes: the procedure for adding or removing servers from a running cluster without ever allowing two separate majorities to form during the change.
- The commit rule for earlier terms: a new leader counts copies only of entries from its own term to decide what is committed, and entries from earlier terms become committed along with them; this closes a subtle gap described in the original Raft paper.
- Paxos: the older and famously hard-to-follow consensus method that Raft was designed to be an understandable alternative to.
