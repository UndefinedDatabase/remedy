# Handback — F275 round 88

## Session

`SESSION 30 of feature F275 · round 88 · rounds so far 88`

Context self-assessment: this worker wrote one production function, one mechanical fifteen-module edit and two
test additions, ran the scoped suite once, one mutation worktree of 21 selection runs, and the committed residue
instrument once over the two pinned transcripts. Nothing about the session boundary is forced by this round.

## Range

Review of `058bfa2d`..`HEAD` (the ten commits C0a–C8 plus this handback commit C9).

## Commits

### 94b9fdaf F275 R88 C0a: save the round 88 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r88.md` | +283 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r88_block.md` at 24621 bytes |

### 72061f40 F275 R88 C0b: mirror the round 88 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +194 / -211 | written from the COMMITTED C0a blob read back with `git show` |

### 1a48f81a F275 R88 C1: make the plan current for round 88

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +15 / -15 | slice PLAN88, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### d995de7e F275 R88 C2: book the round 87 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +8 / -0 | slice RECORD88 appended |

### 5dc27f9b F275 R88 C3: append the round 87 prose slips

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +4 / -0 | slice SLIPS88 appended |

### d49fcbe3 F275 R88 C4: add the disk-free job id shape check normalize_job_id

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/data_paths.py` | +21 / -0 | SPEC F1: `_JOB_ID_HEX16_RE`, `normalize_job_id` and the one-line WHY comment, directly above `def lookup_job_id` |

### 35bb9fad F275 R88 C5: route the job-store load parses through normalize_job_id

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_continue.py` | +9 / -8 | SPEC F2: 7 routed; module import added; `from uuid import UUID` deleted |
| `packages/orchestration/gauntlet_runner.py` | +2 / -3 | 1 routed; function-local `UUID` import deleted |
| `packages/orchestration/handoff.py` | +2 / -3 | 1 routed; function-local `UUID` import deleted |
| `packages/orchestration/job_fulfillment.py` | +7 / -5 | 5 routed; `UUID` still used, import kept |
| `packages/orchestration/mission_readiness.py` | +3 / -2 | 1 routed; `UUID` import deleted |
| `packages/orchestration/mission_state.py` | +4 / -4 | 2 routed (one is the `uuid = ...` assignment); `UUID` dropped from the `uuid` import |
| `packages/orchestration/orchestrator_brain.py` | +4 / -2 | 1 routed; `UUID` dropped from the `uuid` import |
| `packages/orchestration/proposed_tasks.py` | +5 / -5 | 3 routed (two are the `job_uuid = ...` assignments); `UUID` dropped |
| `packages/orchestration/real_test_execution.py` | +6 / -5 | 4 routed; `UUID` dropped |
| `packages/orchestration/repair_loop.py` | +5 / -5 | 4 routed; `UUID` import deleted |
| `packages/orchestration/repair_request_builder.py` | +4 / -2 | 1 routed; `UUID` dropped |
| `packages/orchestration/self_dogfood.py` | +5 / -4 | 3 routed (one into `_lj`); `UUID` import deleted |
| `packages/orchestration/self_dogfood_execution.py` | +5 / -3 | 2 routed; `UUID` dropped |
| `packages/orchestration/task_execution.py` | +3 / -3 | 1 routed; function-local `UUID` import deleted |
| `packages/orchestration/token_economy.py` | +2 / -3 | 1 routed; function-local `UUID` import deleted |

### 3d0dac64 F275 R88 C6: pin normalize_job_id and guard the job-store load census

| Path | +/- | Reason |
|---|---|---|
| `tests/test_data_paths.py` | +125 / -0 | SPEC T1: `TestNormalizeJobId` (3 tests), `_uuid_parses_fed_to_a_job_load`, `TestJobStoreLoadsDoNotParseTheirIdWithUuid` (2 tests) with the two-row exemption set and D62's reasons; module-level `import ast` |

