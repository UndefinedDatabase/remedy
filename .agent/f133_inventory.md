# F133 T001 — inventory of trust sources and per-model aggregations

Read at `main` `11fda065b` unless a line names a different commit. Every factual sentence names
`path:line`. Section 6 is a proposal for DECISION F133 D2, not a decision.

## 1. The deleted pair

`packages/orchestration/provider_trust.py` (1058 lines) and
`packages/orchestration/provider_trust_verification.py` (1020 lines) were deleted at `0242c0a3b`
("F275 R22 C4: delete the provider trust pair, its handler and the whole provider command group...",
2026-09-10), read via `git show 0242c0a3b^:<path>`.

**What they computed.** `provider_trust.py` (pre-deletion) was "Provider Trust Gate + External Repair
Intake v0" (its docstring, lines 2-10): a safety/intake gate over a candidate repair patch produced
OUTSIDE Remedy — secret scan, path safety, patch shape, failure linkage — ending in a
`ProviderTrustReport` keyed by `quarantine_id`/`report_id`/`job_id` (its dataclasses,
`ProviderOutputQuarantineRecord`, `ProviderTrustReport`). `provider_trust_verification.py` was a
second-stage plausibility/relevance/scope check layered on the same candidate (its docstring, lines
2-10), importing `provider_trust`'s parser and scanner directly (its import block, lines 44-51).
Both are keyed by CANDIDATE and JOB, never by model or role; neither computed a pass rate, a repair
count, a format-error rate or a cost figure.

**Who consumed them at deletion** (from the deletion commit's file list): the whole
`apps/cli/commands/provider_cmd.py` command group (170 lines, deleted entirely);
`apps/cli/commands/repair_cmd.py`; `packages/orchestration/orchestrator_brain.py`;
`packages/orchestration/provider_patch_material.py`; `packages/orchestration/repair_request_builder.py`;
`packages/orchestration/run_contract.py`; `packages/orchestration/self_dogfood.py`;
`packages/orchestration/self_dogfood_execution.py`; and their four now-deleted test files under
`tests/cli/` and `tests/orchestration/`.

**Every surviving reference today** (`grep -rn provider_trust packages apps docs tests`):
- `packages/orchestration/self_dogfood_execution.py:167,195` — `provider_trust_report_id: str = ""`,
  a field of `SelfImprovementLinkage` and `SelfImprovementAttempt`; `:179,217` export it to JSON.
  No production code assigns it (`grep -rn "provider_trust_report_id\s*=" packages apps tests` finds
  only the two declarations above), so it is always the empty string.
- `packages/orchestration/self_dogfood_execution.py:677` — a comment: "the trust reports of
  `packages.orchestration.provider_trust`. That module, its Trust Gate and its `provider
  intake-repair` command are deleted, so no candidate can enter and is left to link."
- `docs/roadmap/features/T2_F260.md:335-336`, `docs/roadmap/features/T2_F272.md:744`,
  `docs/roadmap/features/T2_F274.md:157` — roadmap prose about the F275/F260 deletion cluster, not code.
- `docs/roadmap/features/T7_F133.md:16,59,92` — this feature's own file (the claim this file
  corrects, and the correction).

## 2. Sources per metric

### pass_quota — a task's terminal outcome AND the model that served each role

**Terminal outcome.** `TaskEntry.status` (`packages/orchestration/pingpong_job.py:215`, default
`TASK_PENDING`) is the field a job's `tasks[]` carries in `jobs/<job_id>/job.json`. The PASS set is
`TASK_DONE_STATUSES = frozenset({TASK_PASSED, TASK_APPLIED, RunState.COMPLETED.value})`
(`pingpong_job.py:75`, with `TASK_PASSED`/`TASK_APPLIED` at `pingpong_job.py:58-59`); `job_evidence.py`
treats the same two literal statuses as `outcome="pass"` at `job_evidence.py:1100-1101`.

