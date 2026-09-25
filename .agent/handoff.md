# Handback — F024 Phase timeline with scrubber · Round 8 (closing round)

## Session

SESSION 1 of feature F024 · round 8 · rounds so far 8

Ample context remained throughout this round; a large majority of the budget remained at the point
this handback was written.

## Range

Review of 59ee84e42..HEAD

## Commits

### f5d5e214a F024 R8 C1: copy round 8 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r8-block.md | +194/-0 | copy of this round's block, verbatim |
| .agent/authored/f024-r8-closure.diff | +57/-0 | copy of the closure.diff payload |
| .agent/authored/f024-r8-ledger.diff | +10/-0 | copy of the ledger.diff payload |
| .agent/authored/f024-r8-plan.md | +28/-0 | copy of the plan.md payload |
| .agent/authored/f024-r8-pr_body.md | +64/-0 | copy of the pr_body.md payload |
| .agent/authored/f024-r8-status_line.txt | +1/-0 | copy of the status_line.txt payload |

354 insertions by `git show --numstat` (block's line count 194 + 160) — matches the block's
expectation exactly; well under the 500-insertion STOP threshold.

### 19ef0f7db F024 R8 C2: book round 7's PASS, the package READY_FOR_REVIEW
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | round 7's Gate entry appended, via `git apply` of ledger.diff |
| .agent/plan.md | +7/-6 | rewritten to the plan.md payload |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0. Insertions/deletions by `git show
--numstat`: 2/0 live_review.md, 7/6 plan.md — matches the block's expected counts (2/0, 7/6)
exactly.

### e069725fc F024 R8 C3: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0/-20 | gate records moved out to the archive |
| .agent/live_review_archive.md | +20/-0 | gate records moved in from the ledger |

`python3 scripts/rotate_live_review.py` printed: gate records moved 10, finding pairs moved 0 (0
records), old ledger size 311161 bytes, new ledger size 292216 bytes, old archive size 4993265
bytes, new archive size 5012210 bytes, open findings before 1, open findings after 1 — matching the
block's G3 table line for line. Insertions/deletions by `git show --numstat`: 0/20 live_review.md,
20/0 live_review_archive.md — matches the block's expected counts exactly. Path set: exactly the
two ledger files, nothing else.

### (this commit) F024 R8 C4: accept F024 in STATUS with its README pins
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | F024's STATUS line flipped `[~]` → `[x]` with T001–T003
complete, live review PASS — ACCEPTED, evidence job `f024r7e1001`, package
`remedy-review-20260925-082755-READY_FOR_REVIEW.zip`, SHA-256
`1c4b4b358b97b54252a665e60acd3eaaedb134b8b3b0cbbe5ee36d80e60289e6`, package path
`/home/decodeux/Repos/remedy-history/zips` and accepted HEAD `b650ced4b1d0fef4c9156de0b217cbad7a76bef7`, via `git apply` of closure.diff |
| README.md | +17/-2 | accepted count 101→102, Tier 5 Done cell 19→20, and Tier 5 prose paragraph
for F024 appended, via `git apply` of closure.diff |
| .agent/handoff.md | (self-reference) | this handback, rewritten for round 8's closing round |

Per the handback template's self-reference exception: a handback cannot table the commit that
writes it. Insertions reported in the final reply, as measured by `git show --numstat` after the
commit.

## External actions

None yet at the point this handback is written. C4's `git push origin
feature/f024-phase-timeline-scrubber` and the `gh pr create` into `main` both happen after this
handback is committed, and are reported in the final reply only, per G6 (these steps cannot be
captured before they happen).

## Verification

```
$ ls .agent/STOP; echo "REAL_EXIT=$?"
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2
(absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f024-phase-timeline-scrubber
$ git log --oneline -1
59ee84e42 F024 R7 C3: rewrite handoff for round 7 with the evidence and package readings
```
All BEFORE ANYTHING ELSE step 2 checks passed at round start.

```
$ (line count and sha256 of .remedy-wt/f024-r8/block.md, measured)
line_count: 194
sha256: 5b07351a02bccf2812d11e9897db25c2f7d045eb45af06045144e86e01152eb8
```
Matches both readings given in the delegation message exactly (194 lines,
5b07351a02bccf2812d11e9897db25c2f7d045eb45af06045144e86e01152eb8) — R-0954.

```
$ git worktree list
(primary + 15 f015-*-dry/sim r1-r6, 5 f015-*-sim r7-r9, 16 f020-*-dry/sim r1-r8,
 20 f023-*-dry/sim r1-r9, f023-r10-dry, f023-r10-sim, f024-r1..r7 dry/sim (14),
 f024-r8-dry, f024-r8-sim, 8 f284-*-dry/sim r1-r4, 4 job-* worktrees)
$ gh pr list --state open --json number,headRefName
[]
```
Empty, as required.

```
$ (lines/bytes/sha256 of each payload under .remedy-wt/f024-r8-payloads/)
closure.diff     lines=57 bytes=3903 sha256=1a4bb0c9b0b51f7606ea1ec98686c8fc049e7b1ddc70acb8e059e8ed148debd8
ledger.diff      lines=10 bytes=6157 sha256=bcb63619df95ed9dd0edd636a9b680358675b4be6e9a471a67b5e2074f851717
plan.md          lines=28 bytes=939  sha256=ba905eb3bc560879445dc9063a7fd10d6c2c077cb9a01d148660986f69436dfa
pr_body.md       lines=64 bytes=3766 sha256=24f29a751141417916a80258efa09a399274631718a5d35c8fcc1d118cd85275
status_line.txt  lines=1  bytes=402  sha256=8e33ff67a040a9bd6a5e3b9bec0a0938ab568c09efbbe7119b5eae75e631a268
```
All 5 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f024-r8-* blob against its source, via `git show <C1>:<path>`)
f024-r8-block.md         @ f5d5e214a: IDENTICAL (sha 5b07351a...)
f024-r8-closure.diff     @ f5d5e214a: IDENTICAL (sha 1a4bb0c9...)
f024-r8-ledger.diff      @ f5d5e214a: IDENTICAL (sha bcb63619...)
f024-r8-plan.md          @ f5d5e214a: IDENTICAL (sha ba905eb3...)
f024-r8-pr_body.md       @ f5d5e214a: IDENTICAL (sha 24f29a75...)
f024-r8-status_line.txt  @ f5d5e214a: IDENTICAL (sha 8e33ff67...)
```
All 6 BYTE-IDENTICAL against their sources (G1).

```
$ git apply --check .remedy-wt/f024-r8-payloads/ledger.diff; echo "REAL_EXIT=$?"
REAL_EXIT=0
$ git apply .remedy-wt/f024-r8-payloads/ledger.diff; echo "REAL_EXIT=$?"
REAL_EXIT=0
```
`.agent/plan.md` was rewritten whole with `shutil.copyfile` from the plan.md payload — never
retyped.

```
$ (bytes/sha256 of the files named in the block's G2 table, read at C2 via `git show <C2>:<path>`)
.agent/live_review.md bytes=311161 sha256=13c07741e2c2105a151d4338bc999a3f642f3a2d1cc7b5720446e692755cce5c match=True
.agent/plan.md         bytes=939    sha256=ba905eb3bc560879445dc9063a7fd10d6c2c077cb9a01d148660986f69436dfa match=True
```
Both match the block's G2 table exactly.

```
$ (lines C2's own diff adds to .agent/live_review.md beginning "Gate: F024 R7 — ")
count=1
```
Matches the block's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
  at 59ee84e4 and at 19ef0f7db (C2)
59ee84e4  open ids: ['R-1008']
19ef0f7db (C2) open ids: ['R-1008']
```
Reads R-1008 alone at both, matching the block's stated reading exactly (G2).

```
$ python3 scripts/rotate_live_review.py
gate records moved: 10
finding pairs moved: 0 (0 records)
old ledger size: 311161 bytes
new ledger size: 292216 bytes
old archive size: 4993265 bytes
new archive size: 5012210 bytes
open findings before: 1
open findings after: 1
written: /home/decodeux/Repos/remedy/.agent/live_review.md and
  /home/decodeux/Repos/remedy/.agent/live_review_archive.md
REAL_EXIT=0
```
Line for line identical to the block's G3 table.

```
$ (bytes/sha256 of the two ledger files after rotation)
.agent/live_review.md         bytes=292216  sha256=0ddd96d6df7623ed6932d829a06f413b8898ae38ca5cd91358286c4febbc2ed0
.agent/live_review_archive.md bytes=5012210 sha256=95c0d02ec6788a1067a8cbeaf2eff92a5c908503e890acf1d16081ba88c1e90f
```
Both match the block's G3 table exactly.

```
$ git apply --check .remedy-wt/f024-r8-payloads/closure.diff; echo "REAL_EXIT=$?"
REAL_EXIT=0
$ git apply .remedy-wt/f024-r8-payloads/closure.diff; echo "REAL_EXIT=$?"
REAL_EXIT=0
$ git diff --numstat
17	2	README.md
1	1	docs/roadmap/STATUS.md
```
Matches the block's expected 17/2 README.md, 1/1 STATUS.md exactly.

```
$ (bytes/sha256 of STATUS.md and README.md with closure.diff applied, before the handback)
docs/roadmap/STATUS.md bytes=52107 sha256=c8058ed59f6ac736cc1f64c390d561e7c120ff3fbd97a9c9011d308813d60869
README.md               bytes=32262 sha256=85f398bdc88f1738d58e7b958581d9d10b815309a659b0662e1e045a4b5c0f0a
```
Both match the block's G4 table exactly.

```
$ (count of lines of STATUS.md equal to status_line.txt's one line, byte for byte)
count=1
```
Matches the required 1 exactly.

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
  tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
......                                                                   [100%]
437 passed, 1 skipped in 59.53s
REAL_EXIT=0
```
This worker's run INCLUDES `tests/cli/test_golden_path.py` (the block's own selection names it), so
its count (437 passed) is not directly comparable to the reviewer's dry-run figure of `395 passed,
1 skipped`, which the block states was read WITHOUT the golden path over the same tree. Exit 0 in
both cases; no failures.

```
$ python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"
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
All six checks `pass`, `fail_count` 0.

```
$ python3 -m apps.cli.main integrity block .remedy-wt/f024-r8/block.md; echo "REAL_EXIT=$?"
  [OK] item 1 (size): 194 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 28 lines
  [OK] item 10 (open set recomputed): states 1; .agent/live_review.md holds 1 open by distinct id, and the block registers 0 and resolves 0, leaving 1
  [OK] item 24 (gate paths resolve): 0 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): the block orders no gates before a commit
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0
```
All 7 checkable items pass.

```
$ (self-use track, .agent/selfuse_f024/result.txt)
F024 closure — self-use track, closure precondition 6 of docs/roadmap/STATUS_closure_protocol.md
next_self_use_item() before: None
generate_and_append_if_empty(): None
next_self_use_item() after: None
scripts/self_use_queue.json: unchanged
self-use NONE (queue exhausted)
```
Confirms the block's statement: the closure's self-use track answered NONE; no
`scripts/self_use_queue.json` edit this round.

```
$ git diff --name-only 59ee84e4
(range through this commit, C1..C4)
.agent/authored/f024-r8-block.md
.agent/authored/f024-r8-closure.diff
.agent/authored/f024-r8-ledger.diff
.agent/authored/f024-r8-plan.md
.agent/authored/f024-r8-pr_body.md
.agent/authored/f024-r8-status_line.txt
.agent/live_review.md
.agent/live_review_archive.md
.agent/plan.md
docs/roadmap/STATUS.md
README.md
.agent/handoff.md
```
Exactly the tracked path set constraint 3 names.

## Authored-text proofs

All 6 authored copies under `.agent/authored/f024-r8-*` (the block copy, `closure.diff`,
`ledger.diff`, `plan.md`, `pr_body.md`, `status_line.txt`) were built by `shutil.copyfile` from
source to destination — never retyped, never edited. Each was read back with `git show
<C1>:<path>` and compared byte for byte against its source: all 6 BYTE-IDENTICAL (G1 above).
`ledger.diff` was applied with `git apply` after `git apply --check` passed (exit 0, both).
`.agent/plan.md` was rewritten whole via `shutil.copyfile` from the plan.md payload source — never
retyped — and confirmed MATCH against both the PAYLOADS table and the G2 table. `closure.diff` was
applied with `git apply` after `git apply --check` passed (exit 0, both), and the resulting
`docs/roadmap/STATUS.md` / `README.md` bytes confirmed MATCH against the G4 table.

## Deviations & assumptions

None. All four content commits landed in the block's stated order — C1, C2, C3, C4 — with no
payload edited, retyped or repaired. G1 through G4 ran before this handback was written, per the
block's instruction; G5 runs after this handback is written and before C4 is committed, and its
readings go in the final reply, not here. No worktree was added or removed this round; every
worktree named in constraint 7 (`f015-r*`, `f020-r*`, `f023-r*`, `f284-r*`, `job-*`, and the
reviewer's own `f024-r8-sim`/`f024-r8-dry`, plus rounds 1 through 7's dry/sim worktrees) was left
untouched. No `git stash` was used, nothing was merged, no force-push occurred. The pull request
this handback names by its future package pins does not yet exist when this handback is written,
and its number is deliberately not named here (block C4 instruction); it is reported in the final
reply only, per G6.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 354 insertions, matches block's expectation exactly (194+160); well under the 500-insertion STOP threshold |
| C2 | done | ledger.diff apply --check and apply both exit 0; 2/0, 7/6 insertions/deletions match exactly |
| C3 | done | rotation script output matches G3 table line for line; 0/20, 20/0 insertions/deletions match exactly; path set exactly the two ledger files |
| C4 | in progress | closure.diff apply --check and apply both exit 0; 17/2, 1/1 insertions/deletions match exactly; this handback is being written now, per the block's ordering (G4 before the handback, G5 after) |
| G1 | done | all 5 payload digests and 6 authored-copy comparisons matched |
| G2 | done | both named file digests matched; Gate-line count 1 and open-id set R-1008 both matched |
| G3 | done | rotation output and both post-rotation file digests matched |
| G4 | done | STATUS.md/README.md digests matched; status-line count 1; pytest exit 0 (437 passed, 1 skipped, golden path included per the block's own command); integrity check 6/6 pass; integrity block 7/7 OK |
| G5 | pending | reported in the final reply, run after this handback is written and before C4 is committed |
| G6 | pending | reported in the final reply, since C4 has not yet happened when this handback is written |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the Open PR Gate — the pull request this round
opens is merged by the NEXT feature's session, never by this one. Then Rule A5, the first unchecked
feature in `docs/roadmap/STATUS.md`. Open findings: 1. Operator questions open: 3.
