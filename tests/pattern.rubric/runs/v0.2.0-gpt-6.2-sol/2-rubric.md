| # | Check | Pass condition | Decided by |
|---|---|---|---|
| 1 | Review outcome | The output gives at least one finding, explicitly reports that it found no defects, or identifies the missing diff needed to perform the review. | grader |
| 2 | Defect grounding | Each finding’s claim that the PR causes or exposes a failure is supported by the diff and available review context. | grader |
| 3 | Behavioral impact | Each finding identifies a consequence for behavior, data, security, compatibility, or operation. | grader |
| 4 | Failing scenario | Each finding identifies a specific input, state, or sequence and the wrong result it produces. | grader |
| 5 | Actionable location | Each finding identifies where in the change the author can inspect the cause. | grader |
| 6 | Defect coverage | The output includes every independently verified in-scope defect in the grading reference. | grader |
| 7 | Distinct findings | Each underlying defect is reported once. | grader |
| 8 | Severity ranking | The findings appear in descending order of severity. | grader |

## Grading conventions

1. **Review outcome.** Score the output as a whole. Pass if it contains a finding or a clear no-defects conclusion. A missing-diff response passes only when the diff is unavailable. A change summary or test plan alone fails.
2. **Defect grounding.** Score each finding against the diff, surrounding code, and any requirements supplied with the input. One unsupported causal claim fails. A conditional claim passes when its condition is reachable and the failure follows. Score preference-only comments under check 3.
3. **Behavioral impact.** Score each review comment that asks the author to change the PR. One comment based solely on formatting, naming, or another preference fails. A naming change that breaks a public API passes.
4. **Failing scenario.** Score each finding. One finding missing either a trigger or its wrong result fails. A prose scenario passes without an executable reproduction. Judge whether the scenario can actually occur under check 2.
5. **Actionable location.** Score each finding against the diff. One finding whose location cannot be identified fails. A path and line, an unambiguous symbol, or a quoted expression unique in context passes.
6. **Defect coverage.** Score each reference defect. One omission fails. Use only reference defects independently verified against the review input, and accept equivalent descriptions even if the wording or proposed fix differs. Mark this check not applicable when no verified reference is supplied.
7. **Distinct findings.** Score each group of findings that describes the same cause and would be resolved by the same correction. Two or more separate entries in one group fail. Multiple failing scenarios within one finding pass.
8. **Severity ranking.** Compare findings using the verified impact and trigger conditions. One lower-severity finding placed ahead of a higher-severity finding fails. Ties may appear in either order, and ordered findings pass without explicit severity labels. Mark this check not applicable when fewer than two findings remain after excluding unsupported and preference-only entries.