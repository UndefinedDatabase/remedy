── STEP T003 closure run 1 — the INTEGRATION GATE — F085 — R70 ───────────────

Goal: run the first of the two full-suite runs this feature owes, per docs/agents/integration_gate.md,
and record the R69 PASS. The build work is finished: this round measures the branch against its merge
base and attributes every difference. It adds no test, changes no source file and asserts no new
behaviour.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 record the R69 PASS · C3 the gate evidence dir · C4 handback.

CONVENTION, binding on every count here, carried verbatim in force from the R69 block. A line count is
the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and NO
joiner and NO terminator byte is ever added. THIS BLOCK'S ONE FROM/TO PAIR IS PLAN24. ITS ONE
END-OF-FILE APPEND, WHICH HAS NO FROM AT ALL, IS RECORD38 — listed rather than counted, per §3
checklist item 11. RECORD38 CARRIES ITS OWN LEADING BLANK LINES, so the separation its target's
convention requires is a property of bytes that were measured and never of a join shape that was
reasoned about.

## Change

C1 applies PLAN24F→PLAN24T to `.agent/plan.md`, rewriting the `## Current Step` section and the WHOLE
`## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep a stale
label. C2 appends RECORD38 to the END of `.agent/live_review.md`. C3 creates the gate evidence dir
`.agent/gate_f085_r70/` and commits ONLY the files G4 names there; the raw run logs are NOT committed,
for the reason `full_log_provenance.txt` states.

Change set, named rather than counted: `.agent/authored/f085-r70.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, the files under `.agent/gate_f085_r70/` that G4 names, and
`.agent/handoff.md`. Nothing else. NO `docs/**` path is in that set, so no docs suite is ordered and
Rule A4 is untouched. NO `.py` path is in it, so NO lint gate is ordered this round — that is a
consequence of the change set and not an omission. NO source file under `packages/` or `apps/` is
touched, so NO red control is ordered either: this round measures, and a measurement round has no new
assertion to prove falsifiable. Every TRACKED path named in a gate below was resolved with `git
ls-tree 126b70ae`, one call per path, before emission, per checklist item 24, and all of them exist.
Three named paths are deliberately NOT tracked and `git ls-tree` reports them absent by design:
`apps/ui/node_modules` and `apps/ui/dist` are gitignored build artifacts, which is precisely why G4
orders them COPIED into the base worktree rather than expected there, and the reviewer confirmed both
exist in the primary checkout at 126b70ae with `ls -d`. `.agent/authored/f085-r70.md` and everything
under `.agent/gate_f085_r70/` are the paths no gate reads at the base, because C0a and C3 create them.

WHAT THIS GATE IS AND WHAT IT IS NOT. The integration gate does not ask whether the suite is green. It
asks whether THIS BRANCH made anything worse than its merge base, which is a COMPARISON and never a
colour — so no expected exit code, no expected pass count and no expected failure count is ordered
anywhere below. Both sides are reported as measured. The one thing that blocks is a branch-only
failure that reproduces serially and is coupled to this feature's code; everything else is recorded
and classified. The merge base is a5a70621, which is the commit `.agent/plan.md` at 126b70ae names as
this branch's cut point, and it has not moved.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r70.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C4; if it exists, finish the commit in
   flight, write the handback and stop. `git status --porcelain` is empty at round start and after
   every commit.
3. PAIR SHAPE. The reviewer ran the containment test at emission against the target's blob at
   126b70ae and prints its own output here per checklist item 15: PLAN24F→PLAN24T `TO contains FROM:
   false`. It is therefore a REWRITE and owes the FROM 0x / TO 1x reading over its post-commit file.
   PLAN24F occurs EXACTLY 1x in `.agent/plan.md` at 126b70ae — the reviewer measured it.
4. RECORD38 HAS NO FROM. Do not invent one and do not report a FROM count for it. It is appended at
   the END of `.agent/live_review.md` and owes the ORDERED EQUALITY of §4.9 as R-0531 narrows it:
   pre-commit blob a byte-exact PREFIX, slice an exact SUFFIX, and that commit's ADDED lines exactly
   the slice's lines IN ORDER.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of the gate evidence. Only C0a
   and C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
