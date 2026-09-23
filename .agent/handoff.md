# Handback — F279 Configuration & toolchain truth · Round 6 · Book round 5's PASS, record DECISION F279 D6, land T004's report half (`remedy doctor toolchain`)

## Session

SESSION 1 of feature F279 · round 6 · rounds so far 6

This round booked round 5's PASS into the ledger, recorded DECISION F279 D6
(a new `doctor toolchain` command sits beside `doctor core`, since `doctor
core` promises no network and the report needs `--offline` to skip the
package index; the new module joins the entry points' import closure, so
the allowlist and `tests/cli/test_worker_facade_cmd.py`'s handler-set guard
both gained a line in the same commit as the module), and landed T004's
report half: `packages/orchestration/toolchain.py` (the installed/pinned/
newest table, "unknown" rather than a guessed number whenever the index is
unreachable or skipped), the `doctor.toolchain` command
(`apps/cli/commands/worker_facade_cmd.py`, `apps/cli/command_catalog.py`),
the reachability-allowlist line, and a test holding the CI matrix to
exactly two Python versions with the first as the floor
(`tests/orchestration/test_ci_workflow.py`). All of G1-G5 ran before this
handoff was written and matched the block's stated expectations exactly,
byte for byte and reading for reading. Context self-assessment: a
comfortable majority of the working budget remains at handback.

## Range

Review of `86e12317`..`HEAD`.

## Commits

### f5bef15f F279 R6 C1a: copy round 6 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r6-block.md | +232/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f279-r6-ledger.diff | +10/-0 | Payload copy |
| .agent/authored/f279-r6-plan.md | +31/-0 | Payload copy |
| .agent/authored/f279-r6-decisions.diff | +36/-0 | Payload copy |

