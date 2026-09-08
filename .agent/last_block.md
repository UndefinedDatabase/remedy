── STEP T001/5 — F275 ────────────────────────────────
Goal:        Derive and record the deletion ORDER operator RULE 2 requires before the first `git rm`, with the ratchet that keeps it true; rule the atomic unit in a DECISION, because the cluster's internal import graph is CYCLIC and RULE 2's wording is unsatisfiable at module granularity; and discharge the route-policy knob check the same ruling pairs with it.
Bundle:      C0a save block · C0b mirror block · C1 plan · C2 book round 4 PASS, confirm R-0831, append two prose slips · C3 the order file and its ratchet · C4 DECISION F275 D2 · C5 gates (writes no file) · C6 handback
Change:      EXACTLY these eleven paths and nothing else —
             `.agent/authored/f275-r5.md`, `.agent/last_block.md`, `.agent/plan.md`,
             `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/decisions.md`,
             `.agent/f275_deletion_order.md`,
             `tests/orchestration/test_cluster_deletion_order.py`, `.agent/handoff.md`.
             That list is NINE paths; no production file under `packages/` or `apps/` is touched.
Constraints: below, numbered 1 to 9.
Done when:   the eight gates G1 to G8 below all report exit 0, with G8 last.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────

WHAT THIS ROUND IS, AND THE MEASUREMENT THAT SHAPED IT. Operator ruling amend0908-f275-finish
RULE 2 orders the deletion to proceed "in dependency order — leaf modules first, the modules they
import last — so that each group commit leaves no dangling import", derived from the map and
written into `.agent/f275_deletion_order.md` BEFORE the first `git rm`. The reviewer performed
that derivation at `a040b60c` and found the cluster's internal import graph is CYCLIC: a
topological order over single modules is IMPOSSIBLE, and a first attempt needed twelve cycle
breaks and left twelve modules deleted after something that imports them. Three cycles exist —
`provider_trust` ↔ `provider_trust_verification`, a four-module cycle around `builder_routing`,
and a six-module cycle around `dogfood_run`. The reviewer confirmed one of them by reading the
source rather than trusting the walker: `provider_trust.py` imports from
`provider_trust_verification` inside a function body, and `provider_trust_verification.py`
imports from `provider_trust` at module level — both real, executable imports.

So RULE 2's "leaf modules first" is unsatisfiable as literally worded, and this round rules the
atomic unit to be the STRONGLY CONNECTED COMPONENT: one module wherever the graph is acyclic, the
whole cycle where it is not. That reading is the only one consistent with all three operator
rules at once — RULE 1's "a half-deleted module is the state this work must not leave behind",
RULE 1's requirement that the tree is green after every group commit, and RULE 3's ban on stubs
and shims. It is recorded as DECISION F275 D2 rather than referred to the operator, because
§4.7 makes a dated, reversible DECISION the instrument for exactly this. Over components the
order is clean: fifteen components covering all twenty-four modules, ZERO cross-component
violations, and stable across twelve consecutive derivations.

NO PRODUCTION FILE IS TOUCHED and nothing is deleted. This round writes the plan for the deletion
and the guard that keeps that plan honest; the first `git rm` is the NEXT round's.

────────────────────────── CONSTRAINTS ──────────────────────────

1. NO SLICE IS EDITED. Every authored text is applied byte for byte. If a slice looks wrong,
   apply it anyway and DECLARE it in the handback's deviations.

2. C0a and C0b are `shutil.copyfile` from `.remedy-wt/f275-r5-FINAL.md` — NEVER retyped — to
   `.agent/authored/f275-r5.md` and `.agent/last_block.md`.

3. C1 IS THE FIRST SUBSTANTIVE COMMIT; only C0a and C0b may precede it (§3 item 23).