**The model that served a role.** NOT on `TaskEntry`. `TaskEntry.model_override`
(`pingpong_job.py:265`) and `job.execution_config.builder_model`/`reviewer_model`
(`pingpong_job.py:2565-2566`) are the CONFIGURED ask, not the model that ran — `token_ledger.py:152-153`
states this directly: "configured models are not it." The model that actually served a call is the
`calls.model` column of the ledger (`token_ledger.py:171-172,213`), written per call by
`call_records_from_evidence` (`token_ledger.py:763-831`), which reads `model = _first_string(
provider_evidence, (f"{role}_actual_model",))` (`token_ledger.py:806-807`) only when
`provider_evidence.get("actual_model_verified") is True` (`token_ledger.py:801`). Rows are
persisted by `record_task_run_calls`
(`token_ledger.py:836ff`), keyed `call_id, job_id, task_id, role, model` (`_CALL_COLUMNS`,
`token_ledger.py:166-179`).

**MISSING.** No single record carries both a task's terminal status and its per-role actual model.
Computing pass_quota needs a join, by `(job_id, task_id)`, between `job.json`'s `tasks[].status` and
the ledger's `calls` rows' `(role, model)`, grouped by `(model, role)`; n = the count of distinct
tasks in that group.

### repair_need — repair rounds or retries per task

Two different granularities exist, and the feature file's wording ("repair rounds OR retries")
covers both without picking one:

- **Task-level rounds**: `TaskEntry.repair_rounds_used` / `repair_rounds_allowed`
  (`pingpong_job.py:224-225`, mirrored on `TaskProofSummary` at `pingpong_job.py:190-191`) — one pair
  of counts per task. Attributable to whichever model served the task's role, UNLESS the task's
  tier escalated mid-run.
- **Call-level retries**: `provider_attempts[].is_retry` / `is_parse_retry`, summed per tier segment
  in `tier_outcome_rows` (`packages/orchestration/tier_outcomes.py:116`).

