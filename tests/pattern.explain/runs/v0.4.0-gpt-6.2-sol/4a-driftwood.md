# Driftwood, the Rust job scheduler

I don’t have reliable knowledge of Driftwood itself. This article explains what job schedulers generally do.

Your shop needs a sales report every morning at 6:00. You already have a program that reads yesterday’s orders and writes the report. Someone still has to start it every morning. A job scheduler takes care of starting work when it’s due.

The work you want done is called a **job**. In this case, the job is generating the sales report. Its **schedule** is the rule that says when it’s due. You set that rule to 6:00 every morning. The report program contains the instructions for making the report, and the schedule can change without any change to those instructions.

At 6:00, a scheduler would see that the report job is due and arrange for the report program to run. That one attempt is called a **run**. Monday’s report and Tuesday’s report are separate runs of the same job, each with its own outcome.

The distinction matters when something goes wrong. Suppose the program starts at 6:00 on Monday but can’t open yesterday’s orders. The job was due, the program started, and the report was never written. Those are three different facts. When you check what happened, look for the outcome of Monday’s run. The schedule tells you when the report was due. The run’s outcome tells you whether the program reported success or failure, if the scheduler records that information.

A missed start is a different problem. If the scheduler is off at 6:00 and comes back at 6:20, there may be no Monday run to check. Some schedulers start missed jobs when they come back. Others wait until the next scheduled time. Both can use the same daily schedule, so knowing the job is due at 6:00 tells you little about what happens after an outage.

There’s one more time to pay attention to. If the report usually takes two minutes, a run that starts at 6:00 will usually produce a report around 6:02. If the shop needs the report ready at 6:00, when to start it depends on how long the work takes. That’s the practical difference between scheduling a run and setting a deadline.

## Going further

- How do you register a job in Driftwood and set it to run every day at 6:00?
- Which time zone does Driftwood use to decide when it’s 6:00?
- What happens if Driftwood is stopped when a job is due?
- Where can you check whether a particular run started and how it ended?