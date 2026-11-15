# Raft, From the Ground Up

By the end you will know how Raft keeps a group of servers agreeing on one shared history, even while some of them crash or lose contact, and where people usually get it wrong.

## The problem of keeping copies in agreement

Raft is an algorithm for distributed systems, meaning software that runs across several machines connected by a network. It lets a small group of servers agree on one sequence of changes, so that together they behave like a single server that does not go down when one machine does.

Here is the situation it was built for. Say your team keeps its important settings in a small key-value store: a program that holds named values and lets other programs read and change them. One of those settings is called `checkout`, and it decides whether the shop's checkout page is on or off. Dozens of services ask this store for the value of `checkout` every second.

If the store runs on one server, that server is a single point of failure. When it crashes, or its disk dies, or someone reboots it for an update, every service that depends on it is stuck. The obvious fix is to run copies of the store on several servers, so that if one disappears the others carry on.

Copies bring their own trouble. Suppose two engineers change the setting at almost the same moment: one sends "set checkout to off", the other sends "set checkout to on". The network delivers these messages to the different copies at slightly different times. One copy receives "off" then "on" and ends with `checkout` on. Another receives "on" then "off" and ends with it off. Both copies are healthy and both did exactly what they were told, yet they now disagree, and whichever copy a service happens to ask decides whether customers can pay.

The fix for that has a name. If every copy starts from the same state and applies the same commands in the same order, every copy ends in the same state. A program that behaves this way, where the result depends only on the starting point and the commands fed to it, is called a state machine. Running identical copies of one on several servers is called a replicated state machine.

That shifts the problem. You no longer need the copies to agree on the value of `checkout` directly. You need them to agree on the list of commands, in order. This ordered list is called the log. Each entry in the log is one command, and each entry has a position number called its index: entry 1, entry 2, entry 3, and so on. If every server holds the same log, every server's key-value store holds the same values.

Getting several machines to agree on one value, such as "what is entry 7 in the log", is called consensus. It sounds easy until you remember what the network and the machines are allowed to do. Messages can arrive late, arrive out of order, or not arrive at all. Servers can crash at any moment and restart later with whatever they had saved to disk. A server cannot tell the difference between another server that has crashed and one that is merely slow, because in both cases it hears nothing.

For a long time the standard answer to consensus was an algorithm called Paxos, published by Leslie Lamport. Paxos works, but it is famous for being hard to understand and harder to turn into a working system. In 2014, Diego Ongaro and John Ousterhout at Stanford published Raft with an explicit goal: to solve the same problem with an algorithm that people could actually understand, explain, and implement correctly. Today Raft sits inside widely used systems such as etcd, the store that Kubernetes keeps its cluster state in, as well as Consul, CockroachDB, and TiKV.

Raft does not protect against servers that lie or have been taken over by an attacker. It assumes every server follows the rules honestly, and that the only problems are crashes, restarts, delays, and lost messages. Tolerating dishonest servers is a different and much more expensive problem, called Byzantine fault tolerance, and Raft does not attempt it.

So the question Raft answers is this: how do five ordinary servers, any of which might vanish at any moment, end up with the same log? The answer starts with two ideas, majorities and leaders.

## Majorities, leaders and terms

You now have the shape of the goal: a group of servers, each running a copy of the key-value store, each holding a log of commands that must end up identical everywhere. Raft gets there with a few ideas that the rest of the algorithm leans on.

Throughout this piece, the group will be five servers named A, B, C, D and E. A group of servers running Raft together is called a cluster.

The first idea is that Raft never waits for everyone. Waiting for all five servers would mean one crashed server stops the whole cluster, which is the very thing you were trying to avoid. Instead, Raft treats something as decided once more than half the cluster has it. For five servers, that means three. More than half of a cluster is called a majority, and in many systems you will also hear it called a quorum.

Majorities matter because of one plain fact: any two majorities of the same cluster always share at least one server. If A, B and C agree to something, and later C, D and E agree to something else, C was in both groups. There is no way to pick two groups of three out of five that do not overlap. That shared server carries knowledge from one decision to the next, and much of Raft's safety comes from making sure it speaks up.

