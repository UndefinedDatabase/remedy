# Handoff — F200 Daemon mode (remedy serve), round 4

## Session

SESSION 1 of feature F200 · round 4

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~40 % (T001 complete in its amended scope · T002: the supervisor's runs landed,
client-mode job run, the restart and the artifacts open) — Schätzung

## Range

Review of `bb22ee016`..`HEAD`: three commits on `feature/f200-daemon-mode` plus this handback
commit: `16a19967d`, `412e9dc02`, `de2e85a8d`, and this commit.

## Commits

### `16a19967d` F200 R4 C1: book round 3, DECISION F200 D4 with the feature file's addendum and Q4's update, save the round 4 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f200-r4.md` | +139/-0 | NEW FILE at `.agent/authored/f200-r4.md`; byte-for-byte copy of this round's step block, verified against `.remedy-wt/f200-r4/block.md` before commit (`wc -l` 139, sha256 `1cc85b0cb80f92b3d67a7ded6e8c8d8e9c119dcba51c417a95881ed1621319d5`) |
| `.agent/live_review.md` | +2/-0 | bytes of `.remedy-wt/f200-r4/append-live_review.txt` appended without retyping (books F200 round 3's Gate entry, VERDICT PASS); pre-commit blob (`git show bb22ee016:.agent/live_review.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/decisions.md` | +10/-0 | bytes of `.remedy-wt/f200-r4/append-decisions.txt` appended without retyping (records DECISION F200 D4); pre-commit blob (`git show bb22ee016:.agent/decisions.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/plan.md` | +14/-14 | whole-file `cp` from `.remedy-wt/f200-r4/dry-plan.md`; `cmp` silent |
| `.agent/operator_questions.md` | +11/-9 | whole-file `cp` from `.remedy-wt/f200-r4/dry-operator_questions.md`; `cmp` silent; Q4's body updated to name the four commands |
| `docs/roadmap/features/T12_F200.md` | +5/-0 | whole-file `cp` from `.remedy-wt/f200-r4/dry-T12_F200.md`; `cmp` silent; appends the `**Amended by DECISION F200 D4 (2026-10-01).**` paragraph |

`git diff --cached --numstat` before the commit read `2 0 .agent/live_review.md`,
`10 0 .agent/decisions.md`, `14 14 .agent/plan.md`, `11 9 .agent/operator_questions.md`,
`5 0 docs/roadmap/features/T12_F200.md`, plus `139 0 .agent/authored/f200-r4.md` — matching the
block's stated numbers exactly. `git show --numstat 16a19967d` after the commit read the same six
lines.

### `412e9dc02` F200 R4 C2: the run launcher and its run registry (DECISION F200 D4)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/serve_runs.py` | +140/-0 | NEW FILE at `packages/orchestration/serve_runs.py`; whole-file `cp` from `.remedy-wt/f200-r4/dry-serve_runs.py`; `cmp` silent; the run launcher and its run registry, carries `DIRECT_ENV` |
| `tests/orchestration/test_serve_runs.py` | +123/-0 | NEW FILE at `tests/orchestration/test_serve_runs.py`; whole-file `cp` from `.remedy-wt/f200-r4/dry-test_serve_runs.py`; `cmp` silent |
| `apps/cli/serve_client.py` | +2/-2 | whole-file `cp` from `.remedy-wt/f200-r4/dry-serve_client.py`; `cmp` silent; its own `DIRECT_ENV` constant replaced by an import from `serve_runs` and an `__all__` line — nothing else, read in full as self-review |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | whole-file `cp` from `.remedy-wt/f200-r4/dry-import_reachability_allowlist.txt`; `cmp` silent; adds `packages.orchestration.serve_runs` |

`git diff --cached --numstat` before the commit read `2 2 apps/cli/serve_client.py`,
`140 0 packages/orchestration/serve_runs.py`,
`1 0 tests/orchestration/import_reachability_allowlist.txt`,
`123 0 tests/orchestration/test_serve_runs.py` — matching the block's stated numbers exactly.
`git show --numstat 412e9dc02` after the commit read the same four lines. `git diff --cached` was
read in full as self-review before the commit: it showed in `serve_client.py` only its own
`DIRECT_ENV` constant replaced by an import from `serve_runs` plus the `__all__` line — nothing
else.

### `de2e85a8d` F200 R4 C3: the supervisor's socket accepts job.run through the door's extra-command hook (DECISION F200 D4)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/ui_server.py` | +21/-0 | whole-file `cp` from `.remedy-wt/f200-r4/dry-ui_server.py`; `cmp` silent; adds the hook call with its comment before the 501 guard of `_handle_command_submission`, and the `_dispatch_extra_command` method before `_command_is_ui_exposed` — nothing else |
| `packages/orchestration/serve_daemon.py` | +49/-13 | whole-file `cp` from `.remedy-wt/f200-r4/dry-serve_daemon.py`; `cmp` silent; the socket handler class overrides `_dispatch_extra_command` for `job.run`, and the launcher wires it |
| `tests/orchestration/test_serve_daemon.py` | +95/-3 | whole-file `cp` from `.remedy-wt/f200-r4/dry-test_serve_daemon.py`; `cmp` silent; tests for the `job.run` socket path |
| `tests/cli/test_serve_client_parity.py` | +1/-1 | whole-file `cp` from `.remedy-wt/f200-r4/dry-test_serve_client_parity.py`; `cmp` silent |

`git diff --cached --numstat` before the commit read `21 0 packages/orchestration/ui_server.py`,
`49 13 packages/orchestration/serve_daemon.py`, `95 3 tests/orchestration/test_serve_daemon.py`,
`1 1 tests/cli/test_serve_client_parity.py` — matching the block's stated numbers exactly.
`git show --numstat de2e85a8d` after the commit read the same four lines. `git diff --cached` was
read in full as self-review before the commit: it showed in `ui_server.py` only the hook call with
its comment before the 501 guard of `_handle_command_submission`, and the `_dispatch_extra_command`
method before `_command_is_ui_exposed` — nothing else.

### this commit — F200 R4 C4: handback

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
Then 12 `cmp` proofs, all silent, of every committed file against its prepared file under
`.remedy-wt/f200-r4/`: `.agent/authored/f200-r4.md`/`block.md`, `.agent/plan.md`/`dry-plan.md`,
`.agent/operator_questions.md`/`dry-operator_questions.md`,
`docs/roadmap/features/T12_F200.md`/`dry-T12_F200.md`,
`packages/orchestration/serve_runs.py`/`dry-serve_runs.py`,
`tests/orchestration/test_serve_runs.py`/`dry-test_serve_runs.py`,
`apps/cli/serve_client.py`/`dry-serve_client.py`,
`tests/orchestration/import_reachability_allowlist.txt`/`dry-import_reachability_allowlist.txt`,
`packages/orchestration/ui_server.py`/`dry-ui_server.py`,
`packages/orchestration/serve_daemon.py`/`dry-serve_daemon.py`,
`tests/orchestration/test_serve_daemon.py`/`dry-test_serve_daemon.py`,
`tests/cli/test_serve_client_parity.py`/`dry-test_serve_client_parity.py` — all 12 silent.

**Gate 2**:
```
$ python3 -m ruff check packages/orchestration/serve_runs.py packages/orchestration/serve_daemon.py packages/orchestration/ui_server.py apps/cli/serve_client.py tests/orchestration/test_serve_runs.py tests/orchestration/test_serve_daemon.py tests/cli/test_serve_client_parity.py
All checks passed!
```
Exit 0, captured via a `subprocess.run` wrapper script so the command ran exactly once.

**Gate 3**:
```
$ python3 -m pytest @.remedy-wt/f200-r4/selection.txt -q -n auto -rs
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
4682 passed, 3 skipped in 35.22s
```
Exit 0. No failure, no error, no line containing "process(es) behind". The summary line
(`4682 passed, 3 skipped`) is exactly the block's stated reviewer dry-tree reading
(`4681 passed, 3 skipped` with one failure) plus the one failing test that C2's allowlist line
turned green — matching the block's done-when arithmetic exactly. Captured via the same
`subprocess.run` wrapper pattern so the command ran exactly once.

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

`.agent/authored/f200-r4.md` (commit `16a19967d`): saved as a byte-for-byte copy of the step block
given to this round; `wc -l` read 139 lines, `sha256sum` read
`1cc85b0cb80f92b3d67a7ded6e8c8d8e9c119dcba51c417a95881ed1621319d5`, matching both the delivering
prompt's stated digest/line count and `block.md`'s own digest; `cmp` against `block.md` printed
nothing.

`.agent/live_review.md` and `.agent/decisions.md` (commit `16a19967d`): the append-byte-equality
proofs (pre-commit blob at `bb22ee016` plus the respective append bytes equals the post-append
file) each read `True`.

`.agent/plan.md`, `.agent/operator_questions.md`, `docs/roadmap/features/T12_F200.md` (commit
`16a19967d`); `packages/orchestration/serve_runs.py`, `tests/orchestration/test_serve_runs.py`,
`apps/cli/serve_client.py`, `tests/orchestration/import_reachability_allowlist.txt` (commit
`412e9dc02`); `packages/orchestration/ui_server.py`, `packages/orchestration/serve_daemon.py`,
`tests/orchestration/test_serve_daemon.py`, `tests/cli/test_serve_client_parity.py` (commit
`de2e85a8d`): whole-file replace from their respective `dry-*` prepared files; `cmp` against each
prepared file printed nothing.

## Deviations & assumptions

None. The block's own digest (`1cc85b0cb80f92b3d67a7ded6e8c8d8e9c119dcba51c417a95881ed1621319d5`,
139 lines) and every prepared companion file's digest were verified with `sha256sum` before use and
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
4. Book round 4's verdict in the next round's first commit.
5. `remedy job run` in client mode, following the run's output to its end.

