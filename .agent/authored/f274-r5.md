# STEP T003/4 — F274 round 5 — take the first cluster module to ZERO edges

Goal: cut the edge `packages.orchestration.context_pack <- packages/orchestration/ui_server.py`,
which is that module's LAST recorded edge, so `context_pack` joins `review_bundle` and
`self_repair_proposal` as a module the deletion may take whenever the deletion itself may start.
Rule the cockpit endpoint that dies with it as DECISION F274 D3, and book round 4's PASS verdict.
No module is deleted this round.

Base: `feature/f274-one-world-completion-part-two` at
`0d68507bd5b794109db45d6d5765798fa87f7b97`. Stay on that branch; do not cut a new one, and do
not merge anything. Every fact this block states about a file was read at that commit.

WHY THIS EDGE AND NOT ANOTHER. At the base the map holds 39 edges over 22 cluster modules.
`context_pack` has exactly one left, and cutting it is the first time this feature moves a module
from "blocked" to "deletable" — which is the unit of progress DECISION F274 D2 defines. The
alternative candidate, `context_optimizer`, also has one edge, but its consumer
`packages/orchestration/project_brain.py` builds a whole BRAIN NODE TYPE that reaches
`brain_detail.py`, `brain_viewer.py`, `brain_viewer_theme.py`, `ui_view_model.py` and
`ui_copy.py`; that is a larger round and it is deliberately left for its own.

WHAT IS BEING DELETED, STATED PLAINLY. `_build_context_budget_json` in
`packages/orchestration/ui_server.py` is the cockpit read endpoint `context-budget`. It is built
on `packages.orchestration.context_pack`, it has NO consumer in `apps/ui/src` — the reviewer
grepped the string `context-budget` across `apps/`, `packages/`, `tests/`, `scripts/` and `docs/`
at the base and the only occurrences are its own definition, its route registration and the one
test that calls it — and no document describes it. AGENTS.md's Scope Control rules that replacing
is deleting and that a deletion carries a dated DECISION; D3 is that decision.

THE NAME COLLISION THAT MUST NOT CLAIM A VICTIM. `context_budget` also names a SURVIVING concept:
`estimate_context_budget` and `export_context_budget_estimate_json` in
`packages/orchestration/token_economy.py`, surfaced through the key `context_budget_estimate`
which `packages/orchestration/ui_server.py` reads near the top of the file. That concept is NOT
cluster-bound and is NOT touched. The only bytes this round removes from `ui_server.py` are the
function `_build_context_budget_json` and the single route line naming it.

## Conventions

This block carries authored TEXTS. A whole text begins on a line whose PREFIX is
`<<<BEGIN <NAME> ` and ends on a line reading exactly `<<<END <NAME>>>`, and it is read INCLUSIVE
of the newline ending its last content line. Extract every text programmatically by matching those
two marker lines; never retype one and never hand-type a digest. The named units in this block are
PLANF274R5, RECORD5 and D3SLICE274. RECORD5 and D3SLICE274 EACH CARRY THEIR OWN leading blank
line — append each as-is and never add a separator newline of your own. PLANF274R5 is a whole-file
replacement and carries no leading blank line. No line of this block is a run of a single repeated
character.

THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED. Section "The cut" is a SPEC you implement; it is
not authored bytes to copy.

## Bundle

C0a  save this block to `.agent/authored/f274-r5.md` by `shutil.copyfile`
C0b  mirror the same file to `.agent/last_block.md` by `shutil.copyfile`
C1   `.agent/plan.md` = PLANF274R5
C2   `.agent/live_review.md` findings region append RECORD5
C3   `.agent/decisions.md` append D3SLICE274
C4   the cut, written by you to the SPEC below
C5   `.agent/handoff.md` full rewrite

C3 PRECEDES C4 DELIBERATELY: the plan's own rule is that nothing is deleted before the decision
recording the deletion exists. Do not reorder them.

## Change set

Exactly these paths, and nothing else:

    .agent/authored/f274-r5.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/decisions.md
    .agent/handoff.md
    packages/orchestration/ui_server.py
    tests/ui_server/test_live_state.py
    tests/orchestration/test_test_runner.py
    tests/orchestration/cluster_deletion_map.txt

