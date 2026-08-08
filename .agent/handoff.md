# Handback — F103 R3, T002 data layer + the call site

Feature **T2_F103 — Token ledger (SQLite)**, round **R3** (SPLIT, PRODUCTION
CODE — never merges self-certified). Branch **`feature/f103-token-ledger`**,
already at `c3a03076` — not re-cut, no PR, no merge, no force-push, main
untouched. `.agent/STOP` absent, re-checked before every commit.

## Range
Review of `c3a03076..HEAD`. Five content commits; this file is the sixth.

## Commits

### eef95aff chore(f103): persist the R2 PASS verdict and findings R-0218 and R-0219
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +85/-3 | receipt 1 — R2 step line → PASS, R-0218/R-0219, DECISION D16, the R2 verdict, `- R3: pending review.` |
| .agent/authored/f103-r3-1.md | +136/-0 | receipt 1, all four pairs |

### 37627879 docs(f103): record the ledger row-granularity ruling on the feature file
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F103.md | +15/-0 | receipt 3 — the D16 row-granularity section |
| .agent/authored/f103-r3-3.md | +22/-0 | receipt 3, the APPEND-shaped pair |

### 798e47d3 feat(f103): add ledger backfill and reconcile over actuals evidence
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/token_ledger.py | +451/-12 | `call_id_for_task_run`, `job_id_for_evidence_dir`, `call_record_from_evidence`, `backfill_ledger`, `verify_ledger`, `BackfillResult`, `ReconcileResult` |

### c4b4e32c test(f103): pin backfill idempotence, the unmeasured and malformed cases, and reconcile drift
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_token_ledger.py | +348/-1 | on-disk `evidence_tree` fixture + 26 T002 tests |

### 6b030495 feat(f103): record finalized actuals into the token ledger
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_evidence.py | +91/-0 | the opt-in hook after the `provider_evidence.json` write |
| packages/orchestration/token_ledger.py | +4/-1 | docstring now names its one call site |
| tests/orchestration/test_token_ledger.py | +123/-0 | 6 call-site tests |
| .agent/plan.md | +32/-32 | receipt 2 — full-file replacement, current at the final content commit |
| .agent/authored/f103-r3-2.md | +52/-0 | receipt 2 |

### (this commit) chore(f103): rewrite handoff for the R3 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback — cannot table its own SHA |

Staged by exact path; `git add -A` never used. No CLI in this round. No new
dependency (bundled `sqlite3` only, no ORM). Untouched: `token_truth.py`
(no re-export was needed — see below), `token_measurement.py`,
`provider_token_evidence.py`, `data_paths.py`, `project_registry.py`,
`budget_guard.py`, `budget_resolution.py`, `final_verifier.py`, all
estimation/calibration code, `.agent/decisions.md`, `.agent/context.md`,
`.agent/candidates.md`, `docs/roadmap/STATUS.md`, `README.md`.

## Verification (real commands, real exit codes, after commit 5)
| Command | Exit | Tail |
|---|---|---|
| `pytest tests/orchestration/test_token_ledger.py -q` | 0 | `50 passed in 0.30s` |
| `pytest tests/ -q -k "pingpong or evidence"` | 0 | `1129 passed, 14926 deselected in 77.60s` |
| `pytest tests/docs/ -q` | 0 | `294 passed in 0.30s` |
| `pytest test_dashboard_contract.py test_test_runner.py test_resource_safety.py -q` | 0 | `142 passed in 18.73s` |
| `pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 19.20s` |
| `git status --porcelain` | 0 | no output — clean tree |
| `ruff check` (the 3 changed .py) | 0 | `All checks passed!` |
The regression guard selected **1129** tests — far above the 20 that would have
forced widening, so the selection stands as written. `tests/docs/` ran because
this round changes `docs/roadmap/**`. Repo-wide sweep for `*.sqlite`, `*-wal`,
`*-shm`, including `.data/` and `.data/projects/`: **0 hits** — every test DB
lives under `tmp_path`. Nothing red; the STOP rule never fired.

## Authored-text proofs
All three receipts saved BEFORE any target was touched; none hand-retyped; no
trailing whitespace on any line; each ends in exactly one newline (byte-wise
checked: 6473 B / 2717 B / 1193 B).
- Receipt 1 → `.agent/live_review.md`, four REWRITE pairs. Every FROM counted
  **exactly 1x BEFORE any edit**. After: PAIR 1 FROM **0x** / TO **1x**;
  PAIR 2 FROM **0x** / TO **1x**; PAIR 3 FROM **0x** / TO **1x**;
  PAIR 4 FROM **0x** / TO **1x**. live_review.md **97 → 176 lines**.
