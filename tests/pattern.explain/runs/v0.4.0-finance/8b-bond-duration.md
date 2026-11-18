# Bond Duration

By the end you will know what bond duration measures, how it is worked out from a bond's payments, how to use it to estimate price changes when interest rates move, and why it is not the same as the time until a bond matures.

## The problem: rates move, and bond prices move with them

A bond is a loan you make by buying a piece of paper. A company or government borrows your money and promises a fixed schedule of payments in return. Take one concrete bond and keep it in mind for the rest of the read: it costs 1,000 dollars today, it pays you 50 dollars at the end of each year for five years, and at the end of year five it also hands back the original 1,000.

The yearly 50-dollar payments are called coupons. The 1,000 returned at the end is called the face value, and the date it comes back is the maturity. On our bond the coupon is 5 percent of the face value, and the maturity is five years away.

Once a bond is issued, its payments never change. What does change is the interest rate the rest of the market is offering. Suppose that a month after you buy, new five-year bonds start paying 6 percent instead of 5. Nobody will now pay you 1,000 dollars for your bond's 50-dollar coupons when 1,000 dollars elsewhere earns 60. The only way your bond can still find a buyer is for its price to fall.

The yearly return a buyer earns if they pay today's price and hold the bond to maturity is called its yield. Price and yield are two views of the same thing, and they move in opposite directions: when yields rise, prices fall, and when yields fall, prices rise. This is one of the most commonly confused pairs in finance. A "rising bond market" means rising prices, which means falling yields.

So far that tells you the direction. Anyone holding bonds needs more than that. If rates rise by one percentage point, does a bond lose 1 percent of its value, or 4, or 15? Two bonds with the same price can react very differently to the same change in rates, and a fund manager, a pension scheme or a bank has to know which kind it is holding.

Bond duration is the number that answers this. It tells you, in a single figure, how sensitive a bond's price is to a change in interest rates. Before it can be computed, though, there is a question to settle: what is a payment five years from now actually worth today?

## Weighting the payments by time

The bond from the first section pays 50 dollars a year for five years plus 1,000 at the end, and its price falls when market yields rise. To see why some bonds fall further than others, it helps to look at each payment on its own.

A payment you receive sooner is worth more than the same payment later, because money in hand today can be invested and earn interest in the meantime. The amount of money today that is worth the same as a future payment, once that interest is taken into account, is called its present value. You find it by dividing the future payment by one plus the yield, once for every year you have to wait.

Here are the present values of our bond's five payments at a 5 percent yield, rounded to the nearest dollar. The year-one coupon of 50 is worth about 48 today. The year-two coupon is worth about 45. Year three's is worth about 43, year four's about 41. The final payment of 1,050, the last coupon plus the face value, is worth about 823. Add those five together and you get 1,000, which is exactly the bond's price. That is not a coincidence: a bond's price is the sum of the present values of its payments.

Now look at what share of the price each payment represents. The first coupon is a little under 5 percent of the 1,000. The final payment is more than 82 percent. Most of what you are paying for arrives in year five, but not all of it.

Duration takes those shares and uses them as weights on time. Each payment's date, in years, is multiplied by that payment's share of the price, and the results are added up. For our bond that is one year times about 4.8 percent, plus two years times about 4.5 percent, and so on through five years times about 82 percent. The total comes to about 4.55 years.

That figure, the average time until you receive your money, with each payment weighted by its present value, is called Macaulay duration, after the economist Frederick Macaulay, who described it in the 1930s. One way to picture it: lay the five present values out as weights along a five-year plank, and Macaulay duration is the point where the plank balances. The picture holds for the arithmetic only; on its own it says nothing about price risk.

This is where the most common misunderstanding arises. People hear "duration" and assume it means how long until the bond matures. It does not. Our bond matures in five years, but its duration is about 4.55, because the coupons arriving in years one to four pull the balance point earlier. A bond with larger coupons would have a shorter duration still, and a higher market yield would shorten it too, since higher yields shrink the present value of distant payments more than near ones.

There is exactly one kind of bond whose duration equals its maturity: a zero-coupon bond, which pays no coupons at all and makes a single payment at the end. A five-year zero-coupon bond has a duration of exactly five years, because all of its weight sits at year five. For every bond that pays coupons, duration is shorter than maturity.

