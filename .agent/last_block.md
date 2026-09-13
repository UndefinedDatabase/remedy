── STEP T003 — F275 — ROUND 96 ──
Goal: Commit the flip's seventh OVERLAY, applied after the first six to the flipped tree at
`844a7f21`: the unified record's JSON form is its exporter's, an old record a test loads has
the unified shape, a record's `created_at` is the string it stores, and the fulfillment
record's `created_at` is formatted again; measured by the full suite in fresh flipped trees.

Base commit: `0fe76bb9`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
edits production code and tests, carried in a diff, and G6 red-proves both production changes.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r96.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN96, a full replacement
C2  `.agent/live_review.md`                   slice RECORD96 appended, the round 95 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS96 appended
C4  `.agent/authored/f275-r96-overlay-<k>.md` the overlay carriers of SPEC C, ONE COMMIT EACH
C5  `.agent/decisions.md`                     slice DEC96 appended
C6  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths, `<k>` running from 1 over the carriers SPEC C produces.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the sixth overlay

SPEC O edits these paths and no others: `apps/cli/commands/job.py`,
`packages/orchestration/job_fulfillment.py`, `tests/cli/test_context_inspect_runtime.py`,
`tests/cli/test_golden_path.py`, `tests/orchestration/test_fence_e2e.py`,
`tests/orchestration/test_job_budgets.py`, `tests/orchestration/test_long_run_executor.py`,
`tests/orchestration/test_loop_run.py`, `tests/orchestration/test_run_contract.py`,
`tests/test_grouped_cli.py`. No test is added or deleted. `_export_job` and `_import_job` are
imported from `packages.orchestration.pingpong_job`, inside the function that uses them.
O1 JOB SHOW. `_cmd_show_job` in `apps/cli/commands/job.py` prints
`json.dumps(_export_job(job), indent=2)` where it printed `job.model_dump_json(indent=2)`.
O2 THE FULFILLMENT EXPORT. `export_job_fulfillment_json` in
`packages/orchestration/job_fulfillment.py` writes `"created_at": record.created_at.isoformat(),`.
O3 ROUND TRIPS. `test_saved_contract_survives_json_roundtrip` and
`test_usage_survives_json_roundtrip` in `test_run_contract.py`, and `test_round_trip_json` and
`test_fences_none_round_trip` in `test_fence_e2e.py`, restore the record as
`_import_job(json.loads(json.dumps(_export_job(job))))` in place of their pydantic dump and
validate. In `test_long_run_executor.py`, `_normalize` reads
`json.loads(json.dumps(_export_job(job)))`, and
`test_defaults_reproduce_the_single_pass_exactly` makes its two copies with `copy.deepcopy(job)`.
O4 OLD RECORDS AND BUDGETS. `test_backward_compatible_load` in `test_fence_e2e.py` loads
`_import_job({"job_id": uuid4().hex[:16], "job_title": "old-job"})`. In `test_job_budgets.py`,
class `TestJobBudgetsModel`: `test_backward_compatible_old_job_fixture` loads
`_import_job({"job_id": "0000000000000001", "job_title": "old-job"})`;
`test_job_with_budgets_serializes`, `test_job_with_budgets_roundtrips` and
`test_json_roundtrip_preserves_strict_types` give `JobPlan` its budgets as
`JobBudgets(...).model_dump(mode="json")`, export with `_export_job`, restore with `_import_job` —
the last of the three through `json.dumps` and `json.loads` — and read each budget value by key.
In `test_golden_path.py`, `test_old_job_json_without_mission_loads` spells its old record's `id`
and `name` keys `job_id`, with the value `"0000000000000001"`, and `job_title`, imports
`_import_job` in place of `JobPlan`, loads with `_import_job(json.loads(old_json))` and asserts
`job.mission == ""`; `test_job_show_accepts_short_id` asserts `data["job_id"] == job_id`.
O5 THE RUNTIME FIXTURE. `_create_temp_job` in `test_context_inspect_runtime.py` saves the record
with `save_job_plan(job, tmp_path)` in place of making `jobs/` and writing `<job_id>.json`.
O6 `created_at`. The four `created_at=datetime(...)` arguments in `test_loop_run.py`, and the two
in `test_default_order_is_newest_first` in `test_grouped_cli.py`, pass `.isoformat()` of the same
value.

## SPEC C — the carriers, at C4

The VERBATIM stdout of `git diff` in EDIT, against its index as constraint 8 stages it, is cut at
`diff --git` lines into consecutive parts in its own order, each part as many whole file diffs as
fit in 440 lines, a new part starting only when the next file diff would not fit. Part `<k>` is
`.agent/authored/f275-r96-overlay-<k>.md`: at most 40 lines of prose naming its base `844a7f21`,
that the flipped tree is built as G4 of `.agent/authored/f275-r96.md` orders, that the parts form
the SEVENTH overlay and apply after `.agent/authored/f275-r95-overlay-4.md` in `<k>` order, and
how to apply each — extract the fence, `git apply --check`, then `git apply`; then exactly ONE
fence, a line of three backticks and `diff`, the part, and a line of three backticks; nothing
after it but one newline. Joined in `<k>` order, the fences equal the whole diff byte for byte.

