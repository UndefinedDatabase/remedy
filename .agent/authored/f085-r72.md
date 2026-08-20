── STEP T003 closure run 2 — re-gate and settle the count — F085 — R72 ───────

Goal: re-run the INTEGRATION GATE now that R71's repair has landed, resolve R-0564 with
reviewer-authored text, register the reviewer's own arithmetic defect as R-0566, and settle the
open-findings counting rule as a DECISION so it cannot recur. R71 PASSED; the gate comparison R70 took
is stale because a repair landed after it, which is the whole reason this round re-takes it.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 record the R71 PASS and register R-0566 · C3 replace the `Landed:` line with the authored `Done:`
text · C4 append DECISION F085 D7 · C5 the gate evidence dir · C6 handback.

CONVENTION, binding on every count here, carried verbatim in force from the R71 block. A line count is
the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and NO
joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIRS ARE PLAN26 AND LANDED. ITS
END-OF-FILE APPENDS, WHICH HAVE NO FROM AT ALL, ARE RECORD41 AND DECISIOND7 — listed rather than
counted, per §3 checklist item 11. Each append slice CARRIES ITS OWN LEADING BLANK LINES, so the
separation its target's convention requires is a property of bytes that were measured and never of a
join shape that was reasoned about.

## Change

C1 applies PLAN26F→PLAN26T to `.agent/plan.md`, rewriting the `## Current Step` section and the WHOLE
`## Next Steps` list — the whole list, per §3 checklist item 17. C2 appends RECORD41 to the END of
`.agent/live_review.md`. C3 applies LANDEDF→LANDEDT to `.agent/live_review.md`, replacing the
worker-authored `Landed: R-0564` paragraph with the reviewer-authored `Done: R-0564` paragraph. C4
appends DECISIOND7 to the END of `.agent/decisions.md`. C5 creates `.agent/gate_f085_r72/` and commits
only the files G4 names there; raw run logs are NOT committed.

Change set, named rather than counted: `.agent/authored/f085-r72.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`, the files under
`.agent/gate_f085_r72/` that G4 names, and `.agent/handoff.md`. Nothing else. NO `docs/**` path is in
that set, so no docs suite is ordered and Rule A4 is untouched. NO `.py` path is in it, so NO lint gate
is ordered — a consequence of the change set, not an omission. NO file under `packages/`, `apps/` or
`tests/` is touched, so NO red control is ordered either: this round measures and records, and it
introduces no new assertion to prove falsifiable. Every TRACKED path named in a gate below was resolved
with `git ls-tree f023e2b1`, one call per path, before emission, per checklist item 24, and all exist;
`apps/ui/node_modules` and `apps/ui/dist` are gitignored build artifacts that `git ls-tree` reports
absent BY DESIGN, which is why G4 orders them COPIED into the base worktree rather than expected there,
and the reviewer confirmed both exist in the primary checkout at f023e2b1 with `ls -d`.
`.agent/authored/f085-r72.md` and everything under `.agent/gate_f085_r72/` are the paths no gate reads
at the base, because C0a and C5 create them.

WHY C3 IS A REPLACEMENT AND NOT AN APPEND. docs/agents/planner_reviewer_prompt.md §4 item 4 rules that
the reviewer "replaces the `Landed:` line with the authored `Done:` text at the next gate". A `Landed:`
line is a worker's record of an UNREVIEWED fix, written precisely so a session that dies between the
fix and its review leaves a state no reader can mistake for a resolution; once the reviewer has
verified the fix, that line has done its job and the resolution takes its place. This is the ONE class
of landed text in `.agent/live_review.md` this workflow overwrites, and it is overwritten because the
governing document says so — every other line in that file is append-only, which constraint 6 keeps.

WHAT THIS GATE IS AND WHAT IT IS NOT, unchanged from R70. The integration gate does not ask whether the
suite is green. It asks whether THIS BRANCH made anything worse than its merge base, which is a
COMPARISON and never a colour — so no expected exit code, no expected pass count and no expected
failure count is ordered anywhere below. Both sides are reported as measured. R70's own gate is on disk
under `.agent/gate_f085_r70/` and its branch-only list held exactly one id, the one R71 repaired; this
round's comparison stands on its own readings and inherits no number from that one.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r72.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C6; if it exists, finish the commit in
   flight, write the handback and stop. `git status --porcelain` is empty at round start and after
   every commit.
