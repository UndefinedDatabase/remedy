── STEP T002b protocol repair — F085 — R41 ───────────────────────────────────

Goal: record the R40 PASS, register R-0533 and R-0534 — two clauses of the reviewer's own
RECORD8 that R40's worker measured as false — and resolve R-0530, R-0531 and R-0532 by
writing their counter-measures into `docs/agents/planner_reviewer_prompt.md`. No
production code changes.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R40,
register R-0533 and R-0534, resolve R-0530, R-0531 and R-0532 · C2 the §4.9 code-append
rule · C3 checklist item 20's narrowing plus items 21 and 22 · C4 the plan · C5 handback.

## Change

C1 appends RECORD9 to `.agent/live_review.md` and nothing else. C2 applies the P49 pair to
`docs/agents/planner_reviewer_prompt.md`. C3 applies the CL20 pair to that same file, after
C2 has landed. C4 applies the plan pair over the Current Step block alone; Next Steps and
Risks are untouched.

Change set, named rather than counted: `.agent/authored/f085-r41.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`,
`.agent/plan.md` and `.agent/handoff.md`. Nothing else. No production file changes and no
`.py` file changes, so this round orders no ruff run and no red proof.

`docs/roadmap/**` is NOT in that set, so the §3 docs-round tier does not trigger and
`tests/docs/` is not ordered. Stated so no later reader reads its absence as an omission:
the reviewer grepped the suite for readers of the edited path and the only match is a
`@pytest.mark.skip` reason string in `tests/test_agent_tooling.py`, which reads a deleted
file and asserts nothing about this one. NO test in this repository asserts the content of
`docs/agents/planner_reviewer_prompt.md`. That is why G5 is textual and structural rather
than a suite, and why the reviewer red-controlled it before ordering it.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r41.md` by its marker pair. Never retype one, never apply one from
   the prompt. Marker lines never reach a target file.
2. Pair shapes, MEASURED by the reviewer with a containment test and recorded here as that
   test's OUTPUT, one reading per pair:
   - P49FROM→P49TO reads `TO contains FROM: true` — an APPEND. It is therefore owed the
     §4.9 append obligation and NOT a FROM-zero count: after C2, P49FROM still occurs
     exactly 1x, because it survives inside P49TO. Ordering "FROM 0x" here would be
     unattainable by construction (R-0522).
   - CL20FROM→CL20TO reads `TO contains FROM: true` — an APPEND, same obligation, and
     CL20FROM still occurs exactly 1x after C3 for the same reason.
   - PLANF9→PLANT9 reads `TO contains FROM: false` — a REWRITE, owed the FROM 0x / TO 1x
     reading.
   Each FROM was measured to occur exactly 1x in its target at 93226220.
3. Re-read `.agent/STOP` from disk before C0a and again before C5. If it exists, finish the
   commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This round
   orders no destructive check, so it creates no worktree; `git worktree list` is one line
   throughout.
5. C1 is an APPEND: the pre-commit file stays a byte-exact prefix, exactly one blank line
   joins it to RECORD9, and RECORD9 is not reflowed, re-wrapped or re-indented.
6. ORDERING, load-bearing. RECORD9 contains three `Done:` paragraphs, each stating that a
   counter-measure now stands in `docs/agents/planner_reviewer_prompt.md`. C1 lands BEFORE
   C2 and C3, so each of those sentences is false at the instant it is written and true
   from C3 onward. That is deliberate and is the R-0524 carve-out: a slice describing this
   round's OWN landed change cannot name a SHA that does not yet exist, so it names this
   constraint instead, and this constraint is what makes the claim checkable. The sequence
   C1 → C2 → C3 is therefore not reorderable, and C2 must precede C3 because CL20FROM is
   measured against the file as C2 leaves it.
7. If a gate comes out red, or any FROM does not match at exactly one place, STOP: write
   the handback naming the exact command, its exit code and its output, and do not
   improvise a repair.
8. STALENESS, standing: after C4 re-read every file this round edited and confirm no
   sentence this round put on disk was falsified by a later commit of the same round, and
   that no slice quotes another file's current wording as a claim. Name what was re-read
   and report the measurement, not a restatement of this sentence. Give special attention
   to any sentence quantifying over commits, files or lines — R-0530, R-0531, R-0532,
   R-0533 and R-0534 are all that shape, and the last two landed in the round that
   registered the first three.
9. Do not "repair" any landed text. The clauses R-0533 and R-0534 register stay in commit
   a5e240ca, and the gate sentences R-0531 and R-0532 register stay in eba5de68. The
   registration IS the correction — checklist item 20, and the R-0521 principle.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 3; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r41.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's own `.remedy-wt/f085-r41.md` — disk-to-disk, not a digest fallback. Report the
sha256, byte count, line count, marker-line count, and region digests over lines 1-120,
121-240 and 241-end, each taken with trailing newlines included and reported with its own
byte count so an empty region is visible as empty. Measure every one; compute none by hand.

G3 APPEND SHAPE for C1 on `.agent/live_review.md`: the pre-commit blob is a byte-exact
PREFIX of the post-commit file; the remainder is exactly one blank line plus RECORD9;
RECORD9 is an exact suffix; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
count marker LINES, never the substring, because that regex already appears in that file's
prose. RECORD9 is PROSE, so the §4.9 per-line obligation applies and is ordered: every line
RECORD9 contains occurs exactly once among the lines C1's diff adds, EXCEPT the empty line,
which is exempt because a paragraph break repeats by construction — report how many empty
lines the slice holds rather than counting them as failures. The reviewer measured RECORD9
to hold no duplicate non-empty line, so a violation here is a transport fault, not a
property of the text. Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at
base 93226220 and at HEAD, from the line-start patterns for a registration, a resolution
and a landed line. The reviewer's base reading is 147 / 24 / 0, 123 open, max registered
R-0532, max resolved R-0527. At HEAD it must be 149 / 27 / 0, 122 open, max registered
R-0534, max resolved R-0532. Report the registered symmetric difference (exactly R-0533 and
R-0534), the done symmetric difference (exactly R-0530, R-0531 and R-0532), the landed
symmetric difference (empty), the duplicate-id count, the count of resolutions naming an
unregistered id, and the next free id, which moves from R-0533 to R-0535.

G5 THE DOC EDITS, measured on `docs/agents/planner_reviewer_prompt.md` at HEAD after C3.
Both pairs are APPENDs per constraint 2, so no FROM-zero count is ordered:
- P49FROM occurs exactly 1x and P49TO exactly 1x; CL20FROM exactly 1x and CL20TO exactly
  1x. Each TO-ONLY addition — the lines the TO adds beyond its FROM — occurs exactly once
  among the lines its own commit's diff ADDS. The reviewer measured the TO-only sets to
  hold no duplicate line, so a violation is a transport fault.
- STRUCTURAL, and the reason this gate exists: extract the pre-emission checklist region,
  from the line containing the checklist heading up to the line beginning
  `  Why this is on disk and not a habit:`, take every checklist item label in that region
  IN ORDER — a line matching two spaces, digits, a dot, a space and two asterisks — and
  confirm the numbers are exactly 1..22 with no gap and no repeat. Scope the match to that
  region: an unscoped one also matches the §3 Verification-tiers list and reads `1,2,3,5`.
  Base reading at 93226220 is 1..20 contiguous. The reviewer red-controlled this gate in a
  disposable worktree: relabelling item 22 as a second 21 makes it fire, and deleting item
  21 makes it fire.
- 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` reached the file. The file is 707 lines at
  HEAD against 644 at 93226220; report the number rather than asserting it, and report
  `git show --numstat` for C2 and for C3 separately.

