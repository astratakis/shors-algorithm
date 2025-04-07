# Shor's Algorithm

This is the implementation of Shor's algorithm using Qiskit. This repository also contains other algorithms that are used as subroutines in Shor's algorithm, like Quantum Fourier Transform and Quantum Phase Estimation. This algorithm computes the number \(r\), such that
\[
a^r \mod N = 1,
\]
where \(N\) is the public key and \(a\) is a randomly selected number. Given this number \(r\), the public key \(N\) can then be decomposed into the prime numbers that were used to compute it, which form the private key.

### Python and Qiskit version

Python version: 3.13.2

| Package    | Version |
| ---------- | ------- |
| qiskit     | 2.0.0   |
| qiskit-aer | 0.17.0  |
