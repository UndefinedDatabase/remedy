"""Pin `docs/system/vocabulary.md` against the SHIPPED command catalog.

The vocabulary page is binding (operator order amend0905-vocab-rebuild,
DECISION amend0905-vocab D1), and a binding page that nothing reads drifts
away from the code within one feature. These assertions read the page and
the catalog that `apps/cli/command_catalog.py` exports, and nothing else:
only checked-in files and the imported catalog — no network, no provider
call, no captured help transcript, no child process.

Two of the checks below are MODE-DEPENDENT. They are never skipped: in
planned mode each one asserts the OPPOSITE of what it will assert once
F261 has performed the renames, so the planned mode is a live measurement
of the debt rather than a switched-off test, and the file turns red by
itself on the day the debt is paid and the mode constant has not moved.
"""
from __future__ import annotations

import re
from pathlib import Path

from apps.cli.command_catalog import CATALOG, GROUPS

#: `"planned"` while the catalog still carries the retired words; F261 owns
#: the renames and flips this constant to `"enforced"` in the same feature.
#: It is a plain module constant on purpose — never a skip marker, so that
#: both modes stay measured rather than switched off (T2_F259.md, T003).
VOCABULARY_MODE = "planned"

REPO = Path(__file__).resolve().parents[2]
PAGE = REPO / "docs" / "system" / "vocabulary.md"
#: The feature file holds the authoritative Mermaid block the page copies.
FEATURE = REPO / "docs" / "roadmap" / "features" / "T2_F259.md"

#: The fifteen binding words, in DECISION amend0905-vocab D1's order.
BINDING_WORDS = [
    "Project", "Order", "Mission", "Contract", "Job", "Plan", "Task", "Run",
    "Round", "Worker", "Decision", "Evidence", "Gate", "Verdict", "Roadmap",
]

#: The retired synonyms the enforced mode asserts absent from the catalog.
#: `Worker:` as a role label is DELIBERATELY EXCLUDED: DECISION F259 D3
#: (2026-09-05) measured it as occurring nowhere in the catalog — it lives in
#: report and render code under `packages/` and `apps/` — so a catalog-scoped
#: absence clause for it could not fail for any possible state of this
#: repository. That is the vacuous-gate shape recorded as R-0438. F261 owns
#: the role-label check, because F261 edits those renderers. Do not "restore"
#: `Worker:` here without reversing that decision.
RETIRED_SYNONYMS = [
    "promote", "flight plan", "job-file", "task-file", "loop", "overnight",
]

#: The do-not-confuse table's rows, in page order.
CONFUSION_PAIRS = [
    "Job / Run", "Plan / Roadmap", "Order / Job", "Task / Round",
    "Contract / permissions", "Mission / schedule", "Worker / role",
    "template / order file",
]

#: The rulings copied onto the page, in page order.
PAGE_DECISIONS = [
    "amend0905-vocab D2", "amend0905-vocab D3", "amend0905-vocab D4",
    "amend0905-vocab D5", "amend0905-vocab D6", "amend0905-vocab D7",
    "amend0905-vocab D8", "amend0905-vocab D9", "amend0905-vocab D10",
    "F259 D1", "F259 D2",
]

MERMAID_RE = re.compile(r"^```mermaid\n(.*?)^```", re.S | re.M)
DECISION_HEADING_RE = re.compile(r"^### DECISION (.+)$", re.M)


def _page() -> str:
    return PAGE.read_text(encoding="utf-8")


def _section(heading: str) -> str:
    """The text of one `## <heading>` section, up to the next `## ` heading."""
    text = _page()
    marker = "## " + heading
    start = text.index(marker) + len(marker)
    rest = text[start:]
    end = rest.find("\n## ")
    return rest if end < 0 else rest[:end]


def _first_cells(section: str) -> list[str]:
    """First cell of every DATA row of the single table in `section`.

    The header row and the `|---|` separator are not data; bold markers are
    stripped so a row reads as the word it names.
    """
    cells = []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cell = line.split("|")[1].strip()
        if cell and set(cell) <= set("-: "):
            continue
        cells.append(cell.replace("**", ""))
    return cells[1:]


def _word_rows() -> list[str]:
    return _first_cells(_section("The words"))


def _confusion_rows() -> list[str]:
    return _first_cells(_section("Do not confuse these"))


def _meaning_fragments() -> dict[str, list[str]]:
    """word -> the backticked fragments that count as the page's meaning."""
    fragments: dict[str, list[str]] = {}
    for line in _section("What counts as the meaning").splitlines():
        if not line.startswith("|"):
            continue
        parts = line.split("|")
        word = parts[1].strip().replace("**", "")
        if not word or set(word) <= set("-: ") or word == "Word":
            continue
        fragments[word] = re.findall(r"`([^`]+)`", parts[2])
    return fragments


