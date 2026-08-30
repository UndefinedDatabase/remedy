"""Contract tests for the completion digest's HERO CARD COMPONENT (F040 T002).

DECISION F040 D7 rules what "component tests" means in this repository:
`apps/ui/vitest.config.ts` sets `environment: "node"`, includes
`src/**/*.test.ts` only, and the package ships neither jsdom nor a testing
library, so `DigestHeroCard.tsx` is neither collected by vitest nor renderable
by it. Its colour is THIS file: a pytest text guard that reads the component's
source and pins the properties a type-checker cannot see, the same shape
`test_digest_card_copy.py` already establishes for the copy module one file
over. This file does not import anything from that sibling — the helpers below
are short, and a shared import would couple two guards that should each stay
readable and breakable on their own.

WHY EVERY ABSENCE IS ASSERTED OVER STRIPPED, LITERAL-BLANKED SOURCE. The
component's own header names the capabilities it promises not to use — it says
in prose that it opens no socket, keeps no storage and reads no clock except at
one edge. A guard that grepped raw source would find that prose and report the
component's own promise back as a violation, so comments are stripped and
quoted literals are blanked before any absence is asserted, and every absence
claim is paired with a salted positive control proving the scan can see the
thing when it is really there — the vacuous-absence trap R-0559 records.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
CARD = UI_SRC / "components" / "digest" / "DigestHeroCard.tsx"
CSS = UI_SRC / "components" / "digest" / "DigestHeroCard.module.css"
COPY = UI_SRC / "api" / "digestCardCopy.ts"
TMB = UI_SRC / "components" / "metrics" / "TopMetricsBar.tsx"

#: Constraint 7 of the round-11 block: the card reads no clock except at the
#: dismissal, and it reads no storage at all. These four must occur zero times
#: in the component's executable source.
FORBIDDEN_CAPABILITIES = ("localStorage", "sessionStorage", "fetch", "XMLHttpRequest")


def strip_ts_comments(text: str) -> str:
    """Drop `//` and `/* */` comments, so an assertion reads the code rather
    than the prose about the code."""
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
    import specifier or a copied phrase cannot be read as a capability."""
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
    whose comments have already been stripped. The reader that
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
    """Comment-stripped, literal-blanked source held in memory: what the module
    actually executes, with both places prose can hide removed."""
    return blank_quoted_literals(strip_ts_comments(text))


def executable_of(path: Path) -> str:
    """`executable_of_text` over a file on disk."""
    return executable_of_text(path.read_text())


def imported_names(code: str, module_suffix: str) -> set[str]:
    """Every name pulled from an `import { ... } from "...<module_suffix>";`
    statement (type or value import), unioned across every such statement in
    `code`. Read this way rather than by a single regex per module so two
    imports from the same specifier — a `import type` and a plain `import` —
    are both seen."""
    names: set[str] = set()
    for m in re.finditer(r'import\s+(?:type\s+)?\{([^}]*)\}\s*from\s*"([^"]*)";', code):
        if m.group(2).endswith(module_suffix):
            names.update(n.strip() for n in m.group(1).split(","))
    return names


def digest_state_phrases() -> list[str]:
    """The seven `RunState` label PHRASES, PARSED out of `DIGEST_STATE_LABELS`
    in `digestCardCopy.ts` rather than retyped — a retyped list would be a
    second home for exactly the words this guard exists to keep singly-owned."""
    code = code_of(COPY)
    match = re.search(r"const DIGEST_STATE_LABELS[^=]*=\s*\{(.*?)\};", code, re.S)
    assert match, "digestCardCopy.ts must still declare DIGEST_STATE_LABELS"
    phrases = re.findall(r'"[^"]*"\s*:\s*"([^"]*)"', match.group(1))
    return phrases


