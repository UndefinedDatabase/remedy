# Handback — F278 Durable writes & loud failures · Round 12 · The closure: rotation, accepted STATUS line with README pins, and the pull request

## Session

SESSION 2 of feature F278 · round 12 · rounds so far 12

This round is the closing round. It copied the round's block and ten
payloads into `.agent/authored/` (C1); booked round 11's PASS onto
`.agent/live_review.md` by strict byte concatenation and rewrote
`.agent/plan.md` (C2); ran the finding-ledger rotation as its own commit,
moving 24 gate records and 4 finding pairs (8 records) into the archive
(C3); and applied the closure edits — the accepted `[x]` line in
`docs/roadmap/STATUS.md`, the three pinned places in `README.md` (accepted
count, Tier 2 Done cell, Tier 2 prose entry), and `SU-027`'s `consumed_by`
in `scripts/self_use_queue.json` — together with this handback (C4). All of
G1-G5 ran before C4 was committed and matched the block's stated
expectations exactly, byte for byte and reading for reading. Context
self-assessment: a comfortable majority of the working budget remains at
handback.

## Range

Review of `5558aa1d`..`HEAD`.

## Commits

### e28cb30d F278 R12 C1: copy round 12 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r12-block.md | +190/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r12-ledger.md | +2/-0 | Payload copy: round 11's `Gate:` entry |
| .agent/authored/f278-r12-plan.md | +28/-0 | Payload copy: the plan.md rewrite |
| .agent/authored/f278-r12-readme_count_from.txt | +1/-0 | Payload copy: README accepted-count FROM |
| .agent/authored/f278-r12-readme_count_to.txt | +1/-0 | Payload copy: README accepted-count TO |
| .agent/authored/f278-r12-readme_prose_from.txt | +1/-0 | Payload copy: README Tier 2 prose FROM |
| .agent/authored/f278-r12-readme_prose_to.txt | +8/-0 | Payload copy: README Tier 2 prose TO |
| .agent/authored/f278-r12-readme_tier_from.txt | +1/-0 | Payload copy: README Tier 2 table Done-cell FROM |
| .agent/authored/f278-r12-readme_tier_to.txt | +1/-0 | Payload copy: README Tier 2 table Done-cell TO |
| .agent/authored/f278-r12-status_from.txt | +1/-0 | Payload copy: STATUS line FROM |
| .agent/authored/f278-r12-status_to.txt | +1/-0 | Payload copy: STATUS line TO |

Measured insertions: 235 (190+2+28+1+1+1+8+1+1+1+1), under the 500 cap.

### a3ce1bb4 F278 R12 C2: book round 11's PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `ledger.md` appended by strict byte concatenation onto the `5558aa1d` bytes |
| .agent/plan.md | +10/-9 | Rewritten to the round-12 plan.md payload |

Measured insertions: 12 (2+10), deletions: 9, both by `git show --numstat` and
`git log --stat` (re-checked twice after an inconsistent reading appeared
transiently in the commit command's own stdout at commit time; see
Deviations).

### 99045bac F278 R12 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0/-64 | `rotate_live_review.py`: 24 gate records + 4 finding pairs (8 records) moved out |
| .agent/live_review_archive.md | +64/-0 | Same records moved in |

Measured insertions: 64, deletions: 64, all from the rotation script.

