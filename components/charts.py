"""
components/charts.py - Interactive Plotly Visualizations
Provides scientifically styled interactive charts with Dark Navy / Deep Purple themes,
Cyan, Violet, and Blue accents, and rich hover details.
"""

from typing import Dict, Any, List
import plotly.graph_objects as go
import plotly.express as px

# Theme color constants
COLOR_BG = "#0f172a"          # Slate 900
COLOR_CARD_BG = "#1e293b"     # Slate 800
COLOR_CYAN = "#06b6d4"        # Cyan 500
COLOR_VIOLET = "#8b5cf6"      # Violet 500
COLOR_BLUE = "#3b82f6"        # Blue 500
COLOR_EMERALD = "#10b981"     # Emerald 500
COLOR_ROSE = "#f43f5e"        # Rose 500
COLOR_TEXT = "#f8fafc"        # Slate 50
COLOR_MUTED = "#94a3b8"       # Slate 400
COLOR_GRID = "#334155"        # Slate 700


def apply_dark_theme(fig: go.Figure) -> go.Figure:
    """Applies consistent dark navy / deep purple theme to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        font=dict(color=COLOR_TEXT, family="Inter, system-ui, sans-serif"),
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            gridcolor=COLOR_GRID,
            zerolinecolor=COLOR_GRID,
            tickfont=dict(color=COLOR_MUTED),
            title_font=dict(color=COLOR_TEXT),
        ),
        yaxis=dict(
            gridcolor=COLOR_GRID,
            zerolinecolor=COLOR_GRID,
            tickfont=dict(color=COLOR_MUTED),
            title_font=dict(color=COLOR_TEXT),
        ),
        legend=dict(
            bgcolor="rgba(30, 41, 59, 0.8)",
            bordercolor=COLOR_GRID,
            borderwidth=1,
            font=dict(color=COLOR_TEXT),
        ),
    )
    return fig


def plot_coin_toss(heads_count: int, tails_count: int, total_shots: int) -> go.Figure:
    """
    Creates an interactive bar chart for Quantum Coin Toss results.
    """
    heads_pct = round((heads_count / total_shots) * 100.0, 2)
    tails_pct = round((tails_count / total_shots) * 100.0, 2)

    categories = ["Heads (|0⟩)", "Tails (|1⟩)"]
    counts = [heads_count, tails_count]
    percentages = [heads_pct, tails_pct]
    colors = [COLOR_CYAN, COLOR_VIOLET]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=categories,
            y=percentages,
            text=[f"{pct}% ({cnt} shots)" for pct, cnt in zip(percentages, counts)],
            textposition="auto",
            marker=dict(
                color=colors,
                line=dict(color=["#38bdf8", "#a78bfa"], width=1.5),
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                + "Observed Probability: %{y:.2f}%<br>"
                + "Raw Count: %{customdata} shots<br>"
                + "Theoretical Target: 50.00%<extra></extra>"
            ),
            customdata=counts,
        )
    )

    # Reference benchmark line at 50%
    fig.add_hline(
        y=50,
        line_dash="dash",
        line_color=COLOR_EMERALD,
        annotation_text="Ideal Theoretical Probability (50%)",
        annotation_position="top right",
        annotation_font_color=COLOR_EMERALD,
    )

    fig.update_layout(
        title=dict(
            text=f"Quantum Coin Toss Distribution (Total Shots: {total_shots:,})",
            x=0.05,
            font=dict(size=18, color=COLOR_TEXT),
        ),
        yaxis=dict(title="Probability (%)", range=[0, 105]),
        xaxis=dict(title="Quantum State Outcome"),
        height=380,
    )
    return apply_dark_theme(fig)


def plot_theoretical_vs_observed(comparison_table: List[Dict[str, Any]], title: str = "Theoretical vs Observed Probability") -> go.Figure:
    """
    Creates a dual-series bar chart comparing theoretical vs observed percentages.
    """
    states = [item["State"] for item in comparison_table]
    obs_pct = [item["Observed %"] for item in comparison_table]
    theory_pct = [item["Theoretical %"] for item in comparison_table]
    counts = [item["Count"] for item in comparison_table]
    deltas = [item["Delta %"] for item in comparison_table]

    fig = go.Figure()

    # Theoretical Series
    fig.add_trace(
        go.Bar(
            name="Theoretical Probability",
            x=states,
            y=theory_pct,
            marker_color="rgba(148, 163, 184, 0.45)",
            marker_line=dict(color=COLOR_MUTED, width=1),
            hovertemplate="<b>%{x} (Theoretical)</b><br>Probability: %{y:.2f}%<extra></extra>",
        )
    )

    # Observed Series
    fig.add_trace(
        go.Bar(
            name="Observed (AerSimulator)",
            x=states,
            y=obs_pct,
            marker_color=COLOR_CYAN,
            marker_line=dict(color="#38bdf8", width=1.5),
            hovertemplate=(
                "<b>%{x} (Observed)</b><br>"
                + "Observed: %{y:.2f}%<br>"
                + "Counts: %{customdata[0]:,}<br>"
                + "Delta: %{customdata[1]:+.2f}%<extra></extra>"
            ),
            customdata=list(zip(counts, deltas)),
        )
    )

    fig.update_layout(
        barmode="group",
        title=dict(text=title, x=0.05, font=dict(size=18, color=COLOR_TEXT)),
        yaxis=dict(title="Probability (%)", range=[0, max(max(obs_pct, default=0), max(theory_pct, default=0)) * 1.25 + 5]),
        xaxis=dict(title="Computational Basis State"),
        height=420,
    )
    return apply_dark_theme(fig)


def plot_multi_qubit_distribution(comparison_table: List[Dict[str, Any]], num_qubits: int, total_shots: int) -> go.Figure:
    """
    Creates a distribution chart for 1 to 5 qubits (up to 32 states).
    """
    states = [item["State"] for item in comparison_table]
    obs_pct = [item["Observed %"] for item in comparison_table]
    counts = [item["Count"] for item in comparison_table]
    ideal_pct = (1.0 / (2**num_qubits)) * 100.0

    # Color gradient across states
    colors = px.colors.sample_colorscale("Viridis", [i / max(1, len(states) - 1) for i in range(len(states))])

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=states,
            y=obs_pct,
            marker=dict(color=colors, line=dict(color=COLOR_CYAN, width=1)),
            text=[f"{c:,}" for c in counts],
            textposition="auto" if num_qubits <= 3 else "none",
            hovertemplate=(
                "<b>Basis State: %{x}</b><br>"
                + "Observed: %{y:.2f}%<br>"
                + "Counts: %{customdata:,} shots<br>"
                + f"Ideal Target: {ideal_pct:.2f}%<extra></extra>"
            ),
            customdata=counts,
        )
    )

    fig.add_hline(
        y=ideal_pct,
        line_dash="dash",
        line_color=COLOR_ROSE,
        annotation_text=f"Uniform Target 1/2^{num_qubits} ({ideal_pct:.2f}%)",
        annotation_position="top right",
        annotation_font_color=COLOR_ROSE,
    )

    fig.update_layout(
        title=dict(
            text=f"{num_qubits}-Qubit Superposition Spectrum (2^{num_qubits} = {len(states)} States, {total_shots:,} Shots)",
            x=0.05,
            font=dict(size=18, color=COLOR_TEXT),
        ),
        yaxis=dict(title="Probability (%)"),
        xaxis=dict(title="Quantum Basis State (|q...q₀⟩)", tickangle=-45 if num_qubits >= 3 else 0),
        height=440,
    )
    return apply_dark_theme(fig)


def plot_classical_vs_quantum(classical_counts: Dict[str, int], quantum_counts: Dict[str, int], trials: int) -> go.Figure:
    """
    Creates a grouped comparison chart between Classical PRNG and Quantum AerSimulator.
    """
    categories = ["Heads (0)", "Tails (1)"]
    c_heads_pct = (classical_counts.get("0", 0) / trials) * 100.0
    c_tails_pct = (classical_counts.get("1", 0) / trials) * 100.0
    q_heads_pct = (quantum_counts.get("0", 0) / trials) * 100.0
    q_tails_pct = (quantum_counts.get("1", 0) / trials) * 100.0

    fig = go.Figure()

    # Classical trace
    fig.add_trace(
        go.Bar(
            name="Classical (Python PRNG)",
            x=categories,
            y=[c_heads_pct, c_tails_pct],
            marker_color="#f59e0b",  # Amber
            text=[f"{c_heads_pct:.2f}%", f"{c_tails_pct:.2f}%"],
            textposition="auto",
            hovertemplate="<b>Classical %{x}</b><br>Observed: %{y:.2f}%<extra></extra>",
        )
    )

    # Quantum trace
    fig.add_trace(
        go.Bar(
            name="Quantum (Qiskit Aer)",
            x=categories,
            y=[q_heads_pct, q_tails_pct],
            marker_color=COLOR_CYAN,
            text=[f"{q_heads_pct:.2f}%", f"{q_tails_pct:.2f}%"],
            textposition="auto",
            hovertemplate="<b>Quantum %{x}</b><br>Observed: %{y:.2f}%<extra></extra>",
        )
    )

    fig.add_hline(
        y=50,
        line_dash="dot",
        line_color=COLOR_EMERALD,
        annotation_text="Theoretical Fair Coin (50%)",
        annotation_position="bottom right",
    )

    fig.update_layout(
        barmode="group",
        title=dict(text=f"Classical vs Quantum Sampling ({trials:,} Trials)", x=0.05),
        yaxis=dict(title="Observed Probability (%)", range=[0, 100]),
        height=380,
    )
    return apply_dark_theme(fig)


def plot_statevector_amplitudes(states_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Visualizes real, imaginary, and absolute amplitudes for statevector states.
    """
    bases = [item["basis"] for item in states_data]
    reals = [item["real"] for item in states_data]
    imags = [item["imag"] for item in states_data]
    probs = [item["probability"] * 100.0 for item in states_data]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Real Amplitude Re(α)",
            x=bases,
            y=reals,
            marker_color=COLOR_BLUE,
            hovertemplate="<b>%{x} Real</b>: %{y:.4f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Imaginary Amplitude Im(α)",
            x=bases,
            y=imags,
            marker_color=COLOR_VIOLET,
            hovertemplate="<b>%{x} Imag</b>: %{y:.4f}i<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            name="Measurement Prob |α|² (%)",
            x=bases,
            y=probs,
            mode="lines+markers",
            yaxis="y2",
            line=dict(color=COLOR_EMERALD, width=3),
            marker=dict(size=8, color=COLOR_EMERALD),
            hovertemplate="<b>%{x} Prob</b>: %{y:.2f}%<extra></extra>",
        )
    )

    fig.update_layout(
        barmode="group",
        title=dict(text="Statevector Complex Amplitudes & Probabilities", x=0.05),
        yaxis=dict(title="Amplitude Value", range=[-1.2, 1.2]),
        yaxis2=dict(
            title="Probability (%)",
            overlaying="y",
            side="right",
            range=[0, 110],
            gridcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(title="Basis State"),
        height=380,
    )
    return apply_dark_theme(fig)