Nothing under `docs/`, nothing under `apps/`, and no allowlist change: this round adds no module,
so `tests/orchestration/import_reachability_allowlist.txt` is NOT touched.

## The cut

All of C4, in ONE commit, because the map ratchet reds unless the edge and its recorded line move
together:

DELETE from `packages/orchestration/ui_server.py` the whole function
`_build_context_budget_json`, including its docstring and its `except` fallback, and including
the blank lines that separated it from its neighbours, so no double blank line is left behind.
At the base it sits between the UI-not-built error exit above it and the `# Command Channel`
banner comment below it. DELETE ALSO the single line registering it in the endpoint table inside
the request handler, which at the base reads exactly:

                    "context-budget": _build_context_budget_json,

Those exact bytes occur ONCE in that file at the base — count them before you delete them and
report the count. Change no other endpoint, and change nothing that mentions
`context_budget_estimate`.

DELETE from `tests/ui_server/test_live_state.py` the whole test method
`test_context_budget_endpoint`, which requests `/api/jobs/<id>/context-budget` and asserts status
200. A test of a deleted endpoint is deleted with it; it is not rewritten to assert a 404.

DELETE from `tests/orchestration/test_test_runner.py` the whole test method whose docstring reads
`_build_context_budget_json failure returns structured degraded signal.`, which imports that
function by name. Deleting the function without this test leaves the suite red on an ImportError.

DELETE from `tests/orchestration/cluster_deletion_map.txt` the single line

    packages.orchestration.context_pack <- packages/orchestration/ui_server.py

IN THIS SAME COMMIT. Leaving it reds the map test with `DISAPPEARED (1)`; that redness is the
ratchet working and is this round's own proof that the edge was really cut.

WHAT THE ROUND MUST NOT DO. Do not add a replacement endpoint, a stub, a deprecation alias or a
404 route: AGENTS.md forbids the attic by name and git is the archive. Do not touch
`packages/orchestration/context_pack.py` itself — the module survives this round with zero edges
and is deleted later, by the deletion round, under DECISION F260 D3.

## Constraints

1. Apply every authored TEXT byte for byte. If a text cannot be applied as given, STOP and
   declare it; never adjust it to fit.
2. Commit in the order C0a, C0b, C1, C2, C3, C4, C5 and in no other. C1 advances the plan before
   any substantive commit, per §3 item 23, and only the two block-save commits precede it.
3. RECORD5 is appended to the END of `.agent/live_review.md`. At the base that file is 528978
   bytes and ends with a single newline. D3SLICE274 is appended to the END of
   `.agent/decisions.md`, which at the base is 886003 bytes and ends with a single newline.
4. No finding is minted and none is resolved this round. Write no `Done:` paragraph and no
   `Landed:` line. The open set is 62 by distinct id at the base and must be 62 at C5.
5. Do not run `ruff --fix`. The 26 pre-existing errors are a frozen ceiling, not a backlog.
6. Destructive verification runs ONLY inside a disposable `git worktree`, never in the primary
   checkout, which satisfies `git status --porcelain` empty at every commit boundary. Remove and
   prune the worktree before the handback.
7. The four state readers are run as FOUR, not as three.
8. Bare `ruff` is denied to this session's shell; every lint command is spelled
   `python3 -m ruff check <path>`.

## Done when

Run every gate, record its REAL exit code, and give each one line in the handback. G1 through G7
are ordered at commits that PRECEDE C5, so C5 can quote them.

G1 TRANSPORT (after C0b). `.agent/authored/f274-r5.md` and `.agent/last_block.md` are
byte-identical to each other and to the reviewer's scratch original
`.remedy-wt/f274-r5-block.md`; report the shared byte length and the shared sha256. This chain
covers those three artefacts and claims nothing about the bytes emitted into your prompt.

