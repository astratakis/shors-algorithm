from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
from numpy import pi

from qiskit.visualization import *


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
    n = 3
    init_state = 4
    # ----------------------------------- #

    qc = QuantumCircuit(n)

    binary = bin(init_state)[2:][::-1]

    for i in range(len(binary)):
        if binary[i] == '1':
           qc.x(i)


    qc.append(qft(n).decompose(), range(n))
    
    print(qc)

    simulator = AerSimulator()
    simulator.set_options(device='GPU')
    result = simulator.run(qc, memory=True, shots=1).result()

    figure = plot_state_qsphere(qc)
    figure.savefig("figure_qft_" + str(n) + "_" + str(init_state), dpi=1000)

    bloch = plot_bloch_multivector(qc)
    bloch.savefig("multivector_qft_" + str(n) + "_" + str(init_state), dpi=1000)
    