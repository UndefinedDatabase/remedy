# Handoff — F261 round 24

## Session

SESSION 6 of feature F261 · round 24 · rounds so far 24

Context self-assessment: the round was one record commit and two measured tables of 29 and 30 rows,
every gate passed on its first run, and the worker's context stayed comfortable, with the full suite
the only long wait.

## Range

Review of `fc13ba87`..`HEAD`.

## Commits

### 021b3c33 F261 R24 C0a: save the round 24 step block under the authored directory
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r24.md` | +265 / -0 | the block file the delegating message names, copied with `shutil.copyfile`, sha256 `7ef435c5…e6de9a5` verified before and after the copy |

Insertions read by `git show --numstat --format= 021b3c33`: 265, deletions 0.

### 1fb1d5e1 F261 R24 C0b: mirror the round 24 step block into the last block state file
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +150 / -153 | the same bytes, byte-identical to the C0a copy |

Insertions: 150, deletions 153.

### a9ed91b4 F261 R24 C1: book round 23's PASS, register R-0931 for F273 and record DECISION F261 D23
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12 / -12 | full replacement by slice PLAN24 |
| `.agent/live_review.md` | +4 / -0 | slice RECORD24 appended — the `Gate: F261 R23` PASS paragraph and registration R-0931 |
| `.agent/decisions.md` | +12 / -0 | slice DEC23 appended — DECISION F261 D23 |
| `docs/roadmap/features/T2_F273.md` | +2 / -0 | pair P273D applied: the acceptance line for R-0931 |

Insertions: 30, deletions 12. This is the FIRST SUBSTANTIVE COMMIT of the round.

### 27dcd9e4 F261 R24 C2: delete job rerun with its handler, catalog entry, dispatch wiring and CLI-driven tests, by the rerun table
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r24-rerun.jsonl` | +29 / -0 | the edit table's own carrier, copied with `shutil.copyfile`, sha256 `a3ece98b…4f5c678bdbc7` verified |
| `README.md` | +0 / -1 | the `job rerun --check-manifest` quickstart line deleted |
| `apps/cli/command_catalog.py` | +0 / -16 | the `job.rerun` entry deleted |
| `apps/cli/commands/__init__.py` | +1 / -2 | `job_rerun_cmd` dropped from the import list and the handler loop |
| `apps/cli/commands/job_rerun_cmd.py` | +0 / -170 | the handler module of the deleted command |
| `packages/orchestration/run_manifest.py` | +2 / -2 | docstrings no longer name the deleted word |
| `packages/orchestration/worktrees.py` | +2 / -2 | docstrings no longer name the deleted word |
| `tests/cli/test_job_rerun_integrity_errors.py` | +1 / -33 | the CLI-driven class and its helper deleted; loader tests stay |
| `tests/cli/test_job_rerun_manifest.py` | +7 / -237 | the CLI-driven classes and helpers deleted; package-driven tests stay |
| `tests/orchestration/import_reachability_allowlist.txt` | +0 / -1 | the `job_rerun_cmd` line deleted |
| `tests/orchestration/test_run_manifest_input_coverage.py` | +1 / -2 | docstring re-worded |
| `tests/orchestration/test_run_manifest_integrity.py` | +1 / -11 | the CLI exit test deleted, section header re-worded |
| `tests/orchestration/test_run_manifest_reference_coverage.py` | +1 / -1 | comment re-worded |
| `tests/orchestration/test_run_manifest_strict_boundaries.py` | +0 / -2 | the deleted module's two path entries deleted |
| `tests/test_command_catalog.py` | +1 / -0 | `job.rerun` joins `TestDeletedCommands` |

Insertions: 46, deletions 480 — under the 500-insertion cap of constraint 5.

