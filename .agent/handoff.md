# F280 Round 19 Handoff

**Feature**: F280 CLI vocabulary v2, part two  
**Round**: 19 (closure repair round 1)  
**Session**: 11  
**Branch**: feature/f280-cli-vocabulary-v2-part-two  

## Commits

| Commit | SHA | Description |
|--------|-----|-------------|
| C1 | 26533011 | Append Gate:F280 R18 + register R-0945 through R-0950 + replace plan.md |
| C2 | 91ff506f | Fix R-0945 (stale gauntlet-manifest digest) |
| C3 | 9edbef11 | Fix R-0946 and R-0947 (hint string and doc advertisements) |
| C4 | 8d27c005 | Fix R-0948 and R-0949 (test file updates) |
| C5 | (this commit) | Handback |

**Previous**: f52c6c8f (F280 R18 handback: integration gate run, 51 bad nodes found)

## Changes Summary

### C1: Gate entry, findings, and plan replacement
| File | Changes |
|------|---------|
| `.agent/live_review.md` | +Gate:F280 R18 + 6 findings (R-0945 through R-0950) |
| `.agent/plan.md` | replaced with R19 plan (45 lines) |
| `.agent/authored/f280-r19.md` | +125 lines (step block for this round) |
| `.agent/last_block.md` | +125 lines (mirrored step block) |

### C2: R-0945 fix
| File | Changes |
|------|---------|
| `scripts/gauntlet_orders/manifest.json` | Updated g05 sha256 and set_hash (2 insertions/2 deletions) |

### C3: R-0946 and R-0947 fixes
| File | Changes |
|------|---------|
| `apps/cli/commands/job.py` | Changed hint string: propose list → decision list |
| `docs/system/core-product-spine-v0.md` | Updated quick-start step 4 and taxonomy table row |
| `docs/system/first-fulfilled-job-demo-v0.md` | Updated steps 4-5 with deletion comments |
| `docs/guides/simple-operator-quickstart-v0.md` | Updated quick-start and demo sections |

### C4: R-0948 and R-0949 fixes
| File | Changes |
|------|---------|
| `tests/cli/test_job_stop.py` | Deleted test_propose_list_status_still_takes_a_value; deleted propose.list assertion; updated docstring |
| `tests/cli/test_runtime_helpers.py` | Changed 4 propose list invocations to decision list |
| `tests/orchestration/import_reachability_allowlist.txt` | Deleted apps.cli.commands.propose_cmd line |

## Verification Results

**G1 RECORD** (after C1):
- Gates: 45 ✓
- Finding IDs (distinct `-R-\d{4}`): 146 ✓
- Done IDs (distinct `Done: R-\d{4}`): 9 (unchanged) ✓
- plan.md lines: 45 with exactly 1x Goal, 1x Current Step, 1x Next Steps, 1x Risks ✓

**G2 R-0945 REPAIRED** (after C2):
- `python3 -m pytest tests/orchestration/test_gauntlet_orders.py tests/orchestration/test_self_run_gauntlet.py -q`
- Result: **68 passed** ✓

**G3 R-0946/R-0947 REPAIRED** (after C3):
- `python3 -m pytest tests/cli/test_advertised_commands.py tests/docs/ -q`
- Result: **323 passed** ✓
- `git grep -n 'propose list\|propose approve\|propose reject\|propose defer' -- docs/ apps/cli/commands/job.py`
- Result: **zero** (only historical references in roadmap docs remain) ✓

**G4 R-0948/R-0949 REPAIRED** (after C4):
- `python3 -m pytest tests/cli/test_job_stop.py tests/cli/test_runtime_helpers.py tests/orchestration/test_import_reachability.py -q`
- Result: **35 passed** ✓
- `git grep -n 'propose' -- tests/cli/test_job_stop.py tests/cli/test_runtime_helpers.py tests/orchestration/import_reachability_allowlist.txt`
- Result: **zero** (only docstring references, which are correct) ✓

