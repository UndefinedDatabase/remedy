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
- R12: PASS — INTEGRATION GATE PASS (SPLIT, LARGE, 2026-08-05).
  Range 05a15669..8bc1305a (7 commits, all tabled). Transport:
  r12-1/2/3 cmp 0 against the reviewer's scratchpad originals AND
  against the applied files; the r12-2 corruption (ONE blank line
  dropped in transport) was caught by the sha256 check BEFORE
  anything was applied, isolated, restored, and re-verified — the
  R-0148 mechanism doing exactly its job; the archived block was
  corrected too (ba266dab). ADR-0001 verified: status PROPOSED,
  the diff applies cleanly and is NOT applied (CYCLE_SAFETY_CAP
  still 1 at source line 165, pinned by the new test until a
  human applies the ADR); the honest evidence-limit note (per-run
  cycle consumption unrecoverable, argued from the proven
  ceiling) accepted. INTEGRATION GATE: reviewer re-ran the FULL
  SUITE at HEAD personally: 15805 passed / 19 skipped, exit 0 in
  150s — matching the worker's branch run; base run raw records
  audited (6 failed / 15377 passed); comm -13 EMPTY (0
  branch-only), comm -23 = 6 ids, all
  test_live_state.py::TestUIServerIntegration, attributed to the
  known mid-run-UI-rebuild class on per-id direct evidence
  (identical dist content hash, mtimes inside the base run,
  serial re-run 16/16 green, no F075 commit touching apps/ui) —
  .agent/gate_f075_r12/attribution.txt. Flake debt: 6 base-only,
  under the 10-id escalation threshold; the recurring rebuild
  class goes to closure candidates. Worktree hygiene: the base
  gate worktree removed, pruned, branch deleted, primary only;
  porcelain empty. Only this round carries the full-suite claim:
  FULL SUITE GREEN. T003 complete — 10/10 stands, the ADR + diff
  are prepared. GATE VERDICT: PASS.
  LAST_REVIEWED_SHA = 8bc1305a.
