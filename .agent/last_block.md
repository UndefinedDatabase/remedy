OUTCOME: executed
── STEP R3 — F252 (R-0153 + integration gate + determinism proof) ───
Goal:        Persist the R2 verdict + finding R-0153, fix R-0153,
             then run the official integration-gate round and the
             feature's DONE proof (three consecutive identical
             full-suite runs).
Bundle:      Slice 0 persist + fix · Slice A integration gate ·
             Slice B three-run determinism proof.
Change:      .agent state per the authored texts;
             tests/docs/test_docs_consistency.py (one dead
             assertion). Nothing else.
Constraints: AGENTS.md. Worker never writes ## Verdicts / Resolved.
             Authored texts: save verbatim, sha256-verify BEFORE
             commit; mismatch = STOP, commit and push
             .agent/last_block.md with the refusal record, apply
             nothing. A red integration gate is a normal repair
             situation: STOP after recording the raw transcript,
             hand back — do not fix ad hoc inside this round.
Done when:   R-0153 gate green + integration gate per
             docs/agents/integration_gate.md complete + three
             consecutive full-suite runs with identical,
             quarantine-only failure sets, all transcripts in the
             handoff.
Handback:    Completion report + rewrite .agent/handoff.md per
             docs/agents/handback_template.md. NO closure artifacts:
             no evidence job, no zip, no STATUS [x], no PR — R4 is
             its own reviewer-gated round.

PROCEDURE

Slice 0 — persist verdict + finding, fix R-0153 (two commits)
1. Write .agent/last_block.md: line 1 "OUTCOME: pending", then THIS
   block verbatim; "OUTCOME: executed" when the round ends.
2. Save the two authored texts below VERBATIM to
   .agent/authored/f252-r3-1.md and f252-r3-2.md; sha256-verify
   each. Apply by copy: f252-r3-1 FULL REPLACE .agent/live_review.md
   (cmp exit 0), f252-r3-2 FULL REPLACE .agent/plan.md (cmp 0).
   Commit A: "chore(f252): persist R2 verdict + R-0153". Push.
3. Fix R-0153 in tests/docs/test_docs_consistency.py: delete the
   `assert unaccepted <= named` line, its `unaccepted = …` binding
   if now unused, and the comment that introduces it; the
   accepted-blocks loop stays untouched. Mark `Done: R-0153` in
   live_review.md's finding line (that one edit only).
   Gate (docs round): python3 -m pytest tests/docs/ -q → 292 passed
   + canary pytest tests/cli/test_golden_path.py -q → 42 passed.
   Commit B: "test(f252): drop a dead assertion from the README pin
   (R-0153)". Push.

Slice A — official integration gate
4. Follow docs/agents/integration_gate.md exactly (that file is the
   procedure; do not improvise). Record command, exit code and
   output tail for every step in the handoff. A regression here →
   STOP per Constraints and hand back with the raw transcript.

Slice B — feature DONE proof: three consecutive identical runs
5. Three times in a row, no code change in between:
   python3 -m pytest -n auto -q --junitxml=<scratch>/f252-run<i>.xml
   For each run extract the failing-id set from the junitxml
   (LC_ALL=C sorted). Required: all three sets are IDENTICAL and
   EMPTY, and the skip count stays 19 (11 F252 quarantines + 8
   env-gated). Any nonempty or differing set → STOP, record all
   three transcripts, hand back.
6. Record in the handoff: the three "N passed, M skipped in Xs"
   summary lines, the three set-comparison results (empty/empty/
   empty), and runtimes (§3 budget: if a run exceeds ~5 min wall
   clock, note it — perf pass is F252 follow-up material, not this
   round's work).
7. git status --porcelain → empty; everything pushed. Handback per
   template.

--- BEGIN f252-r3-1 sha256=1f07b06c19f96f3d5b09bbf049c216ebe9c0c94738c6cf87602894d4a66b8255 ---
# Live Review — F252 Standing-red paydown (154 ids, 13 classes)

Branch: feature/f252-standing-red-paydown
Scope: every catalogued standing-red id reaches an explicit terminal
state, class by class (catalog: .agent/f251_baseline/class_map.txt).

## Steps
- R1: claim + state reset + product-bug classes D8, D10, D11. Done.
- R2: R-0152 + all remaining classes; 143 fixed, 11 quarantined by
  decision; full suite 14295 passed / 0 failed / 19 skipped. Done.
- R3: persist this verdict + R-0153, fix R-0153, then the
  integration-gate round per docs/agents/integration_gate.md incl.
  the three-consecutive-runs determinism proof. In progress.

## Findings
- R-0153 (nit, open): tests/docs/test_docs_consistency.py — in the
  rewritten README honesty pin, `assert unaccepted <= named` is a
  tautology (`unaccepted` is derived from `named`), a dead check
  that reads as coverage. Fix: delete the assertion and its comment
  line; the accepted-blocks loop above it is the real check.

## Verdicts
- R1: PASS (reviewer, 2026-07-29). Range 7baff1d..cc247fa. Details
  in git history of this file; LAST_REVIEWED_SHA was cc247fa.
- R2: PASS (reviewer, 2026-07-29). Range cc247fa..fc3e843, 14
  commits. Authored proofs disk-to-disk: cmp 0 for plan.md and both
  authored files; live_review.md deviates from f252-r2-1 by exactly
  the one instructed `Done: R-0152` edit. Diff reviewed bottom-up:
  product fixes (catalog action classes, do-planning fallback
  removal, evidence-packaging v1.1 + verdict read-back +
  self-check scope, provider-evidence zero counts, named exception
  catches, runtime port override) all carry in-code rationale; test
  edits are honest updates or strengthenings — D6 removed zero
  assertions, renames declared, quarantines are per-test skips with
  reason + backlog ref (10x D3, 1x D12 per the registered
  decisions). Full suite re-run by the reviewer: 14295 passed, 0
  failed, 19 skipped (11 quarantines + 8 pre-existing env-gated),
  matching the handback exactly; failing set empty, so all 154
  catalogued ids have left the standing set. R-0153 filed as nit,
  non-blocking. Verified tier: scoped gates + canary + a reviewer
  full-suite run (the official integration gate is R3).
  LAST_REVIEWED_SHA = fc3e843.
--- END f252-r3-1 ---

--- BEGIN f252-r3-2 sha256=dc3e03cc7b0b118d6852e83b4f121d4f360aacbe3817cbdd0f61d795435de0fe ---
# Plan — F252 Standing-red paydown

## Goal
All 154 catalogued standing-red ids reach an explicit terminal state
(root-cause fix, honest test update, or operator-decided retirement);
DONE when three consecutive full-suite runs produce identical failure
sets, empty except explicit quarantines (F251 rules unchanged).

## Next Steps
- R3: fix R-0153 (dead assertion), then the integration-gate round
  per docs/agents/integration_gate.md, plus the feature's own DONE
  proof: three consecutive `pytest -n auto -q` runs with identical,
  quarantine-only failure sets, all three transcripts recorded.
- R4: closure round per docs/roadmap/STATUS_closure_protocol.md
  (evidence job, fresh review zip, STATUS [x], PR) — reviewer-gated,
  never bundled with R3.
--- END f252-r3-2 ---
