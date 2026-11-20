# Raft Consensus

By the end you will know how Raft lets a group of servers agree on one shared history of changes, how it picks a leader and survives crashes, and what it cannot protect against.

## The problem: copies that drift apart

Suppose you run a small service that stores settings for a fleet of apps: which features are switched on, what the current price is. If that data lives on one server and the server dies, every app that depends on it stops. The natural fix is to keep copies on several servers, so any one of them can fail without the data disappearing.

Copies bring their own trouble. Say you keep five, on servers called A, B, C, D and E. One client sends "set price to 10" while another sends "set price to 12" at almost the same instant. If A receives the first change before the second, and B receives them the other way round, A ends up with 10 and B with 12. Both servers did their job correctly, they now disagree, and nobody can tell which answer is right. Add crashes, restarts, and network messages that arrive late or never, and the copies drift further apart.

Getting a group of machines to settle on one answer despite failures like these is called consensus. Raft is a consensus algorithm: a precise set of rules that every server follows, so that the group behaves like one dependable machine as long as enough of its members stay up. It was published in 2014 with the stated aim of being easier to understand than the methods before it, and it now runs inside many databases and coordination services.

Raft's central move is to agree on the order of changes rather than on their results. Every change is written as an entry in a numbered list: the first change at position 1, the next at position 2, and so on. This list is called the log. If every server holds the same log and applies its entries in the same order, starting from the same empty data, every server ends up with the same data.

This arrangement is called a replicated state machine. The "state machine" is the data together with the fixed rule for applying each entry to it, and "replicated" means every server runs its own copy. Raft's whole job is to keep the logs identical; once they are, the data takes care of itself. In the example, the question is no longer "is the price 10 or 12" but "which change sits at position 7, and does every server agree on it".

How can five independent servers agree on what goes in each position when any of them might fail at any moment?

## A majority and a leader

You now hold the goal: five servers, A through E, must end up with the same log of changes in the same order. A group of servers working together like this is called a cluster. Raft gets it there by resting on two ideas.

The first is that every decision needs a majority, meaning more than half of the servers. With five servers, a majority is three. Any two majorities drawn from the same five must share at least one server, because two groups of three cannot fit into five without overlapping. That shared server is Raft's thread of memory: whatever one majority agreed to, at least one member of any later majority knows about it. The cost is that five servers keep working with two of them down, but not with three. A sixth server would not help, since a majority of six is four and six servers can still lose only two, which is why clusters are usually built with an odd number of servers.

The second idea is that one server at a time is in charge. That server is called the leader. Clients send their changes to the leader, the leader decides which position each change takes in the log, and it passes the entries on to the others. Because one server chooses the order, the race between "price 10" and "price 12" goes away: whichever reaches the leader first takes position 7, and the other takes position 8.

The servers that are not leading are called followers. A follower decides nothing on its own. It accepts entries from the leader and answers its messages, and in most implementations a client that contacts a follower by mistake is pointed to the leader.

A leader can crash, so Raft needs a way to replace it and a way to tell an old leader from a new one. It divides time into numbered periods called terms. Each term begins with an election, and at most one leader can win in a given term. Every server remembers the highest term number it has seen and stamps that number on every message it sends. When a server receives a message carrying a higher term than its own, it adopts the higher number at once, and if it was a leader, it steps down to follower. A leader from term 4 that freezes for a few seconds and then wakes up learns from the first reply stamped with term 5 that its time is over.

So how does a term begin, and how do the servers choose who leads it?

## Electing a leader

You know now that one leader runs each numbered term and that every decision needs three of the five servers. What remains is how a leader comes into being, and how it gets replaced.

A working leader proves it is alive by sending a short message to every follower at regular intervals, typically every few tens of milliseconds, even when there are no new changes to pass on. This message is called a heartbeat.

Each follower keeps a timer called the election timeout, which restarts every time a heartbeat arrives. If the timer runs out with no heartbeat, the follower concludes that the leader is gone. The paper that introduced Raft suggests a timeout somewhere between 150 and 300 milliseconds, roughly the length of a blink; real systems tune it to their own network.

Suppose A is leader in term 4 and loses power. Its heartbeats stop. On C, the timer happens to run out first. C stops being a follower and becomes a candidate, the third role a server can hold: a server asking to be made leader. It raises its term to 5, votes for itself, and sends a request for votes to every other server.

Each server may cast one vote per term, and it gives that vote to the first candidate that asks. B and D have not voted in term 5, so they vote for C. Counting its own vote, C now has three, a majority of five. It becomes leader for term 5 and starts sending heartbeats at once, which resets everyone's timers and keeps anyone else from starting an election.

Two followers can time out at nearly the same moment, both become candidates, and split the votes so that neither reaches three. That term then ends without a leader, the timers run out again, and a fresh election starts in the next term. Raft makes this rare by having each server pick its timeout at random from the allowed range every time the timer restarts. One server almost always wakes first and wins before the others stir, which is why elections in practice usually settle within a fraction of a second.

With C in charge, how does a change travel from the leader into everyone's log?

## Copying the log and committing

C is now leader of term 5. B, D and E are its followers, and A is still without power. This section follows one change from a client into the logs, and then watches A come back.

