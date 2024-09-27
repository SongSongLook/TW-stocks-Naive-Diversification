import pandas as pd

risk_free_rate_file = 'A13Rate.xlsx'
risk_free_rate_df = pd.read_excel(risk_free_rate_file)

daily_returns_file = 'daily_returns.xlsx'
daily_returns_df = pd.read_excel(daily_returns_file)

latest_risk_free_rate = risk_free_rate_df['定存利率-一年期-固定'].iloc[-1]

daily_risk_free_rate = latest_risk_free_rate / 100 / 365

sharp_ratios = {}

for column in daily_returns_df.columns[1:]: 
    stock_returns = daily_returns_df[column].dropna()
    
    excess_returns = stock_returns - daily_risk_free_rate
    
    if excess_returns.std() != 0:  
        sharp_ratio = excess_returns.mean() / excess_returns.std()
    else:
        sharp_ratio = None  
    
    sharp_ratios[column] = sharp_ratio

sharp_ratios_df = pd.DataFrame(list(sharp_ratios.items()), columns=['Stock', 'Sharpe Ratio'])

sharp_ratios_file = 'sharpe_ratios.xlsx'
sharp_ratios_df.to_excel(sharp_ratios_file, index=False)

sharp_ratios_file

