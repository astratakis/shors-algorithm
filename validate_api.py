from qiskit import ClassicalRegister, QuantumCircuit, execute
from qiskit.providers.aer import QasmSimulator
from math import gcd

from qiskit.providers.aer import Aer

import matplotlib.pyplot as plt

from shor import adder, adder_dagger, c_U, c_modular_multiplier, cc_mod_adder, cc_mod_adder_dagger, fast_shor_circuit, qft, qft_dagger, shor_circuit

import os, time
os.system('color')

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

n = 4

def test_adder() -> bool:
    for initial_number in range(1 << n):
        for alpha in range(1 << n):
        
            test_circuit = QuantumCircuit(n+1, n+1)
            binary = bin(initial_number)[2:]
        
            # Prepare the initial number encoded into x gates in the beggining...
            for k in range(len(binary)):
                if binary[::-1][k] == '1':
                    test_circuit.x(k)

            test_circuit.barrier()
            test_circuit.append(qft(n+1), range(n+1))

            # This is the test circuit
            test_circuit.append(adder(alpha, n), range(n+1))
            test_circuit.append(qft_dagger(n+1), range(n+1))

            test_circuit.measure(range(n+1), range(n+1))

            backend = QasmSimulator()
            backend_options = {'method': 'simulator'}
            job = execute(test_circuit, backend, backend_options=backend_options, shots=20000)
            job_result = job.result()

            counts = job_result.get_counts(test_circuit)

            bin_value = list(counts.keys())[0]
            value = int(bin_value, 2)

            if not assertEqual(len(list(counts.keys())), 1):
                return False
            if not assertEqual(value, initial_number + alpha):
                return False
    return True

def test_adder_dagger() -> bool:
    for initial_number in range(1 << n):
        for alpha in range(1 << n):
        
            test_circuit = QuantumCircuit(n+1, n+1)
            binary = bin(initial_number)[2:]
        
            # Prepare the initial number encoded into x gates in the beggining...
            for k in range(len(binary)):
                if binary[::-1][k] == '1':
                    test_circuit.x(k)

            test_circuit.barrier()
            test_circuit.append(qft(n+1), range(n+1))

            # This is the test circuit
            test_circuit.append(adder_dagger(alpha, n), range(n+1))
            test_circuit.append(qft_dagger(n+1), range(n+1))

            test_circuit.measure(range(n+1), range(n+1))

            backend = QasmSimulator()
            backend_options = {'method': 'simulator'}
            job = execute(test_circuit, backend, backend_options=backend_options, shots=20000)
            job_result = job.result()

            counts = job_result.get_counts(test_circuit)

            bin_value = list(counts.keys())[0]
            value = int(bin_value, 2)

            if not assertEqual(len(list(counts.keys())), 1):
                return False
            
            if initial_number >= alpha:
                if not assertEqual(value, initial_number - alpha):
                    return False
            else:
                if not assertEqual(value, (1 << (n + 1)) - (alpha - initial_number)):
                    return False

    return True

def test_cc_mod_adder():

    for N in range(1 << (n-1), 1 << n):
        for initial_number in range(N):
            for alpha in range(N):

                controls = ClassicalRegister(2, name="ctrl")
                result = ClassicalRegister(n+1, name="result")
                flag = ClassicalRegister(1, name="flag")

                test_circuit = QuantumCircuit(n+4)
                test_circuit.add_register(controls)
                test_circuit.add_register(result)
                test_circuit.add_register(flag)
                test_circuit.x([0, 1])

                binary = bin(initial_number)[2:]
            
                # Prepare the initial number encoded into x gates in the beggining...
                for k in range(len(binary)):
                    if binary[::-1][k] == '1':
                        test_circuit.x(k+2)

                test_circuit.barrier()
                test_circuit.append(qft(n+1), range(2, n+3))

                cc_mod_adder_gate = cc_mod_adder(alpha, n, N).to_gate(label="cc_mod_add()")
                test_circuit.append(cc_mod_adder_gate, [0, 1] + [i+2 for i in range(n+2)])

                test_circuit.append(qft_dagger(n+1), range(2, n+3))

                test_circuit.measure([0, 1], controls)
                test_circuit.measure(range(2, n+3), result)
                test_circuit.measure([n+3], flag)

                backend = QasmSimulator()
                backend_options = {'method': 'simulator'}
                job = execute(test_circuit, backend, backend_options=backend_options, shots=20000)
                job_result = job.result()

                counts = job_result.get_counts(test_circuit)

                if not assertEqual(len(list(counts.keys())), 1):
                    return False

                bin_value = list(counts.keys())[0]
                elements = bin_value.split(' ')

                if not assertEqual(elements[0], '0'):
                    return False

                if not assertEqual(elements[2], '11'):
                    return False

                value = int(elements[1], 2)

                if not assertEqual(value, (initial_number + alpha) % N):
                    return False
    return True

