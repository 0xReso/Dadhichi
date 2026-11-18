# How the Dadhichi prompt library works

You’ll see how Dadhichi assembles a prompt from reusable parts and tests whether it is ready to rely on.

## What makes a prompt worth keeping?

Suppose you want an explanation of Kafka consumer groups that you can read on a train. A Kafka consumer group is a set of programs that divide up the work of reading a stream of records. You want to understand how that division works in one pass, with every unfamiliar term explained on the page. If you later want a different concept explained on the same journey, much of what made the first prompt useful still applies.

Dadhichi is designed around that repeatable work. A prompt is the set of instructions a language model receives. Dadhichi treats it as a specification: it says what you supply, what the model should return, what constraints it should follow, and how you can judge the answer. “Explain Kafka consumer groups” names the subject. The specification also says who will read the explanation and what they should understand by the end.

That distinction matters when you save a prompt. A copy can preserve instructions that worked once, but it can also tie the subject, the reader, and the writing approach together. Dadhichi gives each of those decisions a place of its own. Which parts of the train-reading request belong in separate files?

## The parts that make up a prompt

The train-reading request already tells you two things: the job is to explain one concept, and the explanation has to stand on its own. Dadhichi starts with shared instructions that apply across jobs. This shared base is called the **kernel**. For example, the model should plan before writing and introduce terms by the time the reader meets them.

The instructions for a particular job form a **task pattern**. The Explain pattern aims to make a concept understandable in one linear read. It tells the model to decide which ideas the reader needs first, which can be explained in passing, and which can be left out. Those decisions apply to an explanation of Kafka consumer groups or to a concept from another field.

The audience’s circumstances belong in a **reader profile**. The Commuter profile describes someone who reads from top to bottom, may stop midway, and cannot look anything up. That gives the model a reason to define unfamiliar terms as they appear and to make each major section easy to resume.

The field’s vocabulary, conventions, and common pitfalls belong in a **domain pack**. For the Kafka request, the information technology pack supplies field knowledge. The Explain pattern supplies the instructions for turning that knowledge into an explanation. The design keeps those responsibilities in separate files so that the same pattern can serve another field.

A **modifier** is a small adjustment, such as a length limit or a language choice. When instructions conflict, the kernel holds. Among the other instructions, the user’s request takes priority over a modifier, a modifier over the reader profile, and the reader profile over the pattern’s defaults. How do those pieces become a prompt you can paste into a fresh conversation?

## From a rough request to a finished prompt

The Kafka request now has an Explain pattern, a Commuter profile, and an information technology domain pack. The **engine** is itself a prompt. It instructs a model to identify those parts from a rough request and assemble them into instructions another model can follow on its own.

The engine first identifies the job, the reader, and the field. It can ask up to three short questions if an answer would materially change the prompt and cannot reasonably be inferred. Here, “Explain Kafka consumer groups so I can read it on the train without looking anything up” already gives it enough to proceed. When a needed library part is missing, the engine can write one and flag it as new.

The assembled prompt starts by describing the reader’s situation and what the reader should be able to understand afterward. It gives the model a private planning step, followed by writing instructions and field knowledge. It ends by telling the model what to check before answering and exactly what to return. The model receiving that prompt has the context it needs on the page.

Before handing over the prompt, the engine reads it as a colleague would, with only the context in the prompt itself. It also names two likely ways the answer could fall short and gives a test input for each. For instance, a test could ask about the division of work when one program stops. An answer would expose a problem if it relied on a new technical term without explaining it. What would it take to mark the prompt as tested?

## How a prompt earns its place

The engine’s two suggested cases give you somewhere to start. Dadhichi’s quality system calls for a broader, fixed set of inputs for each pattern. The Explain pattern should face an easy topic, a hard one, a vague request, a topic outside the model’s likely knowledge, and a topic from another field. Each case probes a different way the instructions might fail.

The outputs are scored against a **rubric**, a list of checks with yes-or-no answers. For Explain, the checks include whether every term is introduced by first use, whether each sentence depends only on what came before, and whether the length fits the difficulty. The design calls for a different model to grade the answers. It also calls for a human to read them on a phone away from a desk, because a grader can miss the moment an unexplained term makes a reader pause.

A prompt can look ready to paste while its library status is still `draft`. To mark it `tested`, the design requires a run against the written checks. To replace a released version, the new version has to pass more checks on the same inputs without losing any check the previous version passed. Each entry records the model and date of verification, and a failure log records what broke and which version addressed it.

The design’s roadmap proposes Kafka consumer groups as one of three topics for the first explainer trial. The material behind this article describes the trial and its pass criteria. It does not give results for that trial.

## The whole picture

Dadhichi’s design makes a prompt reusable by giving the job, the reader’s circumstances, and the field knowledge separate homes. In the train-reading example, the engine brings those parts together into a prompt that another model can follow from a fresh conversation. The quality system then asks whether the resulting explanation actually works for that reader, using fixed inputs and checks that let you judge the next version on the same terms.