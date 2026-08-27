# F032 source inventory — measured at `a399a330`

Every answer below is a measurement taken on the round base, cited with
`path:line` or with the command and its real output. Where a question could not
be answered by measurement the gap is stated as a gap; nothing here is inferred
from the feature file.

Tool note: the block's Q8 command names `rg`. `rg` is not installed in this
session (`python3 -c subprocess.run(['rg', ...])` raised
`FileNotFoundError: [Errno 2] No such file or directory: 'rg'`), so the
equivalent `grep -rlE 'decision_queue|HumanDecision|export_decision_json' tests/`
was run instead and its real output is quoted under Q8.

## Q1 — the enforcement point

The eight producing branches of
`packages/orchestration/decision_queue.py::list_decisions` (function at
`decision_queue.py:62`), each with the record it derives from and the site that
CREATES that record.

| # | Branch (site) | `type` | id form | Underlying record → its creation site |
|---|---|---|---|---|
| 1 | `decision_queue.py:73-97` | `patch_approval` | `pa:<intent_id>` | `artifact.metadata["patch_intent_explanations"]`, read by `approval_queue.list_patch_intents` (`packages/orchestration/approval_queue.py:129`). Written at FIVE sites: `packages/orchestration/job_fulfillment.py:691`, `packages/orchestration/autorun.py:253`, `packages/orchestration/builder_bridge.py:287`, `packages/orchestration/provider_trust.py:875`, `packages/orchestration/provider_patch_material.py:456` |
| 2 | `decision_queue.py:99-120` | `stop_reason` | `sr:<sr.id>` (`sr:derived_no_repo`, `sr:derived_test_fail`, `sr:derived_not_approved`, `sr:derived_dirty_repo`) | `StopReason` objects constructed INLINE by `stop_reasons.derive_stop_reasons` (`packages/orchestration/stop_reasons.py:187`; the four constructor calls at `:200`, `:214`, `:232`, `:246`). Never persisted — the docstring at `:191` says "Does not persist". The module ALSO has a persisted store (`create_stop_reason` at `:124`, JSONL at `:65-68`) that this branch does NOT read |
| 3 | `decision_queue.py:122-142` | `test_failure` | `tf:<test_run_id[:8]>` | run-log events named `test_run_completed` with `metadata.status == "failed"`. Emitted at `packages/orchestration/autorun.py:394`, `:524` and `:574` through `_emit` (`autorun.py:739`) |
| 4 | `decision_queue.py:144-162` | `repo_dirty` | literal `dirty_repo` | run-log event `git_status_read` with `metadata.dirty`. Written at `apps/cli/commands/repo.py:84-94` via `RunLogWriter.log` |
| 5 | `decision_queue.py:164-217` | `token_budget` | `budget:<request_id>`, else literal `budget_exhausted` (`:202-203`) | three different carriers: `job.metadata["budget_stop_reason"]`/`["error"]`/`job.error` (`:169-174`), `job.stop_reason`/`job.stop_source` (`:176-179`), and the run-log event `job_stopped` with `metadata.source == "budget"` (`:181-187`), written at `packages/orchestration/pingpong_job.py:2906-2913` |
| 6 | `decision_queue.py:219-240` | `memory_review` | `mem:<key>` | `MemoryEntry` rows from `packages.memory.local_gateway.list_memory` (`packages/memory/local_gateway.py:177`), created by `upsert_memory` (`:206`) and moved to `stale` by `mark_stale` (`:331`) |
| 7 | `decision_queue.py:242-324` | `flight_plan_approval` | literal `fp:approval` (both arms, `:294` and `:312`) | `job.flight_plan["_approval"]`. Set to `"pending"` at `apps/cli/commands/do_cmd.py:277` (first plan) and `packages/orchestration/flight_plan.py:787` (replan); set to `"approved"` with `_approval_audit` at `flight_plan.py:751-752` and `:829` |
| 8 | `decision_queue.py:326-372` | `task_decision` (`escalation.DECISION_TYPE_TASK_DECISION`, `packages/orchestration/escalation.py:54`) | `td:<task8>` / `td:<task8>-<n>` (prefix `escalation.py:68`, minted at `escalation.py:190-203`) | escalation records in `job.metadata["escalations"]` (key at `escalation.py:57`), created by `escalation.enqueue_task_decision` (`packages/orchestration/escalation.py:211`) |