### 8cc8ec6a F275 R88 C7: pin that a minted job id reaches the store in run_job_fulfill

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_fulfillment.py` | +12 / -0 | SPEC T2: the test in `TestJobFulfillFixturePass`; module-level `import pytest` added (it was absent) |

### 9d33664b F275 R88 C8: record DECISION F275 D62

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | slice DEC88 APPENDED after G4, G5 and G6 ran; deletion column ZERO |

### C9 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10: no gate runs after C9, and a handback cannot carry a reading of the commit that writes it; the REVIEWER measures this commit |

THE `+/-` CELLS ABOVE WERE READ FROM `git show --numstat` AND COMPARED CELL BY CELL AGAINST G8:
C0a 283/0 = 283/0; C0b 194/211 = 194/211; C1 15/15 = 15/15; C2 8/0 = 8/0; C3 4/0 = 4/0; C4 21/0 = 21/0;
C5 66/57 (the fifteen rows summed) = 66/57; C6 125/0 = 125/0; C7 12/0 = 12/0; C8 14/0 = 14/0. Ten of ten pairs
EQUAL, zero differ. Every commit staged exactly ONE path except C5 with 15; the largest insertion count is C0a at 283.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r88w/wt 8cc8ec6a` (G6, at C7) | exit **0**; `git worktree list` then showed two rows |
| `git worktree remove .remedy-wt/r88w/wt`, then `git worktree prune -v` | exit **0**, **0**, BEFORE C8 and WITHOUT `--force`; the worktree's `status --porcelain` read `''` first; the path no longer exists; one row afterwards |
| `git archive 058bfa2d` extracted by `tarfile` into `.remedy-wt/r88w/tree_base` with its own `git init -q` (G7 base lint) | exit 0; a plain directory, never a registered worktree |
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C9; its result is in the round report |
| `gh` / `remedy` | NOT RUN. No pull request, no branch created or deleted, no merge, no force-push, no history rewrite, no full suite |

## Verification