### 6f506cea F261 R24 C3: rename the group teach to teacher with its handler module, test file, handler functions and test classes, by the teacher table
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r24-teacher.jsonl` | +30 / -0 | the edit table's own carrier, copied with `shutil.copyfile`, sha256 `f9d47405…517242a2b` verified |
| `README.md` | +1 / -1 | the F255 line reads `remedy teacher narrate` and `remedy teacher ask` |
| `apps/cli/command_catalog.py` | +7 / -7 | group `teacher`, ids `teacher.narrate` and `teacher.ask`, `related=` and the test-file comment |
| `apps/cli/commands/__init__.py` | +2 / -2 | `teacher_cmd` in the import list and the handler loop |
| `apps/cli/commands/teach_cmd.py` → `teacher_cmd.py` | +8 / -8 | moved; `_cmd_teacher_*`, dispatch keys and docstrings |
| `packages/orchestration/teacher_model.py` | +1 / -1 | docstring names `remedy teacher ask` |
| `packages/orchestration/teacher_qa.py` | +1 / -1 | the refusal hint names `remedy teacher narrate` |
| `tests/cli/test_cli_ux.py` | +1 / -1 | the visible-group list reads `teacher` |
| `tests/cli/test_teach_cmd.py` → `test_teacher_cmd.py` | +44 / -44 | moved; imports, `TestTeacher*` classes, ids and the operator quotation re-spelled with its date kept |
| `tests/orchestration/import_reachability_allowlist.txt` | +1 / -1 | `apps.cli.commands.teacher_cmd` |
| `tests/orchestration/test_import_reachability.py` | +1 / -1 | the entry-point list names `teacher_cmd` |
| `tests/orchestration/test_teacher_model.py` | +1 / -1 | the hint assertion reads the new word |
| `tests/orchestration/test_teacher_qa.py` | +1 / -1 | the hint assertion reads the new word |
| `tests/test_command_catalog.py` | +2 / -0 | the two ids join `TestRenamedCommands` |

Insertions: 101, deletions 69 (git's default rename detection) — under the 500-insertion cap.

### Item status — the block's ordered bundle

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | all 29 table rows applied, every count exactly as stated |
| C3 | done | all 30 table rows applied, every count exactly as stated |
| C4 | done | this commit, then the push |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r24w/wt 6f506cea` | created, detached at C3 — for G5 only |
| `git worktree remove --force .remedy-wt/f261r24w/wt` | removed; `git worktree list` back to one row |
| `git push origin feature/f261-cli-vocabulary-v2` | see the completion message; run after this commit |

No pull request created, edited or merged. No `gh` command run. No `remedy` CLI invocation. No
runner and no `run_job` call: `git branch --list 'remedy/job-*'` reads 16 lines, unchanged.

## Verification

STOP reads, before C0a, C2 and C4: `ls .agent/STOP` → exit 2, `No such file or directory` each
time.

### G1 TRANSPORT — exit 0

    PASS authored block sha256 at C0a == delegating digest
         7ef435c5d02c99cd680106e5fc576e1a14b3383aead836eded3dc3bf8e6de9a5
    PASS last_block.md at C0b byte-identical to it
    PASS slice PLAN24      FOUND  bbe2ac62…c83a7
    PASS slice RECORD24    FOUND  6885ec14…da9649
    PASS slice DEC23       FOUND  1e08ad58…6dc6
    PASS slice P273D-FROM  FOUND  ac8aa4ad…8290
    PASS slice P273D-TO    FOUND  2c179aea…b87c
    PASS committed carrier .agent/authored/f261-r24-rerun.jsonl
         a3ece98b795f51e1e7703c0f5cc07af38c5787296d31d38606064f5c678bdbc7
    PASS committed carrier .agent/authored/f261-r24-teacher.jsonl
         f9d47405806677c0bb788285a86135ce0f3af981bd860581d76caed517242a2b

### G2 THE RECORD at C1 — exit 0

    PASS plan.md byte-identical to PLAN24, 37 lines, ^## Goal$ once, ^## Next Steps$ once
    PASS live_review.md == fc13ba87 blob + RECORD24
    PASS decisions.md   == fc13ba87 blob + DEC23
    PASS T2_F273.md == fc13ba87 blob with P273D applied; FROM base=1 C1=0; TO C1=1
    PASS ^Gate: F\d+ R\d+ —          base=132  C1=133
    PASS Gate: F261 R23 —            base=0    C1=1
    PASS distinct ^- R-\d+ — ids     base=133  C1=134, delta exactly R-0931
    PASS distinct ^Done: R-\d+ — ids base=9    C1=9
    PASS open set by distinct id     base=124  C1=125

    python3 -m pytest tests/docs/ -q   → exit 0, "310 passed in 1.05s"

### G3 THE TABLES — exit 0

