# Handback — F019 Live node materialization · Round 9 (the closing round)

## Session

SESSION 2 of feature F019 · round 9 · rounds so far 9

This round books round 8's PASS, rotates the finding ledger into its
archive, flips F019's STATUS line to `[x]` with the README's accepted
count, Tier 5 Done cell and Tier 5 prose in the same commit, and opens the
pull request into `main`. This closes F019. I had ample context remaining
throughout this round; no session-limit pressure at any point.

## Range

Review of 787759d9..HEAD

## Commits

### 76a970f1f F019 R9 C1: copy round 9 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r9-block.md | +178/-0 | copy of this round's block, verbatim |
| .agent/authored/f019-r9-ledger.diff | +10/-0 | copy of the ledger.diff payload |
| .agent/authored/f019-r9-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f019-r9-closure.diff | +54/-0 | copy of the closure.diff payload |
| .agent/authored/f019-r9-pr_body.md | +65/-0 | copy of the pr_body.md payload |
| .agent/authored/f019-r9-status_line.txt | +1/-0 | copy of the status_line.txt payload |

339 insertions by `git show --numstat` (block's 178 lines + 161); matches
the block's expectation exactly; under the 500-insertion cap.

### d3221664b F019 R9 C2: book round 8's PASS, the package READY_FOR_REVIEW
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `Gate: F019 R8 —` entry appended |
| .agent/plan.md | +6/-6 | rewritten to the plan.md payload (round 9 scope) |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0.
Insertions/deletions by `git show --numstat`: 2/0 live_review.md, 6/6
plan.md — matches the block's expectation exactly.

### 8263d1f57 F019 R9 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0/-24 | `scripts/rotate_live_review.py` moved 10 gate records and 1 finding pair out |
| .agent/live_review_archive.md | +24/-0 | the same records appended to the archive |

`python3 scripts/rotate_live_review.py` real exit 0. Printed output:
```
gate records moved: 10
finding pairs moved: 1 (2 records)
old ledger size: 324355 bytes
new ledger size: 302065 bytes
old archive size: 4918588 bytes
new archive size: 4940878 bytes
open findings before: 4
open findings after: 4
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
```
Insertions/deletions by `git show --numstat`: 0/24 live_review.md, 24/0
live_review_archive.md — matches the block's expectation exactly. Path
set: exactly the two ledger files, nothing else.

### (this commit) F019 R9 C4: accept F019 in STATUS with its README pins
Self-reference exception per the handback template (a handback cannot
table the commit that writes it).
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | F019's STATUS line flipped `[~]` → `[x]` with round 8's evidence job, package, sha256, path and accepted head |
| README.md | +14/-2 | accepted count 97→98, Tier 5 Done cell 16→17, Tier 5 F019 prose paragraph added |
| .agent/handoff.md | rewritten | this handback |

`git apply --check` on closure.diff: exit 0. `git apply`: exit 0.
Insertions/deletions by `git show --numstat` (README.md, STATUS.md only,
measured before this handback was added to the commit): 14/2 README.md,
1/1 STATUS.md — matches the block's expectation exactly.

## External actions

- No `git push` yet at the time this handback is written; the block orders
  the push after C4 is committed. Its real outcome is reported in the
  reply only, per G6.
- No `gh pr create` yet at the time this handback is written; the block
  orders it after the push. Its real outcome (number and URL) is reported
  in the reply only, per G6.
- No checkout of `main`, no branch deletion, no force-push, no `git
  stash`, no worktree add/remove this round (constraint 7 leaves every
  existing worktree alone).

## Verification

G1 TRANSPORT — all 5 payloads (ledger.diff, plan.md, closure.diff,
pr_body.md, status_line.txt) measured against the block's PAYLOADS table,
all matched (line count, byte count, sha256):
```
ledger.diff       lines=10 bytes=6871 sha256=9cec48a06f5de527e90f4bfea483e21d440a9a74f777df6ff794a9b0d8eb0ad6
plan.md           lines=31 bytes=1145 sha256=80c2b1052740038402c711e5d8fa71fc616f38dd0dcc7d6186ed14aa2bb9a51d
closure.diff      lines=54 bytes=4064 sha256=e83081a1928fdae5b2c1258d4c051f37c0db3f4436d4320e9e3930f6a17a8a49
pr_body.md        lines=65 bytes=3708 sha256=ae0e1ca738825b3d86a0ea0f32911a95d19a734e332eeb913873804d1b62e5ab
status_line.txt   lines=1  bytes=399  sha256=9c71595a139f7cfc2fa7fd5d5a04bd5545edc9a0c899efcd0002a791b2cf400b
ALL PAYLOAD DIGESTS MATCH: True
```
Each `.agent/authored/f019-r9-*` copy, read back with `git show
76a970f1f:<path>` from C1, matched its source byte for byte (6
comparisons: the block copy against `.remedy-wt/f019-r9/block.md`, plus
the 5 payload copies) — `ALL_TRANSPORT_OK: True`.

G2 THE BOOKING — at C2 (`d3221664b`), `.agent/live_review.md` read 324355
bytes, sha256
`40b7bfe950628223f8686781c475de55355f4de8434b5c55932e5cf01e8be183`
(MATCH); `.agent/plan.md` read 1145 bytes, sha256
`80c2b1052740038402c711e5d8fa71fc616f38dd0dcc7d6186ed14aa2bb9a51d`
(MATCH, equal to the plan.md payload). The count of lines C2's diff adds
to the ledger beginning `Gate: F019 R8 — ` is 1. `open_finding_ids`
(`scripts/rotate_live_review.py`) over `.agent/live_review.md`: at
`787759d9` → `['R-0499', 'R-0950', 'R-1008', 'R-1046']`; at C2
(`d3221664b`) → the same four — matches the reviewer's simulated reading
exactly at both.

G3 THE ROTATION — at C3 (`8263d1f57`): `scripts/rotate_live_review.py`
printed exactly the reviewer's simulated readings (10 gate records moved,
1 finding pair / 2 records moved, ledger 324355→302065 bytes, archive
4918588→4940878 bytes, open findings 4 before and 4 after). Resulting
`.agent/live_review.md`: 302065 bytes, sha256
`36a4838a7b111078b6ab3de8b8f7972d74ab0d7088fd95e519161f0a1ce9fd84`
(MATCH). Resulting `.agent/live_review_archive.md`: 4940878 bytes, sha256
`2dd64ce58680344f26521a9e065d7c60afe0cf0f2e476c98922d257ec6d49435`
(MATCH). C3's path set: exactly `.agent/live_review.md` and
`.agent/live_review_archive.md`, nothing else.

