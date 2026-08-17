── STEP T002d record round — F085 — R55 ──────────────────────────────────────

Goal: persist R54's PASS to `.agent/live_review.md`, advance `.agent/plan.md` to name the migration
R56 will perform, and record on disk the environment-allowlist question that migration must answer
before it is designed. This round writes NO production code and ships NO test: it is a record
round, opened deliberately because the reviewer's session is ending at its declared cap and a
verdict that lives only in a chat reply is a verdict the next session must re-derive.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R54 · C3 handback. That is FIVE ordered commits, which is not more
than five, so the handback's ≤60-line cap applies rather than the ≤100-line allowance.

CONVENTION, binding on every count here, carried verbatim in force from the R54 block because it is
the R-0556 counter-measure. A line count is the `splitlines` reading — a trailing newline is NOT an
extra line. A SLICE IS THE BYTES STRICTLY BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE
NEWLINE THAT TERMINATES ITS LAST CONTENT LINE: extract it as everything after the `BEGIN-` line's
own newline up to and including the newline immediately before the `END-` line, so that
`pre + slice` is already a newline-terminated file and NO joiner and NO terminator byte is ever
added. RECORD23 is PROSE joined to its target by exactly one blank line; this block carries no code
slice.

## Change

C1 applies PLAN9F→PLAN9T to `.agent/plan.md`, which rewrites the `## Current Step` section, the
WHOLE `## Next Steps` list and the WHOLE `## Risks` list — the last because the migration's
environment question belongs where the next session reads it, and adding an entry changes that
list's arity. C2 appends RECORD23 to `.agent/live_review.md`.

Change set, named rather than counted: `.agent/authored/f085-r55.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md`. Nothing else. No `docs/roadmap/**`
path is in that set, so the §3 docs tier does NOT trigger and no `tests/docs/` gate is ordered; NO
`.py` file is in it either, so this round orders no lint gate and no code suite — the state-reader
suite and the canary are what a `.agent/**` round owes, and G4 carries them.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r55.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C3; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit. This round orders no destructive check, so it creates no worktree and
   `git worktree list` stays one line throughout.
3. PAIR SHAPES. The reviewer ran the containment test on the one pair at emission against that
   file's blob at 1812c219 and prints its own output here per checklist item 15: PLAN9F→PLAN9T
   `TO contains FROM: false`. It is therefore a REWRITE and owes the FROM 0x / TO 1x reading over
   its whole post-commit file. Its FROM occurs EXACTLY 1x in its target at 1812c219 — the reviewer
   measured it. RECORD23 is an APPEND carrying no FROM, so no containment reading is owed for it.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record. Only C0a and C0b may precede it. This
   round writes to the finding ledger, so §3 checklist item 23 binds it.
5. Every sentence in RECORD23 that states a reading of a file THIS BLOCK also edits names the SHA
   it was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first. C0b overwrites the
   working `.agent/last_block.md` before RECORD23 lands, which is why a SHA carries those readings.
6. NO SLICE REPRODUCES A RETIRED FROM TEXT. The reviewer tested PLAN9F against every later-applied
   text at emission and got NO hits, so the G3 FROM-0x reading stays attainable (item 2).
7. Nothing outside the declared change set is touched. This round REGISTERS NOTHING and RESOLVES
   NOTHING: the registered, done and landed counts are all UNCHANGED, the open count stays 145 and
   the next free id stays R-0558. The npm environment question is recorded as a plan RISK and not
   as a finding, because nothing on disk is defective — it is an input the R56 design owes an
   answer to. `.agent/plan.md` after C1 is 46 lines, which the reviewer projected mechanically by
   applying the pair to that file's blob at 1812c219.
8. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never widen
   the change set to route around a red.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and states them here: TOTAL 253, PROSE 158, RECORD23 46. The worker
   re-measures all three from the committed `.agent/authored/f085-r55.md` and reports them; a
   mismatch is a finding against this block, not against the worker.
10. THIS ROUND ORDERS NO RED CONTROL, because it changes no code and no test. The reviewer's own
   red controls for R54 are recorded inside RECORD23 and are not to be repeated.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r55.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r55.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - The REWRITE of constraint 3: in the post-commit file PLAN9F occurs 0x and PLAN9T exactly 1x.
   Report both counts and `git show --numstat` for that path and commit.
 - C2 / RECORD23 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's prose.
   §4.9's per-line PROSE obligation also applies: every non-empty line the slice contains occurs
   exactly once among the lines C2's diff adds TO THAT PATH.

