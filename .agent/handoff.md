# Handback — F078 round 9: the evidence round (evidence job exited 1, package not built)

## Session

SESSION 2 of feature F078 · round 9 · rounds so far 9

Context self-assessment: this worker copied prepared files, ran the helpers and wrote text, and the context was far from exhausted.

Fortschritt: ~90 % (T001 to T003 landed, suite green on the repaired tree; the evidence job read `is_valid_current_run False`, so no package was built and the evidence round must be repeated after the cause is settled) — Schätzung

## Range

Review of `86e853759`..`HEAD` on `feature/f078-autonomy-levels-2` (base: round 8's handback commit `86e853759`).

## Commits

### 27efa169d F078 R9 C1: book round 8, resolve R-1392 and R-1393, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f078-r9.md` | +113/-0 | new: the block of this round |
| `.agent/live_review.md` | appended | round 8 booked, R-1392 and R-1393 resolved |
| `.agent/plan.md` | rewritten | the plan |

### 2b5cc0c18 F078 R9 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f078-r9-create_f078_evidence.py` | +438/-0 | new: the evidence script |

### (this commit) F078 R9 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this handback |

## External actions

- `git push -u origin feature/f078-autonomy-levels-2` after C2: `86e853759..2b5cc0c18`, no retry needed.
- The push after this commit: result in the worker's final reply.
- No provider call, no pull request opened or created.

## Verification

1. Preconditions: `git rev-parse --short=9 HEAD` `86e853759`, equal to the remote branch tip; `git status --porcelain` empty; `.agent/STOP` absent. All prepared digests matched.
2. Gate 1 after C2: `git status --porcelain` empty; `verify.py .`: every line `True`, C3 `absent`, last line `ALL True`.
3. Gate 2: A2 exited 1 (see below); A3 skipped by the block's rule.
4. Gate 3: `python3 -m apps.cli.main integrity check --json`: exit 1, `fail_count` 1, the one failing check `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`. `open_finding_ids` count: `87`. `git status --porcelain` empty.

## Staging reclaim

A1 preview (`data reclaim --orphans`): `Reclaimable: nothing`, `Would free 0 B in 0 paths`, no refused path; only durable classes listed as not reclaimed. The apply was skipped because the preview listed no candidate.

## Evidence and package

Evidence job id `f078r9e1001`. Reflog before: `2b5cc0c18 HEAD@{2026-10-21 07:00:11 +0200}: commit: F078 R9 C2: the evidence script`, `27efa169d ... C1`, `86e853759 ... R8 C5`. A2: `launch.py evidence` then `wait.py evidence 50`: `exit 1 wall 1452.9`. Lines:

```
head 2b5cc0c18b61cac3e45384e617d951eca2f90907
ancestry-path count 24
first-parent count 24
collected node ids 10048, deselected 177
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 10042, 'failed': 0, 'skipped': 6}, output_hash ebeb9219fb862e3833ec61a9f77260ee596f6e2b6621a2285d90e2b200e10191
validate_verification_tests problems [] passed 10042
is_valid_current_run False
validation_errors ["the review subject claims committed changes no packaged commit made: ['apps/cli/commands/mission_cmd.py', 'apps/cli/commands/status_cmd.py', 'docs/guides/environment.md', 'docs/roadmap/STATUS.md', 'docs/system/mission-run-loop-morning-report-v0.md', 'docs/system/structure-ledger-v1.md', 'packages/orchestration/config.py', 'packages/orchestration/config_keys_autonomy.py', 'packages/orchestration/data_paths.py', 'packages/orchestration/orchestrator_dispatch.py', 'tests/cli/test_status_cmd.py', 'tests/orchestration/import_reachability_allowlist.txt', 'tests/orchestration/test_autonomy_seams.py', 'tests/test_structure_ratchet.py']"]
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
"job_id": "f078r9e1001", "head_commit": "2b5cc0c18b61cac3e45384e617d951eca2f90907", "authority_count": 33,
"commit_count": 24, "verdict": "PASS_WITH_RISKS", "manual_completion": true, "total_passed": 10042
```

Everything matched the expectations (head, equal counts, 10048 and 177, red control 0, pytest exit 0 with 0 failed, no problems) except `is_valid_current_run False` with one validation error, which made the script exit 1. The error lists fourteen paths that the review subject claims as committed changes while no packaged commit touched them. A3 was skipped as the block orders: no package was built, so no package name, SHA-256, directory or accepted head exists.

## Authored-text proofs

C1, C2: each prepared file is a byte copy, proven by a Python equality over bytes at copy time (all True) and again by `verify.py` (all `True`). All prepared digests were checked before use and every one matched.

## Deviations & assumptions

A2 exited non-zero, so A3 was skipped and this handback was written as the block orders for that case. The helpers were run through a small wrapper script that sets the repository root as the working directory. Assumption: the validation error comes from the packaged commit range (24 commits) not containing the fourteen paths' changes, which the review subject's base appears to reach beyond; the cause is not diagnosed here.

## For the operator, in plain sentences

The evidence of this feature was collected and mostly checked: the tests it covers all passed and the safety scan found nothing. One final consistency check failed, because the review subject lists some changed files that the collected commits do not include. For that reason the review package was not built.

## Next

1. Phase 1 rule 1: `.agent/STOP`.
2. Phase 1 rule 2: the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 9, settles the cause of the failed validation (the review subject's base against the packaged commit range), and books its verdict in the next round's first commit.
4. A repeat of the evidence job and the review package, then the closing round: the rotation or its recorded skip, SU-069's consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

Operator questions open: 2.
Open findings: 87 (rule: `scripts.rotate_live_review.open_finding_ids` over `.agent/live_review.md`, gate 3).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `27efa169d` |
| C2 | done | `2b5cc0c18` |
| A1 | done | nothing reclaimable, apply skipped |
| A2 | deviated | exit 1, `is_valid_current_run False` |
| A3 | skipped | A2 exited non-zero |
| C3 | done | this commit |
| Gate 1 | done | ALL True |
| Gate 2 | deviated | A2 exit 1, A3 skipped |
| Gate 3 | done | fail_count 1, the twelve findings; 87 open |
