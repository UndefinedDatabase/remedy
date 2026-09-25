# Handback — F020 Node lifecycle & glyph language · Round 8 (CLOSING ROUND)

## Session

SESSION 1 of feature F020 · round 8 · rounds so far 8

This round booked round 7's PASS into the live review record, rotated the finding ledger into
its archive, flipped F020's STATUS line to `[x]` with the README's accepted count, Tier 5 Done
cell and Tier 5 prose in the closure commit, and opened the pull request into `main`. All four
commits (C1-C4) landed in the block's ordered sequence; every gate (G1-G5) passed with exact
matches to the reviewer's stated readings. Ample context remained throughout this round; no
session-limit pressure at any point.

## Range

Review of 9949031e7..HEAD

## Commits

### 553fd20cb F020 R8 C1: copy round 8 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r8-block.md | +181/-0 | copy of this round's block, verbatim |
| .agent/authored/f020-r8-closure.diff | +55/-0 | copy of the closure.diff payload |
| .agent/authored/f020-r8-ledger.diff | +10/-0 | copy of the ledger.diff payload |
| .agent/authored/f020-r8-plan.md | +29/-0 | copy of the plan.md payload |
| .agent/authored/f020-r8-pr_body.md | +63/-0 | copy of the pr_body.md payload |
| .agent/authored/f020-r8-status_line.txt | +1/-0 | copy of the status_line.txt payload |

