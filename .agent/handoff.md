# Handback — F015 Interactive plan editing · Round 9 (THE CLOSING ROUND: STATUS accepted, ledger rotated, PR opened)

## Session

SESSION 1 of feature F015 · round 9 · rounds so far 9

This is the closing round: book round 8's PASS (C2), rotate the finding
ledger into its archive (C3), flip F015's STATUS line to `[x]` with the
README's accepted count, Tier 5 Done cell and Tier 5 prose in the same
commit (C4), and open the pull request into `main`. F015 registered no
finding, so there is no ownership step, and F015 is not a findings-paydown
feature, so it registers nothing. A large majority of this session's
working-context budget remained at the point this handback was written.

## Range

Review of 2cdf826f..HEAD

## Commits

### 93047c37 F015 R9 C1: copy round 9 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r9-block.md | +177/-0 | copy of this round's block, verbatim |
| .agent/authored/f015-r9-ledger.diff | +10/-0 | copy of the ledger.diff payload |
| .agent/authored/f015-r9-plan.md | +29/-0 | copy of the plan.md payload |
| .agent/authored/f015-r9-closure.diff | +53/-0 | copy of the closure.diff payload |
| .agent/authored/f015-r9-pr_body.md | +55/-0 | copy of the pr_body.md payload |
| .agent/authored/f015-r9-status_line.txt | +1/-0 | copy of the status_line.txt payload |

Total 325 insertions, matching the block's own formula (block line count
177 plus 148 = 325) exactly; under the 500-insertion cap.

### 4a02a310 F015 R9 C2: book round 8's PASS, the package READY_FOR_REVIEW
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `Gate: F015 R8 — ` entry appended, via ledger.diff |
| .agent/plan.md | +6/-5 | rewritten to the plan.md payload |

Matches the block's expected 2/0 and 6/5 insertions exactly.

### 184ceaba F015 R9 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0/-6 | 3 closed `Gate:` records moved out |
| .agent/live_review_archive.md | +6/-0 | the same 3 records appended verbatim |

Matches the block's expected 0/6 and 6/0 insertions exactly.
`scripts/rotate_live_review.py` reported: gate records moved 3, finding
pairs moved 0 (0 records), ledger 307764 -> 301103 bytes, archive
4911927 -> 4918588 bytes, open findings 4 before and 4 after — matching
the reviewer's simulation exactly.

### (this commit) F015 R9 C4: accept F015 in STATUS with its README pins
| Path | +/- | Reason |
|---|---|---|
| README.md | +13/-2 | accepted count 96->97, Tier 5 Done 15->16, F015 one-line prose added |
| docs/roadmap/STATUS.md | +1/-1 | F015's STATUS line flipped `[~]` -> `[x]` with its full acceptance pins |
| .agent/handoff.md | rewrite | this handback |

Matches the block's expected 13/2 (README.md) and 1/1 (STATUS.md) exactly.

## External actions

- `git apply --check` then `git apply` for `ledger.diff` — real exit 0, 0.
- `git apply --check` then `git apply` for `closure.diff` — real exit 0, 0.
- `python3 scripts/rotate_live_review.py` (C3) — real exit 0.
- `git push origin feature/f015-interactive-plan-editing` after C4 runs
  after this handback is written; its real outcome is reported in the
  reply, not here, per G6.
- `gh pr create --base main --head feature/f015-interactive-plan-editing
  --title "F015 — Interactive plan editing" --body-file
  .remedy-wt/f015-r9-payloads/pr_body.md` runs after the push; its number
  and URL are reported in the reply only, per the block's own instruction
  — no pull request exists at the time this handback is written.
- No `gh pr merge`, no checkout of `main`, no branch deletion, no
  force-push, no `git stash`, no `scripts/self_use_queue.json` edit (the
  self-use track answered NONE, `.agent/selfuse_f015/result.txt`).

## Verification

G1 TRANSPORT — each of the 5 payloads' lines/bytes/sha256 measured
against the PAYLOADS table, all matched exactly:
```
ledger.diff       lines=10 bytes=5383 sha256=6951a42a52e21a23282bc0b8c7f85b338ed277749873d1a9ad24fb5657e45c06
plan.md           lines=29 bytes=1005 sha256=f54fe04928fcc3407237e5fabc2a197be7077132a0c4086333bacfe39b9cf5f9
closure.diff      lines=53 bytes=4051 sha256=4e13ffbc4d25ab7df49f7da055212ff703cc328a1473f803613202758b0b7651
pr_body.md        lines=55 bytes=3279 sha256=24afd9c200bf936244dbc82ad7f105798b54431f592c559c343bcff192e64856
status_line.txt   lines=1  bytes=398  sha256=427f92353f11dcbe18192cfbadd0d10e6318183a15f5dcb31807d904e70eeca4
```
The block file itself measured 177 lines, sha256
`8122f4cb64ce7f9a8aec343df8076e363528f4cf1087ce35ead532709a603955` — equal
to the delegation message's two readings.
Each committed `.agent/authored/f015-r9-*` blob, read with `git show
93047c37:<path>`, compared byte for byte (sha256) against its source —
all 6 matched exactly (block, ledger.diff, plan.md, closure.diff,
pr_body.md, status_line.txt): `byte_identical=True` for every one.

G2 THE BOOKING — read with `git show 4a02a310:<path>`, each equal to
the reviewer's simulation:
```
.agent/live_review.md   307764 bytes  82310ee4224bebb82538f6f905fa28711a58bb02504be67768a90c0c432524bd  MATCH
.agent/plan.md             1005 bytes  f54fe04928fcc3407237e5fabc2a197be7077132a0c4086333bacfe39b9cf5f9  MATCH
```
Count of lines C2's diff adds to `.agent/live_review.md` beginning
`Gate: F015 R8 — `: 1 — matches. `open_finding_ids`
(scripts/rotate_live_review.py) over `.agent/live_review.md`'s text: at
`2cdf826f` -> `{R-0499, R-0950, R-1008, R-1046}` (4); at `4a02a310` (C2)
-> the same 4; set difference in both directions = `{}` — matches the
reviewer's reading of 4 and 4, both differences empty.

