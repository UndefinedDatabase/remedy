STEP T001-close / F275 — ROUND 23 — DECISION F260 D3, THE DELETION PARAGRAPH

Goal: draft DECISION F260 D3 — the paragraph F260's Design, F275's Goal & Done and
F275's T001 all require before this feature can close — naming every module the
prototype-cluster deletion removed and the feature that inherited its idea; rule the
three questions open fix clauses hand to this round; book session 12's pending record;
and repair the two stale comments and the two vacuous test assertions that the
deletion left behind.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r23.md`
  C0b  mirror the COMMITTED C0a blob into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN23
  C2   the record: LEDGER23 appended to `.agent/live_review.md`, SLIPS23 appended to
       `.agent/prose_slips.md`
  C3   DEC23 appended to `.agent/decisions.md` — DECISION F260 D3, DECISION F275 D12,
       DECISION F275 D13
  C4   the repairs (pairs P1 to P4) and LANDED23 appended to
       `.agent/live_review.md`
  C5   the handback

Change set — EXACTLY these paths, nothing else:
  .agent/authored/f275-r23.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/decisions.md
  packages/common/public_text_redaction.py
  packages/orchestration/decision_evidence.py
  tests/cli/test_product_spine.py
  tests/cli/test_mission_cmd.py
  .agent/handoff.md

Constraints:
 1. Every slice between a BEGIN and END marker is applied BYTE FOR BYTE. Do not
    reflow, re-wrap, re-indent or "fix" anything inside one. If a slice looks wrong,
    apply it anyway and declare it in the handback — that is the protocol.
 2. Marker lines are never written into any target file.
 3. THE APPEND CONVENTION for `.agent/live_review.md`, `.agent/prose_slips.md` and
    `.agent/decisions.md`, verified by the reviewer against all three files at
    `6f865e50`: each file ends with exactly ONE newline byte. An append writes
    `pre + b"\n" + slice`, where the slice itself ends with one newline. The joining
    byte produces the blank line that separates records. Do not add or trim any other
    byte at the seam.
 4. WITHIN a slice bound for `.agent/live_review.md` or `.agent/prose_slips.md`,
    records are separated from each other by a BLANK line, because that is the record
    format both files already use. This is the correction the round 22 prose slip
    asked for: round 22's three slip entries were separated by single newlines and
    landed as ONE blank-line unit.
 5. C2 is the FIRST substantive commit of this round, before C3 and before C4.
 6. C4 follows C2. R-0870's registration paragraph in LEDGER23 states that this
    round's C4 repairs it; this constraint is what makes that sentence true, and it
    is named there rather than a SHA, per planner_reviewer_prompt.md §3 item 20 and
    finding R-0524.
 7. PAIR SHAPES, each classified by a containment test the reviewer RAN at
    `6f865e50`, one reading per pair, output quoted:
      P1  TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
      P2  TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
      P3  TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
      P4  TO contains FROM: false -> REWRITE. FROM occurs 1x in its target, AND the
          TO string ALREADY occurs 1x in that target before the edit, because the TO
          is the second line of the FROM. So P4 gets no "TO 1x" gate — G5 gates it on
          the deleted assertion going to zero and the surviving one staying at one.
 8. NO module, command, catalog entry or test is deleted in this round. This is not a
    deletion round. `.agent/f275_deletion_order.md`, `cluster_deletion_map.txt`,
    `test_cluster_deletion_map.py` and `test_cluster_deletion_order.py` are NOT
    touched here — DECISION F275 D13 routes their retirement to the next round.
 9. Destructive verification runs ONLY inside a disposable `git worktree`, never in
    the primary checkout (self_drive_protocol.md G5). Remove and prune it before the
    handback.
10. Read `.agent/STOP` from disk before the first commit. If it exists, write the
    handback and stop.

Done when — G1 to G8 below have all been RUN, with their real exit codes recorded,
and the handback carries ONE line per gate. Every gate runs at or before C4, so the
handback written by C5 can quote all of them (§3 item 31).

G1 TRANSPORT. `sha256` of the committed `.agent/authored/f275-r23.md` blob at C0a
equals the digest in this block's BEGIN marker, and the committed `.agent/last_block.md`
blob at C0b equals the same digest. Report both digests. Per §3 item 37 this chain
covers those two committed artefacts and the reviewer's own scratch original, and
claims NOTHING about the bytes that travelled into your prompt.

G2 THE PLAN. `.agent/plan.md` at C1 is byte-identical to the PLAN23 slice. Report its
byte length and its line count, which must be under the AGENTS.md cap of 50, and
confirm `^## Goal$` and `^## Next Steps$` each occur exactly once.

G3 THE RECORD, at C2, for `.agent/live_review.md` and `.agent/prose_slips.md`
separately. Reading (a), bytes: the committed post-blob equals the pre-blob, then one
newline, then the slice exactly as extracted; READ THE JOINING BYTE BACK from the post
blob at offset len(pre) and report it rather than asserting it. Reading (b),
structure: count N as the number of blank-line-separated paragraphs IN THE SLICE with
your own script — do not take N from this block — and compare the LAST N blank-line
units of the whole post-file against those N paragraphs IN ORDER. Negative control:
flip one byte inside the FIRST appended paragraph and confirm BOTH readers reject it
while both accept the truth (§3 item 36). Then report these counts over the whole
post-file: `^Gate: F275 R22 ` exactly 1, `^- R-0869 — ` exactly 1, `^- R-0870 — `
exactly 1, `^Note: F275 R23 ` exactly 2, `^Done: R-0862 — ` exactly 1, and
`^Landed: R-0862 ` STILL exactly 1 and NOT removed — the `Landed:` line survives
beside the `Done:` paragraph that supersedes it, per DECISION F272 D10. Finally
report THE OPEN SET BY DISTINCT ID, computed as every distinct id in a `^- R-\d+ — `
paragraph minus every distinct id in a `^Done: R-\d+ — ` line. The reviewer computed
it at `6f865e50` as 91, over 97 distinct registrations against 6 distinct resolutions.
It must read 92 at C2, because this commit registers two ids and resolves one.