The same arithmetic says how many failures a cluster survives. Five servers need three to make progress, so they can lose two. Three servers need two, so they can lose one. This number is worth keeping in mind, because it comes back when things go wrong.

The second idea is that one server is in charge at a time. That server is called the leader. All changes go through it: clients send their commands to the leader, the leader decides where each command goes in the log, and it tells the other servers. The servers that take instructions from the leader are called followers.

Having one leader makes the ordering problem from earlier disappear. When the two engineers send "off" and "on" at the same moment, both commands reach the same leader, and the leader puts one of them first. Whatever order it picks becomes the order for everyone. The followers do not decide anything about ordering; they copy.

A leader can crash, of course, so the cluster needs a way to choose a new one. A server that is trying to become leader is in a third role, called candidate. Every Raft server is always in exactly one of these three roles: follower, candidate, or leader. In a healthy cluster there is one leader and every other server is a follower; candidates exist only briefly, during an election.

The third idea is a way to tell old leadership from new. Raft divides time into numbered periods called terms. Term 1, term 2, term 3, and so on. Each term begins with an election, and if the election succeeds, the winner leads for the rest of that term. A term can also end without a leader, if the election fails; the cluster then moves on to the next term and tries again.

Every server remembers the highest term number it has seen, and it attaches that number to every message it sends. This makes the term number work like a date stamp on a letter. If a server receives a message carrying a higher term than its own, it learns that it has fallen behind: it updates its own term and, if it was a leader or candidate, it immediately goes back to being a follower. If it receives a message carrying a lower term, it knows the sender is out of date and rejects the message.

Terms solve a subtle problem. A leader might be cut off from the network for a while, keep believing it is in charge, and then reappear. Without terms, the cluster could end up with two servers both giving orders. With terms, the stale leader's messages carry an old number, everyone ignores them, and the first reply it gets tells it to stand down.

One last piece of vocabulary. Raft servers talk to each other through remote procedure calls, usually shortened to RPCs. An RPC is a request one server sends to another, asking it to do something and send back an answer, much like calling a function that happens to run on a different machine. Raft's core needs only two kinds: RequestVote, which candidates send during elections, and AppendEntries, which leaders send to copy log entries to followers.

You now hold the full cast: a cluster of five, majorities of three, one leader with four followers, and numbered terms that keep old leaders from causing harm. The next question is how the cluster picks its leader in the first place, and how it notices that a leader has gone.

## Electing a leader

So far you have a cluster of five servers in which one leader makes all the decisions and the others follow, with every server tracking a term number that rises whenever leadership changes hands. What is missing is the moment of change itself: how the followers notice the leader is gone, and how one of them takes over.

Start with a working cluster. Server A is the leader for term 2. B, C, D and E are followers.

A leader has to keep proving it is alive. It does this by sending a small message to every follower several times a second, even when there is nothing new to report. That message is called a heartbeat. In Raft, a heartbeat is an AppendEntries RPC that carries no log entries; it simply says "I am still the leader of term 2."

Each follower runs a countdown timer called the election timeout. Every time a heartbeat arrives, the follower resets its timer to the start. If the timer ever reaches zero without a heartbeat, the follower concludes that the leader is gone, and it tries to become leader itself.

The election timeout is not the same length on every server. Each server picks a random value within a range every time it resets its timer. The original Raft paper suggests a range of 150 to 300 milliseconds, roughly the length of a blink or two, though real systems tune it to their networks; etcd, for instance, defaults to one second. The randomness is the important part, and you will see why in a moment.

Now A crashes. The heartbeats stop. Each follower's timer keeps running down. Suppose C's timer happens to be set to 170 milliseconds, while B, D and E drew longer values, between 220 and 290 milliseconds. C's timer runs out first.

C does four things at once. It increases its term from 2 to 3. It switches its role from follower to candidate. It votes for itself. And it sends a RequestVote RPC to every other server, saying in effect: "I am a candidate for term 3; will you vote for me?"

Each server can vote for at most one candidate in each term, on a first-come, first-served basis, and it writes its vote to disk before replying so that a crash and restart cannot let it vote twice. B, D and E have not voted in term 3 yet. When C's request arrives, they see the higher term, update their own term to 3, and grant their vote. There is one more check they make before voting, which matters a great deal for safety and gets its own chapter later; for now, assume C passes it.

