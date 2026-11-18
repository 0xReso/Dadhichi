# Raft consensus

You’ll understand how Raft keeps a group of servers in agreement about what happened, even when a server fails or the network splits.

## Why the order matters

A shop has one jacket left. Two customers try to buy it at nearly the same time. The shop runs its inventory service on three servers so it can keep taking orders if one goes down. If each server can decide on its own whether a sale goes through, two servers could promise the same jacket. The service needs the three servers to agree on which purchase to handle first.

Each server keeps an ordered record of commands, such as “reserve one jacket for order 421.” This record is called a **log**, and each command recorded in it is a **log entry**. A server can have an entry in its log while the group is still deciding whether that entry belongs in the agreed order.

Each server also runs the same rules for updating inventory. Given the same starting inventory and the same commands in the same order, every server reaches the same result. This rule-following part of the service is called a **state machine**. Raft handles agreement on the log. The state machine handles what a command means for the shop, including whether there is a jacket left to reserve.

Raft is a **consensus algorithm**, a set of rules servers follow to agree even when messages are delayed or servers stop responding. It gives one server at a time the job of deciding where new commands go in the log. How do the servers choose who gets that job?

## Choosing a leader

The shop’s servers need one server to put new commands in order. That server is called the **leader**. The other servers normally act as **followers**. They receive log entries from the leader and keep their own copies.

Raft divides time into numbered periods called **terms**. An election starts a new term, and a term can have at most one elected leader. A term can also end without a leader if nobody wins the election. Servers include their term numbers in messages, so a server that learns of a higher term knows its own information about who leads is out of date.

A leader sends regular messages even when there are no new commands to copy. These messages are called **heartbeats**. If a follower goes long enough without hearing from a leader, it can start an election. Followers wait for randomly chosen lengths of time, making it less likely that several will start elections together.

In the shop’s group, suppose server A starts an election. It advances to a new term, votes for itself, and asks servers B and C for their votes. To win, A needs a **majority**, which means more than half the servers in the group. Here that takes two votes. Each server gets one vote per term, so two candidates in the same term cannot both get a majority. Suppose B votes for A. A becomes leader and starts sending heartbeats.

A also recorded the new term before asking for votes. Servers save their current term, their vote, and their log in storage that survives a restart. If B restarts during the election, it still knows how it voted.

A now has the authority to propose an order for the shop’s commands. What makes a command safe to act on?

## Committing a purchase

Server A is the leader, so it takes the request to reserve the jacket for order 421 and appends it to its log. A records the entry’s **index**, its numbered position in the log, and stamps it with the current term. It then sends the entry to B and C.

Before a follower accepts an entry, it checks that the preceding position in its own log has the term number the leader expects. If the follower is missing earlier entries or has a conflicting entry there, it rejects the request. The leader then tries from an earlier position until the logs match at that point, and sends the entries the follower needs from there. This lets a follower catch up in order.

Suppose B saves the entry for order 421 and acknowledges it. C has yet to receive it. The entry is now on A and B, a majority of the three servers. Because A created the entry in its current term, A can mark it **committed**. From here on, any future leader must preserve that entry in that position.

A can now **apply** the entry, which means handing the command to its state machine. The state machine reserves the jacket, so the shop can tell the customer that order 421 got it. In later messages, A tells the followers how far the log has been committed. Each follower applies the committed entries it has, in order.

This is where it’s easy to mistake a saved entry for a completed purchase. Saving is one step toward commitment. A leader can save a command and lose contact with the other servers before any of them copies it. A later leader may then replace that entry. The shop waits for the command to be committed and applied before reporting the result.

Order 421 is committed on A and B, and C is still behind. What happens if A drops out now?

## Keeping the purchase through a failure

The shop has already confirmed order 421. Now A stops responding. B has the entry for the order, and C is missing it. The two remaining servers can still form a majority, so the group can elect a leader and keep working.

Raft ties the right to lead to what a server has saved. When a server is asked for its vote, it compares the candidate’s last log entry with its own. The log whose last entry comes from a higher term counts as more up to date. If those terms are equal, the log with the higher last index counts as more up to date. A server grants its vote only if the candidate’s log is at least as up to date as its own.

In the shop’s case, if C asks B for a vote while still missing the entry for order 421, B refuses. C has its own vote and needs a second. In a new election, B can win with C’s vote because B has the more up-to-date log. B becomes leader and sends C the missing entry. The majority that saved the purchase and the majority that elects the new leader share a server. The voting rule makes that overlap count by giving B a reason to refuse a candidate whose log is behind.

B may have missed A’s message saying how far A had committed. Raft has a rule for this situation. A leader advances commitment by counting copies of an entry from its **current term**. Once that entry is committed, all earlier entries in its log are committed as well. If the request for the last jacket arrives at B now, B can append it in its new term and get C to save it. Committing that new entry also establishes that B can apply through order 421. When B applies the commands in order, the second request finds that the jacket is already reserved.

If B and C also lose contact with each other while A is down, neither can form a majority. The shop has to wait before it can confirm another purchase. The agreed order remains protected while the service waits for enough servers to communicate again.

## The whole picture

Raft gives the shop one agreed order for its inventory commands. A leader puts commands in the log, a majority saves enough of that log for the leader to commit new entries, and the servers apply the committed commands in order. When the leader changes, the voting rule protects the entries the shop has already relied on. Order 421 keeps its place, and every server that applies the next purchase request reaches the same answer about the last jacket.

## Going further

- **Election timeout** is how long a follower waits without hearing from a leader before starting an election.
- **Snapshots** capture the state after a set of committed commands so a server can discard the corresponding older log entries.
- **Membership changes** let a running Raft group add or remove servers while preserving agreement.