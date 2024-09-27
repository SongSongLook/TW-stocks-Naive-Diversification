import pandas as pd

file_path = 'TW Stock.csv'
df = pd.read_csv(file_path)

df.head()
df['Stock Code'] = df.iloc[1:, 0].str.split().str[0] + '.TW'

result_df = df[['Unnamed: 0', 'Stock Code']].rename(columns={'Unnamed: 0': 'Company'})

result_df = result_df.iloc[1:].reset_index(drop=True)

output_file_path = 'stock_codes_for_yfinance.xlsx'
result_df.to_excel(output_file_path, index=False)

output_file_path

