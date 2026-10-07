# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order; T001 to T003 have landed.

## Current Step
Round 12, the closure sequence's integration-gate round (docs/agents/integration_gate.md,
amend0917-throughput rule 1): book round 11, whose self-use run reported no defect; run the
feature's one full suite on the tree that ships and its cost script, and commit the transcript
`.agent/authored/f287-closure-suite.txt`.

## Next Steps
1. A green suite: the checklist's consolidation pass, then the evidence job and the review
   package. A red one: repair rounds that strictly shrink the bad set, at most three.
2. The ledger rotation, the STATUS line with its README sync and the self-use queue's
   `consumed_by`, and the pull request, left unmerged.

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109,
  DECISION F287 D6); the closure's self-use run needed no repair round, so that is not yet
  observed in real use.
- R-1162 (Low, F297): a `claude-cli` job with no model configured cannot finish a stop.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 (Low) stay open,
  owned by F297.
