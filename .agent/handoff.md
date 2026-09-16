# Handoff — F280 round 2

## Session

SESSION 1 of feature F280 · round 2 · rounds so far 2

Context self-assessment: the round was three record commits and three table-applied code commits
driven by scripts, plus one full serial suite run, and the worker's context stayed comfortable.

## Range

Review of `4e93c22c`..`HEAD`.

## Commits

### 7af33af1 F280 R2 C0a: save the round 2 step block under the authored directory
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f280-r2.md` | +319 / -0 | the block file the delegating message names, copied with `shutil.copyfile`, sha256 `fa7f1ba7…9900c5a4` verified before and after the copy |

### b3906ab4 F280 R2 C0b: mirror the round 2 step block into the last block state file
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +248 / -301 | the same bytes, byte-identical to the C0a copy |

### f53f109e F280 R2 C1: book round 1's PASS, register R-0932 to R-0934, re-point the plan and record DECISION F280 D2
The FIRST SUBSTANTIVE COMMIT of the round. Commit total +46 / -19.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +18 / -19 | full replacement by PLAN2 |
| `.agent/live_review.md` | +8 / -0 | RECORD2 appended: `Gate: F280 R1` PASS, R-0932, R-0933, R-0934 |
| `.agent/decisions.md` | +14 / -0 | DEC2 appended, DECISION F280 D2 |
| `docs/roadmap/features/T2_F268.md` | +2 / -0 | pair P268, REWRITE: R-0933 resolution line |
| `docs/roadmap/features/T2_F273.md` | +2 / -0 | pair P273, REWRITE: R-0932 resolution line |
| `docs/roadmap/features/T2_F280.md` | +2 / -0 | pair P280, REWRITE: R-0934 resolution line |

### 787f3b74 F280 R2 C2: delete the ping-pong path of do run with the flags only it reads, per DECISION F280 D2
Commit total +158 / -813, applied from the committed carrier by its 53 rows in file order.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f280-r2-path.jsonl` | +53 / -0 | the table carrier, sha256 `df98e2a6…61cd16` verified before and after the copy |
| `apps/cli/command_catalog.py` | +1 / -17 | rows 1-17: the sixteen ping-pong-only flags leave `do.run`; goal help no longer names a prompt file |
| `apps/cli/commands/do_cmd.py` | +4 / -413 | rows 18-26: `_cmd_do_pingpong`, `pingpong_effective_model`, `_print_scope_summary`, `_resolve_timeout_precedence`, `_VALID_PINGPONG_PROVIDERS`, the prelude, the ping-pong branch and the `run show` scope block go |
| `apps/cli/grouped.py` | +4 / -22 | rows 27-36: dead special-cases of the deleted flags; quick start rewritten onto `do run --repo . --json` and `job show $JOB_ID --full` |
| `docs/system/vocabulary.md` | +1 / -1 | row 46: DECISION F259 D2 names the task file in the past tense |
| `packages/orchestration/pingpong_provider.py` | +2 / -2 | rows 41-42: both provider messages name `--builder-provider` and `--reviewer-provider` |
| `tests/cli/test_cli_ux.py` | +32 / -5 | rows 37-38: quick-start tests move to `JOB_ID`/`job show`; new `test_quick_start_flags_are_declared_by_their_commands` |
| `tests/cli/test_do_cmd_pingpong_budget.py` | +0 / -128 | row 47: deleted, it drove only `_cmd_do_pingpong` |
| `tests/cli/test_product_spine.py` | +2 / -2 | row 39: `job show` in the quick start |
| `tests/cli/test_scope_plan.py` | +0 / -38 | row 52: the text-report scope summary test goes |
| `tests/orchestration/test_pingpong.py` | +7 / -0 | row 43: API-key message names the provider flags |
| `tests/orchestration/test_pingpong_cli.py` | +8 / -1 | rows 44-45: claude-cli message names the provider flags; write-mode catalog test reads `job.run` |
| `tests/orchestration/test_provider_retry.py` | +2 / -26 | row 48: `_resolve_timeout_precedence` tests go |
| `tests/orchestration/test_repair_loop.py` | +2 / -122 | rows 49-50: `do.run` repair-rounds dispatch tests go |
| `tests/orchestration/test_stream_evidence_integration.py` | +2 / -35 | row 51: `do.run` stream-evidence dispatch test goes |
| `tests/test_cli_execution_loop_closure.py` | +1 / -1 | row 40 |
| `tests/test_command_catalog.py` | +37 / -0 | row 53: `TestDeletedFlags` pins every deleted flag of `do run` and `job run` as undeclared |

