# Handback — F275 round 96

## Session

`SESSION 32 of feature F275 · round 96 · rounds so far 96`

## Range

Review of `0fe76bb9`..`HEAD`: seven commits (C0a, C0b, C1, C2, C3, one C4 carrier, C5), plus this handback commit C6.

## Commits

### 73f1e642 F275 R96 C0a: save the round 96 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r96.md` | +292 / -0 | the block copied with `shutil.copyfile`; `cmp` against `.remedy-wt/r96_block.md` is byte-identical at 25466 bytes |

### 4cbb07db F275 R96 C0b: mirror the round 96 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +146 / -153 | written from the COMMITTED C0a blob, read back with `git show` |

### d70f733a F275 R96 C1: make the plan current for round 96

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +13 / -12 | slice PLAN96, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### ec2ceed1 F275 R96 C2: book the round 95 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6 / -0 | slice RECORD96 appended |

### 43965f42 F275 R96 C3: append the round 95 prose slip

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +2 / -0 | slice SLIPS96 appended |

### 1e1d4824 F275 R96 C4: commit the flip's seventh overlay, carrier 1 of 1

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r96-overlay-1.md` | +363 / -0 | SPEC C part 1 of 1: 36 prose lines, then ONE ```` ```diff ```` fence of all 10 file diffs, 325 lines (`apps/cli/commands/job.py` through `tests/test_grouped_cli.py`), then the closing line; 17263 bytes, sha256 `c65e9e5c686a6d1f2198a328d942b62190e4a5eebfe8d663442cc8f428cc4854` |

EDIT's `git diff` is 325 lines, 14780 bytes, sha256 `afa48881e0a541c44afaebba89106250c65d318c9313db463139bc00ae574466`. Its 10 file diffs run 23, 13, 24, 39, 36, 84, 34, 28,
28 and 16 lines, 325 in all. That is under 440, so the greedy cut gives ONE part.

### 7ba2b46f F275 R96 C5: record DECISION F275 D70

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | slice DEC96 APPENDED after G4's readings, G5 and G6, and after the three worktrees were removed; deletion column ZERO |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10 says no gate runs after C6, and a handback cannot carry a reading of the commit that writes it; the REVIEWER measures this commit |

I read the `+/-` cells above from `git show --numstat` and compared each one against G8. C0a 292/0 = 292/0; C0b 146/153 = 146/153;
C1 13/12 = 13/12; C2 6/0 = 6/0; C3 2/0 = 2/0; C4 363/0 = 363/0; C5 14/0 = 14/0. All seven pairs are EQUAL. Every commit staged
exactly ONE path. The largest is the C4 carrier at 363 insertions, and 0 commits reach 500.

### SPEC O, as the overlay carries it (10 paths, in the flipped tree only; +/- read with `git apply --numstat` of EDIT's saved diff)

