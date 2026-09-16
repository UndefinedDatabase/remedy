# Handoff — F280 round 1

## Session

SESSION 1 of feature F280 · round 1 · rounds so far 1

Context self-assessment: the round was four record commits and one table-applied code commit with
script-driven gates, and the worker's context stayed comfortable throughout.

## Range

Review of `9f1b6d25`..`HEAD`.

## Commits

### 11454c29 F280 R1 C0a: save the round 1 step block under the authored directory
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f280-r1.md` | +372 / -0 | the block file the delegating message names, copied with `shutil.copyfile`, sha256 `e0160539…0043c9da` verified before and after the copy |

### be2271d3 F280 R1 C0b: mirror the round 1 step block into the last block state file
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +335 / -167 | the same bytes, byte-identical to the C0a copy |

### cadd1e81 F280 R1 C1: re-point the plan, re-head the review record, book F261 round 28 and its prose slip, and record DECISION F280 D1
The FIRST SUBSTANTIVE COMMIT of the round. Commit total +67 / -40.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +26 / -23 | full replacement by PLAN1 |
| `.agent/live_review.md` | +20 / -17 | head swap to HEAD1 on `^## Findings$`, carried region byte-identical, RECORD1 appended (`Gate: F261 R28`) |
| `.agent/decisions.md` | +14 / -0 | DEC1 appended, DECISION F280 D1 |
| `.agent/prose_slips.md` | +2 / -0 | SLIP1 appended |
| `docs/roadmap/features/T2_F280.md` | +5 / -0 | pair PF, APPEND-shaped: PF-FROM's one occurrence replaced by AMEND1 |

### 5716d3a7 F280 R1 C2: claim F280 on the STATUS line and re-point the context file
Commit total +19 / -17.
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1 / -1 | pair PS, REWRITE: F280 `[ ]` to `[~]` |
| `.agent/context.md` | +18 / -16 | full replacement by CTX1 |

### 290bd0ed F280 R1 C3: hand job run's provider flags to the runner, delete its builder and reviewer flags and refuse fixture, per DECISION F280 D1
Commit total +134 / -47, applied from the committed carrier by its 21 rows in file order.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f280-r1-jobrun.jsonl` | +21 / -0 | the table carrier, sha256 `91c80c25…a4b92f` verified before the copy |
| `apps/cli/command_catalog.py` | +2 / -4 | rows 1-3: `--builder`/`--reviewer` leave `job.run`; provider flag descriptions name the four buildable providers |
| `apps/cli/commands/do_cmd.py` | +4 / -15 | rows 4-8: `_VALID_ROLE_PROVIDERS` drops `fixture`; `_cmd_job_run` loses `builder`/`reviewer` and hands `builder_provider`/`reviewer_provider` to `run_job`; dispatch entry updated |
| `tests/orchestration/test_job_run_refs.py` | +2 / -2 | row 9: drives `job run` with the provider flags |
| `tests/orchestration/test_job_task_runner.py` | +23 / -23 | rows 11-19: handler calls move to `builder_provider`/`reviewer_provider` |
| `tests/orchestration/test_job_worktree_handoff.py` | +1 / -1 | row 10: same move |
| `tests/test_role_override_flags.py` | +81 / -2 | rows 20-21: `fixture` parse case moves to `fake`; new `TestJobRunProviderWiring` |

### The handback commit, C4 (this commit)
| Path | Reason |
|---|---|
| `.agent/handoff.md` | this rewrite |

### Item status — the block's ordered bundle

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | branch cut from `9f1b6d25` |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | all 21 table rows read their expected counts |
| C4 | done | this commit; the push follows it |

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]`, Open PR Gate clear |
| `git checkout -b feature/f280-cli-vocabulary-v2-part-two 9f1b6d25…` | branch created |
| `git worktree add --detach .remedy-wt/f280r1w/wt 290bd0ed…` (G5) | created |
| `git worktree remove --force .remedy-wt/f280r1w/wt` (G5) | removed; `git worktree list` one row |
| `git push -u origin feature/f280-cli-vocabulary-v2-part-two` | run after this commit; outcome in the completion message |

No pull request. No `remedy` CLI invocation. No runner or `run_job` call by the worker.

## Verification

STOP reads before C0a, C3 and C4: `ls .agent/STOP` → exit 2, `No such file or directory`, each time.
`git branch --list 'remedy/job-*'` read 17 lines at the start, after G5 and before C4.

### G1 TRANSPORT — exit 0 (`gate_g1g2.py`)

    PASS G1 authored sha256 == delegated digest (e0160539e502a0c73d2de3eb4f32190b065d94fe8e7915ecc41d3afe0043c9da)
    PASS G1 last_block at C0b byte-identical
    PASS G1 slices FOUND 10, all match
    block measured: TOTAL 372, CONTENT 154, PROSE 218; no single-character-run line; every header rule 2 characters