C needs a majority, three of five. It has its own vote, and B's arrives, and D's. That is three. C is now the leader for term 3. It immediately starts sending heartbeats to everyone, which tells the remaining servers that the election is over and resets their timers. The whole process, from A's crash to C's first heartbeat, has taken a few hundred milliseconds.

Notice that C won without hearing from A, which is down, and did not need E's vote either. That is the majority rule doing its job: the cluster moved on while two of its five servers were absent or slow.

Now the reason for the randomness. Suppose instead that every server used the same timeout. When A crashed, all four followers would time out at the same instant, all would become candidates for term 3, and each would vote for itself. With every server holding one vote for itself, nobody reaches three. This situation is called a split vote, and the term ends with no leader.

When a split vote happens, the candidates' timers run out again, they move to term 4, and they try once more. If the timers were identical, this could repeat forever. Random timeouts make it very likely that one server times out noticeably before the rest, gathers its votes before anyone else even starts, and wins cleanly. Split votes still happen occasionally, but they resolve within an extra round or two.

Raft does not promise that an election will finish within a fixed time. On a badly behaved network, elections could in principle keep failing. In practice, with timeouts that are long compared to the time it takes a message to cross the network, the cluster settles on a leader quickly. This is a general truth about consensus: no algorithm can guarantee progress on a network with unbounded delays, so practical algorithms like Raft guarantee that they never give a wrong answer, and rely on timing only to make progress.

One more rule completes the election picture. If a candidate, while waiting for votes, receives a heartbeat from another server claiming to be leader with a term at least as high as its own, it accepts that leader and becomes a follower again. Someone else won; there is no point continuing.

You now know how the cluster ends up with exactly one leader per term, and how it replaces one that disappears. A leader that only sends heartbeats is not much use, though. The point of having one is to accept commands and get them into everyone's log, and that is the next step.

## Copying the log

At this point the cluster has a leader, C, elected for term 3, sending heartbeats to the four other servers, with A still down. Every server has a log of commands, and the goal is for every log to end up the same. Here is how a new command gets in.

Before C was elected, the cluster had already processed six commands under earlier leaders, stored in log entries 1 through 6. Entry 6 was the last one A added during term 2, and it reached B, C and D before A crashed. E, which had been slow, holds only entries 1 through 5.

Each log entry carries three things: its index, the command itself, and the term in which a leader first created it. So entry 6 says, in effect: "index 6, term 2, set `max_retries` to 5." That term number stays with the entry forever, and it turns out to be the key to how Raft keeps logs consistent.

A client now sends C the command "set `checkout` to off". If a client sends a command to a follower instead, the follower knows who the current leader is from its heartbeats, and typically either redirects the client or passes the request along, depending on the implementation.

C appends the command to its own log as entry 7, term 3. Then it sends an AppendEntries RPC to each follower, carrying the new entry and asking them to add it to their logs.

A follower that receives the entry writes it to its log on disk and replies that it has stored it. Writing to disk first matters: a server that said "stored" and then lost the entry in a crash would be breaking a promise the leader is counting on.

B and D reply quickly. C now knows that entry 7 is stored on three servers: itself, B and D. That is a majority of five. Once a leader knows that an entry from its current term is stored on a majority, the entry is committed. Committed means the entry is permanent: Raft guarantees that it will never be removed or replaced, and that every future leader will have it.

This is the moment that matters to the client. Only once entry 7 is committed does C apply the command to its own key-value store, setting `checkout` to off, and reply to the client that the change succeeded. A write in Raft costs one round of messages from the leader to a majority plus a disk write on each of them. Inside one data centre that typically adds up to a few milliseconds. When the servers sit in different regions, each write pays at least one cross-region round trip, tens of milliseconds or more.

The followers also need to apply the command to their own copies of the store, but they can only do so once they know it is committed, and only C knows that so far. C tells them in later messages. Every AppendEntries RPC, heartbeats included, carries a number called the commit index: the highest log index the leader knows is committed. When B sees the commit index reach 7, it applies entry 7 to its own store. Every server applies committed entries strictly in index order, which is exactly what makes every copy of the state machine end up the same.

