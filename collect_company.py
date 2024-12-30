from alpha_vantage.fundamentaldata import FundamentalData
import pandas as pd

# Your API key
api_key = "YSQUQVQWGTMP4IBO"

# Initialize the FundamentalData object
fd = FundamentalData(key=api_key, output_format='json')  # Fetch data as JSON

# Define the symbol list
symbols = ['AAPL', 'NVDA', 'MSFT', 'AMZN', 'GOOG', 'GOOGL', 'META', 'TSLA', 'BRK/B', 'BRK.A',
    'TSM', 'AVGO', 'LLY', 'WMT', 'JPM', 'V', 'UNH', 'XOM', 'ORCL', 'MA', 'NVO', 'COST',
    'HD', 'PG', 'NFLX', 'JNJ', 'BAC', 'ABBV', 'CRM', 'SMFG', 'CVX', 'TMUS', 'SAP', 'ASML',
    'KO', 'MRK', 'WFC', 'TM', 'CSCO', 'AMD', 'CCZ', 'ADBE', 'ACN', 'PEP', 'LIN', 'NOW', 'NVS',
    'AXP', 'DIS', 'MS', 'IBM', 'MCD', 'BABA', 'AZN', 'PM', 'TMO', 'ABT', 'SHEL', 'GE', 'CAT',
    'ISRG', 'GS', 'VZ', 'TXN', 'QCOM', 'TBC', 'INTU', 'RY', 'DHR', 'BKNG', 'HSBC', 'TBB', 'HDB',
    'CMCSA', 'LYG', 'T', 'SPGI', 'NEE', 'BLK', 'RTX', 'FMX', 'PGR', 'UBER', 'LOW', 'PLTR', 'AMAT',
    'HON', 'AMGN', 'UL', 'SCHW', 'SYK', 'ETN', 'PFE', 'ARM', 'UNP', 'SHOP', 'MUFG', 'TJX', 'KKR',
    'PDD', 'BX', 'C', 'BHP', 'BSX', 'TTE', 'ANET', 'PANW', 'DE', 'ADP', 'FI', 'LMT', 'COP', 'BMY',
    'SONY', 'SNY', 'VRTX', 'NKE', 'GILD', 'CB', 'SBUX', 'MMC', 'UPS', 'BA', 'APP', 'UBS', 'MDT',
    'ADI', 'MU', 'IBN', 'PLD', 'RACE', 'INTC', 'LRCX', 'SHW', 'MELI', 'TD', 'APO', 'MO', 'AMT',
    'SO', 'ELV', 'SPOT', 'BUD', 'CI', 'TT', 'EQIX', 'GEV', 'BN', 'ENB', 'INFY', 'PBR', 'ICE', 'MCO',
    'WM', 'PH', 'CTAS', 'KLAC', 'DUK', 'DELL', 'RELX', 'APH', 'MDLZ', 'ABNB', 'SNPS', 'PYPL',
    'CRWD', 'CDNS', 'CME', 'MRVL', 'PNC', 'AON', 'REGN', 'BTI', 'WELL', 'MSI', 'HCA', 'CMG', 'USB',
    'ITW', 'ZTS', 'MAR', 'CL', 'RIO', 'MCK', 'BP', 'SCCO', 'CEG', 'MSTR', 'EMR', 'GD', 'COIN', 'APD',
    'CVS', 'TRI', 'EOG', 'EPD', 'DASH', 'FTNT', 'FDX', 'MMM', 'ORLY', 'CNQ', 'COF', 'SAN', 'CP',
    'GSK', 'EQNR', 'TDG', 'NOC', 'ECL', 'CSX', 'CNI', 'BNS', 'CRH', 'BMO', 'TEAM', 'WMB', 'CARR',
    'AJG', 'RSG', 'TTD', 'WDAY', 'DEO', 'ET', 'RCL', 'MFG', 'SE', 'OKE', 'BDX', 'ADSK', 'DLR', 'FCX',]  
# Initialize a list to hold data
data = []

# Fetch data for each symbol
for symbol in symbols:
    try:
        # Fetch company overview
        overview, _ = fd.get_company_overview(symbol)

        # Extract market cap and shares outstanding to calculate price per share
        market_cap = float(overview.get('MarketCapitalization', 0))
        shares_outstanding = float(overview.get('SharesOutstanding', 0))
        
        # Calculate price per share (handle cases where shares_outstanding is 0)
        if shares_outstanding > 0:
            price_per_share = f"{market_cap / shares_outstanding:.2f}" # Rounded to 2 decimals
        else:
            price_per_share = None
        
        overview['PricePerShare'] = price_per_share  # Add to the data

        data.append(overview)  # Append the enriched dictionary
    except Exception as e:
        None
# Convert list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
output_file = 'data_2024_1230.csv'
df.to_csv(output_file, index=False)
print(f"Financial data has been successfully saved to '{output_file}'.")
