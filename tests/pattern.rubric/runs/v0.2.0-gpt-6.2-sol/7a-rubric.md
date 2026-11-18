| # | Check | Pass condition | Decided by |
|---|---|---|---|
| 1 | Result present | The output contains at least one token. | code |
| 2 | Single result | The output contains at most one token. | code |
| 3 | Decimal integer syntax | The sole token consists of ASCII digits with an optional leading minus sign. | code |
| 4 | Bare terminal output | The token occupies the entire output apart from an optional final line ending. | code |
| 5 | Correct nonblank count | The integer equals the number of nonblank lines in the supplied text. | code |

### Grading conventions

- **1.** Unit: whole output. A token is a maximal run of non-whitespace characters. Zero tokens is Fail, including when the supplied text is empty. One or more tokens passes this check.
- **2.** Unit: whole output. Skip if check 1 fails. One token passes. Two or more is Fail, whether the extra token is another number or explanatory text.
- **3.** Unit: sole token. Skip unless there is exactly one token. One character outside the permitted syntax is Fail. Leading zeros pass.
- **4.** Unit: whole output. Skip unless there is exactly one token and it passes check 3. A bare token or a token followed by one LF or CRLF passes. Any other surrounding whitespace is Fail.
- **5.** Unit: integer value. Skip unless there is exactly one token and it passes check 3. Use the supplied text as the reference. Split on CRLF, LF, or CR and count each resulting line containing at least one non-whitespace character. A difference of one is Fail. A final line without a terminator counts if nonblank. Empty or whitespace-only input has an expected count of zero.