3. PAIR SHAPES. The reviewer ran the containment test at emission against each target's blob at
   f023e2b1 and prints its own output here per checklist item 15, one reading per pair:
   PLAN26F→PLAN26T `TO contains FROM: false`; LANDEDF→LANDEDT `TO contains FROM: false`. Both are
   therefore REWRITES and each owes the FROM 0x / TO 1x reading over its own post-commit file. Each
   FROM occurs EXACTLY 1x in its target at f023e2b1 — the reviewer measured both.
4. RECORD41 AND DECISIOND7 HAVE NO FROM. Do not invent one for either and do not report a FROM count
   for either. Each is appended at the END of its own target in its own commit and owes the ORDERED
   EQUALITY of §4.9 as R-0531 narrows it: pre-commit blob a byte-exact PREFIX, slice an exact SUFFIX,
   and that commit's ADDED lines exactly the slice's lines IN ORDER.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record, the resolution, the decision and the gate
   evidence. Only C0a and C0b may precede it. This round writes to the finding ledger, so §3 checklist
   item 23 binds it.
6. NOTHING IN `.agent/live_review.md` THAT ALREADY EXISTS AT f023e2b1 IS EDITED, MOVED OR DELETED,
   WITH EXACTLY ONE EXCEPTION: the `Landed: R-0564` paragraph that LANDEDF names, which C3 replaces for
   the reason stated above. Nothing in `.agent/decisions.md` that already exists at f023e2b1 is edited,
   moved or deleted — DECISION F085 D6's own correction section is the precedent this follows, and D6
   itself stays byte-verbatim.
7. Every sentence in RECORD41 and in LANDEDT that states a reading of a file names the SHA it was read
   at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches
   to EVERY reading in the clause, not only the first.
8. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD41, LANDEDT and DECISIOND7 are all reviewer
   text. Do not add a `Landed:` line, do not add a `Done:` paragraph of your own, and do not edit any
   of the three to reconcile them with anything you measure. A disagreement between them and your own
   reading is a finding to REPORT in the handback, never to fix — the rule that caught R66, R67 and, in
   R71, an arithmetic error of the reviewer's own that this round registers as R-0566.
9. THIS ROUND REGISTERS ONE AND RESOLVES ONE, AND THE COUNT IS COMPUTED THE WAY DECISIOND7 RULES:
   OPEN = REGISTERED − DONE, and a `Landed:` line is NOT a resolution. Registered moves 180 → 181,
   done moves 31 → 32, landed moves 1 → 0 because C3 converts the one landed line into a resolution,
   and open stays 149 at both SHAs — one finding resolved and one registered in the same round. The
   next free id becomes R-0567. RECORD41 carries exactly one `- R-` registration line and no `Done:`
   line; LANDEDT carries exactly one `Done:` line and no `- R-` line. G6 proves all of it.
10. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as its correction section fixes the ruled figure:
   490 lines TOTAL, PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all
   three on the final bytes at emission. The worker re-measures all three from the committed
   `.agent/authored/f085-r72.md`; a mismatch is a finding against this block, not the worker.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and its
   output, and push what is committed. Never edit a slice to make a gate green, never delete or skip a
   test, and never widen the change set to route around a red. G4 is the one gate below whose non-zero
   exit is EXPECTED to be possible and is not by itself a red — read G4's own text for what blocks.
12. RUN THE SUITES SERIALLY, one pytest process at a time, never alongside another in any checkout or
   worktree. THE BRANCH RUN AND THE BASE RUN ARE SEQUENTIAL, never concurrent, even though they live in
   different checkouts. `-n auto` parallelism INSIDE one pytest process is what the gate procedure
   orders and is not what this constraint bars.
13. RUN LOGS ARE WRITTEN OUTSIDE THE REPO'S TRACKED TREE WHILE A SUITE RUNS, to the gitignored scratch
   dir `.remedy-wt/.cache/gate_r72/`, and are copied into `.agent/gate_f085_r72/` only after the run
   exits (R-0176). Evidence files are named `.txt` and never `.log` (R-0169). The raw full logs stay in
   scratch and are NOT committed; `full_log_provenance.txt` records their line count and sha256.
