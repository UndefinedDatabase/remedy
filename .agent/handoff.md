# Handback — F275 round 98

## Session

`SESSION 33 of feature F275 · round 98 · rounds so far 98`

## Range

Review of `ac17fd6e`..`HEAD`: seven commits (C0a, C0b, C1, C2, C3, one C4 carrier, C5), plus this handback commit C6.

## Commits

### 8c2df4d4 F275 R98 C0a: save the round 98 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r98.md` | +287 / -0 | the block copied with `shutil.copyfile`; `cmp` against `.remedy-wt/r98_block.md` exit 0, byte-identical at 24607 bytes, sha256 `36de0227…` (the digest received, verified before the copy) |

### df75d04d F275 R98 C0b: mirror the round 98 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +131 / -117 | written from the COMMITTED C0a blob, read back with `git show` |

### 88c49ff7 F275 R98 C1: make the plan current for round 98

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +7 / -8 | slice PLAN98, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### 67eea0e4 F275 R98 C2: book the round 97 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6 / -0 | slice RECORD98 appended |

### 967378bb F275 R98 C3: append the round 97 prose slip

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +2 / -0 | slice SLIPS98 appended |

### 159163c3 F275 R98 C4: commit the flip's ninth overlay, carrier 1 of 1

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r98-overlay-1.md` | +327 / -0 | SPEC C part 1 of 1: 39 prose lines, then ONE ```` ```diff ```` fence holding all 9 file diffs in 286 lines (`apps/cli/commands/contract_cmd.py` through `tests/cli/test_test_run_runtime.py`), then the closing line; 16121 bytes, sha256 `ff0f867b0c2b421ebfea18813a0690974020d546eeea3a395b567f8f20ef92cc` |

EDIT's `git diff` is 286 lines, 13426 bytes, sha256 `a048783f59be3ca073b26168876309ee8fe3f33744f43bf457c9315fbe131840`. Its 9 file diffs run 58, 18, 15,
55, 42, 22, 22, 32 and 22 lines, 286 in all. That is under 440, so the greedy cut gives ONE part.

### ad19821a F275 R98 C5: record DECISION F275 D72

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC98 APPENDED after G4's readings, G5 and G6, and after the three worktrees were removed; deletion column ZERO |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10 says no gate runs after C6, and a handback cannot carry a reading of the commit that writes it; the REVIEWER measures this commit |

I read the `+/-` cells above from `git show --numstat` and compared each one against G8. C0a 287/0 = 287/0; C0b 131/117 = 131/117;
C1 7/8 = 7/8; C2 6/0 = 6/0; C3 2/0 = 2/0; C4 327/0 = 327/0; C5 12/0 = 12/0. All seven pairs are EQUAL. Every commit staged
exactly ONE path. The largest is C4 at 327 insertions, and 0 commits reach 500.

### SPEC O, as the overlay carries it (9 paths, in the flipped tree only)

| Path | What |
|---|---|
| `apps/cli/commands/contract_cmd.py` | O1: `_cmd_contract_inspect`, `_cmd_contract_check` and `_cmd_contract_set` each call `require_job_plan(job_id)`; each local import reads `require_job_plan, save_job_plan` |
| `apps/cli/commands/repo.py` | O1: `_cmd_commit_readiness` calls `require_job_plan(lookup_job_id(job_id_str))`; its import names `require_job_plan` |
| `apps/cli/commands/test_cmds.py` | O1: `_cmd_discover_commands` calls `require_job_plan(job_id)`; its import names `require_job_plan` |
| `packages/orchestration/orchestrator_loop.py` | O1: `open_mission_decisions`, `collect_milestone_evidence` and `escalate_repeated_refusal` call `require_job_plan(normalize_job_id(...))` with the same argument; imports `require_job_plan` and `require_job_plan, save_job_plan` |
| `packages/orchestration/real_test_execution.py` | O1: `resolve_allowed_command` and `list_test_runs` call `require_job_plan(normalize_job_id(job_id), ddir)`, and `get_test_run` calls `require_job_plan(normalize_job_id(str(jid)), ddir)`; imports `require_job_plan` and `list_job_plans, require_job_plan` |
| `packages/orchestration/repair_loop.py` | O1: `start_repair_loop_v0`'s first load calls `require_job_plan(job_id)`; the second `load_job_plan(job_id)` (the `reloaded` load) is unchanged; import `load_job_plan, require_job_plan, save_job_plan` |
| `packages/orchestration/watchdog.py` | O1: in `decide`, nested in `act_on_trips`, the call is `require_job_plan(normalize_job_id(link.job_id))`; `act_on_trips`'s import reads `require_job_plan, save_job_plan` |
| `tests/cli/runtime_helpers.py` | O2: `create_test_env` makes `job_dir = root / "jobs" / jid` with the same `mkdir(parents=True, exist_ok=True)`; the keys become `"job_id"`, `"job_title"`, `"status"` with values and places kept; `"user_prompt": ""`; it writes `job_dir / "job.json"` |
| `tests/cli/test_test_run_runtime.py` | O2: `_make_job_with_repo` and `test_no_traceback_on_missing_repo_dir` read `data_root / "jobs" / job_id / "job.json"` |

