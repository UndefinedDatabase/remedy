── STEP T003 — F275 — ROUND 86 ──
Goal: Route the last handler job-id parses under `apps/cli/` so that no `UUID(...)` call feeds
`load_job`, without letting any handler file a job under an id it did not resolve; pin every
reachable site with a test its own restored parse fails; register the crash found beside them.

Base commit: `b0ef6ab4`. Round type: SPLIT. Production code changes, so the red-proofs of G6 are
mandatory in full.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r86.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN86, a full replacement
C2  `.agent/live_review.md`                   slice RECORD86 appended, the round 85 verdict
C3  `.agent/live_review.md`                   slice FIND86 appended, registering `R-0883`
C4  `.agent/prose_slips.md`                   slice SLIPS86 appended
C5  the handler files F1 to F7 of SPEC F       the production change, ONE commit
C6  `tests/test_data_paths.py`                SPEC T
C7  `.agent/decisions.md`                     slice DEC86 appended
C8  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. RECORD86 and SLIPS86 are the round 85
verdict and the slip lines carried in `.agent/handoff.md` at `b0ef6ab4`, extracted by bytes.

## Change — exactly these paths and no others

The Bundle's paths. Under `apps/` exactly the paths F1 to F7 of SPEC F name; under `tests/` exactly
`tests/test_data_paths.py`. NOTHING under `packages/`, `docs/` or `scripts/`.

## What the reviewer measured before authoring, at `b0ef6ab4`

