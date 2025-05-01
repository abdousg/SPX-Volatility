import pandas as pd
from datetime import datetime


class DataCleaning:
    """
    Class for cleaning SPX options data.
    Filters and prepares the raw market data to build a clean dataset
    for implied volatility calculations and volatility surface plotting.
    """

    def __init__(self, database):
        # Initialize main parameters
        self.database = database
        # New Put and Call databases cleaned, as attributes to be used later
        self.call_database, self.put_database = self.base_cleaning()

    def base_cleaning(self):
        """
        Cleans the database by removing expired options,
        filtering based on price and volumes.
        """
        today = pd.Timestamp(datetime.today().date())

        # First, we convert expiration dates
        self.database['Expiration Date'] = pd.to_datetime(self.database['Expiration Date'])
        self.database = self.database[self.database['Expiration Date'] > today]

        # Then, we select relevant columns, including Bid and Ask prices
        call_cols = ['Expiration Date', 'Calls', 'Last Sale', 'Bid', 'Ask', 'Volume', 'IV', 'Delta', 'Gamma', 'Strike']
        put_cols = ['Expiration Date', 'Puts', 'Last Sale.1', 'Bid.1', 'Ask.1', 'Volume.1', 'IV.1', 'Delta.1', 'Gamma.1', 'Strike']

        call_df = self.database[call_cols].copy()
        put_df = self.database[put_cols].copy()

        # We rename the columns
        call_df.columns = ['Expiration', 'Call', 'Last', 'Bid', 'Ask', 'Volume', 'IV', 'Delta', 'Gamma', 'Strike']
        put_df.columns = ['Expiration', 'Put', 'Last', 'Bid', 'Ask', 'Volume', 'IV', 'Delta', 'Gamma', 'Strike']

        # Create the column Price = (Bid + Ask) / 2
        call_df['Price'] = (call_df['Bid'] + call_df['Ask']) / 2
        put_df['Price'] = (put_df['Bid'] + put_df['Ask']) / 2

        # Filter options with reasonable prices (>1 to avoid deep OTM options) and volumes
        call_df = call_df[(call_df['Price'] > 1) & (call_df['Volume'] > 0)]
        put_df = put_df[(put_df['Price'] > 1) & (put_df['Volume'] > 0)]

        # We calculate time to maturity in years
        call_df['T'] = (call_df['Expiration'] - today).dt.days / 365
        put_df['T'] = (put_df['Expiration'] - today).dt.days / 365

        return call_df.reset_index(drop=True), put_df.reset_index(drop=True)


