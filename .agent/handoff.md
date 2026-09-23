# Handback — F278 Durable writes & loud failures · Round 10 · Book round 9, register and repair R-1039, re-run the full suite

## Session

SESSION 2 of feature F278 · round 10 · rounds so far 10

This is the first closure repair round. It copied the round's block and
four payloads into `.agent/authored/` (C1); booked round 9's PASS into
`.agent/live_review.md` (the `Gate: F278 R9` entry, the registration of
R-1039 and the `Recurrence: R-1035` paragraph), and rewrote `.agent/plan.md`
(C2); applied the one-line repair to
`packages/orchestration/runtime_integration_gate.py` — the
`f146_registry_atomic_save` check now pins `durable_write(` instead of
`os.replace` — and appended the `Landed: R-1039` line to
`.agent/live_review.md` in the same commit (C3); and re-ran this feature's
ONE full suite, `python3 -m pytest -n auto -q`, which read GREEN — 18546
passed, 20 skipped, 1 warning, zero bad nodes, down from round 9's five —
with the transcript rewritten in `.agent/authored/f278-closure-suite.txt`
together with this handback (C4). All of G1-G5 ran and matched the block's
stated expectations exactly, including the red-proof mutation in the
disposable worktree, which turned the five nodes from 5 passed to 5 failed
and back. Context self-assessment: a comfortable majority of the working
budget remains at handback.

## Range

Review of `82c47da0`..`HEAD`.

## Commits

### 0320c1d0 F278 R10 C1: copy round 10 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r10-block.md | +170/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r10-landed.md | +2/-0 | Payload copy: the `Landed: R-1039` append |
| .agent/authored/f278-r10-ledger.md | +6/-0 | Payload copy: the round-9 booking + R-1039 registration + R-1035 recurrence append |
| .agent/authored/f278-r10-plan.md | +31/-0 | Payload copy: the plan.md rewrite |
| .agent/authored/f278-r10-repair.diff | +13/-0 | Payload copy: the one-line `git apply` patch for R-1039 |

Measured insertions: 222 (170+2+6+31+13), under the 500 cap.

### 4ddf5cf8 F278 R10 C2: book round 9's PASS, register R-1039, record R-1035's recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | `ledger.md` appended by byte concatenation onto the `82c47da0` bytes (round-9 `Gate:` entry, R-1039 registration, R-1035 recurrence) |
| .agent/plan.md | +10/-9 | Rewritten to the round-10 plan.md payload |

Measured insertions: 16 (6+10), deletions: 9, all from the plan.md rewrite.

### f6efb8e3 F278 R10 C3: pin the registry check on durable_write, not os.replace (R-1039)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/runtime_integration_gate.py | +1/-1 | `git apply` of repair.diff: `f146_registry_atomic_save`'s pattern changed from `"os.replace"` to `"durable_write("` |
| .agent/live_review.md | +2/-0 | `landed.md` appended by byte concatenation |

Measured insertions: 3 (1+2), deletions: 1.

### C4 (this commit) F278 R10 C4: record the repaired suite transcript and rewrite handoff for round 10
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-closure-suite.txt | rewritten | Round 10's full-suite transcript: real exit code, summary line, empty bad-node list, shrinking reading, closure precondition 7 sentence |
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add .remedy-wt/f278-r10-mut f6efb8e3` — real exit 0 (disposable, for the G4 red-proof mutation).
- `git worktree remove .remedy-wt/f278-r10-mut` — real exit 0.
- `git worktree prune` — run after removal, no output.
- `git push origin feature/f278-durable-writes-loud-failures` — see the session's final reply for the real outcome (it runs after this commit).
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no checkout of another branch or commit in the primary checkout: none run, per the block's constraints.
- The two pre-existing job worktrees/branches (`.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`) were left untouched throughout, per constraint 7.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, absent (proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `feature/f278-durable-writes-loud-failures`. `git log --oneline -1` → `82c47da0 F278 R9 C6: record the closure suite transcript and rewrite handoff for round 9`.
- Block bytes (R-0954): measured line count=170, sha256=`ab9e3c0ee35e5dc756803a365e660da5dacd1508c39da87bb92ab8940a0c68f9`; matches both given readings exactly.
- `git branch --list 'remedy/job-*' | wc -l` (before C1) → 39. `git worktree list` (before C1) → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` + `.remedy-wt/job-e7268925db3a4831`. `git stash list` first line (before C1) → `stash@{0}: WIP on (no branch): 365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`.