HALF C2: `git diff --no-renames --name-only 27dcd9e4^ 27dcd9e4` prints exactly 15 paths: the carrier
plus the 14 the block names. `git rev-parse 27dcd9e4:<object>`, all nine equal to the reviewer's dry
run:

    apps            ff95a593890b1f47e479052ccdd11a71afbfce68   PASS
    packages        7af6331963c75cb02b15b159837e7f0186daf37c   PASS
    scripts         3e3c450e0dffcdd11abbc52b0a7b085359df38e4   PASS
    tests           9a67f6e8bfa5b11c9814506df1562e1e9bd6e109   PASS
    docs/guides     52e345b71419d519c98eba49cea68cc424c249ce   PASS
    docs/system     cc42698197076bc70d79a91b05ca633d7ebd2df8   PASS
    docs/README.md  c282d425ef909cf9257605294f23aba7d9457fac   PASS
    README.md       142c3f25897ec869c73753beb4e37b21c772f642   PASS
    .claude         e3cd5e0ac262f3f993506e95825e270e39c03ec0   PASS

    python3 -B -m pytest -q tests/cli/test_golden_path.py  (primary checkout, at C2)
      → exit 0, "42 passed in 19.81s"

HALF C3: `git diff --no-renames --name-only 6f506cea^ 6f506cea` prints exactly 16 paths: the carrier
plus the 15 the block names. `git rev-parse 6f506cea:<object>`, all nine equal:

    apps            57cdc70d5ddc3b059e3cb6023b538057fa9df9e2   PASS
    packages        ec2c3efd7541c8cc7d30b2b226b109e1b285da45   PASS
    scripts         3e3c450e0dffcdd11abbc52b0a7b085359df38e4   PASS
    tests           c4a66e215510d3e625f77e4e591a99996ff37e5e   PASS
    docs/guides     52e345b71419d519c98eba49cea68cc424c249ce   PASS
    docs/system     cc42698197076bc70d79a91b05ca633d7ebd2df8   PASS
    docs/README.md  c282d425ef909cf9257605294f23aba7d9457fac   PASS
    README.md       9cef3616d99c9689b6b100ea7792e9d8c2b7e57d   PASS
    .claude         e3cd5e0ac262f3f993506e95825e270e39c03ec0   PASS

Insertions per constraint 5: C2 46, C3 101.

### G4 THE SWEEP — exit 0

    git ls-tree 6f506cea -- apps/cli/commands/job_rerun_cmd.py   → prints nothing
    git ls-tree 6f506cea -- apps/cli/commands/teach_cmd.py       → prints nothing
    git ls-tree 6f506cea -- tests/cli/test_teach_cmd.py          → prints nothing
    git ls-tree 6f506cea -- apps/cli/commands/teacher_cmd.py
      → 100644 blob a2e2bab2e63d3f5178ad00eefab8b586d0acdeab
    git ls-tree 6f506cea -- packages/orchestration/run_manifest.py
      → 100644 blob dc333d48d70dc0fc5150bab9028693c0302be091

Patterns read in Python from `.remedy-wt/f261-block/f261-r24-gates.json` (sha256 verified), each
passed as one argv element to `git grep -n -I -E`, every run exit 0:

    deleted  at fc13ba87  31 lines in 12 files   PASS
    deleted  at C2         2 lines in  2 files   PASS
    deleted  at C3         2 lines in  2 files   PASS
    control  at fc13ba87  67 lines in 11 files   PASS
    control  at C2        67 lines in 11 files   PASS
    control  at C3        67 lines in 11 files   PASS
    fulfill  at fc13ba87  21 lines in  7 files   PASS
    fulfill  at C2        21 lines in  7 files   PASS
    fulfill  at C3        21 lines in  7 files   PASS
    teach    at fc13ba87  77 lines in 17 files   PASS
    teach    at C2        77 lines in 17 files   PASS
    teach    at C3        10 lines in  6 files   PASS

The `deleted` lines at C3:

    tests/docs/test_docs_consistency.py:332:  "job rerun <job_id> --check-manifest", "exit 4",   (F012 history pin)
    tests/test_command_catalog.py:339:        "job.rerun",                                      (TestDeletedCommands)

The `teach` lines at C3:

    apps/cli/commands/worker_facade_cmd.py:91:        cloned repo and teach operators to ignore the one word this command
    docs/system/model-defaults-and-dead-model-check-v0.md:52:  teach operators to ignore the word. That was the live state until
    docs/system/vocabulary.md:146:stats, teach, memory, ui, config (with the `settings` alias of amend0831 D-D), doctor,
    docs/system/vocabulary.md:191:(1) The group written `teach` above is named `teacher` — a noun like `worker` and
    docs/system/vocabulary.md:192:`doctor`; `teach` was the only verb among the visible groups. Its commands are
    docs/system/vocabulary.md:195:feature file that says `teach` as the group name reads `teacher`. (2) The visible
    packages/orchestration/dead_model_list.py:164:    extends the documented console-error base list: an operator can teach
    packages/orchestration/product_smoke.py:229:    Config extends; it never replaces. A project can teach the smoke about its
    tests/test_command_catalog.py:278:        ("teach.ask", "teacher.ask"),
    tests/test_command_catalog.py:279:        ("teach.narrate", "teacher.narrate"),

