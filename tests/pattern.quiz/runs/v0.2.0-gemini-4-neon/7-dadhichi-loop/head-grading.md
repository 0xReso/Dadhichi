# Head review · Input 7, The Dadhichi round protocol

**v0.2.0 · gemini-4-neon · low depth · sheet mode.** 8 Pass, 0 Borderline, 7 Fail. Check 15 is inapplicable. The highest-priority repair is to derive each complete answer from the supplied protocol before writing the options. Q12 teaches that a Mac round may end immediately after a commit. The runner handles the push, but every round still needs a terminal status line.

The source embedded in the filled prompt matches `loop/LOOP.md` after trimming outer whitespace. Source line numbers below refer to that file. No earlier-version Input 7 output exists in the local runs for a matched comparison. This sample supplies no basis for promotion.

## Independent answer and determinacy audit · Checks 2 and 3

I applied the protocol to each stem, then compared the result with the key. “Yes” means the stated outcome follows for the supplied case. A trace or general rule can still introduce an unsupported claim. Status names in this table abbreviate the literal lines prefixed with `DADHICHI-STATUS: `.

| Q# | Independent result | Stated result | Agree? |
| --- | --- | --- | --- |
| 1 | The state names unfinished test set B for pattern-a. Resume it (L10). | Run test set B for pattern-a. | Yes |
| 2 | Freeze the exact prompt before the run. Give fresh general-purpose writers only the filled prompt (L16, L18). | (a), freeze first and isolate the writers. | Yes |
| 3 | Even visibly deficient outputs go to the different-model head with input and destination paths (L17). | (b), have the head write the grade. | Yes |
| 4 | Four passes beat two, but C2 went from pass to fail. Promotion is barred (L19). | No, C2. | Yes |
| 5 | Stage and commit locally. Command 3 is the runner’s responsibility (L22, L28). | 3, git push. | Yes |
| 6 | Item 3 remains open and no human intervention is needed. End with CONTINUE (L30–33). | CONTINUE. | Yes |
| 7 | Choose a format, record why and proceed (L1). The handoff includes decisions for user review (L27). | (b), choose, document and continue working. | Yes, (b) is the appropriate action. |
| 8 | The four reading stages are state, backlog, design, then changelog and touched files together (L3–7). | E, C, B, (A, D). | Yes |
| 9 | The active parent began open and still has work. Mark only its finished child complete (L11, L26). | (b), parent open, children complete/open/open. | Yes on the stated active work. |
| 10 | Three new failures add three lines to the existing two (L20). Total five. | Five lines. | Yes |
| 11 | A released typo needs a new version. The head must verify improvement with no lost pass before promotion (L19). | (b), new version and promotion gate. | Yes |
| 12 | Cloud owes a branch push and a final status line. Mac owes the status line. The transcript gives no end-of-round work state from which to select its value (L22, L30–33). | Cloud owes the push. On Mac “nothing is missing”. | **No**, both endings omit a required action. |
| 13 | With no unfinished step, skip items 1–3 and select the first open item, 4 (L10–11). | Item 4, write tests for pattern-d. | Yes |
| 14 | Input 2 invents a quote. Input 3 uses a real customer’s private details (L21). | Inputs 2 and 3 for those reasons. | Yes |
| 15 | Step 3 adds coaching to the filled prompt, which violates the writer-input restriction (L16). | Step 3, builder hint. | Yes |
| 16 | No unfinished work, open item or blocker remains. End with IDLE (L10–11, L30–33). | IDLE. | Yes |
| 17 | Appending violates L27. The stale instruction can cause a repeated run under L10. Which instruction a reader will follow in a malformed handoff is unspecified. | (a), Round 5 **can** repeat test set A. | Yes as a possible consequence, as option (a) says. |
| 18 | A tie at three passes fails the strict increase condition regardless of shorter prose (L19). | No, the counts tie. | Yes |
| 19 | Installing software (2) and changing user settings (3) violate L22. | Actions 2 and 3. | Yes |
| 20 | Supply paths for the material and the review destination so the head judges it (L17). | (a), relevant paths and destination. | Yes |
| 21 | The decision to wait alone triggers a dated changelog entry (L25). The stem establishes a grading request. | Yes, a decision was made and the key says grading finished. | Yes on the outcome, unsupported trace. |
| 22 | Grading remains. Keep item 2 open and emit CONTINUE because there is no blocker (L26, L30–33). | Open and CONTINUE. | Yes |
| 23 | Editing the release violates L19. Editing the saved run prompt destroys the exact snapshot required by L18. | Release immutability and frozen snapshot. | Yes |
| 24 | The head grades. C3 regressed. Each failure needs a line (L17, L19–20). All three proposals are barred. | No, no, no. | Yes |
| 25 | X must choose and carry on. It can later end IDLE if the last item finishes, or CONTINUE if work remains. Y has one open item and a stated human-only blocker, so end BLOCKED with its reason (L1, L30–33). | (a), X must emit CONTINUE, Y BLOCKED. | **No**, X has no unique final status. |
| 26 | Among the five supplied steps, update the changelog and state, commit, push to the cloud session branch, then emit CONTINUE (L22, L25–33). | C, B, D, A, E. | Yes |
| 27 | The handoff identifies the run. The head writes the grade. Closing the sole open item cleanly yields IDLE (L4, L10, L17, L30–33). | STATE.md, dadhichi-head, IDLE. | Yes |
| 28 | Private review, invented statistic and missing snapshot are certain (L18, L21). If the described live path is all the writer gets, it also lacks the required filled prompt (L16). | Exactly three violations, ending with the missing frozen copy. | **Conditional**, all three are real, but the handoff can violate a fourth rule. |
| 29 | A meets the gate. Promotion is allowed, its occurrence unspecified. No new failure, changelog yes. B cannot be promoted, must log C3 and must update the changelog (L19–20, L25). | A yes/no/yes. B no/yes/yes. | **No**, A’s first “Yes” is a possible decision, not an entailed result. |
| 30 | Log two lines, tick item 3 complete, push to the cloud session branch and end IDLE (L11, L20, L22, L26, L30–33). | Two, complete, yes, IDLE. | Yes |

