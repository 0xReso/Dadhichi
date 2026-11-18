# Raft Consensus

By the end you will understand how Raft lets a small group of servers agree on one shared history of changes, even when some of them crash or lose touch, and where people commonly misjudge what it guarantees.

## The problem with copies

Suppose a company keeps a small but vital store of settings: which server handles payments, which feature switches are on, which accounts are frozen. Every other system asks this store before acting. If it lives on one machine and that machine dies, everything that depends on it stops.

The obvious fix is to keep copies on several machines. Say five, named Ash, Birch, Cedar, Dogwood and Elm. Now one dead machine no longer stops anything, because four others still hold the settings.

Copies bring a new problem, though. Two people change the same setting at nearly the same moment. One request reaches Ash first and the other reaches Elm first. Ash now says "payments go to server 7" while Elm says "payments go to server 9", and neither is wrong by its own account. Worse, a network cable can fail so that Ash and Birch can talk to each other but not to the other three. Each side keeps accepting changes, and the copies drift apart. That split, where two groups each believe they are in charge, is called split brain.

What the company needs is for the five machines to behave like one machine that happens not to die. Every copy must hold the same changes, in the same order, and once a change has been confirmed to the person who made it, it must never vanish. Getting several machines to settle on one answer like this, while some of them may be down or unreachable, is called consensus.

Raft is a set of rules for reaching consensus. It was published in 2014 by Diego Ongaro and John Ousterhout at Stanford, with the explicit aim of being easier to understand than the older approaches, and it now sits underneath many widely used databases and coordination services. Its approach is to make one server the leader, let the leader decide the order of every change, and treat a change as final only once more than half of the servers have stored it.

Those two ideas, a single ordered history and "more than half", carry everything else, so what exactly is the history the servers are keeping?

## The log and the majority

The settings store needs five machines that hold identical settings and never lose a confirmed change. Raft gets there by not copying the settings directly at all.

Instead, each server keeps a list of commands, written in the order they should be carried out: "set payments to server 7", then "freeze account 1182", then "turn on the new checkout page". This ordered, append-only list is called the log. Each position in it has a number, called its index, starting at 1.

The settings themselves are worked out by reading the log from the top and carrying out each command in turn. The part of each server that does this, holding the current settings and updating them one command at a time, is called the state machine. It is an ordinary program, here a small table of keys and values, and Raft does not care what it contains.

The trick rests on one plain fact: if two servers start from the same empty table and carry out the same commands in the same order, they end up with the same table. So if Raft can make every server's log identical, the settings follow for free. This whole arrangement, many servers each feeding the same log into their own copy of the same program, is called a replicated state machine, and making the logs agree is the only job Raft takes on.

The second idea is the majority. In a group of five, a majority is three: any number greater than half. Raft uses it as its unit of agreement. A change counts as safely recorded once a majority holds it, and a server counts as leader only if a majority chose it.

Majorities work because any two of them must share at least one member. If Ash, Birch and Cedar hold a change, and later Cedar, Dogwood and Elm agree on something, Cedar is in both groups. There is no way to pick two sets of three from five servers without an overlap. That shared member is how knowledge passes from one decision to the next, and it is why split brain cannot happen: two separate groups of three cannot both exist among five machines.

Here is where many people go wrong. The majority is always counted against the full membership of the group, never against the servers that happen to be running. If Dogwood and Elm crash, the remaining three are still a majority of five and carry on. If Cedar crashes too, Ash and Birch are two out of five. They are not "all the servers that are left, so a majority of the living". They are a minority, and Raft will refuse to confirm any new change until a third server returns. The group stops rather than risk two halves disagreeing, because from the inside Ash and Birch cannot tell whether the others are dead or simply cut off and carrying on without them.

This gives the arithmetic of how much failure a group can survive. Five servers survive two failures. Three survive one. Four also survive only one, because a majority of four is three, so adding a fourth machine buys nothing. This is why Raft groups are almost always an odd size, usually three or five.

So the servers keep an identical log, and a majority is the unit of agreement. Someone still has to decide which command goes at which index, so how does the group choose who that is?

## Choosing a leader

The servers keep identical logs of commands, and anything that counts must be backed by a majority, three of the five. The next question is who decides the order of the commands.

Raft's answer is that one server, the leader, makes every ordering decision. Clients send their changes to the leader. The leader adds each one to the end of its own log and tells the others to do the same. Because only one server writes to the end of the log, two changes can never be given the same index, which removes the "Ash says 7, Elm says 9" problem at its root.

Every other server is a follower. A follower accepts log entries from the leader and answers its messages, and otherwise does nothing on its own. If a client contacts a follower by mistake, the follower points it to the leader.

Time in Raft is divided into numbered periods called terms. Each term begins with an election and has at most one leader. Every server remembers the highest term number it has seen and stamps it on every message it sends. The term works like a clock that only moves forward: a server that receives a message carrying a higher term than its own updates its number at once, and if it was a leader, it steps down to follower. A message carrying a lower term is out of date and is rejected.

