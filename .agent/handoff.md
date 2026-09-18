# Handoff — F270 History apply: one commit per task, merge on demand · Round 3

## Session

SESSION 1 of feature F270 · round 3 · rounds so far 3

Context self-assessment: I read the block, AGENTS.md, T2_F270.md, DECISIONs F270 D1 to D3, R-0975 and R-0976, all of `job_apply.py`, and the prototype diff and test (as references only). I also read the helpers the round reuses. Every figure below comes from a command run in this round.

## Range

Review of 4a615385..HEAD — branch `feature/f270-history-apply`.

## Summary

Round 3 books round 2's FAIL and repairs both of its findings in C2:
- R-0975: three new tests, each reaching one refusal.
- R-0976: the `--commit-with-history` help now uses the vocabulary page's meaning of "task".

The round then builds the `job apply` half of T004 per DECISION F270 D3. The new flags are `remedy job apply <job> --approve --commit "<message>" | --commit-auto [--push]`:
- They copy files exactly as a plain `--approve` does.
- After the post-apply verification and the post-test pass, they land ONE commit of exactly the copied files on the operator's current branch, under the operator's identity, configuration and hooks.
- `--push` then runs `git push --porcelain <remote> <landed sha>:<upstream ref>` to the configured upstream. It is never forced, uses a timeout, and runs with `GIT_TERMINAL_PROMPT=0` and stdin closed.

Refusals:
- The shared checkout refusals now cover a rebase, a cherry-pick and a revert in progress, as well as a merge. They are checked after every existing gate and again right before the first write.
- A clash between the flags, a lone `--push`, and an empty or multi-line `--commit` are refused before the job is read.

The config key `apply.push_after_mission` is registered with its helper. `job apply` never reads it.

## Commits

### 897c9ee4 F270 R3 C1: book round 2's FAIL with R-0975 and R-0976, land DECISION F270 D3 and the round 3 plan, and save the payload and block copies
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f270-r3-block.md` | +115 / -0 | Byte copy of the block |
| `.agent/authored/f270-r3-decisions.md` | +55 / -0 | Byte copy of decisions.md |
| `.agent/authored/f270-r3-ledger.md` | +6 / -0 | Byte copy of ledger.md |
| `.agent/authored/f270-r3-plan.md` | +27 / -0 | Byte copy of plan.md |
| `.agent/authored/f270-r3-slips.md` | +3 / -0 | Byte copy of slips.md |
| `.agent/decisions.md` | +55 / -0 | `4a615385` bytes + decisions.md (DECISION F270 D3) |
| `.agent/live_review.md` | +6 / -0 | `4a615385` bytes + ledger.md (Gate F270 R2 FAIL, R-0975, R-0976) |
| `.agent/plan.md` | +7 / -8 | := plan.md |
| `.agent/prose_slips.md` | +3 / -0 | `4a615385` bytes + slips.md |

277 insertions, 8 deletions (`git show --numstat`).

### 74247dc7 F270 R3 C2: tests reach the diff-hash, merge-in-progress and top-level refusals, and the --commit-with-history help keeps the vocabulary
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +1 / -1 | R-0976: "the job's per-task commits" → "the job's commits, one per applied task step" |
| `tests/orchestration/test_job_apply_history.py` | +54 / -0 | R-0975: h14, h15, h16 |

55 insertions, 1 deletion.

### 63c8b88f F270 R3 C3a: the shared checkout refusals, the --commit, --commit-auto and --push helpers, the shared subject fitter and the apply.push_after_mission key
| Path | +/- | Reason |
|------|-----|--------|
| `docs/system/remedy-toml-configuration-system-v0.md` | +1 / -0 | D3 (7): one row for `apply.push_after_mission` |
| `packages/orchestration/config.py` | +27 / -0 | D3 (7): the key spec and `push_after_mission_enabled` |
| `packages/orchestration/job_apply.py` | +361 / -18 | Result fields; `_history_git(…, env=)`; `_checkout_refusals`; the D3 helper section |
| `packages/orchestration/pingpong_job.py` | +19 / -8 | `fit_commit_subject`; `build_task_commit_message` now calls it, with unchanged output |

408 insertions, 26 deletions.

### 685e6ffe F270 R3 C3b: job apply --approve takes --commit, --commit-auto and --push, commits exactly the copied files as the operator and pushes to the upstream, refusing before anything is written
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +3 / -0 | The `--commit`, `--commit-auto` and `--push` ArgDefs on `job.apply` |
| `apps/cli/commands/do_cmd.py` | +12 / -1 | `_cmd_job_apply` parameters, docstring, pass-through, the `job.apply` handler |
| `packages/orchestration/job_apply.py` | +155 / -37 | The flags through `apply_job`, both refusal checks, the commit, the push, the record, the summary, the preview and the next-step line |

170 insertions, 38 deletions.

### 24aa5bce F270 R3 C4a: tests prove --commit and --commit-auto land one commit of exactly the copied files as the operator, the subject rule, and every flag and checkout refusal changing nothing
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_job_apply_commit.py` | +345 / -0 | Helpers; the classes `TestCommitWithAMessage`, `TestCommitAuto` and `TestFlagRefusals` |

