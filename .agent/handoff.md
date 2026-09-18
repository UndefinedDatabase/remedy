# Handoff — F269 Contract & contract templates · Round 4 (T003 hygiene)

## Session

SESSION 1 of feature F269 · round 4 · rounds so far 4

Context self-assessment: the round fit in one worker context with room to spare. Every gate below was run in this session at C4 `032de8ab`; none was carried over from memory.

## Range

Review of fc9aae2b..HEAD — branch `feature/f269-contract`.

## Summary

Round 4 lands T003's hygiene half under DECISION F269 D5:

- C1 books round 3's verdict (ledger), appends DECISION F269 D5, writes the round 4 plan, and saves the payloads and the block.
- C2 (two commits, deviation 1) adds `packages/orchestration/contract_hygiene.py`. It holds three pure rules (`unreferenced`, `replaced`, `stubs`), a git measurement of a work tree against `HEAD`, and `main(argv)`, which exits 0 when there is no finding, 1 on findings and 2 when it cannot measure. The second commit adds its tests.
- C3 adds the three blocking hygiene criteria to all four `docs/contracts/*.md`, byte-exact from the payloads. Each criterion has a `custom_cmd` `check:` line that runs its rule.
- C4 adds D5 (6)'s sentence to `_REVIEWER_SYSTEM` and the round hook in `run_pingpong`. After the reviewer answers, `unreferenced` and `replaced` run over the files the job has added so far. Each finding is appended to the reviewer's findings with the path in `file` and in the summary. A `pass` verdict becomes `needs_repair`.
- C5 is this handoff.

## Commits

### c5ebaf72 F269 R4 C1: bookkeeping — round 3 verdict, DECISION F269 D5, the round 4 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r4-block.md` | +103 / -0 | Byte copy of block.md |
| `.agent/authored/f269-r4-decisions.md` | +46 / -0 | Byte copy of decisions.md |
| `.agent/authored/f269-r4-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r4-plan.md` | +27 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +46 / -0 | `fc9aae2b` bytes + decisions.md (D5) |
| `.agent/live_review.md` | +2 / -0 | `fc9aae2b` bytes + ledger.md (Gate F269 R3 PASS) |
| `.agent/plan.md` | +7 / -8 | := plan.md |

### 1cef2b6a F269 R4 C2: the contract hygiene check — unreferenced, replaced and stubs over a git work tree, exit 0, 1 or 2
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/contract_hygiene.py` | +331 / -0 | NEW, standard library only. `HYGIENE_RULES`, `EXIT_CLEAN/FINDINGS/CANNOT_MEASURE`, `CODE_FILE_SUFFIXES`, `HygieneFinding`, `WorkTreeChanges`, `HygieneMeasureError`; `find_unreferenced_files` (stem bounded by non-word characters, the file's own text excluded, reads 1 MiB per file, D5 (2) exemptions), `replaced_originals` / `find_replaced_files` (D5 (3) markers), `find_stubs` (TODO/FIXME/XXX as a word on added lines; a Python function whose def line was added and whose body after an optional docstring is only `pass`, `...` or `raise NotImplementedError`, unless decorated `abstractmethod`/`overload`), `run_hygiene_rule`, `measure_work_tree` (untracked non-ignored + index-added against `HEAD`; modified files with their added line numbers from `git diff -U0 HEAD`; `GIT_OPTIONAL_LOCKS=0`), `main(argv)` under `if __name__ == "__main__"` |

### 57b5e752 F269 R4 C2: the hygiene check's tests — each rule over a tmp git repository, the subprocess exit codes, and F061's real gate
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_contract_hygiene.py` | +258 / -0 | NEW, 26 tests over a tmp git repository whose base commit holds `main.py` (with a committed TODO) and `util.py`. `unreferenced`: an orphan whose own text names its stem is reported; it passes once a committed `main.py` imports it; a longer name containing the stem is no reference; `__init__.py`, a `tests/` file, a `test_` file and a `.spec.ts` file are exempt; a non-code file is not judged. `replaced`: `util_v2.py` is reported beside `util.py` and passes once `util.py` is deleted; ten markers are parametrized; a marker with no original is not a finding. `stubs`: a TODO added to a committed file is reported by line, and the committed TODO is not; an added `pass` body is reported; an `abstractmethod` passes; `...` and `raise NotImplementedError(...)` are reported. Each rule is run as the subprocess `python3 -m packages.orchestration.contract_hygiene <rule>` and exits 0, 1 and 2 (outside a work tree); an unknown rule exits 2; a `custom_cmd` check of that argv through the real `dod_gate.evaluate_dod` is red with an orphan and green without |

