# Handoff — F262 List commands v2 (dates, sort, filter), round 1 (claim + plan/context)

## Session

SESSION 1 of feature F262 · round 1 · rounds so far 1.

This is F262's FIRST round. The branch was already cut by the reviewing
session directly from `main` at pull request 235's merge commit
(`7c65d9cc`) before this round started — no branch creation or Open PR
Gate work belonged to this round. This round claims F262 in the
STATUS.md ledger (`[ ]` → `[~]`) and sets `.agent/plan.md` and
`.agent/context.md` for the branch. No production code lands this
round; T001 (the shared listing-option surface) is round 2's work, per
the plan's own Next Steps.

## Range

Review of `7c65d9ccfb512aef1c3eea0245030647332c26ea..7ebdf78e556301ef12b0bbfe6832308ab7581fc4`.
That is C0a through C2 (the four content commits before this
handback). This handback (C3) follows and is not part of the reviewed
content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| Preconditions | done | HEAD matched, branch matched, tree clean, STOP absent |
| C0a | done | `.agent/authored/f262-r1.md` saved verbatim, cmp exit 0 |
| C0b | done | mirrored to `.agent/last_block.md`, cmp exit 0 |
| C1 | done | PLAN1 applied to `.agent/plan.md`, first substantive commit |
| C2 | done | PAIR S applied to STATUS.md + CONTEXT1 to `.agent/context.md` |
| C3 (this handback) | done | |
| G1 TRANSPORT | done | PASS — one digest, twice |
| G2 THE PLAN | done | PASS — cmp 0, 41 lines, both header counts 1 |
| G3 THE STATUS PAIR | done | PASS — FROM 1→0, TO 0→1, TO contains FROM: False |
| G4 THE CONTEXT | done | PASS — cmp 0, all readings match |
| G5 THE SUITES | done | PASS — 295/30/515/52/21/16/42, all green |
| G6 THE TREE, COMMITS, SWEEP | done | PASS — tree clean, `.remedy-wt` untracked, numstats match |

## Commits

### fd661a85 F262 R1 C0a: save step block verbatim to .agent/authored/f262-r1.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r1.md` | +242/-0 | transport proof — verbatim `cp` of the reviewer's step block (`.remedy-wt/f262-r1-block.txt`), new file |

### e261acbd F262 R1 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +221/-310 | mirror of the round's authored block via `cp` (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption from the 500-line cap) |

### 31ecf299 F262 R1 C1: apply PLAN1 to .agent/plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +29/-21 | whole-file replace with PLAN1 extracted from the committed authored file (first substantive commit, per constraint 2) |

### 7ebdf78e F262 R1 C2: claim in STATUS.md ledger, apply CONTEXT1 to .agent/context.md
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | PAIR S: `- [ ] F262 — List commands v2 (dates, sort, filter)` → `- [~] F262 — ...` via `str.replace(FROM, TO, 1)`, FROM occurred exactly once |
| `.agent/context.md` | +36/-40 | whole-file replace with CONTEXT1 extracted from the committed authored file |

### (this handback commit, C3)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

