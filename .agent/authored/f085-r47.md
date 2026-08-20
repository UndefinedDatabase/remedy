── STEP checklist promotion — F085 — R47 ─────────────────────────────────────

Goal: record the R46 PASS, register R-0548 for the plan-path defect R46's handback declared,
and carry the two counter-measures that are owed into the §3 pre-emission checklist — item 16
widened to reach any sentence that quantifies what follows it and any heading whose body fixes
a different value, and a NEW item 23 carrying R-0377's and R-0491's plan-path rule out of
finding prose. The plan advance R46 could not make is this round's first substantive commit.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R46 and register R-0548 · C3 both checklist edits · C4 handback.

CONVENTION, binding on every count here: a line count is the `splitlines` reading — a trailing
newline is NOT an extra line.

## Change

C1 applies PLANF→PLANT to `.agent/plan.md`. C2 appends RECORD15 to `.agent/live_review.md`.
C3 applies C16F→C16T and C23F→C23T to `docs/agents/planner_reviewer_prompt.md`. No source file
is touched this round and no `.py` path changes, so no lint gate and no code suite is ordered —
their absence is declared here rather than filled with a command that could not see this
round's change.

Change set, named rather than counted: `.agent/authored/f085-r47.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`,
`.agent/handoff.md`. Nothing else. `docs/roadmap/**` is NOT in that set, so the §3 docs tier
does not trigger; and NO test in this repository reads
`docs/agents/planner_reviewer_prompt.md` — the reviewer grepped `tests/` at c8da1928 and the
only match, `tests/test_agent_tooling.py` line 46, names the path inside a docstring and
asserts nothing about it. G4's green therefore proves NOTHING about C3, whose proof is G3's
pair shapes and G7's structure reading, and this sentence exists so no reader mistakes one for
the other.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r47.md` by its marker pair. Never retype one, never apply one from
   the prompt. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C4; if it exists, finish the
   commit in flight, write the handback and stop. `git status --porcelain` is empty at round
   start and after every commit; this round orders no destructive check, so it creates no
   worktree and `git worktree list` stays one line.
3. PAIR SHAPES, each tested mechanically by the reviewer at emission and its output printed
   here, per checklist item 15:
   - PLANF→PLANT on `.agent/plan.md`: `TO contains FROM: false` → REWRITE. Order the FROM 0x /
     TO 1x reading over the whole post-commit file.
   - C16F→C16T on `docs/agents/planner_reviewer_prompt.md`: `TO contains FROM: true` → APPEND.
     No FROM-zero count is owed; §4.9's per-line obligation applies instead.
   - C23F→C23T on the same path: `TO contains FROM: true` → APPEND. Same obligation.
   RECORD15 is an APPEND of PROSE to `.agent/live_review.md`: the target stays a byte-exact
   prefix, exactly one blank line joins it to the slice, nothing is reflowed. It carries no
   FROM, so no containment reading is owed for it.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of C3. Only C0a and C0b,
   which write nothing but the block itself, may precede it. This is the rule C23T writes, and
   this round is its first application; ordering the plan later would register a finding under
   a plan that does not yet name the round doing the registering.
5. PLANT states what this round DOES, in the present tense of a plan file, and asserts no
   landed fact about this round's own commits — the R-0524 carve-out is deliberately not
   invoked, because it is not needed. Every sentence in RECORD15 that reads a file THIS BLOCK
   also edits — `.agent/plan.md` at C1, the checklist at C3 — names the SHA c8da1928 in the
   same clause, per checklist item 20 as R-0521 narrows it.
6. Nothing outside the declared change set is touched. This round registers R-0548 and
   resolves nothing: the open count goes 135 → 136, next free id R-0549. R-0377 and R-0491
   stay OPEN by design; C2 records their recurrence and does not close them.
7. Item 17 asks how far a FROM must reach when a pair changes a numbered structure's arity.
   C23T adds item 23 at the END of the §3 checklist, whose items run 1 through 22 at
   c8da1928, so NO surviving entry is renumbered and a prefix-shaped FROM is correct here.
   The reviewer verified at c8da1928 that no line matches `^  23\. ` in that file. G7 is the
   reading that proves it stayed that way.
8. If a gate comes out red, STOP: write the handback naming the exact command, its exit code
   and its output. Never edit a slice to make a gate green.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines
   TOTAL, PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all
   three at emission and states them here: PROSE 180, TOTAL 308, RECORD15 61 lines. The worker
   re-measures all three from the committed `.agent/authored/f085-r47.md` and reports them; a
   mismatch is a finding against this block, not against the worker.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r47.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's `.remedy-wt/f085-r47.md` — disk-to-disk, not a digest fallback. Report sha256, byte
count, line count and marker-line count. Measure every one.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - C1 / PLANF→PLANT / `.agent/plan.md`, a REWRITE: PLANF occurs 0x and PLANT occurs exactly 1x
   in the post-commit file. Report both counts and `git show --numstat` for the path.
 - C2 / RECORD15 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's
   prose. §4.9's per-line obligation applies: every non-empty line the slice contains occurs
   exactly once among the lines C2's diff adds TO THAT PATH; report the slice's empty-line
   count. Report `git show --numstat` for the path.
 - C3 / both pairs / `docs/agents/planner_reviewer_prompt.md`, both APPEND-shaped: for EACH
   pair, its FROM occurs exactly 1x and its TO exactly 1x in the post-commit file, and every
   non-empty TO-ONLY line — the TO's lines minus the FROM's — occurs exactly once among the
   lines C3's diff adds to that path. Report the two TO-only line counts, C3's added-line count
   for the path and `git show --numstat`. 0 marker LINES reach the file.

G4 SUITE, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read `.agent/` state
live, and the two of them that assert on `.agent/plan.md` are the reason this is the right
class for C1; base reading at c8da1928, taken by the reviewer in the primary checkout,
`159 passed`. REPORT the number this run prints. CANARY
`python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer
collected by grepping `tests/` at c8da1928 plus the AGENTS.md cap: the file contains `## Goal`,
contains `## Next Steps`, matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count
and each of the three booleans. G4 covers the first three through their tests; this gate covers
the cap, which no test reads.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
c8da1928 and at HEAD, from the line-start patterns for a registration, a resolution and a
landed line. The reviewer's base reading is 162 / 27 / 0, 135 open, max registered R-0547, max
resolved R-0532. At HEAD registered must be 163, the registered symmetric difference exactly
R-0548, done and landed symmetric differences EMPTY, 136 open, next free id R-0549. Report the
three symmetric differences, the duplicate-id count and the count of resolutions naming an
unregistered id, at both SHAs.

