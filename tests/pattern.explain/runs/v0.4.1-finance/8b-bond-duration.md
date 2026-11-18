# Bond Duration

By the end you will know what bond duration measures, how it is worked out, how to use it to estimate a price change, and why it is not the same as the time left on a bond.

## Why a bond's price moves at all

When interest rates rise, people who already own bonds lose money on paper, sometimes a lot of it. Some bonds barely move while others drop sharply, and anyone holding them wants to know in advance which kind they own. Bond duration is the number that answers that question. It sits on the oldest map in finance: comparing money today with money later through an interest rate.

A bond is a loan you make to a government or a company, written down as something you can buy and sell. You hand over money now, and the borrower promises a fixed schedule of payments back.

Most of those payments are regular interest. Each one is called a coupon, a name left over from the paper slips that holders once clipped off and handed in. In the example used throughout this piece, the bond pays a coupon of 40 every year.

At the end, the borrower also repays the amount the loan was written for. That amount is called the face value. Here it is 1,000, so the coupon of 40 works out to 4 percent of face value a year.

The date of that last repayment is the maturity. This bond matures in five years. So the whole promise is: 40 at the end of each of years one to four, and 1,040 at the end of year five.

That schedule never changes, but the bond's price in the market does. If new five-year loans start paying 5 percent, nobody will pay the full 1,000 for a bond that pays 4 percent. Its price has to fall until a buyer would earn about 5 percent by holding it. The yearly return a buyer locks in at today's price is called the yield. Price and yield move in opposite directions, like two ends of a seesaw: the yield rises because the price fell, and the price falls because the yield the market demands went up.

In the example, the market yield happens to be 4 percent, the same as the coupon, so the bond is priced at exactly 1,000. The question duration answers is how far that 1,000 will move when the yield moves away from 4 percent.

## Weighing time by money

You now hold a five-year bond paying 40 a year and 1,000 at the end, priced at 1,000 because the market yield is 4 percent. The next step is to see why some of those payments matter more to the price than others.

A payment that arrives later is worth less today, because money you hold now could be earning interest in the meantime. The amount today that is worth the same as a future payment is its present value. At 4 percent, 40 arriving in one year is worth 40 divided by 1.04, about 38.46. The same 40 arriving in two years is divided by 1.04 twice, giving about 36.98. Each year further out shrinks it again.

Do that for all five payments and you get roughly 38.46, 36.98, 35.56 and 34.19 for the four coupons, and 854.80 for the final 1,040. Those add up to 1,000, which is the bond's price. A bond's price is the sum of the present values of everything it will pay.

Now look at where the weight of that 1,000 sits. About 855 of it, more than 85 percent, comes from the payment in year five. Only about 145 comes from the earlier coupons. If you had to say when, on average, this bond pays you back, you would say "late, but a little before year five".

Duration turns that impression into a number. Take each payment's arrival time in years and weight it by that payment's share of the price. Year one gets a weight of 38.46 out of 1,000, year two gets 36.98 out of 1,000, and so on up to year five, which gets 854.80 out of 1,000. Multiply each time by its weight and add them up: about 0.04, plus 0.07, plus 0.11, plus 0.14, plus 4.27. The total is about 4.63 years.

That figure is called the Macaulay duration, after Frederick Macaulay, the economist who defined it in the 1930s. It is the average time until you are paid, where each payment counts in proportion to how much of today's price it supplies.

This is the place where most people go wrong with duration. Because it is measured in years, it is easy to read it as "how long until the bond ends". It is not. The bond matures in five years; its duration is 4.63. The gap comes from the coupons, which pull the average earlier. The bigger the coupons, the bigger the gap. A bond that pays no coupons at all, only 1,000 at the end, has nothing pulling the average forward, so its duration equals its maturity: exactly five years. For every bond that pays coupons, duration is shorter than maturity.

The same reasoning shows why yield matters too. A higher yield shrinks distant payments more than near ones, which shifts weight toward the early coupons and shortens duration a little. Duration is a property of the bond at its current price, and it drifts as the market moves.

An average time in years is useful, but it does not yet say how many units of currency you stand to lose, which is what the holder worried about rising rates wants to know.

## From years to a price change

The Macaulay duration of 4.63 years says where the weight of the bond's payments sits in time. A small adjustment turns it into a direct estimate of how the price reacts to a change in yield.

Divide the Macaulay duration by one plus the yield. For this bond that is 4.63 divided by 1.04, which gives about 4.45. This adjusted number is called the modified duration. Its meaning is practical: for a small change in yield, the bond's price changes by about the modified duration, as a percentage, for each percentage point the yield moves, in the opposite direction.

