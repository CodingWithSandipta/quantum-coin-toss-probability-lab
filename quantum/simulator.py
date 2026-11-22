"""
quantum/simulator.py - AerSimulator Execution Engine
Handles circuit compilation, transpilation, and execution using Qiskit Aer.
"""

import time
from typing import Dict, Any, Optional
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


_SIMULATOR_INSTANCE: Optional[AerSimulator] = None


def get_aer_simulator() -> AerSimulator:
    """
    Returns a cached AerSimulator instance to avoid repeated initialization overhead.
    """
    global _SIMULATOR_INSTANCE
    if _SIMULATOR_INSTANCE is None:
        _SIMULATOR_INSTANCE = AerSimulator()
    return _SIMULATOR_INSTANCE


def execute_circuit(circuit: QuantumCircuit, shots: int = 1000) -> Dict[str, Any]:
    """
    Executes a measured quantum circuit on Qiskit AerSimulator.

    Args:
        circuit: Transpilable QuantumCircuit with measurements.
        shots: Number of measurement repetitions (shots).

    Returns:
        Dict containing:
            - 'counts': Raw measurement counts { 'bitstring': count }
            - 'normalized_counts': Padded counts dictionary for all 2^n basis states
            - 'shots': Int shot count
            - 'num_qubits': Int qubit count
            - 'execution_time_sec': Float runtime in seconds
            - 'backend_name': Name of simulator
    """
    if shots <= 0:
        raise ValueError("Shots must be a positive integer greater than zero.")

    simulator = get_aer_simulator()
    start_time = time.perf_counter()

    # Transpile circuit for optimal simulator execution
    transpiled_circuit = transpile(circuit, simulator)
    job = simulator.run(transpiled_circuit, shots=shots)
    result = job.result()
    raw_counts = result.get_counts(circuit)
    execution_time = time.perf_counter() - start_time

    # Number of classical bits measured determines the bitstring length
    num_clbits = circuit.num_clbits if circuit.num_clbits > 0 else circuit.num_qubits
    all_possible_states = [format(i, f"0{num_clbits}b") for i in range(2**num_clbits)]

    # Ensure every possible state is represented even if count == 0
    normalized_counts: Dict[str, int] = {}
    for state in all_possible_states:
        normalized_counts[state] = raw_counts.get(state, 0)

    return {
        "counts": raw_counts,
        "normalized_counts": normalized_counts,
        "shots": shots,
        "num_qubits": circuit.num_qubits,
        "execution_time_sec": round(execution_time, 4),
        "backend_name": simulator.name,
    }


def get_formatted_counts(raw_counts: Dict[str, int], num_qubits: int = 1) -> Dict[str, int]:
    """
    Pads and sorts counts dictionary for all 2^n basis states.
    """
    all_states = [format(i, f"0{num_qubits}b") for i in range(2**num_qubits)]
    return {state: raw_counts.get(state, 0) for state in all_states}
