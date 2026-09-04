═══════════════════════════════════════════════════════════════
STEP — F262 R10/? — loop.list gains --json end to end
═══════════════════════════════════════════════════════════════

GOAL: Give `loop.list` a `--json` output (matching the pattern already shipped for job.list/queue.list/patch.list in earlier rounds), carrying each loop's last-run created_at/state as structured JSON fields sourced from the exact same `last_run_for_loop()` call the existing text "last run:" label already uses — no new timestamp invented. Book round 9's reviewer verdict into the ledger, plus one prose_slips.md line for a byte-fidelity gap the reviewer found in round 9's own C4.

BACKGROUND FACTS (already verified by the reviewer — do not re-derive):
- `loop.list` already gets T001's `--sort/--since/--until/--limit` flags automatically via `_with_list_options()` in `apps/cli/command_catalog.py` (it matches on `subcommand == "list"`), so those are NOT a gap. The only real gap is `--json` support and JSON-shaped date fields.
- `_last_run_label()` in `apps/cli/commands/loop_cmd.py` already computes a real timestamp per loop (`last_run_for_loop(name)` → a `Job` → `.created_at`/`.state`) for the TEXT output. The JSON path reuses that same function, just returns the fields structurally instead of as one formatted string.
- `tests/cli/test_loop_cmd.py` has an explicit, deliberate testing convention stated in its own module docstring: every test dispatches through `collect_all_handlers()`, NEVER by importing `_cmd_loop_list` directly — this proves the command is reachable through the registered table, not just importable. The file already has a `_dispatch_with(command_id, **attributes)` helper for exactly this (builds an `argparse.Namespace(**attributes)` and dispatches through the real handler table). Your new tests MUST use `_dispatch_with("loop.list", json=True)`, never call `_cmd_loop_list` directly — this is a hard convention of this specific file, stated in its own header.

═══ COMMIT SEQUENCE (5 commits total) ═══

──────────────────────────────────────────────────────────
C0a — save this entire step block verbatim
──────────────────────────────────────────────────────────
Save the FULL literal text of this prompt message (everything between the "STEP —" header above and the final "END OF BLOCK" marker at the bottom) to `.agent/authored/f262-r10.md`, byte for byte, exactly as received. Commit message: `F262 R10 C0a: save block verbatim to .agent/authored/f262-r10.md`

──────────────────────────────────────────────────────────
C0b — mirror to .agent/last_block.md
──────────────────────────────────────────────────────────
Copy `.agent/authored/f262-r10.md` to `.agent/last_block.md`, whole-file replace. Verify `sha256sum` of both files matches after writing. Commit message: `F262 R10 C0b: mirror block to .agent/last_block.md`

──────────────────────────────────────────────────────────
C1 — append GATE9 to .agent/live_review.md AND one line to .agent/prose_slips.md
──────────────────────────────────────────────────────────
Append exactly the text between the GATE9 markers below to the END of `.agent/live_review.md`: one newline, then the GATE9 text verbatim (it is a SINGLE LINE — no internal newlines), nothing else added.

