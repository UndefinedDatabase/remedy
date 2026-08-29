"""Property tests for F033's rejection→repair renderer.

One test per PROPERTY the renderer turns on, named for the property rather than for the
function that happens to implement it. THE FIRST ONE IS THE ACCEPTANCE MATERIAL:
``docs/roadmap/features/T5_F033.md`` names a "verbatim-quote trace proof" in T003, and
``test_a_reason_of_awkward_bytes_survives_into_the_rendered_text`` is it — an operator's
reason carrying a newline, a backtick, a markdown bullet and surrounding whitespace is
asserted to appear in the rendered bytes as an EXACT SUBSTRING. The assertion is on the
PROPERTY and never on a hand-typed copy of the expected document: a fixture that restates
the whole rendered text passes for the wrong reason the day a heading is improved, and would
have to be retyped by the same hand that would have to notice the reason had been mangled.

The remaining properties, in the order they appear below: two rejections keep the LEDGER's
order rather than a sorted one; approved and pending entries contribute nothing at all; an
empty ledger and an all-approved ledger both render the empty string, which are different
inputs and both legitimate; TOTALITY, DRIVEN rather than asserted — every broken input is
actually passed to the function and its RETURN is what the test reads; and the module's
``Public API::`` block naming every public module-level function it defines, walked from the
module's own AST so the list starts true and stays true.

Ledgers are built by CALLING ``decide_hunk_approval`` and ``build_hunk_ledger`` wherever the
case allows it, so the suite pins the two modules AGREEING rather than this one's reading of
a shape nothing produces. Only the malformed cases hand-build, because production cannot
produce them by design — which is exactly why the renderer's totality has to be driven."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from packages.orchestration import hunk_repair_findings
from packages.orchestration.hunk_approval import HunkRejection, decide_hunk_approval
from packages.orchestration.hunk_ledger import (
    HUNK_LANDING_UNATTEMPTED,
    HUNK_STATE_APPROVED,
    HUNK_STATE_PENDING,
    HUNK_STATE_REJECTED,
    HunkDecisionLedger,
    HunkLedgerEntry,
    build_hunk_ledger,
)
from packages.orchestration.hunk_repair_findings import (
    REJECTION_FINDINGS_ENTRY_PREFIX,
    REJECTION_FINDINGS_HEADING,
    REJECTION_FINDINGS_REASON_INTRO,
    render_rejection_findings,
)

#: An operator's reason built out of every byte a renderer is tempted to tidy: LEADING and
#: TRAILING whitespace, an internal NEWLINE, a BACKTICK, a markdown BULLET and BOLD markers,
#: a TAB, and a run of internal spaces a rewrapper would collapse. Nothing here is decorative
#: — each is one of the reformattings ``hunk_ledger.py`` says this layer does not perform.
AWKWARD_REASON = (
    "  the `re.sub(r'}$', '', s)` call is too greedy\n"
    "  * it eats the **closing brace** of the block below\n"
    "\tand the    run    of    spaces    here is deliberate  "
)


def _ledger_from(known, approved, rejected):
    """A ledger built the way production builds one — through the decision core."""
    decision = decide_hunk_approval(known, approved, rejected)
    return build_hunk_ledger(known, decision)


class TestTheVerbatimTraceProof:
    """T5_F033's Acceptance: "rejected hunks' reasons appear verbatim in the following
    repair prompt". This class is the trace proof it calls acceptance material."""

    def test_a_reason_of_awkward_bytes_survives_into_the_rendered_text(self):
        ledger = _ledger_from(
            ["h1", "h2"], ["h1"], [HunkRejection("h2", AWKWARD_REASON)]
        )
        rendered = render_rejection_findings(ledger)
        assert AWKWARD_REASON in rendered, (
            "the operator's reason did not reach the rendered text unchanged; got "
            f"{rendered!r}")
        assert AWKWARD_REASON.encode("utf-8") in rendered.encode("utf-8"), (
            "the reason survives as characters but not as BYTES")

    def test_the_reason_is_neither_stripped_nor_rewrapped_nor_escaped(self):
        ledger = _ledger_from(["h2"], [], [HunkRejection("h2", AWKWARD_REASON)])
        rendered = render_rejection_findings(ledger)
        # Each clause names ONE reformatting the renderer must not have performed, so a
        # failure says WHICH one happened rather than only that the text differs.
        assert AWKWARD_REASON.strip() not in rendered.replace(AWKWARD_REASON, ""), (
            "a stripped copy of the reason appears beside or instead of the stored one")
        assert "\n" in AWKWARD_REASON and AWKWARD_REASON in rendered, (
            "the reason's internal newline did not survive")
        assert "`" in AWKWARD_REASON and "\\`" not in rendered, (
            "the backtick was escaped")
        assert "    run    of    spaces    " in rendered, (
            "an internal run of spaces was collapsed")
        assert rendered.count(AWKWARD_REASON) == 1, (
            "the reason reached the output more than once, or not at all")

    def test_the_reason_sits_on_its_own_lines_under_the_named_intro(self):
        ledger = _ledger_from(["h2"], [], [HunkRejection("h2", AWKWARD_REASON)])
        rendered = render_rejection_findings(ledger)
        # Matched on the module's NAMES, never on a spelling (the module's own convention).
        assert rendered.startswith(REJECTION_FINDINGS_HEADING)
        marker = REJECTION_FINDINGS_REASON_INTRO + "\n"
        assert marker in rendered
        assert rendered.split(marker, 1)[1].startswith(AWKWARD_REASON), (
            "the reason is not the text directly under its intro line, so something was "
            "inserted between them — an indent, a bullet or a quote character")


