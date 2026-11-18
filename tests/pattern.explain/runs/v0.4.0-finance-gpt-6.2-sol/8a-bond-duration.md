# Bond duration

You’ll understand why the timing of a bond’s payments affects its price, and how to use duration to estimate a price change.

## Why a fixed payment can have a changing price

Suppose you hold a bond that pays you $50 in one year and $1,050 in two years. You know how many dollars the bond promises and when they’re due. But if you want to sell it today, what will a buyer pay? That depends on the return the buyer can get on comparable bonds. If those bonds start offering a higher return, your bond has to sell for less to compete, even though its promised payments stay the same.

A bond is a loan that investors can buy and sell. In this example, the borrower promises to repay the original $1,000 after two years. The time until that final repayment is the bond’s **maturity**. The two-year maturity tells you when the loan ends, but the first $50 reaches you a full year before then.

The $50 paid each year is the **coupon**, the bond’s regular interest payment. You receive one coupon after a year. After two years, you receive the second coupon along with the $1,000 repayment, giving you the final $1,050.

A buyer can describe the price of those payments using a single annual rate. If the buyer pays $1,000, the rate that makes the two promised payments worth exactly that price is 5 percent. This rate is called the **yield to maturity**, or **yield** here. At a lower price, the same payments imply a higher yield. At a higher price, they imply a lower one.

How does the date of each payment affect how much the price moves when the yield changes?

## How payment dates become duration

The buyer gets $50 in one year and $1,050 in two years. To see how much each payment matters to the price, put both payments in today’s dollars using the same yield.

At a 5 percent yield, $47.62 today grows to about $50 in one year. So $47.62 is the **present value** of that first payment. For the final $1,050, you work back through two years of growth at 5 percent a year. That gives a present value of $952.38. Add the two present values and you get the bond’s $1,000 price.

That gives you a way to average the payment dates. Count each date according to its share of the price. The first payment accounts for about 4.8 percent of the price, so the one-year date gets about 4.8 percent of the weight. The final payment accounts for the other 95.2 percent, so the two-year date gets most of the weight. The result is about 1.95 years. This average is called **Macaulay duration**.

The 1.95 years describes where the value of the payments sits in time. It doesn’t mark a date when you receive money, and the bond still matures in two years. The earlier coupon pulls the average a little below two years. If all the money arrived at maturity, the average would land exactly there.

Think about what happens to the two present values when the yield rises. To value the first payment, you divide $50 by a year’s growth at the new, higher rate. To value the final payment, you divide $1,050 by that higher growth factor twice, once for each year. The extra year makes the final payment’s present value fall more in percentage terms. That is why later payments make a bond’s price more sensitive to changes in yield.

How do you turn that average payment date into an estimate of what the bond will sell for?

## How to estimate the price change

Macaulay duration tells you where the value of the bond’s payments falls in time. To estimate the price move, you use a related number called **modified duration**. With the annual payments and annual yield in this example, divide the Macaulay duration by one plus the yield. Dividing 1.95 by 1.05 gives about 1.86.

A modified duration of 1.86 means that if the bond’s yield rises by one percentage point, its price falls by approximately 1.86 percent. A percentage point measures the difference between two rates. A move from 5 percent to 6 percent is one percentage point. On this $1,000 bond, the estimate is a drop of $18.60, leaving a price of about $981.40. A small fall in yield gives an estimated price rise by the same calculation.

You can check the estimate by valuing the two payments again, now at a 6 percent yield. The $50 due in one year is worth about $47.17 today, and the $1,050 due in two years is worth about $934.50. Together they give a price of about $981.67. That’s 27 cents above the duration estimate.

The difference comes from using the price’s sensitivity at the starting yield. As the yield moves, that sensitivity changes. Modified duration works best for small moves. If you need the price at a particular new yield, you can calculate it directly from the promised payments, as we did at 6 percent.

When someone says a bond has “a duration of 1.86,” listen for what they’re using the number to do. In a conversation about price moves, they usually mean modified duration. The practical reading is a percentage price move for a given change in the bond’s yield. The date you get your final payment is still its maturity.

## The whole picture

A bond’s price is the sum of what its promised payments are worth today at its yield. A change in yield has more effect on payments farther away, because it changes the rate used to work back through every year between those payments and today. Macaulay duration captures that timing by averaging the payment dates according to their shares of the price. Modified duration turns the average into an estimate of how much the price moves, in the opposite direction, for a small change in yield.

## Going further

- **Convexity** measures how the price’s sensitivity changes as yield moves and helps refine the duration estimate.
- **Effective duration** estimates price sensitivity when a change in rates can also change the payments the bond is expected to make.