`.remedy-wt/r98w/spec_o.py` made every replacement. Each is an exact literal, confined to the span of the function it names, located
with `ast.walk`, and each count matched: 32 of 32 replacements read `count 1 (want 1)` (`.remedy-wt/r98w/spec_o.out`). Every function
name O1 and O2 give matched my own `ast` reading of the chained tree, so there is no name difference to declare.

## External actions

| Command | Outcome |
|---|---|
| `git push origin feature/f275-one-world-completion-part-three` after C3, after C4 and after C5 | exit 0 each: `ac17fd6e..967378bb`, `967378bb..159163c3`, `159163c3..ad19821a`. The push of C6 follows this commit, and its result is in the round report |
| `git worktree add --detach .remedy-wt/r98w/wt_EDIT 844a7f21`, then `… wt_CONTROL 844a7f21`, then `… wt_OVERLAY 844a7f21`. This was G4 setup, run after C3 and before the C4 commit, per constraint 10 | exit **0**, **0**, **0** |
| In each worktree: the transform, then `git add -A`, then each COMMITTED overlay in order: `f275-r90-overlay.md`; `f275-r91-overlay.md`; `f275-r92-overlay-1.md` … `-4.md`; `f275-r93-overlay-1.md`, `-2.md`; `f275-r94-overlay-1.md`, `-2.md`; `f275-r95-overlay-1.md` … `-4.md`; `f275-r96-overlay-1.md`; `f275-r97-overlay-1.md`. Each carrier got `git apply --check` then `git apply`, and `git add -A` ran once after each overlay's parts. Then SPEC O in EDIT only, and the C4 fence in OVERLAY only | exit 0 throughout (see G4) |
| One targeted pytest run in EDIT, after SPEC O and before the diff was taken (constraint 8 allows it) | see deviation 3 |
| In each worktree `git checkout HEAD -- .`, then `git worktree remove` for each, then `git worktree prune -v` | exit 0 throughout. This ran AFTER G6 and BEFORE C5, WITHOUT `--force`. After the restore, `git status --porcelain` printed `''` in each worktree. Only ignored entries were left: `.ruff_cache/` in EDIT; `.data/…`, `.pytest_cache/`, `.ruff_cache/`, `apps/ui/dist/` and `apps/ui/node_modules/` in CONTROL and OVERLAY. All three paths are gone, and `git worktree list` shows one row |
| `git archive` of `ef75e213` and `844a7f21`, extracted by `tarfile` into `.remedy-wt/r98w/gen/` (tree_base, tree_tip, tree_shift, tree_delete, each `git init -q` + `git add -A -f .`); `git archive` of `ac17fd6e` into `.remedy-wt/r98w/tree_base` (the G7 base lint) | exit 0; plain directories, never registered worktrees |
| `gh` / `remedy` | NOT RUN, not even a version query. No pull request, no branch created or deleted, no merge, no force-push, no history rewrite |

## Verification

