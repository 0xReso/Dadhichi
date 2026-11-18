# Bond duration

You’ll learn how the timing of a bond’s payments helps you estimate how much its price will move when its yield changes.

## Why the payment dates matter

Suppose you own a bond worth $1,000 today. Tomorrow, buyers want a higher yearly return for holding it. The bond still promises the same payments on the same dates, but buyers can get that higher return by paying less for those payments. You know which way the price will move. Bond duration helps you estimate by how much.

A bond is a loan that investors can buy and sell. When you buy one, you take over the right to receive its scheduled payments. In this example, the issuer, the organisation that borrowed the money, has promised to make payments over the next three years.

The amount the issuer promises to repay at the end is called the **face value**. Here it is $1,000. That’s also what the bond happens to sell for today, but the two amounts have different jobs. The face value tells you what the issuer owes at the end. The price tells you what a buyer pays today.

The issuer also promises to pay $50 in interest at the end of each year. Each of those interest payments is called a **coupon**. So you expect $50 after one year, $50 after two years, and $1,050 after three years, when the last coupon and the face value arrive together.

The date of that final payment is called **maturity**. Your bond has three years to maturity. That tells you when the payments end, but the earlier coupons also count. To see how much they count, you need to put all three payments in today’s dollars. How do you do that?

## Turning payments into a measure of time

You have three payments due on three different dates. To compare them, ask how much money you would need today to end up with each payment on its due date if your money grew at a given yearly rate. That amount today is the payment’s **present value**. At a yearly rate of 5 percent, for example, $47.62 today grows to about $50 in one year.

For a bond, you can work backwards from its price to find the yearly rate at which the present values of its payments add up to that price. The rate is called the **yield to maturity**, or **yield** for short. For this bond at its $1,000 price, with interest calculated once a year, the yield is 5 percent.

At that yield, the $50 due after one year is worth about $47.62 today. The $50 due after two years is worth about $45.35 today because the same amount is a year further away. The $1,050 due after three years is worth about $907.03 today. Together those present values add up to $1,000.

Now take an average of the three waiting times. Give each waiting time influence in proportion to its share of the bond’s price. The first payment accounts for less than 5 percent of the price, so the one-year wait has little influence. The final payment accounts for about 91 percent, so the three-year wait does most of the work. The average comes to about 2.86 years. This is the bond’s **Macaulay duration**.

It’s easy to read 2.86 years as the date when you get your money back. The payment schedule gives you the actual dates. You still receive most of the money at the end of year three. Macaulay duration describes where the payments sit in time when you give the payments worth more today greater weight. How does that average help you estimate the change in price?

## Turning duration into a price estimate

Your bond’s Macaulay duration of 2.86 years puts most of the weight near year three. That matters because a higher yield reduces the present value of a later payment by a larger percentage than it reduces the present value of an earlier one. To find what a payment three years away is worth today, you divide by the yearly growth factor three times. For a payment one year away, you divide once. Raising the yield increases that divisor each time you use it.

The measure used for the price estimate is called **modified duration**. With interest calculated once a year, divide Macaulay duration by one plus the yield written as a decimal. Here you divide about 2.86 by 1.05 and get about 2.72. That number tells you the approximate percentage change in price for each percentage point of change in yield, with the price moving in the opposite direction.

Suppose the yield rises from 5 percent to 6 percent. That’s a rise of one percentage point. With a modified duration of about 2.72, the estimated price drop is 2.72 percent, or about $27 on a $1,000 bond. That puts the estimated price at about $973.

You can check the estimate by finding the present value of each scheduled payment again, this time at 6 percent, and adding them. The result is about $973.27. The two answers are close because modified duration measures how sensitive the price is at the starting yield. That sensitivity changes as the yield moves. For a larger move, the estimate can stray further from the recalculated price. What connects the average waiting time to that local estimate?

## The whole picture

Bond duration connects when a bond pays with how its price responds to a change in yield. Macaulay duration gives each payment a weight based on what it contributes to the price today, so a large payment far in the future pulls the average waiting time towards its date. Those later payments are also more sensitive to yield changes, because the yearly rate enters their present-value calculation more times. Modified duration expresses that sensitivity as an approximate price change at the bond’s current yield.