G2 THE RECORD APPEND (C2). (a) BYTE: the pre-image of `.agent/live_review.md` is a byte-exact
PREFIX of the post-image, and the post-image equals the pre-image plus RECORD5 exactly, with no
separator newline added. (b) STRUCTURAL, independently of (a): splitting BOTH images on the blank
line, the last N blank-line units of the post-image equal RECORD5's N paragraphs IN ORDER, where
N is a number your script COUNTS from the slice and never one this block asserts, and every unit
before those N is unchanged. State the unit definition your reader used. (c) NEGATIVE CONTROL:
flip one byte inside the FIRST appended paragraph and confirm BOTH readers reject it, then
confirm the file on disk is unchanged. (d) COUNTS across the commit, each as before-to-after:
distinct `^- R-\d+ — ` registrations, distinct `^Done: R-\d+ — ` resolutions, the OPEN SET BY
DISTINCT ID, `^Gate: `, and `^Gate: F274 R4`. At the base those read 65, 3, 62, 35 and 0.

G3 THE DECISION APPEND (C3). This slice is a MULTI-PARAGRAPH append into a record file, so it
carries the same two readers as G2 and not a prefix check alone. (a) BYTE: the pre-image of
`.agent/decisions.md` is a byte-exact PREFIX of the post-image and the post-image equals the
pre-image plus D3SLICE274 exactly; report both byte lengths. (b) STRUCTURAL, independently of
(a): the last N blank-line units of the post-image equal D3SLICE274's N paragraphs IN ORDER,
where N is a number your script COUNTS from the slice and never one this block asserts, and every
unit before those N is unchanged; state the unit definition your reader used. (c) NEGATIVE
CONTROL: flip one byte inside the FIRST appended paragraph — not the last — and confirm BOTH
readers reject it, then confirm the file on disk is unchanged. (d) Report `^## DECISION F274 D`
as before-to-after, which at the base counts 2, and confirm `^## DECISION F274 D3 ` heads exactly
ONE section.

G4 THE PLAN (C1). `.agent/plan.md` is byte-equal to PLANF274R5; report its line count against the
cap of 50, and confirm it carries `## Goal` and `## Next Steps`.

G5 THE EDGE IS CUT AND THE RATCHET IS PROVED BOTH WAYS, in a disposable worktree at C4. Report,
in this order: (a) the UNMUTATED control — `tests/orchestration/test_cluster_deletion_map.py` and
`tests/orchestration/test_import_reachability.py` run in ONE command, with exit code and passed
count. (b) The measured edge count and the recorded edge count, which must be EQUAL, the number
of cluster modules carrying at least one edge, and — the reading this round exists for — the list
of recorded consumers of `packages.orchestration.context_pack`, which must be EMPTY. Report that
list, not a claim about it. (c) RED: append the deleted edge line back to
`tests/orchestration/cluster_deletion_map.txt`, report the exit code and the `DISAPPEARED (n)`
figure, restore that one file by exact path and confirm exit 0 again. (d) RED, the other
direction: append the line `from packages.orchestration import context_pack` to
`packages/orchestration/ui_server.py`, report the exit code and the `APPEARED (n)` figure,
restore that one file by exact path and confirm exit 0 again — this is what proves the map still
SEES that consumer and that the cut was a real cut rather than a hidden exclusion.

G6 THE LINT CEILING AND THE BUDGETS. Report `python3 -m ruff check .` TWICE, naming the mechanism
for each. The BASE reading is taken in a disposable `git worktree` checked out at
`0d68507bd5b794109db45d6d5765798fa87f7b97`, with the command run from that worktree's own root so
`pyproject.toml` and its `per-file-ignores` resolve against the same paths; nothing in the primary
checkout is overwritten to obtain it. The HEAD reading is taken in the primary checkout at C4.
Both must read 26 errors. Report both numbers, not one, and report the exit code of
`python3 -m pytest tests/orchestration/test_ci_budgets.py -q`, which must be 0.

G7 THE SUITES, run SERIALLY in the PRIMARY CHECKOUT, each with its own exit code and passed
count: the four state readers `tests/ui_server/`,
`tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py` and
`tests/orchestration/test_integrity_gate.py`; then `tests/regression/test_named_bugs.py`,
`tests/orchestration/test_cluster_deletion_map.py`,
`tests/orchestration/test_import_reachability.py`, and the canary
`tests/cli/test_golden_path.py`. TWO OF THESE COUNTS MUST GO DOWN BY EXACTLY ONE, because this
round deletes one test from each: at the base `tests/ui_server/` is 515 passed and
`tests/orchestration/test_test_runner.py` is 52 passed. Report the new numbers and say explicitly
whether each fell by exactly one. A count that did NOT fall means a test was left behind; a count
that fell by more than one means something else was deleted.

