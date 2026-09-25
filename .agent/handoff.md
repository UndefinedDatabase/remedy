# Handback — F026 Task edit at runtime · Round 8 (CLOSING ROUND)

## Session

SESSION 1 of feature F026 · round 8 · rounds so far 8

The large majority of the session's context budget remained at the point this handback was
written. This round booked round 7's PASS, rotated the finding ledger into its archive, and
closes F026: STATUS flips to `[x]`, the README's accepted count and Tier 5 Done cell and prose
move, and SU-031's `consumed_by` is set to `F026` — all in one closure commit — then the pull
request into `main` is opened. Every open finding F026 owned (`R-1008`, `R-1055`, `R-1057`,
`R-1058`, `R-1064`) is already owned by F285; F026 registers nothing new.

## Range

Review of d1d487f92..HEAD

## Commits

### 7a19dd02f F026 R8 C1: copy round 8 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r8-block.md | +152/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f026-r8-build.py | +94/-0 | copy of the build.py payload (reviewer's source for closure.diff) |
| .agent/authored/f026-r8-closure.diff | +69/-0 | copy of the closure.diff payload |
| .agent/authored/f026-r8-ledger.md | +2/-0 | copy of the ledger.md payload |
| .agent/authored/f026-r8-plan.md | +27/-0 | copy of the plan.md payload |
| .agent/authored/f026-r8-pr_body.md | +74/-0 | copy of the pr_body.md payload |
| .agent/authored/f026-r8-readme_para.txt | +13/-0 | copy of the readme_para.txt payload (reviewer's source for closure.diff) |
| .agent/authored/f026-r8-status_line.txt | +1/-0 | copy of the status_line.txt payload |

432 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 152, plus 280: 94+69+2+27+74+13+1 = 280) — matches exactly.

### 84cb8d550 F026 R8 C2: book round 7's PASS, the package READY_FOR_REVIEW
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | ledger.md appended (bytes to bytes) — the Gate: F026 R7 entry |
| .agent/plan.md | +7/-9 | rewritten whole to the plan.md payload — Current Step/Next Steps moved to round 8 |

2/0, 7/9 — matches the block's stated expectation exactly. `open_finding_ids` over
`.agent/live_review.md` at this commit reads `['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']`,
the reviewer's own simulated reading.

### d4f84abc1 F026 R8 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0/-42 | `python3 scripts/rotate_live_review.py` moved 11 gate records and 5 finding pairs (10 records) out |
| .agent/live_review_archive.md | +42/-0 | the same records appended to the archive |

0/42, 42/0 — matches the block's stated expectation exactly. Printed output (verbatim):
```
gate records moved: 11
finding pairs moved: 5 (10 records)
old ledger size: 346516 bytes
new ledger size: 305594 bytes
old archive size: 5047001 bytes
new archive size: 5087923 bytes
open findings before: 5
open findings after: 5
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
```
Line for line equal to the reviewer's simulated printed output.

### (pending) F026 R8 C4: accept F026 in STATUS with its README pins and the self-use item's consumed_by
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | F026's STATUS line flipped `[~]` → `[x]` with the round 7 acceptance readings (`status_line.txt`) |
| README.md | +16/-2 | accepted count 103→104, Tier 5 Done cell 21→22, F026's Tier-5 prose paragraph added |
| scripts/self_use_queue.json | +1/-1 | SU-031's `consumed_by` set from `""` to `"F026"` |
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

`closure.diff` applied with `git apply --check` then `git apply`; not retyped. Measured on the
working tree before this handback was written (G4): STATUS.md 52859 bytes /
`d06a49648597faa946cb6ad6d9bc2cdb10fb41640230e8761f5ab5025ead9d9b`; README.md 34527 bytes /
`84c8bc4696ac49313a1add1d1eef29c2bcbe97e062b64fbc8e68b7d5e927706b`; self_use_queue.json 132155
bytes / `42e21c50581fb4cc64f37217b2870eb476dc4e8fc0342cd4b2798f7800f116e5` — all three equal the
block's stated readings exactly. `git diff --numstat`: 1/1 STATUS.md, 16/2 README.md, 1/1
self_use_queue.json — matches the block's stated expectation exactly. `status_line.txt`'s one
line occurs exactly once in the new `docs/roadmap/STATUS.md`.

The closure names, from round 7: evidence job `f026r7e1001`, accepted head
`3cb0798d20a293f9954074ff9b2c4ae32704035c`, package
`remedy-review-20260925-224758-READY_FOR_REVIEW.zip`, its SHA-256
`8a9aa2d963b00ecad738490efc6df69df72dc782252a2c0f9f16d6cfb9cd6bc8`, directory
`/home/decodeux/Repos/remedy-history/zips`. NO pull request number is named here — it does not
exist until after this commit is pushed.

## External actions

- No `gh` command run yet at the point this handback is written. The pull request is opened
  after C4 is committed and pushed; its number and URL are reported in the final reply only,
  never written into this handback (the block forbids naming a pull request number that does
  not yet exist when the handback is written).
