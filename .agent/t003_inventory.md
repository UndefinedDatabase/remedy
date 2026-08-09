# T003 inventory — prompt-assembly sites to migrate (F105)

> `.agent/` task state for F105 T003, written at R9. NOT a `docs/` document and
> deliberately NOT registered in docs/README.md. Every line number below is a
> line at commit c0e59290 and was confirmed on disk; a number given as
> "(line N)" beside a function name is that function's `def` line, and every
> other number is the exact line of the statement it describes. Two module
> constants are cited as such (`_BUILDER_SYSTEM`, `_REVIEWER_RETRY_PROMPT`) and
> carry no `def`. Ranks cite the F105 scale as `SegmentStabilityRank`
> declares it in `packages/orchestration/prompt_segments.py`: SYSTEM=0,
> CONVENTIONS=1, DOSSIER=2, JOB_CONTEXT=3, TASK=4, STEERING=5.

Read before writing: every site below was read in the source this round. Where
a claim is about wiring rather than text ("does not reach call evidence"), it
was derived by reading every call site of the function, not by assuming.

## Cross-cutting fact that shapes every migration

Four of the six builders (intake, plan, mission, orchestrator) never send the
string they build. `run_structured_call`
(`packages/orchestration/structured_outputs.py`) wraps the base prompt through
`build_schema_prompt` or `native_schema_prompt` and sends THAT. So for those
four the "prompt" has a schema tail nobody's builder emits, and a
content-equality golden must state which of the two strings it pins.

