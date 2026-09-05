# Handoff — F262 List commands v2 (dates, sort, filter), round 29 (README repair landed, docs gate green, PR #236 OPEN)

## Session

SESSION 9 of feature F262 · round 29 · rounds so far 29.

Context self-assessment: this round was delegated as the FINAL round on
the branch — book round 28's FAIL, register FINDING R-0797 (the reviewer's
own README slice named `F267` inside an "Accepted" block), repair it with
ONE README pair that names no feature id, re-run the docs gate to green
and open the pull request; every ordered step landed in the ordered
sequence, `tests/docs/` reads 295 passed at the committed head, PR #236
is OPEN against `main` (not a draft, not merged, hosted `ci` check
pending at handback time), and nothing outside the declared change set
was written. Round 29 is past the 25-round / 7-session soft limit
(29 of 25; session 9 of 7) — scope report: FINISHED — T001-T003 built and
accepted at the D4 scope, evidence bundle and zip, STATUS `[x]`, README
sync, `consumed_by=F262`, the README repair and the PR; MISSING — nothing
on this branch; PROPOSAL — the reviewer merges PR #236 once its hosted
check is green and verifies `main`.

## Range

Review of `893ae3c9..22073040`. FINAL content HEAD (C2, the README
repair + `Landed:` line) is `22073040ff10c259611dee3cfb92815a796b3bd0`.
This handback (C3) follows and is not part of the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| C0a | done | copyfile route, sha256 5b57b6d2… over 18962 bytes = reviewer's stated digest |
| C0b | done | mirror byte-identical (G2) |
| C1 | done | RECORD28 then FINDING appended (that order), PLAN30 replaced; every G3/G4 expectation met |
| C2 | done | PARA pair applied once (`grep -c F267 README.md` 0) + `Landed: R-0797 —` line, ONE commit; pushed `893ae3c9..22073040` |
| push | done | `origin/feature/f262-list-commands-v2` = 22073040 after C2 |
| G5 (pre-PR) | done | 295 passed / 30 passed, both exit 0, run at the committed C2 before `gh pr create` |
| gh pr create | done | PR #236 https://github.com/UndefinedDatabase/remedy/pull/236 — base main, head feature/f262-list-commands-v2, isDraft false, state OPEN, mergedAt null |
| C3 (this handback) | done | |
| G1 HYGIENE | done | PASS — STOP absent at all three reads; porcelain 0 after C0a/C0b/C1/C2 |
| G2 TRANSPORT | done | PASS — one digest, twice (and equal to the scratch original) |
| G3 RECORD APPENDS + Landed | done | PASS — 2513219 + 2 + 4060 + 2 + 2545 = 2519828, tail equal, control rejected; Landed 1 / Done 0 |
| G4 PLAN AT C1 | done | PASS — 1375 bytes byte-equal, `wc -l` 33, headers 1/1 |
| G5 DOCS GATES | done | PASS — `tests/docs/` 295, `test_roadmap_index.py` 30 |
| G6 STATE READERS + CANARY | done | PASS — 515 / 52 / 21 / 16 / 42 |
| G7 STRUCTURE + PR | done | PASS — tree clean, prod diff-stat empty, numstat = table, integrity passed/0/pass, PR #236 read back |

## Commits

### adaa6b3e F262 R29 C0a: save round-29 block verbatim to .agent/authored/f262-r29.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r29.md` | +236/-0 | transport proof — verbatim save of the round's step block (new file) via `shutil.copyfile` from the reviewer's scratch original |

