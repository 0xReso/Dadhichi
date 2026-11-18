| # | Check | Pass condition | Decided by |
|---|---|---|---|
| 1 | Count present | The output contains at least one ASCII digit. | code |
| 2 | Single digit run | The output contains at most one contiguous run of ASCII digits. | code |
| 3 | Digits without decoration | Every non-whitespace character in the output is an ASCII digit. | code |
| 4 | Single terminal line | The output contains no line break except for one optional final line ending. | code |
| 5 | Exact nonblank count | The integer in the output equals the number of nonblank lines in the supplied text. | code |

### Grading conventions

1. Unit is an ASCII digit across the whole output. Zero digits scores Fail, and one or more scores Pass.
2. Unit is a maximal contiguous run of ASCII digits. Apply after checks 1, 3, and 4 pass. One run scores Pass, including a multi-digit integer such as `12`. Two or more score Fail.
3. Unit is a character across the whole output. Apply after check 1 passes. One or more characters other than ASCII digits or whitespace scores Fail, including a sign, decimal point, or code fence. Surrounding spaces and tabs pass this check.
4. Unit is a line break across the whole output. Apply after checks 1 and 3 pass. No line break or one final line ending scores Pass. One internal line break or two or more line breaks scores Fail. Treat CRLF as one line ending.
5. Unit is the whole output. Apply after checks 1–4 pass. Use only the supplied text as the reference. Treat LF, CRLF, and lone CR as line endings, and count each line containing at least one non-whitespace character, including a final line without a line ending. Empty and whitespace-only text have a count of zero. Interpret the digit run in base 10, allowing leading zeros. An exact match scores Pass, and a difference of one or more scores Fail.