import requests
import pandas as pd
import json
import time
import ollama
import os
import yfinance as yf
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:1.5b-base')
OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '15'))
OLLAMA_RETRIES = int(os.getenv('OLLAMA_MAX_RETRIES', '2'))
WORKERS = int(os.getenv('ENRICHMENT_WORKERS', '10'))
LATEST_FILE = os.getenv('LATEST_FILENAME', 'pharma_compintel_latest.csv')

PHASE_MAP = {
    'discovery': 'Pre-clinical', 'ind-enabling': 'Pre-clinical', 'preclinical': 'Pre-clinical',
    'pre-clinical': 'Pre-clinical', 'phase 1': 'Phase 1', 'phase i': 'Phase 1',
    'mid phase 1': 'Phase 1', 'early phase': 'Phase 1', 'investigational': 'Phase 1',
    'phase 2': 'Phase 2', 'phase ii': 'Phase 2', 'phase 1/2': 'Phase 2',
    'phase 1b/2a': 'Phase 2', 'phase 2b': 'Phase 2', 'mid phase 2': 'Phase 2',
    'combined / transitional phases': 'Phase 2', 'clinical stage': 'Phase 2',
    'clinical trials': 'Phase 2', 'phase 3': 'Phase 3', 'phase iii': 'Phase 3',
    'phase 2/3': 'Phase 3', 'phase 3b': 'Phase 3', 'pivotal phase 2/3': 'Phase 3',
    'pivotal phase 3': 'Phase 3', 'phase iii / pivotal': 'Phase 3', 'late stage': 'Phase 3',
    'late-stage pipeline': 'Phase 3', 'registrational': 'Registration',
    'bla readiness': 'Registration', 'approved': 'Approved', 'fda approved': 'Approved',
    'approved / marketed': 'Approved', 'commercial': 'Approved',
}

def normalize_phase(raw):
    if not raw or raw == 'Not Available':
        return 'Not Available'
    return PHASE_MAP.get(str(raw).strip().lower(), raw)

def fetch_nasdaq_data():
    try:
        r = requests.get(
            'https://api.nasdaq.com/api/screener/stocks',
            params={'tableonly': 'true', 'limit': 10000, 'offset': 0,
                    'download': 'true', 'sector': 'Health Care'},
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json',
                     'Referer': 'https://www.nasdaq.com/market-activity/stocks/screener'},
            timeout=30
        )
        if r.status_code == 200:
            rows = r.json().get('data', {}).get('rows')
            if rows:
                df = pd.DataFrame(rows)
                print(f"Fetched {len(df)} healthcare companies from NASDAQ")
                return df
    except Exception as e:
        print(f"NASDAQ fetch failed: {e}")
    print("NASDAQ fetch failed — no data")
    return pd.DataFrame()

def _default_enrichment():
    return {
        'disease_area': 'Not Available', 'diseases': [],
        'clinical_phase': 'Not Available', 'profile': 'Not Available',
        'technology': 'Not Available', 'rationale': 'Not Available',
        'approved_products': [], 'pipeline': [], 'lead_product': 'Not Available',
        'partnerships': [], 'keywords': []
    }

def enrich_company(symbol, name):
    prompt = (f'Company: {name} ({symbol}). Pharma/biotech.\n'
              'Return ONLY valid JSON:\n'
              '{"disease_area":"","diseases":[],"clinical_phase":"","profile":"",'
              '"technology":"","rationale":"","approved_products":[],"pipeline":[],'
              '"lead_product":"","partnerships":[],"keywords":[]}')
    for attempt in range(OLLAMA_RETRIES):
        try:
            client = ollama.Client(host=OLLAMA_HOST)
            resp = client.chat(model=OLLAMA_MODEL,
                               messages=[{'role': 'user', 'content': prompt}],
                               options={'timeout': OLLAMA_TIMEOUT})
            content = resp['message']['content']
            s, e = content.find('{'), content.rfind('}') + 1
            if s != -1 and e != -1:
                return json.loads(content[s:e])
        except Exception:
            if attempt < OLLAMA_RETRIES - 1:
                time.sleep(1)
    return _default_enrichment()

def get_stock_info(symbol):
    try:
        info = yf.Ticker(symbol).info
        desc = info.get('longBusinessSummary', '')
        return {
            'website': info.get('website', 'N/A'),
            'employees': info.get('fullTimeEmployees', 'N/A'),
            'description': (desc[:500] + '...') if desc else 'N/A'
        }
    except Exception:
        return {'website': 'N/A', 'employees': 'N/A', 'description': 'N/A'}

def process_company(row):
    enrichment = enrich_company(row['symbol'], row['name'])
    enrichment['clinical_phase'] = normalize_phase(enrichment.get('clinical_phase'))
    stock = get_stock_info(row['symbol'])
    return {
        'symbol': row['symbol'], 'name': row['name'],
        'last_sale': row.get('lastsale', 'N/A'),
        'net_change': row.get('netchange', 'N/A'),
        'percent_change': row.get('pctchange', 'N/A'),
        'market_cap': row.get('marketCap', '0'),
        'country': row.get('country', 'N/A'),
        'ipo_year': row.get('ipoyear', 'N/A'),
        'volume': row.get('volume', '0'),
        'sector': row.get('sector', 'N/A'),
        'industry': row.get('industry', 'N/A'),
        'pipeline_link': f"https://www.nasdaq.com/market-activity/stocks/{row['symbol'].lower()}",
        'clinical_trials_link': f"https://clinicaltrials.gov/search?term={row['name'].replace(' ', '+')}",
        **enrichment,
        **stock
    }

def run():
    print("Starting Pharma-CompIntel extraction...")
    df = fetch_nasdaq_data()
    if df.empty:
        print("No data to process.")
        return

    total = len(df)
    results = []
    rows = [row for _, row in df.iterrows()]

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {executor.submit(process_company, row): row for row in rows}
        for i, future in enumerate(as_completed(futures), 1):
            try:
                results.append(future.result())
                print(f"[{i}/{total}] {futures[future]['symbol']} done")
            except Exception as e:
                print(f"Error: {e}")

    enriched_df = pd.DataFrame(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    enriched_df.to_csv(f"pharma_compintel_data_{timestamp}.csv", index=False)
    enriched_df.to_csv(LATEST_FILE, index=False)
    print(f"Saved {len(enriched_df)} companies to {LATEST_FILE}")

if __name__ == "__main__":
    run()
