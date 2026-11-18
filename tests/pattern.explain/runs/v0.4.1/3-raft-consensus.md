# How Raft Keeps Servers in Agreement

By the end you will understand how Raft lets a small group of servers act as one reliable machine, how it survives crashes and broken networks, and where its guarantees stop.

## Why one copy is not enough

Picture a company that keeps its feature switches in a small database: which features are turned on for customers, and with what settings. Every one of the company's app servers asks this database, many times a second, whether the new checkout page is switched on. Those app servers are its clients. If the single machine holding the database dies, every client is left without an answer at once.

The natural fix is to keep several copies on separate machines, so that losing one costs nothing. Copies bring their own trouble, though. Suppose one person turns the new checkout on and another turns it off a moment later. If one copy receives those two changes in one order and another copy receives them in the other order, the copies now disagree, and the answer a client gets depends on which copy it happened to ask.

The network makes this harder. Messages between machines arrive late, arrive out of order, or never arrive. A server that has gone quiet might have crashed, or might be slow, or might be fine but cut off, and from the outside there is no reliable way to tell which.

Getting a group of machines to agree on one answer despite all of this is called consensus. Raft is a recipe for consensus, published in 2014 by two researchers at Stanford University. Its stated aim was to be easy to understand, because the older recipes for the same job had a reputation for being correct but very hard to follow and to build.

Throughout this piece the feature-switch database runs on five servers, called A, B, C, D and E. Five is a common size for a Raft group, which is usually called a cluster.

Raft does not make the five servers agree on the settings directly. It makes them agree on a list of changes, kept in order: first "turn checkout on", then "set the discount to 10 percent", then "turn checkout off". This ordered list is called the log, and each change in it is a log entry. Entries are only ever added to the end.

Each server feeds the entries of its log, one by one in order, into the part of the program that actually holds the settings. That part is called the state machine. If all five servers start from the same empty settings and apply the same entries in the same order, all five state machines end up holding exactly the same settings. So Raft's whole job is to keep the logs identical; the settings follow from that.

The second idea is that no decision needs every server. A decision counts once a majority of the cluster has accepted it: with five servers, any three. Any two groups of three drawn from the same five servers must share at least one server. That shared server is what carries knowledge of one decision into the next, and much of Raft's safety rests on it. In Raft's documentation and in most software built on it, such a majority is called a quorum.

The arithmetic of quorums decides how many failures a cluster survives. With five servers, a quorum of three can still be formed while two servers are down, so the cluster survives two failures. A three-server cluster survives one.

The third idea is that servers do not take turns proposing changes. At any moment one server is in charge: it alone accepts new changes from clients, decides their order, and sends them to the others. That server is the leader. Because one machine chooses the order of every change, the problem of two copies receiving changes in different orders disappears.

If everything goes through the leader, the next question is who picks the leader, and what happens when it dies.

## Choosing a leader

You now have five servers, A to E, each holding its own copy of an ordered log, with one leader deciding the order of every change and every decision counted by a quorum of three. Here is how the cluster gets its leader in the first place, and gets a new one when the old one disappears.

Each server is always in one of three roles. Most of the time, every server except the leader is a follower. A follower never starts anything on its own: it answers the leader's messages and otherwise waits.

The leader proves it is still alive by sending every follower a short message at a steady rhythm, even when no changes are happening. This message is called a heartbeat. Implementations commonly send one every few tens of milliseconds, many times faster than a blink.

Every follower runs a timer that restarts each time it hears from the leader. If the timer runs out with no word from the leader, the follower concludes the leader is gone. This waiting period is called the election timeout.

Raft divides time into numbered periods called terms. Term 1, term 2, term 3 and so on each begin with an election, and each term has at most one leader. Every message a server sends carries its current term number. When a server sees a message with a higher term than its own, it adopts that higher number at once, and if it was leading, it stops and becomes a follower. When it sees a lower term, it knows the sender is out of date and rejects the message. The term number is how servers recognise stale news without any shared clock.

When a follower's election timeout runs out, it moves to the third role. It adds one to its term, votes for itself, and asks every other server for its vote. A server in this role is a candidate, and the message asking for a vote is called RequestVote.

