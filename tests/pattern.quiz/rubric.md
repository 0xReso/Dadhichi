# Upskill quiz checks

The grader applies each check to the whole output and quotes the question number for any non-Pass. Checks 2 and 3 require the grader to work every answer independently, not to read the given trace and agree with it. For check 2, record one line per question: number, your own result, the stated result, agree or not.

| # | Check | Pass condition |
| --- | --- | --- |
| 1 | Count | Exactly 30, 60 or 100 numbered questions for low, medium or high. Interactive mode: part one has exactly ten. |
| 2 | Correct | Every stated answer is right under the stated assumptions. One wrong answer is a Fail. One answer that is right but whose trace contains a false step is Borderline. |
| 3 | Determinate | Every question has exactly one defensible answer under the stated assumptions. Ambiguity caused by an unstated setting is scored under check 4, not here. Zero ambiguous questions is Pass, one is Borderline, two or more is a Fail. |
| 4 | Assumptions | The opening states the version, runtime, mode or convention that the answers depend on. One answer that depends on an unstated setting is Borderline; two or more is a Fail. |
| 5 | Prediction | At least 50% of questions ask the learner to predict an outcome from a concrete artifact (code, numbers, rows, a position or a described setup). |
| 6 | No trivia | Zero questions whose answer is a date, a person, a product name or a flag name memorized without the behavior behind it. |
| 7 | Trap named | Every answer's trap names a specific wrong belief, not a generic "people often get confused." Pass: none generic. Borderline: up to 10% generic. Fail: more than 10%. |
| 8 | Answer shape | Every answer has Why, Answer, The trap and Rule, in that order. 90% or more fall within 60 to 150 words. |
| 9 | Coverage | The mechanism list at the head of the answer key (sheet) or scorecard (interactive) maps to question numbers, and the opening contains no such map, and every mechanism is tested at least twice in different shapes. No two questions differ only in surface details. |
| 10 | Distractors | In every multiple-choice question, each wrong option corresponds to a recognizable wrong belief. No filler options. |
| 11 | Artifact size | No artifact exceeds 15 lines of code; scenarios stay near 80 words. No stem, variable name or comment gives the answer away. |
| 12 | Progression | The three bands are present in the stated proportions (about 20/50/30), and the final band combines mechanisms or tests edge cases. |
| 13 | Answers hidden | Sheet mode: no answer appears before the answer key. Interactive mode: part one contains no answers. |
| 14 | Honesty and source | Input 5 corrects the premise without inventing an API. Input 7 contains no claim absent from or contradicting the source. Any input: an unreliable area is declared rather than filled with invention. |
| 15 | Diagnosis (input 9 only) | Each wrong reply is marked wrong, given the full answer, and the specific wrong belief behind that reply is named. |
| 16 | No copying | No question reuses a calibration example from the prompt with only surface changes. |
