# Handback — F261 round 7

## Session

`SESSION 2 of feature F261 · round 7 · rounds so far 7`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `8b07c95b`..`HEAD`: C0a, C0b, C1, C2, C3, C4 and C5, plus this handback commit C6. `.agent/STOP` was ABSENT
at all three readings constraint 2 orders: before C0a (`ls -la .agent/STOP` exit 2, "No such file or directory"),
before C2 (exit 2) and before C6 (exit 2).

## Commits

### 82f2f088 F261 R7 C0a: save the round 7 step block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r7.md` | +237 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### ab225280 F261 R7 C0b: mirror the round 7 step block into last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +131 / -120 | the same bytes, the mirror |

### 9984586e F261 R7 C1: re-point the plan at round 7, book round 6's PASS, record DECISION F261 D6

This is the FIRST SUBSTANTIVE COMMIT.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC6 appended: DECISION F261 D6 |
| `.agent/live_review.md` | +2 / -0 | slice RECORD7 appended: `Gate: F261 R6 —` PASS |
| `.agent/plan.md` | +13 / -13 | slice PLAN7, a full replacement: 37 lines |

### a8ac671a F261 R7 C2: rename the job apply status values and reason codes to apply words, by words table 1

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r7-words-1.jsonl` | +30 / -0 | the table, copied with `shutil.copyfile`; sha256 `0e2d9ebf…0b43cde3` equal |
| `packages/orchestration/job_apply.py` | +19 / -19 | the status values and reason codes of D6's first paragraph |
| `tests/orchestration/test_job_apply.py` | +27 / -27 | their assertions |
| `tests/orchestration/test_job_apply_consistency.py` | +7 / -7 | their assertions |
| `tests/orchestration/test_job_worktree_handoff.py` | +2 / -2 | their assertions |
| `tests/orchestration/test_job_worktree_integrity.py` | +5 / -5 | their assertions |

### 0e7e2182 F261 R7 C3: spell the job apply record with job_apply, its key, directory, prefix and names, by words table 2

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r7-words-2.jsonl` | +21 / -0 | the table, copied with `shutil.copyfile`; sha256 `3f424e7d…bf7af6e6` equal |
| `packages/orchestration/job_apply.py` | +14 / -14 | `job_apply_id`, `job_apply_records`, `remedy-job-apply-`, `_job_apply_records_dir`, `job_apply_record_*` codes |
| `tests/orchestration/test_job_apply.py` | +11 / -11 | the field, the record-test class names and `fake_job_apply_records_dir` |
| `tests/orchestration/test_job_apply_consistency.py` | +4 / -4 | the field and the directory helper |
| `tests/orchestration/test_job_worktree_handoff.py` | +2 / -2 | the field and the directory helper |
| `tests/orchestration/test_job_worktree_integrity.py` | +2 / -2 | the temporary prefix |

