── STEP T002b interlude — F085 — R34 ─────────────────────────────────────────

Goal: record the R33 FAIL, and register AND resolve R-0522, R-0523 and R-0524 — a
pair the block labelled REWRITE while its TO contained its FROM verbatim, the false
rewrite proof that label produced in the permanent record, and the slice class for
which checklist item 20's newly required SHA cannot exist at all.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 narrow
checklist items 15 and 20 · C2 record R33 and register and resolve R-0522, R-0523 and
R-0524 · C3 plan · C4 handback.

## Why this round exists — read before C1

R33 failed on one sentence. Every gate the R33 block ordered was re-run by the
reviewer over c2033d6c..7480d880 and every one reproduces the handback's reading
exactly: the block's five copies byte-equal at sha256 a089cc66, the append commit
c933b949 holding its shape at numstat 79/0, the arithmetic moving 135/17/0 to
136/18/0 with 118 open at both ends, the checklist narrowing landed once, and the
suites at 159, 295 and 42 passed. The worker deviated from nothing.

The defect is in the handback's `## Authored-text proofs` section. It states that
SHARPF→SHARPT and PLANF→PLANT are "both REWRITE" and that "each FROM matched exactly
once before apply and 0 times after". At 74dfa30e the SHARPF text occurs ONCE in
`docs/agents/planner_reviewer_prompt.md`, not zero times, because SHARPT begins with
SHARPF verbatim: the pair is APPEND-shaped. The reviewer's constraint 2 declared it a
REWRITE while claiming a mechanical containment test per pair, and the worker then
reported the rewrite proof's number for a count that cannot come out that way.

That is checklist item 15 — the R-0508 counter-measure — being obeyed in form and
defeated in substance, one round after item 20 was narrowed for the identical reason.
Item 15 asks that "the answer is printed beside that pair"; the R33 block did print
an answer, and the answer was a LABEL rather than the test's output. A label is a
recollection wearing a measurement's clothes, so the narrowing records the boolean
and derives the label from it.

A third defect is the reviewer's alone and blocks this very block. Item 20 as
narrowed by R-0521 demands an absolute SHA that already exists when a slice is
written, justified by "a block always has such a SHA to hand, because its own base is
stated in its done-when". That covers a reading taken BEFORE the round. It cannot
cover a slice describing the round's OWN landed change — and every `Done:` paragraph
is exactly that, including those below. Demanding a SHA there demands a value
that cannot exist, which is the R-0371 shape. Item 20 gains the carve-out in C1, and
C2 relies on it; the commit order is what makes that honest.

This round changes no production code, so it orders no red proof and no ruff run.

## Change

C1 — `docs/agents/planner_reviewer_prompt.md`, one commit, the pairs P15F→P15T, which
narrows checklist item 15, and P20F→P20T, which carves out item 20. Neither adds or
removes an item, so no list arity changes and no label is renumbered.

C2 — `.agent/live_review.md`, one commit, RECORD2 appended and nothing else. RECORD2
carries the R33 gate entry, then the registrations, then the resolutions, as one
slice.

C3 — `.agent/plan.md`, one commit, the PLANF2→PLANT2 pair over the Current Step block
alone. Next Steps is untouched: the migration order did not change.

