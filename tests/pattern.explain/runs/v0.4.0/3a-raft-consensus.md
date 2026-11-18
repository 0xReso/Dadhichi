# Raft: How a Group of Servers Agrees on One Story

By the end you will understand what problem the Raft consensus algorithm solves, how it elects a leader and copies changes between servers, why a change that has been confirmed is never lost, and the point where people most often misread its rules.

## Why one server is not enough

Take an online shop's inventory service. It remembers how many of each item are in stock, and every order checks it before taking a customer's money. If that service runs on a single machine and the machine's disk fails, the shop cannot sell anything until someone repairs it, and any change written since the last backup is gone.

The natural fix is to run copies of the service on several machines, so that one failure does not matter. The copies bring a new danger: they can disagree. Suppose one blue mug is left, and two customers order it in the same second. One order reaches the first copy, the other reaches the second, each copy sees one mug in stock, and both say yes. The shop has now sold a mug it does not have.

Networks make this worse. A faulty switch can cut a group of machines in two, with each half still running and each half unable to see the other. If both halves keep accepting orders, they drift apart, and there is no clean way to merge them afterwards. This situation is called split brain.

What the shop needs is a way for several machines to agree on the same facts even when some of them crash and messages between them are delayed or lost. Getting machines to agree under those conditions is called consensus.

Raft is an algorithm for consensus. It was published in 2014 by Diego Ongaro and John Ousterhout at Stanford University, with the stated aim of being easier to understand than the methods that came before it. Today it runs inside many databases and coordination services that need a small set of facts to stay correct no matter what fails.

Raft does not make the machines agree on stock counts directly. It makes them agree on an ordered list of commands, such as "set blue-mug stock to 40" followed by "subtract 1 from blue-mug stock". This ordered list is called the log, and every server keeps its own copy of it.

Each server feeds the commands from its log, one at a time and in order, into its own copy of the inventory. The part that holds the data and applies commands to it is called the state machine. If every server applies the same commands in the same order, starting from the same empty inventory, every server ends up with the same stock counts. So the whole problem shrinks to one question: how do the servers agree on the log?

The shop runs five servers, which we will call A, B, C, D and E. Together they form a cluster. Raft's central counting rule is the majority: more than half of the cluster, which for five servers means any three. Two different groups of three, out of five, always share at least one server. That overlap is what lets Raft carry knowledge from one decision to the next, and a group large enough to count as a majority is called a quorum.

Because only three of the five need to respond, the cluster keeps working with two servers down. A cluster of four would need three as well, and could survive only one failure, the same as a cluster of three. This is why Raft clusters almost always have an odd number of servers, usually three or five.

With five servers each holding a log, the next question is who decides what goes into it, and in what order.

## Electing a leader

Five servers are trying to keep identical logs, and any three of them make a majority. Raft's answer to the question of order is to put one server in charge at a time.

That server is called the leader, and the others are followers. Only the leader accepts new commands, and the order in which it receives them becomes the order in the log. Followers do not decide anything on their own; they copy what the leader sends and answer its messages.

The leader sends every follower a small "I'm still here" message at regular intervals, often every few tens of milliseconds. This message is called a heartbeat.

Each follower runs a timer that restarts every time a heartbeat arrives. If the timer runs out with no word from the leader, the follower concludes the leader is gone. The length of that timer is the election timeout, and Raft picks it at random for each server, inside a range. The original paper suggests between 150 and 300 milliseconds, roughly the time of a blink.

Raft divides time into numbered periods called terms. Each term begins with an election, and if the election succeeds, one leader runs the cluster until that term ends. Every message a server sends carries its current term number. A server that sees a higher term number than its own adopts it at once and becomes a follower. A message carrying a lower term number than the receiver's is rejected as out of date.

Here is an election in the shop's cluster. A has been leader during term 3, and it crashes. The other four servers stop receiving heartbeats, and their timers start running down. Because the timeouts are random, they do not run out together. C's timer, set to 170 milliseconds, runs out first; D's is set to 260, and the others are longer still.

C raises its term to 4 and declares itself a candidate, the in-between state of a server asking to become leader. It votes for itself and sends a vote request to every other server. This message is called RequestVote.

Each server may vote for at most one candidate in any given term, and gives that vote to the first candidate that asks. B, D and E have not voted in term 4, so all three say yes. With its own vote, C now holds four of five, which is more than the three it needed, and it becomes leader of term 4. It sends heartbeats straight away, and the followers' timers reset before any of them can start a rival election.

