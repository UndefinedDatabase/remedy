# STEP T003/3 — F274 round 4 — cut the three handler edges the deletion map records

Goal: remove three of the deletion map's forty-two edges by splitting the cluster-bound command
handlers out of the two files that host both surviving and cluster-bound commands, so those two
files stop being surviving consumers of the cluster. Book round 3's PASS verdict in the same
round. NOTHING IS DELETED and no command id changes.

Base: `feature/f274-one-world-completion-part-two` at
`57d6698bf0af530dedd3d4df4b82cfb17163ba6b`. Stay on that branch; do not cut a new one, and do
not merge anything. Every fact this block states about a file was read at that commit.

WHY THIS ROUND IS NOT A DELETION. DECISION F274 D1 prohibits splitting inside T003, which binds
the `git rm` sequence a session that cannot finish it must not start. Cutting an edge is ordinary
product work and is not that sequence, so this round is safe to run and safe to stop after.
DECISION F274 D2 rules the deletion is bounded by EDGES rather than by F260's module list; this
round pays down three of them.

WHY A SPLIT RATHER THAN A DELETION OF THE COMMANDS. `apps/cli/commands/context.py` and
`apps/cli/commands/worker.py` each host BOTH surviving and cluster-bound commands. While a
cluster-bound handler sits in them, the file itself is a surviving consumer and its import is a
blocker. Moving the handler into a file that is ITSELF cluster-bound — one listed in
`CLUSTER_COMMAND_HANDLERS` — makes the import die with the cluster instead of blocking it. The
command ids are untouched: this is not a rename, which F261 owns.

## Conventions

This block carries authored TEXTS. A whole text begins on a line whose PREFIX is
`<<<BEGIN <NAME> ` and ends on a line reading exactly `<<<END <NAME>>>`, and it is read INCLUSIVE
of the newline ending its last content line. Extract every text programmatically by matching those
two marker lines; never retype one and never hand-type a digest. The named units in this block are
PLANF274R4, RECORD4 and SLIPS4. RECORD4 and SLIPS4 EACH CARRY THEIR OWN leading blank line —
append each as-is and never add a separator newline of your own. PLANF274R4 is a whole-file
replacement and carries no leading blank line. No line of this block is a run of a single repeated
character.

THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED. Section "The production change" below is a SPEC
you implement; it is not authored bytes to copy. Where it names a body to MOVE, the move is
byte-for-byte: the function's text is unchanged, only its file changes.

## Bundle

C0a  save this block to `.agent/authored/f274-r4.md` by `shutil.copyfile`
C0b  mirror the same file to `.agent/last_block.md` by `shutil.copyfile`
C1   `.agent/plan.md` = PLANF274R4
C2   `.agent/live_review.md` findings region append RECORD4
C3   `.agent/prose_slips.md` append SLIPS4
C4   the context split, written by you to the SPEC below
C5   the worker split, written by you to the SPEC below
C6   `.agent/handoff.md` full rewrite

## Change set

Exactly these paths, and nothing else:

    .agent/authored/f274-r4.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/handoff.md
    apps/cli/commands/__init__.py
    apps/cli/commands/context.py
    apps/cli/commands/context_pack_cmd.py
    apps/cli/commands/context_optimizer_cmd.py
    apps/cli/commands/worker.py
    apps/cli/commands/worker_recommend_cmd.py
    tests/orchestration/test_cluster_deletion_map.py
    tests/orchestration/cluster_deletion_map.txt
    tests/orchestration/import_reachability_allowlist.txt

Nothing under `docs/`, nothing under `packages/`, and no catalog file. `.agent/decisions.md` is
NOT in this set: this round rules nothing new.

## The production change

### C4 — the context split

