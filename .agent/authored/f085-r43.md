── STEP T002b record — F085 — R43 ────────────────────────────────────────────

Goal: record the R42 PASS and register R-0537 and R-0538, two defects in the reviewer's own
R-0536 text. No production code this round: the `ci_run.py` migration is authored and proved
but its block measures 487 lines against the 400-line cap of DECISION F105 D5, so R44 carries
it. RECORD11 states that on disk.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R42 and
register R-0537 and R-0538 · C2 the plan · C3 handback.

CONVENTION, binding on every count in this block: a line count is the `splitlines` reading —
a trailing newline is NOT an extra line. This is what R-0536 registered.

## Change

C1 appends RECORD11 to `.agent/live_review.md` and nothing else. C2 applies PLANF11 to
PLANT11 and PLANF12 to PLANT12 in `.agent/plan.md` and nothing else.

Change set, named rather than counted: `.agent/authored/f085-r43.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. Nothing else. No `.py`
file changes, so this round orders no ruff run and no red proof. Neither `docs/**` nor
`docs/roadmap/**` is in that set, so no docs tier triggers.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r43.md` by its marker pair. Never retype one, never apply one from
   the prompt. Marker lines never reach a target file.
2. Pair shape, MEASURED by the reviewer with a containment test and recorded here as that
   test's OUTPUT, one reading per pair. PLANF11 to PLANT11: `TO contains FROM: false`.
   PLANF12 to PLANT12: `TO contains FROM: false`. Both are therefore REWRITES and each is
   owed the FROM 0x / TO 1x reading. Each FROM was measured to occur exactly 1x in
   `.agent/plan.md` at 4c7bcb3a and each TO exactly 0x there. RECORD11 is an append and
   carries no FROM.
3. Re-read `.agent/STOP` from disk before C0a and again before C3. If it exists, finish the
   commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This round orders
   no destructive check, so it creates no worktree; `git worktree list` is one line
   throughout.
5. C1 is an APPEND: the pre-commit file stays a byte-exact prefix, exactly one blank line
   joins it to the slice, and the slice is not reflowed, re-wrapped or re-indented.
6. Nothing outside the declared change set is touched. This round registers R-0537 and R-0538
   and resolves nothing, so the open count moves from 124 to 126.
7. If a gate comes out red, or either PLAN FROM does not match at exactly one place, STOP:
   write the handback naming the exact command, its exit code and its output, and do not
   improvise a repair.
8. STALENESS, standing: after C2 re-read every file this round edited and confirm no sentence
   this round put on disk was falsified by a later commit of the same round, and that no slice
   quotes another file's current wording as a claim. Name what was re-read and report the
   measurement, not a restatement of this sentence. Give special attention to any trailing
   reading whose clause qualifies an EARLIER reading with a SHA — R-0538, which this round
   registers, is the third consecutive instance of that shape.
9. Do not "repair" any landed text. The sentences R-0537 and R-0538 register stay in commit
   dc34997a. The registration IS the correction — checklist item 20.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 3; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r43.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's own `.remedy-wt/f085-r43.md` — disk-to-disk, not a digest fallback. Report the
sha256, byte count, line count, marker-line count, and region digests over lines 1-100 and
101-end, each with trailing newlines included and each with its own byte count so an empty
region is visible as empty. Measure every one; compute none by hand.

G3 APPEND SHAPE for C1 on `.agent/live_review.md`: the pre-commit blob is a byte-exact PREFIX
of the post-commit file; the remainder is exactly one blank line plus RECORD11; the slice is
an exact suffix; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker
LINES, never the substring, because that regex already appears in that file's prose. RECORD11
is PROSE, so the §4.9 per-line obligation applies and is ordered: every line the slice
contains occurs exactly once among the lines C1's diff adds, EXCEPT the empty line, which is
exempt because a paragraph break repeats by construction — report how many empty lines the
slice holds rather than counting them as failures. The reviewer measured RECORD11 to hold no
duplicate non-empty line, so a violation is a transport fault rather than a property of the
text. Report `git show --numstat` for the path.

G4 THE PLAN at HEAD after C2, proved by reconstruction rather than by counting: take
`.agent/plan.md` at 4c7bcb3a, replace PLANF11 with PLANT11 and PLANF12 with PLANT12, and
confirm the result is byte-identical to the committed file; report both sha256 values. Then
report PLANF11 0x, PLANT11 1x, PLANF12 0x and PLANT12 1x at HEAD, that the file still carries
`## Goal` and `## Next Steps`, that 0 marker lines reached it, and `git show --numstat` for
C2. The reviewer's dry run puts the file at 47 lines on the convention stated above, against
the 50-line AGENTS.md cap — report the number rather than asserting it.

G5 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at
base 4c7bcb3a and at HEAD, from the line-start patterns for a registration, a resolution and a
landed line. The reviewer's base reading is 151 / 27 / 0, 124 open, max registered R-0536, max
resolved R-0532. At HEAD it must be 153 / 27 / 0, 126 open, max registered R-0538, max
resolved R-0532. Report the registered symmetric difference (exactly R-0537 and R-0538), the
done and landed symmetric differences (both empty), the duplicate-id count, the count of
resolutions naming an unregistered id, and the next free id, which moves from R-0537 to R-0539.

G6 SUITES, each in the PRIMARY checkout and never in a worktree (R-0518), each as its exact
command line, each exit 0. Both base readings were taken by the reviewer at 4c7bcb3a.
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read `.agent/`
  state live; base reading `159 passed`. A red naming
  `TestVitestFrontendTestFoundation::test_vitest_passes` with `apps/ui/node_modules` absent IS
  finding R-0518 and means the command ran in a worktree; re-run it in the primary checkout.
  Any other red is a STOP under constraint 7.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base reading `42 passed`.

G7 HYGIENE. `git diff --name-only 4c7bcb3a..HEAD` measured BEFORE C3 holds exactly the change
set above minus `.agent/handoff.md`, which C3 writes, and nothing else. Report per-commit
insertions for every commit BEFORE C3 — C3 cannot measure itself, so its own insertions go in
the round report — and confirm none exceeds 500. Confirm every commit has exactly one parent
and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch,
base SHA 4c7bcb3a, a per-commit changed-files table, the item-status table covering C0a, C0b,
C1, C2 and C3, the real G1-G7 results with exit codes, the open-findings count and the next
expected action. Keep it inside the 60-line cap, or name the DECISION D15 stated cause and the
exact mandated content behind it. Repeat this Fortschritt line verbatim:
Fortschritt: ~77 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R42 PASS ·
T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, `ci_run.py` als DECISION F085 D4 gerulet
und die Migration fertig vermessen, R44 setzt sie um · T002c-d, T003 offen) — Schätzung, gegen
die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section states that the next round is R44; that R44 applies DECISION F085 D4 to
`packages/orchestration/ci_run.py` — `_run_via_subprocess` onto `run_guarded_test_command`,
the per-stage budget through the `extra_env` overlay that landed at dce66faa, the captured
stdout and stderr re-emitted before returning, the guard's wall set above `stage.timeout_sec`
as a backstop, and five tests covering the three behavioural deltas; that
`packages/orchestration/builder_bridge.py` follows as the last `test`-class site, then
T002c-d, then T003 and the integration gate; and that R44's first reviewed act is recording
R43's gate entry.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD11
Gate: R43 — the R42 entry. R42 PASSED. Every ordered gate was re-run by the reviewer over
0e2cdacd..4c7bcb3a and each reproduces the handback's reading. LINE COUNTS HERE ARE
`splitlines` COUNTS. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch
file `.remedy-wt/f085-r42.md`, the committed `.agent/authored/f085-r42.md` and
`.agent/last_block.md` at 7b02da1c, and the working copies of those two paths as they stand
at 4c7bcb3a, are all five byte-EQUAL at sha256 b6ba3371…f7161c25, 23195 B, 332 lines, 8
marker lines, region 1-100 at 3bc171fb05e29fa9 over 6720 B and region 101-end at
d0ad2b78183925d3 over 16475 B. BOTH APPENDS HELD THEIR SHAPE: at dc34997a a pre-commit blob
of 420193 B is a byte-exact prefix of the 426006 B post-commit file, its 5813 B remainder is
exactly one blank line plus RECORD10 — sha256 407c8ff2e3c61ac6…, 5812 B, 71 lines, 3 empty —
an exact suffix, numstat 72/0, each of the 68 non-empty slice lines occurring exactly once
among the 72 added and the added lines equal to blank-plus-slice IN ORDER; at 5695c2b0 the
same shape holds for DEC4 over 358646 B and 363135 B with a 4489 B remainder — sha256
fa6f2e9fd40c883f…, 4488 B, 60 lines, 6 empty — numstat 61/0, 54 non-empty lines each once
among the 61 added, ordered equality holding. No marker line reached either file at
4c7bcb3a. THE ARITHMETIC MOVED AS ORDERED: 149 / 27 / 0 at 0e2cdacd against 151 / 27 / 0 at
4c7bcb3a, 122 open against 124, registered symmetric difference exactly R-0535 and R-0536,
done and landed symmetric differences empty, and at each of those two SHAs no duplicate id
and no resolution naming an unregistered id. THE DECISION LANDED: lines matching
`^## DECISION F085 D\d+ —` number 2 at 0e2cdacd against 3 at 4c7bcb3a, the D4 heading occurs
exactly 1x at 4c7bcb3a, and there is no D1 section at either SHA. THE PLAN PAIR LANDED AS A
REWRITE: PLANF10 1x and PLANT10 0x at 0e2cdacd against 0x and 1x at 4c7bcb3a, `## Goal` and
`## Next Steps` present at both, no marker line at either, numstat 7/8, and `.agent/plan.md`
measuring 46 lines at 0e2cdacd and 45 at 4c7bcb3a, each under the 50-line cap. THE SUITES
WERE RE-RUN, NOT READ, each in the primary
checkout, each exit 0: the four state readers `159 passed` against a base of 159, and the
canary `42 passed` against 42. HYGIENE IS CLEAN: walking 0e2cdacd..4c7bcb3a mechanically
gives the per-commit insertion counts 332, 273, 72, 61, 7 and 122, none over 500; the path
set at 7c4a2583 is exactly the five ordered paths; all six commits are single-parent; and at
4c7bcb3a `git reflog -10` held ten entries of no non-`commit:` kind while `git worktree
list` held one line. The handback at 4c7bcb3a runs to 153 lines and carries the DECISION D15
stated cause, whose named content is mandated rather than padding.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraints 8 and 9 R42's worker measured the
reviewer's own RECORD10 and DEC4 against the repository, declared one reading that differs
and repaired none — again the round's finding came out of the constraint-8 report, as
RECORD10 recorded for R41. R-0538 is that reading; R-0537 is the reviewer's own, found while
re-reading R-0536 at this gate. R42's execution reproduced under independent re-run in every
particular.

WHY R43 SHIPS NO CODE. The `ci_run.py` migration DECISION F085 D4 rules was authored in full
for this round and proved before being deferred: applied to two disposable worktrees at
4c7bcb3a, linted clean, run to `59 passed` there against a base of `54 passed` at the same
commit, and red-controlled on four separate mutations, each of which exited non-zero. Its
step block then measured 487 lines against the 400-line cap DECISION F105 D5 sets, and
checklist item 1 requires the split BEFORE emission rather than a declared deviation
afterwards. The migration is R44's, and it starts from measured slices rather than from a
design.

- R-0537 — Low, A FINDING'S HEADLINE COUNTED FOUR OF SOMETHING ITS BODY GIVES THREE OF.
R-0536, applied at commit dc34997a, opens "A BLOCK PREDICTED FOUR LINE COUNTS UNDER AN
UNSTATED NEWLINE CONVENTION AND EVERY ONE READ ONE HIGH", and its body then quotes three
predictions from the R41 block — "707 lines at HEAD against 644 at 93226220" and "put it at
47 lines" — and measures three values against them, "706, 643 and 46". Measured at 4c7bcb3a:
the R41 block, committed at 9cc4772c, predicts exactly three line counts; its other numerals
of that family are the 50-line and 60-line caps it quotes as standing rules and the 45 and 69
that RECORD9 reports as READINGS of R40's round, none of them a prediction and none of them
quoted by R-0536. The trailing half of the headline survives — all three predictions did read
one high — so the defect is the numeral alone. This is the R-0402 / R-0404 / R-0436
enumeration family arriving where checklist item 16 does not reach: item 16 binds a section
HEADING over a list, and a finding headline is a heading over a body by every property that
made item 16 necessary, being the half nobody re-reads and the half that drifted from the
body beneath it. The counter-measure is to widen item 16 from a heading to any sentence that
counts what follows it; that promotion is NOT in the checklist and is owed to a later round,
which is why this finding names it instead of asserting it. Found and registered by the
reviewer.

- R-0538 — Low, ONE SHA QUALIFIED THREE VALUES AND ONLY TWO WERE READ THERE. R-0536, applied
at commit dc34997a, closes "Measured at 0e2cdacd with `splitlines`: 706, 643 and 46."
Measured at 4c7bcb3a: `docs/agents/planner_reviewer_prompt.md` is 706 lines at 0e2cdacd and
643 at 93226220, and `.agent/plan.md` is 46 at 0e2cdacd — so the middle value is a reading at
a commit OTHER than the one its own sentence names, and at the named commit that file is 706
rather than 643. The intent is recoverable, because the three values map positionally onto
the three predictions the preceding sentence quotes and the second of those is itself
qualified "at 93226220", so nothing false about the repository follows. What earns it an id
is where it landed: this is the mis-scoped-qualifier shape R-0534 registered and R-0535
recorded recurring, arriving for the third consecutive round and this time INSIDE the
paragraph registering a different measurement-convention defect — the same self-application
failure R-0535 named, one round after naming it. R42's worker declared it under constraint 8
and correctly left it standing under constraint 9; the registration is the correction, per
checklist item 20. Found by the worker under constraint 8 and registered by the reviewer.
END-RECORD11

BEGIN-PLANF11
## Current Step
R42, this round: record the R41 PASS, register R-0535 and R-0536 — both defects in
RECORD9's own text — and rule DECISION F085 D4, the measured design for the `ci_run.py`
migration. Session-closing round: no production code changes, and R43 applies D4 in code.
END-PLANF11

BEGIN-PLANT11
## Current Step
R43, this round: record the R42 PASS and register R-0537 and R-0538, both defects in
R-0536's own text. A RECORD round by measurement, not by choice: the `ci_run.py` migration
is authored, dry-run and red-controlled, but its block measured 487 lines against the
400-line cap of DECISION F105 D5, so R44 applies it.
END-PLANT11

BEGIN-PLANF12
   design is ruled in DECISION F085 D4: capture and re-emit the stage output, set the
   guard's wall ABOVE the child's own budget as a backstop, and carry that budget through
   `extra_env`. R43 applies it. One or two per order, never as one group.
END-PLANF12

BEGIN-PLANT12
   design is ruled in DECISION F085 D4: capture and re-emit the stage output, set the
   guard's wall ABOVE the child's own budget as a backstop, and carry that budget through
   `extra_env`. R44 applies it, then `builder_bridge.py` as the last site of this
   sub-slice. One or two per order, never as one group.
END-PLANT12
