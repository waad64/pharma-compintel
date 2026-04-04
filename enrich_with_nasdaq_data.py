import requests
import pandas as pd
import json
import time
from bs4 import BeautifulSoup
import re

print("="*100)
print("NASDAQ HEALTHCARE STOCK DATA EXTRACTION")
print("="*100)

# Load existing clinical trials data
csv_file = r'c:\Users\Waad_BOUZID\Desktop\compintel\clinical_trials_extracted.csv'
excel_file = r'c:\Users\Waad_BOUZID\Desktop\compintel\clinical_trials_extracted.xlsx'

df_trials = pd.read_csv(csv_file)
print(f"\nLoaded {len(df_trials)} clinical trial records")

# Extract unique companies
unique_companies = df_trials[['Company_Symbol', 'Company_Name']].drop_duplicates()
print(f"Unique companies to match: {len(unique_companies)}")

# NASDAQ API endpoint for screener
NASDAQ_API = "https://api.nasdaq.com/api/screener/stocks"

# Headers to mimic browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.nasdaq.com/market-activity/stocks/screener'
}

nasdaq_stocks = {}

print("\n" + "="*100)
print("FETCHING NASDAQ HEALTHCARE STOCK DATA")
print("="*100)

try:
    # Fetch healthcare stocks from NASDAQ API
    params = {
        'tableonly': 'true',
        'limit': 10000,
        'offset': 0,
        'download': 'true'
    }
    
    print("\nAttempting to fetch from NASDAQ API...")
    response = requests.get(NASDAQ_API, headers=headers, params=params, timeout=15)
    response.raise_for_status()
    
    data = response.json()
    print(f"API Response Status: {response.status_code}")
    
    if 'data' in data and 'rows' in data['data']:
        stocks = data['data']['rows']
        print(f"Total stocks fetched: {len(stocks)}")
        
        # Filter for healthcare sector only
        healthcare_count = 0
        for stock in stocks:
            try:
                symbol = stock.get('symbol', '').strip()
                name = stock.get('name', '').strip()
                sector = stock.get('sector', '').strip()
                
                # Only include healthcare sector
                if sector and 'health' in sector.lower():
                    nasdaq_stocks[symbol] = {
                        'symbol': symbol,
                        'name': name,
                        'last_sale': stock.get('lastsale', 'N/A'),
                        'net_change': stock.get('netchange', 'N/A'),
                        'pct_change': stock.get('pctchange', 'N/A'),
                        'market_cap': stock.get('marketCap', 'N/A'),
                        'country': stock.get('country', 'N/A'),
                        'ipo_year': stock.get('ipoYear', 'N/A'),
                        'volume': stock.get('volume', 'N/A'),
                        'sector': sector
                    }
                    healthcare_count += 1
            except Exception as e:
                continue
        
        print(f"Healthcare sector stocks found: {healthcare_count}")
    else:
        print("No data in API response, attempting alternative method...")
        nasdaq_stocks = {}

except Exception as e:
    print(f"API Error: {str(e)}")
    print("Attempting alternative scraping method...")
    nasdaq_stocks = {}

# Alternative: Try to fetch from NASDAQ screener page
if not nasdaq_stocks:
    print("\nAttempting to scrape NASDAQ screener page...")
    try:
        url = "https://www.nasdaq.com/market-activity/stocks/screener"
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Look for JSON data in the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find script tags with data
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'initialState' in script.string:
                try:
                    # Extract JSON from script
                    json_str = script.string
                    if 'initialState' in json_str:
                        start = json_str.find('{')
                        end = json_str.rfind('}') + 1
                        if start >= 0 and end > start:
                            json_data = json.loads(json_str[start:end])
                            print("Found data in page script")
                except:
                    continue
    except Exception as e:
        print(f"Scraping Error: {str(e)}")

print(f"\nTotal NASDAQ healthcare stocks in database: {len(nasdaq_stocks)}")

# Now match companies with NASDAQ data
print("\n" + "="*100)
print("MATCHING COMPANIES WITH NASDAQ DATA")
print("="*100)

