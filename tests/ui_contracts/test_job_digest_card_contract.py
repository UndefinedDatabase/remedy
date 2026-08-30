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


#: The TRIGGER rule's module (F040 T002 part 2).  It is a separate file from
#: `jobDigest.ts` because the envelope and the trigger are two rules, so it gets
#: its own Path rather than widening the one the seam above uses.  The Path is
#: declared here, at the top of the appended region, because the round-7 block's
#: constraint 14 makes the base file's bytes a PREFIX of this one: nothing above
#: this line may move.
VISIBILITY = API_DIR / "digestVisibility.ts"

#: The storage port DECISION F040 D8 rules is DECLARED in the rule module and
#: IMPLEMENTED at the card's edge, never here.
PORT_TYPE_NAME = "DigestVisibilityPort"

#: The exported reason type the card branches on.  It must be a closed union of
#: string literals, so a typo in the card is a type error and not a dead branch.
REASON_TYPE_NAME = "DigestVisibilityReason"

#: The two sentences `docs/roadmap/features/T5_F040.md` Acceptance audits BY
#: NAME.  Neither may appear anywhere in the rule module — the copy belongs to
#: the card, and a phrase sitting in a rule's comment is a phrase waiting to be
#: pasted into a render.
AUDITED_PHRASES = (
    "since you were last here",
    "while you slept",
)


