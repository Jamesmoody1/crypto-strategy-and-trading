# %%
from pandas.core.frame import DataFrame
import yfinance as yahooFinance 
import datetime
import pandas as pd
import numpy as np
import mplfinance as mpf
from matplotlib import pyplot as plt
# from mpl_finance import candlestick2_ohlc

class StrategyTest:
    def __init__(self):
        # startDate, endDate, as per our convenience we can modify
        self.startDate = datetime.datetime(2021, 12, 1) 
        self.endDate = datetime.datetime(2021, 12, 5)
        self.candleinterval = "15m"

    def get_data(self):
        btc_usd = yahooFinance.Ticker("BTC-USD")
        return btc_usd.history(interval=self.candleinterval, start=self.startDate, end=self.endDate)

    def plot_data(self, data):
        mpf.plot(data, type='candle', mav=(10, 20, 50), volume=True)

    def initiate_sma(self, period, df) -> DataFrame:

        ''' Takes in a period and returns a Series of values for the simple
        moving average for the specified period. 
        
        Arguments
        -----
        period: int (The desired period for the SMA).
        df: DataFrame ( The initial Dataframe). 
        
        Returns
        -----
        df:  DataFrame (An updated DataFrame containing a Series relating
        to the SMA). '''
        
        # Initiates the list for the Series.
        series_list =  [np.nan for _ in range(period-1)] 
        
        # Loops through the data and creates a moving average Series for the DataFrame.
        rolling_count = period
        for _ in range(len(df)-period+1):
            start = rolling_count - (period - 1)
            end = rolling_count
            try:
                # If there is an error with the range we are looping through. Should never happen.
                if rolling_count > len(df):
                    print('Something went wrong with calculating SMA points. ')
                    raise Exception
                # Finds the mean for the SMA.
                else:
                    avg = df.loc[start:end, 'Close'].mean()
                    series_list.append(avg)
                rolling_count += 1
            except:
                raise Exception
        
        df[f'{period} SMA'] = series_list

        return df

        ''' If I want to make this function faster:
        
            - Try keeping a list of values the length of the
              period. Everytime you move up to the next value
              to calculate, add the new value and drop the 
              oldest one. 
              
            This should save some time as I don't need to 
            constantly grab and regrab numbers I have previously
            used. '''

pd.set_option("display.min_rows", 60)
datatest = StrategyTest()
data = datatest.get_data()
df = pd.DataFrame(data)
df['Index'] = [x+1 for x in range(len(df))]
df['Datetime'] = df.index
df.set_index('Index', inplace=True)
df = datatest.initiate_sma(10, df)
df = datatest.initiate_sma(20, df)
df = datatest.initiate_sma(100, df)
data_2 = df.set_index('Datetime')
plt.plot(data_2['10 SMA'], label='10 SMA')
plt.plot(data_2['20 SMA'], label='20 SMA')
plt.plot(data_2['100 SMA'], label='100 SMA')
plt.legend()
df.head(60)
# datatest.plot_data(data)