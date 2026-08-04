OUTCOME: done — F075 R10 complete. R9 PASS persisted; R-0193 and R-0194 built; re-proof achieved+released with a DIRECT declare; set-v4 campaign attempt 02 = 3/10 (first flawless runs), two findings reported for Window 1.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R10 (SPLIT, LARGE): persist the R9 PASS +
  R-0193 (the released-gate context directive) + R-0194 (order-set v4,
  budgets only) + re-proof + the set-v4 campaign. Save THIS ENTIRE block
  verbatim to .agent/last_block.md first (update OUTCOME at handback).
  You are on feature/f075-self-run-gauntlet at ae4c6e9a. STOP rule:
  every phase ends with a verification; first red TEST gate -> STOP per
  AGENTS.md If-Blocked. Phase 4 has its own hard STOP. Commits < 500
  lines, NO oversize left (R-0181).

  PHASE 1 — PERSIST THE R9 VERDICT (first commit)
   1. Save the three AUTHORED TEXT payloads below to
      .agent/authored/f075-r10-<n>.md (bytes between BEGIN/END
      markers, exclusive, incl. final newline; payload lines at
      column 0). Verify each sha256sum against its BEGIN-marker hash.
      Mismatch -> STOP, report raw sums, apply nothing.
   2. Apply f075-r10-1 -> .agent/live_review.md, f075-r10-2 ->
      .agent/plan.md, f075-r10-3 -> .agent/context.md — FULL
      replacements, byte-exact from the saved files.
   3. Commit 1: chore(f075): persist the R9 PASS, register
      R-0193/R-0194. Gate: python3 -m pytest
      tests/cli/test_golden_path.py -q -> exit 0. Push.

  PHASE 2 — R-0193: THE RELEASED-GATE CONTEXT DIRECTIVE (own commit)
   1. assemble_context (or the milestone-evidence section it renders):
      when a milestone's latest job COMPLETED with a RELEASED gate
      verdict — the same collect_milestone_evidence facts the R-0191
      guard reads — the context carries an explicit directive line
      naming the milestone and the move: the correct next move is
      declare_milestone_done for <id>. State a proven fact only
      (released is True); no directive for None/blocked/in-flight.
      The R-0191 refusal stays untouched as the net.
   2. Tests (fakes, R-0182): the context bytes carry the directive
      exactly when the evidence says released, and never otherwise;
      a fake model that follows the context achieves in ~2
      iterations per milestone; the refusal still fires on a
      dispatch attempt against a released milestone. Existing suites
      green unedited — list any exception per name with reason.
   3. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_orchestrator_loop.py
      tests/orchestration/test_mission_e2e.py
      tests/orchestration/test_era_integrity.py -q -> exit 0. Push.

  PHASE 3 — R-0194: ORDER-SET v4, BUDGETS ONLY (own commit)
   1. Re-issue the ten orders changing ONLY budget values:
      max_iterations sized from the observed economics (the compiler
      shapes plans of ~3 milestones from a one-milestone goal; a
      milestone costs ~2 iterations on the direct path, 3 with the
      net; add margin, document the sizing rationale per order in
      the file's rationale or a budget_rationale field); re-check
      max_tokens/max_wall_seconds/max_cycles for the same shapes.
      Goals, kinds, rationales, risks, injections, milestones,
      template: byte-UNCHANGED.
   2. Manifest: gauntlet_order_set_version 4, fresh digests + set
      hash (template digest unchanged). Count resets per A9. Order
      tests hold against v4 (version literals via the constant —
      the R7 lesson).
   3. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_gauntlet_orders.py
      tests/orchestration/test_gauntlet_runner.py -q -> exit 0. Push.

  PHASE 4 — RE-PROOF (one order, hard-gated)
   1. python3 scripts/self_run_gauntlet.py --live <fresh root OUTSIDE
      the repo> --only 1 --format json
   2. REQUIRED: terminal `achieved` AND dod_result.json released:
      true AND zero open decisions. Quote the terminal, the verdict
      fields, the iteration count and the full criteria table in the
      handoff — plus whether the declare was DIRECT (no refusal
      needed) as the R-0193 evidence.
   3. Anything missing -> STOP: commit nothing further, record the
      full evidence trail in .agent/decisions.md, hand back (the
      R4-R9 STOP precedent).

  PHASE 5 — CAMPAIGN, SET v4 (only after a green Phase 4)
   1. Preconditions in the handoff: porcelain empty, pushed,
      provider reachable, set_hash (v4) re-verified,
      preflight_injections -> [].
   2. ONE invocation, full ten: --live <fresh root OUTSIDE the repo>
      --format both. No rerun inside the attempt, no order or
      template edits; provider flakiness fails a run honestly (A9).
   3. Copy matrix.md + matrix.json into .agent/gauntlet/attempt-02/
      and commit, sliced under the cap; the handoff states set
      version 4 and the count reset. Evidence-root path + per-run
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
   "F075 R10 complete — awaiting review." (append "set-v4 campaign
   matrix recorded" if Phase 5 ran).

  --- BEGIN f075-r10-1 sha256=b3e2c7dc2af59c6f5fb0094b9d9e7cd379e046fd28a3d97ebc97b7b557552bf7 ---
  # Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

  Branch: feature/f075-self-run-gauntlet
  Scope: a gauntlet HARNESS — evaluator + matrix + a frozen order set
  (v4 this round: orders + sample-project template) — that earns
  autonomy with data. Flawless per run = start command only +
  terminal green + blocking DoD green + zero unknown postmortems +
  zero open decisions + host data root byte-untouched. Product
  changes ride along ONLY as reviewed SPLIT work: exception boundary
  (R3), transport classes (R4), execution wiring (R5), cycles
  vehicle + production DoD path (R6), sample-project world +
  blocked-gate escalation (R7), released-gate dispatch guard (R8),
  attribution fix (R9), the released-gate context directive (R10).

  ## Steps
  - R1-R8 (SPLIT, LARGE): harness + set + boundary + injections +
    attempt 1 + execution + cycles vehicle + DoD path + template
    world + escalation + released-gate guard — PASS x8 (history).
  - R9 (SPLIT, LARGE): R-0192 built; the chain CLOSES per milestone
    (dispatch -> execute -> release -> declare, twice in one run);
    compliant 3.3 STOP on iteration economics — PASS, see Verdicts.
  - R10 (SPLIT, LARGE, current): persist R9 verdict + R-0193 (the
    assembled context carries the released-gate directive so
    declare is the DIRECT path) + R-0194 (order-set v4: budgets
    re-issued from observed economics; count resets) + re-proof
    (--only 1 must reach achieved WITH a released verdict and zero
    open decisions) + the set-v4 campaign from ONE invocation.
  - R11+: campaign iterations until 10/10 from one invocation; then
    the integration gate per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR (the
    CYCLE_SAFETY_CAP / default raise — human-applied).

  ## Findings
  - R-0178..R-0191: all fixed and reviewer-verified; R-0181
    resolved by ruling (exemption SPENT). Done: R-0178 ·
    Done: R-0179 · Done: R-0180 · Done: R-0182 · Done: R-0183 ·
    Done: R-0184 · Done: R-0185 · Done: R-0186 · Done: R-0187 ·
    Done: R-0188 · Done: R-0189 · Done: R-0190 · Done: R-0191 ·
    R-0181 Resolved.
  - R-0192 (product, Medium): refused dispatch erased the
    attribution. Fixed e213733b — exactly one condition (no job_id
    -> skip, never overwrite), five tests incl. the R8 sequence
    replayed to achieved with the real dispatched_job_for
    load-bearing; live-proven in the R9 re-proof (declare succeeds,
    twice). Reviewer-verified. Done: R-0192
  - R-0193 (product, Medium) 2026-08-04, R9 re-proof: each
    milestone costs three iterations (dispatch, the R-0191 refusal,
    declare) because the model only learns "this milestone is
    finished" from the refusal. Fix (DECISION below): the assembled
    context carries an explicit directive when a milestone's latest
    job completed with a RELEASED gate ("the correct next move is
    declare_milestone_done for M00X"), making declare the DIRECT
    path (~2 iterations per milestone); the R-0191 refusal stays as
    the safety net. Test: the context bytes carry the directive
    exactly when the evidence says released; the refusal still
    fires on a dispatch attempt.
  - R-0194 (campaign, Medium) 2026-08-04, R9 re-proof: g01's budget
    (6 iterations, set in R1 before anything ever executed) cannot
    fit the compiler's real plan shape (three milestones from a
    one-milestone goal). Fix (DECISION below): order-set v4
    re-issues BUDGETS ONLY from observed economics — max_iterations
    sized per order for the compiler's real shapes with margin
    (rationale per order), tokens/wall re-checked; goals, kinds,
    rationales, injections UNCHANGED; template unchanged; count
    resets per A9 (nothing lost, zero passing attempts).
  - Deferred closure candidates: F070 review gap; absent resume
    verb.
  - Next free ID: R-0195.

  ## Verdicts
  - R1-R8: PASS x8. Full texts in this file's git history
    (55f706db, c95f23db, e5ca780e, 6a002f09, 9e8ced5b, df856730,
    1fe38c56, 5d068078).
  - R9: PASS (SPLIT, LARGE, 2026-08-04). Range 09348505..ae4c6e9a
    (4 commits, all tabled). Transport: r9-1/2/3 cmp 0 against the
    reviewer's scratchpad originals; live_review at the apply
    commit byte-equals the authored text. Reviewer re-ran every
    gate: loop/e2e/era 237 (e2e and era UNEDITED), seven harness
    files 261, canary 42 — all exit 0, porcelain empty. R-0192
    verified in the diff (exactly one condition, nothing rode
    along) and live: the R8-blocked declare now lands, two
    milestones completed in one run, open_decisions 0, gate
    released. The 3.3 STOP is COMPLIANT and TRUE: iteration_limit
    with M003 never started — a budget-versus-plan-shape mismatch
    precisely accounted (3 iterations x 3 compiler milestones + 1
    > budget 6). DECISIONS 2026-08-04 (§4.7), reversal = any later
    relay: (D1/R-0193) the released-gate fact becomes an explicit
    context directive — alternative rejected: not counting refused
    iterations against the budget (weakens iteration_limit's
    safety meaning; refusal spin is already bounded by the
    second-refusal escalation, and a budget that ignores real
    behavior is a budget that lies). (D2/R-0194) v4 re-issues
    budgets only, from evidence — alternative rejected: keeping
    R1's guessed budgets (the campaign would measure a guess, not
    the product). Worktree hygiene: primary only, porcelain empty.
    LAST_REVIEWED_SHA = ae4c6e9a.
  --- END f075-r10-1 ---

  --- BEGIN f075-r10-2 sha256=9fe177188ea74187b482befe0f9af4dc3d768300882feaaf8a893c71300c99a8 ---
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
  R10 (SPLIT, LARGE): persist R9 PASS + R-0193 — the assembled
  context carries an explicit directive when a milestone's latest
  job completed with a released gate, so declare_milestone_done is
  the DIRECT path and the R-0191 refusal is only the net — +
  R-0194 — order-set v4, budgets ONLY, sized from the observed
  economics (goals/kinds/rationales/injections/template unchanged;
  count resets per A9) — + re-proof (--only 1 must reach achieved
  WITH a released verdict and zero open decisions, hard STOP
  otherwise) + the set-v4 campaign (full ten, ONE invocation,
  matrix to .agent/gauntlet/attempt-02/, sliced commits).

  ## Next Steps
  - R11+: campaign iterations until 10/10 from one invocation; then
    the integration gate.
  - Closure per STATUS_closure_protocol.md incl. the
    CYCLE_SAFETY_CAP config diff + ADR and the closure candidates.

  ## Risks
  - The directive must state a fact the evidence proves (released),
    never a hope; the refusal net stays for the model that ignores
    it.
  - Budgets sized with margin but not slack — the gate still
    measures economy; document the sizing rationale per order.
  - Real runs spend real tokens; provider flakiness fails a run
    honestly (A9).
  - Do-not-touch: config defaults by machine, the pass definition;
    the oversize exemption stays spent (R-0181).
  --- END f075-r10-2 ---

  --- BEGIN f075-r10-3 sha256=13d724a16045475d4372b5586bd3bdf73641313ff6f60f6d102926a709d7e48f ---
  # Context — F075 MILESTONE GATE: 10 flawless self-runs

  ## Active Branch
  feature/f075-self-run-gauntlet (from main after the Open PR Gate
  merged PR #178, the F071 closure)

  ## Scope
  Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
  harness + evaluator + matrix + frozen order set v4 (orders +
  sample-project template) + live runner + injection driver + their
  tests. Reviewed product changes: exception boundary (R3),
  transport classes (R4), execution wiring (R5), cycles vehicle +
  production DoD path (R6), sample-project world + blocked-gate
  escalation (R7), released-gate dispatch guard (R8), attribution
  fix (R9), the R-0193 released-gate context directive (R10,
  DECISIONS in the R9 verdict).

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
    .agent/authored/f075-r10-<n>.md after sha256 verification.
  - No pytest test may take a production/provider path (R-0182).
  - F046 safety: config and flag stay clamped to CYCLE_SAFETY_CAP;
    only the explicit experiment override exceeds it, recorded in
    the run's evidence.
  - Gauntlet runs use an ISOLATED data root AND an isolated
    materialised workspace copy; the operator's tree is never a job
    workspace; campaign evidence lives outside the repo during runs
    (R-0176); only matrix.md + matrix.json are committed under
    .agent/gauntlet/.
  - Do-not-touch: config defaults by machine, order/template edits
    mid-campaign (v4 is a versioned budgets-only re-issue, count
    reset per A9); the pass definition freezes at campaign time.

  ## Steps
  R1-R9 done (PASS x9) → R10 R-0193 + R-0194 + re-proof + set-v4
  campaign (current) → R11+ iterations → integration gate → closure.
  --- END f075-r10-3 ---
