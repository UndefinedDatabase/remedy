── STEP T003 — F275 — ROUND 90 ──
Goal: Commit the flip's first OVERLAY — a unified diff applied after the transform to a flipped
tree at `844a7f21` — that loads the cockpit's job from the one store and renames the string
`getattr` reads the transform cannot see, and prove it by the full suite in fresh flipped trees.

Base commit: `844a7f21`. Round type: SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/`
or `scripts/` changes; the overlay is production code carried in a diff, so G4 to G6 give it
full forensics and a mutation red-proof.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r90.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN90, a full replacement
C2  `.agent/live_review.md`                   slice RECORD90 appended, the round 89 verdict
C3  `.agent/authored/f275-r90-overlay.md`     the overlay carrier, SPEC C over SPEC O
C4  `.agent/decisions.md`                     slice DEC90 appended
C5  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 after the transform

O1 `packages/orchestration/ui_server.py`. `_load_job(job_id_str)` imports `JobIdInvalid` and
`normalize_job_id` from `packages.orchestration.data_paths` and `load_job_plan` from
`packages.orchestration.pingpong_job`. On `JobIdInvalid` it returns `None` with
`_safe_error(404, "job not found")` when the string fully matches `[0-9a-fA-F]+`, else `None`
with `_safe_error(400, "invalid job id")`. Otherwise it calls `load_job_plan` on the normalized
id, reads an `OSError` as no record, returns `None` with `_safe_error(404, "job not found")` for
no record, and the record with `None` for one. No `UUID` call and no `_JobPlanAdapter` in it;
docstring `Load a job record by id, return (job, error_tuple).`; the module-level
`from uuid import UUID`, left unused, is deleted. Nothing else in the file changes.
O2 Every call of the builtin `getattr` whose first argument is the bare name `job`,
`previous_job` or `jref` and whose second is the string `"id"` or `"name"` reads `"job_id"` or
`"job_title"`; whose first is `t` or `task` and second `"id"` or `"description"` reads
`"task_id"` or `"title"`; in exactly these files, reviewer's count each:
`packages/orchestration/source_apply.py` 2, `patch_apply.py` 1, `repo_applicator.py` 1,
`diff_repair_apply.py` 1, `mission_state.py` 1 (the `previous_job` read), `run_report.py` 9,
`job_digest.py` 1, `real_test_execution.py` 1, all under `packages/orchestration/`, and
`apps/cli/commands/repo.py` 1. `mission_state.py`'s two reads inside the verify-first error
messages stay.
O3 `tests/orchestration/test_run_report.py`: `_FakeTask` sets `task_id` and `title` in place of
`id` and `description`; `_FakeJob` sets `job_id` and `job_title` in place of `id` and `name`,
its docstring ending `reads off a job record.`; the docstring `str(t.id)[:8]` reads
`str(t.task_id)[:8]`.

## SPEC C — the carrier, at C3

`.agent/authored/f275-r90-overlay.md` opens with prose: what an overlay is, its base
`844a7f21`, that the flipped tree is built as G4 of `.agent/authored/f275-r90.md` orders, that
it is the FIRST overlay and later ones apply after it, and how to apply it — extract the
fence, `git apply --check`, then `git apply`. Then exactly ONE fence: a line of three backticks and `diff`, the VERBATIM stdout of `git diff` in
the EDIT worktree taken after SPEC O and before any test runs there, and a line of three
backticks. Nothing after it but one newline.

## Constraints

1. NO SLICE IS EDITED. PLAN90, RECORD90 and DEC90 land byte for byte; a discrepancy inside one
   is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` is not
   opened.
3. READ `.agent/STOP` before C0a and before C5, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r90w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md` and `.agent/decisions.md` commits
   are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r90w/`,
   each transformed as G4 orders: EDIT, CONTROL and OVERLAY. Only EDIT receives SPEC O; only
   OVERLAY receives the carrier. All three are REMOVED AND PRUNED before C4, without `--force`.
   The generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 258 lines TOTAL and 190 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4, G5 and G6 run at C3, strictly before C4, because DEC90 quotes them, per item
    31 of §3. DEC90's figures and where each comes from: 752 is DECISION F275 D62's; 404, 400
    and the two doubles are SPEC O's; eighteen, nine and the two error-message reads G4
    produces; 650, 31, 681, 529, 560, 121 and 57 G5 produces; 85, four and 2 G6 produces. G1,
    G2, G3, G7 and G8 run at C4. No gate runs after C5; C5's own numbers are the reviewer's.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r90.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN90 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C4 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1128932 and 1277039 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. Derive the ledger's `Gate:` header pattern from the file, report how many heads it
