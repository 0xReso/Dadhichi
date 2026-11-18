# Driftwood, the Rust Job Scheduler

I have no reliable knowledge of a tool called Driftwood. This page explains the kind of software it is said to be, and leaves Driftwood's own features to its documentation.

I cannot recall concrete facts about a Rust job scheduler named Driftwood that I would stand behind, so nothing below describes it. What follows is about job schedulers in general, the category the name puts it in, so that you can open its documentation already knowing what to look for.

Start with the problem. Take an online shop. When you place an order, the shop wants to email you a receipt, and every night at 2 a.m. it wants to total the day's sales into a report. Neither belongs inside the web request that shows you "Order confirmed": the email server might take several seconds to answer, or be down, and the nightly report has no request to hang on at all.

A job scheduler is the program that takes this work off the request's hands. Each piece of work is written down as a job: a small record saying what to run and with what input, such as "send receipt for order 4182". The shop's web code hands the job over and answers you at once.

The scheduler keeps waiting jobs in a queue, an ordered list of work not yet done. Schedulers of this kind usually keep the queue somewhere that survives a restart, such as a database, so a crash at 1:59 a.m. does not lose the night's report.

Separate processes called workers take jobs off the queue and run them. You can add more workers when the queue grows, without touching the web code.

When a job fails, say because the email server is down, the scheduler puts it back to be tried again later, usually waiting a little longer after each failure. That is called a retry.

Recurring work, like the 2 a.m. report, is commonly written as a cron expression: a short line of five fields for minute, hour, day of the month, month, and day of the week. "0 2 * * *" means minute 0, hour 2, every day.

Rust is a programming language that compiles to fast machine code and checks, before the program ever runs, that it does not misuse memory. A scheduler written in Rust is usually one of two things: a library you build into your own Rust program, with jobs written as Rust functions, or a standalone service that runs jobs for programs written in any language. Which one a tool is changes how you use it.

The usual mistake is assuming a job runs exactly once. Most schedulers promise only that it runs at least once. If a worker sends the receipt and then crashes before reporting success, the scheduler sees an unfinished job and runs it again, and you get two receipts.

The fix lies in the job, not the scheduler: write it so that repeating it does no harm. Here the worker first checks whether the receipt for order 4182 has already gone out. A job built this way is called idempotent.

## Going further

Questions to take to Driftwood's documentation:

- Is it a library inside a Rust program, or a standalone service?
- Where does it keep its queue, and does that survive a restart?
- Does it run jobs at least once or exactly once, and how does it retry them?
- Does it accept cron expressions for recurring jobs?