`python3 -m ruff check` over the 19 `.py` paths C2 or C3 edits that still exist at C3 → exit 0,
`All checks passed!`.

### G5 THE RED-PROOF — exit 0 (every row as ordered)

In `git worktree add --detach .remedy-wt/f261r24w/wt 6f506cea`, each run through a runner that
changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, disables bytecode
writing, and asserts `apps.cli.grouped` loaded from
`.remedy-wt/f261r24w/wt/apps/cli/grouped.py`. Mutation carrier sha256
`c611f931d1a411ac3412d6879191823d96e3a6506954c7ebe3994a0996adfa2b`, verified; READ in place, never
committed and never copied into `.agent/`.

| Run | FROM count | exit | summary | failed nodes | row's node among them |
|---|---|---|---|---|---|
| CONTROL | — | 0 | `480 passed in 3.55s` | 0 | — |
| catalog_entry_job_rerun | 1 | 1 | `1 failed, 479 passed in 3.55s` | 1 | yes |
| dispatch_entry_job_rerun | 1 | 1 | `1 failed, 479 passed in 3.59s` | 1 | yes |
| doc_invocation_job_rerun | 1 | 1 | `1 failed, 479 passed in 3.51s` | 1 | yes |
| allowlist_line_job_rerun_cmd | 1 | 1 | `1 failed, 479 passed in 3.52s` | 1 | yes |
| R1-dispatch-key | 1 | 1 | `3 failed, 477 passed in 3.52s` | 3 | yes |
| R2-catalog-id | 1 | 1 | `6 failed, 474 passed in 3.50s` | 6 | yes |
| R3-group-word | 1 | 1 | `4 failed, 476 passed in 3.52s` | 4 | yes |
| R4-hint | 1 | 1 | `5 failed, 475 passed in 3.54s` | 5 | yes |

The further nodes of the four rename rows pin the same ids or the same hint (catalog integrity,
`TestRenamedCommands`, `TestTeacherCatalogDeclaration`, the advertised-commands guard and the
refusal-hint tests), expected per G5. Each file was restored with
`git -C .remedy-wt/f261r24w/wt checkout -- <path>` after its run (exit 0) and the worktree read
`git status --porcelain` empty each time. After `git worktree remove --force` (exit 0):
`git worktree list` one row, `git branch --list 'remedy/job-*'` 16 lines.

### G6 THE SUITE, SPEC S at C3 — exit 0

    python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs
    (primary checkout root; PYTHONPATH, REMEDY_PROJECT and REMEDY_DATA_DIR removed in-process;
     PYTHONDONTWRITEBYTECODE=1; transcript under .remedy-wt/f261r24w/)

    RETURN CODE: 0
    LAST OUTPUT LINE: 17642 passed, 23 skipped, 1 warning in 1268.90s (0:21:08)
    DISTINCT BAD NODES: 0

No line-initial `FAILED ` or `ERROR ` in the transcript, so no node needed a lone re-run.

## Authored-text proofs

PLAN24, RECORD24, DEC23, P273D-FROM and P273D-TO were extracted as the bytes strictly between their
`BEGIN` and `END` lines and matched their BEGIN-marker sha256 before use; none was edited. The
applied results were re-read from the git objects at C1 and compared to base blob plus slice (G2).
The edit tables `.agent/authored/f261-r24-rerun.jsonl` and `.agent/authored/f261-r24-teacher.jsonl`
are byte-identical to their `.remedy-wt/f261-block/` originals; their 29 and 30 rows applied in file
order, each count read exactly as stated.

## Deviations & assumptions

None to the ordered commit sequence: C0a, C0b, C1, C2, C3 and C4 landed in that order, each
single-parent, on `fc13ba87`; no gate was skipped, weakened or re-valued. Declared: the G5 runs
passed `-q -p no:cacheprovider -p no:randomly` beside the ordered `-rf --tb=no`, for a parseable
summary line and no cache directory in the worktree, and the G5 runner also removed
`REMEDY_PROJECT` and `REMEDY_DATA_DIR`, as SPEC S does.

## Next

1. Phase 1 rule 1 — re-read `.agent/STOP` from disk before anything else.
2. The reviewer's verdict on round 24.
3. The `settings` alias surface over `config`.

Open findings: 125 by distinct id, with the High ids R-0803, R-0804 and R-0807.

Operator questions open: 0
