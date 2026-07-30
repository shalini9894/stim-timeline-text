# Modifications to vendored Stim sources

Vendored from Stim v1.15.0 (commit 42e0b9e099180e8570407c33f87b4683cac00d81).

58 of 61 files are byte-identical to upstream. Verify with:

    sha256sum -c ORIGINAL_SHA256SUMS.txt

Three files are modified. Each change is marked with a `TSIM MODIFICATION` comment.

## src/stim/diagram/circuit_timeline_helper.h

Added a `tag` field to `ResolvedTimelineOperation`, and a `cur_tag` member to
`CircuitTimelineHelper`. Upstream drops the instruction tag during resolution,
so it never reaches the drawer.

## src/stim/diagram/circuit_timeline_helper.cc

`do_next_operation` records the current instruction's tag; `do_atomic_operation`
passes it into the resolved operation.

## src/stim/diagram/timeline/timeline_ascii_drawer.cc

Before writing a gate label, consults `tsim_labels::logical_label`. When the tag
is recognised the logical name is used instead of the placeholder gate name;
otherwise upstream behaviour is unchanged. Applies to both the single-qubit path
and the Pauli-product path.

Label substitution happens before ASCII layout, so column widths and connectors
account for the longer names.
