# Handback — F275 round 85

## Session

`SESSION 29 of feature F275 · round 85 · rounds so far 85`

NO SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED, by amendment amend0911-f275-to-scope.

Context self-assessment: this worker ran one scoped suite, one canary, one CLI probe of two arms and one
red-proof of one mutation, and has ample context left; nothing about the session boundary is forced by
this round.

## Range

Review of `53659062`..`HEAD` (the ten commits C0a–C8 plus this handback commit C9).

## Commits

### 86eadc98 F275 R85 C0a: save the round 85 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r85.md` | +261 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r85_block.md` at 26157 bytes |

### f2c7de8c F275 R85 C0b: mirror the round 85 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +179 / -211 | written from the COMMITTED C0a blob read back with `git show` |

### 842e7b71 F275 R85 C1: make the plan current for round 85

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12 / -12 | slice PLAN85, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### f66f2765 F275 R85 C2: book the round 84 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +8 / -0 | slice RECORD85 appended |

### 9759bcf1 F275 R85 C3: register R-0882, the adopt crash on a ping-pong job id

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | slice FIND85 appended, BEFORE the repair commit |

### 2fc16fab F275 R85 C4: append the round 83 and round 84 prose slips

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +4 / -0 | slice SLIPS85 appended |

### 185f18d4 F275 R85 C5: pass the resolved id to load_job as a string in project adopt

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/project.py` | +1 / -1 | SPEC F: `        job = load_job(UUID(resolved_id))` became `        job = load_job(resolved_id)`; nothing else changed; the `UUID` import stays for the seven other references. The worker's own edit |

### 86b86e23 F275 R85 C6: pin the adopt repair with an in-process ping-pong test

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_scoped_listings.py` | +34 / -0 | SPEC T: `TestScopedListingsCLI.test_adopting_a_pingpong_job_id_exits_cleanly_instead_of_crashing`, in-process, plus `import pytest` at module level (the file had none); no existing test edited or deleted. The worker's own code |

### 589a37ed F275 R85 C7: resolve R-0882 in the round that registered it

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | slice DONE85 appended, only after G4, G5 and G6 at C6 reproduced every reading it states |

### a3c64ca1 F275 R85 C8: record DECISION F275 D59

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | slice DEC85 APPENDED; deletion column ZERO; D58 untouched |

### C9 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10: no gate runs after C9, and a handback cannot carry a reading taken after the commit that writes it; the REVIEWER measures this commit |

THE `+/-` CELLS ABOVE WERE READ FROM `git show --numstat` AND COMPARED CELL BY CELL AGAINST G8:
C0a 261/0 = 261/0; C0b 179/211 = 179/211; C1 12/12 = 12/12; C2 8/0 = 8/0; C3 2/0 = 2/0; C4 4/0 = 4/0;
C5 1/1 = 1/1; C6 34/0 = 34/0; C7 2/0 = 2/0; C8 14/0 = 14/0. Ten of ten pairs EQUAL, zero differ. Every
commit staged exactly ONE path; the largest insertion count is C0a at 261.

## External actions

| Command | Outcome |
|---|---|
| `git archive -o .remedy-wt/r85w/base.tar 53659062` and `git archive -o .remedy-wt/r85w/c6.tar 86b86e23`, extracted by `tarfile` into `tree_base` and `tree_c6` | the G4 and G5(c) scratch trees; plain directories, never registered |
| `git worktree add --detach .remedy-wt/r85w/wt 86b86e23` (G6) | `Preparing worktree (detached HEAD 86b86e23)`; `git worktree list` then showed two rows |
| `git worktree remove .remedy-wt/r85w/wt` then `git worktree prune -v` | WITHOUT `--force`, before C7; both printed nothing and no error; afterwards the directory is gone (`os.path.exists` False) and `git worktree list` shows the primary checkout alone. Their exit codes were NOT captured separately (deviation 4) |
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C9; result in the round report |
| `gh` / `remedy` | NOT RUN. The CLI ran only as `python3 -B -m apps.cli.grouped` inside the G5(c) scratch probe. No pull request, no branch created or deleted, no merge, no force-push, no history rewrite |

## Verification