Operator questions open: 1.
Open findings: 5 (R-1117, R-1125, R-1127, R-1128, R-1129, all owned by F290).

## Item status

| Item | Status | Reason |
|---|---|---|
| Book round 3's verdict (PASS) in `.agent/live_review.md` | done | commit `16a19967d` |
| Record DECISION F200 D4 in `.agent/decisions.md` | done | commit `16a19967d` |
| Append the amendment paragraph to `docs/roadmap/features/T12_F200.md` | done | commit `16a19967d` |
| Update operator question Q4 to match DECISION F200 D4 | done | commit `16a19967d` |
| Advance `.agent/plan.md` | done | commit `16a19967d` |
| NEW FILE `.agent/authored/f200-r4.md` (copy of `block.md`) | done | commit `16a19967d` |
| NEW FILE `packages/orchestration/serve_runs.py` (the run launcher and registry) | done | commit `412e9dc02` |
| NEW FILE `tests/orchestration/test_serve_runs.py` | done | commit `412e9dc02` |
| `apps/cli/serve_client.py` takes `DIRECT_ENV` from `serve_runs` | done | commit `412e9dc02` |
| Allowlist line for `packages.orchestration.serve_runs` | done | commit `412e9dc02` |
| `_dispatch_extra_command` hook in `ui_server.py`'s `_handle_command_submission` | done | commit `de2e85a8d` |
| Socket handler class and launcher override for `job.run` in `serve_daemon.py` | done | commit `de2e85a8d` |
| Tests for the `job.run` socket path | done | commit `de2e85a8d` |
| Gates 1-5 before the handback | done | all matched the block's stated readings, each run exactly once |
| Rewrite `.agent/handoff.md` | done | this file |
| Push | done/reported in reply | `git push origin feature/f200-daemon-mode` — outcome in the session's own reply |