CREATE `apps/cli/commands/context_pack_cmd.py`. It holds `_cmd_context_pack`, moved
byte-for-byte out of `apps/cli/commands/context.py`, and a `COMMAND_HANDLERS` dict holding the
single entry `"context.pack"`, moved byte-for-byte out of that file's own dict. Its module header
carries the imports that body actually uses and no others: `json as _json`, `sys`,
`collections.abc.Callable`, `typing.TYPE_CHECKING`, `uuid.UUID`, and
`from packages.orchestration.storage import JobNotFoundError, load_job`, with
`import argparse` under `if TYPE_CHECKING:`. Give it a module docstring that says WHY it exists —
that `packages.orchestration.context_pack` is cluster-bound, that this file is therefore listed in
`CLUSTER_COMMAND_HANDLERS` and dies with the module, and that the command id is unchanged.

CREATE `apps/cli/commands/context_optimizer_cmd.py`. Same shape, holding `_cmd_context_explain`
and `_cmd_context_optimize` moved byte-for-byte, and a `COMMAND_HANDLERS` dict holding
`"context.explain"` and `"context.optimize"` in that order, moved byte-for-byte. Same import set.
Its docstring additionally records the deliberate absence AGENTS.md's discoverability rules ask
for: these two are NOT put beside `context.pack` because that command is built on a DIFFERENT
cluster module, and one file per cluster module is what lets each be deleted on its own edge.

EDIT `apps/cli/commands/context.py`: delete the bodies of `_cmd_context_pack`,
`_cmd_context_explain` and `_cmd_context_optimize` and their `"context.pack"`,
`"context.explain"` and `"context.optimize"` dict entries. `_cmd_context_inspect` and the
`"context.inspect"` entry are the only ones that remain. Its module header is UNCHANGED —
`_cmd_context_inspect` still uses `UUID`, `load_job` and `JobNotFoundError`, so nothing there
becomes unused. Verify that rather than assume it.

### C5 — the worker split

CREATE `apps/cli/commands/worker_recommend_cmd.py`. It holds `_cmd_worker_recommend` and
`_cmd_worker_explain`, moved byte-for-byte out of `apps/cli/commands/worker.py`, and a
`COMMAND_HANDLERS` dict holding `"worker.recommend"` and `"worker.explain"` in that order, moved
byte-for-byte. Same import set as the two files above. Its docstring says why it exists and
records the measured fact that cutting this edge does NOT make `worker_recommend` deletable,
because three `packages/orchestration/` consumers still reach it.

EDIT `apps/cli/commands/worker.py`: delete the bodies of `_cmd_worker_recommend` and
`_cmd_worker_explain` and their `"worker.recommend"` and `"worker.explain"` dict entries. THEN
DELETE THE IMPORTED NAMES THAT BECOME UNUSED — `UUID`, `JobNotFoundError` and `load_job`, which
is the WHOLE of the line `from uuid import UUID` and the WHOLE of the line
`from packages.orchestration.storage import JobNotFoundError, load_job`, both removed entirely —
because the two moved bodies were their only users in that file. Leaving them turns
`python3 -m ruff check .` from 26 errors to 29, reported as three `F401` diagnostics against that
file, and breaks the ceiling DECISION F083 D5 freezes; the reviewer measured exactly that at
`57d6698bf0af530dedd3d4df4b82cfb17163ba6b` before authoring this block. `_json`, `sys`,
`Callable`, `TYPE_CHECKING` and `argparse` all stay in use and are NOT removed.

### The wiring both commits share

Each commit carries its OWN share of the four wiring edits, so that each commit is green on its
own and the map ratchet proves the cut in the commit that makes it:

`apps/cli/commands/__init__.py` — add each new module to BOTH lists inside
`collect_all_handlers()`: the alphabetical `from apps.cli.commands import (...)` block and the
`for mod in (...)` tuple that merges every `COMMAND_HANDLERS`. A module missing from the tuple is
never dispatched and its command ids vanish from the table.

`tests/orchestration/test_cluster_deletion_map.py` — add each new module's repo-relative path to
`CLUSTER_COMMAND_HANDLERS`, keeping that tuple sorted. Without this the moved import registers as
a NEW edge and the map test reds with `APPEARED`.