G6 THE PLAN at HEAD after C4: PLANF9 occurs 0x and PLANT9 1x; `.agent/plan.md` stays under
the 50-line AGENTS.md cap and still carries `## Goal` and `## Next Steps`; 0 lines matching
`^(BEGIN|END)-[A-Z0-9]+$` reached it. The reviewer's dry run put it at 47 lines. Report
`git show --numstat` for C4.

G7 SUITES, each run in the PRIMARY checkout and never in a worktree (R-0518), each as its
exact command line, each exit 0. Both base readings were taken by the reviewer at 93226220:
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read `.agent/`
  state live; base reading `159 passed`. A red naming
  `TestVitestFrontendTestFoundation::test_vitest_passes` with `apps/ui/node_modules` absent
  IS finding R-0518 and means the command ran in a worktree; re-run it in the primary
  checkout. Any other red is a STOP under constraint 7.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base reading `42 passed`.

G8 HYGIENE. `git diff --name-only 93226220..HEAD` measured BEFORE C5 holds exactly the
change set above minus `.agent/handoff.md`, which C5 writes, and nothing else. Report
per-commit insertions for every commit BEFORE C5 — C5 cannot measure itself, so its own
insertions go in the round report — and confirm none exceeds 500. Confirm every commit has
exactly one parent and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch,
base SHA 93226220, a per-commit changed-files table, the item-status table covering C0a,
C0b, C1, C2, C3, C4 and C5, the real G1-G8 results with exit codes, the open-findings count
and the next expected action. Repeat this Fortschritt line verbatim:
Fortschritt: ~77 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R40 PASS
· T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, die letzten 2 ab R42 migrierbar ·
T002c-d, T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