**F296's tier records.** A run whose builder and reviewer both run on configured tier models carries
`tier_ladder` in its record (`tier_outcomes.py:3-4`, `packages/orchestration/tier_escalation.py`);
`tier_outcome_rows` (`tier_outcomes.py:100-121`) turns it into one row per tier segment: `task_class`,
`tier`, `reviewer_tier`, `rounds`, `retries`, `outcome`, `cost_usd`/`cost_basis`
(`TierOutcomeRow`, `tier_outcomes.py:65-82`). `tier` is a config LABEL from `model_escalation.tiers`
(`tier_escalation.py:78`, `TierModel(provider, model)` at `tier_escalation.py:66-71`), not a model
name — rows exist ONLY when `tier_ladder` is present (`tier_outcomes.py:102-104`), i.e. only for runs
with tier escalation enabled. `query_tier_outcomes` (`tier_outcomes.py:194-216`) answers one summary
per `(task_class, tier)`, and its own module docstring already says "F133 reads
`query_tier_outcomes`" (`tier_outcomes.py:13-14`) — but it has NO current consumer (`grep -rn
query_tier_outcomes packages apps` outside `tier_outcomes.py` itself finds nothing).

**MISSING.** For a non-escalating task, repair_need per `(model, role)` is `repair_rounds_used`
joined to the ledger's model for that task's role (the same join as pass_quota). For an escalating
task it is tier-keyed, and resolving a tier to a model name needs `model_escalation.tiers` AS
CONFIGURED AT RUN TIME, which the row does not carry — only the tier label.

### format_error_rate — the parse or format classes, their storage, and the per-call denominator

**The class.** `FailureClass.PARSE = "parse"` (`packages/orchestration/failure_postmortem.py:86`) is
the only "format"-shaped class in the enum (`failure_postmortem.py:79-123` lists all of them); there
is no separate "format" value, and `grep -rn format_error packages apps` (outside this feature's own
file) finds nothing.

**Storage.** `PostmortemV1` (`failure_postmortem.py:511-553`) is written by `write_postmortem`
(`failure_postmortem.py:687`) into a per-call directory `calls/<role>/round-NN/<kind>` when the
provider streams nothing, or the provider's own per-call stream directory when it has one
(`call_evidence_dir`, `failure_postmortem.py:800-818`), and collected by
`collect_task_call_postmortems` (`failure_postmortem.py:853ff`, both the `pingpong_runs/` and the
`jobs/.../streams/` layouts).

**Names model, role, call?** `PostmortemV1` carries `job_id`, `task_id`, `run_id`, `call_id`
(`failure_postmortem.py:516-519`), `role` and `provider` (`failure_postmortem.py:520-521`) — but NOT
`model`, and NOT a round number. Its `call_id` is built by `shared_call_id`
(`packages/orchestration/pingpong_loop.py:2499-2513`): either the provider's own stream id, or
`f"calls/{role}/round-{round_no}/{kind}"` — NEVER the ledger's own format,
`"<job_id>:<task_id>:<seq>"` (`call_id_for_provider_call`, `token_ledger.py:653-663`). The two
namespaces do not overlap, so a postmortem's `call_id` cannot be joined to a `calls` row by that
column.

**MISSING.** No shared key joins a PARSE postmortem to the model that produced it. The round number
is recoverable only from the postmortem's OWN DIRECTORY PATH (`calls/<role>/round-NN/...`,
`failure_postmortem.py:818`), not from any JSON field, and would need matching against
`provider_evidence.json`'s `provider_attempts[].round` for the same `(job_id, task_id, role)` to find
the attempt's `actual_model`. The per-call denominator (total calls by that model/role, to turn a
PARSE count into a rate) is the ledger's `calls` row count for the same `(model, role)` — same join
gap.

### cost_per_pass — the ledger's `cost_usd` and every `cost_basis` value

`calls.cost_usd` / `calls.cost_basis` (`token_ledger.py:178-179`) are per-call. The basis vocabulary
is `COST_BASIS_PROVIDER_REPORTED = "provider_reported"`, `COST_BASIS_PRICE_TABLE = "price_table"`,
`COST_BASIS_UNKNOWN = "unknown"` (`token_ledger.py:157-163`); `grep -rn COST_BASIS_PRICE_TABLE
packages apps` outside `token_ledger.py`'s own declaration finds nothing — no writer ever sets it, so
every call today is `provider_reported` or `unknown`.

`query_cost(by="role"|"model"|"day")` (`token_ledger.py:1191-1230`) aggregates cost, but `by` takes
exactly ONE group key at a time — `COST_GROUP_KEYS = ("role", "model", "day")`
(`token_ledger.py:186`) is a flat tuple, not a combinable pair, so no existing call gives a JOINT
`(model, role)` cost total; the raw `calls` table supports `GROUP BY role, model` directly, but no
public helper issues that query today.

"Per PASS" needs the same `(job_id, task_id)` join to task terminal status as pass_quota: sum
`cost_usd` over calls whose task is in `TASK_DONE_STATUSES`, divided by the count of such tasks, per
`(model, role)`. `tier_outcomes` rows also carry a per-`(task_class, tier)` `cost_usd`/`cost_basis`
(`tier_outcomes.py:58-59,118-119`), summed only when every call in the segment is priced — tier-keyed,
not model-keyed, same as repair_need.

## 3. Existing aggregations over model or role

- `apps/cli/commands/stats_calls_cmd.py` (77 lines): `remedy stats calls` — tokens per call grouped
  by `(role, provider)` (`_HEADERS`, line 17-18) — NOT model — from
  `packages/orchestration/call_tokens.py`'s `recorded_calls`/`summarize_call_tokens`
  (`stats_calls_cmd.py:59-63`). Window = `--since`/`--job` filter only, no rolling window. Consumer:
  this command only.
- `apps/cli/commands/stats_ledger_cmd.py` (707 lines): `remedy stats cost`/`cache`/`report`/
  `backfill-ledger`/`verify-ledger` (its docstring, lines 1-8). `cost` calls `token_ledger.query_cost`
  grouped by role OR model OR day, basis-labeled (its docstring, lines 10-17), never jointly, no
  pass/fail join.
- `apps/cli/commands/failure_stats_cmd.py` (77 lines): `remedy stats failures` — calls
  `packages/orchestration/failure_stats.collect_failures`, a `FailureClass` histogram scoped by
  job/since/project (`failure_stats_cmd.py:40-57`); `collect_failures`
  (`packages/orchestration/failure_stats.py:116`) has no role or model parameter — `grep -n "role\|
  model" packages/orchestration/failure_stats.py` finds nothing.