A census of every `UUID(...)` call under `apps/cli/` by what its value flows into reads 21: 12
are the argument of `load_job`, 8 parse a project id, 1 validates a task id. The twelve are
`dashboard_cmd.py` `_cmd_dashboard_project`, `job_stop_cmd.py` `_load_job`, `memory.py`
`_cmd_memory_candidates`, `_cmd_memory_approve_candidate` and `_cmd_memory_reject_candidate`,
`project.py` `_cmd_attach_project_job`, `readiness.py` `_cmd_readiness_project`, `repo.py`
`_cmd_commit_readiness`, and `review_cmd.py` `_cmd_review_run`, `_cmd_review_list`,
`_cmd_review_accept` and `_cmd_review_reject`. The reviewer applied SPEC F and SPEC T in a
disposable worktree: `ruff check` passed on every path of SPEC F and SPEC T, the scoped suite there read 13260
passed, 10 skipped and 1 failed, the failure being
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`,
which needs the gitignored `apps/ui/node_modules` a worktree lacks, and every mutation of G6
gave the colours G6 requires. `remedy dashboard project` crashes at its first import, which is
FIND86. `remedy job stop <32 unhyphenated hex>` on a classic job filed the stop under that
spelling, which DEC86 records.

## SPEC F — the handler files, at C5, and nothing else in them

F1 `apps/cli/commands/review_cmd.py`: delete `from uuid import UUID`; add
`from packages.orchestration.data_paths import lookup_job_id` as its own import group directly
after the standard-library group; each of the four lines `    job = load_job(UUID(args.job_id))`
becomes `    job = load_job(lookup_job_id(args.job_id))`.
F2 `apps/cli/commands/memory.py`: in each of the three memory-candidate handlers delete the
local `    from uuid import UUID` line and the blank line after it, and
`    job = load_job(UUID(job_id_str))` becomes `    job = load_job(lookup_job_id(job_id_str))`.
The module already imports `lookup_job_id`.
F3 `apps/cli/commands/repo.py`: delete `from uuid import UUID`, which nothing else uses;
`        job = load_job(UUID(job_id_str))` becomes `        job = load_job(lookup_job_id(job_id_str))`.
F4 `apps/cli/commands/dashboard_cmd.py`: delete `from uuid import UUID`, which nothing else uses;
`            j = load_job(UUID(jid))` becomes `            j = load_job(lookup_job_id(jid))`.
F5 `apps/cli/commands/readiness.py`: `            j = load_job(UUID(jid))` becomes
`            j = load_job(lookup_job_id(jid))`. The `UUID` import stays; the project id uses it.
F6 `apps/cli/commands/project.py`: add `from packages.orchestration.data_paths import lookup_job_id`
directly above the module's `from packages.orchestration.storage import` line. In
`_cmd_attach_project_job` the line `        job = load_job(UUID(job_id_str))` becomes the two lines
`        job_id = lookup_job_id(job_id_str)` and `        job = load_job(job_id)`;
`    added = attach_job(project, job_id_str)` becomes `    added = attach_job(project, job_id)`;
in the `Attached job` message `{job_id_str[:8]}` becomes `{job_id[:8]}`. The `job not found`
message keeps `job_id_str`. The `UUID` import stays.
F7 `apps/cli/commands/job_stop_cmd.py`: in `_load_job` delete `        from uuid import UUID` and the
blank line after it; `        core = load_job(UUID(job_id))` becomes `        core = load_job(job_id)`.
`_load_job` is NOT routed through the resolver: DECISION F275 D58 measured that doing so lets
a short id skip its caller's normalisation.

## SPEC T — `tests/test_data_paths.py`, at C6

Tests added to the existing class `TestRoutedHandler`, IN-PROCESS, each setting
`REMEDY_DATA_DIR` to `tmp_path` through `monkeypatch`; no existing test is edited or deleted.
T1 `test_a_loading_handler_hands_load_job_the_id_a_short_prefix_resolves_to`, parametrized with
the ids EXACTLY `review-run`, `review-list`, `review-accept`, `review-reject`,
`memory-candidates`, `memory-approve`, `memory-reject`, `commit-readiness`, one per F1 to F3
handler in that order. It writes `jobs/abcd1234-0000-0000-0000-000000000001.json`, replaces
`packages.orchestration.storage.load_job` through `monkeypatch.setattr` with a spy that records
`str()` of its first argument and raises a test-local exception, calls the handler with
`abcd1234` while suppressing that exception and `SystemExit`, and asserts the recorded list is
exactly the full id. The handlers import `load_job` inside the function, which is why the
module attribute is the one to replace.
T2 `test_project_readiness_hands_a_stored_pingpong_id_to_load_job`: a ping-pong record
`<jobs_dir>/<minted id>/job.json`, a `RemyProject` saved with that id in `job_ids`, the same spy,
and `_cmd_readiness_project(str(project.id), json_output=True)`; the recorded list is exactly
the minted id.
T3 `test_attaching_by_short_prefix_stores_the_full_job_id`: a saved classic `Job` and a saved
`RemyProject`; `_cmd_attach_project_job(str(project.id), <first eight characters of the job id>)`;
the reloaded project's `job_ids` equals `[str(job.id)]` and stdout names the first eight.
T4 `test_stopping_by_an_unhyphenated_id_files_the_stop_under_the_canonical_id`: a saved classic
`Job`; `_cmd_job_stop(job.id.hex)`; `stop_requested(str(job.id))` is not None and
`stop_requested(job.id.hex)` is None.
Module-level imports the tests need are added in the file's import block, sorted as ruff requires.

## Constraints

1. NO SLICE IS EDITED. PLAN86, RECORD86, FIND86, SLIPS86 and DEC86 land byte for byte; a
   discrepancy inside one is DECLARED, never repaired.
2. C5 and C6 are the worker's OWN code from the SPECs. The reviewer's dry-run files under
   `.remedy-wt/r86/` are not opened.
3. READ `.agent/STOP` before C0a and before C8, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path, except C5, which stages the paths F1 to F7 name; every
   commit stays under 500 insertions.
5. No `.py` under `.agent/`; scratch under `.remedy-wt/r86w/`, uncommitted.
6. No landed record is rewritten: every `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commit is an APPEND with a ZERO deletion column.
7. No `gh`, no `remedy` command outside a scratch probe, no pull request, no branch created or
   deleted, no merge, NEVER a force-push, no history rewrite.
8. The red-proof worktree is created with `git worktree add --detach` at C6 and REMOVED AND
   PRUNED before C7. The scoped suite runs in the PRIMARY checkout.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 291 lines TOTAL and 220 lines of
   PROSE, against the caps of 490 and 400.
