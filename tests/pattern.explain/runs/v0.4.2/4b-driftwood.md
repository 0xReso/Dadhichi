# Driftwood, the Rust Job Scheduler

I have no reliable knowledge of a tool called Driftwood, so this piece does not describe it. Instead it explains what a job scheduler written in Rust is for, and ends with questions to take to Driftwood's own documentation.

Rust is a programming language used for software that has to be fast and keep running for a long time, such as servers and system tools. It checks a program for many kinds of memory mistakes before the program ever runs, which is why people pick it for software that sits in the background for months. Saying a tool is "written in Rust" tells you what its authors built it with, not what it does.

Now the problem. Say you run an online shop. Every night at 2 a.m. you want a sales report emailed to you, and every ten minutes you want the system to look for abandoned shopping baskets and send each customer a reminder. Nobody wants to stay awake to press a button at 2 a.m., and a person pressing a button every ten minutes is not a plan.

Each of those pieces of work is called a job: a task a program carries out without anyone asking for it at that moment.

A job scheduler is the program that keeps a list of jobs and the time each one should run, watches the clock, and starts each job when its moment comes. For your shop it holds two entries: "sales report, daily at 2:00" and "basket reminders, every 10 minutes". At 2:00 it starts the report; at 2:10, 2:20 and onwards it starts the basket check. Schedulers of this kind usually also record whether each run succeeded, and can start a failed run again.

Starting a failed run again is called a retry. If the email server is down at 2:00, the scheduler can wait a few minutes and try the report once more, so you still get it before breakfast.

Here is where people commonly go wrong. It is easy to assume a scheduler guarantees each job runs exactly once, exactly on time. In general it cannot promise that. If the machine is switched off at 2:00, the report may be skipped, or start late when the machine comes back. If the basket job crashes halfway through its list, a retry starts it again from the top, and the customers it already reached could get a second reminder.

The usual answer is to write each job so that running it twice does no extra harm: before sending a basket reminder, the job checks whether that customer already got one today. A job with that property is called idempotent, meaning a repeated run changes nothing the first run did not.

## Questions for Driftwood's documentation

- How do you write down when a job should run?
- What happens to a job whose time passed while the scheduler was not running?
- Does it retry failed jobs, and how many times, with what wait in between?
- Can it run on several machines at once, and if so, what stops two machines starting the same job?