# Create new columns for stock data
df_trials['NASDAQ_Symbol'] = 'N/A'
df_trials['NASDAQ_Name'] = 'N/A'
df_trials['Last_Sale'] = 'N/A'
df_trials['Net_Change'] = 'N/A'
df_trials['Pct_Change'] = 'N/A'
df_trials['Market_Cap'] = 'N/A'
df_trials['Country'] = 'N/A'
df_trials['IPO_Year'] = 'N/A'
df_trials['Volume'] = 'N/A'

matched_count = 0
unmatched_companies = set()

for idx, row in df_trials.iterrows():
    company_symbol = row['Company_Symbol']
    company_name = row['Company_Name']
    
    matched = False
    
    # Try matching by symbol first
    if company_symbol and company_symbol in nasdaq_stocks:
        stock_data = nasdaq_stocks[company_symbol]
        df_trials.at[idx, 'NASDAQ_Symbol'] = stock_data['symbol']
        df_trials.at[idx, 'NASDAQ_Name'] = stock_data['name']
        df_trials.at[idx, 'Last_Sale'] = stock_data['last_sale']
        df_trials.at[idx, 'Net_Change'] = stock_data['net_change']
        df_trials.at[idx, 'Pct_Change'] = stock_data['pct_change']
        df_trials.at[idx, 'Market_Cap'] = stock_data['market_cap']
        df_trials.at[idx, 'Country'] = stock_data['country']
        df_trials.at[idx, 'IPO_Year'] = stock_data['ipo_year']
        df_trials.at[idx, 'Volume'] = stock_data['volume']
        matched = True
        matched_count += 1
    
    # If not matched by symbol, try by company name
    if not matched and company_name:
        for symbol, stock_data in nasdaq_stocks.items():
            # Check if company name matches (partial match)
            if company_name.lower() in stock_data['name'].lower() or stock_data['name'].lower() in company_name.lower():
                df_trials.at[idx, 'NASDAQ_Symbol'] = stock_data['symbol']
                df_trials.at[idx, 'NASDAQ_Name'] = stock_data['name']
                df_trials.at[idx, 'Last_Sale'] = stock_data['last_sale']
                df_trials.at[idx, 'Net_Change'] = stock_data['net_change']
                df_trials.at[idx, 'Pct_Change'] = stock_data['pct_change']
                df_trials.at[idx, 'Market_Cap'] = stock_data['market_cap']
                df_trials.at[idx, 'Country'] = stock_data['country']
                df_trials.at[idx, 'IPO_Year'] = stock_data['ipo_year']
                df_trials.at[idx, 'Volume'] = stock_data['volume']
                matched = True
                matched_count += 1
                break
    
    if not matched:
        unmatched_companies.add(company_name)

print(f"\nMatched records: {matched_count} out of {len(df_trials)}")
print(f"Unique unmatched companies: {len(unmatched_companies)}")

if unmatched_companies:
    print("\nUnmatched companies:")
    for company in sorted(unmatched_companies):
        print(f"  - {company}")

# Save enriched data to CSV
print("\n" + "="*100)
print("SAVING ENRICHED DATA")
print("="*100)

df_trials.to_csv(csv_file, index=False, encoding='utf-8')
print(f"✓ CSV updated: {csv_file}")

# Save enriched data to Excel
df_trials.to_excel(excel_file, index=False, sheet_name='Clinical Trials')
print(f"✓ Excel updated: {excel_file}")

# Show sample of enriched data
print("\n" + "="*100)
print("SAMPLE OF ENRICHED DATA")
print("="*100)

sample_cols = [
    'Company_Name',
    'NASDAQ_Symbol',
    'NASDAQ_Name',
    'Last_Sale',
    'Net_Change',
    'Pct_Change',
    'Market_Cap',
    'Country',
    'IPO_Year',
    'Volume'
]

print("\nFirst 5 enriched records:")
print(df_trials[sample_cols].head().to_string())

print("\n" + "="*100)
print("ENRICHMENT COMPLETE")
print("="*100)
print(f"Total records enriched: {len(df_trials)}")
print(f"Successfully matched: {matched_count}")
print(f"Not found on NASDAQ: {len(df_trials) - matched_count}")
