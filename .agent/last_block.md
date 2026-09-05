── STEP R-0795 fix batch 1 (wiring) — F262 List commands v2 ────────────────
Goal: Wire config.list/worker.list/execution.list to apply_list_options (FIX option (a) of finding R-0795), add regression tests proving --limit and an unknown --sort field now work identically to every other list command, and book round 21's already-PASSED verdict into the ledger.

Bundle:
C0a. Save this entire step block, byte for byte, to a NEW file `.agent/authored/f262-r22.md`.
C0b. Whole-file replace `.agent/last_block.md` with the same bytes (mirror of C0a).
C1. Append GATE21 (below) to `.agent/live_review.md`.
C2. Production change: PAIR W1 (whole-function rewrite) + PAIR W2 (dispatch site) in `apps/cli/commands/worker.py`. ONE commit.
C3. Production change: PAIR CFG1 (whole-function rewrite) in `apps/cli/commands/config_cmd.py`. ONE commit.
C4. Production change: PAIR EXE1 (whole-function rewrite) in `apps/cli/commands/managed_builder_execution_cmd.py`. ONE commit.
C5. Test change: TEST T1 (append) in `tests/cli/test_config_cmd.py`, TEST T2 (rewrite, inserts before the module guard) in `tests/cli/test_managed_builder_execution_cli.py`, TEST T3 (append, new class) in `tests/cli/test_worker_facade_cmd.py`. ONE commit covering all three files.
C6. Append the LANDED line (below) to `.agent/live_review.md`.
C7. Whole-file replace `.agent/plan.md` with PLAN23 (below).
C8. Rewrite `.agent/handoff.md` (handback) per docs/agents/handback_template.md; this is the round's LAST commit.

============================================================
GATE21 — append verbatim as a new paragraph at the end of `.agent/live_review.md`. The current file ends with NO trailing newline, and its own last entry is FINDING R-0795 (not a Gate) — every non-Gate-to-Gate transition measured in this file uses a BLANK LINE separator (confirmed directly: GATE20-to-R-0795 used `\n\n`; every Landed-to-* and Done-to-* transition checked also used `\n\n`; only Gate-immediately-after-Gate has ever been observed using a single `\n`, and this append is Finding-to-Gate, not Gate-to-Gate). C1 must therefore: read the current file, append exactly TWO `\n` characters followed by the GATE21 text below (with no trailing newline after it either). Do this with Python (`pathlib.Path.write_bytes`), not a shell append.

GATE21 text (copy exactly, it is a single line with zero internal newlines, 2545 bytes UTF-8):
Gate: R21 — the F262 R21 entry. R21 was the OPERATOR-MANDATED SCOPE-REPORT ROUND triggered by amend0827-process-diet rule 6 (F262 reached 7 sessions, the stated soft limit): it booked round 20's already-PASSED verdict (GATE20, above) into the ledger, registered FINDING R-0795 (config.list/worker.list/execution.list PARSE all four T003 flags via the catalog's mechanical `_with_list_options` attachment but their handlers silently discard them, measured directly — `--sort bogus` against any of the three raises nothing, violating T2_F262.md's Acceptance bullet requiring a non-zero exit naming the valid fields), replaced `.agent/plan.md` with PLAN22 stating the two-option proposal (Option A: wire the three handlers plus build the T001 catalog test and the Acceptance smoke test; Option B: register a DECISION narrowing Acceptance to exempt the three by name), and wrote the mandated SCOPE REPORT handback — no `apps/`, `packages/`, `tests/` or `docs/` path was touched, which is the round's OWN stated obligation under rule 6 and not a rule-1 pure-bookkeeping violation, since rule 6 is a second sanctioned exception alongside a feature's closure sequence — AND THE REVIEWER RE-RAN EVERY GATE ITSELF, in a fresh session (session 8), independently. TRANSPORT HELD: `sha256sum .agent/authored/f262-r21.md .agent/last_block.md` printed one identical digest, `62077e148db6644c38030ef6fe3c94f225f8020448fa53d1e75d927871ba984f`, for both files, reproduced exactly. THE LEDGER APPENDS HELD, reproduced by direct byte reads of the tracked file: base 2473689 (before C2) plus one newline plus GATE20 (2778 bytes) equals 2476468 (after C2); 2476468 plus two newlines plus FINDING R-0795 (3228 bytes) equals 2479698 (after C3) — both exact, matching the round's own stated arithmetic and the file's current on-disk size (2479698 bytes, confirmed by a fresh byte read). THE PLAN HELD: `.agent/plan.md` measured 2350 bytes at HEAD `c129b4f2`, byte-for-byte equal to PLAN22, 49 lines, under the 50-line cap. THE NUMSTAT CROSS-CHECK HELD: `git show --numstat --format="" 655f71ae` read `104 0 .agent/authored/f262-r21.md`; `2909d2b4` read `68 240 .agent/last_block.md`; `76c8c6b9` read `28 26 .agent/plan.md`; `8d141dd4` read `2 1 .agent/live_review.md`; `d4760aa2` read `3 1 .agent/live_review.md` — every path and every insertion/deletion count matches the round's own handback Commits table exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `c129b4f2`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE VERDICT IS PASS.

