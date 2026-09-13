── STEP T003 — F275 — ROUND 91 ──
Goal: Commit the flip's second OVERLAY, applied after the first to the flipped tree at
`844a7f21`: artifact ids on the unified task record become strings and are compared as
strings, tests hand the unified record strings, and the full suite in fresh flipped trees
measures what it fixes and that it breaks nothing.

Base commit: `1f7a52f9`. The chain's base stays `844a7f21`, per DECISION F275 D64. Round type:
SPLIT. No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` changes; the overlay
is production code carried in a diff, so G4 to G6 give it full forensics and a mutation probe.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r91.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN91, a full replacement
C2  `.agent/live_review.md`                   slice RECORD91 appended, the round 90 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS91 appended
C4  `.agent/authored/f275-r91-overlay.md`     the overlay carrier, SPEC C over SPEC O
C5  `.agent/decisions.md`                     slice DEC91 appended
C6  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths.

## SPEC O — the edits, made in the EDIT worktree of constraint 8 on top of the first overlay

O1 PRODUCTION, exactly these sites and nothing else under `packages/` or `apps/`. In
`packages/orchestration/task_runner.py`, `run_next_task` appends `str(artifact.id)` to
`task.output_artifact_ids`. The lookup of an artifact whose id was read from
`output_artifact_ids` compares `str(a.id)` with that id in `finalize_task` and
`materialize_task_output` of the same file, in `verify_task_output` of
`packages/orchestration/verifier.py`, and at both lookups in `_cmd_run_next_task_local` of
`apps/cli/commands/job.py`.
O2 TESTS, under `tests/` only. Where a test constructs, assigns, appends to or saves a
`JobPlan` or `TaskEntry` with a `UUID` object in `job_id`, `task_id` or a member of
`output_artifact_ids`, it passes the string form; where a test compares such a field with a
`UUID` object, or derives a prefix from it with `.hex`, it uses the string form. The smallest
edit per site; no test added or deleted; no assertion loosened. Touch a test file only when a
test in it is bad in the flipped tree under this rule, or goes bad under O1.
O3 OUT OF SCOPE, named: `repository_snapshot.revert_repository_apply` and
`test_execution_service.execute_test_run` keep their `UUID(...)` parses, and their tests are
not edited for them.

## SPEC C — the carrier, at C4

`.agent/authored/f275-r91-overlay.md` opens with prose: what it changes, its base `844a7f21`,
that the flipped tree is built as G4 of `.agent/authored/f275-r91.md` orders, that it is the
SECOND overlay and applies after `.agent/authored/f275-r90-overlay.md`, and how to apply it —
extract the fence, `git apply --check`, then `git apply`. Then exactly ONE fence: a line of three
backticks and `diff`, the VERBATIM stdout of `git diff` in EDIT against its index as constraint 8
stages it, and a line of three backticks. Nothing after it but one newline. The carrier commit
stays under 500 insertions; if it cannot, the round stops at C3 and declares the size.

## Constraints

1. NO SLICE IS EDITED. PLAN91, RECORD91, SLIPS91 and DEC91 land byte for byte; a discrepancy
   inside one is DECLARED, never repaired.
2. SPEC O and SPEC C are the worker's OWN work. The reviewer's scratch `.remedy-wt/r90/` and
   `.remedy-wt/r91/` are not opened.
3. READ `.agent/STOP` before C0a and before C6, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r91w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: the `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commits are APPENDS with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite.
8. THREE worktrees, each `git worktree add --detach` at `844a7f21` under `.remedy-wt/r91w/`:
   EDIT, CONTROL and OVERLAY. In each: the transform as G4 orders, `git add -A`, the fence of the
   COMMITTED `.agent/authored/f275-r90-overlay.md` applied with `git apply --check` then
   `git apply`, and `git add -A` again. Only EDIT receives SPEC O, and any test may run there
   while it is made; its `git diff --name-only` before the diff is taken lists only paths SPEC O
   edited. Only OVERLAY receives the C4 carrier. All three are REMOVED AND PRUNED before C5,
   without `--force`. The generator's trees are plain directories.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 260 lines TOTAL and 187 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4, G5 and G6 run at C4, strictly before C5, per item 31 of §3. DEC91's figures
    and where each comes from: five and two, the lookups and the out-of-scope callers, are
    SPEC O's and G4 counts the five; DEC91 quotes no G5 or G6 reading. G1, G2, G3, G7 and G8 run
    at C5. No gate runs after C6; C6's own numbers are the reviewer's.
