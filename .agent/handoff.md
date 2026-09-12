# Handback — F275 round 84

## Session

`SESSION 29 of feature F275 · round 84 · rounds so far 84`

NO SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED, by amendment amend0911-f275-to-scope.

Context self-assessment: this worker ran one scoped suite, one canary, one extra handler-test sweep
and one red-proof pass of four mutations, and has ample context left; nothing about the session
boundary is forced by this round.

## Range

Review of `dd92a035`..`HEAD` (the ten commits C0a–C8 plus this handback commit C9).

## Commits

### 570946de F275 R84 C0a: save the round 84 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r84.md` | +293 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r84_block.md` at 26831 bytes |

### ee498710 F275 R84 C0b: mirror the round 84 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +222 / -244 | written from the COMMITTED C0a blob read back with `git show` |

### 3c8f4fee F275 R84 C1: make the plan current for round 84

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12 / -13 | slice PLAN84, a full replacement, byte for byte; the FIRST SUBSTANTIVE COMMIT |

### cfba1a13 F275 R84 C2: book the round 83 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +8 / -0 | slice RECORD84 appended |

### 8e1f0b38 F275 R84 C3: append the round 83 and round 84 prose slips

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +6 / -0 | slice SLIPS84 appended |

### 11580cc2 F275 R84 C4: give the job-id resolver a raising form

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/data_paths.py` | +70 / -16 | SPEC L: `JobIdError(ValueError)` and its three subclasses, `lookup_job_id`, `resolve_job_id` rewritten as its exiting wrapper, the `Public API::` table gains a row; plus `_exit_ambiguous` annotated `NoReturn` (deviation 1). The worker's own code |

### e8548dad F275 R84 C5: route the 27 handler job-id parses that keep their value

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/brain.py` | +12 / -13 | SPEC R: 11 statements routed; `lookup_job_id` joined to the existing module-level `data_paths` import; `from uuid import UUID` removed |
| `apps/cli/commands/context.py` | +2 / -1 | 1 routed; module-level import added; `UUID` still used at line 38, kept |
| `apps/cli/commands/dashboard_cmd.py` | +3 / -1 | 1 routed; module-level import added; `UUID` still used, kept |
| `apps/cli/commands/event.py` | +3 / -2 | 1 routed; module-level import added; `UUID` import removed |
| `apps/cli/commands/file.py` | +2 / -3 | 1 routed; joined to the existing module-level import; `UUID` import removed |
| `apps/cli/commands/guide.py` | +2 / -3 | 1 routed; joined to the existing module-level import; `UUID` import removed |
| `apps/cli/commands/memory.py` | +3 / -3 | 1 routed; module-level import added; the function-local `UUID` import in `_cmd_memory_learn` removed with its blank line (deviation 3); the three other local `UUID` imports serve the unrouted `load_job(UUID(...))` sites and are kept |
| `apps/cli/commands/policy.py` | +3 / -3 | 2 routed; module-level import added; `UUID` import removed |
| `apps/cli/commands/propose_cmd.py` | +5 / -4 | 2 routed; module-level import added; `UUID` import removed; `_make_writer`'s docstring corrected (deviation 2) |
| `apps/cli/commands/readiness.py` | +2 / -1 | 1 routed; module-level import added; `UUID` still used for project ids, kept |
| `apps/cli/commands/repo.py` | +3 / -1 | 1 routed; module-level import added; `UUID` still used, kept |
| `apps/cli/commands/snapshot_cmds.py` | +4 / -4 | 2 routed; module-level import added; two function-local `UUID` imports removed |
| `apps/cli/commands/test_cmds.py` | +4 / -4 | 2 routed; module-level import added; module-level and one function-local `UUID` import removed |

### e35e41ed F275 R84 C6: pin the raising lookup and one routed handler with five tests

| Path | +/- | Reason |
|---|---|---|
| `tests/test_data_paths.py` | +77 / -0 | SPEC T: `TestLookupJobId` (four tests) and `TestRoutedHandler` (one); no existing test edited or deleted |

