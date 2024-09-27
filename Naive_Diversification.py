import yfinance as yf 
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

sharpe_ratios_df = pd.read_excel('sharpe_ratios.xlsx')
top_100_sharpe_stocks = sharpe_ratios_df.sort_values(by='Sharpe Ratio', ascending=False).head(100)
top_sharpe_stocks = [stock.replace(' Return', '') for stock in top_100_sharpe_stocks['Stock']]

# 定義開始和結束日期
start = '2023-09-20'
end = '2024-09-20'

# 創建股票資料
def create_TW(id):
    try:
        df1 = yf.download(id, start=start, end=end)
        df1['Stock'] = id
        df1 = df1[['Stock', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']]
        df1['return'] = df1['Adj Close'].pct_change()
        return df1
    except Exception as e:
        print(f"抓取資料失敗 for {id}, 原因: {e}")
        return None

# ---------主程式-------------
ndf = pd.DataFrame(columns=top_sharpe_stocks)

data = []
for stock in top_sharpe_stocks:
    df = create_TW(stock)
    if df is not None:
        ndf[stock] = df['return']
        data.append(df)

if len(data) > 0:
    day = len(data[0])
    print(f"收錄股票數量: {len(top_sharpe_stocks)}")
    print(f"每日報酬: \n{ndf}")
else:
    print("未能成功載入任何股票資料，請檢查網路或API請求狀態。")

# n為隨機產生個數，ndf為全部股票資料,以此方程式計算個股標準差並進行回傳
def cal_std(n, ndf):
    testStock = random.sample(top_sharpe_stocks, n)
    testndf = ndf[testStock]
    testndf_cov = testndf.cov() * day
    weights = np.full([1, n], 1 / n)[0]
    p_std = np.dot(weights.T, np.dot(testndf_cov, weights))
    return float(p_std)

# 將結果以list方式存取，由n=1~n=100計算標準差
Result = []
for i in range(1, 101):
    result = cal_std(i, ndf)
    Result.append(result)

# 繪製Naïve Diversification圖表
plt.plot(Result)
plt.title('(TW)Naïve Diversification - Top 100 Sharpe Ratio Stocks Portfolio Risk')
plt.ylabel('Portfolio Variance')
plt.xlabel('Number of Stocks in Portfolio')
plt.show()

