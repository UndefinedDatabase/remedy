# Handoff — F276 Data-root hygiene & disk budget · Round 2

## Session

SESSION 1 of feature F276 · round 2 · rounds so far 2

Context self-assessment: the worker read the step block and verified its sha256 before anything else, then AGENTS.md in full, `docs/agents/handback_template.md`, `docs/roadmap/features/T2_F276.md` and the `decisions.md` payload (DECISION F276 D3, which rules where the block is terser), and held all of it without loss; every numeral below is the output of a command run in this round, not a recollection.

## Range

Review of 96fd8f9c..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 2 books round 1's verdict and builds T002.
- C1 books round 1: the four reviewer payloads saved under `.agent/authored/`, round 1's PASS verdict and the measurement of the operator's data root appended to the review record, R-1001 recorded as resolved by the reviewer's own `Done:` paragraph, DECISION F276 D3 appended, the plan moved to T002.
- C2 gives the repository one spelling of "terminal": `JOB_TERMINAL_STATES` and `job_is_terminal` in `pingpong_job`, and `status_cmd`'s private `_TERMINAL` set routed through it.
- C3 lands DECISION F276 D3 in the registry — `workspaces`, `runs` and `job_logs` move to `DURABLE_CLASSES` — and adds `data_footprint.child_usage`.
- C4 builds `packages/orchestration/data_reclaim.py` and the `data.reclaim` handler, preview-first.
- C5 adds the catalog entry and the `--apply` flag test; C6 adds the behaviour tests and the docs.
- C7 is this handoff. No pull request was opened.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 the terminal-state vocabulary | done | |
| C3 the D3 registry moves and the footprint helper | done | |
| C4 the reclaim module and its importer | done | |
| C5 the catalog entry and the flag test | done | |
| C6 the behaviour tests and the docs | done | |
| C7 handoff | done | |
| G1 transport + state | done | 12 readings, every one True |
| G2 code transport | done | four object ids as ordered; twelve paths and no other |
| G3 targeted suite | done | `1243 passed in 195.70s`, exit 0, 0 failed |
| G4 ruff | done | `All checks passed!`, exit 0 |
| G5 mutation red-proofs | done | control green; all four mutations red; none stayed green |
| G6 push + clean tree | done | reported in the round report; it follows this commit |

No `Done:` or `Landed:` line is written by the worker this round. R-1001's resolution is the reviewer's own `Done: R-1001` paragraph, applied byte-exact inside the C1 ledger append; nothing else was resolved here.

## Commits

### 5d01c85a F276 R2 C1: book round 1 — the four reviewer payloads saved under .agent/authored, round 1's PASS verdict and the measurement of the operator's data root appended to the review record, R-1001 recorded as resolved, DECISION F276 D3 appended, and the plan moved to T002
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f276-r2-block.md` | +112 / -0 | Byte copy of the block |
| `.agent/authored/f276-r2-decisions.md` | +55 / -0 | Byte copy of decisions.md |
| `.agent/authored/f276-r2-ledger.md` | +6 / -0 | Byte copy of ledger.md |
| `.agent/authored/f276-r2-plan.md` | +31 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +55 / -0 | `96fd8f9c` bytes + decisions.md (DECISION F276 D3) |
| `.agent/live_review.md` | +6 / -0 | `96fd8f9c` bytes + ledger.md (the R1 PASS, the root measurement, `Done: R-1001`) |
| `.agent/plan.md` | +10 / -9 | := plan.md |

275 insertions, 9 deletions (`git show --numstat`).

### 16c2374b F276 R2 C2: the terminal-state vocabulary — JOB_TERMINAL_STATES and job_is_terminal declared beside the JOB_* constants in pingpong_job, naming completed, failed and cancelled and deliberately excluding blocked, stopped and paused because each keeps pending work a resume will want, and status_cmd's private _TERMINAL set routed through that one function
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/status_cmd.py` | +5 / -2 | The private `_TERMINAL` set replaced by `job_is_terminal(j.state)` |
| `packages/orchestration/pingpong_job.py` | +22 / -0 | `JOB_TERMINAL_STATES`, `job_is_terminal`, and the comment stating why the three non-terminal states are absent |

27 insertions, 2 deletions (`git show --numstat`).