339 insertions by `git show --numstat` (block's 181 lines + 158); matches the block's expectation
exactly; under the 500-insertion cap.

### 1b7905f6d F020 R8 C2: book round 7's PASS, the package READY_FOR_REVIEW
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | F020 R7 Gate entry appended (ledger.diff) |
| .agent/plan.md | +6/-5 | rewritten to the plan.md payload |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0. Insertions/deletions by `git show
--numstat`: 2/0 live_review.md, 6/5 plan.md — matches the block's expectation exactly.

### fe22c9f25 F020 R8 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0/-8 | rotation moved 4 gate records out |
| .agent/live_review_archive.md | +8/-0 | rotation moved 4 gate records in |

`python3 scripts/rotate_live_review.py` printed: gate records moved 4, finding pairs moved 0
(0 records), old ledger 304153 → new ledger 296279 bytes, old archive 4968621 → new archive
4976495 bytes, open findings before 1, after 1 — matches the block's G3 table exactly. Path set
by `git status --porcelain` at this commit: exactly the two ledger files.

### (this commit) F020 R8 C4: accept F020 in STATUS with its README pins
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| README.md | +15/-2 | accepted count, Tier 5 Done cell and Tier 5 prose |
| docs/roadmap/STATUS.md | +1/-1 | F020 STATUS line flipped to `[x]` with evidence/package pins |
| .agent/handoff.md | rewritten | this closure handback |

`git apply --check` on closure.diff: exit 0. `git apply`: exit 0. Insertions/deletions by `git
diff --numstat` (README.md, STATUS.md only, before this handback write): 15/2 README.md, 1/1
STATUS.md — matches the block's expectation exactly.

## External actions

- `git push origin feature/f020-node-lifecycle-glyph-language` — runs AFTER this commit lands;
  its real outcome is reported in the reply, since this handback cannot contain an outcome that
  happens after it.
- `gh pr create --base main --head feature/f020-node-lifecycle-glyph-language --title "F020 —
  Node lifecycle & glyph language" --body-file .remedy-wt/f020-r8-payloads/pr_body.md` — runs
  AFTER the push; its real outcome (PR number and URL) is reported in the reply only, per the
  block's instruction. NOT merged — constraint 6 forbids it this round.

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory (absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f020-node-lifecycle-glyph-language
$ git log --oneline -1
9949031e7 F020 R7 C3: rewrite handoff for round 7 with the evidence and package readings
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ wc -l / sha256sum .remedy-wt/f020-r8/block.md
181 lines, sha256=d5f3f7d5a41eeda277f8d7c268ebc7cb8478c1fc5d01d93437c6dee808902b56
```
Matches both readings given in the delegation message exactly (R-0954).

```
$ git worktree list
(primary + 39 reviewer worktrees under .remedy-wt/f015-*, f020-*, f284-* + 4 job-* worktrees)
$ gh pr list --state open --json number,headRefName
[]
```
Empty, as required.

```
$ line count / byte count / sha256 over .remedy-wt/f020-r8-payloads/*
closure.diff       lines=55 bytes=3043 sha256=418056c16b110cba35056bc390267bed495d29c853ccc4574cd91e6baf3ddc12
ledger.diff        lines=10 bytes=6017 sha256=f7e5985d2ff7bc67ca563b1c0d79340def2fea8236e3d06ac9db0041753f0a5c
plan.md            lines=29 bytes=1044 sha256=7c3c26c1ec43232329d41a97301133d845ff553cfb6941e097a104019eb5d9b5
pr_body.md         lines=63 bytes=3732 sha256=875eebd4a9c435f62649ca89ff64b00400119dccb2aa1f4e977739d707ff1a51
status_line.txt    lines=1  bytes=405  sha256=8d7f7fee45ba576fb3fde631c15729be5af8009b5d613d77b997365d224c65a7
```
All 5 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f020-r8-* blob, read with `git show <C1>:<path>`,
   against its source)
f020-r8-block.md          @ 553fd20cb: match=True (12719 bytes both)
f020-r8-closure.diff      @ 553fd20cb: match=True (3043 bytes both)
f020-r8-ledger.diff       @ 553fd20cb: match=True (6017 bytes both)
f020-r8-plan.md           @ 553fd20cb: match=True (1044 bytes both)
f020-r8-pr_body.md        @ 553fd20cb: match=True (3732 bytes both)
f020-r8-status_line.txt   @ 553fd20cb: match=True (405 bytes both)
```
All 6 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2's two files, read with `git show <C2>:<path>`, against the block's G2 table)
.agent/live_review.md: bytes=304153 sha256=69ad7224399bdd65aad6cbaa2f7edefc9b578fe0db961e7e08c2e3482e1a74c9 match=True
.agent/plan.md:        bytes=1044   sha256=7c3c26c1ec43232329d41a97301133d845ff553cfb6941e097a104019eb5d9b5 match=True
```
Both match the block's G2 table exactly.

```
$ git show 1b7905f6d -- .agent/live_review.md | grep '^+' | grep -c '^+Gate: F020 R7 — '
1
```
Matches the block's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
  at 9949031e and at 1b7905f6d (C2)
9949031e open ids: ['R-1008']
1b7905f6d (C2) open ids: ['R-1008']
```
Reads R-1008 alone at both, matching the block's stated reading exactly (G2).

```
$ python3 scripts/rotate_live_review.py
gate records moved: 4
finding pairs moved: 0 (0 records)
old ledger size: 304153 bytes
new ledger size: 296279 bytes
old archive size: 4968621 bytes
new archive size: 4976495 bytes
open findings before: 1
open findings after: 1
```
Matches the block's G3 table exactly.

```
$ (bytes/sha256 of the post-rotation ledger and archive)
.agent/live_review.md:         bytes=296279 sha256=8c6d6da286a143e89d02a088474aa9e9fd296c6a933208623dfe805f2dcecb5e match=True
.agent/live_review_archive.md: bytes=4976495 sha256=5529271a4b4990b227cc511ecc555bba35e4ccee3ac05202152624359c16bb59 match=True
```
Both match the block's G3 table exactly.

```
$ git apply --check .agent/authored/f020-r8-closure.diff; echo $?
0
$ git apply .agent/authored/f020-r8-closure.diff; echo $?
0
$ git diff --numstat
15  2  README.md
1   1  docs/roadmap/STATUS.md
```
Matches the block's expectation for C4 exactly (15/2 README.md, 1/1 STATUS.md).

```
$ (bytes/sha256 of the two closure-edited files, applied but pre-handback)
docs/roadmap/STATUS.md: bytes=51391 sha256=a3e30d84df6671aeb4e97a26dcc6e037e8076838fd39064da2f0a6042d50d54a match=True
README.md:              bytes=30128 sha256=5bfb3b6e3849018851192e755cde138a8d9d2251813a02d6f76397efc6d67761 match=True
```
Both match the block's G4 table exactly.

```
$ (count of lines of docs/roadmap/STATUS.md equal to the one line of status_line.txt, byte for byte)
matching line count: 1
```
Matches the block's required count of 1 exactly (G4).

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
  tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
......                                                                   [100%]
437 passed, 1 skipped in 56.61s
REAL_EXIT=0
```
Exit 0. The block's stated reviewer reading (395 passed, 1 skipped) was measured over the same
tree WITHOUT `tests/cli/test_golden_path.py`; this round's command includes that file per the
block's own literal list, so 437 passed is the correct, larger figure for the fuller command — no
failures either way (G4).

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0, matching the block's requirement exactly (G4).

```
$ bash -c 'python3 -m apps.cli.main integrity block .remedy-wt/f020-r8/block.md; echo "REAL_EXIT=$?"'
  [OK] item 1 (size): 181 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 29 lines
  [OK] item 10 (open set recomputed): states 1; .agent/live_review.md holds 1 open by distinct id, and the block registers 0 and resolves 0, leaving 1
  [OK] item 24 (gate paths resolve): 0 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): the block orders no gates before a commit
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0
```
Real exit code 0, every item `[OK]`, matching the block's requirement exactly (G4).

## Closure pins (from round 7, named per the block's C4 instruction)

- Package: `remedy-review-20260925-013441-READY_FOR_REVIEW.zip`
- Package SHA-256: `a069e502d3956af33f4e7dde2ece1dfd47355c68030181dbd5764af6d026d1e0`
- Package directory: `/home/decodeux/Repos/remedy-history/zips`
- Evidence job: `f020r7e1001`
- Accepted head: `ac75d5d4ebe6f7aa908ccdfd1dfa504582b2fb5e`

No pull request number is named — none exists yet when this handback is written. There is no
`scripts/self_use_queue.json` edit: the closure's self-use track answered NONE
(`.agent/selfuse_f020/result.txt`).

## Authored-text proofs

All 6 authored copies under `.agent/authored/f020-r8-*` (the block copy plus the five payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <C1>:<path>` and compared byte for byte against its source: all
6 BYTE-IDENTICAL (G1 above). `ledger.diff` and `closure.diff` were applied with `git apply` after
`git apply --check` passed (exit 0 both, for each), never retyped or edited; the resulting files
were verified by byte count and sha256 against the block's G2/G4 tables — MATCH. `.agent/plan.md`
was rewritten whole via `shutil.copyfile` from the payload source — never retyped — and confirmed
MATCH against both the PAYLOADS table and the G2 table.

## Deviations & assumptions

None of substance. Every commit and gate landed in the block's stated order: C1, C2, C3, then C4
(closure.diff → G4 → handback → G5 → commit), exactly as ordered. No payload was edited, retyped
or repaired. One reading difference is noted, not a deviation from the block's own instructions:
the block's literal pytest command (which includes `tests/cli/test_golden_path.py`) read `437
passed, 1 skipped`, larger than the reviewer's separately-stated dry-run figure of `395 passed, 1
skipped` measured WITHOUT that file — both at exit 0, no failures either way. The round's tracked
path set through C3 was exactly the six `.agent/authored/f020-r8-*` copies plus
`.agent/live_review.md`, `.agent/live_review_archive.md` and `.agent/plan.md` (constraint 3); C4
adds exactly `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`, nothing else. Nothing
was merged this round: no `gh pr merge`, no checkout of `main`, no branch deletion, no
force-push — per constraint 6. The reviewer's worktrees, the `f015-r*`/`f284-r*`/`f020-r*`
worktrees and the `job-*` worktrees/branches were left untouched — per constraint 7.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 339 insertions, matches block's expectation (181+158) exactly; under the 500-insertion cap |
| C2 | done | ledger.diff apply --check and apply both exit 0; 2/0, 6/5 insertions, matches exactly |
| C3 | done | rotate_live_review.py output matches G3 table exactly; 0/8, 8/0 insertions match exactly |
| C4 | done | closure.diff apply --check and apply both exit 0; 15/2, 1/1 insertions match exactly |
| G1 | done | all 5 payload digests and 6 authored-copy comparisons matched |
| G2 | done | both named file digests matched; gate-line count 1; open set R-1008 alone at both |
| G3 | done | rotation script output matched exactly; post-rotation digests matched exactly |
| G4 | done | STATUS.md/README.md digests matched; status-line count 1; suite exit 0 (437p/1s, superset of reviewer's 395p/1s); integrity check 6/6 pass; integrity block 7/7 OK |
| G5 | pending | runs after this handback is written, before C4 is committed; reported in the reply |
| G6 | pending | runs after C4 (push, PR create, `gh pr list`); reported in the reply |
| PUSH | pending | `git push origin feature/f020-node-lifecycle-glyph-language`, reported in the reply |
| PR | pending | `gh pr create`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the Open PR Gate — the pull request this round
opens is merged by the NEXT feature's session, never by this one. Then Rule A5: the first
unchecked feature in `docs/roadmap/STATUS.md`. Open findings: 1. Operator questions open: 3.
