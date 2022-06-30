from qiskit import *
from adder import Shor
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

