"""
app.py - Quantum Coin Toss and Probability Laboratory
Main Home Dashboard & Entrypoint
"""

import os
import streamlit as st
from qiskit import __version__ as qiskit_version
import qiskit_aer

from database.db import init_db
from quantum.circuits import create_coin_toss_circuit
from components.circuit_visualizer import draw_circuit_figure
from components.ui_components import render_header, render_concept_card, render_info_banner

# Configure Streamlit page
st.set_page_config(
    page_title="Quantum Lab | Coin Toss & Probability",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize database
init_db()

# Load custom styling
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar metadata
with st.sidebar:
    st.markdown("### ⚛️ **QUANTUM LAB**")
    st.caption("College Quantum Computing Lab")
    st.divider()

    st.markdown("#### 🔬 **Simulation Engine**")
    st.markdown(f"- **Qiskit Core:** `v{qiskit_version}`")
    st.markdown(f"- **Aer Simulator:** `v{qiskit_aer.__version__}`")
    st.markdown("- **Backend:** `AerSimulator (CPU)`")
    st.markdown("- **Mode:** Statevector & Local Shots")
    st.divider()

    st.markdown("#### 🧭 **Laboratory Modules**")
    st.markdown("""
    1. **Quantum Coin Toss**
    2. **Superposition Explorer**
    3. **Multi-Qubit Laboratory**
    4. **Probability Analysis**
    5. **Classical vs Quantum**
    6. **About Quantum Computing**
    7. **Knowledge Quiz**
    """)
    st.divider()
    st.caption("Powered by genuine Qiskit QuantumCircuit simulations.")

# Main Header
render_header(
    title="QUANTUM LAB",
    subtitle="Quantum Coin Toss and Probability Laboratory — Explore superposition, measurement and probability through interactive quantum experiments.",
    badge="Interactive Qiskit Lab",
)

# Introduction section
st.markdown("""
Welcome to the **Quantum Coin Toss and Probability Laboratory**. This interactive educational environment 
simulates real quantum computational circuits right on your local machine using **Qiskit** and **Qiskit Aer**. 

Unlike classical computer systems where information is stored strictly as discrete binary bits (`0` or `1`), quantum 
systems harness fundamental physical principles—most notably **superposition**, **quantum phase**, and **probabilistic state collapse**.
""")

st.write("")

# Three Primary Feature Cards
col1, col2, col3 = st.columns(3)

with col1:
    render_concept_card(
        title="1. Quantum Coin Toss",
        description="Simulate a genuine quantum coin toss using the Hadamard gate. Observe how a qubit is placed into an equal superposition before measurement.",
        icon="🪙",
        link="Quantum_Coin_Toss",
    )

with col2:
    render_concept_card(
        title="2. Superposition Explorer",
        description="Understand how a single qubit exists in a linear combination of |0⟩ and |1⟩. Apply Pauli gates, inspect statevector amplitudes, and explore the 3D Bloch sphere.",
        icon="🌌",
        link="Superposition_Explorer",
    )

with col3:
    render_concept_card(
        title="3. Probability Laboratory",
        description="Observe how repeated finite measurements converge toward theoretical probability distributions across single and multi-qubit systems.",
        icon="📊",
        link="Multi_Qubit_Laboratory",
    )

st.write("")
st.divider()

# Fundamental Concepts Breakdown
st.subheader("💡 Fundamental Quantum Foundations")

c1, c2 = st.columns(2)

with c1:
    with st.expander("❓ What is Quantum Computing?", expanded=True):
        st.markdown("""
        **Quantum computing** is a computational paradigm based on the principles of quantum mechanics. 
        While classical computers use electrical transistors representing definite bits ($0$ or $1$), 
        quantum computers manipulate quantum bits (**qubits**), allowing algorithms to compute in a vast 
        multidimensional state space via quantum interference.
        """)

    with st.expander("❓ What is a Qubit?", expanded=True):
        st.markdown("""
        A **qubit** (quantum bit) is the basic unit of quantum information. Mathematically, it is a two-level 
        quantum system represented as a normalized vector in a two-dimensional complex Hilbert space:
        """)
        st.latex(r"|\psi\rangle = \alpha |0\rangle + \beta |1\rangle \quad \text{where} \quad |\alpha|^2 + |\beta|^2 = 1")
        st.markdown("""
        Here, $\\alpha$ and $\\beta$ are complex probability amplitudes corresponding to the computational basis states $|0\\rangle$ and $|1\\rangle$.
        """)

with c2:
    with st.expander("❓ What is Superposition?", expanded=True):
        st.markdown("""
        **Superposition** is the ability of a quantum system to exist simultaneously as a linear combination 
        of its orthogonal basis states. 
        
        Applying a **Hadamard gate ($H$)** to the ground state $|0\\rangle$ yields an equal superposition:
        """)
        st.latex(r"H|0\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle")
        st.markdown("""
        Until measurement, the qubit has no deterministic single outcome; both paths exist concurrently.
        """)

    with st.expander("❓ What is Quantum Measurement?", expanded=True):
        st.markdown("""
        **Measurement** irreversibly collapses a delicate quantum superposition into one definite classical state 
        according to the **Born Rule**. 
        
        The probability of observing state $|x\\rangle$ is proportional to the square of its amplitude:
        """)
        st.latex(r"P(x) = |\langle x | \psi \rangle|^2")
        st.markdown("""
        After measurement, the quantum superposition is destroyed, leaving the system strictly in the measured state.
        """)

st.write("")
st.subheader("⚡ The Canonical Quantum Coin Toss Circuit")
st.markdown("Below is the genuine Qiskit circuit that powers our foundational quantum coin toss experiment:")

# Render Circuit Graphic
qc_coin = create_coin_toss_circuit()
circ_col1, circ_col2 = st.columns([1.6, 1.0])

with circ_col1:
    fig_circ, ascii_text = draw_circuit_figure(qc_coin)
    if fig_circ:
        st.pyplot(fig_circ, use_container_width=True)
    else:
        st.code(ascii_text, language="text")

with circ_col2:
    st.markdown("""
    **Circuit Anatomy:**
    1. **Initialization:** Qubit $q_0$ starts in ground state $|0\\rangle$.
    2. **Hadamard Gate ($H$):** Rotates the state vector to the equator of the Bloch sphere, yielding $\\frac{1}{\\sqrt{2}}(|0\\rangle + |1\\rangle)$.
    3. **Measurement:** Collapses the state onto classical bit $c_0$, producing outcome `0` (Heads) or `1` (Tails) with equal theoretical probability $P=0.5$.
    """)
    if st.button("🚀 Launch Quantum Coin Toss Experiment", type="primary", use_container_width=True):
        st.switch_page("pages/1_Quantum_Coin_Toss.py")

render_info_banner(
    "Select any module from the left sidebar or click the button above to begin exploring quantum mechanics!",
    alert_type="info",
)
