── STEP record+amend — F085 — R49 ────────────────────────────────────────────

Goal: record the R48 PASS, register R-0550 and R-0551, and amend the F085 feature file so the
`dod` class carries the two policies its two sites actually need. T002c cannot be implemented
correctly until that row is split, because the feature file and `.agent/plan.md` currently
contradict each other about it and BOTH are wrong against the code.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R48 and register R-0550 and R-0551 · C3a split the policy table ·
C3b append DECISION F085 D7 · C4 handback.

CONVENTION, binding on every count here: a line count is the `splitlines` reading — a trailing
newline is NOT an extra line. A slice is the bytes strictly between its marker lines.

## Change

C1 applies PLAN3F→PLAN3T to `.agent/plan.md`. C2 appends RECORD17 to `.agent/live_review.md`.
C3a applies AMEND7F→AMEND7T and C3b appends DEC7, both to
`docs/roadmap/features/T2_F085.md`. They are two commits and not one so that each carries its
own clean shape proof: an append proof needs a pre-commit blob the same commit did not already
rewrite. No `.py` file is touched, so no lint gate and no code suite is ordered; their absence
is declared here rather than filled with a command that could not see this round's change.

Change set, named rather than counted: `.agent/authored/f085-r49.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `docs/roadmap/features/T2_F085.md`,
`.agent/handoff.md`. Nothing else. `docs/roadmap/**` IS in that set, so the §3 docs tier
triggers and G5 carries it.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r49.md` by its marker pair. Never retype one, never apply one from
   the prompt. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C4; if it exists, finish the
   commit in flight, write the handback and stop. `git status --porcelain` is empty at round
   start and after every commit. This round orders no destructive check, so it creates no
   worktree and `git worktree list` stays one line.
3. PAIR SHAPES, each tested mechanically by the reviewer at emission, each output printed here
   per checklist item 15, one reading per pair and none generalised to another:
   - PLAN3F→PLAN3T on `.agent/plan.md` gives `TO contains FROM: false` → REWRITE, so the
     FROM 0x / TO 1x reading over the whole post-commit file is owed. The pair spans the
     `## Current Step` and `## Next Steps` sections and stops before the blank line preceding
     `## Risks`; `## Goal` and `## Risks` are unchanged and stay outside it.
   - AMEND7F→AMEND7T on `docs/roadmap/features/T2_F085.md` gives `TO contains FROM: false` →
     REWRITE, same FROM 0x / TO 1x obligation. Per checklist item 17 the FROM spans every table
     row from `dod` to the end of the table plus the paragraph beneath it, because the TO
     changes the table's ARITY by splitting one row into two.
   - RECORD17 and DEC7 are APPENDS of PROSE, each carrying no FROM, so no containment reading
     is owed for either. Each target stays a byte-exact prefix and exactly one blank line joins
     it to the slice.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of the amendment. Only
   C0a and C0b may precede it. This round registers findings, so §3 checklist item 23 binds it.
5. Every sentence in RECORD17 and in DEC7 that states a reading of a file THIS BLOCK also edits
   names the SHA 1e0c14e0 in the same clause, per checklist item 20 as R-0521 and R-0534 narrow
   it — the qualifier attaches to EVERY reading in the clause, not only the first.
   `.agent/plan.md` and `docs/roadmap/features/T2_F085.md` are both such files: C1 changes the
   first, C3a and C3b the second, and both slices land before C3a or read the base.
6. NO SLICE REPRODUCES THE RETIRED TABLE ROW. DEC7 describes the single `dod` row it replaces
   in prose and never quotes it, so G3's AMEND7F-0x reading stays attainable — checklist
   item 2, whose whole failure mode is a TO that quotes retired text on purpose.
7. Nothing outside the declared change set is touched. This round registers R-0550 and R-0551
   and resolves nothing: the open count goes 137 → 139, next free id R-0552.
8. If a gate comes out red, STOP: write the handback naming the exact command, its exit code
   and its output. Never edit a slice to make a gate green.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines
   TOTAL, PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all
   three at emission and states them here: TOTAL 345, PROSE 180, RECORD17 93. The worker
   re-measures all three from the committed `.agent/authored/f085-r49.md` and reports them; a
   mismatch is a finding against this block, not against the worker.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r49.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's `.remedy-wt/f085-r49.md` — disk-to-disk, not a digest fallback. Report sha256, byte
count, line count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - C1 / PLAN3F→PLAN3T / `.agent/plan.md`, a REWRITE: PLAN3F occurs 0x and PLAN3T exactly 1x in
   the post-commit file. Report both counts and `git show --numstat` for the path.
 - C2 / RECORD17 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's
   prose. §4.9's per-line obligation applies, and it is the PROSE form because the slice is
   prose: every non-empty line the slice contains occurs exactly once among the lines C2's diff
   adds TO THAT PATH. Report the slice's empty-line count and `git show --numstat`.
 - C3a / AMEND7F→AMEND7T / `docs/roadmap/features/T2_F085.md`, a REWRITE: AMEND7F occurs 0x and
   AMEND7T exactly 1x in the post-commit file. Report both counts and `git show --numstat`.
 - C3b / DEC7 / the same path, a PROSE APPEND against the blob C3a left: prefix, remainder of
   exactly one blank line plus the slice, exact suffix, 0 marker LINES, the same per-line
   obligation over C3b's added lines. Report the empty-line count and `git show --numstat`.

G4 SUITE, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read `.agent/` state
live, two of which assert on `.agent/plan.md`. Base reading at 1e0c14e0, taken by the reviewer
in the primary checkout: `159 passed`. REPORT the number this run prints. CANARY
`python3 -m pytest tests/cli/test_golden_path.py -q` — base at 1e0c14e0 `42 passed`.

G5 DOCS TIER, required because `docs/roadmap/**` is in the change set:
`python3 -m pytest tests/docs/ -q`, base at 1e0c14e0 `295 passed`, exit 0. REPORT the number.
WHAT THIS GATE DOES AND DOES NOT SEE, measured by the reviewer at 1e0c14e0 in a disposable
worktree with a red control: replacing the `dod` table row with garbage left it at
`295 passed` exit 0, and renaming `T2_F085.md` away made it `4 failed` exit 1. So it guards
the feature file's EXISTENCE and its F-id mapping and is blind to the file's BODY. It is
ordered because the tier requires it and because C3a and C3b must not break the mapping — not
as evidence that the amendment's text is right. G3 is that evidence.

G6 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer
collected by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains
`## Next Steps`, matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and each
of the three booleans. G4 covers the first three through their tests; this gate covers the cap,
which no test reads.

G7 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
1e0c14e0 and at HEAD, from the line-start patterns for a registration, a resolution and a
landed line. The reviewer's base reading is 164 / 27 / 0, 137 open, max registered R-0549, max
resolved R-0532. At HEAD registered must be 166, the registered symmetric difference exactly
R-0550 and R-0551, done and landed symmetric differences EMPTY, 139 open, next free id R-0552.
Report the three symmetric differences, the duplicate-id count and the count of resolutions
naming an unregistered id, at both SHAs.

G8 HYGIENE. `git diff --name-only 1e0c14e0..HEAD` measured BEFORE C4 holds exactly the change
set above minus `.agent/handoff.md`, which C4 writes, and nothing else. Report per-commit
insertions for every commit BEFORE C4 — C4 cannot measure itself, so its own insertions go in
the round report — and confirm none exceeds 500. This branch already spent the AGENTS.md
declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under constraint
8, never a declaration. Confirm every commit has exactly one parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch,
base SHA 1e0c14e0, a per-commit changed-files table, the item-status table covering C0a, C0b,
C1, C2, C3a, C3b and C4, the real G1-G8 results with exit codes, the open-findings count and
the next expected action. This round has more than five commits, so the ≤100-line allowance
applies; beyond that, name the DECISION D15 stated cause and the mandated content behind it.
Repeat this Fortschritt line verbatim:
Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R48 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c entsperrt durch Amendment F085 D7, noch nicht gebaut ·
T002d, T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next
round is R50, started by a FRESH session, and it implements T002c under the policy DECISION
F085 D7 rules — `_run_process_check`
onto the guard seam KEEPING its wall timeout and closing its `env=os.environ.copy()` gap, and
`_run_app_once` under the dod-app policy with no wall timeout and network allowed; T002d, T003,
the integration gate and closure follow. TWO: R49's own verdict is NOT on disk as a gate entry,
because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a missing
gate, and R50 must not open a repair round to close it; R49's verdict, when the reviewer issues
it, is recorded by R50's OWN record slice. THREE: a standalone closing line stating the open
findings count and the next free id as its own sentence, not only inside a gate transcript.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, because the self-drive protocol
requires every handoff that names the next session's first action to name that rule ahead of
the Open PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN3F
## Current Step
R48, this round: record the R47 PASS and register R-0549 for the session-resume clauses the R47
handback dropped. A record-only round, so the verdict reaches disk before the session that
issued it ends; T002c opens at R49. No source file changes this round.

## Next Steps
1. T002c — the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy differs
   from the `test` class in taking no wall timeout, because their children are the long-lived
   harness rather than a bounded suite run.
2. T002d — the five runtime sites, under that same no-wall-timeout policy.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLAN3F

BEGIN-PLAN3T
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
END-PLAN3T

BEGIN-AMEND7F
| dod | 2 | yes | yes | yes | yes | yes | yes | default-deny |
| runtime | 5 | yes | yes | NO | yes | yes | yes | allowed |
| git | 24 | no | — | — | — | — | — | — |
| packaging | 11 | no | — | — | — | — | — | — |
| other | 8 real | no | — | — | — | — | — | — |

The runtime class differs because its children are long-lived servers: a wall
timeout would kill the very harness the class exists to serve, and that harness
needs its port. It still takes rlimits, an output cap, a pinned cwd and the
environment allowlist.
END-AMEND7F

BEGIN-AMEND7T
| dod-process | 1 | yes | yes | yes | yes | yes | yes | default-deny |
| dod-app | 1 | yes | yes | NO | yes | yes | yes | allowed |
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
END-AMEND7T

BEGIN-DEC7
## Amendment F085 D7 (2026-08-17) — the dod class is not policy-homogeneous

Ruled by the reviewer at the R48 gate under docs/agents/planner_reviewer_prompt.md
§4 item 7, applied here at R49. Reverse it by deleting this section and restoring
the single `dod` row the policy table above replaced (`git log -p` on this file).
It changes the POLICY table only: Goal & Done, Task slicing and Do not touch are
untouched, and T002c still covers exactly the two sites it always covered.

Read at 1e0c14e0, the two sites `.agent/f085_inventory.md` assigns to `dod` do not
share a policy, and Amendment F085 D1 gave them one row. `_run_process_check` runs
one bounded check — pytest, lint, build or a custom command — and already passes
`timeout=ctx.timeout_sec`, so a wall timeout is correct for it and removing one
would be a regression; its real stage-1 gap is `env=os.environ.copy()`, which
hands the child the whole parent environment. `_run_app_once` starts the
application itself with `Popen(..., start_new_session=True)`, waits for it with
`http_probe` against `spec.health_path`, and stops it in a `finally`; a guard wall
timeout would kill the harness mid-probe, and a default-deny network posture would
break the very probe that judges it. Its lifetime is already bounded — by the
caller's deadline and by that `finally` — rather than by a clock the guard holds.

The correction runs in both directions, which is why it is an amendment and not a
typo fix: the D1 table understated `_run_app_once` by giving it a wall timeout and
default-deny, while `.agent/plan.md` at 1e0c14e0 overstated the same class in the
opposite direction by putting BOTH sites under "no wall timeout". Finding R-0551
carries the measurement.
END-DEC7

BEGIN-RECORD17
Gate: R49 — the R48 entry. R48 PASSED. Every ordered gate G1-G7 was re-executed by the reviewer
over d6b06997..1e0c14e0, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r48.md`, the committed `.agent/authored/f085-r48.md` at
452ffd2b, the committed `.agent/last_block.md` at 5e81e727 and both working copies as they
stand at 1e0c14e0 are all five byte-EQUAL at sha256
da6fd5a6a1de5b03d5f78f39c312a04c6504fe39a51065a82088fde08751ca38, 15488 B, 213 lines, 6 marker
lines. THE SHAPES HELD, each measured separately from slices the reviewer extracted
programmatically from the committed block by marker pair rather than retyping them. THE
REWRITE: PLAN2F occurs 0x and PLAN2T exactly 1x in `.agent/plan.md` at 360897f7, with
`TO contains FROM: false` as that block declared, numstat `3 4`. THE PROSE APPEND: for RECORD16
on `.agent/live_review.md` at 3bc7977b the pre-commit blob is a byte-exact prefix, the remainder
is exactly one blank line plus the slice, the slice is an exact suffix, 0 marker LINES reached
the file, and every non-empty slice line occurs exactly once among that path's added lines — 60
slice lines of which 2 empty against 61 added, numstat `61 0`. THE SUITES WERE RE-RUN, NOT READ,
each in the primary checkout, each exit 0: the four state readers `159 passed` against a base of
159, the canary `42 passed` against 42. THE PLAN CONTRACT HELD at 1e0c14e0: 39 lines against the
50-line cap, `## Goal`, `## Next Steps` and a roadmap F-id all present. THE ARITHMETIC MOVED AS
ORDERED: 164 / 27 / 0 at 1e0c14e0 against 163 / 27 / 0 at d6b06997, 137 open against 136, the
registered symmetric difference exactly R-0549, done and landed symmetric differences EMPTY, no
duplicate id and no resolution naming an unregistered id at either SHA. HYGIENE IS CLEAN: over
the five commits of d6b06997..1e0c14e0 the per-commit INSERTION counts, the column AGENTS.md
DECISION F104 D1 fixes for the cap, are 213, 140, 3, 61 and 34, none over 500 and so no second
call on the allowance d4473f85 spent; the path set of the range ending at 3bc7977b is exactly
the four ordered paths and the full range adds only `.agent/handoff.md`; all five commits are
single-parent; the tree is clean and `git worktree list` is one line. THE BLOCK'S OWN SIZE
re-measured from the committed file gives TOTAL 213, PROSE 144 and RECORD16 60, all three
agreeing with what that block stated.

TWO CLAIMS THAT BLOCK MADE ABOUT EARLIER ROUNDS WERE RE-MEASURED RATHER THAN TRUSTED, because a
record repeating an unverified number launders it. R47's per-commit insertions over
c8da1928..d6b06997 really are 308, 259, 8, 62, 36 and 42. R47's five-copy transport really does
hold at sha256 a1d2fe72fd6425b5bbf3a06d13e9eb25dbebabb80bfd8a10e49694251cb5530f, 22123 B, 308
lines, 14 marker lines. RECORD16's checklist-structure claim holds WITHIN THE BOUNDS IT NAMES:
walking `docs/agents/planner_reviewer_prompt.md` at d6b06997 from its introductory checklist
bullet to the line beginning `  Why this is on disk` gives the numerals 1 through 23 ascending
with no duplicate and no gap. Read over the WHOLE file that same pattern also matches the
Verification-tiers list further down, so the bound is load-bearing and the claim is true only
because it states one. ONE DIFFERENCE IS NOTED AND IS NOT A DEFECT: the reviewer's slice digests
differ from the handback's by exactly one byte per slice, because the reviewer's extractor keeps
the newline before the END marker and the worker's dropped it; all three line counts agree at
5, 4 and 60, and the applied bytes are what G3 proved.

- R-0550 — Low, REVIEWER-BLOCK DEFECT, A RECORD SLICE STATED A PRESENT-TENSE READING OF A FILE
ITS OWN BLOCK REWROTE ONE COMMIT EARLIER. RECORD16 closes its plan-contract sentence with "THE
PLAN CONTRACT HOLDS: 40 lines against the 50-line cap", and that clause names no commit. The
reading was true of `.agent/plan.md` at d6b06997, where the file is 40 lines. C1 of that same
round, 360897f7, made it 39, and RECORD16 landed at C2, 3bc7977b — one commit LATER. So the
sentence was false of the file it describes at the moment it reached disk, and it is false at
1e0c14e0 too. This is exactly checklist item 20, the R-0520 class, and the block did not miss
the rule: its own constraint 5 asserted that "every sentence in RECORD16 that reads a file THIS
BLOCK also edits names the SHA d6b06997 in the same clause". That constraint is false of its
own slice twice over — this sentence names no SHA at all, and the one plan-reading sentence
that DOES name one names 3fe2667d, which is correct on the merits and is not the SHA the
constraint promised. A constraint asserting a property its own slice does not have is the
R-0527 shape checklist item 11 governs, so the two items met in one paragraph. Low, because
nothing about a GATE was misreported: every gate result RECORD16 states is reproducible, this
reviewer reproduced all of them, and the damage is one stale number in a permanent record.
THE COUNTER-MEASURE IS NOT A REWRITE. Item 20 fixes that explicitly — appending a correction is
how this record stays honest, and overwriting landed text is worse than a dated wrong sentence
— so the sentence stays and this paragraph is its correction. What changes is the emission
step: a constraint of the form "every sentence in X names SHA Y" is MEASURED sentence by
sentence before emission, in the same way item 15 requires a containment test per pair rather
than one reading generalised across pairs, because a universal asserted over a slice's own
sentences is the recollection item 11 exists to forbid. Found and registered by the reviewer
while gating R48.

- R-0551 — Medium, SPEC DEFECT, THE `dod` POLICY ROW COVERS TWO SITES THAT DO NOT SHARE A
POLICY, AND THE TWO DOCUMENTS DESCRIBING IT CONTRADICT EACH OTHER AND THE CODE. Amendment F085
D1 in `docs/roadmap/features/T2_F085.md` at 1e0c14e0 gives `dod` one row reading wall timeout
`yes` and network `default-deny` for both of its sites. `.agent/plan.md` at 1e0c14e0 says the
opposite of the same two sites — "whose policy differs from the `test` class in taking no wall
timeout, because their children are the long-lived harness rather than a bounded suite run" —
and the R48 handback at 1e0c14e0 repeats it. Measured against the code at 1e0c14e0, both are
wrong, in opposite directions, and each is right about one site. `.agent/f085_inventory.md`
assigns exactly `packages/orchestration/dod_runners.py`:302 and :575 to the class.
`_run_process_check`, the first, runs ONE BOUNDED CHECK — its docstring says "a check that IS
one process: pytest, lint, build, custom_cmd" — and already passes `timeout=ctx.timeout_sec`
with a `subprocess.TimeoutExpired` handler that classifies the trip; it is not a long-lived
harness, it keeps its wall timeout, and its actual stage-1 gap is `env=os.environ.copy()`.
`_run_app_once`, the second, starts the application with
`Popen(..., start_new_session=True)`, waits with `http_probe` against `spec.health_path` over
`http://<host>:<port>`, and stops it in a `finally`; a wall timeout would kill the harness
mid-probe and a default-deny network posture would break the probe that judges it, which is
word for word the reason D1 already gives for excusing the `runtime` class. THE CONSEQUENCE IS
THAT T002c COULD NOT HAVE BEEN BUILT CORRECTLY FROM EITHER DOCUMENT: following the feature file
puts a killing clock and a network denial on the app harness, and following the plan strips a
working timeout off a bounded check. Medium rather than Low because it would have landed as
production behaviour and the wrong half is invisible at review time — both readings look
internally consistent. THE COUNTER-MEASURE IS THIS ROUND'S OWN C3a AND C3b: the row splits into
`dod-process` and `dod-app` under DECISION F085 D7, ruled per §4 item 7, and `.agent/plan.md`
is corrected by C1 in the same round so the two documents agree. The site total is unchanged,
so the inventory needs no edit. Found and registered by the reviewer while planning T002c.
END-RECORD17
