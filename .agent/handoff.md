# Handback — F103 R4, T003 + T002's CLI surface

Feature **T2_F103 — Token ledger (SQLite)**, round **R4** (SPLIT, PRODUCTION
CODE — never merges self-certified). Branch **`feature/f103-token-ledger`**,
already at `d2bc7d8e` — not re-cut, no PR, no merge, no force-push, main
untouched. `.agent/STOP` absent, re-checked before every commit.

## Range
Review of `d2bc7d8e..HEAD`. Six content commits; this file is the seventh.

## Commits

### 550685fd chore(f103): persist the R3 PASS verdict and close finding R-0219
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +58/-5 | receipt 1 — R3 step line → PASS, R-0219 closed, the R3 verdict, `- R4: pending review.` |
| .agent/authored/f103-r4-1.md | +97/-0 | receipt 1, all three pairs |

### e3101b74 feat(f103): add cost aggregation queries over the ledger
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/token_ledger.py | +296/-0 | `CostRow`, `CostReport`, `COST_GROUP_KEYS`, `query_cost`, `merge_cost_reports`, `_connect_readonly`, `_cost_filters`, `_cost_bucket_rows`, `_add_optional`, `_combine_cost_rows` |

### 16c99fdb test(f103): pin the cost aggregation queries and the unmeasured rule
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_token_ledger.py | +244/-0 | `cost_ledger` fixture + 22 T003 tests (18 → 50 → 72 in the file) |

### d94bf047 feat(f103): add remedy stats cost, backfill-ledger and verify-ledger
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/stats_ledger_cmd.py | +400/-0 | the three `_cmd_*` handlers, the basis renderer, `COMMAND_HANDLERS` |
| apps/cli/command_catalog.py | +66/-0 | three `CommandEntry`s in the EXISTING `stats` group |
| apps/cli/commands/__init__.py | +2/-1 | the import AND the collector tuple |
| tests/cli/test_failure_cmd.py | +4/-1 | see Deviations 2 — the one assertion that pinned the group's whole contents |

### 50ab6e25 test(f103): pin the stats ledger commands and basis labeling
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_stats_cost.py | +460/-0 | 33 tests: registration, dispatch, JSON shape, grouping, basis labeling, drift exit codes, idempotence |

### 74495d28 chore(f103): sync the plan to the R4 step
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +26/-31 | receipt 2 — full-file replacement |
| .agent/authored/f103-r4-2.md | +47/-0 | receipt 2 |

### (this commit) chore(f103): rewrite handoff for the R4 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback — cannot table its own SHA |

Staged by exact path; `git add -A` never used. No new dependency (bundled
`sqlite3` only, no ORM); no price table and no computed price anywhere; no
second capture path. Untouched: `token_truth.py`, `token_measurement.py`,
`provider_token_evidence.py`, `data_paths.py`, `project_registry.py`,
`budget_guard.py`, `budget_resolution.py`, `final_verifier.py`,
`pingpong_evidence.py`, all estimation/calibration code, `.agent/decisions.md`,
`.agent/context.md`, `.agent/candidates.md`, `docs/roadmap/**`, `README.md`.

## Verification (real commands, real exit codes, after commit 6)
| Command | Exit | Tail |
|---|---|---|
| `pytest tests/cli/test_stats_cost.py -q` | 0 | `33 passed in 0.37s` |
| `pytest tests/orchestration/test_token_ledger.py -q` | 0 | `72 passed in 0.53s` |
| `pytest tests/cli -q` | 0 | `1329 passed in 257.05s (0:04:17)` |
| `pytest test_dashboard_contract.py test_test_runner.py test_resource_safety.py -q` | 0 | `142 passed in 18.90s` |
| `pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 19.27s` |
| `git status --porcelain` | 0 | no output — clean tree |
| `ruff check` (the 5 changed/new .py) | 0 | `All checks passed!` |
Repo-wide sweep for `*.sqlite`, `*-wal`, `*-shm` including `.data/`: **0 hits**.
Each new command was also RUN for real against a temporary `REMEDY_DATA_DIR`,
human and `--json`; the actual stdout is in the completion report. Nothing red;
the STOP rule never fired.

