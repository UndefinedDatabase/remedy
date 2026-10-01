# Handoff — F200 Daemon mode (remedy serve), round 7

## Session

SESSION 2 of feature F200 · round 7

Context self-assessment: context remains workable after four commits and five gates this round.

Fortschritt: ~75 % (T001 and T002 built in their amended scope; the hardening stage and the
closure open) — Schätzung

## Range

Review of `13687cae5`..`HEAD`: four commits on `feature/f200-daemon-mode` and this handback
commit: `77a856328`, `8c69a1a6e`, `c7c059698`, `396576c3c`, and this commit.

## Commits

### `77a856328` F200 R7 C1: book round 6 (FAIL, the reviewer's selection), register R-1132 and R-1133, DECISION F200 D8 with the feature file's paragraph, save the round 7 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f200-r7.md` | +151/-0 | NEW FILE at `.agent/authored/f200-r7.md`; byte-for-byte copy of this round's step block, verified against `.remedy-wt/f200-r7/block.md` before commit (`wc -l` 151, sha256 `a1a14a1caa26e7ac7ad2d9e602013752f3c397840a4df1b49c8f3a5255f89203`) |
| `.agent/live_review.md` | +6/-0 | bytes of `.remedy-wt/f200-r7/append-live_review.txt` appended without retyping (books F200 round 6's Gate entry, VERDICT FAIL, and registers R-1132 and R-1133); pre-commit blob (`git show 13687cae5:.agent/live_review.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/decisions.md` | +10/-0 | bytes of `.remedy-wt/f200-r7/append-decisions.txt` appended without retyping (records DECISION F200 D8); pre-commit blob (`git show 13687cae5:.agent/decisions.md`) plus the append bytes verified byte-equal to the new file (`True`) |
| `.agent/plan.md` | +9/-8 | whole-file `cp` from `.remedy-wt/f200-r7/dry-plan.md`; `cmp` silent |
| `docs/roadmap/features/T12_F200.md` | +5/-0 | whole-file `cp` from `.remedy-wt/f200-r7/dry-T12_F200.md`; `cmp` silent; appends the `**Amended by DECISION F200 D8 (2026-10-01).**` paragraph |

`git diff --cached --numstat` before the commit read `6 0 .agent/live_review.md`,
`10 0 .agent/decisions.md`, `9 8 .agent/plan.md`, `5 0 docs/roadmap/features/T12_F200.md`, plus
`151 0 .agent/authored/f200-r7.md` — matching the block's stated numbers exactly. `git show
--numstat 77a856328` after the commit read the same five lines.

### `8c69a1a6e` F200 R7 C2: register REMEDY_SERVE_DIRECT in the environment registry (R-1132)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config.py` | +13/-0 | whole-file `cp` from `.remedy-wt/f200-r7/stage1-config.py`; `cmp` silent; registers `REMEDY_SERVE_DIRECT` as the env-only key `serve.force_direct` |
| `docs/guides/environment.md` | +1/-0 | whole-file `cp` from `.remedy-wt/f200-r7/stage1-environment.md`; `cmp` silent; the regenerated registry table's new row |
| `.agent/live_review.md` | +2/-0 | bytes of `.remedy-wt/f200-r7/append-landed.txt` appended without retyping (the `Landed: R-1132` line); pre-commit blob (`git show 77a856328:.agent/live_review.md`) plus the append bytes verified byte-equal to the new file (`True`) |

`git diff --cached --numstat` before the commit read `13 0 packages/orchestration/config.py`,
`1 0 docs/guides/environment.md`, `2 0 .agent/live_review.md` — matching the block's stated
numbers exactly. `git show --numstat 8c69a1a6e` after the commit read the same three lines.

### `c7c059698` F200 R7 C3: the systemd user unit and the container entrypoint, with their tests (DECISION F200 D8)

| Path | +/- | Reason |
|---|---|---|
| `scripts/serve/remedy-serve.service` | +42/-0 | NEW FILE at `scripts/serve/remedy-serve.service`; whole-file `cp` from `.remedy-wt/f200-r7/dry-remedy-serve.service`; `cmp` silent; a systemd user unit, `Type=simple`, `Restart=on-failure`, `KillMode=process` |
| `scripts/serve/container-entrypoint.sh` | +29/-0 | NEW FILE at `scripts/serve/container-entrypoint.sh`, committed executable (mode set with `os.chmod(path, 0o755)` before `git add`; `git ls-files -s` read `100755` after commit); whole-file `cp` from `.remedy-wt/f200-r7/dry-container-entrypoint.sh`; `cmp` silent; `exec`s the supervisor, requires `REMEDY_DATA_DIR` |
| `tests/orchestration/test_serve_artifacts.py` | +176/-0 | NEW FILE at `tests/orchestration/test_serve_artifacts.py`; whole-file `cp` from `.remedy-wt/f200-r7/dry-test_serve_artifacts.py`; `cmp` silent; parses the unit file and runs the entrypoint against a stub `remedy` executable |
| `packages/orchestration/config.py` | +11/-0 | whole-file `cp` from `.remedy-wt/f200-r7/dry-config.py`; `cmp` silent; registers `REMEDY_BIN` as the env-only key `serve.container_bin` |
| `docs/guides/environment.md` | +1/-0 | whole-file `cp` from `.remedy-wt/f200-r7/dry-environment.md`; `cmp` silent; the regenerated registry table's new row |

`git diff --cached --numstat` before the commit read `42 0` for the unit, `29 0` for the
entrypoint, `176 0` for the test, `11 0 packages/orchestration/config.py`,
`1 0 docs/guides/environment.md` — matching the block's stated numbers exactly. `git show
--numstat c7c059698` after the commit read the same five lines. `git diff --cached` was read in
full as self-review before the commit.

### `396576c3c` F200 R7 C4: the built-state page of the serve supervisor, registered in the docs index

| Path | +/- | Reason |
|---|---|---|
| `docs/system/serve-daemon-v1.md` | +191/-0 | NEW FILE at `docs/system/serve-daemon-v1.md`; whole-file `cp` from `.remedy-wt/f200-r7/dry-serve-daemon-v1.md`; `cmp` silent; the built-state page of the serve supervisor |
| `docs/README.md` | +2/-0 | whole-file `cp` from `.remedy-wt/f200-r7/dry-README.md`; `cmp` silent; registers the new page in both index tables |

`git diff --cached --numstat` before the commit read exactly `191 0` for the page and
`2 0 docs/README.md` — matching the block's stated numbers exactly. `git show --numstat
396576c3c` after the commit read the same two lines.

### this commit — F200 R7 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this file, per `docs/agents/handback_template.md`; this commit |

## External actions

`git push origin feature/f200-daemon-mode` runs after this commit; its outcome is reported in the
session's own reply, not in this file, because it occurs after this file is written and committed.
No pull request was opened — the block forbids it this round. No worktree was added or removed by
this session's own commands.

## Verification

Gates run once each, in order, strictly after C4 and before C5.

**Gate 1**:
```
$ git status --porcelain
(empty)
```
Then 10 `cmp` proofs, all silent, of every committed file against its prepared file under
`.remedy-wt/f200-r7/`: `.agent/authored/f200-r7.md`/`block.md`, `.agent/plan.md`/`dry-plan.md`,
`docs/roadmap/features/T12_F200.md`/`dry-T12_F200.md`,
`packages/orchestration/config.py`/`dry-config.py`, `docs/guides/environment.md`/`dry-environment.md`,
`scripts/serve/remedy-serve.service`/`dry-remedy-serve.service`,
`scripts/serve/container-entrypoint.sh`/`dry-container-entrypoint.sh`,
`tests/orchestration/test_serve_artifacts.py`/`dry-test_serve_artifacts.py`,
`docs/system/serve-daemon-v1.md`/`dry-serve-daemon-v1.md`, `docs/README.md`/`dry-README.md` — all
10 silent.
```
$ git ls-files -s scripts/serve/container-entrypoint.sh
100755 13fecdff38cd7eeb0160d2247cbb2ac8cd7820f3 0	scripts/serve/container-entrypoint.sh
```

**Gate 2**:
```
$ python3 -m ruff check packages/orchestration/config.py tests/orchestration/test_serve_artifacts.py
All checks passed!
```
Exit 0.
```
$ bash -n scripts/serve/container-entrypoint.sh
```
Exit 0, no output. Both captured via a `subprocess.run` wrapper script so each command ran
exactly once.

**Gate 3**:
```
$ python3 -m pytest @.remedy-wt/f200-r7/selection.txt -q -n auto -rs
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
SKIPPED [3] tests/orchestration/test_model_routing.py:455: covered by the violating fixture above
SKIPPED [1] tests/regression/test_f293_acceptance.py:191: main holds F293, so its own changes are history
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
8394 passed, 15 skipped, 1 warning in 99.43s (0:01:39)
```
Exit 0. No failure, no error, no line containing "process(es) behind". The summary line
(`8394 passed, 15 skipped`) is exactly the block's stated reviewer dry-tree reading (`8394
passed, 15 skipped`). Captured via the same `subprocess.run` wrapper pattern so the command ran
exactly once.

**Gate 4**:
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=174", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict FAIL", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0. `fail_count` 0.

**Gate 5**:
```
$ python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
['R-1117', 'R-1125', 'R-1127', 'R-1128', 'R-1129', 'R-1132', 'R-1133']
```
Exit 0. Matches exactly.

## Authored-text proofs

`.agent/authored/f200-r7.md` (commit `77a856328`): saved as a byte-for-byte copy of the step block
given to this round; `wc -l` read 151 lines, `sha256sum` read
`a1a14a1caa26e7ac7ad2d9e602013752f3c397840a4df1b49c8f3a5255f89203`, matching both the delivering
prompt's stated digest/line count and `block.md`'s own digest; `cmp` against `block.md` printed
nothing.

`.agent/live_review.md` and `.agent/decisions.md` (commit `77a856328`): the append-byte-equality
proofs (pre-commit blob at `13687cae5` plus the respective append bytes equals the post-append
file) each read `True`.

`.agent/live_review.md` (commit `8c69a1a6e`): the append-byte-equality proof (pre-commit blob at
`77a856328` plus `append-landed.txt`'s bytes equals the post-append file) read `True`.

`.agent/plan.md`, `docs/roadmap/features/T12_F200.md` (commit `77a856328`);
`packages/orchestration/config.py`, `docs/guides/environment.md` (commits `8c69a1a6e` and
`c7c059698`, the second stage over the first); `scripts/serve/remedy-serve.service`,
`scripts/serve/container-entrypoint.sh`, `tests/orchestration/test_serve_artifacts.py` (commit
`c7c059698`); `docs/system/serve-daemon-v1.md`, `docs/README.md` (commit `396576c3c`): whole-file
replace from their respective prepared files (`stage1-*` for C2, `dry-*` for C1/C3/C4); `cmp`
against each prepared file printed nothing.

## Deviations & assumptions

None. The block's own digest (`a1a14a1caa26e7ac7ad2d9e602013752f3c397840a4df1b49c8f3a5255f89203`,
151 lines) and every prepared companion file's digest were verified with `sha256sum` before use
and matched the block exactly, before any file was applied. All four code/record commits matched
the block's named paths and numstat exactly — no file outside the paths named per commit, no
extra hunk; `git diff --cached` was read as self-review before each commit. The entrypoint's mode
was set with `os.chmod(path, 0o755)` before `git add`, and `git ls-files -s` confirmed `100755`
after the commit. All five gates matched the block's stated done-when readings, run exactly once
each, after C4 and before C5. No mutation red-proof ran (amend0930-test-load rule 4, reserved to
the reviewer in a disposable worktree). No full suite ran and `REMEDY_TEST_MAX_WORKERS` was not
set; every test command passed `-n auto`, and only one test command ran at any time. No gate line
contained "process(es) behind". `.agent/STOP` did not appear at any point in this round. No
operator commit sits between this round's base and its first commit this time (unlike round 6).

## Next

1. Phase 1 rule 1 (`.agent/STOP`) — check first, in the next session.
2. Phase 1 rule 2 (the Open PR Gate).
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 7's verdict and R-1132's resolution in the next round's first commit.
5. The amend0930b-slow-cap hardening stage.

Operator questions open: 0.
Open findings: 7 (R-1117, R-1125, R-1127, R-1128, R-1129, R-1133 owned by F290; R-1132 owned by
F200, landed in this round).

## Item status

| Item | Status | Reason |
|---|---|---|
| Book round 6's verdict (FAIL) in `.agent/live_review.md` | done | commit `77a856328` |
| Register R-1132 and R-1133 in `.agent/live_review.md` | done | commit `77a856328` |
| Record DECISION F200 D8 in `.agent/decisions.md` | done | commit `77a856328` |
| Append the amendment paragraph to `docs/roadmap/features/T12_F200.md` | done | commit `77a856328` |
| Advance `.agent/plan.md` | done | commit `77a856328` |
| NEW FILE `.agent/authored/f200-r7.md` (copy of `block.md`) | done | commit `77a856328` |
| Register `REMEDY_SERVE_DIRECT` in `packages/orchestration/config.py` (R-1132 repair) | done | commit `8c69a1a6e` |
| Regenerate `docs/guides/environment.md` | done | commit `8c69a1a6e` (first stage), `c7c059698` (second stage) |
| Append the `Landed: R-1132` line | done | commit `8c69a1a6e` |
| NEW FILE `scripts/serve/remedy-serve.service` | done | commit `c7c059698` |
| NEW FILE `scripts/serve/container-entrypoint.sh`, mode `100755` | done | commit `c7c059698` |
| Register `REMEDY_BIN` in `packages/orchestration/config.py` | done | commit `c7c059698` |
| NEW FILE `tests/orchestration/test_serve_artifacts.py` | done | commit `c7c059698` |
| NEW FILE `docs/system/serve-daemon-v1.md` | done | commit `396576c3c` |
| Register the new page in `docs/README.md` | done | commit `396576c3c` |
| Gates 1-5 before the handback | done | all matched the block's stated readings, each run exactly once |
| Rewrite `.agent/handoff.md` | done | this file |
| Push | done/reported in reply | `git push origin feature/f200-daemon-mode` — outcome in the session's own reply |