4. C3's TWO FILES ARE WHOLE NEW FILES AND TRAVEL BY `shutil.copyfile`, NEVER BY RETYPING:
     `.remedy-wt/f275-r5-ORDER.md` → `.agent/f275_deletion_order.md`
       410360ec0225340aff2bf4ff61d743598500d21d105c37e3e55b72a21a65fed4 · 2714 bytes · 41 lines
     `.remedy-wt/f275-r5-TEST.py`  → `tests/orchestration/test_cluster_deletion_order.py`
       a80d4c9610cc89afb2cf2eb6bd9d56d5e31745dcc0d4644f6649f75efefbf1f7 · 7792 bytes · 185 lines
   Verify each digest and byte count BEFORE copying and again after. A 185-line test retyped is a
   185-line test with a typo in it; the copy is the proof and the digest is the gate.

5. C3 IS ONE COMMIT. The ratchet and the file it ratchets land together: a test whose subject
   does not exist yet reds, and an order file nothing measures is precisely the artefact
   `tests/orchestration/test_cluster_deletion_map.py` names in its own docstring as having told
   three consecutive features this deletion was cheap.

6. NOTHING UNDER `packages/`, `apps/` OR `docs/` CHANGES. No module is deleted, no import is cut,
   no catalog entry moves. `tests/orchestration/cluster_deletion_map.txt` and
   `tests/orchestration/import_reachability_allowlist.txt` are NOT touched — G8 gates all three
   of those files byte-identical to their blobs at `a040b60c`.

7. THE ORDER FILE IS GENERATED OUTPUT, NOT PROSE. Its component lines were produced by the
   derivation `tests/orchestration/test_cluster_deletion_order.py` ships as `measured_order()`,
   not typed by hand. Do not reflow, re-sort or "tidy" them; the ratchet compares them literally.

8. THIS ROUND ADDS A TEST THE OPERATOR DID NOT ORDER, AND THAT IS A DELIBERATE, DECLARED CHOICE.
   RULE 2 orders a FILE. The reviewer adds `tests/orchestration/test_cluster_deletion_order.py`
   beside it because this repository's own precedent — F274 building
   `test_cluster_deletion_map.py` for the identical reason — and that module's own docstring both
   say an unmeasured inventory is what misled three features. It is recorded in DECISION F275 D2
   so the operator can reverse it by deleting one file and one paragraph. If the operator would
   rather have the bare file, that reversal costs nothing and loses nothing else.

9. PAIR SHAPES (§3 items 4 and 15). This round authors NO FROM/TO pair: C1 is a whole-file
   replacement, C2 and C4 are appends, and C3 is two whole new files. There is nothing to
   classify, so no containment test is ordered and no APPEND/REWRITE label appears anywhere.
   EVERY SEPARATOR LINE IN THIS BLOCK'S FRAME IS A RUN OF EXACTLY 54 `─` CHARACTERS (§3 item 37),
   stated because a run has no length a reader recovers by eye.

────────────────────────── C1 — THE PLAN ──────────────────────────

Replace the WHOLE of `.agent/plan.md` with the text between the markers. The marker lines
themselves are NOT part of the file.

<<<BEGIN PLAN5>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 5 books round 4's PASS, confirms R-0831's measurement still holds, and writes the
DELETION ORDER operator RULE 2 requires before the first `git rm`, with a ratchet holding it
against the live import graph. The cluster's internal graph is CYCLIC, so the atomic unit is
the strongly connected component — fifteen of them over twenty-four modules — which DECISION
F275 D2 rules and records. No production file is touched and nothing is deleted.

## Next Steps

1. The FIRST module groups, in the recorded order, one commit each: `context_optimizer`, then
   `review_bundle`. Each commit takes the module, its handler, its catalog entries, its
   cockpit section, its tests and its map lines together, and leaves the tree green.
2. The remaining thirteen components in the recorded order, the three multi-module ones deleted
   as single commits because their members import each other.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831 and
   R-0840 named among the ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- 66 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only, so a consumer coupled to the cluster
  by EVENT NAME is invisible to both the map and the deletion order. The order is a safe
  sequence for imports and is not a completeness claim about couplings.
- The full suite must be run in the PRIMARY checkout: a fresh worktree has no
  `apps/ui/node_modules`, so `test_test_runner.py`'s vitest node fails there for the
  environment rather than for the change.
<<<END PLAN5>>>

────────────────────────── C2 — THE RECORD AND THE SLIPS ──────────────────────────

ONE commit, two files.

