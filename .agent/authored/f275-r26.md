STEP T001-close / F275 — ROUND 26 — THE SWEEP-FIRST ROUND: FINISH THE TWO PAGES, THEN CLOSE R-0843 AND R-0858

Goal: finish the two documents rounds 23 to 25 repaired in parts, by sweeping each
ENCLOSING UNIT for the concept before writing a single pair rather than after — which
is what R-0870's widened fix clause asks for and what three consecutive rounds of this
session did not do. Then close R-0843 and R-0858, whose subjects those sweeps complete,
and book the round 25 verdict.

WHY THIS ROUND EXISTS AND WHAT IT IS CORRECTING. Rounds 23, 24 and 25 each repaired a
region and each left the enclosing unit contradicting it: a docstring whose line 8
falsified its own line 4, a page whose Quick start was fixed while two bullets kept
promising the deleted mechanism, and a feature file whose DONE condition kept a numeral
the same round deleted from its Acceptance. Every one was found by the WORKER after the
fact. The reviewer has now swept both remaining files END TO END and the pairs below
are the whole result, stated as a measurement rather than as a hope: in
`docs/roadmap/features/T2_F267.md` the residues are at three places and nowhere else,
and in `docs/system/architecture.md` the enclosing section is historical throughout, so
it gets ONE banner at the section level rather than a pair per false sentence.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r26.md`
  C0b  mirror the COMMITTED C0a blob into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN26
  C2   the record: LEDGER26 appended to `.agent/live_review.md`, SLIPS26 appended to
       `.agent/prose_slips.md`
  C3   `docs/roadmap/features/T2_F267.md`: pairs U1, U2 and U3. The commit message
       NAMES R-0858.
  C4   `docs/system/architecture.md`: pairs U4 and U5. The commit message NAMES R-0843.
  C5   the handback

Change set — EXACTLY these paths, nothing else:
  .agent/authored/f275-r26.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  docs/roadmap/features/T2_F267.md
  docs/system/architecture.md
  .agent/handoff.md

Constraints:
 1. Every slice between a BEGIN and END marker is applied BYTE FOR BYTE. Do not
    reflow, re-wrap, re-indent or "fix" anything inside one. If a slice looks wrong,
    apply it anyway and declare it in the handback.
 2. Marker lines are never written into any target file.
 3. THE APPEND CONVENTION for `.agent/live_review.md` and `.agent/prose_slips.md`,
    verified by the reviewer against both at `684b1b55`: each ends with exactly ONE
    newline byte, and an append writes `pre + b"\n" + slice`, where the slice itself
    ends with one newline. At this base the ledger is 745098 bytes and the slips file
    is 209425 bytes. `.agent/decisions.md` is NOT in this round's change set.
 4. WITHIN a slice bound for either append target, records are separated from each
    other by a BLANK line.
 5. C2 is the FIRST substantive commit of this round, before C3 and C4.
 6. C3 follows C2. The `Done: R-0858` paragraph in LEDGER26 states that this round's
    C3 completes the repair; this constraint is what makes that sentence true, and it
    is named there rather than a SHA, per planner_reviewer_prompt.md §3 item 20 and
    finding R-0524, because the commit does not exist when the text is written.
 7. TWO COMMIT MESSAGES CARRY AN ID: C3 names R-0858 and C4 names R-0843. Commit
    subjects carry no leading-slash token and no absolute path, per AGENTS.md Commit
    Discipline.
 8. PAIR SHAPES, each classified by a containment test the reviewer RAN at `684b1b55`,
    one reading per pair, output recorded. ALL FIVE read `TO contains FROM: false` ->
    REWRITE, with the FROM occurring 1x in its target and the TO 0x before the edit, so
    every one gets the ordinary FROM-0x / TO-1x proof. U4 is the one that LOOKS
    append-shaped and is not: it inserts a banner between a heading and the paragraph
    under it, which splits the FROM's blank line from its second line, so the TO does
    not contain the FROM verbatim. That reading came from the test rather than from the
    eye, which is §3 item 15, and it is recorded here because the eye said APPEND.
 9. NOTHING under `packages/`, `apps/` or `tests/` is touched. This round changes two
    documents and the record, and no gate over the catalog or the suite can therefore
    move; G7 measures that rather than assuming it.
10. Destructive verification runs ONLY inside a disposable `git worktree`, never in the
    primary checkout. None is ordered this round.
11. Read `.agent/STOP` from disk before the first commit. If it exists, write the
    handback and stop.

Done when — G1 to G7 below have all been RUN, with their real exit codes recorded, and
the handback carries ONE line per gate. Every gate runs at or before C4.

G1 TRANSPORT. `sha256` of the committed `.agent/authored/f275-r26.md` blob at C0a equals
the digest the delegation names, and the committed `.agent/last_block.md` blob at C0b
equals the same digest. Report both. Per §3 item 37 this covers those two committed
artefacts and the reviewer's scratch original, and claims nothing about the bytes that
travelled into your prompt.

G2 THE PLAN. `.agent/plan.md` at C1 is byte-identical to PLAN26. Report its byte length
and line count, under the AGENTS.md cap of 50, and confirm `^## Goal$` and
`^## Next Steps$` each occur exactly once.

