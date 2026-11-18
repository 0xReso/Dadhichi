# Driftwood, the Rust job scheduler

I don’t have reliable information about Driftwood itself. Here’s what a job scheduler does and what to look for in Driftwood’s documentation.

Suppose an online shop wants to produce a sales report every morning at 6:00. The report is written in Rust, a programming language used to build software. The report code can add up yesterday’s sales whenever it runs, but the shop still needs something to start it at the right time.

A piece of work that software can start and track is called a **job**. Here, the job is to read yesterday’s sales and save a report. The shop can run that job by hand to check that it works. Once it does, the shop has a separate decision to make about when it should run on its own.

The rule for when a job should run is its **schedule**. The shop’s schedule is “every day at 6:00 a.m. in the shop’s time zone.” The time zone matters because the shop wants the report to follow its business day, even if the computer running it is elsewhere.

A **job scheduler** uses the schedule to decide when the job is due. At 6:00, a scheduler might start the report itself or hand it off to another program that runs it. The report code then reads the sales and writes the file. That division lets the shop move the report to 7:00 without changing how it calculates sales.

The common mistake is to read “scheduled for 6:00” as “the file will be ready at 6:00.” The schedule tells you when the job becomes due. If the report starts on time and takes four minutes, the file is ready at 6:04. If the report runs into an error, it may produce no file at all. To find out whether the report is ready, the shop needs to know how the job finished.

## Going further

- How do you register a job and tell Driftwood when it is due?
- What happens if the program is stopped when a job is due?
- What happens if the next scheduled run is due while the previous run is still going?
- Where can you see whether a run finished successfully?