11. A RED G5 IS A STOP. If G5 finds a node bad only in OVERLAY, the worker commits nothing
    further after C4 except the handback, which lists every such node with its last `E   ` line.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r91.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN91 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C5 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1131427 and 1281959 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 299259-byte pre-commit blob followed by
exactly SLIPS91. Derive the ledger's `Gate:` header pattern from the file, report how many heads
it matches, and that RECORD91's header matches it and duplicates none.

G4 THE TREES, THE CHAIN AND THE CARRIER, at C4. The generator trees and run exactly as G4 of
`.agent/authored/f275-r90.md` orders, the pinned digests checked first; the reviewer's readings
there stand: 56 paths, 2183 ruled sites all recovered with 0 UNRESOLVED, the line-key control
1895, 1886 and 1886, the owner check 1908, 275 and 0. The transform in each worktree: 2183
resolving and 0 not, 264 files, 6097 rewrites, 0 broken. The first overlay's `git apply --check`
and `git apply` exit 0 in each. Then: (a) the fence extracted from the COMMITTED C4 blob; in
OVERLAY `git apply --check` and `git apply` exit 0; `git diff --name-only` there, against the
index constraint 8 staged, lists exactly EDIT's paths, each byte-identical to EDIT's; report the
list. Under `packages/` and `apps/` it holds exactly `packages/orchestration/task_runner.py`,
`packages/orchestration/verifier.py` and `apps/cli/commands/job.py`; every other path is under
`tests/`. (b) In CONTROL and in OVERLAY: `str(a.id) == ` 0 and 5 over the three production
files, 2 of the 5 in `task_runner.py`, 1 in `verifier.py` and 2 in `job.py`;
`output_artifact_ids.append(str(artifact.id))` 0 and 1, and
`output_artifact_ids.append(artifact.id)` 1 and 0, in `task_runner.py`. Over every changed test
file, the `def test_` count equal in CONTROL and OVERLAY, per file. (c) `ruff check
--output-format concise --stdin-filename <path> -`, run from inside each worktree, over every
changed path, rows compared as a MULTISET of `<path>: <code> <message>` with line and column
DROPPED: added 0.

G5 THE FULL SUITE IN FRESH FLIPPED TREES, at C4, CONTROL first and OVERLAY second, serially.
Each is its worktree's FIRST full run, `apps/ui/node_modules` and `apps/ui/dist` reported absent
before it, because the first full run installs both and a second run is not comparable. `cwd`
the worktree; `PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed;
`PYTHONDONTWRITEBYTECODE=1`; `packages.orchestration.task_runner.__file__` printed and inside the
worktree; `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`. A bad
node is the text after `FAILED ` or `ERROR ` up to the first ` - ` or the line's end. The
reviewer measured CONTROL `529 failed, 17876 passed, 29 skipped, 1 warning, 31 errors`, 560 bad
nodes. REPORT OVERLAY's tally and bad-node count as measured. Bad only in OVERLAY: MUST be 0,
per constraint 11. THE GROUP: the CONTROL bad nodes whose `--tb=short` section contains
`Object of type UUID is not JSON serializable` or `unsupported operand type(s) for /:
'PosixPath' and 'UUID'` — the reviewer counted 58. Of the group, REPORT how many are fixed, and
list each one still bad with its last `E   ` line and its test file. Outside the group, REPORT
the fixed count per test file.

G6 THE PROBE, at C4, in OVERLAY after G5; `__pycache__` purged before each run; selection
`tests/test_verifier.py`, `tests/test_task_runner.py` and `tests/test_run_log_cli.py`, with G5's
environment and the flags `-q -p no:randomly -p no:cacheprovider --tb=short -rfE`. CONTROL:
report its tally. M1: in `run_next_task` the one line appending `str(artifact.id)`, its bytes
counted in the file as 1 first, appends `artifact.id` again. M2: in `verify_task_output` the one
`str(a.id) == ` comparison, counted in the file as 1 first, compares `a.id` again. For each,
report the tally and the node ids bad only under the mutation; each MUST name at least one.
After each, restore and confirm the file's bytes equal the carrier-applied ones.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C5. `git status --porcelain` prints `''`;
`git worktree list` one row; `git diff --name-only 1f7a52f9 C5 -- packages apps tests docs
scripts` empty; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, 42;
`ruff check . --output-format concise` rows as a MULTISET at `1f7a52f9`, read from a
`git archive` tree, and at C5, difference empty, 26 at `1f7a52f9`. The changed-path set of
`1f7a52f9`..C5 against the Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name.
The open set BY DISTINCT ID at `1f7a52f9` and at C5: 88 at both, membership identical;
`R-0809`, `R-0880` and `R-0883` open.

G8 THE INSERTION CAP over `1f7a52f9`..C5: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 31 of feature F275 · round 91 · rounds so far 91`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C6's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN91 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN91 sha256=a878e82bf5e40e7e4ed01e77fb3ec07feb03f280031d122d6eafd4ebe61ccf5e
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