A weighted average of years still does not say how many dollars the bond loses when rates rise. How does a number measured in years turn into a percentage change in price?

## From years to a price estimate

You now have a number, about 4.55 years for our bond, that describes where its value sits in time. The link to price comes from the fact that distant payments are the ones most hurt by a rise in yields, because their present value is divided by one plus the yield many more times. A bond whose value is concentrated far away reacts more than one whose value arrives soon, and Macaulay duration measures exactly how far away that value sits.

To turn this into a price rule, Macaulay duration is divided by one plus the yield. For our bond, 4.55 divided by 1.05 gives about 4.33. This adjusted figure is called modified duration, and it is the one traders use for price estimates. Its meaning is direct: for each one-percentage-point change in yield, the bond's price changes by roughly that many percent, in the opposite direction.

Apply it to the scenario from the first section, where market yields rise from 5 to 6 percent. Modified duration of 4.33 predicts a fall of about 4.33 percent, or roughly 43 dollars, taking the bond from 1,000 to about 957. If yields instead fell to 4 percent, it predicts a rise of the same size, to about 1,043.

Small moves scale the same way. Rates are usually quoted in basis points, where one basis point is a hundredth of a percentage point, so 25 basis points is a quarter of a point. A 25-basis-point rise would cost our bond about a quarter of 4.33 percent, a little over 1 percent, or around 11 dollars.

This is why duration matters well beyond a single bond. A bond fund that reports a duration of 7 is telling you that a one-point rise in rates would knock roughly 7 percent off its value. A fund with a duration of 2 would lose roughly 2 percent. The fund's maturity dates, coupons and yields are all folded into that one number, which is why it is printed on almost every bond fund fact sheet.

The word "roughly" has been doing work in each of those sentences. How close is the estimate to what actually happens?

## Where the estimate bends

Modified duration gave a clean rule for our bond: about 4.33 percent of price for each point of yield, in either direction. Checking it against the bond's real price shows where that rule holds and where it does not.

Work out the bond's price exactly at a 6 percent yield, by adding up the present values of its payments the same way as before, and you get about 957.88 dollars. The fall is about 42 dollars, a little less than the 43 duration predicted. At a 4 percent yield the exact price is about 1,044.52, a rise of about 45 dollars, a little more than predicted. The real bond loses less than the estimate when rates rise and gains more when rates fall.

The reason is that the true relationship between price and yield is a curve, while duration treats it as a straight line through the bond's current price. For small moves, the line and the curve are almost the same. For larger moves, the curve bends away from the line. That bending is called convexity, and for an ordinary bond it works in the holder's favour, on both sides. Duration is therefore a first approximation: very good for moves of a few dozen basis points, and less reliable as moves get larger.

Duration also rests on assumptions worth knowing. The simple version assumes the bond's payments are fixed, which is not true of a bond the borrower can repay early. It assumes yields for all maturities move up or down together by the same amount, when in practice short-term and long-term rates often move differently. And the number itself drifts: as time passes, the bond gets closer to maturity, and as yields change, the present-value weights change too, so a bond's duration has to be recalculated rather than read once and kept.

## The whole picture

A bond's payments are fixed, so when market interest rates move, its price has to move the other way, and the question that matters is by how much. Duration answers it by valuing each payment in today's money and finding the weighted average time until those payments arrive. That average, Macaulay duration, is shorter than maturity for any bond that pays coupons, which is why the two should not be confused. Dividing it by one plus the yield gives modified duration, the approximate percentage price change for a one-point move in yields: about 4.33 percent for the five-year, 5 percent bond followed here. The estimate is a straight-line view of a curved relationship, accurate for small moves and increasingly off for large ones, and it holds only as long as the bond's payments stay fixed and rates move together.

## Going further

- **Effective duration**: a version computed by re-pricing the bond under small rate shifts, used for bonds whose payments can change, such as callable bonds and mortgage-backed securities.
- **DV01**: the dollar change in a bond's price for a one-basis-point move in yield, a common way traders express duration in money.
- **Key rate duration**: sensitivity to a change in one point of the yield curve at a time, for when short and long rates move differently.
- **Immunisation**: matching the duration of assets to the duration of future liabilities, a technique used by pension funds and insurers.