G7 STRUCTURE, on `docs/agents/planner_reviewer_prompt.md` after C3. Collect every line matching
`^  (\d+)\. \*\*` in the §3 pre-emission checklist — the region from the checklist's own
introductory bullet to the line beginning `  Why this is on disk`. Their numerals must be
exactly 1 through 23 in ascending order, with no duplicate and no gap, and no line matches
`^  24\. `. Report the numeral list as the walk produced it. This is the gate that proves item
17's arity question was answered correctly; no test in this repository reaches this file.

G8 HYGIENE. `git diff --name-only c8da1928..HEAD` measured BEFORE C4 holds exactly the change
set above minus `.agent/handoff.md`, which C4 writes, and nothing else. Report per-commit
insertions for every commit BEFORE C4 — C4 cannot measure itself, so its own insertions go in
the round report — and confirm none exceeds 500. This branch already spent the AGENTS.md
declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under constraint
8, never a declaration. Confirm every commit has exactly one parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch,
base SHA c8da1928, a per-commit changed-files table, the item-status table covering C0a, C0b,
C1, C2, C3 and C4, the real G1-G8 results with exit codes, the open-findings count and the next
expected action. Keep it inside the 60-line cap, or name the DECISION D15 stated cause and the
exact mandated content behind it. Repeat this Fortschritt line verbatim:
Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R46 PASS ·
T002a KOMPLETT · T002b KOMPLETT, alle Sites der Klasse auf dem Seam · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section states that the next round is R48, started by a FRESH session; that R48
opens T002c with the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy
differs from the `test` class because their children are the long-lived harness and take no
wall timeout; and that T002d, T003, the integration gate and closure follow. It also states
that R47's own verdict is NOT on disk as a gate entry, because the round that records a verdict
cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is
the terminator, not a missing gate, and R48 must not open a repair round to close it.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLANF
## Current Step
R45, this round: record the R44 PASS, register R-0539 through R-0546, rule DECISION F085 D6 on
the block budget, and migrate `packages/orchestration/builder_bridge.py` onto the stage-1 guard
as the last `test`-class site. T002b closes with this round.

