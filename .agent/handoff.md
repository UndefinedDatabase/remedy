# Handback — F261 round 6

## Session

`SESSION 2 of feature F261 · round 6 · rounds so far 6`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `a1c42d72`..`HEAD`: C0a, C0b, C1, C2 and C3, plus this handback commit C4. `.agent/STOP` was ABSENT at all
three readings constraint 2 orders: before C0a (`ls .agent/STOP` exit 2, "No such file or directory"), before C2
(`ls .agent/STOP` exit 2) and before C4 (`ls .agent/STOP` exit 2).

## Commits

### 2e6cc882 F261 R6 C0a: save the round 6 step block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r6.md` | +226 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### c3c39002 F261 R6 C0b: mirror the round 6 step block into last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +119 / -130 | the same bytes, the mirror |

### 7f94f581 F261 R6 C1: re-point the plan at round 6, book round 5's PASS, record DECISION F261 D5

This is the FIRST SUBSTANTIVE COMMIT.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC5 appended: DECISION F261 D5 |
| `.agent/live_review.md` | +2 / -0 | slice RECORD6 appended: `Gate: F261 R5 —` PASS, byte-identical to the handoff paragraph at `a1c42d72` |
| `.agent/plan.md` | +13 / -11 | slice PLAN6, a full replacement: 37 lines |

### dd3e1f3e F261 R6 C2: rename job_promote.py to job_apply.py with its two test files, by rename table 1

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r6-rename-1.jsonl` | +30 / -0 | the table, copied with `shutil.copyfile`; sha256 `04842b38…31da4a1` equal |
| `apps/cli/commands/do_cmd.py` | +1 / -1 | row 4: the module import of `_cmd_job_apply` |
| `packages/orchestration/{job_promote.py => job_apply.py}` | +0 / -0 | row 1: the move, content unchanged |
| `packages/orchestration/self_use_job.py` | +1 / -1 | row 5: the `:mod:` reference |
| `packages/orchestration/self_use_runner.py` | +1 / -1 | row 6: the `:mod:` reference |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -1 | rows 7–8: the allowlist line, re-sorted |
| `tests/orchestration/{test_job_promote.py => test_job_apply.py}` | +86 / -86 | row 2 the move; rows 9–18 the imports, `patch` and `__import__` targets, alias `jp_mod` |
| `tests/orchestration/{test_job_promote_consistency.py => test_job_apply_consistency.py}` | +19 / -19 | row 3 the move; rows 19–22 the imports and alias `JP` |
| `tests/orchestration/test_job_worktree_handoff.py` | +4 / -4 | rows 23–26 |
| `tests/orchestration/test_job_worktree_integrity.py` | +10 / -10 | rows 27–30 |

### fa5a9990 F261 R6 C3: rename the job_apply.py identifiers to apply words, by rename table 2

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r6-rename-2.jsonl` | +74 / -0 | the table, copied with `shutil.copyfile`; sha256 `3602beb2…718fd5e` equal |
| `apps/cli/commands/do_cmd.py` | +6 / -6 | rows 18–21: the three imported names, re-sorted |
| `packages/orchestration/job_apply.py` | +54 / -54 | rows 1–17: the D5 name map of the module |
| `tests/orchestration/test_job_apply.py` | +193 / -193 | rows 22–46 |
| `tests/orchestration/test_job_apply_consistency.py` | +52 / -52 | rows 47–56 |
| `tests/orchestration/test_job_worktree_handoff.py` | +20 / -20 | rows 57–63 |
| `tests/orchestration/test_job_worktree_integrity.py` | +23 / -23 | rows 64–74 |

