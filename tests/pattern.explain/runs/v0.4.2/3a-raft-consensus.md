# Raft: How a Group of Servers Agrees on One History

By the end you will understand what the Raft consensus algorithm is for, how it elects a leader and copies one shared record of changes across several servers, and why it keeps working through crashes and network splits as long as most of the servers can still reach each other.

## Why one copy is not enough

Picture an online shop whose checkout reads its settings, such as the current discount, from a small database on one server. While that server runs, all is well. When it crashes, or its disk fails, or someone reboots it for an update, checkout cannot read its settings and stops. The obvious fix is to keep copies of the settings on several servers, so that losing one does not matter.

Copies bring a new problem. Suppose one change says "set the discount to 10%" and another says "set it to 15%". If one server receives them in that order and another receives them the other way round, the first ends at 15% and the second at 10%, and both believe they are right. Messages across a network can be delayed, lost or reordered, and a server can be down while changes happen and come back later holding an old picture. Getting a group of machines to agree on the same data in spite of all that is called consensus.

Raft is an algorithm for reaching consensus. Two researchers at Stanford University published it in 2014, with the stated aim of being easier to understand, and so easier to build correctly, than the methods that came before it. Today it sits underneath many widely used systems, most often to keep small, critical databases of settings and coordination data consistent.

The settings database has a helpful property. It holds some data and changes that data only when given a command, and the result depends only on the data it started with and the command it received. Give two copies the same starting data and the same commands in the same order, and they end up identical. A program that behaves like this is called a state machine.

That property shrinks the problem. Instead of agreeing on the settings themselves, the servers only need to agree on the list of commands and their order. Raft calls this ordered list the log. Each item in it is an entry holding one command, and each entry has a position number called its index: the first entry is index 1, the next is index 2, and so on. Raft's whole job is to make every server end up with the same entries at the same indexes. Each server then feeds those entries, in order, to its own copy of the settings database.

The shop runs five servers, which this article calls A, B, C, D and E. A group of servers running Raft together is called a cluster.

Raft never waits for every server in the cluster to answer. It waits for a majority: more than half, which in a five-server cluster means three. Waiting for everyone would let one crashed server halt the cluster; waiting for three means the cluster keeps working with any two servers down. Majorities also have a property that matters a great deal: any two majorities of the same cluster share at least one server. Three servers plus three servers is six, and there are only five, so at least one server belongs to both groups. Whatever one majority has stored, any later majority includes at least one server that has stored it.

That still leaves a question: when several commands arrive at once, who decides their order?

## Electing a leader

You now hold the basic picture: five servers, each keeping a log of commands, and a rule that a majority, three of the five, is enough to act. Someone still has to put the commands in order.

Raft hands that job to a single server, called the leader. The leader receives every new command, places it in its own log, and tells the others what to add. Because one server sets the order, two commands cannot end up in different orders on different servers.

The other servers are followers. A follower does not take commands from the checkout service, which is the program sending the changes; it waits for the leader and adds what the leader tells it to add. If the checkout service contacts a follower, the follower turns it away, and most implementations tell it which server is the current leader.

Raft divides time into numbered periods called terms: term 1, term 2, term 3, and so on. Each term begins with an election and has at most one leader. Every server keeps its own copy of the current term number and attaches it to every message it sends. Terms work as a clock all servers can compare. When a server sees a message carrying a higher term than its own, it knows it has fallen behind, so it updates its number and, if it was anything other than a follower, becomes a follower again. A message carrying a lower term is stale, and the receiver rejects it.

A leader holds its position by sending small messages to every follower at regular intervals, even when there are no new commands. These are called heartbeats. In the shop's cluster, say the leader sends one every 50 milliseconds, twenty a second.

Each follower runs a countdown timer called the election timeout, and every heartbeat resets it. If the timer runs out with no word from a leader, the follower concludes that the leader is gone. Each server picks its timeout at random from a range, for example between 150 and 300 milliseconds, the range suggested in Raft's original paper. The randomness matters: if every follower's timer ran out at the same instant, they would all try to take over together and get in each other's way.

Here is how the shop's cluster gets its first leader. All five servers start as followers in term 0, with empty logs and no leader. No heartbeats arrive, so the timers run down. A happened to pick 180 milliseconds, the shortest of the five, so its timer runs out first.

A server whose timer has run out and that is trying to become leader is called a candidate. On becoming one, A moves its term to 1 and votes for itself.

A then asks every other server for its vote, using a message that Raft's description calls RequestVote. The message carries the new term number, 1.

Each server votes at most once per term, and gives that vote to the first candidate that asks. It writes the vote to its disk before replying, so that a restart cannot trick it into voting twice. B, C, D and E have not voted in term 1, so they grant their votes. As soon as A counts three votes, its own plus those from B and C, it has a majority and becomes leader of term 1. It sends heartbeats at once, and the other timers reset before they run out.

