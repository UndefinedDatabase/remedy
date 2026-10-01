# Handoff — F200 Daemon mode (remedy serve), round 5

## Session

SESSION 1 of feature F200 · round 5

Context self-assessment: the reviewer's context is still workable; the session continues.

Fortschritt: ~52 % (T001 complete in its amended scope · T002: supervised runs and client-mode job
run landed, the restart and the artifacts open) — Schätzung

## Range

Review of `17a8cbafc`..`HEAD`: three commits on `feature/f200-daemon-mode` plus this handback
commit: `38f96684e`, `f705c60e9`, `71581610b`, and this commit.

## Commits

### `38f96684e` F200 R5 C1: book round 4 and two prose slips, DECISION F200 D5 with the feature file's paragraph, save the round 5 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f200-r5.md` | +135/-0 | NEW FILE at `.agent/authored/f200-r5.md`; byte-for-byte copy of this round's step block, verified against `.remedy-wt/f200-r5/block.md` before commit (`wc -l` 135, sha256 `a1cf737b2ee89072cb7195ee1e79b66ac4f7f166786a1f3cb27a068a35bb7f14`) |
| `.agent/live_review.md` | +2/-0 | bytes of `.remedy-wt/f200-r5/append-live_review.txt` appended without retyping (books F200 round 4's Gate entry, VERDICT PASS); pre-commit blob (`git show 17a8cbafc:.agent/live_review.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/decisions.md` | +10/-0 | bytes of `.remedy-wt/f200-r5/append-decisions.txt` appended without retyping (records DECISION F200 D5); pre-commit blob (`git show 17a8cbafc:.agent/decisions.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/prose_slips.md` | +2/-0 | bytes of `.remedy-wt/f200-r5/append-prose_slips.txt` appended without retyping (two dated lines for F200 round 4); pre-commit blob (`git show 17a8cbafc:.agent/prose_slips.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/plan.md` | +9/-11 | whole-file `cp` from `.remedy-wt/f200-r5/dry-plan.md`; `cmp` silent |
| `docs/roadmap/features/T12_F200.md` | +5/-0 | whole-file `cp` from `.remedy-wt/f200-r5/dry-T12_F200.md`; `cmp` silent; appends the `**Amended by DECISION F200 D5 (2026-10-01).**` paragraph |

`git diff --cached --numstat` before the commit read `2 0 .agent/live_review.md`,
`10 0 .agent/decisions.md`, `2 0 .agent/prose_slips.md`, `9 11 .agent/plan.md`,
`5 0 docs/roadmap/features/T12_F200.md`, plus `135 0 .agent/authored/f200-r5.md` — matching the
block's stated numbers exactly. `git show --numstat 38f96684e` after the commit read the same six
lines.

### `f705c60e9` F200 R5 C2: a supervised run takes --json and imports the supervisor's own code (DECISION F200 D5)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/serve_runs.py` | +17/-4 | whole-file `cp` from `.remedy-wt/f200-r5/dry-serve_runs.py`; `cmp` silent; adds `CODE_ROOT`, `RunLauncher.start`'s `json_output` keyword and the `PYTHONPATH` env entry |
| `packages/orchestration/serve_daemon.py` | +3/-1 | whole-file `cp` from `.remedy-wt/f200-r5/dry-serve_daemon.py`; `cmp` silent; the socket handler reads `args.json` and passes it to `run_launcher.start` |
| `tests/orchestration/test_serve_runs.py` | +14/-2 | whole-file `cp` from `.remedy-wt/f200-r5/dry-test_serve_runs.py`; `cmp` silent; adds the `json_output` and `CODE_ROOT` tests |

`git diff --cached --numstat` before the commit read `17 4 packages/orchestration/serve_runs.py`,
`3 1 packages/orchestration/serve_daemon.py`, `14 2 tests/orchestration/test_serve_runs.py` —
matching the block's stated numbers exactly. `git show --numstat f705c60e9` after the commit read
the same three lines. `git diff --cached` was read in full as self-review before the commit.

### `71581610b` F200 R5 C3: job run in client mode follows the supervised run to its end (DECISION F200 D5)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/serve_client.py` | +76/-1 | whole-file `cp` from `.remedy-wt/f200-r5/dry-serve_client.py`; `cmp` silent; adds `follow_run` |
| `apps/cli/commands/do_cmd.py` | +20/-0 | whole-file `cp` from `.remedy-wt/f200-r5/dry-do_cmd.py`; `cmp` silent; adds the client-mode seam in `_cmd_job_run`, placed only after the `job_not_resumable` refusal — nothing else, read in full as self-review |
| `tests/cli/test_exit_codes.py` | +8/-0 | whole-file `cp` from `.remedy-wt/f200-r5/dry-test_exit_codes.py`; `cmp` silent; adds only the `job.run` entry of `UNRESOLVED_SITES` — nothing else, read in full as self-review |
| `tests/cli/test_serve_client_parity.py` | +166/-1 | whole-file `cp` from `.remedy-wt/f200-r5/dry-test_serve_client_parity.py`; `cmp` silent; both-modes tests for `job run` and `job run --json` |

`git diff --cached --numstat` before the commit read `76 1 apps/cli/serve_client.py`,
`20 0 apps/cli/commands/do_cmd.py`, `8 0 tests/cli/test_exit_codes.py`,
`166 1 tests/cli/test_serve_client_parity.py` — matching the block's stated numbers exactly.
`git show --numstat 71581610b` after the commit read the same four lines. `git diff --cached` was
read in full as self-review before the commit: it showed in `do_cmd.py` only the commented
client-mode block after the `job_not_resumable` refusal of `_cmd_job_run`, and in
`test_exit_codes.py` only the `job.run` entry of `UNRESOLVED_SITES` — nothing else, confirming the
base had not moved.

### this commit — F200 R5 C4: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this file, per `docs/agents/handback_template.md`; this commit |

## External actions

`git push origin feature/f200-daemon-mode` runs after this commit; its outcome is reported in the
session's own reply, not in this file, because it occurs after this file is written and committed.
No pull request was opened — the block forbids it this round. No worktree was added or removed by
this session's own commands.

## Verification

Gates run once each, in order, strictly after C3 and before C4.

**Gate 1**:
```
$ git status --porcelain
(empty)
```
Then 10 `cmp` proofs, all silent, of every committed file against its prepared file under
`.remedy-wt/f200-r5/`: `.agent/authored/f200-r5.md`/`block.md`, `.agent/plan.md`/`dry-plan.md`,
`docs/roadmap/features/T12_F200.md`/`dry-T12_F200.md`,
`packages/orchestration/serve_runs.py`/`dry-serve_runs.py`,
`packages/orchestration/serve_daemon.py`/`dry-serve_daemon.py`,
`tests/orchestration/test_serve_runs.py`/`dry-test_serve_runs.py`,
`apps/cli/serve_client.py`/`dry-serve_client.py`, `apps/cli/commands/do_cmd.py`/`dry-do_cmd.py`,
`tests/cli/test_exit_codes.py`/`dry-test_exit_codes.py`,
`tests/cli/test_serve_client_parity.py`/`dry-test_serve_client_parity.py` — all 10 silent.

**Gate 2**:
```
$ python3 -m ruff check packages/orchestration/serve_runs.py packages/orchestration/serve_daemon.py apps/cli/serve_client.py apps/cli/commands/do_cmd.py tests/orchestration/test_serve_runs.py tests/cli/test_exit_codes.py tests/cli/test_serve_client_parity.py
All checks passed!
```
Exit 0, captured via a `subprocess.run` wrapper script so the command ran exactly once.

**Gate 3**:
```
$ python3 -m pytest @.remedy-wt/f200-r5/selection.txt -q -n auto -rs
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
4705 passed, 3 skipped in 48.67s
```
Exit 0. No failure, no error, no line containing "process(es) behind". The summary line
(`4705 passed, 3 skipped`) is exactly the block's stated reviewer dry-tree reading
(`4703 passed, 3 skipped`) plus the two tests the reviewer added after that reading
(`test_a_json_run_adds_the_one_option_a_supervised_run_takes`,
`test_the_code_root_holds_the_command_line_the_run_imports`) — matching the block's done-when
arithmetic exactly. Captured via the same `subprocess.run` wrapper pattern so the command ran
exactly once.

**Gate 4**:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0. `fail_count` 0.

**Gate 5**:
```
$ python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
['R-1117', 'R-1125', 'R-1127', 'R-1128', 'R-1129']
```
Exit 0. Matches exactly.

## Authored-text proofs

`.agent/authored/f200-r5.md` (commit `38f96684e`): saved as a byte-for-byte copy of the step block
given to this round; `wc -l` read 135 lines, `sha256sum` read
`a1cf737b2ee89072cb7195ee1e79b66ac4f7f166786a1f3cb27a068a35bb7f14`, matching both the delivering
prompt's stated digest/line count and `block.md`'s own digest; `cmp` against `block.md` printed
nothing.

`.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` (commit `38f96684e`):
the append-byte-equality proofs (pre-commit blob at `17a8cbafc` plus the respective append bytes
equals the post-append file) each read `True`.

`.agent/plan.md`, `docs/roadmap/features/T12_F200.md` (commit `38f96684e`);
`packages/orchestration/serve_runs.py`, `packages/orchestration/serve_daemon.py`,
`tests/orchestration/test_serve_runs.py` (commit `f705c60e9`); `apps/cli/serve_client.py`,
`apps/cli/commands/do_cmd.py`, `tests/cli/test_exit_codes.py`,
`tests/cli/test_serve_client_parity.py` (commit `71581610b`): whole-file replace from their
respective `dry-*` prepared files; `cmp` against each prepared file printed nothing.

## Deviations & assumptions

None. The block's own digest (`a1cf737b2ee89072cb7195ee1e79b66ac4f7f166786a1f3cb27a068a35bb7f14`,
135 lines) and every prepared companion file's digest were verified with `sha256sum` before use and
matched the block exactly, before any file was applied. All three code/record commits matched the
block's named paths and numstat exactly — no file outside the paths named per commit, no extra
hunk; `git diff --cached` was read as self-review before each of C2 and C3's commits and showed
only the named changes. All five gates matched the block's stated done-when readings, run exactly
once each, after C3 and before C4. No mutation red-proof ran (amend0930-test-load rule 4, reserved
to the reviewer in a disposable worktree). No full suite ran and `REMEDY_TEST_MAX_WORKERS` was not
set; every test command passed `-n auto`, and only one test command ran at any time. No gate line
contained "process(es) behind". `.agent/STOP` did not appear at any point in this round.

