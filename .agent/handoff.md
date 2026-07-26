# Handoff — F016 Scaling task granularity — CLOSED (form repair, R-0143)

Review of 2fad892..HEAD

## State
- Branch: `feature/f016-task-granularity` · PR #150 (NOT merged — Open PR
  Gate handles it at the next feature start)
- Verdict: PASS_WITH_RISKS — ACCEPTED (2026-07-26, closure round)
- Evidence job: `1cc3b1c0-fd59-4884-9252-f8a8e79b5a59`
- Evidence dir: `.data/evidence_exports/1cc3b1c0-fd59-4884-9252-f8a8e79b5a59`
- Zip: `remedy-review-20260726-165629-READY_FOR_REVIEW.zip`
- Zip SHA-256: `0a147595147fa300d0b6b7257e626394b365d689e3af540c536a0c477fb5a991`
- accepted HEAD: `85004253705e5eae15d969812af84738373e5453`
- LAST_REVIEWED_SHA: `2fad89295e11bc2aad51f7ae5f7de52b7542e9b5`
- This round: handback FORM repair only. No code, no STATUS, no zip
  rebuild — the package and STATUS line are accepted as-is.

## Item-Status Table
| Item | Status | Reason |
|------|--------|--------|
| R-0143 persisted verbatim | done | |
| Per-commit changed-files tables | done | every commit in dcb8b1a..HEAD |
| Raw grep proofs | done | |
| Review-range line | done | |

## Per-commit changed files — dcb8b1a..HEAD

### 88911bd — chore(f016): claim F016, reset live review and plan for task granularity
| File | +/- |
|------|-----|
| .agent/live_review.md | 177 (6/173) |
| .agent/plan.md | 36 (19/17) |
| docs/roadmap/STATUS.md | 2 (1/1) |

3 files changed, 25 insertions(+), 190 deletions(-)

### 8b5360c — feat(f016): pure task-granularity split heuristic and planning config keys
| File | +/- |
|------|-----|
| packages/orchestration/config.py | 41 (+) |
| packages/orchestration/task_granularity.py | 298 (+, new) |

2 files changed, 339 insertions(+)

### 6513fca — test(f016): table-driven split cases for task granularity
| File | +/- |
|------|-----|
| .agent/plan.md | 10 (5/5) |
| tests/orchestration/test_config.py | 29 (+) |
| tests/orchestration/test_task_granularity.py | 209 (+, new) |

3 files changed, 243 insertions(+), 5 deletions(-)

### fc2e219 — feat(f016): merge rule for runs of trivial neighboring tasks
| File | +/- |
|------|-----|
| .agent/decisions.md | 28 (+) |
| .agent/plan.md | 10 (5/5) |
| packages/orchestration/task_granularity.py | 207 (202/5) |
| tests/orchestration/test_task_granularity.py | 169 (+) |

4 files changed, 404 insertions(+), 10 deletions(-)

### 51e2575 — feat(f016): revalidate, wire normalization into plan generation
| File | +/- |
|------|-----|
| .agent/plan.md | 18 (9/9) |
| apps/cli/commands/do_cmd.py | 7 (6/1) |
| docs/system/remedy-toml-configuration-system-v0.md | 16 (+) |
| packages/orchestration/flight_plan.py | 85 (79/6) |
| packages/orchestration/task_granularity.py | 19 (17/2) |
| tests/cli/test_plan_approval.py | 46 (43/3) |
| tests/orchestration/test_flight_plan.py | 93 (+) |
| tests/orchestration/test_task_granularity.py | 99 (+) |

8 files changed, 363 insertions(+), 20 deletions(-)

### cd13645 — chore(f016): handback state for round 1
| File | +/- |
|------|-----|
| .agent/handoff.md | 164 (52/112) |

1 file changed, 52 insertions(+), 112 deletions(-)

### c534d82 — chore(f016): persist round 1 reviewer verdict; open integration gate
| File | +/- |
|------|-----|
| .agent/live_review.md | 15 (13/2) |
| .agent/plan.md | 8 (5/3) |

2 files changed, 18 insertions(+), 5 deletions(-)

