# Handoff — F107 Context compiler v2, round R19

Branch: feature/f107-context-compiler-v2 (base 6e1970c4, R18 reviewed PASS).
Fortschritt: ~96 % (T001-T004 ✅ · Integration Gate ✅ · Built State ✅ · R19 im Review · Closure offen) — Schätzung

Deviations, declared: this handoff is 119 lines, over the 60-line cap, per
AGENTS.md DECISION D15. Cause: the mandated content — the C1-C6 SHA list, the
changed-files table, the item-status table and the TEN gate results A-J with
their real output — does not fit in 60. No section is dropped.

## Commits (all pushed, one push per commit)
| Item | SHA      | Subject                                                        |
|------|----------|----------------------------------------------------------------|
| C1   | d5d5e0ea | chore(f107): save the R19 step block verbatim                   |
| C2   | ce3dc135 | chore(f107): mirror the R19 block into last block               |
| C3   | 64bd8565 | chore(f107): record the R18 gate, R-0293, R-0294 and two resolutions |
| C4   | 4afc990d | fix(f107): record an unparseable omission on the budget demotion path |
| C5   | 09270e86 | docs(f107): record the built state of the context compiler      |
| C6   | (this)   | chore(f107): rewrite the plan and handoff for R19               |

## Changed files (6e1970c4..HEAD), `git show --numstat` per commit
| Path                                         | Commit | +   | -   |
|----------------------------------------------|--------|-----|-----|
| .agent/authored/f107-r19-1.md                | C1     | 379 | 0   |
| .agent/last_block.md                         | C2     | 293 | 321 |
| .agent/live_review.md                        | C3     | 96  | 1   |
| packages/orchestration/context_compiler.py   | C4     | 14  | 2   |
| tests/orchestration/test_context_compiler.py | C4     | 28  | 0   |
| docs/roadmap/features/T2_F107.md             | C5     | 67  | 0   |
| .agent/plan.md                               | C6     | see C6 diff |
| .agent/handoff.md                            | C6     | see C6 diff |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C1   | done   |        |
| C2   | done   |        |
| C3   | done   |        |
| C4   | done   |        |
| C5   | done   |        |
| C6   | done   |        |

## Gates — real results
A transport: `cmp .remedy-wt/f107-r19-1.block.md .agent/authored/f107-r19-1.md`
  no output, exit 0. `wc -l` = 379. `sha256sum` =
  1e39713c2a45f080fc0b36e24b9c76e279cbe15f2088cef638e4b1d75bc289ad, identical
  for the scratch original. `cmp .agent/authored/f107-r19-1.md
  .agent/last_block.md` no output, exit 0.
B block cap: GREEN. 379 lines against the cap of 400 (DECISION F105 D5).
C pairs, in .agent/live_review.md after C3 (64bd8565) — all nine counts hit:
  `^> Branch:.*Next free ID: R-0293` 0 · `...R-0295` 1 · `^- R-0293` 1 ·
  `^- R-0294` 1 · `^Done: R-0291` 1 · `^Done: R-0292` 1 ·
  `Reviewer gate on R18` 1 · `^Done:` 12 · `^Landed:` 0.
  `git show --numstat 64bd8565 -- .agent/live_review.md` = `96 1`.
  Shapes: PAIR_HDR is the one REWRITE — its FROM is 0x and its TO 1x in the
  file. PAIR_LRF, PAIR_LRG and PAIR_DONE are APPEND-shaped and proved as such:
  each FROM line still occurs exactly 1x in the file, and their 35 + 35 + 25
  TO-only lines each occur exactly 1x among the 96 lines C3's own diff adds.
  35+35+25+1 header = 96. Added lines belonging to no TO body = 0.
  One qualifier, stated: 2 of PAIR_DONE's 25 TO-only lines are BLANK and so
  occur more than once among the 96 added lines — the R-0253 blank-line
  counting exception this file already records at the R10 gate. Every
  non-blank TO-only line is exactly 1x.