G4 THE DECISIONS, at C3, over `.agent/decisions.md`. The same two readings and the
same negative control as G3, because this is a record file and the gate budget
reserves full byte forensics for exactly that. Then report `^## DECISION F260 D3 `,
`^## DECISION F275 D12 ` and `^## DECISION F275 D13 ` as each occurring exactly once
in the whole file.

G5 THE REPAIRS, at C4. For each of P1, P2 and P3: the FROM string reads 0x and
the TO string reads 1x in its target file. For P4: the FROM string reads 0x, the line
`assert "packages.orchestration.overnight_readiness" not in source` reads 0x in
`tests/cli/test_mission_cmd.py`, and the line
`assert "from packages.orchestration.mission_readiness import" in source` STILL reads
exactly 1x. Then run, from the primary checkout, and report the real counts:
  python3 -m pytest tests/cli/test_product_spine.py tests/cli/test_mission_cmd.py tests/orchestration/test_decision_evidence.py -q
  python3 -m ruff check packages/common/public_text_redaction.py packages/orchestration/decision_evidence.py tests/cli/test_product_spine.py tests/cli/test_mission_cmd.py
The reviewer ran both against an APPLIED copy of these four pairs in a disposable
worktree at `6f865e50` and measured 307 passed and `All checks passed!`. Report what
YOU measure; a difference is a finding, not something to fix silently.

G6 THE COMPLETENESS SWEEP, IN TWO HALVES, at C4. This split is R-0869's fix clause:
one half can be a hard zero and the other cannot, and ordering a single zero over both
is the gate that cannot pass.
  (a) THE HARD ZERO, over every tracked file outside `.agent/` and `.data/`: each of
      the five spaced advertisement forms `remedy provider intake-repair`,
      `remedy provider trust-show`, `remedy provider material-show`,
      `remedy provider verify` and `remedy provider verification-show` reads ZERO.
      Report the number of files swept and the count per form.
  (b) THE RAW LIST, over the same file set, for the bare names `provider_trust` and
      `provider_trust_verification` matched as whole words: PRINT EVERY HIT IN FULL as
      `path:line`, never truncated, and report the total. Do NOT drive it to zero.
      The reviewer measured this at `6f865e50` and states the expectation in advance:
      hits under `docs/roadmap/features/` are HISTORY PROSE and stay, and at that
      commit they are in `T2_F260.md`, `T2_F272.md`, `T2_F274.md` and `T7_F133.md`;
      the deliberate-absence notes this feature deliberately wrote stay, and
      they live in exactly `packages/orchestration/provider_patch_material.py`,
      `packages/orchestration/self_dogfood_execution.py`,
      `tests/orchestration/test_cluster_deletion_map.py` and
      `tests/orchestration/test_cluster_deletion_order.py`; the two hits in
      `packages/common/public_text_redaction.py` and
      `packages/orchestration/decision_evidence.py` are R-0870 and MUST BE GONE after
      C4. Reconcile your list against that expectation and report any hit in a file
      not named here — that is the reading this gate exists to produce.

G7 THE CANARY, at C4: `python3 -m pytest tests/cli/test_golden_path.py -q`, real exit
code and real counts. The full suite is NOT part of this round's gate — this is a
round gate, verification tier 1.

G8 HYGIENE, at C4. `.agent/STOP` does not exist. `git status --porcelain` is EMPTY.
`git worktree list` holds exactly ONE entry. The branch is
`feature/f275-one-world-completion-part-three`. `git diff --name-only 6f865e50..C4`
names EXACTLY the change-set paths above other than `.agent/handoff.md`, reported as
an exact set match with MISSING and EXTRA both printed even when empty. Report each
commit's insertion count from `git show --numstat`, for every commit before the
handback commit, against the AGENTS.md DECISION F104 D1 cap of 500 insertions.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — the state
block with the SESSION NUMBER, the per-commit changed-files table with `+/-` cells
transcribed from `git show --numstat` and compared cell by cell against it (§3 item
28), one line per gate with its real exit code, every declared deviation, the item
status table, and the next expected action. There is no length cap. Then push.

<<<BEGIN PLAN23>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 23 drafts DECISION F260 D3, the deletion paragraph T001 names as its last item and
F275's Goal & Done makes a closing condition: every module F260's Design listed, the feature
that inherited its idea, and the ideas deleted rather than inherited, with the finding ids
that hold each enumeration. DECISION F275 D12 rules the three questions R-0866, R-0867 and
R-0868 hand to this round; DECISION F275 D13 records that the fix clauses bound to "the D3
round" are discharged across this round and the next, because they do not fit one block.
The round also books session 12's pending record and repairs two stale comments and two
vacuous test assertions.

## Next Steps

1. The repairs the D3 fix clauses leave outstanding: R-0832's event-name couplings and the
   dead code they left, R-0859's two dangling `related=` references and its
   referential-closure test, R-0858's F267 repair, R-0843's `Groups` table, and R-0868's
   retirement of the four now-vacuous cluster scaffolding artefacts.
