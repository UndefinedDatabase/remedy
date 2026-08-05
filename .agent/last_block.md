OUTCOME: done — F075 R11 complete. R10 PASS persisted; R-0196 and R-0197 built; both re-proofs green; campaign attempt 03 = 10/10 FLAWLESS from one invocation.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
10 flawless self-runs, round R11 (SPLIT, LARGE): persist the R10 PASS
+ R-0196 (boundary retry semantics) + R-0197 (compiler milestone cap)
+ two re-proofs + campaign attempt 03. Save THIS ENTIRE block verbatim
to .agent/last_block.md first (update OUTCOME at handback). You are on
feature/f075-self-run-gauntlet at e4119c86. STOP rule: every phase
ends with a verification; first red TEST gate -> STOP per AGENTS.md
If-Blocked. Phase 4 has its own hard STOPs. Commits < 500 lines, NO
oversize left; NEVER force-push — an over-cap pushed commit is
declared and handed back (R-0195).

PHASE 1 — PERSIST THE R10 VERDICT (first commit)
 1. Save the three AUTHORED TEXT payloads below to
    .agent/authored/f075-r11-<n>.md (bytes between BEGIN/END
    markers, exclusive, incl. final newline; payload lines at
    column 0). Verify each sha256sum against its BEGIN-marker hash.
    Mismatch -> STOP, report raw sums, apply nothing.
 2. Apply f075-r11-1 -> .agent/live_review.md, f075-r11-2 ->
    .agent/plan.md, f075-r11-3 -> .agent/context.md — FULL
    replacements, byte-exact from the saved files.
 3. Commit 1: chore(f075): persist the R10 PASS, register
    R-0195..R-0197. Gate: python3 -m pytest
    tests/cli/test_golden_path.py -q -> exit 0. Push.

PHASE 2 — R-0196: THE BOUNDARY CONTINUES ON RETRYABLE CLASSES (own
 commits)
 1. orchestrator_loop, the except block at ~984: after
    record_iteration_failure classifies, branch on the class:
    - RETRYABLE (exactly provider_unavailable and io_failure —
      keep the set NARROW and named): ledger the iteration with a
      non-terminal failed outcome (a new OUTCOME_ constant, not a
      TERMINAL_), post-mortem written as today, and CONTINUE the
      loop — the next iteration re-attempts under the same
      budgets. Track a consecutive boundary-failure streak PER
      MILESTONE (the milestone the failed iteration was working);
      the SECOND consecutive caught failure on the same milestone
      escalates via hand_over (the R-0190 pattern; reset on any
      successful iteration or other milestone).
    - anything else (unknown included): TERMINAL_ITERATION_FAILED
      exactly as today.
 2. Tests (fakes, R-0182): a ConnectionError at iteration 1 ->
    mission continues, retries, achieves; the post-mortem and the
    ledgered failed iteration both present; an OSError mid-write
    (update_dossier) -> same; two consecutive caught failures on
    one milestone -> escalated with both in the detail; an
    unknown-class raise -> terminates as today;
    KeyboardInterrupt/SystemExit still propagate; the injection
    drivers' dispositions settle correctly against the new
    behavior (g06/g08/g09 shape: injected once -> retried ->
    achieved -> disposition retry_within_budget or ledgered
    per the closed set — adjust gauntlet_injection.settle ONLY if
    its reading of the facts needs the new outcome, never the
    closed set itself).
 3. Gate (STOP if red): python3 -m pytest
    tests/orchestration/test_orchestrator_loop.py
    tests/orchestration/test_mission_e2e.py
    tests/orchestration/test_era_integrity.py
    tests/orchestration/test_gauntlet_injection.py
    tests/orchestration/test_gauntlet_runner.py -q -> exit 0. Push.

PHASE 3 — R-0197: THE COMPILER HONORS DECLARED SHAPE (own commit)
 1. compile_mission_plan (mission_compiler): optional
    max_milestones: int | None = None — None is byte-for-byte
    today's behavior; a value caps the compiled plan (prompt
    carries the cap AND the validator refuses an over-cap draft
    with the one retry, then the deterministic fallback applies
    unchanged; the F069 cap-12 stays the outer bound). The
    gauntlet runner passes len(order.milestones) + 1.
 2. Tests (fakes, R-0182): None -> unchanged (existing suite
    green); cap honored on a compliant draft; over-cap draft
    refused then retried then fallback; runner passes the
    order-derived cap (pinned).
 3. Gate (STOP if red): python3 -m pytest
    tests/orchestration/test_mission_compiler.py
    tests/orchestration/test_gauntlet_runner.py -q -> exit 0. Push.

