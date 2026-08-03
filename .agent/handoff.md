# Handoff — F071 Mission dossier · R2 (SPLIT, LARGE repair+continue)

## Range
Review of 097e4959..\<HEAD\> · feature/f071-mission-dossier · 16 commits.
LAST_REVIEWED_SHA stayed 097e4959 on the R1 FAIL, so R1's seven are re-tabled.

## Commits — paths: pkg=`packages/orchestration/`, t=`tests/orchestration/`

### R1 range (097e4959..a2e06afc) — unchanged since the R1 handback
| Commit | Paths | +/- |
|---|---|---|
| 4b5f940d claim + authored state | .agent state + docs/roadmap/STATUS.md | +160/-196 |
| 31684c88 T001 structure | pkg+t mission_dossier | +452 |
| 64306334 T001 budget+versioning | pkg/config + pkg+t mission_dossier | +307/-6 |
| c0124741 T002 compression | pkg+t mission_dossier | +435/-9 |
| fd989184 T002 update+flag | pkg+t mission_dossier | +167/-4 |
| dc809a21 R1 decisions+plan | .agent/decisions.md + plan.md | +72/-11 |
| a2e06afc handback R1 | .agent/handoff.md | +84/-42 |

### 06a37117 chore(f071): persist R1 verdict and findings (FAIL, R-0172..R-0174)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f071-r2-1.md | +75 | reviewer text, sha256-verified |
| .agent/live_review.md | +81/-19 | authored replacement |

### 90141a5d fix(f071): validate compression rules against the rebuilt dossier (R-0172)
| Path | +/- | Reason |
|---|---|---|
| pkg/mission_dossier.py | +95/-40 | `_check_rules` builds then judges; `_rebuild` moved above it |
| t/test_mission_dossier.py | +65/-1 | section-crossing refusals; dossier untouched |
| .agent/live_review.md | +1 | Done: R-0172 |

### e3575f71 fix(f071): refuse silent overwrite of a stored dossier version (R-0173)
| Path | +/- | Reason |
|---|---|---|
| pkg/mission_dossier.py | +18/-2 | identical rewrite = no-op; differing = ValueError |
| t/test_mission_dossier.py | +24 | both branches pinned, original bytes intact |
| .agent/live_review.md | +1 | Done: R-0173 |

### 55139dab docs(f071): IterationFacts docstring states merge-by-id semantics (R-0174)
| Path | +/- | Reason |
|---|---|---|
| pkg/mission_dossier.py | +12/-4 | docstring now matches `_merge_by_id` |
| t/test_mission_dossier.py | +9 | a restated decision replaces its line |
| .agent/live_review.md | +1 | Done: R-0174 |

### 2925abd6 feat(f071): live dossier state, iteration facts and refresh (T003)
| Path | +/- | Reason |
|---|---|---|
| pkg/mission_dossier.py | +192 | dossier_state.json, mission_iteration_facts, refresh_mission_dossier |
| t/test_mission_dossier.py | +150/-1 | state round-trip, facts from plan+ledger, one version/refresh |

### 544dffff feat(f071): wire the maintained dossier into the loop prefix seam (T003)
| Path | +/- | Reason |
|---|---|---|
| pkg/orchestrator_loop.py | +68/-20 | update_mission_dossier drives the maintained doc; maintained_dossier_text feeds the existing seam |
| t/test_orchestrator_loop.py | +111 | byte-prefix, one version per iteration, flagged doc still whole |

### 993c0fc9 feat(f071): seeded recall harness as a reusable deliverable (T003)
| Path | +/- | Reason |
|---|---|---|
| pkg/mission_dossier.py | +146 | RECALL_FIXTURE_FACTS, run_recall_harness, recall_report |
| t/test_mission_dossier.py | +106/-1 | open facts answerable, resolved may compress away |

### 0bdda1ed test(f071): negative control pins the recall harness missing set
| Path | +/- | Reason |
|---|---|---|
| t/test_mission_dossier.py | +17 | mutation M12 survivor -> control that kills it |

