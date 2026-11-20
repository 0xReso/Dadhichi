# Bond Duration

By the end you will know what a bond's duration measures, how it is worked out, how it predicts a bond's price change when interest rates move, and where that prediction stops being reliable.

## Why bond prices move when rates move

A bond is a loan you make by buying a piece of paper. A company or a government borrows money from you, and in return promises a fixed schedule of payments. Unlike a share in a company, a bond gives you no ownership; it gives you a set of promised payments and nothing else.

Take one bond and keep it in mind throughout. It promises to repay $1,000 in five years. That $1,000, the sum handed back at the end, is called the face value.

Along the way, the bond also pays you $50 at the end of each year for five years. These regular payments are called coupons. This bond's coupon is 5 percent of its face value, paid once a year. Many real bonds pay twice a year, but once a year keeps the arithmetic clean.

The date when the face value is repaid and the payments stop is called the maturity. Here it is five years away.

So the whole bond is a list of six promised payments: $50 after one year, two, three and four, and $1,050 after five years, the last coupon plus the face value.

The payments are fixed, but the bond trades on a market, and its price can change every day. The reason is that interest rates elsewhere change. Suppose you bought this bond for $1,000, and next week new five-year bonds start paying 6 percent. Nobody will now pay you $1,000 for a bond that pays $50 a year when $1,000 buys $60 a year elsewhere. Your bond only sells if its price drops far enough that the buyer earns about 6 percent anyway. When rates rise, existing bond prices fall; when rates fall, they rise. Price and rate move in opposite directions.

That raises the practical question every bond holder faces: if rates move by one percentage point, how much does my bond's price move? Some bonds barely flinch and others swing hard. Duration is the number that answers it, and to see where it comes from, you need one more idea about money and time.

## Waiting time, weighted by value

Your bond is a list of six payments spread over five years, and its price falls when rates rise. To measure how far, start with how much each payment is worth today.

A dollar paid in a year is worth less than a dollar now, because a dollar now could be put on deposit and earn interest. If you can earn 5 percent a year, $47.62 today grows to $50 in a year. So $50 arriving in a year is worth $47.62 to you today. That figure, a future payment shrunk back to what it is worth now at a given interest rate, is called its present value. The further away a payment is, the more it shrinks, because it has more years of missed interest to make up.

The interest rate used for this shrinking is the bond's yield. Strictly, the yield is the one rate that, applied to every payment, makes their present values add up to the bond's market price. It is the yearly return a buyer locks in by paying that price and holding the bond to maturity. For your bond, priced at $1,000 with a 5 percent coupon, the yield is exactly 5 percent.

Here are the six payments shrunk at 5 percent:

- the $50 in year one is worth $47.62 today
- the $50 in year two, $45.35
- the $50 in year three, $43.19
- the $50 in year four, $41.14
- the $1,050 in year five, $822.70

Add them and you get $1,000, the price. Now look at where that $1,000 sits in time. About 82 percent of the bond's value arrives in year five, and the remaining 18 percent arrives in small slices across the first four years.

Now ask a simple question: on average, how long do you wait for your money? Not counting dollars as they are written on the bond, but counting each payment by what it is worth today. Multiply each payment's time by its share of the price and add up the results. Year one carries about 4.8 percent of the value, year two 4.5 percent, year three 4.3 percent, year four 4.1 percent and year five 82.3 percent. The weighted average comes to about 4.55 years.

That number is the bond's Macaulay duration, named after the economist Frederick Macaulay, who described it in the 1930s. It is the average time until you receive the bond's value, with each payment weighted by its present value. It is measured in years.

This is the point where most people go wrong. Duration is not the same thing as maturity. Your bond matures in five years, but its duration is 4.55 years, because the coupons hand part of your money back early and pull the average forward. A bond with bigger coupons would have a shorter duration still. Only a bond that pays nothing until the end, called a zero-coupon bond, has a duration equal to its maturity: all its value arrives on one date, so the average wait is that date. Two bonds with the same maturity can have quite different durations, and it is the duration, not the maturity, that tells you how exposed each one is to rates.

Which leaves the question of how an average waiting time turns into a price change.

## From years to a price forecast

You now hold the bond's Macaulay duration, 4.55 years: the average wait for its money, weighted by present value. The link to price sensitivity comes from the shrinking itself.