2. T002, the atomic record flip, alone, because every later commit's size depends on it.
3. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 91 by distinct id at this round's base `6f865e50`, computed mechanically
  from the record. This round registers two and resolves one, leaving 92. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- DECISION F260 D3 lands in an append-only file and cannot be corrected, only superseded, so
  every module-to-feature mapping in it is taken from a dated finding or a dated decision
  rather than from the reviewer's reading of what a module looked like it did.
- R-0855 is RESOLVED, not open. Session 12's handoff routed two new residues to it as an open
  finding; they are registered as R-0870 instead.
<<<END PLAN23>>>

<<<BEGIN LEDGER23>>>
Gate: F275 R22 — the F275 round 22 entry. VERDICT PASS, written by the planner and reviewer of session 12 after reading the committed range `5178df03`..`67f83bdd` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was not evidence for any line here. Booked by round 23's C2 from the pushed handback at `6f865e50`, under amend0827-process-diet rule 1. SEVEN single-parent commits C0a `05cdebe2`, C0b `f1d77cac`, C1 `80268fd0`, C2 `c9b439b3`, C3 `6992661a`, C4 `0242c0a3` and C5 `67f83bdd`, per-commit insertions 490, 419, 20, 14, 66 and 183 for the six before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own delegation source and both committed copies are 49993 bytes at `101928f714785319151732c17c8758b4ded01df8221e0b7b41a7020aabff56cc` and compare BYTE-EQUAL; per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` at C1 is 2300 bytes byte-identical to its slice, 40 lines against the cap of 50, all four slices occur exactly once in their targets, and a sweep for all eight marker strings over the four targets returns ZERO for every file. G3 HELD OVER THREE APPENDS: for `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` the committed post-blob equals the pre-blob then one newline then the slice, the joining byte was READ BACK from each post blob at offset len(pre) and is a newline in all three, the structural reader counted N from the slice itself — 5, 1 and 9 paragraphs — and matched the last N blank-line units in order, and all three NEGATIVE CONTROLS were flipped inside the FIRST appended paragraph per §3 item 36 and rejected by BOTH readers while both accepted all three truths; `^Gate: ` rose 43 to 44 and the open set went 88 to 91 BY DISTINCT ID against registrations 94 to 97 and resolutions 6 to 6, with `Landed:` unchanged at 39 lines and never subtracted. G4 IS RED AND THE REVIEWER SUSTAINS BOTH THE COLOUR AND THE WORKER'S REFUSAL TO CHASE IT: the gate as the reviewer wrote it CANNOT PASS, which is a defect of the block and is registered as R-0869. THE HALF THAT IS MEETABLE HOLDS COMPLETELY — over the 1652 tracked files outside `.agent/` and `.data/`, all five deleted command ids, all six deleted `ContractAction` values and all five SPACED advertisement forms return ZERO hits anywhere in the repository, so no page and no live code path still gives an operator a command that cannot run. RAW over the bare module names is 20, printed in full, of which 7 are history prose under `docs/roadmap/features/`, 5 are the deliberate-absence notes the block itself ordered, 5 are PERSISTED data-shape names a deletion round must not change, 2 are illustrative docstring examples inside the two cluster ratchets, and 1 is the stale `CLUSTER_COMMAND_HANDLERS` entry R-0864 already holds — leaving exactly TWO genuinely new residues, both prose in comments and both in files the change set did NOT name, which the worker found, declined to widen an exhaustive change set to reach, and flagged. G5's STOP CONDITION DID NOT FIRE: re-run in a disposable worktree at C4, the import resolves inside that worktree so no editable install shadows it, the mutated bytes occur exactly ONCE in the named path, the unmutated CONTROL is exit 0 at 39 passed, making `_transition` ACCEPT an illegal transition is exit 1 with EXACTLY ONE failure — `TestStartAndIdempotency::test_transition_rejects_illegal` — and the revert returns exit 0 at 39 passed with the worktree porcelain EMPTY. G6 DISCHARGES R-0859's STANDING OBLIGATION BY MEASUREMENT, reading the SHIPPED catalog by import and never by grepping source, at the tip and in a READ-ONLY disposable worktree at the base: commands fall 227 to 222, groups 45 to 44, `"provider"` is ABSENT from `GROUPS`, the id set beginning `provider.` is EMPTY where the base held five, duplicate ids are 0 at both revisions, and resolving every `related=` tuple against the live id set gives EXACTLY TWO dangling references at BOTH revisions, both pre-existing and both held by R-0859 — this round added none, and step 7 repaired the three it would otherwise have created. G7: the guards 884 passed, the canary 42, and THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18352 passed, 23 skipped and ZERO failed in 1287.83s; the arithmetic closes BY THE ID SET, taking the WHOLE line as the node id so a parametrized id carrying a space is not truncated into a collision — 18478 at the base against 18375 at the tip, being 104 ids REMOVED against 1 ADDED, and 18352 plus 23 equals 18375 exactly. Ruff reads `Found 24 errors.` at BOTH revisions with identical per-file distributions over 16 files, paired with a RED CONTROL confirming the comparison can fail, and not one of the 24 is in a file this round touched. G8: no `.agent/STOP`, porcelain EMPTY, ONE worktree, the branch correct, `C3..C4` naming 36 paths in an exact set match with MISSING and EXTRA both empty, exactly TEN files deleted whole, and every one of the 42 `+/-` cells of the handback's `## Commits` tables agreeing with `git show --numstat`. ALL SEVEN DECLARED DEVIATIONS ARE SUSTAINED, and the two that matter are the round rescuing the reviewer: C4 was committed, found wanting by the worker's own G4 run, unstaged with `git reset --soft` while UNPUSHED, repaired and re-committed as ONE commit, which was correct because constraint 3 made C4 atomic by operator RULE 1 and an unstage of an unpushed commit is not a history rewrite; and what the repair ADDED is the reviewer's own gap, FOUR dead advertisements the block's steps had not named, so the spaced-form sweep reads ZERO because the worker went further than it was told.

