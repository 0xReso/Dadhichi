# Driftwood, the Rust Job Scheduler

I have no reliable knowledge of a tool called Driftwood and will not describe it; what follows explains the kind of tool it is said to be, so you can read its documentation with the right questions in hand.

Rust is a programming language. Programs written in it tend to run fast, and the language catches many kinds of memory mistakes before the program ever runs, which makes it popular for software that has to keep going for months without supervision. Saying a tool is "written in Rust" tells you how it was built, not what it does.

What a job scheduler does starts with a problem. Picture an online shop that needs three things done every night: at 02:00, total up the day's sales and email a report; at 02:30, delete customer uploads older than 90 days; at 03:00, back up the database. Nobody wants to stay awake to start these by hand, and nobody wants them forgotten on a busy week.

Each of those tasks is called a job: a piece of work, usually a program or a command, that should run without a person pressing a button.

A job scheduler is the program that keeps the list of jobs and their times, watches the clock, and starts each job when its moment comes. Schedulers of this kind usually also record whether each run worked, so in the morning you can see that the 02:00 report went out and the 03:00 backup did too.

When a run fails, say the email server was down at 02:00, schedulers usually offer to try again after a pause. That second attempt is called a retry.

Here is where people commonly go wrong. It is natural to assume a scheduled job runs exactly once, exactly on time. In practice schedulers usually promise less. If the machine running the scheduler is switched off from 01:55 to 02:10, the 02:00 report may be skipped, or run late once the machine is back, depending on how the scheduler is set up. And a retry can make a job run twice: if the report was actually sent but the confirmation got lost, the retry sends a second copy. The usual answer is to write jobs so that running them twice does no harm. The cleanup job is already like this: deleting files older than 90 days a second time finds nothing left to delete. A job with that property is called idempotent. The report job is not, unless it first checks whether today's report has already gone out.

So the useful mental picture of any job scheduler is a reliable alarm clock with a logbook, not a guarantee. Whether a specific tool skips, delays, or repeats runs is the thing its documentation has to tell you.

## Going further

- If the machine is off when a job is due, does Driftwood skip that run, or run it as soon as it can?
- Does it retry failed jobs on its own, and can a job end up running twice?
- Does it run on one machine, or can several machines share the list of jobs?
- How do you write down when a job should run, and where is its record of past runs kept?
