OUTCOME: executed — F075 R1 complete: PR #178 merged, claim + T001 (evaluator, matrix, recorded fixtures, golden, CLI) + T002 (frozen ten, set version 1) landed; both slice gates exit 0; canary exit 0; no PR (comes at closure).

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
  10 flawless self-runs, round R1 (SPLIT, LARGE bundle): Open PR Gate +
  claim + T001 + T002. Save THIS ENTIRE block verbatim to
  .agent/last_block.md first (update OUTCOME at handback). LARGE rule:
  every slice ends with its own verification; at the FIRST red gate STOP
  per AGENTS.md If-Blocked — record the raw failure in the handoff, do
  NOT continue into the next slice. Read docs/roadmap/features/T1_F075.md
  COMPLETELY before Phase 2 — it is the specification of record for this
  round; where this block is silent, the feature file governs.

  PHASE 0 — OPEN PR GATE + BRANCH
   1. gh pr list --state open --json number,headRefName,baseRefName,isDraft
      Expected: exactly one — #178, feature/f071-mission-dossier -> main,
      not draft. Then: gh pr merge 178 --merge --delete-branch.
      Anything else (multiple PRs, draft, different head) -> STOP, report.
   2. git status (clean) · git checkout main · git pull ·
      git checkout -b feature/f075-self-run-gauntlet

  PHASE 1 — CLAIM (first commit)
   1. Save the four AUTHORED TEXT payloads below to
      .agent/authored/f075-r1-<n>.md (bytes between BEGIN/END markers,
      exclusive, incl. the final newline; payload lines start at column
      0). Verify each sha256sum against its BEGIN-marker hash. Mismatch
      -> STOP, report raw sums, apply nothing.
   2. Apply f075-r1-1 -> docs/roadmap/STATUS.md (FROM line occurs once;
      replace once; copy from the SAVED file, never retype).
   3. Apply f075-r1-2 -> .agent/live_review.md, f075-r1-3 ->
      .agent/plan.md, f075-r1-4 -> .agent/context.md — each a FULL file
      replacement, byte-exact copy of the saved authored file.
   4. Commit 1: chore(f075): claim F075 — STATUS [~] + state reset.
      Gates (docs/roadmap touched): python3 -m pytest tests/docs/ -q AND
      python3 -m pytest tests/cli/test_golden_path.py -q -> both exit 0.
      Push (git push -u origin feature/f075-self-run-gauntlet).

  PHASE 2 — T001: EVALUATOR + MATRIX + DRY-RUN PROOF
   Zero provider calls in this round — the evaluator is proven against
   RECORDED fixture evidence before any real run (T1_F075.md, T001).
   1. Evaluator logic in an importable module (suggested:
      packages/orchestration/gauntlet_evaluator.py) + thin CLI
      scripts/self_run_gauntlet.py with at least: --dry-run
      <evidence-dir> (evaluate recorded evidence, no execution) and
      --only <n>. Record interface decisions (module name, evidence
      layout consumed, order-file schema) in .agent/decisions.md.
   2. Pass definition, explicit and falsifiable — flawless per run =
      start command only (zero operator interventions) + terminal green
      + all blocking DoD checks green + zero unknown postmortems + zero
      open decisions + host data root byte-untouched (before/after
      content hash). Failure classification MUST be able to name the
      F070 era-fixture classes (R-0141/R-0143/R-0144/R-0145/R-0146/
      R-0147/R-0148 — see T1_F070.md, Design) and the harness-failure
      injection classes (provider API error mid-move, truncated model
      response, harness death mid-dispatch, harness death mid-write);
      each injection degrades to a LEDGERED failure, retry within
      budget, or escalation (F051 semantics) — never a silent success,
      never a corrupted artifact accepted downstream.
   3. Matrix report (markdown + json), deterministic bytes for a given
      evidence set; per run: terminal status, DoD matrix, postmortem
      classes, operator interventions, wall/tokens, links into the
      run's evidence. During real runs (T003, later) all run artifacts
      live in the ISOLATED data root, never inside the repo working
      tree (docs/agents/integration_gate.md, R-0176).
   4. Recorded fixture evidence under the tests fixture area covering
      at minimum: one flawless run; one run with an operator command ->
      NOT flawless; one run with an unknown postmortem -> NOT flawless;
      one fixture per harness-failure injection class (ledgered ->
      still eligible; silent success or corrupted-artifact-accepted ->
      NOT flawless); era-fixture classes covered at least via
      classification-mapping tests. Golden matrix (md + json) for the
      recorded set.
   5. Tests: tests/orchestration/test_gauntlet_evaluator.py — every
      pass criterion has a test that flips it and asserts not-flawless
      (falsifiability is the acceptance bar); golden-matrix comparison.
      Multiple small commits expected, each < 500 lines.
   6. SLICE GATE (STOP here if red):
      python3 -m pytest tests/orchestration/test_gauntlet_evaluator.py -q
      -> exit 0. Push.

  PHASE 3 — T002: THE CURATED TEN-ORDER SET
   1. Ten mission-order fixture files, each with a rationale comment
      (why this order probes a DIFFERENT risk) and a fixed budget;
      mixed kinds per T1_F075.md: pure-code change, test-add, small app
      feature with smoke, doc generation, a two-milestone mission.
      Location chosen by you (suggested: scripts/gauntlet_orders/ or
      the tests fixture area) — record it in .agent/decisions.md.
   2. Frozen + versioned: a set manifest (set version 1, per-order
      sha256, set hash). Order-set edits mid-campaign are forbidden;
      any change resets the gauntlet count (T1_F075.md, A9).
   3. Tests pin the frozen set: exactly 10 orders, unique ids, budget
      present on every order, manifest hashes match the files, the
      kind mix is present.
   4. SLICE GATE (STOP here if red): scoped pytest over the order-set
      tests (same file or tests/orchestration/test_gauntlet_orders.py)
      -> exit 0. Push.

  PHASE 4 — HANDBACK
   Canary: python3 -m pytest tests/cli/test_golden_path.py -q -> exit 0.
   git status --porcelain empty. Rewrite .agent/handoff.md per
   docs/agents/handback_template.md (per-commit changed-files tables;
   raw gate outputs with exit codes; PR #178 merge result recorded;
   sha256 proof that every applied reviewer text is byte-identical to
   its .agent/authored/ file). Update last_block OUTCOME. Completion
   report ends: "F075 R1 complete — awaiting review."

  --- BEGIN f075-r1-1 sha256=be68f1e9abc044da3c429aa03c0677ef158a27847e73fc59a5977fad73e05ea5 ---
  FROM:
  - [ ] F075 — MILESTONE GATE: 10 flawless self-runs

  TO:
  - [~] F075 — MILESTONE GATE: 10 flawless self-runs
  --- END f075-r1-1 ---

  --- BEGIN f075-r1-2 sha256=28246a1eb247df34ca454aa8d2b41602de909bcdec77293294f7416b1c63532d ---
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
  - R1 (SPLIT, LARGE bundle, current): Open PR Gate (merge PR #178,
    the F071 closure) + claim + T001 evaluator/matrix/dry-run mode
    proven against recorded fixture evidence + T002 the curated
    ten-order set with rationale + budgets, frozen and versioned.
  - R2+: T003 campaign — run, read the matrix, file targeted fix
    orders with failing evidence attached, rerun; multiple rounds
    EXPECTED. Then the integration gate per
    docs/agents/integration_gate.md.
  - Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
    10/10 emits a prepared-but-not-applied config diff + ADR — a
    human applies it, never the harness.

  ## Findings
  (none yet — F071's R-0176/R-0177 Done at F071 closure)
  - Next free ID: R-0178.

  ## Verdicts
  (pending R1)
  --- END f075-r1-2 ---

  --- BEGIN f075-r1-3 sha256=32729c7409dba63aded5b07cce4b00a39b4e5274e0cce106846d6b7773b51aeb ---
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
  R1 (SPLIT, LARGE bundle): Open PR Gate (PR #178) + claim + T001
  evaluator + matrix + dry-run fixture proof + T002 the ten curated
  orders with rationale + budgets, frozen and versioned. Gate:
  scoped evaluator/order-set tests + docs suite + canary.

  ## Next Steps
  - R2+: T003 campaign (run → targeted fix orders → rerun) +
    integration gate per docs/agents/integration_gate.md.
  - Closure per STATUS_closure_protocol.md incl. config diff + ADR.

  ## Risks
  - Every pass criterion must be demonstrably falsifiable — a
    fixture proves each one can fail (one operator command → not
    flawless; one unknown postmortem → not flawless).
  - Do-not-touch: the pass definition once frozen (ADR to change),
    config defaults by machine, order-set edits mid-campaign.
  - Host-state isolation: every run and every verify step against an
    isolated data root; ANY pollution disqualifies (F081 lesson
    2026-07-23).
  --- END f075-r1-3 ---

  --- BEGIN f075-r1-4 sha256=26b3de432a11307f7df927e8a434f50f29d295b96419eb786c305890adc8b812 ---
  # Context — F075 MILESTONE GATE: 10 flawless self-runs

  ## Active Branch
  feature/f075-self-run-gauntlet (from main after the Open PR Gate
  merged PR #178, the F071 closure)

  ## Scope
  Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
  harness + evaluator + matrix report + frozen ten-order set + their
  tests. The harness adds no product code paths; product fixes found
  by the campaign go through normal orders with their own tests.

  ## Constraints
  - Round gate = scoped pytest command(s) authored in the step
    block; canary per handback:
    python3 -m pytest tests/cli/test_golden_path.py -q. Docs-round
    gate applies to any commit touching docs/roadmap/**:
    python3 -m pytest tests/docs/ -q. Full-suite pytest -n auto only
    at the integration gate; the resource-safety rules of
    tests/regression apply.
  - Commits < 500 lines; authored texts applied byte-exact from
    .agent/authored/f075-r1-<n>.md after sha256 verification.
  - Gauntlet runs use an ISOLATED data root, never the operator's
    real one; gate run logs live outside the repo during a run
    (docs/agents/integration_gate.md, R-0176).
  - Do-not-touch: the pass definition once frozen, config defaults
    by machine, order-set edits mid-campaign.

  ## Steps
  R1 T001+T002 (current) → R2+ T003 campaign + integration gate →
  closure.
  --- END f075-r1-4 ---