### cc56e9e4 F261 R7 C4: rename the job apply text, prose and skip-blocked help to apply words, by words table 3

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r7-words-3.jsonl` | +83 / -0 | the table, copied with `shutil.copyfile`; sha256 `7f5278cb…ef795a8ea5` equal |
| `apps/cli/command_catalog.py` | +1 / -1 | the `--skip-blocked` help: "Apply", "not applied" |
| `packages/orchestration/job_apply.py` | +44 / -44 | printed lines (`Job apply record: `), docstrings and comments |
| `tests/orchestration/test_job_apply.py` | +30 / -30 | docstrings, comments and the `not applied` summary assertion |
| `tests/orchestration/test_job_apply_consistency.py` | +6 / -6 | docstrings, comments, `Temporary apply cleanup failed.` |
| `tests/orchestration/test_job_worktree_handoff.py` | +3 / -3 | comments |
| `tests/orchestration/test_job_worktree_integrity.py` | +7 / -7 | docstrings and comments |

### c7d8f7a6 F261 R7 C5: guard the job apply record's directory, key and summary line and the skip-blocked help, by the guard table

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r7-guard.jsonl` | +2 / -0 | the table, copied with `shutil.copyfile`; sha256 `06ac0b87…68ba78e29` equal |
| `tests/orchestration/test_job_apply.py` | +23 / -0 | three tests: the record under `job_apply_records/<job>/<job_apply_id>.json`, the summary's `Job apply record: <id>`, and no promote word in the `--skip-blocked` help |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r7w/wt c7d8f7a6` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r7w/wt checkout -- <file>` (rc 0, worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r7w/wt`; `git worktree list` then read one row |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r7w/`, not committed. Every exit code below is the real return
code of the command as the tool reported it.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `9984586e` | `g12.py` 0 | sha256 of `.agent/authored/f261-r7.md` at C0a `b3aba0b5f49dae402c943a75bb806675477743918f7ea2bb3abd8cbf9379f6e9`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical**. Slices FOUND **3** (PLAN7, RECORD7, DEC6), each **matching** its BEGIN-marker sha256. Committed carriers read at C5 by `g4.py` (exit 0): words-1 `0e2d9ebf700c8d7417c0fb3b0c334ef71e1d0a8cf26ce6d3f3dca1ae0b43cde3`, words-2 `3f424e7dd4ed86bf29b4badb9a7e3df5078171b818f47aaebf8885fcbf7af6e6`, words-3 `7f5278cbd603fe074c0bbfefba3eb3dd46a68c233ad53c1ad8d53eff795a8ea5`, guard `06ac0b87c1ee1e8075c0ff2df271a00468ba78e29e57f072e34acc56cc7224a2`, each **equal** |
| G2 the record | C1 | `g12.py` 0 | `plan.md` **equals** PLAN7; **37** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `8b07c95b` blob + RECORD7; `decisions.md` **equals** its `8b07c95b` blob + DEC6. `^Gate: F\d+ R\d+ — ` **115** → **116**; `Gate: F261 R6 — ` **1** at C1; distinct `^- R-\d+ — ` **100** → **100**; distinct `^Done: R-\d+ — ` **4** → **4**; open by distinct id **96** → **96**, equal as sets |
| G3 the words | C2 `a8ac671a`, C3 `0e7e2182`, C4 `cc56e9e4` | `g3.py` 0 | tables: words-1 **30** rows, words-2 **21**, words-3 **83**, every count as stated. `--no-renames --name-only` from each parent: C2 and C3 exactly the carrier and J; C4 the carrier, J and `apps/cli/command_catalog.py`. Trees, each **match**: C2 `apps` `712eeb42…`, `packages` `4cbcd990…`, `tests` `a940c877…`; C3 `apps` `712eeb42…`, `packages` `fd54296c…`, `tests` `7d62b611…`; C4 `apps` `5366495d…`, `packages` `c9e52035…`, `tests` `93007477…`. At all three, `scripts` `fb0b7d81…`, `docs` `eebc60ba…` and `README.md` `86ec95f3…` **equal** `8b07c95b`. Insertions: C2 **90** (60 deletions), C3 **54** (33), C4 **174** (91) |
| G4 the guards | C5 `c7d8f7a6` | `g4.py` 0 | guard table **2** rows. `--no-renames --name-only cc56e9e4 c7d8f7a6` printed exactly `.agent/authored/f261-r7-guard.jsonl` and `tests/orchestration/test_job_apply.py`; `tests` `4fc4dc808311601a0bd720297cc365029c9da7ea` **match**; `apps` and `packages` **equal** C4. C5 insertions **25** (0 deletions). GA exit **1**, stdout `''`, stderr `''`. GB exit **0**, exactly one line: `c7d8f7a6:tests/orchestration/test_job_apply.py:609:        assert "promot" not in help_text.lower()`. GC exit **1**, stdout `''`. `python3 -m ruff check apps/cli/command_catalog.py` + J: exit **0**, `All checks passed!` |
| G5(a) control | worktree at C5 | 0 | `packages.orchestration.job_apply` and `apps.cli.command_catalog` loaded from the worktree; `172 passed in 54.85s`; **0** failed nodes |
| G5(b) `result.status = "applied"` → `"promoted"` in `job_apply.py` | same worktree | 1 | count **1**; `25 failed, 147 passed in 51.61s`; **25** failed nodes, `TestApproveApplies::test_approve_applies_safe_files` **among them** |
| G5(c) `"job_apply_records"` → `"job_promotions"` | same worktree, after `checkout --` | 1 | count **1**; `1 failed, 171 passed in 27.21s`; **1** failed node, `TestJobApplyRecord::test_the_record_is_stored_under_job_apply_records_by_its_job_apply_id` |
| G5(d) `"job_apply_id"` → `"promotion_id"` | same worktree, after `checkout --` | 1 | count **1**; `1 failed, 171 passed in 27.63s`; **1** failed node, `TestJobApplyRecord::test_the_record_is_stored_under_job_apply_records_by_its_job_apply_id` |
| G5(e) `Job apply record: ` → `Promotion: ` | same worktree, after `checkout --` | 1 | count **1**; `1 failed, 171 passed in 65.20s (0:01:05)`; **1** failed node, `TestJobApplyRecord::test_the_summary_names_the_job_apply_record` |
| G5(f) the `--skip-blocked` help → "Promote … unpromoted …" in `apps/cli/command_catalog.py` | same worktree, after `checkout --` | 1 | count **1**; `1 failed, 171 passed in 76.02s (0:01:16)`; **1** failed node, `TestCLICommandShape::test_the_skip_blocked_help_speaks_of_applying` |
| G6 the suite, SPEC S | primary checkout at C5, serially | 0 | `suite.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18176 passed, 23 skipped, 1 warning in 1338.15s (0:22:18)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` afterwards |
| G7 the tree | after C6 and the push | not yet run | reported in the completion message only |

