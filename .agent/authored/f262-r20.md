── STEP T003 batch8 (final) — F262 List commands v2 ────────────────────────
Goal: Implement DECISION F262 D3 — restructure loop.list to wire apply_list_options with default_sort_field=None, closing out T003 — and book round 19's already-PASSED verdict into the ledger.

Bundle:
C0a. Save this entire step block, byte for byte, to a NEW file `.agent/authored/f262-r20.md`.
C0b. Whole-file replace `.agent/last_block.md` with the same bytes (mirror of C0a).
C1. Append GATE19 (below) to `.agent/live_review.md`.
C2. Production change: PAIR L1 (whole-body rewrite) + PAIR L2 (dispatch site) in `apps/cli/commands/loop_cmd.py`, plus TEST T1 appended to `tests/cli/test_loop_cmd.py`. ONE commit covering both files.
C3. Whole-file replace `.agent/plan.md` with PLAN21 (below).
C4. Rewrite `.agent/handoff.md` (handback) per docs/agents/handback_template.md; this is the round's LAST commit.

============================================================
GATE19 — append verbatim as a new line at the end of `.agent/live_review.md`. The current file ends with NO trailing newline. C1 must: read the current file, append exactly one `\n` character followed by the GATE19 text below (with no trailing newline after it either). Do this with Python (`pathlib.Path.write_bytes`), not a shell append.

GATE19 text (copy exactly, it is a single line with zero internal newlines, 3350 bytes UTF-8):
Gate: R19 — the F262 R19 entry. R19 SHIPPED T003 BATCH 7, `patch.list` wired to `apply_list_options` with `default_sort_field="created_at"` (ordinary dict-row shape, dispatch lambda needed both pairs, no order-asserting test), and recorded DECISION F262 D3 documenting why `loop.list` is deferred to round 20 — its config-declaration order is operator-authored and load-bearing (D2 precedent), and wiring it requires a real control-flow restructure (unify text/json into one row list before applying options) rather than the insert-before-render shape every other T003 batch used — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. A GENUINE ARITHMETIC TYPO IN THE REVIEWER'S OWN BLOCK WAS CAUGHT BY THE WORKER, NOT SILENTLY ROUTED AROUND: the GATE18 section's headline sentence stated the post-C1 live_review.md target as 2470337, contradicting both the same block's own correction note and gate G5, both of which correctly read 2470338 (2467532 + 1 + 2805); the worker halted before any commit, reported the exact contradiction, and the reviewer confirmed 2470338 as authoritative — the authored block was saved VERBATIM with the typo intact (the historical record of what was authored), while the actual C1 write and verification used 2470338 throughout, confirmed by the reviewer independently reading `.agent/authored/f262-r19.md` and finding the string "2470337" present exactly once (the uncorrected headline) and the file's own next line stating 2470338. TRANSPORT HELD: `.agent/authored/f262-r19.md`/`.agent/last_block.md` share one sha256 digest, `24ee4af552a9b61d4f752189d7f1ef28a700a313b59baeb40561ef0f650343ab`, confirmed by the reviewer's own sha256sum of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff f8ba752121e55af75231081f9a29490117ceea55..383e8808ef70633a65d16d07da2b7de072cc9818` for `apps/cli/commands/patch.py` and `tests/test_patch_intent_approval.py` shows exactly PAIR PA1, PAIR PA2, and TEST T1's two new methods, every other line in both files untouched, confirmed by reading the full diff. `python3 -c "import py_compile; ..."` printed OK for both touched files, run independently by the reviewer. THE GATE18 LEDGER APPEND (commit 55f6202c) AND DECISION F262 D3 APPEND (commit 0b43c4fd) WERE BOTH RE-VERIFIED BYTE-EXACT: live_review.md base 2467532 plus one newline plus GATE18 (2805 bytes) equals 2470338; decisions.md base 802422 plus one newline plus DECISION D3 (3645 bytes) equals 806068 — both exact, both matching the CORRECTED target rather than the block's typo'd headline. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `python3 -m pytest tests/test_patch_intent_approval.py -q` read 70 passed (68 pre-existing plus 2 new). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read 646 passed, matching 515+52+21+16+42 exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `383e8808`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 2180 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN20 slice against the written file. THE VERDICT IS PASS.

