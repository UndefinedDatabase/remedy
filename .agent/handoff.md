# Handback — F291 round 2: book round 1, record D2, consolidate the checklist, document the two sources, write the Built State, run the closure's self-use item

## Session

SESSION 1 of feature F291 · round 2 · rounds so far 2. Context self-assessment: roughly half the
session's context window remained when this handback was written, after all seven commits and all
five gates.

## Range

Review of `045de81f5`..HEAD (this round's final commit, C6 — the push's real outcome is reported in
the worker's reply, since this file is committed as part of C6 and cannot name its own commit's sha
or anything that follows it).

## Commits

### `13145ec2e` F291 R2 C1a: copy round 2 block, plan, records and docs diffs
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-r2-block.md | +222/-0 | this round's block, copied verbatim via `shutil.copyfile` |
| .agent/authored/f291-r2-plan.md | +28/-0 | payload copy |
| .agent/authored/f291-r2-records.diff | +71/-0 | payload copy |
| .agent/authored/f291-r2-docs.diff | +96/-0 | payload copy |

Total 417 insertions (block's 222 + 195), matching the block's stated formula exactly; measured
`git diff --stat --cached` before commit: `4 files changed, 417 insertions(+)`.

### `983eafe95` F291 R2 C1b: copy round 2 code and tests diffs and the self-use script
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-r2-code.diff | +22/-0 | payload copy |
| .agent/authored/f291-r2-tests.diff | +126/-0 | payload copy |
| .agent/authored/f291-r2-selfuse.py | +122/-0 | payload copy |

Measured 270 insertions — equal to the block's expected reading exactly.

### `bfd2bd8fc` F291 R2 C2: book F291 R1, record D2, consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +35/-0 | DECISION F291 D2 appended (records.diff) |
| .agent/live_review.md | +2/-0 | Gate: F291 R1 entry appended (records.diff) |
| .agent/plan.md | +9/-10 | rewritten via `shutil.copyfile` from plan.md payload |
| docs/agents/planner_reviewer_prompt.md | +7/-0 | the checklist consolidation paragraph appended above the 34-item line (records.diff) |

Measured `git diff --numstat --cached` before commit: 35/0, 2/0, 9/10, 7/0 — equal to the block's
expected numstat table exactly, in the same order.

### `33ce3a29f` F291 R2 C3: document the two new self-use sources and write F291's Built State
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS_closure_protocol.md | +4/-2 | precondition 6 now names Tiers 4 and 5 as almost-always sources (docs.diff) |
| docs/roadmap/features/T5_F291.md | +35/-0 | `## Built State (F291, 2026-09-29)` appended (docs.diff) |
| docs/system/self-use-track-v1.md | +17/-1 | the two new sources described under "Who runs it, and on what budget" (docs.diff) |
| packages/orchestration/self_use_generator.py | +2/-2 | the clause label `S0` dropped from two comments (code.diff) |

Measured `git diff --numstat --cached` before commit: 4/2, 35/0, 17/1, 2/2 — equal to the block's
expected numstat table exactly, in the same order.

### `10352b102` F291 R2 C4: add the reviewer's test that a Tier 4 item runs to the approval gate
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_self_use_runner.py | +110/-1 | `git apply` of tests.diff: imports `TASK_APPLIED`, appends `TestAnExcusedHandlerItemRunsToTheApprovalGate` |

Measured `git diff --cached --numstat` before commit: 110/1 — equal to the block's expected numstat
exactly.

### `b5aebe4d0` F291 R2 C5: add the round 2 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f291-r2-mutations.py | +132/-0 | this round's mutation tool (G3): 3 labelled mutations (r1, r2, r3), an unmutated control run first and last, byte-identical restore after each |

Measured 132 insertions.

### `883aad85d` F291 R2 C6: generate and run the closure's self-use item, record its readings
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | +8/-0 | item `SU-037` appended by `generate_and_append_if_empty()`, `consumed_by` left empty |
| .agent/selfuse_f291/SU-037.md | +13/-0 | the generated job's markdown, copied from the run's job file |
| .agent/selfuse_f291/changed_paths.txt | +2/-0 | the two files the job's applied task touched |
| .agent/selfuse_f291/entry_and_job_file.txt | +5/-0 | the queue entry's id/title/provenance/consumed_by and its job file path |
| .agent/selfuse_f291/execution_config.txt | +39/-0 | the run's resolved execution config (provider/model per role) |
| .agent/selfuse_f291/full_transcript.txt | +14/-0 | the job/task summary |
| .agent/selfuse_f291/job_diff.txt | +27/-0 | `git diff HEAD...remedy/job-d6d60ea3d586425a` |
| .agent/selfuse_f291/result_state.txt | +12/-0 | job id/state/budgets/budget actuals/task states |
| .agent/selfuse_f291/run_defects.txt | +1/-0 | `describe_self_use_run_defects()` — NONE |
| .agent/selfuse_f291/staleness_after.txt | +2/-0 | staleness catalog read from the job branch after the run — NONE |
| .agent/selfuse_f291/timing.txt | +3/-0 | started/finished/wall seconds |

Measured `git diff --cached --numstat` before commit: 13/0, 2/0, 5/0, 39/0, 14/0, 27/0, 12/0, 1/0,
2/0, 3/0, 8/0 — 126 insertions total, well under the 500 cap. `git status --porcelain` before
staging showed exactly these two paths modified/untracked (`scripts/self_use_queue.json` modified,
`.agent/selfuse_f291/` untracked) and nothing else, so nothing outside the block's named commit
scope was committed.

### C7 (this commit) — F291 R2 C7: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this file | round 2 handback, written and committed as its own commit per the block's bundle order (C7 is the handback alone; no code or state file rides with it) |

## External actions

- `git worktree add --detach .remedy-wt/f291-r2-mut b5aebe4d0` (G3): succeeded, `HEAD is now at
  b5aebe4d0`.
- `git worktree remove --force .remedy-wt/f291-r2-mut` then `git worktree prune` (G3, last action):
  both exit 0; `git worktree list | wc -l` read 13 afterward, equal to the BEFORE-ANYTHING-ELSE step
  4 reading.
- The self-use run (C6) added and removed `.remedy-wt/f291-r2-jobtree` itself (the payload script's
  own staleness-read worktree, over branch `remedy/job-d6d60ea3d586425a`); it was gone by the time
  the run finished, confirmed by `ls` before staging C6.
- The self-use run left branch `remedy/job-d6d60ea3d586425a` behind (never applied, never merged):
  `git branch --list 'remedy/*' | wc -l` read 16 before C6 and 17 after — the one new job branch.
  Nothing was deleted that this round did not create as scratch (the worktree above), and every
  worktree and branch listed at BEFORE-ANYTHING-ELSE step 4 was left untouched.
- `git push -u origin feature/f291-self-use-sources-v2` after C7: real outcome reported in the
  worker's final reply, since this file cannot record a push that follows it.
- No PR was created (the block forbids it this round). No `gh pr merge`, no checkout of `main`, no
  branch deletion, no force-push, no `git stash`.

## Verification

**BEFORE ANYTHING ELSE:** step 1 `ls .agent/STOP` — absent (`No such file or directory`). step 2
`pwd` `/home/decodeux/Repos/remedy`; `git status --porcelain` empty; `git branch --show-current`
`feature/f291-self-use-sources-v2`; `git log --oneline -1` `045de81f5` — all matched exactly. step 3
block measured 222 newlines, 17265 bytes, sha256
`dbf9e6c5531844b1c9e125d9a6fef88d872c18b8579b29f8b8f0e3b7cf7636b8` — equal to the delegation
message's two readings exactly. step 4 `git worktree list | wc -l` 13; `git branch --list
'remedy/*'` 16.

**PAYLOADS:** all six measured exactly against the table — records.diff 71/10124/
`bcc6ea6659eda98aa5f0a313d3a3707ebe93f47acd18044c5a713bfbe8e4d1cc`, docs.diff 96/6521/
`dc06ebb7acd565c570e930856bf64ed9a5c0c49c27c58af8a0872262bd424b12`, code.diff 22/1354/
`03bdff1807268cbd524b14631ab50cfb78fa94eb58cc55da162fd85d342d3a45`, tests.diff 126/6217/
`43a85a7c78d42cfd616644a528a1dbe93b337e954e5d1380567008b400eb188f`, plan.md 28/896/
`a59330b4d49e9b584a6542f126c227f8387b3b765fc82ac0ad284ed4c3513301`, selfuse.py 122/6488/
`be69f7b61e980b8667bfc1fc44aafc32de9a0710c717ff66bbda14cef9c9d81c` — full hashes match the block's
table digit for digit.

**G1 transport:** all seven committed `.agent/authored/f291-r2-*` copies (block, plan, records diff,
docs diff, code diff, tests diff, selfuse.py) verified byte-identical to their sources with an
independent hash-comparison script (`git show <commit>:<path>` vs. source bytes) — all seven equal,
the block copy against `.remedy-wt/f291-r2/block.md` included. The nine-row G1 table (four files at
C2, four at C3, one at C4) was read via `git show <commit>:<path>` with an independent script that
computed each file's byte count and full sha256 and compared both against the block's table; every
one of the nine rows matched on both bytes and the full 64-hex sha256, exactly as the block stated
them (`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/agents/planner_reviewer_prompt.md` at C2; `docs/roadmap/STATUS_closure_protocol.md`,
`docs/roadmap/features/T5_F291.md`, `docs/system/self-use-track-v1.md`,
`packages/orchestration/self_use_generator.py` at C3; `tests/orchestration/test_self_use_runner.py`
at C4 — no row printed MISMATCH). Also over the ledger text at C2: `open_finding_ids` (imported from
`scripts/rotate_live_review.py`) read `[]`, `latest_gate_verdict` read `PASS` — both equal to the
reviewer's reading. `live_checklist_items` (imported from `packages/orchestration/block_lint.py`)
over the planner prompt at C2 read 34 items — equal to the reviewer's reading.

**C2/C3/C4 apply:** `git apply --check` then `git apply`, each exit 0, in order: records.diff,
docs.diff, code.diff, tests.diff. Every `git diff --numstat` reading matched the block's expected
table exactly before each commit (see per-commit tables above).

**G2 the tests, serially, in the primary checkout at C5:**
```
python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_findings.py tests/orchestration/test_self_use_job.py tests/orchestration/test_doc_staleness.py tests/test_ble001_ratchet.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py
```
→ `685 passed, 1 skipped in 59.39s`, `REAL_EXIT=0` — equal to the reviewer's simulated-tree reading
of `685 passed, 1 skipped` at exit 0 exactly. The `-rs` summary printed exactly one SKIPPED line:
`SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md
was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1,
docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog:
re-pin this contract on the split-workflow docs, or retire the test.` — the D12 quarantine, equal to
the reviewer's own reading. Then
```
python3 -m ruff check tests/orchestration/test_self_use_runner.py packages/orchestration/self_use_generator.py .agent/authored/f291-r2-mutations.py .agent/authored/f291-r2-selfuse.py
```
→ `All checks passed!`, exit 0. Then `python3 -m apps.cli.main integrity check --json` → all six
checks `status: "pass"` (`handler_import` handlers=171, `live_review_verdict` last Gate verdict
PASS, `plan_consistency` unchecked=0 context_complete=False, `relevant_untracked` untracked=0
relevant=0, `repo_root_hygiene` no reviewer scratch/evidence dir/archive at root, `high_blockers_open`
no open blocker/high findings), `fail_count: 0`, `ok: true`, `passed: true`, real exit 0. The full
suite was NOT run this round (constraint 8 — it runs once, in the next round).

**G3 the red proofs:** `git worktree add --detach .remedy-wt/f291-r2-mut b5aebe4d0` succeeded.
`python3 -B .agent/authored/f291-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f291-r2-mut`
printed, verbatim:
```
control (before) exit=0 failed=0
r1 (Tier 4 job markdown loses its ## Task 1 heading): exit=1 failed=1
restored byte-identical: True
r2 (generate_and_append_if_empty drops source_root): exit=1 failed=1
restored byte-identical: True
r3 (_MAX_PROVIDER_CALLS reads 1): exit=1 failed=4
restored byte-identical: True
control (after) exit=0 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All three mutations turned the suite red (non-zero exit, failed count > 0); both controls passed
clean; every restore was byte-identical to the original, checked by re-reading the mutated file's
bytes after restore and comparing to the bytes read before mutation. Each mutation's FROM text was
independently verified to occur exactly once in its target file in the primary checkout before the
tool was committed. `git worktree remove --force .remedy-wt/f291-r2-mut` and `git worktree prune`
both exit 0; `git worktree list | wc -l` read 13 afterward — equal to the BEFORE-ANYTHING-ELSE step
4 reading.

**G4 the self-use readings:** the run's whole stdout is reproduced verbatim in
`.remedy-wt/f291-r2-worker/selfuse.log`; `REAL_EXIT=0`.

- **Item:** id `SU-037`, title "Narrow the excused handler at apps/cli/commands/brain.py:132", Tier 4
  — equal to the reviewer's stated reading exactly. Provenance: `generated (self-use-generator tier
  4, excused handler, apps/cli/commands/brain.py:1:except Exception:  # noqa: BLE001 — constitution
  is optional; warn and continue without it)`.
- **Job:** id `d6d60ea3d586425a`, state `completed`, stop reason/source empty, error empty, run
  manifest error empty.
- **Provider/model** (`.agent/selfuse_f291/execution_config.txt`): builder `claude-cli` /
  `claude-sonnet-4-6` (effort `medium`, all sourced `cli`); reviewer `claude-cli` /
  `claude-sonnet-4-6` (effort `medium`, all sourced `cli`) — the `self_use` role's configured
  provider, never `fake`. `max_tasks` 1 (source `invocation`), `timeout_sec` 600 (source
  `invocation`), `repair_rounds_allowed` 2 (default), `claude_cli_write_mode`
  `allowed-tools`.
- **Budgets:** `{"deadline": null, "max_cost_usd": 6.0, "max_provider_calls": 8,
  "max_total_tokens": null, "max_wall_clock_minutes": null, "min_free_disk_bytes": null}` — the
  default budget, no override passed.
- **Budget actuals:** `{"actual_call_count": 2, "actual_sources": ["pingpong_live"],
  "measured_cost_usd": 0.6615633000000001, "priced_call_count": 2, "provider_call_count": 2,
  "schema_version": "2.0.0", "total_tokens": 4489, "unmeasured_call_count": 0,
  "unpriced_call_count": 0}` — 2 calls, inside the cap of 8; real provider calls (`pingpong_live`),
  never a stand-in.
- **Task statuses:** `T001: applied_to_job_workspace (verdict: pass; final_status:
  staged_review_passed; repair_rounds_used: 0; run_id: ac2f5b9ce6ca4e79)` — the one task reached the
  approval gate, applied to the job's own workspace only, never to the checkout.
- **`changed_paths.txt`** (verbatim): `apps/cli/commands/brain.py`, `tests/test_ble001_ratchet.py`.
- **`staleness_after.txt`** (verbatim): `Read from: the job branch remedy/job-d6d60ea3d586425a` then
  `NONE`.
- **`job_diff.txt`** (verbatim, `git diff HEAD...remedy/job-d6d60ea3d586425a`, exit 0): narrows
  `except Exception:  # noqa: BLE001 — constitution is optional; warn and continue without it` to
  `except OSError:` in `apps/cli/commands/brain.py` line 132, and lowers `MAX_EXCUSED` from `290` to
  `289` in `tests/test_ble001_ratchet.py` — exactly the task's acceptance criteria, and no other
  file touched.
- **`run_defects.txt`** (verbatim): `NONE`.
- Timing: started `2026-09-29T20:05:52.521215+00:00`, finished `2026-09-29T20:07:26.880720+00:00`,
  wall 94.4 seconds — well inside the ten-minute-per-call / most-of-an-hour envelope the block named.
- `git worktree list | wc -l` after the run: 13 (unchanged — the run's own jobtree worktree was
  added and removed by the payload script itself). `git branch --list 'remedy/*' | wc -l` after the
  run: 17 (16 before the run, +1 for `remedy/job-d6d60ea3d586425a`, left behind per constraint 4 —
  the job was never applied, no `job apply`, no `--approve`, no copy of its files into the checkout).

**G5 sizes** (`git show --numstat --format= <commit>` for C1a to C6, beside the block's stated
expected insertions where one is given):
| Commit | Reading | Expected | Match |
|---|---|---|---|
| C1a `13145ec2e` | 417 | 417 (222+195) | equal |
| C1b `983eafe95` | 270 | 270 | equal |
| C2 `bfd2bd8fc` | 35/0, 2/0, 9/10, 7/0 | 35/0, 2/0, 9/10, 7/0 | equal |
| C3 `33ce3a29f` | 4/2, 35/0, 17/1, 2/2 | 4/2, 35/0, 17/1, 2/2 | equal |
| C4 `10352b102` | 110/1 | 110/1 | equal |
| C5 `b5aebe4d0` | 132/0 | (none stated) | — |
| C6 `883aad85d` | 126/0 across 11 files | (none stated) | — |

`git status --porcelain` and `git log --oneline -n 9`, plus the push's real outcome and the open-PR
check, are reported in the worker's reply, since C7 (this commit) cannot record itself or anything
that follows it.

**Round's whole tracked path set** (constraint 3), measured with `git diff --name-only 045de81f5`
after C6 (before C7 is committed): `.agent/authored/f291-r2-block.md`,
`.agent/authored/f291-r2-plan.md`, `.agent/authored/f291-r2-records.diff`,
`.agent/authored/f291-r2-docs.diff`, `.agent/authored/f291-r2-code.diff`,
`.agent/authored/f291-r2-tests.diff`, `.agent/authored/f291-r2-selfuse.py`,
`.agent/authored/f291-r2-mutations.py`, `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`,
`docs/roadmap/STATUS_closure_protocol.md`, `docs/roadmap/features/T5_F291.md`,
`docs/system/self-use-track-v1.md`, `packages/orchestration/self_use_generator.py`,
`tests/orchestration/test_self_use_runner.py`, `scripts/self_use_queue.json`,
`.agent/selfuse_f291/SU-037.md`, `.agent/selfuse_f291/changed_paths.txt`,
`.agent/selfuse_f291/entry_and_job_file.txt`, `.agent/selfuse_f291/execution_config.txt`,
`.agent/selfuse_f291/full_transcript.txt`, `.agent/selfuse_f291/job_diff.txt`,
`.agent/selfuse_f291/result_state.txt`, `.agent/selfuse_f291/run_defects.txt`,
`.agent/selfuse_f291/staleness_after.txt`, `.agent/selfuse_f291/timing.txt` — every path is a member
of the block's stated set (constraint 3's list, `.agent/handoff.md` itself added by C7). No
`consumed_by` is set on `SU-037` in `scripts/self_use_queue.json` (verified in the C6 diff review
above) — the closure commit sets it, per the block.

