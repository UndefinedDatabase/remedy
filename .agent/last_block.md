OUTCOME: executed
── STEP R1 — F252 (bookkeeping + D8 + D10 + D11) ────────────────────
Goal:        Claim F252, reset the .agent state, and root-cause-fix
             the three product-bug classes D8, D10, D11 (14 ids).
Bundle:      Slice 0 bookkeeping · Slice A D8 · Slice B D10 ·
             Slice C D11 · closing full-suite delta.
Change:      docs/roadmap/STATUS.md (one line), .agent state files,
             product code + only these classes' tests where a test
             encodes a stale expectation. Nothing beyond this.
Constraints: AGENTS.md. F251 quarantine rules unchanged (never
             deletion, never blanket skips, never weakened
             assertions). Commits small (<500-line diffs), one
             logical step each — multiple commits expected. Worker
             never writes ## Verdicts / Resolved. Authored texts:
             save verbatim, sha256-verify BEFORE commit; mismatch =
             STOP, commit and push .agent/last_block.md with the
             refusal record, apply nothing.
Done when:   Every slice gate below green + full-suite delta
             recorded in the handoff.
Handback:    Completion report + rewrite .agent/handoff.md per
             docs/agents/handback_template.md. NO PR, NO STATUS [x],
             no closure artifacts — closure is a later
             reviewer-gated round.

PROCEDURE

Slice 0 — bookkeeping (own commit)
1. Open PR Gate: gh pr list --state open — expected empty (PR #160
   already merged). If anything is open, act per the AGENTS.md gate
   before branching.
2. From clean, current main (git pull --ff-only):
   git checkout -b feature/f252-standing-red-paydown
3. Save the three authored texts below VERBATIM to
   .agent/authored/f252-r1-1.md, f252-r1-2.md, f252-r1-3.md and
   sha256-verify each against its BEGIN marker.
4. Write .agent/last_block.md: line 1 "OUTCOME: pending", then THIS
   entire block verbatim. Set "OUTCOME: executed" when the round
   ends.
5. Apply by copy (disk-to-disk proof, never a retype):
   - f252-r1-1 replaces the line
     "- [ ] F252 — Standing-red paydown (154 ids, 13 classes)"
     in docs/roadmap/STATUS.md (afterwards grep -c of the old line
     = 0, of the new line = 1);
   - f252-r1-2 FULL REPLACE of .agent/live_review.md (cmp exit 0);
   - f252-r1-3 FULL REPLACE of .agent/plan.md (cmp exit 0).
6. Slice gate (docs round — STATUS touched):
   python3 -m pytest tests/docs/ -q
     → failing ids must be EXACTLY the baseline set (compare against
       .agent/f251_baseline/churn_gate2_run1.txt; none new)
   pytest tests/cli/test_golden_path.py -q → all pass
   Commit: "chore(f252): claim F252, reset agent state". Push.

Slice A — D8 "flight-plan schema_v regression" (3 ids)
7. Reproduce: python3 -m pytest tests/cli/test_scoped_listings.py -q
   Target ids (TestScopedListingsCLI):
     test_legacy_job_hidden_and_unscoped_label
     test_orphaned_label_on_deleted_project
     test_status_scoped
8. Diagnose the actual root cause (catalog label says flight-plan
   schema_v; the catalog is authoritative on ids, you are
   authoritative on the diagnosis — record it). Fix in PRODUCT code.
   A test edit is allowed only for a provably stale expectation and
   is named in the handoff with its reason.
9. Slice gate: the 3 ids pass; remaining failures in that file are a
   subset of the baseline set (its D14 ids may stay red). Canary
   green. Own commit(s), push.

Slice B — D10 discover-commands CLI rc=1 / non-JSON (8 ids)
10. Reproduce: python3 -m pytest tests/test_command_discovery.py -q
    (all 8 catalogued ids: TestCLIDiscoverCommands,
    TestCLIDiscoverCommandsSchemaV1).
11. Root-cause fix in product code, same rules as slice A.
12. Slice gate: tests/test_command_discovery.py fully green (this
    file has no other baseline red). Canary green. Own commit(s),
    push.

Slice C — D11 malformed TOML raises BudgetConfigError instead of
FenceConfigError (3 ids)
13. Reproduce:
    python3 -m pytest tests/orchestration/test_fence_e2e.py \
      tests/orchestration/test_fences.py -q
14. Root-cause fix in product code (error mapping at the
    fence-config boundary), same rules.
15. Slice gate: the 3 ids pass; both files' remaining failures are a
    subset of the baseline set. Canary green. Own commit(s), push.

Closing — full-suite delta (required by the feature file)
16. python3 -m pytest -n auto -q — keep the raw output. Extract the
    sorted failing-id set; comm -23 against the sorted
    .agent/f251_baseline/churn_gate2_run1.txt must be EMPTY (if an
    environment-dependent flake appears, name it explicitly — never
    fold it into the delta silently). Record in the handoff WHICH of
    the 14 target ids left the standing set.
17. git status --porcelain → empty. Everything committed and pushed.
18. Handback: per-commit changed-files tables, raw transcripts for
    every gate (command, exit code, output tail), the full-suite
    delta list, and one line per class: root cause + fix shape.

STOP rule for this bundle: at the FIRST slice gate you cannot turn
green without leaving the class's bucket (product bug turning into
product change or wider), stop there — do NOT start the next slice.
Record the diagnosis and the partial delta in the handoff and hand
back with the finished slices. Never silent scope drift.

--- BEGIN f252-r1-1 sha256=2d0a38649ee6e1f1f68b2c609f5b834fec46e3405624e3adf78bd64c6f792938 ---
- [~] F252 — Standing-red paydown (154 ids, 13 classes)
--- END f252-r1-1 ---

--- BEGIN f252-r1-2 sha256=6b278594b1a4add6faed224eeb4c710f8003cb9a3bbfaa9073c7c2120200bf4a ---
# Live Review — F252 Standing-red paydown (154 ids, 13 classes)

Branch: feature/f252-standing-red-paydown
Scope: every catalogued standing-red id reaches an explicit terminal
state, class by class (catalog: .agent/f251_baseline/class_map.txt).
Round 1 = STATUS claim + state reset + the three product-bug classes
D8, D10, D11 (14 ids).

## Steps
- R1: claim F252 in STATUS, reset state files, fix D8 + D10 + D11,
  record the full-suite delta, hand back.

## Findings
(none yet)

## Verdicts
(pending R1)
--- END f252-r1-2 ---

--- BEGIN f252-r1-3 sha256=c551e984c6590aaa7601f2124dafe2c8eb0f6d64c2fb0c586c50a5ce87c7ff53 ---
# Plan — F252 Standing-red paydown

## Goal
All 154 catalogued standing-red ids reach an explicit terminal state
(root-cause fix, honest test update, or operator-decided retirement);
DONE when three consecutive full-suite runs produce identical failure
sets, empty except explicit quarantines (F251 rules unchanged).

## Next Steps
- R1: product-bug classes — D8 flight-plan schema_v (3 ids), D10
  discover-commands CLI (8 ids), D11 fence TOML error type (3 ids);
  full-suite delta recorded in the handoff.
- Later rounds: product change (D5, D7, D9, D13), test rewrites (D6),
  doc drift (D1, D14), decision classes (D3, D12), the D4 design
  item, the two stopped F-A ids.
--- END f252-r1-3 ---