def test_cc_mod_adder_dagger():
    for N in range(1 << (n-1), 1 << n):
        for initial_number in range(N):
            for alpha in range(N):

                controls = ClassicalRegister(2, name="ctrl")
                result = ClassicalRegister(n+1, name="result")
                flag = ClassicalRegister(1, name="flag")

                test_circuit = QuantumCircuit(n+4)
                test_circuit.add_register(controls)
                test_circuit.add_register(result)
                test_circuit.add_register(flag)
                test_circuit.x([0, 1])

                binary = bin(initial_number)[2:]
            
                # Prepare the initial number encoded into x gates in the beggining...
                for k in range(len(binary)):
                    if binary[::-1][k] == '1':
                        test_circuit.x(k+2)

                test_circuit.barrier()
                test_circuit.append(qft(n+1), range(2, n+3))

                cc_mod_adder_dagger_gate = cc_mod_adder_dagger(alpha, n, N).to_gate(label="cc_mod_add()")
                test_circuit.append(cc_mod_adder_dagger_gate, [0, 1] + [i+2 for i in range(n+2)])

                test_circuit.append(qft_dagger(n+1), range(2, n+3))

                test_circuit.measure([0, 1], controls)
                test_circuit.measure(range(2, n+3), result)
                test_circuit.measure([n+3], flag)

                backend = QasmSimulator()
                backend_options = {'method': 'simulator'}
                job = execute(test_circuit, backend, backend_options=backend_options, shots=20000)
                job_result = job.result()

                counts = job_result.get_counts(test_circuit)

                if not assertEqual(len(list(counts.keys())), 1):
                    return False

                bin_value = list(counts.keys())[0]
                elements = bin_value.split(' ')

                if not assertEqual(elements[0], '0'):
                    return False

                if not assertEqual(elements[2], '11'):
                    return False

                value = int(elements[1], 2)

                if not assertEqual(value, (initial_number - alpha) % N):
                    return False
    return True

def test_mult():

    for N in range(1 << (n-1), 1 << n):
        for initial_number in range(N):
            for alpha in range(N):

                ctrl = ClassicalRegister(1, name="ctrl")
                x_register = ClassicalRegister(n, name="x")
                b_register = ClassicalRegister(n+1, name="b")
                flag = ClassicalRegister(1, name="flag")

                test_circuit = QuantumCircuit(2*n + 3)
                test_circuit.add_register(ctrl, x_register, b_register, flag)
                test_circuit.x(0)

                binary = bin(initial_number)[2:]
            
                # Prepare the initial number encoded into x gates in the beggining...
                for k in range(len(binary)):
                    if binary[::-1][k] == '1':
                        test_circuit.x(k+1)

                test_circuit.barrier()

                mult = c_modular_multiplier(alpha, n, N)

                test_circuit.append(mult, range(2*n + 3))

                test_circuit.measure([0], ctrl)
                test_circuit.measure([i+1 for i in range(n)], x_register)
                test_circuit.measure([n+1+i for i in range(n+1)], b_register)
                test_circuit.measure(2*n+2, flag)

                print(test_circuit)

                backend = QasmSimulator()
                backend_options = {'method': 'simulator'}
                job = execute(test_circuit, backend, backend_options=backend_options, shots=20000)
                job_result = job.result()

                counts = job_result.get_counts(test_circuit)

                print(counts)
    return True