10. THE GATES RUN AT TWO COMMITS. G4, G5 and G6 run at C6, because DEC86 at C7 carries their
    results and item 31 of §3 requires such a gate to run STRICTLY EARLIER. G1, G2, G3, G7 and
    G8 run at C7. No gate runs after C8; C8's own numbers are the reviewer's.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r86.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN86 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD, FULL FORENSICS, for each record append: C2 and C3 into
`.agent/live_review.md` and C7 into `.agent/decisions.md`. For each, read its pre-commit blob
with `git show` at that commit's PARENT and print its length; the first is 1114453 and the
decisions pre-commit length is 1260475. READER A with the arithmetic printed; READER B over the
file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by the
script; a letter flipped in the FIRST appended paragraph of each, REJECTED by both readers;
every deletion column 0. `.agent/prose_slips.md` at C4 equals its 295435-byte pre-commit blob
followed by exactly SLIPS86. Derive the ledger's `Gate:` header pattern from the file, report
how many heads it matches and that RECORD86's header matches it and duplicates none. Report
that after C3 exactly one line starts `- R-0883 — `.

G4 THE CHANGE, STRUCTURALLY, at C6, with `ast`. Under `apps/cli/`, every `UUID(...)` call
classified by what its value flows into — an argument of `load_job`, an argument whose source
names a project, anything else — with the counts at `b0ef6ab4`, read with `git show` into memory, and at C6; the reviewer measured
21 = 12 + 8 + 1 at `b0ef6ab4`, and at C6 the `load_job` count must be 0 and the others
unchanged. The number of `load_job(lookup_job_id(...))` calls under `apps/cli/`: 0 at
`b0ef6ab4`, 10 at C6. In each function the round changes, every LATER read of the
argument the load consumed at `b0ef6ab4`, listed by line at C6 with what reads it. `ruff check`
over every path C5 and C6 stage exits 0.

G5 THE BEHAVIOUR, at C6. (a) Every node id SPEC T adds PASSED, in the primary checkout, their count reported. (b) The
scoped suite `python3 -B -m pytest tests/test_data_paths.py tests/cli/ tests/orchestration/ -q -p no:randomly`
in the primary checkout, totals REPORTED AS MEASURED, failure set EMPTY; the reviewer measured
it in the primary checkout at `b0ef6ab4` at 13261 passed, 10 skipped and 0 failed; state and account for the difference.
(c) THE CLI PROBE of FIND86, in a scratch tree built with `git archive` at C6: run
`python3 -B -m apps.cli.grouped dashboard project 11111111-1111-1111-1111-111111111111` with
the working directory and `PYTHONPATH` both set to that tree and `REMEDY_DATA_DIR` to an empty
scratch directory; report the
exit code, the module `__file__` it imported, and the last stderr line verbatim.

G6 THE MUTATION RED-PROOFS, in the worktree of constraint 8, at C6. PRINT the `__file__` of
`apps.cli.commands.project` imported inside the worktree; it must lie inside it. Purge
`__pycache__` before each run. Selection: `tests/test_data_paths.py::TestRoutedHandler`,
`tests/cli/test_job_stop.py`, `tests/cli/test_golden_path.py::TestShortIdResolution` and
`tests/cli/test_review_cmd.py`. CONTROL, unmutated: every test PASSES. Then ONE mutation at a
time, each restored before the next, its target's occurrence count in the file reported first.
M1 to M4: the first, second, third, fourth `load_job(lookup_job_id(` in `review_cmd.py`; M5 to
M7: the first, second, third in `memory.py`; M8: the one in `repo.py`; M9: the one in
`readiness.py`; M10: the one in `dashboard_cmd.py` — each becomes `load_job(__import__("uuid").UUID(`.
M11: `job_id = lookup_job_id(job_id_str)` in `project.py` becomes
`job_id = str(__import__("uuid").UUID(job_id_str))`. M12: `attach_job(project, job_id)` in
`project.py` becomes `attach_job(project, job_id_str)`. M13: `core = load_job(job_id)` in
`job_stop_cmd.py` becomes `core = load_job(__import__("uuid").UUID(job_id))`.
REQUIRED: M1 to M8 each fail ONLY the T1 parameter of the same position; M9 fails only T2; M11
and M12 each fail only T3; M13 fails only T4; M10 fails NOTHING, because the handler dies at its
import before the load, which is FIND86. Report every failing node id and exit code per run.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C7. `git status --porcelain` prints `''`;
`git worktree list` one row; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`
exit 0, 42 at `b0ef6ab4`; `ruff check .` exit 1 with its rows cross-checked against its own
`Found <n> errors.` line, 26 at `b0ef6ab4`. The changed-path set of `b0ef6ab4`..C7 against the
Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name. The open set BY DISTINCT ID
at `b0ef6ab4`, after C3 and at C7: the reviewer measured 87 at `b0ef6ab4`; after C3 and at C7 it
must be 88 with `R-0883` the only id added; `R-0809` and `R-0880` open throughout.

G8 THE INSERTION CAP over `b0ef6ab4`..C7: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 30 of feature F275 · round 86 · rounds so far 86`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C8's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 0`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN86 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN86 sha256=4e7bff4bd9145799caeb9a1b367153bafa4119f8ca838181697c479b3ee569ce
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

