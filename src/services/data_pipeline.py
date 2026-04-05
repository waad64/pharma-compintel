"""
Unified Data Pipeline for PCI Dashboard
Combines clinical trials extraction and NASDAQ enrichment in one process
"""

import openpyxl
import requests
import pandas as pd
import json
import time
import os
import logging
import sys
from urllib.parse import quote
from datetime import datetime
from typing import List, Dict, Optional

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_pipeline.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Setup base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration
CLINICAL_TRIALS_API = "https://clinicaltrials.gov/api/v2/studies"
NASDAQ_API = "https://api.nasdaq.com/api/screener/stocks"
RATE_LIMIT_DELAY = 0.5  # seconds

class DataPipeline:
    """Unified data pipeline for clinical trials and NASDAQ enrichment"""
    
    def __init__(self):
        self.companies_data = []
        self.all_trials = []
        self.nasdaq_stocks = {}
        self.enriched_data = None
        
    def load_excel_data(self, excel_file: str = None) -> bool:
        """Load company data from Excel file or use existing CSV"""
        try:
            if excel_file is None:
                # Try to find Excel file
                for file in os.listdir(BASE_DIR):
                    if file.endswith('.xlsx') and 'pharma' in file.lower():
                        excel_file = os.path.join(BASE_DIR, file)
                        break
            
            # If no Excel file found, check if we have existing clinical trials data
            csv_file = os.path.join(BASE_DIR, 'clinical_trials_extracted.csv')
            if not excel_file and os.path.exists(csv_file):
                logger.info(f"Using existing clinical trials data: {csv_file}")
                df = pd.read_csv(csv_file)
                self.all_trials = df.to_dict('records')
                logger.info(f"Loaded {len(self.all_trials)} records from existing CSV")
                return True
            
            if not excel_file or not os.path.exists(excel_file):
                logger.error(f"Excel file not found. Please provide pharma_compintel_latest.xlsx")
                logger.info(f"Files in directory: {[f for f in os.listdir(BASE_DIR) if f.endswith(('.xlsx', '.csv'))]}")
                return False
            
            logger.info(f"Loading Excel file: {excel_file}")
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
            
            for row in ws.iter_rows(min_row=4, values_only=True):
                if row[1]:  # Check if symbol exists
                    self.companies_data.append({
                        'symbol': row[1],
                        'name': row[2],
                        'disease_area': row[18],
                        'disease': row[17],
                        'lead_product': row[20],
                        'clinical_phase': row[19],
                        'technology': row[23],
                        'partnerships': row[24],
                        'competition_level': row[32],
                        'investor_highlights': row[29],
                        'trial_id': row[34],
                        'link_clinical_trials': row[13],
                        'link_NCT': row[35]
                    })
            
            logger.info(f"Loaded {len(self.companies_data)} companies from Excel")
            return True
        except Exception as e:
            logger.error(f"Error loading Excel: {str(e)}")
            return False
    
    def search_clinical_trials(self, company_name: str, disease_area: Optional[str] = None) -> List[Dict]:
        """Search clinicaltrials.gov API"""
        try:
            # Try searching by company name first
            params = {
                'query.term': company_name,
                'pageSize': 100,
                'format': 'json'
            }
            
            response = requests.get(CLINICAL_TRIALS_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('totalCount', 0) > 0:
                return data.get('studies', [])
            
            # If no results, try searching by disease area
            if disease_area:
                params['query.term'] = disease_area
                response = requests.get(CLINICAL_TRIALS_API, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                return data.get('studies', [])
            
            return []
        
        except Exception as e:
            logger.warning(f"Error searching for {company_name}: {str(e)}")
            return []
    
    def extract_trial_details(self, study: Dict) -> Optional[Dict]:
        """Extract relevant details from a trial"""
        try:
            protocol = study.get('protocolSection', {})
            identification = protocol.get('identificationModule', {})
            status = protocol.get('statusModule', {})
            conditions = protocol.get('conditionsModule', {})
            design = protocol.get('designModule', {})
            
            nct_id = identification.get('nctId', 'N/A')
            title = identification.get('officialTitle', 'N/A')
            
            # Extract diseases/conditions
            disease_list = conditions.get('conditions', [])
            diseases = ' | '.join(disease_list) if disease_list else 'N/A'
            
            # Extract clinical phase
            phases = design.get('phases', [])
            clinical_phase = ' | '.join(phases) if phases else 'N/A'
            
            # Extract study type
            study_type = design.get('studyType', 'N/A')
            
            # Extract status
            overall_status = status.get('overallStatus', 'N/A')
            
            return {
                'nct_id': nct_id,
                'title': title,
                'diseases': diseases,
                'clinical_phase': clinical_phase,
                'study_type': study_type,
                'overall_status': overall_status
            }
        except Exception as e:
            logger.warning(f"Error extracting trial details: {str(e)}")
            return None
    
    def extract_clinical_trials(self) -> bool:
        """Extract clinical trials for all companies"""
        try:
            logger.info("Starting clinical trials extraction...")
            
            for idx, company in enumerate(self.companies_data):
                logger.info(f"[{idx+1}/{len(self.companies_data)}] Processing: {company['name']}")
                
                # Search API
                trials = self.search_clinical_trials(
                    company['name'],
                    company['disease_area']
                )
                
                if trials:
                    logger.info(f"  Found {len(trials)} trials")
                    for trial in trials:
                        trial_details = self.extract_trial_details(trial)
                        if trial_details:
                            self.all_trials.append({
                                'Company_Symbol': company['symbol'],
                                'Company_Name': company['name'],
                                'Disease_Area': company['disease_area'],
                                'Disease': company['disease'],
                                'Lead_Product': company['lead_product'],
                                'Clinical_Phase': company['clinical_phase'],
                                'Technology': company['technology'],
                                'Partnerships': company['partnerships'],
                                'Competition_Level': company['competition_level'],
                                'Investor_Highlights': company['investor_highlights'],
                                'Trial_NCT_ID': trial_details['nct_id'],
                                'Trial_Title': trial_details['title'],
                                'Trial_Diseases': trial_details['diseases'],
                                'Trial_Clinical_Phase': trial_details['clinical_phase'],
                                'Trial_Study_Type': trial_details['study_type'],
                                'Trial_Overall_Status': trial_details['overall_status']
                            })
                else:
                    logger.info(f"  No trials found")
                
                # Rate limiting
                time.sleep(RATE_LIMIT_DELAY)
            
            logger.info(f"Total trials extracted: {len(self.all_trials)}")
            return True
        except Exception as e:
            logger.error(f"Error extracting clinical trials: {str(e)}")
            return False
    
    def fetch_nasdaq_data(self) -> bool:
        """Fetch NASDAQ healthcare stock data"""
        try:
            logger.info("Fetching NASDAQ healthcare stock data...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Referer': 'https://www.nasdaq.com/market-activity/stocks/screener'
            }
            
            params = {
                'tableonly': 'true',
                'limit': 10000,
                'offset': 0,
                'download': 'true'
            }
            
            response = requests.get(NASDAQ_API, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"API Response Status: {response.status_code}")
            
            if 'data' in data and 'rows' in data['data']:
                stocks = data['data']['rows']
                logger.info(f"Total stocks fetched: {len(stocks)}")
                
                # Filter for healthcare sector
                healthcare_count = 0
                for stock in stocks:
                    try:
                        symbol = stock.get('symbol', '').strip()
                        name = stock.get('name', '').strip()
                        sector = stock.get('sector', '').strip()
                        
                        # Only include healthcare sector
                        if sector and 'health' in sector.lower():
                            self.nasdaq_stocks[symbol] = {
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
                        logger.warning(f"Error processing stock: {str(e)}")
                        continue
                
                logger.info(f"Healthcare sector stocks found: {healthcare_count}")
                return True
            else:
                logger.warning("No data in API response")
                return False
        
        except Exception as e:
            logger.error(f"Error fetching NASDAQ data: {str(e)}")
            return False
    
    def enrich_with_nasdaq(self) -> bool:
        """Match companies with NASDAQ data"""
        try:
            logger.info("Enriching data with NASDAQ information...")
            
            # Create DataFrame from trials
            df = pd.DataFrame(self.all_trials)
            
            # Add NASDAQ columns
            nasdaq_columns = {
                'NASDAQ_Symbol': 'N/A',
                'NASDAQ_Name': 'N/A',
                'Last_Sale': 'N/A',
                'Net_Change': 'N/A',
                'Pct_Change': 'N/A',
                'Market_Cap': 'N/A',
                'Country': 'N/A',
                'IPO_Year': 'N/A',
                'Volume': 'N/A'
            }
            
            for col, default_val in nasdaq_columns.items():
                df[col] = default_val
            
            # Match companies with NASDAQ data
            matched_count = 0
            unmatched_companies = set()
            
            for idx, row in df.iterrows():
                company_symbol = row['Company_Symbol']
                company_name = row['Company_Name']
                
                matched = False
                
                # Try matching by symbol first
                if company_symbol and company_symbol in self.nasdaq_stocks:
                    stock_data = self.nasdaq_stocks[company_symbol]
                    for col, val in stock_data.items():
                        if col == 'symbol':
                            df.at[idx, 'NASDAQ_Symbol'] = val
                        elif col == 'name':
                            df.at[idx, 'NASDAQ_Name'] = val
                        elif col == 'last_sale':
                            df.at[idx, 'Last_Sale'] = val
                        elif col == 'net_change':
                            df.at[idx, 'Net_Change'] = val
                        elif col == 'pct_change':
                            df.at[idx, 'Pct_Change'] = val
                        elif col == 'market_cap':
                            df.at[idx, 'Market_Cap'] = val
                        elif col == 'country':
                            df.at[idx, 'Country'] = val
                        elif col == 'ipo_year':
                            df.at[idx, 'IPO_Year'] = val
                        elif col == 'volume':
                            df.at[idx, 'Volume'] = val
                    matched = True
                    matched_count += 1
                
                # If not matched by symbol, try by company name
                if not matched and company_name:
                    for symbol, stock_data in self.nasdaq_stocks.items():
                        if company_name.lower() in stock_data['name'].lower() or \
                           stock_data['name'].lower() in company_name.lower():
                            for col, val in stock_data.items():
                                if col == 'symbol':
                                    df.at[idx, 'NASDAQ_Symbol'] = val
                                elif col == 'name':
                                    df.at[idx, 'NASDAQ_Name'] = val
                                elif col == 'last_sale':
                                    df.at[idx, 'Last_Sale'] = val
                                elif col == 'net_change':
                                    df.at[idx, 'Net_Change'] = val
                                elif col == 'pct_change':
                                    df.at[idx, 'Pct_Change'] = val
                                elif col == 'market_cap':
                                    df.at[idx, 'Market_Cap'] = val
                                elif col == 'country':
                                    df.at[idx, 'Country'] = val
                                elif col == 'ipo_year':
                                    df.at[idx, 'IPO_Year'] = val
                                elif col == 'volume':
                                    df.at[idx, 'Volume'] = val
                            matched = True
                            matched_count += 1
                            break
                
                if not matched:
                    unmatched_companies.add(company_name)
            
            logger.info(f"Matched records: {matched_count} out of {len(df)}")
            logger.info(f"Unique unmatched companies: {len(unmatched_companies)}")
            
            self.enriched_data = df
            return True
        
        except Exception as e:
            logger.error(f"Error enriching data: {str(e)}")
            return False
    
    def save_data(self) -> bool:
        """Save enriched data to CSV and Excel"""
        try:
            if self.enriched_data is None:
                logger.error("No enriched data to save")
                return False
            
            logger.info("Saving enriched data...")
            
            # Save to CSV
            csv_file = os.path.join(BASE_DIR, 'clinical_trials_extracted.csv')
            self.enriched_data.to_csv(csv_file, index=False, encoding='utf-8')
            logger.info(f"✓ CSV saved: {csv_file}")
            
            # Save to Excel
            excel_file = os.path.join(BASE_DIR, 'clinical_trials_extracted.xlsx')
            self.enriched_data.to_excel(excel_file, index=False, sheet_name='Clinical Trials')
            logger.info(f"✓ Excel saved: {excel_file}")
            
            return True
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return False
    
    def run(self) -> bool:
        """Execute the complete pipeline"""
        logger.info("="*80)
        logger.info("STARTING UNIFIED DATA PIPELINE")
        logger.info("="*80)
        
        start_time = datetime.now()
        
        # Step 1: Load Excel data (auto-detect file)
        if not self.load_excel_data():
            logger.error("Failed to load data")
            return False
        
        # Step 2: Extract clinical trials (skip if already loaded from CSV)
        if self.companies_data:
            if not self.extract_clinical_trials():
                logger.error("Failed to extract clinical trials")
                return False
        
        # Step 3: Fetch NASDAQ data
        if not self.fetch_nasdaq_data():
            logger.warning("Failed to fetch NASDAQ data, continuing without enrichment")
        
        # Step 4: Enrich with NASDAQ data
        if not self.enrich_with_nasdaq():
            logger.error("Failed to enrich data")
            return False
        
        # Step 5: Save data
        if not self.save_data():
            logger.error("Failed to save data")
            return False
        
        # Summary
        elapsed_time = datetime.now() - start_time
        logger.info("="*80)
        logger.info("PIPELINE COMPLETE")
        logger.info("="*80)
        logger.info(f"Total records processed: {len(self.enriched_data)}")
        logger.info(f"Execution time: {elapsed_time.total_seconds():.2f} seconds")
        logger.info(f"Data saved to: clinical_trials_extracted.csv and .xlsx")
        
        return True


def main():
    """Main entry point"""
    pipeline = DataPipeline()
    success = pipeline.run()
    
    if success:
        logger.info("Data pipeline executed successfully")
        return 0
    else:
        logger.error("Data pipeline failed")
        return 1


if __name__ == "__main__":
    exit(main())
