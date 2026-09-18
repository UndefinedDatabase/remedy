# F281 Round 17 — step block

## Goal

Book round 16's independently-reviewed PASS, then land the `remedy doctor
core` dead-commands SECTION (DECISION F281 D6), clearing the Acceptance line
"`remedy doctor core` lists dead commands as a section and the section is
empty." Scope read from `T2_F271.md`'s Design (c) before authoring, per
PLAN16's Risks: F271 (later) owns the closure-precondition wiring and the
fixture-based red-proof; this round lands only the detection mechanism and
the always-shown section, expected empty, matching T2_F281.md's narrower
Acceptance wording. Pre-verified in a disposable worktree (removed after
use): every edit applied cleanly, every targeted test read green, the real
CLI output showed `dead commands:\n    (none)`, and a mutation red-proof
(removing the AST-pair signal) reddened exactly the two dependent tests —
including the real catalog's own `dev.smoke-help`, tested only via argv.

## Bundle

C0a: save this block verbatim to `.agent/authored/f281-r17.md`.
C0b: mirror this block verbatim to `.agent/last_block.md`.
C1: RECORD16 + DECISION F281 D6 + PLAN17 — one commit.
C2: CODE — 2 new files (`packages/orchestration/dead_command_check.py`,
`tests/orchestration/test_dead_command_check.py`) and 4 edits across
`apps/cli/commands/worker_facade_cmd.py` (2 edits),
`tests/cli/test_worker_facade_cmd.py` (1) and
`tests/orchestration/import_reachability_allowlist.txt` (1) — one commit.
C3: HANDBACK.

## C1 — RECORD16 + DECISION F281 D6 + PLAN17

### RECORD16 — append to `.agent/live_review.md`, after its current last
line, separated by exactly one blank line, verbatim:

```
Gate: F281 R16 — the F281 round 16 entry. VERDICT PASS. Written by the planner and reviewer of F281's third session after reading the committed range `2322e12c`..`c01a6f7d` (commits `e0d8ff22`, `d46da12f`, `65097ff2`, `c01a6f7d`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f281-r16.md` and `.agent/last_block.md` are byte-identical, reproduced directly by `cmp`, sha256 `06ee94fbf111e411ec970a713a6774cd65f51fef7328dcee8ba8474f5839ad77` for the authored copy. THE CODE, reproduced by `git show d46da12f`: `apps/cli/command_catalog.py` gains `VISIBLE_GROUP_ORDER` exactly as ordered, immediately after `GROUPS`'s closing brace; `apps/cli/grouped.py` imports it and `_print_root_help`'s default branch reads `[(gid, GROUPS[gid].description) for gid in VISIBLE_GROUP_ORDER]` in place of the old `GROUPS.items()` filter; the `--all-commands` branch is untouched; the three test files gain exactly the two new pinning classes and the stale-canary rewrite the block ordered — the commit's path set is exactly the five declared files. THE MEASUREMENT, reproduced directly at HEAD: `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py tests/test_help_renderer.py -q` reads `352 passed`; `python3 -m pytest tests/cli/test_golden_path.py -q` reads `42 passed`; `python3 -m ruff check apps/cli/command_catalog.py apps/cli/grouped.py tests/test_command_catalog.py tests/test_grouped_cli.py tests/cli/test_golden_path.py` reads `All checks passed!`. THE G4 DIRECT MEASUREMENT, reproduced directly: a fresh import of `VISIBLE_GROUP_ORDER` and a row-scan of the real `python3 -m apps.cli.grouped --help` output both read `['do', 'mission', 'job', 'run', 'decision', 'status', 'stats', 'teacher', 'memory', 'ui', 'config', 'doctor', 'project', 'init', 'worker', 'runtime']`, identical. THE G5 MUTATION RED-PROOF, independently re-run by the reviewer in a disposable worktree (`git worktree add --detach` at `d46da12f`, removed after): with the round's edits applied, `python3 -m pytest tests/test_grouped_cli.py::TestRootHelpVisibleOrder tests/cli/test_golden_path.py::TestHelpPinning -q` reads `2 passed`; reverting only the `_print_root_help` edit back to its `GROUPS.items()` FROM text reddens both tests at the exact index the handback names (`'status' != 'mission'` at index 1); re-applying restores `2 passed`. THE TREE: `git status --porcelain` empty, `git worktree list` one row, HEAD `c01a6f7d` matches `origin/feature/f281-cli-help-surface`. WHY PASS: every byte independently reproduces, the code edit is correct and complete, the mutation red-proof confirms it is load-bearing, and the real CLI output matches `VISIBLE_GROUP_ORDER` exactly.
```

### DECISION — append to `.agent/decisions.md`, after its current last
line, separated by exactly one blank line, verbatim:

```
## DECISION F281 D6 (2026-09-17, F281 round 17) — `remedy doctor core`'s dead-commands section detects a dead command by FOUR independent reference signals, never by the handler function's own `__name__`