6. NOTHING IN `.agent/live_review.md` THAT ALREADY EXISTS AT 126b70ae IS EDITED, MOVED OR DELETED. No
   test, no source file and no document is touched this round by any commit.
7. Every sentence in RECORD38 that states a reading of a file names the SHA it was read at in the same
   clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches to EVERY
   reading in the clause, not only the first. RECORD38 states readings of R69's range only, all of
   which are prior state, so every SHA it names already exists when it is written.
8. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD38 is reviewer text and carries the R69 gate
   entry. Do not add a `Landed:` line, do not add a `Done:` paragraph of your own, and do not edit
   RECORD38 to reconcile it with anything you measure. A disagreement between RECORD38 and your own
   reading is a finding to REPORT in the handback, never to fix — the rule that caught R66 and R67.
9. THIS ROUND REGISTERS NOTHING AND RESOLVES NOTHING. Registered stays 178, done stays 31, landed
   stays 0, open stays 147, and the next free id stays R-0564. RECORD38 therefore carries no `Done:`
   line and no `- R-` registration line; G6 proves it. If the gate turns up a BLOCKER under G4, that
   is reported in the handback and registered by the REVIEWER next round, not by you.
10. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as its correction section fixes the ruled figure:
   490 lines TOTAL, PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all
   three on the final bytes at emission. The worker re-measures all three from the committed
   `.agent/authored/f085-r70.md`; a mismatch is a finding against this block, not the worker.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and its
   output, and push what is committed. Never edit a slice to make a gate green, and never widen the
   change set to route around a red. G4 is the one gate below whose non-zero exit is EXPECTED to be
   possible and is not by itself a red — read G4's own text for what blocks and what does not.
12. RUN THE SUITES SERIALLY, one pytest process at a time, never alongside another in any checkout or
   worktree. These suites spawn real supervisors and real children that bind ports, so two concurrent
   runs redden each other on tests neither touched. THE BRANCH RUN AND THE BASE RUN ARE THEREFORE
   SEQUENTIAL, never concurrent, even though they live in different checkouts. `-n auto` parallelism
   INSIDE one pytest process is what the gate procedure orders and is not what this constraint bars.
13. RUN LOGS ARE WRITTEN OUTSIDE THE REPO'S TRACKED TREE WHILE A SUITE RUNS, to the gitignored scratch
   dir `.remedy-wt/.cache/gate_r70/`, and are copied into `.agent/gate_f085_r70/` only after the run
   exits (R-0176: a log growing inside the tree during a run changes the worktree digest mid-run and
   fails the manifest-identity ids as false positives). Evidence files are named `.txt` and never
   `.log` (R-0169). The raw full logs stay in scratch and are NOT committed; `full_log_provenance.txt`
   records their line count and sha256 so the trim is auditable, exactly as
   `.agent/gate_f115_r21/full_log_provenance.txt` does at 126b70ae.
14. THE BASE WORKTREE IS CREATED ON A THROWAWAY BRANCH AND NEVER DETACHED (DECISION D3): the
   self-dogfood branch guard refuses a detached HEAD by design, so a detached base worktree fails the
   guard-dependent ids and poisons the comparison. Remove the worktree, delete the throwaway branch,
   and prove `git worktree list` is one line at the end. Never commit anything in that worktree.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit. The base worktree G4 creates is removed before C4; `git worktree
list` is one line at round start and one line at the end.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r70.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each. Also report the block's TOTAL, PROSE and RECORD38 line counts read
from that committed file, against constraint 10's 490 / 400 / 140, where PROSE is TOTAL minus the
slice lines.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN24F→PLAN24T is a REWRITE over `.agent/plan.md` at C1: report FROM 0x and TO exactly 1x over the
   post-commit blob, and re-applying the extracted FROM→TO to the pre-commit blob must reproduce the
   post-commit blob BYTE-EXACTLY.
 - RECORD38 at C2 over `.agent/live_review.md`: report the ordered-equality readings constraint 4
   names — PREFIX, SUFFIX, `pre + slice` equal byte for byte, and that commit's ADDED lines exactly the
   slice's lines IN ORDER.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0. Count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 THE INTEGRATION GATE, per docs/agents/integration_gate.md, run BEFORE C3 so C3 commits its results.
