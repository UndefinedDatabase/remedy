── STEP T003 batch4 — F262 List commands v2 ────────────────────────
Goal: Wire project.list into the shared apply_list_options helper (T003), following the exact pattern round 15 used for tournament.list, and book round 15's already-PASSED verdict into the ledger.

Bundle:
C0a. Save this entire step block, byte for byte, to a NEW file `.agent/authored/f262-r16.md`.
C0b. Whole-file replace `.agent/last_block.md` with the same bytes (mirror of C0a).
C1. Append GATE15 (below) to `.agent/live_review.md`.
C2. Production change: PAIR P1 + PAIR P2 in `apps/cli/commands/project.py`, plus TEST T1 appended to `tests/test_grouped_cli.py`. ONE commit covering both files.
C3. Whole-file replace `.agent/plan.md` with PLAN17 (below).
C4. Rewrite `.agent/handoff.md` (handback) per docs/agents/handback_template.md; this is the round's LAST commit.

============================================================
GATE15 — append verbatim as a new line at the end of `.agent/live_review.md`. The current file ends with NO trailing newline. C1 must: read the current file, append exactly one `\n` character followed by the GATE15 text below (with no trailing newline after it either — the file must still end with no trailing newline, matching every prior round's convention). Do this with Python (`pathlib.Path.write_bytes`), not a shell append, to control the exact bytes.

GATE15 text (copy exactly, it is a single line with zero internal newlines, 2317 bytes UTF-8):
Gate: R15 — the F262 R15 entry. R15 SHIPPED T003 BATCH 3, `tournament.list` wired to `apply_list_options` with `default_sort_field="created_at"` — `list_tournament_reports()`'s own order (`sorted(root.iterdir())`, an arbitrary on-disk directory-name order with no operational meaning) needed no D2-style opt-out, unlike `queue.list` — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r15.md`/`.agent/last_block.md` share one sha256 digest, `3f3043f01bee72369808de89ae2e4efe755f3570aa7b11fe3d5c9a38e8257fcf`, confirmed by the reviewer's own sha256sum of both committed files, over 225 lines. THE DIFF WAS READ, NOT ONLY GATED: `git diff 60fe2ed19ff4f1f8c0c888139cb5ff356175e031..0fc3b66e2cc1301606942ce3ab0c94c9e83bfce6` for `apps/cli/commands/tournament_cmd.py` and `tests/cli/test_tournament_cli.py` shows exactly PAIR P1 (the apply_list_options wiring inside `_cmd_tournament_list`) and TEST T1's two new functions (`test_limit_caps_the_report_count`, `test_unknown_sort_field_exits_nonzero`), every other line in both files untouched, confirmed by reading the full diff. `python3 -c "import py_compile; ..."` (the same substitution the handback declared) printed OK for both touched files, run independently by the reviewer. THE GATE14 LEDGER APPEND (commit 04f07b8a) WAS RE-VERIFIED BYTE-EXACT: base 2457413 plus one newline plus GATE14 (2811 bytes, 0 internal newlines) equals 2460225, matching the file's own on-disk size measured immediately before this entry. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `python3 -m pytest tests/cli/test_tournament_cli.py -q` read 10 passed (8 pre-existing plus 2 new). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read 646 passed, matching 515+52+21+16+42 exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `095cd91b`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 2616 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN16 slice against the written file. THE VERDICT IS PASS.

Base file size immediately before C1 must read 2460225 (confirm with a fresh Python byte read before writing). Post-C1 size must read exactly 2462543 (2460225 + 1 + 2317). Verify both numbers yourself and report them.
============================================================

PAIR P1 — apps/cli/commands/project.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
def _cmd_list_projects(*, json_output: bool = False) -> None:
    from packages.orchestration.project_registry import _list_projects_readonly
    projects = _list_projects_readonly()
    if json_output:

Replace it with this TO text:
def _cmd_list_projects(
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.project_registry import _list_projects_readonly
    projects = _list_projects_readonly()
    try:
        projects = apply_list_options(
            projects,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda p: p.created_at,
                "name": lambda p: p.name,
            },
            default_sort_field="created_at",
            date_getter=lambda p: p.created_at.isoformat(),
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    if json_output:

Note: `sys` is already imported at module scope in project.py (line 6, `import sys`) — do not add a duplicate import.

PAIR P2 — apps/cli/commands/project.py — REWRITE. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
    "project.list": lambda args: _cmd_list_projects(json_output=args.json),

Replace it with this TO text:
    "project.list": lambda args: _cmd_list_projects(
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),

TEST T1 — tests/test_grouped_cli.py — insert two new test methods into class TestProjectListCLI, immediately before class TestJobListCLI. Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
        text = buf.getvalue()
        assert "created=" in text


class TestJobListCLI:

Replace it with this TO text (note it contains the FROM text as its head, followed by two new test methods, then the same two blank lines and class line):
        text = buf.getvalue()
        assert "created=" in text

    def test_limit_caps_returned_projects(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import RemyProject, save_project
        for i in range(3):
            save_project(RemyProject(name=f"p{i}", slug=f"p{i}"))
        from apps.cli.commands.project import _cmd_list_projects
        buf = StringIO()
        monkeypatch.setattr("sys.stdout", buf)
        _cmd_list_projects(json_output=True, limit="2")
        data = json.loads(buf.getvalue())
        assert data["project_count"] == 2

    def test_unknown_sort_field_exits_nonzero(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import RemyProject, save_project
        save_project(RemyProject(name="p1", slug="p1"))
        from apps.cli.commands.project import _cmd_list_projects
        with pytest.raises(SystemExit) as exc:
            _cmd_list_projects(json_output=True, sort="bogus")
        assert exc.value.code == 1


class TestJobListCLI:

Note: `StringIO`, `json`, and `pytest` are already imported at module scope in tests/test_grouped_cli.py — do not add duplicate imports.

Commit C2 covers both files (project.py's two pairs, and test_grouped_cli.py's one insertion) as ONE commit.

============================================================
PLAN17 — whole-file replace of `.agent/plan.md`. Byte length must be exactly 2530 (UTF-8), confirm with a binary-mode byte comparison after writing (read the file back and compare bytes, not text-mode, since Write-tool trailing-newline drift has bitten prior rounds — see the file's own git history for R14/R15's PLAN15/PLAN16 handbacks if you want the precedent).

PLAN17 text (copy exactly):
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 16, session 6 - T003 batch 4: `project.list` wired to
`apply_list_options` with `default_sort_field="created_at"` -
`_list_projects_readonly()` already sorted newest-first
(`test_list_sorted_newest_first`), so forcing the same default via the
shared helper changes nothing observable and needed no D2-style
opt-out. Dispatch is a lambda (`"project.list": lambda args: ...`), so
both the handler body AND the dispatch site needed a pair, unlike
tournament.list's single pair.

## Next Steps

- T003 batch 5+: wire the remaining plain-dict/model-row commands -
  blocker.list, decision.list, review.list, propose.list,
  external-builder.submission-list are shaped like
  project.list/tournament.list. patch.list (approval_queue.py's
  format_intent_list table renderer) and loop.list (JSON/text rows
  built from two different collections) still need their own look
  before wiring. config.list/worker.list/execution.list stay excused
  per Risks. Re-check EACH remaining command's OWN tests for an
  order-asserting test FIRST, per DECISION F262 D2's precedent, before
  assuming date-descending is safe to force.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
- Once every command is wired, add an integration-level smoke test
  proving the ten-second demo in Acceptance: a named run findable by
  one command with --since/--sort.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
- A command with its OWN meaningful non-date default order (queue.list's
  priority, DECISION F262 D2) opts out of the forced newest-first default
  via `default_sort_field=None` rather than losing that order - audit
  each remaining command for this shape before wiring it.

============================================================
CONSTRAINTS:
1. Do not touch any list command other than project.list this round. Do not touch `_list_projects_readonly`'s own sort in project_registry.py — it already sorts newest-first and stays untouched.
2. Do not widen or change `apply_list_options` itself (packages/orchestration/list_options.py) — it is unchanged this round.
3. No file besides these may be written: `apps/cli/commands/project.py`, `tests/test_grouped_cli.py`, `.agent/authored/f262-r16.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
4. Re-confirm each FROM string's exact occurrence count (must be 1) against the file's CURRENT on-disk content immediately before applying — not against the copy quoted in this prompt, in case anything has drifted.
5. Commit order is exactly C0a, C0b, C1, C2, C3, C4, each its own commit.
6. Run `git status --porcelain` after every commit; it must be empty before proceeding.
7. `.agent/STOP` must be absent before C0a and re-checked before C4. If it appears, stop immediately, finish only a half-written commit, and write the handoff reporting the STOP instead of continuing with new work.
8. Capture REAL exit codes for every command (wrap as `bash -c '<cmd>; echo REAL_EXIT=$?'` if needed) — do not report "green" as a bare word.
9. Known sandbox quirks in this repo (from prior rounds, so you don't waste turns rediscovering them): `python3 -m py_compile <files>` as a literal multi-arg command has been denied by the Bash sandbox before — if it is denied for you too, substitute `python3 -c "import py_compile; py_compile.compile('path/a.py', doraise=True); py_compile.compile('path/b.py', doraise=True); print('OK')"` and declare the substitution in your handback (this is an accepted, previously-used equivalent, not a shortcut). Also: `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`, and `cp` are all denied outright — use `monkeypatch.setenv` in tests (already the pattern in tests/test_grouped_cli.py) and `python3 -c "import shutil; shutil.copyfile(a,b)"` if you ever need to copy a file. Never use a sandbox-override flag to route around a denial — if something is denied, find the equivalent or declare it.

DONE WHEN (run every one of these EXACTLY as written and record the REAL, complete output of each in your handback — do not summarize as "passed", quote the actual pytest/py_compile output):
G1. `python3 -c "import py_compile; py_compile.compile('apps/cli/commands/project.py', doraise=True); py_compile.compile('tests/test_grouped_cli.py', doraise=True); print('OK')"` → must print OK.
G2. `python3 -m pytest tests/test_grouped_cli.py -q` → expect 525 passed (523 pre-existing + 2 new). Report the exact number.
G3. `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` → expect 646 passed (515+52+21+16+42), unmoved from the round-15 baseline. Report the exact number.
G4. `sha256sum .agent/authored/f262-r16.md .agent/last_block.md` → must print one identical digest for both files. Report both digests.
G5. Byte-read `.agent/live_review.md` immediately before C1 and immediately after C1 (Python, binary mode) → before must be 2460225, after must be 2462543. Report both numbers.
G6. Byte-read `.agent/plan.md` immediately after C3, binary mode → must be exactly 2530 bytes, and byte-for-byte equal to the PLAN17 text given above. Report the byte count and whether it matched exactly.
G7. `git status --porcelain` → empty, checked before C0a and immediately before C4. Report both checks.
G8. `git ls-files .remedy-wt` → empty (proves no scratch artifact was accidentally tracked). Report the output (should be nothing).

HANDBACK: write a full completion report and rewrite `.agent/handoff.md` per docs/agents/handback_template.md and the "### handoff.md" section of AGENTS.md — include the changed-files table (path, +/-, reason) for every commit, an item-status table (Item | Status | Reason) covering every bundle item (C0a..C4, and each gate G1..G8), the real verification results for every gate above (not summarized), the SESSION NUMBER (this is SESSION 6 of feature F262, round 16), and the next expected action (round 17: T003 batch 5 — wire blocker.list, decision.list, review.list, propose.list, external-builder.submission-list per PLAN17's Next Steps, re-checking each command's own tests for an order-asserting test first per DECISION F262 D2's precedent). After the handoff commit (C4), run `git push -u origin feature/f262-list-commands-v2` and report the push result. Do NOT create a PR. Do NOT merge anything. Do NOT touch `main`.
──────────────────────────────────────────────────────────────