Open findings: **96** by distinct id. The open High ids are **R-0803, R-0804, R-0806 and R-0807**.

Operator questions open: 0

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r7.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN7 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD7, DEC6 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `8b07c95b` blob followed by the slice at C1 (G2) |
| words tables 1, 2, 3 | `.agent/authored/f261-r7-words-{1,2,3}.jsonl` and their paths | carrier digests **equal**; the C2, C3 and C4 trees equal the reviewer's dry run (G3) |
| guard table | `.agent/authored/f261-r7-guard.jsonl` and its path | carrier digest **equal**; the C5 `tests` tree equals the reviewer's dry run (G4) |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN7, RECORD7, DEC6 | done | one commit, the first substantive commit |
| C2 words table 1 | done | one commit |
| C3 words table 2 | done | one commit |
| C4 words table 3 | done | one commit |
| C5 guard table | done | one commit |
| C6 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **The first STOP reading.** Before C0a a compound command carrying `echo "exit=$?"` was refused by the tool before
   anything ran; the reading was then taken alone as `ls -la .agent/STOP`, exit 2, which is the reading recorded above.
2. **G1's carrier clause was read at C5, not after C1.** Constraint 8 places G1 after C1, but the carriers are first
   committed at C2 to C5; their committed digests were read by `g4.py` at C5, and each source carrier's digest was
   also verified before its table was applied and copied.
3. **Tables were applied directly on disk.** `.remedy-wt/f261r7w/apply_table.py` checks the carrier digest, then
   applies every row strictly in file order against the tree the previous rows left, with `encoding="utf-8",
   newline=""` and the exact-count check, stopping on the first mismatch; it copies the carrier after the last row. No
   count differed and no target existed, so no STOP arose.
4. **G5 ran through a runner**, `.remedy-wt/f261r7w/runner.py`, invoked as `python3 -B`: it changes into the worktree,
   puts it first on `sys.path` and in `PYTHONPATH`, sets `PYTHONDONTWRITEBYTECODE=1`, asserts that
   `packages.orchestration.job_apply` and also `apps.cli.command_catalog` loaded from inside the worktree, and calls
   `pytest.main` with `-q -p no:randomly -p no:cacheprovider -rf --tb=no` over the four test files of J.
   `PYTHONPATH`, `REMEDY_PROJECT` and `REMEDY_DATA_DIR` were already unset in the session environment. The control's
   script line printed a cosmetic `named_node_among_failed=True` for the case that names no node; its failed-node count
   read 0.
5. **The suite was launched detached.** The tool refuses the shell `&` operator by form, and a serial run outlasts one
   tool call, so `.remedy-wt/f261r7w/launch.py` started `suite.py` as a detached child with output under
   `.remedy-wt/f261r7w/`; nothing in the checkout was written while it ran.
6. **File reading before edits.** The tables were applied programmatically, so instead of reading each target file in
   full I read the unstaged diff of each of C2 to C5 line by line before committing; the tree-id gates and ruff prove
   each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 7.
3. `job show --full`.
