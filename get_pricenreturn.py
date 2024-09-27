import yfinance as yf
import pandas as pd
from datetime import datetime

tickers_df = pd.read_excel("ticker.xlsx")

start_date = "2023-09-20"
end_date = "2024-09-20"

all_data = pd.DataFrame()
returns_data = pd.DataFrame()

for index, row in tickers_df.iterrows():
    ticker = row['Stock Code']
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data = stock_data[['Close']]
    stock_data.columns = [f"{ticker} Close"]
    stock_data[f"{ticker} Return"] = stock_data[f"{ticker} Close"].pct_change()
    stock_data.reset_index(inplace=True)
    if all_data.empty:
        all_data = stock_data[['Date', f"{ticker} Close"]]
    else:
        all_data = pd.merge(all_data, stock_data[['Date', f"{ticker} Close"]], on='Date', how='outer')
    if returns_data.empty:
        returns_data = stock_data[['Date', f"{ticker} Return"]]
    else:
        returns_data = pd.merge(returns_data, stock_data[['Date', f"{ticker} Return"]], on='Date', how='outer')

all_data = all_data[['Date'] + [col for col in all_data.columns if col != 'Date']]
returns_data = returns_data[['Date'] + [col for col in returns_data.columns if col != 'Date']]

all_data.to_excel("stock_prices.xlsx", index=False)
returns_data.to_excel("daily_returns.xlsx", index=False)

print("收盤價數據-> stock_prices.xlsx，報酬率數據-> daily_returns.xlsx")

