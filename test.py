from qiskit import *
from numpy import pi
from qiskit.providers.aer import QasmSimulator
steps = 200

min = 10000000
best = -1

for i in range(steps):

    theta = i * (2*pi/steps)

    print('Simulating for theta:', theta)

    for j in range(steps):
        phi = j * (2*pi/steps)

        #print('Simulating for theta:', theta, 'and phi:', phi)

        qc = QuantumCircuit(2)
        qc.h(0)
        qc.h(1)
        qc.z(0)
        qc.x(0)
        qc.z(0)
        qc.x(0)
        qc.cz(0, 1)
        
        qc.cp(theta, 0, 1)

        qc.h(0)
        qc.h(1)
        qc.x(0)
        qc.x(1)
        qc.cp(phi, 0, 1)
        qc.x(0)
        qc.x(1)
        qc.h(0)
        qc.h(1)

        qc.save_statevector()

        qc.measure_all()

        backend = QasmSimulator()
        backend_options = {'method': 'statevector'}
        job = execute(qc, backend, backend_options=backend_options)
        job_result = job.result()
        wanted = job_result.get_statevector(qc)[3]

        if abs(wanted) < min:
            min = abs(wanted)
            best = wanted

print(min)

