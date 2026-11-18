# Raft: How a Group of Servers Agrees on One Story

By the end you will understand how Raft, a widely used consensus algorithm in distributed computing, lets several servers keep identical copies of the same data and carry on working when some of them fail.

## The problem of many copies

Suppose a company keeps one small but critical piece of data: the current price of its product, which every shop and website reads. If that price lives on a single server and the server dies, everything that depends on it stops. The obvious fix is to keep copies on several servers, so that losing one is not a disaster.

Copies bring a new problem. Two people change the price at almost the same moment: one sets it to 40, the other to 45. If one server applies 40 then 45, and another applies 45 then 40, the first ends up saying 45 and the second says 40. Both servers are working correctly, and they now disagree. Anyone reading the price gets a different answer depending on which server they happen to ask.

The way out is to stop thinking about copying the data and start thinking about copying the list of changes. If every server keeps the same ordered list of commands, such as "set price to 40" followed by "set price to 45", and each applies them strictly in that order, every server arrives at the same result. That ordered list is called the log. Each position in it has a number, its index, starting from 1.

A program that turns a sequence of commands into a current value, like the little price database here, is called a state machine. The arrangement as a whole, where every server feeds the same log into its own copy of the same state machine, is called a replicated state machine. From the outside it behaves like one dependable server, even though it is several.

That leaves one hard question: how do several servers, connected by a network that can delay or lose messages, and any of which might crash at any moment, agree on what goes into the log and in what order? Getting a group of machines to agree on a value despite failures is called consensus. Raft is a set of rules for reaching consensus on a log.

Raft was published in 2014 by Diego Ongaro and John Ousterhout at Stanford, in a paper titled "In Search of an Understandable Consensus Algorithm". An older algorithm, Paxos, already solved the same problem, but it had a reputation for being very hard to understand and even harder to build correctly. Raft's stated goal was to be easy to understand, and it splits the problem into a few separate pieces that can each be grasped on their own. It now sits underneath many well-known systems, including etcd, the database that stores the configuration of Kubernetes clusters.

The running example for the rest of this piece is a cluster, the usual word for such a group, of five servers named S1 to S5, all keeping the price log. The question is how five machines can decide together what the next entry in that log is.

## Majorities and a single leader

The idea of keeping an identical log on five servers is now in place; what remains is how they agree on its contents. Raft's answer rests on two ideas, and the first is about counting.

Raft never waits for every server to answer, because a crashed server never will. Instead, a decision counts once more than half of the whole cluster has accepted it. With five servers, that means any three. This group, more than half, is called a majority, and practitioners often call it a quorum.

The reason majorities work is that any two majorities of the same cluster must share at least one server. If three servers accepted one thing, and three servers accepted another, at least one server is in both groups. So a decision made by one majority can never be silently unknown to the next majority: someone in the room always remembers it. Almost every safety property of Raft comes back to this overlap.

Majorities also set how many failures the cluster survives. Five servers keep working with any two of them down, since three are still left to form a majority. Three servers survive one failure. Adding a sixth server does not help: a majority of six is four, so six servers still survive only two failures. That is why clusters are nearly always an odd size, usually three or five.

The second idea is that one server is in charge. At any moment, Raft aims to have exactly one leader. Only the leader accepts new commands from clients, decides where each goes in the log, and sends it to the others. The other servers are called followers; they accept what the leader sends and otherwise stay quiet. Having one leader turns a hard problem, several servers proposing at once, into an easy one: there is only one proposer, so there is only one order.

Leaders can crash, so Raft needs a way to replace them, and a way to tell an old leader from a new one. It does this with a counter called the term. Time in a Raft cluster is divided into terms, numbered 1, 2, 3 and upwards. Each term begins with an election, and at most one leader can win in any given term. Every message between servers carries the sender's current term.

Terms let servers spot stale information. If a server receives a message carrying a higher term than its own, it learns that it has fallen behind: it adopts the higher number and, if it believed it was the leader, it steps down and becomes a follower. If it receives a message with a lower term, it rejects it, because it comes from a past that has already been superseded.

In the example, say S1 is the leader in term 2, and S2 to S5 are its followers. The next question is how S1 came to be leader, and what happens when it stops answering.

## Electing a leader

So far there is a cluster of five servers, decisions that need three of them, and one leader per numbered term. Now the leader disappears, and the cluster must find a new one without any outside help.

