# F022 Cost Inventory — measured, not read off the feature file

Every reading below was taken at commit `aead9822`, the C3 commit of F022 R3, in
the primary checkout on `feature/f022-live-cost-ticker`. No commit of this round
touches a path outside `.agent/`: `git diff --name-only 66f87edc..aead9822`
lists 5 paths and 0 of them fall outside `.agent/`, so every source reading here
is equally a reading at the round base `66f87edc`.

This file cites `path:line` for every row. It deliberately cites NO row to
`docs/roadmap/features/T5_F022.md`: that file states its preconditions as
settled fact, which is the R-0612 class, and the point of this inventory is to
measure the ground instead of quoting the plan.

## (a) Where spent-vs-limits is evaluated

Set definition, semantic and not a grep (R-0492): every `ast.Call` node in
`apps/**`, `packages/**`, `tests/**` and `scripts/**` whose callee resolves to
the name `evaluate_budget`, excluding the `def` itself. The grep candidate list
was wider — it also matches prose in docstrings, comments and `.md` state files
— so the AST predicate is the set and the grep was only the shortlist.

MEASURED: 4 production call sites in `apps/**` and `packages/**`. That agrees
with the R3 block's stated 4, and with its split of one in
`packages/orchestration/safe_points.py` and three in `apps/cli/commands/job.py`.
Repo-wide the same predicate finds 51 call sites, the other 47 being in
`tests/**`; the block named only the production 4, and both numbers are correct
under their own scope.

The definition itself: `packages/orchestration/budget_guard.py:254`,
`def evaluate_budget(budgets, counters, *, now=None) -> BudgetEvaluation`.

| # | path:line | enclosing symbol | what it does with the returned `BudgetEvaluation` |
|---|---|---|---|
| 1 | `packages/orchestration/safe_points.py:616` | `should_stop` | Reads `.exhausted` only. On true it builds `ShouldStopResult(should_stop=True, reason=f"budget_exhausted:{limit}", source="budget", budget_evaluation=evaluation)` with `limit = evaluation.first_exhausted_limit or "unknown"` (lines 617-624). The evaluation object is carried on the result but no field other than `.exhausted` and `.first_exhausted_limit` is read here. |
| 2 | `apps/cli/commands/job.py:2127` | `_cmd_job_budget` | JobPlan branch. Assigns `evaluation` after decoding persisted budget actuals; guarded by `if _budgets is not None`. On any exception the branch sets `_counter_status = "corrupt"` and `evaluation = None` (lines 2129-2133). |
| 3 | `apps/cli/commands/job.py:2172` | `_cmd_job_budget` | Core-Job branch, reached only when `_found_as is None` resolved the id as a Core Job. Same decode-then-evaluate shape, same corrupt fallback at lines 2174-2178. |
| 4 | `apps/cli/commands/job.py:2221` | `_cmd_job_budget` | RE-evaluation after the ledger cost read. Only entered when `_has_cost_limit and counters is not None and counters.measured_cost_usd is None` (line 2203): `collect_ledger_cost_for_job` supplies `measured_cost_usd`, `priced_call_count` and `unpriced_call_count`, the counters are rebuilt with `dataclasses.replace`, and the budget is evaluated a second time against the money-bearing counters. |

All three `job.py` sites feed ONE consumer pair, both inside `_cmd_job_budget`:
`apps/cli/commands/job.py:2289` serialises `evaluation.to_json()` for
`--json`, and `apps/cli/commands/job.py:2340-2346` prints `exhausted`,
`first_exhausted_limit`, `source_descriptions` and `warnings` as text.

### What the evaluation actually carries

`packages/orchestration/budget_guard.py:216`, `class BudgetEvaluation`, a frozen
result with fields at lines 219-227: `configured_limits: JobBudgets | None`,
`counters: BudgetCounters`, `exhausted: bool`, `first_exhausted_limit`,
`token_lower_bound: bool`, `cost_lower_bound: bool`, `warnings` and
`source_descriptions`. `to_json` at line 229 emits all eight.

Three consequences for the tick envelope, each measured rather than assumed:

