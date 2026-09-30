# Handback — F043 round 7: the closure's integration gate — book round 6, land SU-038, add its
tests and Built State paragraph, add the round's mutation tool, and run the one full suite

## Session

SESSION 1 of feature F043 · round 7 · rounds so far 7. Context self-assessment: a comfortable
majority of the session's context window remained when this handback was written, after all six
commits and gates G1 through G4.

## Range

Review of `6b2c3e8c6`..HEAD (this round's final commit, C7 — the push's real outcome and
`gh pr list` are reported in the worker's reply, since this file is committed as part of C7 and
cannot name a push that follows it).

## Commits

### `a358edc75` F043 R7 C1: copy round 7 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f043-r7-block.md | +199/-0 | this round's block, copied verbatim via `shutil.copyfile` |
| .agent/authored/f043-r7-docs.diff | +18/-0 | payload copy |
| .agent/authored/f043-r7-plan.md | +28/-0 | payload copy |
| .agent/authored/f043-r7-records.diff | +42/-0 | payload copy |
| .agent/authored/f043-r7-selfuse.diff | +26/-0 | payload copy |
| .agent/authored/f043-r7-tests.diff | +53/-0 | payload copy |

Total 366 insertions, matching the block's stated formula exactly (block's 199 lines + 167).

### `ba7df3e03` F043 R7 C2: book F043 R6, record D6
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +24/-0 | `git apply records.diff`: DECISION F043 D6 appended |
| .agent/live_review.md | +2/-0 | `git apply records.diff`: round 6's Gate entry appended |
| .agent/plan.md | +6/-8 | rewrite := plan.md payload |

Every numstat reading equals the block's expected table exactly (24/0, 2/0, 6/8). `git apply
--check` on records.diff read exit 0 before the real apply, which also read exit 0.

### `ea86dd6b2` F043 R7 C3: land SU-038, narrow the viewer helper's constitution handler to OSError
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/brain.py | +1/-1 | `git apply selfuse.diff`: `_prepare_viewer`'s handler narrowed from `except Exception:  # noqa: BLE001 ...` to `except OSError:` |
| tests/test_ble001_ratchet.py | +1/-1 | `git apply selfuse.diff`: `MAX_EXCUSED` lowered from 289 to 288 |

Every numstat reading equals the block's expected table exactly (1/1, 1/1). `git apply --check`
read exit 0 before the real apply, which also read exit 0. This diff is byte-for-byte the same
diff the self-use job produced: `git diff 6b2c3e8c6...remedy/job-d1a4eea4787f420c`, written to the
worker's own directory and `cmp`'d against `selfuse.diff`, reported no difference (exit 0).

### `10af55316` F043 R7 C4: add the reviewer's tests for the viewer helper's narrowed handler
| Path | +/- | Reason |
|---|---|---|
| tests/test_brain_viewer.py | +42/-0 | `git apply tests.diff`: two tests added to `TestConstitutionGuard` — a `PermissionError` loader still writes the viewer, a `RuntimeError` loader reaches the caller with none written |

Every numstat reading equals the block's expected table exactly (42/0). `git apply --check` read
exit 0 before the real apply, which also read exit 0.

### `d64531c42` F043 R7 C5: record the closure's self-use item in F043's Built State
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F043.md | +8/-0 | `git apply docs.diff`: the self-use item's paragraph (job id, provider/model, cost, diff summary, DECISION F043 D6) |

Every numstat reading equals the block's expected table exactly (8/0). `git apply --check` read
exit 0 before the real apply, which also read exit 0.

### `d6e77ea37` F043 R7 C6: add the round 7 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f043-r7-mutations.py | +140/-0 | the G3 red-proof tool: m1 reverts the landed handler to `Exception`, m2 narrows it to `ValueError` instead of `OSError` |

Total 140 insertions; the block states no expected count for C6, so this is the real count,
reported as ordered.

### `<this commit>` F043 R7 C7: record the closure suite transcript and rewrite handoff for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f043-closure-suite.txt | new file | the C7(b) full-suite transcript: command, real exit code, wall time, summary line, bad node ids (`NONE`), and the tree it ran on (`d6e77ea37`) |
| .agent/handoff.md | rewrite | this file, per `docs/agents/handback_template.md` |

## External actions

