# Live Review — F013 Job intake

Per-feature ledger. Findings are authored by the reviewer
(Window 1) and applied here verbatim by the worker. R-XXXX IDs
continue monotonically across features (last used: R-0109).
History lives in git and in each feature's evidence zip.

### R-0110: schema-level clarifications cap defeats the A9 truncate-and-record rule
- **Status**: Resolved
- **Severity**: Medium
- **Area**: packages/orchestration/schemas/models.py (JobIntake.clarifications), tests/schemas/test_job_intake.py
(test_clarifications_over_max_rejected)
- **Details**: max_length=5 makes an LLM response with >5
  clarifications a parse FAILURE (retry burned, possible
  parse-class abort) instead of the feature's A9 default:
  "keep the first five, record the drop count". Validation
  rejects before the intake module can truncate, and the
  contract has no field to carry the drop count.
- **Expected fix**: (a) remove max_length from clarifications;
  (b) add `dropped_clarifications: int = 0` to JobIntake —
  set by the intake module after truncating to 5, default 0;
  (c) replace test_clarifications_over_max_rejected with a test
  that >5 clarifications VALIDATE at schema level (truncation
  is module behavior, tested in T002); (d) schema-size ceiling
  test stays green.
- **Reviewer**: independently verified — cap removed,
  dropped_clarifications contract added, module truncation
  tested; suites rerun by reviewer (147 green). Resolved.

### R-0111: job show intake rendering missing (ordered in T003, absent, unreported)
- **Status**: Resolved
- **Severity**: High
- **Area**: apps/cli/commands/job.py (_cmd_show_job)
- **Details**: T003 ordered "remedy job show renders the intake
  block". Not built; absent from the handoff changed-files and
  prose — incomplete handback per review protocol.
- **Expected fix**: _cmd_show_job renders an Intake block when
  job.intake is set: goal, context_refs, constraints,
  acceptance_hints, clarifications (question + default), source
  label, truncated_input / dropped_clarifications when nonzero.
  No block when intake is None (legacy jobs). Tests: shows block
  for job with intake; silent for legacy job; probes use only
  text-UI-displayed values.
- **Reviewer**: independently verified — diff read, 156 tests
  rerun green by reviewer, ruff main-parity 6=6 confirmed.
  Resolved.

### R-0112: do path never attempts LLM intake; no per-call evidence
- **Status**: Resolved
- **Severity**: High
- **Area**: apps/cli/commands/do_cmd.py (_cmd_do_mission),
  packages/orchestration/intake.py
- **Details**: heuristic_intake is hardwired; run_intake is dead
  code from the CLI; the no_llm parameter changes nothing; no
  intake call ever writes a per-call evidence directory. Feature
  acceptance requires: fake-provider run stores the fake's exact
  goal AND its evidence directory exists; no-provider run falls
  back with label, exit 0.
- **Expected fix**: (a) _cmd_do_mission: unless --no-llm, attempt
  run_intake with a call_fn built ONLY on the loop's existing
  provider invocation surface (A6 — no new subprocess/timeout
  code; if a minimal helper extraction is unavoidable, extract
  with unchanged behavior + its own tests). Provider missing/
  unconfigured/error → heuristic fallback. --no-llm skips the
  attempt. (b) Per-call evidence: wire on_call to the same
  per-call evidence writer the loop uses (F004/F005 infra) so
  each real intake call gets a normal evidence directory. Name
  the exact reused functions in the handoff. (c) Tests: CLI-level
  fake-provider run asserts stored intake carries schema_v +
  exact fake goal + evidence dir exists; no-provider run asserts
  heuristic label + exit 0; --no-llm asserts zero provider
  attempts.
- **Reviewer**: independently verified — diff read, 156 tests
  rerun green by reviewer, ruff main-parity 6=6 confirmed.
  Resolved.

### R-0113: degraded-mode label deviates from specified P6 wording
- **Status**: Resolved
- **Severity**: Medium
- **Area**: apps/cli/commands/do_cmd.py (_cmd_do_mission output)
- **Details**: Prints "Intake: heuristic". Feature specifies the
  fallback line "intake: heuristic fallback (provider
  unavailable)" whenever the heuristic path served an LLM-capable
  invocation.
