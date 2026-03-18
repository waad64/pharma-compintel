import schedule
import time
import subprocess
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pharma_compintel.log'),
        logging.StreamHandler()
    ]
)

def run_data_extraction():
    """Run the data extraction process"""
    try:
        logging.info("Starting scheduled data extraction...")
        result = subprocess.run(['python', 'nasdaq_fetcher.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            logging.info("Data extraction completed successfully")
        else:
            logging.error(f"Data extraction failed: {result.stderr}")
            
    except Exception as e:
        logging.error(f"Error running data extraction: {e}")

def main():
    """Main scheduler function"""
    logging.info("Starting Pharma-CompIntel Scheduler...")
    
    extraction_day = os.getenv('EXTRACTION_DAY', 'sunday')
    extraction_time = os.getenv('EXTRACTION_TIME', '02:00')
    
    # Schedule weekly extraction based on environment variables
    getattr(schedule.every(), extraction_day.lower()).at(extraction_time).do(run_data_extraction)
    
    # Run initial extraction
    logging.info("Running initial data extraction...")
    run_data_extraction()
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    main()