G3 THE RECORD, at C2, for `.agent/live_review.md` and `.agent/prose_slips.md`
separately. Reading (a), bytes: the committed post-blob equals the pre-blob, then one
newline, then the slice exactly as extracted; READ THE JOINING BYTE BACK from the post
blob at offset len(pre) and report it. Reading (b), structure: count N as the number of
blank-line-separated paragraphs IN THE SLICE with your own script — never from this
block — and compare the LAST N blank-line units of the whole post-file against those N
paragraphs IN ORDER. Negative control: flip one byte inside the FIRST appended paragraph
and confirm BOTH readers reject it while both accept the truth. Then report over the
whole post-file: `^Gate: F275 R25 ` exactly 1, `^Note: F275 R26 ` exactly 1,
`^Done: R-0843 — ` exactly 1, `^Done: R-0858 — ` exactly 1, and `^Done: R-0859 — `
still exactly 1. Finally report THE OPEN SET BY DISTINCT ID, every distinct id in a
`^- R-\d+ — ` paragraph minus every distinct id in a `^Done: R-\d+ — ` line. The
reviewer computed it at `684b1b55` as 90, over 100 distinct registrations against 10
distinct resolutions. It must read 88 at C2, because this commit registers nothing and
resolves two.

G4 THE FEATURE FILE, at C3, over `docs/roadmap/features/T2_F267.md`. For each of U1, U2
and U3 the FROM reads 0x and the TO reads 1x. Then SWEEP THE WHOLE FILE and report, with
line numbers, every occurrence of each of these: the digits `24`, the words `fifteen`,
`nine` and `four`, and each of the five ids `repair.item-list`, `builder.session-list`,
`execution.approval-list`, `external-builder.package-list` and
`self-repair.proposal-list`. The reviewer states the expectation in advance so you
reconcile against it rather than against an impossible zero, which is R-0869's clause.
`24`, `fifteen` and `nine` must reach ZERO. The five ids survive ONLY inside the
blockquote round 25 added, which names them on purpose. `four` survives at exactly four
places and every one of them is a sentence ABOUT the DECISION F262 D4 exclusions rather
than a live claim: F262's own dated measurement in "Why this exists", the correction
paragraph beneath it, the T002 sentence saying F275 deleted all four, and U3's own TO
saying the same in "Do not touch". Report any hit that falls outside that expectation —
that is the reading this gate exists to produce.