ROUND 86 ROUTES THE LAST HANDLER JOB-ID PARSES. The twelve `load_job(UUID(...))` calls left under
`apps/cli/` stop parsing. Ten hand `load_job` what `lookup_job_id` resolves; `project attach-job`
resolves once and files the resolved id in the project; `job stop`'s loader loads the id exactly
as given, so its caller's normalisation still runs. Eleven of the twelve are pinned by a test
that fails when that site's parse is restored. The round registers `R-0883`, `dashboard project`
crashing on a module that never existed, for the findings paydown, and books the round 85
verdict and its prose slips.

## Next Steps

1. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, the input
   is re-derived by round 82's committed generator at the flip's own base, and any site fallen
   to zero witnesses is a stop. The stale test double at
   `packages/orchestration/project_registry.py:856` is updated in the flip's own commit.
2. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- ONE ROUTED LOAD IS REACHED BY NO TEST. `dashboard project` dies at its first import, so its
  load stays unproven until `R-0883` is repaired.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, and the re-key
  cannot see a deleted ruled site.
- The open set is 87 by distinct id at this round's base, with `R-0809` and `R-0880` open. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN86

── SLICE RECORD86 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD86 sha256=e2966bb0789a29b28efb099eace555f3512d14f2e5d47b85a5595162ac07ba71

