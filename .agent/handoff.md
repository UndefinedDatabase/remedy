# Handoff — F112 Prompt budget per task class, round 1 (claim)

## Session

SESSION 1 of feature F112 · round 1 · rounds so far 1.

This is F112's first round. It claims F112 in the STATUS ledger and sets
`.agent/plan.md` and `.agent/context.md` for the branch, which the
reviewing session had already cut from `main` at pull request 233's merge
commit (`5c28c674`) and merged the PR itself (git plumbing only — no file
content in that action). No production code ships this round: T001
(config schema, resolver, validation, tests) is split across rounds 2 and
3 to respect the 400-line block cap
(docs/agents/planner_reviewer_prompt.md section 3 item 1).

## Range

`5c28c674..c1c31bef` (commits C0a through C2; C3 is this handback commit
itself).

## Commits

### be926e18 F112 R1 C0a: save the round 1 block verbatim to .agent/authored/f112-r1.md

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f112-r1.md` | +235/-0 | verbatim transport of this round's block, written directly by the Write tool from the prompt's literal bytes |

### da27fa9c F112 R1 C0b: mirror the committed authored file to last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +223/-100 | whole-file mirror of the committed `.agent/authored/f112-r1.md`, overwriting the prior F110 R20 block it held |

### 853914e8 F112 R1 C1: apply PLAN1 to plan.md

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +35/-20 | whole-file replacement with PLAN1, extracted programmatically from the committed authored file |

### c1c31bef F112 R1 C2: claim F112 in STATUS.md and apply CONTEXT1 to context.md

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/context.md` | +30/-29 | whole-file replacement with CONTEXT1, extracted programmatically from the committed authored file |
| `docs/roadmap/STATUS.md` | +1/-1 | PAIR S applied as `str.replace(FROM, TO, 1)`: `- [ ] F112` → `- [~] F112`, a rewrite (TO does not contain FROM) |

### C3 (this commit, self-reference)

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | (this commit) | the round 1 handback |

## External actions

- `git push` after C3 — reported below with real output, not assumed.
- No `gh pr create` or `gh pr merge` this round: PR #233 was already
  merged by the reviewing session before this round began, and this round
  creates no new PR. No worktree add/remove. `main` was never touched.

## Verification

**Pre-round HEAD check** — `git rev-parse HEAD` before C0a:
```
5c28c6741db2d9073fc75cd159d91037e0757fb0
```
Matches the block's required `5c28c674...` exactly.

**STOP check** — `.agent/STOP` was read from disk before the first commit
(did not exist) and again immediately before C3 (still did not exist):
```
no STOP file
```
(both readings)

**G1 TRANSPORT** — `sha256sum .agent/authored/f112-r1.md
.agent/last_block.md`, run after C0b:
```
8305f3fea6b57ec0ceda3bf7dce1b69d441eab4c579f8353c532484185ecee6c  /home/decodeux/Repos/remedy/.agent/authored/f112-r1.md
8305f3fea6b57ec0ceda3bf7dce1b69d441eab4c579f8353c532484185ecee6c  /home/decodeux/Repos/remedy/.agent/last_block.md
```
Identical digest on both files.

**G2 THE PLAN** — PLAN1 extracted from the committed authored file to
`.remedy-wt/PLAN1.extracted` via a Python marker-index script (never
retyped), then:
```
cmp .remedy-wt/PLAN1.extracted .agent/plan.md   -> CMP_OK (exit 0)
wc -l .agent/plan.md                            -> 48 (.agent/plan.md)
grep -c '^## Goal' .agent/plan.md               -> 1
grep -c '^## Next Steps' .agent/plan.md         -> 1
```
48 is under the required 50-line ceiling.

**G3 THE STATUS PAIR** — FROM count in `docs/roadmap/STATUS.md` measured
BEFORE C2 (`- [ ] F112 — Prompt budget per task class`, matched by exact
Python string containment against the extracted `PAIR S FROM` slice):
```
FROM count before: 1
```
After C2 (Python string counts on the post-edit file):
```
FROM count after: 0
TO count after: 1
TO contains FROM: False
```
i.e. **TO contains FROM: false** — the pair is a genuine rewrite and the
FROM-zero count after is the correctness proof.

