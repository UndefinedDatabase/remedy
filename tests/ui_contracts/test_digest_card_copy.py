"""Contract tests for the completion digest's CARD COPY RULES (F040 T002).

DECISION F040 D7 rules what "component tests" means in this repository: it sets
`environment: "node"` in `apps/ui/vitest.config.ts`, ships neither jsdom nor a
testing library and renders no component in any test, so every decidable rule of
the hero card lives in a pure module under `apps/ui/src/api/` and the properties
no type-checker can see are pinned HERE by reading that source as TEXT.  This is
the shape `test_job_digest_card_contract.py` already establishes for the
envelope and the trigger; `digestCardCopy.test.ts` grades the SENTENCES, and
this file grades the module's SHAPE.

WHY EVERY ABSENCE IS ASSERTED OVER STRIPPED SOURCE.  `digestCardCopy.ts` NAMES
the four capabilities it promises to avoid in its own header — it says in prose
that it calls no `fetch`, reads no `Date.now`, keeps no `localStorage` and mints
nothing from `crypto`.  A guard that grepped raw source would find that prose
and report the module's own promise back as a violation, and a guard written to
tolerate the prose would tolerate the real call too.  So comments are removed
before every purity assertion and quoted literals with them, every absence is
paired with a salted positive control, and `TestTheStrippersReallyStrip` proves
the stripping happens rather than assuming it.  Finding R-0584 records the same
trap from the other side.

WHAT THIS FILE PINS THAT NOTHING ELSE CAN.  DECISION F040 D10 rules that the
card shows the server's words with the report's markup taken out and rewrites
nothing, and that the §17 screen keeps ONE home in `apps/ui/src/copy/
humanCopy.ts`.  Both are architectural rather than behavioural: vitest can prove
that a sentence comes out clean, but only a reader of the source can prove that
it came out clean because the shared screen was applied rather than because a
second copy of the word list was pasted in here.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
API_DIR = UI_SRC / "api"
COPY = API_DIR / "digestCardCopy.ts"
HUMAN_COPY = UI_SRC / "copy" / "humanCopy.ts"
MODELS = REPO_ROOT / "packages" / "core" / "models.py"
RUN_REPORT = REPO_ROOT / "packages" / "orchestration" / "run_report.py"

#: Every capability constraint 8 of the R9 block forbids this module.  A copy
#: rule that read a clock would answer differently on the second call, one that
#: kept storage would carry a sentence between two jobs, and one that opened a
#: socket would be a second door beside the one `remedyApi.ts` owns.
FORBIDDEN_CAPABILITIES = (
    "fetch",
    "Date.now",
    "new Date",
    "localStorage",
    "sessionStorage",
    "crypto",
    "XMLHttpRequest",
)

#: The wrong-vocabulary trap.  `humanCopy.stateLabel` answers the CHECKLIST's
#: words — `done`, `current`, `blocked`, `suggested` — and `RunState` shares none
#: of those spellings, so it would answer "Planned" for six of the seven digest
#: states.  It is not a near miss; it is the wrong function, and a later edit
#: reaching for it by name is what this constant exists to catch.
WRONG_STATE_LABEL_IMPORT = "stateLabel"

#: The exported name that closes the CTA rule set.
RULE_IDS_NAME = "DIGEST_CTA_RULE_IDS"


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
    import specifier or a state word cannot be read as a capability."""
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


def quoted_literals(text: str) -> list[str]:
    """Every single- and double-quoted literal's CONTENT, read out of source
    whose comments have already been stripped.  The READER that
    `blank_quoted_literals` is the eraser for."""
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


def code_of(path: Path) -> str:
    """The comment-stripped source."""
    return strip_ts_comments(path.read_text())


def executable_of_text(text: str) -> str:
    """The comment-stripped, literal-blanked source held in memory: what the
    module actually executes, with both places prose can hide removed.  Template
    literals are left intact on purpose, the same choice the sibling guards
    make — blanking them would HIDE a call rather than exclude one."""
    return blank_quoted_literals(strip_ts_comments(text))


def executable_of(path: Path) -> str:
    """`executable_of_text` over a file on disk."""
    return executable_of_text(path.read_text())


