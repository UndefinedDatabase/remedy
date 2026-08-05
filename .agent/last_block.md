OUTCOME: done — F075 R12 complete. R11 PASS persisted; ADR-0001 + config diff prepared and NOT applied; integration gate run: branch exit 0, zero branch-only failures, six base-only ids attributed to R-0169.

You are the Remedy worker (Window 2) for feature F075 — MILESTONE GATE:
10 flawless self-runs, round R12 (SPLIT, LARGE): persist the R11 PASS
+ prepare the config diff + ADR + the INTEGRATION GATE. Save THIS
ENTIRE block verbatim to .agent/last_block.md AS ITS OWN FIRST COMMIT
(R-0198: the persist commit stays under the cap without it). You are
on feature/f075-self-run-gauntlet at 05a15669. STOP rule: every phase
ends with a verification; first red TEST gate -> STOP per AGENTS.md
If-Blocked — EXCEPT the integration gate itself, where a regression is
recorded and handed back as a normal repair finding, not continued
past. Commits < 500 lines; NEVER force-push (R-0195).

PHASE 0 — THE BLOCK (own commit)
 Commit 0: chore(f075): save the R12 block. Touches ONLY
 .agent/last_block.md. Push.

PHASE 1 — PERSIST THE R11 VERDICT (own commit)
 1. Save the three AUTHORED TEXT payloads below to
    .agent/authored/f075-r12-<n>.md (bytes between BEGIN/END
    markers, exclusive, incl. final newline; payload lines at
    column 0). Verify each sha256sum against its BEGIN-marker hash.
    Mismatch -> STOP, report raw sums, apply nothing.
 2. Apply f075-r12-1 -> .agent/live_review.md, f075-r12-2 ->
    .agent/plan.md, f075-r12-3 -> .agent/context.md — FULL
    replacements, byte-exact from the saved files.
 3. Commit 1: chore(f075): persist the R11 PASS — 10/10 stands;
    register R-0198/R-0199. Gate: python3 -m pytest
    tests/cli/test_golden_path.py -q -> exit 0. Push.

PHASE 2 — THE PREPARED CONFIG DIFF + ADR (own commits)
 T1_F075.md: "Passing emits a prepared-but-not-applied config diff
 + ADR template naming the evidence; a human applies it. The
 harness never edits config itself."
 1. Inspect the repo's ADR convention first (existing ADR files or
    docs structure; record the location decision in
    .agent/decisions.md).
 2. The ADR (proposed status, never accepted-by-machine): what the
    gate proved (attempt 03, 10/10, one invocation, evidence path
    .agent/gauntlet/attempt-03/ + the 0/10 and 3/10 history);
    the measured cycle usage per order (v4 budgets 3-8, recorded
    over-cap usage from the evidence); the proposal — raise
    CYCLE_SAFETY_CAP from 1 to the evidence-supported value (state
    it and justify it from the measured usage, e.g. the maximum
    the campaign actually needed with margin); what stays
    conservative (the shipped cycles.max_cycles config default —
    name your recommendation and its reason); the rollback (one
    constant). The experiment override stays for future gauntlets.
 3. The config diff: a ready-to-apply unified diff file beside the
    ADR (the CYCLE_SAFETY_CAP line + its comment naming this ADR).
    NOT applied: the working tree after this phase carries the
    diff FILE, not the change — assert CYCLE_SAFETY_CAP == 1 in a
    test that the ADR's application will consciously flip (mark it
    with the ADR's name so the human finds it).
 4. Gate: python3 -m pytest tests/orchestration/test_long_run_executor.py
    -q -> exit 0 (the cap still 1, the new pin green); if the ADR
    lands under docs/: python3 -m pytest tests/docs/ -q -> exit 0.
    Push.