- `apps/cli/commands/stats_calibration_cmd.py` (110 lines): `remedy stats calibration` — F074's
  design precedent this feature's file names (T7_F133.md, line 24): per `(task_class, role)` token
  and cost percentile distributions (`calibration_rows`, `stats_calibration_cmd.py:34-45`); `role`
  here is `TASK_TOTAL_ROLE = "all"` for the whole task (`estimate_calibration.py:46`) or a per-role
  breakdown — but grouped by task CLASS, not by model.
- `packages/orchestration/model_routing.py` (1442 lines): policy/validation (hard rules, promotion
  bars), not an aggregation over historical outcomes — `PromotionEvidence`
  (`model_routing.py:615-648`) is an OPERATOR-LOGGED benchmark record, not ledger-derived.
- `packages/orchestration/tier_escalation.py` / `tier_outcomes.py`: per `(task_class, tier)` outcome,
  rounds, retries, cost (section 2's repair_need/cost_per_pass above); zero current consumers outside
  the module itself.
- `packages/orchestration/estimate_calibration.py` (section 2's precedent): per `(task_class, role)`
  token/cost percentile distributions with a rolling window, a sample floor, outlier damping and a
  cached snapshot — the explicit design precedent this feature's file names.
- `grep -rniE "pass_rate|reliab|per.model|by_model|success_rate" packages apps --include="*.py"`
  (outside `tests/`): the only hits are `model_routing.py`'s `PromotionAssertionResults`
  (`block_level_pass_rate`, `overall_pass_rate`, lines 606-607) and
  `PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE`/`PROMOTION_MINIMUM_OVERALL_PASS_RATE`
  (`model_routing.py:560,564`) — both OPERATOR-SUPPLIED benchmark bars for a manual tier-promotion
  decision, not a computed historical aggregate. No other hit anywhere in `packages apps`.

**The one-trust-home risk (Acceptance).** `tier_outcomes.py` is the existing structure closest to a
second trust home: it already has outcome + rounds + retries + cost per tier, mirrored into the same
`ledger.sqlite` the new module would use (`tier_outcomes.py:11-14`). Its own docstring already
invites F133 to read it rather than re-derive the figures a second way.

## 4. Routing evidence

`resolve_task_class_tier` (`model_routing.py:253-266`) is the resolver: it returns `(tier, reason)`
for a `task_class`, `reason` being `SEED_MAPPING_REASON` or `UNKNOWN_CLASS_REASON`. The real
per-call evidence shape is `ROUTED_CALL_EVIDENCE_FIELDS` — `task_class`, `tier`, `reason`,
`promoted_by` — built by `routed_call_evidence_fields` (`model_routing.py:1170-1210`) and returned by
`route_role_call` (`model_routing.py:1371-1395`), named in its own comment as "THE SINGLE SEAM ...
every provider call site routes through it once the wiring round lands" (`model_routing.py:1366-1369`).

`resolve_routed_call_evidence` (`packages/orchestration/role_config.py:380-409`) wires this into
`RoleConfig.routed_call: dict[str, str | None] | None` (`role_config.py:236`), consumed by
`resolve_role_config` at `role_config.py:490` (`routed_call=resolve_routed_call_evidence(role,
originating_task_class)`). The tests that pin it: `tests/orchestration/test_role_config.py:304-449`
assert `cfg.routed_call`'s keys equal `ROUTED_CALL_EVIDENCE_FIELDS` and its values match
`ROLE_TASK_CLASSES`/`resolve_task_class_tier`/`UNDECLARED_ROLE_TASK_CLASS` for each case, including
`None` for an inheriting role (`repair`) given no originating class.

**MISSING / the note's home.** `grep -rn "\.routed_call\b" packages apps` outside tests and
`role_config.py`'s own docstring finds NO production reader: `RoleConfig.routed_call` is resolved and
then never consumed by anything that persists it into `job.json` or `provider_evidence.json` today.
This is exactly where an informational "trust suggests otherwise" note could be added without
changing the route: as an extra key a future consumer of `RoleConfig.routed_call` reads and logs,
without touching `resolve_task_class_tier` or `route_role_call`'s own return value — the route itself
never has to know trust exists.

## 5. Names

`grep -rliE trust packages apps --include="*.py"` outside `tests/` returns many files that merely use
the word "trust" in prose; the ones that NAME a trust concept:

- `packages/orchestration/trust_report.py` (543 lines), `summarize_trust_report`
  (`trust_report.py:64`) — a per-JOB audit summary: "what was requested, planned, run, created,
  verified, decided, and explicitly NOT done" (`trust_report.py:2-7`). Unrelated to F133's per-model
  metric. Command: `apps/cli/commands/brain.py:326` `_cmd_trust_report`, catalog id `"brain.trust"`
  (`apps/cli/command_catalog.py:977`), subcommand `"trust"` → `remedy brain trust`.
- The deleted pair (section 1) is gone; nothing else under `packages apps` names a class or module
  `*Trust*` that aggregates anything.

**Proposed names** (grep-to-self only, AGENTS.md "Code Discoverability Conventions"):
- Module: `packages/orchestration/model_reliability.py` — avoids "trust" entirely, so it never
  collides with `trust_report.py`'s per-job audit or greps as a ghost of the deleted
  `provider_trust.py`.
- Snapshot file: `model_reliability_snapshot.json` beside the ledger, mirroring
  `CALIBRATION_SNAPSHOT_FILENAME = "calibration_snapshot.json"` (`estimate_calibration.py:49`).
- Command file: `apps/cli/commands/stats_trust_cmd.py` for `remedy stats trust`, command id
  `"stats.trust"` — paralleling `stats_calibration_cmd.py`/`"stats.calibration"`. "trust" stays
  acceptable at the COMMAND layer because `remedy stats trust` and `remedy brain trust` sit under
  different parent groups and do not collide; the MODULE layer drops "trust" so a grep for
  `provider_trust` or `trust_report` never returns this feature's aggregator by accident.

## 6. Proposal (for DECISION F133 D2, not a decision)

- **pass_quota**: join `job.json`'s `tasks[].status` (`TASK_DONE_STATUSES`, `pingpong_job.py:75`) to
  the ledger's `calls` rows by `(job_id, task_id)`, grouped by `(model, role)`; n = tasks in the
  group. Not recorded as one record today — T002 builds the join, cached as a snapshot like
  calibration's.
- **repair_need**: `TaskEntry.repair_rounds_used` (`pingpong_job.py:224`) summed per `(model, role)`
  via the same join, for tasks whose tier never escalated. For an escalated task: "not recorded
  today" against a model name — only against a tier label — shown as a dash (A9's sparse-honest
  rule) unless a later round records the tier-to-model mapping AS OF the run.
- **format_error_rate**: "not recorded today" as a clean join. T002 either adds a `model` field to
  `PostmortemV1` at the write site (a schema bump past `POSTMORTEM_VERSION = 1`,
  `failure_postmortem.py:41`) or performs the directory-path-based join read-only, at query time.
  Denominator: the ledger's `calls` count per `(model, role)` over the same window.
- **cost_per_pass**: sum `calls.cost_usd` over calls whose task is in `TASK_DONE_STATUSES` (the same
  join as pass_quota), divided by the task count, per `(model, role)`; basis stays
  `provider_reported`/`unknown` until a pricing feature gives `price_table` a writer.
- **Window and floor discipline**, borrowed from `estimate_calibration.py`: sample floor
  `DEFAULT_CALIBRATION_SAMPLE_FLOOR = 20` and window `DEFAULT_CALIBRATION_WINDOW_DAYS = 90`
  (`estimate_calibration.py:54-55`), its outlier damping (one sample in twenty, at least one, trimmed
  from each end once a class has three or more — its docstring, line 16), its snapshot-cache
  pattern beside the ledger (`CALIBRATION_SNAPSHOT_FILENAME`, `estimate_calibration.py:49`), and its
  read-only `PRAGMA query_only=1` ledger connection (its docstring, line 20).
- **What retires**: nothing production-facing — the provider-trust pair is already gone. The dead
  `provider_trust_report_id` field on `self_dogfood_execution.py` (lines 167, 179, 195, 217) is out
  of this feature's scope; a later DECISION may remove it.
- **The one trust home**: T002 should make `tier_outcomes.query_tier_outcomes`
  (`tier_outcomes.py:194`) a SOURCE the new module reads, exactly as its own docstring invites
  (`tier_outcomes.py:13-14`), rather than re-deriving round/retry/cost figures a second way over the
  same ledger.