matches, and that RECORD90's header matches it and duplicates none.

G4 THE FLIPPED TREES AND THE CARRIER, at C3. Build `tree_base` from `git archive ef75e213` and
`tree_tip` from `git archive 844a7f21`, then the shift and delete controls, the committed fences
extracted and the generator run, all exactly as round 87's block G4 orders, with the pinned
`/home/decodeux/Repos/remedy/.remedy-wt/r77_corrected.json` sha256 765b5ba9…, its owners file
sha256 670c6e95… and `/home/decodeux/Repos/remedy/.remedy-wt/r61_status.json` sha256 a4c6cd63…
checked first. The reviewer measured: 56 paths differing between BASE and TIP; 2183 ruled sites,
all recovered by the scope key at TIP, SHIFT and DELETE, 0 UNRESOLVED; the line-key control 1895,
1886 and 1886; the owner check at TIP 1908 CONFIRMED, 275 REFUSED, 0 CONTRADICTED. Run the
transform in each of the three worktrees with the TIP re-keyed set, its owners file and
`r61_status.json`: 2183 resolving and 0 not, 264 files, 6097 rewrites, 0 broken, in each. In
EDIT, `git add -A` before SPEC O. Then: (a) the fence extracted from the COMMITTED C3 blob; in
OVERLAY `git apply --check` exit 0, then `git apply` exit 0; the paths `git diff --name-only`
lists there are exactly SPEC O's eleven, each byte-identical to EDIT's. (b) With `ast`, in the
nine O2 files, `getattr` calls whose first argument is a bare name among `job`, `t`, `task`,
`previous_job` and `jref` and whose second is a string constant: reading `id`, `name` or
`description`, 19 in CONTROL and 1 in OVERLAY; reading `job_id`, `job_title`, `task_id` or
`title`, 0 and 18. In OVERLAY's `mission_state.py` the calls reading `description` with the
default `'?'` count 2. In `_load_job`: calls named `UUID` 1 and 0, `normalize_job_id` 0 and 1,
`load_job_plan` 2 and 1, `_JobPlanAdapter` 1 and 0; module-level `from uuid` imports 1 and 0.
(c) `ruff check --output-format concise --stdin-filename <path> -`, run from inside each
worktree, over the eleven files in CONTROL and in OVERLAY, rows as a MULTISET: added 0; the reviewer read 4 rows and 3, the one
removed an `I001`.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, at C3, CONTROL first and OVERLAY second, serially.
Each run is its worktree's FIRST full run, `apps/ui/node_modules` and `apps/ui/dist` reported
absent before it: the first full run in a worktree installs both, which unskips six tests and
turns `test_vitest_passes` green, so a second run is not comparable. `cwd` the worktree;
`PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.ui_server.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. The reviewer
measured CONTROL `650 failed, 17755 passed, 29 skipped, 1 warning, 31 errors`, 681 distinct
FAILED/ERROR node ids; OVERLAY `529 failed, 17876 passed, 29 skipped, 1 warning, 31 errors`, 560;
bad only in CONTROL 121, only in OVERLAY 0; the 121 by test file: `tests/ui_server/`
`test_command_channel.py` 57, `test_command_dispatch.py` 11, `test_diff_endpoint.py` 6,
`test_live_state.py` 4, `test_decisions_endpoint.py` 2, `test_digest_route.py` 2,
`test_dashboard_contract.py` 1; `tests/orchestration/` `test_run_report_hook.py` 16,
`test_job_digest.py` 6, `test_fence_e2e.py` 2; `tests/cli/` `test_job_report.py` 8,
`test_command_catalog.py` 3, `test_job_commands.py` 2; `tests/ui_contracts/test_ux_quality.py` 1.

G6 THE RED-PROOF, at C3, in OVERLAY after G5; `__pycache__` purged before each run; selection
`tests/ui_server/test_command_channel.py`, `tests/ui_server/test_digest_route.py`,
`tests/orchestration/test_job_digest.py`, `tests/orchestration/test_run_report_hook.py`, with
G5's environment and flags `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. CONTROL: the
reviewer's read `7 failed, 174 passed`. M1: in `_load_job`, the one line calling `load_job_plan`,
its bytes counted in the file as 1 first, has that argument wrapped as `__import__("uuid").UUID(<argument>)`;
the reviewer's read `92 failed, 89 passed, 85 warnings`, 85 newly bad, 0 recovered. M2: in
`packages/orchestration/job_digest.py` the one `getattr` reading `job_id`, its bytes counted
in the file as 1 first, reads `id`; the reviewer's read `9 failed, 172 passed`, newly bad exactly
`test_cost_basis_is_actual_when_every_call_is_priced` and
`test_cost_basis_is_lower_bound_when_calls_are_unpriced` of `test_job_digest.py`. After each,
restore and confirm the file's bytes equal the carrier-applied ones.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C4. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only 844a7f21 C4 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `844a7f21`, read from a `git archive`
tree, and at C4, difference empty, 26 at `844a7f21`. The changed-path set of `844a7f21`..C4
against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name. The open set BY
DISTINCT ID at `844a7f21` and at C4: 88 at both, membership identical; `R-0809`, `R-0880` and
`R-0883` open.

