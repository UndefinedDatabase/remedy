"""Guard: the diff viewer is really MOUNTED, not merely present on disk.

`apps/ui/src/components/diff/DiffView.tsx` has been on disk since F037 R16 with no caller
at all. This round opens the door to it (`docs/roadmap/features/T5_F037.md`, T003): the
"Open diff" button `docs/ui/design_reference/component_spec.md:108` names emits
`onOpenDiff(taskId)` from `DetailPopover`, and `RemedyShell` holds which task run is open,
reads its envelope through `loadDiffEnvelope` and draws `DiffView` behind it.

NOTHING IN THIS REPOSITORY CAN RENDER ANY OF THE THREE. There is no DOM environment here
and `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a NODE environment, so the
frontend runner reaches no markup whatever its availability. The wiring is therefore gated
the way every other component here is gated — by READING it — exactly as
`tests/ui_contracts/test_diff_view_render.py` gates the drawing half.

Every assertion runs over COMMENT-STRIPPED source, because all three files carry WHY
comments that NAME the symbols asserted below (finding `R-0584`).

AND EVERY ASSERTION IS SCOPED TO A FUNCTION BODY, A SIGNATURE, AN IMPORT STATEMENT OR A
JSX OPEN TAG — never to a whole file. Finding `R-0725` is exactly the defect a whole-file
`in` check produces: `type="button"` occurs on the popover's close control as well as on
the diff entry point, and `readDiffEnvelope` was satisfied by an `import` line. A guard
written after that finding does not repeat it.

It reads all three files AS TEXT and imports nothing from `apps/`.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
POPOVER = UI_SRC / "components" / "detail" / "DetailPopover.tsx"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
DIFF_VIEW = UI_SRC / "components" / "diff" / "DiffView.tsx"

VITEST_AUTHORITY = (
    "apps/ui/vitest.config.ts (environment: node, include: src/**/*.test.ts), "
    "DECISION F031 D5 and DECISION F037 D8"
)

# The four rules `DiffView` calls out to `diffViewModel.ts` for. Constraint 3 of the F037
# R18 block forbids this round from editing that component at all, and these four names are
# that prohibition made mechanical: a round that quietly rewrote the drawing half while
# claiming only to mount it would lose one of them.
DIFF_VIEW_DELEGATED_RULES = (
    "buildDiffRowModels",
    "defaultCollapsedHunkIds",
    "toggleHunkCollapse",
    "splitLineIntoIntralineSegments",
)

# The cancellation flag S5 of the F037 R18 block requires, PINNED BY NAME. The property —
# "a response that arrives after the open task id changed again is discarded" — cannot be
# read out of text without naming the variable that carries it, so this guard names it and
# says so rather than asserting something weaker that would pass on a viewer that lies.
CANCELLATION_FLAG = "cancelled"


def strip_ts_comments(text: str) -> str:
    """Drop `//` and `/* */` comments, the scanner `test_diff_view_render.py` uses.

    None of the three files scanned through this holds a string literal carrying either
    marker, which is what lets so plain a scanner be trustworthy here.
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


def popover_code() -> str:
    return strip_ts_comments(POPOVER.read_text())


def shell_code() -> str:
    return strip_ts_comments(SHELL.read_text())


def diff_view_code() -> str:
    return strip_ts_comments(DIFF_VIEW.read_text())


def _braced_region(code: str, open_index: int) -> str:
    """The `{ ... }` beginning at `open_index`, brace depth respected."""
    depth = 0
    for index in range(open_index, len(code)):
        if code[index] == "{":
            depth += 1
        elif code[index] == "}":
            depth -= 1
            if depth == 0:
                return code[open_index:index + 1]
    raise AssertionError(f"a braced region opened at {open_index} never closes")


