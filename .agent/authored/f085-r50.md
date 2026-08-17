── STEP record+amend — F085 — R50 ────────────────────────────────────────────

Goal: record the R49 PASS, register R-0552 and R-0553, and amend the F085 feature file so the
`runtime` class carries the two policies its sites actually need. T002d cannot be implemented
correctly until that row is split: it rules NO wall timeout over two sites that already pass
`timeout=120`, which is the defect DECISION F085 D7 fixed one row above and left standing here.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R49 and register R-0552 and R-0553 · C3a split the runtime policy
row · C3b append DECISION F085 D8 · C4 handback.

CONVENTION, binding on every count here: a line count is the `splitlines` reading — a trailing
newline is NOT an extra line. A slice is the bytes strictly between its marker lines.

## Change

C1 applies PLAN4F→PLAN4T to `.agent/plan.md`. C2 appends RECORD18 to `.agent/live_review.md`.
C3a applies AMEND8F→AMEND8T and C3b appends DEC8, both to
`docs/roadmap/features/T2_F085.md`. They are two commits and not one so that each carries its own
clean shape proof: an append proof needs a pre-commit blob the same commit did not already
rewrite. No `.py` file is touched, so no lint gate and no code suite is ordered; their absence is
declared here rather than filled with a command that could not see this round's change.

Change set, named rather than counted: `.agent/authored/f085-r50.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/features/T2_F085.md`,
`.agent/handoff.md`. Nothing else. `docs/roadmap/**` IS in that set, so the §3 docs tier triggers
and G5 carries it.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r50.md` by its marker pair. Never retype one, never apply one from the
   prompt. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C4; if it exists, finish the
   commit in flight, write the handback and stop. `git status --porcelain` is empty at round
   start and after every commit. This round orders no destructive check, so it creates no
   worktree and `git worktree list` stays one line.
3. PAIR SHAPES, each tested mechanically by the reviewer at emission, each output printed here
   per checklist item 15, one reading per pair and none generalised to another:
   - PLAN4F→PLAN4T on `.agent/plan.md` gives `TO contains FROM: false` → REWRITE, so the
     FROM 0x / TO 1x reading over the whole post-commit file is owed. The pair spans the
     `## Current Step` and `## Next Steps` sections and stops before the blank line preceding
     `## Risks`; `## Goal` and `## Risks` are unchanged and stay outside it.
   - AMEND8F→AMEND8T on `docs/roadmap/features/T2_F085.md` gives `TO contains FROM: false` →
     REWRITE, same FROM 0x / TO 1x obligation. Per checklist item 17 the FROM spans every table
     row from `runtime` to the end of the table plus the paragraph beneath it, because the TO
     changes the table's ARITY by splitting one row into two.
   - RECORD18 and DEC8 are APPENDS of PROSE, each carrying no FROM, so no containment reading is
     owed for either. Each target stays a byte-exact prefix and exactly one blank line joins it
     to the slice.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of the amendment. Only C0a
   and C0b may precede it. This round registers findings, so §3 checklist item 23 binds it.
5. Every sentence in RECORD18 and in DEC8 that states a reading of a file THIS BLOCK also edits
   names the SHA 25a5b42e in the same clause, per checklist item 20 as R-0521 and R-0534 narrow
   it — the qualifier attaches to EVERY reading in the clause, not only the first.
   `.agent/plan.md` and `docs/roadmap/features/T2_F085.md` are both such files: C1 changes the
   first, C3a and C3b the second, and both slices land before C3a or read the base.
6. NO SLICE REPRODUCES THE RETIRED TABLE ROWS. DEC8 describes the single `runtime` row it
   replaces in prose and never quotes it, so G3's AMEND8F-0x reading stays attainable — checklist
   item 2, whose whole failure mode is a TO that quotes retired text on purpose. The reviewer
   tested this mechanically at emission: AMEND8F does not occur inside DEC8.
7. Nothing outside the declared change set is touched. This round registers R-0552 and R-0553 and
   resolves nothing: the open count goes 139 → 141, next free id R-0554.
8. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output. Never edit a slice to make a gate green.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three at
   emission and states them here: TOTAL 334, PROSE 182, RECORD18 72. The worker re-measures all
   three from the committed `.agent/authored/f085-r50.md` and reports them; a mismatch is a
   finding against this block, not against the worker.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty
at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r50.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r50.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - C1 / PLAN4F→PLAN4T / `.agent/plan.md`, a REWRITE: PLAN4F occurs 0x and PLAN4T exactly 1x in
   the post-commit file. Report both counts and `git show --numstat` for the path.
 - C2 / RECORD18 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's
   prose. §4.9's per-line obligation applies, and it is the PROSE form because the slice is
   prose: every non-empty line the slice contains occurs exactly once among the lines C2's diff
   adds TO THAT PATH. Report the slice's empty-line count and `git show --numstat`.
 - C3a / AMEND8F→AMEND8T / `docs/roadmap/features/T2_F085.md`, a REWRITE: AMEND8F occurs 0x and
   AMEND8T exactly 1x in the post-commit file. Report both counts and `git show --numstat`.
 - C3b / DEC8 / the same path, a PROSE APPEND against the blob C3a left: prefix, remainder of
   exactly one blank line plus the slice, exact suffix, 0 marker LINES, the same per-line
   obligation over C3b's added lines. Report the empty-line count and `git show --numstat`.

G4 SUITE, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read `.agent/` state
live, two of which assert on `.agent/plan.md`. Base reading at 25a5b42e, taken by the reviewer in
the primary checkout: `159 passed`. REPORT the number this run prints. CANARY
`python3 -m pytest tests/cli/test_golden_path.py -q` — base at 25a5b42e `42 passed`.

G5 DOCS TIER, required because `docs/roadmap/**` is in the change set:
`python3 -m pytest tests/docs/ -q`, base at 25a5b42e `295 passed`, exit 0. REPORT the number.
WHAT THIS GATE DOES AND DOES NOT SEE, re-measured by the reviewer at 25a5b42e in a disposable
worktree with a red control rather than carried over from R49: replacing the `runtime` table row
with a garbage row left it at `295 passed` exit 0, and renaming `T2_F085.md` to
`T2_F085.md.hidden` made it `2 failed, 293 passed` exit 1. So it guards the feature file's
EXISTENCE and its F-id mapping and is blind to the file's BODY. It is ordered because the tier
requires it and because C3a and C3b must not break the mapping — not as evidence that the
amendment's text is right. G3 is that evidence.

G6 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer
collected by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains
`## Next Steps`, matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and each of
the three booleans. The reviewer's projection of the post-C1 file is 41 lines. G4 covers the
first three through their tests; this gate covers the cap, which no test reads.

G7 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
25a5b42e and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 166 / 27 / 0, 139 open, max registered R-0551, max resolved
R-0532. At HEAD registered must be 168, the registered symmetric difference exactly R-0552 and
R-0553, done and landed symmetric differences EMPTY, 141 open, next free id R-0554. Report the
three symmetric differences, the duplicate-id count and the count of resolutions naming an
unregistered id, at both SHAs.

G8 HYGIENE. `git diff --name-only 25a5b42e..HEAD` measured BEFORE C4 holds exactly the change set
above minus `.agent/handoff.md`, which C4 writes, and nothing else. Report per-commit insertions
for every commit BEFORE C4 — C4 cannot measure itself, so its own insertions go in the round
report — and confirm none exceeds 500. This branch already spent the AGENTS.md declared-oversize
allowance at d4473f85, so a second oversize commit is a STOP under constraint 8, never a
declaration. Confirm every commit has exactly one parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 25a5b42e, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2,
C3a, C3b and C4, the real G1-G8 results with exit codes, the open-findings count and the next
expected action. This round has more than five commits, so the ≤100-line allowance applies;
beyond that, name the DECISION D15 stated cause and the mandated content behind it.
Repeat this Fortschritt line verbatim:
Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R49 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c entsperrt durch Amendment F085 D7, noch nicht gebaut ·
T002d entsperrt durch Amendment F085 D8, noch nicht gebaut · T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round
is R51, started by a FRESH session, and it implements T002c — `_run_process_check` onto the guard
seam KEEPING its wall timeout and closing its `env=os.environ.copy()` gap, and `_run_app_once`
under the dod-app policy with no wall timeout and network allowed; T002d then follows under the
D8 split, then T003, the integration gate and closure. TWO: R50's own verdict is NOT on disk as a
gate entry, because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a missing
gate, and R51 must not open a repair round to close it; R50's verdict, when the reviewer issues
it, is recorded by R51's OWN record slice. THREE: a standalone closing line stating the open
findings count and the next free id as its own sentence, not only inside a gate transcript.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, because the self-drive protocol
requires every handoff that names the next session's first action to name that rule ahead of the
Open PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN4F
## Current Step
R49, this round: record the R48 PASS, register R-0550 and R-0551, and amend the F085 feature
file so the `dod` class carries the two policies its two sites actually need. A planning
correction that unblocks T002c rather than implementing it. No source file changes this round.