def forbidden_words() -> list[str]:
    """The §17 word list, PARSED out of `humanCopy.ts` rather than retyped.

    Retyping it here would be the very duplication this file exists to forbid:
    the guard would then hold a second copy of the list while asserting that the
    module under test holds none."""
    match = re.search(r"const forbidden\s*=\s*\[(.*?)\];", code_of(HUMAN_COPY), re.S)
    assert match, "humanCopy.ts must still declare the forbidden-word list"
    return quoted_literals(match.group(1))


def run_state_values() -> list[str]:
    """The `RunState` member values, PARSED out of `packages/core/models.py`.

    Read rather than retyped on purpose: a retyped list produces a guard that
    keeps passing on the day someone adds an eighth state, which is precisely
    the day `digestCardCopy.ts` needs revisiting, because an unaccounted state
    falls through to the missing-value phrase and quietly stops being named."""
    source = MODELS.read_text()
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


def next_action_rule_ids() -> list[str]:
    """Every `NextAction("<id>", …)` rule id, PARSED out of `run_report.py`.

    Read with `ast` rather than by grep so a call split across lines — which
    `stopped-by-operator` is — is found by the same mechanism as the others, and
    so a rule id appearing in a docstring is not mistaken for a rule."""
    source = RUN_REPORT.read_text()
    ids: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "NextAction"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)):
            ids.append(node.args[0].value)
    return ids


def declared_rule_ids() -> list[str]:
    """The ids the module's closed tuple names, read out of the declaration."""
    match = re.search(
        rf"export const {RULE_IDS_NAME}\s*=\s*\[(.*?)\]\s*as const;",
        code_of(COPY),
        re.S,
    )
    assert match, f"{RULE_IDS_NAME} must be a closed readonly tuple"
    return quoted_literals(match.group(1))


class TestTheStrippersReallyStrip:
    """Without these, every absence below could be a stripper that ate the file."""

    def test_the_comment_stripper_removes_a_comment_the_module_really_carries(self):
        raw = COPY.read_text()
        promise = "IT OPENS NO SOCKET"
        assert promise in raw, "the module must keep its written-down absences"
        assert promise not in strip_ts_comments(raw), "stripper must remove it"

    def test_the_comment_stripper_leaves_the_code_around_the_comment(self):
        code = code_of(COPY)
        assert "export function digestStateLabel(" in code, (
            "a stripper that ate the code as well would make every assertion "
            "below vacuous"
        )
        assert "export function digestCtaText(" in code
        assert f"export const {RULE_IDS_NAME}" in code
        assert len(code) > 1000, f"only {len(code)} characters were read"

    def test_the_literal_blanker_empties_a_literal_the_module_really_carries(self):
        code = code_of(COPY)
        assert '"../copy/humanCopy"' in code, "the import specifier is a real literal"
        assert '"../copy/humanCopy"' not in blank_quoted_literals(code), (
            "blanker must empty it"
        )

    def test_the_literal_reader_finds_the_literals_the_blanker_erases(self):
        literals = quoted_literals(code_of(COPY))
        assert "../copy/humanCopy" in literals
        assert "open-decision" in literals


class TestTheCopyRulesArePure:
    """Constraint 8 of the round-9 block, and the reason the rules are testable
    at all: a pure rule needs no renderer, no clock and no network."""

    def test_the_module_names_none_of_the_forbidden_capabilities(self):
        executable = executable_of(COPY)
        for token in FORBIDDEN_CAPABILITIES:
            assert token not in executable, (
                f"{token!r} would make the copy rules untestable without faking "
                f"it, and copy is a function of its label and nothing else"
            )

    def test_the_capability_scan_can_actually_see_a_capability(self):
        # The salted copy is the discriminator: a scan that cannot go red over a
        # real call proves nothing when it comes back green over the shipped
        # file (the vacuous-absence trap R-0559 records).
        for token in FORBIDDEN_CAPABILITIES:
            salted = executable_of_text(f"const leak = {token};\n" + COPY.read_text())
            assert token in salted, f"the scan cannot see {token!r} even when it is there"

    def test_the_module_promises_those_absences_in_prose_as_well(self):
        # AGENTS.md asks that deliberate absences be documented where a reader
        # would search for them. The prose is what the stripping above exists to
        # keep OUT of the assertion, so its presence is checked separately.
        raw = COPY.read_text()
        for token in ("Date.now", "localStorage", "fetch", "crypto"):
            assert token in raw, (
                f"the header must name {token!r} as a deliberate absence, or a "
                f"reader searching for it finds nothing at all"
            )