## Next Steps
1. R46 — the checklist item 16 widening R-0537 and R-0543 both name, cut from R45 for size,
   then T002c: the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy
   differs from the `test` class in taking no wall timeout, because their children are the
   long-lived harness rather than a bounded suite run.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANF

BEGIN-PLANT
## Current Step
R47, this round: record the R46 PASS, register R-0548 for the plan-path defect R46's handback
declared, and promote two counter-measures into the §3 pre-emission checklist — item 16 widened
past headings, and a new item 23 carrying the plan-path rule R-0377 and R-0491 state only as
finding prose. No source file changes this round.

## Next Steps
1. T002c — the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy differs
   from the `test` class in taking no wall timeout, because their children are the long-lived
   harness rather than a bounded suite run.
2. T002d — the five runtime sites, under that same no-wall-timeout policy.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANT

BEGIN-RECORD15
Gate: R47 — the R46 entry. R46 PASSED. Every ordered gate G1-G6 was re-executed by the reviewer
over 470d2577..c8da1928, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r46.md`, the committed `.agent/authored/f085-r46.md` at
6f302271, the committed `.agent/last_block.md` at 5b351a2e and both working copies as they
stand at c8da1928 are all five byte-EQUAL at sha256
89a8b79bd98dbc53c40225c15b0070e9a57cad5d1cb788d6eef2dac6bce1363c, 13950 B, 192 lines, 4 marker
lines. BOTH APPENDS HELD THEIR SHAPE, and the reviewer extracted the two slices programmatically
from the committed block by marker pair rather than retyping them: for RECORD14 on
`.agent/live_review.md` and DEC6C on `.agent/decisions.md` alike the pre-commit blob is a
byte-exact prefix, the remainder is exactly one blank line plus the slice, the slice is an exact
suffix, 0 marker LINES reached either file, and every non-empty slice line occurs exactly once
among that path's added lines — 59 slice lines of which 3 empty against 60 added for the first,
16 of which 3 empty against 17 for the second, at sha256 ecb74b8c782b1baa… and
b1bb9c74c7725dea…, the two digests the R46 handback also reports. THE SUITES WERE RE-RUN, NOT
READ, each in the primary checkout, each exit 0: the four state readers `159 passed` against a
base of 159, the canary `42 passed` against 42. THE ARITHMETIC MOVED AS ORDERED: 162 / 27 / 0 at
c8da1928 against 161 / 27 / 0 at 470d2577, 135 open against 134, the registered symmetric
difference exactly R-0547, done and landed symmetric differences EMPTY, no duplicate id and no
resolution naming an unregistered id at either SHA. HYGIENE IS CLEAN: walking the range
mechanically gives the per-commit insertion counts 192, 144, 77 and 31, none over 500 and so no
second call on the allowance d4473f85 spent; the path set of the range ending at 9afeeb86 is
exactly the four ordered paths and the full range adds only `.agent/handoff.md`; all four
commits are single-parent; the tree is clean and `git worktree list` is one line.

THE CORRECTION IS REAL, NOT MERELY APPLIED. Measured at c8da1928 in `.agent/decisions.md`:
DECISION F085 D6's heading still reads 480 while its CHOSEN and CONSEQUENCE paragraphs read 490,
and DEC6C now stands later in that same file fixing the ruled figure at 490 without editing D6,
which is checklist item 20's rule that landed text is corrected by appending and never by
rewriting. R-0547's description of the defect reproduces on disk in every particular.

- R-0548 — Medium, REVIEWER-BLOCK DEFECT, A ROUND REGISTERED A FINDING UNDER A CHANGE SET THAT
NAMED NO PLAN, WHICH IS ALREADY THE COUNTER-MEASURE OF TWO OPEN FINDINGS AND THE BINDING RULE OF
NEITHER. The R46 block, committed at 6f302271, names five paths in its change set — the authored
block, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/decisions.md` and
`.agent/handoff.md` — and its constraint 5 forbids touching anything outside that set. That same
round registered R-0547. R-0377 rules, still OPEN: "any round whose bundle registers, resolves
or renumbers a finding names `.agent/plan.md` in its change set and rewrites its ledger in the
round's FIRST commit". R-0491 rules, still OPEN: the plan update "is ordered as the FIRST commit
of a round that has substance to record", ahead of everything but the two block-save commits.
R46 satisfied neither, and its worker did the only correct thing available to it — it declared
the conflict as handback deviation 2 rather than widening the change set past a gate that would
then have gone red, which is what constraints 5 and 6 of that block require. Measured at
c8da1928, before this round's own C1 changes it: `.agent/plan.md` reads "R45, this round" under
its `## Current Step` heading and its Next Steps item 1 describes R46 as work still to come,
while all four of R46's commits stand above it in the history. THE COST IS THE ONE R-0377
ALREADY PRICED: AGENTS.md's Session Resume tells a new session to read `.agent/plan.md` second,
ahead of the review record, so a bootstrapping reader starts from a plan one round behind that
names the round it is reading as unstarted. AGENTS.md's Commit Gate item 1 — "Verify
`.agent/plan.md` matches the current work ... If any of these fail: DO NOT COMMIT" — was
unmet for all four of R46's commits, and a broken repository rule rather than a broken
convention is why this is Medium. THE CAUSE IS NOT THE R46 BLOCK ITSELF. It is that R-0377's and
R-0491's counter-measures live as finding PROSE and were never promoted into the §3 pre-emission
checklist, so no block reads them at the one moment they bind — the class this repository keeps
paying for, in which a standing rule stated in a finding body binds nothing. That is why the
counter-measure here is a checklist item and not a third restatement: this same round adds item
23 carrying both rules, and its own C1 advances the plan ahead of every other substantive
commit, which is the first application of the rule it writes. R-0377 and R-0491 stay OPEN. This
finding records their recurrence and resolves neither, because neither is resolved until a later
round demonstrates the promoted item catching what the prose did not. Found and registered by
the reviewer while gating R46.
END-RECORD15