### 8bd055d9 F280 R2 C3: delete the scope plan module and run_pingpong's scope branches, per DECISION F280 D2
Commit total +200 / -1285, applied from the committed carrier by its 11 rows in file order.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f280-r2-scope.jsonl` | +11 / -0 | the table carrier, sha256 `1c99303d…1a8756` verified before and after the copy |
| `packages/orchestration/pingpong_loop.py` | +1 / -24 | rows 2-7: `scope_data`/`scope_validation` parameters and both scope-contract branches go |
| `packages/orchestration/scope_plan.py` | +0 / -609 | row 1: deleted whole |
| `tests/cli/test_scope_plan.py` | +0 / -651 | row 11: deleted |
| `tests/cli/test_task_input.py` | +188 / -0 | rows 9-10: the scope-free report and flow tests move here |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | row 8: `packages.orchestration.scope_plan` line goes |

### 298cd353 F280 R2 C4: turn argparse prefix matching off for every parser, per DECISION F280 D2
Commit total +32 / -0, applied from the committed carrier by its 4 rows in file order.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f280-r2-abbrev.jsonl` | +4 / -0 | the table carrier, sha256 `5f4f42bb…a3560` verified before and after the copy |
| `apps/cli/grouped.py` | +3 / -0 | rows 1-3: `allow_abbrev=False` on root, group and command parsers |
| `tests/test_command_catalog.py` | +25 / -0 | row 4: every deleted flag refused by the parser with exit 2; surviving full flags still parse |

### The handback commit, C5 (this commit)
| Path | Reason |
|---|---|
| `.agent/handoff.md` | this rewrite |