class TestTheScreenHasOneHome:
    """DECISION F040 D10 keeps §17's word list, the whole-value identifier test
    and the length cap in `humanCopy.ts`.  This module applies that screen; it
    does not own a second copy of it."""

    def test_the_module_imports_the_screen_from_its_one_home(self):
        code = code_of(COPY)
        assert re.search(
            r'import\s*\{[^}]*\bscrubUiText\b[^}]*\}\s*from\s*"\.\./copy/humanCopy";',
            code,
        ), "the §17 screen must be IMPORTED from its one home, not reimplemented"
        assert "scrubUiText" in executable_of(COPY), (
            "the imported screen must be USED, or the import is decoration"
        )

    def test_the_import_scan_would_notice_the_import_going_away(self):
        # The discriminator for the assertion above: with the import line gone
        # the search must fail, or it was never reading the import at all.
        without = re.sub(
            r'import\s*\{[^}]*\}\s*from\s*"\.\./copy/humanCopy";', "", code_of(COPY))
        assert not re.search(
            r'import\s*\{[^}]*\bscrubUiText\b[^}]*\}\s*from\s*"\.\./copy/humanCopy";',
            without,
        ), "the reader cannot see the import going away"

    def test_the_word_list_is_not_restated_here(self):
        """At most ONE of `humanCopy`'s forbidden words may appear as a literal.

        MECHANISM: the list is PARSED out of `humanCopy.ts` and matched against
        the quoted literals of this module's comment-stripped source.  One is
        tolerated because a single word could legitimately turn up inside a
        sentence; two or more is a copy of the list, however it is spelled.

        WHAT IT CANNOT SEE: a paraphrase of the list, or the list assembled from
        fragments.  Neither would function as a screen, because `scrubUiText`
        matches the words literally."""
        words = forbidden_words()
        assert len(words) >= 10, (
            f"the parse found only {words}; a reader that returns almost "
            f"nothing would make the count below vacuous"
        )
        literals = quoted_literals(code_of(COPY))
        restated = sorted({word for word in words if word in literals})
        assert len(restated) <= 1, (
            f"the §17 word list has one home and this file is not it; found "
            f"{restated} restated as literals here"
        )

    def test_the_restatement_scan_can_see_a_restated_list(self):
        # The discriminator: without it the count above would pass just as
        # happily over a file the reader could never have read.
        words = forbidden_words()
        salted = strip_ts_comments(
            "const copied = [\n"
            + "".join(f'  "{word}",\n' for word in words[:4])
            + "];\n"
            + COPY.read_text()
        )
        literals = quoted_literals(salted)
        restated = sorted({word for word in words if word in literals})
        assert len(restated) >= 4, (
            f"the scan cannot see a restated list even when one is there; it "
            f"found {restated}"
        )

    def test_the_module_declares_no_word_list_of_its_own(self):
        executable = executable_of(COPY)
        assert not re.search(r"\bforbidden\b", executable), (
            "a `forbidden` binding here would be the second home the whole "
            "decision exists to prevent"
        )

    def test_the_one_home_still_owns_the_list_and_the_screen(self):
        # Paired with the zeros above so the guard fails if the list MOVES
        # rather than silently passing once it is gone from both files.
        code = code_of(HUMAN_COPY)
        assert "const forbidden = [" in code
        assert "export function scrubUiText(" in code