PHASE 4 — TWO RE-PROOFS (hard-gated, in this order)
 1. python3 scripts/self_run_gauntlet.py --live <fresh root OUTSIDE
    the repo> --only 6 --format json
    REQUIRED: terminal achieved, released verdict, zero open
    decisions, the injection settled as retry_within_budget or
    ledgered_failure (NOT never_fired, NOT silent_success), the
    post-mortem classified provider_unavailable. Quote the
    injection block + the ledger's failed-then-retried iterations.
 2. python3 scripts/self_run_gauntlet.py --live <fresh root OUTSIDE
    the repo> --only 2 --format json
    REQUIRED: terminal achieved within g02's v4 budget; quote the
    compiled milestone count (must be <= declared + 1) and the
    iteration count.
 3. Either re-proof missing anything -> STOP: commit nothing
    further, record the full evidence trail in
    .agent/decisions.md, hand back (the R4-R10 STOP precedent).

PHASE 5 — CAMPAIGN ATTEMPT 03 (only after BOTH re-proofs green)
 1. Preconditions in the handoff: porcelain empty, pushed,
    provider reachable, set_hash (v4) re-verified,
    preflight_injections -> [].
 2. ONE invocation, full ten: --live <fresh root OUTSIDE the repo>
    --format both. No rerun inside the attempt, no order or
    template edits; provider flakiness fails a run honestly (A9).
 3. Copy matrix.md + matrix.json into .agent/gauntlet/attempt-03/
    and commit, SLICED under the cap (md and json in separate
    commits like attempt-02). Evidence-root path + per-run
    terminals in the handoff.
 4. Gate: committed matrix.json parses, runs_recorded == 10;
    canary python3 -m pytest tests/cli/test_golden_path.py -q ->
    exit 0. The flawless count is REPORTED, not gated.

