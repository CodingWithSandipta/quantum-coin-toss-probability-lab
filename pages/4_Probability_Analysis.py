"""
pages/4_Probability_Analysis.py - Interactive Probability Analysis & Statistical Residuals
Explores the convergence of finite sample measurements to theoretical probability distributions.
"""

import os
import streamlit as st
from quantum.circuits import create_multi_qubit_circuit
from quantum.simulator import execute_circuit
from quantum.probability import calculate_theoretical_probabilities, calculate_probability_metrics
from components.charts import plot_theoretical_vs_observed
from components.ui_components import render_header, render_metric_card, render_info_banner
from database.db import save_experiment

st.set_page_config(
    page_title="Probability Analysis | Quantum Lab",
    page_icon="📊",
    layout="wide",
)

# Apply CSS styles
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header(
    title="📊 Probability Analysis",
    subtitle="Compare theoretical probability models against empirical AerSimulator sampling distributions.",
    badge="Statistical Analysis",
)

st.markdown("""
According to the **Law of Large Numbers**, as the number of measurement shots ($N$) increases, the empirical sample mean 
converges toward the true theoretical expectation value. In quantum computing, quantum state tomography and algorithm 
readouts must account for finite sampling error (shot noise), which scales as:
""")
st.latex(r"\sigma \approx \frac{1}{\sqrt{N}}")

st.divider()

# Controls
col_q, col_s, col_btn = st.columns([1.2, 1.2, 1.0])

with col_q:
    num_qubits = st.slider(
        "🎛️ Number of Qubits:",
        min_value=1,
        max_value=4,
        value=2,
        help="State space dimension will be 2^n.",
    )

with col_s:
    shots = st.select_slider(
        "🎯 Number of Shots (N):",
        options=[100, 500, 1000, 5000, 10000],
        value=1000,
        help="Higher shot counts reduce statistical shot noise.",
    )

with col_btn:
    st.write("")
    st.write("")
    run_btn = st.button("🚀 Analyze Probabilities", type="primary", use_container_width=True)

state_key = "prob_analysis_data"
if state_key not in st.session_state:
    st.session_state[state_key] = None

if run_btn:
    with st.spinner(f"Simulating {num_qubits} qubits ({2**num_qubits} basis states) across {shots:,} shots..."):
        qc = create_multi_qubit_circuit(num_qubits)
        sim_res = execute_circuit(qc, shots=shots)
        counts = sim_res["normalized_counts"]

        theory_probs = calculate_theoretical_probabilities(num_qubits)
        metrics = calculate_probability_metrics(counts, theory_probs, shots)

        st.session_state[state_key] = {
            "num_qubits": num_qubits,
            "shots": shots,
            "counts": counts,
            "theory_probs": theory_probs,
            "metrics": metrics,
            "sim_res": sim_res,
        }

        # Save to database
        summary = f"{num_qubits} Qubits, {shots} Shots, Avg Dev: {metrics['mean_absolute_error_percent']}%"
        save_experiment("Probability Analysis", num_qubits, shots, counts, summary)

data = st.session_state.get(state_key)

if data is not None:
    shots = data["shots"]
    n_q = data["num_qubits"]
    metrics = data["metrics"]
    most_freq = metrics["most_frequent"]
    least_freq = metrics["least_frequent"]

    st.subheader(f"📈 Empirical Convergence Metrics ({shots:,} Total Shots)")

    # Key statistics cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card(
            label="Total Measurements",
            value=f"{shots:,}",
            subvalue="Total sampled shots",
            delta_color="#06b6d4",
        )
    with m2:
        render_metric_card(
            label="Most Frequent State",
            value=f"{most_freq['state']}",
            subvalue=f"{most_freq['count']:,} ({most_freq['percent']}%)",
            delta_color="#10b981",
        )
    with m3:
        render_metric_card(
            label="Least Frequent State",
            value=f"{least_freq['state']}",
            subvalue=f"{least_freq['count']:,} ({least_freq['percent']}%)",
            delta_color="#f43f5e",
        )
    with m4:
        render_metric_card(
            label="Avg. Deviation (MAE)",
            value=f"{metrics['mean_absolute_error_percent']}%",
            subvalue=f"Max: {metrics['max_deviation_percent']}%",
            delta_color="#f59e0b" if metrics["mean_absolute_error_percent"] > 2.0 else "#38bdf8",
        )

    st.write("")

    # Dual Series Plotly Chart: Theoretical vs Observed
    fig_prob = plot_theoretical_vs_observed(
        metrics["comparison_table"],
        title=f"Theoretical Target vs Observed Qiskit Aer Probabilities (N = {shots:,})",
    )
    st.plotly_chart(fig_prob, use_container_width=True)

    # Detailed statistics dataframe
    st.markdown("#### 📋 Detailed Outcome Comparison Table")
    st.dataframe(metrics["comparison_table"], use_container_width=True)

    # Mandatory educational explanation from Section 8
    st.markdown("""
    > [!NOTE] Educational Takeaway: Finite Sampling in Quantum Measurement
    > **"Quantum measurement is probabilistic. Although the theoretical probability distribution may be uniform, 
    > the observed results can vary because the simulator samples a finite number of measurements."**
    """)

    render_info_banner(
        f"Try increasing the shot count from 100 to 10,000. As N quadruples, the expected statistical deviation roughly halves (approx 1/sqrt(N)), illustrating quantum statistical convergence.",
        alert_type="tip",
    )
else:
    st.info("👈 Choose the qubit count and shot size, then click **Analyze Probabilities** to observe the statistical distribution.")