**G4 THE CONTEXT** — CONTEXT1 extracted from the committed authored file
to `.remedy-wt/CONTEXT1.extracted`, then:
```
cmp .remedy-wt/CONTEXT1.extracted .agent/context.md   -> CMP_OK (exit 0)
grep -c '^## Active Branch' .agent/context.md         -> 1
grep -c '^## Steps' .agent/context.md                 -> 1
count of 'feature/'                                   -> 1
first regex match of F\d{3}                            -> F112
'pytest' in the lowercased text                        -> True
```

**G5 THE SUITES** — each run as its own separate invocation, serially, on
the post-C2 tree:

```
$ python3 -m pytest tests/docs/ -q
........................................................................ [ 24%]
........................................................................ [ 48%]
........................................................................ [ 73%]
........................................................................ [ 97%]
.......                                                                  [100%]
295 passed in 0.45s
```

```
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
..............................                                           [100%]
30 passed in 0.37s
```

```
$ python3 -m pytest tests/ui_server/ -q
........................................................................ [ 13%]
........................................................................ [ 27%]
........................................................................ [ 41%]
........................................................................ [ 55%]
........................................................................ [ 69%]
........................................................................ [ 83%]
........................................................................ [ 97%]
...........                                                              [100%]
515 passed in 33.21s
```

```
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
....................................................                     [100%]
52 passed in 5.75s
```

```
$ python3 -m pytest tests/regression/test_resource_safety.py -q
.....................                                                    [100%]
21 passed in 11.54s
```

```
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
................                                                         [100%]
16 passed in 0.30s
```

```
$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 20.82s
```

Pass counts: tests/docs/ **295**, test_roadmap_index.py **30**,
tests/ui_server/ **515**, test_test_runner.py **52**,
test_resource_safety.py **21**, test_integrity_gate.py **16**,
test_golden_path.py (canary) **42**. All seven suites ran as seven
separate invocations; the four state readers (`tests/ui_server/`,
`test_test_runner.py`, `test_resource_safety.py`, `test_integrity_gate.py`)
ran as four, not three. This round edited no test and no production code,
so these are the round's own MOVED-COUNT readings for the reviewer's base
diff, not asserted as unchanged by the worker.

**G6 THE TREE, THE COMMITS AND THE SWEEP** —

`git status --porcelain` immediately before C3 was staged:
```
(empty)
```

`git ls-files .remedy-wt`:
```
(empty — no output, nothing under .remedy-wt/ is ever committed)
```

Per-commit insertion counts (`git show --numstat`, `+` column only) for
C0a, C0b, C1 and C2, compared cell-by-cell against this handback's own
Commits table above:

| Commit | Path | `+` (numstat) | `+` (Commits table above) | Match |
|--------|------|---------------|---------------------------|-------|
| be926e18 (C0a) | `.agent/authored/f112-r1.md` | 235 | 235 | yes |
| da27fa9c (C0b) | `.agent/last_block.md` | 223 | 223 | yes |
| 853914e8 (C1) | `.agent/plan.md` | 35 | 35 | yes |
| c1c31bef (C2) | `.agent/context.md` | 30 | 30 | yes |
| c1c31bef (C2) | `docs/roadmap/STATUS.md` | 1 | 1 | yes |

C3's own numbers are withheld from this file per the block's instruction
— the reviewer measures them at the next gate.

**THE STALENESS SWEEP** — one entry per file this round touched:

- `.agent/authored/f112-r1.md` — new file, not stale (created this round,
  matches the block byte for byte per G1).
- `.agent/last_block.md` — not stale; mirrors the just-committed authored
  file, confirmed identical by G1.
- `.agent/plan.md` — not stale; wholly replaced with PLAN1, describes this
  round and the next two rounds accurately, confirmed by G2.
- `docs/roadmap/STATUS.md` — not stale; the single F112 line now reads
  `[~]` (in progress), matching the branch's actual state. Checked whether
  this claim ripples into README.md's derived "accepted" count or Tier 3
  "Done" cell: those counts are both derived from `[x]` (accepted) lines
  only (confirmed by `tests/orchestration/test_roadmap_index.py` and
  `tests/docs/` both passing unchanged at 30/295), and `[~]` is not `[x]`,
  so neither derived count moves. Not stale.
- `.agent/context.md` — not stale; wholly replaced with CONTEXT1, scoped
  to F112's actual branch/scope/constraints, confirmed by G4.
