"""The three role conventions documents keep their cap and their rule anchors.

F105 T002's conventions loaders were deleted for finding R-0981 because no prompt
builder ever registered the segment they built. The documents stay, reviewed
by hand, and these tests keep the two properties that were about the DOCUMENTS and
not the loader: each stays under the conventions cap, and none was hollowed out.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from packages.orchestration.prompt_segments import CONVENTIONS_TOKEN_CAP
from packages.orchestration.token_economy import estimate_text_tokens

REPO = Path(__file__).resolve().parents[2]

ANCHORS = {
    "docs/agents/worker_conventions.md": ("## Ground rules", "## Completion report (required fields)"),
    "docs/agents/reviewer_conventions.md": ("## Stance", "## Findings", "## Block conditions"),
    "docs/agents/teacher_conventions.md": ("## Stance", "## Grounding sources", "## Isolation"),
}


def _text(relative: str) -> str:
    return (REPO / relative).read_text(encoding="utf-8")


@pytest.mark.parametrize("relative", sorted(ANCHORS))
def test_document_estimate_is_positive_and_under_the_cap(relative):
    estimated = estimate_text_tokens(_text(relative))
    assert estimated > 0, f"{relative}: ESTIMATE is {estimated}"
    assert estimated <= CONVENTIONS_TOKEN_CAP, (
        f"{relative}: ESTIMATE {estimated} tokens (chars/4, never a count) "
        f"exceeds the cap {CONVENTIONS_TOKEN_CAP}"
    )


@pytest.mark.parametrize("relative", sorted(ANCHORS))
def test_document_still_carries_its_headings(relative):
    text = _text(relative)
    for anchor in ANCHORS[relative]:
        assert anchor in text, anchor


def test_reviewer_document_still_lists_six_block_conditions():
    text = _text("docs/agents/reviewer_conventions.md")
    section = text.split("## Block conditions", 1)[1].split("\n## ", 1)[0]
    numbered = [line for line in section.split("\n") if re.match(r"^\d+\. ", line)]
    assert len(numbered) == 6, numbered