## Next Steps
1. T002c — `_run_process_check` in `packages/orchestration/dod_runners.py` onto the guard seam
   under the dod-process policy: it is a bounded check and KEEPS a wall timeout; the gap it
   closes is `env=os.environ.copy()`, which hands the child the whole parent environment.
2. T002c — `_run_app_once` in that same module under the dod-app policy: no wall timeout and
   network allowed, because it starts the app harness and probes it over HTTP.
3. T002d — the five runtime sites. Then T003, the integration gate, then closure.
END-PLAN4F

BEGIN-PLAN4T
## Current Step
R50, this round: record the R49 PASS, register R-0552 and R-0553, and amend the F085 feature
file so the `runtime` class carries the two policies its sites actually need — the same
correction D7 made for `dod`, applied to the row D7 left standing. A planning correction; no
source file changes this round, and T002c is built at R51.

## Next Steps
1. T002c — `_run_process_check` in `packages/orchestration/dod_runners.py` onto the guard seam
   under the dod-process policy: it is a bounded check and KEEPS a wall timeout; the gap it
   closes is `env=os.environ.copy()`, which hands the child the whole parent environment.
2. T002c — `_run_app_once` in that same module under the dod-app policy: no wall timeout and
   network allowed, because it starts the app harness and probes it over HTTP.
3. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout,
   `runtime-build` keeps the one it already has. Then T003, the integration gate, then closure.
END-PLAN4T

BEGIN-AMEND8F
| runtime | 5 | yes | yes | NO | yes | yes | yes | allowed |
| git | 24 | no | — | — | — | — | — | — |
| packaging | 11 | no | — | — | — | — | — | — |
| other | 8 real | no | — | — | — | — | — | — |

The classes that take no wall timeout are the ones whose children are long-lived
servers: killing them on a clock would kill the very harness the class exists to
serve, and each is judged by a readiness probe over HTTP, so each keeps network
access. They still take rlimits, an output cap, a pinned cwd and the environment
allowlist. DECISION F085 D7 below splits what was a single `dod` row into the two
policies its two sites need; the sites it covered still sum to two.
END-AMEND8F

BEGIN-AMEND8T
| runtime-server | 3 | yes | yes | NO | yes | yes | yes | allowed |
| runtime-build | 2 | yes | yes | yes | yes | yes | yes | allowed |
| git | 24 | no | — | — | — | — | — | — |
| packaging | 11 | no | — | — | — | — | — | — |
| other | 8 real | no | — | — | — | — | — | — |

A class takes no wall timeout only when every child it covers is a long-lived server
that a clock would kill mid-service; a bounded child keeps its wall timeout even when
its class serves a long-lived purpose. The network column follows what a class's
children must reach: the server classes are judged by an HTTP readiness probe, and
`runtime-build` fetches from a package registry. Every stage-1 class still takes
rlimits, an output cap, a pinned cwd and the environment allowlist. DECISION F085 D7
below splits what was a single `dod` row and DECISION F085 D8 splits what was a single
`runtime` row; each split leaves the site total of the row it replaced unchanged.
END-AMEND8T

BEGIN-DEC8
## Amendment F085 D8 (2026-08-17) — the runtime class is not policy-homogeneous either