def ts_function_body(code: str, name: str) -> str:
    """The body of `export function <name>`, brace depth respected.

    The signature's own braces — a destructured prop list and its inline type — are stepped
    over by matching PARENTHESES first, so the body found here is the body and not the
    argument list.
    """
    match = re.search(rf"export (?:async )?function {name}\b", code)
    assert match, f"no exported function named {name} was found"
    return _braced_region(code, code.index("{", _signature_end(code, match.end())))


def ts_function_signature(code: str, name: str) -> str:
    """`export function <name>(...)` up to, but not including, the body's opening brace."""
    match = re.search(rf"export (?:async )?function {name}\b", code)
    assert match, f"no exported function named {name} was found"
    return code[match.start():_signature_end(code, match.end())]


def _signature_end(code: str, after_name: int) -> int:
    """The index just past the argument list's closing parenthesis."""
    start = code.index("(", after_name)
    depth = 0
    for index in range(start, len(code)):
        if code[index] == "(":
            depth += 1
        elif code[index] == ")":
            depth -= 1
            if depth == 0:
                return index + 1
    raise AssertionError(f"the argument list opened at {start} never closes")


def jsx_open_tag(code: str, element: str, naming: str | None = None) -> str:
    """The OPEN TAG `<element ...>` — the one naming `naming` when that is given.

    Brace depth is tracked while scanning for the tag's `>`, because an arrow function in a
    prop expression carries a `>` of its own and a naive scan would cut the tag in half.
    """
    tags: list[str] = []
    for match in re.finditer(rf"<{element}\b", code):
        depth = 0
        for index in range(match.start(), len(code)):
            char = code[index]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            elif char == ">" and depth == 0:
                tags.append(code[match.start():index + 1])
                break
    if naming is not None:
        tags = [tag for tag in tags if naming in tag]
    assert tags, f"no <{element} open tag naming {naming} was found"
    return tags[0]


def import_statement(code: str, module: str) -> str:
    """The single `import ... from "<module>";` statement, as one string."""
    match = re.search(rf'import[^;]*?from\s*"{re.escape(module)}"\s*;', code, re.DOTALL)
    assert match, f'no import statement from "{module}" was found'
    return match.group(0)


def diff_read_effect_body(code: str) -> str:
    """The body of the `useEffect` that calls `loadDiffEnvelope`.

    Scoped rather than swept: the shell runs more than one effect, and a cancellation flag
    belonging to a different one would answer the stale-response assertions below.
    """
    for match in re.finditer(r"useEffect\(\s*\(\s*\)\s*=>\s*\{", code):
        body = _braced_region(code, code.index("{", match.start()))
        if "loadDiffEnvelope(" in body:
            return body
    raise AssertionError("no useEffect body in the shell calls loadDiffEnvelope")


class TestTheStripperIsNotVacuous:
    """Without this, every assertion below is satisfiable by the three files' own WHY
    comments — and every SCOPED one is satisfiable by a scanner that silently handed back
    the whole file, which is finding `R-0725` arriving through the back door."""

    def test_the_stripper_removes_both_comment_forms(self):
        sample = 'const a = 1; // note\n/* block */ const b = 2;'
        stripped = strip_ts_comments(sample)
        assert "note" not in stripped, "the // form must go"
        assert "block" not in stripped, "the /* */ form must go"
        assert "const b = 2;" in stripped, "and the code between them must survive"

    def test_all_three_components_really_lose_text_to_the_stripper(self):
        for path in (POPOVER, SHELL, DIFF_VIEW):
            raw = path.read_text()
            assert "//" in raw or "/*" in raw, (
                f"{path.name} must keep the WHY comments the Code Discoverability "
                f"Conventions of AGENTS.md require; with no comment in the file the "
                f"stripper proves nothing"
            )
            assert len(strip_ts_comments(raw)) < len(raw), (
                f"the stripper returned {path.name} unchanged, so every assertion in this "
                f"module would be satisfied by prose rather than by code (finding R-0584)"
            )

    def test_every_scanner_finds_its_subject_and_returns_less_than_the_file(self):
        """Each scoper below is exercised on both sides of every pair it is used on.

        A scoper that returned its whole input would make each `in` check a whole-file
        search wearing a function's name, which is the defect finding `R-0725` records.
        """
        popover, shell, diff_view = popover_code(), shell_code(), diff_view_code()
        scoped = (
            ("DetailPopover signature", ts_function_signature(popover, "DetailPopover"), popover),
            ("DetailPopover diff button tag", jsx_open_tag(popover, "button", "onOpenDiff"), popover),
            ("RemedyShell body", ts_function_body(shell, "RemedyShell"), shell),
            ("RemedyShell DetailPopover tag", jsx_open_tag(shell, "DetailPopover"), shell),
            ("RemedyShell diff read effect", diff_read_effect_body(shell), shell),
            ("RemedyShell DiffView import", import_statement(shell, "../diff/DiffView"), shell),
            ("RemedyShell door import", import_statement(shell, "../../api/remedyApi"), shell),
            ("DiffView body", ts_function_body(diff_view, "DiffView"), diff_view),
        )
        for label, region, whole in scoped:
            assert region, f"the scanner for the {label} found nothing at all"
            assert len(region) < len(whole), (
                f"the scanner for the {label} returned {len(region)} characters out of "
                f"{len(whole)}, so it is not scoping and every assertion built on it is a "
                f"whole-file search (finding R-0725)"
            )