Base file size immediately before C1 must read 2470338 (confirm with a fresh Python byte read before writing). Post-C1 size must read exactly 2473689 (2470338 + 1 + 3350). Verify both numbers yourself and report them.
============================================================

PAIR L1 — apps/cli/commands/loop_cmd.py — REWRITE (whole function body). Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
def _cmd_loop_list(*, json_output: bool = False) -> None:
    """List every loop: name, trigger, action, last run. Reads, never writes."""
    from packages.orchestration.loop_spec import LoopSpecError, load_loop_specs

    try:
        specs = load_loop_specs()
    except LoopSpecError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if json_output:
        from packages.orchestration.loop_run import last_run_for_loop
        loops = []
        for spec in specs:
            job = last_run_for_loop(spec.name)
            last_run_created_at = None
            last_run_state = None
            if job is not None:
                last_run_created_at = getattr(
                    job.created_at, "isoformat", lambda: str(job.created_at)
                )()
                last_run_state = getattr(job.state, "value", job.state)
            loops.append({
                "name": spec.name,
                "trigger": spec.trigger.kind,
                "is_inert": spec.is_inert,
                "action": spec.action.kind,
                "last_run_created_at": last_run_created_at,
                "last_run_state": last_run_state,
            })
        print(json.dumps({"version": 1, "loops": loops}, sort_keys=True))
        return

    if not specs:
        print("No loops defined. Add a [[loop]] table to remedy.toml.")
        return

    for spec in specs:
        print(f"{spec.name:<24}  {_trigger_label(spec):<20}  "
              f"{spec.action.kind:<8}  last run: {_last_run_label(spec.name)}")

    if any(spec.is_inert for spec in specs):
        print(f"  ({INERT_MARK}: {INERT_TRIGGER_LEGEND})")