(i) APPEND the two paragraphs between the RECORD5 markers to `.agent/live_review.md`, preceded
by a single `\n` and followed by exactly one newline. They are TWO blank-line units — the round
4 gate entry, then the R-0831 confirmation. The file is 527075 bytes before this commit.

(ii) APPEND the two paragraphs between the SLIPS5 markers to `.agent/prose_slips.md` the same
way: one leading `\n`, the text, one trailing newline. That file is 168666 bytes before this
commit. Both are reviewer-prose defects of ROUND 4 that left nothing wrong on disk, so under
amend0827 rule 2 they are dated lines and NOT ids.

IF ANY FORMULA IN THIS BLOCK DISAGREES WITH THE OPERATION ORDERED HERE, THE OPERATION WINS and
the disagreement is declared. Round 3 lost a deviation to exactly that and round 4 caught it.

<<<BEGIN RECORD5>>>
Gate: F275 R4 — the F275 round 4 entry. VERDICT PASS, booked by round 5 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier was the round 4 handback committed at `d6c8deb1` with the verdict appended at `a040b60c`. Range `280fd101`..`d6c8deb1`, seven commits — C0a, C0b, C1, C2, C3, C4, C6 — every one single-parent, no C5 commit because C5 writes no file. THE CHANGE SET IS EXACTLY THE ELEVEN PATHS the block named, and the reviewer re-ran every gate itself against the COMMITTED blobs. THIS ROUND COMPLETED BOTH CARRY-OVERS F260's DESIGN ORDERS BEFORE THE FIRST `git rm`: `mission readiness` landed in round 3 and `mission report` here, the second onto a name that was not free. DECISION F274 D2's coupling was honoured exactly — the carry-over and the death of the old holder are ONE commit, `d045eaf6`, so at no commit boundary did two handlers claim `mission.report` or the catalog name a handler nothing provided. G1 TRANSPORT covers the chain this workflow can walk, per §3 item 37, and not the emitted bytes: scratch original, `.agent/authored/f275-r4.md` and `.agent/last_block.md` all 36589 bytes at `bbbb408cf1971d2ffb34af15d626b61b0b0f51132de733ff7e8de7bc816ce260`. G2: `.agent/plan.md` byte-identical to PLAN4 at 2362 bytes and 41 lines. G3 THE RECORD: `.agent/live_review.md` 519228 to 527075, gain 7847 = 1 + 7845 + 1, pre-blob an exact PREFIX, RECORD4 plus one newline an exact SUFFIX, blank-line separated; units 216 to 218, `^Gate: ` 25 to 26, `^Gate: F275 R3 ` 0 to 1, `^- R-0840 — ` 0 to 1, OPEN SET 65 TO 66 BY DISTINCT ID over DISTINCT ids and never over the 5 `Done:` LINES; `.agent/prose_slips.md` 168030 to 168666 with prefix and suffix exact. G4: C3's real numstat is 7/4, 28/0, 0/27 and 2/38, and in `apps/cli/commands/worker_facade_cmd.py` the dead symbols `_cmd_mission_report` and `build_mission_morning_report` each went 2 to 0 while `packages.orchestration.dogfood_run` went 3 to 2 — the import site that died is the handler's, and the two that survive are `mission run`'s. `packages/orchestration/dogfood_run.py` and `packages/orchestration/mission_readiness.py` are BYTE-IDENTICAL to their blobs at `280fd101`. G5: the deletion map is UNCHANGED at 19 edges over 10 modules with the `dogfood_run <- worker_facade_cmd.py` edge still present — an EQUALITY gate on purpose, because a shrinking map here would have meant more was deleted than was asked for. G6: the parser reaches `mission report` with a `job_id` and a `--markdown` flag, the facade no longer provides the id, and the `overnight.report` and `mission.report` payloads are 1225 characters each differing in `generated_at` ALONE. G7: 146 · 650 · 93 · 42, all exit 0 — down exactly two where the deleted handler's tests died with it, up exactly five where C4 added five, unmoved on the cluster builder's own suite and on the canary. G8: tree clean, no `.agent/STOP`, one worktree, branch pushed. FIVE DEVIATIONS WERE DECLARED. DEVIATION 4 IS DECLINED ON A MEASUREMENT: the worker flagged that RECORD4 and PLAN4 call `packages.orchestration.overnight_readiness` DELETABLE at zero consumer edges while six live import sites remain in three production files, and raising it was correct, but the claim is TRUE as written and the word carrying it is SURVIVING — `apps/cli/commands/overnight_cmd.py` is in `CLUSTER_COMMAND_HANDLERS` and `review_bundle` and `overnight_executor` are both in `CLUSTER_MODULES`, and operator RULE 2 says of exactly this case that such an importer "is deleted WITH its target and never counted as a blocking edge". The worry that a later round could break three production files is answered by RULE 1: each dies inside its own module-group commit. Nothing on disk needs repair and no id is minted. DEVIATION 2 IS THE BLOCK WORKING AS DESIGNED: G3(a) told the worker that where a formula and the ordered OPERATION disagree the OPERATION wins and the disagreement is declared, and the operation produced 527075, the only value under which the exact-SUFFIX reading can hold. DEVIATIONS 1 AND 3 ARE THE REVIEWER'S OWN PROSE and are dated `.agent/prose_slips.md` lines rather than ids, per amend0827 rule 2, because neither left anything wrong on disk. NO FINDING IS RESOLVED BY THIS GATE and none is minted here; R-0840 was minted by round 4's own C2.

