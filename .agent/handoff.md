# Handoff — F147 Golden-path CLI — CLOSURE

Branch: `feature/f147-golden-path-cli`
Head: 366ff63 chore(f147): evidence bundle f147-closure
Base: 9802799 (main)

## Commits (20 total)
```
366ff63 chore(f147): evidence bundle f147-closure (29 passed, PASS_WITH_RISKS)
8403967 docs(f147): add Built State section to T0_F147.md; plan → CLOSURE
39cb674 chore(review): resolve R-0092..R-0093
adf25b5 chore(f147): handback repair round 2 with raw transcripts + manual probe
dd368dd fix(f147): R-0093 argv-level bare detection replaces value-equality guard
68064a7 fix(f147): R-0092 job stop finds golden-path jobs; smoke uses real CLI
5e85afb chore(review): persist R-0092..R-0093
ef43228 chore(f147): R-0091 handback with raw verification transcripts
c1d1378 fix(f147): R-0090 extend smoke test with stop leg
7b42514 fix(f147): R-0089 add "all projects" label and per-section next-command
16c0fbc fix(f147): R-0088 decisions_open uses real events, not empty list
0dcbc31 fix(f147): R-0087 stops_pending uses F011 kill-switch, not stop-reasons
b19b543 fix(f147): R-0086 corrupt runtime state → unknown + warning
df359a4 fix(f147): R-0085 bare-mission intercept only on truly bare invocations
a6f7fdb chore(review): persist R-0085..R-0091
805a7ef chore(f147): update handoff for T001-T003 completion
a99e220 feat(f147): T003 help pinning + golden-path smoke test
48899b9 feat(f147): T002 remedy status — project status overview
2e4a8c3 feat(f147): T001 remedy do mission — golden-path job creation
746455c chore(f147): claim feature, reset ledgers
```

## Source files changed
| File | Purpose |
|------|---------|
| apps/cli/command_catalog.py | GROUPS order pins do/status/decision first |
| apps/cli/commands/__init__.py | register status_cmd handlers |
| apps/cli/commands/do_cmd.py | bare-mission golden path (F147), truly_bare routing |
| apps/cli/commands/job_stop_cmd.py | _CoreJobAdapter fallback to storage.load_job |
| apps/cli/commands/status_cmd.py | status command: jobs, decisions, runtime, stops |
| apps/cli/grouped.py | _injected_default + _truly_bare injection markers |
| docs/roadmap/STATUS.md | feature status tracking |
| docs/roadmap/features/T0_F147.md | feature spec + Built State section |
| packages/core/models.py | mission field on Job |
| tests/cli/test_golden_path.py | 29 tests across do/status/help/smoke |

## Findings resolved: R-0085..R-0093 (9 findings, all Resolved)

## Evidence
- Job id: `f147-closure`
- Evidence dir: `remedy-job-evidence-f147/`
- Tests: 29 passed, 0 failed
- Verdict: PASS_WITH_RISKS

## Integrity check
```
$ python3 -m apps.cli.main integrity check --json
passed: true, check_count: 5, fail_count: 0
```

## RAW verification transcripts

### Golden-path tests (at 366ff63)
```
$ python3 -m pytest tests/cli/test_golden_path.py -v
29 passed in 9.58s
exit 0
```

### Evidence bundle
```
$ python3 -c "from packages.orchestration.job_evidence import create_manual_completion_bundle; ..."
job_id: f147-closure
head_commit: 8403967906d3e15aef126a3132c32fbf03436f06
authority_count: 10
partition: T001=4, T002=4, T003=2
verdict: PASS_WITH_RISKS
```

### Integrity check
```
$ python3 -m apps.cli.main integrity check --json
{
  "version": 1,
  "passed": true,
  "fail_count": 0,
  "check_count": 5,
  "checks": [
    {"name": "handler_import", "status": "pass", "message": "handlers=304"},
    {"name": "live_review_verdict", "status": "pass"},
    {"name": "plan_consistency", "status": "pass", "message": "unchecked=0"},
    {"name": "relevant_untracked", "status": "pass", "message": "untracked=0"},
    {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
  ]
}
```