def _mermaid_body(text: str) -> str:
    """The body of the SINGLE fenced mermaid block in `text`."""
    blocks = MERMAID_RE.findall(text)
    assert len(blocks) == 1, f"expected exactly one mermaid block, found {len(blocks)}"
    return blocks[0]


def _catalog_surfaces() -> list[tuple[str, str]]:
    """(where, text) for the whole catalog surface a description can hide in.

    This is the scope DECISION F259 D3 fixed for the enforced mode, and it
    is stated once, here: every group's id, label and description; every
    command's command_id and description; and every argument's name and
    description. `ArgDef` spells the argument's description `help`; the
    decision calls it a description and this helper is where the two names
    meet. A `where` ending in `:description` IS a description — the
    meaning check below reads only those.
    """
    surfaces: list[tuple[str, str]] = []
    for group in GROUPS.values():
        surfaces.append((f"group:{group.id}:id", group.id))
        surfaces.append((f"group:{group.id}:label", group.label))
        surfaces.append((f"group:{group.id}:description", group.description))
    for entry in CATALOG:
        surfaces.append((f"command:{entry.command_id}:command_id", entry.command_id))
        surfaces.append((f"command:{entry.command_id}:description", entry.description))
        for arg in entry.args:
            surfaces.append((f"arg:{entry.command_id}:{arg.name}:name", arg.name))
            surfaces.append((f"arg:{entry.command_id}:{arg.name}:description", arg.help))
    return surfaces


def _synonym_offenders() -> list[tuple[str, str]]:
    """Sorted (where, synonym) for every catalog surface carrying a retired word."""
    offenders = set()
    for where, text in _catalog_surfaces():
        lowered = text.lower()
        for synonym in RETIRED_SYNONYMS:
            if synonym.lower() in lowered:
                offenders.add((where, synonym))
    return sorted(offenders)


def _is_description(where: str) -> bool:
    return where.endswith(":description")


def _meaning_violations() -> list[tuple[str, str]]:
    """Sorted (where, word) for a description using a word without its meaning."""
    fragments = _meaning_fragments()
    violations = set()
    for where, text in _catalog_surfaces():
        if not _is_description(where):
            continue
        lowered = text.lower()
        for word in BINDING_WORDS:
            if not re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE):
                continue
            if not any(f.lower() in lowered for f in fragments.get(word, [])):
                violations.add((where, word))
    return sorted(violations)


# --- the page, in both modes -------------------------------------------------

def test_the_word_table_carries_the_fifteen_binding_words_in_order():
    assert _word_rows() == BINDING_WORDS


def test_the_do_not_confuse_table_carries_the_eight_pairs_in_order():
    assert _confusion_rows() == CONFUSION_PAIRS


def test_the_pages_mermaid_block_is_byte_equal_to_the_feature_files():
    page_body = _mermaid_body(_page())
    feature_body = _mermaid_body(FEATURE.read_text(encoding="utf-8"))
    assert page_body == feature_body, (
        "the concept diagram drifted between the page and T2_F259.md")


def test_the_page_carries_every_ruling_as_a_decision_heading_in_order():
    headings = [h.split(" (")[0].strip()
                for h in DECISION_HEADING_RE.findall(_page())]
    assert headings == PAGE_DECISIONS


def test_every_binding_word_and_only_those_have_meaning_fragments():
    fragments = _meaning_fragments()
    assert sorted(fragments) == sorted(BINDING_WORDS), (
        "the meaning table must cover exactly the binding words")
    empty = sorted(w for w, f in fragments.items() if not f)
    assert empty == [], f"these words have no meaning fragments: {empty}"


# --- the two mode-dependent checks; neither is ever skipped ------------------

def test_no_retired_synonym_reaches_the_catalog():
    offenders = _synonym_offenders()
    if VOCABULARY_MODE == "enforced":
        assert offenders == [], (
            f"retired vocabulary still reaches the catalog: {offenders}")
    else:
        assert offenders != [], (
            "no catalog surface carries a retired synonym any more — the F261 "
            "renames have landed, so VOCABULARY_MODE must now be 'enforced'")


def test_every_binding_word_in_a_description_carries_the_pages_meaning():
    violations = _meaning_violations()
    if VOCABULARY_MODE == "enforced":
        assert violations == [], (
            f"descriptions use a binding word against the page: {violations}")
    else:
        assert violations != [], (
            "every description now uses its binding words with the page's "
            "meaning — the F261 renames have landed, so VOCABULARY_MODE must "
            "now be 'enforced'")