G5 THE ARCHITECTURE PAGE, at C4, over `docs/system/architecture.md`. For U4 and U5 the
FROM reads 0x and the TO reads 1x. Then report, with line numbers, every occurrence of
`12 groups` and of `twelve` in the whole file, together with the line number of the
`^## Group-first CLI v0 ` heading. The property is ORDERING, not absence: every
surviving occurrence must fall BENEATH that heading and its banner, inside the section
the banner dates, and none may fall outside it. The reviewer measured at `684b1b55`
that after this round the occurrences of `twelve` are inside the two banners themselves
and the occurrences of `12 groups` are in the section they date.

G6 THE BANNERS ARE WHERE A READER LANDS, at C4. Report the line number of
`^## Group-first CLI v0 ` and the line number of the FIRST `^> ` line after it, and
confirm they are adjacent but for one blank line — a banner a reader scrolls past is a
banner that does not bind. Report the same pair for `^### Groups`.

G7 NOTHING ELSE MOVED, at C4. Through the SHIPPED reader by importing
`apps.cli.command_catalog`: `len(_BASE_CATALOG)` is 222, `len(GROUPS)` is 44, and
resolving every `related=` tuple against the live id set gives ZERO dangling references
— all three UNCHANGED from `684b1b55`, which is what constraint 9 predicts for a round
that touches no code. Then:
  python3 -m pytest tests/docs/ tests/cli/test_product_spine.py -q
  python3 -m pytest tests/cli/test_golden_path.py -q
Report both real exit codes and real counts; `tests/docs/` is mandatory because this
change set contains a `docs/roadmap/**` path. Then: `.agent/STOP` does not exist;
`git status --porcelain` is EMPTY; `git worktree list` holds exactly ONE entry; the
branch is `feature/f275-one-world-completion-part-three`;
`git diff --name-only 684b1b55..C4` names EXACTLY the change-set paths above other than
`.agent/handoff.md`, reported as an exact set match with MISSING and EXTRA both printed
even when empty; and each commit's insertion count from `git show --numstat`, for every
commit before the handback commit, against the AGENTS.md DECISION F104 D1 cap of 500.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — the state
block with the SESSION NUMBER, the per-commit changed-files table with `+/-` cells
transcribed from `git show --numstat` and compared cell by cell against it, one line per
gate with its real exit code, every declared deviation, the item status table, and the
next expected action. There is no length cap. Then push.

<<<BEGIN PLAN26>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 26 finishes the two documents rounds 23 to 25 repaired in parts, by sweeping each
enclosing unit for the concept BEFORE writing a pair rather than after. `T2_F267.md` loses
the three numerals and the dead cross-reference its earlier repair left standing, and the
historical `Group-first CLI v0` section of `architecture.md` gets one banner at the section
level instead of a pair per false sentence. R-0843 and R-0858 close on those sweeps.

## Next Steps

1. T002: the DECISION F272 D7 raising-property probe over every candidate `.id` receiver,
   giving the real site set rather than D15's upper bound, then the dated decision choosing
   the route. No production line moves in that slice, and it wants a fresh session.
2. T003, the classic runner, which T002's ruling is the prerequisite for.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   STATUS line and the PR.

## Risks

- The open set is 90 by distinct id at this round's base `684b1b55`, computed mechanically
  from the record. This round registers nothing and resolves two, leaving 88. Four are High
  — R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- R-0870's class has recurred in every round of this session, always as a region repaired
  while its enclosing unit kept contradicting it. This round is the counter-measure applied
  to itself; if it recurs again the clause is not working and the next session should say so
  rather than write a fourth instance.
- T001's remaining work is documentary only. Every module F260's Design lists is gone, the
  deletion paragraph is recorded, and the scaffolding is retired.
<<<END PLAN26>>>