<<<BEGIN GATE9>>>
Gate: R9 — the F262 R9 entry. R9 SHIPPED T002 BATCH 7, patch.list gains a CREATED date end to end: created_at stamped once at intent-derivation time in both creation flows (do_run.py's fixture dict, apps/cli/commands/job.py's dict-comprehension via a new pi_created_at + datetime/timezone import), surfaced through list_patch_intents() and a new CREATED column in format_intent_list() ahead of DECIDED — patch.list --json needed no separate change since it prints list_patch_intents()'s own dicts verbatim. DECISION F262 D1 records why the value is sourced from the stored explanation dict rather than the run-event log, correcting a stale R8 plan.md claim (job.py:623 DOES emit patch_intent_created; only do_run.py's own do_run_patch_intent_created is dead; neither is what list_patch_intents() actually reads) — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r9.md`/`.agent/last_block.md` share one sha256 digest, confirmed by the reviewer's own read of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff 74cfbd28..9adfbc53` for the six production/test files shows exactly the six pairs and four test appends the handback claimed, every diff re-read in full, nothing else touched — job.py gains the datetime import and pi_created_at + created_at key exactly as ordered, do_run.py gains one created_at key, approval_queue.py gains created_at in the returned dict, its docstring and format_intent_list()'s new CREATED column ahead of DECIDED. `python3 -m py_compile` exited 0 on all six touched files, run together by the reviewer. THE GATE8 LEDGER APPEND (commit 7d6df1bd) WAS RE-VERIFIED BYTE-EXACT: base plus one newline plus GATE8 (2457 bytes, 0 internal newlines) reproduces the post-commit file exactly; tail-equality, preceding-newline and negative-control byte-flip rejection all confirmed. THE DECISION F262 D1 APPEND (commit 59bf9fe9) WAS RE-VERIFIED BYTE-EXACT the same way. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `tests/orchestration/test_do_run.py tests/test_patch_intent_approval.py tests/test_run_log_cli.py tests/test_command_catalog.py` read 223 passed. THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer: `tests/ui_server/` 515, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42. HYGIENE HELD: `git status --porcelain` empty at HEAD `9adfbc53`, `git ls-files .remedy-wt` empty. ONE GAP FOUND AND ROUTED, NOT A BLOCK CONDITION: the round's own C4 gate for PLAN10 ran `wc -l` plus `git diff --stat`, not the byte-equality check the gate-budget rule mandates for a `.agent/` prose whole-file replace — the applied `.agent/plan.md` (1928 bytes) carries one trailing newline byte the authored PLAN10 slice (1927 bytes) does not, added by the file-write tool used to apply it; content, line count and both required headings are unaffected, so this is routed to `.agent/prose_slips.md` rather than an R-id, per amend0827 rule 2 (no product-effect defect — `.agent/` is not `packages/`/`apps/`/`tests/`/`docs/`). THE VERDICT IS PASS.
<<<END GATE9>>>

Then append exactly the text between the PROSE_SLIP markers below to the END of `.agent/prose_slips.md`: one newline, then the text verbatim (single line, no internal newlines), nothing else added.

<<<BEGIN PROSE_SLIP>>>
2026-09-04 · F262 R9 (reviewer) · The round 9 C4 commit (PLAN10 replacing `.agent/plan.md`) was applied via a file-write tool that appended a trailing newline the authored PLAN10 slice did not have (1928 bytes on disk vs 1927 authored) — a byte gap the round's own gate did not catch, since it ran `wc -l` plus `git diff --stat` rather than the byte-equality comparison against the authored marker content that the gate-budget rule mandates for a `.agent/` prose file. THE LESSON: a whole-file `.agent/` replacement's gate is the byte-equality check itself, not a proxy for it (line count, diffstat) — proxies pass wherever the real check would too, until a tool's own defaults introduce exactly the byte the proxy cannot see. Worker-applied gap, caught only by the reviewer's independent re-verification; nothing on disk asserts otherwise, no R-id spent (amend0827-process-diet rule 2).
<<<END PROSE_SLIP>>>

Commit message: `F262 R10 C1: append GATE9 to live_review.md and one line to prose_slips.md - books round 9's PASS verdict`

──────────────────────────────────────────────────────────
C2 — production pairs + tests (one commit, three production files, one test file)
──────────────────────────────────────────────────────────

PAIR P1 (REWRITE) — `apps/cli/commands/loop_cmd.py`, add the `json` import.
FROM (exact, currently near the top of the file):
<<<BEGIN PAIR_P1_FROM>>>
import sys
from collections.abc import Callable
<<<END PAIR_P1_FROM>>>
TO:
<<<BEGIN PAIR_P1_TO>>>
import json
import sys
from collections.abc import Callable
<<<END PAIR_P1_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P2 (REWRITE) — `apps/cli/commands/loop_cmd.py`, `_cmd_loop_list` gains a `json_output` kwarg and a JSON branch. This is the WHOLE current function body — re-read the file yourself first and confirm this FROM matches exactly before applying; if it does not match, STOP and report the mismatch rather than guessing.
FROM (exact):
<<<BEGIN PAIR_P2_FROM>>>
def _cmd_loop_list() -> None:
    """List every loop: name, trigger, action, last run. Reads, never writes."""
    from packages.orchestration.loop_spec import LoopSpecError, load_loop_specs

    try:
        specs = load_loop_specs()
    except LoopSpecError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    if not specs:
        print("No loops defined. Add a [[loop]] table to remedy.toml.")
        return

    for spec in specs:
        print(f"{spec.name:<24}  {_trigger_label(spec):<20}  "
              f"{spec.action.kind:<8}  last run: {_last_run_label(spec.name)}")

    if any(spec.is_inert for spec in specs):
        print(f"  ({INERT_MARK}: {INERT_TRIGGER_LEGEND})")