`tests/orchestration/cluster_deletion_map.txt` — delete the edge lines the commit cuts. C4 deletes
the two `<- apps/cli/commands/context.py` lines; C5 deletes the one
`<- apps/cli/commands/worker.py` line. Leaving a line behind reds the map test with `DISAPPEARED`,
which is the ratchet working and is this round's own proof that the edges were really cut.

`tests/orchestration/import_reachability_allowlist.txt` — add each new module's DOTTED name,
keeping the file sorted. The new modules are reachable from the D11 (c) entry points through
`collect_all_handlers()`, so omitting them reds
`test_no_module_outside_the_allowlist_is_reachable_from_the_entry_points`.

### The guards over these two files, read at the base before this block was written

Both surviving files are already guarded, and neither guard obstructs this change — the reviewer
read each at `57d6698bf0af530dedd3d4df4b82cfb17163ba6b` rather than assuming it, and states what
it found so you do not have to rediscover it. `tests/orchestration/test_command_discovery.py`
carries `test_no_shell_true`, which reads `apps/cli/commands/worker.py` AS TEXT and asserts no
line contains `shell=True`; the moved bodies contain no such line and the surviving
`_cmd_worker_unload` and `_cmd_worker_resources` already satisfy it, so the guard passes
unchanged. `tests/cli/test_context_inspect_cli.py` carries `test_context_inspect_in_handlers`,
which asserts `"context.inspect" in COMMAND_HANDLERS` — a MEMBERSHIP test, not an equality over
the key set, so removing the other three keys does not red it. Every other test naming either
module imports only a SURVIVING handler: `_cmd_worker_unload` and `_cmd_worker_resources` in
`tests/orchestration/test_command_discovery.py` and `tests/storage/test_persistence.py`, and
`_cmd_context_inspect` in `tests/cli/test_context_inspect_cli.py`. No test imports a moved
handler by name, and there is NO directory-completeness guard over `apps/cli/commands/` that a
new file would trip.

## Constraints

1. Apply every authored TEXT byte for byte. If a text cannot be applied as given, STOP and
   declare it; never adjust it to fit.
2. Commit in the order C0a, C0b, C1, C2, C3, C4, C5, C6 and in no other. C1 advances the plan
   before any substantive commit, per §3 item 23, and only the two block-save commits precede it.
3. RECORD4 is appended to the END of `.agent/live_review.md`, which is where the append-only
   findings region ends. At the base that file is 522330 bytes and ends with a single newline.
4. RECORD4 states facts about THIS round's own commits nowhere; every reading in it was taken by
   the reviewer at a commit that already existed when it was written, and each such sentence
   names its SHA.
5. `.agent/prose_slips.md` is append-only and NOTHING in this block gates it. It is never a block
   condition, by the rule that created it.
6. No command id is added, removed or renamed. The dispatch table `collect_all_handlers()`
   returns 341 entries at the base and must return 341 at C5.
7. Do not run `ruff --fix`. The 26 pre-existing errors are a frozen ceiling, not a backlog; touch
   none of them.
8. Destructive verification runs ONLY inside a disposable `git worktree`, never in the primary
   checkout, which satisfies `git status --porcelain` empty at every commit boundary. Remove and
   prune the worktree before the handback.
9. The four state readers are run as FOUR, not as three.
10. Bare `ruff` is denied to this session's shell; every lint command is spelled
    `python3 -m ruff check <path>`.

## Done when

Run every gate, record its REAL exit code, and give each one line in the handback. G1 through G7
are ordered at commits that PRECEDE C6, so C6 can quote them.

G1 TRANSPORT (after C0b). `.agent/authored/f274-r4.md` and `.agent/last_block.md` are
byte-identical to each other and to the reviewer's scratch original
`.remedy-wt/f274-r4-block.md`; report the shared byte length and the shared sha256. This chain
covers those three artefacts and claims nothing about the bytes emitted into your prompt.

