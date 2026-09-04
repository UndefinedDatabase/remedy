# Handoff — F114 Cost preview per command, round 1 (claim + plan/context set — no production code this round)

## Session

SESSION 1 of feature F114 · round 1 · rounds so far 1.

Fresh loop-session bootstrap: the branch
`feature/f114-cost-preview-per-command` was cut directly by the
reviewing session (git plumbing only, no file content authored by that
session) from `main` at pull request 234's merge commit. This is the
first delegated round of F114.

## Range

Review of `a1b5d4bb455550f082da7d6c4c80fd968d6e1a88..HEAD` (base is the
commit the branch was cut from; verified equal to `git rev-parse HEAD`
before C0a — see Verification).

## Commits

### 064c28dd F114 R1 C0a: save step block verbatim to .agent/authored/f114-r1.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r1.md` | +248/-0 | transport proof — verbatim `cp` of the supplied step block, new file |

### 8534dfa4 F114 R1 C0b: mirror step block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +236/-87 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 88f6e57f F114 R1 C1: apply PLAN1 to .agent/plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +30/-26 | whole-file replace with PLAN1 (first substantive commit, per constraint 2) |

### 3f3fc506 F114 R1 C2: apply PAIR S to STATUS.md and CONTEXT1 to .agent/context.md
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | `str.replace(FROM, TO, 1)` — F114 ledger line `[ ]` → `[~]` (claimed) |
| `.agent/context.md` | +41/-31 | whole-file replace with CONTEXT1 |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f114-cost-preview-per-command` → run after
  this handback commit (C3), pushing all five commits of the round.
- No `gh pr` command of any kind was run this round — no PR is created
  or touched this round, per the block (Bundle/Constraints make no
  mention of PR creation this round; Done-when carries no Open PR Gate
  item). PR #234 (the previous feature, F112) was not touched, per
  constraint 9.

## Verification

Preconditions, checked before C0a:

```
$ git branch --show-current
feature/f114-cost-preview-per-command
$ git rev-parse HEAD
a1b5d4bb455550f082da7d6c4c80fd968d6e1a88
$ git status --short
(empty)
$ sha256sum .remedy-wt/f114_r1_block.txt
c286ebc3ec985927a7a20018db46e9f98b35808c9e7c9514c76d3d896fca25e4  .remedy-wt/f114_r1_block.txt
$ wc -l .remedy-wt/f114_r1_block.txt; wc -c .remedy-wt/f114_r1_block.txt
248 .remedy-wt/f114_r1_block.txt
12185 .remedy-wt/f114_r1_block.txt
```
All four match the block's own stamp (248 lines, 12185 bytes, the
quoted sha256) exactly. `.agent/STOP` checked absent both before the
first commit and again before C3 (`ls`: "No such file or directory"
both times).

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r1.md .agent/last_block.md
c286ebc3ec985927a7a20018db46e9f98b35808c9e7c9514c76d3d896fca25e4  .agent/authored/f114-r1.md
c286ebc3ec985927a7a20018db46e9f98b35808c9e7c9514c76d3d896fca25e4  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE PLAN**:
```
$ cmp <PLAN1 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
42 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0, `wc -l` 42 (under 50 — PASS), both grep counts 1 — PASS.

**G3 THE STATUS PAIR**:
```
FROM count in docs/roadmap/STATUS.md, BEFORE C2: 1
FROM count AFTER C2: 0
TO count AFTER C2: 1
TO contains FROM: false
```
Exactly 1 before, matching constraint's requirement — PASS. This pair
is a rewrite; the FROM-zero-after count is the proof, per the block's
own wording.

**G4 THE CONTEXT**:
```
$ cmp <CONTEXT1 extracted from committed authored file> .agent/context.md
(no output — exit 0)
$ grep -c '^## Active Branch' .agent/context.md
1
$ grep -c '^## Steps' .agent/context.md
1
count of 'feature/' in .agent/context.md: 1
first regex match of F\d{3}: F114
'pytest' in lowercased text: True
```
`cmp` exit 0 — PASS. All readings as required.

