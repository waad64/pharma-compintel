"""Logging utility module"""

import logging
import os
from config.settings import Config

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with file and console handlers"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.logging.LOG_LEVEL))
    
    # Create logs directory if it doesn't exist
    os.makedirs(Config.LOGS_DIR, exist_ok=True)
    
    # File handler
    if Config.logging.ENABLE_FILE_LOGGING:
        file_handler = logging.FileHandler(
            os.path.join(Config.LOGS_DIR, "pci_dashboard.log"),
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, Config.logging.LOG_LEVEL))
        file_formatter = logging.Formatter(Config.logging.LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Console handler
    if Config.logging.ENABLE_CONSOLE_LOGGING:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, Config.logging.LOG_LEVEL))
        console_formatter = logging.Formatter(Config.logging.LOG_FORMAT)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger

# Create application logger
logger = setup_logger("pci_dashboard")
