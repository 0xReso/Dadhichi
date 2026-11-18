# Driftwood, the Rust job scheduler

I have no reliable knowledge of Driftwood. This article explains job scheduling in general.

Suppose you run an online shop and want a sales report ready each morning. Someone could open the shop’s admin page at 6 a.m. and generate it by hand. A program can do the work instead. Rust is a programming language you can use to write programs like that.

Generating the report is a unit of work the shop wants done. In scheduling, that unit is called a **job**. The job contains or points to the instructions for gathering yesterday’s sales and saving the report.

The shop also needs a rule for when to start the job. “Every day at 6 a.m. in the shop’s time zone” is its **schedule**. The shop can move report generation to 7 a.m. by changing the schedule while keeping the same job.

A **job scheduler** uses that rule to decide when a run is due. In a typical setup, the scheduler reaches 6 a.m. and starts the job or hands it to another program that runs it. The job then reads the sales records and saves the report.

The common mistake is to treat 6 a.m. as the time the report will be ready. It’s the time the job is due to start. If the run starts at 6 a.m. and takes four minutes, the report is ready at 6:04. If the job cannot read the sales records, the scheduled time can pass without a report. A record of when the job started and how it finished tells the shop what happened that morning.

## Going further

- How do you tell Driftwood what work to run?
- How do you set a daily schedule and choose its time zone?
- What happens if Driftwood is stopped when a job is due?
- How can you tell whether a run finished successfully?