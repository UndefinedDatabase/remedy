# Handoff — F280 round 3

## Session

SESSION 1 of feature F280 · round 3 · rounds so far 3

Context self-assessment: the round was three record commits and two table-applied commits driven
by scripts, plus one worktree red-proof and one full serial suite run, and the worker's context
stayed comfortable.

`.agent/STOP` APPEARED DURING THIS ROUND: absent at the reads before C0a and before C2, present
at the read before C4 (an empty untracked file, created 2026-09-16 18:54:13 +0200, while the
SPEC S suite was running). Per constraint 2 the worker wrote this handoff, pushes, and stops.
No committed code searches for or writes that path except one text assertion in
`tests/test_agent_tooling.py`, so it is read as the operator's sentinel; it was left untouched
and is not committed.

## Range

Review of `4806b03c`..`HEAD`.

## Commits

Commit totals, each the first and second column of `git show --numstat --format= <commit>`
summed over its paths:

| Commit | +/- | Block item |
|---|---|---|
| `cb4aa3fe` | +315 / -0 | C0a |
| `933ff1bd` | +177 / -181 | C0b |
| `27576f94` | +59 / -15 | C1 |
| `0e34d3ab` | +345 / -23 | C2 |
| `759b3484` | +47 / -177 | C3 |

### cb4aa3fe F280 R3 C0a: save the round 3 step block under the authored directory
| Path | file +/- | Reason |
|---|---|---|
| `.agent/authored/f280-r3.md` | +315 / -0 | the block file the delegating message names, copied with `shutil.copyfile`; sha256 `b2f2cf96…0d8431` before and after |

### 933ff1bd F280 R3 C0b: mirror the round 3 step block into the last block state file
| Path | file +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +177 / -181 | the same bytes, byte-identical to the C0a copy |

### 27576f94 F280 R3 C1: book round 2's PASS, register R-0935 and R-0936, re-point the plan and record DECISIONs F280 D3 and D4
The FIRST SUBSTANTIVE COMMIT of the round.
| Path | file +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +15 / -15 | full replacement by PLAN3 |
| `.agent/live_review.md` | +10 / -0 | RECORD3 appended: `Gate: F280 R2` PASS, `Done:` R-0767 and R-0894, R-0935, R-0936 |
| `.agent/decisions.md` | +24 / -0 | DEC3 appended, DECISIONs F280 D3 and D4 |
| `docs/roadmap/features/T2_F273.md` | +4 / -0 | pair P273, REWRITE: R-0935 and R-0936 Acceptance lines |
| `docs/roadmap/features/T2_F280.md` | +6 / -0 | pair P280, REWRITE: the D3/D4 amendment paragraph |

### 0e34d3ab F280 R3 C2: build job budget set over the run contract's budget fields and the token budget profile, per DECISION F280 D3
Applied from the committed carrier by its 16 rows in file order; every edit row read its count.
| Path | file +/- | Reason |
|---|---|---|
| `.agent/authored/f280-r3-budget.jsonl` | +16 / -0 | the table carrier, sha256 `9ec801c5…952494` before and after the copy |
| `apps/cli/command_catalog.py` | +8 / -2 | row 1: `job.budget` gains `action`, `field`, `value`; `write_metadata` |
| `apps/cli/commands/job.py` | +104 / -5 | rows 2-4: `_cmd_job_budget_route`, `_cmd_job_budget_set`, field tuples, dispatch |
| `packages/orchestration/run_contract.py` | +2 / -1 | rows 5-6: zero and exhausted test budgets name `job budget <job_id> set max_test_runs <n>` |
| `packages/orchestration/test_execution_service.py` | +2 / -0 | row 7: `contract_guidance` names the write with the job's id |
| `tests/orchestration/test_job_budgets.py` | +1 / -1 | row 8: comment no longer cites `read_only` |
| `tests/cli/test_job_budget_set.py` | +187 / -0 | row 9: created, 16 tests |
| `docs/system/token-economy-context-budget-optimizer-v0.md` | +4 / -3 | row 10 |
| `docs/guides/token-economy-user-guide-v0.md` | +5 / -4 | row 11 |
| `docs/system/real-test-execution-v1.md` | +3 / -2 | row 12 |
| `docs/system/run-contract-v1.md` | +8 / -4 | rows 13-14 |
| `docs/system/job-budget-enforcement-v0.md` | +5 / -1 | rows 15-16 |