## Constraints

1. NO SLICE IS EDITED. PLAN96, RECORD96, SLIPS96 and DEC96 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` through
   `.remedy-wt/r96/` is not opened.
3. READ `.agent/STOP` before C0a and before C6, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r96w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commits are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r96w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, then for each of
   `.agent/authored/f275-r90-overlay.md`, `.agent/authored/f275-r91-overlay.md`,
   `.agent/authored/f275-r92-overlay-1.md` through `-4.md`, `.agent/authored/f275-r93-overlay-1.md`
   and `-2.md`, `.agent/authored/f275-r94-overlay-1.md` and `-2.md` and
   `.agent/authored/f275-r95-overlay-1.md` through `-4.md`, overlay by overlay in that order, the
   fences of the COMMITTED carriers applied with `git apply --check` then `git apply`, and
   `git add -A` once after each overlay's parts. Only EDIT receives SPEC O, and any test may run
   there while it is made; before the diff is taken its `git diff --name-only` lists exactly
   SPEC O's paths. Only OVERLAY receives the C4 carriers. All three are REMOVED AND PRUNED before
   C5, without `--force`. The generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 292 lines TOTAL and 221 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4's setup — the generator, the three worktrees, the chain — runs after C3 and
    before the first C4 commit, because the carriers are cut from EDIT; G4's readings, G5 and G6
    are taken after the last C4 commit and strictly before C5, per item 31 of §3. DEC96's
    measured figures, 9, 12 and 6, are G4(b)'s CONTROL readings; DEC96 quotes no G5 or G6
    reading. G1, G2, G3, G7 and G8 run at C5. No gate runs after C6; C6's own numbers are the
    reviewer's.
11. A RED G5 IS A STOP. Each node G5 finds bad only in OVERLAY is re-run by its node id alone in
    OVERLAY three times with G5's environment; unless every re-run passes, the worker commits
    nothing further after C4 except the handback, which lists every such node with its last
    `E   ` line. A node whose three re-runs all pass is reported FLAKY with the three tallies.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r96.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN96 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C5 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1148938 and 1297335 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 303243-byte pre-commit blob followed by
exactly SLIPS96. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD96's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIERS, set up and read per constraint 10. The generator trees
and run exactly as G4 of `.agent/authored/f275-r90.md` orders, the pinned digests checked first,
with the readings that block states; the transform in each worktree reading 2183 resolving and 0
not, 264 files, 6097 rewrites and 0 broken; every earlier overlay applying with exit 0 in each.
Then: (a) the fences extracted from the COMMITTED C4 blobs: report the part count and each part's
line count, each at most 440; joined in `<k>` order they equal EDIT's diff; in OVERLAY each
applies with `git apply --check` and `git apply` exit 0, in order; `git diff --name-only` there,
against the index constraint 8 staged, lists exactly SPEC O's paths by name, each byte-identical
to EDIT's; report MISSING and EXTRA. (b) With `ast`, in CONTROL and in OVERLAY, names matched
EXACTLY: calls of an attribute whose name starts `model_` read off the bare name `JobPlan`,
under `packages/`, `apps/` and `tests/`, 9 and 0; calls of an attribute named `model_dump`,
`model_dump_json` or `model_copy` read off the bare name `job`, under `apps/` and `tests/`, 12
and 0; `created_at` keywords of calls of the bare name `JobPlan` or `_stored_job`, under all
three, whose value contains a call of the bare name `datetime` or of `datetime.now` and is not
itself a call of an attribute named `isoformat`, 6 and 0. `def test_` counts per changed test
file equal in both trees. (c) `ruff check --output-format concise`, run from inside each of
CONTROL and OVERLAY over SPEC O's paths, rows compared as a MULTISET of `<path>: <code> <message>`
with line and column DROPPED: added 0 and removed 0. The reviewer read 9 rows in each; the exit
is 1 in BOTH trees and is reported, never ordered.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, per constraint 10, CONTROL first and OVERLAY second,
serially. Each is its worktree's FIRST pytest run of any kind, `apps/ui/node_modules` and
`apps/ui/dist` reported absent before it. `cwd` the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and
`REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`;
`packages.orchestration.pingpong_job.__file__` printed and inside the worktree;
`python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad node is the
text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The reviewer measured
CONTROL `150 failed, 18261 passed, 29 skipped, 1 warning, 31 errors`, 181 bad nodes, and its own
dry run of SPEC O, before an unused import that run left in `test_golden_path.py` was removed,
`118 failed, 18293 passed, 29 skipped, 1 warning, 31 errors`, 149. REPORT OVERLAY's tally and
bad-node count. Bad only in OVERLAY: MUST be 0, per constraint 11. REPORT the fixed nodes' count
per test file.

