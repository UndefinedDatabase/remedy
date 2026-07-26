# Handoff — F016 Scaling task granularity — CLOSED

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

## Item-Status Table
| Item | Status | Reason |
|------|--------|--------|
| STEP A verdicts persisted | done | byte-identical to the ordered text |
| STEP B Built State + plan | done | |
| STEP C git status + push | done | clean, pushed |
| STEP C integrity check | done | PASS, 5/5 checks |
| STEP D evidence job | done | 3rd attempt; two producer pitfalls, below |
| STEP E review zip | done | 2nd attempt; first was BLOCKED_EVIDENCE |
| STEP F STATUS + commit + PR | done | |

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
0 open. R-0141 Resolved; R-0142 documented Low (gap backlog).

## Next expected action
Next feature start runs the Open PR Gate, which merges PR #150.