14. THE BASE WORKTREE IS CREATED ON A THROWAWAY BRANCH AND NEVER DETACHED (DECISION D3): the
   self-dogfood branch guard refuses a detached HEAD by design. Remove the worktree, delete the
   throwaway branch, and prove `git worktree list` is one line at the end. Never commit in it.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit. The base worktree G4 creates is removed before C6; `git worktree
list` is one line at round start and one line at the end.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r72.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each. Also report the block's TOTAL, PROSE and RECORD41 line counts read
from that committed file, against constraint 10's 490 / 400 / 140, where PROSE is TOTAL minus the
slice lines.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN26F→PLAN26T is a REWRITE over `.agent/plan.md` at C1: report FROM 0x and TO exactly 1x over the
   post-commit blob, and re-applying the extracted FROM→TO to the pre-commit blob must reproduce the
   post-commit blob BYTE-EXACTLY.
 - RECORD41 at C2 over `.agent/live_review.md`: report the ordered-equality readings constraint 4
   names — PREFIX, SUFFIX, `pre + slice` equal byte for byte, and that commit's ADDED lines exactly the
   slice's lines IN ORDER.
 - LANDEDF→LANDEDT is a REWRITE over `.agent/live_review.md` at C3: report FROM 1x pre-commit and 0x
   post-commit with TO exactly 1x post-commit, and re-applying the extracted FROM→TO to C3's OWN
   pre-commit blob must reproduce its post-commit blob BYTE-EXACTLY. Measure against C3's pre-commit
   blob, never against C2's.
 - DECISIOND7 at C4 over `.agent/decisions.md`: the same ordered-equality readings as RECORD41,
   measured against C4's own pre-commit blob.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0. Count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 THE INTEGRATION GATE, per docs/agents/integration_gate.md, run BEFORE C5 so C5 commits its results.
Every number below is REPORTED, never predicted; no expected value is ordered for any of them. The
merge base is a5a70621 and it has not moved.
 - BRANCH RUN, in the primary checkout, from the repository root: `python3 -m pytest -n auto -q`, with
   stdout+stderr to `.remedy-wt/.cache/gate_r72/branch_run.txt`. Record exit code and wall seconds into
   `.agent/gate_f085_r72/branch_meta.txt` as `EXIT_CODE=<n>` and `WALL_SECONDS=<n>`. Copy the last 40
   lines of that log to `branch_run_tail.txt`. Write the sorted FAILED list to `branch_failed.txt` with
   `grep '^FAILED' ... | sort`.
 - BASE WORKTREE, per constraint 14: `git worktree add -b tmp/base-gate-r72 .remedy-wt/base-r72
   a5a70621`.
 - PARITY BEFORE THE BASE RUN, per the R-0155 amendment. COPY — never symlink — the primary checkout's
   `apps/ui/node_modules` and `apps/ui/dist` into the base worktree at the same relative paths. Set
   `REMEDY_UI_NO_AUTO_BUILD=1` for the base run but do NOT trust it alone: record BOTH a sha256 over
   the copied `apps/ui/dist` tree AND the mtime of `apps/ui/dist/index.html` BEFORE the base run and
   again AFTER it, into `.agent/gate_f085_r72/base_parity.txt`. A changed digest OR a moved mtime voids
   the parity claim — say so there and attribute every base-only failure per id instead of claiming
   parity. The mtime half is ordered because R-0565, registered at R71 from R70's own evidence, is
   exactly that the content digest is blind to a byte-identical rebuild while staleness is decided by
   mtime; this gate is the first to read the property that finding names.
 - BASE RUN, sequentially after the branch run has exited, inside that worktree, same command, log to
   `.remedy-wt/.cache/gate_r72/base_run.txt`; sorted FAILED list to `base_failed.txt`; its exit code
   and wall seconds appended to `base_parity.txt`.
 - COMPARE. `comm -13 base_failed.txt branch_failed.txt` → `comm_branch_only_failures.txt`, and
   `comm -23 base_failed.txt branch_failed.txt` → `comm_base_only_failures.txt`. Both files are
   committed even when empty. Report the line count of each.
 - ATTRIBUTION, into `.agent/gate_f085_r72/attribution.txt`, with ONE entry for EVERY id in BOTH comm
   outputs — no id may be silently absent. Re-run each branch-only id SERIALLY by its exact node id in
   the primary checkout and record the command, exit code and outcome. Classify: serial-pass ⇒
   xdist-flake class, recorded and not a blocker; serial-fail ⇒ re-run the same id in the base worktree
   and report whether it reproduces there. A branch-only id that fails serially, does NOT reproduce at
   the base, and touches this feature's code is a BLOCKER: stop under constraint 11, write the
   handback, and do not attempt a fix. Every base-only id is likewise attributed by direct evidence,
   naming the missing artifact per id where the environment class applies; an unattributed id there
   blocks the verdict. State explicitly whether
   `tests/test_command_discovery.py::TestNoShellTrue::test_run_tests_local_no_shell_true` — R70's only
   branch-only id — appears in either comm output this round.
 - PROVENANCE. `full_log_provenance.txt` records, for each raw log left in scratch, its path, its
   `wc -l` line count and its sha256, plus one sentence saying why the raw logs are not committed. Then
   remove the worktree and delete `tmp/base-gate-r72`.
 - WALL BUDGET. If the branch run exceeds ~5 minutes wall clock, say so in the handback as a note for
   a perf pass. That is a note and never a red.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 38 lines by applying the pair to that blob at f023e2b1.

