# How the Dadhichi prompt library works

You’ll understand how Dadhichi turns a rough request into a reusable prompt and how it checks whether a revised prompt earns its place in the library.

## The problem with saving whole prompts

You want an explanation of how a group of programs shares the work of reading a stream of events. You’ll read it on your phone on the train, so it needs to introduce each term before you have to use it. You could write a prompt for that job and save it. Then you could write another for a finance topic, or another for a colleague who needs the same technical explanation before a meeting. Soon you’d have several prompts that share most of their instructions. Fixing a weakness in one would leave you deciding which of the others need the same fix.

Dadhichi is a design for a prompt library that stores reusable instructions in separate parts. A prompt in this design is a specification. It says what the model receives, what it should produce, what constraints matter, and how to tell whether the result works.

The design lays out a build and testing roadmap. The train example below uses the proposed workflow. It illustrates how the parts fit together without assuming the tests have already run.

Which instructions would you keep when the topic changes?

## What the library reuses

The train reader needs an explanation that makes sense from top to bottom. Some instructions that help that reader also belong in prompts for other jobs. Dadhichi puts rules shared across the library in a **kernel**. One example is asking the model to plan privately before writing, so it can decide what the reader needs first and where a short explanation will do.

The instructions for explaining one concept belong in a **task pattern**. The Explain pattern gives the model a job with a finish line. It should leave the reader able to say what the concept does and how it works. That job carries over when you switch from event processing to finance.

The constraints of reading on a train belong in a **reader profile**. The Commuter profile describes someone who reads in order and cannot look up an unfamiliar term. Giving the model that situation helps it make decisions the prompt writer hasn’t listed, such as whether a sentence introduces too much at once.

The vocabulary and conventions of a field belong in a **domain pack**. The information technology pack supplies background that helps the model use the terms a practitioner would recognise. It can change when the subject changes while the Explain pattern still gives the model the same job.

A small adjustment belongs in a **modifier**. If you need a fixed length, you can apply a length cap to this request without editing the Commuter profile for every other reader. The design puts an explicit user request ahead of a modifier, a modifier ahead of the reader profile, and the profile ahead of the pattern’s defaults. The kernel applies throughout.

How does a rough request become a prompt you can hand to another model?

## From request to finished prompt

The library now has a place for the job, the reader’s circumstances, the field, and any small adjustment. The **engine** is itself a prompt. Its job is to turn your rough request into instructions for a model that will see none of the conversation that produced them.

Suppose you ask, “Explain Kafka consumer groups for my train ride. I know what an app is, but I don’t know how apps share the work of reading incoming events.” Kafka is the system in this example that makes a stream of events available for programs to read. A consumer group is a set of readers that share that work. The engine classifies the request as Explain for a Commuter in information technology. If a missing detail would change the resulting prompt and the engine can’t reasonably infer it, it asks up to three short questions and waits. Here, the request gives it enough to proceed.

The engine assembles the prompt in seven named sections. It starts with the reader’s situation and the goal. It then tells the model how to plan privately and how to write. It supplies the field knowledge, a check to apply before answering, and an exact description of what to return. The finished prompt carries the context forward, including what you already know and why an unexplained term would break the thread on the train.

Before returning the prompt, the engine applies the **colleague test**. Someone reading the prompt cold should be able to follow it without guessing what was meant. The engine also names two ways the resulting answer could fall short and gives a test input for each. Those inputs are starting points for testing the prompt.

How would you tell whether changing that prompt actually improves the explanation?

## What earns a new version

The engine has produced a prompt you can hand to another model and two places to start looking for trouble. To test the prompt, you run it on a set of inputs and score the answers. The design calls for a set that includes an easy case, a hard case, a vague case, a case outside the model’s likely knowledge, and a case from another field. A strong answer about Kafka consumer groups tells you how the prompt did on that input. The other cases show how well the instructions carry over.

A **rubric** is the list of yes-or-no checks used to score each answer. For the train explanation, one check asks whether every term is introduced by the time the reader meets it. Another asks whether any sentence depends on something explained later. The design also calls for a human check on those two points. Read the output on a phone away from a desk and count the pauses. An answer can look clear to someone who already knows the topic and still leave a first-time reader stuck.

Suppose the first version uses “consumer group” before it explains what the readers share. You record the input, the failed check, and the suspected cause in the pattern’s **failure log**. You revise the prompt and run both versions on the same full test set. Under the design’s promotion rule, the revision must pass more checks overall and preserve every check the previous version passed. Fixing the Kafka explanation still leaves the question of whether the revision made an easy explanation too long or a difficult one harder to follow.

Each tested entry records which model ran the tests and when. That record matters because the same wording can behave differently on a newer model. When the model changes, the design calls for running the tests again before relying on the old result.

## The whole picture

Dadhichi gives the instructions that recur across prompts a place of their own. For the train explanation, the engine combines the shared rules, the Explain pattern, the Commuter profile, and the field knowledge into a prompt that can travel on its own. The engine’s review checks whether someone can follow those instructions cold. The test set checks what happens when a model follows them, and the version comparison determines whether a change has earned its place in the library.