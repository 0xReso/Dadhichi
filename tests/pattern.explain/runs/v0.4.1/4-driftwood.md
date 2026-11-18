# Driftwood, the Rust Job Scheduler

I have no reliable knowledge of a tool called Driftwood and will not describe it; what follows explains what a job scheduler written in Rust usually is, so you can read its documentation with the right questions in hand.

Rust is a programming language. It produces fast programs, and it checks a whole class of memory mistakes while the program is being built from its source code, before it ever runs. Calling a tool "a Rust job scheduler" tells you what it is written in. It may also mean the tool is meant to be used from inside other Rust programs, as a library, rather than as a standalone application; that depends on the tool.

Now the problem such a tool exists to solve. Picture an online shop that wants a sales report emailed to its owners every night at 2 a.m., old abandoned shopping carts deleted every hour, and a confirmation email sent a few seconds after each order. None of this should wait for a person to press a button, and none of it should slow down the page a customer is looking at.

Each of those pieces of work is called a job: a named task the system should run on its own, sometimes on a timetable, sometimes once in response to an event such as a new order.

A job scheduler is the program that keeps the list of jobs and decides when each one runs. At its simplest, it wakes up, checks the clock against every job's timetable, starts the jobs that are due, and goes back to waiting. For the shop, it would see that 2:00 has arrived and start the report job.

Timetables are often written in a compact format called a cron expression, borrowed from the long-standing Unix tool named cron. "0 2 * * *" means minute 0 of hour 2, every day of every month, on any weekday. Schedulers of this kind commonly accept this format, though not all do.

Here is where people most often go wrong: they assume a scheduler guarantees that every job runs exactly once, exactly on time. A basic scheduler only promises to try. If the shop's server is switched off at 2 a.m., the report may simply be skipped. If the report job crashes halfway, it may not be retried. If two copies of the scheduler run on two servers, the report may be sent twice. Whether a given scheduler catches up on missed runs, retries failures, or prevents duplicates is a design choice, and each tool answers it differently. These are the first things worth checking.

## Going further

- Does Driftwood run as its own program, or is it a library you add to a Rust project?
- What timetable format does it accept, and in which time zone are times read?
- If the machine is off or a job fails, does it catch up, retry, or skip?
- Can it run on several servers at once without starting the same job twice?
