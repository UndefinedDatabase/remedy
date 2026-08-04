OUTCOME: in progress — F075 R6 (SPLIT, LARGE) started.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R6 (SPLIT, LARGE): persist the R5 PASS +
  R-0187 (cycles experiment vehicle + order-set v2) + R-0188 (production
  DoD path) + re-proof + the first set-v2 campaign. Save THIS ENTIRE
  block verbatim to .agent/last_block.md first (update OUTCOME at
  handback). You are on feature/f075-self-run-gauntlet at 32e5e419.
  STOP rule: every phase ends with a verification; first red TEST gate
  -> STOP per AGENTS.md If-Blocked. Phase 4 has its own hard STOP.
  Commits < 500 lines, NO oversize left (R-0181) — slice everything.

  PHASE 1 — PERSIST THE R5 VERDICT (first commit)
   1. Save the three AUTHORED TEXT payloads below to
      .agent/authored/f075-r6-<n>.md (bytes between BEGIN/END markers,
      exclusive, incl. final newline; payload lines at column 0).
      Verify each sha256sum against its BEGIN-marker hash. Mismatch ->
      STOP, report raw sums, apply nothing.
   2. Apply f075-r6-1 -> .agent/live_review.md, f075-r6-2 ->
      .agent/plan.md, f075-r6-3 -> .agent/context.md — FULL
      replacements, byte-exact from the saved files.
   3. Commit 1: chore(f075): persist the R5 PASS, register
      R-0187/R-0188. Gate: python3 -m pytest
      tests/cli/test_golden_path.py -q -> exit 0. Push.

  PHASE 2 — R-0187: THE CYCLES EXPERIMENT VEHICLE (own commits)
   1. long_run_executor: an EXPLICIT override parameter with a loud
      name (suggested: experiment_max_cycles, docstring naming F075
      as its only intended caller) that may exceed CYCLE_SAFETY_CAP.
      resolve_max_cycles' clamping of flag and config is UNCHANGED —
      pin BOTH directions with tests (flag>cap still clamped,
      config>cap still clamped, override>cap honored, override
      absent -> exactly today's behavior). The resolved cycles
      (requested/allowed/source/override) are recorded in the run
      log / job evidence so no run can exceed the cap silently.
   2. Order-set v2: every order's budget gains a required
      max_cycles (positive int, chosen per order's rationale —
      two-milestone missions need more than a doc order). Manifest:
      gauntlet_order_set_version 2, fresh per-file sha256 + set
      hash. The campaign count resets per T1_F075.md A9 — nothing
      is lost, no passing attempt exists. Update gauntlet_orders
      (BUDGET_KEYS + set version) and the order tests (all existing
      freeze/tamper pins must hold against v2).
   3. Runner: pass the order's max_cycles through the execution
      path (RunnerDeps seam -> execute_dispatched_job -> the
      override parameter); run.json records the cycles used (e.g.
      cycles budget + resolved value) so the matrix's facts stay
      honest.
   4. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_gauntlet_orders.py
      tests/orchestration/test_gauntlet_runner.py
      tests/orchestration/test_orchestrator_loop.py
      <the long_run_executor test file(s) — real names in the
      handoff> -q -> exit 0. Push.

  PHASE 3 — R-0188: THE PRODUCTION DoD PATH (own commits)
   Inspect the real shapes FIRST (dod_gate.store_dod / DoD,
   mission_plan dod_ref -> dod_<milestone>.json, load_gate_result's
   read location); record wiring decisions in .agent/decisions.md.
   1. At dispatch (the continue_mission path in execute_move): the
      dispatched job gets its milestone's COMPILED DoD stored via
      store_dod — the F069 dod_ref artifact, no recompilation, no
      second DoD mechanism. A milestone without a compiled DoD
      stores nothing and the gate stays un-run for that job (honest
      absence, the evaluator already reports it).
   2. At PRODUCTION completion inside the execution wiring
      (execute_dispatched_job, after run_cycles returns): invoke
      run_job_gate(job_id, repo_root) and persist its verdict
      exactly where load_gate_result reads it — ONE author, no
      second store, the demo fulfillment untouched. The move
      outcome detail carries released/blocker (it already carries
      terminal/status).
   3. Tests (fakes only, R-0182): dispatch stores the DoD; a
      completed job gets a persisted gate verdict readable via
      load_gate_result; released gate -> declare_milestone_done
      acceptable -> a fake mission achieves end-to-end; blocked
      gate -> milestone not claimable and the loop's next context
      shows the blocker; no-DoD milestone -> no verdict, honest
      absence. Existing suites green; list any test whose
      assertion pinned the old gate-less behavior, per name, with
      reason.
   4. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_orchestrator_loop.py
      tests/orchestration/test_mission_e2e.py
      tests/orchestration/test_era_integrity.py
      tests/orchestration/test_gauntlet_injection.py
      tests/orchestration/test_gauntlet_runner.py
      <the dod_gate test file — real name in the handoff> -q ->
      exit 0. Push.

  PHASE 4 — RE-PROOF (one order, hard-gated)
   1. python3 scripts/self_run_gauntlet.py --live <fresh root OUTSIDE
      the repo> --only 1 --format json
   2. REQUIRED: terminal `achieved` AND dod_result.json present in
      the run dir with a released verdict. Quote both in the
      handoff, plus the recorded cycles override.
   3. Either missing -> STOP: commit nothing further, record the
      full evidence trail in .agent/decisions.md, hand back (the R4
      2c / R5 3.3 precedent).

  PHASE 5 — CAMPAIGN, SET v2 ATTEMPT (only after a green Phase 4)
   1. Preconditions in the handoff: porcelain empty, pushed,
      provider reachable, set_hash (v2) re-verified,
      preflight_injections -> [].
   2. ONE invocation, full ten: --live <fresh root OUTSIDE the repo>
      --format both. No rerun inside the attempt, no order edits;
      provider flakiness fails a run honestly (A9).
   3. Copy matrix.md + matrix.json into .agent/gauntlet/attempt-02/
      and commit, sliced under the cap; the handoff states set
      version 2 and the count reset. Evidence-root path + per-run
      terminals in the handoff.
   4. Gate: committed matrix.json parses, runs_recorded == 10;
      canary python3 -m pytest tests/cli/test_golden_path.py -q ->
      exit 0. The flawless count is REPORTED, not gated.

  PHASE 6 — HANDBACK
   git status --porcelain empty. Rewrite .agent/handoff.md per
   docs/agents/handback_template.md (per-commit tables; raw gate
   outputs; the Phase 4 proof quoted; if Phase 5 ran, its summary
   table verbatim; sha256 proof per applied reviewer text). Update
   last_block OUTCOME. Completion report ends:
   "F075 R6 complete — awaiting review." (append "set-v2 attempt
   matrix recorded" if Phase 5 ran).

  --- BEGIN f075-r6-1 sha256=701dbe2601fa5a08434e4ffbe2c44cc43b93aac816a45855992c2587f09dfe1b ---
  # Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

  Branch: feature/f075-self-run-gauntlet
  Scope: a gauntlet HARNESS — evaluator + matrix + a frozen ten-order
  set — that earns autonomy with data. Flawless per run = start
  command only + terminal green + blocking DoD green + zero unknown
  postmortems + zero open decisions + host data root byte-untouched.
  Product changes ride along ONLY as reviewed SPLIT work: the
  run_mission exception boundary (R3), failure_postmortem transport
  classes (R4), the R-0186 execution wiring (R5), the R-0187 cycles
  experiment vehicle and the R-0188 production DoD path (R6).

  ## Steps
  - R1-R4 (SPLIT, LARGE): harness + frozen set + boundary + four
    injections + attempt 1 (0/10) + R-0184 diagnosis — PASS x4
    (history).
  - R5 (SPLIT, LARGE): R-0186 built and live-proven (job executes,
    guard works); compliant 3.3 STOP on two blockers — PASS, see
    Verdicts.
  - R6 (SPLIT, LARGE, current): persist R5 verdict + R-0187 (cycles
    experiment vehicle + order-set v2 with per-order max_cycles) +
    R-0188 (store_dod at dispatch, run_job_gate at production
    completion) + re-proof (--only 1 must reach achieved WITH
    dod_result.json) + the first set-v2 campaign from ONE
    invocation.
  - R7+: campaign iterations until 10/10 from one invocation; then
    the integration gate per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR (the
    CYCLE_SAFETY_CAP / default raise — unchanged, human-applied).

  ## Findings
  - R-0178/R-0179/R-0180/R-0182/R-0183/R-0185: fixed and
    reviewer-verified (history). Done: R-0178 · Done: R-0179 ·
    Done: R-0180 · Done: R-0182 · Done: R-0183 · Done: R-0185
  - R-0181 (process, Medium): oversize ruling; exemption SPENT.
    Resolved.
  - R-0184 (product, High): loop dispatched but never executed.
    Fixed via R-0186 (ce80e034), live-proven in the R5 re-proof: a
    job runs to completed, the six-dispatch loop is refused with an
    instructive message. Done: R-0184
  - R-0186 (product, High): execution wiring. Built ce80e034,
    reviewer-verified (diff + 268-test gate + live ledger evidence);
    reuses run_cycles/limits_from_config — the F046 cap applied
    as everywhere else. Done: R-0186
  - R-0187 (product, High) 2026-08-04, R5 blocker 1:
    CYCLE_SAFETY_CAP=1 makes any job needing >1 cycle end
    max_cycles_reached forever (no resume verb), so the gate cannot
    pass — while the cap's own docstring defers raising it to F075
    and the feature's Goal defers the DEFAULT flip to the
    post-10/10 human ADR. Circular unless the CAMPAIGN and the
    DEFAULT are separated. Fix (DECISION below): an explicit,
    loudly-named experiment override in long_run_executor usable
    only by a caller that passes it deliberately (the gauntlet
    runner); flag/config clamping UNCHANGED (F046's shipped safety
    intact); order-set v2 gives every order a max_cycles budget;
    the run's evidence records the override used; the post-10/10
    ADR still raises the cap/default itself.
  - R-0188 (product, High) 2026-08-04, R5 blocker 2: no production
    DoD path exists — store_dod has ZERO callers and run_job_gate's
    only caller is the fixture-demo run_job_fulfill, so
    dod_blocking_green is unmeetable by ANY run. The R5 order's
    "use the existing job-execution path" assumed a path that is
    demo-only — a reviewer spec error, corrected here (§4.7). Fix
    (DECISION below): store_dod at dispatch from the milestone's
    compiled DoD (F069 dod_ref); run_job_gate invoked at PRODUCTION
    job completion inside the execution wiring; verdict persisted
    where load_gate_result reads it; no demo reuse, no second gate
    mechanism.
  - Observation (deferred, closure candidate): the move schema has
    no resume kind — a paused job's only forward path is
    re-dispatch, and a max_cycles_reached job cannot be continued.
    Roadmap F045/F106 territory; recorded at closure in
    .agent/candidates.md, not fixed in F075.
  - Next free ID: R-0189.

  ## Verdicts
  - R1: PASS. R2: PASS. R3: PASS. R4: PASS. Full texts in this
    file's git history (55f706db, c95f23db, e5ca780e, 6a002f09).
  - R5: PASS (SPLIT, LARGE, 2026-08-04). Range 49202f47..32e5e419
    (4 commits, all tabled). Transport: r5-1/2/3 cmp 0 against the
    reviewer's scratchpad originals; live_review at the apply
    commit byte-equals the authored text. Reviewer re-ran every
    gate: P2 268 (injection/runner suites UNEDITED — g08 still
    fires at dispatch), remaining harness+classifier 305, canary 42
    — all exit 0, porcelain empty; zero assertions removed in
    test_mission_e2e.py (verified in the diff). R-0186 verified in
    the real diff AND in the live re-proof ledger: job 0db084c6
    executed to completed/all_green, the re-dispatch guard refused
    with an instructive message — attempt 1's six-dispatch loop is
    gone. The 3.3 STOP is COMPLIANT and TRUE: both blockers
    re-verified in source by the reviewer (the hard clamp
    min(requested, CYCLE_SAFETY_CAP=1) with flag AND config capped;
    store_dod caller count zero; run_job_gate's sole caller the
    fixture-demo fulfillment). The provider-hang incident was
    honestly reported and correctly fixed at the seam contract (29
    injection sites; the gate now runs in ~1.6s provider-free,
    R-0182 upheld). The paused-not-guarded deviation is accepted
    with its deadlock rationale and recorded as the resume-verb
    observation. DECISIONS 2026-08-04 (§4.7), reversal = any later
    relay: (D1/R-0187) the campaign runs multi-cycle via an
    explicit experiment override + order-set v2 per-order
    max_cycles — alternatives rejected: passing at cap=1 is
    impossible (wedged jobs), raising the cap now is the ADR's job
    after 10/10; the set-v2 count reset loses nothing (zero passing
    attempts). (D2/R-0188) the gate verdict is produced at
    production job completion inside the execution wiring —
    alternatives rejected: the demo path grades a demo (R2 rule),
    gate-from-the-loop duplicates the job path's authority.
    Worktree hygiene: primary only, porcelain empty.
    LAST_REVIEWED_SHA = 32e5e419.
  --- END f075-r6-1 ---

  --- BEGIN f075-r6-2 sha256=7d88016fd4f13f4b8c4f7ff0be0f504dca263fefa6b1d9398a0710f980552221 ---
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
  R6 (SPLIT, LARGE): persist R5 PASS + R-0187 — an explicit,
  loudly-named experiment override in long_run_executor (flag and
  config clamping UNCHANGED; only a deliberate caller passes it),
  order-set v2 with a required max_cycles budget per order (count
  resets; nothing lost), the runner passes it through and the run's
  evidence records it — + R-0188 — store_dod at dispatch from the
  milestone's compiled DoD, run_job_gate at PRODUCTION job
  completion inside the execution wiring, verdict persisted where
  load_gate_result reads — + re-proof (--only 1 must reach achieved
  WITH dod_result.json, hard STOP otherwise) + the first set-v2
  campaign (full ten, ONE invocation, matrix to
  .agent/gauntlet/attempt-02/, sliced commits).

  ## Next Steps
  - R7+: campaign iterations until 10/10 from one invocation; then
    the integration gate.
  - Closure per STATUS_closure_protocol.md incl. the
    CYCLE_SAFETY_CAP config diff + ADR and the closure candidates
    (F070 review gap; absent resume verb).

  ## Risks
  - The override must not weaken F046's shipped safety: config and
    flag stay clamped to 1 — tests pin BOTH directions.
  - Gate at completion must have one author: run_job_gate, verdict
    persisted once, read via load_gate_result — no second store.
  - Real runs spend real tokens; provider flakiness fails a run
    honestly (A9).
  - Do-not-touch: config defaults by machine (the override is
    per-invocation evidence-recorded, not a default), the pass
    definition; the oversize exemption stays spent (R-0181).
  --- END f075-r6-2 ---

  --- BEGIN f075-r6-3 sha256=f3855e510c5b4b6a4a3953f53092675c935729d21f05fd25190b942f8eddf6b7 ---
  # Context — F075 MILESTONE GATE: 10 flawless self-runs

  ## Active Branch
  feature/f075-self-run-gauntlet (from main after the Open PR Gate
  merged PR #178, the F071 closure)

  ## Scope
  Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
  harness + evaluator + matrix + frozen order set (v2 this round) +
  live runner + injection driver + their tests. Reviewed product
  changes: run_mission exception boundary (R3), failure_postmortem
  transport classes (R4), R-0186 execution wiring (R5), R-0187
  cycles experiment vehicle + R-0188 production DoD path (R6,
  DECISIONS in the R5 verdict).

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
    .agent/authored/f075-r6-<n>.md after sha256 verification.
  - No pytest test may take a production/provider path (R-0182).
  - F046 safety: config and flag stay clamped to CYCLE_SAFETY_CAP;
    only the explicit experiment override exceeds it, recorded in
    the run's evidence.
  - Gauntlet runs use an ISOLATED data root; campaign evidence
    lives outside the repo during runs (R-0176); only matrix.md +
    matrix.json are committed under .agent/gauntlet/.
  - Do-not-touch: config defaults by machine, order-set edits
    mid-campaign (v2 is a versioned re-issue, count reset per A9);
    the pass definition freezes at campaign time.

  ## Steps
  R1-R5 done (PASS x5) → R6 R-0187 + R-0188 + re-proof + set-v2
  campaign (current) → R7+ iterations → integration gate → closure.
  --- END f075-r6-3 ---