<<<BEGIN LEDGER26>>>
Gate: F275 R25 — the F275 round 25 entry. VERDICT PASS, written by the planner and reviewer of session 13 after reading the committed range `06dbb1c6`..`684b1b55` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was not evidence for any line here. Booked by round 26's C2 from the pushed handback, under amend0827-process-diet rule 1. NINE single-parent commits C0a `3777e3f1`, C0b `2b31cea4`, C1 `062c8945`, C2 `a8ee2c41`, C3 `e833cf8a`, C4 `4a54dded`, C5 `5ffe7c46`, C6 `9cf79a08` and C7 `684b1b55`, per-commit insertions 468, 388, 20, 16, 44, 0, 0 and 42 for the eight before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500 — and the two ZEROES are the point of the round, being the deletion commit and the residue-sweep commit. G1 TRANSPORT covers the chain this workflow can walk and NOT the emitted bytes, per §3 item 37: the reviewer's scratch original, the committed `.agent/authored/f275-r25.md` and the committed `.agent/last_block.md` are all 40290 bytes at `0fb0e9084d7436d84afab34d57dc35f998d895066fd8ff20c2d020ebf4afb34c` and compare BYTE-EQUAL. G2: `.agent/plan.md` at C1 is 2180 bytes byte-identical to PLAN25, 41 lines against the cap of 50. G3 AND G4 HELD OVER THREE APPENDS, each re-run by the reviewer: `.agent/live_review.md` 732715 to 745098, `.agent/prose_slips.md` 207261 to 209425 and `.agent/decisions.md` 1009356 to 1012375, every post-blob equal to its pre-blob then ONE newline then the slice exactly as extracted, the joining byte READ BACK at offset len(pre) and reading `b'\n'` in all three, and the structural reader counting N from each slice — 5, 3 and 7 paragraphs — and matching the last N blank-line units IN ORDER. The reviewer ran its own negative control on the FIRST appended paragraph of the SLIPS slice this time, so across rounds 23 to 25 the control has now been placed on all three record files: byte reader rejects, structural reader rejects, both accept the truth, later paragraphs provably untouched. `^Gate: F275 R24 `, `^Done: R-0859 — `, `^Done: R-0871 — `, `^Done: R-0864 — `, `^Landed: R-0862 ` and `^## DECISION F275 D15 ` each read exactly 1, and `^Note: F275 R25 ` reads exactly 2. THE OPEN SET FELL 92 TO 90 BY DISTINCT ID, over 100 registrations against 10 resolutions, correct for a round registering nothing and resolving two. G5 THE RETIREMENT IS COMPLETE AND THE SWEEP IS SPLIT AS R-0869 REQUIRES: all four scaffolding paths resolve at the base and NONE resolves at C4, the HARD ZERO half reads ZERO for `cluster_deletion_map`, `cluster_deletion_order` and `f275_deletion_order` over the 1649 tracked files outside `.agent/`, `.data/` and `docs/roadmap/`, and the RAW half is exactly six hits in `T2_F274.md` and `T2_F275.md`, which are history prose and stay. `tests/orchestration/` is green and the collected count falls by EXACTLY SIX, which is the two retired ratchets' own tests and nothing else. G6: the vacant `dogfood` banner is gone, the anchor line above it still reads once, exactly three `self-repair` lines remain on the operator page and all three are inside the section round 24 rewrote to say the mechanism is gone, and through the SHIPPED reader the catalog is unchanged at 222 commands and 44 groups with ZERO dangling `related=` references. G7: all seven feature-file and architecture pairs applied, the five deleted ids occur ONLY inside the blockquote round 25 added, the four survivors are all present, and `tests/docs/` is green at 303 passed. G8: 12216 passed and 10 skipped across the named suites and the canary 42 passed, both re-run by the reviewer in the PRIMARY checkout; no `.agent/STOP`, porcelain EMPTY, ONE worktree, the branch correct, and `06dbb1c6..9cf79a08` an EXACT set match over the fourteen change-set paths with MISSING and EXTRA both empty and all four retired paths carrying status `D`. THE TWO DECLARED DEVIATIONS ARE SUSTAINED and neither is a worker error: no worktree was created because no destructive check was ordered, and the three factual asides inside the authored slices were re-measured by the worker and hold. THE TWO FINDINGS THE WORKER RAISED THAT THE BLOCK DID NOT NAME ARE BOTH REAL and the reviewer measured each at `684b1b55`; they are folded into R-0870 by the `Note: F275 R26` entry below rather than given ids, and they are what the round 26 block exists to repair.

