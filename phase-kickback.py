from qiskit import QuantumCircuit
from numpy import pi

from qiskit.visualization import *

if __name__ == "__main__":

    qc = QuantumCircuit(2)
    qc.h(0)
    qc.x(1)

    # Add Controlled-T
    qc.cp(pi/4, 0, 1)
    qc.save_statevector()
    qc.draw('mpl', fold=-1).savefig("kickback", dpi=400)
    # See Results:
    svsim = AerSimulator()
    final_state = svsim.run(qc).result().get_statevector()
    plot_bloch_multivector(final_state).savefig("kickback_bloch", dpi=400)