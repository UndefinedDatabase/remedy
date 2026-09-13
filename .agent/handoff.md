# Handback — F275 round 91

## Session

`SESSION 31 of feature F275 · round 91 · rounds so far 91`

## Range

Review of `1f7a52f9`..`HEAD` (the seven commits C0a–C5 plus this handback commit C6).

## Commits

### e9487e7e F275 R91 C0a: save the round 91 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r91.md` | +260 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r91_block.md` at 23060 bytes |

### 88afb92d F275 R91 C0b: mirror the round 91 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +165 / -163 | written from the COMMITTED C0a blob read back with `git show` |

### c0e364d8 F275 R91 C1: make the plan current for round 91

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12 / -11 | slice PLAN91, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### ff8ed09b F275 R91 C2: book the round 90 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +8 / -0 | slice RECORD91 appended |

### e443a783 F275 R91 C3: append the round 90 prose slips

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +6 / -0 | slice SLIPS91 appended |

### 444de3ee F275 R91 C4: commit the flip's second overlay carrier

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r91-overlay.md` | +412 / -0 | SPEC C: 31 lines of prose, then ONE ```` ```diff ```` fence holding the verbatim 379-line, 17241-byte stdout of `git diff` in EDIT against its staged index, then the closing fence line and one newline; 19368 bytes, sha256 `b8c2b391a0c066564e44007e79a8653d2ff63019261650e1c0129ec3f7394eb7` |

### 78fae2e7 F275 R91 C5: record DECISION F275 D65

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +10 / -0 | slice DEC91 APPENDED after G4, G5 and G6 ran; deletion column ZERO |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10: no gate runs after C6, and a handback cannot carry a reading of the commit that writes it; the REVIEWER measures this commit |

THE `+/-` CELLS ABOVE WERE READ FROM `git show --numstat` AND COMPARED CELL BY CELL AGAINST G8:
C0a 260/0 = 260/0; C0b 165/163 = 165/163; C1 12/11 = 12/11; C2 8/0 = 8/0; C3 6/0 = 6/0; C4 412/0 = 412/0;
C5 10/0 = 10/0. Seven of seven pairs EQUAL, zero differ. Every commit staged exactly ONE path; the largest
insertion count is C4 at 412.

### SPEC O, as carried by the overlay (twelve paths, inside the flipped tree only; +/- read with `git apply --numstat` of the extracted fence)