Note: F275 R26 — new evidence for the OPEN finding R-0870, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30, and recorded with the pattern it completes rather than as two more instances. R-0870 records prose falsified by a deletion that no gate can see, and its fix clause — widened one round earlier to demand a pair authored against the WHOLE enclosing unit — has now failed to bind in three consecutive rounds of one session, each time in a file the failing round's own change set named. THE SEVENTH AND EIGHTH INSTANCES, measured by the reviewer at `684b1b55`. FIRST, `docs/roadmap/features/T2_F267.md` line 28 still reads "all 24 in-scope commands" in its DONE condition — the same numeral round 25 deleted from that file's Acceptance section four lines of prose away, left standing because the pair's FROM stopped one line short of it; line 54 keeps "the fifteen landed wirings" and lines 90 to 91 keep "the four D4 exclusions" with a pointer to `approval.policy-list`, a command F275 deleted. SECOND, `docs/system/architecture.md` states "one of 12 groups" at line 2917 and "Root help shows only the 12 groups" at line 2961, both outside the banner round 25 added over the `### Groups` table and both false against a catalog of 44 groups; the same section's `action_class` list omits `local_state_change`, which the shipped catalog uses. WHY THIS IS ONE NOTE AND NOT TWO IDS: R-0870 is OPEN and both are its subject exactly, and both are Low for the reason its other instances are — nothing executes any of these lines. THE LESSON THE CLAUSE WAS MISSING, and it is the reason three rounds reproduced the class under a rule written to stop it: the clause said WHAT to sweep and not WHEN, so every round swept after authoring its pairs and found the residue in the worker's report instead of in its own. The round 26 block states the sweep as the FIRST act of authoring and carries its result as the pairs' justification, and where the enclosing unit is historical throughout it takes ONE banner at the section level rather than a pair per false sentence — because a page that needs five pairs is a page that should have been dated instead.

Done: R-0843 — Resolved by F275 round 25's C6 `9cf79a08` and completed by this round's C4, which constraint 6 of the round 26 block orders after this commit. The finding recorded that the `Groups` table in `docs/system/architecture.md` still advertised the deleted `context.pack` command as the `context` group's purpose, and its fix clause was explicit that the instance-fix was forbidden: repair the WHOLE table, or give the section a status banner naming it a historical snapshot, because fixing the one row is the staleness shape the checklist exists to prevent. THE BANNER ROUTE WAS TAKEN AND THE MEASUREMENT BEHIND IT IS ON THE RECORD: the reviewer read every row of that table through the shipped catalog at `06dbb1c6` and only three of the twelve — `readiness`, `context` and `file` — still state a command count the catalog agrees with, against a live surface of 222 commands in 44 groups. Repairing the table row by row would have produced a hand-written mirror of the catalog that drifts again after the next feature to add or delete a command, which is why the clause offered the banner as an equal option rather than a lesser one. WHAT THIS ROUND ADDS, and why the resolution names two commits: the banner round 25 wrote covers the TABLE, and the reviewer then measured that the enclosing section states the same false thing twice more outside it, so C4 moves the historical declaration up to the section heading where a reader lands. The `context.pack` row itself is untouched and stays as the record of what shipped at that step; git is the archive and the banner is the pointer.

