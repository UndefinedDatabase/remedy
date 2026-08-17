── STEP record — F085 — R48 ──────────────────────────────────────────────────

Goal: record the R47 PASS and register R-0549 for the session-resume clauses the R47 handback
dropped, so the verdict is on disk rather than only in a session that is about to end. This is
a record-only round by design: T002c opens at R49 with a fresh session's budget.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R47 and register R-0549 · C3 handback.

CONVENTION, binding on every count here: a line count is the `splitlines` reading — a trailing
newline is NOT an extra line.

## Change

C1 applies PLAN2F→PLAN2T to `.agent/plan.md`. C2 appends RECORD16 to `.agent/live_review.md`.
No source file is touched this round and no `.py` path changes, so no lint gate and no code
suite is ordered — their absence is declared here rather than filled with a command that could
not see this round's change.

Change set, named rather than counted: `.agent/authored/f085-r48.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md`. Nothing else; neither `docs/**`
nor `docs/roadmap/**` is in that set, so the §3 docs tier does not trigger.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r48.md` by its marker pair. Never retype one, never apply one from
   the prompt. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C3; if it exists, finish the
   commit in flight, write the handback and stop. `git status --porcelain` is empty at round
   start and after every commit; this round orders no destructive check, so it creates no
   worktree and `git worktree list` stays one line.
3. PAIR SHAPE, tested mechanically by the reviewer at emission and its output printed here per
   checklist item 15: PLAN2F→PLAN2T on `.agent/plan.md` gives `TO contains FROM: false` →
   REWRITE, so the FROM 0x / TO 1x reading over the whole post-commit file is owed. The pair
   spans the `## Current Step` section ONLY: `## Next Steps` and `## Risks` are unchanged this
   round and stay outside it. RECORD16 is an APPEND of PROSE to `.agent/live_review.md` — the
   target stays a byte-exact prefix, exactly one blank line joins it to the slice, nothing is
   reflowed, and it carries no FROM, so no containment reading is owed for it.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record. Only C0a and C0b may precede it.
   This round registers a finding, so §3 checklist item 23 — added at 522d925a, one round ago —
   binds it, and this is the second round to apply that item and the first to apply it as a
   standing rule rather than as the round that wrote it.
5. Every sentence in RECORD16 that reads a file THIS BLOCK also edits names the SHA d6b06997
   in the same clause, per checklist item 20 as R-0521 narrows it. `.agent/plan.md` is that
   file: C1 changes it, and RECORD16's reading of it is taken at the base.
6. Nothing outside the declared change set is touched. This round registers R-0549 and
   resolves nothing: the open count goes 136 → 137, next free id R-0550.
7. If a gate comes out red, STOP: write the handback naming the exact command, its exit code
   and its output. Never edit a slice to make a gate green.
8. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines
   TOTAL, PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all
   three at emission and states them here: PROSE 144, TOTAL 213, RECORD16 60 lines. The worker
   re-measures all three from the committed `.agent/authored/f085-r48.md` and reports them; a
   mismatch is a finding against this block, not against the worker.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r48.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's `.remedy-wt/f085-r48.md` — disk-to-disk, not a digest fallback. Report sha256, byte
count, line count and marker-line count. Measure every one.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - C1 / PLAN2F→PLAN2T / `.agent/plan.md`, a REWRITE: PLAN2F occurs 0x and PLAN2T occurs exactly
   1x in the post-commit file. Report both counts and `git show --numstat` for the path.
 - C2 / RECORD16 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's
   prose. §4.9's per-line obligation applies: every non-empty line the slice contains occurs
   exactly once among the lines C2's diff adds TO THAT PATH; report the slice's empty-line
   count. Report `git show --numstat` for the path.