## Rubric findings

1. **Count.** Python found the consecutive question and answer numbers 1 through 30 with no gaps or duplicates. Low depth requires 30. **Pass.**

2. **Correct.** Q12 says the agent commits “and ends its turn.” Its key says “On a local Mac with the runner script, nothing is missing because the runner handles `git push`.” L30 requires a final status in both environments. Q25 and Q29 also assert outcomes the protocol leaves open. Any one wrong answer suffices. **Fail.**

3. **Determinate.** Q25 asks “Which status lines must end Situation X and Situation Y?” X describes a choice midway through drafting and gives no final backlog. Both a clean finish with open work and a clean finish with no open work fit. Q29 asks “is `v1.1` promoted” when the source specifies only when it *may* be promoted. Two decisions satisfy Case A. Q28’s “Passes the live path patterns/pattern-e/v0.1.md directly to fresh subagents” leaves unclear whether they also receive a filled prompt. The requested list of “all three” changes on the path-only reading. The first two cases alone reach the Fail threshold. **Fail.**

4. **Assumptions.** The opening identifies the supplied source, the default local Mac session with runner, and how to treat the three backlog markers. The cloud overrides are explicit. Q25 lacks an event outcome and Q29 asks for a discretionary decision. Neither defect arises from an unstated runtime or convention. **Pass.**

5. **Prediction.** Even counting only Q1, Q4–6, Q9–10, Q12–14, Q16, Q18–19, Q22, Q24, Q27 and Q30 gives 16/30. These require applying a rule to a particular file state, grade, command sequence or described action to determine a result. The threshold is 15. **Pass.**

6. **No trivia.** The file and role names serve operational questions, including which record controls work selection and which agent can issue a grade. No question asks for a date, person, product or flag name as an isolated fact. **Pass.**

7. **Trap named.** Each trap identifies a concrete erroneous choice or belief. Q4 identifies accepting a higher total despite a lost pass. Q8 singles out opening the target before checking the handoff. Q28 identifies equating a live path with a snapshot. No trap consists solely of a generic claim of confusion. **Pass.**