Every number below is REPORTED, never predicted; no expected value is ordered for any of them.
 - BRANCH RUN, in the primary checkout, from the repository root:
   `python3 -m pytest -n auto -q`, with stdout+stderr to
   `.remedy-wt/.cache/gate_r70/branch_run.txt`. Record exit code and wall seconds into
   `.agent/gate_f085_r70/branch_meta.txt` as `EXIT_CODE=<n>` and `WALL_SECONDS=<n>`. Copy the last 40
   lines of that log to `.agent/gate_f085_r70/branch_run_tail.txt`. Write the sorted FAILED list to
   `.agent/gate_f085_r70/branch_failed.txt` with `grep '^FAILED' ... | sort`.
 - BASE WORKTREE, per constraint 14:
   `git worktree add -b tmp/base-gate-r70 .remedy-wt/base-r70 a5a70621`.
 - PARITY BEFORE THE BASE RUN, per the R-0155 amendment. COPY — never symlink — the primary
   checkout's `apps/ui/node_modules` and `apps/ui/dist` into the base worktree at the same relative
   paths, because a symlinked auto-build writes THROUGH into the primary checkout. Set
   `REMEDY_UI_NO_AUTO_BUILD=1` for the base run but do NOT trust it alone: record a sha256 over the
   copied `apps/ui/dist` tree BEFORE the base run and again AFTER it, into
   `.agent/gate_f085_r70/base_parity.txt`. If those two digests differ, the parity claim is VOID —
   say so there and attribute every base-only failure per id instead of claiming parity.
 - BASE RUN, sequentially after the branch run has exited, inside that worktree, same command, log to
   `.remedy-wt/.cache/gate_r70/base_run.txt`; sorted FAILED list to
   `.agent/gate_f085_r70/base_failed.txt`; its exit code and wall seconds appended to
   `base_parity.txt`.
 - COMPARE. `comm -13 base_failed.txt branch_failed.txt` → `comm_branch_only_failures.txt`, and
   `comm -23 base_failed.txt branch_failed.txt` → `comm_base_only_failures.txt`. Both files are
   committed even when empty. Report the line count of each.
 - ATTRIBUTION, into `.agent/gate_f085_r70/attribution.txt`, with ONE entry for EVERY id in
   `comm_branch_only_failures.txt` — no id may be silently absent. Re-run each such id SERIALLY by its
   exact node id in the primary checkout and record the command, exit code and outcome. Classify:
   serial-pass ⇒ xdist-flake class, recorded and not a blocker; serial-fail ⇒ re-run the same id in
   the base worktree and report whether it reproduces there. A branch-only id that fails serially,
   does NOT reproduce at the base, and touches this feature's code is a BLOCKER: stop under constraint
   11, write the handback, and do not attempt a fix — the fix is its own reviewer-gated round. Every
   id in `comm_base_only_failures.txt` is likewise attributed by direct evidence, naming the missing
   artifact per id where the environment class applies; an unattributed id there blocks the verdict.
 - PROVENANCE. `.agent/gate_f085_r70/full_log_provenance.txt` records, for each raw log left in
   scratch, its path, its `wc -l` line count and its sha256, plus one sentence saying why the raw logs
   are not committed. Then remove the worktree and delete `tmp/base-gate-r70`.
 - WALL BUDGET. If the branch run exceeds ~5 minutes wall clock, say so in the handback as a note for
   a perf pass. That is a note and never a red.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 37 lines by applying the pair to that blob at 126b70ae — two shorter than the round
before, because PLAN24T's `## Next Steps` list carries one item fewer than PLAN24F's.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
126b70ae and at HEAD, from the line-start patterns for a registration, a resolution and a landed line.
The reviewer's base reading is 178 / 31 / 0, 147 open, max registered R-0563, max resolved R-0563. At
HEAD the reading must be UNCHANGED — 178 / 31 / 0 and 147 open with the same two maxima — because
constraint 9 rules this round registers nothing and resolves nothing. All three symmetric differences
must be EMPTY. Next free id R-0564. Report all three symmetric differences, the duplicate-id count and
the count of resolutions naming an unregistered id, at both SHAs.

