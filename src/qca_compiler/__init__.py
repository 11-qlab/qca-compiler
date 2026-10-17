"""QCA-to-Qiskit compiler.

Convert QCA circuit specifications into Qiskit circuits that
use only the native gate set {Rz, Rx, CZ}, as established in
the qca-sim paper (arXiv:2610.XXXXX, findings F2 and F25).
"""
from .ir import Gate, Circuit
from .parser import parse, to_json
from .mapper import map_to_native, native_gate_set
from .emitter import emit_qiskit, emit_qasm
from .estimator import estimate, estimate_logical_to_physical

__version__ = "0.1.0"
__all__ = [
    "Gate", "Circuit",
    "parse", "to_json",
    "map_to_native", "native_gate_set",
    "emit_qiskit", "emit_qasm",
    "estimate", "estimate_logical_to_physical",
]
