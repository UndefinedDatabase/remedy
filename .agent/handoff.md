# Handoff — F295 session 3, round 14: STOPPED at gate 3 — the exit-code static reader has no `job.resume` entry for D13's shared hand-off (R-1147)

## Session

SESSION 3 of feature F295 · rounds 10 to 14 · rounds so far 14

Context self-assessment (quoted from the block): "The reviewer's context is comfortable after
five rounds; the session continues."

Fortschritt: ~80 % (T001 and T002 landed · T003's stdin proof and the budget decision's two
answers landed · R-1147's providers landed in code and unit-tested, but NOT CLEAN against the
full selection — gate 3 is red, see below; the hunk decision and T004 open; then the hardening
stage and the closure) — Schätzung

## Range

Review of `c2b9a817f`..`23af94e30`, plus this handback commit.

## Commits

### 452b1de1c F295 R14 C1: book round 13, resolve R-1146 and R-1150, DECISION F295 D13, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r14.md` | 146/0 (new) | byte copy of the round 14 block |
| `.agent/live_review.md` | 6/0 | append round 13's gate entry (PASS) and R-1146/R-1150's resolutions, exactly as the reviewer prepared it |
| `.agent/decisions.md` | 10/0 | append DECISION F295 D13 |
| `.agent/plan.md` | 8/11 | rewrite to round 14's current step |

### 6f9f0a195 F295 R14 C2: job resume runs a job the ping-pong engine ran through job run (R-1147)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | 32/3 | DECISION F295 D13 (1) to (3): `_cmd_job_resume`, after the progress line, hands a job whose `execution_config` is not `None` to `_cmd_job_run(str(job.job_id), json_output=json_output)`, imported inside the function from `apps.cli.commands.do_cmd` at call time, and returns; every other job keeps `_cmd_job_run_cycles`, unchanged. When `cycles` is not `None` or `unattended` is true on such a job, one stderr line says `--cycles`/`--unattended` do not apply and the job runs as `remedy job run` runs it. The progress line (`no checkpoint found...` / `resuming from checkpoint...`) now prints to `sys.stderr` when `json_output` is true and to `sys.stdout`, unchanged, otherwise. Docstring rewritten to say where each kind of job goes and why. |

### 8838cb092 F295 R14 C3: unit tests of the resume hand-off and its JSON stdout (R-1147)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_resume_cli.py` | 107/1 | `ExecutionConfig` import; `job_run_calls` fixture standing `_cmd_job_run` in on `apps.cli.commands.do_cmd`; `_pingpong_job()` helper (`make_job()` plus a saved `ExecutionConfig()`); new class `TestResumeHandsAPingPongJobToJobRun` with the four tests the block names: the ping-pong job goes to `_cmd_job_run` with exactly `(str(job.job_id), {"json_output": True})` and `handed_off == []`; a plain job keeps the cycle executor; `--cycles`/`--unattended` note on stderr for a ping-pong job, both flags, each on a fresh job; the progress line on stderr under `--json` (with and without a checkpoint) and on stdout without `--json` (with and without a checkpoint) |

### 23af94e30 F295 R14 C4: a client extends a budget-stopped job and resumes it through its own providers (R-1147)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_decision_cmd.py` | 28/0 | `test_extend_then_resume_runs_the_job_through_its_own_providers` in `TestABudgetDecisionAnsweredThroughTheCommandLine`, reusing `_stopped_job`: answers `extend` with a deadline one day ahead, then `job resume <job> --yes --json` — exit 0, stdout parses as one JSON object whose `status` is `completed`; the job's record read from disk (`load_job_plan`) reads `state` `completed` with `execution_config.builder` still `fake` |

### F295 R14 C5: handback (self-reference exception — committed by this same write)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md`, reporting the gate 3 stop |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` returned `[]` — no open PR
for this branch; the Open PR Gate passes with nothing to merge. No PR opened, no other `gh`
command. After C5: `git push origin feature/f295-machine-client-contract-v1`; its outcome is in
the worker's final reply (write-once rule).

## Verification

