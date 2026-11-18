# Driftwood and the Job Scheduler

I have no reliable knowledge of a Rust job scheduler called Driftwood, so nothing below describes it; this piece explains what a job scheduler is in general, so you can read Driftwood's own documentation with the right questions in hand.

I have no facts about Driftwood that I would stand behind, and the material I was given contains nothing about it. Anything I wrote under its name you would take as true, with no way to check it from where you are sitting. So what follows is about the kind of tool it is said to be, and you should not read any of it as a description of Driftwood.

The problem a job scheduler solves is a familiar one. Say a small online shop needs three things done without anyone pressing a button: send a sales report every morning at 7:00, retry failed card payments every 15 minutes, and resize each product photo soon after it is uploaded. Each of these is a piece of work that runs on its own, away from any user waiting for a reply. That unit of work is called a job.

A job scheduler is the program that decides when each job runs and then makes sure it does. Some jobs are tied to the clock, like the 7:00 report. Others are triggered by an event, like the photo upload. Schedulers of this kind usually hold the jobs that are waiting in a queue, an ordered waiting line, and hand them one by one to workers, the parts of the program that do the actual work. If the shop gets 200 photo uploads in a minute, the queue holds them and the workers get through them at whatever pace they can manage.

The useful part is what happens when things go wrong. Schedulers of this kind usually retry a failed job a set number of times, often waiting a little longer after each failure, and record what happened so a person can look later. Some also store the queue on disk or in a database, so jobs survive a restart. Others keep it only in memory, so anything still waiting is lost if the program stops.

Rust is a programming language known for speed and for catching many memory mistakes before a program ever runs. A scheduler written in Rust is usually either a library you build into your own Rust program or a separate service that other programs send jobs to. These are very different things to run, and the name alone does not tell you which one Driftwood is.

The common mistake is to assume a scheduler guarantees each job runs exactly once. In general practice, many promise "at least once": after a crash, a job may run twice. That is why the shop's payment retry should check whether a payment already went through before charging again.

## Going further

Questions to take to Driftwood's documentation:

- Is it a library inside your program, or a separate service you run?
- Where does it keep waiting jobs, and do they survive a restart?
- Does it promise that each job runs at least once, at most once, or exactly once?
- Does it handle clock-based schedules, event-triggered jobs, or both?
