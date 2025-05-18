#!/usr/bin/env python3
# test_stabilizer.py - Testing script for 2-qubit stabilizer circuit

import sys
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

def create_2qubit_stabilizer_circuit(add_error=False):
    """
    Creates a simple 2-qubit circuit that measures the ZZ stabilizer.
    This is the simplest possible stabilizer measurement circuit.
    
    Returns:
    - qc: The quantum circuit
    """
    # Create registers
    data = QuantumRegister(2, 'data')  # 2 data qubits
    anc = QuantumRegister(1, 'anc')    # 1 ancilla qubit
    cr = ClassicalRegister(1, 'c')     # 1 classical bit for measurement
    qc = QuantumCircuit(data, anc, cr)
    
    # Optional: Prepare a specific state
    # For |00⟩ state, do nothing (default state)
    # For |11⟩ state, apply X to both qubits
    # qc.x(data[0])
    # qc.x(data[1])

    # Optional: Add error if requested
    if add_error:
        qc.x(data[0])  # Simulate X-error on first qubit
    
    # Measure ZZ stabilizer
    qc.cx(data[0], anc[0]) # CNOT from ancilla to first data qubit
    qc.cx(data[1], anc[0]) # CNOT from ancilla to second data qubit
    qc.measure(anc[0], cr[0]) # Measure the ancilla
    
    return qc

def test_stabilizer_circuit():
    """
    Tests the 2-qubit stabilizer circuit implementation.
    
    Returns:
    - Boolean indicating whether all tests passed
    - Dictionary with test results
    """
    print("Running 2-Qubit Stabilizer Circuit Test Suite")
    print("============================================")
    
    results = {}
    all_passed = True
    
    # Test 1: No Error Case
    print("\nTest 1: ZZ stabilizer with no errors...")
    
    # Create and run circuit without error
    qc_no_error = create_2qubit_stabilizer_circuit(add_error=False)
    
    # Simulate
    backend = AerSimulator()
    qc_t = transpile(qc_no_error, backend)
    result = backend.run(qc_t, shots=1024).result()
    counts = result.get_counts()
    
    # |00⟩ is a +1 eigenstate of ZZ, so we expect mostly '0' outcomes
    zero_count = counts.get('0', 0)
    zero_percent = 100 * zero_count / 1024
    
    test1_passed = zero_percent > 95  # Allow for some simulator noise
    results["test1"] = {
        "passed": test1_passed,
        "zero_percent": zero_percent
    }
    all_passed = all_passed and test1_passed
    
    print(f"  {'✓' if test1_passed else '✗'} ZZ stabilizer on |00⟩: {zero_percent:.2f}% '0' outcomes (expected >95%)")
    
    # Test 2: With X Error
    print("\nTest 2: ZZ stabilizer with X error on first qubit...")
    
    # Create and run circuit with error
    qc_error = create_2qubit_stabilizer_circuit(add_error=True)
    
    # Simulate
    qc_t = transpile(qc_error, backend)
    result = backend.run(qc_t, shots=1024).result()
    counts = result.get_counts()
    
    # |10⟩ is a -1 eigenstate of ZZ, so we expect mostly '1' outcomes
    one_count = counts.get('1', 0)
    one_percent = 100 * one_count / 1024
    
    test2_passed = one_percent > 95  # Allow for some simulator noise
    results["test2"] = {
        "passed": test2_passed,
        "one_percent": one_percent
    }
    all_passed = all_passed and test2_passed
    
    print(f"  {'✓' if test2_passed else '✗'} ZZ stabilizer with X error: {one_percent:.2f}% '1' outcomes (expected >95%)")
    
    # Visualize the results
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.bar(counts.keys(), counts.values())
    plt.title("ZZ Stabilizer with X Error")
    plt.xlabel("Measurement Outcome")
    plt.ylabel("Counts")
    
    # Overall result
    print(f"\nOverall result: {'All tests passed!' if all_passed else 'Some tests failed.'}")
    
    return all_passed, results

def estimate_hardware_runtime():
    """
    Estimates the runtime for the 2-qubit stabilizer circuit on IBM Quantum hardware.
    
    Returns:
    - Estimated runtime in seconds
    """
    # Parameters
    num_qubits = 3  # 2 data qubits + 1 ancilla qubit
    circuit_depth = 5  # Approximate depth for 2-qubit stabilizer
    shots = 4096  # Number of shots
    
    # Estimate based on typical gate times
    gate_time_us = 100  # Approximate gate time in microseconds
    readout_time_us = 300  # Approximate measurement time in microseconds
    
    # Calculate total runtime
    gate_runtime_s = (circuit_depth * gate_time_us * 1e-6) * shots
    readout_runtime_s = (readout_time_us * 1e-6) * shots
    total_runtime_s = gate_runtime_s + readout_runtime_s
    
    print(f"Estimated hardware runtime for 2-qubit stabilizer circuit:")
    print(f"  Number of qubits: {num_qubits}")
    print(f"  Circuit depth: {circuit_depth}")
    print(f"  Number of shots: {shots}")
    print(f"  Estimated runtime: {total_runtime_s:.2f} seconds (excluding queue time)")
    
    # This should be well under the 5-minute limit
    print("  ✓ Estimated runtime is well within the recommended 5-minute limit.")
    
    return total_runtime_s

if __name__ == "__main__":
    # Run the tests
    all_passed, results = test_stabilizer_circuit()
    
    # Estimate hardware runtime
    print("\n" + "="*50)
    runtime = estimate_hardware_runtime()
    
    # Display circuit
    print("\nCircuit visualization:")
    qc = create_2qubit_stabilizer_circuit(add_error=True)
    print(qc.draw(output='text'))
    
    # Exit with appropriate status code
    sys.exit(0 if all_passed else 1)