G4 SUITE, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read `.agent/` state
live, two of which assert on `.agent/plan.md` and are the reason this is the right class for
C1; base reading at d6b06997, taken by the reviewer in the primary checkout, `159 passed`.
REPORT the number this run prints. CANARY
`python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer
collected by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains
`## Next Steps`, matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and each
of the three booleans. G4 covers the first three through their tests; this gate covers the cap,
which no test reads.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
d6b06997 and at HEAD, from the line-start patterns for a registration, a resolution and a
landed line. The reviewer's base reading is 163 / 27 / 0, 136 open, max registered R-0548, max
resolved R-0532. At HEAD registered must be 164, the registered symmetric difference exactly
R-0549, done and landed symmetric differences EMPTY, 137 open, next free id R-0550. Report the
three symmetric differences, the duplicate-id count and the count of resolutions naming an
unregistered id, at both SHAs.

G7 HYGIENE. `git diff --name-only d6b06997..HEAD` measured BEFORE C3 holds exactly the change
set above minus `.agent/handoff.md`, which C3 writes, and nothing else. Report per-commit
insertions for every commit BEFORE C3 — C3 cannot measure itself, so its own insertions go in
the round report — and confirm none exceeds 500. This branch already spent the AGENTS.md
declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under constraint
7, never a declaration. Confirm every commit has exactly one parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch,
base SHA d6b06997, a per-commit changed-files table, the item-status table covering C0a, C0b,
C1, C2 and C3, the real G1-G7 results with exit codes, the open-findings count and the next
expected action. Keep it inside the 60-line cap, or name the DECISION D15 stated cause and the
exact mandated content behind it. Repeat this Fortschritt line verbatim:
Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R47 PASS ·
T002a KOMPLETT · T002b KOMPLETT, alle Sites der Klasse auf dem Seam · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries FOUR statements. R-0549 exists because the R47 handback carried
the first, carried part of the second and dropped the rest. ONE: the next round is R49, started
by a FRESH session, and it
opens T002c with the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy
differs from the `test` class because their children are the long-lived harness and take no
wall timeout; T002d, T003, the integration gate and closure follow. TWO: R48's own verdict is
NOT on disk as a gate entry, because the round that records a verdict cannot record one on
itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a
missing gate, and R49 must not open a repair round to close it; R48's verdict, when the
reviewer issues it, is recorded by R49's OWN record slice, and naming that successor is the
half whose absence this round registers. THREE: a standalone closing line stating the open
findings count and the next free id as its own sentence, not only inside a gate transcript.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, because the self-drive protocol
requires every handoff that names the next session's first action to name that rule ahead of
the Open PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN2F
## Current Step
R47, this round: record the R46 PASS, register R-0548 for the plan-path defect R46's handback
declared, and promote two counter-measures into the §3 pre-emission checklist — item 16 widened
past headings, and a new item 23 carrying the plan-path rule R-0377 and R-0491 state only as
finding prose. No source file changes this round.
END-PLAN2F

BEGIN-PLAN2T
## Current Step
R48, this round: record the R47 PASS and register R-0549 for the session-resume clauses the R47
handback dropped. A record-only round, so the verdict reaches disk before the session that
issued it ends; T002c opens at R49. No source file changes this round.
END-PLAN2T

