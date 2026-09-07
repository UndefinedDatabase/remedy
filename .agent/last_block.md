STEP — F274 ROUND 6 — cut `context_optimizer`'s last edge by deleting the `context_budget` brain node

Goal: take `packages.orchestration.context_optimizer` to ZERO recorded consumer edges by deleting
the `context_budget` BRAIN NODE — its builder, its constants, its ordering weight, its detail
renderer, its viewer and view-model entries and its copy — together with the deletion-map line that
records the edge and the four tests that read the node. That makes `context_optimizer` the fourth
cluster module the deletion may take. NO CLUSTER MODULE IS DELETED THIS ROUND.

Base commit for every reading in this block: `fcb77eab139faec83ffd88963bd5888d59dad677`.

FRAME CONVENTION. No line of this block is a run of a single repeated character. Every slice is
delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>` and a line reading `END <NAME>`,
and the slice is the bytes BETWEEN those two lines, the leading newline of an appended slice
included. The marker lines themselves are never written to any file.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r6.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN6 slice.
C2   Append the RECORD6 slice to `.agent/live_review.md` — this books round 5's PASS verdict and
     registers finding R-0832, both carried by the committed handoff under amend0827 rule 1.
C3   Append the SLIPS6 slice to `.agent/prose_slips.md` — round 5's two reviewer prose slips.
C4   THE CUT: the node deletion across the six production files, the deletion-map line, and the
     four tests. One commit.
C5   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must
be current before every commit.


## Change set — these paths and nothing else

  .agent/authored/f274-r6.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/handoff.md
  packages/orchestration/project_brain.py
  packages/orchestration/brain_detail.py
  packages/orchestration/brain_viewer.py
  packages/orchestration/brain_viewer_theme.py
  packages/orchestration/ui_view_model.py
  packages/orchestration/ui_copy.py
  tests/orchestration/cluster_deletion_map.txt
  tests/orchestration/test_project_brain.py
  tests/ui_server/test_brain_view_model.py


## C4 — the cut, specified per file

The reviewer applied this exact change in a disposable worktree at the base commit and ran it
before authoring; every count below was MEASURED there, not predicted. Delete the text described;
where a line is EDITED rather than deleted, the surviving half is named explicitly.

`packages/orchestration/project_brain.py` — delete, in the order they appear:
  - the module-docstring node line for `context_budget` (the "context budget optimizer summary"
    entry in the node-type list);
  - the module-docstring edge line for `has_context_budget` (the "job → context_budget" entry);
  - the constant assignment `NT_CONTEXT_BUDGET`;
  - the constant assignment `ET_HAS_CONTEXT_BUDGET`;
  - the `_NODE_TYPE_ORDER` entry mapping `NT_CONTEXT_BUDGET` to 26;
  - the WHOLE function `_build_context_budget_node`, including its docstring and the two blank
    lines that separate it from the function following it;
  - the call `_build_context_budget_node(acc)` in the node-build sequence;
  - `NT_CONTEXT_BUDGET` from the `_all_types` list near the end of the file. That name shares its
    line with `NT_DECISION_QUEUE`: EDIT the line so `NT_DECISION_QUEUE` SURVIVES on it.
  Nothing else in this file changes. `_build_context_pack_node`, `NT_CONTEXT_PACK` and every
  `context_pack` spelling SURVIVE — they read an event rather than an import, they carry no edge,
  and they are R-0832's business rather than this round's.

`packages/orchestration/brain_detail.py` — delete:
  - `NT_CONTEXT_BUDGET` from the sorted import block it appears in;
  - the WHOLE function `_detail_context_budget`, including the two blank lines separating it from
    what follows;
  - the dispatch-table entry mapping `NT_CONTEXT_BUDGET` to `_detail_context_budget`.

`packages/orchestration/brain_viewer.py` — delete the `"context_budget"` layer entry and the
  `"context_budget"` weight entry, and EDIT the colour branch in the embedded script that reads
  `context_pack` and `context_budget` in ONE condition so that it tests `context_pack` ALONE and
  returns the same value. `context_pack` MUST SURVIVE that line.

`packages/orchestration/brain_viewer_theme.py` — delete the `"context_budget"` layer entry.

`packages/orchestration/ui_view_model.py` — delete the `"context_budget"` entry from each of the
  two weight maps, from the class map, and from the copy map, and delete the
  `"has_context_budget"` entry from the edge map. The neighbouring `"context_coverage"` and
  `"constitution"` entries SURVIVE in every one of those maps.

`packages/orchestration/ui_copy.py` — delete the `"context_budget"` copy tuple, and EDIT the
  `_DIAGNOSTICS_ONLY` line that lists `context_coverage`, `context_budget` and `context_pack` so
  that `context_coverage` and `context_pack` BOTH SURVIVE on it.

`tests/orchestration/cluster_deletion_map.txt` — delete the single line
  `packages.orchestration.context_optimizer <- packages/orchestration/project_brain.py`. That line
  occurs exactly once in that file at the base commit. THE MAP LINE GOES IN THE SAME COMMIT AS THE
  CUT — the map test reds in both directions and a line left behind is as red as a new edge.

`tests/orchestration/test_project_brain.py` — delete the whole test methods
  `test_brain_has_context_budget_node` and `test_brain_context_budget_edges`, and EDIT
  `test_brain_node_type_order` to drop `NT_CONTEXT_BUDGET` from its import tuple and to drop its
  two `NT_CONTEXT_BUDGET` assertions. THAT TEST SURVIVES: its `NT_DECISION_QUEUE` import and both
  of its `NT_DECISION_QUEUE` assertions, including the one pinning the weight 25, are UNCHANGED.

`tests/ui_server/test_brain_view_model.py` — delete the whole test method
  `test_detail_context_budget`.

DO NOT TOUCH, and the reviewer measured each of these as byte-identical between the base commit
and its own applied worktree: `packages/orchestration/token_economy.py`,
`packages/orchestration/token_cost_policy.py`, `packages/orchestration/event_schemas.py`,
`packages/orchestration/worker_registry.py`, `apps/ui/src/api/humanizeCatalog.ts`,
`apps/ui/src/api/actionClass.ts` and `apps/cli/commands/context_optimizer_cmd.py`. The token
`context_budget` NAMES A SURVIVING CONCEPT in the first four of those — `estimate_context_budget`,
`context_budget_estimate`, `context_budget_policy`, `context_budget_hint` — and the event name
`context_budget_optimized` survives in the rest. NONE of them is cluster-bound and none is in this
round's change set.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype, re-indent or "fix" a slice. If a slice
   looks wrong, apply it as given and DECLARE the doubt in the handback.
2. Two slices are APPENDS and one is a full REPLACEMENT. RECORD6 and SLIPS6 are appends: the
   target's existing bytes are a byte-exact PREFIX of the result and the slice is an exact SUFFIX.
   Each carries its OWN leading newline, which supplies the blank-line separation — ADD NO
   SEPARATOR of your own. PLAN6 replaces `.agent/plan.md` entirely.
3. The path set of C0a through C4 is exactly the paths listed under "Change set" other than
   `.agent/handoff.md`, which C5 writes. Nothing outside that list is created, edited or deleted.
4. Every destructive check runs ONLY inside a disposable `git worktree`, never in the primary
   checkout, which satisfies `git status --porcelain` == empty at every commit boundary. Remove and
   prune each worktree you create.
5. Do not write a `Done:` paragraph. Only reviewer-authored text resolves a finding.
6. Every gate below runs at a commit STRICTLY EARLIER than C5, so the handback can quote each
   result. Where a gate names the commit it runs at, run it there and nowhere else.
7. The two `.remedy-wt` scratch directories the reviewer used are gitignored and are not yours to
   clean up; `git ls-files .remedy-wt` must stay empty.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r6.md` equals `sha256` of
    the committed `.agent/last_block.md`, and both equal the digest the delegation message states
    for this block. Report the digest you measured. ONE comparison; do not build a chain.