Each gate ran through `.remedy-wt/r85w/run.py`. It saves the output to `.remedy-wt/r85w/<gate>.out`
and appends `PROCESS_EXIT=` from the subprocess's own return code.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C8 | 0 | `cmp` of the block as received against the COMMITTED C0a blob exit **0**, empty output, both 26157 bytes, sha256 `88e35ec9…fa3be5`; `.agent/last_block.md` at C0b equals the C0a blob; slices FOUND **6**: PLAN85 2645 bytes / 44 lines, RECORD85 3119 / 8, FIND85 2322 / 2, SLIPS85 1130 / 4, DONE85 1360 / 2, DEC85 3035 / 14, each MATCHING the sha256 on its BEGIN marker; TOTAL **261**, slice lines 74, PROSE **187**, as constraint 9 states; no line (length ≥ 1) is a run of one repeated character; all 7 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C8 | 0 | `.agent/plan.md` at C1 byte-identical to PLAN85 from the committed C0a blob, 2645 bytes, sha256 `bc6516c9…edaefc`; **44** lines; one `## Goal`, one `## Next Steps` |
| G3 the record | C8 | 0 | pre-commit blobs read at each commit's PARENT. C2 RECORD85: 1107652 (MATCHES the block) + 3119 = 1110771; C3 FIND85: 1110771 + 2322 = 1113093; C7 DONE85: 1113093 + 1360 = 1114453; C8 DEC85: 1257440 (MATCHES the block) + 3035 = 1260475. READER A exact for all four; READER B holds at N counted by the script as **4**, **1**, **1**, **7**. Negative controls: a letter flipped in each FIRST appended paragraph (`G`→`g` at 1107653, `R`→`r` at 1110774, `D`→`d` at 1113094, `D`→`d` at 1257444) REJECTED by BOTH readers, all four. Deletion columns **0 / 0 / 0 / 0**. prose_slips at C4 = its 294305-byte pre-commit blob + SLIPS85 exactly (295435), deletion column 0. Header pattern DERIVED from the pre-commit ledger (prefix to the first ` — `, digit runs generalised): one shape, `^Gate: F\d+ R\d+ — `, matching **106 of 106** `Gate:` heads (544 paragraphs); RECORD85's header matches it as `Gate: F275 R84 — `, and no earlier head has that prefix or the same first line. `- R-0882 — ` lines: 0 at C2, **1** at C3, 1 at C7; `Done: R-0882 — ` lines: 0 at C3, **1** at C7, 1 at C8 |
| G4 the repair, structurally | C6 | 0 / 0 / 0 | by `ast` (`g4.out`). `_cmd_project_adopt`: `UUID` calls taking `resolved_id` **1** at `53659062`, **0** at C6; SPEC F's new line whole-line count **1** at C6, in the file and in the function. `UUID(...)` census under `apps/cli/`: at `53659062` **22 = 13 into `load_job` + 8 naming a project + 1 other** (`context.py:38`, `task_id`); at C6 **21 = 12 + 8 + 1**, the only row gone being `project.py:452`. Resolver sweep over `apps/` and `packages/`, `data_paths.py` excluded: **62** resolver calls at both points; a bound result passed to a LATER `UUID(...)` in the same function **1** at `53659062` (`project.py:449` binds `resolved_id` → `UUID(resolved_id)` at 452), **0** at C6. PLANTED CONTROL (`g4_plant.out`, exit 0): a copy of the C6 tree with `planted = lookup_job_id(raw)` then `return UUID(planted)` appended to `project.py` reports **1** (`project.py:504` → 505) at 63 calls, and the unplanted C6 tree reports 0 at 62. `ruff check apps/cli/commands/project.py tests/cli/test_scoped_listings.py` exit **0**, `All checks passed!` |
| G5 the behaviour | C6 | 0 / 0 / 0 | (a) the SPEC T node id **PASSED**, `1 passed`, pytest exit 0, primary checkout. (b) the scoped suite in the PRIMARY checkout at C6, exit **0**: **13261 passed, 10 skipped, 0 failed**, 1 warning, 934.07s; zero `FAILED`/`ERROR` lines, so the failure set is EMPTY. Against the reviewer's 13260 at `53659062` the difference is **+1**: the one test C6 adds, whose deletion column is 0. Skipped stays 10. (c) THE CLI PROBE (`g5c.out`). Each arm used a fresh data root: a git repo, `init` run from that arm's own tree (exit 0, 1 project), and one ping-pong record `jobs/0123456789abcdef/job.json`. Each arm's `apps.cli.commands.project.__file__` was printed and lies inside its own scratch tree. ARM `53659062`: exit **1**, stderr holds `Traceback` **True**, last stderr line `ValueError: badly formed hexadecimal UUID string`. ARM C6: exit **3**, `Traceback` **False**, last stderr line `Error: job not found: 01234567` |
| G6 mutation red-proof | C6 | 0 | worktree at `86b86e23`. Before each run `apps.cli.commands.project.__file__` printed as `/home/decodeux/Repos/remedy/.remedy-wt/r85w/wt/apps/cli/commands/project.py`, INSIDE the worktree; pytest `rootdir` the worktree both times; `__pycache__` purged before each run (0 before CONTROL, 8 before M1, 8 after restore). Selection `TestScopedListingsCLI`, six tests in the order full_isolation, legacy_job_hidden, adopt_persists, adopting_a_pingpong, orphaned_label, status_scoped. CONTROL pytest exit **0**: PASS PASS PASS PASS PASS PASS. M1: target whole-line count **1**, mutated numstat 1/1. Pytest exit **1**: PASS PASS PASS **FAIL** PASS PASS, `1 failed, 5 passed`. The pinned test's first error line is `E               ValueError: badly formed hexadecimal UUID string`. Required colours MET. Restored by `git checkout`, and `git diff` in the worktree was empty; worktree `status --porcelain` `''`; then removed and pruned before C7 |
| G7 tree, canary, lint, path set, open set | C8 | 0 | `git status --porcelain` exit 0 `''`; `git worktree list` **1** row; CANARY exit **0**, **42 passed**; `ruff check .` exit **1** by design, **26** `-->` rows against ruff's own `Found 26 errors.`; changed paths `53659062`..C8 **8** against the Bundle minus handoff **8**, MISSING `[]`, EXTRA `[]`. Open set BY DISTINCT ID: **87** at `53659062` (110 registered − 23 Done), **88** after C3 (111 − 23), added exactly `['R-0882']`, removed none; **87** at C8 (111 − 24), removed exactly `['R-0882']`, added none; base-to-C8 membership difference empty; `R-0809` and `R-0880` OPEN at all three points |
| G8 insertion cap | C8 | 0 | C0a 261/0 1 path, C0b 179/211 1, C1 12/12 1, C2 8/0 1, C3 2/0 1, C4 4/0 1, C5 1/1 1, C6 34/0 1, C7 2/0 1, C8 14/0 1; commits reaching 500 insertions **0** |

