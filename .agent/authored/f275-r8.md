── STEP T001 · module group 3 · F275 ROUND 8 ──
Goal:        Book round 7's PASS, register R-0841 and R-0842, rule DECISION F275 D4, and
             delete the `context_pack` module group together with the surviving readers that
             were coupled to it by EVENT NAME rather than by import, leaving the tree green.

Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the ledger and the slips ·
             C3 the decision · C4 the deletion · C5 the `Landed:` line · gates · C6 the handback.

WHY THIS ROUND IS NOT A DELETION ROUND. Operator amendment amend0906-triage-throughput defines
a deletion round as one whose change set holds no EDITED line under `packages/`, `apps/` or
`tests/`, and grants it a four-measurement shortcut. This round edits lines in all three, so
the shortcut does not apply and it is gated as a production-code round: a ratchet red-proof in
a disposable worktree, and the full suite run serially in the primary checkout. DECISION F275
D4, which C3 lands, records that reasoning and the measurement behind it.

WHAT THE REVIEWER MEASURED BEFORE WRITING THIS, all of it in a disposable worktree at
`65409e647b04939746ff010a687c48621022b9e3`, with the whole change set APPLIED and COMMITTED
before a line of this block was authored. `context_pack_created` is emitted at exactly ONE
site in the tracked tree and that site dies with this group, so every reader of the event is
dead the moment the commit lands. The full suite is EXIT 0 at 19728 passed and 23 skipped,
down 32 from the base's 19760, and that 32 equals the fall in `--collect-only` over the five
affected test files, 317 to 285 — so every deleted test is accounted for and nothing else
moved. Through the SHIPPED readers `apps.cli.commands.collect_all_handlers` and
`apps.cli.command_catalog._BASE_CATALOG` both fall 336 to 335, which is the one deleted
command. `ruff check packages/ apps/cli/ tests/` reads 24 at the base and 24 after, none of
them in a file this round touches.

THREE THINGS THE DRY RUN FOUND THAT AN IMPORTER SWEEP DID NOT, stated so the worker recognises
them rather than rediscovering them. FIRST, `tests/cli/test_context_inspect_cli.py` asserts
`"context.pack" in entry.related` on the SURVIVING `context.inspect` catalog entry, so the
catalog edit is not confined to the deleted entry. SECOND, `tests/test_remedy_smoke_script.py`
guards the smoke script as TEXT and one of its guards, `test_smoke_has_token_ordering`, sits
under a section header this round's own smoke edit empties. THIRD, `tests/conftest.py`,
`tests/orchestration/test_project_brain.py` and `tests/regression/test_named_bugs.py` each name
`context_pack.py` as a PATH they read from disk, so two of them raise `FileNotFoundError`
rather than fail an assertion once the file is gone.

Change set: EXACTLY these paths and nothing else.
  .agent/authored/f275-r8.md · .agent/last_block.md · .agent/plan.md · .agent/live_review.md ·
  .agent/prose_slips.md · .agent/decisions.md · .agent/f275_deletion_order.md ·
  .agent/handoff.md
  packages/orchestration/context_pack.py · packages/orchestration/project_brain.py ·
  packages/orchestration/brain_detail.py · packages/orchestration/brain_viewer.py ·
  packages/orchestration/brain_viewer_theme.py · packages/orchestration/ui_copy.py ·
  packages/orchestration/ui_view_model.py · packages/orchestration/ui_server.py
  apps/cli/commands/context_pack_cmd.py · apps/cli/commands/__init__.py ·
  apps/cli/command_catalog.py · apps/ui/src/api/humanizeCatalog.ts
  scripts/remedy_smoke.sh · docs/system/architecture.md
  tests/test_context_pack.py · tests/test_remedy_smoke_script.py ·
  tests/storage/test_persistence.py · tests/cli/test_context_inspect_cli.py ·
  tests/conftest.py · tests/orchestration/test_project_brain.py ·
  tests/regression/test_named_bugs.py · tests/orchestration/import_reachability_allowlist.txt ·
  tests/orchestration/test_cluster_deletion_map.py

WHAT MUST NOT BE TOUCHED. `docs/roadmap/features/T2_F260.md`, `T2_F272.md`, `T2_F274.md` and
`T2_F275.md` are the SPECIFICATION of what is being deleted and stay unedited on purpose, and
`T2_F260.md` line 341 legitimately names `context_pack.py` for that reason. The `context_pack`
PARAMETER of `build_builder_request_package` in `packages/orchestration/main_builder_adapter.py`
and its three test call sites are a DIFFERENT concept — a dict argument, not this module — and
that adapter is itself further down the deletion order; leave all four alone. Everything in
`packages/orchestration/token_economy.py` spelled `recommend_context_pack`,
`ContextPackRecommendation`, `context_pack_kind` or `context_pack_recommendation`, and
`build_repair_context_pack` in `packages/orchestration/repair_loop_v2.py`, are likewise other
concepts and survive untouched.