Change set, named rather than counted: `docs/agents/planner_reviewer_prompt.md`,
`.agent/authored/f085-r34.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md` and `.agent/handoff.md`. Nothing else is touched.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r34.md` by its marker pair. Never retype a slice,
   never apply one from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test and recorded as
   the test's OUTPUT, one reading per pair:
   P15F→P15T — TO contains FROM: true — APPEND.
   P20F→P20T — TO contains FROM: true — APPEND.
   PLANF2→PLANT2 — TO contains FROM: false — REWRITE.
   For the two APPEND pairs the "FROM 0x after" count is unattainable by
   construction and is NOT ordered; §4.9's append obligation is ordered instead. Do
   not report a FROM-zero reading for them under any wording.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists,
   finish the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This
   round orders no destructive check, so it creates no worktree; `git worktree list`
   is one line throughout.
5. C2 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD2. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round registers and
   resolves R-0522, R-0523 and R-0524 and touches no other id, so the open count must
   come out unchanged.
7. If any gate comes out red, or a FROM does not match at exactly one place in the
   file it is applied to, STOP: write the handback naming the exact command, its exit
   code and its output, and do not improvise a repair.
8. STALENESS, standing: after C3 re-read every edited file and confirm that no
   sentence this round put on disk was falsified by a later commit of the same round,
   and that no slice quotes another file's current wording as a claim. Name what was
   re-read. RECORD2 states facts about `docs/agents/planner_reviewer_prompt.md` and
   `.agent/live_review.md`, both of which this block edits. Every reading RECORD2
   ASSERTS about a state BEFORE this round names the SHA 7480d880 or an earlier one;
   every claim about a state this round CREATES names constraint 9 instead, under the
   item-20 carve-out C1 lands. `HEAD` appears nowhere in RECORD2 as a reading.
9. The commit order C1 before C2 is load-bearing twice over: it is what makes
   RECORD2's claims about the narrowed items 15 and 20 true when they are written,
   and it is what licenses RECORD2 to use the item-20 carve-out at all. Do not
   reorder.
10. Do not "repair" the R33 handback. `.agent/handoff.md` is rewritten by C4 in the
    normal way; the false proof sentence is corrected by RECORD2's registration, not
    by editing landed text — the R-0521 principle.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r34.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report the sha256, the
byte count, the line count, the number of marker lines, and region digests over the
line ranges 1-100, 101-200 and 201-end, each digest taken over those lines with their
trailing newlines included. Do not compute any of those numbers by hand; measure
them.

G3 APPEND SHAPE for C2. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank line
plus RECORD2; RECORD2 is an exact suffix of the post-commit file; RECORD2's first
line occurs once among the lines that commit's diff ADDS; 0 lines matching
`^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker LINES, never the substring,
because the quoted regex already appears in that file's prose. Report
`git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in
`.agent/live_review.md` at base 7480d880 and at HEAD, taking registered from
`^- R-\d{4} — `, done from `^Done: R-\d{4} — ` and landed from `^Landed: R-\d{4}`.
The reviewer's base reading is 136 registered / 18 done / 0 landed, 118 open, max
registered R-0521 and max resolved R-0521; at HEAD it must be 139 / 21 / 0 with 118
open again and both maxima R-0524. Report the registered symmetric difference and the
done symmetric difference (each must hold exactly R-0522, R-0523 and R-0524), the
landed symmetric difference (empty), the count of duplicate ids, the count of
resolutions naming an unregistered id, the maximum id, and the next free id, which
moves from R-0522 to R-0525.

G5 THE NARROWINGS LANDED, measured at HEAD after C1, and the APPEND obligation
for both pairs. In `docs/agents/planner_reviewer_prompt.md`:
- the P15F text still occurs exactly once and the P20F text still occurs exactly
  once, because both pairs are APPEND-shaped and their FROMs survive by construction;
- the item-15 opener
  `  15. **Pair shapes are classified by a containment test, never by eye.** Finding`
  and the item-20 opener
  `  20. **A slice states a fact about a file the same block edits only with the commit`
  and the item-16 opener
  `  16. **No heading states a count of the contents beneath it.** Finding R-0510. A`
  and the closing paragraph opener
  `  Why this is on disk and not a habit: item 2 has recurred six times across`
  each still occur exactly once, because this commit narrows two items rather than
  adding, removing or renumbering any;
- every line that P15T and P20T add and their FROMs do not contain occurs exactly
  once AMONG THE LINES C1's DIFF ADDS — that is the §4.9 append obligation, and it is
  the reading ordered INSTEAD of a FROM-zero count;
- 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` reached the file.
Report `git show --numstat` for C1.

G6 STATE READERS AND DOCS. This round changes no production code, so it orders no
ruff run and no red proof. Because it rewrites `.agent/` state:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading
`159 passed`. RUN IT IN THE PRIMARY CHECKOUT AND NEVER IN A WORKTREE: R-0518 records
why, and a red naming `TestVitestFrontendTestFoundation::test_vitest_passes` with
`apps/ui/node_modules` absent IS that finding rather than a regression. Any other red
is a STOP under constraint 7. Because a file under `docs/` changes:
`python3 -m pytest tests/docs/ -q` exits 0, base reading `295 passed`. Do NOT read
that green as evidence about C1: the reviewer ran the red control in a disposable
worktree at 7480d880 and, with `docs/agents/planner_reviewer_prompt.md` replaced by
the single line `# broken`, the suite still returned `295 passed`. No test under
`tests/docs/` reads that file, so this gate covers the README index and roadmap
consistency and is BLIND to C1 by construction. G5 is the only check on C1's content.
CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
`42 passed`.

