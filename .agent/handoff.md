# Handback — F261 round 4

## Session

`SESSION 1 of feature F261 · round 4 · rounds so far 4`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `b8f019de`..`HEAD`: C0a, C0b, C1, C2 and C3, plus this handback commit C4. `.agent/STOP` was ABSENT at all
three readings constraint 2 orders: before C0a (`.remedy-wt/f261r4w/probe0.py` printed `STOP exists: False`; a Python
`os.path.exists` reading exited 1 and `ls .agent/STOP` exited 2, "No such file or directory"), before C2 (`ls` exit 2)
and before C4 (`ls` exit 2).

## Commits

### 2ccc400b F261 R4 C0a: save the round 4 step block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r4.md` | +215 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### 71b078e7 F261 R4 C0b: mirror the round 4 step block into last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +94 / -148 | the same bytes, the mirror |

### bca20317 F261 R4 C1: re-point the plan at round 4, book round 3's PASS, register R-0894 and R-0895, record DECISION F261 D3

This is the FIRST SUBSTANTIVE COMMIT.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | slice DEC3 appended: DECISION F261 D3 |
| `.agent/live_review.md` | +6 / -0 | slice RECORD4 appended: `Gate: F261 R3 —` PASS, R-0894, R-0895 |
| `.agent/plan.md` | +16 / -17 | slice PLAN4, a full replacement: 1724 bytes, 36 lines |

### 36eb4573 F261 R4 C2: delete do job-plan, its handler and the tests that tested only it, by deletion table 1

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r4-delete-1.jsonl` | +16 / -0 | the table, copied with `shutil.copyfile`; sha256 `432429e6…0693d13c` equal |
| `apps/cli/command_catalog.py` | +7 / -28 | rows 1–8: the `do.job-plan` entry, its `related=` tuples and argument help |
| `apps/cli/commands/do_cmd.py` | +0 / -76 | rows 9–10: the handler-table entry and `_cmd_do_job_plan` |
| `tests/orchestration/test_f018_authority_integration.py` | +2 / -17 | row 11: the `do job-plan` budget test; the class becomes `TestJobRunBudgetPath` |
| `tests/orchestration/test_job_task_runner.py` | +4 / -15 | rows 12–15 |
| `tests/test_command_catalog.py` | +1 / -0 | row 16: `do.job-plan` joins `TestDeletedCommands.DELETED` |

### 40f449d1 F261 R4 C3: delete do plan, its handler, its CLI tests and its README line, by deletion table 2

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r4-delete-2.jsonl` | +8 / -0 | the table, copied with `shutil.copyfile`; sha256 `1f7856e9…95f730af` equal |
| `README.md` | +0 / -1 | row 7: the `remedy do plan <job-id>` Quickstart line |
| `apps/cli/command_catalog.py` | +0 / -16 | row 1: the `do.plan` entry |
| `apps/cli/commands/do_cmd.py` | +0 / -60 | rows 2–3: the handler-table entry and `_cmd_do_plan` |
| `tests/cli/test_scope_plan.py` | +0 / -71 | rows 4–5: `TestCliPlan` and the now unused `import pytest` |
| `tests/orchestration/test_stream_evidence_integration.py` | +1 / -1 | row 6: the source split now ends at `"do.replan":` |
| `tests/test_command_catalog.py` | +1 / -0 | row 8: `do.plan` joins `TestDeletedCommands.DELETED` |

