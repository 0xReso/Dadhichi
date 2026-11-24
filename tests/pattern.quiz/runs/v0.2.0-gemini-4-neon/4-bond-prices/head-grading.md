# Head review · Input 4 · How bond prices react to interest rates

**Gemini 4 Neon, frozen prompt v0.2.0, medium depth, sheet mode.** Of 15 applicable checks, 8 pass, 1 is borderline and 6 fail. Check 15 does not apply. The highest-priority failure is Q8. A learner who remembers the prompt's bond example can answer Q8 using the same comparison and the same trap.

## Check 2 and 3 evidence

I repriced the specified cash flows in Python 3. For a face value of 100, annual dollar coupon C, yield y in decimal form and n remaining years, I used the following calculations. Prices and returns below use full precision until the displayed result. I treated dollar quotes as cent-rounded unless a question explicitly asks the learner to use a quoted intermediate value.

```python
flows = [C] * (n - 1) + [100 + C]
pv = [cash / (1 + y)**t for t, cash in enumerate(flows, 1)]
price = sum(pv)
macaulay = sum(t * value for t, value in enumerate(pv, 1)) / price
modified = macaulay / (1 + y)
```

I solved for YTM by bisecting the yield until price matched the purchase price. For horizon wealth, I compounded each received coupon from its payment date and added the value of the remaining cash flows at the horizon. For portfolios I applied each bond's percentage move to the dollars invested in that bond. For direction-only questions without a coupon or starting yield, the sign follows from the change in the discount factor for each positive cash flow. The agreement column grades the requested outcome. It flags trace errors and identifies answers conditional on a missing setting.

