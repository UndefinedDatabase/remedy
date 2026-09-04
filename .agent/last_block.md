═══════════════════════════════════════════════════════════════
STEP — F262 R12/? — test.list gains a real per-row text listing
═══════════════════════════════════════════════════════════════

GOAL: Fix a pre-existing gap round 11's audit found: `test.list`'s `--json` branch already carries `created_at` per row (added long before this feature), but its TEXT branch prints only a bare count (`"Test runs for {job}: {N}"`) with NO per-row listing at all — wider than a missing date, since there are no rows to attach one to. Give the text branch a real per-row listing (test_run_id, status, exit_code, created) matching the shape already used elsewhere in this feature (`review.list`, `patch.list`), and an honest empty-state message. Also book round 11's reviewer verdict into the ledger.

BACKGROUND FACTS (already verified by the reviewer — do not re-derive):
- `apps/cli/commands/real_test_execution_cmd.py`'s `_cmd_test_list` already builds a fully-shaped `out["runs"]` list (each row: `test_run_id`, `status`, `exit_code`, `created_at`) for the JSON branch — the TEXT branch below it just never used it, printing only `len(runs)`. No new field needs to be added anywhere; this round only wires the TEXT branch to data that already exists.
- `tests/cli/test_real_test_execution_cli.py` already has `test_test_list_empty` (JSON-only, checks `run_count == 0`) and uses a `run_grouped_cli` subprocess helper plus a `_job(env)` fixture helper already defined in that file — do not redefine either.
- `_cmd_test_list` never calls `load_job`; it only calls `list_test_runs(job_id)` directly, so a job ID does not need to be a real persisted job for a direct-call test of this function — a bare `str(uuid4())` is sufficient when `list_test_runs` itself is mocked.

═══ COMMIT SEQUENCE (5 commits total) ═══

──────────────────────────────────────────────────────────
C0a — save this entire step block verbatim
──────────────────────────────────────────────────────────
Save the FULL literal text of this prompt message (everything between the "STEP —" header above and the final "END OF BLOCK" marker at the bottom) to `.agent/authored/f262-r12.md`, byte for byte, exactly as received. Commit message: `F262 R12 C0a: save block verbatim to .agent/authored/f262-r12.md`

──────────────────────────────────────────────────────────
C0b — mirror to .agent/last_block.md
──────────────────────────────────────────────────────────
Copy `.agent/authored/f262-r12.md` to `.agent/last_block.md`, whole-file replace. Verify `sha256sum` of both files matches after writing. Commit message: `F262 R12 C0b: mirror block to .agent/last_block.md`

──────────────────────────────────────────────────────────
C1 — append GATE11 to .agent/live_review.md
──────────────────────────────────────────────────────────
Append exactly the text between the GATE11 markers below to the END of `.agent/live_review.md`: one newline, then the GATE11 text verbatim (it is a SINGLE LINE — no internal newlines), nothing else added.

<<<BEGIN GATE11>>>
Gate: R11 — the F262 R11 entry. R11 SHIPPED T002 BATCH 9, review.list gains a CREATED date end to end: `ReviewerRecommendation` gains a `created_at` field stamped once in `run_reviewer()` at construction time (datetime/timezone), carried through `store_recommendations()`'s persisted dict, and rendered as a `(created=...)` suffix in `_cmd_review_list`'s text branch — its `--json` branch needed no code change since it already prints `list_recommendations()`'s own dicts verbatim — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r11.md`/`.agent/last_block.md` share one sha256 digest, `22243901b501929043ad99dd8aa873620c89f476fe82753f6e4c4d4e30622d13`, confirmed by the reviewer's own sha256sum of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff c37fd166..a57aa2d4` for `packages/orchestration/reviewer.py` and `apps/cli/commands/review_cmd.py` shows exactly PAIR P1 (datetime/timezone import), PAIR P2 (created_at field append on the dataclass), PAIR P3 (run_reviewer stamps created_at), PAIR P4 (store_recommendations persists created_at), PAIR P5 (review_cmd.py's text loop gains a created= suffix), every other line in both files untouched, confirmed by reading the full diff. `python3 -m py_compile` exited 0 on all four touched/added files (reviewer.py, review_cmd.py, test_approval_queue.py, test_review_cmd.py), run together by the reviewer. THE GATE10 LEDGER APPEND (commit f794abda) WAS RE-VERIFIED BYTE-EXACT: base (2446822 bytes) + one newline + GATE10 (2871 bytes, 0 internal newlines) reproduces the post-commit file (2449694 bytes) exactly. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `tests/cli/test_review_cmd.py tests/orchestration/test_approval_queue.py` read 28 passed. THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read 646 passed, matching 515+52+21+16+42 exactly. HYGIENE HELD: `git status --porcelain` empty at HEAD `de9d412e`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 2144 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN12 slice against the written file. ONE DECLARED DEVIATION VERIFIED AS HARMLESS, NOT A DEFECT: the new file `tests/cli/test_review_cmd.py` carries one trailing newline byte beyond the block's literal content (standard POSIX Write-tool convention, confirmed by the worker's own byte comparison, `t2 == written[:-1]` true) — no line of code differs, no product effect, not even a prose_slips.md line, since it is neither `.agent/` prose nor a defect of any kind. THE VERDICT IS PASS.
<<<END GATE11>>>

Commit message: `F262 R12 C1: append GATE11 to live_review.md - books round 11's PASS verdict`