G2  THE RECORD APPEND, at C2, re-derived from the COMMITTED blobs and not the working tree.
    (a) BYTES: `.agent/live_review.md` goes 535659 -> 543921, the pre-image is a byte-exact PREFIX
        of the post-image, and the post-image equals pre plus the 8262-byte RECORD6 slice with no
        separator added.
    (b) STRUCTURE, an independent reader over the WHOLE appended region: define a unit as a
        maximal run of consecutive non-empty lines; COUNT N as the number of units in the RECORD6
        slice itself (do not take N from this block); assert that the file's last N units equal the
        slice's N units IN ORDER and that everything before them is unchanged. Units go 215 -> 217.
    (c) NEGATIVE CONTROL: flip one byte INSIDE THE FIRST APPENDED PARAGRAPH — the byte at
        ZERO-INDEXED BYTE offset 535660 of the post-image, read as bytes and not as characters
        because this file carries multi-byte UTF-8; that byte is the `G` that opens this slice's
        `Gate:` header — and confirm BOTH readers (a) and (b) REJECT it. Do the flip in memory or
        in a disposable worktree; the primary checkout stays clean.
    (d) COUNTS over the post-image: registrations 65 -> 66, resolutions 3 -> 3, OPEN SET 62 -> 63
        BY DISTINCT ID (distinct `^- R-\d+ — ` ids minus distinct `^Done: R-\d+ — ` ids),
        `^Gate: ` 36 -> 37, `^Gate: F274 R5` 0 -> 1, and `^- R-0832 — ` exactly 1.