G3 THE ROTATION — at C3, `python3 scripts/rotate_live_review.py` real
output:
```
gate records moved: 3
finding pairs moved: 0 (0 records)
old ledger size: 307764 bytes
new ledger size: 301103 bytes
old archive size: 4911927 bytes
new archive size: 4918588 bytes
open findings before: 4
open findings after: 4
```
Post-write readings:
```
.agent/live_review.md          301103 bytes  41add2d19a15af999decb086828f99332326b74ace154034aa28105a31d05803  MATCH
.agent/live_review_archive.md 4918588 bytes  b5c3f60b45df355b40d1093b68995b3d99c6d21fb5b1d1a03c5ed962cc798273  MATCH
```
C3's path set: `.agent/live_review.md` and `.agent/live_review_archive.md`
only — matches.

G4 THE CLOSURE EDITS AND THE TREE — with `closure.diff` applied, before
this handback was written:
```
docs/roadmap/STATUS.md  50105 bytes  156d7a9b3a598fca2ec2d2c68cae4ed04ff76cbb638223323564ee2bece5ce82  MATCH
README.md               27839 bytes  fd25b1849f613dc121acb1897aaffde21f8e60f625e2cdeddba304066ea20ab4  MATCH
```
Count of lines of `docs/roadmap/STATUS.md` byte-equal to the one line of
`status_line.txt`: 1 — matches, must be 1.
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
......                                                                   [100%]
437 passed, 1 skipped in 55.64s
REAL_EXIT=0
```
Matches the reviewer's dry-run reading of `437 passed, 1 skipped` at exit
0 exactly.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
```
All six checks pass, `fail_count` 0, real exit 0.
```
$ python3 -m apps.cli.main integrity block .remedy-wt/f015-r9-block.md
  [OK] item 1 (size): 177 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 29 lines
  [OK] item 10 (open set recomputed): states 4; .agent/live_review.md holds 4 open by distinct id, and the block registers 0 and resolves 0, leaving 4
  [OK] item 24 (gate paths resolve): 0 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): the block orders no gates before a commit
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0
```
Real exit 0, every item `[OK]` — matches.

G5 — reported in the reply per the block's own instruction (measured
after this handback is written, before C4 is committed).

G6 — reported in the reply per the block's own instruction (measured
after C4 is committed and pushed).

## Authored-text proofs

`f015-r9-block.md`, `f015-r9-ledger.diff`, `f015-r9-plan.md`,
`f015-r9-closure.diff`, `f015-r9-pr_body.md` and `f015-r9-status_line.txt`
copies: each read back with `git show 93047c37:<path>` and compared
against the payload table's own reading — all 6 matched byte for byte
(see G1 above). `ledger.diff` and `closure.diff` were each applied with
`git apply` (never retyped), each preceded by a real `git apply --check`
at exit 0 and followed by a real `git apply` at exit 0. `plan.md` was
copied whole with `shutil.copyfile` into `.agent/plan.md`, never
retyped, never edited. `pr_body.md` was passed unedited to `gh pr create`
via `--body-file`. `status_line.txt` was used only to prove G4's single
line-match measurement, never applied.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1, C2, C3, C4),
every gate ran in the block's stated order relative to the commits (G1
before the handback; G2 at C2; G3 at C3; G4 on the working tree before
the handback; G5 after the handback, before the C4 commit; G6 after C4
and the push), and no payload was edited, retyped, or repaired. The
closure's self-use track answered NONE (`.agent/selfuse_f015/result.txt`),
so no `scripts/self_use_queue.json` edit was made, matching the block's
own statement that none is ordered. THE ACCEPTED PACKAGE THIS CLOSURE
NAMES IS FROM ROUND 8, carried forward unchanged: package
`remedy-review-20260924-151010-READY_FOR_REVIEW.zip`, SHA-256
`920b9e1c3763632b86e97cb9724831e9c9e58378bbc71bac4532638e976da840`,
directory `/home/decodeux/Repos/remedy-history/zips`, evidence job
`f015r8e1001`, accepted head
`15aec1449745c1843ad4096e44974b8710b0756c`. No pull request number is
named here — none exists at the time this handback is written; it is
reported in the reply only, per the block's own instruction.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 325 insertions, matches block formula (177+148) exactly |
| C2 | done | live_review + plan advance, matches 2/0 and 6/5 exactly |
| C3 | done | ledger rotation, matches 0/6 and 6/0 exactly; reviewer's simulation readings matched |
| C4 | done | STATUS + README closure edits applied, matches 13/2 and 1/1 exactly |
| Pull request | pending | opens after C4's push, per the block's own instruction; number/URL in the reply only |
| G1 | done | all 5 payloads and 6 authored copies matched byte for byte |
| G2 | done | both file hashes, Gate-line count and finding-id sets matched |
| G3 | done | rotation script output and post-write ledger/archive hashes matched |
| G4 | done | STATUS/README hashes matched, status line matched once, test suite 437/1/0, integrity check 6/6, block lint 7/7 |
| G5 | pending | reported in the reply, measured after this handback and before the C4 commit |
| G6 | pending | reported in the reply, measured after C4's push and PR creation |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the Open PR Gate — the
pull request this round opens is merged by the NEXT feature's session,
never by this one. Then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`. Open findings: 4. Operator questions: 1.