| Path | +/- in the overlay | What |
|---|---|---|
| `packages/orchestration/task_runner.py` | +3 / -3 | O1: `run_next_task` appends `str(artifact.id)`; `finalize_task` and `materialize_task_output` compare `str(a.id)` |
| `packages/orchestration/verifier.py` | +1 / -1 | O1: `verify_task_output` compares `str(a.id)` |
| `apps/cli/commands/job.py` | +2 / -2 | O1: both lookups in `_cmd_run_next_task_local` compare `str(a.id)` |
| `tests/test_verifier.py` | +8 / -8 | O2: eight appends to `output_artifact_ids` take the string form (seven `artifact.id`, one dangling `uuid4()`) |
| `tests/test_task_runner.py` | +7 / -7 | O2: one append and one member assignment take the string form; five comparisons of a list member with `a.id` / `job.artifacts[-1].id` use `str(...)` |
| `tests/test_run_log_cli.py` | +5 / -5 | O2: five appends `str(artifact.id)` |
| `tests/test_cli_main.py` | +3 / -3 | O2: three appends `str(artifact.id)` |
| `tests/cli/test_patch_cmd.py` | +2 / -2 | O2: `_job` constructs `JobPlan(job_id=str(job_id or uuid4()), ...)`; the prefix reads `job.job_id[:8]` in place of `.hex[:8]` |
| `tests/storage/test_persistence.py`, `tests/ui_contracts/test_responsive.py` | +2 / -2 each | O2: two `"job_id": uuid4()` defaults read `str(uuid4())` |
| `tests/orchestration/test_escalation.py`, `tests/test_workspace.py` | +1 / -1 each | O2: a prefix derived from `task_id` with `.hex[:8]` reads `task_id[:8]` (deviation 3) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r91w/wt_EDIT 844a7f21`, `... wt_CONTROL 844a7f21`, `... wt_OVERLAY 844a7f21` (G4, before C4) | exit **0**, **0**, **0** |
| in each worktree: transform, `git add -A`, `git apply --check` and `git apply` of the fence of the COMMITTED `.agent/authored/f275-r90-overlay.md`, `git add -A`; then SPEC O in EDIT only, the C4 fence applied in OVERLAY only | exit 0 throughout (see G4) |
| two full suite runs in EDIT, one before SPEC O and one after it (constraint 8 allows tests there) | pytest exit 1 both (red suites); readings in deviation 1 |
| `git checkout HEAD -- .` in each worktree, then `git worktree remove` each, then `git worktree prune -v` | exit 0 throughout, AFTER G6 and BEFORE C5, WITHOUT `--force`; `git status --porcelain` `''` in each before removal (only ignored `.data/`, `.pytest_cache/`, `.ruff_cache/`, `apps/ui/dist/`, `apps/ui/node_modules/`); all three paths gone; `git worktree list` one row |
| `git archive` of `ef75e213` and `844a7f21` extracted by `tarfile` into `.remedy-wt/r91w/gen/` (tree_base, tree_tip, tree_shift, tree_delete, each `git init -q` + `git add -A -f .`), and `1f7a52f9` into `.remedy-wt/r91w/tree_base` (G7 base lint) | exit 0; plain directories, never registered worktrees |
| `git push origin feature/f275-one-world-completion-part-three` | run after C6; its result is in the round report |
| `gh` / `remedy` | NOT RUN. No pull request, no branch created or deleted, no merge, no force-push, no history rewrite |

## Verification

Each gate ran through `.remedy-wt/r91w/run.py`, which saves output to `.remedy-wt/r91w/<name>.out` and appends
`PROCESS_EXIT=` from the subprocess's own return code. Every figure the block states reproduced.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C5 | 0 (`g123`) | `cmp` of `.remedy-wt/r91_block.md` against the COMMITTED C0a blob exit **0**, empty output, 23060 / 23060 bytes, sha256 `a5e695d1…58f913`; `.agent/last_block.md` at C0b equals the C0a blob and is unchanged at C5; slices FOUND **4**: PLAN91 2983 bytes / 49 lines, RECORD91 3472 / 8, SLIPS91 1161 / 6, DEC91 2628 / 10, each MATCHING its BEGIN-marker sha256; TOTAL **260**, slice lines 73, PROSE **187**, as constraint 9 states; no line is a run of one repeated character; all 5 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C5 | 0 (`g123`) | `.agent/plan.md` at C1 byte-identical to PLAN91 from the committed C0a blob, 2983 bytes; **49** lines; one `## Goal`, one `## Next Steps`; unchanged at C5 |
| G3 the record | C5 | 0 (`g123`) | Pre-commit blobs read with `git show` at each commit's PARENT. C2 RECORD91: **1131427** (MATCHES) + 3472 = 1134899; C5 DEC91: **1281959** (MATCHES) + 2628 = 1284587. READER A exact for both; READER B holds at N counted by the script as **4** and **5**, in order. Negative controls `G`→`g` at offset 1131428 and `D`→`d` at 1281963, each in the FIRST appended paragraph, REJECTED by BOTH readers. Deletion columns **0 / 0**. C3: `.agent/prose_slips.md` pre-commit blob **299259** (MATCHES) + 1161 = 300420, post equals pre followed by exactly SLIPS91, deletion 0 (reader B N=3 also holds). Header pattern DERIVED from the pre-commit ledger: one shape `^Gate: F\d+ R\d+ — ` matching **112 of 112** heads (570 paragraphs); RECORD91's header matches as `Gate: F275 R90 — `, no earlier head has that prefix, duplicate first lines 0 |
| G4 trees, chain, carrier | C4 | 0 (`g4_build`), 0 (`c4_carrier`), 0 (`g4_check`) | Pinned inputs MATCH: `r77_corrected.json` 120753 bytes `765b5ba9…`, owners 121095 `670c6e95…`, `r61_status.json` 1438 `a4c6cd63…`. Fences: rekey 5186 `f56394e9…`, owner 24253 `7be34374…`, input 10580 `c50da973…`, transform 29032 `075bc0dc…`; first overlay carrier 14527 bytes `92529281…`, its patch 12756 bytes `aa9c08fb…`. DELETE control line count 1. Generator exit **0**: paths differing BASE/TIP **56**; ruled sites **2183** recovered by scope at TIP, SHIFT, DELETE, UNRESOLVED **0**; line-key CONTROL **1895 / 1886 / 1886**; owner check at TIP **1908** CONFIRMED, **275** REFUSED, **0** CONTRADICTED. Transform exit 0 in EDIT, CONTROL, OVERLAY: **2183** resolving / **0** not, **264** files, **6097** rewrites, **0** broken, in each. First overlay `git apply --check` exit **0** and `git apply` exit **0** in each; after `git add -A`, `git diff --name-only` empty in each. (a) fence from the COMMITTED C4 blob (one `` ```diff `` line, one closing line, nothing after but one newline), 17241 bytes sha256 `eff93a17…1a024032`, equal to EDIT's saved `git diff` stdout; OVERLAY `git apply --check` exit **0**, `git apply` exit **0**; `git diff --name-only` there against the staged index: **12** paths = EDIT's 12, each byte-identical to EDIT's: `apps/cli/commands/job.py`, `packages/orchestration/task_runner.py`, `packages/orchestration/verifier.py`, `tests/cli/test_patch_cmd.py`, `tests/orchestration/test_escalation.py`, `tests/storage/test_persistence.py`, `tests/test_cli_main.py`, `tests/test_run_log_cli.py`, `tests/test_task_runner.py`, `tests/test_verifier.py`, `tests/test_workspace.py`, `tests/ui_contracts/test_responsive.py`; under `packages/` and `apps/` exactly the three named, the rest under `tests/`; cross-check: tracked paths whose bytes differ OVERLAY vs CONTROL = the same 12. (b) `str(a.id) == ` CONTROL **0**, OVERLAY **5** (task_runner 2, verifier 1, job 2); in `task_runner.py` `output_artifact_ids.append(str(artifact.id))` **0 / 1**, `output_artifact_ids.append(artifact.id)` **1 / 0**; `def test_` per changed test file equal CONTROL/OVERLAY in all 9 (13, 68, 15, 48, 62, 45, 30, 51, 84). (c) ruff by stdin, `cwd` inside each worktree, over the 12: CONTROL **11** rows, OVERLAY **11** rows (all `I001`), as a multiset of `<path>: <code> <message>` with line and column dropped: added **0**, removed 0 |
| G5 full suite, CONTROL then OVERLAY | C4 | 1 (`g5_CONTROL`), 1 (`g5_OVERLAY`), 0 (`g5_cmp`) | Before each run `apps/ui/node_modules` and `apps/ui/dist` ABSENT (both present after); `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`, `cwd` the worktree; `packages.orchestration.task_runner.__file__` inside the worktree in both. pytest exit 1 in both (red suites, as expected). CONTROL **`529 failed, 17876 passed, 29 skipped, 1 warning, 31 errors`** (1399.79s), **560** bad nodes — MATCHES. OVERLAY **`485 failed, 17920 passed, 29 skipped, 1 warning, 31 errors`** (1400.60s), **516** bad nodes. Bad only in OVERLAY **0**. Bad only in CONTROL 44. THE GROUP in CONTROL: **58** — MATCHES; fixed **42** (`test_run_log_cli.py` 19, `test_patch_cmd.py` 9, `test_cli_main.py` 6, `test_responsive.py` 4, `test_persistence.py` 3, `test_long_run_executor.py` 1); still bad **16**, listed below. OUTSIDE the group, fixed per test file: `tests/orchestration/test_escalation.py` 1, `tests/test_workspace.py` 1 |
| G6 the probe in OVERLAY | C4 | 0 (`g6`) | `__pycache__` purged before each run (0 directories each time); module printed inside OVERLAY before each run. CONTROL exit 1 **`1 failed, 136 passed`** (`test_task_runner.py::test_context_includes_prior_task_summaries`). M1: the line `    task.output_artifact_ids.append(str(artifact.id))` count in `task_runner.py` **1**, appends `artifact.id` again: exit 1 **`17 failed, 120 passed`**, bad only under M1 **16** (9 in `test_task_runner.py`, 7 in `test_verifier.py`), recovered 0. M2: `str(a.id) == ` count in `verifier.py` **1**, compares `a.id` again: exit 1 **`25 failed, 112 passed`**, bad only under M2 **24**, all in `test_verifier.py`, recovered 0. After each, bytes restored and EQUAL to the carrier-applied ones (EDIT's) |
| G7 tree, canary, lint, path set, open set | C5 | 0 (`g78`) | `git status --porcelain` exit 0 `''`; `git worktree list` **1** row; `git diff --name-only 1f7a52f9 78fae2e7 -- packages apps tests docs scripts` exit 0, empty; CANARY exit **0**, **42 passed**; `ruff check . --output-format concise` exit 1 at both ends, **26** rows at `1f7a52f9` (archive tree) and **26** at C5, multiset difference EMPTY both ways; `.py` files under `.agent/` **0**; changed paths `1f7a52f9`..C5 **7** against the Bundle minus handoff **7**, MISSING `[]`, EXTRA `[]`. Open set BY DISTINCT ID: **88** at `1f7a52f9` and **88** at C5 (112 − 24 each), membership IDENTICAL; `R-0809`, `R-0880`, `R-0883` OPEN at both |
| G8 insertion cap | C5 | 0 (`g78`) | C0a 260/0 1 path, C0b 165/163 1, C1 12/11 1, C2 8/0 1, C3 6/0 1, C4 412/0 1, C5 10/0 1; commits reaching 500 insertions **0** |

G5, THE GROUP'S SIXTEEN STILL-BAD NODES in OVERLAY, each with its last `E   ` line:

- `tests/cli/test_patch_cmd.py::TestItMintsNoRefusalVocabularyOfItsOwn::test_a_refusal_never_persists_the_job` — `E   AttributeError: <module 'apps.cli.commands.patch' from '…/wt_OVERLAY/apps/cli/commands/patch.py'> has no attribute 'save_job'`
- `tests/orchestration/test_long_run_executor.py::TestDefaultTaskStep::test_default_step_runs_the_real_single_task_path` — `E     + blocked`
- `tests/orchestration/test_long_run_executor.py::TestJobRunCommand::test_a_capped_config_value_names_the_config_key` — `E   SystemExit: 1`
- `tests/orchestration/test_long_run_executor.py::TestJobRunCommand::test_multi_cycle_path_runs_the_loop_after_the_gate` — `E   SystemExit: 1`
- `tests/orchestration/test_long_run_executor.py::TestJobRunCommand::test_the_flag_is_capped_and_the_operator_is_told` — `E   SystemExit: 1`
- `tests/orchestration/test_repository_snapshot.py::TestBuildSnapshotTruth::test_reverted_apply` — `E   TypeError: unsupported operand type(s) for /: 'PosixPath' and 'UUID'`
- `tests/orchestration/test_repository_snapshot.py::TestNoRawContentLeaks::test_revert_result_no_content` — same `E` line
- `tests/orchestration/test_repository_snapshot.py::TestRevertEvidenceStatus::test_successful_revert_evidence_complete` — same
- `tests/orchestration/test_repository_snapshot.py::TestRevertRepositoryApply::test_revert_blocked_when_drift_detected` — same
- `tests/orchestration/test_repository_snapshot.py::TestRevertRepositoryApply::test_revert_contract_denied` — same
- `tests/orchestration/test_repository_snapshot.py::TestRevertRepositoryApply::test_revert_deletes_created_files` — same
- `tests/orchestration/test_repository_snapshot.py::TestRevertRepositoryApply::test_revert_job_not_found` — same
- `tests/orchestration/test_repository_snapshot.py::TestRevertRepositoryApply::test_revert_permission_denied` — same
- `tests/orchestration/test_repository_snapshot.py::TestRevertRepositoryApply::test_revert_success` — same
- `tests/orchestration/test_repository_snapshot.py::TestRevertRepositoryApply::test_revert_verifies_restored_state` — same
- `tests/orchestration/test_test_execution_service.py::TestExecuteTestRunGates::test_job_not_found_blocked` — same

The eleven `PosixPath`/`UUID` nodes are O3's two out-of-scope callers. The other five no longer raise on a `UUID`
and now fail on a later residue: the patched `save_job` name, and a job-run whose cycles end `blocked` with
`no_ready_tasks`.

STOP READINGS, per constraint 3: before C0a and before C6, `.agent/STOP` ABSENT at both — `test -e` exit 1,
`ls -la` exit 2, `os.path.exists` False — transcripts `.remedy-wt/r91w/stop_before_C0a.txt` and
`.remedy-wt/r91w/stop_before_C6.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r91.md` | `cmp` exit 0 against `.remedy-wt/r91_block.md`, 23060 bytes, sha256 `a5e695d1bb536f73b95d3ab16d7be322df00df4c8159f9d283b300f84158f913` |
| PLAN91 | `.agent/plan.md` | byte-identical, 2983 bytes, sha256 `a878e82bf5e40e7e4ed01e77fb3ec07feb03f280031d122d6eafd4ebe61ccf5e` |
| RECORD91 | `.agent/live_review.md` | exact suffix at C2 under readers A and B, 3472 bytes, sha256 `d3df0e409a5f8819b53424967504287c7c006c6977647f6404eef850acd87dc9` |
| SLIPS91 | `.agent/prose_slips.md` | post equals the 299259-byte pre-commit blob followed by exactly the slice, 1161 bytes, sha256 `e864ccf7239785f3f12ac72bb46e50cb6578933cbd012d6bccb991a68e3aa82f` |
| DEC91 | `.agent/decisions.md` | exact suffix at C5 under readers A and B, 2628 bytes, sha256 `2e37203f361adbc2baf0b85b47fa96dc393c4dc7477b672e27b1d0aead89ff57` |

Every slice was applied by bytes from the COMMITTED C0a blob, and NO SLICE WAS EDITED. C4 is the worker's own
text from SPEC C over the worker's own SPEC O edit.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 round 90 verdict | done | |
| C3 round 90 prose slips | done | |
| C4 overlay carrier (SPEC C over SPEC O) | done | 412 insertions, under 500 |
| C5 DECISION F275 D65 | done | after G4, G5 and G6 ran |
| C6 handback | done | this commit |
| G4 · G5 · G6 | done | at C4; exits in the table; G5 bad only in OVERLAY 0, so constraint 11 did not stop the round |
| G1 · G2 · G3 · G7 · G8 | done | exit 0 · 0, at C5 |

## Deviations & assumptions

1. **EDIT RAN THE FULL SUITE TWICE, TO FIND THE SITES.** Before SPEC O, EDIT's first full run read
   `529 failed, 17876 passed, 29 skipped, 1 warning, 31 errors`, 560 bad nodes. That is the same tally as G5's
   CONTROL, with the same group of 58 found by the same script. I read each group node's traceback, and then every
   other bad node whose section mentions `UUID` or `.hex`, to choose the O2 sites. After SPEC O, EDIT's second
   run read `484 failed, 17927 passed, 23 skipped, 1 warning, 31 errors`, 515 bad nodes, with 0 newly bad. That run
   is not comparable: `node_modules` was already installed, which unskipped six tests and turned
   `test_vitest_passes` green. The carrier's diff was taken after those runs, which SPEC C of this block allows.
   The tracked paths that differ from the index were still exactly SPEC O's twelve, and `git status` showed no
   untracked file.
2. **O2 APPLIED TO EVERY RULE SITE IN A TOUCHED FILE.** A file was touched only when one of its tests was bad in the
   flipped tree under the rule, or went bad under O1. Inside such a file I applied the rule at every site it
   names, including three sites whose test was not made green by that edit. In `test_verifier.py`, the dangling
   `uuid4()` append sits in a test that passes both ways. In `test_task_runner.py`, the `phantom_id` member
   assignment sits in a test that passes both ways. Also in `test_task_runner.py`, the `art.id` append sits in
   `test_context_includes_prior_task_summaries`, which fails both before and after on `task_id` being `''`; that
   is the one bad node in G6's CONTROL. Under O1 alone, 24 nodes of `test_verifier.py` and `test_task_runner.py`
   went bad in EDIT, and O2 returns all of them.
3. **TWO `.hex` EDITS NOW TEST NOTHING FOR THEIR FIXTURE.** In `test_escalation.py` and `test_workspace.py`, O2
   turns `task_id.hex[:8]` into `task_id[:8]`, as the rule orders, and both nodes go green. The flipped
   `TaskEntry` built by these fixtures has `task_id == ''`, though. So the prefix is `''`, and `'' in ...` holds
   for any decision id and any filename. For a real id the assertion is exactly as strong as before, because a
   canonical UUID string's first eight characters equal `.hex[:8]`. For this fixture it tests nothing until task
   ids are minted, which is a later residue. I declare it here and have not repaired it; it is the reviewer's
   call whether this counts against "no assertion loosened".
4. **DEC91'S CHOSEN PARAGRAPH OMITS THE `.hex` PREFIX EDITS.** It describes the test edits as constructions,
   assignments, appends and saves taking the string form, plus comparisons with a `UUID` object. SPEC O2 also
   orders a prefix derived with `.hex` to use the string form, and the overlay does that at three sites
   (`test_patch_cmd.py`, `test_escalation.py`, `test_workspace.py`). DEC91 landed byte for byte per constraint 1.
   Its claim about the two O3 callers checks out at `844a7f21`: both parse with `UUID(...)` and both catch
   `JobNotFoundError`.
5. **G5 READINGS THE BLOCK LEFT TO BE MEASURED.** OVERLAY's tally and 516 bad nodes, the group's 42 fixed and 16
   still bad, and the fixed count outside the group (1 in `test_escalation.py`, 1 in `test_workspace.py`) are
   measured, not compared against a figure. A section was paired with its node by position within the ERRORS and
   FAILURES sections, cross-checked against each section header: 0 mismatches in all four transcripts. A node id is
   the text up to the first ` - `, as G5 defines it.
6. **NO OTHER DEVIATION.** The commit sequence is exactly the Bundle. `.agent/context.md` is not in the Change set
   and was not touched. The reviewer's `.remedy-wt/r90/` and `.remedy-wt/r91/` were not opened; round 90's worker
   scratch `.remedy-wt/r90w/` was read for its scripts only. All of this worker's scratch is under
   `.remedy-wt/r91w/`, uncommitted.

## Next

The reviewer re-runs the gates and issues the round 91 verdict.

Operator questions open: 1

After that, per `.agent/plan.md`: more overlays, one residue group each, applied on top of these two, starting with
the loader's contract for `revert_repository_apply` and `execute_test_run`; then the flip as a series of commits
under the cap; then the classic store and the closure sequence.