- R-0831 CONFIRMED, NOT RESOLVED, at `a040b60c` — the route-policy knob check operator ruling amend0908-f275-finish pairs with the carry-overs is now DISCHARGED as a check, and its answer is unchanged. That ruling says the knobs "are checked against F110's config keys (R-0831 already records that none has an equivalent, so this is a finding update, not a rebuild)". THE RE-MEASUREMENT, taken by the reviewer at `a040b60c` over the two modules F260's Design names: all eight knobs R-0831 lists — `prefer_local_for_cheap_tasks`, `prefer_ollama_for_cheap_tasks`, `preferred_worker_ids`, `user_selected_worker_ids`, `prefer_local_advisor`, `require_human_approval`, `risk_tier` and `default_autonomy_ceiling` — occur ZERO times in `packages/orchestration/role_config.py` and ZERO times in `packages/orchestration/model_routing.py`, both of which still exist on disk. That is the same reading R-0831 recorded at `4ba5e0f6df26fbf0ed791f1eaa4d072d722802a6`, re-taken 46 commits later against a tree that has since gained both carry-overs. So every one of the eight still falls on F260's "missing knob" branch, F260's own rule "never rebuild" continues to bind, and NOTHING IS OWED IN CODE. R-0831 STAYS OPEN and its original text is not rewritten: what resolves it is unchanged and is the deletion round deleting these knobs with their modules while DECISION F260 D3 names route policy among the ideas deleted rather than inherited. This paragraph exists so that the ordered check has a dated answer on the record rather than being discharged silently, and so the deletion round can cite a confirmation taken after the carry-overs rather than before them.
<<<END RECORD5>>>

<<<BEGIN SLIPS5>>>
2026-09-08 · F275 R4 · The round 4 block's gate G7 suite 3 gave `tests/orchestration/test_dogfood_run.py` a BASE of 135, which was the COMBINED count of that suite and the canary from the reviewer's own paired dry run; the suite alone is 93, the worker re-measured 93 at the base `280fd101` and 93 again at the round's own tip, and the no-regression property the gate exists for held exactly.

2026-09-08 · F275 R4 · The round 4 block's constraint 9 lettered the pairs (a), (b), (d), (e) and the deletions (c), (f), (g) while its C3 labels the pairs (a), (b), (e), (f) and the deletions (c), (d), (g), leaving C3's registry-line deletion in neither list; the worker re-ran the containment test mechanically and reproduced all four classifications unchanged.
<<<END SLIPS5>>>

────────────────────────── C3 — THE ORDER AND ITS RATCHET ──────────────────────────

