# Handoff — F115 Prompt breakdown & cost report · Round 5 (LAST OF SESSION)

Branch: feature/f115-prompt-cost-report · head = the C4 commit in the table
below (parent 151efc4c; `git log -1` names the tip). Last reviewed SHA:
19b59ccc (R4 PASS). Block: `.agent/authored/f115-r5-1.md`. Housekeeping only:
no source file and no test file touched. No PR created, as the block ordered.

Open findings: 3, all OPEN. Next free finding ID: R-0324.
- R-0320 Low — carried from F111: `stale_diff_context` is a stop reason no code
  can emit. Not an F115 defect.
- R-0322 Medium — inherited suite red at the merge base: 5 `[reviewer]` ids in
  `tests/orchestration/test_role_conventions.py` over the 800-token cap.
  Deliberately NOT fixed here — AGENTS.md bars an unrelated fix on a feature
  branch. F115's integration gate will meet it as five pre-existing reds.
- R-0323 Low — registered this round (C2): the R4 block's gate (f) ordered
  SEVENTEEN paths where only SIXTEEN were reachable. No fix possible on disk;
  registered so the reviewer-arithmetic pattern stays countable.

## Items

| Item | Status | Reason |
|------|--------|--------|
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |

## Commits

| SHA | Subject | Ins |
|-----|---------|-----|
| 186db9ed | chore(f115): save the R5 step block verbatim | 213 |
| 22fb8973 | chore(f115): mirror the R5 block into last_block | 167 |
| 5133fd4c | chore(f115): register R-0323 for the R4 gate arithmetic | 24 |
| 151efc4c | docs(f115): record the planner call site shape as DECISION D2 | 53 |
| (C4, this commit) | chore(f115): refresh the plan and write the R5 handoff | see log |

## Changed files

| Path | Change |
|------|--------|
| .agent/authored/f115-r5-1.md | new, block verbatim (C1a) |
| .agent/last_block.md | mirror of the block (C1b) |
| .agent/live_review.md | TEXT-A appended, R-0323 OPEN (C2) |
| .agent/decisions.md | TEXT-B appended, DECISION F115 D2 (C3) |
| .agent/plan.md | TEXT-C in full (C4) |
| .agent/handoff.md | this file (C4) |

## Gates (real measured values)

a. `cmp` exit 0 · sha256 identical for both files,
   `7d36e6af2eb8b7e901a4117b3b3c3c40877097942fa8568f557f25108124d08f` ·
   `wc -lc` authored: `213 12895`.
b. `^- R-0323` = 1 · `^- R-0` = 4 (was 3) · `^Done:` = 1 · `^## Steps` = 1.
c. `^## DECISION F115 D2` = 1.
d. `tests/cli/test_golden_path.py` → `42 passed in 19.76s`, exit 0 ·
   `tests/docs/` → `294 passed in 0.25s`, exit 0. Neither baseline moved.
e. `wc -l .agent/plan.md` = 40.
f. `git status --porcelain` empty · `git diff --name-only 0d6c97aa..HEAD | wc -l`
   = 18, matching the block; no `.remedy-wt/**` path appears ·
   `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
   = `0	0` after the final push.

## Resume here

Next work is the PLANNER call site, the last of the three unwired
`build_trace_entry` sites. Its shape is already on disk as DECISION F115 D2 in
`.agent/decisions.md`: build `compose_planner_prompt` in
`packages/orchestration/llm_planner.py` over the two parts that already exist
(job prompt at TASK rank, recalled memory at JOB_CONTEXT rank), thread the
`ComposedPrompt` out to `_record_plan_call` (`apps/cli/commands/job.py:236`)
through an explicit optional hook on `plan_job_with_llm`, and gate FIRST on
byte-identity of the sent prompt. If that identity fails, the round stops
rather than changing what the planner sends. Then T001 → T002 → T003 as
`.agent/plan.md` lists them.

Deviations, declared: this handoff is 85 lines. The cause is the mandated
content — the item-status table, the per-commit table, the changed-files table,
six gate results a-f as real measured values, and the block's own requirement
that this last-of-session handoff carry the branch, head, last reviewed SHA,
every open finding with its state, and the resumable next action
(AGENTS.md DECISION D15).

Fortschritt: 30 % (R1 ✅ · T001a ✅ · Reviewer-Site ✅ · Planner-Site · T001 · T002 · T003 offen) — Schätzung