| Path | +/- in the overlay | What |
|---|---|---|
| `apps/cli/commands/job.py` | +5 / -1 | O1: `_cmd_show_job` prints `json.dumps(_export_job(job), indent=2)`, with `import json` and `from packages.orchestration.pingpong_job import _export_job` inside the function |
| `packages/orchestration/job_fulfillment.py` | +1 / -1 | O2: `"created_at": record.created_at.isoformat(),` in `export_job_fulfillment_json` |
| `tests/cli/test_context_inspect_runtime.py` | +2 / -4 | O5: `_create_temp_job` calls `save_job_plan(job, tmp_path)`; `save_job_plan` joins the module's existing `pingpong_job` import |
| `tests/cli/test_golden_path.py` | +6 / -6 | O4: the old record's keys are `job_id` `"0000000000000001"` and `job_title`, it is loaded with `_import_job(json.loads(old_json))` and the test asserts `job.mission == ""`; `test_job_show_accepts_short_id` asserts `data["job_id"]` |
| `tests/orchestration/test_fence_e2e.py` | +6 / -6 | O3: two round trips go through `_import_job(json.loads(json.dumps(_export_job(job))))`; O4: `test_backward_compatible_load` loads `_import_job({"job_id": uuid4().hex[:16], "job_title": "old-job"})` |
| `tests/orchestration/test_job_budgets.py` | +23 / -15 | O4: the old fixture goes through `_import_job`; the three budget tests pass `JobBudgets(...).model_dump(mode="json")` and use `_export_job` and `_import_job`, the strict-types test through `json.dumps`/`json.loads`, and read budget values by key; module-level `import json` (deviation 2) |
| `tests/orchestration/test_long_run_executor.py` | +6 / -3 | O3: `_normalize` reads `json.loads(json.dumps(_export_job(job)))`; the two copies are `copy.deepcopy(job)`; module-level `import copy` |
| `tests/orchestration/test_loop_run.py` | +4 / -4 | O6: four `created_at=datetime(...).isoformat()` |
| `tests/orchestration/test_run_contract.py` | +4 / -6 | O3: both round trips go through `_import_job(json.loads(json.dumps(_export_job(job))))`; the local `JobPlan` import is replaced by `_export_job, _import_job` |
| `tests/test_grouped_cli.py` | +2 / -2 | O6: `created_at=(datetime.now(timezone.utc) - timedelta(days=1)).isoformat()` and `created_at=datetime.now(timezone.utc).isoformat()` |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r96w/wt_EDIT 844a7f21`, `… wt_CONTROL 844a7f21`, `… wt_OVERLAY 844a7f21` (G4 setup, after C3 and before the C4 commit, per constraint 10) | exit **0**, **0**, **0** |
| in each worktree: the transform, `git add -A`, then overlay by overlay the COMMITTED `f275-r90-overlay.md`; `f275-r91-overlay.md`; `f275-r92-overlay-1.md` … `-4.md`; `f275-r93-overlay-1.md`, `-2.md`; `f275-r94-overlay-1.md`, `-2.md`; `f275-r95-overlay-1.md` … `-4.md`: `git apply --check` and `git apply` per carrier, `git add -A` once after each overlay's parts; then SPEC O in EDIT only, and the C4 fence in OVERLAY only | exit 0 throughout (see G4) |
| two pytest runs in EDIT after SPEC O and before the diff was taken (constraint 8 allows them) | see deviation 3 |
| `git checkout HEAD -- .` in each worktree, then `git worktree remove` for each, then `git worktree prune -v` | exit 0 throughout, AFTER G6 and BEFORE C5, WITHOUT `--force`. `git status --porcelain` printed `''` in each after the restore; only the ignored `.data/…`, `.pytest_cache/`, `.ruff_cache/`, `apps/ui/dist/` and `apps/ui/node_modules/` were left. All three paths are gone, and `git worktree list` shows one row |
| `git archive` of `ef75e213` and `844a7f21` extracted by `tarfile` into `.remedy-wt/r96w/gen/` (tree_base, tree_tip, tree_shift, tree_delete, each `git init -q` + `git add -A -f .`), and of `0fe76bb9` into `.remedy-wt/r96w/tree_base` (G7 base lint) | exit 0; plain directories, never registered worktrees |
| `git push origin feature/f275-one-world-completion-part-three` | runs after C6; its result is in the round report |
| `gh` / `remedy` | NOT RUN. I issued one `gh --version` call early on, and the permission layer rejected it before it executed (deviation 6). No pull request, no branch created or deleted, no merge, no force-push, no history rewrite |

## Verification

Each gate ran through `.remedy-wt/r96w/run.py`, which saves the output to `.remedy-wt/r96w/<name>.out` and appends `PROCESS_EXIT=`
from the subprocess's own return code. Every figure the block states reproduced.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C5 | 0 (`g123`) | `cmp` of `.remedy-wt/r96_block.md` against the COMMITTED C0a blob: exit **0**, empty output, 25466 / 25466 bytes, sha256 `9f3a14dbc95d990fe993d93e131d829389107cd96dd1a6b1ae57598577389b4e`. `.agent/last_block.md` at C0b equals the C0a blob and is unchanged at C5. Slices FOUND **4**, each MATCHING its BEGIN-marker sha256: PLAN96 2954 bytes / 49 lines, RECORD96 2937 / 6, SLIPS96 559 / 2, DEC96 3042 / 14. TOTAL **292**, slice lines 71, PROSE **221**, as constraint 9 states (caps 490 / 400). No line is a run of one repeated character. All 5 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C5 | 0 (`g123`) | `.agent/plan.md` at C1 is byte-identical to PLAN96 from the committed C0a blob: 2954 bytes, **49** lines, one `## Goal`, one `## Next Steps`; unchanged at C5 |
| G3 the record | C5 | 0 (`g123`) | Pre-commit blobs read with `git show` at each commit's PARENT. C2 RECORD96: **1148938** (MATCHES) + 2937 = 1151875. C5 DEC96: **1297335** (MATCHES) + 3042 = 1300377. READER A is exact for both. READER B holds, in order, at N counted by the script as **3** and **7**. Negative controls `G`→`g` at offset 1148939 and `D`→`d` at 1297339, each in the FIRST appended paragraph, were REJECTED by BOTH readers. Deletion columns **0 / 0**. C3: the `.agent/prose_slips.md` pre-commit blob is **303243** (MATCHES) + 559 = 303802; post equals pre followed by exactly SLIPS96; deletion 0. Header pattern DERIVED from the pre-commit ledger: one shape, `^Gate: F\d+ R\d+ — `, matching **117 of 117** heads (590 paragraphs). RECORD96's header matches as `Gate: F275 R95 — `; no earlier head has that prefix, and there are 0 duplicate first lines |
| G4 trees, chain, carriers | setup after C3 and before C4; readings after the C4 commit `1e1d4824`, before C5 | 0 (`g4_build`), 0 (`c4_split`), 0 (`g4_check`) | Pinned inputs MATCH: `r77_corrected.json` 120753 bytes `765b5ba9…`, owners 121095 `670c6e95…`, `r61_status.json` 1438 `a4c6cd63…`. Fences: rekey 5186 `f56394e9…`, owner 24253 `7be34374…`, input 10580 `c50da973…`, transform 29032 `075bc0dc…`. DELETE control line count 1. Generator exit **0**: **56** paths differ BASE/TIP; **2183** ruled sites recovered by scope at TIP, SHIFT and DELETE, UNRESOLVED **0**; line-key CONTROL **1895 / 1886 / 1886**; owner check at TIP **1908** CONFIRMED, **275** REFUSED, **0** CONTRADICTED. Transform exit 0 in EDIT, CONTROL and OVERLAY, in each: **2183** resolving / **0** not, **264** files, **6097** rewrites, **0** broken. All fourteen earlier carrier applications (r90, r91, r92 ×4, r93 ×2, r94 ×2, r95 ×4; the r95 patches `c6023801…`, `13140f64…`, `73a45df8…`, `885d839e…`): `git apply --check` exit **0** and `git apply` exit **0** in each worktree (84 of 84). `git diff --name-only` read 11, 12, 36, 13, 15 and 32 paths after overlays 1 to 6, and was empty after each `git add -A`. (a) Fence from the COMMITTED C4 blob: 36 prose lines, one `` ```diff `` line and one closing line, with nothing after but one newline. Part count **1**; line count **325**, ≤ 440. It equals EDIT's saved `git diff` stdout AND EDIT's live `git diff` (14780 bytes, `afa48881…`). In OVERLAY, `git apply --check` exit **0**, then `git apply` exit **0**. `git diff --name-only` there, against the staged index, lists **10** paths: MISSING `[]`, EXTRA `[]` against SPEC O's 10, each byte-identical to EDIT's. Cross-check: the tracked paths whose bytes differ between OVERLAY and CONTROL are the same 10. (b) `ast`, names matched exactly, 0 unparsable files under `packages/`, `apps/` and `tests/` in either tree. Model calls off `JobPlan`: CONTROL **9** (`test_fence_e2e.py` 3, `test_job_budgets.py` 3, `test_run_contract.py` 2, `test_golden_path.py` 1), OVERLAY **0**. `model_dump`/`model_dump_json`/`model_copy` off `job` under `apps/` and `tests/`: CONTROL **12** (`test_job_budgets.py` 3, `test_long_run_executor.py` 3, `test_fence_e2e.py` 2, `test_run_contract.py` 2, `job.py` 1, `test_context_inspect_runtime.py` 1), OVERLAY **0**. `created_at` datetime keywords of `JobPlan`/`_stored_job`: CONTROL **6** (`test_loop_run.py` 4, `test_grouped_cli.py` 2), OVERLAY **0**. `def test_` per changed test file, CONTROL / OVERLAY, EQUAL in all 8: 10/10, 42/42, 107/107, 135/135, 76/76, 23/23, 88/88, 69/69. All MATCH. (c) `ruff check --output-format concise` over SPEC O's 10 paths from inside each tree: CONTROL exit **1**, **9** rows; OVERLAY exit **1**, **9** rows (I001 ×8, F401 ×1 in `tests/test_grouped_cli.py`). Two I001 rows in `test_long_run_executor.py` moved by 3 lines. As a multiset of `<path>: <code> <message>` with line and column dropped: added **0**, removed **0** |
| G5 full suite, CONTROL then OVERLAY | after the C4 commit, before C5 | 1 (`g5_CONTROL`), 1 (`g5_OVERLAY`), 0 (`g5_cmp`) | Each was its worktree's FIRST pytest run of any kind; `apps/ui/node_modules` and `apps/ui/dist` were ABSENT before each run and present after it. `PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` removed; `PYTHONDONTWRITEBYTECODE=1`; `cwd` the worktree; `packages.orchestration.pingpong_job.__file__` inside the worktree in both. pytest exit 1 in both. CONTROL **`150 failed, 18261 passed, 29 skipped, 1 warning, 31 errors`** (1383.46s), **181** bad nodes: MATCHES. OVERLAY **`118 failed, 18293 passed, 29 skipped, 1 warning, 31 errors`** (1429.66s), **149** bad nodes. **Bad only in OVERLAY: 0**, so constraint 11 required no re-run. Bad only in CONTROL (fixed): **32**. Section mapping: 0 header mismatches in both transcripts |
| G6 the probes | after G5, before C5, in OVERLAY | 0 (`g6`) | `__pycache__` purged before each of the four runs (0 directories each time); the module printed inside the worktree each time. **M1** `apps/cli/commands/job.py`: the line `    print(json.dumps(_export_job(job), indent=2))` counts **1** in the file and becomes `    print(job.model_dump_json(indent=2))`, over `tests/cli/test_golden_path.py -k "job_show or intake_persisted or llm_intake or accepts_short_id"`. Unmutated: exit 0, **`5 passed, 37 deselected`**. Mutated: exit 1, **`4 failed, 1 passed, 37 deselected`**. Bad only under M1: `TestShortIdResolution::test_job_show_accepts_short_id` (REQUIRED, present), `TestDoMission::test_intake_persisted_on_job`, `TestDoMission::test_job_show_silent_for_legacy_job`, `TestLLMIntakeWiring::test_fake_provider_stores_llm_intake_with_evidence`. **M2** `packages/orchestration/job_fulfillment.py`: the line `        "created_at": record.created_at.isoformat(),` counts **1** in the file and becomes `        "created_at": record.created_at,`, over `tests/orchestration/test_job_fulfillment.py`. Unmutated: exit 1, **`1 failed, 104 passed`** (`TestJobFulfillFixturePass::test_a_pingpong_job_id_reaches_the_store_instead_of_a_uuid_parse`). Mutated: exit 1, **`3 failed, 102 passed`**. Bad only under M2: exactly `TestFulfillmentModel::test_record_export_no_secrets` and `TestJobReportAfterFulfilled::test_report_shows_completed`, both REQUIRED. The other node was bad in both runs, as the reviewer's dry run read. Nothing recovered under either mutation. After each, the file was restored and its bytes equal the pre-mutation sha256 (`1dd130f1…`, `b718fe5a…`) and EDIT's bytes |
| G7 tree, canary, lint, path set, open set | C5 | 0 (`g78`) | `git status --porcelain` exit 0 `''`. `git worktree list` **1** row. `git diff --name-only 0fe76bb9 7ba2b46f -- packages apps tests docs scripts` exit 0, empty. CANARY exit **0**, **42 passed**. `ruff check . --output-format concise` exit 1 at both ends: **26** rows at `0fe76bb9` (archive tree) and **26** at C5, multiset difference EMPTY both ways. `.py` files under `.agent/`: **0**. Changed paths `0fe76bb9`..C5: **7**, against the Bundle minus handoff: **7**; MISSING `[]`, EXTRA `[]`. Open set BY DISTINCT ID: **88** at `0fe76bb9` and **88** at C5 (112 − 24 each), membership IDENTICAL; `R-0809`, `R-0880` and `R-0883` OPEN at both |
| G8 insertion cap | C5 | 0 (`g78`) | C0a 292/0 1 path, C0b 146/153 1, C1 13/12 1, C2 6/0 1, C3 2/0 1, C4 363/0 1, C5 14/0 1; commits reaching 500 insertions **0** |

G5, THE FIXED NODES PER TEST FILE (32): `tests/cli/test_context_inspect_runtime.py` 10, `tests/cli/test_golden_path.py` 5,
`tests/orchestration/test_job_budgets.py` 4, `tests/orchestration/test_fence_e2e.py` 3, and 2 each in `tests/cli/test_plan_approval.py`,
`tests/orchestration/test_job_fulfillment.py`, `tests/orchestration/test_loop_run.py` and `tests/orchestration/test_run_contract.py`.
One each in `tests/orchestration/test_long_run_executor.py` and `tests/test_grouped_cli.py`. The two `test_plan_approval.py` nodes
(`TestAutoApproval::test_yes_auto_approves`, `TestFlightPlanLabel::test_llm_plan_stores_pending_approval`) sit in a file SPEC O does
not touch, so O1's `job show` output reaches them. The full node list is in `.remedy-wt/r96w/g5_cmp.out`.

STOP READINGS, per constraint 3: `.agent/STOP` was ABSENT both before C0a and before C6 (`test -e` exit 1, `ls -la` exit 2,
`os.path.exists` False). Transcripts: `.remedy-wt/r96w/stop_before_C0a.txt` and `.remedy-wt/r96w/stop_before_C6.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r96.md` | `cmp` exit 0 against `.remedy-wt/r96_block.md`, 25466 bytes, sha256 `9f3a14dbc95d990fe993d93e131d829389107cd96dd1a6b1ae57598577389b4e` |
| PLAN96 | `.agent/plan.md` | byte-identical, 2954 bytes, sha256 `0e6bb90599e342af4a08395adb9ec3cd33de102b5559d7f87fcf99f9f924abfe` (the BEGIN marker's) |
| RECORD96 | `.agent/live_review.md` | exact suffix at C2 under readers A and B, 2937 bytes, sha256 `497418d38a6e43197e48bcef297c3103f8dd3c6c19f2f89449c095a428281fea` |
| SLIPS96 | `.agent/prose_slips.md` | post equals the 303243-byte pre-commit blob followed by exactly the slice, 559 bytes, sha256 `7e50e965e6e5b7f1886d9605c10b2445788f4a996a71c9f48a9af1a7c7932b92` |
| DEC96 | `.agent/decisions.md` | exact suffix at C5 under readers A and B, 3042 bytes, sha256 `a3f87974437147aa4fc96079cdf5eb943029dae3523c97f8ac73b9a4b783ed7d` |

Every slice was applied from the bytes of the COMMITTED C0a blob, and NO SLICE WAS EDITED. The C4 carrier is my own text, written from
SPEC C over my own SPEC O edit.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 round 95 verdict | done | |
| C3 round 95 prose slip | done | |
| C4 overlay carriers (SPEC C over SPEC O) | done | one carrier, 363 insertions; the whole 325-line diff fits one part |
| C5 DECISION F275 D70 | done | after G4's readings, G5 and G6, and after the worktrees were removed |
| C6 handback | done | this commit |
| SPEC O1 · O2 · O3 · O4 · O5 · O6 | done | 10 paths; how two phrases were read is in deviations 1 and 2 |
| G4 · G5 · G6 | done | bad only in OVERLAY 0, so constraint 11 did not stop the round; both probes as ordered |
| G1 · G2 · G3 · G7 · G8 | done | exit 0 · 0, at C5 |

## Deviations & assumptions

1. **NO DEPARTURE FROM THE COMMIT SEQUENCE.** The commits are exactly the Bundle: C0a, C0b, C1, C2, C3, one C4 carrier (SPEC C's cut
   produced one part), C5, C6. `.agent/context.md` is not in the Change set and was not touched.
2. **HOW O4's BUDGET SENTENCE WAS READ.** O4 says the three budget tests "export with `_export_job`, restore with `_import_job` — the
   last of the three through `json.dumps` and `json.loads` — and read each budget value by key". I read that as applying to all
   three. So `test_job_with_budgets_serializes` also restores the exported dict with `_import_job` and reads `max_total_tokens` and
   `deadline` by key from the restored record, in addition to its two original key reads of the exported dict. That is two more
   assertions in an existing test; no test is added. The `json.dumps`/`json.loads` that the strict-types test needs come from a
   module-level `import json`, and `copy.deepcopy` in `test_long_run_executor.py` from a module-level `import copy`. `_cmd_show_job`
   imports `json` locally, beside `_export_job`, following the local-`json`-import pattern of the neighbouring handlers. SPEC O
   places only `_export_job` and `_import_job`, and G4(c) shows the ruff multiset unchanged.
3. **EDIT RAN TWO PYTEST RUNS WHILE SPEC O WAS MADE.** Constraint 8 allows this, and neither is a gate reading. Both came after SPEC O
   and before the diff was taken. First, the eight changed test files plus `tests/orchestration/test_job_fulfillment.py`:
   `4 failed, 1002 passed`, and all 4 nodes were bad in round 95's committed OVERLAY list. Second, the full suite:
   `118 failed, 18293 passed, 29 skipped, 1 warning, 31 errors`, 149 bad nodes. Against round 95's committed OVERLAY bad-node list
   (181), which is this round's CONTROL chain, that is 32 fixed and 0 newly bad. EDIT's `git diff --name-only` then listed exactly
   SPEC O's 10 paths. Before the diff I also ran my G4(b)/(c) script with EDIT in OVERLAY's place (`.remedy-wt/r96w/g4_pre.out`), and
   it read 9/12/6 and 0/0/0 with ruff added 0 and removed 0. That ran ruff in CONTROL, not pytest, so G5's first-run condition held.
4. **G4(c) EXITS 1 WHERE THE BLOCK SAID IT WOULD.** Ruff exits 1 in both trees with 9 rows each. That is a reported reading, not a red
   gate.
5. **CARRIER PROSE FOR ONE PART.** The carrier names itself "part 1 of 1". It keeps SPEC C's `<k>`-order instructions even though
   there is only one part.
6. **ONE REJECTED `gh` CALL.** Early in the session I issued `gh --version` while checking the environment. The permission layer
   rejected it ("This command requires approval"), so it never ran. Constraint 7 forbids `gh`, and no other `gh` or `remedy` command
   was issued.
7. **SCRATCH.** I did not open the reviewer's `.remedy-wt/r90/` through `.remedy-wt/r96/`. This session's shell started with
   `.remedy-wt/r94` as its working directory, but every command used absolute paths elsewhere. I read round 95's worker scratch
   (`.remedy-wt/r95w/`) for its scripts and its G5 OVERLAY bad-node list only. All of this worker's scratch is under
   `.remedy-wt/r96w/`, uncommitted.

## Next

The reviewer re-runs the gates and issues the round 96 verdict.

Operator questions open: 1

After that, per `.agent/plan.md`, come more overlays, one residue group each, applied on top of these seven. In order: production
code that hands a `JobPlan` a `JobBudgets` model; the mission end-to-end fixture and `mission continue`; command-line tests whose job
the flipped store does not find; the classic-shaped tests of routed handlers in `tests/test_data_paths.py`; and the classic runner
under `job resume`. Then the flip lands as a series of commits under the cap, then the classic store, then the closure sequence.
