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
    # Create a variable which turns off rest of trading until trade is completed.
    trade_in_progress = False
    trades_made = 0
    no_of_winners = 0
    no_of_losers = 0
    biggest_winner = 0
    biggest_loser = 0
    # This all needs to be done in a loop through the data starting with the earlier date (Index 0)
    for i in range(len(data.df)):
        x = i + 1    
        sma_10 = data.df.loc[x, '10 SMA']
        sma_20 = data.df.loc[x, '20 SMA']
        sma_100 = data.df.loc[x, '100 SMA']
        # Check if there is a trade in progress. If yes, do not look for new trades.
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
                pnl = trade_close_price - trade_entry_price
                if pnl < 0:
                    no_of_losers += 1
                    if pnl < biggest_loser:
                        biggest_loser = pnl
                elif pnl > 0:
                    no_of_winners += 1
                    if pnl > biggest_winner:
                        biggest_winner = pnl
                # print(f'Trade PnL is {pnl :.2f}! ')
                # print(f'New Balance is ${balance :.2f}! ')
    print(f'Total trades made = {trades_made}! ')
    print(f'Number of winning trades was: {no_of_winners}. Biggest Winner was {biggest_winner}, WOW! ')
    print(f'Number of losing trades was: {no_of_losers}. Biggest Loser was {biggest_loser}, Boooo! ')
    print(f'Win percentage was: {(no_of_winners / trades_made) * 100 :.2f}%. This does not show much as there was no defined SL/TPs')
    print(f'Total PnL was {balance - 200000 :.2f}. ')
    print(f'Final Balance is {balance :.2f}... ')

    # Machine learning to learn best swing low/high SL placement!