G2 THE RECORD APPEND (C2). (a) BYTE: the pre-image of `.agent/live_review.md` is a byte-exact
PREFIX of the post-image, and the post-image equals the pre-image plus RECORD4 exactly, with no
separator newline added. (b) STRUCTURAL, independently of (a): splitting BOTH images on the blank
line, the last N blank-line units of the post-image equal RECORD4's N paragraphs IN ORDER, where
N is a number your script COUNTS from the slice and never one this block asserts, and every unit
before those N is unchanged. State the unit definition your reader used. (c) NEGATIVE CONTROL:
flip one byte inside the FIRST appended paragraph and confirm BOTH readers reject it, then
confirm the file on disk is unchanged. (d) COUNTS across the commit: `^- R-\d+ — ` distinct
registrations, `^Done: R-\d+ — ` distinct resolutions, the OPEN SET BY DISTINCT ID, `^Gate: `,
and `^Gate: F274 R3` — report each as before-to-after. At the base the open set is 62 by distinct
id, 65 distinct registrations against 3 distinct resolutions, and `^Gate: ` is 34.

G3 THE PLAN (C1). `.agent/plan.md` is byte-equal to PLANF274R4; report its line count against the
cap of 50, and confirm it carries `## Goal` and `## Next Steps`.

G4 THE EDGE CUT IS REAL, AND THE RATCHET IS PROVED BOTH WAYS IN A DISPOSABLE WORKTREE AT C5.
Report, in this order: (a) the UNMUTATED control — `tests/orchestration/test_cluster_deletion_map.py`
and `tests/orchestration/test_import_reachability.py` run in ONE command, with exit code and
passed count; running them together is what proves the map test's reuse import resolves under
collection. (b) The measured edge count and the recorded edge count, which must be EQUAL, and the
number of cluster modules carrying at least one edge. (c) RED, map: append the three deleted edge
lines back to `tests/orchestration/cluster_deletion_map.txt` and report the exit code and the
`DISAPPEARED (n)` figure; restore that one file by exact path and confirm exit 0 again. (d) RED,
handlers: delete the line `    "apps/cli/commands/worker_recommend_cmd.py",` from
`tests/orchestration/test_cluster_deletion_map.py` — count those exact bytes in that file first
and confirm the count is 1 — and report the exit code and the `APPEARED (n)` figure; restore and
confirm exit 0. (e) RED, allowlist: remove the three added dotted names from
`tests/orchestration/import_reachability_allowlist.txt` and report the exit code of
`tests/orchestration/test_import_reachability.py`; restore and confirm exit 0.

G5 THE LINT CEILING AND THE BUDGETS. Report `python3 -m ruff check .` TWICE, and report the
mechanism for each rather than leaving the route to be invented. The BASE reading is taken in a
disposable `git worktree` checked out at `57d6698bf0af530dedd3d4df4b82cfb17163ba6b`, with the
command run from that worktree's own root so `pyproject.toml` and its `per-file-ignores` resolve
against the same paths; nothing in the primary checkout is overwritten to obtain it. The HEAD
reading is taken in the primary checkout at C5. Both must read 26 errors. Report both numbers,
not one, and report the exit code of
`python3 -m pytest tests/orchestration/test_ci_budgets.py -q`, which must be 0.

G6 THE DISPATCH TABLE IS INTACT (at C5). Through the SHIPPED reader
`apps.cli.commands.collect_all_handlers`, report the table size — 341 at the base — and confirm
each of `context.pack`, `context.explain`, `context.optimize`, `context.inspect`,
`worker.recommend`, `worker.explain`, `worker.list` and `worker.status` is present. Report the
size as before-to-after.