The division by 1.04 assumes the bond pays once a year. For bonds that pay twice a year, which is common for government bonds in several countries, the same step divides by one plus half the yearly yield. The idea is unchanged.

Run the example. Suppose the market yield jumps from 4 percent to 5 percent, a move of one percentage point. Modified duration of 4.45 predicts the price falls by about 4.45 percent, from 1,000 to about 955.50.

Traders usually measure rate changes in smaller steps. One hundredth of a percentage point is called a basis point, so the move from 4 to 5 percent is 100 basis points. Scaled down, each basis point rise in yield costs this bond about 0.0445 percent of its price, roughly 45 cents on a 1,000 bond. That sounds tiny, but rates can move by 10 or 20 basis points in a single day.

Now compare bonds. A five-year bond with no coupons has a Macaulay duration of 5 years and a modified duration of about 4.81 at a 4 percent yield, so it falls a little more than the coupon bond for the same move. A thirty-year bond paying 4 percent has a modified duration of roughly 17. The same one-point rise would cut its price by around 17 percent. That is the answer to the question from the start: the bonds that drop sharply are the ones with long duration, and you can see it in a single figure before rates move at all.

The same logic adds up across holdings. The duration of a portfolio is, to a close approximation, the average of its bonds' durations weighted by how much money sits in each. A fund that reports a duration of 6 is telling you that a one-point rise in yields would take roughly 6 percent off its value.

The estimate of 955.50 is close, but it is not what the bond would actually be worth at 5 percent.

## Where the estimate bends

You can now turn a bond's duration into a predicted price change: 4.45 percent for each percentage point of yield, in the opposite direction. Checking that prediction against the real price shows what duration leaves out.

Work out the bond's price properly at a 5 percent yield, by taking the present value of each payment at 5 percent instead of 4. The result is about 956.71, not 955.50. The real fall is about 4.33 percent, a little smaller than duration predicted.

Try the other direction. If the yield drops to 3 percent, duration predicts a rise of 4.45 percent, to about 1,044.50. The real price is about 1,045.80, a rise of about 4.58 percent. Here the real gain is a little larger than predicted.

So in both directions the real outcome is better for the holder than the duration estimate. The reason is that the true relationship between price and yield is a curve, not a straight line. Duration is the slope of that curve at the current yield: it draws a straight line touching the curve at one point. Near that point, the line and the curve agree closely. Further away, the curve bends upward above the line, so prices fall less and rise more than the line suggests. That bending is called convexity.

For small moves, such as a few basis points or even half a percentage point, the duration estimate is good enough for most purposes. For large moves, or for long bonds where the curve bends more, people add a convexity correction on top.

Duration also rests on a quieter assumption. The calculation uses one yield for every payment, and the estimate treats a rate change as all yields moving up or down by the same amount together. In real markets, short-term and long-term rates often move by different amounts. When they do, a single duration figure can misstate the risk, and that is where the more detailed measures in the closing list come in.

One more limit matters for some bonds. The calculation assumes the payment schedule is fixed. Some bonds let the borrower repay early, which tends to happen when rates fall. For those, the schedule itself depends on rates, and the plain duration calculation overstates how much the price will rise.

## The whole picture

A bond is a fixed schedule of coupons and a final repayment of face value, and its price is the sum of the present values of those payments at the market yield. Because later payments are discounted more heavily, a change in yield hits them harder, so a bond whose value sits mostly in distant payments is more sensitive to rates. Macaulay duration measures exactly that: the average time to payment, weighted by each payment's share of the price, which is why it is shorter than maturity whenever coupons are paid. Dividing it by one plus the yield gives modified duration, the percentage price change for a one-point change in yield, so the five-year 4 percent bond at 4.63 years moves about 4.45 percent per point. That estimate is a straight-line approximation of a curved relationship, accurate for small, even shifts in rates and progressively less so for large or uneven ones.

## Going further

- **DV01**: the change in a bond's price, in currency, for a one basis point move in yield; traders use it to size and hedge positions.
- **Convexity**: the measure of how much the price-yield curve bends, used to correct the duration estimate for larger rate moves.
- **Effective duration**: a version worked out by repricing the bond at slightly higher and lower yields, used for bonds whose payments can change, such as callable bonds.
- **Key rate duration**: a set of sensitivities to rates at individual maturities, used when short and long rates do not move together.