G6 ARITHMETIC, computed as DECISIOND7 rules — OPEN = REGISTERED − DONE, and a `Landed:` line is NOT a
resolution and is never subtracted. Count the registered, done and landed id sets in
`.agent/live_review.md` at base f023e2b1 and at HEAD, from the line-start patterns for a registration,
a resolution and a landed line. The reviewer's base reading is 180 registered / 31 done / 1 landed,
149 open, max registered R-0565, max resolved R-0563. At HEAD the reading must be 181 / 32 / 0, still
149 open, max registered R-0566 and max resolved R-0564. The registered symmetric difference must be
EXACTLY `{R-0566}`, the done symmetric difference EXACTLY `{R-0564}`, and the landed symmetric
difference EXACTLY `{R-0564}`. Next free id R-0567. Report all three symmetric differences, the
duplicate-id count and the count of resolutions naming an unregistered id, at both SHAs. Report the
open count under BOTH formulas at both SHAs, so the record shows the rule DECISIOND7 settles and the
one it rejects side by side.

G7 CANARY, in the primary checkout and never in a worktree (R-0518), serially per constraint 12:
`python3 -m pytest tests/cli/test_golden_path.py -q` — exit 0. Report the passed count; the count is
reported, never predicted. The reviewer's own base reading at f023e2b1 was `42 passed`.

