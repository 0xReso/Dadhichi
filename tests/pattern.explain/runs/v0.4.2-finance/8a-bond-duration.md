# Bond Duration

By the end you will know what a bond's duration measures, how it is worked out, and how to use it to estimate what a change in interest rates does to a bond's price.

## When rates rise, old bonds lose value

Suppose you lend a company 1,000 and in return it promises you a fixed series of payments over the next five years. A loan like this, written up as a piece of paper that can be bought and sold, is a bond. You can keep it to the end, or sell it to someone else along the way, and the price you get for it on any given day is set by the market rather than by the company.

The amount the company promises to hand back at the end is the bond's face value. For your bond it is 1,000.

Until then, the company also pays you interest each year at a fixed rate written into the bond. These yearly interest payments are called coupons. Your bond has a 5% coupon, so it pays 50 a year.

The date the face value comes back is the bond's maturity. Your bond matures in five years, so you receive 50 at the end of years one, two, three and four, and 1,050 at the end of year five: the last coupon plus the face value.

Now the trouble. Suppose that the day after you buy, rates in the market rise, so that new five-year bonds from similar companies pay 6%. Nobody will pay 1,000 for your bond, which pays 50 a year, when 1,000 elsewhere buys 60 a year. To sell, you would have to accept a lower price, low enough that the buyer still ends up earning 6% a year.

That rate a buyer earns, if they pay today's price and hold the bond until maturity, is the bond's yield. Yield and price move in opposite directions: when the yield the market demands goes up, the price of an existing bond goes down, and when it falls, the price goes up. This is the pair most often muddled, so it is worth holding firmly: a bond's coupon is fixed, and its price is what adjusts.

The risk that your bond loses value because rates rise is called interest rate risk. A natural first guess is that it grows with maturity, since a 30-year bond leaves you stuck at the old rate for longer than a 5-year one. That guess points the right way but is too coarse, because two bonds with the same maturity can react quite differently to the same change in rates. So how much does your bond's price actually fall, and what decides the size of the fall?

## Pricing a bond as a stack of payments

You now hold a bond that pays 50 a year for four years and 1,050 in year five, and you know its price falls when yields rise. To see by how much, you need the way a bond's price is worked out, which goes one payment at a time.

A payment due later is worth less than the same payment today, because money in hand now could be earning interest in the meantime. The amount you would need to invest today, at the bond's yield, to grow into a future payment is called that payment's present value. At 5%, the 50 due in one year has a present value of about 47.62, because 47.62 plus 5% interest comes to 50.

For a payment further away, the interest compounds: each year's interest itself earns interest the following year. So to find the present value you divide by 1.05 once for every year of waiting. Working backwards from a future payment to its present value this way is called discounting. Discounted at 5%, the 50 due in year two is worth 45.35 today, the 50 in year three 43.19, the 50 in year four 41.14, and the 1,050 in year five 822.70.

Add those five present values together and you get 1,000. That is the rule for pricing any plain bond: its price is the sum of the present values of all its remaining payments, discounted at its yield. Your bond comes out at exactly its face value because its coupon and its yield are both 5%; whenever those two match, the price equals the face value.

Now apply the market's new demand of 6% by dividing by 1.06 for each year instead of 1.05. The five present values become 47.17, 44.50, 41.98, 39.61 and 784.62, and they add up to 957.88. Your bond has lost 42.12, a little over 4.2% of its value, from a one-point rise in yield.

Look at where that loss came from. The payment in year one lost less than half a unit of value, going from 47.62 to 47.17. The final payment lost about 38, going from 822.70 to 784.62. A distant payment is discounted over more years, so a change in the rate compounds over more years and hits it harder. On top of that, the final payment carries most of the bond's value, so the hardest-hit payment is also the biggest one.

So a bond's sensitivity depends on how far away in time its value sits. How do you put one number on that?

## Duration as the bond's balance point

A bond's price is the sum of its discounted payments, and a rise in yield hurts the distant payments most. What matters, then, is where in time the bond's value is concentrated.

Take each payment's present value as a share of the bond's price of 1,000. The year-one payment is 4.8% of the value, year two 4.5%, year three 4.3%, year four 4.1%, and year five 82.3%. Multiply each year number by its share and add the results: one times 4.8%, plus two times 4.5%, and so on up to five times 82.3%. The total comes to about 4.55 years.

That figure, the average time until each unit of the bond's present value arrives, weighted by how much value arrives when, is the bond's Macaulay duration, named after the economist Frederick Macaulay, who set it out in 1938.

