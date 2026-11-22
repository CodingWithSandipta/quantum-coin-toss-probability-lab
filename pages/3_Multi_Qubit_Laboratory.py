"""
pages/3_Multi_Qubit_Laboratory.py - Multi-Qubit Independent Superposition Laboratory
Simulates n-qubit independent superpositions (1 to 5 qubits) using Qiskit Aer.
"""

import os
import streamlit as st
from quantum.circuits import create_multi_qubit_circuit
from quantum.simulator import execute_circuit
from quantum.probability import calculate_theoretical_probabilities, calculate_probability_metrics
from components.charts import plot_multi_qubit_distribution, plot_theoretical_vs_observed
from components.circuit_visualizer import draw_circuit_figure
from components.ui_components import render_header, render_metric_card, render_info_banner
from database.db import save_experiment

st.set_page_config(
    page_title="Multi-Qubit Laboratory | Quantum Lab",
    page_icon="🌌",
    layout="wide",
)

# Apply CSS styles
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header(
    title="🌌 Multi-Qubit Laboratory",
    subtitle="Scale from 1 to 5 qubits: explore exponential state space expansion (2ⁿ) and uniform superposition.",
    badge="1 to 5 Qubits",
)

st.markdown("""
When multiple qubits are each placed into an equal superposition via independent Hadamard gates ($H^{\\otimes n}$), 
the composite state is the tensor product of each individual qubit:
""")

st.latex(r"|\psi_n\rangle = H^{\otimes n} |0\dots 0\rangle = \frac{1}{\sqrt{2^n}} \sum_{x \in \{0, 1\}^n} |x\rangle")

st.markdown("""
Every one of the $2^n$ basis states has an identical theoretical probability of observation:
""")
st.latex(r"P(x) = \left|\frac{1}{\sqrt{2^n}}\right|^2 = \frac{1}{2^n}")

st.divider()

# Controls
c_qubits, c_shots, c_action = st.columns([1.2, 1.2, 1.0])

with c_qubits:
    num_qubits = st.slider(
        "🎛️ Number of Qubits ($n$):",
        min_value=1,
        max_value=5,
        value=3,
        help="Number of qubits in the circuit. Produces 2^n orthogonal states.",
    )

with c_shots:
    shot_options = [100, 500, 1000, 5000]
    shots = st.select_slider(
        "🎯 Measurement Shots:",
        options=shot_options,
        value=1000,
        help="Total number of circuit executions.",
    )

with c_action:
    st.write("")
    st.write("")
    run_btn = st.button("🚀 Run Multi-Qubit Experiment", type="primary", use_container_width=True)

# State initialization
state_key = "multi_qubit_data"
if state_key not in st.session_state:
    st.session_state[state_key] = None

if run_btn:
    with st.spinner(f"Simulating {num_qubits} qubits (2^{num_qubits} = {2**num_qubits} states) with {shots:,} shots..."):
        qc = create_multi_qubit_circuit(num_qubits)
        sim_res = execute_circuit(qc, shots=shots)
        counts = sim_res["normalized_counts"]

        theory_probs = calculate_theoretical_probabilities(num_qubits)
        metrics = calculate_probability_metrics(counts, theory_probs, shots)

        st.session_state[state_key] = {
            "num_qubits": num_qubits,
            "shots": shots,
            "circuit": qc,
            "counts": counts,
            "theory_probs": theory_probs,
            "metrics": metrics,
            "sim_res": sim_res,
        }

        # Save to database
        summary = f"{num_qubits} Qubits, 2^{num_qubits}={2**num_qubits} states. Shots: {shots}. MAE: {metrics['mean_absolute_error_percent']}%"
        save_experiment("Multi-Qubit Laboratory", num_qubits, shots, counts, summary)

data = st.session_state.get(state_key)

if data is not None:
    n_q = data["num_qubits"]
    n_shots = data["shots"]
    n_states = 2**n_q
    ideal_pct = round((1.0 / n_states) * 100.0, 3)
    metrics = data["metrics"]

    st.subheader(f"📊 Results: {n_q} Qubits ({n_states} Total Computational States)")

    # Key metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card(
            label="State Space Dimension",
            value=f"{n_states} States",
            subvalue=f"2^{n_q} basis configurations",
            delta_color="#06b6d4",
        )
    with m2:
        render_metric_card(
            label="Ideal Probability",
            value=f"{ideal_pct}%",
            subvalue=f"1 / {n_states} per outcome",
            delta_color="#10b981",
        )
    with m3:
        render_metric_card(
            label="Avg. Deviation (MAE)",
            value=f"{metrics['mean_absolute_error_percent']}%",
            subvalue=f"Max: {metrics['max_deviation_percent']}%",
            delta_color="#f59e0b" if metrics["mean_absolute_error_percent"] > 2.0 else "#38bdf8",
        )
    with m4:
        render_metric_card(
            label="Simulator Runtime",
            value=f"{data['sim_res']['execution_time_sec']:.3f}s",
            subvalue=f"Qiskit Aer (shots={n_shots:,})",
            delta_color="#8b5cf6",
        )

    st.write("")

    # Histogram Distribution
    fig_hist = plot_multi_qubit_distribution(metrics["comparison_table"], n_q, n_shots)
    st.plotly_chart(fig_hist, use_container_width=True)

    # Circuit diagram and data table
    c1, c2 = st.columns([1.2, 1.2])

    with c1:
        st.markdown("#### ⚡ Generated Qiskit Multi-Qubit Circuit")
        fig_qc, ascii_qc = draw_circuit_figure(data["circuit"])
        if fig_qc:
            st.pyplot(fig_qc, use_container_width=True)
        else:
            st.code(ascii_qc, language="text")

    with c2:
        st.markdown("#### 📋 Measurement Counts & Deviation Table")
        st.dataframe(metrics["comparison_table"], use_container_width=True, height=350)

    # Vital Theoretical Distinction requirement from Section 7
    render_info_banner(
        "**Important Physics Distinction: Independent Superposition vs Entanglement**  \n"
        f"In this circuit, a Hadamard gate is applied independently to each of the {n_q} qubits without any entangling gates (such as CNOT or CZ). "
        "Therefore, the qubits are in a separable product state: $|\\psi\\rangle = |+\\rangle \\otimes |+\\rangle \\otimes \\dots \\otimes |+\\rangle$. "
        "Measuring qubit $q_0$ provides zero information about the outcome of qubit $q_1$. "
        "They are purely independent random variables that collectively span the $2^n$ basis states.",
        alert_type="info",
    )
else:
    st.info("👈 Select the number of qubits (1 to 5) and measurement shots, then click **Run Multi-Qubit Experiment**.")
    qc_prev = create_multi_qubit_circuit(2)
    st.markdown("#### 2-Qubit Circuit Preview ($H^{\\otimes 2}$):")
    fig_qc, ascii_qc = draw_circuit_figure(qc_prev)
    if fig_qc:
        st.pyplot(fig_qc, use_container_width=True)
    else:
        st.code(ascii_qc, language="text")
