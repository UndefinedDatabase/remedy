OUTCOME: executed with a STOP — F075 R7: R6 PASS persisted; R-0189 BUILT (frozen sample-project template, all ten goals audited meaningful with no order edited, materialised as a git-committed COPY per run, manifest v3 folding the template digest into set hash c267ccab..., tamper refused) and R-0190 BUILT (escalate after two consecutive gate-blocked completions of one milestone, via the existing F051 hand_over). Phase 4 re-proof: the DoD gate RELEASED for the first time in this feature's history (acc-001 pytest passed, exit 0) — but terminal iteration_limit, because the model never chose declare_milestone_done -> rule 4.3 STOP; campaign NOT run. Next gap recorded: no guard refuses a dispatch for a milestone whose latest job completed with a released gate.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R7 (SPLIT, LARGE): persist the R6 PASS +
  R-0189 (the sample-project world) + R-0190 (blocked-gate escalation) +
  re-proof + the set-v3 campaign. Save THIS ENTIRE block verbatim to
  .agent/last_block.md first (update OUTCOME at handback). You are on
  feature/f075-self-run-gauntlet at 73c19023. STOP rule: every phase
  ends with a verification; first red TEST gate -> STOP per AGENTS.md
  If-Blocked. Phase 4 has its own hard STOP. Commits < 500 lines, NO
  oversize left (R-0181) — slice everything, the template lands over as
  many commits as it needs.

  PHASE 1 — PERSIST THE R6 VERDICT (first commit)
   1. Save the three AUTHORED TEXT payloads below to
      .agent/authored/f075-r7-<n>.md (bytes between BEGIN/END markers,
      exclusive, incl. final newline; payload lines at column 0).
      Verify each sha256sum against its BEGIN-marker hash. Mismatch ->
      STOP, report raw sums, apply nothing.
   2. Apply f075-r7-1 -> .agent/live_review.md, f075-r7-2 ->
      .agent/plan.md, f075-r7-3 -> .agent/context.md — FULL
      replacements, byte-exact from the saved files.
   3. Commit 1: chore(f075): persist the R6 PASS, register
      R-0189/R-0190. Gate: python3 -m pytest
      tests/cli/test_golden_path.py -q -> exit 0. Push.

  PHASE 2 — R-0189: THE SAMPLE-PROJECT WORLD (own commits)
   Record every design decision in .agent/decisions.md.
   1. The template: a small, real, self-contained Python project
      under scripts/gauntlet_sample_project/ — source package, a
      GREEN test suite (fast, no network, no provider), README,
      CHANGELOG, and the concrete artifacts the ten goals name.
      AUDIT every order's goal against it and record the mapping in
      .agent/decisions.md: a goal about a hardcoded retry backoff
      cap needs that cap to exist in the code; upgrade notes need a
      release history to describe; the two-milestone missions need
      enough surface for two real milestones. A goal that cannot be
      made meaningful is reported in the handoff — do NOT edit
      orders silently.
   2. Materialisation per run (gauntlet_runner): copy the template
      into the run's own isolated area (e.g. <run_dir>/workspace),
      git init + one baseline commit inside the COPY, and create
      the project with its repository pointing THERE (inspect the
      real project fields: repo_paths / canonical_repo_path). Jobs
      and DoD checks then run against that checkout. The operator's
      tree is NEVER a workspace; the host-root hash criterion
      already polices the data root — extend the run evidence with
      the template digest used (see 3).
   3. Freeze: manifest v3 — gauntlet_order_set_version 3, the
      existing per-order sha256s, PLUS a template tree digest
      (stable: sorted relative paths + content hashes) folded into
      the set hash. gauntlet_orders verifies it at load like
      everything else (tamper on any template file -> OrderSetError)
      and run.json records the digest. Campaign count resets per
      A9; nothing is lost. Update the order tests: freeze/tamper
      pins hold against v3, template tampering refused, template
      suite green as its own fixture check.
   4. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_gauntlet_orders.py
      tests/orchestration/test_gauntlet_runner.py -q -> exit 0, AND
      the template's own suite green run FROM a scratch
      materialised copy (prove the copy is self-sufficient; state
      the exact command). Push.

  PHASE 3 — R-0190: ESCALATE THE SECOND BLOCKED COMPLETION (own commit)
   1. orchestrator_loop: track consecutive gate-blocked completions
      per milestone; on the SECOND in a row for the same milestone,
      escalate via the existing hand_over path (the second-refusal
      precedent) with a detail naming the milestone, both attempts'
      blockers, and the budget saved. A released gate or a
      different milestone resets the counter. First block stays a
      visible retry opportunity (context already shows the
      blocker).
   2. Tests (fakes, R-0182): blocked-blocked -> escalated terminal
      with both blockers in the detail; blocked-released ->
      proceeds; blocked on M1 then blocked on M2 -> no escalation;
      the escalation lands in the ledger and the escalation log
      (F051). Existing suites green unedited — list any exception
      per name with reason.
   3. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_orchestrator_loop.py
      tests/orchestration/test_mission_e2e.py
      tests/orchestration/test_era_integrity.py
      tests/orchestration/test_gauntlet_injection.py -q -> exit 0.
      Push.

  PHASE 4 — RE-PROOF (one order, hard-gated)
   1. python3 scripts/self_run_gauntlet.py --live <fresh root OUTSIDE
      the repo> --only 1 --format json
   2. REQUIRED: terminal `achieved` AND dod_result.json with
      released: true. Quote the terminal, the verdict fields, the
      recorded cycles and the template digest in the handoff.
   3. Either missing -> STOP: commit nothing further, record the
      full evidence trail in .agent/decisions.md, hand back (the
      R4/R5/R6 STOP precedent).

  PHASE 5 — CAMPAIGN, SET v3 (only after a green Phase 4)
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

  PHASE 6 — HANDBACK
   git status --porcelain empty. Rewrite .agent/handoff.md per
   docs/agents/handback_template.md (per-commit tables; raw gate
   outputs; the goal-vs-template audit table; the Phase 4 proof
   quoted; if Phase 5 ran, its summary table verbatim; sha256 proof
   per applied reviewer text). Update last_block OUTCOME. Completion
   report ends: "F075 R7 complete — awaiting review." (append
   "set-v3 campaign matrix recorded" if Phase 5 ran).

  --- BEGIN f075-r7-1 sha256=35bed48dd81851f1aca4e03518fe85713a87fc5c21fa30ac41bf9932a56319bf ---
  # Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

  Branch: feature/f075-self-run-gauntlet
  Scope: a gauntlet HARNESS — evaluator + matrix + a frozen order set
  — that earns autonomy with data. Flawless per run = start command
  only + terminal green + blocking DoD green + zero unknown
  postmortems + zero open decisions + host data root byte-untouched.
  Product changes ride along ONLY as reviewed SPLIT work: run_mission
  exception boundary (R3), transport classes (R4), execution wiring
  (R5), cycles experiment vehicle + production DoD path (R6), the
  sample-project world + blocked-gate escalation (R7).

  ## Steps
  - R1-R5 (SPLIT, LARGE): harness + set + boundary + injections +
    attempt 1 + R-0184 diagnosis + R-0186 execution — PASS x5
    (history).
  - R6 (SPLIT, LARGE): R-0187 (override + set v2) + R-0188
    (store_dod at dispatch, gate at completion) built and
    live-proven; compliant 4.3 STOP on the missing mission
    repository — PASS, see Verdicts.
  - R7 (SPLIT, LARGE, current): persist R6 verdict + R-0189 (frozen
    sample-project template, materialised per run into the isolated
    workspace, manifest v3) + R-0190 (escalate after two
    consecutive gate-blocked completions) + re-proof (--only 1 must
    reach achieved WITH a released verdict) + the set-v3 campaign
    from ONE invocation.
  - R8+: campaign iterations until 10/10 from one invocation; then
    the integration gate per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR (the
    CYCLE_SAFETY_CAP / default raise — human-applied).

  ## Findings
  - R-0178..R-0186: all fixed and reviewer-verified; R-0181
    resolved by ruling (exemption SPENT). Done: R-0178 ·
    Done: R-0179 · Done: R-0180 · Done: R-0182 · Done: R-0183 ·
    Done: R-0184 · Done: R-0185 · Done: R-0186 · R-0181 Resolved.
  - R-0187 (product, High): cycles experiment vehicle. Built
    d54091e7 — experiment_max_cycles early-returns with source
    "experiment"/over_cap recorded; flag AND config clamping
    untouched, both directions pinned; order-set v2 carries
    per-order max_cycles; the runner passes it through and the
    re-proof recorded "cycles=4/experiment OVER-CAP".
    Reviewer-verified in source and tests. Done: R-0187
  - R-0188 (product, High): production DoD path. Built 072a2025 —
    store_dod at dispatch (first real caller), run_job_gate at
    production completion, ONE persisted verdict readable via
    load_gate_result; the re-proof produced a real dod_result.json
    (released false, blocking_red acc-001) where before R-0188 no
    run could produce any. Reviewer-verified. Done: R-0188
  - R-0189 (product, High) 2026-08-04, R6 blocker: the gauntlet's
    missions have NO repository — the runner creates a project with
    no repo_paths, the orders say "in the sample project", none is
    materialised, so any DoD like "the unit suite is green" can
    never release (acc-001: "file or directory not found: tests").
    Fix (DECISION below): a frozen sample-project template ships
    with the harness; the runner materialises a COPY per run into
    the run's isolated workspace (git init + baseline commit); the
    project record points THERE; manifest v3 freezes the template
    (tree digest in the set hash); run.json records the digest;
    every order's goal audited against the template so each goal is
    MEANINGFUL there (a goal about a backoff cap needs one to
    exist).
  - R-0190 (product, Medium) 2026-08-04, R6 observation: with jobs
    now completing, a gate-blocked milestone makes the model retry
    dispatch until iteration_limit — six identical failed attempts,
    the R-0184 pattern back for an honest reason. Fix (DECISION
    below): mirror the loop's own second-refusal precedent — after
    the SECOND consecutive gate-blocked completion for the SAME
    milestone, the loop escalates (F051) instead of burning the
    budget; first block stays a visible retry opportunity.
  - Deferred closure candidates: F070 review gap; absent resume
    verb (paused/max_cycles_reached).
  - Next free ID: R-0191.

  ## Verdicts
  - R1-R5: PASS x5. Full texts in this file's git history
    (55f706db, c95f23db, e5ca780e, 6a002f09, 9e8ced5b).
  - R6: PASS (SPLIT, LARGE, 2026-08-04). Range 32e5e419..73c19023
    (5 commits, all tabled). Transport: r6-1/2/3 cmp 0 against the
    reviewer's scratchpad originals; live_review at the apply
    commit byte-equals the authored text. Reviewer re-ran every
    gate: orders/runner/loop/executor 291, e2e/era/injection/dod
    135, remaining harness 271, canary 42 — all exit 0, porcelain
    empty. R-0187 verified in source: the override is an early
    return with source "experiment", the flag/config clamp is
    byte-identical to F046's, both directions pinned; set v2 loads
    with per-order max_cycles [4,4,5,3,8,4,4,5,8,3]. R-0188
    verified: store_dod's first caller, one-author verdict, and the
    re-proof's dod_result.json proves the whole chain live. The 4.3
    STOP is COMPLIANT and TRUE: the runner's project has no
    repository (verified in _default_make_project) and acc-001's
    raw reason says exactly that. Test renames/extensions accepted
    as declared (version literal -> constant+1; a now-false name).
    DECISIONS 2026-08-04 (§4.7), reversal = any later relay:
    (D1/R-0189) per-run materialised copy of a frozen template —
    alternatives rejected: pointing DoD checks at the operator's
    tree (isolation breach by design), keeping workspace-only
    missions (makes every real-project DoD a lie); freeze via
    manifest v3 because the template shapes outcomes exactly like
    the orders do; count reset costs nothing (zero passing
    attempts). (D2/R-0190) escalate on the second consecutive
    blocked completion — alternatives rejected: unlimited retries
    (burns budget, attempt-1 pattern), escalate on first block
    (denies the model its legitimate targeted-fix retry; the
    refusal precedent already chose two). Worktree hygiene: primary
    only, porcelain empty. LAST_REVIEWED_SHA = 73c19023.
  --- END f075-r7-1 ---

  --- BEGIN f075-r7-2 sha256=1382a11cf5f7159e4ed01bec7d7b831b97fa6ecbf0ce7c12289f53ee48427985 ---
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
  R7 (SPLIT, LARGE): persist R6 PASS + R-0189 — a frozen
  sample-project template under the harness, materialised as a COPY
  per run into the run's isolated workspace (git init + baseline
  commit), project record pointing there, manifest v3 freezing the
  template tree digest inside the set hash, run.json recording it,
  and every order's goal audited to be meaningful against the
  template — + R-0190 — after the second consecutive gate-blocked
  completion for one milestone the loop escalates (F051), first
  block stays a retry opportunity — + re-proof (--only 1 must reach
  achieved WITH a released verdict, hard STOP otherwise) + the
  set-v3 campaign (full ten, ONE invocation, matrix to
  .agent/gauntlet/attempt-02/, sliced commits).

  ## Next Steps
  - R8+: campaign iterations until 10/10 from one invocation; then
    the integration gate.
  - Closure per STATUS_closure_protocol.md incl. the
    CYCLE_SAFETY_CAP config diff + ADR and the closure candidates.

  ## Risks
  - The template must make every goal meaningful — an order about a
    backoff cap needs one in the code; audit all ten before
    freezing v3.
  - Materialisation must never touch the operator's tree: copy into
    the isolated workspace only; the host-root hash criterion
    already polices it.
  - Real runs spend real tokens; provider flakiness fails a run
    honestly (A9).
  - Do-not-touch: config defaults by machine, the pass definition;
    the oversize exemption stays spent (R-0181).
  --- END f075-r7-2 ---

  --- BEGIN f075-r7-3 sha256=cf8121ef41c0178032da602c8606258762a4b2cc21c9bf2d0a21577575e8e043 ---
  # Context — F075 MILESTONE GATE: 10 flawless self-runs

  ## Active Branch
  feature/f075-self-run-gauntlet (from main after the Open PR Gate
  merged PR #178, the F071 closure)

  ## Scope
  Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
  harness + evaluator + matrix + frozen order set (v3 this round:
  orders + sample-project template) + live runner + injection
  driver + their tests. Reviewed product changes: run_mission
  exception boundary (R3), transport classes (R4), R-0186 execution
  wiring (R5), R-0187 cycles vehicle + R-0188 production DoD path
  (R6), R-0189 sample-project world + R-0190 blocked-gate
  escalation (R7, DECISIONS in the R6 verdict).

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
    .agent/authored/f075-r7-<n>.md after sha256 verification.
  - No pytest test may take a production/provider path (R-0182).
  - F046 safety: config and flag stay clamped to CYCLE_SAFETY_CAP;
    only the explicit experiment override exceeds it, recorded in
    the run's evidence.
  - Gauntlet runs use an ISOLATED data root AND an isolated
    materialised workspace copy; the operator's tree is never a job
    workspace; campaign evidence lives outside the repo during runs
    (R-0176); only matrix.md + matrix.json are committed under
    .agent/gauntlet/.
  - Do-not-touch: config defaults by machine, order-set edits
    mid-campaign (v3 is a versioned re-issue, count reset per A9);
    the pass definition freezes at campaign time.

  ## Steps
  R1-R6 done (PASS x6) → R7 R-0189 + R-0190 + re-proof + set-v3
  campaign (current) → R8+ iterations → integration gate → closure.
  --- END f075-r7-3 ---
