OUTCOME: in progress — F075 R3 (SPLIT, LARGE) started.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R3 (SPLIT, LARGE): persist the R2 PASS +
  fix R-0179/R-0180 + the run_mission exception boundary + unblock the
  three raise-class injections + campaign attempt 1. Save THIS ENTIRE
  block verbatim to .agent/last_block.md first (update OUTCOME at
  handback). You are on feature/f075-self-run-gauntlet at ef23e274.
  STOP rule: every phase ends with a verification; at the FIRST red TEST
  gate STOP per AGENTS.md If-Blocked, record the raw failure, do not
  continue. The CAMPAIGN result (Phase 6) is campaign data: below 10/10
  is an EXPECTED outcome, recorded honestly, never a stop and never a
  reason to edit orders or rerun inside the same attempt.

  PHASE 1 — PERSIST THE R2 VERDICT (first commit)
   1. Save the three AUTHORED TEXT payloads below to
      .agent/authored/f075-r3-<n>.md (bytes between BEGIN/END markers,
      exclusive, incl. the final newline; payload lines start at column
      0). Verify each sha256sum against its BEGIN-marker hash. Mismatch
      -> STOP, report raw sums, apply nothing.
   2. Apply f075-r3-1 -> .agent/live_review.md, f075-r3-2 ->
      .agent/plan.md, f075-r3-3 -> .agent/context.md — each a FULL file
      replacement, byte-exact copy of the saved file.
   3. Commit 1: chore(f075): persist the R2 PASS, register
      R-0179/R-0180. Gate: python3 -m pytest
      tests/cli/test_golden_path.py -q -> exit 0. Push.

  PHASE 2 — FIX R-0179 AND R-0180 (own commit(s), finding by finding)
   1. R-0179: add a REJECTED disposition (suggested name
      injection_never_fired) to gauntlet_evaluator's
      REJECTED_DISPOSITIONS; TruncatedResponseInjector.settle uses it
      when the injection never fired; update the line-92 pinning test
      so a never-fired injection FAILS the run through the evaluator
      (one end-to-end assertion: run verdict not flawless). Record in
      .agent/decisions.md: closed-set tightening, landed BEFORE any
      campaign (pre-freeze, no ADR). Mark Done: R-0179 in
      .agent/live_review.md in the same commit.
   2. R-0180: per-order boundary in run_campaign (a raise from
      run_order becomes a synthetic crashed OrderOutcome; the loop
      continues); harden run_order's crash path (body initialized or
      the fallback nested) so the hash-after line can never hit an
      unbound body. One test where the CRASH PATH itself raises (e.g.
      a collector that throws on the crash re-entry) proving the
      campaign continues and evidence for the other runs survives.
      Mark Done: R-0180 same commit.
   3. Gate: python3 -m pytest tests/orchestration/test_gauntlet_injection.py
      tests/orchestration/test_gauntlet_runner.py
      tests/orchestration/test_gauntlet_evaluator.py -q -> exit 0. Push.

  PHASE 3 — THE run_mission EXCEPTION BOUNDARY (product change, own commits)
   The DECISION of record (R2 verdict; worker analysis decisions.md
   2026-08-04). Scope: packages/orchestration/orchestrator_loop.py —
   minimal boundary, nothing else.
   1. A raise of Exception (NEVER KeyboardInterrupt/SystemExit) from
      the per-iteration work — the provider call, dispatch via
      execute_move, update_dossier/refresh — is caught ONCE per
      iteration and becomes: (a) a classified F010 postmortem via the
      existing failure_postmortem path (a class it cannot determine is
      recorded honestly as its unknown/unclassified value, never
      invented); (b) the iteration's ledger entry (the docstring's
      "every iteration leaves a ledger entry" becomes true under a
      raise); (c) an honest terminal on the result (pick/extend the
      existing terminal constants — record the naming decision in
      .agent/decisions.md) or an F051 escalation where the existing
      escalation semantics apply. NO retry logic in the boundary:
      transport retries live below call_fn (F001).
   2. Tests (new or in the existing loop test file — follow the repo's
      test_x <-> x convention): raising call_fn, raising dispatch,
      raising update_dossier — each leaves a ledger entry + classified
      postmortem + honest terminal and does NOT propagate; a
      KeyboardInterrupt DOES propagate; the mission record is not
      corrupted (reloadable) after a boundary catch.
   3. Gate (STOP if red): the loop's own test file(s) — python3 -m
      pytest tests/orchestration/test_orchestrator_loop*.py -q (adjust
      to the real filenames, state them in the handoff) -> exit 0,
      proving the EXISTING suite stays green with the new tests. Push.

  PHASE 4 — UNBLOCK THE THREE INJECTION CLASSES
   1. gauntlet_injection.py: drivers for provider_api_error_mid_move
      (call_fn raises once at the named move), harness_death_mid_dispatch
      (dispatch raises once), harness_death_mid_write (update_dossier
      raises once) — decorators around production callables, same
      pattern as the truncation injector; move the three from
      BLOCKED_INJECTIONS to SUPPORTED_INJECTIONS; dispositions read
      off what the product DID (postmortem written + honest
      terminal/escalation -> ledgered/escalated/retried; anything else
      -> the named mishandling or unclassified). Runner passes
      dispatch/update_dossier wrappers through the same RunnerDeps
      seams it already owns.
   2. Preflight now passes a full-set live run; the exit-2 refusal for
      unknown classes stays. Update tests: each class driveable end-to-
      end against a fake loop that RAISES at the seam; the settled
      run.json block carries class + disposition + detail.
   3. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_gauntlet_injection.py
      tests/orchestration/test_gauntlet_runner.py
      tests/orchestration/test_self_run_gauntlet.py -q -> exit 0. Push.

  PHASE 5 — FULL HARNESS GATE
   python3 -m pytest tests/orchestration/test_gauntlet_evidence.py
   tests/orchestration/test_gauntlet_evaluator.py
   tests/orchestration/test_gauntlet_matrix.py
   tests/orchestration/test_gauntlet_orders.py
   tests/orchestration/test_gauntlet_injection.py
   tests/orchestration/test_gauntlet_runner.py
   tests/orchestration/test_self_run_gauntlet.py -q -> exit 0. If the
   golden matrices changed bytes (R-0179 tightening does not touch the
   recorded fixtures unless a fixture declares a never-fired
   injection), regenerate in the same commit and say so. Push.

  PHASE 6 — CAMPAIGN ATTEMPT 1 (real runs, real tokens)
   1. Preconditions in the handoff BEFORE starting: porcelain empty,
      branch pushed, provider reachable (one cheap ping), set_hash
      re-verified via load_order_set(), preflight_injections -> [].
   2. ONE invocation: python3 scripts/self_run_gauntlet.py --live
      <campaign-root OUTSIDE the repo> --format both. Per-order
      budgets are the orders' own; set ceiling ~3.1M tokens. Provider
      flakiness fails a run honestly (A9) — no rerun inside the
      attempt, no order edits.
   3. Copy matrix.md + matrix.json (only these) into
      .agent/gauntlet/attempt-01/ and commit — failed gauntlets are
      KEPT. Record the evidence-root path + per-run terminals in the
      handoff.
   4. Gate: the committed matrix.json parses, runs_recorded == 10;
      canary python3 -m pytest tests/cli/test_golden_path.py -q ->
      exit 0. The flawless count is REPORTED, not gated.

  PHASE 7 — HANDBACK
   git status --porcelain empty. Rewrite .agent/handoff.md per
   docs/agents/handback_template.md (per-commit tables; raw gate
   outputs with exit codes; the campaign summary table verbatim;
   sha256 proof per applied reviewer text vs its .agent/authored/
   file). Update last_block OUTCOME. Completion report ends:
   "F075 R3 complete — attempt 1 matrix recorded, awaiting review."

  --- BEGIN f075-r3-1 sha256=f1224711b244b770af8c829d0ed7c1339632fb2ddaa59d6639d83338720d97ae ---
  # Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

  Branch: feature/f075-self-run-gauntlet
  Scope: a gauntlet HARNESS — evaluator + matrix report + a frozen,
  versioned set of ten mission orders — that earns autonomy with
  data. Flawless per run = start command only + terminal green + all
  blocking DoD checks green + zero unknown postmortems + zero open
  decisions + host data root byte-untouched (before/after hash). The
  evaluator names the F070 era-fixture classes (R-0141/R-0143/R-0144/
  R-0145/R-0146/R-0147/R-0148) and the harness-failure injection
  classes (provider API error mid-move, truncated model response,
  harness death mid-dispatch and mid-write) — each degrades to a
  LEDGERED failure, retry within budget, or escalation, never a
  silent success. This round the scope gains ONE reviewed product
  change: the run_mission exception boundary (DECISION 2026-08-04 in
  the R2 verdict) — the loop's own docstring contract ("every
  iteration leaves a ledger entry") made true under a raise.

  ## Steps
  - R1 (SPLIT, LARGE): claim + T001 evaluator/matrix/dry-run proof +
    T002 frozen ten-order set — PASS, see Verdicts.
  - R2 (SPLIT, LARGE): R1 PASS persisted + R-0178 fixed + T003a
    runner/injection driver/--live CLI; campaign attempt REFUSED at
    preflight on the missing run_mission exception boundary —
    compliant STOP, PASS, see Verdicts.
  - R3 (SPLIT, LARGE, current): persist R2 verdict + fix R-0179 and
    R-0180 + the run_mission exception boundary (product change, own
    tests) + unblock the three raise-class injections + campaign
    attempt 1 from ONE invocation, matrix recorded honestly — below
    10/10 is campaign data, not a round failure.
  - R4+: campaign iterations until 10/10 stands from one invocation;
    then the integration gate per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR — a
    human applies it, never the harness.

  ## Findings
  - R-0178 (product, Low): non-numeric evidence numbers were silent
    zeros. Fixed a11e089e, reviewer-verified in the diff and by
    rerunning the evidence/evaluator/matrix gates; goldens unchanged.
    Done: R-0178
  - R-0179 (product, Low) 2026-08-04, reviewer's R2 read: an
    injection that NEVER FIRED settles as disposition
    ledgered_failure — an ACCEPTED class — so a run that never
    exercised its declared injection can still count flawless while
    its evidence claims a failure-handling that never happened
    (test_gauntlet_injection.py pins this at line 92). Benign today
    only because INJECT_ON_MOVE=1 and reaching `achieved` needs at
    least one move. Fix: a never-fired injection settles to its own
    REJECTED disposition (e.g. injection_never_fired) so the
    evaluator fails the run honestly; update the pinning test and
    the evaluator's REJECTED_DISPOSITIONS; record in decisions.md
    that this tightens the closed set BEFORE any campaign has run
    (pre-freeze, so no ADR needed — T1_F075.md freezes the
    definition at campaign time).
  - R-0180 (product, Low) 2026-08-04, reviewer's R2 read:
    run_campaign's docstring promises "a run that dies takes only
    itself down" but its loop has no boundary — only run_mission
    raises are absorbed (inside run_order). A raise from run_order's
    own crash path (evidence write, the re-entered collectors) kills
    the rest of the campaign; in that path `body` can also be
    unbound at the hash-after line (NameError masks the original
    error). Fix: per-order boundary in run_campaign recording a
    synthetic crashed OrderOutcome; initialize body before the try
    or nest the crash path's fallback; one test where the crash
    path itself raises.
  - Next free ID: R-0181.

  ## Verdicts
  - R1: PASS (SPLIT, LARGE, 2026-08-04). Range 563b15b4..740ff133.
    Full text in this file's git history (55f706db).
    LAST_REVIEWED_SHA was 740ff133.
  - R2: PASS (SPLIT, LARGE, 2026-08-04). Range 740ff133..ef23e274
    (7 commits, all tabled). Transport: r2-1/2/3 cmp 0 against the
    reviewer's scratchpad originals; live_review at the apply commit
    byte-equals the authored text (worker's later append is the
    permitted Done-mark only). Reviewer re-ran every gate: P2 111,
    slice 205, canary 42 — all exit 0 — and re-reproduced the golden
    matrix byte-exact through the CLI. R-0178 fix verified in the
    real diff. The STOP is COMPLIANT and TRUE: reviewer reproduced
    the escape independently (AST: zero try-blocks in run_mission
    698-885 and execute_move; a raising call_fn escaped
    run_structured_call at structured_outputs.py:158 in a live
    probe), so three injection classes are honestly undriveable and
    the preflight refusal spent zero tokens. R-0179/R-0180
    registered from the reviewer's read. DECISION 2026-08-04 (§4.7):
    the missing run_mission exception boundary is built IN THIS
    BRANCH as reviewed SPLIT work with its own tests — alternatives
    considered: a separate feature first (slower, breaks campaign
    momentum for a change this feature's acceptance explicitly
    demands) and a harness-side except (rejected: grades the
    harness's crutch, decisions.md 2026-08-04); reversal = any later
    relay. Worktree hygiene: primary only, porcelain empty.
    LAST_REVIEWED_SHA = ef23e274.
  --- END f075-r3-1 ---

  --- BEGIN f075-r3-2 sha256=918012f5d869f402c01378470ec35d95241a1126b57eca78651f518e6c5699e8 ---
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
  R3 (SPLIT, LARGE): persist R2 PASS + fix R-0179 (never-fired
  injection is a REJECTED disposition) + R-0180 (campaign-level
  boundary, crash-path NameError) + the run_mission exception
  boundary (product change: classify via failure_postmortem, write
  the F010 postmortem, append the iteration's ledger entry, end on
  an honest terminal or F051 escalation — own tests, existing loop
  suite stays green) + unblock the three raise-class injections +
  campaign attempt 1 from ONE invocation (evidence outside the
  repo, matrix kept under .agent/gauntlet/attempt-01/). Below 10/10
  is campaign data; a red TEST gate is a STOP.

  ## Next Steps
  - R4+: campaign iterations — targeted fix orders + full reruns —
    until 10/10 from one invocation; then the integration gate.
  - Closure per STATUS_closure_protocol.md incl. config diff + ADR.

  ## Risks
  - The boundary touches the loop's core: it must catch Exception
    only (never KeyboardInterrupt/SystemExit), add no retry of its
    own (transport retries are F001's, below call_fn), and keep the
    full existing loop suite green.
  - Real runs spend real tokens (set ceiling ~3.1M); provider
    flakiness makes a run FAIL honestly (A9).
  - Do-not-touch: config defaults by machine, order-set edits
    mid-campaign; the pass definition freezes at campaign time —
    R-0179's tightening lands before any campaign has run.
  --- END f075-r3-2 ---

  --- BEGIN f075-r3-3 sha256=47e68f9d646d4ef43a407ee208859e1ae0a116e6bd7afdf0b77270cd5b2492af ---
  # Context — F075 MILESTONE GATE: 10 flawless self-runs

  ## Active Branch
  feature/f075-self-run-gauntlet (from main after the Open PR Gate
  merged PR #178, the F071 closure)

  ## Scope
  Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
  harness + evaluator + matrix report + frozen ten-order set + live
  runner + injection driver + their tests. This round adds ONE
  reviewed product change: the run_mission exception boundary in
  packages/orchestration/orchestrator_loop.py (DECISION 2026-08-04,
  R2 verdict) — everything else stays harness-side.

  ## Constraints
  - Round gate = scoped pytest command(s) authored in the step
    block; canary per handback:
    python3 -m pytest tests/cli/test_golden_path.py -q. Docs-round
    gate applies to any commit touching docs/roadmap/**:
    python3 -m pytest tests/docs/ -q. Full-suite pytest -n auto only
    at the integration gate; the resource-safety rules of
    tests/regression apply.
  - Commits < 500 lines; authored texts applied byte-exact from
    .agent/authored/f075-r3-<n>.md after sha256 verification.
  - Gauntlet runs use an ISOLATED data root, never the operator's
    real one; campaign evidence lives outside the repo during runs
    (docs/agents/integration_gate.md, R-0176); only matrix.md +
    matrix.json are committed under .agent/gauntlet/.
  - Do-not-touch: config defaults by machine, order-set edits
    mid-campaign; the pass definition freezes at campaign time.

  ## Steps
  R1 done (PASS) → R2 done (PASS, compliant STOP) → R3 boundary +
  injections + campaign attempt 1 (current) → R4+ iterations →
  integration gate → closure.
  --- END f075-r3-3 ---
