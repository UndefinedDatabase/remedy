── STEP T003 limitations document — F085 — R66 ───────────────────────────────

Goal: T003's document. A new `docs/system/exec-guard-limitations-v0.md` states what F085 stage 1 does
NOT prevent, and the docs index links it from both of its tables, which is the "limitations document
exists, is linked, and names the non-guarantees explicitly" half of T2_F085's Acceptance. The R65 PASS
is recorded in the same round.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 record the R65 PASS · C3 write the limitations document · C4 link it from the docs index ·
C5 handback. That list runs past five commits, so the handback takes the ≤100-line cap AGENTS.md
allows when a per-commit table needs it.

THIS ROUND EDITS NO `.py` FILE. Its change set holds no code path at all, so NO lint gate and NO red
control are ordered — both are ordered by the presence of a `.py` path, and there is none. The
acceptance line that a network access really fails under deny is measured by its own round, named in
PLAN20T, because that one needs a code change and a destructive control this one cannot host.

CONVENTION, binding on every count here, carried verbatim in force from the R65 block. A line count is
the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and NO
joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIRS ARE PLAN20, INDEX1 AND INDEX2;
ITS ONE END-OF-FILE APPEND, WHICH HAS NO FROM AT ALL, IS RECORD34; ITS ONE WHOLE-FILE SLICE IS
DOCLIM — listed rather than counted, per §3 checklist item 11. Each append slice CARRIES ITS OWN
LEADING BLANK LINES, so the separation its target's convention requires is a property of bytes that
were measured and never of a join shape that was reasoned about.

## Change

C1 applies PLAN20F→PLAN20T to `.agent/plan.md`, rewriting the `## Current Step` section and the WHOLE
`## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep a stale
label. C2 appends RECORD34 to the END of `.agent/live_review.md`. C3 CREATES
`docs/system/exec-guard-limitations-v0.md` whose entire content is the DOCLIM slice. C4 applies
INDEX1F→INDEX1T and then INDEX2F→INDEX2T to `docs/README.md`, adding the quick-find row and the
system-table row.

Change set, named rather than counted: `.agent/authored/f085-r66.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `docs/system/exec-guard-limitations-v0.md`,
`docs/README.md`, `.agent/handoff.md`. Nothing else. NO `docs/roadmap/**` path is in that set, so no
roadmap file is edited and Rule A4 is untouched; a `docs/**` path IS in it, so the docs-consistency
suite is ordered in G4. Every tracked path named here was resolved on disk at 97caa9e1 with
`git ls-tree`, one call per path, before emission, per checklist item 24: all exist EXCEPT
`docs/system/exec-guard-limitations-v0.md`, which returns EMPTY because C3 creates it, and that
absence is itself a gate reading in G3 rather than an oversight.

The reading a gate cannot recompute, taken at 97caa9e1: the only `docs/**` files naming `exec_guard`
are the two roadmap feature files and `docs/agents/planner_reviewer_prompt.md`, none of them an
ist-doc, so DOCLIM creates rather than duplicates — the justification AGENTS.md's "prefer updating
existing files over creating new ones" rule requires. Its content is bounded the same way: every
non-guarantee it states is one this feature's own code or tests already established, and the proxy
paragraph reports a measurement the reviewer took at 97caa9e1 — a child under the posture printed
`REFUSED:URLError` against a loopback server that was really listening, where the same child without
the posture printed `REACHED:SERVED`.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r66.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C5; if it exists, finish the commit in
   flight, write the handback and stop. `git status --porcelain` is empty at round start and after
   every commit.
3. PAIR SHAPES. The reviewer ran the containment test at emission against each target's blob at
   97caa9e1 and prints its own output here per checklist item 15, one reading per pair:
   PLAN20F→PLAN20T `TO contains FROM: false`; INDEX1F→INDEX1T `TO contains FROM: false`;
   INDEX2F→INDEX2T `TO contains FROM: true`. PLAN20 and INDEX1 are therefore REWRITES and each owes
   the FROM 0x / TO 1x reading over its own post-commit file. INDEX2 is APPEND-shaped — its TO opens
   with the new row and then repeats its own FROM line — so the FROM-zero count is unattainable for it
   BY CONSTRUCTION and must NOT be reported: its obligation is FROM exactly 1x AND TO exactly 1x in
   the post-commit blob, which is §4.9's append reading. Each FROM occurs EXACTLY 1x in its target at
   97caa9e1 — the reviewer measured all three.