Measured insertions: 309 (block's line count 232 plus 77), matching the
block's formula exactly, well under the 500 cap.

### d8982f0a F279 R6 C1b: copy round 6 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r6-toolchain.py | +107/-0 | Payload copy |
| .agent/authored/f279-r6-test_toolchain.py | +103/-0 | Payload copy |
| .agent/authored/f279-r6-worker_facade_cmd.diff | +40/-0 | Payload copy |
| .agent/authored/f279-r6-command_catalog.diff | +27/-0 | Payload copy |
| .agent/authored/f279-r6-allowlist.diff | +12/-0 | Payload copy |
| .agent/authored/f279-r6-test_ci_workflow.diff | +26/-0 | Payload copy |
| .agent/authored/f279-r6-test_worker_facade_cmd.diff | +13/-0 | Payload copy |
| .agent/authored/f279-r6-mutations.py | +65/-0 | Payload copy (G5 tool, never applied to a tracked file) |

Measured insertions: 393, matching the block's expected 393 exactly.

### 21bf1fbf F279 R6 C2: book round 5's PASS and record DECISION F279 D6
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `ledger.diff` applied: round 5's `Gate:` entry appended |
| .agent/plan.md | +7/-6 | Rewritten to the round-6 plan.md payload |
| .agent/decisions.md | +28/-0 | `decisions.diff` applied: DECISION F279 D6 recorded |

Measured insertions (`git diff --numstat` before staging, confirmed
unchanged after `git add`): 28 decisions.md, 2 live_review.md, 7 plan.md —
matching the block's expected counts exactly.

### 5f64cdb9 F279 R6 C3: add remedy doctor toolchain and hold the CI matrix to two Pythons
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/toolchain.py | +107/-0 | NEW FILE (`shutil.copyfile` from payload): the report — installed/pinned/newest per tool |
| tests/orchestration/test_toolchain.py | +103/-0 | NEW FILE (`shutil.copyfile` from payload): the report's and command's tests |
| apps/cli/commands/worker_facade_cmd.py | +24/-0 | `worker_facade_cmd.diff` applied: the `doctor.toolchain` handler |
| apps/cli/command_catalog.py | +16/-0 | `command_catalog.diff` applied: the `doctor.toolchain` catalog entry |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | `allowlist.diff` applied: `packages.orchestration.toolchain` added |
| tests/orchestration/test_ci_workflow.py | +15/-0 | `test_ci_workflow.diff` applied: the two-Python-matrix guard |
| tests/cli/test_worker_facade_cmd.py | +1/-1 | `test_worker_facade_cmd.diff` applied: expected handler set gains `doctor.toolchain` |

Measured insertions: 16 command_catalog.py, 24 worker_facade_cmd.py, 107
toolchain.py, 1 test_worker_facade_cmd.py, 1
import_reachability_allowlist.txt, 15 test_ci_workflow.py, 103
test_toolchain.py — matching the block's expected counts exactly.

### (this commit) F279 R6 C4: rewrite handoff for round 6
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f279-r6-mut 5f64cdb9` — created for
  G5; `git worktree remove --force .remedy-wt/f279-r6-mut` then
  `git worktree prune` removed it as G5's last action. `git worktree list`
  afterward showed only the primary checkout and the two pre-existing
  `.remedy-wt/job-*` worktrees.
- `git push origin feature/f279-configuration-toolchain-truth` — see the
  session's final reply for the real outcome; it runs after this commit.
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no
  checkout of `main` or any other branch/commit in the primary checkout: none
  run, per constraint 5.
- `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their
  branches and every existing stash were left untouched.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, real exit 2 (ENOENT), absent — proceed.
- `git status --porcelain` → empty. `git branch --show-current` →
  `feature/f279-configuration-toolchain-truth`. `git log --oneline -1` →
  `86e12317 F279 R5 C4: rewrite handoff for round 5`. All three matched.
- Block bytes (R-0954): measured line count (newline count)=232,
  sha256=`f43353d6ba14829cb5bfb55967e20b79a41e91035a1ad1d2910357746933a1fe`;
  matches both readings given in the delegation message exactly.
- `git worktree list` (before any change) → primary checkout at `86e12317`
  plus `.remedy-wt/job-129b3ad7206d4f8d` (`09441a92`) and
  `.remedy-wt/job-e7268925db3a4831` (`cc8696a3`).
- `git stash list | head -1` →
  `stash@{0}: WIP on (no branch): 365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`.

PAYLOADS — all 11 measured and matched the block's table exactly (line
count, byte count, sha256): allowlist.diff (12/586/`4db2f64c...`),
command_catalog.diff (27/1241/`6d615f16...`), decisions.diff
(36/2646/`cccc087f...`), ledger.diff (10/6330/`096065e3...`), mutations.py
(65/2754/`75508693...`), plan.md (31/1249/`d828e60c...`),
test_ci_workflow.diff (26/1326/`2898e29e...`), test_toolchain.py
(103/4309/`72b7eee6...`), test_worker_facade_cmd.diff (13/636/`40ba7986...`),
toolchain.py (107/3992/`c854f244...`), worker_facade_cmd.diff
(40/1977/`3b83c540...`).

`git apply --check` then `git apply` for every `.diff` payload (ledger,
decisions at C2; worker_facade_cmd, command_catalog, allowlist,
test_ci_workflow, test_worker_facade_cmd at C3): all 7 pairs at real exit
code 0, in the commit order the block specifies. `.agent/plan.md`,
`toolchain.py` and `test_toolchain.py` were rewrites/new files by
`shutil.copyfile`, never a `git apply`.

G1 TRANSPORT — every `.agent/authored/f279-r6-*` copy (12 files, including
the block copy) read back with `git show <adding-commit>:<path>` and
compared byte-for-byte against its source (`.remedy-wt/f279-r6-block.md` for
the block, `.remedy-wt/f279-r6-payloads/<name>` for the rest): all 12
matched exactly.

G2 THE BOOKKEEPING — at C2 (`21bf1fbf`): `.agent/live_review.md`
bytes=384675 sha256=`ee7a9ca8fcfb6fe4aeeb37d5199815cb3f4d7b09f7772c5691dab9378da353b0`
MATCH; `.agent/plan.md` bytes=1249
sha256=`d828e60c61c901f0cc720d709ef1bb819b17230c7136992b20242cb65d85e363` MATCH;
`.agent/decisions.md` bytes=1872202
sha256=`59cdbf56cc3b5ea972f24a81370f0c32abbd2849acb4c127837d9dd058f8c12c` MATCH.
Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`),
computed over `.agent/live_review.md` text at `86e12317` and at C2: 26 and
26, both set differences empty — matching the block's 26/26 exactly. Lines
beginning `Gate: F279 R5 — ` at `86e12317` and at C2: 0 and 1 — matching the
block's 0/1 exactly. `git diff --name-only <C1b> <C2>` → exactly
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` — matches
C2's list.