class TestThePopoverOffersTheEntryPoint:
    """(b) `docs/ui/design_reference/component_spec.md:108` and `:113-116` put the viewer's
    entry point here, as a button emitting `onOpenDiff(taskId)`."""

    def test_the_popover_declares_the_open_diff_prop(self):
        signature = ts_function_signature(popover_code(), "DetailPopover")
        assert "onOpenDiff" in signature, (
            f"{POPOVER.name} declares no onOpenDiff prop, so no caller can open the viewer "
            f"and {DIFF_VIEW.name} keeps the zero callers it has had since F037 R16"
        )
        assert re.search(r"onOpenDiff\?\s*:\s*\(\s*taskId\s*:\s*string\s*\)\s*=>\s*void",
                         signature), (
            f"the onOpenDiff prop of {POPOVER.name} does not have the optional "
            f"`(taskId: string) => void` shape the entry point needs: optional so a caller "
            f"that handles nothing keeps the popover it had, and taking the TASK id "
            f"because that is what the server's task-run route keys on"
        )

    def test_the_entry_point_is_a_real_button(self):
        tag = jsx_open_tag(popover_code(), "button", "onOpenDiff")
        assert 'type="button"' in tag, (
            f"the diff entry point in {POPOVER.name} is not a `type=\"button\"` button. A "
            f"div carries no keyboard affordance, and an untyped button submits a form it "
            f"may one day sit in — the rule test_diff_view_render.py pins for this "
            f"feature's other control. Scoped to this tag because the popover's close "
            f"control is a typed button too (finding R-0725)"
        )


class TestTheEntryPointPassesTheTaskId:
    """(c) `onOpenDiff(taskId)` means the TASK RUN id. The graph node id is a different
    value entirely, and the server's task-run route would answer nothing for it."""

    def test_the_button_passes_the_task_id_and_not_the_node_id(self):
        tag = jsx_open_tag(popover_code(), "button", "onOpenDiff")
        assert "task.id" in tag, (
            f"the diff entry point in {POPOVER.name} does not pass task.id, so the id it "
            f"hands to onOpenDiff is not the one the server's task-run route keys on"
        )
        assert "selectedNode" not in tag, (
            f"the diff entry point in {POPOVER.name} passes a value derived from "
            f"selectedNode. The graph node id and the task run id are different values "
            f"and a diff addressed by the wrong one is a request for a run that does not "
            f"exist ({VITEST_AUTHORITY} reaches none of this)"
        )