## Authored-text proofs
Both receipts saved BEFORE any target was touched; no trailing whitespace on any
line; each ends in exactly one newline (4322 B / 2385 B).
- Receipt 1 → `.agent/live_review.md`, three REWRITE pairs. Every FROM counted
  **exactly 1x BEFORE any edit**. After: PAIR 1 FROM **0x** / TO **1x**; PAIR 2
  FROM **0x** / TO **1x**; PAIR 3 FROM **0x** / TO **1x**. File **176 → 229**.
- Receipt 2 → `.agent/plan.md`, FULL-FILE REPLACEMENT applied by
  `cp .agent/authored/f103-r4-2.md .agent/plan.md`, proved by `cmp` → **exit 0**.

## Design points worth the reviewer's eye
1. **NULL is preserved, never coerced.** `SUM()` over an all-NULL bucket stays
   NULL; the two basis columns use `COUNT(CASE …)` instead, because `COUNT`
   never returns NULL and a count of nothing genuinely IS 0. No `COALESCE`.
2. **Reading cannot write.** `_connect_readonly` opens `file:…?mode=rw` plus
   `PRAGMA query_only=1`: the first refuses to CREATE a ledger, the second makes
   SQLite reject every write, so `--all-projects` cannot create or migrate
   another project's DB. `mode=ro` was rejected deliberately — a ro handle
   cannot checkpoint the WAL on close and would leave `-wal`/`-shm` behind.
3. **`--all-projects` is refused for backfill and verify**, with a message
   saying why: backfill writes, and a reconcile compares ONE evidence tree
   against ONE ledger.
4. **Basis in both modes**: human gets an `unmeasured` word (never `0`), a
   `basis (measured/calls)` column, a counts sentence, and a FULLY/PARTLY
   UNMEASURED warning; JSON gets `null` figures plus a per-row `basis` key.

## Item status — R4 bundle B1-B7
| Item | Status | Reason |
|---|---|---|
| B1 save receipts 1-2 | done | written first, before any target touched |
| B2 commit 1 — verdict + findings persist | done | 550685fd, first action |
| B3 commit 2 — aggregation layer | deviated | split into e3101b74 (module, 296) and 16c99fdb (tests, 244); together 540 lines and the step block orders a split over an oversize exception |
| B4 commit 3 — the three CLI commands | done | d94bf047, 472 lines |
| B5 commit 4 — tests | deviated | split into 50ab6e25 (tests, 460) and 74495d28 (plan + receipt 2, 104); together 564 lines |
| B6 verification | done | seven commands, all exit 0, numbers above |
| B7 commit 5 + push | done | this commit, then push |

## Findings
Open findings: **1** — R-0218 (Low, deferred to R5's integration gate). Next
free ID: **R-0220**. LAST_REVIEWED_SHA `d2bc7d8e`.

## Deviations, declared
1. **Seven commits, not five** — B3 and B5 each split on the step block's own
   instruction (see the item table). No oversize exception is claimed; no
   commit exceeds 500 lines.
2. **`tests/cli/test_failure_cmd.py` edited although it is not in the path
   set.** Its `test_the_command_is_registered` asserted
   `[c.command_id for c in get_commands_for_group("stats")] == ["stats.failures"]`
   — an exact-contents assertion on the very group this round was told to
   extend. It went red the moment the three commands were registered. ONE line
   changed, to `"stats.failures" in {…}`, keeping F010's own claim intact;
   nothing else in that file was touched. The alternative was leaving
   `tests/cli -q` red, which B6 forbids.
3. **Two helpers beyond the two named in B3**: `merge_cost_reports` (public)
   and `_connect_readonly`/`_cost_*`/`_add_optional` (private). B4 says the CLI
   only renders, so cross-project folding had to live in the data layer.
4. `.agent/decisions.md` not updated although the read-only-connection choice is
   a real trade-off — the step block puts that file outside the path set. It is
   recorded in the module docstring and here.
5. This file is 145 lines, over the 60-line cap, with NO section dropped. Cause,
   all mandated: seven per-commit changed-files tables, the seven-row
   verification table, the two-receipt transport proof with its counts, the
   B1-B7 item-status table, and the declared deviations.
6. Commit 7's SHA and the push result are absent by self-reference
   impossibility, not omission; both are in the completion report.

## Next
Window 1 reviews `d2bc7d8e..HEAD` and issues the R4 verdict; production code, so
self-certification is barred. On PASS, R5 is the integration gate per
docs/agents/integration_gate.md, which also owes R-0218 a real before/after
timing of the call-site seam.
