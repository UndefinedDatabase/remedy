# Handback — F275 round 90

## Session

`SESSION 31 of feature F275 · round 90 · rounds so far 90`

## Range

Review of `844a7f21`..`HEAD` (the six commits C0a–C4 plus this handback commit C5).

## Commits

### 8904d129 F275 R90 C0a: save the round 90 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r90.md` | +258 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r90_block.md` at 23717 bytes |

### cd762e16 F275 R90 C0b: mirror the round 90 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +179 / -156 | written from the COMMITTED C0a blob read back with `git show` |

### 49ef7e09 F275 R90 C1: make the plan current for round 90

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +22 / -19 | slice PLAN90, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### 5ee86fa2 F275 R90 C2: book the round 89 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6 / -0 | slice RECORD90 appended |

### 2d477f96 F275 R90 C3: commit the flip's first overlay carrier

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r90-overlay.md` | +314 / -0 | SPEC C: 28 lines of prose, then ONE ```` ```diff ```` fence holding the verbatim 284-line, 12756-byte stdout of `git diff` in EDIT after SPEC O and before any test ran there, then the closing fence line and one newline; 14527 bytes, sha256 `92529281f1e022787676048ad85cb6c7c2b1031abc1405b03effa088b80204bb` |

### bc467b07 F275 R90 C4: record DECISION F275 D64

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | slice DEC90 APPENDED after G4, G5 and G6 ran; deletion column ZERO |

### C5 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10: no gate runs after C5, and a handback cannot carry a reading of the commit that writes it; the REVIEWER measures this commit |

THE `+/-` CELLS ABOVE WERE READ FROM `git show --numstat` AND COMPARED CELL BY CELL AGAINST G8:
C0a 258/0 = 258/0; C0b 179/156 = 179/156; C1 22/19 = 22/19; C2 6/0 = 6/0; C3 314/0 = 314/0; C4 14/0 = 14/0.
Six of six pairs EQUAL, zero differ. Every commit staged exactly ONE path; the largest insertion count is C3 at 314.

### SPEC O, as carried by the overlay (the eleven paths, inside the flipped tree only; +/- read with `git apply --numstat` of the extracted fence)

