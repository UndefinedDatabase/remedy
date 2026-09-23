"""`remedy integrity block <path>`: the checkable items of the reviewer's checklist (T2_F279 T003).

`docs/agents/planner_reviewer_prompt.md` §3 carries a pre-emission checklist the reviewer runs
by hand on every step block before a worker sees it. Some of its items are arithmetic or a
lookup, and those are the ones the record shows slipping. Each rule below checks one of them: it
reads the block's text, and where its item needs it the repository's own files, and answers one
`LintResult` naming the item number and the checklist sentence it enforces. Nothing here writes
a file. `tests/orchestration/test_block_lint.py` holds every rule to a LIVE item number and to a
sentence that item really contains, so a rule cannot outlive the item it cites (DECISION F279 D5).
"""
from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKLIST_PATH = "docs/agents/planner_reviewer_prompt.md"
LEDGER_PATH = ".agent/live_review.md"
ARCHIVE_PATH = ".agent/live_review_archive.md"
BLOCK_LINE_LIMIT = 400
PLAN_LINE_LIMIT = 50

_PAYLOAD_ROW = re.compile(r"^\| *([^|`]+?) *\| *(\d+) *\| *(\d+) *\| *([0-9a-f]{64}) *\|$", re.M)
_OPEN_COUNT = re.compile(r"open-findings count, (\d+)")
_FENCE = re.compile(r"^```[^\n]*\n(.*?)^```", re.M | re.S)
_REPO_PATH = re.compile(r"(?<![\w./-])((?:packages|apps|tests|scripts|docs)/[\w./-]*[\w/])")
_NEW_FILE = re.compile(r"NEW FILE at\s+`([^`]+)`")
_REGISTRATION = re.compile(r"^- (R-\d{4}) — ", re.M)
_GATES_BEFORE = re.compile(r"\bG(\d+) to G(\d+) run before (C\w+) is written")
_GATE_HEADER = re.compile(r"^G(\d+) ", re.M)


@dataclass(frozen=True)
class BlockContext:
    """What a rule may read: the block's text and the repository it is about."""

    text: str
    repo_root: Path = REPO_ROOT

    def read(self, relative: str) -> str:
        path = self.repo_root / relative
        return path.read_text(encoding="utf-8") if path.is_file() else ""


@dataclass(frozen=True)
class Rule:
    item: int
    name: str
    sentence: str
    check: Callable[[BlockContext], tuple[bool, str]]


@dataclass(frozen=True)
class LintResult:
    item: int
    name: str
    ok: bool
    detail: str
    sentence: str

    def as_dict(self) -> dict[str, object]:
        return {"item": self.item, "name": self.name, "ok": self.ok, "detail": self.detail,
                "sentence": self.sentence}


def _line_count(text: str) -> int:
    return text.count("\n") + (0 if text.endswith("\n") or not text else 1)


def check_size(ctx: BlockContext) -> tuple[bool, str]:
    lines = _line_count(ctx.text)
    return lines <= BLOCK_LINE_LIMIT, f"{lines} lines, limit {BLOCK_LINE_LIMIT}"


def check_plan_cap(ctx: BlockContext) -> tuple[bool, str]:
    rows = [(name, int(lines)) for name, lines, _bytes, _sha in _PAYLOAD_ROW.findall(ctx.text)
            if name.strip().endswith("plan.md")]
    if not rows:
        return True, "no plan.md payload in the block's payload table"
    over = [f"{name} at {lines} lines" for name, lines in rows if lines >= PLAN_LINE_LIMIT]
    if over:
        return False, f"{', '.join(over)}; the cap is under {PLAN_LINE_LIMIT}"
    return True, ", ".join(f"{name} at {lines} lines" for name, lines in rows)


def _ledger_reader():
    from packages.orchestration.integrity_gate import _load_ledger_reader

    return _load_ledger_reader()


def check_open_set(ctx: BlockContext) -> tuple[bool, str]:
    stated = sorted({int(n) for n in _OPEN_COUNT.findall(ctx.text)})
    if not stated:
        return True, "the block states no open-findings count"
    measured = len(_ledger_reader().open_finding_ids(ctx.read(LEDGER_PATH)))
    wrong = [n for n in stated if n != measured]
    if wrong:
        return False, f"states {', '.join(map(str, wrong))}; {LEDGER_PATH} holds {measured} open by distinct id"
    return True, f"states {measured}, and {LEDGER_PATH} holds {measured}"