G3  THE STATE PROSE FILES, at C3.
    (a) `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN6 slice, is 43 lines against the cap of 50,
        and carries both `## Goal` and `## Next Steps`.
    (b) `.agent/prose_slips.md` at C3: the pre-image is a byte-exact PREFIX, the post-image is pre
        plus the 555-byte SLIPS6 slice, bytes go 158178 -> 158733, and each of the two appended
        lines occurs exactly once in the file.

G4  THE RATCHET, BOTH WAYS, in a disposable worktree checked out at C4. Report the exit code of
    every run, and the UNMUTATED control BEFORE the mutations as well as after.
    (a) CONTROL: `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py
        tests/orchestration/test_import_reachability.py -q` is EXIT 0.
    (b) MEASURED equals RECORDED at 37 edges; the measured consumers of
        `packages.orchestration.context_optimizer` are THE EMPTY LIST; and the modules with no
        edge are exactly `context_optimizer`, `context_pack`, `review_bundle` and
        `self_repair_proposal`.
    (c) RED ONE: append the deleted line back to `tests/orchestration/cluster_deletion_map.txt`.
        `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py -q` must be EXIT 1
        and its output must contain `DISAPPEARED (1)` and name that exact edge. Restore that file
        BY EXACT PATH and confirm it is byte-identical to before the mutation.
    (d) RED TWO: append the single line `from packages.orchestration import context_optimizer` to
        `packages/orchestration/ui_server.py`. The same command must be EXIT 1 and its output must
        contain `APPEARED (1)` and name `context_optimizer <- packages/orchestration/ui_server.py`.
        This proves the map still SEES that consumer, so the cut is a real cut and not a hidden
        exclusion. Restore that file BY EXACT PATH and confirm it is byte-identical.
    (e) The control of (a) returns to EXIT 0 after both restorations.

G5  THE ORDERED COUNTS, run serially in the primary checkout at C4. These are the discriminator
    between "the tests went with their subject", "a test was left behind" and "something else was
    deleted too", so report the NUMBER for each, not a colour.
    (a) MOVED, and each must fall by exactly the stated amount:
        `tests/orchestration/test_project_brain.py` 84 -> 82 (two tests deleted, one edited),
        `tests/ui_server/test_brain_view_model.py` 39 -> 38, `tests/ui_server/` 514 -> 513.
    (b) NOT MOVED, each EXIT 0 and each at the same count as the base commit:
        `tests/orchestration/test_event_ledger.py`, `tests/orchestration/test_token_economy.py`,
        `tests/orchestration/test_token_cost_policy.py`, `tests/orchestration/test_source_apply.py`
        — all four match on a SURVIVING spelling and must not move. Together they are 108 passed.
    (c) The canary `pytest tests/cli/test_golden_path.py -q` is EXIT 0 at 42 passed.

G6  THE SWEEP, at C4. Over `packages/`, `apps/`, `tests/` and `scripts/`, excluding
    `node_modules` and `dist`, the tokens `NT_CONTEXT_BUDGET`, `ET_HAS_CONTEXT_BUDGET`,
    `_build_context_budget_node`, `_detail_context_budget` and `has_context_budget` occur ZERO
    times in total — report the total you measured. In the same run confirm that the colour branch
    in `packages/orchestration/brain_viewer.py` still names `context_pack` exactly once, and that
    each of the seven DO-NOT-TOUCH files named above is byte-identical between
    `fcb77eab139faec83ffd88963bd5888d59dad677` and C4. READ THE BASE BLOB WITH
    `git show fcb77eab139faec83ffd88963bd5888d59dad677:<path>` into memory or into a gitignored
    scratch file — never by writing the base bytes over the tracked file, which would dirty the
    primary checkout that constraint 4 requires to stay clean.

