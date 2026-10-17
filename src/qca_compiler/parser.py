"""Parse JSON QCA circuits into the IR."""
import json
from .ir import Circuit, Gate


def parse(source):
    """Parse a JSON file path or dict into a Circuit."""
    if isinstance(source, dict):
        data = source
    else:
        with open(source) as f:
            data = json.load(f)

    n = data["n_qubits"]
    gates = []
    for entry in data["gates"]:
        gates.append(Gate(
            name=entry["name"],
            qubits=list(entry["qubits"]),
            params=list(entry.get("params", [])),
        ))
    return Circuit(n_qubits=n, gates=gates)


def to_json(circuit):
    """Serialize a Circuit back to a dict."""
    return {
        "n_qubits": circuit.n_qubits,
        "gates": [
            {"name": g.name, "qubits": g.qubits, "params": g.params}
            for g in circuit.gates
        ],
    }
