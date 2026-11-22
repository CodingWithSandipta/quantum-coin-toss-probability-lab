"""
pages/2_Superposition_Explorer.py - Single Qubit Superposition & Gate Explorer
Investigate single-qubit quantum gates (H, X, Y, Z, None), inspect complex statevector
amplitudes, theoretical measurement probabilities, and 3D Bloch sphere representation.
"""

import os
import streamlit as st
import numpy as np

from quantum.circuits import create_superposition_circuit, GATE_DESCRIPTIONS
from quantum.statevector import calculate_statevector_data
from components.charts import plot_statevector_amplitudes
from components.circuit_visualizer import draw_circuit_figure, create_interactive_bloch_sphere
from components.ui_components import render_header, render_metric_card, render_dirac_formula, render_info_banner

st.set_page_config(
    page_title="Superposition Explorer | Quantum Lab",
    page_icon="🌌",
    layout="wide",
)

# Apply CSS styles
css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header(
    title="🌌 Superposition Explorer",
    subtitle="Analyze single-qubit state transformations, complex amplitudes, and 3D Bloch vector dynamics.",
    badge="Statevector Simulation",
)

st.markdown("""
A single qubit initialized in the ground state $|0\\rangle$ can be manipulated by unitary quantum logic gates. 
Unitary operations are represented by $2 \\times 2$ complex matrices that preserve vector norm: $\\langle \\psi | \\psi \\rangle = 1$.
""")

st.divider()

# Controls: Gate Selection
gate_choices = ["None", "H", "X", "Y", "Z"]
gate_labels = {
    "None": "Identity (No Gate) — Leaves |0⟩ unchanged",
    "H": "Hadamard (H) — Equal Superposition (|0⟩ + |1⟩)/√2",
    "X": "Pauli-X (NOT) — Bit Flip to |1⟩",
    "Y": "Pauli-Y — Bit & Phase Flip to i|1⟩",
    "Z": "Pauli-Z — Phase Flip (leaves |0⟩ unchanged)",
}

selected_gate = st.selectbox(
    "Select Quantum Gate Operation:",
    options=gate_choices,
    format_func=lambda g: f"{g}: {gate_labels[g]}",
    index=1,  # Default to Hadamard
)

# Gate metadata
gate_info = GATE_DESCRIPTIONS[selected_gate]

# Construct genuine Qiskit circuit without measurement
qc = create_superposition_circuit(selected_gate)
sv_data = calculate_statevector_data(qc)

# Display State Transformations Overview
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    render_metric_card(
        label="Initial State",
        value="|0⟩",
        subvalue="Computational ground state",
        delta_color="#94a3b8",
    )

with col_info2:
    render_metric_card(
        label="Applied Gate",
        value=f"{selected_gate} Gate",
        subvalue=gate_info["name"],
        delta_color="#06b6d4",
    )

with col_info3:
    render_metric_card(
        label="Final State |ψ⟩",
        value=sv_data["dirac_representation"],
        subvalue=f"Prob(0): {sv_data['probabilities']['0']*100:.0f}%, Prob(1): {sv_data['probabilities']['1']*100:.0f}%",
        delta_color="#8b5cf6",
    )

st.write("")

# Detailed Statevector and Bloch Sphere Visualizations
col_bloch, col_chart = st.columns([1.1, 1.3])

with col_bloch:
    st.markdown("#### 🌐 Genuine 3D Bloch Sphere")
    x, y, z = sv_data["bloch_coordinates"]
    angles = sv_data["bloch_angles"]

    fig_bloch = create_interactive_bloch_sphere(x, y, z, state_label=sv_data["dirac_representation"])
    st.plotly_chart(fig_bloch, use_container_width=True)

    st.markdown(
        f"**Bloch Vector Coordinates:** `⟨X⟩ = {x:.3f}`, `⟨Y⟩ = {y:.3f}`, `⟨Z⟩ = {z:.3f}`  \n"
        f"**Spherical Polar Angles:** $\\theta = {angles['theta_deg']}^\\circ$, $\\phi = {angles['phi_deg']}^\\circ$"
    )

with col_chart:
    st.markdown("#### 📊 Complex Amplitudes & Probabilities")
    fig_amp = plot_statevector_amplitudes(sv_data["states_data"])
    st.plotly_chart(fig_amp, use_container_width=True)

    # Statevector Amplitudes Table
    amp_rows = []
    for item in sv_data["states_data"]:
        amp_rows.append({
            "Basis": item["basis"],
            "Re(α)": item["real"],
            "Im(α)": item["imag"],
            "Magnitude |α|": item["magnitude"],
            "Phase Angle": f"{item['phase_deg']}°",
            "Probability |α|²": f"{item['probability']*100:.2f}%",
        })
    st.dataframe(amp_rows, use_container_width=True)

st.divider()

# Circuit Diagram and Theoretical Math Explanation
c_col1, c_col2 = st.columns([1.2, 1.2])

with c_col1:
    st.markdown("#### ⚡ Qiskit Quantum Circuit")
    fig_qc, ascii_qc = draw_circuit_figure(qc)
    if fig_qc:
        st.pyplot(fig_qc, use_container_width=True)
    else:
        st.code(ascii_qc, language="text")

with c_col2:
    st.markdown(f"#### 📐 Matrix Representation: {gate_info['name']}")
    st.markdown(f"**Gate Matrix:**")
    st.code(gate_info["matrix"], language="text")
    st.markdown(f"**Gate Description:** {gate_info['description']}")

# Important note regarding Phase and Measurement from Section 6
render_info_banner(
    "**Crucial Quantum Principle: Relative Phase vs Measurement Probabilities**  \n"
    "Notice that for both the **Pauli-X** and **Pauli-Y** gates applied to $|0\\rangle$, the final state yields outcome $1$ with 100% probability, "
    "even though Pauli-Y introduces an imaginary phase factor $i = e^{i\\pi/2}$. "
    "Similarly, the **Pauli-Z** gate does not change the computational basis measurement of $|0\\rangle$. "
    "However, quantum phase is not irrelevant! In multi-gate algorithms (such as the Quantum Fourier Transform or Grover's Search), "
    "phases create constructive and destructive quantum interference when combined with subsequent Hadamard gates.",
    alert_type="info",
)