G7  THE LINT CEILING, which DECISION F083 D5 freezes. `python3 -m ruff check .` is 26 errors in a
    disposable worktree checked out at `fcb77eab139faec83ffd88963bd5888d59dad677` and RUN FROM
    THAT WORKTREE'S OWN ROOT, and 26 in the primary checkout at C4. Report both numbers.
    `python3 -B -m pytest tests/orchestration/test_ci_budgets.py -q` is EXIT 0.

G8  THE TREE, at C4. `git status --porcelain` is EMPTY; `git ls-files .remedy-wt` is EMPTY;
    `git worktree list` has the same number of entries as before your first worktree and after
    your last prune; `git diff --name-only fcb77eab139faec83ffd88963bd5888d59dad677..<C4>` names
    exactly the paths of constraint 3 and nothing else; and every commit from C0a through C4 is
    single-parent. Report the INSERTION count of each commit C0a through C4 — the `+` column only,
    per AGENTS.md DECISION F104 D1. Do not report C5's own numbers: that commit does not exist when
    the handback quoting it is written, and the reviewer measures them at the next gate.


## Handback — rewrite `.agent/handoff.md` at C5, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits
table with its `+/-` column taken from `git diff --numstat` and compared cell by cell against the
insertion counts G8 reports, the changed-files table, ONE LINE PER GATE G1 through G8 with its real
result, the deviations, the open-findings count, and the next expected action. The handback has NO
length cap. Name the SESSION NUMBER as SESSION 4 of feature F274 and the round as 6. State the
open-findings count as the number G2(d) MEASURED. Add the one sentence of context self-assessment
amend0905-throughput requires.

DECLARE, do not silently repair: if any gate goes red, or any slice does not apply as described,
report the real exit code and the real output and say what you did. A worker who reports a red gate
honestly is doing the thing this workflow exists for.


BEGIN PLAN6 sha256=715a57a19adf05d4e08ed0828b8a4dce01aa93d97d2b01624968ebd50de0f7c3 bytes=2532
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 6: cut `context_optimizer`'s last recorded edge by deleting the `context_budget` BRAIN NODE
from the six production files that build, render, weight, colour and describe it, together with
its deletion-map line and the four tests that read it. That takes `context_optimizer` to zero
edges and makes it the fourth module the deletion may take. Book round 5's PASS verdict, register
R-0832 and append round 5's two prose slips. No module is deleted this round.

## Next Steps

1. `worker_recommend`'s three remaining edges, in `agent_loop.py`, `autonomy_loop.py` and
   `dashboard.py`. These are LIVE RUNTIME CALLS rather than read-only views, so a DECISION naming
   what inherits worker recommendation is authored before the cut.
2. The `worker_facade_cmd.py` edges, which carry the `mission report` name collision DECISION
   F274 D2 rules.
3. The remaining edges, of which `packages/orchestration/ui_server.py` holds the most by far.
4. The first carry-over, on the route DECISION F274 D2 fixes: the read-only overnight readiness
   and report views survive as `mission readiness` and `mission report`, the latter only in the
   commit that deletes the cluster-bound command already holding that name.
5. Draft DECISION F260 D3, the deletion paragraph, naming every deleted module and the feature
   that inherited its idea. R-0832's fix clause binds it. Nothing is deleted before it exists.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — measure the `Job.id` flip with a recording property, rule the cap route, and rule the
   persisted key. Then T002 — the classic runner and the resolver collapse.

## Risks

- Of the catalog's 341 command ids, 311 resolve to an owning handler file and 105 of those sit in
  one of the 21 files that import a cluster module, `mission.run` and `mission.report` among them.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
END PLAN6


BEGIN RECORD6 sha256=beb0acbaa2a96564c6cdbe9ea8d36fcbf6856f3e8ec5d804829333f14d417f6f bytes=8262

