from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.providers.aer import QasmSimulator
from quantum_fourier_transform import qft_dagger
import numpy as np

def U(theta: float, power: int) -> QuantumCircuit:
    qc = QuantumCircuit(1)
    for i in range(1 << power):
        qc.p(theta * 2 * np.pi, 0)
    return qc

n = 3 # Precision
theta = 5/16

counting_registers = QuantumRegister(n, name="cnt")
aux_register = QuantumRegister(1, name="aux")
measuring_registers = ClassicalRegister(n, name="meas")

qc = QuantumCircuit(counting_registers, aux_register, measuring_registers)

for i in range(n):
    qc.h(i)
qc.x(n)

# Create controlled gates...
for i in range(n):
    qc.append(U(theta=theta, power=i).to_gate(label=r'$U^{2^{%i}}$' %(i)).control(num_ctrl_qubits=1), [i] + [n])

qc.append(qft_dagger(n).to_gate(label=r'QFT$\dagger$'), range(n))

qc.measure(range(n), range(n))

simulator = QasmSimulator(method='automatic')
result = simulator.run(qc.decompose(), shots=1000, memory=True).result()
print(qc)

memory = result.get_memory()

memory.sort()

counts = result.get_counts()

print(counts)

qc.draw('mpl', fold=-1).savefig("phase_estimation_precision_3", dpi=400)