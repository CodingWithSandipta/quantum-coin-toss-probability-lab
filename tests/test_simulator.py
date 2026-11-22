"""
tests/test_simulator.py - Unit tests for Quantum Simulation & Persistence
Covers Tests 5, 7, 8, and 9 from project specifications.
"""

import pytest
from quantum.circuits import create_coin_toss_circuit, create_multi_qubit_circuit
from quantum.simulator import execute_circuit
from quantum.classical_comparison import run_classical_coin_toss, run_comparison
from database.db import init_db, save_experiment, get_all_experiments, clear_history


def test_5_measurement_outcomes():
    """
    Test 5: Measurement
    - Execute a single-qubit Hadamard circuit.
    - Verify valid measurement outcomes ('0' and '1') are returned.
    """
    qc = create_coin_toss_circuit()
    sim_result = execute_circuit(qc, shots=500)
    counts = sim_result["normalized_counts"]

    # Verify keys
    assert set(counts.keys()) == {"0", "1"}
    # Valid non-negative counts
    assert counts["0"] >= 0
    assert counts["1"] >= 0
    # Both outcomes should generally appear in 500 shots
    assert counts["0"] > 0
    assert counts["1"] > 0


def test_7_shot_count_integrity():
    """
    Test 7: Shot count
    - Verify the total measurement counts equal the selected number of shots.
    """
    test_shots_list = [100, 500, 1000]
    qc = create_coin_toss_circuit()

    for shots in test_shots_list:
        res = execute_circuit(qc, shots=shots)
        total_observed = sum(res["normalized_counts"].values())
        assert total_observed == shots


def test_8_classical_comparison_trials():
    """
    Test 8: Classical comparison
    - Verify the total number of classical trials equals the selected number of trials.
    """
    for trials in [100, 500, 1000]:
        res = run_classical_coin_toss(trials)
        assert res["trials"] == trials
        assert (res["heads"] + res["tails"]) == trials
        assert (res["counts"]["0"] + res["counts"]["1"]) == trials

    # Test full comparison wrapper
    comp = run_comparison(300)
    assert comp["trials"] == 300
    assert (comp["classical"]["heads"] + comp["classical"]["tails"]) == 300
    assert (comp["quantum"]["heads"] + comp["quantum"]["tails"]) == 300


def test_9_experiment_history_persistence():
    """
    Test 9: Experiment history
    - Verify experiment results are saved and retrieved correctly.
    """
    # Ensure database is initialized
    assert init_db() is True

    # Clear prior test records for deterministic testing
    clear_history()

    # Save a test experiment
    test_counts = {"0": 512, "1": 488}
    record_id = save_experiment(
        experiment_type="Test Run",
        num_qubits=1,
        num_shots=1000,
        counts=test_counts,
        summary="Automated Unit Test Verification",
    )
    assert record_id is not None
    assert record_id > 0

    # Retrieve and verify
    history = get_all_experiments(limit=10)
    assert len(history) >= 1
    latest = history[0]
    assert latest["experiment_type"] == "Test Run"
    assert latest["num_qubits"] == 1
    assert latest["num_shots"] == 1000
    assert latest["counts"] == test_counts
    assert "Automated Unit Test Verification" in latest["summary"]
