"""Map QCA circuit gates to the native gate set {Rz, Rx, CZ}.

Decompositions (from F25, arXiv:2610.XXXXX):
  H    = Rz(pi/2) . Rx(pi/2) . Rz(pi/2)
  S    = Rz(pi/2)
  T    = Rz(pi/4)
  X    = Rx(pi)
  Y    = Rz(pi) . Rx(pi)
  Z    = Rz(pi)
  CNOT = (I x H) . CZ . (I x H)
       = 3 + 1 + 3 = 7 native gates
"""
import numpy as np
from .ir import Circuit, Gate


NATIVE_GATES = {"Rz", "Rx", "CZ"}


# Static decompositions: gate -> [(native_name, [qubit_offsets], [params])]
DECOMPOSITIONS = {
    "H": [
        ("Rz", [0], [np.pi / 2]),
        ("Rx", [0], [np.pi / 2]),
        ("Rz", [0], [np.pi / 2]),
    ],
    "S": [("Rz", [0], [np.pi / 2])],
    "T": [("Rz", [0], [np.pi / 4])],
    "X": [("Rx", [0], [np.pi])],
    "Y": [("Rz", [0], [np.pi]), ("Rx", [0], [np.pi])],
    "Z": [("Rz", [0], [np.pi])],
    "CNOT": [
        # H on target (3 native)
        ("Rz", [1], [np.pi / 2]),
        ("Rx", [1], [np.pi / 2]),
        ("Rz", [1], [np.pi / 2]),
        # CZ (1 native)
        ("CZ", [0, 1], []),
        # H on target (3 native)
        ("Rz", [1], [np.pi / 2]),
        ("Rx", [1], [np.pi / 2]),
        ("Rz", [1], [np.pi / 2]),
    ],
    "CZ": [("CZ", [0, 1], [])],
}


def map_to_native(circuit):
    """Decompose every gate into the native gate set {Rz, Rx, CZ}."""
    out = []
    for g in circuit.gates:
        if g.name in NATIVE_GATES:
            out.append(Gate(g.name, list(g.qubits), list(g.params)))
            continue

        if g.name not in DECOMPOSITIONS:
            raise ValueError(f"Cannot decompose gate: {g.name}")

        for name, qubit_offsets, params in DECOMPOSITIONS[g.name]:
            actual = [g.qubits[q] for q in qubit_offsets]
            out.append(Gate(name, actual, list(params)))

    return Circuit(circuit.n_qubits, out)


def native_gate_set():
    """Return the set of native gate names."""
    return NATIVE_GATES.copy()