**G5 THE SUITES** (run serially, each its own invocation):
```
$ python3 -m pytest tests/docs/ -q
295 passed in 0.46s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.39s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.60s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.96s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.48s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.30s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 21.15s
```
All seven green, all four state readers run as four (not three):
`tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
`tests/regression/test_resource_safety.py`,
`tests/orchestration/test_integrity_gate.py`. No test or production
code was edited this round, so these pass counts are the moved-count
finding the block calls for: nothing moved (295/30/515/52/21/16/42 —
the reviewer's independent base reading is the comparison point).

**G6 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain
(empty — checked immediately before C3 staged)
$ git ls-files .remedy-wt
(no output — nothing under .remedy-wt/ is ever committed)
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's Commits table above — all four cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| 064c28dd (C0a) | `.agent/authored/f114-r1.md` | 248 | 248 | yes |
| 8534dfa4 (C0b) | `.agent/last_block.md` | 236 | 236 | yes |
| 88f6e57f (C1) | `.agent/plan.md` | 30 | 30 | yes |
| 3f3fc506 (C2) | `docs/roadmap/STATUS.md` | 1 | 1 | yes |
| 3f3fc506 (C2) | `.agent/context.md` | 41 | 41 | yes |

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r1.md` | NOT stale | immutable historical stamp of this round's instructions — always accurate as a record |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 2 overwrites it |
| `.agent/plan.md` | NOT stale | reflects F114 round 1's actual current step |
| `docs/roadmap/STATUS.md` | NOT stale | F114 line now reads `[~]`, matching the claim just made this round |
| `.agent/context.md` | NOT stale | reflects F114's actual scope/assumptions/constraints for this round |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: no sentence was found made stale by this
round's edits (checked `docs/roadmap/ROADMAP.md` F114 entry, line 547 —
it describes target behavior only, carries no status claim to go
stale; `docs/README.md` and root `README.md` carry no F114 mention).
Nothing to declare under constraint 6.

## Authored-text proofs

- `.agent/authored/f114-r1.md` (copied via `cp`, never retyped) sha256
  `c286ebc3ec985927a7a20018db46e9f98b35808c9e7c9514c76d3d896fca25e4`
  at 12185 bytes, 248 lines — matches the block's own stamp exactly
  (verified before C0a and again after commit).
- `.agent/last_block.md` after C0b: same sha256 as above — confirmed
  equal (G1).
- PLAN1 extracted from the COMMITTED `.agent/authored/f114-r1.md`
  between its `<<<BEGIN PLAN1>>>` / `<<<END PLAN1>>>` markers (marker
  lines excluded, and the single newline immediately preceding the END
  marker line excluded as the line separator, not slice content, per
  constraint 3's own wording): 1881 bytes, ending `...which and why).`
  with no trailing newline (`tail -c 1 .agent/plan.md | od -An -tx1` →
  `2e`, never `0a`). `.agent/plan.md` reproduces it byte-identical
  (`cmp` exit 0).
- CONTEXT1 extracted the same way between `<<<BEGIN CONTEXT1>>>` /
  `<<<END CONTEXT1>>>`: 3480 bytes, ending `...not restate it.` with no
  trailing newline (`tail -c 1 .agent/context.md | od -An -tx1` → `2e`).
  `.agent/context.md` reproduces it byte-identical (`cmp` exit 0).
- PAIR S FROM/TO extracted the same way between their own markers: 37
  bytes each (`- [ ] F114 — Cost preview per command` /
  `- [~] F114 — Cost preview per command`); `str.replace(FROM, TO, 1)`
  applied to `docs/roadmap/STATUS.md`'s full text — FROM count 1 before,
  0 after; TO count 1 after; TO does not contain FROM.
- Extraction was done by a Python script reading delimiter indices from
  the committed file, never by hand-retyping (constraint 1).

## Deviations & assumptions

None. The bundle's commit order (C0a, C0b, C1, C2, C3) was followed
exactly; the change set touched exactly the six declared paths and
nothing else; no slice looked wrong, so nothing needed declaring under
constraint 1's "apply as written and declare" clause; `.agent/STOP` was
absent at both checkpoints; no `.py` file was shipped this round, so
the `ruff check` / `py_compile` standing constraint in CONTEXT1 does
not trigger this round (it binds a FUTURE round that ships a `.py`
file, not this one).

## Next

Round 2: extract the shared cost-arithmetic helper
(`packages/orchestration/budget_guard.py:482-484`, today inlined
inside `predict_next_task_cost`) into `packages/orchestration/token_economy.py`
as `tokens_to_cost_usd()`, with `predict_next_task_cost` refactored to
call it (no behavior change), regression-proving
`tests/orchestration/test_budget_guard.py` unchanged — per `.agent/plan.md`'s
own Next Steps. No PR exists yet and none is expected until T001
(rounds 2-3) lands.