def estimate_tokens() -> tuple[str, str]:
    """`ESTIMATE_MARK` and `ESTIMATE_PHRASE`, PARSED out of `TopMetricsBar.tsx`
    rather than retyped, so this file cannot drift from the one home G5 also
    checks against."""
    code = code_of(TMB)
    mark = re.search(r'export const ESTIMATE_MARK\s*=\s*"([^"]*)";', code)
    phrase = re.search(r'export const ESTIMATE_PHRASE\s*=\s*"([^"]*)";', code)
    assert mark and phrase, "TopMetricsBar.tsx must still export both constants"
    return mark.group(1), phrase.group(1)


def css_class_names() -> set[str]:
    """Every class `DigestHeroCard.module.css` declares at its top level,
    PARSED out of the sheet rather than retyped, so a renamed class fails the
    reference check below instead of the guard silently agreeing with itself.
    Read-only: constraint 6 keeps the sheet out of this round's change set."""
    css = re.sub(r"/\*.*?\*/", "", CSS.read_text(), flags=re.S)
    return set(re.findall(r"^\.([A-Za-z_][\w-]*)\s*\{", css, re.M))


class TestTheStrippersReallyStrip:
    """Without these, every absence below could be a stripper that ate the
    file rather than one that read it."""

    def test_the_comment_stripper_removes_a_comment_the_component_really_carries(self):
        raw = CARD.read_text()
        promise = "IT OPENS NO SOCKET"
        assert promise in raw, "the component must keep its written-down absences"
        assert promise not in strip_ts_comments(raw), "stripper must remove it"

    def test_the_comment_stripper_leaves_the_code_around_the_comment(self):
        code = code_of(CARD)
        assert "export function DigestHeroCard(" in code, (
            "a stripper that ate the code as well would make every assertion "
            "below vacuous"
        )
        assert "port.writeDismissal(" in code
        assert len(code) > 500, f"only {len(code)} characters were read"

    def test_the_literal_blanker_empties_a_literal_the_component_really_carries(self):
        code = code_of(CARD)
        assert '"../../api/jobDigest"' in code, "the import specifier is a real literal"
        assert '"../../api/jobDigest"' not in blank_quoted_literals(code), (
            "blanker must empty it"
        )

    def test_the_literal_reader_finds_the_literals_the_blanker_erases(self):
        literals = quoted_literals(code_of(CARD))
        assert "../../api/jobDigest" in literals


class TestTheCardIsTheEdgeAndNothingMore:
    """SPEC item 1. Constraint 7 of the round-11 block: `Date.now()` is called
    in exactly one place — the dismiss handler, the edge DECISION F040 D8
    names — and every persisted read or write goes through the injected
    `DigestVisibilityPort`."""

    def test_the_component_calls_none_of_the_forbidden_capabilities(self):
        executable = executable_of(CARD)
        for token in FORBIDDEN_CAPABILITIES:
            assert token not in executable, (
                f"{token!r} would make the component a second storage or "
                f"network edge, which DECISION F040 D8 reserves for the port"
            )

    def test_the_capability_scan_can_actually_see_a_capability(self):
        # The salted copy is the discriminator: a scan that cannot go red over
        # a real call proves nothing when it comes back green over the shipped
        # file.
        for token in FORBIDDEN_CAPABILITIES:
            salted = executable_of_text(f"const leak = {token};\n" + CARD.read_text())
            assert token in salted, f"the scan cannot see {token!r} even when it is there"

    def test_date_now_is_called_exactly_once(self):
        executable = executable_of(CARD)
        assert executable.count("Date.now") == 1, (
            "Date.now must be read at exactly one edge, the dismiss handler"
        )

    def test_write_dismissal_is_called(self):
        executable = executable_of(CARD)
        assert "writeDismissal" in executable, (
            "a dismissal must be persisted through the injected port"
        )