### 759b3484 F280 R3 C3: delete job fulfill with its fixture-demo switch and tests, per DECISION F280 D4
Applied from the committed carrier by its 23 rows in file order; every edit row read its count.
| Path | file +/- | Reason |
|---|---|---|
| `.agent/authored/f280-r3-fulfill.jsonl` | +23 / -0 | the table carrier, sha256 `c3675d0d…69326c` before and after the copy |
| `apps/cli/command_catalog.py` | +0 / -15 | row 1: `job.fulfill` entry goes |
| `apps/cli/commands/job.py` | +0 / -59 | rows 2-3: `_cmd_job_fulfill` and its dispatch entry go |
| `apps/cli/grouped.py` | +0 / -2 | row 4: `--fixture-demo` special case goes |
| `tests/test_command_catalog.py` | +1 / -0 | row 5: `job.fulfill` into `TestDeletedCommands` |
| `tests/orchestration/test_job_fulfillment.py` | +0 / -88 | rows 6-11: CLI, catalog and doc-mention tests of the command go |
| `docs/system/first-fulfilled-job-demo-v0.md` | +13 / -4 | rows 12-14: dated banner, past tense |
| `docs/guides/simple-operator-quickstart-v0.md` | +5 / -4 | rows 15-18 |
| `docs/system/core-product-spine-v0.md` | +0 / -1 | row 19 |
| `docs/system/real-test-execution-v1.md` | +1 / -1 | row 20 |
| `docs/system/run-contract-v1.md` | +1 / -1 | row 21 |
| `docs/system/first-perfect-job-demo-v0.md` | +2 / -1 | row 22 |
| `docs/README.md` | +1 / -1 | row 23 |

### The handback commit, C4 (this commit)
| Path | Reason |
|---|---|
| `.agent/handoff.md` | this rewrite |