| Q# | Independent result | Stated result | Agree? |
| --- | --- | --- | --- |
| 1 | 4% of $100 pays $4 at year-end, including after the move to 7%. | $4 | Yes |
| 2 | If new 8% bonds sell at par, the old $5 coupon discounts at 8% to $88.02. An 8% coupon alone does not establish the issue yield. | (c) Below $100 | Conditional |
| 3 | $100/1.10 = $90.91. The unrounded price earns $9.09. Subtracting 10 dollars instead would imply an 11.11% yield. | (b) $90.91 | Yes |
| 4 | At 4%, A is $108.90 and B is $95.55. | (b) A above par, B below | Yes |
| 5 | Current yield is 4/96 = 4.1667%. Redemption adds $4 over two years. Solving for YTM gives 6.1875%. | (d) Above 4.17% | Yes |
| 6 | Three years of cash flows are worth $89.30795. Two years are worth $92.66643 at the same 6%. | (c) Above $89.31 | Yes |
| 7 | A falls to $98.17 (−1.83%). B falls to $90.29 (−9.71%). | (b) B | Yes |
| 8 | A goes from $112.42 to $119.39 (+$6.97 or 6.20%). B goes from $75.16 to $80.61 (+$5.45 or 7.25%). | (a) B | Yes |
| 9 | −6 × 0.005 = −3%, taking $100 to approximately $97. | $97 | Yes |
| 10 | One-period ratios are 0.990291 and 0.990991. Over ten years, $82.03 becomes $74.41 (−9.30%) and $38.55 becomes $35.22 (−8.65%). | (a) The 2% to 3% shock | Yes |
| 11 | At 7% the price is $78.81, a $21.19 loss. At 3% it is $129.75, a $29.75 gain. | (d) Gain larger | Yes |
| 12 | Fixed bond reprices to $79.87 (−20.13%). At reset, an unlevered default-free floater paying the market rate is worth $100. | (c) Only A drops sharply | Yes |
| 13 | $100 plus accumulated $6 coupons gives $179.08477 at 6% and $186.91938 at 8%. | (b) Higher final wealth | Yes |
| 14 | $100/1.21 = $82.64463. Next year's value is $90.90909 using full precision. Literally multiplying the displayed $82.64 by 1.10 gives $90.904. | (b) $82.64 | Yes, intermediate rounding |
| 15 | At 3%, A is $125.59. Under immediate economically optimal exercise with deterministic rates, B redeems at $102. | (c) Roughly $126 and near $102 | Yes under the simple call model |
| 16 | 9/112 = 8.0357% current yield. The $12 premium amortizes over three years. YTM is 4.6245%. | (a) Below 8.04% | Yes |
| 17 | Discounting $4 coupons at the stipulated 6% gives $85.28. Exact compounded nominal yields would be 4.04% and 6.08%. The stem supplies the nominal yields to use. | (d) Well below $100 | Yes |
| 18 | At 4%, five years of $8 coupons give $117.81. Three remaining years give $111.10. | (a) Lower | Yes |
| 19 | 4 + 3 = 7%, then 3.5 + 4.5 = 8%. A five-year $7 coupon falls from $100 to $96.01. | (c) Falls | Yes |
| 20 | Losses are A 10.8485%, C 9.6265%, B 7.9617%. A rounds to 10.8% at one decimal. | A, C, B | Yes, trace gives A 10.9% |
| 21 | Only the ten-year payment matters. Its price rises from $64.39 at 4.5% to $66.27 at 4.2%. | (b) Rises | Yes |
| 22 | All value arrives in year 11. Modified duration is 11/1.10 = 10 years. | 10 years | Yes |
| 23 | Both modified durations are 9.52381. Scaling each position by (1.05/1.08) to its maturity gives X $75.45 and Y $77.37. | (d) Y | Yes |
| 24 | The 6% coupon pays $6 per $100 face. Applying it to the $90 purchase price would give $5.40. | $6 | Yes |
| 25 | At 6% the exact prices are $91.57527 and $108.42473. Both round to the quotes, and each is $8.42 from par to the cent. | (a) Both 6% | Yes |
| 26 | Par implies a $4 coupon. Modified duration is 9.98565, or 10 to the stated precision. The supplied linear estimate is $120 and exact repricing gives $122.70. | (c) Higher than $120 | Yes |
| 27 | Prices rise to $102.77509 and $107.43533 (+2.8% and +7.4%). Macaulay durations are 2.85941 and 7.46321 years. Modified durations are 2.72325 and 7.10782. | (b) About 7.4% | Yes, duration trace is wrong |
| 28 | X loses 4.8068% and Y loses 4.3472%, from the fifth powers of 1.01/1.02 and 1.12/1.13. | (a) X | Yes |
| 29 | A seven-year $4 coupon reprices to $106.23 at 3%. That is an illustration. The question specifies the fund's holdings' yield, not their coupon or the fund's distributions. Rising holdings values lift NAV with other fund effects held fixed. | (d) Fund share price rose | Conditional |
| 30 | In units of current indexed principal, pricing the $1 real coupon at 3% takes $100 to $82.94. | (b) Falls sharply | Yes |
| 31 | Original Macaulay duration is 7.80169. At year 2 the sale brings $83.40, total wealth $95.94 and annual return −2.05%. Year 10 wealth is $191.16 and annual return 6.69%. | (a) Only the two-year holder earns below 6% | Yes |
| 32 | Straight-bond value at 8% is $79.87. A financially rational issuer has no immediate incentive to exercise. The callable bond equals the straight bond if future exercise is worthless. Its residual option value is unspecified. | (c) Falls nearly as much as A | Conditional |
| 33 | One $4 coupon and a $100 reset value in one year give $104/1.08 = $96.30. Treating all ten coupons as fixed at $4 would give $73.16. | (b) $96.30 | Yes, using the stated full coupon periods |
| 34 | 4 + 4 = 8%, then 4.5 + 2.5 = 7%. An $8 coupon at 7% gives $104.10. | (d) Rises | Yes |
| 35 | For each zero, price decreases with its own yield. Lower two-year yield raises A, higher ten-year yield lowers B. | (a) A up, B down | Yes |
| 36 | Par implies a $5 coupon. Modified duration is 12.08532, or 12 at the supplied precision. The supplied estimate is $64. Exact price is $71.19 (−28.81%). | (c) Above $64 | Yes |
| 37 | $82.64463 grows at 10% to $90.90909. As in Q14, multiplying the printed $82.64 by 1.10 gives $90.904. | $90.91 | Yes, intermediate rounding |
| 38 | Steps 1 and 2 give −0.004 and +2%. Step 3 applies 2% to the wrong base. The gain is $1.80 on $90, giving $91.80. | Step 3, $91.80 | Yes |
| 39 | Scaling to $100 invested gives A $121.43381 and B $121.66288. B's Macaulay duration is 4.996746 versus 5 for A. The displayed durations agree to one decimal only. | (b) B | Yes, trace treats durations as exactly equal |
| 40 | Loan installment $23.09748. At 7% the loan is worth $94.70423 (−5.30%) and the bullet $91.79960 (−8.20%). | (d) B loses more | Yes |
| 41 | A's current yield is 2.1739%. Its $8 redemption gain contributes to a YTM of 6.3872%. B yields 5%. | A | Yes |
| 42 | $500 to $333.33 loses one-third. $100 to $90.91 loses one-eleventh. The relative yield increases are 50% and 10%. | 33.3% and 9.1% | Yes |
| 43 | Macaulay durations A 6 and B 5.56621. A loses 5.5285% and B loses 5.1208%. | (a) A | Yes |
| 44 | In the immediate-exercise model, the straight value at 3% is $117.06, capped at $100. At 7% the straight value is $85.95, a $14.05 loss. | (c) Loss much larger than gain | Yes under the simple call model |
| 45 | Starting price $82.64463. After a year at unchanged yield it would be $90.90909 (+10%). The 12% yield cuts that by 1.7857% to $89.28571, still above purchase price. | Higher, $89.29 | Yes |
| 46 | Duration 5.91732 years. Resale $100 vs $98.14815, accumulated coupons $41.85191 vs $44.01557. Wealth $141.85191 vs $142.16372. Actual surplus $0.31181. | (b) Slightly above target | Yes, trace gives $142.17 |
| 47 | Stipulated nominal yield rises from 4% to 5.5%, reducing the nominal PV. The real yield falls from 2% to 1.5%, increasing the indexed PV. | (d) Nominal down, linked up | Yes |
| 48 | Contract coupon at today's benchmark is 4 + 2 = 6%. Required yield is 4 + 5 = 9%. Five years of a 3-point spread shortfall put the value at $88.33 with a flat curve and unchanged spreads in the illustration. | (a) Well below $100 | Yes |
| 49 | Linear losses 2.8846% and 1.9231%, exact losses 2.8234% and 1.9029%. A's shock is 7.5 times as large against one-fifth the duration. | (b) A | Yes, final rule contradicts calculation |
| 50 | Modified durations 9.52381 and 9.09091. With the displayed inputs, $61.39 × 0.524 = $32.17. Using full precision gives a $32.16 tangent estimate. Exact price $38.55, down 37.1991%. | (c) Above $32.17 | Yes |
| 51 | A falls from par to $91.47 (−8.5302%), B to $93.58 (−6.4177%). | (a) A | Yes |
| 52 | Initial value $111.31657. After the first coupon the remaining $110 discounts at 3% to $106.79612. | Lower, $106.80 | Yes |
| 53 | $100 − $81 = $19. Annualized gain is √(100/81) − 1 = 11.1111%. The 23.4568% cumulative return divided by two would give 11.7284%. | $19 and 11.1% | Yes |
| 54 | X stays at $100. Y's components become $49.06105 and $59.39875, totalling $108.45980. Initial Macaulay duration is 10 for each portfolio. The initially flat curve becomes inverted across the quoted tenors. | (d) Y | Yes, stem mislabels the final curve shape as flattening |
| 55 | A moves $87.01157 to $89.36215 and pays $2. B moves $112.98843 to $110.63785 and pays $8. Both earn exactly 5% on full-precision prices. | (c) Both 5% | Yes |
| 56 | 4 + 0.5 = 4.5%. Straight value $119.78 exceeds the $101 immediate call price. | (b) A near $120, B capped near $101 | Yes under the simple call model |
| 57 | Perpetuity modified duration is 20. Price falls $100 to $83.33 (−16.6667%). Zero's modified duration is 28.57143. Price falls $23.14 to $17.41 (−24.7506%). | (a) B | Yes |
| 58 | Using the supplied 7% nominal yield, A falls to $78.93. B resets to $100. C stays at $100 per $100 of current indexed face at its unchanged 2% real yield. | (d) Only A | Yes |
| 59 | Coupons accumulate to $39.542385, giving $139.542385 held. Exact proceeds $77.919739 compound to the same wealth. Literal $77.92 compounds to $139.542853. Both round to $139.54. | (c) Same $139.54 | Yes to cents, trace calls $77.92 exact |
| 60 | D goes $61.39133 to $82.03483 (+33.6261%). A goes $100 to $126.94775 (+26.9478%). With immediate exercise B gains 2%, and C gains 0%. | D, A, B, C | Yes under the simple call model, A's gain rounds to 26.9% |

