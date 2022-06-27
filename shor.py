from msilib.schema import Class
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
import numpy as np

def qft_dagger(n: int) -> QuantumCircuit:
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

def c_amodN(y: int, target: int, n: int, a: int, N: int, power: int) -> QuantumCircuit:
    U = QuantumCircuit(n)

    # UNSAFE...
    # THIS WILL OVERFLOW WHEN N IS REALLY BIG.
    # TODO REPLACE THIS WITH ARRAYS OF BINARY STRINGS.
    mask = 1
    for i in range(n):
        if ((y & mask) != (target & mask)):
            U.x(i)
        mask = mask << 1

    U.name = "%i^%i mod %i" % (a, power, N)

    return U

def Shor(N: int, a: int) -> QuantumCircuit:
    n = len(bin(N)[2:])

    # Create a list of size n (log2(N)) of quantum registers.
    counting_registers = [QuantumRegister(1, name="q" + str(i)) for i in range(n)]
    unitary_function_registers = [QuantumRegister(1, name="u" + str(i)) for i in range(n)]
    classical_resiter = ClassicalRegister(n, name="bits")
    #final_Y_state = ClassicalRegister(n, name="y_state")

    qc = QuantumCircuit(classical_resiter)
    
    # Initialize the circuit by creating all the neccessary registers.
    for register in counting_registers:
        qc.add_register(register)
    for register in unitary_function_registers:
        qc.add_register(register)

    # Apply Hadamard gates to the counting qubits in order to create a superposition.
    for i in range(n):
        qc.h(i)

    # Generate state |1> (little endian representation) using only secondary qubits
    qc.x(n)

    # Initial auxillery state is |1>
    Y = 1
    prev_a = a

    for i in range(n):
        target = prev_a * Y % N
        mod_gate = c_amodN(Y, target, n, a, N, 1 << i).to_gate()
        Y = target
        prev_a = (prev_a * prev_a) % N

        c_m = mod_gate.control()

        qc.append(c_m, [i] + [n + i for i in range(n)])

    inverse_qft_gate = qft_dagger(n).to_gate()
    qc.append(inverse_qft_gate, range(n))

    qc.barrier()
    qc.measure(range(n), range(n))
    return qc