G8 HYGIENE. `git diff --name-only f023e2b1..HEAD` measured BEFORE C6 holds exactly the change set above
minus `.agent/handoff.md`, which C6 writes, and nothing else — and in particular holds no path under
`packages/`, `apps/`, `docs/`, `scripts/` or `tests/`, and no path ending in `.log`. Report the list.
Report per-commit insertions for every commit BEFORE C6 — C6 cannot measure itself, so its own go in
the round report — and confirm none exceeds 500. This branch spent the AGENTS.md declared-oversize
allowance at d4473f85, so a second oversize commit is a STOP under constraint 11, never a declaration;
if the gate evidence would push C5 over the cap, TRIM the committed tail files rather than the FAILED
lists and say so. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base SHA
f023e2b1, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3, C4,
C5 and C6, the real G1-G8 results with exit codes, the open-findings count and the next expected
action. The Bundle above holds more than five commits, so the ≤100-line cap AGENTS.md allows when a
per-commit table needs it applies; drop no section. G4's numbers belong in that table in full: both
exit codes, both wall times, both FAILED counts, both comm line counts, the parity digest AND mtime
readings, and the attribution verdict per id.
Repeat this Fortschritt line verbatim:
Fortschritt: ~100 % der Bauarbeit; der Regress aus R70 ist repariert und gegengeprüft, R71 PASS, und
das Integration Gate läuft in dieser Runde erneut, weil eine Reparatur nach einem Gate dessen Vergleich
entwertet. R-0564 ist aufgelöst, R-0566 registriert, die Zählregel als DECISION F085 D7 festgeschrieben.
Offen bleibt nur noch die Closure. Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: if G4 comes back
clean, R73 is CLOSURE per docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH review zip, the
reviewer-authored STATUS line, and the PR the operator merges at the next Open PR Gate; if G4 returns a
BLOCKER, R73 is the repair round for it instead and closure waits. TWO: R72 carries no verdict of its
own, because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4 item 13); R73 carries it. THREE: a standalone closing line
stating the open findings count under DECISION F085 D7's rule and the next free id. FOUR:
`Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires every
handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN26F
## Current Step
R71, this round: the repair the integration gate demanded. R70 PASSED and its gate found exactly
one real branch-only regression — `test_run_tests_local_no_shell_true` pinned a spawn site that
F085 T002b moved, so it failed on a property that still holds. The test is pulled to the new seam
and its two assertions are proved reachable by mutation. Registered as R-0564; the parity-digest
blindness the same gate surfaced is registered as R-0565. No production file is touched.

## Next Steps
1. Re-run the integration gate per docs/agents/integration_gate.md: a repair landed after a gate
   invalidates that gate's comparison, so the branch-versus-base reading is taken again.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the
   STATUS line authored by the reviewer, and the PR the operator merges at the next Open PR Gate.
END-PLAN26F

BEGIN-PLAN26T
## Current Step
R72, this round: the integration gate re-taken, plus the ledger work R71 left open. R71 PASSED —
its repair is verified and R-0564 is resolved by reviewer text here — and the reviewer's own
arithmetic slip in the R71 block is registered as R-0566 and settled as DECISION F085 D7: the open
count is REGISTERED minus DONE, and a `Landed:` line is an unreviewed fix rather than a resolution.
The gate is re-run because a repair landing after a gate makes that gate's comparison stale.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the STATUS
   line authored by the reviewer, and the PR the operator merges at the next Open PR Gate — unless
   this round's gate returns a blocker, in which case its repair round comes first.
END-PLAN26T

BEGIN-LANDEDF
Landed: R-0564 — the defeated no-shell test now spies on `subprocess.Popen`, delegating to the real
spawn, and asserts over every recorded spawn that no `shell=True` is present and that argv is a list;
`tests/test_command_discovery.py` only, in this round's C3.
END-LANDEDF

BEGIN-LANDEDT
Done: R-0564 — Resolved at R71, commit 3cf6788e, and verified by the reviewer at f023e2b1 rather than
read. The repaired test patches `subprocess.Popen` with a spy that DELEGATES to the real spawn and
asserts over every recorded call that no `shell=True` is present and that argv is a list, so it pins
the property at the seam the guard actually uses. The reviewer re-ran the file at f023e2b1 in the
primary checkout: `92 passed`, exit 0, against the base reading of `1 failed, 91 passed` at 6a04b37b,
and both ruff halves printed `All checks passed!` over it at f023e2b1. The fix is not merely green: the
reviewer proved BOTH of its assertions reachable by mutation inside a disposable worktree at 6a04b37b,
inserting `shell=True` into the guard's `Popen` call to make the shell assertion fail, and replacing
the guarded call with a fabricated `CompletedProcess` to make `assert spawns` fail on an empty list.
The new seam is strictly stronger than the one it replaces, which the reviewer also measured: reverting
`run_tests_local` to `subprocess.run` in that worktree left the test GREEN, because `subprocess.run` is
itself implemented on `Popen`, so the assertion now holds wherever the spawn is written and cannot be
defeated by moving it again. The counter-measure R-0564 names is therefore satisfied by construction
for this test rather than by vigilance. No production file was touched by the repair, because the
property was always true of the source and only the measurement had come loose.
END-LANDEDT

BEGIN-RECORD41

Gate: R72 — the R71 entry. R71 PASSED. Every gate its block ordered was re-taken by the reviewer over
6a04b37b..f023e2b1 rather than read from the handback, except `git status --porcelain` after each
intermediate commit and the absence of `.agent/STOP` at the two points R71's constraint 2 names, which
are unobservable once a round has ended and are accepted on the worker's report. TRANSPORT HELD,
disk-to-disk with the reviewer's OWN pre-emission original in the comparison and no digest fallback:
that original, the committed `.agent/authored/f085-r71.md`, the committed `.agent/last_block.md` at
f023e2b1 and both working copies at f023e2b1 are all five byte-EQUAL at sha256
9c87a93b587cfcef5db3ba28246f088439a61aad6587f9b3f8220513e31ba630, 29863 B, 408 lines, 12 marker lines;
TOTAL 408 against the 490 cap, PROSE 255 against 400, RECORD40 65 against 140. THE SHAPES HELD, one
reading per pair: PLAN25F→PLAN25T over `.agent/plan.md` at 17df8755 and NOSHELLF→NOSHELLT over
`tests/test_command_discovery.py` at 3cf6788e both read `TO contains FROM: false`, both show FROM 1x
pre-commit and 0x post-commit with TO exactly 1x post-commit, and both reproduce their post-commit blob
BYTE-EXACTLY when re-applied. RECORD40 at ea9e80b5 and the `Landed:` line at 2eb5d1f3 each satisfy
ORDERED EQUALITY against their OWN pre-commit blob — PREFIX, SUFFIX, `pre + slice` equal byte for byte,
ADDED lines equal to the slice's lines IN ORDER, 65 and 65 and then 4 and 4. Marker LINES at f023e2b1
are 0 in all three edited files. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout, serially,
each exit 0: `92 passed` for `tests/test_command_discovery.py` at f023e2b1 where the same file read
`1 failed, 91 passed` at 6a04b37b, `44 passed` for `tests/orchestration/test_exec_guard.py`, and the
canary `42 passed`. BOTH LINT HALVES printed `All checks passed!` over the repaired file at f023e2b1.
THE PLAN CONTRACT HELD at 17df8755: 39 lines against the 50-line cap with `## Goal`, `## Next Steps`
and a roadmap F-id all present. THE HYGIENE READING HELD: the range touches six paths, exactly one of
them under `tests/` and none under `packages/`, `apps/`, `docs/` or `scripts/`, over seven
single-parent commits inserting 408, 334, 9, 65, 25, 4 and 109 lines, none over 500.

