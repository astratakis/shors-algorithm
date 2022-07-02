from qiskit import QuantumCircuit
from numpy import pi

from qiskit.providers.aer import AerSimulator

from quantum_fourier_transform import qft, qft_dagger

def theta(index: int) -> float:
    return 2 * pi / (2**index)

def fourier_adder(a: int, n: int) -> QuantumCircuit:
    '''
    This creates a circuit that adds a + b in the fourier computational plain.
    The input that will be attached to the circuit is supposed to be a number b
    in the Fourier domain.
    '''
    qc = QuantumCircuit(n)

    number = a
    index = 0
    binary = [0] * n

    for i in range(n):
        if (number & 1) == 1:
            binary[index] = 1
        index += 1
        number = number >> 1

    binary.reverse()
    #print(binary)

    for i in range(n):
        index = 1
        sum = 0.0
        for j in range(i, n):
            if binary[j] == 1:
                sum += theta(index)
            index += 1
        qc.p(sum, i)

    qc.name = "ADDER(a)"

    return qc

def fourier_subtractor(a: int, n: int) -> QuantumCircuit:
    return fourier_adder(a, n).inverse()

def adder(a: int, n: int) -> QuantumCircuit:
    circuit = QuantumCircuit(n+1)
    circuit.append(fourier_adder(a, n+1), range(n+1))
    return circuit

if __name__ == "__main__":
    # ----------- <VARIABLES> ----------- #
    N = 15
    n = len(bin(N)[2:])
    # ----------------------------------- #

    qc = QuantumCircuit(n, )
    qc = adder(2, n)
    qc.measure_all()

    print(qc)

    simulator = AerSimulator()
    simulator.set_options(device='GPU')
    result = simulator.run(qc, memory=True, shots=1).result()

    memory = result.get_memory()

    print(memory)