4. RECORD34 HAS NO FROM, AND DOCLIM HAS NO FROM AND NO PRE-IMAGE. RECORD34 owes ORDERED EQUALITY per
   §4.9 as R-0531 narrows it: the pre-commit blob is a byte-exact PREFIX of the post-commit file, the
   slice is an exact SUFFIX of it, and the lines that commit's diff ADDS are exactly the slice's lines
   IN ORDER. DOCLIM owes WHOLE-FILE equality instead: the file does not exist at 97caa9e1, and its
   post-commit blob equals the DOCLIM bytes EXACTLY, with nothing prepended and nothing appended. Do
   not invent a FROM for either.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of both docs commits. Only C0a
   and C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
6. Every sentence in RECORD34 that states a reading of a file names the SHA it was read at in the same
   clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches to EVERY
   reading in the clause, not only the first. RECORD34 states readings of R65's range only, all of
   which are prior state, so every SHA it names already exists when it is written.
7. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD34 is reviewer text. Do not add a `Landed:`
   line, do not add a `Done:` paragraph of your own, and do not edit RECORD34 to reconcile it with
   anything you measure. A disagreement between RECORD34 and your own reading is a finding to REPORT
   in the handback, never to fix.
8. THIS ROUND REGISTERS NOTHING AND RESOLVES NOTHING. The reviewer re-executed every R65 gate and
   found nothing to register. Registered stays 175, done stays 28, landed stays 0, open stays 147, and
   the next free id stays R-0561. RECORD34 is a `Gate:` paragraph and carries no `- R-` registration
   line and no `Done:` line, which is why the arithmetic must not move; G6 proves it.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission. The worker re-measures all three from the committed
   `.agent/authored/f085-r66.md`; a mismatch is a finding against this block, not the worker.
10. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and its
   output, and push what is committed. Never edit a slice to make a gate green, and never widen the
   change set to route around a red.
11. RUN THE SUITES SERIALLY, one pytest process at a time, never alongside another in any checkout or
   worktree. These suites spawn real supervisors that bind a port and leave escapees when a readiness
   assertion fails, so two concurrent runs redden each other on tests neither touched.
12. DOCLIM IS AN IST-DOC AND STATES ONLY WHAT IS BUILT. Do not add a status banner, do not add a
   roadmap promise, and do not soften a non-guarantee. If you believe a sentence in it is false at
   HEAD, that is a finding to REPORT in the handback, never to edit.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit. This round orders NO destructive check, so no `git worktree` is
created at all and `git worktree list` is one line at round start and one line at the end.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r66.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each. Also report the block's TOTAL, PROSE and RECORD34 line counts read
from that committed file, against constraint 9's 490 / 400 / 140.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN20F→PLAN20T is a REWRITE over `.agent/plan.md` at C1 and INDEX1F→INDEX1T a REWRITE over
   `docs/README.md` at C4: for each report FROM 0x and TO exactly 1x over the post-commit blob.
   INDEX2F→INDEX2T, over `docs/README.md` at that same commit, reports FROM exactly 1x AND TO exactly
   1x instead, per constraint 3, and NO FROM-zero count. Re-applying the extracted pairs to each
   pre-commit blob — for `docs/README.md` both of its pairs IN ORDER — must reproduce the post-commit
   blob BYTE-EXACTLY.
 - For RECORD34 at C2 report the ordered-equality readings constraint 4 names: pre-commit blob is a
   byte-exact PREFIX, the slice is an exact SUFFIX, `pre + slice` equals the post-commit blob byte for
   byte, and that commit's ADDED lines are exactly the slice's lines IN ORDER.
 - For DOCLIM at C3 report: `git ls-tree 97caa9e1 -- docs/system/exec-guard-limitations-v0.md` is
   EMPTY, the post-commit blob EQUALS the DOCLIM bytes exactly, and that commit's ADDED lines are
   exactly the slice's lines IN ORDER.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each EXIT 0, and serially per
