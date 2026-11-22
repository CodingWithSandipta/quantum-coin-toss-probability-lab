# Project Report: Quantum Coin Toss and Probability Laboratory

**Academic Level:** Undergraduate / College Quantum Computing Laboratory  
**Technology Stack:** Python 3.12, Qiskit 2.6, Qiskit Aer 0.18, Streamlit 1.67, Plotly 7.1, SQLite  
**Author:** Quantum Computing Laboratory Development Team  

---

## 1. Executive Summary

The **Quantum Coin Toss and Probability Laboratory** is an interactive, scientifically rigorous educational software application designed to teach fundamental quantum computing principles—superposition, unitary transformations, projective measurement, and statistical probability distributions.

Unlike conventional classroom simulations that generate outcomes using classical pseudorandom generators like `random.random()`, this platform builds, transpiles, and simulates genuine **Qiskit quantum circuits** executed on the high-performance C++ backend of **Qiskit Aer** (`AerSimulator`). The laboratory is entirely local, requiring no paid cloud APIs, physical quantum hardware access, or network credentials.

---

## 2. Project Architecture & Modular Design

The project is architected with strict separation of concerns across quantum circuit synthesis, numerical simulation, UI components, state management, and persistence:

```
NNDL Project/
├── app.py                      # Master Entrypoint & Home Dashboard
├── quantum/                    # Core Quantum Physics & Simulation Layer
│   ├── circuits.py             # Qiskit circuit definitions (H, X, Y, Z, multi-qubit)
│   ├── simulator.py            # AerSimulator compilation and execution
│   ├── statevector.py          # Statevector extraction, Bloch coordinates (⟨X⟩, ⟨Y⟩, ⟨Z⟩)
│   ├── probability.py          # Theoretical/observed probability metrics and MAE
│   └── classical_comparison.py # PRNG vs Quantum AerSimulator benchmark engine
├── components/                 # Presentation & Visualization Layer
│   ├── charts.py               # Dark-theme Plotly visualizations
│   ├── circuit_visualizer.py   # Qiskit Matplotlib circuit & 3D Bloch sphere renderers
│   └── ui_components.py        # Reusable metric cards, badges, and Dirac containers
├── database/                   # Persistence Layer
│   └── db.py                   # Thread-safe SQLite experiment history and CSV export
├── pages/                      # Interactive Multi-Page Streamlit Application
│   ├── 1_Quantum_Coin_Toss.py
│   ├── 2_Superposition_Explorer.py
│   ├── 3_Multi_Qubit_Laboratory.py
│   ├── 4_Probability_Analysis.py
│   ├── 5_Classical_vs_Quantum.py
│   ├── 6_About_Quantum_Computing.py
│   └── 7_Quiz.py
├── assets/
│   └── styles.css              # Custom Dark Navy & Deep Purple CSS design system
├── tests/                      # Automated Unit Test Suite (12 test functions)
│   ├── test_circuits.py
│   ├── test_simulator.py
│   └── test_probabilities.py
└── docs/                       # Project Documentation & Viva Preparation
    ├── PROJECT_REPORT.md
    ├── QUANTUM_CONCEPTS.md
    ├── VIVA_QUESTIONS.md
    └── TESTING_REPORT.md
```

---

## 3. Core Functional Modules

### 3.1 Home Dashboard (`app.py`)
- Introduces core quantum tenets: qubits, superposition, measurement, and unitary gates.
- Highlights three interactive feature cards leading directly to core experiments.
- Displays the canonical single-qubit quantum coin toss circuit (`|0⟩ ─── H ─── Measure`).
- Monitors local Qiskit core and AerSimulator engine version status.

### 3.2 Quantum Coin Toss (`1_Quantum_Coin_Toss.py`)
- Implements the foundational Hadamard coin toss:
  $$|\psi\rangle = H|0\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$$
- Configurable shots: 100, 500, 1,000, 5,000, 10,000.
- Displays Heads ($0$) and Tails ($1$) counts, empirical percentages, deviations from 50%, and Aer execution runtime.
- Automatically saves experiment runs to the local SQLite database.

### 3.3 Superposition Explorer (`2_Superposition_Explorer.py`)
- Provides interactive gate exploration: Identity (`None`), Hadamard (`H`), Pauli-X (`X`), Pauli-Y (`Y`), and Pauli-Z (`Z`).
- Uses `Statevector.from_instruction` without projective measurement to preserve phase amplitudes.
- Renders an interactive 3D **Bloch Sphere** plotting the exact Pauli expectation vector $(x=\langle X \rangle, y=\langle Y \rangle, z=\langle Z \rangle)$.
- Emphasizes the distinction between relative phase shifts and computational basis probabilities.

### 3.4 Multi-Qubit Laboratory (`3_Multi_Qubit_Laboratory.py`)
- Allows users to scale from 1 to 5 qubits, demonstrating the exponential expansion of Hilbert space ($2^n \in [2, 32]$).
- Applies $H^{\otimes n}$ to initialize a uniform separable superposition state.
- Plots probability distribution histograms against the ideal uniform target ($1/2^n$).
- Clarifies that these states are independent product superpositions, not entangled Einstein-Podolsky-Rosen (EPR) states.

### 3.5 Probability Analysis (`4_Probability_Analysis.py`)
- Evaluates the empirical convergence of finite sample measurements toward ideal theoretical distributions.
- Calculates Mean Absolute Error (MAE) and maximum observed deviation across configurable shots.
- Demonstrates the $1/\sqrt{N}$ scaling of statistical shot noise.

### 3.6 Classical vs Quantum Coin Toss (`5_Classical_vs_Quantum.py`)
- Conducts side-by-side sampling of Python's Mersenne Twister PRNG against Qiskit Aer simulation.
- Delivers an explicit scientific nuance: clarifies that local simulators calculate linear algebra numerically and are not physical sources of quantum indeterminism or hardware advantage.

### 3.7 About & History (`6_About_Quantum_Computing.py`)
- Comprehensive educational encyclopedia covering Dirac notation, gate matrices, and Born rule mathematics.
- Provides a persistent SQLite experiment log with single-click CSV export and history clearing.

### 3.8 Knowledge Quiz (`7_Quiz.py`)
- 10 interactive multiple-choice questions assessing comprehension of superposition, gates, statevectors, and measurement collapse.
- Provides instant scoring, proficiency ratings, and question-by-question explanations.

---

## 4. Software Quality & Testing

The project incorporates 12 automated unit tests implemented with `pytest`:
- **Circuit Validity:** Verification of statevectors, Hadamard balanced probabilities, Pauli-X bit flips, and identity operations.
- **Normalization:** Proves $\sum P(x) = 1.0$ across 1 to 5 qubits.
- **Simulation Integrity:** Validates that total measurement counts strictly equal configured shot counts without loss.
- **Persistence:** Verifies SQLite database creation, record insertion, querying, and clearing.
- **Test Results:** 12/12 passed in 5.51 seconds.

---

## 5. Conclusion

The Quantum Coin Toss and Probability Laboratory fulfills all academic and technical requirements. It delivers an intuitive, visually sophisticated, and scientifically accurate environment for college students and instructors to explore quantum computational fundamentals without hardware barriers.
