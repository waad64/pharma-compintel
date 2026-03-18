@echo off
echo Starting Pharma-CompIntel AI Insights...
echo.

echo Setting up environment variables...
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your Ollama configuration
    echo Press any key after editing .env file...
    pause
)

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing/Updating dependencies (Windows-optimized)...
call install_windows.bat

echo.
echo Checking Ollama installation...
ollama --version
if %errorlevel% neq 0 (
    echo Ollama is not installed. Please install Ollama first.
    echo Visit: https://ollama.ai
    pause
    exit /b 1
)

echo.
echo Pulling Ollama model (if not exists)...
ollama pull llama2

echo.
echo Running initial data extraction...
python nasdaq_fetcher.py

echo.
echo Starting Streamlit dashboard...
echo Dashboard will open in your browser at http://localhost:8501
streamlit run dashboard.py

pause