BEGIN-RECORD16
Gate: R48 — the R47 entry. R47 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer
over c8da1928..d6b06997, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r47.md`, the committed `.agent/authored/f085-r47.md` at
e0eee32f, the committed `.agent/last_block.md` at 313e8321 and both working copies as they
stand at d6b06997 are all five byte-EQUAL at sha256
a1d2fe72fd6425b5bbf3a06d13e9eb25dbebabb80bfd8a10e49694251cb5530f, 22123 B, 308 lines, 14 marker
lines. THE SHAPES HELD, each measured separately from slices the reviewer extracted
programmatically from the committed block by marker pair rather than retyping them. THE REWRITE:
R47's PLANF occurs 0x and its PLANT exactly 1x in `.agent/plan.md` at 3fe2667d, with
`TO contains FROM: false` as that block declared, numstat `8 9`. THE PROSE APPEND: for RECORD15
on `.agent/live_review.md` the pre-commit blob is a byte-exact prefix, the remainder is exactly
one blank line plus the slice, the slice is an exact suffix, 0 marker LINES reached the file,
and every non-empty slice line occurs exactly once among that path's added lines — 61 slice
lines of which 2 empty against 62 added, at sha256 a2f71483…. THE TWO CHECKLIST APPENDS: on
`docs/agents/planner_reviewer_prompt.md` at 522d925a, C16F and C23F each occur exactly 1x and
C16T and C23T each exactly 1x, `TO contains FROM: true` for both as declared, 18 TO-only lines
each against the 36 lines that commit adds to the path, 0 violations, 0 marker LINES, numstat
`36 0`. THE SUITES WERE RE-RUN, NOT READ, each in the primary checkout, each exit 0: the four
state readers `159 passed` against a base of 159, the canary `42 passed` against 42. THE PLAN
CONTRACT HOLDS: 40 lines against the 50-line cap, `## Goal`, `## Next Steps` and a roadmap F-id
all present — the union of every assertion the reviewer collected by grepping `tests/`. THE
ARITHMETIC MOVED AS ORDERED: 163 / 27 / 0 at d6b06997 against 162 / 27 / 0 at c8da1928, 136 open
against 135, the registered symmetric difference exactly R-0548, done and landed symmetric
differences EMPTY, no duplicate id and no resolution naming an unregistered id at either SHA.
THE CHECKLIST STRUCTURE IS INTACT: walking the region from its introductory bullet to the line
beginning `  Why this is on disk` gives the numerals 1 through 23 ascending with no duplicate
and no gap, and no line matches `^  24\. ` anywhere in the file, so item 23 landing at the END
of the list renumbered no surviving entry — the answer item 17 asks for. HYGIENE IS CLEAN: the
per-commit insertion counts are 308, 259, 8, 62, 36 and 42, none over 500 and so no second call
on the allowance d4473f85 spent; the path set of the range ending at 522d925a is exactly the
five ordered paths and the full range adds only `.agent/handoff.md`; all six commits are
single-parent; the tree is clean and `git worktree list` is one line.

THE PROMOTION IS REAL, NOT MERELY APPLIED. Read at d6b06997, item 16 of the §3 checklist now
reaches a finding headline and a quantifying sentence as well as a heading, and a VALUE a body
fixes as well as a COUNT; item 23 now carries the plan-path rule that R-0377 and R-0491 had
stated only in their own bodies. R47's own C1 advanced `.agent/plan.md` ahead of every other
substantive commit, which is item 23 binding the round that wrote it.

- R-0549 — Low, REVIEWER-BLOCK DEFECT, A HANDBACK'S CLOSING SECTION LOST THREE CLAUSES THE
PREVIOUS ONE CARRIED, AND ONE OF THEM NAMES WHO RECORDS THE VERDICT. Measured by diffing the
`## Next` sections of `.agent/handoff.md` at c8da1928 and at d6b06997: the R46 handback closes
with the successor clause "R46's verdict, when the reviewer issues it, is recorded by R47's own
record slice", a standalone line "Open findings: 135, next free id R-0548" and the pointer
"Phase 1 rule 1 first: re-read `.agent/STOP` from disk". The R47 handback carries none of the
three. Its open-findings count survives only inside the G6 transcript, where a resuming session
reading the `## Next` section alone will not meet it. THE CONSEQUENCE IS THE ONE THIS WORKFLOW
CANNOT ABSORB: R47's handback tells R48 not to open a repair round over the missing gate entry
and never says that R48's record slice is what writes the verdict instead, so a verdict issued
at the end of a session can be stranded in that session — the handoff is the only return
channel, and the clause that routes the verdict onto disk is the one that went missing. The
protocol's own Phase 2 requires the STOP pointer by name, so its loss is a rule broken rather
than a habit skipped. THE CAUSE IS THE R47 BLOCK, not its worker: that block's Handback section
ordered the successor clause and the repair-round warning but omitted all three of these, and
the worker wrote exactly what was ordered. Low, because nothing false was written and every
gate held; the cost is a resume hazard, not a wrong record. The counter-measure is this round's
own Handback section, which enumerates all four closing statements explicitly instead of
naming the section and trusting the previous round's shape to carry over. Found and registered
by the reviewer while gating R47.
END-RECORD16
