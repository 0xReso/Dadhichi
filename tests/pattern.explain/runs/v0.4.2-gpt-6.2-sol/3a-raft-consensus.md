# Raft consensus

You’ll understand how Raft keeps copies of a service in agreement, how it replaces a failed leader, and when it can safely tell you that a change is final.

## The problem with three copies

A booking service has one seat left. You ask to reserve it, and another request for the same seat arrives a moment later. The service has three copies running on separate machines so it can keep working if one machine fails. If two copies accept the two requests independently, both can promise the same seat. The copies need to agree on which request comes first. Reaching that agreement despite some machines failing is the problem Raft solves.

Raft gives each machine an ordered record of the actions the service has been asked to perform. This record is called a **log**. Each action occupies a numbered position. If all three copies begin with the same seat available and carry out the same actions in the same order, they reach the same result. The first reservation takes the seat. The second finds it taken.

One machine at a time is meant to choose that order. It is called the **leader**. The other machines, called **followers**, copy the leader’s log. Call the three machines A, B, and C. With A as leader, all three start with the same first ten log entries. Your reservation is the next request A receives.

A can put your reservation at position 11 on its own machine. If A fails at that instant, the other two machines have no record of it. When can A safely tell you that the seat is yours?

## When a reservation is final

A has given your reservation position 11, but that position still exists on one machine. A sends the entry to B and C. B saves it and replies. C is slow and hasn’t replied yet.

A now has the entry on two of the three machines, counting itself. Two out of three is a **majority**, meaning more than half the group. Any two majorities share at least one machine. If A stops responding and B and C need to choose a new leader, they still have B, which has your reservation. Raft’s voting rules make that overlap count.

Once A knows that a majority has saved position 11, it can mark the entry **committed**. For an entry the leader added while in charge, this is the point at which Raft guarantees that future leaders will keep it. A can now carry out the reservation and return the result to you. Carrying out a committed entry is called **applying** it. Here, applying position 11 changes the booking service’s record from a free seat to a reserved seat.

A also tells the followers how far the log is committed, so they can apply those entries in order. Having an entry and knowing it is committed are separate things. B can have position 11 on disk while still waiting to hear that it is safe to apply.

Suppose A confirms your reservation and then loses its connection to both followers, before C receives position 11. How do B and C choose a leader that will keep the reservation?

## How a new leader takes over

B has your reservation in its log, while C’s log still ends at position 10. Neither has heard from A for a while. A leader normally sends regular messages even when there is no new booking to copy. These messages are called **heartbeats**. When a follower goes too long without hearing from a leader, it can start an election. Followers choose their waiting times at random to reduce the chance that they start together and split the vote.

Raft numbers its election rounds. Each round is called a **term**. Say A led in term 4 and B starts an election in term 5. A machine can vote once in each term, and a machine running for leader needs votes from a majority. B votes for itself and asks C for its vote.

C also checks whether B’s log is at least as up to date as its own. Raft compares the terms in which the last entries were created. If those terms match, the longer log is more up to date. B passes the check because it shares C’s first ten entries and has position 11 as well. C can vote for B, giving B the two votes it needs. If C had asked B for a vote first, B would have rejected it because C’s log ends too early.

B can now send position 11 to C. There is a wrinkle when B works out how far it can safely tell C to apply the log. B can use a majority count to commit an entry it added in term 5. For entries it inherited, a majority count on the old entry alone is insufficient. Once B commits an entry from term 5, the earlier entries in its log are committed with it. This rule matters because an election checks when the last entry was created as well as how long the log is. An earlier entry can appear on a majority without, on its own, settling what a future leader will inherit.

B can add an entry that changes nothing about the booking. Once B and C have saved that entry at position 12, B can commit through position 12 and tell C to apply through it. C applies the reservation at position 11, then applies the entry that leaves the booking as it is. What happens if A still thinks it is in charge during all of this?

## What an isolated leader can do

B and C have elected a leader and kept your reservation, but A may still believe it leads term 4. A has received no message that would tell it otherwise. Two machines can briefly believe they are leaders, each in a different term.

While cut off, A might receive the next reservation request and write it at position 12 in its own log. It has one copy of that entry and needs two to commit it. The same connection loss that kept A from hearing about the election also keeps it from collecting the replies it needs to confirm the new reservation.

When A hears from B in term 5, it steps down. B brings A’s log into line with its own. Their logs agree through position 11. At position 12, A removes the uncommitted reservation and copies B’s entry. If the request reaches B, it can be put in the log and processed in order. It will find the seat already reserved.

The difference between the two reservations is what the service could safely promise. Your reservation was committed before A confirmed it. The request that reached A during the outage received no such confirmation. If the connection breaks while you’re waiting for a reply, the silence alone leaves you unsure. A request might have failed to reach a majority, or it might have committed before the reply was lost.

With three machines, Raft can keep committing changes when two can communicate. If no two can reach each other, new commitments wait. What connects that limit to the promise the service made about your seat?

## The whole picture

Raft gives the booking service one agreed order in which to carry out requests. The leader proposes that order in its log. A majority makes a new entry safe to commit, and the voting rules use the overlap between majorities to keep committed entries in future leaders’ logs. That is how the promise about your seat survives the loss of the machine that made it. When the machines cannot form a majority, the service has to wait before making another promise.

## Going further

- **Log compaction** lets a service save its current state and discard older log entries it no longer needs to replay.
- **Membership changes** are how a running Raft group adds or removes machines while preserving agreement.
- **Linearizable reads** return results that respect the order of completed changes, even when a request reaches a machine whose copy is behind.