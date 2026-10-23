# Handback — F314 "Findings paydown v10," round 5

## Session

SESSION 1 of feature F314 · round 5 · rounds so far 5

Context self-assessment: this session booked round 4's PASS verdict, resolved six findings carried
from rounds 3 and 4, recorded DECISION F314 D7 for the hosted runner's three findings, repaired the
scale harness's git identity and the sandbox test's disk search to match that decision, ran every
gate exactly once after the last commit, and is about to push and dispatch one hosted run.

State block:
Feature F314 (claimed `[~]`), branch `feature/f314-findings-paydown-v10`, base `ba1c97279`.
Fortschritt: ~65 % (T001 to T005 landed, T006 awaiting its hosted run · T007 and T008 open) — Schätzung

## Range

Review of `ba1c97279`..HEAD.

## Commits

### ba89c7248 F314 R5 C1: book F314 R4, resolve six findings, DECISION F314 D7
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f314-r5.md` | +93/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/decisions.md` | +10/-0 | DECISION F314 D7 appended (the hosted runner's three findings) |
| `.agent/live_review.md` | +16/-0 | F314 round 4's PASS gate entry and the resolutions of R-1326, R-1425, R-1446 and R-1447 appended, plus R-1427's reproduction recorded as a Recurrence |
| `.agent/plan.md` | +7/-7 | rewritten for F314 round 5 |

All four paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py` and a
direct sha256 comparison (see Authored-text proofs) confirm each equality.

### 271ccac5e F314 R5 C2: the harness repositories carry their own git identity, and the disk search prunes the read-only toolchain (R-1427, R-1428)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/scale_harness.py` | +7/-1 | `commit_repository` now writes `user.email`, `user.name` and `commit.gpgsign` into the repository's own configuration, in addition to passing them on each git call, so a commit the harness makes works on a machine with no global git identity |
| `tests/orchestration/test_tool_sandbox.py` | +13/-3 | the whole-disk search test now prunes the sandbox's own read-only trees (`/proc`, `/dev`, the system directories and the run's toolchain directories) by full path with `find`, instead of excluding three directories by base name with `grep --exclude-dir`, so a hosted runner's much larger toolchain no longer makes the search time out while every other directory stays searched |

Both paths are byte copies of the reviewer's prepared `c2-*` files; gate 1's `verify.py` and a direct
sha256 comparison (see Authored-text proofs) confirm each equality. Self-review ran over
`git diff --cached` before this commit: both diffs matched their prepared files exactly, touched
only the two named test files, and introduced no behaviour change outside the two findings.

### this commit — F314 R5 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | n/a (self-reference; R-0149 pattern) | this handback, rewritten per `docs/agents/handback_template.md` |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `ba89c7248`, exactly the four named paths, each byte-equal to its prepared `c1-*` file |
| C2 | done | `271ccac5e`, exactly the two named paths, each byte-equal to its prepared `c2-*` file |
| C3 | done | this commit, `.agent/handoff.md` only |
| Gate 1 (`verify.py`) | done | every line `True`, `C3` read `absent`, last line `ALL True` |
| Gate 2 (`ruff check .`) | done | `All checks passed!` |
| Gate 3 (pytest selection) | done | exit 0, `3823 passed, 2 skipped in 105.00s`, no FAILED/ERROR/`process(es) behind` line |
| Gate 4 (integrity) | done | `"fail_count": 0` |
| Gate 5 (open finding ids) | done | `9` |
| Push | done | see External actions / the reply after this handback |
| Dispatch | pending | dispatched after this commit is pushed; its run id is in the worker's reply and the reviewer books it |

## External actions

- `git push origin feature/f314-findings-paydown-v10` — to run immediately after this commit,
  carrying `ba89c7248`, `271ccac5e` and this handback's own commit; see the reply for the push's
  own result. The branch already tracks `origin/feature/f314-findings-paydown-v10`.
- `gh workflow run ci.yml --ref feature/f314-findings-paydown-v10` — to run once, immediately after
  the push, under operator amendment amend1011-manual-hosted-ci; see the reply for its output and
  the one allowed `gh run list` reading.
- No PR created, edited or merged by this session (none is ordered by this round's block; no open
  PR exists on this branch). No other `gh` command run. No `git worktree add`/`remove` run.