345 insertions, 0 deletions.

### 4051c73b F270 R3 C4b: tests prove one fast-forward push to a bare upstream, the no-upstream and unmet-criterion refusals, a failed push keeping the commit, no commit without a flag, and the config key
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_job_apply_commit.py` | +175 / -0 | The classes `TestPush`, `TestNoCommitWithoutAFlag`, `TestTheConfigKey` and `TestThroughTheCli`, plus the imports they use |

175 insertions, 0 deletions.

### C5 (this commit) F270 R3 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 / -0 | Two `Landed:` lines, for R-0975 and R-0976, each after a blank line |
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C3a, with 408.

## What C3 builds (DECISION F270 D3)

- **(1) The flags**:
  - `commit_flags_refusal(commit_message, commit_auto, commit_with_history, push)` runs in `apply_job` before `load_job_plan`.
  - The three `--commit…` flags are mutually exclusive. `--push` alone is refused. A `--commit` message that is empty, or that holds a line break after stripping, is refused.
  - The reasons are prefixed `commit_refused: ` or `push_refused: ` and read "…, so nothing was applied."
  - `result.commit_message_mode` is `""`, `message`, `auto` or `history`.
- **(2) Checkout refusals**:
  - `_checkout_refusals(target, landing=, what=)` is now shared with `_history_refusals`. The history sentences are byte-identical to round 2's.
  - It refuses a target below its repository's top level (ending the list), a detached `HEAD`, and `MERGE_HEAD`, `CHERRY_PICK_HEAD` or `REVERT_HEAD`. It also refuses when `git rev-parse --git-path rebase-merge|rebase-apply` exists, or when the tree is dirty, naming the paths.
  - `_commit_refusals` adds `git check-ignore -- <planned>` for `--commit` and `--commit-auto`. A staging job is not refused.
  - `_flag_refusals` gathers the refusals of the mode plus, with `--push`, `_push_refusals`. It runs after the mode gate (a preview lists them all) and again after the durable pre-apply record, right before the merge or the copy.
- **(3) The commit**, in `_commit_applied_files`:
  - It runs only after the verification and the post-test pass: `git add -- <copied>`, then `git commit -q --only -m <message> -- <copied>` as the operator.
  - Afterwards `HEAD^` must be the previous tip, and `git diff-tree -r -z` must name no path outside the copied set.
  - A refused commit runs `git restore --staged -- <copied>`, which touches only the index. The status is `blocked` with the reason `commit_failed: <git's words>`.
  - A failed post-test leaves the files copied and uncommitted. The status is `applied_test_failed`, and `blocked_reasons` says `--commit made no commit`.
