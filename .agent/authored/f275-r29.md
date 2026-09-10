── STEP T001 (documentary remainder) — F275 — ROUND 29 ──
(The rule line above and the one at the end are each exactly 56 characters, per §3 item 37.)

Goal: Finish R-0872 by making every command example in `docs/system/architecture.md`
name the command that actually ships, and delete the ratchet that has been holding
the backlog. Steps 38-40 renamed the whole CLI from flat commands to a group-first
layout; `architecture.md` was never followed through, so its command examples still
spell the pre-Step-38 form. They are not dated history — they sit in
present-tense instructions like "**Attaching a repo** stores the resolved absolute
path", so a reader following one gets exit 2. Each has an exact group-first
successor in the shipped catalog, which is why this round is a rename rather than
a deletion.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r29.md`
  C0b  mirror the COMMITTED C0a blob into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN29
  C2   the record: LEDGER29 into `.agent/live_review.md`
  C3   the rename table over `docs/system/architecture.md`, plus pairs V1 and V2
  C4   delete the ratchet machinery from the guard
  C5   the handback

Change set — exactly these paths, nothing else:
  .agent/authored/f275-r29.md            (C0a, new file)
  .agent/last_block.md                   (C0b)
  .agent/plan.md                         (C1)
  .agent/live_review.md                  (C2, append)
  docs/system/architecture.md            (C3)
  docs/system/vocabulary.md              (C3)
  tests/cli/test_advertised_commands.py  (C4)
  .agent/handoff.md                      (C5)

`.agent/prose_slips.md` is NOT in this change set. Round 28's worker declared no
doubt about the round 28 block and every numeral it predicted reproduced on
measurement, so this round has no reviewer-prose inaccuracy to record and does not
manufacture one.

Constraints:
 1. Every slice is applied BYTE FOR BYTE. If a slice looks wrong, apply it anyway
    and DECLARE the doubt in the handback. Never repair a reviewer slice.
 2. Marker lines never reach a target file. Extract slices from the COMMITTED C0a
    blob, never from a retype.
 3. PAIR SHAPES, from the reviewer's own containment test, one reading per pair —
    `TO contains FROM: false` for V1 and V2. Both are REWRITES, so each gets the
    FROM 1x -> 0x and TO 0x -> 1x proof, measured before and after the write.
 4. THE RENAME TABLE IS APPLIED AS A MEASURED TRANSFORMATION, NOT AS 37 PAIRS.
    Apply the mappings in DESCENDING ORDER OF FROM LENGTH, so that no mapping can
    consume a prefix of a longer one — `remedy attach-repo` must not fire inside
    `remedy attach-project-repo`. Each FROM matches only when NOT followed by
    another command character, i.e. the regex `re.escape(FROM) + r"(?![a-z0-9-])"`.
    Report the count each mapping replaced and prove each one reaches ZERO after.
 5. V1 IS APPLIED FIRST, BEFORE THE RENAME TABLE, AND THIS ORDERING IS LOAD-BEARING.
    The sentence V1 rewrites is the one that EXPLAINS the restructure by quoting the
    old spelling; if the table ran first it would rewrite that quotation into the new
    spelling and the sentence would claim the restructure changed nothing. V1's TO
    removes the `remedy ` prefix from the two quoted flat commands, so the table then
    cannot match them and no exclusion list is needed.
 6. `.agent/STOP` is re-read FROM DISK before the FIRST commit and again before C4.
 7. RUFF IS A GATE OF ITS OWN AT C4 AND IS NOT OPTIONAL, because the suite CANNOT
    see this round's most likely defect. The reviewer hit it in the dry run: after
    the allowlist is deleted, a surviving reference to it inside a list comprehension
    over an EMPTY list is never evaluated, so `pytest` reported 5 passed while
    `tests/cli/test_advertised_commands.py` still named an undefined
    `KNOWN_DEAD_DOC_ADVERTISEMENTS`. A green suite is not evidence that the removal
    was complete; `ruff check` reading `F821` is what catches it.
 8. No file outside the change set is edited, and no test is deleted, skipped or
    weakened to make a gate green — with the one exception this round exists to
    make, C4's removal of the ratchet, which is ordered below and gated by G6.
 9. Commit subjects carry NO leading-slash token or absolute path. C3's and C4's
    subjects name R-0872.
10. Do not re-verify rounds 27 and 28; both were measured and both hold.

──────── WHAT THE REVIEWER ALREADY MEASURED, by APPLYING all of it ────────

Applied in a disposable worktree at `99e677f0` and RUN. These are the numbers the
gates re-derive, not predictions. The rename table replaced 37 OCCURRENCES across
`architecture.md` and every mapping reached zero. That is one MORE than the sites
the sweep flagged there, and the difference is stated rather than smoothed over:
36 of the 37 are flagged sites, V1 carries the 37th flagged site, and the extra
occurrence is `remedy list-projects` at line 1897, which the sweep never flagged
because an EM DASH follows it and the tail rule reads that as prose. It is repaired
anyway, because it is as dead as the ones the sweep could see. So `architecture.md`
holds 37 flagged sites and `vocabulary.md` one, which is the 38 the sweep reports.
The operator-facing sweep falls from 387 seen / 38 unresolved to 384 seen and ZERO
unresolved, and the production sweep is UNCHANGED at 542 / 0. With the ratchet
deleted the guard file runs 5 passed rather than 6, because the ratchet test is one
of the tests removed. `ruff check` is clean on the guard. `tests/docs/ tests/cli/`
is green at 1648 passed, one fewer than round 28's 1649, and that difference is
exactly the deleted ratchet test. The diff is 41 insertions against 115 deletions
over three files.

RED PROOF ALREADY TAKEN, and G6 re-takes it: with the allowlist gone, restoring
`remedy absorb` into `vocabulary.md` turns
`test_every_operator_facing_advertised_command_exists_in_the_catalog` RED at 1
failed / 4 passed. The guard did not lose its teeth when it lost its allowlist.

──────── V1 — the sentence that explains the restructure ────────

Applied BEFORE the rename table, per constraint 5.

<<<BEGIN V1 FROM>>>
Steps 38–40 restructure the Remedy CLI from flat commands (`remedy create-job`, `remedy brain`) to a group-first layout (`remedy job create`, `remedy brain graph`).
<<<END V1 FROM>>>

<<<BEGIN V1 TO>>>
Steps 38–40 restructure the Remedy CLI from flat commands, spelled `create-job` and `brain`, to a group-first layout: `remedy job create`, `remedy brain graph`. The flat spellings are shown without the `remedy` prefix because they no longer run.
<<<END V1 TO>>>

──────── V2 — the vocabulary decision's forward-looking command ────────

`docs/system/vocabulary.md` line 264 sits inside DECISION F259 D1 and names a
command F263 WILL ship. It is not a dead advertisement and the DECISION's content
is not changed: the chosen name stays `absorb`. Only the spelling that reads as a
runnable invocation goes, because the sweep cannot distinguish a planned command
from a deleted one and a permanent one-entry allowlist is worse than a rewording.

<<<BEGIN V2 FROM>>>
F263 ships `remedy absorb`; T2_F263.md carries the final name.
<<<END V2 FROM>>>

<<<BEGIN V2 TO>>>
F263 ships the command named `absorb`; T2_F263.md carries the final name.
<<<END V2 TO>>>

──────── The rename table, applied per constraint 4 ────────

FROM -> TO, with the count the reviewer measured at `99e677f0` in brackets. Apply
longest FROM first. Every count is a reading, not a target: report what you measure
and STOP if any mapping's post-count is not zero.

  remedy attach-project-repo  -> remedy project attach-repo   [1]
  remedy list-patch-intents   -> remedy patch list            [1]
  remedy apply-patch-intent   -> remedy patch apply           [2]
  remedy attach-project-job   -> remedy project attach-job    [1]
  remedy discover-commands    -> remedy test discover         [2]
  remedy show-permissions     -> remedy job permissions       [1]
  remedy project-context      -> remedy project context       [3]
  remedy run-tests-local      -> remedy test run              [1]
  remedy create-project       -> remedy project create        [1]
  remedy list-projects        -> remedy project list          [1]
  remedy trust-report         -> remedy brain trust           [1]
  remedy constitution         -> remedy brain constitution    [2]
  remedy show-project         -> remedy project show          [2]
  remedy run-contract         -> remedy policy contract       [2]
  remedy token-policy         -> remedy policy token          [2]
  remedy attach-repo          -> remedy job attach-repo       [1]
  remedy brain-node           -> remedy brain node            [7]
  remedy brain-view           -> remedy brain view            [1]
  remedy create-job           -> remedy job create            [1]
  remedy timeline             -> remedy brain timeline        [1]
  remedy cockpit              -> remedy brain cockpit         [1]
  remedy workers              -> remedy worker list           [2]

EVERY TO ON THAT LIST WAS RESOLVED AGAINST THE SHIPPED CATALOG by the reviewer at
`99e677f0`, not guessed from the name: each `(group, subcommand)` pair is in
`CATALOG`. `remedy brain trust` is the successor of `remedy trust-report` because
`apps/cli/commands/brain.py` dispatches `brain.trust` to `_cmd_trust_report`, which
calls `summarize_trust_report` — the same function the flat command called. The
handback reports, through the SHIPPED catalog, that all 22 TO pairs resolve.

──────── The ratchet removal at C4 ────────

Delete, from `tests/cli/test_advertised_commands.py`, all four of:
  (a) `KNOWN_DEAD_DOC_ADVERTISEMENTS` and the comment block above it;
  (b) `_ALLOWLIST_CEILING` and its comment;
  (c) `test_the_known_dead_doc_advertisement_list_only_ever_shrinks` entirely;
  (d) the subtraction inside
      `test_every_operator_facing_advertised_command_exists_in_the_catalog` — the
      local list built from `unresolved` by filtering on the allowlist — so that
      the assertion reads directly against `unresolved`, exactly as the PRODUCTION
      sweep's assertion already does.
Nothing else in the module changes: the scanner, the tail rule, `_resolves`, both
corpora and the three scanner unit tests are untouched. After the removal the
module must contain ZERO occurrences of `KNOWN_DEAD_DOC_ADVERTISEMENTS`,
`_ALLOWLIST_CEILING` and `only_ever_shrinks` — item (d) is in this list precisely
because the reviewer's dry run left it behind and the SUITE did not notice.

──────── PLAN29 — the whole of `.agent/plan.md` ────────

<<<BEGIN PLAN29>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 29 finishes R-0872. `architecture.md` gets the flat-to-group-first rename that Steps
38 to 40 performed on the CLI and never on the docs, every mapping resolved against the
shipped catalog rather than guessed; `vocabulary.md` stops spelling
F263's planned command as a runnable one. The R-0872 ratchet then falls to zero and is
deleted with its ceiling and its test, because a ratchet at zero is a gate that cannot fail.

## Next Steps

1. R-0873's ruling, which round 29 names as declined rather than performed: read the
   capability sweep's eighteen pages one by one and rule each DELETE, DATE or LEAVE,
   recording the ruling as a dated DECISION. `docs/archive/` is archival by design and is
   expected to survive it.
2. T002: the DECISION F272 D7 raising-property probe over every candidate `.id` receiver,
   giving the real site set rather than D15's upper bound, then the dated decision choosing
   the route. No production line moves in that slice.
3. T003, the classic runner, which T002's ruling is the prerequisite for.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   STATUS line and the PR.

## Risks

- The open set is 89 by distinct id at this round's base `99e677f0`, computed mechanically
  from the record. This round registers none and resolves one, leaving 88. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- Deleting the ratchet removes the only mechanism that was counting the doc backlog. What
  replaces it is a guard with no exceptions at all, which is stronger — but it means the
  R-0873 residue is now carried by that finding alone, and nothing on disk counts it.
<<<END PLAN29>>>

──────── LEDGER29 — appended to `.agent/live_review.md` ────────

Two paragraphs, blank-line separated.

<<<BEGIN LEDGER29>>>
Gate: F275 R28 — the F275 round 28 entry. VERDICT PASS, written by the planner and reviewer of session 14 after reading the committed range `d3e35f0f`..`99e677f0` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs, and booked here by round 29 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1. Seven single-parent commits C0a `47400579`, C0b `1ec9489b`, C1 `7769c74a`, C2 `39d85f72`, C3 `43374b84`, C4 `7cfd213e` and C5 `99e677f0`, per-commit insertions 316, 253, 17, 8, 1, 1 and the handback's own, every one far under the AGENTS.md DECISION F104 D1 cap of 500 — C3 and C4 are ONE insertion each because a deletion round's diff is almost entirely the minus column. G1: scratch original and both committed copies 28018 bytes at `05026d2071b930534091721ea51244a9811f75537e53daa526011fa0485cf706`, BYTE-EQUAL. G2: `.agent/plan.md` byte-identical to PLAN28 at 2519 bytes, 45 lines against the cap of 50. G3: `.agent/live_review.md` 767596 to 775926 and `.agent/prose_slips.md` 213983 to 215418, each post-blob equal to pre plus ONE newline plus the slice, the joining byte READ BACK as a newline in both, the structural reader counting N=2 from each slice and matching in order, and both negative controls flipped inside the FIRST appended paragraph and REJECTED by BOTH readers. THE OPEN SET ROSE 88 TO 89 BY DISTINCT ID over 102 registrations against 13 resolutions, correct for a round that registers one and resolves none. G4: all five pages PRESENT at `d3e35f0f` and ABSENT at C3 — the presence reading is taken as well as the absence, because an absence proves nothing without it — and a repo-wide basename sweep over `docs tests scripts packages apps` finds ZERO surviving mentions; `docs/README.md` falls 204 to 198 lines, losing exactly the six rows the block named, each 1 before and 0 after. G5 THE RATCHET WORKED TWICE IN ONE ROUND, which is the round's real evidence: at C3 the allowlist and its ceiling both read 27 with zero stale entries, at C4 both read 22 with zero stale, and the C4 digest is `7a6b5f4fa5b0ff693acff44b3c181f0b36df05b098d61c08641fb575c96d41d2` exactly as ordered; the operator-facing sweep falls to 387 seen, 38 unresolved and 22 distinct keys over exactly TWO paths, and the production sweep is UNCHANGED at 542 and ZERO. G6: the spine page's dead section and its taxonomy row each 1 to 0, `self-repair` ZERO over the whole page, the page still present at 132 lines, and `tests/docs/ tests/cli/` green at 1649 passed run SERIALLY. G7: the shipped catalog unchanged at 222 commands, 44 groups and ZERO dangling `related=` references over 286, no `.agent/STOP`, porcelain EMPTY, ONE worktree, and `d3e35f0f..7cfd213e` an EXACT set match over thirteen paths with MISSING and EXTRA both empty. THREE DECLARATIONS FROM THE WORKER ARE SUSTAINED AND TWO OF THEM ARE WORTH THE RECORD. FIRST, the worker's own first `related=` reader split references on whitespace and reported 286 dangling — a false alarm on every reference, because `related=` holds DOTTED catalog ids and not spaced pairs — and it declared the wrong reading BECAUSE IT HAD BEEN RUN rather than quietly replacing it. That is the R-0859 pattern arriving through the reader instead of through the data: nothing in this repository resolves `related=`, so every deletion round hand-rolls the check and can pick the wrong key shape. SECOND, the worker strengthened G7's word "unchanged" on its own initiative, observing that a reading at C4 alone shows a VALUE and not an INVARIANCE, and added that the range contains no `apps/` or `packages/` path at all and that `command_catalog.py` is byte-identical base to C4. THIRD, carried forward deliberately and not repaired: the spine page's command-taxonomy table still lists `dogfood create/step/show/stop/replay` and `self inspect/plan/propose/reconcile`, which carry no `remedy ` prefix and are therefore invisible to every advertisement scanner in this repository, while `dogfood` names the very mechanism whose user guide C3 deleted. The reviewer re-measured that at `99e677f0` and confirms both rows stand at lines 108 and 109. They are R-0873's, and R-0873's fix clause reaches them.

Done: R-0872 — RESOLVED at F275 round 29, by the commit constraint 4 of that round's block orders; the readings below are the reviewer's own, taken by APPLYING the change in a disposable worktree at `99e677f0` before the round was delegated. THE FINDING'S FIX CLAUSE HAD TWO HALVES AND BOTH ARE DISCHARGED. The first, "delete the four dying pages and repair `core-product-spine-v0.md`, lowering the allowlist to 22", was done by round 28's C3 and C4 — five pages in the end rather than four, because the reviewer found a fifth, `run-replay-to-self-repair-proposal-v0.md`, that carries no advertisement at all and was invisible to the sweep that raised this finding. The second, "repair `architecture.md` and `vocabulary.md`, lowering it to ZERO, and DELETE `KNOWN_DEAD_DOC_ADVERTISEMENTS`, `_ALLOWLIST_CEILING` and the ratchet test in that same commit", is this round. WHAT THE REPAIR ACTUALLY WAS, and it is not what the finding assumed: `architecture.md`'s 37 dead command examples were not residue of F275's deletions at all. They are the pre-Step-38 FLAT CLI, which the group-first restructure of Steps 38 to 40 replaced in the product and never in this page, so every one of them has an exact successor that ships today and the repair is a RENAME rather than a deletion — `remedy brain-node` to `remedy brain node` at seven sites, `remedy project-context` to `remedy project context` at three, and twenty other mappings, all 22 TO pairs resolved against the shipped `CATALOG` rather than inferred from their names. TWO SITES WERE NOT RENAMED AND BOTH ARE STATED, because renaming either would have made a true sentence false. The sentence introducing the restructure QUOTES the old spelling to say it is gone; renaming it would have made it claim the restructure changed nothing, so its TO drops the `remedy` prefix from the quotation instead and says why in the page. And `vocabulary.md` line 264 names `absorb`, a command F263 WILL ship, inside DECISION F259 D1; the DECISION's chosen name is untouched and only the runnable spelling goes, because a sweep cannot tell a planned command from a deleted one and a permanent one-entry allowlist is worse than a rewording. THE MEASUREMENT: the operator-facing corpus falls from 387 seen with 38 unresolved to 384 seen with ZERO unresolved, the production corpus is unchanged at 542 with ZERO, and the ratchet is gone — allowlist, ceiling, test and the subtraction inside the operator-facing assertion, which now reads against `unresolved` directly exactly as the production assertion always has. THE GUARD DID NOT LOSE ITS TEETH WITH ITS ALLOWLIST, and that was proved rather than assumed: restoring `remedy absorb` into `vocabulary.md` with the allowlist gone turns the operator-facing test RED. ONE THING THIS RESOLUTION DOES NOT CLAIM. R-0873's fix clause binds "the round that finishes R-0872" to rule the eighteen pages of the capability sweep page by page, and THIS ROUND DECLINES IT, explicitly and with its reason, per `docs/agents/planner_reviewer_prompt.md` §3 item 34: that ruling needs a per-page reading of eighteen documents and a dated DECISION, it shares no file with this round's change set, and folding it in would put a rename table and eighteen editorial judgements in one reviewable commit. It is named as the next round's whole subject in `.agent/plan.md`, which is where a declined clause has to land if it is to bind anything. R-0873 stays OPEN and nothing on disk now counts its backlog, which the plan's Risks section states in as many words.
<<<END LEDGER29>>>

Done when — the gates below, G1 to G7, inside the amend0827 rule 5 budget of
eight. Each is run with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, with real exit
codes and real numbers in the handback, ONE LINE PER GATE. G1 to G6 are ordered at
commits strictly before C5, per §3 item 31.

G1 TRANSPORT (at C0b). `sha256sum` of the scratch original at
   `.remedy-wt/f275-r29-block.md`, of the committed `.agent/authored/f275-r29.md`
   and of the committed `.agent/last_block.md` are ONE comparison and must be equal.
   State that this covers the scratch original, the saved copy and the mirror.

G2 THE PLAN (at C1). `.agent/plan.md` byte-identical to PLAN29; report
   `written == slice`. Line count under the AGENTS.md cap of 50. `^## Goal$` and
   `^## Next Steps$` each exactly 1.

