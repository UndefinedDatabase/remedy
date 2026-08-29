"""Contract tests for the completion digest's CLIENT SEAM (F040 T002).

DECISION F040 D7 rules what "component tests" means here: this repository sets
`environment: "node"` in `apps/ui/vitest.config.ts`, ships neither jsdom nor a
testing library, and renders no component in any test — so every decidable rule
of the hero card lives in `apps/ui/src/api/jobDigest.ts` as a pure function
covered by vitest, and the properties no type-checker can see are pinned HERE by
reading that source as TEXT.  This is the shape `test_cost_metric_render.py`,
`test_design_drift.py` and `test_main_layout_guard.py` already establish.

WHY EVERY ABSENCE IS ASSERTED OVER STRIPPED SOURCE, and why that is what makes
this guard honest rather than merely green: `jobDigest.ts` NAMES the four
absences it promises in its own header — it says in prose that it calls no
`fetch`, reads no `Date.now`, keeps no `localStorage` and mints nothing from
`crypto`.  A guard that grepped raw source would find that prose and report the
module's own promise back as a violation, and a guard written to tolerate it
would tolerate the real call too.  So comments are removed before every purity
assertion and quoted literals with them, and the module's own sentences about
what is missing can never stand in for the code that is missing.  Finding R-0584
records the same trap from the other side.  `TestTheStrippersReallyStrip` below
proves the stripping happens rather than assuming it, and every absence is
paired with a positive control so a zero is distinguishable from a blind search.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
API_DIR = UI_SRC / "api"
DIGEST = API_DIR / "jobDigest.ts"
METRIC = API_DIR / "costMetric.ts"
BAR = UI_SRC / "components" / "metrics" / "TopMetricsBar.tsx"

#: Every capability constraint 10 of the R6 block forbids this module.  A card
#: rule that read a clock could not be tested without freezing one, a rule that
#: kept storage would answer differently on the second call, and a rule that
#: opened a socket would be a second door beside the one `remedyApi.ts` owns.
FORBIDDEN_CAPABILITIES = (
    "fetch",
    "Date.now",
    "new Date",
    "localStorage",
    "sessionStorage",
    "crypto",
    "XMLHttpRequest",
)

#: The one string that means a cost figure is not an estimate.  It has exactly
#: one home in this client and `costMetric.ts` is it.
EXACTNESS_LITERAL = '"actual"'

#: The presentation copy that renders an estimate.  `TopMetricsBar.tsx` owns
#: both as named constants; a second copy anywhere else is the drift this
#: feature keeps paying to avoid.
ESTIMATE_PHRASE_TEXT = ", estimated"
ESTIMATE_MARK_TEXT = "~"


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments, so an assertion reads the code rather than
    the prose about the code."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def blank_quoted_literals(text: str) -> str:
    """Empty every single- and double-quoted literal, keeping its quotes, so an
    import specifier or a route fragment cannot be read as a capability."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'":
            j = i + 1
            while j < n and text[j] != ch:
                j += 2 if text[j] == "\\" else 1
            out.append(ch + ch)
            i = j + 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def code_of(path: Path) -> str:
    """The comment-stripped source."""
    return strip_ts_comments(path.read_text())


def executable_of_text(text: str) -> str:
    """The comment-stripped, literal-blanked source held in memory: what the
    module actually executes, with both places prose can hide removed.  Template
    literals are left intact on purpose, the same choice
    `test_cost_metric_render.py` makes — blanking them would HIDE a call rather
    than exclude one."""
    return blank_quoted_literals(strip_ts_comments(text))


def executable_of(path: Path) -> str:
    """`executable_of_text` over a file on disk."""
    return executable_of_text(path.read_text())


def api_sources() -> list[Path]:
    """Every shipped `.ts` under `apps/ui/src/api/`.  Test files are excluded
    because a fixture naming a wire value is describing the payload, not
    deciding anything from it."""
    return sorted(
        path for path in API_DIR.glob("*.ts")
        if not path.name.endswith(".test.ts")
    )


class TestTheStrippersReallyStrip:
    """Without these, every absence below could be a stripper that ate the file."""

    def test_the_comment_stripper_removes_a_comment_the_module_really_carries(self):
        raw = DIGEST.read_text()
        promise = "IT OPENS NO SOCKET"
        assert promise in raw, "the module must keep its written-down absences"
        assert promise not in strip_ts_comments(raw), "stripper must remove it"

    def test_the_comment_stripper_leaves_the_code_around_the_comment(self):
        code = code_of(DIGEST)
        assert "export function decodeJobDigest(" in code, (
            "a stripper that ate the code as well would make every assertion "
            "below vacuous"
        )
        assert "export function jobDigestPath(" in code
        assert "export function digestCostLine(" in code

    def test_the_literal_blanker_empties_a_literal_the_module_really_carries(self):
        code = code_of(DIGEST)
        assert '"./costMetric"' in code, "the import specifier is a real literal here"
        assert '"./costMetric"' not in blank_quoted_literals(code), (
            "blanker must empty it"
        )

    def test_the_capability_scan_can_actually_see_a_capability(self):
        # The salted copy is the discriminator: a scan that cannot go red over
        # a real call proves nothing when it comes back green over the shipped
        # file (the vacuous-absence trap R-0559 records).
        for token in FORBIDDEN_CAPABILITIES:
            salted = executable_of_text(f"const leak = {token};\n" + DIGEST.read_text())
            assert token in salted, f"the scan cannot see {token!r} even when it is there"


