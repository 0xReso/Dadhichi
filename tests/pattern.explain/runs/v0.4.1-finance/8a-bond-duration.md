# Bond Duration

By the end you will know what a bond's duration measures, how it is worked out from the bond's payments, how it turns a change in interest rates into a change in price, and why it is not the same thing as the time until the bond ends.

## The problem: rates move, and bond prices move with them

Suppose you own a bond and interest rates across the market rise by one percentage point overnight. Your bond is now worth less than it was yesterday. The question that matters is how much less, and the answer is different for different bonds. Duration is the number that answers it.

A bond is a loan you make by buying a piece of paper. A government or a company borrows money from you, and in return promises a fixed schedule of payments. You do not own part of the borrower, as you would with a share; you are a lender, and the bond is the record of the promise.

The running example in this piece is one such bond. You lend $1,000, and the borrower promises to give the $1,000 back after five years. That amount, the sum repaid at the end, is called the face value.

Along the way, the borrower also pays you $50 at the end of each year. These regular payments are called coupons, and this bond's coupon rate is 5 percent, because $50 is 5 percent of the $1,000 face value.

The date of the final payment, five years from now in the example, is called the maturity. On that date you receive the last $50 coupon and the $1,000 face value together, $1,050 in all, and the bond is finished.

Once a bond exists, it can be bought and sold between investors at whatever price the market sets. The return a buyer would earn by paying today's price and collecting every remaining payment, expressed as a yearly rate, is called the yield. When the bond's price equals its face value, the yield equals the coupon rate. In the example, you pay $1,000, collect 5 percent a year, and your yield is 5 percent.

Here is the relationship that drives everything else: when the price of a bond goes down, its yield goes up, and the reverse. The payments are fixed in the contract, so the only way a bond can offer a higher return to a new buyer is for its price to fall. If new bonds start paying 6 percent, nobody will pay $1,000 for your bond's 5 percent payments; its price has to drop until a buyer gets roughly 6 percent on what they pay. Price and yield always move in opposite directions.

So when rates rise, every bond paying fixed amounts loses value. But a bond that pays everything back next month barely notices, while one that pays back in thirty years can fall hard. What decides how far a given bond falls?

## When the money arrives, measured in years

You now hold a bond with a fixed list of payments, and you know its price falls when market yields rise. The size of that fall depends on how far into the future the bond's money sits, and duration is a precise way of measuring that distance.

To measure it, you need a way to compare payments that arrive at different times. Money received sooner is worth more than the same amount received later, because money in hand can earn interest in the meantime. The amount you would need today, invested at the bond's yield, to grow into a given future payment is called that payment's present value. At a 5 percent yield, $50 due in one year has a present value of about $47.62, because $47.62 earning 5 percent for a year becomes $50.

Applying this to each of the example bond's payments, at its 5 percent yield, gives these present values:

1. The $50 coupon in year one is worth about $47.62 today.
2. The $50 in year two is worth about $45.35.
3. The $50 in year three is worth about $43.19.
4. The $50 in year four is worth about $41.14.
5. The $1,050 in year five is worth about $822.70.

These add up to $1,000, which is the bond's price. That is no accident: a bond's price is the sum of the present values of all its remaining payments. Notice also where the value sits. More than four-fifths of it, the $822.70, is in the final payment.

Now take an average of the payment dates, one through five years, but weight each date by how much of the bond's value arrives on it. Year five counts for 822.70 out of 1,000, year one for only 47.62 out of 1,000, and so on. Multiply each year by its share and add them up, and the result is about 4.55 years. This weighted average time until you receive the bond's value is called Macaulay duration, after the economist Frederick Macaulay, who described it in 1938.

This is the point where most people get duration wrong. The bond matures in five years, yet its duration is 4.55 years. Duration is not the maturity under another name. The coupons pay part of your money back early, and each early payment pulls the average date closer to today. The bigger the coupons, the further duration falls below maturity.

The clearest case is a bond with no coupons at all, called a zero-coupon bond, which pays one lump sum at maturity. A five-year zero-coupon bond has a Macaulay duration of exactly five years, because all of its value arrives on one date. For every bond that pays coupons, duration is shorter than maturity.

You now have a number in years. But the opening question asked for a price change in dollars. How does an average date tell you how much a bond loses when rates rise?