G7 COMMIT HYGIENE. `git diff --name-only 7480d880..HEAD` measured BEFORE C4 holds
exactly the paths named in the change set above, minus `.agent/handoff.md` which C4
writes, and nothing else. Report per-commit insertions for every commit BEFORE C4 —
C4 cannot measure itself, so report its own insertions in the round report instead —
and confirm none exceeds 500. Confirm every commit has exactly one parent and that
`git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
branch, base SHA 7480d880, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2, C3 and C4, the real verification results for G1-G7 with
exit codes, the open-findings count, and the next expected action. In the
`## Authored-text proofs` section, report each pair under the shape constraint 2
assigns it and NEVER report a FROM-zero count for an APPEND pair. Repeat this
Fortschritt line verbatim:
Fortschritt: ~70 % (T001 gebaut · R13-R32 PASS · R33 FAIL, hier repariert · T002a
KOMPLETT · T002b 9 von 12 Sites auf dem Seam, 3 offen · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The handback MUST state, in its `## Next` section, that the next session's first
action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open
PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). It
MUST also state that R34's own verdict is NOT a §4.13 terminator because this branch
continues, that the next reviewed round records R34's gate entry in
`.agent/live_review.md`, and that the next MIGRATION round takes `mission_state.py`'s
spawn, because `builder_bridge.py` cannot move until the seam can SET an environment
value rather than only allowlist a key.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-P15F
      likely to be trusted. Nothing broke that round only because no gate ordered the
      unsatisfiable "FROM 0x" reading; the next block to order one pays for it.
END-P15F

BEGIN-P15T
      likely to be trusted. Nothing broke that round only because no gate ordered the
      unsatisfiable "FROM 0x" reading; the next block to order one pays for it.
      Finding R-0522 narrows what "the answer is printed" means: the constraint records
      the containment test's own OUTPUT — the words `TO contains FROM: true` or
      `TO contains FROM: false` — and the APPEND or REWRITE label is derived from that
      output on the same line, never written on its own. A bare label is a recollection
      wearing a measurement's clothes, and it is indistinguishable on the page from a
      measured one, which is how R-0522 arose one round after this item was last
      relied on: a block declared a pair a REWRITE while its TO began with its FROM
      verbatim, and the handback then reported the rewrite proof's FROM-zero count for
      a FROM that still occurred once. A block that records `true` orders the §4.9
      append obligation and never a FROM-zero count, and it says so in the same
      constraint, because the unattainable count is what turns a mislabelled pair into
      a false line in the permanent record.
END-P15T

BEGIN-P20F
      hand, because its own base is stated in its done-when. R-0521 is this rule
      failing while being obeyed: the slice that RESOLVED R-0520 wrote "at HEAD",
      satisfied item 20 as it was then worded, and was falsified one commit later by
      its own round.
END-P20F

BEGIN-P20T
      hand, because its own base is stated in its done-when. R-0521 is this rule
      failing while being obeyed: the slice that RESOLVED R-0520 wrote "at HEAD",
      satisfied item 20 as it was then worded, and was falsified one commit later by
      its own round.
      Finding R-0524 carves out the one class for which no such SHA can exist. A slice
      that describes THIS round's own landed change — every `Done:` paragraph is of
      that class — asserts a fact whose commit has not been written when the slice is
      authored, so it names instead the block CONSTRAINT that fixes the commit order,
      and the block carries that constraint as an ordering requirement the worker
      cannot satisfy by accident. The base SHA answers a reading taken BEFORE the
      round; the ordering constraint answers a reading only the round itself makes
      true, and demanding a SHA for the second demands a value that cannot exist when
      the text is written — the R-0371 shape, which this checklist already forbids for
      gates and now also forbids for slices. The carve-out is narrow on purpose: it
      reaches a claim about the round's OWN commits and nothing else, and a reading of
      any PRIOR state still names its SHA.