G3 THE RECORD (at C2), full byte forensics. `.agent/live_review.md` is 775926 bytes
   before: post == pre + ONE newline + slice, joining byte READ BACK at offset
   len(pre) and shown to be a newline; plus an INDEPENDENT structural reader
   comparing the LAST N blank-line units against the slice's N paragraphs IN ORDER,
   N COUNTED BY THE SCRIPT from the slice and never taken from this block; plus a
   negative control flipping one byte inside the FIRST appended paragraph, which
   BOTH readers must REJECT while both accept the truth. Then `^Gate: F275 R28 `
   == 1 and `^Done: R-0872 — ` == 1. Then THE OPEN SET BY DISTINCT ID, every
   distinct `^- R-\d+ — ` id minus every distinct `^Done: R-\d+ — ` id, reporting
   both counts. It reads 89 at the base `99e677f0` over 102 registrations against
   13 resolutions; this commit registers none and resolves one, so it must read 88.

G4 THE RENAME (at C3). V1 and V2 each FROM 1 -> 0 and TO 0 -> 1. Then, for EVERY
   mapping in the table, the count before and the count after, with the after count
   ZERO for all of them; report the total replaced. Then over the whole file the
   RAW substring `remedy ` followed by any of the 22 flat spellings must be 0, and
   the file's total line count must be reported. If any mapping's before-count
   differs from the bracketed number, that is a deviation to DECLARE, not a reason
   to stop — the counts are the reviewer's readings at `99e677f0` and the file has
   not moved since, so a difference means one of us is wrong and the handback says
   which.

