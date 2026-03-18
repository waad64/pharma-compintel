@echo off
echo Installing Pharma-CompIntel Dependencies for Windows...
echo.

echo Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing core dependencies first...
pip install numpy>=1.21.0
pip install pandas>=1.5.0

echo.
echo Installing remaining dependencies...
pip install requests>=2.28.0
pip install streamlit>=1.28.0
pip install beautifulsoup4>=4.11.0
pip install selenium>=4.10.0
pip install schedule>=1.2.0
pip install plotly>=5.15.0
pip install yfinance>=0.2.0
pip install lxml>=4.9.0
pip install webdriver-manager>=3.8.0
pip install python-dotenv>=1.0.0

echo.
echo Installing Ollama Python client...
pip install ollama>=0.1.0

echo.
echo Installation completed!
echo.
echo If you encounter any issues, try:
echo 1. Update Visual Studio Build Tools
echo 2. Use conda instead: conda install pandas numpy
echo 3. Use pre-compiled wheels: pip install --only-binary=all pandas
echo.
pause