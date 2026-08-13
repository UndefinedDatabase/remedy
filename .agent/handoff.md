# Handoff — F115 Prompt breakdown & cost report · Round 1

Branch: feature/f115-prompt-cost-report, cut from main tip
0d6c97aa06e65bea966b5210f1569de45d503845 after PR #194 merged.
No PR this round (per block). Open findings: 1 (R-0320, Low, carried from F111).
Next free finding ID: R-0321.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0   | done   | |
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | |
| C3   | done   | |

## Commits

| SHA | Subject | Insertions |
|-----|---------|-----------|
| 63d57dae | chore(f115): save the R1 step block verbatim | 282 |
| f60d64a5 | chore(f115): mirror the R1 block into last_block | 253 |
| 4fc24f51 | chore(f115): claim F115 and reset the round state | 84 |
| (C3) | docs(f115): inventory the ledger and segment registry shape | see below |

## Changed files

| Path | Commit |
|------|--------|
| .agent/authored/f115-r1-1.md | 63d57dae (new) |
| .agent/last_block.md | f60d64a5 |
| docs/roadmap/STATUS.md | 4fc24f51 (one line) |
| .agent/live_review.md | 4fc24f51 |
| .agent/candidates.md | 4fc24f51 |
| .agent/plan.md | 4fc24f51 |
| .agent/context.md | 4fc24f51 |
| .agent/f115_inventory.md | C3 (new) |
| .agent/handoff.md | C3 |

## Gates (measured)

- a. PR #194 state MERGED, mergedAt 2026-08-13T04:22:42Z. Branch
  `feature/f115-prompt-cost-report`. `git log --oneline -n 2 main`: 0d6c97aa
  "Merge pull request #194 …" / 98a49b5c. `merge-base --is-ancestor` exit 0.
- b. `cmp` exit 0. sha256 both
  393c19a37bde96f7bbe3b3b5e7e7bc1b33cbdf0f9e45602c785432670f30971f.
  `wc -lc` authored: 282 15857.
- c. 1 / 1 / 44 / 0.
- d. R-0320: 1 · `^- R-0`: 1 · `^## Steps`: 1 · `^Done:`: 0 · `^Landed:`: 0.
- e. 0.
- f. 39.
- g. 142 passed in 19.35s, exit 0.
- h. 294 passed in 0.30s, exit 0.
- i. 42 passed in 19.75s, exit 0.
- j. All seven questions answered with path:line; Q5 records "no `stats report`
  subcommand yet" and Q4 answers with a qualified YES (path-level join via
  job_id/task_id, no column) — see .agent/f115_inventory.md.
- k. See "Final state" below.

## Inventory headline (C3)

Q4 is a QUALIFIED YES, not the NO the block anticipated: a ledger row's
`(job_id, task_id)` / `evidence_ref` reaches `prompt_trace.jsonl` in the same
task-run directory, and trace lines carry the segment manifest. BUT the three
call sites behind every real ledger row — builder `pingpong_loop.py:2824`,
reviewer `pingpong_loop.py:3010`, planner `job.py:236` — never pass
`composed_prompt`, so the manifest is EMPTY on live data. T001 is therefore
LARGER than the feature file assumes; T003 is smaller. Also: `role` is
hardcoded `"builder"` (`pingpong_loop.py:4011`) and no task-class source
exists at all (`task_granularity.py:5`).

## Next expected action

Planner writes the R2 block: decide whether T001 wires the three ping-pong
call sites through the prompt-segment registry, or accepts existing rows as
permanently unattributed and builds only the backfill-tolerant path.

Deviations, declared: 83 lines, over the 60-line cap (AGENTS.md DECISION D15).
Cause is mandated content only — the item-status table (C0/C1a/C1b/C2/C3), the
four-row commit table, the nine-row changed-files table, and the eleven gate
results a-k, which the block requires as REAL measured values. No section was
dropped to meet the cap.
