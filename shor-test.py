from qiskit import *
from shor import Shor
from qiskit.providers.aer import QasmSimulator
import matplotlib.pyplot as plt


import random as rand
rand.seed(1)

# ----------- <CONSTANTS> ----------- #
p = 5
q = 3

N = p*q
N = 15
a = rand.randint(2, N-1)
a = 2
# ----------------------------------- #

print('Running Shor\'s algorithm for N:', N, 'and a:', a)

qc = Shor(N, a)
print(qc.draw('text'))

backend = QasmSimulator()
backend_options = {'method': 'simulator'}
job = execute(qc, backend, backend_options=backend_options, shots=20000, memory=True)
job_result = job.result()

memory = job_result.get_memory()
memory.sort()
counts = job_result.get_counts()

s = dict(reversed(sorted(counts.items(), key=lambda item : item[1])))

new_memory = []
for item in memory:
    new_memory.append(int(item, 2))

#print(new_memory)

plt.figure(facecolor='white')
plt.hist(new_memory, linewidth=1, orientation='vertical', stacked=False, rwidth=1, bins=200)
plt.show()