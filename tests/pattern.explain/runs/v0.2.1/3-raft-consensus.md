# Raft: How a Group of Servers Agrees on One Story

By the end, you will understand how Raft lets a handful of servers act as one dependable machine, how it elects a leader and copies data safely, and where people commonly misread its guarantees.

## The problem of keeping copies in step

Raft is a consensus algorithm: a set of rules that lets a small group of servers agree on the same data, in the same order, even when some of them crash or their messages go missing. It was published in 2014 by Diego Ongaro and John Ousterhout at Stanford, with the explicit aim of being easier to understand than the older algorithm it competes with, called Paxos. Today it sits underneath widely used systems such as etcd, the database that stores the state of every Kubernetes cluster, and Consul, a tool for keeping track of services and their settings.

Start with the problem. Suppose a company keeps its important settings in a small database: which servers are healthy, which feature switches are on, how many connections each service may open. Every other system asks this database before acting. If it lives on one machine and that machine dies, everything that depends on it stalls. So the obvious move is to keep copies on several machines.

Copies bring a new problem. Say there are five copies, on servers we will call A, B, C, D and E. Two clients send changes at almost the same moment. One says "set max_connections to 200", the other says "set max_connections to 300". Server A receives the first change before the second; server D, a little further away on the network, receives them in the opposite order. Now A ends up at 300 and D ends up at 200. Both servers did exactly what they were told, and they disagree. Add a server that was rebooting during one of those messages and missed it entirely, and you have three different answers to one question.

The fix Raft builds on is an old and solid idea. Instead of copying the data itself, copy the list of changes, in order, and have every server apply that list from the top. If every server starts from the same empty database and applies "set max_connections to 200" and then "set max_connections to 300", every server ends at 300. Same starting point, same changes, same order: same result.

That ordered list of changes is called the log. Each change in it is a log entry, and each entry has a position, counted from 1, called its index. The database that the log is applied to is called the state machine, a general name for any program whose result depends only on the commands it is fed. A group of servers that each keep a copy of the log and feed it to their own copy of the state machine is a replicated state machine. Raft's whole job is to keep the logs identical. Once the logs agree, the databases agree on their own.

Keeping logs identical is harder than it sounds, because servers fail in untidy ways. A server can crash and come back an hour later. A network cable can be pulled so that two servers can talk to each other but not to the other three; that kind of split is called a network partition. Messages can arrive late, twice, or never. Raft assumes all of this can happen. What it does not assume is lying: it trusts that a server which answers is running the real Raft code honestly. Defending against servers that have been hacked or are deliberately misbehaving is a different and much more expensive problem, and Raft does not attempt it.

The tool Raft uses against untidy failure is counting to a majority. With five servers, a majority is three. With three servers, it is two. The rule throughout Raft is that a decision counts only once a majority of servers has accepted it.

Majorities work because any two of them overlap. In a five-server cluster, if one decision was accepted by A, B and C, and a later decision is accepted by C, D and E, at least one server, here C, took part in both. There is no way to pick two separate groups of three out of five that share nobody. That shared server is a witness: it remembers the earlier decision and can stop the later one from contradicting it. Almost every safety rule in Raft is, underneath, a way of making sure that witness speaks up.

Majorities also set the price of fault tolerance. A five-server cluster keeps working with any two servers down, because the remaining three are still a majority. A three-server cluster survives one failure. A four-server cluster also survives only one, because its majority is three, so it costs an extra machine for no extra safety. This is why Raft clusters almost always have an odd number of servers, usually three or five.

Knowing that decisions need a majority still leaves the question of who proposes them in the first place.

## Leaders and terms

So far we have a log that every server must hold identically, and a rule that nothing counts until a majority accepts it. Raft's next choice is to give one server the job of deciding what goes into the log.

That server is the leader. Every change from a client goes to the leader. The leader adds it to its own log, sends it to the others, and decides when it is safe. The other servers are followers: they accept entries from the leader and otherwise stay quiet. Because only one server is choosing the order, the problem from the opening, where A and D saw changes in different orders, cannot arise. The leader's order is the order.