Each gate ran through `.remedy-wt/r88w/run.py`, which saves output to `.remedy-wt/r88w/<name>.out` and appends
`PROCESS_EXIT=` from the subprocess's own return code. No reading below differs from a figure the reviewer stated.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C8 | 0 (`g123`) | `cmp` of `.remedy-wt/r88_block.md` against the COMMITTED C0a blob exit **0**, empty output, 24621 / 24621 bytes, sha256 `69b35460…2acd95`; `.agent/last_block.md` at C0b equals the C0a blob; slices FOUND **4**: PLAN88 2553 bytes / 45 lines, RECORD88 2839 / 8, SLIPS88 897 / 4, DEC88 3871 / 14, each MATCHING its BEGIN-marker sha256; TOTAL **283**, slice lines 71, PROSE **212**, as constraint 9 states; no line is a run of one repeated character; all 5 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C8 | 0 (`g123`) | `.agent/plan.md` at C1 byte-identical to PLAN88 from the committed C0a blob, 2553 bytes; **45** lines; one `## Goal`, one `## Next Steps`; unchanged at C8 |
| G3 the record | C8 | 0 (`g123`) | pre-commit blobs read with `git show` at each commit's PARENT. C2 RECORD88: **1123104** (MATCHES) + 2839 = 1125943; C8 DEC88: **1270070** (MATCHES) + 3871 = 1273941. READER A exact for both; READER B holds at N counted by the script as **4** and **7**, in order. Negative controls `G`→`g` at 1123105 and `D`→`d` at 1270074, each in the FIRST appended paragraph, REJECTED by BOTH readers. Deletion columns **0 / 0**. prose_slips at C3 = its **297865**-byte pre-commit blob + SLIPS88 exactly (298762), deletion 0. Header pattern DERIVED from the pre-commit ledger: one shape `^Gate: F\d+ R\d+ — ` matching **109 of 109** heads (559 paragraphs); RECORD88's header matches as `Gate: F275 R87 — `, no earlier head has that prefix, duplicate first lines 0 |
| G4 the change, structurally | C7 | 0 (`g4`) | the T1 helper EXECUTED FROM THE COMMITTED C7 BLOB of `tests/test_data_paths.py`, over every `.py` under `packages/` read with `git show`: at `058bfa2d` **269** files, **39** pairs in **17** files, **2** exempt; at C7 **2** pairs, both exempt. Bare-name calls: `UUID` **55** / `normalize_job_id` **0** at `058bfa2d`; **19** / **37** at C7, the 37 in the fifteen SPEC F2 modules with counts EQUAL to SPEC F2's (do_continue 7, gauntlet_runner 1, handoff 1, job_fulfillment 5, mission_readiness 1, mission_state 2, orchestrator_brain 1, proposed_tasks 3, real_test_execution 4, repair_loop 4, repair_request_builder 1, self_dogfood 3, self_dogfood_execution 2, task_execution 1, token_economy 1); `data_paths.py` holds 2 of the 19. `ui_server.py` and `test_execution_service.py` byte-identical at `058bfa2d` and C7. `ruff check` over the **18** paths C4–C7 stage: exit **0**, `All checks passed!` |
| G5 the behaviour | C7 | 0 (`g5`); scoped suite 0 (`g5b`) | (a) the **6** added node ids (diff shows exactly 6 added `def test_`) all PASSED, pytest exit 0, `6 passed`. (b) `python3 -B -m pytest tests/test_data_paths.py tests/cli/ tests/orchestration/ -q -p no:randomly` in the primary checkout: exit **0**, **`13278 passed, 10 skipped, 1 warning in 963.58s`**, failure set EMPTY. Against the reviewer's 13272 / 10 / 0 at `bd2a75d5`: **+6 passed**, which is exactly the six nodes T1 and T2 add; `058bfa2d` changed no test, and no other test was added or removed. (c) both pinned digests MATCH (30993 and 692836 bytes); the ONE fence of `.agent/authored/f275-r87-residue.py.md` at C7 (5468 bytes, `d42fbd3c…`) ran with `suite_applied.out` as control, `suite_flip88_short.out` as both flipped transcripts and the prefix: exit 0, no stderr. Flipped tally **`721 failed, 17684 passed, 29 skipped, 1 warning, 31 errors`**; bad nodes **752**; flip-only **751**; control-only **1**; pairs `data_paths.py::job_dir` TypeError **36**, `job_fulfillment.py::run_job_fulfill` ValueError **46**. All MATCH. SHARED bad nodes **1**: `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`. Lines equal after stripping to `task_id=str(UUID(td["model_task_id"])),`: **46**. Full stdout at `.remedy-wt/r88w/g5c.stdout` |
| G6 the mutation red-proofs | C7 | 0 (`g6`) | worktree at `8cc8ec6a`; `packages.orchestration.data_paths.__file__` printed before EVERY run as `.remedy-wt/r88w/wt/packages/orchestration/data_paths.py` (inside); `__pycache__` purged before each run, `python3 -B`, `PYTHONDONTWRITEBYTECODE=1`. CONTROL: exit 0, 6 passed. M1–M15, occurrence counts of `normalize_job_id(` 7, 1, 1, 5, 1, 2, 1, 3, 4, 4, 1, 3, 2, 1, 1: each exit **1**, failing ONLY `…TestJobStoreLoadsDoNotParseTheirIdWithUuid::test_no_job_store_load_under_packages_is_handed_a_uuid_parse`. M16 (occurrences 4; the first is line 639 in `run_job_fulfill`): exit **1**, failing EXACTLY that guard test and `tests/orchestration/test_job_fulfillment.py::TestJobFulfillFixturePass::test_a_pingpong_job_id_reaches_the_store_instead_of_a_uuid_parse`. M17 (occurrences 1): exit **1**, failing ONLY `tests/test_data_paths.py::TestNormalizeJobId::test_a_short_prefix_is_not_a_job_id_and_raises_invalid`. M18 (occurrences 1) and M19 (occurrences 1): each exit **1**, failing ONLY `…TestJobStoreLoadsDoNotParseTheirIdWithUuid::test_the_guard_sees_both_shapes_it_forbids`. Every restoration read `git diff --quiet` exit 0; CONTROL after the last restoration exit 0, 6 passed. All 19 required colours MET |
| G7 tree, canary, lint, path set, open set | C8 | 0 (`g78`) | `git status --porcelain` exit 0 `''`; `git worktree list` **1** row; CANARY exit **0**, **42 passed**; `ruff check . --output-format concise` exit 1 at both ends, **26** rows at `058bfa2d` (archive tree) and **26** at C8, `Found 26 errors.` at both, multiset difference EMPTY both ways; `.py` files under `.agent/` **0**; changed paths `058bfa2d`..C8 **24** against the Bundle minus handoff **24**, MISSING `[]`, EXTRA `[]`. Open set BY DISTINCT ID: **88** at `058bfa2d` and **88** at C8 (112 − 24 each), membership IDENTICAL; `R-0809`, `R-0880`, `R-0883` OPEN at both |
| G8 insertion cap | C8 | 0 (`g78`) | C0a 283/0 1 path, C0b 194/211 1, C1 15/15 1, C2 8/0 1, C3 4/0 1, C4 21/0 1, C5 66/57 15, C6 125/0 1, C7 12/0 1, C8 14/0 1; commits reaching 500 insertions **0** |