CONTEXT. `docs/roadmap/features/T2_F281.md`'s Acceptance list requires:
"`remedy doctor core` lists dead commands as a section and the section is
empty." `docs/roadmap/features/T2_F271.md`'s Design (c) names the fuller
mechanism — "a catalog command whose handler is referenced by no test and no
script is reported as a section" — but F271 itself runs AFTER F281 and owns
the closure-precondition wiring and the fixture-based red-proof (planting a
fake dead command and seeing it listed); PLAN16's Risks scoped this round to
the section and its detection mechanism alone.

MEASURED. `collect_all_handlers()` maps 146 of 146 catalog command_ids to a
handler; 122 are `lambda`s closing over the real implementation function
(`"job.list": lambda args: _cmd_list_jobs(...)`), so `__name__` reads the
literal `"<lambda>"` for most commands — a check keyed on it alone would call
nearly every command dead. A design using only `co_names` plus the dotted and
spaced forms, scanned as text over `tests/` + `scripts/`, measured 8 false
"dead" commands (e.g. `roadmap.status`, `dev.smoke-help`), each genuinely
tested only via a `subprocess` argv list holding the group and the
subcommand as two separate string tokens (`["roadmap", "status"]`), the same
blind spot F275 round 33's own command-deletion sweep recorded: no substring
scan sees two list elements as one command.

CHOSEN. `packages/orchestration/dead_command_check.py` (new module, no
`apps.cli.*` import, mirroring `dead_model_list.py`'s isolation) exposes
`dead_command_ids(catalog, handlers, root=None)`; a command counts as
referenced when ANY of four signals holds: (1) an `ast`-detected adjacent
string pair `("<group>", "<subcommand>")` in a list/tuple literal under
`root`'s `tests/` or `scripts/` — the fix for the argv-list blind spot; (2)
the spaced form as a substring; (3) the dotted `command_id` as a substring;
(4) any of the handler's own `co_names` (plus `__name__` when not
`"<lambda>"`) as a whole-word match. Wired into `_cmd_doctor_core` as a HARD
check (`dead_command_scan`) plus an ALWAYS-SHOWN section, never conditional
on non-emptiness like the F254 warnings block — the Acceptance line lists the
section itself, so a later fixture command must appear the moment it exists.
`--json` gets a new `dead_commands` key. Measured on the shipped catalog: `0
dead of 146`, matching T2_F271.md's "Expected empty after F261."

ALTERNATIVES CONSIDERED. `__name__` alone — rejected: 122 of 146 handlers
share the literal name `"<lambda>"`. Text scan only (no AST pair) —
rejected: measured 8 false positives, training an operator to ignore the
section exactly as `_warn`'s docstring warns against. A `CommandEntry.handler`
field instead of `collect_all_handlers()` — deferred: a catalog-shape change
outside this round's scope and T2_F271's "Do not touch"; the plain-argument
shape lets a later feature swap the source without touching this module.

