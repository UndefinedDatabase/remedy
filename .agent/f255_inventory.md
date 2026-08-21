# F255 seam inventory — measured at HEAD, R2

Every claim below was resolved by opening the named file at the round's base
commit `6c47a490` and reading the cited line. Nothing here is recalled from a
feature file, from a previous round or from the step block. Where the answer is
that something does not exist, it is written as an explicit ABSENT together with
the search that established it. Nothing is designed here and no source file,
test or document was changed this round: suggestions for R3 are marked
`SUGGESTION` and are not decisions.

## Q1 — Role resolution

The role vocabulary is `KNOWN_ROLES`, a seven-name tuple declared once in
`packages/orchestration/role_config.py:56`. Its members are `builder`,
`reviewer`, `repair`, `design_worker`, `test_worker`, `final_verifier` and
`orchestrator`. A role OUTSIDE that tuple does not raise: `resolve_role_config`
tests membership at line 125 and, on a miss, calls `warnings.warn` at line 126
and then resolves the role anyway against whatever overrides were supplied,
returning `RoleConfig(role=role, **resolved)` at line 149. So the behaviour
today is WARN-AND-DEFAULT, not error, and not silent either. The test suite
pins exactly that: `test_unknown_role_warns_not_crashes` at
`tests/orchestration/test_role_config.py:96` asserts a `UserWarning` AND that
the unknown role still resolves with the default provider.

SPEC-VS-REALITY GAP, measured. The feature file at
`docs/roadmap/features/T5_F255.md:15` says the teacher is "resolved through the
same role_config mechanism as orchestrator/worker/reviewer". `orchestrator` and
`reviewer` are in `KNOWN_ROLES`; **`worker` is not**. The string `worker` as a
role name lives in a DIFFERENT vocabulary — the `ConventionsRole` enum at
`packages/orchestration/role_conventions.py:54`, whose member `WORKER = "worker"`
sits at line 57 and which has exactly two members. The registration phrase
therefore names two vocabularies as if they were one. R3 must rule which of the
two a teacher joins; the answer is probably both, since the teacher needs a
model (role_config) and will want a conventions document (role_conventions).

FIVE INDEPENDENT ROLE LISTS EXIST. A fourth role must be taught to each one that
applies to it; none of them derives from `KNOWN_ROLES` at import time, so adding
a name to the tuple alone changes nothing anywhere else.

| path:line | symbol | what it does |
|---|---|---|
| `packages/orchestration/role_config.py:56` | `KNOWN_ROLES` | the seven-name role vocabulary; the only list `resolve_role_config` consults |
| `packages/orchestration/role_config.py:125` | membership test | `if role not in KNOWN_ROLES:` — the single gate on the vocabulary |
| `packages/orchestration/role_config.py:126` | `warnings.warn` | unknown role warns; it does not raise |
| `packages/orchestration/role_config.py:149` | `return RoleConfig(...)` | the unknown role still resolves and is returned |
| `tests/orchestration/test_role_config.py:123` | `test_all_seven_roles_present` | a frozen exact-tuple assertion; its NAME also encodes the count |
| `tests/orchestration/test_role_config.py:124` | `assert KNOWN_ROLES == (` | duplicates all seven names literally — list #2 |
| `tests/orchestration/test_role_config.py:96` | `test_unknown_role_warns_not_crashes` | pins warn-and-default as the contract |
| `apps/cli/commands/do_cmd.py:74` | `_ROLE_OVERRIDE_ROLES` | list #3: `("builder", "reviewer", "repair")`, the CLI `--<role>-model` surface |
| `apps/cli/commands/do_cmd.py:150` | `for role in _ROLE_OVERRIDE_ROLES:` | the loop that builds those flags; a role absent here gets no CLI flag |
| `packages/orchestration/token_cost_policy.py:33` | `_ROLE_PROMPT_KEYS` | list #4a: builder/reviewer/repair prompt-count columns |
| `packages/orchestration/token_cost_policy.py:38` | `_ROLE_ESTIMATED_KEYS` | list #4b: the same three roles' estimated-token columns |
| `packages/orchestration/role_conventions.py:54` | `class ConventionsRole` | list #5: a two-member enum, a role vocabulary of its own |
| `packages/orchestration/role_conventions.py:57` | `WORKER = "worker"` | the ONLY place `worker` is a role name in code |
| `packages/orchestration/role_conventions.py:63` | `CONVENTIONS_DOC_RELATIVE_PATHS` | role to conventions-document path |
| `packages/orchestration/config.py:481` | `key="orchestrator.model"` | the precedent for a role-specific config key; `teacher.model` would copy this shape |

