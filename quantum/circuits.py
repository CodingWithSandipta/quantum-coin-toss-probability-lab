"""
quantum/circuits.py - Genuine Qiskit Circuit Construction Module
Constructs standard quantum circuits for quantum coin tossing, single-qubit
gate explorations, and multi-qubit independent superposition states.
"""

from typing import Dict, Any
from qiskit import QuantumCircuit

GATE_DESCRIPTIONS: Dict[str, Dict[str, Any]] = {
    "None": {
        "name": "Identity / No Gate (I)",
        "symbol": "I",
        "matrix": "[[1, 0], [0, 1]]",
        "state_equation": "|0⟩",
        "description": "Leaves the qubit in its initial ground state |0⟩. The statevector is [1, 0]^T.",
        "theory_probs": {"0": 1.0, "1": 0.0},
    },
    "H": {
        "name": "Hadamard Gate (H)",
        "symbol": "H",
        "matrix": "1/√2 [[1, 1], [1, -1]]",
        "state_equation": "(|0⟩ + |1⟩) / √2",
        "description": "Creates an equal, balanced superposition with real positive amplitudes. Fundamental for quantum coin tossing.",
        "theory_probs": {"0": 0.5, "1": 0.5},
    },
    "X": {
        "name": "Pauli-X Gate (NOT)",
        "symbol": "X",
        "matrix": "[[0, 1], [1, 0]]",
        "state_equation": "|1⟩",
        "description": "Flips the basis state |0⟩ to |1⟩ (bit-flip). Corresponds to a π rotation around the X-axis on the Bloch sphere.",
        "theory_probs": {"0": 0.0, "1": 1.0},
    },
    "Y": {
        "name": "Pauli-Y Gate",
        "symbol": "Y",
        "matrix": "[[0, -i], [i, 0]]",
        "state_equation": "i|1⟩",
        "description": "Applies a bit-flip and a π/2 phase shift. Rotates the statevector around the Y-axis by π. Produces imaginary amplitude.",
        "theory_probs": {"0": 0.0, "1": 1.0},
    },
    "Z": {
        "name": "Pauli-Z Gate (Phase Flip)",
        "symbol": "Z",
        "matrix": "[[1, 0], [0, -1]]",
        "state_equation": "|0⟩",
        "description": "Leaves |0⟩ unchanged, but flips the phase of |1⟩ to -|1⟩. In the computational basis alone on |0⟩, measurement probabilities are unaffected.",
        "theory_probs": {"0": 1.0, "1": 0.0},
    },
}


def create_coin_toss_circuit() -> QuantumCircuit:
    """
    Constructs the canonical 1-qubit Quantum Coin Toss circuit.
    Sequence:
        |0⟩ ─── H ─── Measure
    Theoretical Probabilities:
        P(|0⟩ = Heads) = 0.5
        P(|1⟩ = Tails) = 0.5
    """
    qc = QuantumCircuit(1, 1, name="Quantum Coin Toss")
    qc.h(0)
    qc.measure(0, 0)
    return qc


def create_superposition_circuit(gate_name: str = "H") -> QuantumCircuit:
    """
    Constructs an unmeasured single-qubit circuit for statevector inspection.
    Args:
        gate_name: One of 'None', 'H', 'X', 'Y', 'Z' (case-insensitive).
    Returns:
        QuantumCircuit: 1-qubit circuit without measurements.
    """
    qc = QuantumCircuit(1, name=f"Single Qubit ({gate_name})")
    normalized_gate = gate_name.strip().upper()

    if normalized_gate == "NONE" or normalized_gate == "NO GATE":
        pass  # Identity / initial state |0>
    elif normalized_gate == "H":
        qc.h(0)
    elif normalized_gate == "X":
        qc.x(0)
    elif normalized_gate == "Y":
        qc.y(0)
    elif normalized_gate == "Z":
        qc.z(0)
    else:
        raise ValueError(f"Unsupported gate: '{gate_name}'. Supported: None, H, X, Y, Z")

    return qc


def create_measured_single_qubit_circuit(gate_name: str = "H") -> QuantumCircuit:
    """
    Constructs a measured single-qubit circuit for shot-based sampling.
    """
    qc = QuantumCircuit(1, 1, name=f"Single Qubit Measured ({gate_name})")
    normalized_gate = gate_name.strip().upper()

    if normalized_gate == "NONE" or normalized_gate == "NO GATE":
        pass
    elif normalized_gate == "H":
        qc.h(0)
    elif normalized_gate == "X":
        qc.x(0)
    elif normalized_gate == "Y":
        qc.y(0)
    elif normalized_gate == "Z":
        qc.z(0)
    else:
        raise ValueError(f"Unsupported gate: '{gate_name}'. Supported: None, H, X, Y, Z")

    qc.measure(0, 0)
    return qc


def create_multi_qubit_circuit(num_qubits: int) -> QuantumCircuit:
    """
    Constructs an n-qubit independent superposition circuit.
    Initializes all qubits to |0>, applies an individual Hadamard gate to each qubit,
    and measures each into its corresponding classical bit.

    Sequence:
        |0...0⟩ ─── H ⊗ ... ⊗ H ─── Measure All

    Args:
        num_qubits: Integer between 1 and 5 (clamped/validated).
    Returns:
        QuantumCircuit with num_qubits qubits and classical bits.
    """
    if not (1 <= num_qubits <= 10):
        raise ValueError("Number of qubits must be between 1 and 10.")

    qc = QuantumCircuit(num_qubits, num_qubits, name=f"{num_qubits}-Qubit Superposition")
    for q in range(num_qubits):
        qc.h(q)
    qc.measure(range(num_qubits), range(num_qubits))
    return qc