- **(4) Messages**:
  - `--commit` uses the operator's line (stripped) as the first line.
  - `build_auto_commit_subject` tries the mission's goal, then the job's title. Each is capitalised, fitted by `pingpong_job.fit_commit_subject` (the per-task fitter, extracted) and tested by `commit_subject_problem`: one line, at most 72 characters, at least 3 words, the first word from `COMMIT_AUTO_VERBS`. The fallback is `Apply the <n> tasks of Remedy job <id8>`.
  - `build_apply_commit_message` produces: the subject, then a sentence naming the job, then (for auto) `- <task title>` lines, then the D1 (3) contract line, then `Remedy-Job` and `Co-authored-by: Remedy <remedy@local>`.
- **(5) Push**:
  - `_push_refusals` refuses no upstream, with the sentence naming `git push --set-upstream <remote> <branch>`. It also refuses an upstream `.` (a local branch), an unreadable contract, and `contract_blockers` non-empty over the whole mission, where an `open` criterion counts as not met.
  - `_push_landed_commit` pushes the landed sha (the commit, or the merge commit of `--commit-with-history`) and records the outcome. A failed push sets status `applied_push_failed` with git's words, and the summary says to push by hand.
- **(6) The record**: gains `commit_message_mode`, `commit_sha`, `push`, `pushed`, `push_remote` (the name, or `(not a named remote)`), `push_ref` and `push_error`.
- **(7) The key**: `apply.push_after_mission` is a bool, defaults to false and reads env `REMEDY_APPLY_PUSH_AFTER_MISSION`. `push_after_mission_enabled(config)` reads a bool as it is, and a string as true only for `1`, `true` or `yes`. Nothing in `job apply` calls it.
- **Not touched**: `do.run`'s own flags and `_DO_FLAGS_NOT_YET_AVAILABLE`.
- **Parse probe**: `job apply abc --commit ""` reaches the empty-message refusal, and `--commit-with` still exits 2, so the new flags open no abbreviation.

## External actions

- C3a check: I added a disposable worktree `.remedy-wt/f270-r3-c3a` at `63c8b88f`, ran the apply, history, worktree-integration and config test files there (`204 passed`), and removed it with `git worktree remove --force`.
- G4: I added `.remedy-wt/f270-r3-g4` at `4051c73b` and then removed it with `git worktree remove --force`. `git worktree list` afterwards shows only `/home/decodeux/Repos/remedy  4051c73b [feature/f270-history-apply]`.
- After this commit: `git push origin feature/f270-history-apply`, never forced. No pull request is opened this round.
- No evidence job and no zip.

## Verification

G1 to G4 ran at C4b (`4051c73b`), before this commit.

- **G1**: `python3 .remedy-wt/f270-r3/g1.py`, exit 0:
  ```
  True digest ledger.md
  True digest decisions.md
  True digest slips.md
  True digest plan.md
  True digest block.md
  True plan.md == payload
  True .agent/live_review.md == base + ledger.md
  True .agent/decisions.md == base + decisions.md
  True .agent/prose_slips.md == base + slips.md
  True copy f270-r3-ledger.md
  True copy f270-r3-decisions.md
  True copy f270-r3-slips.md
  True copy f270-r3-plan.md
  True copy f270-r3-block.md
  block copy sha256 9e0aad21bfa6c86d9436bd72b94767e85d71f4707851119ce527cb73ff156175
  ALL True 14
  ```
