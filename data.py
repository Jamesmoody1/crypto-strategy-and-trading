from pandas.core.frame import DataFrame
import yfinance as yahooFinance 
import datetime
import pandas as pd
import numpy as np
import mplfinance as mpf
from matplotlib import pyplot as plt
import plotly.graph_objs as go
# from mpl_finance import candlestick2_ohlc

class DataCollector:
    def __init__(self) -> None:

        ''' Initialises an instance of the StrategyTest class. 
        
        Arguments
        -----
        None
        
        Returns
        ----- 
        None '''

        # startDate, endDate, as per our convenience we can modify
        self.startDate = datetime.datetime(2021, 12, 1) 
        self.endDate = datetime.datetime(2021, 12, 13)
        self.candleinterval = "15m"

    def get_data(self):
        btc_usd = yahooFinance.Ticker("BTC-USD")
        return btc_usd.history(interval=self.candleinterval, start=self.startDate, end=self.endDate)

    def plot_data(self, data):
        mpf.plot(data, type='candle', mav=(10, 20, 50), volume=True)

    def generate_sma(self, period, df) -> DataFrame:

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

if __name__ == "__main__":

    pd.set_option("display.min_rows", 60)
    # Create an instance of the class and grab initial data.
    datatest = DataCollector()
    data = datatest.get_data()
    df = pd.DataFrame(data)
    # Create an Index column for the DataFrame for easier looping.
    df['Index'] = [x+1 for x in range(len(df))]
    # Create a Datetime column from the initial df index.
    df['Datetime'] = df.index
    # Make the Index column the index of the DataFrame.
    df.set_index('Index', inplace=True)
    # Generate some SMAs.
    df = datatest.generate_sma(10, df)
    df = datatest.generate_sma(20, df)
    df = datatest.generate_sma(100, df)
    # Create a second DataFrame with Datetime as the index column.
    data_2 = df.set_index('Datetime')
    # Plot graph of SMAs.
    plt.plot(data_2['10 SMA'], label='10 SMA')
    plt.plot(data_2['20 SMA'], label='20 SMA')
    plt.plot(data_2['100 SMA'], label='100 SMA')
    plt.legend()
    plt.show(block=True)
    # ------------------------------------------
    # This code is for different plotting using plotly.graph_objs
    ''' datatest.plot_data(data)
    trace_1 = go.Candlestick(
        x=df['Datetime'], open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close']
    )
    trace_2 = go.Line(
        x=df['Datetime'], y=df['10 SMA']
    )
    trace_3 = go.Line(
        x=df['Datetime'], y=df['20 SMA']
    )
    trace_4 = go.Line(
        x=df['Datetime'], y=df['100 SMA']
    )
    chart_data = [trace_1, trace_2, trace_3, trace_4]
    fig = go.Figure(data=chart_data)
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_traces(marker_line_color=['#1CFFCE', '#F1CEBB', '#444444'], selector=dict(type='line'))
    fig.show() '''
