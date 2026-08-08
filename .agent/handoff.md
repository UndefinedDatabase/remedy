# Handback — F103 R2, T001 SQLite token ledger

Feature **T2_F103 — Token ledger (SQLite)**, round **R2** (SPLIT, PRODUCTION
CODE — never merges self-certified). Branch **`feature/f103-token-ledger`**,
already at `28781d8f` — not re-cut, no PR, no merge, no force-push.
`.agent/STOP` absent, re-checked before every commit.

## Range
Review of `28781d8f..HEAD`. Three content commits; this file is the fourth.

## Commits

### 5fbc5660 chore(f103): persist the R1 PASS verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +30/-3 | receipt 1 — R1 step line → PASS, R1 verdict written, `- R2: pending review.` added |
| .agent/authored/f103-r2-1.md | +63/-0 | receipt 1, both FROM→TO pairs |

### b00ffa41 feat(f103): add the SQLite token ledger schema and writer
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/token_ledger.py | +351/-0 | T001 module: schema, migration bootstrap, `record_call`, WAL, miss counter |
| .agent/plan.md | +28/-16 | receipt 2 — Current Step moves R1 → R2 |
| .agent/authored/f103-r2-2.md | +52/-0 | receipt 2, full-file replacement |

### b04006dd test(f103): pin the ledger schema, writer and never-fail rule
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_token_ledger.py | +393/-0 | 18 tests, all 8 mandated behaviours |

### (this commit) chore(f103): rewrite handoff for the R2 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback — cannot table its own SHA |

Staged by exact path; `git add -A` never used. No call site added anywhere; no
file outside the declared set touched. `data_paths.py`, `project_registry.py`,
`budget_guard.py`, `budget_resolution.py`, `token_truth.py`,
`token_measurement.py`, `provider_token_evidence.py`, `.agent/decisions.md`,
`.agent/context.md`, `.agent/candidates.md`, `docs/roadmap/**`, `README.md`
— all unchanged. No new dependency: bundled `sqlite3` only, no ORM.

## Verification (real commands, real exit codes, after commit 3)
| Command | Exit | Tail |
|---|---|---|
| `pytest tests/orchestration/test_token_ledger.py -q` | 0 | `18 passed in 0.14s` |
| `pytest test_dashboard_contract.py test_test_runner.py test_resource_safety.py -q` | 0 | `142 passed in 18.53s` |
| `pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 19.20s` |
| `git status --porcelain` | 0 | no output — clean tree |
| `ruff check token_ledger.py test_token_ledger.py` | 0 | `All checks passed!` |
Tests collected in `test_token_ledger.py`: **18**, all passed, none skipped
(euid 1000, so the read-only-DB test ran). Repo-wide sweep for `*.sqlite`,
`*.sqlite3`, `*-wal`, `*-shm` including `.data/`: **0 hits** — every test DB
lives under `tmp_path`. Nothing red; the STOP rule never fired.

## Authored-text proofs
Both receipts saved BEFORE any target was touched; neither hand-retyped; no
trailing whitespace on any line; each ends in exactly one newline (byte-wise
checked: 2726 B / 63 lines and 2638 B / 52 lines).
- Receipt 1 → `.agent/live_review.md`, TWO REWRITE pairs, both applied by exact
  substring replacement lifted from the receipt (never retyped):
  PAIR 1 FROM **1x before → 0x after**, TO **0x before → 1x after**;
  PAIR 2 FROM **1x before → 0x after**, TO **0x before → 1x after**.
  Both pairs verified disjoint (FROM ⊄ TO and TO ⊄ FROM) before editing, so the
  REWRITE shape is real. live_review.md **70 → 97 lines**.
- Receipt 2 → `.agent/plan.md`, FULL-FILE REPLACEMENT by
  `cp .agent/authored/f103-r2-2.md .agent/plan.md`, then
  `cmp .agent/plan.md .agent/authored/f103-r2-2.md` → **exit 0**.

## What T001 actually contains
Schema v1 in a numbered-step migration map (`{1: (...)}`, not an if-ladder):
`meta(key,value)` carrying `schema_version`, `calls(...)` with the 13
CallRecord columns and `call_id` PRIMARY KEY, plus the three covering indexes
`idx_calls_job_id`, `idx_calls_ts_utc`, `idx_calls_role_model`. `open_ledger`
creates parents, sets `journal_mode=WAL` and `busy_timeout=5000`, and is
idempotent. `record_call` writes one `INSERT OR IGNORE` per commit, closes in
`finally`, catches every `Exception`, logs at ERROR with `exc_info`, counts a
miss and returns False — it cannot raise. `CallRecord` is `kw_only` so
`call_id` and `ts_utc` stay genuinely required while the field ORDER stays as
mandated. The docstring carries the "file evidence remains the source of truth
and the database is a mirror" sentence, the first-and-only-SQLite note, and the
four deliberate absences (no ORM, no second capture path, no invented prices,
budgets do not read this DB).

**One judgement call worth the reviewer's eye:** `INSERT OR IGNORE` silently
swallows CHECK/NOT NULL rejections exactly as it swallows a duplicate key, so a
bad `cost_basis` would have returned True with no row. `record_call` therefore
checks `rowcount == 0` and asks the table whether the row is actually present:
present → idempotent re-record → True; absent → constraint rejected it → miss +
False. Pinned by `test_rejected_basis_is_a_counted_miss_not_a_silent_drop`.

## Item status — R2 bundle B1-B5
| Item | Status | Reason |
|---|---|---|
| B1 save receipts 1 and 2 | done | written first, before any target touched |
| B2 commit 1 — persist R1 verdict | done | 5fbc5660 |
| B3 commit 2 — module + tests + plan | deviated | split into b00ffa41 (module + plan + receipt, 447 lines) and b04006dd (tests, 393 lines); the single commit would have been 840 lines, and the step block orders a split over an oversize exception |
| B4 verification | done | five commands, all exit 0, numbers above |
| B5 commit 3 + push | done | this commit, then push |

## Findings
Open findings: **0**. Next free ID: **R-0218**. LAST_REVIEWED_SHA `28781d8f`.

## Deviations, declared
1. **Four commits, not three** — B3 split per its own instruction (see table).
   No oversize exception is claimed; no commit exceeds 500 lines.
2. This file is 121 lines, over the 60-line cap, with NO section dropped.
   Cause, all mandated: four per-commit changed-files tables, the five-row
   verification table, the two-pair transport proof with its eight counts, the
   B1-B5 item-status table, and the closure values.
3. `.agent/decisions.md` not updated though the `rowcount==0` disambiguation is
   a non-obvious tradeoff — the step block puts that file outside the round's
   path set. It is documented in the module comment and in this handback.
4. Commit 4's SHA and the push result are absent by self-reference
   impossibility, not omission; both are in the completion report.

## Next
Window 1 reviews `28781d8f..HEAD` and issues the R2 verdict; production code,
so self-certification is barred. On PASS, R3 is T002 — and its FIRST item is
wiring `record_call` into the seam where actuals are finalized, so the ledger
stops being dead code, then `backfill-ledger` and `verify-ledger`.
