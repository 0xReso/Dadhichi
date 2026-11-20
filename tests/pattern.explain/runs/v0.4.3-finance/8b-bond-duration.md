# Bond Duration

By the end you will know what a bond's duration measures, how it is worked out, why it is given in years, and how it lets you estimate how far a bond's price moves when interest rates change.

## The problem duration solves

Suppose you own some bonds and interest rates across the market rise by one percentage point. Your bonds lose value. The question that matters is how much. Two bonds that pay the same rate of interest can lose very different amounts from the same rise, and an investor who cannot tell them apart cannot tell how much risk they are holding. Duration is the number investors use to answer that question before the rates move.

A bond is a loan that you make by buying it. A government or a company borrows money from whoever buys the bond and promises a fixed schedule of repayments in return. For the running example, take a bond issued by a company, which you buy for $1,000.

Every year, the company pays you $50. That regular interest payment is called the coupon. Here it is 5 percent of the amount you lent, so the bond has a coupon rate of 5 percent.

At the end, the company hands back the $1,000 it borrowed. That amount is called the face value of the bond.

The date of that final repayment is called the maturity. This bond matures in five years. Put together, its whole schedule is four payments of $50, one at the end of each of the first four years, and then $1,050 at the end of year five: the last coupon plus the face value.

You do not have to hold the bond until it matures. Bonds are bought and sold between investors every day, and their prices change as they do. That raises an odd question: if the payments are fixed in writing, why should the price move at all?

## Why a fixed bond's price moves

The bond in hand pays a fixed $50 a year for five years and $1,000 at the end, yet its market price changes. The reason lies in what money paid later is worth today.

A dollar received in a year is worth less than a dollar received now, because a dollar you hold now can earn interest in the meantime. If you can earn 5 percent a year elsewhere, then $47.62 today grows to $50 in a year. So $50 paid a year from now is worth $47.62 to you today. That figure is called the present value of the payment. A bond's fair price is the present values of all its payments added together.

The interest rate used to work out those present values is the return the market currently demands on loans like this one. That rate is called the yield. At a yield of 5 percent, the five payments of the example bond are worth $47.62, $45.35, $43.19, $41.14 and $822.70 today. They add up to $1,000, which is why the bond sells for exactly its face value when the yield equals the coupon rate.

Now suppose the market's demanded return rises to 6 percent. Every payment is discounted more heavily, the same fixed payments are worth less today, and the price falls to $957.88. This is why a bond's price and its yield always move in opposite directions. They are not two separate facts that happen to line up; a higher yield is a lower price, seen from the other side.

The fall is not spread evenly across the payments. The first $50 coupon, one year away, loses less than 1 percent of its present value when the yield goes from 5 to 6 percent. The final $1,050, five years away, loses about 4.6 percent, because the higher rate compounds against it for five years instead of one. The further away a payment sits, the harder a rise in yield hits it. So the size of a bond's price swing depends on how far away its money is, and that leads to the next question: on average, how far away is the money in this bond?

## Duration as an average waiting time

A bond's price is the sum of the present values of its payments, and distant payments react most to a change in yield. Measuring a bond's risk therefore means measuring how far into the future its value lies.

The way to measure that is a weighted average of the payment dates. Take each payment's share of the price as its weight. In the example, the first four coupons make up about 4.8, 4.5, 4.3 and 4.1 percent of the $1,000 price, and the final payment makes up about 82.3 percent. Multiply each payment's year by its share and add the results: 1 times 4.8 percent, plus 2 times 4.5 percent, and so on up to 5 times 82.3 percent. The total comes to about 4.55 years.

That figure, the average time you wait for the bond's value to reach you, weighted by present value, is called the Macaulay duration. It is named after Frederick Macaulay, an economist who proposed it in 1938. When people say a bond has a duration of four and a half years, this average is usually what they started from.

