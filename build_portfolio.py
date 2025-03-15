import pandas as pd
from itertools import combinations
from math import floor
import sys
from tabulate import tabulate

# Choose company you want

"""# Focus growth
def select(dataframe):
    sectors = ['LIFE SCIENCES', 'TECHNOLOGY', 'ENERGY & TRANSPORTATION']
               
    grouped = dataframe.groupby('Sector')

    companys = []

    for sector, group in grouped:
        if sector not in sectors:
            continue
        else:
            #choice = group[group['PricePerShare'] < 250]
            #choice = choice[choice['PER'] < choice['PER'].quantile(0.25)]
            choice = group[group['PER'] < group['PER'].quantile(0.25)]
            choice = choice.nlargest(3, 'ROE').dropna(subset=['DividendYield', 'EVToEBITDA','PBR','PER', 'ROE', 'Beta'])
            companys.append(choice)
    
     # Combine all selected companies into a single DataFrame
    return pd.concat(companys) if companys else pd.DataFrame()"""

# Focus Income
def select(dataframe):
    sectors = ['FINANCE', 'REAL ESTATE & CONSTRUCTION', 'ENERGY & TRANSPORTATION', 'TRADE & SERVICES']
               
    grouped = dataframe.groupby('Sector')

    companys = []

    for sector, group in grouped:
        if sector not in sectors:
            continue
        else:
            choice = group[(group['DividendYield'] > 0.03) & (group['PER'] < group['PER'].mean())]
            choice = choice[choice['ROE'] > 0.1]
            choice = choice[choice['Beta'] < 1]
    
      # Select top 2 by Dividend Yield
        selected = choice.nlargest(2, 'DividendYield').dropna(subset=['DividendYield', 'PER', 'ROE', 'Beta'])
        companys.append(selected)

    return pd.concat(companys) if companys else pd.DataFrame()
"""
def select(dataframe):
    sectors = ['MANUFACTURING', 'TRADE & SERVICES']
               
    grouped = dataframe.groupby('Sector')

    companys = []

    for sector, group in grouped:
        if sector not in sectors:
            continue
        else:
            #choice = group[group['PricePerShare'] < 250]
            #choice = choice[choice['PER'] < choice['PER'].quantile(0.25)]
            choice = group[group['PER'] < group['PER'].quantile(0.25)]
            choice = choice.nlargest(3, 'ROE').dropna(subset=['DividendYield', 'EVToEBITDA','PBR','PER', 'ROE', 'Beta'])
            companys.append(choice)
    
     # Combine all selected companies into a single DataFrame
    return pd.concat(companys) if companys else pd.DataFrame()"""

# How torelate aganst risk you are
def risk_torelence():
    min_beta = 7
    max_beta = 9
    return min_beta, max_beta

# How much you invest
def budget():
    min_bud = 4000
    max_bud = 5000
    return min_bud, max_bud

# Define min-size of portfolio
def min_size():
    min_asset = 6
    return min_asset

def adjust():
    interval = 500
    return interval

