# Bond Duration

By the end you will know what a bond's duration measures, how it is worked out, how to turn it into an expected price change, and why it is not the same as the time until a bond is repaid.

## Two loans, one risk

A bond is a loan you make by buying a piece of paper. A company or government borrows, say, 1,000 dollars from you and promises two things: a fixed payment every year while the loan runs, and the 1,000 back at the end. The yearly payment is called the coupon, the 1,000 is the face value, and the date the face value comes back is the maturity.

Take one bond and keep it for the rest of this piece. It has a face value of 1,000 dollars, a coupon of 50 dollars a year (5 percent of the face value), and five years to maturity. So it pays 50 at the end of years one, two, three and four, and 1,050 at the end of year five: the last coupon plus the face value.

Bonds are bought and sold long before they mature, and their prices move. The main thing that moves them is the level of interest rates in the wider market. When rates rise, the price of a bond you already hold falls. When rates fall, its price rises. Anyone holding bonds is therefore exposed to interest-rate risk: the chance that a change in rates changes what their bonds are worth.

The awkward part is that bonds feel this risk to very different degrees. A bond maturing in thirty years can lose far more value from the same rise in rates than our five-year bond. Even two bonds that mature on the same day can react differently if their coupons differ. A bond investor needs a single number that says, for any bond, "this is how hard rate changes will hit it." That number is duration.

## Why a rate change moves a price

You now hold the problem: bond prices fall when rates rise, and some bonds fall much further than others. To see why, it helps to look at how a bond gets its price in the first place.

Money arriving later is worth less than the same money now, because money you hold today can earn interest in the meantime. If you can earn 5 percent a year, then 50 dollars a year from now is worth about 47.62 dollars today, since 47.62 invested at 5 percent grows to 50 in a year. That today-equivalent is called the present value. A payment further away is cut down more: 50 dollars five years out is worth only about 39 dollars today at 5 percent.

The interest rate used to cut future payments down to present values is the bond's yield: the yearly return the market demands for holding it. A bond's price is the sum of the present values of all its payments, worked out at that yield.

For our bond at a 5 percent yield, the five payments are worth about 47.62, 45.35, 43.19, 41.14 and 822.70 dollars today. They add up to 1,000 dollars, so the bond's price is 1,000. (That neat result is not a coincidence: when the yield equals the coupon rate, a bond's price equals its face value.)

Now suppose market rates rise and the yield goes to 6 percent. Every payment gets discounted harder, every present value shrinks, and the sum shrinks with it. Worked out at 6 percent, the bond's price is about 957.88 dollars. Price and yield move in opposite directions because the yield sits in the denominator of every present value.

This also shows why some bonds are hit harder. A higher yield shrinks distant payments much more than near ones, because the extra discount is applied once for every year of waiting. A bond whose value sits mostly in far-off payments therefore loses more. So the question becomes: how far off, on average, is a bond's value?

## Duration as a balance point

You hold two ideas now: a bond's price is the sum of the present values of its payments, and a rise in yield hurts distant payments most. Duration turns "how distant is this bond's value" into a single number of years.

Look at what share of the bond's price each payment supplies. For our bond at 5 percent, the year-one coupon supplies about 4.8 percent of the 1,000-dollar price, year two about 4.5 percent, year three about 4.3 percent, year four about 4.1 percent, and the final payment of 1,050 about 82.3 percent.

Now take the average of the payment dates, one through five, giving each date a weight equal to its share of the price. One times 4.8 percent, plus two times 4.5 percent, and so on up to five times 82.3 percent, comes to about 4.55 years. This weighted-average time is called the Macaulay duration, after Frederick Macaulay, the economist who proposed it in the 1930s.

A physical picture fits well here. Lay the five payments along a ruler marked in years, each with a weight equal to its present value. The point where the ruler would balance on your finger is the Macaulay duration. The picture holds for the calculation, but stops at that: it says nothing about what happens to the price, which is what the next idea handles.

This is where the most common misunderstanding lives. Many people take duration to be another word for maturity, or something close to it. It is not. Our bond matures in five years but has a duration of about 4.55, because the coupons arriving in years one to four pull the balance point earlier. A bond with larger coupons would balance earlier still. Only a bond that pays nothing until maturity, called a zero-coupon bond, has a duration equal to its maturity: a five-year zero-coupon bond has a duration of exactly five years, because all its weight sits at the end. Two bonds with the same maturity can have quite different durations, and it is duration, not maturity, that tracks their sensitivity to rates.