Each gate ran through `.remedy-wt/r98w/run.py`. It saves the output to `.remedy-wt/r98w/<name>.out` and appends `PROCESS_EXIT=`
taken from the subprocess's own return code. Every figure the block states reproduced.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C5 | 0 (`g123`) | `cmp` of `.remedy-wt/r98_block.md` against the COMMITTED C0a blob: exit **0**, empty output, 24607 / 24607 bytes, sha256 `36de022748279459487fd04d5e6712ca950fddff2daaff2692545207b28931f6`. `.agent/last_block.md` at C0b equals the C0a blob and is unchanged at C5. Slices FOUND **4**, each MATCHING its BEGIN-marker sha256: PLAN98 2870 bytes / 48 lines, RECORD98 2790 / 6, SLIPS98 427 / 2, DEC98 2625 / 12. TOTAL **287**, slice lines 68, PROSE **219**, as constraint 9 states (caps 490 / 400). No line is a run of one repeated character. All 5 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C5 | 0 (`g123`) | `.agent/plan.md` at C1 is byte-identical to PLAN98 from the committed C0a blob: 2870 bytes, sha256 `68f437d7…`, **48** lines, one `## Goal`, one `## Next Steps`; unchanged at C5 |
| G3 the record | C5 | 0 (`g123`) | Pre-commit blobs read with `git show` at each commit's PARENT. C2 RECORD98: **1154699** (MATCHES) + 2790 = 1157489. C5 DEC98: **1302522** (MATCHES) + 2625 = 1305147. READER A is exact for both. READER B holds, in order, at N counted by the script as **3** and **6**. The negative controls flip `G`→`g` at offset 1154700 and `D`→`d` at 1302526, each inside the FIRST appended paragraph; BOTH readers REJECTED both. Deletion columns **0 / 0**. C3: the `.agent/prose_slips.md` pre-commit blob is **304316** (MATCHES) + 427 = 304743; post equals pre followed by exactly SLIPS98; deletion 0. Header pattern DERIVED from the pre-commit ledger: one shape, `^Gate: F\d+ R\d+ — `, matching **119 of 119** heads (596 paragraphs). RECORD98's header matches as `Gate: F275 R97 — `; no earlier head has that prefix, and there are 0 duplicate first lines |
| G4 trees, chain, carriers | setup after C3 and before C4; readings after the C4 commit `159163c3`, before C5 | 0 (`g4_build`), 0 (`c4_split`), 0 (`g4_check`) | **Inputs.** Pinned inputs MATCH: `r77_corrected.json` 120753 bytes `765b5ba9…`, owners 121095 `670c6e95…`, `r61_status.json` 1438 `a4c6cd63…`. Fences: rekey 5186 `f56394e9…`, owner 24253 `7be34374…`, input 10580 `c50da973…`, transform 29032 `075bc0dc…`. DELETE control line count 1. **Generator** exit **0**: **56** paths differ BASE/TIP; **2183** ruled sites recovered by scope at TIP, SHIFT and DELETE; UNRESOLVED **0**. Line-key CONTROL **1895 / 1886 / 1886**. Owner check at TIP: **1908** CONFIRMED, **275** REFUSED, **0** CONTRADICTED. **Transform** exit 0 in EDIT, CONTROL and OVERLAY, reading in each **2183** resolving / **0** not, **264** files, **6097** rewrites, **0** broken. **Chain.** All sixteen earlier carrier applications (r90, r91, r92 ×4, r93 ×2, r94 ×2, r95 ×4, r96 ×1, r97 ×1; the r97 patch `fb44133f…`) exited **0** for both `git apply --check` and `git apply` in each worktree, 96 of 96. `git diff --name-only` read 11, 12, 36, 13, 15, 32, 10 and 6 paths after overlays 1 to 8, and was empty after each `git add -A`. **(a)** The fence from the COMMITTED C4 blob has 39 prose lines before it, one `` ```diff `` line and one closing line, with nothing after but one newline. Part count **1**; line count **286**, ≤ 440. It equals EDIT's saved `git diff` stdout AND EDIT's live `git diff` (13426 bytes, `a048783f…`). In OVERLAY, `git apply --check` exit **0**, then `git apply` exit **0**. `git diff --name-only` there, against the staged index, lists **9** paths: MISSING `[]`, EXTRA `[]` against SPEC O's 9, each byte-identical to EDIT's. Cross-check: the tracked paths whose bytes differ between OVERLAY and CONTROL are the same 9. **(b)** `ast`, names matched exactly, 0 unparsable files under `packages/`, `apps/` and `tests/` in either tree. THE RULE with `load_job_plan` / `require_job_plan`: CONTROL **13 / 0**, OVERLAY **0 / 13** (reading of "the same statement list" per deviation 2). The 13 sites, as path, innermost function and line, are the same in both trees: `orchestrator_loop.py` `open_mission_decisions` 376, `collect_milestone_evidence` 1738, `escalate_repeated_refusal` 1930; `real_test_execution.py` `resolve_allowed_command` 229, `list_test_runs` 324, `get_test_run` 341; `repair_loop.py` `start_repair_loop_v0` 84; `watchdog.py` `decide` 522; `contract_cmd.py` `_cmd_contract_inspect` 25, `_cmd_contract_check` 64, `_cmd_contract_set` 131; `repo.py` `_cmd_commit_readiness` 174; `test_cmds.py` `_cmd_discover_commands` 106. Inside the three O2 functions: dict keys `id`/`name`/`state` CONTROL **3** (`create_test_env` lines 63, 64, 68), OVERLAY **0**; keys `job_id`/`job_title`/`status` **0** and **3**; f-strings whose last literal part ends in `.json` CONTROL **3** (`create_test_env` 73, `_make_job_with_repo` 89, `test_no_traceback_on_missing_repo_dir` 424), OVERLAY **0**. All MATCH. **(c)** `ruff check --output-format concise` over SPEC O's 9 paths, run from inside each tree: CONTROL exit **1** with **10** rows; OVERLAY exit **1** with **10** rows. All rows are `I001`: `contract_cmd.py` ×3, `repo.py` ×1, `test_cmds.py` ×1, `repair_loop.py` ×5, at the same line and column in both trees. As a multiset of `<path>: <code> <message>` with line and column dropped: added **0**, removed **0** |
| G5 full suite, CONTROL then OVERLAY | after the C4 commit, before C5 | 1 (`g5_CONTROL`), 1 (`g5_OVERLAY`), 0 (`g5_cmp`) | Each was its worktree's FIRST pytest run of any kind. `apps/ui/node_modules` and `apps/ui/dist` were ABSENT before each run and present after it. `PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`; `cwd` the worktree; `packages.orchestration.pingpong_job.__file__` inside the worktree in both. pytest exit 1 in both. CONTROL **`106 failed, 18329 passed, 29 skipped, 1 warning, 7 errors`** (1401.96s), **113** bad nodes: MATCHES the reviewer's. OVERLAY **`84 failed, 18351 passed, 29 skipped, 1 warning, 7 errors`** (1424.10s), **91** bad nodes, equal to the reviewer's dry run. **Bad only in OVERLAY: 0**, so constraint 11 required no re-run. Bad only in CONTROL (fixed): **22**. Section mapping: 0 header mismatches in both transcripts |
| G6 the probes | after G5, before C5, in OVERLAY | 0 (`g6`) | `__pycache__` purged before each of the four runs (0 directories each time); the module printed inside the worktree each time. **M1** in `apps/cli/commands/contract_cmd.py`. The bytes `require_job_plan(job_id)` count **1** inside `_cmd_contract_inspect` and **3** in the file, as stated. They become `__import__("packages.orchestration.pingpong_job", fromlist=["load_job_plan"]).load_job_plan(job_id)` inside that function only. Selection `tests/cli/test_contract_runtime.py`. Unmutated: exit 0, **`6 passed`**. Mutated: exit 1, **`2 failed, 4 passed`**. Bad only under M1: `TestContractInspectCLI::test_invalid_job_safe` and `TestContractInspectCLI::test_missing_job_safe`, both REQUIRED and both present. **M2** in `packages/orchestration/repair_loop.py`. The same bytes count **1** inside `start_repair_loop_v0` and **1** in the file, and change the same way. Selection `tests/orchestration/test_test_failure_repair.py`. Unmutated: exit 0, **`58 passed`**. Mutated: exit 1, **`2 failed, 56 passed`**. Bad only under M2: `TestRepairCLIHandlers::test_repair_start_job_not_found` and `TestRepairLoopV0::test_repair_loop_job_not_found`, both REQUIRED and both present. Nothing recovered under either mutation. After each probe the file was restored; its bytes equal the pre-mutation sha256 (`5ef88b75…`, `f482e47e…`) and EDIT's bytes |
| G7 tree, canary, lint, path set, open set | C5 | 0 (`g78`) | `git status --porcelain` exit 0 `''`. `git worktree list` **1** row. `git diff --name-only ac17fd6e ad19821a -- packages apps tests docs scripts` exit 0, empty. CANARY exit **0**, **42 passed**. `ruff check . --output-format concise` exit 1 at both ends: **26** rows at `ac17fd6e` (archive tree) and **26** at C5, multiset difference EMPTY both ways. `.py` files under `.agent/`: **0**. Changed paths `ac17fd6e`..C5: **7**, against the Bundle minus handoff: **7**; MISSING `[]`, EXTRA `[]`. Open set BY DISTINCT ID: **88** at `ac17fd6e` and **88** at C5 (112 − 24 each), membership IDENTICAL; `R-0809`, `R-0880` and `R-0883` OPEN at both |
| G8 insertion cap | C5 | 0 (`g78`) | C0a 287/0 1 path, C0b 131/117 1, C1 7/8 1, C2 6/0 1, C3 2/0 1, C4 327/0 1, C5 12/0 1; commits reaching 500 insertions **0** |

G5, THE FIXED NODES PER TEST FILE (22): `tests/cli/test_test_run_runtime.py` 15, `tests/cli/test_contract_runtime.py` 5,
`tests/orchestration/test_test_failure_repair.py` 2. The full node list is in `.remedy-wt/r98w/g5_cmp.out`.

STOP READINGS, per constraint 3: `.agent/STOP` was ABSENT both before C0a and before C6 (`test -e` exit 1, `ls -la` exit 2,
`os.path.exists` False). Transcripts: `.remedy-wt/r98w/stop_before_C0a.txt` and `.remedy-wt/r98w/stop_before_C6.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r98.md` | `cmp` exit 0 against `.remedy-wt/r98_block.md`, 24607 bytes, sha256 `36de022748279459487fd04d5e6712ca950fddff2daaff2692545207b28931f6` |
| PLAN98 | `.agent/plan.md` | byte-identical, 2870 bytes, sha256 `68f437d7db73c8782b87311ab1ab924739fbfd235b0d45d7744683984bdc1042` (the BEGIN marker's) |
| RECORD98 | `.agent/live_review.md` | exact suffix at C2 under readers A and B, 2790 bytes, sha256 `a765ca276968914d7aa88672dfc71ca08841a6a28f59850e675f70558260a99b` |
| SLIPS98 | `.agent/prose_slips.md` | post equals the 304316-byte pre-commit blob followed by exactly the slice, 427 bytes, sha256 `5967d10a4d592f571f0c9c17e241449bf5d9b6e3b728f0f66518f1e735e33b55` |
| DEC98 | `.agent/decisions.md` | exact suffix at C5 under readers A and B, 2625 bytes, sha256 `eb47782bc620227f9843ea7f6d96991d6d16265a24ef3040a570214aa2ff826d` |

Every slice was applied from the bytes of the COMMITTED C0a blob, and NO SLICE WAS EDITED. The C4 carrier is my own text, written from
SPEC C over my own SPEC O edit.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 round 97 verdict | done | |
| C3 round 97 prose slip | done | |
| C4 overlay carriers (SPEC C over SPEC O) | done | one carrier, 327 insertions; the whole 286-line diff fits one part |
| C5 DECISION F275 D72 | done | after G4's readings, G5 and G6, and after the worktrees were removed |
| C6 handback | done | this commit |
| SPEC O1 · O2 | done | 9 paths; THE RULE read as deviation 2 states |
| G4 · G5 · G6 | done | bad only in OVERLAY 0, so constraint 11 did not stop the round; both probes as ordered |
| G1 · G2 · G3 · G7 · G8 | done | exit 0 · 0, at C5 |

## Deviations & assumptions

1. **NO DEPARTURE FROM THE COMMIT SEQUENCE.** The commits are exactly the Bundle: C0a, C0b, C1, C2, C3, one C4 carrier (SPEC C's cut
   produced one part), C5, C6. `.agent/context.md` is not in the Change set and was not touched.
2. **HOW I READ "THE SAME STATEMENT LIST" IN THE RULE OF O1.** The Assign is a direct statement of the `try` body. Read literally,
   "the first later statement of the same statement list" would mean the statements after the Assign inside that `try` body. That
   reading does not give the 13 functions SPEC O1 names. In CONTROL it matches **10** other calls (`run_job_fulfill`,
   `create_snapshot_proof`, three in `test_execution_service.py`, `token_economy._inspect`, `_cmd_dashboard_project`,
   `_index_job_evidence`, `job_stop_cmd._load_job`, `_cmd_readiness_project`) and none of the named ones. I read the list as the one
   that holds the `try`, taking the statements after it. That reading gives exactly the 13 named calls, one in each named function. It
   also agrees with DEC98 ("read after that `try`") and PLAN98 ("read after that handler"). SPEC O and G4(b) use this reading.
   `.remedy-wt/r98w/g4_check.out` also prints the literal reading's counts for the record: 10 / 0 in CONTROL and 10 / 0 in OVERLAY.
   This is a wording gap in the block's SPEC prose, not in a slice, and I repaired nothing.
3. **EDIT RAN ONE TARGETED PYTEST RUN WHILE SPEC O WAS MADE.** Constraint 8 allows this, and it is not a gate reading. It ran after
   SPEC O and before the diff was taken, over `tests/cli/test_contract_runtime.py`, `tests/orchestration/test_test_failure_repair.py`
   and `tests/cli/test_test_run_runtime.py`: exit 0, `87 passed`. No full run was made in EDIT. Before the diff I also ran my
   G4(b)/(c) script with EDIT in OVERLAY's place (`.remedy-wt/r98w/g4_pre.out`). It read 13/0/3/0/3 and 0/13/0/3/0, with ruff added 0
   and removed 0. That step ran ruff and `ast` in CONTROL, not pytest, so G5's first-run condition still held.
4. **G4(c) EXITS 1 WHERE THE BLOCK SAID IT WOULD.** Ruff exits 1 in both trees with 10 rows each. That is a reported reading, not a
   red gate.
5. **THE WATCHDOG'S IMPORT.** The call sits in `decide`. As O1 orders, the import changed is the one in `act_on_trips`, and no import
   was added to `decide`.
6. **SCRATCH AND THE SHELL'S STARTING DIRECTORY.** This session's shell started with `.remedy-wt/r98` as its working directory, which
   is the reviewer's scratch path. My first two actions touched that path by accident. First, `git -C .remedy-wt/r98 status`, `log` and
   `branch`, which git resolves to the primary checkout and which read nothing from that directory. Second, one `Read` of the relative
   path `AGENTS.md`, which resolved to `.remedy-wt/r98/AGENTS.md` and returned "File does not exist", so nothing was read. After that,
   every command used absolute paths elsewhere, and nothing under `.remedy-wt/r90/` through `.remedy-wt/r98/` was opened. I read
   round 97's worker scratch (`.remedy-wt/r97w/`) for its scripts only, and ported them with counted replacements. All of this
   worker's scratch is under `.remedy-wt/r98w/`, uncommitted.

## Next

The reviewer re-runs the gates and issues the round 98 verdict.

Operator questions open: 1

After that, per `.agent/plan.md`, come more overlays, one residue group each, applied on top of these nine. In order: production
code that hands a `JobPlan` a `JobBudgets` model; the `mission` and `decision resolve --as-mission` commands finding no previous job;
the self-dogfood runtimes; the classic-shaped tests of routed handlers in `tests/test_data_paths.py`; and the classic runner under
`job resume`. Then the flip lands as a series of commits under the cap, then the classic store, then the closure sequence.