### 66d44655 F269 R4 C3: the three hygiene criteria in all four contract templates, each checked by its contract_hygiene rule
| Path | +/- | Reason |
|------|-----|--------|
| `docs/contracts/api-service.md` | +6 / -0 | := api-service.md payload |
| `docs/contracts/cli-tool.md` | +6 / -0 | := cli-tool.md payload |
| `docs/contracts/python-library.md` | +6 / -0 | := python-library.md payload |
| `docs/contracts/website.md` | +6 / -0 | := website.md payload |
| `tests/orchestration/test_contract_templates.py` | +30 / -1 | `WEBSITE_CRITERIA` gains the three hygiene criteria, and the compiled website ids are `C001`..`C007`. D5 (5) changes both by design; the property kept is "the file's criteria in order". New parametrized test (4 templates): the last three criteria are the hygiene texts, blocking, each with the exact `custom_cmd` check of its `check:` line, id `ctr-<id>` |

### 032de8ab F269 R4 C4: the reviewer's hygiene rule — its sentence in the system text, and the round rejects an unreferenced or replaced added file naming the path
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_loop.py` | +70 / -0 | `_REVIEWER_SYSTEM` gains one line: "A change that adds a file nothing references, or leaves replaced code beside its replacement, is rejected with the path named." New `ROUND_HYGIENE_RULES`, `_workspace_hygiene_changes` (worktree: `measure_work_tree`; copy mode: staged files absent from the original, tree = staging walk without noise), and `round_hygiene_findings`. The round hook sits after the reviewer-error break and before `validate_reviewer_output` |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -0 | Regenerated from `reachable_closure()`: `packages.orchestration.contract_hygiene` |
| `tests/orchestration/test_pingpong.py` | +91 / -0 | `TestTheRoundRejectsAHygieneViolation` over a tmp git repository whose base commit holds `main.py` and `util.py`, through `pingpong_job.run_job` with `FakeProvider(builder_files=[...], pass_on_round=1)` as builder, `FakeProvider(pass_on_round=1)` as reviewer, and `repair_rounds=0`. Adding `orphan_module.py` ends the job BLOCKED: the exported round's verdict is `needs_repair`, its findings are exactly `[("orphan_module.py", "orphan_module.py: an added file that no other file references")]` as (`file`, `summary`), the final status is `repair_exhausted`, and the decision is `stop_repair_disabled`. `main.py` completes with a `pass` and no findings. `util_v2.py` is blocked with the finding "added beside util.py" |
| `tests/orchestration/test_reviewer_prompt_golden.py` | +8 / -6 | DECLARED CONTENT CHANGE, per the file's docstring: all six `_FROZEN_RENDERS` gain exactly the new sentence after "Only flag real issues.". The replacement was mechanical: a script replaced the one substring and asserted 6 occurrences. A comment above the dict records the change |

### C5 (this commit) F269 R4 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | This file |

## External actions

- `git worktree add --detach .remedy-wt/f269-r4-g4 HEAD` (at `032de8ab`) for G4. It was removed with `git worktree remove --force .remedy-wt/f269-r4-g4` (exit 0). `git worktree list` afterwards: `/home/decodeux/Repos/remedy  032de8ab [feature/f269-contract]`.
- `git push` runs after this commit. Its outcome and G5 are in the worker's final report.
- No PR was created, edited or merged.

## Verification

All gates ran at C4 `032de8ab` with a clean tree, through the helper scripts in `.remedy-wt/f269-r4/`. Each exit code is a subprocess return code, printed by `gate.py`.

G1 transport + state, `python3 .remedy-wt/f269-r4/g1.py`, EXIT 0:
```
payload digests matched: True
templates equal payloads: True
plan.md equals payload: True
live_review.md = base + ledger: True
decisions.md = base + decisions: True
authored copies equal payloads: True
True
```

G2, `python3 -m pytest -q -p no:cacheprovider` over the block's 15 paths, EXIT 0. Every test file this round created or edited is in that list: `test_contract_hygiene.py`, `test_contract_templates.py`, `test_pingpong.py`, `test_reviewer_prompt_golden.py`, and `test_import_reachability.py` through its allowlist.
```
1070 passed in 171.59s (0:02:51)
```
Also run, though not ordered: every one of the 122 test files under `tests/` that drives the loop (its text matches `run_pingpong|run_job|FakeProvider|builder_name="fake"|--builder fake|"fake"`), with `-n 12`. That read `1 failed, 4583 passed, 1 skipped`. The one failure was `tests/orchestration/test_product_smoke.py::test_no_zombie_processes_after_every_outcome`, which counts processes machine-wide and so is sensitive to parallel workers. Run serially, that file read `76 passed`.

G3, `python3 -m ruff check packages/orchestration/contract_hygiene.py tests/orchestration/test_contract_hygiene.py tests/orchestration/test_contract_templates.py packages/orchestration/pingpong_loop.py tests/orchestration/test_pingpong.py tests/orchestration/test_reviewer_prompt_golden.py`, EXIT 0:
```
All checks passed!
```

G4, `python3 .remedy-wt/f269-r4/g4.py`: one worktree at `032de8ab`, running `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_contract_hygiene.py tests/orchestration/test_pingpong.py` from the worktree root. `__pycache__` was purged before each run and the module path printed before each run. Each mutation was reverted with `git checkout -- <exact path>`, and the worktree status read clean after every revert.
```
module: /home/decodeux/Repos/remedy/.remedy-wt/f269-r4-g4/packages/orchestration/contract_hygiene.py   (printed identically before every run)
[control] EXIT 0: 66 passed in 5.01s
[mutation a] EXIT 1: 2 failed, 64 passed in 5.04s
    FAILED tests/orchestration/test_contract_hygiene.py::test_unreferenced_reports_an_added_module_only_its_own_text_names
    FAILED tests/orchestration/test_pingpong.py::TestTheRoundRejectsAHygieneViolation::test_an_added_file_nothing_references_blocks_the_job_naming_the_path