| Path | +/- in the overlay | What |
|---|---|---|
| `packages/orchestration/ui_server.py` | +13 / -30 | O1: `_load_job` rewritten — `JobIdInvalid`, `normalize_job_id` and `load_job_plan` imported in the function; `JobIdInvalid` answers 404 when the string fully matches `[0-9a-fA-F]+`, else 400; `OSError` from `load_job_plan` read as no record; no record 404; docstring `Load a job record by id, return (job, error_tuple).`; module `from uuid import UUID` deleted |
| `packages/orchestration/run_report.py` | +9 / -9 | O2: 9 reads |
| `packages/orchestration/source_apply.py` | +2 / -2 | O2: 2 reads |
| `packages/orchestration/patch_apply.py`, `repo_applicator.py`, `diff_repair_apply.py`, `mission_state.py` (the `previous_job` read), `job_digest.py`, `real_test_execution.py`, `apps/cli/commands/repo.py` | +1 / -1 each | O2: 1 read each; `mission_state.py`'s `getattr(task, 'description', '?')` and `getattr(tasks[0], 'description', '?')` in the verify-first error messages untouched |
| `tests/orchestration/test_run_report.py` | +6 / -6 | O3: `_FakeTask` sets `task_id` / `title`; `_FakeJob` sets `job_id` / `job_title`, docstring ends `reads off a job record.`; docstring `str(t.task_id)[:8]` |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r90w/wt_EDIT 844a7f21`, `... wt_CONTROL 844a7f21`, `... wt_OVERLAY 844a7f21` (G4, before C3) | exit **0**, **0**, **0** |
| transform in each worktree; in EDIT `git add -A` then SPEC O; in OVERLAY `git add -A` then `git apply --check` and `git apply` of the fence from the committed C3 blob | exit 0 throughout (see G4; the OVERLAY `git add -A` is deviation 1) |
| `git checkout HEAD -- .` in each worktree, then `git worktree remove` each, then `git worktree prune -v` | exit 0 throughout, AFTER G6 and BEFORE C4, WITHOUT `--force`; `git status --porcelain` `''` in each before removal (only ignored `.data/`, `.pytest_cache/`, `.ruff_cache/`, `apps/ui/dist/`, `apps/ui/node_modules/` in CONTROL and OVERLAY); all three paths gone; `git worktree list` one row |
| `git archive` of `ef75e213` and `844a7f21` extracted by `tarfile` into `.remedy-wt/r90w/gen/` (tree_base, tree_tip, tree_shift, tree_delete, each `git init -q` + `git add -A -f .`), and `844a7f21` into `.remedy-wt/r90w/tree_base` (G7 base lint) | exit 0; plain directories, never registered worktrees |
| `git push origin feature/f275-one-world-completion-part-three` | run after C5; its result is in the round report |
| `gh` / `remedy` | NOT RUN. No pull request, no branch created or deleted, no merge, no force-push, no history rewrite |

## Verification

Each gate ran through `.remedy-wt/r90w/run.py`, which saves output to `.remedy-wt/r90w/<name>.out` and appends
`PROCESS_EXIT=` from the subprocess's own return code. Every figure the block states reproduced; the three reading
choices behind G4(c), G5's node count and DEC90's "four" are in the deviations.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C4 | 0 (`g123`) | `cmp` of `.remedy-wt/r90_block.md` against the COMMITTED C0a blob exit **0**, empty output, 23717 / 23717 bytes, sha256 `35ef3ccb…9b1c9c`; `.agent/last_block.md` at C0b equals the C0a blob and is unchanged at C4; slices FOUND **3**: PLAN90 2967 bytes / 48 lines, RECORD90 2495 / 6, DEC90 4920 / 14, each MATCHING its BEGIN-marker sha256; TOTAL **258**, slice lines 68, PROSE **190**, as constraint 9 states; no line is a run of one repeated character; all 4 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C4 | 0 (`g123`) | `.agent/plan.md` at C1 byte-identical to PLAN90 from the committed C0a blob, 2967 bytes; **48** lines; one `## Goal`, one `## Next Steps`; unchanged at C4 |
| G3 the record | C4 | 0 (`g123`) | pre-commit blobs read with `git show` at each commit's PARENT. C2 RECORD90: **1128932** (MATCHES) + 2495 = 1131427; C4 DEC90: **1277039** (MATCHES) + 4920 = 1281959. READER A exact for both; READER B holds at N counted by the script as **3** and **7**, in order. Negative controls `G`→`g` at offset 1128933 and `D`→`d` at 1277043, each in the FIRST appended paragraph, REJECTED by BOTH readers. Deletion columns **0 / 0**. Header pattern DERIVED from the pre-commit ledger: one shape `^Gate: F\d+ R\d+ — ` matching **111 of 111** heads (567 paragraphs); RECORD90's header matches as `Gate: F275 R89 — `, no earlier head has that prefix, duplicate first lines 0 |
| G4 flipped trees and the carrier | C3 | 0 (`g4_build`), 0 (`o_edit`), 0 (`c3_carrier`), 0 (`g4_check`) | Pinned inputs MATCH: `r77_corrected.json` 120753 bytes `765b5ba9…`, owners 121095 `670c6e95…`, `r61_status.json` 1438 `a4c6cd63…`. Fences from the committed carriers: rekey 5186 `f56394e9…`, owner 24253 `7be34374…`, input 10580 `c50da973…`, transform 29032 `075bc0dc…`. DELETE control line count **1**. Generator exit **0**: paths differing BASE/TIP **56**; ruled sites 2183 recovered by scope at TIP, SHIFT, DELETE, UNRESOLVED **0**; line-key CONTROL **1895 / 1886 / 1886**; owner check at TIP **1908** CONFIRMED, **275** REFUSED, **0** CONTRADICTED (stdout identical to round 89's C5 run but for the scratch paths). Transform exit **0** in EDIT, CONTROL, OVERLAY: 2183 resolving / 0 not, **264** files, **6097** rewrites, **0** broken, numstat +5252 −5079, untracked `[]`, in each. SPEC O script: renamed per file 2,1,1,1,1,9,1,1,1 = **18**, each equal to SPEC O's count. (a) fence from the COMMITTED C3 blob: one `` ```diff `` line, one closing line, nothing after but one newline; extracted patch 12756 bytes, sha256 `aa9c08fb…6275fe18f`, equal to EDIT's saved `git diff` stdout; OVERLAY `git apply --check` exit **0**, `git apply` exit **0**; `git diff --name-only` **11** paths = SPEC O's eleven, each byte-identical to EDIT's; cross-check: tracked paths whose bytes differ OVERLAY vs CONTROL = the same 11. (b) `ast` over the nine O2 files: reading `id`/`name`/`description` **19** CONTROL, **1** OVERLAY; reading `job_id`/`job_title`/`task_id`/`title` **0** and **18**; OVERLAY `mission_state.py` `getattr(..., 'description', '?')` **2**; in `_load_job` `UUID` **1 / 0**, `normalize_job_id` **0 / 1**, `load_job_plan` **2 / 1**, `_JobPlanAdapter` **1 / 0**; module-level `from uuid` imports **1 / 0**. (c) ruff by stdin with `cwd` inside each worktree over the eleven: CONTROL **4** rows (I001 in `repo.py`, `mission_state.py`, and `ui_server.py` at 241 and 1604), OVERLAY **3** rows; as a multiset with line:col removed: added **0**, removed **1** (`ui_server.py` I001, the `_load_job` import block); as a multiset of full rows: added 1 / removed 2, only because the `ui_server.py` row at 1604 moved to 1587 (deviation 2) |
| G5 full suite, CONTROL then OVERLAY | C3 | 1 (`g5_CONTROL`), 1 (`g5_OVERLAY`), 0 (`g5_cmp`) | Before each run `apps/ui/node_modules` and `apps/ui/dist` ABSENT (both present after); `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`, `cwd` the worktree; `packages.orchestration.ui_server.__file__` inside the worktree in both. pytest exit 1 in both (red suites, as expected). CONTROL **`650 failed, 17755 passed, 29 skipped, 1 warning, 31 errors`** (in 1565.53s), **681** distinct FAILED/ERROR node ids; OVERLAY **`529 failed, 17876 passed, 29 skipped, 1 warning, 31 errors`** (in 1382.06s), **560**; bad only in CONTROL **121**, only in OVERLAY **0**; the 121 by file: `test_command_channel.py` 57, `test_run_report_hook.py` 16, `test_command_dispatch.py` 11, `test_job_report.py` 8, `test_job_digest.py` 6, `test_diff_endpoint.py` 6, `test_live_state.py` 4, `test_command_catalog.py` 3, `test_job_commands.py` 2, `test_fence_e2e.py` 2, `test_decisions_endpoint.py` 2, `test_digest_route.py` 2, `test_ux_quality.py` 1, `test_dashboard_contract.py` 1 — equal to the block's list. All MATCH |
| G6 red-proof in OVERLAY | C3 | 0 (`g6`) | `__pycache__` purged before each run (0 directories each time, `PYTHONDONTWRITEBYTECODE=1`); module printed inside OVERLAY before each run. CONTROL exit 1 **`7 failed, 174 passed`**. M1: the line `        job = load_job_plan(job_id)` count in `ui_server.py` **1**, argument wrapped as `__import__("uuid").UUID(job_id)`: exit 1 **`92 failed, 89 passed, 85 warnings`**, newly bad **85**, recovered **0** (78 in `test_command_channel.py`, 7 in `test_digest_route.py`). M2: the line `        job_id = str(getattr(job, "job_id", "") or "")` count in `job_digest.py` **1**, reads `"id"`: exit 1 **`9 failed, 172 passed`**, newly bad exactly `test_job_digest.py::test_cost_basis_is_actual_when_every_call_is_priced` and `::test_cost_basis_is_lower_bound_when_calls_are_unpriced`, recovered 0. After each, bytes restored and EQUAL to the carrier-applied ones (EDIT's). All MATCH |
| G7 tree, canary, lint, path set, open set | C4 | 0 (`g78`) | `git status --porcelain` exit 0 `''`; `git worktree list` **1** row; `git diff --name-only 844a7f21 bc467b07 -- packages apps tests docs scripts` exit 0, empty; CANARY exit **0**, **42 passed**; `ruff check . --output-format concise` exit 1 at both ends, **26** rows at `844a7f21` (archive tree) and **26** at C4, multiset difference EMPTY both ways; `.py` files under `.agent/` **0**; changed paths `844a7f21`..C4 **6** against the Bundle minus handoff **6**, MISSING `[]`, EXTRA `[]`. Open set BY DISTINCT ID: **88** at `844a7f21` and **88** at C4 (112 − 24 each), membership IDENTICAL; `R-0809`, `R-0880`, `R-0883` OPEN at both |
| G8 insertion cap | C4 | 0 (`g78`) | C0a 258/0 1 path, C0b 179/156 1, C1 22/19 1, C2 6/0 1, C3 314/0 1, C4 14/0 1; commits reaching 500 insertions **0** |

STOP READINGS, per constraint 3: before C0a and before C5, `.agent/STOP` ABSENT at both — `test -e` exit 1,
`ls -la` exit 2, `os.path.exists` False — transcripts `.remedy-wt/r90w/stop_before_C0a.txt` and
`.remedy-wt/r90w/stop_before_C5.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r90.md` | `cmp` exit 0 against `.remedy-wt/r90_block.md`, 23717 bytes, sha256 `35ef3ccb4c781e6ef18294fd87c878e074cf1a7cfb08c6459b9db3e66a9b1c9c` |
| PLAN90 | `.agent/plan.md` | byte-identical, 2967 bytes, sha256 `9a9215f7264417fd8b49c1954a4acb4e11bdbc93af9ca84720d00b0f99860ddd` |
| RECORD90 | `.agent/live_review.md` | exact suffix at C2 under readers A and B, 2495 bytes, sha256 `bb11e112ee3c0633a3ed45056c15fdca2a20b72256be573c56ec91a11360957c` |
| DEC90 | `.agent/decisions.md` | exact suffix at C4 under readers A and B, 4920 bytes, sha256 `4f9fdd0d02e28208f74c909859de43e4391339b3caa49c2e74cfb8e93fd810ba` |

Every slice was applied by bytes from the COMMITTED C0a blob, and NO SLICE WAS EDITED. C3 is the worker's own
text from SPEC C over the worker's own SPEC O edit.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 round 89 verdict | done | |
| C3 overlay carrier (SPEC C over SPEC O) | done | |
| C4 DECISION F275 D64 | done | after G4, G5 and G6 ran |
| C5 handback | done | this commit |
| G4 · G5 · G6 | done | at C3; exits in the table |
| G1 · G2 · G3 · G7 · G8 | done | exit 0 · 0, at C4 |

## Deviations & assumptions

1. **`git add -A` IN OVERLAY BEFORE `git apply`.** The block orders `git add -A` only in EDIT. Without it, OVERLAY's
   `git diff --name-only` would list the transform's 264 files as well, and G4(a) states that it lists exactly
   SPEC O's eleven. So OVERLAY's transform was staged too, and `git apply` still wrote only the working tree. As a
   check that does not depend on the staging, the tracked paths whose bytes differ between OVERLAY and CONTROL
   are exactly the same eleven.
2. **G4(c) ROW IDENTITY.** Compared as full `path:line:col: CODE message` rows, the multisets differ by added 1 /
   removed 2. That is because the one `ui_server.py` row outside `_load_job` sits at 1604 in CONTROL and at 1587 in
   OVERLAY, after the overlay removes 17 lines above it. With line:col removed, the rows read added **0** and
   removed **1**, an `I001`. That is the only reading that fits the reviewer's "4 rows and 3, the one removed an
   `I001`", and it is the reading reported as G4(c).
3. **G5 DISTINCT NODE IDS.** My first extraction used `^(FAILED|ERROR) (\S+?)( - .*)?$`, which misses a node id
   containing a space, and so read CONTROL as 680. The id is
   `tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field[has space]`.
   The reported counts read each summary line's id up to its first ` - `: CONTROL 681 lines and 681 distinct ids,
   OVERLAY 560 and 560. Neither transcript has an id on two lines.
4. **DEC90's "85 nodes of four test files".** G6's M1 turns 85 nodes bad, all inside G6's four-file selection, but
   only two of those files hold them: 78 in `test_command_channel.py` and 7 in `test_digest_route.py`. The sentence
   is true if "four test files" means the selection. It is false if it means the files that go bad. DEC90 landed
   byte for byte per constraint 1, and I declare the wording here without repairing it.
5. **SPEC O EDIT MECHANICS.** O1 replaced `_load_job`'s whole `ast` line span. The local `import re` it held was
   dropped because the module already imports `re` at the top. Deleting the module-level `from uuid import UUID`
   left the function-local `from uuid import UUID` at `ui_server.py`'s project-loading route untouched. O2 replaced
   each string constant's bytes by `ast` byte offsets and kept its quote character. Every rename passed through a
   per-file count assertion equal to SPEC O's figures.
6. **NO OTHER DEVIATION.** The commit sequence is exactly the Bundle. `.agent/context.md` is not in the Change set
   and was not touched. The reviewer's `.remedy-wt/r90/` was not opened. All of this worker's scratch is under
   `.remedy-wt/r90w/`, uncommitted.

## Next

The reviewer re-runs the gates and issues the round 90 verdict.

Operator questions open: 1

After that, per `.agent/plan.md`: more overlays, one residue group each, applied on top of this one; then the flip
(transform plus every overlay in round order) as a series of commits under the cap; then the classic store and the
closure sequence.
