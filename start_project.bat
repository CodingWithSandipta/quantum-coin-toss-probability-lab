@echo off
echo ========================================================
echo   Quantum Coin Toss and Probability Laboratory
echo ========================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not added to PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo Installing / verifying dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Launching Streamlit application...
echo The application will open in your default browser at http://localhost:8501
echo.
streamlit run app.py
pause