### Item status — the block's ordered bundle

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | all 16 rows applied, every count as stated |
| C3 | done | all 23 rows applied, every count as stated |
| C4 | done | this commit; the push follows it; `.agent/STOP` present, so the worker stops after the push |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f280r3w/wt <guessed sha>` | exit 128, `invalid reference`, nothing created (see Deviations 2) |
| `git worktree add --detach .remedy-wt/f280r3w/wt 759b3484dd2a00ede51fee98c9d161726410f98a` (G5) | created |
| `git worktree remove --force .remedy-wt/f280r3w/wt` (G5) | removed; `git worktree list` one row |
| `git push origin feature/f280-cli-vocabulary-v2-part-two` | run after this commit; outcome in the completion message |

No pull request. No `remedy` CLI invocation. No runner or `run_job` call by the worker.

## Verification

STOP reads, by `os.path.exists` in a one-line Python probe that exits 0 when present:
before C0a exit 1 (`exists False`), before C2 exit 1 (`exists False`), before C4 exit 0
(`exists True`). `git branch --list 'remedy/job-*'` read 17 lines at the start, after G5 and
after G6. The block measured on its final bytes: TOTAL 315, CONTENT 94, PROSE 221; no line of a
single repeated character; all 8 header rules two characters.

### G1 TRANSPORT — exit 0 (`gate_g1g2.py`)

    PASS G1 authored sha256 == delegated digest b2f2cf96675597fee363122dc153a0e107dd0ba599994fb7be8634082c6d8431
    PASS G1 last_block at C0b byte-identical
    PASS G1 slice PLAN3 / RECORD3 / DEC3 / P280-FROM / P280-TO / P273-FROM / P273-TO digest
    PASS G1 slices FOUND 7
    carriers: budget 9ec801c5…, fulfill c3675d0d… — each committed copy equals its digest (apply_table.py)

### G2 THE RECORD at C1 — exit 0 (same script)

    PASS G2 plan == PLAN3, 38 lines, Goal 1, Next Steps 1
    PASS G2 live_review == base + RECORD3
    PASS G2 decisions == base + DEC3
    PASS G2 P280 / P273: base FROM 1; C1 FROM 0 TO 1; C1 == base with pair
    PASS G2 Gate lines base=29 c1=30; Gate: F280 R2 base=0 c1=1
    PASS G2 distinct ids base=130 c1=132 delta=['R-0935', 'R-0936']
    PASS G2 distinct Done ids base=2 c1=4 delta=['R-0767', 'R-0894']
    PASS G2 open set base=128 c1=128
    python3 -B -m pytest -q tests/docs/ → exit 0, 310 passed in 1.24s

### G3 THE TABLES — exit 0 for each commit (`gate_g3.py`)

    C2 0e34d3ab: single parent 27576f94; name-only 12 paths == carrier + the 11 named
         apps 3bda6ea6, packages e5d99f30, scripts 4bea3f9f, tests d49f307a, docs/guides b1a68d32,
         docs/system d5b2ad11, docs/README.md c282d425, README.md 3c6b8d40, .claude e3cd5e0a — all nine equal
         insertions 345 (deletions 23)
    C3 759b3484: single parent 0e34d3ab; name-only 13 paths == carrier + the 12 named
         apps 068608a3, packages e5d99f30, scripts 4bea3f9f, tests 1c14c8b8, docs/guides 969f52e3,
         docs/system 3d77ab79, docs/README.md 0f1933b9, README.md 3c6b8d40, .claude e3cd5e0a — all nine equal
         insertions 47 (deletions 177)
    python3 -B -m pytest -q tests/cli/test_golden_path.py (primary checkout at C2) → exit 0, 42 passed in 17.97s

### G4 THE SWEEP at C3 — exit 0 (`gate_g4.py`, gates carrier sha256 0315f9e2… match)

    newword          base 0/0      C2 11/8     C3 12/9
    fulfill          base 33/11    C2 33/11    C3 11/8
    control_create   base 107/41   C2 107/41   C3 106/41
    control_propose  base 59/12    C2 59/12    C3 59/12        (lines/files, all as expected)
    fulfill at C3:
      docs/system/first-fulfilled-job-demo-v0.md:4, :34, :51   (the dated banner and past-tense lines)
      docs/system/first-perfect-job-demo-v0.md:84
      docs/system/real-test-execution-v1.md:15
      docs/system/run-contract-v1.md:56
      packages/orchestration/job_fulfillment.py:6, :617        (module docstrings, kept under D17)
      packages/orchestration/orchestrator_loop.py:1494         (comment)
      tests/orchestration/test_orchestrator_loop.py:1619       (comment)
      tests/test_command_catalog.py:336                        ("job.fulfill" in TestDeletedCommands)
    python3 -m ruff check over 9 paths → exit 0, All checks passed!

### G5 THE RED-PROOF — driver exit 0 (`redproof_driver.py`)

`apps.cli.commands.job` loaded from `.remedy-wt/f280r3w/wt/apps/cli/commands/job.py` on every run;
every FROM occurred exactly once; worktree status after the restores `''`.

    budget carrier 783cebe3… match, over tests/cli/test_job_budget_set.py
    CONTROL                                     exit 0  16 passed in 0.65s
    m1-contract-write-skipped                   exit 1  2 failed, 14 passed — node among failed
    m2-token-write-skipped                      exit 1  1 failed, 15 passed — node failed
    m3-floor-refusal-removed                    exit 1  2 failed, 14 passed — node among failed
    m4a-zero-budget-next-action-reverted        exit 1  2 failed, 14 passed — node among failed
    m4b-exhausted-budget-next-action-reverted   exit 1  1 failed, 15 passed — node failed
    m4c-test-run-guidance-reverted              exit 1  1 failed, 15 passed — node failed
    m5-job-budgets-refusal-removed              exit 1  1 failed, 15 passed — node failed
    m6-action-not-set-accepted                  exit 1  1 failed, 15 passed — node failed
    fulfill carrier 0884ccae… match, over tests/test_command_catalog.py and tests/cli/test_advertised_commands.py
    CONTROL                                     exit 0  65 passed in 1.08s
    M1-catalog-entry                            exit 1  1 failed, 64 passed — node failed
    M2-doc-advertisement                        exit 1  1 failed, 64 passed — node failed

Extra failed nodes: m1 also `TestR0906TheTestRunBudget::test_a_persisted_contract_keeps_every_other_field`;
m3 also `TestRefusals::test_each_exits_2_names_the_way_out_and_writes_no_store[contract-below-floor]`;
m4a also `TestTheRefusalNamesTheWrite::test_test_run_names_the_write_with_the_jobs_id`. After the
removal `git worktree list` read one row and `git branch --list 'remedy/job-*'` 17 lines.

### G6 THE SUITE, SPEC S at C3 — exit 0 (`spec_suite.py`)

    python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs  (PYTHONPATH, REMEDY_PROJECT,
      REMEDY_DATA_DIR removed; PYTHONDONTWRITEBYTECODE=1; primary checkout)
    rc 0 — 17643 passed, 23 skipped, 1 warning in 1184.21s (0:19:44)
    distinct bad nodes: 0

G7 runs after this commit and the push; it is reported in the completion message only. Its
`git status --porcelain` reading will show `?? .agent/STOP`, the sentinel the worker leaves alone.

## Authored-text proofs

The seven slices were extracted as the bytes strictly between their `BEGIN` and `END` lines and
each matched its BEGIN-marker sha256 before use; none was edited and no marker line reached a file.
The applied results were re-read from the git objects at C1 (G2). The two tables were applied
from the committed-path copies of their carriers, byte-identical to the block's digests, and the
resulting trees equal the reviewer's dry run (G3).

## Deviations & assumptions

None to the ordered commit sequence: C0a, C0b, C1, C2, C3 and C4 in that order, each
single-parent, on `4806b03c`. Declared:

1. `.agent/STOP` appeared between the read before C2 and the read before C4. Nothing was
   half-written; the worker writes this handoff, pushes and stops, and neither deletes nor
   commits the file. `.agent/plan.md` is not amended with it, because the block binds the plan
   to PLAN3 and C4's change set to `.agent/handoff.md`; this section carries it instead.
2. The first `git worktree add` named a guessed full sha for C3 and exited 128 without creating
   anything; it was re-run with the sha `git rev-parse 759b3484` printed.
3. The first STOP read used `test -e` in the shell tool, which returned no output and no error
   report; since that is not an unambiguous exit code, it was re-issued at once as the Python probe
   above, which read `exists False`, exit 1. A first compound state probe was refused by the shell
   guard by form before running anything.
4. `tests/docs/` at C1 was first run with an added `-p no:cacheprovider`; the G2 reading is the
   re-run of the exact command the gate names.
5. `## Commits` carries one commit-total row per commit whose `+/-` cell is constraint 5's reading,
   and keeps the template's per-commit changed-files tables with the column named `file +/-`.
6. Beyond the gates, `python3 -m ruff check` ran over each table's `.py` paths before its commit,
   as part of the self-review loop; each printed `All checks passed!`.

## Next

1. Phase 1 rule 1: `.agent/STOP` exists — write the handoff, end the session, do nothing else,
   until the operator removes it.
2. The reviewer's verdict on round 3.
3. Moving the fixtures and smoke sections off `job create`, then deleting `job create`.

Open findings: 128 by distinct id, with the High ids R-0803, R-0804 and R-0807.

Operator questions open: 1
