# Raft consensus

You’ll understand how Raft helps several servers agree on the order of changes, even when a server crashes or the network splits.

## Why servers need to agree

An online shop has one backpack left. Two orders arrive close together, and the shop can accept only one. A single server can handle the orders one at a time. But the shop wants to keep taking orders if that server crashes, so it runs the inventory service on three servers, named A, B, and C.

Each server keeps its own copy of the inventory. If A accepts one order while B accepts the other, each can give away the last backpack. The servers need to agree on which order came first. If A crashes after telling a customer their order was accepted, the servers that carry on must also preserve that decision. Reaching and preserving this kind of agreement is called **consensus**. Raft is a set of rules that lets the servers do it.

Each server keeps an ordered record of instructions called a **log**. Each instruction is a **log entry**. For the shop, an entry might say, “Try to reserve one backpack for order 271.” The entry’s position determines when the server will carry out that instruction relative to the others.

To get the same result, the servers start with the same inventory and follow the same rules. If the instruction for order 271 comes first, it reserves the backpack. When the instruction for order 272 runs, there are none left. The program that updates its stored information by following these instructions is called a **state machine**. Raft gives each server’s state machine the same agreed instructions in the same order.

How do the three servers choose who puts the orders in sequence?

## How a leader is chosen

The shop’s servers need one agreed order for the entries in their logs. Raft gives one server at a time the job of adding new entries. That server is the **leader**. The others are **followers**, and they take their new entries from the leader.

The leader sends frequent messages to its followers, even when the shop has no orders to process. An empty message of this kind is called a **heartbeat**. As long as a follower hears from the leader, it waits. If it goes long enough without hearing from the leader, it can start an election. Each follower varies how long it waits so they are less likely to start elections at the same moment.

Raft numbers its election rounds. Each round, including the time that the winner leads, is called a **term**. A server starting an election moves to the next term, votes for itself, and asks the others to vote for it. While it seeks votes, it is called a **candidate**. Servers include their term in their messages. A server that learns of a higher term updates its own and becomes a follower if it was a leader or candidate.

A candidate needs a **majority**, meaning more than half of all the servers in the group. In the shop’s group of three, that means two votes. Each server can vote only once per term. Any two groups of two must share a server, so two candidates cannot both collect enough votes in the same term. If nobody wins, another election can take place in a higher term.

A server also checks the candidate’s log before giving it a vote. It compares the term of the last entry in each log. A log whose last entry is from a higher term counts as more up to date. If the terms match, the longer log counts as more up to date. A server grants its vote only if the candidate’s log is at least as up to date as its own. This rule helps ensure that an election preserves decisions the group has already made.

Suppose A wins an election with its own vote and B’s. When order 271 reaches A, what lets A tell the shop that the backpack is reserved?

## When an order becomes final

A is the leader, so it decides where the reservation instruction for order 271 goes in the log. It stores the entry in its own log, marks it with its current term, and sends it to B and C.

When A sends the entry, it also gives the position and term of the entry immediately before it. A follower checks those details against its log. If they match, the follower can store the new entry and acknowledge it. If they differ, A tries from an earlier position until it finds a point where the logs agree. The follower can then replace any conflicting entries after that point with the leader’s entries.

Say B stores the entry for order 271 and acknowledges it while C is still catching up. A now knows that the entry is stored on two of the three servers, counting itself. Because A created the entry in its current term and has stored it on a majority, A can mark it **committed**. A committed entry has a permanent place in the agreed log. Committing an entry also commits every entry before it. Entries inherited from an earlier term can become committed this way when the leader commits an entry from its own term.

A can now carry out the reservation instruction and return the result. Raft calls carrying out a committed instruction **applying** the entry. A tells its followers how far the log has been committed. Each follower applies those entries in order as soon as it has them. C may learn about the reservation later than B does, so the servers can hold different amounts of the log while still agreeing on the order of its committed entries.

If order 272 follows the same path, its entry can be committed too. When the state machine applies it, the reservation fails because order 271 already took the last backpack. The entry records the instruction to try the reservation, and applying the instruction determines the outcome.

What happens to those decisions if A loses contact with the other two servers?

## What survives a failure

A and B stored the committed entry for order 271 before A reported that the backpack was reserved. Now suppose A loses contact with both followers while C still lacks that entry. B and C can reach each other, so they have enough votes to elect a leader.

If C tries to win while its log is still behind B’s, B will withhold its vote. B can win with its own vote and C’s because B has the more up-to-date log. As leader, B sends C the missing entry. The shop can continue from the agreed record that gave the backpack to order 271.

On its side of the split, A might still believe it is the leader. It could even receive another order and store a new entry. With only its own copy, A cannot commit that entry or report a successful reservation. When contact returns and A learns of the higher term, it becomes a follower. Any conflicting uncommitted entries it stored can be replaced as its log comes back into agreement with B’s.

If no two servers can communicate, the three-server group has no reachable majority and cannot commit any new entries. The shop has to wait to confirm new reservations. Once a majority can communicate again and a leader is available, the group can continue.

## The whole picture

Raft makes the shop’s inventory behave like one ordered service while its log lives on several servers. The leader gives each instruction a position, a majority lets the leader commit new entries, and the election rules protect that committed history when leadership changes. Each server can then apply the same instructions in the same order. An accepted reservation can survive the loss of the server that reported it.