<<<END PAIR_P2_FROM>>>
TO:
<<<BEGIN PAIR_P2_TO>>>
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
<<<END PAIR_P2_TO>>>
Verify FROM occurs exactly once in the file before applying. Note: the tail of TO (from `if not specs:` onward) is byte-identical to the tail of FROM — the only change is the new `json_output` parameter and the new `if json_output:` block inserted before it. The existing TEXT output path is completely unchanged.

PAIR P3 (REWRITE) — `apps/cli/command_catalog.py`, the `loop.list` CommandEntry gains `_JSON_OPT` and `supports_json=True` (same shape every prior list-command JSON addition in this feature used).
FROM (exact):
<<<BEGIN PAIR_P3_FROM>>>
    CommandEntry(
        command_id="loop.list",
        group_id="loop",
        subcommand="list",
        description="List the loops in remedy.toml: name, trigger, action and last run.",
        action_class="read_only",
        related=("loop.validate", "loop.run"),
    ),
<<<END PAIR_P3_FROM>>>
TO:
<<<BEGIN PAIR_P3_TO>>>
    CommandEntry(
        command_id="loop.list",
        group_id="loop",
        subcommand="list",
        description="List the loops in remedy.toml: name, trigger, action and last run.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("loop.validate", "loop.run"),
    ),
<<<END PAIR_P3_TO>>>
Verify FROM occurs exactly once in the file before applying. `_JSON_OPT` is already defined earlier in this same file (used by job.list/queue.list/patch.list already) — do not redefine it.

PAIR P4 (REWRITE) — `apps/cli/commands/loop_cmd.py`, the dispatch lambda.
FROM (exact):
<<<BEGIN PAIR_P4_FROM>>>
    "loop.list": lambda args: _cmd_loop_list(),
<<<END PAIR_P4_FROM>>>
TO:
<<<BEGIN PAIR_P4_TO>>>
    "loop.list": lambda args: _cmd_loop_list(json_output=args.json),
<<<END PAIR_P4_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P5 (REWRITE) — `tests/cli/test_loop_cmd.py`, add the `json` import.
FROM (exact, currently near the top of the file):
<<<BEGIN PAIR_P5_FROM>>>
import argparse
from pathlib import Path

import pytest
<<<END PAIR_P5_FROM>>>
TO:
<<<BEGIN PAIR_P5_TO>>>
import argparse
import json
from pathlib import Path

import pytest
<<<END PAIR_P5_TO>>>
Verify FROM occurs exactly once in the file before applying.

TEST T1 (APPEND) — `tests/cli/test_loop_cmd.py`. Insert this new test method immediately after `test_after_one_real_firing_the_row_shows_that_run` (which ends `assert stored.state.value in row`) and before `test_validate_reports_every_error_and_exits_non_zero`. MUST dispatch via `_dispatch_with`, never call `_cmd_loop_list` directly (see this file's own module docstring — a hard convention):
<<<BEGIN T1>>>

def test_json_output_carries_last_run_created_at_and_state(project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)
    (spec,) = load_loop_specs()
    outcome = run_loop(spec, project_id="remedy", date="2026-08-13", root=project)
    stored = storage.load_job(outcome.job.id, project)

    _dispatch_with("loop.list", json=True)

    data = json.loads(capsys.readouterr().out)
    row = next(item for item in data["loops"] if item["name"] == "nightly-tidy")
    assert row["last_run_created_at"] == stored.created_at.isoformat()
    assert row["last_run_state"] == stored.state.value

<<<END T1>>>

TEST T2 (APPEND) — `tests/cli/test_loop_cmd.py`. Insert immediately after T1 (above), still before `test_validate_reports_every_error_and_exits_non_zero`:
<<<BEGIN T2>>>

def test_json_output_last_run_is_null_when_never_ran(project, capsys):
    _write_config(project, MANUAL_JOB_LOOP)

    _dispatch_with("loop.list", json=True)

    data = json.loads(capsys.readouterr().out)
    row = next(item for item in data["loops"] if item["name"] == "nightly-tidy")
    assert row["last_run_created_at"] is None
    assert row["last_run_state"] is None

<<<END T2>>>

Apply P1-P5 and T1-T2. Note: `tests/cli/test_loop_cmd.py` defines its test functions at MODULE level (not inside a class) — confirm this yourself by reading the file before inserting; insert T1 and T2 as plain module-level functions with no indentation, matching the surrounding functions exactly.

Run `python3 -m py_compile apps/cli/commands/loop_cmd.py apps/cli/command_catalog.py tests/cli/test_loop_cmd.py` and confirm exit 0. Then run `python3 -m pytest tests/cli/test_loop_cmd.py tests/test_command_catalog.py -q` and record the exact pass count verbatim. All 4 files (3 production, 1 test) in ONE commit. Commit message: `F262 R10 C2: loop.list gains --json end to end (T002 batch 8)`

──────────────────────────────────────────────────────────
C3 — replace .agent/plan.md with PLAN11
──────────────────────────────────────────────────────────
Replace the ENTIRE content of `.agent/plan.md` with exactly the text between the PLAN11 markers below (whole-file replace, byte-exact — this time verify with an actual byte-for-byte comparison, e.g. `python3 -c` reading both the authored slice and the written file in binary mode and comparing, NOT just `wc -l`/diffstat, per the lesson just booked in C1):

<<<BEGIN PLAN11>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 10, session 4 - loop.list gains --json end to end (catalog
_JSON_OPT + supports_json=True, handler json_output kwarg + json
branch, dispatch lambda), carrying last_run_created_at/last_run_state
per loop sourced from the SAME last_run_for_loop() call the existing
text "last run:" label already uses - no new timestamp invented.
T001's --sort/--since/--until/--limit flags were already present on
loop.list via _with_list_options' auto-injection (subcommand=="list"
matches); only --json and its JSON date fields were the real gap.

