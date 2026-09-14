# Handback — F275 round 99

## Session

`SESSION 33 of feature F275 · round 99 · rounds so far 99`

## Range

Review of `e7c09077`..`HEAD`: seven commits (C0a, C0b, C1, C2, C3, one C4 carrier, C5), plus this handback commit C6.

## Commits

### 5010244b F275 R99 C0a: save the round 99 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r99.md` | +307 / -0 | the block copied with `shutil.copyfile`; `cmp` against `.remedy-wt/r99_block.md` exit 0, byte-identical at 26552 bytes, sha256 `4634e254…` (the digest received, verified before the copy) |

### 4b8821a1 F275 R99 C0b: mirror the round 99 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +153 / -133 | written from the COMMITTED C0a blob, read back with `git show` |

### 4d2168a5 F275 R99 C1: make the plan current for round 99

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +11 / -11 | slice PLAN99, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### 09e4fa5b F275 R99 C2: book the round 98 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6 / -0 | slice RECORD99 appended |

### b490f95b F275 R99 C3: append the round 98 prose slip

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +2 / -0 | slice SLIPS99 appended |

### 57d22c99 F275 R99 C4: commit the flip's tenth overlay, carrier 1 of 1

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r99-overlay-1.md` | +343 / -0 | SPEC C part 1 of 1: 38 prose lines, then ONE ```` ```diff ```` fence holding all 10 file diffs in 303 lines (`packages/orchestration/checkpoints.py` through `tests/test_data_paths.py`), then the closing line; 18826 bytes, sha256 `765fea3984d949f9f290507cc2a185e4712cd57583ba3174ec2e63dacdca2768` |

EDIT's `git diff` is 303 lines, 16232 bytes, sha256 `903074061b87b171193707bbcd9e9118292861e8fa4439fb8723f230d44346b8`. Its 10 file diffs run 22, 10, 93, 31, 13,
13, 31, 13, 13 and 64 lines, 303 in all. That is under 440, so the greedy cut gives ONE part.

### f0b6007b F275 R99 C5: record DECISION F275 D73

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC99 APPENDED after G4's readings, G5 and G6, and after the three worktrees were removed; deletion column ZERO |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10 says no gate runs after C6, and a handback cannot carry a reading of the commit that writes it; the REVIEWER measures this commit |

I read the `+/-` cells above from `git show --numstat` and compared each one against G8. C0a 307/0 = 307/0; C0b 153/133 = 153/133;
C1 11/11 = 11/11; C2 6/0 = 6/0; C3 2/0 = 2/0; C4 343/0 = 343/0; C5 12/0 = 12/0. All seven pairs are EQUAL. Every commit staged
exactly ONE path. The largest is C4 at 343 insertions, and 0 commits reach 500.

### SPEC O, as the overlay carries it (10 paths, in the flipped tree only)

