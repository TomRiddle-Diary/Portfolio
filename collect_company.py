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
    'AJG', 'RSG', 'TTD', 'WDAY', 'DEO', 'ET', 'RCL', 'MFG', 'SE', 'OKE', 'BDX', 'ADSK', 'DLR', 'FCX',
    'TFC', 'NGG', 'AFL', 'NSC', 'SLB', 'HLT', 'ROP', 'KMI', 'PCAR', 'GM', 'CM', 'PSA', 'MET', 'TGT',
    'TRV', 'CPRT', 'NXPI', 'PCG', 'SPG', 'BK', 'JD', 'SRE', 'GWW', 'SQ', 'MFC', 'NU', 'NTES', 'SNOW',
    'FICO', 'PSX', 'URI', 'CHTR', 'JCI', 'BBVA', 'AMP', 'ARES', 'ALL', 'DHI', 'AZO', 'MNST', 'ING',
    'CVNA', 'VST', 'PAYX', 'AEP', 'MPLX', 'ITUB', 'DDOG', 'ROST', 'CMI', 'FANG', 'MPC', 'PWR', 'TRP',
    'LNG', 'SU', 'O', 'FLUT', 'WCN', 'BCS', 'AXON', 'COR', 'D', 'ODFL', 'HWM', 'MSCI', 'VRT', 'AIG',
    'E', 'FAST', 'OXY', 'LEN', 'NDAQ', 'NEM', 'KMB', 'KVUE', 'AMX', 'TEL', 'LHX', 'PEG', 'FIS', 'CCI',
    'PRU', 'HES', 'AME', 'DFS', 'CPNG', 'VLO', 'HLN', 'KDP', 'ALC', 'F', 'EA', 'KR', 'TAK', 'BKR', 'STZ',
    'NWG', 'FERG', 'CTVA', 'LULU', 'TRGP', 'IR', 'CBRE', 'TCOM', 'GLW', 'HMC', 'VALE', 'EW', 'AEM',
    'VRSK', 'GRMN', 'DAL', 'XEL', 'OTIS', 'A', 'CTSH', 'IT', 'LVS', 'IMO', 'YUM', 'EXC', 'HBANL', 'KHC',
    'GEHC', 'VMC', 'MCHP', 'SYY', 'STLA', 'ACGL', 'HUBS', 'HEI', 'GIS', 'WIT', 'ONON', 'VEEV', 'NUE',
    'IQV', 'ARGX', 'MLM', 'NET', 'HSY', 'EXR', 'RMD', 'MTB', 'IRM', 'SLF', 'HUM', 'IDXX', 'CCEP', 'HIG',
    'HPQ', 'HBANM', 'DD', 'CCL', 'DB', 'ABEV', 'TPL', 'OWL', 'WAB', 'RBLX', 'ED', 'RJF', 'VICI', 'ROK',
    'HOOD', 'EIX', 'TTWO', 'ETR', 'AVB', 'CSGP', 'ALNY', 'WTW', 'EFX', 'UAL', 'LYV', 'BRO', 'FITB', 'ZS',
    'TW', 'CUK', 'WEC', 'ON', 'FCNCA', 'DOW', 'TSCO', 'DXCM', 'XYL', 'DECK', 'ANSS', 'WDS', 'BSBR',
    'BIDU', 'CNC', 'EBAY', 'FER', 'GOLD', 'GPN', 'IOT', 'KEYS', 'CAH', 'CHT', 'PPG', 'CVE', 'STT', 'SW',
    'EQR', 'CQP', 'MPWR', 'RKT', 'NVR', 'DOV', 'HBANP', 'WPM', 'BNTX', 'K', 'BNH', 'IX', 'GDDY', 'HAL',
    'PHM', 'HPE', 'ERIC', 'TROW', 'FTV', 'BR', 'EL', 'CHD', 'ECCF', 'TYL', 'CPAY', 'LYB', 'EQT', 'MTD',
    'AWK', 'VLTO', 'SYF', 'VTR', 'KB', 'ADM', 'WBD', 'HBAN', 'GIB', 'CCJ', 'DTE', 'TEF', 'ZM', 'BNJ', 'PPL',
    'WDC', 'SOJC', 'TPG', 'NTAP', 'GFS', 'RDDT', 'AEE', 'DVN', 'BCE', 'CINF', 'SMCI', 'HUBB', 'PHG', 'RYAAY',
    'WRB', 'LPLA', 'ROL', 'RF', 'CDW']  
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
output_file = 'data_1219.csv'
df.to_csv(output_file, index=False)
print(f"Financial data has been successfully saved to '{output_file}'.")
