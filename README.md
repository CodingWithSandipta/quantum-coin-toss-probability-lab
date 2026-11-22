# Quantum Coin Toss and Probability Laboratory

**Subtitle:** An Interactive Quantum Computing Laboratory for Understanding Superposition, Measurement and Probability Distributions.

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-2.6.2-purple.svg)](https://qiskit.org/)
[![Qiskit Aer](https://img.shields.io/badge/Qiskit--Aer-0.18.4-cyan.svg)](https://github.com/Qiskit/qiskit-aer)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.67.0-red.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/Tests-12%2F12%20Passing-brightgreen.svg)]()

---

## 📌 Project Overview

The **Quantum Coin Toss and Probability Laboratory** is a comprehensive, interactive college-level educational application designed to demonstrate fundamental quantum computing phenomena through simulated quantum circuits.

Built on **Qiskit** and **Qiskit Aer**, the laboratory executes actual quantum circuits locally on standard hardware without requiring an IBM Quantum account, physical quantum processors, cloud APIs, or network access.

### 🌟 Key Educational Capabilities
- **Genuine Quantum Coin Toss:** Prepares $|0\rangle$, applies a Hadamard gate ($H$), and measures the state with Qiskit `AerSimulator`.
- **Superposition Explorer:** Investigate single-qubit transformations (Identity, $H$, $X$, $Y$, $Z$), inspect complex statevector amplitudes, and visualize genuine 3D **Bloch Spheres**.
- **Multi-Qubit Laboratory:** Scale from 1 to 5 qubits, demonstrating the exponential state space growth ($2^n = 2, 4, 8, 16, 32$) and uniform separable superposition.
- **Probability Analysis:** Interactively analyze the convergence of finite sample measurements to theoretical probability distributions.
- **Classical vs Quantum Comparison:** Scientifically benchmark classical PRNG (Mersenne Twister) against simulated quantum sampling.
- **Experiment History:** SQLite database tracks experiment runs, with one-click CSV export and history management.
- **Interactive Knowledge Quiz:** 10 multiple-choice questions assessing understanding of quantum principles with instant feedback and scoring.

---

## 🚀 Step-by-Step Startup Guide

### 1. Prerequisites: Install Python
Ensure Python 3.10, 3.11, or 3.12 is installed on your computer.  
Check your Python installation in your terminal:
```bash
python --version
```

### 2. Open Project Folder
Open your terminal or command prompt and navigate to the project directory:
```bash
cd "c:\Users\Sandip Bhattacharyya\NNDL Project"
```

### 3. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv

# macOS / Linux
python3 -m venv venv
```

### 4. Activate the Virtual Environment
```bash
# Windows (Command Prompt)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

### 5. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 6. Launch the Streamlit Application
```bash
streamlit run app.py
```

### 7. Open the Application in Your Web Browser
The application will open automatically in your browser. If not, open:
```
http://localhost:8501
```

> **Note on Offline Operation:** Once dependencies are installed, the laboratory operates **100% offline without any internet connection**.

---

## ⚡ Quick Start Scripts

- **Windows Users:** Double-click `start_project.bat`.
- **macOS / Linux Users:** Run `chmod +x start_project.sh && ./start_project.sh`.

---

## 🧪 Running Automated Unit Tests

The laboratory comes with a full automated test suite verifying all 10 specifications required by the curriculum:

```bash
python -m pytest -v tests/
```

### Test Coverage Highlights:
- **Test 1:** Hadamard gate superposition and theoretical 50/50 probabilities.
- **Test 2:** Pauli-X gate bit-flip to $|1\rangle$.
- **Test 3:** Identity (no gate) baseline preservation of ground state $|0\rangle$.
- **Test 4:** Multi-qubit circuit equal probabilities ($1/2^n$).
- **Test 5:** Measurement execution integrity on AerSimulator.
- **Test 6:** Probability normalization ($\sum P(x) = 1.0$).
- **Test 7:** Shot count verification (total counts equal configured shots).
- **Test 8:** Classical comparison trial count consistency.
- **Test 9:** SQLite database persistence, insertion, retrieval, and clearing.
- **Test 10:** Application module imports and startup verification.

---

## 📁 Repository Structure

```
├── app.py                      # Master Streamlit entrypoint & Home Dashboard
├── requirements.txt            # Pinned dependency specifications
├── start_project.bat           # Windows 1-click startup script
├── start_project.sh            # Linux/macOS startup script
├── .gitignore                  # Git exclusions
├── quantum/                    # Quantum circuit and simulation logic
│   ├── circuits.py             # Qiskit circuit construction
│   ├── simulator.py            # Qiskit AerSimulator execution engine
│   ├── statevector.py          # Statevector & Bloch coordinate calculations
│   ├── probability.py          # Probability distribution & metrics engine
│   └── classical_comparison.py # PRNG vs Quantum comparative simulation
├── components/                 # Reusable UI & plotting components
│   ├── charts.py               # Dark-theme Plotly visualizations
│   ├── circuit_visualizer.py   # Qiskit Matplotlib & Bloch sphere renderers
│   └── ui_components.py        # Reusable metric cards & containers
├── database/                   # Persistence layer
│   └── db.py                   # Thread-safe SQLite experiment history
├── pages/                      # Multi-page interactive application
│   ├── 1_Quantum_Coin_Toss.py
│   ├── 2_Superposition_Explorer.py
│   ├── 3_Multi_Qubit_Laboratory.py
│   ├── 4_Probability_Analysis.py
│   ├── 5_Classical_vs_Quantum.py
│   ├── 6_About_Quantum_Computing.py
│   └── 7_Quiz.py
├── assets/
│   └── styles.css              # Custom scientific dark CSS stylesheet
├── tests/                      # Automated unit test suite
│   ├── test_circuits.py
│   ├── test_simulator.py
│   └── test_probabilities.py
└── docs/                       # Comprehensive documentation
    ├── PROJECT_REPORT.md       # Full academic project report
    ├── QUANTUM_CONCEPTS.md     # Detailed theory and mathematical formulas
    ├── VIVA_QUESTIONS.md       # Viva voce oral exam questions and model answers
    └── TESTING_REPORT.md       # Complete test verification report
```

---

## 🔬 Scientific Disclaimer & Nuance

1. **Simulator vs Physical QPU:** This software uses **Qiskit Aer**, an open-source software simulator that performs classical numerical linear algebra modeling quantum circuits.
2. **Local Randomness:** Local simulators utilize classical pseudorandom algorithms to sample counts from calculated probability vectors. This differs from physical quantum processors, where randomness originates from physical quantum indeterminism.
3. **No Quantum Advantage Claimed:** This project does not claim a computational quantum advantage. Its purpose is educational: to provide intuitive, interactive visual models of quantum statevectors, gates, and measurements.

---

## 📄 License
Educational use only. Built for quantum computing coursework and laboratory demonstrations.
