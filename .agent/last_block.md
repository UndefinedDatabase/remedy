OUTCOME: in progress — F075 R8 (SPLIT, LARGE) started.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R8 (SPLIT, LARGE): persist the R7 PASS +
  R-0191 (the released-gate dispatch guard) + re-proof + the set-v3
  campaign. Save THIS ENTIRE block verbatim to .agent/last_block.md
  first (update OUTCOME at handback). You are on
  feature/f075-self-run-gauntlet at 854a9860. STOP rule: every phase
  ends with a verification; first red TEST gate -> STOP per AGENTS.md
  If-Blocked. Phase 3 has its own hard STOP. Commits < 500 lines, NO
  oversize left (R-0181).

  PHASE 1 — PERSIST THE R7 VERDICT (first commit)
   1. Save the three AUTHORED TEXT payloads below to
      .agent/authored/f075-r8-<n>.md (bytes between BEGIN/END markers,
      exclusive, incl. final newline; payload lines at column 0).
      Verify each sha256sum against its BEGIN-marker hash. Mismatch ->
      STOP, report raw sums, apply nothing.
   2. Apply f075-r8-1 -> .agent/live_review.md, f075-r8-2 ->
      .agent/plan.md, f075-r8-3 -> .agent/context.md — FULL
      replacements, byte-exact from the saved files.
   3. Commit 1: chore(f075): persist the R7 PASS, register R-0191.
      Gate: python3 -m pytest tests/cli/test_golden_path.py -q ->
      exit 0. Push.

  PHASE 2 — R-0191: THE RELEASED-GATE DISPATCH GUARD (own commit)
   1. evaluate_dispatch: refuse a dispatch_job for a milestone whose
      LATEST linked job completed with a RELEASED gate verdict — read
      the REAL verdict via load_gate_result, never re-derive it. The
      refusal detail tells the model the only correct move:
      declare_milestone_done (the existing first-refusal re-prompt
      carries it; the second-refusal escalation already exists). A
      milestone whose latest job has no verdict or a blocked one is
      untouched by this guard (R-0186/R-0190 own those cases).
   2. Tests (fakes, R-0182): released latest job -> dispatch refused
      with declare_milestone_done in the detail -> a fake model that
      follows the instruction achieves the mission end-to-end;
      blocked latest job -> this guard silent (R-0190 path);
      in-flight -> R-0186 path unchanged; a NEWER non-released job
      supersedes an older released one (LATEST rules); ledger shows
      refusal then declaration. Existing suites green unedited —
      list any exception per name with reason.
   3. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_orchestrator_loop.py
      tests/orchestration/test_mission_e2e.py
      tests/orchestration/test_era_integrity.py
      tests/orchestration/test_gauntlet_injection.py
      tests/orchestration/test_gauntlet_runner.py -q -> exit 0. Push.

  PHASE 3 — RE-PROOF (one order, hard-gated)
   1. python3 scripts/self_run_gauntlet.py --live <fresh root OUTSIDE
      the repo> --only 1 --format json
   2. REQUIRED: terminal `achieved` AND dod_result.json with
      released: true. Quote the terminal, the verdict fields, the
      cycles record, the template digest and the declare move's
      ledger entry in the handoff.
   3. Either missing -> STOP: commit nothing further, record the
      full evidence trail in .agent/decisions.md, hand back (the
      R4-R7 STOP precedent).

  PHASE 4 — CAMPAIGN, SET v3 (only after a green Phase 3)
   1. Preconditions in the handoff: porcelain empty, pushed,
      provider reachable, set_hash (v3) re-verified,
      preflight_injections -> [].
   2. ONE invocation, full ten: --live <fresh root OUTSIDE the repo>
      --format both. No rerun inside the attempt, no order or
      template edits; provider flakiness fails a run honestly (A9).
   3. Copy matrix.md + matrix.json into .agent/gauntlet/attempt-02/
      and commit, sliced under the cap; the handoff states set
      version 3 and the count reset. Evidence-root path + per-run
      terminals in the handoff.
   4. Gate: committed matrix.json parses, runs_recorded == 10;
      canary python3 -m pytest tests/cli/test_golden_path.py -q ->
      exit 0. The flawless count is REPORTED, not gated.

  PHASE 5 — HANDBACK
   git status --porcelain empty. Rewrite .agent/handoff.md per
   docs/agents/handback_template.md (per-commit tables; raw gate
   outputs; the Phase 3 proof quoted; if Phase 4 ran, its summary
   table verbatim; sha256 proof per applied reviewer text). Update
   last_block OUTCOME. Completion report ends:
   "F075 R8 complete — awaiting review." (append "set-v3 campaign
   matrix recorded" if Phase 4 ran).

  --- BEGIN f075-r8-1 sha256=bc4c813c811e2c4c717bbdcc0a11016e92e2123f745a1c4dea3953843657ba3f ---
  # Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

  Branch: feature/f075-self-run-gauntlet
  Scope: a gauntlet HARNESS — evaluator + matrix + a frozen order set
  (v3: orders + sample-project template) — that earns autonomy with
  data. Flawless per run = start command only + terminal green +
  blocking DoD green + zero unknown postmortems + zero open
  decisions + host data root byte-untouched. Product changes ride
  along ONLY as reviewed SPLIT work: exception boundary (R3),
  transport classes (R4), execution wiring (R5), cycles vehicle +
  production DoD path (R6), sample-project world + blocked-gate
  escalation (R7), the released-gate dispatch guard (R8).

  ## Steps
  - R1-R6 (SPLIT, LARGE): harness + set + boundary + injections +
    attempt 1 + execution + cycles vehicle + DoD path — PASS x6
    (history).
  - R7 (SPLIT, LARGE): R-0189 (template world, manifest v3) +
    R-0190 (blocked-streak escalation) built; the gate RELEASED for
    the first time; compliant 4.3 STOP on the missing
    released-gate dispatch guard — PASS, see Verdicts.
  - R8 (SPLIT, LARGE, current): persist R7 verdict + R-0191 (refuse
    a dispatch for a milestone whose latest job completed with a
    released gate; the refusal instructs declare_milestone_done) +
    re-proof (--only 1 must reach achieved WITH a released verdict)
    + the set-v3 campaign from ONE invocation.
  - R9+: campaign iterations until 10/10 from one invocation; then
    the integration gate per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR (the
    CYCLE_SAFETY_CAP / default raise — human-applied).

  ## Findings
  - R-0178..R-0188: all fixed and reviewer-verified; R-0181
    resolved by ruling (exemption SPENT). Done: R-0178 ·
    Done: R-0179 · Done: R-0180 · Done: R-0182 · Done: R-0183 ·
    Done: R-0184 · Done: R-0185 · Done: R-0186 · Done: R-0187 ·
    Done: R-0188 · R-0181 Resolved.
  - R-0189 (product, High): the missions' world. Built 2eb5ab46 +
    0cc11d4d + 7404fdf9 — sample project (7 modules, 30-test green
    suite, README/CHANGELOG), per-run materialised copy (git init +
    baseline), manifest v3 folds the template tree digest into the
    set hash, tamper refused, run.json records the digest; all ten
    goals audited meaningful, no order edited. Reviewer re-ran the
    scratch-copy proof personally: 30 passed from a fresh
    materialisation. The R6 blocker check (acc-001) now PASSES and
    the gate produced this feature's first RELEASED verdict.
    Done: R-0189
  - R-0190 (product, Medium): blocked-streak escalation. Built
    e19af5e6 — per-milestone consecutive-blocked counter, second
    block escalates via the existing F051 hand_over, reset on
    release or other milestone; 9 tests; correctly did NOT fire in
    the R7 re-proof (nothing was blocked). Done: R-0190
  - R-0191 (product, High) 2026-08-04, R7 re-proof: six dispatches
    of M001, every one completed with a RELEASED gate, and the
    model never chose declare_milestone_done — the guard triad has
    a hole: in-flight -> refuse+wait (R-0186), blocked x2 ->
    escalate (R-0190), but completed+released -> nothing. Fix
    (DECISION below): evaluate_dispatch refuses a dispatch_job for
    a milestone whose LATEST job completed with a released gate;
    the refusal detail says the only correct move is
    declare_milestone_done — the loop's existing first-refusal
    re-prompt then carries that instruction to the model.
  - Deferred closure candidates: F070 review gap; absent resume
    verb.
  - Next free ID: R-0192.

  ## Verdicts
  - R1-R6: PASS x6. Full texts in this file's git history
    (55f706db, c95f23db, e5ca780e, 6a002f09, 9e8ced5b, df856730).
  - R7: PASS (SPLIT, LARGE, 2026-08-04). Range 73c19023..854a9860
    (7 commits, all tabled). Transport: r7-1/2/3 cmp 0 against the
    reviewer's scratchpad originals; live_review at the apply
    commit byte-equals the authored text. Reviewer re-ran every
    gate: orders/runner 81, loop/e2e/era/injection 259 (all four
    suites UNEDITED), remaining seven files 376, canary 42 — all
    exit 0, porcelain empty — and personally materialised a fresh
    copy and ran its suite: 30 passed, self-sufficient, template
    digest matching the v3 manifest. The goal-vs-template audit
    spot-checked (g01's BACKOFF_CAP_SECONDS exists at retry.py:8).
    The 4.3 STOP is COMPLIANT and TRUE: the re-proof's
    dod_result.json is RELEASED with acc-001 passed — the R6
    blocker demonstrably closed — and the miss is the model never
    claiming the milestone, with the guard hole precisely
    identified. Version-literal test renames accepted as declared.
    DECISION 2026-08-04 (§4.7), reversal = any later relay:
    (R-0191) the released-gate dispatch guard with an instructive
    refusal — alternatives rejected: the loop auto-declaring the
    milestone (the declare move carries the model's accountability;
    the loop must not claim on its behalf), prompt-engineering
    alone (a guard is falsifiable, a hint is a hope). Worktree
    hygiene: primary only, porcelain empty.
    LAST_REVIEWED_SHA = 854a9860.
  --- END f075-r8-1 ---

  --- BEGIN f075-r8-2 sha256=c28791b09ad4e8a001b5c29db0f17c8b582d15e4a2a6d82976252ab31051a525 ---
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
  R8 (SPLIT, LARGE): persist R7 PASS + R-0191 — evaluate_dispatch
  refuses a dispatch_job for a milestone whose LATEST job completed
  with a RELEASED gate, refusal detail instructing
  declare_milestone_done (completing the guard triad: in-flight ->
  wait, blocked x2 -> escalate, released -> declare) — + re-proof
  (--only 1 must reach achieved WITH a released verdict, hard STOP
  otherwise) + the set-v3 campaign (full ten, ONE invocation,
  matrix to .agent/gauntlet/attempt-02/, sliced commits).

  ## Next Steps
  - R9+: campaign iterations until 10/10 from one invocation; then
    the integration gate.
  - Closure per STATUS_closure_protocol.md incl. the
    CYCLE_SAFETY_CAP config diff + ADR and the closure candidates.

  ## Risks
  - The guard must read the REAL gate verdict (load_gate_result),
    not re-derive it; released-but-stale edge (a later job for the
    same milestone) resolves by LATEST job.
  - Real runs spend real tokens; provider flakiness fails a run
    honestly (A9).
  - Do-not-touch: config defaults by machine, the pass definition,
    order/template edits mid-campaign; the oversize exemption stays
    spent (R-0181).
  --- END f075-r8-2 ---

  --- BEGIN f075-r8-3 sha256=e97aae1657ab7e3c762a30b66f2357ef7d939f72bbbdb5e68dfa9ad15e6c2f80 ---
  # Context — F075 MILESTONE GATE: 10 flawless self-runs

  ## Active Branch
  feature/f075-self-run-gauntlet (from main after the Open PR Gate
  merged PR #178, the F071 closure)

  ## Scope
  Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
  harness + evaluator + matrix + frozen order set v3 (orders +
  sample-project template) + live runner + injection driver + their
  tests. Reviewed product changes: exception boundary (R3),
  transport classes (R4), execution wiring (R5), cycles vehicle +
  production DoD path (R6), sample-project world + blocked-gate
  escalation (R7), the R-0191 released-gate dispatch guard (R8,
  DECISION in the R7 verdict).

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
    .agent/authored/f075-r8-<n>.md after sha256 verification.
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
    mid-campaign; the pass definition freezes at campaign time.

  ## Steps
  R1-R7 done (PASS x7) → R8 R-0191 + re-proof + set-v3 campaign
  (current) → R9+ iterations → integration gate → closure.
  --- END f075-r8-3 ---