END-P20T

BEGIN-RECORD2
Gate: R34 — the R33 entry. R33 FAILED, on one sentence, under §4.5's "unverified
completion claims". EVERY GATE R33 ORDERED REPRODUCES: the reviewer re-ran G1-G7 over
c2033d6c..7480d880 and each returns the handback's reading. TRANSPORT WAS PROVED
AGAINST THE REVIEWER'S OWN ORIGINAL, not only against a digest: the scratch file the
block was authored into, the committed `.agent/authored/f085-r33.md`, the committed
`.agent/last_block.md` and both working copies are all five byte-EQUAL at sha256
a089cc6604b57cfd9c7ee5449742a4651c10c9d7db80af0f8da735bd5b566404, 19296 B, 305 lines,
10 marker lines, region digests 2c1d1941, 84609b00 and f6c3a188 under the
trailing-newline convention the handback used. THE APPEND COMMIT HELD ITS SHAPE:
c933b949's pre-commit blob is a byte-exact PREFIX of the 373548 B post-commit file,
the remainder is 6064 B = one blank line plus RECORD1, RECORD1 is an exact suffix,
its first line occurs once among the 79 lines that commit adds, numstat 79/0, 0 lines
match `^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 7 times. THE
ARITHMETIC MOVED IN BOTH SETS BY ONE ID: 135 registered / 17 done / 0 landed at
c2033d6c against 136 / 18 / 0 at 7480d880, 118 open at both ends, registered and done
symmetric differences each exactly R-0521, landed symmetric difference empty, no
duplicate id, no resolution naming an unregistered id, and next free R-0522. THE
NARROWING LANDED WHERE IT WAS AIMED: at 7480d880 the item-20 opener, the new
`identifier that already EXISTS` line and the checklist's closing paragraph each
occur exactly once in `docs/agents/planner_reviewer_prompt.md`, 0 marker lines
reached it, numstat 9/1, and 74dfa30e does precede c933b949 as R33's constraint 9
required. THE SUITES WERE RE-RUN, NOT READ: the four state readers `159 passed`, the
docs suite `295 passed` and the canary `42 passed`, each as its exact ordered command
line in the primary checkout, each exit 0. COMMIT HYGIENE IS CLEAN: the path set is
the six declared paths, per-commit insertions are 305, 223, 9, 79, 13 and the
handback's own 89, none over 500, all six commits are single-parent, the reflog holds
only `commit:` entries, and the ordered push landed — origin and local agree at
7480d880. The worker deviated from nothing it was ordered to do.

WHAT FAILED IS A SENTENCE NO GATE ASKED FOR. R33's handback closes its
`## Authored-text proofs` section by calling both pairs REWRITE and stating that each
FROM "matched exactly once before apply and 0 times after". The reviewer measured the
SHARPF text at 74dfa30e: it occurs once, not zero times. The findings follow: the
reviewer's mislabelling, the false line it produced, and one the reviewer found while
authoring this block's own resolutions.

- R-0522 — Medium, A PAIR WAS DECLARED A REWRITE WHILE ITS TO CONTAINED ITS FROM
VERBATIM, BY A CONSTRAINT THAT CLAIMED A MECHANICAL CONTAINMENT TEST. R33's constraint
2 reads "Pair shapes, each MEASURED by the reviewer with a containment test, one
reading per pair: SHARPF→SHARPT REWRITE · PLANF→PLANT REWRITE". SHARPT begins with
SHARPF verbatim, so the containment test returns true and the pair is APPEND-shaped;
PLANF→PLANT is a REWRITE and that half is right. This is checklist item 15 — itself
the counter-measure for R-0508, the finding in which a block "ran the check for the
single pair it suspected" and generalised — recurring one feature later in the round
that had just narrowed item 20 for the same underlying reason. Item 15 was obeyed as
written: a per-pair reading WAS printed. What was printed was the LABEL and not the
test's output, and a label is indistinguishable on the page from a measured one, so
nothing downstream could catch it. Medium rather than Low because the label is what
the worker's proof obligation is derived FROM: a wrong label does not stay a
documentation defect, it manufactures a false measurement, which is R-0523.