STOP READINGS, per constraint 3: before C0a and before C9, `.agent/STOP` ABSENT at both — `test -e` exit 1,
`ls -la` exit 2, `os.path.exists` False — transcripts `.remedy-wt/r88w/stop_before_C0a.txt` and
`.remedy-wt/r88w/stop_before_C9.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r88.md` | `cmp` exit 0 against `.remedy-wt/r88_block.md`, 24621 bytes, sha256 `69b3546048a96c87c8c2dfc7d0f67061e2bfa5757d80761d6344b5762d2acd95` |
| PLAN88 | `.agent/plan.md` | byte-identical, 2553 bytes, sha256 `6f7beb9bec199e6ad61e3bcc5a38b005c8d01cc859617da49da4c2bc58faeb53` |
| RECORD88 | `.agent/live_review.md` | exact suffix at C2 under readers A and B, 2839 bytes, sha256 `507d5fb28e751a9841f102dbf018be79a412a27f27e56706947a1b9c5280544c` |
| SLIPS88 | `.agent/prose_slips.md` | exact suffix at C3, 897 bytes, sha256 `882b2770656ed99208fdd84465104c1ec4234ef4590ab28b63f66f2beacafc10` |
| DEC88 | `.agent/decisions.md` | exact suffix at C8 under readers A and B, 3871 bytes, sha256 `587198a64c952e3576106c1be50ce4ac3ef268e5fde6ea9dfa63674b9e244a22` |

Every slice was applied by bytes from the COMMITTED C0a blob, and NO SLICE WAS EDITED. C4 to C7 are the worker's
own code, written from SPEC F1, F2, T1 and T2.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 round 87 verdict | done | |
| C3 prose slips | done | |
| C4 SPEC F1 | done | WHY comment wording kept under the line length (deviation 2) |
| C5 SPEC F2 | done | orphan blank lines removed with the deleted imports (deviation 1) |
| C6 SPEC T1 | done | helper definitions stated in deviation 3 |
| C7 SPEC T2 | done | |
| C8 DECISION F275 D62 | done | after G4, G5 and G6 ran |
| C9 handback | done | this commit |
| G4 · G5 · G6 | done | exit 0 · 0 · 0, at C7 |
| G1 · G2 · G3 · G7 · G8 | done | exit 0 · 0, at C8 |

## Deviations & assumptions

1. **C5: THE BLANK LINE LEFT BY A DELETED FUNCTION-LOCAL IMPORT WAS DELETED WITH IT.** The routing was applied by
   `ast` byte offsets (the `UUID` name token of each of the 37 calls). Then `ruff check --fix` ran over the fifteen
   files, which passed ruff at `058bfa2d`. It sorted the new import and deleted each now-unused `UUID` import. In
   `gauntlet_runner.collect_open_decisions`, `handoff._load_job_for_decisions`, `task_execution.can_retry_task` and
   `token_economy._inspect`, the deleted line was a function-local `from uuid import UUID` followed by a blank
   separator. Ruff left that blank line dangling after `try:` or the docstring, so the worker removed it (4 lines).
   Nothing else in C5 differs from SPEC F2. Where the module had no first-party import block (`do_continue`,
   `job_fulfillment`, `mission_readiness`, `orchestrator_brain`, `repair_request_builder`, `self_dogfood`,
   `self_dogfood_execution`, `task_execution`), the new import starts a block of its own, as ruff's isort requires.
