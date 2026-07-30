OUTCOME: pending
── STEP R2 — F051: verdict persist + R-0157 fix + Built State + gate ────
Block id: f051-r2
Goal:        Persist the R1 PASS verdict, make the unattended path
             reachable from the CLI (R-0157), record Built State, then
             run the integration gate per docs/agents/integration_gate.md.
Bundle:      1 guard · 2 authored texts · 3 persist commit ·
             4 R-0157 fix + CLI test · 5 Built State · 6 docs gate +
             canary · 7 integration gate · 8 handback commit + push +
             PR update
Change:      .agent/**, apps/cli/commands/job.py (run-loop flag
             passthrough; catalog entry if the flag needs registering),
             docs/roadmap/features/T1_F051.md (Built State section),
             the CLI test (new or existing test file per repo pattern).
             Nothing else.
Constraints: R-0157 fix is ADDITIVE — default behavior unchanged
             (attended asks, exactly as now). Follow the new AGENTS.md
             Code Discoverability Conventions for any new names. Do not
             touch: notification channels, inbox UI, decision
             auto-answering, closure. Closure and its zip are NOT part
             of this round. STOP-ON-RED: integration-gate step 4 — a
             reproducible branch-only failure coupled to feature code
             ends the block, hand back immediately.
Done when:   CLI-level unattended test green; docs gate + canary green;
             integration gate executed with full records (raw tails,
             FAILED lists, exit codes, wall time, per-id attribution).
Handback:    Completion report + rewrite .agent/handoff.md (changed-
             files tables, sha256sum outputs verbatim, all raw gate
             logs, worktree-removal proof).

AUTHORED-TEXT PROTOCOL (both blocks below): bytes = the lines strictly
BETWEEN the BEGIN and END marker lines, joined with LF, plus one final
LF. Save to .agent/authored/<name>.md, verify sha256sum against the
BEGIN-marker hash BEFORE any use. Mismatch: rejoin hard-wrapped lines
with a single space and re-verify; if still mismatched, STOP that item,
record received bytes + computed hash in the handoff, hand back. Never
apply an unverified text.

1. Guard: record this block in .agent/last_block.md (id f051-r2,
   OUTCOME pending; note any transport faults).

2. Save and verify the two authored texts:
   .agent/authored/f051-r2-1.md, .agent/authored/f051-r2-2.md.
   Record the sha256sum lines verbatim for the handoff.

3. Commit 1 — persist the verdict, own commit:
   - .agent/live_review.md := full replace with f051-r2-1.md (cmp).
   - .agent/plan.md        := full replace with f051-r2-2.md (cmp).
   git add those + .agent/authored/f051-r2-*.md + .agent/last_block.md
   Commit message: chore(f051): persist R1 verdict (PASS) + register R-0157

4. R-0157 fix — CLI unattended wiring:
   Inspect the run-loop command path first (_cmd_job_run_cycles at
   apps/cli/commands/job.py:637, catalog entry "job.run"): if the CLI
   already has a --yes/unattended convention, reuse that exact
   spelling; otherwise add an additive --unattended flag. Wire it
   through to run_cycles(unattended=...). Help text says what it does:
   safe defaults auto-apply and land in the escalation assumption log;
   questions without a default still wait.
   CLI-level test (place per repo pattern, e.g. alongside the existing
   run-loop CLI tests or tests/orchestration/test_escalation.py's CLI
   class): (a) with the flag, a needs_decision task carrying a safe
   default is auto-answered (answer_source "default") and the run
   continues past it; (b) without the flag, the same fixture leaves
   the decision open. Then mark the finding in .agent/live_review.md
   by appending exactly "  Done: R-0157 (commit <sha>)." as a new
   line at the end of the R-0157 bullet — change nothing else in the
   file; the reviewer sets Resolved after verifying.
   Slice gate: the new CLI test file + tests/orchestration/
   test_escalation.py -q -> exit 0.
   Commit message: fix(f051): expose the unattended run mode on the run-loop CLI (R-0157)

5. Built State — docs/roadmap/features/T1_F051.md:
   Append a "## Built State" section at the end of the file, F050's
   shape (T1_F050.md:66): per T-slice, the files, the key exported
   names, the behavioral invariants, and the test counts — strictly
   factual from the diff, no claims beyond what tests pin. Include
   R-0157's CLI flag once it exists (this commit comes after item 4).
   Commit message: docs(f051): record Built State (T001–T003 + R-0157 wiring)

6. Docs-round gate + canary (this round touches docs/roadmap/**):
   python3 -m pytest tests/docs/ -q                    (exit 0)
   python3 -m pytest tests/cli/test_golden_path.py -q  (exit 0)

7. Integration gate — follow docs/agents/integration_gate.md exactly
   (branch run, base run in a throwaway worktree at merge base
   894375e, comm both directions, per-id attribution, worktree
   remove + prune with git worktree list proof). Known context: the
   base run is expected to show the R-0155 environment class
   (~20 ids, no install/build outputs in a fresh worktree) in
   comm -23 — record them, they are NOT failures the branch fixed.
   Record everything raw; the verdict itself is the reviewer's, not
   yours — your handback carries the records only.
   STOP-ON-RED per step 4 of that file.

8. Final commit (handoff rewrite + last_block OUTCOME executed), push,
   update PR #165's body with R2 (verdict PASS noted, R-0157 fixed,
   Built State, gate records). Do NOT merge. Hand back.

TRANSPORT NOTES (worker, f051-R2):
(1) Both authored texts arrived CLEAN. Both sha256sum outputs matched
    their BEGIN-marker hashes on first computation, before any use — no
    rejoin needed.
(2) Cosmetic wraps in the block's own instruction text only (the item-4
    and item-5 commit-message lines and the item-4 slice-gate path are
    recorded above rejoined). No authored bytes affected.
