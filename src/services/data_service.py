"""Data service layer"""

import pandas as pd
import os
from typing import Optional, Dict, List
from src.utils.logger import logger
from src.utils.validators import DataValidator, ErrorHandler
from config.settings import Config

class DataService:
    """Handle data loading and processing"""
    
    @staticmethod
    def load_clinical_trials_data() -> Optional[pd.DataFrame]:
        """Load clinical trials data from CSV"""
        try:
            csv_file = os.path.join(Config.DATA_DIR, 'clinical_trials_extracted.csv')
            
            # Try current directory first
            if not os.path.exists(csv_file):
                csv_file = 'clinical_trials_extracted.csv'
            
            if not os.path.exists(csv_file):
                logger.error(f"Clinical trials data not found: {csv_file}")
                return None
            
            logger.info(f"Loading clinical trials data from: {csv_file}")
            df = pd.read_csv(csv_file)
            
            # Validate data
            is_valid, message = DataValidator.validate_dataframe(df, ['Company_Name', 'Trial_NCT_ID'])
            if not is_valid:
                logger.error(f"Data validation failed: {message}")
                return None
            
            logger.info(f"Loaded {len(df)} records from clinical trials data")
            return df
        
        except Exception as e:
            ErrorHandler.handle_error(e, "load_clinical_trials_data")
            return None
    
    @staticmethod
    def filter_data(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Apply filters to dataframe"""
        try:
            df_filtered = df.copy()
            
            if filters.get('disease_area') and filters['disease_area'] != 'All':
                df_filtered = df_filtered[df_filtered['Disease_Area'] == filters['disease_area']]
            
            if filters.get('disease') and filters['disease'] != 'All':
                df_filtered = df_filtered[df_filtered['Disease'] == filters['disease']]
            
            if filters.get('trial_status') and filters['trial_status'] != 'All':
                df_filtered = df_filtered[df_filtered['Trial_Overall_Status'] == filters['trial_status']]
            
            if filters.get('geography') and filters['geography'] != 'Global':
                df_filtered = df_filtered[df_filtered['Country'] == filters['geography']]
            
            logger.info(f"Applied filters: {len(df_filtered)} records remaining")
            return df_filtered
        
        except Exception as e:
            ErrorHandler.handle_error(e, "filter_data")
            return df
    
    @staticmethod
    def get_unique_values(df: pd.DataFrame, column: str) -> List[str]:
        """Get unique values from column"""
        try:
            values = sorted(df[column].dropna().unique().tolist())
            return values
        except Exception as e:
            ErrorHandler.handle_error(e, f"get_unique_values_{column}")
            return []
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str) -> bool:
        """Export dataframe to CSV"""
        try:
            filepath = os.path.join(Config.DATA_DIR, filename)
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"Data exported to CSV: {filepath}")
            return True
        except Exception as e:
            ErrorHandler.handle_error(e, "export_to_csv")
            return False
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame, filename: str, sheet_name: str = 'Data') -> bool:
        """Export dataframe to Excel"""
        try:
            filepath = os.path.join(Config.DATA_DIR, filename)
            df.to_excel(filepath, index=False, sheet_name=sheet_name)
            logger.info(f"Data exported to Excel: {filepath}")
            return True
        except Exception as e:
            ErrorHandler.handle_error(e, "export_to_excel")
            return False