## Authored-text proofs

All seven `.agent/authored/f291-r2-*` payload/block copies (block, plan, records diff, docs diff,
code diff, tests diff, selfuse.py) are byte-identical, source to committed copy, verified by an
independent hash-comparison script comparing `.remedy-wt/f291-r2/block.md` and each
`.remedy-wt/f291-r2-payloads/*` file against `git show <commit>:<path>` — all seven equal (G1,
above). The applied `records.diff` (→ `.agent/decisions.md`, `.agent/live_review.md`, and the
rewritten `.agent/plan.md` via `shutil.copyfile`) and `docs.diff`/`code.diff` (→
`docs/roadmap/STATUS_closure_protocol.md`, `docs/roadmap/features/T5_F291.md`,
`docs/system/self-use-track-v1.md`, `packages/orchestration/self_use_generator.py`) and `tests.diff`
(→ `tests/orchestration/test_self_use_runner.py`) all reproduced content matching the block's G1
sha256 table exactly at C2, C3 and C4 respectively — this confirms `git apply` and `shutil.copyfile`
reproduced the reviewer-authored text exactly, not only that the source payload itself was
uncorrupted.

## Deviations & assumptions

None. No payload was retyped or edited. No existing test was edited to pass. Every gate the block
ordered (G1 through G5) ran and read as the block predicted, with no red outside the self-use run's
own expected outcome (which completed, never blocked or stopped — no STOP condition was met). No
file outside the round's tracked path set (constraint 3) was touched (verified above). No `gh pr
create` or `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no `git stash`.
The full pytest suite was not run (constraint 8: it runs once, in the next round). The self-use job
was never applied: no `job apply`, no `--approve`, no copying of its files into the checkout; its
branch `remedy/job-d6d60ea3d586425a` and no evidence directory were left behind, reported above, and
nothing was deleted that this round did not itself create as scratch.