class TestTheWrongStateLabelIsNotReachedFor:
    """`humanCopy.stateLabel` answers the checklist's vocabulary.  Reaching for
    it here would silently render "Planned" for six of the seven digest states,
    which no type-checker and no vitest assertion over this module would see."""

    def test_the_checklist_state_label_is_not_imported(self):
        code = code_of(COPY)
        imports = re.findall(r'import\s*\{([^}]*)\}\s*from\s*"[^"]*humanCopy";', code)
        assert imports, "the module must import something from humanCopy"
        names = {name.strip() for group in imports for name in group.split(",")}
        assert WRONG_STATE_LABEL_IMPORT not in names, (
            f"{WRONG_STATE_LABEL_IMPORT!r} answers the checklist's vocabulary — "
            f"`done`, `current`, `blocked`, `suggested` — and would render "
            f"'Planned' for every RunState value"
        )
        assert "scrubUiText" in names

    def test_the_import_reader_would_see_it_if_it_were_reached_for(self):
        salted = code_of(COPY).replace(
            'import { scrubUiText } from "../copy/humanCopy";',
            'import { scrubUiText, stateLabel } from "../copy/humanCopy";',
        )
        imports = re.findall(r'import\s*\{([^}]*)\}\s*from\s*"[^"]*humanCopy";', salted)
        names = {name.strip() for group in imports for name in group.split(",")}
        assert WRONG_STATE_LABEL_IMPORT in names, (
            "the reader cannot see the wrong import even when it is there"
        )

    def test_the_trap_is_written_down_where_a_reader_would_reach_for_it(self):
        raw = COPY.read_text()
        assert WRONG_STATE_LABEL_IMPORT in raw, (
            "the module must NAME the function it refuses to use, or the next "
            "reader reaches for it and finds nothing warning them off"
        )


class TestEveryRuleIdIsAccountedFor:
    """A sixth rule added to `recommended_next_action` reddens this class, which
    is the point: the client cannot bind an affordance to a rule it has never
    heard of, and the wire carries the id as a bare string."""

    def test_the_report_still_returns_five_rules(self):
        ids = next_action_rule_ids()
        assert len(ids) == 5, (
            f"the parse read {ids}; a reader that returns nothing would make "
            f"the assertion below vacuous"
        )
        assert len(set(ids)) == 5, f"the report's rule ids must be distinct; {ids}"

    def test_every_reported_rule_id_appears_in_the_closed_tuple(self):
        listed = declared_rule_ids()
        missing = [rule_id for rule_id in next_action_rule_ids() if rule_id not in listed]
        assert missing == [], (
            f"{missing} are returned by recommended_next_action but absent from "
            f"{RULE_IDS_NAME}, so the card could not branch on them"
        )

    def test_the_tuple_invents_no_rule_the_report_never_returns(self):
        reported = set(next_action_rule_ids())
        invented = [rule_id for rule_id in declared_rule_ids() if rule_id not in reported]
        assert invented == [], (
            f"{invented} appear in {RULE_IDS_NAME} but no rule emits them"
        )

    def test_the_rule_id_reader_would_notice_a_missing_entry(self):
        # The discriminator: drop one id from the declaration and the comparison
        # must fail, or it is comparing something other than what it claims.
        listed = declared_rule_ids()
        shortened = listed[1:]
        missing = [rule_id for rule_id in next_action_rule_ids() if rule_id not in shortened]
        assert missing == [listed[0]], (
            f"the reader cannot see a dropped rule id; it found {missing}"
        )


class TestEveryRunStateIsAccountedFor:
    """The states are read FROM `packages/core/models.py`, so this fails LOUDLY
    the day someone adds a state to the enum — which is exactly the day
    `digestCardCopy.ts` needs revisiting, because an unaccounted state falls
    through to the missing-value phrase and stops being named at all."""

    def test_all_seven_run_states_are_named_by_the_label_map(self):
        states = run_state_values()
        assert len(states) >= 7, (
            f"the parse found only {states}; a reader that returns nothing "
            f"would make the loop below vacuous"
        )
        code = code_of(COPY)
        missing = [state for state in states if f'"{state}"' not in code]
        assert missing == [], (
            f"{missing} appear in RunState but not in digestCardCopy.ts, so the "
            f"card would show the missing-value phrase for a real state"
        )

    def test_the_state_check_would_notice_a_state_the_module_does_not_carry(self):
        # The discriminator: a state the module has never accounted for must NOT
        # be found, or the search above finds everything and pins nothing.
        assert '"quantum-tunnelling"' not in code_of(COPY)

    def test_the_label_map_answers_a_phrase_for_an_unreadable_state(self):
        code = code_of(COPY)
        assert "UNREADABLE_STATE_LABEL" in code, (
            "an unknown state must land on a named phrase rather than being "
            "passed through raw, which §17 forbids"
        )
