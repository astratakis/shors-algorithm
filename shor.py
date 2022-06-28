from qiskit import QuantumCircuit
from numpy import pi

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

    print(binary)

    return qc

fourier_adder(5, 99)