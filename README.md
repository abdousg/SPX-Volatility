# SPX-Volatility
Volatility surface and Term Structure of SPX Options


Here is some information on how I approached the task:

Database management:
I chose to use the average of the bid and ask prices for each option, rather than the last traded price. To reduce the impact of outliers and avoid potential liquidity issues, I only included options with both a non-zero price and a non-zero trading volume. I then split the dataset into two subsets: one for call options and one for put options, so they could be processed separately.
Cboe APIs were not accessible at the time I was working on the task. I know that having access to live data is essential for this kind of project. In the absence of an API, one alternative would have been web scraping, but this method raises stability and reliability issues, especially due to CAPTCHAs or changes in the website’s structure. Using APIs is clearly the proper and scalable approach for data retrieval. Since Cboe does not oJer free API access, this is definitely something I would reconsider in the future.

You will need the data from cboe.com/delayed_quotes/spx/quote_table
- Select “Options Range” and “Expiration” to All, and click on “View Chain”
- Scroll down to the bottom and download csv

Black Scholes implementation & missing inputs:
While implementing the Black-Scholes model, I identified a few missing inputs: the risk- free rate, the historical volatility, and of course, the spot price of the S&P 500. Here is how I retrieved each of them:
- Risk-free rate: I used the 13-week US Treasury yield.
- Spot price: I pulled the real-time value from Yahoo Finance.
- Historical volatility: I used the 2-month historical volatility of the SPDR S&P 500
ETF (SPY), which closely tracks the S&P 500.

Implied Volatility estimation:
To compute the implied volatilities, I considered several numerical methods and ultimately chose the Newton-Raphson algorithm. Although it does not always guarantee convergence, it proved to be fast and eJective enough for the scope of this project.
To run the code:
Please run the “Execution.py” module. The volatility surface and the term structure will then appear in two diJerent windows.
