── STEP T002b interlude — F085 — R33 ─────────────────────────────────────────

Goal: record the R32 PASS, and register AND resolve R-0521 — the defect R32's own
resolving slice committed against the rule it was resolving — by sharpening
pre-emission checklist item 20 so the commit a slice names must be one that
already exists rather than a label that re-resolves.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 sharpen
checklist item 20 · C2 record R32 and register and resolve R-0521 · C3 plan ·
C4 handback.

## Why this round exists — read before C1

R32 passed. The reviewer re-ran every gate it ordered over 16234fbf..HEAD and each
reproduces the handback's reading, including the red proof, which the reviewer
re-broke independently in its own disposable worktree.

R32's worker declared, under constraint 8 and correctly, that a sentence its own
C2 committed was falsified by its own C3. The R31 gate entry says
`builder_bridge.py`, `ci_run.py`, `integrity_gate.py` and `mission_state.py` each
show 0 references to `run_guarded_test_command` "at HEAD". That reading was taken
at 16234fbf and is true there; C3 of the same round put `integrity_gate.py` on the
seam, so one of those four names is wrong for every commit from ed88be4c onward.

That is the exact class checklist item 20 was promoted to prevent, committed by
the slice that promoted it, one commit after it landed. Item 20 as written asks a
slice to name "the commit the reading was taken at", and the sentence did name a
commit — it named `HEAD`, which is a label that re-resolves as the round proceeds
and therefore names a different commit by the time the round ends. The rule was
followed to the letter and defeated anyway, so the counter-measure is a narrowing
of the rule and not a new one: the commit named must be an ABSOLUTE identifier
that already exists when the slice is written. A block always has one to hand —
its own base SHA, which the reviewer states in every done-when.

This round changes no production code, so it orders no red proof and no ruff run.

## Change

C1 — `docs/agents/planner_reviewer_prompt.md`, one commit, the SHARPF→SHARPT
pair, which narrows item 20 in place.

C2 — `.agent/live_review.md`, one commit, RECORD1 appended and nothing else.
RECORD1 carries the R32 gate entry, then the R-0521 registration, then its
resolution, as one slice.

C3 — `.agent/plan.md`, one commit, the PLANF→PLANT pair. It spans the Current Step
and list item 1, the only lines that change; items 2 and 3 keep their labels
untouched because the list's arity does not change.

Change set, named rather than counted: `docs/agents/planner_reviewer_prompt.md`,
`.agent/authored/f085-r33.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md` and `.agent/handoff.md`. Nothing else is touched.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r33.md` by its marker pair. Never retype a
   slice, never apply one from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test, one reading
   per pair: SHARPF→SHARPT REWRITE · PLANF→PLANT REWRITE.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists,
   finish the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This
   round orders no destructive check, so it creates no worktree; `git worktree
   list` is one line throughout.
5. C2 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD1. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round both registers
   and resolves R-0521 and touches no other id, so the open count must come out
   unchanged.
7. If any gate comes out red, or a FROM does not match at exactly one place in the
   file it is applied to, STOP: write the handback naming the exact command, its
   exit code and its output, and do not improvise a repair.
8. STALENESS, standing: after C3 re-read every edited file and confirm that no
   sentence this round put on disk was falsified by a later commit of the same
   round, and that no slice quotes another file's current wording as a claim. Name
   what was re-read. RECORD1 states facts about `.agent/live_review.md` and about
   `docs/agents/planner_reviewer_prompt.md`, both of which this block edits, and
   every reading it ASSERTS names a SHA rather than a relative label. `HEAD` does
   appear in RECORD1, always QUOTING or naming the defect R-0521 registers rather
   than asserting a reading of its own — that is the finding's subject, not an
   instance of it. Check that distinction holds; do not "repair" the quotations.
9. The commit order C1 before C2 is load-bearing: it is what makes RECORD1's claim
   about the sharpened item 20 true when it is written. Do not reorder.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r33.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report the sha256,
the byte count, the line count, the number of marker lines, and region digests over
the line ranges 1-100, 101-200 and 201-end. Do not compute any of those numbers by
hand; measure them.

G3 APPEND SHAPE for C2. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank line
plus RECORD1; RECORD1's first line occurs once among the lines that commit's diff
ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker
LINES, never the substring, because the quoted regex already appears in that file's
prose and a substring count reports it. Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in
`.agent/live_review.md` at base c2033d6c and at HEAD, taking registered from
`^- R-\d{4} — `, done from `^Done: R-\d{4} — ` and landed from `^Landed: R-\d{4}`.
The reviewer's base reading is 135 registered / 17 done / 0 landed, 118 open, max
registered R-0520 and max resolved R-0520; at HEAD it must be 136 / 18 / 0 with 118
open again and both maxima R-0521. Report the registered symmetric difference and
the done symmetric difference (each must hold exactly R-0521), the landed symmetric
difference (empty), the count of duplicate ids, the count of resolutions naming an
unregistered id, the maximum id, and the next free id, which moves from R-0521 to
R-0522.

G5 THE CHECKLIST NARROWING LANDED, measured at HEAD after C1. In
`docs/agents/planner_reviewer_prompt.md` the line
`      identifier that already EXISTS when the slice is written — a SHA, never a label`
occurs exactly once; the closing paragraph opener
`  Why this is on disk and not a habit: item 2 has recurred six times across`
still occurs exactly once; the item-20 opener
`  20. **A slice states a fact about a file the same block edits only with the commit`
still occurs exactly once, because this pair narrows item 20 rather than adding an
item; and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` reached the file. Report
`git show --numstat` for C1.

