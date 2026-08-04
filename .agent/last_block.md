OUTCOME: executed with a STOP — F075 R9: R8 PASS persisted; R-0192 BUILT (one condition — a dispatch_job ledger entry with no job_id no longer overwrites the attribution; 5 tests incl. the R8 sequence replayed to achieved). Phase 3 re-proof: the chain CLOSES — dispatch, execute, gate RELEASED, declare_milestone_done accepted, TWICE in one run (_milestones_done ['M001','M002']), zero open decisions. Terminal still iteration_limit: the compiler expanded g01's single-milestone goal into THREE plan milestones and each costs 3 iterations (dispatch, R-0191 refusal, declare) against a budget of 6 -> rule 3.3 STOP; campaign NOT run. Two reviewer calls recorded: whether a refused iteration should cost budget, and whether the R1-era order budgets need a v4 re-issue.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R9 (SPLIT, LARGE): persist the R8 PASS +
  R-0192 (the attribution fix) + re-proof + the set-v3 campaign. Save
  THIS ENTIRE block verbatim to .agent/last_block.md first (update
  OUTCOME at handback). You are on feature/f075-self-run-gauntlet at
  09348505. STOP rule: every phase ends with a verification; first red
  TEST gate -> STOP per AGENTS.md If-Blocked. Phase 3 has its own hard
  STOP. Commits < 500 lines, NO oversize left (R-0181).

  PHASE 1 — PERSIST THE R8 VERDICT (first commit)
   1. Save the three AUTHORED TEXT payloads below to
      .agent/authored/f075-r9-<n>.md (bytes between BEGIN/END markers,
      exclusive, incl. final newline; payload lines at column 0).
      Verify each sha256sum against its BEGIN-marker hash. Mismatch ->
      STOP, report raw sums, apply nothing.
   2. Apply f075-r9-1 -> .agent/live_review.md, f075-r9-2 ->
      .agent/plan.md, f075-r9-3 -> .agent/context.md — FULL
      replacements, byte-exact from the saved files.
   3. Commit 1: chore(f075): persist the R8 PASS, register R-0192.
      Gate: python3 -m pytest tests/cli/test_golden_path.py -q ->
      exit 0. Push.

  PHASE 2 — R-0192: A REFUSED DISPATCH IS NOT A DISPATCH (own commit)
   Keep this commit to the one condition and its tests — nothing else
   rides along.
   1. dispatched_job_for (orchestrator_loop.py): only a dispatch_job
      entry that actually DISPATCHED (outcome carries a job_id /
      status dispatched) updates the attribution; a refused entry is
      skipped, never erasing the real answer.
   2. Tests (fakes, R-0182): the R8 sequence — dispatch, refused
      dispatch, declare — now ACHIEVES end-to-end with a released
      verdict; real-then-refused keeps the attribution; several real
      dispatches -> the latest REAL one wins; a mission with only
      refused dispatches still answers "" honestly.
   3. Gate (STOP if red): python3 -m pytest
      tests/orchestration/test_orchestrator_loop.py
      tests/orchestration/test_mission_e2e.py
      tests/orchestration/test_era_integrity.py -q -> exit 0. Push.

  PHASE 3 — RE-PROOF (one order, hard-gated)
   1. python3 scripts/self_run_gauntlet.py --live <fresh root OUTSIDE
      the repo> --only 1 --format json
   2. REQUIRED: terminal `achieved` AND dod_result.json with
      released: true AND zero open decisions. Quote the terminal, the
      verdict fields, the declare move's ledger entry and the full
      criteria table in the handoff.
   3. Anything missing -> STOP: commit nothing further, record the
      full evidence trail in .agent/decisions.md, hand back (the
      R4-R8 STOP precedent).

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
   "F075 R9 complete — awaiting review." (append "set-v3 campaign
   matrix recorded" if Phase 4 ran).

  --- BEGIN f075-r9-1 sha256=cde835a274e1dc65ee6d2f7b7b0afc05c882956fd01f1ec86d62c440553c75da ---
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
  escalation (R7), released-gate dispatch guard (R8), the
  attribution fix (R9).

  ## Steps
  - R1-R7 (SPLIT, LARGE): harness + set + boundary + injections +
    attempt 1 + execution + cycles vehicle + DoD path + template
    world + escalation — PASS x7 (history).
  - R8 (SPLIT, LARGE): R-0191 built; the model OBEYED the
    instructive refusal and declared — blocked only by the latent
    attribution defect the guard exposed; compliant 3.3 STOP —
    PASS, see Verdicts.
  - R9 (SPLIT, LARGE, current): persist R8 verdict + R-0192 (a
    refused dispatch_job entry must not erase the attribution) +
    re-proof (--only 1 must reach achieved WITH a released verdict)
    + the set-v3 campaign from ONE invocation.
  - R10+: campaign iterations until 10/10 from one invocation; then
    the integration gate per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR (the
    CYCLE_SAFETY_CAP / default raise — human-applied).

  ## Findings
  - R-0178..R-0190: all fixed and reviewer-verified; R-0181
    resolved by ruling (exemption SPENT). Done: R-0178 ·
    Done: R-0179 · Done: R-0180 · Done: R-0182 · Done: R-0183 ·
    Done: R-0184 · Done: R-0185 · Done: R-0186 · Done: R-0187 ·
    Done: R-0188 · Done: R-0189 · Done: R-0190 · R-0181 Resolved.
  - R-0191 (product, High): released-gate dispatch guard. Built
    03038187 — refusal only on gate_released is True, verdict read
    via load_gate_result (a test pins that the guard's source never
    re-derives), LATEST-job rules, instructive refusal naming
    declare_milestone_done; 9 tests; the R8 re-proof shows the
    model OBEYING it (one dispatch, one refusal, then the declare
    move). Reviewer-verified. Done: R-0191
  - R-0192 (product, Medium) 2026-08-04, R8 re-proof — a latent
    defect the guard exposed: dispatched_job_for keeps the LAST
    dispatch_job ledger entry's outcome.job_id for the milestone,
    and a REFUSED dispatch is still a dispatch_job move with NO
    job_id — so it overwrote the real attribution with "" (source:
    orchestrator_loop.py:1319, unconditional overwrite). The
    declare move was then refused ("no job was ever dispatched"),
    the second-refusal rule escalated, and the run ended escalated
    with one open decision. Pre-existing: before R-0191 no ledger
    held a refused dispatch beside a real one. Fix: only an entry
    whose outcome actually dispatched (status dispatched / job_id
    present) updates the attribution; tests for refused-then-claim
    (achieves end-to-end), real-then-refused (attribution kept),
    and multiple dispatches (latest REAL one wins).
  - Deferred closure candidates: F070 review gap; absent resume
    verb.
  - Next free ID: R-0193.

  ## Verdicts
  - R1-R7: PASS x7. Full texts in this file's git history
    (55f706db, c95f23db, e5ca780e, 6a002f09, 9e8ced5b, df856730,
    1fe38c56).
  - R8: PASS (SPLIT, LARGE, 2026-08-04). Range 854a9860..09348505
    (4 commits, all tabled). Transport: r8-1/2/3 cmp 0 against the
    reviewer's scratchpad originals; live_review at the apply
    commit byte-equals the authored text. Reviewer re-ran every
    gate: loop/e2e/era/injection/runner 307 (all five suites
    UNEDITED), remaining seven files 386, canary 42 — all exit 0,
    porcelain empty. R-0191 verified in the diff and in the live
    re-proof ledger: the R7 six-dispatch pattern became
    dispatch -> instructive refusal -> declare_milestone_done — the
    model followed the guard's named move. The 3.3 STOP is
    COMPLIANT and TRUE: the attribution defect is real (reviewer
    read the unconditional overwrite at orchestrator_loop.py:1319),
    pre-existing, and precisely located by the worker WITH the
    honest note that the run would also fail no_open_decisions.
    Guard design deviations all accepted (released-only trigger;
    no self-declaring — the F070 authority boundary). R-0192
    registered. Worktree hygiene: primary only, porcelain empty.
    LAST_REVIEWED_SHA = 09348505.
  --- END f075-r9-1 ---

  --- BEGIN f075-r9-2 sha256=7abaf098fb8548c4282ef00bc81ca6133d133bac56f49da5c2313658c5bd6f23 ---
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
  R9 (SPLIT, LARGE): persist R8 PASS + R-0192 — dispatched_job_for
  only updates its answer from a dispatch_job entry that actually
  dispatched (job_id present / outcome status dispatched); a
  refused dispatch never erases the real attribution — with tests
  for refused-then-claim (achieves), real-then-refused (kept), and
  latest-REAL-wins — + re-proof (--only 1 must reach achieved WITH
  a released verdict, hard STOP otherwise) + the set-v3 campaign
  (full ten, ONE invocation, matrix to .agent/gauntlet/attempt-02/,
  sliced commits).

  ## Next Steps
  - R10+: campaign iterations until 10/10 from one invocation; then
    the integration gate.
  - Closure per STATUS_closure_protocol.md incl. the
    CYCLE_SAFETY_CAP config diff + ADR and the closure candidates.

  ## Risks
  - The chain is one condition away from its first achieved
    self-run — resist bundling anything else into the fix commit.
  - Real runs spend real tokens; provider flakiness fails a run
    honestly (A9).
  - Do-not-touch: config defaults by machine, the pass definition,
    order/template edits mid-campaign; the oversize exemption stays
    spent (R-0181).
  --- END f075-r9-2 ---

  --- BEGIN f075-r9-3 sha256=b9af4aac91fefa47844f2a17917a690781885f80bb09374d75d50918b720c80e ---
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
  escalation (R7), released-gate dispatch guard (R8), the R-0192
  attribution fix (R9).

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
    .agent/authored/f075-r9-<n>.md after sha256 verification.
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
  R1-R8 done (PASS x8) → R9 R-0192 + re-proof + set-v3 campaign
  (current) → R10+ iterations → integration gate → closure.
  --- END f075-r9-3 ---