class TestTheDigestSeamIsPure:
    """Constraint 10 of the round-6 block, and the reason the seam is testable
    at all: a pure rule needs no renderer, no clock and no network."""

    def test_the_module_names_none_of_the_forbidden_capabilities(self):
        executable = executable_of(DIGEST)
        for token in FORBIDDEN_CAPABILITIES:
            assert token not in executable, (
                f"{token!r} would make the card's rules untestable without "
                f"faking it, and the trigger rule that needs a clock takes "
                f"`nowMs` as a parameter instead"
            )

    def test_the_module_promises_those_absences_in_prose_as_well(self):
        # AGENTS.md asks that deliberate absences be documented where a reader
        # would search for them. The prose is what the stripping above exists to
        # keep OUT of the assertion, so its presence is checked separately.
        raw = DIGEST.read_text()
        for token in ("Date.now", "localStorage", "fetch", "crypto"):
            assert token in raw, (
                f"the header must name {token!r} as a deliberate absence, or a "
                f"reader searching for it finds nothing at all"
            )

    def test_the_path_builder_returns_a_url_and_does_not_walk_it(self):
        executable = executable_of(DIGEST)
        assert "export function jobDigestPath(" in executable
        assert "async " not in executable, (
            "a loader belongs beside the path builder, never inside it — the "
            "shape `loadDiffEnvelope` and `diffEnvelopePath` already establish"
        )
        assert "await " not in executable


class TestTheExactnessStringHasOneHome:
    def test_the_digest_seam_never_restates_the_literal(self):
        assert EXACTNESS_LITERAL not in code_of(DIGEST), (
            "a second copy of the exactness string is the drift DECISION F040 "
            "D2 already spent a round preventing for the urgency formula"
        )

    def test_the_search_reaches_the_file_at_all(self):
        # The POSITIVE CONTROL for the zero above: without it the assertion
        # would pass just as happily over an empty read.
        code = code_of(DIGEST)
        assert "export const JOB_DIGEST_VERSION" in code
        assert "export interface JobDigest {" in code
        assert len(code) > 1000, f"only {len(code)} characters were read"

    def test_the_digest_seam_imports_the_constant_instead(self):
        code = code_of(DIGEST)
        assert re.search(
            r'import\s*\{[^}]*\bACTUAL_BASIS\b[^}]*\}\s*from\s*"\./costMetric";',
            code,
        ), "the basis must be IMPORTED from its one home, not redeclared"
        assert "ACTUAL_BASIS" in executable_of(DIGEST), (
            "the imported constant must be USED, or the import is decoration"
        )

    def test_the_literal_has_exactly_one_home_in_the_whole_api_directory(self):
        homes = {
            path.name: code_of(path).count(EXACTNESS_LITERAL)
            for path in api_sources()
        }
        naming = sorted(name for name, hits in homes.items() if hits)
        assert naming == ["costMetric.ts"], (
            f"exactly one module may name the exactness string; found {naming}"
        )
        assert homes["costMetric.ts"] == 1, (
            f"and it may name it once, not {homes['costMetric.ts']} times"
        )

    def test_the_directory_sweep_really_read_the_directory(self):
        scanned = [path.name for path in api_sources()]
        assert "jobDigest.ts" in scanned
        assert "costMetric.ts" in scanned
        assert "recency.ts" in scanned
        assert not any(name.endswith(".test.ts") for name in scanned)
        assert len(scanned) > 20, f"the sweep collected only {len(scanned)} files"

    def test_the_one_home_still_exports_it(self):
        assert 'export const ACTUAL_BASIS = "actual";' in code_of(METRIC), (
            "the bar and the hero card read the same binding, so the home must "
            "export it rather than keep it private"
        )


class TestTheSeamWritesNoPresentationCopy:
    """`costMetric.ts` returns an `estimated` BOOLEAN and the component owns the
    words.  The digest seam does the same, one layer up, or the phrase gains a
    second home the moment the hero card is written."""

    def test_the_seam_contains_neither_the_phrase_nor_the_marker(self):
        code = code_of(DIGEST)
        assert ESTIMATE_PHRASE_TEXT not in code, (
            "the estimate phrase belongs to TopMetricsBar.tsx as ESTIMATE_PHRASE"
        )
        assert ESTIMATE_MARK_TEXT not in code, (
            "the estimate marker belongs to TopMetricsBar.tsx as ESTIMATE_MARK"
        )

    def test_the_seam_answers_a_boolean_instead(self):
        code = code_of(DIGEST)
        assert "estimated: boolean" in code, (
            "the cost line reports exactness as a flag, the way CostMetricView "
            "does, so the words stay where they already live"
        )

    def test_the_component_still_owns_both_constants(self):
        # Paired with the two zeros above so the guard fails if the copy MOVES
        # rather than silently passing once it is gone from both files.
        code = code_of(BAR)
        assert 'const ESTIMATE_MARK = "~";' in code, (
            "the marker's one home is this component; if it moved, the zeros "
            "above stopped meaning anything"
        )
        assert 'const ESTIMATE_PHRASE = ", estimated";' in code, (
            "and so is the phrase's"
        )
