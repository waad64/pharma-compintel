"""Data validation utilities"""

import pandas as pd
from typing import Tuple, List, Any
from src.utils.logger import logger

class DataValidator:
    """Validate data quality and integrity"""
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, str]:
        """Validate dataframe structure"""
        if df is None or df.empty:
            return False, "DataFrame is empty"
        
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            return False, f"Missing columns: {missing_cols}"
        
        logger.info(f"DataFrame validation passed: {len(df)} rows, {len(df.columns)} columns")
        return True, "Valid"
    
    @staticmethod
    def validate_numeric(value: Any, min_val: float = None, max_val: float = None) -> bool:
        """Validate numeric value"""
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_string(value: str, min_length: int = 1, max_length: int = None) -> bool:
        """Validate string value"""
        if not isinstance(value, str):
            return False
        if len(value) < min_length:
            return False
        if max_length and len(value) > max_length:
            return False
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe by removing duplicates and handling missing values"""
        df = df.drop_duplicates()
        df = df.fillna('N/A')
        logger.info(f"DataFrame cleaned: {len(df)} rows remaining")
        return df

class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle_error(error: Exception, context: str = "") -> dict:
        """Handle and log errors"""
        import hashlib
        from datetime import datetime
        
        error_id = hashlib.md5(f"{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        error_msg = {
            'id': error_id,
            'type': type(error).__name__,
            'message': str(error),
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        logger.error(f"Error [{error_id}]: {error_msg}")
        return error_msg
    
    @staticmethod
    def safe_execute(func, *args, default: Any = None, **kwargs) -> Any:
        """Execute function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorHandler.handle_error(e, func.__name__)
            return default
