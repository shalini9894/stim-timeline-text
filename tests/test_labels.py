"""Tsim tag decoding: correct labels in, unrecognised tags left alone."""

import pytest

from stim_timeline_text import render_timeline_text


def render(program: str) -> str:
    return str(render_timeline_text(program))


@pytest.mark.parametrize(
    "program,expected",
    [
        ("S[T] 0\n", "T"),
        ("S[T:mynote] 0\n", "T"),
        ("S_DAG[T] 0\n", "T_DAG"),
        ("I[R_X(theta=0.125*pi)] 0\n", "R_X(0.125)"),
        ("I[R_Y(theta=-0.25*pi)] 0\n", "R_Y(-0.25)"),
        ("I[R_Z(theta=0.5*pi)] 0\n", "R_Z(0.5)"),
        (
            "I[U3(theta=0.5*pi, phi=0.25*pi, lambda=-0.125*pi)] 0\n",
            "U3(0.5,0.25,-0.125)",
        ),
    ],
)
def test_tsim_gate_labels(program, expected):
    assert expected in render(program)


def test_pauli_product_labels():
    out = render("SPP[T] X0*Y1\n")
    assert "TPP[X]" in out and "TPP[Y]" in out


def test_pauli_product_dagger():
    assert "TPP_DAG[Z]" in render("SPP_DAG[T] Z0\n")


def test_r_pauli():
    assert "R_PAULI(0.5)[X]" in render("SPP[R_PAULI(theta=0.5*pi)] X0\n")


@pytest.mark.parametrize(
    "program,expected",
    [
        ("H[whatever] 0\n", "H"),
        ("CX[note] 0 1\n", "@"),
        ("S[not_a_tsim_tag] 0\n", "S"),
        ("I[R_Z(theta=broken)] 0\n", "I"),
        ("I[UNKNOWN_GATE(theta=0.5*pi)] 0\n", "I"),
    ],
)
def test_unrecognised_tags_are_ignored(program, expected):
    assert expected in render(program)


def test_tags_survive_repeat_blocks():
    out = render("REPEAT 3 {\n  S[T] 0\n  I[R_Z(theta=0.25*pi)] 1\n}\n")
    assert "T" in out and "R_Z(0.25)" in out