### 822a5824 F275 R84 C7: correct the teach comment the resolver collapse falsified

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/teach_cmd.py` | +6 / -5 | SPEC C: the comment now says "Until F275 T003 collapsed the two resolvers"; `ast.dump` of the file before and after is IDENTICAL, so no executable line changed |

### 6edfed53 F275 R84 C8: record DECISION F275 D58

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +16 / -0 | slice DEC84 APPENDED; deletion column ZERO |

### C9 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS, BY CONSTRUCTION | constraint 10: no gate is ordered after C9, and a handback cannot carry a reading taken after the commit that writes it; the REVIEWER measures this commit at the next gate |

THE `+/-` CELLS ABOVE WERE READ FROM `git show --numstat` AND COMPARED CELL BY CELL AGAINST G8:
C0a 293/0 = 293/0; C0b 222/244 = 222/244; C1 12/13 = 12/13; C2 8/0 = 8/0; C3 6/0 = 6/0;
C4 70/16 = 70/16; C5 48/43 (the sum of its 13 rows) = 48/43; C6 77/0 = 77/0; C7 6/5 = 6/5;
C8 16/0 = 16/0. Ten of ten pairs EQUAL, zero differ. Every commit staged exactly ONE path except C5,
which staged the 13 SPEC R files; the largest insertion count is C0a at 293.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r84/wt 822a5824` (G6) | exit 0 |
| `git worktree remove .remedy-wt/r84/wt` then `git worktree prune -v` | exit 0 and exit 0, WITHOUT `--force`, before C8; the directory is gone and `git worktree list` shows the primary checkout alone |
| `git archive dd92a035` extracted by `tarfile` into `.remedy-wt/r84/tree_base` | the G5(c) base tree; a plain directory, never registered, the primary checkout untouched |
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C9; result in the round report |
| `gh` / `remedy` | NOT RUN. No pull request, no branch created or deleted, no merge, no force-push, no history rewrite |

## Verification

