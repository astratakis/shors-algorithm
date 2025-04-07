from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.providers.aer import AerSimulator

from quantum_fourier_transform import qft, qft_dagger

import matplotlib.pyplot as plt

class Shor:
    def __init__(self, number_to_factor, backend="some_default_backend"):
        self.number_to_factor = number_to_factor
        self.backend = backend
        # Any other initialization needed
    
    def factor(self):
        """
        Implement Shor's algorithm here.
        """
        # Implementation details
        return NotImplemented  # placeholder


from numpy import pi
from math import gcd
from fractions import Fraction

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

def cc_modular_adder(a: int, n: int, N: int) -> QuantumCircuit:
    
    circuit = QuantumCircuit(n+4)
    
    circuit.append(fourier_adder(a, n+1).control(num_ctrl_qubits=2).decompose(), [0, 1] + [i+2 for i in range(n+1)])
    circuit.append(fourier_subtractor(N, n+1), [i+2 for i in range(n+1)])
    circuit.append(qft_dagger(n+1), [i+2 for i in range(n+1)])
    circuit.cx(n+2, n+3)
    circuit.append(qft(n+1), [i+2 for i in range(n+1)])
    circuit.append(fourier_adder(N, n+1).control(num_ctrl_qubits=1).decompose(), [n+3] + [i+2 for i in range(n+1)])
    circuit.append(fourier_subtractor(a, n+1).control(num_ctrl_qubits=2).decompose(), [0, 1] + [i+2 for i in range(n+1)])
    circuit.append(qft_dagger(n+1), [i+2 for i in range(n+1)])
    circuit.x(n+2)
    circuit.cx(n+2, n+3)
    circuit.x(n+2)
    circuit.append(qft(n+1), [i+2 for i in range(n+1)])
    circuit.append(fourier_adder(a, n+1).control(num_ctrl_qubits=2).decompose(), [0, 1] + [i+2 for i in range(n+1)])
    return circuit

def cc_modular_subtractor(a: int, n: int, N: int) -> QuantumCircuit:
    return cc_modular_adder(a, n, N).inverse()

def c_modular_multiplier(a: int, n: int, N: int) -> QuantumCircuit:
    
    circuit = QuantumCircuit(2*n + 3)

    circuit.append(qft(n+1), [1+n+i for i in range(n+1)])
    for i in range(n):
        circuit.append(cc_modular_adder((a * (1 << i)) % N, n, N).decompose(), [0, i+1] + [n+1+j for j in range(n+2)])

    circuit.append(qft_dagger(n+1), [1+n+i for i in range(n+1)])

    return circuit

def n_swap(n: int) -> QuantumCircuit:
    circuit = QuantumCircuit(n)

    for i in range(n >> 1):
        circuit.swap(i, i + (n >> 1))

    return circuit

def conditional_oracle(a: int, inv_a: int, n: int, N: int) -> QuantumCircuit:
    
    circuit = QuantumCircuit(2*n + 3)

    circuit.append(c_modular_multiplier(a, n, N).decompose(), range(2*n + 3))
    circuit.append(n_swap(2*n).control(num_ctrl_qubits=1).decompose(), [0] + [i+1 for i in range(2*n)])
    circuit.append(c_modular_multiplier(inv_a, n, N).inverse().decompose(), range(2*n + 3))
    
    return circuit

def shor_circuit(N: int, a: int) -> QuantumCircuit:
    n = len(bin(N)[2:])

    circuit = QuantumCircuit(4*n + 2)
    result = ClassicalRegister(2*n, name="result")
    #remainder = ClassicalRegister(n+1, name="remainder")
    #flag = ClassicalRegister(1, name="flag")

    circuit.add_register(result)

    for i in range(2*n):
        circuit.h(i)
    circuit.x(2*n)

    for i in range(2*n):
        alpha = (a**(1 << i)) % N
        inv_alpha = calculate_inverse_mod_n(alpha, N)
        circuit.append(conditional_oracle(alpha, inv_alpha, n, N).decompose(), [i] + [2*n+i for i in range(2*n+2)])

    circuit.append(qft_dagger(2*n), range(2*n))

    circuit.barrier()
    circuit.measure(range(2*n), result)

    return circuit