## Rubric decisions

1. **Count.** The questions and answer key each number Q1 through Q60 once, in order. Medium depth requires 60. **Pass.**

2. **Correct.** The 60-row audit finds no incorrect keyed choice or requested numerical answer under the intended classroom conventions. Several traces would teach a false step. Q27 calls duration the “weighted-average payment time (duration) to 7.4 years—less than triple the 3-year bond's 2.8 years.” The actual weighted times round to 7.5 and 2.9 years. The percentages in the answer are finite price gains. Q46 says “leaving `$142.17`, slightly above your `$141.85` target.” Full-precision wealth rounds to $142.16, and the increase in accumulated coupons rounds to $2.16. Adding the cent-rounded components produces the extra cent. Q49 says “Actual price moves equal duration times *that maturity's* yield change,” even though its own exact and approximate losses differ. The signed first-order estimate is −modified duration × change in yield. Q39's “respond identically to tiny yield moves” also overstates equality of the first-order sensitivities. The table records additional rounding discrepancies, including Q20, Q37, Q59 and Q60. The rubric reserves Fail for a wrong answer and grades a right answer with a false trace step Borderline. **Borderline.**

3. **Determinate.** I checked each prompt and choice against the outcome in its table row. Q38 has one originating error at step 3. Step 4 correctly adds the amount propagated from that error. Q39's rounded durations do not create a tie when its specified cash flows are priced. Q54's stated tenor-by-tenor shocks give a unique portfolio ranking despite the curve label. The questions with answers that vary by a missing market setting are scored under check 4 as the rubric directs. I found no additional case with two defensible outcomes under the same settings. **Pass.**

