── STEP T002b record — F085 — R37 ────────────────────────────────────────────

Goal: record the R36 PASS, register R-0527, and resolve both R-0526 and R-0527 with
one checklist clause — that a claim a block or a slice makes about its OWN text is
measured before emission and stated as the property measured.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 extend
checklist item 11 · C2 record R36 and register and resolve R-0526 and R-0527 · C3 plan
· C4 handback.

## Why this round exists — read before C1

R36 PASSED, and it was the first production round in four. The reviewer re-ran G1-G8
over 23b5fcd9..483975b3 and every one reproduces the handback's reading; RECORD5
carries the numbers and this section does not repeat them.

R36's worker did the thing constraint 8 exists to produce: it measured the reviewer's
own constraint against the slice that constraint described, found the constraint false,
declared it in the handback, and changed nothing. That declaration is R-0527 below.

TWO FINDINGS, ONE SHAPE. R-0526 is a slice asserting a universal about its own
references — "every reference it makes to `.agent/handoff.md` names the SHA that holds
the text it means" — which is false of three of its own four. R-0527 is a block
CONSTRAINT asserting a property of its own slice — "RECORD4 states facts about
`packages/orchestration/mission_state.py` and `tests/orchestration/test_mission_state.py`"
— when at 483975b3 RECORD4 contains zero occurrences of either path, which made the
staleness obligation that constraint carried vacuous rather than met. Different
sentences, same defect: a claim about the author's OWN text, written from recollection
instead of measurement, in a document whose whole purpose is that its claims are
measured. Item 11 already forbids the NUMERAL form of this; neither the universal
quantifier nor the bare property assertion is reached by it. C1 extends item 11 to the
class rather than to the two instances — the R-0417 staleness shape, where a fix that
reaches only the noticed instance leaves the class open.

Nothing here reaches a claim about another file, a gate result or a prior commit: items
19 and 20 already govern those. This clause binds only what the author says about text
the author is writing.

## Change

C1 — `docs/agents/planner_reviewer_prompt.md`, one commit, the I11F→I11T pair, which
extends checklist item 11 in place. No item is added, removed or renumbered.

C2 — `.agent/live_review.md`, one commit, RECORD5 appended and nothing else. RECORD5
carries the R36 gate entry, then the R-0527 registration, then the resolutions of
R-0526 and R-0527, as one slice.

C3 — `.agent/plan.md`, one commit, the PLANF5→PLANT5 pair over the Current Step block
alone. Next Steps is untouched: the migration order did not change this round.

Change set, named rather than counted: `.agent/authored/f085-r37.md`,
`.agent/last_block.md`, `docs/agents/planner_reviewer_prompt.md`,
`.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`. Nothing else is
touched. This round changes no production code, so it orders no ruff run and no red
proof.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r37.md` by its marker pair. Never retype a slice, never apply
   one from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test and recorded as
   the test's OUTPUT, one reading per pair — the form checklist item 15 requires:
   I11F→I11T — TO contains FROM: true — APPEND.
   PLANF5→PLANT5 — TO contains FROM: false — REWRITE.
   For the APPEND pair the "FROM 0x after" count is unattainable by construction and is
   NOT ordered; §4.9's append obligation is ordered instead. Do not report a FROM-zero
   reading for it under any wording.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists, finish
   the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This round
   orders no destructive check, so it creates no worktree; `git worktree list` is one
   line throughout.
5. C2 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one blank
   line separates it from RECORD5. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round registers R-0527 and
   resolves R-0526 and R-0527, so the open count moves from 119 to 118.
7. If any gate comes out red, or a FROM does not match at exactly one place in the file
   it is applied to, STOP: write the handback naming the exact command, its exit code
   and its output, and do not improvise a repair.
8. STALENESS, standing: after C3 re-read every edited file and confirm that no sentence
   this round put on disk was falsified by a later commit of the same round, and that no
   slice quotes another file's current wording as a claim. Name what was re-read. The
   only file this block both edits and makes claims about is
   `docs/agents/planner_reviewer_prompt.md`: RECORD5 says item 11 now carries the
   clause, and constraint 9 is what makes that true when the sentence is written. Every
   other reading RECORD5 asserts about a state before this round names 483975b3 or an
   earlier SHA. This constraint states no property of any slice's contents — R-0527 is
   what happens when it does.
9. The commit order C1 before C2 is load-bearing: it is what makes RECORD5's claim about
   the extended item 11 true when it is written, and what licenses RECORD5 to use the
   item-20 carve-out for that sentence. Do not reorder.
10. Do not "repair" any landed text. R-0526's sentence stays in commit cde59e8c and
    R-0527's constraint stays in commit 8a0766c1 where they landed; the correction is
    RECORD5's registration and the C1 clause, never an edit to what is already on disk —
    the R-0521 principle.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r37.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report the sha256, the
byte count, the line count, the number of marker lines, and region digests over the line
ranges 1-100, 101-200 and 201-end, each digest taken over those lines with their
trailing newlines included. Do not compute any of those numbers by hand; measure them.

G3 APPEND SHAPE for C2. The pre-commit blob of `.agent/live_review.md` is a byte-exact
PREFIX of the post-commit file; the remainder is exactly one blank line plus RECORD5;
RECORD5 is an exact suffix of the post-commit file; RECORD5's first line occurs once
among the lines that commit's diff ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land
in the file — count marker LINES, never the substring, because the quoted regex already
appears in that file's prose. Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md`
at base 483975b3 and at HEAD, taking registered from `^- R-\d{4} — `, done from
`^Done: R-\d{4} — ` and landed from `^Landed: R-\d{4}`. The reviewer's base reading is
141 registered / 22 done / 0 landed, 119 open, max registered R-0526 and max resolved
R-0525; at HEAD it must be 142 / 24 / 0 with 118 open, max registered R-0527 and max
resolved R-0527. Report the registered symmetric difference (exactly R-0527), the done
symmetric difference (exactly R-0526 and R-0527), the landed symmetric difference
(empty), the count of duplicate ids, the count of resolutions naming an unregistered id,
the maximum id, and the next free id, which moves from R-0527 to R-0528.

