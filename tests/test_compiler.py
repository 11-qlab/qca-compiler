"""Tests for the QCA compiler."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pytest


def test_parse_bell():
    from qca_compiler import parse
    circ = parse({"n_qubits": 2, "gates": [
        {"name": "H", "qubits": [0]},
        {"name": "CNOT", "qubits": [0, 1]},
    ]})
    assert circ.n_qubits == 2
    assert len(circ.gates) == 2
    assert circ.gates[0].name == "H"


def test_h_decomposition_count():
    """H -> 3 native gates (Rz, Rx, Rz)."""
    from qca_compiler import parse, map_to_native
    circ = parse({"n_qubits": 1, "gates": [
        {"name": "H", "qubits": [0]},
    ]})
    native = map_to_native(circ)
    assert len(native.gates) == 3
    assert [g.name for g in native.gates] == ["Rz", "Rx", "Rz"]


def test_cnot_decomposition_count():
    """CNOT -> 7 native gates (3 H + CZ + 3 H)."""
    from qca_compiler import parse, map_to_native
    circ = parse({"n_qubits": 2, "gates": [
        {"name": "CNOT", "qubits": [0, 1]},
    ]})
    native = map_to_native(circ)
    assert len(native.gates) == 7


def test_bell_native_count():
    """Bell state = H + CNOT = 3 + 7 = 10 native gates."""
    from qca_compiler import parse, map_to_native
    circ = parse({"n_qubits": 2, "gates": [
        {"name": "H", "qubits": [0]},
        {"name": "CNOT", "qubits": [0, 1]},
    ]})
    native = map_to_native(circ)
    assert len(native.gates) == 10


def test_ghz_native_count():
    """GHZ = H + 2 CNOT = 3 + 14 = 17 native gates."""
    from qca_compiler import parse, map_to_native
    circ = parse({"n_qubits": 3, "gates": [
        {"name": "H", "qubits": [0]},
        {"name": "CNOT", "qubits": [0, 1]},
        {"name": "CNOT", "qubits": [1, 2]},
    ]})
    native = map_to_native(circ)
    assert len(native.gates) == 17


def test_emit_qiskit_bell():
    """Emit Qiskit circuit and verify Bell state simulation."""
    from qca_compiler import parse, map_to_native, emit_qiskit
    from qiskit.quantum_info import Statevector

    circ = parse({"n_qubits": 2, "gates": [
        {"name": "H", "qubits": [0]},
        {"name": "CNOT", "qubits": [0, 1]},
    ]})
    native = map_to_native(circ)
    qc = emit_qiskit(native)

    sv = Statevector(qc)
    probs = sv.probabilities_dict()
    # Bell state: |00> and |11> only
    p00 = probs.get("00", 0)
    p11 = probs.get("11", 0)
    p01 = probs.get("01", 0)
    p10 = probs.get("10", 0)
    assert abs(p00 - 0.5) < 1e-6
    assert abs(p11 - 0.5) < 1e-6
    assert p01 < 1e-6
    assert p10 < 1e-6


def test_emit_ghz():
    """GHZ state: |000> and |111> only."""
    from qca_compiler import parse, map_to_native, emit_qiskit
    from qiskit.quantum_info import Statevector

    circ = parse({"n_qubits": 3, "gates": [
        {"name": "H", "qubits": [0]},
        {"name": "CNOT", "qubits": [0, 1]},
        {"name": "CNOT", "qubits": [1, 2]},
    ]})
    native = map_to_native(circ)
    qc = emit_qiskit(native)

    sv = Statevector(qc)
    probs = sv.probabilities_dict()
    assert abs(probs.get("000", 0) - 0.5) < 1e-6
    assert abs(probs.get("111", 0) - 0.5) < 1e-6


def test_estimate_fidelity():
    """Estimate returns a fidelity in [0, 1]."""
    from qca_compiler import parse, map_to_native, estimate
    circ = parse({"n_qubits": 2, "gates": [
        {"name": "H", "qubits": [0]},
        {"name": "CNOT", "qubits": [0, 1]},
    ]})
    native = map_to_native(circ)
    est = estimate(native)
    assert 0.5 < est["estimated_fidelity"] < 1.0
    assert est["native_2q"] == 1
    assert est["native_1q"] == 9


def test_unknown_gate_raises():
    from qca_compiler import parse, map_to_native
    circ = parse({"n_qubits": 1, "gates": [
        {"name": "XYZ", "qubits": [0]},
    ]})
    with pytest.raises(ValueError, match="Cannot decompose"):
        map_to_native(circ)
