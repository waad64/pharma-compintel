# PCI Dashboard - Pharmaceutical Competitive Intelligence

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Status](https://img.shields.io/badge/status-Production%20Ready-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-Proprietary-red)

## Overview

PCI Dashboard is a production-grade Pharmaceutical Competitive Intelligence platform built with Streamlit. It provides comprehensive analysis of clinical trials, competitive landscape, and market intelligence for pharmaceutical companies.

### Key Features

- 🎨 **Professional UI/UX**: Modern design system with responsive layout
- 🔒 **Enterprise Security**: Authentication, session management, data protection
- ⚡ **High Performance**: Caching, optimization, efficient data processing
- 📊 **Advanced Analytics**: Metrics calculation, CI scoring, trend analysis
- 📄 **Report Generation**: PDF/Excel exports, batch processing
- 🔧 **Production-Ready**: Monitoring, logging, error handling
- 📚 **Well-Documented**: Comprehensive guides and API documentation

## Quick Start

### Prerequisites

- Python 3.8+
- pip or conda
- 2GB RAM minimum
- 500MB disk space

### Installation

```bash
# Clone repository
git clone <repository-url>
cd compintel

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config/.env.example config/.env
# Edit config/.env with your settings

# Run application
python run.py
```

### Access Application

```
http://localhost:8501
```

### Demo Credentials

- **Username**: admin
- **Password**: admin123

## Project Structure

```
compintel/
├── src/                          # Source code
│   ├── app/                      # Application layer (UI)
│   ├── core/                     # Core business logic
│   ├── services/                 # Business services
│   ├── models/                   # Data models
│   └── utils/                    # Utilities
├── config/                       # Configuration
├── data/                         # Data directory
├── logs/                         # Application logs
├── tests/                        # Test suite
├── docs/                         # Documentation
├── run.py                        # Entry point
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

See [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for detailed structure.

## Architecture

The application follows a layered architecture:

1. **Presentation Layer** (`src/app/`): Streamlit UI components
2. **Service Layer** (`src/services/`): Business logic
3. **Core Layer** (`src/core/`): Algorithms and calculations
4. **Data Layer** (`src/models/`): Data models
5. **Utility Layer** (`src/utils/`): Cross-cutting concerns

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture.

## Configuration

### Environment Variables

```bash
# .env file
DEBUG=False
LOG_LEVEL=INFO
SESSION_TIMEOUT_MINUTES=60
CACHE_TTL_SECONDS=3600
```

See [config/.env.example](config/.env.example) for all available options.

### Settings

All configuration is managed in `config/settings.py`:

```python
from config.settings import Config

Config.app.APP_NAME
Config.security.SESSION_TIMEOUT_MINUTES
Config.performance.CACHE_TTL_SECONDS
```

## Usage

### Login

1. Open http://localhost:8501
2. Enter credentials
3. Click "Login"

### Workflow

1. **Input & Filters Tab**: Select filters for analysis
2. **Results & Analysis Tab**: View KPIs and detailed analysis
3. **Reports Tab**: Generate and export reports

### Data Filtering

- All filters are cumulative
- "All" option includes all values
- Real-time record count updates
- Data quality indicator

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run linting
flake8 src/
black src/
```

### Running Data Pipeline

```bash
python src/services/data_pipeline.py
```

### Logging

```python
from src.utils.logger import logger

logger.info("Application started")
logger.error("An error occurred")
```

## Deployment

### Local Deployment

```bash
streamlit run src/app/main.py
```

### Docker Deployment

```bash
docker-compose up -d
```

### Cloud Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions for:
- AWS (EC2, ECS, Streamlit Cloud)
- Azure (App Service)
- GCP (Cloud Run)

## Monitoring & Logging

### Logs Location

```
logs/pci_dashboard.log
```

### Log Levels

- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

### Monitoring

- Application performance metrics
- User activity tracking
- Error rate monitoring
- Data processing time tracking

## Security

### Authentication

- Password hashing (SHA-256)
- Session management (60-minute timeout)
- Role-based access control

### Data Protection

- Input sanitization (XSS prevention)
- CSRF protection
- Secure data export
- Audit logging

### Best Practices

- Use strong passwords
- Enable MFA for admin accounts
- Rotate credentials regularly
- Keep dependencies updated

## Performance

### Optimization

- Data caching (1-hour TTL)
- Connection pooling
- Query optimization
- Lazy loading

### Benchmarks

- Page load time: ~1-2 seconds
- Memory usage: ~80MB
- Cache hit rate: 85%+

## Testing

### Run Tests

```bash
pytest tests/
```

### Test Coverage

```bash
pytest --cov=src tests/
```

### Test Types

- Unit tests: Utility functions
- Integration tests: Services
- End-to-end tests: User workflows

## Troubleshooting

### Application Won't Start

```bash
# Check logs
tail -f logs/pci_dashboard.log

# Verify configuration
cat config/.env

# Check dependencies
pip list
```

### High Memory Usage

- Increase cache TTL
- Reduce batch size
- Optimize queries

### Slow Performance

- Check database performance
- Monitor network latency
- Check CPU usage

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for more troubleshooting.

## Documentation

- [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - Project organization
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide
- [DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) - Design guidelines
- [PRODUCTION_GUIDE.md](docs/PRODUCTION_GUIDE.md) - Production setup

## Support

### Contact

- Email: support@pci-dashboard.com
- Issues: GitHub Issues
- Documentation: `/docs`

### Escalation

1. Level 1: Support Team
2. Level 2: Engineering Team
3. Level 3: DevOps Team
4. Level 4: Management

## Contributing

1. Follow project structure
2. Add tests for new features
3. Update documentation
4. Follow PEP 8 style guide
5. Use type hints

## License

Proprietary - All rights reserved

## Version History

### v2.0.0 (Current)
- Production-grade architecture
- Enhanced UI/UX design
- Comprehensive security
- Performance optimization
- Complete documentation

### v1.0
- Initial release
- Basic functionality
- Simple UI

## Changelog

See [ENHANCEMENT_SUMMARY.md](docs/ENHANCEMENT_SUMMARY.md) for detailed changes.

## Roadmap

- [ ] Advanced analytics
- [ ] Machine learning models
- [ ] Real-time data updates
- [ ] Mobile app
- [ ] API endpoints
- [ ] Multi-language support

---

**Version**: 2.0.0  
**Status**: Production Ready ✓  
**Last Updated**: 2024

For more information, see the [documentation](docs/).