class TestNoRuleHasASecondHome:
    """SPEC item 2. None of the seven `RunState` phrases, and neither the
    estimate mark nor the estimate phrase, may be restated as a literal here."""

    def test_no_run_state_phrase_is_restated_as_a_literal(self):
        phrases = digest_state_phrases()
        assert len(phrases) == 7, (
            f"the parse found only {phrases}; a reader that returns almost "
            f"nothing would make the loop below vacuous"
        )
        literals = quoted_literals(code_of(CARD))
        restated = [p for p in phrases if p in literals]
        assert restated == [], (
            f"the state phrases have one home, digestCardCopy.ts, and this "
            f"file is not it; found {restated} restated as literals here"
        )

    def test_the_phrase_restatement_scan_can_see_a_restated_phrase(self):
        phrases = digest_state_phrases()
        salted = strip_ts_comments(f'const leak = "{phrases[0]}";\n' + CARD.read_text())
        literals = quoted_literals(salted)
        assert phrases[0] in literals, "the scan cannot see a restated phrase even when it is there"

    def test_neither_estimate_token_is_restated_as_a_literal(self):
        mark, phrase = estimate_tokens()
        literals = quoted_literals(code_of(CARD))
        assert mark not in literals, f"{mark!r} has one home, TopMetricsBar.tsx"
        assert phrase not in literals, f"{phrase!r} has one home, TopMetricsBar.tsx"

    def test_the_estimate_restatement_scan_can_see_a_restated_token(self):
        mark, phrase = estimate_tokens()
        salted = strip_ts_comments(f'const leak = "{phrase}";\n' + CARD.read_text())
        literals = quoted_literals(salted)
        assert phrase in literals, "the scan cannot see a restated phrase even when it is there"
        salted_mark = strip_ts_comments(f'const leak = "{mark}";\n' + CARD.read_text())
        assert mark in quoted_literals(salted_mark), "the scan cannot see a restated mark even when it is there"


class TestEveryDecidedValueIsImported:
    """SPEC item 3. `digestStateLabel` and `digestCtaText` from the copy
    module, `digestCostLine` from the envelope module, `ESTIMATE_MARK` and
    `ESTIMATE_PHRASE` from `TopMetricsBar`."""

    def test_the_copy_module_supplies_state_label_and_cta_text(self):
        names = imported_names(code_of(CARD), "api/digestCardCopy")
        assert {"digestStateLabel", "digestCtaText"} <= names, (
            f"only found {names} imported from digestCardCopy"
        )

    def test_the_envelope_module_supplies_the_cost_line_rule(self):
        names = imported_names(code_of(CARD), "api/jobDigest")
        assert "digestCostLine" in names, f"only found {names} imported from jobDigest"

    def test_top_metrics_bar_supplies_the_estimate_tokens(self):
        names = imported_names(code_of(CARD), "metrics/TopMetricsBar")
        assert {"ESTIMATE_MARK", "ESTIMATE_PHRASE"} <= names, (
            f"only found {names} imported from TopMetricsBar"
        )

    def test_the_import_reader_would_notice_an_import_going_away(self):
        # The discriminator: with the digestCostLine import specifier gone,
        # the search above must fail, or it was never reading the import at all.
        without = code_of(CARD).replace(
            'import { digestCostLine } from "../../api/jobDigest";', ""
        )
        names = imported_names(without, "api/jobDigest")
        assert "digestCostLine" not in names, "the reader cannot see the import going away"


class TestTheCtaGoesThroughTheRule:
    """SPEC item 4. `digestCtaText(` occurs in the source and the raw
    `primary_action.label` is never placed in markup.

    WHAT THIS TEST CAN SEE: every occurrence of `primary_action.label` in the
    comment-stripped source is immediately preceded by `digestCtaText(` — i.e.
    it is only ever that call's own argument.
    WHAT IT CANNOT SEE: a differently-named alias reaching the same object
    property through destructuring under another name; that is out of reach
    for a text scan and is not claimed here."""

    def test_digest_cta_text_is_called(self):
        code = code_of(CARD)
        assert "digestCtaText(" in code

    def test_the_raw_label_never_appears_outside_that_call(self):
        code = code_of(CARD)
        occurrences = list(re.finditer(r"primary_action\.label", code))
        assert occurrences, "primary_action.label must be read at least once"
        for m in occurrences:
            prefix = code[max(0, m.start() - 40):m.start()]
            assert prefix.endswith("digestCtaText(digest."), (
                f"primary_action.label found outside digestCtaText(digest. ...): "
                f"...{code[max(0, m.start() - 40):m.end() + 10]}..."
            )

    def test_the_scan_would_notice_the_raw_label_placed_directly_in_markup(self):
        # The discriminator: a raw placement must be caught by the loop above,
        # or the assertion is vacuous.
        salted = code_of(CARD) + "\nconst leak = <span>{digest.primary_action.label}</span>;\n"
        occurrences = list(re.finditer(r"primary_action\.label", salted))
        bad = [
            m for m in occurrences
            if not salted[max(0, m.start() - 40):m.start()].endswith("digestCtaText(digest.")
        ]
        assert bad, "the scan cannot see a raw placement even when it is there"


