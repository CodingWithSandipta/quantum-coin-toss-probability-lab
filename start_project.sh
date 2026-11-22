#!/usr/bin/env bash
echo "========================================================"
echo "  Quantum Coin Toss and Probability Laboratory"
echo "========================================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 could not be found."
    echo "Please install Python 3.10+."
    exit 1
fi

echo "Installing / verifying dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "Launching Streamlit application..."
echo "Default local URL: http://localhost:8501"
echo ""
streamlit run app.py
