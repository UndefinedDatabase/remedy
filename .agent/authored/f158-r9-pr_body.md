## What

F158 — Cost normalization & price catalog. Money from different workers becomes comparable,
honestly: one configured currency, a versioned price catalog per adapter with dated and sourced
prices, and a valuation of every ledger call beside its untouched raw row, with the basis it rests
on, a cross-check, and staleness warnings that never block.

- `packages/orchestration/cost_currency.py` (new): the `cost.currency` key's resolver (usd only),
  the refusal `remedy config validate` names, and the guard that refuses a second currency in any
  display; `docs/system/cost-currency-v1.md` (new) is the audit of every money key and display.
- `packages/orchestration/price_catalog.py` (new): the TOML catalog per adapter under
  `packages/orchestration/price_catalog_files/` (the shipped `claude-cli.toml` lists no model), its
  validation, the foreign-currency and unknown-model warnings, staleness, and the update planner.
- `packages/orchestration/call_valuation.py` (new): the `call_valuations` table beside `calls`, the
  basis rules (provider cost wins, the catalog computes `price_table` otherwise and cross-checks,
  unknown says why), the recompute that rewrites only what changed, and the per-basis summary;
  `packages/orchestration/pingpong_evidence.py` values each mirrored call.
- `packages/orchestration/config_keys_budget.py`: `cost.currency`,
  `cost.cross_check_threshold_percent` and `cost.catalog_stale_days`.
- `apps/cli/command_catalog_worker.py` (new): the `worker` group moved out of the held
  `apps/cli/command_catalog.py` first (ratchet row 2255 to 2199, pin 62976 to 62920).
- `remedy worker pricing-update` (`apps/cli/commands/worker_pricing_cmd.py`, new), `remedy stats
  recompute-costs` and `remedy stats valuations` (`apps/cli/commands/stats_valuation_cmd.py`, new);
  `docs/system/price-catalog-v1.md` (new).

## Why

Every budget field spoke dollars, but nothing said so as one rule, no price existed to check a
reported cost against, and a ledger row's cost could not be revalued without rewriting the raw
record. The cross-vendor scoreboard, the customer cost calculator and the counterfactual cost
replay (F159, F222 and F228) need one honest money language to build on.

## Key decisions

- DECISION F158 D1: F153 waits behind the paydown F316, because no session can read the Codex
  command line its research needs.
- DECISION F158 D3: `cost.currency` accepts only usd; no exchange rate is invented.
- DECISION F158 D4: one catalog file per adapter, every price with a required source; the shipped
  catalog is empty because no price source exists on disk and claude-cli reports its own cost.
- DECISION F158 D5: valuations live in their own table, so the `calls` row is never rewritten; a
  deviation strictly above the threshold is flagged and logged, never blocking.
- DECISION F158 D6: `pricing-update` shows the difference first, writes only with `--yes`, and
  refuses a change that does not raise `pricing_version`.
- DECISION F158 D7: the recompute and the summary are two `stats` commands beside
  `backfill-ledger`; staleness is reported there, not in `worker doctor`.

## How to review and test

- `python3 -m pytest -q tests/orchestration/test_cost_currency.py tests/orchestration/test_price_catalog.py tests/orchestration/test_call_valuation.py tests/cli/test_worker_pricing_cmd.py tests/cli/test_stats_valuation_cmd.py`
  — the guard with its violation fixture, the catalog's refusals, the mixed-basis goldens, the
  update's shown difference and the end-to-end with the `calls` digest unchanged.
- The closure's one full suite on `b16e6f296`: `24235 passed, 11 skipped, 1 warning in 364.35s`,
  exit 0 (`.agent/authored/f158-closure-suite.txt`); CPU 1421.53 s, 2.2 % below F162's.
- Evidence job `f158r8e1001` on `18af758db`: `13221 passed, 6 skipped`, exit 0; package
  `remedy-review-20261024-192309-READY_FOR_REVIEW.zip`, SHA-256
  `f095df6c9db88fc7ac379572cf9a0d783f4eb187cdfa68b5123917814fa6451a`.
- The reviewer ran 70 mutations of the production code; all went red, three only after tests the
  reviewer added before delegating.

## Changed files

| Area | Files |
|---|---|
| Production | `packages/orchestration/cost_currency.py` (new), `packages/orchestration/price_catalog.py` (new), `packages/orchestration/price_catalog_files/claude-cli.toml` (new), `packages/orchestration/call_valuation.py` (new), `packages/orchestration/config_keys_budget.py`, `packages/orchestration/pingpong_evidence.py`, `packages/orchestration/lessons.py`, `apps/cli/command_catalog.py`, `apps/cli/command_catalog_worker.py` (new), `apps/cli/command_catalog_stats.py`, `apps/cli/commands/__init__.py`, `apps/cli/commands/config_cmd.py`, `apps/cli/commands/worker_pricing_cmd.py` (new), `apps/cli/commands/stats_valuation_cmd.py` (new) |
| Tests | `tests/orchestration/test_cost_currency.py` (new), `tests/orchestration/test_price_catalog.py` (new), `tests/orchestration/test_call_valuation.py` (new), `tests/cli/test_worker_pricing_cmd.py` (new), `tests/cli/test_stats_valuation_cmd.py` (new), `tests/test_structure_ratchet.py`, the reachability allowlist |
| Docs | `docs/system/cost-currency-v1.md` (new), `docs/system/price-catalog-v1.md` (new), `docs/README.md`, `docs/guides/environment.md`, `docs/guides/do-run-v1.md`, `docs/system/structure-ledger-v1.md`, the checklist's consolidation paragraph, F158's feature file, STATUS, README |
| Records | `.agent/`, `scripts/self_use_queue.json` |

## Verdict

Latest live review: PASS_WITH_RISKS. F158's one finding against its own rounds, R-1471, is
resolved inside the feature. R-1472, self-use runs reaching no token ledger so no real run has yet
recorded a valuation, is owned by F316. Open findings: 11, ten owned by F316 and one by F246.

## Runtime actuals

Two sessions, nine delegated rounds. The self-use run made two priced provider calls, measured by
the job's own budget record; the evidence job's pytest took 1910 s and the full suite 364 s. Token
counts of the planner and worker sessions are not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