8. **Answer shape.** Python verified exactly one Why, Answer, The trap and Rule label, in that order, in each of the 30 answers. All 30 are within the inclusive 60–150 range (100%, minimum 79, maximum 134). Per-question counts appear below. **Pass.**

9. **Coverage.** The nine-group map is at the head of the key and absent from the opening. Some references overstate coverage. Group 8 assigns Q25 to “Project-folder boundaries and session-dependent git push”, although “only a human can renew” supplies the blocker directly and neither situation tests who pushes. The startup *reading order* is tested in Q8, while Q1 and Q13 ask which work to pick. The *bounded step size* is generally a given, e.g. Q26 already “decides to stop cleanly”. Q3 and Q20 repeat the same handoff decision in the same four-option format. Compare Q3(b) “the relevant file paths and a target review output path” with Q20(a) “The relevant file paths to review and the output path”. Changing grading to gate review leaves the decisive reasoning and response unchanged. **Fail.**

10. **Distractors.** There are eight multiple-choice questions. Q2, Q3, Q7, Q9, Q11, Q20 and Q25 have identifiable procedural beliefs behind the alternatives. Q17(b) adds “appending after a clean round corrupts `CHANGELOG.md`” and Q17(c) says leaving the handoff “prevents Round 5 from reading `loop/BACKLOG.md`”. Neither offers a plausible link between those files. The trap’s description that both “misunderstand `STATE.md`'s role” never explains either consequence. These are filler alternatives. **Fail.**

11. **Artifact size and answer leakage.** Python found 19 fenced artifacts, all 1–10 lines long including internal blank lines. The longest procedural setup was Q26 at 92 words including its five action cards. Q27’s setup is 75 words before the question, within the approximate target. Its stem nevertheless quotes “Next step: Have dadhichi-head grade runs/r1/ into runs/r1/review.md” and identifies the file containing it. A learner can copy the answers to parts 1 and 2 without applying the handoff or reviewer rules. **Fail.**

12. **Progression.** Q1–6, Q7–21 and Q22–30 give exactly 6/15/9 (20/50/30%). The final band combines rules. Q23 requires recognizing two different protected copies, Q24 combines grading authority, promotion and logging, and Q30 combines logging, backlog completion, pushing and final status. **Pass.**

13. **Answers hidden.** The files correctly separate the questions from the formal key. Q27 nevertheless answers two of its own scored parts before the key. It says Round 1 “overwrites `loop/STATE.md` with `Next step: Have dadhichi-head grade runs/r1/ into runs/r1/review.md`”, then asks “which file tells Round 2 to grade” and “which agent writes `runs/r1/review.md`”. Both requested identities are explicitly paired with their jobs in the question sheet. Ordinary unmarked multiple-choice options are not the issue here. **Fail.**

14. **Honesty and source.** Q20’s “only file paths” adds a restriction to the review handoff. Q12, Q25 and Q29 present stronger conclusions than their source rules support. The audit below also records unsupported trace details, including Q21’s claim of a completed grade. Input 7 permits no invented protocol claims. **Fail.**

15. **Diagnosis.** This is Input 7 in sheet mode. Only Input 9 tests diagnosis of a learner reply. **N/A.**

16. **No copying.** The questions use round handoffs, grades, file operations and backlog transitions. None reproduces the React, bond or Python calibration artifact or trace. **Pass.**

## Source audit for Check 14

The following are claims about what the protocol requires, or what the described run establishes. Fictional case inputs, explicitly hypothetical grades and deliberately wrong choices are not assertions that those events or policies exist in Dadhichi.