Gate: F275 R85 — the F275 round 85 entry. VERDICT PASS. Written by the planner and reviewer of session 29 after reading the committed range `53659062`..`21b184c4` and RE-DERIVING EVERY GATE AND THE RED-PROOF INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is carried here because a verdict that stays in the session is lost, and it is booked into `.agent/live_review.md` by the FIRST SUBSTANTIVE COMMIT of round 86 that writes the record, per operator amendment amend0827-process-diet rule 1.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/` blob was identical by `cmp` to the reviewer's own original at 26157 bytes, `.agent/last_block.md` equalled it, all six slices matched their BEGIN-marker digests, and the block re-measured at 261 lines TOTAL and 187 PROSE. `.agent/plan.md` equalled its slice at 44 lines. All five appends were exact under reader A — 1107652 plus 3119, then plus 2322, then plus 1360 into the review record, 294305 plus 1130 into the prose slips and 1257440 plus 3035 into the decisions — with reader B holding at N counted from each slice as 4, 1, 1, 2 and 7, and a letter flipped in each FIRST appended paragraph rejected by both readers. Eight paths changed, every commit staging one, the largest 261 insertions.

THE REPAIR HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The production change is the one line SPEC F ordered: `_cmd_project_adopt` passes the resolved id to `load_job` as a string, and no `UUID(resolved_id)` call remains in it. Through the real CLI over trees built with `git archive`, `remedy project adopt 0123456789abcdef` exits 1 with an uncaught traceback ending `ValueError: badly formed hexadecimal UUID string` at `53659062` and exits 3 with `Error: job not found: 01234567` and no traceback at `86b86e23`. In a worktree whose module the reviewer printed as resolving inside it, the test class passes unmutated, and restoring `UUID(resolved_id)` fails only `test_adopting_a_pingpong_job_id_exits_cleanly_instead_of_crashing`, with `ValueError`. The census by flow reads 22 `UUID(...)` calls under `apps/cli/` at the base — 13 into `load_job`, 8 naming a project, 1 other — and 21 at C6 with the `load_job` count one lower. The scoped suite in the primary checkout read 13261 passed, 10 skipped and 0 failed, the base's 13260 plus the one new test; `ruff check .` rows compared as a multiset at the base and the tip differ by nothing; the canary read 42; and the open set went 87, then 88 with `R-0882` the only id added, then 87 with `R-0882` the only id resolved, `R-0809` and `R-0880` open throughout.

ONE FIGURE THE WORKER COULD NOT REPRODUCE, AND BOTH READINGS ARE TRUE. DECISION F275 D59 says the resolver sweep finds 64 calls; the worker, counting the three function names the same block's G4 names, measured 62. The reviewer measured both at `53659062`: 32 calls of `resolve_job_id`, 27 of `lookup_job_id` and 3 of `resolve_any_job_id` make 62, and `apps/cli/commands/decision.py` imports `resolve_job_id` under the alias `_rji` and calls it twice, which the reviewer's instrument followed and the worker's did not, making 64. The load-bearing figure — exactly one resolver result passed to a later `UUID(...)`, this site — agrees under both. D59 stays as landed; this entry is where its unit is stated.
END RECORD86

── SLICE FIND86 ── target `.agent/live_review.md` ── APPEND ──
BEGIN FIND86 sha256=984db7b72773e68337ab377ab8158c7b4a9cee0f4040b0edf6b8c52ea03ad188

- R-0883 — Medium, `remedy dashboard project` CRASHES ON EVERY CALL WITH `ModuleNotFoundError`, BECAUSE ITS HANDLER IMPORTS A MODULE THIS REPOSITORY HAS NEVER HELD. Raised by the planner and reviewer of session 30 of F275 while preparing round 86, from reading the handler whose job-id load that round routes. THE DEFECT: the first statement of `_cmd_dashboard_project` in `apps/cli/commands/dashboard_cmd.py` is `from packages.orchestration.project_store import load_project`; at `b0ef6ab4` no such file exists, and `git log --all -- packages/orchestration/project_store.py` lists no commit, so it never did. The import arrived with commit `007f7454`, and the catalog registers the handler as `dashboard.project`. MEASURED at `b0ef6ab4` through the real CLI against an empty data root: `python3 -B -m apps.cli.grouped dashboard project 11111111-1111-1111-1111-111111111111` exits 1 with an uncaught traceback ending `ModuleNotFoundError: No module named 'packages.orchestration.project_store'`. No other outcome is reachable, because the import runs before anything reads the argument. At `b0ef6ab4` no file under `tests/` names `_cmd_dashboard_project` or `dashboard.project`, which is why the suite is green. The body below the import is also written against a dictionary, `project.get("job_ids", [])`, while the project store this repository does hold, `packages/orchestration/project_registry.py`, has a `load_project` that takes a `UUID` and returns a `RemyProject` model, so the repair is more than the import line. WHY MEDIUM: a catalogued command that no input can make succeed; nothing is written and the exit is non-zero. WHY NOT F275's: its scope is the job-id seam and the record flip, and round 86 only routes the handler's job-id load like its neighbours', a routing no test can reach while the handler dies first. FIX: load the project through `project_registry` and read the model's `job_ids`, and pin the command with a test that runs the handler against a saved project holding one job. Owner: F273.
END FIND86

── SLICE SLIPS86 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS86 sha256=347e9cae0d9f4e356c790eb497dbd77a0f3b6057c29066ddc70a6b79fe4789f8

2026-09-12 · F275 R85 · Constraint 2 of the round 85 block told the worker "The reviewer's candidate is deleted", and the disposable worktree holding it was, but the scratch scripts that had applied the fix and inserted the test stayed on disk under `.remedy-wt/r85/`; the worker neither opened nor deleted them and declared it. THE RULE THAT FOLLOWS: a block asserts a state of the filesystem only after measuring it, and "deleted" names every path that carried the thing, not only the one that was removed.

2026-09-12 · F275 R85 · DECISION F275 D59 says the resolver sweep "finds 64 calls" while G4 of the same block defines the sweep over three literal function names, under which the count is 62; the difference is two calls through an import alias the reviewer's instrument followed and the definition did not mention. THE RULE THAT FOLLOWS: a count states its definition beside it — here, whether import aliases are followed — because two correct instruments disagreeing on an unstated definition is indistinguishable, on the page, from one of them being wrong.
END SLIPS86

── SLICE DEC86 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC86 sha256=c5fb18281405f656bb31a5e40111f081d67b6642ab5acb2beb8f3c3878285cb4

## DECISION F275 D60 (2026-09-13, F275 round 86) — the last handler job-id parses stop parsing: ten load what the raising lookup resolves, `project attach-job` files the id it resolved, and `job stop`'s loader loads exactly what it is given

CONTEXT. DECISION F275 D59 counted twelve `load_job(UUID(...))` calls left under `apps/cli/` by flow, and DECISION F275 D58 had held them back because routing `job stop`'s loader let a short id skip its caller's normalisation. Before this round was authored the reviewer applied the change below in a disposable worktree at `b0ef6ab4`, ran the scoped suite there, and restored each changed site's parse one at a time against the new tests; the choices below rest on those runs.

CHOSEN, FIRST: TEN CALLS BECOME `load_job(lookup_job_id(...))`. They are the four `review` handlers, the three memory-candidate handlers, `commit-readiness`, and the two project handlers that load each job id their project stores. For any string `UUID(...)` accepts, `lookup_job_id` returns `str(UUID(...))` without touching the disk, and `load_job` builds the same path from that string as from the `UUID`, so everything that loaded before loads the same record. A string the parse refused now either raises a `JobIdError`, a `ValueError` like the parse's, or resolves: a short classic prefix to its job, a ping-pong id to itself. ALTERNATIVE: `load_job` on the raw string, rejected for these ten because an unhyphenated or upper-case UUID that loads today would stop loading.

CHOSEN, SECOND: `project attach-job` RESOLVES ONCE AND FILES THE RESOLVED ID. Routing the load alone would let a short prefix load its job and then be appended to the project's `job_ids` as the prefix, a key every later reader must resolve again and may resolve differently once a second job shares it. The handler binds the resolved id and uses it for the attach and for its message; its error message keeps the argument as typed. ALTERNATIVE: route the load and keep the raw key, rejected for that reason.

CHOSEN, THIRD: `job stop`'s LOADER DROPS THE PARSE INSTEAD OF ROUTING IT. `_load_job` answers whether this exact id names a job, and its caller normalises through `resolve_job_id` only when the answer is no. Routing made the answer yes for a short id, which is D58's measured defect. Loading the string as given keeps that answer no, and gives the same answer for an unhyphenated full id, so the caller now normalises that one too. The reviewer measured the difference at `b0ef6ab4`: stopping a classic job by its 32 unhyphenated hex characters filed the stop under that spelling, and a pending-stop check under the canonical id found none. ALTERNATIVE: route inside the loader and hand the resolved id back, rejected as a wider change to a helper with three call sites in its file.

CHOSEN, FOURTH: ONE ROUTED LOAD IS PROVED BY NO TEST, AND THAT IS REGISTERED RATHER THAN HIDDEN. `dashboard project` dies at its first import, which is `R-0883`, so nothing reaches its load, and restoring its parse changed no test's colour in the dry run. Each of the other eleven sites is pinned by a test that fails when that site's parse is restored.

CONSEQUENCE. No `UUID(...)` call under `apps/cli/` feeds `load_job` any more; the calls that parse a project id and the one that validates a task id remain, outside the job-id seam. `R-0883` is registered with owner F273, and `R-0809` and `R-0880` stay open. The readings behind this paragraph are the gates constraint 10 of round 86's block runs at C6, before the commit that lands it.

HOW TO REVERSE. Restore the seven handler files and `tests/test_data_paths.py` from `b0ef6ab4` and delete this paragraph block. The handlers then parse with `UUID(...)` again and refuse a short prefix.
END DEC86
