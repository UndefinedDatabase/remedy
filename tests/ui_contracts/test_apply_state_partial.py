"""Guard: every apply label the backend fold can emit has a label in the popover.

Finding R-0738. `fold_task_apply_states` in `packages/orchestration/proof_chain.py`
folds a task's changes to ONE apply label. The cockpit's `_task_truth_maps` in
`packages/orchestration/ui_server.py` is now only an adapter over that fold, so the
label reaches the UI as `RemedyTaskItem.applyStatus` and is rendered by the
`applyStatus` helper in `apps/ui/src/components/detail/DetailPopover.tsx`. That
helper ends in `return UNKNOWN;`, so a value the fold emits and the helper does not
branch on renders as "Unknown" — a silent, uninformative answer rather than a broken
build.

NOTHING ELSE IN THIS REPOSITORY READS THE TWO ENDS TOGETHER. The Python suite cannot
see the TSX, and the shipped vitest config (`apps/ui/vitest.config.ts`, environment
node, include `src/**/*.test.ts`) reaches no component markup and could not see the
Python in any case. This file is that check, and it reads BOTH files AS TEXT and
imports nothing from `apps/`, exactly as `tests/ui_contracts/test_diff_envelope_door.py`
and `tests/ui_contracts/test_decision_answer_wiring.py` do.

THE EMITTED SET IS DERIVED, NOT RESTATED. `fold_apply_labels` walks the AST of the
shipped `fold_task_apply_states` and collects every string literal it assigns to
`state_by_task[...]`, so adding a fifth state on the Python side alone fails a test
here rather than shipping as "Unknown". THE WALK NAMES ITS OWN FILE AND FUNCTION in
the constants below: move the fold to another module without moving these with it and
the walk finds NOTHING, which `test_the_ast_derivation_finds_labels_at_all` exists to
catch before an empty expected set silently passes every seam assertion beneath it.

THE POPOVER IS NOT THE ONLY SURFACE. `apps/ui/src/components/panels/TaskChecklistCard.tsx`
is the tasks-card row an operator watches while a job runs, and it renders the same
`RemedyTaskItem`. Its `stateText` used to answer "Done" for a task whose changes only
partly applied, and its `iconFor` used to paint the done tile for it. DECISION F033 D5
rules that row the task node's partial treatment, so this module pins the card at the
same seam as the popover: the card labels the state the fold emits, that label is
distinct from every other state text the card can produce, its tile differs from the
done tile, and it is the SAME STRING the popover uses — one spelling per concept, made
mechanical so the two surfaces cannot drift apart.

Every assertion over the TSX runs on COMMENT-STRIPPED source. The helper now carries a
WHY comment that names the very state asserted below — "Unknown", "Applied", the
disagreement it describes — so an unstripped guard would be satisfied by the prose
describing the branch rather than by the branch (finding R-0584).
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
# The fold's home, which is NOT the HTTP server: it lives beside the
# `ProofChange.apply_state` field it reads so the run report can import it too.
FOLD_MODULE = REPO_ROOT / "packages" / "orchestration" / "proof_chain.py"
POPOVER = REPO_ROOT / "apps" / "ui" / "src" / "components" / "detail" / "DetailPopover.tsx"
CARD = REPO_ROOT / "apps" / "ui" / "src" / "components" / "panels" / "TaskChecklistCard.tsx"

FOLD_FUNCTION = "fold_task_apply_states"
FOLD_MAP = "state_by_task"
# The local list of per-change apply states the fold decides from. Named here so the
# membership predicate below binds to the fold's real local rather than to a name that
# survived only in this file.
FOLD_STATE_LIST = "apply_states"
HELPER = "applyStatus"

# The card's two helpers, and the field they read beside the lifecycle state.
CARD_TILE_HELPER = "iconFor"
CARD_STATE_HELPER = "stateText"
APPLY_FIELD = "applyStatus"
PARTIAL = "partial"
DONE = "done"

# `if (task?.applyStatus === "<value>") return "<label>";` — the file's one branch
# idiom, read off comment-stripped source.
RE_BRANCH = re.compile(r'task\?\.' + HELPER + r' === "([^"]+)"\)\s*return "([^"]+)";')
RE_BRANCH_VALUE = re.compile(r'task\?\.' + HELPER + r' === "([^"]+)"')
RE_FALLBACK = re.compile(r"return\s+(\w+);\s*\}\s*$")
RE_UNKNOWN_CONST = re.compile(r'const UNKNOWN = "([^"]+)";')

# `if (task.<field> === "<value>") return "<label>";` — the card's status-text idiom.
RE_CARD_STATE_BRANCH = re.compile(r'if \(task\.(\w+) === "([^"]+)"\) return "([^"]+)";')
# The unguarded label the card's status text ends in.
RE_CARD_STATE_FALLBACK = re.compile(r'return "([^"]+)";\s*\}\s*$')
# `if (task.<field> === "<value>") return <span className={styles.<tile>}` — its tile idiom.
RE_CARD_TILE_BRANCH = re.compile(
    r'if \(task\.(\w+) === "([^"]+)"\) return <span className=\{styles\.(\w+)\}'
)


def strip_ts_comments(text: str) -> str:
    """Drop `//` and `/* */` comments, the scanner every guard in this directory uses.

    Neither file scanned through this holds a string literal carrying either marker,
    which is what lets so plain a scanner be trustworthy here.
    """
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            newline = text.find("\n", i)
            i = n if newline == -1 else newline
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def fold_apply_function() -> ast.FunctionDef:
    """The AST of the shipped fold, or an assertion naming what is missing."""
    tree = ast.parse(FOLD_MODULE.read_text())
    fold = next(
        (
            node for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == FOLD_FUNCTION
        ),
        None,
    )
    assert fold is not None, (
        f"{FOLD_MODULE.name} defines no function named {FOLD_FUNCTION}; this guard would "
        f"measure the popover against an empty backend set and could not fail"
    )
    return fold


def fold_apply_labels() -> set[str]:
    """Every string literal the SHIPPED fold can assign to `state_by_task[...]`.

    Derived from the AST rather than listed, so a fifth state added on the Python side
    alone widens this set and reddens the agreement test below instead of reaching an
    operator as "Unknown".
    """
    labels: set[str] = set()
    for node in ast.walk(fold_apply_function()):
        if not isinstance(node, ast.Assign):
            continue
        if not (isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)):
            continue
        for target in node.targets:
            if (
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == FOLD_MAP
            ):
                labels.add(node.value.value)
    return labels


def fold_membership_tests_over_apply_states() -> set[str]:
    """Every literal the fold tests for MEMBERSHIP of its `FOLD_STATE_LIST` local.

    An AST predicate, not a text search: the fold's WHY comment quotes the membership
    test it replaced, so a grep over the source would be answered by the prose that
    explains the repair rather than by code (the R-0584 class, on the Python side).
    The agreement fold compares each state one at a time and so puts nothing here;
    `s in ("applied", "reverted")` inside a generator is a membership test over a
    TUPLE, not over the list, and is deliberately out of scope.
    """
    found: set[str] = set()
    for node in ast.walk(fold_apply_function()):
        if not isinstance(node, ast.Compare):
            continue
        for op, comparator in zip(node.ops, node.comparators):
            if (
                isinstance(op, ast.In)
                and isinstance(comparator, ast.Name)
                and comparator.id == FOLD_STATE_LIST
                and isinstance(node.left, ast.Constant)
                and isinstance(node.left.value, str)
            ):
                found.add(node.left.value)
    return found


def popover_code() -> str:
    """The popover with its prose removed — the only form the assertions below read."""
    return strip_ts_comments(POPOVER.read_text())


def helper_body(code: str, name: str) -> str:
    """The body of `function <name>(...)` in `code`, brace depth respected.

    Scoped rather than swept: in the popover `UNKNOWN` is returned by `testStatusLabel`
    and `proofStatusLabel` directly below `applyStatus` and is rendered by four `Field`
    call sites, so a whole-file reading of the fallback would be answered by any of them
    and would stay green with this helper's own fallback gone. The card has the same
    shape — `iconFor`, `stateText` and `outcomeHint` sit one after another — which is
    why this walker takes the function name rather than assuming one.
    """
    match = re.search(rf"function {name}\(", code)
    assert match, f"the scanned source declares no function named {name}"
    start = code.index("{", match.end())
    depth = 0
    for index in range(start, len(code)):
        if code[index] == "{":
            depth += 1
        elif code[index] == "}":
            depth -= 1
            if depth == 0:
                return code[start:index + 1]
    raise AssertionError(f"the body of {name} never closes in the scanned source")


def helper_branches() -> dict[str, str]:
    """The helper's `<backend value> -> <operator label>` map, read off its own body."""
    return dict(RE_BRANCH.findall(helper_body(popover_code(), HELPER)))