Here is where people most often go wrong with Raft, so it is worth saying plainly. An entry being in a server's log is not the same as the entry being committed. A leader can write an entry to its log and then crash before a majority receives it. That entry may later be thrown away. The only promise Raft makes is about committed entries, and the only safe moment to tell a client "done" is after commit. You will see an entry thrown away in the next chapter, and why that is acceptable.

Now consider E, the slow server. C sends it the same AppendEntries RPC with entry 7. But E is missing entry 6, and if it blindly appended entry 7, its log would have a gap. Raft has a check to catch exactly this.

Every AppendEntries RPC carries, alongside the new entries, the index and term of the entry that comes immediately before them in the leader's log. For entry 7, that is "index 6, term 2". The follower accepts the new entries only if its own log has an entry at that index with that same term. This is called the consistency check.

E looks at its log, finds nothing at index 6, and rejects the request. C does not give up. It keeps track, for each follower, of the next index it should try to send, and when a follower rejects, C steps that index back by one and tries again. Its next message to E carries entries 6 and 7, along with the details of the entry before them: index 5, term 2. E does have entry 5 from term 2, so the check passes, and E appends 6 and 7. E is now caught up. Real implementations often step back faster than one entry at a time, for instance by having the follower report where its log diverges, but the idea is the same.

The consistency check is small, but it gives Raft a powerful guarantee. Each time a follower accepts entries, it has confirmed that its log matches the leader's at the position just before them. That position was itself accepted only after matching the position before it, and so on back to the start. So whenever two logs have an entry with the same index and the same term, the logs are identical in every entry up to that point. This is called the log matching property, and it means a leader never needs to compare whole logs; checking one entry is enough.

The check also handles followers that have the wrong entries, not only missing ones. If a follower holds an entry at some index whose term differs from the leader's, the follower deletes that entry and everything after it, and takes the leader's entries instead. The leader's log always wins. The leader itself never deletes or overwrites anything in its own log; it only appends.

That rule sounds dangerous. If the leader's log always wins, what stops a leader with a bad or incomplete log from overwriting committed entries on everyone else? The answer is a rule in the election that you skipped over earlier, and it is the heart of why Raft is safe.

## Why committed entries are never lost

Here is what you now hold. A leader, chosen by a majority vote in a numbered term, appends each client command to its log and copies it to followers. An entry is committed once a majority has stored it, and only then is it applied and confirmed to the client. When a follower's log disagrees with the leader's, the follower's version is replaced. The open question is why that replacement can never erase a committed entry.

The danger is easy to picture. Suppose E had been slow for a long time and held only entries 1 through 5, while entries 6 and 7 were committed on B, C and D. If E could win an election and become leader, it would force its shorter log onto everyone, and entry 7, the "checkout off" command that a client was told had succeeded, would be gone.

Raft prevents this at election time. When a server receives a RequestVote RPC, it refuses to vote for a candidate whose log is less up to date than its own. This is the check mentioned in the election chapter, and it is called the election restriction.

"Up to date" has a precise meaning. The candidate's RequestVote includes the index and term of its last log entry. The voter compares that with its own last entry. If the last terms differ, the log whose last entry has the higher term is more up to date. If the last terms are the same, the longer log is more up to date. The voter grants its vote only if the candidate's log is at least as up to date as its own.

Run this against E before it caught up. Say C has crashed, and E's timer runs out first. E becomes a candidate for term 4 and asks for votes. Its last entry is index 5, term 2. B and D both have a last entry of index 7, term 3. Their last term is higher, so their logs are more up to date, and they refuse. E can get its own vote and perhaps A's, if A is back, but A refuses too: A's log ends at a higher index than E's, as you will see shortly. E cannot reach three votes. It loses, and a server with entry 7 wins instead.

Here is why this always works, not only in this example. A committed entry is stored on a majority. A winning candidate needs votes from a majority. Two majorities always share at least one server. So at least one voter for any winning candidate has the committed entry. That voter would have refused to vote for a candidate whose log was less up to date than its own, and a log that is at least as up to date as one holding the committed entry also holds it. So every new leader already has every committed entry. And since a leader only appends to its own log and never deletes from it, those entries spread outward from the leader and are never removed.