G4 THE CLOSURE EDITS AND THE TREE — with closure.diff applied, before
this handback was written: `docs/roadmap/STATUS.md` 50463 bytes, sha256
`72f0e4ba7a869890f68aaaf15dc67237db2b020b07360163bad931de10def118`
(MATCH); `README.md` 28679 bytes, sha256
`7619b1cdc92751479441d62b764fe6ea7f5ec863fc1887a83012cb692a4c6a9b`
(MATCH). The status_line.txt content (with its trailing newline stripped)
occurs exactly 1 time in `docs/roadmap/STATUS.md` (MATCH, must be 1).
Serially:
```
$ python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"
......                                                                   [100%]
437 passed, 1 skipped in 35.44s
REAL_EXIT=0
```
Matches the reviewer's dry run exactly (`437 passed, 1 skipped` at exit
0).
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0.
```
$ python3 -m apps.cli.main integrity block .remedy-wt/f019-r9/block.md
  [OK] item 1 (size): 178 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 31 lines
  [OK] item 10 (open set recomputed): states 4; .agent/live_review.md holds 4 open by distinct id, and the block registers 0 and resolves 0, leaving 4
  [OK] item 24 (gate paths resolve): 0 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): the block orders no gates before a commit
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0
```
Every item `[OK]`, real exit code 0.

G5 — reported in the reply per the block's own instruction (measured
after this handback is written, before C4 is committed).

G6 — reported in the reply per the block's own instruction (measured
after C4, after the push and the pull request).

## Authored-text proofs

