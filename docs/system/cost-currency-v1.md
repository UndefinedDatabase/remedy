# One currency for every cost (v1)

Since F158 T001 (DECISION F158 D3) Remedy states every cost figure in one configured currency, the
`cost.currency` key, which budgets, cost previews, the token ledger and the price catalog share.
Code: `packages/orchestration/cost_currency.py`; the key: `packages/orchestration/config_keys_budget.py`;
tests: `tests/orchestration/test_cost_currency.py`.

## The rule

`cost.currency` defaults to `usd`, and `usd` is the only value Remedy accepts while every budget
field it ships is a USD field. Any other value is refused by name: `remedy config validate` reports
`cost.currency '<value>' is not accepted`, names the budget fields that make it so, and says the
configuration is not valid. Remedy deliberately does not convert between currencies on its own: a
price stated in another currency is converted only through a rate the operator configures, or left
unnormalized with a note, and no exchange rate is ever invented.

A display that prints a second currency beside dollar figures is forbidden. The mixed-currency
guard in `tests/orchestration/test_cost_currency.py` reads the string literals of every Python file
under `packages/` and `apps/` and fails on any foreign currency symbol (such as the euro or pound
sign) or upper-case ISO code (such as EUR or GBP). The one exempt file is `cost_currency.py`
itself, whose table of those markers is what the guard searches for.

## Dollars are hidden by default

Since operator amendment amend1024-one-real-order Part E Remedy shows tokens and provider calls,
not dollars. Every output of `remedy stats`, `remedy job show`, `remedy do` and the public HTTP API
shows a dollar figure only when `cost.show_usd = true` is set in `remedy.toml` (or
`REMEDY_COST_SHOW_USD=true`); the key defaults to `false`. The dollar calculation itself is
unchanged: the ledger, the price catalog and the valuations still record every figure, and setting
the key brings back exactly the output Remedy printed before.

One rule applies to every JSON answer while the key is false, through
`cost_currency.visible_cost_usd`: every field whose name ends in `_usd` keeps its key and reads
`null`, so a client's key sets and the machine contract do not change. A limit the operator set,
such as `max_cost_usd`, `cap_usd` or `confirm_above_usd`, is not a measured cost and stays, and so
does the `show_cost_usd` flag that `remedy do`'s `cost` object and the job digest's `tokens` carry,
which says which reading the answer holds. A `basis` beside a nulled figure still says whether the
cost was measured. The few money fields not named `*_usd` follow the same rule by hand: the job
digest's `cost.value` reads `not-shown`, a money `cost_per_pass` of `remedy stats trust` and the
`normalized_cost` and `catalog_cost` of `remedy stats valuations` read `null`. A text output leaves
its dollar column out, or prints `not-shown` where the figure would stand, and says how to show it.
The key replaced the per-project `[cockpit] show_cost_usd` switch of `.remedy/config.toml`
(amend1015 D7), which nothing reads any more.

## The audit (2026-10-24, at `407536a9b`)

Every place a money figure lives or is shown, the currency it is in, and how it stands against the
rule. No figure in the tree was in another currency, so no figure changed; the audit is the record
that each one was checked. Source: the reviewed findings pass `.agent/f158_inventory.md`.

## Configuration keys

| Key | Currency | Standing |
|---|---|---|
| `cost.currency` | names it | the key itself; default and only accepted value `usd` |
| `budget.max_cost_usd` | USD | aligned: the job cost limit |
| `budget.profile.paid.max_cost_usd` | USD | aligned: the paid profile's default cost limit |
| `budget.price_basis_usd_per_1k_tokens` | USD | aligned: the provisional prediction price, unset by default |
| `cost_preview.confirm_above_usd` | USD | aligned: the confirmation threshold of a cost preview |
| `autonomy.idea_usd_per_day` | USD | aligned: the daily estimated-cost limit of idea drafts autonomy starts on its own |
| `cost.show_usd` | none: a switch | whether dollar figures are shown at all; default `false` (amend1024 Part E, above) |

`tests/orchestration/test_cost_currency.py` fails when a registered key with `_usd` in its name is
missing from this table, or when a row names a key the registry does not hold.

## Fields, columns and displays

| Site | Currency | Standing |
|---|---|---|
| `max_cost_usd` in `packages/core/models.py` | USD | aligned: the job budget field |
| `BudgetCounters.measured_cost_usd` in `packages/orchestration/budget_guard.py` | USD | aligned: a job's measured cost |
| the `calls.cost_usd` column of the token ledger (`packages/orchestration/token_ledger.py`) | USD | aligned: the provider-reported cost of a call |
| `remedy job` budget lines (`apps/cli/commands/job.py`) | USD | aligned: printed with a `$` sign |
| `remedy stats cost` (`apps/cli/commands/stats_ledger_cmd.py`) | USD | aligned: the column header reads `Cost USD` |
| `remedy stats trust` (`apps/cli/commands/stats_trust_cmd.py`) | USD | aligned: printed with a `$` sign and the basis |

The three command-line renderings differ in form — a `$` sign, a `Cost USD` header, a `$` sign with
the basis — and agree on the currency, which is what the rule requires; their form is left as it
is. The cockpit that once rendered costs was deleted with `apps/ui` on 2026-10-15, so it has no row.