Gate: F274 R5 — the F274 round 5 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF, in the primary checkout and in two disposable worktrees, against the COMMITTED blobs rather than the working tree. THIS ENTRY IS BOOKED BY ROUND 6 RATHER THAN BY ROUND 5, under operator amendment amend0827-process-diet rule 1, which makes the committed and pushed `.agent/handoff.md` a durable carrier and forbids a round whose whole change set is bookkeeping. Range `0d68507bd5b794109db45d6d5765798fa87f7b97`..`f8e2c69ef1f3abb336d0001d8c62072056f858dd`, seven commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, with `git diff --name-only` over that range naming exactly the ten declared paths and nothing else. G1 TRANSPORT IS A REAL CHAIN, AND IT IS NAMED FOR WHAT IT COVERS RATHER THAN FOR WHAT IT CANNOT: the reviewer's own scratch original `.remedy-wt/f274-r5-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f274-r5.md` and `.agent/last_block.md` are all 26865 bytes and all hash to `086b486a775911164ac34029a7583a6e556aba9d11c439334950e8c3cc8ab301`. G2 THE RECORD APPEND at `5e2a9e07`, re-derived from the committed blobs: 528978 to 535659 bytes, pre-image a byte-exact PREFIX, post-image equal to pre plus the 6681-byte RECORD5 slice with no separator added; under the unit definition "a maximal run of consecutive non-empty lines" units went 214 to 215, N counted from the slice is 1, the last unit matches in order and everything before it is unchanged, and the control flipped at byte 528979 — inside the FIRST appended paragraph — is rejected by BOTH readers; registrations 65 to 65, resolutions 3 to 3, OPEN SET 62 TO 62 BY DISTINCT ID, `^Gate: ` 35 to 36, `^Gate: F274 R4` 0 to 1. G3 THE DECISION APPEND at `97403515` is the first MULTI-PARAGRAPH append this feature has gated under the checklist item covering a whole appended region and it holds: 886003 to 889313 bytes, prefix and ordered equality true, units 1951 to 1959, N counted from the slice as 8, the last eight units matching IN ORDER, the control flipped inside the FIRST of the eight rejected by both readers, `^## DECISION F274 D` 2 to 3, and `^## DECISION F274 D3 ` heading exactly one section. G4: `.agent/plan.md` is byte-equal to its slice at 44 lines against the cap of 50 and carries both mandated headings. G5 THE EDGE IS CUT AND THE REVIEWER PROVED THE RATCHET BOTH WAYS IN ITS OWN DISPOSABLE WORKTREE AT `f8e2c69ef1f3abb336d0001d8c62072056f858dd`: the unmutated control over both suites in ONE command is EXIT 0 at 6 passed; measured edges equal recorded edges at 38 over 21 modules; THE RECORDED AND MEASURED CONSUMERS OF `packages.orchestration.context_pack` ARE BOTH THE EMPTY LIST, which is the reading this round existed for, and the zero-edge modules are `context_pack`, `review_bundle` and `self_repair_proposal`; restoring the deleted map line is EXIT 1 reporting `DISAPPEARED (1)` and naming that exact edge; appending `from packages.orchestration import context_pack` to `packages/orchestration/ui_server.py` is EXIT 1 reporting `APPEARED (1)`, which proves the map still SEES that consumer and that the cut was a real cut rather than a hidden exclusion; each mutated file was restored byte-identically by exact path and each control returned to EXIT 0. G6 THE LINT CEILING HELD: 26 errors at the base in a worktree checked out at `0d68507bd5b794109db45d6d5765798fa87f7b97` and run from that worktree's own root, and 26 in the primary checkout at `f8e2c69ef1f3abb336d0001d8c62072056f858dd`, so DECISION F083 D5's frozen ceiling is untouched; `test_ci_budgets.py` EXIT 0 at 10 passed. G7 THE SUITES, re-run serially in the primary checkout, every one EXIT 0: `tests/ui_server/` 514 passed, `test_test_runner.py` 51, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_named_bugs.py` 64 passed with 6 skipped, the deletion map 3, import reachability 3, and the canary `tests/cli/test_golden_path.py` 42. BOTH ORDERED COUNTS FELL BY EXACTLY ONE, 515 to 514 and 52 to 51, which is the gate that distinguishes "the tests were deleted with their subject" from "a test was left behind" and from "something else was deleted too". G8 THE TREE: porcelain empty at every boundary, `git ls-files .remedy-wt` empty, worktrees 14 before and after, per-commit insertions 324, 230, 19, 2, 46, 0 and 257 for C0a through C5 — C4, the cut itself, is a PURE DELETION at zero insertions. THE NAME COLLISION CLAIMED NO VICTIM, AND THE REVIEWER MEASURED THAT RATHER THAN TRUSTING IT: `_build_context_budget_json` and the route string both occur ZERO times at `f8e2c69ef1f3abb336d0001d8c62072056f858dd`, while the surviving `context_budget_estimate` read still occurs once and `packages/orchestration/token_economy.py` is BYTE-IDENTICAL between base and that commit. SIX DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL SIX. THE ONE THAT MATTERS IS THE WORKER'S OWN GATE SCRIPT GOING RED FIRST: its structural reader split on blank lines with a regex that left boundary newlines attached asymmetrically, so both structural clauses read False while the byte reader read True; the worker reported the real EXIT 1, diagnosed it as a defect of its own reader rather than of the file, redefined a unit as a maximal run of consecutive non-empty lines, re-ran to EXIT 0 and said so — which is the standard this workflow exists to hold, and the reviewer independently reproduced the corrected reading. TWO DEVIATIONS ARE THE REVIEWER'S OWN PROSE AND ARE RECORDED AS DATED `.agent/prose_slips.md` LINES rather than as ids, per amend0827 rule 2, because neither left anything wrong on disk. NO FINDING IS RESOLVED BY THIS GATE. ONE IS MINTED, R-0832, and it is the paragraph directly below this one.