Constraints:
 1. Apply every authored slice BYTE FOR BYTE. A slice is never edited, reflowed, retyped or
    "corrected" — if one is wrong, apply it as given and DECLARE it in the handback.
 2. Commit order is fixed and load-bearing: C0a, C0b, C1, C2, C3, C4, C5, then the gates,
    then C6. C1 is the FIRST substantive commit, per planner_reviewer_prompt.md §3 item 23.
    C2 is the commit that registers R-0841 and R-0842 — every sentence in this block and in
    the slices that speaks of "the registrations" means that commit. C4 is the commit that
    performs the deletion, and C5 the one that records `Landed: R-0841`; R-0842's own text
    describes what C4 removes and is authored before C4 exists, which is the carve-out
    planner_reviewer_prompt.md §3 item 20 makes for a claim about the round's own change.
 3. C5 exists because §4 item 4 reserves `Done:` for reviewer-authored text. R-0841 is FIXED
    by C4, and a worker never writes its own resolution; it writes `Landed:` and the reviewer
    replaces it with `Done:` at the next gate. Do NOT write a `Done:` paragraph this round.
 4. All destructive verification — the G6 red-proof — runs ONLY in a disposable `git
    worktree`, per self_drive_protocol.md G5. `git status --porcelain` is EMPTY in the primary
    checkout at every commit boundary and at the handback.
 5. Re-read `.agent/STOP` from disk before C0a and again before C6. It does not exist as this
    block is written; if it appears, finish the commit in hand, write the handoff and end.
 6. The full suite runs SERIALLY in the PRIMARY checkout — never `-n auto`, which races the
    `ui_server` command-channel tests for a port, and never in a worktree, which has no
    `apps/ui/node_modules`.
 7. `.agent/f275_deletion_order.md` is REGENERATED by running the shipped `measured_order()`
    after steps (1) to (21) are on disk. Do not edit it by hand. Its `# ` comment header is
    kept verbatim and only the body below it is rewritten.
 8. Every gate is RUN and its REAL exit code reported. A gate that cannot be run is reported
    as not run. If a gate's prediction disagrees with a measurement, report the MEASUREMENT
    and declare the disagreement — three of round 7's gate clauses were the reviewer's own
    error and the worker was right to measure rather than comply.

The authored slices follow. Each is delimited by its own BEGIN and END marker lines and the
BEGIN marker carries the byte count and the sha256 of the slice's exact bytes, which are the
bytes BETWEEN the two marker lines. Verify each digest BEFORE applying it.

===BEGIN PLAN8 bytes=2614 sha256=a661322e908605f9a32cdfac351f2f9f56db43a2855f6734c028165a5611d434===
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 8 books round 7's PASS, registers R-0841 and R-0842, and deletes the THIRD module group,
`context_pack` — the module, its handler, its catalog entry, the brain-graph node that read its
event by NAME rather than by import, that node's detail renderer and its viewer, theme, copy and
edge-humanization entries, two dead `ui_server.py` readers, three smoke-script sections with
their guards, the surviving test call sites, one ist-doc section and its map lines. DECISION
F275 D4 rules that an event-coupled consumer dies in the same commit as the emitter that fed it.

## Next Steps

1. `review_bundle`, which this round's regeneration makes the order file's first line: 2254
   lines, sixteen surviving test importers, eight `docs/system/` pages, a `pyproject.toml`
   per-file ignore and list entry, and `scripts/remedy_test_runtime.sh`. It needs a session
   that can carry it whole, and DECISION F275 D3 keeps it deferred until one can.
2. The remaining components in the recorded order, the multi-module ones as single commits
   because their members import each other.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840 and R-0842 named among the ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 66 by distinct id at this round's base `65409e64`; the ledger commit this
  block fixes as C2 registers R-0841 and R-0842 and takes it to 68. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only. This is the first group whose
  surviving readers are coupled ONLY by event name, and an AST importer sweep saw none of
  them; they were found by reading the emitter's event string back out of the tree.
- The full suite is run SERIALLY. Under `pytest -n auto` the `ui_server` command-channel tests
  race for a server port and the vitest node needs `apps/ui/node_modules`.
===END PLAN8===

