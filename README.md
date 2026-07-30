# stim-timeline-text

Tag-aware ASCII timeline diagrams for [Stim](https://github.com/quantumlib/Stim) circuits.

Simulators built on Stim often express non-Clifford gates as tagged Clifford
placeholders. `T` gate stored as `S` carrying the tag `T`, for example.
Stim's own timeline renderer discards the tag, so those gates are drawn under
their placeholder names. This package renders the logical gate instead.

## Install

    pip install stim-timeline-text

## Usage

```python
from stim_timeline_text import render_timeline_text

print(render_timeline_text("S[T] 0\nSPP[T] X1*Y2\n"))
```
cat >> README.md << 'EOF'

## Supported tags

Currently decodes [tsim](https://github.com/QuEraComputing/tsim)'s conventions:

| Stored form | Rendered |
|---|---|
| `S[T]`, `S_DAG[T]` | `T`, `T_DAG` |
| `SPP[T]`, `SPP_DAG[T]` | `TPP[X]`, `TPP_DAG[Z]` |
| `I[R_X(theta=0.125*pi)]` | `R_X(0.125)` |
| `I[U3(theta=..., phi=..., lambda=...)]` | `U3(0.5,0.25,-0.125)` |
| `SPP[R_PAULI(theta=0.5*pi)]` | `R_PAULI(0.5)[X]` |

A user tag attached to a gate (`S[T:mynote]`) is stripped from the label.

**Tags this package doesn't recognise are ignored entirely.** Circuits with no
tsim metadata render byte-identically to upstream Stim, verified against 500
generated circuits plus curated cases in the test suite.

### Known limitation

`R_XX`, `R_YY`, and `R_ZZ` are stored by tsim under the same tag as `R_PAULI`,
so the specific name cannot be recovered from the tag alone. They render as
`R_PAULI(theta)[X]`. This is intentional; see
[tsim#171](https://github.com/QuEraComputing/tsim/issues/171).

## Vendored Stim sources

`cpp/vendor/stim/` contains a partial copy of Stim v1.15.0 (commit
`42e0b9e099180e8570407c33f87b4683cac00d81`). Vendoring is necessary because the
tag is discarded inside Stim's C++ before any label is built, and that point is
not reachable from Stim's Python API.

61 files are vendored. 58 are byte-identical to upstream; 3 are modified, each
change marked with a `TSIM MODIFICATION` comment and described in
[`MODIFICATIONS.md`](cpp/vendor/stim/MODIFICATIONS.md).

Verify for yourself:

    cd cpp/vendor/stim && sha256sum -c ORIGINAL_SHA256SUMS.txt

Stim is Apache-2.0 licensed; its licence is retained alongside the vendored
sources.

## Development

    uv venv && source .venv/bin/activate
    uv pip install -e ".[test]"
    pytest tests/ -v

## Licence

Apache-2.0. Independent project, not affiliated with QuEra Computing or Google.