def card_code() -> str:
    """The tasks card with its prose removed — the only form the card assertions read."""
    return strip_ts_comments(CARD.read_text())


def card_state_branches() -> list[tuple[str, str, str]]:
    """`(field, value, label)` for every guarded string return in the card's stateText.

    The card's branch idiom is `if (task.<field> === "<value>") return "<label>";`, and
    the field is part of the reading on purpose: a branch on the LIFECYCLE state and a
    branch on the APPLY state are different answers and must not be conflated here.
    """
    return RE_CARD_STATE_BRANCH.findall(helper_body(card_code(), CARD_STATE_HELPER))


def card_state_fallback() -> str:
    """The unguarded label the card's stateText ends in."""
    body = helper_body(card_code(), CARD_STATE_HELPER).strip()
    match = RE_CARD_STATE_FALLBACK.search(body)
    assert match, (
        f"{CARD.name}'s {CARD_STATE_HELPER} no longer ends in an unguarded string "
        f"return, so the labels it can produce cannot be read off it"
    )
    return match.group(1)


def card_tile_branches() -> list[tuple[str, str, str]]:
    """`(field, value, tile class)` for every guarded tile the card's iconFor returns."""
    return RE_CARD_TILE_BRANCH.findall(helper_body(card_code(), CARD_TILE_HELPER))