All 6 authored copies under `.agent/authored/f019-r9-*` (the block copy
plus the 5 payload copies) were built by reading each source's bytes with
`shutil.copyfile` and writing them unedited — never retyped, never
edited. Each was read back from C1 (`76a970f1f`) with `git show
76a970f1f:<path>` and compared byte for byte against its source: all 6
`BYTE-IDENTICAL` (G1 above). `ledger.diff` was applied with `git apply`
after `git apply --check` passed (exit 0 both), never retyped or edited;
its resulting file contents (`.agent/live_review.md`) were verified by
byte count and sha256 against the reviewer's own simulated reading at C2
(G2 above) — `MATCH`; `.agent/plan.md` was separately rewritten whole via
`shutil.copyfile` from its payload and also confirmed `MATCH`.
`closure.diff` was applied the same way (`git apply --check` then `git
apply`, exit 0 both), never retyped or edited; its resulting file
contents (`docs/roadmap/STATUS.md`, `README.md`) were verified by byte
count and sha256 against the reviewer's own simulated reading (G4 above)
— `MATCH` on both.

## Deviations & assumptions

None. Every commit landed in the block's stated order C1, C2, C3, then
this closure commit C4, exactly as ordered. G1–G4 ran before this
handback was written, as ordered; G5 runs after this handback is written
and before C4 is committed. No payload was edited, retyped or repaired.
The round's whole tracked path set matches constraint 3 exactly: `git
diff --name-only 787759d9` over C1 through C3 named exactly the six
`.agent/authored/f019-r9-*` copies, `.agent/live_review.md`,
`.agent/live_review_archive.md` and `.agent/plan.md`; C4 adds exactly
`docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`, matching
the closure commit's stated path set exactly. There is no
`scripts/self_use_queue.json` edit: F019 is not a findings-paydown
feature and registers nothing, and the closure's self-use track answered
NONE (`.agent/selfuse_f019/result.txt`), unchanged this round. C4 is the
LAST commit on this branch per Rule A4; nothing follows it except, if the
reviewer's closure gate asks for one, a commit whose path set is exactly
`.agent/candidates.md`, which this block does not order and which I do
not write on my own initiative. Nothing is merged: no `gh pr merge`, no
checkout of `main`, no branch deletion, no force-push. The evidence
package, its SHA-256, its directory, the evidence job and the accepted
head this handback names are all from round 8, exactly as the block
orders: package `remedy-review-20260924-204836-READY_FOR_REVIEW.zip`, its
SHA-256 `d0340a1a2ed77a6472e2d3f3469a4e5bf590674fd21e4d229b9c4d52d01263ff`,
its directory `/home/decodeux/Repos/remedy-history/zips`, the evidence
job `f019r8e1001` and the accepted head
`d581b6667a9e29a1d276a39555b9038adb82a92b`. This handback does not name a
pull request number, which does not exist when it is written, and carries
no partial GitHub URL path of that kind anywhere above.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 339 insertions, matches (178 block + 161) |
| C2 | done | git apply --check and apply both exit 0; 2/0, 6/6 insertions, matches both files |
| C3 | done | rotation script exit 0; printed output matches the reviewer's simulated reading exactly; 0/24, 24/0 insertions, matches |
| C4 | done | closure.diff apply --check and apply both exit 0; 14/2 README.md, 1/1 STATUS.md, matches |
| G1 | done | all 5 payload digests and 6 authored-copy comparisons matched |
| G2 | done | both named file digests matched at C2; 1 new Gate line; open_finding_ids correct at both commits |
| G3 | done | rotation output, byte counts and sha256 of both ledger files matched the reviewer's simulation exactly |
| G4 | done | STATUS.md and README.md digests matched; status line occurs once; serial pytest 437 passed/1 skipped exit 0; integrity check all 6 pass fail_count 0; integrity block all 7 items OK exit 0 |
| G5 | done | reported in the reply (measured after this handback, before C4 commits) |
| G6 | done | reported in the reply (push, PR number/URL, tree/PR state after C4) |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the Open PR Gate — the
pull request this round opens is merged by the NEXT feature's session,
never by this one. Then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`. Open findings: 4. Operator questions open: 3.