G5 THE SWEEP (at C3), through the WORKER's OWN import of the guard module as it
   stands at C3, with the allowlist STILL PRESENT. The operator-facing sweep must
   read ZERO unresolved, and the allowlist must therefore be entirely STALE — report
   `len(KNOWN_DEAD_DOC_ADVERTISEMENTS)` and the count of its entries that no longer
   occur, which must be 22 and 22. This is the ratchet correctly demanding its own
   deletion, and it means the guard suite is EXPECTED TO BE RED between C3 and C4;
   report that red, with its assertion, as the evidence it is. The production sweep
   must read 542 seen and ZERO unresolved.

G6 THE RATCHET IS GONE (at C4). ZERO occurrences of `KNOWN_DEAD_DOC_ADVERTISEMENTS`,
   `_ALLOWLIST_CEILING` and `only_ever_shrinks` in the guard module. Then
   `ruff check tests/cli/test_advertised_commands.py`, which per constraint 7 is the
   only check that can see an incomplete removal — report its real message. Then
   `python3 -m pytest tests/cli/test_advertised_commands.py -q`, which must be GREEN
   at 5 passed, one fewer than round 28's 6 because the ratchet test is one of them.
   Then, INSIDE A DISPOSABLE WORKTREE at C4 per guardrail G5, the RED PROOF: run the
   unmutated control first and report it; then restore `remedy absorb` into
   `docs/system/vocabulary.md` and report the colour, which must be RED; then revert
   and prove the file is byte-identical to its committed blob. Remove and prune the
   worktree.