- R-0523 — Medium, A HANDBACK REPORTED A PROOF NUMBER THAT THE FILE ON DISK
CONTRADICTS. R33's handback, applied at 7480d880, states in `## Authored-text proofs`
that SHARPF→SHARPT and PLANF→PLANT are "both REWRITE; each FROM matched exactly once
before apply and 0 times after, each TO once after". At 74dfa30e the SHARPF text
occurs exactly once in `docs/agents/planner_reviewer_prompt.md` and the SHARPT text
occurs exactly once, because the second contains the first; the claim is true of
PLANF→PLANT and false of SHARPF→SHARPT. §4.5 lists unverified completion claims among
the block conditions, so this is the sentence that costs R33 its PASS even though
every ordered gate is green — a round's verdict is not the conjunction of its gates.
The defect is not dishonesty: §4.9 says in terms that demanding a FROM-zero count for
an append-shaped pair "invites either a fabricated number or a pointless repair
round", and this is that invitation being accepted. The counter-measure is upstream,
at R-0522, because a worker handed a correct shape reports a correct number. The
landed sentence is NOT rewritten: this paragraph is its correction, per R-0521.

- R-0524 — Low, ITEM 20 NOW DEMANDS A SHA FOR A CLASS OF SLICE IN WHICH NO SHA CAN
EXIST. R-0521's narrowing, applied at 74dfa30e, requires that the commit a slice names
be "an absolute identifier that already EXISTS when the slice is written", justified
on the ground that "a block always has such a SHA to hand, because its own base is
stated in its done-when". The base SHA answers a reading of a state that PRECEDES the
round. It cannot answer a slice that asserts what the round's own commits have just
made true — and every `Done:` paragraph in this file is of that class, including
those in this entry, which assert what items 15 and 20 require after C1 of R34. For
those the required identifier is a commit that does not exist when the slice is
authored, so the rule as narrowed is satisfiable only by a value that cannot be
written: the R-0371 shape, which this same checklist forbids for gates. Low because
it has cost no round yet and was caught while authoring rather than after landing.
Found by the reviewer against its own draft, which is where item 20 is supposed to be
read.

Done: R-0522 — Resolved at R34. Checklist item 15 of
`docs/agents/planner_reviewer_prompt.md` §3 now requires the constraint to record the
containment test's OUTPUT — `TO contains FROM: true` or `false` — with the APPEND or
REWRITE label derived on the same line, and it states that a `true` reading orders the
§4.9 append obligation and never a FROM-zero count. The narrowing is applied by the
commit that constraint 9 of this round's block fixes ahead of this one; constraint 2
of that same block is the first use of the new form, recording a boolean for every
pair it lists.

Done: R-0523 — Resolved at R34. This registration is the correction, and it is the
whole resolution: the false sentence stays in `.agent/handoff.md` where it landed,
because overwriting landed text is worse than a dated wrong sentence. What stops the
class is R-0522's narrowing plus the constraint this round's block carries, which
forbids reporting a FROM-zero count for an APPEND pair under any wording. No gate is
added, because no gate could have caught a number nothing ordered.

Done: R-0524 — Resolved at R34. Checklist item 20 of
`docs/agents/planner_reviewer_prompt.md` §3 now carves out the slice that describes
the round's own landed change: it names the block CONSTRAINT fixing the commit order
instead of a SHA, and a reading of any prior state still names its SHA. Applied by the
commit that constraint 9 of this round's block fixes ahead of this one, which is what
lets these three paragraphs name constraint 9 rather than an impossible identifier.
END-RECORD2

BEGIN-PLANF2
## Current Step
R33, this round: record the R32 PASS, and register and resolve R-0521 by narrowing
pre-emission checklist item 20 so the commit a slice names must be a SHA that
already exists rather than a label that re-resolves. No production code changes.
END-PLANF2

BEGIN-PLANT2
## Current Step
R34, this round: record the R33 FAIL, and register and resolve R-0522, R-0523 and
R-0524 — a pair mislabelled REWRITE, the false rewrite proof that label produced, and
the slice class item 20's required SHA cannot reach. No production code changes.
END-PLANT2
