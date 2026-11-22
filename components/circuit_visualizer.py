"""
components/circuit_visualizer.py - Quantum Circuit & Bloch Sphere Rendering
Renders live Qiskit circuit diagrams using Matplotlib with robust fallbacks,
and produces Bloch sphere representations for single-qubit states.
"""

from typing import Optional, Tuple
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import plotly.graph_objects as go
import numpy as np


def draw_circuit_figure(circuit: QuantumCircuit) -> Tuple[Optional[plt.Figure], Optional[str]]:
    """
    Renders an actual Qiskit circuit diagram using Matplotlib.
    Applies custom dark styling to match the application aesthetic.

    Returns:
        (plt.Figure, None) if successful.
        (None, ascii_str) if Matplotlib drawing fails.
    """
    try:
        # Style configuration for Qiskit mpl drawer
        style = {
            "backgroundcolor": "#0f172a",
            "linecolor": "#94a3b8",
            "textcolor": "#f8fafc",
            "gatetextcolor": "#f8fafc",
            "subtextcolor": "#cbd5e1",
            "gatefacecolor": "#1e293b",
            "barrierfacecolor": "#475569",
            "fontsize": 11,
            "subfontsize": 9,
        }
        fig = circuit.draw(output="mpl", style=style, plot_barriers=True, reverse_bits=False)
        fig.patch.set_facecolor("#0f172a")
        return fig, None
    except Exception as e:
        # Fallback to ASCII representation if graphical render encounters issues
        try:
            ascii_text = circuit.draw(output="text")
            return None, str(ascii_text)
        except Exception:
            return None, str(circuit)


def create_interactive_bloch_sphere(
    x: float, y: float, z: float, state_label: str = "|ψ⟩"
) -> go.Figure:
    """
    Creates an interactive 3D Bloch sphere in Plotly using genuine Pauli expectation
    coordinates: x = ⟨X⟩, y = ⟨Y⟩, z = ⟨Z⟩.
    """
    # Create sphere mesh
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones(np.size(u)), np.cos(v))

    fig = go.Figure()

    # Wireframe / semi-transparent sphere surface
    fig.add_trace(
        go.Surface(
            x=xs,
            y=ys,
            z=zs,
            opacity=0.18,
            colorscale=[[0, "#334155"], [1, "#1e293b"]],
            showscale=False,
            hoverinfo="skip",
        )
    )

    # Equator and meridian guide rings
    phi_ring = np.linspace(0, 2 * np.pi, 100)
    # Equator (XY plane)
    fig.add_trace(
        go.Scatter3d(
            x=np.cos(phi_ring),
            y=np.sin(phi_ring),
            z=np.zeros(100),
            mode="lines",
            line=dict(color="#475569", width=2),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    # Meridian (XZ plane)
    fig.add_trace(
        go.Scatter3d(
            x=np.cos(phi_ring),
            y=np.zeros(100),
            z=np.sin(phi_ring),
            mode="lines",
            line=dict(color="#475569", width=2),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # Coordinate Axes: X, Y, Z
    axis_coords = [
        ([-1.2, 1.2], [0, 0], [0, 0], "+X", "-X"),
        ([0, 0], [-1.2, 1.2], [0, 0], "+Y", "-Y"),
        ([0, 0], [0, 0], [-1.2, 1.2], "|0⟩ (+Z)", "|1⟩ (-Z)"),
    ]
    colors = ["#38bdf8", "#a78bfa", "#34d399"]

    for (ax_x, ax_y, ax_z, pos_lbl, neg_lbl), col in zip(axis_coords, colors):
        fig.add_trace(
            go.Scatter3d(
                x=ax_x,
                y=ax_y,
                z=ax_z,
                mode="lines+text",
                line=dict(color=col, width=3),
                text=[neg_lbl, pos_lbl],
                textposition="top center",
                textfont=dict(color="#f8fafc", size=11),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # Statevector vector line from origin to (x, y, z)
    fig.add_trace(
        go.Scatter3d(
            x=[0, x],
            y=[0, y],
            z=[0, z],
            mode="lines",
            line=dict(color="#f43f5e", width=6),
            name="State Vector",
            hoverinfo="skip",
        )
    )

    # Statevector tip marker
    fig.add_trace(
        go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode="markers+text",
            marker=dict(size=8, color="#f43f5e", symbol="circle"),
            text=[f" {state_label} (x={x:.2f}, y={y:.2f}, z={z:.2f})"],
            textposition="top center",
            textfont=dict(color="#f43f5e", size=12),
            name="State Pointer",
            hovertemplate=(
                f"<b>{state_label}</b><br>"
                + f"⟨X⟩ = {x:.4f}<br>"
                + f"⟨Y⟩ = {y:.4f}<br>"
                + f"⟨Z⟩ = {z:.4f}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=dict(text=f"Bloch Sphere: {state_label}", x=0.05, font=dict(color="#f8fafc", size=16)),
        paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, title="X", color="#94a3b8"),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, title="Y", color="#94a3b8"),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, title="Z", color="#94a3b8"),
            aspectmode="cube",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        height=420,
    )

    return fig