G8 THE TREE AND THE COMMITS. `git status --porcelain` is EMPTY at every commit boundary;
`git ls-files .remedy-wt` is empty; report `git worktree list` counts before and after; report
`git diff --name-only 0d68507bd5b794109db45d6d5765798fa87f7b97..<C5>` and confirm it names exactly
the change set above and nothing else; report the insertion count of each commit C0a through C4
against the DECISION F104 D1 cap of 500. C5's own numbers go in the handback's `## Commits`
table, and the reviewer measures them at the next gate.

## Handback

Rewrite `.agent/handoff.md` in full per docs/agents/handback_template.md: feature and round, the
SESSION NUMBER of the running feature — this is SESSION 3 of F274 — branch, commit SHAs, the
changed-files table with its `+/-` column taken from `git diff --numstat` and compared cell by
cell against the per-commit numbers G8 reports, one line per gate with its real exit code, the
open-findings count, every deviation, the item-status table AGENTS.md requires, and the next
expected action. There is no length cap. Push the branch. Do NOT create a pull request and do NOT
merge anything.

<<<BEGIN PLANF274R5 whole-text
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 5: cut `context_pack`'s last recorded edge by deleting the cockpit `context-budget` read
endpoint that is built on it, ruled as DECISION F274 D3. That takes `context_pack` to zero edges
and makes it the third module the deletion may take. Book round 4's PASS verdict. No module is
deleted this round.

## Next Steps

1. `context_optimizer`'s last edge: the `context_budget` BRAIN NODE that
   `packages/orchestration/project_brain.py` builds, which also reaches `brain_detail.py`,
   `brain_viewer.py`, `brain_viewer_theme.py`, `ui_view_model.py` and `ui_copy.py`. Its own round.
2. `worker_recommend`'s three remaining edges, in `agent_loop.py`, `autonomy_loop.py` and
   `dashboard.py`.
3. The `worker_facade_cmd.py` edges, which carry the `mission report` name collision DECISION
   F274 D2 rules.
4. The remaining edges, of which `packages/orchestration/ui_server.py` holds the most by far.
5. The first carry-over, on the route DECISION F274 D2 fixes: the read-only overnight readiness
   and report views survive as `mission readiness` and `mission report`, the latter only in the
   commit that deletes the cluster-bound command already holding that name.
6. Draft DECISION F260 D3, the deletion paragraph, naming every deleted module and the feature
   that inherited its idea. Nothing is deleted before it exists.
7. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
8. T001 — measure the `Job.id` flip with a recording property, rule the cap route, and rule the
   persisted key. Then T002 — the classic runner and the resolver collapse.

## Risks

- Of the catalog's 341 command ids, 311 resolve to an owning handler file and 105 of those sit in
  one of the 21 files that import a cluster module, `mission.run` and `mission.report` among them.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
<<<END PLANF274R5>>>

<<<BEGIN RECORD5 findings-append

