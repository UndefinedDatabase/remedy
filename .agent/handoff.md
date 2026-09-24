# Handback — F019 Live node materialization · Round 6 (book round 5 + finish T003)

## Session

SESSION 2 of feature F019 · round 6 · rounds so far 6

This round books round 5's PASS, records DECISION F019 D6, and finishes
T003: the committed performance fixture `brainPerfFixture.ts` with its
vitest test, the end-to-end test `test_brain_demo_recording_live.py`
checking a live fake job against the demo recording, one line naming the
fixture in `docs/roadmap/features/T5_F044.md`, red proofs, and the
stage-1 frame budget measured on the fixture with the reviewer's
measurement tool, kept as evidence under `.agent/authored/`. I had ample
context remaining throughout this round; no session-limit pressure at any
point.

## Range

Review of 22f3fe999..HEAD

## Commits

### f8806d599 F019 R6 C1a: copy round 6 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r6-block.md | +189/-0 | copy of this round's block, verbatim |
| .agent/authored/f019-r6-plan.md | +34/-0 | copy of the plan.md payload |

223 insertions by `git show --numstat` (block's 189 lines + 34); matches
the block's expectation exactly; under the 500-insertion cap.

### 971fd9840 F019 R6 C1b: copy round 6 records, product and tests diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r6-product.diff | +167/-0 | copy of the product.diff payload |
| .agent/authored/f019-r6-records.diff | +61/-0 | copy of the records.diff payload |
| .agent/authored/f019-r6-tests.diff | +253/-0 | copy of the tests.diff payload |

481 insertions by `git show --numstat`; matches the block's expectation
(481) exactly.

### 20dcfa28c F019 R6 C1c: copy round 6 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r6-mutations.py | +295/-0 | copy of the mutations.py payload |

295 insertions by `git show --numstat`; matches the block's expectation
exactly.

### 5fafe9b84 F019 R6 C1d: copy round 6 frame-rate measurement tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r6-perf-drive_chrome.mjs | +127/-0 | copy of perf/drive_chrome.mjs |
| .agent/authored/f019-r6-perf-index.html | +14/-0 | copy of perf/index.html |
| .agent/authored/f019-r6-perf-main.tsx | +119/-0 | copy of perf/main.tsx |
| .agent/authored/f019-r6-perf-measure.py | +191/-0 | copy of perf/measure.py |
| .agent/authored/f019-r6-perf-vite.config.mjs | +28/-0 | copy of perf/vite.config.mjs |

479 insertions by `git show --numstat`; matches the block's expectation
exactly.

### 7269f5c18 F019 R6 C2: book round 5's PASS, record DECISION F019 D6
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +43/-0 | DECISION F019 D6 appended |
| .agent/live_review.md | +2/-0 | `Gate: F019 R5 —` entry appended |
| .agent/plan.md | +10/-10 | rewritten to the plan.md payload (round 6 scope) |

`git apply --check` on records.diff: exit 0. `git apply`: exit 0.
Insertions/deletions by `git show --numstat`: 43/0 decisions.md, 2/0
live_review.md, 10/10 plan.md — matches the block's expectation exactly
on every file.

### d20d9bbb9 F019 R6 C3: add the frame-budget fixture and name it in F044's file
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainPerfFixture.ts | +144/-0 | new file, the committed performance fixture |
| docs/roadmap/features/T5_F044.md | +6/-0 | one bullet naming the fixture |

144/0, 6/0 insertions/deletions by `git show --numstat`; matches the
block's expectation exactly on every file. `git apply --check` then `git
apply` on product.diff: exit 0 both. `brainPerfFixture.ts` was `git add`ed
before commit (no untracked product file at commit time).

### b7d351d53 F019 R6 C4: check a live fake job against the demo recording, pin the fixture
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainPerfFixture.test.ts | +65/-0 | new file, pins the fixture |
| tests/ui_server/test_brain_demo_recording_live.py | +176/-0 | new file, checks a live fake job against the demo recording |

65/0, 176/0 insertions/deletions by `git show --numstat`; matches the
block's expectation exactly on every file. `git apply --check` then `git
apply` on tests.diff: exit 0 both. Both new test files were `git add`ed
before commit.

### (this commit) F019 R6 C5: rewrite handoff for round 6
This file, rewritten, its own commit — self-reference exception per the
handback template (a handback cannot table the commit that writes it).

## External actions

- `git worktree add --detach .remedy-wt/f019-r6-mut b7d351d53` (G5) — real
  outcome: `Preparing worktree (detached HEAD b7d351d53)`, `HEAD is now at
  b7d351d53`.
- `git worktree remove --force .remedy-wt/f019-r6-mut` (G5, after the
  mutation sweep) — real outcome: exit 0, no output.
- `git worktree prune` (G5) — real outcome: exit 0, no output.
- `git push origin feature/f019-live-node-materialization` runs after
  this handback is committed; its real outcome is reported in the reply
  only, per G6.
- No `gh pr` command of any kind this round. No checkout of `main`, no
  branch deletion, no force-push, no `git stash`.

## Verification

G1 TRANSPORT — all 10 payloads measured against the block's PAYLOADS
table, all matched (line count, byte count, sha256):
```
records.diff          lines=61  bytes=10720 sha256=b04bb2ea3debc6bd2eb2f8ac31143492a5df80e23b26ee91c431985542cb5403
plan.md                lines=34  bytes=1403  sha256=a03a038cf49858201e514d2bc35fdd4d9b157db1e018f6fb3148415f07bbd4a8
product.diff            lines=167 bytes=8473  sha256=137375662f2e0328acd402d454c3e5d12847304b2e52407137d268278285ec3e
tests.diff              lines=253 bytes=10283 sha256=eb7e3c8ae58dba663f31b4ab6b8a81db5f54f47bc9b1a2961f8cc0fda0cf4456
mutations.py            lines=295 bytes=11928 sha256=a8eee80e81b94c7341874813a0739c342fda7d2e119c0308f60b321a7074644a
perf/measure.py         lines=191 bytes=6512  sha256=b5f38fd7112f0ffb787424fc18d585d5db05e8e9290e06ec70191490e2a8e4f9
perf/index.html         lines=14  bytes=351   sha256=36c417978e86247aa68b70efdad66f35d0cf22e8e10ec4aa2dcdd3830c95a6cc
perf/main.tsx           lines=119 bytes=3814  sha256=3a9721713b9daa476dbfd3515a4c5ed0ca0b56b96d1e1107ead9ead996dae1c4
perf/vite.config.mjs    lines=28  bytes=766   sha256=82b2d0f857c6821f6136d323d41d43ad94e6e4993ff192f17ee5425f9a74c6a9
perf/drive_chrome.mjs   lines=127 bytes=4459  sha256=6b8886d2b1f5367e9f2b9690234531ad2c6fa657475061902d760c74c09c7438
ALL PAYLOAD DIGESTS MATCH: True
```
Each `.agent/authored/f019-r6-*` copy, read back with `git show
<commit>:<path>` from the commit that added it, matched its source byte
for byte (11 comparisons: the block copy against
`.remedy-wt/f019-r6/block.md`, plus the 10 payload copies) —
`ALL_TRANSPORT_OK: True`.

G2 THE BOOKING — at C2 (`7269f5c18`), `.agent/decisions.md` read 2015857
bytes, sha256 `a0b68b8aadc2a67353828c72f736943cefc5966c9448215ae1a8aa3de32a1fdd`
(MATCH); `.agent/live_review.md` read 317737 bytes, sha256
`cb0f8c063c8305f17320069dbafdc1160f28100d64d136544ca630c50a43da73` (MATCH);
`.agent/plan.md` at C2 read 1403 bytes, sha256
`a03a038cf49858201e514d2bc35fdd4d9b157db1e018f6fb3148415f07bbd4a8` (MATCH,
equal to the plan.md payload). The count of lines C2 adds to the ledger
beginning `Gate: F019 R5 — ` is 1 (measured over C2's
`.agent/live_review.md`). `open_finding_ids` (`scripts/rotate_live_review.py`)
over `.agent/live_review.md`: at `22f3fe999` → `['R-0499', 'R-0950',
'R-1008', 'R-1046']`; at C2 (`7269f5c18`) → the same four — matches the
reviewer's reading exactly at both.

G3 THE PRODUCT AND TESTS — at C4 (`b7d351d53`), the byte count and sha256
of all 4 named files, read with `git show b7d351d53:<path>`, matched the
reviewer's simulated reading exactly:
```
apps/ui/src/components/graph/brainPerfFixture.ts        7263 bytes  MATCH
docs/roadmap/features/T5_F044.md                        5327 bytes  MATCH
apps/ui/src/components/graph/brainPerfFixture.test.ts   2691 bytes  MATCH
tests/ui_server/test_brain_demo_recording_live.py       6838 bytes  MATCH
```

G4 THE TESTS — real transcript, primary checkout, at C4:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_demo_recording_live.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md deleted deliberately
1428 passed, 5 skipped in 66.88s (0:01:06)
REAL_EXIT=0
```
All 5 SKIPPED lines are pre-existing D3/D12 quarantine skips, unrelated to
the toolchain or to the new test file. The two eslint nodes of
`test_ui_lint.py`, the tsc node of `test_dashboard_contract.py`, and the
vitest node of `test_test_runner.py` do not appear in the skip list — each
ran and PASSED, as the block requires for the primary checkout. (The
reviewer's sim-tree run, without the golden path, read `1381 passed, 10
skipped`; the primary-checkout difference — 47 more passed, 5 fewer
skipped — is the golden-path suite plus those toolchain nodes running here
instead of skipping.)
```
$ python3 -m ruff check tests/ui_server/test_brain_demo_recording_live.py
All checks passed!
REAL_EXIT=0
```
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0. `git status --porcelain` immediately
after: empty.

G5 THE RED PROOFS AND THE MEASUREMENT — worktree `.remedy-wt/f019-r6-mut`
added detached at C4 (`b7d351d53`), then `python3 -B
.remedy-wt/f019-r6-payloads/mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f019-r6-mut`:
```
CONTROL RUN #1 (unmutated, before any mutation) — both runners
  [vitest] exit_code=0 failed=0 passed=134
  [pytest] exit_code=0 failed=0 passed=1
F1: the fixture's stage-1 constant becomes 199 — [vitest] exit=1 failed=2 passed=132, restored byte-identical: True
F2: the generator leaves no builder run in progress (no active link) — [vitest] exit=1 failed=6 passed=128, restored byte-identical: True
F3: the generator skips task_run_completed for every task (lastSeq changes) — [vitest] exit=1 failed=2 passed=132, restored byte-identical: True
P1: one outcome in brainDemoRecording.ts changed from "pass" to "fail" (seq 3) — [vitest] exit=1 failed=2 passed=132, [pytest] exit=1 failed=1 passed=0 (test_live_fake_job_renders_identically_to_the_demo_recording), restored byte-identical: True
P2: one recorded task label changed — [vitest] exit=1 failed=2 passed=132, [pytest] exit=1 failed=1 passed=0 (test_live_fake_job_renders_identically_to_the_demo_recording), restored byte-identical: True
CONTROL RUN #2 (unmutated, after the full sweep) — both runners
  [vitest] exit_code=0 failed=0 passed=134
  [pytest] exit_code=0 failed=0 passed=1
control #1 green (all runners): True
control #2 green (all runners): True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every failed-count matches the reviewer's prototype-tree reading exactly
(F1 vitest 2, F2 vitest 6, F3 vitest 2, P1 vitest 2 + pytest 1, P2 vitest
2 + pytest 1), both controls read `134 passed` vitest / `1 passed` pytest
at exit 0 first and last, every restore read byte-identical True, and the
final line reads `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. `git
worktree remove --force .remedy-wt/f019-r6-mut` and `git worktree prune`
both exit 0.

THE MEASUREMENT, primary checkout, at C4:
```
$ python3 .remedy-wt/f019-r6-payloads/perf/measure.py /home/decodeux/Repos/remedy
{"requestedN":200,"runIndex":1,...,"frames":481,"meanFps":60,"p50Ms":16.7,"p95Ms":16.8,...}
{"requestedN":200,"runIndex":2,...,"frames":481,"meanFps":60,"p50Ms":16.7,"p95Ms":16.8,...}
{"requestedN":200,"runIndex":3,...,"frames":481,"meanFps":60,"p50Ms":16.7,"p95Ms":16.7,...}
{"requestedN":500,"runIndex":1,...,"frames":481,"meanFps":60,"p50Ms":16.7,"p95Ms":16.7,...}
{"requestedN":500,"runIndex":2,...,"frames":481,"meanFps":60,"p50Ms":16.7,"p95Ms":16.8,...}
{"requestedN":500,"runIndex":3,...,"frames":482,"meanFps":60,"p50Ms":16.7,"p95Ms":16.8,...}
BUDGET stage1 200 nodes: p95 16.8 ms, mean 60 fps, PASS
REAL_EXIT=0
```
Six runs, three at 200 nodes and three at 500 nodes, matching the
reviewer's shape exactly: 481 frames on five of six runs (one 500-node run
read 482, within the block's stated frame/millisecond tolerance), mean 60
fps on every run, p50 16.7 ms on every run, p95 16.7–16.8 ms — all at most
16.8 ms as the block requires. The final budget line reads verbatim
`BUDGET stage1 200 nodes: p95 16.8 ms, mean 60 fps, PASS`, matching the
reviewer's reading exactly; `REAL_EXIT=0`. `git worktree list` afterward
shows no `f019-r6-mut` entry, only the primary checkout, the pre-existing
`f015-r*` worktrees, `f019-r2-sim`, `f019-r3-proto`, `f019-r3-sim`,
`f019-r4-proto`, `f019-r4-sim`, `f019-r5-proto`, `f019-r5-sim`,
`f019-r6-proto`, `f019-r6-sim` and the four `job-*` worktrees — all named
by the block's constraint 6, nothing else. `ls .remedy-wt/f019-perf-run`
reads "No such file or directory" — the measurement tool removed its own
work dir as its last action.

G6 — reported in the reply per the block's own instruction (measured
after this handback is written, committed and pushed).

## Authored-text proofs

All 11 authored copies under `.agent/authored/f019-r6-*` (the block copy
plus the 10 payload copies) were built by reading each source's bytes with
`shutil.copyfile` and writing them unedited — never retyped, never
edited. Each was read back from the commit that added it with `git show
<commit>:<path>` and compared byte for byte against its source: all 11
`BYTE-IDENTICAL` (G1 above). `records.diff` was applied with `git apply`
after `git apply --check` passed (exit 0 both), never retyped or edited;
its resulting file contents (`.agent/decisions.md`, `.agent/live_review.md`)
were verified by byte count and sha256 against the reviewer's own
readings at C2 (G2 above) — both `MATCH`; `.agent/plan.md` was separately
rewritten whole via `shutil.copyfile` from its payload and also confirmed
`MATCH`. `product.diff` was applied the same way (`git apply --check`
then `git apply`, both exit 0), never retyped or edited; `tests.diff`
likewise. The four resulting product/test files' C4 contents were
confirmed `MATCH` against the reviewer's simulated reading in G3 above.
`mutations.py` and the five `perf/*` files were copied into
`.agent/authored/` (G1, matched) and run unedited from their payload
location in G5; none was ever applied to a tracked file, per the block's
instruction that they are TOOLS only.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1a, C1b, C1c,
C1d, C2, C3, C4, then this handback as C5), all gates G1–G5 ran before C5
as ordered, and no payload was edited, retyped or repaired. The round's
tracked path set matches constraint 3: `git diff --name-only 22f3fe999
HEAD` (measured just before writing this handback, i.e. through C4) names
the ten `.agent/authored/f019-r6-*` copies, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/plan.md`, and the four files the
product/test diffs name — this handoff's own path is added by C5 itself.
No full-suite run was made (amend0917 rule 1; F019's belongs to its
closure). No `.agent/context.md`, `.agent/prose_slips.md`,
`.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
`docs/roadmap/STATUS.md` or `docs/roadmap/features/T5_F019.md` was
touched, matching this round's scope.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 223 insertions, matches (189 block + 34 plan.md) |
| C1b | done | 481 insertions, matches |
| C1c | done | 295 insertions, matches |
| C1d | done | 479 insertions, matches |
| C2 | done | git apply --check and apply both exit 0; 43/2/10-10 insertions/deletions, matches every file |
| C3 | done | 144/0, 6/0 insertions/deletions, matches; diff applied clean; brainPerfFixture.ts tracked before commit |
| C4 | done | 65/0, 176/0 insertions/deletions, matches; tests.diff applied clean; both test files tracked before commit |
| C5 | done | this handback, rewritten per docs/agents/handback_template.md |
| G1 | done | all 10 payload digests and 11 authored-copy comparisons matched |
| G2 | done | decisions.md/live_review.md/plan.md byte counts and sha256 matched; 1 new Gate line; open_finding_ids correct at both commits |
| G3 | done | all 4 product/test file digests matched at C4 |
| G4 | done | 1428 passed, 5 skipped (all pre-existing quarantine, none toolchain), exit 0; ruff clean; integrity check all 6 pass, fail_count 0 |
| G5 | done | all 5 mutations caught, both vitest and pytest controls green, all restores byte-identical, final line True; worktree removed and pruned; measurement PASS, work dir removed |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 6.
Then F019's closure sequence per `docs/roadmap/STATUS_closure_protocol.md`,
T001, T002 and T003 being built. Open findings: 4. Operator questions
open: 3.