SUGGESTION for R3: adding `teacher` to `KNOWN_ROLES` immediately reddens
`tests/orchestration/test_role_config.py:123`, whose name says "seven". That
test is the intended tripwire, so the rename to eight is part of the T-slice
rather than an accident to discover at build time.

## Q2 — Ledger event vocabulary

There is NO closed vocabulary. Run-log event names are FREE STRINGS. The decisive
line is `packages/orchestration/run_log.py:66`:

    event: str

`RunEvent.event` is an unconstrained `str` field, and the emitter
`RunLogWriter.log` at `packages/orchestration/run_log.py:134` takes it as a
positional `event: str` at line 136 and appends the JSONL line with no lookup
against any registry. The read side agrees: `LedgerEvent.event_type` at
`packages/orchestration/event_ledger.py:37` is likewise a bare `str`.

A PARTIAL registry exists but is not wired to anything. `EVENT_METADATA_SCHEMAS`
at `packages/orchestration/event_schemas.py:23` enumerates the required METADATA
KEYS of seven event types, and `validate_event_metadata` at line 71 checks a
metadata dict against them, returning `[]` for an unknown event because line 77
simply misses the dict. Measured: `validate_event_metadata` and
`get_event_schema` have NO caller under `packages/`, `apps/` or `scripts/` — the
only callers are tests, e.g. `tests/storage/test_persistence.py:358`. Command
run: `grep -rn "validate_event_metadata\|get_event_schema\|EVENT_METADATA_SCHEMAS"
--include=*.py packages/ apps/ scripts/ tests/`.

MEASURED SIZE OF THE GAP. A scan of every `.log("<name>"` call under
`packages/`, `apps/` and `scripts/` finds **39 distinct event-name literals
emitted from 14 files**. Of those 39, only **4** appear in the seven-entry
`EVENT_METADATA_SCHEMAS` table, and the table's coverage is of metadata keys,
never of the name itself.

VERDICT ON THE DEPENDENCY. `docs/roadmap/features/T5_F255.md:3` registers F255 as
"Depends on: stable ledger event vocabulary (Tier 2)". **That dependency is NOT
satisfied today.** Stage 1 of F255 is "passive narration keyed to ledger events",
and there is nothing today that a narration template could key to that a typo in
an unrelated module could not silently break.

| path:line | symbol | what it does |
|---|---|---|
| `packages/orchestration/run_log.py:66` | `event: str` | the event NAME is an unconstrained string — the whole answer to Q2 |
| `packages/orchestration/run_log.py:134` | `RunLogWriter.log` | the emitter; builds a `RunEvent` from kwargs and appends |
| `packages/orchestration/run_log.py:136` | `event: str,` | the emitter's parameter; no validation, no allowlist |
| `packages/orchestration/event_ledger.py:37` | `event_type: str` | the normalized read-side record; also a free string |
| `packages/orchestration/event_schemas.py:23` | `EVENT_METADATA_SCHEMAS` | partial registry: 7 event types, METADATA keys only |
| `packages/orchestration/event_schemas.py:71` | `validate_event_metadata` | the validator — production callers: zero |
| `packages/orchestration/event_schemas.py:77` | `EVENT_METADATA_SCHEMAS.get(event_name)` | an unregistered name is a miss, not an error |
| `tests/storage/test_persistence.py:358` | test import | a test is the only thing that calls the validator |
| `docs/roadmap/features/T5_F255.md:3` | dependency line | names the vocabulary this section measures as absent |