A leader shows it is alive by sending regular messages to every follower, even when there is nothing new to say. These are called heartbeats. A typical system might send one every 50 milliseconds, around twenty times a second.

Each follower runs a countdown, called the election timeout. Every heartbeat resets it. If the countdown reaches zero without hearing from a leader, the follower concludes the leader is gone. In the Raft paper the example range is 150 to 300 milliseconds, so a follower gives up on a silent leader after roughly a fifth of a second.

Say S1 crashes. S2 to S5 stop receiving heartbeats, and their countdowns begin running out. The first one to reach zero, say S3, starts an election. It increases its term from 2 to 3, moves into a third role called candidate, votes for itself, and sends a message to every other server asking for its vote. That message is named RequestVote.

Each server has one vote per term, written to disk so that a crash and restart cannot make it vote twice. It gives that vote to the first candidate that asks in that term. S2, S4 and S5 each have term 2, see S3's request for term 3, adopt term 3 and grant their vote.

When a candidate collects votes from a majority, counting its own, it becomes the leader for that term. S3 needs three votes; it has its own plus up to three more, so it wins. It immediately sends heartbeats to everyone, which tells them there is a leader for term 3 and stops anyone else from starting an election.

Because each server votes only once per term, and a winner needs a majority, two candidates cannot both win the same term: that would need two majorities with no server in common, and the overlap rule forbids it. This is how Raft keeps its promise of at most one leader per term.

Elections can fail. If S3 and S4 time out at almost exactly the same moment, they may split the votes two and two, with the remaining server's vote not enough for either, and nobody reaches three. Then both wait for another timeout, raise the term again to 4, and try again. To make repeated ties unlikely, every server picks its timeout at random within the range, and picks a fresh random value for each new election. One server almost always wakes up clearly first and wins before the others have started. This randomness is one of Raft's simplest and most important design choices.

The whole changeover, from S1 going silent to S3 sending its first heartbeat, typically takes a few hundred milliseconds, quicker than a person notices a page loading. With a leader in place, the cluster's real work can resume: how does that leader get a new command safely into everyone's log?

## Copying the log

The cluster now has a leader, S3 in term 3, chosen by a majority and announced by heartbeats. Its job is to take commands from clients and get them into every server's log in the same order.

A client sends S3 the command "set price to 45". S3 appends it to the end of its own log, say at index 7, and records the current term alongside it. Every log entry carries three things: its index, the term in which a leader first created it, and the command itself.

S3 then sends the new entry to every follower in a message called AppendEntries. This is the same kind of message as a heartbeat; a heartbeat is an AppendEntries with no entries in it. Each follower that accepts the entry writes it to its own log on disk and replies that it has done so.

Once the entry is stored on a majority of the cluster, the leader treats it as committed. Committed means the entry is permanent: Raft guarantees it will never be removed or replaced, whatever crashes follow. Here S3 has the entry itself; when S2 and S4 confirm theirs, that makes three of five, and index 7 is committed even if S5 has not replied yet.

Only a committed entry is applied. S3 feeds "set price to 45" into its state machine, so its price becomes 45, and only now does it tell the client the change succeeded. In later AppendEntries messages, including heartbeats, S3 tells the followers how far the committed part of the log reaches, and each of them then applies the same entries to its own state machine in order. S5, which was slow, catches up later and arrives at exactly the same price.

This is where the most common misunderstanding of Raft tends to sit. It is easy to assume an entry is safe once the leader has written it, or that a leader is whoever believes it is the leader. Neither is true. A leader's own copy counts for nothing until a majority of the full cluster holds the entry, and a leader that cannot reach a majority cannot commit anything at all.

Go back to term 2, when S1 was still leader, and suppose that instead of crashing it was cut off by a network fault that split the cluster in two: S1 and S2 on one side, S3, S4 and S5 on the other. S2 still hears S1's heartbeats, so nothing seems wrong on that side. S1 still thinks it is leader of term 2, and a client on its side sends it "set price to 50". S1 appends the entry and sends it to S2, but two servers are not a majority of five, so the entry never becomes committed and the client never gets a success reply. On the other side, S3, S4 and S5 stop hearing heartbeats, elect S3 in term 3 with three votes, and keep committing. For a while there are two servers that each believe they are leader, but only one of them can get anything done. When the network heals, S1 sees a message carrying term 3, adopts it, steps down, and its uncommitted "set price to 50" entry is thrown away. The lesson is that during a split, the smaller side does not keep working on its own; it stops making progress, and that is a deliberate choice that prevents the two sides from writing conflicting histories.

