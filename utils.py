import requests
import time
import hmac
import hashlib
import pandas_ta as ta
import numpy as np


def getBalance(currency2balance,api_secret,headers):
    # Define the parameters
    timestamp = str(int(time.time() * 1000))
    params = "timestamp=" + timestamp

    # Sign the request
    signature = hmac.new(api_secret.encode('utf-8'), params.encode('utf-8'), hashlib.sha256).hexdigest().upper()

    # Make the GET request
    response = requests.get("https://api.binance.com/api/v3/account?" + params + "&signature=" + signature, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response
        response_json = response.json()

        # Find the USDT balance
        for asset in response_json["balances"]:
            if asset["asset"] == currency2balance:
                #print("Your", currency2balance, "balance is:", float(asset["free"]))
                return float(asset["free"])
    else:
        print("Failed to retrieve balance:", response.text)
        return None

def pointposbreaksell(x):
    if x['TotalSignal']=='sell':
        return x['High']+1e-4
    else:
        return np.nan

def pointposbreakbuy(x):
    if x['TotalSignal']=='buy':
        return x['Low']-1e-4
    else:
        return np.nan

def where2sell(x):
    if x['where2sell']=='sold':
        return x['High']+1e-4
    else:
        return np.nan

def supply_demand_signals(df):
    N = len(df.Close)
    SD = np.zeros(N)
    signals = np.zeros(N)
    for i in range(N):
        if i == 0:
            SD[i] = 0
        else:
            if df.Close[i] > df.Close[i-1]:
                SD[i] = SD[i-1] + 1
            else:
                SD[i] = SD[i-1] - 1
    for i in range(1,N):
        if SD[i] > SD[i-1] and df.Close[i] > df.Close[i-1]:
            signals[i] = 1
        elif SD[i] < SD[i-1] and df.Close[i] < df.Close[i-1]:
            signals[i] = -1
    return signals

def closeResistance(df,l,levels,lim):
    if len(levels)==0:
        return 0
    c1 = abs(df.High[l]-min(levels, key=lambda x:abs(x-df.High[l])))<=lim
    c2 = abs(max(df.Open[l],df.Close[l])-min(levels, key=lambda x:abs(x-df.High[l])))<=lim
    c3 = min(df.Open[l],df.Close[l])<min(levels, key=lambda x:abs(x-df.High[l]))
    c4 = df.Low[l]<min(levels, key=lambda x:abs(x-df.High[l]))
    if( (c1 or c2) and c3 and c4 ):
        return 1
    else:
        return 0
    
def closeSupport(df,l,levels,lim):
    if len(levels)==0:
        return 0
    c1 = abs(df.Low[l]-min(levels, key=lambda x:abs(x-df.Low[l])))<=lim
    c2 = abs(min(df.Open[l],df.Close[l])-min(levels, key=lambda x:abs(x-df.Low[l])))<=lim
    c3 = max(df.Open[l],df.Close[l])>min(levels, key=lambda x:abs(x-df.Low[l]))
    c4 = df.High[l]>min(levels, key=lambda x:abs(x-df.Low[l]))
    if( (c1 or c2) and c3 and c4 ):
        return 1
    else:
        return 0


def fibonacci_retracement(high, low, n):
    retracement_levels = []
    for i in range(1, n +1):
        retracement_levels.append(low + (high - low) * i / n )
    return retracement_levels

def getRetracementLevel(fibo, currentPrice, size):
    for level in range(1,size):
        if(fibo[level-1] < currentPrice < fibo[level]):
            return level
    return 0

def add_bearish_bullish(df, threshold=1.5):
    """
    Given a DataFrame with volume data, adds two new columns to indicate whether
    the asset's volume movements are bearish or bullish, based on significant changes in volume.
    
    Args:
    - df: a pandas DataFrame with a column 'volume'
    - threshold: a float indicating the minimum number of IQRs away from
                the median required to set the bearish or bullish flag (default: 1.5)
    
    Returns:
    - a new pandas DataFrame with the same columns as df, plus two new columns
    named 'bearish' and 'bullish'
    """
    # Initialize the bearish and bullish columns to False
    df['bearish'] = False
    df['bullish'] = False
    
    # Calculate the gradient of the volume series
    volume_gradient = np.gradient(df['Volume'])
    
    # Calculate the median and IQR of the volume series
    volume_median = df['Volume'].median()
    volume_iqr = np.percentile(df['Volume'], 75) - np.percentile(df['Volume'], 25)
    #print(volume_median, volume_iqr)
    
    # Calculate the minimum volume change required to trigger a bearish or bullish flag
    threshold_volume = volume_median + threshold * volume_iqr
    
    # Set the bearish or bullish flag based on the sign and magnitude of the gradient
    df.loc[(volume_gradient < 0) & (df['Volume'].diff() <= -threshold_volume), 'bearish'] = True
    df.loc[(volume_gradient > 0) & (df['Volume'].diff() >= threshold_volume), 'bullish'] = True
    
    return df


def TotalSignal_VOL(df,l):
    buy_signals = []
    sell_signals = []
    # Initialize variables to track major and minor crossovers

    if df.MACD.iloc[l] > df.signal_line.iloc[l] and df.MACD.iloc[l-1] < df.signal_line.iloc[l-1] and df.bullish_MACD.iloc[l] and df.signal.iloc[l] == 1:
        buy_signals.append('buy_MACD_major')
        
    # Check if MACD line crosses below signal line
    if df.MACD.iloc[l] < df.signal_line.iloc[l] and df.MACD.iloc[l-1] > df.signal_line.iloc[l-1] and df.bearish_MACD.iloc[l] and df.signal.iloc[l] == -1:
        sell_signals.append('sell_MACD_major')
        
    # Other signals
    if df.EMAhigh.iloc[l] < df.Close.iloc[l] and df.EMA.iloc[l] < df.Close.iloc[l] and df.signal.iloc[l] == -1  and df.dRSI.iloc[l] < 0 and df.d2RSI.iloc[l] < 0 and df.dOBV.iloc[l] < 0:
        sell_signals.append('sellGPT')
    if df.EMAlow.iloc[l] > df.Close.iloc[l] and df.EMA.iloc[l] > df.Close.iloc[l] and df.signal.iloc[l] == 1 and df.dRSI.iloc[l] > 0 and df.d2RSI.iloc[l] > 0 and df.dOBV.iloc[l] > 0:
        buy_signals.append('buyGPT')

    """if df.RETRACEMENT_3.iloc[l] < df.EMAlong.iloc[l]:
        sell_signals.append('sellLong') """
    
    # If no clear signal, return most frequent action
    if len(buy_signals) > len(sell_signals):
        return 'buy'
    elif len(sell_signals) > len(buy_signals):
        return 'sell'



def calculate_macd_impulse(df, fast_period=12, slow_period=26, signal_period=9, threshold=1.5):
    """
    Calculates MACD using impulse method and adds the MACD line, signal line and histogram to the DataFrame.
    """
    # Calculate exponential moving averages of closing price for fast and slow periods
    ema_fast = ta.ema(df['Close'], length=fast_period)
    ema_slow = ta.ema(df['Close'], length=slow_period)
    
    # Calculate MACD line using impulse method
    macd_line = ema_fast - ema_slow
    
    # Calculate signal line using EMA of MACD line for signal period
    signal_line = ta.ema(macd_line, length=signal_period)
    
    # Calculate MACD histogram as the difference between MACD and signal line
    macd_histogram = macd_line - signal_line
    
    # Add MACD, signal line and histogram to DataFrame
    df['MACD'] = macd_line
    df['signal_line'] = signal_line
    df['MACD_histogram'] = macd_histogram
    
    # Convert any NaN values to 0
    df['MACD_histogram'] = df['MACD_histogram'].fillna(0)


    # Initialize the bearish and bullish columns to False
    df['bearish_MACD'] = False
    df['bullish_MACD'] = False
    
    # Calculate the gradient of the volume series
    macd_gradient = np.gradient(df['MACD'])
    
    # Calculate the median and IQR of the volume series
    macd_hist_median = df['MACD_histogram'].mean()
    macd_hist_std = df['MACD_histogram'].std()
    
    # Calculate the minimum volume change required to trigger a bearish or bullish flag
    threshold_volume = threshold * macd_hist_std
    
    # Set the bearish or bullish flag based on the sign and magnitude of the gradient
    df.loc[(macd_gradient < 0) & (abs(macd_histogram) >= threshold_volume), 'bearish_MACD'] = True
    df.loc[(macd_gradient > 0) & (abs(macd_histogram) >= threshold_volume), 'bullish_MACD'] = True
    
    return df
