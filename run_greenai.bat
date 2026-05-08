@echo off
REM GreenAI Streamlit Application Launcher
REM This script starts the GreenAI Streamlit dashboard

echo.
echo ============================================================
echo 🌿 GreenAI - Sustainability-Aware LLM Routing Dashboard
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ⚠️  Streamlit not found. Installing dependencies...
    pip install -r requirements.txt
)

REM Check for sample data
if not exist "outputs\all_observations.csv" (
    echo 📊 Generating sample data for first-time demo...
    python generate_sample_data.py
    echo.
)

REM Launch Streamlit
echo 🚀 Starting Streamlit app...
echo.
echo 📍 The app will open at: http://localhost:8501
echo.
echo 💡 Tips:
echo    - Paste your Groq API key in the sidebar (get from https://console.groq.com/keys)
echo    - Or just use mock mode (🟡) for testing without API key
echo    - Start with "Live Query" page to test routing
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run streamlit_app/app.py

pause
