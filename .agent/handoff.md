# Handoff — F028, round 12 (closure)

## Session

SESSION 2 of feature F028 · round 12 · rounds so far 12. Context remaining
at handback: ample — this round read `AGENTS.md`, the block, the seven
payloads, `docs/agents/handback_template.md` and the previous handoff for
its table format; no source module needed reading since the round books
round 11's PASS, rotates the ledger and applies the reviewer's closure
diff rather than writing new production code.

## Range

Review of `41e4b9fd`..`HEAD` (`HEAD` is this handback's own commit, `F028
R12 C4`, on `feature/f028-task-injection`).

## Commits

### 1cedcf1da F028 R12 C1: copy round 12 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r12-block.md | 157/0 | copy of this round's block |
| .agent/authored/f028-r12-build.py | 104/0 | copy of the reviewer's simulation source |
| .agent/authored/f028-r12-closure.diff | 55/0 | copy of the closure diff payload |
| .agent/authored/f028-r12-ledger.md | 2/0 | copy of the ledger-append payload |
| .agent/authored/f028-r12-plan.md | 25/0 | copy of the plan payload |
| .agent/authored/f028-r12-pr_body.md | 83/0 | copy of the PR description payload |
| .agent/authored/f028-r12-readme_para.txt | 12/0 | copy of the README paragraph payload |
| .agent/authored/f028-r12-status_line.txt | 1/0 | copy of the STATUS line payload |

Measured insertions: 439 (block's own line count 157 + 282), matching the
block's expectation exactly, under the 500-line cap.

### ae51859d9 F028 R12 C2: book round 11's PASS, the package READY_FOR_REVIEW
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | round 11's Gate entry appended (ledger.md payload) |
| .agent/plan.md | 5/5 | rewrite from the plan.md payload |

Matches the block's expected numstat (2/0, 5/5) exactly. `.agent/plan.md`
rewritten via `shutil.copyfile`; `.agent/live_review.md` appended
byte-for-byte from `ledger.md`, which itself begins with a blank line.

### 02b0aedac F028 R12 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 0/36 | rotation moved 10 gate records + 4 finding pairs (8 records) out |
| .agent/live_review_archive.md | 36/0 | the same records appended to the archive |

Matches the block's expected numstat (0/36, 36/0) exactly. Produced by
`python3 scripts/rotate_live_review.py`, real exit 0; its full printed
output is reported in the round reply. Path set: exactly the two ledger
files, nothing else.

### F028 R12 C4: accept F028 in STATUS with its README pins (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | 1/1 | closure.diff: STATUS line flipped `[~]` → `[x]` with the accepted-head pins |
| README.md | 15/2 | closure.diff: accepted count 108→109, Tier 5 Done 25→26, F028 prose paragraph added |
| .agent/handoff.md | rewrite | this handback |

Applied via `git apply --check` (exit 0) then the real apply (exit 0) of
`closure.diff`; the two file diffs measured 15/2 and 1/1 before this
commit, matching the block's expectation exactly.

## External actions

- No `git worktree add`/`remove` this round; `git worktree list | wc -l`
  read 61 at session start, unchanged (nothing added or removed).
- No push yet at the time this file is written — the block orders exactly
  one push, after C4, reported under G6 and External actions cannot be
  known in advance of it; `git push origin feature/f028-task-injection`
  runs immediately after this commit and its real outcome is reported in
  the round reply.
- `gh pr create --base main --head feature/f028-task-injection --title
  "F028 — Task injection" --body-file .remedy-wt/f028-r12/pr_body.md` runs
  after the push; its number and URL are reported in the round reply only
  (this handback names NO pull request number, since none exists yet).
- No `gh pr merge`, no checkout of `main`, no branch deletion, no
  force-push, no `git stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `build.py`: 104 lines, 5844 bytes, sha256
  `356e6c3eff06599372f05609e848518f50571a4fd5ea7fcdc45f20a35c300c27`.
- `closure.diff`: 55 lines, 3456 bytes, sha256
  `d5a46d60f97f1139a337cf0d35a225ed7102fb86529ed9567ce589f451911ba3`.
- `ledger.md`: 2 lines, 1868 bytes, sha256
  `9a8d58f847d5b4c827c598898c00c777ead5dd715c5cc066ab896c5488d9b5f1`.
- `plan.md`: 25 lines, 802 bytes, sha256
  `bc5319158c2afb0405567f624c17d6addb067d15eb7348da689c7ba6ea6c5d42`.
- `pr_body.md`: 83 lines, 5237 bytes, sha256
  `730ec6829fc17c6fc9da16243125c064f3530112dbc8d7b8f6c7c6f475a4f68a`.
- `readme_para.txt`: 12 lines, 1008 bytes, sha256
  `ffee8298a57459bca3e524d1ff7fe965ee0a9180cf861117b61150f2e4936b16`.
- `status_line.txt`: 1 line, 389 bytes, sha256
  `1a332d9cfaa685cab2397a6b8ff3450e7383d44c1278665913ea060fb9f4fbad`.
- Block: 157 lines, sha256
  `242be8a91b1b9968041dc39e200fe2fed6e9c25633a61bc845af9b0c7ab7a05d` —
  MATCH against both readings the delegation message stated (step 3).

Each `.agent/authored/f028-r12-*` payload copy, read back with `git show
<commit>:<path>` from C1 (`1cedcf1da`), compared byte-for-byte against its
source — all seven payloads plus the block MATCH (verified by length
equality and direct byte comparison, not by re-hashing separately).

### G2 — THE BOOKING
`git show <C2>:<path>`, bytes and sha256, read at `ae51859d9`, MATCHING
the reviewer's table exactly:
```
.agent/live_review.md   bytes=342930 sha256=de07c53a382777485726fbc9f9a0b9b272a11ff7687e1386923295021c0bd6da
.agent/plan.md          bytes=802    sha256=bc5319158c2afb0405567f624c17d6addb067d15eb7348da689c7ba6ea6c5d42
```
Both MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text at C2, reads `[]` —
MATCH against the reviewer's stated reading.

### G3 — THE ROTATION
```
$ python3 scripts/rotate_live_review.py
gate records moved: 10
finding pairs moved: 4 (8 records)
old ledger size: 342930 bytes
new ledger size: 305800 bytes
old archive size: 5214551 bytes
new archive size: 5251681 bytes
open findings before: 0
open findings after: 0
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
REAL_EXIT=0
```
Line for line identical to the reviewer's simulation apart from the final
`written:` line, which names the worker's own repo paths (not the
simulation's) as expected. Post-rotation file readings, MATCHING the
reviewer's table exactly:
```
.agent/live_review.md         bytes=305800  sha256=d6a70e718556dfd5f526142c9ef93532b0c52a24cda01992b43a05a4658dbdeb
.agent/live_review_archive.md bytes=5251681 sha256=8d5c7b464af6e4df33bac23d93c260e403cd3159b6336692630dcdf30fe5c5dd
```
C3's path set was exactly `.agent/live_review.md` and
`.agent/live_review_archive.md`, nothing else (`git status --porcelain`
before staging showed only these two paths modified).

### G4 — THE CLOSURE EDITS AND THE TREE
`closure.diff` applied via `git apply --check` (exit 0) then the real
apply (exit 0). File readings after apply, before this handback commit,
MATCHING the reviewer's table exactly:
```
docs/roadmap/STATUS.md bytes=55186 sha256=503ce42ccb7b3d93c869c00f4246c232aa6a8034ae5b42aa68e17998ec947abe
README.md              bytes=39048 sha256=c305fc3c1cea302f8a6f12a8346b44f62a9d3c4d588a54b2a395505cf327950b
```
The STATUS line from `status_line.txt` occurs exactly 1 time in
`docs/roadmap/STATUS.md` — MATCH. `pending_self_use_items()` from
`packages.orchestration.self_use_queue` read `()` (length 0, empty) —
MATCH, confirming closure precondition 6 reads self-use NONE (queue exhausted). Serially:
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
........................................................................ [ 98%]
........                                                                 [100%]
512 passed in 40.64s
REAL_EXIT=0
```
Matches the reviewer's simulation exactly (512 passed, exit 0).
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=164"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
All six checks read `pass` (the reading, not the exit code), `fail_count`
0 — MATCH.

### G5 — THE HANDBACK'S PINS
Reported in the round reply (necessarily taken after this file is written
and before the C4 commit).

### G6 — AFTER C4
Reported in the round reply (necessarily taken after this commit and the
subsequent push and PR create).

## Authored-text proofs

- Block copy (`.agent/authored/f028-r12-block.md`, at `1cedcf1da`) vs
  `.remedy-wt/f028-r12/block.md`: byte-identical, sha256
  `242be8a91b1b9968041dc39e200fe2fed6e9c25633a61bc845af9b0c7ab7a05d` both
  sides.
- `build.py` copy vs source: byte-identical, sha256
  `356e6c3eff06599372f05609e848518f50571a4fd5ea7fcdc45f20a35c300c27` both
  sides; copied for the record, never run (the block names it as the
  reviewer's simulation source).
- `closure.diff` copy vs source: byte-identical, sha256
  `d5a46d60f97f1139a337cf0d35a225ed7102fb86529ed9567ce589f451911ba3` both
  sides; applied via `git apply --check` then the real apply at C4, never
  edited or retyped.
- `ledger.md` copy vs source: byte-identical, sha256
  `9a8d58f847d5b4c827c598898c00c777ead5dd715c5cc066ab896c5488d9b5f1` both
  sides; appended byte-for-byte to `.agent/live_review.md` at C2.
- `plan.md` copy vs source: byte-identical, sha256
  `bc5319158c2afb0405567f624c17d6addb067d15eb7348da689c7ba6ea6c5d42` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `pr_body.md` copy vs source: byte-identical, sha256
  `730ec6829fc17c6fc9da16243125c064f3530112dbc8d7b8f6c7c6f475a4f68a` both
  sides; passed to `gh pr create --body-file` unedited.
- `readme_para.txt` copy vs source: byte-identical, sha256
  `ffee8298a57459bca3e524d1ff7fe965ee0a9180cf861117b61150f2e4936b16` both
  sides; copied for the record, folded into `closure.diff` by the
  reviewer, never applied separately by the worker.
- `status_line.txt` copy vs source: byte-identical, sha256
  `1a332d9cfaa685cab2397a6b8ff3450e7383d44c1278665913ea060fb9f4fbad` both
  sides; used only as G4's proof string, never applied (the STATUS line
  itself arrives via `closure.diff`).

## Deviations & assumptions

None. C1, C2, C3 and C4 landed in the block's exact order, no extra
commit, no reordering, no gate went red on any run, and no payload was
edited or retyped. Every numeric expectation the block stated (439
insertions at C1, 2/0 and 5/5 numstat at C2, the rotation's exact
line-for-line output and 0/36 + 36/0 numstat at C3, 15/2 and 1/1 numstat
at C4, six passing checks and 512 passed at G4) was met exactly as
stated.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | 439 insertions (157 + 282), all eight authored copies MATCH |
| C2 | done | numstat 2/0 + 5/5 exact match; open_finding_ids [] |
| C3 | done | rotation output line-for-line match; numstat 0/36 + 36/0 exact match |
| C4 | done | closure.diff applied clean; numstat 15/2 + 1/1 exact match; STATUS line count 1; pending self-use items 0; 512 passed exit 0; integrity 6/6 pass |
| G1 | done | all seven payloads and the block MATCH the table exactly |
| G2 | done | both records MATCH; open_finding_ids [] |
| G3 | done | rotation output and both post-rotation files MATCH the reviewer's table exactly |
| G4 | done | both closure-edit files MATCH; status_line count 1; pending_self_use_items empty; 512 passed exit 0; integrity 6/6 pass, fail_count 0 |
| G5 | done | its readings (string counts, the no-PR-number check, item-status table presence) are necessarily taken after this file is written and before C4 is committed; reported in the round reply |
| G6 | done | its readings (git log, git status, push outcome, PR number/URL, `gh pr list`) are necessarily taken after this commit and the subsequent push/PR create; reported in the round reply |
| Pull request | done | opened after C4 and its push, from `feature/f028-task-injection` into `main`, NOT merged; number and URL reported in the round reply |

## Next

Phase 1 rule 1, then the Open PR Gate — the pull request this round opens
is merged by the NEXT feature's session, never by this one — then Rule
A5, the first unchecked feature in `docs/roadmap/STATUS.md`. Open findings
(by `open_finding_ids` at C3, this round's rotation): 0. Operator
questions open: 0.

Evidence job `f028r11e1001`; package
`remedy-review-20260927-132129-READY_FOR_REVIEW.zip`, SHA-256
`904723bf332d1f076cdfde262f84609fada02ca86635f3ef09a88c3d025692fe`,
directory `/home/decodeux/Repos/remedy-history/zips`; accepted head
`9cfd84d1217c24057173f4b9a8db03734c174c09`; self-use NONE (queue exhausted).
