# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

FOUR CANDIDATES ARE OPEN, all raised by the reviewer at the F109 closure gate on
2026-09-03 and none of them carrying an R-id, per the closure protocol's
"Closure-candidate findings" ruling. The FIRST reviewed round of the next session
registers each one with the next free id or resolves it inline as a §4.7
DECISION, and empties this file in that same round.

1. THE §3 CHECKLIST CONSOLIDATION PASS THAT F109 OWED WAS NEVER PERFORMED ·
source feature F109 · 2026-09-03. Operator amendment amend0827-process-diet rule
4 freezes the pre-emission checklist of `docs/agents/planner_reviewer_prompt.md`
§3 while a feature is open and requires the consolidation to happen EXACTLY ONCE
per feature, inside the closure sequence, coming out the SAME LENGTH OR SHORTER.
MEASURED at `d065f7cb`: `git log 5e18a853..HEAD -- docs/agents/planner_reviewer_prompt.md`
returns NO commit, so that file was never touched on this branch and the pass did
not happen. The list stood at 37 items on 2026-08-27, which is the number the
next consolidation measures against. F109 ran 21 rounds and produced lessons that
belong to it; they are candidate 2 below.

2. `.agent/prose_slips.md` STOPPED BEING WRITTEN AFTER F109 ROUND 7, WHILE LATER
ROUNDS KEPT PROMISING IT · source feature F109 · 2026-09-03. MEASURED at
`d065f7cb`: the file's last entry is dated `2026-09-03 · F109 R7`, and rounds 8
through 21 added none — yet gate entries and handbacks across those rounds
repeatedly routed a reviewer-prose inaccuracy to "a `.agent/prose_slips.md` line
at the consolidation". Since the consolidation also did not happen (candidate 1),
those lessons exist only inside `.agent/live_review.md` gate paragraphs. The ones
this session named, so they are not lost: the R-0783 finding text called itself
"THE SIXTH SITE" of the stale-prose class while omitting `R-0782`, making the
true count SEVEN, corrected in the R18 gate entry; gate G6 of the round 18 block
asked a marker string to "resolve in the modules named" when it lives in one
module and reaches the other by import; gate G3(d) of that same block named a
base two rounds earlier than G3(a) did, so its ledger delta spanned two rounds;
the round 17 block's constraint 6 sent a running suite's log inside the measured
repository on an over-wide reading of `R-0176`, which the worker corrected by
measuring that `worktree_identity()` cannot see a gitignored file; the round 17
block implied `REMEDY_UI_NO_AUTO_BUILD` for the whole gate where
`docs/agents/integration_gate.md` scopes it to the base run; and the round 20
block asserted the review zip would land in the repository root when the packager
archives it outside the repository.

3. THE ROUND 21 BLOCK'S CLOSURE COMMIT PATH SET NAMED A FILE IT LEFT NOTHING TO
WRITE · source feature F109 · 2026-09-03. The block listed `.agent/plan.md` among
the five paths C3 must touch while its own bundle assigned the single authored
plan slice to C1, whose text is already terminal, so C3 had no plan diff to make.
This is the R-0527 class — a block constraint asserting a property its own slices
do not have. The worker refused both routes to a green gate, declining to author
unordered bytes over a just-verified slice and declining to move the slice against
the bundle, and reported the gate PARTIAL with the reason. That is the correct
behaviour and the reason this is a candidate rather than a defect on disk: C3
landed with four paths, README and STATUS still shared one commit, and nothing
outside the change set was touched.

4. A CLOSURE GATE CLAUSE WAS VACUOUS AND THE WORKER SAID SO RATHER THAN BANKING
IT · source feature F109 · 2026-09-03. Gate G6 of the round 21 block ordered the
count of the literal U+2014 character in `scripts/self_use_queue.json` compared
before and after the edit, as the discriminator proving no `json.dumps` round
trip had occurred. That count is 0 before and 0 after, because `R-0785`'s damage
had ALREADY escaped every such character on disk, so the reading cannot
distinguish a correct text edit from the round trip it was written to catch —
the §3 item 27 shape, a gate that discharges itself. The worker reported it as
vacuous and supplied three non-vacuous readings instead: 18 escape sequences
before and after, a file-size delta of exactly the four characters `F109`, and a
one-line committed diff. A gate whose discriminator is destroyed by the very
defect it sits next to needs re-deriving, not re-running.

The entry F108's closure round recorded on 2026-09-02 — `README.md` carries
F106's capability paragraph twice, the second copy misplaced under "Accepted
in Tier 5 so far" — was registered in F109 round 1 as finding `R-0769` in
`.agent/live_review.md`; the reason, the measurement and the routing are on
that record. The entry recorded after F106's closure (job/mission
resume-from-persisted-state, DECISION F106 D2) was registered in F108 round 1
as finding `R-0762` on the same record.
