from qiskit import *
import numpy as np
import matplotlib.pyplot as plt

import os

os.system('color')

from qiskit.providers.aer import QasmSimulator

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def qft_rotations(circuit, n):
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

def qft(n) -> QuantumCircuit:
    qc = QuantumCircuit(n)

    qft_rotations(qc, n)

    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)

    qc.name = "QFT"

    return qc

def qft_dagger(n) -> QuantumCircuit:
    """n-qubit QFTdagger the first n qubits in circ"""
    qc = QuantumCircuit(n)
    # Don't forget the Swaps!
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"

    return qc

def theta(index: int) -> float:
    return 2 * np.pi / (2**index)

def fourier_subtractor(a: int, n: int) -> QuantumCircuit:
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
                sum -= theta(index)
            index += 1
        qc.p(sum, i)

    qc.name = "SUB(" + str(a) + ")"

    return qc

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

    qc.name = "ADDER(" + str(a) + ")"

    return qc

def cc_fourier_adder(a: int, n: int) -> QuantumCircuit:
    qc = fourier_adder(a, n)
    qc.control(2)
    return qc

def fourier_add_mod(N: int, n: int, a: int) -> QuantumCircuit:
    carry_register = QuantumRegister(1, name="q_carry")
    classical_register = ClassicalRegister(n, name="result")
    cout = ClassicalRegister(1, name="carry")

    circuit = QuantumCircuit(n+1)
    circuit.add_register(carry_register)
    circuit.add_register(classical_register)
    circuit.add_register(cout)

    circuit.append(fourier_adder(a, n+1), range(n+1))
    circuit.append(fourier_subtractor(N, n+1), range(n+1))

    circuit.append(qft_dagger(n+1), range(n+1))

    circuit.cx(n, n+1)

    circuit.measure(n+1, cout[0])
    circuit.reset(n+1)

    circuit.append(qft(n+1), range(n+1)).c_if(cout, 1)
    circuit.append(fourier_adder(N, n+1), range(n+1)).c_if(cout, 1)
    circuit.append(qft_dagger(n+1), range(n+1)).c_if(cout, 1)
    return circuit


if __name__ == "__main__":
    n = 4

    for N in range(1 << (n-1), 1 << n):
        
        for i in range(N):
            init_number = i

            for j in range(N):
                a = j

                carry_register = QuantumRegister(1, name="q_carry")
                classical_register = ClassicalRegister(n, name="result")
                cout = ClassicalRegister(1, name="carry")

                circuit = QuantumCircuit(n+1)
                circuit.add_register(carry_register)
                circuit.add_register(classical_register)
                circuit.add_register(cout)

                # Create a number and change into Fourier domain...

                binary = bin(init_number)[2:]
            
                for k in range(len(binary)):
                    if binary[::-1][k] == '1':
                        circuit.x(k)

                circuit.barrier()

                circuit.append(qft(n+1), range(n+1))
                circuit.append(fourier_adder(a, n+1), range(n+1))

                circuit.append(fourier_subtractor(N, n+1), range(n+1))

                circuit.append(qft_dagger(n+1), range(n+1))

                circuit.cx(n, n+1)

                circuit.measure(n+1, cout[0])

                circuit.append(qft(n+1), range(n+1)).c_if(cout, 1)
                circuit.append(fourier_adder(N, n+1), range(n+1)).c_if(cout, 1)
                circuit.append(qft_dagger(n+1), range(n+1)).c_if(cout, 1)

                circuit.measure(range(n), range(n))

                #circuit.measure(n, cout[0])

                backend = QasmSimulator()
                backend_options = {'method': 'simulator'}
                job = execute(circuit, backend, backend_options=backend_options, shots=20000)
                job_result = job.result()

                counts = job_result.get_counts(circuit)

                bin_value = list(counts.keys())[0]

                elements = bin_value.split(' ')
                
                binary_value = elements[1]
                value = int(binary_value, 2)

                print(str(init_number) + ' + ' + str(a) + ' % ' + str(N) + ' = ' + str(value), end="\t")
            
                if (value != (init_number + a) % N):
                    print(bcolors.BOLD + bcolors.FAIL + "***ERROR***" + bcolors.ENDC)
                    print(circuit)
                    
                    exit(1)
                else:
                    print(bcolors.BOLD + bcolors.OKGREEN + "Passed!" + bcolors.ENDC)