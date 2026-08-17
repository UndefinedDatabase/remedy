── STEP T002b paydown — F085 — R25 ───────────────────────────────────────────

Goal: record the R24 PASS, register the one finding it produced — a stale claim
the reviewer's own R24 block failed to sweep out of a file that block edited —
and retire that claim in the same round. Then close the session cleanly.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1
record R24 and register R-0516 · C2 retire the stale claim · C3 resolve R-0516 ·
C4 plan · C5 handback.

This is the session's LAST round, reached at the declared cap of two authored
rounds and not at a blocker. No production code is touched: the only change
outside `.agent/` is a docstring that asserts something false.

## Why this round exists — read before C2

`tests/orchestration/test_exec_guard.py` opens with "The guard has NO callers in
this repository, so nothing here says anything about whether any existing Remedy
subprocess is limited. It is not." That was true when T001 wrote it. It stopped
being true at T002a, when the managed builder seam and the CLI provider became
callers, and R24 made it doubly false by adding `test_runner`. R24's own C2
EDITED that file and swept the sibling claim in `exec_guard.py`'s PARTIAL
COVERAGE bullet — so the block reached the instance it happened to notice and
left the one in the file it was editing, which is the R-0417 staleness shape the
record already names.

A false sentence in a test file is worth a round: it is read by whoever next asks
what the guard covers, and it answers with the opposite of the truth.

## Change

C2 — `tests/orchestration/test_exec_guard.py`, one commit, the DOCF→DOCT pair
below applied to the module docstring and NOTHING else in the file. The pair is a
REWRITE: the reviewer tested containment mechanically and DOCT does not contain
DOCF. The replacement does not substitute a new count for the old claim — it
points at where the migration state actually lives, so it cannot go stale the
same way.

## Constraints

1. SINGLE-SESSION rules do NOT apply: this round is gated by the reviewer like
   every other. The change set is `.agent/**` plus one file under `tests/`, so no
   production code path is self-certified.
2. AGENTS.md in full: the self-review loop before EVERY commit, one logical step
   per commit, `.agent/plan.md` current before committing, a clean tree, the push,
   the handoff rewrite. Commit subjects carry no leading-slash token and no path.
3. C1 lands BEFORE C2. The verdict record and the registration persist first, so a
   session that dies mid-round still leaves both on disk.
4. C3 lands AFTER C2, and G5 is RUN in between — after C2 is committed and before
   C3 is committed. DONE1 states both that the claim is already retired and that
   G5 verified it, and checklist item 19 binds a block that orders such a
   sentence to schedule its producer: a gate result may be asserted only by a
   slice the block commits after that gate has run. Report G5's reading at the
   point it is taken, not only at the end of the round.
5. The authored slices — RECORD1, DOCF, DOCT, DONE1, PLANF, PLANT — are extracted
   programmatically from the COMMITTED `.agent/authored/f085-r25.md` by their
   one-line markers and applied byte-verbatim. Never retype them, never source
   them from `.remedy-wt/`, and let no marker line reach a target file.
6. Pair shapes, classified mechanically before this block was emitted, one reading
   per pair: DOCT contains DOCF — False, a REWRITE. PLANT contains PLANF — False,
   a REWRITE. Both therefore carry a legitimate "FROM 0x at HEAD" gate. RECORD1
   and DONE1 are not pairs: each is an APPEND of a new paragraph at the end of
   `.agent/live_review.md`, so each is proved by a prefix proof and no `0x`
   reading is ordered for either.
7. Destructive verification, if you run any, happens ONLY inside a disposable
   `git worktree` under `.remedy-wt/`, removed and pruned before the handback. The
   primary checkout satisfies `git status --porcelain` == empty at every commit
   and at the handback.
8. The 500-line cap counts INSERTIONS — the first column of `git show --numstat` —
   never the churn total `git show --stat` prints.
9. If any gate comes out red, or if this block contradicts itself or the code,
   finish the commit in hand, record the contradiction in the handback and END.
   Do not guess and do not widen scope to route around it.