- R-0832 — Medium, THE CLUSTER DELETION MAP MEASURES IMPORT EDGES ONLY, SO A CONSUMER COUPLED TO THE CLUSTER BY EVENT NAME IS INVISIBLE TO IT AND WILL SURVIVE THE DELETION AS DEAD CODE. Raised by the reviewer at the F274 round 5 gate and booked by round 6's first substantive commit. THE RULE. `tests/orchestration/test_cluster_deletion_map.py` builds its edge set from `first_party_imports`, which parses `import` statements with `ast`; DECISION F274 D2 then rules the deletion bounded by those edges. THE MEASUREMENT, taken at `f8e2c69ef1f3abb336d0001d8c62072056f858dd`. `_build_context_pack_node` in `packages/orchestration/project_brain.py` builds the `NT_CONTEXT_PACK` brain node from events whose `event` field equals `context_pack_created`, and it imports NOTHING from the cluster — that file carries no import of `packages.orchestration.context_pack`, and the map correctly records no such edge, so nothing here is a defect of the map's arithmetic. That event is emitted by `_cmd_context_pack`, which round 4 moved into the deletion-bound `apps/cli/commands/context_pack_cmd.py`. So when the cluster goes, the event stops being emitted, the node silently stops appearing, and the builder, the node type constant, its ordering weight and its detail renderer all remain on disk — reachable, tested, and dead. THE SAME SHAPE REACHES `context_budget_optimized`, emitted by `_cmd_context_optimize` in `apps/cli/commands/context_optimizer_cmd.py` and named in `packages/orchestration/event_schemas.py`, `apps/ui/src/api/humanizeCatalog.ts` and `apps/ui/src/api/actionClass.ts`; F274 round 6 deletes the `context_budget` BRAIN NODE for its IMPORT edge and deliberately leaves every one of those event-name sites standing, which is this finding's scope and not that round's. This is a gate over production code shown to be BLIND to a real coupling, which is what amend0827 rule 2 spends an id on. FIX, binding on the round that drafts DECISION F260 D3: extend the map, or add a second measurement beside it, that records EVENT-NAME couplings from the cluster's emitters to their non-cluster readers, and name the event-coupled consumers in D3 so the deletion round removes them in the same commit as their emitter. Do not widen the import walker to do it — the events are string literals, not imports, and the lesson of the checklist item covering stubs and patched targets is that a guard which cannot see a coupling is not made honest by being pointed at the wrong syntax.
END RECORD6


BEGIN SLIPS6 sha256=16646ff77babc1929130f39d17206ec599bcc1de057c4d8a07957835077e8c16 bytes=555

2026-09-07 · F274 R5 · The round 5 block quoted the cockpit `context-budget` route line with four more leading spaces than `packages/orchestration/ui_server.py` carries, so the worker counted the identifying bytes instead and reported the count of 1.

2026-09-07 · F274 R5 · That block's gate G8 ordered a `git diff --name-only` path-set reading over a range ending at C5 while stating only that G1 through G7 precede C5, so the commit at which G8 itself runs was never fixed, and an honest worker ran it before C5 existed and saw nine paths of ten.
END SLIPS6