===BEGIN LEDGER8 bytes=9712 sha256=3976b5eb4bd5860ed97efa83c22643575407a9fbe4dec5614972dfb1a5d16c90===
Gate: F275 R7 — the F275 round 7 entry. VERDICT PASS, booked by round 8 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier is the committed and pushed `.agent/handoff.md` at `65409e647b04939746ff010a687c48621022b9e3`. Every gate was RE-RUN by the reviewer itself against the COMMITTED blobs; the worker's report was evidence for nothing. Range `d4402dc268f0786d25d5da341db08c7884efc807`..`ce671728` — seven single-parent commits C0a `dbefb640`, C0b `596c7780`, C1 `793f139f`, C2 `8f23fc41`, C3 `1e870c39`, C4 `2cb9d947` and C6 `ce671728`, with no C5 commit, each parent verified by `git rev-list --parents`, and `git diff --name-status` over that range naming EXACTLY the nineteen paths the block enumerates. THIS ROUND DELETED THE SECOND MODULE GROUP OF THE PROTOTYPE CLUSTER, `worker_recommend`, in ONE commit. G1 TRANSPORT: the reviewer's own scratch original, the committed `.agent/authored/f275-r7.md` and the committed `.agent/last_block.md` are all 35103 bytes at `32dbccc7104faa375e0a18a9f70b72fb8dd06dadb568a9890c72f285a3dc5413`; per docs/agents/planner_reviewer_prompt.md §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` byte-identical to PLAN7 at 2394 bytes and 41 lines, under the AGENTS.md cap of 50, with both mandated headings. G3 THE RECORD: `.agent/live_review.md` 536113 to 541694, gain 5581 = 1 + 5580; `.agent/prose_slips.md` 171102 to 172799, gain 1697 = 1 + 1696; for both the pre-image is a byte-exact PREFIX and one newline plus the slice a byte-exact SUFFIX, N counted from each slice by the reviewer's own reader as 1 and 4 with ordered paragraph equality holding, blank-line units 221 to 222 and 242 to 246, `^Gate: ` 28 to 29, `^Gate: F275 R6 ` 0 to 1, and THE OPEN SET UNCHANGED AT 66 BY DISTINCT ID. G4 THE DECISION: `.agent/decisions.md` 947292 to 953044, gain 5752 = 1 + 5751, both edges exact, N = 8 paragraphs in order, `^## DECISION F275 D` 2 to 3, and `^## DECISION F275 D3 ` heading exactly one section. G5: `git ls-tree` finds neither group file at the tip, and `worker.recommend` and `worker.explain` are at ZERO over the tracked tree. G6: the three ratchets 9 passed, the docs trio 345 passed, the canary 42 passed, and through the SHIPPED readers `apps.cli.commands.collect_all_handlers` and `apps.cli.command_catalog._BASE_CATALOG` the dispatch table and the catalog are BOTH 336 where the base measured 338, with `worker.recommend` and `worker.explain` absent and `worker.list` and `worker.show` present; the REGENERATED order file holds thirteen components with `context_pack` first, which a line edit could not have produced. G7: ruff `All checks passed!` over the six touched Python files, and the FULL SUITE RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT is EXIT 0 at 19760 passed and 23 skipped with ZERO failures — down EXACTLY EIGHT from round 6's 19768, which is the count of tests this round deletes. G8: `git status --porcelain` empty, one worktree, `.agent/STOP` absent, and per-commit insertions 385, 295, 17, 10, 16, 6 and 316, every one under the AGENTS.md DECISION F104 D1 cap of 500. EIGHT DEVIATIONS WERE DECLARED AND ALL EIGHT ARE SUSTAINED. THREE OF THEM ARE THE REVIEWER'S OWN GATE CLAUSES BEING WRONG and the worker measured each rather than reporting the number the block asked for: G5 ordered `recommend_worker` to ZERO while the same block's must-not-touch list keeps `docs/roadmap/features/T2_F272.md`, which contains it; G5 ordered the shell string `worker recommend` to ZERO in `scripts/` and `tests/` while one literal survives in a class docstring at `tests/storage/test_persistence.py`; and G5 predicted a seven-file survivor set where the true set is FIVE. All three are dated `.agent/prose_slips.md` lines rather than ids, per amend0827-process-diet rule 2, because not one put anything wrong on disk. A FOURTH DEVIATION IS THE WORKER'S APPLICATION BEING BETTER THAN THE REVIEWER'S: three of C4's twelve numstat cells exceed the reviewer's dry run by three to five deletions each, because the worker took every deleted unit together with its separating blank line where the reviewer's own AST prune left the blanks behind, which would have left a nine-blank run between two classes; the reviewer inspected the committed diff and confirms the worker's reading is the correct one, and the other nine cells reproduce exactly. ONE DEVIATION IS A REAL DEFECT ON DISK and is registered by this same commit as R-0841. NO FINDING IS RESOLVED BY THIS GATE. The open set stands at 66 by distinct id before the two registrations this commit carries.

- R-0841 — Low, TWO COMMENTS FALSIFIED BY THE ROUND 7 DELETION SURVIVE ON DISK UNDER `tests/`. Raised by the reviewer at the F275 round 7 gate and booked by round 8's ledger commit. `tests/test_remedy_smoke_script.py` still carries the section header `# --- Step 64: Worker show + explain (steps 12v-12w) ----------------------` while section 12w and the `remedy worker explain` call it named were deleted from `scripts/remedy_smoke.sh` in the same commit `2cb9d9473cc692f5d19404f8c191d495dfabb294`, and the guard test that read it was deleted beside it; the `remedy_smoke.sh` sibling of that heading WAS repaired, because the round 7 block's step (4)(c) named it, and this one was not, because step (5) enumerated three function names without naming the section comment above them. `tests/storage/test_persistence.py` still carries the class docstring `"""Token Economy v1 — context pack modes, worker recommend."""` on a class whose worker-recommend half that commit removed. Both readings were taken at `2cb9d9473cc692f5d19404f8c191d495dfabb294`. Neither comment is executable and neither changes a result, so this is LOW; it is an id rather than a `.agent/prose_slips.md` line because the wrong state is on disk under `tests/` rather than in the reviewer's own prose, which is the line amend0827-process-diet rule 2 draws. The worker declined to repair either without an order, which the round 7 block's constraint 1 required of it and which is correct behaviour. FIX CLAUSE, BINDING ON THE NEXT BLOCK THAT TOUCHES EITHER FILE: repair both comments in that same commit, and where a deletion round removes a named step, sweep the SECTION COMMENTS above the deleted units in EVERY file of the change set rather than only in the file whose banner the block happened to name. This is the third occurrence of the class in three rounds — round 6 repaired one such comment in `tests/orchestration/test_cluster_deletion_map.py`, round 7 repaired that same comment a second time as its own TRAP 2, and round 7 then left these two — so the sweep is the counter-measure, not another instance-fix.