constraint 11. Report each run's passed count; the counts are reported, never predicted, and only the
exit code is ordered. The reviewer took every base reading below itself, in the primary checkout, at
97caa9e1.
 - `python3 -m pytest tests/docs/test_docs_consistency.py -q` — base `295 passed`; C3 and C4 change
   `docs/**` and this suite reads `docs/README.md` directly, which is the whole reason it is ordered.
 - `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
   tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
   base `160 passed`; two of them assert on `.agent/plan.md`, which C1 rewrites.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected by
grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 40 lines by applying the pair to that blob at 97caa9e1.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
97caa9e1 and at HEAD, from the line-start patterns for a registration, a resolution and a landed line.
The reviewer's base reading is 175 / 28 / 0, 147 open, max registered R-0560, max resolved R-0558. At
HEAD the reading must be IDENTICAL — 175 / 28 / 0, 147 open, same two maxima — and all three symmetric
differences must be EMPTY, because constraint 8 rules this round registers and resolves nothing. Next
free id R-0561. Report all three symmetric differences, the duplicate-id count and the count of
resolutions naming an unregistered id, at both SHAs.

G7 LINK INTEGRITY, on `docs/README.md` after C4, because a link gate is the point of this round.
Report all four readings: the string `system/exec-guard-limitations-v0.md` occurs EXACTLY twice in
that file; the path `docs/system/exec-guard-limitations-v0.md` resolves on disk at HEAD; the file it
resolves to is byte-identical to the DOCLIM slice; and the quick-find row and the system-table row are
each present exactly once, counted as whole LINES from INDEX1T's and INDEX2T's own new line.

G8 HYGIENE. `git diff --name-only 97caa9e1..HEAD` measured BEFORE C5 holds exactly the change set
above minus `.agent/handoff.md`, which C5 writes, and nothing else — and in particular holds no `.py`
path at all, and none of `packages/orchestration/exec_guard.py`, `packages/runtimes/dev_server.py`,
`packages/runtimes/runtime_supervisor.py` and `apps/cli/commands/runtime_cmd.py`. Those four were each
resolved at 97caa9e1 with `git ls-tree 97caa9e1 -- <path>`, one call per path, and all four exist;
re-run those four calls and report each result, per §3 checklist item 24. Report per-commit insertions
for every commit BEFORE C5 — C5 cannot measure itself, so its own go in the round report — and confirm
none exceeds 500. This branch spent the AGENTS.md declared-oversize allowance at d4473f85, so a second
oversize commit is a STOP under constraint 10, never a declaration. Confirm every commit is
single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base SHA
97caa9e1, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3, C4
and C5, the real G1-G8 results with exit codes, the open-findings count and the next expected action.
The Bundle above holds more than five commits, so the ≤100-line cap applies; if the mandated content
genuinely does not fit even there, name the DECISION D15 stated cause and the specific mandated
content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~99 % (T001 gebaut · R13-R65 PASS · T002 KOMPLETT · T003 fast fertig: alle drei
default-deny-Zeilen verdrahtet und gepinnt, das Limitations-Dokument steht und ist zweifach verlinkt;
offen bleibt allein die Akzeptanzmessung am echt lauschenden Server) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: R67 measures
T2_F085's remaining acceptance line — a network access from a guarded test command fails under deny —
against a loopback server that is really listening, with the red control that line needs; the
integration gate and closure follow it. TWO: R66 carries no verdict of its own, because the round that
records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R67
carries it. THREE: a standalone closing line stating the open findings count and the next free id.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires
every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN20F
## Current Step
R65, this round: the two deny rows amendment F085 D1 still leaves unwired take the posture R64
built. `dod_process_exec_policy` and `managed_builder_execution._builder_exec_policy` set
`deny_network=True`, each pinned by a test in the file its own class already owns, so all three
bounded rows of that table now deny. The R64 PASS is recorded and its one finding registered in
the same round, with the counter-measure landing ahead of the record.

## Next Steps
1. T003's limitations document and its README link, stating what stage 1 does NOT prevent: a
   binary that ignores proxy variables reaches the network anyway, an app log written to a file
   takes no guard output cap, and the git, packaging and other classes never ran under the guard
   at all.
2. Then the integration gate, then closure.
END-PLAN20F

BEGIN-PLAN20T
## Current Step
R66, this round: T003's document. `docs/system/exec-guard-limitations-v0.md` states what stage 1
does NOT prevent — a proxy posture is not containment, three classes of five run under the guard
at all, an allowlist does not bound what a child's own runtime adds, and an app log written to a
file takes no cap — and `docs/README.md` links it from both tables. The R65 PASS is recorded in
the same round.

## Next Steps
1. The remaining acceptance measurement: a guarded test command is refused against a loopback
   server that is really listening, where the same child without the posture is served.
2. The integration gate: the full suite per docs/agents/integration_gate.md, the first of the two
   full-suite runs this feature owes.
3. Then closure per docs/roadmap/STATUS_closure_protocol.md.
END-PLAN20T

BEGIN-INDEX1F
| dogfood | [dogfood-run-user-guide.md](guides/dogfood-run-user-guide.md) | guide |
| external builder | [external-builder-sandbox-v0.md](system/external-builder-sandbox-v0.md) | system |
END-INDEX1F

BEGIN-INDEX1T
| dogfood | [dogfood-run-user-guide.md](guides/dogfood-run-user-guide.md) | guide |
| exec guard | [exec-guard-limitations-v0.md](system/exec-guard-limitations-v0.md) | system |
| external builder | [external-builder-sandbox-v0.md](system/external-builder-sandbox-v0.md) | system |
END-INDEX1T

BEGIN-INDEX2F
| [execution-approval-policy-v0.md](system/execution-approval-policy-v0.md) | Human approval gates for execution |
END-INDEX2F

BEGIN-INDEX2T
| [exec-guard-limitations-v0.md](system/exec-guard-limitations-v0.md) | What the F085 stage-1 execution guard does NOT prevent |
| [execution-approval-policy-v0.md](system/execution-approval-policy-v0.md) | Human approval gates for execution |
END-INDEX2T

BEGIN-DOCLIM
# Execution Guard — what stage 1 does NOT prevent

## Overview

F085 stage 1 gives builder-spawned commands POSIX resource limits, a wall timeout, output
caps, a pinned cwd, an environment allowlist over a forbidden-key floor, and a default-deny
network posture. This document states the non-guarantees, because a guard trusted past its
evidence is worse than no guard: the code deliberately declines to call any of this
containment.

## The network posture is a PROXY posture, never a kernel one

`deny_network` points a child's proxy variables — both spellings, plus an empty `NO_PROXY` so
no host is exempt — at `http://127.0.0.1:9`, the RFC 863 discard port, where nothing listens
and a connect is refused at once.