- Receipt 2 → `.agent/plan.md`, FULL-FILE REPLACEMENT applied by
  `cp .agent/authored/f103-r3-2.md .agent/plan.md`, proved by
  `cmp .agent/authored/f103-r3-2.md .agent/plan.md` → **exit 0**.
- Receipt 3 → `docs/roadmap/features/T2_F103.md`, APPEND-shaped: FROM **1x
  before AND 1x after**, TO **0x before → 1x after**, and each of the **14
  TO-ONLY lines occurs exactly 1x after**. Feature file **83 → 98 lines**.

## How R-0219 was resolved — CONTENT COMPARISON in `verify_ledger`
Both options were available; content comparison was chosen. `verify_ledger`
re-derives each row from its own evidence through `call_record_from_evidence`
and compares the whole `CallRecord` field by field, reporting mismatches in a
new `drifted_rows` list. Why not the presence-only option: `record_call`'s
`INSERT OR IGNORE` cannot overwrite an existing row, so a drifted row can never
heal itself — presence-only would leave a permanently wrong row permanently
invisible, which is exactly the failure R-0219 predicted. `call_id` IS also
pinned immutable by construction and said so in `call_id_for_task_run`'s
docstring, but that alone only guarantees the id, not the row's contents.
Content comparison is only safe because the live call site and backfill share
ONE producer: the hook re-reads the `provider_evidence.json` it has just
written through the same `call_record_from_evidence`, so two producers of one
row cannot disagree. `test_the_live_row_is_the_row_backfill_would_have_written`
pins that, and `test_finds_a_content_drifted_row` pins the detection.

## Design points worth the reviewer's eye
1. **No second capture path.** `_call_record_from_parts` calls
   `token_truth._extract_actual` and `token_truth._strict_cost` — the private
   helpers the step block authorised — instead of a second parser. Nothing in
   `token_truth.py` changed, so the re-export route was not needed.
2. **`TokenEvidenceError` is honoured, not swallowed.** A malformed counter
   makes the task run unrecordable (None), counted in `failed`; no plausible
   number is stored.
3. **The hook is inert three ways**: no ledger target, or missing job/task id,
   or an `out_dir` that is not `task_runs/<task_id>/` → it returns without
   touching anything. It never resolves a project implicitly.
4. **Orphan detection is scoped by `job_id`**, because one project ledger holds
   many jobs and another job's rows are not orphans of this evidence tree.

## Item status — R3 bundle B1-B7
| Item | Status | Reason |
|---|---|---|
| B1 save receipts 1-3 | done | written first, before any target touched |
| B2 commit 1 — findings + verdict persist | done | eef95aff, first action |
| B3 commit 2 — feature-file amendment | done | 37627879 |
| B4 commit 3 — backfill + reconcile core | deviated | split into 798e47d3 (module, 463 lines) and c4b4e32c (tests, 349 lines); one commit would have been 812 lines and the step block orders a split over an oversize exception |
| B5 commit 4 — the call site | done | 6b030495, with `.agent/plan.md` + receipt 2 as instructed |
| B6 verification | done | seven commands, all exit 0, numbers above |
| B7 commit 5 + push | done | this commit, then push |

## Findings
Open findings: **2** — R-0218 (Low, deferred to R5's integration gate) and
R-0219 (Low, **resolved this round**, see above; the reviewer decides whether
to close it). Next free ID: **R-0220**. LAST_REVIEWED_SHA `c3a03076`.

## Deviations, declared
1. **Six commits, not five** — B4 split per its own instruction (see table).
   No oversize exception is claimed; no commit exceeds 500 lines.
2. This file is 152 lines, over the 60-line cap, with NO section dropped.
   Cause, all mandated: six per-commit changed-files tables, the seven-row
   verification table, the three-receipt transport proof with its counts, the
   B1-B7 item-status table, the explicitly-demanded R-0219 resolution
   statement, and the closure values.
3. `.agent/decisions.md` not updated although the R-0219 ruling is a
   meaningful decision — the step block puts that file outside the round's
   path set. It is recorded in the module docstrings and in this handback.
4. Commit 6's SHA and the push result are absent by self-reference
   impossibility, not omission; both are in the completion report.

## Next
Window 1 reviews `c3a03076..HEAD` and issues the R3 verdict; production code,
so self-certification is barred. On PASS, R4 is T003 plus T002's surface: the
`remedy stats` command group (`cost`, `backfill-ledger`, `verify-ledger`),
basis labeling on every figure, read-only `--all-projects`, and CLI tests.