Each gate ran through `.remedy-wt/r84/run.py`, which saves the output to `.remedy-wt/r84/<gate>.out`
and appends `PROCESS_EXIT=` from the subprocess's own return code.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | C8 | 0 | `cmp` of the block as received against the COMMITTED C0a blob exit **0**, empty output, both 26831 bytes, sha256 `23fcc4fa…6f77a8`; `.agent/last_block.md` at C0b equals the C0a blob; slices FOUND **4** — PLAN84 2631 bytes / 44 lines, RECORD84 3085 / 8, SLIPS84 2014 / 6, DEC84 4292 / 16 — each MATCHING the sha256 on its BEGIN marker; TOTAL **293**, slice lines 74, PROSE **219**, as constraint 9 states; no line is a run of one repeated character; the 5 STEP/SLICE header lines carry only two-character rules |
| G2 the plan | C8 | 0 | `.agent/plan.md` at C1 byte-identical to PLAN84 from the committed C0a blob, 2631 bytes, sha256 `9c75e9a8a0967b1fd40010d46ca272a2abc4685c97094d1c16084641b5255315`; **44** lines; one `## Goal`, one `## Next Steps` |
| G3 the record | C8 | 0 | READER A: 1104567 + 3085 = 1107652 (live_review at C2) and 1253148 + 4292 = 1257440 (decisions at C8), both pre-commit lengths MATCHING the block; READER B holds at N counted from the slice as **4** and **8**; negative controls `G`→`g` (file offset 1104568) and `D`→`d` (file offset 1253152), each in the FIRST appended paragraph, and a letter flipped inside each slice, all REJECTED by BOTH readers; deletion columns **0** (C2), **0** (C3), **0** (C8); prose_slips at C3 = 292291-byte pre-commit blob + SLIPS84 exactly (294305); header pattern `^Gate: F\d+ R\d+ — ` matches **105 of 105** `Gate:` paragraph heads of the pre-commit ledger (540 paragraphs); RECORD84's header matches it and byte-duplicates **0** heads, and no earlier head carries `Gate: F275 R83 — ` |
| G4 the production change | C7 | 0 | by `ast` at `822a5824`: `JobIdError`, `JobIdInvalid`, `JobIdNotFound`, `JobIdAmbiguous` each defined **1**x, bases `ValueError`, `JobIdError`, `JobIdError`, `JobIdError`; `FunctionDef` `lookup_job_id` **1**, `resolve_job_id` **1**; whole-line counts of SPEC L's three quoted lines **1**, **1**, **1**; `resolve_any_job_id is resolve_job_id` True. Across `apps/cli/`: `X = UUID(<job…>)` statements **27** at `dd92a035`, **0** at C7; `load_job(UUID(<job…>))` calls **10** at both. `git diff --numstat dd92a035` over production paths: data_paths 70/16, brain 12/13, context 2/1, dashboard_cmd 3/1, event 3/2, file 2/3, guide 2/3, memory 3/3, policy 3/3, propose_cmd 5/4, readiness 2/1, repo 3/1, snapshot_cmds 4/4, teach_cmd 6/5, test_cmds 4/4 |
| G5 the behaviour | C7 | 0 / 0 / 0 | (a) the five SPEC T node ids each **PASSED**, pytest exit 0. (b) the scoped suite in the PRIMARY checkout, exit **0**: **13260 passed, 10 skipped, 0 failed**, 1 warning, 982.76s; failure set EMPTY. Against the reviewer's 13255 at `dd92a035` the difference is **+5**, the five tests C6 adds (C6's deletion column is 0); skipped unchanged at 10. (c) `ruff check . --output-format json`: base `dd92a035` from the `git archive` scratch copy exit 1 at **26** rows, C7 in the primary checkout exit 1 at **26** rows; multiset by (code, path) ADDED `[]`, REMOVED `[]` |
| G6 mutation red-proofs | C7 | 0 | worktree `__file__` of `data_paths` and `guide` both under `/home/decodeux/Repos/remedy/.remedy-wt/r84/wt/`, printed before EVERY run; pytest `rootdir` the worktree each time; `__pycache__` purged before each run (0 found each time, the runs use `-B`). Six colours in the order not_found, invalid, ambiguous, exit_codes_and_messages, routed_handler, evaluate_missing_job. CONTROL exit 0: PASS PASS PASS PASS PASS PASS. M1 (target count 1) exit 1: FAIL PASS PASS PASS PASS FAIL. M2 (target count 1) exit 1: FAIL PASS PASS FAIL PASS PASS. M3 (target count 1) exit 1: PASS PASS PASS FAIL PASS PASS. M4 (both target counts 1) exit 1: PASS PASS PASS PASS FAIL PASS. All four required colour sets MET; each restore verified by an empty `git diff` in the worktree; worktree removed and pruned |
| G7 tree, canary, lint, path set, open set | C8 | 0 | `git status --porcelain` `''`; `git worktree list` **1** row; CANARY exit **0**, **42 passed**; `ruff check .` exit **1** by design, **26** `-->` rows against ruff's own `Found 26 errors.`; changed paths `dd92a035`..C8 **22** against the Bundle minus handoff **22**, MISSING `[]`, EXTRA `[]`; open set **87** at `dd92a035` (110 registered − 23 Done, by distinct id) and **87** at C8, membership difference empty both ways, `R-0809` and `R-0880` OPEN at both; registered, resolved and de-registered all EMPTY |
| G8 insertion cap | C8 | 0 | C0a 293/0 1 path, C0b 222/244 1, C1 12/13 1, C2 8/0 1, C3 6/0 1, C4 70/16 1, C5 48/43 13, C6 77/0 1, C7 6/5 1, C8 16/0 1; commits reaching 500 insertions **0** |

THE FAILURE REASONS UNDER EACH MUTATION were read, not only the colours: M1 fails the not-found test
on `JobIdNotFound` escaping `pytest.raises(ValueError)` and `test_evaluate_missing_job` on
`JobIdInvalid: invalid job ID: 'cli-test-job'` escaping `_require_job`'s guard; M2 fails on
`SystemExit: 1` and on an empty stderr; M3 on `Error: job id problem: invalid job ID: 'not-a-hex'`;
M4 on `Error: invalid job ID: 'ae99eb94'`.