G7 CANARY, in the primary checkout and never in a worktree (R-0518), serially per constraint 12:
`python3 -m pytest tests/cli/test_golden_path.py -q` — exit 0. Report the passed count; the count is
reported, never predicted. The reviewer's own base reading at 126b70ae was `42 passed`. This runs even
though G4's branch run already covered it, because §3 tier 2 makes the canary a property of every
handback rather than of the suites a round happens to run.

G8 HYGIENE. `git diff --name-only 126b70ae..HEAD` measured BEFORE C4 holds exactly the change set
above minus `.agent/handoff.md`, which C4 writes, and nothing else — and in particular holds no path
under `packages/`, `apps/`, `docs/`, `scripts/` or `tests/`, and no path ending in `.log`. Report the
list. Report per-commit insertions for every commit BEFORE C4 — C4 cannot measure itself, so its own
go in the round report — and confirm none exceeds 500. This branch spent the AGENTS.md
declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under constraint 11,
never a declaration; if the gate evidence would push C3 over the cap, TRIM the committed tail files
rather than the FAILED lists and say so. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base SHA
126b70ae, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3 and
C4, the real G1-G8 results with exit codes, the open-findings count and the next expected action. The
Bundle above holds more than five commits, so the ≤100-line cap AGENTS.md allows when a per-commit
table needs it applies; drop no section. G4's numbers belong in that table in full: both exit codes,
both wall times, both FAILED counts, both comm line counts, and the attribution verdict per
branch-only id.
Repeat this Fortschritt line verbatim:
Fortschritt: ~100 % der Bauarbeit und das Integration Gate gelaufen (T001 gebaut · T002 KOMPLETT ·
T003 KOMPLETT und akzeptanzgemessen · R69 PASS) — offen bleibt nur noch die Closure: Evidence-Job,
frischer Review-Zip, die STATUS-Zeile und der PR. Schätzung, gegen die Klassentabelle aus Amendment
F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: R71 is CLOSURE per
docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH review zip, the reviewer-authored STATUS
line, and the PR the operator merges at the next Open PR Gate. TWO: R70 carries no verdict of its own,
because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4 item 13); R71 carries it. THREE: a standalone closing line
stating the open findings count and the next free id. FOUR:
`Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires every
handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN24F
## Current Step
R69, this round: T003's last acceptance line. A guarded `test`-class command is refused against a
loopback server that IS listening, while the same argv without the posture is served and the
server keeps serving afterwards — the control lives in the test body, so a harness that never
came up turns the measurement red rather than green. R68 PASSED and R-0563 is marked done. This
completes the build work; only the integration gate and closure remain.

## Next Steps
1. The integration gate: the full suite per docs/agents/integration_gate.md, the first of the two
   full-suite runs this feature owes.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the
   STATUS line authored by the reviewer, and the PR the operator merges at the next Open PR Gate.
END-PLAN24F

BEGIN-PLAN24T
## Current Step
R70, this round: the INTEGRATION GATE, the first of the two full-suite runs this feature owes.
The branch suite and a merge-base suite run sequentially under restored parity, every branch-only
failure is attributed by direct evidence, and the comparison is REPORTED rather than predicted.
R69 PASSED: the denied fetch is now measured against a really listening server, with its control
in the same test body. No source file, no test and no document is touched this round.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the STATUS
   line authored by the reviewer, and the PR the operator merges at the next Open PR Gate.
END-PLAN24T

BEGIN-RECORD38

Gate: R70 — the R69 entry. R69 PASSED with no finding registered against it. Every one of R69's nine
ordered gates was re-taken by the reviewer over 1df91b27..126b70ae rather than read from the handback,
except the two readings that exist only while a round is running — `git status --porcelain` after each
intermediate commit, and the absence of `.agent/STOP` at the two points R69's constraint 2 names —
which are unobservable once the round has ended and are accepted on the worker's report. Every value
the reviewer could re-measure equals the one the handback reports. LINE COUNTS ARE `splitlines`
COUNTS. TRANSPORT HELD, disk-to-disk with
no digest fallback: the committed `.agent/authored/f085-r69.md`, the committed `.agent/last_block.md`
at 126b70ae and both working copies at 126b70ae are all four byte-EQUAL at sha256
3b506bf1f24540e5ed8fe84ac7487b67041b17da43b02b0d869d08305d893dc3, 27901 B, 420 lines, 12 marker
lines; TOTAL 420 against the 490 cap, PROSE 241 against 400, RECORD37 40 against 140. THE SHAPES HELD,
one reading per pair. PLAN23F→PLAN23T over `.agent/plan.md` at cc563f6d reads `TO contains FROM:
false`, FROM 1x pre-commit and 0x post-commit with TO exactly 1x post-commit, and re-applied
reproduces the post-commit blob BYTE-EXACTLY. RECORD37 over `.agent/live_review.md` at 4651069b
satisfies ORDERED EQUALITY on every clause — PREFIX, SUFFIX, `pre + slice` equal byte for byte, and
that commit's ADDED lines equal to the slice's lines IN ORDER, 40 and 40. The two edits C3 made to
`tests/orchestration/test_exec_guard.py` at b735eb93 reconstruct BYTE-EXACTLY from that commit's
pre-commit blob by applying `IMPORTSF`→`IMPORTST` and then concatenating `NETTEST`, with IMPORTSF 1x
pre-commit and 0x post-commit, IMPORTST exactly 1x post-commit, and NETTEST an exact SUFFIX of the
post-commit blob. Marker LINES at 126b70ae are 0 in all three edited files. THE SUITES WERE RE-RUN,
NOT READ, in the primary checkout, serially, each exit 0: `44 passed` for
`tests/orchestration/test_exec_guard.py` at 126b70ae, `2 passed, 42 deselected` for the same file
filtered to the two tests C3 added — so those two are exactly the file's growth and the other 42 are
the ones that predate them — `160 passed` for the four state readers, and the canary `42 passed`. BOTH LINT HALVES printed `All checks passed!` over that test file at 126b70ae, the preview
half included. THE PLAN CONTRACT HELD at cc563f6d: 39 lines against the 50-line cap, with `## Goal`,
`## Next Steps` and a roadmap F-id all present. THE ARITHMETIC MOVED AS THAT BLOCK'S CONSTRAINT 9
REQUIRED: 178 registered / 30 done / 0 landed and 148 open at 1df91b27 against 178 / 31 / 0 and 147
open at 126b70ae, the registered and landed symmetric differences both EMPTY, the done symmetric
difference exactly {R-0563}, and 0 duplicate ids and 0 orphan resolutions at both SHAs.

