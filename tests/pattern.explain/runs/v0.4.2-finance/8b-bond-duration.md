# Bond Duration

By the end you will know what bond duration measures, why a single number in years can tell you how far a bond's price moves when interest rates change, and where that number starts to mislead.

## Why bond prices move at all

A bond is a loan you make to a government or a company. You hand over money now, and in return the borrower promises a fixed schedule of payments. Take one concrete bond and keep it in mind throughout: you pay 1,000 dollars for a bond from a company that promises you 50 dollars a year for five years, and then your 1,000 dollars back at the end.

The 50 dollars paid each year is called the coupon. Here it is 5 percent of the amount lent, so this is a 5 percent coupon bond.

The 1,000 dollars returned at the end is called the face value. It is the sum the borrower owes back, and the coupon is quoted as a percentage of it.

The date of that final repayment, five years from now, is called the maturity.

None of these numbers ever change once the bond is issued. That is the point of a bond: the payments are fixed. What does change is what other people will pay you for it. Suppose that the day after you buy, interest rates rise, and companies like yours now have to offer 6 percent to borrow. A new buyer can get 60 dollars a year for their 1,000. Nobody will pay you 1,000 for a bond that pays only 50, so if you want to sell, you must accept less. Your bond's price has fallen, even though the company is just as reliable as before.

This exposure is called interest rate risk: the price of a bond you already hold moves when market rates move. Bonds with different coupons and maturities move by very different amounts for the same change in rates. Duration is the number that tells you how much a given bond will move, and to see where it comes from you first need a way to turn a schedule of future payments into a price today.

## Turning future payments into a price today

You hold a bond that pays 50 dollars a year for five years plus 1,000 at the end, and you have seen that its price falls when rates rise. The question is by how much, which starts with how a price is worked out in the first place.

A dollar paid next year is worth less than a dollar today, because a dollar today can be invested and earn interest in the meantime. If you can earn 5 percent, then 47.62 dollars today grows to 50 dollars in a year. So, at 5 percent, a promise of 50 dollars next year is worth 47.62 dollars now. That figure is the payment's present value: the amount today that is worth the same as a future payment once interest is taken into account. A payment further away is discounted more, because it is divided by 1.05 once for every year of waiting.

Apply that to every payment of your bond at 5 percent and you get five present values. The first coupon is worth 47.62 today, the second 45.35, the third 43.19, the fourth 41.14, and the final payment of 1,050 dollars, which is the last coupon plus the face value, is worth 822.70. Added together they come to 1,000 dollars, exactly what you paid.

The rate used for that discounting has a name. A bond's yield is the single annual rate that, when used to discount all of its payments, gives the bond's current market price. Your bond, bought for 1,000, has a yield of 5 percent, the same as its coupon. Once it trades at a different price, its yield and its coupon part ways.

Now redo the sum at 6 percent, the new market rate. Every payment is divided by 1.06 per year instead of 1.05, so each present value shrinks, and the total comes to 957.88 dollars. That is the new price. This is why bond prices and yields always move in opposite directions: a higher yield means heavier discounting of the same fixed payments, and so a lower price. The two are one fact seen from two sides, and it helps to treat "yields rose" and "prices fell" as the same news.

Look again at those five present values. More than four fifths of the bond's value, 822.70 of the 1,000, sits in the final payment. Which raises a natural question: on average, when does this bond actually pay you back?

## Duration as an average time

You can now price a bond by discounting each payment, and you have seen that your five-year bond's value is heavily concentrated in its last payment. Duration starts from that observation.

Take each payment's present value as a share of the price. The first coupon is 4.8 percent of the bond's value, the second 4.5 percent, the third 4.3 percent, the fourth 4.1 percent, and the final payment 82.3 percent. Now take the average of the payment dates, one to five years, with each date weighted by its share. The early coupons pull the average a little towards the present, the big final payment pulls it strongly towards year five, and the result is 4.55 years.

That weighted average time is called the Macaulay duration, named after the economist who described it in the 1930s. It is measured in years, and it answers the question at the end of the last section: in present-value terms, your bond pays you back, on average, about four and a half years from now.

A useful picture is a seesaw laid along a timeline. Put each payment's present value on it as a weight at its year, a small weight at each of years one to four and a heavy one at year five. The point where the seesaw balances is the Macaulay duration. The picture holds for a fixed yield; it stops being true once yields move, because the weights themselves change, which is why duration has to be recalculated as rates change.