The voting rule is what keeps a term to one leader. Winning needs a majority, two majorities always share a server, and that shared server can only have voted once in the term, so two candidates cannot both win it.

Sometimes two followers' timers run out close together, each gathers some votes, and neither reaches three. This is called a split vote. Each candidate's timer runs out again at a fresh random value, and the next attempt starts with a higher term. The randomness makes repeated ties unlikely, so in practice an election usually finishes within a fraction of a second.

So the cluster has a leader. What does the leader do when a command arrives?

## Copying the log

The cluster now has a leader, A, for term 1, kept in place by its heartbeats, with B, C, D and E following. The leader's real work is getting commands into everyone's log.

The checkout service sends A the command "set discount to 10%". A adds it to the end of its own log as index 1. Alongside the command, every entry records the term in which the leader created it, so this entry is labelled index 1, term 1. The term label lets servers tell whether two entries at the same index came from the same leader.

A sends the entry to each follower in a message Raft's description calls AppendEntries. A heartbeat is the same message with no entries in it. Each follower writes the entry to its log on disk and replies that it has stored it.

Once a majority of the cluster, counting the leader itself, has stored an entry, the leader marks it committed. B and C reply first, so A, B and C make three, and index 1 is committed without A waiting for D or E. Committed is Raft's word for permanent: a committed entry will stay at its index in the log of every future leader, whatever crashes follow.

Committed entries are the ones that get applied, meaning fed to the state machine. A applies index 1 to its copy of the settings database, which now shows a 10% discount, and only then tells the checkout service that the change succeeded. Each AppendEntries also carries the index of the latest committed entry, so with the next heartbeat the followers learn that index 1 is committed and apply it to their own copies.

Meanwhile, E was offline for a few seconds and missed index 1 entirely. Then the checkout service sends "set discount to 15%", and A stores it as index 2, term 1, and sends it out.

Every AppendEntries also names the entry that should come directly before the new ones; here it says "previous entry: index 1, term 1". A follower accepts the new entries only if its own log holds an entry at that index with that term. This is called the consistency check.

E, now back online, receives the message, has no index 1, and rejects it. A responds by stepping back one position and trying again: "previous entry: none; new entries: index 1 and index 2". E's log is empty, which matches "none", so it accepts both. In general, the leader keeps stepping back until it reaches the last point where the follower's log agrees with its own, then sends everything after that point.

Because every entry was accepted only after the entry before it matched, the check builds a chain. If two servers' logs hold an entry with the same index and the same term, their logs are identical in every entry up to that point. Raft's paper calls this the Log Matching Property.

All five servers now hold index 1 and index 2, both from term 1 and both committed, and every copy of the settings shows a 15% discount. All of this depends on A, though. What happens to the log when the leader fails halfway through a change?

## When the leader crashes

The log now holds two committed entries on all five servers. A, leader of term 1, sends each new command to the followers and counts an entry committed once a majority has stored it.

The checkout service sends "set discount to 20%". A stores it as index 3, term 1, gets it to B, which stores it too, and then A loses power before the message reaches anyone else. A and B now have index 3; C, D and E stop at index 2. Two copies out of five is not a majority, so index 3 is not committed. A never applied it and never told the checkout service it succeeded; from the checkout service's side, the request timed out.

The heartbeats stop. C's timer runs out first, so C becomes a candidate for term 2 and sends RequestVote to the others.

At this point a second voting rule comes into play. A server refuses its vote to any candidate whose log is less up to date than its own. To compare two logs, look at their last entries: the one whose last entry has the higher term is more up to date, and if the terms are equal, the longer log is. RequestVote carries the index and term of the candidate's last entry for exactly this comparison. Raft calls this rule the election restriction.

Apply it to the shop. C's last entry is index 2, term 1. B's last entry is index 3, term 1: the same term, but B's log is longer, so B refuses. D and E also end at index 2, term 1, so C's log is as up to date as theirs, and they grant their votes. C, D and E make three, and C becomes leader of term 2.

The election restriction is what protects committed entries. A committed entry is stored on a majority. A winning candidate collected votes from a majority. Those two majorities share at least one server, and that server holds the committed entry, so it refuses its vote to any candidate whose log lacks it. Raft's full proof has more steps than this, but the overlap is its heart. In the shop, indexes 1 and 2 sit on all five servers, so whoever wins has them.

Index 3 is a different case. It was never committed, so nobody was promised it. B's log is as up to date as anyone's, so had B's timer run out first, B could have won term 2 and kept index 3. Either outcome is safe, because the checkout service was never told the change succeeded.

The checkout service retries and sends "set discount to 20%" to C, the new leader. C stores it as index 3, term 2, and sends it out.