THE RED CONTROL WAS RE-RUN BY THE REVIEWER'S OWN HAND, inside a disposable worktree at 126b70ae and
never in the primary checkout. The ordered byte string occurs exactly 1 time in
`packages/orchestration/exec_guard.py` at 126b70ae; mutating only its `deny_network` argument moves
the bare `deny_network=True,` count in that file from 2 to 1, leaving the untouched `dod-process`
occurrence beside one `False`. The two selected tests then FAIL: the guarded child comes back
`returncode=0` carrying `REMEDY_EXEC_GUARD_SERVED_BODY` in its stdout, and the refusal assertion reads
`assert b'Connection refused' in b''`. That is the exact opposite of the green reading, which is what
makes the green attributable to the deny posture rather than to a harness that never came up. The
worktree was removed and `git worktree list` is one line.

THE RECORD ITSELF WAS RE-MEASURED, which is the obligation R66 and R67 failed. Every mechanically
checkable claim RECORD37 makes about R68's range was re-run at the SHA it names, and all of them hold
— including the clause that R-0563 exists to police: at a8ba453d the bare word matches 4 lines of
`packages/runtimes/dev_server.py` under the case-insensitive reading R68's own `git grep -ic` command
ran, while the phrase `spawn unsupervised` matches none there, and `docs/agents/planner_reviewer_prompt.md`
contains no occurrence of `unsupervised` at a8ba453d or at 1df91b27. The `.agent/live_review.md` blob
at a8ba453d is a byte-exact PREFIX of the blob at 1df91b27, so nothing landed was overwritten. The
history over 1df91b27..126b70ae is six single-parent commits inserting 420, 349, 8, 40, 104 and 81
lines, none over 500, with no amend, rebase, reset or force-push in the reflog, and the branch is in
sync with its remote.

R69 REGISTERED NOTHING AND RESOLVED NOTHING, so this entry carries no registration line and no
resolution line of its own: the open set stays 147 and the next free id stays R-0564.
END-RECORD38