- R-0869 — Medium, A ZERO-GATE OVER PRODUCTION CODE WAS UNMEETABLE BY CONSTRUCTION, BECAUSE THE SAME BLOCK ORDERED THE VERY TEXT IT FORBADE. Raised by the reviewer of session 12 against its own round 22 block and registered rather than recorded as a prose slip, because amend0827-process-diet rule 2 reserves an id for "a gate over production code shown to be blind or unmeetable" and this gate was ordered over `packages/`, `apps/` and `tests/`. THE MEASUREMENT, taken at `67f83bdd`: G4's closing clause reads that ANY hit for a deleted module name under `docs/guides/`, `docs/system/`, `packages/`, `apps/`, `scripts/` or `tests/` "is a defect of this round", while steps 3(a), 5 and 9 of the same block order deliberate-absence comments naming `provider_trust` and `provider_trust_verification` into `packages/orchestration/self_dogfood_execution.py`, `packages/orchestration/provider_patch_material.py` and `docs/system/self-dogfood-execution-v0.md` — five hits the block itself commissioned. The worker could satisfy the clause only by deleting text the same block ordered, so it ran the gate, reported exit 1, enumerated all 20 raw hits and declared the contradiction; that is the honest reading and it cost the round a deviation. `docs/agents/planner_reviewer_prompt.md` §3 item 2 states this rule exactly — "a `must be 0` done-when may not count a string that any TO slice in the same block writes into that same file" — and item 2's own note records that it had recurred six times across F104 and F105 before it was written down, so this is the class recurring under the rule rather than a new one. FIX CLAUSE, binding on the next block of this feature that orders a completeness sweep after a deletion: split the sweep into the clause that CAN be zero and the clause that cannot. The command ids, the `ContractAction` values and the SPACED advertisement forms are the meetable half and stay a hard zero, because nothing the block orders writes a runnable invocation; the BARE MODULE NAME half is ordered as a RAW LIST to be printed and classified, with the block naming in advance the files its own deliberate-absence notes will put a name into, so the worker reconciles against a stated expectation instead of against an impossible zero. THAT CLAUSE IS APPLIED BY THE BLOCK THIS ENTRY IS BOOKED BY: gate G6 of the round 23 block is the split form, and this sentence names the block rather than a SHA because the commit carrying it does not exist while this text is written, per §3 item 20's R-0524 carve-out.

- R-0870 — Low, SURVIVING COMMENTS WERE FALSIFIED BY A DELETION IN FILES THAT DELETION'S CHANGE SET DID NOT NAME, AND NO GATE IN THE REPOSITORY CAN SEE EITHER. Raised by the reviewer of session 13 while researching DECISION F260 D3, and registered rather than folded into R-0855 because R-0855 is RESOLVED — its `Done:` paragraph was written at `8124377d` by the reviewer of session 9 — and evidence cannot be added to the fix of a finding that no longer has one. §3 item 30 orders the OPEN set searched for the defect before an id is minted, and the reviewer did so at `6f865e50`: the open set holds 91 ids and none of them describes prose falsified in a file OUTSIDE the round's change set. R-0841 was the nearest and is resolved; R-0843's own text places itself at "ordinary prose elsewhere in a file the change set already edits", which is the distinguishing half. THE MEASUREMENT, taken at `6f865e50` by a whole-word sweep for all twenty-four cluster module names over the 1652 tracked files outside `.agent/` and `.data/`. FIRST, `packages/common/public_text_redaction.py` line 4 cites `packages/orchestration/provider_trust.py` as the origin of the redaction helpers it now hosts, and F275 round 22 deleted that path at `0242c0a3`, so a reader following the provenance sentence lands on nothing. The reviewer of session 12 WROTE that sentence in round 21 knowing round 22 would delete its referent, which is why this is the sharper of the two. SECOND, `packages/orchestration/decision_evidence.py` line 54 names `provider_trust_verification.ProviderVerificationEvidenceRef` as one of "the two nearest existing types", which is not stale wording but a FALSE claim, since that type is gone and only `orchestrator_brain.OrchestratorEvidenceRef` remains. WHY AN ID AND NOT A PROSE SLIP: both are wrong state on disk under `packages/`, which amend0827-process-diet rule 2 names as product effect; and NO GATE COULD SEE EITHER, because ruff is clean, the suite is green at 18352 passed, and both lines are prose inside comments. Low rather than Medium because nothing executes either line and no behaviour depends on them. REPAIRED BY THIS ROUND'S C4, which constraint 6 of the round 23 block fixes to follow this commit — the commit does not exist while this text is written, so the constraint is named instead of a SHA, per §3 item 20's R-0524 carve-out. FIX CLAUSE, binding on every remaining round of this feature whose change set contains a deletion: before the round's own completeness sweep is declared clean, run it over the files the PREVIOUS round CREATED as well as over the files this round edits, because a provenance sentence written one round before its referent dies is invisible to a sweep scoped to the change set.