G3 THE REPORT — `git diff --name-only <C2> <C3>` → exactly
`apps/cli/command_catalog.py`, `apps/cli/commands/worker_facade_cmd.py`,
`packages/orchestration/toolchain.py`,
`tests/cli/test_worker_facade_cmd.py`,
`tests/orchestration/import_reachability_allowlist.txt`,
`tests/orchestration/test_ci_workflow.py`,
`tests/orchestration/test_toolchain.py` — matches C3's list exactly. At C3
(`5f64cdb9`): `packages/orchestration/toolchain.py` bytes=3992
sha256=`c854f24448029c004f73846619402e5f0ab10ed6453751b146807b2cdf2329a9` MATCH;
`tests/orchestration/test_toolchain.py` bytes=4309
sha256=`72b7eee658dba5619d027147dfcbc7d46c1d4c74fdf36b1dfa6103852f8a585b` MATCH;
`apps/cli/commands/worker_facade_cmd.py` bytes=21424
sha256=`fc1aafb6f048aa9c41c786208e15f783079a33d003b86e5f4627743f587551c2` MATCH;
`apps/cli/command_catalog.py` bytes=110896
sha256=`a34066026a9d44a7c88b4ad446fbf33e0544d9c32029c85b35d43846513f1631` MATCH;
`tests/orchestration/import_reachability_allowlist.txt` bytes=9867
sha256=`56a7fd7d5cb82648b7917a304633efed53716a54929cc186484688de948a3f66` MATCH;
`tests/orchestration/test_ci_workflow.py` bytes=5019
sha256=`2afefc40c7eeffdc045ac6aa3d02b218e2fc4865e1fa79d19666a847ef95a8e8` MATCH;
`tests/cli/test_worker_facade_cmd.py` bytes=33678
sha256=`8047f6e8885340e1dd1ed16523fa4918fec4c8887b11aa877971c53329ed0bf1` MATCH.
No digest differed, so no `git diff --no-index` stop was needed.