G7 NOTHING ELSE MOVED (at C4, before C5).
   - `python3 -m pytest tests/docs/ tests/cli/ -q` run SERIALLY — report passed and
     failed. It must be GREEN at 1648, one fewer than round 28's 1649, and the
     difference must be exactly the deleted ratchet test; say so explicitly rather
     than reporting a bare number. The canary is inside `tests/cli/`.
   - Through the shipped reader `apps.cli.command_catalog`: `len(_BASE_CATALOG)`,
     `len(GROUPS)`, dangling `related=` count — 222, 44 and 0 at `99e677f0` and
     unchanged. Resolve `related=` on the DOTTED id, not on a spaced pair; round 28
     declared a reader that got this wrong.
   - All 22 TO pairs of the rename table resolve in the shipped `CATALOG` — report
     the count that resolve and name any that do not.
   - `.agent/STOP` absent (from disk), `git status --porcelain` EMPTY,
     `git worktree list` exactly ONE entry, branch correct.
   - `git diff --name-only 99e677f0..<C4>` an EXACT SET MATCH against the change set
     minus `.agent/handoff.md`; report MISSING and EXTRA explicitly.
   - Per-commit insertions for every commit BEFORE the handback commit, against the
     DECISION F104 D1 cap of 500.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — feature
and round, SESSION 14 of F275, branch, per-commit changed-files table with `+/-`
transcribed cell by cell from `git show --numstat` (§3 item 28), one line per gate
with real exit codes, the item-status table covering C0a..C5, V1, V2, the rename
table, G1..G7 and R-0872, every deviation declared, the open-findings count, and the
next expected action. It has NO length cap. Push the branch. Create NO pull request.

────────────────────────────────────────────────────────
