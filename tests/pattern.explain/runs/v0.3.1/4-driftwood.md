# Driftwood and What a Job Scheduler Does

I have no reliable knowledge of a Rust job scheduler called Driftwood, so this piece does not describe it; it explains the kind of tool it is said to be, and ends with questions to take to its documentation.

I cannot tell you anything specific about Driftwood: not its features, its design, or the words it uses for things. Anything written here under its name would be a guess, and you would have no way to tell it from a fact. So what follows is about job schedulers in general, and about what being written in Rust usually means for one.

Start with the problem. Say a small online shop needs to email every customer a receipt, rebuild its sales report every night at 2 a.m., and delete abandoned shopping carts once an hour. None of this should happen while a shopper waits for a page to load, and none of it should be forgotten if the server restarts. Each of these pieces of work, done outside the moment someone asks for it, is called a job.

A job scheduler is the program that decides when each job runs and makes sure it does. It usually keeps a list of jobs waiting to run, called a queue. Some jobs go on the queue the moment they are needed, like the receipt email. Others repeat on a timetable, like the 2 a.m. report, and schedulers of this kind often write that timetable in cron syntax, a compact five-field notation borrowed from an old Unix tool, where "0 2 * * *" means "at minute 0 of hour 2, every day".

Separate programs called workers take jobs off the queue and carry them out. If the email server is down and the receipt fails, a good scheduler tries again later, a step called a retry, usually waiting a little longer after each failure so it does not hammer a service that is already struggling.

The common trap is assuming a job runs exactly once. In practice most schedulers promise that a job runs at least once: if a worker crashes after sending the receipt but before reporting success, the job is retried and the customer gets two emails. The usual defence is to write jobs so that running them twice does no harm, a property called idempotence.

Rust is a programming language known for catching many memory and concurrency mistakes before the program runs, and for producing fast programs. Schedulers written in it are typically used by other Rust programs, added as a library, though whether Driftwood works that way is one of the things I cannot tell you.

## Going further

When you open Driftwood's documentation, these questions will orient you quickly:

- Where does it keep its queue: in memory, where jobs vanish on a restart, or in a database that survives one?
- Does it promise at-least-once or exactly-once running, and what does it say about duplicates?
- How does it handle retries and failed jobs that never succeed?
- Is it a library you add to your own Rust program, or a separate service you run beside it?