- R-0842 — Medium, THE COCKPIT LOSES ITS CONTEXT-PACK BRAIN NODE, THE HUMANIZED FORM OF THE `context_pack_created` STREAM EVENT AND THE PLANNER ROW OF THE TOKEN-BUDGET BREAKDOWN WHEN THE `context_pack` MODULE GROUP IS DELETED, AND NO SURVIVING FEATURE CARRIES THOSE THREE READINGS. Raised by the reviewer while authoring F275 round 8 and registered by that round's ledger commit, because operator RULE 3 in `docs/roadmap/features/T2_F275.md` T001 requires a deletion that takes away a behaviour a user could observe to register a finding naming the behaviour and the feature that inherited the idea. THE MEASUREMENT, taken at `65409e647b04939746ff010a687c48621022b9e3`. `context_pack_created` is emitted at exactly ONE site in the tracked tree, `apps/cli/commands/context_pack_cmd.py`, which is a cluster command handler on the deletion list; three SURVIVING production readers consume it and no importer sweep can see any of them, because all three match on the event's STRING. `_build_context_pack_node` in `packages/orchestration/project_brain.py` builds the `NT_CONTEXT_PACK` node with its `has_context_pack` and `summarizes` edges, which `packages/orchestration/brain_detail.py` renders as a detail panel titled Context Pack and which `packages/orchestration/brain_viewer.py`, `packages/orchestration/brain_viewer_theme.py`, `packages/orchestration/ui_copy.py` and `packages/orchestration/ui_view_model.py` colour, layer, label and humanize; `packages/orchestration/ui_server.py` maps the same event to `by_role["planner"]` in the token-budget breakdown, and it is the ONLY event mapped to that bucket, so the planner row stops being populated at all rather than merely thinning; and `apps/ui/src/api/humanizeCatalog.ts` carries the one-sentence human form of the event. THE INHERITING FEATURE IS F107, context compiler v2, per the mapping DECISION F260 D3 fixes in `docs/roadmap/features/T2_F260.md` — context pack goes to F107 — and F107 is `[x]` accepted in `docs/roadmap/STATUS.md`, so the IDEA is already carried by shipped code and nothing is owed for it. WHAT IS NOT INHERITED, and why this is an id rather than a note: the three COCKPIT READINGS above have no equivalent in F107's context compiler, which emits no brain node, no stream event of that name and no role bucket. The surviving `context_coverage` node is a different reading — coverage of the sources, not the size of a composed pack — and is not offered as a replacement. FIX CLAUSE, BINDING ON THE ROUND THAT DRAFTS DECISION F260 D3: name these three readings in D3 among the ideas DELETED rather than inherited, beside R-0831's route-policy knobs and R-0840's run-keyed dogfood fields, and state F107 as the inheritor of the context-pack idea itself so that the mapping D3 is required to carry is complete for this module. No stub, no shim and no copy of cluster code into a survivor is permitted to close this, per AGENTS.md Scope Control and RULE 3's own wording.
===END LEDGER8===

===BEGIN SLIPS8 bytes=1125 sha256=2f9600d26575369d8067186715f22f382bd9c674221e57a2313ad1757df1ec8a===
2026-09-08 · F275 R7 · The round 7 block's gate G5 ordered `recommend_worker` to ZERO over the tracked tree while the same block's must-not-touch list keeps `docs/roadmap/features/T2_F272.md`, which contains that token, so the two clauses of one gate could not both be satisfied; the worker obeyed the must-not-touch half, which was the correct half, and declared the disagreement instead of silently repairing it.

2026-09-08 · F275 R7 · The round 7 block's gate G5 ordered the shell string `worker recommend` to ZERO in `scripts/` and `tests/` and one literal survives as a class docstring in `tests/storage/test_persistence.py`, which is prose rather than an invocation; `scripts/` really was at zero, which is the reading the gate existed for.

2026-09-08 · F275 R7 · The round 7 block's gate G5 predicted a SEVEN-file survivor set for `worker_recommend` and the true set is FIVE, because that block's own step (9) takes `tests/orchestration/test_cluster_deletion_map.py` to zero and `tests/STEP_TEST_MIGRATION.md` never held the token at all — it holds `TestWorkerExplain`, which the reviewer conflated with it.
===END SLIPS8===

===BEGIN DECISION8 bytes=5286 sha256=634502400c89f1b77003ccee2fa42f6c9bb5717cacbe1186f680961eacb71031===
## DECISION F275 D4 — an EVENT-COUPLED consumer of a cluster module dies in the same commit as the emitter that fed it, and the map's blindness to that coupling is R-0832's to repair, not this round's (2026-09-08, F275 round 8)

CONTEXT. Operator RULE 1 in `docs/roadmap/features/T2_F275.md` T001 defines a module group as one cluster module together with everything that exists ONLY for it, and names its handler, its catalog entries, its `ui_server.py` section, its tests and its map lines. RULE 3 governs a SURVIVING CONSUMER and is written entirely in terms of IMPORTS. R-0832 records that the deletion map is built from `ast`-parsed import statements and therefore cannot see a consumer coupled to the cluster by EVENT NAME, and routes its own fix to the round that drafts DECISION F260 D3. The feature file's "WHAT IS OWED HERE, IN ORDER" places that D3 round AFTER every module group. Round 8 is the first group whose surviving readers are ALL of that kind, so the three texts have to be read against each other before a single line is deleted.

