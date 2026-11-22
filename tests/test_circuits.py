"""
tests/test_circuits.py - Unit tests for Quantum Circuits and Statevector Analysis
Covers Tests 1, 2, 3, 4, and 6 from project specifications.
"""

import pytest
import numpy as np
from quantum.circuits import (
    create_coin_toss_circuit,
    create_superposition_circuit,
    create_multi_qubit_circuit,
)
from quantum.statevector import calculate_statevector_data
from quantum.probability import calculate_theoretical_probabilities


def test_1_hadamard_gate():
    """
    Test 1: Hadamard gate
    - Initialize |0⟩.
    - Apply H.
    - Verify theoretical probabilities are 50% and 50%.
    """
    qc = create_superposition_circuit("H")
    sv_data = calculate_statevector_data(qc)
    probs = sv_data["probabilities"]

    assert pytest.approx(probs["0"], rel=1e-5) == 0.5
    assert pytest.approx(probs["1"], rel=1e-5) == 0.5

    # Check statevector amplitudes
    amplitudes = sv_data["raw_amplitudes"]
    expected_amp = 1.0 / np.sqrt(2)
    assert pytest.approx(np.real(amplitudes[0]), rel=1e-4) == expected_amp
    assert pytest.approx(np.real(amplitudes[1]), rel=1e-4) == expected_amp


def test_2_pauli_x_gate():
    """
    Test 2: Pauli-X gate
    - Initialize |0⟩.
    - Apply X.
    - Verify final state is |1⟩.
    """
    qc = create_superposition_circuit("X")
    sv_data = calculate_statevector_data(qc)
    probs = sv_data["probabilities"]

    assert pytest.approx(probs["0"], abs=1e-5) == 0.0
    assert pytest.approx(probs["1"], rel=1e-5) == 1.0

    # Dirac representation check
    assert "|1⟩" in sv_data["dirac_representation"]


def test_3_no_gate():
    """
    Test 3: No gate
    - Initialize |0⟩.
    - Verify final state remains |0⟩.
    """
    qc = create_superposition_circuit("None")
    sv_data = calculate_statevector_data(qc)
    probs = sv_data["probabilities"]

    assert pytest.approx(probs["0"], rel=1e-5) == 1.0
    assert pytest.approx(probs["1"], abs=1e-5) == 0.0
    assert "|0⟩" in sv_data["dirac_representation"]


def test_4_multi_qubit_circuit():
    """
    Test 4: Multi-qubit circuit
    - Initialize two qubits.
    - Apply Hadamard to both.
    - Verify four possible measurement outcomes have equal theoretical probability (25% each).
    """
    qc = create_multi_qubit_circuit(2)
    assert qc.num_qubits == 2
    assert qc.num_clbits == 2

    # Theoretical probabilities
    theory_probs = calculate_theoretical_probabilities(2)
    assert len(theory_probs) == 4

    for state in ["00", "01", "10", "11"]:
        assert state in theory_probs
        assert pytest.approx(theory_probs[state], rel=1e-5) == 0.25


def test_6_probability_normalization():
    """
    Test 6: Probability normalization
    - Verify theoretical probabilities sum to 1.0 across various qubit counts.
    """
    for n in range(1, 6):
        probs = calculate_theoretical_probabilities(n)
        assert len(probs) == 2**n
        total_prob = sum(probs.values())
        assert pytest.approx(total_prob, rel=1e-5) == 1.0