- SPENT and LIMIT are both already reachable at every one of the four sites —
  the limit through `configured_limits`, the spend through `counters` — so a
  tick emitter needs no new arithmetic home.
- BASIS already exists in two separate boolean flags, not one vocabulary:
  `token_lower_bound` (line 223) and `cost_lower_bound` (line 225, whose comment
  reads "True when the cost figure is a floor, not a total: some call was
  unpriced"). Any basis vocabulary F022 rules in R4 must reconcile with these
  two booleans, which are the existing spelling of the same idea.
- `_LIMIT_ORDER` at `packages/orchestration/budget_guard.py:245` fixes the
  precedence `max_provider_calls`, `max_total_tokens`, `max_cost_usd`,
  `max_wall_clock_minutes`, `deadline`. `first_exhausted_limit` is a member of
  that tuple, so a cost limit is only one of five and a job may be
  budget-limited with no money limit at all.

The money reader for the terminal reconciliation already exists:
`collect_ledger_cost_for_job` at `packages/orchestration/budget_guard.py:645`,
called at `apps/cli/commands/job.py:2213`. The comment at
`apps/cli/commands/job.py:2189-2196` records that the persisted budget-actuals
record carries NO cost field and that the ledger is the only place a real
provider cost lives, and that a failed read leaves the cost UNMEASURED — `None`,
never `0.0`.

## (b) The event-kind vocabulary the ledger and the stream carry today

### The SSE transport enumerates nothing

`packages/orchestration/ui_server.py:2748`, `_safe_event_summary`, returns the
envelope `{seq, event, timestamp, outcome, task_id}` (lines 2769-2775). Its
`event` field is `event.get("event", "")` — the ledger's own event name passed
through unvalidated against any list. `sse_event_frame` at line 2778 emits
`id: <seq>` and `data: <json>` and NO SSE `event:` field; `sse_heartbeat_frame`
at line 2783 emits the comment `: heartbeat`. Its docstring states a comment
carries no `id:`, `event:` or `data:` field. So on the transport there is no
kind whitelist to extend, which is what the R3 context file's additive-kind
assumption depends on.

The docstring at `packages/orchestration/ui_server.py:2749-2755` states that the
cursor endpoint and the SSE stream are one consumer contract over two transports
and that this summary has ONE writer, so a field added there reaches both or
neither. A tick payload richer than `{seq, event, timestamp, outcome, task_id}`
therefore changes both transports at once, by construction.

### The statically enumerable vocabulary: 83 kinds, on both sides, equal

Measured by executing the extractors that `tests/ui_contracts/test_humanize_catalog.py`
itself defines, against the tree at `aead9822`:

| source | path:line that DEFINES it | count |
|---|---|---|
| call-site string literals passed as the event argument, walked over `packages`, `apps`, `scripts` | `tests/ui_contracts/test_humanize_catalog.py:92` (`emission_literals`), roots at line 33 | 60 |
| `TRACE_EVENT_KINDS` | `packages/orchestration/agent_run_trace.py:17` | 16 |
| `_STREAM_EVENT_KINDS`, its VALUES | `packages/orchestration/agent_run_trace.py:184` | 6 |
| `COMMAND_ACCEPTED_EVENT` | `packages/orchestration/ui_server.py:3119` (`"command.accepted"`) | 1 |
| union of the four = the Python-side vocabulary | `tests/ui_contracts/test_humanize_catalog.py:157` | 83 |
| `STREAM_EVENT_CATALOG`, the TypeScript side | `apps/ui/src/api/humanizeCatalog.ts:8`, entries on lines 9-91 | 83 |

The two sets are EQUAL: the extractor reports `catalog == vocabulary: True`, and
the pin is `tests/ui_contracts/test_humanize_catalog.py:222`,
`test_catalog_keys_equal_the_static_stream_vocabulary`.

GATE CONSEQUENCE, and the sharpest thing this inventory found: the catalog's own
header comment at `apps/ui/src/api/humanizeCatalog.ts:5-6` states that adding a
Python emitter without adding an entry there goes red, and so does the reverse.
`tests/ui_contracts/` is NOT in the R3 block's G11 suite list. Any round that
emits a `budget`-named event from Python must therefore add the matching catalog
key in the same commit AND gate `tests/ui_contracts/test_humanize_catalog.py`,
or it lands a red suite it never ran.

The vocabulary is not statically complete: `apps/ui/src/api/humanize.ts:16-18`
states that eleven run-log writers compute their event name at runtime, so
`humanizeStreamEvent` at line 19 renders an unrecognised kind as `${kind} event`
with `known: false` rather than dropping it. `feedRowOf` at
`apps/ui/src/api/feedRow.ts:50` is total by construction for the same reason.

### Is there a `budget`-prefixed kind anywhere? No.

MEASURED over the 83-kind vocabulary and over the catalog keys alike: kinds
beginning `budget` = the EMPTY set, under a case-insensitive prefix test on both
sets. The only kind CONTAINING the substring is `context_budget_optimized`
(`apps/ui/src/api/humanizeCatalog.ts:20`), whose rendered line is "The context
budget was optimized to fit the prompt." — a prompt-token concern and not money.
So `budget.tick`, or whatever R4 names it, is genuinely additive and collides
with nothing.

The `command.accepted` kind is the precedent for a DOTTED name: the vocabulary
already contains one, at `packages/orchestration/ui_server.py:3119`, so a dotted
`budget.tick` needs no new naming rule.

### The other, smaller vocabulary — the timeline, not the stream

The R3 block's section (b) named `RemedyTimelineEventKind` in
`apps/ui/src/api/types.ts` as three literals. That reproduces exactly:
`apps/ui/src/api/types.ts:79`,
`export type RemedyTimelineEventKind = "llm_action" | "test" | "review";`, with
the runtime guard `VALID_TIMELINE_KINDS` at `apps/ui/src/api/remedyApi.ts:448`
carrying the same three and `normalizeTimelineEventKind` at line 455 defaulting
anything else to `"llm_action"`.

DECLARED DISAGREEMENT WITH THE BLOCK, reported and not reconciled (constraint
8): this is a DIFFERENT vocabulary from the one the live stream carries, and it
is the smaller of the two. It is produced by `_build_timeline_events` at
`packages/orchestration/ui_server.py:386`, whose `_event_map` at lines 392-401
maps 7 ledger event names onto those 3 kinds and CONTINUES past anything
unmapped (line 408-409). The block's (b) named only this one; the stream feed
that a live cost ticker would ride on uses the 83-key catalog above. Both
readings are correct; their scopes differ. R4 should be explicit about which of
the two it is extending — on the measured evidence the answer is the 83-key
stream catalog, and the 3-kind timeline union is a separate decision.

## (c) What the metrics bar renders today

`apps/ui/src/components/metrics/TopMetricsBar.tsx`, 100 lines at `aead9822`.

MEASURED, case-insensitive, in that file: `cost` = 0, `spent` = 0, `usd` = 0.
That agrees with the R3 block's stated 0 for all three. The sibling
`TopMetricsBar.module.css` also reads 0, 0, 0. Repo-wide in `apps/ui/src` the
four case-insensitive matches that do exist are all incidental — "costs one
state write per second" at `apps/ui/src/components/panels/AgentNowCard.tsx:13`,
"then discards costs a closure" at `apps/ui/src/api/brainStreamSession.ts:25`,
and a local variable `spent` at `apps/ui/src/api/brainStreamHost.ts:67` and `:69`.
There is no money vocabulary in this UI at all.

The component is GENERIC: it renders `metrics.map(...)` at line 47 over whatever
`RemedyMetric[]` it is handed and hardcodes no metric list. The rendered metrics
are therefore fixed by the array at `apps/ui/src/api/remedyApi.ts:87-95`:

| metric | key | prop it reads | path:line |
|---|---|---|---|
| Open | `open` | `dm.open ?? 0` | `apps/ui/src/api/remedyApi.ts:88` |
| Planned | `planned` | `dm.planned ?? 0` | `apps/ui/src/api/remedyApi.ts:89` |
| Done | `done` | `dm.done ?? 0` | `apps/ui/src/api/remedyApi.ts:90` |
| Progress | `progress` | `dm.progress_percent ?? 0`, `suffix: "%"` | `apps/ui/src/api/remedyApi.ts:91` |
| Tests | `tests` | `metricTests(dm.tests)` — value = passed runs, `state` = latest outcome | `apps/ui/src/api/remedyApi.ts:92`, builder at `:186` |
| Proof | `proof` | `metricProof(dm.proof)` | `apps/ui/src/api/remedyApi.ts:93`, builder at `:193` |
| Tokens | `tokens` | `tu.known ? tu.total_tokens : "—"`, plus `tooltip: tu.by_role` and `unknown` | `apps/ui/src/api/remedyApi.ts:94`, inputs at `:83-86` |

Seven metrics. `iconByKey` at `apps/ui/src/components/metrics/TopMetricsBar.tsx:9-17`
carries exactly those seven keys and falls back to `ChartGlyph` at line 48, so an
eighth key renders with a generic icon rather than crashing.

### The three shapes a COST metric collides with

1. `RemedyMetricKey` at `apps/ui/src/api/types.ts:3` is a CLOSED union of the
   same seven strings. A cost metric widens that union; it is not additive at
   the type level.
2. `RemedyMetric.value` at `apps/ui/src/api/types.ts:8` is `number | "—"`. There
   is nowhere in the current shape to put a limit, a basis or a warn state:
   `suffix` is a display string, `tooltip` is `Record<string, number>`, `state`
   is `"pass" | "fail" | "none"` and `unknown` is a boolean. The `{spent, limit,
   basis}` triple the plan's Goal names does not fit `RemedyMetric` as it stands.
3. The bar fill already has a precedent and it is `progress`-only:
   `progressWidth` at `apps/ui/src/components/metrics/TopMetricsBar.tsx:53` is
   `Math.min(m.value, 100)` and the track at lines 78-82 renders only when
   `m.key === "progress"`. A cost fill against a limit either reuses that branch
   by widening its key test or gets its own.

The "estimated" label precedent for a basis marker is at line 83 and is
`tokens`-only: `{isTokens && main !== EM_DASH && <div className={styles.estimated}>estimated</div>}`.
The tooltip machinery at lines 85-94 is already generic over `m.tooltip`, keyed
by `role`, and is gated on `m.tooltip` being present.

### The backend side of the same seam

The `metrics` dict the UI reads has TWO producers, both in
`packages/orchestration/ui_server.py`:
`_build_dashboard` at line 1919 and `_build_job_plan_dashboard` at line 1637.
Neither carries a cost key today: `_build_dashboard`'s dict at lines 1919-1928
holds `open`, `planned`, `done`, `progress_percent`, `source_counts`,
`computed_from`, `tests` and `proof`. `token_usage` is a SIBLING of `metrics`
rather than a member, at line 1954 via `_build_token_usage`
(`packages/orchestration/ui_server.py:2192`) — which is the shape precedent for
a cost section: the Tokens metric is assembled in the client at
`apps/ui/src/api/remedyApi.ts:94` from a top-level dashboard section, not from
`metrics`. A cost metric can follow either pattern, and the token one is the
closer analogue because it carries a known/unknown flag.

`apps/ui/src/components/shell/RemedyShell.tsx:48` is the single mount point,
`<TopMetricsBar metrics={dashboard.metrics} />`.

## Measured disagreements with the R3 block

Reported, never reconciled, per constraint 8.

1. Section (a) count: block says 4, I measure 4 production sites. AGREES. The
   repo-wide figure under the same AST predicate is 51, the extra 47 being test
   call sites; the block's scope was production and both figures stand.
2. Section (b): block named `RemedyTimelineEventKind` and its 3 literals, which
   reproduces exactly. I additionally measured a SECOND and larger vocabulary,
   the 83-key `STREAM_EVENT_CATALOG` / static-stream-vocabulary pair, which is
   the one the live SSE feed actually carries. The block's reading is correct
   and incomplete for F022's purpose; no number in it is wrong.
3. Section (c): block says 0 for `cost`, `spent` and `usd` in `TopMetricsBar.tsx`.
   I measure 0, 0, 0. AGREES.
