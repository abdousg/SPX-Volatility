import pandas as pd
import yfinance as yf
import numpy as np
from Process import Processing
from VSurface import plot_volatility_surface
from TStructure import plot_volatility_term_structure
import sys

# ---- Instantiation ----
database = pd.read_csv("spx_quotedata.csv", sep=",", skiprows = 3)

# --- Missing values ---

ticker = "^GSPC" # To extract the spot price directly on yf, to have more precision
spot_price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]

# We download historical SPY data (proxy for S&P 500)
spy = yf.download("SPY", period="6mo", interval="1d")
spy['log_return'] = np.log(spy['Close'] / spy['Close'].shift(1))

# We Compute 60-day historical volatility (annualized)
hv60 = spy['log_return'].rolling(window=60).std() * np.sqrt(252)
hist_vol = hv60.dropna().iloc[-1]

# We Download short-term US Treasury yield (IRX is the 13 week T-Bill)
data = yf.download("^IRX", period="5d", interval="1d")
risk_free_rate = data['Close'].dropna().iloc[-1].item() / 100

print("Historical Volatility is : ", hist_vol, "Risk Free Rate is : ", risk_free_rate, " Spot price is : ", spot_price)
print("Code is running...")

# --- Instantiate Processing Class ---
processing = Processing(database, spot_price, risk_free_rate, hist_vol)

# --- Compute Implied Volatilises ---
processing.compute_implied_vol(option_type='put')
processing.compute_implied_vol(option_type='call')

# --- Retrieve Cleaned and Updated Databases ---
puts = processing.put_database
calls = processing.call_database

# --- Plot Volatility Surface for calls and puts options ---
df_total = pd.concat([puts, calls], ignore_index=True)
plot_volatility_surface(df_total, spot_price)

# --- Plot Term Structure for 100% Moneyness ---
plot_volatility_term_structure(df_total,spot_price)

# We exit the code now
sys.exit(0)