class TestTheShellReallyMountsTheViewer:
    """(d) The mount itself: the shell imports both halves of the door, renders the
    component, and hands the popover the handler that opens it."""

    def test_the_shell_imports_the_component_and_the_door(self):
        code = shell_code()
        assert "DiffView" in import_statement(code, "../diff/DiffView"), (
            f"{SHELL.name} does not import DiffView from its own module"
        )
        assert "loadDiffEnvelope" in import_statement(code, "../../api/remedyApi"), (
            f"{SHELL.name} does not import loadDiffEnvelope, so the panel has no way to "
            f"read an envelope and could only render an empty one"
        )

    def test_the_shell_really_renders_the_diff_view(self):
        body = ts_function_body(shell_code(), "RemedyShell")
        assert "<DiffView" in body, (
            f"{SHELL.name} imports DiffView but renders no <DiffView element, which is the "
            f"state F037 R16 left behind — a component on disk that nothing draws. Scoped "
            f"to the function body so the import line alone cannot satisfy this "
            f"(finding R-0725)"
        )

    def test_the_shell_hands_the_popover_an_open_diff_handler(self):
        tag = jsx_open_tag(shell_code(), "DetailPopover")
        assert "onOpenDiff" in tag, (
            f"{SHELL.name} renders DetailPopover without an onOpenDiff prop, so the entry "
            f"point renders nothing and the viewer stays unreachable"
        )


class TestALateResponseIsDiscarded:
    """(e) S5 of the F037 R18 block: a response arriving after the open task id changed
    again must be DISCARDED, not painted under the new task. A viewer that lies is worse
    than one that is slow, and this is the only gate in this repository that can see it.

    THE FLAG IS PINNED BY NAME (`cancelled`). The property is not readable out of text
    without naming the variable that carries it, so this guard names it deliberately; a
    rename of the flag is a change to the code this assertion exists to describe.
    """

    def test_the_read_effect_declares_a_cancellation_flag(self):
        body = diff_read_effect_body(shell_code())
        assert re.search(rf"let\s+{CANCELLATION_FLAG}\s*=\s*false", body), (
            f"the effect in {SHELL.name} that calls loadDiffEnvelope declares no "
            f"`let {CANCELLATION_FLAG} = false`, so it has nothing to discard a stale "
            f"response with"
        )

    def test_the_effect_checks_the_flag_before_storing_the_envelope(self):
        body = diff_read_effect_body(shell_code())
        assert re.search(
            rf"if\s*\(\s*!\s*{CANCELLATION_FLAG}\s*\)\s*\{{?\s*setDiffEnvelope\(", body), (
            f"the effect in {SHELL.name} stores what loadDiffEnvelope resolved to without "
            f"first checking {CANCELLATION_FLAG}, so a response for a task run the operator "
            f"has already navigated away from is painted under the task now open"
        )

    def test_the_effect_returns_a_cleanup_that_sets_the_flag(self):
        body = diff_read_effect_body(shell_code())
        cleanup = re.search(rf"return\s*\(\s*\)\s*=>\s*\{{[^}}]*{CANCELLATION_FLAG}\s*=\s*true",
                            body)
        assert cleanup, (
            f"the effect in {SHELL.name} returns no cleanup function setting "
            f"{CANCELLATION_FLAG}, so the flag is never raised and the check above can "
            f"never be false — the guard would be present and inert"
        )


class TestTheDrawingHalfIsUnchanged:
    """(f) Constraint 3 of the F037 R18 block made mechanical: this round MOUNTS
    `DiffView.tsx` and does not edit it. The four rules it delegates to `diffViewModel.ts`
    are what a quiet rewrite would lose first."""

    def test_the_diff_view_still_calls_every_rule_it_delegates(self):
        body = ts_function_body(diff_view_code(), "DiffView")
        for rule in DIFF_VIEW_DELEGATED_RULES:
            assert f"{rule}(" in body, (
                f"{DIFF_VIEW.name} no longer calls {rule}, so the round that was to mount "
                f"the drawing half changed it instead. Scoped to the component's body "
                f"because the import list names all four too (finding R-0725)"
            )
