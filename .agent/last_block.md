You are the worker for F079 R3 (SPLIT round): the INTEGRATION GATE.
R2 verdict: PASS — T001–T003 are built and verified. Reviewer issues
the gate verdict; you execute and record. Authority: AGENTS.md. If any
step goes red in a way integration_gate.md does not itself handle:
STOP per AGENTS.md If-Blocked and hand back with the raw output.

── STEP gate/1 — F079 ───────────────────────────────────────
Goal:        Persist the R2 verdict, then run the integration gate
             exactly per docs/agents/integration_gate.md.
Bundle:      1 state commits · 2 integration gate · 3 handback
Change:      .agent/** only (state files + gate evidence). NO source
             or test edits this round — a regression found here is
             its own reviewer-gated repair round.
Constraints: Primary checkout porcelain-empty at every point after
             commits; the base run happens in the disposable worktree
             integration_gate.md prescribes, removed and pruned
             before handback. Commits < 500 lines each; the
             last_block save rides alone (R-0198 rule).
Done when:   Both suite runs recorded raw, every differing id
             attributed per integration_gate.md, evidence under
             .agent/gate_f079_r3/.
Handback:    Completion report + rewrite .agent/handoff.md (see 3).
──────────────────────────────────────────────────────────────

1. STATE COMMITS (persist FIRST)
   Two authored texts follow at the bottom, delimited by BEGIN/END
   markers. Authored bytes = everything BETWEEN the marker lines,
   including the final newline; markers are never content.
   a. COMMIT A: this entire prompt saved verbatim to
      .agent/last_block.md (own commit).
   b. Save to .agent/authored/f079-r3-1.md and
      .agent/authored/f079-r3-2.md; verify each with sha256sum
      against its BEGIN-marker hash. Mismatch → STOP, hand back
      naming block and both hashes; apply nothing.
      COMMIT B: the two authored files.
   c. Apply: f079-r3-1 replaces .agent/live_review.md entirely;
      f079-r3-2 replaces .agent/plan.md entirely. COMMIT C: exactly
      these two files, message
      "chore(f079): persist R2 PASS verdict (R-0199, R-0203 done) +
      gate plan".

2. INTEGRATION GATE — follow docs/agents/integration_gate.md EXACTLY
   Parameters for this gate:
   - Branch HEAD: the tip after your state commits.
   - Merge base: `git merge-base main HEAD` (main is at the PR #180
     merge, 38854f60).
   - Evidence directory: .agent/gate_f079_r3/ (raw stdout+stderr of
     BOTH runs, the id lists, comm outputs, attribution.txt with one
     line per differing id and its direct evidence).
   - Full runs use `pytest -n auto` per the gate doc; record wall
     clock for both runs.
   - Step 3 of the gate doc is MANDATORY here: the R-0202 class
     (mid-run UI rebuild despite REMEDY_UI_NO_AUTO_BUILD=1) recurred
     in the F075 R12 base gate — hash apps/ui/dist before and after
     the base run and record both hashes; a changed hash voids the
     parity claim and forces per-id attribution.
   - A reproducible branch-only failure coupled to feature code is a
     BLOCKER: STOP, hand back — the fix is its own round (the gate
     doc's step 4 rule).
   Commit the evidence directory when complete (one commit; split
   only if a raw log pushes it past 500 lines — logs may be split
   from attribution).

3. HANDBACK
   Canary: python3 -m pytest tests/cli/test_golden_path.py -q →
   exit 0. git worktree list → primary only (base worktree removed
   and pruned, per the gate doc). git status --porcelain → empty.
   Push the branch. Rewrite .agent/handoff.md (last commit) with:
   - changed-files table per commit,
   - raw transcripts: both full-suite runs (command, exit code,
     tail with counts and wall clock), the canary, the hygiene
     proofs,
   - the dist-hash pair from step 3 of the gate doc,
   - the comm results and EVERY differing id with its attribution
     line,
   - item status. NO verdict — the reviewer issues the gate verdict.

AUTHORED TEXTS

<<<BEGIN AUTHORED f079-r3-1
sha256=80c9b272e89c82f3bcafff959b968bb27edcdef1441102e27dbc44b1aa4e0488>>>
# Live Review — F079 Context handoffs (Tier 1)

Branch: feature/f079-context-handoffs
Scope: handoff artifact (handoff.json + rendered handoff.md) composed
from dossier, checkpoint reference, open decisions and next intent;
triggers + loop consumption; measured recall eval. T001–T003 are all
built and reviewer-verified; the F075 candidate sweep landed in R1.

## Steps
- R1 (SPLIT, LARGE): Open PR Gate (#180) + STATUS claim + candidate
  sweep + R-0199 measured diagnosis + reuse inspection + T001 —
  PASS, see Verdicts.
- R2 (SPLIT, LARGE): R-0199 fix (metadata-manifest digest) + T002
  (triggers + loop consumption + reference verification) + T003
  (boundary recall eval + threshold) — PASS, see Verdicts.
- R3 (SPLIT, current): the INTEGRATION GATE per
  docs/agents/integration_gate.md. Awaiting handback.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md — its own
  round, never bundled.

## Findings
- R-0199 (harness perf, Medium — carried from F075): FIXED in R2,
  commit e249ea15 — data_root_digest hashes the sorted metadata
  manifest (relpath, size, mtime_ns), value prefixed meta-sha256: so
  old and new definitions can never compare equal; per-run frequency
  and evidence field names unchanged; the only semantic consumer
  (gauntlet_evaluator._check_data_root) compares within-run equality
  and is unaffected. Measured proof: one call 34.611 s against the
  394.8 s content-hash baseline (11.4x), content bytes read per call
  ~143.66 GB -> ~0. Reviewer verified the diff, the consumer audit
  and the honest-contract docstring. Done: R-0199
- R-0200 (process/gate-tooling, Medium): F070 verb-called gate half.
  Deferred, OPEN — rolls to candidates at closure if unbuilt.
- R-0201 (roadmap routing): resolved by routing in R1 — scope note in
  docs/roadmap/features/T3_F106.md. Resolved.
- R-0202 (gate tooling, Low): mid-run UI rebuild env-var class.
  Deferred, OPEN — rolls to candidates at closure if unbuilt.
- R-0203 (design, Low): root discipline at the consumption seam.
  FIXED in R2 — documented in handoff.py ("ROOT DISCIPLINE") and made
  visible by handoff_root_conflict (named, tested, R-0203 cited in
  the message). Done: R-0203
- Next free ID: R-0204.

## Verdicts
- R1: PASS (SPLIT, LARGE, 2026-08-06). Range 38854f60..79621fc0.
  Full text in this file's git history (commit b3a0291e).
  LAST_REVIEWED_SHA was 79621fc0.
- R2: PASS (SPLIT, LARGE, 2026-08-06). Range 79621fc0..0938884f
  (10 commits, all tabled). Transport: f079-r2-1/2 cmp 0 against the
  reviewer's scratchpad originals (primary proof); both applied state
  files byte-equal their authored texts. Reviewer re-ran every gate
  personally: handoff+gauntlet_runner 84, evaluator+evidence+
  self_run 125, mission_cmd+resume 106, orchestrator_loop 192,
  canary 42, tests/docs 293 — all exit 0; porcelain empty;
  `git worktree list` = primary only. Full diff read bottom-up:
  the R-0199 fix verified in source with its consumer audit; the
  T002 loop seams verified (limit and stop terminals return through
  build_boundary_handoff; a build failure lands in handoff_error and
  the terminal is never masked — pinned by test; the seed reaches
  iteration one's context only — pinned by a prompt-recording test);
  schema refusal and stale-head refusal assert the checkpoint
  feature's own sentence verbatim via worktree_drift_message; the
  T003 eval reuses run_recall_harness, RECALL_FIXTURE_FACTS and
  recall_report verbatim, inherits the dossier's documented
  threshold (100 % of OPEN items), is falsifiable (a lost open fact
  fails it), and archives the report beside the handoffs it
  measures. DECLARED scope deviation (checkpoints.py + job.py: the
  drift wording extracted to one source) ACCEPTED by ruling — the
  order's own single-wording constraint required it, the wording is
  byte-identical, both resume test files green; not a silent scope
  change. The 504-line last_block commit rides alone per the R-0198
  rule. Verification tier: round gates + canary + docs gate.
  LAST_REVIEWED_SHA = 0938884f.
<<<END AUTHORED f079-r3-1>>>

<<<BEGIN AUTHORED f079-r3-2
sha256=5d1be7e33ca3685c32713732d62ecc80f3eb12842159a7ce7de7b9e867841c6f>>>
# Plan — F079 Context handoffs

Branch: feature/f079-context-handoffs

## Goal
Session and context-window boundaries stop losing knowledge — DONE in
substance: T001 composer (idempotent, pure), T002 triggers + loop
consumption + reference verification, T003 measured boundary recall
(100 % open-item threshold met, report archived). R-0199 fixed
(metadata-manifest digest, 11.4x). Spec: docs/roadmap/features/
T1_F079.md. What remains is proving the whole, then closing.

## Current Step
R3: the integration gate per docs/agents/integration_gate.md — full
suite at HEAD and at the merge base, per-id attribution of every
difference, evidence under .agent/gate_f079_r3/. The reviewer issues
the gate verdict.

## Next Steps
- R4: closure per docs/roadmap/STATUS_closure_protocol.md (own
  round): evidence job + fresh review zip + authored STATUS [x] line
  + PR. R-0200/R-0202 roll back to .agent/candidates.md if unbuilt.

## Risks
- The known mid-run-UI-rebuild flake class (R-0202) may reappear in
  the base run — integration_gate.md step 3 carries the mandatory
  dist-hash neutralization check.
- Full-suite wall clock ~2.5 min per run; two runs plus attribution.
<<<END AUTHORED f079-r3-2>>>