CONSEQUENCE. `remedy doctor core` always prints `dead commands:`, `(none)`
today; `--json` always carries `"dead_commands": []` today.
`test_dead_command_check.py` pins the algorithm (a synthetic dead command is
found, a synthetic argv-list-only reference is not) and asserts the real
catalog reads empty; `test_worker_facade_cmd.py` pins the section's presence
in both render modes. The allowlist gains one line, mirroring how
`dead_model_list` was added — the new module is stdlib-only, so no further
entry follows. F271 layers the closure-precondition wiring and the
fixture-based red-proof on top of `dead_command_ids` without redoing the
mechanism. HOW TO REVERSE: revert this round's C2 commit; delete this
paragraph.
```

### PLAN17 — replace the entire content of `.agent/plan.md` with exactly:

```
# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 17. C1 books round 16's independently-reviewed PASS and adds DECISION
F281 D6. C2 lands `packages/orchestration/dead_command_check.py`
(`dead_command_ids`, a four-signal reference check: an AST-detected argv-list
pair, the spaced form, the dotted `command_id`, and the handler's own
referenced names) and wires it into `remedy doctor core` as an always-shown
`dead commands:` section plus a `dead_command_scan` hard check; two new
tests pin the section's presence in both render modes and the algorithm
itself is pinned in its own new test file, which also asserts the real
catalog reads empty. One line added to the import-reachability allowlist.
After this round: `remedy doctor core` lists dead commands as a section and
the section reads empty on the shipped catalog, clearing that Acceptance
line; F271 (later) owns the closure-precondition wiring and the
fixture-based red-proof.

## Next Steps

1. Remaining Acceptance items: R-0805 (`ui status` dead-session pruning),
   R-0809 (one id-error-message shape for mission/job/run), R-0895 (README
   quickstart) and R-0934 (advertised-flag scanner skips a quoted argument)
   are all OPEN. R-0895 runs last (orchestrator brief: it quotes the
   finished catalog). Session 3 begins at this round; continuing is allowed
   while context comfortably suffices (amend0905-throughput's 6-to-8 target).

## Risks

- None carried from round 16: DECISION F281 D6 resolves the design question
  PLAN16 flagged, measured non-vacuous by this round's mutation red-proof.
```

## C2 — CODE (2 new files, 4 edits across 3 existing files)

Apply each item below EXACTLY. For the two new files, `git add` a file that
does not yet exist. For each FROM → TO pair, the FROM string must appear
verbatim EXACTLY ONCE; if it does not, STOP and report the exact mismatch
rather than guessing or forcing it.

### Edit 1 — CREATE `packages/orchestration/dead_command_check.py` with
exactly this content:

```python
"""T2_F271 design (c), scoped narrow by F281 (T2_F281.md Acceptance: the
section only). A catalog command is DEAD when none of its handler's
underlying names, its dotted command_id, its spaced ``<group> <subcommand>``
form, or an adjacent ``("<group>", "<subcommand>")`` list/tuple literal
appears anywhere under a search root's ``tests/`` or ``scripts/`` directory.

The fourth signal exists because a CLI test invoked as an argv list —
``subprocess.run([*_CLI, "job", "run-next", short_id])`` — holds the group and
the subcommand as two separate string tokens that neither the spaced nor the
dotted text scan ever matches (the blind spot F275 round 33's command-deletion
sweep hit). Text scans alone would misreport a subprocess-tested command as
dead; the AST pass over list/tuple literals is what makes this check answer
the real question rather than a shape it resembles.

This module never imports ``apps.cli.command_catalog``: the caller passes the
catalog's own ``(command_id, group_id, subcommand)`` triples and its handler
table, so a CLI-layer import cycle can never form here.

Public API::

    dead_command_ids(catalog, handlers, root=None) -> list[str]
"""

from __future__ import annotations

import ast
import re
from collections.abc import Callable, Iterable
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SEARCH_DIRS = ("tests", "scripts")


def _handler_names(fn: Callable[..., object]) -> frozenset[str]:
    """Every identifier the handler's own code references, by name.

    Most catalog handlers are a ``lambda`` closing over the real
    implementation function (``lambda args: _cmd_list_jobs(...)``), so the
    lambda's own ``__name__`` is always the literal string ``"<lambda>"`` and
    never the name a test actually imports; ``co_names`` reaches through to
    the real callee.
    """
    names = set(fn.__code__.co_names)
    if fn.__name__ != "<lambda>":
        names.add(fn.__name__)
    return frozenset(n for n in names if not n.startswith("__"))


def _iter_search_files(root: Path) -> Iterable[Path]:
    for rel in _SEARCH_DIRS:
        d = root / rel
        if d.is_dir():
            yield from (p for p in d.rglob("*") if p.is_file())


def _adjacent_string_pairs(tree: ast.AST) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.List, ast.Tuple)):
            elts = node.elts
            for i in range(len(elts) - 1):
                a, b = elts[i], elts[i + 1]
                if (isinstance(a, ast.Constant) and isinstance(a.value, str)
                        and isinstance(b, ast.Constant) and isinstance(b.value, str)):
                    pairs.add((a.value, b.value))
    return pairs


