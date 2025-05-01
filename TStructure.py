import matplotlib.pyplot as plt

def plot_volatility_term_structure(df, spot_price):
    """
    Generate and plot the volatility term structure for ATM options.

    Parameters:
    - df: Options DataFrame
    """
    df = df.copy()
    df['Moneyness'] = df['Strike']/spot_price

    # We select options near 100% moneyness (± 0,1%)
    atm_df = df[
        (df['Moneyness'] >= 0.999) &
        (df['Moneyness'] <= 1.001) &
        (df['T'] <= 3.0)
        ]


    # Options are grouped by time to maturity and compute the average implied vol
    term_structure = atm_df.groupby('T')['Implied Vol'].mean().reset_index()
    term_structure = term_structure.sort_values(by='T')

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(term_structure['T'], term_structure['Implied Vol'], marker='o', linestyle='-', color='b')
    ax.set_title(f"Volatility Term Structure 100% Moneyness")
    ax.set_xlabel("Time to Maturity (Years)")
    ax.set_ylabel("Implied Volatility")
    ax.grid(True)
    plt.tight_layout()
    plt.show()
