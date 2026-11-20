# Driftwood, the Rust Job Scheduler

I have no reliable knowledge of a tool called Driftwood and will not describe it. What follows explains what a job scheduler is for, so you can open its documentation knowing what to ask.

Rust is a programming language chosen for software that has to be fast and must not crash because of mistakes in how it handles memory, such as servers and system tools. A tool described as "written in Rust" is usually either a program you install and run, or a library that other Rust programs build in.

Take an online shop whose owner wants a sales summary in their inbox every hour: orders taken, money in, items running low. Someone could sit at a computer and start the report program on the hour, every hour, day and night. Nobody wants that task, and the hour they forget is the hour the owner notices.

A piece of work a computer should do without a person starting it is called a job. Here the job is "build the sales summary and email it".

A program that keeps a list of jobs and starts each one at the right moment is called a job scheduler. You give it a rule, "run the summary job at the start of every hour", and it watches the clock and launches the job when the time comes. Schedulers of this kind usually also record whether each run succeeded, so a failure at 3 a.m. is visible in the morning rather than discovered when the owner asks where the 3 a.m. summary went.

That is the whole exchange: a rule that says when, a job that says what, and a program that joins the two while everyone else is asleep.

The common mistake is to assume the scheduler promises that the job runs once, exactly on time, every time. Most schedulers make no such promise by default. Suppose the shop's server restarts for an update at 2:55 and is running again at 3:10. Some schedulers notice the 3:00 run was missed and start it at 3:10; others skip it, and the owner never gets that hour's summary.

Now suppose instead that the server stays up all night, but on a busy evening the 9:00 summary takes 70 minutes to build. At 10:00 the rule fires again while the first run is still going. Depending on the scheduler, the second run waits, is dropped, or starts alongside the first, and the owner may receive two summaries that each counted the same orders.

So a scheduler decides when a job starts. What happens to a missed run, and whether two runs may overlap, are choices each scheduler makes in its own way. The usual practice is to write the job so it copes with both: before sending, the summary job checks whether that hour's summary has already gone out.

## Going further

- How do I write the rule for when a job runs, and which time zone does it follow?
- What happens to a run that was due while the program was stopped?
- Can two runs of the same job overlap, and how do I prevent that?
- Where are jobs and the record of their runs kept, and do they survive a restart?