### C4 (this commit) F278 R12 C4: accept F278 in STATUS with its README pins and the self-use entry
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | `[~]` line replaced by the accepted `[x]` line (status pair) |
| README.md | +9/-2 | Accepted count, Tier 2 Done cell, Tier 2 prose entry (three pairs) |
| scripts/self_use_queue.json | +1/-1 | `SU-027`'s `"consumed_by": ""` set to `"F278"`, text edit only |
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git push origin feature/f278-durable-writes-loud-failures` — after C4: see the session's final reply for the real outcome; it runs after this commit.
- `gh pr create --base main --head feature/f278-durable-writes-loud-failures` — see the session's final reply for the PR number and URL; it runs after the push, after this commit.
- No `gh pr merge`, no force-push, no `git stash`, no checkout of another branch or commit in the primary checkout: none run, per the block's constraints.
- No self-use runs, job worktrees or job branches were created or removed this round; anything pre-existing under `.remedy-wt/` was left untouched, per constraint 7.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, absent (proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `feature/f278-durable-writes-loud-failures`. `git log --oneline -1` → `5558aa1d F278 R11 C3: rewrite handoff for round 11 with the evidence and package readings`.
- Block bytes (R-0954): measured line count (newline count)=190, sha256=`fe55fc13f748861257b5b0561dc341db09f7f43ea33334711e52c2ed034f3cbf`; matches both readings given in the delegation message exactly.
- `git stash list` first line (before C1) → `stash@{0}: WIP on (no branch): 365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`.

PAYLOADS — all 10 measured and matched the block's table exactly: ledger.md (2/2371/`9599aba3f85c683e4d7ebd5ee54c534b26e6ec25ad8acfd9720ee67739710ab8`), plan.md (28/1030/`3fcd1b8ca04ff18ceaba9681e2a34097e3e76db3f2346a7c8019f9919c26eaad`), readme_count_from.txt (0/36/`eb97e2238fecfc7b4abd0d9a35cbf69ce5b323915288f27506cbe34001301806`), readme_count_to.txt (0/36/`02205025b2739a377b34f50948095a51de409d93bd36935b9db7aea45bdfa579`), readme_prose_from.txt (0/27/`ffcd85056bd4e13d8d0c64883d6769d0d80821e56ec9417504245c24e4640299`), readme_prose_to.txt (7/587/`f1280dcc322f7ffb0bd7238221113ab5506e10b97336b4faaec1e5f70736f859`), readme_tier_from.txt (0/44/`108b2c75ad90a36e36fee3bb55b2996c44d266fea0e38cc9fb84e54de4a9f5f0`), readme_tier_to.txt (0/44/`654915a8657fe94b203354b6994b68a6dadb005a21de49c872e1e1b124520517`), status_from.txt (0/45/`f844a4503c6a065ceb23cf8f181a5407588f0a4b5fa5b5519bfac8e22264715a`), status_to.txt (0/402/`579d40f8334d85f139af279f3cd0f8360af08fa307246c8091d198a21b0d923d`).

G1 TRANSPORT — every `.agent/authored/f278-r12-*` copy (plus the block copy) read back with `git show e28cb30d:<path>` and compared byte-for-byte against its source: all 11 copies matched exactly, equal on both sides in every case.

G2 THE BOOKING — at C2 (`a3ce1bb4`):
- `.agent/live_review.md`: bytes=465513, sha256=`50617da22f505ad916549ad1f31683bca1ee661f02df7e299d97dd0565c4a757` — MATCH to the block's stated reading exactly.
- `.agent/plan.md`: sha256-equal to the plan.md payload — MATCH.
- `^Gate: F278 R11 — ` occurs 1 time in the post-append text — MATCH.
- Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`): pre (`5558aa1d`) count=26, post (C2) count=26 — matching the block's 26/26.

G3 THE ROTATION — at C3 (`99045bac`), `python3 scripts/rotate_live_review.py` real exit 0:
gate records moved: 24; finding pairs moved: 4 (8 records); old ledger size 465513 bytes, new ledger size 374026 bytes; old archive size 4575897 bytes, new archive size 4667384 bytes; open findings before 26, after 26. Post-rotation sha256: ledger `5ef819652c64cb796ffaea674aedd53881970c34d4cde272e083016a3cde5ac6`, archive `0b4060395f3142622e074d31d894db6abd79ef4a26eb0b77baddc3177598e624` — both MATCH the block's stated readings exactly. C3's path set: `.agent/live_review.md` and `.agent/live_review_archive.md`, and nothing else (`git diff --stat` at C3 confirms exactly those two paths).

G4 THE CLOSURE EDITS — before C4 was committed:
- `status` pair on `docs/roadmap/STATUS.md`: FROM count before=1, FROM count after=0, TO count after=1.
- `readme_count` pair on `README.md`: FROM count before=1, FROM count after=0, TO count after=1.
- `readme_tier` pair on `README.md`: FROM count before=1, FROM count after=0, TO count after=1.
- `readme_prose` pair on `README.md`: FROM count before=1, FROM count after=0, TO count after=1.
- `scripts/self_use_queue.json`: `"consumed_by": "",` count before=1, after=0; `"consumed_by": "F278",` count after=1, carried by entry `SU-027`; `python3 -m json.tool` accepted the file (real exit 0); `git diff --numstat` of the queue file read `1  1  scripts/self_use_queue.json` — MATCH (1 insertion, 1 deletion).
- Post-edit sha256, staged, pre-C4: `docs/roadmap/STATUS.md` = `3cfef11ce652f02f82ffbc6be93ac2beebe4bccfeb708efc84ca8adb27419f60`, `README.md` = `f787c108fd9710747058b98b82387f7b3140804834c30a89a0918ab710281892`, `scripts/self_use_queue.json` = `7f4636092fee3f03510cebd13701ee4e76beb8704427fe10816407df3cc622b8` — all three MATCH the block's stated readings exactly.
- `python3 -m pytest tests/docs/ -q` → `315 passed in 84.69s`, real exit 0 — MATCH the dry run's `315 passed` at exit 0.