def check_gate_paths(ctx: BlockContext) -> tuple[bool, str]:
    new_files = set(_NEW_FILE.findall(ctx.text))
    named = sorted({path for body in _FENCE.findall(ctx.text) for path in _REPO_PATH.findall(body)})
    missing = [path for path in named if path not in new_files and not (ctx.repo_root / path).exists()]
    if missing:
        return False, f"{len(missing)} of {len(named)} named paths do not resolve: {', '.join(missing)}"
    return True, f"{len(named)} paths named in the block's commands, every one resolves"


def check_new_ids(ctx: BlockContext) -> tuple[bool, str]:
    minted = _REGISTRATION.findall(ctx.text)
    if not minted:
        return True, "the block registers no finding id"
    taken = set(_REGISTRATION.findall(ctx.read(LEDGER_PATH))) | set(_REGISTRATION.findall(ctx.read(ARCHIVE_PATH)))
    clash = sorted({rid for rid in minted if rid in taken} | {rid for rid in minted if minted.count(rid) > 1})
    if clash:
        return False, f"already registered or minted twice: {', '.join(clash)}"
    return True, f"{', '.join(sorted(set(minted)))} new to the ledger and its archive"


def check_gates_before_the_text(ctx: BlockContext) -> tuple[bool, str]:
    claims = _GATES_BEFORE.findall(ctx.text)
    if not claims:
        return True, "the block orders no gates before a commit"
    headers = [(int(m.group(1)), m.start()) for m in _GATE_HEADER.finditer(ctx.text)]
    bodies = {n: ctx.text[start:(headers[i + 1][1] if i + 1 < len(headers) else len(ctx.text))]
              for i, (n, start) in enumerate(headers)}
    late = [f"G{n} runs after {commit}" for first, last, commit in claims
            for n in range(int(first), int(last) + 1) if f"after {commit}" in bodies.get(n, "")]
    if late:
        return False, "; ".join(late)
    return True, "; ".join(f"G{first} to G{last} before {commit}" for first, last, commit in claims)


def check_repeated_runs(ctx: BlockContext) -> tuple[bool, str]:
    # A bare code fence is exempt: its length is Markdown syntax, fixed at three.
    runs = [number for number, line in enumerate(ctx.text.splitlines(), start=1)
            if len(line.strip()) >= 3 and len(set(line.strip())) == 1 and line.strip() != "```"]
    if runs:
        return False, f"lines {', '.join(map(str, runs))} are runs of one repeated character"
    return True, "no line is a run of one repeated character"


RULES: tuple[Rule, ...] = (
    Rule(1, "size", "Count the block's lines. Over 400 (DECISION F105 D5) → split or cut BEFORE "
         "emitting.", check_size),
    Rule(3, "cap-bounded replacements", "`.agent/plan.md` under 50 lines (AGENTS.md)", check_plan_cap),
    Rule(10, "open set recomputed", "Derive the set mechanically from `.agent/live_review.md` at "
         "emission", check_open_set),
    Rule(24, "gate paths resolve", "a path that does not resolve is corrected, or dropped with the "
         "correction stated inline", check_gate_paths),
    Rule(30, "new ids searched first", "Before writing `- R-XXXX`, grep `.agent/live_review.md` for "
         "the defect itself", check_new_ids),
    Rule(31, "gates before the text", "an authored text may claim what a gate showed only when the same "
         "block fixes that the gate runs BEFORE the commit writing that text", check_gates_before_the_text),
    Rule(37, "no unmeasured runs", "no line of a block is a run of a single repeated character unless "
         "its length is stated beside it", check_repeated_runs),
)


def lint_block(text: str, repo_root: Path = REPO_ROOT) -> list[LintResult]:
    """One result per rule, in item order."""
    ctx = BlockContext(text=text, repo_root=repo_root)
    results = []
    for rule in RULES:
        ok, detail = rule.check(ctx)
        results.append(LintResult(rule.item, rule.name, ok, detail, rule.sentence))
    return results


def live_checklist_items(checklist_text: str) -> dict[int, str]:
    """Item number -> item text, for the items the §3 checklist carries NOW.

    Only the checklist's own region is read: the same file numbers other lists as well.
    """
    start = checklist_text.index("Pre-emission block checklist")
    end = checklist_text.index("Why this is on disk and not a habit", start)
    region = checklist_text[start:end]
    heads = list(re.finditer(r"^  (\d+)\. \*\*", region, re.M))
    return {int(m.group(1)): region[m.start():(heads[i + 1].start() if i + 1 < len(heads) else len(region))]
            for i, m in enumerate(heads)}