### packages/orchestration/structured_outputs.py — `build_schema_prompt` (line 85)
- Idiom: f-string concatenation — `f"{base_prompt}\n\n{schema_instruction(model_cls)}"`, plus an appended retry-hint paragraph when `hint` is non-empty.
- Segments in emission order: base prompt (whatever rank the caller's own composition ends at) · schema instruction incl. the full JSON schema (rank 4, task-shaped: it changes with the model class, not with the task) · retry hint (rank 5, steering; present only on the parse retry).
- Order vs scale: MATCHES. The volatile-most part (the retry hint) is genuinely last, and the schema block is constant per model class.
- Call sites: `packages/orchestration/structured_outputs.py:155` (inside `run_structured_call`, the only one).
- Call evidence: yes, indirectly — the effective prompt this returns is what `on_call(attempt, schema_v, is_parse_retry, effective_prompt)` hands to the caller's recorder, so any trace a caller writes is of THIS string, not of the builder's.
- Migration risk: if T003 makes a builder return a `ComposedPrompt` and the schema tail stays outside the registry, the manifest will describe a prefix of the sent bytes and silently under-report the tail.

### packages/orchestration/structured_outputs.py — `native_schema_prompt` (line 65)
- Idiom: f-string concatenation — base + `NATIVE_SCHEMA_INSTRUCTION`, plus the same optional retry paragraph.
- Segments: base prompt · one-line native-schema instruction (rank 4) · retry hint (rank 5).
- Order vs scale: MATCHES.
- Call sites: `packages/orchestration/structured_outputs.py:153`; `packages/orchestration/pingpong_loop.py:1911` (inside `_reviewer_effective_prompt`).
- Call evidence: yes — same mechanism as above, and for the reviewer it is the string actually traced.
- Migration risk: the two wrappers differ only by which instruction they append; migrating one and not the other splits one concept into two spellings, which AGENTS.md Code Discoverability bars.

## Site 1 — packages/orchestration/pingpong_loop.py · `_build_builder_prompt` (line 812)

- Idiom: a `parts` list join — `parts: list[str]` appended conditionally, returned as `"\n".join(parts)`.
- Ordered segments as the code emits them:
  1. `_BUILDER_SYSTEM` (module constant, line 790) — rank 0 SYSTEM.
  2. a bare `"\n"` element — pure delimiter, no rank.
  3. `context` — the `build_repo_context` pack (goal, file tree, mentioned files or README, safety notes) — rank 3 JOB_CONTEXT.
  4. a second bare `"\n"` — delimiter.
  5. `scope_contract` when non-empty — rank 3 JOB_CONTEXT.
  6. `## Task (Round N)` + `goal` — rank 4 TASK.
  7. `## Detailed Task Instructions` + the safety preamble + `task_body` (round 1 only) — rank 4 TASK.
  8. `## Current Staged State` (rounds ≥2) — rank 5 STEERING.
  9. `## Current Staged Diff` fenced, capped at `_REPAIR_DIFF_CAP` — rank 5.
  10. `## Test Result` — rank 5.
  11. `## REPAIR TASK — Fix Reviewer Findings` + per-finding lines — rank 5.
  12. `"\nProvide your changes and a summary of what you did."` — rank 5.
- Order vs scale: MATCHES (0 → 3 → 3 → 4 → 4 → 5…). Two caveats, neither a rank inversion: the goal text appears TWICE (once inside `context`'s `## Goal` section, once at `## Task`), and the round number is embedded in the rank-4 heading rather than carried as its own volatile segment.
- Call sites: `packages/orchestration/pingpong_loop.py:2560` (the only production one).
- Call evidence: YES. `packages/orchestration/pingpong_loop.py:2591-2592` builds a `prompt_trace` entry from `builder_prompt` with `role="builder"`; entries land in `result.prompt_traces` and are written at line 3249 to `<run_dir>/prompt_trace.jsonl` plus `prompt_trace_summary.json`. `apps/cli/commands/do_cmd.py:2363` reads that index back into a `builder_prompt_created` / `repair_prompt_created` agent-run-trace event. What is recorded is `prompt_sha256` and `prompt_chars` — `PromptTraceEntry` has no segment-manifest field today.
- Migration risk: `"\n".join(parts)` over elements that themselves end in `"\n"`, plus the two bare `"\n"` elements, produces a specific run of blank lines. `PROMPT_SEGMENT_DELIMITER` is `"\n\n"` (DECISION F105 D1), so a naive registry migration changes the blank-line runs and breaks content equality unless each part's trailing newlines are normalised into the segment boundary.

## Site 2 — packages/orchestration/pingpong_loop.py · `_build_reviewer_prompt` (line 1141)

- Idiom: a `parts` list join, with TWO mutually exclusive branches and an early `return` — the scope-packet branch returns at line 1200; the fallback branch returns at line 1240.
- Ordered segments, scope-packet branch:
  1. `_REVIEWER_SYSTEM` (line 801) — rank 0.
  2. `## Original Goal` + goal — rank 4 TASK.
  3. `## Spec Compliance Checklist` via `_render_spec_compliance_summary` — rank 3 JOB_CONTEXT.
  4. the scope section via `_render_reviewer_scope_section` — rank 3.
  5. `scope_contract` — rank 3.
  6. `## RE-REVIEW — Repair Round N` + prior findings — rank 5 STEERING.
  7. `## Builder Summary` — rank 5.
  8. `## Focused Staged Diff` (or `diff_summary`) — rank 5.
  9. `## Test Result` — rank 5.
- Ordered segments, fallback branch: 1 `_REVIEWER_SYSTEM` (0) · 2 `## Original Goal` (4) · 3 spec summary (3) · 4 `scope_contract` (3) · 5 RE-REVIEW + prior findings (5) · 6 `## Task Input Summary` with task hash and token estimate (4) · 7 `## Builder Summary` (5) · 8 `## Files Changed` (5) · 9 `## Staged Unified Diff` (5) · 10 `## Test Result` (5).
- Order vs scale: VIOLATES, in both branches. `## Original Goal` is rank 4 and sits at position 2, ahead of every rank-3 job-context segment; the fallback branch additionally puts the rank-4 `## Task Input Summary` after the rank-5 prior findings. This is the worst-ordered of the six and the largest prospective cache win.
- Call sites: `packages/orchestration/pingpong_loop.py:2750` (the only production one).
- Call evidence: YES, but of a DIFFERENT string. `_reviewer_effective_prompt(reviewer_prompt)` (line 1897) is computed at line 2771 and it is that value the `_rev_trace` recorder (defined line 2776, installed at lines 2827 and 2884) writes, one entry per real provider call. The parse-retry path traces `retry_prompt`, which is `_reviewer_effective_prompt(reviewer_prompt, _parse_hint)` at line 2865 when the provider gave a parse hint and otherwise `_REVIEWER_RETRY_PROMPT.format(excerpt=…)` at line 2867 (`packages/orchestration/pingpong_provider.py:319`) — that second variant is a third reviewer-role string sharing no bytes with the other two.
- Migration risk: the two branches emit different segment SETS. A single registry populated unconditionally would emit both the focused and the full diff, and both scope shapes, changing content rather than composition. The branch must stay a branch over which segments are REGISTERED.

## Site 3 — packages/orchestration/orchestrator_loop.py · `build_orchestrator_prompt` (line 797)

- Idiom: f-string concatenation of exactly two halves — `f"{build_orchestrator_system_prompt(repo_root)}\n\n# Mission state\n\n{context.text}"`.
- Ordered segments:
  1. `build_orchestrator_system_prompt` (line 89): a two-line provenance header (`# Orchestrator protocol v1` / `# Source: docs/agents/orchestrator_protocol.md`) plus the protocol document read from disk — rank 0/1. The feature file rules this the orchestrator's conventions segment: the generated protocol block, no second source.
  2. `# Mission state` + `context.text` from `assemble_context` (line 206), itself joined `"\n\n"` in this order: `## Mission dossier` (rank 2 DOSSIER) · `## Mission plan state` (3) · `## Last report` (3) · `## Open decisions` (3) · `## Handoff from the previous context` (3, first iteration of a resumed mission only) · `## Milestones ready to declare` (5) · `## Your previous move was refused` (5).
- Order vs scale: MATCHES, and it is the only one of the six whose docstring already states the stability argument. Its join string is already `"\n\n"`, i.e. `PROMPT_SEGMENT_DELIMITER`.
- Call sites: `packages/orchestration/orchestrator_loop.py:992` (inside `run_mission`, the only one).
- Call evidence: NO. `run_mission` accepts `on_call` and forwards it to `run_structured_call` at line 994, but neither production caller supplies one: `apps/cli/commands/mission_cmd.py:362` passes only `call_fn`, and `packages/orchestration/gauntlet_runner.py:514` passes the seam callables and no `on_call`. What does reach evidence is `context.digest` — a digest of the SECOND half only — recorded per iteration in the mission ledger via `_record(iteration, context.digest, …)`. The protocol half and the schema tail are in no evidence artifact today.
- Migration risk: `build_orchestrator_system_prompt` reads `docs/agents/orchestrator_protocol.md` at every call. If the registry hashes a segment at registration time while the loop re-reads per iteration, the manifest hash and the bytes actually sent can diverge mid-run after an edit to that file.

## Site 4 — packages/orchestration/intake.py · `_build_intake_prompt` (line 73)

- Idiom: template `.format` — `_INTAKE_PROMPT_TEMPLATE.format(mission=prompt_mission)`, one field, the mission text pre-truncated by `_truncate_mission` at 8000 chars.
- Ordered segments as the template emits them:
  1. `Analyze this mission and produce a structured job intake.` — rank 0 SYSTEM.
  2. `Mission:` + the mission text — rank 4 TASK.
  3. the `Rules:` block (seven bullet rules for the output fields) — rank 0/1 SYSTEM/CONVENTIONS.
- Order vs scale: VIOLATES, and it is the clearest violation of the six. The single volatile part sits in the MIDDLE, so everything after it — the whole rules block, which never changes — can never be part of a cached prefix. Moving the rules ahead of the mission is the entire migration.
- Call sites: `packages/orchestration/intake.py:165` (inside `run_intake`, the only one).
- Call evidence: YES, and this is the only one of the four schema-wrapped builders that reaches it. `run_intake` forwards `on_call` at line 167, and `apps/cli/commands/do_cmd.py:221` supplies `_record_intake_call` (defined at line 206), which builds a `role="intake"` trace entry from the EFFECTIVE prompt — i.e. after `build_schema_prompt`/`native_schema_prompt` — with `prompt_kind` `intake` or `intake-retry`.
- Migration risk: reordering the rules ahead of the mission CHANGES the bytes. That is a content change by the feature file's own definition ("must not change their CONTENT, only their composition"), so this site's golden cannot be a pure equality golden — it needs an explicit before/after pair and a stated decision that the reorder is intended.

## Site 5 — packages/orchestration/flight_plan.py · `_build_plan_prompt` (line 83)

- Idiom: template `.format` — `_PLAN_PROMPT_TEMPLATE.format(intake_json=json.dumps(intake_dict, indent=2), repo_facts=repo_facts_block())`.
- Ordered segments:
  1. `You are a project planner…` preamble — rank 0 SYSTEM.
  2. `## Intake` + the JSON-dumped intake — rank 4 TASK.
  3. `## Repo Facts` + `repo_facts_block()` — rank 2/3 DOSSIER/JOB_CONTEXT.
  4. `## Rules` (task ids, DAG, bands, clarification-resolution and conservative-default rules) — rank 0/1.
  5. `Return ONLY a JSON object matching the flight_plan_v1 schema.` — rank 5 STEERING.
- Order vs scale: VIOLATES. Task (4) precedes job-context (2/3), which precedes conventions (0/1); only the trailing steering line is where the scale wants it. Correct order would be 1 → 4 → 3 → 2 → 5.
- Call sites: `packages/orchestration/flight_plan.py:347` (inside `plan_job_llm`, the only one).
- Call evidence: NO. `plan_job_llm` accepts `on_call` and forwards it at line 353, but both production callers omit it — `apps/cli/commands/do_cmd.py:253` and `apps/cli/commands/do_cmd.py:2860` pass only the call function. The `role="planner"` traces that DO exist (`apps/cli/commands/job.py:230-267`, `_record_plan_call`) belong to the other planner path, `packages/orchestration/structured_planner.py:59` `make_structured_planner` over `PlannerPlan` — not to this prompt. A reader who greps for planner prompt traces will find that one and must not mistake it for this site.
- Migration risk: `repo_facts_block()` is called at build time and lists the current working directory, so the prompt is environment-dependent and a golden pinned in CI differs from a golden pinned locally. Unlike `build_mission_prompt`, this function has no parameter to inject the facts — the seam has to be added before the golden can exist.

## Site 6 — packages/orchestration/mission_compiler.py · `build_mission_prompt` (line 169)

- Idiom: template `.format` — `_MISSION_PROMPT_TEMPLATE.format(goal=…, repo_facts=project_facts or repo_facts_block(), max_milestones=resolve_milestone_cap(max_milestones), max_draft_jobs=MAX_MILESTONE_DRAFT_JOBS, schema_v=MISSION_PLAN_DRAFT_SCHEMA_V)`.
- Ordered segments:
  1. `You are compiling a mission plan…` preamble — rank 0 SYSTEM.
  2. `## Mission Goal` + the goal — rank 4 TASK.
  3. `## Repo Facts` — rank 2/3.
  4. `## Rules` (outcome-not-step rule, id/DAG rules, the `{max_milestones}` and `{max_draft_jobs}` caps, rationale and jobs_draft rules) — rank 0/1, but PARAMETERISED, so it is only stable for a fixed cap.
  5. `Return ONLY a JSON object matching the {schema_v} schema.` — rank 5 STEERING.
- Order vs scale: VIOLATES, same shape as site 5.
- Call sites: `packages/orchestration/mission_compiler.py:277` (inside `compile_mission_plan`, the only one).
- Call evidence: NO. `compile_mission_plan` forwards `on_call` at line 280 and `plan_mission` forwards it at line 626, but neither production caller supplies one — `apps/cli/commands/mission_cmd.py:187` and `packages/orchestration/gauntlet_runner.py:505` both call `plan_mission` positionally with a call function only. `compile_mission_plan` writes nothing by design, so there is no evidence path here at all until the CLI passes a recorder.
- Migration risk: the rules block interpolates `max_milestones`, so it is NOT a constant segment — registering it as a rank-1 conventions segment would make the "byte-stable prefix across calls within a role" acceptance claim false for any caller that varies the cap (R-0197's whole point). It has to be split into a constant part and a parameterised tail, which changes where the delimiter falls.

## Further prompt-assembly sites found while reading the six

These are not among the feature file's six, but the six either call them or are
wrapped by them, so T003 cannot migrate a site without deciding what happens to
its neighbour.

### packages/orchestration/pingpong_loop.py — `build_repo_context` (line 687)
- Idiom: a `sections` list join — `"\n".join(sections)`, returning `(text, categories)`.
- Segments in order: `## Goal` (rank 4 TASK) · `## File Tree` fenced (rank 2/3) · `## File: <path>` blocks for mentioned files (rank 3) · `## README.md` when no mentioned files (rank 2) · `## Context Safety Notes` (rank 3).
- Order vs scale: VIOLATES — the goal (rank 4) leads a block whose remainder is rank 2/3, and the whole result is then injected into `_build_builder_prompt` at rank-3 position, so the goal is rank-4 material embedded inside a rank-3 segment.
- Call sites: `packages/orchestration/pingpong_loop.py:2462` — called ONCE, before the round loop, so its bytes are stable across every round of a run.
- Call evidence: only derivatively — `result.context_categories` and `result.context_chars` are recorded, and the text itself reaches evidence only as part of the builder prompt trace.
- Migration risk: pulling `## Goal` out of this pack to rank it correctly changes the builder prompt's bytes AND removes the duplicate goal, which is a content change, not a composition change.

### packages/orchestration/pingpong_loop.py — `_render_spec_compliance_summary` (line 910)
- Idiom: a `lines` list join, `"\n".join(lines) + "\n"`; returns `""` when no checklist exists.
- Segments: heading · the deterministic pass/fail line · missing-items line · forbidden-file violations line · an interpretation instruction when not PASS. All rank 3 JOB_CONTEXT except the closing instruction (rank 5).
- Order vs scale: internally MATCHES; its placement inside the reviewer prompt is what violates (see site 2).
- Call sites: `packages/orchestration/pingpong_loop.py:1162`.
- Call evidence: only as part of the reviewer prompt trace.
- Migration risk: it returns `""` for "no checklist", and the caller guards on truthiness. A registry that registers an empty segment would emit a stray delimiter.

### packages/orchestration/pingpong_loop.py — `_render_reviewer_scope_section` (line 1042)
- Idiom: a `lines` list join.
- Segments: the scope heading and reason · changed files · hunks · related tests · risk tags · estimated review tokens (all rank 3) · four fixed guidance paragraphs about scope escalation (rank 1 CONVENTIONS, emitted last).
- Order vs scale: VIOLATES internally — the four fixed guidance paragraphs are the only constant text in the function and they are emitted AFTER the per-task scope data.
- Call sites: `packages/orchestration/pingpong_loop.py:1170`.
- Call evidence: only as part of the reviewer prompt trace.
- Migration risk: those guidance paragraphs are conventions text living in a builder module — moving them to `docs/agents/reviewer_conventions.md` would be the F105 T002 shape, but that IS a content move and belongs in a reviewed diff of the conventions file, never in a composition change.

### packages/orchestration/orchestrator_loop.py — `build_orchestrator_system_prompt` (line 89)
- Idiom: f-string concatenation of a two-line provenance header plus `orchestrator_protocol_text(repo_root)`, read from disk on every call.
- Segments: `# Orchestrator protocol v1` + `# Source: …` (rank 0) · the protocol document (rank 1 CONVENTIONS).
- Order vs scale: MATCHES.
- Call sites: `packages/orchestration/orchestrator_loop.py:805` (inside `build_orchestrator_prompt`); also exported and used by tests.
- Call evidence: NO — see site 3.
- Migration risk: read-per-call versus hash-at-registration, as noted at site 3.

### packages/orchestration/orchestrator_loop.py — `assemble_context` (line 206)
- Idiom: a tuple of `(section_name, body)` pairs joined `"\n\n"` with a per-section `f"{name}\n\n{body}"`, plus a trailing `"\n"`.
- Segments and ranks: listed under site 3.
- Order vs scale: MATCHES — the module comments state the stability argument per section constant.
- Call sites: `packages/orchestration/orchestrator_loop.py:963`.
- Call evidence: its `digest` reaches the mission ledger; its text does not.
- Migration risk: `context_digest(text)` is computed over the joined text and is compared across iterations elsewhere. Changing the join or the trailing newline changes every stored digest, so the digest and the manifest must be migrated together or old ledgers stop comparing.

## Migration order

One builder per round, each with its own golden, in this order.

1. **`_build_intake_prompt`** — first. Smallest surface (one template, one
   format field) and the ONLY one of the six whose prompt already reaches call
   evidence end to end through an existing recorder. That lets the first
   migration prove BOTH halves of T003 — composition through the registry and
   the manifest reaching call evidence — without inventing an evidence path in
   the same round. Its reorder is also the one with the clearest cache
   argument, so the T004 before/after number has something to show.
2. **`build_mission_prompt`** — same template idiom, and it already accepts
   `project_facts`, so its golden can be made deterministic without adding a
   seam. Carries the parameterised-rules problem, which is worth meeting on the
   simpler of the two sites that have it.
3. **`_build_plan_prompt`** — same idiom again; needs a `repo_facts` injection
   seam added before its golden can be deterministic, and needs `on_call`
   threaded at `apps/cli/commands/do_cmd.py:253` and `:2860` before its
   manifest can reach evidence.
4. **`build_orchestrator_prompt`** — two segments, already rank-ordered, join
   string already `"\n\n"`, so the composition move is nearly a no-op and the
   round's real work is the evidence gap (`on_call` at
   `apps/cli/commands/mission_cmd.py:362`) plus the read-per-call hashing
   question.
5. **`_build_builder_prompt`** — twelve conditional parts and a `"\n".join`
   whose blank-line runs must be reproduced exactly. Take it after the registry
   has been exercised four times.
6. **`_build_reviewer_prompt`** — last. Two mutually exclusive branches, the
   clearest rank inversion of the six, and three distinct
   reviewer-role strings (base, effective, parse-retry) that all reach
   evidence. Highest content-equality risk of the six.

Independent of the six, and BEFORE step 5: decide whether the schema tail from
`build_schema_prompt`/`native_schema_prompt` becomes a registered rank-4
segment. If it does not, every manifest for sites 1-4 describes a strict prefix
of the bytes actually sent, and the acceptance claim "the segment manifest
appears in call evidence for every role" is only half true.

## Deliberate absences

Text search cannot find what is not there (AGENTS.md, Code Discoverability), so
the prompt-assembly sites this inventory deliberately does NOT list as T003
targets are named here with the reason.

- `packages/orchestration/mission_dossier.py` · `build_compression_prompt`
  (line 497) — template `.format`. The F071 dossier-compression prompt. Not
  named by the feature file; the dossier is an INPUT segment to the
  orchestrator prompt, and compressing it is a different role.
- `packages/orchestration/dod_compiler.py` · `_build_dod_prompt` (line 349) —
  template `.format`. F061's Definition-of-Done compiler. Reached from
  `attach_milestone_dods` in the mission path, so it is adjacent to site 6, but
  it is not one of the six and migrating it would widen the feature.
- `packages/orchestration/structured_planner.py` · `make_structured_planner`
  (line 59) — the OTHER planner path, over `PlannerPlan`. It assembles no
  prompt of its own (it delegates to `run_structured_call`), but it owns the
  `role="planner"` traces that a reader will find first when grepping for
  planner prompt evidence. Listed so site 5's evidence claim is not misread.
- `packages/orchestration/pingpong_job.py` · `_build_task_prompt` (line 2536) —
  the job-level task prompt. Not named by the feature file; needs its own
  read before anyone claims it is or is not a builder module.
- `packages/orchestration/local_candidate_generator.py` ·
  `build_candidate_prompt` (line 304) and
  `packages/orchestration/local_model_advisor.py` ·
  `build_local_advisor_prompt` (line 363) — local-model side channels, not role
  prompts in the builder/reviewer/orchestrator sense, and not cache-bearing.
- `packages/orchestration/self_repair_proposal.py` ·
  `convert_self_repair_proposal_to_worker_prompt` (line 625) — converts a
  stored proposal into worker text; a document transform, not a provider
  prompt assembled per call.
- `packages/orchestration/pingpong_provider.py` · `_REVIEWER_RETRY_PROMPT`
  (module constant at line 319, formatted at
  `packages/orchestration/pingpong_loop.py:2867`) — a third reviewer-role
  string. It is NOT a `def`, so it carries no `def` line number; it is named
  here because it reaches call evidence through the same `_rev_trace` recorder
  as site 2 and any reviewer manifest that ignores it will be incomplete.
- Provider-side prompt additions (the Claude CLI `--json-schema` payload, the
  Ollama `format=` field) — assembled outside this repository. Nothing in T003
  can register them, and the manifest must not pretend to cover them.

The acceptance guard the feature file specifies ("a guard test greps direct
string-assembly patterns in the builder modules, allowlist starting empty") has
to name which modules count as builder modules. Every absence above is a
candidate for that list; none is ruled out here, and the decision belongs to the
round that writes the guard.