Note: F275 R23 — a correction to the `Note: F275 R22 ` entry booked by round 22's C2, which states that `CLUSTER_COMMAND_HANDLERS` in `tests/orchestration/test_cluster_deletion_map.py` names seven handler paths of which FIVE have no file on disk. Re-measured by the reviewer of session 13 at `6f865e50` by resolving each of the seven paths: the tuple still names seven and now SIX of them are stale — `dogfood_cmd.py`, `overnight_mission_cmd.py`, `progress_cmd.py`, `provider_cmd.py`, `repair_loop_v2_cmd.py` and `self_repair_cmd.py` — leaving `apps/cli/commands/review_cmd.py` as the only entry that resolves. The earlier entry was true when it was written, at the base of the round that wrote it, and it named no commit, which is the §3 item 20 failure rather than an arithmetic one. The record is append-only, so that entry is NOT rewritten; this is the dated correction the checklist prescribes instead. The count is not load-bearing to R-0864, whose subject is that a stale entry can never fail, so no correction round is owed and R-0868's fix clause still carries the repair.

Note: F275 R23 — new evidence for the OPEN finding R-0858, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30, and stated here because it makes R-0858's own proposed repair too small. R-0858 records that `docs/roadmap/features/T2_F267.md`, `[ ]` in `docs/roadmap/STATUS.md`, plans nine list-shaped commands of which this feature deleted one, and proposes striking `execution.approval-list`, restating the count as EIGHT, and dropping `execution.template-list` from the DECISION F262 D4 exclusion sentence. THE RE-MEASUREMENT, taken by the reviewer of session 13 at `6f865e50` by reading the SHIPPED catalog through `apps.cli.command_catalog._BASE_CATALOG` rather than by grepping the feature file: of F267's nine, FIVE are gone — `repair.item-list`, `builder.session-list`, `execution.approval-list`, `external-builder.package-list` and `self-repair.proposal-list` — and only `test.list`, `mission.list`, `change.list` and `event.list` survive; and ALL FOUR of the D4 exclusions are gone, `builder.adapter-list`, `execution.template-list`, `worker.registry-list` and `approval.policy-list`, so the sentence that excluded four commands now excludes nothing that exists. F267's DONE condition additionally pins "all 24 in-scope commands", a figure derived from a catalog that has since fallen from 339 commands to 222. So the repair R-0858 proposes would leave the file wrong in three more places, and the numeral EIGHT it proposes is itself wrong by four. WHAT NOW RESOLVES R-0858: the repair strikes every deleted id, DELETES the numerals rather than synchronising them per §3 item 16, and adds one dated note naming R-0858, F275 and this measurement, telling the session that eventually claims F267 to re-derive its scope from the catalog rather than from the file. That repair is NOT performed by this round — DECISION F275 D13 routes it to the next, with the reason.

Done: R-0862 — Resolved by F275 round 21. The human-review routing tier has a positive pin again. `tests/orchestration/test_orchestrator_brain.py::TestModelRouting::test_loop_guard_forces_human_review_tier` drives two `tested_failed` repair attempts into the loop guard, asserts `LoopGuardStatus.REQUIRE_HUMAN_REVIEW` as a PRECONDITION so the test cannot pass vacuously, and then asserts `_routing_plan` returns `RoutingTier.HUMAN_REVIEW_REQUIRED` with `allow_external` False. THE COLOUR THE FIX CLAUSE ASKED FOR WAS MEASURED, by the reviewer as well as by the worker, in a disposable worktree at `eaea1cff`: the unmutated control is exit 0 at 6 passed, replacing the two-line loop-guard condition at the top of `_routing_plan` with a constant false gives exit 1 with EXACTLY ONE failure, that test, reading `assert 'local_advisor_preferred' == 'human_review_required'`, and the revert returns exit 0 at 6 passed. R-0862's own measurement was that the same mutation left `TestAntiLoop` and `TestModelRouting` GREEN at 5 passed, so the branch went from unpinned to pinned and the finding is closed on its own terms. The tier itself never changed and no capability was inherited by another feature; only its guard was missing, which is why it was Medium. The `Landed: R-0862` line round 21 wrote is SUPERSEDED by this paragraph and is deliberately NOT removed, per DECISION F272 D10.
<<<END LEDGER23>>>

<<<BEGIN SLIPS23>>>
2026-09-10 · F275 R22 · The round 22 block's SLIPS22 slice carried three dated entries separated by single newlines, while every entry already in `.agent/prose_slips.md` is separated from its neighbour by a BLANK line. The three landed as one blank-line unit, so the file's own record shape is broken for them and a reader counting entries by paragraph will find one where there are three. The structural reader in that round's G3 counted N as 1 and was right to; nothing measured the SHAPE against the shape of the entries it joined, which is `docs/agents/planner_reviewer_prompt.md` §3 item 26 applied to a file other than the ledger. The record is append-only so the landed entries stay as they are. The lesson is that item 26's mechanical comparison is run for EVERY append-only target a block writes into, not only for `.agent/live_review.md`, and that the separator is part of the record format rather than presentation.

2026-09-10 · F275 R22 · The round 22 block's documentation step named six pages and the reviewer's applied dry run had edited them, yet the worker's own sweep found FOUR dead advertisements the step had not reached: the intake pipeline still drawn in `docs/archive/candidate-generator-adapter-future.md`, two advertised commands in `docs/system/provider-patch-materialization-v0.md`, the re-entry section of `docs/system/repair-request-builder-v0.md`, and a `_detect_roadmap` rule in `packages/orchestration/self_dogfood.py` gated on a module file that would never exist again. The reviewer's dry run had reached those first three pages and edited only their LINKS, because the token sweep that drove it matched module names and command ids rather than the prose around them. The lesson is that a deletion round's documentation step is derived from a sweep for the CAPABILITY in the pages' own words — "re-enter", "import the response", "intake" — and not only from a sweep for the identifiers being deleted, because a page can advertise a deleted flow without naming a single deleted symbol.

