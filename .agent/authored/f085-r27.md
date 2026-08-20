── STEP T002b paydown — F085 — R27 ───────────────────────────────────────────

Goal: record the R26 PASS and register the one finding it produced — a pointer
the reviewer's own R26 block left out of its Handback section, which that round's
handoff then inherited. Then close the session cleanly.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record
R26 and register R-0517 · C2 plan · C3 handback.

This is the session's LAST round, reached at the declared cap of two authored
rounds and not at a blocker. No production code is touched: every path in the
change set is under `.agent/`.

## Why this round exists — read before C1

R26 passed on every gate. The defect it exposed is on the REVIEWER's side of the
line: docs/agents/self_drive_protocol.md §Phase 2 requires that a handoff naming
the next session's first action name Phase 1 rule 1 — re-read `.agent/STOP` from
disk — BEFORE rule 2, the Open PR Gate. R25's handoff carried that sentence and
R26's does not, because the R26 block enumerated the handoff's mandated contents
and omitted it. The worker wrote exactly what it was told to write.

That is why R-0517 is registered here rather than mentioned and dropped: a
reviewer defect that lives only in a chat window is the A1 trap, and the next
session is the party that pays for it.

R-0517 is NOT resolved this round. Its fix lands in this round's own handback,
which is the LAST commit, so a `Done:` paragraph committed before it would claim
an outcome that does not yet exist on disk. The next reviewed round authors the
resolution after reading the handback the fix produced.

## Change

C1 — `.agent/live_review.md`, one commit, RECORD2 appended and nothing else.
RECORD2 carries both the R26 gate entry and the R-0517 registration, in that
order, as one slice — the shape R25's C1 already used.
C2 — `.agent/plan.md`, one commit, the PLANF2→PLANT2 pair. Containment was tested
mechanically: PLANT2 does not contain PLANF2, so the pair is a REWRITE. The FROM
spans the whole `## Current Step` and `## Next Steps` region, so the numbered list
is renumbered by the pair itself rather than left half-edited.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r27.md` by its marker pair. Never retype a
   slice and never apply one from this prompt directly. Marker lines never reach
   a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C3. If it exists,
   finish the commit in flight, write the handback and stop.
3. `git status --porcelain` is empty at round start and after every commit; any
   destructive check runs ONLY in a disposable `git worktree` under `.remedy-wt/`,
   removed and pruned before the handback. Use absolute paths: a `cd` into a
   worktree persists across commands and makes later readings describe the wrong
   tree.
4. C1 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD2. Do not reflow, re-wrap or re-indent it.
5. Nothing outside the declared change set is touched. This round resolves no
   finding, so the `Done:` count must come out unchanged.
6. If any gate comes out red, or PLANF2 does not match at exactly one place,
   STOP: write the handback naming the exact command, its exit code and its
   output, and do not improvise a repair.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 2;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line at the handback.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r27.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report the sha256,
the byte count, the line count, the number of marker lines, and region digests
over the line ranges 1-60, 61-140 and 141-end.

G3 APPEND SHAPE for C1. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank line
plus RECORD2; RECORD2's first line occurs once among the lines that commit's diff
ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker
LINES, never the substring, because `APPEND-shaped` already appears in that file's
prose and a substring count reports it. Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in
`.agent/live_review.md` at base 369d94a3 and at HEAD. The reviewer's base reading
is 131 registered / 14 done / 0 landed, 117 open; at HEAD it must be 132 / 14 / 0
with 118 open. Report the registered symmetric difference (it must hold exactly
R-0517), the done and landed symmetric differences (both empty), the count of
duplicate ids, the count of resolutions naming an unregistered id, the maximum id
and the next free id.

G5 PLAN PAIR. PLANF2 occurs 0 times at HEAD and PLANT2 exactly once. `## Goal` and
`## Risks` are byte-IDENTICAL to their base bytes. Report `.agent/plan.md`'s
sha256, its byte count, a line count under 50, and the numerals its `## Next
Steps` list parses to rather than a count of them.

G6 STATE READERS AND CANARY, because this round rewrites `.agent/` state and
changes no `.py`: `python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -q` exits 0, base reading `158 passed`;
that suite spawns wrapper processes under flock and is timing-sensitive, so report
the count as a READING. CANARY: `python3 -m pytest tests/cli/test_golden_path.py
-q` exits 0, base reading `42 passed`. No ruff gate and none skipped by oversight:
the change set contains no `.py` file. No docs gate: nothing under `docs/` changes.

G7 COMMIT HYGIENE. `git diff --name-only 369d94a3..HEAD` measured BEFORE C3 holds
exactly these paths and nothing else, named rather than counted:
`.agent/authored/f085-r27.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`. Report per-commit insertions for every commit BEFORE C3 — C3
cannot measure itself, so report its own insertions in the round report instead —
and confirm none exceeds 500. Confirm every commit has exactly one parent and that
`git reflog -12` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, base SHA, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2 and C3, the real verification results for G1-G7 with
exit codes, the open-findings count, and the next expected action. Repeat this
Fortschritt line verbatim:
Fortschritt: ~80 % (T001 gebaut · R13-R26 PASS · T002a KOMPLETT · T002b: Seam
gebaut, `test_runner` + `autorun` migriert · T002b Rest, T002c-d, T003 offen) —
Schätzung.

The handback MUST state, in its `## Next` section, that the next session's first
action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the
Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). That sentence is the fix R-0517 names;
omitting it repeats the finding in the same round that registers it. Also state
that R-0517 is OPEN and awaits the next reviewed round's authored resolution, and
that R27's own verdict is NOT a §4.13 terminator — this branch continues, so the
next reviewed round records R27's gate entry in `.agent/live_review.md`.