Base file size immediately before C1 must read 2479698 (confirm with a fresh Python byte read before writing). Post-C1 size must read exactly 2482245 (2479698 + 2 + 2545). Verify both numbers yourself and report them.
============================================================

PAIR W1 — apps/cli/commands/worker.py — REWRITE (whole function). Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
def _cmd_workers(*, json_output: bool = False) -> None:
    from packages.orchestration.worker_adapters import (
        export_worker_specs_json,
        list_worker_specs,
        summarize_worker_specs,
    )

    specs = list_worker_specs()
    if json_output:
        print(_json.dumps(export_worker_specs_json(specs), sort_keys=True))
    else:
        print(summarize_worker_specs(specs))

Replace it with this TO text:
def _cmd_workers(
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.worker_adapters import (
        export_worker_specs_json,
        list_worker_specs,
        summarize_worker_specs,
    )

    specs = list_worker_specs()
    try:
        specs = apply_list_options(
            specs,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "provider_id": lambda s: s.provider_id,
                "display_name": lambda s: s.display_name,
                "status": lambda s: s.status,
            },
            default_sort_field=None,
            date_getter=None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps(export_worker_specs_json(specs), sort_keys=True))
    else:
        print(summarize_worker_specs(specs))

Notes: `sys` is already imported at module scope (line 5) — no duplicate import; `apply_list_options` returns a `list`, and `export_worker_specs_json`/`summarize_worker_specs` iterate whatever is passed, no cast needed.

PAIR W2 — apps/cli/commands/worker.py — REWRITE (dispatch site). Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
    "worker.list": lambda args: _cmd_workers(json_output=args.json),

Replace it with this TO text:
    "worker.list": lambda args: _cmd_workers(
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),

Commit C2 covers both pairs in `apps/cli/commands/worker.py` as ONE commit.