G8 THE INSERTION CAP over `844a7f21`..C4: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 31 of feature F275 · round 90 · rounds so far 90`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C5's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN90 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN90 sha256=9a9215f7264417fd8b49c1954a4acb4e11bdbc93af9ca84720d00b0f99860ddd
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 90 STARTS THE FLIP'S OVERLAY. An edit that is right only once the classic record is gone
no longer waits for the flip round: it is committed as a unified diff under `.agent/authored/`,
applied after the transform to a flipped tree at `844a7f21`, and proved by the full suite in
that tree against the transform alone. The first overlay makes the cockpit's `_load_job` load
every well-formed id from the one store, and renames the string `getattr` reads of a job or task
field that the transform cannot see. No path under `packages/`, `apps/` or `tests/` moves. The
round books the round 89 verdict and records the method as a dated decision.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it: the
   pydantic calls made on the unified records, such as `TaskEntry.model_validate` and
   `JobPlan.model_dump_json`; the classic `Task` constructions that pass `acceptance_checks`;
   `UUID` values reaching the unified record; what is left of the classic runner under
   `job resume`; and the duck-typed test doubles, including the `_FakeJob` behind the ruled
   site at `packages/orchestration/project_registry.py:856`.
2. THE FLIP: the transform, then every overlay in round order, landed as a series of commits
   each under the 500-insertion cap inside one round, carrying DECISION F275 D48's obligations,
   unless the operator allows one more oversized commit.
3. Then the classic store, with the which-store branches and adapters in `ui_server.py` the
   first overlay leaves unreached, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: several hundred test nodes still fail in the flipped tree.
- AN OVERLAY IS A DIFF AGAINST A FIXED TREE: it holds only while the production tree stays at
  `844a7f21`, and it depends on the generator and transform staying reproducible from round
  77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN90

── SLICE RECORD90 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD90 sha256=bb11e112ee3c0633a3ed45056c15fdca2a20b72256be573c56ec91a11360957c

Gate: F275 R89 — the F275 round 89 entry. VERDICT PASS. Written by the planner and reviewer of session 30 after reading the committed range `5bff6960`..`2565697d` and RE-DERIVING EVERY GATE AND THE RED-PROOF INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 90 that writes the record, per operator amendment amend0827-process-diet rule 1.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/` blob was identical to the reviewer's own original at 20405 bytes, `.agent/last_block.md` equalled it, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN89. The three appends were exact under reader A — 1125943 plus 2989 into the review record, 298762 plus 497 into the prose slips, and 1273941 plus 3098 into the decisions — with reader B holding at N counted from each slice as 4, 1 and 7, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path except C5, which staged the twenty test files, and the largest commit was 235 insertions.

THE CHANGE HOLDS UNDER THE REVIEWER'S OWN RE-RUN. C4 changes exactly one line of `run_job_fulfill`, `task_id=str(UUID(td["model_task_id"]))` to `task_id=td["model_task_id"]`. In each of C5's twenty test files the abstract syntax tree outside import statements is identical to the one at `5bff6960` once every `UUID(...)` argument of `load_job`, `load_job_safe` or `append_run_event` is read as `normalize_job_id(...)`; that accounts for 68 replacements and leaves none unreplaced, so no assertion changed. Unflipped in the primary checkout the twenty files read 711 passed and the scoped suite 13278 passed, 10 skipped and 0 failed, the same totals as at the base; `ruff check` over the touched paths passed, `ruff check .` read 26 rows, and the canary read 42. The reviewer rebuilt the flip from the committed C5 with the committed generator and transform: the twenty files read 82 failed, 598 passed and 31 errors, 113 bad nodes against 179 in the reviewer's own flip of `5bff6960`, 66 fixed and none new, with 2 `badly formed hexadecimal UUID string` lines against 93. Inside that flipped C5, restoring the round trip took `test_dod_gate.py` and `test_job_fulfillment.py` from 26 failures to 45, with the parse error raised at that line 41 times. The open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.
END RECORD90

