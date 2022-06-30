from modular_adder import fourier_add_mod
from qiskit import *

from qiskit.providers.aer import QasmSimulator

import os
os.system('color')

N = 15
n = len(bin(N)[2:])
a = 2