### 8788fad3 F262 R29 C0b: mirror round-29 block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +119/-158 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### a7880f5f F262 R29 C1: book RECORD28 and register FINDING R-0797 in live_review.md; replace plan.md with PLAN30
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +5/-1 | two appends in order: `\n\n` + RECORD28 (4060 bytes, round 28's FAIL-on-one-gate verdict), then `\n\n` + FINDING (2545 bytes, registers R-0797 Low) |
| `.agent/plan.md` | +12/-12 | whole-file replace with PLAN30 (first substantive commit, constraint 2) |

### 22073040 F262 R29 C2: repair README accepted block to name no feature id (R-0797); append Landed line to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `README.md` | +2/-1 | PARA pair: `the remaining nine are F267's).` → `the remaining nine belong to the follow-up feature the STATUS ledger\nregisters next).` (REWRITE, FROM occurred once) |
| `.agent/live_review.md` | +3/-1 | `\n\n` + the worker's one-line `Landed: R-0797 — …` marker (540 bytes, own words, names commit C2 of F262 R29, the pair and the 295 count) |

### (this handback commit, C3)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled per the template's self-reference exception |

## External actions

- `git push -u origin feature/f262-list-commands-v2` after C2 →
  `893ae3c9..22073040  feature/f262-list-commands-v2 -> feature/f262-list-commands-v2`,
  exit 0; `git rev-parse origin/feature/f262-list-commands-v2` →
  `22073040ff10c259611dee3cfb92815a796b3bd0`.
- `gh pr list --state open --json number --jq 'length'` before creating → `0`.
- `gh pr create --title "F262: List commands v2 (dates, sort, filter)" --base main --head feature/f262-list-commands-v2 --body-file <scratch>/f262-prbody.md`
  → `https://github.com/UndefinedDatabase/remedy/pull/236`, exit 0.
  **PR #236.** The body file is the PRBODY slice extracted by Python from
  the committed `.agent/authored/f262-r29.md` (4071 bytes), unmodified.
- `gh pr view 236 --json …` → number 236, baseRefName `main`, headRefName
  `feature/f262-list-commands-v2`, isDraft false, state OPEN, mergedAt
  null, mergeable MERGEABLE. `gh pr checks 236` → `ci  pending` (run
  33959176105) at handback time.
- No `gh pr merge` of any kind. No `git worktree` created or removed.
- Scratch files, never committed (session scratchpad, outside the repo):
  `slices29.py` (marker extractor), `f262-prbody.md` (the PRBODY slice).
- A second push follows this handback commit (C3).

## Verification

Preconditions before C0a:
```
$ git status --porcelain | wc -l        → 0
$ git rev-parse --short HEAD            → 893ae3c9
$ git branch --show-current             → feature/f262-list-commands-v2
$ ls .agent/STOP                        → No such file or directory
```

**G1 HYGIENE**:
```
ls .agent/STOP:  before C0a: absent · before C2: absent · before C3: absent
git status --porcelain | wc -l:  after C0a: 0 · after C0b: 0 · after C1: 0 · after C2: 0
```
PASS.

**G2 TRANSPORT** (route: PRIMARY `shutil.copyfile` from the scratch original; the Write-tool fallback was not needed):
```
$ sha256sum .agent/authored/f262-r29.md .agent/last_block.md
5b57b6d22c7308f07b792f267c4dfb06a6bcbf6d9cac9437a73aee3792bf3b02  .agent/authored/f262-r29.md
5b57b6d22c7308f07b792f267c4dfb06a6bcbf6d9cac9437a73aee3792bf3b02  .agent/last_block.md
$ wc -c .agent/authored/f262-r29.md   → 18962
```
One digest, twice, equal to the reviewer's stated digest — PASS.

**G3 THE RECORD APPENDS AT C1** (slices extracted from the committed block by Python):
```
RECORD28 4060 bytes  trailing newline False  internal newlines 0
FINDING  2545 bytes  trailing newline False  internal newlines 0
live_review base size before C1: 2513219  trailing newline False
expected post-C1: 2513219 + 2 + 4060 + 2 + 2545 = 2519828
post-C1 length: 2519828  match True   prefix (base) intact True
tail == b"\n\n" + RECORD28 + b"\n\n" + FINDING: True
negative control: scratch copy, byte at offset 2513321 (inside RECORD28, the first appended paragraph) XOR 0x01 → reader rejects: True
```
After C2:
```
post-C2 length: 2520370 = 2519828 + 2 + 540; file ends with b"\n\n" + the Landed line: True
$ grep -c '^Landed: R-0797' .agent/live_review.md   → 1
$ grep -c '^Done: R-0797' .agent/live_review.md     → 0
```
PASS, every figure equal to the block's expectation.

**Constraint 6 — THE OPEN SET** (`^- R-\d{4} — ` registered / `^Done: R-\d{4}` lines / open):
```
BEFORE C1:            356 / 77 / 279
AFTER  C1:            357 / 77 / 280   (FINDING registers R-0797)
AFTER  C2 Landed line: 357 / 77 / 280  (unchanged)
```
PASS.

**G4 THE PLAN AT C1**:
```
PLAN30 1375 bytes, trailing newline False;  plan.md == PLAN30: True (1375)
$ wc -l .agent/plan.md              → 33
$ grep -c '^## Goal' .agent/plan.md → 1
$ grep -c '^## Next Steps' .agent/plan.md → 1
```
PASS.

**Constraint 5 — THE PARA PAIR AT C2**:
```
FROM count in README.md before: 1     TO contains FROM: False (block: false — REWRITE confirmed)
README.md 13767 → 13821 bytes (delta 54 = len(TO) 156 − len(FROM) 102);  TO present once: 1
$ grep -c "F267" README.md          → 0
```
README.md lines 66-68 now read `sort/filter/limit behaviour wired into 15 of the 24 in-scope commands;` / `the remaining nine belong to the follow-up feature the STATUS ledger` / `registers next).` — still inside the "Accepted in Tier 2 so far:" block, naming no `F\d{3}` token.

**G5 THE DOCS GATES** (at the committed and pushed C2, before `gh pr create`; the same 295 was also measured on the working tree before the `Landed:` line was written):
```
$ python3 -m pytest tests/docs/ -q                              → 295 passed in 0.50s   exit 0
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q → 30 passed in 0.39s    exit 0
```
GREEN — the PR step was therefore taken.

**G6 THE STATE READERS AND THE CANARY** (serially):
```
$ python3 -m pytest tests/ui_server/ -q                          → 515 passed in 38.29s  exit 0
$ python3 -m pytest tests/orchestration/test_test_runner.py -q   → 52 passed in 6.30s    exit 0
$ python3 -m pytest tests/regression/test_resource_safety.py -q  → 21 passed in 11.43s   exit 0
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q → 16 passed in 0.29s   exit 0
$ python3 -m pytest tests/cli/test_golden_path.py -q             → 42 passed in 24.19s   exit 0
```
515 / 52 / 21 / 16 / 42 — PASS.

**G7 STRUCTURE AND THE PR**:
```
$ git status --porcelain | wc -l   (before C3 was staged)          → 0
$ git diff --stat 893ae3c9..22073040 -- packages/ apps/ tests/ docs/ scripts/   → (empty)
$ git show --numstat --format="" adaa6b3e   → 236 0   .agent/authored/f262-r29.md
$ git show --numstat --format="" 8788fad3   → 119 158 .agent/last_block.md
$ git show --numstat --format="" a7880f5f   → 5 1     .agent/live_review.md
                                              12 12   .agent/plan.md
$ git show --numstat --format="" 22073040   → 3 1     .agent/live_review.md
                                              2 1     README.md
$ git rev-list --parents 893ae3c9..22073040 → 4 commits, each 1 parent; largest insertion count 236
$ git diff --shortstat 893ae3c9..22073040   → 5 files changed, 376 insertions(+), 172 deletions(-)
$ python3 -m apps.cli.grouped integrity check --json
  passed: true, fail_count: 0, check_count: 5, checks[high_blockers_open].status: pass ("no open blocker/high findings")   exit 0
$ gh pr view 236 --json number,url,baseRefName,headRefName,isDraft,state,mergedAt
  {"baseRefName":"main","headRefName":"feature/f262-list-commands-v2","isDraft":false,"mergedAt":null,"number":236,"state":"OPEN","url":"https://github.com/UndefinedDatabase/remedy/pull/236"}
push: 893ae3c9..22073040 exit 0; origin head == local head (22073040ff10c259611dee3cfb92815a796b3bd0)
```
Every numstat cell matches the Commits table above; no stray path; STATUS.md and scripts/self_use_queue.json untouched (constraint 7). PASS.

## Authored-text proofs

- `.agent/authored/f262-r29.md` written by `shutil.copyfile` from the
  reviewer's scratch original; sha256
  `5b57b6d22c7308f07b792f267c4dfb06a6bcbf6d9cac9437a73aee3792bf3b02`,
  18962 bytes, equal to the reviewer's stated digest and to
  `.agent/last_block.md` after C0b (G2).
- Every slice (RECORD28, FINDING, PLAN30, PARA_FROM, PARA_TO, PRBODY)
  was extracted by Python (`slices29.py`) from the COMMITTED
  `.agent/authored/f262-r29.md` as the exact bytes between
  `<<<BEGIN X>>>\n` and `\n<<<END X>>>`, each marker asserted to occur
  once — never retyped (constraint 1). RECORD28 / FINDING / PLAN30 carry
  no trailing newline (constraint 3).
- RECORD28 and FINDING: the post-C1 tail of `.agent/live_review.md`
  equals `\n\n` + RECORD28 + `\n\n` + FINDING (G3).
- PLAN30: `.agent/plan.md` == PLAN30 byte for byte, 1375 bytes (G4).
- PARA_TO occurs in README.md exactly once; PARA_FROM zero times.
- PRBODY: 4071 bytes written to the scratch body file and passed to
  `gh pr create --body-file` unmodified; PR #236's body is that slice.
- The `Landed: R-0797 — ` line is the worker's own words (the block
  ordered it so), not a reviewer slice.

