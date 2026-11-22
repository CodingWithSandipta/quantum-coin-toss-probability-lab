"""
quantum/statevector.py - Statevector & Bloch Vector Simulation Module
Extracts exact quantum state amplitudes, phases, theoretical probabilities,
and genuine Bloch vector coordinates from unmeasured Qiskit circuits.
"""

import cmath
import math
from typing import Dict, Any, List
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def calculate_statevector_data(circuit: QuantumCircuit) -> Dict[str, Any]:
    """
    Computes exact statevector amplitudes, theoretical probabilities, and Bloch
    representation for a single-qubit or multi-qubit circuit without measurements.

    Args:
        circuit: An unmeasured QuantumCircuit.

    Returns:
        Dict with statevector information:
            - 'statevector': Raw Statevector object
            - 'amplitudes': List of complex amplitudes
            - 'probabilities': Dict of theoretical probabilities {bitstring: float}
            - 'dirac_representation': Pretty-printed Dirac notation
            - 'bloch_coordinates': (x, y, z) tuple for 1-qubit states
            - 'bloch_angles': {'theta_deg': float, 'phi_deg': float}
    """
    sv = Statevector.from_instruction(circuit)
    raw_amplitudes = sv.data
    num_qubits = circuit.num_qubits

    # Theoretical probabilities from squared moduli
    probabilities: Dict[str, float] = {}
    states_data: List[Dict[str, Any]] = []

    for idx, amp in enumerate(raw_amplitudes):
        bitstring = format(idx, f"0{num_qubits}b")
        prob = float(np.abs(amp) ** 2)
        probabilities[bitstring] = round(prob, 6)

        real_part = float(np.real(amp))
        imag_part = float(np.imag(amp))
        phase_rad = float(cmath.phase(amp))
        phase_deg = round(math.degrees(phase_rad), 2)

        states_data.append({
            "basis": f"|{bitstring}⟩",
            "bitstring": bitstring,
            "amplitude": amp,
            "real": round(real_part, 4),
            "imag": round(imag_part, 4),
            "magnitude": round(float(np.abs(amp)), 4),
            "phase_deg": phase_deg,
            "probability": round(prob, 4),
        })

    # Dirac representation
    dirac_terms = []
    for item in states_data:
        if abs(item["magnitude"]) > 1e-6:
            r = item["real"]
            im = item["imag"]
            if abs(im) < 1e-6:
                amp_str = f"{r:+.3f}".rstrip("0").rstrip(".") if abs(r - 1.0) > 1e-4 and abs(r + 1.0) > 1e-4 else ("" if r > 0 else "-")
            elif abs(r) < 1e-6:
                amp_str = f"{im:+.3f}i".rstrip("0").rstrip(".") if abs(abs(im) - 1.0) > 1e-4 else ("+i" if im > 0 else "-i")
            else:
                amp_str = f"({r:.3f}{im:+.3f}i)"
            dirac_terms.append(f"{amp_str}{item['basis']}")

    dirac_str = " + ".join(dirac_terms).replace("+ -", "- ") if dirac_terms else "|0⟩"
    if dirac_str.startswith("+ "):
        dirac_str = dirac_str[2:]

    # Bloch vector for single qubit
    bloch_coords = (0.0, 0.0, 1.0)
    bloch_angles = {"theta_deg": 0.0, "phi_deg": 0.0}

    if num_qubits == 1:
        bloch_coords, bloch_angles = get_bloch_coordinates(raw_amplitudes[0], raw_amplitudes[1])

    return {
        "statevector": sv,
        "raw_amplitudes": raw_amplitudes,
        "probabilities": probabilities,
        "states_data": states_data,
        "dirac_representation": dirac_str,
        "bloch_coordinates": bloch_coords,
        "bloch_angles": bloch_angles,
        "num_qubits": num_qubits,
    }


def get_bloch_coordinates(alpha: complex, beta: complex) -> tuple:
    """
    Computes exact Bloch sphere coordinates (x, y, z) and angles (theta, phi)
    from single-qubit state |ψ⟩ = α|0⟩ + β|1⟩.

    Pauli expectation values:
        ⟨X⟩ = 2 * Re(α* β)
        ⟨Y⟩ = 2 * Im(α* β)
        ⟨Z⟩ = |α|² - |β|²
    """
    # Expectation values with Pauli operators
    x = 2.0 * float(np.real(np.conj(alpha) * beta))
    y = 2.0 * float(np.imag(np.conj(alpha) * beta))
    z = float(np.abs(alpha) ** 2 - np.abs(beta) ** 2)

    # Normalize vector to guard against floating-point inaccuracies
    norm = math.sqrt(x**2 + y**2 + z**2)
    if norm > 1e-7:
        x, y, z = x / norm, y / norm, z / norm
    else:
        x, y, z = 0.0, 0.0, 1.0

    # Spherical coordinates
    theta_rad = math.acos(max(-1.0, min(1.0, z)))
    phi_rad = math.atan2(y, x)

    theta_deg = round(math.degrees(theta_rad), 2)
    phi_deg = round(math.degrees(phi_rad), 2)

    return (round(x, 4), round(y, 4), round(z, 4)), {
        "theta_deg": theta_deg,
        "phi_deg": phi_deg,
    }