Ruled by the reviewer at the R49 gate under docs/agents/planner_reviewer_prompt.md
§4 item 7, applied here at R50. Reverse it by deleting this section and restoring
the single `runtime` row the policy table above replaced (`git log -p` on this
file). It changes the POLICY table only: Goal & Done, Task slicing and Do not touch
are untouched, and T002d still covers exactly the sites it always covered.

D7 split the `dod` row and left the identical defect standing one row below it.
Read at 25a5b42e, `.agent/f085_inventory.md` assigns five sites to `runtime`, and
its own `callee` and `timeout` columns already separate them. Three are `Popen`
calls that pass no timeout and start long-lived children —
`apps/cli/commands/runtime_cmd.py`:136, `packages/runtimes/dev_server.py`:1484 and
`packages/runtimes/runtime_supervisor.py`:235 — and each is judged by an HTTP
readiness probe, reported for the first through the supervisor's bounded filesystem
handshake. Two are `subprocess.run` calls inside `_auto_build_frontend`,
`packages/orchestration/ui_server.py`:2787 and :2800, which pass `timeout=120` and
run `npm install` and `npm run build` to completion. For that second pair a
no-wall-timeout policy does not relax a guard, it REMOVES a working one — the same
regression D7 identified for `_run_process_check`.

The sweep behind this amendment covered every stage-1 row rather than the row that
prompted it, read at 25a5b42e against the inventory's `callee` and `timeout`
columns. Only `dod-app` and `runtime` carried a no-wall-timeout policy, so only they
could hold this defect, and `dod-app`'s single site is a `Popen` that passes no
timeout and is consistent. The rows demanding a wall timeout a site does not yet
have — `builder` at `stream_evidence.py`:595, `test` at `ci_run.py`:79 and
`test_execution_service.py`:323 — are the change stage 1 exists to make and are not
this defect. Findings R-0552 and R-0553 carry the measurement.
END-DEC8