### G2 THE RECORD at C1 — exit 0 (same script)

    PASS G2a plan == PLAN1, 39 lines, ^## Goal$ once, ^## Next Steps$ once
    PASS G2b live_review == HEAD1 + carried + RECORD1
         carried region sha256 base=c1=899e94f06a7302e2b73abf7bdd57442ae49b86ae2371bfec50cee94a65792c02
    PASS G2c decisions == base + DEC1; prose_slips == base + SLIP1
    PASS G2d PF-FROM once at base; T2_F280 == base with FROM->AMEND1
    PASS G2e Gate lines base=27 c1=28; F261 R28 base=0 c1=1
    PASS G2e distinct ids 127/127; Done 2/2; open 125/125, identical membership

### G3 THE CLAIM at C2 — exit 0

    PASS PS-FROM 0, STATUS1 1; ^- \[~\]  once; [x] F\d{3} base=78 C2=78; context == CTX1
    python3 -B -m pytest -q tests/docs/                                  → exit 0, 310 passed in 1.23s
    python3 -B -m pytest -q tests/orchestration/test_roadmap_index.py    → exit 0, 30 passed in 0.38s

### G4 THE TABLE at C3 — exit 0

    git diff --no-renames --name-only 5716d3a7 290bd0ed → exactly the seven ordered paths
    rev-parse apps f3c2c62a…, packages ec2c3efd…, scripts 4bea3f9f…, tests 3d7381b4…,
      docs/guides 52e345b7…, docs/system cc426981…, README.md 3c6b8d40…, .claude e3cd5e0a… — all eight equal the dry run
    C3 numstat total +134 / -47
    python3 -m ruff check <six .py paths> → exit 0, All checks passed!

### G5 THE RED-PROOF — driver exit 0 (carrier sha256 56d2b309…dc864c6 match)

do_cmd loaded from `.remedy-wt/f280r1w/wt/apps/cli/commands/do_cmd.py` on every run; every FROM
occurred exactly once; worktree status after the restores `''`.

    CONTROL                          exit 0  243 passed in 101.82s
    M1-builder-name-not-wired        exit 1  12 failed, 231 passed  — node test_provider_flags_reach_run_job_as_the_role_names among failed
    M2-job-run-builder-flag-readded  exit 1  1 failed, 242 passed   — node test_deleted_role_flag_is_refused[--builder] failed
    M3-fixture-readmitted            exit 1  3 failed, 240 passed   — node test_fixture_provider_is_refused_with_exit_2[--builder-provider] among failed
    M4-reviewer-name-not-wired       exit 1  12 failed, 231 passed  — node test_each_provider_flag_reaches_its_own_role among failed

M1 and M4 each also failed the other `TestJobRunProviderWiring` wiring test,
`test_job_run_refs.py::TestJobRunRefsEndToEnd::test_run_refs_names_every_task_run_in_order` and nine
`test_job_task_runner.py` handler tests; M3 also failed the `--reviewer-provider` and
`--repair-provider` cases. Full node lists are in the completion message.

### G6 THE SUITES at C3 — each exit 0, serial, `python3 -B -m pytest -q -p no:randomly <path>`

    tests/test_role_override_flags.py                   30 passed
    tests/orchestration/test_job_run_refs.py            4 passed
    tests/orchestration/test_job_task_runner.py         209 passed
    tests/orchestration/test_job_worktree_handoff.py    26 passed
    tests/test_command_catalog.py                       31 passed
    tests/cli/test_advertised_commands.py               13 passed
    tests/cli/test_cli_ux.py                            72 passed
    tests/orchestration/test_live_review_rotation.py    10 passed
    tests/ui_server/                                    497 passed
    tests/orchestration/test_test_runner.py             50 passed
    tests/regression/test_resource_safety.py            21 passed
    tests/orchestration/test_integrity_gate.py          16 passed
    tests/cli/test_golden_path.py (canary)              42 passed

G7 runs after this commit and the push; it is reported in the completion message only.

## Authored-text proofs

The ten slices were extracted as the bytes strictly between their `BEGIN` and `END` lines and each
matched its BEGIN-marker sha256 before use; none was edited and no marker line reached a file. The
applied results were re-read from the git objects at C1 and C2 (G2, G3). The table was applied from
the committed-path copy of its carrier, byte-identical to the block's digest.

## Deviations & assumptions

None to the ordered commit sequence: C0a, C0b, C1, C2, C3 and C4 in that order, each single-parent,
on `9f1b6d25`. Declared:

1. The first STOP read was issued inside a compound shell command, which the guard refused by form
   before running anything; it was re-issued alone as `ls .agent/STOP` (exit 2).
2. The first G6 attempt was also a compound command refused by form; G6 then ran through
   `.remedy-wt/f280r1w/serial_suites.py`, one subprocess per path in the ordered sequence.
3. A first `tests/docs/` run was piped through `grep`, which hides the exit code; the G3 reading is
   from the standalone re-run. The two G3 pytest exit codes are the shell tool's: it surfaces any
   non-zero exit as an error, and neither run did.

## Next

1. Phase 1 rule 1: re-read `.agent/STOP` from disk before anything else.
2. The reviewer's verdict on round 1.
3. The deletion of the ping-pong path of `do run` with its flags and the scope plan, R-0894.

Open findings: 125 by distinct id, with the High ids R-0803, R-0804 and R-0807.

Operator questions open: 1
