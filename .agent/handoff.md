# F280 Round 21 Handback

## Session

SESSION 13 of feature F280 · round 21 · rounds so far 21

Round 21 books round 20's independently-reviewed PASS and discharges closure precondition 6 by generating and running the self-use item SU-016 under the configured real provider without applying it.

## Range

Review of c570aeac..bac1e61a

## Commits

### 681ebd60 F280 R21 C1: book Gate:F280 R20 PASS, append record and prose slip, replace plan

| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f280-r21.md | 211/0 | Transport C0a copy |
| .agent/last_block.md | 211/40 | Transport C0b copy (rewrite) |
| .agent/live_review.md | 2/0 | Append RECORD21 (2356 bytes) |
| .agent/prose_slips.md | 2/0 | Append PROSESLIP21 (631 bytes) |
| .agent/plan.md | 16/15 | Replace with PLAN21 (2086 bytes) |

### bac1e61a F280 R21 C2: generate and run self-use item SU-016, record evidence

| Path | +/- | Reason |
|------|-----|--------|
| scripts/self_use_queue.json | 8/0 | SU-016 appended (58833 bytes total) |
| .agent/selfuse_f280/ | 23/0 | 6 U3 evidence files (entry_and_job, result_state, execution_config, timing, run_defects, full_transcript) |

## External actions

```
git push origin feature/f280-cli-vocabulary-v2-part-two (after C1)
  To github.com:UndefinedDatabase/remedy.git
  c570aeac..681ebd60  feature/f280-cli-vocabulary-v2-part-two -> feature/f280-cli-vocabulary-v2-part-two
  exit code: 0

git push origin feature/f280-cli-vocabulary-v2-part-two (after C2)
  To github.com:UndefinedDatabase/remedy.git
  681ebd60..bac1e61a  feature/f280-cli-vocabulary-v2-part-two -> feature/f280-cli-vocabulary-v2-part-two
  exit code: 0
```

## Verification

### G1 TRANSPORT

**Command:** Verify `.agent/authored/f280-r21.md` and `.agent/last_block.md` sha256

**Output:**
```
.agent/authored/f280-r21.md:
  Expected sha256: cc6474ec2d9574173200e0f2c365c4a51f66157bf7ab6b42121cb40ff686f14a
  Actual sha256:   cc6474ec2d9574173200e0f2c365c4a51f66157bf7ab6b42121cb40ff686f14a
  Match: True

.agent/last_block.md:
  Byte-identical to authored: True

Slices verified:
  RECORD21: sha256 match True
  PROSESLIP21: sha256 match True
  PLAN21: sha256 match True
```

**Exit code:** 0

**Result:** PASS

### G2 THE RECORD

**Output:**
```
.agent/live_review.md: 748709 bytes (expected 748709) ✓
.agent/prose_slips.md: 314271 bytes (expected 314271) ✓
.agent/plan.md: 2093 bytes, 40 lines (expected 40) ✓

Gate count: 47 (expected 47) ✓
Open R-ids: 146 distinct (expected 146) ✓
Done R-ids: 14 distinct (expected 14) ✓

Sections:
  ## Goal ✓
  ## Current Step ✓
  ## Next Steps ✓
  ## Risks ✓
```

**Exit code:** 0

**Result:** PASS

### G3 THE GENERATION

**Output:**
```
Before U1:
  Pending items: empty
  Next item: None

Generated:
  ID: SU-016
  Title: Address ledger finding R-0445
  Provenance: generated (self-use-generator tier 1, ledger scan, R-0445)
  Consumed by: (empty)

Queue stats:
  Before: 53814 bytes, 15 items
  After:  58833 bytes, 16 items

Pending after: SU-016 alone
```

**Exit code:** 0

**Result:** PASS

### G4 THE RUN

**Output:**
```
Worktree: .remedy-wt/f280r21w/su_worktree at 681ebd60 on tmp/f280-r21-selfuse
Destination: .remedy-wt/f280r21w/su_run

Call: run_next_self_use_item(
  dest_dir=/home/decodeux/Repos/remedy/.remedy-wt/f280r21w/su_run
  repo_path=/home/decodeux/Repos/remedy/.remedy-wt/f280r21w/su_worktree
  queue_path=scripts/self_use_queue.json
)

Job result:
  job_id: c87bd5b5eb894a96
  state: blocked
  task_T001: blocked

ExecutionConfig:
  builder: ollama
  builder_source: cli
  reviewer: ollama
  reviewer_source: cli
  (fake NOT in config) ✓

Budgets:
  max_provider_calls: 6
  max_cost_usd: 0.5

Defects: 2
  - job c87bd5b5eb894a96 (blocked): task_T001_gate_failed
  - T001 (blocked): completion_gate_failed

Duration: 67.8 seconds
Start: 2026-09-17 14:58:10
End:   2026-09-17 14:59:17

Cleanup:
  Worktree removed ✓
  Pruned ✓
  tmp/f280-r21-selfuse deleted ✓

Primary checkout unchanged (git status --porcelain empty) ✓
New remedy/job branch: remedy/job-c87bd5b5eb894a96 preserved ✓
```

**Exit code:** 0

**Result:** PASS

### G5 TREE, PATH SET, CANARY

**Output:**
```
git status --porcelain:
  (empty) ✓

git worktree list:
  /home/decodeux/Repos/remedy  bac1e61a [feature/f280-cli-vocabulary-v2-part-two]
  (1 row) ✓

HEAD == origin/feature/f280-cli-vocabulary-v2-part-two: True ✓

Changed paths (c570aeac..bac1e61a):
  .agent/authored/f280-r21.md
  .agent/last_block.md
  .agent/live_review.md
  .agent/plan.md
  .agent/prose_slips.md
  .agent/selfuse_f280/entry_and_job_file.txt
  .agent/selfuse_f280/execution_config.txt
  .agent/selfuse_f280/full_transcript.txt
  .agent/selfuse_f280/result_state.txt
  .agent/selfuse_f280/run_defects.txt
  .agent/selfuse_f280/timing.txt
  scripts/self_use_queue.json

Commit insertions:
  681ebd60 (C1): 242 insertions (under 500 limit) ✓
  bac1e61a (C2): 28 insertions (under 500 limit) ✓
```

**Exit code:** 0

**Result:** PASS

## Authored-text proofs

None applied — the block's slices (RECORD21, PROSESLIP21, PLAN21) were transported as delivered and verified by sha256.

## Deviations & assumptions

None. Round followed block specifications exactly.

## Open findings

132 open by distinct id (unchanged). High: R-0803, R-0804, R-0807 — none F280's. The self-use run's defect tuple (2 items: job and task blocking at approval gate) is a PROCESS outcome, not a new finding; registration is round 22 C1 work.

## Next steps

1. Phase 1 rule 1 (STOP check before next round's C1)
2. Book round 21 verdict PASS plus register self-use-run defect tuple (round 22 C1)
3. Precondition 3: `remedy integrity check --json` confirmed PASS
