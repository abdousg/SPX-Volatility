import numpy as np
import matplotlib.pyplot as plt

def plot_volatility_surface(df, spot_price):
    """
    We plot a volatility surface by distinguishing between puts and calls based on moneyness.
    For strikes with moneyness less than 1.0, we use only out-of-the-money (OTM) puts.
    For strikes with moneyness greater than or equal to 1.0, we use out-of-the-money (OTM) calls and include at-the-money (ATM) options.
    """
    df = df.copy()
    df['Moneyness'] = df['Strike'] / spot_price
    df['T_rounded'] = (df['T'] * 365).round().astype(int)

    counts = df['T_rounded'].value_counts().sort_index()  # We count the number of observations for each maturity

    # We define target maturities (in days) and their corresponding tolerance windows
    horizons = {7: 2, 30: 3, 60: 3, 90: 5, 180: 10, 365: 15}

    best_days = []
    for target, window in horizons.items():
        # We find the best available maturity close to each target
        local_counts = counts[(counts.index >= target - window) & (counts.index <= target + window)]
        if not local_counts.empty:
            best_day = local_counts.idxmax()  # We select the maturity with the most available data
            best_days.append(best_day)
        else:
            best_days.append(target)  # We keep the target maturity if no close data is available

    ttm_grid = np.array(best_days) / 365  # We convert maturities back into years
    moneyness_grid = np.arange(0.80, 1.21, 0.05)  # We define the moneyness range from 0.80 to 1.20

    Z = []  # We initialize the implied volatility matrix
    for T_day in best_days:
        row = []
        filt_T = df[np.abs(df['T_rounded'] - T_day) <= 1]  # We select options close to the target maturity
        for m in moneyness_grid:
            if m < 1.0:
                # We select only OTM puts for moneyness below 1.0
                filt = filt_T[(filt_T['Moneyness'] < 1.0) & (np.abs(filt_T['Moneyness'] - m) < 0.07)]
                # We increase the moneyness range to get more points
            else:
                # We select OTM calls and ATM options for moneyness greater than or equal to 1.0
                filt = filt_T[(filt_T['Moneyness'] >= 1.0) & (np.abs(filt_T['Moneyness'] - m) < 0.07)]

            if not filt.empty:
                row.append(filt['Implied Vol'].mean())  # We average the implied volatilities if data is available
            else:
                row.append(np.nan)  # We assign NaN if no matching options are found
        Z.append(row)

    X, Y = np.meshgrid(ttm_grid, moneyness_grid)
    Z = np.array(Z).T

    # --- Plot ---
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', linewidth=0.3)
    ax.set_title("Volatility Surface")
    ax.set_xlabel("Time to Maturity (Years)")
    ax.set_ylabel("Moneyness (Strike / Spot)")
    ax.set_zlabel("Implied Volatility", labelpad=10)
    ax.invert_yaxis()
    ax.view_init(elev=30, azim=225)
    plt.tight_layout()
    plt.show()