G6 STATE READERS AND DOCS. This round changes no production code, so it orders no
ruff run and no red proof. Because it rewrites `.agent/` state:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading
`159 passed`. RUN IT IN THE PRIMARY CHECKOUT AND NEVER IN A WORKTREE: R-0518
records why, and a red naming `TestVitestFrontendTestFoundation::test_vitest_passes`
with `apps/ui/node_modules` absent IS that finding rather than a regression. Any
other red is a STOP under constraint 7. Because a file under `docs/` changes:
`python3 -m pytest tests/docs/ -q` exits 0, base reading `295 passed`. CANARY:
`python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
`42 passed`.

G7 COMMIT HYGIENE. `git diff --name-only c2033d6c..HEAD` measured BEFORE C4 holds
exactly the paths named in the change set above, minus `.agent/handoff.md` which C4
writes, and nothing else. Report per-commit insertions for every commit BEFORE C4 —
C4 cannot measure itself, so report its own insertions in the round report instead
— and confirm none exceeds 500. Confirm every commit has exactly one parent and
that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
branch, base SHA c2033d6c, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2, C3 and C4, the real verification results for G1-G7 with
exit codes, the open-findings count, and the next expected action. Repeat this
Fortschritt line verbatim:
Fortschritt: ~70 % (T001 gebaut · R13-R32 PASS · T002a KOMPLETT · T002b 9 von 12
Sites auf dem Seam, 3 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The handback MUST state, in its `## Next` section, that the next session's first
action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open
PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
It MUST also state that R33's own verdict is NOT a §4.13 terminator because this
branch continues, that the next reviewed round records R33's gate entry in
`.agent/live_review.md`, and that the next MIGRATION round takes
`mission_state.py`'s spawn, because `builder_bridge.py` cannot move until the seam
can SET an environment value rather than only allowlist a key.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-SHARPF
      counter-measure is the commit name, never a rewrite: appending a correction is
      how this record stays honest, and overwriting landed text is worse than a dated
      wrong sentence.
END-SHARPF

BEGIN-SHARPT
      counter-measure is the commit name, never a rewrite: appending a correction is
      how this record stays honest, and overwriting landed text is worse than a dated
      wrong sentence. Finding R-0521 narrows what counts as naming the commit: it must
      be an absolute
      identifier that already EXISTS when the slice is written — a SHA, never a label
      like `HEAD` or `main` that re-resolves as the round proceeds and therefore names
      a different commit by the time the round ends. A block always has such a SHA to
      hand, because its own base is stated in its done-when. R-0521 is this rule
      failing while being obeyed: the slice that RESOLVED R-0520 wrote "at HEAD",
      satisfied item 20 as it was then worded, and was falsified one commit later by
      its own round.
