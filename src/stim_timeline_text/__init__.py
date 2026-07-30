"""Tag-aware ASCII timeline diagrams for Stim circuits."""

from __future__ import annotations

import html as _html

from stim_timeline_text._native import render_timeline_text as _render

__version__ = "0.1.0"
__all__ = ["TimelineTextDiagram", "render_timeline_text"]


class TimelineTextDiagram:
    """An ASCII timeline diagram. Renders as plain text, or as HTML in notebooks."""

    def __init__(self, text: str) -> None:
        self._text = text

    def __str__(self) -> str:
        return self._text

    def __repr__(self) -> str:
        return f"TimelineTextDiagram({self._text!r})"

    def _repr_html_(self) -> str:
        return f"<pre>{_html.escape(self._text)}</pre>"


def render_timeline_text(stim_program: str) -> TimelineTextDiagram:
    """Render a Stim circuit program as a tag-aware ASCII timeline diagram."""
    return TimelineTextDiagram(_render(stim_program))