| Path | What |
|---|---|
| `packages/orchestration/checkpoints.py` | O1: `_job_snapshot_reference` imports `job_record_path, resolve_data_root` on one line, reads `path = job_record_path(job_id)`, adds `relative = path.relative_to(resolve_data_root()).as_posix()` after `data = path.read_bytes()`, and returns `(relative, "sha256:" + …)`; docstring and `except (OSError, ValueError)` unchanged |
| `tests/cli/test_job_report.py` | O2: `_job_file` returns `jobs_dir() / job.job_id / "job.json"` |
| `tests/cli/test_mission_cmd.py` | O2: `test_a_deleted_job_renders_as_missing_and_never_crashes` and `test_not_even_when_the_goal_smells_long_lived` use `data_root / "jobs" / job_id / "job.json"`. O3: `_link_job`, `_pending_plan_job` and `TestContinue._green_job` import `RunState` alone from `packages.core.models` and `JobPlan, save_job_plan` from `pingpong_job`, build `JobPlan(job_title=…)` with every other keyword kept, call `save_job_plan(job);`, and read `job.job_id`; the `_Job` double's attribute is `job_id` |
| `tests/orchestration/test_checkpoints.py` | O2: `make_checkpoint`, `test_build_checkpoint_records_the_persisted_snapshot` and `test_the_checkpoint_references_the_persisted_snapshot` use `f"jobs/{…}/job.json"` |
| `tests/orchestration/test_handoff.py` | O2: `_seed_job_checkpoint` uses `f"jobs/{job_id}/job.json"` |
| `tests/orchestration/test_long_run_executor.py` | O2: `test_default_step_runs_the_real_single_task_path` checks `isolate_data_root / "jobs" / job.job_id / "job.json"` |
| `tests/orchestration/test_mission_state.py` | O2: the three named functions use `tmp_path / "jobs" / <job>.job_id / "job.json"` |
| `tests/orchestration/test_resume_cli.py` | O2: `put_checkpoint` uses `f"jobs/{job.job_id}/job.json"` |
| `tests/orchestration/test_resume_kill.py` | O2: `test_the_kill_leaves_checkpoints_for_the_committed_cycles` checks `f"jobs/{job_id}/job.json"` |
| `tests/test_data_paths.py` | O4: the guard imports `storage` alone and loops `for module in (storage,):`; the comment above `_JOB_EVIDENCE_OWNING_MODULES`, the evidence guard's docstring and the classic-store guard's docstring name `storage.py` as the module that names the classic store; the comment and the classic-store guard's docstring each add one sentence saying `checkpoints.py` called `jobs_dir` until the flip moved its job snapshot onto `job_record_path` |

`.remedy-wt/r99w/spec_o.py` made every replacement. Each is an exact literal, confined to the span of the function it names, located
with `ast` (the whole file for the module-level comment). Each count matched: 41 of 41 replacements read `count <n> (want <n>)`
(`.remedy-wt/r99w/spec_o.out`). Every function name O2, O3 and O4 give matched a single definition in the chained tree, so there is
no name difference to declare.

## External actions

| Command | Outcome |
|---|---|
| `git push origin feature/f275-one-world-completion-part-three` after C3, after C4 and after C5 | exit 0 each: `e7c09077..b490f95b`, `b490f95b..57d22c99`, `57d22c99..f0b6007b`. The push of C6 follows this commit, and its result is in the round report |
| `git worktree add --detach .remedy-wt/r99w/wt_EDIT 844a7f21`, then `… wt_CONTROL 844a7f21`, then `… wt_OVERLAY 844a7f21`. This was G4 setup, run after C3 and before the C4 commit, per constraint 10 | exit **0**, **0**, **0** |
| In each worktree: the transform, then `git add -A`, then each COMMITTED overlay in order: `f275-r90-overlay.md`; `f275-r91-overlay.md`; `f275-r92-overlay-1.md` … `-4.md`; `f275-r93-overlay-1.md`, `-2.md`; `f275-r94-overlay-1.md`, `-2.md`; `f275-r95-overlay-1.md` … `-4.md`; `f275-r96-overlay-1.md`; `f275-r97-overlay-1.md`; `f275-r98-overlay-1.md`. Each carrier got `git apply --check` then `git apply`, and `git add -A` ran once after each overlay's parts. Then SPEC O in EDIT only, and the C4 fence in OVERLAY only | exit 0 throughout (see G4) |
| One targeted pytest run in EDIT, after SPEC O and before the diff was taken (constraint 8 allows it) | see deviation 3 |
| In each worktree `git checkout HEAD -- .`, then `git worktree remove` for each, then `git worktree prune -v` | exit 0 throughout. This ran AFTER G6 and BEFORE C5, WITHOUT `--force`. After the restore, `git status --porcelain` printed `''` in each worktree. Only ignored entries were left: `.ruff_cache/` in EDIT; `.data/…`, `.pytest_cache/`, `.ruff_cache/`, `apps/ui/dist/` and `apps/ui/node_modules/` in CONTROL and OVERLAY. All three paths are gone, and `git worktree list` shows one row |
| `git archive` of `ef75e213` and `844a7f21`, extracted by `tarfile` into `.remedy-wt/r99w/gen/` (tree_base, tree_tip, tree_shift, tree_delete, each `git init -q` + `git add -A -f .`); `git archive` of `e7c09077` into `.remedy-wt/r99w/tree_base` (the G7 base lint) | exit 0; plain directories, never registered worktrees |
| `gh` / `remedy` | NOT RUN, not even a version query. No pull request, no branch created or deleted, no merge, no force-push, no history rewrite |