### 2fad892 — chore(f016): integration gate measurements and handback
| File | +/- |
|------|-----|
| .agent/handoff.md | 102 (49/53) |
| .agent/plan.md | 13 (9/4) |

2 files changed, 58 insertions(+), 57 deletions(-)

### f27f9a9 — chore(f016): persist integration-gate and final reviewer verdicts
| File | +/- |
|------|-----|
| .agent/live_review.md | 30 (+) |

1 file changed, 30 insertions(+)

### 8500425 — docs(f016): built state in the feature file; plan set to closure
| File | +/- |
|------|-----|
| .agent/plan.md | 25 (13/12) |
| docs/roadmap/features/T1_F016.md | 53 (+) |

2 files changed, 66 insertions(+), 12 deletions(-)

### ecbe72f — chore(f016): close F016 — evidence job, review package, STATUS line
| File | +/- |
|------|-----|
| .agent/handoff.md | 105 (55/50) |
| docs/roadmap/STATUS.md | 2 (1/1) |
| remedy-review-20260726-165629-READY_FOR_REVIEW.zip | Bin 0 → 8225339 |
| .data/evidence_exports/1cc3b1c0-fd59-4884-9252-f8a8e79b5a59/ | 68 files under that dir (gates, review_subject, review_commit_chain + 10 commit patches, token_truth, verification_tests, tasks.json, workspace.diff, task_runs/T001–T003/*) |

71 files changed, 7505 insertions(+), 50 deletions(-)

### 2db44f9 — chore(f016): persist R-0143 handback form finding
| File | +/- |
|------|-----|
| .agent/live_review.md | 11 (+) |

1 file changed, 11 insertions(+)

## Raw grep proofs
```
$ grep -c "accepted HEAD 85004253705e5eae15d969812af84738373e5453" docs/roadmap/STATUS.md
1
$ grep -c "R-0143" .agent/live_review.md
1
$ sha256sum remedy-review-20260726-165629-READY_FOR_REVIEW.zip
0a147595147fa300d0b6b7257e626394b365d689e3af540c536a0c477fb5a991  remedy-review-20260726-165629-READY_FOR_REVIEW.zip
```

## Artifact-build attempts (all, including failures)
1. Evidence bundle #1 (`ef3acc17-…`) → zip
   `remedy-review-20260726-165436-BLOCKED_EVIDENCE.zip`
   (sha256 74467b95…). BLOCKED: `verification_tests.json runs[0..5] has
   the wrong field set` — the producer stamps schema_version 1.1.0, and
   the validator demands that exact 14-field set; 10 fields were supplied.
   Bundle and zip deleted.
2. Evidence bundle #2 (`ac14f641-…`), full field set. Still invalid:
   `output_hash does not match sha256(stdout_summary)` — the hash must
   cover the summary line, not the full captured stdout. Deleted; no zip
   was built.
3. Evidence bundle #3 (`1cc3b1c0-…`) — `validate_manual_completion: []`,
   `is_valid_current_run: True`. Zip → PACKAGE_STATUS=READY_FOR_REVIEW.

Both pitfalls are exactly the class the closure protocol §1 warns about;
neither is an F016 code defect.

## Verification recorded in the bundle (230 passed, all exit 0)
| run | command | result |
|-----|---------|--------|
| vr-0001 | pytest tests/orchestration/test_task_granularity.py -q | 26 passed |
| vr-0002 | pytest tests/orchestration/test_flight_plan.py -q | 29 passed |
| vr-0003 | pytest tests/orchestration/test_config.py -q | 62 passed |
| vr-0004 | pytest tests/cli/test_plan_approval.py -q | 27 passed |
| vr-0005 | pytest tests/orchestration/schemas/test_schemas.py -q | 44 passed |
| vr-0006 | pytest tests/cli/test_golden_path.py -q | 42 passed |

Integration gate (earlier round): base dcb8b1a 181 failed · branch
162/158 across two runs · ~3 min each with `-n auto` · no F016-attributable
regression.

## Open findings
0 open. R-0141 Resolved; R-0142 documented Low (gap backlog);
R-0143 Resolved by this handoff rewrite.

## Next expected action
Next feature start runs the Open PR Gate, which merges PR #150.