This is the overlap of majorities from the second chapter, now doing the real work. A server that took part in committing an entry is guaranteed to sit in the group that elects the next leader, and the election restriction makes it veto any candidate who would lose that entry.

Now the promised case of an entry being thrown away, which shows the other side of the same rule. Rewind to just before A crashed in term 2. A had received a client command, "set `checkout` to on", and appended it to its own log as entry 7, term 2. Then A crashed before sending it to anyone. That client never got a reply.

Meanwhile C won term 3 and wrote a different command, "set `checkout` to off", as its own entry 7, term 3, and committed it. Later, A restarts. It still believes it is leader of term 2, and it sends heartbeats. The other servers see term 2, which is older than their term 3, and reject them, telling A the current term. A updates its term to 3 and becomes a follower.

When C next sends A an AppendEntries RPC, the consistency check finds that A's entry 7 carries term 2 while C's entry 7 carries term 3. A deletes its entry 7 and takes C's. The command "set `checkout` to on" vanishes from the cluster.

That is acceptable, because nobody was ever told it succeeded. It was never committed, and its client got no reply. From the client's side, the request timed out, and the usual answer is to retry. This is the practical meaning of the distinction from the previous chapter: Raft keeps every promise it made, and it makes a promise only at commit.

There is one more subtle rule, which you will see in the Raft paper and in any careful implementation. A new leader counts replicas to decide commitment only for entries from its own current term. It never declares an older-term entry committed just because it notices that entry is now on a majority. Older entries become committed indirectly, the moment the leader commits an entry from its own term that sits after them in the log, because the log matching property means anyone holding the newer entry also holds everything before it. The reason for this rule involves a specific sequence of crashes in which an old-term entry on a majority could still be overwritten; the details are intricate and not needed to use Raft, but the rule exists to close that gap. Many implementations also have a new leader immediately append an empty entry from its own term, so that earlier entries get committed promptly.

Raft's safety also depends on what each server keeps on disk. Three things must survive a crash: the server's current term, which candidate it voted for in that term, and its log. Each must be written to disk before the server replies to any message that depends on it. A server that forgot its vote after a restart could vote twice in one term and help elect two leaders. A server that forgot log entries it had acknowledged could undo a commit. This is one reason Raft clusters care so much about disk speed: every vote and every write waits on a disk flush.

With the election restriction, the current-term commit rule and durable storage, Raft guarantees that once an entry is committed, every server that ever applies an entry at that index applies the same one. That is the whole point of the algorithm. What remains is to watch it under the conditions where it is tested hardest: broken networks and lost servers.

## When the network breaks

You have now seen Raft's full machinery. Leaders are elected by majority vote in numbered terms, entries are committed once a majority stores them, the election restriction guarantees every new leader has every committed entry, and stale leaders are defeated by their outdated term numbers. This chapter puts that machinery under stress.

The hardest case is not a crash, because a crashed server stays quiet. The hardest case is a network partition: the network splits so that some servers can talk among themselves but not to the others, while every server keeps running.

Take the five servers with C as leader in term 3. A network fault cuts C and B off from A, D and E. C and B can still reach each other. A, D and E can still reach each other. Neither group can reach the other.

On C's side, C still believes it is leader. Clients that can reach C keep sending it commands. Say one sends "set `checkout` to on". C appends it as entry 8 and sends it to everyone. Only B receives it. C now has the entry on two servers out of five, which is not a majority. The entry is never committed, C never applies it, and the client never gets a success reply. The minority side keeps running but makes no progress.

On the other side, A, D and E stop hearing heartbeats. One of them, say D, times out, starts an election for term 4, and receives votes from A and E. Their logs all hold the committed entry 7, so the election restriction is satisfied. D now leads term 4 with three of five servers, a majority, and it can commit new commands. A client on this side sends "set `checkout` to off", and it commits as D's entry 8, term 4.

For a while, two servers believe they are leader: C in term 3 and D in term 4. This sounds like the disaster consensus is meant to prevent, the situation called split brain, where two halves of a system both accept writes and drift apart. Raft avoids the harm, because only one of them can commit anything. C cannot reach a majority, so its writes go nowhere. Two majorities cannot exist side by side, so at most one leader is ever able to commit.