def plot_shor_circuit(N: int, a: int):
    n = len(bin(N)[2:])

    couting_registers = QuantumRegister(2*n, name="cnt")
    aux_registers = QuantumRegister(2*n+2, name="aux")
    result = ClassicalRegister(2*n, name="res")

    circuit = QuantumCircuit(couting_registers, aux_registers, result)

    for i in range(2*n):
        circuit.h(i)
    circuit.x(2*n)

    for i in range(2*n):
        U = QuantumCircuit(2*n+2)

        gate = U.to_gate(label=r'$%i^{%i}$ mod N' %(a, 1 << i))
        gate = gate.control()

        circuit.append(gate, [i] + [2*n+i for i in range(2*n+2)])
    
    qft = QuantumCircuit(2*n)

    circuit.append(qft.to_gate(label=r'QFT$\dagger$'), range(2*n))

    circuit.measure(range(2*n), result)

    figure = circuit.draw('mpl', fold=-1)
    name = "images/shor_circuit_" + str(N) + "_" + str(a)
    figure.savefig(name, dpi=600)



def calculate_inverse_mod_n(alpha: int, N: int) -> int:
    if alpha == 0:
        return 0

    num = 1

    while True:

        if (alpha * num) % N == 1:
            return num
        num += 1

if __name__ == "__main__":
    # ----------- <VARIABLES> ----------- #
    N = 15
    n = len(bin(N)[2:])
    a = 2
    # ----------------------------------- #

    #plot_shor_circuit(N, a)

    qc = shor_circuit(N, a)
    print(qc)

    if 'GPU' in AerSimulator().available_devices():
        simulator = AerSimulator(provider='unitary_gpu')
        simulator.set_options(device='GPU')
        result = simulator.run(qc.decompose(), memory=True, shots=20000).result()
    else:
        print('[FAILED] to run simulation on GPU... Trying again on CPU...')
        simulator = AerSimulator(provider='unitary')
        simulator.set_options(device='CPU')
        result = simulator.run(qc.decompose(), memory=True, shots=20000).result()

    memory = result.get_memory()
    memory.sort()

    counts = result.get_counts()

    memory_int = []

    for element in memory:
        memory_int.append(int(element, 2))


    r_guesses = []

    r_counts = {}

    for element in memory:
        phase = int(element, 2) / (1 << (2*n))
        fr = Fraction(phase).limit_denominator(N)
        r_guesses.append(fr.denominator)

        if not (fr.denominator in r_counts.keys()):
            r_counts[fr.denominator] = 1
        else:
            r_counts[fr.denominator] += 1

    best_r_guess = -1
    max = 0

    for key in r_counts.keys():
        if r_counts.get(key) > max:
            best_r_guess = key
            max = r_counts.get(key)


    #plt.figure(facecolor='white')
    #plt.hist(memory_int, bins=500)
    #plt.show()

    #plt.figure(facecolor='white')
    #plt.hist(r_guesses, bins=500)
    #plt.show()

    print('Best guess for r:', best_r_guess)

    # Then make sure that r is even
    if best_r_guess % 2 == 1:
        print('Invalid result: r is not even')
        exit(1)

    p = a**(best_r_guess >> 1) + 1
    q = a**(best_r_guess >> 1) - 1

    p = gcd(p, N)
    q = gcd(q, N)

    if p == 1 or q == 1:
        print('Bad guess, try again...')
        exit(1)

    print("Factors: %i = %i * %i" %(N, p, q))

    file = open("data.txt", "w")
    for key in result.get_counts():
        file.write(str(int(key, 2)) + " " + str(result.get_counts().get(key)) + "\n")
    file.close()

    hash_set = set()
    max = 0

    counts = result.get_counts()

    modified_file = open("modified.txt", "w")
    for key in counts:
        number = int(key, 2)
        hash_set.add(number)
        if number > max:
            max = number

        modified_file.write(str(number) + ";" + str(counts.get(key)) + "\n")
    
    for i in range(max):
        if i not in hash_set:
            modified_file.write(str(i) + ";" + "0\n")
    modified_file.close()





    
