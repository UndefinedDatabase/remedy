── STEP T003 batch5 — F262 List commands v2 ────────────────────────
Goal: Wire blocker.list and decision.list into the shared apply_list_options helper (T003), and book round 16's already-PASSED verdict into the ledger.

Bundle:
C0a. Save this entire step block, byte for byte, to a NEW file `.agent/authored/f262-r17.md`.
C0b. Whole-file replace `.agent/last_block.md` with the same bytes (mirror of C0a).
C1. Append GATE16 (below) to `.agent/live_review.md`.
C2. Production change: PAIR B1 + PAIR B2 in `apps/cli/commands/blocker.py`, PAIR D1 + PAIR D2 in `apps/cli/commands/decision.py`, plus TEST T1 (new tests) appended to `tests/cli/test_blocker_cmd.py` and TEST T2 (new tests) appended to `tests/cli/test_decision_cmd.py`. ONE commit covering all four files.
C3. Whole-file replace `.agent/plan.md` with PLAN18 (below).
C4. Rewrite `.agent/handoff.md` (handback) per docs/agents/handback_template.md; this is the round's LAST commit.

============================================================
GATE16 — append verbatim as a new line at the end of `.agent/live_review.md`. The current file ends with NO trailing newline. C1 must: read the current file, append exactly one `\n` character followed by the GATE16 text below (with no trailing newline after it either). Do this with Python (`pathlib.Path.write_bytes`), not a shell append.