PHASE 3 — THE INTEGRATION GATE (the round's verdict-carrier)
 Follow docs/agents/integration_gate.md EXACTLY: full suite
 (pytest -n auto) on the BASE and on the BRANCH, run logs OUTSIDE
 the repo during the runs (R-0176), raw tails copied to
 .agent/gate_f075_r12/ (as .txt, R-0169) and committed; comm lists
 both directions; per-id attribution for any base-only/branch-only
 failures with direct evidence; the dist-parity and worktree
 hygiene steps as written. A branch-only regression -> record it as
 the gate result and hand back (normal repair round next).
 Gate: branch full suite exit 0 AND 0 unattributed branch-only
 failures. Push.

PHASE 4 — HANDBACK
 git status --porcelain empty. Rewrite .agent/handoff.md per
 docs/agents/handback_template.md (per-commit tables; raw gate
 outputs incl. the full-suite counts base and branch; the ADR +
 diff paths; sha256 proof per applied reviewer text). Update
 last_block OUTCOME. Completion report ends:
 "F075 R12 complete — integration gate run, awaiting review."

--- BEGIN f075-r12-1 sha256=acc6fcfb1f9bee3ce396aab3536269df409e5d110dd48133ede61e84a1788be4 ---
# Live Review — F075 MILESTONE GATE: 10 flawless self-runs (Tier 1)

Branch: feature/f075-self-run-gauntlet
Scope: a gauntlet HARNESS — evaluator + matrix + a frozen order set
(v4: orders + sample-project template) — that earns autonomy with
data. THE BAR IS MET: attempt 03 = 10/10 flawless from ONE
invocation (evidence .agent/gauntlet/attempt-03/, history 0/10 ->
3/10 -> 10/10 all KEPT). Remaining: the prepared-but-not-applied
CYCLE_SAFETY_CAP config diff + ADR (T003's done condition), the
integration gate, then closure.

## Steps
- R1-R10 (SPLIT, LARGE): harness + set + eight reviewed product
  changes + attempts 01/02 — PASS x10 (history).
- R11 (SPLIT, LARGE): R-0196 (boundary retries the retryable) +
  R-0197 (compiler honors declared shape) built; both re-proofs
  green; ATTEMPT 03 = 10/10 FLAWLESS — PASS, see Verdicts.
- R12 (SPLIT, LARGE, current): persist R11 verdict + prepare the
  config diff + ADR (naming the attempt-03 evidence; NOT applied
  — a human applies it) + the INTEGRATION GATE per
  docs/agents/integration_gate.md (T003 complete when this round
  passes).
- R13: closure per docs/roadmap/STATUS_closure_protocol.md — its
  own round, never bundled.

## Findings
- R-0178..R-0194: all fixed and reviewer-verified; R-0181/R-0195
  resolved by ruling. Done: R-0178 · Done: R-0179 · Done: R-0180 ·
  Done: R-0182 · Done: R-0183 · Done: R-0184 · Done: R-0185 ·
  Done: R-0186 · Done: R-0187 · Done: R-0188 · Done: R-0189 ·
  Done: R-0190 · Done: R-0191 · Done: R-0192 · Done: R-0193 ·
  Done: R-0194 · R-0181 Resolved · R-0195 Resolved.
- R-0196 (product, High): boundary retry semantics. Built
  583bc2c9 — narrow frozen RETRYABLE set (provider_unavailable,
  io_failure), OUTCOME_ITERATION_RETRYING non-terminal ledger
  entries, per-milestone streak escalation; the injection reading
  distinguishes survived (green terminal WITH a post-mortem ->
  retry_within_budget) from swallowed (green with NOTHING ->
  silent_success), closed set untouched. Live-proven: g06/g08/g09
  all achieved with their faults ledgered and retried.
  Reviewer-verified in source, tests, and the campaign matrix.
  Done: R-0196
- R-0197 (product, Medium): compiler milestone cap. Built
  25d04521 — resolve_milestone_cap clamped to [1, cap-12], None
  is byte-identical today (pinned), prompt AND validator enforce,
  fallback intact; runner passes declared + 1. Live-proven: g02
  compiled 2 <= 1+1, achieved in 5 of 12 budgeted iterations.
  Done: R-0197
- R-0198 (process, Low) 2026-08-05: commit 4792dd02 is 1044 lines
  — over the cap, correctly DECLARED not rewritten (the R-0195
  rule working). Cause: the R11 block ordered four state files
  plus the verbatim last_block as ONE commit — a reviewer-order
  defect; the content is entirely reviewer-authored text.
  Resolved by ruling: it stands; from R12 on, blocks order the
  last_block save as its own commit when the persist commit
  approaches the cap. Resolved.
- R-0199 (harness perf, Medium) 2026-08-05, worker-observed: the
  attempt-03 campaign read ~872 GB while writing ~2 MB. Results
  unaffected, isolation held. Reviewer hypothesis, unverified:
  data_root_digest hashes EVERY file under the operator's real
  data root before and after every run (20+ full scans per
  campaign) — the cost scales with the operator's history, not
  the gauntlet's work. Needs its own measured diagnosis and fix
  order (e.g. a manifest-based digest or scoped root). NOT a
  flawless-criterion and NOT a closure blocker; registered as a
  CLOSURE CANDIDATE for .agent/candidates.md alongside the F070
  review gap and the absent resume verb.
- Next free ID: R-0200.

## Verdicts
- R1-R10: PASS x10. Full texts in this file's git history
  (55f706db, c95f23db, e5ca780e, 6a002f09, 9e8ced5b, df856730,
  1fe38c56, 5d068078, 43c9c9ca, 4792dd02).
- R11: PASS (SPLIT, LARGE, 2026-08-05) — AND THE 10/10 STANDS,
  subject only to the integration gate and the closure protocol.
  Range e4119c86..05a15669 (8 commits, all tabled). Transport:
  r11-1/2/3 cmp 0 against the reviewer's scratchpad originals
  (primary proof restored); live_review at the apply commit
  byte-equals the authored text. Reviewer re-ran every gate: P2
  340, compiler 113, remaining harness 423, canary 42 — all exit
  0, porcelain empty. R-0196/R-0197 verified in source and
  tests; the injection-reading change audited line by line —
  silent_success still fires when nothing was recorded; the
  closed set is untouched. The committed attempt-03 matrix
  audited in full: 9/9 criteria on 10/10 runs, zero failures,
  failure_kinds [], every terminal achieved, manifest order, the
  kind mix 2x5, md and json in agreement; preconditions recorded
  before the run (set v4 hash re-verified, preflight empty);
  attempts 01 and 02 KEPT beside it — the history of earning the
  bar is part of the proof. Both re-proofs quoted every required
  fact incl. the survived-fault ledger shape. NO force-push this
  round (R-0195 honoured); the oversize persist commit ruled in
  R-0198. R-0199 registered from the worker's own I/O
  observation. Worktree hygiene: primary only, porcelain empty.
  LAST_REVIEWED_SHA = 05a15669.
--- END f075-r12-1 ---

--- BEGIN f075-r12-2 sha256=11349415f7bead79ad1eae1974a97744156a8ae54e6cc7ee7ad0651d47ad1696 ---
# Plan — F075 MILESTONE GATE: 10 flawless self-runs

Branch: feature/f075-self-run-gauntlet

## Goal
Autonomy earned with data, not vibes — AND NOW EARNED: attempt 03
ran the ten frozen orders unattended, 10/10 flawless from ONE
invocation, all four injected harness failures survived and
ledgered, host untouched, zero refusals needed. DONE when the
prepared config diff + ADR name the evidence (human-applied,
never the harness) and the integration gate + closure protocol
confirm the branch. Attempt history 0/10 -> 3/10 -> 10/10 KEPT
under .agent/gauntlet/.

## Current Step
R12 (SPLIT, LARGE): persist R11 verdict + prepare the
CYCLE_SAFETY_CAP config diff + ADR — prepared, NOT applied,
naming the attempt-03 evidence and the measured cycle usage;
location and ADR convention inspected first, decisions recorded —
+ the INTEGRATION GATE per docs/agents/integration_gate.md (full
suite base vs branch, run logs outside the repo, raw tails into
.agent/gate_f075_r12/). T003 completes when this round passes.

## Next Steps
- R13: closure per STATUS_closure_protocol.md — evidence job,
  fresh review zip, STATUS [x], README sync, PR; closure
  candidates registered (F070 review gap; absent resume verb;
  R-0199 campaign I/O).

## Risks
- The ADR proposes; a human disposes — the diff must be
  applicable but NOT applied, and CI/tests must stay green
  WITHOUT it.
- The integration gate is the round's verdict-carrier: a
  regression there is a normal repair round, not a crisis.
- Do-not-touch: config defaults by machine, the pass definition,
  order/template edits; the oversize exemption stays spent; NEVER
  force-push (R-0195).
--- END f075-r12-2 ---

--- BEGIN f075-r12-3 sha256=5747f126cd06dc148b5c1b37960b7d37eeebad299ad1f69a0405bc46c1eeee5a ---
# Context — F075 MILESTONE GATE: 10 flawless self-runs

## Active Branch
feature/f075-self-run-gauntlet (from main after the Open PR Gate
merged PR #178, the F071 closure)

## Scope
Roadmap F075 (Tier 1, docs/roadmap/features/T1_F075.md): gauntlet
harness + evaluator + matrix + frozen order set v4 + live runner
+ injection driver + their tests; nine reviewed product changes
(R3-R11, see live_review). THE BAR IS MET: attempt 03 = 10/10
flawless from one invocation. This round: the prepared config
diff + ADR (NOT applied) and the integration gate; then closure.

## Constraints
- Round gate = scoped pytest command(s) authored in the step
  block; canary per handback:
  python3 -m pytest tests/cli/test_golden_path.py -q. Docs-round
  gate applies to any commit touching docs/roadmap/**:
  python3 -m pytest tests/docs/ -q. The INTEGRATION GATE runs the
  full suite per docs/agents/integration_gate.md (pytest -n auto;
  run logs OUTSIDE the repo during the run, copied to
  .agent/gate_f075_r12/ after; the resource-safety rules of
  tests/regression apply).
- Commits < 500 lines, NO oversize left (R-0181; R-0198 rules the
  persist-commit class); NEVER force-push (R-0195); authored
  texts applied byte-exact from .agent/authored/f075-r12-<n>.md
  after sha256 verification.
- No pytest test may take a production/provider path (R-0182).
- The config diff + ADR are PREPARED, never applied — config
  defaults by machine remain do-not-touch; the suite must be
  green without them.
- Gauntlet evidence: only matrix.md + matrix.json committed under
  .agent/gauntlet/ (attempts 01-03 KEPT).
- Do-not-touch: the pass definition, order/template edits.

## Steps
R1-R11 done (PASS x11; 10/10 stands) → R12 ADR/diff prep +
integration gate (current) → R13 closure.
--- END f075-r12-3 ---