SUGGESTION for R3: rule whether F255 must FIRST close its own dependency (a
named-event registry the emitter enforces) or may narrate a small explicitly
enumerated subset of the 39 names, with unknown events narrated as "unknown"
under the feature's own honesty rule. This is a planning decision, not a build
detail.

## Q3 — Budget pools

A "pool" concept DOES NOT EXIST in the code. Search:
`grep -rn "pool" --include=*.py packages/orchestration/` returns exactly two
hits, both a local variable in an unrelated selection routine —
`packages/orchestration/evidence_index.py:252` reads `pool = same_branch or
candidates`. There is no budget pool, no spend pool and no pool table anywhere
under `packages/orchestration/`.

WHAT ACTUALLY EXISTS IS AN ATTRIBUTION AXIS CALLED `role`. A token charge is
attributed by a `role` COLUMN on the F103 ledger's `calls` table:
`_CALL_COLUMNS` at `packages/orchestration/token_ledger.py:154` lists `"role"`
at line 158, beside `job_id`, `task_id`, `model` and the token/cost fields.
Reporting groups along that axis: `COST_GROUP_KEYS` at
`packages/orchestration/token_ledger.py:173` is the literal
`("role", "model", "day")`, and `query_cost` at line 1000 refuses any other
grouping with a `ValueError` rather than answering a different question.

BUDGET LIMITS ARE A SEPARATE AND JOB-SCOPED THING. The five limits are
`_LIMIT_ORDER` at `packages/orchestration/budget_guard.py:245` —
`max_provider_calls`, `max_total_tokens`, `max_cost_usd`,
`max_wall_clock_minutes`, `deadline` — configured through the `budget.*` keys in
`_CONFIG_KEYS` at `packages/orchestration/budget_resolution.py:120`. **None of
them is per-role.** So the two halves answer differently: teacher spend
REPORTING is a new value on the existing `role` axis and costs nothing new,
while a teacher spend LIMIT is a new axis, because no limit in Remedy is
currently scoped to anything narrower than the job.

| path:line | symbol | what it does |
|---|---|---|
| `packages/orchestration/token_ledger.py:154` | `_CALL_COLUMNS` | the ledger row shape; the attribution fields live here |
| `packages/orchestration/token_ledger.py:158` | `"role",` | the column that attributes a charge to its spender |
| `packages/orchestration/token_ledger.py:173` | `COST_GROUP_KEYS` | `("role", "model", "day")` — the only reporting axes |
| `packages/orchestration/token_ledger.py:1000` | `query_cost` | read-only aggregation; rejects an unknown `by` |
| `packages/orchestration/budget_guard.py:245` | `_LIMIT_ORDER` | the five enforceable limits, all job-scoped |
| `packages/orchestration/budget_resolution.py:120` | `_CONFIG_KEYS` | maps each limit to its `budget.*` config key |
| `packages/orchestration/evidence_index.py:252` | `pool = ...` | the ONLY `pool` token under packages/orchestration — unrelated local |

SUGGESTION for R3: "own budget pool" in the registration can be satisfied at
Stage 1 by reporting alone, since Stage 1 is declared zero-token. Only Stage 2
needs the limit, and that is where a new limit axis has to be ruled.

## Q4 — `ActionClass` and `read_only`

`ActionClass` is declared at `apps/cli/command_catalog.py:31` and is a
`typing.Literal`, not an Enum and not a validated value object. Its eight
members are `read_only`, `write_metadata`, `approval_gate`, `apply_write`,
`test_execution`, `dev_helper`, `local_state_change` and
`controlled_builder_execution`. It is used as the annotation of one field,
`action_class: ActionClass` at line 80 of the same file.

