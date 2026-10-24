# F158 findings pass — every place money, prices and currency live today

Read-only investigation at `407536a9b`. Every factual sentence names `path:line` or the command
whose output it read. Section 9's draft is a PROPOSAL, not a decision.

## 1. The token ledger (F103)

One sqlite file per project (`token_ledger.py:519-530 token_ledger_path_for`), holding THREE
tables, not one:

- `calls` — one row per provider call (or, pre-R-0807, one per finalized task run). Columns, in
  order (`token_ledger.py:167-181 _CALL_COLUMNS`, created `token_ledger.py:208-223`): `call_id`,
  `job_id`, `task_id`, `role`, `model`, `ts_utc`, `tokens_in`, `tokens_out`, `cache_read`,
  `cache_write`, `cost_usd`, `cost_basis` (CHECK'd against `COST_BASES`, `token_ledger.py:162-164`),
  `evidence_ref`. No `raw_counters`, `normalized_cost`, `pricing_version` or `basis`-as-exactness
  column exists on `calls` today.
- `call_segments` — one row per composed-prompt segment (`token_ledger.py:235-246`, F115 D4).
- `meta` — one `key`/`value` row per schema generation (`token_ledger.py:202-205`).

**The migration pattern.** `SCHEMA_VERSION = 2` (`token_ledger.py:127`); `_MIGRATIONS` is a dict of
`{version: (sql, ...)}` (`token_ledger.py:199-248`), applied in order by
`_migrate_to_current` (`token_ledger.py:1862-1879`) and read back from `meta` by
`_read_schema_version` (`token_ledger.py:1844-1861`). `test_schema_version_matches_the_last_migration_step`
(`tests/orchestration/test_token_ledger.py:182-186`) pins `max(_MIGRATIONS) == SCHEMA_VERSION`. This
is the ADDITIVE-COLUMN precedent for `calls`/`call_segments` specifically — but two OTHER modules add
whole SEPARATE tables to the same sqlite file instead of a migration step here: `side_role_calls`
(own `CREATE TABLE`, own `meta` key `side_role_calls_schema_version`,
`side_role_calls.py:38-60`) and `tier_outcomes` (own table, own `meta` key
`tier_outcomes_schema_version`, `tier_outcomes.py:40-60`). Both docstrings give the same reason:
"`token_ledger.py` is held at its row of the structure ledger" (`side_role_calls.py:13-15`,
`tier_outcomes.py:18-20`) — `token_ledger.py` is 1879 lines and listed in
`docs/system/structure-ledger-v1.md:476`'s "Files above 1,000 lines" table. Neither docstring
states a numeric ceiling and the structure-ledger doc itself does not define "held" beyond that
table, so I report the fact rather than infer a threshold.

**Writers.** The live hook: `pingpong_evidence.py:495-544`, opt-in and inert without a ledger
target (`:517-520`), calls `record_task_run_calls` (`:526,537`) after re-reading
`provider_evidence.json` through `call_records_from_evidence` — never a second parse of provider
output. `teacher_spend.py:90` is the one other writer (DECISION F255 D7), for a teacher question
that has no task run. `record_call` (`token_ledger.py:559-622`) and `record_task_run_calls`
(`:836-885`) both return `False` on any failure and never raise. The manual path:
`apps/cli/commands/stats_ledger_cmd.py:586-591` (`remedy stats backfill-ledger`) calls
`backfill_ledger`.

**Readers.** `apps/cli/commands/stats_ledger_cmd.py`: `_cmd_stats_cost` (`:346-379`, `remedy stats
cost`), `_cmd_stats_cache` (`:492-507`, `remedy stats cache`), `_cmd_stats_report` (`:508-581`,
`remedy stats report`, also reads `query_segment_shares`), `_cmd_stats_backfill_ledger` (`:582-612`),
`_cmd_stats_verify_ledger` (`:614-...`). Other readers: `job_tokens.py:47` (`query_cost(...,
by="role")`), `do_summary.py:88`, `tier_outcomes.py:155-157` and `side_role_calls.py:138-140`
(`open_ledger`/`token_ledger_path_for` directly, for their own tables).

**Columns that exist under another name.** `cost_usd`/`cost_basis` exist (`calls` columns above).
`raw_counters` exists one layer UP, at the adapter-usage mapping (see §5), never persisted into a
`calls` row. `pricing_version`, `normalized_cost` and a basis value named `catalog_computed` do not
exist anywhere in `packages`/`apps`/`tests` (checked by `git grep`, see §9).

**Tests pinning the schema.** `test_token_ledger.py:182-186` (schema version), `:1672-1683`
(`test_call_segments_columns_mirror_the_manifest`, pins `call_segments`'s columns via `PRAGMA
table_info`). No equivalent `PRAGMA table_info(calls)` pin exists — a `calls`-column addition is
not caught by an explicit column-list test today.

## 2. Prices today

`git grep -il "price|pricing" -- packages apps` names 33 files. None of them holds a per-model or
per-call price FIGURE; every one of them either (a) defines or reads the single operator-configured
scalar below, or (b) uses "price"/"priced"/"unpriced" to mean "did this call report a cost", never a
rate table. The one actual price input in the tree:

- `budget.price_basis_usd_per_1k_tokens` (`config_keys_budget.py:59-68`, env
  `REMEDY_BUDGET_PRICE_BASIS_USD_PER_1K_TOKENS`, `value_type=float`, `default=None` — "DECISION
  F104 D4: an invented price would make every prediction a fabrication"). One scalar, one currency
  (USD, by name only — no `currency` field), no per-model breakdown, no source URL or comment
  anywhere near it. Read by `budget_guard.py:589` and `cost_preview.py:80,100` (as
  `config.price_basis_usd_per_1k_tokens`) and applied by `token_economy.py:101-110
  tokens_to_cost_usd` (`tokens / 1000 * price_basis`). This is a prediction/estimate input
  (`cost_preview.py`'s module docstring, F104), never written to a ledger row.

Representative "consumes, never defines" sites (the remaining 30-ish files read the same way):
`budget_guard.py:589`, `budget_resolution.py:114,152,340-357`, `subtree_rerun.py:267`,
`estimate_calibration.py:12,93,277-281` (prices a CLASS from measured history, not a catalog),
`job_burn.py:7-8`, `order_ledger.py:88-178` ("unpriced" = cost unknown, never free),
`teacher_model.py:128` ("Ollama reports no price"), `do_rehearsal.py:52-99`, `run_report.py:345,645`,
`safe_points.py:608,632-638`, `bench_cmd.py:75,247` ("No price is computed: the bench records token
counts, never money"), `stats_calibration_cmd.py:20`, `client_interface_story.py:87-88`,
`command_catalog_stats.py:65`, `pingpong_provider_fake.py:16`, `job.py:1993-2267`,
`order_intent.py:27` (a verb-parsing docstring example, `"price.js"`, unrelated to money),
`run_contract.py:82` ("NOT real pricing"), `client_digest.py:108`, `budget_clock.py:112-114`,
`budget_profiles.py:22`, `project_cockpit.py` (see §4), `model_trust_score.py` (see §4),
`job_digest.py` (see §4), `side_role_routing.py`/`side_role_calls.py` (see §1/§4),
`tier_outcomes.py` (see §1), `token_ledger.py`/`cost_report.py`/`cost_preview.py` (see §1/§6/§7),
`stats_ledger_cmd.py`/`stats_trust_cmd.py` (see §1/§7), `config_keys_budget.py` (above).

No file defines a model-indexed price table. No price cites a source URL or comment anywhere in
`packages`/`apps`.

## 3. Money fields and currency

`_usd`-suffixed fields found: `cost_usd` (`token_ledger.py` `calls`/`CostRow`/`CallRecord`),
`max_cost_usd` (`packages/core/models.py:23`; `config_keys_budget.py:36-41`
`budget.max_cost_usd`; `:179-218` per-profile `budget.profile.{local,paid}.max_cost_usd`),
`confirm_above_usd` (`config_keys_budget.py:132 cost_preview.confirm_above_usd`, resolved by
`cost_preview.py:120-142 resolve_confirm_above_usd`, read by `job.py:1244-1250`,
`job_rerun_cmd.py:76-97`, `subtree_rerun.py:836-889`), `measured_cost_usd`
(`budget_guard.py:65,133-168 BudgetCounters.measured_cost_usd`; `budget_clock.py:112`;
`job.py:1998,2147`). `git grep -n "EUR"` and `git grep -n "€"` under `packages`/`apps` return
NOTHING — no non-USD currency figure or symbol exists anywhere in the tree.

**Rendering for a human.** `apps/cli/commands/job.py:2245` prints a literal `$` prefix:
`f"  max_cost_usd:          ${_budgets.max_cost_usd:.4f}"`; `:2266` similarly via
`_format_remaining_usd`. `apps/cli/commands/stats_ledger_cmd.py` prints NO `$` symbol — its column
header is the word `"Cost USD"` (`:61`) and `_figure` (`:229-235`) prints a plain decimal or the
`UNMEASURED` word. `tests/cli/test_stats_trust_cmd.py:228` pins a THIRD rendering,
`"$0.0123 (provider_reported, 15 passes)"`, from `stats_trust_cmd.py`. Three CLI surfaces, three
different money-rendering conventions (symbol-prefixed, word-suffixed, symbol-with-basis-suffix);
none currently disagree on currency because only USD exists, but nothing enforces that today — the
feature file's "mixed-display guard" does not exist yet (checked: no file matches
`git grep -n "mixed.*currency\|currency.*guard"` under `packages`/`apps`/`tests`).

`apps/ui/src/` — the feature file's named cockpit rendering surface — does not exist. `apps/ui` was
deleted whole: `git log --oneline -1 -- apps/ui/src` reads `a4d285aaf amend1015 P4.8: apps/ui is
deleted, the wheel stops carrying it, and the smoke loses its UI section` (2026-10-15). `git
ls-files apps/ui` returns zero tracked paths today. Any money-rendering work this feature does has
no cockpit consumer in the current tree.

No other currency (EUR or otherwise) is read, stored or rendered anywhere in `packages`/`apps`.

## 4. Bases today

FOUR independent "basis" vocabularies exist, answering different questions, none named
`catalog_computed`:

1. **`cost_basis` (PROVENANCE of the ledger row, F103).**
   `COST_BASIS_PROVIDER_REPORTED = "provider_reported"`, `COST_BASIS_PRICE_TABLE = "price_table"`,
   `COST_BASIS_UNKNOWN = "unknown"` (`token_ledger.py:157-164`). `price_table` is declared but
   "no code in Remedy writes one" (`token_ledger.py:409-410`'s docstring). Read by every `calls`
   reader in §1.
2. **`cost.basis` (EXACTNESS, DECISION F040 D4).** `COST_BASIS_ACTUAL = "actual"`,
   `COST_BASIS_LOWER_BOUND = "lower_bound"`, `COST_BASIS_ABSENT = "absent"`
   (`job_digest.py:59-67`), explicitly NOT the same question as `BudgetCounters.actual_sources`
   (`job_digest.py:60-64`). Read/written by `project_cockpit.py:20-46` and pinned by
   `tests/orchestration/test_job_digest.py:42-44,445-717` (14+ assertions).
3. **`local_zero` (a local call bought no API tokens).** `COST_BASIS_LOCAL_ZERO = "local_zero"`
   (`side_role_routing.py:47`), used by `side_role_calls.py`'s own `cost_basis` CHECK
   (`:57`, restricted to `local_zero`/`unknown` only — `calls`'s `price_table`/`provider_reported`
   do not apply to a side-role call).
4. **`BudgetCounters.actual_sources` (PROVENANCE of a job's measured counters, not a basis word).**
   `VALID_ACTUAL_SOURCES = {"pingpong_actuals", "pingpong_live", "persisted_job_actuals",
   "token_actuals", "aggregate_actuals"}` (`budget_guard.py:41-44`), validated at
   `budget_guard.py:97-109,738-746,927-940`.

`model_trust_score.py:58-67` DUPLICATES `COST_BASIS_PROVIDER_REPORTED`/`COST_BASIS_UNKNOWN` as its
own module-level constants rather than importing `token_ledger`'s — kept in sync by a pinning test,
`test_cost_basis_constants_match_the_ledgers_own_vocabulary` (named in `model_trust_score.py:58-59`,
AGENTS.md "One spelling per concept"), and adds two more of its own: `TRUST_COST_BASIS_PRICE_TABLE
= "price_table"`, `TRUST_COST_BASIS_TOKENS = "tokens"`, `TRUST_COST_BASIS_MIXED = "mixed"`
(`:65-67`). This equality-test pattern (repeat the constant, pin it equal, rather than share an
import) is the tree's established way of keeping a vocabulary word from drifting across modules
that must not import each other.

`provider_reported`/`unknown` exist (vocabulary 1, widely read: `stats_ledger_cmd.py:15,286,485`,
`model-trust-score-v1.md:51,82`). `catalog_computed` exists NOWHERE (checked, §9) — the tree's
existing word for "priced from a table rather than the provider" is `price_table` (vocabulary 1 and
3 above, plus `docs/system/model-trust-score-v1.md:51`, `docs/roadmap/features/T2_F103.md:27,159`,
`T7_F133.md:106`).

## 5. Usage under the adapter contract (F151)

`AdapterUsage` (`packages/contracts/adapter_contract.py:114-119`): `actuals: UsageActuals`,
`raw_counters: dict`. `raw_counters` is NOT a new idea this feature needs to invent — it already
exists at this layer, non-empty-enforced by `adapter_conformance_kit.py:236-238`. `UsageActuals`
(`packages/orchestration/token_actuals.py:16-38`): `input_tokens`, `output_tokens`, `cache_read`,
`cache_creation`, `total_cost_usd` (`float | None`), plus turn/duration/session/version metadata —
no currency field, no pricing_version field.

The reference adapter, `packages/providers/adapters/claude_cli_reference.py:170-181 map_usage`:
parses the CLI's own JSON via `parse_cli_result_detailed`, then re-reads the SAME payload's
`"usage"` object verbatim into `raw_counters` (`:178-181`) — "the provider's own usage object
unchanged" (`:168-169`'s comment). `total_cost_usd` is the provider-reported cost; there is no
second, computed figure anywhere in this adapter.

No local or HTTP adapter implements `WorkerAdapter` yet — `packages/providers/adapters/` holds only
`claude_cli_reference.py` and `adapter_registry.py`; `map_usage` is not implemented for a local or
HTTP provider under the F151 contract. F113's zero/absent rule for a local call lives one layer
below the contract instead, in `side_role_routing.py:44-47` (basis `local_zero`, "no API tokens
were bought") and `side_role_calls.py:10-12` ("the count is unmeasured... NULL, never... a zero").

## 6. Configuration keys

`ConfigKeySpec` (`packages/orchestration/config_key_spec.py:16-44`): `key`, `env_var`,
`description`, `value_type` (`str`/`int`/`float`/`bool`/`list`/`dict`), `entry_type`, `default`,
`env_only`, `secret`, `fallback_key`. THERE IS NO `choices`/enum FIELD. A "choice-valued" key today
is simply `value_type=str` with the allowed values stated only in `description` prose and enforced
by the CONSUMING code, not the registry — e.g. `claude_cli.sandbox_profile`
(`config_keys_claude.py:59-70`: "strict, standard or net-local", `value_type=str`). A number-valued
key uses `value_type=int` (`budget.max_total_tokens`, `config_keys_budget.py:15-20`) or `float`
(`budget.max_cost_usd`, `:36-41`; `budget.price_basis_usd_per_1k_tokens`, `:59-68`).

`tests/orchestration/test_env_registry.py` pins: every literal env read names a registered
variable (`:125`), every `REMEDY_*` name production code spells is registered (`:129`), every one a
shell script expands is registered (`:133`), every registered name is unique and `REMEDY_`-prefixed
(`:143`), a typed variable round-trips through the registry reader (`:192`).

`docs/guides/environment.md` is a generated table, one row per key: `| ENV_VAR | type-word |
default | key | description |` — e.g. `:40`
(`REMEDY_BUDGET_PRICE_BASIS_USD_PER_1K_TOKENS` / "a number" / none / `budget.price_basis_usd_per_1k_tokens`)
and `:51` (`REMEDY_CLAUDE_CLI_SANDBOX_PROFILE` / "text" / none / `claude_cli.sandbox_profile`).
Generated by `packages/orchestration/config.py`, pinned by `tests/docs/test_environment_guide.py`.

`cost.currency` does not exist as a config key: `git grep -n "cost\.currency"` under
`packages`/`apps` returns nothing; the string appears only in
`docs/roadmap/features/T8_F158.md:24`. No `cost.*` config group exists at all today (`cost_preview.*`
is the nearest group name, holding only `confirm_above_usd`).

## 7. Consumers, warnings and the shown-diff precedent

`apps/cli/commands/stats_ledger_cmd.py` is the main consumer: `_cmd_stats_cost`, `_cmd_stats_cache`,
`_cmd_stats_report` (`remedy stats cost|cache|report`, §1). `cost_report.py:51-52` writes
`cost_report.md`/`cost_report.json` for `remedy stats report`.

**"Scoreboard" does not exist.** `git grep -riln "scoreboard" -- packages apps` returns nothing; the
word appears only in `docs/roadmap/features/T8_F158.md`'s own design prose. The feature file's
"Consumers: the scoreboard and cost stats read normalized_cost + basis" names a module that is not
in the tree.

**Warning events.** No generic warning-event vocabulary for cost exists: `event_names.py` defines
only `"budget.tick"` (`:62`) among budget/cost-adjacent names; no "stale", "deviation" or
"cross-check" event exists anywhere in `packages/orchestration/cost_report.py`,
`token_ledger.py`, `budget_guard.py` or `config_keys_budget.py` (checked, no hits).

**`worker doctor`.** `command_catalog.py:1116 command_id="worker.doctor"` →
`apps/cli/commands/worker.py:248 _cmd_worker_doctor`. It reports sandbox-limit enforcement (F162/
F157); it carries no cost, price or staleness content today.

**The shown-diff / baselines-update pattern.** Named only in planned feature files, never built:
`docs/roadmap/features/T6_F098.md:21,73,89` (`remedy baselines update`, F098 status `[ ]` —
unclaimed, `docs/roadmap/STATUS.md:420`), `T11_F188.md:58` (`api-baselines update`), `T9_F172.md:46,57`.
`git grep -n "unified_diff" -- apps/cli/commands scripts` returns nothing — no CLI command in the
tree today shows a diff before writing. The nearest BUILT precedent is a threshold confirmation,
not a diff: `cost_preview_confirm.py:36,71` and `subtree_rerun.py:854-889` gate on
`estimate.band_usd_high > confirm_above_usd`, prompting only above a dollar figure, never rendering
a diff of what changes.

**`worker pricing`.** `git grep -rn "worker pricing\|\"pricing\"" -- apps/cli` returns nothing — no
such command exists.

## 8. Guards, ledgers and file homes

**Structure ledger.** `token_ledger.py` — 1879 lines, in `docs/system/structure-ledger-v1.md:476`'s
"Files above 1,000 lines" table (see §1 for the consequence other modules draw from this).
`budget_guard.py` carries two named-function rows: `evaluate_budget` (`:402`) and
`decode_persisted_budget_actuals` (`:404`). `config_key_spec.py`/`config_keys_budget.py`'s split is
narrated at `structure-ledger-v1.md:263,272` (F310, `ConfigKeySpec` moved out of `config.py`; the
budget group moved out at step (6)). None of `job_digest.py`, `side_role_routing.py`,
`side_role_calls.py`, `tier_outcomes.py`, `cost_report.py`, `cost_preview.py`,
`adapter_contract.py` or `claude_cli_reference.py` appear in either named-function table or the
over-1000-lines table — they are not currently flagged by the structure ledger.

**New-module guards.** `tests/orchestration/import_reachability_allowlist.txt` is a 470-line
GENERATED allowlist (header, `:1-5`: "never typed by hand... a deletion round removes an entry in
the same commit that removes its module"), computed by
`tests/orchestration/test_import_reachability.py`. `tests/test_no_orphan_modules.py` asserts every
module is reachable from six entry points (`:253 test_no_module_is_an_orphan`) and that every
deliberately-unwired exception carries a stated reason (`:298`). A new T002/T003 module (a catalog
loader, a `pricing` writer) will need an entry in both, or a reachable import from an existing
entry point.

**`tests/workers/` does not exist** — `ls tests/workers/` fails (`No such file or directory`). The
feature file's suggested `tests/workers/test_pricing.py` (`docs/roadmap/features/T8_F158.md:87`)
would be the first file in a new test directory.

**Package data precedent (F162).** `packages/orchestration/sandbox_profiles.py:53`:
`_PROFILE_FILES_DIR = Path(__file__).resolve().parent / "sandbox_profile_files"` — a plain
filesystem path relative to the module's own `__file__`, not `importlib.resources`. The three files
(`strict.toml`, `standard.toml`, `net-local.toml`) ship with no explicit `package_data`/`include`
entry in `pyproject.toml` (`git grep -n "sandbox_profile_files\|package.data\|package_data"
pyproject.toml` returns nothing): `pyproject.toml:24 packages = ["packages", "apps"]` is
hatchling's wheel target, and hatchling's default is to include every file under a declared package
directory unless excluded — this is presumably how the TOML files ship, but no explicit opt-in for
them was found, so a T002 catalog under `packages/orchestration/` should expect to rely on, and
verify, the same implicit inclusion rather than a declared one.

## 9. Names, a draft, and where the design does not match the tree

**Grep results (`packages`/`apps`/`tests`, `407536a9b`), each checked separately:**

| Name | In code today? |
|---|---|
| `pricing_version` | No — only in `docs/roadmap/features/T12_F197.md:11`, `T8_F158.md:8,28,31` |
| `normalized_cost` | No — only in `T8_F158.md:28,33,52` |
| `raw_counters` | YES — `adapter_contract.py:119`, widely used/tested (§5) |
| `catalog_computed` | No — only in `T8_F158.md:9,44` |
| `provider_reported` | YES — `token_ledger.py:157`, `model_trust_score.py:63`, `tier_outcomes.py:120`, tests (§4) |
| `price_catalog` | No — zero hits anywhere, including the feature file's own prose |
| `cost.currency` | No — only in `T8_F158.md:24` |
| `pricing/` (repo-root dir) | No — `ls pricing` fails |

**Proposed T001 audit list** (every USD-shaped site a currency key would need to reach, from §3):
`budget.max_cost_usd` + the two `budget.profile.*.max_cost_usd` keys, `budget.price_basis_usd_per_1k_tokens`,
`cost_preview.confirm_above_usd`, `token_ledger.calls.cost_usd`, `BudgetCounters.measured_cost_usd`,
`packages/core/models.py:23 max_cost_usd`, `job.py`'s `$`-prefixed render, `stats_ledger_cmd.py`'s
`"Cost USD"`-headed render, `stats_trust_cmd.py`'s `"$...(basis, n passes)"` render. The cockpit
render (`apps/ui/src/`) is OUT OF SCOPE — it does not exist (§3).

**Proposed catalog shape and home (a proposal only).** Given `token_ledger.py` is already at its
structure-ledger row (§1/§8) and the tree's established answer to "a new cost concept needs a home"
is a NEW MODULE with its OWN table in the SAME sqlite file (`side_role_calls.py`, `tier_outcomes.py`)
rather than a new column on `calls`, T002 should default to the same shape: a new module (e.g.
`packages/orchestration/price_catalog.py`) owning its own `meta` schema key, rather than widening
`_CALL_COLUMNS`. The catalog FILES themselves can follow F162's precedent (§8): TOML under a
`*_files/` directory beside the owning module, loaded by a plain `Path(__file__).parent` join, no
new `pyproject.toml` entry expected to be needed.

**Proposed basis word.** Reuse `price_table` (vocabulary 1 in §4) rather than add `catalog_computed`
as a second spelling of the same idea — the Code Discoverability convention (AGENTS.md) states "one
spelling per concept repo-wide. No synonym drift," and `price_table` already greps cleanly across
`token_ledger.py`, `model_trust_score.py` and two feature files (T2_F103, T7_F133) that F158 depends
on or sits beside.

**Where the feature file's design does not match the tree (marked, not decided):**
1. "the cockpit under `apps/ui/src/`" — `apps/ui` was deleted whole on 2026-10-15 (§3); no cockpit
   consumer exists for this feature's output.
2. "the scoreboard... read normalized_cost + basis" — no `scoreboard` module or concept exists
   anywhere in `packages`/`apps` (§7).
3. "basis (provider_reported | catalog_computed)" — `catalog_computed` greps to nothing; the tree's
   own word for this exact idea, already wired in three modules, is `price_table` (§4, §9 table).
4. "`pricing/<adapter>.toml` in-repo" at the repository root — no `pricing/` directory exists; the
   tree's only precedent for shipping adapter-scoped TOML data is a package-internal
   `*_files/` directory beside the owning module (§8), not a top-level folder.
5. "ledger rows gain raw_counters{}" — `raw_counters` is not a new idea to invent; it already
   exists one layer up, at `AdapterUsage.raw_counters` (§5), and is simply not yet threaded down
   into a `calls` row.
6. "`cost.currency`, default usd" — no `cost.*` config group exists today (§6); the nearest
   existing group is `cost_preview.*`, holding only `confirm_above_usd`.
7. "the baselines-update pattern (shown diff)" — named only in OTHER unbuilt feature files
   (F098, F188); no command in the tree renders a diff before writing anything today (§7); the
   built precedent that exists is a threshold confirmation, not a diff.
