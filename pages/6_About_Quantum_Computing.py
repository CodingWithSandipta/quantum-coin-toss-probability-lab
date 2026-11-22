"""
pages/6_About_Quantum_Computing.py - Educational Theory & Experiment History
Comprehensive quantum computing fundamentals guide, mathematical glossary,
and persistent laboratory experiment log management with CSV export.
"""

import os
import streamlit as st
import pandas as pd

from database.db import get_all_experiments, clear_history, export_history_to_df
from components.ui_components import render_header, render_metric_card, render_info_banner

st.set_page_config(
    page_title="About & History | Quantum Lab",
    page_icon="📚",
    layout="wide",
)

# Apply CSS styles
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header(
    title="📚 Quantum Computing Theory & Lab Log",
    subtitle="Fundamental theory, mathematical formulations, and persistent experiment history.",
    badge="Reference & History",
)

# Tabs: Theory Guide vs Experiment History
tab_theory, tab_math, tab_history = st.tabs([
    "📖 Quantum Computing Concepts",
    "📐 Mathematical Foundations & Gates",
    "🗄️ Experiment History & CSV Export",
])

with tab_theory:
    st.markdown("### 🎓 Core Quantum Concepts Explained for Undergraduates")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(r"""
        #### 1. Classical vs Quantum Computing
        - **Classical Computing:** Uses physical transistors storing discrete binary digits (**bits**), which are strictly either `0` (low voltage) or `1` (high voltage). Algorithms evaluate operations sequentially or via classical parallel cores.
        - **Quantum Computing:** Uses quantum mechanical systems (**qubits**) that can occupy superpositions of states, correlate through entanglement, and undergo interference to solve certain complex problems (like prime factorization or molecular simulation) exponentially faster.

        #### 2. The Qubit (Quantum Bit)
        A qubit is the basic unit of quantum information. Physically, a qubit can be an electron spin, a polarized photon, or a superconducting Josephson junction circuit. While reading a classical bit yields its exact state, reading a qubit destroys its superposition and returns only a classical bit `0` or `1`.

        #### 3. Quantum Superposition
        Superposition allows a quantum system to exist in a linear combination of its basis states:
        $$|\\psi\\rangle = \\alpha |0\\rangle + \\beta |1\\rangle$$
        Until a measurement occurs, the qubit does not choose a state—both possibilities evolve simultaneously according to Schrödinger's equation.
        """)

    with c2:
        st.markdown(r"""
        #### 4. Quantum Measurement & The Born Rule
        In quantum mechanics, measurement is not a passive observation; it is an active physical interaction that causes **wave function collapse**. 
        According to the **Born Rule** (formulated by Max Born in 1926), the probability of finding the system in basis state $|x\\rangle$ equals the squared magnitude of its complex amplitude:
        $$P(x) = |\\langle x | \\psi \\rangle|^2$$

        #### 5. Quantum Circuits & Unitary Evolution
        A **quantum circuit** represents a sequence of quantum logic gates operating on qubits, ordered from left to right in time. Every valid quantum gate (apart from measurement) is a **unitary matrix** ($U^\dagger U = I$), meaning that quantum state evolution is strictly reversible and preserves probability.

        #### 6. Quantum Simulation
        Physical quantum computers are noisy and currently in the NISQ (Noisy Intermediate-Scale Quantum) era. **Quantum simulators** (such as Qiskit Aer) emulate the linear algebra of state vectors and density matrices on standard classical CPUs and GPUs, enabling students and researchers to test quantum algorithms without physical hardware.
        """)

with tab_math:
    st.markdown("### 📐 Mathematical Foundations & Essential Quantum Gates")

    st.markdown(r"""
    #### Statevector Normalization Condition
    A general single-qubit statevector $|\psi\rangle$ is a unit vector in a 2D complex vector space ($\mathbb{C}^2$):
    """)
    st.latex(r"|\psi\rangle = \alpha |0\rangle + \beta |1\rangle = \begin{bmatrix} \alpha \\ \beta \end{bmatrix}, \quad \text{where } \alpha, \beta \in \mathbb{C}")
    st.latex(r"|\alpha|^2 + |\beta|^2 = 1")
    st.markdown("""
    The computational basis states are defined as column vectors:
    """)
    st.latex(r"|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad |1\rangle = \begin{bmatrix} 0 \\ 1 \end{bmatrix}")

    st.write("")
    st.markdown("#### Elementary Quantum Logic Gates")

    g1, g2 = st.columns(2)

    with g1:
        st.markdown(r"""
        ##### 1. Hadamard Gate ($H$)
        Creates an equal superposition with real, positive amplitudes from $|0\rangle$:
        $$H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$$
        $$H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}, \quad H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$$

        ##### 2. Pauli-X Gate (Quantum NOT)
        Flips the basis state $|0\rangle \leftrightarrow |1\rangle$:
        $$X = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$$
        $$X|0\rangle = |1\rangle, \quad X|1\rangle = |0\rangle$$
        """)

    with g2:
        st.markdown(r"""
        ##### 3. Pauli-Y Gate
        Applies a bit flip combined with a phase rotation of $\pi/2$:
        $$Y = \begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}$$
        $$Y|0\rangle = i|1\rangle, \quad Y|1\rangle = -i|0\rangle$$

        ##### 4. Pauli-Z Gate (Phase-Flip)
        Leaves $|0\rangle$ unchanged while reversing the sign of $|1\rangle$:
        $$Z = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$$
        $$Z|0\rangle = |0\rangle, \quad Z|1\rangle = -|1\rangle$$
        """)

with tab_history:
    st.markdown("### 🗄️ Laboratory Experiment Run History")
    st.caption("Persistent SQLite storage tracking all local simulation runs.")

    # Fetch experiments from SQLite
    experiments = get_all_experiments(limit=50)

    col_btn1, col_btn2, col_spacer = st.columns([1.2, 1.2, 2.5])

    df_export = export_history_to_df()
    csv_bytes = df_export.to_csv(index=False).encode("utf-8")

    with col_btn1:
        st.download_button(
            label="📥 Export History to CSV",
            data=csv_bytes,
            file_name="quantum_lab_experiments.csv",
            mime="text/csv",
            disabled=len(experiments) == 0,
            use_container_width=True,
        )

    with col_btn2:
        if st.button("🗑️ Clear Experiment History", type="secondary", use_container_width=True):
            if clear_history():
                st.success("Experiment history successfully cleared!")
                st.rerun()

    if experiments:
        st.write("")
        st.markdown(f"**Total Recorded Experiments:** `{len(experiments)}`")

        history_table_data = []
        for exp in experiments:
            history_table_data.append({
                "ID": exp["id"],
                "Timestamp": exp["timestamp"],
                "Experiment Type": exp["experiment_type"],
                "Qubits": exp["num_qubits"],
                "Shots": f"{exp['num_shots']:,}",
                "Counts Summary": str(exp["counts"]),
                "Observations": exp["summary"],
            })

        st.dataframe(pd.DataFrame(history_table_data), use_container_width=True)
    else:
        render_info_banner(
            "No experiment records found in the database. Run the Quantum Coin Toss or Multi-Qubit Lab to log results!",
            alert_type="info",
        )
