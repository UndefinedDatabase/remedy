# Handoff — F036, round 3 (book round 2, record DECISION F036 D4, land T002's second half:
`tour.json` versioned at every reported terminal, `job show --full`'s `tour` section and
`job show --tour`, and the fixture goldens)

## Session

SESSION 1 of feature F036 · round 3 · rounds so far 3. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md, the block, `DECISION F036 D4`
in the booking diff, and every required source file in full (`result_tour.py` as round 2 left it,
`_apply_terminal`/`REPORTED_TERMINALS`/`TERMINAL_MAX_CYCLES_REACHED` in `long_run_executor.py`,
`write_final_report`/`REPORT_ERROR_METADATA_KEY` in `run_report.py`, `durable_write_json` in
`secure_fs.py`, `_cmd_show_job`/`_SHOW_SECTION_ORDER`/`ShowSectionError`/`_SHOW_SECTIONS`/
`_build_show_sections`/the `job.show` dispatch entry in `apps/cli/commands/job.py`, the `job.show`
catalog entry, `tests/cli/test_job_show.py`, `tests/orchestration/test_run_report_hook.py`,
`ALLOWED_UNWIRED` in `tests/test_no_orphan_modules.py`, the head of
`import_reachability_allowlist.txt`, and `_meaning_violations` in `tests/docs/test_vocabulary.py`);
wrote the S1–S7 storage/hook/CLI code, its tests, three fixture goldens and the mutation tool from
the specification; ran a smoke script confirming the hook and CLI end-to-end (with `tour_call_fn`
stubbed to avoid a live model call after one accidental unstubbed run); ran the payload-
verification, G1/G2 byte-equality and hash checks, ruff, the G4 pytest selection (base-line
collect-only counts at `42543dd9` and at C4, then the full 37-target serial run), `integrity
check`, and the G5 mutation tool twice (a preliminary dry run in a throwaway worktree, then the
official run at C5).

## Range

Review of `42543dd9..HEAD` (`HEAD` is this handback's own commit, `F036 R3 C6`, on
`feature/f036-guided-result-tour`).

## Commits

### 41276dc63 F036 R3 C1: copy round 3 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r3-block.md | 299/0 | copy of the block, verified line count and sha256 |
| .agent/authored/f036-r3-booking.diff | 65/0 | copy of the reviewer's booking.diff payload |
| .agent/authored/f036-r3-plan.md | 28/0 | copy of the reviewer's plan.md payload |

### 1d40b8521 F036 R3 C2: book round 2, record DECISION F036 D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 47/0 | DECISION F036 D4 appended by booking.diff |
| .agent/live_review.md | 2/0 | round 2's `Gate: F036 R2 —` entry appended by booking.diff |
| .agent/plan.md | 7/8 | rewritten to the reviewer's plan.md payload |

### 10a39a850 F036 R3 C3: store the tour at every reported terminal and show it on the command line
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 6/1 | `--full`'s closing words gain "and guided tour"; new `--tour` `ArgDef` after it (S5) |
| apps/cli/commands/job.py | 46/2 | `_tour_section`, `"tour"` appended to `_SHOW_SECTION_ORDER`/`_SHOW_SECTIONS`, `_build_show_sections(job, names=...)`, `_cmd_show_job(..., tour=...)`, dispatch entry (S5) |
| packages/orchestration/long_run_executor.py | 6/0 | `_apply_terminal` calls `write_result_tour(job)` directly after `write_final_report(job)`, inside the same condition (S4) |
| packages/orchestration/result_tour.py | 148/4 | S1 storage (`TOUR_ERROR_METADATA_KEY`, `tour_path`, `stored_tour_versions`, `load_result_tour`), S2 writer (`write_result_tour`), S3 renderer (`render_tour_lines`); module docstring corrected (no longer says "writes no file"/"nothing calls it yet") |
| tests/cli/test_job_show.py | 2/1 | the two `_SHOW_SECTION_ORDER`/`_SHOW_SECTIONS` pins gain `"tour"` after `"dod"` (S6) |
| tests/orchestration/import_reachability_allowlist.txt | 1/0 | `packages.orchestration.result_tour` added after `repository_snapshot` (S6) |
| tests/test_no_orphan_modules.py | 0/3 | `result_tour.py`'s `ALLOWED_UNWIRED` entry removed (S6) |

