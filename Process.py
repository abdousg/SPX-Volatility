import numpy as np
from scipy.stats import norm
from DataCleaning import DataCleaning

class Processing(DataCleaning):
    """
    Class to compute theoretical Black-Scholes prices and implied volatilities,
    reusing cleaned data from DataCleaning.
    """

    def __init__(self, database, spot_price, risk_free_rate, historical_vol):
        super().__init__(database)
        # --- Attributs ---
        self.spot_price = spot_price
        self.risk_free_rate = risk_free_rate
        self.historical_vol = historical_vol

    def get_database(self, option_type):
        """
        Select the appropriate database based on the option type.
        """
        return self.put_database if option_type == 'put' else self.call_database

    def black_scholes_price(self, S, K, T, r, sigma, option_type):
        """
        Compute theoretical Black-Scholes price for a call or a put option.
        """
        if T <= 0 or sigma <= 0: # To avoid division per zero, return the instric value
            return max(0.0, S - K) if option_type == 'call' else max(0.0, K - S)

        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type == 'put':
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        else:
            return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    def function_to_approx(self, S, K, T, r, vol, option_type, market_price):
        """
        Returns the difference between Black-Scholes theoretical price and observed market price.
        """
        return self.black_scholes_price(S, K, T, r, vol, option_type) - market_price

    def d_function_to_approx(self, S, K, T, r, vol, option_type, market_price):
        """
        Numerical derivative (finite difference method) of the pricing function volatility.
        """
        dx = 1e-5
        f_plus = self.function_to_approx(S, K, T, r, vol + dx, option_type, market_price)
        f = self.function_to_approx(S, K, T, r, vol, option_type, market_price)
        return (f_plus - f) / dx

    def implied_volatility(self, S, K, T, r, vol_guess, option_type, market_price, eps=1e-5, max_iter=1000):
        """
        Computes implied volatility using Newton-Raphson method.
        """
        if T <= 0 or market_price <= 0:
            return np.nan

        intrinsic_value = max(0, K - S) if option_type == 'put' else max(0, S - K)
        if abs(market_price - intrinsic_value) < eps:
            return 0.0

        sigma = vol_guess

        for _ in range(max_iter): # Max iterations for the N-R algorithm
            try:
                f = self.function_to_approx(S, K, T, r, sigma, option_type, market_price)
                df = self.d_function_to_approx(S, K, T, r, sigma, option_type, market_price)

                if df == 0:
                    return np.nan # To avoid division per zero

                sigma_new = sigma - f / df

                if abs(sigma_new - sigma) < eps: # The stop condition
                    return max(sigma_new, 0.0)

                sigma = sigma_new

            except Exception:
                return np.nan

        return np.nan

    def compute_implied_vol(self, option_type):
        """
        Adds 'Implied Vol' columnn to the selected option DataFrame.
        """
        df = self.get_database(option_type).copy()

        # We compute Implied Volatility based on Price (Mid Price)
        df['Implied Vol'] = df.apply(
            lambda row: self.implied_volatility(
                S=self.spot_price,
                K=row['Strike'],
                T=row['T'],
                r=self.risk_free_rate,
                vol_guess=self.historical_vol,
                option_type=option_type,
                market_price=row['Price']
            ),
            axis=1
        )
        df = df.dropna(subset=['Implied Vol']).copy() # We delete the lines where Implied Vol can't be computed

        # We update the appropriate database, by updating the class' attributs
        if option_type == 'put':
            self.put_database = df
        else:
            self.call_database = df