── SLICE DEC90 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC90 sha256=4f9fdd0d02e28208f74c909859de43e4391339b3caa49c2e74cfb8e93fd810ba

## DECISION F275 D64 (2026-09-13, F275 round 90) — an edit that is right only after the flip is committed before it as an overlay, a unified diff applied after the transform and proved by the full suite in a flipped tree; the first loads the cockpit's job from the one store and renames the string `getattr` reads the transform cannot see

CONTEXT. DECISION F275 D62's flipped full suite had 752 bad nodes, and DECISION F275 D63 removed a further group. Before this round was authored the reviewer re-derived the flip at `844a7f21` with the committed generator and transform and classified the full suite in the flipped tree. Most of what remains cannot be repaired before the flip. The cockpit's `_load_job` still chooses a store by the id's shape, so a job the flip mints a sixteen-hex id for comes back wrapped in `_JobPlanAdapter`, whose attributes the transformed readers no longer name, and a `UUID`-shaped id reaches `load_job_plan` as a `UUID` object. A read written `getattr(job, "id", ...)` names its field in a string the transform does not rewrite. The unified records carry no `model_validate` or `model_dump_json`, and classic `Task` constructions pass `acceptance_checks`. Each of those edits is right only once the classic record is gone, and a reader accepting both records is what DECISION F275 D61 rejected under AGENTS.md Scope Control. The readings in CHOSEN, THIRD are the reviewer's at `844a7f21`, and the gates that constraint 10 of round 90's block runs before the commit landing this paragraph reproduce them.

CHOSEN, FIRST: SUCH AN EDIT IS COMMITTED BEFORE THE FLIP AS AN OVERLAY. An overlay is a carrier under `.agent/authored/` holding one unified diff, taken against the flipped tree at `844a7f21` with every earlier overlay applied in round order. The round that adds one runs the full suite in two fresh flipped worktrees, one carrying the chain before it and one carrying the chain with its own overlay, and reads the difference as two sets of test nodes. The flip round applies the transform and then the chain, and lands the result under the cap as DECISION F275 D61 rules. ALTERNATIVES: a pre-flip production round, rejected for these groups because each edit is wrong while the classic record lives; the repair inside the flip round, rejected by D61 because hundreds of failures inside one commit series is a round no worker can finish; a branch of red commits merged back later, rejected because guardrail G1 of the self-drive protocol allows a merge only at the Open PR Gate.

CHOSEN, SECOND: THE PRODUCTION TREE STAYS AT `844a7f21` UNTIL THE FLIP. An overlay's context lines are bytes of that tree after the transform, so no path under `packages/`, `apps/` or `tests/` moves before the flip round. A repair that cannot wait first shows that every overlay still applies with `git apply --check` to the flipped tree at its own base, and moves the chain's base to that commit in a dated decision.

CHOSEN, THIRD: THE FIRST OVERLAY IS `.agent/authored/f275-r90-overlay.md`. `_load_job` checks the id with `normalize_job_id`, answers 404 for a well-formed id no record holds and for any other string of hex digits, 400 for anything else, and otherwise returns the record `load_job_plan` reads, with no `UUID(...)` call and no adapter. Eighteen string `getattr` reads of `id`, `name` or `description` on a job or a task in nine modules take the transform's own mapping to `job_id`, `job_title`, `task_id` and `title`; the two inside `mission_state.py`'s verify-first error messages are left to the overlay that rewrites that module's task construction. The two duck-typed doubles of `tests/orchestration/test_run_report.py` carry the unified names. In fresh flipped worktrees the transform alone reads 650 failed and 31 errors, 681 bad nodes, and with the overlay 529 failed and 31 errors, 560 bad nodes: 121 nodes are fixed, 57 of them in `tests/ui_server/test_command_channel.py`, and none is newly bad. In the overlay's tree, handing `load_job_plan` a `UUID` again makes 85 nodes of four test files bad, and reading the job id as `id` again in `job_digest.py` makes 2.

CONSEQUENCE. After the flip `_JobPlanAdapter`, `_JobPlanTaskAdapter` and the trace dashboard they feed are reached by no id, so a job-flow job opens the one job dashboard. Deleting them, and deciding whether the trace phases move into that dashboard or are registered as a loss, belongs to the round that deletes the which-store branches with the classic store; so do the readers in `decision_inbox.py`, `decision_queue.py`, `job_context_cmd.py` and `escalation.py` that accept either spelling. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete `.agent/authored/f275-r90-overlay.md` and this paragraph block. The flip then carries these groups again, and the choice between a pre-flip round and a repair inside the flip returns to DECISION F275 D61.
END DEC90