def emitted_partial_state() -> str:
    """The disagreement state, taken from the SHIPPED fold rather than restated here.

    Every card assertion below asks the fold's own AST whether the state it pins can
    still be produced. Rename or remove it on the Python side and these go RED rather
    than pinning a card branch no backend value reaches.
    """
    emitted = fold_apply_labels()
    assert PARTIAL in emitted, (
        f"{FOLD_FUNCTION} in {FOLD_MODULE.name} emits {sorted(emitted)} and not {PARTIAL!r}; "
        f"the card assertions below would pin a state the backend can no longer produce"
    )
    return PARTIAL


def card_label_for(state: str) -> str:
    """The card's status text for an APPLY state, or an assertion naming what is missing."""
    for field, value, label in card_state_branches():
        if field == APPLY_FIELD and value == state:
            return label
    raise AssertionError(
        f"{CARD_STATE_HELPER} in {CARD.name} has no branch on {APPLY_FIELD} === "
        f"{state!r}; a task in that state keeps whatever its lifecycle state says, "
        f"which for a finished task is 'Done' about changes that only half landed"
    )


def card_tile_for(field: str, value: str) -> str:
    """The tile class the card's iconFor returns for one `<field> === <value>` branch."""
    for found_field, found_value, tile in card_tile_branches():
        if found_field == field and found_value == value:
            return tile
    raise AssertionError(
        f"{CARD_TILE_HELPER} in {CARD.name} has no branch on {field} === {value!r} "
        f"returning a tile; the branches it does have are {card_tile_branches()}"
    )


class TestTheReadersAreNotVacuous:
    """Without these, every assertion below could pass on prose, on an empty set, or on
    a scoper that silently handed back the whole module."""

    def test_the_stripper_removes_both_comment_forms(self):
        sample = 'const a = 1; // note\n/* block */ const b = 2;'
        stripped = strip_ts_comments(sample)
        assert "note" not in stripped, "the // form must go"
        assert "block" not in stripped, "the /* */ form must go"
        assert "const b = 2;" in stripped, "and the code between them must survive"

    def test_the_popover_really_loses_text_to_the_stripper(self):
        raw = POPOVER.read_text()
        assert "//" in raw, (
            f"{POPOVER.name} must keep the WHY comment the Code Discoverability "
            f"Conventions of AGENTS.md require above {HELPER}; with no comment in the "
            f"file the stripper proves nothing"
        )
        assert len(strip_ts_comments(raw)) < len(raw), (
            f"the stripper returned {POPOVER.name} unchanged, so every assertion in "
            f"this module would be satisfied by prose rather than by code (R-0584)"
        )

    def test_the_helper_scoper_returns_less_than_the_whole_module(self):
        code = popover_code()
        body = helper_body(code, HELPER)
        assert len(body) < len(code), (
            f"helper_body returned {len(body)} characters out of {len(code)} in "
            f"{POPOVER.name}, so it is not scoping at all and the fallback reading "
            f"below is a whole-file search wearing a function's name"
        )
        assert "testStatusLabel" not in body, (
            f"the body returned for {HELPER} reaches as far as testStatusLabel, so it "
            f"spans more than one helper and its neighbours' returns would answer for "
            f"this one"
        )

    def test_the_ast_derivation_finds_labels_at_all(self):
        labels = fold_apply_labels()
        assert labels, (
            f"the AST walk over {FOLD_FUNCTION} in {FOLD_MODULE.name} found no literal "
            f"assigned to {FOLD_MAP}; an agreement measured against an empty backend "
            f"set passes on any popover at all"
        )

    def test_the_branch_scan_finds_branches_at_all(self):
        assert helper_branches(), (
            f"the branch scan over {HELPER} in {POPOVER.name} found nothing, so the "
            f"agreement below would be measured against an empty popover set"
        )