THE MEASUREMENT, taken by the reviewer at `65409e647b04939746ff010a687c48621022b9e3` in a disposable worktree. `context_pack_created` is emitted at exactly ONE site in the tracked tree and that site is `apps/cli/commands/context_pack_cmd.py`, a cluster command handler already listed in `CLUSTER_COMMAND_HANDLERS`. Three surviving production modules read the event by string — `packages/orchestration/project_brain.py`, `packages/orchestration/ui_server.py` at two separate sites, and through the node type they build, `packages/orchestration/brain_detail.py`, `packages/orchestration/brain_viewer.py`, `packages/orchestration/brain_viewer_theme.py`, `packages/orchestration/ui_copy.py` and `packages/orchestration/ui_view_model.py`. Not one of them imports `packages.orchestration.context_pack`; the map correctly records no edge, so nothing here is a defect of the map's arithmetic. `packages/orchestration/ui_server.py` also holds a `token_mode` local computed from that event and read by NOTHING, which was already dead before this round and goes with the block it sits in.

CHOSEN. The event-coupled readers of a deleted emitter are part of the module group and are deleted in the SAME commit as the emitter. RULE 1's "everything that exists only for it" is the clause that reaches them, and it reaches them on a measurement rather than on a reading of intent: an event with one emitter and no other producer cannot be emitted again once that emitter is gone, so every reader of it exists only for the deleted module. R-0832's fix is NOT discharged by this decision and stays OPEN: what R-0832 asks for is a MEASUREMENT — the map extended, or a second measurement beside it, that records event-name couplings — and a NAMING of the event-coupled consumers in DECISION F260 D3. This round supplies neither. It supplies only the third clause of R-0832's own fix sentence, that the deletion round removes them in the same commit as their emitter.

WHY, and why this is a ruling rather than a question to the operator. Leaving them standing lands exactly the state R-0832 was registered to describe — reachable, tested, dead code — inside the round that creates it, and AGENTS.md Scope Control forbids an attic in the sentence "Replacing is deleting". The competing reading, that the feature file's ordering sentence reserves this work for the D3 round, would make every group commit between now and D3 deposit dead code deliberately, which is a worse outcome than a wider commit. docs/agents/planner_reviewer_prompt.md §4 item 7 requires the reviewer to rule and record rather than ask.

ALTERNATIVES CONSIDERED AND REJECTED. (1) Delete the group and leave the event readers for the D3 round. Rejected on the paragraph above, and because the tree would then carry a brain node builder, a detail renderer, four presentation maps and a token-budget branch that no input can reach, with the full suite green over all of it — the shape R-0832 exists to prevent. (2) Split the round in two commits, the module group and then the event readers. Rejected because both commits land in the same round anyway and R-0832's fix sentence names the SAME COMMIT; an intermediate commit whose smoke script asserts an event nothing can emit is a state this work should not pass through. (3) Widen the import walker so the map sees the coupling. Rejected by R-0832 itself, in terms: the events are string literals, not imports.

CONSEQUENCE. Round 8's change set is 24 paths rather than the dozen a pure module group costs, and it EDITS lines under `packages/`, `apps/`, `scripts/` and `tests/`, so it is NOT a deletion round under operator amendment amend0906-triage-throughput and does not get that paragraph's four-measurement shortcut. It is gated as a production-code round, with a ratchet red-proof in a disposable worktree and the full suite run serially in the primary checkout.

REVERSE by deleting this section, at which point the event readers of a deleted emitter go back to waiting for the D3 round and R-0832 carries the whole obligation alone. Nothing on disk becomes inconsistent under that reversal, because the deletions this decision authorises are recoverable from git and no later commit depends on their absence.
===END DECISION8===

===BEGIN LANDED8 bytes=872 sha256=680d3828d40842ccb65a51d20919c097f4c0359f96ed0ed8cec1eb3999f99ed5===
Landed: R-0841 — both falsified comments are repaired and the sweep its fix clause orders was run over the whole change set: the `Step 64` section header in `tests/test_remedy_smoke_script.py` loses its `+ explain` half and its `12w`, the `TestTokenEconomy` docstring in `tests/storage/test_persistence.py` names the token policy alone, and the sweep additionally found and removed a `Step 113 — Semantic Zoom Truth Table v4` banner left heading nothing at the end of that same file, a `Step 49` and a `Step 56` guard header in `tests/test_remedy_smoke_script.py` whose bodies this round deletes, a `context_pack_cmd.py` reference in the `CLUSTER_COMMAND_HANDLERS` comment in `tests/orchestration/test_cluster_deletion_map.py`, and two causal-chain lines in `docs/system/architecture.md` naming a deleted node and a deleted edge. Awaiting the reviewer's `Done:` text.
===END LANDED8===