## Done when

G1 STOP AND TREE. Re-read `.agent/STOP` from disk before C0a and again before C5
and report both readings; if it exists at either point, finish the commit in
hand, write the handoff and END. `git status --porcelain` is empty at round start
and after every commit. Report `git worktree list`'s line count at the handback.

G2 TRANSPORT. The committed `.agent/authored/f085-r25.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL. Report the sha256,
the byte count, the line count and the number of marker lines. Then report the
sha256 of each of these regions of the saved file, measured by the reviewer
before delegating: lines 1 through 60, lines 61 through 140, and line 141 to the
end. Three matching digests show a split write changed nothing.

G3 APPEND SHAPE, for C1 and again for C3. The pre-commit blob of
`.agent/live_review.md` is a byte-exact PREFIX of the post-commit file; the
remainder is exactly one blank line followed by the slice; the HEAD blob equals
the working copy; the slice's first line occurs exactly ONCE in the whole file;
the file carries 0 marker lines. Report the `git show --numstat` pair for each as
a READING, insertions being the FIRST column.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `,
`^Done: R-\d+ — ` and `^Landed: R-\d+`. At base 3d1821bf the reading is
130 / 13 / 0 with 117 open. After C1 expect 131 / 13 / 0 with 118 open — the
registration must LAND before the fix. At HEAD expect 131 / 14 / 0 with 117 open.
Report the reading at all three points, both symmetric differences — each exactly
R-0516 — the duplicate-id counts, any resolution naming an unregistered id, and
the max and next-free id.

G5 THE DOCSTRING PAIR. DOCF occurs exactly ONCE in
`tests/orchestration/test_exec_guard.py` at base and 0 times at HEAD; DOCT occurs
exactly once at HEAD. Report the file's sha256 and byte count at HEAD, and report
that the file's first line is unchanged from base — the pair rewrites a paragraph
inside the docstring, never the docstring's opening.

G6 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT exactly once. `## Goal` and
`## Risks` are byte-IDENTICAL to their base bytes. Report `.agent/plan.md`'s
sha256, its byte count, a line count under 50, and the numbers its `## Next
Steps` list parses to rather than a count of them.

G7 THE EDITED SUITE, run after C2: `python3 -m pytest
tests/orchestration/test_exec_guard.py -q` exits 0. The reviewer's base reading
is `24 passed`. Report the count as a READING. A docstring edit must not move it,
so report whether it did.

G8 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py
-q` exits 0; base reading `158 passed`, and that suite spawns wrapper processes
under flock and is timing-sensitive, so report the count as a READING. CANARY:
`python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
`42 passed`. No ruff gate is ordered and none is skipped by oversight: this change
set holds one `.py` file and the only edit in it is inside a string literal — run
`python3 -m ruff check tests/orchestration/test_exec_guard.py` anyway and report
it, since it costs nothing and the file is a `.py` file. No docs gate: nothing
under `docs/` changes.

G9 COMMIT HYGIENE. `git diff --name-only 3d1821bf..HEAD` measured BEFORE C5
equals the declared paths minus `.agent/handoff.md` — report the list and 0 paths
outside it. For C0a, C0b, C1, C2, C3 and C4 report the FIRST COLUMN of
`git show --numstat`; none exceeds 500. C5's own count is ordered nowhere, since a
commit cannot measure itself; report it in the round report instead. Report
`git log --format=%h %p 3d1821bf..HEAD` and confirm one parent each, and report
`git reflog -10` showing no amend, rebase, reset or force-push.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, a per-commit changed-files table, the item-status table covering
C0a, C0b, C1, C2, C3, C4 and C5 exactly once each, the real gate readings above,
the open-findings count, and the next expected action. Repeat this Fortschritt
line verbatim, estimate label included:

