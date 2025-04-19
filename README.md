# Shor's Algorithm

This is the implementation of Shor's algorithm using Qiskit. This repository also contains other algorithms that are used as subroutines in Shor's algorithm, like Quantum Fourier Transform and Quantum Phase Estimation.

## Prodecure

Suppose that we are given a number ***N*** which is the **public** key and is always constructed by multipying two **prime numbers**. Then we can execute the following steps to factorize ***N***.

1. Pick a number ***a*** uniformly at random **x ∈ [2, N−1]**
2. Compute ***K = gcd(a, N)*** using Eucledian algorithm
3. If ***K ≠ 1*** then ***K*** is a factor of ***N*** and we are done. (Very unlikely for large numbers)
4. Use **Shor's algorithm** to compute **r = ordₙ(a)**
5. If ***r*** is odd, repeat the process from step 1
6. If **√(aʳ) ± 1 ≡ 0 (mod N)** then repeat again the process from step 1
7. The factors of ***N*** are **gcd(√(aʳ) + 1, N)** and **gcd(√(aʳ) - 1, N)**

Note that steps 1, 2, 3 are the preprocessing steps done on a classical computer. Steps 5, 6, 7 are the postprocessing steps and are also executed on a classical computer. **Only step 4 runs on a quantum computer**

## Python and Qiskit version

Python version: 3.13.2

| Package    | Version |
| ---------- | ------- |
| qiskit     | 2.0.0   |
| qiskit-aer | 0.17.0  |