G7 THE SUITES, run SERIALLY in the PRIMARY CHECKOUT, each with its own exit code and passed
count: `tests/orchestration/test_cluster_deletion_map.py`,
`tests/orchestration/test_import_reachability.py`,
`tests/orchestration/test_command_discovery.py`, `tests/cli/test_context_inspect_cli.py`,
`tests/storage/test_persistence.py`, the four state readers `tests/ui_server/`,
`tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py` and
`tests/orchestration/test_integrity_gate.py`, and the canary `tests/cli/test_golden_path.py`.

G8 THE TREE AND THE COMMITS. `git status --porcelain` is EMPTY at every commit boundary;
`git ls-files .remedy-wt` is empty; report `git worktree list` counts before and after; report
`git diff --name-only 57d6698bf0af530dedd3d4df4b82cfb17163ba6b..<C6>` and confirm it names
exactly the change set above and nothing else; report the insertion count of each commit C0a
through C5 against the DECISION F104 D1 cap of 500. C6's own numbers go in the handback's
`## Commits` table, and the reviewer measures them at the next gate.

## Handback

Rewrite `.agent/handoff.md` in full per docs/agents/handback_template.md: feature and round, the
SESSION NUMBER of the running feature — this is SESSION 3 of F274 — branch, commit SHAs, the
changed-files table with its `+/-` column taken from `git diff --numstat` and compared cell by
cell against the per-commit numbers G8 reports, one line per gate with its real exit code, the
open-findings count, every deviation, the item-status table AGENTS.md requires, and the next
expected action. There is no length cap. Push the branch. Do NOT create a pull request and do NOT
merge anything.

<<<BEGIN PLANF274R4 whole-text
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 4: cut three of the deletion map's forty-two edges. `apps/cli/commands/context.py` and
`apps/cli/commands/worker.py` each host both surviving and cluster-bound commands; move the
cluster-bound handlers into three new files that are themselves cluster-bound, so their imports
die with the cluster instead of blocking it. Book round 3's PASS verdict. Nothing is deleted and
no command id changes.

## Next Steps

1. The remaining edge cuts the map records, module group by module group. The two modules with no
   edge at all, `review_bundle` and `self_repair_proposal`, are deletable whenever the deletion
   itself may start.
2. The first carry-over, on the route DECISION F274 D2 fixes: the read-only overnight readiness
   and report views survive as `mission readiness` and `mission report`, the latter only in the
   commit that deletes the cluster-bound command already holding that name.
3. Draft DECISION F260 D3, the deletion paragraph, naming every deleted module and the feature
   that inherited its idea. Nothing is deleted before it exists.
4. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
5. T001 — measure the `Job.id` flip with a recording property, rule the cap route, and rule the
   persisted key: `Job` stores its identity under the JSON key `"id"`, so renaming the field
   alone makes a stored job load with a FRESH id.
6. T002 — the classic runner and the resolver collapse.

## Risks

- The deletion reaches further than F260's Design describes: of the catalog's 341 command ids,
  311 resolve to an owning handler file and 105 of those sit in one of the 21 files that import a
  cluster module, `mission.run` and `mission.report` among them.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
<<<END PLANF274R4>>>

<<<BEGIN RECORD4 findings-append

