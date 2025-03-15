from alpha_vantage.fundamentaldata import FundamentalData
import pandas as pd

# Your API key
api_key = "YSQUQVQWGTMP4IBO"

# Initialize the FundamentalData object
fd = FundamentalData(key=api_key, output_format='json')  # Fetch data as JSON

# Define the symbol list
symbols = ['AXP', 'DIS', 'MS', 'IBM', 'MCD', 'BABA', 'AZN', 'PM', 'TMO', 'ABT', 'SHEL']  
# Initialize a list to hold data
data = []

# Fetch data for each symbol
for symbol in symbols:
    try:
        # correct company data
        overview, _ = fd.get_company_overview(symbol)
        income_statement, _ = fd.get_income_statement_annual(symbol)
        balance_sheet, _ = fd.get_balance_sheet_annual(symbol)

        # Extract market cap and shares outstanding to calculate price per share
        market_cap = float(overview.get('MarketCapitalization', 0))
        shares_outstanding = float(overview.get('SharesOutstanding', 0))
        
        # Calculate price per share (handle cases where shares_outstanding is 0)
        if shares_outstanding > 0:
            price_per_share = f"{market_cap / shares_outstanding:.2f}" # Rounded to 2 decimals
        else:
            price_per_share = None
        
        overview['PricePerShare'] = price_per_share  # Add to the data

        income_statement = pd.DataFrame(income_statement)
        balance_sheet = pd.DataFrame(balance_sheet)

        if not income_statement.empty and not balance_sheet.empty:

            # Cost of debt
            interest_payment = float(income_statement.get('interestExpense', 0)[0])
            if interest_payment == 0:
                break
            total_debt = float(balance_sheet.get('shortLongTermDebtTotal', 0)[0])
            if total_debt == 0:
                break
            tax_rate = 0.21

            cost_of_debt = (interest_payment / total_debt) * (1 - tax_rate) if total_debt > 0 else 0
            overview['cost-of-debt'] = round(cost_of_debt, 2)

            # Cost of equity
            risk_free_rate = 0.0425
            beta = float(overview.get('Beta', 0))
            if beta == 0:
                break
            ex_market_return = 0.125

            cost_of_equity = risk_free_rate + beta * (ex_market_return - risk_free_rate)
            overview['cost-of-equity'] = round(cost_of_equity, 2)

            # WACC
            ev = market_cap + total_debt
            wacc = ((market_cap * cost_of_equity) + (total_debt * cost_of_debt)) / ev if ev > 0 else 0

            overview['WACC'] = round(wacc, 2)

            # Nopat
            ebit = float(income_statement.get('ebit', 0)[0])
            if ebit == 0:
                break
            nopat = ebit * (1 - tax_rate)

            # Book equity
            total_equity = float(balance_sheet.get('totalShareholderEquity', 0)[0])
            if total_equity == 0:
                break

            # Cash and cash equivalents
            cash = float(balance_sheet.get('cashAndCashEquivalentsAtCarryingValue', 0)[0])
            if cash == 0:
                break
            # Invested Capital
            invested_capital = total_debt + total_equity - cash

            # Calculate ROIC
            if invested_capital > 0:
                roic = nopat / invested_capital
                overview['ROIC'] = round(roic, 2)
            else:
                roic = None

            # ROIC - WACC
            roic_wacc = round(roic - wacc, 2)
            overview['ROIC-WACC'] = roic_wacc

        else:
            print('there is no annual report')

        data.append(overview)  # Append the enriched dictionary
    except Exception as e:
        print(f"Error processing {symbol}: {e}")

# Convert list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
output_file = 'data_roic_2_7.csv'
df.to_csv(output_file, index=False)
print(f"Financial data has been successfully saved to '{output_file}'.")
