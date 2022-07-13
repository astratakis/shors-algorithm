from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
from numpy import pi

from qiskit.visualization import *

import matplotlib.pyplot as plt


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
    n = 5
    init_state = 0
    # ----------------------------------- #

    qft_circuit = qft(n)
    qft_circuit.draw('mpl', fold=-1).savefig("example_qft_" + str(n), dpi=400)

    qc = QuantumCircuit(n)

    binary = bin(init_state)[2:][::-1]

    for i in range(len(binary)):
        if binary[i] == '1':
           qc.x(i)

    qc.append(qft(n).decompose(), range(n))
    qc = qc.decompose()

    qc.save_statevector()

    simulator = AerSimulator()
    simulator.set_options(device='CPU')
    result = simulator.run(qc.decompose(), memory=True, shots=1).result()

    #figure = plot_state_qsphere(qc)
    #figure.savefig("figure_qft_" + str(n) + "_" + str(init_state), dpi=200)

    #bloch = plot_bloch_multivector(qc)
    #bloch.savefig("multivector_qft_" + str(n) + "_" + str(init_state), dpi=200)

    sv = result.get_statevector(qc)

    print(sv)

    array = []

    for i in range(len(sv)):
        element = sv[i]
        array.append((i, pow(element, 2).real))
    print(array)

    
    plt.figure(facecolor='white')
    plt.hist(array)
    plt.show()
