
## DECISION F276 D10 (2026-09-20, reviewer, round 9) — the checklist consolidation merges item 17 into item 15 and says out loud that no free number was left, and the finding re-assignment follows the rotation rather than the verdict bookings

PART ONE, THE CONSOLIDATION. Operator amendment amend0827-process-diet rule 4 gives a
feature exactly one consolidation pass of the §3 pre-emission checklist, inside the
closure sequence, and the list must come out the same length or shorter. It stood at 35.

CHOSEN: item 17, "a pair that changes a structure's arity spans the whole structure",
is merged into item 15, "pair shapes are classified by a containment test, never by
eye", and the number 17 is RETIRED and never reused. The list comes out at 34, counted
mechanically over the checklist's own numbering after the edit. The family is the right
one and item 17's own text already named it: item 4 states what an APPEND claim
REQUIRES, while 15 and 17 both govern how the pair a block SHIPS is determined — 15
fixes the pair's SHAPE by a mechanical containment test, 17 fixes how far its FROM must
REACH. No containment test answers the reach question, so the merged item states them as
two clauses rather than one sentence, and neither clause loses a word of its instance.

THE DIRECTION WAS MEASURED, and the measurement did not come out the way F260's did.
That pass could retire item 19 because it had ZERO landed references, and the paragraph
it wrote implies such a number will be there next time. At `8da83220`, counted over
`.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/prose_slips.md` and
`.agent/decisions.md`, EVERY surviving number has at least one landed reference: the
smallest is item 17 at one, then item 29 at two, then items 21 and 27 at four each. So
17 is the number that strands the fewest, not the number that strands none, and the
consolidation paragraph in the prompt is amended to say that rather than to leave the
earlier implication standing. The append-only record's references to item 17 are not
rewritten — item 20 forbids that — and the retirement notice inside the merged item is
what a later reader follows.

ALTERNATIVES: merging item 29 into item 21, the two rules about a gate ordered AT A BASE,
which is an equally real family but strands two references instead of one; merging item
11 into item 16, rejected because the prompt's own text separates them deliberately and
item 11 carries 25 landed references; and a no-op pass, which rule 4 permits by its
letter — "the same length or shorter" — and which was rejected because the rule's stated
intent is that merging is the move and a closure that spends the one pass on nothing
spends it.

PART TWO, WHERE THE RE-ASSIGNMENT COMMIT SITS. `docs/roadmap/STATUS_closure_protocol.md`
step 5 states the finding re-assignment twice and the two statements disagree: its lead
sentence puts it "After the rotation and BEFORE the STATUS `[x]` flip", and the
parenthesis inside clause (i) says "same commit as the verdict bookings". The verdict
bookings are this round's FIRST commit and the rotation is a later one, so no single
commit satisfies both.

CHOSEN, FIRST, THE PLACE: the re-assignment is its OWN commit, placed AFTER the rotation
and before the flip, and the lead sentence governs. The reason is mechanical rather than
aesthetic: the rotation rewrites `.agent/live_review.md` wholesale and re-baselines every
byte offset in it, so an `Owner:` line edited before the rotation is an edit the rotation
must carry through its own per-record sha256 verification, and an edit made after it is
verified against the file the closure actually ships. The parenthesis is read as what it
plainly is — wording from before the rotation existed as a step of this sequence.

CHOSEN, SECOND, THE FORM: the re-assignment APPENDS a line to each open finding's
paragraph and MODIFIES no landed byte. Measured at `8da83220`, the sixteen open findings
divide three ways: seven carry no `Owner:` line at all, seven name `Owner: F273` — a
feature that has since closed without re-assigning them, which is the gap amend0911
rule A exists to prevent — and two already read `Owner: F282 — Findings paydown v2`. A
literal reading of "Owner: line rewritten" would edit fourteen landed paragraphs, and
seven of those have no such line to rewrite, so the instruction is already impossible as
written for half its subjects. §3 item 20 forbids repairing landed text by rewriting it
and names appending a dated correction as the way this record stays honest; that is
exactly what this is. So each of the fourteen gains ONE new final line naming F282 and
saying that it supersedes any earlier `Owner:` line in the same paragraph, the two that
already name F282 are left untouched, and the commit's `git show --numstat` for that path
reads insertions and ZERO deletions — which is itself the gate that no landed byte moved.

CONSEQUENCE: the §3 checklist runs 1 to 16, 18, 20 to 31 and 33 to 37, and the next
consolidation measures against 34. Every finding still open at this closure carries
`Owner: F282 — Findings paydown v2`, written in a commit that follows the rotation, and
no finding leaves this feature unowned.

REVERSE: restore `docs/agents/planner_reviewer_prompt.md` from `8da83220`, which puts
item 17 back and returns the list to 35; and for part two, move the re-assignment into
the verdict-booking commit of a future closure. Then delete this paragraph.