This is the point where many people go wrong. Because duration is given in years, it is easy to treat it as another way of saying how long the bond has left to run. It is not. The example bond matures in five years, but its duration is 4.55 years, because the coupons hand back part of your money before the end. Maturity says when the last payment arrives; duration says when the money arrives on average.

The two are equal in one case. A bond that pays no coupons and hands over everything in a single payment at maturity is called a zero-coupon bond. With only one payment, the weighted average sits exactly on that date, so a five-year zero-coupon bond has a duration of exactly five years.

For every bond that pays coupons, duration is shorter than maturity, and the gap widens as the maturity gets longer. A 30-year bond paying 5 percent and priced at a 5 percent yield has a Macaulay duration of about 16 years, little more than half its maturity, because decades of coupons pull the average forward. Higher coupons pull it forward further. A higher yield shortens it too, since it shrinks the weight of the distant payments.

An average waiting time is a useful thing to know, but it is not yet a statement about money. The last step is to see how it turns into a forecast of price.

## Duration as a measure of price risk

The example bond has a Macaulay duration of about 4.55 years, the present-value-weighted average time until its payments arrive. That same number, slightly adjusted, tells you how sensitive its price is to the yield.

For a bond that pays its coupon once a year, the adjustment is to divide the Macaulay duration by one plus the yield. For the example bond, that is 4.55 divided by 1.05, which gives about 4.33. This adjusted figure is called the modified duration. It is no longer a time; it is a percentage. It says that for every one percentage point the yield rises, the price falls by about 4.33 percent, and for every point it falls, the price rises by about the same.

Try it on the example. If the yield rises from 5 to 6 percent, modified duration predicts a fall of about 4.33 percent, which is $43.29 on a $1,000 bond. The actual new price is $957.88, a fall of $42.12. The estimate is off by just over a dollar. This is how duration is used day to day: a bond fund manager who sees that a portfolio has a duration of around 4 can say, without recalculating every bond, that a one-point rise in yields would cost it about 4 percent of its value.

The estimate is not exact, because the true link between price and yield is a curve, while duration treats it as a straight line that touches the curve at the current yield. For small moves the line and the curve are almost the same: a rise of a tenth of a percentage point puts the estimate for the example bond within about a cent of the true price. For larger moves the gap grows, which is why a one-point move left an error of over a dollar.

That bend in the curve is called convexity. For an ordinary bond like the example, it always works in the holder's favour. If the yield falls from 5 to 4 percent, duration predicts a gain of $43.29, but the real price rises to $1,044.52, a gain of $44.52. When yields rise, the bond loses a little less than duration predicts; when they fall, it gains a little more.

Duration has other limits built into it. It is calculated at today's yield, so it changes as the yield changes and as the bond moves closer to maturity, and needs recalculating. It assumes the bond's payments are fixed. And when it is applied to a portfolio of many bonds, it assumes yields at every maturity rise or fall by the same amount, which real markets often do not do.

## The whole picture

A bond's price is the present value of a fixed schedule of payments, worked out at the market's current yield, so when the yield rises, the price falls, and payments further in the future fall the most. Duration captures that in one number: the Macaulay duration is the average time until the bond's value is paid, weighted by present value, and is shorter than the maturity whenever the bond pays coupons. Divided by one plus the yield, it becomes the modified duration, which estimates the percentage change in price for each percentage point change in yield. The estimate is a straight line laid against a curve, accurate for small moves and increasingly off for large ones, with convexity making up the difference.

## Going further

- DV01: the change in a bond's price, in money rather than percent, for a yield change of one basis point, which is one hundredth of a percentage point.
- Effective duration: a version of duration for bonds whose payments can change, such as bonds the issuer is allowed to repay early, worked out by repricing the bond at slightly higher and lower yields.
- Key rate duration: a set of figures showing how sensitive a bond or portfolio is to yields at particular maturities, for when yields at different maturities do not move together.
- Immunisation: matching the duration of a set of bonds to the date when money is needed, so that rate changes affect the bonds' price and the return on reinvested coupons in roughly offsetting ways.
