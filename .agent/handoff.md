# Handoff — F200 Daemon mode (remedy serve), round 6

## Session

SESSION 2 of feature F200 · round 6

Context self-assessment: context remains workable after four commits and five gates this round.

Fortschritt: ~65 % (T001 complete in its amended scope · T002: supervised runs, client-mode job run
and the restart landed, the artifacts open) — Schätzung

## Range

Review of `9bdd7bb61`..`HEAD`: the operator's commit, three commits on `feature/f200-daemon-mode`
and this handback commit: `70c984073`, `afed9f95a`, `6513a1486`, `cefeed64b`, and this commit.

## Commits

### `70c984073` Operator answers recorded: Q4

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +10/-0 | records DECISION F200 D6, the operator's answer to question Q4; written by the operator, not this round's worker |
| `.agent/operator_questions.md` | +1/-34 | closes question Q4, leaving the file's live-question count at zero |

This commit precedes this round's own base (`70c984073`, confirmed by `git rev-parse HEAD` before
any write) and is not one of this round's four ordered commits; it is listed here only because the
template requires every commit in the reviewed range.

### `afed9f95a` F200 R6 C1: book round 5 and one prose slip, DECISION F200 D7 with the feature file's paragraph, save the round 6 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f200-r6.md` | +128/-0 | NEW FILE at `.agent/authored/f200-r6.md`; byte-for-byte copy of this round's step block, verified against `.remedy-wt/f200-r6/block.md` before commit (`wc -l` 128, sha256 `7290feb25ef545bfcbc4036e2ae9ab4153b86e1d09acdcb521809f9992a518f5`) |
| `.agent/live_review.md` | +2/-0 | bytes of `.remedy-wt/f200-r6/append-live_review.txt` appended without retyping (books F200 round 5's Gate entry, VERDICT PASS); pre-commit blob (`git show 70c984073:.agent/live_review.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/decisions.md` | +10/-0 | bytes of `.remedy-wt/f200-r6/append-decisions.txt` appended without retyping (records DECISION F200 D7); pre-commit blob (`git show 70c984073:.agent/decisions.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/prose_slips.md` | +1/-0 | bytes of `.remedy-wt/f200-r6/append-prose_slips.txt` appended without retyping (one dated line for F200 round 5); pre-commit blob (`git show 70c984073:.agent/prose_slips.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/plan.md` | +9/-9 | whole-file `cp` from `.remedy-wt/f200-r6/dry-plan.md`; `cmp` silent |
| `docs/roadmap/features/T12_F200.md` | +5/-0 | whole-file `cp` from `.remedy-wt/f200-r6/dry-T12_F200.md`; `cmp` silent; appends the `**Amended by DECISION F200 D7 (2026-10-01).**` paragraph |

`git diff --cached --numstat` before the commit read `2 0 .agent/live_review.md`,
`10 0 .agent/decisions.md`, `1 0 .agent/prose_slips.md`, `9 9 .agent/plan.md`,
`5 0 docs/roadmap/features/T12_F200.md`, plus `128 0 .agent/authored/f200-r6.md` — matching the
block's stated numbers exactly. `git show --numstat afed9f95a` after the commit read the same six
lines.

### `6513a1486` F200 R6 C2: the supervisor settles its open runs when it starts — adopt, run again or record as lost (DECISION F200 D7)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/serve_runs.py` | +162/-2 | whole-file `cp` from `.remedy-wt/f200-r6/dry-serve_runs.py`; `cmp` silent; adds `_process_is_alive`, `_process_is_this_job`, `RunLauncher.resume_registered`, `_job_is_running`, `_adopt` and `_watch_adopted`, and the `_adopted` set that `running`/`start` now also consult |
| `packages/orchestration/serve_daemon.py` | +8/-0 | whole-file `cp` from `.remedy-wt/f200-r6/dry-serve_daemon.py`; `cmp` silent; `run_supervisor` takes `job_is_running` and calls `launcher.resume_registered(job_is_running=job_is_running)` after the pid file is written and before any signal handler installs, any serving thread starts, or `on_ready` fires |
| `tests/orchestration/test_serve_runs.py` | +213/-0 | whole-file `cp` from `.remedy-wt/f200-r6/dry-test_serve_runs.py`; `cmp` silent; adds the restart/adopt/lost/failed `resume_registered` tests, the default-reader tests against real job records, and their `_plant_record`/`_dead_pid`/`_spawn_child` fixtures |

`git diff --cached --numstat` before the commit read `162 2 packages/orchestration/serve_runs.py`,
`8 0 packages/orchestration/serve_daemon.py`, `213 0 tests/orchestration/test_serve_runs.py` —
matching the block's stated numbers exactly. `git show --numstat 6513a1486` after the commit read
the same three lines. `git diff --cached` was read in full as self-review before the commit.

### `cefeed64b` F200 R6 C3: the restart kill test — SIGKILL the supervisor and its run, start again, every task once (DECISION F200 D7)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_serve_restart_kill.py` | +245/-0 | NEW FILE at `tests/orchestration/test_serve_restart_kill.py`; whole-file `cp` from `.remedy-wt/f200-r6/dry-test_serve_restart_kill.py`; `cmp` silent; runs a real supervisor subprocess and a real run child in its own session, SIGKILLs both mid-task, starts a second supervisor on the same data root, and reads the cycle evidence records on disk to prove each task executed exactly once and the job completed |

`git diff --cached --numstat` before the commit read exactly `245 0
tests/orchestration/test_serve_restart_kill.py` — matching the block's stated number exactly.
`git show --numstat cefeed64b` after the commit read the same line. The file was read in full as
self-review before the commit.

### this commit — F200 R6 C4: handback

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
Then 7 `cmp` proofs, all silent, of every committed file against its prepared file under
`.remedy-wt/f200-r6/`: `.agent/authored/f200-r6.md`/`block.md`, `.agent/plan.md`/`dry-plan.md`,
`docs/roadmap/features/T12_F200.md`/`dry-T12_F200.md`,
`packages/orchestration/serve_runs.py`/`dry-serve_runs.py`,
`packages/orchestration/serve_daemon.py`/`dry-serve_daemon.py`,
`tests/orchestration/test_serve_runs.py`/`dry-test_serve_runs.py`,
`tests/orchestration/test_serve_restart_kill.py`/`dry-test_serve_restart_kill.py` — all 7 silent.

**Gate 2**:
```
$ python3 -m ruff check packages/orchestration/serve_runs.py packages/orchestration/serve_daemon.py tests/orchestration/test_serve_runs.py tests/orchestration/test_serve_restart_kill.py
All checks passed!
```
Exit 0, captured via a `subprocess.run` wrapper script so the command ran exactly once.

**Gate 3**:
```
$ python3 -m pytest @.remedy-wt/f200-r6/selection.txt -q -n auto -rs
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
4723 passed, 3 skipped in 35.68s
```
Exit 0. No failure, no error, no line containing "process(es) behind". The summary line
(`4723 passed, 3 skipped`) is exactly the block's stated reviewer dry-tree reading
(`4723 passed, 3 skipped`). Captured via the same `subprocess.run` wrapper pattern so the command
ran exactly once.

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

`.agent/authored/f200-r6.md` (commit `afed9f95a`): saved as a byte-for-byte copy of the step block
given to this round; `wc -l` read 128 lines, `sha256sum` read
`7290feb25ef545bfcbc4036e2ae9ab4153b86e1d09acdcb521809f9992a518f5`, matching both the delivering
prompt's stated digest/line count and `block.md`'s own digest; `cmp` against `block.md` printed
nothing.

`.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` (commit `afed9f95a`):
the append-byte-equality proofs (pre-commit blob at `70c984073` plus the respective append bytes
equals the post-append file) each read `True`.

`.agent/plan.md`, `docs/roadmap/features/T12_F200.md` (commit `afed9f95a`);
`packages/orchestration/serve_runs.py`, `packages/orchestration/serve_daemon.py`,
`tests/orchestration/test_serve_runs.py` (commit `6513a1486`);
`tests/orchestration/test_serve_restart_kill.py` (commit `cefeed64b`): whole-file replace from
their respective `dry-*` prepared files; `cmp` against each prepared file printed nothing.

## Deviations & assumptions

None. The block's own digest (`7290feb25ef545bfcbc4036e2ae9ab4153b86e1d09acdcb521809f9992a518f5`,
128 lines) and every prepared companion file's digest were verified with `sha256sum` before use and
matched the block exactly, before any file was applied. All three code/record commits matched the
block's named paths and numstat exactly — no file outside the paths named per commit, no extra
hunk; `git diff --cached` was read as self-review before each of C2 and C3's commits (and C1's
record diffs), and showed only the named changes. All five gates matched the block's stated
done-when readings, run exactly once each, after C3 and before C4. No mutation red-proof ran
(amend0930-test-load rule 4, reserved to the reviewer in a disposable worktree). No full suite ran
and `REMEDY_TEST_MAX_WORKERS` was not set; every test command passed `-n auto`, and only one test
command ran at any time. No gate line contained "process(es) behind". `.agent/STOP` did not appear
at any point in this round. The operator's commit `70c984073`, which sits in this round's reviewed
range between round 5's handback and this round's base, is tabled above for the template's "every
commit in the range" rule but is not one of this round's four ordered commits.