WHAT ENFORCES IT: **nothing at runtime.** A `Literal` annotation on a frozen
dataclass field is not checked when the dataclass is constructed, and a sweep of
`action_class` across `packages/`, `apps/` and `scripts/` finds only three
non-declaration sites: the catalog itself, a SERIALIZATION at
`packages/orchestration/review_bundle.py:1756` which copies the value into the
review bundle, and a COMMENT at `apps/cli/commands/job.py:2193`. No code path
anywhere branches on `action_class == "read_only"` to permit or deny an
operation. Command run: `grep -rn "action_class" --include=*.py packages/ apps/
scripts/ tests/`.

WHAT DOES ENFORCE IT IS THE TEST SUITE, in two distinct strengths. The weak,
systematic form checks the DECLARATION: `test_every_command_has_action_class` at
`tests/test_command_catalog.py:61` checks the value is in an allowlist that is
retyped in the test rather than imported, and `test_mutating_commands_flagged` at
line 66 asserts at line 70 that a command flagged `may_mutate_repo` or
`may_execute_commands` is not `read_only` — that is consistency between two
declarations, not evidence about behaviour. The strong, behavioural form exists
but only per command:
`tests/orchestration/test_job_budgets.py:1352`,
`test_the_command_does_not_mutate_the_persisted_job`, whose comment at line 1354
states the standard exactly — `action_class="read_only" has to be true of the
bytes on disk` — and which proves it by comparing `job.json` bytes before and
after the command runs.

| path:line | symbol | what it does |
|---|---|---|
| `apps/cli/command_catalog.py:31` | `ActionClass = Literal[` | the definition; a type alias with eight string members |
| `apps/cli/command_catalog.py:80` | `action_class: ActionClass` | the only field carrying it; never validated at construction |
| `packages/orchestration/review_bundle.py:1756` | `"action_class": cmd.action_class` | serializes the declaration into evidence; reads, never enforces |
| `apps/cli/commands/job.py:2193` | comment | the only other production mention — prose, not a check |
| `tests/test_command_catalog.py:61` | `test_every_command_has_action_class` | allowlist check, retyped in the test rather than imported |
| `tests/test_command_catalog.py:70` | `assert cmd.action_class != "read_only"` | declaration-vs-declaration consistency for mutating commands |
| `tests/orchestration/test_job_budgets.py:1352` | `test_the_command_does_not_mutate_the_persisted_job` | the ONE behavioural read-only proof found: bytes on disk unchanged |

SUGGESTION for R3: the plan's risk "READ-ONLY IS AN INVARIANT, NOT AN INTENTION"
is confirmed by measurement — `read_only` is declarative. If the teacher's hard
invariant is to mean anything, the T-slices need an enforcement seam plus a
behavioural test in the shape of
`tests/orchestration/test_job_budgets.py:1352`, and the block
should say so rather than assume `ActionClass` already provides it.

## Q5 — The watch path

`remedy do watch` DOES NOT EXIST. `remedy teach` DOES NOT EXIST. Both are ABSENT.
The `do` group holds fifteen commands — `do.run`, `do.plan`, `do.continue`,
`do.replan`, `do.repair-attest`, `do.report`, `do.evidence`, `do.promote`,
`do.job-plan`, `do.job-run`, `do.job-resume`, `do.job-report`, `do.job-evidence`,
`do.job-promote`, `do.job-flow` — and none is `watch`. Searches run:
`grep -n "command_id=\"do\." apps/cli/command_catalog.py`;
`grep -rn "\"watch\"\|'watch'\|add_parser(\"watch\|watch --learn" --include=*.py
apps/ packages/ scripts/`, which returns NOTHING — every `watch` hit in the repo
belongs to the word `watchdog` or to prose in a comment; and
`grep -rn "teach" --include=*.py apps/ packages/ scripts/`, whose five hits are
all the English verb inside docstrings. So the registration's phrase "same
isolation rules as watch" at `docs/roadmap/features/T5_F255.md` refers to
isolation rules that have never been written, because the command they would
belong to has never been built.