2. **C4: THE WHY COMMENT NAMES `UUID(...)` AND `mint_job_id` WITHOUT BACKTICKS.** With double backticks the one
   line was 126 characters, over the configured 120. Without them it is 118, and it still says what SPEC F1 orders.
3. **T1 HELPER DEFINITIONS SPEC T1 LEFT OPEN.** The pair's line is the line of the ARGUMENT handed to the loader:
   the `UUID(...)` call, or the bare name. A loader call is matched by its callee's bare `Name` id or `Attribute`
   attr, against `{"load_job", "load_job_safe", "_lj"}`. No other import alias is followed, and at `058bfa2d` every
   one of the 39 matches is a bare `Name`. "Inside each function" means that function's own nodes. A nested `def`
   or `class` body belongs to the nested function only; a lambda body belongs to its enclosing function. "Assigned
   from a `UUID(...)` call" means an `ast.Assign` whose value is that call, with a bare `Name` target. The guard does
   NOT also assert that the two exempt pairs are still found: M19 must fail only the planted test, and both exempt
   sites are named shapes.
4. **TWO FIGURES IN DEC88 ARE NOT PRODUCED BY THIS ROUND'S G4–G6, contrary to constraint 10's "every figure DEC88
   states".** "827 at `bd2a75d5`" and the `job_dir` group "from 80" are round 87 readings: G5 of the round 87
   handback records distinct flipped bad nodes 827 and the `data_paths.py::job_dir` TypeError pair at 80. They were
   compared against that committed handback before C8 and match, so nothing false landed. Every other figure in
   DEC88 is one of this round's gate readings: 39 / 17 and thirty-seven / fifteen from G4; 752, the shared
   node-modules node, 36 and 46 and the `task_id=` seam from G5(c); "restoring" either kind of parse fails the guard
   (and the T2 test for `run_job_fulfill`) from G6.
5. **OBSERVED, NOT ACTED ON: THE PINNED CONTROL FAILS TWO NODES.** `suite_applied.out` tallies
   `2 failed, 18428 passed, 29 skipped, 1 warning`. One of the two is the shared vitest node. The other, the
   control-only node, is `tests/runtimes/test_runtime_cli_process_boundary.py::TestSupervisorFailures::test_an_unexpected_application_exit_is_recorded_honestly`,
   which the flipped run passes. The block states no control tally, and DEC88's "the one of them an unflipped run of
   the change also fails" counts shared nodes, so it holds. This round ran no full suite, so the worker did not
   investigate that node.
6. **G7 BASE LINT TREE.** ruff at `058bfa2d` ran over a `git archive` extraction with its own `git init`, so the
   primary checkout's `.gitignore` of `.remedy-wt/` does not hide it. Both ends used `--output-format concise`, and
   rows were compared as a `Counter` multiset of the `path:line:col: CODE message` lines.
7. **STATE FILES.** C0a and C0b land before C1 updates `.agent/plan.md`, as the Bundle orders. `.agent/context.md`
   is not in the Change set and was not touched.
8. **NO OTHER DEVIATION.** The commit sequence is exactly the Bundle. `ui_server.py` and `test_execution_service.py`
   are unchanged. No landed record was rewritten, and no `.py` file was created under `.agent/`. Of the reviewer's
   `.remedy-wt/r88/`, only the two pinned transcripts were opened, plus one directory listing. All of this worker's
   scratch is under `.remedy-wt/r88w/`, uncommitted.

## Next

The reviewer re-runs the gates and issues the round 88 verdict.

Operator questions open: 1

After that, per `.agent/plan.md`: the next residue groups of the flip's dry run (the task-id parses that feed
`TaskEntry`, the `UUID` values `pingpong_job._persist_job` cannot serialise, `ui_server`'s which-store loader and
its adapter); then the flip's dry run again; then the flip as a series of commits under the cap unless the operator
answers Q1 otherwise; then the classic store and the closure sequence.
