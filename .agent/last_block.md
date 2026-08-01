OUTCOME: executed — R-0165 fixed, dod_v1 registered in SCHEMA_REGISTRY,
integration gate run on branch AND base: both fully green (branch 14900 passed
/ 19 skipped, base 14744 / 19, exit 0 both), comm -13 and comm -23 both EMPTY,
worktree removed + pruned. No closure artifacts. See .agent/handoff.md and
.agent/gate_f061_r3/ for the raw evidence and six A9 deviations.

You are the WORKER for F061 — Definition-of-Done compiler (Tier 1), round R3.
  Authority: AGENTS.md. R2 is reviewed PASS. This round: R-0165 fix, the dod_v1
  registry registration, then the INTEGRATION GATE per
  docs/agents/integration_gate.md — read that file and follow it exactly; this
  block does not restate its sequence. STOP at the first red ordered gate
  (AGENTS.md If-Blocked) — an integration-gate regression is handed back as a
  normal repair round, not fixed ad hoc. Save THIS ENTIRE block verbatim to
  .agent/last_block.md first (append OUTCOME at handback).

  PHASE 1 — PERSIST FINDINGS + STATE (first commit)
  1. Save the three AUTHORED TEXT payloads below to
     .agent/authored/f061-r3-<n>.md (bytes between BEGIN/END markers,
     exclusive, including the final newline). Verify each sha256sum against its
     BEGIN-marker hash. Mismatch → STOP, report raw output, apply nothing.
  2. Apply by copy: f061-r3-1 → .agent/live_review.md, f061-r3-2 →
     .agent/plan.md, f061-r3-3 → .agent/context.md (each cmp → 0).
  3. Commit 1: chore(f061): persist R2 verdict + register R-0165
  4. Gate: python3 -m pytest tests/regression/test_resource_safety.py \
         tests/orchestration/test_test_runner.py -q      (state-file readers)

  PHASE 2 — FIX R-0165 (own commit)
  1. packages/orchestration/dod_schema.py, validate_check_spec runtime_flow
     branch: each step must have action == "open", a 'path' string starting
     with "/", and no keys outside {action, path, expect_status, expect_text};
     expect_status, when present, must be an int (or int-valued). Error
     messages name the step index and the violated rule.
  2. The RUNNER's run-time guards stay untouched — they defend stored DoDs
     written before this rule.
  3. Negative tests per rule in tests/orchestration/test_dod_compiler.py;
     the existing fixtures already use the v1 vocabulary and must pass
     UNCHANGED — if any fixture or golden needs an edit to stay green, STOP
     and hand back instead of editing it.
  4. Append exactly the line
     `  Done: R-0165 (commit <sha>).`
     under the R-0165 entry in .agent/live_review.md — nothing else changes.
     Own commit: fix(f061): compile-time runtime_flow step validation (R-0165)

  PHASE 3 — REGISTER dod_v1 (own commit, accepted R1 open item)
  1. packages/orchestration/schemas/models.py: add dod_v1 -> DoD to
     SCHEMA_REGISTRY following the file's existing pattern (import placement,
     ordering, comments). Registration lives in that module — not as an
     import side effect from dod_schema.py.
  2. Extend the existing registry test with the dod_v1 entry, same style as
     its neighbours. Also register dod_draft_v1 ONLY if the registry's own
     conventions include provider-facing draft schemas — decide by reading
     the file, state the decision in the handoff.
  3. Gate (red → STOP):
     python3 -m pytest tests/orchestration/test_dod_compiler.py \
         tests/orchestration/test_dod_runners.py \
         tests/orchestration/test_dod_gate.py -q
     python3 -m pytest tests/orchestration/schemas -q
     python3 -m pytest tests/cli/test_golden_path.py -q

  PHASE 4 — INTEGRATION GATE
  Follow docs/agents/integration_gate.md exactly. Base parity per the F056 R3
  precedent: throwaway worktree at the merge base on a throwaway branch, COPY
  apps/ui/node_modules + apps/ui/dist in, REMEDY_UI_NO_AUTO_BUILD=1. Full
  suite with pytest -n auto on branch AND base; attribute every branch-only
  failure per the gate doc's classes with per-id evidence; a branch-only
  failure not attributable to a pre-existing class → STOP and hand back (repair
  round). Remove + prune the worktree, delete the tmp branch, record
  `git worktree list` afterwards. Raw transcripts (command, exit code, tail)
  into the handoff — counts, ids, wall clock.

  Done when:   Phases 1–3 gates green; the integration gate ran on branch and
               base with every branch-only failure attributed; primary
               checkout `git status --porcelain` empty at handback.
  Handback:    Completion report + REWRITE .agent/handoff.md: review range
               ("Review of ef60758b..HEAD"), per-commit changed-files table,
               raw transcripts for every gate and both full-suite runs,
               authored-text proofs (sha256sum + cmp + the exact live_review
               diff), the dod_draft_v1 registration decision, deviations &
               assumptions. NO closure artifacts: no STATUS edit, no README
               edit, no evidence job, no zip — closure is its own round.
  ──────────────────────────────────────────────────────────────

  ----- BEGIN AUTHORED f061-r3-1 sha256=afdddec6f97e2ceb59783c34fb17d2b3a65bd2a49ccf008af47a26cfdd1b4339 -----
  # Live Review — F061 Definition-of-Done compiler (Tier 1)

  Branch: feature/f061-dod-compiler
  Scope: user intent + Flight Plan compile into a machine-checkable DoD
  (versioned schema; checks with blocking flags); runners execute checks
  with per-check evidence; the job-end gate holds a job open on a red
  blocking check. Compiler is an LLM step with intake/plan discipline:
  schema-enforced, parse-retried, honest deterministic fallback labeled
  compiled=false.

  ## Steps
  - R1 (LARGE): T001 schema + compiler + fallback + fixtures +
    traceability, T002 runners red+green per kind — PASS.
  - R2 (LARGE): R-0164 fix, T003 runtime_flow runner on the F007
    harness + fixture app flow, T004 job-end gate + report matrix +
    `remedy job dod` + end-to-end hold/release — PASS.
  - R3: persist + fix R-0165, register dod_v1 in SCHEMA_REGISTRY
    (accepted R1 open item), then the integration gate per
    docs/agents/integration_gate.md — awaiting handback.
  - Later: closure is its own round.

  ## Findings
  - Resolved: R-0164 (hardening, Low) 2026-08-01: validate_check_spec
    accepted flag-shaped first tokens (pytest selector, lint/build
    tool, custom_cmd argv[0]); a flag-shaped selector landed in the
    pytest argv as an option and silently changed what runs. Fixed:
    _reject_flag_shaped on the three named fields, one negative test
    per field plus dash-elsewhere-still-legal pins.
    Done: R-0164 (commit af5c39d7).
  - Open: R-0165 (hardening, Low) 2026-08-01: the runtime_flow v1
    action vocabulary is enforced only by the RUNNER
    (unknown_flow_action at run time); the schema still accepts any
    step object with a non-empty action. The feature file orders
    detectable nonsense refused at compile time, and an unknown action
    or a non-"/" path is detectable there. Registered from the
    worker's own declared deviation 2 — correctly scoped out of R2,
    ordered now. Fix: validate_check_spec runtime_flow branch requires
    action == "open" and a 'path' starting with "/", allows only the
    step keys {action, path, expect_status, expect_text}; negative
    tests per rule; the runner's run-time guard stays (defence for
    stored DoDs written before this rule).
  - Next free ID: R-0166.

  ## Verdicts
  - R1: PASS (SPLIT round, 2026-08-01). Range 1869d89a..785f8cbd.
    Scoped 89 + docs 293 + canary 42, all reviewer-run, exit 0;
    transport cmp 0 disk-to-disk (all four texts, scratchpad
    originals); A9 deviations 1–10 accepted; R-0164 registered.
    LAST_REVIEWED_SHA = 785f8cbd.
  - R2: PASS (SPLIT round, 2026-08-01). Range 785f8cbd..ef60758b.
    Reviewer re-ran at HEAD: scoped 140 passed, adjacent
    job_fulfillment + run_report 177 passed — exit 0; tree
    porcelain-empty; `git worktree list` = primary only. Transport:
    all three authored texts cmp 0 disk-to-disk against scratchpad
    originals; plan/context cmp 0; live_review differs by exactly the
    ordered Done line; docs/ untouched (empty diff). Seam audited in
    situ (job_fulfillment.run_job_fulfill): the gate sits after the
    contract check, RunState.COMPLETED is reachable only through the
    branch the gate guards, a hold routes through the EXISTING blocked
    machinery, and a job without a stored DoD returns None — additive,
    one seam, provable by reading the branch. End-to-end drives the
    real run_job_fulfill: hold on red blocking, release after fix,
    matrix recorded, timeline event. Worker deviations 1–11 ACCEPTED,
    notably: runtime spec from project config not from the check;
    action vocabulary runner-enforced (promoted to R-0165); four
    report goldens updated to keep the not-recorded convention; hold
    via the existing blocked branch with a dod_blocking_red-prefixed
    blocker; three additive record fields, None = never gated. R-0164
    verified fixed in the diff and marked Done. Round tier: scoped
    gates + canary + state-file readers, plus the worker's adjacent
    runs (tests/cli 1231, tests/docs 293) — the full suite remains
    R3's integration gate. No mutation checks ran.
    LAST_REVIEWED_SHA = ef60758b.
  ----- END AUTHORED f061-r3-1 -----

  ----- BEGIN AUTHORED f061-r3-2 sha256=0ff1ba92934894f37735f412fae47fc66e9e92746e71693db58dfd9b273b8a46 -----
  # Plan — F061 Definition-of-Done compiler

  ## Goal
  "Done" stops being vibes: user intent plus the Flight Plan compile
  into a machine-checkable DoD — a versioned list of concrete checks
  (pytest, lint, build, runtime_flow, custom_cmd) with blocking flags —
  and a job only ends green when all blocking checks pass. T001–T004
  are built and reviewed PASS: schema, compiler with deterministic
  fallback, four process runners plus the runtime_flow runner on the
  F007 harness, and the job-end gate with report matrix and
  `remedy job dod`.

  ## Current Step
  R3: fix R-0165 (runtime_flow v1 step vocabulary validated at compile
  time: action == "open", path starts with "/", closed step-key set;
  the runner's run-time guard stays), register dod_v1 in
  SCHEMA_REGISTRY (accepted R1 open item), re-run the scoped gates,
  then the integration gate per docs/agents/integration_gate.md —
  branch full suite vs base full suite, failure classes attributed,
  only this round may claim "full suite green".

  ## Next Steps
  - Closure per docs/roadmap/STATUS_closure_protocol.md (own round:
    Built State, preconditions, evidence job, fresh review zip,
    STATUS [x] + README sync, PR).

  ## Risks
  - The integration gate compares against base in a throwaway
    worktree — UI build-artifact parity (copy apps/ui/node_modules +
    apps/ui/dist, REMEDY_UI_NO_AUTO_BUILD=1) per the F056 R3
    precedent; a branch-only failure is a normal repair round.
  - Production wiring that COMPILES a DoD at job creation is
    downstream scope (F062 product smoke registers standard checks;
    F069/F070 consume the seam) — not part of this feature's Done.
  ----- END AUTHORED f061-r3-2 -----

  ----- BEGIN AUTHORED f061-r3-3 sha256=4501430fe7acd484b3a260eda414ebe62b9fe5bcd0b84c8d9307739350f6f250 -----
  # Context — F061 Definition-of-Done compiler (Tier 1)

  ## Active Branch
  `feature/f061-dod-compiler`
  Base commit: main after PR #171 merge (F056)

  ## Steps (round map)
  R1 (LARGE, PASS): claim + T001 schema/compiler/fallback/fixtures/
  traceability + T002 runners red+green per kind.
  R2 (LARGE, PASS): R-0164 fix + T003 runtime_flow runner + T004
  job-end gate + matrix + CLI + end-to-end hold/release.
  R3: R-0165 fix + dod_v1 SCHEMA_REGISTRY registration + integration
  gate per docs/agents/integration_gate.md. Closure is its own later
  round.

  ## Scope
  `packages/orchestration/dod_schema.py` (R-0165 step validation),
  `packages/orchestration/schemas/models.py` (register dod_v1, one
  line + its registry test), `tests/orchestration/test_dod_compiler.py`
  (negative tests), the integration-gate evidence, and `.agent/`
  state. Nothing beyond.

  ## Gates (round verification, pytest)
  python3 -m pytest tests/orchestration/test_dod_compiler.py \
      tests/orchestration/test_dod_runners.py \
      tests/orchestration/test_dod_gate.py -q     scoped gate
  python3 -m pytest tests/orchestration/schemas -q  registry gate
  python3 -m pytest tests/cli/test_golden_path.py -q  canary
  Integration gate: full suite with pytest -n auto, branch AND base,
  per docs/agents/integration_gate.md — only this round claims "full
  suite green".
  Resource safety: everything runs through these pytest wrappers; no
  unbounded subprocess fan-out from gate tooling.

  ## Constraints
  - R-0165: compile-time step validation (action == "open", path
    starts with "/", closed key set {action, path, expect_status,
    expect_text}); the runner's unknown_flow_action guard STAYS as
    defence for previously stored DoDs.
  - dod_v1 registration follows the existing SCHEMA_REGISTRY pattern
    in schemas/models.py — registration lives in that module, not as
    an import side effect elsewhere.
  - Fixture steps already use the v1 vocabulary; goldens must not
    need changes — if one does, STOP and report instead of editing.
  - Base-parity in the integration gate: copy apps/ui/node_modules +
    apps/ui/dist into the throwaway worktree,
    REMEDY_UI_NO_AUTO_BUILD=1 (F056 R3 precedent).
  - Reviewer-authored texts under .agent/authored/ are applied by copy
    and sha256-verified before use; never hand-edited.
  - Commits stay under 500-line diffs (AGENTS.md).
  - context.md satisfies its FULL test reader list: a "Steps" section,
    "## Active Branch" with a feature/ slug, a roadmap F-id, and this
    pytest/resource line (R-0162; reader rule in
    planner_reviewer_prompt.md §4 item 11).

  ## Do not touch
  Visual regression, deep browser automation, Tier-11 verification
  depth. docs/roadmap/ROADMAP.md and all of docs/roadmap/STATUS.md
  this round. Job-lifecycle behavior beyond the existing gate seam.
  No closure artifacts this round.
  ----- END AUTHORED f061-r3-3 -----