### 3ce0332d chore(f071): record R2 decisions and sync plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +48 | five R2 design decisions |
| .agent/plan.md | +39/-19 | current step -> R2 delivered |

### \<handoff sha\> chore(f071): handback R2 — self-reference (R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file |

## Item status
| Item | Status | Reason |
|---|---|---|
| R-0172 | done | 90141a5d — rule check judges the rebuilt document |
| R-0173 | done | e3575f71 — identical rewrite no-op, differing raises |
| R-0174 | done | 55139dab — docstring matches behavior |
| T003 loop integration | done | 2925abd6 + 544dffff (500-line rule) |
| T003 recall harness | done | 993c0fc9 + 0bdda1ed (negative control) |

## External actions
- `git worktree add --detach <scratch>/wt-f071-r2 HEAD` -> ok; `remove --force` -> ok; list = primary only.
- `git push` -> exit 0, a2e06afc..3ce0332d. No PR (closure creates it).

## Verification
R1 gate re-run BEFORE T003 started, per the order:
```
pytest t/test_mission_dossier.py -q        71 passed  EXIT=0
pytest tests/cli/test_golden_path.py -q    42 passed  EXIT=0
```
T003 gate at HEAD:
```
pytest t/test_mission_dossier.py -q        97 passed  EXIT=0
pytest t/test_orchestrator_loop.py -q     106 passed  EXIT=0
pytest tests/cli/test_golden_path.py -q    42 passed  EXIT=0
ruff check <the changed files>      All checks passed  EXIT=0
```
All 6 suites importing the changed modules + tests/docs/: `674 passed` EXIT=0.
Recall harness (fake provider): 5 iterations, version 6, 84 tokens, over
budget False, open answerable 5/5, open missing 0, compressed away 3.
Mutation red-proofs (disposable worktree at HEAD, each restored): rule check
back on the ANSWER 3F · version overwrite allowed 1F · decisions stop merging
1F · prefix falls back to stand-in 1F · refresh stops storing a version 6F ·
harness budget not tight 4F · **harness `missing` hard-coded empty SURVIVED**
-> fixed by 0bdda1ed, re-run 1F. Baseline 202 passed. Tree porcelain-clean.

## Authored-text proofs
`.agent/authored/f071-r2-1.md` sha256 `527a210a…` matches the BEGIN digest.
`cmp` authored vs applied live_review.md as committed in 06a37117: 0. The three
`Done: R-XXXX` lines were appended in the fixing commits, not at apply time.

## Deviations & assumptions
1. T003 split into TWO commits (helpers, then wiring) — 520 changed lines
   together. Helpers are green standalone.
2. The loop's compression provider is a SEPARATE opt-in seam (`call_fn=None`),
   so F070's one-call-per-iteration accounting is unchanged and the default
   path FLAGS over budget instead of compressing. decisions.md.
3. Live state is `dossier_state.json`; markdown versions stay a pure
   projection — parsing them back would make facts hostage to the renderer.
4. The recall harness is PUBLIC in `mission_dossier` (not test-local) so F079
   can reuse it. Published, NOT wired into F079 — handoffs stay untouched.
5. `DOSSIER_STANDIN_NOTE` reworded: the stand-in is now the no-stored-version
   fallback. `render_mission_dossier` is kept, reachable and tested.
6. One mutation SURVIVED; reported above rather than quietly re-run, and the
   control that kills it is its own commit.
7. Assumption: an "open decision" is not an open item (`open_items` excludes
   decisions by design) — the negative control documents that boundary.
8. R1's seven already-reviewed commits share ONE grouped table (the range
   reopened because R1 FAILed); each R2 commit has its own. ~1.77k tokens vs
   the 1.6k >10-commit cap, reported not hidden.

## Next
Reviewer verdict on R2. On PASS: R3 — the integration gate per
docs/agents/integration_gate.md.