class TestOwnershipIsOmittedWhenEmpty:
    """SPEC item 5. DECISION F040 D3: the ownership section sits behind an
    emptiness check on `ownership`.

    TWO THINGS ARE PINNED, deliberately kept separate. The first assertion
    below would still pass if `hasOwnership` were computed and then never
    actually used to gate the JSX — a defect the FIRST version of this test
    missed, since `digest.ownership.length > 0` still occurs in the binding's
    own definition even after the `&&` gate in front of the ownership section
    is deleted. The second assertion closes that gap by requiring the gate
    ITSELF, `hasOwnership &&`, to be present — which is exactly what block
    mutation (d), "delete the emptiness guard in front of the ownership
    section", removes."""

    def test_the_ownership_section_sits_behind_an_emptiness_check(self):
        code = code_of(CARD)
        assert re.search(r"digest\.ownership\.length\s*>\s*0", code), (
            "DECISION F040 D3 requires the ownership section to be OMITTED, "
            "not rendered empty, when the list is empty"
        )

    def test_the_emptiness_check_scan_would_notice_it_going_away(self):
        code = code_of(CARD).replace("digest.ownership.length > 0", "true")
        assert not re.search(r"digest\.ownership\.length\s*>\s*0", code), (
            "the scan cannot see the check going away"
        )

    def test_the_emptiness_check_actually_gates_the_ownership_section(self):
        # The gap the two tests above cannot see: a binding can exist and
        # never be applied. `hasOwnership &&` is the JSX short-circuit that
        # actually omits the section; its absence is what block mutation (d)
        # produces even though the binding's own definition line survives.
        code = code_of(CARD)
        assert "hasOwnership &&" in code, (
            "the emptiness check must actually GATE the ownership section, "
            "not merely be computed and left unused"
        )

    def test_the_gate_scan_would_notice_the_gate_going_away(self):
        code = code_of(CARD).replace("hasOwnership && (", "(")
        assert "hasOwnership &&" not in code, (
            "the scan cannot see the gate going away"
        )


class TestEveryStylesReferenceIsADeclaredClass:
    """SPEC item 6. Every `styles.<name>` the component names is a class
    `DigestHeroCard.module.css` declares — parsed out of the sheet rather than
    retyped, so a renamed class fails here."""

    def test_every_styles_reference_is_declared_in_the_sheet(self):
        used = set(re.findall(r"styles\.([A-Za-z_]\w*)", code_of(CARD)))
        assert used, "no styles.<name> reference found; the scan is vacuous"
        declared = css_class_names()
        assert declared, "no class parsed from the sheet; the scan is vacuous"
        missing = used - declared
        assert missing == set(), (
            f"{missing} referenced by the component but not declared in "
            f"DigestHeroCard.module.css"
        )

    def test_the_class_scan_would_notice_an_undeclared_class(self):
        salted = code_of(CARD) + "\nconst leak = styles.doesNotExist;\n"
        used = set(re.findall(r"styles\.([A-Za-z_]\w*)", salted))
        missing = used - css_class_names()
        assert "doesNotExist" in missing, "the scan cannot see an undeclared class even when it is there"
