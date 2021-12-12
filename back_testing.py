import yfinance as yahooFinance 
import datetime
import pandas as pd
import mplfinance as mpf
# from mpl_finance import candlestick2_ohlc

class StrategyTest:
    def __init__(self):
        # startDate, endDate, as per our convenience we can modify
        self.startDate = datetime.datetime(2021, 12, 1) 
        self.endDate = datetime.datetime(2021, 12, 12)
        self.candleinterval = "15m"

    def get_data(self):
        btc_usd = yahooFinance.Ticker("BTC-USD")
        return btc_usd.history(interval=self.candleinterval, start=self.startDate, end=self.endDate)

    def plot_data(self, data):
        mpf.plot(data, type='candle', mav=(50, 100, 200), volume=True)
        
datatest = StrategyTest()
data = datatest.get_data()
datatest.plot_data(data)