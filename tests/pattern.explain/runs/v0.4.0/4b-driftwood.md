# Driftwood and What a Job Scheduler Does

I have no reliable knowledge of a Rust job scheduler called Driftwood, so this page will not describe it; what follows explains the kind of tool it is said to be, so you can read its documentation with the right questions in mind.

I cannot tell you what Driftwood does, how it is built, or what its parts are called. Anything written here under its name would be a guess, and you would have no way to tell the guess from a fact. What I can explain is the general job that a job scheduler does, which gives you a frame to hold its real documentation against.

Start with the problem. Picture an online shop. When a customer places an order, the shop has to send a receipt email, and every night at 2 a.m. it has to build a sales report. Neither task should hold up the customer: if the email server is slow and takes ten seconds to answer, the customer should not stare at a spinning checkout page for those ten seconds.

The usual answer is to treat each piece of work as a separate item to be done later. One such item, "send the receipt for order 4512" or "build last night's report", is called a job. The checkout page records the job and replies to the customer at once, and the email goes out a moment afterwards.

A job scheduler is the program that keeps track of jobs and decides when each one runs. Schedulers of this kind usually handle two sorts: jobs to run as soon as possible, like the receipt, and jobs to run on a timetable, like the 2 a.m. report. They usually hand jobs to a small pool of background workers, and they often retry a job that fails, so a receipt that bounced off a busy email server at 14:03 gets another try a minute later.

Rust, the language Driftwood is described as written in, is a programming language known for producing fast programs while catching many memory mistakes before the program ever runs. A scheduler written in Rust is normally used from inside a Rust program, though the sources behind this article do not cover how Driftwood is meant to be used.

The common misunderstanding about schedulers in general is to think of one as a fancy timer. A timer inside a running program forgets everything if that program restarts. If the shop's server reboots at 1:59 a.m., a timer-only setup can silently lose both the pending receipt and the night's report. Many schedulers therefore write their jobs to a database or other lasting storage, so the work survives a restart. Whether a given scheduler does this is one of the first things worth checking.

## Going further

Questions to take to Driftwood's own documentation:

- Where does it keep its jobs: only in the program's memory, or in a database that survives a restart?
- Does it support timetable jobs, such as "every night at 2 a.m.", as well as run-once jobs?
- What happens when a job fails: does it retry, how many times, and how long does it wait between tries?
- If two copies of the program run at once, can the same job end up running twice?