G5 THE CLAUSE LANDED, measured at HEAD after C1, and the APPEND obligation. In
`docs/agents/planner_reviewer_prompt.md`:
- the I11F text still occurs exactly once, because the pair is APPEND-shaped and its
  FROM survives by construction;
- the item-11 opener
  `  11. **A convention paragraph names its units and states NO count of them.**`
  and the item-12 opener
  `  12. **A dry run executes the gate's EXACT command line.** Finding R-0463. When`
  and the closing paragraph opener
  `  Why this is on disk and not a habit: item 2 has recurred six times across`
  each still occur exactly once, because this commit extends one item rather than
  adding, removing or renumbering any;
- every line I11T adds that I11F does not contain occurs exactly once AMONG THE LINES
  C1'S DIFF ADDS — that is the §4.9 append obligation, ordered INSTEAD of a FROM-zero
  count;
- 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` reached the file.
Report `git show --numstat` for C1, and for PLANF5→PLANT5 in `.agent/plan.md` after C3
the rewrite reading: FROM 0x, TO 1x.

G6 STATE READERS AND DOCS, each run in the PRIMARY checkout and never in a worktree
(R-0518):
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading `159 passed`.
  A red naming `TestVitestFrontendTestFoundation::test_vitest_passes` with
  `apps/ui/node_modules` absent IS finding R-0518 rather than a regression, and means
  the command was run in a worktree; re-run it in the primary checkout. Any other red is
  a STOP under constraint 7.
- Because a file under `docs/` changes: `python3 -m pytest tests/docs/ -q` exits 0, base
  reading `295 passed`. Do NOT read that green as evidence about C1. The reviewer ran
  the red control in a disposable worktree at 7480d880 with
  `docs/agents/planner_reviewer_prompt.md` replaced by the single line `# broken` and
  the suite still returned `295 passed`, so no test under `tests/docs/` reads that file
  and G5 is the only check on C1's content.
- CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
  `42 passed`.