D built state: `grep -c '^## Built State' docs/roadmap/features/T2_F107.md` = 1.
  `git show --numstat 09270e86 -- docs/roadmap/features/T2_F107.md` = `67 0` —
  zero deletions. The previous last line,
  `tests/orchestration/test_context_compiler.py.`, is still 1x.
E marker leak: `grep -c '^<<<'` = 0 in .agent/live_review.md, .agent/plan.md,
  .agent/handoff.md, docs/roadmap/features/T2_F107.md,
  packages/orchestration/context_compiler.py and
  tests/orchestration/test_context_compiler.py. Declared: this session's shell
  refuses compound commands, so the grep exit code could not be printed beside
  each count; the counts themselves are the six zeros above.
F scoped suites (all exit 0):
  tests/orchestration/test_context_compiler.py     -> 65 passed in 0.17s
  tests/orchestration/test_context_compiler_e2e.py -> 6 passed in 0.28s
  tests/cli/test_job_context_cmd.py                -> 9 passed in 2.74s
  tests/docs/                                      -> 294 passed in 0.25s
  test_context_compiler.py count: 64 before -> 65 after (+1, as specified).
G red-proof, in the disposable worktree `.remedy-wt/r19redproof` at HEAD
  (09270e86) and nowhere else: reverting ONLY the C4 phase-A
  `if signatures.parse_failed:` append (`git diff --numstat` = `0 9`, one file)
  turns the new test RED — exit 1, `1 failed, 64 deselected`, failing on
  `AssertionError: assert [('budget', 'signatures')] == [('budget',
  '...'signatures')] / Right contains one more item: ('unparseable',
  'signatures')`. The test bites the line it names. Worktree removed and
  pruned; afterwards `git worktree list` =
  `/home/decodeux/Repos/remedy  09270e86 [feature/f107-context-compiler-v2]`
  alone and `git status --porcelain` is empty.
H canary: `python3 -m pytest tests/cli/test_golden_path.py -q` -> 42 passed in
  19.63s, exit 0.
I lint: `python3 -m ruff check packages/orchestration/context_compiler.py
  tests/orchestration/test_context_compiler.py` -> "All checks passed!", exit 0.
J tree, push and scope: `git status --porcelain` empty · `git worktree list` the
  primary checkout alone · `git rev-list --left-right --count
  origin/feature/f107-context-compiler-v2...HEAD` = `0 0` after the last push ·
  `git diff --name-only 6e1970c4..HEAD` = exactly the eight paths the Change
  line names · insertions per commit 379, 293, 96, 42 and the C6 pair, each far
  under 500 · `gh pr list --state open` returns an empty list.
  Phase 0 probe, with a declared substitution: this session's shell REFUSES the
  bare `remedy` command, so both were run through the same entry point the R17
  gate used, `python3 -m apps.cli.grouped`.
  `plan status` -> `Active: F107 — Context compiler v2  [in_progress]` · File
  docs/roadmap/features/T2_F107.md · Milestone M3 · Blockers: F105 [done] ·
  `Next unchecked: F111 — Diff-only repair` · `Roadmap: 255 features · 255
  scheduled in STATUS` · `Consistency: no findings` · Mirror .data/roadmap/index.json.
  `plan next` -> `F107 — Context compiler v2` · File
  docs/roadmap/features/T2_F107.md · `State: in progress (Rule A5: the active
  line) · docs/roadmap/STATUS.md:60` · `Proposal only — nothing was started.`

## Findings
Registered `^- R-0` = 32; resolved `^Done: R-0` = 12; derived open = 20. This
round registered R-0293 and R-0294 and resolved R-0291 and R-0292, so the open
count is unchanged at 20. Next free ID: R-0295.

## Next expected action
Reviewer gate on R19, then R20 closure per
docs/roadmap/STATUS_closure_protocol.md, verdict PASS_WITH_RISKS for the five
pre-existing R-0286 `[reviewer]` failures. No gate is RED this round.