class TestEveryRejectionAppearsInTheLedgersOwnOrder:

    def test_two_rejections_both_appear_with_their_own_ids_and_reasons(self):
        ledger = _ledger_from(
            ["zeta-hunk", "alpha-hunk"],
            [],
            [
                HunkRejection("zeta-hunk", "the loop never terminates"),
                HunkRejection("alpha-hunk", "  this import is unused  "),
            ],
        )
        rendered = render_rejection_findings(ledger)
        assert REJECTION_FINDINGS_ENTRY_PREFIX + "zeta-hunk" in rendered
        assert REJECTION_FINDINGS_ENTRY_PREFIX + "alpha-hunk" in rendered
        assert "the loop never terminates" in rendered
        assert "  this import is unused  " in rendered

    def test_the_order_is_the_ledgers_and_not_a_sorted_one(self):
        # The known ids are given in an order whose SORT is the reverse, so a renderer that
        # sorted would be caught. ``build_hunk_ledger`` walks the known list, which is the
        # diff's order, and this asserts the renderer walks the ledger the same way.
        known = ["zeta-hunk", "alpha-hunk"]
        assert sorted(known) != known, "the fixture cannot detect sorting"
        ledger = _ledger_from(
            known,
            [],
            [
                HunkRejection("zeta-hunk", "the loop never terminates"),
                HunkRejection("alpha-hunk", "this import is unused"),
            ],
        )
        rendered = render_rejection_findings(ledger)
        assert rendered.index("the loop never terminates") < rendered.index(
            "this import is unused"), rendered


class TestApprovedAndPendingEntriesContributeNothing:

    def test_a_ledger_of_only_approvals_and_pendings_renders_the_empty_string(self):
        ledger = _ledger_from(["approved-hunk", "pending-hunk"], ["approved-hunk"], [])
        states = {entry.state for entry in ledger.entries}
        assert states == {HUNK_STATE_APPROVED, HUNK_STATE_PENDING}, states
        assert render_rejection_findings(ledger) == ""

    def test_a_mixed_ledger_renders_its_rejections_and_nothing_else(self):
        ledger = _ledger_from(
            ["approved-hunk", "rejected-hunk", "pending-hunk"],
            ["approved-hunk"],
            [HunkRejection("rejected-hunk", "the guard is inverted")],
        )
        rendered = render_rejection_findings(ledger)
        assert "the guard is inverted" in rendered
        assert "rejected-hunk" in rendered
        assert "approved-hunk" not in rendered, (
            "an approved hunk reached the repair prompt; a prompt listing what was accepted "
            "is a different feature")
        assert "pending-hunk" not in rendered, "an undecided hunk reached the repair prompt"


class TestNothingToRepairRendersTheEmptyString:

    def test_an_empty_ledger_renders_the_empty_string(self):
        assert render_rejection_findings(HunkDecisionLedger(())) == ""

    def test_an_all_approved_ledger_renders_the_empty_string(self):
        # A DIFFERENT input from the empty ledger and an equally legitimate one: this
        # feature's edge-case note says a round in which the operator approves everything is
        # valid. Neither may render a heading with nothing under it.
        ledger = _ledger_from(["h1", "h2"], ["h1", "h2"], [])
        assert [entry.state for entry in ledger.entries] == [
            HUNK_STATE_APPROVED, HUNK_STATE_APPROVED]
        assert render_rejection_findings(ledger) == ""


