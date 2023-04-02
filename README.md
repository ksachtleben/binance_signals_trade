# Crypto Signals Bot README
This Crypto Signals Bot is a Python-based application that uses the Binance API to automate cryptocurrency trading. It fetches real-time data, analyzes it, and makes trading decisions based on various strategies like EMA crossover, Fibonacci retracement levels, and more. The bot supports multiple cryptocurrencies and can be easily customized to fit your trading preferences.

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
The bot will make trading decisions based on the analysis and execute trades accordingly.
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