This is where the most common misunderstanding arises. Because duration is measured in years, people often take it to be the same as maturity, or a fancier word for it. It is not. Your bond matures in five years but has a duration of 4.55, because the coupons return part of your money before the end. Only a bond with no coupons, which pays everything in one sum at maturity, has a duration equal to its maturity: all the weight sits at one point, so that is where the seesaw balances. Every coupon bond has a duration shorter than its maturity, and the gap grows with the coupon and with the length of the bond. A 30-year bond with a 5 percent coupon, priced at a 5 percent yield, has a duration of only about 16 years.

So duration is an average time to repayment. Why should an average time tell you anything about how much a price drops when rates rise?

## Duration as a measure of price sensitivity

You now hold two things: a bond's price is the sum of its discounted payments, and its Macaulay duration is the average time of those payments, weighted by their present values. The link between them is that distant payments are hit harder by a rise in rates.

Go back to the move from 5 to 6 percent and watch each payment separately. The first coupon's present value falls from 47.62 to 47.17 dollars, a loss of about 1 percent, because it is discounted for only one year. The final payment falls from 822.70 to 784.62 dollars, a loss of about 4.6 percent, because the extra discounting compounds over five years. Roughly, each payment loses a percentage equal to its time in years multiplied by the change in yield, scaled down slightly by dividing by one plus the yield.

Average that effect over all the payments, weighting each by its share of the price, and you get the bond's overall sensitivity. The averaging is the same one that produced the Macaulay duration, so the sensitivity comes out as the Macaulay duration divided by one plus the yield. For your bond that is 4.55 divided by 1.05, which is 4.33.

That figure is called the modified duration. It turns duration from a time into a rule of thumb about price: the percentage change in a bond's price is roughly the modified duration multiplied by the change in yield in percentage points, with the sign flipped. For your bond, a one-point rise in yield means a fall of about 4.33 percent, or about 43 dollars on 1,000. A one-point fall means a rise of about the same amount. A bond with twice the modified duration would move about twice as far.

When traders and fund managers say "duration" without a qualifier, they usually mean modified duration, and they read it as a sensitivity rather than as a time. The two numbers are close for ordinary yields, 4.55 against 4.33 here, so which one is meant changes the arithmetic only a little, but it is worth asking when precision matters.

The rule gives a quick estimate of 43 dollars for a one-point move. How close is that to what actually happens?

## Where the estimate stops working

So far you have seen that modified duration predicts your bond should lose about 4.33 percent, or 43.29 dollars, when its yield rises by one percentage point. Now check that against the real repricing.

You already know the actual price at 6 percent: 957.88 dollars, a fall of 42.12. The estimate overstated the loss by a little over a dollar. Run the yield the other way, down to 4 percent, and the real price comes out at 1,044.52, a gain of 44.52, while the estimate again says 43.29. So the estimate is too pessimistic in both directions: the real bond loses a bit less than predicted when yields rise and gains a bit more when they fall.

The reason is that duration treats the link between price and yield as a straight line, while the real link is a curve that bends upwards. For small moves the line and the curve sit almost on top of each other, which is why duration works well for everyday changes of a fraction of a point. For large moves the gap widens. That bend is called convexity, and for ordinary bonds like yours it works in the holder's favour. Practitioners add a convexity correction when they need accuracy over bigger moves.

There is a second limit, built into the calculation itself. Your bond's duration was worked out with one yield applied to every payment, and the rule assumes that yield moves by the same amount for the one-year payment as for the five-year one. Real markets often move short and long rates by different amounts, so that a bond's actual price change can differ from what its single duration figure predicts. Duration is most reliable when rates across all maturities move roughly together.

A third limit follows from the first two: duration is a snapshot. It changes as yields change, and it shortens as the bond ages and payments are made, so a figure computed today describes today's sensitivity, not next year's.

## The whole picture

A bond's payments are fixed, so its price can move only through the rate used to discount them, and every rise in that yield lowers the present value of each payment, the distant ones most. Macaulay duration averages the timing of those payments, weighted by how much of the price each one carries, so it measures in years how far away the bond's value sits. Because a payment's sensitivity to rates grows with its distance in time, that same average, divided by one plus the yield, becomes modified duration: the approximate percentage a bond's price moves for each percentage point change in its yield. It is a straight-line estimate of a curved relationship, built on a single yield moving evenly, so it is sharp for small moves and drifts for large ones, where convexity takes over.

## Going further

Effective duration: a version computed by repricing the bond at slightly higher and lower yields, used for bonds whose payments change when rates move, such as bonds the issuer can repay early.

DV01: the dollar change in a bond's price for a one basis point change in yield, where a basis point is 0.01 percentage points.

Immunisation: matching the duration of assets to the timing of future liabilities, so that a rate change affects both sides by roughly the same amount, as pension funds and insurers commonly aim to do.

Key rate duration: a set of sensitivities, one for each point along the range of maturities, that captures how a bond responds when short and long rates move by different amounts.
