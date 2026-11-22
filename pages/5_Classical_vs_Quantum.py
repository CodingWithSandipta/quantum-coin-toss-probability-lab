"""
pages/5_Classical_vs_Quantum.py - Classical vs Quantum Coin Toss Comparison
Comparative laboratory contrasting algorithmic pseudorandom sampling with simulated quantum state measurement.
"""

import os
import streamlit as st
import pandas as pd

from quantum.classical_comparison import run_comparison
from components.charts import plot_classical_vs_quantum
from components.ui_components import render_header, render_metric_card, render_info_banner
from database.db import save_experiment

st.set_page_config(
    page_title="Classical vs Quantum | Quantum Lab",
    page_icon="⚖️",
    layout="wide",
)

# Apply CSS styles
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header(
    title="⚖️ Classical vs Quantum Coin Toss",
    subtitle="Compare conventional pseudo-random number generation with simulated quantum superposition measurement.",
    badge="Comparative Analysis",
)

st.markdown("""
How does a classical algorithmic coin toss compare with a quantum coin toss? 
In this module, we benchmark both methods side-by-side using identical trial sizes.
""")

st.divider()

# Controls
col1, col2 = st.columns([2, 1])

with col1:
    trial_options = [100, 500, 1000, 5000, 10000]
    trials = st.select_slider(
        "🎯 Select Number of Trials / Shots for Both Systems:",
        options=trial_options,
        value=1000,
        help="Both the classical PRNG and the Qiskit Aer simulator will run this exact number of samples.",
    )

with col2:
    st.write("")
    st.write("")
    run_btn = st.button("🚀 Run Comparative Benchmark", type="primary", use_container_width=True)

state_key = "classical_vs_quantum_data"
if state_key not in st.session_state:
    st.session_state[state_key] = None

if run_btn:
    with st.spinner(f"Running {trials:,} trials on Classical PRNG and Qiskit AerSimulator..."):
        res = run_comparison(trials)
        st.session_state[state_key] = res

        # Save to database
        summary = f"Classical (H: {res['classical']['heads_pct']}%, T: {res['classical']['tails_pct']}%) vs Quantum (H: {res['quantum']['heads_pct']}%, T: {res['quantum']['tails_pct']}%)"
        save_experiment("Classical vs Quantum", 1, trials, res["quantum"]["counts"], summary)

data = st.session_state.get(state_key)

if data is not None:
    c = data["classical"]
    q = data["quantum"]
    n = data["trials"]

    st.subheader(f"📊 Benchmark Results ({n:,} Total Trials)")

    # Side-by-side Metric Cards
    col_c, col_q = st.columns(2)

    with col_c:
        st.markdown("#### 💻 Classical (Python PRNG - Mersenne Twister)")
        mc1, mc2 = st.columns(2)
        with mc1:
            render_metric_card(
                label="Classical Heads",
                value=f"{c['heads']:,}",
                subvalue=f"{c['heads_pct']}% (Δ {c['heads_delta_pct']:+}%)",
                delta_color="#f59e0b",
            )
        with mc2:
            render_metric_card(
                label="Classical Tails",
                value=f"{c['tails']:,}",
                subvalue=f"{c['tails_pct']}% (Δ {c['tails_delta_pct']:+}%)",
                delta_color="#f59e0b",
            )

    with col_q:
        st.markdown("#### ⚛️ Quantum Simulation (Qiskit AerSimulator)")
        mq1, mq2 = st.columns(2)
        with mq1:
            render_metric_card(
                label="Quantum Heads (|0⟩)",
                value=f"{q['heads']:,}",
                subvalue=f"{q['heads_pct']}% (Δ {q['heads_delta_pct']:+}%)",
                delta_color="#06b6d4",
            )
        with mq2:
            render_metric_card(
                label="Quantum Tails (|1⟩)",
                value=f"{q['tails']:,}",
                subvalue=f"{q['tails_pct']}% (Δ {q['tails_delta_pct']:+}%)",
                delta_color="#06b6d4",
            )

    st.write("")

    # Visual Comparison Chart
    fig_comp = plot_classical_vs_quantum(c["counts"], q["counts"], n)
    st.plotly_chart(fig_comp, use_container_width=True)

    # Comparison Table
    st.markdown("#### 📋 Detailed Comparison Table")
    table_df = pd.DataFrame([
        {
            "Metric": "Heads Count (0)",
            "Classical PRNG": f"{c['heads']:,}",
            "Quantum Aer": f"{q['heads']:,}",
            "Ideal Target": f"{n // 2:,}",
        },
        {
            "Metric": "Tails Count (1)",
            "Classical PRNG": f"{c['tails']:,}",
            "Quantum Aer": f"{q['tails']:,}",
            "Ideal Target": f"{n // 2:,}",
        },
        {
            "Metric": "Heads Percentage",
            "Classical PRNG": f"{c['heads_pct']}%",
            "Quantum Aer": f"{q['heads_pct']}%",
            "Ideal Target": "50.00%",
        },
        {
            "Metric": "Tails Percentage",
            "Classical PRNG": f"{c['tails_pct']}%",
            "Quantum Aer": f"{q['tails_pct']}%",
            "Ideal Target": "50.00%",
        },
        {
            "Metric": "Heads Deviation from 50%",
            "Classical PRNG": f"{c['heads_delta_pct']:+}%",
            "Quantum Aer": f"{q['heads_delta_pct']:+}%",
            "Ideal Target": "0.00%",
        },
    ])
    st.dataframe(table_df, use_container_width=True)

    st.divider()

    # Scientific Accuracy Note requirement from Section 9
    st.subheader("🔬 Scientific Accuracy & Nuance")
    
    st.markdown("""
    > [!IMPORTANT] Fundamental Scientific Nuance
    > **A local quantum simulator is NOT automatically a source of true physical quantum randomness.**
    > 
    > 1. **Underlying Mechanism:**  
    >    - The **classical** experiment uses Python's standard `random` module, which implements the **Mersenne Twister** algorithm (MT19937)—a deterministic pseudorandom number generator (PRNG).
    >    - The **quantum** experiment compiles a Qiskit `QuantumCircuit`, applies unitary matrix mathematics ($H = \\frac{1}{\\sqrt{2}}\\begin{bmatrix}1 & 1\\\\ 1 & -1\\end{bmatrix}$), and samples from the resulting statevector $|\\psi\\rangle$ using **Qiskit Aer**'s C++ simulation engine.
    >
    > 2. **Physical Quantum Computers vs Simulators:**  
    >    - On a **physical quantum processor (QPU)**, randomness arises from fundamental quantum indeterminism governed by the Heisenberg uncertainty principle and wave function collapse.
    >    - In contrast, our local **AerSimulator** runs on a classical CPU and internally generates sampling statistics via numerical pseudorandom routines.
    >
    > 3. **No Quantum Advantage Claimed:**  
    >    - We do **not** claim that this simulated quantum coin toss is faster, more random in a physical sense, or computationally superior to classical coin tossing.
    >    - This experiment serves purely as an **educational model** to understand how quantum states are formulated, transformed by unitary gates, and sampled upon measurement.
    """)
else:
    st.info("👈 Select the number of trials and click **Run Comparative Benchmark** to compare both systems.")