## Next

1. Phase 1 rule 1 (`.agent/STOP`) — check first, in the next session.
2. Phase 1 rule 2 (the Open PR Gate).
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 5's verdict in the next round's first commit.
5. The restart that runs registered jobs again, with its SIGKILL test.

Operator questions open: 1.
Open findings: 5 (R-1117, R-1125, R-1127, R-1128, R-1129, all owned by F290).

## Item status

| Item | Status | Reason |
|---|---|---|
| Book round 4's verdict (PASS) in `.agent/live_review.md` | done | commit `38f96684e` |
| Append two dated lines to `.agent/prose_slips.md` | done | commit `38f96684e` |
| Record DECISION F200 D5 in `.agent/decisions.md` | done | commit `38f96684e` |
| Append the amendment paragraph to `docs/roadmap/features/T12_F200.md` | done | commit `38f96684e` |
| Advance `.agent/plan.md` | done | commit `38f96684e` |
| NEW FILE `.agent/authored/f200-r5.md` (copy of `block.md`) | done | commit `38f96684e` |
| `--json` and the code root's import path in `serve_runs.py` | done | commit `f705c60e9` |
| The socket's `args.json` in `serve_daemon.py` | done | commit `f705c60e9` |
| Tests for `RunLauncher.start`'s `json_output` and `CODE_ROOT` | done | commit `f705c60e9` |
| `follow_run` in `apps/cli/serve_client.py` | done | commit `71581610b` |
| The client-mode seam in `_cmd_job_run` of `do_cmd.py` | done | commit `71581610b` |
| `job.run` entry in `tests/cli/test_exit_codes.py`'s `UNRESOLVED_SITES` | done | commit `71581610b` |
| Both-modes tests in `tests/cli/test_serve_client_parity.py` | done | commit `71581610b` |
| Gates 1-5 before the handback | done | all matched the block's stated readings, each run exactly once |
| Rewrite `.agent/handoff.md` | done | this file |
| Push | done/reported in reply | `git push origin feature/f200-daemon-mode` — outcome in the session's own reply |