THE HOLD BEFORE C7 WAS CHECKED, NOT ASSUMED. DONE85 states five readings, and each was compared with G4 to G6
at C6 before C7 was committed. They are: exit 3 with `job not found` and the first eight characters; restoring
the parse fails the pinned test alone, with `ValueError`, and the rest of its class stays green; the real CLI
exits 3 with no traceback at C6 and 1 with one at the base; and the sweep finds no other resolver result
passed to a later `UUID(...)`. All five matched, so C7 and C8 landed.

STOP READINGS, per constraint 3: before C0a and before C9, `.agent/STOP` ABSENT at both — `test -e`
exit 1, `ls -la` exit 2, `os.path.exists` False — transcripts `.remedy-wt/r85w/stop_before_C0a.txt`
and `.remedy-wt/r85w/stop_before_C9.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r85.md` | `cmp` exit 0 against `.remedy-wt/r85_block.md`, 26157 bytes, sha256 `88e35ec979a2efa4b16642327e4aeec1a572bc4af6f04981691f0fcb7bfa3be5` |
| PLAN85 | `.agent/plan.md` | byte-identical, 2645 bytes, sha256 `bc6516c9d26fc7d6c5ffa564caee5e182280c673e777ed2f0066d36073edaefc` |
| RECORD85 | `.agent/live_review.md` | exact suffix at C2 under readers A and B, 3119 bytes, sha256 `3982ca823f7ce7e7282ae61d6324a26d1d9798db151c9ec26ccbcb11ca904c96` |
| FIND85 | `.agent/live_review.md` | exact suffix at C3 under readers A and B, 2322 bytes, sha256 `ba714fa8c316af951b4a733d784186a2839e47a38d79ded392c28e60815e9f92` |
| SLIPS85 | `.agent/prose_slips.md` | exact suffix at C4, 1130 bytes, sha256 `f268d4dafb58ee32b3af579c16a570102afeee450dfe5ada1480897972697428` |
| DONE85 | `.agent/live_review.md` | exact suffix at C7 under readers A and B, 1360 bytes, sha256 `6d68a4867d8f22e33c6946ed7a236a42affb0ff6b0411de921d31de1a460b6bb` |
| DEC85 | `.agent/decisions.md` | exact suffix at C8 under readers A and B, 3035 bytes, sha256 `59d541e9d2f837cf5d1a0c13c0585b399f8950f72cf935de0ecf15fba5ee4b95` |

Every slice was applied by bytes from the COMMITTED C0a blob, and NO SLICE WAS EDITED. C5 and C6 are the
worker's own code, written from SPEC F and SPEC T.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 round 84 verdict | done | |
| C3 register R-0882 | done | before C5 |
| C4 prose slips | done | |
| C5 the repair | done | exactly SPEC F's one line |
| C6 the regression test | done | in-process; `import pytest` added at module level |
| C7 resolve R-0882 | done | after the DONE85 readings reproduced at C6 |
| C8 DECISION F275 D59 | deviated | landed byte for byte; one figure inside it does not reproduce (deviation 1) |
| C9 handback | done | this commit |
| G1 · G2 · G3 | done | exit 0 · 0 · 0, at C8 |
| G4 · G5 · G6 | done | exit 0 · 0 · 0, at C6 |
| G7 · G8 | done | exit 0 · 0, at C8 |

