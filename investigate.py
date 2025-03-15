import pandas as pd
import tabulate

df = pd.read_csv('data_roic_2_7.csv')

cost_of_debt = {row['Name']: row['cost-of-debt'] for _, row in df.iterrows()}
cost_of_equity = {row['Name']: row['cost-of-equity'] for _, row in df.iterrows()}
wacc = {row['Name']: row['WACC'] for _, row in df.iterrows()}
roic = {row['Name']: row['ROIC'] for _, row in df.iterrows()}
roic_wacc = {row['Name']: row['ROIC-WACC'] for _, row in df.iterrows()}
profit_margin = {row['Name']: row['ProfitMargin'] for _, row in df.iterrows()}
dividen_yield = {row['Name']: row['DividendYield'] for _, row in df.iterrows()}
per = {row['Name']: row['PERatio'] for _, row in df.iterrows()}
pbr = {row['Name']: row['PriceToBookRatio'] for _, row in df.iterrows()}
roe = {row['Name']: row['ReturnOnEquityTTM'] for _, row in df.iterrows()}


data = []
for name in cost_of_debt.keys():
    data.append([name, round(per[name],2), pbr[name], round(roe[name], 2), round(profit_margin[name], 2), round(dividen_yield[name], 2), round(cost_of_debt[name], 2), round(cost_of_equity[name], 2), round(wacc[name], 2), round(roic[name], 2), roic_wacc[name]])

# Define the headers
headers = ["Name","PER", "PBR", "ROE", "Profit_Margin", "yeild", "Cost of Debt", "Cost of Equity", "WACC", "ROIC", "ROIC-WACC"]

# Display the data using tabulate
print(tabulate.tabulate(data, headers=headers, tablefmt="grid"))
