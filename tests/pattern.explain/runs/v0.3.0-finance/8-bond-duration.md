# Bond Duration

By the end you will know what bond duration measures, how it is calculated, how to use it to estimate what a change in interest rates does to a bond's price, and where that estimate goes wrong.

## Why rates move bond prices

A bond is a loan you make to a government or a company, packaged so it can be bought and sold. In return, the borrower promises a fixed schedule of payments. Take one bond and carry it through this whole piece: it has a face value of 1,000 dollars, which is the amount repaid at the end, and it matures in five years. Every year until then it pays 4 percent of the face value, 40 dollars. Those yearly payments are called coupons.

The schedule is fixed the day the bond is issued, but the rest of the world keeps moving. Suppose you bought this bond for 1,000 dollars, and a month later new five-year bonds start paying 5 percent. Nobody will now pay you 1,000 dollars for a bond that pays 40 a year when 50 a year is on offer. To sell, you have to accept a lower price.

The way markets settle that lower price rests on present value: the amount of money today that is worth the same as a payment in the future, once interest is taken into account. If you can earn 5 percent a year, then 1,000 dollars in five years is worth about 784 dollars today, because 784 dollars growing at 5 percent a year for five years reaches 1,000. A bond's fair price is the present value of all its remaining payments, added up.

The interest rate used to discount those payments is the bond's yield, the yearly return a buyer gets if they pay today's price and hold the bond to the end. When the yield goes up, every future payment is discounted more heavily, so the price goes down. When the yield goes down, the price goes up. Price and yield always move in opposite directions. People who are new to bonds often expect a higher yield to be good news for someone already holding the bond; for that holder, it means the bond they own just lost value.

Our bond, priced at a 4 percent yield, is worth exactly 1,000 dollars. At a 5 percent yield the same sums give about 956.71 dollars. At 3 percent, about 1,045.80. So the direction is clear. The question a bond investor actually lives with is the size: if rates rise by one percentage point, how much do I lose? Different bonds answer that very differently, and you need a single number that tells them apart.

## Weighing payments by time

You now hold two facts: a bond's price is the sum of its discounted payments, and a rise in yield shrinks that sum. The size of the shrinkage depends on when the money arrives.

A payment due next year barely changes when the yield moves, because it is discounted for only one year. A payment due in five years is discounted five times over, so a change in the yield compounds across all five years and hits it much harder. A bond whose money mostly arrives late is therefore more sensitive to rates than one whose money mostly arrives early.

That suggests a measure: the average time until you get your money, where each payment counts in proportion to how much of the bond's value it represents. This weighted average is called Macaulay duration, after the economist Frederick Macaulay, who described it in 1938. It is measured in years.

Here is how it works out for our bond at a 4 percent yield. Walk through the five payments and find each one's present value.

1. The first coupon of 40 dollars, one year away, is worth about 38.46 dollars today.
2. The second, two years away, is worth about 36.98.
3. The third, about 35.56.
4. The fourth, about 34.19.
5. The final payment is the last coupon plus the face value, 1,040 dollars in five years, worth about 854.80 today.

Those add up to 1,000 dollars, the price. Now multiply each present value by the number of years until it arrives: 38.46 times 1, 36.98 times 2, and so on up to 854.80 times 5. The total is about 4,630. Divide by the price of 1,000 and you get a Macaulay duration of about 4.63 years.

This is the place where most people's picture of duration goes wrong. The common belief is that duration is another name for how long the bond lasts. It is not. Our bond matures in five years, but its duration is 4.63, because the coupons pull some of the value earlier. The final payment dominates, which is why the figure sits close to five, but every coupon received along the way drags it down a little.

The only bond whose duration equals its maturity is one that pays no coupons at all, a zero-coupon bond, which pays a single lump sum at the end. A five-year zero-coupon bond has a duration of exactly five years, since all of its value arrives at year five. Any bond that pays coupons has a duration shorter than its maturity, and the higher the coupon, the shorter the duration. Two bonds that both mature in 2031 can therefore have quite different durations and quite different sensitivity to rates.

## From years to a price change

You now have Macaulay duration: a weighted average time to receive a bond's money, 4.63 years for our bond. What an investor wants, though, is a percentage: how much the price moves when the yield moves.