| Location | Wording and source discrepancy |
| --- | --- |
| Q2, Q5 | Q2 defines a subagent as “an independent agent instance with clean context”. L16 requires **fresh general-purpose** writers, without defining all subagents that way. Q5 calls the runner “the host wrapper that launches rounds”. L22 assigns it the push. It does not describe its launch architecture. |
| Q7 | Option (b) includes “the decision in `loop/STATE.md` for user review”. L1 requires recording the reason. L27 reserves the handoff requirement for decisions the user should review. Recording this routine formatting choice there is permissible, but its inclusion is not compulsory simply because a choice occurred. |
| Q9 | “keep a split parent `[ ]` until every sub-item under it is complete” works for the active parent in the stem. L26 forbids premature completion and requires adding split sub-items. It does not establish a universal rule forbidding a split item from being parked. |
| Q12 | “nothing is missing” conflicts with the last-line rule at L30. L22 changes responsibility for pushing only. |
| Q16, Q22, Q27, Q30 | Q16 says skipped items “are never picked up automatically”; L11 skips them during backlog selection, while L10 independently prioritizes a state-named unfinished step. Q16’s “Emit ... IDLE when no `[ ]` items remain”, Q27’s “finishing the last `[ ]` item ends in `IDLE`” and Q30’s analogous rule omit the clean-finish condition. L32 makes an empty backlog necessary for IDLE. It does not give it precedence over a human blocker. Q22’s “keeps the status at `CONTINUE` until the entire item is complete” likewise omits the human-blocker case (L33). The particular clean examples support the keyed statuses. |
| Q19 | “Actions 1 and 4 ... follow the required freeze-and-commit workflow” overstates action 1. Creating a file called `prompt.md` establishes its location, not that it contains the exact prompt required by L18. The Rule’s “modify external settings” also narrows L22’s unqualified prohibition on changing settings. |
| Q20 | “passing only file paths” adds exclusivity. L17 specifies what the head needs. L16 explicitly restricts what **test writers** may receive. L13 mentions gate reviews, but does not define the key’s wider gloss “formal checks before advancing or shipping a prompt”. “Sending summaries or pre-filled grades biases or replaces the judge” is a rationale or risk, not a documented result of sending any summary. |
| Q21 | The stem says the agent “only sends ... to `dadhichi-head` for grading”. The key says “this round both graded a run and made a decision.” Dispatch does not establish a returned grade, and L13 treats running a test set and grading a run as distinct examples. The recorded decision independently satisfies L25. |
| Q25 | “chooses sensibly, records why, and emits `CONTINUE`” confuses the instruction to keep working at L1 with the final status under L30–33. “only when an external issue requires a human fix” adds *external* to L33’s human-fix requirement. In Y, the stem itself supplies the human-only credential condition. |
| Q26, Q27 | Q26’s trace calls the stopping point “45 minutes with saved state” although overwriting the handoff is still pending. Q27 describes writers receiving “only filled inputs”. Read literally, this omits the prompt itself, required by L16. Its trap says the backlog “doesn't record that tests already ran”. L26 permits completed sub-items to record progress. The source assigns the next-step handoff to state without imposing that limitation on backlog contents. |
| Q28 | If “Passes the live path ... directly to fresh subagents” describes the entire handoff, L16 is independently violated as well as L18. The answer accepts the stem’s claim of exactly three violations without resolving what those subagents saw. |
| Q29 | “zero regressions -> promoted” reverses the implication in L19, “Promote only when the head says”. The gate permits promotion in Case A. The protocol and stem do not say that a passing candidate was promoted. |

## Python measurement details

The parser matched the 30 numbered Markdown sections in each file. It excluded field labels, separators and standalone numbered trace markers, then counted whitespace-delimited tokens containing at least one alphanumeric character. Paths and hyphenated words each count as one token. In Q1–Q30 order, the answer counts were:

~~~text
98 119 104 111 99 79 101 106 106 100
103 134 85 115 109 84 103 101 94 91
106 107 112 101 99 115 102 124 110 111
~~~

For each fenced block, the script counted physical content lines between delimiters, including internal blank lines. The results as question number/lines were:

~~~text
1/8  4/2  5/3  6/3  9/1  10/4  12/2  13/10  14/4  15/5
16/3  18/2  19/4  22/7  23/4  24/2  28/3  29/2  30/3
~~~

As a conservative screen for prose length, the script also counted each complete stem including artifacts and the question itself, excluding option lists, band headings and fence delimiters. Four exceeded 80 words. Removing just the final request yielded Q22 62, Q26 92, Q27 75 and Q30 51. Q26 includes five ordering choices. The Check 11 failure turns on disclosure of the answers, independently of that approximate length target.