## Deviations & assumptions

1. **The `Landed:` line names the repairing commit by LABEL, not by short
   sha.** The block orders the line to name "the repairing commit's short
   sha" while also ordering the line INTO that same commit (C2, "ONE
   commit for both edits"); a commit cannot embed its own sha. The line
   therefore reads "applied in commit C2 of F262 R29 — the commit
   carrying this line, whose short sha the round-29 handback names" —
   that sha is `22073040`. Prior `Landed:` lines in the ledger use the
   same by-label form (e.g. R-0787 "commit C3 of F110 R11").
2. **Sandbox forms used without refusal** (reported per constraint 7):
   `$( )` inside compounds for the porcelain counts and the `gh pr list
   … | length` read; one shell `for` loop over the four SHAs for `git
   show --numstat`; `${PIPESTATUS[0]}` for pytest exit codes after
   `| tail`. No `cd` was issued this round; every path was absolute or
   repo-relative from the fixed working directory. `cp`/`cmp` were
   pre-emptively re-expressed in Python (`shutil.copyfile`, `bytes`
   equality / `endswith`), so no refusal to report. Commit messages went
   through `git commit -q -F -` with a quoted heredoc.
3. **Integrity-check field shape.** The block names
   `passed / fail_count / high_blockers_open`; the JSON exposes the third
   as an entry of the `checks` array (`name: high_blockers_open, status:
   pass`), not a top-level key — reported from there.
4. **Bundle order followed exactly**: C0a, C0b, C1, C2, push, G5, `gh pr
   create`, C3. No extra, dropped or reordered commit. G6 and the G7
   structure reads were run after `gh pr create` (the block gates only
   G5 on the PR step). The hosted `ci` check on PR #236 was still
   `pending` when this handback was written; it was not waited on, since
   the block hands the checks to the reviewer.

No path outside the declared change set was written under version
control. `packages/`, `apps/`, `tests/`, `docs/`, `scripts/` untouched
(G7 diff-stat empty). `.agent/STOP` absent at all three reads.

## Next

The reviewer reads the PR's hosted checks and merges under the
operator's 2026-09-05 authorization; F262 is closed on this branch;
R-0797's `Done:` is booked by the next feature's first round.