- `git worktree add --detach .remedy-wt/f043-r7-mut d6e77ea37` then, after G3,
  `git worktree remove --force .remedy-wt/f043-r7-mut` and `git worktree prune` — both run by the
  worker directly, per the block's G3 instruction. `git worktree list | wc -l` read 11 before
  (step 4) and 11 again after G3 (unchanged: the mutation worktree was added and removed inside the
  same gate).
- `git push -u origin feature/f043-explanation-layer` — real outcome reported in the worker's
  reply, since it runs after this commit.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no
  `git stash`, no self-use run, no job that calls a provider — none ordered this round. The branch
  `remedy/job-d1a4eea4787f420c` was left untouched throughout.

## Verification

**BEFORE ANYTHING ELSE** —
- `ls .agent/STOP` → `ls: cannot access '.../.agent/STOP': No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty. `git branch
  --show-current` → `feature/f043-explanation-layer`. `git log --oneline -1` → `6b2c3e8c6 F043 R6
  C6: rewrite handoff for round 6` — all three match the block's stated readings.
- Block bytes (R-0954): measured line count (newline count) 199, sha256
  `78c861bebed39ba9d3c9c020923f9ed4a17a5175fd31a81dfbf41222cd56e25b`, both equal the two readings
  the delegation message stated.
- `git worktree list | wc -l` → 11. `git branch --list 'remedy/*' | wc -l` → 18.

**PAYLOADS TABLE** — every reading measured before use, all five exact matches against the block's
table:
| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 42 | 6305 | `beb5fbdcda2eae2abaf6d3b65268515385b7adb5daf4e70b60c07f0cdb3ba22a` |
| selfuse.diff | 26 | 1154 | `50178f8e5e5a2a8fc7405806d6bc709923787fbe41f7507a3bd6ef616446eab9` |
| tests.diff | 53 | 2643 | `212f66d3a13555d341783fb2dcff0b3b4f336666db0f6ee014028b5fc73d7865` |
| docs.diff | 18 | 1144 | `ab3770115c8c9ec8936ca50f3d7b46487d308c3f2c3f0b73c600e47ef5bede70` |
| plan.md | 28 | 974 | `e4cb59cb361c9544bef8d110ab5d7374eec73b270e5d1d596316054a50cac471` |

**G1 TRANSPORT AND RECORDS** — every `.agent/authored/f043-r7-*` copy, read back with `git show
<commit>:<path>` from C1, was byte-for-byte identical to its source: block.md against
`.remedy-wt/f043-r7/block.md`, plan.md/records.diff/selfuse.diff/tests.diff/docs.diff against
their payloads — 6 pairs, all `byte_equal: True`.

Every committed file's bytes and sha256 at its named commit equaled the block's given values
exactly:
- `.agent/decisions.md` @ C2 (2537033 bytes, `3808a8ca...6d34ff`) — match
- `.agent/live_review.md` @ C2 (133368 bytes, `a7e7362f...d996dc6`) — match
- `.agent/plan.md` @ C2 (974 bytes, `e4cb59cb...50cac471`) — match
- `apps/cli/commands/brain.py` @ C3 (20311 bytes, `10fa9b4c...264f52c`) — match
- `tests/test_ble001_ratchet.py` @ C3 (2243 bytes, `453a2f1d...3aac315b3`) — match
- `tests/test_brain_viewer.py` @ C4 (55575 bytes, `ee1ce293...fdab1380`) — match
- `docs/roadmap/features/T5_F043.md` @ C5 (8263 bytes, `a0e7d8a7...bbb944d9e74`) — match

`open_finding_ids` (from `scripts/rotate_live_review.py`) over the ledger text at C2 read `[]`,
`latest_gate_verdict` read `PASS` — both matching the reviewer's stated reading exactly.

`cmp` of `selfuse.diff` against `git diff 6b2c3e8c6...remedy/job-d1a4eea4787f420c`, written fresh
to the worker's own directory, reported no difference (exit 0).

**G2 THE TESTS** (at C6) —
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/test_brain_viewer.py tests/test_ble001_ratchet.py tests/test_context_coverage.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/docs tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -8; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
805 passed, 1 skipped in 82.15s (0:01:22)
REAL_EXIT=0
```
Matches the reviewer's dry-tree reading exactly (`805 passed, 1 skipped` at exit 0), the one
SKIPPED line the D12 quarantine, same as stated.
- `python3 -m ruff check apps/cli/commands/brain.py tests/test_brain_viewer.py
  tests/test_ble001_ratchet.py .agent/authored/f043-r7-mutations.py` → `All checks passed!`, exit 0.