GATE16 text (copy exactly, it is a single line with zero internal newlines, 2567 bytes UTF-8):
Gate: R16 — the F262 R16 entry. R16 SHIPPED T003 BATCH 4, `project.list` wired to `apply_list_options` with `default_sort_field="created_at"` — `_list_projects_readonly()` already sorted newest-first (`tests/test_project_registry.py::test_list_sorted_newest_first`), so the shared helper changes nothing observable and needed no D2-style opt-out; dispatch is a lambda, so BOTH the handler body (PAIR P1) and the dispatch site (PAIR P2) needed a pair, unlike tournament.list's single pair — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r16.md`/`.agent/last_block.md` share one sha256 digest, `ca1aaebf4e6024b0a7d98d1faefbc12001bdf0635dc1931c5d7c514213adcc3d`, confirmed by the reviewer's own sha256sum of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff 095cd91bda17a3ae4c25e4f9f52e6b18a19f5c74..94eb67c91cb9c1f28c7f1285d4d6411a475c23e4` for `apps/cli/commands/project.py` and `tests/test_grouped_cli.py` shows exactly PAIR P1 (the apply_list_options wiring inside `_cmd_list_projects`), PAIR P2 (the dispatch lambda), and TEST T1's two new methods (`test_limit_caps_returned_projects`, `test_unknown_sort_field_exits_nonzero`) inserted into `TestProjectListCLI` before `TestJobListCLI`, every other line in both files untouched, confirmed by reading the full diff. `python3 -c "import py_compile; ..."` printed OK for both touched files, run independently by the reviewer. THE GATE15 LEDGER APPEND (commit 6ed533d3) WAS RE-VERIFIED BYTE-EXACT: base 2460225 plus one newline plus GATE15 (2317 bytes, 0 internal newlines) equals 2462543, matching the file's own on-disk size measured immediately after the round. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `python3 -m pytest tests/test_grouped_cli.py -q` read 525 passed (523 pre-existing plus 2 new). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read 646 passed, matching 515+52+21+16+42 exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `94eb67c9`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 2530 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN17 slice against the written file, and its content was read back in full and confirmed byte-identical to the authored text. THE VERDICT IS PASS.

Base file size immediately before C1 must read 2462543 (confirm with a fresh Python byte read before writing). Post-C1 size must read exactly 2465111 (2462543 + 1 + 2567). Verify both numbers yourself and report them.
============================================================

PAIR B1 — apps/cli/commands/blocker.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
def _cmd_blocker_list(
    job_id_str: str,
    *,
    json_output: bool = False,
) -> None:
    from packages.orchestration.stop_reasons import (
        export_stop_reason_json,
        list_stop_reasons,
    )

    stops = list_stop_reasons(job_id_str)

    if json_output:

Replace it with this TO text:
def _cmd_blocker_list(
    job_id_str: str,
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.stop_reasons import (
        export_stop_reason_json,
        list_stop_reasons,
    )

    stops = list_stop_reasons(job_id_str)
    try:
        stops = apply_list_options(
            stops,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda s: s.created_at,
                "status": lambda s: s.status,
                "severity": lambda s: s.severity,
            },
            default_sort_field="created_at",
            date_getter=lambda s: s.created_at or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:

PAIR B2 — apps/cli/commands/blocker.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
    "blocker.list": lambda args: _cmd_blocker_list(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),

Replace it with this TO text:
    "blocker.list": lambda args: _cmd_blocker_list(
        args.job_id,
        json_output=getattr(args, "json", False),
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),

PAIR D1 — apps/cli/commands/decision.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
def _cmd_decision_list(job_id_str: str, *, json_output: bool = False) -> None:
    from packages.orchestration.decision_queue import export_decision_json, list_decisions

    job, events, jid = _load_job_events(job_id_str)
    decisions = list_decisions(job, events)

    if json_output:

Replace it with this TO text:
def _cmd_decision_list(
    job_id_str: str,
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.decision_queue import export_decision_json, list_decisions
    from packages.orchestration.list_options import ListOptionError, apply_list_options

    job, events, jid = _load_job_events(job_id_str)
    decisions = list_decisions(job, events)
    try:
        decisions = apply_list_options(
            decisions,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda d: d.created_at,
                "status": lambda d: d.status,
                "severity": lambda d: d.severity,
            },
            default_sort_field="created_at",
            date_getter=lambda d: d.created_at or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:

PAIR D2 — apps/cli/commands/decision.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
    "decision.list": lambda args: _cmd_decision_list(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),

Replace it with this TO text:
    "decision.list": lambda args: _cmd_decision_list(
        args.job_id,
        json_output=getattr(args, "json", False),
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),

Note: `sys` is already imported at module scope in BOTH blocker.py and decision.py (line 6, `import sys` in each) — do not add duplicate imports.

TEST T1 — tests/cli/test_blocker_cmd.py — append two new test functions at the END of the file (the file currently ends with `assert "resolved=2026-09-02T00:00:00+00:00" in out` as the last line, no trailing blank line after the class body). Before applying, re-read the CURRENT file to find its exact final line and confirm your insertion point is genuinely the end of the file.

Append this new content, as a new top-level class after the existing `TestBlockerListText` class (two blank lines before it, matching PEP8 spacing already used elsewhere in the file):

class TestBlockerListOptions:
    @patch(_LIST_STOPS)
    def test_limit_caps_returned_blockers(self, mock_list, capsys):
        mock_list.return_value = [_stop(), _stop(), _stop()]
        from apps.cli.commands.blocker import _cmd_blocker_list
        _cmd_blocker_list("job-1", json_output=True, limit="2")
        import json
        out = capsys.readouterr().out
        data = json.loads(out)
        assert len(data["stop_reasons"]) == 2

    @patch(_LIST_STOPS)
    def test_unknown_sort_field_exits_nonzero(self, mock_list, capsys):
        mock_list.return_value = [_stop()]
        from apps.cli.commands.blocker import _cmd_blocker_list
        with pytest.raises(SystemExit) as exc:
            _cmd_blocker_list("job-1", json_output=True, sort="bogus")
        assert exc.value.code == 1

This test file does not currently import `pytest` at module scope — add `import pytest` to its existing import block (alongside `from unittest.mock import patch`) as part of this same commit, since `pytest.raises` is used by the new test.

TEST T2 — tests/cli/test_decision_cmd.py — append two new test functions at the END of the file (the file currently ends with `assert "resolved=2026-09-02T00:00:00+00:00" in out` as the last line). Before applying, re-read the CURRENT file to find its exact final line and confirm your insertion point is genuinely the end of the file.

Append this new content, as a new top-level class after the existing `TestDecisionListText` class (two blank lines before it, matching PEP8 spacing already used elsewhere in the file):

class TestDecisionListOptions:
    @patch(_LIST_DECISIONS)
    @patch(_LOAD_JOB_EVENTS)
    def test_limit_caps_returned_decisions(self, mock_load, mock_list, capsys):
        mock_load.return_value = (None, [], "job-1")
        mock_list.return_value = [_decision(), _decision(), _decision()]
        from apps.cli.commands.decision import _cmd_decision_list
        _cmd_decision_list("job-1", json_output=True, limit="2")
        import json
        out = capsys.readouterr().out
        data = json.loads(out)
        assert len(data["decisions"]) == 2

    @patch(_LIST_DECISIONS)
    @patch(_LOAD_JOB_EVENTS)
    def test_unknown_sort_field_exits_nonzero(self, mock_load, mock_list, capsys):
        mock_load.return_value = (None, [], "job-1")
        mock_list.return_value = [_decision()]
        from apps.cli.commands.decision import _cmd_decision_list
        with pytest.raises(SystemExit) as exc:
            _cmd_decision_list("job-1", json_output=True, sort="bogus")
        assert exc.value.code == 1

This test file does not currently import `pytest` at module scope — add `import pytest` to its existing import block (alongside `from unittest.mock import patch`) as part of this same commit, since `pytest.raises` is used by the new test.

Commit C2 covers all four files (blocker.py's two pairs, decision.py's two pairs, and both test files' appends plus their new `import pytest` lines) as ONE commit.

============================================================
PLAN18 — whole-file replace of `.agent/plan.md`. Byte length must be exactly 2159 (UTF-8), confirm with a binary-mode byte comparison after writing (read the file back and compare bytes, not text-mode — Write-tool trailing-newline drift has bitten prior rounds).

PLAN18 text (copy exactly):
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 17, session 6 - T003 batch 5: `blocker.list` and `decision.list`
wired to `apply_list_options`, both `default_sort_field="created_at"`.
Both are job-scoped, return typed rows (StopReason/HumanDecision) whose
`created_at` is already a plain ISO string (no `.isoformat()` needed).
Neither store's existing order is meaningful, and neither has an
order-asserting test, so no D2-style opt-out was needed. Both
dispatch via lambda, so each needed two pairs (handler + dispatch).

## Next Steps

- T003 batch 6: wire review.list, propose.list,
  external-builder.submission-list - same drill, grep each command's
  own tests for an order-asserting test FIRST (DECISION F262 D2).
- patch.list (approval_queue.py's table renderer) and loop.list
  (two-collection rows) still need their own look before wiring -
  neither is a plain single-collection list like the batches so far.
  config.list/worker.list/execution.list stay excused per Risks.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
- Once every command is wired, add an integration-level smoke test
  proving the ten-second demo in Acceptance.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order (queue.list's
  priority, DECISION F262 D2) opts out via `default_sort_field=None` -
  audit each remaining command for this shape before wiring it.

============================================================
CONSTRAINTS:
1. Do not touch any list command other than blocker.list/decision.list this round.
2. Do not widen or change `apply_list_options` itself (packages/orchestration/list_options.py) — it is unchanged this round.
3. No file besides these may be written: `apps/cli/commands/blocker.py`, `apps/cli/commands/decision.py`, `tests/cli/test_blocker_cmd.py`, `tests/cli/test_decision_cmd.py`, `.agent/authored/f262-r17.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
4. Re-confirm each FROM string's exact occurrence count (must be 1) against the file's CURRENT on-disk content immediately before applying — not against the copy quoted in this prompt.
5. Commit order is exactly C0a, C0b, C1, C2, C3, C4, each its own commit.
6. Run `git status --porcelain` after every commit; it must be empty before proceeding.
7. `.agent/STOP` must be absent before C0a and re-checked before C4. If it appears, stop immediately, finish only a half-written commit, and write the handoff reporting the STOP instead of continuing.
8. Capture REAL exit codes for every command — do not report "green" as a bare word.
9. Known sandbox quirks in this repo (from prior rounds): `python3 -m py_compile <files>` as a literal multi-arg command has sometimes been denied by the Bash sandbox — if denied, substitute `python3 -c "import py_compile; py_compile.compile('path/a.py', doraise=True); ...; print('OK')"` and declare the substitution. `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`, and `cp` are denied outright — use `monkeypatch`/`python3 -c "import shutil; shutil.copyfile(a,b)"` if ever needed. Never use a sandbox-override flag to route around a denial.

