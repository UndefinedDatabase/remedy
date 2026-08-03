# Handoff — F071 Mission dossier · R3 (SPLIT, LARGE repair+gate)

## Range
Review of 097e4959..\<HEAD\> · feature/f071-mission-dossier · 21 commits.
LAST_REVIEWED_SHA stayed 097e4959 on the R2 FAIL: R1+R2 are re-tabled grouped
(accepted at R2), every R3 commit has its own table.

## Commits — paths: pkg=`packages/orchestration/`, t=`tests/orchestration/`

### R1 range 097e4959..a2e06afc — grouped, unchanged since the R1 handback
| Commit | Paths | +/- |
|---|---|---|
| 4b5f940d claim + authored state | .agent state + docs/roadmap/STATUS.md | +160/-196 |
| 31684c88 T001 structure | pkg+t mission_dossier | +452 |
| 64306334 T001 budget+versioning | pkg/config + pkg+t mission_dossier | +307/-6 |
| c0124741 T002 compression | pkg+t mission_dossier | +435/-9 |
| fd989184 T002 update+flag | pkg+t mission_dossier | +167/-4 |
| dc809a21 R1 decisions+plan | .agent/decisions.md + plan.md | +72/-11 |
| a2e06afc handback R1 | .agent/handoff.md | +84/-42 |

### R2 range a2e06afc..9698306e — grouped, unchanged since the R2 handback
| Commit | Paths | +/- |
|---|---|---|
| 06a37117 persist R1 verdict | .agent/authored/f071-r2-1 + live_review | +137/-19 |
| 90141a5d R-0172 fix | pkg+t mission_dossier + live_review | +121/-40 |
| e3575f71 R-0173 fix | pkg+t mission_dossier + live_review | +41/-2 |
| 55139dab R-0174 fix | pkg+t mission_dossier + live_review | +18/-4 |
| 2925abd6 T003 state/facts/refresh | pkg+t mission_dossier | +341/-1 |
| 544dffff T003 loop wiring | pkg+t orchestrator_loop | +159/-20 |
| 993c0fc9 T003 recall harness | pkg+t mission_dossier | +251/-1 |
| 0bdda1ed harness negative control | t mission_dossier | +17 |
| 3ce0332d R2 decisions+plan | .agent/decisions.md + plan.md | +68/-19 |
| 9698306e handback R2 | .agent/handoff.md | +101/-58 |

### cde1f07b chore(f071): persist R2 verdict and finding R-0175 (FAIL)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f071-r3-1.md | +87 | reviewer text, sha256-verified |
| .agent/live_review.md | +127/-59 | authored full replacement |

### c4068b85 fix(f071): reconcile the dossier version against the archive before writing (R-0175)
| Path | +/- | Reason |
|---|---|---|
| pkg/mission_dossier.py | +27/-4 | `refresh_mission_dossier` fast-forwards past `latest_dossier_version` before write |
| t/test_mission_dossier.py | +90 | `TestATornWriteHealsItself` — six tests |
| .agent/decisions.md | +30 | fast-forward as the explicit exception |
| .agent/live_review.md | +1 | Done: R-0175 |

### 8db010f0 chore(f071): integration gate evidence for R3
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f071_r3/ | +81 | 8 files: run tails, failed/comm lists, dist hashes, attribution |
| .agent/decisions.md | +19 | gate evidence written outside the repo during the run |

### 532dc6e8 chore(f071): sync plan after the R3 integration gate
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +19/-19 | current step -> R3 delivered, gate PASS |

### \<handoff sha\> chore(f071): handback R3 — self-reference (R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this file |

## Item status
| Item | Status | Reason |
|---|---|---|
| R-0175 | done | c4068b85 — reconcile before write; reproduced, fixed, pinned |
| gate-run | done | branch + base full suites, both exit 0, comm both EMPTY |
| gate-evidence | done | .agent/gate_f071_r3/, .txt names, attribution |

## External actions
- `git worktree add -b tmp/base-gate <scratch>/base-gate 097e4959` -> ok.
- `worktree remove --force` + `prune` + `branch -D tmp/base-gate` -> ok; `worktree list` = primary only, no `tmp/*`.
- `git push` -> exit 0, 9698306e..532dc6e8. No PR (closure creates it).

## Verification
R2 gate re-run BEFORE the integration gate:
```
pytest t/test_mission_dossier.py -q       103 passed  EXIT=0
pytest t/test_orchestrator_loop.py -q     106 passed  EXIT=0
pytest tests/cli/test_golden_path.py -q    42 passed  EXIT=0
```
**INTEGRATION GATE** (docs/agents/integration_gate.md):
```
branch c4068b85  pytest -n auto -q   15383 passed, 19 skipped  EXIT=0  149.72s
base   097e4959  pytest -n auto -q   15274 passed, 19 skipped  EXIT=0  165.58s
                 (REMEDY_UI_NO_AUTO_BUILD=1, throwaway branch worktree)
comm -13 (branch-only)  EMPTY      comm -23 (fixed by branch)  EMPTY
dist parity  5ff2033a…  before == after  UNCHANGED
```
+109 tests vs base — the F071 R1-R3 additions, all passing. Flake debt 0;
step-4 per-id attribution does not apply (no branch-only ids). Both runs under
the ~5 min threshold. `git status --porcelain` empty at handback.

R-0175 reproduced BEFORE the fix in a scratch root: stale state + one ledger
entry -> `ValueError: … dossier_v3.md already holds a different dossier
version 3`, same on every retry — permanently wedged. After the fix: version 4
then 5, `dossier_v3.md` byte-identical.

## Authored-text proofs
`.agent/authored/f071-r3-1.md` sha256 `8dcfb986…` matches the BEGIN digest.
`cmp` authored vs applied live_review.md as committed in cde1f07b: 0. The
`Done: R-0175` line was appended in the fixing commit, not at apply time.

## Deviations & assumptions
1. **Gate procedure hazard, reported not amended.** The FIRST branch run wrote
   its log inside the repo and reported 4 failures — 2 in
   `test_run_manifest_logical_identity`, 2 in
   `test_job_rerun_workspace_identity`, all comparing
   `remedy_worktree_digest`. The log was appended to WHILE the suite ran, so
   the digest genuinely changed mid-run: the tests were right, the harness was
   wrong. Re-run with evidence in the scratchpad, copied in afterwards: 15383
   passed, exit 0. `integration_gate.md` constrains evidence NAMES (.txt,
   R-0169) but not LOCATION during the run. Doc NOT amended — that call is the
   reviewer's. In attribution.txt + decisions.md to register or discard.
2. Version numbers become a monotonic high-water mark, not an update counter:
   a torn run consumes one number. Explicit exception to the R1
   one-update-one-version decision; the normal path is still pinned.
3. Gate run logs stored TRIMMED to exactly the records integration_gate.md
   asks for (header, FAILED list, raw tail, exit code, wall time) — 17 KB of
   progress dots each otherwise.
4. No closure work: no STATUS edit, no Built State, no evidence zip, no PR.

## Next
Reviewer verdict on R3 (gate verdict is the reviewer's alone). On PASS: R4 —
closure per docs/roadmap/STATUS_closure_protocol.md.
