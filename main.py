import requests
import json
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

from datamanager import datamanager


symbolsList = ["AGIX","MKR","ADA","BTC","ETH","SOL","MATIC","LINK","OP","BNB","FET","VET","DYDX","ALICE","GMX","XRP","DOGE","DOT","TRX","SHIB","AVAX","XMR","NMR","OCEAN"]#["USDT"]
#["AGIX","MKR","ADA","BTC","ETH","SOL","MATIC","LINK","OP","BNB","FET","VET","DYDX","ALICE","GMX","XRP","DOGE","DOT","TRX","SHIB","AVAX","XMR"]
for symbols in symbolsList:
    # Define the symbol you want to trade
    symbol2change = symbols
    symbol2offer = 'BUSD'
    symbol = symbol2change + symbol2offer

    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    price = float(response.json()["price"])

    # Define the API endpoint for placing a buy order
    order_url = "https://api.binance.com/api/v3/order"

    # Define the API key and secret for authentication
    api_key = "your_api_key_binance"
    api_secret = "your_api_secret_binance"


    # Define the type of the order (market or limit)
    order_type = "MARKET"

    # Add the API key to the request header
    headers = {
        "X-MBX-APIKEY": api_key
    }


    # if you put your api you can get your balance here:
    #balance0 = getBalance(symbol2offer,api_secret,headers)
    #print('started with=',balance0)

    # Continuously check the latest price of the symbol and execute the trade accordingly
    #intervalList = ['3m','5m','15m','30m','1h','2h','4h','1d','1w','1m']
    #intervalTail = [2000,2000,2000,2000,2000,2000,2000,2000,2000,2000]
    intervalEMA = ['1 min', '3 min','5 min', '15 min', '30 min', '1 hour', '2 hour']
    intervalList = ['1d']
    intervalTail = [2000]

    for interval,tail in zip(intervalList,intervalTail):
        
        # Binance API endpoint for getting the latest price of a symbol
        price_url = "https://api.binance.com/api/v3/klines?symbol=" + symbol + "&interval=" + interval + "&limit=2000"

        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        price = float(response.json()["price"])

        #print(price)
        # Get the historical 1-minute candlestick data for the symbol
        response = requests.get(price_url)
        data = json.loads(response.text)

        df = datamanager(data)
        
        # Get the latest close price
        current_price = df.Close[-1]
        
        j =0        
        
        buy_last_6 = df['pointposbreakbuy'].iloc[-1]
        sell_last_6 = df['pointposbreaksell'].iloc[-1]

        if not pd.isnull(sell_last_6) and not pd.isnull(buy_last_6):
            entry_exit = None
        elif not pd.isnull(buy_last_6):
            entry_exit = 'buy'
        elif not pd.isnull(sell_last_6):
            entry_exit = 'sell'
        else:
            entry_exit = None
        

        if not pd.isnull(df['pointposbreakbuy'].iloc[-1]):
            print('buy')
        if not pd.isnull(df['pointposbreaksell'].iloc[-2]):
            print('sell')

        df = df.tail(30)
        df.reset_index(inplace=True)
        if 'fig' in locals():
            pass
        else:   
            fig = go.Figure(data=[go.Candlestick(x=df.index,
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close']),
                            go.Scatter(x=df.index, y=df['EMAlong'], 
                                    line=dict(color='red', width=1), 
                                    name="EMAlong"),
                            go.Scatter(x=df.index, y=df['EMA'], 
                                    line=dict(color='grey', width=1), 
                                    name="EMA"),
                            go.Scatter(x=df.index, y=df['RETRACEMENT_1'], 
                                    line=dict(color='green', width=1), 
                                    name="RETRACEMENT_1"),
                            go.Scatter(x=df.index, y=df.RETRACEMENT_High, 
                                    line=dict(color='darkblue', width=2), 
                                    name="FibHigh"),
                            go.Scatter(x=df.index, y=df.RETRACEMENT_Low, 
                                    line=dict(color='navy', width=2), 
                                    name="FibLow"),
                            go.Scatter(x=df.index, y=df['RETRACEMENT_2'], 
                                    line=dict(color='red', width=1), 
                                    name="RETRACEMENT_2"),
                            go.Scatter(x=df.index, y=df['RETRACEMENT_3'], 
                                    line=dict(color='purple', width=1), 
                                    name="RETRACEMENT_3"),
                            go.Scatter(x=df.index, y=df['RETRACEMENT_4'], 
                                    line=dict(color='orange', width=1), 
                                    name="RETRACEMENT_4")])

            fig.add_scatter(x=df.index, y=df['pointposbreaksell'], mode="markers",
                            marker=dict(size=10, color="deeppink"),
                            name="Signal")
            fig.add_scatter(x=df.index, y=df['pointposbreakbuy'], mode="markers",
                            marker=dict(size=10, color="khaki"),
                            name="Signal")

        fig.data[0].update(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
        fig.data[1].update(x=df.index, y=df['EMAlong'])
        fig.data[2].update(x=df.index, y=df['EMA'])
        fig.data[3].update(x=df.index, y=df['RETRACEMENT_1'])
        fig.data[4].update(x=df.index, y=df['RETRACEMENT_High'])  
        fig.data[5].update(x=df.index, y=df['RETRACEMENT_Low']) 
        fig.data[6].update(x=df.index, y=df['RETRACEMENT_2'])
        fig.data[7].update(x=df.index, y=df['RETRACEMENT_3'])
        fig.data[8].update(x=df.index, y=df['RETRACEMENT_4'])
        fig.data[9].update(x=df.index, y=df.pointposbreaksell)
        fig.data[10].update(x=df.index, y=df.pointposbreakbuy)
        fig.update_layout(title=symbols)
        pyo.plot(fig, auto_open=True)
        #break
        time.sleep(5)
        