When the network heals, C sends a message and gets a reply carrying term 4. It steps down at once and becomes a follower. D's AppendEntries then finds that C's and B's entry 8 carries term 3 while D's carries term 4, so they delete theirs and take D's. The uncommitted "on" command disappears, exactly like A's lost entry in the last chapter, and for the same reason it was safe to lose: no one was told it succeeded.

Now the most common misunderstanding about Raft clusters, which this scenario brings into view. People often assume that Raft keeps going as long as some servers are healthy, or that it needs a majority of the servers that are currently up. It needs a majority of the whole cluster, counted against the full membership. If three of the five servers fail, the two survivors are perfectly healthy, can talk to each other, and still refuse to accept any write. They have no way of knowing whether the other three are dead or are on the far side of a partition, busy electing their own leader, and accepting writes anyway would risk exactly the split brain described above. Losing a majority makes a Raft cluster stop, by design.

The same counting explains why Raft clusters almost always have an odd number of servers. A four-server cluster needs three for a majority, so it can lose only one server, the same as a three-server cluster. The fourth server adds cost and one more participant in every write, without adding any tolerance. Three servers tolerate one failure, five tolerate two, and seven tolerate three. Most deployments use three or five, because every additional server means more messages for each write.

Partitions raise one more practical issue, about reading data rather than writing it. A client that asks C for the value of `checkout` during the partition might get an old answer, because C does not know that D has since committed a change. Serving a read from a leader's local copy can return stale data, since the server might no longer be the leader without knowing it.

Implementations handle this in a few ways. The most direct is to send the read through the log like a write, which is correct but slow. A cheaper method, often called ReadIndex, has the leader note its current commit index, confirm with a round of heartbeats that a majority still accepts it as leader, wait until its store has applied entries up to that commit index, and then answer. A third method, leader leases, skips the heartbeat round by assuming that clocks on different servers run at roughly the same rate; it is faster but trades some safety for speed if that assumption breaks. Which one a system uses, and whether it offers a weaker "may be stale" read as an option, varies by product, so this is worth checking in the documentation of any Raft-based system you rely on.

A last practical point concerns a server that keeps losing contact, for instance one with a flaky network link. Each time it times out, it raises its term and starts an election. When it reconnects, its higher term forces the healthy leader to step down, disrupting a cluster that was working fine. Many implementations add a step called pre-vote, in which a server first asks whether it could win an election before raising its term. This extension was described in Ongaro's later work and is widely adopted, but it is not part of the basic algorithm.

You have now watched Raft survive a crashed leader, a lagging follower, a returning stale leader, and a split network, and in each case the committed history stayed intact while uncommitted work was quietly dropped.

## The whole picture

Raft lets a group of servers act as one reliable machine by agreeing on a single ordered log of commands, which each server applies to its own copy of the same state machine. A leader orders the commands, so there is never a question of whose order wins. Terms stamp every message, so a leader that has been replaced cannot keep giving orders. An entry counts as committed only when a majority has stored it, and only committed entries are applied and confirmed to clients. Because any two majorities share a server, and because voters refuse candidates whose logs are behind their own, every new leader already holds everything that was committed before it. The result is a cluster that keeps working while a minority of its servers are down or cut off, stops rather than risk disagreement when a majority is lost, and never takes back a promise it has made.

## Going further

Log compaction and snapshots: a log cannot grow forever, so servers periodically save a snapshot of the state machine and discard the entries it covers, and leaders send snapshots to followers that have fallen too far behind, using an RPC called InstallSnapshot.

Membership changes: adding or removing servers safely needs care so that old and new majorities cannot decide different things; Raft describes a method called joint consensus, and most implementations use a simpler one-server-at-a-time approach.

Multi-Raft: systems such as CockroachDB and TiKV split their data into many ranges and run a separate Raft group for each, so that one cluster of machines can spread its load across many leaders.

Paxos: the older consensus algorithm Raft was designed to replace in teaching and practice; reading about it after Raft makes the shared ideas, majorities and numbered rounds, easy to recognise.