ONE commit, two WHOLE NEW FILES, both by `shutil.copyfile` per constraint 4. Neither file exists
at `a040b60c`; both are additions, so `git diff --numstat` reads them as pure insertions.

  `.remedy-wt/f275-r5-ORDER.md` → `.agent/f275_deletion_order.md`
  `.remedy-wt/f275-r5-TEST.py`  → `tests/orchestration/test_cluster_deletion_order.py`

WHAT THE ORDER FILE SAYS, so the worker can recognise a corrupted copy without reading the
derivation: 26 comment lines, then FIFTEEN component lines, each a comma-separated list of
dotted cluster module names, in deletion order. The first line is
`packages.orchestration.context_optimizer` and the last is
`packages.orchestration.provider_trust, packages.orchestration.provider_trust_verification`.
Three lines name more than one module: the six-module cycle around `dogfood_run` at line 3 of
the fifteen, the four-module cycle around `builder_routing` at line 5, and the
`provider_trust` pair at line 15. Twenty-four modules in total, each named exactly once.

WHAT THE TEST DOES: it imports the ONE first-party walker this repository keeps, rebuilds the
cluster's internal dependency graph, computes the strongly connected components with Tarjan
walking every neighbour set SORTED so the result is stable, condenses them, and orders the
condensation with importers first and ties broken by the component's own sorted module names.
It then asserts three things — the recorded order EQUALS the measured one; no module is deleted
before a module it imports; and every cluster module still on disk appears exactly once. The
reviewer measured the derivation as STABLE ACROSS TWELVE CONSECUTIVE RUNS at `a040b60c`, which
is why a ratchet over it is safe: an order that flapped would red for no reason and be turned off
within a round.

────────────────────────── C4 — THE DECISION ──────────────────────────

APPEND the text between the markers to `.agent/decisions.md`, preceded by a single `\n` and
followed by exactly one newline. It is ONE blank-line unit. The file is 927408 bytes before this
commit. `^## DECISION F275 D` goes from 1 to 2 and `^## DECISION F275 D2 ` heads exactly one
section.

<<<BEGIN DECISION5>>>
## DECISION F275 D2 — the atomic unit of the cluster deletion is the strongly connected COMPONENT, because the cluster's internal import graph is cyclic (2026-09-08)

CONTEXT. Operator ruling amend0908-f275-finish RULE 1 makes "one module group" the atomic unit of the deletion and requires the tree green after every group commit. RULE 2 orders the sequence: "The deletion proceeds in dependency order — leaf modules first, the modules they import last — so that each group commit leaves no dangling import. The deletion order is derived from the map by the first round of this slice and written into `.agent/f275_deletion_order.md` before the first `git rm`." This round is that first round, and performing the derivation surfaced a fact none of F260, F272 or F274 had recorded.

THE MEASUREMENT, taken by the reviewer at `a040b60c` over the twenty-four modules `tests/orchestration/test_cluster_deletion_map.py` names as `CLUSTER_MODULES`, using the same first-party `ast` walker the map uses. The cluster's INTERNAL import graph — cluster module importing cluster module — is CYCLIC. A topological sort over single modules is therefore impossible: a first attempt required TWELVE cycle breaks and produced an order in which twelve modules were deleted after a module that imports them, which is exactly the dangling import RULE 2 exists to prevent. There are three cycles. `packages.orchestration.provider_trust` and `packages.orchestration.provider_trust_verification` import each other. A four-module cycle joins `builder_routing`, `candidate_quality`, `local_candidate_generator` and `model_route_tournament`. A six-module cycle joins `dogfood_run`, `feature_planner`, `overnight_mission`, `progress_ledger`, `repair_loop_v2` and `self_repair_proposal`. The reviewer verified one cycle by READING THE SOURCE rather than trusting the walker: `packages/orchestration/provider_trust.py` imports from `provider_trust_verification` inside a function body — the usual dodge for a circular import at module load — and `packages/orchestration/provider_trust_verification.py` imports from `provider_trust` at module level. Both are real, executable imports, so the cycle is a property of the code and not an artefact of static analysis.

