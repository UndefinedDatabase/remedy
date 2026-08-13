# Handoff — F115 Prompt breakdown & cost report · Round 7

Branch: feature/f115-prompt-cost-report · head = the C6 commit in the table
below (parent 8114dda7; `git log -1` names the tip). Last reviewed SHA:
139b5c48 (R6 PASS). Block: `.agent/authored/f115-r7-1.md`. R7 cleared the two
R6 authoring defects and put the T001 persistence FACTS on disk. No PR created,
as the block ordered. LAST ROUND OF THE SESSION.

Open findings: 6, all OPEN. Next free finding ID: R-0327.
- R-0320 Low — carried from F111: `stale_diff_context` is a stop reason no code
  can emit. Not an F115 defect. No fix this round (block forbade it).
- R-0322 Medium — inherited suite red at the merge base: 5 `[reviewer]` ids in
  `tests/orchestration/test_role_conventions.py` over the 800-token cap. Not
  fixed here — AGENTS.md bars an unrelated fix on a feature branch.
- R-0323 Low — the R4 block's gate (f) ordered SEVENTEEN paths where only
  SIXTEEN were reachable. Reviewer arithmetic; no fix possible on disk.
- R-0324 Low — DECISION F115 D2's rank assignment made its own byte-identity
  gate unmeetable; corrected before emission as D3. No on-disk fix.
- R-0325 Low — registered this round (C2). Landed: R-0325 — the
  `prompt_segments` import moved below `planner_models` in
  `tests/test_llm_planner.py`, commit dd7feebd.
- R-0326 Low — registered this round (C2). Landed: R-0326 — the
  `compose_planner_prompt` docstring now names the blank-line separator in
  words instead of spelling the escape, commit cbe38b90.
Neither is marked resolved: the reviewer authors the `Done:` text at the gate.

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

## Commits

| SHA | Subject | Ins |
|-----|---------|-----|
| 90218c6f | chore(f115): save the R7 step block verbatim | 243 |
| ccd5d308 | chore(f115): mirror the R7 block into last_block | 166 |
| f8d4cfd0 | chore(f115): register R-0325 and R-0326 from the R6 gate | 24 |
| dd7feebd | fix(f115): sort the planner test imports | 1 |
| cbe38b90 | docs(f115): keep the composer docstring free of an escape | 4 |
| 8114dda7 | docs(f115): inventory the T001 persistence facts | 208 |
| (C6, this commit) | chore(f115): refresh the plan and write the R7 handoff | see log |

## Changed files

| Path | Change |
|------|--------|
| .agent/authored/f115-r7-1.md | new, block verbatim (C1a) |
| .agent/last_block.md | mirror of the block (C1b) |
| .agent/live_review.md | TEXT-A appended, R-0325 + R-0326 OPEN (C2) |
| tests/test_llm_planner.py | TEXT-B — import block sorted (C3) |
| packages/orchestration/llm_planner.py | TEXT-C — docstring escape removed (C4) |
| .agent/f115_inventory.md | TEXT-D plus the Q1-Q6 answers (C5) |
| .agent/plan.md | TEXT-E in full (C6) |
| .agent/handoff.md | this file (C6) |

## Gates (real measured values)

a. `cmp .agent/authored/f115-r7-1.md .agent/last_block.md` exit 0 · sha256
   identical for the authored file, `last_block.md` AND the `.remedy-wt/`
   source: `c6ab0e7d25c42144af766401daf7a90309dae3736c6c0ba8285a0a6b9942ea00` ·
   `wc -lc` authored: `243 13927`.
b. Over `.agent/live_review.md`: `^- R-0325` = 1 · `^- R-0326` = 1 ·
   `^- R-0` = 7 (was 5) · `^Done:` = 1 · `^## Steps` = 1. All five as ordered.