A picture that carries the real arithmetic: lay a plank along a timeline from year zero to year five, and stand a weight on it at each payment date, sized by that payment's present value. Four small weights sit at years one to four and one large weight at year five. The point where the plank balances is at 4.55 years. The picture stops being accurate the moment yields change, because the weights are present values and every one of them shifts when the yield does, which moves the balance point too.

Here is where most people go wrong. Duration is not the bond's maturity, and it is not the date you get your money back. Your money arrives at years one through five; 4.55 years is a summary of that spread, and it falls short of maturity because the coupons pull value earlier.

Duration equals maturity in one case: a bond with a single payment at the end. Such a bond pays no coupons at all; it is sold below its face value and pays the full face value at maturity, and it is called a zero-coupon bond. A five-year zero-coupon bond yielding 5% would cost about 783.53 today and has a duration of exactly five years, because all of its value sits at year five.

That difference shows up in price. If the zero-coupon bond's yield rises from 5% to 6%, its price falls to about 747.26, a drop of around 4.6%, against 4.2% for your coupon bond. Same maturity, same move in rates, noticeably different loss. The general pattern is that a higher coupon moves value earlier and shortens duration, and a lower coupon lengthens it.

Duration in years is a measure of time, though, and the original worry was money. How does one turn into the other?

## From years to a price estimate

Your bond has a duration of 4.55 years, the balance point of its value in time, and you have seen that the further out that balance point sits, the more the price suffers when yields rise. One small adjustment turns that time into a direct estimate of price change.

Divide the Macaulay duration by one plus the yield: 4.55 divided by 1.05 gives about 4.33. This adjusted figure is the modified duration, and it reads directly as a percentage. For every one percentage point rise in yield, the bond's price falls by about 4.33%; for every point of fall, it rises by about the same. That division assumes one payment a year, as your bond has; for bonds that pay twice a year, the yield is split across the two periods in the calculation.

Test it against what you worked out by hand. A one-point rise should cost about 4.33% of 1,000, which is 43.29, giving a price near 956.71. The full calculation gave 957.88. The estimate is off by just over one unit, close enough for most purposes, and it took a single multiplication instead of five discounting sums.

Real rate moves are usually smaller than a full point. Traders measure them in basis points, where one basis point is one hundredth of a percentage point. A 25 basis point rise, a quarter of a point, would on this estimate cost your bond about 1.08%, or roughly 10.82.

The estimate has limits, and they are part of how it works. Try a fall in yield from 5% to 4%. Modified duration predicts a gain of 43.29, to 1,043.29. The full calculation gives 1,044.52. In both directions, the real price came out a little better than the estimate: it fell less than predicted when yields rose and rose more than predicted when they fell.

The reason is that the relationship between price and yield is a curve, not a straight line. Modified duration treats it as a straight line touching the curve at today's yield, which is accurate for small moves and drifts further off as the move grows. That bending of the curve is called convexity, and for plain bonds like yours it always works in the holder's favour.

Duration also rests on assumptions worth knowing. It is calculated at today's yield and changes as yields move and as the bond ages, so a figure from last year is stale. The simple version also treats every payment as discounted at the same yield and assumes that yield moves as one, whereas in practice short-term and long-term rates can move by different amounts. And it assumes the payments are fixed; a bond the issuer can repay early does not have fixed payments, and the calculation above does not apply to it as written.

Within those limits, duration is the everyday language of bond risk. A bond fund that reports a duration of six years is saying that a one-point rise in rates would cut its value by roughly 6%, and a fund's duration is the value-weighted average of the durations of the bonds it holds. Two funds with the same yield but different durations carry very different exposure to rate changes.

## The whole picture

A bond is a stack of future payments, and its price is the sum of what each payment is worth today once discounted at the bond's yield. When yields rise, every payment is discounted more heavily, and the distant ones suffer most because the extra discount compounds over more years. Duration puts a single number on where in time the bond's value sits: the weighted average arrival time of its value, 4.55 years for your five-year 5% bond. Divided by one plus the yield, it becomes modified duration, 4.33, which estimates the percentage price change for each point of yield change. It is not the same as maturity except for a zero-coupon bond, and it is a straight-line estimate of a curved relationship, accurate for small moves, slightly pessimistic for large ones, and only as good as its assumption that the payments are fixed and the yield moves as one.

## Going further

- Effective duration: a version measured by recalculating the price for small yield changes, used for bonds whose payments can change, such as those the issuer can repay early.
- DV01: the change in a bond's price, in money, for a one basis point move in yield, often used by traders instead of a percentage.
- Key rate duration: a set of durations that measures sensitivity to rates at particular maturities separately, for when short and long rates move by different amounts.
- Immunisation: matching the duration of assets to the timing of future obligations so that a rate change affects both sides roughly equally.
