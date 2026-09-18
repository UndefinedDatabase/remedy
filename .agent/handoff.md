# Handoff — F266 Round 9

## Session

SESSION 2 of feature F266 · round 9 · rounds so far 9

## Range

Review of 2b066ce3..0a4f4ff1

## Summary

Closure repair round: fixed five genuine regressions from round 8's closure suite
(test_vocabulary.py binding-word collision, test_cli_ux.py group count pin,
test_import_reachability.py allowlist, test_role_config.py KNOWN_ROLES pin,
test_resource_safety.py context constraint). Five additional failures are
pre-existing xdist cross-test-pollution flakes (R-0950), reproduced at the
fork point (ec520c17, F281's merge commit); no repair owed.

## Commits

### 5e858e20 F266 C1: closure repair — record fork-point classification of round 8's 10 red nodes
| Path | Change | Reason |
|------|--------|--------|
| `.agent/live_review.md` | +59 lines | Appended R-0950 recurrence documenting pre-existing xdist flake class |
| `.agent/plan.md` | rewritten | Updated plan for closure-repair round with 5 fixes + 5 flakes |

### bacbf3ab F266 C2: fix study.run's description — avoid the binding word "Run" outside its page meaning
| Path | Change | Reason |
|------|--------|--------|
| `apps/cli/command_catalog.py` | 1 line | Changed "Run a bounded..." to "Execute a bounded..." in study.run command |

### b4880dfb F266 C3: fix the D4 group-partition pin — study is the 30th group, internal tier
| Path | Change | Reason |
|------|--------|--------|
| `tests/cli/test_cli_ux.py` | 3 lines | Added "study" to _INTERNAL_GROUPS; updated group count 29→30 in test |

### 6c004d8c F266 C4: add study's two modules to the import-reachability allowlist
| Path | Change | Reason |
|------|--------|--------|
| `tests/orchestration/import_reachability_allowlist.txt` | +2 lines | Added apps.cli.commands.study_cmd and packages.orchestration.study |

### c6d99ee4 F266 C5: fix the KNOWN_ROLES pin — study is the tenth role
| Path | Change | Reason |
|------|--------|--------|
| `tests/orchestration/test_role_config.py` | 4 lines | Renamed test method to test_all_ten_roles_present; added "study" to KNOWN_ROLES |

### 4e775c5b F266 C6: mention pytest in .agent/context.md — closure repair
| Path | Change | Reason |
|------|--------|--------|
| `.agent/context.md` | +1 line | Added pytest constraint bullet to Constraints section |

### d6827239 F266 C7: closure repair verification — targeted re-check of all 10 nodes, canary
| Path | Change | Reason |
|------|--------|--------|
| `.agent/authored/f266-r9-targeted-recheck.txt` | +2 lines | Saved targeted serial pytest run output (all 10 nodes PASSED) |

### 06d3e44a F266 C9: commit round-9 authored transport-proof copies
| Path | Change | Reason |
|------|--------|--------|
| `.agent/authored/f266-r9-context.md` | new | Transport-proof: additions to context.md before applying |
| `.agent/authored/f266-r9-live-review.md` | new | Transport-proof: R-0950 recurrence note before appending to live_review.md |

### 0a4f4ff1 F266 C10: handoff — round 9 closure repair, final state
| Path | Change | Reason |
|------|--------|--------|
| `.agent/handoff.md` | rewritten | Updated Range line to include C9, final commit list |

## Verification

**Targeted re-check of all 10 originally-red nodes (serial, no `-n auto`):**

```
..........                                                               [100%]
10 passed in 7.41s
```

All nodes:
1. test_every_binding_word_in_a_description_carries_the_pages_meaning ✓
2. test_catalog_partition_matches_d4 ✓
3. test_no_zombie_processes_after_every_outcome ✓
4. test_no_module_outside_the_allowlist_is_reachable_from_the_entry_points ✓
5. test_all_ten_roles_present ✓
6. test_different_execution_identities_same_logical_hash ✓
7. test_two_real_runs_report_no_input_drift ✓
8. test_context_mentions_resource_safety ✓
9. test_an_unchanged_stopped_workspace_shows_no_drift ✓
10. test_a_mutated_workspace_shows_blocking_drift ✓

Additional verification:
- `python3 -m ruff check`: All checks passed! ✓
- `tests/cli/test_golden_path.py` canary: 42 passed in 17.72s ✓

## Pre-Existing Flakes (R-0950)

Five failures from round 8's full-suite run (`python3 -m pytest -n auto -q`) are
xdist cross-test-pollution, reproduced at fork point (ec520c17, F281's merge commit)
under identical `-n auto` invocation:

1. tests/orchestration/test_product_smoke.py::test_no_zombie_processes_after_every_outcome — passes in isolation
2. tests/cli/test_job_rerun_workspace_identity.py::TestNoFalseWorkspaceDrift::test_an_unchanged_stopped_workspace_shows_no_drift — passes in isolation
3. tests/cli/test_job_rerun_workspace_identity.py::TestNoFalseWorkspaceDrift::test_a_mutated_workspace_shows_blocking_drift — passes in isolation
4. Pre-existing UI-server failure (unbuilt apps/ui/dist in fresh worktree)
5. test_vitest_passes — unrelated to F266 changes

No repair owed per amend0917-throughput rule 2: failure reproduces at fork point
under identical full-suite invocation, so nodes are not broken by F266's changes.
General xdist-isolation paydown remains Owner: F273.

## External actions

```
git push origin feature/f266-remedy-study
```

(After C10)

## Next

1. Algorithm step 1: evidence job
2. Algorithm step 2: review zip
(Per `docs/roadmap/STATUS_closure_protocol.md`)