**Is there a single function every one of the eight passes through on the way
in? NO.** There is no enqueue seam. `list_decisions` is a read-only derivation —
its own module docstring says so at `decision_queue.py:4-6` ("Derives decisions
from existing records … Not a second source of truth — a read-only
aggregation"). Only branch 8 has a function whose name and shape is an enqueue
(`escalation.enqueue_task_decision`, `escalation.py:211`), and it serves that one
branch. Every other branch mints its `HumanDecision` inline inside
`list_decisions` itself, from a record that was created somewhere else for a
different purpose.

The distinct creation sites, counted: 5 for branch 1, 1 for branch 2 (inline in
`derive_stop_reasons`), 3 for branch 3, 1 for branch 4, 1 event writer for
branch 5 (plus two job-field carriers that are not sites), 2 for branch 6
(`upsert_memory`, `mark_stale`), 2 for branch 7, 1 for branch 8 — **16 distinct
sites in 12 modules** (`autorun.py` serves branches 1 and 3, so it is counted
once among the modules), none of them common to more than one branch.

The nearest thing to ONE common point is `list_decisions` itself: every
`HumanDecision` in the system is constructed inside that one function body — the
NINE `HumanDecision(...)` calls at `:79`, `:105`, `:129`, `:149`, `:204`,
`:225`, `:293`, `:311` and `:343`, nine rather than eight because branch 7 has
two arms.
That is a DERIVATION point, not an enqueue point: a gate there can refuse to
EMIT a tripleless decision, but it cannot refuse to CREATE one, because nothing
is created. The feature file's Design at
`docs/roadmap/features/T5_F032.md:31-33` ("the enforcement point is the enqueue
seam every producer already funnels through (one gate)") does not describe this
source.

Also measured, not asked: `DECISION_TYPES` (`decision_queue.py:53-59`) holds TEN
types; `worker_approval` and `revert_missing` have no producing branch. This
agrees with `tests/orchestration/test_decision_inbox.py:28-40`, whose comment
records the same eight as DECISION F031 D3.

Latent defect measured while answering Q1, reported to the reviewer rather than
fixed: `decision_queue.py:223` filters memory entries by
`e.validity in ("stale", "needs_review")`, but `validity` is
`Literal["active", "stale", "superseded", "contradicted"]`
(`packages/memory/models.py:44`) — `"needs_review"` is a `review_status` value
(`models.py:45`), not a validity, so that half of the predicate can never match.

## Q2 — the schema as built

`HumanDecision` (`packages/orchestration/decision_queue.py:30-50`) has THIRTEEN
fields, in declaration order: `id`, `type`, `status`, `severity`, `source`,
`related_node_id`, `related_intent_id`, `related_file`, `safe_summary`,
`next_actions` (`tuple[str, ...]`), `created_at`, `resolved_at` (`str | None`),
and `payload` (`dict[str, Any]`, `field(default_factory=dict)`, `:50`). The
dataclass is `frozen=True` (`:30`). Twelve fields are required positionally;
`payload` is the only one with a default.

`export_decision_json` (`:409-425`) emits exactly those thirteen keys, one per
field, with two conversions: `next_actions` becomes a `list` (`:421`) and
`payload` a shallow `dict` copy (`:424`). Nothing is dropped and nothing is
added.

**`payload` is the only additive slot** — every other field is required, so a new
key without a schema change has nowhere else to go.

Producers that write `payload` today: TWO of the nine construction sites.
- Branch 7, PENDING arm (`:279-292`, passed at `:306`): always
  `payload["options"] = ["approve", "reject"]` (`:288`), plus
  `payload["clarifications"]` when the plan has open questions (`:290`) and
  `payload["mission_offer"]` when intake flagged a mission candidate (`:292`).
- Branch 8 (`:362-369`): always five keys — `task_id`, `question`, `options`,
  `safe_default`, `cross_references`.

Branch 7's RESOLVED arm (`:308-324`) and branches 1-6 pass no `payload` and get
`{}`. Note that the escalation record carries an `impact` field
(`escalation.py:242`) which branch 8's payload does NOT forward — the nearest
existing thing to an `expected_outcome`/`downside` string is already on disk and
already dropped at the derivation.

## Q3 — where a decision is persisted

**Nowhere. There is no decision store.** `list_decisions` derives around the
storage of eight other subsystems; the feature file's Do-not-touch name "queue
storage" has no single referent in the source.

What storage actually exists, per branch:
- Branches 1, 5 (job fields), 7 and 8 live on the `Job` itself and are persisted
  with it: `packages/orchestration/storage.py:75-80` (`save_job`, one JSON file
  per job at `<jobs dir>/<job.id>.json`), read back at `:83-95` (`load_job`).
  Escalation records are `job.metadata["escalations"]` (`escalation.py:57`,
  `:131-138`); the flight plan is `job.flight_plan`; patch intents are
  `artifact.metadata["patch_intent_explanations"]`.
- Branches 3, 4 and part of 5 read RUN-LOG EVENTS, passed into `list_decisions`
  as the `events` argument — the module never opens them itself.
- Branch 2 reads nothing on disk at all: `derive_stop_reasons`
  (`stop_reasons.py:187-255`) constructs its records per call. A separate
  persisted JSONL store exists in the same module
  (`_stops_path` `stop_reasons.py:65-68` → `<data root>/stops/<job_id>.jsonl`,
  written by `_save_stops` `:103`), and `list_decisions` does not use it.
- Branch 6 reads the memory JSONL through `local_gateway.list_memory`
  (`packages/memory/local_gateway.py:177`).

So: `list_decisions` DERIVES AROUND storage in every branch; it reads no queue of
its own, because none exists.

## Q4 — the evidence-ref vocabulary

**The typed provenance vocabulary the feature file names does not exist in
code.** Measured:
`grep -rn "resolve_ref\|ProvenanceRef\|REF_KIND\|ref_kind" packages/ apps/`
returns ZERO lines. No constant, enum or `Literal` anywhere under `packages/` or
`apps/` carries `file`, `failure` and `decision` as ref kinds, and no function
produces a staleness badge for a reference.

It exists only as an UNBUILT SPEC: `docs/roadmap/features/T3_F066.md` — "Idea
provenance" — states the ref schema at `:24-29` (`type: file|failure|coverage|
decision`), the resolver `resolve_ref(ref) -> Resolution{status: ok|drifted|
missing, detail}` at `:30-36`, and the `ok|drifted|stale` badge at `:37-40`.
F066 is unclaimed at `docs/roadmap/STATUS.md:136` (`- [ ] F066 — Idea
provenance`), and its dependency F063 is unclaimed at `:133`.

Nearest BUILT things, none of which is a resolver:
- `ProviderVerificationEvidenceRef`
  (`packages/orchestration/provider_trust_verification.py:171-177`): fields
  `kind`, `ref_id`, `label`. Its kind vocabulary
  (`trust_report | quarantine | material | intent | failure_artifact |
  request_package | self_attempt | proposed_task`) is a COMMENT on `:172` — no
  constant, no validation. It has no `file` and no `decision` kind.
- `OrchestratorEvidenceRef`
  (`packages/orchestration/orchestrator_brain.py:87-95`): fields `source`,
  `status`, `ref`, `summary`, with the status vocabulary
  `available | missing | malformed | unknown` again only as a comment on `:89`.
  This is the closest existing "badge": a per-ref resolution status.
- `packages/orchestration/file_provenance.py` carries the provenance NAME but
  builds a causal chain for one file, not a typed ref (`ProvenanceLink` `:30-38`,
  `FileProvenance` `:41-50`).
- The only real staleness ENUM in the repo is the memory card's
  `validity: Literal["active", "stale", "superseded", "contradicted"]`
  (`packages/memory/models.py:44`).

Consequence for T001: the chips have no resolver to call. Either F032 builds the
vocabulary it needs, or the triple's refs are untyped strings until F066 lands.
The feature file's Do-not-touch list names the resolver
(`docs/roadmap/features/T5_F032.md:91`), which cannot be honoured literally for
a thing that does not exist.

## Q5 — the options list

`expected_outcome` and `downside` are specified PER OPTION
(`docs/roadmap/features/T5_F032.md:43-45`). Where the options come from today:
**both `payload["options"]` and `next_actions`, and only two branches have a real
options list.**

| # | `type` | `payload["options"]` | `next_actions` |
|---|---|---|---|
| 1 | `patch_approval` | absent | 2 commands, `approve`/`reject` (`decision_queue.py:89-92`) |
| 2 | `stop_reason` | absent | `sr.next_actions`, 1 or 2 strings (`stop_reasons.py:206`, `:220`, `:238`, `:252`) |
| 3 | `test_failure` | absent | 2, one prose + one command (`:139`) |
| 4 | `repo_dirty` | absent | 1 prose string (`:159`) |
| 5 | `token_budget` | absent | `("extend", "abandon")` — bare words, not commands (`:214`) |
| 6 | `memory_review` | absent | 1 command (`:235`) |
| 7 | `flight_plan_approval` PENDING | `["approve", "reject"]` (`:288`) | 2-4 commands (`:250-278`) |
| 7 | `flight_plan_approval` RESOLVED | absent, payload `{}` | `()` — empty (`:321`) |
| 8 | `task_decision` OPEN | the escalation record's `options`, possibly `[]` (`:365`) | one command per option, or one `<your answer>` placeholder when the list is empty (`:338-342`) |
| 8 | `task_decision` ANSWERED | same `options` list | `()` (`:342`) |

So: **no, not every branch has options.** Six of the eight have only
`next_actions`, which are commands and prose, not choices. Branch 7's resolved
arm has neither. The single consumer that reconciles them is
`apps/ui/src/api/decisionCard.ts::decisionAnswers` (`:223`), which prefers
`payload.options` (`:230`) and falls back to `next_actions` (`:234`) — for every
card, without branching on `card.type`, which the file's own comment at `:220-222`
forbids.

The consequence for T001 is that "per option" is undefined for six branches
unless they first grow an options list.

## Q6 — the card surface

`apps/ui/src/api/decisionCard.ts` is 345 lines (`wc -l`). Exports:
`DecisionAnswerKind` (`:35`), `DecisionAnswer` (`:39`), `DecisionClarification`
(`:57`), `DecisionCardModel` (`:67`), `DecisionInboxEntry` (`:104`),
`DecisionInboxDocument` (`:124`), `decisionAgeLabel` (`:132`),
`decisionBlockedLabel` (`:155`), `decisionAnswers` (`:223`),
`buildDecisionCardModel` (`:289`), `decisionCardModels` (`:328`),
`countOpenDecisions` (`:343`).

Fields the module READS off a wire entry: `answerable_by_decision_resolve`
(`:229`, `:313`), `payload` (`:230`, `:301`, `:319`), `next_actions` (`:234`),
`blocked_count` (`:291-292`), `age_seconds` (`:294`), `id` (`:296`), `type`
(`:302`), `status` (`:303`, `:310`), `severity` (`:304`), `safe_summary`
(`:305`), and `inbox.decisions` (`:329`, `:332`). Inside `payload` it reads only
`options` (`:179`), `task_id` (`:189`) and `clarifications` (`:200`). **No
evidence-shaped key is read anywhere today.**

What a card renders: title from `safe_summary`, an age chip, a blocked chip, a
type chip, the clarification question block, and the answer strip — rendered by
`apps/ui/src/components/panels/DecisionInboxCard.tsx`.

Where a chip row would attach: the model side is the object literal returned by
`buildDecisionCardModel` (`decisionCard.ts:295-320`), beside `clarifications`
(`:319`), with a reader mirroring the `payloadOptions`/`payloadTaskId`/
`payloadClarifications` trio (`:175-201`) and a projector mirroring
`cardClarifications` (`:257`). The render side is the existing chip strip
`<div className={styles.decisionChips}>` at
`apps/ui/src/components/panels/DecisionInboxCard.tsx:281`, whose three
`<span className={styles.decisionChip}>` children are lines `:282`, `:283`,
`:284`; the conditional jump chip is `:293`.

Test file that pins it: `apps/ui/src/api/decisionCard.test.ts`, 492 lines,
53 `it(` cases (`grep -c "  it("` = 53). `grep -rln 'from "./decisionCard"'
apps/ui/src/api/` returns EIGHTEEN files: eight further `*.test.ts` siblings
(`decisionAnswerFlow`, `decisionAnswer`, `decisionClarificationForm`,
`decisionFilter`, `decisionFocus`, `decisionOrder`, `decisionSend`,
`decisionSubmit`), the eight production modules behind them, plus
`remedyApi.ts` and `types.ts`. Under `tests/`, the only Python file naming
`decisionCard.ts` is `tests/ui_contracts/test_decision_answer_wiring.py`, and its
single mention at `:432` is inside an assertion MESSAGE, not a structural pin —
so no Python test reads that file's contents.

Not measured: this round ran no vitest, so the 53 cases are a count of `it(`
occurrences in the source, not of collected tests.

## Q7 — the migration precedent

`DECISION_INBOX_VERSION` (`packages/orchestration/decision_inbox.py:37`, value
`1`) is WRITTEN into the inbox document at `:160` and read by NOTHING in
`packages/` or `apps/`. `grep -rn "DECISION_INBOX_VERSION" packages/ apps/
tests/` returns FIVE lines and no more: `decision_inbox.py:17` (docstring),
`:37` (the definition), `:160` (the write),
`tests/orchestration/test_decision_inbox.py:19` (the import) and `:179`
(`assert inbox["version"] == DECISION_INBOX_VERSION`). The one production
consumer is
`packages/orchestration/ui_server.py:2759-2761` (`_build_decisions_json`), which
returns the document unread. The browser does not model the field at all:
`apps/ui/src/api/decisionCard.ts:124-126` declares
`interface DecisionInboxDocument { decisions?: unknown; }` — no `version` key —
and `decisionCardModels` (`:328-333`) only checks that `inbox.decisions` is an
array.

Other precedents found by
`grep -rnE "^[A-Z_]*_VERSION[A-Z_]* *[:=]" --include=*.py packages/ apps/`
(30+ constants). Grouped by what the READER does, since that is the only part
F032 has to choose. Every row below was opened and read at the cited lines:

| Posture | Precedent | Path:line | Value | How an older payload is handled |
|---|---|---|---|---|
| RAISE | `HANDOFF_SCHEMA_VERSION` | `packages/orchestration/handoff.py:74`, written `:402`, checked `:588-589` | `1` | raises `HandoffSchemaVersionError`; the error's own text at `:539` says it "refuses to guess" |
| RAISE | `MISSION_SCHEMA_VERSION` | `packages/orchestration/mission_state.py:64`, field `:192`, check `:217-219` | `1` | `Mission.from_json` raises `ValueError(f"unknown mission schema version: {version}")` |
| RAISE, and actually bumped | `GAUNTLET_ORDER_SET_VERSION` | `packages/orchestration/gauntlet_orders.py:39`, check `:220-222` | `4` | no back-compat path at all; the comment at `:31-38` narrates v2→v3→v4 and older sets are simply unsupported. The repo's only int bumped past 2 with a stated rationale per bump |
| PROBLEM LIST | `SUPPORTED_TOKEN_TRUTH_VERSIONS` | `packages/orchestration/token_authority.py:31`, check `:149-151` | `{"1.0.0"}` | appends a problem string, does not raise. Shaped as a SET so a second accepted version is a one-line change |
| DROP THE RECORD | `QUEUE_ENTRY_VERSION` | `packages/orchestration/job_queue.py:56`, check `:205-206` | `1` | the entry decodes to `None` and is silently skipped |
| DEGRADE, KEEP THE INTENT | `STOP_SIGNAL_VERSION` | `packages/orchestration/safe_points.py:48`, check `:320-327` | `1` | keeps the stop, drops every untrusted field, sets `degraded=True`. The closest posture to F032's "honest placeholder" |
| MIGRATE FORWARD | token ledger `SCHEMA_VERSION` | `packages/orchestration/token_ledger.py:120`, migration table `:192`, applied `:1665-1676` | `2` | the ONLY genuine upgrade path in the repository: per-version DDL plus a meta bump, older DBs migrated, current DBs execute nothing |
| BACKFILL | `RunContract.version` + `migrate_contract` | `packages/orchestration/run_contract.py:276` (field, default `1`), `:644-650`, validation `:768-769` | `1` | idempotent; only ensures a contract EXISTS, never rewrites a version |
| WRITE-ONLY | `COST_REPORT_VERSION` | `packages/orchestration/cost_report.py:48`, written `:296` | `3` | bumped twice with no reader logic anywhere — the same posture as `DECISION_INBOX_VERSION`, at value 3 |
| HISTORY STACK | flight plan `_version` / `_versions` | `packages/orchestration/flight_plan.py:780-786` | derived, starts at `1` | a replan pushes the whole previous plan dict onto `_versions` and increments `_version`. Not a schema version, and the only per-record versioning that already touches a decision-bearing structure |

**What a v1 record looks like to a v2 reader today: indistinguishable from a v2
record, because no reader looks.** `DECISION_INBOX_VERSION` is a write-only
stamp: the only code that compares it is the test at
`test_decision_inbox.py:179`, which compares the document against the constant
the same process just wrote. A v2 that changes only the constant would therefore
change nothing observable; the legacy-rendering story F032 needs
(`docs/roadmap/features/T5_F032.md:29-31`) has to be built from a per-CARD
marker, or the version stamp has to acquire its first real reader.

## Q8 — the guards a schema change must satisfy

`rg` is absent (see the tool note at the top). Real output of
`grep -rlE 'decision_queue|HumanDecision|export_decision_json' tests/`,
17 files:

    tests/cli/test_decision_answers.py
    tests/cli/test_open_decisions_view.py
    tests/cli/test_plan_approval.py
    tests/orchestration/test_approval_queue.py
    tests/orchestration/test_budget_stop_integration.py
    tests/orchestration/test_bundled_clarification.py
    tests/orchestration/test_decision_inbox.py
    tests/orchestration/test_escalation.py
    tests/orchestration/test_f018_authority_integration.py
    tests/orchestration/test_local_model_advisor.py
    tests/orchestration/test_mission_state.py
    tests/orchestration/test_orchestrator_brain.py
    tests/orchestration/test_project_brain.py
    tests/ui_contracts/test_graph_architecture.py
    tests/ui_server/test_brain_view_model.py
    tests/ui_server/test_dashboard_contract.py
    tests/ui_server/test_live_state.py

The EQUALITY guards a new required field would turn red — assertions that pin an
exact field set, an exact list of types, or a count over a whole collection:

1. `tests/orchestration/test_decision_inbox.py:305` —
   `assert set(card) == expected`, where `expected` is
   `set(export_decision_json(decision)) | {"age_seconds", "blocked_count",
   "answerable_by_decision_resolve"}` (built at `:297-301`). This is the
   strongest guard: it is an EXACT key-set equality over every card, but it is
   self-adjusting — it derives `expected` from `export_decision_json` itself, so
   a field added to BOTH the dataclass and the exporter keeps it green. It turns
   red only if the exporter and the card disagree.
2. `tests/orchestration/test_decision_inbox.py:311` —
   `assert set(inbox) == {"version", "job_id", "decisions"}`. An exact top-level
   key set, NOT self-adjusting: any new document-level key turns this red.
3. `tests/orchestration/test_decision_inbox.py:171` —
   `assert tuple(sorted(PRODUCING_FIXTURES)) == tuple(sorted(PRODUCING_DECISION_TYPES))`.
   An exact list of the eight producing types (`:31-40`); a ninth producing type
   turns this red unless it also gets a fixture.
4. `tests/orchestration/test_decision_inbox.py:326-327` — the answerability
   assertion against `ANSWERABLE_DECISION_TYPES` (`:52`), parametrized over all
   eight types at `:319`: an exact statement of which types the write door
   accepts.
5. `tests/orchestration/test_budget_stop_integration.py:195`, `:205`, `:351`,
   `:363` — `len(budget_decisions) == 1` / `== 0` over the whole
   `list_decisions` result, filtered by type.
6. `tests/orchestration/test_approval_queue.py:429` —
   `assert len(dirty_decs) == 1` over the whole result.
7. `tests/orchestration/test_escalation.py:363` — `assert len(derived) == 1`;
   `:404` — `assert len(d.payload["cross_references"]) == 1`, a count inside the
   payload branch 8 writes.
8. `tests/orchestration/test_bundled_clarification.py:345` —
   `assert len(found) == 1, "exactly ONE decision per plan"`; `:282` —
   `assert row.replace("\\|", "").count("|") == 6`, a column-count guard on the
   rendered escalation table (`escalation.py:354`), which turns red if a
   triple adds a column there.
9. `tests/cli/test_plan_approval.py:489-490` — `len(open_decisions) == 0` and
   `len(resolved_decisions) == 1` over the whole result.

Presence-only, therefore NOT equality guards but worth naming because they pin
the type vocabulary: `tests/orchestration/test_approval_queue.py:398-403`
(asserts `DECISION_TYPES` is a frozenset and pins five members by name),
`tests/orchestration/test_budget_stop_integration.py:174`
(`"token_budget" in DECISION_TYPES`), `tests/orchestration/test_escalation.py:354`
(`DECISION_TYPE_TASK_DECISION in DECISION_TYPES`).

Adjacent, and NOT returned by the Q8 command because it does not name any of the
three symbols: `tests/orchestration/test_handoff.py:282` pins an exact key set on
a decision-shaped row (`assert set(row) == {"id", "job_id", "type", "severity",
"summary", ...}`). A T001 author should check it by hand.

Not measured: no test was RUN against a mutated schema this round, so every
"would turn red" above is read from the assertion's text, not from an observed
failure. T001 owes a real red-proof for each guard it expects to move.
