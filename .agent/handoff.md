# Handoff — F115 Prompt breakdown & cost report · Round 6

Branch: feature/f115-prompt-cost-report · head = the C8 commit in the table
below (parent 595a1062; `git log -1` names the tip). Last reviewed SHA:
1422b01f (R5 PASS). Block: `.agent/authored/f115-r6-1.md`. The PLANNER call
site is wired: all three `build_trace_entry` sites now carry a real segment
manifest. No PR created, as the block ordered.

Open findings: 4, all OPEN. Next free finding ID: R-0325.
- R-0320 Low — carried from F111: `stale_diff_context` is a stop reason no code
  can emit. Not an F115 defect.
- R-0322 Medium — inherited suite red at the merge base: 5 `[reviewer]` ids in
  `tests/orchestration/test_role_conventions.py` over the 800-token cap. NOT
  fixed here — AGENTS.md bars an unrelated fix on a feature branch.
- R-0323 Low — the R4 block's gate (f) ordered SEVENTEEN paths where only
  SIXTEEN were reachable. No fix possible on disk.
- R-0324 Low — registered this round (C2): DECISION F115 D2's rank assignment
  composed the memory section FIRST and so made its own byte-identity gate
  unmeetable. Corrected before emission as DECISION F115 D3 (C3).

## Items

| Item | Status | Reason |
|------|--------|--------|
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | |
| C6   | done   | |
| C7   | done   | |
| C8   | done   | |

## Commits

| SHA | Subject | Ins |
|-----|---------|-----|
| b51a5afb | chore(f115): save the R6 step block verbatim | 400 |
| f810b6b3 | chore(f115): mirror the R6 block into last_block | 354 |
| 320d3c36 | chore(f115): register R-0324 for the D2 rank assignment | 16 |
| cdaf2ffe | docs(f115): correct the planner segment ranks as DECISION D3 | 31 |
| 920e1e72 | feat(f115): compose the planner prompt from ranked segments | 38 |
| aa0330e9 | test(f115): pin the planner composition against the sent bytes | 59 |
| cb17024a | feat(f115): give the planner trace entry its segment manifest | 8 |
| 595a1062 | test(f115): pin the planner trace manifest and its wiring | 31 |
| (C8, this commit) | chore(f115): refresh the plan and write the R6 handoff | see log |

## Changed files

| Path | Change |
|------|--------|
| .agent/authored/f115-r6-1.md | new, block verbatim (C1a) |
| .agent/last_block.md | mirror of the block (C1b) |
| .agent/live_review.md | TEXT-A appended, R-0324 OPEN (C2) |
| .agent/decisions.md | TEXT-B appended, DECISION F115 D3 (C3) |
| packages/orchestration/llm_planner.py | TEXT-C/D/E/F — `compose_planner_prompt` plus the optional `on_prompt_composed` hook (C4) |
| tests/test_llm_planner.py | TEXT-G/H — four composition tests (C5) |
| apps/cli/commands/job.py | TEXT-I1/I2/I3 — `_plan_compositions`, `composed_prompt=`, hook wired (C6) |
| tests/orchestration/test_structured_planner_cli.py | TEXT-J — two wiring guards (C7) |
| .agent/plan.md | TEXT-K in full (C8) |
| .agent/handoff.md | this file (C8) |

## Gates (real measured values)

a. `cmp` exit 0 · sha256 identical for the authored file, `last_block.md` AND
   the `.remedy-wt/` source:
   `6f4b0445f148e9b3cf92a2edbab0b2998432c2741439282bee3012599372b136` ·
   `wc -lc` authored: `400 19445`.
b. IDENTITY GATE, run after C5 with no C6 on disk:
   `tests/test_llm_planner.py` → `38 passed in 0.15s`, exit 0. GREEN — the
   composed prompt is byte-identical to the concatenation it replaces.
c. Over `.agent/live_review.md`: `^- R-0324` = 1 · `^- R-0` = 5 (was 4) ·
   `^Done:` = 1 · `^## Steps` = 1; and `^## DECISION F115 D3` in
   `.agent/decisions.md` = 1. All five as ordered.
d. `tests/orchestration/test_structured_planner_cli.py` → `17 passed in 0.25s`,
   exit 0.
e. Neighbours, one command → `134 passed in 0.44s`, exit 0.
f. Canary `tests/cli/test_golden_path.py` → `42 passed in 19.62s`, exit 0.
   The 42 baseline did not move.
g. `wc -l .agent/plan.md` = 34.
h. `git status --porcelain` empty · `git diff --name-only 0d6c97aa..HEAD | wc -l`
   = 23, matching the block; no `.remedy-wt/**` path appears ·
   `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
   = `0	0` after the final push.

## Observation, not a gate

`python3 -m ruff check` reports one NEW `I001` (un-sorted import block) at
`tests/test_llm_planner.py:7:1`, introduced by TEXT-G, which places the
`prompt_segments` import above `planner_models`. Measured, not assumed: the
same command on `git show 920e1e72:tests/test_llm_planner.py` prints
`All checks passed!`. The other three touched files are clean. NOT fixed —
authored bytes may not be edited, and ruff is not one of this round's gates.

## Resume here

All three `build_trace_entry` call sites are wired, so T001a is closed. Next is
T001 proper — persist the manifest, or a reference to it, alongside the ledger
row, additively, with backfill tolerance: pre-F115 rows render as
"unattributed", never guessed. Then T002 (aggregation queries plus the pure
renderer, with goldens) and T003 (CLI, prior-period comparison, json schema),
then the integration gate and closure, as `.agent/plan.md` lists them.

Deviations, declared: this handoff is 113 lines. The cause is the mandated
content — the nine-row item-status table, the nine-row commit table, the
ten-row changed-files table, eight gate results a-h as real measured values,
and every open finding with its state (AGENTS.md DECISION D15). One further
deviation: the "Observation, not a gate" section above is not prescribed by the
block, and is present because a measured NEW lint error introduced by an
authored slice must reach the reviewer rather than be silently dropped.

Fortschritt: 40 % (R1 ✅ · T001a ✅ · alle drei Call-Sites ✅ · T001 · T002 · T003 offen) — Schätzung