Each server writes its current term and the vote it gave onto its disk before replying. A server that crashes and restarts in the middle of term 4 therefore cannot forget it already voted and vote a second time.

Sometimes two timers do run out almost together. If C and D both become candidates in term 4 and each collects two votes, neither has a majority, and nobody wins. Their timers run out again, at new random lengths, and one of them starts term 5 ahead of the other. The randomness makes a repeated tie unlikely.

Now suppose A was not dead, only cut off for a moment. It comes back still believing it leads term 3, and sends a heartbeat. Every server that replies includes term 4 in its answer, A sees the higher number, and A steps down to follower. While it was confused, any request it sent was refused by servers that had already moved to term 4, and three of the five had. There can be at most one leader per term, because winning needs a majority of votes and each server votes once per term.

The cluster has a leader. What happens when a customer actually places an order?

## Copying the log

C now leads term 4, and the others follow it. The shop's stock clerk, through an admin screen, sends the command "set blue-mug stock to 40". The admin screen is the client here: the program asking the cluster to do something. If it happens to send its request to a follower, the follower turns it away and names the current leader, so the client tries C.

C appends the command to the end of its own log. Each place in the log has a position number, called its index, and each entry remembers the term in which a leader first wrote it. C's log already holds seven entries, so the new one sits at index 8 and is tagged with term 4.

C then sends the entry to every follower in a message called AppendEntries. It is the same message type the leader uses for heartbeats; a heartbeat is an AppendEntries that carries no new entries. A follower that accepts the entry writes it to disk and replies that it now holds it.

The message carries one more piece of information: the index and term of the entry just before the new one. Here that is index 7, term 3. A follower accepts the new entry only if its own log has an entry at index 7 with term 3. If it does not, it rejects the message.

That check has a strong consequence, called the Log Matching property. If two servers' logs have an entry with the same index and the same term, then the two logs are identical in every entry up to and including that one. Each accepted entry vouches for the one before it, and that one for the one before it, back to the start of the log.

E was restarted earlier and its log stops at index 5. When it receives the entry for index 8, it has nothing at index 7 and refuses. C responds by stepping back one place and offering entry 7 with the details of entry 6. E refuses again. C steps back once more and offers entry 6, with the details of entry 5. This time they match, E accepts, and C sends entries 7 and 8 behind it. E's log is now identical to C's.

If a follower holds entries the leader does not, left behind by some earlier leader, the same backing-off finds the last point where they agree, and the follower deletes everything after it and takes the leader's entries instead. Information always flows from leader to follower. A leader never deletes or rewrites entries in its own log.

B and D write entry 8 quickly. With C's own copy, the entry now sits on three of five servers, a majority. At that point C marks entry 8 as committed, which means it is permanent: no future leader will ever remove it or put anything else at index 8. C applies the command to its own state machine, so its blue-mug count becomes 40, and tells the client the change is done.

Followers learn that entry 8 is committed from the next AppendEntries C sends them, which includes the highest committed index. Each follower then applies every committed entry it has not yet applied, in order, to its own state machine. A follower can therefore be a little behind for a moment, holding an entry it has not yet applied.

The cost of all this is time. Each write waits for the leader to reach the fastest majority of its followers and for each to save the entry to disk. Inside one data centre that is usually a millisecond or a few; with servers spread across continents it grows to tens or hundreds of milliseconds per write.

That leaves the case Raft was built for. If C crashes right after committing entry 8, could the next leader be a server that never received it?

## Keeping committed entries safe

An entry is committed once a majority of servers hold it, and a leader is elected by a majority of votes. So far nothing ties those two majorities together.

Suppose E had still been offline when entry 8 was committed, so it holds only entries up to 7. If C crashed and E won the next election, E would send its own log out as the truth, and the backing-off from the previous chapter would delete entry 8 from everyone. The clerk was told the stock was set to 40; the cluster would have forgotten it.

Raft closes this gap with a rule on voting. A server refuses to vote for a candidate whose log is less up to date than its own. "Up to date" is judged by the last entry in each log: the one whose last entry has the higher term wins; if the terms are equal, the longer log wins. This is called the election restriction.

Here is why the rule is enough. Entry 8 is on C, B and D. C has crashed, so a winner needs three votes out of A, B, D and E. Any three of those must include B or D, and both of them hold entry 8 at term 4. E's log ends at index 7, so B and D will refuse it. E cannot collect three votes, and only a server holding entry 8 can win. Raft calls the outcome the Leader Completeness property: every leader already holds every entry committed before its term.

