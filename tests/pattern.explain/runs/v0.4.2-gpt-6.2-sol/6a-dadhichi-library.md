# How the Dadhichi prompt library works

You’ll understand how Dadhichi turns a rough request into a reusable prompt and how it decides whether a revision earns its place in the library.

## From a request to a prompt

Suppose you want a model to explain bond duration to someone reading on a Kindle during a commute. You could ask for a clear explanation, but the model would have to guess what the reader already knows, how much detail they need, and whether they can look up an unfamiliar term. Those guesses can change from one answer to the next.

A prompt is the set of instructions you give the model. In this case, it needs to say what the reader should be able to explain afterward and what would make the answer usable on the commute. It also needs to carry that context when pasted into a new conversation, where the model has no access to the discussion that produced it.

Dadhichi is designed as a library of reusable prompt parts, with a procedure for putting them together. The design starts from a practical question. If you already have instructions for explaining a technical concept to a commuter, how much of that work should you have to do again to explain a finance concept?

## The parts that make up a prompt

The bond-duration request gives Dadhichi a job, a reader, and a subject. Each can change independently, so the library gives each its own place.

The instructions for doing a recurring job form a **task pattern**. The Explain pattern aims to make one concept understandable in a single read. It gives the model a way to decide which ideas the reader needs first, which can be explained as they arise, and which can be left out. Those decisions apply whether the concept comes from finance or another field.

The instructions that describe who will read the result form a **reader profile**. The commuter profile describes someone reading in short stretches with no browser open. That setting gives the model a reason to define terms as they appear and to arrange the explanation so the reader can pick up the thread after a stop.

The vocabulary and conventions of a field go in a **domain pack**. The finance pack supplies the subject knowledge relevant to the bond-duration request. If the next request asks for a different finance concept for the same commuter, the model can draw on the same pack. If the request moves to another field, the Explain pattern and commuter profile can carry over.

A specific adjustment can come from a **modifier**. If you ask for the bond-duration explanation in Hindi, a language modifier can supply that instruction without requiring a separate version of the Explain pattern.

The rules shared across the library are called the **kernel**. One is to plan silently before writing. For the bond-duration piece, that means identifying the ideas the reader needs, putting them in an order that makes sense, and deciding how much space each deserves before drafting the article.

The design sets an order for resolving conflicts. The kernel takes priority. After that come the user’s request, the modifiers, the reader profile, and the task pattern’s defaults, in that order. If you specify a length and a modifier supplies a different one, your requested length governs. How does Dadhichi turn these parts into instructions that another model can use?

## How the engine assembles the prompt

The bond-duration request now has a job, a reader, and a field. The **engine** is itself a prompt. Its job is to turn those choices into a complete set of instructions for the model that will write the explanation.

It first classifies the request as Explain, commuter, and finance. It then asks whether any missing information would materially change the prompt and cannot reasonably be inferred. The Kindle setting is already clear in this request, so there is no need to ask about it. If an important detail is missing, the engine can ask up to three short questions and pause for the answers.

The engine then assembles seven sections in a fixed order. It starts with the reader’s **situation**, which gives the model the circumstances it should write for.

The **goal** states what the reader should be able to do afterward. For this request, the reader should be able to explain what bond duration means and why it matters.

The **plan** tells the model how to prepare privately before writing. It decides which ideas the explanation depends on and puts them in the order the reader needs them.

The **write** section gives the instructions for drafting the piece. It can tell the model to explain each term when the reader first needs it, since the reader has no way to look it up.

The **domain** section supplies the finance knowledge needed for the task.

The **check** section tells the model to review its own draft before answering. For the commuter, one check is to catch any term the draft uses before explaining it.

The **output** section says exactly what to return. Here, that could be a plain-text article that reads cleanly on a Kindle.

Before handing over the assembled prompt, the engine reads it as a colleague would, with no knowledge of the original conversation. It fixes gaps and conflicts, then returns the prompt with two likely ways its output could fall short and an input that could expose each one. At that point you have a prompt you can try. What would earn it the label *tested*?

## How a prompt earns its place

The assembled prompt can ask the writing model to check its own draft. Dadhichi’s quality process goes further by running the prompt on several inputs and assessing what it actually produces.

The design calls for an initial set of six to ten inputs per task pattern. Bond duration gives the Explain pattern a case from finance. The set also needs an easy topic to see whether the prompt stays brief, a hard topic to see whether it stays clear, a vague request to see how it handles missing detail, and a topic outside the model’s likely knowledge to see whether it acknowledges its limits.

The outputs are judged against a **rubric**, a list of checks with yes-or-no pass conditions. For the bond-duration article, a grader can ask whether every term is introduced by its first use, whether any sentence depends on an explanation that comes later, and whether the article is technically accurate. The design calls for a different model to grade the output and a human reading check for the two failures that matter most to the commuter. Read the article on a phone away from a desk and count the times you have to stop because a term or step is missing.

Suppose that check exposes a gap and you revise the Explain pattern. Dadhichi’s rule is to run both versions on the full set and grade them with the same rubric. The revision takes over only if it passes more checks and preserves every pass the old version earned. Fixing the bond-duration article would therefore be insufficient if the revision caused an easy topic to fail its length check.

The library records the model and date used for verification. That matters because a wording choice that works well with one model can behave differently with another. The source describes a roadmap that starts by testing the explainer and then checks whether it still works when the reader profile and domain pack change. The bond-duration case illustrates that design.

## The whole picture

Dadhichi turns “explain bond duration for a Kindle commute” into a prompt by combining instructions for the job, the reader’s situation, and the subject. The engine puts those instructions into a form a model can follow in a fresh conversation. The tests then ask whether the resulting article delivers what the prompt promised and whether a revision keeps delivering it across the rest of the cases. That is what makes the Explain pattern reusable across subjects while giving each revision a standard it has to meet.