- **G2**: the block's 23-path list, with `tests/orchestration/test_job_apply_commit.py` first, run serially in the primary checkout. Both test files this round edited are on the list. Command: `python3 -m pytest -q -p no:cacheprovider …`, exit 0: `1197 passed in 231.93s (0:03:51)`. The reviewer's base reading was 1135 passed and 1 failed. 1197 = 1136 + 3 (h14 to h16) + 58 (the new file). R-0976's node now passes.
- **G3**: `python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/do_cmd.py packages/orchestration/config.py packages/orchestration/job_apply.py packages/orchestration/pingpong_job.py tests/orchestration/test_job_apply_commit.py tests/orchestration/test_job_apply_history.py` (every `.py` file in `git diff --name-only 897c9ee4..4051c73b`), exit 0: `All checks passed!`
- **G4**: `python3 .remedy-wt/f270-r3/g4.py`, exit 0.
  - It used ONE worktree, `.remedy-wt/f270-r3-g4` at `4051c73b`. Before each run it purged `__pycache__`, and it ran `python3 -B -m pytest -p no:cacheprovider tests/orchestration/test_job_apply_history.py tests/orchestration/test_job_apply_commit.py` from the worktree root.
  - Every run printed the imported module as `/home/decodeux/Repos/remedy/.remedy-wt/f270-r3-g4/packages/orchestration/job_apply.py`.
  - Each FROM is whole lines and matched exactly once. Each mutation was restored to the original bytes and asserted equal, and the script ends with `reverted: True`.
  - Ids are under `tests/orchestration/`.

  | Run | Change | Result | Failing tests |
  |-----|--------|--------|---------------|
  | control | none | exit 0, `76 passed` | none |
  | (a) | the diff-hash `if` → `if False:` | exit 1, `1 failed, 75 passed` | `test_job_apply_history.py::TestRefusals::test_h14_a_tip_at_the_recorded_head_whose_tree_is_not_the_reviewed_diff_is_refused` |
  | (b) | the `MERGE_HEAD` refusal `if` → `if False:` | exit 1, `1 failed, 75 passed` | `test_job_apply_history.py::TestRefusals::test_h15_the_operators_own_conflicted_merge_is_refused_and_left_untouched` |
  | (c) | the top-level `if` → `if False:` | exit 1, `1 failed, 75 passed` | `test_job_apply_history.py::TestRefusals::test_h16_a_subdirectory_of_a_repository_is_refused` |
  | (d) | `if len(given) > 1:` → `if False:` | exit 1, `9 failed, 67 passed` | `test_job_apply_commit.py::TestFlagRefusals::test_f1_the_commit_flags_clash` ×8 (all parameters), `test_job_apply_commit.py::TestThroughTheCli::test_a_clash_is_a_blocked_apply_and_a_commit_lands` |
  | (e) | `elif dirty:` → `elif False:` | exit 1, `6 failed, 70 passed` | history `test_h3_…`, `test_h4_…`, `TestThroughTheCli::test_a_refused_…`; commit `test_f4_…[mode0]`, `test_f4_…[mode1]`, `test_f8_the_preview_names_every_refusal_and_the_command` |
  | (f) | `if stray:` → `if False:` | exit 1, `1 failed, 75 passed` | `test_job_apply_commit.py::TestCommitWithAMessage::test_c4_a_commit_touching_a_path_remedy_did_not_copy_is_reported` |
  | (g) | the no-upstream `if` → `if False:` | exit 1, `2 failed, 74 passed` | `test_job_apply_commit.py::TestFlagRefusals::test_f8_…`, `test_job_apply_commit.py::TestPush::test_p4_no_upstream_is_refused_naming_the_command` |
  | (h) | `if blockers:` → `if False:` | exit 1, `2 failed, 74 passed` | `test_job_apply_commit.py::TestPush::test_p5_a_blocking_criterion_not_met_is_refused_before_anything[open]`, `…[unmet]` |
  | (i) | `"--force"` added to the push argv | exit 1, `1 failed, 75 passed` | `test_job_apply_commit.py::TestPush::test_p2_the_push_argv_names_the_upstream_and_no_force` |
  | (j) | the commit condition widened to `("", "message", "auto")` | exit 1, `4 failed, 72 passed` | history `TestPlainApproveIsUnchanged::test_h8_…`, `TestRefusals::test_h7_…[False]`; commit `TestNoCommitWithoutAFlag::test_n1_plain_approve_commits_and_pushes_nothing[False]`, `…[True]` |

  No mutation stayed green.
- **Full suite**: not run (amend0917-throughput).

## Authored-text proofs

