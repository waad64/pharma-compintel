# Pharma-CompIntel AI Insights

An AI-powered competitive intelligence platform for pharmaceutical and biotech companies, featuring automated data extraction from NASDAQ and intelligent analysis.

## 🚀 Features

- **Automated Data Extraction**: Weekly automated fetching of healthcare companies from NASDAQ
- **AI-Powered Enrichment**: Uses LLM for intelligent data extraction and analysis
- **Interactive Dashboard**: Streamlit-based dashboard with CI scoring and visualizations
- **Comprehensive Analysis**: 6 CI domains with 17 sub-domains analysis
- **Real-time Updates**: Automated weekly data refresh

## 📋 Prerequisites

- Python 3.10+
- Ollama installed locally/ or LLM key(if aiming for production).
- Chrome browser (for web scraping)

## 🛠️ Installation

1. **Clone/Download the project**
 ```bash
   git clone 
   ``` 
3. 
   ```bash
   cd Pharma-Compintel
   ```

4. **Setup Environment Variables**
   ```bash
   copy  .env
   # Edit .env file with your Ollama configuration
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Setup Ollama**
   - Ensure Ollama is running locally
   - Pull the required model:
   ```bash
   ollama pull llama2
   ```

## 🎯 Usage

### 1. Run Data Extraction (One-time)
```bash
python nasdaq_fetcher.py
```

### 2. Start the Dashboard
```bash
streamlit run dashboard.py
```

### 3. Setup Automated Extraction (Optional)
```bash
python scheduler.py
```

## 📊 Dashboard Features

### Input Tab
- Disease Area selection
- Clinical Phase filtering
- Market Cap filters
- Geography options

### Results Tab
- **KPI Cards**: Total companies, active trials, average market cap, risk index
- **Forest Plot**: CI domain scores with confidence intervals
- **Company Analysis**: Detailed company comparison table
- **Market Analysis**: Clinical phase and disease area distributions

### CI Domains Analyzed
1. **Clinical Maturity** (0-100)
2. **Financial Stability** (0-100)
3. **Pipeline Diversification** (0-100)
4. **Partnership Activity** (0-100)
5. **Regulatory Strength** (0-100)
6. **Innovation Index** (0-100)

## 📁 Project Structure

```
Pharma-Compintel/
├── nasdaq_fetcher.py      # Main data extraction script
├── dashboard.py           # Streamlit dashboard
├── scheduler.py           # Automated scheduling
├── config.json           # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── pharma_compintel_latest.csv  # Latest data (generated)
```

## ⚙️ Configuration

Edit `.env` file to customize:
- **Ollama Settings**: Host, model, timeout, retries
- **NASDAQ API**: Rate limiting, data limits
- **Scheduling**: Extraction day/time
- **Output**: File naming, backup settings
- **Dashboard**: Port, title customization

Example `.env` configuration:
```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
NASDAQ_RATE_LIMIT=2
EXTRACTION_DAY=sunday
EXTRACTION_TIME=02:00
```

## 🔄 Data Fields Extracted

### Basic NASDAQ Data
- Symbol, Name, Last Sale, Net Change, % Change
- Market Cap, Country, IPO Year, Volume
- Sector, Industry

### AI-Enriched Data
- Disease Area & Diseases
- Clinical Trial Phase
- Company Profile & Technology
- Approved Products & Pipeline
- Lead Product & Partnerships
- Stock Information & Links

## 🤖 AI Integration

The system uses Ollama to intelligently extract:
- **Pipeline Information**: Automated analysis of company pipelines
- **Disease Areas**: Classification of therapeutic focus
- **Clinical Phases**: Most advanced trial phases
- **Technology Platforms**: Core technology identification
- **Partnership Analysis**: Key collaboration identification

## 📈 CI Scoring Algorithm

Each company receives scores across 6 domains:
- **Clinical Maturity**: Based on most advanced clinical phase
- **Financial Stability**: Market capitalization analysis
- **Pipeline Diversification**: Number and variety of pipeline products
- **Partnership Activity**: Strategic collaborations count
- **Regulatory Strength**: Approved products portfolio
- **Innovation Index**: Composite innovation score

## 🔧 Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   - Ensure Ollama is running: `ollama serve`
   - Check model availability: `ollama list`

2. **NASDAQ API Rate Limiting**
   - Increase delay in `config.json`
   - Check internet connection

3. **Chrome Driver Issues**
   - Update Chrome browser
   - Clear browser cache

### Logs
Check `pharma_compintel.log` for detailed error messages.

## 🚀 Deployment for Client

### Production Setup
1. **Server Requirements**
   - 4GB+ RAM
   - Python 3.8+
   - Ollama installed

2. **Environment Setup**
   ```bash
   pip install -r requirements.txt
   ollama pull llama2
   ```

3. **Start Services**
   ```bash
   # Start scheduler (background)
   nohup python scheduler.py &
   
   # Start dashboard
   streamlit run dashboard.py --server.port 8501
   ```

4. **Access Dashboard**
   - Open browser to `http://localhost:8501`
   - Use filters to analyze specific therapeutic areas

## 📞 Support

For technical support or customization requests, contact the development team.

## 📄 License

Proprietary software for pharmaceutical competitive intelligence.
