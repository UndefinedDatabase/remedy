# Handback — F020 Node lifecycle & glyph language · Round 5

## Session

SESSION 1 of feature F020 · round 5 · rounds so far 5

This round booked round 4's PASS into the live review record, recorded DECISION F020 D5, and
landed T003's second half: `renderers/glyphConformance.ts`, which places a pixel probe on every
discriminating detail of every matrix cell (the status dot and its outline, the strike and its
outline, the planned ring) and on every place the dot and strike must NOT be, with the binding
spec it judges against and the pixel judge; its vitest tests; and the committed headless harness
`.agent/authored/f020-r5-conformance_*` that paints the matrix with the live painter, reads each
probe's pixel and applies the judge. All nine commits landed in the block's ordered sequence; all
five gates passed with exact matches to the reviewer's stated readings, with no deviations. I had
ample context remaining throughout this round; no session-limit pressure at any point.

## Range

Review of 106df185..HEAD

## Commits

### 78036fca3 F020 R5 C1a: copy round 5 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r5-block.md | +257/-0 | copy of this round's block, verbatim |
| .agent/authored/f020-r5-plan.md | +32/-0 | copy of the plan.md payload |

289 insertions by `git show --numstat` (block's 257 lines + 32); matches the block's expectation
exactly; under the 500-insertion cap.

### 932000751 F020 R5 C1b: copy round 5 diff and red-proof tools into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r5-book.diff | +58/-0 | copy of the book.diff payload |
| .agent/authored/f020-r5-harness_redproof.py | +70/-0 | copy of the harness_redproof.py payload (G5 tool) |
| .agent/authored/f020-r5-mutations.py | +163/-0 | copy of the mutations.py payload (G5 tool) |

291 insertions by `git show --numstat`; matches the block's expectation of 291 exactly.

### 692d159a7 F020 R5 C1c: commit the glyph conformance harness into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r5-conformance_drive.mjs | +79/-0 | copy of the conformance_drive.mjs payload |
| .agent/authored/f020-r5-conformance_index.html | +10/-0 | copy of the conformance_index.html payload |
| .agent/authored/f020-r5-conformance_main.tsx | +46/-0 | copy of the conformance_main.tsx payload |
| .agent/authored/f020-r5-conformance_measure.py | +190/-0 | copy of the conformance_measure.py payload (the harness entry point) |
| .agent/authored/f020-r5-conformance_vite.config.mjs | +28/-0 | copy of the conformance_vite.config.mjs payload |

353 insertions by `git show --numstat`; matches the block's expectation of 353 exactly.

### dfa991abe F020 R5 C1d: copy round 5 conformance module and its tests into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r5-glyphConformance.ts | +146/-0 | copy of the glyphConformance.ts payload |
| .agent/authored/f020-r5-glyphConformance.test.ts | +130/-0 | copy of the glyphConformance.test.ts payload |

276 insertions by `git show --numstat`; matches the block's expectation of 276 exactly.

### 92a9f9a69 F020 R5 C2: book round 4's PASS, record D5, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +40/-0 | DECISION F020 D5 appended (book.diff) |
| .agent/live_review.md | +2/-0 | F020 R4 Gate entry appended (book.diff) |
| .agent/plan.md | +11/-9 | rewritten to the plan.md payload |

`git apply --check` on book.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 40 decisions.md, 2 live_review.md, 11 plan.md — matches the block's expectation
exactly; aggregate 53 insertions(+)/9 deletions(-), all deletions attributable to plan.md's
rewrite diff.

### 7ad336105 F020 R5 C3: probe every discriminating detail of the matrix fixture against the binding spec
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/renderers/glyphConformance.ts | +146/-0 | new file: the pixel probe placement over every matrix cell, the binding spec and the pixel judge |

`git add` fires per the block's instruction (an untracked module fails integrity check's
`relevant_untracked`). Insertions by `git show --numstat`: 146 — matches the block's expectation
exactly.

### 59ada189e F020 R5 C4: pin the probes, the binding spec and the pixel judge
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/renderers/glyphConformance.test.ts | +130/-0 | new file: vitest goldens for glyphConformance.ts |