A leader can crash, so Raft needs a way to notice and pick a new one. It divides time into numbered periods called terms. Term 1, term 2, term 3, and so on, each beginning with an election. Every server remembers the highest term number it has seen. Terms are not measured in seconds; a term lasts as long as its leader keeps working, which could be milliseconds or months.

Term numbers act as a clock that every server can compare. Every message in Raft carries the sender's current term. If a server receives a message with a higher term than its own, it learns that it has fallen behind: it updates its term number and, if it thought it was a leader or was running in an election, it immediately goes back to being a follower. If it receives a message with a lower term, it knows the sender is out of date and rejects the message. This one comparison quietly settles a great many confusing situations.

The leader tells everyone it is alive by sending small messages at a steady rate, often every 50 milliseconds or so, about the time it takes to blink. These are called heartbeats. As long as a follower keeps hearing them, it stays a follower.

Each follower also runs a countdown called the election timeout. Every heartbeat resets it. If the countdown reaches zero without a heartbeat arriving, the follower concludes the leader is gone. A typical election timeout is somewhere between 150 and 300 milliseconds, so a few missed heartbeats in a row are enough.

Here is what happens in our cluster when the leader dies. Say A has been leader in term 1, and A's power supply fails. B, C, D and E stop receiving heartbeats. Each of them is counting down, and whoever reaches zero first acts. Say it is C.

C becomes a candidate: a server that is asking to be leader. It does three things at once. It increases its term number from 1 to 2. It votes for itself. And it sends a message to every other server asking for their vote. That message is called RequestVote, and it carries C's new term number, 2.

Each server has one vote per term, given to the first candidate that asks and qualifies, and never changed. B, D and E receive C's request, see term 2, update their own term to 2, and each grants its vote to C. C now has four votes including its own, more than the three it needs. C is the leader of term 2, and it starts sending heartbeats at once. Those heartbeats carry term 2, so every server that receives them recognises C as the current leader and resets its countdown.

Before a server replies to a vote request, it writes its current term and the name of the server it voted for to disk, not only to memory. Memory is lost in a crash; disk survives. Without this, a server could vote for C, crash, restart having forgotten, and vote for someone else in the same term. Two candidates could each collect a majority and both become leader of term 2. Writing the vote down first rules that out.

Elections can fail. If B and D both time out at nearly the same moment, both become candidates for term 2, both vote for themselves, and the remaining votes may split so that neither reaches three. This is a split vote. Nobody wins term 2. Each candidate waits for its election timeout again, then starts a fresh election for term 3.

Raft makes split votes rare with one small trick: each server picks its election timeout at random from the range, a fresh random value each time. One server might pick 170 milliseconds and another 260. The one with the shorter countdown usually starts its election, collects its votes and sends its first heartbeat before anyone else's countdown runs out. Randomness breaks the tie that identical timers would create.

This brings us to the most common misreading of Raft. People often say that Raft guarantees there is only ever one leader. It does not. It guarantees at most one leader per term, which is a weaker and more precise promise.

Picture a partition. A is leader of term 1 and the network splits so that A and B can talk only to each other, while C, D and E can talk only to each other. C, D and E stop hearing heartbeats, hold an election, and choose C as leader of term 2. Meanwhile A has no idea anything happened. From where it sits, it is still the leader of term 1, and it will happily accept requests from any client that can reach it.

So, for a while, two servers believe they are leader. What keeps this safe is the majority rule. A can reach only B, two servers out of five, so nothing A tries to decide can ever reach three, and none of it will count. C can reach three, so C's decisions do count. When the network heals, A receives a message carrying term 2, sees that its own term 1 is lower, and steps down. Raft never promises that a stale leader does not exist; it promises that a stale leader cannot get anything accepted.

With a leader in place, the question becomes how it actually puts entries into everyone's log, and how it knows when an entry is safe.

## Copying the log and committing entries

We now have a leader, C, chosen for term 2 by a majority, and followers that obey any leader with a current term. The leader's main work is copying log entries to the followers and deciding when they are final.