CHOSEN. The atomic unit of the deletion is the STRONGLY CONNECTED COMPONENT of the cluster's internal import graph: a single module wherever that graph is acyclic, and the entire cycle in ONE commit where it is not. Over components the order is well defined — fifteen components covering all twenty-four modules, with ZERO cross-component violations, stable across twelve consecutive derivations. `.agent/f275_deletion_order.md` records that order, one component per line, and `tests/orchestration/test_cluster_deletion_order.py` holds it against the live graph in the same way `test_cluster_deletion_map.py` holds the map.

WHY, and why this is a ruling rather than a question to the operator. RULE 2's "leaf modules first" is unsatisfiable AS LITERALLY WORDED against a cyclic graph, so some reading has to be chosen before the first `git rm`. Only one reading satisfies all three operator rules at once. Deleting a cycle member alone leaves its partner importing a deleted module, which breaks RULE 1's "the tree is green after every group commit" and leaves precisely the half-deleted state RULE 1 names as the thing this work must not leave behind. Keeping a shim or a temporary re-export to break the cycle is forbidden by name in RULE 3 and in AGENTS.md's Scope Control. Deleting the whole cluster in one commit would abandon the group granularity RULE 1 exists to give. The component reading keeps every rule: it is the SMALLEST unit that can be deleted without a dangling import, it degenerates to RULE 1's single module wherever the graph allows, and it changes the sequencing without weakening a single guarantee. Under docs/agents/planner_reviewer_prompt.md §4 item 7 a dated, reversible DECISION is the instrument for exactly this, and the reviewer does not stop a session to ask what the rules already answer.

ALTERNATIVES CONSIDERED AND REJECTED. (1) Break each cycle by deleting the function-local import first, in its own commit, then order the modules normally — rejected because it edits a module that is about to be deleted, spending a commit and a review on code with hours to live, and because it does not generalise: the four- and six-module cycles are joined at module level, not by a single dodgeable import. (2) Order by number of importers and accept the dangling imports for one commit — rejected outright; it makes the suite red at a commit boundary, which RULE 1 forbids. (3) Ask the operator — rejected under the standing practice that a rule the existing rules determine is ruled here and recorded, not relayed.

CONSEQUENCE. The deletion is FIFTEEN group commits and not twenty-four. Three of them delete more than one module and are correspondingly larger, though all three are pure deletions and so cannot approach the DECISION F104 D1 insertion cap. The order file and its ratchet are maintained exactly as the map is: a group commit removes its modules from `.agent/f275_deletion_order.md` in the SAME commit that removes them from disk, and the ratchet reds if it does not. This ruling says NOTHING about event-name couplings, which R-0832 records as invisible to the import map and therefore invisible to this order too; the order is a safe sequence for IMPORTS and is not a completeness claim.

REVERSE by deleting this section, `.agent/f275_deletion_order.md` and `tests/orchestration/test_cluster_deletion_order.py`. The deletion then has no recorded order and RULE 2's derivation is owed again by whichever round next approaches the first `git rm`. Reversing ONLY the test, and keeping the file as the plain inventory RULE 2 literally asks for, costs nothing else and is the narrower reversal if the operator would rather not carry the guard.
<<<END DECISION5>>>

────────────────────────── C5 — THE GATES ──────────────────────────

Run ALL EIGHT at C5, after C4 and STRICTLY BEFORE the C6 handback commit (§3 item 31). C5 writes
no file and has no commit. Report ONE LINE PER GATE with the REAL exit code. A gate that cannot
be run is reported as not run — never as green.

EVERY GATE BELOW WAS RUN BY THE REVIEWER AT THE BASE `a040b60c` BEFORE EMISSION, and each carries
its BASE reading beside its expected one, per the procedure R-0819's recurrence paragraph
strengthened from a clause. Non-discriminating readings are labelled. R-0741's fix clause is
DECLINED AS NOT APPLICABLE on its own terms — it binds "the next block that orders such a set",
and this block orders no grep-derived leave-alone set.

G1 TRANSPORT. sha256 and byte count of `.remedy-wt/f275-r5-FINAL.md`, of the committed
`.agent/authored/f275-r5.md`, and of the committed `.agent/last_block.md`. All three must be ONE
value. Per §3 item 37 this covers the chain this workflow can walk — saved copy, mirror, working
copy — and NOT the bytes the reviewer emitted; do not claim more.

