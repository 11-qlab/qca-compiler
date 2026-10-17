# qca-compiler

Compile QCA circuit specifications into Qiskit circuits that use
only the native gate set `{Rz, Rx, CZ}`.

Built on the gate algebra established in
[QCA as a Native Quantum Platform](https://github.com/11-qlab/qca-sim):

- `H = Rz(pi/2) . Rx(pi/2) . Rz(pi/2)` -- 3 native gates
- `S = Rz(pi/2)` -- 1 native gate
- `T = Rz(pi/4)` -- 1 native gate
- `CNOT = (I tensor H) . CZ . (I tensor H)` -- 7 native gates

## Install

pip install qca-compiler

## CLI usage

qca-compile examples/bell.json -o bell.qasm --estimate

Input JSON format:

{
  "n_qubits": 2,
  "gates": [
    {"name": "H", "qubits": [0]},
    {"name": "CNOT", "qubits": [0, 1]}
  ]
}

Supported gates: H, S, T, X, Y, Z, CNOT, CZ, Rz(theta), Rx(theta).

## Python API

from qca_compiler import parse, map_to_native, emit_qiskit, estimate

circ = parse("examples/bell.json")
native = map_to_native(circ)
qc = emit_qiskit(native)
est = estimate(native)

## Resource estimate

The estimate function reports:
- Native 1q and 2q gate counts
- Estimated circuit depth
- Predicted hardware fidelity based on IBM Eagle r3 error rates

## Tests

pytest tests/ -v

## License

Apache 2.0