DONE WHEN (run every one of these EXACTLY as written and record the REAL, complete output of each in your handback — quote actual pytest/py_compile output, do not summarize as "passed"):
G1. `python3 -c "import py_compile; py_compile.compile('apps/cli/commands/blocker.py', doraise=True); py_compile.compile('apps/cli/commands/decision.py', doraise=True); py_compile.compile('tests/cli/test_blocker_cmd.py', doraise=True); py_compile.compile('tests/cli/test_decision_cmd.py', doraise=True); print('OK')"` → must print OK.
G2. `python3 -m pytest tests/cli/test_blocker_cmd.py tests/cli/test_decision_cmd.py -q` → expect 8 passed (4 pre-existing + 4 new). Report the exact number.
G3. `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` → expect 646 passed (515+52+21+16+42), unmoved. Report the exact number.
G4. `sha256sum .agent/authored/f262-r17.md .agent/last_block.md` → must print one identical digest for both files. Report both digests.
G5. Byte-read `.agent/live_review.md` immediately before C1 and immediately after C1 (Python, binary mode) → before must be 2462543, after must be 2465111. Report both numbers.
G6. Byte-read `.agent/plan.md` immediately after C3, binary mode → must be exactly 2159 bytes, byte-for-byte equal to the PLAN18 text above. Report the byte count and whether it matched exactly.
G7. `git status --porcelain` → empty, checked before C0a and immediately before C4. Report both checks.
G8. `git ls-files .remedy-wt` → empty. Report the output (should be nothing).

HANDBACK: write a full completion report and rewrite `.agent/handoff.md` per docs/agents/handback_template.md and AGENTS.md's "### handoff.md" section — include the changed-files table (path, +/-, reason) for every commit, an item-status table (Item | Status | Reason) covering every bundle item (C0a..C4, and each gate G1..G8), the real verification results for every gate above, the SESSION NUMBER (this is SESSION 6 of feature F262, round 17), and the next expected action (round 18: T003 batch 6 — wire review.list, propose.list, external-builder.submission-list per PLAN18's Next Steps, re-checking each command's own tests for an order-asserting test first per DECISION F262 D2's precedent). After the handoff commit (C4), run `git push -u origin feature/f262-list-commands-v2` and report the push result. Do NOT create a PR. Do NOT merge anything. Do NOT touch `main`.
──────────────────────────────────────────────────────────────