- One scratch directory used, `.remedy-wt/f314-r5-worker/` (created this round), holding one
  digest-verification helper (`check_digests.py`), two copy-and-verify helpers for C1 and C2
  (`copy_c1.py`, `copy_c2.py`) and the gate output file (`selection-output.txt`);
  `.remedy-wt/f314-r5/` (the reviewer's prepared tree) was only read, never written.

## Verification

Gate order per the block, run once each, after C2 and before this handoff.

1. `git status --porcelain` → empty.
   `python3 .remedy-wt/f314-r5/prep/verify.py .` →
   ```
   True	ba89c7248 single parent equal to the commit before it
   True	ba89c7248 carries a new F314 R5 Cn subject
   True	ba89c7248 insertions 126 under 500
   True	271ccac5e single parent equal to the commit before it
   True	271ccac5e carries a new F314 R5 Cn subject
   True	271ccac5e insertions 20 under 500
   True	the commits come in block order: ['C1', 'C2']
   True	on feature/f314-findings-paydown-v10
   True	C1 paths exactly [...]
   True	C1 .agent/authored/f314-r5.md equals c1-.agent__authored__f314-r5.md
   True	C1 .agent/decisions.md equals c1-.agent__decisions.md
   True	C1 .agent/live_review.md equals c1-.agent__live_review.md
   True	C1 .agent/plan.md equals c1-.agent__plan.md
   True	C2 paths exactly [...]
   True	C2 tests/orchestration/scale_harness.py equals c2-tests__orchestration__scale_harness.py
   True	C2 tests/orchestration/test_tool_sandbox.py equals c2-tests__orchestration__test_tool_sandbox.py
   absent	C3
   True	the saved block equals block.md
   ALL True
   ```

2. `python3 -m ruff check .` → exit 0, `All checks passed!`.

3. `python3 .remedy-wt/f314-r5/prep/run_selection.py . .remedy-wt/f314-r5-worker/selection-output.txt` →
   ```
   paths 90
   exit 0
   3823 passed, 2 skipped in 105.00s (0:01:44)
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
   Exit 0; no FAILED, ERROR or `process(es) behind` line. Both skips are pre-existing and unrelated
   to this round's files (one a documented quarantine, one an opt-in network smoke test) — the same
   two round 4's handback recorded.

4. `python3 -m apps.cli.main integrity check --json` →
   `{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}` — `fail_count: 0`.

5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` →
   `9`. The open set itself: `R-1246`, `R-1281`, `R-1351`, `R-1353`, `R-1421`, `R-1426`, `R-1427`,
   `R-1428`, `R-1448` — R-1427 and R-1428 stay open until the dispatched hosted run reads green in
   both columns, per DECISION F314 D7 (3).

## Authored-text proofs

- `.agent/authored/f314-r5.md`: `wc -l` 93, matching `block.md`'s 93; sha256
  `5a0887ec82323b12612e3fe7dbd93a4d650e5a306f9106fd70810f48f8d22190` on both. Byte-identical.
- `.agent/decisions.md` against `.remedy-wt/f314-r5/prep/c1-.agent__decisions.md`: sha256
  `e554411e6dce43666293cee65f963ebdfe65c7081a3fe0240b71f2ecb61107d5` on both. Byte-identical.
- `.agent/live_review.md` against `.remedy-wt/f314-r5/prep/c1-.agent__live_review.md`: sha256
  `b0bcc766e02cd6cf835716ace99633c51ec35faf549581f7b3e3bf4c21544696` on both. Byte-identical.
- `.agent/plan.md` against `.remedy-wt/f314-r5/prep/c1-.agent__plan.md`: sha256
  `8e146f72c277f5bc51e3fb9283b97a10f925d876a362a533e6293ca2c19d0f56` on both. Byte-identical.
- `tests/orchestration/scale_harness.py` against `.remedy-wt/f314-r5/prep/c2-tests__orchestration__scale_harness.py`:
  sha256 `0d7f52ec76e92a9e447f3065cf14bafe8a4961170c9d6a6c9292643f28cd9680` on both. Byte-identical.
- `tests/orchestration/test_tool_sandbox.py` against `.remedy-wt/f314-r5/prep/c2-tests__orchestration__test_tool_sandbox.py`:
  sha256 `48d188eca3b033faf9085c2171d995223cc9f8faa9724e22a1d250725ab1bbf9` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f314-r5/prep/digests.txt` was checked against its own
stated sha256 (`e7ab5cb8c587a79882434717816f7aa2b2485f9eee3e8b9a30347d1d1a3dcebe`, matched), then
every one of its ten listed entries was recomputed and matched, before any prepared file was
copied, run or read.

## Deviations & assumptions

None. C1 and C2 landed in the block's order, with no added, dropped or reordered commit; every
prepared byte was copied verbatim and proved equal by direct byte comparison before being staged;
every gate ran exactly once, after C2 and before this handoff, with no retry needed.

## For the operator, in plain sentences

This session closed out last round's review and fixed the two small things it found in the
project's own test suite: one test's helper now leaves a working author name and email inside
every throwaway repository it builds, so it still works on a computer that has none of its own
set up, such as the hosted machine that runs the checks; and one test's disk search is now told
exactly which read-only system folders to skip, so it finishes quickly even on a hosted machine
whose installed toolchain is much larger than the one this session runs on. Every required local
check came back clean, and the branch is about to be pushed. Right after that push, this session
starts one run of the checks on the hosted service and reports which run it started, without
waiting for it to finish; a later session will read its result and close out this piece of work.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Rule 2, the Open PR Gate: check for open pull requests before starting any new unrelated work.
3. Read the dispatched hosted run and book round 5's verdict in the next round's first commit.
4. T007: R-1421, the closure suite's cost per test module.

Operator questions open: 1. Open findings: 9.
