# Bond Duration

By the end you will know what bond duration measures, why it is counted in years but used as a percentage, how to read it for a real bond, and where the number misleads people.

## Rates move, and bond prices follow

Bond duration is a single number that tells you how much a bond's price will fall or rise when interest rates change. It exists because anyone holding bonds faces one question above all others: if rates go up tomorrow, how much do I lose?

To see why that question matters, start with the bond itself. A bond is a loan you make to a government or a company. In return, the borrower pays you a fixed amount of interest every year and hands back the original sum on a set date. The yearly interest is called the coupon, the original sum is the face value, and the end date is the maturity.

Here is the bond this whole piece will follow. It has a face value of 1,000, a coupon of 5 percent, so it pays 50 every year, and it matures in 10 years. In year ten you receive the last 50 plus the 1,000 back, so 1,050 in all.

The price of a bond today is the present value of those payments: what each future payment is worth now, once you account for the interest you could have earned in the meantime. A payment of 50 arriving in one year is worth a little less than 50 today, and a payment arriving in ten years is worth a good deal less. The rate used to shrink future payments down to today's value is the rate the market currently demands on bonds like this one. That rate is called the yield.

If the market demands 5 percent, our bond's payments shrink to exactly 1,000 today, so it trades at 1,000. Now suppose rates across the market rise and new bonds start paying 6 percent. Nobody will pay 1,000 for a bond paying 50 a year when a fresh one pays 60. Our bond's price has to drop until a buyer earns 6 percent on it. Working it out, that price is about 926.40, a loss of about 7.4 percent. Had rates fallen to 4 percent instead, the price would have climbed to about 1,081.11.

This is the rule underneath everything that follows: when yields go up, bond prices go down, and the reverse. They move in opposite directions because the same fixed payments are being shrunk at a harsher or gentler rate.

The rule tells you the direction. It does not tell you the size. A different bond, faced with the same one-point rise in rates, might lose 2 percent or 15 percent. So what decides how hard a given bond is hit?

## Duration as an average waiting time

So far you hold two ideas: a bond's price is its future payments shrunk back to today, and a rise in yield shrinks them harder, pushing the price down. The size of that push depends on when the money arrives.

A payment arriving next year barely feels a change in rates, because it is shrunk for only one year. A payment arriving in ten years feels the change ten times over, because the harsher rate is applied year after year. A bond whose money comes mostly late is therefore much more sensitive than one whose money comes mostly early.

Duration turns that observation into a number. Take each payment, note how many years away it is, and weight it by how much of today's price it accounts for. The weighted average of those waiting times is the bond's duration, measured in years. This version, the original one, is called Macaulay duration, after the economist Frederick Macaulay, who described it in 1938.

In our bond, the weights are lopsided. The first 50, a year away, is worth about 47.62 today, under 5 percent of the 1,000 price. The final 1,050, ten years away, is worth about 644.61 today, nearly two thirds of the price. The nine coupons in between fill out the rest. Average the waiting times with those weights and you get about 8.11 years.

This is where the most common misunderstanding sits. People often take duration to be the same as maturity, or a fancier word for it. It is not. Our bond matures in 10 years, but its duration is about 8.11 years, because the coupons along the way pull the average earlier. The only bond whose duration equals its maturity is one that pays nothing until the end. That kind is called a zero-coupon bond, and a 10-year zero-coupon bond has a duration of exactly 10 years. Every bond that pays coupons has a duration shorter than its maturity, and the bigger the coupons, the shorter it gets.

Duration also shifts as the yield changes. At a higher yield, the distant payments shrink more, so they carry less weight, and the average moves earlier. Duration is a property of a bond at a particular yield, not a fixed label printed on it.

A waiting time in years is a useful picture, but it is not yet what an investor wants to know. How does 8.11 years become a figure for how much money you lose?

## From years to a percentage: modified duration

You now hold duration as the weighted average time until a bond pays you back, about 8.11 years for our bond. The remarkable thing about that number is that, with one small adjustment, it also measures price sensitivity directly.