G5 THE TREE — with C4's edits staged (STATUS.md, README.md, queue, before the handoff rewrite was added to the same set):
- `python3 -m apps.cli.main integrity check --json` → `passed: true`, `fail_count: 0`, all 5 checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `high_blockers_open`), real exit 0.
- `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 130.45s`, real exit 0. (The suite ran past the harness's default 3-minute window on the first attempt and required an extended timeout to complete; no repair was needed, the run simply needed more wall time.)

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- This block (`f278-r12-block.md`): `.agent/authored/f278-r12-block.md` at C1 verified byte-identical to `.remedy-wt/f278-r12-block.md` (G1) and to the two readings given in the delegation message.
- `ledger.md` (append): `.agent/live_review.md` at C2 sha256 `50617da22f505ad916549ad1f31683bca1ee661f02df7e299d97dd0565c4a757` == the reviewer's stated post-concatenation sha256 (G2). MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256-equal to the plan.md payload (G2). MATCH.
- `status_from.txt`/`status_to.txt`, `readme_count_from.txt`/`readme_count_to.txt`, `readme_tier_from.txt`/`readme_tier_to.txt`, `readme_prose_from.txt`/`readme_prose_to.txt` (all four FROM/TO pairs, applied by substring replacement, never retyped): each FROM read exactly once in its target before the edit and zero after, each TO exactly once after (G4); resulting `docs/roadmap/STATUS.md` and `README.md` sha256 both MATCH the reviewer's stated post-edit readings exactly (G4).
- The rotation (`scripts/rotate_live_review.py`, reviewer-authored, not a payload the worker retypes): its printed counts and post-rotation sha256 for both ledger files MATCH the block's stated dry-run readings exactly (G3).

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | 24 gate records + 4 finding pairs (8 records) moved, both hashes match |
| C4 | done | four pairs applied, queue edit applied, tests/docs/ 315 passed |
| G1 TRANSPORT | done | |
| G2 THE BOOKING | done | |
| G3 THE ROTATION | done | both hashes match the block's stated readings exactly |
| G4 THE CLOSURE EDITS | done | all four pairs and the queue edit exact, all three hashes match, tests/docs/ 315 passed |
| G5 THE TREE | done | integrity passed, golden path 42 passed |
| G6 THE PUSH AND THE PULL REQUEST | done | reported in the session's final chat reply, not this file, since it runs after C4 |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1, C2, C3, C4)
exactly and touched exactly the tracked path set constraint 3 names.

One reading anomaly, not a disk defect: immediately after the `git commit`
call for C2, the commit command's own stdout displayed a summary line
reading "2 files changed, 30 insertions(+), 27 deletions(-)". This
disagreed with the `git diff --stat` reading taken immediately before the
same commit ("12 insertions(+), 9 deletions(-)"). Re-checked twice after
the fact with `git show --numstat a3ce1bb4` and `git log -1 --stat
a3ce1bb4`: both independently read 12 insertions (2+10), 9 deletions,
agreeing with the pre-commit reading and not the transient one. The commit
content itself (the ledger append and the plan rewrite) is correct and
matches the payloads exactly per G2; only one single terminal-output line
briefly disagreed with the disk truth. This handback reports the
disk-verified 12/9, not the transient 30/27.

No other procedural deviation. Nothing was merged this round, per
constraint 6. No `remedy/job-*` branch or self-use worktree was created,
touched or deleted, per constraint 7.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the Open PR Gate — the
pull request this round opens is merged by the NEXT feature's session,
never by this one — and then Rule A5, the first unchecked feature in
`docs/roadmap/STATUS.md`. Open findings: 26. Operator questions: 0.
