OUTCOME: executed
── STEP R2 — F252 (R-0152 + the whole remaining feature, no closure) ─
Goal:        Persist the R1 verdict + finding R-0152, fix R-0152,
             then drive every remaining class to its terminal state:
             D9, D7, D5, D13, the two F-A ids, D6, D4 remainder,
             D1, D14, D3 (park), D12. Stop at the first red slice
             gate.
Bundle:      Slice 0 persist+fix · slices A–J below · closing
             full-suite delta.
Change:      Product code, tests, and docs strictly as each class
             requires. Nothing beyond.
Constraints: AGENTS.md. F251 quarantine rules unchanged (never
             deletion, never blanket directory skips, never weakened
             assertions; marker/skip needs reason + backlog ref per
             test). One commit minimum per slice, each <500-line
             diff; push after every slice. Worker never writes
             ## Verdicts / Resolved — the authored text below is the
             only source of those. Authored texts: save verbatim,
             sha256-verify BEFORE commit; mismatch = STOP, commit
             and push .agent/last_block.md with the refusal record,
             apply nothing. A class whose honest fix exceeds its
             bucket: STOP the bundle there, record the diagnosis,
             hand back with the finished slices.
Done when:   Every slice gate green (or a documented STOP) +
             full-suite delta recorded in the handoff.
Handback:    Completion report + rewrite .agent/handoff.md per
             docs/agents/handback_template.md (≤100 lines applies —
             many commits). NO PR, NO STATUS [x], no closure
             artifacts; integration gate and closure are their own
             later reviewer-gated rounds.

PROCEDURE

Slice 0 — persist verdict + findings, fix R-0152 (two commits)
1. Write .agent/last_block.md: line 1 "OUTCOME: pending", then THIS
   block verbatim; "OUTCOME: executed" when the round ends.
2. Save the two authored texts below VERBATIM to
   .agent/authored/f252-r2-1.md and f252-r2-2.md; sha256-verify
   each. Apply by copy: f252-r2-1 FULL REPLACE .agent/live_review.md
   (cmp exit 0), f252-r2-2 FULL REPLACE .agent/plan.md (cmp 0).
   Commit A: "chore(f252): persist R1 verdict + R-0152". Push.
3. Fix R-0152 in apps/cli/commands/do_cmd.py: remove the
   `or call_fn` fallback; when make_structured_call_fn(FlightPlan)
   returns None, skip LLM planning the same way the no-provider
   path does. Mark `Done: R-0152` in live_review.md's finding line.
   Gate: python3 -m pytest tests/cli/test_scoped_listings.py -q
   (18 passed) + canary. Commit B, push.

Slice A — D9 command-catalog classification drift (3 ids)
4. Reproduce: python3 -m pytest tests/test_command_catalog.py -q
   Root-cause fix (product or honest test update — diagnose, record
   in .agent/decisions.md). Gate: file fully green + canary.

Slice B — D7 dev_server private names removed (6 ids)
5. Files: tests/orchestration/test_failure_postmortem.py (1),
   tests/runtimes/test_supervisor_portability.py (5). Diagnose: the
   catalog says tests reach for removed private names; decide per id
   between restoring a shared public seam and honest test update.
   Gate: the 6 ids pass, files' remaining failures subset of
   baseline. Canary.

Slice C — D5 CLI requires a registered project (11 ids)
6. Files: tests/test_cli_main.py (10),
   tests/orchestration/test_test_runner.py (1). Per-id rule, D10
   precedent: intentional F148 behavior → fixture registers a
   project (honest update, assert rc); a genuine cwd-coupling defect
   against a command's documented contract → product fix. Record
   the split in decisions.md. Gate: the 11 ids pass, subset rule.
   Canary.

Slice D — D13 review-zip / evidence packaging drift (11 ids)
7. Files: tests/orchestration/test_review_zip_hygiene.py (8),
   test_review_manual_completion_shapes.py (1),
   test_review_subject_explicit_base.py (1),
   test_evidence_index.py ids stay D14. Diagnose against the REAL
   packaging behavior (make_review_zip.sh, build_review_manifest);
   product fix where packaging broke a documented contract, honest
   update where the contract legitimately moved. Gate: the 11 ids
   pass, subset rule. Canary.

Slice E — the two stopped F-A ids from F251 (2 ids, product change)
8. From the F251 notes (.agent/f251_baseline/, flake_set /
   reviewer_flake_extras): the real-Vite probe binds the product's
   apps/ui port; the supervisor teardown guard's fix reaches the
   product stop/ownership path. Product fixes. Gate: each id run 3x
   consecutively green (they were flake-class), no port bound on the
   product's default. Canary.

Slice F — D6 incomplete MagicMock vs real comparison (9 ids)
9. Files: tests/orchestration/test_test_execution_service.py (8),
   tests/orchestration/test_test_runner.py (1). Test rewrites: real
   objects or complete fakes instead of half-specced MagicMocks —
   assertions must stay at least as strong. Gate: the 9 ids pass,
   subset rule. Canary.

Slice G — D4 remainder: context.md joins the maintained state set
10. Rewrite .agent/context.md to current reality (worker-owned
    file): active branch, F252 scope boundaries, resource-safety
    note, current steps — whatever the 5 remaining D4 ids assert;
    read the tests first, satisfy them honestly, keep the file
    current every future round. Gate:
    python3 -m pytest tests/ui_server/test_dashboard_contract.py \
      tests/orchestration/test_test_runner.py \
      tests/regression/test_resource_safety.py -q
    → remaining failures subset of baseline minus the D4 ids.
    Canary.