G7 COMMIT HYGIENE. `git diff --name-only 483975b3..HEAD` measured BEFORE C4 holds
exactly the paths named in the change set above, minus `.agent/handoff.md` which C4
writes, and nothing else. Report per-commit insertions for every commit BEFORE C4 — C4
cannot measure itself, so report its own insertions in the round report instead — and
confirm none exceeds 500. Confirm every commit has exactly one parent and that
`git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
branch, base SHA 483975b3, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2, C3 and C4, the real verification results for G1-G7 with exit
codes, the open-findings count, and the next expected action. In the
`## Authored-text proofs` section report each pair under the shape constraint 2 assigns
it, and NEVER report a FROM-zero count for an APPEND pair. Repeat this Fortschritt line
verbatim:
Fortschritt: ~73 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R36
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, 2 offen · T002c-d, T003
offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The handback MUST state, in its `## Next` section, that the next session's FIRST action
is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate
(`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). It MUST also
state that R37's own verdict is NOT a §4.13 terminator because this branch continues,
and that the next reviewed round records R37's gate entry in `.agent/live_review.md`.

The `## Next` section MUST additionally carry this note verbatim, because the reviewer
measured it at 483975b3 and it would otherwise be re-derived wrongly:

  The next migration site is `packages/orchestration/ci_run.py`. At 483975b3 its only
  spawn is line 79, `subprocess.run(command, check=False, cwd=cwd, env=env).returncode`
  — no capture, no timeout, output streaming straight to the console. Moving it onto
  `run_guarded_test_command` therefore CHANGES observable behaviour rather than
  preserving it: the seam captures, so a console-streaming CI run would go silent unless
  the migration also decides where that output goes. That decision is the round's own
  work and is recorded as a DECISION in `.agent/decisions.md`, not taken in passing. It
  also passes `env=`, which the seam does not accept: the seam allowlists keys the
  parent already has and cannot SET a value, so that round must establish what happens
  to the caller's `env` before it changes any line.
  `builder_bridge.py` comes LAST and stays BLOCKED for the same allowlist reason.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-I11F
      (R-0461). This item is that promotion, finally performed.
END-I11F

BEGIN-I11T
      (R-0461). This item is that promotion, finally performed.
      Findings R-0526 and R-0527 widen this item from the NUMERAL to the class it
      belongs to: any claim a block or a slice makes about its OWN text is MEASURED
      before emission and written as the property that was measured. Two forms have now
      cost rounds. A slice may not assert a universal over its own contents — R-0526 was
      a resolution closing with "every reference it makes to `.agent/handoff.md` names
      the SHA that holds the text it means", which was false of three of its own four,
      because the clause it restated binds only references that LOCATE landed text and
      the sentence quantified over all of them. A block constraint may not assert a
      property its own slice does not have — R-0527 was constraint 8 of the R36 block
      declaring that RECORD4 stated facts about two named source files when RECORD4
      contained neither path, which made the staleness obligation that constraint
      carried vacuous rather than met, and only the worker's own measurement caught it.
      Both are recollections in the one document that exists because recollections are
      not evidence. State what was counted, or state nothing: "the sentences that locate
      landed text name their SHA" is measurable, "every reference names its SHA" is a
      universal nobody checked. Items 19 and 20 govern claims about a GATE's result and
      about another FILE's content; this one governs a claim about the author's own
      bytes, which neither reaches because the text in question has not landed anywhere
      yet when the claim is written.
END-I11T

BEGIN-RECORD5
Gate: R37 — the R36 entry. R36 PASSED, and it was the first production round since R32:
the default `runner` closure of `packages/orchestration/mission_state.py` moved onto
`run_guarded_test_command`, with the first test that reaches that closure at all. Every
ordered gate was re-run by the reviewer over 23b5fcd9..483975b3 and each reproduces the
handback's reading. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL, not only
against a digest: the scratch file the block was authored into, the committed
`.agent/authored/f085-r36.md`, the committed `.agent/last_block.md` and both working
copies are all five byte-EQUAL at sha256
208ad9d39755891b5bb83f9382e6f3d613c97cafc4652ad2b8b662887d3ce8d1, 24223 B, 400 lines, 22
marker lines, region digests 7d583ed0, ace9d813 and 9b5a9653 — and that digest is the
one the reviewer measured BEFORE emission, so the block the worker applied is the block
the reviewer wrote. THE APPEND COMMIT HELD ITS SHAPE: e27c1c61's pre-commit blob 387274 B
is a byte-exact PREFIX of the 391135 B post-commit file, the remainder 3861 B is one
blank line plus RECORD4, RECORD4 is an exact suffix, its first line occurs once among the
47 lines that commit adds, numstat 47/0, 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the
BEGIN substring occurs 13 times. THE ARITHMETIC MOVED IN THE REGISTERED SET ALONE: 140
registered / 22 done / 0 landed at 23b5fcd9 against 141 / 22 / 0 at 483975b3, 118 open
against 119, registered symmetric difference exactly R-0526, done and landed symmetric
differences empty, no duplicate id, no resolution naming an unregistered id, and next
free R-0527. THE MIGRATION IS THE SLICES AND NOTHING ELSE: at 483975b3 the import sits at
MODULE level in isort order, the three APPEND FROMs each still occur once, the REWRITE
pair reads FROM 0x and TO 1x, the 34 lines C2 adds are exactly the 24 TO-only lines of the
four pairs plus the ten unchanged context lines the diff carries, 0 marker lines reached
either file, and the string `subprocess` now occurs 0 times in that module. THE SEAM IS
REACHED BY A TEST FOR THE FIRST TIME: at 23b5fcd9 every test exercising `run_verify_task`
passed its own `runner=`, so the default closure was executed by no test, and
`test_the_default_runner_goes_through_the_guarded_seam` closes that gap in the same commit
as the code. THE RED PROOF WAS RE-RUN BY THE REVIEWER, NOT READ: in a disposable worktree
at 83bc6df1 with the module-level import moved into the closure, `1 failed, 81 passed`
and the failure is `AttributeError` naming `run_guarded_test_command` at the
`monkeypatch.setattr` line — the module-level import is load-bearing, and a closure-local
one would have left the site untestable while every other gate stayed green. The worktree
was removed and pruned and the primary checkout is clean. THE SUITES WERE RE-RUN, NOT
READ: ruff `All checks passed!`, `test_mission_state.py` `82 passed`, the four state
readers `159 passed` and the canary `42 passed`, each as its exact ordered command line in
the primary checkout, each exit 0. COMMIT HYGIENE IS CLEAN: the path set is the six
declared paths, per-commit insertions are 400, 361, 47, 34, 8 and the handback's own 50,
none over 500, all six commits are single-parent, the reflog holds only `commit:` entries,
and the ordered push landed — origin and local agree at 483975b3.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R36's worker measured the
reviewer's own constraint against the slice it described, found it false, declared it in
the handback, and changed nothing. That is the second consecutive round in which the
constraint-8 report produced the round's finding, and it is why the reviewer's text is
gated by the worker's measurement rather than by the reviewer's own re-reading.

- R-0527 — Low, A BLOCK CONSTRAINT ASSERTED A PROPERTY ITS OWN SLICE DOES NOT HAVE.
Constraint 8 of the R36 block, applied at commit 8a0766c1, states that RECORD4 "states
facts about `packages/orchestration/mission_state.py` and
`tests/orchestration/test_mission_state.py`, both of which C2 of this same round edits",
and then binds every such sentence to name the SHA 23b5fcd9. Measured at 483975b3,
RECORD4 contains zero occurrences of either path: its file-state readings all belong to
the R35 range and name 6ca30b16, 23b5fcd9, cde59e8c or 2342ed97. The obligation was
therefore VACUOUS rather than met — a staleness gate that could not fail, which is the
R-0438 class arriving through a constraint instead of a path. Nothing false about the
repository landed on disk, and the worker performed the re-read anyway across all six
edited files, which is why this is Low. What makes it worth an id is where the false
sentence lives: constraint text is committed verbatim to `.agent/authored/f085-r36.md`
and `.agent/last_block.md`, so a reviewer recollection about the reviewer's own slice is
now part of the permanent record, and the only reason it was caught is that a worker
measured a claim its author had not. Found by the worker under constraint 8 and
registered by the reviewer, which is where a constraint-8 report is supposed to land.

Done: R-0526 — Resolved at R37. Checklist item 11 of
`docs/agents/planner_reviewer_prompt.md` §3 now binds any claim a block or a slice makes
about its OWN text to be measured before emission and written as the property measured,
and it names the universal-quantifier form explicitly: a slice may not assert a universal
over its own contents, because "every reference names its SHA" is a claim nobody counted
while "the sentences that locate landed text name their SHA" is one that can be. Applied
by the commit that constraint 9 of this round's block fixes ahead of this one. The
sentence R-0526 registered stays where it landed; nothing in `.agent/live_review.md` was
rewritten.

Done: R-0527 — Resolved at R37 by the same clause, which is why the two share one. Item
11 now also forbids a block constraint from asserting a property its own slice does not
have, and the counter-measure is stated as a method rather than as a prohibition: state
what was counted, or state nothing. The block that carries this resolution applies it to
itself — its constraint 8 names the one file this block both edits and makes claims
about, and asserts no property of any slice's contents. Applied by the commit that
constraint 9 of this round's block fixes ahead of this one.
END-RECORD5

BEGIN-PLANF5
## Current Step
R36, this round: record the R35 PASS and register R-0526, then migrate the default
`runner` closure of `mission_state.py` onto `run_guarded_test_command` together with
the first test that reaches that closure at all.
END-PLANF5

BEGIN-PLANT5
## Current Step
R37, this round: record the R36 PASS, register R-0527, and resolve R-0526 and R-0527
with one checklist clause — a claim a block or a slice makes about its own text is
measured before emission. No production code changes.
END-PLANT5