## Next

Per the block's `## Next` order: Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of
round 2 and of the self-use run's diff, then the integration gate (the one full suite). Open
findings: 0. Operator questions: 0.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a copy round 2 block, plan, records and docs diffs | done | 417 insertions, matching block's formula |
| C1b copy round 2 code and tests diffs and the self-use script | done | 270 insertions, matching expected |
| C2 book F291 R1, record D2, consolidate the checklist | done | numstat matched exactly; G1 hashes matched |
| C3 document the two new self-use sources and write the Built State | done | numstat matched exactly; G1 hashes matched |
| C4 add the reviewer's test | done | 110/1 numstat matched; G1 hash matched |
| C5 add the round 2 mutation tool | done | ruff clean; all 3 mutations caught, both controls clean, all restores byte-identical |
| C6 generate and run the closure's self-use item | done | job completed, task applied to workspace with verdict pass; item SU-037 matched the reviewer's stated reading exactly; run_defects NONE |
| C7 rewrite handoff | done | this commit |
| G1 transport and records | done | all payload and authored-copy hashes verified equal; nine-row table matched; open_finding_ids `[]`, latest_gate_verdict PASS, live_checklist_items 34 |
| G2 the tests | done | 685 passed/1 skipped at exit 0, matching the reviewer's reading; ruff clean; integrity check 6/6 pass, fail_count 0 |
| G3 the red proofs | done | all 3 mutations caught (exit 1, failed>0); both controls clean; all restores byte-identical; `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`; worktree count restored to 13 |
| G4 the self-use readings | done | SU-037, Tier 4, job completed, task applied_to_job_workspace/pass/staged_review_passed, real provider calls (claude-cli/claude-sonnet-4-6), 2 calls inside the cap of 8, cost $0.66 inside $6.00, run_defects NONE |
| G5 sizes, tree and push | done for C1a–C6 sizing; push/log/PR-list reported in the worker's reply |

Open findings: 0 (per `open_finding_ids` at C2). Operator questions open: 0.