class TestTheBackendCanReallyEmitPartial:
    """Asserted against the SOURCE of the fold, not against a recollection of it."""

    def test_the_fold_assigns_the_partial_label(self):
        labels = fold_apply_labels()
        assert "partial" in labels, (
            f"{FOLD_FUNCTION} in {FOLD_MODULE.name} assigns {sorted(labels)} to {FOLD_MAP} "
            f"and never 'partial', so a task whose changes disagree is folded to one of "
            f"the confident answers again — the whole of finding R-0738"
        )

    def test_the_three_confident_labels_survive_beside_it(self):
        labels = fold_apply_labels()
        for expected in ("applied", "reverted", "not_applied"):
            assert expected in labels, (
                f"{FOLD_FUNCTION} no longer emits '{expected}'; the partial state was "
                f"added to model a case the three confident answers could not, never to "
                f"replace one of them"
            )

    def test_the_fold_no_longer_answers_by_membership(self):
        # Read as an AST PREDICATE rather than as a text grep, for the reason every
        # guard in this directory strips comments before asserting: the fold's own WHY
        # comment QUOTES the membership test it replaced, so `'if "applied" in
        # apply_states' not in source` fails on the prose that explains the repair.
        offenders = sorted(fold_membership_tests_over_apply_states())
        assert not offenders, (
            f"{FOLD_FUNCTION} in {FOLD_MODULE.name} still tests {offenders} for MEMBERSHIP "
            f"of apply_states; that reports 'applied' when a single change of many "
            f"applied, which is the exact reading the agreement fold replaced"
        )


class TestEveryEmittedValueHasALabel:
    """The seam itself. A value emitted on one side only renders as the UNKNOWN
    fallback, which is not a build failure and not a test failure anywhere else."""

    def test_the_two_sets_agree_in_both_directions(self):
        emitted = fold_apply_labels()
        branched = set(RE_BRANCH_VALUE.findall(helper_body(popover_code(), HELPER)))
        unlabelled = sorted(emitted - branched)
        assert not unlabelled, (
            f"{FOLD_FUNCTION} in {FOLD_MODULE.name} can emit {unlabelled}, which {HELPER} in "
            f"{POPOVER.name} does not branch on; every one of them renders as the "
            f"UNKNOWN fallback, so the operator is told nothing rather than told wrong"
        )
        unreachable = sorted(branched - emitted)
        assert not unreachable, (
            f"{HELPER} in {POPOVER.name} branches on {unreachable}, which "
            f"{FOLD_FUNCTION} in {FOLD_MODULE.name} can never emit; a branch no backend "
            f"value reaches is dead markup that reads as a supported state"
        )


class TestThePartialLabelSaysSomething:
    """A branch that returned the fallback's own string would satisfy the agreement
    above and tell the operator exactly as little as no branch at all."""

    def test_the_helper_returns_a_label_for_partial(self):
        branches = helper_branches()
        assert branches.get("partial"), (
            f"{HELPER} in {POPOVER.name} has no 'partial' branch returning a label; "
            f"the backend value would fall through to the fallback"
        )

    def test_the_partial_label_is_not_the_unknown_fallback(self):
        code = popover_code()
        unknown = RE_UNKNOWN_CONST.search(code)
        assert unknown, f"{POPOVER.name} no longer declares the UNKNOWN constant"
        assert helper_branches()["partial"] != unknown.group(1), (
            "the 'partial' branch returns the UNKNOWN string itself, which replaces a "
            "confident wrong answer with an uninformative one — the reason the fold "
            "and the label had to land together"
        )

    def test_the_partial_label_is_distinct_from_the_other_three(self):
        branches = helper_branches()
        others = {value: label for value, label in branches.items() if value != "partial"}
        assert branches["partial"] not in others.values(), (
            f"the 'partial' branch returns {branches['partial']!r}, a label already "
            f"used by {sorted(v for v, ll in others.items() if ll == branches['partial'])}; "
            f"an operator cannot tell the two states apart on screen"
        )
        assert len(set(branches.values())) == len(branches), (
            f"{HELPER} maps {len(branches)} backend values onto "
            f"{len(set(branches.values()))} labels, so at least two states render "
            f"identically"
        )

    def test_the_helper_still_ends_in_the_fallback(self):
        body = helper_body(popover_code(), HELPER)
        fallback = RE_FALLBACK.search(body.strip())
        assert fallback and fallback.group(1) == "UNKNOWN", (
            f"{HELPER} in {POPOVER.name} must still end in `return UNKNOWN;`: an "
            f"applyStatus this component has never heard of is exactly what the "
            f"fallback is for, and the agreement test above is what keeps a value the "
            f"backend really emits out of it"
        )


