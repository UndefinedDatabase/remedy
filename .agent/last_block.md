Round f053-r2 (LARGE) — persist R1 verdict, then T002 COMPLETE.
Read docs/roadmap/features/T1_F053.md again INCLUDING the amendment
applied in commit A; it wins over the block summary.

COMMIT A (first, own commit, before any T002 code): in
.agent/live_review.md replace the R1 "In progress." Steps bullet with
f053-r2-1, "- R1: PENDING (reviewer)." with f053-r2-2, and
"- Next free ID: R-0160." with f053-r2-3; append f053-r2-4 at the end
of the "## How it fits" section of docs/roadmap/features/T1_F053.md.
cmp proofs for all four regions. Touches docs/roadmap/** → the docs
gate is mandatory (planner_reviewer_prompt.md §3 item 5).

T002 in slices, each its own commit(s), that slice's tests run before
the next starts; STOP on red and hand back with the failure raw.
SLICE 1 — STATUS-mirror producer (DECISION D2):
packages/orchestration/status_mirror.py, read-only, parses
docs/roadmap/STATUS.md of a given repo root into
run_report.StatusMirror (milestone = F075 MILESTONE GATE line or a
passed-in id; remaining = unchecked [ ]/[~] through the milestone
inclusive; accepted/in-progress capability lines from [x]/[~]).
Missing file, unparseable ledger, or no milestone line → None, never
a guess. Wired into collect_report_sources only where a repo root is
knowable; absent → status_mirror=None. Plus the stopped-by-operator
rule in NEXT_ACTION_RULES, worded exactly as the amendment, ranked
between open-decision and blocked-failed, with table +
golden-consistency test updates. Verify: test_run_report.py.
SLICE 2 — terminal-state hook at long_run_executor._apply_terminal:
every terminal transition (all_green, stopped_by_operator,
budget_exhausted, deadline_reached, blocked) writes EXACTLY ONE final
report into the job's evidence area, fixed filename, REGENERATED on
resume-then-finish, never appended. max_cycles_reached is NOT
terminal and writes nothing. A report-write failure never kills the
run: record and continue. Verify: new hook tests +
test_self_healing_cycles.py (50).
SLICE 3 — interim + CLI: `remedy job report <id>` on the job command
group; final report of a terminal job from disk sources; `--interim`
renders the labeled snapshot of a running job and never mutates state
(asserted); `--json` emits the structured sources; unknown job →
clean error, no traceback. Verify: tests/cli/test_job_report.py.

DO NOT TOUCH: notification delivery, UI rendering, cost calibration.
No closure work of any kind this round.
Round gate: test_run_report.py green · test_job_report.py green ·
tests/docs 293 · canary 42 — raw tails + exit codes in the handback.
Handback per docs/agents/handback_template.md: per-commit
changed-files tables, item-status table (commit A + slices 1-3 +
gates), authored-text proofs (sha256sum + cmp), enumeration of every
terminal path hooked. Red-proofs ONLY in a disposable git worktree on
a branch, never the primary checkout (R-0160 is open on exactly
this). Never write ## Verdicts content beyond applying f053-r2-2
verbatim; never merge anything. Then await the reviewer.
Authored texts f053-r2-{1,2,3,4} (sha256 verified before use, saved
verbatim under .agent/authored/, applied by copy).
OUTCOME: pending
