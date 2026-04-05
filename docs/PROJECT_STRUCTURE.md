# PCI Dashboard - Project Structure

## Production-Grade Engineering Organization

```
compintel/
├── src/                          # Source code
│   ├── __init__.py
│   ├── app/                      # Application layer
│   │   ├── __init__.py
│   │   ├── main.py              # Main Streamlit app
│   │   ├── pages/               # Streamlit pages
│   │   └── components/          # Reusable UI components
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── metrics.py           # Metrics calculation
│   │   ├── analytics.py         # Analytics engine
│   │   └── scoring.py           # CI scoring logic
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── data_service.py      # Data operations
│   │   ├── auth_service.py      # Authentication
│   │   └── report_service.py    # Report generation
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   ├── company.py           # Company model
│   │   ├── trial.py             # Trial model
│   │   └── metrics.py           # Metrics model
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── logger.py            # Logging setup
│       ├── security.py          # Security utilities
│       ├── validators.py        # Data validation
│       ├── performance.py       # Performance monitoring
│       └── ui_helpers.py        # UI formatting
│
├── config/                       # Configuration
│   ├── settings.py              # Main configuration
│   ├── .env                     # Environment variables
│   └── .env.example             # Example env file
│
├── data/                         # Data directory
│   ├── clinical_trials_extracted.csv
│   ├── clinical_trials_extracted.xlsx
│   └── exports/                 # User exports
│
├── logs/                         # Application logs
│   └── pci_dashboard.log
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_utils.py
│   ├── test_services.py
│   ├── test_validators.py
│   └── conftest.py
│
├── docs/                         # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── USER_GUIDE.md
│
├── .github/                      # GitHub configuration
│   ├── workflows/               # CI/CD workflows
│   └── ISSUE_TEMPLATE/
│
├── scripts/                      # Utility scripts
│   ├── setup.py
│   ├── migrate.py
│   └── backup.py
│
├── pci_dashboard.py             # Main entry point
├── unified_data_pipeline.py     # Data pipeline
├── requirements.txt             # Dependencies
├── .gitignore
├── .env.example
├── README.md
├── PRODUCTION_GUIDE.md
├── DESIGN_SYSTEM.md
├── ENHANCEMENT_SUMMARY.md
└── docker-compose.yml           # Docker configuration
```

## Directory Descriptions

### `/src` - Source Code
Main application code organized by layer:
- **app/**: Streamlit UI and page components
- **core/**: Core business logic and algorithms
- **services/**: Business logic services (data, auth, reports)
- **models/**: Data models and schemas
- **utils/**: Reusable utility functions

### `/config` - Configuration
- **settings.py**: Centralized configuration management
- **.env**: Environment variables (not in git)
- **.env.example**: Example environment file

### `/data` - Data Directory
- Clinical trials data (CSV/Excel)
- User exports
- Temporary data files

### `/logs` - Logs
- Application logs
- Error logs
- Audit logs

### `/tests` - Test Suite
- Unit tests
- Integration tests
- Test fixtures

### `/docs` - Documentation
- API documentation
- Architecture diagrams
- Deployment guides
- User guides

### `/.github` - GitHub Configuration
- CI/CD workflows
- Issue templates
- Pull request templates

### `/scripts` - Utility Scripts
- Setup scripts
- Database migrations
- Backup utilities

## Module Organization

### Layers

#### 1. **Presentation Layer** (`src/app/`)
- Streamlit UI components
- Page routing
- User interactions
- Form handling

#### 2. **Service Layer** (`src/services/`)
- Business logic
- Data operations
- Authentication
- Report generation

#### 3. **Core Layer** (`src/core/`)
- Metrics calculation
- Analytics engine
- Scoring algorithms
- Data processing

#### 4. **Data Layer** (`src/models/`)
- Data models
- Schemas
- Validation rules

#### 5. **Utility Layer** (`src/utils/`)
- Logging
- Security
- Validation
- UI helpers
- Performance monitoring

## Configuration Management

### Environment Variables
```bash
# .env file
DEBUG=False
LOG_LEVEL=INFO
SESSION_TIMEOUT_MINUTES=60
CACHE_TTL_SECONDS=3600
DATABASE_URL=your_database_url
```

### Settings Access
```python
from config.settings import Config

# Access configuration
Config.app.APP_NAME
Config.security.SESSION_TIMEOUT_MINUTES
Config.performance.CACHE_TTL_SECONDS
```

## Logging

### Setup
```python
from src.utils.logger import logger

logger.info("Application started")
logger.error("An error occurred")
```

### Log Levels
- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

## Security

### Authentication
```python
from src.utils.security import AuthenticationManager

if AuthenticationManager.authenticate(username, password):
    AuthenticationManager.initialize_session(username)
```

### Data Validation
```python
from src.utils.validators import DataValidator

is_valid, message = DataValidator.validate_dataframe(df, required_columns)
```

## Services

### Data Service
```python
from src.services.data_service import DataService

df = DataService.load_clinical_trials_data()
df_filtered = DataService.filter_data(df, filters)
```

## Best Practices

### 1. **Separation of Concerns**
- Each module has a single responsibility
- Clear interfaces between layers
- Minimal coupling

### 2. **Configuration Management**
- All settings in `config/settings.py`
- Environment variables for sensitive data
- No hardcoded values

### 3. **Error Handling**
- Centralized error handling
- Proper logging
- User-friendly error messages

### 4. **Testing**
- Unit tests for utilities
- Integration tests for services
- Test fixtures in conftest.py

### 5. **Documentation**
- Docstrings for all functions
- Type hints for parameters
- README files in each module

## Development Workflow

### 1. Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
```bash
cp config/.env.example config/.env
# Edit .env with your settings
```

### 3. Run Application
```bash
streamlit run pci_dashboard.py
```

### 4. Run Tests
```bash
pytest tests/
```

### 5. Run Data Pipeline
```bash
python unified_data_pipeline.py
```

## Deployment

### Local
```bash
streamlit run pci_dashboard.py
```

### Docker
```bash
docker-compose up
```

### Production
See `PRODUCTION_GUIDE.md` for detailed instructions

## Contributing

1. Follow the project structure
2. Add tests for new features
3. Update documentation
4. Follow PEP 8 style guide
5. Use type hints

## Support

- Documentation: `/docs`
- Issues: GitHub Issues
- Email: support@pci-dashboard.com

---

**Version**: 2.0.0
**Status**: Production Ready