A small adjustment turns one into the other. Divide Macaulay duration by one plus the yield, and you get modified duration, which reads directly as price sensitivity. For our bond, 4.63 divided by 1.04 is about 4.45. This calculation assumes one coupon a year; for bonds that pay twice a year, the yield used in the adjustment is the half-year rate, and market data providers state which convention they follow.

Modified duration is read like this: for each one percentage point change in yield, the bond's price moves by about that many percent, in the opposite direction. Our bond's modified duration of 4.45 says that if its yield rises from 4 to 5 percent, the price should fall by about 4.45 percent, from 1,000 to roughly 955.50 dollars. If the yield falls to 3 percent, the price should rise by about 4.45 percent, to roughly 1,044.50.

Rate changes are usually talked about in smaller steps. Traders measure them in basis points, where one basis point is one hundredth of a percentage point, so a move from 4.00 to 4.25 percent is 25 basis points. Duration scales down cleanly to these steps: a 25 basis point rise would cost our bond about a quarter of 4.45 percent, roughly 1.1 percent, or about 11 dollars per bond.

This is why duration is the first number many fund managers and analysts look at. A bond fund that reports an average duration of six is telling you that a one point rise in rates across the board would cut its value by roughly six percent. A fund with a duration of two would lose roughly two percent from the same move. The figure reduces a whole portfolio's exposure to interest rates to one comparable number. What you do with that number depends on how long you plan to hold, what you expect rates to do, and how much of a fall you can sit through; duration describes the exposure, it does not make that choice for you.

Duration also gives a way to understand holding a bond to the end. If you hold our bond for its full five years, price swings in between do not change the 1,000 dollars you get back at maturity. Duration measures what happens to the bond's market value if you need to sell, or if you are judged on that value along the way.

The estimate is good, but our earlier exact prices do not match it perfectly, and the gap tells you something about the shape of the relationship.

## Where the straight line bends

So far you have a single number, modified duration, that turns a change in yield into a change in price: 4.45 percent per percentage point for our bond. That number treats the relationship as a straight line, the same percentage for every step. The real relationship is not straight.

Compare the estimates with the exact prices worked out at the start. At a 5 percent yield, duration predicted 955.50 dollars; the true price is 956.71. The bond fell by less than predicted. At a 3 percent yield, duration predicted 1,044.50; the true price is 1,045.80. The bond rose by more than predicted. In both directions, the real bond did better than the straight-line estimate.

The reason is that duration itself changes as the yield changes. When the yield rises, the distant payments shrink in present value more than the near ones, so the near ones carry more of the weight, and the duration gets shorter. The bond becomes less sensitive as it falls. When the yield drops, the opposite happens and the bond becomes more sensitive as it rises. Plotted out, price against yield is a curve that bows outward, and this bowing is called convexity.

For a small move, such as 10 or 25 basis points, the curve and the straight line are almost the same, and duration alone is accurate enough for most purposes. For large moves, the error grows: for long-dated bonds, whose durations can exceed 15 or 20, a two or three point change in rates makes the straight-line estimate visibly off. Analysts then add a convexity correction on top of duration to get closer to the true price.

One more assumption carries much of the weight. The standard calculation treats the yield as a single number that moves all at once. In practice, rates for one year, five years and thirty years do not always move together, and a bond's price responds to the whole set. Duration as described here measures sensitivity to a parallel shift, where every rate moves by the same amount, and is less reliable when short and long rates move differently.

## The whole picture

A bond's price is the present value of its fixed future payments, so when yields rise its price falls, and the question is by how much. Payments far in the future are hit hardest, so the right measure is the value-weighted average time to receive the bond's money, Macaulay duration, which is shorter than maturity for any bond that pays coupons. Dividing it by one plus the yield gives modified duration, the approximate percentage price change for a one point move in yield, which is the number used to compare and manage interest rate exposure. That approximation is a straight line laid along a curve, so it is accurate for small moves and drifts for large ones, where convexity accounts for the difference.

## Going further

Effective duration: a version computed by repricing the bond under shifted rates, used for bonds whose payments can change, such as callable bonds and mortgage-backed securities.

DV01: the dollar change in a bond's price for a one basis point move in yield, often used by traders instead of a percentage.

Key rate duration: a set of durations, one for each point along the range of maturities, which measures sensitivity when short and long rates move by different amounts.

Convexity adjustment: the second term added to the duration estimate to correct for the curve in the price and yield relationship.