C4 — THE DELETION, ONE COMMIT, in this order.

 (1) `git rm` three files whole: `packages/orchestration/context_pack.py`,
     `apps/cli/commands/context_pack_cmd.py`, `tests/test_context_pack.py`.
 (2) `apps/cli/commands/__init__.py`: delete the import line `        context_pack_cmd,` and
     remove `context_pack_cmd, ` from the single long `for mod in (...)` tuple, which is the
     file's one insertion.
 (3) `apps/cli/command_catalog.py`: delete the whole `CommandEntry(command_id="context.pack",
     ...)` block through its closing `    ),` and the blank line that follows it, and delete
     the line `        related=("context.pack",),` from the SURVIVING `context.inspect` entry
     directly above it. The `# ── context ──` group comment stays: `context.inspect` survives.
 (4) `apps/ui/src/api/humanizeCatalog.ts`: delete the one `"context_pack_created"` line.
 (5) `packages/orchestration/project_brain.py`: delete the module-docstring line
     `  summarizes            — context_pack → readiness or job (causal)`; the constants
     `NT_CONTEXT_PACK`, `ET_HAS_CONTEXT_PACK` and `ET_SUMMARIZES`; the `_NODE_TYPE_ORDER`
     entry `    NT_CONTEXT_PACK:        20,`; the whole `def _build_context_pack_node` with
     the blank lines that separated it from the next `def`; the `# context_pack
     --summarizes--> readiness or job` comment and the four statements under it inside
     `_build_causal_edges`, with the blank line above the comment; and the call
     `    _build_context_pack_node(acc)`. Remove `NT_CONTEXT_PACK, ` from the `_all_types`
     line, which is the file's one insertion. Do NOT renumber the surviving `_NODE_TYPE_ORDER`
     weights — that map is a lookup, the gap at 20 is harmless, and renumbering would be churn
     AGENTS.md's Code Discoverability section forbids as its own activity.
 (6) `packages/orchestration/brain_detail.py`: delete `    NT_CONTEXT_PACK,` from the import
     list, the whole `def _detail_context_pack` with the blank lines separating it from
     `_detail_patch_apply_proof`, and the dispatch entry
     `    NT_CONTEXT_PACK: _detail_context_pack,`.
 (7) `packages/orchestration/brain_viewer.py`: delete `    "context_pack": "policy",`,
     `    "context_pack": 2,` and `  if(t==='context_pack')return'var(--remedy-cyan)';`.
 (8) `packages/orchestration/brain_viewer_theme.py`: delete the one `"context_pack"` entry.
 (9) `packages/orchestration/ui_copy.py`: delete the `"context_pack":` label pair, and rewrite
     `    "context_coverage", "context_pack",` to `    "context_coverage",` inside
     `_DIAGNOSTICS_ONLY` — the file's one insertion.
(10) `packages/orchestration/ui_view_model.py`: delete
     `    "summarizes": ("informed_by", "Context summarizes job"),`.
(11) `packages/orchestration/ui_server.py`: delete the `# Token budget` block — the comment,
     the `token_mode = "compact"` assignment, the `for` loop over reversed events with its
     `if`, its assignment and its `break` — together with the blank line after it; MEASURED AT
     `65409e647b04939746ff010a687c48621022b9e3`, `token_mode` is READ BY NOTHING in that file
     (the only other occurrence is an unrelated `"token_mode": "compact"` dict literal), so
     this removes a dead local rather than a value. Then delete the three-line
     `elif ev in ("context_pack_created",):` branch of the token-role attribution.
(12) `scripts/remedy_smoke.sh`, three edits. (a) Delete section 12j whole, from its
     `    # 12j. Context pack JSON (Step 49)` heading through the line ending
     `"${PACK_COMPACT}")"`, and then the opening frame line and the blank line it leaves
     orphaned above section 12k. (b) In 12l drop `context_pack_created` from the section
     comment and the `echo`, delete the `chk('context_pack_created' in event_names, ...)`
     line and the whole `# Check context_pack_created metadata` block, and drop the `pack='`
     term from the closing `print`. (c) In 12s rewrite the heading comment and the `echo` from
     Token economy to Token policy, and delete the three `remedy context pack` assignments and
     the token-ordering `python3 -c` block; the `# Token policy required fields` half of that
     section SURVIVES and is untouched.
(13) `tests/test_remedy_smoke_script.py`: delete the
     `    # --- Step 49: Context pack JSON (step 12j) ---...` header with all five tests under
     it; delete `test_smoke_has_context_pack_created_event` and
     `test_smoke_context_pack_created_metadata_keys`; delete the
     `    # --- Step 56: Token economy (step 12s) ---...` header with its one test
     `test_smoke_has_token_ordering`. R-0841 FIX, HALF ONE: rewrite the header
     `    # --- Step 64: Worker show + explain (steps 12v-12w) ----------------------` to
     `    # --- Step 64: Worker show (step 12v) -------------------------------------`, which
     is the file's one insertion.
(14) `tests/storage/test_persistence.py`. R-0841 FIX, HALF TWO: rewrite the `TestTokenEconomy`
     docstring `    """Token Economy v1 — context pack modes, worker recommend."""` to
     `    """Token Economy v1 — the token policy."""`, the file's one insertion. Delete its
     four `context_pack`-importing methods — the three contiguous ones ending in
     `test_caveman_no_long_prose`, and `test_all_modes_obey_redaction` — each with the blank
     line that separated it, leaving `test_token_policy_json_has_all_fields` and
     `test_token_policy_applied_event_schema`. Then delete `class TestContextPackMemory` and
     all three of its methods TOGETHER WITH the `# ═══…` / `# Step 113 — Semantic Zoom Truth
     Table v4` / `# ═══…` banner above it and every blank line between and after it, so the
     file ENDS at the last statement of the class above. That banner is the R-0841 sweep
     working: it headed only the deleted class, and leaving it would have left a section
     comment over nothing at the end of the file.
(15) `tests/cli/test_context_inspect_cli.py`: delete `def test_context_inspect_related_commands`
     whole, with its trailing blank lines, leaving the `# ---` frame above it intact — that
     frame heads the surviving Handler tests region, not this test.
