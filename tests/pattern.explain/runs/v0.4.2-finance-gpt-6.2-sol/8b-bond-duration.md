# Bond duration

You’ll understand how the timing of a bond’s payments determines its duration, and how to use duration to estimate what happens to its price when its yield changes.

## Why a bond’s price moves

Suppose you buy a bond for $1,000. Buying a bond means lending money in exchange for promised payments. This bond pays you $50 in one year and another $50 in two years. With the second payment, you also get back the $1,000 you lent.

The $50 interest payment is called a **coupon**. The final payment combines the last coupon and the original $1,000, so the two payments you expect to receive are $50 and $1,050.

The date when the bond is due to repay that $1,000 is its **maturity**. Your bond matures in two years. If you sell it before then, the buyer gets the remaining payments, and you get whatever price the buyer is willing to pay.

The buyer can compare your bond with other investments. If comparable bonds start offering a better return, the same $50 and $1,050 payments become less attractive. A lower price makes up for that by letting the buyer pay less for the same future cash. If comparable bonds start offering a lower return, a buyer may pay more for yours.

How does the return a buyer requires translate into a price today?

## What the payments are worth today

Your bond promises $50 in a year and $1,050 in two years. To put a price on those payments today, start with the return a buyer requires. Suppose it is 5 percent a year.

At 5 percent, $1 today grows to $1.05 in one year. To work backward from a payment due in a year, divide it by 1.05. The $50 payment is therefore worth about $47.62 today. That amount is the payment’s **present value**.

For the $1,050 payment due in two years, divide by 1.05 twice, once for each year the buyer waits. That gives a present value of about $952.38. Adding the two present values gives a bond price of $1,000.

You can also work backward from the market price. If the bond trades at $1,000, the yearly rate that makes the two present values add up to that price is 5 percent. That rate is called the **yield to maturity**. For this bond, a higher yield means dividing by a larger number each year, which gives a lower price.

The two-year payment gets divided twice, so it loses a larger fraction of its present value when the yield rises than the one-year payment does. How can you describe the timing of the two payments with a figure that reflects what each contributes to the price?

## How payment timing becomes duration

At a yield of 5 percent, about $48 of your bond’s $1,000 price comes from a payment one year away, and about $952 comes from a payment two years away. The second payment matters much more to the price, so an average that treats both payment dates equally would give the small first payment too much influence.

Instead, give each payment date a share of the average equal to the payment’s share of the price. Count one year at about 4.8 percent and two years at about 95.2 percent. Add those contributions and you get about 1.95 years. This average is called **Macaulay duration**.

This is where duration and maturity are easy to confuse. Your bond’s maturity is the date of the final payment, two years away. Its Macaulay duration takes both payments into account. The coupon due in one year pulls the average a little earlier than the final payment date. An otherwise identical bond that paid everything at maturity would have a Macaulay duration of two years.

How do you turn that average of 1.95 years into an estimate of the money you could gain or lose when the yield changes?

## What duration tells you about price

Your bond’s Macaulay duration reflects both how long you wait for each payment and how much of the price depends on it. To express that timing as price sensitivity for this bond, divide its Macaulay duration by 1.05, using its current yield of 5 percent and its annual payment schedule. The result, about 1.86, is called **modified duration**.

Suppose the yield rises from 5 percent to 6 percent immediately after you buy the bond. That is a rise of one percentage point. A modified duration of 1.86 gives an estimated price decline of 1.86 percent, or about $18.60 on your $1,000 bond. For a rise of half a percentage point, the estimated decline would be half as large.

You can check the estimate by pricing the payments again. Divide $50 by 1.06 and divide $1,050 by 1.06 twice. Add the results and the price is about $981.67, a drop of $18.33. The difference comes from using the bond’s sensitivity at the starting yield across the whole move. That sensitivity changes as the yield changes, so the estimate generally gets less accurate for larger moves.

When someone quotes a duration, check which measure they mean. On this bond, 1.95 years describes the timing of the payments, and 1.86 gives the approximate percentage price change per percentage point of yield change. The price moves in the opposite direction to the yield.

## The whole picture

A bond’s price is the sum of what its future payments are worth today at the current yield. Payments farther away are more sensitive to that yield because the rate applies for more years. Macaulay duration captures this timing by giving each payment date weight according to its contribution to the price. Modified duration turns that weighted timing into an estimate you can use when the yield moves.