BEGIN-C16F
      sweep every heading in the block, not the one that changed.
END-C16F

BEGIN-C16T
      sweep every heading in the block, not the one that changed.
      Findings R-0537, R-0543 and R-0547 widen this item twice over, and the two widenings
      are independent of each other. FIRST, from a HEADING to ANY SENTENCE that quantifies
      what follows it: a finding headline counting the instances its own body gives, a plan
      sentence counting the tests its round shipped, a goal line counting the sites a bundle
      touches. A headline is a heading by every property that made this item necessary — it
      is the half nobody re-reads and the half that drifts once the body grows — and R-0537
      and R-0543 are that same shape one round apart, the first counting FOUR of something
      its body gives three of, the second saying "five tests" over a round that shipped
      four. SECOND, from a COUNT to ANY VALUE the body beneath it fixes: R-0547 is a
      DECISION whose heading rules 480 lines TOTAL while its own CHOSEN and CONSEQUENCE
      paragraphs rule 490, so the numeral is a budget rather than a tally and this item as
      first written does not reach it at all. Both widenings share one mechanical check,
      which is what to run before emission: for every heading, every finding headline and
      every quantifying sentence in the block, read the numerals it states against the body
      beneath it, and wherever the two can drift apart, DELETE the numeral from the heading
      rather than synchronise it. A ruled figure that must appear in a heading appears there
      once, in the same words as the body that rules it, so that a later revision cannot
      change one without visibly contradicting the other.
END-C16T

BEGIN-C23F
      while the quantifier or the column is wrong.
END-C23F

BEGIN-C23T
      while the quantifier or the column is wrong.
  23. **A round that touches the finding ledger names `.agent/plan.md` in its change set.**
      Findings R-0377, R-0491 and R-0548. A block whose bundle registers, resolves or
      renumbers a finding also advances `.agent/plan.md`, and orders that update as the FIRST
      substantive commit of the round — only the two block-save commits, which write nothing
      but the block itself, may precede it. Omitting the path does not make the change set
      smaller; it makes a pair of rules that cannot both hold, because AGENTS.md's Commit Gate
      item 1 requires the plan to match the current work before EVERY commit while the block's
      own change-set constraint forbids touching anything unnamed. An honest worker can then
      only declare the conflict, which repairs nothing, and the plan stays false on disk for
      the length of a round — the file AGENTS.md's Session Resume tells the next session to
      read SECOND, ahead of the review record. Where a round genuinely cannot advance the plan
      first, the block says so in its own text and names the commit at which the plan becomes
      current, rather than leaving the worker to discover the conflict. This is an item rather
      than a habit because R-0377 and R-0491 each stated exactly this counter-measure in a
      finding BODY and neither bound anything: R-0548 is the R46 block registering a finding
      under a five-path change set holding no plan, features after the first of the two was
      written. A rule that lives only in a finding body is a rule the next block does not
      read.
END-C23T