(16) `tests/conftest.py`: delete `    "test_context_pack.py",`.
(17) `tests/orchestration/test_project_brain.py`: delete `            "_build_context_pack_node",`
     and `            "packages/orchestration/context_pack.py",`.
(18) `tests/regression/test_named_bugs.py`: delete
     `            "packages/orchestration/context_pack.py",`.
(19) `tests/orchestration/import_reachability_allowlist.txt`: delete the two lines
     `apps.cli.commands.context_pack_cmd` and `packages.orchestration.context_pack`. Do NOT
     re-sort the file.
(20) `tests/orchestration/test_cluster_deletion_map.py`: delete
     `    "packages.orchestration.context_pack",` from `CLUSTER_MODULES` and
     `    "apps/cli/commands/context_pack_cmd.py",` from `CLUSTER_COMMAND_HANDLERS`. R-0841
     SWEEP: this commit falsifies that comment for the SECOND round running, so rewrite
     `# \`context_pack_cmd.py\` for exactly that reason.` to
     `# their own deletion-bound handler files for exactly that reason.` — the one insertion.
(21) `docs/system/architecture.md`: delete the whole `### Token Budget + Context Pack v0 (Step
     49)` section — heading, lead sentence, its bullets and the blank line after it. R-0841
     SWEEP: in `### Causal Proof Graph v1 (Step 51)` drop `, \`summarizes\`` from the causal
     chain edges bullet and `/context_pack` from the full-chain bullet, which are the file's
     two insertions. No status banner is added: the page's subject is the architecture, and
     the section that described this module is gone rather than superseded.
(22) REGENERATE `.agent/f275_deletion_order.md` from the live graph, per constraint 7, once
     (1) to (21) are on disk.

The reviewer's own application of (1) to (22) produced 24 paths at 13 insertions against 952
deletions, and its per-file `git diff --numstat` cells are NOT reproduced here on purpose:
round 7 showed that a reviewer's AST prune and a worker's careful hand differ by exactly the
blank lines that separated the deleted units, and the worker's reading was the better one.
Report your own numstat in the handback; it is not a target to hit. The insertion counts named
per step above ARE load-bearing, because each names a specific rewritten line.

Done when — the gates below, inside the budget of at most eight that operator amendment
amend0827-process-diet rule 5 allows a round. Every one is RUN and its real exit code is
reported, one line per gate, in the handback.

G1 TRANSPORT. `sha256` of the committed `.agent/authored/f275-r8.md` and of the committed
   `.agent/last_block.md` are ONE value, and it equals the digest the delegation states for
   the scratch original. Report the value and the byte count. Per §3 item 37 this chain covers
   those three artefacts and claims nothing about the emitted bytes.

G2 THE PLAN. The committed `.agent/plan.md` is BYTE-IDENTICAL to the PLAN8 slice: 2614 bytes,
   43 lines against the AGENTS.md cap of 50, `^## Goal$` exactly once and `^## Next Steps$`
   exactly once.

G3 THE RECORD, read from the committed blobs at C1 (pre) and C2 (post), never from the working
   tree. (a) `.agent/live_review.md` 541694 -> 551407, gain 9713 = 1 + 9712;
   `.agent/prose_slips.md` 172799 -> 173925, gain 1126 = 1 + 1125. (b) For each: the pre-blob
   is a byte-exact PREFIX of the post-blob, and one newline plus the slice is a byte-exact
   SUFFIX. (c) ORDERED EQUALITY over the WHOLE appended region: with a unit defined as a
   maximal run of consecutive non-empty lines, COUNT N from the slice's own bytes with your
   own reader — do not read N off this block — and require the file's last N units to equal
   the slice's N paragraphs IN ORDER. (d) NEGATIVE CONTROL, IN MEMORY ONLY: flip one byte
   inside the FIRST appended paragraph of each and require BOTH readers (b) and (c) to REJECT;
   re-read each tracked file from disk afterwards and report its unchanged size, which is the
   proof the control never reached disk. (e) `^Gate: ` 29 -> 30, `^Gate: F275 R7 ` 0 -> 1,
   `^- R-0841 — ` exactly 1, `^- R-0842 — ` exactly 1. (f) THE OPEN SET 66 -> 68 BY DISTINCT
   ID, computed as distinct `^- R-\d+ — ` ids minus distinct `^Done: R-\d+ — ` ids, never as
   raw line counts; report registrations 69 -> 71 and resolutions 3 -> 3 beside it.

G4 THE DECISION, from the committed blobs at C2 (pre) and C3 (post). `.agent/decisions.md`
   953044 -> 958331, gain 5287 = 1 + 5286; both edges exact as in G3(b); ordered equality over
   the whole appended region with N counted from the slice; the negative control on the FIRST
   appended paragraph rejected by both readers, in memory only, with the tracked size unchanged
   on disk afterwards; `^## DECISION F275 D` 3 -> 4 and `^## DECISION F275 D4 ` heading exactly
   ONE section.

