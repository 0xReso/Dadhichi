# Head gate review: built/explain.commuter.it.md v0.2.2

Note: this review ran on Opus (claude-opus-5-5) because the usual head model was out of credits. The head role's independence from the builder and output models still holds, but verdicts may not calibrate exactly with earlier head files.

Date: 2026-11-18. Stage: gate review before testing.
Read: design doc, v0.2.2 and v0.2.1 frozen prompts, both v0.2.1 head gradings, failures.md, rubric.md, inputs.md.

## Verdict: REVISE

All seven edits are applied verbatim and nothing else in the prompt changed. The problems are at the seams: three pieces of untouched text (the output section, the self-check, step 9's closing line) still use the old wording, and two of them sit right where the new rubric checks 6 and 12 will be graded. The owner wants the prompt to work in one shot, so I want these fixed before the run. Each one is a one-line change.

## 1. Were the edits applied correctly?

I compared v0.2.1 and v0.2.2 line by line.

| Edit | Location | Applied verbatim | Notes |
| --- | --- | --- | --- |
| v0.2.1 grading, edit 1 (simple criterion) | plan step 9 | Yes | Old "A simple concept, such as what a port number is, gets about 450 words and no chapters, never more than 600." fully replaced |
| edit 2 (size-aware body test) | plan step 5 | Yes | |
| edit 3 (unknown tool) | plan step 1 | Yes | |
| edit 4 (sections for moderate) | write, chapter paragraph | Yes | Rest of the paragraph unchanged |
| edit 5 (pace in self-check) | check, second line | Yes | |
| Alexa edit 1 (source confidence) | source paragraph, now three paragraphs | Yes | |
| Alexa edit 2 (traceability) | check, last line | Yes | |

Other changes: version 0.2.1 to 0.2.2 and the frontmatter status comment. Situation, goal, plan steps 2 to 4 and 6 to 8, the rest of the write section, domain, the other check lines and the whole output section are byte-identical to v0.2.1. The failure-log lines are recorded as "0.2.2 (edit applied, not yet tested)", which is the right status.

Version bump: these edits change planning logic (the size criterion) and output shape (sections for moderate pieces, a new unknown-tool shape). By the design's table that is at least a minor bump (0.3.0), not a patch. This does not affect the test run. I list it for the builder; it is not one of the five edits.

## 2. Conflicts between edits and untouched text

C1. Unknown-tool statement and the output section (affects check 12, input 4). Step 1 now says to state in "the first two sentences" that the tool is unknown. The untouched output section still says the article opens with "One line under the title saying what the reader will understand by the end", and still says "Leave out ... any notes to the person who sent this". The v0.2.1 grading named that leave-out line as one cause of the soft admission, and it is still there. A model following the output section will most likely write a hopeful subtitle ("What a Rust job scheduler does, and what to ask about Driftwood"), then a setup sentence, then the admission as sentence three. Under rubric check 12 that is a Fail. Whether the subtitle counts as a "sentence" is also unclear, so the grader could go either way. The fix is to say in the output section where the admission goes and that it is written to the reader (edit 1).

C2. Sections in the write section, "chapters" in the self-check (affects check 6, inputs 2, 4, 5, 7, 9). Edit 4 fixes the write section. But the self-check, which the model applies last, still says "Each chapter, if there are chapters, can be picked up cold from its opening lines" and "No chapter ends with a summary of itself". Step 9 says only deep topics are "split into chapters", so a model reviewing a moderate piece can read "if there are chapters" as "not this piece" and skip the reminder check. That is the same gap that caused the Kafka and Driftwood check-6 failures, now moved from the write section to the check (edit 2).

C3. Tier names and headings in step 9 against the output section (affects input 1). Step 9 now says a simple piece has "no headings". The output section still describes the body as "continuous prose for a short piece, or chapters under '##' headings for a longer one" and allows "a final section titled 'Going further'". So the prompt describes three tiers in one place and two in another, uses short/long in one place and simple/moderate/deep in the other, and does not say whether the "Going further" title in a simple piece breaks "no headings". The likely result is either a dropped "Going further" or a "## Going further" that a grader may count against the input-1 stress "no chapters". The risk is low but it costs one line to remove, and input 1 is the input that blocked promotion last time (edit 4).

C4. Pace rule against the simple-tier clause rule. Step 9 says the ideas around a simple topic "get one clause each". The new check line says "No paragraph hands the reader more than one new term ... give each term its own paragraph". If those clauses name terms (hashing, HTTPS), the check pushes each one into its own paragraph and the 450-word piece grows. The tail of the same check line ("drop any name the piece never uses again") mostly settles this, because clause-level ideas are usually named once. I am not proposing an edit. Watch input 1 for one-sentence paragraphs and for growth past 600.

C5. Pace rule against rubric 11b. The prompt says at most one new term per paragraph. 11b allows two "when they are a pair defined against each other", and the domain block's confused pairs (authentication and authorization) are exactly the case where defining the two together helps. The prompt is the stricter of the two, so this cannot cause an 11b Fail. It can make pair explanations choppier. No edit; watch for it.

C6. Source-handling text outside the seven sections. The three source paragraphs sit above `<situation>`, outside the seven-section shape, and the longest of them is instructions rather than source. v0.2.1 already did this with one sentence, and the design puts source material above the instructions. It is not a first-run risk. I record it for a later structural pass. No edit.

## 3. Likely over-corrections and first-run risks

R1. Input 7 has a pass condition the prompt never states. inputs.md now caps input 7 at 1,700 words. The NOTES for input 7 set no length, and step 9 sizes the budget from the topic alone. Docker stays moderate (about 1,500, at most 2,200), and edit 4's three to five sections push toward the middle of that range. The last run was 2,144. Nothing in v0.2.2 tells the model that a reader who already holds the foundations should get a shorter piece, so I expect another miss (edit 3).

R2. Hedging creep on input 9. The new source paragraph asks the model to "say where they come from in the source's own terms" and to word additions "as general practice". Without saying how often, this tends to produce a string of "reportedly" and "according to the pack" on every line, which also adds words. The last Alexa output was already at 1,982 of 2,200, and edit 4 adds section-opening reminders. The Alexa grading already drafted the guard sentence; add it now rather than after a failed run (edit 5).

R3. Edit 1 could misclassify the API key in the other direction. "No chain of several stages or several machines" could be read as excluding the API key, since it involves an app and a server. The examples (port number, checksum) and edit 2's "the mechanism is a single exchange" should keep it simple. No edit. If input 1 again produces "The whole picture", this criterion is the cause.

R4. Input 5 (the cloud) could be pulled down to simple. The v0.2.1 grading already flagged this. It should stay moderate. No edit; watch for it.

R5. Rubric, outside the prompt. Check 6 now covers "anything under a '##' heading after the first". Read literally, that includes "The whole picture" and "Going further", which are not meant to open with a reminder. Add "excluding 'The whole picture' and 'Going further'" to the rubric so the grader does not mark a correct output down. Edit 2 below uses the same exclusion so prompt and rubric agree.

## Edits, in order of importance

Edit 1. Put the unknown-tool admission in the line under the title, and say it is not a note to the sender (output section). Fixes C1, protects check 12.

Replace:
> One line under the title saying what the reader will understand by the end.

With:
> One line under the title saying what the reader will understand by the end. If the topic is a named tool you have no reliable knowledge of, this line says that plainly instead, because it is the first thing the reader meets under the tool's name. That statement is written to the reader and is part of the article, not a note to the person who sent this.

Edit 2. Make the self-check cover sections as well as chapters (check section). Fixes C2, protects check 6.

Replace:
> No chapter ends with a summary of itself.

With:
> No section or chapter ends with a summary of itself.

And replace:
> Each chapter, if there are chapters, can be picked up cold from its opening lines.

With:
> Every "##" section or chapter after the first, apart from "The whole picture" and "Going further", opens with a sentence or two on what the reader now holds, so it can be picked up cold.

Edit 3. Let a reader note shrink the budget (plan step 9, closing lines). Fixes R1, input 7.

Replace:
> Long source material does not make the piece long; it means there is more to cut. If the notes above set a length, follow them instead.

With:
> Long source material does not make the piece long; it means there is more to cut. When the notes say the reader already holds some of what the topic rests on, take the words those passages would have needed off the budget rather than spending them elsewhere, because a reader who knows the ground wants to reach the new part sooner. If the notes above set a length, follow them instead.

Edit 4. Use the same tier names and heading rule in step 9 and the output section. Fixes C3, input 1.

In plan step 9, replace:
> written as continuous prose with no headings and no "The whole picture" section.

With:
> written as continuous prose with no headings other than an optional "Going further" at the end, and no "The whole picture" section.

In the output section, replace:
> The body: continuous prose for a short piece, or chapters under "##" headings for a longer one.
> For moderate and long pieces, a closing section titled "The whole picture":

With:
> The body: continuous prose for a simple topic; three to five sections under "##" headings for a moderate one; chapters under "##" headings for a deep one.
> For moderate and deep pieces, a closing section titled "The whole picture":

Edit 5. Say confidence once, where it changes (source paragraph). Fixes R2, input 9.

Replace:
> Present unconfirmed parts as what the source says they are, and say where they come from in the source's own terms.

With:
> Present unconfirmed parts as what the source says they are, and say where they come from in the source's own terms. Say it once, at the point where the confidence changes, not on every sentence, so the confirmed parts still read as plain statements.

## What to look at first in the test run

1. Input 4: whether the line under the title is the admission, and whether anything in the body or "Going further" is attributed to Driftwood.
2. Input 1: word count (at most 600), no "The whole picture", and no one-sentence paragraph chains caused by the pace rule (C4).
3. Inputs 2 and 7: three to five sections, each after the first opening with a reminder; input 7 at most 1,700 words.
4. Input 9: check 13, with M1 to M5 from the Alexa grading as the specific sentences to look for, and no line-by-line hedging.
5. Input 3: whether the pace rule pushes Raft past 4,500.

Run input 1 at least three times, as the v0.2.1 grading asked, because the last promotion was blocked by one sample.