G6 THE PROBES, per constraint 10, in OVERLAY after G5; `__pycache__` purged before each run;
G5's environment; flags `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. For each
mutation, the bytes it replaces counted in the file as 1 first, then the selection run UNMUTATED
and MUTATED, each tally and exit code reported with the node ids bad only under the mutation,
then the file restored and its bytes confirmed. M1 in `apps/cli/commands/job.py`, O1's print in
`_cmd_show_job` becomes `print(job.model_dump_json(indent=2))`, over
`tests/cli/test_golden_path.py -k "job_show or intake_persisted or llm_intake or accepts_short_id"`:
`TestShortIdResolution::test_job_show_accepts_short_id` MUST go bad; the reviewer's dry run read 5
passed unmutated and 4 bad mutated, that node with `test_intake_persisted_on_job`,
`test_job_show_silent_for_legacy_job` and `test_fake_provider_stores_llm_intake_with_evidence`.
M2 in `packages/orchestration/job_fulfillment.py`, O2's `.isoformat()` is removed, over
`tests/orchestration/test_job_fulfillment.py`: `TestFulfillmentModel::test_record_export_no_secrets`
and `TestJobReportAfterFulfilled::test_report_shows_completed` MUST go bad; the reviewer's dry run
read one other node bad in both runs.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C5. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only 0fe76bb9 C5 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `0fe76bb9`, read from a
`git archive` tree, and at C5, difference empty, 26 at `0fe76bb9`. The changed-path set of
`0fe76bb9`..C5 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `0fe76bb9` and at C5: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G8 THE INSERTION CAP over `0fe76bb9`..C5: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 32 of feature F275 · round 96 · rounds so far 96`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN96 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN96 sha256=0e6bb90599e342af4a08395adb9ec3cd33de102b5559d7f87fcf99f9f924abfe
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

ROUND 96 ADDS THE FLIP'S SEVENTH OVERLAY, on top of the first six, under DECISION F275 D64's
method. The unified record's JSON form is its exporter's: `job show --json` prints it, tests
round-trip a record through the exporter and the importer instead of pydantic calls, an old
record a test loads has the unified shape, a record's `created_at` is the ISO string it stores,
and the fulfillment record's `created_at` is formatted again. The diff is carried in a carrier,
so no path under `packages/`, `apps/` or `tests/` moves; the round books the round 95 verdict and
its prose slip.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it:
   production code that hands a `JobPlan` a `JobBudgets` model where the record holds its
   serialized dict; the mission end-to-end fixture and `mission continue` finding no previous
   job; command-line tests whose job the flipped store does not find; the classic-shaped tests
   of routed handlers in `tests/test_data_paths.py`; and what is left of the classic runner
   under `job resume`, which still builds a classic job.
2. THE FLIP: the transform, then every overlay in round order, landed as a series of commits
   each under the 500-insertion cap inside one round, carrying DECISION F275 D48's obligations
   and registering the structured acceptance form DECISION F275 D22 leaves to it, unless the
   operator allows one more oversized commit.
3. Then the classic store, with the which-store branches and adapters the overlays leave
   unreached, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: many test nodes still fail in the flipped tree.
- AN OVERLAY IS A DIFF AGAINST A FIXED TREE: it holds only while the production tree stays at
  `844a7f21`, and it depends on the generator and transform staying reproducible from round
  77's two scratch JSON files.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN96

── SLICE RECORD96 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD96 sha256=497418d38a6e43197e48bcef297c3103f8dd3c6c19f2f89449c095a428281fea

Gate: F275 R95 — the F275 round 95 entry. VERDICT PASS. Written by the planner and reviewer of session 32 after reading the committed range `6ec72f20`..`0fe76bb9` and RE-DERIVING EVERY GATE AND EVERY PROBE INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 96 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its code is the diff carried in `.agent/authored/f275-r95-overlay-1.md` through `-4.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r95.md` blob was identical to the reviewer's own original at 26594 bytes, `.agent/last_block.md` equalled it from its own commit through `0fe76bb9`, and all four slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN95. The three appends were exact under reader A — 1145506 plus 3432 into the review record, 302371 plus 872 into the prose slips and 1294405 plus 2930 into the decisions — with reader B holding at N counted from each slice as 4, 2 and 7, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, the largest the first carrier at 474 insertions, and the four fences read 436, 371, 407 and 156 lines, which is what cutting the joined diff greedily at 440 lines gives.

THE OVERLAY HOLDS, AND WHERE ITS READINGS WERE TAKEN. The reviewer transformed a worktree at `844a7f21` from its own generator run, applied and staged the committed overlays of rounds 90 to 94, and applied the four committed round 95 fences: every `git apply --check` and `git apply` exited 0, 32 paths changed, 20 of them production code, and that tree's diff was byte-identical to the diff of the reviewer's own dry run of SPEC O. Because the bytes are identical, the suite and the probes were read in the dry-run tree and not run a second time. There, O1's reads and O2's spellings read 0 and 0 against 79 and 54 in a control tree of the chain before it, and the resolver doubles read 27; the `ruff` rows over the 32 files read 23 in each tree as a multiset with line and column dropped, none added. That tree's first full run read 150 failed, 18261 passed, 29 skipped and 31 errors, 181 bad nodes, against 256 in the reviewer's fresh run of the chain before it: 75 fixed and none newly bad. In the same tree, reading `name` back in `summarize_project` made exactly `test_jobs_shown_with_state` bad; reading `job.id` in `_build_events_since_json` made all seven nodes of `tests/ui_server/test_event_seq.py` bad; and removing the resolver double from `test_handler_text_output` made that node bad. In the primary checkout at `0fe76bb9` the canary read 42 and `ruff check .` read 26 rows; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.
END RECORD96

── SLICE SLIPS96 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS96 sha256=7e50e965e6e5b7f1886d9605c10b2445788f4a996a71c9f48a9af1a7c7932b92

2026-09-14 · F275 R95 · G4(b) of the round 95 block defined O2's count by class-body targets, attribute nodes off named receivers and `SimpleNamespace` keywords, which misses a `self.id` read and a `seen[0].id` read that O2 itself orders changed, so the gate counted 54 where O2 orders 56 edits, and DECISION F275 D69 quotes the 54 as the doubles' spellings; the worker changed all 56 and declared the gap. THE RULE THAT FOLLOWS: a census ordered as a spec's measurement is read against every site the spec names before its figure is written into a slice.
END SLIPS96

── SLICE DEC96 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC96 sha256=a3f87974437147aa4fc96079cdf5eb943029dae3523c97f8ac73b9a4b783ed7d

## DECISION F275 D70 (2026-09-14, F275 round 96) — the seventh overlay: a unified record's JSON form is its exporter's, an old record a test loads has the unified shape, a record's `created_at` is the string it stores, and the fulfillment record's `created_at` is formatted again

CONTEXT. `JobPlan` is a dataclass, while the classic `Job` it replaces was a pydantic model. In the flipped tree at `844a7f21`, with six overlays applied, 9 calls under `packages/`, `apps/` and `tests/` still call a pydantic class method on `JobPlan`, and 12 calls under `apps/` and `tests/` call `model_dump`, `model_dump_json` or `model_copy` on a local named `job`; `job show --json` is one of them. 6 test constructions give a record's `created_at` a `datetime`, while the record stores the ISO string its exporter writes. And the transform removed `.isoformat()` from `export_job_fulfillment_json`'s `created_at`, although the fulfillment record's field is a `datetime`: an over-selected rewrite of the class `R-0880` names.

CHOSEN, FIRST: THE RECORD'S JSON FORM IS ITS EXPORTER'S. `job show --json` prints `_export_job`'s dict, so its keys are the keys the record is stored under — `job_id` where the classic output said `id` — and the one test reading `id` from it reads `job_id`. Tests round-trip a record through `_export_job` and `_import_job`, as `tests/orchestration/test_job_administrative_fields.py` already does, and a deep copy is `copy.deepcopy`. ALTERNATIVES: pydantic-compatible methods on `JobPlan`, rejected as the compatibility reader AGENTS.md Scope Control forbids; a public second name for the exporter, rejected because the one production caller does not justify two names for one function.

CHOSEN, SECOND: AN OLD RECORD A TEST LOADS HAS THE UNIFIED SHAPE. The tests that loaded a classic-shaped record written before a field existed load the unified record's minimal shape instead, which is what such a record is after the flip, and an absent mission reads as the empty string, the unified record's spelling of absent. Budget tests hand the record `JobBudgets(...).model_dump(mode="json")`, the serialized dict `JobPlan.budgets` holds, and read its keys.

CHOSEN, THIRD: A RECORD'S `created_at` IS THE STRING IT STORES, so the test constructions pass `.isoformat()`; and the fulfillment export formats its `datetime` again. `R-0880` stays open: this overlay repairs one instance of its class and the finding is about the class.

CONSEQUENCE. `job show --json` changes its keys to the record's; that is the record flip itself reaching the one command that prints the record whole, not a separate ruling. What the overlay fixes, and that it newly breaks nothing, is measured by the gates of round 96's block and recorded in the round 96 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete the round 96 overlay carriers under `.agent/authored/` and this paragraph block; those calls then raise in the flipped tree again.
END DEC96
