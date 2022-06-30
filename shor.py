from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np
from math import gcd

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

    qc.name = "SUB(a)"

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

    qc.name = "ADDER(a)"

    return qc

def adder(a: int, n: int) -> QuantumCircuit:
    circuit = QuantumCircuit(n+1)
    fourier_gate = fourier_adder(a, n+1).to_gate(label="F_add(%i)" % a)
    circuit.append(fourier_gate, range(n+1))
    return circuit

def c_adder(a: int, n: int) -> QuantumCircuit:
    circuit = QuantumCircuit(n+1)
    fourier_gate = fourier_adder(a, n+1).to_gate(label="F_add(%i)" % a)
    circuit.append(fourier_gate, range(n+1))
    circuit = circuit.control(1)
    return circuit

def cc_adder(a: int, n: int) -> QuantumCircuit:
    circuit = QuantumCircuit(n+1)
    fourier_gate = fourier_adder(a, n+1).to_gate(label="F_add(%i)" % a)
    circuit.append(fourier_gate, range(n+1))
    circuit = circuit.control(2)
    return circuit

def adder_dagger(a: int, n: int) -> QuantumCircuit:
    circuit = QuantumCircuit(n+1)
    fourier_gate = fourier_subtractor(a, n+1).to_gate(label="F_sub(%i)" % a)
    circuit.append(fourier_gate, range(n+1))
    return circuit

def c_adder_dagger(a: int, n: int) -> QuantumCircuit:
    circuit = QuantumCircuit(n+1)
    fourier_gate = fourier_subtractor(a, n+1).to_gate(label="F_sub(%i)" % a)
    circuit.append(fourier_gate, range(n+1))
    circuit = circuit.control(1)
    return circuit

def cc_adder_dagger(a: int, n: int) -> QuantumCircuit:
    circuit = QuantumCircuit(n+1)
    fourier_gate = fourier_subtractor(a, n+1).to_gate(label="F_sub(%i)" % a)
    circuit.append(fourier_gate, range(n+1))
    circuit = circuit.control(2)
    return circuit

def cc_mod_adder(a: int, n: int, N: int) -> QuantumCircuit:

    control_registers = QuantumRegister(2, name="c")
    counting_registers = QuantumRegister(n+1, name="q")
    flag_register = QuantumRegister(1, name="flag")

    circuit = QuantumCircuit(control_registers, counting_registers, flag_register)

    cc_adder_gate = cc_adder(a, n).to_gate(label="cc_F_add(%i)" %a)
    circuit.append(cc_adder_gate, [0, 1] + [i+2 for i in range(n+1)])

    sub_gate = adder_dagger(N, n).to_gate(label="F_sub(%i)" %N)
    circuit.append(sub_gate, range(2, n+3))

    qft_dagger_gate = qft_dagger(n+1).to_gate(label="QFT†")
    circuit.append(qft_dagger_gate, range(2, n+3))

    circuit.cx(n+2, n+3)

    qft_gate = qft(n+1).to_gate(label="QFT")
    circuit.append(qft_gate, range(2, n+3))

    c_adder_gate = c_adder(N, n).to_gate(label="c_F_add(%i)" %N)
    circuit.append(c_adder_gate, [n+3] + [i+2 for i in range(n+1)])

    cc_sub_gate = cc_adder_dagger(a, n).to_gate(label="cc_F_sub(%i)" %a)
    circuit.append(cc_sub_gate, [0, 1] + [i+2 for i in range(n+1)])

    circuit.append(qft_dagger_gate, range(2, n+3))
    
    circuit.x(n+2)
    circuit.cx(n+2, n+3)
    circuit.x(n+2)

    circuit.append(qft_gate, range(2, n+3))

    circuit.append(cc_adder_gate, [0, 1] + [i+2 for i in range(n+1)])

    return circuit

def cc_mod_adder_dagger(inv_a: int, n: int, N: int) -> QuantumCircuit:
    
    circuit = cc_mod_adder(inv_a, n, N).inverse()
    return circuit

def c_modular_multiplier(a: int, n: int, N: int) -> QuantumCircuit:

    circuit = QuantumCircuit(3 + 2 * n)
    
    qft_gate = qft(n+1).to_gate(label="QFT")
    qft_dagger_gate = qft_dagger(n+1).to_gate(label="QFT†")

    circuit.append(qft_gate, range(1+n, 2+2*n))

    for i in range(n):

        modular_adder_gate = cc_mod_adder(((1 << i) * a) % N, n, N).to_gate(label="mod_adder")
        circuit.append(modular_adder_gate, [0, i+1] + [1+n+i for i in range(n+2)])

    circuit.append(qft_dagger_gate, range(1+n, 2+2*n))

    return circuit

