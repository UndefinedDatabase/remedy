# Handoff — F280 CLI vocabulary v2, part two
SESSION 5 of feature F280 · round 11 · rounds so far 11

This round booked round 10's independently-reviewed PASS (Gate: F280 R10, one prose slip noted, no new finding) and authored DECISION F280 D6, naming the persisted-literal spellings the second half of DECISION F280 D5's rename needs: `flight_plan` (job-record key/attribute) becomes `task_plan`, `FLIGHT_PLAN_SCHEMA_V`/`"flight_plan_v1"` become `TASK_PLAN_SCHEMA_V`/`"task_plan_v1"`, `_MAX_FLIGHT_PLAN_TASKS` becomes `_MAX_TASK_PLAN_TASKS`, `"flight_plan_approval"` becomes `"task_plan_approval"` — with NO migration shim per DECISION D-A. This round is DECISION-ONLY; no code under `apps/`, `packages/`, `tests/`, or `scripts/` changed.

## Range
Review of `2bf73ac7`..`a1b1f7e2` (commits C0a through C1).

## Commits

### 2488894b C0a: F280 R11 C0a: write authored block f280-r11.md (transport carrier)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f280-r11.md` | 89/0 | Block carrier |

### 9c884ba7 C0b: F280 R11 C0b: mirror authored block to last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 89/158 | Block carrier mirror |

### a1b1f7e2 C1: F280 R11 C1: append Gate:F280 R10 + prose slip, append DECISION F280 D6, insert T2_F280 amendment, replace plan.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 2/0 | Append blank line + Gate:F280 R10 entry (4583 bytes) |
| `.agent/prose_slips.md` | 2/0 | Append blank line + prose slip R10 line (412 bytes) |
| `.agent/decisions.md` | 19/0 | Append blank line + DECISION F280 D6 (6464 bytes) |
| `docs/roadmap/features/T2_F280.md` | 11/0 | Insert D6 amendment after D5, before T002 heading (895 bytes) |
| `.agent/plan.md` | 32/15 | Replace with R11 plan (44 lines) |

Total: 5 files, 51 insertions(+), 15 deletions(-)

## External actions
Push to remote after handoff complete.

## Verification

G1 TRANSPORT: PASS
- `.agent/authored/f280-r11.md` sha256 = `6734a30f94da2f6b568225305b2521f214763fff54c9ff5b2326b66257118c08` ✓
- `.agent/last_block.md` sha256 = `6734a30f94da2f6b568225305b2521f214763fff54c9ff5b2326b66257118c08` ✓
- `.remedy-wt/gate_r10_entry.txt` (4583 bytes) matches end of .agent/live_review.md ✓
- `.remedy-wt/prose_slip_r10.txt` (412 bytes) matches end of .agent/prose_slips.md ✓
- `.remedy-wt/decision_f280_d6.txt` (6464 bytes) matches end of .agent/decisions.md ✓
- `.remedy-wt/t2_f280_amendment.txt` (895 bytes) found in docs/roadmap/features/T2_F280.md ✓
- `.remedy-wt/f280-r11-plan.md` (2534 bytes) matches .agent/plan.md ✓
- Exit code: 0

G2 THE RECORD (after C1): PASS
- `.agent/live_review.md`: 37 gates, 136 distinct R-ids open, 7 Done ids ✓
- `.agent/decisions.md`: 6 DECISION F280 D entries ✓
- `.agent/prose_slips.md`: 1025 lines (1023 base + 2 new lines for append) ✓
- `.agent/plan.md`: 44 lines, 1 Goal, 1 Current Step, 1 Next Steps, 1 Risks ✓
- Exit code: 0

G3 THE SPLICE (after C1): PASS
- `git diff --numstat HEAD~1..HEAD -- docs/`: exactly one file changed ✓
- `docs/roadmap/features/T2_F280.md`: 11 insertions, 0 deletions ✓
- New paragraph lands between D5's amendment (operator-facing heir.) and T002 heading ✓
- Every other line of T2_F280.md unchanged ✓
- Exit code: 0

G4 THE BOUNDARY (after C1): PASS
- `git diff --stat HEAD~1..HEAD` shows exactly 5 files changed ✓
- Files: .agent/decisions.md, .agent/live_review.md, .agent/plan.md, .agent/prose_slips.md, docs/roadmap/features/T2_F280.md ✓
- No changes under apps/, packages/, tests/, scripts/ ✓
- Exit code: 0

G5 DOCS SUITE (after C1): PASS
- `python3 -m pytest tests/docs/ -q`: 310 passed ✓
- Exit code: 0

## Deviations
None. All gates matched exactly.

## Next Steps
1. A future round executes DECISION F280 D6: the mechanical persisted-literal rename (`flight_plan` → `task_plan`, etc.), using the same boundary method as round 10 (zero-count sweep for old spellings; `.data/evidence_exports/` closure bundles and accepted history files untouched).
2. D5's third owed item: surviving English-prose noun "flight plan" (catalog descriptions, CLI print statements, comments) — its own round after step 1 lands.
3. The `"fp:"` decision-id prefix — explicitly out of scope for D6 (CHOSEN, SECOND of D6) — gets its own DECISION once measurement is done.
4. Continue with T001 workflow: `propose` deletion (blocked on operator question Q4), `job attach-repo` and `job permit` (blocked on a DECISION providing a writer).