G2 THE PLAN. `.agent/plan.md` byte-identical to PLAN5. Report its sha256, byte count, line count
(under the AGENTS.md cap of 50), and that `^## Goal$` and `^## Next Steps$` occur once each.

G3 THE RECORD. Six parts over `.agent/live_review.md`, plus one byte-equality reading for
`.agent/prose_slips.md`, which is a `.agent/` prose file and earns no more under the gate budget.
  (a) BYTES: 527075 before; after = the result of the C2(i) operation. State both.
  (b) EXACT EDGES: pre-commit blob a byte-exact PREFIX; RECORD5 a byte-exact SUFFIX. Both booleans.
  (c) ORDERED EQUALITY by an independent paragraph reader: the LAST N blank-line units of the
      whole file against RECORD5's N paragraphs IN ORDER, N COUNTED FROM THE SLICE by your script
      and never taken from this block. Report N and the per-unit sha256 pairs.
  (d) NEGATIVE CONTROL on the FIRST appended paragraph, in scratch or memory only: flip one byte
      and confirm BOTH the reader of (b) and the reader of (c) REJECT it. Re-read the tracked file
      afterwards and report its byte count.
  (e) COUNTS: blank-line units 218 → 220; `^Gate: ` 26 → 27; `^Gate: F275 R4 ` 0 → 1.
  (f) THE OPEN SET DOES NOT MOVE: distinct `^- R-\d+ — ` ids 69 → 69, distinct `^Done: R-\d+ — `
      ids 3 → 3, OPEN SET BY DISTINCT ID 66 → 66. Subtract DISTINCT IDS, never the 5 `Done:`
      LINES. The R-0831 paragraph is a CONFIRMATION, not a registration and not a resolution:
      it opens `- R-0831 CONFIRMED` and so matches neither `^- R-\d+ — ` nor `^Done: R-\d+ — `.
      Report the count of `^- R-0831 CONFIRMED` as 0 → 1 to show it landed.
  (g) `.agent/prose_slips.md`: 168666 before; after = the result of the C2(ii) operation; the
      pre-blob an exact PREFIX and SLIPS5 an exact SUFFIX. Two readings and no more.

G4 THE TWO NEW FILES ARE THE REVIEWER'S BYTES. For each of `.agent/f275_deletion_order.md` and
`tests/orchestration/test_cluster_deletion_order.py`: sha256 and byte count of the committed blob
equal to the scratch original's, as constraint 4 states them. Then `git ls-tree a040b60c -- <path>`
must be EMPTY for both, proving they are additions and not overwrites. Then
`python3 -m ruff check tests/orchestration/test_cluster_deletion_order.py` exit 0 and `ast.parse`
clean. BASE reading: both paths absent at `a040b60c`, so this gate is unmeetable there.

G5 THE DECISION. Over `.agent/decisions.md`: 927408 bytes before, and after = the result of the
C4 operation; the pre-blob a byte-exact PREFIX and DECISION5 a byte-exact SUFFIX; a negative
control flipping one byte inside the appended paragraph REJECTED by both readers, in scratch or
memory only; `^## DECISION F275 D` 1 → 2 and `^## DECISION F275 D2 ` exactly 1.

G6 THE RATCHET IS REAL, AND BOTH CONTROLS RUN IN A DISPOSABLE WORKTREE, NEVER THE PRIMARY
CHECKOUT (guardrail G5). Green first, in the primary checkout: `python3 -m pytest
tests/orchestration/test_cluster_deletion_order.py tests/orchestration/test_cluster_deletion_map.py
tests/orchestration/test_import_reachability.py -q` exit 0 at 9 passed. Then in the worktree:
  control 1 — SWAP the `packages.orchestration.overnight_readiness` line with the
  `packages.orchestration.overnight_executor` line in the order file and re-run the order test
  ALONE. It must FAIL, and its message must name
  `overnight_executor imports ... overnight_readiness, but ... overnight_readiness is deleted first`.
  control 2 — restore that swap, then DELETE the `packages.orchestration.context_pack` line and
  re-run. It must FAIL naming `packages.orchestration.context_pack` as on disk but not in the order.