Slice H — D1 doc/file missing at flat path (36 ids)
11. Per id: the doc moved in the restructure → point the test at
    the real path (docs/README.md is the index); the doc is
    genuinely gone → restore or fix the doc, never delete the test.
    Multiple commits fine, subset-rule gate per touched test file.
    Canary per commit.

Slice I — D14 misc drift (46 ids incl. the 13 tests/docs pins)
12. Same per-id triage as D1. The 13 README pins: update the pinned
    text honestly to current truth — a pin that asserts a stale
    claim is updated WITH the README statement it pins, same
    commit. Gate at slice end: python3 -m pytest tests/docs/ -q
    fully green + touched files subset rule. Canary.

Slice J — decisions D3 and D12 (registered above, execute)
13. D3 (10 ids): quarantine markers — skip + reason + backlog ref
    "Tier 5 UI build (F019+)", per test, per F251 rules. Gate:
    python3 -m pytest <the three D3 files> -q -rs → 0 failed, the
    10 shown as skipped with reasons.
14. D12 (1 id): git log --follow on .claude/agents/
    remedy-reviewer.md. Removal without stated reason → restore
    from history and the test goes green. Deliberate, reasoned
    removal → quarantine with that reason + backlog ref. Record
    which path in decisions.md. Gate: the id green or properly
    skipped.

Closing — full-suite delta
15. python3 -m pytest -n auto -q --junitxml=<scratch>/f252-r2.xml —
    keep the raw output. Extract the failing-id set from the xml,
    LC_ALL=C sort, comm against LC_ALL=C-sorted
    .agent/f251_baseline/churn_gate2_run1.txt. NEW must be EMPTY;
    record the GONE list per class in the handoff. Expected end
    state: failures empty except explicit quarantines (D3, possibly
    D12) and any documented STOP remainder.
16. git status --porcelain → empty; everything pushed. Handback per
    template: per-commit tables, raw gate transcripts, the delta,
    one line per class: root cause + fix shape + terminal state.

--- BEGIN f252-r2-1 sha256=11d5380886ecdd2fcf3c2ede9e8a760ad6612788b6f64b7e30181b85289e7ba7 ---
# Live Review — F252 Standing-red paydown (154 ids, 13 classes)

Branch: feature/f252-standing-red-paydown
Scope: every catalogued standing-red id reaches an explicit terminal
state, class by class (catalog: .agent/f251_baseline/class_map.txt).

## Steps
- R1: claim + state reset + product-bug classes D8, D10, D11. Done.
- R2: persist this verdict + R-0152, fix R-0152, then D9, D7, D5,
  D13, the two F-A ids, D6, D4 remainder, D1, D14, D3 park, D12;
  full-suite delta; stop at the first red slice gate. In progress.

## Findings
- R-0152 (minor, open): apps/cli/commands/do_cmd.py — the `do`
  planning path falls back to the intake-bound call_fn
  (`make_structured_call_fn(FlightPlan) or call_fn`) when the
  FlightPlan factory returns None. The degraded path then knowingly
  re-drives planning with a wrong-shaped native schema — the exact
  D8 failure shape. Fix: no fallback; when the factory returns None,
  skip LLM planning exactly like the no-provider path.

## Verdicts
- R1: PASS (reviewer, 2026-07-29). Range 7baff1d..cc247fa, 5
  commits; diff = instructed scope only. Authored proofs verified
  disk-to-disk against the reviewer's originals (cmp 0 x5; STATUS
  grep new=1/old=0). Gates re-run independently: 18/92/208 passed,
  canary 42, tests/docs 13F/279P = baseline exactly. Full suite
  re-run twice by the reviewer: 134F/14172P; junitxml failing-id set
  vs churn_gate2_run1.txt: NEW empty, GONE = exactly the claimed 20
  (14 targets, 2 D14 siblings, 4 D4). Red-proof in a throwaway
  worktree at 7baff1d: 3/3 sampled target ids fail at base, pass at
  HEAD; worktree removed, primary checkout clean. R-0152 filed as
  minor, non-blocking. Verified tier: scoped gates + canary + a full
  suite run (reviewer-side; the official integration gate stays a
  dedicated later round). LAST_REVIEWED_SHA = cc247fa.
--- END f252-r2-1 ---

--- BEGIN f252-r2-2 sha256=9b806d942ca51c5b64a5dd85c0b961832c9f431edd70611adc72418fb8be5b2d ---
# Plan — F252 Standing-red paydown

## Goal
All 154 catalogued standing-red ids reach an explicit terminal state
(root-cause fix, honest test update, or operator-decided retirement);
DONE when three consecutive full-suite runs produce identical failure
sets, empty except explicit quarantines (F251 rules unchanged).

## Next Steps
- R2 (bundle): fix R-0152; class rounds in order D9, D7, D5, D13,
  the two stopped F-A ids, D6; D4 remainder via a current
  context.md; D1 + D14 doc-drift triage; D3 parked by decision
  (quarantine + Tier 5 backlog ref); D12 restore-or-quarantine by
  history. Full-suite delta at the end (or at a STOP).
- Then: integration-gate round, closure round (evidence job, fresh
  zip, STATUS [x], PR) — reviewer-gated, never bundled.
--- END f252-r2-2 ---