Each log entry stores two things besides the change itself: its index, its position in the log, and the term in which a leader first created it. So an entry might be "index 7, term 2: set max_connections to 300". The index and term together act like a fingerprint for an entry, and Raft relies on that fingerprint heavily.

A client sends C the change "set max_connections to 300". C appends it to its own log at the next free position, say index 7, labelled term 2. Then C sends it to every follower in a message called AppendEntries. The same message type doubles as the heartbeat; a heartbeat is an AppendEntries with no new entries in it.

Each AppendEntries message carries the new entries along with one piece of context: the index and term of the entry that comes immediately before them in the leader's log. For our change at index 7, C includes "the entry before this is at index 6, term 1". A follower accepts the new entries only if its own log also has an entry at index 6 with term 1. If it does not, it refuses. This is the consistency check.

The consistency check is how Raft keeps logs identical without comparing them in full. Raft maintains a simple property: if two logs have an entry with the same index and term, then those entries hold the same change, and every entry before them is identical too. A leader creates at most one entry at each index in its term, which settles the first half. The consistency check settles the second, because a follower accepts an entry only when the one before it already matches, and that one was accepted only when the one before it matched, all the way back to the start. One matching fingerprint stands for the entire history behind it.

When a follower refuses, the leader steps back. It retries with an earlier starting point, "here are entries from index 6 onward, and the one before is index 5, term 1", and keeps going back one position at a time until it finds the place where the follower's log and its own agree. From there it sends everything forward. If the follower had any entries after that point that differ from the leader's, the follower deletes them and takes the leader's instead.

That deletion sounds alarming, and it is where people often worry that Raft loses data. It does not lose anything that mattered, because of a distinction that runs through the rest of the algorithm. An entry that sits in a follower's log has been stored. An entry is committed only when it is guaranteed to stay forever. The entries a follower throws away during repair were never committed. Raft only ever overwrites entries that nobody was promised.

So when is an entry committed? The basic rule is the majority rule from the start. Once C has stored the index 7 entry on a majority of servers, itself included, and that entry was created in C's own current term, the entry is committed. In our five-server cluster, if B and D confirm they have stored it, then C, B and D make three, and index 7 is committed. Committing an entry also commits every entry before it in the log, since those are part of the same matching history.

Speed here is set by the fastest majority, not by every server. If E is slow or offline, C does not wait for it. A round trip inside one data centre is under a millisecond, so a write can be committed in a few milliseconds, most of which is servers writing to disk, which each one must do before confirming.

Once the leader knows index 7 is committed, it applies the change to its own state machine, so its copy of the database now says 300, and only then replies to the client that the change succeeded. In its next AppendEntries messages it tells the followers the highest index it knows to be committed. Each follower then applies everything up to that point to its own state machine, in order. Every server ends with max_connections at 300, having applied exactly the same entries in exactly the same order.

Notice what this order of events means for the client. A change is reported as successful only after a majority has stored it. If C crashes one instant after replying, the change still exists on B and D, and it cannot be lost, as long as whoever becomes leader next is guaranteed to carry it forward.

Which raises the question this whole design has been building towards: what stops a server with an incomplete log from becoming leader and overwriting what was promised?

## Staying safe through crashes

We have a leader that copies entries to followers, repairs any follower whose log differs from its own, and treats an entry as committed once a majority stores it. The danger is plain: since a leader forces its log on everyone, a leader with a log that is missing committed entries would erase them.

Back to our cluster. Index 7, "set max_connections to 300", is committed on C, B and D. E was offline at the time and its log stops at index 6. Now C crashes, and by bad luck E's election timeout runs out first. If E won the election, it would start repairing everyone else's log to match its own, deleting index 7 from B and D. A change the client was told had succeeded would vanish.

Raft prevents this with the election restriction: a server refuses to vote for a candidate whose log is less up to date than its own. "Up to date" is judged by comparing the last entry in each log. The log whose last entry has the higher term is more up to date. If the last terms are equal, the longer log is more up to date.