G4 STATE READERS, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` — ordered because C1 rewrites `.agent/plan.md`,
which two of them assert on. Base at 1812c219, taken by the reviewer in the primary checkout:
`159 passed`. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q`, base `42 passed`. REPORT
both numbers.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. G4
covers the first three through their tests; this gate covers the cap.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
1812c219 and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 172 / 27 / 0, 145 open, max registered R-0557, max resolved
R-0532. At HEAD ALL THREE COUNTS MUST BE UNCHANGED and ALL THREE SYMMETRIC DIFFERENCES MUST BE
EMPTY, because this round records a verdict and registers nothing; 145 open, next free id R-0558.
Report the three symmetric differences, the duplicate-id count and the count of resolutions naming
an unregistered id, at both SHAs.

G7 HYGIENE. `git diff --name-only 1812c219..HEAD` measured BEFORE C3 holds exactly the change set
above minus `.agent/handoff.md`, which C3 writes, and nothing else — and in particular does NOT
hold any path under `packages/` or `tests/`. Report per-commit insertions for every commit BEFORE
C3 — C3 cannot measure itself, so its own insertions go in the round report — and confirm none
exceeds 500. This branch spent the AGENTS.md declared-oversize allowance at d4473f85, so a second
oversize commit is a STOP under constraint 8, never a declaration. Confirm every commit is
single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 1812c219, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2 and
C3, the real G1-G7 results with exit codes, the open-findings count and the next expected action.
The Bundle above names five commits, which is not more than five, so the ≤60-line cap applies; if
the mandated content genuinely does not fit, name the DECISION D15 stated cause and the specific
mandated content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~93 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R54 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT · T002d zur Hälfte — Naht und Extraktion gebaut,
die fünf Call-Sites offen · T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round is
R56, which migrates the two `runtime-build` call sites in `_auto_build_frontend`
(`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with `check=True`,
and must FIRST settle the environment question `.agent/plan.md` now carries as a risk. Then the
three `runtime-server` sites, then T003, the integration gate and closure. TWO: R55's own verdict is
NOT on disk as a gate entry, because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, and R56 must not
open a repair round to close it. THREE: a standalone closing line stating the open findings count
and the next free id as its own sentence. FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from
disk`, which the self-drive protocol requires every handoff naming a next action to put ahead of
the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN9F
## Current Step
R54, this round: T002d's first half. `packages/orchestration/exec_guard.py` gains the
`runtime-build` seam under Amendment F085 D8 — a BOUNDED class, so it KEEPS a wall timeout — and
that third caller is what makes the guard-result translation worth extracting, so the `test` and
`dod-process` wrappers move onto the shared helper in the same round. No call site migrates here.
Four tests ship with it. The R53 PASS is recorded in the same round, with finding R-0557.

## Next Steps
1. T002d's second half — migrate the two `runtime-build` sites in `_auto_build_frontend`
   (`packages/orchestration/ui_server.py`) onto the new seam with `check=True`, then the three
   `runtime-server` sites, which take no wall timeout because a clock would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output cap.
   Then the integration gate, then closure.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
END-PLAN9F

BEGIN-PLAN9T
## Current Step
R55, this round: a RECORD round only. It persists the R54 PASS to `.agent/live_review.md` and
advances this file; it writes no production code and ships no test. It exists because the
reviewer's session ended at its declared round cap, and a verdict that lives only in a chat reply
is one the next session would have to re-derive from the diff.

## Next Steps
1. T002d's second half — migrate the two `runtime-build` sites in `_auto_build_frontend`
   (`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with
   `check=True`, settling the npm environment risk below FIRST. Then the three `runtime-server`
   sites, which take no wall timeout because a clock would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output cap.
   Then the integration gate, then closure.

## Risks
- `RUNTIME_BUILD_ENV_ALLOWLIST` is `TEST_COMMAND_ENV_ALLOWLIST`, read at 1812c219: it carries
  `HOME` and `PATH`, so a public-registry `npm install` survives the scrub, but it names no
  `NPM_CONFIG_*`, no `NODE_*` and no proxy variable. A project on a private registry or behind a
  proxy would break at the migration, not at the seam. R56 settles this BEFORE it migrates —
  widen that row, or take the `extra_env_keys` knob the `test` row already carries.
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
END-PLAN9T

BEGIN-RECORD23
Gate: R55 — the R54 entry. R54 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 8ba3ad45..1812c219, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r54.md`, the committed `.agent/authored/f085-r54.md` at eb18ad04,
the committed `.agent/last_block.md` at 2067581f, both of those paths at 1812c219 and both working
copies as they stand at 1812c219 are all seven byte-EQUAL at sha256
19497ed6660efbf34b3e2fbb246faa0c1ef0e0a75e7132c14e3757a6c3182959, 31279 B, 490 lines, 22 marker
lines — every figure measured on every copy. THE SHAPES HELD. Each of the four REWRITES gives
`TO contains FROM: false`, its FROM 1x in the pre-commit blob and 0x after with its TO exactly 1x:
PLAN8F→PLAN8T at dbfb26af numstat `8 9`, and XLAT1F→XLAT1T, XLAT2F→XLAT2T and DOCXF→DOCXT all at
1bfcaf0c, that path's numstat `7 26`. THE PROSE APPEND RECORD22 on `.agent/live_review.md` at
d48febf0: byte-exact prefix, a remainder of exactly one blank line plus the slice, an exact suffix,
0 marker LINES, and each of its 51 non-empty slice lines occurring exactly once among the 53 lines
that commit adds, numstat `53 0`. THE TWO CODE APPENDS held under ORDERED EQUALITY — SEAM3 at
27279810 numstat `99 0` and TESTSRB at a3d32124 numstat `46 0`: each post-commit file equals
`pre + slice` with NO byte between them, each commit's added lines are exactly that slice's lines
IN ORDER, and 0 marker LINES reached either. THE SUITES AND THE LINT GATE WERE RE-RUN, NOT READ, in
the primary checkout with the block's exact command lines, each exit 0: the code suite `156 passed`
against a base of 152, the four state readers `159 passed` against 159, the canary `42 passed`
against 42, and ruff `All checks passed!`. THE PLAN CONTRACT HELD at dbfb26af: 41 lines against the
50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id present — 41 is the figure that
block projected. THE ARITHMETIC MOVED AS ORDERED: 172 / 27 / 0 at 1812c219 against 171 / 27 / 0 at
8ba3ad45, 145 open against 144, the registered symmetric difference exactly R-0557, done and landed
symmetric differences EMPTY, no duplicate id and no resolution naming an unregistered id at either
SHA. HYGIENE IS CLEAN: walking 8ba3ad45..1812c219 commit by commit the INSERTION counts, the column
AGENTS.md DECISION F104 D1 fixes for the cap, are 490, 417, 8, 53, 99, 7, 46 and 35 for the
handback commit; none over 500; that range's path set measured before the handback is exactly the
six ordered paths and does NOT hold `packages/orchestration/ui_server.py`, which that round's
change set excluded; all eight commits are single-parent; the tree is clean and `git worktree list`
is one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 490, PROSE 225
and RECORD22 52, agreeing with that block. THE HANDBACK'S OWN SELF-CLAIM was checked and holds:
`.agent/handoff.md` at 1812c219 states 92 lines and measures 92, inside the ≤100 allowance an
eight-commit round carries. THE WORKER'S ONE DECLARED DEVIATION WAS VERIFIED RATHER THAN ACCEPTED:
it reported writing throwaway helper scripts under the gitignored `.remedy-wt/`, and
`git ls-files .remedy-wt` returns EMPTY at 1812c219, so nothing it named entered the repository.
THE EXTRACTION WAS PROVEN SHARED, NOT ASSUMED, by the reviewer's own red control in a disposable
worktree at 1812c219 that it removed afterwards. At that commit
`_completed_process_from_guarded` is defined exactly once and called from three sites, and the
module holds `raise subprocess.TimeoutExpired(` exactly once where 8ba3ad45 held it twice — so the
duplication really is gone rather than merely wrapped. Deleting the wall-trip branch from that one
helper turned three tests RED across all three seams at once — the `test` seam's
`test_a_wall_trip_raises_timeout_expired_carrying_the_partial_output`, the `dod-process` seam's
`TestNeverASilentPass::test_a_timeout_is_red_not_a_hang` in `tests/orchestration/test_dod_runners.py`,
and the new `test_the_runtime_build_seam_raises_timeout_expired_on_a_wall_trip` — against 80 passed
and 0 failed unmutated. A refactor whose single point of failure reddens every caller is the
equality claim actually holding, which is what the round's own G5 could only show negatively.
END-RECORD23
