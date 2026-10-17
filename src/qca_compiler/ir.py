"""Intermediate representation for QCA circuits."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Gate:
    """One gate in a QCA circuit."""
    name: str                     # 'H', 'S', 'T', 'X', 'Y', 'Z', 'CNOT', 'CZ', 'Rz', 'Rx'
    qubits: List[int]             # target qubit(s)
    params: List[float] = field(default_factory=list)

    def __repr__(self):
        p = f" {self.params}" if self.params else ""
        return f"{self.name}({','.join(map(str, self.qubits))}){p}"


@dataclass
class Circuit:
    """A QCA circuit."""
    n_qubits: int
    gates: List[Gate]

    def __len__(self):
        return len(self.gates)

    def count(self, name=None):
        if name is None:
            return len(self.gates)
        return sum(1 for g in self.gates if g.name == name)