============================================================
PAIR CFG1 — apps/cli/commands/config_cmd.py — REWRITE (whole function). Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
def _cmd_config_list(args: argparse.Namespace) -> None:
    from packages.orchestration.config import all_key_specs, get_config

    config = get_config()
    use_json = getattr(args, "json", False)

    if use_json:
        entries = []
        for spec in all_key_specs():
            cv = config.get_value(spec.key)
            val = cv.value if cv else None
            if spec.secret or spec.env_only:
                val = "[REDACTED]" if val is not None else None
            entries.append({
                "key": spec.key,
                "value": val,
                "source": cv.source.value if cv else "unknown",
                "env_var": spec.env_var,
                "type": spec.value_type.__name__,
                "is_default": cv.is_default if cv else True,
            })
        json.dump(entries, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    for spec in all_key_specs():
        cv = config.get_value(spec.key)
        val = cv.value if cv else None
        source = cv.source.value if cv else "default"
        if spec.secret or spec.env_only:
            val = "[REDACTED]" if val is not None else None
        val_str = str(val) if val is not None else "(not set)"
        print(f"  {spec.key:40s} = {val_str:30s} [{source}]")

Replace it with this TO text:
def _cmd_config_list(args: argparse.Namespace) -> None:
    from packages.orchestration.config import all_key_specs, get_config
    from packages.orchestration.list_options import ListOptionError, apply_list_options

    config = get_config()
    use_json = getattr(args, "json", False)

    try:
        specs = apply_list_options(
            list(all_key_specs()),
            sort=getattr(args, "sort", None),
            desc=getattr(args, "desc", False),
            since=getattr(args, "since", None),
            until=getattr(args, "until", None),
            limit=getattr(args, "limit", None),
            sort_fields={"key": lambda s: s.key},
            default_sort_field=None,
            date_getter=None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if use_json:
        entries = []
        for spec in specs:
            cv = config.get_value(spec.key)
            val = cv.value if cv else None
            if spec.secret or spec.env_only:
                val = "[REDACTED]" if val is not None else None
            entries.append({
                "key": spec.key,
                "value": val,
                "source": cv.source.value if cv else "unknown",
                "env_var": spec.env_var,
                "type": spec.value_type.__name__,
                "is_default": cv.is_default if cv else True,
            })
        json.dump(entries, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    for spec in specs:
        cv = config.get_value(spec.key)
        val = cv.value if cv else None
        source = cv.source.value if cv else "default"
        if spec.secret or spec.env_only:
            val = "[REDACTED]" if val is not None else None
        val_str = str(val) if val is not None else "(not set)"
        print(f"  {spec.key:40s} = {val_str:30s} [{source}]")

Notes: `sys` already imported at module scope (line 6) — no duplicate import. This function ALSO serves `config.show` (`"config.show": _cmd_config_list`); its Namespace has no sort/desc/since/until/limit attributes, which is exactly why every read uses `getattr(args, ..., default)`. Commit C3 covers this pair.

============================================================
PAIR EXE1 — apps/cli/commands/managed_builder_execution_cmd.py — REWRITE (whole function). Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
def _cmd_list(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import list_execution_results
    job_id = getattr(ns, "job_id", "") or ""
    results = list_execution_results(job_id)
    print(json.dumps(results, indent=2))

Replace it with this TO text:
def _cmd_list(ns: argparse.Namespace) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.managed_builder_execution import list_execution_results
    job_id = getattr(ns, "job_id", "") or ""
    results = list_execution_results(job_id)
    try:
        results = apply_list_options(
            results,
            sort=getattr(ns, "sort", None),
            desc=getattr(ns, "desc", False),
            since=getattr(ns, "since", None),
            until=getattr(ns, "until", None),
            limit=getattr(ns, "limit", None),
            sort_fields={
                "started_at": lambda r: r.get("started_at") or "",
                "ended_at": lambda r: r.get("ended_at") or "",
                "status": lambda r: r.get("status") or "",
                "duration_ms": lambda r: r.get("duration_ms") or 0,
            },
            default_sort_field="started_at",
            date_getter=lambda r: r.get("started_at") or None,
        )
    except ListOptionError as exc:
        _err(str(exc))
    print(json.dumps(results, indent=2))

Notes: `_err` is already defined above in this file (prints `json.dumps({"error": msg})` to stderr and calls `sys.exit(1)`) — reuse it, matching the file's own error convention. Commit C4 covers this pair.

============================================================
TEST T1 — tests/cli/test_config_cmd.py — APPEND at the very end of the file (currently ends with `test_config_set_json`'s last line, exactly `        assert data["value"] == "http://custom:11434"`, no trailing blank line). Re-read the CURRENT file first to confirm your insertion point is genuinely the end.

Append this new content (one blank line before it, matching the file's existing spacing between methods):

    def test_config_list_limit(self):
        r = subprocess.run(
            [*_CLI, "config", "list", "--json", "--limit", "1"],
            capture_output=True, text=True, timeout=30,
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert len(data) == 1

    def test_config_list_unknown_sort_field_exits_nonzero(self):
        r = subprocess.run(
            [*_CLI, "config", "list", "--json", "--sort", "bogus"],
            capture_output=True, text=True, timeout=30,
        )
        assert r.returncode != 0
        assert "unknown --sort field" in r.stderr

`_CLI`, `subprocess`, `json` are all already defined/imported at module scope — no duplicate imports.

============================================================
TEST T2 — tests/cli/test_managed_builder_execution_cli.py — REWRITE (inserts two new methods before the module guard; TO does not contain FROM verbatim, so use the standard REWRITE proof, not an append proof). Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
    def test_approval_list(self):
        r = _run(["execution", "approval-list", "--json"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert isinstance(data, list)


if __name__ == "__main__":
    unittest.main()

Replace it with this TO text:
    def test_approval_list(self):
        r = _run(["execution", "approval-list", "--json"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert isinstance(data, list)

    def test_execution_list_limit(self):
        r = _run(["execution", "list", "--json", "--limit", "1"])
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert isinstance(data, list)
        assert len(data) <= 1

    def test_execution_list_unknown_sort_field_exits_nonzero(self):
        r = _run(["execution", "list", "--json", "--sort", "bogus"])
        assert r.returncode != 0
        assert "unknown --sort field" in r.stderr


if __name__ == "__main__":
    unittest.main()

============================================================
TEST T3 — tests/cli/test_worker_facade_cmd.py — APPEND at the very end of the file (currently ends with `test_grant_no_session`'s body, last line exactly `            ))`, no trailing blank line). Re-read the CURRENT file first to confirm your insertion point is genuinely the end.

Append this new content (two blank lines before it, matching the file's existing spacing between top-level classes):

class TestWorkerListOptions:
    def test_limit_caps_returned_workers(self, capsys):
        from apps.cli.commands import collect_all_handlers
        collect_all_handlers()["worker.list"](_ns(json=True, limit="1"))
        data = json.loads(capsys.readouterr().out)
        assert len(data["providers"]) == 1

    def test_unknown_sort_field_exits_nonzero(self):
        from apps.cli.commands import collect_all_handlers
        with pytest.raises(SystemExit) as exc:
            collect_all_handlers()["worker.list"](_ns(json=True, sort="bogus"))
        assert exc.value.code == 1

`_ns`, `json`, `pytest` are all already defined/imported at module scope (`_ns` at line 124) — no duplicate imports.

Commit C5 covers TEST T1, TEST T2 and TEST T3 across all three files as ONE commit.

============================================================
LANDED line — append verbatim as a new paragraph at the end of `.agent/live_review.md` (after GATE21, which C1 already appended). Every Landed-to-* transition measured in this file uses a blank-line separator, so C6 must: read the current file (now ending with GATE21, no trailing newline), append exactly TWO `\n` characters followed by the text below (no trailing newline after it either). Python `pathlib.Path.write_bytes`, not a shell append.

LANDED text (copy exactly, it is a single line with zero internal newlines, 293 bytes UTF-8):
Landed: R-0795 — `worker.list` (commit C2), `config.list` (commit C3) and `execution.list` (commit C4) of F262 R22 are now wired to `apply_list_options`, with six new regression tests (commit C5) proving `--limit` and an unknown `--sort` field behave identically to every other list command.

Base file size immediately before C6 must read 2482245 (the post-C1 size from GATE21's own arithmetic — C2 through C5 touch no other path in `.agent/live_review.md`). Post-C6 size must read exactly 2482540 (2482245 + 2 + 293). Verify both numbers yourself and report them. Do NOT write `Done: R-0795` — only the reviewer writes `Done:`, at the next gate, per docs/agents/planner_reviewer_prompt.md §4 item 4.

============================================================
PLAN23 — whole-file replace of `.agent/plan.md`. Byte length must be exactly 1959 (UTF-8), confirm with a binary-mode byte comparison after writing.

PLAN23 text (copy exactly):
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 22, session 8 - R-0795 core fix: `config.list`, `worker.list`
and `execution.list` wired to `apply_list_options`. `worker.list`/
`config.list` use `default_sort_field=None` (no date field, like
queue.list/loop.list's D2/D3); `execution.list` uses
`default_sort_field="started_at"` (a real ISO date per row). Six
regression tests added (two per command). R-0795 is LANDED, not yet
Done - the reviewer converts it at the next gate (§4 item 4).

## Next Steps

- Round 23: extend `TestListCommandOptions`
  (tests/test_command_catalog.py) to dispatch every `_is_list_command`
  entry's HANDLER (not just its argparse signature) with an invalid
  `--sort` and assert a non-zero exit - T001's own never-built
  Acceptance bullet.
- Round 24: the Acceptance ten-second-demo smoke test, then closure
  per docs/roadmap/STATUS_closure_protocol.md.
- change.list's event-log CREATED date stays open, UNRELATED to D1 -
  see DECISION F262 D1's Alternative section.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order opts out
  via `default_sort_field=None` (queue.list D2, loop.list D3,
  worker.list/config.list now too).
- R-0795: LANDED this round for the three named commands - the
  catalog-wide enumeration proof (T001's own gap) stays open, round 23.

============================================================
CONSTRAINTS:
1. Do not touch any list command other than config.list, worker.list, execution.list this round.
2. Do not widen or change `apply_list_options` itself (packages/orchestration/list_options.py) — it is unchanged this round.
3. No file besides these may be written: `apps/cli/commands/worker.py`, `apps/cli/commands/config_cmd.py`, `apps/cli/commands/managed_builder_execution_cmd.py`, `tests/cli/test_config_cmd.py`, `tests/cli/test_managed_builder_execution_cli.py`, `tests/cli/test_worker_facade_cmd.py`, `.agent/authored/f262-r22.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
4. Re-confirm each FROM string's exact occurrence count (must be 1) against the file's CURRENT on-disk content immediately before applying — not against the copy quoted in this prompt.
5. Commit order is exactly C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8, each its own commit.
6. Run `git status --porcelain` after every commit; it must be empty before proceeding. Capture REAL exit codes for every command — do not report "green" as a bare word.
7. `.agent/STOP` must be absent before C0a and re-checked before C8. If it appears, stop immediately, finish only a half-written commit, and write the handoff reporting the STOP instead of continuing.
8. Known sandbox quirks in this repo: `python3 -m py_compile <files>` as a literal multi-arg command has sometimes been denied — if denied, substitute a `python3 -c` one-liner using `py_compile.compile(..., doraise=True)` and declare the substitution. `VAR=x cmd`, `export VAR=x; cmd`, and `cp` are denied outright — use a `python3 -c "import shutil; shutil.copyfile(a,b)"` one-liner if ever needed. The `remedy` CLI itself is denied session-wide — use `python3 -m apps.cli.grouped` or `python3 -m pytest` instead. Never use a sandbox-override flag to route around a denial.
9. No mutation red-proof is ordered this round (deferred to round 23, bundled with the catalog test's own red-proof, per PLAN23's Next Steps) — the new tests (G3) are this round's only behavioural proof; do not claim a mutation red-proof ran.

DONE WHEN (run every one of these EXACTLY as written and record the REAL, complete output of each in your handback — quote actual pytest/py_compile output, do not summarize as "passed"):
G1. `sha256sum .agent/authored/f262-r22.md .agent/last_block.md` → must print one identical digest for both files. Report both digests.
G2. `python3 -c "import py_compile; [py_compile.compile(p, doraise=True) for p in ['apps/cli/commands/worker.py','apps/cli/commands/config_cmd.py','apps/cli/commands/managed_builder_execution_cmd.py','tests/cli/test_config_cmd.py','tests/cli/test_managed_builder_execution_cli.py','tests/cli/test_worker_facade_cmd.py']]; print('OK')"` → must print OK.
G3. `python3 -m pytest tests/cli/test_worker_facade_cmd.py tests/cli/test_config_cmd.py tests/cli/test_managed_builder_execution_cli.py -q` → expect 98 passed (92 pre-existing + 6 new). Report the exact number.
G4. `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` → expect 646 passed (515+52+21+16+42), unmoved. Report the exact number.
G5. Byte-read `.agent/live_review.md` immediately before C1 and immediately after C1 (before must be 2479698, after must be 2482245); immediately before C6 and immediately after C6 (before must be 2482245, after must be 2482540). Python, binary mode. Report all four numbers.
G6. Byte-read `.agent/plan.md` immediately after C7, binary mode → must be exactly 1959 bytes, byte-for-byte equal to the PLAN23 text above. Report the byte count and whether it matched exactly.
G7. `git status --porcelain` → empty, checked before C0a and immediately before C8. `git ls-files .remedy-wt` → empty. Report all three checks.

HANDBACK: write a full completion report and rewrite `.agent/handoff.md` per docs/agents/handback_template.md and AGENTS.md's "### handoff.md" section — include the changed-files table (path, +/-, reason) for every commit, an item-status table (Item | Status | Reason) covering every bundle item (C0a..C8, and each gate G1..G7), the real verification results for every gate above, the SESSION NUMBER (this is SESSION 8 of feature F262, round 22), and the next expected action (round 23: extend `TestListCommandOptions` into a catalog-driven handler test per PLAN23's Next Steps, AND run the full mutation red-proof deferred from this round, covering all three of this round's wirings). State explicitly that no mutation red-proof was ordered this round and why (deferred, not skipped — constraint 9). Confirm the `Landed: R-0795` line from C6 landed byte-for-byte (G5's second pair). State this round is at 22 of the 25-round soft cap, 3 rounds of headroom left before the cap. After the handoff commit (C8), run `git push -u origin feature/f262-list-commands-v2` and report the push result. Do NOT create a PR. Do NOT merge anything. Do NOT touch `main`.
──────────────────────────────────────────────────────────────