END-SHARPT

BEGIN-RECORD1
Gate: R33 — the R32 entry. R32 PASSED: the round that promoted the slice-fact rule
into pre-emission checklist item 20, resolved R-0520 and moved
`integrity_gate._check_collect_only` onto the shared `test`-class seam. Every ordered
gate was re-run by the reviewer over 16234fbf..c2033d6c and each reproduces the
handback's reading. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL, not
only against a digest: the scratch file the block was authored into, the committed
`.agent/authored/f085-r32.md`, the committed `.agent/last_block.md` and both working
copies are all five byte-EQUAL at sha256
75deb8c5d666fc2f4053583eb8c4a3d94dd2db8f52c227df2a22b2392cf1e686, 23119 B, 400
lines, 24 marker lines, region digests eb26791d, 656230ba and 0d724fc0. THE APPEND
COMMIT HOLDS ITS SHAPE: C2's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1 at 4361 =
1 + 4360 bytes, numstat 55/0, RECORD1's first line occurs once among the 55 lines
that commit adds, 0 lines match `^(BEGIN|END)-[A-Z0-9]+$`, and the applied slice is
an exact suffix of the file. THE ARITHMETIC MOVED IN THE DONE SET ALONE: 135
registered / 17 done / 0 landed at c2033d6c against 135 / 16 / 0 at 16234fbf, 119
open falling to 118, registered and landed symmetric differences empty, done
symmetric difference exactly R-0520, no duplicate id, no resolution naming an
unregistered id, and next free R-0521 at both ends because the round registered
nothing. THE ORDERING THAT MADE THE RECORD TRUE WAS OBEYED: constraint 10 required
the checklist promotion to precede the resolution that cites it, and 94e70839 does
precede ce69c39a. THE PAIRS LANDED WHERE THEY WERE AIMED: at c2033d6c IGSPAWNF and
IGERRF each occur 0 times in `integrity_gate.py` while IGSPAWNT, IGERRT and IGIMPT
each occur once, the guard import occurs once among the lines C3 adds to that file,
`import subprocess` still occurs once because the `git ls-files` call in
`_check_relevant_untracked` is a different command class, the new test def occurs
once among the lines C3 adds to its test file, TESTIG is an exact suffix of that
file, and 0 marker lines reached any target. Item 20 occurs once and the checklist's
closing paragraph still occurs once. PLANF is gone and PLANT occurs once, in a
46-line plan under the 50-line cap. THE MIGRATION WAS PROVED TWICE, BY RUNNING IT
AND BY BREAKING IT: the round gate exits 0 at `16 passed` against the `15 passed`
the reviewer measured at 16234fbf, the migrated function run FOR REAL prints
`collect_only IntegrityStatus.PASS pytest collection passed` — identical to the
unmigrated reading at 16234fbf, which is the behaviour-equality evidence this
feature's Acceptance asks for, and it shows the guard's environment allowlist does
not starve a real collection — and in the reviewer's own disposable worktree at
c2033d6c, with the guarded call replaced by a bare `subprocess.run`, the run exits 1
with `1 failed, 15 passed` at node `test_collect_only_runs_on_the_guarded_seam`,
`AssertionError` at `test_integrity_gate.py:235`. THE GATES WERE RE-RUN, NOT READ:
ruff over the two changed files `All checks passed!`, the four state readers
`159 passed`, the docs suite `295 passed` and the canary `42 passed`, each as its
exact ordered command line in the primary checkout, each exit 0. COMMIT HYGIENE IS
CLEAN: the path set is the eight declared paths, per-commit insertions are 400, 288,
16, 55, 41, 12 and the handback's own 80, none over 500, all seven commits are
single-parent, and the reflog holds only `commit:` entries. The 128-line handback
declares its own overage against the 100-line cap and names the mandated content
that caused it. The worker deviated from nothing it was ordered to do, and the one
defect the round put on disk is the reviewer's, registered next.