Replace it with this TO text:
def _cmd_loop_list(
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    """List every loop: name, trigger, action, last run. Reads, never writes."""
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.loop_run import last_run_for_loop
    from packages.orchestration.loop_spec import LoopSpecError, load_loop_specs

    try:
        specs = load_loop_specs()
    except LoopSpecError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    rows = []
    for spec in specs:
        job = last_run_for_loop(spec.name)
        last_run_created_at = None
        last_run_state = None
        if job is not None:
            last_run_created_at = getattr(
                job.created_at, "isoformat", lambda: str(job.created_at)
            )()
            last_run_state = getattr(job.state, "value", job.state)
        rows.append((spec, last_run_created_at, last_run_state))

    try:
        rows = apply_list_options(
            rows,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "last_run_created_at": lambda r: r[1] or "",
            },
            default_sort_field=None,
            date_getter=lambda r: r[1],
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if json_output:
        loops = [{
            "name": spec.name,
            "trigger": spec.trigger.kind,
            "is_inert": spec.is_inert,
            "action": spec.action.kind,
            "last_run_created_at": last_run_created_at,
            "last_run_state": last_run_state,
        } for spec, last_run_created_at, last_run_state in rows]
        print(json.dumps({"version": 1, "loops": loops}, sort_keys=True))
        return

    if not rows:
        print("No loops defined. Add a [[loop]] table to remedy.toml.")
        return

    for spec, last_run_created_at, last_run_state in rows:
        last_run_label = (
            NEVER_RAN if last_run_created_at is None
            else f"{last_run_created_at}  {last_run_state}"
        )
        print(f"{spec.name:<24}  {_trigger_label(spec):<20}  "
              f"{spec.action.kind:<8}  last run: {last_run_label}")

    if any(spec.is_inert for spec, _, _ in rows):
        print(f"  ({INERT_MARK}: {INERT_TRIGGER_LEGEND})")

Notes:
- `json`, `sys`, `EXIT_ERROR`, `NEVER_RAN`, `INERT_MARK`, `INERT_TRIGGER_LEGEND` are already available (imported/defined at module scope) in loop_cmd.py — do not add duplicate imports or redefine them.
- The pre-existing `_last_run_label` function (defined earlier in the file) becomes unused by this change and is intentionally left in place — do NOT delete it, that is out of this round's scope (DECISION F262 D3 only specifies the restructure of `_cmd_loop_list`, not removing now-dead helpers).
- `_trigger_label(spec)` is a pre-existing helper taking the spec object directly — it is still called the same way, on `spec` from the tuple.

PAIR L2 — apps/cli/commands/loop_cmd.py — REWRITE (dispatch site). Before applying, re-read the CURRENT file and confirm this FROM text occurs exactly 1 time:

FROM:
    "loop.list": lambda args: _cmd_loop_list(json_output=args.json),

Replace it with this TO text:
    "loop.list": lambda args: _cmd_loop_list(
        json_output=args.json,
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),

TEST T1 — tests/cli/test_loop_cmd.py — append two new test functions at the END of the file (the file currently ends with the function `test_loop_run_is_registered_and_in_the_catalog`, whose body is exactly `handlers = collect_all_handlers()` / `catalog_ids = {entry.command_id for entry in CATALOG}` / a blank line / `assert "loop.run" in handlers` / `assert "loop.run" in catalog_ids`, with no blank line after the last assert). Before applying, re-read the CURRENT file to confirm your insertion point is genuinely the end of the file.

Append this new content (two blank lines before it, matching the file's existing spacing between its top-level functions):

def test_limit_caps_returned_loops(project, capsys):
    _write_config(project, """
[[loop]]
name = "alpha-loop"

[loop.action]
kind = "job"
goal_template = "alpha {project} on {date}"

[[loop]]
name = "beta-loop"

[loop.action]
kind = "job"
goal_template = "beta {project} on {date}"
""")

    _dispatch_with("loop.list", json=True, limit="1")

    data = json.loads(capsys.readouterr().out)
    assert len(data["loops"]) == 1


def test_unknown_sort_field_exits_nonzero(project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)

    with pytest.raises(SystemExit) as exc:
        _dispatch_with("loop.list", json=True, sort="bogus")
    assert exc.value.code == 1

`_write_config`, `_dispatch_with`, `MANUAL_JOB_LOOP`, `json`, and `pytest` are all already defined/imported at module scope in this test file — do not add duplicate imports or redefine them.

Commit C2 covers both files (loop_cmd.py's two pairs, and the test file's append) as ONE commit.

============================================================
PLAN21 — whole-file replace of `.agent/plan.md`. Byte length must be exactly 2189 (UTF-8), confirm with a binary-mode byte comparison after writing.

PLAN21 text (copy exactly):
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 20, session 6 - T003 batch 8 (final): `loop.list` restructured
per DECISION F262 D3 - `_cmd_loop_list` now builds one
`(spec, last_run_created_at, last_run_state)` row list unconditionally
(moving the `last_run_for_loop` lookup out of the json-only branch),
runs `apply_list_options` once with `default_sort_field=None`
(config-declaration order stays default, D2/D3 precedent), and renders
BOTH text and json from that same row list - the text branch now reads
its row's own precomputed last-run fields instead of calling
`_last_run_label` a second time, removing the prior duplicate lookup.

## Next Steps

- T003 is now DONE for every list command in scope. Remaining before
  T003 closes out: an integration-level smoke test proving the
  ten-second demo in Acceptance (a named run findable by one command
  with --since/--sort), then move to closure per
  docs/roadmap/STATUS_closure_protocol.md.
- config.list/worker.list/execution.list stay excused per Risks -
  confirm this is still true at closure time, not just asserted.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order (queue.list's
  priority D2, loop.list's config order D3) opts out via
  `default_sort_field=None` rather than losing that order - this is
  now DONE for both of the two commands that needed it.

============================================================
CONSTRAINTS:
1. Do not touch any list command other than loop.list this round.
2. Do not widen or change `apply_list_options` itself (packages/orchestration/list_options.py) — it is unchanged this round.
3. No file besides these may be written: `apps/cli/commands/loop_cmd.py`, `tests/cli/test_loop_cmd.py`, `.agent/authored/f262-r20.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`.
4. Re-confirm each FROM string's exact occurrence count (must be 1) against the file's CURRENT on-disk content immediately before applying — not against the copy quoted in this prompt.
5. Do NOT delete the now-unused `_last_run_label` function — leaving it in place is the specified, intentional outcome of this round, not an oversight.
6. Commit order is exactly C0a, C0b, C1, C2, C3, C4, each its own commit.
7. Run `git status --porcelain` after every commit; it must be empty before proceeding.
8. `.agent/STOP` must be absent before C0a and re-checked before C4. If it appears, stop immediately, finish only a half-written commit, and write the handoff reporting the STOP instead of continuing.
9. Capture REAL exit codes for every command — do not report "green" as a bare word.
10. Known sandbox quirks in this repo (from prior rounds): `python3 -m py_compile <files>` as a literal multi-arg command has sometimes been denied by the Bash sandbox — if denied, substitute `python3 -c "import py_compile; py_compile.compile('path/a.py', doraise=True); ...; print('OK')"` and declare the substitution. `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`, and `cp` are denied outright — use `monkeypatch`/`python3 -c "import shutil; shutil.copyfile(a,b)"` if ever needed. Never use a sandbox-override flag to route around a denial.

DONE WHEN (run every one of these EXACTLY as written and record the REAL, complete output of each in your handback — quote actual pytest/py_compile output, do not summarize as "passed"):
G1. `python3 -c "import py_compile; py_compile.compile('apps/cli/commands/loop_cmd.py', doraise=True); py_compile.compile('tests/cli/test_loop_cmd.py', doraise=True); print('OK')"` → must print OK.
G2. `python3 -m pytest tests/cli/test_loop_cmd.py -q` → expect 18 passed (16 pre-existing + 2 new). Report the exact number. This ALSO re-proves every pre-existing loop.list test still passes after the restructure — in particular `test_after_one_real_firing_the_row_shows_that_row`, `test_json_output_carries_last_run_created_at_and_state`, and `test_json_output_last_run_is_null_when_never_ran`, which depend on the last-run lookup still working correctly after being moved out of the json-only branch.
G3. `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` → expect 646 passed (515+52+21+16+42), unmoved. Report the exact number.
G4. `sha256sum .agent/authored/f262-r20.md .agent/last_block.md` → must print one identical digest for both files. Report both digests.
G5. Byte-read `.agent/live_review.md` immediately before C1 and immediately after C1 (Python, binary mode) → before must be 2470338, after must be 2473689. Report both numbers.
G6. Byte-read `.agent/plan.md` immediately after C3, binary mode → must be exactly 2189 bytes, byte-for-byte equal to the PLAN21 text above. Report the byte count and whether it matched exactly.
G7. `git status --porcelain` → empty, checked before C0a and immediately before C4. Report both checks.
G8. `git ls-files .remedy-wt` → empty. Report the output (should be nothing).

HANDBACK: write a full completion report and rewrite `.agent/handoff.md` per docs/agents/handback_template.md and AGENTS.md's "### handoff.md" section — include the changed-files table (path, +/-, reason) for every commit, an item-status table (Item | Status | Reason) covering every bundle item (C0a..C4, and each gate G1..G8), the real verification results for every gate above, the SESSION NUMBER (this is SESSION 6 of feature F262, round 20), and the next expected action. State explicitly in the handback that this is the LAST round of session 6 (the session has now run 5 delegated rounds — R16 through R20 — meeting the self-drive protocol's default of four to five rounds per session), and that T003 is now complete for every list command in scope; the next session's first action should be Phase 0 fresh, likely moving toward an Acceptance-level integration smoke test and then F262 closure. After the handoff commit (C4), run `git push -u origin feature/f262-list-commands-v2` and report the push result. Do NOT create a PR. Do NOT merge anything. Do NOT touch `main`.
──────────────────────────────────────────────────────────────