One detail from A's last moments matters here. Just before it lost power, A had accepted a change from a client, "turn on dark mode", and written it at position 7 in its own log, but it had not yet sent it to anyone. Every entry in a Raft log carries the term in which it was created, so this one is marked term 4. The other servers' logs all end at position 6.

Now a client sends C "set price to 12". C writes it at position 7 in its own log, marked term 5, and sends it to every follower in a message called AppendEntries. This is the same message type that, sent with no entries in it, serves as the heartbeat.

B and D store the entry and reply that they have it. The entry now sits on three servers, C, B and D, which is a majority. At that moment C marks it committed, meaning the entry is permanent and no future leader will ever remove it. C applies it, so the price on C is now 12, and answers the client. Each later message from C carries the highest committed position, and the followers apply entries up to that point when they see it. E's reply arrives a little late, which changes nothing: the leader waits for a majority, not for everyone, so one slow server cannot hold up the whole cluster.

This is where the most common misunderstanding of Raft sits: the belief that a change is safe once the leader has written it. A's dark-mode entry shows why it is not. A was the leader, it wrote the entry, and the entry is still doomed, because it never reached a majority and so was never committed. The client that sent it never received a reply. Raft's promise covers committed entries, those stored on a majority, and nothing short of that.

The way A loses that entry is the log's repair mechanism. Every AppendEntries message carries, alongside the new entries, the position and term of the entry just before them. A follower accepts the new entries only if its own log holds an entry with that same position and term; otherwise it refuses. This is called the consistency check.

When power returns, A's first message from C carries term 5, so A becomes a follower. C sends it position 7, along with a note that position 6 should be from term 4. A's position 6 matches, so it accepts, but its own position 7 is marked term 4 while C's is marked term 5. A deletes its conflicting entry and everything after it, and takes C's entry instead. Had A's log differed further back, it would have refused, and C would have stepped back one position at a time, retrying, until it found the point where the two logs agree, then sent everything from there forward. The leader's log always wins, and followers are brought into line with it.

That raises a worry. If the leader's log always wins, a server that missed recent changes must never become leader. Raft adds one more rule to voting for exactly this reason: a server refuses its vote to a candidate whose log is less up to date than its own. It compares the last entry in each log. The one written in the later term counts as more up to date, and if both were written in the same term, the longer log does.

Suppose A, back from its outage, had timed out before hearing from C and stood as a candidate in term 6. Its log ends at position 7, term 4; B's and D's end at position 7, term 5. Both would refuse, and A could not win. The majority overlap does the rest: a committed entry sits on at least three servers, a winning candidate needs three votes, so at least one voter holds every committed entry and will turn away a candidate that lacks it.

Committed entries can't be lost while a majority survives. But what happens when that condition fails?

## What Raft cannot survive

You have the full mechanism now: a leader per term, elected by a majority of up-to-date voters, copying entries that become permanent once a majority stores them. Each guarantee leans on assumptions, and the edges of those assumptions are worth knowing.

If three of the five servers are down, no candidate can gather three votes and no entry can reach a majority. The cluster stops accepting changes. This is deliberate: Raft prefers to stop rather than let two parts of the cluster make decisions that disagree.

The same rule governs a network split. Suppose a fault cuts C and E off from A, B and D. C still believes it is leader, but it can reach only one follower, so nothing it receives can be committed and its clients wait without an answer. On the other side, one of A, B and D times out, wins an election in term 6 with three votes, and carries on. When the network heals, C sees term 6, steps down, and the consistency check removes whatever uncommitted entries it collected. One subtlety: during the split, C might still answer requests to read data with values that are already out of date, because it does not know it has been replaced. Implementations handle this in different ways, commonly by having the leader confirm with a majority before answering a read.

Raft also assumes that servers fail only by stopping, slowing down, or losing messages, never by lying. A server with a corrupted disk that reports entries it never stored, or a compromised server sending false votes, can break its guarantees. Protecting against misbehaving servers is a separate and more expensive family of algorithms, known as Byzantine fault tolerance.

Finally, the guarantees hold only if each server writes its current term, its vote, and its log to disk before replying to a message. A server that forgot its vote after a restart could vote twice in one term and help elect two leaders. That disk write, plus a network round trip to a majority, is the price of every change: well under a millisecond inside one data centre, but tens of milliseconds when the servers sit in different regions.

## The whole picture

Raft exists so that a group of servers can act as one dependable machine: rather than agreeing on data, they agree on a single ordered log of changes and each apply it in the same order. Terms give time a numbered sequence so that an old leader can always be recognised and retired. Elections, triggered by a missing heartbeat and spread out by random timeouts, put one leader in charge of each term, and the vote rule ensures that leader already holds every committed entry. The leader copies entries with AppendEntries, the consistency check forces every follower's log to match its own, and an entry becomes permanent the moment a majority stores it. Underneath all of it is one fact: any two majorities overlap, so whatever one majority knew, the next one cannot forget.

## Going further

- Log compaction and snapshots: how servers periodically replace a long log with a saved copy of the data, so the log does not grow forever.
- Membership changes: how servers are added to or removed from a running cluster without two majorities appearing at once, through an approach called joint consensus or by changing one server at a time.
- Committing entries from earlier terms: a new leader does not count a majority for an old entry as committed until an entry from its own term is also stored on a majority, a rule that closes a rare failure case.
- Paxos: the older and more general consensus algorithm that Raft was designed as an easier-to-understand alternative to.