### df16a94fa F036 R3 C4: test the tour's storage, hook and command line, and pin three goldens
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_show.py | 47/0 | import + `TestTourSection`: `--tour` alone, nothing stored, an unreadable stored tour |
| tests/orchestration/fixtures/result_tour/golden_generated.json | 45/0 | the generated golden (S7), written once from the code, job id replaced by `<job>` |
| tests/orchestration/fixtures/result_tour/golden_green_mechanical.json | 48/0 | the green mechanical golden (S7) |
| tests/orchestration/fixtures/result_tour/golden_held_mechanical.json | 32/0 | the held mechanical golden (S7) |
| tests/orchestration/fixtures/result_tour/model_answer.json | 29/0 | the recorded model answer (S7): 5 stops, 2 sound + 3 claim-violating, none anchored to a task |
| tests/orchestration/test_result_tour.py | 271/0 | versions, the writer, the call-fn spy, the renderer, the `_apply_terminal` hook (S4), the 3 golden tests |

### 33e4b180f F036 R3 C5: add the round 3 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r3-mutations.py | 186/0 | the G5 red-proof tool: 10 mutations (m1–m10 of the block) across 3 files, all caught |

### <this commit> F036 R3 C6: rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f036-r3-mut-dry HEAD` — a preliminary, non-official dry
  run of the mutation tool before C5 existed, to validate the tool's own correctness. Outcome:
  worktree created at `df16a94fa` (C4's tip); tool run passed all 10 mutations first try; removed
  with `git worktree remove --force` (exit 0) immediately after, `git worktree prune`, restoring
  `git worktree list | wc -l` to 62.
- `git worktree add --detach .remedy-wt/f036-r3-mut 33e4b180f` — the official G5 worktree, cut
  from C5 per the block. Outcome: worktree created at detached HEAD `33e4b180f`.
- `git worktree remove --force .remedy-wt/f036-r3-mut` then `git worktree prune` — the official
  G5 worktree's own cleanup (constraint 6). Outcome: removed; `git worktree list | wc -l` read 62,
  matching the round's step-4 reading.
- `git push -u origin feature/f036-guided-result-tour` — run immediately after this commit per
  the bundle order. Its real outcome is reported in the round's reply (G6), not here, because
  this file is written before the push happens.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push,
  no `git stash` — none of these were run, per constraint 5.

## Verification

**G1 TRANSPORT** — PAYLOADS table readings (before use), all MATCH:
```
booking.diff: 65 lines, 11302 bytes, sha256 ebff11af…9fe43ba5f11be9
plan.md:      28 lines,   941 bytes, sha256 820cd94b…081f35f760f9cf78
```
Block self-check: 299 lines, sha256 `a88208af…730a32fd237b3394` — MATCH on both readings given in
the delegation message. `.agent/authored/f036-r3-*` copies vs. sources, read back via
`git show 41276dc63:<path>`, all byte-identical (verified by direct byte comparison, not sha256
alone):
```
f036-r3-block.md     vs .remedy-wt/f036-r3/block.md              True, 23402 bytes, sha256 a88208af…37b3394
f036-r3-booking.diff vs .remedy-wt/f036-r3-payloads/booking.diff True, 11302 bytes, sha256 ebff11af…43ba5f11be9
f036-r3-plan.md       vs .remedy-wt/f036-r3-payloads/plan.md      True,   941 bytes, sha256 820cd94b…5f760f9cf78
```

**G2 THE BOOKING** — every file's bytes and sha256 at C2 (`git show 1d40b8521:<path>`) MATCHED
the reviewer's table exactly:
```
.agent/decisions.md   2361115 bytes  sha256 29737d50…09baf31ae160a58  MATCH
.agent/live_review.md  316115 bytes  sha256 ca43e961…12095d214ac7d9b5d MATCH
.agent/plan.md            941 bytes  sha256 820cd94b…081f35f760f9cf78 MATCH
```
`open_finding_ids` over `.agent/live_review.md` TEXT at C2 read `[]`. The ledger's last non-empty
line at C2 begins `Gate: F036 R2 — ` (confirmed verbatim). `git diff --name-only 41276dc63
1d40b8521` named exactly the 3 paths of the G2 table, no more, no fewer.

**G3 THE CODE** — `python3 -m ruff check packages/orchestration/result_tour.py
packages/orchestration/long_run_executor.py apps/cli/commands/job.py apps/cli/command_catalog.py
tests/test_no_orphan_modules.py tests/cli/test_job_show.py tests/orchestration/test_result_tour.py`
at C4: `All checks passed!`, REAL_EXIT=0. `stored_tour_versions`, `write_result_tour` and
`_tour_section` were quoted whole from `git show 10a39a850`, and the changed lines of
`_apply_terminal`, `_cmd_show_job` and the catalog entry were shown as diff hunks — see the
round's reply for the full text; behaviour matches S1–S5 exactly.

**G4 THE TESTS** — baseline `--collect-only -q` node counts, measured by temporarily swapping in
the `42543dd9` versions of both files and restoring via `git checkout --` afterward (working tree
verified clean before and after): `tests/orchestration/test_result_tour.py` 24 nodes,
`tests/cli/test_job_show.py` 19 nodes (43 total) at `42543dd9`; 44 and 22 (66 total) at C4 — 23
new nodes (20 + 3). The full 37-target serial selection:
```
2157 passed, 4 skipped, 1 warning in 207.56s (0:03:27)
REAL_EXIT=0
```
2134 (block's baseline) + 23 (new nodes) = 2157 — no discrepancy. SKIPPED lines (all 4, identical
to the block's baseline):
```
SKIPPED [3] tests/orchestration/test_model_routing.py:455: covered by the violating fixture above
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 ...
```
The run's single reported warning, re-run with `-W default` to identify it: 16 warnings total under
that flag, all `ResourceWarning`s from pytest's own fixture teardown and from
`tests/orchestration/test_orchestrator_loop.py:294` (an unclosed file handle, pre-existing, a file
this round never touched), plus one `UserWarning` from `packages/orchestration/model_routing.py`
about a deliberately-undeclared test role — none from any file this round changed; re-running just
`tests/orchestration/test_result_tour.py tests/cli/test_job_show.py` with `-W error::DeprecationWarning`
raised nothing. `python3 -m apps.cli.main integrity check --json`: all six checks `pass`,
`fail_count` 0, `ok` true.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f036-r3-mut 33e4b180f` then
`python3 -B .agent/authored/f036-r3-mutations.py <worktree>`, whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1 every write goes to version 1, overwriting tour.json: exit=1 failed=1 nodes=['tests/orchestration/test_result_tour.py::test_two_writes_give_tour_json_then_tour_v2_json']
m2 load_result_tour answers the LOWEST stored version: exit=1 failed=1 nodes=['tests/orchestration/test_result_tour.py::test_two_writes_give_tour_json_then_tour_v2_json']
m3 write_result_tour catches no OSError: exit=1 failed=1 nodes=['tests/orchestration/test_result_tour.py::test_a_failing_write_records_tour_error_and_a_later_good_write_clears_it']
m4 a good write leaves tour_error in place: exit=1 failed=1 nodes=['tests/orchestration/test_result_tour.py::test_a_failing_write_records_tour_error_and_a_later_good_write_clears_it']
m5 load_result_tour skips the tour_problems check: exit=1 failed=1 nodes=['tests/orchestration/test_result_tour.py::test_load_result_tour_raises_for_an_unsound_tour']
m6 render_tour_lines omits each stop's anchor line: exit=1 failed=1 nodes=['tests/orchestration/test_result_tour.py::test_render_tour_lines_gives_the_exact_s3_lines_with_a_multiline_body']
m7 stored_tour_versions counts directories too: exit=1 failed=1 nodes=['tests/orchestration/test_result_tour.py::test_tour_v1_tour_vx_and_a_directory_tour_v3_are_not_versions']
m8 the hook runs outside the report's condition, for every terminal: exit=1 failed=2 nodes=['tests/orchestration/test_result_tour.py::TestApplyTerminalWritesTheTour::test_max_cycles_reached_writes_no_tour', 'tests/orchestration/test_result_tour.py::TestApplyTerminalWritesTheTour::test_write_report_false_writes_no_tour']
m9 --tour builds every section, not only tour: exit=1 failed=1 nodes=['tests/cli/test_job_show.py::TestTourSection::test_tour_alone_gives_a_sections_object_holding_only_tour']
m10 with nothing stored the section raises tour_unreadable: exit=1 failed=1 nodes=['tests/cli/test_job_show.py::TestTourSection::test_nothing_stored_reads_stored_false_and_version_zero']
control (after): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
No mutation stayed green; no extra test was needed. A preliminary, non-official dry run against a
throwaway worktree at C4's tip produced the identical result before C5 existed (see External
actions), which is why no correction round was needed between writing the tool and running it
officially. `git worktree remove --force .remedy-wt/f036-r3-mut`, `git worktree prune`,
`git worktree list | wc -l` = 62 (matches step 4).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this handback |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | every mutation caught first run (both the preliminary dry run and the official run); no extra test needed |

## Authored-text proofs

`booking.diff` applied via `git apply --check` (exit 0) then `git apply` (exit 0) — never edited,
never retyped. The two payloads (`booking.diff`, `plan.md`) were verified line count/byte
count/sha256 against the PAYLOADS table before use, and the committed `.agent/authored/f036-r3-*`
copies read back byte-identical to their sources via `git show` (G1, above). `.agent/plan.md` was
REWRITTEN to the payload file by `shutil.copyfile`, never hand-edited; its post-write sha256 equals
the payload table's own `820cd94b…` row and C2's resulting file hashes matched the reviewer's G2
table exactly for all 3 files (see Verification, G2). No reviewer-authored text was applied outside
these two payloads; the S1–S7 storage/hook/CLI code, its tests, the three fixture goldens and the
mutation tool are worker-authored against the block's specification, not transcribed from a
payload.

## Deviations & assumptions

- **`result_tour.py`'s module docstring corrected (not ordered by the block).** The docstring
  round 1 wrote said "this module is pure — it writes no file" and "Nothing calls it yet;
  F036 T002 wires it at the job terminal and removes this module's `ALLOWED_UNWIRED` entry" — both
  became false this round (`write_result_tour` writes, and `_apply_terminal` calls it). AGENTS.md's
  file-editing rules require files to "remain consistent with architecture" after an edit, so the
  docstring was updated to describe `write_result_tour` as the one function that touches disk and
  to name its caller, without changing anything about the pure generation functions' description.
  No test depends on the docstring's exact wording.
- **A self-caught test bug that wrote three stray directories into the real (non-isolated) data
  root, corrected before C4 was committed.** `test_a_failing_write_records_tour_error_and_a_later_
  good_write_clears_it` originally called `monkeypatch.undo()` to restore the patched
  `durable_write_json` after the first (failing) write. Because this test file's own autouse
  `_isolated_data_root` fixture sets `REMEDY_DATA_DIR` through the SAME `monkeypatch` fixture
  instance, `.undo()` rolled back that env-var patch too, not just the one this test applied
  itself — sending the test's second `write_result_tour` call to the real repository's `.data/`
  directory instead of the isolated temp root. This was caught by the suite's own `pytest_
  sessionfinish` R-0803 guard (`tests/conftest.py`), which failed the run with "the test run
  changed the configured data root". Fixed by restoring only the one patched attribute
  (`monkeypatch.setattr(result_tour_module, "durable_write_json", real_durable_write_json)`)
  instead of calling `.undo()`. The three orphaned evidence-only job directories the buggy version
  created (`cb1a2bca23ea44ed`, `f8427de0b4484967`, `2646bb9bed194750` under the real `.data/jobs/`,
  each holding only `evidence/tour.json`, no `job.json` — confirming no real job record was ever
  created, i.e. pure test pollution) were removed by hand before continuing, and the fixed test
  file was re-run clean (no R-0803 warning) before C4 was committed. Constraint 4 permits
  correcting a test this round itself wrote before C6; this correction and cleanup happened before
  C4, so C4 never carried the buggy version.
- No other deviation. Every mutation in G5 was caught on the first (and only) official run; no
  additional test was needed. No red gate was hit; nothing under AGENTS.md "If Blocked" applies
  this round.

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk at session
start. (2) The review of this round (F036 round 3). (3) T003 — the browser's read route for the
tour, the overlay with its spotlight and navigation to each anchor, and the demo's tour. Open-
findings count: 0. Operator-questions count: 1 (Q6).
