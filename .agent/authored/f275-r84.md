── STEP T003 — F275 — ROUND 84 ──
Goal: Give the job-id resolver a RAISING form that handlers can catch, route the 27 handler
parses that keep their parsed value through it, and leave the 10 that discard it for their own
round, because the reviewer measured one of those losing a stop request when routed blindly.

Base commit: `dd92a035`. Round type: SPLIT. PRODUCTION CODE changes, so the reviewer re-runs
every gate and every red-proof before a verdict.

THE FRAME RULE, per item 37 of `docs/agents/planner_reviewer_prompt.md` §3, stated as the
property MEASURED over the final bytes: NO LINE of this block is a run of a single repeated
character, and every box-drawing rule inside the STEP and SLICE header lines is exactly two
characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r84.md`           the block, saved verbatim
C0b `.agent/last_block.md`                  mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                        slice PLAN84, a full replacement
C2  `.agent/live_review.md`                 slice RECORD84 appended
C3  `.agent/prose_slips.md`                 slice SLIPS84 appended
C4  `packages/orchestration/data_paths.py`  the raising lookup, SPEC L
C5  the routed handler files under `apps/cli/commands/`, SPEC R, ONE commit
C6  `tests/test_data_paths.py`              five tests, SPEC T
C7  `apps/cli/commands/teach_cmd.py`        one comment round 83 falsified, SPEC C
C8  `.agent/decisions.md`                   slice DEC84 appended
C9  `.agent/handoff.md`                     the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. C5 precedes C6 so no commit adds a
failing test: the reviewer measured the routing alone changing no test's colour, while one of
the five tests fails until a handler is routed.

## Change — exactly these paths and no others

The Bundle's paths. C5 stages exactly the handler files SPEC R routes, which the reviewer
measured at `dd92a035` as thirteen: `brain.py`, `context.py`, `dashboard_cmd.py`, `event.py`,
`file.py`, `guide.py`, `memory.py`, `policy.py`, `propose_cmd.py`, `readiness.py`, `repo.py`,
`snapshot_cmds.py` and `test_cmds.py`. NOTHING under `docs/` or `scripts/`.
`apps/cli/commands/job_stop_cmd.py`, `project.py` and `review_cmd.py` are NOT touched.

## SPEC L — `packages/orchestration/data_paths.py`, at C4

1. Add `class JobIdError(ValueError)` and three subclasses of it: `JobIdInvalid`,
   `JobIdNotFound` and `JobIdAmbiguous`, the last carrying the raw prefix and a SORTED list of
   its matches as the attribute `matches`. The base class line reads EXACTLY
   `class JobIdError(ValueError):`, so G6's M1 finds it. Its docstring states WHY it is a
   `ValueError`: the handlers already guard their parse with `except ValueError` or wider, and
   several of those guards select a documented path of their own.
2. Add `lookup_job_id(raw: str) -> str`, the search `resolve_job_id` performs today, raising
   instead of exiting: a full UUID returns as `str(UUID(raw))` without touching the disk; a
   string matching neither that nor `_SHORT_HEX_RE` raises `JobIdInvalid`; a prefix with no
   match in either store raises `JobIdNotFound`, from a line reading EXACTLY
   `    raise JobIdNotFound(f"no job matches prefix {raw!r}")`; more than one match raises
   `JobIdAmbiguous`. It never ends the process.
3. `resolve_job_id` keeps its signature, its docstring's contract and its alias, and its body
   becomes a call to `lookup_job_id` that turns `JobIdAmbiguous` into the existing
   `_exit_ambiguous` call and any other `JobIdError` into ONE line reading EXACTLY
   `        print(f"Error: {exc}", file=sys.stderr)` followed by `sys.exit(1)`. Its stderr and
   exit codes stay BYTE-IDENTICAL to `dd92a035`: `Error: invalid job ID: 'x'`, then
   `Error: no job matches prefix 'x'`, each exit 1, and the ambiguity listing with exit 2.

## SPEC R — the handler layer, at C5

In every handler under `apps/cli/commands/`, a statement of the shape `X = UUID(<expr>)` —
one plain name bound to one `UUID(...)` call whose argument's source names a job — becomes
`X = lookup_job_id(<expr>)`. Measured at `dd92a035` with `ast`: 27 such statements in the
thirteen files above. Import `lookup_job_id` from `packages.orchestration.data_paths` where a
MODULE-LEVEL import does not already bind it: a function-local import of a name elsewhere in
the same file does not bind it inside another function, and the reviewer's own first dry run
missed that and swallowed a `NameError` as a false failure. Remove any `UUID` import the
change leaves unused. Then run
`python3 -m ruff check --select I001,F401 --fix` over EXACTLY the files C5 stages, and nothing
wider; the reviewer measured that as restoring `ruff check .` to its base rows exactly.

WHY THESE 27 AND NOT THE OTHER 10, which DEC84 records. The remaining ten are
`load_job(UUID(<expr>))`, where the resolved value is DISCARDED once the load succeeds. The
reviewer routed all 37 in a disposable worktree and measured
`tests/cli/test_golden_path.py::TestShortIdResolution::test_stop_with_screen_displayed_short_id`
going red: `_load_job` in `job_stop_cmd.py` now SUCCEEDS on a short id, which skips the caller's
normalisation, so the stop request is filed under the short id and `status --json` counts zero
pending. Each of the ten needs reading for that shape, and that is a later round.

## SPEC T — `tests/test_data_paths.py`, at C6

Five tests with EXACTLY these names. The first four go in a new class `TestLookupJobId`, the
fifth in a new class `TestRoutedHandler`; each sets `REMEDY_DATA_DIR` to `tmp_path`.
 `test_an_unmatched_prefix_raises_not_found_which_is_a_value_error` — with an empty `jobs`
   directory, `lookup_job_id("deadbeef")` raises `JobIdNotFound`, and ALSO raises under
   `pytest.raises(ValueError)`.
 `test_a_non_hex_string_raises_invalid` — `lookup_job_id("not-a-hex")` raises `JobIdInvalid`.
 `test_an_ambiguous_prefix_raises_with_the_sorted_matches` — two classic records
   `aaaa1111-0000-0000-0000-000000000002` and `…0001`; `JobIdAmbiguous.matches` equals the two
   ids sorted.
 `test_resolve_job_id_keeps_its_exit_codes_and_its_exact_messages` — through `capsys`,
   `resolve_job_id("not-a-hex")` exits 1 with stderr EXACTLY `Error: invalid job ID: 'not-a-hex'`
   and a newline, and `resolve_job_id("deadbeef")` over an empty `jobs` directory exits 1 with
   stderr EXACTLY `Error: no job matches prefix 'deadbeef'` and a newline.
 `test_a_routed_handler_accepts_a_short_classic_prefix` — saves a real `Job` through
   `storage.save_job`, calls `_cmd_guide_job` from `apps/cli/commands/guide.py` with the first
   eight characters of its id and `json_output=True`, and asserts stderr does not contain
   `invalid job ID` and stdout parses as JSON.

## SPEC C — `apps/cli/commands/teach_cmd.py`, at C7

The comment above `resolve_any_job_id(job_id_str)` in `_cmd_teach_narrate` says `resolve_job_id`
"searches `jobs/*.json` and returns a UUID". Round 83 made that false and its block did not
name the comment, because the reviewer's sweep read one line at a time and the claim spans two.
Rewrite it to say this was true until F275 T003 collapsed the two resolvers. No executable
line changes.

## Constraints

1. NO SLICE IS EDITED. PLAN84, RECORD84, SLIPS84 and DEC84 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. C4 to C7 are the worker's OWN code from the SPECs. The reviewer's candidate is deleted and
   not supplied.
3. READ `.agent/STOP` before C0a and before C9, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. EVERY COMMIT STAGES EXACTLY ONE PATH EXCEPT C5, which stages exactly the handler files
   SPEC R routes. Every commit stays under 500 insertions.
5. No `.py` under `.agent/`; scratch under `.remedy-wt/`, uncommitted.
6. No landed DECISION rewritten; DEC84 is an APPEND, C8's deletion column ZERO.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite.
8. THE RED-PROOF WORKTREE is created with `git worktree add --detach` at C7 and REMOVED AND
   PRUNED before C8. The scoped suite runs in the PRIMARY checkout, because
   `apps/ui/node_modules` is absent from a fresh worktree and turns one vitest test red there.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 293 lines TOTAL and 219 lines of PROSE,
   against the caps of 490 and 400.
10. THE GATES RUN AT TWO COMMITS. G4, G5 and G6 run at C7, because DEC84 at C8 carries their
    results and item 31 of §3 requires such a gate to run STRICTLY EARLIER. G1, G2, G3, G7 and
    G8 run at C8. No gate is ordered after C9; C9's own numbers are the reviewer's to measure
    at the next gate.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r84.md` at C0a against the block as
received, by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob.
Extract the slices by their markers, report how many were FOUND, check each against its own
BEGIN-marker sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN84 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD, FULL FORENSICS, for `.agent/live_review.md` at C2 and `.agent/decisions.md` at
C8. READER A with the arithmetic printed, from pre-commit lengths 1104567 and 1253148. READER
B over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted
by the script. One ASCII letter flipped in the FIRST appended paragraph of each, REJECTED by
both readers. Deletion columns 0. `.agent/prose_slips.md` at C3 equals its 292291-byte
pre-commit blob followed by exactly SLIPS84. Derive the ledger's header pattern from the file,
report how many headers it matches, and that RECORD84's header matches and duplicates none.

G4 THE PRODUCTION CHANGE, STRUCTURALLY, at C7, with `ast`. In `data_paths.py`: the classes
`JobIdError`, `JobIdInvalid`, `JobIdNotFound`, `JobIdAmbiguous` each defined once, each of the
last three a subclass of `JobIdError` and `JobIdError` a subclass of `ValueError`; one
`FunctionDef` named `lookup_job_id` and one named `resolve_job_id`; the whole-line counts of
SPEC L's three quoted lines, each 1; `resolve_any_job_id is resolve_job_id`. Across
`apps/cli/`: the count of `X = UUID(<job…>)` statements, which must be 0, and of
`load_job(UUID(<job…>))` calls, reported, which the reviewer measured at 10 at `dd92a035` and
which must be unchanged. Report the `git diff --numstat dd92a035` of every production path.

G5 THE BEHAVIOUR, in the PRIMARY checkout at C7. (a) The five tests of SPEC T by node id, each
PASSED. (b) `python3 -B -m pytest tests/test_data_paths.py tests/cli/ tests/orchestration/ -q -p no:randomly`
with its totals REPORTED AS MEASURED and its failure set, which must be EMPTY; the reviewer
measured it at `dd92a035` at 13255 passed, 10 skipped and 0 failed; state and account for the
difference. (c) A multiset comparison of `ruff check . --output-format json` rows by code and
path at `dd92a035` and at C7, reported as ADDED and REMOVED; both must be empty. Read the base
rows from a scratch copy made with `git archive`, never by overwriting the primary checkout.

G6 THE MUTATION RED-PROOFS, in the worktree of constraint 8, at C7. First PRINT the `__file__`
of `packages.orchestration.data_paths` imported inside the worktree; it must lie inside it.
Purge `__pycache__` before each run. Select the five SPEC T node ids and
`tests/cli/test_propose_cli.py::TestProposeEvaluateHandler::test_evaluate_missing_job`. Before
each mutation report its target's whole-line count, which must be 1, and restore after it.
 CONTROL, unmutated: all six PASS.
 M1 `class JobIdError(ValueError):` becomes `class JobIdError(Exception):`. Required: the
   not-found test and `test_evaluate_missing_job` FAIL; the other four PASS.
 M2 SPEC L's `raise JobIdNotFound(...)` line becomes `    sys.exit(1)`. Required: the not-found
   test and the exit-codes-and-messages test FAIL; the other four PASS.
 M3 SPEC L's `print(f"Error: {exc}", ...)` line prints `Error: job id problem: {exc}` instead.
   Required: ONLY the exit-codes-and-messages test FAILS.
 M4 in `guide.py`, the line `        job_id = lookup_job_id(job_id_str)` becomes
   `        job_id = UUID(job_id_str)`, with `from uuid import UUID` restored so it imports.
   Required: ONLY `test_a_routed_handler_accepts_a_short_classic_prefix` FAILS.
Report each run's six colours and exit code, then remove and prune the worktree.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C8. `git status --porcelain` prints `''`;
`git worktree list` one row; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`
exit 0 at the count it measures, 42 at `dd92a035`; `ruff check .` exit 1 with its row count
cross-checked against its own `Found <n> errors.` line, 26 at `dd92a035`. The changed-path set
of `dd92a035`..C8 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by
name. The open set at `dd92a035` and at C8, BY DISTINCT ID, with both counts, the membership
difference each way and whether `R-0809` and `R-0880` are open; 87 at `dd92a035`; the
registered, resolved and de-registered sets all EMPTY.

G8 THE INSERTION CAP over `dd92a035`..C8: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 29 of feature F275 · round 84 · rounds so far 84`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C9's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 0`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN84 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN84 sha256=9c75e9a8a0967b1fd40010d46ca272a2abc4685c97094d1c16084641b5255315
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

ROUND 84 GIVES THE JOB-ID RESOLVER A RAISING FORM AND ROUTES THE HANDLERS THAT KEEP THEIR ID.
`lookup_job_id` raises a `ValueError` subclass where `resolve_job_id` exits, so a handler that
guards its parse keeps its own documented path; `resolve_job_id` becomes its wrapper with the
same messages and exit codes. The handler statements that bind a parsed job id are routed
through it. The ones that pass the parse straight into `load_job` are left, because the
reviewer's dry run found `job stop` losing a stop request when one of them was routed without
reading it. The round 83 verdict, its prose slips and one comment round 83 falsified are booked.

## Next Steps

1. THE REMAINING HANDLER PARSES, each `load_job(UUID(...))` read for whether its caller keeps
   using the raw argument as a key, starting with `job stop`'s loader and its caller's
   normalisation. Production code, so a SPLIT round with mutation red-proofs.
2. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, the input
   is re-derived by round 82's committed generator at the flip's own base, and any site fallen
   to zero witnesses is a stop. The stale test double at
   `packages/orchestration/project_registry.py:856` is updated in the flip's own commit.
3. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- A HANDLER THAT DISCARDS ITS RESOLVED ID CAN KEY ON THE RAW ONE. The dry run caught one such
  site through a test; untested sites of that shape are not seen by any run.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, and the re-key
  cannot see a deleted ruled site.
- The open set is 87 by distinct id at this round's base, with `R-0809` and `R-0880` open. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN84

── SLICE RECORD84 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD84 sha256=8f11cc4e47dd36c10f15b49efd86b8884135a5bbb9edc0f5d3283014d5f93198

Gate: F275 R83 — the F275 round 83 entry. VERDICT PASS. Written by the planner and reviewer of session 29 after reading the committed range `afffd7cc`..`dd92a035` and RE-DERIVING EVERY GATE AND EVERY RED-PROOF INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 84, per operator amendment amend0827-process-diet rule 1. The round changed production code, and a production change is never self-certified: the reviewer ran its own mutations in its own worktree before writing this.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/` blob was identical by `cmp` to the reviewer's own original at 29728 bytes, `.agent/last_block.md` equalled it, all four slices matched their BEGIN-marker digests, and the block re-measured at 315 lines TOTAL and 238 PROSE. `.agent/plan.md` was byte-identical to its slice at 45 lines. The three appends were exact under reader A — 1100820 plus 3747, 289390 plus 2901 and 1248878 plus 4270 — with reader B holding at N counted from the slice as 4, 4 and 8 and a letter flipped in each FIRST appended paragraph rejected by both readers. Nine paths changed, each commit staging one, the largest at 315 insertions.

THE PRODUCTION CHANGE HOLDS UNDER THE REVIEWER'S OWN RE-RUN. Read with `ast` at C6, `data_paths.py` defines `resolve_job_id` once and `resolve_any_job_id` never, carries the alias statement and the union `matches` statement once each with the latter inside `resolve_job_id`, and assigns no classic-only `matches` anywhere; the two names import as one object. In a worktree whose module the reviewer printed as resolving inside it, the three new tests pass unmutated; restoring the classic-only statement fails the two behavioural tests and leaves the identity test green; replacing the alias with a function fails only the identity test. Called against a scratch root holding one ping-pong record, `_cmd_job_status` exits 1 with `job not found` after the change and with `no job matches prefix` on the base version of the module. The scoped suite in the primary checkout read 13255 passed, 10 skipped and 0 failed, the base's 13252 plus exactly the three tests C5 adds; the canary read 42, `ruff check .` 26, and the open set stayed 87 with `R-0809` and `R-0880` open.

ONE FACT THE BLOCK DID NOT PREDICT, AND THE WORKER FOUND IT. The comment above the resolver call in `apps/cli/commands/teach_cmd.py` still says `resolve_job_id` searches `jobs/*.json` and returns a UUID, which C4 made false. It sat outside the change set, so the worker left it and flagged it, which was right. The reviewer's sweep over comment and docstring PARAGRAPHS in every tracked file naming either resolver returns two: the one in `apps/cli/commands/job_context_cmd.py`, which C6 made correctly past tense, and the one in `teach_cmd.py`, which is the only stale claim; round 84's block names it. No id is spent: it is a comment the round's own block should have named, so it is a prose slip and a line in the next change set.
END RECORD84

── SLICE SLIPS84 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS84 sha256=d46d6c15713c90650c2997896c794f3bce1b65e01e0bdf745ebe4f8532127863

2026-09-12 · F275 R83 · The round 83 block named one comment its collapse falsified and missed a second, in `apps/cli/commands/teach_cmd.py`, because the reviewer's sweep matched `resolve_job_id` and a stale phrase on the SAME LINE while that comment says `resolve_job_id` on one line and "searches `jobs/*.json` and returns a UUID" on the next. THE RULE THAT FOLLOWS: a sweep for claims a change falsifies reads comments and docstrings as PARAGRAPHS, joining adjacent comment lines before matching, because prose wraps and a line-scoped pattern finds only the claims short enough to fit on one.

2026-09-12 · F275 R83 · The round 83 block told the worker the alias statement's text "also occurs INSIDE the module docstring's table once SPEC P item 4 is applied", which was true of the reviewer's candidate and false of the worker's, whose table row words it differently. Nothing depended on it. THE RULE THAT FOLLOWS: a block describes the code the worker will write by the properties the SPEC REQUIRES and never by the incidental text of the reviewer's own candidate, because the SPEC is what the worker implements and the candidate is deleted before the worker starts.

2026-09-12 · F275 R84 · Dry-running round 84, the reviewer's transform decided whether a file already imported `resolve_job_id` by a SUBSTRING test, which matched a function-local import in a different function of `apps/cli/commands/job_stop_cmd.py`; so no import was added, the replaced call raised `NameError` inside `_load_job`, `except Exception` swallowed it, and three golden-path tests failed for a reason that was the instrument's. It was caught by reading one failure's output before authoring. THE RULE THAT FOLLOWS: whether a name is bound where a call runs is a question about SCOPE and is answered with `ast` over the enclosing module's top-level statements, never with a substring over the file, and a transform whose failure path is an exception a broad handler swallows is dry-run with that handler's catches counted.
END SLIPS84

── SLICE DEC84 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC84 sha256=b9e875fe09c2686f550aa50c7b92617ad0c6c59882e75f7489f2bdb191cddb25

## DECISION F275 D58 (2026-09-12, F275 round 84) — the resolver gains a RAISING form so a handler's own guard survives routing, the 27 handler parses that bind their value are routed, and the 10 that discard it are held back on a measured defect

CONTEXT. DECISION F275 D57 collapsed the two resolvers and measured that doing so moves a ping-pong id's failure one step later, and it named the handler layer — 37 `UUID(...)` parses whose argument names a job, in 16 files under `apps/cli/` — as the rest of DECISION F275 D37's seam. Before this round was authored the reviewer routed all 37 through the resolver in a disposable worktree and ran the scoped suite, so the choices below rest on what broke rather than on what might.

CHOSEN, FIRST: THE RESOLVER GAINS A RAISING FORM, AND ITS EXCEPTIONS ARE `ValueError`S. Routed through the exiting `resolve_job_id`, six tests failed in two handlers, `job stop`'s loader and `propose`'s job check. Five of them failed because those handlers treat an unknown id as a documented path — an exit 3 with a `job_not_found` document, a JSON error payload — and `SystemExit` escapes both guards; under the raising form below all five pass. The sixth failed for the different reason CHOSEN THIRD gives, and it still fails under the raising form. `lookup_job_id` performs the same search and raises `JobIdInvalid`, `JobIdNotFound` or `JobIdAmbiguous`, all subclasses of `JobIdError(ValueError)`, so every existing `except ValueError` or wider guard catches the failure exactly where it caught the `UUID` parse's. `resolve_job_id` becomes its wrapper with byte-identical messages and exit codes. ALTERNATIVE: a lookup returning `None`, rejected because it collapses invalid, unknown and ambiguous into one value and forces every caller to re-derive which it was.

CHOSEN, SECOND: THE 27 PARSES THAT BIND THEIR VALUE ARE ROUTED. Each is a statement `X = UUID(<expr>)` whose value the handler keeps and uses. The reviewer measured, with a survey whose negative control found both uses planted for it, that no later use of any such `X` needs a real `UUID` — no UUID-only attribute, no `isinstance`, no comparison — and that routing them changes no test's colour. What was NOT surveyed is the functions those handlers pass the id on to, which now receive a `str` where they received a `UUID`; the suite exercises some of them and not all. An existing short classic prefix now resolves where the parse rejected it.

CHOSEN, THIRD: THE 10 THAT DISCARD THEIR VALUE ARE NOT ROUTED, AND THE REASON IS A DEFECT THE DRY RUN MEASURED. They are `load_job(UUID(<expr>))`. Routed, `_load_job` in `apps/cli/commands/job_stop_cmd.py` SUCCEEDS on a short id, which skips its caller's step that normalises the id, so the stop request is filed under the short id while `status` looks it up under the full one and counts zero pending — and the command still prints "Stop requested" and exits 0. `tests/cli/test_golden_path.py::TestShortIdResolution::test_stop_with_screen_displayed_short_id` is what caught it. Any of the ten whose caller keeps using the raw argument can do the same, and each is read in its own round.

CHOSEN, FOURTH: THE TESTS ARE DISCRIMINATORS, EACH MUTATION REACHING ONE. Making `JobIdError` a plain `Exception` fails the not-found test and `propose`'s missing-job test, which is the measured form of why the base class matters; making the lookup exit fails the not-found test and the message test; changing the wrapper's message fails only the message test; restoring one handler's `UUID` parse fails only the routed-handler test. All four were measured in a worktree before authoring.

CONSEQUENCE. A handler can now resolve a job id across both stores without losing its own failure path, and 27 of the 37 handler parses do. `R-0809` stays OPEN, its message-shape defect untouched, and `R-0880` stays OPEN. No finding is registered or resolved. The stale comment in `apps/cli/commands/teach_cmd.py` is corrected here as a line the round 83 block should have named.

HOW TO REVERSE. Restore `data_paths.py`, the thirteen handler files, `tests/test_data_paths.py` and `apps/cli/commands/teach_cmd.py` from `dd92a035`, and delete this paragraph block. The handlers then parse with `UUID(...)` again, and `resolve_job_id` exits as before.
END DEC84
