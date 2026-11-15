# Driftwood and the Job Schedulers of Rust

By the end you will understand what a job scheduler written in Rust does, how one decides when to run your code, and why "it runs once at two o'clock" is a promise no scheduler can quite keep.

## A word on the name first

Driftwood is described as a job scheduler for Rust, the programming language. I cannot vouch for the exact details of Driftwood itself: its function names, its defaults, or which features it ships with. Small open-source projects change quickly, and a name like this can belong to more than one project. So this piece does something more useful than guessing. It explains the mechanism that a Rust job scheduler of this kind is built on, using the vocabulary its documentation will almost certainly use. When you open Driftwood's own documentation later, you will be reading about choices within a design you already understand.

## The problem it solves

A small online shop sends every customer a summary of their monthly invoices. There are 4,000 customers, and building and emailing all the summaries takes about six minutes. Nobody wants to press a button at two in the morning on the first of every month, so the work has to start by itself.

That piece of work, a named chunk of code that should run without a person starting it, is called a job. The rule that says when it should run, "02:00 on the first day of each month", is its schedule. A job scheduler is the program, or the part of a program, that holds a list of jobs and their schedules and starts each job when its time arrives.

Operating systems already have a basic version of this. On Linux and macOS it is called cron, and it has run scheduled commands since the 1970s. A Rust job scheduler exists because cron sits outside your application. Cron can start a program, but it knows nothing about what happens inside it. It cannot see that the invoice job failed halfway, it cannot retry it sensibly, and it has no idea that a second copy of your application on another server is about to do the same work. A scheduler built into your Rust application lives where the job lives, so it can watch, record, and react.

## How a schedule is written down

Most schedulers, Rust ones included, borrow the notation cron invented. A cron expression is a short line of fields separated by spaces, read from left to right as minute, hour, day of the month, month, and day of the week. A star in a field means "any".

The invoice schedule becomes this:

```
0 2 1 * *
```

Read it field by field: minute 0, hour 2, day 1 of the month, any month, any day of the week. In plain words, two o'clock sharp on the first of every month. Some Rust libraries add a seconds field at the front, which makes the line six fields long instead of five. That difference is a common source of jobs firing at the wrong time, so it is worth checking which form a library expects.

Schedulers usually also accept simpler forms: "every 30 seconds", or "once, at this exact moment". Underneath, all of them answer one question, which is the core of everything a scheduler does: given the time right now, when is the next moment this job should run? That moment is called the next fire time.

## Waiting without wasting effort

A scheduler with one job could loop forever, checking the clock and asking "is it two o'clock yet?" That would keep a processor core busy doing nothing useful for a month.

Instead, the scheduler works out the next fire time for every job, picks the earliest one, and goes to sleep until then. For the invoice job on the evening of 31 January, that means computing 02:00 on 1 February and sleeping for the hours in between. When it wakes, it starts the job, computes that job's following fire time, 02:00 on 1 March, and goes back to sleep until whichever job is due next.

In Rust, this sleeping is usually done with an async runtime. Async code lets one program juggle many waiting tasks without dedicating a thread to each one; a task that is waiting hands control back, and the runtime wakes it when its moment comes. The runtime almost every Rust scheduler builds on is called Tokio. A scheduled job in this world is typically an async function, and starting it means handing it to Tokio as a new task that runs alongside the rest of your application. Your web server keeps answering requests while the invoice job works through its 4,000 customers in the background.

## What happens when a job runs

Starting the job is only the beginning. A scheduler worth using does a few more things each time a job fires, roughly in this order:

1. It records that the run started, and when.
2. It runs the job's code.
3. It records whether the run succeeded or failed, and how long it took.
4. If the run failed, it decides whether to try again.

That fourth step is called a retry policy. The invoice job might fail because the email service was briefly unreachable. A sensible policy waits a little and tries again, then waits longer before the next attempt, up to a limit. Waiting longer each time is called exponential backoff: perhaps 10 seconds, then 20, then 40, so a struggling email service is not hammered by your retries while it recovers.

Where those records are kept matters a great deal. If the scheduler keeps them only in memory, they vanish when the application stops. If it writes them to a database, they survive a restart. A scheduler that stores its jobs and their history in a database is called persistent, and whether a given library offers this, and with which databases, is one of the first things to look up in its documentation.

## Where people go wrong

The trap with schedulers is believing that "run at 02:00" means "runs exactly once, at 02:00". In real systems it can mean zero times, once, or twice, and the shop's invoice job shows all three.

Zero times: the server restarts for an update at 01:58 and comes back at 02:03. A scheduler that only keeps its list in memory starts up, computes the next fire time from "now", and lands on 1 March. February's invoices never go out. Schedulers handle this with a misfire policy, a rule for what to do with runs that should have happened while the scheduler was down: run them once immediately, run every missed one, or skip them. Only a persistent scheduler can apply such a rule, because only it remembers what was due.

Twice, the first way: the shop grows and runs two copies of its application on two servers, so the website stays up if one fails. Each copy contains the scheduler. At 02:00, both wake up and both send the invoices. Customers get two emails each. Preventing this needs the copies to agree on who goes. The usual tool is a lock in a shared database: the first copy to claim the job for that fire time wins, and the other sees the claim and stands down. A lock that expires on its own after a set time, so a crashed server cannot hold it forever, is called a lease.

Twice, the second way: a retry. The job emails 3,000 customers, then the email service times out. The scheduler sees a failure and retries the whole job, and those 3,000 customers receive their summary again. The scheduler cannot know which part of the work finished; only the job can.

That last case leads to the real lesson. Schedulers can reduce duplicates, but across crashes, network failures, and retries, the honest guarantee most of them offer is at-least-once: the job will run, perhaps more than once. The defence lives in the job itself. A job that produces the same result no matter how many times it runs is called idempotent. The invoice job becomes idempotent if it records, per customer, that February's summary was sent, and skips anyone already marked. Then a retry or a duplicate run costs a few seconds of checking instead of 3,000 annoyed customers.

## The whole picture

A Rust job scheduler such as Driftwood exists so that code can run on a timetable from inside your application, where it can be watched, retried, and coordinated, rather than being fired blindly from outside by cron. It turns a schedule, often a cron expression, into a next fire time, sleeps efficiently on an async runtime like Tokio until that moment, runs the job as a background task, records the outcome, and retries failures with backoff. Persistence lets it survive restarts and apply a misfire policy; locks and leases stop several copies of an application from all running the same job. None of that adds up to "exactly once", which is why the final safeguard belongs in the job: make it idempotent, and the scheduler's at-least-once promise becomes safe to rely on.

## Going further

Time zones and daylight saving: a job set for 02:30 local time may be skipped or run twice on the nights clocks change, so check whether schedules are evaluated in UTC or a local zone.

Job queues versus schedulers: tools that run work as soon as it is submitted, often by separate worker processes, overlap with schedulers and are frequently used alongside them.

Graceful shutdown: how a scheduler lets running jobs finish, or abandons them, when the application is asked to stop.

Concurrency limits: settings that stop a job from starting a new run while the previous one is still going.
