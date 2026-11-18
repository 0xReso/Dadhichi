# Driftwood, the Rust job scheduler

I don’t have reliable knowledge of Driftwood’s design, so this article explains what job schedulers do in general.

A shop needs to generate a sales report at 6 every morning, even if nobody opens the shop’s app. The report program knows how to add up the sales and write the report. Something else needs to decide when that work is due and arrange for it to run. That is the job of a **job scheduler**.

A **job** is a unit of work the scheduler can arrange to run. For the shop, the job is “generate the daily sales report.” The report program still contains the instructions for reading sales and calculating totals.

A **schedule** tells the scheduler when the job is due. The shop sets its schedule for 6 a.m. every day in the shop’s local time. When 6 a.m. arrives, the scheduler can start the report program itself or hand the job to another program that runs it. Which arrangement applies depends on the scheduler.

The important distinction is between a job being due and a job finishing successfully. The report can be due at 6, start at 6, and still fail because the sales records are unavailable. When the scheduler records job outcomes, checking the outcome tells you whether that run succeeded. The schedule tells you when it was meant to happen.

Even a job that runs every day can miss a scheduled time. If the shop’s scheduler is offline at 6 and comes back at 6:20, its rules determine whether it starts the missed report then or waits until the next morning. The daily schedule alone leaves that question open.

## Going further

- How do you register the daily report job in Driftwood and set the time zone for its schedule?
- Does Driftwood run the job itself, or does another program run it?
- What happens to a job that comes due while Driftwood is offline?
- Where can you check whether a job finished, and can Driftwood try it again after a failure?