2026-09-10 · F275 R22 · The round 22 block's introduction said `provider_patch_material.py` "loses six of its imports", a figure inherited verbatim from session 11's handoff, and the R-0867 slice repeated it as "takes six names from the dying pair". The reviewer caught it before emission by resolving the module's import statements at the base, where the answer is FOUR — session 11 measured six before F275 round 21 moved `_scrub_public` and `_safe_path_label` out of that dependency — and corrected both occurrences. It is recorded even though nothing landed wrong, because the same session had already written a slip about re-measuring inherited prose and then reproduced the class twice in the next block it wrote. The lesson is that every numeral carried across a session boundary is re-derived from the tree, and that a slip written about a class is not evidence the class has stopped.

2026-09-10 · F275 R23 · Session 12's handoff drafted a `Note:` folding two new residues into R-0855 and called it "the OPEN finding R-0855", and the reviewer of session 13 measured at `6f865e50` that R-0855 carries a `Done:` paragraph written at `8124377d` by session 9 and is not in the open set at all. Nothing landed wrong, because the note was still a draft in a handback when the error was caught, and the residues are registered as R-0870 instead. The lesson is that §3 item 30's "search the open set for the defect" is a search of the OPEN set specifically — the mechanical `^- R-\d+ — ` minus `^Done: R-\d+ — ` computation item 10 already requires — and that a finding id recalled from a previous round's prose is not evidence of that finding's state, which is the A1 trap §0 names arriving through a resolved id rather than through a stale numeral.
<<<END SLIPS23>>>

<<<BEGIN DEC23>>>
## DECISION F260 D3 (2026-09-10, F275 round 23) — the deletion paragraph: every module the prototype-cluster slice removed, and the feature that inherited its idea

WHERE THIS WAS OWED. `docs/roadmap/features/T2_F260.md` carries D3 as a stub headed "to
be recorded in T005" and lists the mapping it must expand. F260's Design section names the
twenty-four modules; F275's Goal & Done makes this paragraph a closing condition of the
feature; F275's T001 orders it drafted after the last module group and before the slice is
called done. It is recorded here rather than in F260's file because `.agent/decisions.md`
is where every DECISION of this chain lives, and because F260 is `[x]` and its file is kept
unedited on purpose, as F272's, F274's and F275's own files each state.

THE MEASUREMENT, taken by the reviewer at `6f865e50` by importing the SHIPPED readers —
`apps.cli.command_catalog._BASE_CATALOG` and `GROUPS`, and
`packages.orchestration.run_contract.ContractAction` — at F275's fork point
`a5bf894946ab6de053a4232109d6341a63533768` in a read-only disposable worktree and at the
tip, never by grepping source. Commands fall 339 to 222. Groups fall 59 to 44. Run-contract
actions fall 122 to 90. Exactly ONE command id was ADDED across the whole feature,
`mission.readiness`, which is the first carry-over. All twenty-four modules F260's Design
lists are absent from disk, verified path by path at the same commit.

THE COMMAND GROUPS DELETED WHOLE, with their ids: `approval` (policy-disable,
policy-enable, policy-evaluate, policy-grant, policy-list, policy-show); `builder`
(adapter-enable, adapter-list, adapter-show, integrity, package-create, session-create,
session-intake, session-list, session-record-output, session-show); `builder-routing`
(decide, report); `candidate-quality` (evaluate, integrity, report, scorecard, show);
`dogfood` (brainstorm, checkpoints, create, evaluate, morning-report, next, replay,
run-loop, show, status, step, stop); `execution` (approval-list, approval-show,
approval-validate, approve, claude-doctor, debug-bundle, integrity, list,
operator-runbook, run, show, template-create, template-disable, template-enable,
template-list, template-show, template-update); `external-builder` (evaluate, integrity,
package-create, package-list, package-show, submission-list, submission-show, submit);
`local-advisor` (run, status); `local-candidate` (generate, status); `overnight`
(contract-create, contract-readiness, contract-show, cycles, evaluate, integrity,
next-action, plan, readiness, report, run); `progress` (checklist); `provider`
(intake-repair, material-show, trust-show, verification-show, verify); `route-policy`
(evaluate, set, show); `self-repair` (proposal-approve, proposal-create, proposal-deny,
proposal-edit, proposal-list, proposal-show, worker-prompt); `tournament` (integrity,
list, report, show).

THE GROUPS THAT SURVIVE HAVING LOST IDS: `context` loses explain, optimize and pack;
`repair` loses attempts, context-pack, evaluate, integrity, item-create-from-failure,
item-create-from-review, item-list, item-show, policy-set, policy-show and route-recommend;
`review` loses bundle; `worker` loses add, disable, doctor, explain, recommend,
registry-integrity, registry-list and registry-show.

