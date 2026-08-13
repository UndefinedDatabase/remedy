# Handoff — F115 Prompt breakdown & cost report · R8

Branch: feature/f115-prompt-cost-report · no PR this round. Goal: settle T001's
shape (DECISION F115 D4) and land it SCHEMA ONLY — `call_segments` as migration
step 2, `calls`/`CallRecord`/`_CALL_COLUMNS` untouched.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | TEXT-A applied verbatim; no `Done:` text authored here |
| C3   | done   | TEXT-B appended to `.agent/decisions.md` |
| C4   | done   | TEXT-C appended to `docs/roadmap/features/T2_F115.md` |
| C5   | done   | three authored pairs, each FROM matched exactly once |
| C6   | done   | four tests, one class, no parametrize |
| C7   | done   | plan rewritten, this handoff rewritten |

## Commits

| SHA | Subject | Insertions |
|-----|---------|-----------|
| 8d3397f8 | chore(f115): save the R8 step block verbatim | 284 |
| 04880fd6 | chore(f115): mirror the R8 block into last_block | 272 (−231) |
| 24e1c46d | docs(f115): record the R7 resolutions for R-0325 and R-0326 | 4 |
| d43dcc4a | docs(f115): decide the T001 persistence shape as DECISION D4 | 50 |
| 1e121370 | docs(f115): record the T001 table shape in the feature file | 15 |
| d84b4f8f | feat(f115): add the call_segments table as migration step 2 | 25 (−2) |
| 0e02933d | test(f115): prove the call_segments schema and its upgrade path | 107 |
| (C7)     | chore(f115): refresh the plan and write the R8 handoff | see git |

## Changed files this round

| Path | Change |
|------|--------|
| .agent/authored/f115-r8-1.md | new, the R8 block verbatim |
| .agent/last_block.md | rewrite, byte-identical mirror |
| .agent/live_review.md | +4 (TEXT-A, two paragraphs) |
| .agent/decisions.md | +50 (DECISION F115 D4) |
| docs/roadmap/features/T2_F115.md | +15 (T001 persistence shape) |
| packages/orchestration/token_ledger.py | +25 −2 (SCHEMA_VERSION 2, step 2, docstring) |
| tests/orchestration/test_token_ledger.py | +107 (four tests) |
| .agent/plan.md | full replace |
| .agent/handoff.md | rewrite |

## Results (all measured, exit codes recorded)

- a. `cmp` rc=0. sha256 of BOTH copies
  `db01e5cd2eb0e006d22a9ab238381e520c39f53b63b29f8b03d17970b32fe2ad`.
  `wc -lc .agent/authored/f115-r8-1.md` = `284 18965`.
- b. `.agent/live_review.md`: `^Done:` = 3 · `^- R-0` = 7 · `^## Steps` = 1.
- c. `^## DECISION F115 D4` in `.agent/decisions.md` = 1.
- d. `^## T001 persistence shape` in `docs/roadmap/features/T2_F115.md` = 1.
- e. `^SCHEMA_VERSION = 2` = 1 · `^SCHEMA_VERSION = 1` = 0 ·
  `CREATE TABLE IF NOT EXISTS call_segments` = 1 · `idx_call_segments_call_id` = 1 ·
  the block's literal `'        2: ('` (EIGHT leading spaces) = **0**; the entry is
  written at the dict's four-space indent, so `'    2: ('` = 1. Reported as
  measured, nothing changed to meet the number. ruff rc=0 `All checks passed!`;
  `python3 -c "import packages.orchestration.token_ledger"` rc=0.
- f. `pytest tests/orchestration/test_token_ledger.py -q` rc=0 → `86 passed in 6.28s`
  (R7 baseline 82 + 4). Matches the expected `86 passed`.
- g. RED-PROOF in `.remedy-wt/r8-redproof` (detached at 0e02933d), step 2 deleted:
  `8 failed, 78 passed in 6.96s`. All FOUR new tests failed
  (`test_a_fresh_ledger_carries_the_call_segments_table`,
  `test_a_version_one_ledger_gains_the_table_on_reopen`,
  `test_call_segments_columns_mirror_the_manifest`,
  `test_a_pre_f115_call_owns_no_segment_rows` — the fourth fails too, on
  `sqlite3.OperationalError: no such table: call_segments`, one more than the
  block predicted). Four PRE-EXISTING tests also failed, because deleting step 2
  while `SCHEMA_VERSION` stays 2 desynchronises them: `TestOpenLedger`'s
  `test_creates_file_meta_wal_and_indexes`, `test_open_is_idempotent`,
  `test_schema_version_matches_the_last_migration_step`,
  `test_meta_holds_exactly_one_version_row`. Worktree removed with
  `--force` and pruned; `git worktree list` now prints exactly one line:
  `/home/decodeux/Repos/remedy  0e02933d [feature/f115-prompt-cost-report]`.
  The primary checkout was never mutated.
- h. `pytest tests/docs/ -q` rc=0 → `294 passed in 0.25s`.
- i. Canary `pytest tests/cli/test_golden_path.py -q` rc=0 → `42 passed in 19.61s`.
- j. `wc -l .agent/plan.md` = 35 (below 50).
- k. `git status --porcelain` empty · `git diff --name-only 0d6c97aa..HEAD | wc -l`
  = 27 (24 from R7 + `.agent/authored/f115-r8-1.md`,
  `packages/orchestration/token_ledger.py`,
  `tests/orchestration/test_token_ledger.py`); no `.remedy-wt/**` path present ·
  `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
  = `0 0`.

Open findings: 4 — R-0320, R-0322, R-0323, R-0324. Next free ID: R-0327.
Next expected action: the `call_segments` WRITER, populating from the copied
`prompt_trace.jsonl` on the backfill path (the live hook runs before the copy).

Shell restriction declared: the sandbox refuses any command whose arguments
contain a dollar sign, so every exit code was captured through a small
`subprocess` runner instead of echoing the shell status variable; no grep
pattern this round needed one.

Deviations, declared: 102 lines. The mandated content — item-status table,
commit table (8 commits), changed-files table and eleven lettered results
including the multi-line red-proof breakdown — does not fit in 60
(AGENTS.md DECISION D15).

Fortschritt: 50 % (R1 ✅ · T001a ✅ · alle drei Call-Sites ✅ · T001-Shape-Inventar ✅ · T001-Persistenz läuft · T002 · T003 offen) — Schätzung
