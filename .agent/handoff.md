# Handoff — F115 Prompt breakdown & cost report · Round 4

Branch: feature/f115-prompt-cost-report · head eed27fb0 (+ this C5 commit).
Block: `.agent/authored/f115-r4-1.md`. Open findings: 2 — R-0320, R-0322.
R-0321 resolved at the R4 gate. No PR created, as the block ordered.

## Items

| Item | Status | Reason |
|------|--------|--------|
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | |

## Commits

| SHA | Subject | Ins |
|-----|---------|-----|
| 991222c7 | chore(f115): save the R4 step block verbatim | 282 |
| 7ffe2c90 | chore(f115): mirror the R4 block into last_block | 222 |
| 781c995d | chore(f115): resolve R-0321 with the reviewer verdict | 1 |
| 53094b97 | feat(f115): give the reviewer trace entry its segment manifest | 7 |
| eed27fb0 | test(f115): pin the reviewer trace manifest and its wiring | 75 |
| (C5) | chore(f115): refresh the plan and write the R4 handoff | see log |

## Changed files

| Path | Change |
|------|--------|
| .agent/authored/f115-r4-1.md | new, block verbatim |
| .agent/last_block.md | mirror of the block |
| .agent/live_review.md | R-0321 Landed → Done |
| packages/orchestration/pingpong_loop.py | TEXT-B/C/D, reviewer call site composes |
| tests/orchestration/test_prompt_trace.py | TEXT-E, two new tests |
| .agent/plan.md | TEXT-F in full |
| .agent/handoff.md | this file |

## Gates (real measured values)

a. `cmp` exit 0. sha256 both files
   `b9af81cb17ee479f84ed8107d93565ebe09067f7f2bfa72f24ec355b93f72801`.
   `wc -lc` authored: `282 16043`.
b. `^Done: R-0321` = 1 · `^Landed:` = 0 · `^- R-0` = 3.
c. `reviewer_composed = compose_reviewer_prompt(` = 1 ·
   `reviewer_prompt = reviewer_composed.text` = 1 ·
   `composed_prompt=reviewer_composed,` = 1 ·
   `reviewer_prompt = _build_reviewer_prompt` = 0.
d. `48 passed in 0.29s`, exit 0 — no golden moved.
e. `46 passed in 0.25s`, exit 0 (44 + the two new tests).
f. RED-PROOF in worktree `.remedy-wt/f115r4`, wiring line deleted:
   `1 failed, 1 passed, 44 deselected in 0.24s`, exit 1.
   FAILED `test_the_reviewer_call_site_hands_its_composition_down`;
   PASSED `test_the_reviewer_composition_traces_a_real_segment_manifest`
   — exactly the expected split; the guard is alive. After removal + prune,
   `git worktree list` = one line: `/home/decodeux/Repos/remedy  eed27fb0
   [feature/f115-prompt-cost-report]`.
g. `303 passed in 2.63s`, exit 0.
h. `tests/cli/test_golden_path.py` → `42 passed in 19.93s`, exit 0 ·
   `tests/docs/` → `294 passed in 0.25s`, exit 0.
i. `wc -l .agent/plan.md` = 43.
j. `git status --porcelain` empty. `git diff --name-only 0d6c97aa..HEAD` =
   SIXTEEN paths, not seventeen — see the deviation below.
   `git rev-list --left-right --count origin/...HEAD` = `0	0`.

## Deviation, gate (j) arithmetic

Gate (j) says seventeen paths: fifteen from R1-R3 plus
`.agent/authored/f115-r4-1.md` and `tests/orchestration/test_prompt_trace.py`.
`tests/orchestration/test_prompt_trace.py` is ALREADY one of the fifteen —
`git diff --name-only 0d6c97aa..8601e276` lists it (R2 added the builder
behaviour test and its wiring guard there). Only ONE path is new this round,
so the reachable total is SIXTEEN. Nothing was changed to meet the number; the
real value is reported (planner_reviewer_prompt.md §checklist item 8). No
`.remedy-wt/**` path appears; `pingpong_loop.py` is in the fifteen as stated.

Next expected action: the PLANNER call site (`apps/cli/commands/job.py:236`),
whose prompt arrives through `llm_planner` / `make_structured_planner`.

Deviations, declared: this handoff is 88 lines. The cause is the mandated
content — item-status table, per-commit table for six commits, changed-files
table, and ten gate results a-j reported as real measured values, plus the
gate (j) arithmetic deviation that must be stated rather than silently met
(AGENTS.md DECISION D15).

Fortschritt: 30 % (R1 ✅ · T001a ✅ · Reviewer-Site ✅ · Planner-Site · T001 · T002 · T003 offen) — Schätzung