## Next Steps

- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
- The execution.* trio always prints JSON unconditionally with no
  text branch - the pre-existing --json-ignored quirk Risks excuses.
- T003 (sort/filter/limit) starts once date coverage is far enough
  along to sort by - patch.list and loop.list both now have dates;
  audit whether any remaining list command still lacks one before
  starting T003, or start T003 against the commands that already
  qualify.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
<<<END PLAN11>>>

Commit message: `F262 R10 C3: replace plan.md with PLAN11`

──────────────────────────────────────────────────────────
C4 — handback
──────────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` (whole-file, per AGENTS.md's handback contract) with: Session (SESSION 4 of feature F262, round 10, rounds so far 10), a Range section stating this handback covers `9adfbc53..<C3 sha>` (C4/this handback commit is NOT part of the reviewed content range), an Item Status table (Preconditions, C0a, C0b, C1, C2, C3, C4, plus one row per gate you ran), a Commits table with every file changed per commit and its +/- line counts from `git show --numstat`, a Verification section with the REAL output of every command you ran (py_compile exit codes, the exact pytest pass count for C2's combined run, the canary suite counts run individually: `tests/ui_server/`, `tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py`, `tests/orchestration/test_integrity_gate.py`, `tests/cli/test_golden_path.py`), a Deviations & assumptions section (state honestly anything that didn't go exactly as ordered — including explicitly stating the plan.md byte-equality check result this time, per the C1 lesson), and a Next section naming round 11's likely focus (change.list's event-log question, or auditing remaining list commands before starting T003 — your call, state your one-sentence reasoning). Follow the exact structure of the R9 handback (commit 9adfbc53, already on disk — read it for the template).

After committing C4, run `git push -u origin feature/f262-list-commands-v2` and report the push result in your closing message.

Do NOT run any `gh pr` command. Do NOT merge anything. Do NOT touch `main`. This round ships no PR — the branch stays open for round 11.

═══════════════════════════════════════════════════════════════
CONSTRAINTS
═══════════════════════════════════════════════════════════════
1. Every FROM string in P1-P5 must be verified to occur exactly once in its target file, using the file's CURRENT content on disk (re-read each file yourself before applying, do not trust cited context blindly). If a FROM does not match, STOP that pair, do not guess a fix, report the exact mismatch in Deviations instead.
2. Do not touch any file not named in this block.
3. Do not run `ruff` if it requires approval you don't have — note the refusal in Deviations if so, not a blocker.
4. If `.agent/STOP` appears at any point mid-round, finish the commit you are mid-way through (if any), then stop and hand off.
5. Keep C2 as ONE commit covering exactly the four named files.
6. Report every command's REAL exit code and REAL output. Never write "green"/"passed" without the actual number.
7. The C3 plan.md gate MUST be an actual byte-for-byte comparison (read both files in binary mode and compare with `==`), not a line-count or diffstat proxy — this is the exact lesson C1 just booked.

END OF BLOCK
