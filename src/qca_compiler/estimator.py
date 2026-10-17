"""Resource estimates for native QCA circuits."""
from .ir import Circuit


# IBM Eagle r3 default error rates
ECR_ERROR = 0.007
SQ_ERROR = 1e-4
READOUT_ERROR = 0.02


def estimate(circuit, ecr_error=ECR_ERROR, sq_error=SQ_ERROR,
             shots=8192):
    """Return resource estimate dict."""
    n_1q = sum(1 for g in circuit.gates if g.name in ("Rz", "Rx"))
    n_2q = sum(1 for g in circuit.gates if g.name == "CZ")

    # Fidelity model: (1 - ecr)^n_2q * (1 - sq)^n_1q
    fidelity = (1 - ecr_error) ** n_2q * (1 - sq_error) ** n_1q

    # Estimated circuit depth (naive -- no scheduling)
    depth_estimate = n_2q + n_1q // circuit.n_qubits + 1

    return {
        "n_qubits": circuit.n_qubits,
        "total_native_gates": len(circuit.gates),
        "native_1q": n_1q,
        "native_2q": n_2q,
        "estimated_depth": depth_estimate,
        "estimated_fidelity": round(fidelity, 4),
        "ecr_error": ecr_error,
        "sq_error": sq_error,
    }


def estimate_logical_to_physical(circuit, code_distance=3):
    """Estimate physical gate count if the circuit runs on a
    surface code of given distance.

    Each native 2q gate becomes O(d^2) physical gates.
    """
    n_2q = sum(1 for g in circuit.gates if g.name == "CZ")
    physical_2q = n_2q * code_distance ** 2
    return {
        "logical_2q": n_2q,
        "code_distance": code_distance,
        "physical_2q": physical_2q,
    }
