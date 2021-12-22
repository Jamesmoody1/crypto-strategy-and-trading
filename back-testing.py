import data

if __name__ == "__main__":

    ''' Main idea for the back testing of a strategy:
        
        - Loop through the df from the earliest date.
        - When conditions are met, prime the script to enter a trade.
        - End the trade when the signal changes (later will be SL/TP triggered.
        - Mark the trade as a loss or a win depending on how trade went. 
        - Calculate win rate (more important for SL/TP triggered trading). 
        - Calculate net P/L after each trade. (Will need a start wallet amount for this.) '''

# First Strategy: Simple Moving Average Cross:
    balance = 200000
    trade_in_progress = False
    trades_made = 0
    # This all needs to be done in a loop through the data starting with the earlier date (Index 0)
    for i in range(len(data.df)):
        x = i + 1    
        sma_10 = data.df.loc[x, '10 SMA']
        sma_20 = data.df.loc[x, '20 SMA']
        sma_100 = data.df.loc[x, '100 SMA']
        if not trade_in_progress: 
        # Are 10 and 20 SMA above 100?
            if sma_10 > sma_100 and sma_20 > sma_100:
            # Prime trade when 20 is above 10.
                # When trade is primed and when 10 crosses 20 to upside, execute trade at close price of crossing candle.
                if sma_10 > sma_20 and true_primed:
                    trade_entry_price = data.df.loc[x, 'Close']
                    # print(f"Trade entry price is {trade_entry_price}")
                    # print(x)
                    # print(
                    #     f"10 SMA is {sma_10}. "
                    #     f"20 SMA is {sma_20}. "
                    #     f"100 SMA is {sma_100}. \n"
                    #     f"Datetime is {data.df.loc[x, 'Datetime']}. "
                    # )
                    # Create a variable which turns off rest of trading until trade is completed.
                    trade_in_progress = True
                elif sma_20 > sma_10:
                    true_primed = True
            # If 10 doesn't cross when primed and 20 or 10 drop below 100, unprime trade.
            else:
                true_primed = False
        else:
            # Trade ends when 10 crosses 20 to the low side.
            if sma_20 > sma_10:
                trade_close_price = data.df.loc[x, 'Close']
                # print(f"Trade close price is {trade_close_price}")
                # print(x)
                # print(
                #         f"10 SMA is {sma_10}. "
                #         f"20 SMA is {sma_20}. "
                #         f"100 SMA is {sma_100}. \n"
                #         f"Datetime is {data.df.loc[x, 'Datetime']}. "
                # ) 
                trade_in_progress = False
                trades_made += 1
                # For each trade, account_balance += account_balance + (trade_close_price - trade_open_price)
                balance = balance - trade_entry_price + trade_close_price
                print(f'Trade PnL is {trade_close_price - trade_entry_price}! ')
                print(f'New Balance is ${balance}! ')
    print(f'Total trades made = {trades_made}! ')
