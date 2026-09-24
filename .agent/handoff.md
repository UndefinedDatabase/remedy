# Handback — F284 Findings paydown v3 · Round 4 (CLOSING ROUND)

## Session

SESSION 1 of feature F284 · round 4 · rounds so far 4

This round books round 3's PASS with DECISION F284 D3 (R-1008's `Owner:` line moved to F285),
rotates the finding ledger into its archive, registers F285 — Findings paydown v4 under operator
amendment amend0911-feedback rule B, flips F284's STATUS line to `[x]` with the README's accepted
count, Tier 2 Done cell and Tier 2 prose, and (after this commit) pushes and opens the pull request
into `main`. This closes F284. I had ample context remaining throughout this round; no
session-limit pressure at any point.

## Range

Review of b6bdea3b..HEAD

## Commits

### 2283e9bd0 F284 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f284-r4-block.md | +174/-0 | copy of this round's block, verbatim |
| .agent/authored/f284-r4-book.diff | +53/-0 | copy of the book.diff payload |
| .agent/authored/f284-r4-plan.md | +29/-0 | copy of the plan.md payload |
| .agent/authored/f284-r4-register.diff | +99/-0 | copy of the register.diff payload |
| .agent/authored/f284-r4-status_line.txt | +1/-0 | copy of the status_line.txt payload |
| .agent/authored/f284-r4-closure.diff | +49/-0 | copy of the closure.diff payload |
| .agent/authored/f284-r4-pr_body.md | +57/-0 | copy of the pr_body.md payload |