- `.agent/authored/f270-r3-{ledger.md,decisions.md,slips.md,plan.md,block.md}` equal their payloads byte for byte, and all five went in C1 (G1).
- The block copy's sha256 is `9e0aad21bfa6c86d9436bd72b94767e85d71f4707851119ce527cb73ff156175`, the digest the orchestrator named.
- `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` at C1 are their `4a615385` bytes with ledger.md, decisions.md and slips.md appended. `.agent/plan.md` is plan.md (G1). C5 then appends the two `Landed:` lines to `.agent/live_review.md`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `897c9ee4`, the block copy included |
| R-0975 | done | `74247dc7`: h14, h15, h16; red at G4 (a), (b), (c) |
| R-0976 | done | `74247dc7`; `tests/docs/` green in G2 |
| C3 D3 (1)–(7) | deviated | Split into C3a `63c8b88f` and C3b `685e6ffe` (the block allows it over 500 lines) |
| C4 tests | deviated | Split into C4a `24aa5bce` and C4b `4051c73b` (the block allows it over 500 lines) |
| C5 handoff and push | done | This commit, then the push |
| G1–G4 | done | All exit 0; every mutation red |

## Open findings

`python3 .remedy-wt/f268-r4/count.py` (by distinct id) at `4051c73b` reads `HEAD registrations 133 done 4 open 129`. The count rose from 127 by R-0975 and R-0976. This round lands both (`Landed:`, never `Done:`), so both stay open until the reviewer's verdict.

## Deviations & assumptions

- **Commit sequence**: the order was C1, C2, C3a, C3b, C4a, C4b, C5, then the push.
  - C3 would have inserted 578 lines and C4 520, so each was split as the block allows.
  - C3a holds only additions that nothing calls yet: the helpers, the fields, the shared refusals, the fitter and the key. C3b holds the wiring. I staged C3a's five `job_apply.py` hunks with `git apply --cached` from a filtered patch. The staged blob compiled and passed ruff, and a worktree at `63c8b88f` read `204 passed` over the apply, history, worktree-integration and config test files.
  - C4a is the new test file cut before `class TestPush:`, without the two imports only C4b uses. C4b restores the final bytes.
- **Capitalised first letter**: `--commit-auto` capitalises the first letter of the mission's goal or the job's title before the rule tests it. The verb list is capitalised, and a goal such as "add the contact page" would otherwise always fall through to the fixed sentence. D3 (4) does not say whether the candidate may be capitalised.
- **Surrounding whitespace**: the `--commit` line is used with it stripped (D3 (4) says "unchanged"). git's own cleanup would strip trailing whitespace anyway, and an all-blank message counts as empty.
- **The auto body**: the job sentence comes before the task-title lines. D3 (4) gives no order, and the contract line stays the last body line.
- **`git commit --only -- <copied>`**: I used this rather than a plain commit, so an index entry staged outside the copy cannot slip in. A `pre-commit` hook that stages another file does reach the commit, and c4 measures that the stray-path check reports it: the status is `blocked`, `commit_sha` is recorded, and the summary names `git reset --keep <previous tip>`. Remedy moves no branch.
- **`push_remote`**: a `branch.<b>.remote` that is not a named remote (a URL written directly into the config) is recorded as `(not a named remote)`, and the push is not attempted. This keeps D3 (6)'s "never its URL". D3 does not name the case.
- **The `commit_sha` of a history merge**: it is set to the merge commit, so `--commit-with-history --push` pushes it. p3 measures one push.
- **`_history_git` gained `env=`**: when it is given, stdin is `DEVNULL`. Only the push passes it, with `GIT_TERMINAL_PROMPT=0`. Every other call is unchanged.
- **The late re-check for `--commit-with-history`**: it is now `_flag_refusals`, whose history entries carry the same `history_merge_refused: ` prefix and position as round 2's. It extends `blocked_reasons` with every late refusal rather than only the first.
- **Scratch scripts**: `.remedy-wt/f270-r3/{digests,c1_build,parse_probe,split_c3,check_staged,split_c4,restore_c4,g1,g4,c5_landed}.py` are gitignored.

## Next

Phase 1 rule 1 (`.agent/STOP`), then the review of round 3.

Operator questions open: 5