def dead_command_ids(
    catalog: Iterable[tuple[str, str, str]],
    handlers: dict[str, Callable[..., object]],
    *,
    root: Path | None = None,
) -> list[str]:
    """The sorted command_ids of every catalog command referenced nowhere.

    ``catalog`` is an iterable of ``(command_id, group_id, subcommand)``
    triples, taken from the caller's own ``CATALOG`` entries.
    """
    root = root if root is not None else _REPO_ROOT
    texts: list[str] = []
    pairs: set[tuple[str, str]] = set()
    for path in _iter_search_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        texts.append(text)
        if path.suffix == ".py":
            try:
                pairs |= _adjacent_string_pairs(ast.parse(text))
            except SyntaxError:
                continue

    dead: list[str] = []
    for command_id, group_id, subcommand in catalog:
        if (group_id, subcommand) in pairs:
            continue
        spaced = f"{group_id} {subcommand}"
        if any(spaced in t or command_id in t for t in texts):
            continue
        patterns = [re.compile(r"\b" + re.escape(n) + r"\b") for n in _handler_names(handlers[command_id])]
        if any(p.search(t) for t in texts for p in patterns):
            continue
        dead.append(command_id)
    return sorted(dead)
```

### Edit 2 — CREATE `tests/orchestration/test_dead_command_check.py` with
exactly this content:

```python
"""Tests for packages.orchestration.dead_command_check.dead_command_ids.

Pure in-process: every test builds its own tmp_path search root with a
synthetic tests/ and scripts/ directory, except the one integration test that
proves the real catalog and the real repo's tests/ + scripts/ read empty.
"""
from __future__ import annotations

from packages.orchestration.dead_command_check import dead_command_ids


def _fn(name):
    ns: dict = {}
    exec(f"def {name}(args):\n    pass\n", ns)
    return ns[name]


class TestDeadCommandIds:
    def test_a_command_referenced_nowhere_is_dead(self, tmp_path):
        (tmp_path / "tests").mkdir()
        (tmp_path / "scripts").mkdir()
        (tmp_path / "tests" / "test_x.py").write_text("live_handler()\n", encoding="utf-8")
        catalog = [("do.run", "do", "run"), ("ghost.vanish", "ghost", "vanish")]
        handlers = {"do.run": _fn("live_handler"), "ghost.vanish": _fn("dead_handler")}
        assert dead_command_ids(catalog, handlers, root=tmp_path) == ["ghost.vanish"]

    def test_an_argv_list_pair_counts_as_a_reference(self, tmp_path):
        (tmp_path / "tests").mkdir()
        (tmp_path / "scripts").mkdir()
        (tmp_path / "tests" / "test_x.py").write_text(
            'subprocess.run([*_CLI, "job", "run-next", short_id])\n', encoding="utf-8",
        )
        catalog = [("job.run-next", "job", "run-next")]
        handlers = {"job.run-next": _fn("unrelated_name")}
        assert dead_command_ids(catalog, handlers, root=tmp_path) == []

    def test_the_real_catalog_has_no_dead_commands(self):
        from apps.cli.command_catalog import CATALOG
        from apps.cli.commands import collect_all_handlers

        triples = [(e.command_id, e.group_id, e.subcommand) for e in CATALOG]
        assert dead_command_ids(triples, collect_all_handlers()) == []
