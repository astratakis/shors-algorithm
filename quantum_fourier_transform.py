from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
from numpy import pi


def qft_rotations(circuit: QuantumCircuit, n: int):
    """Performs qft on the first n qubits in circuit (without swaps)"""
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi/2**(n-qubit), qubit, n)
    # At the end of our function, we call the same function again on
    # the next qubits (we reduced n by one earlier in the function)
    qft_rotations(circuit, n)


def qft(n: int) -> QuantumCircuit:
    circuit = QuantumCircuit(n)
    qft_rotations(circuit, n)
    for i in range(n // 2):
        circuit.swap(i, n-i-1)
    return circuit



def qft_dagger(n: int) -> QuantumCircuit:
    return qft(n).inverse()
    
# Driver code...
if __name__ == "__main__":

    # ----------- <VARIABLES> ----------- #
    N = 15
    n = len(bin(N)[2:])
    # ----------------------------------- #

    qc = qft(n)
    qc.measure_all()

    simulator = AerSimulator()
    simulator.set_options(device='GPU')
    result = simulator.run(qc, memory=True, shots=1).result()

    memory = result.get_memory()

    print(memory)
    