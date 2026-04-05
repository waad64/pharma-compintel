"""Configuration management for PCI Dashboard"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class AppConfig:
    """Application configuration"""
    APP_NAME: str = "PCI Dashboard"
    APP_VERSION: str = "2.0.0"
    APP_DESCRIPTION: str = "Pharmaceutical Competitive Intelligence"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
@dataclass
class StreamlitConfig:
    """Streamlit configuration"""
    PAGE_TITLE: str = "PCI Dashboard - Pharmaceutical Competitive Intelligence"
    PAGE_ICON: str = "💊"
    LAYOUT: str = "wide"
    INITIAL_SIDEBAR_STATE: str = "expanded"
    
@dataclass
class ThemeConfig:
    """Theme configuration"""
    PRIMARY_COLOR: str = "#667eea"
    SECONDARY_COLOR: str = "#764ba2"
    DARK_TEXT: str = "#1a365d"
    LIGHT_TEXT: str = "#718096"
    BORDER_COLOR: str = "#e2e8f0"
    BG_LIGHT: str = "#f5f7fa"
    SUCCESS: str = "#48bb78"
    WARNING: str = "#ed8936"
    ERROR: str = "#f56565"

@dataclass
class SecurityConfig:
    """Security configuration"""
    SESSION_TIMEOUT_MINUTES: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_SPECIAL_CHARS: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    ENABLE_XSRF_PROTECTION: bool = True
    ENABLE_CSRF_PROTECTION: bool = True

@dataclass
class PerformanceConfig:
    """Performance configuration"""
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    MAX_CONCURRENT_USERS: int = 100
    ENABLE_COMPRESSION: bool = True
    ENABLE_LAZY_LOADING: bool = True
    CONNECTION_POOL_SIZE: int = 10
    QUERY_TIMEOUT_SECONDS: int = 30

@dataclass
class APIConfig:
    """API configuration"""
    CLINICAL_TRIALS_API: str = "https://clinicaltrials.gov/api/v2/studies"
    NASDAQ_API: str = "https://api.nasdaq.com/api/screener/stocks"
    REQUEST_TIMEOUT: int = 30
    RATE_LIMIT_DELAY: float = 0.5
    ENABLE_RATE_LIMITING: bool = True

@dataclass
class LoggingConfig:
    """Logging configuration"""
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/pci_dashboard.log"
    ENABLE_FILE_LOGGING: bool = True
    ENABLE_CONSOLE_LOGGING: bool = True

@dataclass
class DatabaseConfig:
    """Database configuration"""
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    CONNECTION_POOL_SIZE: int = 10
    QUERY_TIMEOUT: int = 30
    ENABLE_CONNECTION_RETRY: bool = True
    MAX_RETRIES: int = 3

@dataclass
class ExportConfig:
    """Export configuration"""
    MAX_EXPORT_ROWS: int = 50000
    SUPPORTED_FORMATS: list = None
    ENABLE_ENCRYPTION: bool = True
    
    def __post_init__(self):
        if self.SUPPORTED_FORMATS is None:
            self.SUPPORTED_FORMATS = ["csv", "xlsx", "pdf"]

class Config:
    """Main configuration class"""
    
    app = AppConfig()
    streamlit = StreamlitConfig()
    theme = ThemeConfig()
    security = SecurityConfig()
    performance = PerformanceConfig()
    api = APIConfig()
    logging = LoggingConfig()
    database = DatabaseConfig()
    export = ExportConfig()
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SRC_DIR = os.path.join(BASE_DIR, "src")
    CONFIG_DIR = os.path.join(BASE_DIR, "config")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    TESTS_DIR = os.path.join(BASE_DIR, "tests")
    DOCS_DIR = os.path.join(BASE_DIR, "docs")
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        for directory in [cls.LOGS_DIR, cls.DATA_DIR]:
            os.makedirs(directory, exist_ok=True)

# Initialize configuration
Config.ensure_directories()