Fortschritt: ~78 % (T001 gebaut · R13-R24 PASS · T002a KOMPLETT · T002b: Seam
gebaut, 1 von 12 `test`-Sites migriert · T002b Rest, T002c-d, T003 offen) —
Schätzung.

The Next section states, in the protocol's own order, that the next session's
first action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2,
the Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`); that R25's own verdict is NOT a §4.13
terminator, because that clause covers the last round of a BRANCH and this branch
continues, so the next session's first reviewed round records R25's gate entry in
`.agent/live_review.md`; and that the first work item is the remaining
`test`-class sites, starting with the three in `autorun.py`, which share the
migrated shape exactly.

Then push the branch. Do not create a PR and do not merge anything.

BEGIN-RECORD1
Gate: R24 — PASS, the round that opened T002b by building the shared test-class
seam and migrating the first of the twelve sites onto it. All ten ordered gates
were re-run by the reviewer over f28ed65a..3d1821bf and every one reproduces the
handback's reading. TRANSPORT IS PROVEN DISK-TO-DISK AND NOT BY FALLBACK: the
committed `.agent/authored/f085-r24.md` is byte-EQUAL to the reviewer's own
pre-delegation original as well as to the committed `.agent/last_block.md` and
both working copies, at sha256
46db5e38c4b586971364f75b7976daa3ff88e20ac5558aa2d82b807698380340, 22645 B, 355
lines, and the three region digests 7804f388, 69d643fe and 7ac81591 reproduce
exactly, so the single write really was single and nothing shifted. THE APPEND
COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1, that
slice occurs once, no marker line reached any target file, and the HEAD blob
equals the working copy. THE ARITHMETIC IS FLAT EXACTLY WHERE IT WAS ORDERED TO
BE: 130 / 13 / 0 with 117 open at base and unchanged at HEAD, both symmetric
differences empty, no duplicate id, no resolution naming an unregistered id, max
R-0515. THE SEAM IS REAL AND SHAPED LIKE WHAT IT REPLACED:
`run_guarded_test_command` returns a `CompletedProcess` with bytes streams,
raises `subprocess.TimeoutExpired` on a wall trip CARRYING the partial streams
the guard already holds, republishes a signal death as a negative returncode, and
deliberately does not catch `FileNotFoundError`, which is why `run_tests_local`'s
`command_not_found` branch still works untouched. The policy sets only what it
can defend — `cpu_seconds`, `address_space_bytes` and `open_files` stay None on
the precedent `_builder_exec_policy` already established, rather than inventing a
second answer — and the 16 MiB output cap sits above the caller's own 1 MiB
truncation with the reason written beside the value, so `output_truncated` keeps
describing what the caller measured. THE MIGRATION CHANGED THE MECHANISM AND NOT
THE OUTCOME: every mocked call site in both test files moved onto the new seam
with its fabricated `CompletedProcess` values unchanged, and the one assertion
that could no longer fail — a `shell=` check against a seam with no `shell`
parameter — was REPLACED rather than retargeted, so it now pins the argv, the
timeout and the cwd the seam really receives. THE GOLDEN RUNS A REAL CHILD AND
REACHES THE MIGRATED PATH, which the reviewer confirmed independently rather than
accepting the worker's probe: with `run_guarded_test_command` made to raise on
entry in a disposable worktree at HEAD, the golden node stopped passing and
reported the injected error. THE GATES WERE RE-RUN, NOT READ: ruff over the five
changed files exited 0 with `All checks passed!`, the migrated suites gave
`119 passed`, the four state readers `158 passed` and the canary `42 passed`,
each as its exact ordered command line and each reproducing the handback's
number. COMMIT HYGIENE IS CLEAN: the changed-path set before C5 is exactly the
declared one, per-commit insertions are 355, 315, 46, 206, 62, 9 and 68 with none
over 500, seven commits form a single-parent chain, and the reflog holds nothing
but `commit:` entries. The three declared deviations are all improvements the
block should have ordered itself and none widens scope: the falsified
`test_runner.py` safety bullets, the module-handle import that keeps a `test_`
prefixed factory out of pytest's collection, and naming the 16 MiB default as a
constant. No block condition is met.

- R-0516 — Low, A BLOCK EDITED A FILE AND LEFT A CLAIM IN IT THAT THE SAME BLOCK
MADE FALSE. R24's C2 added six tests to `tests/orchestration/test_exec_guard.py`
and, in the same commit, correctly rewrote the PARTIAL COVERAGE bullet in
`exec_guard.py` that the migration falsified. It did not touch that TEST file's
own module docstring, which still says the guard "has NO callers in this
repository, so nothing here says anything about whether any existing Remedy
subprocess is limited. It is not." That sentence has been false since T002a and
R24 made it doubly false. Low because nothing executable depends on it and no
gate could have gone red over it — its whole cost is paid by the next reader who
asks what the guard covers and is told the opposite of the truth. It is
registered rather than waved through because it is the R-0417 staleness shape
that this record already names twice: the fix reached the INSTANCE the reviewer
noticed, in the neighbouring file, and not the CLASS, in the file the block was
already editing. The counter-measure is not a new checklist item — item 16 and
the sweep rule it carries already cover a block's own headings, and the gap here
is that the same sweep was never run over the TARGET file's existing prose.
Widening item 16 would restate what the R-0417 entry already says; retiring the
claim is the fix, and this round's own C2 performs it. OPEN.
END-RECORD1

BEGIN-DOCF
The guard has NO callers in this repository, so nothing here says anything about
whether any existing Remedy subprocess is limited. It is not.
END-DOCF

BEGIN-DOCT
These tests exercise the guard DIRECTLY, so a green run here says the mechanism
works and says nothing about which of Remedy's own subprocesses are spawned
through it. That migration state lives in one place on purpose — the PARTIAL
COVERAGE note in `exec_guard`'s own module docstring — and the caller grep is the
honest answer. No count is repeated here, because a count in a second file is a
second thing to forget.
END-DOCT

BEGIN-DONE1
Done: R-0516 — resolved. The false sentence is off disk: this round's C2 replaced
it with a paragraph that says what these tests DO prove, points at
`exec_guard`'s PARTIAL COVERAGE note as the single place the migration state is
recorded, and deliberately repeats no count — a count in a second file is a
second thing to forget, which is how the retired sentence went stale in the first
place. The resolution is verified by this round's G5 before this line is
committed, per constraint 4. No checklist item is added: item 16 and the R-0417
entry already carry the sweep rule, and the gap R-0516 exposed was that the sweep
was run over the block's own text and not over the prose already sitting in the
file the block was editing. That is a reading of an existing rule, not a new one,
and this record is where it belongs.
END-DONE1

BEGIN-PLANF
## Current Step
R24, this round: record the R23 PASS and open T002b. `exec_guard` gains the shared
test-class seam — an explicit environment allowlist, a policy factory and a
`subprocess.run`-shaped runner — and `test_runner.run_tests_local`, the most
load-bearing of the twelve `test`-class sites, becomes its first caller. Its mocked
call sites move onto the new seam and one real pytest run proves a well-behaved
command still works through it.

## Next Steps
1. T002b continued — the remaining `test`-class sites, including
   `test_execution_service.py`'s `Popen`, which takes the child half via
   `plan_child_spawn` rather than the runner, and which carries R-0202.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANF

BEGIN-PLANT
## Current Step
R25, this round: record the R24 PASS, register R-0516 — a stale claim the R24
block left standing in a file it was itself editing — and retire that claim in the
same round. The session's declared cap of two authored rounds is reached here, not
a blocker.

## Next Steps
1. T002b continued — the remaining `test`-class sites, starting with the three in
   `autorun.py`, which share the migrated shape exactly, and ending with
   `test_execution_service.py`'s `Popen`, which takes the child half via
   `plan_child_spawn` rather than the runner and which carries R-0202.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANT
