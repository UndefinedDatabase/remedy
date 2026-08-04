OUTCOME: in progress — F075 R5 (SPLIT, LARGE) started.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R5 (SPLIT, LARGE): persist the R4 PASS +
  build R-0186 (job execution wired into the loop) + cheap re-proof +
  campaign attempt 2. Save THIS ENTIRE block verbatim to
  .agent/last_block.md first (update OUTCOME at handback). You are on
  feature/f075-self-run-gauntlet at 49202f47. STOP rule: every phase
  ends with a verification; first red TEST gate -> STOP per AGENTS.md
  If-Blocked. Phase 3 has its own STOP. Commits < 500 lines, NO oversize
  left (R-0181) — slice the work; the matrix artifact commit in Phase 4
  is sliced too if needed.

  PHASE 1 — PERSIST THE R4 VERDICT (first commit)
   1. Save the three AUTHORED TEXT payloads below to
      .agent/authored/f075-r5-<n>.md (bytes between BEGIN/END markers,
      exclusive, incl. final newline; payload lines at column 0).
      Verify each sha256sum against its BEGIN-marker hash. Mismatch ->
      STOP, report raw sums, apply nothing.
   2. Apply f075-r5-1 -> .agent/live_review.md, f075-r5-2 ->
      .agent/plan.md, f075-r5-3 -> .agent/context.md — FULL
      replacements, byte-exact from the saved files.
   3. Commit 1: chore(f075): persist the R4 PASS, register R-0186.
      Gate: python3 -m pytest tests/cli/test_golden_path.py -q ->
      exit 0. Push.

  PHASE 2 — R-0186: THE LOOP EXECUTES WHAT IT DISPATCHES (own commits)
   The spec of record: the loop's own docstring verb map and
   T1_F070.md Design ("run it through the multi-cycle executor ->
   evaluate"). Reuse existing verbs ONLY — a second executor, DoD
   mechanism or approval path is a defect by the loop's own words.
   Record every interface decision in .agent/decisions.md.
   1. After a dispatch_job move creates and auto-approves its job
      (the existing continue_mission + auto_approve_flight_plan
      path), the SAME iteration runs the job through
      long_run_executor.run_cycles under the existing budget/stop/
      checkpoint semantics (F046/F047) — injectable through the
      loop's dependency parameters the same way dispatch already is,
      defaulting to the production verb. The DoD gate verdict comes
      from the EXISTING job-execution path (job_fulfillment ->
      run_job_gate) — do not call the gate from the loop directly.
      The move outcome records what execution produced (job terminal
      state, gate released or blocker) so declare_milestone_done
      becomes reachable on the loop's next iterations.
   2. Re-dispatch guard: evaluate_dispatch refuses a dispatch_job
      for a milestone whose linked job is still in flight (planned/
      running — inspect the real state names first), with a refusal
      message that tells the model what to do instead (wait /
      declare done when the gate released). The six-identical-
      dispatches loop from the R4 diagnosis must be impossible.
   3. Execution failures degrade through the R3 iteration boundary
      (a raising executor -> iteration_failed + classified
      postmortem + ledger entry), and the runner's injection seams
      keep working: dispatch remains the seam g08 fires at — verify
      the injection tests still hold unchanged.
   4. Tests (fake executor/gate deps — NO provider, NO real job
      execution in pytest, R-0182): a dispatched job is executed in
      the same iteration and its state advances; the gate verdict
      lands and is readable by the next iteration; a released gate
      makes declare_milestone_done acceptable; the re-dispatch guard
      refuses in-flight and allows after-terminal; a raising
      executor degrades through the boundary; budgets pass through;
      existing loop/e2e/era suites green UNEDITED except where an
      assertion pinned the old create-only behavior — list any such
      test per name in the handoff with the reason.
   5. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_orchestrator_loop.py
      tests/orchestration/test_mission_e2e.py
      tests/orchestration/test_era_integrity.py
      tests/orchestration/test_gauntlet_injection.py
      tests/orchestration/test_gauntlet_runner.py -q -> exit 0. Push.

  PHASE 3 — CHEAP RE-PROOF (one order, hard-gated)
   1. python3 scripts/self_run_gauntlet.py --live <fresh root OUTSIDE
      the repo> --only 1 --format json
   2. REQUIRED: the run reaches terminal `achieved` AND its run dir
      contains dod_result.json (the gate actually produced a
      verdict). Quote the terminal + the gate verdict fields in the
      handoff.
   3. Not achieved or no gate verdict -> STOP: commit nothing
      further, record both this run's and the R4 diagnostic run's
      evidence trails in .agent/decisions.md, hand back (the R4
      2c-precedent).

  PHASE 4 — CAMPAIGN ATTEMPT 2 (only after a green Phase 3)
   1. Preconditions in the handoff: porcelain empty, pushed, provider
      reachable, set_hash re-verified, preflight_injections -> [].
   2. ONE invocation, full ten, fresh root OUTSIDE the repo:
      --live <root> --format both. No rerun inside the attempt, no
      order edits; provider flakiness fails a run honestly (A9).
   3. Copy matrix.md + matrix.json into .agent/gauntlet/attempt-02/
      and commit, sliced under the cap. Evidence-root path + per-run
      terminals in the handoff.
   4. Gate: committed matrix.json parses, runs_recorded == 10; canary
      python3 -m pytest tests/cli/test_golden_path.py -q -> exit 0.
      The flawless count is REPORTED, not gated.

  PHASE 5 — HANDBACK
   git status --porcelain empty. Rewrite .agent/handoff.md per
   docs/agents/handback_template.md (per-commit tables; raw gate
   outputs; the Phase 3 proof quoted; if attempt 2 ran, its summary
   table verbatim; sha256 proof per applied reviewer text). Update
   last_block OUTCOME. Completion report ends:
   "F075 R5 complete — awaiting review." (append "attempt 2 matrix
   recorded" if Phase 4 ran).

  --- BEGIN f075-r5-1 sha256=5a6342c91a8c095c22d165b32c45b69a98a32d72160e9947e1e4031c339badab ---
  # Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

  Branch: feature/f075-self-run-gauntlet
  Scope: a gauntlet HARNESS — evaluator + matrix + a frozen ten-order
  set — that earns autonomy with data. Flawless per run = start
  command only + terminal green + blocking DoD green + zero unknown
  postmortems + zero open decisions + host data root byte-untouched.
  Product changes ride along ONLY as reviewed SPLIT work (so far: the
  run_mission exception boundary R3; failure_postmortem transport
  classes R4; the R-0186 execution wiring R5).

  ## Steps
  - R1-R3 (SPLIT, LARGE): harness + frozen set + boundary + all four
    injections + campaign attempt 1 (0/10, honest) — PASS x3
    (history).
  - R4 (SPLIT, LARGE): R-0185 + R-0183 fixed; R-0184 diagnosed with
    evidence, compliant 2c STOP — PASS, see Verdicts.
  - R5 (SPLIT, LARGE, current): persist R4 verdict + R-0186 — wire
    job EXECUTION into the loop (long_run_executor.run_cycles after
    dispatch, gate verdict via the existing job path, re-dispatch
    guard) — + cheap --only re-proof (must reach achieved with a
    gate verdict) + campaign attempt 2 from ONE invocation.
  - R6+: campaign iterations until 10/10 from one invocation; then
    the integration gate per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR.

  ## Findings
  - R-0178/R-0179/R-0180: fixed and reviewer-verified (history).
    Done: R-0178 · Done: R-0179 · Done: R-0180
  - R-0181 (process, Medium): two oversize commits in R3, second
    reviewer-ordered. Resolved by ruling; exemption SPENT. Resolved.
  - R-0182 (test-safety, Medium): real campaign inside pytest;
    fixed in-round, reviewer-verified. Done: R-0182
  - R-0183 (product, Low): unmeasured tokens rendered as 0/0. Fixed
    364c68ef (tokens_measured through evidence, md "unmeasured",
    json null+source; golden json regenerated, md byte-identical);
    reviewer reproduced both goldens. Done: R-0183
  - R-0185 (product, Medium): transport/machine failures classified
    unknown. Fixed 7202beca (ConnectionError -> the existing
    provider_unavailable; new io_failure; two documented predicates;
    falsification kept: unrecognizable stays unknown); both injected
    shapes end-to-end through record_iteration_failure;
    reviewer-verified. The honest-red first run (the worker's own R3
    test had used "HTTP 503" as its unclassifiable example) was an
    extension, not a weakening. Done: R-0185
  - R-0184 (product, High): campaign attempt 1 — zero runs reach
    achieved, the DoD gate never runs. DIAGNOSED in R4
    (decisions.md, raw quotes; reviewer re-verified every claim in
    source): the loop dispatches jobs — create-only via
    continue_mission — and NEVER executes them; run_cycles is
    imported for next_cycle_index only; run_job_gate's sole caller
    is job execution; six identical dispatches for one milestone
    because evaluate_dispatch does not refuse a milestone with an
    in-flight job. The model is NOT the blocker (six schema-valid,
    on-topic moves). T1_F070's Design specifies the executor step
    ("run it through the multi-cycle executor -> evaluate"); the
    build omitted it. Fix = R-0186.
  - R-0186 (product, High) 2026-08-04, from the R-0184 diagnosis:
    wire job execution into the loop — after a dispatch_job move
    creates and auto-approves its job, run it through the EXISTING
    long_run_executor.run_cycles (budgets, stops, checkpoints; no
    second executor) so the DoD gate verdict flows from the existing
    job-execution path; add the re-dispatch guard (evaluate_dispatch
    refuses a milestone whose job is still in flight); execution
    lives INSIDE the R3 iteration boundary. Done when a --only live
    run reaches achieved with a dod_result.json present and the
    loop/e2e/era suites stay green.
  - Next free ID: R-0187.

  ## Verdicts
  - R1: PASS. R2: PASS. R3: PASS. Full texts in this file's git
    history (55f706db, c95f23db, e5ca780e).
  - R4: PASS (SPLIT, LARGE, 2026-08-04). Range a4cb91ca..49202f47
    (5 commits, all tabled). Transport: r4-1/2/3 cmp 0 against the
    reviewer's scratchpad originals; live_review at the apply commit
    byte-equals the authored text. Reviewer re-ran every gate:
    classifier+loop 246, evidence/matrix/evaluator 123, remaining
    harness 121, canary 42 — all exit 0, porcelain empty — and
    reproduced BOTH goldens byte-exact post-regeneration. The 2c
    STOP is COMPLIANT and TRUE: every diagnosis claim re-verified in
    source by the reviewer (run_cycles absent from the loop,
    run_job_gate's one caller at job_fulfillment.py:1003,
    create-only dispatch, T1_F070.md line 9 specifying the executor
    step). The honest-red P2 first run was extension-not-weakening,
    cause explained per test. DECISION 2026-08-04 (§4.7): R-0186 is
    built IN THIS BRANCH as reviewed SPLIT work (the R3-boundary
    precedent; F075's acceptance depends on it and the executor verb
    already exists tested) — alternative, reopening F070 as its own
    feature, rejected as pure bookkeeping overhead for the same
    diff; reversal = any later relay. CLOSURE CANDIDATE noted for
    .agent/candidates.md at closure: F070 was accepted with a
    specified execution step unbuilt — its zero-provider evidence
    never ran a job, so no test could notice; gate-tooling/review
    -practice class. Worktree hygiene: primary only, porcelain
    empty. LAST_REVIEWED_SHA = 49202f47.
  --- END f075-r5-1 ---

  --- BEGIN f075-r5-2 sha256=d7d08f7feadbb4f8c6cb9e57139bd5b29042727c0091957fe20bffbc019ec44d ---
  # Plan — F075 MILESTONE GATE: 10 flawless self-runs

  Branch: feature/f075-self-run-gauntlet

  ## Goal
  Autonomy earned with data, not vibes: scripts/self_run_gauntlet.py
  runs ten frozen mission orders unattended and judges each against
  a strict, falsifiable pass definition (start command only, terminal
  green, blocking DoD green, zero unknown postmortems, zero open
  decisions, host data root byte-untouched). Matrix report (md+json)
  lands in a gauntlet evidence area; failed attempts are KEPT. DONE
  when 10/10 stands from ONE invocation and the prepared config diff
  + ADR name the evidence — applied by a human, never the harness.

  ## Current Step
  R5 (SPLIT, LARGE): persist R4 PASS + R-0186: after a dispatch_job
  move creates and auto-approves its job, the loop RUNS it through
  the existing long_run_executor.run_cycles under the mission's
  budgets, the DoD gate verdict flows from the existing
  job-execution path, and evaluate_dispatch refuses a milestone
  whose job is still in flight (the six-identical-dispatches loop).
  Execution sits INSIDE the R3 iteration boundary. Own tests with
  fake executor deps — no provider in pytest (R-0182). Then the
  cheap re-proof: one --only live run must reach achieved WITH a
  dod_result.json; only then campaign attempt 2 (full ten, ONE
  invocation, matrix to .agent/gauntlet/attempt-02/, sliced
  commits).

  ## Next Steps
  - R6+: campaign iterations until 10/10 from one invocation; then
    the integration gate.
  - Closure per STATUS_closure_protocol.md incl. config diff + ADR
    and the F070-review-gap closure candidate.

  ## Risks
  - The wiring must reuse the existing executor verb — a second
    execution mechanism is a defect by the loop's own docstring.
  - Executor raises inside an iteration must degrade through the R3
    boundary, not escape.
  - Real runs spend real tokens; provider flakiness fails a run
    honestly (A9).
  - Do-not-touch: config defaults by machine, order-set edits
    mid-campaign, the pass definition; the oversize exemption stays
    spent (R-0181).
  --- END f075-r5-2 ---

  --- BEGIN f075-r5-3 sha256=1d9bf4e8d61fa2e8a339182e655b855a949b1d6d4341a9ec0930072ee53711a4 ---
  # Context — F075 MILESTONE GATE: 10 flawless self-runs

  ## Active Branch
  feature/f075-self-run-gauntlet (from main after the Open PR Gate
  merged PR #178, the F071 closure)

  ## Scope
  Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
  harness + evaluator + matrix + frozen ten-order set + live runner
  + injection driver + their tests. Reviewed product changes: the
  run_mission exception boundary (R3), failure_postmortem transport
  classes (R4), and the R-0186 execution wiring (R5, DECISION in
  the R4 verdict) — run_cycles after dispatch, gate verdict via the
  existing job path, re-dispatch guard.

  ## Constraints
  - Round gate = scoped pytest command(s) authored in the step
    block; canary per handback:
    python3 -m pytest tests/cli/test_golden_path.py -q. Docs-round
    gate applies to any commit touching docs/roadmap/**:
    python3 -m pytest tests/docs/ -q. Full-suite pytest -n auto only
    at the integration gate; the resource-safety rules of
    tests/regression apply.
  - Commits < 500 lines, NO oversize left (R-0181 spent it);
    authored texts applied byte-exact from
    .agent/authored/f075-r5-<n>.md after sha256 verification.
  - No pytest test may take a production/provider path (R-0182).
  - Gauntlet runs use an ISOLATED data root; campaign evidence
    lives outside the repo during runs (R-0176); only matrix.md +
    matrix.json are committed under .agent/gauntlet/.
  - Do-not-touch: config defaults by machine, order-set edits
    mid-campaign; the pass definition freezes at campaign time.

  ## Steps
  R1-R4 done (PASS x4) → R5 R-0186 execution wiring + re-proof +
  attempt 2 (current) → R6+ iterations → integration gate → closure.
  --- END f075-r5-3 ---