- **Expected fix**: fallback path prints exactly
  intake: heuristic fallback (provider unavailable)
  LLM success prints intake: llm. --no-llm prints
  intake: heuristic (forced by --no-llm). JSON output carries
  source + fallback reason. Update golden-path probes to the
  displayed strings.
- **Reviewer**: independently verified — diff read, 156 tests
  rerun green by reviewer, ruff main-parity 6=6 confirmed.
  Resolved.

### R-0114: LLM path drops the deterministic truncated_input flag
- **Status**: Resolved
- **Severity**: Medium
- **Area**: packages/orchestration/intake.py (run_intake)
- **Details**: run_intake truncates the prompt but discards the
  was_truncated bit; the stored flag then depends on LLM
  self-report, violating A9 ("truncated in the PROMPT at a
  documented marker … and flagged truncated_input").
- **Expected fix**: run_intake forces truncated_input=True on the
  validated result whenever the prompt was truncated (post-parse
  override, like _truncate_clarifications). Test: oversized
  mission + fake provider returning truncated_input=false →
  stored intake has truncated_input=true.
- **Reviewer**: independently verified — diff read, 156 tests
  rerun green by reviewer, ruff main-parity 6=6 confirmed.
  Resolved.

### R-0115: handoff ruff claim excluded a touched file
- **Status**: Resolved
- **Severity**: Low
- **Area**: .agent/handoff.md (verification section)
- **Details**: "ruff (touched files): All checks passed!" but
  touched do_cmd.py was omitted from the command. (Reviewer
  checked: main parity 6=6, zero NEW — outcome fine, claim
  incomplete.)
- **Expected fix**: rerun ruff over ALL touched files; report
  do_cmd.py main-parity explicitly (pre-existing count vs branch
  count). Process rule going forward: the ruff command in a
  handoff lists every touched file.
- **Reviewer**: independently verified — diff read, 156 tests
  rerun green by reviewer, ruff main-parity 6=6 confirmed.
  Resolved.

### R-0116: intake duplicates the Ollama provider configuration surface
- **Status**: Open
- **Severity**: Medium
- **Area**: packages/orchestration/intake.py
  (make_provider_call_fn), packages/providers/ollama_planner/
  provider.py
- **Details**: make_provider_call_fn re-implements host/model
  resolution copied from OllamaPlanner, hardcodes the model
  fallback "qwen3-coder-next" and timeout=15.0, and ignores the
  temperature/num_predict options the planner surface resolves.
  Second config surface = drift risk; the order required reusing
  the existing provider invocation surface.
- **Expected fix**: (a) OllamaPlanner gains a neutral
  raw_call(prompt, *, schema, system=None) that builds the client
  from self.host and applies self.temperature/self.num_predict;
  plan_raw delegates to it with UNCHANGED behavior (same system
  prompt + "Plan this job:" wrapping). Unit tests with a fake
  ollama module prove delegation and option passthrough.
  (b) make_provider_call_fn instantiates OllamaPlanner() and
  returns a closure over raw_call(prompt, schema=JobIntake
  schema) — delete the duplicated host/model resolution, the
  hardcoded model fallback, and the hardcoded timeout. The
  client.list() availability probe may stay, built from the
  planner's host. Any timeout goes through config, not a literal;
  record the choice in .agent/decisions.md.
  (c) Update TestMakeProviderCallFn: env-var model override
  (REMEDY_OLLAMA_PLANNER_MODEL) reaches the chat call; ollama
  missing → None. All existing suites stay green.
- **Reviewer**: pending

### R-0117: provider-error fallback mislabeled as provider unavailable
- **Status**: Open
- **Severity**: Low
- **Area**: apps/cli/commands/do_cmd.py (_cmd_do_mission label
  logic)
- **Details**: fallback_reason == "provider_error" prints
  "intake: heuristic fallback (provider unavailable)" — the
  provider WAS reachable; its output failed the schema gate or
  transport errored mid-call. Label contradicts the JSON reason.
- **Expected fix**: provider_error prints exactly
  intake: heuristic fallback (provider error)
  provider_unavailable keeps the spec string. Golden-path probes
  updated to the displayed strings.
- **Reviewer**: pending