Keep it inside the 60-line cap, or name the DECISION D15 stated cause and the exact
mandated content behind it.

The `## Next` section MUST state that the next session's FIRST action is Phase 1 rule 1 —
re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open
--json number,headRefName,baseRefName,isDraft`); that R41's own verdict is NOT a §4.13
terminator because this branch continues; and that the next reviewed round records R41's
gate entry. It MUST also carry this note verbatim:

  R42 migrates `packages/orchestration/ci_run.py` onto the seam, passing the per-stage
  budget through the `extra_env` overlay that landed at dce66faa. It still owes its own
  DECISION on where the stage output goes: at 93226220 `_run_via_subprocess` streams
  straight to the console and returns only the returncode, while the seam CAPTURES both
  streams, so the migration changes observable behaviour rather than preserving it. That
  decision is the round's own work and belongs in `.agent/decisions.md` before any line
  changes. `packages/orchestration/builder_bridge.py` follows it; then T002c-d, then T003
  and the integration gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD9
Gate: R41 — the R40 entry. R40 PASSED. Every ordered gate was re-run by the reviewer over
d3a707f5..93226220 and each reproduces the handback's reading. TRANSPORT WAS PROVED AGAINST
THE REVIEWER'S OWN ORIGINAL: the scratch file the block was authored into, the committed
`.agent/authored/f085-r40.md` at fc5d957a, the committed `.agent/last_block.md` at 067fa3d2
and the working copies of those two paths as they stand at 93226220 are all five byte-EQUAL
at sha256 fad599b49902bd898feca72a990ba03061af4ba6598135570e7028ff797c41ed, 15082 B, 225
lines, 6 marker lines. THE APPEND HELD ITS SHAPE: a5e240ca's pre-commit blob of 406554 B is
a byte-exact PREFIX of the 412143 B post-commit file, the remainder of 5589 B is one blank
line plus RECORD8, and RECORD8 extracted by its marker pair from the committed authored
block hashes d6ce71700bafa738218c94e573b2470bfefc0532953f679234604721dc3b96af over 5588 B
and 69 lines, equal byte for byte to what that commit appended; numstat 70/0, and no marker
line reached the file. THE ARITHMETIC MOVED IN THE REGISTERED SET ALONE: 145 / 24 / 0 at
d3a707f5 against 147 / 24 / 0 at 93226220, 121 open against 123, registered symmetric
difference exactly R-0531 and R-0532, done and landed symmetric differences empty, no
duplicate id, no resolution naming an unregistered id, next free R-0533. THE PLAN PAIR
LANDED AS A REWRITE: PLANF8 0x and PLANT8 1x at 93226220, `.agent/plan.md` 45 lines under
the 50-line cap with `## Goal` and `## Next Steps` both present, no marker line, numstat
3/3. THE SUITES WERE RE-RUN, NOT READ, each in the primary checkout, each exit 0: the four
state readers `159 passed` against a base of 159, and the canary `42 passed` against 42.
HYGIENE IS CLEAN: per-commit insertions over that range are 225, 168, 70, 3 and the
handback commit's own 81, none over 500; every commit in the range is single-parent; `git
reflog -10` holds only `commit:` entries; and `git worktree list` is one line.

BOTH R40 FINDINGS REPRODUCE INDEPENDENTLY. R-0531's counts were re-measured over the 49
lines dce66faa adds to `tests/orchestration/test_exec_guard.py`: the empty line 12x,
`    )` 4x, the argument line 3x and `@pytest.mark.subprocess` 2x, and those four are the
only distinct lines occurring more than once there. R-0532's premise was re-measured at
93226220: `git ls-tree origin/main` returns nothing for either
`packages/orchestration/exec_guard.py` or `tests/orchestration/test_exec_guard.py`.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraints 8 and 9 R40's worker measured
two clauses of RECORD8 — the reviewer's own text, landed at a5e240ca — against the
repository, found both false, declared them, and repaired neither, which is exactly what
constraint 9 required. That is the sixth consecutive round in which the constraint-8 report
produced the round's findings. Both are registered below, and this registration IS the
correction: checklist item 20 holds that appending a correction is how this record stays
honest and that overwriting landed text is worse than a dated wrong sentence, so a5e240ca
keeps its bytes.

- R-0533 — Low, A PER-COMMIT INSERTION LIST REPORTED ONE COMMIT'S CHURN COLUMN. RECORD8's
hygiene clause, applied at commit a5e240ca, reads "per-commit insertions are 349, 295, 50,
66, 6 and the handback's own 147". Re-measured by walking cbcb5c23..d3a707f5, the six
commits insert 349, 295, 50, 66, 3 and 147: f31802f0 is 3 insertions and 3 deletions, so 6
is the insertions+deletions churn reading that AGENTS.md DECISION F104 D1 excludes from the
500-line cap. The clause's conclusion, none over 500, survives, so nothing false about this
repository's compliance landed; what landed is a wrong number in a permanent record. Its
provenance is what earns it an id: this is R-0530's class recurring inside the paragraph
that REGISTERED R-0530, one commit after that paragraph concluded "nothing new is owed to
the checklist ... what is owed is the habit of running that measurement over sentences
quantifying across COMMITS". A counter-measure written as finding prose binds nothing, and
the round that wrote this one is the proof. Found by the worker under constraint 8 and
registered by the reviewer.

- R-0534 — Low, A PRESENT-TENSE CLAIM ABOUT A WORKING COPY WAS FALSIFIED BY ITS OWN ROUND'S
EARLIER COMMIT. RECORD8's transport clause, applied at commit a5e240ca, states that the R39
scratch file, `.agent/authored/f085-r39.md`, `.agent/last_block.md` "at 757be21c" and "both
working copies" are "all five byte-EQUAL" at sha256 32415af6…1181a. Measured:
`.agent/last_block.md` does hash 32415af6 at 757be21c as the clause says, but 067fa3d2 —
C0b of the very round that wrote the sentence, two commits before it landed — overwrote
that path with the R40 block, so at a5e240ca both the working and the committed
`.agent/last_block.md` hash fad599b4…c41ed. Four of the five copies matched when the
sentence landed and the fifth did not. The same clause's closing "origin and local agree at
d3a707f5" was false for the same structural reason: that block ordered its single push
AFTER the handback commit, so while RECORD8 was landing local HEAD was a5e240ca and origin
was still d3a707f5. This is R-0520's shape with a twist that let it through: the qualifier
was attached to the COMMITTED reading and omitted from the WORKING reading standing beside
it in the same sentence, so item 20 read as satisfied because a SHA was present — just not
for the half that needed one. Found by the worker under constraint 8 and registered by the
reviewer.

Done: R-0530 — Resolved at R41. Item 22 of `docs/agents/planner_reviewer_prompt.md` §3 now
binds any clause that states a value per commit, a value holding at "every commit after"
one, or a total over a range to be recomputed at emission by walking that range with `git
rev-list --reverse`, one reading per commit, and written as the list that walk produced.
R-0530 concluded that nothing was owed to the checklist and that the counter-measure was a
habit; R-0533 is that habit failing one commit later inside R-0530's own paragraph, which
is the evidence that overturns the conclusion. The commit carrying item 22 is fixed by
constraint 6 of the R41 block to land after the commit carrying this paragraph. The
sentence R-0530 registered stays where it landed at 3b915e3c; nothing was rewritten.

Done: R-0531 — Resolved at R41 by the same block. §4.9 of
`docs/agents/planner_reviewer_prompt.md` now states that its per-line count is written for
PROSE and binds prose only, that a slice of CODE repeats lines structurally so the count is
unattainable by construction for every code append, and that the obligation there is
ORDERED EQUALITY instead — pre-commit blob a byte-exact prefix, slice an exact suffix, and
the lines the commit's diff adds exactly the slice's lines IN ORDER. That is the property
R39's worker substituted and measured, promoted from one round's improvisation to the rule,
and it is strictly stronger than the count it replaces because it fixes position as well as
multiplicity. The commit carrying that text is fixed by constraint 6 to land after this
one. The gate sentence R-0531 registers stays in commit eba5de68.

Done: R-0532 — Resolved at R41 by the same block. Item 21 now binds a gate ordered at any
commit other than the one under review to be checked at emission with `git ls-tree <base>
-- <path>` for EVERY path it names, because a path this branch added does not exist at that
base and the tool then exits on the missing file and produces no reading at all — the
vacuous-gate shape of R-0438, reached through the base rather than through a typo. The same
item carries the carve-out the R39 instance also needed: an R-0518 primary-checkout clause
reaches SUITE commands, which need installed dependencies, and never a read-only baseline
reading of named paths at another commit, which has no dependency to miss. The commit
carrying item 21 is fixed by constraint 6 to land after this one. G6 of the R39 block stays
as it landed at eba5de68.
END-RECORD9

BEGIN-P49FROM
   measurement is `git show --numstat <commit> -- <path>` for the
   total, plus a per-line count over that diff's ADDED lines for the
   strays. The reviewer states which shape each pair is at authoring
   time, in the receipt itself.
END-P49FROM

BEGIN-P49TO
   measurement is `git show --numstat <commit> -- <path>` for the
   total, plus a per-line count over that diff's ADDED lines for the
   strays. The reviewer states which shape each pair is at authoring
   time, in the receipt itself.
   That per-line count is written for PROSE and binds prose only
   (R-0531). A slice of CODE repeats lines STRUCTURALLY — blank
   separators, closing parentheses, decorators and repeated argument
   lines are what code is made of — so "each TO-ONLY addition exactly
   1x among the added lines" is unattainable by construction for
   every code append, and demanding it invites the fabricated number
   R-0207 already warned about, arriving through a slice's LANGUAGE
   rather than through its pair shape. For a code append the
   obligation is ORDERED EQUALITY: the pre-commit blob is a
   byte-exact PREFIX of the post-commit file, the slice is an exact
   SUFFIX of it, and the lines that commit's diff ADDS are exactly
   the slice's lines IN ORDER. That reading is strictly stronger than
   the count it replaces — it fixes position as well as multiplicity
   — and it stays measurable however often a line recurs.
END-P49TO

BEGIN-CL20FROM
      workflow rewrites every round — `.agent/handoff.md`, `.agent/plan.md`,
      `.agent/last_block.md`, `.agent/context.md`. For those the rewrite is SCHEDULED
      rather than possible: the last commit of every round rewrites the handback by
      construction, so a bare path reference to one of them is stale before the round
      that wrote it has ended, and no ordering constraint can rescue it. Elsewhere a
      bare path is fine, and this clause deliberately reaches no further. R-0525 is the
      carve-out above being read too widely one round after it landed: it licenses an
      ordering constraint in place of a SHA for a claim about the round's OWN change,
      and a sentence locating a PRIOR round's text is not that claim.
END-CL20FROM

BEGIN-CL20TO
      workflow rewrites every round — `.agent/handoff.md`, `.agent/plan.md`,
      `.agent/last_block.md`, `.agent/context.md`. For those the rewrite is SCHEDULED
      rather than possible: the last commit of every round rewrites the handback by
      construction, so a bare path reference to one of them is stale before the round
      that wrote it has ended, and no ordering constraint can rescue it. Elsewhere a
      bare path is fine, and this clause deliberately reaches no further. R-0525 is the
      carve-out above being read too widely one round after it landed: it licenses an
      ordering constraint in place of a SHA for a claim about the round's OWN change,
      and a sentence locating a PRIOR round's text is not that claim.
      Finding R-0534 narrows this item from the SENTENCE to the READING. A clause that
      names a SHA for one reading and sets a second reading beside it in the present
      tense satisfies this item as worded and is still false on landing: the qualifier
      attaches to EVERY reading the clause states, including the working copies a
      transport proof lists last. The instance: a transport clause named
      `.agent/last_block.md` "at 757be21c" correctly, then called five copies equal with
      no commit named, while that round's own C0b had already overwritten the working
      copy two commits earlier — four of the five matched, and the sentence claimed five.
  21. **A baseline gate resolves its own paths at the base it names.** Finding R-0532. A
      gate ordered "at `origin/main` as well", or at any commit other than the one under
      review, is checked at emission with `git ls-tree <base> -- <path>` for EVERY path it
      names, because a path this branch ADDED does not exist there: the tool then exits
      non-zero on a missing file and produces no reading at all, so the comparison the
      gate exists to make is empty by construction rather than merely unreported. Drop
      that path from the baseline half and say so inline, or name a base where it
      resolves. R-0364 requires every gate to be EXECUTED at its base before it is
      ordered and item 12 pairs the reviewer's own dry run with a red control; this one
      governs whether the base run can produce a reading AT ALL, which neither reaches,
      because a command that exits on a missing path never evaluates the rule the gate
      was written for — the vacuous-gate shape of R-0438, arriving through the base
      rather than through a typo. The R39 instance: G6 ordered `ruff check` over
      `packages/orchestration/exec_guard.py` and its test at `origin/main`, and
      `exec_guard.py` was added on this branch, so both paths are absent there and the
      baseline half exited `E902 No such file or directory` per path.
      The same item carries the carve-out that instance also needed. A clause binding a
      block's commands to the PRIMARY checkout and never a worktree (R-0518, whose red is
      `apps/ui/node_modules` absent from any fresh worktree) reaches SUITE commands, which
      need installed dependencies, and never a read-only baseline reading of named paths
      at another commit: that reading has no dependency to miss, and requiring it in the
      primary checkout while also requiring another commit's content is a pair of
      sentences no worker can obey together. Read such a baseline with `git show
      <base>:<path>` into scratch, or in a disposable worktree under §4.10.
  22. **A sentence quantifying across COMMITS is measured over the whole range.** Findings
      R-0530 and R-0533. Any clause stating a value per commit, a value holding at "every
      commit after" one, or a total over a range is recomputed at emission by walking that
      range mechanically — `git rev-list --reverse <base>..<head>`, one reading per commit
      — and written as the list that walk produced, never generalised from the commits the
      author happened to read. Two forms have cost this branch a finding each. R-0530 was a
      correction that named two SHAs correctly and then added "and every commit after it",
      which its own round's C0b had already falsified. R-0533 is the same class one round
      later inside the record that REGISTERED R-0530: a per-commit insertion list read
      `349, 295, 50, 66, 6` where that fifth commit is 3 insertions and 3 deletions, so the
      sentence reported the churn column AGENTS.md DECISION F104 D1 excludes from the
      500-line cap. That recurrence is why this is an item rather than a habit — R-0530
      concluded "nothing new is owed to the checklist", and the class returned in the very
      paragraph that concluded it. Item 11 governs a claim about the author's OWN bytes and
      item 20 a claim about a FILE's content at a commit; this one governs a claim about a
      RANGE, which neither reaches, because each individual reading in it can be correct
      while the quantifier or the column is wrong.
END-CL20TO

BEGIN-PLANF9
## Current Step
R40, this round: record the R39 PASS and register R-0531 and R-0532, the two R39 gate
sentences its worker measured as unsatisfiable. Session-closing round: no production
code changes, and R41 takes the `ci_run.py` migration.
END-PLANF9

BEGIN-PLANT9
## Current Step
R41, this round: record the R40 PASS, register R-0533 and R-0534 — both defects in
RECORD8's own text — and resolve R-0530, R-0531 and R-0532 by writing their
counter-measures into `docs/agents/planner_reviewer_prompt.md`. No production code
changes; R42 takes the `ci_run.py` migration.
END-PLANT9