G5 THE DELETION IS COMPLETE, over the TRACKED tree at C4 with `git grep`, so that build caches
   and ignored artefacts cannot answer for the source. `git ls-tree -r <C4> --name-only` finds
   NONE of `packages/orchestration/context_pack.py`,
   `apps/cli/commands/context_pack_cmd.py`, `tests/test_context_pack.py`. Outside `.agent/`,
   each of these eleven strings is at ZERO: `context_pack_created`, `build_context_pack`,
   `export_context_pack_json`, `summarize_context_pack`, `NT_CONTEXT_PACK`,
   `ET_HAS_CONTEXT_PACK`, `ET_SUMMARIZES`, `_build_context_pack_node`, `_detail_context_pack`,
   `context_pack_cmd`, `context.pack`. The WHOLE-WORD token `context_pack` outside `.agent/`
   is at SEVEN, and the survivor set is exactly `docs/roadmap/features/T2_F260.md` once,
   `packages/orchestration/main_builder_adapter.py` three times,
   `tests/orchestration/test_main_builder_adapter.py` once and
   `tests/orchestration/test_managed_builder_execution.py` twice — all of them the
   must-not-touch items named above. PRINT EVERY HIT; suppress nothing. If the reading differs
   from seven, report the real number and every line, and do not edit toward this list.

G6 THE RATCHETS, THE READERS AND THE RED-PROOF. In the PRIMARY checkout,
   `python3 -m pytest tests/orchestration/test_import_reachability.py
   tests/orchestration/test_cluster_deletion_map.py
   tests/orchestration/test_cluster_deletion_order.py -q` is EXIT 0 at 9 passed, and
   `python3 -m pytest tests/docs/ tests/test_test_categories.py
   tests/orchestration/test_roadmap_index.py -q` and the canary
   `python3 -m pytest tests/cli/test_golden_path.py -q` are both EXIT 0; report each count.
   Through the SHIPPED readers `apps.cli.commands.collect_all_handlers` and
   `apps.cli.command_catalog._BASE_CATALOG`, report both lengths and confirm `context.pack`
   ABSENT from both and `context.inspect` PRESENT in both. Print the regenerated body of
   `.agent/f275_deletion_order.md` in FULL. THEN THE RED-PROOF, in a DISPOSABLE WORKTREE
   checked out at C4 and nowhere else, running the same three-suite command each time and
   reporting the exit code of every run: the UNMUTATED control FIRST; then three mutations,
   each applied alone and reverted byte-identically before the next, each FROM string counted
   in its own named file at C4 where the count must be 1 — (i) insert
   `    "packages.orchestration.context_pack",` into `CLUSTER_MODULES` in
   `tests/orchestration/test_cluster_deletion_map.py`, (ii) insert
   `packages.orchestration.context_pack` as a body line of `.agent/f275_deletion_order.md`,
   (iii) insert `packages.orchestration.context_pack` into
   `tests/orchestration/import_reachability_allowlist.txt`; then the control AGAIN. The
   reviewer measured control 0, then 1, 1, 1, then 0. Remove and prune the worktree before the
   handback and show `git worktree list`.

G7 RUFF AND THE FULL SUITE, in the PRIMARY checkout. `python3 -m ruff check` over every Python
   file this round edits is `All checks passed!`; `python3 -m ruff check packages/ apps/cli/
   tests/` reads 24 at the base `65409e647b04939746ff010a687c48621022b9e3` and 24 at C4, taken
   at the base with `git show <base>:<path>`-style reading or in a disposable worktree, never
   by writing over the primary checkout. `bash -n scripts/remedy_smoke.sh` is EXIT 0. Then
   `python3 -m pytest tests/ -q` SERIALLY, no `-n auto`: report the real passed/skipped counts
   and the exit code. The reviewer's own dry run added `-p no:randomly` for determinism; this
   gate does NOT order that flag, because the counts are order-independent and the gate is the
   repository's own default invocation. The reviewer's applied dry run measured EXIT 0 at 19728 passed and 23
   skipped against the base's 19760, a fall of 32; report `--collect-only -q` over
   `tests/test_context_pack.py tests/storage/test_persistence.py
   tests/test_remedy_smoke_script.py tests/cli/test_context_inspect_cli.py
   tests/orchestration/test_project_brain.py` at the base and over the four survivors of that
   list at C4, which the reviewer measured at 317 and 285, and state whether the two falls
   agree. Report the MEASURED numbers whatever they are.

G8 THE TREE, run LAST, before C6. `.agent/STOP` does not exist; `git status --porcelain` is
   EMPTY; `git branch --show-current` is `feature/f275-one-world-completion-part-three`;
   `git worktree list` shows the primary checkout ALONE. `git diff --name-only <base>..<C5>`
   names EXACTLY the change set above minus `.agent/handoff.md`, which C6 adds after this gate
   — report the count and the set. Every commit in the range is single-parent, in the order
   C0a, C0b, C1, C2, C3, C4, C5, by `git rev-list --parents`; report each commit's INSERTION
   count from `git diff --numstat` — the `+` column only, per AGENTS.md DECISION F104 D1 —
   against the cap of 500. This gate can honestly reach only the commits that exist when it
   runs; the readings over the full round including C6 belong to the reviewer's next gate, not
   to a self-referential guess in the handback.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
             state block with FEATURE F275, ROUND 8, SESSION 4, the branch and every commit
             SHA; the changed-files table with real `+/-` from `git diff --numstat`; the
             item-status table covering C0a..C6 and G1..G8 with `done`, `skipped` or
             `deviated` and a reason for each of the last two; one line per gate with its real
             exit code; the open-findings count; the deviations; and the next expected action.
             It has NO length cap. Do not table the numstat of the commit that writes it.
             Push after C6.
── END OF STEP BLOCK ──