class TestTheCardReadersAreNotVacuous:
    """The same obligation the popover readers carry, for the second surface: without
    these, every card assertion below could pass on prose or on a scoper that silently
    handed back the whole module."""

    def test_the_card_really_loses_text_to_the_stripper(self):
        raw = CARD.read_text()
        assert "//" in raw, (
            f"{CARD.name} must keep the WHY comment the Code Discoverability "
            f"Conventions of AGENTS.md require above {CARD_TILE_HELPER}; with no "
            f"comment in the file the stripper proves nothing"
        )
        assert len(strip_ts_comments(raw)) < len(raw), (
            f"the stripper returned {CARD.name} unchanged, so every card assertion in "
            f"this module would be satisfied by prose rather than by code (R-0584)"
        )

    def test_the_card_tile_scoper_returns_less_than_the_whole_module(self):
        code = card_code()
        body = helper_body(code, CARD_TILE_HELPER)
        assert len(body) < len(code), (
            f"helper_body returned {len(body)} characters out of {len(code)} for "
            f"{CARD_TILE_HELPER} in {CARD.name}, so it is not scoping at all and the "
            f"tile reading below is a whole-file search wearing a function's name"
        )
        assert CARD_STATE_HELPER not in body, (
            f"the body returned for {CARD_TILE_HELPER} reaches as far as "
            f"{CARD_STATE_HELPER}, so it spans more than one helper and the "
            f"neighbouring helper's returns would answer for this one"
        )

    def test_the_card_state_scoper_returns_less_than_the_whole_module(self):
        code = card_code()
        body = helper_body(code, CARD_STATE_HELPER)
        assert len(body) < len(code), (
            f"helper_body returned {len(body)} characters out of {len(code)} for "
            f"{CARD_STATE_HELPER} in {CARD.name}, so it is not scoping at all and the "
            f"label reading below is a whole-file search wearing a function's name"
        )
        assert "outcomeHint" not in body, (
            f"the body returned for {CARD_STATE_HELPER} reaches as far as outcomeHint, "
            f"so it spans more than one helper and the neighbouring helper's returns "
            f"would answer for this one"
        )


class TestTheCardTellsThePartialStateApart:
    """The tasks-card row is the surface an operator watches while a job runs. A task
    whose changes disagree must not read 'Done' there, and its tile must not be the
    done tile — DECISION F033 D5, the second of the three surfaces R-0738 names."""

    def test_the_card_labels_the_state_the_fold_emits(self):
        state = emitted_partial_state()
        assert card_label_for(state), (
            f"{CARD_STATE_HELPER} in {CARD.name} branches on {APPLY_FIELD} === "
            f"{state!r} but returns an empty label for it"
        )

    def test_the_card_partial_label_is_distinct_from_every_other_state_text(self):
        state = emitted_partial_state()
        label = card_label_for(state)
        others = {
            found_label
            for field, value, found_label in card_state_branches()
            if not (field == APPLY_FIELD and value == state)
        }
        others.add(card_state_fallback())
        assert label not in others, (
            f"{CARD_STATE_HELPER} in {CARD.name} returns {label!r} for {state!r} and "
            f"for another state as well, so an operator cannot tell a partially applied "
            f"task from {sorted(others)} on the row"
        )

    def test_the_card_tile_for_partial_is_not_the_done_tile(self):
        state = emitted_partial_state()
        partial_tile = card_tile_for(APPLY_FIELD, state)
        done_tile = card_tile_for("state", DONE)
        assert partial_tile != done_tile, (
            f"{CARD_TILE_HELPER} in {CARD.name} paints {partial_tile!r} for both "
            f"{state!r} and the finished lifecycle state, so the row looks finished "
            f"while only part of its changes landed — the whole of finding R-0738"
        )

    def test_the_card_and_the_popover_use_one_spelling(self):
        state = emitted_partial_state()
        assert card_label_for(state) == helper_branches()[state], (
            f"{CARD.name} says {card_label_for(state)!r} where {POPOVER.name} says "
            f"{helper_branches()[state]!r} for the same backend value; two spellings of "
            f"one concept is exactly the drift the Code Discoverability Conventions of "
            f"AGENTS.md forbid, and it reads to an operator as two different states"
        )