4. **Assumptions.** The opening fixes face value, coupon dates and frequency, default risk, compounding and a flat curve unless overridden. It leaves out settings that affect multiple answers.
   
   - Q2 says only “new 5-year bonds are issued paying 8% annual coupons.” The Why adds “$8 per year for $100.” If the new bonds are issued at par, the market yield is 8% and the old bond falls. At a still-unchanged 5% yield, a new 8% coupon could instead be issued for $112.99 and the old bond would remain at par.
   - Q29 asks what happened to “the fund's share price” **over a month**. Its holdings appreciate from the yield move, but a fund distribution reduces ex-distribution NAV per share. Neither the distribution nor its absence is specified. Its Why also prices “existing 4% bonds” as par coupon bonds when the stem gives the yield only.
   - Q32 concludes the callable bond falls “nearly as much as Bond A” because the issuer has no reason to exercise today. A still-live future call can have value. The curve alone does not price that option. The Why's “near `$79.87`” is the straight-bond value. State deterministic post-shock rates and rational, costless exercise for the call examples, or ask about the incentive to call today. **Fail.**

5. **Prediction.** A conservative count takes Q1–Q21 and Q23–Q36, or 35/60 (58.3%). Each asks for the outcome of a specific payment, trade, time passage or rate shock. This already clears the 50% threshold before counting Q37–Q60. **Pass.**

6. **No trivia.** All 60 ask about payments, prices, risk, portfolio performance or a calculation. Even the direct duration question, Q22, requires deriving 10 years from an 11-year maturity and 10% yield. **Pass.**

7. **Trap named.** Every trap identifies a particular belief. For example, Q24 applies the coupon to the $90 purchase price, Q38 applies a duration percentage to face value, and Q59 assumes selling creates the economic loss. None of the 60 uses a generic confusion in place of a belief. **Pass.**

8. **Answer shape.** Python 3 split the key on its 60 question markers and checked each field sequence. All 60 contain Why, Answer, The trap and Rule in order. Counting the body text of all four fields, including numbers and excluding field labels, list markers and numbered trace steps, gave **60/60 (100%) within 60–150 words**, range 78–145, median 120.5. I counted alphanumeric tokens, retaining internal apostrophes, decimals, slashes and hyphens. **Pass.**