- A toolchain that HONOURS proxy variables cannot reach the network. Measured: a guarded child
  is refused against a loopback server that is really listening, while the same child without
  the posture is served.
- A binary that IGNORES them reaches the network anyway. Static Go binaries, anything using
  raw sockets, and most things speaking a non-HTTP protocol are in that set.
- Nothing here blocks DNS, raw sockets, or a unix socket to a local daemon.

Kernel-level isolation is stage 2. Stage 1 raises the bar and reports honestly.

## Only three command classes run under the guard at all

Amendment F085 D1's table wires `builder`, `test` and `dod-process`. The `dod-app` class
deliberately takes no wall timeout and no deny — its harness must keep serving on its own
port. The git, packaging, runtime and other call sites still spawn unsupervised, so a limit
proved for a test command says nothing about a `git` invocation.

## An allowlist bounds the PARENT, not the child's own runtime

Scrubbing decides what the parent hands over. It cannot decide what the child then adds to
itself: a CPython child sets `LC_CTYPE` during PEP 538 locale coercion, so a child's
environment is a SUPERSET of the scrubbed one. Tests subtract that key rather than crediting
the guard with producing it.

## Output caps bound what the guard READS

The cap applies to the child's stdout and stderr while the guard is reading them. An
application that writes its own log to a FILE takes no guard cap at all, and neither does
anything a child writes through a descriptor the guard never owned. Past the cap the guard
stops STORING and keeps COUNTING, so the reported byte totals stay honest while the stored
output is truncated.

## Limits that are enforced but not classified

`address_space_bytes` is enforced through RLIMIT_AS. A child that exceeds it has its mapping
refused, raises `MemoryError` and exits 1 with no signal, and its `ru_maxrss` stays below the
limit because the refused mapping never became resident. Nothing `wait4` reports distinguishes
that death from any other exit-1 failure, so the guard enforces the limit and declines to name
it in `tripped_limit`. Naming it would be an overclaim.

## There is no filesystem fence

The cwd is PINNED, which decides where a relative path lands. It does not stop a child writing
to an absolute path outside the worktree. A filesystem fence is stage 2.

## A stream still blocked at the grace deadline leaks

If a stream is still blocked when the grace deadline passes, one pipe read end and one daemon
thread survive the run. Closing that descriptor under a blocked reader risks the thread reading
a recycled descriptor after a later `open()`, so the leak is the deliberately chosen cheaper
wrong.

## Where the rules live

Policy per command class: `packages/orchestration/exec_guard.py`. The class table and the
staging plan: `docs/roadmap/features/T2_F085.md`.
END-DOCLIM

BEGIN-RECORD34

