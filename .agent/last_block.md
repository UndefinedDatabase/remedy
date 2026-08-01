OUTCOME: executed — R-0164 fixed, T003 and T004 delivered; all slice gates and
the full Done-when set green at d76a8f32. The feature's build work is complete
(T001–T004). See .agent/handoff.md for transcripts, the declared T004 seam,
authored-text proofs and eleven A9 deviations.

You are the WORKER for F061 — Definition-of-Done compiler (Tier 1), round R2.
  Authority: AGENTS.md. Feature file: docs/roadmap/features/T1_F061.md. R1
  (T001+T002) is reviewed PASS. This round finishes the feature's build work:
  R-0164 fix, then T003, then T004. STOP at the first red gate (AGENTS.md
  If-Blocked) and hand back with the raw failure. Save THIS ENTIRE block
  verbatim to .agent/last_block.md first (append OUTCOME at handback).

  PHASE 1 — PERSIST FINDINGS + STATE (first commit, before any fix)
  1. Save the three AUTHORED TEXT payloads below: for each, copy EXACTLY the
     lines between its BEGIN and END markers (exclusive, including the final
     newline) to .agent/authored/f061-r2-<n>.md. Verify each:
     sha256sum .agent/authored/f061-r2-<n>.md  must equal its BEGIN-marker
     hash. Mismatch → STOP, report raw sha256sum output, apply nothing.
  2. Apply by copy: f061-r2-1 → .agent/live_review.md, f061-r2-2 →
     .agent/plan.md, f061-r2-3 → .agent/context.md (each cmp → 0).
  3. Commit 1: chore(f061): persist R1 verdict + register R-0164
  4. Gate: python3 -m pytest tests/regression/test_resource_safety.py \
         tests/orchestration/test_test_runner.py -q      (state-file readers)

  PHASE 2 — FIX R-0164 (own commit)
  1. In packages/orchestration/dod_schema.py, validate_check_spec: refuse
     values whose first non-whitespace character is "-" for pytest
     'selector', lint/build 'tool', and custom_cmd argv[0]. Error message
     names the field and the offending value.
  2. Tests: one negative test per field in
     tests/orchestration/test_dod_compiler.py (schema section).
  3. Mark the fix "Done: R-0164" by appending exactly the line
     `  Done: R-0164 (commit <sha>).` under the R-0164 entry in
     .agent/live_review.md — nothing else in that file changes.
  4. RE-RUN the R1 gate:
     python3 -m pytest tests/orchestration/test_dod_compiler.py \
         tests/orchestration/test_dod_runners.py -q
     python3 -m pytest tests/cli/test_golden_path.py -q
     If not green now → STOP the block here and hand back.

  ── STEP T003+T004/4 — F061 ────────────────────────────────────
  Goal:        The runtime_flow runner on the harness (T003), then the
               job-end gate + report matrix + end-to-end (T004).
  Bundle:
    T003 — runtime_flow runner + fixture app flow
      - INSPECT FIRST: packages/runtimes/runtime_supervisor.py and
        dev_server.py (F007). Reuse their start/stop discipline — do not
        reinvent process management.
      - Extend packages/orchestration/dod_runners.py: a runtime_flow check
        drives the harness — start the app, execute the declarative steps in
        order (v1 actions: open a path, expect text and/or status), stop the
        app (ALWAYS stopped, also on failure). No browser automation, no new
        dependency.
      - Evidence stays CheckEvidence: per-flow command/argv analog, duration,
        output tail (step log), red with a NAMED reason (e.g. app_start_failed,
        flow_step_failed, timeout) — never a silent pass. The loud
        UnsupportedCheckKindError guarantee remains for kinds without runners.
      - Generated flow specs (when the compiler emits them) belong under the
        job's evidence area (data root), never the user's repo — assert the
        path in a test if you touch that surface.
      - Fixture: a tiny harness-startable app under
        tests/orchestration/fixtures/ + the api_service fixture's api-smoke
        flow proven RED and GREEN against it.
      - Tests: extend tests/orchestration/test_dod_runners.py.
      T003 GATE (red → STOP):
        python3 -m pytest tests/orchestration/test_dod_compiler.py \
            tests/orchestration/test_dod_runners.py -q
        python3 -m pytest tests/cli/test_golden_path.py -q
    T004 — job-end gate + report matrix + CLI + e2e
      - INSPECT FIRST: the terminal-green path in
        packages/orchestration/job_runner.py / job_fulfillment.py. Wire the
        gate at ONE seam — the smallest that provably intercepts the
        job-going-green transition; prefer a new
        packages/orchestration/dod_gate.py that the seam calls. Declare the
        chosen seam in the handoff.
      - Behavior: on the terminal-green path the DoD runs; ANY red BLOCKING
        check keeps the job open with status blocked and the check matrix in
        the report; non-blocking reds are reported, not gating; after a fix
        the gate releases (job ends green). Green requires ALL blocking
        checks green.
      - Report: the check matrix (id, kind, blocking, status, reason,
        duration) rendered by packages/orchestration/run_report.py, from
        structured evidence like the existing sections.
      - CLI: remedy job dod <id> shows the matrix live; follow the existing
        job-command conventions; test beside the existing CLI job tests.
      - End-to-end test: a job goes green only when all blocking checks are
        green; a red blocking check holds it open (status blocked, matrix
        present); the same job releases after the fix. Use fixture-level
        jobs, not a live provider.
      - Tests: tests/orchestration/test_dod_gate.py (new) + the CLI test.
      T004 GATE (red → STOP):
        python3 -m pytest tests/orchestration/test_dod_gate.py -q
        python3 -m pytest tests/cli/test_golden_path.py -q
  Change:      ONLY: dod_schema.py (R-0164 guard), dod_runners.py,
               dod_gate.py (or the declared seam), run_report.py (matrix),
               the CLI command, the named tests + fixtures, .agent/ state.
               Nothing else. docs/roadmap/** untouched this round.
  Constraints: A9 defaults for unspecified details — record every one in the
               handoff. Job-lifecycle behavior beyond the single gate seam
               untouched. Commits <500-line diffs, multiple commits expected.
               Mandatory self-review loop before every commit. Mutation
               red-proofs only in a disposable git worktree, removed + pruned.
  Done when:   All slice gates green (raw transcripts) plus final:
               python3 -m pytest tests/orchestration/test_dod_compiler.py \
                   tests/orchestration/test_dod_runners.py \
                   tests/orchestration/test_dod_gate.py -q
               python3 -m pytest tests/cli/test_golden_path.py -q
               python3 -m pytest tests/regression/test_resource_safety.py \
                   tests/orchestration/test_test_runner.py -q
               git status --porcelain  → empty
  Handback:    Completion report + REWRITE .agent/handoff.md: review range
               line ("Review of 785f8cbd..HEAD"), per-commit changed-files
               table, raw verification transcripts (command, exit code, real
               output), authored-text proofs (sha256sum + cmp outputs), the
               chosen T004 seam with rationale, deviations & assumptions.
               STOP at the first red gate and hand back with the raw failure.
  ──────────────────────────────────────────────────────────────

  ----- BEGIN AUTHORED f061-r2-1 sha256=47c01f1e8de3a1eb39cf9b69fc40fb57bc0a2b817c8ae91460eabefa958e7d6f -----
  # Live Review — F061 Definition-of-Done compiler (Tier 1)

  Branch: feature/f061-dod-compiler
  Scope: user intent + Flight Plan compile into a machine-checkable DoD
  (versioned schema; checks with blocking flags); runners execute checks
  with per-check evidence; the job-end gate (T004) holds a job open on a
  red blocking check. Compiler is an LLM step with intake/plan
  discipline: schema-enforced, parse-retried, honest deterministic
  fallback labeled compiled=false.

  ## Steps
  - R1 (LARGE): T001 schema + compiler + deterministic fallback + three
    fixture missions with golden DoDs + acceptance-traceability rule,
    then T002 runners (pytest/lint/build/custom_cmd) with per-check
    evidence, each kind proven red and green — PASS.
  - R2 (LARGE): persist + fix R-0164, then T003 runtime_flow runner on
    the runtime harness + fixture app flow, then T004 job-end gate +
    report matrix + CLI matrix view + end-to-end — awaiting handback.
  - Later: integration gate; closure is its own round.

  ## Findings
  - Open: R-0164 (hardening, Low) 2026-08-01: validate_check_spec
    accepts flag-shaped first tokens — a pytest selector like "-x" (or
    a lint/build tool, or custom_cmd argv[0], like "--version") passes
    compile-time validation; a flag-shaped selector then lands in the
    pytest argv as an option and silently changes what runs. The
    feature file orders detectable nonsense refused at compile time.
    Fix: refuse values starting with "-" for pytest selector, lint/build
    tool, and custom_cmd argv[0] in validate_check_spec; one negative
    test per field.
  - Next free ID: R-0165.

  ## Verdicts
  - R1: PASS (SPLIT round, 2026-08-01). Range 1869d89a..785f8cbd.
    Reviewer re-ran at HEAD: scoped 89 passed, tests/docs 293 passed,
    canary 42 passed — all exit 0; tree porcelain-empty; `git worktree
    list` = primary only. Transport: all four authored texts cmp 0
    disk-to-disk against the reviewer scratchpad originals (primary
    proof); applied live_review/plan/context each cmp 0 against their
    authored files; STATUS TO-line occurs exactly once, FROM-line zero
    times. The worker's declared A9 deviations 1–10 ACCEPTED, notably:
    SCHEMA_REGISTRY registration deferred (registry has no production
    consumer; one-line follow-up), provider answers in DoDDraft so it
    cannot label provenance or claim compiled, acceptance checks group
    by selector (rule asks coverage, not duplicate processes),
    executable allowlist shared with test_runner, F017 fences enforced
    as execution location, runners return evidence not verdicts (gate
    is T004). Phase-0 deviation (last_block.md checkout collision,
    recovered, no content lost, net effect exactly the gate's order)
    ACCEPTED. Round tier: scoped gates + canary + docs gate. R-0164
    registered (Low); fix ordered in R2. No mutation checks ran.
    LAST_REVIEWED_SHA = 785f8cbd.
  ----- END AUTHORED f061-r2-1 -----

  ----- BEGIN AUTHORED f061-r2-2 sha256=a762a076567ea05419052e469b78f256768ba80458a8e98ad765c3c71b88162f -----
  # Plan — F061 Definition-of-Done compiler

  ## Goal
  "Done" stops being vibes: user intent plus the Flight Plan compile
  into a machine-checkable DoD — a versioned list of concrete checks
  (pytest, lint, build, runtime_flow, custom_cmd) with blocking flags —
  and a job only ends green when all blocking checks pass. Three fixture
  missions compile into sensible DoDs; every plan acceptance line is
  traceable to at least one check id; the fallback DoD (no provider) is
  deterministic and labeled compiled=false.

  ## Current Step
  R2 (LARGE bundle, rest of the feature): persist + fix R-0164
  (flag-shaped first tokens refused at compile time), then T003 — the
  runtime_flow runner driving the runtime harness (start → declarative
  steps: open path, expect text/status → stop) plus a fixture app flow
  proven red and green; then T004 — the job-end gate (a red BLOCKING
  check holds the job open with status blocked; non-blocking reds are
  reported, not gating; the gate releases after a fix), the report
  check matrix, `remedy job dod <id>`, and the end-to-end proof.

  ## Next Steps
  - Integration gate round per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md.

  ## Risks
  - T004 touches the terminal-green path of the job lifecycle — the
    smallest seam wins; inspect job_runner/job_fulfillment first and
    wire the gate at one point, never scattered.
  - runtime_flow drives the runtime supervisor (F007) — reuse its
    start/stop discipline; v1 steps stay declarative, no browser
    automation dependency.
  - Generated runtime-flow specs belong under the job's evidence area
    (data root), never in the user's repo.
  ----- END AUTHORED f061-r2-2 -----

  ----- BEGIN AUTHORED f061-r2-3 sha256=3b808727fb2ec4412a9c24277dcd3fcd8328771c31909311adf15c48b10f23a3 -----
  # Context — F061 Definition-of-Done compiler (Tier 1)

  ## Active Branch
  `feature/f061-dod-compiler`
  Base commit: main after PR #171 merge (F056)

  ## Steps (round map)
  R1 (LARGE, PASS): claim + T001 schema/compiler/fallback/fixtures/
  traceability + T002 runners red+green per kind.
  R2 (LARGE): R-0164 fix → T003 runtime_flow runner on the harness +
  fixture app flow → T004 job-end gate + report matrix + CLI view +
  end-to-end. Then integration gate; closure is its own later round.

  ## Scope
  `packages/orchestration/dod_schema.py` (R-0164 guard),
  `packages/orchestration/dod_runners.py` (runtime_flow runner),
  `packages/orchestration/dod_gate.py` (new, or the smallest seam the
  inspection of job_runner/job_fulfillment justifies — declared either
  way), report matrix in `packages/orchestration/run_report.py`, CLI
  `remedy job dod <id>`, plus `tests/orchestration/test_dod_runners.py`
  (extended), `tests/orchestration/test_dod_gate.py` (new), a CLI test
  beside the existing job-command tests, and a harness-startable
  fixture app under tests/orchestration/fixtures/. Also `.agent/`
  state. Nothing beyond.

  ## Gates (round verification, pytest)
  python3 -m pytest tests/orchestration/test_dod_compiler.py \
      tests/orchestration/test_dod_runners.py -q   R-0164 + T003 gate
  python3 -m pytest tests/orchestration/test_dod_gate.py -q   T004 gate
  python3 -m pytest tests/cli/test_golden_path.py -q          canary
  python3 -m pytest tests/regression/test_resource_safety.py \
      tests/orchestration/test_test_runner.py -q   state-file readers
  Resource safety: everything runs through these pytest wrappers; no
  unbounded subprocess fan-out from runner or gate tooling.

  ## Constraints
  - A red BLOCKING check holds the job open with status blocked and
    the matrix in the report; non-blocking reds are reported, never
    gating; the gate releases after a fix. Green only when all
    blocking checks are green.
  - runtime_flow v1 steps are declarative (open path, expect
    text/status) — NO browser-automation dependency; reuse the
    runtime supervisor's start/stop discipline (F007).
  - Generated runtime-flow specs land under the job's evidence area
    (data root), not the user's repo.
  - A flow that cannot run is red with a named reason — never a
    silent pass; the loud-unsupported-kind guarantee holds for any
    kind still lacking a runner.
  - Reviewer-authored texts under .agent/authored/ are applied by copy
    and sha256-verified before use; never hand-edited.
  - Commits stay under 500-line diffs (AGENTS.md).
  - context.md satisfies its FULL test reader list: a "Steps" section,
    "## Active Branch" with a feature/ slug, a roadmap F-id, and this
    pytest/resource line (R-0162; reader rule in
    planner_reviewer_prompt.md §4 item 11).

  ## Do not touch
  Visual regression, deep browser automation (the smoke feature
  decides), Tier-11 verification depth. docs/roadmap/ROADMAP.md and
  all of docs/roadmap/STATUS.md this round. Job-lifecycle behavior
  beyond the single T004 gate seam.
  ----- END AUTHORED f061-r2-3 -----
