# Handoff — F147 Golden-path CLI — CLOSED

Branch: `feature/f147-golden-path-cli`
Base: 9802799 (main)

## Source files changed
| File | Purpose |
|------|---------|
| apps/cli/command_catalog.py | GROUPS order pins do/status/decision first |
| apps/cli/commands/__init__.py | register status_cmd handlers |
| apps/cli/commands/do_cmd.py | bare-mission golden path (F147), truly_bare routing |
| apps/cli/commands/job_stop_cmd.py | _CoreJobAdapter fallback to storage.load_job |
| apps/cli/commands/status_cmd.py | status command: jobs, decisions, runtime, stops |
| apps/cli/grouped.py | _injected_default + _truly_bare injection markers |
| docs/roadmap/STATUS.md | F147 closed |
| docs/roadmap/features/T0_F147.md | feature spec + Built State section |
| packages/core/models.py | mission field on Job |
| tests/cli/test_golden_path.py | 29 tests across do/status/help/smoke |

## Findings: R-0085..R-0093 — all Resolved

## Evidence
- Job id: `f147-closure`
- Evidence dir: `remedy-job-evidence-f147/` (on disk, not committed)
- Tests: 29 passed, 0 failed
- Verdict: PASS_WITH_RISKS
- Package: `remedy-review-20260724-121604-READY_FOR_REVIEW.zip`
- SHA-256: `953410ab4c6aa0d4b639f96d797b7e66e93e36378338a6f9885e736d0e26ea17`

## Integrity check
```
$ python3 -m apps.cli.main integrity check --json
passed: true, check_count: 5, fail_count: 0
```

## RAW verification transcripts

### Step 3 — evidence bundle
```
$ python3 -c "from packages.orchestration.job_evidence import create_manual_completion_bundle; ..."
job_id: f147-closure
head_commit: 6869d82ffb68385d563f1c17d6f86c6590698ea9
authority_count: 10
partition: T001=4, T002=4, T003=2
verdict: PASS_WITH_RISKS
total_passed: 29
```

### Step 4 — integrity check
```
$ python3 -m apps.cli.main integrity check --json
exit 0
{"version":1,"passed":true,"fail_count":0,"check_count":5,
 "checks":[
   {"name":"handler_import","status":"pass","message":"handlers=304"},
   {"name":"live_review_verdict","status":"pass"},
   {"name":"plan_consistency","status":"pass","message":"unchecked=0"},
   {"name":"relevant_untracked","status":"pass","message":"untracked=0"},
   {"name":"high_blockers_open","status":"pass","message":"no open blocker/high findings"}
 ]}
```

### Step 6 — review zip
```
$ bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f147
PACKAGE_STATUS=READY_FOR_REVIEW
EVIDENCE_AUTHORITATIVE=true
REVIEW_SUBJECT_ALIGNMENT=PASS
ZIP_PATH=remedy-review-20260724-121604-READY_FOR_REVIEW.zip
SHA-256: 953410ab4c6aa0d4b639f96d797b7e66e93e36378338a6f9885e736d0e26ea17
member_count: 1448
```