Gate: F274 R3 — the F274 round 3 entry. VERDICT PASS. THIS ENTRY IS BOOKED BY ROUND 4 RATHER THAN BY ROUND 3, under operator amendment amend0827-process-diet rule 1: the verdict was written into `.agent/handoff.md` at `9d58db022fca1df933f0b47f24f390841b4d3e7b`, committed and pushed, and a pushed handback is a durable carrier that is booked into the first commit of the next round that is happening anyway. IT IS ALSO BOOKED BY A DIFFERENT SESSION FROM THE ONE THAT ISSUED IT, AND THIS ENTRY SAYS SO PLAINLY RATHER THAN LETTING THE RECORD IMPLY OTHERWISE: the session-2 reviewer issued the verdict after re-running every gate itself, in the primary checkout and in a disposable worktree, against the committed blobs rather than the working tree, and the figures below are ITS measurements as its pushed handback carries them, not a second re-run by the session-3 reviewer. What the session-3 reviewer did independently re-measure at `57d6698bf0af530dedd3d4df4b82cfb17163ba6b` is stated as such at the end of this entry. G1 TRANSPORT: `.remedy-wt/f274-r3-block.md`, `.agent/authored/f274-r3.md` and `.agent/last_block.md` are all 28580 bytes and all hash to `7138ea1b960639e12b0a70d5b641440225b365761cfafbac8a14e16e50bc1e9f`; per §3 item 37 that chain covers those three artefacts and claims nothing about emitted bytes. G2 THE RECORD APPEND: the head region is byte-identical across the commit, the findings pre-image is a byte-exact prefix of the post-image, the post-image equals the pre-image plus the RECORDR3 slice, N counted from the slice is 2, the last two units match in order, and the negative control flipped at byte 515000 — inside the FIRST appended paragraph, the append beginning at 514989 — is rejected by BOTH readers with the disk unchanged; registrations 64 to 65, resolutions 3 to 3, OPEN SET 61 TO 62 BY DISTINCT ID, `^Gate: ` 33 to 34, `^Gate: F274 R2` 0 to 1, `^- R-0831` 0 to 1. G3 THE DECISION APPEND: prefix true, post equals pre plus the slice, `^## DECISION F274 D` 1 to 2, and `^## DECISION F274 D2 ` heads exactly one section. G4 THE DELETION MAP IS A REAL RATCHET AND THE SESSION-2 REVIEWER PROVED IT BOTH WAYS IN ITS OWN DISPOSABLE WORKTREE AT `0d6da86f`: the test alone is EXIT 0 at 3 passed and, run in ONE command with `tests/orchestration/test_import_reachability.py`, EXIT 0 at 6 passed, which is what proves the reuse import resolves under collection; with a single `review_bundle` import appended to `packages/orchestration/data_paths.py` it is EXIT 1 reporting `APPEARED (1)` and naming that exact edge, and EXIT 0 again after restoring that one file by exact path; with one bogus line added to the map it is EXIT 1 reporting `DISAPPEARED (1)`, and EXIT 0 again after removing that one line. The map holds 42 edges over 22 of the 24 cluster modules from 16 distinct surviving consumer files. `python3 -m ruff check .` reports 26 both before and after, so the frozen ceiling DECISION F083 D5 protects is untouched, and `test_ci_budgets.py` is EXIT 0 at 10 passed. G5: `.agent/plan.md` is byte-equal to its slice at 40 lines against the cap of 50. G6 THE SUITES, re-run serially in the primary checkout, every one EXIT 0: `tests/ui_server/` 515 passed, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, and the canary `tests/cli/test_golden_path.py` 42 passed. Seven commits, every one single-parent, every one under the 500-insertion cap, the tree empty at every boundary, `git ls-files .remedy-wt` empty and worktrees 14 to 15 to 14. SIX DEVIATIONS WERE DECLARED AND THE SESSION-2 REVIEWER SUSTAINED ALL SIX; THE ONE THAT MATTERS IS DEVIATION 3, resolved in the reviewer's favour on a re-measurement rather than on authority. The worker could not reproduce the claim, carried in DECISION F274 D2 and in `.agent/plan.md`, that 105 of the catalog's 341 command ids sit in a handler file importing the cluster, and reported 134 and 26 under two other attributions. The reviewer re-measured with an owner map built by `ast` from every COMMAND_HANDLERS-shaped dict literal under `apps/cli/commands/` rather than by regex, and reproduced 105 exactly: of 341 catalog ids, 311 resolve to an owning handler file, and 105 of those sit in one of the 21 files that import a cluster module. The worker's 26 is the sharper figure and is not in conflict — it is the subset owned by files that are NOT among the 17 pinned cluster-command handlers. The landed sentence is true; what it omitted is the ATTRIBUTION METHOD, which is why it was not reproducible, and that omission is a reviewer prose defect recorded as a dated `.agent/prose_slips.md` line rather than an id, per amend0827 rule 2, because nothing on disk is wrong. THREE THINGS THE ROUND-3 HANDBACK COULD NOT CARRY ARE MEASURED HERE INSTEAD, per §3 item 31, because under `docs/agents/self_drive_protocol.md` there is no round report that survives a session: the round's own handback commit `9d58db022fca1df933f0b47f24f390841b4d3e7b` writes `.agent/handoff.md` at +222/-303, the session-end handoff commit `57d6698bf0af530dedd3d4df4b82cfb17163ba6b` writes the same file at +208/-268, and `git diff --name-only 4ba5e0f6df26fbf0ed791f1eaa4d072d722802a6..57d6698bf0af530dedd3d4df4b82cfb17163ba6b` names exactly eight paths, six under `.agent/` and the two the deletion map shipped, with nothing under `packages/`, `apps/` or `docs/`. ONE CLAIM OF THE ROUND-3 HANDBACK IS FALSE AND THE SESSION-3 REVIEWER MEASURED IT AT `57d6698bf0af530dedd3d4df4b82cfb17163ba6b` RATHER THAN INHERITING IT: that handback's round-4 plan predicted the map would fall from 42 edges to 39 and the count of cluster modules carrying at least one edge from 22 to 20, "since `context_pack` and `worker_recommend` each lose their only recorded consumer". The edge figure is right and the module figure is wrong, because neither module loses its only consumer — `context_pack` keeps `packages/orchestration/ui_server.py`, `context_optimizer` keeps `packages/orchestration/project_brain.py`, and `worker_recommend` keeps `packages/orchestration/agent_loop.py`, `packages/orchestration/autonomy_loop.py` and `packages/orchestration/dashboard.py` — so the module count stays at 22 after the cut. The prediction was labelled a prediction and its round was ordered to measure rather than assert it, which is the system working; the false REASON beside it was a statement about the map that was already checkable when written, and it is a dated prose-slip line rather than an id because it left nothing wrong under `packages/`, `apps/`, `tests/` or `docs/`. NO FINDING IS RESOLVED BY THIS GATE and none is minted; R-0830 and R-0831 both stay open.
<<<END RECORD4>>>

