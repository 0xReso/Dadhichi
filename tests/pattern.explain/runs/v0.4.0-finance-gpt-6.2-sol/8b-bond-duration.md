# Bond duration

You’ll understand why bond prices move when yields change, how duration estimates the move, and why two bonds due on the same day can react differently.

## Why a bond’s price moves

Suppose you hold a bond that will pay you $50 at the end of each year for three years, plus $1,000 at the end of the third year. You paid $1,000 for it. Then buyers start demanding a higher return from bonds like yours. Your bond still promises the same dollars on the same dates. For a buyer to earn a higher return from those payments, the price has to fall. Duration tells you how much it might fall.

A bond is a loan that can be bought and sold. The $1,000 the borrower promises to repay is the bond’s **face value**. The date that repayment is due is its **maturity date**.

Each $50 interest payment is called a **coupon**. On this bond, the coupon is fixed. A buyer who pays less than you did still gets $50 a year, and if the borrower pays as promised, that buyer also gets the same $1,000 at maturity.

The yearly rate that makes the promised payments worth the bond’s current price is called its **yield to maturity**, or **yield** for short. This rate takes account of the coupons, the repayment, and what you pay for them today. At a price of $1,000, your bond’s yield is 5 percent. At a lower price, its yield is higher.

To see how much higher, work backward from the payments. At a 5 percent yield, $50 due in one year is worth $47.62 today, because $47.62 growing by 5 percent for one year comes to about $50. That $47.62 is the payment’s **present value**. For a payment due in two years, you reverse two years of growth. The bond’s price is the sum of the present values of all its promised payments.

A rise in yield lowers the present value of every payment. How much does the timing of each payment matter?

## How the payment dates add up

Your bond’s price comes from three payments, and a higher yield reduces what each is worth today. The further away a payment is, the more years of growth you reverse to get its present value. That makes a later payment more sensitive to a change in yield than an earlier payment of the same size.

At a 5 percent yield, the first year’s $50 is worth about $48 today, and the second year’s $50 is worth about $45. The third year’s $1,050, which includes the final coupon and the face value, is worth about $907. So about 91 percent of the bond’s price comes from money due three years from now.

To give the payment schedule a single time figure, take an average of the three payment times. Give each time a weight equal to its payment’s share of the bond price. The first two payments pull the average below three years, but their weights are small. The result is about 2.86 years. This weighted average is called **Macaulay duration**.

This is where duration and maturity are easy to mix up. The maturity date tells you when the face value comes due. Macaulay duration accounts for every payment. If a bond paid the entire amount on the maturity date, all the weight would sit on that date and its Macaulay duration would equal the time to maturity. A bond with the same maturity and yield that returns more of its value through earlier coupons has a shorter Macaulay duration.

How do you turn that weighted average of payment times into an estimate of the price change?

## From payment timing to price sensitivity

Your bond’s Macaulay duration is 2.86 years because most of its value comes from the final payment. To turn that figure into a measure of price sensitivity for this annually paying bond, divide it by one plus the yield written as a decimal. At a 5 percent yield, that means dividing 2.86 by 1.05, giving about 2.72. This figure is called **modified duration**.

A modified duration of 2.72 means that if the bond’s yield rises by one percentage point, from 5 percent to 6 percent, its price falls by about 2.72 percent. On a $1,000 bond, that’s about $27, for an estimated price of $973. A one-percentage-point fall in yield gives an estimated rise of the same size. When someone uses duration to discuss how much a bond might gain or lose as yields move, they’re talking about price sensitivity.

The estimate uses the bond’s sensitivity at its starting yield. That sensitivity changes as the yield moves. If you price each payment again at a 6 percent yield, the bond comes to $973.27. At a 4 percent yield, it comes to $1,027.75. The two moves are close to $27, and the gain is a little larger than the loss. For larger yield moves, that difference from the duration estimate matters more.

The yield in the calculation is the yield on your bond. If you hear that an interest rate moved by one percentage point, you still need to know how much your bond’s yield moved before you can use its duration to estimate the price change.

## The whole picture

A fixed-rate bond’s price is what its promised payments are worth today at the yield buyers require. When that yield rises, each payment is worth less today, and the effect is stronger for payments further away. Macaulay duration combines those payment times according to how much each contributes to the price. Modified duration turns the result into a practical estimate of how much the price will move when the bond’s yield changes.

## Going further

- **Convexity** describes how a bond’s price sensitivity changes as its yield moves and helps refine the duration estimate.
- **Effective duration** estimates price sensitivity when changing rates can alter the payments themselves, as when a borrower has the right to repay a bond early.
- **Key rate duration** estimates how the price responds when market yields move around one maturity, such as three years, while yields at other maturities stay roughly in place.