Done: R-0858 — Resolved by F275 round 25's C6 `9cf79a08` and completed by this round's C3, which constraint 6 of the round 26 block orders after this commit. The finding recorded that `docs/roadmap/features/T2_F267.md`, an UNSTARTED feature Rule A5 will one day propose, planned a scope that named commands this feature deleted, so the session claiming it would plan against commands that cannot exist. THE REPAIR IS WIDER THAN THE FINDING'S OWN PROPOSAL, and deliberately so: R-0858 proposed striking one id and restating a count as EIGHT, and the reviewer re-measured at `6f865e50` through the SHIPPED catalog that FIVE of the nine were gone and ALL FOUR of the DECISION F262 D4 exclusions with them, so the proposed numeral was itself wrong by four. That re-measurement is the `Note: F275 R23` entry on this record. What landed instead: the five deleted ids are struck from the scope list and preserved in a dated blockquote that names this id and this feature, every numeral that counted a scope the catalog has changed is DELETED rather than re-synchronised per §3 item 16, the F262 measurement paragraph is kept and explicitly dated as history, and this round's C3 finishes the three residues the first pass left — the DONE condition's own count, the Design bullet's count of F262's landed wirings, and the "Do not touch" clause pointing at a deleted command. THE PROPERTY THAT MATTERS is not that the file is now correct about the catalog, which no file can stay: it is that the file no longer asserts a scope, and instead tells the session that claims it to re-derive the in-scope set from `apps/cli/command_catalog.py` through the shipped reader. A plan that names its source outlives the thing it planned against.
<<<END LEDGER26>>>

<<<BEGIN SLIPS26>>>
2026-09-10 · F275 R25 · The round 25 block's S2 pair rewrote the F267 scope list and its DONE sentence, and its FROM ended one line above the clause reading "all 24 in-scope commands" — so the same round that added a blockquote declaring those numerals deleted left one of them four lines below the blockquote, and the same round's S6 deleted the identical numeral from the Acceptance section. The worker measured it and said so. The lesson is that when a pair's justification is "this numeral is being removed", the sweep for that numeral runs over the WHOLE file before the FROM's boundaries are chosen, because a boundary drawn around the sentence the author was reading is exactly how a second copy survives.

2026-09-10 · F275 R25 · The round 25 block's S7 pair bannered the `### Groups` subsection of `docs/system/architecture.md` while the enclosing `## Group-first CLI v0 (Steps 38–40)` section states the same false thing twice more outside it — "one of 12 groups" and "Root help shows only the 12 groups" — against a live catalog of 44. R-0843's clause offered the banner as an alternative to repairing the whole table, and the reviewer took it at the granularity of the TABLE rather than of the historical unit. The lesson is that a status banner is placed at the outermost heading every false sentence beneath it shares a cause with, because a banner that covers one table while its own section keeps contradicting the catalog is an instance-fix wearing a banner's clothes.

2026-09-10 · F275 R23-R25 · Every round of session 13 reproduced the same class — a region repaired while its enclosing unit kept contradicting it — and every one was found by the WORKER after the round rather than by the reviewer before it, across four files and three different documents. The fix clause was widened after the second and the class recurred in the third under the widened wording. The lesson is not another widening: it is that the sweep belongs at the START of authoring, as the act that PRODUCES the pairs, and that a reviewer who writes the pairs first and sweeps afterwards is measuring its own work with the tool that was supposed to plan it.
<<<END SLIPS26>>>

U1 — docs/roadmap/features/T2_F267.md — REWRITE — the DONE condition's count
<<<BEGIN U1 FROM>>>
DONE when every one of them exits non-zero on `--sort bogus` naming its
valid fields, `--limit`/`--since`/`--until` filter its real rows, the
catalog-driven handler test is green over all 24 in-scope commands, and the
ten-second demo is a test, not a claim.
<<<END U1 FROM>>>
<<<BEGIN U1 TO>>>
DONE when every one of them exits non-zero on `--sort bogus` naming its
valid fields, `--limit`/`--since`/`--until` filter its real rows, the
catalog-driven handler test is green over every in-scope command the catalog
holds when that test is written, and the ten-second demo is a test, not a
claim.
<<<END U1 TO>>>

U2 — docs/roadmap/features/T2_F267.md — REWRITE — the Design bullet's count
<<<BEGIN U2 FROM>>>
- Reuse, never re-implement: every wiring is one `apply_list_options` call over
  the handler's already-built row list, with `sort_fields` naming that
  command's own columns and `default_sort_field` naming its genuine date
  (`created_at`, `started_at`, `timestamp`, ...), the same shape as the
  fifteen landed wirings (`apps/cli/commands/job.py` is the reference).