The adjustment is to divide Macaulay duration by one plus the yield, using the bond's yield per payment period. For our bond, which pays once a year at a 5 percent yield, that is 8.11 divided by 1.05, which gives about 7.72. This adjusted figure is called modified duration.

Modified duration reads as a percentage. It says: for every one percentage point the yield moves, the price moves by about this many percent in the opposite direction. Our bond has a modified duration of about 7.72, so a rise in yield from 5 to 6 percent should cut its price by about 7.72 percent, from 1,000 to roughly 922.80.

The same rule scales down to small moves. Traders talk about rate changes in basis points, where one basis point is a hundredth of a percentage point. A rise of 10 basis points, from 5.00 to 5.10 percent, is a tenth of a point, so the estimated loss on our bond is a tenth of 7.72 percent, about 0.77 percent, or roughly 7.70 on a 1,000 bond.

This is why duration is the first number quoted for a bond fund or a bond portfolio. A fund reporting a duration of 2 is telling you that a one-point rise in rates would cost it about 2 percent. A fund reporting a duration of 15 would lose about 15 percent in the same move. Investment managers usually describe a portfolio's duration as roughly the value-weighted average of the durations of the bonds it holds, which makes it a single dial for the whole portfolio's rate risk.

Notice, though, that the estimate of 922.80 does not quite match the true price of 926.40 that you met earlier. The estimate was too gloomy by a few units. Where does that gap come from, and when does it start to matter?

## Where the straight line bends

At this point you can turn a bond's payments into a duration in years, and turn that into an expected percentage price change for a given rate move. For our bond, a one-point rise was expected to cost about 7.72 percent and actually cost about 7.36 percent.

The gap exists because duration treats the link between yield and price as a straight line: each extra point of yield knocks off the same percentage. The real link is a curve. As yields rise, the price falls by less and less for each extra point, and as yields fall, the price rises by more and more. The same thing showed up in our bond in the other direction: duration predicted a gain of about 7.72 percent if the yield dropped to 4 percent, and the true gain was about 8.11 percent.

That bend is called convexity. For an ordinary bond it works in the holder's favour: losses come in a little smaller than duration predicts, and gains a little larger. For small moves, such as a few basis points, the gap is tiny and duration on its own is good enough. For large moves, one or two percentage points and more, the gap grows, and analysts add a convexity correction to the estimate.

Two further assumptions carry weight. Duration describes what happens if yields on all bonds of every maturity shift by the same amount at once. In practice short-term and long-term rates often move by different amounts, and a single duration figure cannot capture that. And duration assumes the bond's payments are fixed. A bond that the borrower can repay early, which is common with mortgages and some corporate bonds, does not have fixed payments, so the simple calculation no longer applies and a different method is used.

With those limits in mind, duration remains the standard first answer to the question this piece opened with.

## The whole picture

A bond's price is its fixed future payments shrunk back to today at the market's yield, so when the yield rises the price falls. How far it falls depends on when the money arrives, because late payments are shrunk over more years. Macaulay duration captures that as a weighted average waiting time, about 8.11 years for a 10-year bond paying 5 percent, shorter than its maturity because coupons arrive along the way. Dividing by one plus the yield gives modified duration, about 7.72, which reads directly as the percentage the price moves for each one-point move in yield. That estimate is a straight line laid on a curve: it is close for small moves, drifts for large ones, and assumes every rate moves together and the payments never change.

## Going further

Convexity: the measure of how much the price-yield curve bends, used to correct duration's estimate for large rate moves.

DV01 (dollar value of one basis point): the change in a bond's price, in money rather than percent, for a one-basis-point move in yield.

Effective duration: a version calculated by repricing the bond under small rate shifts, used for bonds with early repayment or other features that change their payments.

Key rate duration: a set of durations, one for each point along the range of maturities, that shows how a bond or portfolio responds when short and long rates move by different amounts.