ROUND 91 ADDS THE FLIP'S SECOND OVERLAY, on top of the first, under DECISION F275 D64's method.
An artifact id the unified task record holds becomes the artifact's id as a string, and every
lookup of an artifact by such an id compares string forms; tests that hand the unified record a
`UUID` object where it declares a string hand it the string. No path under `packages/`, `apps/`
or `tests/` moves. The round books the round 90 verdict and its three prose slips.

## Next Steps

1. MORE OVERLAYS, one residue group each, every one applied on top of those before it: the
   loader's contract, where callers parse an id with `UUID(...)` or catch the
   `JobNotFoundError` that `load_job_plan` never raises, as in
   `repository_snapshot.revert_repository_apply` and `test_execution_service.execute_test_run`;
   the pydantic calls made on the unified records, such as `TaskEntry.model_validate` and
   `JobPlan.model_dump_json`; the classic `Task` constructions that pass `acceptance_checks`;
   what is left of the classic runner under `job resume`; and the duck-typed test doubles,
   including the `_FakeJob` behind the ruled site at
   `packages/orchestration/project_registry.py:856`.
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
END PLAN91

── SLICE RECORD91 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD91 sha256=d3df0e409a5f8819b53424967504287c7c006c6977647f6404eef850acd87dc9

Gate: F275 R90 — the F275 round 90 entry. VERDICT PASS. Written by the planner and reviewer of session 31 after reading the committed range `844a7f21`..`1f7a52f9` and RE-DERIVING EVERY GATE AND THE RED-PROOF INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 91 that writes the record, per operator amendment amend0827-process-diet rule 1. The round moved no path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; its production code is the diff inside `.agent/authored/f275-r90-overlay.md`.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f275-r90.md` blob was identical to the reviewer's own original at 23717 bytes, `.agent/last_block.md` equalled it from its own commit through `1f7a52f9`, and all three slices matched their BEGIN-marker digests; `.agent/plan.md` equalled PLAN90. The two appends were exact under reader A — 1128932 plus 2495 into the review record and 1277039 plus 4920 into the decisions — with reader B holding at N counted from each slice as 3 and 7, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path, and the largest was the carrier at 314 insertions.

THE OVERLAY HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The reviewer transformed a worktree at `844a7f21` from its own generator run, whose eleven overlay files equalled its own transform-state copies, staged it, and applied the fence extracted from the committed carrier: `git apply --check` and `git apply` exited 0 and exactly the eleven paths of that block's SPEC O changed. With `ast`, the string `getattr` reads of `id`, `name` or `description` on the named receivers in the nine modules went from 19 to 1 and those of the unified names from 0 to 18; `_load_job` holds no `UUID` call, one `normalize_job_id` and one `load_job_plan`; and `ruff` rows over the eleven files, compared without their line and column, went from 4 to 3 with none added. That worktree's first full run read 529 failed, 17876 passed, 29 skipped and 31 errors, 560 bad nodes and the same set as the reviewer's own dry run, against 650 failed and 31 errors, 681 bad nodes, in the reviewer's fresh run of the transform alone: 121 fixed and none newly bad. In the same worktree the unmutated four-file selection read 7 failed and 174 passed; handing `load_job_plan` a `UUID` again read 92 failed with 85 newly bad, 78 in `tests/ui_server/test_command_channel.py` and 7 in `tests/ui_server/test_digest_route.py`; reading the job id as `id` again in `job_digest.py` read 9 failed with exactly its two `test_cost_basis_is_` nodes newly bad. In the primary checkout at `1f7a52f9` the canary read 42 and `ruff check .` read 26 rows, a multiset equal to that at `844a7f21`; the open set stayed 88 with identical membership, `R-0809`, `R-0880` and `R-0883` open.

THREE SENTENCES OF THE ROUND 90 BLOCK WERE WRONG, AND THE WORKER DECLARED EACH. G4(a) ordered the changed paths read in the overlay worktree without ordering its transform state staged there first; G4(c) ordered `ruff` rows compared as a multiset without saying that a row's line and column are dropped, and one row moved lines; and DECISION F275 D64 says the first mutation makes 85 nodes of four test files bad, where the four files are the selection and the 85 nodes lie in two of them. None reached a production path; the prose slips carry all three.
END RECORD91

── SLICE SLIPS91 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS91 sha256=e864ccf7239785f3f12ac72bb46e50cb6578933cbd012d6bccb991a68e3aa82f

2026-09-13 · F275 R90 · G4(a) of the round 90 block ordered `git diff --name-only` in the overlay worktree to list exactly the overlay's paths without ordering that worktree's transform state staged first, so the command would have listed every file the transform rewrote; the worker staged it and declared that. THE RULE THAT FOLLOWS: a gate reading a diff in a worktree names the state that diff is taken against.

2026-09-13 · F275 R90 · G4(c) of the round 90 block ordered `ruff` rows compared as a multiset without saying that each row's line and column are dropped, and one `ui_server.py` row moves 17 lines under the overlay; the worker compared both ways and declared it. THE RULE THAT FOLLOWS: a multiset comparison of tool rows states the fields it keeps.

2026-09-13 · F275 R90 · DECISION F275 D64 says restoring the `UUID` makes 85 nodes of four test files bad, where the four files are the mutation's selection and the 85 nodes lie in two of them, 78 and 7; the worker declared it and the decision landed as written. THE RULE THAT FOLLOWS: a count is attributed to the set it was counted over, never to the selection that contains that set.
END SLIPS91

── SLICE DEC91 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC91 sha256=2e37203f361adbc2baf0b85b47fa96dc393c4dc7477b672e27b1d0aead89ff57

## DECISION F275 D65 (2026-09-13, F275 round 91) — the second overlay: an artifact id the unified task record holds is the artifact's id as a string, lookups compare string forms, and tests hand the unified record strings where it declares strings

CONTEXT. With the first overlay applied, the flipped full suite at `844a7f21` still raises where a `UUID` object reaches the unified record: `json.dumps` refuses one inside the exported record, or a job directory is joined onto one. `TaskEntry.output_artifact_ids` is declared `list[str]` by DECISION F275 D22, while `task_runner.run_next_task` appends `artifact.id`, a `UUID`, and five lookups — in `finalize_task` and `materialize_task_output` of `task_runner.py`, in `verify_task_output` of `verifier.py`, and twice in `_cmd_run_next_task_local` of `apps/cli/commands/job.py` — compare `a.id` with an id read back from that list. Tests construct a `JobPlan` with `uuid4()` as its `job_id`, or put an artifact's `UUID` into a task's list. Two production callers, `repository_snapshot.revert_repository_apply` and `test_execution_service.execute_test_run`, hand `load_job_plan` a `UUID(...)` parse and are NOT in this overlay: each also catches a `JobNotFoundError` the unified loader never raises, which is the next overlay's subject.

CHOSEN: THE STRING FORM IS STORED AND COMPARED. `run_next_task` appends `str(artifact.id)`, and the five lookups compare `str(a.id)`. The artifact keeps its `UUID`, because `JobPlan.artifacts` holds the classic `Artifact` model, which the flip does not change. In the tests, a unified record constructed, assigned, appended to or saved with a `UUID` object in a field it declares a string receives the string form, and an assertion or lookup comparing such a field with a `UUID` object compares string forms; no test is added or deleted. ALTERNATIVES: letting `TaskEntry.output_artifact_ids` hold `UUID` objects, rejected because `_export_job` writes JSON and `_import_job` reads strings back, so a task would compare unequal to itself after one persist; a JSON encoder that writes a `UUID` as a string, rejected for the same round trip and because a path joined onto a `UUID` is not an encoding problem.

CONSEQUENCE. What this overlay fixes, and that it newly breaks nothing, is measured by the gates of round 91's block and recorded in the round 91 ledger entry by the round that books its verdict. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved.

HOW TO REVERSE. Delete `.agent/authored/f275-r91-overlay.md` and this paragraph block; the flipped tree then raises at those `UUID` values again.
END DEC91
