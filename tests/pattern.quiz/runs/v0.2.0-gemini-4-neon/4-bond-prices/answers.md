# Answer key

## Mechanisms tested

1. **Fixed cash flows** (contractual coupons and face value do not change when rates move): Q1, Q24, Q48, Q53
2. **Inverse price–yield relationship** (bond prices move opposite to market yields): Q2, Q29, Q45, Q47, Q52, Q58, Q59, Q60
3. **Present value discounting** (price equals future cash flows divided by `(1 + r)^t`): Q3, Q14, Q53, Q59
4. **Par, discount, and premium pricing** (coupon rate versus market yield sets price relative to face value): Q4, Q25, Q55
5. **Current yield versus yield to maturity** (true return combines coupons and price gain or loss to maturity): Q5, Q16, Q41, Q55
6. **Pull to par** (discount and premium prices converge toward face value as maturity approaches): Q6, Q18, Q37, Q45, Q52, Q55
7. **Maturity effect on price sensitivity** (longer maturity amplifies percentage price moves): Q7, Q27, Q43, Q49, Q54, Q57
8. **Coupon effect on price sensitivity** (lower coupons delay cash flows and increase percentage sensitivity): Q8, Q20, Q40, Q43, Q51, Q57, Q60
9. **Modified duration approximation** (linear estimate `−Modified Duration × Δy` for small yield shifts): Q9, Q22, Q38, Q46, Q49, Q50, Q57
10. **Starting yield level effect** (lower starting yields make percentage price moves larger): Q10, Q28, Q42, Q51, Q57
11. **Convexity asymmetry** (prices gain more on rate drops than they lose on equal rate hikes): Q11, Q26, Q36, Q44, Q46, Q50
12. **Cash-flow dispersion** (at equal duration, more spread-out cash flows have higher convexity): Q23, Q39, Q54
13. **Reinvestment risk versus price risk** (holding period relative to duration decides whether higher rates help or hurt): Q13, Q31, Q46, Q53, Q59
14. **Floating-rate bonds** (resetting coupons keep prices near par on reset dates): Q12, Q33, Q48, Q58, Q60
15. **Callable bonds** (issuer's right to redeem caps upside when yields fall, creating negative convexity): Q15, Q32, Q44, Q56, Q60
16. **Real versus nominal yields and inflation** (inflation shocks raise nominal yields; inflation-linked bonds track real yields): Q17, Q30, Q47, Q58
17. **Credit spreads versus benchmark rates** (corporate bond prices respond to benchmark yield plus credit spread): Q19, Q34, Q48, Q56
18. **Non-parallel yield curve shifts** (each bond responds to the yield at its own cash-flow maturities): Q21, Q35, Q49, Q54

---

**Q1.**
- **Why:** 1. A bond's coupon rate (the promised yearly interest percentage) is multiplied by its face value ($100) to set the dollar payment: `4% × $100 = $4`. 2. By the fixed cash flows mechanism, a fixed-rate bond's promised payments are locked in by contract and do not change when market interest rates rise to 7%. 3. At the end of Year 1, the issuer pays $4.
- **Answer:** `$4`.
- **The trap:** Answering `$7`, from treating a fixed-rate bond like a savings account or variable-rate loan whose interest payout resets when market rates move.
- **Rule:** A fixed-rate bond's dollar coupons are fixed by contract on its face value, regardless of later moves in market interest rates.

**Q2.**
- **Why:** 1. Your bond's payments remain fixed at $5 per year and $100 at Year 5, while new buyers can now buy 5-year bonds paying $8 per year for $100. 2. By the inverse price–yield relationship, no buyer will pay $100 for $5 a year when $100 buys $8 a year; your bond's price must fall (to $88.02) until its lower purchase price makes its total return match 8%.
- **Answer:** `(c) It falls below $100`.
- **The trap:** Picking `(a)` from believing higher interest rates make bonds more valuable, `(b)` from assuming bonds always trade at face value, or `(d)` from confusing a bond's maturity with a lock-up period.
- **Rule:** Because fixed-rate bond payments cannot rise, market prices must fall when market interest rates rise.

**Q3.**
- **Why:** 1. By present value discounting, a future payment is worth what you would need to invest today at the market rate (10%) to reach that payment. 2. Dividing the $100 payment by `1 + 0.10` gives `$100 / 1.10 = $90.91`. 3. Check: investing `$90.91` at 10% earns `$9.09`, returning `$100.00` in one year.
- **Answer:** `(b) $90.91`.
- **The trap:** Picking `(a) $90.00` by subtracting 10% directly from $100 (which actually yields `$10 / $90 = 11.1%`), `(c)` by ignoring the time value of money, or `(d)` by multiplying instead of dividing.
- **Rule:** To find today's price of a future payment, divide by `(1 + yield)` rather than subtracting the yield percentage from face value.

**Q4.**
- **Why:** 1. Market yield (4%) is what new 5-year bonds pay at $100. 2. By par, discount, and premium pricing, Bond A's 6% coupon beats the 4% market rate, so buyers bid its price above $100 (a *premium*, at $108.90). 3. Bond B's 3% coupon trails the 4% market rate, so it must sell below $100 (a *discount*, at $95.55) to attract buyers.
- **Answer:** `(b) Bond A trades above $100; Bond B trades below $100`.
- **The trap:** Picking `(a)` from assuming bonds always trade at face value, `(c)` from flipping the direction of coupon versus yield, or `(d)` from thinking any positive coupon creates a premium.
- **Rule:** A bond trades above face value when its coupon rate exceeds the market yield, at face value when they match, and below face value when its coupon rate is lower.

**Q5.**
- **Why:** 1. Dividing the annual coupon by the price (`$4 / $96 = 4.17%`) gives only the *current yield* (annual income return). 2. By current yield versus yield to maturity, holding a discount bond to maturity also delivers a $4 capital gain when it repays $100 (about $2 per year over 2 years). 3. Adding that price gain lifts the true yield to maturity to about 6.19%, well above 4.17%.
- **Answer:** `(d) Higher than 4.17%, because they also earn a $4 price gain by maturity`.
- **The trap:** Picking `(a)` by mistaking current yield for total return, `(b)` by thinking a discount is a penalty rather than a gain, or `(c)` by equating return with coupon rate.
- **Rule:** On a bond bought below face value, true yield to maturity exceeds current yield because you earn both coupons and a capital gain to maturity.

**Q6.**
- **Why:** 1. At purchase (3 years left), the bond's $2 coupons lag the 6% yield by $4 per year, pulling its price down to `$89.31`. 2. One year later at the same 6% yield, only 2 years of below-market coupons remain, so by pull to par the price rises to `$92.67` (`$2/1.06 + $102/1.06^2`). 3. Every passing year narrows the gap between price and the $100 maturity payout.
- **Answer:** `(c) It rises above $89.31, moving closer to $100`.
- **The trap:** Picking `(a)` from thinking flat interest rates mean flat bond prices, `(b)` from thinking paying a coupon drains the price of a discount bond, or `(d)` from expecting an instant jump to par.
- **Rule:** Even when market yields never move, a discount bond's price climbs steadily toward face value as maturity gets closer.

**Q7.**
- **Why:** 1. When market yields rise from 5% to 6%, both bonds pay $1 less per year than new 6% bonds. 2. By the maturity effect on price sensitivity, Bond A locks buyers into that $1 shortfall for only 2 years (falling 1.8% to `$98.17`), whereas Bond B locks buyers into it for 15 years and discounts its $100 repayment over 15 periods (falling 9.7% to `$90.29`).
- **Answer:** `(b) Bond B (15-year)`.
- **The trap:** Picking `(c)` from assuming an equal 1-point rate hike causes an equal percentage drop, `(a)` from thinking closer maturity increases exposure, or `(d)` from confusing fixed coupons with fixed market value.
- **Rule:** All else equal, the longer a bond's time to maturity, the larger its percentage price move when interest rates change.

**Q8.**
- **Why:** 1. Both bonds mature in 8 years, but Bond A returns far more cash early through its $8 annual coupons, while Bond B leaves almost all of its value in the $100 Year 8 repayment. 2. By the coupon effect on price sensitivity, later cash flows are discounted over more years and react more to yield changes. 3. When yields fall from 6% to 5%, Bond B jumps +7.3% (`$75.16` to `$80.61`), beating Bond A's +6.2% (`$112.42` to `$119.39`).
- **Answer:** `(a) Bond B (2% coupon)`.
- **The trap:** Picking `(c)` from assuming equal maturity means equal rate sensitivity, `(b)` from noticing Bond A's larger dollar move (+$6.97 vs. +$5.45) instead of percentage move, or `(d)` from expecting opposite directions.
- **Rule:** Among bonds with the same maturity and yield, the lower-coupon bond has a larger percentage price change when rates move.

**Q9.**
- **Why:** 1. Modified duration approximates the percentage price change as `−Modified Duration × Δy`, where `Δy` is the yield change as a decimal. 2. Here `Δy = +0.005` (+0.5 percentage points), so `%ΔP ≈ −6 × (+0.005) = −0.03`, or `−3%`. 3. Applying `−3%` to the $100 starting price gives `$100 − $3 = $97`.
- **Answer:** `$97` (a 3% drop).
- **The trap:** Answering `$103` by forgetting the minus sign (inverse price–yield relationship), or `$94` by multiplying 6 by 1% instead of 0.5%.
- **Rule:** For small rate moves, multiply negative modified duration by the yield change to estimate a bond's percentage price change.

**Q10.**
- **Why:** 1. A 10-year zero-coupon bond's price is `$100 / (1 + y)^10`, so moving from `y1` to `y2` scales the price by `((1 + y1) / (1 + y2))^10`. 2. By the starting yield level effect, `1.02 / 1.03 = 0.9903` (a larger proportional hit per year) gives a `−9.3%` drop (`$82.03` to `$74.41`), while `1.10 / 1.11 = 0.9910` gives a smaller `−8.7%` drop (`$38.55` to `$35.22`).
- **Answer:** `(a) Scenario 1 (2% to 3%)`.
- **The trap:** Picking `(c)` from assuming a 1-point rate increase always causes the same percentage drop, `(b)` from thinking higher rates are more punishing, or `(d)` from ignoring market prices before maturity.
- **Rule:** The same bond loses a larger percentage of its price from a 1-point rate hike when starting yields are low than when starting yields are high.

**Q11.**
- **Why:** 1. Discounting by `1 / (1 + y)^t` produces a curved (convex) price–yield relationship rather than a straight line. 2. At 7% (+2 points), the bond falls to `$78.81` (a loss of `$21.19`). 3. At 3% (−2 points), it climbs to `$129.75` (a gain of `$29.75`). 4. By convexity asymmetry, the price rises more when yields fall than it drops when yields rise by the same amount.
- **Answer:** `(d) The gain is larger than the loss`.
- **The trap:** Picking `(b)` from assuming price changes are symmetric straight lines, `(a)` from fearing downside compounding, or `(c)` from assuming $100 acts as a soft ceiling.
- **Rule:** For a standard non-callable bond, a drop in yields produces a larger price gain than an equal rise in yields produces a loss.

**Q12.**
- **Why:** 1. Bond A's coupons stay locked at $5 while the market demands 8%, so its price plunges 20.1% to `$79.87`. 2. By the floating-rate bond mechanism, Bond B resets immediately to the new 8% rate and will keep resetting to match market rates every year. 3. Because its coupons match the market yield, Bond B stays right at its $100 face value.
- **Answer:** `(c) Only Bond A drops sharply; Bond B stays at $100`.
- **The trap:** Picking `(a)` from assuming equal 10-year maturity means equal rate risk, `(b)` from confusing coupon uncertainty with price risk, or `(d)` from thinking a higher future coupon pushes a reset floater above par.
- **Rule:** A floating-rate bond that resets to the current market rate stays near face value on reset dates and avoids long-term interest-rate price drops.

**Q13.**
- **Why:** 1. Holding to maturity guarantees the full $100 face value at Year 10, so the temporary Year 1 market price drop disappears by maturity. 2. Meanwhile, by reinvestment risk versus price risk, each $6 coupon received in Years 1 through 9 is reinvested at 8% instead of 6%. 3. Total Year 10 wealth rises from `$179.08` (at 6%) to `$186.92` (at 8%).
- **Answer:** `(b) Higher, because your reinvested coupons compound at 8% instead of 6%`.
- **The trap:** Picking `(a)` from believing rising rates always hurt bondholders, `(c)` from forgetting that coupons earn interest after being paid, or `(d)` from assuming price and reinvestment effects always cancel at every horizon.
- **Rule:** When you hold a coupon bond all the way to maturity, higher interest rates raise your final wealth because reinvested coupons compound faster while the final repayment stays $100.

**Q14.**
- **Why:** 1. By present value discounting with annual compounding, a payment two years away is discounted twice: `$100 / (1.10)^2`. 2. Computing `1.10 × 1.10 = 1.21`, today's price is `$100 / 1.21 = $82.64`. 3. Check: `$82.64 × 1.10 = $90.91` after Year 1, and `$90.91 × 1.10 = $100.00` at Year 2.
- **Answer:** `(b) $82.64`.
- **The trap:** Picking `(c) $83.33` from using simple-interest discounting (`$100 / 1.20`), `(a) $80.00` from subtracting `2 × 10%` linearly, or `(d) $90.91` from discounting for only one year.
- **Rule:** Multi-year discounting compounds `(1 + yield)^t` in the denominator, making the price lower than simple linear discounting suggests.

**Q15.**
- **Why:** 1. When market yields drop from 6% to 3%, Bond A's locked-in 6% coupons become highly valuable, lifting its price to `$125.59`. 2. By the callable bond mechanism, the issuer can buy Bond B back at `$102` and refinance at 3%. 3. Because no buyer will pay `$126` for a bond the issuer can immediately redeem for `$102`, Bond B's price stays capped near `$102`.
- **Answer:** `(c) Bond A jumps to roughly $126, while Bond B stays near $102`.
- **The trap:** Picking `(a)` by ignoring the issuer's incentive to refinance, `(b)` by thinking "callable" is a buyer's right rather than the issuer's right, or `(d)` by reversing how yields affect prices.
- **Rule:** A call option belongs to the issuer, so falling interest rates cap a callable bond's price near its call price.

**Q16.**
- **Why:** 1. Dividing `$9 / $112 = 8.04%` computes only the current yield (annual coupon divided by price). 2. By current yield versus yield to maturity, buying at `$112` means taking a guaranteed `$12` capital loss when the bond repays `$100` in 3 years (about `$4` per year). 3. Subtracting that built-in loss brings the true yield to maturity down to about 4.6%, far below 8.04%.
- **Answer:** `(a) Lower than 8.04%, because you lose $12 of price by maturity`.
- **The trap:** Picking `(b)` by treating current yield as total return, or `(c)`/`(d)` by focusing on the 9% coupon rate while overlooking the premium paid up front.
- **Rule:** On a premium bond bought above face value, true yield to maturity is always lower than current yield because the purchase premium disappears by maturity.

**Q17.**
- **Why:** 1. Market yields on fixed-rate nominal bonds reflect both the real interest rate and expected inflation (roughly `real rate + expected inflation`). 2. By real versus nominal yields and inflation, higher expected inflation pushes nominal market yields from 4% to about 6%. 3. Because this bond's future dollar payments stay fixed at $4/year and $100, higher discounting drops its nominal price immediately (to about `$85.28`).
- **Answer:** `(d) It falls well below $100`.
- **The trap:** Picking `(a)` from believing inflation only erodes future purchasing power without changing today's dollar price, `(b)` from thinking bond prices rise with inflation, or `(c)` from subtracting 2% linearly from $100.
- **Rule:** Rising expected inflation lifts nominal market yields, which pushes fixed-rate bond prices down immediately in nominal dollars.

**Q18.**
- **Why:** 1. You paid a `$17.81` premium above `$100` to collect five years of above-market 8% coupons when market yields were 4%. 2. After two years at the same 4% yield, only three years of those extra coupons remain. 3. By pull to par, the bond's price declines steadily toward `$100`, falling to `$111.10` with 3 years left.
- **Answer:** `(a) It is lower than $117.81, moving closer to $100`.
- **The trap:** Picking `(b)` from thinking unchanged yields mean an unchanged price, `(c)` from expecting above-market coupons to keep lifting the price, or `(d)` from thinking it drops below par even though its coupon still beats 4%.
- **Rule:** Even if market yields stay completely flat, a premium bond's price falls steadily toward face value as maturity approaches.

**Q19.**
- **Why:** 1. By credit spreads versus benchmark rates, a corporate bond's total yield equals the government benchmark rate plus its credit spread. 2. Yesterday's total yield was `4% + 3% = 7%`. Today's total yield is `3.5% + 4.5% = 8%`. 3. Because the total yield rose by 1 percentage point, the bond's market price falls (for example, from `$100` to `$96.01` on a 7% coupon bond).
- **Answer:** `(c) It falls, because the bond's total yield rose from 7% to 8%`.
- **The trap:** Picking `(a)` from assuming falling government rates lift all bond prices, `(b)` from thinking opposite moves always cancel without checking sizes, or `(d)` from thinking a wider spread raises fixed coupons.
- **Rule:** A corporate bond's price reacts to the sum of the benchmark rate and its credit spread, not to the benchmark rate alone.

**Q20.**
- **Why:** 1. All three bonds have 12-year maturities and start at a 4% yield, so only their coupon rates differ. 2. By the coupon effect on price sensitivity, lower coupons push more of a bond's value into the distant Year 12 repayment, raising percentage price sensitivity. 3. When yields rise from 4% to 5%, Bond A (0%) drops `−10.9%`, Bond C (2%) drops `−9.6%`, and Bond B (8%) drops `−8.0%`.
- **Answer:** `Bond A, Bond C, Bond B`.
- **The trap:** Reversing the order (`Bond B, Bond C, Bond A`) from thinking larger coupons expose more cash to higher rates, or claiming all three tie because all mature in 12 years.
- **Rule:** At the same maturity and yield, percentage interest-rate sensitivity increases strictly as the coupon rate decreases.

**Q21.**
- **Why:** 1. A 10-year zero-coupon bond has only one cash flow, at Year 10, so its price is `$100 / (1 + y_10)^10`. 2. By non-parallel yield curve shifts, the bond depends on the 10-year yield (`y_10`), not the overnight or 1-year rate. 3. Because `y_10` fell from 4.5% to 4.2%, the bond's price rises (from `$64.39` to `$66.27`).
- **Answer:** `(b) It rises, because the 10-year yield that discounts its cash flow fell`.
- **The trap:** Picking `(a)` from believing every central bank rate hike pushes long-term bond prices down, `(c)` from averaging unrelated maturities, or `(d)` from thinking policy never affects bond markets.
- **Rule:** A bond's price moves with the market yields at its own cash-flow maturities, which can move opposite to central bank short-term rates.

**Q22.**
- **Why:** 1. *Macaulay duration* is the value-weighted average time until a bond's cash flows arrive. For a zero-coupon bond, 100% of the cash arrives at maturity, so Macaulay duration equals 11 years. 2. By the modified duration definition, `Modified Duration = Macaulay Duration / (1 + yield)`. 3. Dividing `11 / 1.10` gives exactly `10` years.
- **Answer:** `10 years` (or `10`).
- **The trap:** Answering `11 years` by using maturity/Macaulay duration directly without dividing by `(1 + yield)`, or `9.9 years` by subtracting 10% of 11 instead of dividing by `1.10`.
- **Rule:** A zero-coupon bond's Macaulay duration equals its maturity, and dividing by `(1 + yield)` converts it into modified duration.

**Q23.**
- **Why:** 1. Both portfolios have the same starting value ($100) and the same modified duration (9.52 years), so they react identically to tiny rate moves. 2. By cash-flow dispersion, Portfolio Y's payments (Years 2 and 18) are spread widely around Year 10, giving it strictly higher convexity than Portfolio X (all cash concentrated at Year 10). 3. When yields jump from 5% to 8%, Portfolio X drops to `$75.45` while Portfolio Y holds up better at `$77.37`.
- **Answer:** `(d) Portfolio Y (barbell)`.
- **The trap:** Picking `(b)` from assuming equal duration guarantees equal performance for any parallel shift, `(a)` from fearing the 18-year leg's loss, or `(c)` from thinking convexity helps only when rates fall.
- **Rule:** Between two portfolios with the same duration, the one with more dispersed cash flows has higher convexity and outperforms on large parallel shifts in either direction.

**Q24.**
- **Why:** 1. A bond's annual coupon is always calculated as `coupon rate × face value`, here `6% × $100 = $6`. 2. By the fixed cash flows mechanism, the price you paid another investor on the secondary market (`$90`) does not alter the issuer's contractual promise to pay `$6` per year.
- **Answer:** `$6`.
- **The trap:** Answering `$5.40` (`6% × $90`), from assuming the coupon percentage applies to your purchase price rather than the bond's face value.
- **Rule:** Secondary-market purchase prices change your yield, never the issuer's dollar coupon payments.

**Q25.**
- **Why:** 1. By par, discount, and premium pricing, Bond A's low 4% coupon is offset by buying it at a discount (`$91.58`, earning an `$8.42` gain to `$100`), while Bond B's high 8% coupon is offset by paying a premium (`$108.42`, taking an `$8.42` loss to `$100`). 2. Because the market priced both default-free 5-year bonds at the same 6% yield, both deliver an identical 6% yield to maturity.
- **Answer:** `(a) Both offer the exact same 6% yield to maturity`.
- **The trap:** Picking `(b)` from viewing a discount bond as a "bargain" with extra return, or `(c)`/`(d)` from equating a higher coupon or higher price with a higher return.
- **Rule:** In an accurately priced market, discounts and premiums adjust bond prices so bonds of equal maturity and credit risk offer the same yield to maturity.

**Q26.**
- **Why:** 1. Modified duration draws a straight tangent line to the curved price–yield relationship at the starting yield (4%). 2. By convexity asymmetry, a non-callable bond's true price curve bends upward above that straight line everywhere away from the starting yield. 3. When yields drop from 4% to 2%, the actual price climbs to `$122.70`, beating the `$120.00` linear estimate.
- **Answer:** `(c) Higher than $120.00`.
- **The trap:** Picking `(b)` by treating modified duration as an exact formula for large rate shifts, `(a)` by thinking duration overstates gains, or `(d)` by thinking convexity depends on discount vs. par status.
- **Rule:** Because standard bond prices curve upward, linear duration estimates always understate the actual price after a large rate drop.

**Q27.**
- **Why:** 1. By the maturity effect on price sensitivity, a 9-year bond moves much more than a 3-year bond when yields fall from 5% to 4%. 2. However, because both pay 5% annual coupons along the way, early coupons shrink the 9-year bond's weighted-average payment time (duration) to 7.4 years—less than triple the 3-year bond's 2.8 years. 3. Bond B actually rises 7.4% (to `$107.44`), not 8.4%.
- **Answer:** `(b) About 7.4% (much larger than 2.8%, but less than triple)`.
- **The trap:** Picking `(a) 8.4%` from assuming price sensitivity scales linearly with maturity for coupon bonds, `(c)` from thinking equal coupons mean equal gains, or `(d)` from dividing by 3 instead of scaling up.
- **Rule:** Longer maturity raises a coupon bond's rate sensitivity, but at a diminishing rate because interim coupons pull the average cash-flow time below maturity.

**Q28.**
- **Why:** 1. A 5-year zero-coupon bond's price changes by `((1 + y1) / (1 + y2))^5 − 1`. 2. By the starting yield level effect, moving from 1% to 2% in Country X yields `(1.01 / 1.02)^5 − 1 = −4.81%`, whereas moving from 12% to 13% in Country Y yields `(1.12 / 1.13)^5 − 1 = −4.35%`. 3. A 1-point jump is a larger relative jump on top of 1.01 than on top of 1.12.
- **Answer:** `(a) Country X's bond (1% to 2%)`.
- **The trap:** Picking `(c)` from treating all 1-point moves as identical, `(b)` from thinking higher yields magnify losses, or `(d)` from guessing that Country Y's lower starting price makes its percentage drop bigger.
- **Rule:** For the same maturity and rate jump, a bond starting at a lower yield suffers a larger percentage price drop.

**Q29.**
- **Why:** 1. A bond fund's share price reflects the current market value of the bonds it already owns. 2. By the inverse price–yield relationship, when market yields drop from 4% to 3%, the fund's existing 4% bonds become more valuable (rising to roughly `$106.23` per `$100` face value). 3. Therefore, the fund's share price rises.
- **Answer:** `(d) It rose, because falling yields increased the market value of the bonds the fund already holds`.
- **The trap:** Picking `(a)` or `(c)` from hearing "yields fell" and confusing lower future yields with falling current fund value, or `(b)` from thinking diversification eliminates interest-rate risk.
- **Rule:** Falling market yields push bond fund share prices up, because the fund's existing higher-coupon bonds gain market value.

**Q30.**
- **Why:** 1. An inflation-linked bond adjusts its face value and coupon dollars for inflation, protecting against *inflation* surprises—not against changes in *real* interest rates. 2. By real versus nominal yields and inflation, its real cash flows are discounted at the market real yield. 3. When the real yield jumps from 1% to 3%, the bond's price drops sharply (from `$100` to `$82.94`).
- **Answer:** `(b) It falls sharply, because its real cash flows are now discounted at a higher real rate`.
- **The trap:** Picking `(a)` from believing "inflation-protected" means "rate-protected," `(c)` from confusing real rates with inflation, or `(d)` from thinking prices wait for an official inflation release.
- **Rule:** Inflation-linked bonds shield you from unexpected inflation, but their prices still fall whenever real interest rates rise.

**Q31.**
- **Why:** 1. By reinvestment risk versus price risk, higher yields cause an immediate price drop (price risk) while letting future coupons compound faster (reinvestment gain). 2. Investor A sells at Year 2, long before the bond's ~7.8-year duration: the remaining 8-year bond sells for `$83.40`, leaving `$95.94` total with coupons (about `−2.1%/yr`, well below 6%). 3. Investor B holds to Year 10, recovering `$100` at maturity plus higher-compounded coupons (`$191.16` total, about `6.7%/yr`).
- **Answer:** `(a) Only Investor A (2-year horizon)`.
- **The trap:** Picking `(c)` from assuming rising rates hurt every bondholder, `(b)` from thinking a longer stay increases damage, or `(d)` from thinking holding a 6% bond always locks in 6%.
- **Rule:** Rising interest rates hurt investors with short holding periods (price risk dominates) and help investors who hold coupon bonds to maturity (reinvestment gains dominate).

**Q32.**
- **Why:** 1. A call option gives the issuer the *right*—not the obligation—to buy the bond back at `$100`. 2. When market yields jump from 5% to 8%, the issuer enjoys cheap 5% borrowing and will never voluntarily repay it to refinance at 8%. 3. By the callable bond mechanism, the call option becomes irrelevant when rates rise, so Bond B drops sharply (near `$79.87`), just like Bond A.
- **Answer:** `(c) It falls sharply, nearly as much as Bond A, because the issuer has no reason to call it`.
- **The trap:** Picking `(a)` or `(b)` from confusing a call price (a ceiling when rates fall) with a buyer's put price (a floor when rates rise), or `(d)` from expecting extra issuer payments.
- **Rule:** A call feature caps upside when rates fall, but offers no protection on the downside when rates rise.

**Q33.**
- **Why:** 1. Because the bond just reset yesterday, Year 1's coupon is locked at `$4`, while from Year 2 onward the coupon will reset to the new 8% market rate. 2. By the floating-rate bond mechanism, at the end of Year 1 (right after paying `$4`) the bond will reset to 8% and trade at `$100`. 3. Today's price is therefore the present value of `$104` received in one year at 8%: `$104 / 1.08 = $96.30`.
- **Answer:** `(b) $96.30`.
- **The trap:** Picking `(a) $100.00` from thinking floaters never budge even between reset dates, `(c) $73.16` from pricing it like a 10-year fixed 4% bond, or `(d)` from reversing the direction.
- **Rule:** Between reset dates, a floating-rate bond behaves like a short-term fixed bond maturing at the next reset date.

**Q34.**
- **Why:** 1. By credit spreads versus benchmark rates, the corporate bond's total yield equals `benchmark rate + credit spread`. 2. Last week's yield was `4% + 4% = 8%`. This week's yield is `4.5% + 2.5% = 7%`. 3. Because the 1.5-point spread narrowing more than offsets the 0.5-point benchmark rise, total yield fell by 1 point and the bond's price rises (e.g., to `$104.10` on an 8% coupon bond).
- **Answer:** `(d) It rises, because the bond's total yield fell from 8% to 7%`.
- **The trap:** Picking `(a)` from watching only the government rate, `(b)` from assuming a lower credit spread hurts existing bond prices, or `(c)` from assuming corporate yields ignore government rates.
- **Rule:** A corporate bond's price rises whenever a narrowing credit spread outweighs a rise in the benchmark rate, lowering its total yield.

**Q35.**
- **Why:** 1. By non-parallel yield curve shifts, each zero-coupon bond is discounted solely by the market yield matching its own maturity. 2. Bond A's 2-year yield fell by 0.5 points, so Bond A's price rises. 3. Bond B's 10-year yield rose by 0.5 points, so Bond B's price falls.
- **Answer:** `(a) Bond A rises; Bond B falls`.
- **The trap:** Picking `(c)` from averaging the two moves to zero, `(b)` from flipping the inverse price–yield rule, or `(d)` from assuming long-term rate increases drag short-term bond prices down too.
- **Rule:** When different maturities move in opposite directions, each bond's price responds to the yield move at its own maturity.

**Q36.**
- **Why:** 1. Modified duration approximates the curved price–yield line with a straight line that lies strictly *below* the true price curve everywhere away from the starting yield. 2. By convexity asymmetry, as yields climb, the bond's sensitivity shrinks, cushioning further losses. 3. At 8%, the actual price is `$71.19` (−28.8%), strictly higher than the linear estimate of `$64.00` (−36%).
- **Answer:** `(c) Higher than $64.00, because the actual loss is smaller than 36%`.
- **The trap:** Picking `(a)` or `(d)` from thinking convexity magnifies large moves in both directions, or `(b)` from treating duration as exact.
- **Rule:** Positive convexity helps the bondholder in both directions: linear duration underestimates prices after both large rate drops and large rate hikes.

**Q37.**
- **Why:** 1. At Year 0 (2 years left), the price was `$100 / 1.10^2 = $82.64`. 2. One year later with 1 year left and yields still 10%, present value discounting gives `$100 / 1.10 = $90.91`. 3. By pull to par, the price rose exactly 10% (`$82.64 × 1.10 = $90.91`), delivering the bond's 10% annual yield entirely through price appreciation.
- **Answer:** `$90.91`.
- **The trap:** Answering `$82.64` (thinking unchanged yields mean an unchanged price) or `$91.32` (averaging `$82.64` and `$100` linearly instead of compounding at 10%).
- **Rule:** When yields stay constant, a zero-coupon bond's price compounds upward at its yield each year as it pulls to par.

**Q38.**
- **Why:** 1. Steps 1 and 2 are right: `Δy = −0.004`, and by the modified duration approximation `%ΔP ≈ −5 × (−0.004) = +2%`. 2. Step 3 contains the error: a percentage price change applies to the bond's *current market price* (`$90`), not its `$100` face value. 3. Multiplying `+2% × $90.00 = +$1.80` gives an approximate new price of `$90.00 + $1.80 = $91.80`.
- **Answer:** `Step 3; $91.80`.
- **The trap:** Accepting Step 3 because face value is `$100` and easy to multiply by, overlooking that duration predicts percentage change from the current market price.
- **Rule:** Always apply a duration-estimated percentage change to the bond's current market price, never to its face value.

**Q39.**
- **Why:** 1. Both investments start at `$100` and have the same 5.0-year Macaulay duration, so both respond identically to tiny yield moves. 2. By cash-flow dispersion, Bond A concentrates 100% of its cash at Year 5 (minimum dispersion), whereas Bond B spreads payments across Years 1 through 6, giving Bond B higher convexity. 3. When yields plunge from 5% to 1%, Bond A grows +21.4% (`$121.43`) while Bond B grows +21.7% (`$121.66`).
- **Answer:** `(b) Bond B (6-year coupon bond), because its cash flows are more spread out in time`.
- **The trap:** Picking `(a)` from overgeneralizing "zero-coupon bonds move more" (true at equal *maturity*, not equal *duration*), `(c)` from assuming equal duration means equal returns on big shifts, or `(d)` from miscrediting discount pricing.
- **Rule:** At the same duration, a coupon bond with spread-out payments has higher convexity than a zero-coupon bond and outperforms on large parallel rate shifts.

**Q40.**
- **Why:** 1. Bond B holds back all `$100` of principal until Year 5, paying only `$5` per year along the way. 2. Loan A repays a large chunk of principal in every annual installment (`$23.10`/year), bringing its cash flows much closer to today. 3. By the coupon/cash-flow timing effect on price sensitivity, when yields rise from 5% to 7%, Bond B drops `−8.2%` (`$91.80`) while Loan A drops only `−5.3%` (`$94.70`).
- **Answer:** `(d) Bond B loses a larger percentage`.
- **The trap:** Picking `(b)` from thinking equal 5-year terms mean equal interest-rate risk, `(a)` from seeing Loan A's larger yearly payments, or `(c)` from assuming gradual repayment removes market-value risk completely.
- **Rule:** Returning principal earlier (as in an amortizing loan) shortens duration and lowers interest-rate sensitivity compared to a bullet bond of the same maturity.

**Q41.**
- **Why:** 1. Bond B trades at its `$100` face value, so its yield to maturity equals its coupon rate: `5.0%`. 2. By current yield versus yield to maturity, Bond A's low current yield (`$2 / $92 = 2.17%`) omits its `$8` price gain over 2 years (about `+$4/yr`, or over `4%/yr` extra). 3. Combined, Bond A's true yield to maturity is `6.39%`, beating Bond B's `5.0%`.
- **Answer:** `Bond A`.
- **The trap:** Picking `Bond B` by comparing only coupon rates (`5%` vs. `2%`) or current yields (`5.0%` vs. `2.17%`) and ignoring Bond A's capital gain to maturity.
- **Rule:** Always include the built-in capital gain or loss to maturity when comparing yields, not just the annual coupon.

**Q42.**
- **Why:** 1. Using `Price = $10 / Yield`: at 2%, price is `$500`; at 3%, price is `$333.33`, a drop of `$166.67 / $500 = 33.3%` (one-third). 2. At 10%, price is `$100`; at 11%, price is `$90.91`, a drop of `$9.09 / $100 = 9.1%` (one-eleventh). 3. By the starting yield level effect, adding 1 point to 2% is a 50% relative jump in yield, while adding 1 point to 10% is only a 10% relative jump.
- **Answer:** `33.3% (one-third) vs. 9.1% (one-eleventh)`.
- **The trap:** Expecting identical percentage drops because both rates rose by 1 percentage point, or thinking the higher yield creates the bigger drop.
- **Rule:** A fixed 1-percentage-point rate rise is a much larger proportional shock when starting yields are low, causing a far steeper percentage price drop.

**Q43.**
- **Why:** 1. Here the maturity effect (Bond B is 1 year longer) clashes with the coupon effect (Bond B pays huge 10% coupons early). 2. Bond A's cash arrives entirely at Year 6 (Macaulay duration = `6.00` years), while Bond B's heavy coupons pull its Macaulay duration down to `5.57` years. 3. When yields rise from 5% to 6%, Bond A drops `−5.5%` while Bond B drops `−5.1%`.
- **Answer:** `(a) Bond A (the 6-year zero-coupon bond)`.
- **The trap:** Picking `(b)` by relying blindly on maturity alone, `(c)` by guessing the two effects cancel, or `(d)` by assuming a premium price raises percentage sensitivity.
- **Rule:** Duration—not maturity alone—governs rate sensitivity, so a shorter zero-coupon bond can be more rate-sensitive than a longer high-coupon bond.

**Q44.**
- **Why:** 1. Normally, convexity makes gains on rate drops exceed losses on equal rate hikes. 2. Here, by the callable bond mechanism, when yields fall to 3% the issuer can redeem the bond at `$100`, capping the gain near `$0`. 3. When yields rise to 7%, the issuer leaves the bond outstanding and its price falls to `$85.95` (a `$14.05` loss)—creating *negative convexity*.
- **Answer:** `(c) The loss is much larger than the gain`.
- **The trap:** Picking `(a)` by applying standard convexity to a callable bond, `(b)` by assuming symmetry, or `(d)` by assuming the `$100` call price works as both ceiling and floor.
- **Rule:** A call option flips convexity negative near the call price: upside is capped when rates fall, while full downside remains when rates rise.

**Q45.**
- **Why:** 1. Two forces act over Year 1: inverse price–yield pushes the price *down* as yields rise from 10% to 12%, while pull to par pushes the price *up* as maturity shrinks from 2 years to 1 year. 2. With 1 year left at 12%, exact discounting gives `$100 / 1.12 = $89.29`. 3. Pull to par (`+10%` from time passing) easily outweighs the 1-year sensitivity to a `+2%` rate jump (`−1.8%`), leaving the price higher than `$82.64`.
- **Answer:** `Higher; $89.29`.
- **The trap:** Answering `Lower` by applying "higher yields mean lower prices" without accounting for the year of pull to par on a deep-discount bond.
- **Rule:** Over time, a discount bond's pull to par can outweigh a moderate rise in yields, leaving its market price higher than what you paid.

**Q46.**
- **Why:** 1. By reinvestment risk versus price risk, jumping yields from 6% to 8% lowers the bond's resale price at Year 6 (from `$100` to `$106 / 1.08 = $98.15`, a `$1.85` loss) while raising the compounded value of reinvested coupons (from `$41.85` to `$44.02`, a `$2.17` gain). 2. Because your 6-year horizon matches the bond's 5.9-year Macaulay duration, the two effects offset—leaving `$142.17`, slightly above your `$141.85` target.
- **Answer:** `(b) Roughly equal to (slightly above) your original 6% target`.
- **The trap:** Picking `(a)` by noticing only the immediate price drop, `(c)` by ignoring the lower Year 6 sale price, or `(d)` by forgetting reinvested coupons.
- **Rule:** Matching your holding horizon to a bond's Macaulay duration offsets price risk and reinvestment risk against parallel shifts in interest rates.

**Q47.**
- **Why:** 1. By real versus nominal yields and inflation, the nominal bond's cash flows are fixed in dollars and discounted at the nominal yield, which rose from 4% to 5.5%—so by the inverse price–yield rule, the nominal bond **falls**. 2. The inflation-linked bond adjusts its dollars for inflation and is priced off the *real* yield, which fell from 2% to 1.5%—so its price **rises**.
- **Answer:** `(d) Nominal bond falls; inflation-linked bond rises`.
- **The trap:** Picking `(a)` or `(b)` from assuming nominal and inflation-linked bonds always move together, or `(c)` from flipping the price–yield relationship.
- **Rule:** Nominal bonds react to nominal yields, whereas inflation-linked bonds react to real yields, so they can move in opposite directions when inflation expectations and real rates diverge.

**Q48.**
- **Why:** 1. Although the benchmark leg resets to the 1-year government rate (4%), by fixed cash flows the `2%` credit spread is locked in for all 5 years (`4% + 2% = 6%` total coupon). 2. By credit spreads versus benchmark rates, investors now demand `4% + 5% = 9%`, leaving a 3-point annual shortfall for 5 years. 3. That multi-year shortfall pushes the price sharply below `$100` (to about `$88.33`), despite the floating benchmark.
- **Answer:** `(a) It falls sharply well below $100`.
- **The trap:** Picking `(b)` or `(c)` from assuming a floating-rate bond resets its *entire* required yield, forgetting that only the benchmark rate floats while the contractual credit spread stays fixed.
- **Rule:** Floating-rate corporate bonds avoid benchmark interest-rate risk, but still drop like fixed-rate bonds when their issuer's credit spread widens.

**Q49.**
- **Why:** 1. By non-parallel yield curve shifts, each zero-coupon bond reacts only to its own maturity's yield change. 2. Using the modified duration approximation (`−maturity/(1+y) × Δy`): Bond A drops roughly `−(2/1.04) × 1.5% ≈ −2.9%` (exact: `−2.82%`), while Bond B drops roughly `−(10/1.04) × 0.2% ≈ −1.9%` (exact: `−1.90%`). 3. Bond A's 7.5-times-larger yield jump more than overcomes its 5-times-shorter duration.
- **Answer:** `(b) Bond A (2-year), because its much larger yield jump outweighs its shorter duration`.
- **The trap:** Picking `(a)` or `(d)` from assuming the longer-maturity bond always drops more regardless of how much each maturity's yield moved, or `(c)` from guessing they balance out.
- **Rule:** Actual price moves equal duration times *that maturity's* yield change, so a short bond can lose more than a long bond when short rates jump far more than long rates.

**Q50.**
- **Why:** 1. Modified duration is a straight-line approximation accurate only for small rate moves; for a huge 5-point jump, it predicts `−47.6%` (`$32.17`). 2. By convexity asymmetry, as yields climb from 5% toward 10%, the bond's modified duration continuously shrinks (from `9.52` down toward `9.09`), slowing the decline. 3. Exact discounting gives `$100 / 1.10^10 = $38.55` (`−37.2%`), well above `$32.17`.
- **Answer:** `(c) It is higher than $32.17, because convexity cushions large rate increases`.
- **The trap:** Picking `(a)` from thinking compounding makes big drops worse than linear duration, `(b)` from thinking duration is exact for zero-coupon bonds, or `(d)` from assuming doubling the yield halves the price.
- **Rule:** For large rate jumps, linear duration exaggerates the price drop because positive convexity reduces sensitivity as yields rise.

**Q51.**
- **Why:** 1. Both bonds start at `$100` (par) with 10-year maturities, but two mechanisms reinforce each other. 2. By the coupon effect, Bond A's lower 2% coupon pushes more value to Year 10 than Bond B's 8% coupon. 3. By the starting yield level effect, Bond A also starts at a much lower yield (2% vs. 8%). 4. After a 1-point hike, Bond A falls `−8.5%` (`$91.47`) versus Bond B's `−6.4%` (`$93.58`).
- **Answer:** `(a) Bond A (the 2% par bond)`.
- **The trap:** Picking `(c)` from assuming any two 10-year par bonds carry identical interest-rate risk, or `(b)`/`(d)` from thinking higher starting yields amplify rate losses.
- **Rule:** A low-coupon par bond issued in a low-rate environment is significantly more sensitive to rate hikes than a high-coupon par bond of the same maturity.

**Q52.**
- **Why:** 1. Two opposing forces act over Year 1: falling yields (4% to 3%) push the price *up* via the inverse price–yield rule, while losing one of the two above-market `$10` coupons pulls the price *down* via pull to par. 2. With 1 year left at 3%, exact pricing gives `($10 + $100) / 1.03 = $106.80`. 3. Pull to par overwhelms the 1-point rate drop, leaving the price lower than `$111.32`.
- **Answer:** `Lower; $106.80`.
- **The trap:** Answering `Higher` from assuming a drop in market yields must leave a bond's price above what you paid a year earlier.
- **Rule:** Over time, a steep premium bond's pull to par can outweigh a modest fall in interest rates, causing its price to drop even as yields fall.

**Q53.**
- **Why:** 1. By fixed cash flows, the bond repays `$100` at Year 2 regardless of interim market swings, giving a dollar profit of `$100 − $81 = $19`. 2. Because a zero-coupon bond pays no interim coupons, reinvestment risk is zero: interim rate swings cannot affect your final wealth if you hold to maturity. 3. By present value compounding, `(1 + r)^2 = 100 / 81`, so `1 + r = 10 / 9`, giving `r = 1/9 = 11.1%` per year.
- **Answer:** `$19 profit; 11.1% annualized return`.
- **The trap:** Claiming the return depends on the 2% and 15% swings (confusing coupon reinvestment risk with a zero-coupon bond) or dividing `$19 / $81 = 23.5%` by 2 to get `11.7%` (forgetting compounding).
- **Rule:** Held to maturity, a default-free zero-coupon bond locks in its exact purchase yield with zero reinvestment risk, no matter how wildly rates move in between.

**Q54.**
- **Why:** 1. By non-parallel yield curve shifts, Portfolio X's 10-year yield did not move, so Portfolio X stays at `$100.00`. 2. In Portfolio Y, the 2-year leg faces a `+1%` hike (`$50 × (1.05/1.06)^2 = $49.06`, a `$0.94` loss), while the 18-year leg gets a `−1%` cut (`$50 × (1.05/1.04)^18 = $59.40`, a `$9.40` gain). 3. By the maturity effect, the 18-year leg is roughly 9 times as sensitive as the 2-year leg, lifting Portfolio Y to `$108.46`.
- **Answer:** `(d) Portfolio Y (barbell), because the 18-year gain dwarfs the 2-year loss`.
- **The trap:** Picking `(b)` by thinking equal `+1%` and `−1%` shifts on equal `$50` legs cancel out, or `(a)`/`(c)` by overlooking how much more sensitive the 18-year bond is than the 2-year bond.
- **Rule:** Equal-sized opposite rate moves do not cancel in a barbell portfolio; the long-maturity leg dominates, so curve flattening strongly favors a barbell over a duration-matched bullet.

**Q55.**
- **Why:** 1. When yields stay flat at 5%, Bond A pays low coupons (`$2` per `$87.01` invested) while pull to par lifts its price from `$87.01` to `$89.36` (`+$2.35`). Total return: `($89.36 + $2) / $87.01 − 1 = +5.0%`. 2. Bond B pays high coupons (`$8` per `$112.99` invested) while pull to par lowers its price from `$112.99` to `$110.64` (`−$2.35`). Total return: `($110.64 + $8) / $112.99 − 1 = +5.0%`.
- **Answer:** `(c) Both earned the exact same 5.0% total return`.
- **The trap:** Picking `(a)` from thinking a premium bond's pull to par destroys return, or `(b)`/`(d)` from looking only at coupon rates while ignoring price convergence.
- **Rule:** At unchanged yields, every default-free bond priced to the same yield earns that exact yield as its total return—discount gains and premium losses simply balance the coupon differences.

**Q56.**
- **Why:** 1. By credit spreads versus benchmark rates, cutting the credit spread from 3% to 0.5% lowers both bonds' required total yield from 7% to 4.5%, even though government rates stayed flat. 2. Non-callable Bond A jumps to `$119.78`. 3. By the callable bond mechanism, the company can now refinance at 4.5% and call Bond B at `$101`, capping Bond B's price near `$101`.
- **Answer:** `(b) Bond A jumps sharply (near $120), while Bond B is capped near $101`.
- **The trap:** Picking `(a)` from watching only government rates, `(c)` from assuming calls are triggered only by central-bank rate cuts rather than credit upgrades, or `(d)` from ignoring the call cap.
- **Rule:** A call cap is triggered whenever the issuer's total borrowing yield falls below the bond's coupon—whether from lower benchmark rates or a narrower credit spread.

**Q57.**
- **Why:** 1. A perpetual bond pays `$5` every year starting in Year 1; at a 5% yield, its modified duration is simply `1 / y = 1 / 0.05 = 20` years, and rising yields from 5% to 6% cut its price from `$100` to `$5 / 0.06 = $83.33` (`−16.7%`). 2. Bond B pays nothing for 30 years (modified duration `30 / 1.05 = 28.6` years), so rising yields from 5% to 6% cut its price by `(1.05 / 1.06)^30 − 1 = −24.8%`.
- **Answer:** `(a) Bond B (30-year zero-coupon)`.
- **The trap:** Picking `(b)` from assuming infinite maturity means infinite rate sensitivity, `(c)` from lumping all long bonds together, or `(d)` from thinking endless coupons protect the price.
- **Rule:** Even an infinite-maturity coupon bond has finite duration (`1 / yield` at par), so a long zero-coupon bond can be more rate-sensitive than a perpetual bond.

**Q58.**
- **Why:** 1. Nominal yields jump from 4% to 7% solely because expected inflation rose (+3%), while real yields stayed at 2%. 2. Bond A's fixed nominal payments are discounted at 7%, dropping its price sharply to `$78.93`. 3. Bond B resets tomorrow to the new 7% nominal rate, staying at `$100`. 4. Bond C's principal adjusts with inflation while its real discount rate stays 2%, so it also stays at `$100`.
- **Answer:** `(d) Only Bond A`.
- **The trap:** Picking `(a)` from assuming a jump in nominal yields hits every bond, `(b)` from thinking inflation-linked bonds fall with nominal yields, or `(c)` from thinking 10-year floaters suffer 10-year rate losses.
- **Rule:** Pure inflation shocks hammer fixed-rate nominal bonds while leaving resetting floating-rate bonds and inflation-linked bonds largely intact.

**Q59.**
- **Why:** 1. Under Path 1 (holding the 3% bond and reinvesting coupons at 6%), `$3` coupons compound to `$39.54`, plus `$100` face value equals `$139.54`. 2. Under Path 2 (selling for `$77.92` and buying `$77.92` of a 6% par bond, reinvesting at 6%), `$77.92` compounds at 6% for 10 years: `$77.92 × 1.06^10 = $139.54`. 3. By present value discounting, `$77.92` is the exact value today of the old bond's cash flows at 6%, so holding and swapping produce identical wealth.
- **Answer:** `(c) Both paths end with the exact same dollar wealth ($139.54)`.
- **The trap:** Picking `(a)` from the common belief that "you haven't lost money unless you sell," `(b)` from forgetting you only have `$77.92` to invest at 6%, or `(d)` from omitting coupon reinvestment.
- **Rule:** Holding a depreciated bond to maturity does not erase an interest-rate loss—it simply converts the upfront price drop into lower annual coupons over the remaining life.

**Q60.**
- **Why:** 1. Yields plunge from 5% to 2% across all maturities, so prices rise unless limited by a bond's structure. 2. Bond D (10-year zero-coupon) has the longest duration (no early coupons), jumping `+33.6%`. 3. Bond A (10-year 5% non-callable) has interim coupons that shorten duration, jumping `+27.0%` (to `$126.95`). 4. Bond B (callable at `$102`) is capped near `$102` (`~+2%`). 5. Bond C (resetting floater) resets immediately to 2% and stays at `$100` (`0%`).
- **Answer:** `Bond D, Bond A, Bond B, Bond C`.
- **The trap:** Putting Bond A ahead of Bond D (thinking the higher coupon boosts gains), ignoring Bond B's `$102` call cap, or expecting Bond C to gain because it also matures in 10 years.
- **Rule:** When rates drop sharply, price gains are largest for long zero-coupon bonds, smaller for fixed coupon bonds, capped for callable bonds, and near zero for resetting floaters.
