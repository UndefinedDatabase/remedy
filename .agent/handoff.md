# Handback — F075 R12 (SPLIT, LARGE)

## Range
Review of 05a15669..f45b1358 (6 commits + this handoff commit).

## Commits
### 4b171dc0 chore(f075): save the R12 block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +198/-285 | the block verbatim, own commit per R-0198 |

### ba266dab chore(f075): restore a blank line dropped from the R12 block in transport
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +1 | archived block corrected to the authored bytes |

### 8d01fb32 chore(f075): persist the R11 PASS -- 10/10 stands; register R-0198/R-0199
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f075-r12-{1,2,3}.md | +95/+38/+39 | reviewer texts, sha256-verified |
| .agent/live_review.md · plan.md · context.md | +196/+60/+50 (-175 tot.) | full replacements from r12-1/2/3 |

### 449d64dd docs(f075): prepare ADR-0001 -- raise the cycle safety cap, not applied
| Path | +/- | Reason |
|---|---|---|
| docs/adr/0001-raise-cycle-safety-cap.md | +152 | the ADR, status PROPOSED |
| docs/adr/0001-raise-cycle-safety-cap.diff | +22 | ready-to-apply diff, NOT applied |
| docs/README.md | +13 | new `docs/adr/` category + quick-find row |
| .agent/decisions.md | +41 | location decision, the 8 reasoning, the evidence limit |

### dcde0698 test(f075): pin the cycle safety cap at 1 until ADR-0001 is applied
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_long_run_executor.py | +10 | pin `test_the_rollout_cap_is_still_one_until_adr_0001_is_applied` |

### f45b1358 chore(f075): record the R12 integration gate evidence
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f075_r12/ | +158 | 11 files: raw tails, both comm lists, per-id attribution, dist hashes, hygiene |

### <this commit> chore(f075): handback R12
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md · .agent/last_block.md | rewrite / +1 | this handback (R-0149) · OUTCOME line |

## External actions
- 6x `git push -u origin feature/f075-self-run-gauntlet`, one per commit — OK. NO force-push (R-0195).
- `git worktree add -b tmp/base-gate-r12 <scratchpad>/base-gate 563b15b4` — OK; then `remove --force` + `prune` + `git branch -D` → `Deleted branch tmp/base-gate-r12 (was 563b15b4)`, `git worktree list` = primary only.
- No PR, no gh command, nothing merged.

## Verification
```
$ pytest tests/cli/test_golden_path.py -q     42 passed 15.32s   EXIT=0  (P1 gate)
$ pytest tests/orchestration/test_long_run_executor.py -q  74 passed  EXIT=0  (P2)
$ pytest tests/docs/ -q                       293 passed         EXIT=0  (P2)
$ grep -n '^CYCLE_SAFETY_CAP' packages/orchestration/long_run_executor.py
  165:CYCLE_SAFETY_CAP = 1        <- diff is a FILE; the change is NOT applied
$ git apply --check docs/adr/0001-raise-cycle-safety-cap.diff   APPLIES CLEANLY  EXIT=0
$ pytest -n auto -q       BRANCH dcde0698  15805 passed, 19 skipped, 183.39s   EXIT=0
$ REMEDY_UI_NO_AUTO_BUILD=1 pytest -n auto -q  BASE 563b15b4  6 failed, 15377 passed, 19 skipped, 147.95s  EXIT=1
$ comm -13 base_failed branch_failed   (empty)  <- branch-only
$ comm -23 base_failed branch_failed   6x tests/ui_server/test_live_state.py::TestUIServerIntegration::*
$ REMEDY_UI_NO_AUTO_BUILD=1 pytest ...::TestUIServerIntegration -q  serial, base worktree  16 passed  EXIT=0
$ pytest tests/cli/test_golden_path.py -q     42 passed 15.67s   EXIT=0  (canary)
$ git status --porcelain   (empty)
```
GATE RESULT: branch exit 0, **0 branch-only failures**, 0 unattributed comm -23 ids.
The six base-only ids are R-0169 recurring — the suite rebuilt the UI mid-run despite
`REMEDY_UI_NO_AUTO_BUILD=1`, racing the UI server. Per id: same stderr `ERROR: React UI
not built.`; dist CONTENT hash identical before/after (5ff2033a…, F071 R3's digest) yet
base `dist/index.html` mtime 13:25:23 and `.vite/deps` 13:23:06 sit INSIDE the base run;
staleness ruled out (dist newer than every `apps/ui/src` file); all six pass serially in
the same worktree; no F075 commit touches apps/ui or ui_server. Per-id evidence:
`.agent/gate_f075_r12/attribution.txt`.

## Authored-text proofs
| text | sha256 vs BEGIN digest | applied |
|---|---|---|
| f075-r12-1 | acc6fcfb…8be4 EQUAL | `cmp` 0 vs .agent/live_review.md |
| f075-r12-2 | 11349415…1696 EQUAL | `cmp` 0 vs .agent/plan.md |
| f075-r12-3 | 5747f126…eee6 EQUAL | `cmp` 0 vs .agent/context.md |

DECLARED, transport: r12-2 as received hashed b55c4de1…. Cause isolated to ONE dropped
blank line before `## Risks`; restoring it reproduced 11349415… exactly. r12-1/r12-3
hashed correct on first extraction, which makes the one-line diagnosis safe, not a guess.
Nothing was applied until all three matched; the archived block was fixed too (ba266dab).

## Deviations & assumptions
- ADR location: repo had NO ADR convention (no `docs/adr/`, no `*adr*` file, no index
  section). Chose `docs/adr/`, precedent `docs/agents/` + `docs/ui/`; alternatives and
  rejections in `.agent/decisions.md`.
- ADR number 8: per-run cycle CONSUMPTION is unrecoverable — it lived in each run's
  `gauntlet_run.json` under the campaign root outside the repo (R-0176), since reclaimed.
  The ADR argues from the proven CEILING (budgets 3–8, ten `achieved`) and says so openly
  instead of inventing a measured-max-plus-margin figure. `DEFAULT_MAX_CYCLES` stays 1.
- Extra commit ba266dab, not in the block: the transport fix above. The mid-run UI
  rebuild deserves its own order — offered as a closure candidate, not filed (your call).

## Next
Window 1 reviews R12 and issues the gate verdict; then R13, closure per `STATUS_closure_protocol.md`.
