import numpy as np
import pandas as pd
import pandas_ta as ta


from utils import add_bearish_bullish, calculate_macd_impulse, supply_demand_signals, fibonacci_retracement, getRetracementLevel, TotalSignal_VOL, pointposbreaksell, pointposbreakbuy

# Extract the close price from the candlestick data
def datamanager(data):
        timedf = np.array([float(candlestick[0]) for candlestick in data])
        open_prices = np.array([float(candlestick[1]) for candlestick in data])
        high_prices = np.array([float(candlestick[2]) for candlestick in data])
        low_prices = np.array([float(candlestick[3]) for candlestick in data])
        close_prices = np.array([float(candlestick[4]) for candlestick in data])
        volume = np.array([float(candlestick[5]) for candlestick in data])
        df = pd.DataFrame({'Time':timedf,'Open':open_prices, 'High':high_prices, 'Low':low_prices,'Close': close_prices,'Volume': volume})
        df['Time'] = pd.to_datetime(df['Time'], unit='ms') - pd.Timedelta('03:00:00')
        
        df.set_index('Time', inplace=True)
        
        df = add_bearish_bullish(df)
        #df['EMA'] = df['Close'].rolling(window='7D', min_periods=8).mean()

        # Calculate MACD and replace MACDs_12_26_9 values
        df = calculate_macd_impulse(df, fast_period=12, slow_period=26, signal_period=9)

        df["dVWAP"]=np.gradient(ta.vwap(df.High, df.Low, df.Close, df.Volume)).cumsum()
        df["VWAP"]=ta.vwap(df.High, df.Low, df.Close, df.Volume)
        
        df['RSI']=ta.rsi(df.Close, length=9)
        df['dRSI']=np.gradient(ta.rsi(df.Close, length=9))
        df['d2RSI']=np.gradient(np.gradient(ta.rsi(df.Close, length=9)))
        #df['RSI'] = df['RSI'].cumsum()

        df['EMA'] = ta.ema(close=df['Close'], length=20)
        
        #df['EMAlong'] = ta.ema(close=df['Close'], length=100)
        df['EMAlong'] = df['Close'].rolling(window='7D', min_periods=8).mean()
        df['EMAhigh'] = ta.ema(close=df['High'], length=20)
        df['EMAlow'] = ta.ema(close=df['Low'], length=20)

        df['signal'] = supply_demand_signals(df)

        df['OBV'] = ta.obv(close=df['Close'], volume=df['Volume'])
        df['dOBV'] = np.gradient(ta.obv(close=df['Close'], volume=df['Volume']))

        df['atr'] = ta.atr(low=df['Low'],close=df['Close'],high=df['High'])
        my_bbands = ta.bbands(df.Close, length=20, std=2.5)

        df=df.join(my_bbands)

        def support(df1, l, n1, n2): #n1 n2 before and after candle l
            for i in range(l-n1+1, l+1):
                if(df1.Low[i]>df1.Low[i-1]):
                    return 0
            for i in range(l+1,l+n2+1):
                if(df1.Low[i]<df1.Low[i-1]):
                    return 0
            return 1

        def resistance(df1, l, n1, n2): #n1 n2 before and after candle l
            for i in range(l-n1+1, l+1):
                if(df1.High[i]<df1.High[i-1]):
                    return 0
            for i in range(l+1,l+n2+1):
                if(df1.High[i]>df1.High[i-1]):
                    return 0
            return 1

        sizeRetracement = 6

        df['RETRACEMENT'] = df.apply(lambda x: fibonacci_retracement( x['BBU_20_2.5'], x['BBL_20_2.5'] , sizeRetracement), axis=1 )

        level = getRetracementLevel(df.RETRACEMENT.iloc[-1], df.Close.iloc[-1], sizeRetracement)        

        backcandles = 20
        n1=3
        n2=0
        
        TotSignal = [0]*len(df)
        RetracementHigh = [0]*len(df)
        RetracementLow = [0]*len(df)
        Retracement1 = [0]*len(df)
        Retracement2 = [0]*len(df)
        Retracement3 = [0]*len(df)
        Retracement4 = [0]*len(df)
        
        for row in range(1,len(df)):
            level = getRetracementLevel(df.RETRACEMENT.iloc[-2], df.Close.iloc[-2], sizeRetracement)  
            RetracementHigh[row] = df.RETRACEMENT[row][5]
            RetracementLow[row] = df.RETRACEMENT[row][0]            
            Retracement1[row] = df.RETRACEMENT[row][1]
            Retracement2[row] = df.RETRACEMENT[row][2]
            Retracement3[row] = df.RETRACEMENT[row][3]
            Retracement4[row] = df.RETRACEMENT[row][4]
        df['RETRACEMENT_High'] = RetracementHigh
        df['RETRACEMENT_1'] = Retracement1
        df['RETRACEMENT_2'] = Retracement2
        df['RETRACEMENT_3'] = Retracement3
        df['RETRACEMENT_4'] = Retracement4
        df['RETRACEMENT_Low'] = RetracementLow
        
        for row in range(backcandles, len(df)-n2): #careful backcandles used previous cell
            ss = []
            rr = []
            for subrow in range(row-backcandles+n1, row+1):
                if support(df, subrow, n1, n2):
                    ss.append(df.Low[subrow])
                if resistance(df, subrow, n1, n2):
                    rr.append(df.High[subrow])

            TotSignal[row] = TotalSignal_VOL(df, row)
        df['TotalSignal'] = TotSignal

        df['pointposbreaksell'] = df.apply(lambda row: pointposbreaksell(row), axis=1)
        df['pointposbreakbuy'] = df.apply(lambda row: pointposbreakbuy(row), axis=1)

        return df