## Next

1. Phase 1 rule 1 (`.agent/STOP`) — check first, in the next session.
2. Phase 1 rule 2 (the Open PR Gate).
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 6's verdict in the next round's first commit.
5. The systemd unit, the container entrypoint and the built-state page.

Operator questions open: 0.
Open findings: 5 (R-1117, R-1125, R-1127, R-1128, R-1129, all owned by F290).

## Item status

| Item | Status | Reason |
|---|---|---|
| Book round 5's verdict (PASS) in `.agent/live_review.md` | done | commit `afed9f95a` |
| Append one dated line to `.agent/prose_slips.md` | done | commit `afed9f95a` |
| Record DECISION F200 D7 in `.agent/decisions.md` | done | commit `afed9f95a` |
| Append the amendment paragraph to `docs/roadmap/features/T12_F200.md` | done | commit `afed9f95a` |
| Advance `.agent/plan.md` | done | commit `afed9f95a` |
| NEW FILE `.agent/authored/f200-r6.md` (copy of `block.md`) | done | commit `afed9f95a` |
| `RunLauncher.resume_registered` in `serve_runs.py` | done | commit `6513a1486` |
| `run_supervisor` calls it before it serves any request, in `serve_daemon.py` | done | commit `6513a1486` |
| Unit tests for the restart in `tests/orchestration/test_serve_runs.py` | done | commit `6513a1486` |
| NEW FILE `tests/orchestration/test_serve_restart_kill.py` (the SIGKILL test) | done | commit `cefeed64b` |
| Gates 1-5 before the handback | done | all matched the block's stated readings, each run exactly once |
| Rewrite `.agent/handoff.md` | done | this file |
| Push | done/reported in reply | `git push origin feature/f200-daemon-mode` — outcome in the session's own reply |