try:
    # Load and clean data
    df = pd.read_csv('data_2025_0101.csv')

    # Change efficient header
    headers = ['Symbol', 'AssetType', 'Name', 'Description', 'CIK', 'Exchange', 'Currency', 'Country', 
            'Sector', 'Industry', 'Address', 'OfficialSite', 'FiscalYearEnd', 'LatestQuarter', 'Map', 
            'EBITDA', 'PER', 'PEGRatio', 'BookValue', 'DividendPerShare', 'DividendYield', 'EPS', 'RevenuePerShareTTM', 
            'ProfitMargin', 'OperatingMarginTTM', 'ReturnOnAssetsTTM', 'ROE', 'RevenueTTM', 'GrossProfitTTM', 
            'DilutedEPSTTM', 'QuarterlyEarningsGrowthYOY', 'QuarterlyRevenueGrowthYOY', 'AnalystTargetPrice', 'AnalystRatingStrongBuy', 
            'AnalystRatingBuy', 'AnalystRatingHold', 'AnalystRatingSell', 'AnalystRatingStrongSell', 'TrailingPE', 'ForwardPE', 
            'PriceToSalesRatioTTM', 'PBR', 'EVToRevenue', 'EVToEBITDA', 'Beta', '52WeekHigh', '52WeekLow', 
            '50DayMovingAverage', '200DayMovingAverage', 'SharesOutstanding', 'DividendDate', 'ExDividendDate', 'PricePerShare']
    df.columns = headers

    # Prepare for some error
    df['Beta'] = pd.to_numeric(df['Beta'], errors='coerce')
    df['PricePerShare'] = pd.to_numeric(df['PricePerShare'], errors='coerce')
    df['EVToEBITDA'] = pd.to_numeric(df['EVToEBITDA'], errors='coerce')
    df['PBR'] = pd.to_numeric(df['PBR'], errors='coerce')
    df['Name'] = df['Name'].str.strip().str.lower()

    """# Compare with whole stock
    df_show = df[['Beta', 'ROE', 'PER', 'PBR', 'EVToEBITDA']]
    print(df_show.describe())"""
    
    # Chose company
    choice = select(df)
    
    # Define some dictionary to access easily
    betas = {row['Name']: row['Beta'] for _, row in choice.iterrows()}
    prices = {row['Name']: row['PricePerShare'] for _, row in choice.iterrows()}
    sectors = {row['Name']: row['Sector'] for _, row in choice.iterrows()}
    roes = {row['Name']: row['ROE'] for _, row in choice.iterrows()}
    market_caps = {row['Name']: row['Map'] for _, row in choice.iterrows()}
    pers = {row['Name']: row['PER'] for _, row in choice.iterrows()}
    pbrs = {row['Name']: row['PBR'] for _, row in choice.iterrows()}
    evtoebitdas = {row['Name']: row['EVToEBITDA'] for _, row in choice.iterrows()}
    dividends = {row['Name']: row['DividendYield'] for _, row in choice.iterrows()}
    
    """# You can add your own company stock if you want
    name = 'toyota'
    toyota_beta = 1.09
    toyota_price = 199
    toyota_sector = 'MANUFACTURING'
    toyota_map = 264_960_000_000
    toyota_roe = 0.1581
    toyota_per = 9.9
    toyota_pbr = 1.20
    toyota_ev = 7.61
    toyota_div = 0.0261

    betas.update({name: toyota_beta})
    prices.update({name: toyota_price})  
    sectors.update({name: toyota_sector})
    roes.update({name: toyota_roe})
    market_caps.update({name: toyota_map})
    pers.update({name: toyota_per})
    pbrs.update({name: toyota_pbr})
    evtoebitdas.update({name: toyota_ev})
    dividends.update({name: toyota_div})"""

    # Set up pattern of portfolio
    assets = list(betas.keys())
    portfolios = set()
    n = min_size()
    l = len(assets)
    for r in range(n, l + 1):
        for subset in combinations(assets, r):
            portfolios.add(subset) 

    # Find out a proportion to correspond beta you want
    minimize, maximize = risk_torelence()
    proportion_list = []

    for beta in range(minimize, maximize + 1):
        beta = beta * 0.1
        for portfolio in portfolios:
            patterns = dict()
            total_proportion = 0
            for asset in portfolio:
                proportion = beta / betas[asset]
                total_proportion += proportion
                patterns[asset] = proportion
            if total_proportion == 0:
                continue

            # Normalize proportions to make sure they sum to 1
            scaling_factor = 1 / total_proportion
            for asset in patterns:
                patterns[asset] = round(patterns[asset] * scaling_factor, 2)
            
            proportion_list.append(patterns)
    
    # Define budjet
    min_budget, max_budget = budget()

    # Collect valid portfolio 
    valid_portfolio = []

    for budget in range(min_budget, max_budget, adjust()):
        for portfolio in proportion_list:
            investment = dict()
            total_value = 0
            skip_portfolio = False
            portfolio_beta = 0 
        
            for asset, proportion in portfolio.items():
                m = proportion * budget
                share = floor(m / prices[asset])

                if share == 0:
                    skip_portfolio = True
                    break

                investment[asset] = share
                total_value += share * prices[asset]

            if skip_portfolio:
                continue

            """# torerence
            if len(investment) < 5:
                continue"""
            
            # Calculate portfolio beta
            for asset, share in investment.items():
                portfolio_beta += (prices[asset] * share / total_value) * betas[asset]

            # Check beta constraints
            if not (minimize * 0.1 <= portfolio_beta <= maximize * 0.1):
                continue
    
            # Avoid duplicate portfolios
            if investment in valid_portfolio:
                continue
            
            # Ensure portfolio value meets budget constraints
            if (budget * 0.95 <= total_value <= budget):
                valid_portfolio.append(investment)

    # Show result
    if valid_portfolio:
        for i, portfolio in enumerate(valid_portfolio):
            line = '-' * 150
            print(f"\n{line}\n")
            print(f"Portfolio {i + 1}:")

            # Prepare table headers and data
            headers = ["Asset", "Sector", "Price", "Value", "Shares","Proportion", "Beta"]
            company_header = ["Asset", "Sector", "Market cap", "Price", "Beta", "DividendYield", "PER", "PBR", "EV/EVITDA", "ROE"]
            table_data = []
            company_data = []

            # Find out portfolio's total value to calculate proportion
            total_value = sum(prices[asset] * share for asset, share in portfolio.items())
            
            # Create table
            for asset, share in portfolio.items():
                sector = sectors[asset]
                price = prices[asset]
                value = price * share
                proportion = round(prices[asset] * share / total_value, 2) if total_value > 0 else 0
                beta = betas[asset]
                market_cap = f"{market_caps[asset]:,}"
                per = pers[asset]
                pbr = pbrs[asset]
                evtoebitda = evtoebitdas[asset]
                roe = roes[asset]
                dividend = f"{dividends[asset]:.2f}"
                table_data.append([asset, sector, price, value, share, proportion, beta])
                company_data.append([asset, sector, market_cap, price, beta, dividend, per, pbr, evtoebitda, roe])

            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            print(f"Total Value: ${total_value:,.0f}")
            total_beta = sum(row[-2] * row[-1] for row in table_data)
            print(f"Portfolio Beta: {total_beta:.2f}\n")

            # Compny information
            print("Information:\n")
            print(tabulate(company_data, headers=company_header, tablefmt='simple'))
            print(f"\n{line}\n")



    else:
        print("No valid portfolio exist.")
    
except KeyboardInterrupt:
    print("\nProgram interrupted by the user. Exiting...")