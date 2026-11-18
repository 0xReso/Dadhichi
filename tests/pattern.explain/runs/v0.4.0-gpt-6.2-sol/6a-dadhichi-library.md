# How the Dadhichi prompt library works

You’ll understand how Dadhichi turns a rough request into a reusable prompt and how it decides whether a revised prompt is ready to use.

## The problem with saving whole prompts

Suppose you have a prompt that explains Kafka consumer groups, a way for several programs to share the work of reading a stream of events. It gives you an explanation you can follow on your phone without looking anything up. Now you want the same kind of explanation of bond duration, a measure of how sensitive a bond’s price is to changes in interest rates. You could copy the prompt and edit it. After enough copies, though, even a small improvement to the instructions for phone reading has to be made in several places.

Dadhichi’s design starts by treating a prompt as a specification. A specification says what goes in, what should come out, and how to tell whether the result meets the requirements. For your explanation, the input is the topic, the output is an article that works in one read, and one requirement is that each unfamiliar term be explained by the time you meet it.

Once you know what the prompt has to accomplish, which instructions can you reuse when the subject changes?

## The parts that go into a prompt

Your two explanations have the same job. Dadhichi stores the instructions for that job in a **task pattern**. The Explain pattern tells the model to work out what the reader needs to understand, then put those ideas in the order the reader needs them. Those instructions apply to both topics.

The conditions under which you read go in a **reader profile**. The commuter profile describes someone reading in short stretches, with no practical way to look up a term. The assembled prompt carries that situation with it. When the model has to decide whether a word needs explaining, it knows what a missed definition would cost you.

Knowledge specific to the subject goes in a **domain pack**. The technology pack supplies vocabulary and common points of confusion from that field. For the bond duration request, the design calls for swapping in the finance pack while keeping the Explain pattern and commuter profile.

A **modifier** makes a narrow adjustment, such as setting a length cap. If you need the bond duration piece to fit within 500 words, you can add that limit for this request.

Under those parts sits the **kernel**, the shared rules that apply to every prompt. One is to plan silently before writing. If instructions conflict, the design puts the kernel first, then your request, then any modifiers, then the reader profile, then the pattern’s defaults.

How does a request in your own words become something another model can follow?

## From a rough request to a finished prompt

The parts hold the job, the reader’s situation, the subject knowledge, and any narrow adjustment. Dadhichi’s **engine** is itself a prompt that tells a model how to choose those parts and assemble them into instructions for another model.

Take “Explain bond duration so I can read it on my phone on the train.” The engine classifies the request as Explain, commuter, and finance. It asks up to three short questions if an answer would change the prompt and the engine cannot reasonably infer it. If the request is clear enough, it proceeds and states any assumptions it made.

The engine puts the instructions into seven sections. The situation describes the reader, and the goal says what the reader should understand by the end. The plan tells the model what to work out privately before writing. The writing instructions guide the article, the domain section supplies field knowledge, the check tells the model what to review, and the output section specifies exactly what to return. If the library lacks a needed part, the engine can draft it and flag it as new.

The engine then reads the assembled prompt as if it had never seen your request. “Explain this for the same reader” would fail that check. The prompt has to name bond duration and describe your reading situation because the model that receives it may see only the prompt. The engine returns the prompt along with two likely ways it could fail and a test input for each.

What would show that the finished prompt reliably produces the kind of explanation you asked for?

## How a prompt earns its place

The engine’s two test inputs give you somewhere to start. Dadhichi’s design calls for a broader set for each pattern, including an easy topic, a hard one, a vague request, a topic outside the model’s likely knowledge, and a case from a second field. Bond duration can serve as that second-field case when the other examples come from technology.

Each answer is scored against a **rubric**, a set of checks with yes-or-no results. For Explain, one check asks whether every unfamiliar term is introduced before or at its first use. Another asks whether every sentence makes sense using only what appeared earlier. Even if the bond duration article gets the finance right, it fails the second check if you have to read ahead to understand a sentence. The design also calls for a human to try reading on a phone away from a desk, where those pauses are easier to notice.

To evaluate a revision, you run the old and new versions on the same inputs. The new version replaces the old one only if it passes more checks and keeps every pass the old version earned. If adding finance guidance helps the bond duration answer but makes the Kafka answer harder to follow, the revision stays out. Each tested entry records the model and date of verification so you know which model actually passed.

The design document sets out this process and lists the explainer and the finance swap as roadmap steps. It gives no test results for either.

## The whole picture

Dadhichi’s design gives you a way to change the subject of a prompt while keeping the instructions that make it work for a particular reader. The engine turns your request into a prompt that can travel on its own. The tests then give you a way to check whether that reuse worked: a change earns its place by improving the answers while preserving the behavior you already relied on.