<<<BEGIN SLIPS4 prose-slips-append

2026-09-07 · F274 R3 · The reviewer wrote a FABRICATED forty-character SHA into three separate slice locations of the round 3 block, inventing the trailing characters after a real short prefix; it was caught only by the pre-emission check that resolves every SHA with `git cat-file -t`, one step from landing a false identifier in an append-only record, and the counter-measure is that a SHA is pasted from a command's output and never completed from memory.

2026-09-07 · F274 R3 · The reviewer stated "105 of the catalog's 341 command ids sit in a handler file that imports the cluster" without stating HOW command ownership was attributed, so the worker could not reproduce it and spent a declared deviation reporting 134 and 26 under two other attributions; the figure was later reproduced exactly from an `ast`-built owner map, and the counter-measure is that a derived count carries its attribution method in the same sentence.

2026-09-07 · F274 R3 · The round 2 block's gate G3(b) ordered a comparison of blank-line separated units without DEFINING a unit, and the appended slice carries its own leading newline, so a reader that keeps boundary newlines rejects the true image while one that strips them accepts it; the worker hit exactly that, restored the file and re-ran the gate from clean, and the counter-measure is that a structural gate states the unit definition it is measured under.

2026-09-07 · F274 R4 · The session 2 handback's round 4 plan predicted the deletion map would fall from 42 edges to 39 and its module count from 22 to 20 "since `context_pack` and `worker_recommend` each lose their only recorded consumer", and that reason was already false against the map on disk: `context_pack` also has `ui_server.py`, `context_optimizer` also has `project_brain.py`, and `worker_recommend` has three further consumers, so the module count stays 22 while the edge figure was right; a prediction may be wrong, but the fact offered as its reason is checkable and gets checked.
<<<END SLIPS4>>>
