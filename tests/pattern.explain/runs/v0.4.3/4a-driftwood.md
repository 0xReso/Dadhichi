# Driftwood, the Rust job scheduler

I have no reliable knowledge of a tool called Driftwood, so this piece does not describe it. It explains what a job scheduler written in Rust is for, so you can open Driftwood's own documentation knowing what to ask.

Rust is a programming language used for software that has to be fast and hard to crash, such as parts of web browsers and operating systems. Saying a tool is "written in Rust" tells you what it was built with, and often that it is meant to be added to other programs written in Rust. It does not tell you what the tool does.

The problem a job scheduler exists for is an ordinary one. Say you run an online shop and want a sales report emailed every night at 2:00 a.m., abandoned shopping carts cleared every hour, and a welcome-back email sent three days after each new sign-up. Nobody wants to stay up to start these by hand, and writing a separate timer into the shop's code for each task gets tangled quickly.

Each of those tasks is called a job: a piece of work your program can start on its own, such as "build yesterday's sales report and email it to the owner".

The rule for when a job runs is called its schedule. "Every day at 2:00 a.m." is a schedule, and so is "once, three days from now".

A scheduler is the part that holds all the jobs and their schedules and starts each one when it is due. It keeps a list of upcoming start times, waits until the earliest one arrives, starts that job, and then works out when the job is next due. Your report job starts at 2:00 a.m., and the scheduler immediately notes that the next run is 2:00 a.m. tomorrow.

The common mistake is to treat a scheduled job as a promise that it will run. A scheduler can only start jobs while it is running itself. If the shop's server restarts at 1:55 a.m. and is back at 2:10, nothing was awake at 2:00, and that night's report may never be sent. Schedulers of this kind usually guard against this by writing their list of jobs somewhere that survives a restart, such as a database, and checking for missed runs when they start up again. The opposite failure exists too: if two copies of the shop's program are running, each with its own scheduler, the owner can get the same report twice. How a given scheduler handles these two cases is often the main difference between one scheduler and the next, and the first thing worth checking.

## Going further

Questions to take to Driftwood's documentation:

- Does it run inside your own program as a library, or as a separate service your program talks to?
- Where does it keep its list of jobs, and does that list survive a restart?
- What does it do about a run that was due while it was stopped: run it late, or skip it?
- How does it stop two copies of a program from running the same job twice?