PAYLOADS — all 4 measured and matched the block's table exactly (lines/bytes/sha256): landed.md (2/147), ledger.md (6/6205), plan.md (31/1270), repair.diff (13/608). All sha256 readings matched the table verbatim.

G1 TRANSPORT — every `.agent/authored/f278-r10-*` copy (plus the block copy) read back with `git show 0320c1d0:<path>` and compared byte-for-byte against its source: all 5 copies matched exactly (block.md, landed.md, ledger.md, plan.md, repair.diff).

G2 THE BOOKING — at C2 (`4ddf5cf8`):
- `.agent/live_review.md`: bytes=459330, sha256=`dc0a16e000c814b320de877692f503af3ef7c36de036037074eca24c3b185e0b` — MATCH to the block's stated C2 reading.
- `.agent/plan.md`: sha256 `f49281be6771a77c0371aa6fdfbdb91434276f12b24787eccdfa81f651d870c0` — sha256-equal to plan.md payload; line count 31, under 50.

Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md` TEXT: at `82c47da0` count=26; at C2 (`4ddf5cf8`) count=27; added=`['R-1039']`; removed=`[]` — matching the block's 26/27, ADDED exactly `R-1039`, REMOVED none.

At C3 (`f6efb8e3`): `.agent/live_review.md` bytes=459477, sha256=`dff9cb12ada89fe31546426c67cd611ea59c84ddf7fb2e47eef9a30c3034c7d5` — MATCH to the block's stated C3 reading. Line-anchored counts on the C3 text: `^Gate: F278 R9 — ` 1, `^- R-1039 — ` 1, `^Recurrence: R-1035 — ` 1, `^Landed: R-1039 — ` 1 — all match.

G3 THE REPAIR — `git diff 4ddf5cf8 f6efb8e3 -- packages/orchestration/runtime_integration_gate.py` compared byte-for-byte against `repair.diff`: both 608 bytes, EQUAL. `python3 -m ruff check packages/orchestration/runtime_integration_gate.py` → `All checks passed!`, real exit 0. `python3 -m pytest -q -p no:cacheprovider` over the seven named files (`test_runtime_integration_gate.py`, `test_f018_authority_integration.py`, `test_f018_package_pipeline_e2e.py`, `test_f146_package_pipeline_e2e.py`, `test_project_resolution.py`, `test_project_registry.py`, `tests/cli/test_golden_path.py`) → `356 passed in 140.73s (0:02:20)`, real exit 0 (the reviewer's dry run of the first six read 314 passed; 356 is that plus the golden path file).

G4 THE RED PROOF — disposable worktree `.remedy-wt/f278-r10-mut` added at `f6efb8e3`. CONTROL, the five round-9 bad node ids under `python3 -B -m pytest -q -p no:cacheprovider`: `5 passed in 0.39s`, real exit 0. The exact bytes `"pattern": "durable_write(",` occur exactly once in the worktree's copy of `packages/orchestration/runtime_integration_gate.py` (measured before mutation). Original bytes saved via `shutil.copyfile`; the pattern replaced with `"pattern": "os.replace",`; the same five node ids re-run → `5 failed in 0.42s`, real exit 1, every failure the expected `verdict == BLOCKED` / `checks_passed` / `found` assertion break. File restored from the saved bytes via `shutil.copyfile`; byte-identity confirmed (`restore byte-identical: True`, sha256 `10b0e0e87c5864b17e1923c13ba38cccd05dc7e44b0718aff938e6e91ba1cdbe`). `git worktree remove .remedy-wt/f278-r10-mut` then `git worktree prune`, both real exit 0. `git worktree list` after: primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` + `.remedy-wt/job-e7268925db3a4831` — unchanged from before C1, the mutation worktree gone.