──────────────────────────────────────────────────────────
C2 — production pair + tests (one commit, one production file, one test file)
──────────────────────────────────────────────────────────

PAIR P1 (REWRITE) — `apps/cli/commands/real_test_execution_cmd.py`, `_cmd_test_list`'s text branch gains a real per-row listing.
FROM (exact):
<<<BEGIN PAIR_P1_FROM>>>
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"Test runs for {str(args.job_id)[:8]}: {len(runs)}")
<<<END PAIR_P1_FROM>>>
TO:
<<<BEGIN PAIR_P1_TO>>>
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    if not out["runs"]:
        print(f"No test runs for {str(args.job_id)[:8]}.")
        return
    for r in out["runs"]:
        print(f"  {r['test_run_id']}  status={r['status']}  exit={r['exit_code']}  created={r['created_at']}")
<<<END PAIR_P1_TO>>>
Verify FROM occurs exactly once in the file before applying. Do NOT touch the JSON branch above this, the `out` dict construction above that, or `list_test_runs`/`_cmd_test_result`/`_cmd_test_integrity` — none of those are part of this round's change set.

TEST T1 (APPEND) — `tests/cli/test_real_test_execution_cli.py`. Insert this new test immediately after `test_test_list_empty` (which ends `assert json.loads(r.stdout)["run_count"] == 0`) and before `test_test_integrity`:
FROM (exact):
<<<BEGIN T1_FROM>>>
    assert json.loads(r.stdout)["run_count"] == 0


def test_test_integrity(env):
<<<END T1_FROM>>>
TO:
<<<BEGIN T1_TO>>>
    assert json.loads(r.stdout)["run_count"] == 0


def test_test_list_empty_text_message(env):
    jid = _job(env)
    r = run_grouped_cli(["test", "list", jid], env)
    assert r.returncode == 0, r.stderr
    assert f"No test runs for {jid[:8]}." in r.stdout


def test_test_list_text_shows_per_row(capsys):
    from argparse import Namespace
    from unittest.mock import patch

    from apps.cli.commands.real_test_execution_cmd import _cmd_test_list

    job_id = str(uuid4())
    fake_runs = [{"test_run_id": "run-1", "status": "passed", "exit_code": 0,
                  "created_at": "2026-09-04T00:00:00+00:00"}]
    args = Namespace(job_id=job_id, json=False)
    with patch("packages.orchestration.real_test_execution.list_test_runs", return_value=fake_runs):
        _cmd_test_list(args)

    out = capsys.readouterr().out
    assert "run-1" in out
    assert "status=passed" in out
    assert "exit=0" in out
    assert "created=2026-09-04T00:00:00+00:00" in out


def test_test_integrity(env):
<<<END T1_TO>>>
Verify FROM occurs exactly once in the file before applying. `uuid4` is already imported at module scope in this file (`from uuid import uuid4`) — do not re-import it. This file's existing tests are plain module-level functions (not inside a class) — insert T1's three new functions the same way, no indentation.

Apply P1 and T1. Both files (1 production: `apps/cli/commands/real_test_execution_cmd.py`; 1 test: `tests/cli/test_real_test_execution_cli.py`) in ONE commit.

Run `python3 -m py_compile apps/cli/commands/real_test_execution_cmd.py tests/cli/test_real_test_execution_cli.py` and confirm exit 0. Then run `python3 -m pytest tests/cli/test_real_test_execution_cli.py -q` and record the exact pass count verbatim — expected 7 (5 pre-existing + 2 new). Commit message: `F262 R12 C2: test.list gains a real per-row text listing`