- R-0521 — Low, A SLICE OBEYED CHECKLIST ITEM 20 AND WAS FALSIFIED ANYWAY, BECAUSE
THE COMMIT IT NAMED WAS A LABEL RATHER THAN A SHA. R32's RECORD1, applied at commit
ce69c39a, closes with a staleness sentence stating that `builder_bridge.py`,
`ci_run.py`, `integrity_gate.py` and `mission_state.py` each show 0 references to
`run_guarded_test_command` "at HEAD". That reading was taken at 16234fbf and is true
there. C3 of the SAME round, commit ed88be4c, put `integrity_gate.py` on the seam,
and at c2033d6c that file references the symbol twice — so one of the four names in
that sentence is wrong for every commit from ed88be4c onward, in a file that is the
permanent record. This is the R-0520 class recurring in the very slice that resolved
R-0520, one commit after the counter-measure landed. The defect is the reviewer's,
not the worker's: R32's handback found it under constraint 8 and reported it instead
of editing a slice it was forbidden to alter, which is exactly the behaviour
constraint 8 exists to produce. Low because nothing executable depends on the
sentence and no gate can go red over it. What makes it worth an id rather than a
correction is that item 20 was FOLLOWED: the sentence did name a commit, and the
commit it named was `HEAD`, which re-resolves as the round proceeds and so denotes a
different commit at the end of the round than at the start. A rule that can be
obeyed and defeated at once is under-specified rather than ignored, which is why the
counter-measure narrows item 20 instead of adding an item. Rewriting the landed
sentence is NOT proposed: appending a correction is how this record stays honest,
and this paragraph is that correction.

Done: R-0521 — Resolved at R33. Checklist item 20 of
`docs/agents/planner_reviewer_prompt.md` §3 now requires that the commit a slice
names be an absolute identifier that already exists when the slice is written — a
SHA, never a label like `HEAD` or `main` — applied by the commit that precedes this
one in this round. The narrowing is the whole resolution; the R31 gate entry's "at
HEAD" sentence stays on disk, wrong for one of its four names from ed88be4c onward,
because overwriting landed text is worse than a dated wrong sentence.
END-RECORD1

BEGIN-PLANF
## Current Step
R32, this round: record the R31 PASS, resolve R-0520 by promoting its
counter-measure into the pre-emission checklist, and move
`integrity_gate._check_collect_only` onto `run_guarded_test_command` — the
`test`-class site that pins no cwd and keeps `cwd=None` deliberately.

## Next Steps
1. T002b remainder — the three `test`-class sites still on a bare spawn, each
   differing from the shapes already migrated: `builder_bridge.py` SETS
   `PYTHONDONTWRITEBYTECODE` on a full `os.environ` copy, which the seam cannot
   express today because `run_guarded_test_command` allowlists keys rather than
   setting values — that site needs the seam widened before it can move;
   `ci_run.py` streams to the console instead of capturing and passes no timeout;
   and `mission_state.py` spawns inside a default `runner` closure. One or two per
   order, never as one group.
END-PLANF

BEGIN-PLANT
## Current Step
R33, this round: record the R32 PASS, and register and resolve R-0521 by narrowing
pre-emission checklist item 20 so the commit a slice names must be a SHA that
already exists rather than a label that re-resolves. No production code changes.

## Next Steps
1. T002b remainder — the three `test`-class sites still on a bare spawn, in this
   order. `mission_state.py` next: it spawns inside a default `runner` closure and
   is otherwise the capture-and-timeout shape already migrated three times. Then
   `ci_run.py`, which streams to the console instead of capturing and passes no
   timeout, so moving it onto a capturing seam is a behaviour decision and not a
   mechanical swap. `builder_bridge.py` comes LAST and is BLOCKED until the seam
   can SET an environment value: it puts `PYTHONDONTWRITEBYTECODE` on a full
   `os.environ` copy, while `run_guarded_test_command` only allowlists keys that
   the parent already has, so migrating it as-is would silently stop that variable
   reaching the child. One or two per order, never as one group.
END-PLANT