```

### Edit 3 — `apps/cli/commands/worker_facade_cmd.py`, insert the scan before
`blockers` and add the key to `result`. FROM (whole block):
```
            _warn("dead_model_comparison", comparison_failed, comparison_failed)

    blockers: list[str] = [str(c["check"]) for c in checks if not c["ok"]]
    ready = len(blockers) == 0

    result: dict[str, Any] = {
        "ready": ready,
        "checks": checks,
        "blockers": blockers,
        "warnings": warnings,
    }
```
TO:
```
            _warn("dead_model_comparison", comparison_failed, comparison_failed)

    # -----------------------------------------------------------------
    # T2_F271 design (c), scoped narrow by F281 (T2_F281.md Acceptance): the
    # SECTION only — always shown, empty on the shipped catalog. The
    # closure-precondition wiring and the fixture-based red-proof (planting a
    # fake dead command and seeing it listed) are F271's, not this round's.
    # -----------------------------------------------------------------
    try:
        from packages.orchestration.dead_command_check import dead_command_ids
        cat_mod = importlib.import_module("apps.cli.command_catalog")
        commands_mod = importlib.import_module("apps.cli.commands")
        dead_commands = dead_command_ids(
            ((e.command_id, e.group_id, e.subcommand) for e in cat_mod.CATALOG),
            commands_mod.collect_all_handlers(),
        )
        _check("dead_command_scan", True,
               f"{len(dead_commands)} dead of {len(cat_mod.CATALOG)} commands")
    except Exception as exc:
        dead_commands = []
        _check("dead_command_scan", False, _safe_err(exc))

    blockers: list[str] = [str(c["check"]) for c in checks if not c["ok"]]
    ready = len(blockers) == 0

    result: dict[str, Any] = {
        "ready": ready,
        "checks": checks,
        "blockers": blockers,
        "warnings": warnings,
        "dead_commands": dead_commands,
    }
```

### Edit 4 — `apps/cli/commands/worker_facade_cmd.py`, print the section
always. FROM (whole block):
```
    if warnings:
        print("  warnings (advisory — these do not affect READY):")
        for w in warnings:
            # The compact rendering; `--json` carries the full `detail`.
            print(f"  [WARN] {w['warning']}: {w['summary']}")
        print("  (run with --json for each warning's full recorded reason)")
```
TO:
```
    if warnings:
        print("  warnings (advisory — these do not affect READY):")
        for w in warnings:
            # The compact rendering; `--json` carries the full `detail`.
            print(f"  [WARN] {w['warning']}: {w['summary']}")
        print("  (run with --json for each warning's full recorded reason)")
    print("  dead commands:")
    if dead_commands:
        for cid in dead_commands:
            print(f"    {cid}")
    else:
        print("    (none)")
```

### Edit 5 — `tests/cli/test_worker_facade_cmd.py`, insert the new test class
immediately before `class TestDoctorCoreFromAnotherDirectory:` (an APPEND: TO
contains FROM verbatim). FROM:
```
class TestDoctorCoreFromAnotherDirectory:
```
TO:
```
class TestDoctorCoreDeadCommands:
    """T2_F271 design (c), scoped narrow by F281: the section only, always
    shown — empty on the shipped catalog."""

    def test_text_mode_shows_the_section_empty(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=False))
        out = capsys.readouterr().out
        assert "dead commands:" in out
        assert "(none)" in out

    def test_json_mode_carries_the_key_empty(self, capsys):
        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core
        _cmd_doctor_core(_ns(json=True))
        out = json.loads(capsys.readouterr().out)
        assert out["dead_commands"] == []