### C4 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r6w/wt fa5a9990` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r6w/wt checkout -- <file>` (worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r6w/wt`; `git worktree list` then read one row |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r6w/`, not committed. Every exit code below is the real return
code of the command as the tool reported it.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `7f94f581` | `g1g2.py` 0 | sha256 of `.agent/authored/f261-r6.md` at C0a `58db64d509ba6eac939675876843a0160c59b651eee94d70399317b4d68e8461`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical**. Slices FOUND **3** (PLAN6, RECORD6, DEC5), each **matching** its BEGIN-marker sha256. Committed carriers: rename-1 at C2 `04842b38d640455bbef9e1edd7fe960f75e240fbc1ea516ae2fd0e84231da4a1` **equal**; rename-2 at C3 `3602beb201f683ddd57f9b708c9ba79c6568929e34213d32c7f06c622718fd5e` **equal** (read by `g3g4.py`) |
| G2 the record | C1 | `g1g2.py` 0 | `plan.md` **equals** PLAN6; **37** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `a1c42d72` blob + RECORD6; `decisions.md` **equals** its `a1c42d72` blob + DEC5. `^Gate: F\d+ R\d+ — ` **114** → **115**; `Gate: F261 R5 — ` **1** at C1; distinct `^- R-\d+ — ` **100** → **100**; distinct `^Done: R-\d+ — ` **4** → **4**; open by distinct id **96** → **96**, equal as sets |
| G3 the module rename | C2 `dd3e1f3e` | `g3g4.py 3` 0 | table 1: all **30** rows valid (3 moves, 27 edits, every count as stated). `--no-renames --name-only 7f94f581 dd3e1f3e` printed exactly the carrier and the **12** paths. Trees: `apps` `4d544c9018a1423edad5152f697fde4ea93c40d7`, `packages` `a53510630e15c346742f9a70a07dfa5376e5a08d`, `tests` `a4e7f6554bc2ea064d727d0a4f197f6ecfbf106e`, each **match**; `scripts` `fb0b7d81…`, `docs` `eebc60ba…` and `README.md` `86ec95f3…` each **equal** `a1c42d72`. **153** insertions, 123 deletions |
| G4 the identifiers | C3 `fa5a9990` | `g3g4.py 4` 0 | table 2: all **74** rows valid (74 edits). `--no-renames --name-only dd3e1f3e fa5a9990` printed exactly the carrier and the **6** paths. Trees: `apps` `712eeb42e83fb80f3135dc818661dd9d551255c0`, `packages` `da8dbf9ba8526212d6ad8bbf928e79b82eab9df9`, `tests` `637383130e627f15f94e476a539bcd2cb47519fe`, each **match**; `scripts`, `docs`, `README.md` each **equal** `a1c42d72`. **422** insertions, 348 deletions. Symbol `git grep -n -I -w` (17 words) exit **1**, output `''`; `git grep -n -I -e job_promote` exit **1**, output `''`. `python3 -m ruff check` over the **8** `.py` paths of C2 and C3 that exist at C3: exit 0, `All checks passed!` |
| G5(a) control | worktree at C3 | 0 | `packages.orchestration.job_apply` loaded from the worktree; `85 passed in 10.79s` |
| G5(b) `from packages.orchestration.job_apply import (` → `…job_promote import (` in `apps/cli/commands/do_cmd.py` | same worktree | 1 | FROM count **1**; `14 failed, 71 passed in 9.69s`; **14** failed nodes, `tests/orchestration/test_job_apply.py::TestCLICommandShape::test_cli_dry_run_json` **among them** |
| G5(c) `def apply_job(` → `def promote_job(` in `packages/orchestration/job_apply.py` | same worktree, after `checkout --` | 1 | FROM count **1**; `74 failed, 11 passed in 9.68s`; **74** failed nodes, `tests/orchestration/test_job_apply.py::TestDryRunCompleted::test_completed_job_dry_run_ready` **among them** |
| G6 the suite, SPEC S | primary checkout at C3, serially | 0 | `suite.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18173 passed, 23 skipped, 1 warning in 1329.82s (0:22:09)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` afterwards |
| G7 the tree | after C4 and the push | not yet run | reported in the completion message only |