This is where the most common misreading of Raft sits. The rule given earlier was that an entry is committed once it is on a majority. That is true for an entry from the leader's own current term. For an entry left over from an earlier term, being on a majority is not enough, and the following run of events in the shop's cluster shows why.

In term 4, C writes entry 9, "set red-mug stock to 12", but manages to copy it only to B before crashing. Entry 9 sits on two of five servers and is not committed.

E wins term 5 with votes from A and D, whose logs end at entry 8 like E's. As leader, E receives a different command, "set red-mug stock to 0", and writes it at index 9 with term 5. It crashes before copying it anywhere.

C restarts and wins term 6, with votes from A, B and D; its last entry is at index 9, term 4, which is at least as up to date as theirs. C carries on sending its old entry 9 and A accepts it. Entry 9, from term 4, now sits on C, B and A, a majority.

If C treated that as committed and crashed, E could restart and stand in term 7. E's last entry is at index 9 with term 5, and term 5 is higher than the term 4 on everyone else's entry 9. By the voting rule, A, B and D would all grant their votes. E would become leader and overwrite index 9 everywhere with "set red-mug stock to 0". An entry that had been declared committed would be gone.

So Raft adds a rule: a leader decides that an entry is committed by counting copies only for entries from its own current term. Older entries become committed indirectly, as soon as a later entry from the current term is committed, because by Log Matching everything before a committed entry is the same on every server that holds it.

In the shop's cluster, C in term 6 writes a new entry at index 10, tagged with term 6, and copies it to A and B. Once three servers hold entry 10, C marks it committed, and entry 9 is committed along with it. Now a majority of servers have a last entry from term 6, which beats E's term 5, and E can never win again with its stale log. Many implementations write an empty "no-op" entry at the start of each new term so that this happens straight away, without waiting for a client to send something.

With these two rules in place, committed entries survive any sequence of crashes and elections. What does that guarantee buy a real system, and what does it cost?

## What Raft gives you and what it costs

The cluster now has a leader that orders commands, a log copied to followers, and voting and commit rules that keep a committed entry permanent. That mechanism shapes how a Raft system behaves when things go wrong.

With two of the shop's five servers down, the other three keep electing leaders and committing entries as normal. With three down, the remaining two cannot form a majority, so they stop accepting writes. They do not guess and they do not give conflicting answers. Raft chooses to stop rather than to be wrong.

A network split plays out the same way. If C and B end up on one side and A, D and E on the other, C may still think it is leader, but it can reach only one follower, so nothing it writes can be committed. On the other side, the three servers stop hearing heartbeats, elect a new leader in a higher term, and carry on taking orders. When the network heals, C sees that higher term, steps down, and its uncommitted entries are replaced. Split brain, the problem from the first chapter, cannot produce two sets of committed orders.

Raft also has firm limits. It assumes every server follows the rules honestly; it protects against crashes, restarts, lost messages and slow networks, but not against a server that lies, whether through a bug or an attacker. A failure in which a machine sends false or contradictory information is called a Byzantine fault, and Raft does not tolerate it.

The other limit is speed. Every write passes through one leader and waits for a majority, so adding servers improves fault tolerance but does not make writes faster, and makes each one wait for more replies. Systems of this kind usually keep a Raft cluster small, holding data that must be correct rather than data that must be huge, such as configuration, ownership of locks, or which machine is responsible for what. Large databases that use Raft generally split their data into many small pieces, each with its own Raft group.

## The whole picture

Raft lets a small cluster of servers behave like one reliable machine by agreeing on a single ordered log of commands, which each server applies to its own state machine to reach the same data. One leader at a time, chosen by a majority vote in a numbered term, decides the order. It copies each entry to the followers with a check on the preceding entry that keeps every log identical up to any matching point, and treats an entry from its own term as committed once a majority holds it. Because any two majorities overlap, and a server will only vote for a candidate whose log is at least as up to date as its own, every new leader already holds every committed entry. The rule that older entries commit only behind a current-term entry closes the one gap that overlap leaves open. The price is that writes wait for a majority and the cluster stops, rather than splits, when it loses one.

## Going further

Snapshots and log compaction: how a server replaces a long log with a saved copy of its state machine, so the log does not grow forever.

Membership changes: the procedure for adding or removing servers safely, either one at a time or through a two-step method the original paper calls joint consensus.

Linearizable reads: the techniques, such as ReadIndex and leader leases, that stop a leader which has been replaced without knowing it from answering reads with stale data.

Paxos: the older and more general consensus algorithm that Raft was designed to be easier to understand than.