That leaves the question of how a follower's log is kept in line with the leader's, given that followers can miss messages, crash, or hold leftover entries like S1's. Raft handles this with a check built into every AppendEntries. Along with the new entries, the leader sends the index and term of the entry that comes right before them. The follower accepts the new entries only if its own log has an entry at that index with that same term.

The check works because of a simple fact about how logs are built. A leader creates at most one entry at a given index in a given term, and never moves entries around. So if two logs have an entry with the same index and the same term, they hold the same command there, and, since each step was checked the same way, every entry before it matches too. This guarantee is called the Log Matching Property.

When the check fails, the follower refuses, and the leader tries again starting one entry earlier, then earlier again, until it finds the last point where the two logs agree. From there the leader sends its own entries forward, and the follower deletes anything of its own that conflicts. That is exactly how S1's stray "set price to 50" disappears after the network heals: the new leader walks back to the point of agreement and overwrites what came after. Real implementations often speed up this walk backwards, but the idea is the same.

The leader's log is always the one that wins. That is safe only if the leader's log is guaranteed to contain everything that was ever committed. How can Raft be sure a newly elected leader is not missing something?

## Why committed entries survive

Every new command now follows the same path: the leader writes it, sends it with a consistency check, and commits it once a majority holds it. Followers are always brought into line with the leader, which only works if the leader never lacks a committed entry.

Imagine what could go wrong without an extra rule. Index 7, "set price to 45", was committed on S2, S3 and S4. Suppose S5, which missed it, then won an election. As leader, it would push its own log onto the others and overwrite index 7, and a change the client had been told was successful would vanish. Raft must make that election impossible.

It does this with one more condition on voting, called the election restriction. A server refuses its vote to any candidate whose log is less up to date than its own. "Up to date" is judged by the last entry in each log: the one whose last entry has the higher term is more up to date, and if the terms are equal, the longer log is.

Now apply the overlap rule again. Index 7 sits on a majority: S2, S3 and S4. To win, S5 needs a majority of votes too, and any majority must include at least one of S2, S3 or S4. Whichever one it is will see that S5's log is behind its own and refuse. So S5 cannot win, and whoever does win already holds index 7. In one sentence: committing needs a majority, winning needs a majority, the two majorities always overlap, and the server in the overlap blocks any candidate that is missing what was committed.

There is one further subtlety the paper treats carefully. A new leader does not count copies of entries left over from earlier terms to decide whether they are committed; it commits them indirectly, by committing a new entry of its own term on top of them, which drags the earlier ones along. Without this, a rare sequence of crashes could undo an entry that looked committed. You do not need the details to follow Raft's design, but it is worth knowing that the rule exists, because it is the part most often gotten wrong in homemade implementations.

Two limits are worth holding onto. First, Raft assumes servers fail by crashing or going silent, not by lying. A server that sends deliberately false messages, known as a Byzantine fault, can break it; Raft is meant for machines run by one operator who trusts them, not for strangers who might cheat. Second, Raft depends on each server writing its term, its vote and its log entries to disk before replying, so a restarted server remembers what it promised. A system that skips those disk writes for speed is no longer giving Raft's guarantees.

## The whole picture

Raft lets a small cluster of servers behave like one reliable machine by agreeing on a single ordered log of commands and having every server apply that log in order. It keeps one leader per numbered term, chosen by majority vote after a randomized timeout; the leader appends each command to its log, copies it to followers with a check that their logs match up to that point, and commits it once a majority holds it. Because any two majorities share a server, and because servers refuse to vote for a candidate whose log is behind theirs, a committed entry is always present in the next leader's log, so nothing a client was told succeeded is ever lost. The price is that the cluster can only make progress while a majority of it can talk to each other, which is exactly what keeps two halves of a split network from writing two different histories.

## Going further

Log compaction and snapshots: how servers stop the log growing forever by saving the current state and discarding the entries that produced it.

Membership changes: how servers are added to or removed from a running cluster safely, described in the paper as joint consensus, and in later work as one-server-at-a-time changes.

Linearizable reads: why reading from a leader can still return stale data, and techniques such as ReadIndex and leader leases that prevent it.

Paxos and Multi-Paxos: the older family of consensus algorithms that Raft was designed to be an easier alternative to.
