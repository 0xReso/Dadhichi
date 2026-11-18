# Raft: How a Group of Servers Agrees on One Story

By the end you will understand how Raft lets a handful of servers behave like one dependable machine: how they pick a leader, how commands are copied safely, and why the cluster stops rather than give two different answers.

## Why one copy is not enough

Picture an online shop that keeps its settings on a single server: the price of tea, whether checkout is switched on, which discount codes are valid. Every part of the shop asks that one server. It works well until the server's disk fails or its machine reboots for an update. Then the whole shop stops, because nothing else knows the answers.

The obvious fix is to keep copies on several servers. Say five of them, which we will call A, B, C, D and E. A crash of one now leaves four. But copies bring trouble of their own. Suppose one part of the shop tells A to set the tea price to 4, and at almost the same moment another part tells B to set it to 5. A and B each pass the news on to the others, the messages cross on the network, and some servers end up with 4 while others end up with 5. The shop now quotes a different price depending on which server it happens to ask.

What the shop needs is for the five servers to agree. Getting a group of machines to settle on the same values, in the same order, even when some of them crash and messages arrive late or not at all, is called consensus. Raft is a consensus algorithm, a set of rules each server follows. It was published in 2014 and was designed from the start to be easier to understand than the methods that came before it.

Raft does not make servers agree on the shop's settings directly. It makes them agree on a list of instructions. Each server keeps an ordered list of commands, such as "set tea-price to 4" followed by "set checkout to on". That list is called the log. Each position in it has a number, starting from 1, and that number is called the index.

The log is enough because of a plain fact about programs. If two copies of the same program start in the same state and carry out the same commands in the same order, they end up in the same state. So if all five servers hold the same log, and each one applies those commands in order to its own copy of the settings, all five copies will match.

The program that applies the commands is called the state machine. Here it is the small piece of software that holds the shop's settings and changes them when told to. The whole arrangement, many copies of one state machine all fed from one agreed log, is called a replicated state machine, and it is what Raft exists to build.

That turns a vague worry into one precise question. If any server can crash at any moment, and messages between servers can be delayed or lost, how do five servers agree on what sits at each index of the log?

## Why three out of five is enough

You now hold the goal: five servers, each with a log of commands, which must agree on the command at every index. Raft's first tool for this is a counting rule.

The group of servers working together is called the cluster. Raft treats something as settled once more than half of the cluster has it. More than half is called a majority, and in Raft writing you will also see it called a quorum. In a five-server cluster, a majority is three.

Three is enough because of overlap. Any two groups of three drawn from five servers must share at least one member, since three plus three is six and there are only five servers to go round. So if one decision was made by A, B and C, and some later decision is being made by C, D and E, then C was present for both. C remembers the first decision and can refuse anything that contradicts it. Almost every safety rule in Raft rests on this one fact: two majorities of the same cluster always have a server in common.

The counting rule also sets how many failures the cluster survives. Five servers need three to act, so two can be down and the cluster keeps working. Three servers need two, so they survive one failure. Seven servers survive three.

This is why clusters nearly always have an odd number of servers. A four-server cluster needs three for a majority, so it survives only one failure, the same as a three-server cluster, while having one more machine that can break. Going from five servers to six raises the majority to four and buys no extra tolerance either.

The majority is always counted against the full membership of the cluster, not against whichever servers happen to be reachable. If three of the five are down, the two that remain are not "a majority of two". They are two out of five, and they cannot settle anything.

Counting tells the cluster when something is safe, but it does not say who gets to propose what. If all five servers could suggest different commands for the same index at once, the votes could still split. So who proposes?

## Electing a leader

So far you have the log, which the servers must agree on, and the majority, three of five, which is how agreement is counted. Raft's next move is to stop everyone proposing at once.

At any time, one server is the leader. It alone accepts new commands and decides the order they go into the log. The other servers are followers: they take what the leader sends them and never add commands on their own. The parts of the shop that send commands, called clients, send them to the leader, and a follower that receives one points the client to the leader instead.

With one leader there is no crossing of messages over who went first. Whatever order the leader writes commands into its log is the order. The hard part moves somewhere else: what happens when the leader crashes, and how the servers make sure there is never more than one leader giving orders.

Raft divides time into numbered periods called terms. Terms count upward, 1, 2, 3 and so on. Each term begins with an election and has at most one leader. Every server remembers the highest term number it has seen, and stamps that number on every message it sends.

The term number works as a clock that cannot drift. Servers do not trust each other's wall clocks, which can disagree by seconds. Instead, a higher term number always means newer information. When a server receives a message carrying a higher term than its own, it moves up to that term, and if it was acting as a leader it steps down to follower. When it receives a message carrying a lower term, it rejects the message as out of date.

A leader keeps its position by sending regular messages to every follower. When there are no new commands to pass on, these messages are empty and only say, in effect, "I am still here." They are called heartbeats, and leaders typically send them every few tens of milliseconds.

