# Failure log: pattern.explain

One line per failure: date | input # | check failed | suspected cause | fixed in version

2026-11-15 | 2 | 4 Proportional, 5 Padding | Situation says reader will "open official documentation later" and write rules say "say so" for version differences, which licenses config keys, protocol versions, and implementation variants in the body | 0.2.1 (inputs 2, 3)
2026-11-15 | 3 | 5 Padding | Same cause; plus read strategies, pre-vote, and history kept in body instead of Going further | 0.2.1 (inputs 2, 3)
2026-11-15 | 2, 3 | 4 Proportional | Length ranges say "roughly"; model plans toward the top of the range, and the self-check has no word-count step | 0.2.1 (inputs 2, 3)
2026-11-15 | 3 | 5 Padding | Rule "end each chapter on what is now possible" read as "end with a recap", so chapters recap at both ends | 0.2.1
2026-11-15 | 2, 3 | 2 Linear | "This matters in a moment" exception generalized into "as you will see" forward references | 0.2.1 (inputs 2, 3)
2026-11-15 | 1 | 4 Proportional, 5 Padding | v0.2.1 sized the topic as moderate: step 9 has no criterion for "simple" after the API-key example was removed, and the body test passes every mechanism step whatever the size | 0.3.0 (edit applied, not yet tested)
2026-11-15 | 2, 4 | 6 Resumable | Prompt applies the reminder rule to "chapters" and tells moderate pieces nothing about headings; model used many "##" sections and did not restate | 0.3.0 (edit applied, not yet tested)
2026-11-15 | 4 | 3 Accurate | No instruction for a topic unknown as a whole; model hedged on "details" and wrote a moderate-size generic piece under the tool's name | 0.3.0 (edit applied, not yet tested)
2026-11-15 | 2, 3, 4, 7 | 11 Unhurried | One-idea-per-paragraph rule is in the write section but not in the self-check; vocabulary paragraphs stack three to six terms | 0.3.0 (edit applied, not yet tested)
2026-11-15 | 3 | 11 Complete | Log repair and discarded entry described as rules without the running example | 0.3.0 (edit applied, not yet tested)
2026-11-15 | alexa (real use, mixed-confidence source) | 3 Accurate, 11 Unhurried | Prompt silent on carrying source confidence through: invented provenance, writer inferences stated as fact, claims of absence where source is silent, hedges dropped in The whole picture | 0.3.0 (edit applied, not yet tested)
