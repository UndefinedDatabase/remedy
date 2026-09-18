# Handoff — F270 History apply: one commit per task, merge on demand · Round 4

## Session

SESSION 1 of feature F270 · round 4 · rounds so far 4

Context self-assessment: I read the block, AGENTS.md, T2_F270.md, DECISIONs F270 D1 to D4 and F268 D12, all of `do_sequence.py` and `job_apply.py`, the `do` handler, and the prototype diff and test (as references only); every figure below comes from a command run in this round, and my context held all of it without loss.

## Range

Review of 8e9c2fad..HEAD — branch `feature/f270-history-apply`.

## Summary

Round 4 books round 3's PASS (R-0975 and R-0976 `Done:`), registers R-0977 for F273, lands DECISION F270 D4 and its operator question Q6, and builds the `do` half of T004:
- `remedy do` takes `--commit "<message>"`, `--commit-auto`, `--commit-with-history` and `--push` with `job apply`'s rules; each commit flag implies `--apply`. `_DO_FLAGS_NOT_YET_AVAILABLE` and its refusal function are deleted.
- Before any step, and exiting 2 with "Nothing was run.": a flag clash, a lone `--push`, an empty or multi-line `--commit`, a commit flag with `--plan-only`, the checkout refusals (top level of the target), and with a push the upstream refusals.
- Under a commit flag no job waits: the run step applies and commits (or merges) each job but the last before the next job's worktree is cut; the apply step applies the last. `--commit` gains ` (job <k> of <n>)` in a walk of several jobs; `--commit-auto` then asks each job's title before the mission's goal.
- The apply step never passes `push` to `apply_job`. After the last job, `do` asks the upstream and contract refusals again and pushes the last landed commit ONCE through `job_apply.push_to_upstream`, never forced.
- `apply.push_after_mission` with a commit flag pushes as `--push` would; without one `do` commits and pushes nothing and prints one sentence on stderr.
- D4 (6), for `do` and `job apply` alike: only an `unmet` blocking criterion refuses a push; each one still `open` is named in the output and the record (`push_open_criteria` in the apply record, `open_blocking_criteria` in `do --json`'s `push`). A single-job `do` is refused before anything is applied; a chained walk lands its commits and the push is refused.
- `do --json` gains `landed` and `push`.

## Commits

### aaf9b0c4 F270 R4 C1: book round 3's PASS with R-0975 and R-0976 resolved, register R-0977 for F273, land DECISION F270 D4, its operator question and the round 4 plan, and save the payload and block copies
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f270-r4-block.md` | +118 / -0 | Byte copy of the block |
| `.agent/authored/f270-r4-decisions.md` | +49 / -0 | Byte copy of decisions.md |
| `.agent/authored/f270-r4-f273_from.txt` | +3 / -0 | Byte copy of f273_from.txt |
| `.agent/authored/f270-r4-f273_to.txt` | +6 / -0 | Byte copy of f273_to.txt |
| `.agent/authored/f270-r4-ledger.md` | +8 / -0 | Byte copy of ledger.md |
| `.agent/authored/f270-r4-operator_questions.md` | +58 / -0 | Byte copy of operator_questions.md |
| `.agent/authored/f270-r4-plan.md` | +26 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +49 / -0 | `8e9c2fad` bytes + decisions.md (DECISION F270 D4) |
| `.agent/live_review.md` | +8 / -0 | `8e9c2fad` bytes + ledger.md (Gate F270 R3 PASS, `Done: R-0975`, `Done: R-0976`, R-0977) |
| `.agent/operator_questions.md` | +16 / -14 | := operator_questions.md (Q1 merges two entries; Q6 added) |
| `.agent/plan.md` | +7 / -8 | := plan.md |
| `docs/roadmap/features/T2_F273.md` | +3 / -0 | `8e9c2fad` bytes with f273_from.txt replaced by f273_to.txt: FROM 1x before and after, the three added lines are exactly the TO-only lines, in order |

351 insertions, 22 deletions (`git show --numstat`).

### f827cfd7 F270 R4 C2: a push waits only for an unmet blocking criterion and names the open ones, and the upstream refusals, the contract refusals, the checkout refusals and the push itself are callable without an apply result
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/job_apply.py` | +122 / -51 | `_push_refusals` split into `upstream_push_refusals(target)` and `mission_push_refusals(read_mission) -> (refusals, open)` with D4 (6)'s rule; `push_open_criteria_sentence`; `PushOutcome` and `push_to_upstream(target, sha, branch_expected)`, which `_push_landed_commit` now calls; `_checkout_refusals` → public `checkout_refusals`; `push_open_criteria` on the result, the record and the applied, push-failed and preview summaries; `commit_auto_title_first` on `apply_job` and `build_auto_commit_subject(title_first=)` for D4 (3) |
| `apps/cli/command_catalog.py` | +1 / -1 | `job.apply --push` help states D4 (6)'s rule instead of D3 (5)'s |
| `tests/orchestration/test_job_apply_commit.py` | +38 / -7 | See "Changed D3 (5) tests" below |

161 insertions, 59 deletions.

### cf305676 F270 R4 C3: remedy do takes --commit, --commit-auto, --commit-with-history and --push, refuses what it cannot honour before any step, chains its jobs under a commit flag and pushes the mission once, honouring apply.push_after_mission
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/do_cmd.py` | +95 / -30 | `_DO_FLAGS_NOT_YET_AVAILABLE` and `_refuse_do_flags_not_yet_available` deleted; `DO_PUSH_KEY_WITHOUT_COMMIT`; `_refuse_before_any_step`; `_resolve_do_commit_flags` (D4 (1), (5)); the pass-through and `apply or bool(mode)`; `--json`'s `landed` and `push` |
| `apps/cli/command_catalog.py` | +4 / -4 | `do.run`'s `--commit`, `--commit-auto`, `--commit-with-history` and `--push` help |
| `packages/orchestration/do_sequence.py` | +188 / -22 | Module docstring; `DoContext` fields and `commit_mode`; the chaining in the run step (`_run_the_walks_jobs`) and `do_stopped_walk_note`, also on a `--step-by-step` halt; `do_apply_one_job`, `do_mission_push_refusals`, `_do_push_record`, `do_push_mission`; the apply step's single-job red refusal and the one push |
| `docs/guides/do-run-v1.md` | +43 / -6 | The run and apply rows, the `landed` and `push` keys, the four flags, "Refused before any step" and "Remedy never commits by itself" |
| `tests/cli/test_do_sequence_cli.py` | +22 / -12 | The four not-yet-available tests replaced by four refusal cases D4 gives the same flags (never deleted without a replacement) |

352 insertions, 74 deletions.

### 0104ead6 F270 R4 C4: tests prove do's one commit, auto commit and merge, every before-any-step refusal, one fast-forward push per mission, the key with and without a commit flag, only an unmet criterion holding a push, and a two-job walk landing two linear commits
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_do_commit_flags.py` | +429 / -0 | New: 17 test functions, 25 cases |

429 insertions, 0 deletions.

### C5 (this commit) F270 R4 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines; the largest is C4, with 429.

## Changed D3 (5) tests (C2)

- `test_p5_a_blocking_criterion_not_met_is_refused_before_anything[open|unmet]` → `test_p5_an_unmet_blocking_criterion_is_refused_before_anything` (one case): D4 (6) makes only `unmet` refuse. It now also carries a non-blocking `unmet` and a blocking `open` criterion, both asserted absent from the sentence, which reads "criteria C002 are unmet, so nothing is pushed".
- New `test_p7_an_open_blocking_criterion_is_pushed_and_named`: the former `[open]` case's property reversed by D4 (6): the push happens once, and `push_open_criteria == ["C002"]` on the result and the record, and the summary names it.
- `COMMIT_KEYS` gains `push_open_criteria`, so c1 and the CLI test assert the new record key.
- New `test_a5_title_first_asks_the_jobs_title_before_the_missions_goal` for D4 (3)'s order.

## The C4 tests (`tests/cli/test_do_commit_flags.py`)

- `--commit "Add the contact page"`: one commit on the previous tip, that first line, both trailers, the operator's identity, `landed`, a clean tree. `--commit-auto`: one commit passing `commit_subject_problem`. `--commit-with-history`: a two-parent merge commit.
- Exit 2 before any step, "Nothing was run.", no data file, no project, no job and `HEAD` unchanged: a lone `--push`; `--commit` with `--commit-auto`; `--commit-auto` with `--commit-with-history`; `--commit` with `--plan-only`; `--commit-auto --push --plan-only`; a two-line `--commit`; a dirty tree (the operator's file untouched); `--push` with a remote but no upstream (the sentence names `git push --set-upstream origin <branch>`, the remote stays empty).
- `--push` to a bare remote under `tmp_path`: the update hook logs exactly one `refs/heads/<branch> <old> <new>`, `<new>^` is `<old>` (a fast-forward), and `push` in `--json` holds the remote's name, never its URL.
- The key with `--commit`: one push without `--push`, source `apply.push_after_mission`. The key with `--apply` only: no commit, no push, the one sentence on stderr. Plain `do` and `do --apply`, key on and off: `HEAD` unchanged, no push, `landed == []`, `push` null.
- A blocking criterion marked `unmet` before the apply step: refused before anything is applied, exit 1. The fixture's `open` planner criteria (R-0977): pushed, named in `push.open_blocking_criteria` and in the apply detail.
- A remote whose update hook refuses: the commit stays, the remote tip does not move, exit 1.
- `--force-mission --commit … --push`: exactly two jobs, two linear commits suffixed `(job 1 of 2)` and `(job 2 of 2)`, job 2's `worktree_base_commit` is the first commit, one push of the second. The same walk under `--commit-auto` with an `unmet` criterion lands both commits (each passing the subject rule) and refuses the push. A walk whose second job does not complete keeps the first commit, pushes nothing and says so. `apply_job` receives two calls, neither with `push`.

## External actions

- G4: `git worktree add --detach .remedy-wt/f270-r4-g4 0104ead6`, removed with `git worktree remove` and `git worktree prune`. `git worktree list` afterwards: `/home/decodeux/Repos/remedy  0104ead6 [feature/f270-history-apply]`.
- After this commit: `git push origin feature/f270-history-apply`, never forced. No pull request is opened this round.
- No evidence job and no zip.

## Verification

G1 to G4 ran at C4 (`0104ead6`), before this commit.

- **G1**: `python3 .remedy-wt/f270-r4/g1.py`, exit 0 (reads the committed tree at HEAD):
  ```
  True payload ledger.md digest
  True payload decisions.md digest
  True payload plan.md digest
  True payload operator_questions.md digest
  True payload f273_from.txt digest
  True payload f273_to.txt digest
  True payload block.md digest
  True .agent/plan.md == plan.md
  True .agent/operator_questions.md == operator_questions.md
  True .agent/live_review.md == base + ledger.md
  True .agent/decisions.md == base + decisions.md
  True T2_F273.md FROM once at base
  True T2_F273.md == base with the pair applied
  True .agent/authored/f270-r4-ledger.md == payload
  True .agent/authored/f270-r4-decisions.md == payload
  True .agent/authored/f270-r4-plan.md == payload
  True .agent/authored/f270-r4-operator_questions.md == payload
  True .agent/authored/f270-r4-f273_from.txt == payload
  True .agent/authored/f270-r4-f273_to.txt == payload
  True .agent/authored/f270-r4-block.md == payload
  ALL True (20 checks)
  block copy sha256 b0c2bd19fb73f6af0a46fe1ab6120ea69f46118cd2c9128953218e2eef57456d
  ```
- **G2**: the block's list, with `tests/cli/test_do_commit_flags.py` first, run serially in the primary checkout. Every test file this round edited (`test_do_commit_flags.py`, `test_do_sequence_cli.py`, `test_job_apply_commit.py`) is on it. `python3 -m pytest -q -p no:cacheprovider …`, exit 0: `1246 passed in 199.11s (0:03:19)`.
- **G3**: `python3 -m ruff check packages/orchestration/job_apply.py tests/orchestration/test_job_apply_commit.py apps/cli/command_catalog.py apps/cli/commands/do_cmd.py packages/orchestration/do_sequence.py tests/cli/test_do_sequence_cli.py tests/cli/test_do_commit_flags.py` (every `.py` file of `git diff --name-only aaf9b0c4 0104ead6`), exit 0: `All checks passed!`
- **G4**: `python3 .remedy-wt/f270-r4/g4.py`, exit 0.
  - ONE worktree, `.remedy-wt/f270-r4-g4` at `0104ead6`; `__pycache__` purged before each run; `python3 -B -m pytest -p no:cacheprovider -q -rf tests/cli/test_do_commit_flags.py tests/orchestration/test_job_apply_commit.py` from the worktree root.
  - Every run first printed `do_sequence imported from: /home/decodeux/Repos/remedy/.remedy-wt/f270-r4-g4/packages/orchestration/do_sequence.py`.
  - Each FROM is whole lines and matched exactly once; each file was written back to its original bytes and `git status --porcelain` asserted empty before the next; the script ends `worktree clean after every revert: True`.

  | Run | Change | Result | Failing tests |
  |-----|--------|--------|---------------|
  | control | none | exit 0, `84 passed` | none |
  | (a) | `_refuse_before_any_step`'s `sys.exit(2)` → `return` | exit 1, `8 failed, 76 passed` | `test_do_commit_flags.py::test_a_dirty_tree_is_refused_before_any_step`, `::test_a_flag_rule_is_refused_before_any_step[auto-and-history]`, `[auto-push-plan-only]`, `[commit-and-auto]`, `[commit-plan-only]`, `[lone-push]`, `[two-line-message]`, `::test_push_with_no_upstream_is_refused_before_any_step` |
  | (b) | `if push and not mode:` → `if False and …` | exit 1, `4 failed, 80 passed` | `test_do_commit_flags.py::test_a_flag_rule_is_refused_before_any_step[lone-push]`, `test_job_apply_commit.py::TestFlagRefusals::test_f3_a_lone_push_is_refused[False]`, `[True]`, `::TestThroughTheCli::test_a_clash_is_a_blocked_apply_and_a_commit_lands` |
  | (c) | `if mode and plan_only:` → `if False and …` | exit 1, `2 failed, 82 passed` | `test_do_commit_flags.py::test_a_flag_rule_is_refused_before_any_step[auto-push-plan-only]`, `[commit-plan-only]` |
  | (d) | the key's source removed: `source = "--push" if push else ""` | exit 1, `1 failed, 83 passed` | `test_do_commit_flags.py::test_the_key_with_a_commit_flag_pushes_once_without_push` |
  | (e) | the key without a commit flag sets `mode = "auto"` | exit 1, `1 failed, 83 passed` | `test_do_commit_flags.py::test_the_key_without_a_commit_flag_commits_and_pushes_nothing_and_says_so` |
  | (f) | `chain = bool(ctx.commit_mode)` → `chain = False` | exit 1, `4 failed, 80 passed` | `test_do_commit_flags.py::test_a_chained_walk_under_an_unmet_criterion_lands_its_commits_and_refuses_the_push`, `::test_a_two_job_walk_under_commit_lands_two_linear_commits_and_one_push`, `::test_a_walk_that_stops_keeps_its_commit_and_pushes_nothing`, `::test_the_apply_step_never_passes_push_to_a_job` |
  | (g) | `"push": ctx.push` added to the apply flags | exit 1, `5 failed, 79 passed` | `test_do_commit_flags.py::test_a_chained_walk_under_an_unmet_criterion_lands_its_commits_and_refuses_the_push`, `::test_a_push_the_remote_refuses_leaves_the_commit_and_fails_the_walk`, `::test_a_two_job_walk_under_commit_lands_two_linear_commits_and_one_push`, `::test_a_walk_that_stops_keeps_its_commit_and_pushes_nothing`, `::test_the_apply_step_never_passes_push_to_a_job` |
  | (h) | `if unmet:` → `if False and unmet:` | exit 1, `3 failed, 81 passed` | `test_do_commit_flags.py::test_a_chained_walk_under_an_unmet_criterion_lands_its_commits_and_refuses_the_push`, `::test_an_unmet_blocking_criterion_is_refused_before_anything_is_applied`, `test_job_apply_commit.py::TestPush::test_p5_an_unmet_blocking_criterion_is_refused_before_anything` |
  | (i) | `c.status == "unmet"` → `c.status != "met"` | exit 1, `8 failed, 76 passed` | `test_do_commit_flags.py::test_a_push_the_remote_refuses_leaves_the_commit_and_fails_the_walk`, `::test_a_two_job_walk_under_commit_lands_two_linear_commits_and_one_push`, `::test_an_open_blocking_criterion_is_pushed_and_named_in_the_json`, `::test_push_sends_exactly_one_fast_forward_push_to_the_upstream`, `::test_the_apply_step_never_passes_push_to_a_job`, `::test_the_key_with_a_commit_flag_pushes_once_without_push`, `test_job_apply_commit.py::TestPush::test_p5_an_unmet_blocking_criterion_is_refused_before_anything`, `::TestPush::test_p7_an_open_blocking_criterion_is_pushed_and_named` |
  | (j) | `do_push_mission(ctx)` called after a stopped run step | exit 1, `1 failed, 83 passed` | `test_do_commit_flags.py::test_a_walk_that_stops_keeps_its_commit_and_pushes_nothing` |

  No mutation stayed green. Ids are under `tests/cli/` and `tests/orchestration/`.
- **Full suite**: not run (amend0917-throughput).

## Authored-text proofs

- `.agent/authored/f270-r4-{ledger.md,decisions.md,plan.md,operator_questions.md,f273_from.txt,f273_to.txt,block.md}` equal their payloads byte for byte, all seven in C1 (G1). Every payload's sha256 matched the block before use.
- The block copy's sha256 is `b0c2bd19fb73f6af0a46fe1ab6120ea69f46118cd2c9128953218e2eef57456d`, the digest the orchestrator named.
- `.agent/live_review.md` and `.agent/decisions.md` are their `8e9c2fad` bytes with ledger.md and decisions.md appended; `.agent/plan.md` and `.agent/operator_questions.md` are their payloads; T2_F273.md is its `8e9c2fad` bytes with the pair applied (G1).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `aaf9b0c4`, the block copy included |
| C2 D4 (6) and the push's reuse | deviated | `f827cfd7`; also carries the `job.apply --push` help and D4 (3)'s `commit_auto_title_first` (see Deviations) |
| C3 `do` D4 (1)–(5), (7) | done | `cf305676`, 352 insertions, not split |
| C4 tests | done | `0104ead6` |
| C5 handoff and push | done | This commit, then the push |
| G1–G4 | done | All exit 0; every mutation red |
| R-0977 | registered | Owner F273; not repaired here |

## Open findings

`python3 .remedy-wt/f268-r4/count.py` (by distinct id) at `0104ead6` reads `HEAD registrations 134 done 6 open 128`: R-0977 registered, R-0975 and R-0976 now `Done:`. This round lands no finding.

## Deviations & assumptions

- **Commit sequence**: C1, C2, C3, C4, C5, then the push, as ordered; none was split.
- **C2 touches `apps/cli/command_catalog.py`**: the `job.apply --push` help stated D3 (5)'s rule ("while any blocking criteria … are not met"), which C2's code amends, so the help was changed in the same commit to stay true. The file is in the Bundle's change set (C3).
- **D4 (3)'s `--commit-auto` order lives in `job_apply.py` (C2)**: `apply_job(…, commit_auto_title_first=)` and `build_auto_commit_subject(job, title_first=)`, because the subject is built inside `job_apply`; `do` passes `True` only in a walk of more than one job. `commit_auto_title_first` is a result attribute, not a record field.
- **`_checkout_refusals` became `checkout_refusals`** (C2), so `do` asks the same refusals before any step. For `--commit-with-history` the pre-step sentences use the merge's wording ("the task commits", "merge into"); the staging-job and job-branch refusals can only be asked once the job exists, at apply.
- **D4 (6)'s single-job refusal** is asked when the walk has exactly one job to apply, before `apply_job`; it also re-asks the upstream refusals. Its `push` object carries `pushed: false`, an empty `sha` and the refusal as `error`.
- **`push` in `do --json`** is `{pushed, sha, remote, ref, error, source, open_blocking_criteria}`; `source` (`--push` or `apply.push_after_mission`) is an addition to D4 (7)'s list. It is `null` when the walk asked no push or stopped before the apply step.
- **The key's configuration** is read with `load_config(<top level>/remedy.toml)` (plus the user file and the env var, as `load_config` does); a configuration that cannot be read counts as the key unset, so Remedy never pushes on a value it cannot read.
- **Stopped walks**: under a commit flag a run step that fails or stops, an apply-step failure, and a `--step-by-step` halt between steps each end their detail with what landed and "nothing was pushed" (D4 (2)).
- **Pre-step refusal wording**: `job apply`'s sentences end "…, so nothing was applied." and `do` appends " Nothing was run.", as D4 (1) asks.
- **The C4 stopped-walk test** makes job 2 not complete by standing in for `run_job` on its second call with the job as planned; no provider is involved.
- **Scratch scripts**: `.remedy-wt/f270-r4/{verify_payloads,build_c1,g1,g4}.py` and the logs `g2.log`, `g4.log` are gitignored.

## Next

Phase 1 rule 1 (`.agent/STOP`), then the review of round 4.

Operator questions open: 5
