"""
quantum/classical_comparison.py - Classical vs Quantum Simulation Comparison
Compares pseudorandom classical coin tosses with simulated quantum circuit measurements.
"""

import random
from typing import Dict, Any
from .circuits import create_coin_toss_circuit
from .simulator import execute_circuit


def run_classical_coin_toss(trials: int) -> Dict[str, Any]:
    """
    Simulates classical coin tossing using Python's standard pseudo-random number generator (Mersenne Twister).
    0 = Heads, 1 = Tails.
    """
    if trials <= 0:
        raise ValueError("Trials must be greater than zero.")

    heads = 0
    tails = 0
    for _ in range(trials):
        if random.random() < 0.5:
            heads += 1
        else:
            tails += 1

    return {
        "heads": heads,
        "tails": tails,
        "counts": {"0": heads, "1": tails},
        "heads_pct": round((heads / trials) * 100.0, 2),
        "tails_pct": round((tails / trials) * 100.0, 2),
        "trials": trials,
    }


def run_comparison(trials: int) -> Dict[str, Any]:
    """
    Executes an identical number of trials on both:
    1. Classical pseudorandom coin toss (Python PRNG).
    2. Simulated quantum coin toss (Qiskit AerSimulator measuring |0⟩ after H gate).

    Returns side-by-side data, metrics, and educational context.
    """
    classical_res = run_classical_coin_toss(trials)

    # Quantum execution
    qc = create_coin_toss_circuit()
    quantum_res = execute_circuit(qc, shots=trials)
    q_counts = quantum_res["normalized_counts"]
    q_heads = q_counts.get("0", 0)
    q_tails = q_counts.get("1", 0)

    q_heads_pct = round((q_heads / trials) * 100.0, 2)
    q_tails_pct = round((q_tails / trials) * 100.0, 2)

    return {
        "trials": trials,
        "classical": {
            "heads": classical_res["heads"],
            "tails": classical_res["tails"],
            "heads_pct": classical_res["heads_pct"],
            "tails_pct": classical_res["tails_pct"],
            "counts": classical_res["counts"],
            "heads_delta_pct": round(classical_res["heads_pct"] - 50.0, 2),
            "tails_delta_pct": round(classical_res["tails_pct"] - 50.0, 2),
        },
        "quantum": {
            "heads": q_heads,
            "tails": q_tails,
            "heads_pct": q_heads_pct,
            "tails_pct": q_tails_pct,
            "counts": q_counts,
            "heads_delta_pct": round(q_heads_pct - 50.0, 2),
            "tails_delta_pct": round(q_tails_pct - 50.0, 2),
            "execution_time_sec": quantum_res["execution_time_sec"],
        },
    }