Gates ran in the block's order, after C4; the round STOPS at gate 3, which is RED, and gates 4
and 5 were NOT run — the block's own rule: "A gate reporting ... is red ... stop, write the
handoff, push", and the session instructions: "a red gate ... stop at that point, write the
handoff ..., commit it, push, and report."

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty output. Byte comparison of
   every file C1 wrote (`git show 452b1de1c:<path>`) against its prepared file, four of four equal
   (`.agent/authored/f295-r14.md` vs `block.md`, `.agent/live_review.md` vs `dry-live_review.md`,
   `.agent/decisions.md` vs `dry-decisions.md`, `.agent/plan.md` vs `dry-plan.md`).
   ```
   exit 0 (git status), then: True True True True
   ```
2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r14/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check apps/cli/commands/job.py tests/orchestration/test_resume_cli.py
   tests/cli/test_decision_cmd.py`
   ```
   exit 0
   All checks passed!
   ```
3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r14/run_selection.py /home/decodeux/Repos/remedy`
   ```
   exit 1
   FAILED tests/cli/test_exit_codes.py::test_declared_codes_equal_the_codes_the_handler_reaches[job.resume]
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
   1 failed, 4443 passed, 3 skipped in 27.42s
   ```
   One FAILED line, no ERROR line, no `process(es) behind` line. Not re-run.
4. NOT RUN — the round stops at gate 3.
5. NOT RUN — the round stops at gate 3.

### Root cause of the gate 3 failure (read statically; the failing test was not re-run)

`tests/cli/test_exit_codes.py` (DECISION F283 D12 (4)) reads, per catalog command, the exit codes
its handler can statically reach: the handler's own body, same-module calls by bare name, and
`apps.cli`-prefixed imports followed into their own module. A call-site argument it cannot resolve
to a literal int becomes an `_UnresolvedSite`; `_resolved_ints()` looks it up in the module-level
dict `UNRESOLVED_SITES` **keyed by the catalog entry under test** (`entry.command_id`), and fails
the test by name when the site is unresolved for THAT entry, even when the identical site is
already named for a different entry.

`apps/cli/commands/do_cmd.py`'s `_cmd_job_run` contains exactly one such site: the serve
supervisor's `sys.exit(code)` in its `follow_run(body)` branch. Before this round, the static
reader only ever walked into `_cmd_job_run` while analyzing the catalog entry `job.run` itself,
and `UNRESOLVED_SITES` names it there:
`"job.run": (frozenset({0, 1, 2}), "sys.exit(code) in apps/cli/commands/do_cmd.py, code =
follow_run(body) ...")`.

DECISION F295 D13 (1) — this round's C2 — requires `_cmd_job_resume` to hand a ping-pong job to
`_cmd_job_run` directly, `from apps.cli.commands.do_cmd import _cmd_job_run`. The reader's import
collector walks the WHOLE module tree (including imports local to a function body, by design, per
its own comment — "a handler often imports its helper INSIDE the function body"), so it now
resolves `_cmd_job_run` as an `apps.cli`-prefixed import for the `job.resume` entry too, follows
it into `do_cmd._cmd_job_run`, and meets the same unresolved `sys.exit(code)` site — this time
while analyzing `job.resume`. `UNRESOLVED_SITES` has no `"job.resume"` key, so
`_resolved_ints()` calls `pytest.fail(f"{entry.command_id}: unresolved exit-code site with no
entry in UNRESOLVED_SITES: ...")` for that parametrization.