## Verification

Each gate ran through `.remedy-wt/r99w/run.py`. It saves the output to `.remedy-wt/r99w/<name>.out` and appends `PROCESS_EXIT=`
taken from the subprocess's own return code. Every figure the block states reproduced.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C5 | 0 (`g123`) | `cmp` of `.remedy-wt/r99_block.md` against the COMMITTED C0a blob: exit **0**, empty output, 26552 / 26552 bytes, sha256 `4634e25424890319e560fa99dd35bf9a2711d9c635a26c0ec78d12403e10cc08`. `.agent/last_block.md` at C0b equals the C0a blob and is unchanged at C5. Slices FOUND **4**, each MATCHING its BEGIN-marker sha256: PLAN99 2916 bytes / 48 lines, RECORD99 3132 / 6, SLIPS99 561 / 2, DEC99 2595 / 12. TOTAL **307**, slice lines 68, PROSE **239**, as constraint 9 states (caps 490 / 400). No line is a run of one repeated character. All 5 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C5 | 0 (`g123`) | `.agent/plan.md` at C1 is byte-identical to PLAN99 from the committed C0a blob: 2916 bytes, sha256 `8d6738e5…`, **48** lines, one `## Goal`, one `## Next Steps`; unchanged at C5 |
| G3 the record | C5 | 0 (`g123`) | Pre-commit blobs read with `git show` at each commit's PARENT. C2 RECORD99: **1157489** (MATCHES) + 3132 = 1160621. C5 DEC99: **1305147** (MATCHES) + 2595 = 1307742. READER A is exact for both. READER B holds, in order, at N counted by the script as **3** and **6**. The negative controls flip `G`→`g` at offset 1157490 and `D`→`d` at 1305151, each inside the FIRST appended paragraph; BOTH readers REJECTED both. Deletion columns **0 / 0**. C3: the `.agent/prose_slips.md` pre-commit blob is **304743** (MATCHES) + 561 = 305304; post equals pre followed by exactly SLIPS99; deletion 0. Header pattern DERIVED from the pre-commit ledger: one shape, `^Gate: F\d+ R\d+ — `, matching **120 of 120** heads (599 paragraphs). RECORD99's header matches as `Gate: F275 R98 — `; no earlier head has that prefix, and there are 0 duplicate first lines |
| G4 trees, chain, carriers | setup after C3 and before C4; readings after the C4 commit `57d22c99`, before C5 | 0 (`g4_build`), 0 (`c4_split`), 0 (`g4_check`) | **Inputs.** Pinned inputs MATCH: `r77_corrected.json` 120753 bytes `765b5ba9…`, owners 121095 `670c6e95…`, `r61_status.json` 1438 `a4c6cd63…`. Fences: rekey 5186 `f56394e9…`, owner 24253 `7be34374…`, input 10580 `c50da973…`, transform 29032 `075bc0dc…`. DELETE control line count 1. **Generator** exit **0**: **56** paths differ BASE/TIP; **2183** ruled sites recovered by scope at TIP, SHIFT and DELETE; UNRESOLVED **0**. Line-key CONTROL **1895 / 1886 / 1886**. Owner check at TIP: **1908** CONFIRMED, **275** REFUSED, **0** CONTRADICTED. **Transform** exit 0 in EDIT, CONTROL and OVERLAY, reading in each **2183** resolving / **0** not, **264** files, **6097** rewrites, **0** broken. **Chain.** All seventeen earlier carrier applications (r90, r91, r92 ×4, r93 ×2, r94 ×2, r95 ×4, r96, r97, r98; the r98 patch `a048783f…`) exited **0** for both `git apply --check` and `git apply` in each worktree, 102 of 102. `git diff --name-only` read 11, 12, 36, 13, 15, 32, 10, 6 and 9 paths after overlays 1 to 9, and was empty after each `git add -A`. **(a)** The fence from the COMMITTED C4 blob has 38 prose lines before it, one `` ```diff `` line and one closing line, with nothing after but one newline. Part count **1**; line count **303**, ≤ 440. It equals EDIT's saved `git diff` stdout AND EDIT's live `git diff` (16232 bytes, `90307406…`). In OVERLAY, `git apply --check` exit **0**, then `git apply` exit **0**. `git diff --name-only` there, against the staged index, lists **10** paths: MISSING `[]`, EXTRA `[]` against SPEC O's 10, each byte-identical to EDIT's. Cross-check: the tracked paths whose bytes differ between OVERLAY and CONTROL are the same 10. **(b)** `ast` over SPEC O's ten paths, CONTROL then OVERLAY, names matched exactly. Flat `.json` f-strings after a job id: **17** and **2**. CONTROL per path: `checkpoints.py` 2 (227, 231), `test_job_report.py` 1 (289), `test_mission_cmd.py` 2 (247, 470), `test_checkpoints.py` 3 (65, 149, 367), `test_handoff.py` 1 (114), `test_long_run_executor.py` 1 (559), `test_mission_state.py` 3 (438, 453, 864), `test_resume_cli.py` 1 (68), `test_resume_kill.py` 1 (220), `tests/test_data_paths.py` 2 (154, 276). OVERLAY: `tests/test_data_paths.py` 2 (154, 276), both there. String constants containing the `storage import save_job;` piece **3** and **0** (`test_mission_cmd.py` 74, 325, 505); containing the `pingpong_job import JobPlan, save_job_plan;` piece **0** and **3** (same three lines). `Assign` targets of `_Job` named `id` **1** and **0**, named `job_id` **0** and **1** (line 1405). Bare names plus import aliases named `checkpoints` in the guard **2** and **0** (alias 833, Name 835). All MATCH. **(c)** `ruff check --output-format concise` over SPEC O's 10 paths, run from inside each tree: CONTROL exit **1** with **16** rows; OVERLAY exit **1** with **16** rows (12 `I001`, 1 `F401`, 3 `F821`, the same rows in both). As a multiset of `<path>: <code> <message>` with line and column dropped: added **0**, removed **0** |
| G5 full suite, CONTROL then OVERLAY | after the C4 commit, before C5 | 1 (`g5_CONTROL`), 1 (`g5_OVERLAY`), 0 (`g5_cmp`) | Each was its worktree's FIRST pytest run of any kind. `apps/ui/node_modules` and `apps/ui/dist` were ABSENT before each run and present after it. `PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`; `cwd` the worktree; `packages.orchestration.pingpong_job.__file__` inside the worktree in both. pytest exit 1 in both. CONTROL **`84 failed, 18351 passed, 29 skipped, 1 warning, 7 errors`** (1404.20s), **91** bad nodes: MATCHES the reviewer's. OVERLAY **`63 failed, 18372 passed, 29 skipped, 1 warning, 7 errors`** (1429.23s), **70** bad nodes. **Bad only in OVERLAY: 0**, so constraint 11 required no re-run and reports no FLAKY node. Bad only in CONTROL (fixed): **21**. The reviewer's dry-run flake `tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_post_to_non_commands_path_is_405` is bad in neither of my runs. Section mapping: 0 header mismatches in both transcripts |
| G6 the probes | after G5, before C5, in OVERLAY | 0 (`g6`) | `__pycache__` purged before each of the four runs (0 directories each time); the module printed inside the worktree each time. Both mutations in `packages/orchestration/checkpoints.py`, inside `_job_snapshot_reference` (lines 218-232) only. **M1**: the bytes `relative = path.relative_to(resolve_data_root()).as_posix()` count **1** in the function and **1** in the file, as stated; they become `relative = f"jobs/{job_id}.json"`. **M2**: the bytes `path = job_record_path(job_id)` count **1** and **1**; they become `path = job_record_path(job_id).parent.with_suffix(".json")`. Selection `tests/orchestration/test_checkpoints.py` for both. M1 unmutated: exit 0, **`37 passed`**; mutated: exit 1, **`2 failed, 35 passed`**. M2 unmutated: exit 0, **`37 passed`**; mutated: exit 1, **`2 failed, 35 passed`**. Bad only under each: `TestWriting::test_build_checkpoint_records_the_persisted_snapshot` and `TestCycleBoundaryWiring::test_the_checkpoint_references_the_persisted_snapshot`, both REQUIRED and both present, under M1 and under M2. Nothing recovered under either. After each probe the file was restored; its bytes equal the pre-mutation sha256 `7fc93eb1…` and EDIT's bytes |
| G7 tree, canary, lint, path set, open set | C5 | 0 (`g78`) | `git status --porcelain` exit 0 `''`. `git worktree list` **1** row. `git diff --name-only e7c09077 f0b6007b -- packages apps tests docs scripts` exit 0, empty. CANARY exit **0**, **42 passed**. `ruff check . --output-format concise` exit 1 at both ends: **26** rows at `e7c09077` (archive tree) and **26** at C5, multiset difference EMPTY both ways. `.py` files under `.agent/`: **0**. Changed paths `e7c09077`..C5: **7**, against the Bundle minus handoff: **7**; MISSING `[]`, EXTRA `[]`. Open set BY DISTINCT ID: **88** at `e7c09077` and **88** at C5 (112 − 24 each), membership IDENTICAL; `R-0809`, `R-0880` and `R-0883` OPEN at both |
| G8 insertion cap | C5 | 0 (`g78`) | C0a 307/0 1 path, C0b 153/133 1, C1 11/11 1, C2 6/0 1, C3 2/0 1, C4 343/0 1, C5 12/0 1; commits reaching 500 insertions **0** |

G5, THE FIXED NODES PER TEST FILE (21): `tests/cli/test_mission_cmd.py` 14, `tests/orchestration/test_mission_state.py` 3,
`tests/orchestration/test_checkpoints.py` 2, `tests/cli/test_job_report.py` 1, `tests/orchestration/test_long_run_executor.py` 1.
The full node list is in `.remedy-wt/r99w/g5_cmp.out`.

STOP READINGS, per constraint 3: `.agent/STOP` was ABSENT both before C0a and before C6 (`test -e` exit 1, `ls -la` exit 2,
`os.path.exists` False). Transcripts: `.remedy-wt/r99w/stop_before_C0a.txt` and `.remedy-wt/r99w/stop_before_C6.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r99.md` | `cmp` exit 0 against `.remedy-wt/r99_block.md`, 26552 bytes, sha256 `4634e25424890319e560fa99dd35bf9a2711d9c635a26c0ec78d12403e10cc08` |
| PLAN99 | `.agent/plan.md` | byte-identical, 2916 bytes, sha256 `8d6738e5e079f0b667348db670f043c8c5d3bab48f438ca4f1b1de67105ce15a` (the BEGIN marker's) |
| RECORD99 | `.agent/live_review.md` | exact suffix at C2 under readers A and B, 3132 bytes, sha256 `9d4383d5b306329a0434bad78e59afc6211926fd3e8d1922f87bac42f25137c5` |
| SLIPS99 | `.agent/prose_slips.md` | post equals the 304743-byte pre-commit blob followed by exactly the slice, 561 bytes, sha256 `177a9f7e140e0cd765e844279395bab31d042e7154e1513682033796454b42d9` |
| DEC99 | `.agent/decisions.md` | exact suffix at C5 under readers A and B, 2595 bytes, sha256 `b236320e7e6c426333c223947893c7f112684aec980e77c139cfa1b8cfca46fd` |

Every slice was applied from the bytes of the COMMITTED C0a blob, and NO SLICE WAS EDITED. The C4 carrier is my own text, written from
SPEC C over my own SPEC O edit.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 round 98 verdict | done | |
| C3 round 98 prose slip | done | |
| C4 overlay carriers (SPEC C over SPEC O) | done | one carrier, 343 insertions; the whole 303-line diff fits one part |
| C5 DECISION F275 D73 | done | after G4's readings, G5 and G6, and after the worktrees were removed |
| C6 handback | done | this commit |
| SPEC O1 · O2 · O3 · O4 | done | 10 paths; readings as deviations 4 and 5 state |
| G4 · G5 · G6 | done | bad only in OVERLAY 0, so constraint 11 did not stop the round; both probes as ordered |
| G1 · G2 · G3 · G7 · G8 | done | exit 0 · 0, at C5 |

## Deviations & assumptions

1. **NO DEPARTURE FROM THE COMMIT SEQUENCE.** The commits are exactly the Bundle: C0a, C0b, C1, C2, C3, one C4 carrier (SPEC C's cut
   produced one part), C5, C6. `.agent/context.md` is not in the Change set and was not touched.
2. **SCRATCH AND THE SHELL'S STARTING DIRECTORY.** This session's shell started with `.remedy-wt/r98` as its working directory, which
   is the reviewer's scratch path. Every command and every file read used absolute paths elsewhere, and nothing under `.remedy-wt/r90/`
   through `.remedy-wt/r98/` was opened. I read round 98's WORKER scratch (`.remedy-wt/r98w/`) for its scripts only, and ported them
   with counted replacements (`port.py`, `g4_build_port.py`, `g6_port.py`, `g_port.py`); `spec_o.py`, `c4_carrier.py`'s prose and
   SPEC_O list, and `g4_check.py`'s (b) are new. All of this worker's scratch is under `.remedy-wt/r99w/`, uncommitted.
3. **EDIT RAN ONE TARGETED PYTEST RUN WHILE SPEC O WAS MADE.** Constraint 8 allows this, and it is not a gate reading. It ran after
   SPEC O and before the diff was taken, over the nine test files SPEC O touches: exit 1, `3 failed, 485 passed, 7 errors`, 10 bad
   nodes, all in `tests/orchestration/test_resume_kill.py` (7, the classic kill-and-resume fixture) and `TestRoutedHandler` of
   `tests/test_data_paths.py` (3); every one of those 10 is also bad in G5's CONTROL. Before writing the carrier I also ran my
   G4(b)/(c) script with EDIT in OVERLAY's place (`.remedy-wt/r99w/g4_pre.out`): 17/3/0/1/0/2 and 2/0/3/0/1/0, ruff added 0 and
   removed 0. That step ran ruff and `ast` in CONTROL, not pytest, so G5's first-run condition still held.
4. **HOW I READ O3's "`str(job.id)` and `job.id` become `job.job_id`".** Literally: `str(job.id)` becomes `job.job_id` with the
   `str(...)` dropped (`JobPlan.job_id` is already a `str`), then each remaining `job.id` becomes `job.job_id`. So `_link_job` and
   `_green_job` pass `job.job_id` to `link_job_to_mission`, and all three print `job.job_id`.
5. **HOW I READ O4's docstring order.** The classic-store guard's summary line said "The excluded pair must keep naming the classic
   store"; "pair" counted `checkpoints.py` as a classic-store module, so it now reads "The excluded module …". The comment's closing
   sentence ("The reason is written down because …") was reflowed around the inserted sentence, its words unchanged. G4(b) reads
   "the LAST literal part" of an f-string as the last `Constant` among its values.
6. **G4(c) EXITS 1 WHERE THE BLOCK SAID IT WOULD.** Ruff exits 1 in both trees with 16 rows each. That is a reported reading, not a
   red gate.

## Next

The reviewer re-runs the gates and issues the round 99 verdict.

Operator questions open: 1

After that, per `.agent/plan.md`, come more overlays, one residue group each, applied on top of these ten. In order: production
code that hands a `JobPlan` a `JobBudgets` model; the self-dogfood runtimes; the classic-shaped tests of routed handlers in
`tests/test_data_paths.py`; and the classic runner under `job resume`, whose kill-and-resume fixture still builds a classic job. Then
the flip lands as a series of commits under the cap, then the classic store, then the closure sequence.

Context self-assessment: this worker's context is comfortable; the round needed no fresh session.
