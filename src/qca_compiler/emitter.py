"""Emit Qiskit circuits from native-gate QCA circuits."""
from qiskit import QuantumCircuit


def emit_qiskit(circuit):
    """Convert a native-gate Circuit to a Qiskit QuantumCircuit."""
    qc = QuantumCircuit(circuit.n_qubits)
    for g in circuit.gates:
        if g.name == "Rz":
            qc.rz(g.params[0], g.qubits[0])
        elif g.name == "Rx":
            qc.rx(g.params[0], g.qubits[0])
        elif g.name == "CZ":
            qc.cz(g.qubits[0], g.qubits[1])
        else:
            raise ValueError(f"Non-native gate: {g.name}")
    return qc


def emit_qasm(circuit):
    """Return QASM 2.0 string."""
    return emit_qiskit(circuit).qasm()
