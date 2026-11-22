"""
tests/test_probabilities.py - Unit tests for Probability Metrics and Application Imports
Covers Test 10 and statistical verification functions.
"""

import pytest
import importlib
from quantum.probability import (
    calculate_observed_probabilities,
    calculate_theoretical_probabilities,
    calculate_probability_metrics,
)


def test_observed_probability_calculation():
    """Verifies that observed probabilities are properly computed from counts."""
    counts = {"0": 450, "1": 550}
    total_shots = 1000
    probs = calculate_observed_probabilities(counts, total_shots)

    assert pytest.approx(probs["0"], rel=1e-5) == 0.45
    assert pytest.approx(probs["1"], rel=1e-5) == 0.55


def test_probability_metrics_calculation():
    """Verifies statistical metrics, residuals, and MAE calculations."""
    counts = {"0": 480, "1": 520}
    total_shots = 1000
    theory = {"0": 0.50, "1": 0.50}

    metrics = calculate_probability_metrics(counts, theory, total_shots)

    assert metrics["total_shots"] == 1000
    assert metrics["most_frequent"]["bitstring"] == "1"
    assert metrics["least_frequent"]["bitstring"] == "0"
    # Deltas: |48% - 50%| = 2%, |52% - 50%| = 2% -> MAE = 2.0%
    assert pytest.approx(metrics["mean_absolute_error_percent"], rel=1e-4) == 2.0
    assert pytest.approx(metrics["max_deviation_percent"], rel=1e-4) == 2.0


def test_10_application_startup_and_imports():
    """
    Test 10: Application startup
    - Verify that all core quantum, database, component, and page modules
      import cleanly without syntax or missing dependency errors.
    """
    modules_to_test = [
        "quantum.circuits",
        "quantum.simulator",
        "quantum.statevector",
        "quantum.probability",
        "quantum.classical_comparison",
        "database.db",
        "components.charts",
        "components.circuit_visualizer",
        "components.ui_components",
    ]

    for mod in modules_to_test:
        imported = importlib.import_module(mod)
        assert imported is not None, f"Failed to import {mod}"
