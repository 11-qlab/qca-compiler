"""Command-line interface for qca-compile."""
import argparse
import json
import sys
from .parser import parse, to_json
from .mapper import map_to_native
from .emitter import emit_qasm
from .estimator import estimate, estimate_logical_to_physical


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="qca-compile",
        description="Compile QCA circuits to Qiskit using native gates",
    )
    p.add_argument("input", help="QCA circuit JSON file")
    p.add_argument("-o", "--output", help="Output QASM file")
    p.add_argument("-n", "--native", help="Output native-gate circuit JSON")
    p.add_argument("--estimate", action="store_true",
                   help="Print resource estimate")
    p.add_argument("--surface-code", type=int, metavar="D",
                   help="Estimate physical gate count with surface code distance D")
    p.add_argument("--quiet", action="store_true", help="Suppress banner")
    args = p.parse_args(argv)

    try:
        circ = parse(args.input)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"Input: {circ.n_qubits} qubits, {len(circ.gates)} gates")

    native = map_to_native(circ)
    if not args.quiet:
        print(f"Native: {len(native.gates)} gates "
              f"(Rz={native.count('Rz')}, "
              f"Rx={native.count('Rx')}, "
              f"CZ={native.count('CZ')})")

    if args.estimate:
        est = estimate(native)
        print(json.dumps(est, indent=2))

    if args.surface_code:
        est = estimate_logical_to_physical(native, args.surface_code)
        print(json.dumps(est, indent=2))

    if args.native:
        with open(args.native, "w") as f:
            json.dump(to_json(native), f, indent=2)
        print(f"wrote {args.native}")

    if args.output:
        qasm = emit_qasm(native)
        with open(args.output, "w") as f:
            f.write(qasm)
        print(f"wrote {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