def quoted_literals(text: str) -> list[str]:
    """Every single- and double-quoted literal's CONTENT, read out of source
    whose comments have already been stripped.

    This is the READER that `blank_quoted_literals` is the eraser for: the same
    scan, keeping what the other one throws away, so a literal can be inspected
    rather than only removed.  It is deliberately given comment-stripped input —
    an apostrophe in prose would otherwise open a literal that never closes."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'":
            j = i + 1
            while j < n and text[j] != ch:
                j += 2 if text[j] == "\\" else 1
            out.append(text[i + 1:j])
            i = j + 1
        else:
            i += 1
    return out


def run_state_values() -> list[str]:
    """The `RunState` member values, PARSED out of `packages/core/models.py`.

    Read rather than retyped on purpose: a retyped list produces a guard that
    keeps passing on the day someone adds an eighth state, which is precisely
    the day `digestVisibility.ts` needs revisiting.  `ast` is imported here
    rather than at module scope because the base file's import block is above
    this appended region and may not be edited."""
    import ast

    source = (REPO_ROOT / "packages" / "core" / "models.py").read_text()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ClassDef) and node.name == "RunState":
            return [
                stmt.value.value
                for stmt in node.body
                if isinstance(stmt, ast.Assign)
                and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)
            ]
    return []


class TestTheTriggerRuleIsPureAndPortless:
    """`apps/ui/src/api/digestVisibility.ts`, read as TEXT the same way the seam
    above is, and for the same reason: no renderer exists here, so the
    properties no type-checker can see are pinned by reading the source.

    WHAT EACH MECHANISM CAN AND CANNOT SEE is stated on the test that uses it,
    because a guard whose reach is unstated is a guard whose green is
    unreadable.  Every zero below is paired with a salted positive control, so a
    zero is distinguishable from a search that could never have found anything.
    """

    def test_the_strippers_reach_this_module_as_well(self):
        # The seam's strippers are REUSED, not copied; this is the proof they
        # bite on the new file too, in both directions — the prose goes and the
        # code stays.
        raw = VISIBILITY.read_text()
        promise = "IT KEEPS NO STORAGE"
        assert promise in raw, "the module must keep its written-down absences"
        assert promise not in strip_ts_comments(raw), "stripper must remove it"
        code = code_of(VISIBILITY)
        assert "export function digestVisibility(" in code, (
            "a stripper that ate the code as well would make every assertion "
            "below vacuous"
        )
        assert len(code) > 1000, f"only {len(code)} characters were read"

    def test_the_rule_names_none_of_the_forbidden_capabilities(self):
        # Constraint 8 of the round-7 block. A trigger that read a clock could
        # not be tested without freezing one, and a trigger that reached for
        # storage could not be tested without faking a global.
        executable = executable_of(VISIBILITY)
        for token in FORBIDDEN_CAPABILITIES:
            assert token not in executable, (
                f"{token!r} belongs at the card's edge, not in the rule: "
                f"`nowMs` and the remembered instants arrive as arguments"
            )

    def test_the_capability_scan_can_see_a_capability_in_this_module_too(self):
        for token in FORBIDDEN_CAPABILITIES:
            salted = executable_of_text(f"const leak = {token};\n" + VISIBILITY.read_text())
            assert token in salted, f"the scan cannot see {token!r} even when it is there"

    def test_the_port_is_declared_and_never_implemented(self):
        """The port is a TYPE and nothing more.

        MECHANISM, and it reads the CODE rather than the prose: over
        comment-stripped, literal-blanked source the identifier occurs EXACTLY
        ONCE, and that once is its own `export interface` declaration.  A
        variable annotated with it, a class implementing it, a function
        returning it or a generic parameterised by it would each be a second
        occurrence, so all four are caught by one count.

        WHAT IT CANNOT SEE: TypeScript is STRUCTURALLY typed, so an object
        literal carrying `readDismissal` and `writeDismissal` would satisfy the
        port without ever naming it, and this count would not notice.  That
        residual hole is closed from the other side rather than left open — such
        a twin could not reach real storage without naming `localStorage` or
        `sessionStorage`, and the purity assertion above pins both at zero, so a
        structural twin in this file would be inert by construction."""
        executable = executable_of(VISIBILITY)
        assert re.search(rf"export interface {PORT_TYPE_NAME} \{{", executable), (
            "the port must be DECLARED here, or the card has nothing to bind"
        )
        uses = re.findall(rf"\b{PORT_TYPE_NAME}\b", executable)
        assert len(uses) == 1, (
            f"the port is a type and nothing more; found {len(uses)} occurrences "
            f"of {PORT_TYPE_NAME!r} where only the declaration may stand"
        )
        assert not re.search(r"\bclass\s", executable), (
            "a class in this module would be state with a name on it"
        )
        assert not re.search(r"\bimplements\s", executable)

    def test_the_port_scan_can_see_an_implementation(self):
        # The discriminator for the count above: without it the assertion would
        # pass just as happily over a file that never mentions the port at all.
        implementation = (
            "const livePort: DigestVisibilityPort = {\n"
            "  readDismissal: () => null,\n"
            "  writeDismissal: () => undefined,\n"
            "};\n"
        )
        salted = executable_of_text(VISIBILITY.read_text() + implementation)
        uses = re.findall(rf"\b{PORT_TYPE_NAME}\b", salted)
        assert len(uses) == 2, (
            f"the count cannot see a bound implementation; it read {len(uses)}"
        )

    def test_the_rule_carries_neither_audited_phrase(self):
        # Asserted over RAW source, comments included: the Acceptance names
        # these two sentences, and a rule module that carries one in a comment
        # is one paste away from carrying it in a render.
        raw = VISIBILITY.read_text()
        for phrase in AUDITED_PHRASES:
            assert phrase not in raw, (
                f"{phrase!r} is the CARD's copy; the rule answers a boolean and "
                f"a reason, and the copy audit belongs to the round that writes "
                f"the sentences"
            )

    def test_the_rule_carries_no_user_facing_sentence_at_all(self):
        """No presentation copy of ANY kind, not only the two audited phrases.

        MECHANISM: every quoted literal in the comment-stripped source is a
        TOKEN — a state word, a reason word, an import specifier — and no token
        contains a space.  A user-facing sentence does.

        WHAT IT CANNOT SEE: a sentence assembled from spaceless fragments, and a
        template literal, which `executable_of_text` deliberately leaves intact
        and this reader does not scan.  The module contains no template literal
        today; the salted control below proves the reader sees a plain one."""
        literals = quoted_literals(code_of(VISIBILITY))
        assert literals, "the reader found no literal at all, so it found nothing"
        sentences = [text for text in literals if " " in text]
        assert sentences == [], (
            f"a rule module holds tokens, not sentences; found {sentences}"
        )

    def test_the_sentence_scan_can_see_a_sentence(self):
        salted = strip_ts_comments(
            'const copy = "since you were last here";\n' + VISIBILITY.read_text()
        )
        assert "since you were last here" in quoted_literals(salted), (
            "the reader cannot see a sentence even when one is there"
        )

    def test_the_reason_type_is_a_closed_union_of_string_literals(self):
        code = code_of(VISIBILITY)
        match = re.search(rf"export type {REASON_TYPE_NAME}\s*=([^;]+);", code)
        assert match, f"{REASON_TYPE_NAME} must be exported as its own named type"
        union = match.group(1)
        members = quoted_literals(union)
        assert len(members) >= 4, (
            f"the reason set must at least name the four the block requires; "
            f"found {members}"
        )
        assert "|" in union, "a closed set is a union, not a single alias"
        assert not re.search(r"\bstring\b", union), (
            "a bare `string` reopens the set and makes a typo in the card a "
            "branch that silently never runs"
        )

    def test_the_closed_union_scan_can_see_a_widening(self):
        widened = re.sub(
            rf"export type {REASON_TYPE_NAME}\s*=[^;]+;",
            f"export type {REASON_TYPE_NAME} = string;",
            code_of(VISIBILITY),
        )
        match = re.search(rf"export type {REASON_TYPE_NAME}\s*=([^;]+);", widened)
        assert match and re.search(r"\bstring\b", match.group(1)), (
            "the reader cannot see a widened type even when it is there"
        )

    def test_every_answered_reason_is_a_member_of_the_closed_union(self):
        # `tsc` would also catch this, but the node that runs it SKIPS when
        # `apps/ui/node_modules/.bin/tsc` is absent, so the union is pinned here
        # as well — this guard needs no toolchain at all.
        code = code_of(VISIBILITY)
        match = re.search(rf"export type {REASON_TYPE_NAME}\s*=([^;]+);", code)
        assert match
        members = set(quoted_literals(match.group(1)))
        answered = set(re.findall(r'reason:\s*"([^"]+)"', code))
        assert answered, "the rule must actually answer a reason somewhere"
        assert answered <= members, (
            f"the rule answers {sorted(answered - members)}, which the closed "
            f"union does not contain"
        )

    def test_all_seven_run_states_are_accounted_for_in_the_rule(self):
        """The three-way partition as a PINNED property rather than a paragraph.

        The states are read FROM `packages/core/models.py`, so this fails
        LOUDLY the day someone adds a state to the enum — which is exactly the
        day `digestVisibility.ts` needs revisiting, because an unaccounted
        state falls through to `unknown` and quietly stops showing."""
        states = run_state_values()
        assert len(states) >= 7, (
            f"the parse found only {states}; a reader that returns nothing "
            f"would make the loop below vacuous"
        )
        code = code_of(VISIBILITY)
        missing = [state for state in states if f'"{state}"' not in code]
        assert missing == [], (
            f"{missing} appear in RunState but not in digestVisibility.ts, so "
            f"the rule cannot classify them and would treat them as unknown"
        )

    def test_the_state_check_would_notice_a_state_the_rule_does_not_carry(self):
        # The discriminator: a state the module has never accounted for must NOT
        # be found, or the search above finds everything and pins nothing.
        assert '"quantum-tunnelling"' not in code_of(VISIBILITY)