Duration also changes as the yield changes, and it shortens as time passes and the bond nears maturity. It is a reading taken at one moment, not a fixed label on the bond.

A number of years is a useful way to compare bonds, but an investor usually wants something more direct: if rates move by one point, how many dollars do I lose?

## From years to a price change

So far duration is a balance point measured in years: for our bond, about 4.55. A small adjustment turns it into a forecast of price change.

Divide the Macaulay duration by one plus the yield. For our bond that is 4.55 divided by 1.05, which gives about 4.33. This figure is called the modified duration, and it reads directly as a percentage: for each one percentage point change in yield, the bond's price moves by roughly 4.33 percent in the opposite direction. (The division by 1.05 assumes payments once a year; for bonds paying twice a year the adjustment uses half the yield.)

Try it on the rise from 5 percent to 6 percent. Modified duration predicts a fall of about 4.33 percent of 1,000 dollars, which is 43.30, taking the price to about 956.70. The true price at 6 percent is 957.88. The estimate is off by little more than a dollar on a move that most bond markets would consider large.

Traders usually think in smaller steps. A basis point is one hundredth of a percentage point, so a move from 5.00 to 5.01 percent is one basis point. For our bond, each basis point rise knocks roughly 0.0433 percent off the price, about 43 cents per 1,000 dollars. That is the kind of figure a fund manager adds up across hundreds of bonds to know what a day's rate move will cost.

The same arithmetic works for a whole portfolio. The duration of a collection of bonds is, to a good approximation, the average of their durations weighted by how much money sits in each. A fund that reports a duration of six years is telling you that a one-point rise in rates would cut its value by roughly 6 percent.

The estimate for our bond was close but not exact. That small miss has a cause, and it grows quickly when rate moves get bigger.

## Where the straight line bends

Modified duration gives you a rule: a one-point move in yield moves the price by about 4.33 percent the other way, and that rule landed within about a dollar for a one-point rise. The leftover gap comes from the shape of the price curve.

Duration treats the link between yield and price as a straight line: every extra point of yield costs the same 4.33 percent. The real link is a curve that bends. As the yield rises, each further rise costs a little less; as it falls, each further fall gains a little more. This bend is called convexity.

Our bond shows it in both directions. At 6 percent, duration predicted 956.70 and the true price was 957.88, so the bond lost less than forecast. At 4 percent, duration predicts a gain of 43.30, to 1,043.30, but the true price is about 1,044.52, so it gained more than forecast. For an ordinary bond like this one, the straight-line estimate is always a little pessimistic, whichever way rates move.

For small moves the gap is tiny, which is why duration alone serves most day-to-day purposes. For large moves it widens, and practitioners add a convexity correction to the estimate.

Duration also rests on two assumptions worth keeping in view. It assumes the bond's payments are fixed, which fails for bonds the issuer can repay early, since the payments then depend on rates themselves. In the usual simple form, it also assumes that every rate across all maturities moves by the same amount at once, which real markets rarely do. When either assumption breaks, the duration figure becomes a rougher guide, and other measures take over.

## The whole picture

A bond's price is the sum of its future payments, each cut down to a present value at the market's yield; a rise in yield cuts distant payments hardest, so a bond's sensitivity to rates depends on how far off its value sits. Macaulay duration measures exactly that, as the present-value-weighted average time of the payments, about 4.55 years for our five-year, 5 percent bond, and it is shorter than maturity whenever coupons arrive along the way. Dividing by one plus the yield gives modified duration, about 4.33 here, which says the price moves roughly 4.33 percent the other way for each point of yield. That straight-line rule is very close for small moves and drifts for large ones because the true price curve bends, which is convexity. Duration exists so that bonds of any coupon and maturity, and whole portfolios of them, can have their interest-rate risk compared and managed with one number.

## Going further

DV01 (dollar value of one basis point): the price change in currency, rather than percent, for a one basis point move in yield; about 43 cents per 1,000 dollars for our bond.

Effective duration: a version calculated by repricing a bond at slightly higher and lower yields, used for bonds whose payments change with rates, such as callable bonds and mortgage-backed securities.

Key rate duration: a set of durations that measure sensitivity to rates at particular maturities separately, for when short-term and long-term rates do not move together.

Immunization: matching the duration of assets to the duration of future liabilities, a technique pension funds and insurers use so that rate changes affect both sides roughly equally.