### b6cfccc5 F276 R2 C3: DECISION F276 D3 in the registry — workspaces, runs and job_logs move to DURABLE_CLASSES, each entry naming the reader that keeps it and pointing retention at F166, review_staging declares that reclaim refuses it, and data_footprint gains child_usage so a reclaim candidate's bytes and its data usage bytes are the one number from the one function
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/data_footprint.py` | +19 / -0 | `child_usage(path) -> (bytes, files)`, following no symlink |
| `packages/orchestration/data_paths.py` | +40 / -7 | The three D3 moves with their readers; `review_staging`'s rule rewritten to the refusal reclaim performs |

59 insertions, 7 deletions (`git show --numstat`).

### 46f8947c F276 R2 C4: the reclaim module and its importer — data_reclaim plans and applies as two functions over one computed set, every decline a named refusal, only a direct child of an ephemeral class directory ever a candidate, a symlink or a path leaving the root refused, apply_reclaim re-checking every rule against the live filesystem so the plan is input and not authority, and the data_cmd handler previewing by default
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/data_cmd.py` | +79 / -1 | `_cmd_data_reclaim`, `_print_reclaim`, the `data.reclaim` handler entry |
| `packages/orchestration/data_reclaim.py` | +401 / -0 | `plan_reclaim`, `apply_reclaim`, `export_reclaim_json`, `REFUSAL_REASONS` and the four dataclasses |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -0 | `packages.orchestration.data_reclaim` |

481 insertions, 1 deletion (`git show --numstat`).

### a9c689d3 F276 R2 C5: the catalog entry and the flag test — data.reclaim declared local_state_change because --apply deletes Remedy's own scratch and never writes into a target repository, --apply declared is_flag so the parser does not demand a value for it, and a test that pins the flag parsing in both directions
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +18 / -0 | The `data.reclaim` `CommandEntry`, `--apply` as `is_flag`, `related=("data.usage",)` |
| `tests/cli/test_data_cmd.py` | +8 / -0 | `--apply` parses False when not typed and True when typed |

26 insertions, 0 deletions (`git show --numstat`).