G5 THE SUITE AND THE SHRINKING RULE — at C4: `python3 -m pytest -n auto -q` in the primary checkout, real exit code 0. Summary line: `18546 passed, 20 skipped, 1 warning in 251.83s (0:04:11)`. Zero `FAILED`/`ERROR` lines in the captured log. Bad node ids: none (0). Shrinking reading: previous bad set (round 9's five ids, all `f146_registry_atomic_save`/`build_runtime_integration_gate` checks) → new bad set (empty) → the new set IS a strict subset of the previous set → no node is newly bad. Neither `tests/orchestration/test_import_reachability.py` nor `tests/test_no_orphan_modules.py` is among the bad nodes (closure precondition 7 intact, vacuously — there are no bad nodes). `python3 -m apps.cli.main integrity check --json` → `fail_count: 0`, `ok: true`, `passed: true`, all 5 checks `pass` (`handler_import` handlers=145, `live_review_verdict`, `plan_consistency` unchecked=0 context_complete=False, `relevant_untracked` untracked=0 relevant=0, `high_blockers_open` no open blocker/high findings). `git status --porcelain` → empty, immediately before this commit (only the rewritten `.agent/authored/f278-closure-suite.txt` staged for it).

G6 TREE AND PUSH — reported in the session's final reply, not this file, since it runs after this commit (C4). The handback cannot contain readings that postdate its own write.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- This block (`f278-r10-block.md`): `.agent/authored/f278-r10-block.md` at C1 verified byte-identical to `.remedy-wt/f278-r10-block.md` (G1) and to the two readings given in the delegation message.
- `landed.md` (append): `.agent/live_review.md` at C3 sha256 `dff9cb12...eef9a30c3034c7d5` == payload sha256 concatenated onto the C2 bytes (G2/G3). MATCH.
- `ledger.md` (append): `.agent/live_review.md` at C2 sha256 `dc0a16e0...074eca24c3b185e0b` == payload sha256 concatenated onto the `82c47da0` bytes (G2). MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256 `f49281be...81f651d870c0` == payload sha256 exactly (G2). MATCH.
- `repair.diff` (applied via `git apply`): `git diff <C2> <C3> -- packages/orchestration/runtime_integration_gate.py` == payload byte-for-byte, 608 bytes both (G3). MATCH.
- C4's rewritten suite transcript is worker-authored prose reporting measured readings, not a reviewer payload; no authored-text fidelity claim applies to it.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| G1 TRANSPORT | done | |
| G2 THE BOOKING | done | |
| G3 THE REPAIR | done | diff match, ruff clean, 356 passed (314 + golden path) |
| G4 THE RED PROOF | done | control 5 passed, mutated 5 failed, restore byte-identical, worktree removed |
| G5 THE SUITE AND THE SHRINKING RULE | done | GREEN, 0 bad nodes, strict subset of round 9's five, none newly bad |
| G6 TREE AND PUSH | done | reported in the session's final chat reply, not this file |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1, C2, C3, C4)
exactly and touched exactly the tracked path set constraint 3 names
(verified via `git diff --name-only 82c47da0 HEAD` before C4: 8 paths, all
within the allowed set; C4 adds exactly the two more paths the block
orders — `.agent/authored/f278-closure-suite.txt` and `.agent/handoff.md`).
No procedural deviations from the block's ordered steps.

One environment note, not a scope deviation: the sandbox rejected an
inline `python3 -c "..."` one-liner containing a `#` after a newline
inside a quoted argument ("Newline followed by # inside a quoted argument
can hide arguments from path validation"); every multi-step Python task
in this round was instead written to a file under
`.remedy-wt/f278-r10-scratch/` and run with `python3 <file>`, per the
block's own guidance to put multi-step code in a scratch file.

C4's full suite is GREEN (0 failed) — the five nodes R-1039 named are all
fixed, and no other node went bad. The transcript is committed exactly as
measured; the shrinking rule's obligation (no newly-bad node, previous bad
set gone) is met.

`.remedy-wt/job-129b3ad7206d4f8d` and `.remedy-wt/job-e7268925db3a4831`
(both pre-existing before this round) are left in place untouched, per
constraint 7. No other deviation.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
10, then the closure sequence's second half — the evidence job and the
review zip — and then the closing round: the ledger rotation, the STATUS
line with the README counters in the same commit, and the pull request.
Open findings: 27, one of them (R-1039) this feature's own until its
resolution is booked. Operator questions: 0.