Each follower runs a timer, and every heartbeat resets it. If the timer runs out with no word from the leader, the follower concludes that the leader has gone. The length of that wait is called the election timeout. The original Raft paper suggests picking it at random, separately on each server, somewhere between 150 and 300 milliseconds, roughly the length of a blink. Real systems often use longer values, tuned to their own networks.

Now the running example. It is term 7, and A is the leader. A's machine loses power. B, C, D and E stop hearing heartbeats. Each of them chose its own random timeout, and C's happens to be the shortest, 170 milliseconds, so C's timer runs out first.

A follower whose timer runs out becomes a candidate. C raises its term from 7 to 8, votes for itself, and sends a request for votes to every other server. That request is a message called RequestVote, and it carries C's new term, 8.

Each server gives at most one vote per term, to the first candidate that asks. It writes that vote to disk before replying, so that a crash and reboot cannot trick it into voting twice in the same term. B and D have not voted in term 8, so they vote for C. E's network link is flaky that afternoon and its reply never arrives. That does not matter: C has its own vote plus B's and D's, which makes three of five, a majority. C is the leader for term 8, and it sends heartbeats at once, which reset everyone's timers before anyone else tries.

There can be only one leader per term because of the counting rule. Winning needs three votes. Any two groups of three share a server, and that server votes once per term. So two candidates cannot both collect three votes in term 8.

The randomness in the timeout has a job. If every follower waited exactly the same time, they would all become candidates together, each would vote for itself, and nobody would reach three. That outcome is called a split vote. The term then ends with no leader, the timers run again, and a new term begins. Spreading the timeouts at random makes it likely that one server starts well ahead of the rest and wins before the others wake. Split votes still happen now and then, and each one costs another round of waiting.

When A's power comes back, A still believes it is the leader of term 7 and starts sending heartbeats. The other servers reply with their term, 8. A sees a higher term than its own, moves up to term 8, and becomes a follower of C.

The cluster has a leader again. How does a command that reaches the leader get into every other server's log, and when is it safe to say it has happened?

## Copying commands to every log

C now leads term 8, and every client command goes to C. Follow one command through.

The shop's admin page sends C the command "set tea-price to 4". C adds it to the end of its own log, at the next free position, index 12. Alongside the command, C records the term in which the entry was created, 8. Every log entry carries both: the command, and the term it was written in. So this entry is index 12, term 8.

C then sends the entry to every follower in a message called AppendEntries. This is the same message type as a heartbeat: a heartbeat is an AppendEntries message with no entries in it. A follower that accepts the entry writes it to its own log on disk and replies that it succeeded.

An entry that is stored on a majority of servers is called committed. C has its own copy. When B and D reply, that makes three of five, and entry 12 is committed. Raft guarantees that a committed entry is permanent: it will never be removed or replaced on any server, in any later term.

Only once the entry is committed does C apply the command to its state machine, so the tea price on C becomes 4, and only then does C tell the admin page that the change succeeded. This is where a common misreading creeps in: the idea that a write is done as soon as the leader has it. It is not. Suppose C had crashed after writing entry 12 into its own log but before any follower received it. That entry could then vanish, and that would be correct behaviour, because the admin page was never told it succeeded. It would wait, get no answer, and send the command again to whichever server leads next.

The followers also need to know when to apply the entry. The leader keeps track of the highest index it knows to be committed, called the commit index, and includes it in every AppendEntries message it sends, heartbeats included. When B and D see a commit index of 12, they apply entry 12 to their own state machines, and their tea price becomes 4 too.

Logs can fall out of step. A follower that was offline misses entries. A server that was leader can hold entries that never reached anyone else. Raft forces each follower's log back into line with a check built into every AppendEntries message: along with the new entries, the leader sends the index and term of the entry that comes immediately before them. A follower accepts the new entries only if its own log has an entry at that index with that same term.

When C sends entry 12, it says: "the entry before this one is index 11, term 7." B and D have exactly that, so they accept.

E is different. Its flaky connection means its log stops at index 9. When E reconnects and C sends it entry 12 with "the previous entry is index 11, term 7", E has nothing at index 11, so it refuses. C steps back and tries again with entry 11, saying the previous one is index 10. E refuses again. C steps back once more and sends entry 10, saying the previous one is index 9, term 7. E has that, so it accepts. C then sends 11 and 12, and E has caught up.

A is different again. Just before its power failed, A, still leader of term 7, had written a command, "set checkout to off", into its own log at index 12, term 7. No other server ever received it. When C sends A its own entry 12, the previous-entry check passes, because A does hold index 11, term 7. But A's index 12 carries term 7 while the incoming entry carries term 8, so they conflict. A deletes its own entry 12, and anything after it, and takes C's entry in its place. Nothing of value is lost: A's entry sat on one server out of five, it was never committed, and so no client was ever told it had worked.