### b8793d20 F276 R2 C6: the behaviour tests and the docs — every refusal reason pinned with a real persisted job record rather than a stub, one case per DECISION F276 D3 move so no single flip stays green, the delete_failed exit made real with an unwritable parent instead of a patched call, a symlinked candidate proved to leave its target alone, and architecture.md plus the feature file recording what reclaim addresses and what it refuses
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F276.md` | +30 / -0 | The DECISION F276 D3 amendment paragraph and its three readers |
| `docs/system/architecture.md` | +27 / -4 | The T001 class list corrected to two ephemeral classes; the new "Reclaiming the scratch (F276 T002)" paragraph |
| `tests/orchestration/test_data_reclaim.py` | +356 / -0 | Preview, apply, second apply, six non-terminal states, orphan, non-direct child, durable and unclassified children, the three D3 moves, both exit codes, the symlink, the JSON shape, the name-derived job id, a missing root |

413 insertions, 4 deletions (`git show --numstat`).

### C7 — this handoff commit
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | A handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f276-r2-wt b8793d20` — exit 0, for G5 only.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f276-r2-wt` — exit 0, as G5's last action; `git worktree list` then shows the primary checkout and the operator's `.remedy-wt/job-468c8e62a2cc4fac` alone, which is what it showed before the round.
- `git push origin feature/f276-data-root-hygiene` — after this commit; its result is in the round report.
- No pull request was created. Nothing was merged, forced, amended, branched or deleted. The operator's `.data/` was never read, listed or written.

## Verification

- G1 transport + state — `python3 -B .remedy-wt/f276-r2/g1_and_counts.py`, EXIT 0: `G1 READINGS: 12 all True: True`. All four payload digests matched the block (`block.md` `d6509059…`, `ledger.md` `4fe2f516…`, `decisions.md` `8a6310a4…`, `plan.md` `8857ce54…`); each `.agent/authored/f276-r2-*` copy equals its payload (four `True`); `live_review.md == 96fd8f9c bytes + ledger.md: True`; `decisions.md == 96fd8f9c bytes + decisions.md: True`; `plan.md == plan.md payload: True`. The saved block, both readings: scratch `block.md` 112 lines / sha256 `d6509059b116c229ba3bb1b6a9cc4d60e8f4e6d9e9192790685780e2777720aa`, and the committed `.agent/authored/f276-r2-block.md` 112 lines / the same sha256.
- G2 code transport — `git rev-parse b8793d20:packages b8793d20:apps b8793d20:tests b8793d20:docs` printed `e92f2ef2352b2f551ad8975ac88ffb9b587f1c7c`, `49e01420b6d44b6aca9043159e9cb968d43c63e4`, `c087f446bb98a4515891bfc464632bba74997856`, `09b32267e9f49a7d3497bbb8147eb2316a64c407` — exactly the four objects the block names, exit 0. `git diff --name-only 5d01c85a b8793d20` named 12 paths and no other: `apps/cli/command_catalog.py`, `apps/cli/commands/data_cmd.py`, `apps/cli/commands/status_cmd.py`, `docs/roadmap/features/T2_F276.md`, `docs/system/architecture.md`, `packages/orchestration/data_footprint.py`, `packages/orchestration/data_paths.py`, `packages/orchestration/data_reclaim.py`, `packages/orchestration/pingpong_job.py`, `tests/cli/test_data_cmd.py`, `tests/orchestration/import_reachability_allowlist.txt`, `tests/orchestration/test_data_reclaim.py`. That is exactly the union of the five `--include` lists of C2 to C6.
- G3 targeted suite — `python3 -m pytest -q -p no:cacheprovider` over the block's twenty-three ordered paths, serial, no `-n`, in the primary checkout at `b8793d20`: `1243 passed in 195.70s (0:03:15)`, EXIT 0, 0 failed. (Run through a wrapper that prints `G3 AT HEAD <sha>` and a wall-clock stamp, the tail of which read `END 2026-09-20T02:46:16.271132`, because two earlier runs of the same list had each reported an identical `195.68s` and that coincidence was worth ruling out; this third run read `195.70s`.)
- G4 ruff — `python3 -m ruff check` over the block's nine ordered paths: `All checks passed!`, EXIT 0.
- G5 mutation red-proofs — ONE disposable worktree, `/home/decodeux/Repos/remedy/.remedy-wt/f276-r2-wt` at `b8793d20`. Import probe first, from the worktree root: `packages.orchestration.data_reclaim` resolved to `…/.remedy-wt/f276-r2-wt/packages/orchestration/data_reclaim.py` and `data_paths` to `…/f276-r2-wt/packages/orchestration/data_paths.py`, both inside the worktree, EXIT 0 — no editable install shadowed it. Every run is `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_data_reclaim.py tests/cli/test_data_cmd.py` with `cwd` the worktree root, `__pycache__` purged first (0 dirs each time: the worktree is fresh and `-B` writes none). CONTROL, unmutated: `28 passed in 1.05s`, EXIT 0.
  - (a) `return True` inserted as the first statement of `pingpong_job.job_is_terminal` — site count 1 — EXIT 1, `8 failed, 20 passed`: `test_a_non_terminal_job_workspace_is_refused_and_named[blocked|paused|pending|planned|running|stopped]`, `test_apply_deletes_exactly_the_previewed_paths`, `test_ordinary_refusals_exit_zero`.
  - (b) `    for cand in plan.candidates:` in `data_reclaim.apply_reclaim` — site count 1 — replaced by a loop building a candidate for every direct child of every ephemeral class directory, so the plan is ignored: EXIT 1, `10 failed, 18 passed`: the six `test_a_non_terminal_job_workspace_is_refused_and_named` cases, `test_a_path_that_is_not_a_direct_child_is_refused`, `test_a_staging_copy_whose_job_has_no_record_is_refused_not_skipped`, `test_a_symlinked_candidate_is_refused_and_its_target_survives`, `test_apply_deletes_exactly_the_previewed_paths`.
  - (c) `    outcome = apply_reclaim(plan) if apply_it else None` in `apps/cli/commands/data_cmd.py` — site count 1 — replaced by `    outcome = apply_reclaim(plan)`, so the dry run deletes: EXIT 1, `3 failed, 25 passed`: `test_preview_deletes_nothing`, `test_apply_deletes_exactly_the_previewed_paths`, `test_the_json_shape`.
  - (d) DECISION D3 undone for `runs` — its `DataRootClass` entry removed from `DURABLE_CLASSES` (site count 1) and re-added to `EPHEMERAL_CLASSES` (site count 1), with `"runs": ""` added to `data_reclaim._JOB_KEYED_PREFIXES` (site count 1): EXIT 1, `2 failed, 26 passed`: `test_a_terminal_jobs_durable_child_survives_an_apply[runs]`, `test_job_workspaces_is_the_only_class_with_candidates`.
  - No mutation stayed green. After each, all four files were rewritten from the bytes read before the first mutation and each was shown byte-identical by sha256 (`REVERTED byte-identically: True`, four times). The worktree's `git status --porcelain` was then empty, and `git worktree remove` was the step's last action.
- G6 push and clean tree — reported in the round report only, since this handoff commit precedes the push.

## Open findings

14 open BY DISTINCT ID and 14 by the canonical line formula (`scripts/rotate_live_review.py::count_open_findings`), both measured on the committed ledger at `b8793d20`: 18 distinct ids match `^- R-\d{4} — ` against 4 matching `^Done: R-\d{4}\b`. An independently written distinct-id reading produced the same set (`independent open set == canonical open set: True`). The open set: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829, R-0866, R-0880, R-0892, R-0950, R-0984, R-0998, R-0999, R-1000 — F273's carried set, owned by F282 under the OWNERSHIP AT CLOSE paragraph. R-1001 left the open set this round, closed by the reviewer's `Done:` paragraph in the C1 ledger append; one round ago the count was 15.

## Authored-text proofs

All four reviewer-authored payloads were copied byte-for-byte with `shutil.copyfile`, never retyped. Disk-to-disk comparison against the committed `.agent/authored/f276-r2-*` copies: `block.md`, `ledger.md`, `decisions.md` and `plan.md` each equal their payload — four `True` readings under G1 — and each payload's sha256 matched the digest the block states, checked twice (once before the copy, once at G1). The code carrier `.remedy-wt/f276-r2/f276-r2.diff` matched sha256 `bf3a73bfa2d27e7a087ef2d8c11ea0518c8032e78d9e90e653692d36eb49d7d2` and was applied with `git apply --include=` in five disjoint slices, never applied whole, never retyped and never edited; G2's four tree object ids are the transport proof that the committed trees are byte-identical to the reviewer's own dry-run trees.

## Deviations & assumptions

- None to the block's ordered commit sequence: C1, C2, C3, C4, C5, C6 and C7 were committed in that order — no extra commit, none dropped, none reordered.
- Block constraint 7 ("each of C2 to C6 is green on its own") was read as an obligation to measure, so the G3 path list was run before each of C2, C3, C4 and C5 as well, filtered to the paths that existed at that commit — `tests/orchestration/test_data_reclaim.py` only exists from C6. Readings, all EXIT 0: C2 `1220 passed in 211.55s`, C3 `1220 passed in 195.28s`, C4 `1220 passed in 194.79s`, C5 `1221 passed in 195.44s` (the new `--apply` flag test), C6 `1243 passed`. Nothing was committed while a gate was red.
- Not a deviation, a reading worth recording: C4 lands the `data.reclaim` HANDLER before C5 lands its catalog entry, and C5 lands the catalog entry before C6 lands the naming test. That order is what DECISION F276 D3 (7) describes and both bracketing guards — `tests/cli/test_advertised_commands.py` and `tests/orchestration/test_dead_command_check.py` — were green at every one of those commits.
- Arithmetic re-checked rather than copied: DECISION F276 D3 says `job_workspaces` is 99.93 per cent and the code comment in `data_paths.py` says 99.98 per cent. They are different denominators and both are right — 922931683643 / 923560682122 = 0.99932 of the data root's bytes, and 922931683643 / 923133615493 = 0.99978 of the four classes T001 had called ephemeral. No contradiction.
- The 500-insertion cap holds for every commit under `git show --numstat`: 275, 27, 59, 481, 26, 413. No oversize commit was declared, and the allowance DECISION F276 D3 (7) declines to spend was not spent.
- An extra probe, beyond the ordered gates: `tests/orchestration/test_pingpong_job_dod_gate.py` was run after C2 (`4 passed`, EXIT 0), because C2 changes `pingpong_job` and the G3 list names no pingpong suite. The repository has no `tests/**/test_status_cmd.py`, so `status_cmd`'s change is covered by the G3 list's CLI suites alone.
- Operator questions open: 5 (`### Q` headings in `.agent/operator_questions.md`).

## Next

Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` first — re-read `.agent/STOP` from disk, and if the sentinel exists write the handoff and end the session, doing nothing else. (It did not exist when this round ran.) Then the review of round 2: the reviewer re-runs G1 to G6 and reads `96fd8f9c..HEAD` bottom-up before any verdict. Then T003 — the copy-mode lifecycle: `release_staging_workspace(job_id)` on the same terminal-state hook the worktree cleanup uses, a `.gitignore`-aware copy filter and a hard per-file size ceiling, with the release call's removal as the red proof.