Followers need a way to notice that the leader has gone. The leader sends every follower a short "I am still here" message several times a second, called a heartbeat, typically every 50 milliseconds or so, about a third of the time a blink takes. As long as heartbeats arrive, followers stay quiet.

Each follower also runs a countdown, called the election timeout. Every heartbeat resets it. If the countdown reaches zero without a heartbeat, the follower concludes the leader is gone. The original paper suggests a timeout somewhere between 150 and 300 milliseconds, and each server picks its own random value in that range, freshly each time. Real systems tune these numbers to their own network; what matters is that the timeout is much longer than the time a message takes to arrive.

Now follow the example. Ash has been leader during term 4. Ash's power supply fails. The heartbeats stop. Each follower's countdown runs on, and because they were chosen at random, they run out at different moments. Say Cedar's runs out first, at 160 milliseconds; the others have set theirs to between 190 and 280.

Cedar now becomes a candidate, the third and last role a server can hold. It raises its term to 5, votes for itself, and sends every other server a request for its vote. This message is called RequestVote, and it carries Cedar's new term along with a description of the last entry in Cedar's log, which matters a little further on.

Each server may give at most one vote per term, and it gives it to the first candidate that asks, as long as that candidate passes a check on its log. Birch, Dogwood and Elm have not yet voted in term 5, so each grants its vote to Cedar and resets its own countdown. Cedar now has four votes counting its own, well past the three it needs. It becomes leader for term 5 and immediately sends heartbeats to everyone, which tells them there is a new leader and stops anyone else from starting an election.

The randomness is what makes this work most of the time. If every follower used the same timeout, they would all become candidates at once, each vote for itself, and nobody would reach three. That outcome, where no candidate gets a majority, is called a split vote. It can still happen when two countdowns end very close together. When it does, nobody wins term 5, each candidate waits for a new random timeout, and one of them tries again in term 6, usually unopposed. Elections in a healthy group usually finish within a few hundred milliseconds.

Cedar is now in charge, and the others follow it. What does a leader actually do with a change once a client hands one over?

## Copying the log

Cedar is the leader for term 5. It alone decides where each new command goes in the log, and the others follow. Now a client wants to change a setting.

The client sends Cedar the command "set payments to server 9". Cedar's log currently has entries at indexes 1 to 41, so Cedar appends the command at index 42. Each entry records two things beside the command: its index and the term in which the leader created it. This one is index 42, term 5.

Cedar then sends the entry to every follower in a message called AppendEntries. It is the same kind of message as the heartbeat; a heartbeat is an AppendEntries that happens to carry no entries. Each follower that accepts the entry writes it to its own log on disk and replies that it has done so.

Writing to disk before replying is essential. A follower that only held the entry in memory could lose it in a crash, and the leader would be counting a promise that no longer exists.

Dogwood and Elm reply quickly. Together with Cedar's own copy, that makes three servers holding index 42: a majority. At that moment the entry is committed, meaning it is permanently part of the history and will never be removed or replaced. Birch is slow today and has not answered, and it does not matter. Ash is still dead, and that does not matter either.

Only once an entry is committed does Cedar carry it out in its own state machine, so that payments now go to server 9, and tell the client the change succeeded. This order is the heart of the promise: the client hears "done" only after the change is on a majority of disks.

Followers learn that an entry has been committed through the next AppendEntries or heartbeat. Every such message carries the leader's commit index, the highest index it knows to be committed. When Dogwood sees a commit index of 42, it carries out entries up to 42 in its own state machine, and its copy of the settings catches up with Cedar's.

Birch still needs entry 42, and Cedar keeps resending it until Birch accepts. But what if Birch's log has fallen further behind, or holds entries that a past leader wrote and never committed? Raft handles this with a consistency check built into every AppendEntries.

Along with the new entries, each AppendEntries names the entry that should sit just before them: "the entry before this one is index 41, from term 4." A follower accepts the message only if its own log has an entry at index 41 with term 4. If it does not, it rejects the message.

This check rests on a property Raft maintains everywhere: if two logs hold an entry with the same index and the same term, then the two logs are identical in every entry up to that point. A leader creates at most one entry for a given index in a given term, and the check above is applied to every addition, so agreement at one point implies agreement all the way back. This property is called log matching.

When a follower rejects a message, the leader steps back one entry and tries again: "the entry before is index 40, from term 4?" It keeps stepping back until it finds the last point where the follower's log agrees with its own. From there it sends its own entries forward, and the follower deletes anything of its own after that point that conflicts, then appends the leader's entries in their place. Real implementations step back faster than one entry at a time, but the outcome is the same: the follower's log becomes a copy of the leader's.

The direction of this repair is worth holding on to. The leader's log is never changed by a follower; followers are always brought into line with the leader. That raises an uncomfortable question. If a follower can have entries deleted, and the leader's log is always treated as correct, what stops a server with an incomplete log from becoming leader and wiping out a change a client was told had succeeded?