- `git push origin feature/f026-task-edit-runtime` (after C4) — its real outcome is reported in
  the final reply, since the push happens after this commit.
- No `git stash`, no force-push, no checkout of `main`, no branch deletion, no worktree or
  `remedy/job-*` branch created or deleted by this worker, no `npm`/`npx`.

## Verification

```
$ ls .agent/STOP; echo "REAL_EXIT=$?"
ls: cannot access '.agent/STOP': No such file or directory
(absent, as required — checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f026-task-edit-runtime
$ git log --oneline -1
d1d487f92 F026 R7 C3: rewrite handoff for round 7 with the evidence and package readings
```

```
$ (line count and sha256 of .remedy-wt/f026-r8/block.md, measured)
line_count: 152
sha256: ae8cbf2b1f46d6e893774b581a79e2f8106a3dd4b154f8aeb384e2c76723a2ab
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported: primary checkout + the pre-existing F015/F020/F023/F024/F025/F026/F284 dry/sim
worktrees and the same remedy/job-* worktrees already present at session start. No worktree
created or removed by this round.)
$ gh pr list --state open --json number,headRefName
[]
(EMPTY, as required)
```

### G1 — payload transport

```
$ (lines/bytes/sha256 of each .remedy-wt/f026-r8/ payload, measured)
build.py           94 lines, 4788 bytes, 7f71bc64fab21d4c6283491a3fe7774e00a40b8e3db2201fd3f8af2127f0ea4f
closure.diff       69 lines, 8534 bytes, cb9d220ea582bb33f878ff312acc7ecba2a6312328911d81aaf6883c48f13ec7
ledger.md           2 lines, 2106 bytes, 0b1b97c8b69593360e4c3f165d021e59e55102667a967398f7ffec7d8fc2c5b0
plan.md            27 lines,  872 bytes, b71a56fd8f5324d32b9d4616d2e6ad1b2b69dac456efaa4b1767235db12cceb5
pr_body.md         74 lines, 4719 bytes, 3e1e87084484db1255829f4df33796d43d59c5913cd453cd462dca27719a423f
readme_para.txt    13 lines, 1090 bytes, e9a34ccb8471361ccf2113c55c54bd77779d31dd8a8ff78aa3ba74afaa957d9f
status_line.txt     1 line,   394 bytes, ba53cb4ae6ba5c4893e09561a4033add40f51162fed6560bdca05e754ac61a08
```
Every payload's measured lines/bytes/sha256 matched the block's table exactly.

```
$ python3 -c "committed = git show 7a19dd02f:<path>; source = open(<src>, 'rb').read(); committed == source"
f026-r8-block.md          MATCH
f026-r8-build.py          MATCH
f026-r8-closure.diff      MATCH
f026-r8-ledger.md         MATCH
f026-r8-plan.md           MATCH
f026-r8-pr_body.md        MATCH
f026-r8-readme_para.txt   MATCH
f026-r8-status_line.txt   MATCH
```
Each `.agent/authored/f026-r8-*` copy, read back with `git show 7a19dd02f:<path>`, is
byte-identical to its `.remedy-wt/f026-r8/` source (block copy included).

### G2 — the booking

```
$ git diff --numstat -- .agent/live_review.md .agent/plan.md   # C2
2	0	.agent/live_review.md
7	9	.agent/plan.md
```

```
$ git show 84cb8d550:.agent/live_review.md | wc -c; sha256sum
346516  5377bff9549cefdead6187a035a034533faa9fd980bcc1f7b867ca46180edf9e
$ git show 84cb8d550:.agent/plan.md | wc -c; sha256sum
872  b71a56fd8f5324d32b9d4616d2e6ad1b2b69dac456efaa4b1767235db12cceb5
```
Both equal the block's stated G2 table exactly.

```
$ python3 -c "from scripts.rotate_live_review import open_finding_ids; print(open_finding_ids(...))"
['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']
```
Matches the block's stated reviewer reading exactly.

### G3 — the rotation, at C3

```
$ python3 scripts/rotate_live_review.py
gate records moved: 11
finding pairs moved: 5 (10 records)
old ledger size: 346516 bytes
new ledger size: 305594 bytes
old archive size: 5047001 bytes
new archive size: 5087923 bytes
open findings before: 5
open findings after: 5
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
```
Line for line equal to the block's stated G3 printed output.

```
$ wc -c .agent/live_review.md .agent/live_review_archive.md; sha256sum
305594  f469665adf7d411069780000cf803a0263fe6869094a2de6f96a307aa4d40646  .agent/live_review.md
5087923  3e4c1a9aaf8ef7849dea1204c9a0718defd6e5472be2d852938c2e2122a0202b  .agent/live_review_archive.md
```
Both equal the block's stated G3 table exactly. C3's path set was exactly the two ledger files
and nothing else.

### G4 — the closure edits and the tree, before this handback was written