This is a genuine, structural consequence of D13 asking `job.resume` to reach the SAME shared
handler `job.run` already owns — not a bug in C2's code, and not something a different
implementation of D13 (still calling `_cmd_job_run` directly, as the block requires) could avoid.
Repairing it means adding a `"job.resume"` entry to `UNRESOLVED_SITES` in
`tests/cli/test_exit_codes.py`, naming the same hand-verified codes already named for `job.run`
(the path is identical: `job.resume` only reaches it by handing off to the exact same
`_cmd_job_run` call `job.run`'s own handler makes). That file is named in none of this round's
five commits (C1's paths are the four `.agent/*` files; C2 is `apps/cli/commands/job.py` only; C3
and C4 are their own test files only), and the block's own constraint — "No file outside the paths
named per commit" — forbids touching it here even though the fix is narrow and obvious. This is
the kind of contradiction the round's instructions name explicitly: stop, write the handoff, push,
report — not patch a file outside scope to force the gate green.

C1 and C2's own test files (gate 2, and the pre-commit runs noted below) are clean; the single red
line is entirely this cross-cutting, pre-existing exit-code contract test discovering a new,
correct call path.

## Authored-text proofs

- `block.md` → `.agent/authored/f295-r14.md`: 146 lines / 146 lines, sha256
  `a6b98409970ee7787466bad9be6550b18c72811815608b6c3f08338d49d93ed6` / same, byte comparison equal
  (verified before any other read of the block's text, per the round's own opening instruction).
- Every prepared file copied over its target (`dry-live_review.md`, `dry-decisions.md`,
  `dry-plan.md`): byte comparison equal, before the commit and again from the committed bytes in
  gate 1.
- Append proofs: `git show c2b9a817f:.agent/live_review.md` plus the bytes of
  `append-live_review.txt` equals the new file: `True`; the same for `.agent/decisions.md` with
  `append-decisions.txt`: `True`.
- Every prepared file's sha256 was read with Python before use and matched the block's value
  (`dry-live_review.md`, `dry-decisions.md`, `dry-plan.md`, `append-live_review.txt`,
  `append-decisions.txt`, and `block.md` itself, 146 lines, verified first).
- `git diff --cached --numstat` before the C1 commit matched the block's cells exactly: `146 0`
  (the authored copy), `6 0` (the ledger), `10 0` (decisions), `8 11` (the plan).

## Deviations & assumptions

- **Stopped after gate 3's red result, as the round's instructions require.** Gates 4 and 5 were
  NOT run. C5 is written and committed as the stop-and-report handback, not the "all gates green"
  handback the block's C5 section otherwise describes; the sections below explain exactly where
  this handback departs from that description and why.
- The block's C5 asked for `## Round verdicts` naming rounds 1 to 5 and 7 to 13 PASS and round 6
  FAIL (booked in the ledger by this round's C1) and leaving round 14's verdict to the reviewer.
  That is restated below unchanged — it is a historical fact about the ledger, independent of this
  round's own gate 3 result. Round 14 itself cannot be called clean by this worker: the reviewer
  will find gate 3 red when it re-verifies, and that redness, with its cause, is this handback's
  main content.
- The `Fortschritt` line above keeps the block's own prescribed wording, "R-1147's providers
  landed, review pending" — true in the sense that the CODE and its own unit/integration tests
  are landed and pass (C2's 32/3 diff, C3's five new tests, C4's one new test, all green); it is
  NOT true in the sense of "ready to close" — the full selection is red because of the gate 3
  finding above, which the reviewer must resolve (most likely: register `job.resume` in
  `UNRESOLVED_SITES`) before R-1147 can be marked repaired.
- The block's mandated `## For the operator, in plain sentences` text is reproduced below as
  written — it correctly describes what C2 implements — with one added sentence noting that this
  is not yet verified clean end-to-end.
- The block's mandated `## Next` line 4 ("the reviewer reviews round 14 and books its verdict and
  R-1147's resolution in the next round's first commit") is kept, but is no longer the only
  candidate for "R-1147's resolution": the reviewer's first task is the gate 3 contradiction
  itself, before anything else in the block's `## Next` list.
- "Open findings: 5" in `## Next` restates the block's own stated expectation for gate 5
  (`['R-1138', 'R-1139', 'R-1143', 'R-1147', 'R-1149']`), already true of the committed ledger
  after C1 regardless of gate 3 — it is NOT independently re-verified by actually running gate 5,
  since the round stopped before gate 5 ran.
- Helper scripts (`verify_block.py`, `verify_prepared.py`, `verify_concat.py`, `do_c1_copy.py`,
  `c1_append_proofs.py`, `gate1_c1_compare.py`, `investigate_state.py`, `cleanup_investigate.py`)
  under `.remedy-wt/f295-r14-worker/` did the digest checks, byte comparisons, the pre-commit
  functional sanity runs and one disposable investigation (below) the block's sandbox rules
  require. They are not committed (the directory is gitignored).
- Before writing C4, this worker ran a disposable, uncommitted investigation script
  (`investigate_state.py`, under the gitignored worker directory, cleaned up afterward) that drove
  `apps.cli.main` through a real `do` → `job run` (budget stop) → `decision resolve --reason
  extend` → `job run` sequence in a throwaway temp git repo and data root, to confirm by direct
  observation (not by re-reading code alone) that a budget-stopped job's `state` stays `stopped`
  after `extend` and that `run_job` still runs it to completion when no OPERATOR stop is pending
  (the `JOB_STOPPED` early-return in `packages/orchestration/pingpong_job.py` only fires inside
  its `if _pending_guard is not None:` block, not unconditionally — this worker initially
  misread the indentation). This was exploratory reading of existing, already-shipped behavior
  through the CLI, not a test command and not one of the five gates; it ran once, no two commands
  ran concurrently, and its output is not part of this round's evidence — only the understanding
  it produced shaped C4's test, which gate 3's full selection then ran for real.
- Before staging C2, this worker ran `python3 -m ruff check apps/cli/commands/job.py` directly as
  a pre-commit sanity check (not one of the five numbered gates).
- Before staging C3, this worker ran `python3 -m ruff check tests/orchestration/test_resume_cli.py`
  and the whole of that file alone (56 passed, including the 5 new tests) as a pre-commit sanity
  check, permitted under the block's "runs of only the test files you are writing, before you
  commit them" clause.
- Before staging C4, this worker ran `python3 -m ruff check tests/cli/test_decision_cmd.py`, the
  new test alone, and then the whole of that file (22 passed, including the new test) — all
  permitted under the same clause.
  These are additional to, not instead of, the five numbered gates; gates 1 and 2 ran exactly once
  each, in order; gate 3 ran exactly once and is NOT re-run per the stop rule; gates 4 and 5 did
  not run. No two test commands ran at once, no mutation red-proof was run, the full suite ran
  through gate 3 exactly once, and `REMEDY_TEST_MAX_WORKERS` was never set.
- C2, C3 and C4 touched exactly the one path the block named for each, no other module.
- No commit exceeded the 500-insertion cap; the largest (C1) carried 146 insertions, all from the
  authored block copy; C3 carried 107.
- Every commit ends with `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`, the model this
  worker runs on.

## Round verdicts

Rounds 1 to 5 and 7 to 13 PASS and round 6 FAIL, booked in the ledger (round 13 by this round's
C1). Round 14's verdict is the reviewer's to give and book in the next round's first commit; the
reviewer will find gate 3 red and its cause in the `## Verification` section above.

## For the operator, in plain sentences

The command that continues a stopped job now runs a job with the same AI builder and reviewer it
was started with, instead of a local model, and when a program asks for the JSON answer it now
gets only that answer on its output, with the progress message moved to the error channel.
Nothing waits for the operator. This is implemented and unit-tested, but not yet verified clean
against the whole test suite — one pre-existing contract test needs a small update this round's
scope does not cover, and the reviewer will make that call next round.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): not present during this round; if it appears, finish the commit
   in hand, write the handoff and stop.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. **First**: resolve the gate 3 contradiction above — most likely, register `"job.resume"` in
   `UNRESOLVED_SITES` (`tests/cli/test_exit_codes.py`) naming the same codes already named for
   `"job.run"`, since `job.resume` now reaches the identical unresolved site by design (DECISION
   F295 D13). Re-run gate 3 once that lands.
4. Phase 1 rule 4: the reviewer reviews round 14 and books its verdict and R-1147's resolution in
   the next round's first commit, once gate 3 is clean.
5. T003's last part: the hunk decision under `--json`.

Operator questions open: 0.
Open findings: 5 (R-1147 High, owned by F295; R-1138, R-1139, R-1143 and R-1149 Low, owned by
F297) — the committed ledger's count after C1, not independently re-verified since gate 5 did not
run this round.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 (block copy, three record copies, append proofs, numstat) | done | `452b1de1c` |
| C2 (`_cmd_job_resume` hands a ping-pong job to `_cmd_job_run`) | done | `6f9f0a195` |
| C3 (unit tests of the hand-off and the JSON progress line) | done | `8838cb092` |
| C4 (client end-to-end test: extend, then resume through its own providers) | done | `23af94e30` |
| Gate 1 (status and byte comparisons) | done | porcelain empty, four of four equal |
| Gate 2 (ruff) | done | `All checks passed!` |
| Gate 3 (selection) | done | RED — `1 failed, 4443 passed, 3 skipped`, exit 1; not re-run |
| Gate 4 (integrity check) | skipped | not run — the round stops at gate 3's red result |
| Gate 5 (open finding ids) | skipped | not run — the round stops at gate 3's red result |
| C5 handback commit | done | this file |
| Push after C5 | pending | runs right after this commit, reported in the worker's final reply |