<<<END U2 FROM>>>
<<<BEGIN U2 TO>>>
- Reuse, never re-implement: every wiring is one `apply_list_options` call over
  the handler's already-built row list, with `sort_fields` naming that
  command's own columns and `default_sort_field` naming its genuine date
  (`created_at`, `started_at`, `timestamp`, ...), the same shape as the
  wirings F262 landed (`apps/cli/commands/job.py` is the reference).
<<<END U2 TO>>>

U3 — docs/roadmap/features/T2_F267.md — REWRITE — the Do-not-touch cross-reference
<<<BEGIN U3 FROM>>>
The stores' own schemas beyond adding a missing timestamp, the `--json`
contract's existing keys, and the four D4 exclusions — a feature adding
genuine per-policy history would revisit `approval.policy-list`, not this one.
<<<END U3 FROM>>>
<<<BEGIN U3 TO>>>
The stores' own schemas beyond adding a missing timestamp and the `--json`
contract's existing keys. The DECISION F262 D4 exclusions used to be named
here too, with `approval.policy-list` as the example of a list a feature adding
genuine per-policy history would revisit; F275 deleted all four of them, so
there is nothing left here to leave alone. Remedy deliberately ships no
list-option wiring for those commands because the commands themselves are gone
— see finding R-0858 and the blockquote in Goal & Done.
<<<END U3 TO>>>

U4 — docs/system/architecture.md — APPEND — the section-level historical banner
<<<BEGIN U4 FROM>>>
## Group-first CLI v0 (Steps 38–40)

Steps 38–40 restructure the Remedy CLI from flat commands (`remedy create-job`, `remedy brain`) to a group-first layout (`remedy job create`, `remedy brain graph`).
<<<END U4 FROM>>>
<<<BEGIN U4 TO>>>
## Group-first CLI v0 (Steps 38–40)

> **Status (2026-09-10): HISTORICAL SNAPSHOT, finding R-0843.** This whole section
> records the CLI as it shipped at Steps 38 to 43. The group-first STRUCTURE it
> describes is still how the CLI works and is still accurate; every COUNT and every
> ENUMERATION in it is not. Measured through the shipped reader at `684b1b55`: the
> catalog holds 222 commands in 44 groups, so the twelve groups listed below are 12
> of 44; and the `action_class` list below omits `local_state_change`, which the
> catalog uses. Read `apps/cli/command_catalog.py`, or run `remedy list`, for what
> ships today. The section is dated rather than repaired sentence by sentence,
> because a hand-written mirror of the catalog drifts again after the next feature
> that adds or deletes a command.

Steps 38–40 restructure the Remedy CLI from flat commands (`remedy create-job`, `remedy brain`) to a group-first layout (`remedy job create`, `remedy brain graph`).
<<<END U4 TO>>>

U5 — docs/system/architecture.md — REWRITE — the table banner becomes a pointer
<<<BEGIN U5 FROM>>>
> **Status (2026-09-10): HISTORICAL SNAPSHOT, finding R-0843.** The table below
> records the groups the grouped CLI shipped with at the step that introduced
> it. Measured through the shipped reader at `06dbb1c6`: the catalog holds 222
> commands in 44 groups, and only three of the twelve rows below still state a
> command count the catalog agrees with. It is kept as the record of that step
> rather than repaired row by row, because a hand-written mirror of the catalog
> drifts by construction and would need repairing again after every feature
> that adds or deletes a command. Read `apps/cli/command_catalog.py`, or run
> `remedy list`, for what ships today.
<<<END U5 FROM>>>
<<<BEGIN U5 TO>>>
> **Historical, under the banner at the top of this section.** Measured through
> the shipped reader at `06dbb1c6`, only three of the twelve rows below still
> state a command count the catalog agrees with: `readiness`, `context` and
> `file`. The table is kept as the record of what shipped at that step.
<<<END U5 TO>>>