## Deviations & assumptions

1. **DEC85 SAYS THE SWEEP "FINDS 64 CALLS"; THIS WORKER MEASURES 62. DECLARED, NOT REPAIRED.** At
   `53659062`, over `apps/` and `packages/` with `data_paths.py` excluded, `ast` finds **62** calls whose
   callee is `resolve_job_id` (32), `lookup_job_id` (27) or `resolve_any_job_id` (3). All 62 are under
   `apps/` and none under `packages/`; `data_paths.py` itself holds 1 more. A `git grep` of `<name>(` over
   the same paths finds 62 lines outside `data_paths.py`. Bare name references are also 62, attribute
   references 0, and `tests/` would add 22. No counting basis I tried gives 64. The figure is in DEC85, not DONE85,
   and no gate orders it, so the hold before C7 did not apply. DEC85 landed byte for byte under
   constraint 1. The readings the sweep's conclusion rests on reproduce exactly: 1 use at the base, this
   site; 0 at C6; and the planted control is caught.

2. **THE REVIEWER'S SCRATCH DIRECTORY STILL HOLDS FILES.** `.remedy-wt/r85/` holds `apply_fix.py`,
   `test_adopt_probe.py`, `redproof.py`, `census.py`, `caller_sweep.py`, `cli_probe.py`, two trees and
   more. Constraint 2 says the reviewer's candidate is deleted. I did NOT open any of them and did NOT
   delete them, because they are not mine and no line orders their removal. All of this worker's scratch
   is under `.remedy-wt/r85w/`, uncommitted.

3. **G5(c) RAN `python3 -B -m apps.cli.grouped`**, not `python3 -m apps.cli.grouped`. The `-B` keeps the
   scratch trees free of bytecode and does not change what is imported: each arm printed its module's
   `__file__` inside its own tree. The probe removed `REMEDY_PROJECT` and any inherited `PYTHONPATH` from the
   environment before setting `PYTHONPATH` to the arm's tree, and ran `adopt` with the arm's fresh git repo
   as the working directory. That is how "a data root holding one project" was met: `init` ran in that repo.

4. **THE WORKTREE `remove` AND `prune` EXIT CODES WERE NOT CAPTURED SEPARATELY.** They ran as plain
   git commands, whose exit status this shell did not surface. Both printed nothing, with no error, and
   their effect was measured: the directory is gone, and `git worktree list` has one row, again under G7 at C8.
   The same applies to `git worktree add`, which printed `HEAD is now at 86b86e23`.

5. **G6 PASSED `-v -p no:randomly -p no:cacheprovider` TO PYTEST** with the class selection. `-v` gives
   the per-test colours. `no:cacheprovider` keeps `.pytest_cache` out of the worktree so it could be
   removed without `--force`. The 8 `__pycache__` directories purged before M1 and after the restore were
   written by the class's own `init` subprocesses, which do not run with `-B`.

6. **SPEC T's TEST, READ IN DETAIL.** `_env(data_dir)` is computed BEFORE `monkeypatch.chdir`, so
   `_init_project`'s subprocess keeps the launch directory as `PYTHONPATH`, exactly as the class's other
   tests do. The record is `{"id": "0123456789abcdef"}`, the shape `tests/test_data_paths.py` uses.
   `capsys.readouterr()` drains the fixture's output before the call, so the assertion reads only the
   handler's stderr. The test carries a docstring stating why it is in-process.

7. **MEASURED, NOT PREDICTED BY THE BLOCK.** The census rows at C6 are in `.remedy-wt/r85w/g4.out`. The
   12 `load_job` rows are `dashboard_cmd.py:63` (`jid`), `job_stop_cmd.py:52` (`job_id`), `memory.py:307`,
   `340` and `381`, `project.py:156`, `readiness.py:88` (`jid`), `repo.py:174`, and `review_cmd.py:24`, `70`,
   `112` and `146` (`args.job_id`). The 8 project rows include `status_cmd.py:49` (`scope.project_id`)
   and `readiness.py:74`. The scoped suite took 934.07s.

8. **NO OTHER DEVIATION.** The commit sequence is exactly the Bundle, and C1 is the first
   substantive commit. Nothing under `packages/`, `docs/` or `scripts/` was touched, and no landed record was rewritten.
   No `.py` file was created under `.agent/`. The bash guard rejects `$?`, so every gate's exit code was
   read through `run.py`.

## Next

The reviewer re-runs the gates and the red-proof and issues the round 85 verdict. That includes reading
deviation 1's resolver-call count against its own instrument.

Operator questions open: 0.

After that comes THE REMAINING `load_job(UUID(...))` PARSES under `apps/cli/`: twelve by flow at C6.
Each is read for whether its caller keeps using the raw argument as a key, starting with `job stop`'s
loader. Then THE FLIP, under DECISION F275 D48 and D56.