THE MAPPING, module by module. Each entry names the feature that inherited the IDEA, and
every one is taken from a dated finding or a dated decision rather than from a reading of
what the module looked like it did. `provider_trust.py` and
`provider_trust_verification.py` — the Trust Gate; NONE, deliberately, the mapping F260's
own stub already fixes for the external builder, with R-0866 recording the residue.
`external_builder_sandbox.py` — F085, external-worker ingress (R-0852), with the scoring
step going to F082 (R-0849). `main_builder_adapter.py` and `managed_builder_execution.py` —
F085 for bounded subprocess execution and F017 for human approval (R-0856, R-0860).
`execution_approval_policy.py` — F017, policy-authorised approval (R-0851).
`local_model_advisor.py` — F110, local-model advisory critique (R-0853).
`local_candidate_generator.py` — NONE, deliberately (R-0848). `candidate_quality.py` and
`model_route_tournament.py` — F082, evidence-based comparison of a candidate (R-0848).
`builder_routing.py` — F110, routing configuration (R-0848, with R-0831 holding the
knob-by-knob audit). `worker_registry.py` — F110, model routing (R-0865).
`worker_recommend.py` — NONE, by DECISION F274 D7, which rules worker recommendation dies
with the cluster; its token mode MOVED to `token_policy.py` because it never belonged to
the cluster. `context_pack.py` and `context_optimizer.py` — F107, context compiler v2
(R-0842). `overnight_mission.py` and `overnight_executor.py` — F269, which
`docs/system/vocabulary.md` already records as the feature that builds the contract
(R-0845), with the morning report carried to `mission report` in its degraded form and the
run-keyed addressing deleted (R-0840). `overnight_readiness.py` — CARRIED, not deleted in
idea: DECISION F275 D1 moved its measured definition set byte-identically into
`packages/orchestration/mission_readiness.py` and it ships as `mission readiness`, the one
command id this feature added. `repair_loop_v2.py` — F110, for the repair work item, its
route recommendation and its policy knobs (R-0845). `self_repair_proposal.py` — F017, the
approval gate (R-0845). `dogfood_run.py` — NONE, deliberately, because F260's Design
deletes the prototype rather than carrying it (R-0845). `progress_ledger.py` and
`review_bundle.py` — `job show --full` and `job evidence`, the mapping F260's stub fixes,
with the safe per-job bundle idea itself going to the review-zip pipeline (R-0844).
`feature_planner.py` — NONE, by DECISION F274 D6, which deletes the `feature` command
group with its module edges and rules that nothing inherits it.

THE IDEAS DELETED RATHER THAN INHERITED, each naming the finding that holds its full
enumeration, because the record is append-only and citing a dated measurement is stronger
than copying it into a second place where it can drift: the user-settable route-policy
knobs, none of which has an equivalent in F110's configuration (R-0831); the five run-keyed
dogfood fields of the old overnight report (R-0840); the three cockpit context readings —
the context-pack brain node, the humanized `context_pack_created` event and the planner row
of the token-budget breakdown (R-0842); the per-job review-bundle export and its doctor row
(R-0844); the 38 ids and the second mode of `remedy mission run` (R-0845); the 13 ids and
four groups of the builder-routing component (R-0848); `external-builder evaluate`, which
leaves the ingress deliberately without a scoring step until F082 provides one (R-0849);
the six ids and the `approval` group (R-0851); the seven ids and the `external-builder`
group (R-0852); the `local-advisor` group and the `--use-local-advisor` path (R-0853); the
seventeen commands, the `execution` group and the fourteen run-permission actions (R-0856);
the narrowing of three surviving `worker` commands (R-0857); the thirteen ids, the `builder`
group and six run-permission actions (R-0860); the review-state stop in three surviving
modules, which NO feature inherits because the capability as built was a parser for a ledger
format this repository no longer writes (R-0863); the routing recommendation and the
`ollama_placeholder_available` cockpit key (R-0865); the only route by which an external
candidate entered a self-improvement attempt (R-0866); and two of the seven checks of
`verify_provider_patch_material` (R-0867).

WHAT THIS PARAGRAPH DELIBERATELY DOES NOT DO. It provides no stub, no shim, no alias and no
compatibility reader, which AGENTS.md's Scope Control forbids by name and which T001 RULE 3
forbids again; git is the archive. It does not re-open any of the findings above, each of
which stays as its own dated record; naming an inheritor is not resolving a finding. And it
mints no feature: where the answer is NONE it says NONE, because "deliberately absent" is a
supported answer in this repository and an invented owner is not.

HOW TO REVERSE: delete this decision. The deletion itself is reversed only from git
history, which is the point of recording the mapping before the branch merges.

## DECISION F275 D12 (2026-09-10, F275 round 23) — the three questions the D3 fix clauses hand to this round, ruled

(a) THE DEGRADED RAIL IS KEPT, which is R-0866's question. `AttemptState`'s members beyond
    `AWAITING_EXTERNAL_CANDIDATE` and the `self_awaiting_candidate` situation key in
    `orchestrator_brain.py` STAY. They are not dead code: they still run for an attempt
    whose `patch_intent_id` is already on disk, and what round 22 removed was the only
    code that could acquire a NEW one. Retiring a surviving module's vocabulary is a
    product change, and F275's Do-not-touch forbids deleting any module outside F260's
    Design list. ALTERNATIVE CONSIDERED: retire the post-`AWAITING_EXTERNAL_CANDIDATE`
    members now — rejected because it would delete reachable behaviour under a deletion
    mandate that does not cover it, and because a state machine narrowed on the way past
    is exactly the "while I'm here" edit Scope Control names. R-0866 stays OPEN and its
    resolution is the feature that next opens the external-candidate route.

(b) `provider_patch_material.py` IS REAPED BY NO FEATURE TODAY, which is R-0867's
    question, and the ruling is stated rather than routed to a convenient id. Its
    remaining reachable function reads material that nothing can now create, and no
    feature file in `docs/roadmap/features/` claims it — the reviewer checked at
    `6f865e50`, where the only roadmap file naming it is F278, and only for its
    atomic-write helper. The module is NOT deleted here, because F275's Do-not-touch
    rules that no module outside F260's Design lists is deleted. TWO CONSEQUENCES BIND
    FORWARD. FIRST, and this is the half R-0867's fix clause asks for by name: no round
    may treat `verify_provider_patch_material`'s weakened `ok` as a safety property. It
    lost two of seven checks and is strictly easier to satisfy than the name suggests.
    SECOND, its retirement belongs to whichever feature next opens the external-candidate
    route, and this decision deliberately mints no feature to hold it, because
    registering a feature to justify a deletion is how an attic gets built.