## Why committed changes survive

So far, the leader orders every change, a change is committed once a majority has written it to disk, and followers are always overwritten to match the leader. That last rule is only safe if every leader already holds every committed entry.

Raft guarantees this with a condition on voting, called the election restriction. When a candidate asks for a vote, it describes the last entry in its log: its index and its term. The voter compares this with the last entry in its own log. If the voter's last entry has a higher term, or the same term and a higher index, the voter's log is more up to date than the candidate's, and it refuses its vote.

This is where the overlap of majorities earns its keep. Entry 42 is stored on Cedar, Dogwood and Elm. Any future leader needs votes from three of the five servers. Among any three, at least one must be Cedar, Dogwood or Elm. That server holds entry 42 and will refuse to vote for a candidate whose log lacks it. So no candidate missing entry 42 can collect three votes, and every future leader will have it.

Walk through a bad case to see it hold. Suppose Cedar crashes right after entry 42 is committed, and Ash recovers from its power failure at about the same time. Ash's log stops at index 40, from term 4, and Birch, the slow one, stops at 41. Ash's countdown runs out and it asks for votes in term 6. Birch's log ends with index 41, more up to date than Ash's 40, so Birch refuses. Dogwood and Elm hold entry 42 and refuse too. Ash cannot win. Shortly after, Dogwood's countdown runs out; its log ends at 42 from term 5, which is at least as up to date as everyone else's, so it gathers votes and becomes leader in term 6 with entry 42 intact. It then brings Ash and Birch up to date with the repair process from before.

One further rule closes a narrow gap in this argument. A new leader may find entries from earlier terms in its log that reached some servers but were never confirmed as committed. Raft does not let the leader commit those by counting copies. Instead, it commits them indirectly: once an entry from the leader's own current term reaches a majority, that entry and everything before it are committed together. The reason involves a specific sequence of crashes worth reading about at a desk, but the effect is that a leader only ever declares commitment on the strength of its own term's work.

The same machinery deals with the cut cable from the start. Suppose Dogwood is still leader in term 6, Cedar has since restarted and caught up, and the network splits so that Dogwood and Ash can reach each other but not Birch, Cedar or Elm. Dogwood keeps accepting client requests and sending them out, but only Ash answers. Two out of five is not a majority, so none of these entries is ever committed, and no client is told its change succeeded. Those clients wait, then give up or retry.

Meanwhile, on the other side, Birch, Cedar and Elm stop hearing heartbeats. One of them, say Elm, times out, starts term 7, collects three votes and becomes leader. It can commit changes, because three of five is a majority. When the cable is repaired, Dogwood receives a message stamped term 7, sees that its own term 6 is out of date, and steps down at once. Its uncommitted entries from the isolated period conflict with Elm's log and are removed during repair. Nothing a client was told about is lost, because nothing on Dogwood's side was ever confirmed.

That example also shows the cost Raft accepts. A minority is not merely slower; it cannot make progress at all. Raft chooses to stop rather than risk disagreement, and that is the right choice for settings that other systems trust, but it means a group of five is out of action for writes whenever three of its members are down or unreachable.

It is also worth being clear about the kind of failure Raft is built for. It assumes servers fail by stopping, by being slow, or by losing messages, and that messages may arrive late, twice, or not at all. It does not assume a server might lie, for example by claiming to have stored an entry it threw away, or by sending different answers to different peers. Failures of that kind are called Byzantine faults, and handling them takes a different and more expensive family of protocols. Raft trusts every member of its group to follow the rules, even if they follow them slowly.

## The whole picture

Raft exists so that a few servers can act like one dependable machine: each keeps the same ordered log of commands and feeds it into the same program, so their state stays identical. One leader, chosen by a majority vote in a numbered term, decides the order of every command, and followers that stop hearing its heartbeats elect a replacement after a randomised timeout. The leader copies each new entry to the others, and an entry becomes committed, and is confirmed to the client, only once a majority has written it to disk; a consistency check on every copy forces followers' logs to match the leader's. Because any two majorities overlap, and voters refuse candidates whose logs are less up to date, every new leader already holds every committed entry, so overwriting followers never destroys a confirmed change. The price is that a group can only act while a majority of its full membership is reachable, and it trusts its members to fail by stopping, never by lying.

## Going further

Log compaction and snapshots: a log cannot grow forever, so servers periodically save the current state of their state machine and discard the log entries that produced it, sending the snapshot to followers that have fallen far behind.

Membership changes: adding or removing servers safely, which the Raft paper handles with a two-stage method called joint consensus, and which many implementations do one server at a time instead.

Linearizable reads: answering a read from the leader is only safe if the leader confirms it is still leader, either by checking with a majority or by relying on a time-limited lease, and implementations differ on which they use.

Paxos: the older and widely studied consensus algorithm that Raft was designed to be an easier-to-understand alternative to.
