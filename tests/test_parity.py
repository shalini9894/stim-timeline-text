"""Untagged circuits must render byte-identically to upstream Stim."""

import random

import pytest

stim = pytest.importorskip("stim")

from stim_timeline_text import render_timeline_text

GATES1 = ["H", "S", "S_DAG", "X", "Y", "Z", "SQRT_X", "SQRT_Y", "C_XYZ", "H_XY", "I"]
GATES2 = ["CX", "CZ", "CY", "SWAP", "ISWAP", "SQRT_XX", "SQRT_ZZ", "XCZ"]
NOISE1 = ["X_ERROR", "Z_ERROR", "DEPOLARIZE1"]
COLLAPSE = ["M", "MX", "MR", "R", "RX"]


def random_circuit(rng: random.Random, n: int = 6) -> str:
    lines = []
    for _ in range(rng.randint(3, 14)):
        r = rng.random()
        if r < 0.30:
            lines.append(f"{rng.choice(GATES1)} {rng.randrange(n)}")
        elif r < 0.55:
            a, b = rng.sample(range(n), 2)
            lines.append(f"{rng.choice(GATES2)} {a} {b}")
        elif r < 0.68:
            p = round(rng.uniform(0.001, 0.2), 4)
            lines.append(f"{rng.choice(NOISE1)}({p}) {rng.randrange(n)}")
        elif r < 0.82:
            lines.append(f"{rng.choice(COLLAPSE)} {rng.randrange(n)}")
        elif r < 0.88:
            lines.append("TICK")
        elif r < 0.94:
            paulis = "*".join(
                f"{rng.choice('XYZ')}{q}"
                for q in rng.sample(range(n), rng.randint(1, 3))
            )
            lines.append(f"{rng.choice(['MPP', 'SPP', 'SPP_DAG'])} {paulis}")
        else:
            lines.append(
                f"REPEAT {rng.randint(2, 4)} {{\n"
                f"  {rng.choice(GATES1)} {rng.randrange(n)}\n"
                f"  M {rng.randrange(n)}\n}}"
            )
    return "\n".join(lines) + "\n"


CURATED = [
    "H 0\nCX 0 1\nM 0 1\n",
    "R 0 1 2\nTICK\nH 0\nCZ 0 1\nS 2\nM 0 1 2\nDETECTOR rec[-1] rec[-2]\n",
    "X_ERROR(0.01) 0\nDEPOLARIZE2(0.001) 0 1\nMPP X0*Y1*Z2\n",
    "REPEAT 5 {\n  H 0\n  CX 0 1\n  M 1\n  DETECTOR rec[-1]\n}\n",
    "QUBIT_COORDS(1,2) 0\nH 0\nM 0\nOBSERVABLE_INCLUDE(0) rec[-1]\n",
    "SPP X0*Y1\nSPP_DAG Z2\nSQRT_XX 0 1\nISWAP 2 3\n",
]


@pytest.mark.parametrize("program", CURATED)
def test_curated_parity(program):
    assert str(render_timeline_text(program)) == str(
        stim.Circuit(program).diagram("timeline-text")
    )


def test_random_parity():
    rng = random.Random(171)
    for _ in range(500):
        program = random_circuit(rng)
        assert str(render_timeline_text(program)) == str(
            stim.Circuit(program).diagram("timeline-text")
        ), f"mismatch for:\n{program}"
