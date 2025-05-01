# SPX-Volatility

This project focuses on constructing the **volatility surface** and **term structure** of SPX (S&P 500 Index) options using historical data. The goal is to estimate implied volatility across different strikes and maturities, and to visualize how volatility evolves both across the moneyness dimension and over time.

## Overview

The project includes:

- Data preparation and cleaning
- Black-Scholes model implementation
- Implied volatility estimation using numerical methods
- Visualization of the volatility surface and term structure

## 1. Data Collection & Management

### Source
Option chain data was obtained manually from the [Cboe SPX Quote Table](https://www.cboe.com/delayed_quotes/spx/quote_table):

1. Set **Options Range** and **Expiration** to "All"
2. Click "View Chain"
3. Scroll down and download the CSV file

### Preprocessing

- Only options with **non-zero bid, ask, and volume** were retained to avoid illiquid contracts.
- The **mid-price** (average of bid and ask) was used instead of the last traded price, to reduce noise and the impact of potential outliers.
- Data was split into two subsets: **calls** and **puts**, processed separately.

> Note: At the time of this project, Cboe APIs were not accessible. While web scraping was considered, its instability (CAPTCHAs, site structure changes) made it an unreliable solution. A future version should use API access to ensure scalability and robustness.

## 2. Black-Scholes Model & Missing Inputs

### Inputs & Assumptions

- **Risk-free rate:** Approximated using the **13-week U.S. Treasury yield**
- **Spot price:** Fetched in real-time from **Yahoo Finance** (S&P 500 index)
- **Historical volatility:** Estimated using the **2-month historical volatility** of SPY, a highly liquid ETF tracking the S&P 500

These inputs were used to compute theoretical prices and implied volatilities for each option.

## 3. Implied Volatility Estimation

To invert the Black-Scholes formula and retrieve implied volatility, the **Newton-Raphson algorithm** was implemented. Despite the risk of non-convergence, it offered a good balance between **speed and accuracy** for this project’s scope.

## 4. How to Run

To generate the plots for both the volatility surface and term structure:

```bash
python Execution.py