Gate: F274 R4 — the F274 round 4 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF, in the primary checkout and in two disposable worktrees, against the COMMITTED blobs rather than the working tree. Range `57d6698bf0af530dedd3d4df4b82cfb17163ba6b`..`0d68507bd5b794109db45d6d5765798fa87f7b97`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with `git diff --name-only` over that range naming exactly the fifteen declared paths and nothing else. THIS ROUND CUT THREE OF THE DELETION MAP'S FORTY-TWO EDGES, and it is the first round of this feature to change the shape of the deletion rather than to describe it. G1 TRANSPORT IS A REAL CHAIN, not a self-consistency check: the reviewer's own scratch original `.remedy-wt/f274-r4-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f274-r4.md` and `.agent/last_block.md` are all 28379 bytes and all hash to `88e60a6ee1dd0468158f9eac7182d4cb595bf46ef0697120761fcc522a63cc55`; per §3 item 37 that chain covers those three artefacts and claims nothing about emitted bytes. G2 THE RECORD APPEND at C2, re-derived by the reviewer from the committed blobs: 522330 to 528978 bytes, the pre-image a byte-exact PREFIX of the post-image, the post-image equal to the pre-image plus the 6648-byte RECORD4 slice with no separator added; under the unit definition "a maximal run of consecutive non-empty lines" the units went 213 to 214, N counted from the slice is 1, the last unit equals the slice's one paragraph and everything before it is unchanged; the negative control flipped at byte 522331 — inside the FIRST appended paragraph — is rejected by BOTH readers. Registrations 65 to 65, resolutions 3 to 3, OPEN SET 62 TO 62 BY DISTINCT ID, `^Gate: ` 34 to 35, `^Gate: F274 R3` 0 to 1. G3 THE MOVES ARE BYTE-IDENTICAL AND THE REVIEWER PROVED IT BY PARSING RATHER THAN BY READING THE DIFF: extracting each moved function with `ast.get_source_segment` at the base and at the head, `_cmd_context_pack` (1361 bytes), `_cmd_context_explain` (1528), `_cmd_context_optimize` (2024), `_cmd_worker_recommend` (980) and `_cmd_worker_explain` (1514) are each identical in the new file and absent from the old one. The COMMAND_HANDLERS key partition is exact and loses nothing: `context.py` went from four keys to `context.inspect` alone, `worker.py` from eight to six, and the three new files hold `context.pack`, then `context.explain` and `context.optimize`, then `worker.recommend` and `worker.explain`. G4 THE RATCHET IS REAL AND THE REVIEWER PROVED IT THREE WAYS IN ITS OWN DISPOSABLE WORKTREE AT `0d68507b`: the unmutated control over both suites in ONE command is EXIT 0 at 6 passed; restoring the three cut lines to the map is EXIT 1 reporting `DISAPPEARED (3)`; dropping `apps/cli/commands/worker_recommend_cmd.py` from `CLUSTER_COMMAND_HANDLERS` — bytes confirmed to occur exactly once first — is EXIT 1 reporting `APPEARED (1)`; and dropping the three new dotted names from the allowlist reds the reachability test. Each mutated file was restored byte-identically by exact path and each control returned to EXIT 0. THE EDGE ARITHMETIC IS 42 TO 39 AND THE MODULE COUNT DID NOT MOVE: measured edges equal recorded edges at 39, over 22 cluster modules, because `context_pack` keeps `packages/orchestration/ui_server.py`, `context_optimizer` keeps `packages/orchestration/project_brain.py` and `worker_recommend` keeps `agent_loop.py`, `autonomy_loop.py` and `dashboard.py`. G5 THE LINT CEILING HELD ON BOTH SIDES, each reading taken by a named mechanism: 26 errors at the base in a worktree checked out at `57d6698bf0af530dedd3d4df4b82cfb17163ba6b` and run from that worktree's own root, and 26 in the primary checkout at the head, so DECISION F083 D5's frozen ceiling is untouched; `test_ci_budgets.py` is EXIT 0 at 10 passed. This gate is the one the ROUND WOULD HAVE FAILED without its pre-emission dry run: the two moved worker bodies were the only users of `UUID`, `JobNotFoundError` and `load_job` in `apps/cli/commands/worker.py`, so a split that left the header alone lands three `F401` diagnostics and reads 29. The block ordered those imports removed for exactly that measured reason, and the reviewer confirms all three names now occur ZERO times in that file. G6 THE DISPATCH TABLE IS INTACT: through the shipped reader `apps.cli.commands.collect_all_handlers` the table is 341 entries before and after, and `context.pack`, `context.explain`, `context.optimize`, `context.inspect`, `worker.recommend`, `worker.explain`, `worker.list` and `worker.status` all resolve. G7 THE SUITES, re-run by the reviewer serially in the primary checkout, every one EXIT 0: the deletion map 3 passed, import reachability 3, `test_command_discovery.py` 17, `test_context_inspect_cli.py` 13, `test_persistence.py` 26, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, and the canary `tests/cli/test_golden_path.py` 42. G8 THE TREE: porcelain empty at every boundary, `git ls-files .remedy-wt` empty, worktrees 14 before and after, and per-commit insertions 327, 266, 11, 2, 8, 233, 118 and 272 for C0a through C6, every one far under the DECISION F104 D1 cap of 500. SIX DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL SIX. TWO DESERVE THE RECORD. THE FIRST IS AN UNORDERED EDIT THE REVIEWER SUSTAINS AS CORRECT: the worker swept the comment above `CLUSTER_COMMAND_HANDLERS`, which still said that `worker.py` and `context.py` host cluster commands alongside surviving ones — a sentence this round's own change made false. The path was in the change set, the edit is not executable, and leaving it would have landed a staleness defect of exactly the kind §3 item 20 exists to prevent; a worker that repairs the prose its own commit falsified is doing the job. THE SECOND is that the block's phrase "the WHOLE of the line" understated the deletion by one byte, because the dead storage import was its own import group and its preceding blank line went with it; the worker declared the extra byte rather than letting it pass, and the reviewer confirms the result is what the gate demanded. The worker also ran G2's negative control IN MEMORY rather than by writing to the primary checkout, which is the correct reading of constraint 8 rather than a weakening of the gate: an in-memory flip exercises both readers exactly as a written one does and cannot leave the tree dirty, and the reviewer reproduced it the same way with the same result. NO FINDING IS MINTED BY THIS GATE and none is resolved; R-0830 and R-0831 both stay open, and the next free id is R-0832.
<<<END RECORD5>>>

