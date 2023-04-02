# Crypto Signals Bot README
This trading algorithm is designed to provide trade signals and can also be used for backtesting. The trading algorithm for stock market tradind (buy-in-hold) and future market trading (open long and short positions) is still under testing, specifically for stop-loss and take-profit positions. If you have any questions or are interested in contributing, please feel free to contact us.

## Features
Real-time data fetching from the Binance API.
Analysis of historical candlestick data.
Implementation of various trading strategies like EMA crossover, Fibonacci retracement levels, and more.
Customizable trading intervals and indicators.
Real-time visualization of trading data using Plotly.
Supports multiple cryptocurrencies.
## Requirements
Python 3.6 or higher
Binance API key and secret
Packages: `requests`, `json`, `time`, `pandas`, `plotly`, `datamanager`
## Installation
Clone the repository or download the source code.
Install the required packages by running pip install -r requirements.txt in your terminal or command prompt.
Replace `your_api_key_binance` and `your_api_secret_binance` in the source code with your own Binance API key and secret.
Customize the `symbolsList` variable with the cryptocurrencies you want to trade.
## Usage
Run the `main.py` script in your terminal or command prompt.
The bot will fetch real-time data for the specified cryptocurrencies and analyze it using the implemented trading strategies.
It is possible to check the future trading market changing the `order_url` to `https://fapi.binance.com/fapi/v1/order`.
Real-time visualization of trading data will be displayed using Plotly.
## Customization
To change the trading interval, modify the `intervalList` variable in the source code. The available intervals are: '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1w', and '1m'.
To change the EMA intervals, modify the `intervalEMA` variable in the source code.
To add or remove cryptocurrencies, modify the `symbolsList` variable in the source code.
To adjust the trading strategies, modify the relevant code sections, such as EMA crossover and Fibonacci retracement levels.
## Disclaimer
This Crypto Trading Bot is for educational purposes only. The user assumes all risks associated with using this bot for live trading. The developer is not responsible for any financial losses incurred while using this bot. Always exercise caution and use your own discretion when trading cryptocurrencies.

## License
This project is licensed under the MIT License.