(c) `repair_request_builder.py` IS REAPED BY NO FEATURE TODAY either, which is the second
    half of R-0868's question, and for the same reason and with the same reversal. It
    still packages evidence for an external actor; what it no longer claims is a round
    trip, because DECISION F275 D11 removed the five advertisements and the two result
    fields that promised one. It is outside F260's Design list and is therefore not
    deleted by this feature.

HOW TO REVERSE: delete this decision. Any later relay may rule (a) the other way, or name
an owner for (b) and (c), without disturbing DECISION F260 D3.

## DECISION F275 D13 (2026-09-10, F275 round 23) — the fix clauses bound to "the D3 round" are discharged across two rounds, because they do not fit one block

CONTEXT. The fix clauses naming "the round that drafts DECISION F260 D3" as the round that
discharges them are R-0832's, R-0858's, R-0859's, R-0864's, R-0866's, R-0867's and
R-0868's, together with the clause R-0870 carries in place of the resolved R-0855's.
Between them they order the deletion paragraph itself, the rulings D12 records, an
event-coupling measurement with the dead code it exposes, a referential-closure test with
its catalog repairs, a roadmap-file repair, the vacuous test assertions and the retirement
of the cluster scaffolding.

MEASURED, not estimated: DECISION F085 D6 caps a step block at 490 lines TOTAL with its
prose capped at 400 by DECISION F105 D5. The reviewer assembled the slices for all eight
clauses at `6f865e50` and the block does not fit — the D3 slice alone runs past a hundred
lines once the id enumerations the clauses require by name are in it, and DECISION F009 D16
rules that a block which does not fit is not delivered, it becomes a declared deviation on
a round that did nothing wrong.

CHOSEN: "the round that drafts DECISION F260 D3" is read as the D3 SEQUENCE, which is this
round and the one after it, and every clause above is discharged inside that sequence. This
round takes the decision itself, the three rulings, the record, and the two repairs whose
clauses name this round AT THE LATEST — R-0870's two comments and R-0864's two vacuous
assertions. The next round takes R-0832's event-name couplings and the dead code path they
left, R-0859's two dangling `related=` references and its referential-closure test,
R-0858's F267 repair as the `Note: F275 R23` entry re-measures it, R-0843's `Groups` table
in `docs/system/architecture.md`, and R-0868's retirement of `cluster_deletion_map.txt`,
`test_cluster_deletion_map.py`, `test_cluster_deletion_order.py` and
`.agent/f275_deletion_order.md`.

ALTERNATIVES CONSIDERED. (i) Exceed the block cap — rejected on the cap, which is a
measurement and not a preference. (ii) Draft D3 with the enumerations replaced by pointers
to the findings — rejected because five of the clauses order the ids NAMED in D3, and a
paragraph that cites where the list lives is not the list. (iii) Split D3 itself across two
decisions — rejected because the whole value of the deletion paragraph is that one place
holds the whole mapping.

HOW TO REVERSE: delete this decision; the clauses then bind whichever single round a later
relay chooses, and nothing on disk needs to change.
<<<END DEC23>>>

<<<BEGIN LANDED23>>>
Landed: R-0870 — both falsified comments repaired in C4 of F275 round 23: `packages/common/public_text_redaction.py` names the deletion instead of the vanished path, and `packages/orchestration/decision_evidence.py` drops the vanished type and keeps the surviving one.
<<<END LANDED23>>>

P1 — packages/common/public_text_redaction.py — REWRITE
<<<BEGIN P1 FROM>>>
the Provider Trust Gate (`packages/orchestration/provider_trust.py`, R-0083: never echo
a secret value or an absolute path out of untrusted provider text). Seven modules that
<<<END P1 FROM>>>
<<<BEGIN P1 TO>>>
the Provider Trust Gate, in a module F275 round 22 deleted at `0242c0a3` (R-0083: never
echo a secret value or an absolute path out of untrusted provider text). Seven modules that
<<<END P1 TO>>>

P2 — packages/orchestration/decision_evidence.py — REWRITE
<<<BEGIN P2 FROM>>>
#: the two nearest existing types,
#: ``provider_trust_verification.ProviderVerificationEvidenceRef`` and
#: ``orchestrator_brain.OrchestratorEvidenceRef``, both state their vocabulary
#: only in a trailing ``#`` comment, so nothing can validate against either.
<<<END P2 FROM>>>
<<<BEGIN P2 TO>>>
#: the nearest existing type, ``orchestrator_brain.OrchestratorEvidenceRef``,
#: states its vocabulary only in a trailing ``#`` comment, so nothing can
#: validate against it.
<<<END P2 TO>>>

P3 — tests/cli/test_product_spine.py — REWRITE
<<<BEGIN P3 FROM>>>
            "test_smoke_scripts.py",
            "test_overnight_executor_cli.py",
        ]
<<<END P3 FROM>>>
<<<BEGIN P3 TO>>>
            "test_smoke_scripts.py",
        ]
<<<END P3 TO>>>

P4 — tests/cli/test_mission_cmd.py — REWRITE
<<<BEGIN P4 FROM>>>
        assert "packages.orchestration.overnight_readiness" not in source
        assert "from packages.orchestration.mission_readiness import" in source
<<<END P4 FROM>>>
<<<BEGIN P4 TO>>>
        assert "from packages.orchestration.mission_readiness import" in source
<<<END P4 TO>>>