BEGIN-RECORD18
Gate: R50 — the R49 entry. R49 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer
over 1e0c14e0..25a5b42e, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r49.md`, the committed `.agent/authored/f085-r49.md` at
6f084636, the committed `.agent/last_block.md` at 8862abce and both working copies as they stand
at 25a5b42e are all five byte-EQUAL at sha256
fe04d524d02f044891f9ffb591b5aa83335a07c9ac0471bde02b6b20f13319dc, 24858 B, 345 lines, 12 marker
lines. THE SHAPES HELD, each measured separately from slices the reviewer extracted
programmatically from the committed block by marker pair rather than retyping them. THE TWO
REWRITES: PLAN3F occurs 0x and PLAN3T exactly 1x in `.agent/plan.md` at d5fb16a5 at numstat
`9 9`, and AMEND7F occurs 0x and AMEND7T exactly 1x in `docs/roadmap/features/T2_F085.md` at
7df0bf33 at numstat `8 5`; both pairs give `TO contains FROM: false`, as that block declared. THE
TWO PROSE APPENDS: for RECORD17 on `.agent/live_review.md` at 0131b21b and for DEC7 on the
feature file at ad9a38a8 the pre-commit blob is a byte-exact prefix, the remainder is exactly one
blank line plus the slice, the slice is an exact suffix, 0 marker LINES reached either file, and
every non-empty slice line occurs exactly once among that path's added lines — 93 slice lines of
which 3 empty against 94 added at numstat `94 0`, and 25 slice lines of which 3 empty against 26
added at numstat `26 0`. THE SUITES WERE RE-RUN, NOT READ, each in the primary checkout, each
exit 0: the four state readers `159 passed` against a base of 159, the canary `42 passed` against
42, the docs tier `295 passed` against 295. THE PLAN CONTRACT HELD at d5fb16a5: 39 lines against
the 50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id all present. THE ARITHMETIC
MOVED AS ORDERED: 166 / 27 / 0 at 25a5b42e against 164 / 27 / 0 at 1e0c14e0, 139 open against
137, the registered symmetric difference exactly R-0550 and R-0551, done and landed symmetric
differences EMPTY, no duplicate id and no resolution naming an unregistered id at either SHA, and
R-0552 free. HYGIENE IS CLEAN: over the six commits of 1e0c14e0..25a5b42e that precede the
handback the per-commit INSERTION counts, the column AGENTS.md DECISION F104 D1 fixes for the
cap, are 345, 283, 9, 94, 8 and 26, and the handback commit adds 99; none over 500 and so no
second call on the allowance d4473f85 spent; the path set of that range is exactly the six
ordered paths and nothing else; all seven commits are single-parent; the tree is clean and
`git worktree list` is one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives
TOTAL 345, PROSE 180 and RECORD17 93, each agreeing with what that block stated and each under
its DECISION F085 D6 cap. ONE DIFFERENCE IS NOTED AND IS NOT A DEFECT: the reviewer's slice byte
counts run one below the handback's on every slice, because the two extractors disagree about the
newline preceding an END marker; the six slice line counts agree at 12, 12, 10, 13, 25 and 93,
and the applied bytes are what G3 proved.

- R-0552 — Medium, SPEC DEFECT, THE `runtime` POLICY ROW COVERS SITES THAT DO NOT SHARE A POLICY,
AND ITS NO-WALL-TIMEOUT RULING WOULD REMOVE A TIMEOUT TWO OF THEM ALREADY HAVE. The `runtime` row
of the policy table in `docs/roadmap/features/T2_F085.md` at 25a5b42e gives all five of its sites
no wall timeout. Measured against `.agent/f085_inventory.md` at 25a5b42e, whose own `callee` and
`timeout` columns already separate them, three are `Popen` calls that pass no timeout and start
long-lived children — `apps/cli/commands/runtime_cmd.py`:136 in `_serve_supervisor`,
`packages/runtimes/dev_server.py`:1484 in `start` and
`packages/runtimes/runtime_supervisor.py`:235 in `run` — while two are `subprocess.run` calls
inside `_auto_build_frontend`, `packages/orchestration/ui_server.py`:2787 and :2800, which pass
`timeout=120` and run `npm install` and `npm run build` to completion. For that second pair a
no-wall-timeout policy does not relax a guard, it REMOVES a working one, which is word for word
the regression R-0551 identified for `_run_process_check` one row above. Medium for the reason
R-0551 was Medium: it would land as production behaviour at T002d, and both readings look
internally consistent at review time. THE COUNTER-MEASURE IS THIS ROUND'S OWN C3a AND C3b, which
split the row into `runtime-server` and `runtime-build` under DECISION F085 D8 and leave the site
total unchanged, so the inventory needs no edit. THE DEEPER COUNTER-MEASURE IS THE SWEEP: D7
fixed the `dod` row and left this one standing, which is the R-0417 shape of fixing the instance
rather than the class, so D8 states the reading it took over EVERY stage-1 row. Found and
registered by the reviewer while gating R49.

- R-0553 — Low, REVIEWER-BLOCK DEFECT, AN AUTHORED SLICE ASSERTED AN UNMEASURED UNIVERSAL OVER A
CLASS AND IS FALSE OF TWO OF ITS MEMBERS. AMEND7T, applied at 7df0bf33, rewrote the paragraph
under the policy table to say that the classes taking no wall timeout are the ones whose children
are long-lived servers and that "each is judged by a readiness probe over HTTP, so each keeps
network access". Measured at 25a5b42e, the two `_auto_build_frontend` sites R-0552 names sit in a
class that paragraph covers, and they are judged by `check=True` on a completed `npm` run rather
than by any HTTP probe, so the sentence is false of them however its quantifier is read — over
classes or over sites. This is checklist item 11 as R-0526 widened it: a universal asserted over
a set nobody enumerated, written by the reviewer in the very slice that was correcting the
identical defect one row above. Low, because no GATE was misreported — every gate R49 ordered is
reproducible and this reviewer reproduced all of them — and because the normative content of that
passage is the table, which this round corrects. THE COUNTER-MEASURE IS NOT A REWRITE of the
landed sentence: C3a replaces the paragraph as part of the D8 split, and its replacement states
the no-wall-timeout rule as a condition each class is tested against rather than as a universal
over an unenumerated set, while the per-site reading lives in DEC8 beside the SHA it was taken
at. Found and registered by the reviewer while gating R49.
END-RECORD18
