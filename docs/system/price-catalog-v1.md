# Price catalogs and call valuations (v1)

Since F158 (DECISIONs F158 D4 to D7) every provider call the token ledger mirrors is also valued in
the one configured currency (see [cost-currency-v1.md](cost-currency-v1.md)), with the basis that
value rests on. Code: `packages/orchestration/price_catalog.py`,
`packages/orchestration/call_valuation.py`, the commands in
`apps/cli/commands/worker_pricing_cmd.py` and `apps/cli/commands/stats_valuation_cmd.py`. Tests:
`tests/orchestration/test_price_catalog.py`, `tests/orchestration/test_call_valuation.py`,
`tests/cli/test_worker_pricing_cmd.py` and `tests/cli/test_stats_valuation_cmd.py`.

## The catalogs

Each worker adapter may have one catalog,
`packages/orchestration/price_catalog_files/<adapter>.toml`, named after the adapter's
`adapter_ref`. It holds a `[catalog]` table with `adapter` and `pricing_version`, and one
`[models."<model id>"]` table per priced model with four prices per million tokens
(`input_per_million`, `output_per_million`, `cache_read_per_million`,
`cache_write_per_million`), a lower-case `currency` code, a `valid_from` date and a `source` naming
where the prices were read. A malformed entry refuses the whole file. A model id Remedy does not
ship, and a price in a currency other than `cost.currency`, are warnings, not refusals.

The shipped `claude-cli.toml` lists no model, on purpose: Remedy records a price only with a source
a reviewer can open, and the claude command line reports each call's cost itself.

## Importing a catalog

`remedy worker pricing-update <file>` checks a maintained catalog against every rule above, prints
the difference to the current catalog, and writes nothing. Running it again with `--yes` writes
the file. A catalog that changes anything must raise `pricing_version` above the current one, so
every valuation keeps naming the prices it used; an unchanged import writes nothing.
`--catalog-dir <folder>` reads and writes another folder of catalogs.

## How a call is valued

| Situation | Normalized cost | Basis |
|---|---|---|
| the provider reported the cost | that cost | `provider_reported` |
| ... and one catalog also prices the call | that cost; the catalog's figure is kept beside it, and a difference beyond `cost.cross_check_threshold_percent` (default 5) is flagged and logged as a warning | `provider_reported` |
| no reported cost, one catalog prices the model in the configured currency and all four token counts are known | the counts times the prices | `price_table` |
| anything else: no model, no catalog lists it, two catalogs do, a foreign currency, or a missing count | unknown, with a note saying which | `unknown` |

The valuation is a row of the ledger's `call_valuations` table, beside the call's `calls` row,
which F158 never writes: the token counts and the reported cost stay what the provider reported.
Remedy deliberately invents no exchange rate, never prices a missing token count as zero, and never
picks one of two catalogs that list the same model.

## Reading and recomputing

`remedy stats valuations` prints, per basis, the calls and their normalized cost — never one figure
blended across bases — then a warning for every flagged call and for every catalog price older
than `cost.catalog_stale_days` (default 60). A stale price is still used; nothing is blocked.

`remedy stats recompute-costs` values every call of a project's ledger again, for example after a
catalog import, and rewrites only the valuations that changed. A second run over the same catalogs
rewrites nothing.