- `docs/roadmap/ROADMAP.md` — outside this round's change set (not
  touched); still describes F112 accurately at line 537 ("Class input caps
  with a documented...") and the dependency line at 1180 ("F118 ← F105/F112
  · ..."); neither sentence is made stale by this round's claim-only
  change, so nothing to declare here beyond noting it was checked.

## Authored-text proofs

- `.agent/authored/f112-r1.md` vs `.agent/last_block.md`: byte-identical,
  sha256
  `8305f3fea6b57ec0ceda3bf7dce1b69d441eab4c579f8353c532484185ecee6c` on
  both — confirmed disk-to-disk (G1).
- `.agent/authored/f112-r1.md` was written directly from this round's
  prompt block via the Write tool, reproduced verbatim (no retyping of
  slices — those were extracted programmatically afterward).
- PLAN1, CONTEXT1, PAIR S FROM and PAIR S TO were all extracted
  programmatically from the COMMITTED `.agent/authored/f112-r1.md` by
  `<<<BEGIN name>>>` / `<<<END name>>>` marker index (never retyped, never
  taken directly from the prompt text), via
  `/home/decodeux/Repos/remedy/.remedy-wt/extract_slices.py`.
- PLAN1 vs the extracted-then-written `.agent/plan.md`: `cmp` exit 0 (G2).
- CONTEXT1 vs the extracted-then-written `.agent/context.md`: `cmp` exit 0
  (G4).
- PAIR S: FROM occurred exactly once in `docs/roadmap/STATUS.md` before
  the edit, zero times after; TO occurs exactly once after; TO does not
  contain FROM (G3).
- Both PLAN1 and CONTEXT1, as extracted, end WITH a trailing newline
  (`repr()` tails confirmed `...not absorbed.\n` and `...does not restate
  it.\n` respectively before writing), and the written `.agent/plan.md`
  and `.agent/context.md` match byte-for-byte per the `cmp` results above,
  so they carry the same trailing newline. Constraint 3 satisfied.

## Deviations & assumptions

- None from the ordered commit sequence: C0a, C0b, C1, C2 ran exactly in
  the bundle's declared order, followed by C3 (this handback).
- Scratch files were created under `.remedy-wt/` (gitignored, confirmed by
  `git check-ignore -v`) to perform marker extraction:
  `extract_slices.py`, `PLAN1.extracted`, `CONTEXT1.extracted`,
  `PAIR_S_FROM.extracted`, `PAIR_S_TO.extracted`. These were left in place
  rather than deleted — `.remedy-wt/` already holds a large number of
  scratch artifacts from prior sessions, and per the standing "never
  delete by glob" convention, this round did not sweep or remove any of
  it; `git ls-files .remedy-wt` confirms none of it is ever tracked
  regardless (G6).
- No `.py` file shipped this round (production code is deferred to rounds
  2–3), so the `ruff check` / `py_compile` gate CONTEXT1 documents as
  standing policy for a round that ships a `.py` file does not apply here
  and was not run.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Pre-round HEAD check (`5c28c674...`) | done | |
| STOP check before first commit | done | did not exist |
| C0a (save block verbatim) | done | |
| C0b (mirror to last_block) | done | |
| C1 (PLAN1 → plan.md, first substantive commit) | done | |
| C2 (PAIR S → STATUS.md, CONTEXT1 → context.md, one commit) | done | |
| STOP check before C3 | done | did not exist |
| C3 (handback) | done | this document |
| G1 transport (sha256 match) | done | |
| G2 the plan (cmp, line count, headings) | done | 48 lines |
| G3 the STATUS pair (FROM 1→0, TO 0→1, no containment) | done | |
| G4 the context (cmp, headings, counts) | done | |
| G5 the suites (seven invocations) | done | 295/30/515/52/21/16/42 |
| G6 the tree, the commits and the sweep | done | porcelain empty, no `.remedy-wt` tracked, numstat matched |
| Push | done | see below — real output |

## Next

Open findings: unchanged this round — F112's claim-only round registers
no new finding and resolves none; this round is not gated against
`.agent/live_review.md`'s ledger counts (that state file is untouched by
this round's change set).

Next expected action: the reviewing session verifies this round's gates
independently, then delegates round 2 — the config schema
(`prompt_budget.task_class_caps` + `prompt_budget.default_cap`) and the
new module `packages/orchestration/prompt_budget.py`
(`resolve_task_class_cap`, `validate_prompt_budget_config`) — per
`.agent/plan.md`'s Next Steps.

SESSION 1 spent this round (round 1, claim) and ends here with this
handback.
