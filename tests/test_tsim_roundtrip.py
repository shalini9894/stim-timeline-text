"""End-to-end: tags produced by tsim itself, not written by hand.

Skipped when bloqade-tsim isn't installed.
"""

import pytest

tsim = pytest.importorskip("tsim")

from stim_timeline_text import render_timeline_text


def render_via_tsim(circuit) -> str:
    return str(render_timeline_text(str(circuit._stim_circ)))


@pytest.mark.parametrize(
    "source,expected",
    [
        ("T 0", "T"),
        ("T_DAG 0", "T_DAG"),
        ("R_X(0.125) 0", "R_X(0.125)"),
        ("R_Y(-0.25) 0", "R_Y(-0.25)"),
        ("R_Z(0.5) 0", "R_Z(0.5)"),
        ("U3(0.5,0.25,-0.125) 0", "U3(0.5,0.25,-0.125)"),
        ("TPP X0*Y1", "TPP[X]"),
        ("TPP_DAG Z0", "TPP_DAG[Z]"),
    ],
)
def test_text_syntax_gates(source, expected):
    assert expected in render_via_tsim(tsim.Circuit(source))


@pytest.mark.parametrize(
    "name,targets,arg,expected",
    [
        ("R_XX", [0, 1], 0.5, "R_PAULI(0.5)[X]"),
        ("R_YY", [0, 1], -0.25, "R_PAULI(-0.25)[Y]"),
        ("R_ZZ", [0, 1], 0.125, "R_PAULI(0.125)[Z]"),
    ],
)
def test_two_qubit_rotations_render_as_r_pauli(name, targets, arg, expected):
    """R_XX/R_YY/R_ZZ share R_PAULI's tag; see README for why."""
    circuit = tsim.Circuit()
    circuit.append(name, targets, arg)
    assert expected in render_via_tsim(circuit)


def test_ccz_renders_as_its_decomposition():
    """tsim decomposes CCZ into Clifford+T before storage, so no CCZ box appears."""
    circuit = tsim.Circuit()
    circuit.append("CCZ", [0, 1, 2])
    out = render_via_tsim(circuit)
    assert "T" in out
    assert "CCZ" not in out


def test_user_tag_is_stripped_from_label():
    circuit = tsim.Circuit()
    circuit.append("T", [0], tag="mynote")
    out = render_via_tsim(circuit)
    assert "T" in out
    assert "mynote" not in out