Report all four exit codes, then remove the worktree BY ITS EXACT PATH and show `git worktree list`
holding only the primary checkout. The reviewer measured all four at `a040b60c`: green, then
2 failed / 1 passed on control 1 and 2 failed / 1 passed on control 2, with exactly those messages.

G7 THE SUITES, IN THE PRIMARY CHECKOUT and each run ALONE. `apps/ui/node_modules` is gitignored,
so `test_test_runner.py`'s vitest node fails in any fresh worktree for the ENVIRONMENT rather than
for the change — the reviewer hit exactly that at `a040b60c` and it is why this gate names the
checkout. Report the real exit code and passed count for each:
  1. `python3 -m pytest tests/orchestration/ -q`
     BASE 12886 passed with 10 skipped, expected 12889 with 10 skipped — DISCRIMINATING UPWARD by
     exactly the three tests C3 adds, counted from the test file and not asserted from memory.
     The reviewer took that base reading in the PRIMARY CHECKOUT at `a040b60c`, where the vitest
     node passes; the same command in a fresh worktree reports one failure and a count three
     higher, which is the environment and the not-yet-committed test file, not the tree.
  2. `python3 -m pytest tests/docs/ tests/test_test_categories.py -q`
     BASE 315, expected 315 — NO-REGRESSION, and the gate for "a new test file trips no pin".
  3. `python3 -m pytest tests/cli/test_golden_path.py -q`
     BASE 42, expected 42 — the canary, NO-REGRESSION.

G8 THE TREE AND THE UNTOUCHED FILES. All of: `.agent/STOP` does not exist; `git status
--porcelain` is EMPTY; the branch is `feature/f275-one-world-completion-part-three`; `git worktree
list` shows ONLY the primary checkout; `git diff --name-only a040b60c..HEAD` names NOTHING under
`packages/`, `apps/` or `docs/`; and `tests/orchestration/cluster_deletion_map.txt`,
`tests/orchestration/import_reachability_allowlist.txt` and
`packages/orchestration/overnight_readiness.py` are each BYTE-IDENTICAL to their blobs at
`a040b60c` — read them with `git show a040b60c:<path>` into memory or gitignored scratch, never by
overwriting the tracked file (§3 item 29). Finally `git log --oneline` over this round's range
shows C0a, C0b, C1, C2, C3, C4 in that order, each single-parent. C6's OWN numbers are ordered
NOWHERE: under docs/agents/self_drive_protocol.md there is no second window, so a value routed to
a "round report" ends with the session (§3 item 31). The REVIEWER measures C6's commit at the next
gate and records it in that round's ledger entry. Do not guess them.

────────────────────────── C6 — THE HANDBACK ──────────────────────────

Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`. NO length cap (amend0827 rule
3); valid when its mandated sections are present. It MUST carry: the state block naming FEATURE
F275, ROUND 5, SESSION 2, the branch, the base `a040b60c` and every commit SHA; the changed-files
table with the REAL `git diff --numstat` columns per commit, taken from the tool and not
re-derived (§3 item 28); ONE LINE PER GATE with its real exit code, plus the G3, G4, G5, G6 and G7
transcripts; the open-findings count (66 by distinct id, UNCHANGED — this round mints none and
resolves none); the item-status table covering C0a, C0b, C1, C2, C3, C4, C5, C6 and G1 to G8
exactly once each; the deviations; the Fortschritt line below verbatim; ONE SENTENCE of context
self-assessment per amend0905-throughput; and the next expected action — the FIRST module group
commit, `context_optimizer`, taking its module, handler, catalog entries, cockpit section, tests
and map lines together. Write NO verdict: the verdict is the reviewer's.

Fortschritt: ~34 % (T001: Claim ✅ · Record ✅ · D1 ✅ · Carry-over readiness ✅ · Carry-over
report ✅ · R-0831 geprüft ✅ · Löschreihenfolge ✅ · D2 ✅ · Löschung offen (15 Gruppen) ·
F260 D3 offen · T002 offen · T003 offen) — Schätzung
