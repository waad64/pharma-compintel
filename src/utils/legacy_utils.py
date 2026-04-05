"""Production-grade utilities for PCI Dashboard"""

import logging
import functools
import time
from datetime import datetime, timedelta
import hashlib
import json
from typing import Any, Callable, Optional
import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    @staticmethod
    def track_execution(func: Callable) -> Callable:
        """Decorator to track function execution time"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"{func.__name__} executed in {execution_time:.2f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"{func.__name__} failed after {execution_time:.2f}s: {str(e)}")
                raise
        return wrapper

class CacheManager:
    """Manage caching with TTL support"""
    
    @staticmethod
    def cache_with_ttl(ttl_seconds: int = 3600):
        """Cache decorator with time-to-live"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}_{hashlib.md5(str(args).encode()).hexdigest()}"
                
                if cache_key in st.session_state:
                    cached_data, timestamp = st.session_state[cache_key]
                    if datetime.now() - timestamp < timedelta(seconds=ttl_seconds):
                        logger.info(f"Cache hit for {func.__name__}")
                        return cached_data
                
                result = func(*args, **kwargs)
                st.session_state[cache_key] = (result, datetime.now())
                logger.info(f"Cache miss for {func.__name__}")
                return result
            return wrapper
        return decorator

class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle_error(error: Exception, context: str = "") -> dict:
        """Handle and log errors"""
        error_id = hashlib.md5(f"{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        error_msg = {
            'id': error_id,
            'type': type(error).__name__,
            'message': str(error),
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        logger.error(json.dumps(error_msg))
        return error_msg
    
    @staticmethod
    def safe_execute(func: Callable, *args, default: Any = None, **kwargs) -> Any:
        """Execute function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            ErrorHandler.handle_error(e, func.__name__)
            return default

class DataValidator:
    """Validate data quality and integrity"""
    
    @staticmethod
    def validate_dataframe(df, required_columns: list) -> tuple[bool, str]:
        """Validate dataframe structure"""
        if df is None or df.empty:
            return False, "DataFrame is empty"
        
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            return False, f"Missing columns: {missing_cols}"
        
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

class SecurityManager:
    """Handle security-related operations"""
    
    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """Sanitize user input"""
        dangerous_chars = ['<', '>', '"', "'", '&', ';']
        sanitized = user_input
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()
    
    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """Hash sensitive data"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def validate_session(username: str, timeout_minutes: int = 60) -> bool:
        """Validate user session"""
        if 'login_time' not in st.session_state:
            return False
        
        elapsed = datetime.now() - st.session_state.login_time
        if elapsed > timedelta(minutes=timeout_minutes):
            return False
        
        return True

class UIHelper:
    """UI/UX helper functions"""
    
    @staticmethod
    def format_number(value: float, decimals: int = 2) -> str:
        """Format number for display"""
        if value >= 1e9:
            return f"${value/1e9:.{decimals}f}B"
        elif value >= 1e6:
            return f"${value/1e6:.{decimals}f}M"
        elif value >= 1e3:
            return f"${value/1e3:.{decimals}f}K"
        return f"${value:.{decimals}f}"
    
    @staticmethod
    def get_status_color(status: str) -> str:
        """Get color for status badge"""
        status_colors = {
            'RECRUITING': '#48bb78',
            'COMPLETED': '#667eea',
            'ACTIVE_NOT_RECRUITING': '#ed8936',
            'TERMINATED': '#f56565'
        }
        return status_colors.get(status, '#cbd5e0')
    
    @staticmethod
    def format_date(date_obj) -> str:
        """Format date for display"""
        if date_obj is None:
            return "N/A"
        return date_obj.strftime('%Y-%m-%d')

class MetricsCollector:
    """Collect and aggregate metrics"""
    
    @staticmethod
    def calculate_growth(current: float, previous: float) -> float:
        """Calculate growth percentage"""
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100
    
    @staticmethod
    def get_trend_indicator(value: float) -> str:
        """Get trend indicator emoji"""
        if value > 0:
            return "📈"
        elif value < 0:
            return "📉"
        return "➡️"

# Decorators for common operations
def log_action(action_name: str):
    """Log user actions"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Action: {action_name} - User: {st.session_state.get('username', 'Unknown')}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_authentication(func: Callable) -> Callable:
    """Require user authentication"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.error("Authentication required")
            return None
        return func(*args, **kwargs)
    return wrapper
