import pandas as pd
from itertools import combinations
import matplotlib.pyplot as plt
import sys

try:
    # Load and clean data
    df = pd.read_csv('data_1219.csv')

    # Change efficient header
    headers = ['Symbol', 'AssetType', 'Name', 'Description', 'CIK', 'Exchange', 'Currency', 'Country', 
            'Sector', 'Industry', 'Address', 'OfficialSite', 'FiscalYearEnd', 'LatestQuarter', 'MarketCapitalization', 
            'EBITDA', 'PER', 'PEGRatio', 'BookValue', 'DividendPerShare', 'DividendYield', 'EPS', 'RevenuePerShareTTM', 
            'ProfitMargin', 'OperatingMarginTTM', 'ReturnOnAssetsTTM', 'ROE', 'RevenueTTM', 'GrossProfitTTM', 
            'DilutedEPSTTM', 'QuarterlyEarningsGrowthYOY', 'QuarterlyRevenueGrowthYOY', 'AnalystTargetPrice', 'AnalystRatingStrongBuy', 
            'AnalystRatingBuy', 'AnalystRatingHold', 'AnalystRatingSell', 'AnalystRatingStrongSell', 'TrailingPE', 'ForwardPE', 
            'PriceToSalesRatioTTM', 'PBR', 'EVToRevenue', 'EVToEBITDA', 'Beta', '52WeekHigh', '52WeekLow', 
            '50DayMovingAverage', '200DayMovingAverage', 'SharesOutstanding', 'DividendDate', 'ExDividendDate', 'PricePerShare']
    df.columns = headers

    df['Beta'] = pd.to_numeric(df['Beta'], errors='coerce')
    df['PricePerShare'] = pd.to_numeric(df['PricePerShare'], errors='coerce')
    df['EVToEBITDA'] = pd.to_numeric(df['EVToEBITDA'], errors='coerce')
    df['PBR'] = pd.to_numeric(df['PBR'], errors='coerce')
    df['Name'] = df['Name'].str.strip().str.lower()

    """
    Here is a place to set conditions
    """
    # If you intend to invest many maney this is not needed
    choice = df[df['PricePerShare'] < 100]

    # Choice good company
    choice = choice[(choice['PBR'] < df['PBR'].mean() / 2) & (choice['PER'] < df['PER'].mean() / 2)]
    choice = choice.nlargest(10, 'EVToEBITDA') 
    choice = choice.nlargest(5, 'ROE').dropna(subset=['EVToEBITDA','PBR','PER', 'ROE', 'Beta', 'PricePerShare']) 

    # Define two kinds of dictionary Beta and Price per share
    betas = {row['Name']: row['Beta'] for _, row in choice.iterrows()}
    prices = {row['Name']: row['PricePerShare'] for _, row in choice.iterrows()}

    """# Define betas of Gold and Bond 
    bond_beta = 0.01
    gold_beta = 0.44
    betas.update({'bond': bond_beta, 'gold': gold_beta})
    prices.update({'bond': 100, 'gold': 2000})  # Example prices"""

    # Set up pattern of portfolio
    assets = list(betas.keys())
    portfolios = set()
    n = 3
    l = len(assets)
    for r in range(n, len(assets) + 1):
        for subset in combinations(assets, r):
            portfolios.add(subset) # It takes about 2 second till this line

    # Find out a proportion beta = 1
    minimize = 7
    maximize = 10
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
    
    
    # How much you invest
    min_budget = 200
    max_budget = 700
    valid_portfolio = []
    for budget in range(min_budget, max_budget, 100):
        for portfolio in proportion_list:
            investment = dict()
            total_value = 0
            skip_portfolio = False
            portfolio_beta = 0 
            valid_beta = 0
            for asset, proportion in portfolio.items():
                m = proportion * budget
                share = round(m // prices[asset])

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
            
            for asset, share in investment.items():
                asset_value = share * prices[asset]
                asset_weight = asset_value / total_value
                portfolio_beta += asset_weight * betas[asset]

            # Check beta 
            min_beta = 0.7
            max_beta = 1.0
    
            if investment in valid_portfolio:
                continue

            if (budget * 0.9 <= total_value <= budget):
                if min_beta <= portfolio_beta <= max_beta:
                    valid_beta += portfolio_beta
                    valid_portfolio.append(investment)
    if valid_portfolio:
        for i, p in enumerate(valid_portfolio):
            print(f"\nPortfolio {i + 1}:")
            for stock, share in p.items():
                print(f"{stock}: {share} share")
            print()
    else:
        print("No valid portfolio exist.")
    
    # Iterate through the valid portfolios
    for i, portfolio in enumerate(valid_portfolio):
        assets = list(portfolio.keys())  
        shares = list(portfolio.values())  
        
        plt.figure(figsize=(10, 6))  
        bar_width = 0.5
        plt.bar(assets, shares, color='green', edgecolor='black', width=bar_width)  
    
        plt.title(f"Portfolio {i + 1}", fontsize=16)  
        plt.xlabel("Assets", fontsize=12)  
        plt.ylabel("Number of Shares", fontsize=12)  
        plt.xticks(rotation=45, ha='right', fontsize=10)  
        plt.yticks(fontsize=10)  
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)  
        plt.tight_layout()  
        plt.show()
    

except KeyboardInterrupt:
    print("\nProgram interrupted by the user. Exiting...")
