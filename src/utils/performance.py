"""Performance monitoring utilities"""

import functools
import time
from src.utils.logger import logger

class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    @staticmethod
    def track_execution(func):
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
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                import streamlit as st
                from datetime import datetime, timedelta
                import hashlib
                
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