def test_modular_multiplier():
    
    for N in range(1 << (n-1), 1 << n):
        for initial_number in range(N):
            for alpha in range(N):

                if gcd(N, alpha) != 1:
                    continue

                controls = ClassicalRegister(1, name="ctrl")
                result = ClassicalRegister(n, name="result")
                aux = ClassicalRegister(n+1, name="aux")
                flag = ClassicalRegister(1, name="flag")

                test_circuit = QuantumCircuit(2*n + 3)
                test_circuit.add_register(controls)
                test_circuit.add_register(result)
                test_circuit.add_register(aux)
                test_circuit.add_register(flag)

                test_circuit.x(0)

                binary = bin(initial_number)[2:]
            
                # Prepare the initial number encoded into x gates in the beggining...
                for k in range(len(binary)):
                    if binary[::-1][k] == '1':
                        test_circuit.x(k+1)

                test_circuit.barrier()

                inv_alpha = calculate_inverse_mod_n(alpha, N)

                c_u_gate = c_U(alpha, inv_alpha, n, N).to_gate(label="U")

                test_circuit.append(c_u_gate, range(2*n+3))

                test_circuit.measure([0], controls)
                test_circuit.measure(range(1, n+1), result)
                test_circuit.measure(range(n+1, 2*n+2), aux)
                test_circuit.measure(2*n+2, flag)

                backend = QasmSimulator()
                backend_options = {'method': 'simulator'}
                job = execute(test_circuit, backend, backend_options=backend_options, shots=20000)
                job_result = job.result()

                counts = job_result.get_counts(test_circuit)

                print(counts)

                bin_result = list(counts.keys())[0]
                elements = bin_result.split(' ')

                beta = int(elements[1], 2)
                res = int(elements[2], 2)

                print(str(initial_number) + ' * ' + str(alpha) + ' mod ' + str(N) + ' = ' + str(res))

                if beta != 0:
                    return False

                if res != (alpha * initial_number) % N:
                    return False


    return True

def calculate_inverse_mod_n(alpha: int, N: int) -> int:
    if alpha == 0:
        return 0

    num = 1

    while True:

        if (alpha * num) % N == 1:
            return num
        num += 1

def print_verdict(verdict: bool, test_name: str, exec_time: float):
    if verdict:
        print("[     " + bcolors.OKGREEN + "OK" + bcolors.ENDC + "     ] - " + test_name + " @ %.2f ms" % exec_time)
    else:
        print("[" + bcolors.FAIL + "***FAILED***" + bcolors.ENDC + "] - " + test_name + " @ %.2f ms" % exec_time)
        exit(1)
    pass

def main():
    #start_time = time.time()
    #verdict = test_adder()
    #print_verdict(verdict, "Fourier ADD gate", time.time() - start_time)

    #start_time = time.time()
    #verdict = test_adder_dagger()
    #print_verdict(verdict, "Fourier SUB gate", time.time() - start_time)

    #start_time = time.time()
    #verdict = test_cc_mod_adder()
    #print_verdict(verdict, "Modular ADD gate", time.time() - start_time)

    #start_time = time.time()
    #verdict = test_cc_mod_adder_dagger()
    #print_verdict(verdict, "Modular SUB gate", time.time() - start_time)

    #start_time = time.time()
    #verdict = test_modular_multiplier()
    #print_verdict(verdict, "Modular MULT gate", time.time() - start_time)

    fast()
    exit(0)

    N = 7*11
    a = 8

    circuit = shor_circuit(N, a)

    print(circuit)

    backend = QasmSimulator()
    backend_options = {'method': 'simulator'}
    job = execute(circuit, backend, backend_options=backend_options, shots=20000, memory=True)
    job_result = job.result()

    counts = job_result.get_counts(circuit)
    memory = job_result.get_memory()
    memory.sort()

    print(counts)

    memory_int = []

    for element in memory:
        a = int(element, 2)
        memory_int.append(a)

    plt.figure(facecolor='white')
    plt.hist(memory_int, bins=1000)
    plt.show()
    
def fast():
    N = 15
    a = 2

    circuit = shor_circuit(N, a)

    print(circuit)

    simulator = Aer.get_backend('aer_simulator_unitary')
    simulator.set_options(precision='single', device='GPU')

    result = simulator.run(circuit).result()
    
    
def assertEqual(arg1, arg2) -> bool:
    return arg1 == arg2

if __name__ == "__main__":
    main()