G4 THE TESTS — the ordered pytest selection, run SERIALLY (real exit code
0): `1762 passed in 328.72s (0:05:28)`. The reviewer ran the same selection
WITHOUT `tests/cli/test_golden_path.py` inside a disposable worktree
carrying C2 and C3 and read `1718 passed, 2 skipped` at exit 0; this round
ran the full selection INCLUDING golden path in the primary checkout, which
carries the UI toolchain a worktree lacks (as the block anticipates),
accounting for the different pass/skip counts. `python3 -m ruff check`
over the Python paths C3 lists (`packages/orchestration/toolchain.py
tests/orchestration/test_toolchain.py apps/cli/commands/worker_facade_cmd.py
apps/cli/command_catalog.py tests/orchestration/test_ci_workflow.py
tests/cli/test_worker_facade_cmd.py` — the allowlist `.txt` excluded, since
it is not Python; a first attempt that mistakenly included it produced
spurious `F821` findings against the `.txt`, self-corrected before this
reading) → `All checks passed!`, real exit 0. `python3 -m apps.cli.main
integrity check --json` → all 5 checks `pass` (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`), `fail_count` 0, real exit 0. `python3 -m
apps.cli.main doctor toolchain --offline` → table pasted below, real exit
0:
```
Toolchain: the version installed here, the version constraints.txt pins, and the newest version the package index knows.
The package index was not asked (--offline), so every newest version reads unknown.
  tool          installed       pinned          newest
  pydantic      2.13.1          2.13.5          unknown
  psutil        5.9.0           7.2.2           unknown
  pytest        9.0.3           9.1.1           unknown
  pytest-xdist  3.8.0           3.8.0           unknown
  ruff          0.15.17         0.15.17         unknown
  mypy          2.1.0           2.3.1           unknown
  pytest-cov    7.1.0           7.1.0           unknown
  coverage      7.14.0          7.16.1          unknown
```
`python3 -m apps.cli.main integrity block .remedy-wt/f279-r6-block.md` →
all 7 items OK (1 size, 3 cap-bounded replacements, 10 open set recomputed,
24 gate paths resolve, 30 new ids searched first, 31 gates before the text,
37 no unmeasured runs), `All 7 checkable items pass.`, real exit 0 —
matching the reviewer's own pre-emission run of this block exactly.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r6-mut
5f64cdb9` real exit 0. `python3 -B .remedy-wt/f279-r6-payloads/mutations.py
.remedy-wt/f279-r6-mut` real exit 0, full output:
```
control_before REAL_EXIT=0
21 passed in 0.30s
m1_offline_reads_zero FROM count in packages/orchestration/toolchain.py: 1
m1_offline_reads_zero REAL_EXIT=1
FAILED tests/orchestration/test_toolchain.py::test_offline_and_an_empty_answer_both_read_unknown_never_a_number
FAILED tests/orchestration/test_toolchain.py::TestTheCommand::test_offline_json_names_every_tool_with_three_columns
2 failed, 19 passed in 0.30s
m1_offline_reads_zero restored byte-identical: True
m2_a_failed_fetch_reads_zero FROM count in packages/orchestration/toolchain.py: 1
m2_a_failed_fetch_reads_zero REAL_EXIT=1
FAILED tests/orchestration/test_toolchain.py::TestTheIndexFetch::test_any_fetch_failure_reads_unknown[failure0]
FAILED tests/orchestration/test_toolchain.py::TestTheIndexFetch::test_any_fetch_failure_reads_unknown[failure1]
2 failed, 19 passed in 0.31s
m2_a_failed_fetch_reads_zero restored byte-identical: True
m3_the_dev_extra_dropped FROM count in packages/orchestration/toolchain.py: 1
m3_the_dev_extra_dropped REAL_EXIT=1
FAILED tests/orchestration/test_toolchain.py::test_the_report_covers_the_runtime_dependencies_and_the_dev_extra
FAILED tests/orchestration/test_toolchain.py::test_the_three_columns_come_from_their_three_sources
FAILED tests/orchestration/test_toolchain.py::TestTheCommand::test_offline_json_names_every_tool_with_three_columns
FAILED tests/orchestration/test_toolchain.py::TestTheCommand::test_text_mode_prints_a_header_and_one_line_per_tool
4 failed, 17 passed in 0.30s
m3_the_dev_extra_dropped restored byte-identical: True
m4_offline_ignored FROM count in apps/cli/commands/worker_facade_cmd.py: 1
m4_offline_ignored REAL_EXIT=1
FAILED tests/orchestration/test_toolchain.py::TestTheCommand::test_offline_json_names_every_tool_with_three_columns
1 failed, 20 passed in 1.06s
m4_offline_ignored restored byte-identical: True
m5_a_third_python_in_the_matrix FROM count in .github/workflows/ci.yml: 1
m5_a_third_python_in_the_matrix REAL_EXIT=1
FAILED tests/orchestration/test_ci_workflow.py::test_hosted_workflow_runs_the_floor_and_a_current_interpreter
FAILED tests/orchestration/test_ci_workflow.py::test_hosted_workflow_matrix_names_exactly_the_floor_and_one_current_python
2 failed, 19 passed in 0.31s
m5_a_third_python_in_the_matrix restored byte-identical: True
control_after REAL_EXIT=0
21 passed in 0.29s
```
Every reading matches the reviewer's stated expectations exactly:
control_before/control_after 21 passed; m1 2 failed at the two named tests;
m2 2 failed at both parameters of `TestTheIndexFetch::test_any_fetch_failure_reads_unknown`;
m3 4 failed at the four named tests; m4 1 failed at
`TestTheCommand::test_offline_json_names_every_tool_with_three_columns`; m5
2 failed at the two named tests.
`git worktree remove --force .remedy-wt/f279-r6-mut` real exit 0, `git
worktree prune` real exit 0. `git worktree list` afterward → primary
checkout plus the two `.remedy-wt/job-*` worktrees only.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148):
byte-identity proof = mechanical disk-to-disk comparison of the applied
location against the `.agent/authored/` copy.