9. **Coverage.** The opening is clear of the map. The key starts with 18 mechanisms, each has at least three references, and their union covers Q1–Q60. The failure is repeated question design. Q10 asks “In which scenario does the bond lose a larger percentage of its starting price?” for the same zero's equal shocks at low and high starting yields. Q28 asks “Which bond drops by a larger percentage?” for the same calculation, now with two countries, five years and different rates. Q26 asks “How does the bond's actual new price compare to $120.00?” and Q36 repeats it as “How does the bond's actual new price compare to $64.00?” Both hand the learner the tangent estimate and ask which side of it the price curve lies on. Reversing the shock leaves the same comparison and answer. **Fail.**

10. **Distractors.** Python found 47 four-option items. Most wrong options express a plausible calculation or pricing belief. Q15(d) says “Bond A stays at $100 while Bond B falls to $102” after stating that both start at $100. A fall from $100 to $102 is internally impossible, and the key's attribution to “reversing how yields affect prices” does not produce that option. A learner can discard it without understanding callability. **Fail.**

11. **Artifact size and leakage.** Python measured each scenario, including embedded lists and the closing question, excluding the Q number and answer choices. Scenario lengths were 21–90 words, median 52. Only Q58 (81) and Q59 (90) exceeded 80, and both are near the guideline. There are no code blocks. Q25 nevertheless says both bonds “are priced accurately today when 5-year yields are 6%” and then asks “Which bond offers the higher yield to maturity?” Option (a) restates the supplied result. The learner can skip the two prices entirely. Remove the given market yield and ask what discount rate fits both quoted prices. **Fail.**

12. **Progression.** Q1–Q12, Q13–Q42 and Q43–Q60 contain 12, 30 and 18 questions, exactly 20%, 50% and 30%. The last band includes opposing coupon and maturity effects (Q43), resale price against reinvested coupons (Q46), and a four-instrument ranking (Q60). **Pass.**

13. **Answers hidden.** The sheet presents all 60 questions in the question file. The mechanism map, worked answers and marked choices appear in the answer file, after its “Answer key” heading. The self-revealing wording of Q25 is scored under check 11. **Pass.**

14. **Honesty and source.** Input 4 supplies no source. Q56 nevertheless teaches an unconditional exercise trigger: “A call cap is triggered whenever the issuer's total borrowing yield falls below the bond's coupon”. Its own callable bond has a $101 redemption price. At a 6.9% refinancing yield, below its 7% coupon, the straight value of its ten remaining years is only $100.71. Immediate redemption at $101 would cost more than leaving it outstanding, even with zero refinancing costs. The specific answer for the much larger shock to 4.5% is sound. The portable rule invents a threshold and omits its limitation. **Fail.**

15. **Diagnosis.** Input 4 uses sheet mode. This check applies only to input 9. **N/A.**

16. **No copying.** The calibration asks “Which loses a larger percentage of its price?” for two ten-year bonds with different coupons, both yielding 5% before a one-point rise to 6%. Q8 asks “Which bond's price rises by a larger percentage?” for two eight-year bonds with different coupons, both yielding 6% before a one-point fall to 5%. Both isolate coupon size at equal maturity and yield, and both offer the equal-maturity/equal-percentage distractor. Reversing the shock, changing the coupons and swapping the bond labels leave the same decision. Q20 is a close three-bond extension. By comparison, Q43 makes coupon and maturity point in opposite directions, and Q60 also requires pricing a call and a floating reset. Those questions introduce decisions beyond the calibration. Q8 alone breaches the zero-copy condition. **Fail.**

## Version decision and next fix

The v0.1.0 run directory contains a gate review, with no bond output for a prior-version comparison. The other v0.2.0 bond grade is a same-version comparison. It also failed copying, coverage and distractors, including a calibration-derived Q8. This sample gives no basis for promotion.

**Fix Q8 first.** Keep the coupon-sensitivity mechanism, but change what the learner must decide. For example, give pre- and post-shock quotes and ask whether a trade sized to equal face amounts produces the same dollar exposure as one sized to equal market values. The writer would need to compute both outcomes, and remembering which coupon had the larger percentage move in the calibration would no longer settle the question.