Take the cluster in term 3, with A as leader. A crashes. The followers stop receiving heartbeats, and B's timer happens to run out first. B moves to term 4, votes for itself, and sends RequestVote to A, C, D and E. A is down and says nothing. C, D and E have not voted in term 4 yet, and each server gives at most one vote per term, to the first candidate that asks. C and D reply yes before anything else happens. B now holds three votes, its own plus two, which is a quorum. B becomes the leader for term 4 and immediately sends heartbeats, which restart everyone's timers and stop any other election from starting.

Now suppose instead that C's and D's timers had run out at the same instant. Both become candidates for term 4, each votes for itself, and B and E split their votes between them. With A down, each candidate ends with two votes, short of three. Nobody wins, and term 4 ends with no leader. This is a split vote. The candidates wait for their timers to run out again and start term 5.

Split votes could repeat forever if every server waited the same length of time. To prevent that, each server picks its election timeout at random, afresh each time, from a range; the original paper suggests 150 to 300 milliseconds. Usually one server wakes first by a clear margin, collects its votes and sends heartbeats before anyone else's timer runs out, so an election normally settles within a fraction of a second.

With B elected, the question becomes what a leader actually does when a change arrives.

## Copying the log

B now leads term 4, holding its place by sending heartbeats, and any follower that stops hearing them will start a new election. A client now asks to turn the new checkout on.

The request goes to B. If a client contacts a follower by mistake, the follower tells it which server is the leader. B adds the change to the end of its own log. Every entry has a position number counting up from 1, called its index. B's log already holds seven entries, so the new one sits at index 8. The entry also records the term in which it was created, term 4.

B then sends the new entry to every follower in a message called AppendEntries. The heartbeats from the previous chapter are AppendEntries messages with no entries inside. Each follower writes the entry into its log, on disk so it survives a restart, and replies that it has it.

As soon as a quorum holds the entry, which here means B itself plus two followers, say C and D, B marks it committed. Committed is Raft's central promise: a committed entry will never be removed or replaced on any server, through any number of crashes and future elections. Only now does B apply the entry to its state machine, so checkout is switched on, and only now does it tell the client the change is done.

This is where people most often go wrong about Raft. An entry that the leader has written to its own log is not yet safe. Until a quorum holds it, it can still vanish if the leader crashes, and the client has not been told it succeeded. "The leader has it" and "it is committed" are different states, and only the second carries the promise.

The followers also need to know the entry is committed before they apply it. B tells them by including, in every later AppendEntries message, the highest index it has committed so far. This number is called the commit index. When C sees a commit index of 8, it applies entries up to 8 to its own state machine.

Notice that E played no part. A slow or crashed follower does not hold anything up, because B only waits for the fastest two. Inside one data centre that round trip, plus a disk write, typically takes a few milliseconds at most.

Logs do not always line up this neatly. Suppose E had been switched off for a while and its log ends at index 5. When B sends entry 8, the follower must not place it after index 5 and leave a gap. To catch this, every AppendEntries message carries the index and term of the entry just before the new ones. A follower accepts the message only if its own log has an entry at that index with that same term. This is called the consistency check.

B's message to E says "the entry before this one is index 7, from term 3". E has nothing at index 7, so it refuses. B steps back one position and tries again: "the entry before is index 6". E still refuses. At index 5 the index and term match, so E accepts, and B sends entries 6, 7 and 8 in turn. E's log now matches B's.

The same check handles a follower holding wrong entries rather than missing ones. Those are entries some earlier leader wrote but crashed before committing. When the check reveals that a follower's entry at some position has a different term from the leader's entry there, the follower deletes that entry and everything after it, and takes the leader's entries instead. Changes flow in one direction only, from leader to followers. A leader never deletes or rewrites anything in its own log.

The check works because of a property the Raft paper calls Log Matching. A leader creates at most one entry at a given index in a given term, and every follower accepts an entry only after confirming the one before it matches. Together these mean that if two logs hold an entry with the same index and the same term, the two logs are identical all the way up to that point. Checking one entry vouches for everything before it.

Overwriting a follower's entries sounds dangerous, though: what stops a newly elected leader from overwriting an entry that was already committed?

## Surviving crashes and broken networks

You now hold the full path of a change: the leader adds it to its log, copies it out, counts it committed once a quorum has it, and forces every follower's log to match its own. That makes the leader's log the authority, so everything depends on every new leader already holding every committed entry.

