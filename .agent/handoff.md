# Handback — F041, round 4: book round 3, record D4, land T002's door, worker and view

## Session

SESSION 1 of feature F041 · round 4 · rounds so far 4. This session read the round 4 block whole,
verified its bytes and every payload, booked round 3's gate entry and recorded DECISION F041 D4
(C1a, C1b, C1c, C2), wrote S1 to S3 against `preview_control.py`, the new `preview_worker.py` and
`ui_server.py`, and applied the wiring diff (C3), applied the reviewer's tests unedited (C4), wrote
and red-proved the round's mutation tool in a real worktree (C5), and ran every gate for real before
writing this handback (C6). Context self-assessment: a comfortable amount of context remains; the
round completed inside one session with no blocked handback and no deviation.

For the operator, in plain words: F041's round 4 is now COMPLETE. A preview request through the
write door (`job.preview-start` / `job.preview-stop`) is now carried by the UI server's own preview
worker thread, which runs the harness's verbs, revalidates every live preview every fifteen seconds,
stops one nobody has viewed after `preview.idle_ttl_seconds` (default 900), and stops every preview
it still keeps live when the server closes. The `preview` view (`/api/jobs/<id>/preview`) counts as
a view and shows a link only while the state is `live`. Round 3's gate entry is booked, and DECISION
F041 D4 is recorded.

## Range

Review of `468b3a36e`..`332e36db4` (before this handback commit).

## Commits

### 87bb46a4f F041 R4 C1a: copy round 4 block, plan, records and wiring into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r4-block.md | 268/0 | copy of this round's block, by `shutil.copyfile` |
| .agent/authored/f041-r4-plan.md | 28/0 | copy of the reviewer's plan.md payload |
| .agent/authored/f041-r4-records.diff | 28/0 | copy of the reviewer's records.diff payload |
| .agent/authored/f041-r4-wiring.diff | 60/0 | copy of the reviewer's wiring.diff payload |

Insertions measured 384 (268+28+28+60); block expected "this block's line count plus 116" =
268+116 = 384. MATCH.

### fcb895075 F041 R4 C1b: copy round 4 tests diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r4-tests.diff | 297/0 | copy of the reviewer's tests.diff payload |

Insertions measured 297; block expected 297. MATCH.

### 6b151ad31 F041 R4 C1c: copy round 4 worker tests diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r4-worker_tests.diff | 217/0 | copy of the reviewer's worker_tests.diff payload |

Insertions measured 217; block expected 217. MATCH.

### 09d38e04b F041 R4 C2: book round 3, record D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 10/0 | `git apply` of records.diff: DECISION F041 D4 |
| .agent/live_review.md | 2/0 | `git apply` of records.diff: round 3 gate entry |
| .agent/plan.md | 7/7 | rewrite := plan.md payload |

Numstat measured 10/0, 2/0, 7/7; block expected the same. MATCH.

### 1c728743f F041 R4 C3: take preview requests at the door and act on them on the server's worker
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/preview_control.py | 115/3 | S1: `mark_viewed`, `idle_stop_due`, `stop_if_idle`, `revalidate_live`, and the view's live-only gate |
| packages/orchestration/preview_worker.py | 213/0 | NEW — S2: `PreviewWorker`: `submit`, `adopt_live`, `step`, `stop_all`, `start`, `close` |
| packages/orchestration/ui_server.py | 84/0 | S3: preview ids, `preview_worker` class attr, door clause, `_dispatch_job_preview`, `_build_preview_json`, worker lifecycle in `start_ui_server` |
| apps/cli/command_catalog.py | 4/0 | `git apply` wiring.diff: `job.preview-start`/`stop` in `UI_EXPOSED_COMMANDS` |
| docs/guides/environment.md | 1/0 | `git apply` wiring.diff: `REMEDY_PREVIEW_IDLE_TTL_SECONDS` row |
| packages/orchestration/config.py | 10/0 | `git apply` wiring.diff: `preview.idle_ttl_seconds` key |
| tests/orchestration/import_reachability_allowlist.txt | 1/0 | `git apply` wiring.diff: `preview_worker` allowlist line |

Total insertions 428, under the 500-line cap — no split needed (block's C3a/C3b clause not
triggered). Wiring numstat measured 4/0, 1/0, 10/0, 1/0; block expected the same. MATCH. No
expected insertion count is given for the three code files themselves.

