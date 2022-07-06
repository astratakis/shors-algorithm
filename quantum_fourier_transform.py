from cProfile import label
from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator
import numpy as np

import matplotlib.pyplot as plt

from math import sin, cos, pow, sqrt

def qft_rotations(circuit: QuantumCircuit, n: int):
    """Performs qft on the first n qubits in circuit (without swaps)"""
    if n == 0:
        return circuit
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(np.pi/2**(n-qubit), qubit, n)
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

    t = np.linspace(0, 2 * np.pi, 1000)

    n = 3
    N = 1 << n

    re_0 = [1/sqrt(N) * cos(x) for x in t]
    im_0 = [1/sqrt(N) * sin(x) for x in t]
    amplitude_0 = [pow(re_0[index], 2) + pow(im_0[index], 2) for index in range(len(t))]

    plt.figure(facecolor='white')
    plt.plot(t, re_0, label=r'Real: $\cos(\phi)$')
    plt.plot(t, im_0, label=r'Imaginary: $\sin(\phi)$')
    plt.plot(t, amplitude_0, label=r'Amplitude: $\cos^{2}(\phi)$ + $\sin^{2}(\phi)$')
    plt.xlabel(r'Phase $\phi$')
    plt.legend()
    plt.show()

    re_1 = [cos(2*x) for x in t]
    im_1 = [sin(2*x) for x in t]
    amplitude_1 = [cos(2*x) * cos(2*x) + sin(2*x) * sin(2*x) for x in t]

    plt.figure(facecolor='white')
    plt.plot(t, re_1, label=r'Real: $\cos(2\phi)$')
    plt.plot(t, im_1, label=r'Imaginary: $\sin(2\phi)$')
    plt.plot(t, amplitude_1, label=r'Amplitude: $\cos^{2}(2\phi)$ + $\sin^{2}(2\phi)$')
    plt.xlabel(r'Phase $\phi$')
    plt.legend()
    plt.show()

    sum_re = [cos(2*x) + cos(x) for x in t]
    sum_im = [sin(2*x) + sin(x) for x in t]
    sum_amp = [pow(sum_re[index], 2) + pow(sum_im[index], 2) for index in range(len(t))]

    plt.figure(facecolor='white')
    plt.plot(t, sum_re, label=r'Real: $\cos(2\phi)$')
    plt.plot(t, sum_im, label=r'Imaginary: $\sin(2\phi)$')
    plt.plot(t, sum_amp, label=r'Amplitude: $\cos^{2}(2\phi)$ + $\sin^{2}(2\phi)$')
    plt.xlabel(r'Phase $\phi$')
    plt.legend()
    plt.show()