──────────────────────────────────────────────────────────
C3 — replace .agent/plan.md with PLAN13
──────────────────────────────────────────────────────────
Replace the ENTIRE content of `.agent/plan.md` with exactly the text between the PLAN13 markers below (whole-file replace, byte-exact — verify with an actual byte-for-byte binary comparison, not `wc -l`/diffstat):

<<<BEGIN PLAN13>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 12, session 5 - test.list's TEXT branch gains a real per-row
listing (test_run_id, status, exit_code, created), replacing the old
bare-count-only print; an honest "No test runs for X." message covers
the empty case. --json needed no change - it already carried every
field the text branch now uses, sourced from the same out["runs"]
list built earlier in _cmd_test_list. This closes the last gap
round 11's audit found: every catalog list command now either shows a
date, or is explicitly excused in Risks below.

## Next Steps

- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
  This is the one remaining named, excused gap.
- T003 (sort/filter/limit) can start now: every list command either
  carries a date (job/queue/loop/project/patch/memory/tournament/
  blocker/decision/propose/review/test/event, event.list's own
  `timestamp` field counting) or is excused (execution.list/
  worker.list/config.list: no timestamp concept or a pre-existing
  --json-unconditional quirk; change.list: DECISION F262 D1).
- T003 design should start with the shared `_with_list_options()`
  surface in apps/cli/command_catalog.py (already injects --sort/
  --since/--until/--limit into every list subcommand per T001) and
  decide where the actual sort/filter/limit BEHAVIOUR lives - likely
  one shared helper each list handler's text/json branches call,
  rather than 18 hand-rolled implementations.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
<<<END PLAN13>>>

Commit message: `F262 R12 C3: replace plan.md with PLAN13`

──────────────────────────────────────────────────────────
C4 — handback
──────────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` (whole-file, per AGENTS.md's handback contract) with: Session (SESSION 5 of feature F262, round 12, rounds so far 12), a Range section stating this handback covers `de9d412e..<C3 sha>` (C4/this handback commit is NOT part of the reviewed content range), an Item Status table (Preconditions, C0a, C0b, C1, C2, C3, C4, plus one row per gate you ran), a Commits table with every file changed per commit and its +/- line counts from `git show --numstat`, a Verification section with the REAL output of every command you ran (py_compile exit codes, the exact pytest pass count for C2's run, the canary suite run as ONE combined invocation: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`, expected 646 passed), a Deviations & assumptions section (state honestly anything that didn't go exactly as ordered, including the plan.md byte-equality check result), and a Next section naming round 13's likely focus — your call: start T003's design (sort/filter/limit behaviour), given PLAN13's Next Steps says every list command's date coverage is now resolved or excused except change.list. State your one-sentence reasoning. Follow the exact structure of the R11 handback (commit de9d412e, already on disk — read it for the template).

After committing C4, run `git push -u origin feature/f262-list-commands-v2` and report the push result in your closing message.

Do NOT run any `gh pr` command. Do NOT merge anything. Do NOT touch `main`. This round ships no PR — the branch stays open for round 13.

═══════════════════════════════════════════════════════════════
CONSTRAINTS
═══════════════════════════════════════════════════════════════
1. Every FROM string in P1 and T1 must be verified to occur exactly once in its target file, using the file's CURRENT content on disk (re-read each file yourself before applying, do not trust cited context blindly). If a FROM does not match, STOP that pair, do not guess a fix, report the exact mismatch in Deviations instead.
2. Do not touch any file not named in this block.
3. Do not run `ruff` if it requires approval you don't have — note the refusal in Deviations if so, not a blocker.
4. If `.agent/STOP` appears at any point mid-round, finish the commit you are mid-way through (if any), then stop and hand off.
5. Keep C2 as ONE commit covering exactly the two named files.
6. Report every command's REAL exit code and REAL output. Never write "green"/"passed" without the actual number.
7. The C3 plan.md gate MUST be an actual byte-for-byte comparison (read both files in binary mode and compare with `==`), not a line-count or diffstat proxy.
8. `test_test_list_text_shows_per_row` does not use the `env`/`_job` fixtures — `_cmd_test_list` never calls `load_job`, only `list_test_runs`, so a bare `str(uuid4())` job id plus a monkeypatched `list_test_runs` is sufficient and does not require `REMEDY_DATA_DIR` to be set. Do not add an unused `env` fixture to that test.

END OF BLOCK
