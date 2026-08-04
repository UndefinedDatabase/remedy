OUTCOME: in progress — F075 R4 (SPLIT, LARGE) started.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R4 (SPLIT, LARGE): persist the R3 PASS +
  fix R-0185 and R-0183 + DIAGNOSE R-0184 + attempt 2 only on a green
  fix. Save THIS ENTIRE block verbatim to .agent/last_block.md first
  (update OUTCOME at handback). You are on feature/f075-self-run-gauntlet
  at a4cb91ca. STOP rule: every phase ends with a verification; first
  red TEST gate -> STOP per AGENTS.md If-Blocked. The R-0184 diagnosis
  has its own STOP conditions (Phase 4). Commits < 500 lines — the
  feature's one oversize exemption is SPENT (R-0181); slice everything,
  including any regenerated goldens if needed.

  PHASE 1 — PERSIST THE R3 VERDICT (first commit)
   1. Save the three AUTHORED TEXT payloads below to
      .agent/authored/f075-r4-<n>.md (bytes between BEGIN/END markers,
      exclusive, incl. final newline; payload lines at column 0).
      Verify each sha256sum against its BEGIN-marker hash. Mismatch ->
      STOP, report raw sums, apply nothing.
   2. Apply f075-r4-1 -> .agent/live_review.md, f075-r4-2 ->
      .agent/plan.md, f075-r4-3 -> .agent/context.md — FULL
      replacements, byte-exact from the saved files.
   3. Commit 1: chore(f075): persist the R3 PASS, register
      R-0181..R-0185. Gate: python3 -m pytest
      tests/cli/test_golden_path.py -q -> exit 0. Push.

  PHASE 2 — FIX R-0185: TRANSPORT CLASSES IN THE CLASSIFIER (own commit)
   1. packages/orchestration/failure_postmortem.py: transport/provider
      -error classes aligned with the F001 transport taxonomy (inspect
      the existing taxonomy first; do NOT invent a parallel naming).
      The boundary already passes the exception object in
      FailureSignals — use type and text both. The injected shapes
      ("HTTP 503 ... closed the connection" as ConnectionError,
      "killed ..." as OSError) must classify to a REAL class, not
      unknown; genuinely unrecognizable input STAYS unknown
      (falsification test).
   2. Tests: one per new class + the two injected shapes end-to-end
      through record_iteration_failure; existing classifier tests stay
      green unedited unless an assertion was pinning the old dishonest
      unknown — say so per test in the handoff if so.
   3. Gate (STOP if red): the classifier's test file +
      tests/orchestration/test_orchestrator_loop.py -q -> exit 0. Push.

  PHASE 3 — FIX R-0183: UNMEASURED TOKENS SAY SO (own commit)
   1. Carry the unmeasured fact through gauntlet_evidence (read
      tokens_source; absent tokens + tokens_source=unmeasured is NOT
      zero) into both matrix formats: md renders "unmeasured", json
      carries an explicit source/null rather than 0/0. The evaluator's
      criteria are untouched — this is rendering honesty only.
   2. Regenerate BOTH goldens in the same commit and declare it. If
      the goldens diff exceeds the commit cap together with the code,
      split: code+tests commit first, goldens-regeneration commit
      second, each gated.
   3. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_gauntlet_evidence.py
      tests/orchestration/test_gauntlet_matrix.py
      tests/orchestration/test_gauntlet_evaluator.py -q -> exit 0. Push.

  PHASE 4 — DIAGNOSE R-0184 (evidence before any fix)
   1. ONE cheap live run: python3 scripts/self_run_gauntlet.py --live
      <fresh root OUTSIDE the repo> --only 1 --format json. Then read
      the run's OWN evidence — the ledger entries (moves decided,
      outcomes, refusals), the mission record, dispatched jobs and
      their states, dossier — and answer with evidence quotes:
      (a) what moves does the model produce; (b) do dispatched jobs
      run and finish; (c) why is declare_milestone_done /
      declare_mission_achieved never reached in budget; (d) why does
      the DoD gate never run (never invoked at all vs invoked and
      failing). Write the analysis to .agent/decisions.md with raw
      quotes (trimmed), and summarize it in the handoff.
   2. Decision fork — apply the FIRST matching rule:
      a. BOUNDED product/harness bug (wiring, prompt gap, a loop or
         gate invocation defect, budget plumbing): fix it with tests,
         gate with the touched files' test suites -> exit 0. Push.
      b. Model capability is the blocker (the default planner model
         cannot finish these missions): STOP after committing the
         analysis. Do NOT change orchestrator.model, do NOT edit
         orders, do NOT weaken the pass definition. The reviewer
         rules next round (config defaults by machine = do-not-touch).
      c. The fix is real product work beyond a bounded bug: STOP
         after committing the analysis (R2-seam precedent).
   3. If 2a landed green: prove it cheaply BEFORE the full campaign —
      rerun the SAME --only 1 live run in a fresh root; the run must
      now reach `achieved` with the DoD gate having produced a
      verdict (dod_result.json present). If it does not, treat as 2c:
      STOP with both runs' evidence.

  PHASE 5 — CAMPAIGN ATTEMPT 2 (only if Phase 4 reached a green 2a+3)
   1. Preconditions in the handoff: porcelain empty, pushed, provider
      reachable, set_hash re-verified, preflight_injections -> [].
   2. ONE invocation, full ten, fresh root OUTSIDE the repo:
      --live <root> --format both. No rerun inside the attempt, no
      order edits; provider flakiness fails a run honestly (A9).
   3. Copy matrix.md + matrix.json into .agent/gauntlet/attempt-02/
      and commit (sliced under the cap — R-0181). Evidence-root path
      + per-run terminals in the handoff.
   4. Gate: committed matrix.json parses, runs_recorded == 10; canary
      python3 -m pytest tests/cli/test_golden_path.py -q -> exit 0.
      The flawless count is REPORTED, not gated.

  PHASE 6 — HANDBACK
   git status --porcelain empty. Rewrite .agent/handoff.md per
   docs/agents/handback_template.md (per-commit tables; raw gate
   outputs; the R-0184 analysis summary; if attempt 2 ran, its
   summary table verbatim; sha256 proof per applied reviewer text).
   Update last_block OUTCOME. Completion report ends:
   "F075 R4 complete — awaiting review." (append "attempt 2 matrix
   recorded" if Phase 5 ran).

  --- BEGIN f075-r4-1 sha256=941af73a72341c876d411e759e6594af437e0708307a2fb756b3fbf253811d8d ---
  # Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

  Branch: feature/f075-self-run-gauntlet
  Scope: a gauntlet HARNESS — evaluator + matrix report + a frozen,
  versioned set of ten mission orders — that earns autonomy with
  data. Flawless per run = start command only + terminal green + all
  blocking DoD checks green + zero unknown postmortems + zero open
  decisions + host data root byte-untouched (before/after hash). The
  evaluator names the F070 era-fixture classes and the four
  harness-failure injection classes. Product changes ride along ONLY
  as reviewed SPLIT work (so far: the run_mission exception boundary,
  R3; the failure_postmortem transport classes, R4).

  ## Steps
  - R1 (SPLIT, LARGE): claim + T001 + T002 — PASS (history).
  - R2 (SPLIT, LARGE): R-0178 + T003a runner; compliant STOP on the
    missing boundary — PASS (history).
  - R3 (SPLIT, LARGE): R-0179/R-0180 + run_mission boundary + all
    four injections + campaign attempt 1 (0/10, honest) — PASS, see
    Verdicts.
  - R4 (SPLIT, LARGE, current): persist R3 verdict + fix R-0185
    (transport classes) + R-0183 (unmeasured tokens display) +
    DIAGNOSE R-0184 (nothing achieves, no DoD gate runs) with one
    cheap --only run; bounded fix -> land it; deep work or a model-
    capability DECISION -> STOP with the analysis. Then attempt 2
    from ONE invocation if and only if the R-0184 fix landed green.
  - R5+: campaign iterations until 10/10 from one invocation; then
    the integration gate per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR.

  ## Findings
  - R-0178 (product, Low): silent-zero evidence numbers. Fixed
    a11e089e. Done: R-0178
  - R-0179 (product, Low): never-fired injection was an ACCEPTED
    disposition. Fixed 587ec34a + d5213ad3 (injection_never_fired,
    REJECTED); reviewer-verified in the diff and the closed-set pin.
    Done: R-0179
  - R-0180 (product, Low): campaign had no per-order boundary;
    crash-path NameError. Fixed 97b6708a (_minimal_body pre-bound,
    nested fallback, runner_crashed named); reviewer-verified.
    Done: R-0180
  - R-0181 (process, Medium) 2026-08-04: TWO >500-line commits in R3
    (35cdc031: 753 diff lines, declared inseparable — accepted;
    0a2ce17c: 958, of which 895 are the ordered-whole matrix
    artifact). AGENTS.md grants ONE oversize per feature. Cause: the
    R3 ordering block told the worker to commit the artifact whole
    without declaring the exemption — a reviewer-order defect, not a
    worker one. Resolved by ruling: both stand (history is pushed;
    a rewrite is destructive); from R4 on, ordering blocks slice
    artifact commits or declare the exemption inline. Resolved.
  - R-0182 (test-safety, Medium) 2026-08-04, worker-reported: when
    preflight stopped refusing, two R2-era --live CLI tests fell
    through to production deps and started a REAL campaign inside
    pytest (~2 min, real provider calls; host isolation HELD, real
    root untouched). Fixed in-round: both tests replaced by
    preflight-level ones; the file states no test may take the
    production path. Reviewer verified: the full harness suite (236)
    runs in under a second with zero provider calls. Done: R-0182
  - R-0183 (product, Low) 2026-08-04, reviewer's read: the matrix
    renders unmeasured tokens as "0/0", indistinguishable from a
    measured zero — run.json carries tokens_source=unmeasured but
    RunEvidence and the matrix ignore it. Attempt 1 displays 0/0 on
    all ten runs while real tokens were spent. Fix: carry the
    unmeasured fact through gauntlet_evidence into both matrix
    formats (md "unmeasured", json null or explicit source field);
    regenerate goldens in the same commit and say so.
  - R-0184 (product, High) 2026-08-04, campaign attempt 1: ZERO of
    ten runs reached `achieved` and the DoD gate NEVER ran — seven
    iteration_limit, three iteration_failed. The loop under the
    default planner model produces no run that finishes its mission
    within budget. Needs DIAGNOSIS with evidence (one --only live
    run, read the moves/ledger) before any fix; if the blocker is
    model capability, that is a DECISION for the reviewer, not a
    silent model switch (config defaults by machine = do-not-touch).
  - R-0185 (product, Medium) 2026-08-04, campaign attempt 1 +
    worker's pre-run prediction: failure_postmortem.classify reads
    the injected transport errors ("HTTP 503 ...", "killed ...") as
    `unknown`, so the three raise-class runs also fail
    no_unknown_postmortems. The boundary already hands the classifier
    the exception object. Fix: transport/provider-error classes in
    failure_postmortem aligned with the F001 transport taxonomy;
    falsification tests; the gauntlet fixtures' expected classes
    updated only where the honest classification changes.
  - Next free ID: R-0186.

  ## Verdicts
  - R1: PASS. R2: PASS. Full texts in this file's git history
    (55f706db, c95f23db).
  - R3: PASS (SPLIT, LARGE, 2026-08-04). Range ef23e274..a4cb91ca
    (8 commits, all tabled). Transport: r3-1/2/3 cmp 0 against the
    reviewer's scratchpad originals; live_review at the apply commit
    byte-equals the authored text. Reviewer re-ran every gate: P2
    133 (with the round's added tests), P3 loop/e2e/era 184, P5
    harness 236, canary 42 — all exit 0, porcelain empty. The
    boundary verified in the real diff (digest/cost pre-bound,
    except Exception only, no retry, never-raising post-mortem
    writer, per-iteration post-mortem dirs) and through its 11
    tests; the honest-red P2 first run (worker's own closed-set pin
    tripped by the R-0179 change, fixed in d5213ad3) is exactly the
    discipline working. Campaign attempt 1 audited from the
    committed matrix: internally consistent, 0/10, criteria counts
    match the handoff exactly, all four injections fired and
    degraded to ledgered_failure. Deviations accepted: the two
    oversize commits ruled in R-0181; the after-the-fact matrix
    write (now done by --live itself, pinned); escalation not used
    by the boundary (honest terminal instead — F051 asks a human a
    question, a raised failure is a failure to ledger;
    decisions.md). R-0181..R-0185 registered. Worktree hygiene:
    primary only, porcelain empty at verdict.
    LAST_REVIEWED_SHA = a4cb91ca.
  --- END f075-r4-1 ---

  --- BEGIN f075-r4-2 sha256=a4a90b75826062d2c2cd36c1e076d73f8d24de24c6d20ef3a195fe031b2fb428 ---
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
  R4 (SPLIT, LARGE): persist R3 PASS + fix R-0185 (transport classes
  in failure_postmortem, F001-aligned, with tests) + R-0183
  (unmeasured tokens rendered as unmeasured, goldens regenerated
  declared) + DIAGNOSE R-0184 with one cheap --only live run and the
  run's own ledger: why does nothing reach `achieved` and why does
  the DoD gate never run? Bounded fix -> land with tests. Deep
  product work or a model-capability blocker -> STOP with the
  analysis (R2-seam precedent); a model switch is a reviewer
  DECISION, never a silent config change. Attempt 2 (full ten, ONE
  invocation, matrix to .agent/gauntlet/attempt-02/) runs ONLY if
  the R-0184 fix landed green.

  ## Next Steps
  - R5+: campaign iterations until 10/10 from one invocation; then
    the integration gate.
  - Closure per STATUS_closure_protocol.md incl. config diff + ADR.

  ## Risks
  - R-0184 is the feature's real work now: the campaign found a
    product truth (missions do not finish unattended in budget) and
    the fix must not weaken the pass definition to pass the gate.
  - Real runs spend real tokens; provider flakiness fails a run
    honestly (A9).
  - Do-not-touch: config defaults by machine, order-set edits
    mid-campaign, the pass definition (freezes at campaign time; the
    R-0183 display fix touches rendering, not criteria).
  --- END f075-r4-2 ---

  --- BEGIN f075-r4-3 sha256=e975c006b099e46216a967d0f0bc700ef8764efe4b8502ec480ceb73ff5b8bc0 ---
  # Context — F075 MILESTONE GATE: 10 flawless self-runs

  ## Active Branch
  feature/f075-self-run-gauntlet (from main after the Open PR Gate
  merged PR #178, the F071 closure)

  ## Scope
  Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
  harness + evaluator + matrix + frozen ten-order set + live runner
  + injection driver + their tests. Reviewed product changes so far:
  the run_mission exception boundary (R3); this round adds the
  failure_postmortem transport classes (R-0185) and whatever bounded
  fix the R-0184 diagnosis proves — everything else stays
  harness-side.

  ## Constraints
  - Round gate = scoped pytest command(s) authored in the step
    block; canary per handback:
    python3 -m pytest tests/cli/test_golden_path.py -q. Docs-round
    gate applies to any commit touching docs/roadmap/**:
    python3 -m pytest tests/docs/ -q. Full-suite pytest -n auto only
    at the integration gate; the resource-safety rules of
    tests/regression apply.
  - Commits < 500 lines (ONE declared oversize per feature — R3
    used it; R-0181 rules the second one closed, no third);
    authored texts applied byte-exact from
    .agent/authored/f075-r4-<n>.md after sha256 verification.
  - No pytest test may take a production/provider path (R-0182).
  - Gauntlet runs use an ISOLATED data root; campaign evidence
    lives outside the repo during runs (R-0176); only matrix.md +
    matrix.json are committed under .agent/gauntlet/.
  - Do-not-touch: config defaults by machine, order-set edits
    mid-campaign; the pass definition freezes at campaign time.

  ## Steps
  R1-R3 done (PASS x3) → R4 R-0184 diagnosis + fixes + attempt 2
  (current) → R5+ iterations → integration gate → closure.
  --- END f075-r4-3 ---