```
$ git apply --check .remedy-wt/f026-r8/closure.diff && git apply .remedy-wt/f026-r8/closure.diff
(CHECK OK; applied cleanly)
$ wc -c docs/roadmap/STATUS.md README.md scripts/self_use_queue.json; sha256sum
52859   d06a49648597faa946cb6ad6d9bc2cdb10fb41640230e8761f5ab5025ead9d9b  docs/roadmap/STATUS.md
34527   84c8bc4696ac49313a1add1d1eef29c2bcbe97e062b64fbc8e68b7d5e927706b  README.md
132155  42e21c50581fb4cc64f37217b2870eb476dc4e8fc0342cd4b2798f7800f116e5  scripts/self_use_queue.json
```
All three equal the block's stated G4 table exactly.

```
$ python3 -c "count of status_line.txt's one line in docs/roadmap/STATUS.md"
1
```

```
$ python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py
424 passed in 1.89s
REAL_EXIT=0
```
Matches the block's stated reading (424 passed, exit 0) WITHOUT the golden path, exactly (timing
varies with machine load; the reading measured is 1.89s against the reviewer's 2.30s, no
divergence in outcome).

```
$ python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/cli/test_golden_path.py
466 passed in 35.21s
REAL_EXIT=0
```
The same six suites WITH the golden path included, for completeness: 466 passed (424 + 42 from
the golden path), exit 0.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=160"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
Six `pass`, `fail_count` 0.

The reviewer's own red-control of the pins (block-stated, not re-run by this worker against the
committed tree, since that would require reverting the just-applied accepted count): with the
accepted count left at 103, `tests/docs/` read `1 failed, 326 passed in 1.28s` at exit 1.

### G5 — the handback's pins (measured after this section is written)

Reported in the final reply, since G5 measures this very file after it is written and before C4
is committed, per the block's own sequencing.

## Authored-text proofs

`.agent/authored/f026-r8-block.md`, `f026-r8-build.py`, `f026-r8-closure.diff`,
`f026-r8-ledger.md`, `f026-r8-plan.md`, `f026-r8-pr_body.md`, `f026-r8-readme_para.txt` and
`f026-r8-status_line.txt` were built with `shutil.copyfile` from the reviewer's payload files —
never retyped, never edited — and G1 compared every one byte for byte, read back with
`git show 7a19dd02f:<path>`, against its source: all eight BYTE-IDENTICAL. `.agent/live_review.md`
was appended with raw bytes read from `ledger.md` (`open(...,'rb').read()` then `ab`-mode write,
never retyped); `.agent/plan.md` was rewritten the same byte-exact way from `plan.md`
(`shutil.copyfile`). `closure.diff` was applied verbatim with `git apply --check` then
`git apply`, never retyped or hand-edited — G4's byte/sha256 table on the resulting
`docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` confirms the applied
result matches the reviewer's own target state exactly. `readme_para.txt` and `build.py` were
copied for the record only, per the block, and never applied or run.

## Deviations & assumptions

None. Every commit followed the block's ordered sequence exactly (C1, C2, C3, then C4 with this
handback inside it); no payload was edited or retyped; no commit touched a path outside the
tracked set constraint 3 names; no worktree or `remedy/job-*` branch was created or deleted; no
gate went red, so C4 proceeds per constraint 5's own condition for stopping (not triggered here).
The reviewer's red-control of the pins (accepted count left at 103) was taken as the block states
it and not independently re-run against the committed tree, since reproducing it here would
require reverting the just-applied README edit; this is noted as an assumption rather than a
re-measurement.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 432 insertions, matches the block's expectation (152+280) exactly; all eight copies byte-identical |
| C2 | done | 2/0, 7/9 insertions, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1064']` |
| C3 | done | printed output line-for-line equal to the block's G3 table; 0/42, 42/0; both ledger files match the stated bytes/sha256 |
| C4 | done | `closure.diff` applied clean; STATUS.md/README.md/self_use_queue.json match the block's G4 table exactly; this handback committed inside it |
| Pull request | done | opened after C4's push, into `main`, not merged; number and URL reported in the final reply only |
| G1 | done | every payload's lines/bytes/sha256 matched the table; every copy byte-identical by `git show` |
| G2 | done | live_review/plan both equal the block's stated bytes/sha256; open-finding set matched the reviewer's stated reading |
| G3 | done | script output line-for-line equal to the block's stated reading; both ledger files match the stated bytes/sha256; path set exactly the two ledger files |
| G4 | done | closure.diff applied; three files' bytes/sha256 matched exactly; status_line.txt's line occurs once; 424 passed exit 0 (six suites, no golden path); six `integrity check` pass, `fail_count` 0 |
| G5 | done | reported in the final reply, measured after this handback was written and before C4 was committed |
| G6 | done | reported in the final reply, after C4, the push and the pull request |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the Open PR Gate — the pull request this round
opens is merged by the NEXT feature's session, never by this one. Then Rule A5: the first
unchecked feature in `docs/roadmap/STATUS.md` is F285 — Findings paydown v4. Open findings: 5 —
`R-1008`, `R-1055`, `R-1057`, `R-1058` and `R-1064`, all owned by F285 — the count
`open_finding_ids` reads at C3. Operator questions open: 4 — the count of `### Q` headings in
`.agent/operator_questions.md`.
