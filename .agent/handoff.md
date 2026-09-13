# Handback — F275 round 94

## Session

`SESSION 32 of feature F275 · round 94 · rounds so far 94`

## Range

Review of `38b0a25a`..`HEAD`: the eight commits C0a, C0b, C1, C2, C3, two C4 carriers and C5, plus this handback commit C6.

## Commits

### ea1f37ba F275 R94 C0a: save the round 94 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r94.md` | +315 / -0 | the block copied with `shutil.copyfile`, byte-identical to `.remedy-wt/r94_block.md` at 28291 bytes |

### 967229a4 F275 R94 C0b: mirror the round 94 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +179 / -135 | written from the COMMITTED C0a blob, read back with `git show` |

### 16a1efa5 F275 R94 C1: make the plan current for round 94

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17 / -17 | slice PLAN94, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### 9a8685ba F275 R94 C2: book the round 93 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +8 / -0 | slice RECORD94 appended |

### d34deffd F275 R94 C3: append the round 93 prose slip

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +2 / -0 | slice SLIPS94 appended |

### df28bf6d · 52441e62 F275 R94 C4: the flip's fifth overlay, carriers 1 and 2 of 2

| Commit | Path | +/- | Reason |
|---|---|---|---|
| `df28bf6d` | `.agent/authored/f275-r94-overlay-1.md` | +391 / -0 | SPEC C part 1: 38 prose lines, then ONE ```` ```diff ```` fence holding 13 whole file diffs, 351 lines (`apps/cli/commands/context.py` through `tests/orchestration/test_mint_call_sites.py`); 19895 bytes, sha256 `a79084b3…f0a04519e0ab11c6` |
| `52441e62` | `.agent/authored/f275-r94-overlay-2.md` | +216 / -0 | part 2: 2 file diffs, 176 lines (`tests/orchestration/test_proposed_tasks.py`, `tests/test_data_paths.py`); 12982 bytes, sha256 `9d665340…a54938e7a94cf4352a205` |

EDIT's `git diff` is 527 lines, 27769 bytes, sha256 `f22c15ab6b67f390609f427e68b7752e15e3340892cc47bb9e91c092758b0284`. Its 15 file diffs run 24, 30, 39, 39, 32, 24, 36, 33, 14, 13, 22, 13, 32, 147 and 29 lines. They were packed in order, and a new part started only when the next file diff would push the part past 440 lines. Part 1 stopped at 351 because `test_proposed_tasks.py` (147) would make it 498.

### 5267d3ad F275 R94 C5: record DECISION F275 D68

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | slice DEC94 APPENDED after G4's readings, G5 and G6, and after the three worktrees were removed; deletion column ZERO |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10: no gate runs after C6, and a handback cannot carry a reading of the commit that writes it; the REVIEWER measures this commit |

I read the `+/-` cells above from `git show --numstat` and compared each one against G8. C0a 315/0 = 315/0; C0b 179/135 = 179/135;
C1 17/17 = 17/17; C2 8/0 = 8/0; C3 2/0 = 2/0; C4 part 1 391/0 = 391/0; part 2 216/0 = 216/0; C5 14/0 = 14/0. All eight pairs are
EQUAL. Every commit staged exactly ONE path. The largest is the part 1 carrier at 391 insertions, and 0 commits reach 500.

### SPEC O, as the overlay carries it (15 paths, in the flipped tree only; +/- read with `git apply --numstat` of the two extracted fences)

| Path | +/- in the overlay | What |
|---|---|---|
| `packages/orchestration/data_paths.py` | +8 / -2 | O1: `def mint_task_id() -> str:` after `mint_episode_id`, docstring naming a TASK no job file numbered, returning `uuid4().hex[:16]`; Public API line `mint_task_id() -> str` after `mint_episode_id`'s; the D2 comment reads "name five" and "the fifth kind" |
| `packages/orchestration/pingpong_job.py` | +9 / -5 | O2: the module-level import binds `mint_task_id`; `    task_id: str = field(default_factory=mint_task_id)` under a three-line comment (job file tasks numbered `T001`, `T002` by parse order; a task built by code mints its id, as the classic `Task` did); the import comment names TASKs (deviation 3) |
| `packages/orchestration/flight_plan.py` | +2 / -4 | O3: `acceptance="\n".join(pt.acceptance)` in `map_flight_plan_to_tasks`; `AcceptanceCheck` leaves the import |
| `packages/orchestration/mission_state.py` | +5 / -6 | O3: `build_verify_first_task` passes its sentence as `acceptance=`, `AcceptanceCheck` leaves its local import; O4: `planned.append(replace(task, inputs=inputs))` |
| `packages/orchestration/proposed_tasks.py` | +2 / -1 | O4: `TaskEntry(task_id=task_dict["id"], title=task_dict["description"], inputs=task_dict["inputs"], status=task_dict["status"])`, wrapped over two lines |
| `packages/orchestration/test_failure_artifact.py` | +2 / -2 | O5: `task_id=failure.task_id or None`; `from uuid import uuid4` |
| `packages/orchestration/escalation.py` | +7 / -6 | O5: `-> set[str]`; `known = {str(task.task_id) for task in getattr(job, "tasks", ()) or ()}`; `task_id = str(record.get("task_id") or "")`; `        if task_id and task_id in known:` under `# An id naming no task of this job blocks nothing.` (the `UUID` import stays, deviation 5) |
| `packages/orchestration/decision_inbox.py` | +5 / -9 | O5: seeds `{str(payload["task_id"])}` when the payload is a dict with a truthy `task_id`, else `set()`; `from uuid import UUID` deleted; the `build_decision_inbox` docstring says a task id that names no task gives 0 blocked |
| `apps/cli/commands/context.py` | +0 / -6 | O5: the `UUID(task_id)` refusal and `from uuid import UUID` deleted; the membership check stays |
| `apps/cli/commands/job_context_cmd.py` | +12 / -7 | O6: `_task_planned_id` begins, after its docstring, with the two ordered lines, returns `str(planned)` there and otherwise `str(getattr(task, "task_id", "") or "")`; docstring and comment say why the flight-plan block wins (deviation 3) |
| `packages/orchestration/test_execution_service.py` | +1 / -1 | O7: the `job show` guidance of `execute_test_run` reads `job.job_id` (deviation 4) |
| `tests/orchestration/test_flight_plan.py` | +1 / -1 | O3: `assert task.acceptance.splitlines() == [f"Thing {i + 1} done"]` |
| `tests/orchestration/test_mint_call_sites.py` | +8 / -2 | O8: docstring first line names the TASK kind; "THE THREE DATACLASS DEFAULTS"; `test_task_entry_task_id_default_is_the_mint_function_itself` after the RUN pin |
| `tests/test_data_paths.py` | +9 / -2 | O8: `_minters` also returns `mint_task_id`; `test_the_task_minter_is_a_fourth_distinct_function` after the three-names test |
| `tests/orchestration/test_proposed_tasks.py` | +16 / -16 | O8: 16 × `monkeypatch.setattr("packages.orchestration.storage._DATA_DIR", tmp_path / "jobs")` → `monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))`, counted 16 before the edit and 0 after |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r94w/wt_EDIT 844a7f21`, `… wt_CONTROL 844a7f21`, `… wt_OVERLAY 844a7f21` (G4 setup, after C3 and before the first C4 commit, per constraint 10) | exit **0**, **0**, **0** |
| in each worktree: the transform, `git add -A`, then overlay by overlay the COMMITTED `f275-r90-overlay.md`; `f275-r91-overlay.md`; `f275-r92-overlay-1.md` … `-4.md`; `f275-r93-overlay-1.md`, `-2.md`: `git apply --check`, `git apply` per carrier, `git add -A` after each overlay; after that SPEC O in EDIT only, and the two C4 fences in OVERLAY only | exit 0 throughout (see G4) |
| one full suite in EDIT after SPEC O, before the diff was taken (constraint 8 allows it) | see deviation 2 |
| `git checkout HEAD -- .` in each worktree, then `git worktree remove` for each, then `git worktree prune -v` | exit 0 throughout, AFTER G6 and BEFORE C5, WITHOUT `--force`. `git status --porcelain` printed `''` in each after the restore; only ignored `.data/…`, `.pytest_cache/`, `.ruff_cache/`, `apps/ui/dist/` and `apps/ui/node_modules/` were left. All three paths are gone and `git worktree list` shows one row |
| `git archive` of `ef75e213` and `844a7f21` extracted by `tarfile` into `.remedy-wt/r94w/gen/` (tree_base, tree_tip, tree_shift, tree_delete, each `git init -q` + `git add -A -f .`), and of `38b0a25a` into `.remedy-wt/r94w/tree_base` (G7 base lint) | exit 0; plain directories, never registered worktrees |
| `git push origin feature/f275-one-world-completion-part-three` | run after C6; its result is in the round report |
| `gh` / `remedy` | NOT RUN. No pull request, no branch created or deleted, no merge, no force-push, no history rewrite |

## Verification

Each gate ran through `.remedy-wt/r94w/run.py`. It saves the output to `.remedy-wt/r94w/<name>.out` and appends `PROCESS_EXIT=`,
taken from the subprocess's own return code. Every figure the block states reproduced.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C5 | 0 (`g123`) | `cmp` of `.remedy-wt/r94_block.md` against the COMMITTED C0a blob: exit **0**, empty output, 28291 / 28291 bytes, sha256 `92992f2a…c89f061`. `.agent/last_block.md` at C0b equals the C0a blob and is unchanged at C5. Slices FOUND **4**, each MATCHING its BEGIN-marker sha256: PLAN94 2947 bytes / 49 lines, RECORD94 3483 / 8, SLIPS94 551 / 2, DEC94 3673 / 14. TOTAL **315**, slice lines 73, PROSE **242**, as constraint 9 states. No line is a run of one repeated character. All 5 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C5 | 0 (`g123`) | `.agent/plan.md` at C1 is byte-identical to PLAN94 from the committed C0a blob: 2947 bytes, **49** lines, one `## Goal`, one `## Next Steps`; unchanged at C5 |
| G3 the record | C5 | 0 (`g123`) | Pre-commit blobs read with `git show` at each commit's PARENT. C2 RECORD94: **1142023** (MATCHES) + 3483 = 1145506. C5 DEC94: **1290732** (MATCHES) + 3673 = 1294405. READER A is exact for both. READER B holds, in order, at N counted by the script as **4** and **7**. Negative controls `G`→`g` at offset 1142024 and `D`→`d` at 1290736, each in the FIRST appended paragraph, were REJECTED by BOTH readers. Deletion columns **0 / 0**. C3: `.agent/prose_slips.md` pre-commit blob **301820** (MATCHES) + 551 = 302371; post equals pre followed by exactly SLIPS94; deletion 0. Header pattern DERIVED from the pre-commit ledger: one shape, `^Gate: F\d+ R\d+ — `, matching **115 of 115** heads (582 paragraphs). RECORD94's header matches as `Gate: F275 R93 — `; no earlier head has that prefix, and there are 0 duplicate first lines |
| G4 trees, chain, carriers | setup after C3 and before C4; readings after the last C4 `52441e62`, before C5 | 0 (`g4_build`), 0 (`c4_split`), 0 (`g4_check`) | Pinned inputs MATCH: `r77_corrected.json` 120753 bytes `765b5ba9…`, owners 121095 `670c6e95…`, `r61_status.json` 1438 `a4c6cd63…`. Fences: rekey 5186 `f56394e9…`, owner 24253 `7be34374…`, input 10580 `c50da973…`, transform 29032 `075bc0dc…`. Overlay patches from the committed carriers: r90 12756 `aa9c08fb…`, r91 17241 `eff93a17…`, r92 parts 13969 `6f95fd0f…`, 17159 `e40bf536…`, 20669 `173436cd…`, 6831 `55811ed3…`, r93 parts 20879 `16f5c2a0…`, 16551 `7942505b…`. DELETE control line count 1. Generator exit **0**: **56** paths differ BASE/TIP; **2183** ruled sites recovered by scope at TIP, SHIFT and DELETE, UNRESOLVED **0**; line-key CONTROL **1895 / 1886 / 1886**; owner check at TIP **1908** CONFIRMED, **275** REFUSED, **0** CONTRADICTED. Transform exit 0 in EDIT, CONTROL and OVERLAY, in each: **2183** resolving / **0** not, **264** files, **6097** rewrites, **0** broken. All eight earlier carrier applications: `git apply --check` exit **0** and `git apply` exit **0** in each worktree; `git diff --name-only` read 11, 12, 36 and 13 paths after overlays 1 to 4 and empty after each `git add -A`. (a) Fences from the COMMITTED C4 blobs (each blob holds one `` ```diff `` line and one closing line, with nothing after but one newline). Part count **2**; line counts **351, 176**, each ≤ 440. Joined in `<k>` order they equal EDIT's saved `git diff` stdout AND EDIT's live `git diff` (27769 bytes, `f22c15ab…`). In OVERLAY, parts 1–2 each `git apply --check` exit **0** then `git apply` exit **0**, in order. `git diff --name-only` there against the staged index lists **15** paths: MISSING `[]`, EXTRA `[]` against SPEC O's 15 (`apps/cli/commands/context.py`, `apps/cli/commands/job_context_cmd.py`, `packages/orchestration/data_paths.py`, `decision_inbox.py`, `escalation.py`, `flight_plan.py`, `mission_state.py`, `pingpong_job.py`, `proposed_tasks.py`, `test_execution_service.py`, `test_failure_artifact.py`, `tests/orchestration/test_flight_plan.py`, `test_mint_call_sites.py`, `test_proposed_tasks.py`, `tests/test_data_paths.py`), each byte-identical to EDIT's. Cross-check: the tracked paths whose bytes differ between OVERLAY and CONTROL are the same 15. (b) `ast`, names matched exactly except the `task_id` containment: `TaskEntry(...)` calls with keyword `acceptance_checks` under `packages/`, `apps/`, `tests/` CONTROL **2** (`flight_plan.py:523`, `mission_state.py:760`), OVERLAY **0**; one-argument `UUID(...)` calls whose argument's source text contains `task_id` under `packages/` and `apps/` **4** (`decision_inbox.py:71`, `escalation.py:165`, `test_failure_artifact.py:324`, `context.py:39`) and **0**; `TaskEntry.model_*` calls **1** (`proposed_tasks.py:668` `model_validate`) and **0**; `model_copy` calls in `mission_state.py` **1** (line 813) and **0**; `setattr` calls in `test_proposed_tasks.py` with first argument `"packages.orchestration.storage._DATA_DIR"` **16** and **0**. 0 unparsable files in either tree. All MATCH. `def test_` per changed test file (CONTROL / OVERLAY): `test_flight_plan.py` 30/30, `test_mint_call_sites.py` 4/5, `test_proposed_tasks.py` 97/97, `tests/test_data_paths.py` 63/64: OVERLAY equals CONTROL plus one in exactly the two ordered files. (c) `ruff check --output-format concise` over SPEC O's 15 paths from inside each tree: CONTROL exit **1**, **12** rows; OVERLAY exit **1**, **12** rows (I001 ×8, F401 ×1, F821 ×3 of `mint_job_id` in `tests/test_data_paths.py`, one I001 row in `mission_state.py` one line earlier in OVERLAY); as a multiset of `<path>: <code> <message>` with line and column dropped: added **0**, removed **0** |
| G5 full suite, CONTROL then OVERLAY | after the last C4, before C5 | 1 (`g5_CONTROL`), 1 (`g5_OVERLAY`), 0 (`g5_cmp`) | Each was its worktree's FIRST pytest run of any kind; `apps/ui/node_modules` and `apps/ui/dist` were ABSENT before each run and present after it. `PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`; `cwd` the worktree; `packages.orchestration.pingpong_job.__file__` inside the worktree in both. pytest exit 1 in both. CONTROL **`375 failed, 18034 passed, 29 skipped, 1 warning, 31 errors`** (1409.88s), **406** bad nodes: MATCHES. OVERLAY **`225 failed, 18186 passed, 29 skipped, 1 warning, 31 errors`** (1409.95s), **256** bad nodes. **Bad only in OVERLAY: 0**, so constraint 11 required no re-run. Bad only in CONTROL (fixed): **150**. Section mapping: 0 header mismatches in both transcripts. Collected outcomes 18469 and 18471: the two added tests, both passing |
| G6 the probes | after G5, before C5, in OVERLAY | 0 (`g6`) | `__pycache__` purged before each of the six runs (0 directories each time), the module printed inside the worktree each time. **M1** `packages/orchestration/pingpong_job.py`, `    task_id: str = field(default_factory=mint_task_id)` counted **1** → `    task_id: str = ""`, over `test_mint_call_sites.py` and `test_dag_schedule.py`: unmutated exit 0 **`40 passed`**; mutated exit 1 **`15 failed, 25 passed`**; bad only under M1 **15**: the pin `TestMintCallSites::test_task_entry_task_id_default_is_the_mint_function_itself` and 14 nodes of `test_dag_schedule.py`. **M2** `packages/orchestration/escalation.py`, `        if task_id and task_id in known:` counted **1** → `        if task_id:`, over `test_escalation.py`: unmutated exit 0 **`68 passed`**; mutated exit 1 **`1 failed, 67 passed`**; bad only under M2 exactly `tests/orchestration/test_escalation.py::TestAwaitingBranch::test_a_malformed_task_id_blocks_nothing`. **M3** `apps/cli/commands/job_context_cmd.py`, `    planned = _task_flight_inputs(task).get("planned_id")` counted **1** → `    planned = getattr(task, "task_id", "")`, over `tests/cli/test_job_context_cmd.py`: unmutated exit 1 **`3 failed, 9 passed`** (the reviewer's 3); mutated exit 1 **`6 failed, 6 passed`**; bad only under M3 **3**: `test_planned_id_and_task_uuid_prefix_reach_the_same_task`, `test_json_view_carries_the_same_paths_as_the_text_view`, `test_empty_files_hint_is_rendered_rather_than_treated_as_an_error` (`Error: no task matches --task 'T001'`). Nothing recovered under any mutation. After each, the file's bytes were restored, equal to the pre-mutation sha256 (`a8840ae6…`, `b5283c5d…`, `645e33bf…`) and to EDIT's bytes |
| G7 tree, canary, lint, path set, open set | C5 | 0 (`g78`) | `git status --porcelain` exit 0 `''`. `git worktree list` **1** row. `git diff --name-only 38b0a25a 5267d3ad -- packages apps tests docs scripts` exit 0, empty. CANARY exit **0**, **42 passed**. `ruff check . --output-format concise` exit 1 at both ends: **26** rows at `38b0a25a` (archive tree) and **26** at C5, multiset difference EMPTY both ways. `.py` files under `.agent/`: **0**. Changed paths `38b0a25a`..C5: **8**, against the Bundle minus handoff: **8**; MISSING `[]`, EXTRA `[]`. Open set BY DISTINCT ID: **88** at `38b0a25a` and **88** at C5 (112 − 24 each), membership IDENTICAL; `R-0809`, `R-0880` and `R-0883` OPEN at both |
| G8 insertion cap | C5 | 0 (`g78`) | C0a 315/0 1 path, C0b 179/135 1, C1 17/17 1, C2 8/0 1, C3 2/0 1, C4 391/0 1, C4 216/0 1, C5 14/0 1; commits reaching 500 insertions **0** |

G5, THE FIXED NODES PER TEST FILE (150): `tests/orchestration/test_escalation.py` 24, `test_mission_state.py` 21,
`test_worker_execution.py` 18, `test_dag_schedule.py` 14, `test_job_fulfillment.py` 14, `test_long_run_executor.py` 12,
`test_proposed_tasks.py` 5, `test_dod_gate.py` 4, `test_flight_plan.py` 3, `tests/cli/test_plan_approval.py` 3,
`tests/test_brain_smoke.py` 3, `tests/test_project_brain.py` 3; two each in `tests/cli/test_decision_answers.py`,
`tests/cli/test_propose_cli.py`, `tests/orchestration/test_job_digest.py`, `test_proof_chain.py`, `test_repair_loop_v1.py`,
`test_test_failure_repair.py`, `test_watchdog.py`, `tests/test_brain_detail.py` and `tests/test_workspace.py`; one each in
`tests/cli/test_job_context_cmd.py`, `tests/cli/test_repair_runtime.py`, `tests/cli/test_repair_v1_cli.py`,
`tests/orchestration/test_checkpoints.py`, `test_decision_inbox.py`, `test_do_run.py`, `tests/test_task_runner.py` and
`tests/ui_server/test_brain_view_model.py` (the `test_*` files without a directory sit under `tests/orchestration/`). The full node list
is in `.remedy-wt/r94w/g5_cmp.out`.

STOP READINGS, per constraint 3: `.agent/STOP` was ABSENT both before C0a and before C6 (`test -e` exit 1, `ls -la` exit 2,
`os.path.exists` False). Transcripts: `.remedy-wt/r94w/stop_before_C0a.txt` and `.remedy-wt/r94w/stop_before_C6.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r94.md` | `cmp` exit 0 against `.remedy-wt/r94_block.md`, 28291 bytes, sha256 `92992f2af94ee7fbc2f19b003c2d70667da9b0019e4e530e713a5ca52c89f061` |
| PLAN94 | `.agent/plan.md` | byte-identical, 2947 bytes, sha256 `3559a4f07543a9a91db0a99ee809eace696714f0c93912535bed21efc0d9ff4c` |
| RECORD94 | `.agent/live_review.md` | exact suffix at C2 under readers A and B, 3483 bytes, sha256 `9884df7c82c0df583a735dd556d635fea2e559f876945b3a1794a0dfd2d66c66` |
| SLIPS94 | `.agent/prose_slips.md` | post equals the 301820-byte pre-commit blob followed by exactly the slice, 551 bytes, sha256 `80503360af56105ca44d5cd4de10ee74b99aa7e552e25d977139a2f4c19168e7` |
| DEC94 | `.agent/decisions.md` | exact suffix at C5 under readers A and B, 3673 bytes, sha256 `5ed6ed9db09a2d10c99a88dc641b1935d37393553b42ffcebb5302ac27b49d90` |

Every slice was applied from the bytes of the COMMITTED C0a blob, and NO SLICE WAS EDITED. The two C4 carriers are my own text,
written from SPEC C over my own SPEC O edit.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 round 93 verdict | done | |
| C3 round 93 prose slip | done | |
| C4 overlay carriers (SPEC C over SPEC O) | done | two carriers, one commit each: 391 and 216 insertions |
| C5 DECISION F275 D68 | done | after G4's readings, G5 and G6, and after the worktrees were removed |
| C6 handback | done | this commit |
| SPEC O1 · O2 · O3 · O4 · O5 · O6 · O7 · O8 | done | wording beyond the ordered bytes declared in deviation 3 |
| G4 · G5 · G6 | done | bad only in OVERLAY 0, so constraint 11 did not stop the round; every probe as ordered |
| G1 · G2 · G3 · G7 · G8 | done | exit 0 · 0, at C5 |

## Deviations & assumptions

1. **STAGING PER OVERLAY, NOT PER CARRIER.** Constraint 8 orders `git add -A` after each overlay. My build script applies every carrier
   of one overlay in order and stages once after the overlay's last carrier: after r90, after r91, after r92 part 4 and after r93
   part 2. Round 93's worker staged after each carrier. The staged tree is the same either way. Every `git apply --check` and
   `git apply` exited 0.
2. **EDIT RAN ONE FULL SUITE WHILE SPEC O WAS MADE.** Constraint 8 allows this; the readings are not gate readings. After SPEC O and
   before the diff was taken, EDIT's full suite read `225 failed, 18186 passed, 29 skipped, 1 warning, 31 errors`, 256 bad nodes.
   Against round 93's committed OVERLAY bad-node list (406), which is this round's CONTROL chain, that is 150 fixed and 0 newly bad. I did
   not run a suite in EDIT before SPEC O. EDIT's `git diff --name-only` then listed exactly SPEC O's 15 paths. Ruff also ran in CONTROL
   and EDIT before C4 as a preview (12 rows each, multiset equal). Ruff is not pytest, so G5's first-pytest-run condition still held
   in CONTROL and OVERLAY.
3. **WORDING BEYOND THE ORDERED BYTES.** Every triple-backtick line of SPEC O is byte for byte. Prose I wrote: the Public API comment
   `# a task id no job file numbered`; `mint_task_id`'s docstring; the `pingpong_job.py` import comment, which now names JOBs, TASKs
   and EPISODEs and the default_factory of JobPlan and of TaskEntry (it named only JOBs, EPISODEs and JobPlan's default before); the
   three-line comment above O2's field; the escalation comment; `_task_planned_id`'s two-paragraph docstring and three-line comment;
   the two new tests' docstrings. For O6 I read "the body begins with exactly the two lines" as the first two statements after the
   docstring, because O6 also orders a docstring; the comment sits inside the `if planned:` branch. O4's `TaskEntry(...)` call is
   wrapped over two lines at the `status=` keyword.
4. **O7 READ NARROWLY.** In `execute_test_run`, only the `job show` guidance line read `job.id`, and it now reads `job.job_id`. Five other
   guidance lines in the same function still read `job.id`: `attach-repo` at line 633, `contract inspect` at 644, `test discover` at 766
   and 773, and `contract set` at 789 (CONTROL numbering). SPEC O7 names only the `job show` guidance, so I did not touch them. This is
   an observation for the planner, not a measured defect.
5. **LEFT UNTOUCHED, OUTSIDE SPEC O.** `escalation.py` keeps `from uuid import UUID`, because `_next_decision_id` still calls
   `UUID(task_str)`; SPEC O5 does not order it out. `proposed_tasks.materialize_approved_task` still mints `str(uuid4())` for the task
   id, and its docstring still names `Task.model_validate()`; SPEC O4 edits only `do_materialize`.
6. **G4(c) AND G6 M3 EXIT 1 WHERE THE BLOCK SAID THEY WOULD.** Ruff exits 1 in both trees with 12 rows each. M3's unmutated run
   exits 1 with the reviewer's 3 failures. These are reported readings, not red gates.
7. **NO OTHER DEVIATION.** The commit sequence is exactly the Bundle. `.agent/context.md` is not in the Change set and was not touched.
   I did not open the reviewer's `.remedy-wt/r90/` through `.remedy-wt/r94/`. I read round 92's and round 93's worker scratch
   (`.remedy-wt/r92w/`, `.remedy-wt/r93w/`) for their scripts and round 93's G5 bad-node list only. All of this worker's scratch is under
   `.remedy-wt/r94w/`, uncommitted.

## Next

The reviewer re-runs the gates and issues the round 94 verdict.

Operator questions open: 1

After that, per `.agent/plan.md`: more overlays, one residue group each, applied on top of these five. The next are tests that still
redirect the classic store's `_DATA_DIR` and handlers resolving a minted job id no store holds. Then the flip lands as a series of
commits under the cap, then the classic store, then the closure sequence.