Here is the danger. Entry 8 is committed: B, C and D hold it. Then B crashes. A, which crashed back in term 3, is still down. E, whose log ends at index 5, happens to time out first and asks for votes. If C and D voted for it, E would become leader and, through the consistency check, overwrite entries 6 to 8 on everyone else, destroying a change the client was told had succeeded.

So a vote carries one more condition. A server refuses its vote to a candidate whose log is less up to date than its own. Up to date is judged by the last entry in each log: the log whose last entry has the higher term is more up to date, and if the terms are equal, the longer log is. RequestVote messages carry the index and term of the candidate's last entry so that voters can make this comparison.

E's last entry is index 5 from term 2. C's last entry is index 8 from term 4. C refuses, and so does D. E cannot reach three votes, so it cannot win. Soon C or D times out, asks for votes, and wins with the other's vote and E's, because their logs are at least as up to date as E's.

The reason this always works comes back to overlapping quorums. A committed entry sits on a quorum of servers. A winning candidate needs votes from a quorum. Those two groups share at least one server, and that server only votes for a candidate whose log is at least as up to date as its own, which means the candidate already holds the committed entry. The Raft paper calls the result Leader Completeness: every leader's log contains every entry committed in earlier terms.

Now a different failure: no server crashes, but the network splits. A has recovered and rejoined. A cable fault cuts the cluster in two, with B, still leader in term 4, and E on one side, and A, C and D on the other. A split like this is called a network partition.

B does not know anything is wrong. It keeps accepting requests from clients that can reach it and sending AppendEntries, but only E answers. Two servers out of five is not a quorum, so nothing B receives can be committed. Those clients' writes hang and eventually fail with a timeout.

On the other side, A, C and D stop hearing heartbeats. C times out, moves to term 5, and wins with votes from A and D: three of five. C is a legitimate leader and commits new changes normally, because its side holds a quorum.

When the cable is fixed, B receives a message stamped term 5. It sees that its own term, 4, is stale and steps down to follower. Any uncommitted entries it collected during the split are overwritten by C's log through the consistency check. No committed entry was lost, and no client was ever told that two conflicting changes had both succeeded.

A reader meeting this often asks: why not let B's side count a majority of the servers it can still reach? The answer is that both sides would then reach a "majority" of their own, both would commit, and the two halves would accept contradictory changes. That failure is called split brain, and avoiding it is the reason quorums are always counted against the full membership of the cluster, five servers here, never against whoever is currently reachable.

The flip side is a deliberate trade. If three of the five servers go down, the remaining two cannot form a quorum, and the cluster stops accepting changes altogether, even though two healthy machines are still running. Raft chooses to stop rather than risk being wrong. For the same reason, a sixth server adds no protection: a quorum of six is four, so it still survives only two failures, which is why clusters are usually built with an odd number of servers.

One more limit belongs with these. Raft assumes servers fail by stopping, freezing or losing messages, not by lying. A server that is buggy or malicious and sends false votes or forged entries can break its guarantees, and guarding against that needs a different family of algorithms.

## The whole picture

Raft keeps a cluster of servers acting as one machine by making them agree on a single ordered log of changes, which each server applies to its own state machine. One leader orders every change, and terms with randomised election timeouts make sure a dead leader is replaced quickly and that two leaders in the same term are impossible. A change is committed once a quorum holds it, and the consistency check and Log Matching let the leader bring every follower's log into line with its own. Because any two quorums overlap, the voting rule guarantees that every new leader already holds every committed entry, so overwriting followers never destroys a committed change. And because quorums are counted against the whole cluster, a minority cut off by a partition can never commit anything, which is why Raft would rather stop than let two halves disagree.

## Going further

Snapshots and log compaction: how servers discard old log entries by saving a copy of the state machine, so the log does not grow forever.

Membership changes: how a running cluster safely adds or removes servers without two different majorities existing at once, through a scheme the paper calls joint consensus or by changing one server at a time.

Linearizable reads: why a cut-off leader like B can serve stale data on reads, and the techniques implementations use against it, such as ReadIndex and leader leases.

Paxos: the older and more general consensus algorithm that Raft was designed to be an easier-to-understand alternative to.
