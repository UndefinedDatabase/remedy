# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order; T001 to T003 have landed.

## Current Step
Round 15, a docs repair inside the closure sequence: book round 14 and register R-1164 (two
built-state texts still say no production provider resumes), then correct
`docs/system/semantic-dedupe-v1.md`, the README's F109 entry and the feature file's Built State.

## Next Steps
1. Round 16, the evidence round again, because round 14's package no longer covers the head:
   resolve R-1164, the staging reclaim, a new evidence job and a new review package.
2. Round 17, the closing round: the ledger rotation, the STATUS line with its README sync and
   SU-046's `consumed_by`, and the pull request, left unmerged.

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109,
  DECISION F287 D6); the closure's self-use run needed no repair round, so that is not yet
  observed in real use.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162 (Low) stay
  open, owned by F297.
