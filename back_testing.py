import yfinance as yahooFinance 
import datetime
import pandas as pd


# startDate , as per our convenience we can modify
startDate = datetime.datetime(2021, 12, 1) 
# endDate , as per our convenience we can modify
endDate = datetime.datetime(2021, 12, 12)

btc_usd = yahooFinance.Ticker("BTC-USD")

print(type(btc_usd.history(period="6mo",start=startDate, end=endDate)))