PHASE 6 — HANDBACK
 git status --porcelain empty. Rewrite .agent/handoff.md per
 docs/agents/handback_template.md (per-commit tables; raw gate
 outputs; both re-proof quotes; if Phase 5 ran, its summary table
 verbatim; sha256 proof per applied reviewer text). Update
 last_block OUTCOME. Completion report ends:
 "F075 R11 complete — awaiting review." (append "attempt 03 matrix
 recorded" if Phase 5 ran).

--- BEGIN f075-r11-1 sha256=f5663147d737e6457c00dd051fe20be26fdb1df8ebc98a836826a2572a450bc7 ---
# Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

Branch: feature/f075-self-run-gauntlet
Scope: a gauntlet HARNESS — evaluator + matrix + a frozen order set
(v4: orders + sample-project template) — that earns autonomy with
data. Flawless per run = start command only + terminal green +
blocking DoD green + zero unknown postmortems + zero open
decisions + host data root byte-untouched. Product changes ride
along ONLY as reviewed SPLIT work: exception boundary (R3),
transport classes (R4), execution wiring (R5), cycles vehicle +
production DoD path (R6), sample-project world + escalation (R7),
released-gate guard (R8), attribution fix (R9), context directive
(R10), boundary retry semantics + compiler milestone discipline
(R11).

## Steps
- R1-R9 (SPLIT, LARGE): harness + set + boundary + injections +
  attempts + the guard triad + attribution — PASS x9 (history).
- R10 (SPLIT, LARGE): R-0193 (context directive, DIRECT declare)
  + R-0194 (v4 budgets) built; re-proof = the feature's FIRST
  flawless run; campaign attempt 02 = 3/10 (g01, g05, g07) with
  two blocking findings — PASS, see Verdicts.
- R11 (SPLIT, LARGE, current): persist R10 verdict + R-0196 (the
  boundary CONTINUES on a retryable failure class instead of
  ending the mission) + R-0197 (the compiler respects the order's
  declared milestone shape as a cap) + re-proofs (--only 6 and
  --only 2 must both reach achieved) + campaign attempt 03 from
  ONE invocation.
- R12+: campaign iterations until 10/10 from one invocation; then
  the integration gate per docs/agents/integration_gate.md.
- Closure per docs/roadmap/STATUS_closure_protocol.md; a passing
  10/10 emits a prepared-but-not-applied config diff + ADR (the
  CYCLE_SAFETY_CAP / default raise — human-applied).

## Findings
- R-0178..R-0192: all fixed and reviewer-verified; R-0181
  resolved by ruling (exemption SPENT). Done: R-0178 ·
  Done: R-0179 · Done: R-0180 · Done: R-0182 · Done: R-0183 ·
  Done: R-0184 · Done: R-0185 · Done: R-0186 · Done: R-0187 ·
  Done: R-0188 · Done: R-0189 · Done: R-0190 · Done: R-0191 ·
  Done: R-0192 · R-0181 Resolved.
- R-0193 (product, Medium): context directive. Built 89269098,
  live-proven: the R10 re-proof achieved with ZERO refusals, two
  iterations per milestone over four milestones — exactly as
  specified. Done: R-0193
- R-0194 (campaign, Medium): v4 budgets from measured economics.
  Built 5001cc32, budgets + budget_rationale only, verified in
  the diff. Necessary and not sufficient (see R-0197).
  Done: R-0194
- R-0195 (process, Medium) 2026-08-04: the worker force-pushed
  ONCE (--force-with-lease) to re-split an 866-line commit into
  three under the cap before review. Honestly declared, content
  preserved (reviewer re-verified the split commits), motive was
  cap compliance — but force push is the hard-STOP destructive
  class (planner_reviewer_prompt.md §2(3)); a worker never
  rewrites pushed history unilaterally, lease or not. Resolved by
  ruling: this instance stands (no loss, declared, verified); the
  rule from here: an over-cap commit already pushed is DECLARED
  and handed back — the reviewer orders the remedy. Resolved.
- R-0196 (product, High) 2026-08-04, attempt 02 Finding B: the R3
  exception boundary classifies, ledgers, and TERMINATES — so
  g06/g08/g09's injected transient faults end their missions at
  iteration 1 with zero milestones; dod_blocking_green fails as
  an absence and those orders cannot be flawless by construction,
  while g06's own rationale demands "ledgered and retried within
  budget". Counter-example: g07's truncation is handled BELOW the
  boundary and that run achieved, flawless. Fix (DECISION below):
  the boundary distinguishes RETRYABLE classes
  (provider_unavailable, io_failure — transient transport/machine)
  from fatal ones: retryable -> classify + post-mortem + ledger
  the iteration + CONTINUE the loop (the next iteration
  re-attempts under the same budgets); a SECOND consecutive
  boundary-caught failure on the SAME milestone escalates
  (mirroring the R-0190 streak); unknown/fatal classes ->
  terminal iteration_failed exactly as today.
- R-0197 (product, Medium) 2026-08-04, attempt 02 Finding A: plan
  expansion is erratic — the same frozen order compiled to 3, 4,
  and >=7 milestones across runs; every iteration_limit run
  finished six milestones economically and ran out mid-plan; no
  static budget can fit a nondeterministic shape. Fix (DECISION
  below): compile_mission_plan gains an optional max_milestones
  cap (None = today's behavior, cap 12 unchanged); the gauntlet
  runner passes the ORDER's declared shape + 1 headroom; the
  compiler's DAG validation and deterministic fallback are
  untouched. The F016 granularity spirit applied to milestones.
- Deferred closure candidates: F070 review gap; absent resume
  verb.
- Next free ID: R-0198.

## Verdicts
- R1-R9: PASS x9. Full texts in this file's git history
  (55f706db, c95f23db, e5ca780e, 6a002f09, 9e8ced5b, df856730,
  1fe38c56, 5d068078, 43c9c9ca).
- R10: PASS (SPLIT, LARGE, 2026-08-05). Range ae4c6e9a..e4119c86
  (8 commits, all tabled; the force-with-lease re-split ruled in
  R-0195). Transport: DIGEST FALLBACK per
  planner_reviewer_prompt.md §4.9 — the reviewer's scratchpad
  originals were pruned by session tmp death, so the proof is the
  committed .agent/authored/f075-r10-{1,2,3}.md files' recomputed
  sha256 equaling the BEGIN digests in the reviewer's own emitted
  block (all three equal), plus live_review at the apply commit
  byte-equal to the authored file — stated so the evidence chain
  stays honest. Reviewer re-ran every gate: loop/e2e/era 249,
  orders/runner 86, seven harness files 380, canary 42 — all exit
  0, porcelain empty. R-0193 verified in the diff and live (zero
  refusals, 2 iterations/milestone); v4 verified budgets-only in
  the real diff (g01: 6->12 iterations with rationale). Campaign
  attempt 02 audited from the committed matrix: internally
  consistent, 3/10 flawless — the feature's FIRST — criteria
  counts matching the handoff digit for digit; all four
  injections degraded; no_unknown_postmortems 10/10 (R-0185
  proven at campaign scale). Findings A and B verified: the
  terminating boundary read in source (orchestrator_loop.py
  984-993), the expansion variance read from the committed
  evidence. R-0195/R-0196/R-0197 registered. DECISIONS 2026-08-05
  (§4.7), reversal = any later relay: (R-0196) retryable classes
  continue + streak-escalate — alternatives rejected: harness
  retries (grades the crutch, R2 rule), softening the pass
  definition (forbidden by the feature file). (R-0197) the
  compiler honors the order's declared shape as a cap —
  alternatives rejected: plan-relative budgets (rewards
  over-expansion with more spend), a v5 budget re-guess (Finding
  A proves no static number fits an erratic shape). Worktree
  hygiene: primary only, porcelain empty.
  LAST_REVIEWED_SHA = e4119c86.
--- END f075-r11-1 ---

--- BEGIN f075-r11-2 sha256=a13ff18b3342ad5f20f7fd5f12ccf389a59287198c3d6c4978986e9031fb69de ---
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
R11 (SPLIT, LARGE): persist R10 PASS + R-0196 — the boundary
continues on retryable classes (provider_unavailable, io_failure):
classify + post-mortem + ledger + CONTINUE; second consecutive
caught failure on the same milestone escalates (R-0190 streak
pattern); unknown/fatal terminates as today — + R-0197 —
compile_mission_plan gains an optional max_milestones cap; the
runner passes the order's declared shape + 1 — + re-proofs
(--only 6: achieved with the injection ledgered and retried;
--only 2: achieved within the v4 budget; both hard STOPs) +
campaign attempt 03 (full ten, ONE invocation, matrix to
.agent/gauntlet/attempt-03/, sliced commits).

## Next Steps
- R12+: campaign iterations until 10/10 from one invocation; then
  the integration gate.
- Closure per STATUS_closure_protocol.md incl. the
  CYCLE_SAFETY_CAP config diff + ADR and the closure candidates.

## Risks
- The boundary change touches the loop's core a second time —
  retryable set kept NARROW (the two named classes), streak
  escalation bounds repetition, full loop/e2e/era suites must
  stay green.
- The compiler cap must not break the deterministic fallback or
  the DAG discipline; None keeps today's behavior for every
  non-gauntlet caller.
- Real runs spend real tokens; provider flakiness fails a run
  honestly (A9).
- Do-not-touch: config defaults by machine, the pass definition,
  order/template edits mid-campaign; the oversize exemption stays
  spent; NEVER force-push (R-0195).
--- END f075-r11-2 ---

--- BEGIN f075-r11-3 sha256=fcdb32ee3fa4b042aac05a3cea597412255b6eae28306c97c971ef7b7887b855 ---
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
production DoD path (R6), sample-project world + escalation (R7),
released-gate guard (R8), attribution fix (R9), context directive
(R10), R-0196 boundary retry semantics + R-0197 compiler
milestone cap (R11, DECISIONS in the R10 verdict).

## Constraints
- Round gate = scoped pytest command(s) authored in the step
  block; canary per handback:
  python3 -m pytest tests/cli/test_golden_path.py -q. Docs-round
  gate applies to any commit touching docs/roadmap/**:
  python3 -m pytest tests/docs/ -q. Full-suite pytest -n auto only
  at the integration gate; the resource-safety rules of
  tests/regression apply.
- Commits < 500 lines, NO oversize left (R-0181 spent it); NEVER
  force-push — an over-cap pushed commit is declared and handed
  back (R-0195); authored texts applied byte-exact from
  .agent/authored/f075-r11-<n>.md after sha256 verification.
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
R1-R10 done (PASS x10) → R11 R-0196 + R-0197 + re-proofs +
attempt 03 (current) → R12+ iterations → integration gate →
closure.
--- END f075-r11-3 ---
