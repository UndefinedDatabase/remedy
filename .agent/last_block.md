Round f053-r3 — persist R2 verdict, two small fixes, then the
INTEGRATION GATE per docs/agents/integration_gate.md (read COMPLETELY,
including the amended step 2 applied in commit A; it wins over the block
summary). No closure work of any kind this round; never merge anything.

COMMIT A (first, own commit, before any fix): in .agent/live_review.md
replace the R2 "In progress." Steps bullet with f053-r3-1, append
f053-r3-2 to "## Verdicts" after the R1 entry, replace
"- Next free ID: R-0161." with f053-r3-3; in
docs/agents/integration_gate.md replace the ENTIRE step-2 item with
f053-r3-4. cmp proofs for all four regions.

COMMIT B — fix R-0161 (--final guard): apps/cli/commands/job.py
_cmd_job_run_report refuses --final when the job's metadata
cycle_terminal_status is NOT in long_run_executor.REPORTED_TERMINALS —
exit 1, stderr "Error: run still in progress (state: <state>) — use
--interim for a snapshot"; with --json {"error": "run_not_terminal",
...}. Never auto-render, never auto-switch mode. --interim and the
--json source dump are unchanged. Tests in tests/cli/test_job_report.py
(refusal text + json, allowed terminal still renders); mark
Done: R-0161 in the commit body. Verify: test_job_report.py.

COMMIT C — capability cap (CALL-2 ruling, A9):
run_report._capability_lines caps the "Can now" lines with _capped
(MAX_CAPABILITY_LINES = 10, honest "… and N more" pattern, noun
"accepted features"); in-progress lines share the cap. Goldens
unaffected (1 line). One test: 30 accepted → 10 lines + count line.
Verify: test_run_report.py.

INTEGRATION GATE exactly per docs/agents/integration_gate.md:
1. Branch run `python3 -m pytest -n auto -q` at HEAD — raw tail, full
   FAILED list, exit code, wall time; branch_failed.txt.
2. Base run at the merge base with origin/main (15105dbe) in a
   throwaway worktree ON A BRANCH per the amended step 2
   (git worktree add -b tmp/base-gate <path> 15105dbe); same records;
   base_failed.txt. Remove + prune + delete the tmp branch;
   git worktree list proof.
3. comm -13 (branch-only) and comm -23 (branch-fixed), BOTH raw.
   Environment-coupled attribution per the doc: parity targets are
   apps/ui/node_modules + apps/ui/dist only (restore parity, or
   attribute EVERY comm -23 id by direct evidence per id). The former
   .git-directory class is GONE (R-0159 fixed) — a dogfood-id failure
   at base is NOT attributable to it any more.
4. Serial re-run of every branch-only id; classify per the doc (F046
   pattern). A reproducible branch-only failure coupled to feature code
   = BLOCKER: STOP and hand back raw. No fixes inside the gate round
   beyond commits B/C, which land BEFORE the gate runs.
5. Wall clock; over ~5 min → note for a perf pass.

Round gate: test_job_report.py green · test_run_report.py green · full
suite (gate) · tests/docs 293 · canary 42 — raw tails + exit codes in
the handback. Handback per docs/agents/handback_template.md: per-commit
tables, item-status table (A, B, C, gate steps 1-5), authored-text
proofs, branch/base FAILED lists + both comm outputs verbatim, per-id
attribution table, wall clocks. Red-proofs only in a disposable worktree
ON a branch. Do NOT write ## Verdicts beyond applying f053-r3-2
verbatim. Closure is R4, its own round, never started here.
Authored texts f053-r3-{1,2,3,4} (sha256 verified before use, saved
verbatim under .agent/authored/, applied by copy).
OUTCOME: executed