- This block (`f279-r6-block.md`): `.agent/authored/f279-r6-block.md` at
  C1a verified byte-identical to `.remedy-wt/f279-r6-block.md` (G1) and to
  the two readings given in the delegation message.
- All 8 product payloads (toolchain.py, test_toolchain.py,
  worker_facade_cmd.diff, command_catalog.diff, allowlist.diff,
  test_ci_workflow.diff, test_worker_facade_cmd.diff, mutations.py) plus the
  3 bookkeeping payloads (ledger.diff, plan.md, decisions.diff) — 11 total:
  each `.agent/authored/f279-r6-<name>` copy verified byte-identical to its
  `.remedy-wt/f279-r6-payloads/<name>` source (G1).
- Every `.diff` payload applied by `git apply` (never retyped): ledger,
  decisions (at C2), worker_facade_cmd, command_catalog, allowlist,
  test_ci_workflow, test_worker_facade_cmd (at C3) — all 7, `git apply
  --check` then `git apply`, real exit 0 both times, and the resulting
  tracked-file digests MATCH the reviewer's stated readings exactly at
  G2/G3.
- `plan.md` (rewrite, never retyped) and `toolchain.py`/`test_toolchain.py`
  (new files, never retyped): all three by `shutil.copyfile` from their
  payloads; the resulting on-disk digests MATCH the reviewer's stated G2/G3
  readings exactly.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 309 insertions, matches 232+77 formula |
| C1b | done | 393 insertions, matches expectation |
| C2 | done | round 5's PASS booked, DECISION F279 D6 recorded, all three insertion counts match |
| C3 | done | report, command and guards landed, all seven counts match |
| C4 | done | this handback |
| G1 TRANSPORT | done | all 12 authored copies byte-identical to source |
| G2 THE BOOKKEEPING | done | all 3 digests match, 26/26 open-finding set empty diff, 0/1 Gate-line count matches, file-list matches |
| G3 THE REPORT | done | file-list and all 7 digests match, no stop needed |
| G4 THE TESTS | done | 1762 passed, exit 0, ruff clean exit 0, integrity check 5/5 pass exit 0, doctor toolchain table pasted exit 0, integrity block 7/7 OK exit 0 |
| G5 THE RED PROOFS | done | control/m1-m5/control_after all match reviewer's exact readings, worktree cleaned up |
| G6 TREE AND PUSH | done | reported in the session's final reply, not this file, since it runs after C4 |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1a, C1b, C2, C3,
C4) exactly and touched exactly the tracked path set constraint 3 names —
confirmed by `git diff --name-only 86e12317 HEAD` before C4 was written.

No oversize commit this round (largest was C1b's 393 insertions, well under
the 500 cap; F279's one declared oversize commit remains round 1's C5).

One transient procedural slip, self-corrected and recorded here per
R-0485: the first `ruff check` invocation for G4 mistakenly included
`tests/orchestration/import_reachability_allowlist.txt` (not a Python
file) in its path list, producing spurious `F821` findings; the reading
reported above and in G4 is the corrected re-run over the Python paths
only, `All checks passed!` at real exit 0. No payload was retyped or
edited in either attempt.

No other sandbox friction beyond the block's own anticipated shapes: every
measurement script was written to a file under
`.remedy-wt/f279-r6-scratch/` and run with `python3 <file>` or `bash -c`,
never as an inline heredoc or `VAR=x cmd` shape; no payload was retyped or
edited.

No other procedural deviation. Nothing was merged this round, per
constraint 5. No `remedy/job-*` branch or self-use worktree was created,
touched or deleted beyond the round's own `.remedy-wt/f279-r6-mut`, which
was created and removed within G5 per constraint 6. The full suite was not
run, per constraint 7 (amend0917 rule 1) — F279's one full-suite run
belongs to its closure.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 6,
then T004's order half — `docs/orders/toolchain-refresh.md`, its docs test
and the self-use generator's fourteen-day tier. Open findings: 26. Operator
questions: 0.