- `python3 -m apps.cli.main integrity check --json` → all six checks `pass`
  (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`,
  `repo_root_hygiene`, `high_blockers_open`), `fail_count` 0, `"ok": true, "passed": true`.

**G3 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f043-r7-mut d6e77ea37`, exit 0. Full
tool output:
```
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f043-r7-mut
=== CONTROL (before) ===
control (before): pytest exit=0 failed=0 all_pass=True
m1: exit=1 failed=1
restored byte-identical: True
m2: exit=1 failed=1
restored byte-identical: True
=== CONTROL (after) ===
control (after): pytest exit=0 failed=0 all_pass=True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Both mutations turned `tests/test_brain_viewer.py` red at exit 1, 1 failed each, both controls
passing and both restores byte-identical — matching the reviewer's stated own-probe reading
exactly (both mutations red, each at 1 failed). `git worktree remove --force
.remedy-wt/f043-r7-mut`, exit 0; `git worktree prune`, exit 0; `git worktree list | wc -l` → 11
(unchanged).

**G4 THE INTEGRATION GATE** —
(a) UI build: `apps/ui/node_modules/.bin/vite build` (cwd `apps/ui`), exit 0, last line `- Adjust
chunk size limit for this warning via build.chunkSizeWarningLimit.` (a chunk-size advisory, not an
error; the build itself reports `✓ built in 2.25s`). `git status --porcelain` after it → empty.

(b) Full suite:
```
$ python3 -m pytest -n auto -q
20984 passed, 20 skipped, 1 warning in 187.91s (0:03:07)
REAL_EXIT=0
```
Wall time measured by the wrapper: 188.63s. Bad node ids (failed + errors): `NONE` — grepped the
full log for `^FAILED`/`^ERROR`, 0 matches. Log at
`.remedy-wt/f043-r7-worker/closure-suite.log`. Transcript committed at
`.agent/authored/f043-closure-suite.txt`, naming the tree it ran on: `d6e77ea37`.

`pgrep -af server.py` afterwards: the only line returned was the `pgrep` invocation's own command
line (the shell wrapper's argv contains the literal substring `server.py` inside the quoted
command), confirmed by re-running `pgrep -af server.py | grep -v "pgrep -af server.py"`, which
returned nothing — no actual `server.py` process is running.

## Authored-text proofs

Every `.agent/authored/f043-r7-*` copy (the block, plan.md, records.diff, selfuse.diff, tests.diff,
docs.diff) was compared byte-for-byte against its source under `.remedy-wt/f043-r7-payloads/` (and
the block itself against `.remedy-wt/f043-r7/block.md`), read back with `git show <commit>:<path>`
from C1: all 6 pairs match (G1 above). None of the four diffs (`records.diff`, `selfuse.diff`,
`tests.diff`, `docs.diff`) was edited or retyped; each applied with `git apply --check` (exit 0)
then `git apply` (exit 0) verbatim. `selfuse.diff` additionally matched, byte for byte, a fresh
`git diff 6b2c3e8c6...remedy/job-d1a4eea4787f420c` computed by the worker (`cmp` exit 0).

## Item status (AGENTS.md Completion Report)

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | UI build exit 0, full suite `20984 passed, 20 skipped` at exit 0, no bad node ids |
| G1 | done | |
| G2 | done | |
| G3 | done | both mutations caught, both restores byte-identical |
| G4 | done | |
| G5 | done | sizes reported above; tree/push/`gh pr list` reported in the worker's reply (run after C7) |

## Deviations & assumptions

- None. Every payload applied unedited (`git apply --check` exit 0 before each real apply, both
  exit 0 every time), every numstat reading equaled the block's expected table exactly, the test
  selection at C6 matched the reviewer's dry-tree reading exactly (`805 passed, 1 skipped`, same
  skip), the ruff and integrity gates read clean, both G3 mutations were caught and restored
  byte-identical, the UI build succeeded, and the one full suite passed with no bad node ids. No
  departure from the block's ordered commit sequence C1-C2-C3-C4-C5-C6-C7: every commit landed in
  order, none dropped, none added, none reordered. The tracked path set at the tip
  (`git diff --name-only 6b2c3e8c6`) contains only paths the block's constraint 3 names;
  `scripts/self_use_queue.json` was not touched, as ordered.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 7 and of the suite
transcript, then the evidence bundle and the review package (the suite is green), or the first
repair round if the reviewer's own re-derivation disagrees. Open findings: 0. Operator questions: 0.