When the yield rises, every payment's present value shrinks a little more. A payment that is further away shrinks more, because the higher rate is applied for more years. So a bond whose value sits mostly far away loses more of its price than one whose value arrives soon. The average distance of the value, which is exactly what Macaulay duration measures, therefore governs how much the price falls. Working through the mathematics shows that, for a small change in yield, the percentage fall in price is close to the Macaulay duration divided by one plus the yield.

That adjusted figure is called modified duration. For your bond it is 4.55 divided by 1.05, which gives about 4.33. Modified duration is the version traders use for forecasts, and its meaning is direct: for each one percentage point rise in yield, the price falls by about 4.33 percent. A fall in yield works the same way in reverse.

Apply it. Suppose rates rise from 5 to 6 percent. Modified duration predicts a fall of about 4.33 percent of $1,000, so a new price near $956.70. Working out the six present values again at 6 percent gives the true new price: $957.88. The forecast is off by about a dollar.

The same figure works at the scale traders talk in. Rates are usually quoted in basis points, where one basis point is one hundredth of a percentage point. A move of one basis point changes your bond's price by about 0.0433 percent, roughly 43 cents on $1,000. A bond portfolio manager who hears that rates jumped 20 basis points can multiply in their head and know they lost about 0.87 percent before checking a screen.

This is why duration matters so much in practice. It turns a whole schedule of payments into a single number that ranks bonds by risk to interest rates. A bond with a modified duration of 10 will move roughly twice as much as yours for the same change in rates; one with a duration of 2 will move less than half as much. The number is quick to use, but it comes from a straight-line approximation, so the next question is where that straight line parts from reality.

## Where the forecast stops working

The forecast you now hold says your bond's price moves about 4.33 percent per percentage point of yield. It was off by a dollar for a one-point rise. That small error is a clue to the first limit.

The true relationship between price and yield is not a straight line but a curve that bends upward. Check the other direction. If rates fall from 5 to 4 percent, the forecast says the price rises to about $1,043.30, but the true price is $1,044.52. So when rates rose, the price fell a little less than forecast, and when they fell, it rose a little more. That bend is called convexity. It always works in the holder's favour for an ordinary bond like yours, and it grows with the size of the move. For a one-point change the error is about a dollar; for a three-point change it becomes large enough that serious users add a convexity correction on top of duration.

The second limit is that duration is a snapshot. It is worked out at today's yield and today's date. When the yield changes, the present-value weights change, so the duration changes too: at a higher yield, distant payments shrink more, so their share of the price falls and the duration gets a little shorter. And as time passes, the bond moves toward maturity and its duration shrinks. Next year, your bond will be a four-year bond with a shorter duration. A forecast is only good for the moment its duration was calculated.

The third limit sits in an assumption about the bond itself: that its payments are fixed. Your bond's six payments are promised and do not change when rates move. Some bonds let the borrower repay early, usually when rates have fallen and borrowing again is cheaper. For those, the payment schedule itself depends on rates, so the simple calculation above misdescribes them, and analysts use a different method that models how the payments would change.

The last limit concerns what duration measures in the first place. It is a measure of sensitivity to interest rates, and of nothing else. It says nothing about whether the borrower will pay. A bond from a shaky company and one from a stable government can share the same duration while carrying very different risks of not being repaid.

## The whole picture

A bond is a fixed list of payments, and its price is the sum of their present values at the going yield. Because distant payments shrink more when the yield rises, the price's sensitivity to rates depends on how far away, on average, the bond's value sits. Macaulay duration measures exactly that average distance in years, weighting each payment by its present value, which is why it is shorter than maturity whenever coupons are paid. Divide it by one plus the yield and you have modified duration, a straight-line forecast of the percentage price change per percentage point of yield: 4.33 percent for the five-year bond here. The forecast is accurate for small moves, drifts as the curve bends for large ones, needs recalculating as yields and time change, and describes rate risk alone.

## Going further

- Convexity correction: a second term added to the duration forecast to account for the curve between price and yield, used for larger rate moves.
- Effective duration: a duration figure found by repricing a bond under small rate shifts, used for bonds whose payments change when rates move, such as those the borrower can repay early.
- DV01 (dollar value of one basis point): the price change in money, rather than in percent, for a one basis point move in yield; about 43 cents for the bond in this article.
- Portfolio duration: the duration of a collection of bonds, found as the average of their durations weighted by how much of the portfolio each one makes up.