Apply it. E asks for votes. B looks at its own log, which ends at index 7, term 2, and at E's, which ends at index 6, term 1. E's last term is lower, so B refuses. D refuses for the same reason. E can gather votes only from servers whose logs are no better than its own. At best that is A, if A is back and its log also stops at index 6, plus E's vote for itself. Two votes is not three. E cannot win.

This is the overlapping-majorities witness from the beginning, doing its job. The committed entry lives on a majority. Any candidate needs votes from a majority. Those two majorities share at least one server, and that server holds the committed entry and will refuse any candidate that lacks it. So every elected leader already has every committed entry, and the repair process only ever removes entries that were never committed.

There is one more rule, and it exists because of an awkward case. The commit rule given earlier said a leader may count a majority only for entries created in its own current term. Here is why that restriction is necessary.

Take a fresh run of the same five servers. In term 2, A is leader and writes an entry at index 2, but only A and B store it before A crashes. In term 3, E wins with votes from C, D and itself, writes a different entry at index 2 on its own log only, and crashes. In term 4, A comes back and wins again. A now copies its old term-2 entry to C, so that entry sits on A, B and C, three out of five. It looks committed. Suppose A treated it as committed, then crashed.

E can now win term 5. Its last entry has term 3, which is higher than the term 2 at the end of B, C and D, so by the election restriction its log counts as more up to date, and those three vote for it. E then overwrites index 2 everywhere with its own term-3 entry. The entry that appeared to be on a majority is gone.

So Raft adds: a leader counts replicas only for entries from its own current term. In term 4, A would first add a new entry of its own, at index 3 with term 4, and wait until that one reached a majority. Once a term-4 entry sits on three servers, no server with a log ending in term 3 can win an election, because those three would refuse it. Committing the new entry then commits the old term-2 entry underneath it as well. Older entries are committed by being carried along, never by counting alone. This is why a new leader, in practice, appends an empty entry as soon as it is elected: it lets the leader commit everything it inherited without waiting for a client to send something.

Put the two rules together and you get Raft's central promise. Once an entry is committed, every future leader will have it in the same position, and every server will eventually apply exactly that entry at exactly that index. That is what consensus means here: not that every server agrees at every instant, but that no two servers ever apply different entries at the same index.

The promise has a cost worth stating clearly. Raft needs a majority to make progress. If three of our five servers are down, or cut off from each other, A and B cannot elect a leader and cannot commit anything. They will keep refusing writes rather than accept something that might later conflict. Raft chooses being correct over being available, and that is deliberate. A system built on it will stop taking changes before it will lie about them.

There is also a subtlety about reading. Because a stale leader can exist, a client that asks the old leader A for the current value of max_connections might get an outdated answer, even though A cannot commit any new writes. Systems built on Raft handle this by having the leader confirm, with a round of heartbeats to a majority, that it is still leader before answering a read, or by sending the read through the log like any other command. Whether a given system does this by default varies, so it is worth checking in that system's own documentation.

## The whole picture

Raft lets a small, odd-numbered group of servers act as one dependable machine by keeping one ordered log of changes identical on all of them. One elected leader decides the order of entries. Numbered terms let every server tell a current leader from a stale one. Randomised timeouts keep elections quick. The consistency check lets one matching index and term vouch for an entire history, so the leader can repair any follower. Everything rests on majorities overlapping: an entry counts as committed only once a majority holds it, a leader is elected only with a majority's votes, and the server in both groups refuses any candidate missing what was promised. The result is that a committed change survives any crash that leaves a majority standing, and a cluster that loses its majority stops rather than disagrees.

## Going further

Log compaction and snapshots: how a server periodically saves its whole state machine to disk and discards the log entries before that point, so the log does not grow forever.

Membership changes: how servers are safely added to or removed from a running cluster, either one at a time or through a two-step method called joint consensus.

PreVote: an optional extension, used by etcd and others, in which a server checks that it could win before starting a real election, so a server returning from a partition does not disrupt a healthy leader.

ReadIndex and leader leases: the two common techniques that let a leader serve up-to-date reads without writing every read into the log.