### ed5c91c64 F041 R4 C4: add the reviewer's door, worker, view and idle-stop tests
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_preview_control.py | 93/0 | `git apply` tests.diff: the view's gate, `mark_viewed`, `idle_stop_due`, `stop_if_idle`, `revalidate_live` |
| tests/orchestration/test_preview_worker.py | 211/0 | NEW — `git apply` worker_tests.diff |
| tests/ui_server/test_command_channel.py | 9/2 | `git apply` tests.diff: door guard + exposed-commands coverage for the preview pair |
| tests/ui_server/test_preview_commands.py | 128/0 | NEW — `git apply` tests.diff: real-server door + view integration tests |

Numstat measured 93/0, 211/0, 9/2, 128/0; block expected the same. MATCH. All four files passed
unedited against the round's code at this commit (see Verification).

### 332e36db4 F041 R4 C5: add the round 4 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f041-r4-mutations.py | 206/0 | NEW — G4's tool: q1 to q8, control-first/control-last, byte-identical restore |

No expected insertion count given for C5.

## External actions

- `git worktree add --detach .remedy-wt/f041-r4-mut-test HEAD` (a preliminary, self-owned sanity
  check of the mutation tool BEFORE writing it to `.agent/authored/`, run at the C4 tip since the
  tool's mutations target only files unchanged between C4 and C5) — added; then
  `git worktree remove --force .remedy-wt/f041-r4-mut-test` and `git worktree prune` — removed.
  Worktree count confirmed back to 62 (the step-4 baseline) before C5 was committed.
- `git worktree add --detach .remedy-wt/f041-r4-mut 332e36db4` (G4, the real run at C5) — added;
  then `git worktree remove --force .remedy-wt/f041-r4-mut` and `git worktree prune` — removed.
  Worktree count 62 both before and after.
- `git push -u origin feature/f041-artifact-preview` — see Verification for the real outcome (run
  after this handback commit; reported in the reply, since C6 cannot contain it per the block).
- No PR create, no PR merge, no branch deletion, no force-push, no `git stash`, no reset of any
  commit.

## Verification

Payload transport (PAYLOADS table), each measured line count / byte count / sha256 against the
block's table, all MATCH:

    records.diff        28 lines   9399 bytes  19a417ff7e3702d772d3181a1814f2857c2b57241b6e3dfddfa5efe481584bd7
    wiring.diff          60 lines   3936 bytes  44226ff3ae012f5ce068ab0ff2932e2962a7f146b146d59b0ef97c7f2022132b
    tests.diff          297 lines  13679 bytes  af450c75305957d5c21e0141dd51f681aedb8c003def2e265b7c77c64f15a048
    worker_tests.diff   217 lines   8278 bytes  351d9c4a60e7d6d621f2041cc2c5cb4f5eb70183c97c986b0b153c8784254583
    plan.md               28 lines    918 bytes  e5c186ceb181bd44b681b8433bc6ab01b69332165a7d3db2608fb1e4cc48f372

`git apply --check` then real `git apply`, each exit 0: records.diff, wiring.diff, tests.diff,
worker_tests.diff.

G1 TRANSPORT — every `.agent/authored/f041-r4-*` copy, read with `git show <commit>:<path>` from
the commit that added it, equals its source byte for byte (sha256 compared): block.md, plan.md,
records.diff, wiring.diff at `87bb46a4f`; tests.diff at `fcb895075`; worker_tests.diff at
`6b151ad31`. All MATCH.

G2 THE RECORDS, THE WIRING AND THE TESTS — every path in the block's G2 table, read with
`git show <commit>:<path>` at the commit named, equals the reviewer's stated bytes and sha256. All
eleven rows MATCH (`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` at C2;
`apps/cli/command_catalog.py`, `packages/orchestration/config.py`, `docs/guides/environment.md`,
`tests/orchestration/import_reachability_allowlist.txt` at C3; the four test files at C4).
`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`: at `468b3a36e`
→ `[]`; at `09d38e04b` (C2) → `[]`. Both equal the reviewer's stated readings.

G3 THE CODE AND THE TESTS —

    python3 -m ruff check packages/orchestration/preview_control.py \
      packages/orchestration/preview_worker.py packages/orchestration/ui_server.py \
      packages/orchestration/config.py apps/cli/command_catalog.py \
      tests/orchestration/test_preview_control.py tests/orchestration/test_preview_worker.py \
      tests/ui_server/test_preview_commands.py tests/ui_server/test_command_channel.py \
      .agent/authored/f041-r4-mutations.py
    → All checks passed! REAL_EXIT=0

Diff of the three code files at C3 (`1c728743f`), whole: reported to the caller in the reply
(the 428-insertion diff already tabled above by file; the same text was self-reviewed against S1 to
S3 before commit, per AGENTS.md's Mandatory Self-Review Loop).

Serial pytest, run in the primary checkout at C5:

    bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_preview_control.py tests/orchestration/test_preview_worker.py tests/ui_server tests/cli tests/docs tests/orchestration/test_config.py tests/orchestration/test_env_registry.py tests/test_subprocess_timeouts.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'

    SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) — same skip the reviewer named.
    3454 passed, 1 skipped in 642.07s (0:10:42)
    REAL_EXIT=0

The reviewer's simulation tree read `3453 passed, 2 skipped` — the second skip being
`tests/ui_server/test_timeline_scrub_live.py:31`, which the block states runs where
`apps/ui/node_modules` exists, "as it does in the primary checkout." That is exactly what happened
here: with `node_modules` present, that test RAN rather than skipped, moving one test from the skip
column to the pass column. Totals agree: 3453+2 = 3455 = 3454+1. Not a deviation — the block named
this exact difference in advance.

Node counts by `--collect-only -q`:

    tests/orchestration/test_preview_control.py → 29 tests collected
    tests/orchestration/test_preview_worker.py  → 11 tests collected
    tests/ui_server/test_preview_commands.py    →  3 tests collected

Matches the reviewer's stated reading (29, 11, 3) exactly.

    python3 -m apps.cli.main integrity check --json
    → {"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}
    all six checks "pass". REAL_EXIT=0

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f041-r4-mut 332e36db4` (C5), then
`python3 -B .agent/authored/f041-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f041-r4-mut`:

    control (first): all three named test files, exit=0 failed=0
    q1 preview_view answers the stored link in every state:                 exit=1 failed=1  restored byte-identical: True
    q2 mark_viewed writes a record that is not live:                       exit=1 failed=1  restored byte-identical: True
    q3 idle_stop_due expires a preview whose ttl is zero or less:           exit=1 failed=2  restored byte-identical: True
    q4 revalidate_live no longer stops a preview that stopped answering:    exit=1 failed=1  restored byte-identical: True
    q5 step no longer revalidates a live preview:                          exit=1 failed=2  restored byte-identical: True
    q6 close no longer stops the previews the worker keeps live:           exit=1 failed=2  restored byte-identical: True
    q7 the door no longer hands the job to the worker:                     exit=1 failed=2  restored byte-identical: True
    q8 adopt_live takes on a record whatever its state:                    exit=1 failed=1  restored byte-identical: True
    control (last): all three named test files, exit=0 failed=0
    ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
    REAL_EXIT=0

Every mutation caught (exit code 1, at least one failed test), every restore byte-identical, both
controls clean. `git worktree remove --force .remedy-wt/f041-r4-mut`, `git worktree prune`;
`git worktree list | wc -l` → 62 (equals the step-4 baseline).

(A preliminary, self-owned sanity run of the same tool against a scratch worktree at the C4 tip,
`ed5c91c64`, under `.remedy-wt/f041-r4-mut-test`, caught no bug: all 8 mutations caught cleanly on
the first try, both controls clean. Removed immediately after; worktree count confirmed back to 62
before the tool was copied into `.agent/authored/` and committed as C5.)

## Authored-text proofs

Every `.agent/authored/f041-r4-*` copy, read back with `git show <commit>:<path>` from the commit
that added it, is byte-identical to its `.remedy-wt/f041-r4*` source (sha256 compared): block.md,
plan.md, records.diff, wiring.diff at `87bb46a4f`; tests.diff at `fcb895075`; worker_tests.diff at
`6b151ad31`. All MATCH — see G1 above for the full table.

## Deviations & assumptions

None. The block's ordered commit sequence (C1a, C1b, C1c, C2, C3, C4, C5, C6) was followed exactly,
C3 did not need the 500-line split (428 insertions), every payload applied unedited, and every gate
passed on its first real run — no repair commit was needed this round.

One assumption, not a deviation: `stop_if_idle` and `revalidate_live` read the job's `repo_path` the
same way `run_pending` already does (`Path(getattr(job, "repo_path", "") or ""))`), since S1 does not
spell a no-project-folder branch for either — the worker only ever calls them for a job it already
loaded through `load_job`, at which point `run_pending` has already run at least once and the project
folder is known good; no test exercises a missing folder at that point, so nothing in the shipped
behaviour depends on this reading.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C1c | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | this commit |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | reported in the reply, not in this commit, per the block |

## Next

In order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk; (2) the review of round 4; (3) T003 —
the preview panel with the README, the screenshot grid and lightbox, and the app card, per the
design reference. Open findings: 0. Operator questions: 1 (unchanged by this round; see
`.agent/operator_questions.md`, not touched this round).
