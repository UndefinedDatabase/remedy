OUTCOME: in progress — F075 R2 (SPLIT, LARGE) started.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R2 (SPLIT, LARGE): persist the R1 PASS +
  fix R-0178 + T003a live runner + campaign attempt 1. Save THIS ENTIRE
  block verbatim to .agent/last_block.md first (update OUTCOME at
  handback). You are on feature/f075-self-run-gauntlet at 740ff133.
  STOP rule: every phase ends with a verification; at the FIRST red TEST
  gate STOP per AGENTS.md If-Blocked, record the raw failure in the
  handoff, do not continue. The CAMPAIGN result itself (Phase 4) is
  campaign data: below 10/10 is an EXPECTED outcome, recorded honestly,
  never a reason to stop or to retry-with-edits.

  PHASE 1 — PERSIST THE R1 VERDICT (first commit)
   1. Save the three AUTHORED TEXT payloads below to
      .agent/authored/f075-r2-<n>.md (bytes between BEGIN/END markers,
      exclusive, incl. the final newline; payload lines start at column
      0). Verify each sha256sum against its BEGIN-marker hash. Mismatch
      -> STOP, report raw sums, apply nothing.
   2. Apply f075-r2-1 -> .agent/live_review.md and f075-r2-2 ->
      .agent/plan.md (FULL replacements, byte-exact copies of the saved
      files). Apply f075-r2-3 -> .agent/context.md (the FROM line occurs
      once; replace it with the two TO lines, copied from the saved
      file).
   3. Commit 1: chore(f075): persist the R1 PASS, register R-0178.
      Gate: python3 -m pytest tests/cli/test_golden_path.py -q -> exit 0.
      Push.

  PHASE 2 — FIX R-0178 (own commit)
   1. packages/orchestration/gauntlet_evidence.py: a non-numeric
      wall_seconds or tokens value in run.json becomes a load_error
      (malformed evidence -> the run is not flawless), so _as_number's
      docstring stands as written. Keep honest edge semantics: absent
      fields still default (absence is not malformation); a bool is not
      a number. One falsification test per field (wall_seconds, tokens
      in, tokens out) in tests/orchestration/test_gauntlet_evidence.py;
      mark Done: R-0178 in .agent/live_review.md in the same commit.
   2. Gate: python3 -m pytest tests/orchestration/test_gauntlet_evidence.py
      tests/orchestration/test_gauntlet_evaluator.py
      tests/orchestration/test_gauntlet_matrix.py -q -> exit 0. If the
      golden matrices change bytes, regenerate them IN THIS COMMIT and
      say so in the handoff. Push.

  PHASE 3 — T003a: THE LIVE RUNNER
   Design authority: T1_F075.md (read it again before this phase). The
   runner EXECUTES; the evaluator keeps sole authority over judging.
   Record every interface decision in .agent/decisions.md.
   1. New module (suggested packages/orchestration/gauntlet_runner.py)
      + CLI wiring in scripts/self_run_gauntlet.py behind an explicit
      --live flag (the exit-2 refusal without --dry-run/--live stays).
      Per order, in manifest order from load_order_set():
      - a FRESH isolated data root (REMEDY_DATA_DIR semantics) per run;
        the operator's real data root is hashed BEFORE and AFTER every
        run and both digests land in run.json (the criterion's facts);
      - unattended --yes semantics under the order's own budget
        (max_iterations, max_tokens, max_wall_seconds), driven through
        the EXISTING mission intake -> compile -> orchestrator loop
        path — the runner adds no second execution mechanism;
      - evidence written per run in the recorded schema
        (gauntlet_run_version 1: terminal_status, interventions,
        postmortems, open_decisions, era_defects, injections,
        wall/tokens, evidence_links, dod_result.json when the gate
        ran) — the same bytes the dry-run evaluator already judges;
      - failures along the way become postmortems/escalations via the
        EXISTING F010/F051 paths, never swallowed by the runner.
   2. Injection driver for the orders that declare injections
      (g06-g09): deterministic fault injection at EXISTING seams
      (transport/dispatch/write). Every injected event is recorded in
      run.json injections[] with class + disposition + detail. HARD
      RULE: no product code bypass, no test-only branch added to
      production paths; if a needed seam does not exist, STOP after
      committing the runner work so far and hand back naming the exact
      seam — a product seam is its own reviewed change, never smuggled.
   3. Runner tests (no provider calls: fake loop/provider doubles):
      evidence lands in schema and is judged by the real evaluator;
      real root hashed before/after and UNTOUCHED (asserted by hash);
      isolated root actually used; budgets passed through; injection
      events recorded; a runner crash mid-campaign leaves prior runs'
      evidence intact and the campaign judgeable.
   4. SLICE GATE (STOP if red): the new runner test file + the four
      existing gauntlet test files + tests/orchestration/
      test_self_run_gauntlet.py -> python3 -m pytest <those> -q,
      exit 0. Push.

  PHASE 4 — CAMPAIGN ATTEMPT 1 (real runs, real tokens)
   1. Preconditions stated in the handoff before starting: porcelain
      empty, branch pushed, provider reachable (one cheap ping),
      set_hash of scripts/gauntlet_orders/ re-verified via
      load_order_set().
   2. ONE invocation over the full frozen set with the campaign
      evidence root OUTSIDE the repo (session scratch or the isolated
      data area — R-0176 discipline; run artifacts are NEVER
      committed). Set budget ceiling across the ten orders is ~3.1M
      tokens; per-order budgets are the orders' own. Provider
      flakiness during a run makes that run FAIL honestly (A9) — do
      not rerun inside the same attempt, do not edit orders.
   3. After the invocation: copy matrix.md + matrix.json (only these)
      into .agent/gauntlet/attempt-01/ and commit — failed gauntlets
      are KEPT; the attempt history is part of the proof. Record the
      evidence root path + per-run terminal facts in the handoff.
   4. Gate: the copied matrix.json parses and its runs_recorded == 10;
      canary python3 -m pytest tests/cli/test_golden_path.py -q ->
      exit 0. The flawless count is REPORTED, not gated.

  PHASE 5 — HANDBACK
   git status --porcelain empty. Rewrite .agent/handoff.md per
   docs/agents/handback_template.md (per-commit tables; raw gate
   outputs with exit codes; the campaign matrix summary table verbatim;
   sha256 proof for every applied reviewer text vs its
   .agent/authored/ file). Update last_block OUTCOME. Completion report
   ends: "F075 R2 complete — attempt 1 matrix recorded, awaiting
   review."

  --- BEGIN f075-r2-1 sha256=41e4bed4f054316f819f9ddb4f3716294c40a81b58731cd454c26231f77c3371 ---
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
  silent success. The harness adds no product code paths; product
  fixes found by the campaign go through normal orders (T003).

  ## Steps
  - R1 (SPLIT, LARGE): Open PR Gate (PR #178 merged) + claim + T001
    evaluator/matrix/dry-run proof + T002 the frozen ten-order set —
    PASS, see Verdicts.
  - R2 (SPLIT, LARGE, current): persist the R1 verdict + fix R-0178
    + T003a live runner (isolated data root per run, real-root hash
    before/after, injection driver, evidence in the recorded
    schema) + campaign attempt 1: the full gauntlet from ONE
    invocation, matrix recorded honestly — a result below 10/10 is
    campaign data, not a round failure.
  - R3+: campaign iterations — targeted fix orders + full reruns —
    until 10/10 stands from one invocation; then the integration
    gate per docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR — a
    human applies it, never the harness.

  ## Findings
  - R-0178 (product, Low) 2026-08-04, reviewer's R1 read:
    gauntlet_evidence._as_number promises "a malformed number is a
    load error, never a silent zero" but returns the default
    silently — a run.json with a non-numeric wall_seconds or tokens
    value renders as 0 in the matrix, understating cost in the very
    report a human reads before flipping defaults. Fix: a
    non-numeric wall_seconds/tokens value becomes a load_error
    (malformed evidence, run not flawless), so the docstring stands
    as written; one falsification test per field.
  - Next free ID: R-0179.

  ## Verdicts
  - R1: PASS (SPLIT, LARGE, 2026-08-04). Range 563b15b4..740ff133
    (13 commits, all tabled). Transport: all four authored files cmp
    0 against the reviewer's scratchpad originals; applied files
    hash-identical to their authored copies. Reviewer re-ran both
    slice gates (evaluator 63, orders 34), siblings 44, canary 42,
    docs 293 — all exit 0 — and independently reproduced BOTH golden
    matrices byte-exact via the CLI over the recorded set (exit 1,
    5/9 flawless, exactly as recorded). Frozen set verified: ten
    orders, two of each kind, all four injection classes exercised,
    distinct risks in prose; the era mapping covers all seven R-ids
    the operator named. No existing product module touched — the
    range adds new files only. Deviations 1–5 accepted (module
    split: the seam is real and both slice gates ran as ordered).
    R-0178 registered from the reviewer's own read. Worktree
    hygiene: primary checkout only, porcelain empty at verdict.
    LAST_REVIEWED_SHA = 740ff133.
  --- END f075-r2-1 ---

  --- BEGIN f075-r2-2 sha256=cb9730c910fb35dc04903767e0bf36a2e717950a2141a25a0799d6411c72cfb7 ---
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
  R2 (SPLIT, LARGE): persist the R1 PASS + fix R-0178 (non-numeric
  evidence numbers become load errors) + T003a live runner: per
  order an isolated data root, real-root hash before/after, --yes
  semantics under the order's budgets, evidence written in the
  recorded schema, deterministic injection driver for g06–g09 at
  existing seams — then campaign attempt 1: the full gauntlet from
  ONE invocation, matrix kept durably under .agent/gauntlet/ (run
  artifacts stay outside the repo). Below 10/10 is campaign data,
  not a round failure; a red TEST gate is a STOP.

  ## Next Steps
  - R3+: campaign iterations — targeted fix orders + full reruns —
    until 10/10 from one invocation; then the integration gate.
  - Closure per STATUS_closure_protocol.md incl. config diff + ADR.

  ## Risks
  - Injections need real seams; a missing seam is a STOP-and-report,
    never a product bypass added quietly.
  - Real runs spend real tokens (set budget ceiling ~3.1M); provider
    flakiness makes a run FAIL honestly (A9) — that is the gate
    working, not breaking.
  - Do-not-touch: the pass definition (ADR to change), config
    defaults by machine, order-set edits mid-campaign.
  --- END f075-r2-2 ---

  --- BEGIN f075-r2-3 sha256=3eddb2c46b02c350352df0e622cb1edd52a326405fe950fc602be4011620efcb ---
  FROM (exact line, occurs once in .agent/context.md):
  R1 T001+T002 (current) → R2+ T003 campaign + integration gate →
  TO (two lines):
  R1 done (PASS) → R2 T003a live runner + campaign attempt 1
  (current) → R3+ iterations → integration gate →
  --- END f075-r2-3 ---