### C4 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r4w/wt 40f449d1` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r4w/wt checkout -- <file>` (worktree status `''` after each), then removed with `git worktree remove .remedy-wt/f261r4w/wt`; `git worktree list` then read one row |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r4w/`, not committed. Every exit code below is the real return
code of the command as the tool reported it.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `bca20317` | `g1g2.py` 0 | sha256 of `.agent/authored/f261-r4.md` at C0a `87b880f80856d3b1689949ddf050b7940e42a2338d00ca79f7c36732da922083`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical**. Slices FOUND **3** (PLAN4, RECORD4, DEC3), each **matching** its BEGIN-marker sha256. Committed carriers: delete-1 at C2 `432429e655ca22fd98173e095ecf7aec861570ecd2206413a5ef54b60693d13c` **equal**; delete-2 at C3 `1f7856e91a7087e8fdc77a1ce2e894a6ba3d3aa7092578792c71c95f95f730af` **equal** (read by `g3g4.py`) |
| G2 the record | C1 | `g1g2.py` 0 | `plan.md` **equals** PLAN4; **36** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `b8f019de` blob + RECORD4; `decisions.md` **equals** its `b8f019de` blob + DEC3. `^Gate: F\d+ R\d+ — ` **112** → **113**; `Gate: F261 R3 — ` **1** at C1; distinct `^- R-\d+ — ` **96** → **98**; distinct `^Done: R-\d+ — ` **4** → **4**; open by distinct id **92** → **94**; C1 minus base `['R-0894', 'R-0895']`, base minus C1 `[]` |
| G3 deletion 1 | C2 `36eb4573` | `g3g4.py 3` 0 | table 1: all **16** rows matched, each count 1. `--no-renames --name-only` printed exactly the **6** paths. Trees: `apps` `0ff86c0343fb1732a86bb6fdde7a4d8582bf63f6`, `tests` `937a8aed02e7e141c5cb0eedfad624897ebc2f14`, each **match**; `packages` `8acfc00a…`, `scripts` `fb0b7d81…`, `docs` `751ebee3…`, `README.md` `9d94d8b5…` each **equal** base. 30 insertions |
| G4 deletion 2 | C3 `40f449d1` | `g3g4.py 4` 0 | table 2: all **8** rows matched, each count 1. `--no-renames --name-only` printed exactly the **7** paths. Trees: `apps` `f800c1d6d77fe4b9c0adfc74c8d98c5be6d40bd0`, `tests` `ab1cb821a2bae58bac8e089f3dfba4c62277e348`, `README.md` `86ec95f3c4d8b1c47514cc7c7de5fe25510fec47`, each **match**; `packages`, `scripts`, `docs` each **equal** base. Symbol `git grep -w` exit 1, output `''`. `git grep -F` exit 0, exactly **2** lines: `40f449d1:tests/test_command_catalog.py:304:        "do.job-plan",` and `…:305:        "do.plan",`. `git diff --name-only b8f019de 40f449d1 -- docs/roadmap` `''`. `python3 -m ruff check` over the **7** `.py` paths of C2 and C3: exit 0, `All checks passed!`. 10 insertions |
| G5(a) control | worktree at C3 | 0 | both modules loaded from the worktree; `30 passed in 0.36s` |
| G5(b) `"do.plan": lambda args: None,` inserted before `"do.promote": lambda args: _cmd_do_promote(` | same worktree | 1 | FROM count **1**; `1 failed, 29 passed in 0.36s`; failed: `tests/test_command_catalog.py::TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` |
| G5(c) `command_id="job.apply",` → `command_id="do.job-plan",` | same worktree, after `checkout --` | 1 | FROM count **1**; `3 failed, 27 passed in 0.36s`; failed: `tests/test_command_catalog.py::TestCatalogIntegrity::test_command_id_format`, `…::TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler`, `…::TestDeletedCommands::test_no_deleted_id_is_left_in_the_catalog` |
| G6 the suite, SPEC S | primary checkout at C3, serially | 0 | `suite.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18260 passed, 23 skipped, 1 warning in 1330.35s (0:22:10)`; distinct bad nodes **0**; `git status --porcelain` `''` afterwards |
| G7 the tree | after C4 and the push | not yet run | reported in the completion message only |

Open findings: **94** by distinct id, R-0894 (Medium, owner F261) and R-0895 (Low, owner F261) among them. The open High
ids are **R-0803, R-0804, R-0806 and R-0807**.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r4.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN4 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD4, DEC3 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `b8f019de` blob followed by the slice at C1 (G2) |
| deletion table 1 | `.agent/authored/f261-r4-delete-1.jsonl` and its paths | carrier digest **equal**; the C2 trees equal the reviewer's dry run (G3) |
| deletion table 2 | `.agent/authored/f261-r4-delete-2.jsonl` and its paths | carrier digest **equal**; the C3 trees equal the reviewer's dry run (G4) |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically from the COMMITTED
`.agent/authored/f261-r4.md` (read with `git show 2ccc400b:`) and verified against its BEGIN-marker sha256 before use;
each table was verified against its digest before it was copied and applied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN4, RECORD4, DEC3 | done | one commit, the first substantive commit |
| C2 deletion table 1 | done | one commit |
| C3 deletion table 2 | done | one commit |
| C4 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **G1's carrier clause was read at C2 and C3, not after C1.** Constraint 8 places G1 after C1, but the carriers are
   first committed at C2 and C3; their committed digests were read by `g3g4.py` right after each commit, and each source
   carrier's digest was also verified before `shutil.copyfile`.
2. **Each table was validated in memory first.** `.remedy-wt/f261r4w/apply_table.py` reads each path with
   `encoding="utf-8", newline=""`, runs every row strictly in file order against a virtual tree the previous rows left,
   and only after every row passed copies the carrier and performs the rows on disk in the same order. No count
   differed and no target existed.
3. **G5 ran through a runner**, `.remedy-wt/f261r4w/runner.py`, invoked as `python3 -B`: it changes into the worktree,
   puts it first on `sys.path` and in `PYTHONPATH`, sets `PYTHONDONTWRITEBYTECODE`, asserts that
   `apps.cli.command_catalog` and `apps.cli.commands.do_cmd` loaded from inside the worktree, and calls `pytest.main`
   with `-p no:randomly -p no:cacheprovider -rf --tb=no` and the path.
4. **The first STOP reading.** A bare `test -e .agent/STOP` returned without the tool showing an exit code, so the
   reading before C0a was repeated with Python (`exists False`, exit 1) and `ls` (exit 2); the file was absent.
5. **File reading before edits.** The tables were applied programmatically, so instead of reading each target file in
   full I read the staged diff of C2 and of C3 and ran ruff over the touched `.py` files before committing; the tree-id
   gates prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 4.
3. T002: `apply` for `promote`, and `job show --full`.

Operator questions open: 1
