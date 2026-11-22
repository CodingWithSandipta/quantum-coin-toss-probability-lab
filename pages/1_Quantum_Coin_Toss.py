"""
pages/1_Quantum_Coin_Toss.py - Quantum Coin Toss Module
Primary experiment simulating a quantum coin toss using the Hadamard gate and Qiskit Aer.
"""

import os
import streamlit as st
from quantum.circuits import create_coin_toss_circuit
from quantum.simulator import execute_circuit
from quantum.probability import calculate_probability_metrics
from components.charts import plot_coin_toss, plot_theoretical_vs_observed
from components.circuit_visualizer import draw_circuit_figure
from components.ui_components import render_header, render_metric_card, render_info_banner
from database.db import save_experiment

st.set_page_config(
    page_title="Quantum Coin Toss | Quantum Lab",
    page_icon="🪙",
    layout="wide",
)

# Apply CSS styles
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header(
    title="🪙 Quantum Coin Toss",
    subtitle="Simulate quantum coin tossing using the Hadamard gate and Qiskit AerSimulator.",
    badge="Single-Qubit Superposition",
)

st.markdown("""
In classical mechanics, tossing a coin is deterministic governed by classical physics (force, air resistance, spin rate), 
though practically unpredictable. In quantum computing, a **Quantum Coin Toss** relies on genuine quantum superposition: 
a qubit in the state $|0\\rangle$ is transformed by a **Hadamard gate ($H$)** into an equal superposition state:
""")

st.latex(r"|\psi\rangle = H|0\rangle = \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle")

st.markdown(r"""
According to the Born Rule, measuring this state yields:
- **Heads ($0$)**: $P(0) = |1/\sqrt{2}|^2 = 0.5$ (50%)
- **Tails ($1$)**: $P(1) = |1/\sqrt{2}|^2 = 0.5$ (50%)
""")

st.divider()

# Interactive Controls
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1.5, 1, 1])

with col_ctrl1:
    shot_options = [100, 500, 1000, 5000, 10000]
    selected_shots = st.select_slider(
        "🎯 Select Number of Measurement Shots:",
        options=shot_options,
        value=1000,
        help="Number of times the quantum circuit is prepared, executed, and measured.",
    )

with col_ctrl2:
    st.write("")
    st.write("")
    run_clicked = st.button("🚀 Run Quantum Coin Toss", type="primary", use_container_width=True)

with col_ctrl3:
    st.write("")
    st.write("")
    reset_clicked = st.button("🔄 Reset Experiment", type="secondary", use_container_width=True)

# Session state management
if reset_clicked or "coin_toss_data" not in st.session_state:
    st.session_state["coin_toss_data"] = None

if run_clicked:
    with st.spinner(f"Preparing circuit and sampling {selected_shots:,} shots via Qiskit AerSimulator..."):
        qc = create_coin_toss_circuit()
        sim_result = execute_circuit(qc, shots=selected_shots)
        counts = sim_result["normalized_counts"]

        heads = counts.get("0", 0)
        tails = counts.get("1", 0)

        # Theoretical probabilities
        theory_probs = {"0": 0.5, "1": 0.5}
        metrics = calculate_probability_metrics(counts, theory_probs, selected_shots)

        st.session_state["coin_toss_data"] = {
            "circuit": qc,
            "counts": counts,
            "heads": heads,
            "tails": tails,
            "shots": selected_shots,
            "metrics": metrics,
            "sim_result": sim_result,
        }

        # Save to experiment history database
        summary = f"Heads: {heads} ({round(heads/selected_shots*100, 1)}%), Tails: {tails} ({round(tails/selected_shots*100, 1)}%)"
        save_experiment("Quantum Coin Toss", 1, selected_shots, counts, summary)

data = st.session_state.get("coin_toss_data")

if data is not None:
    shots = data["shots"]
    heads = data["heads"]
    tails = data["tails"]
    heads_pct = round((heads / shots) * 100.0, 2)
    tails_pct = round((tails / shots) * 100.0, 2)
    heads_diff = round(heads_pct - 50.0, 2)
    tails_diff = round(tails_pct - 50.0, 2)

    st.subheader("📈 Measurement Results")

    # Metrics Display
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        render_metric_card(
            label="Heads Count (|0⟩)",
            value=f"{heads:,}",
            subvalue=f"{heads_pct}% of shots",
            delta_color="#06b6d4",
        )
    with m2:
        render_metric_card(
            label="Tails Count (|1⟩)",
            value=f"{tails:,}",
            subvalue=f"{tails_pct}% of shots",
            delta_color="#8b5cf6",
        )
    with m3:
        delta_sign = "+" if heads_diff > 0 else ""
        render_metric_card(
            label="Heads Deviation",
            value=f"{delta_sign}{heads_diff}%",
            subvalue=f"Target: 50.00%",
            delta_color="#f59e0b" if abs(heads_diff) > 2.0 else "#10b981",
        )
    with m4:
        render_metric_card(
            label="Aer Runtime",
            value=f"{data['sim_result']['execution_time_sec']:.3f}s",
            subvalue=f"{shots:,} shots",
            delta_color="#38bdf8",
        )

    st.write("")

    # Visualizations
    v_col1, v_col2 = st.columns(2)

    with v_col1:
        fig_bar = plot_coin_toss(heads, tails, shots)
        st.plotly_chart(fig_bar, use_container_width=True)

    with v_col2:
        comp_table = data["metrics"]["comparison_table"]
        fig_comp = plot_theoretical_vs_observed(
            comp_table, title=f"Theoretical (50%) vs Observed Comparison ({shots:,} Shots)"
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    # Detailed statistics table and Circuit diagram
    t_col1, t_col2 = st.columns([1.2, 1.0])

    with t_col1:
        st.markdown("#### 📋 Detailed Distribution Table")
        st.table(data["metrics"]["comparison_table"])

    with t_col2:
        st.markdown("#### ⚡ Executed Quantum Circuit")
        fig_qc, ascii_qc = draw_circuit_figure(data["circuit"])
        if fig_qc:
            st.pyplot(fig_qc, use_container_width=True)
        else:
            st.code(ascii_qc, language="text")

    # Scientific Explanation requirement from Section 5
    st.markdown("""
    > [!NOTE] Scientific Interpretation
    > **The Hadamard gate transforms the initial $|0\\rangle$ qubit into an equal superposition of $|0\\rangle$ and $|1\\rangle$. 
    > When the qubit is measured, the simulator produces either $0$ or $1$. Repeating the experiment produces an approximately equal distribution.**
    """)

    render_info_banner(
        f"Notice that for {shots:,} shots, the observed outcomes are close to 50% but not necessarily exactly 50.00%. "
        "This stochastic variance reflects genuine statistical sampling from the quantum state.",
        alert_type="tip",
    )
else:
    st.info("👈 Select your desired shot count and click **Run Quantum Coin Toss** to execute the simulation.")
    qc_preview = create_coin_toss_circuit()
    st.markdown("#### Circuit Diagram Preview:")
    fig_qc, ascii_qc = draw_circuit_figure(qc_preview)
    if fig_qc:
        st.pyplot(fig_qc, use_container_width=True)
    else:
        st.code(ascii_qc, language="text")
