OUTCOME: (pending — update at handback)

You are the Remedy worker (Window 2) for feature F069 — Mission compiler,
  round R1 (SPLIT, LARGE bundle): claim + T001 + T002 + T003. AGENTS.md
  governs. Save THIS ENTIRE block verbatim to .agent/last_block.md FIRST
  (update its OUTCOME line at handback). STOP-ON-RED RULE for the whole
  round: the first red verification command → STOP per AGENTS.md If
  Blocked — do NOT continue into the next slice; commit the safe state,
  record the raw failing output in the handoff, hand back early.

  PHASE 0 — OPEN PR GATE + BRANCH (AGENTS.md, Open PR Gate)
   1. gh pr list --state open --json number,headRefName,baseRefName,isDraft
      Expected: exactly PR #174, feature/f062-product-smoke -> main, not a
      draft. If and only if that is what you see:
      gh pr merge 174 --merge --delete-branch
      ANY other state (more PRs, draft, wrong base/head) → STOP, report raw
      output in the handoff.
   2. git checkout main && git pull. Verify the merge landed (git log
      --oneline -5 contains the F062 closure commits, head includes
      52a283cf's content).
   3. git checkout -b feature/f069-mission-compiler

  PHASE 1 — CLAIM (own commit)
   1. Save the two AUTHORED TEXT payloads below to
      .agent/authored/f069-r1-1.md and .agent/authored/f069-r1-2.md —
      bytes between BEGIN/END markers, exclusive, including the final
      newline. Verify each with sha256sum against its BEGIN-marker hash.
      Mismatch → STOP, report the raw sums, apply nothing.
   2. Apply f069-r1-1 to docs/roadmap/STATUS.md (FROM occurs once).
   3. Replace .agent/live_review.md ENTIRELY with the bytes of f069-r1-2.
   4. Rewrite .agent/plan.md yourself (worker-owned) for F069: keep the
      headings `## Goal` and `## Next Steps` (contract tests read them:
      tests/ui_server/test_dashboard_contract.py, tests/docs/); name the
      branch feature/f069-mission-compiler; Goal = the feature file's Goal
      & Done (docs/roadmap/features/T1_F069.md); Current Step = this R1
      LARGE bundle; Next Steps = integration gate, then closure.
   5. Commit: chore(f069): claim F069 + reset live review. Gates (docs/
      roadmap touched → docs-round gate): python3 -m pytest tests/docs/ -q
      AND python3 -m pytest tests/cli/test_golden_path.py -q → both exit
      0. Push.

  GROUND MAP (read these before writing code; reuse, do not copy —
  if you are about to copy a prompt-building or call helper, EXTRACT a
  shared helper instead, per the feature file's Orchestrator brief):
   - Mission record: packages/orchestration/mission_state.py — Mission
     (:167), save_mission (:284), load_mission (:306), create_mission
     (:354), MISSION_SCHEMA_VERSION (:63). Storage: <data root>/missions/
     <project id>/<mission id>.json, atomic write.
   - DoD compiler (A6 — the ONLY DoD mechanism):
     packages/orchestration/dod_compiler.py — compile_dod (:375),
     deterministic_dod (:276). Schema: dod_schema.py (dod_v1).
   - Structured-call surface: packages/orchestration/
     structured_outputs.py — run_structured_call (:112), one parse retry
     max; validate_response in schemas/validation.py.
   - Schema + DAG discipline to mirror: packages/orchestration/schemas/
     models.py — FlightPlan._validate_dag (:190): no duplicates, no
     unknown deps, no cycles (DFS), hard cap. Versioned ids like
     FLIGHT_PLAN_SCHEMA_V ("flight_plan_v1") at models.py:31.
   - Prompt-shape precedents: intake.py _build_intake_prompt (:73),
     flight_plan.py _build_plan_prompt (:102), plan_job_llm (:348).
   - CLI: apps/cli/commands/mission_cmd.py (start :67, list :88, show
     :399). Tests: tests/orchestration/test_mission_compiler.py (new),
     tests/cli/test_mission_cmd.py; fixtures under
     tests/orchestration/fixtures/ (dod/ shows the golden convention).

  PHASE 2 — T001: schema + validation + compiler + fallback + fixtures
   Feature file: docs/roadmap/features/T1_F069.md — follow its Design.
   1. Schema MissionPlan, versioned "mission_plan_v1": milestones[], each
      {id, goal, rationale, dod_ref (empty until T002 fills it),
      depends_on, jobs_draft[] of {title, goal, est_band}}; risks[];
      assumptions[]. Validators, same discipline as
      FlightPlan._validate_dag: duplicate ids, unknown deps, cycles, cap
      12 milestones (reject as parse-class "hallucinated scope");
      outcome-phrased milestone lint — a documented heuristic rejecting
      obvious task-lists-as-milestones (imperative-verb-list starts).
   2. packages/orchestration/mission_compiler.py: compile(mission) →
      MissionPlan via provider call (mission goal + project facts,
      run_structured_call, allow_parse_retry=True) with honest
      deterministic fallback: ONE milestone wrapping the whole goal,
      labeled deterministic. jobs_draft entries are outlines, NEVER
      runnable jobs. Zero execution side effects.
   3. Three long-goal fixtures with golden milestone structures in
      tests/orchestration/ (follow the fixtures/dod/ golden convention,
      package-safe parametrize ids — F062 lesson: no slash inside a
      bracketed param id).
   Done when: python3 -m pytest tests/orchestration/
   test_mission_compiler.py -q → exit 0, AND python3 -m pytest
   tests/cli/test_golden_path.py -q → exit 0. Red → STOP rule.
   Commit(s) small (<500-line diffs), push.

  PHASE 3 — T002: DoD hand-off + persistence + rendering + no-autostart
   1. For each milestone invoke the F061 compiler (compile_dod — no
      second mechanism, Rule A6) and store the reference in dod_ref.
   2. Persist the MissionPlan on the mission record as an ADDITIVE
      OPTIONAL field (no breaking change to mission_state consumers; if
      you believe a schema-version bump is required, record that as a
      deviation with reasoning in the handoff, do not silently bump).
   3. Render mission_plan.md next to the mission's evidence (follow the
      existing evidence-rendering precedents, e.g. task_plan_evidence).
   4. No-autostart guarantee, pinned: a negative test proving compile
      creates ZERO jobs, starts nothing, touches no worktree.
   Done when: python3 -m pytest tests/orchestration/
   test_mission_compiler.py tests/orchestration/test_mission_state.py -q
   → exit 0, AND the canary → exit 0. Red → STOP rule. Commit(s), push.

  PHASE 4 — T003: CLI + recompile versioning + in-progress refusal
   1. remedy mission plan <id> in apps/cli/commands/mission_cmd.py:
      compiles, and recompiles keeping prior versions (like flight-plan
      replans).
   2. Recompile is REFUSED with a clear message once any milestone is in
      progress. Conservative rule: a milestone counts as in progress as
      soon as any real job attributable to it exists on the mission
      record; document the rule where it lives and pin it with a test.
      If the record's shape forces a different conservative rule, record
      the deviation in the handoff.
   3. Tests: CLI paths (plan, recompile-versioning, refusal) +
      compiler-level version retention.
   Done when: python3 -m pytest tests/orchestration/
   test_mission_compiler.py tests/cli/test_mission_cmd.py -q → exit 0,
   AND the canary → exit 0, AND git status --porcelain is EMPTY.
   Commit(s), push.

  DO NOT TOUCH (feature file): execution, job creation, dossier
  maintenance, loop policy. No harness/process-semantics changes. No
  mutation red-proofs outside a disposable git worktree (R-0160); primary
  checkout porcelain-clean at handback.

  HANDBACK
   Push first (R-0166: hand back only with a clean, committed, PUSHED
   branch). Completion report + rewrite .agent/handoff.md per
   docs/agents/handback_template.md: ALL commits tabled (grouped
   self-reference allowed, R-0149); raw transcripts (command, exit code,
   real output tail) for EVERY gate run; deviations & assumptions
   numbered; grep proof that both applied reviewer texts are
   byte-identical to their .agent/authored/ files. End with:
   "F069 R1 complete — awaiting review."

  --- BEGIN f069-r1-1 sha256=b6e33228ec68e6936693206b81b4c3a40251e02da57aedd9c8bff3bf5d7804c7 ---
  FROM (exact line, occurs once in docs/roadmap/STATUS.md, replace once):
  - [ ] F069 — Mission compiler
  TO:
  - [~] F069 — Mission compiler
  --- END f069-r1-1 ---

  --- BEGIN f069-r1-2 sha256=179664263e424e5895287f7b8516088a71801e6fd76d07e0f0330e24b8990049 ---
  # Live Review — F069 Mission compiler (Tier 1)

  Branch: feature/f069-mission-compiler
  Scope: a long prose goal compiles into a versioned MissionPlan —
  ordered milestones with a milestone DAG, each carrying a compiled
  DoD reference (via the F061 compiler, no second mechanism, A6) and
  draft job outlines that are explicitly NOT runnable; deterministic
  one-milestone fallback without a provider; CLI plan/recompile with
  version retention and in-progress refusal. Compiling creates no
  jobs, starts nothing, touches no worktree.

  ## Steps
  - R1 (SPLIT, LARGE bundle, operator LARGE-mode 2026-08-02): claim +
    T001 schema + milestone-DAG validation + compiler + deterministic
    fallback + three long-goal fixtures with golden milestone
    structures; THEN T002 per-milestone DoD hand-off + persistence on
    the mission record + mission_plan.md rendering + the no-autostart
    guarantee (negative test: compile leaves zero jobs); THEN T003
    CLI `remedy mission plan <id>` + recompile versioning +
    in-progress refusal — per-slice verification, stop-on-red.
  - Next: integration gate per docs/agents/integration_gate.md, then
    closure per docs/roadmap/STATUS_closure_protocol.md.

  ## Findings
  - Next free ID: R-0168.

  ## Verdicts
  - (pending R1 handback)
  --- END f069-r1-2 ---