THE NEAREST EXISTING READ-ONLY READER OF A RUN is `remedy event timeline`,
declared at `apps/cli/command_catalog.py:2478` with `action_class="read_only"` at
line 2482. A second, closer in spirit, is `remedy mission watchdog` at
`apps/cli/command_catalog.py:1681`, `read_only` at line 1685, whose docstring at
`apps/cli/commands/mission_cmd.py:485` states the isolation intent in words:
it evaluates the tripwires and reports what fired, "pausing nothing and raising
no decision".

THE ISOLATION MECHANISM IS THE FILE FORMAT, NOT A LOCK OR A SUBSCRIPTION. The
run log is an append-only JSONL file per run at the path given in
`packages/orchestration/run_log.py:5`, and readers are separate processes that
open and re-read that file whole. The production reader is `load_run_events` at
`packages/orchestration/timeline.py:68`, which globs every `*.jsonl` under
`runs/<job_id>/`, skips malformed lines and sorts by timestamp — so a reader
racing a half-written line degrades by dropping that line rather than by failing.
There is NO tail/follow API and no event subscription anywhere: a live reader
today must re-read the whole file. Two further facts R3 should have: the helper
`read_run_events` at `packages/orchestration/run_log.py:184` is explicitly
disclaimed for production use at line 187 ("Intended for tests and diagnostics —
not for production code paths"), and a SECOND, different function of the same
name exists at `packages/orchestration/stream_evidence.py:854`, which is a
one-spelling-per-concept violation under the AGENTS.md discoverability rules and
a trap for anyone grepping for the run-log reader.

| path:line | symbol | what it does |
|---|---|---|
| `apps/cli/command_catalog.py:2478` | `command_id="event.timeline"` | nearest existing read-only reader of a run's events |
| `apps/cli/command_catalog.py:2482` | `action_class="read_only"` | its declared class |
| `apps/cli/command_catalog.py:1681` | `command_id="mission.watchdog"` | read-only observer of a live mission |
| `apps/cli/command_catalog.py:1685` | `action_class="read_only"` | its declared class |
| `apps/cli/commands/mission_cmd.py:485` | `_cmd_mission_watchdog` docstring | states the isolation intent: pauses nothing, raises no decision |
| `packages/orchestration/run_log.py:5` | run-log path | `<REMEDY_DATA_DIR>/runs/<job_id>/<run_id>.jsonl`, append-only |
| `packages/orchestration/timeline.py:68` | `load_run_events` | THE production reader; globs, tolerates malformed lines, sorts |
| `packages/orchestration/run_log.py:184` | `read_run_events` | reader helper |
| `packages/orchestration/run_log.py:187` | its docstring | disclaims production use in so many words |
| `packages/orchestration/stream_evidence.py:854` | `read_run_events` | a DIFFERENT function with the same name — name collision |

SUGGESTION for R3: since `watch` does not exist, F255 cannot inherit its
isolation rules; it must STATE them. The material to state them from is on this
list — append-only JSONL, whole-file re-read, malformed-line tolerance, no
follow API — and the CLI shape `remedy do watch --learn` implies building
`do watch` itself, which the registration does not scope. Rule whether F255
builds it or retargets onto `event timeline`.

## Q6 — Does `teacher` exist anywhere?

ABSENT, all but one comment. Command run:
`grep -rni "teacher" packages/ apps/ tests/ scripts/`. It returns exactly ONE
line in the whole search, and that line is a comment naming this very feature:

| path:line | symbol | what it does |
|---|---|---|
| `tests/docs/test_docs_consistency.py:26` | comment | reads "and F255 (teacher role), added by" — a docs-consistency note, not code |

There is no teacher module, no teacher role name, no teacher command, no teacher
test and no teacher config key. F255 starts from zero, which is the cleanest
possible starting position and means no existing behaviour can regress from
adding the role itself.
