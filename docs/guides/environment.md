# Environment Variables

> GENERATED from the key registry in `packages/orchestration/config.py` by
> `render_environment_guide()`. Do not edit it by hand:
> `tests/docs/test_environment_guide.py` fails whenever the registry and this file differ.
> Regenerate it from the repository root with
> `python3 -c "from packages.orchestration.config import write_environment_guide; write_environment_guide()"`.

Every environment variable Remedy reads is listed here, once. A variable set in the
environment wins over the same setting in `remedy.toml`, and `remedy.toml` wins over the
built-in default. A variable marked env-only has no `remedy.toml` key and can only be set
in the environment. `remedy doctor core` warns about a `REMEDY_` variable that is not in
this list, naming the closest one that is, and about a listed variable whose value does
not read as its type; neither warning stops Remedy from running.

| Variable | Type | Default | remedy.toml key | Description |
|---|---|---|---|---|
| `REMEDY_AGENT_DIR` | text | `.agent` | env-only | Directory of the .agent state files the self-dogfood inspection reads; the inspection also sets it for its own children (env-only) |
| `REMEDY_APPLY_PUSH_AFTER_MISSION` | yes or no (1, true, yes / 0, false, no) | no | `apply.push_after_mission` | Push the branch a mission's commit landed on to its configured upstream at the end of the mission, exactly as --push would (F270). |
| `REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_HIGH` | a whole number | `120000` | `budget.class_default_tokens_high` | Expected tokens for a high-band task (F104; provisional until calibration) |
| `REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_LOW` | a whole number | `8000` | `budget.class_default_tokens_low` | Expected tokens for a low-band task (F104; provisional until calibration) |
| `REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_MEDIUM` | a whole number | `32000` | `budget.class_default_tokens_medium` | Expected tokens for a medium-band task (F104; provisional until calibration) |
| `REMEDY_BUDGET_DEADLINE` | text | none | `budget.deadline` | UTC deadline for a job as ISO 8601 string (F018 budgets) |
| `REMEDY_BUDGET_MAX_COST_USD` | a number | none | `budget.max_cost_usd` | Maximum cost in USD for a job (F104 budgets) |
| `REMEDY_BUDGET_MAX_PROVIDER_CALLS` | a whole number | none | `budget.max_provider_calls` | Maximum provider calls for a job (F018 budgets) |
| `REMEDY_BUDGET_MAX_TOTAL_TOKENS` | a whole number | none | `budget.max_total_tokens` | Maximum total tokens for a job (F018 budgets) |
| `REMEDY_BUDGET_MAX_WALL_CLOCK_MINUTES` | a whole number | none | `budget.max_wall_clock_minutes` | Maximum wall-clock minutes for a job (F018 budgets) |
| `REMEDY_BUDGET_MIN_FREE_DISK_BYTES` | a whole number | none | `budget.min_free_disk_bytes` | Free bytes that must remain on the data root's filesystem for a job to start and to pass a safe point (F276 disk floor) |
| `REMEDY_BUDGET_PRICE_BASIS_USD_PER_1K_TOKENS` | a number | none | `budget.price_basis_usd_per_1k_tokens` | Provisional USD price per 1000 tokens used for cost predictions (F104; provisional until calibration) |
| `REMEDY_CLAUDE_ENABLED` | yes or no (1, true, yes / 0, false, no) | no | env-only | Enable Claude provider (env-only flag) |
| `REMEDY_CLAUDE_PLANNER_MODEL` | text | none | env-only | Model for the Claude CLI planner; beats planner.model and the alias table's default (env-only) |
| `REMEDY_CLAUDE_PLANNER_TIMEOUT` | a whole number | `300` | env-only | Per-call wall timeout of the Claude CLI planner, in whole seconds (env-only) |
| `REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD` | a number | `0.5` | `cost_preview.confirm_above_usd` | USD threshold above which an expensive command's cost preview requires operator confirmation before it runs (F114) |
| `REMEDY_COVERAGE_FAIL_UNDER` | a whole number | none | `quality.coverage_fail_under` | Minimum test coverage percentage |
| `REMEDY_CYCLES_BATCH_SIZE` | a whole number | `1` | `cycles.batch_size` | Maximum tasks executed per cycle (F046) |
| `REMEDY_CYCLES_CHECKPOINT_RETENTION` | a whole number | `5` | `cycles.checkpoint_retention` | How many per-cycle checkpoints to keep for a job (F047). The FIRST and the LATEST checkpoint are always kept on top of this count, and a checkpoint that does not verify is never pruned — it is forensic evidence. |
| `REMEDY_CYCLES_MAX_CYCLES` | a whole number | `1` | `cycles.max_cycles` | Maximum cycles one multi-cycle run may execute (F046). DEFAULT 1 — the rollout rule: Remedy stays single-pass until the F075 milestone gate raises the cap. Both this key and 'remedy job resume --cycles' are capped by that safety default. |
| `REMEDY_CYCLES_REPAIR_ROUNDS` | a whole number | `2` | `cycles.repair_rounds` | Bounded auto-repair rounds a FAILED cycle verify may spend before the cycle keeps its failure (F052). DEFAULT 2. Rounds run through the existing repair loop and obey the same fences, budgets and stop requests as any other provider work; 0 disables self-healing. A verify that failed for a non-test reason (missing command, bad config) is classified and never repaired. |
| `REMEDY_CYCLES_VERIFY_COMMAND` | text | none | `cycles.verify_command` | Per-cycle verify command override (F046). Unset means the cycle's verify step is whatever the caller injected; no verification is ever claimed that did not run. |
| `REMEDY_DATA_DIR` | text | none | `data_dir` | Root directory for Remedy data storage |
| `REMEDY_DOCTOR_DEAD_MODELS` | a comma-separated list | none | `doctor.dead_models` | ADDITIONAL known-dead model ids for the doctor's model check (F254). Config EXTENDS the shipped list in scripts/dead_models.json; it never replaces it, so an id Remedy already ships as dead cannot be configured away. The list is operator-maintained data — Remedy never probes a provider to build it. |
| `REMEDY_DOSSIER_MAX_TOKENS` | a whole number | `3000` | `dossier.max_tokens` | Hard token budget for a mission's dossier (F071). Conservative by default: the dossier is the PREFIX of every orchestrator prompt, so its size is a cost the mission pays once per iteration. Over budget the dossier is rewritten by compression, never truncated — a compression that fails leaves an honest over-budget flag. |
| `REMEDY_EXTERNAL_MEMORY_ENABLED` | yes or no (1, true, yes / 0, false, no) | no | env-only | Enable external memory integration (env-only flag) |
| `REMEDY_LOG_LEVEL` | text | `WARNING` | `logging.level` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `REMEDY_MODEL_ROUTING_PROMOTION_EVIDENCE` | a table, which only remedy.toml can carry | none | `model_routing.promotion_evidence` | Per-project TASK CLASS to BENCHMARK RUN map (F110). Each entry of the [remedy.model_routing.promotion_evidence] sub-table is itself a table: the documented run that LICENSES A CHEAPER TIER for that class, as docs/agents/model_routing_policy.md's 'Promotion rule' describes it. Whether a run clears the promotion bars is decided in packages/orchestration/model_routing.py, never here. Configured in TOML only — an env var cannot carry a table. |
| `REMEDY_MODEL_ROUTING_TASK_CLASS_TIERS` | a table, which only remedy.toml can carry | none | `model_routing.task_class_tiers` | Per-project TASK CLASS to MODEL TIER map (F110). The whole [remedy.model_routing.task_class_tiers] sub-table resolves as ONE value and is laid over the shipped seed mapping in packages/orchestration/model_routing.py. The hard rules of docs/agents/model_routing_policy.md still win: a map that breaks one is REFUSED with the rule named and the shipped table is used. Configured in TOML only — an env var cannot carry a table. |
| `REMEDY_NODE_TIMEOUT_SEC` | a whole number | `90` | env-only | Outer wall timeout of each node scripts/remedy_test_runtime.sh runs, in seconds (env-only) |
| `REMEDY_OLLAMA_BUILDER_MODEL` | text | none | `ollama.builder.model` | Ollama model for builder role |
| `REMEDY_OLLAMA_BUILDER_NUM_PREDICT` | a whole number | none | `ollama.builder.num_predict` | Max tokens for builder |
| `REMEDY_OLLAMA_BUILDER_TEMPERATURE` | a number | none | `ollama.builder.temperature` | Sampling temperature for builder |
| `REMEDY_OLLAMA_HOST` | text | `http://localhost:11434` | `ollama.host` | Ollama server URL |
| `REMEDY_OLLAMA_MODEL` | text | `muse-glimmer:latest` | `ollama.model` | Default Ollama model for all roles |
| `REMEDY_OLLAMA_PLANNER_MODEL` | text | none | `ollama.planner.model` | Ollama model for planner role |
| `REMEDY_OLLAMA_PLANNER_NUM_PREDICT` | a whole number | none | `ollama.planner.num_predict` | Max tokens for planner |
| `REMEDY_OLLAMA_PLANNER_TEMPERATURE` | a number | none | `ollama.planner.temperature` | Sampling temperature for planner |
| `REMEDY_OPENCODE_ENABLED` | yes or no (1, true, yes / 0, false, no) | no | env-only | Enable OpenCode provider (env-only flag) |
| `REMEDY_ORCHESTRATOR_MAX_ITERATIONS` | a whole number | `10` | `orchestrator.max_iterations` | How many iterations one `remedy mission run` may take (F070). Conservative by default: an unattended loop that mis-decides is cheaper to stop early than to let run. Reaching the limit is a NORMAL terminal with an honest status, never a failure and never a silent continuation. |
| `REMEDY_ORCHESTRATOR_MODEL` | text | none | `orchestrator.model` | Model for the mission orchestrator role (F070). Quality at the decision layer is the point, so this is where a top-tier model is named. Unset means the role resolves exactly like every other one — this key is the ONLY orchestrator-specific routing surface, and docs/agents/model_routing_policy.md is unchanged by it. |
| `REMEDY_PI_DEV_ENABLED` | yes or no (1, true, yes / 0, false, no) | no | env-only | Enable Pi dev provider (env-only flag) |
| `REMEDY_PLANNER_FREETEXT` | yes or no (1, true, yes / 0, false, no) | no | env-only | Legacy free-text planner parsing instead of the structured plan schema (env-only flag) |
| `REMEDY_PLANNER_MODEL` | text | none | `planner.model` | Model for the planner role, whichever service serves it (operator amendment amend0920-selfuse-real, DECISION D1). Unset lets the selected planner resolve its own default — the `ollama-default` alias for Ollama, which also honours `ollama.planner.model`, and the `claude-workhorse` alias for the Claude CLI. |
| `REMEDY_PLANNER_PROVIDER` | text | none | `planner.provider` | Which service does the structured planning: `ollama` or `claude-cli` (operator amendment amend0920-selfuse-real, DECISION D1). Read by `packages.orchestration.intake.make_structured_call_fn` when no `--planner-provider` was given. Unset means `ollama`, the only planner Remedy had before the second one existed, so an unconfigured repository plans exactly as it always did. |
| `REMEDY_PLANNING_GRANULARITY_ENABLED` | yes or no (1, true, yes / 0, false, no) | yes | `planning.granularity.enabled` | Normalize Task-Plan task granularity — split oversized tasks, merge trivial neighbors (F016). Disable for byte-identical pass-through of the planner's task list. |
| `REMEDY_PLANNING_GRANULARITY_MAX_ACCEPTANCE` | a whole number | `3` | `planning.granularity.max_acceptance` | Acceptance-criteria count above which a planned task is split (F016) |
| `REMEDY_PLANNING_GRANULARITY_MERGE_GROUP_SIZE` | a whole number | `3` | `planning.granularity.merge_group_size` | Maximum number of consecutive trivial tasks merged into one (F016) |
| `REMEDY_PLANNING_GRANULARITY_SPLIT_BAND` | text | `XL` | `planning.granularity.split_band` | Token band at and above which a planned task is split (S, M, L, XL) (F016) |
| `REMEDY_POSTMORTEM_LLM_SUMMARY` | yes or no (1, true, yes / 0, false, no) | no | `postmortem.llm_summary` | Generate an LLM summary for failure post-mortems (F010). Disabled by default: v1 post-mortems are fully deterministic and make zero provider calls; no generated prose is ever passed off as analysis. |
| `REMEDY_PROJECT` | text | none | env-only | Registered project a command acts on, as UUID or slug, before cwd autodetection (env-only) |
| `REMEDY_PROMPT_BUDGET_DEFAULT_CAP` | a whole number | none | `prompt_budget.default_cap` | Global fallback input token cap (F112) for a task class carrying no configured per-class cap. Falls back further to packages.orchestration.prompt_budget.DEFAULT_FALLBACK_CAP_TOKENS when unset. |
| `REMEDY_PROMPT_BUDGET_TASK_CLASS_CAPS` | a table, which only remedy.toml can carry | none | `prompt_budget.task_class_caps` | Per-task-class input token cap overrides (F112). Each entry's basis is class_default until F074 calibration ships measured caps. Configured in TOML only — an env var cannot carry a table. |
| `REMEDY_PYTEST_LOCK` | text | `/tmp/remedy-pytest.lock` | env-only | Lock file scripts/remedy_pytest.sh and scripts/remedy_coverage.sh hold so two suite runs never overlap (env-only) |
| `REMEDY_PYTEST_LOCK_WAIT` | a whole number | `0` | env-only | Seconds scripts/remedy_pytest.sh waits for that lock; 0 refuses at once (env-only) |
| `REMEDY_PYTEST_TIMEOUT_SEC` | a whole number | `600` | env-only | Wall budget of one scripts/remedy_pytest_runner.py run, which every CI stage goes through; a different budget from tests.pytest_timeout_seconds (env-only) |
| `REMEDY_PYTEST_TIMEOUT_SECONDS` | a whole number | `300` | `tests.pytest_timeout_seconds` | Default pytest timeout in seconds |
| `REMEDY_PYTHON` | text | none | env-only | Python interpreter scripts/remedy_pytest_runner.py runs pytest under; the runner's own interpreter when unset (env-only) |
| `REMEDY_REAL_OLLAMA_SMOKE` | yes or no (1, true, yes / 0, false, no) | no | env-only | Opt in to the real-Ollama smoke tests, which need a running Ollama server with a model (env-only flag) |
| `REMEDY_REVIEWER_FREETEXT` | yes or no (1, true, yes / 0, false, no) | no | env-only | Legacy free-text reviewer parsing instead of the structured review schema (env-only flag) |
| `REMEDY_REVIEW_BASE` | text | none | env-only | Git base the review subject is diffed against; an invalid base is refused, never ignored (env-only) |
| `REMEDY_REVIEW_DIR` | text | none | env-only | Directory scripts/make_review_zip.sh writes review packages to; a relative path is read from the repository root, and $HOME/Repos/remedy-history/zips is used when unset (env-only) |
| `REMEDY_RUNTIME_LOG_MAX` | a whole number | none | env-only | Byte cap on a supervised runtime's captured log; uncapped when unset (env-only) |
| `REMEDY_RUNTIME_PORT` | a whole number | none | env-only | Port a supervised runtime is started on, overriding the one its spec declares (env-only) |
| `REMEDY_RUN_REAL_OLLAMA` | yes or no (1, true, yes / 0, false, no) | no | env-only | Run scripts/remedy_test_real_providers.sh against a real Ollama server instead of skipping (env-only flag) |
| `REMEDY_SCOPE_ALLOW` | a comma-separated list | none | `scope.allow` | Glob patterns for allowed write paths (F017 scope fences) |
| `REMEDY_SCOPE_DENY` | a comma-separated list | none | `scope.deny` | Glob patterns for denied write paths (F017 scope fences) |
| `REMEDY_SELF_USE_MODEL` | text | none | `self_use.model` | Model for both roles of a self-use run (operator amendment amend0920-selfuse-real, DECISION D2). Unset means the alias table's Sonnet alias, which the run's cost bound of at most 8 provider calls and 1.00 USD per closure is written for. |
| `REMEDY_SELF_USE_PROVIDER` | text | none | `self_use.provider` | Provider for BOTH the builder and the reviewer of a self-use run (operator amendment amend0920-selfuse-real, DECISION D2). Unset means `claude-cli`: a self-use run repairs THIS repository, which is frontier work, and five consecutive runs on the local model (SU-019 to SU-023) landed nothing. Set it to `ollama` to put the track back on the local model. |
| `REMEDY_SMOKE_ENABLED` | yes or no (1, true, yes / 0, false, no) | yes | `smoke.enabled` | Contribute the product-smoke DoD block for projects that have a runnable app (F062). A project with no runtime is reported as not applicable either way — this switch does not make it green. |
| `REMEDY_SMOKE_ERROR_PATTERNS` | a comma-separated list | none | `smoke.error_patterns` | ADDITIONAL case-sensitive console error markers for clean_console (F062). Config extends the documented base list; it never replaces it, so the base guarantees cannot be configured away. |
| `REMEDY_SMOKE_OLLAMA` | yes or no (1, true, yes / 0, false, no) | no | env-only | Opt in to the real-Ollama builder bridge smoke test (env-only flag) |
| `REMEDY_SMOKE_PATHS` | a comma-separated list | none | `smoke.paths` | Override the core_paths_respond probe set (F062). When set, these paths REPLACE the extracted ones; the configured health path is still probed first. |
| `REMEDY_SMOKE_READY_TIMEOUT_S` | a number | none | `smoke.ready_timeout_s` | Readiness window for the smoke's app_starts check (F062). Unset means the runtime spec's own ready_timeout_s is used. |
| `REMEDY_SMOKE_REPO` | text | `/tmp/remedy-target-repo` | env-only | Scratch repository scripts/remedy_smoke.sh builds and drives (env-only) |
| `REMEDY_SMOKE_UNLOAD_MODELS` | yes or no (1, true, yes / 0, false, no) | no | env-only | Unload the Ollama models scripts/remedy_smoke.sh loaded when it ends (env-only flag) |
| `REMEDY_STRICT_EVENT_NAMES` | yes or no (1, true, yes / 0, false, no) | no | env-only | Refuse a run-log event whose name is not declared; tests only, a job never fails a ledger write on it (env-only flag) |
| `REMEDY_TEACHER_LESSONS` | yes or no (1, true, yes / 0, false, no) | no | `teacher.lessons` | Write a lesson from the real diff after every completed task (F265). Off by default: each lesson is one teacher model call, and a run makes no call the operator did not switch on. |
| `REMEDY_TEACHER_LESSON_MAX_CALLS` | a whole number | `30` | `teacher.lesson_max_calls` | The teacher's budget pot per job, in calls (F265): once the job's teacher calls reach it, a completed task gets an empty lesson that says the pot is spent. |
| `REMEDY_TEACHER_LESSON_MAX_TOKENS` | a whole number | `300000` | `teacher.lesson_max_tokens` | The teacher's budget pot per job, in the tokens its calls reported (F265); a call that reports none still counts against the call limit. |
| `REMEDY_TEACHER_MODEL` | text | none | `teacher.model` | Model for the teacher role (F255). The teacher reads and explains and never writes, so this key buys explanation quality and nothing else. Unset means the role resolves exactly like every other one. Stage 1 narration is deterministic and spends nothing, so nothing reads this key until the Stage 2 question path exists (T004) — a declared key with no reader yet, not a forgotten wiring. |
| `REMEDY_UI_ALLOW_LEGACY_FALLBACK` | yes or no (1, true, yes / 0, false, no) | no | env-only | Serve the legacy app shell when the built UI is missing, with a warning (env-only flag) |
| `REMEDY_UI_COMMAND_RATE_LIMIT_PER_MINUTE` | a whole number | `30` | `ui.command_rate_limit_per_minute` | Commands the UI write door accepts for one token fingerprint and one job per minute (DECISION F009 D9). The excess is refused with 429 rather than made to wait, because an inbound request is holding a connection. 30 is the default because a human cockpit stays an order of magnitude below it — an operator clicking a control manages a few commands a minute — while a client stuck in a retry loop is stopped inside two seconds of real traffic. |
| `REMEDY_UI_DEMO_MODE` | yes or no (1, true, yes / 0, false, no) | no | env-only | Label the cockpit's synthetic placeholder data as demo data (env-only flag) |
| `REMEDY_UI_HOST` | text | `127.0.0.1` | `ui.host` | UI server bind host |
| `REMEDY_UI_NO_AUTO_BUILD` | yes or no (1, true, yes / 0, false, no) | no | env-only | Skip the UI server's automatic npm build of apps/ui (env-only flag) |
| `REMEDY_UI_PORT` | a whole number | `8765` | `ui.port` | UI server port |
| `REMEDY_WATCHDOG_BURN_MIN_SAMPLES` | a whole number | `5` | `watchdog.burn_min_samples` | How many measured iterations must sit BEFORE the window before the burn tripwire is allowed to fire at all (F077). Conservative by default: a baseline of five is the smallest one worth comparing to. Below it the tripwire is inert — thin data produces no trip, never a trip on thin data. |
| `REMEDY_WATCHDOG_BURN_MULTIPLIER` | a number | `3.0` | `watchdog.burn_multiplier` | How many times the baseline mean the window mean must STRICTLY exceed before the burn tripwire fires (F077). Conservative by default: 3x tolerates the normal spread between a cheap and an expensive iteration, so an alarm means something. The tripwire is inert below watchdog.burn_min_samples whatever this reads. |
| `REMEDY_WATCHDOG_BURN_WINDOW` | a whole number | `3` | `watchdog.burn_window` | How many of the most recent MEASURED iterations form the burn window the watchdog compares against the mission's own baseline (F077). Conservative by default: three smooths a single expensive iteration without hiding a sustained run-away. The tripwire stays inert below watchdog.burn_min_samples. |
| `REMEDY_WATCHDOG_NO_PROGRESS_REPEATS` | a whole number | `3` | `watchdog.no_progress_repeats` | How many dispatches in a row on ONE milestone, with no milestone declared done between them, count as no progress (F077). Conservative by default: three identical attempts is already a loop arguing with itself, and the watchdog only ever pauses the mission for a human — it never repairs what it stopped. |