462 insertions by `git show --numstat` (block's 174 lines + 288 for the six payloads); matches the
block's expectation exactly; under the 500-insertion cap.

### 92d04ac74 F284 R4 C2: book round 3's PASS, carry R-1008 to F285, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +27/-0 | DECISION F284 D3 appended (book.diff) |
| .agent/live_review.md | +3/-0 | `Owner: F285 — ` line and F284 R3 `Gate:` entry appended (book.diff) |
| .agent/plan.md | +10/-10 | rewritten to the plan.md payload (round 4 closing-round scope) |

`git apply --check` on book.diff: exit 0. `git apply`: exit 0. Insertions/deletions by
`git show --numstat`: 27/0 `.agent/decisions.md`, 3/0 `.agent/live_review.md`, 10/10
`.agent/plan.md` — matches the block's expectation exactly.

### 34d631331 F284 R4 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0/-33 | rotated out by `scripts/rotate_live_review.py` |
| .agent/live_review_archive.md | +33/-0 | rotated in by `scripts/rotate_live_review.py` |

Script output (printed in full, per the block):
```
gate records moved: 9
finding pairs moved: 3 (6 records)
old ledger size: 313847 bytes
new ledger size: 286104 bytes
old archive size: 4940878 bytes
new archive size: 4968621 bytes
open findings before: 1
open findings after: 1
```
Matches the reviewer's simulated-tree reading exactly. Insertions/deletions by
`git show --numstat`: 0/33 `.agent/live_review.md`, 33/0 `.agent/live_review_archive.md` — matches
the block's expectation exactly.

### e083c633c F284 R4 C4: register F285 — Findings paydown v4 under amend0911-feedback rule B: feature file, STATUS line, pin 285, README counters
| Path | +/- | Reason |
|---|---|---|
| README.md | +2/-2 | `TOTAL_FEATURES` count and Tier 2 Done/Total cells updated to 285/38 |
| docs/roadmap/STATUS.md | +7/-0 | F285 STATUS line added under its own Tier 2 heading, Tier 5 re-opened after it |
| docs/roadmap/features/T2_F285.md | +38/-0 | new feature file, registered thin, carrying R-1008 from F284 |
| tests/docs/test_docs_consistency.py | +5/-1 | `TOTAL_FEATURES` pinned to 285 with the dated comment |

`git apply --check` on register.diff: exit 0. `git apply`: exit 0. Insertions/deletions by
`git show --numstat`: 2/2 README.md, 7/0 STATUS.md, 38/0 T2_F285.md, 5/1
test_docs_consistency.py — matches the block's expectation exactly.

### (this commit) F284 R4 C5: accept F284 in STATUS with its README pins
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| README.md | rewritten section | F284's Tier 2 accepted prose and counters (closure.diff) |
| docs/roadmap/STATUS.md | rewritten line | F284's STATUS line flipped `[~]` → `[x]` with acceptance detail (closure.diff) |
| .agent/handoff.md | rewritten | this handback |

`git apply --check` on closure.diff: exit 0. `git apply`: exit 0. Working-tree measurement before
this commit (per the block, "measured before the handback joins the commit"): 10/3 README.md, 1/1
docs/roadmap/STATUS.md — matches the block's expectation exactly (confirmed via `git diff` byte
count/sha256 against G2's C5 table below; the commit's own `git show --numstat` reading goes in the
reply per the block's own instruction, since it is measured only after this commit lands).

## External actions

- None yet inside this commit sequence. Per the block, the push and the pull-request creation
  happen AFTER C5 lands: `git push origin feature/f284-findings-paydown-v3`, then `gh pr create
  --base main --head feature/f284-findings-paydown-v3 --title "F284 — Findings paydown v3"
  --body-file .remedy-wt/f284-r4-payloads/pr_body.md`. Both real outcomes, the PR number and its
  URL, go in the reply per constraint 7 ("Your handback names no pull request number, which does
  not exist when it is written").

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory (exit 2 — absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f284-findings-paydown-v3
$ git log --oneline -1
b6bdea3bf F284 R3 C3: rewrite handoff for round 3 with the evidence and package readings
```
All BEFORE ANYTHING ELSE checks passed.

```
$ wc -l / sha256sum .remedy-wt/f284-r4/block.md
174 lines, sha256=04f4ba6ceb8674be055cd04594f789f48cd08ef207b44c746bb7e0b52af99656
```
Matches both readings given in the delegation message exactly (R-0954).

```
$ wc -lc / sha256sum over .remedy-wt/f284-r4-payloads/*
book.diff       lines=53 bytes=8866 sha256=f2a08514f6f4cac7b592f469cd335846d7cb5a6ddc8e26e3c1107ece60d1dea5
plan.md         lines=29 bytes=957  sha256=73a718b3b590420436648a5db3a3cd35c3560c68fa1da1aeddf6581e9b184c60
register.diff   lines=99 bytes=4848 sha256=23cc562a764835f56010e29d6959f0ff9779dab58d2c36d72980ffca61dc1867
status_line.txt lines=1  bytes=426  sha256=761589baa99cd8e4a8685506dcdc032abab820887ca151c358f0285819574fc0
closure.diff    lines=49 bytes=2722 sha256=7304cd9a38871b952aabf90c51afa92ffa68b591a3d96f860c7877f5b0d87ae4
pr_body.md      lines=57 bytes=3435 sha256=87018ffca2064a618f48e41af5b1eda47d2ea606a7fba223ffb7b6721642f892
```
All 6 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f284-r4-* blob, read with `git show 2283e9bd0:<path>`,
   against its source)
f284-r4-block.md        @ 2283e9bd0: match=True sha256=04f4ba6ceb8674be055cd04594f789f48cd08ef207b44c746bb7e0b52af99656
f284-r4-book.diff       @ 2283e9bd0: match=True sha256=f2a08514f6f4cac7b592f469cd335846d7cb5a6ddc8e26e3c1107ece60d1dea5
f284-r4-plan.md         @ 2283e9bd0: match=True sha256=73a718b3b590420436648a5db3a3cd35c3560c68fa1da1aeddf6581e9b184c60
f284-r4-register.diff   @ 2283e9bd0: match=True sha256=23cc562a764835f56010e29d6959f0ff9779dab58d2c36d72980ffca61dc1867
f284-r4-status_line.txt @ 2283e9bd0: match=True sha256=761589baa99cd8e4a8685506dcdc032abab820887ca151c358f0285819574fc0
f284-r4-closure.diff    @ 2283e9bd0: match=True sha256=7304cd9a38871b952aabf90c51afa92ffa68b591a3d96f860c7877f5b0d87ae4
f284-r4-pr_body.md      @ 2283e9bd0: match=True sha256=87018ffca2064a618f48e41af5b1eda47d2ea606a7fba223ffb7b6721642f892
```
All 7 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2/C3/C4's files, read with `git show <commit>:<path>`, against the block's G2 table)
C2 .agent/decisions.md:         bytes=2024746 sha256=782c10b3f412d3b37105b4260d782f349af0fde6697ef71282854df20583b53c match=True
C2 .agent/live_review.md:       bytes=313847  sha256=4c102a3956082e0355bae721353d2740f43683d905ddc8d7854fa7372bbed3a2 match=True
C2 .agent/plan.md:               bytes=957     sha256=73a718b3b590420436648a5db3a3cd35c3560c68fa1da1aeddf6581e9b184c60 match=True
C3 .agent/live_review.md:       bytes=286104  sha256=cd4468d74dd0b9033b63a2dabba574bceabfa34f58dc43316b85ff8ee960c516 match=True
C3 .agent/live_review_archive.md: bytes=4968621 sha256=12d2ed99739cbae2e8d3d69bbdb270d4e81bb9a2f4866e64cc6c2563fe4b775b match=True
C4 README.md:                    bytes=28679  sha256=1e1009a855b6c2893d8699b3fbd94489207a2f6f5e3c3b0184130a2957416817 match=True
C4 docs/roadmap/STATUS.md:       bytes=50642  sha256=b33d5c3118fba723444d1ee11dcf8be546cae4cbfc815ce5606e1e53bcdd992c match=True
C4 docs/roadmap/features/T2_F285.md: bytes=2246 sha256=107bde79ad79fa89710788007e22a6ad584dfddf31d36fa6f486acf74e9f5165 match=True
C4 tests/docs/test_docs_consistency.py: bytes=95239 sha256=66dc35c0e8a5a8343e46210ed0529bb4486c40429d4b3e272b2c6fe776216fef match=True
```
All 9 match the block's G2 table exactly.

```
$ (C5 rows, read from the working tree BEFORE the handback joins the commit, per the block)
README.md:              bytes=29228 sha256=5c871d3fbd99729a520d0ba0384c8511bd4b97f970c848bc8a1d228f6ac300f5 match=True
docs/roadmap/STATUS.md: bytes=51033 sha256=6302d2d31fe1b8c247ca3f6b08b88df7eef2b06b58400cd14634ac44a2e65708 match=True
```
Both match the block's G2 table exactly.

```
$ grep -c '^+Owner: F285 — ' / '^+Gate: F284 R3 — ' over C2's diff of .agent/live_review.md
Owner: F285 — : 1
Gate: F284 R3 — : 1
```
Both counts read 1, matching the block's stated reviewer reading (G2).

```
$ git show --name-only --format= 34d631331
.agent/live_review.md
.agent/live_review_archive.md
```
Exactly the two ledger files, matching the block's stated C3 path set (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
b6bdea3b open ids: ['R-1008']
92d04ac74 (C2) open ids: ['R-1008']
34d631331 (C3) open ids: ['R-1008']
working tree (C5) open ids: ['R-1008']
```
All four read R-1008 alone, matching the reviewer's simulation exactly (G2).

```
$ (status_line.txt content, trailing newline stripped, counted in docs/roadmap/STATUS.md)
occurrences=1
$ grep -n '^- \[~\]' docs/roadmap/STATUS.md
(no match, exit 1)
```
The status line occurs exactly once; no STATUS line begins `- [~]` (G3).

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
  tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
......                                                                   [100%]
437 passed, 1 skipped in 42.77s
REAL_EXIT=0
```
Matches the reviewer's simulated-tree reading exactly: `437 passed, 1 skipped` at real exit 0 (G4).

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks `pass`, `fail_count` 0 (G4).

```
$ python3 -m apps.cli.main integrity block .remedy-wt/f284-r4/block.md
[OK] item 1 (size): 174 lines, limit 400
[OK] item 3 (cap-bounded replacements): plan.md at 29 lines
[OK] item 10 (open set recomputed): states 1; .agent/live_review.md holds 1 open by distinct id, and the block registers 0 and resolves 0, leaving 1
[OK] item 24 (gate paths resolve): 6 paths named in the block's commands, every one resolves
[OK] item 30 (new ids searched first): the block registers no finding id
[OK] item 31 (gates before the text): the block orders no gates before a commit
[OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0
```
Every item `[OK]`, real exit code 0 (G4).

```
$ git diff --name-only b6bdea3b   (measured before this commit joins the handback)
.agent/authored/f284-r4-block.md
.agent/authored/f284-r4-book.diff
.agent/authored/f284-r4-closure.diff
.agent/authored/f284-r4-plan.md
.agent/authored/f284-r4-pr_body.md
.agent/authored/f284-r4-register.diff
.agent/authored/f284-r4-status_line.txt
.agent/decisions.md
.agent/live_review.md
.agent/live_review_archive.md
.agent/plan.md
README.md
docs/roadmap/STATUS.md
docs/roadmap/features/T2_F285.md
tests/docs/test_docs_consistency.py
```
Exactly the set constraint 3 names, minus `.agent/handoff.md` which joins with this write — matches
exactly.

G5 (per-commit `--numstat --format=` for C1 to C4) is tabled below in its own section, per the
block. G6 (tree, push, PR) runs after this commit lands and is reported in the reply, since this
commit cannot contain outcomes that happen after it.

## G5 — commit sizes (`git show --numstat --format=`, C1 to C4)

### 2283e9bd0
```
174	0	.agent/authored/f284-r4-block.md
53	0	.agent/authored/f284-r4-book.diff
49	0	.agent/authored/f284-r4-closure.diff
29	0	.agent/authored/f284-r4-plan.md
57	0	.agent/authored/f284-r4-pr_body.md
99	0	.agent/authored/f284-r4-register.diff
1	0	.agent/authored/f284-r4-status_line.txt
```
### 92d04ac74
```
27	0	.agent/decisions.md
3	0	.agent/live_review.md
10	10	.agent/plan.md
```
### 34d631331
```
0	33	.agent/live_review.md
33	0	.agent/live_review_archive.md
```
### e083c633c
```
2	2	README.md
7	0	docs/roadmap/STATUS.md
38	0	docs/roadmap/features/T2_F285.md
5	1	tests/docs/test_docs_consistency.py
```

## Authored-text proofs

All 7 authored copies under `.agent/authored/f284-r4-*` (the block copy plus the six payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show 2283e9bd0:<path>` and compared byte for byte against its source:
all 7 BYTE-IDENTICAL (G1 above). `book.diff`, `register.diff` and `closure.diff` were each applied
with `git apply` after `git apply --check` passed (exit 0 both, every time), never retyped or
edited; the resulting files were verified by byte count and sha256 against the block's G2 table —
all MATCH. `.agent/plan.md` was rewritten whole via `shutil.copyfile`'s source content, run through
a Python script (not the Write tool, so no retyping occurred), and confirmed MATCH against the
PAYLOADS table and the G2 table. `scripts/rotate_live_review.py` was run unmodified in place; its
printed output was reported verbatim and matches the reviewer's simulated-tree reading exactly.

## Deviations & assumptions

None in the commit sequence: every commit landed in the block's stated order C1, C2, C3, C4, C5,
exactly as ordered. G1 through G4 ran before this handback was written, as the block orders; G5 and
G6, and the push and pull-request creation, run after this commit lands and are reported in the
reply per constraint 7. No payload was edited, retyped or repaired. The round's tracked path set
matches constraint 3 exactly (verified above). Nothing was merged this round: no `gh pr merge`, no
checkout of `main`, no branch deletion, no force-push — per constraint 5.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 462 insertions, matches block's expectation exactly; under the 500-insertion cap |
| C2 | done | book.diff apply --check and apply both exit 0; 27/0, 3/0, 10/10 insertions, matches; D3 recorded |
| C3 | done | rotate_live_review.py output matches reviewer's simulation exactly; 0/33, 33/0 insertions, matches |
| C4 | done | register.diff apply --check and apply both exit 0; 2/2, 7/0, 38/0, 5/1 insertions, matches |
| C5 | done | closure.diff apply --check and apply both exit 0; G4 run before this handback; committing now with this handback |
| G1 | done | all 6 payload digests and 7 authored-copy comparisons matched |
| G2 | done | all 9 named file digests matched; Owner/Gate line counts 1/1; C3 path set exact; open set R-1008 at all 4 points |
| G3 | done | status line occurs exactly once; no `- [~]` line remains |
| G4 | done | 437 passed, 1 skipped at exit 0; integrity check 6/6 pass; integrity block all items [OK] at exit 0 |
| G5 | done | tabled above from `git show --numstat --format=` for C1-C4; C5's own numbers go in the reply |
| G6 | pending | runs after this commit (push, PR, `gh pr list`); reported in the reply |
| PUSH | pending | `git push origin feature/f284-findings-paydown-v3`, reported in the reply |
| PR | pending | `gh pr create` into `main`; number and URL reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the Open PR Gate, which merges this feature's
pull request in the NEXT feature's session and never in this one. Then Rule A5, the first unchecked
feature in `docs/roadmap/STATUS.md`. Open findings: 1. Operator questions open: 3.