Gate: R66 — the R65 entry. R65 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer over
e5eecb29..97caa9e1, not read, and each reproduces the handback's reading exactly; the worker deviated
in nothing and declared nothing. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD, disk-to-disk
with no digest fallback: the committed `.agent/authored/f085-r65.md` and the committed
`.agent/last_block.md` at 97caa9e1, both working copies at 97caa9e1, and the received
`.remedy-wt/f085-r65.md` are all five byte-EQUAL at sha256
f0fa416c8a4b343601435f75fb8f69a5c7e8f7198b7c433b4a9a9343ebd11399, 31907 B, 459 lines, 32 marker lines.
THE SHAPES HELD, and the two classes were measured apart, one reading per pair. The six REWRITES —
PLAN19 over `.agent/plan.md` at 73db31ec, CHECK25 over `docs/agents/planner_reviewer_prompt.md` at
28a749e3, DOD1 and DOD2 over `packages/orchestration/exec_guard.py` at aadcf5e1, BUILD1 and BUILD2
over `packages/orchestration/managed_builder_execution.py` at 6b0edbef — each read
`TO contains FROM: false`, each FROM 1x in its own pre-commit blob, each ending FROM 0x with TO
exactly 1x. TESTBUILD over `tests/orchestration/test_managed_builder_execution.py` at a2aaff6d is
APPEND-shaped, reading FROM 1x AND TO 1x post-commit with no FROM-zero reading taken. Re-application
IN ORDER reproduced the post-commit blob BYTE-EXACTLY on all five paths. RECORD33 over
`.agent/live_review.md` at 1439a831 and TESTDOD over `tests/orchestration/test_exec_guard.py` at
bf4c6645, neither of which has a FROM, satisfy ORDERED EQUALITY on every clause — PREFIX, SUFFIX,
`pre + slice` equal to the post-commit blob byte for byte, and ADDED lines equal to the slice's lines
IN ORDER, 71 and 71, 9 and 9, numstat `71 0` and `9 0`. Marker LINES at 97caa9e1 are 0 in each of the
seven edited files. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout with that block's exact
command lines, serially, each exit 0: `331 passed` against a base of `329 passed` for the seam set,
C6 and C7 each adding exactly one test; `160 passed` against a base of `160 passed` for the four state
readers; and the canary `42 passed` against a base of `42 passed`. THE PLAN CONTRACT HELD at 97caa9e1:
40 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all present, 40
being that block's own projection. THE ARITHMETIC MOVED IN EXACTLY ONE PLACE, as that block's
constraint 9 required: 174 registered / 28 done / 0 landed and 146 open at e5eecb29 against 175 / 28 /
0 and 147 open at 97caa9e1, max registered moving R-0559 to R-0560 while max resolved stayed R-0558,
the registered symmetric difference exactly the single id R-0560, the done and landed symmetric
differences EMPTY, and 0 duplicate ids and 0 orphan resolutions at both SHAs. LINT WAS RE-RUN over all
four `.py` paths from the repository root with the repository's own configuration, plain and
`--preview`, each exit 0 with `All checks passed!`. THE RED CONTROL REPRODUCED EXACTLY inside a
disposable worktree at 97caa9e1: applying the DOD2T→DOD2F byte pair to
`packages/orchestration/exec_guard.py`, in which the DOD2T bytes were counted 1x before the replace,
gave a worktree `git diff --stat` of `1 file changed, 1 deletion(-)` and turned
`python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf` red at exit 1 with
`1 failed, 41 passed`, the single failure being
`test_the_dod_process_policy_denies_the_network_its_row_denies` on its
`assert policy.deny_network is True` line — exactly the ordered failure and the only one, which is
what item 25 bought: R64's control reddened two tests and this one reddens precisely the test whose
row was reverted. HYGIENE IS CLEAN: the path set over e5eecb29..97caa9e1 is exactly the nine the
change set named and holds none of the three `runtime-server` paths; all seven paths G9 orders
resolved at e5eecb29 under `git ls-tree`; per-commit INSERTIONS are 459, 392, 7, 10, 71, 5, 5, 9, 14
and 50 for the handback commit, none over 500; all ten commits are single-parent; and
`.agent/handoff.md` at 97caa9e1 is 90 lines, within the ≤100-line cap its ten-commit table allows,
with the ordered Fortschritt line present verbatim. THE BLOCK'S OWN SIZE re-measured from the
committed file at 97caa9e1 gives TOTAL 459, PROSE 289 counting its 32 marker lines and RECORD33 71,
agreeing with that block's own figures and inside 490 / 400 / 140. ONE READING THE HANDBACK FLAGGED
WAS CHECKED RATHER THAN ACCEPTED: C0b's insertion count is 392 by `--numstat` and 459 by the commit
line's rewrite detection, and the numstat reading is the one G9 measures, so the handback naming both
is correct rather than a discrepancy. NOTHING FAILED and this round registers no finding.
END-RECORD34