class TestDoctorCoreFromAnotherDirectory:
```

### Edit 6 — `tests/orchestration/import_reachability_allowlist.txt`, add one
line (an APPEND: TO contains FROM verbatim). FROM:
```
packages.orchestration.data_paths
packages.orchestration.dead_model_list
```
TO:
```
packages.orchestration.data_paths
packages.orchestration.dead_command_check
packages.orchestration.dead_model_list
```

## Constraints

- The C2 commit's path set is exactly five files:
  `packages/orchestration/dead_command_check.py` (new),
  `tests/orchestration/test_dead_command_check.py` (new),
  `apps/cli/commands/worker_facade_cmd.py`,
  `tests/cli/test_worker_facade_cmd.py`,
  `tests/orchestration/import_reachability_allowlist.txt`.
- Bare `ruff` is denied to this session's shell; use `python3 -m ruff check
  <path>`.
- `dead_command_check.py` imports no `apps.*` module — it takes the catalog
  triples and the handler table as plain arguments (DECISION F281 D6).
- Do not add `packages.orchestration.dead_command_check` anywhere except the
  one allowlist line named in Edit 6.
- No `.agent/operator_questions.md` entry this round: the detection mechanism
  is advisory-only (never affects `ready`) and the design is fully measured
  in DECISION F281 D6, not a product-facing policy choice.
- Do not touch `docs/roadmap/features/T2_F271.md` or `T2_F281.md`.

## Gates (at most six; run and record real exit codes)

- G1 TARGETED: `python3 -m pytest tests/orchestration/test_dead_command_check.py
  tests/cli/test_worker_facade_cmd.py tests/orchestration/test_import_reachability.py -q`
  — expect `45 passed` (3 new + 39 [37 baseline + 2 new] + 3 unchanged).
- G2 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` — expect
  `42 passed` (unchanged).
- G3 RUFF: `python3 -m ruff check packages/orchestration/dead_command_check.py
  apps/cli/commands/worker_facade_cmd.py
  tests/orchestration/test_dead_command_check.py
  tests/cli/test_worker_facade_cmd.py` reads `All checks passed!`.
- G4 DIRECT MEASUREMENT: `python3 -m apps.cli.grouped doctor core` prints a
  `dead commands:` line followed by `    (none)`; `python3 -m apps.cli.grouped
  doctor core --json`, parsed, has `"dead_commands": []`.
- G5 MUTATION RED-PROOF, in a disposable git worktree (`git worktree add
  --detach`, removed after use): with this round's edits applied, `python3 -m
  pytest tests/orchestration/test_dead_command_check.py -q` reads `3 passed`;
  then remove ONLY the `if (group_id, subcommand) in pairs:\n    continue`
  guard from `dead_command_check.py`'s `dead_command_ids` (leaving everything
  else applied) and re-run the same command — expect exactly
  `test_an_argv_list_pair_counts_as_a_reference` AND
  `test_the_real_catalog_has_no_dead_commands` to FAIL (`2 failed, 1 passed`),
  the second failing on the real catalog's own `dev.smoke-help`; then restore
  the guard and confirm `3 passed` again before deleting the worktree.
- G6 TREE: `git status --porcelain` empty, `git worktree list` shows only the
  primary checkout, HEAD matches `origin/feature/f281-cli-help-surface` after
  push. Re-run this LITERALLY as the LAST action before writing the handback.

## Done-when

C1 and C2 are committed with the exact path sets named above; G1-G6 all pass
with real recorded output; the branch is pushed; `.agent/handoff.md` is
rewritten as C3 naming this round, its commits, its verification results, and
the next expected action (round 18 claims the next unverified Acceptance
line — R-0805, R-0809, R-0895 or R-0934; R-0895 last). Any worker correction
to this block is stated explicitly under "Deviations & assumptions".