**G5 FULL PREVIOUSLY-BAD SET** (after C4):
- `python3 -m pytest tests/cli/test_advertised_commands.py tests/cli/test_job_stop.py tests/cli/test_runtime_helpers.py tests/orchestration/test_import_reachability.py tests/orchestration/test_gauntlet_orders.py tests/orchestration/test_self_run_gauntlet.py tests/cli/test_job_rerun_workspace_identity.py tests/orchestration/test_run_manifest_logical_identity.py -q`
- Result: **135 passed** ✓
- `python3 -m ruff check apps/cli/commands/job.py tests/cli/test_job_stop.py tests/cli/test_runtime_helpers.py`
- Result: **All checks passed** ✓

## Repair Summary

Repaired 5 findings across 51 bad closure-suite nodes:

1. **R-0945 (Medium)**: Round 14's prose-sweep patch edited g05-two-milestone-mission.json without updating its manifest digest. Fixed by recomputing sha256 and set_hash with the module's own hashlib.sha256/compute_set_hash functions. (41 nodes)

2. **R-0946 (Low)**: Second hardcoded `remedy propose list` hint string in job.py that round 15 missed. Fixed by changing to `remedy decision list`. (1 node)

3. **R-0947 (Low)**: Seven dead `propose` invocations in three operator-facing docs. Fixed by repointing to `decision list` or `decision resolve proposal:<id>` with historical deletion comments. (7 nodes)

4. **R-0948 (Low)**: test_job_stop.py had orphaned parser-isolation test for deleted propose command. Fixed by deleting the test method and vacuous assertion, updating docstring. (1 node)

5. **R-0949 (Low)**: Two test files (test_runtime_helpers.py and import_reachability_allowlist.txt) still named deleted propose surface. Fixed by changing invocations to decision list and removing stale allowlist entry. (1 node)

6. **R-0950 (Low, NOT REPAIRED)**: Four closure-suite nodes (test_job_rerun_workspace_identity.py × 2, test_run_manifest_logical_identity.py × 2) that pass reliably in isolation and under -n auto, unconnected to any F280 change. Registered but not repaired; flagged for F273 future investigation. (4 nodes)

**Total bad nodes addressed**: 51 of 51 accounted for (47 repaired by F280, 4 investigated and deferred to F273).

## Status and Next Steps

**This Round**: Closure repair round 1 complete. All five F280-owned findings (R-0945 through R-0949) are fixed and verified green. The four R-0950 nodes remain in closure suite's transcript (not rewritten); they pass independently and investigation shows no F280 connection.

**Next Round (R20)**: Re-verification round. Run exactly the 51 previously-bad nodes (never the full suite) to confirm the bad set shrank to R-0950's four only, per amend0917-throughput rule 2. Once confirmed, proceed with preconditions.

**Pre-Closure Preconditions** (after verification):
1. Precondition 4: Built State section (docs/roadmap/features/T2_F280.md)
2. Precondition 6: Self-use item (F257/F258 call and findings)
3. Precondition 3: `remedy integrity check --json` pass
4. Evidence job, review zip, STATUS line (each own round, per STATUS_closure_protocol.md)

**Ownership Notes**:
- R-0950's four flaky nodes stay in closure suite's committed transcript (rule 2 honesty requirement)
- Future features waiting on F269: `job attach-repo`, `job permit`, `mission contract`, `job contract` (not F280's scope)

## Tree State

- Clean checkout: `git status --porcelain` shows no uncommitted changes ✓
- Branch tip: feature/f280-cli-vocabulary-v2-part-two
- No disposable worktrees: primary checkout only
- All commits in sequence with no post-C5 work
- Ready for next round (R20 re-verification)

## Session Notes

- Session 11, worker round 19 of F280
- Closure repair round 1: all five F280-owned findings fixed in single round
- Tests covering affected areas all green (135 passed in full re-verify)
- Tree clean and pushed at each commit