Note on numstat vs. terminal commit summary: for the three whole-file
rewrites (C0b, C1, and C2's context.md half), the `git commit` command's
own inline `insertions(+)/deletions(-)` line used git's rewrite-detection
heuristic (total old-file-lines deleted + total new-file-lines inserted
— e.g. C0b showed 242/331 there), which differs from `git show --numstat`
(a real minimal-edit diff, e.g. C0b's 221/310 used above). The gate
(G6) explicitly names `git show --numstat`, the '+' column only, as
authoritative, so that is what every number in this table and in the
G6 transcript below uses.

## External actions

- None yet at the time C3 is being written. `git push -u origin
  feature/f262-list-commands-v2` runs immediately after this commit,
  per the Bundle's C3 step — reported in the closing message, not here,
  since it happens after this file is committed. No `gh pr` command of
  any kind was run (forbidden this round: no PR, no merge, no Open PR
  Gate — the branch was already cut and PR #235 was already merged by
  the reviewer in an earlier session). No `git worktree` created or
  removed.

## Verification

Preconditions, checked before C0a:
```
$ git status --porcelain
(empty)
$ git rev-parse HEAD
7c65d9ccfb512aef1c3eea0245030647332c26ea
$ git branch --show-current
feature/f262-list-commands-v2
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
```
All four confirmed.

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r1.md .agent/last_block.md
2823aa0182b4f27f0bb10222c0658dd520b74163333114d2bab7dc280bdb7bb3  .agent/authored/f262-r1.md
2823aa0182b4f27f0bb10222c0658dd520b74163333114d2bab7dc280bdb7bb3  .agent/last_block.md
```
One digest, twice — PASS. (Also, both `cp` + `cmp` steps for C0a and
C0b independently returned exit 0 with no output, confirming
byte-identity before the hashes were even taken.)

**G2 THE PLAN**:
```
$ cmp <extracted-PLAN1-scratch-copy> .agent/plan.md
(exit 0, no output)
$ wc -l .agent/plan.md
41 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
$ tail -c 1 .agent/plan.md | od -An -tx1
 2e
```
cmp exit 0, 41 lines (under 50), both header counts 1, last byte `2e`
(`.`) not `0a` — PASS.

**G3 THE STATUS PAIR**:
```
FROM count in docs/roadmap/STATUS.md, before C2: 1
(str.replace(FROM, TO, 1) applied)
FROM count after C2: 0
TO count after C2: 1
TO contains FROM: False
```
This is a REWRITE pair; the FROM-zero count is the right proof — PASS.

**G4 THE CONTEXT**:
```
$ cmp <extracted-CONTEXT1-scratch-copy> .agent/context.md
(exit 0, no output)
$ tail -c 1 .agent/context.md | od -An -tx1
 2e
$ grep -c '^## Active Branch' .agent/context.md
1
$ grep -c '^## Steps' .agent/context.md
1
count of 'feature/' occurrences: 1
first regex match of F followed by three digits: F262
'pytest' in the lowercased text: True
```
cmp exit 0, last byte `2e` not `0a`, both header counts 1, `feature/`
count 1, first `F\d{3}` match `F262`, `pytest` present — PASS.

**G5 THE SUITES**, each its own invocation, run serially:
```
$ python3 -m pytest tests/docs/ -q
295 passed in 0.44s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.36s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.89s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.66s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.56s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.29s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.78s
```
295 / 30 / 515 / 52 / 21 / 16 / 42 — all green. This round edited no
test and no production code (only `.agent/**` state files and one line
of `docs/roadmap/STATUS.md`), so these are expected to match a clean
baseline; no count differed from what the suites report at rest, so
there is no moved-count finding to raise this round.

**G6 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain   (immediately before C3 staged)
(empty)
$ git ls-files .remedy-wt
(no output)
```
Tree clean before C3, nothing under `.remedy-wt/` tracked —
`.remedy-wt/f262-r1-block.txt` remains untracked scratch, untouched.

Per-commit numstat cross-check (the '+' column) against this
handback's own Commits table:
```
$ git show --numstat fd661a85
242  0    .agent/authored/f262-r1.md
$ git show --numstat e261acbd
221  310  .agent/last_block.md
$ git show --numstat 31ecf299
29   21   .agent/plan.md
$ git show --numstat 7ebdf78e
36   40   .agent/context.md
1    1    docs/roadmap/STATUS.md
```
Every path and every insertion count matches the Commits table exactly
(242, 221, 29, 36+1=37 total for C2).

**Staleness sweep**, one entry per file this round touched:
- `.agent/authored/f262-r1.md` — NOT stale. An immutable verbatim
  record of the round's own step block; nothing to go stale.
- `.agent/last_block.md` — NOT stale. Mirrors the current round's block
  exactly, which is the file's whole purpose.
- `.agent/plan.md` — NOT stale. Freshly written PLAN1 content
  accurately describes round 1's actual state (F262 claimed, branch
  cut, round 2 = T001 next).
- `docs/roadmap/STATUS.md` — NOT stale. The F262 line now correctly
  reads `[~]` (in progress), matching the claim just made; no other
  line was touched or made inconsistent by this edit (checked: no
  other doc references F262 as unclaimed — see below).
- `.agent/context.md` — NOT stale. Freshly written CONTEXT1 content
  matches the branch's actual scope, assumptions and constraints as of
  this round.

Constraint 6 check (a sentence OUTSIDE the change set made stale by
this round): searched `docs/**/*.md` for other `F262` mentions besides
`docs/roadmap/STATUS.md` (edited) and `docs/roadmap/features/T2_F262.md`
(pre-existing feature file, untouched, still accurate as the feature's
own detail doc) — none found. Nothing outside the declared change set
was made stale by this round.

## Authored-text proofs

- `.agent/authored/f262-r1.md` written verbatim via `cp` from
  `.remedy-wt/f262-r1-block.txt` (the reviewer's original), confirmed
  byte-identical by `cmp` (exit 0, no output) immediately after the
  copy — this is the transport proof required before building anything
  on top of it (C0a).
- `.agent/last_block.md` mirrors it via a second `cp`, likewise
  confirmed by `cmp` (exit 0) and by matching sha256 (G1).
- All four slices (PLAN1, CONTEXT1, PAIR S FROM, PAIR S TO) were
  extracted from the COMMITTED `.agent/authored/f262-r1.md` by a
  Python script reading the file in binary mode, locating each
  `<<<BEGIN ...>>>`/`<<<END ...>>>` marker pair by byte index, and
  taking the exact bytes strictly between them (marker lines excluded)
  — never by hand-retyping (constraint 1). Per constraint 3, exactly
  one trailing `\n` (the one belonging to the marker line, not the
  slice) was stripped from each of PLAN1 and CONTEXT1's extracted
  bytes, leaving both slices ending without a trailing newline.
- PLAN1: 1917 bytes, last byte `.` (0x2e). `.agent/plan.md` reproduces
  it byte-identical (G2).
- CONTEXT1: 3488 bytes, last byte `.` (0x2e). `.agent/context.md`
  reproduces it byte-identical (G4).
- PAIR S FROM: `- [ ] F262 — List commands v2 (dates, sort, filter)`
  (53 bytes, UTF-8 em-dash). PAIR S TO: the same string with `[ ]`
  replaced by `[~]`. Applied via `content.replace(FROM, TO, 1)` after
  confirming `content.count(FROM) == 1` (G3).

## Deviations & assumptions

1. **Scratch-file location**: the block's own gate descriptions
   reference "an extracted PLAN1/CONTEXT1 scratch copy" without naming
   a path. This worker's extraction script initially targeted `/tmp/`,
   which this session's sandbox denied ("may only copy files to/from
   the allowed working directories... `/home/decodeux/Repos/remedy`").
   Re-ran the identical extraction writing scratch files under the
   gitignored `.remedy-wt/` instead (`.remedy-wt/f262_plan1_scratch.bin`,
   `f262_context1_scratch.bin`, `f262_pair_from_scratch.bin`,
   `f262_pair_to_scratch.bin`) — same mechanical byte-index extraction
   script, same output bytes (verified: both runs produced identical
   byte counts and content before the `/tmp` version was ever used for
   anything). No effect on any committed file; the scratch files
   themselves stay untracked, per `git ls-files .remedy-wt` in G6.
2. **numstat vs. commit-summary discrepancy**: `git commit`'s own
   inline stat line and `git show --numstat` reported different
   insertion/deletion counts for the three whole-file-rewrite paths
   (C0b's `.agent/last_block.md`, C1's `.agent/plan.md`, and C2's
   `.agent/context.md` half) — see the note under Commits above. Not a
   defect; `git show --numstat` is what the gate (G6) names explicitly,
   and that is the value used consistently throughout this handback.
3. **Bash tool chaining restriction**: several attempted one-line
   compound commands (`cmd1 && echo "..."`, multi-statement `python3`
   heredocs piped through `sed`, etc.) were rejected by this session's
   Bash tool as "multiple operations" requiring separate approval.
   Re-expressed as single, unchained invocations (one `cp`, one `cmp`,
   one `sha256sum`, etc. per tool call) — no change to intent or
   result, only to invocation shape.

No other deviations. `.agent/STOP` was absent both times it was
checked (before C0a and immediately before C3, per constraint 6/7 of
the block). No path outside the declared change set was written under
version control: only `.agent/authored/f262-r1.md`,
`.agent/last_block.md`, `.agent/plan.md`, `docs/roadmap/STATUS.md`,
`.agent/context.md` and this handback were committed. The bundle's
commit order (C0a, C0b, C1, C2 — this handback C3) was followed
exactly, with C1 as the first substantive content commit as required.

## Next

**NEXT EXPECTED ACTION: Round 2 builds T001 — the shared listing-option
surface.** State the exact mechanical rule for "list command" over
`apps/cli/command_catalog.py` (working hypothesis: `subcommand` equal
to `list` or ending `-list`, with `checklist` as a same-suffix false
positive and `snapshot list-applies` a narrower case to classify
explicitly), wire the four flags (`--sort <field> [--desc] --since
<when> --until <when> --limit <n>`) once, and ship the coverage test
that derives the list-command set mechanically from the catalog and
fails loudly with the valid set named — per the plan's own Next Steps
and the feature file's Orchestrator brief
(`docs/roadmap/features/T2_F262.md`).