B now holds a different entry at index 3: the same index, but labelled term 1 rather than term 2. When a follower finds an entry that conflicts with the leader's, meaning the same index with a different term, it deletes that entry and everything after it, then takes the leader's entries in their place. B throws away its old index 3 and stores C's. The leader never deletes or rewrites its own log; entries flow from the leader to the followers and never the other way.

A's power comes back. Because A wrote its term, its vote and its log to disk, it restarts still believing it is in term 1, with its old index 3. C's first heartbeat carries term 2, so A updates its term and stays a follower. The consistency check finds A's index 3 in conflict with C's, and A replaces it. All five servers now hold indexes 1 and 2 from term 1 and index 3 from term 2, all committed, and the discount is 20%.

A crash is clean: the server stops, and everyone notices. What happens when every server is alive but they cannot all reach each other?

## When the network splits

C now leads term 2, and all five logs hold the same three committed entries, ending with a 20% discount. You have seen a leader crash, the election restriction protect what was committed, and a follower's stray entry overwritten.

Then a faulty network switch divides the cluster. C and D can still talk to each other, and A, B and E can talk to each other, but no message crosses between the two groups. A split like this is called a network partition.

On the small side, nothing tells C that anything has changed. It has not crashed and has seen no higher term, so it still believes it is leader of term 2. A checkout service instance on that side sends it "set discount to 25%". C stores it as index 4, term 2, and sends it to D, which stores it. That makes two copies, and C needs three, so the entry never commits. C never applies it and never confirms it.

On the large side, A, B and E stop receiving heartbeats. E's timer runs out first, and E becomes a candidate for term 3. All three logs end at index 3, term 2, so E's log is as up to date as the others', and A and B vote for it. E leads term 3. A checkout service instance on this side sends "set discount to 5%". E stores it as index 4, term 3, A and B store it too, and with three of five it commits. E applies it and confirms.

For a while, then, two servers both act as leader: C in term 2 and E in term 3. This is where many people's picture of Raft breaks, because Raft is often summed up as "there is always one leader". What Raft actually guarantees is narrower: at most one leader per term. Two servers can believe they lead at the same moment, in different terms, and the one in the older term cannot commit anything, because it cannot reach a majority. The leader is not the final authority; the majority is. A command is safe once it is committed, not once a leader has accepted it.

The same point applies to reading data. If C answered "what is the discount?" from its own copy, it would say 20% while the cluster had already committed 5%. Systems built on Raft usually guard against this, for example by having the leader confirm with a majority, through a round of heartbeats, that it is still leader before answering a read, or by passing reads through the log like any other command. The exact approach differs between implementations.

When the switch is fixed, C receives a message from E carrying term 3. C sees the higher term and becomes a follower. Its index 4 is labelled term 2, which conflicts with E's index 4 from term 3, so C deletes its entry and takes E's, and D does the same. The 25% change that was never confirmed disappears; the 5% change that was confirmed stays. All five servers agree again.

The majority rule also sets Raft's limits. If three of the five servers are down or cut off, no group has a majority, so no leader can be elected and no command can commit. The cluster stops accepting changes rather than risk two versions of the truth. Odd cluster sizes follow from the same arithmetic: a four-server cluster needs three for a majority, so it survives only one failure, no better than three servers. Three servers survive one failure, five survive two, and seven survive three, though every commit then waits on more replies.

Raft also assumes that servers fail by stopping, and that the network fails by losing or delaying messages. It does not defend against a server that lies, whether through a bug or an attacker, by sending false terms or invented entries. Failures of that lying kind are called Byzantine failures, and surviving them needs different and more expensive algorithms.

## The whole picture

Raft lets a cluster of servers behave like one reliable machine by agreeing on a single ordered log of commands, which each server feeds to its own identical state machine. Terms and randomised election timeouts produce at most one leader per term, and that leader decides the order of commands and copies them out with AppendEntries, while the consistency check keeps every follower's log in line with the leader's. An entry becomes permanent once a majority has stored it, and the election restriction ensures that any future leader already holds it, because every majority that elects a leader overlaps every majority that stored a committed entry. Crashes and partitions can leave stray, uncommitted entries or an outdated leader, but those were never confirmed and are overwritten once a majority's leader is heard from. The cost is that nothing changes while a majority cannot be reached, and that the servers are trusted not to lie.

## Going further

- **Snapshots and log compaction:** how a server saves the current state and discards old log entries, so the log does not grow forever.
- **Membership changes:** how servers are added to or removed from a running cluster safely, described in Raft's paper as joint consensus, with a simpler one-server-at-a-time method used by many implementations.
- **Committing entries from earlier terms:** a new leader counts copies only for entries from its own term; older entries become committed along with the first entry of its own term that reaches a majority.
- **Paxos:** the older and more famously difficult consensus algorithm that Raft was designed to be an easier alternative to.