Open findings: **96** by distinct id. The open High ids are **R-0803, R-0804, R-0806 and R-0807**.

Operator questions open: 1

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r6.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN6 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD6, DEC5 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `a1c42d72` blob followed by the slice at C1 (G2); RECORD6 also **equal** to one empty line, the `Gate: F261 R5 — ` paragraph of `.agent/handoff.md` at `a1c42d72` and its newline |
| rename table 1 | `.agent/authored/f261-r6-rename-1.jsonl` and its paths | carrier digest **equal**; the C2 trees equal the reviewer's dry run (G3) |
| rename table 2 | `.agent/authored/f261-r6-rename-2.jsonl` and its paths | carrier digest **equal**; the C3 trees equal the reviewer's dry run (G4) |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically from the COMMITTED
`.agent/authored/f261-r6.md` (read with `git show 2e6cc882:`) and verified against its BEGIN-marker sha256 before use;
each table was verified against its digest before it was copied and applied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN6, RECORD6, DEC5 | done | one commit, the first substantive commit |
| C2 rename table 1 | done | one commit |
| C3 rename table 2 | done | one commit |
| C4 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **Constraint 4, a directory listing.** While probing the block directory before C0a, one `ls -la` also listed the
   top level of `.remedy-wt/` itself; no file there outside `.remedy-wt/f261-block/` and `.remedy-wt/f261r6w/` was opened.
2. **The first STOP reading.** Before C0a a `test -e .agent/STOP` ran first, but the tool did not show its exit code
   plainly, so it was repeated as `ls .agent/STOP`, exit 2; that is the reading recorded above.
3. **G1's carrier clause was read at C2 and C3, not after C1.** Constraint 8 places G1 after C1, but the carriers are
   first committed at C2 and C3; their committed digests were read by `g3g4.py` right after each commit, and each source
   carrier's digest was also verified before `shutil.copyfile`.
4. **Each table was validated in memory first.** `.remedy-wt/f261r6w/apply_table.py` reads each path with
   `encoding="utf-8", newline=""`, runs every row strictly in file order against a virtual tree the previous rows left,
   and only after every row passed copies the carrier and performs the rows on disk in the same order, re-checking each
   count. No count differed and no move target existed.
5. **G4 ran three times.** The first run passed `HEAD` as the C3 revision (exit 0, every check OK); a second passed
   `fa5a9990` but was piped into `tail`, hiding its exit code; a third passed `fa5a9990` unpiped with output to a file,
   exit 0. The readings were identical in all three.
6. **G4's ruff clause.** Three `.py` paths of C2, `packages/orchestration/job_promote.py`,
   `tests/orchestration/test_job_promote.py` and `tests/orchestration/test_job_promote_consistency.py`, do not exist at
   C3, so ruff ran over the 8 that do; ruff also ran over the same paths before each of C2 and C3, exit 0 each time.
7. **G5 ran through a runner**, `.remedy-wt/f261r6w/runner.py`, invoked as `python3 -B`: it changes into the worktree,
   puts it first on `sys.path` and in `PYTHONPATH`, also removes `REMEDY_PROJECT` and `REMEDY_DATA_DIR` and sets
   `PYTHONDONTWRITEBYTECODE=1`, asserts that `packages.orchestration.job_apply` loaded from inside the worktree, and
   calls `pytest.main` with `-p no:randomly -p no:cacheprovider -rf --tb=no tests/orchestration/test_job_apply.py`.
   Each mutation was made by `.remedy-wt/f261r6w/mutate.py`, which requires the FROM count to read 1.
8. **File reading before edits.** The tables were applied programmatically, so instead of reading each target file in
   full I read the staged diff of C2 and of C3 (including every changed test line that carries a string literal, which
   are only `patch`, `monkeypatch.setattr` and `__import__` targets) and ran ruff over the touched `.py` files before
   committing; the tree-id gates prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 6.
3. The output-visible promote words of `job_apply.py`.

Operator questions open: 1
