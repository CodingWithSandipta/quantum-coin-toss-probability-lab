"""
quantum/probability.py - Quantum Probability & Statistical Analysis Module
Calculates observed and theoretical probabilities, residuals, and deviations.
"""

from typing import Dict, Any, List


def calculate_observed_probabilities(counts: Dict[str, int], total_shots: int) -> Dict[str, float]:
    """
    Computes observed fractional probabilities from measurement counts.
    P_obs(x) = counts(x) / total_shots
    """
    if total_shots <= 0:
        raise ValueError("Total shots must be greater than zero.")

    return {state: count / total_shots for state, count in counts.items()}


def calculate_theoretical_probabilities(num_qubits: int) -> Dict[str, float]:
    """
    Computes theoretical probabilities for n independent qubits in equal superposition.
    P_theory(x) = 1 / 2^n for every basis state x.
    """
    if num_qubits < 1:
        raise ValueError("Number of qubits must be at least 1.")

    num_outcomes = 2**num_qubits
    ideal_prob = 1.0 / num_outcomes
    all_states = [format(i, f"0{num_qubits}b") for i in range(num_outcomes)]
    return {state: ideal_prob for state in all_states}


def calculate_probability_metrics(
    observed_counts: Dict[str, int],
    theoretical_probs: Dict[str, float],
    total_shots: int,
) -> Dict[str, Any]:
    """
    Computes statistical comparison metrics between observed and theoretical distributions.

    Returns:
        Dict containing:
            - 'comparison_table': List of per-state rows (counts, observed %, theoretical %, delta %)
            - 'max_deviation_percent': Float
            - 'mean_absolute_error_percent': Float (average probability deviation)
            - 'most_frequent': Tuple (state, count, percentage)
            - 'least_frequent': Tuple (state, count, percentage)
            - 'total_shots': Int
    """
    if total_shots <= 0:
        raise ValueError("Total shots must be greater than zero.")

    comparison_table: List[Dict[str, Any]] = []
    abs_deviations = []

    sorted_states = sorted(theoretical_probs.keys())
    for state in sorted_states:
        count = observed_counts.get(state, 0)
        obs_prob = count / total_shots
        theory_prob = theoretical_probs.get(state, 0.0)

        diff = obs_prob - theory_prob
        abs_diff = abs(diff)
        abs_deviations.append(abs_diff * 100.0)

        comparison_table.append({
            "State": f"|{state}⟩",
            "Bitstring": state,
            "Count": count,
            "Observed Prob": round(obs_prob, 4),
            "Observed %": round(obs_prob * 100.0, 2),
            "Theoretical Prob": round(theory_prob, 4),
            "Theoretical %": round(theory_prob * 100.0, 2),
            "Delta %": round(diff * 100.0, 2),
            "Abs Delta %": round(abs_diff * 100.0, 2),
        })

    # Find most and least frequent outcomes
    most_freq_state = max(sorted_states, key=lambda s: observed_counts.get(s, 0))
    least_freq_state = min(sorted_states, key=lambda s: observed_counts.get(s, 0))

    most_count = observed_counts.get(most_freq_state, 0)
    least_count = observed_counts.get(least_freq_state, 0)

    max_deviation = max(abs_deviations) if abs_deviations else 0.0
    mean_deviation = sum(abs_deviations) / len(abs_deviations) if abs_deviations else 0.0

    return {
        "comparison_table": comparison_table,
        "max_deviation_percent": round(max_deviation, 3),
        "mean_absolute_error_percent": round(mean_deviation, 3),
        "most_frequent": {
            "state": f"|{most_freq_state}⟩",
            "bitstring": most_freq_state,
            "count": most_count,
            "percent": round((most_count / total_shots) * 100.0, 2),
        },
        "least_frequent": {
            "state": f"|{least_freq_state}⟩",
            "bitstring": least_freq_state,
            "count": least_count,
            "percent": round((least_count / total_shots) * 100.0, 2),
        },
        "total_shots": total_shots,
    }