## From years to a price change

You hold the example bond's Macaulay duration of 4.55 years: the value-weighted average time until its money arrives. The useful fact about that number is that it also measures how sensitive the price is to the yield, because a payment that sits further in the future has its present value shrink more when the yield rises.

To turn the duration into a price estimate, it gets one small adjustment: divide it by one plus the yield. For the example bond, 4.55 divided by 1.05 gives about 4.33. This adjusted figure is called modified duration, and it reads directly as a percentage: for each percentage point the yield rises, the price falls by about that many percent.

So if the market yield on bonds like yours rises from 5 percent to 6 percent, modified duration predicts that your bond falls by about 4.33 percent, roughly $43, to around $957. Working out the price exactly at a 6 percent yield gives $957.88, a fall of $42.12. The estimate is within about a dollar.

The same number works in the other direction. If yields fall from 5 to 4 percent, modified duration predicts a gain of about 4.33 percent, roughly $43.

Rate moves are usually smaller than a full percentage point, and traders measure them in basis points, where one basis point is one hundredth of a percentage point. A move of 25 basis points, a quarter of a point, would move the example bond by about a quarter of 4.33 percent, a little over 1 percent, or about $11.

This is why duration gets quoted so often. A bond fund that reports a duration of 7 is telling you that a one-point rise in rates would cut its value by roughly 7 percent, and a fund with a duration of 2 would lose roughly 2 percent. Two very different collections of bonds, with different coupons and maturities, are reduced to one comparable figure. That figure is, in effect, the bond's exposure to interest-rate risk.

It is worth being clear about what the years mean in this use. A duration of 7 does not tell you to hold for seven years, and it does not say the fund's bonds mature in seven years. It is a sensitivity, quoted in years because of how it is calculated.

The estimate was close for the example, but not exact. Where does it drift, and which way?

## Where the estimate bends

You can now turn a duration into a price change: multiply the modified duration by the change in yield, and you have the approximate percentage move. That works well for small moves, and it gets less accurate as the moves get larger.

The reason is that the true relationship between price and yield is a curve, not a straight line. Duration treats it as a straight line drawn at today's yield. For a small step along the curve, the line and the curve are close together. For a large step, they come apart.

The example shows which way they come apart. Duration predicted a move of about $43 in each direction for a one-point change. The exact figures were a fall of $42.12 when yields rose to 6 percent, and a rise of $44.52 when yields fell to 4 percent. The bond lost a little less than predicted and gained a little more. This bending of the curve is called convexity, and for an ordinary bond like this one, it works in the holder's favour.

Duration also does not stay fixed. It changes when yields change, because the present values that set the weights change. And it shrinks as time passes, because the remaining payments come closer. A duration figure describes a bond at one yield on one day.

One more limit is a matter of assumptions. The calculation takes the bond's payments as fixed and certain. Some bonds let the borrower repay early, and for those, the simple formula can mislead; analysts use adjusted versions of duration for them. Duration also usually assumes that all yields, short-term and long-term, move by the same amount at once, which real markets often do not do.

## The whole picture

A bond is a fixed schedule of coupons and a face value repaid at maturity, and its price is the sum of the present values of those payments at the market yield. When yields rise, those present values shrink, and the furthest payments shrink most, so a bond's sensitivity to rates depends on how far into the future its value sits. Macaulay duration measures that distance as a value-weighted average time, 4.55 years for the five-year 5 percent bond, always shorter than maturity when there are coupons. Dividing by one plus the yield gives modified duration, 4.33 for the example, which converts a change in yield into an approximate percentage change in price. That single number lets investors compare and manage interest-rate risk across very different bonds, as long as they remember it is a straight-line estimate of a curve, accurate for small moves and true only at the yield and date it was measured.

## Going further

- Convexity as a number: a second measure, alongside duration, that corrects the straight-line estimate for larger yield moves.
- Effective duration: a version calculated by modelling price changes directly, used for bonds whose payments can change, such as those the borrower can repay early.
- DV01: the dollar change in a bond's price for a one-basis-point move in yield, a common way traders express duration.
- Immunization: matching the duration of bonds you hold to the date you need the money, so that price changes and reinvestment changes roughly offset each other.