class _BrokenText:
    """An object whose ``__str__`` raises — the id that would take the screen down."""

    def __str__(self):
        raise RuntimeError("this __str__ is broken on purpose")

    def __repr__(self):
        return "<_BrokenText>"


class _EntryWithoutReason:
    """A rejected entry carrying no ``reason`` attribute at all."""

    def __init__(self, hunk_id: str):
        self.hunk_id = hunk_id
        self.state = HUNK_STATE_REJECTED


class _LedgerLike:
    """Anything with an ``entries`` attribute, however unusable that attribute is."""

    def __init__(self, entries):
        self.entries = entries


class _NoEntriesAtAll:
    """An object that is emphatically not a ledger."""


class TestTotalityIsDrivenAndNotMerelyClaimed:
    """Every case below CALLS the function with the broken input and reads its RETURN. A
    totality claim tested only on well-formed input is not tested at all."""

    def test_none_returns_rather_than_raises(self):
        assert render_rejection_findings(None) == ""

    def test_an_object_with_no_entries_returns_rather_than_raises(self):
        assert render_rejection_findings(_NoEntriesAtAll()) == ""

    def test_a_non_iterable_entries_returns_rather_than_raises(self):
        assert render_rejection_findings(_LedgerLike(7)) == ""

    def test_an_entry_missing_its_reason_returns_rather_than_raises(self):
        result = render_rejection_findings(_LedgerLike([_EntryWithoutReason("h1")]))
        assert isinstance(result, str)
        assert result == "", (
            "an unreadable entry produced a PARTIAL block; the module's rule is the empty "
            "string rather than half a repair prompt")

    def test_an_id_whose_str_raises_returns_rather_than_raises(self):
        entry = HunkLedgerEntry(
            _BrokenText(), HUNK_STATE_REJECTED, "the parser is off by one",
            HUNK_LANDING_UNATTEMPTED)
        result = render_rejection_findings(_LedgerLike([entry]))
        assert isinstance(result, str)
        # The COERCION guard earns its place here: the id degrades to its repr and the
        # operator's reason still reaches the repair prompt, which is the outcome that
        # matters. Collapsing the whole block to "" over one strange id would lose it.
        assert "the parser is off by one" in result, result
        assert "<_BrokenText>" in result, result

    def test_a_string_where_a_ledger_belongs_returns_rather_than_raises(self):
        assert render_rejection_findings("not a ledger at all") == ""


class TestTheModuleDocumentsItsWholePublicApi:
    """R-0746 was exactly the defect of a ``Public API::`` block that had stopped naming
    every public function. This guard is that fix applied to the module being born: the list
    is checked by READING IT AGAINST THE MODULE rather than by having been typed once."""

    def test_every_public_module_level_function_is_named_in_the_public_api_block(self):
        source = Path(hunk_repair_findings.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        public = [node.name for node in tree.body
                  if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and not node.name.startswith("_")]
        assert public, "the AST walk found no public function — the guard is vacuous"
        assert "render_rejection_findings" in public, (
            f"the renderer is no longer a public module-level function; the walk found "
            f"{public}")
        block = _public_api_block(ast.get_docstring(tree) or "")
        assert block.strip(), "the module docstring carries no `Public API::` block"
        missing = [name for name in public
                   if not re.search(rf"^\s*{re.escape(name)}\s+—", block, re.M)]
        assert missing == [], (
            "public in hunk_repair_findings.py but absent from its own `Public API::` "
            f"block: {missing}")

    def test_the_named_constants_are_in_the_public_api_block_too(self):
        source = Path(hunk_repair_findings.__file__).read_text(encoding="utf-8")
        block = _public_api_block(ast.get_docstring(ast.parse(source)) or "")
        for name in ("REJECTION_FINDINGS_HEADING", "REJECTION_FINDINGS_ENTRY_PREFIX",
                     "REJECTION_FINDINGS_REASON_INTRO"):
            assert re.search(rf"^\s*{re.escape(name)}\s+—", block, re.M), (
                f"{name} is a public name the module defines but its `Public API::` block "
                "does not name it")


def _public_api_block(docstring: str) -> str:
    """The indented block under ``Public API::`` in a module docstring."""
    lines = docstring.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if line.strip() == "Public API::"), None)
    if start is None:
        return ""
    body: list[str] = []
    for line in lines[start + 1:]:
        if line.strip() and not line.startswith((" ", "\t")):
            break
        body.append(line)
    return "\n".join(body)