This check gives Raft a property called Log Matching: if two servers' logs hold an entry with the same index and the same term, then the two logs are identical in every entry up to that point. Each accepted entry vouches for the one before it, which vouched for the one before that, all the way back to index 1.

Notice that the leader's log wins every disagreement. Followers are overwritten; the leader never is. That is only safe if the leader already holds every committed entry. What stops a server with an out-of-date log from becoming leader and overwriting entries that clients were told were saved?

## Why committed entries survive

You now hold the whole working cycle: one leader per term, chosen by a majority of votes; commands copied out by the leader; an entry committed once a majority stores it; and followers' logs forced to match the leader's. The gap is that last part. Because the leader's log always wins, a leader missing a committed entry would erase it from everyone.

Go back to the moment E reconnected, while its log still ended at index 9, and suppose C crashed right then and E's timer ran out first. If E could win the election, it would make every log look like its own, and entries 10, 11 and 12, including the tea-price change the admin page was told had succeeded, would be wiped out.

Raft closes this gap with a rule called the election restriction: a server refuses to vote for a candidate whose log is less up to date than its own. To make this possible, every RequestVote message carries the index and term of the candidate's last log entry. A voter compares that with its own last entry. Whichever last entry has the higher term is more up to date. If the terms are equal, the longer log is more up to date.

E's request would say its last entry is index 9, term 7. A, B and D all end at index 12, term 8, a higher term, so all three refuse. E can gather at most its own vote, and it never becomes leader. One of the servers holding entry 12 wins instead.

The guarantee comes from the overlap of majorities once more. Entry 12 is committed, so it sits on at least three servers. Any winning candidate needs votes from at least three servers. Those two groups of three must share a server, and that shared server holds entry 12 and will only vote for a candidate whose log is at least as up to date as its own. So whoever wins the next election already has entry 12. And since a leader never overwrites its own log, entry 12 survives that term, and the next, and every one after.

Now the most common misunderstanding of Raft, which surfaces when the network itself breaks. Many people picture Raft as keeping things running as long as some servers are up, or imagine each side of a broken network carrying on by itself. Neither is true.

Suppose a faulty network switch splits the cluster in two. C and D can reach each other, and A, B and E can reach each other, but no message crosses between the groups. C is still leader of term 8. It keeps accepting commands, writes "set tea-price to 5" at index 13, and sends it to D. That entry reaches two servers out of five, never a majority. It never commits, and C never tells the client it succeeded.

On the other side, A, B and E stop hearing heartbeats. B's timer runs out first. It starts term 9, and A and E vote for it, since their logs are no more up to date than B's. B is now leader of term 9. This side has three of five servers, so it can commit, and it commits "set tea-price to 6" at index 13, term 9.

When the switch is replaced, C receives a message carrying term 9, sees a higher term, and steps down. C's and D's entry at index 13 has term 8, which conflicts with B's index 13, term 9, so it is replaced. No committed entry has been lost. The client whose "set to 5" was never confirmed eventually gives up waiting and retries.

So the minority side keeps running but cannot make progress. That is the price Raft pays for never giving two answers. If three of the five servers are lost, the two survivors cannot accept a single write until enough of the others come back. Raft deliberately chooses being correct over being available whenever it cannot have both.

The split also shows a quieter danger, which concerns reads rather than writes. While cut off, C still believed it was leader. If it had answered a question such as "what is the tea price?" straight from its own state machine, it would have said 4 while the real, committed price was 6. Correct Raft implementations guard against this, either by passing reads through the log like any other command, or by having the leader confirm with a majority that it is still leader before it answers.

Finally, Raft assumes servers fail honestly. A server may crash, run slowly, or lose messages, but it never lies about its log or its votes. A server that sends deliberately false or corrupted messages is showing what is called a Byzantine fault, and Raft offers no protection against it. Defending against that needs a different and more expensive family of algorithms.

## The whole picture

Raft lets a cluster of servers act as one reliable machine by agreeing on a single log of commands, which each server applies in order to its own copy of the state machine. One leader at a time orders every command; it holds its place with heartbeats and is replaced by an election, numbered by term, when followers stop hearing from it. An entry counts as committed only once a majority stores it, and because any two majorities share a server, two leaders cannot win the same term, and the election restriction ensures every new leader already holds every committed entry. The leader then forces followers' logs to match its own, discarding only entries that were never committed. When too few servers can talk to each other to form a majority, the cluster stops accepting changes rather than risk telling two clients two different things.

## Going further

Log compaction and snapshots: how servers stop their logs growing forever by saving the current state and discarding old entries, and how a lagging follower is sent a snapshot instead of the full history.

Membership changes: how servers are added to or removed from a running cluster without two different majorities existing at once, through joint consensus or one-server-at-a-time changes.

Linearizable reads: the techniques, often called ReadIndex and leader leases, that let a leader answer reads quickly without serving stale data.

Committing entries from earlier terms: a subtle rule under which a new leader never counts copies of an older term's entry to commit it, and instead commits it indirectly by committing an entry of its own term on top.