### Item status — the block's ordered bundle

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | all 53 rows read their expected counts |
| C3 | done | all 11 rows read their expected counts |
| C4 | done | all 4 rows read their expected counts |
| C5 | done | this commit; the push follows it |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f280r2w/wt 298cd353…` (G5) | created |
| `git worktree remove --force .remedy-wt/f280r2w/wt` (G5) | removed; `git worktree list` one row |
| `git push origin feature/f280-cli-vocabulary-v2-part-two` | run after this commit; outcome in the completion message |

No pull request. No `remedy` CLI invocation. No runner or `run_job` call by the worker.

## Verification

STOP reads before C0a, C2 and C5: `ls .agent/STOP` → exit 2, `No such file or directory`, each time.
`git branch --list 'remedy/job-*'` read 17 lines at the start, after G5 and after G6.

### G1 TRANSPORT — exit 0 (`gate_g1g2.py`)

    PASS G1 authored sha256 == delegated digest  fa7f1ba70e4b7c4987b54f359d7ed350ac5cfe0ab8f9f3a5989e26049900c5a4
    PASS G1 last_block at C0b byte-identical
    PASS G1 slices FOUND 9, each matches its BEGIN digest
    block measured: TOTAL 319, CONTENT 84, PROSE 235; no single-character-run line; every header rule 2 characters
    carriers: path df98e2a6…, scope 1c99303d…, abbrev 5f4f42bb… — each committed copy equals its digest

### G2 THE RECORD at C1 — exit 0 (same script)

    PASS G2 plan == PLAN2, 38 lines, Goal 1, Next Steps 1
    PASS G2 live_review == base + RECORD2
    PASS G2 decisions == base + DEC2
    PASS G2 P268 / P273 / P280: base FROM 1; C1 FROM 0 TO 1; C1 == base with pair
    PASS G2 Gate lines base=28 c1=29; Gate: F280 R1 base=0 c1=1
    PASS G2 distinct ids base=127 c1=130; C1 minus base = R-0932, R-0933, R-0934
    PASS G2 distinct Done ids base=2 c1=2; open set base=125 c1=128
    python3 -B -m pytest -q tests/docs/ → exit 0, 310 passed in 1.24s

### G3 THE TABLES — exit 0 for each commit (`gate_g3.py`)

    C2 787f3b74: name-only 17 paths == carrier + the 16 named; single parent
         apps 733555aa…, packages 6f7b4b38…, tests 7bcf67a9… — all equal; insertions 158 (deletions 813)
    C3 8bd055d9: name-only 6 paths == carrier + the 5 named; single parent
         apps 733555aa…, packages ed64c3a4…, tests 9b4de341… — all equal; insertions 200 (deletions 1285)
    C4 298cd353: name-only 3 paths == carrier + the 2 named; single parent
         apps 725c9980…, packages ed64c3a4…, scripts 4bea3f9f…, tests 9ff3aca0…, docs/guides 52e345b7…,
         docs/system e730766a…, docs/README.md c282d425…, README.md 3c6b8d40…, .claude e3cd5e0a… — all nine equal;
         insertions 32 (deletions 0)
    python3 -B -m pytest -q tests/cli/test_golden_path.py (primary checkout at C2) → exit 0, 42 passed in 17.68s

### G4 THE SWEEP at C4 — exit 0 (`gate_g4.py`, gates carrier sha256 e3ade034… match)

    ls-tree C4: scope_plan.py '', test_scope_plan.py '', test_do_cmd_pingpong_budget.py '', pingpong_loop.py blob
    deleted          base 181/8   C2 111/5   C3 8/2    C4 8/2
    deleted_flags    base 48/8    C2 22/5    C3 22/5   C4 23/5
    quick_start_old  base 5/2     C2 2/1     C3 2/1    C4 2/1
    control          base 89/14   C2 89/14   C3 89/14  C4 89/14        (lines/files, all as expected)
    deleted at C4:
      packages/orchestration/pingpong_evidence.py:153,155,157,158,159,160,173  (the `scope_plan` manifest field, R-0932)
      tests/cli/test_task_input.py:414  "# Reports and flows with no scope plan (moved from tests/cli/test_scope_plan.py)"
    quick_start_old at C4:
      packages/orchestration/pingpong_loop.py:4262  "remedy run show $RUN_ID --json",
      packages/orchestration/pingpong_loop.py:4265  "remedy run show $RUN_ID",
    python3 -m ruff check over 15 paths → exit 0, All checks passed!

### G5 THE RED-PROOF — driver exit 0 (carrier sha256 77d44762…c0a4ab match)

do_cmd loaded from `.remedy-wt/f280r2w/wt/apps/cli/commands/do_cmd.py` on every run; every FROM
occurred exactly once; worktree status after the restores `''`.

    CONTROL                                   exit 0  349 passed in 5.10s
    M1-do-run-builder-argdef                  exit 1  2 failed, 347 passed — node among failed
    M2-old-quick-start-step-1                 exit 1  1 failed, 348 passed — node failed
    M3-old-api-key-hint                       exit 1  1 failed, 348 passed — node failed
    M4-job-run-builder-argdef                 exit 1  2 failed, 347 passed — node among failed
    M5-old-claude-cli-hint                    exit 1  1 failed, 348 passed — node failed
    M6-command-parsers-allow-abbrev-reverted  exit 1  1 failed, 348 passed — node failed

M1 also failed `test_parser_refuses_a_deleted_flag_as_an_abbreviation[do.run:--builder]`, and M4
`test_parser_refuses_a_deleted_flag_as_an_abbreviation[job.run:--builder]`. After the removal
`git worktree list` read one row and `git branch --list 'remedy/job-*'` 17 lines.

### G6 THE SUITE, SPEC S at C4 — exit 0 (`spec_suite.py`)

    python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs  (PYTHONPATH, REMEDY_PROJECT,
      REMEDY_DATA_DIR removed; PYTHONDONTWRITEBYTECODE=1; primary checkout)
    rc 0 — 17634 passed, 23 skipped, 1 warning in 1238.56s (0:20:38)
    distinct bad nodes: 0

G7 runs after this commit and the push; it is reported in the completion message only.

## Authored-text proofs

The nine slices were extracted as the bytes strictly between their `BEGIN` and `END` lines and
each matched its BEGIN-marker sha256 before use; none was edited and no marker line reached a file.
The applied results were re-read from the git objects at C1 (G2). The three tables were applied
from the committed-path copies of their carriers, byte-identical to the block's digests, and the
resulting trees equal the reviewer's dry run (G3).

## Deviations & assumptions

None to the ordered commit sequence: C0a, C0b, C1, C2, C3, C4 and C5 in that order, each
single-parent, on `4e93c22c`. Declared:

1. The first STOP read was issued inside a compound shell command, which the guard refused by
   form before running anything; it was re-issued alone as `ls .agent/STOP` (exit 2).
2. A later compound read of `pyproject.toml` and the mutation carrier also listed `.remedy-wt/`
   itself, one level, which constraint 4 does not name; no other directory under it was opened.
3. The first `tests/docs/` run at C1 was piped through `tail`, which hides the exit code; the G2
   reading is from the standalone re-run, whose exit 0 the shell tool surfaces by not erroring.
   An attempt to print `$?` was refused by form.
4. The first `git worktree add` named a mistyped short sha and exited 128 without creating
   anything; it was re-run with the full C4 sha.
5. Beyond the gates, `python3 -m ruff check` ran over each table's `.py` paths before its commit,
   as part of the self-review loop; each printed `All checks passed!`.

## Next

1. Phase 1 rule 1: re-read `.agent/STOP` from disk before anything else.
2. The reviewer's verdict on round 2, with the resolutions of R-0767 and R-0894.
3. `job budget <id> set`, R-0906 and R-0909.

Open findings: 128 by distinct id, with the High ids R-0803, R-0804 and R-0807.

Operator questions open: 1