`git add` fires per the block's instruction. Insertions by `git show --numstat`: 130 — matches
the block's expectation exactly.

### c04efc17e F020 R5 C4e: commit the glyph conformance transcript
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r5-conformance.txt | +28/-0 | G4's harness-run transcript, stdout then stderr, saved whole |

28 insertions by `git show --numstat`; the block does not predict this count (the transcript
carries process ids), and it is reported here as measured.

### (this commit) F020 R5 C5: rewrite handoff for round 5
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f020-r5-mut 59ada189e` — outcome: success, detached HEAD
  at `59ada189e`.
- `git worktree remove --force .remedy-wt/f020-r5-mut` — outcome: success.
- `git worktree prune` — outcome: success, no output.
- `git push origin feature/f020-node-lifecycle-glyph-language` — runs AFTER this commit lands;
  its real outcome is reported in the reply, since this handback cannot contain an outcome that
  happens after it. No `gh pr create` this round: the block forbids it (constraint 5).

## Verification

```
$ ls .agent/STOP
ls: cannot access '/home/decodeux/Repos/remedy/.agent/STOP': No such file or directory (absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f020-node-lifecycle-glyph-language
$ git log --oneline -1
106df1853 F020 R4 C5: rewrite handoff for round 4
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ wc -l / sha256sum .remedy-wt/f020-r5/block.md
257 lines, sha256=c21f1840acc68d546a76c66749d7631ef8f11f68c3c6c5e96520b88da3047288
```
Matches both readings given in the delegation message exactly (R-0954).

```
$ line count / byte count / sha256 over .remedy-wt/f020-r5-payloads/*
book.diff                     lines=58  bytes=11570 sha256=651525a6621e886722910faf98992ddc49fd9aaf4661c19696a721120d552959
conformance_drive.mjs         lines=79  bytes=3145  sha256=71bfca163f677088315a623242874588666ceb049da55d6760dadf4986981e74
conformance_index.html        lines=10  bytes=202   sha256=941439e425ecc1554e6ca5daadd5b47476ae85eba1d7c5c6b821b62cd3e104a6
conformance_main.tsx          lines=46  bytes=2186  sha256=d287fefb13acb92c1d8a3a999d472780b16ecbb34475ccb08ad1333dda017a7b
conformance_measure.py        lines=190 bytes=6529  sha256=34b1e5c3cfffb16d657f2e7e7fa8224f86afcc8f87705bc1345e2a0bc96f4d34
conformance_vite.config.mjs   lines=28  bytes=775   sha256=e072fd9ed0ee4eb0efc58a396c8c2149ae64f9235313f28543081897de8f09f8
glyphConformance.test.ts      lines=130 bytes=6597  sha256=844d757a1398b77ff7bd1674a2be65ec06087d61ec15a429d575b5aae3bf280d
glyphConformance.ts           lines=146 bytes=7207  sha256=bb9731ebce8b857cbef6198fca8189277e5a5880352aff1f6e08879ad5903436
harness_redproof.py           lines=70  bytes=3651  sha256=4169214620acf737c668d4b90d8f6dbdef70af9364eb7175980f787222215e43
mutations.py                  lines=163 bytes=7894  sha256=a24543f8bf80ea3c3a6c2b70058392524beeb0655ec0c0f0625d3f88748e66ea
plan.md                       lines=32  bytes=1169  sha256=e4bc66c01f99a95f829b9e0a8dd581471cccb42de7b246df8c2e9d720e193448
```
All 11 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f020-r5-* blob, read with `git show <commit>:<path>`,
   against its source)
f020-r5-block.md                    @ 78036fca3: match=True
f020-r5-plan.md                     @ 78036fca3: match=True
f020-r5-book.diff                   @ 932000751: match=True
f020-r5-mutations.py                @ 932000751: match=True
f020-r5-harness_redproof.py         @ 932000751: match=True
f020-r5-conformance_drive.mjs       @ 692d159a7: match=True
f020-r5-conformance_index.html      @ 692d159a7: match=True
f020-r5-conformance_main.tsx        @ 692d159a7: match=True
f020-r5-conformance_measure.py      @ 692d159a7: match=True
f020-r5-conformance_vite.config.mjs @ 692d159a7: match=True
f020-r5-glyphConformance.ts         @ dfa991abe: match=True
f020-r5-glyphConformance.test.ts    @ dfa991abe: match=True
```
All 12 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2's three files, read with `git show 92a9f9a69:<path>`, against the block's G2 table)
.agent/live_review.md: bytes=298389  sha256=4e85f5dd1850b7c234aa36835532ec3197d0bb2e015433f2cf63ec5e60f5d18c match=True
.agent/decisions.md:   bytes=2043706 sha256=22db38d10317587eff5f2230e11788eaad340b8d2ae777eac92e946e536d2221 match=True
.agent/plan.md:        bytes=1169    sha256=e4bc66c01f99a95f829b9e0a8dd581471cccb42de7b246df8c2e9d720e193448 match=True
```
All 3 match the block's G2 table exactly.

```
$ git diff 92a9f9a69^ 92a9f9a69 -- .agent/live_review.md, counting added lines starting
  "Gate: F020 R4 — "
count = 1
```
Matches the reviewer's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT at C2
92a9f9a69 (C2) open ids: ['R-1008']
```
Reads R-1008 alone, matching the reviewer's stated reading exactly (G2).

```
$ git diff --name-only dfa991abe 92a9f9a69
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Exactly the three paths the block's G2 table names (G2).

```
$ (sha256/bytes of C3/C4 files, read with `git show <commit>:<path>`, against the block's G3 table)
C3 apps/ui/src/components/graph/renderers/glyphConformance.ts:      bytes=7207 sha256=bb9731ebce8b857cbef6198fca8189277e5a5880352aff1f6e08879ad5903436 match=True
C4 apps/ui/src/components/graph/renderers/glyphConformance.test.ts: bytes=6597 sha256=844d757a1398b77ff7bd1674a2be65ec06087d61ec15a429d575b5aae3bf280d match=True
```
Both match the block's G3 table exactly.

```
$ git diff --name-only 92a9f9a69 7ad336105
apps/ui/src/components/graph/renderers/glyphConformance.ts
$ git diff --name-only 7ad336105 59ada189e
apps/ui/src/components/graph/renderers/glyphConformance.test.ts
```
Both name exactly the one path each of C3 and C4 (G3).

```
$ python3 -m ruff check .agent/authored/f020-r5-conformance_measure.py
  .agent/authored/f020-r5-harness_redproof.py .agent/authored/f020-r5-mutations.py
All checks passed!
REAL_EXIT=0
```

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts
  tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
  tests/orchestration/test_block_lint.py tests/regression/test_named_bugs.py
  tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -60; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1174 passed, 11 skipped in 73.51s (0:01:13)
REAL_EXIT=0
```
None of the 11 SKIPPED lines are the four toolchain nodes the block names (the two
`tests/ui_contracts/test_ui_lint.py` eslint checks, the tsc node in
`tests/ui_server/test_dashboard_contract.py`, the vitest node in
`tests/orchestration/test_test_runner.py`, which runs the UI's whole unit suite including this
round's new `glyphConformance.test.ts`) — all four ran and PASSED in the primary checkout, not
skipped, as required. The 11 remaining skips are pre-existing D3/D12 quarantines unrelated to
this round's paths, consistent with round 4's same reading at the same commit count.

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
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0 (G4).

```
$ python3 .agent/authored/f020-r5-conformance_measure.py /home/decodeux/Repos/remedy
repo root: /home/decodeux/Repos/remedy
work dir: /home/decodeux/Repos/remedy/.remedy-wt/f020-conformance-run
+ vite build
vite v6.4.2 building for production...
transforming...
✓ 13 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                 0.30 kB │ gzip: 0.22 kB
dist/assets/index-DFNYlH4h.css  2.39 kB │ gzip: 0.84 kB
dist/assets/index-D18QW5Bv.js   9.99 kB │ gzip: 3.66 kB
✓ built in 99ms

server pid: 4067204
chrome pid: 4067216
+ node drive.mjs
MISSING TOKENS: none
PASSED ring/mark: 8 present, 0 absent
PASSED status_dot/mark: 16 present, 40 absent
PASSED status_dot/outline: 16 present, 0 absent
PASSED strike/mark: 8 present, 48 absent
PASSED strike/outline: 8 present, 0 absent
CONFORMANCE: 144 of 144 probes pass

chrome pid 4067216 stopped (SIGTERM)
server pid 4067204 stopped (SIGTERM)
removed work dir: /home/decodeux/Repos/remedy/.remedy-wt/f020-conformance-run
drive.mjs exit code: 0
REAL_EXIT=0
```
stderr: empty. Every line the block quoted (`MISSING TOKENS: none`, all five `PASSED` lines,
`CONFORMANCE: 144 of 144 probes pass`, `drive.mjs exit code: 0`) matches verbatim; no `FAILED` or
`EXCEPTION` line printed, matching the reviewer's reading of none (G4). This stdout+stderr
transcript is committed whole at C4e as `.agent/authored/f020-r5-conformance.txt` (28 insertions).

```
$ git worktree add --detach .remedy-wt/f020-r5-mut 59ada189e
Preparing worktree (detached HEAD 59ada189e)
REAL_EXIT=0

$ python3 -B .agent/authored/f020-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f020-r5-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f020-r5-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=12 | guard exit=0 failed=0 passed=8
m1 (the spec drops the failed state's dot): vitest exit=1 failed=2 passed=10 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m2 (the dot is probed off its centre): vitest exit=1 failed=2 passed=10 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m3 (the strike's outline is probed on the strike itself): vitest exit=1 failed=1 passed=11 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m4 (a missing ring is probed too): vitest exit=1 failed=2 passed=10 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m5 (the probes ignore the state's size factor): vitest exit=1 failed=1 passed=11 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m6 (a function colour's alpha is read unscaled): vitest exit=1 failed=1 passed=11 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m7 (the tolerance excludes its own bound): vitest exit=1 failed=1 passed=11 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m8 (an unpainted pixel counts as a colour): vitest exit=1 failed=1 passed=11 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m9 (an absent probe passes when the colour shows): vitest exit=1 failed=1 passed=11 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m10 (an unresolved token passes): vitest exit=1 failed=1 passed=11 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m11 (the strike is judged in the failure red): vitest exit=1 failed=1 passed=11 | guard exit=0 failed=0 passed=8 | caught=True restored byte-identical=True
m12 (a raw colour literal enters the conformance module): vitest exit=0 failed=0 passed=12 | guard exit=1 failed=1 passed=7 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=12 | guard exit=0 failed=0 passed=8
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every (v, g) pair matches the block's stated reading exactly: control 12v/8g both exit 0; m1 v2g0;
m2 v2g0; m3 v1g0; m4 v2g0; m5-m11 v1g0; m12 v0g1; control last equals control first; every
`restored byte-identical` True; final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`
(G5a).

```
$ python3 -B .agent/authored/f020-r5-harness_redproof.py
  /home/decodeux/Repos/remedy/.remedy-wt/f020-r5-mut
  /home/decodeux/Repos/remedy/.agent/authored/f020-r5-conformance_measure.py
control first: exit 0, CONFORMANCE: 144 of 144 probes pass, FAILED lines 0
h1 (a failed node loses its status dot): exit 1, CONFORMANCE: 133 of 144 probes pass, FAILED lines 11
h1: red=True restored byte-identical=True
h2 (the painter draws marks without their outline): exit 1, CONFORMANCE: 120 of 144 probes pass, FAILED lines 24
h2: red=True restored byte-identical=True
h3 (the open state carries the strike too): exit 1, CONFORMANCE: 136 of 144 probes pass, FAILED lines 8
h3: red=True restored byte-identical=True
h4 (the status dot is drawn at the top left): exit 1, CONFORMANCE: 122 of 144 probes pass, FAILED lines 22
h4: red=True restored byte-identical=True
control last: exit 0, CONFORMANCE: 144 of 144 probes pass, FAILED lines 0
ALL HARNESS MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every reading matches the block's stated reading exactly: control first/last both 144 of 144 at
exit 0; h1 133/144 exit 1; h2 120/144 exit 1; h3 136/144 exit 1; h4 122/144 exit 1; every
`restored byte-identical` True; final line `ALL HARNESS MUTATIONS CAUGHT AND RESTORED CLEANLY:
True` (G5b).

```
$ git worktree remove --force .remedy-wt/f020-r5-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
```

## Authored-text proofs

All 12 authored copies under `.agent/authored/f020-r5-*` (the block copy plus the eleven payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <commit>:<path>` and compared byte for byte against its source:
all 12 BYTE-IDENTICAL (G1 above). `book.diff` was applied with `git apply` after `git apply
--check` passed (exit 0 both), never retyped or edited; the resulting files were verified by byte
count and sha256 against the block's G2 table — all MATCH. `.agent/plan.md` was rewritten whole
via `shutil.copyfile` from the payload source — never retyped — and confirmed MATCH against the
PAYLOADS table and the G2 table. `glyphConformance.ts` and `glyphConformance.test.ts` were each
copied whole via `shutil.copyfile` into their product/test locations and confirmed MATCH against
the block's G3 table. `mutations.py` and `harness_redproof.py` were run unmodified from their
`.agent/authored/f020-r5-*` paths against the fresh `.remedy-wt/f020-r5-mut` worktree; their
printed output was reported verbatim and matches the block's stated G5 readings exactly. The
harness run's stdout and stderr (captured to scratch files under
`.remedy-wt/f020-r5-worker/`, never edited) were concatenated stdout-then-stderr into
`.agent/authored/f020-r5-conformance.txt` at C4e via direct byte writes from the captured files
— never retyped.

## Deviations & assumptions

None. Every commit landed in the block's stated order C1a, C1b, C1c, C1d, C2, C3, C4, C4e, C5,
exactly as ordered. G1 through G5 ran before this handback was written, as the block orders (G4
at C4, before C4e, as required). No payload was edited, retyped or repaired. The round's tracked
path set matches constraint 3 (full list reported in the reply via `git diff --name-only 106df185
HEAD` after this commit, since that reading is taken after C5 lands). Nothing was merged this
round: no `gh pr merge`, no `gh pr create`, no checkout of `main` after the branch was cut, no
branch deletion, no force-push, no `git stash` — per constraint 5. The reviewer's worktrees, the
`f015-r*`/`f284-r*` worktrees and the `job-*` worktrees/branches were left untouched — per
constraint 6. The full test suite was not run — per constraint 7.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 289 insertions, matches block's expectation exactly; under the 500-insertion cap |
| C1b | done | 291 insertions, matches block's expectation exactly |
| C1c | done | 353 insertions, matches block's expectation exactly |
| C1d | done | 276 insertions, matches block's expectation exactly |
| C2 | done | book.diff apply --check and apply both exit 0; 40/2/11 insertions, matches; D5 recorded |
| C3 | done | 146 insertions, matches block's expectation exactly; module added under relevant_untracked |
| C4 | done | 130 insertions, matches block's expectation exactly |
| C4e | done | 28 insertions as measured (transcript carries process ids, not predicted by the block) |
| C5 | done | committing now with this handback |
| G1 | done | all 11 payload digests and 12 authored-copy comparisons matched |
| G2 | done | all 3 named file digests matched; gate-line count 1; open set R-1008 alone; C1d..C2 path set exact |
| G3 | done | both named file digests matched; C2..C3 and C3..C4 path sets exact; ruff clean |
| G4 | done | 1174 passed, 11 skipped at exit 0; all 4 named toolchain nodes ran and passed (not skipped); integrity check 6/6 pass; harness exit 0, all 7 quoted lines matched verbatim, no FAILED/EXCEPTION |
| G5 | done | 12 mutations + 2 controls (mutations.py) and 4 harness mutations + 2 controls (harness_redproof.py) all matched the block's stated readings exactly; both final lines True |
| G6 | pending | runs after this commit (tree/log check, worktree list, push, `gh pr list`); reported in the reply |
| PUSH | pending | `git push origin feature/f020-node-lifecycle-glyph-language`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 5. Then the closure
sequence's first round — the Built State, the checklist consolidation, the self-use track and
the one full suite. Open findings: 1. Operator questions open: 3.