c. Before C3, `python3 -m ruff check tests/test_llm_planner.py` printed
   `I001 [*] Import block is un-sorted or un-formatted` at
   `tests/test_llm_planner.py:7:1` and `Found 1 error.`, exit 1. After C3:
   `All checks passed!`, exit 0. The other three files, one command
   (`llm_planner.py`, `apps/cli/commands/job.py`,
   `tests/orchestration/test_structured_planner_cli.py`) →
   `All checks passed!`, exit 0.
d. `grep -c 'this module$' packages/orchestration/llm_planner.py` = 1 before
   C4, 0 after · `grep -c 'the same blank-line separator' …` = 1. (Transport
   note: this shell refuses a command whose argument contains `$`; the count
   was run as `grep -c -f <pattern-file>` with the identical pattern.)
e. `python3 -m pytest tests/test_llm_planner.py -q` → `38 passed in 0.15s`,
   exit 0. The R6 baseline of 38 did not move, as predicted.
f. `grep -c '^## T001 persistence inventory (R7)' .agent/f115_inventory.md` = 1 ·
   `grep -c '^Q[1-6]\.' …` = 6 · answers `^A[1-6]\.` = 6, one under each.
g. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` →
   `42 passed in 19.72s`, exit 0. The 42 baseline did not move.
h. `wc -l .agent/plan.md` = 38 — below 50.
i. `git status --porcelain` empty · `git diff --name-only 0d6c97aa..HEAD | wc -l`
   = 24, the 23 paths of R6 plus `.agent/authored/f115-r7-1.md`, matching the
   block; no `.remedy-wt/**` path appears ·
   `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
   = `0	0` after the final push.

## What C5 found (facts, not a decision)

The `calls` row has 13 columns, three of them NOT NULL (`call_id`, `ts_utc`,
`cost_basis`) and NO SQL DEFAULT anywhere; the schema has exactly ONE migration
step and no `ALTER TABLE` has ever run in this repository, so T001 would be the
first user of the migration mechanism. `record_call` writes with
`INSERT OR IGNORE`, which never UPDATEs, and `verify_ledger` compares rows by
whole-dataclass equality — both constrain how a manifest may be attached. The
ledger hook fires BEFORE `prompt_trace.jsonl` is copied into the bundle and the
bundle carries only a PATH to it, so no manifest object is ever in scope at the
write seam. Builder and reviewer traces from the job path carry both halves of
the `call_id`; planner traces carry `job_id` only, and `remedy do` traces carry
neither. The established "no data" word is `unmeasured` — `unattributed` occurs
in no Python file. Full text with `path:line` citations:
`.agent/f115_inventory.md`, section "## T001 persistence inventory (R7)".

## Resume here

Next work is T001's PERSISTENCE SHAPE, decided from the C5 inventory: choose
between an aggregate column on the row, a reference to the trace file, and a
per-call table, record it as a DECISION, then persist additively with backfill
tolerance — pre-F115 rows render "unattributed", never guessed. Then T002
(aggregation queries plus the pure renderer, with goldens) and T003 (CLI,
prior-period comparison, json schema), then the integration gate and closure,
as `.agent/plan.md` lists them.

Deviations, declared: this handoff is 134 lines. The cause is the mandated
content — the seven-row item-status table, the seven-row commit table, the
eight-row changed-files table, nine gate results a-i as real measured values,
and every one of the six open findings with its state (AGENTS.md DECISION D15).
Two further declared items: (1) the "What C5 found" section is not prescribed by
the block, and is present because this is the LAST ROUND OF THE SESSION and the
handoff is the only return channel for the round's substance; (2) the shell used
this round refuses any command whose arguments contain a `$`, so gate (d)'s
`grep -c 'this module$'` was run as `grep -c -f <pattern-file>` over a file
holding exactly the string `this module$` — same grep, same pattern, same
result, recorded here rather than silently substituted.

Fortschritt: 45 % (R1 ✅ · T001a ✅ · alle drei Call-Sites ✅ · T001-Shape ✅ · T001 · T002 · T003 offen) — Schätzung