Then `git push -u origin feature/f085-sandbox-hardening`. Create no PR and merge
nothing.

BEGIN-RECORD2
Gate: R26 — PASS, the round that carried T002b into `autorun.py` and moved its
three `test`-class sites onto the shared seam. All ten ordered gates were re-run
by the reviewer over 5b02cff9..369d94a3 and every one reproduces the handback's
reading. TRANSPORT HELD ACROSS A HALT AND A RE-CREATION: the worker stopped
before C0a because the block ordered a 312-line save while the delivered text
measured 313, committed nothing and left the tree byte-clean at 5b02cff9. The
reviewer re-measured its own source in halves, confirmed 313, and traced 312 to
hand-summed section counts taken after a late edit to three sections — an
arithmetic recollection standing in for a measurement, which is the defect the
gate caught and the reason the gate exists. The worker's two independent
transcriptions produced the identical sha256
4220f7db082fd722fa28163fdbdfe2684f6c0ec42d772c866106009c26402908 at 16616 B, and
at HEAD the committed authored file, the committed `.agent/last_block.md` and both
working copies are byte-EQUAL at that digest, 313 lines, 26 marker lines in 13
pairs, region digests 9a91a0ce, 41d355bc and e34ff2fa. THE APPEND COMMIT HOLDS
ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the post-commit file,
the remainder is exactly one blank line plus RECORD1 at numstat 35/0, and no
marker line reached any target file — the three `END-` hits in
`.agent/live_review.md` are the word `APPEND-shaped` in prose older than this
round, which a substring count reports and a line-anchored count does not. THE
ARITHMETIC IS FLAT EXACTLY WHERE IT WAS ORDERED FLAT: 131 / 14 / 0 with 117 open
at base and identical at HEAD, all three symmetric differences empty, no duplicate
id, no resolution naming an unregistered id, max R-0516. THE MIGRATION CHANGED
THE MECHANISM AND NOT THE OUTCOME: `subprocess.run(` occurs 0 times at HEAD having
occurred 3 times at base, each of the five FROM texts 0 times and each TO exactly
once, `run_guarded_test_command` 5 times as three call sites plus two imports,
`import subprocess` still present in `_run_fixture_builder` for its `except
subprocess.TimeoutExpired` clause and gone from `_run_repair_loop_fixture` where
nothing else used it. THE MIGRATED CODE SITS ON AN EXECUTED PATH, PROVEN FROM
OPPOSITE ENDS: the reviewer broke the three bare spawns at BASE before authoring
and the round gate reported 18 failures; the worker broke the SEAM at HEAD inside
a disposable worktree and the same command line reported 18 failures spanning both
driving files. The same number from both directions is what a preserved call graph
looks like. THE GATES WERE RE-RUN, NOT READ: the round gate exited 0 with
`140 passed, 6 skipped` and the migration did not move it, the guard suite
`24 passed`, the four state readers `158 passed`, the canary `42 passed` and ruff
`All checks passed!`, each as its exact ordered command line. COMMIT HYGIENE IS
CLEAN: the changed-path set before C4 is exactly the five declared paths,
per-commit insertions are 313, 258, 35, 12 and 5 with C4's own 85 measured after
it existed and none over 500, six commits form a single-parent chain, and the
reflog holds only `commit:` entries. Both deviations are declared, the D15 overage
names its own measured length, and neither widens scope. No block condition is met.

- R-0517 — Low, A BLOCK'S HANDBACK SECTION DROPPED A POINTER THE PROTOCOL
REQUIRES, AND THE HANDOFF INHERITED THE GAP. docs/agents/self_drive_protocol.md
§Phase 2 requires that every handoff naming the next session's first action names
Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR
Gate. R25's handoff carried that sentence. R26's does not, because the R26 block's
Handback section enumerated what the handoff must contain and left it out. The
worker is not at fault: it wrote what the block ordered, which is the shape this
record keeps finding on the reviewer's side of the line. Low because nothing
executable depends on it and no gate could have gone red over it — the whole cost
lands on the next session, which opens a handoff telling it to re-run gates and
saying nothing about the sentinel that can halt a round before it starts, nor
about the PR gate that must precede any new branch. It is registered rather than
waved through because the reviewer authored the omission, and a reviewer defect
spoken aloud only in a chat window is exactly the A1 trap this record exists to
close. No checklist item is added: the requirement already lives in the protocol,
so the fix is that this round's own handback carries the sentence and every later
block's Handback section names it among the mandated contents. OPEN.
END-RECORD2

BEGIN-PLANF2
## Current Step
R26, this round: record the R25 PASS and continue T002b by moving `autorun.py`'s
three `test`-class sites onto `run_guarded_test_command`. Every one of them reads
only `returncode`, so the seam's bytes streams change nothing they observe, and
real children already drive both fixture paths in the suite the round gate re-runs.

## Next Steps
1. T002b continued — the `test`-class sites still on a bare spawn, ending with
   `test_execution_service.py`'s `Popen`, which takes the child half via
   `plan_child_spawn` rather than the runner and which carries R-0202.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANF2

BEGIN-PLANT2
## Current Step
R27, this round: record the R26 PASS and register R-0517 — the reviewer's own R26
block under-specified its Handback section, so that round's handoff dropped the
next-session pointer the self-drive protocol requires. The session's declared cap
of two authored rounds is reached here, not a blocker.

## Next Steps
1. T002b continued — the `test`-class sites still on a bare spawn, ending with
   `test_execution_service.py`'s `Popen`, which takes the child half via
   `plan_child_spawn` rather than the runner and which carries R-0202.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANT2
