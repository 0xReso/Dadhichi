# Raft consensus

You’ll understand how Raft keeps several servers in agreement about which changes count and in what order, even when a server fails or loses contact.

## One history across three servers

An online shop has 40 units of a product. When an order reserves 5, the shop needs to remember that 35 remain, even if the server that took the order goes offline. Keeping copies on three servers helps. But if each server accepts changes on its own, two servers can take orders against the same stock. The shop needs the servers to agree on which changes count and in what order. That agreement is called consensus. Raft is a protocol, a set of rules the servers follow to reach it.

Raft has each server keep an ordered record of changes called a log. Each record, called a log entry, contains an instruction such as “reserve 5 units.” A server puts the instruction into effect by applying the entry. Starting from the same stock level, servers that apply the same entries in the same order arrive at the same stock level.

One server at a time is elected to put new entries in order. That server is the leader. The other servers are followers. The leader takes requests, adds entries to its log, and sends them to the followers. Keeping copies of the log on several servers is called replication.

A leader needs support from more than half the servers, a group called a majority. In the shop’s three-server cluster, a majority is any two servers. Any two such groups have at least one server in common. That overlap matters both when a leader records a change and when the servers choose its replacement.

What does the leader need to see before it can tell the shop that the reservation succeeded?

## When a reservation counts

The shop has three copies of the log, and the leader puts new reservations in order. Suppose server A is the leader when the request to reserve 5 units arrives.

A adds the reservation as entry 12 in its log and sends it to servers B and C. The message also identifies entry 11 by its position and by the numbered round of leadership in which it was created. Raft calls that round a term. A follower accepts entry 12 at that point only if its own entry 11 matches. The check makes sure the new instruction follows the same history on both servers.

B stores entry 12 and tells A it has done so. C is slow to respond. A now knows that the entry it created in its current term is stored by a majority, A and B. At that point, A can treat entry 12 as committed. A committed entry is part of the history that future leaders must preserve.

A applies the committed entries in order. When it applies entry 12, the stock falls from 40 to 35 and A can report success. A also tells the followers how far the log has been committed, so each can apply the committed entries it has. For a short time, B may have stored the reservation without applying it, and C may still lack the entry. The servers can be at different points in the same history.

The important distinction is between storing an entry and committing it. A follower’s acknowledgement says it stored the entry. The leader uses those acknowledgements to determine when the entry can count. There is one wrinkle when leadership changes: for an entry inherited from an earlier term, a new leader cannot establish commitment by counting copies of that entry alone. Once it commits an entry from its own term, all preceding entries in its log are committed too.

If A loses contact before telling C about the reservation, how does the shop keep the sale in its history?

## How a replacement keeps the reservation

A and B stored the committed reservation, while C may still be missing it. Now suppose A loses contact with both of them. B and C can still reach each other, so a majority is available to elect a replacement.

A leader periodically sends messages to show it is still in contact. These are called heartbeats. If B goes long enough without hearing from a leader, it starts an election by advancing to a new term and asking for votes. A server seeking election is called a candidate. Servers wait for varying amounts of time before starting an election, which makes it less likely that B and C will ask for votes at the same moment.

Each server votes at most once per term. That rule, together with majority overlap, means two candidates cannot both win the same term. A server also checks the candidate’s log before granting its vote. It compares the terms of their last entries first. If those terms are equal, it compares the positions of those entries. It grants its vote only if the candidate’s log is at least as up to date by that test.

That check matters if C asks first. C’s log ends at entry 11, so B refuses to vote for it. With A unreachable, C cannot win on its own. If B asks in a term when C still has a vote available, C can vote for B. B wins with its own vote and C’s, and the new leader has entry 12.

The vote is about what the servers have stored. Even if A disappeared before telling B that entry 12 was committed, B has the entry it needs to preserve. Raft’s voting and log rules work together to ensure that a server elected in a later term carries the committed history forward.

A may still think it is leader while it is cut off. What keeps it from making a second version of the shop’s history count?

## What happens to entries that never counted

B can lead with C’s support, while A has only its own copy of the log. A may still receive a request. Suppose it adds an entry 13 to reserve another 7 units. A cannot get a second server to store that entry, so it cannot commit it or report a successful reservation.

Meanwhile, B brings C up to date by sending it entry 12. When the shop asks B to reserve 4 units, B records that request at entry 13 in its own term. Once C stores it, B can commit it. Applying the log through entry 13 leaves 31 units, from the original 40 minus the reservations of 5 and 4.

When contact returns, A learns that B is leading in a later term and becomes a follower. B sends its entry 13. A already has an entry at that position, but the terms differ. A deletes its conflicting entry and stores B’s. The 7-unit request never became part of the committed history, which is why replacing it leaves the shop’s confirmed stock intact.

The shop can keep making changes as long as a majority can communicate and settle on a leader. If all three servers lose contact with one another, each has only one vote and one copy. New reservations have to wait until a majority can communicate again.

## The whole picture

Raft gives the shop one history by making the leader place each reservation in an ordered log and requiring a majority to support new commitments. An election also needs a majority, and each voter checks the candidate’s log. Together, those rules let B take over with the 5-unit reservation intact, while A’s isolated 7-unit entry can disappear without changing any reservation the shop confirmed.

## Going further

- **RequestVote** is the message a candidate uses to ask another server for its vote.
- **AppendEntries** is the message a leader uses to copy entries to followers and to send heartbeats.
- **Log compaction** saves the state produced by an applied stretch of the log in a snapshot, so old entries can be discarded.