STOP READINGS, per constraint 3: before C0a and before C9, `.agent/STOP` ABSENT at both — `test -e`
exit 1, `ls -la` exit 2, `os.path.exists` False — transcripts `.remedy-wt/r84/stop_before_C0a.txt`
and `.remedy-wt/r84/stop_before_C9.txt`.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r84.md` | `cmp` exit 0 against `.remedy-wt/r84_block.md`, 26831 bytes, sha256 `23fcc4fa4aac781f896ebf218a8e2bce3777e66053906db05702a4e6435f77a8` |
| PLAN84 | `.agent/plan.md` | byte-identical, 2631 bytes, sha256 `9c75e9a8a0967b1fd40010d46ca272a2abc4685c97094d1c16084641b5255315` |
| RECORD84 | `.agent/live_review.md` | exact suffix under readers A and B, 3085 bytes, sha256 `8f11cc4e47dd36c10f15b49efd86b8884135a5bbb9edc0f5d3283014d5f93198` |
| SLIPS84 | `.agent/prose_slips.md` | exact suffix, 2014 bytes, sha256 `d46d6c15713c90650c2997896c794f3bce1b65e01e0bdf745ebe4f8532127863` |
| DEC84 | `.agent/decisions.md` | exact suffix under readers A and B, 4292 bytes, sha256 `b9e875fe09c2686f550aa50c7b92617ad0c6c59882e75f7489f2bdb191cddb25` |

Every slice was applied by bytes from the COMMITTED C0a blob; NO SLICE WAS EDITED. C4 to C7 are the
worker's own code, written from SPEC L, SPEC R, SPEC T and SPEC C; no candidate was looked for.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block | done | |
| C0b last-block mirror | done | from the committed C0a blob |
| C1 plan | done | first substantive commit |
| C2 ledger | done | |
| C3 prose slips | done | |
| C4 the raising lookup | deviated | SPEC L met; `_exit_ambiguous` also annotated `NoReturn` (deviation 1) |
| C5 the routing | deviated | SPEC R met at 27 in 13 files; one docstring corrected and one blank line removed beyond the ruff fix (deviations 2 and 3) |
| C6 the five tests | done | |
| C7 the comment | done | |
| C8 DECISION F275 D58 | done | deletion column zero |
| C9 handback | done | this commit |
| G1 · G2 · G3 | done | exit 0 · 0 · 0, at C8 |
| G4 · G5 · G6 | done | exit 0 · 0 · 0, at C7 |
| G7 · G8 | done | exit 0 · 0, at C8 |

## Deviations & assumptions

1. **`_exit_ambiguous` IS NOW ANNOTATED `-> NoReturn`, WITH `from typing import NoReturn`.** SPEC L
   does not name it. `resolve_job_id`'s body is now a `try` whose `except JobIdAmbiguous` branch ends
   in `_exit_ambiguous(...)`; annotated `-> None`, mypy reads that branch as falling off the end of
   a function returning `str`. Measured: mypy over the committed file exits 0; the same file with
   the annotation put back to `-> None` exits 1 with one error on `def resolve_job_id(raw: str) -> str:`
   (`.remedy-wt/r84/probe_extra.out`). Its body and output are unchanged. A parity probe ran the base
   and the new `resolve_job_id` on seven inputs: invalid, not found, ambiguous, a classic prefix, a
   ping-pong prefix, a full UUID and `x`. Exit code, stdout and stderr were IDENTICAL for all seven
   (`.remedy-wt/r84/probe_resolve.py`).

2. **ONE DOCSTRING IN A ROUTED FILE WAS CORRECTED.** `_make_writer` in `propose_cmd.py` said "Returns
   None if job_id is not a valid UUID". After routing, a short prefix that resolves returns a writer,
   so it now says "Returns None if job_id does not resolve to one job". SPEC R does not name it. It
   is in a file C5 stages, and it is the kind of falsified claim round 83's slip is about.

3. **ONE BLANK LINE REMOVED BY HAND AFTER THE RUFF FIX.** In `memory.py`, removing the function-local
   `from uuid import UUID` from `_cmd_memory_learn` left its body starting with an empty line. I
   removed that line. `ruff check` over the file is clean after the edit, and G5(c)'s multiset is
   unchanged.

4. **HOW C5 WAS MADE.** `.remedy-wt/r84/route.py` replaced each call's `UUID` name at its `ast` byte
   offsets. It added `from packages.orchestration.data_paths import lookup_job_id` after the last
   top-level import wherever the module's TOP-LEVEL statements did not bind `lookup_job_id`, which
   was all 13 files. Then `python3 -m ruff check --select I001,F401 --fix` ran over exactly those 13
   files and fixed 24 findings: the import merges and sorting, and the `UUID` imports left unused.
   Before the transform, the same selection over those files reported none.

5. **G3's HEADER PATTERN WAS PROPOSED, THEN CHECKED AGAINST THE FILE.** I did not infer it
   mechanically. `^Gate: F\d+ R\d+ — ` was matched against every paragraph of the pre-commit ledger
   that starts with `Gate:`. It matched 105 of 105.

6. **MEASURED, NOT PREDICTED BY THE BLOCK: A ROUTED HANDLER STILL SAYS "invalid job ID" FOR A
   WELL-FORMED PREFIX.** The handlers' own `except ValueError` branches print their fixed message, so
   `_cmd_guide_job` over a data root holding two `aaaa1111-…` records exits 1 with
   `Error: invalid job ID: 'deadbeef'` for an unmatched prefix and `Error: invalid job ID: 'aaaa1111'`
   for an ambiguous one (`.remedy-wt/r84/probe_extra.out`). That is the message-shape class DEC84
   leaves under `R-0809`. No id was spent.

7. **MEASURED, NOT PREDICTED BY THE BLOCK: TWO MORE `load_job(UUID(...))` PARSES SIT OUTSIDE BOTH
   COUNTS.** `apps/cli/commands/dashboard_cmd.py:63` and `apps/cli/commands/readiness.py:88` call
   `load_job(UUID(jid))`. Their argument's source is `jid`, which does not contain "job", so the
   27 and the 10 both leave them out by construction. Whether `jid` is a job id is for the round that
   reads the ten.

8. **AN EXTRA CHECK OUTSIDE THE SCOPED SUITE.** Fifteen test files outside `tests/cli/` and
   `tests/orchestration/` reference the routed handlers, among them `tests/test_timeline.py`, whose
   run-log seam sweep inspects `UUID(...)` arguments. I ran all fifteen in the primary checkout at
   C8: exit 0, **1442 passed, 3 skipped** (`.remedy-wt/r84/extra_suites.out`). No gate orders this
   run.

9. **MY OWN G1–G3 SCRIPT FAILED ITS FIRST RUN** with a `SyntaxError`: a backslash inside an
   f-string expression, which this Python does not allow. I moved the expression out of the
   f-string and re-ran the whole script. The reported transcript is from the re-run.

10. **NO OTHER DEVIATION.** The commit sequence is exactly the Bundle, and C1 is the first
    substantive commit. Nothing under `docs/` or `scripts/` was touched. `job_stop_cmd.py`,
    `project.py` and `review_cmd.py` were not touched, and no landed DECISION was rewritten. No `.py`
    file was created under `.agent/`: every script lives under `.remedy-wt/r84/`, uncommitted.

## Next

The reviewer re-runs the gates and the red-proofs and issues the round 84 verdict.

Operator questions open: 0.

After that comes THE REMAINING HANDLER PARSES. Each of the ten `load_job(UUID(...))` sites is read
for whether its caller keeps using the raw argument as a key, starting with `job stop`'s loader.
Deviation 7's two `UUID(jid)` sites belong in that reading. Then THE FLIP, under DECISION F275 D48
and D56.
