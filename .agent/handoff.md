# Handoff — F289, round 3

## Session

SESSION 1 of feature F289 · round 3 · rounds so far 3. Context remaining at
handback: comfortable — the round closed inside a single session with no
compaction needed.

## Range

Review of `c1851178`..`HEAD` (`HEAD` is this handback's own commit, `F289 R3
C5`, on `feature/f289-self-use-sources`).

## Commits

### 08fbb7248 F289 R3 C1: copy round 3 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f289-r3-block.md | 223/0 | copy of this round's block (`shutil.copyfile`) |
| .agent/authored/f289-r3-plan.md | 28/0 | copy of the plan.md payload |
| .agent/authored/f289-r3-records.diff | 61/0 | copy of the records.diff payload |

Measured insertions: 312 (223+28+61), matching the block's expectation
(block's own line count 223 plus 89).

### ace433ea5 F289 R3 C2: book round 2, register R-1074, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 32/0 | `git apply records.diff` — appends DECISION F289 D3 |
| .agent/live_review.md | 4/0 | `git apply records.diff` — Gate: F289 R2 entry, R-1074's registration |
| .agent/plan.md | 8/10 | rewritten to the plan.md payload |
| .agent/prose_slips.md | 1/0 | `git apply records.diff` — round 2 docstring-prose slip |

Expected by the block: 32/0, 4/0, 8/10, 1/0 — measured identically.

### cbb94501a F289 R3 C3: accept a guide's link to an existing folder (R-1074)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | appended blank line + the `Landed: R-1074` line, S1 |
| packages/orchestration/doc_staleness.py | 3/1 | `_run_c04` now requires `Path.exists()` (file or folder), comment names R-1074 |
| tests/orchestration/test_doc_staleness.py | 20/0 | `TestC04GuideRelativeLinks` gains the existing-folder / missing-folder test |

No insertion count was expected by the block for C3.

### 3e6667886 F289 R3 C4: prove three consecutive self-use items on an empty ledger, the first run to completion
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f289-r3-mutations.py | 146/0 | NEW FILE — the G5 mutation tool, six mutations |
| tests/orchestration/test_self_use_runner.py | 119/0 | `TestThreeConsecutiveItemsOnAnEmptyLedger`, T003 / DECISION F289 D3 |

No insertion count was expected by the block for C4.

### .agent/handoff.md (this commit, F289 R3 C5)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f289-r3-mut 3e6667886` — for G5.
- `git worktree remove --force .remedy-wt/f289-r3-mut` then `git worktree
  prune` — G5's last action; `git worktree list` afterward showed the
  primary checkout and exactly the pre-existing worktrees (see Verification).
- `git push` — real outcome reported in Verification (G6).
- No PR created, no PR merged, no branch checkout, no force-push, no stash —
  none were ordered and none were done.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → does not exist (real exit 2, `No such file or
  directory`).
- `pwd` → `/home/decodeux/Repos/remedy`. `git status --porcelain` → empty.
  `git branch --show-current` → `feature/f289-self-use-sources`. `git log
  --oneline -1` → `c18511783 F289 R2 C6: rewrite handoff for round 2` — all
  three matched (`c1851178` per the delegation message).
- Block bytes: measured 223 lines, sha256
  `df6236a89ef13f7c38d1ff4a54814951e26a7bc6ec8df42cddbe4788b916381a` against
  `.remedy-wt/f289-r3/block.md` — both matched the delegation message.
- `git worktree list` reported as found: the primary checkout plus the
  F015/F020/F023/F024/F025/F027/F284 dry/sim worktrees, `f289-r3-dry` and
  `f289-r3-sim` (the reviewer's), and ten `job-*` worktrees — unchanged at
  the end (see G6).

PAYLOADS (measured against the table, before use):
| file | lines | bytes | sha256 match |
|---|---|---|---|
| plan.md | 28 | 983 | yes |
| records.diff | 61 | 12954 | yes |

CONSTRAINT 1 — `git apply --check .remedy-wt/f289-r3-payloads/records.diff` →
real exit 0. `git apply` (real) → real exit 0.

G1 TRANSPORT — every `.agent/authored/f289-r3-*` copy read back with `git show
08fbb7248:<path>` compared byte-for-byte against its source: all three
byte-identical (block: 16419 bytes both sides; plan.md: 983 bytes both sides;
records.diff: 12954 bytes both sides).

G2 THE BOOKKEEPING — every file's sha256 read with `git show
ace433ea5:<path>` matched the reviewer's table exactly:
| path | bytes | sha256 match |
|---|---|---|
| .agent/decisions.md | 2218696 | yes |
| .agent/live_review.md | 325378 | yes |
| .agent/prose_slips.md | 370935 | yes |
| .agent/plan.md | 983 | yes |

`open_finding_ids` (from `scripts/rotate_live_review.py`) over the ledger
TEXT: at `c1851178` → `[]`; at `ace433ea5` → `['R-1074']`. At `ace433ea5` the
ledger's last non-blank line begins `- R-1074 — ` (confirmed verbatim).

G3 THE CODE — `python3 -m ruff check packages/orchestration/doc_staleness.py
tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_runner.py`
at C4 (branch tip after C4) → `All checks passed!`, real exit 0.

`git diff -U0 ace433ea5 cbb94501a -- packages/orchestration/doc_staleness.py
.agent/live_review.md`, whole:
```
diff --git a/.agent/live_review.md b/.agent/live_review.md
index 32fe636b9..563b25379 100644
--- a/.agent/live_review.md
+++ b/.agent/live_review.md
@@ -444,0 +445,2 @@ Gate: F289 R2 — the F289 round 2 entry: the booking of round 1 with R-1073's r
+
+Landed: R-1074 — the staleness catalog's link check accepts a link to an existing folder and still reports a missing one, at this round's C3.
diff --git a/packages/orchestration/doc_staleness.py b/packages/orchestration/doc_staleness.py
index 5fbadc159..0af14c684 100644
--- a/packages/orchestration/doc_staleness.py
+++ b/packages/orchestration/doc_staleness.py
@@ -449 +449,3 @@ def _run_c04(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
-                if not resolved.is_file():
+                # R-1074: a link to an existing FOLDER is a working link, not stale —
+                # only a target that exists NEITHER as a file NOR as a folder is.
+                if not resolved.exists():
```
Changes exactly the one existence test with its comment, plus the blank line
and the one `Landed:` line — nothing else.

`run_staleness_checks()` over the real repository at C3:
1. `docs_index_guide_registration` | `docs/README.md` | claim: "the
   Quick-Find Table has no link to
   `guides/real-test-execution-snapshot-rollback-user-guide-v1.md`"
2. `config_cli_table_complete` | `docs/guides/remedy-toml-user-guide.md` |
   claim: "the CLI commands table never documents the `config` subcommand
   `show`"

Both are exactly the two claims DECISION F289 D2 names; unchanged by R-1074's
repair.

G4 THE TESTS — serial run at the branch tip (C4) of the block's selection:
```
697 passed, 1 skipped in 65.07s (0:01:05)
```
Real exit code 0 (`REAL_EXIT=0`). The one SKIPPED line:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
```
— the same D12 quarantine the reviewer's base run also skipped.

Node accounting: `--collect-only -q` on `tests/orchestration/test_doc_staleness.py`
and `tests/orchestration/test_self_use_runner.py` together — 74 tests at
`c1851178`, 76 tests at C4, a set-diff of exactly two added nodes and zero
removed:
- `test_doc_staleness.py::TestC04GuideRelativeLinks::test_a_link_to_an_existing_folder_is_not_stale_but_one_to_a_missing_folder_is`
- `test_self_use_runner.py::TestThreeConsecutiveItemsOnAnEmptyLedger::test_three_closures_the_first_run_to_completion`

Reviewer's base was 695 passed + 1 skipped; 695 + 2 = 697, matching the
measured total exactly. No other difference to account for.

`python3 -m apps.cli.main integrity check --json` → all six checks `pass`,
`fail_count` 0, `ok` true.

`git branch --list 'remedy/*'` → 195 both times: measured once after C3 (no
job-running or branch-creating operation happened between C2 and this
reading, so it stands in for "before C3" honestly — see Deviations) and once
more after G4's integrity-check reading. Equal.

G5 THE RED PROOFS — `.agent/authored/f289-r3-mutations.py`, run as
`python3 -B .agent/authored/f289-r3-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f289-r3-mut` against a worktree at
`3e6667886` (this round's C4):
```
control (before) | exit=0 failed=0 nodes=[]
m1 R-1074: _run_c04 goes back to requiring a file | exit=1 failed=1 nodes=['tests/orchestration/test_doc_staleness.py::TestC04GuideRelativeLinks::test_a_link_to_an_existing_folder_is_not_stale_but_one_to_a_missing_folder_is']
m2 R-1074: _run_c04 accepts every link whose target's parent folder exists | exit=1 failed=2 nodes=['tests/orchestration/test_doc_staleness.py::TestC04GuideRelativeLinks::test_stale', 'tests/orchestration/test_doc_staleness.py::TestC04GuideRelativeLinks::test_a_link_to_an_existing_folder_is_not_stale_but_one_to_a_missing_folder_is']
m3 _doc_staleness_tier ignores the keys the queue already targets | exit=1 failed=1 nodes=['tests/orchestration/test_self_use_runner.py::TestThreeConsecutiveItemsOnAnEmptyLedger::test_three_closures_the_first_run_to_completion']
m4 _doctor_warning_tier answers None | exit=1 failed=1 nodes=['tests/orchestration/test_self_use_runner.py::TestThreeConsecutiveItemsOnAnEmptyLedger::test_three_closures_the_first_run_to_completion']
m5 _run_c01 reads only the Guides section | exit=1 failed=2 nodes=['tests/orchestration/test_doc_staleness.py::TestC01DocsIndexGuideRegistration::test_stale', 'tests/orchestration/test_self_use_runner.py::TestThreeConsecutiveItemsOnAnEmptyLedger::test_three_closures_the_first_run_to_completion']
m6 run_next_self_use_item resolves its default max_cost_usd to 1.00 | exit=1 failed=3 nodes=['tests/orchestration/test_self_use_runner.py::TestRunNextSelfUseItem::test_it_attaches_the_small_budget', 'tests/orchestration/test_self_use_runner.py::TestTheSelfUseRoleAndItsBudget::test_the_call_cap_is_eight_and_the_cost_bound_six_dollars', 'tests/orchestration/test_self_use_runner.py::TestThreeConsecutiveItemsOnAnEmptyLedger::test_three_closures_the_first_run_to_completion']
restored byte-identical: True (packages/orchestration/doc_staleness.py)
restored byte-identical: True (packages/orchestration/self_use_generator.py)
restored byte-identical: True (packages/orchestration/self_use_runner.py)
control (after) | exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every one of the six mutations was caught with at least one failing node;
none stayed green, so no test had to be added after the fact. The worktree
was removed (`git worktree remove --force .remedy-wt/f289-r3-mut`, `git
worktree prune`); `git worktree list` afterward matched the BEFORE ANYTHING
ELSE reading exactly.

G6 TREE AND PUSH:
- `git status --porcelain` → empty (after this commit).
- `git log --oneline -n 7` → (see below, filled after commit).
- `git worktree list` → primary checkout plus exactly the worktrees
  constraint 6 names (the pre-existing F015/F020/F023/F024/F025/F027/F284/F289
  dry/sim trees and the ten `job-*` trees) — nothing else.
- `git push` → real outcome below.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` →
  reported below.

## Authored-text proofs

The block copy and the two payload copies (`plan.md`, `records.diff`),
read back at `08fbb7248`, equal the reviewer's originals byte for byte (see
G1 above). `records.diff` was applied with `git apply` unedited (constraint
1); `.agent/plan.md` was rewritten to the `plan.md` payload verbatim via
`shutil.copyfile`, confirmed byte-identical by the G2 sha256 reading.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| BEFORE ANYTHING ELSE 1–4 | done | |
| PAYLOADS verification | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | |
| Constraint 3 (tracked path set) | done | matches exactly, see below |
| Constraint 6 (worktree cleanup) | done | |
| Constraint 7 (no full suite) | done | only the named selection ran |

`git diff --name-only c1851178` at the branch tip after C5 equals exactly:
`.agent/authored/f289-r3-block.md`, `.agent/authored/f289-r3-mutations.py`,
`.agent/authored/f289-r3-plan.md`, `.agent/authored/f289-r3-records.diff`,
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/prose_slips.md`, `.agent/handoff.md`,
`packages/orchestration/doc_staleness.py`,
`tests/orchestration/test_doc_staleness.py`,
`tests/orchestration/test_self_use_runner.py` — the block's constraint-3 set
plus this handback, none of the forbidden paths touched.

## Deviations & assumptions

1. No commit needed to split this round — every commit's insertions stayed
   well under the 500-line cap (the largest was C1 at 312).
2. Constraint 6 / G4's branch-count equality ("counted before C3 and after
   G4"): this worker's first `git branch --list 'remedy/*'` reading was taken
   after C3 was already committed (195), not literally before it, because
   nothing that happens between commits changes tracked branches. No job ran
   and no branch was created between C2 and that first reading, so it stands
   in for the "before C3" count honestly, declared here rather than silently
   assumed. The after-G4 reading (also 195) matched it.
3. No document was edited to clear either of the two real staleness claims
   (S6 is unaffected by this round — T003 is a proof, not a repair); DECISION
   F289 D2 still owns that, deferred to the self-use track.
4. No test written by this round was found wrong and corrected; no reviewer
   payload was edited or retyped.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 3,
then the closure sequence's integration gate: the one full suite of F289.
Open findings: 1 (R-1074, landed and awaiting the reviewer's `Done:`).
Operator questions: 0.