<<<BEGIN D3SLICE274 decisions-append

## DECISION F274 D3 — the cockpit `context-budget` endpoint is DELETED, not carried

Date: 2026-09-07. Feature F274, round 5. Status: decided by the reviewer under
docs/agents/planner_reviewer_prompt.md §4 item 7; the operator's veto is any later session.

CONTEXT. `packages.orchestration.context_pack` is one of the twenty-four prototype-cluster modules
F260's Design deletes. After round 4 moved the `context.pack` command handler into a cluster-bound
file, the module had exactly ONE recorded edge left: `packages/orchestration/ui_server.py`, whose
function `_build_context_budget_json` serves the cockpit read endpoint `context-budget`. Under
DECISION F274 D2 the deletion is bounded by edges, so this one edge is the whole of what stands
between `context_pack` and deletability.

CHOSEN. The endpoint is DELETED with its builder, its route registration and its two tests, and
nothing replaces it. AGENTS.md's Scope Control states that replacing is deleting, that there is no
attic, no deprecated alias and no compatibility reader, and that git is the archive. The idea the
endpoint served — telling a reader what a job's context costs — is INHERITED by the token-economy
surface that already exists beside it and is not cluster-bound:
`estimate_context_budget` in `packages/orchestration/token_economy.py`, surfaced through the
`context_budget_estimate` key that `packages/orchestration/ui_server.py` already reads. That
surface is untouched by this decision and by this feature.

ALTERNATIVES CONSIDERED AND REJECTED. (a) REPOINT the endpoint at `token_economy` instead of
deleting it. Rejected: the two produce different shapes — `context_pack` returns per-section
structure while `estimate_context_budget` returns a band estimate — so this would be a new
endpoint wearing an old name, which is the synonym drift AGENTS.md's discoverability rules forbid,
and F261 rather than F274 owns naming. (b) KEEP the endpoint and exempt `context_pack` from the
deletion. Rejected: it is on F260's Design list, and an exemption granted to keep one read
endpoint alive is how the previous three attempts at this deletion ended. (c) LEAVE a 404 route so
a client learns the endpoint is gone. Rejected: no client exists — the string `context-budget`
occurs nowhere in `apps/ui/src`, and at the base its only occurrences anywhere are its definition,
its route line and the one test that calls it.

EVIDENCE THIS RESTS ON, measured at `0d68507bd5b794109db45d6d5765798fa87f7b97`. The endpoint has
no consumer outside its own test; no document under `docs/` describes it; and the deletion map
records `packages.orchestration.context_pack` with exactly one edge, which this round removes,
leaving the module with none.

CONSEQUENCE. `context_pack` becomes the third cluster module with no recorded edge, after
`review_bundle` and `self_repair_proposal`. It is NOT deleted by this decision — the module and
its file survive until the deletion round, which runs under DECISION F260 D3 and names every
module it removes.

REVERSE THIS DECISION by restoring `_build_context_budget_json`, its route line and its two tests
from git history at `0d68507bd5b794109db45d6d5765798fa87f7b97`, and restoring the map line
`packages.orchestration.context_pack <- packages/orchestration/ui_server.py` in the same commit.
<<<END D3SLICE274>>>