def c_modular_multiplier_inverse(inv_a: int, n: int, N: int) -> QuantumCircuit:
    
    circuit = c_modular_multiplier(inv_a, n, N).inverse()
    return circuit

def swap_n(length: int) -> QuantumCircuit:
    circuit = QuantumCircuit(length)

    for i in range(length >> 1):
        circuit.swap(i, i + (length >> 1))

    return circuit

def c_U(a: int, inv_a: int, n: int, N: int) -> QuantumCircuit:
    
    x_register = QuantumRegister(n, name="x")
    control_register = QuantumRegister(1, name="c")
    b_register = QuantumRegister(n+2, name="b")

    circuit = QuantumCircuit(control_register, x_register, b_register)

    c_modular_multiplier_gate = c_modular_multiplier(a, n, N).to_gate(label="mult a")
    circuit.append(c_modular_multiplier_gate, [0] + [i+1 for i in range(2*n+2)])

    swap_circuit = swap_n(2*n)
    c_swap_circuit = swap_circuit.control(1)
    c_swap_gate = c_swap_circuit.to_gate(label="C_SWAP")

    circuit.append(c_swap_gate, [0] + [i+1 for i in range(2*n)])

    c_modular_multiplier_inverse_gate = c_modular_multiplier_inverse(inv_a, n, N).to_gate(label="inv mult a")
    circuit.append(c_modular_multiplier_inverse_gate, [0] + [i+1 for i in range(2*n+2)])

    return circuit

def calculate_inverse_mod_n(alpha: int, N: int) -> int:
    if alpha == 0:
        return 0

    num = 1

    while True:

        if (alpha * num) % N == 1:
            return num
        num += 1

def shor_circuit(N: int, a: int) -> QuantumCircuit:
    n = len(bin(N)[2:])

    coutning_register = QuantumRegister(2 * n, name="q")
    psi = QuantumRegister(n, name="y")
    aux = QuantumRegister(n+1, name="aux")
    flag = QuantumRegister(1, name="flag")

    result = ClassicalRegister(2*n, name="result")
    #final_psi = ClassicalRegister(n, name="final_psi")
    #aux_result = ClassicalRegister(n+1, name="aux_output")
    #flag_output = ClassicalRegister(1, name="carry")

    circuit = QuantumCircuit(coutning_register, psi, aux, flag, result)

    for i in range(2*n):
        circuit.h(i)

    circuit.x(2*n)

    for i in range(2*n):
        alpha = (a**(1 << i)) % N
        if gcd(alpha, N) != 1:
            print('ERROR')
            exit(1)
        inv_a = calculate_inverse_mod_n(alpha, N)
        gate = c_U(alpha, inv_a, n, N).to_gate(label="U(a^%i)" %(1 << i))
        circuit.append(gate, [i] + [2*n+i for i in range(2*n+2)])

    circuit.append(qft_dagger(2*n), range(2*n))

    circuit.barrier()

    circuit.measure(range(2*n), range(2*n))
    #circuit.measure(psi, final_psi)
    #circuit.measure(aux, aux_result)
    #circuit.measure(flag, flag_output)

    return circuit

def fast_shor_circuit(N: int, a: int) -> QuantumCircuit:
    n = len(bin(N)[2:])

    counting_register = QuantumRegister(1, name="q")
    psi = QuantumRegister(n, name="psi")
    aux = QuantumRegister(n+1, name="aux")
    flag = QuantumRegister(1, name="flag")

    result = ClassicalRegister(2*n, name="result")

    circuit = QuantumCircuit(counting_register, psi, aux, flag, result)

    # measure
    for i in range(2*n):
        circuit.h(0)
        alpha = (a**(1 << i)) % N
        if gcd(alpha, N) != 1:
            print('ERROR')
            exit(1)
        inv_a = calculate_inverse_mod_n(alpha, N)
        gate = c_U(alpha, inv_a, n, N).to_gate(label="U(a^%i)" %(1 << i))
        circuit.append(gate, [0] + [1+i for i in range(2*n+2)])

        if i == 0:
            circuit.h(0)
        else:
            circuit.h(0)


        circuit.measure([0], [i])

        circuit.x(0).c_if(result[i], 1)

    return circuit