[mutation b] EXIT 1: 1 failed, 65 passed in 4.52s
    FAILED tests/orchestration/test_contract_hygiene.py::test_stubs_passes_an_abstractmethod
[mutation c] EXIT 1: 1 failed, 65 passed in 4.58s
    FAILED tests/orchestration/test_pingpong.py::TestTheRoundRejectsAHygieneViolation::test_an_added_file_nothing_references_blocks_the_job_naming_the_path
```
The mutations:
- (a) In `find_unreferenced_files`, `... for rel, text in texts.items() if rel != path)` became `... for rel, text in texts.items())`.
- (b) In `_is_stub_function`, the two lines `if any(_decorator_name(d) in _STUB_EXEMPT_DECORATORS ...): return False` were deleted.
- (c) In `run_pingpong`'s hook, the two lines `if reviewer_out.verdict == "pass": reviewer_out.verdict = "needs_repair"` were deleted. The job still ends blocked, as `review_inconsistent`, so the acceptance test goes red on its verdict assertion.

The full suite was not run (amend0917-throughput).

## Authored-text proofs

- The four payloads (block, decisions, ledger, plan) are committed byte-identical as `.agent/authored/f269-r4-*` (G1 `authored copies equal payloads: True`).
- `.agent/plan.md` equals plan.md. `.agent/live_review.md` and `.agent/decisions.md` equal their `fc9aae2b` bytes plus the payload (G1 True).
- The four `docs/contracts/<name>.md` equal their payloads (G1 `templates equal payloads: True`).

## Deviations & assumptions

1. C2 is two commits, both with the subject prefix `F269 R4 C2:`: the module (+331) and its tests (+258). Together they were 589 insertions, and constraint 1 orders the split rather than exceeding 500. This is one more commit than the block's bundle lists.
2. The round hook fails closed when it cannot measure. If `measure_work_tree` raises in a worktree, the hook appends one finding, `HYG-unmeasured` (severity high, no file). D5 (1) states this rule for the command line only. The hook extends it on the reading that "a tree it cannot read is never a met criterion". No test exercises this path, because a job worktree is always a git work tree.
3. Hook findings carry the id `HYG-<rule>-<path>`, severity `high`, the summary `<path>: <message>`, and a `required_fix` per rule. The id is stable across repair rounds, so the resolved and remaining tracking works. The hook runs in every round and every isolation mode. It appends findings whatever the verdict, and changes only `pass`, to `needs_repair`.
4. The copy-mode "added" set is the staged files absent from the original repository, and its tree is a walk of the staging copy without the noise directories. There is no git there, so there is no ignore file either.
5. In `test_contract_hygiene.py`, the subprocess runs with `PYTHONPATH` set to the source root the test imported `contract_hygiene` from. The `evaluate_dod` test sets the same through `monkeypatch`, because `PYTHONPATH` is on the guard's environment allowlist. This makes the subprocess run the same code as the test, where otherwise an editable install would shadow a worktree. G4's printed paths show the in-process import resolving inside the worktree.
6. No existing test's pinned behaviour changed apart from the two named in C3 (`WEBSITE_CRITERIA` and the website id list) and C4 (the golden renders). This was measured by the 122-file loop-driver run under G2.
7. The acceptance test lives in the existing `tests/orchestration/test_pingpong.py`.
8. No `docs/` page describes the reviewer's system text or the round's review sequence in words that this change made false (a grep for the system text finds only the code and the golden). So no doc edit was made outside the change set.

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 hygiene check + tests | deviated | split into two commits under the 500-line cap (deviation 1) |
| C3 templates | done | |
| C4 reviewer rule + round hook | done | |
| C5 handoff + push | done | push follows this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Then the review of round 4 (T003 hygiene), with its verdict booked in round 5's first commit.

Operator questions open: 4