- R-0566 — Medium — the R71 block's constraint 9 stated an open-findings count its own record text
contradicted, and the worker caught it. That constraint ruled "open moves 147 → 148" for a round that
registered two findings and marked one `Landed:`, deriving the number from OPEN = REGISTERED − DONE −
LANDED. But docs/agents/planner_reviewer_prompt.md §4 item 4 rules that a `Landed:` line is an
UNREVIEWED FIX and not a resolution — "a surviving `Landed:` line is an unreviewed fix, which is
exactly what it should look like" — and RECORD40, authored in the same block, closes R-0564's
registration paragraph with `OPEN.`. So the block asserted a finding was not open in the same breath as
its own ledger text asserted it was, and the correct reading at f023e2b1 is 181 minus 32, that is 149.
The formula was never wrong before because `landed` was 0 at every SHA this feature had measured until
R71, so the two readings agreed everywhere they had been exercised and the defect was latent in every
block that carried it. Medium, not High, because no false number reached `.agent/live_review.md` — the
R71 worker declared the disagreement under that block's constraint 8 and reported BOTH readings in the
handback rather than reconciling them, which is the third round in this feature that rule has caught a
reviewer error. Not Low, because the count is what a closure round reports and what the next session
reads first. COUNTER-MEASURE: DECISION F085 D7, appended to `.agent/decisions.md` by this round's C4,
rules the formula on disk instead of leaving it to be re-derived per block, and G6 of this block is the
first gate written under it — it orders BOTH formulas reported side by side at both SHAs, so the rule
and the reading it rejects are visible together in the record rather than one silently replacing the
other. OPEN.
END-RECORD41

BEGIN-DECISIOND7

## DECISION F085 D7 — the open-findings count (2026-08-19)

CHOSEN. The open-findings count over `.agent/live_review.md` is OPEN = REGISTERED − DONE, where
REGISTERED counts lines matching `^- R-\d+ — ` and DONE counts lines matching `^Done: R-\d+ — `. A
`Landed: R-\d+ — ` line is NOT a resolution and is NEVER subtracted: docs/agents/planner_reviewer_prompt.md
§4 item 4 defines it as a worker's record of an UNREVIEWED fix, written so that a session dying between
a fix and its review leaves a state no reader can mistake for a resolution, and the reviewer replaces
it with authored `Done:` text at the next gate. A finding whose fix has landed but has not been
reviewed is therefore OPEN, and it stops being open when the reviewer says so and not when the worker
does. Finding R-0566 registers the defect this settles.

ALTERNATIVE CONSIDERED and rejected: OPEN = REGISTERED − DONE − LANDED, which several blocks of this
feature carried in their arithmetic constraints. It is undetectable while no `Landed:` line exists —
which was true at every SHA this feature measured before R71 — and it silently closes a finding on the
worker's authority, which is precisely the authority §4 item 4 withholds. It was never a considered
choice; it was an unexamined formula, which is why it is written down now rather than argued about
again.

CONSEQUENCE. A round that lands a fix without a reviewer resolution does not reduce the open count, so
the count stops moving until review happens — which is the honest reading and is meant to be visible.
Blocks that state an expected open count state which formula produced it. Where a round both registers
and resolves one finding, the count is unchanged and that is not an error.

Reverse this decision by deleting this section, which returns the formula to whatever each block
asserts and restores the ambiguity R-0566 was registered for.
END-DECISIOND7
