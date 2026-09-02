# Handoff — F108 Tiered artifact summaries (round 10)

## Session

SESSION 3 of feature F108 · round 10 · rounds so far 10 (a fresh Claude Code
session with no memory of sessions 1-2; round 9 was session 2's final round)

## Range

Review of `07749d21`..`HEAD` (branch `feature/f108-tiered-artifact-summaries`).
Pre-flight confirmed HEAD at exactly the branch tip round 9 left it at
(`07749d21`), `git status --porcelain` empty. This round's own commits only.
The bundle landed in full, after one mid-round STOP-and-repair episode on C3
(detailed under Deviations below) — no data was lost, no red state was ever
pushed.

## Commits

### 4ef588a9 F108 R10: save round 10 step block verbatim (C0a)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f108-r10.md` | +260/-0 (new) | C0a — save the step block verbatim (bytes between the BEGIN/END markers, excluding the marker lines) |

### 7f9cdbbb F108 R10: mirror step block to last_block.md (C0b)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +197/-244 (rewrite) | C0b — mirror `.agent/authored/f108-r10.md` byte-for-byte via `cp`; both sha256 identical (`4fc5812c2764e1b773a8a23522151579df9d68279693402d62e5e4081ae98019`) |

### 0bdacaac F108 R10: append SLICE_LEDGER_R10 (Gate F108 R9 + DECISION F108 D6)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +5/-1 | C1 — append SLICE_LEDGER_R10 (two paragraphs: `Gate: F108 R9`, `DECISION F108 D6`), `"\n\n"`-separated, no trailing newline |

### d4f47eb5 F108 R10: end-to-end tiered summaries reduce composed prompt size (T003d)
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_pingpong_cli.py` | +65/-0 | C2 — SPEC S1 imports (`_OVERSIZED_DIFF_THRESHOLD_CHARS`, `_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS`, `_pingpong_runs_dir`, module-qualified `import ... as pingpong_loop`) + SPEC S2 `TestTieredSummariesReduceComposedPromptSize`, driving `run_pingpong` end to end with a monkeypatched `_apply_fake_builder_changes` and `summary_call_fn`, per DECISION F108 D6 |

### 4b9d5b4a F108 R10: rewrite plan.md to SLICE_PLAN_R10
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +7/-14 (rewrite) | C3 — rewrite to SLICE_PLAN_R10's exact bytes (sha256-verified: 35 lines, 1621 bytes, `73785aa588e2084a52589b0762f7fcb52302d5dbe23917c45f8b09d82a97f16f`); applied via mechanical `cp` from the reviewer-supplied scratch file after my own hand-typed attempt mismatched (see Deviations) |

### (pending, this handback's own commit) handoff.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | C4 — this handback |

All 6 declared change-set paths land across this round's 6 commits (C0a,
C0b, C1, C2, C3, C4) — one commit per path, one path per commit, no
bundling this round.

## External actions

- `git worktree add .remedy-wt/f108-r10-mutation HEAD --detach` then
  `git worktree remove .remedy-wt/f108-r10-mutation` — used for G3's
  mutation red-proofs (self_drive_protocol.md G5 isolation). Files were
  edited by ABSOLUTE path inside the worktree; tests were run with
  `python3 -m pytest <absolute-worktree-path>/tests/...` (never `cd` into
  the worktree — `cd`-based invocation into the worktree was tried first
  and denied by the sandbox permission layer, so the absolute-path
  invocation from the primary cwd was used instead, and it correctly
  resolved imports against the worktree's own mutated `pingpong_loop.py`,
  confirmed by the mutated run producing the expected different failure);
  `git status --porcelain` on the PRIMARY checkout was run immediately
  before worktree creation, immediately after each of the two mutating
  edits, and again after worktree removal, and read empty every time — the
  primary checkout was never mutated.
- Mid-round: reviewer independently re-verified the block's own
  SLICE_PLAN_R10 numbers via a scratch file
  `.remedy-wt/scratch/plan_as_sent.md` (1621 bytes, sha256
  `73785aa588e2084a52589b0762f7fcb52302d5dbe23917c45f8b09d82a97f16f`,
  confirmed to match by this worker before use), which was `cp`'d directly
  to `.agent/plan.md` (no retyping) and then deleted by exact path once C3
  was committed and re-verified.
- `git push -u origin feature/f108-tiered-artifact-summaries` — pushes
  this round's commits after this handback commit lands; real result
  reported below.
- No PR created — explicitly out of scope this round (T003b-iii still
  deferred per D4; T003d is now the last open DONE-condition item and is
  closed out by this round's own work).

## Verification

Pre-flight:
```
$ git status --porcelain
(empty)
$ git log --oneline -1
07749d21 F108 R9: rewrite handoff.md for round 9
```
Matches the block's expected branch tip (`07749d21`) exactly.

G1 TRANSPORT:
```
$ sha256sum .agent/authored/f108-r10.md .agent/last_block.md
4fc5812c2764e1b773a8a23522151579df9d68279693402d62e5e4081ae98019  .agent/authored/f108-r10.md
4fc5812c2764e1b773a8a23522151579df9d68279693402d62e5e4081ae98019  .agent/last_block.md
```
IDENTICAL.

G2 LEDGER APPEND:
```
$ wc -c .agent/live_review.md      # AFTER
1989050
$ sha256sum .agent/live_review.md  # AFTER
cf2de0297d9761de40f9a16aeaad46d4739775a917c560a172881f2a8d43e5b2
```
Matches the block's stated result exactly (1989050 bytes, same sha256).
Anchored grep counts:
```
$ grep -c "^Gate: " .agent/live_review.md
226
$ grep -cE "^DECISION F[0-9]+ D[0-9]+ — " .agent/live_review.md
27
$ grep -cE "^- R-[0-9]{4} — " .agent/live_review.md
326
```
All three match the block's stated values exactly (226, 27, 326 unchanged —
this round mints no new R-id).

G3 NEW TEST + IMPORT WIRING + MUTATION RED-PROOFS:
```
$ python3 -m pytest tests/orchestration/test_pingpong_cli.py -q
........................................................................ [ 41%]
........................................................................ [ 83%]
.............................                                            [100%]
173 passed in 2.10s
```
Matches the required 173 exactly (172 base + 1 new). Mutation red-proofs
(disposable `git worktree` at `.remedy-wt/f108-r10-mutation`, never the
primary checkout):

(a) `_reviewer_tiered_diff_text`'s
`if is_resumed or not safe_diff or not scope_packet:` (pingpong_loop.py
line 1599) mutated to `if True:`.
```
$ python3 -m pytest /home/decodeux/Repos/remedy/.remedy-wt/f108-r10-mutation/tests/orchestration/test_pingpong_cli.py::TestTieredSummariesReduceComposedPromptSize::test_both_call_sites_tiered_and_prompt_shrinks_an_order_of_magnitude -q
F                                                                        [100%]
FAILED ...AssertionError: assert False
 +  where False = exists()
 +    where exists = PosixPath('.../calls/reviewer/round-01/tiered_diff.diff').exists
1 failed in 0.49s
```
MUTATED → RED (real AssertionError: the reviewer's tiered-diff artifact was
never written because the branch short-circuited to `""` unconditionally).
`git status --porcelain` on the PRIMARY checkout, taken immediately after
the mutation edit, read empty. Reverted, confirmed GREEN again:
```
$ python3 -m pytest .../test_pingpong_cli.py::TestTieredSummariesReduceComposedPromptSize::... -q
.                                                                        [100%]
1 passed in 0.30s
```

(b) `_builder_tiered_diff_text`'s
`if is_resumed or not repair_diff or not findings:` (pingpong_loop.py line
1065) mutated to `if True:`.
```
$ python3 -m pytest /home/decodeux/Repos/remedy/.remedy-wt/f108-r10-mutation/tests/orchestration/test_pingpong_cli.py::TestTieredSummariesReduceComposedPromptSize::test_both_call_sites_tiered_and_prompt_shrinks_an_order_of_magnitude -q
F                                                                        [100%]
FAILED ...AssertionError: assert False
 +  where False = exists()
 +    where exists = PosixPath('.../calls/builder/round-02/tiered_diff.diff').exists
1 failed in 0.37s
```
MUTATED → RED (real AssertionError: the builder's tiered-diff artifact was
never written for the same reason). `git status --porcelain` on the
PRIMARY checkout, taken immediately after the mutation edit, read empty.
Reverted, confirmed GREEN again:
```
$ python3 -m pytest .../test_pingpong_cli.py::TestTieredSummariesReduceComposedPromptSize::... -q
.                                                                        [100%]
1 passed in 0.29s
```
Worktree removed cleanly (`git worktree remove .remedy-wt/f108-r10-mutation`,
no error); `git worktree list` afterward shows only the primary checkout
and one unrelated pre-existing job worktree.

G4 REGRESSION:
```
$ python3 -m pytest tests/orchestration/test_artifact_summaries.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_reviewer_prompt_golden.py -q
........................................................................ [ 70%]
..............................                                           [100%]
102 passed in 0.40s-0.48s (re-run twice, both times identical count)
```
Matches the required 102 exactly (27 + 39 + 36), unchanged from round 9. No
production code touched this round (`artifact_summary.py`/`pingpong_loop.py`
untouched), as the block required.

G5 STATE READERS:
```
$ python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q
604 passed in 48-51s (re-run twice, both times identical count)
```
Matches base exactly (604, unchanged).

G6 CANARY:
```
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20-22s (re-run twice, both times identical count)
```
Matches base exactly (42, unchanged).

G7 TREE + PLAN + SIZE:
```
$ wc -l .agent/plan.md
34 .agent/plan.md          # NOTE: file has no trailing final newline, so
                            # wc -l (counts '\n' chars) reads 34 even though
                            # the content is 35 lines; confirmed via
                            # data.split(b'\n') == 35 elements in Python
$ wc -c .agent/plan.md
1621 .agent/plan.md
$ sha256sum .agent/plan.md
73785aa588e2084a52589b0762f7fcb52302d5dbe23917c45f8b09d82a97f16f  .agent/plan.md
```
Byte count and sha256 both match SLICE_PLAN_R10's stated digest exactly
(1621 bytes, `73785aa5...`); this is the authoritative, cryptographically
exact confirmation. `wc -l` reading 34 instead of "35 lines" is a benign
`wc -l` artifact of the file's missing trailing newline, not a content
defect — disclosed here rather than silently reconciled. Under the 50-line
cap either way. Every landed commit's insertions are under 500 — full
list: 260 (C0a), 197 (C0b), 5 (C1), 65 (C2), 7 (C3).

Base SHA for the change-set sweep: `07749d21` — round 9's own tip,
independently re-confirmed via `git log --oneline` before use:
```
$ git diff --stat 07749d21..HEAD    # excludes this handback's own commit
 .agent/authored/f108-r10.md              | 260 ++++++++++++++++++
 .agent/last_block.md                     | 441 ++++++++++++++-----------------
 .agent/live_review.md                    |   6 +-
 .agent/plan.md                           |  21 +-
 tests/orchestration/test_pingpong_cli.py |  65 +++++
 5 files changed, 534 insertions(+), 259 deletions(-)
```
Exactly the 5 declared non-handoff change-set paths, nothing else.
```
$ git status --porcelain
(empty, apart from this handback commit in progress)
```

## Authored-text proofs

`.agent/authored/f108-r10.md` was written directly (`Write` tool) from the
step block's own text, copying every byte between the BEGIN/END markers
excluding the marker lines themselves; `.agent/last_block.md` was then
mirrored via `cp`, and both independently confirmed byte-identical via
`sha256sum` (identical digest, both files). The Gate/DECISION paragraphs
for SLICE_LEDGER_R10 were composed in a Python script as literal string
constants transcribed directly from the block text, appended
(`old + "\n\n" + gate_para + "\n\n" + decision_para`, no trailing newline)
to `.agent/live_review.md`, then independently re-measured (byte count,
sha256, all three grep counts) and confirmed to match the block's stated
targets exactly before commit.

The SLICE_PLAN_R10 text was NOT applied cleanly on the first attempt: this
worker's own hand-typed `Write`-tool transcription produced 35 lines /
1622 bytes / sha256 `295690a5f7ff28a3272d5c269ac67b474d2283e754f2ea54e80907cc87c8731a`,
not the block's stated 35 lines / 1621 bytes /
`73785aa588e2084a52589b0762f7fcb52302d5dbe23917c45f8b09d82a97f16f`. Per the
block's own instruction ("If these do not match your applied file, STOP, do
not commit, and report the mismatch"), the worker reverted the uncommitted
edit and reported the discrepancy rather than forcing a match, having ruled
out a general transcription-competence issue (the much larger and more
error-prone SLICE_LEDGER_R10 append had landed byte-exact against its own
stated numbers). The reviewer then independently reproduced the block's
own exact text via `Write` into a scratch file
(`.remedy-wt/scratch/plan_as_sent.md`), confirmed to hash to the block's
originally-stated digest, and directed a mechanical `cp` of that scratch
file to `.agent/plan.md` instead of a retype. The subsequent `git diff`
against round 9's committed `plan.md` revealed the actual root cause: the
worker's hand-typed attempt had the `T003b-iii` and `T003d` table rows in
swapped order relative to the block's intended order (`T003d` row
immediately after `T003c`, `T003b-iii` row last) — a genuine content slip,
not a stray character or smart-quote substitution. The `cp`'d file
independently re-hashed to the correct digest before commit. The scratch
file was deleted by its exact path (`.remedy-wt/scratch/plan_as_sent.md`)
immediately after C3's commit and re-verification, per policy (never
delete by glob).

## Deviations & assumptions

- The SLICE_PLAN_R10 mismatch-and-repair episode above (hand-typed
  transcription swapped two table rows; caught by the block's own mandated
  byte/hash verification; repaired via a reviewer-supplied, mechanically
  copied scratch file rather than a second retype). No product-code
  effect; the wrong content was never committed. This belongs in
  `.agent/prose_slips.md` by that file's own rule (a worker-transcription
  slip that damaged nothing on disk, caught before commit) — left for the
  next round to append rather than appended here unprompted, matching the
  precedent set by round 9's own equivalent note.
- `wc -l .agent/plan.md` reads 34, not 35, because the file (as supplied
  byte-for-byte by the reviewer's scratch copy) has no trailing final
  newline; byte count and sha256 both confirm the content is exactly
  SLICE_PLAN_R10's intended 35 lines. Noted under G7 above, not treated as
  a gate failure.
- Otherwise none. All 6 declared change-set paths applied exactly as the
  block (and the reviewer's mid-round correction) ordered. All gates
  G1-G7 passed as stated, after the one documented repair above; no other
  stale-SHA or mismatched-digit discrepancy was found in SLICE_LEDGER_R10
  or the SPEC itself.

## Next

T003d is closed — the feature's own DONE-condition wording ("a fixture
long artifact enters a follow-up prompt at a fraction of its size with the
reference path present") is now proven end-to-end against the real
`run_pingpong` call sites. Remaining before closure:
1. Integration gate (full suite, both required runs).
2. Closure sequence: README sync, STATUS `[x]`, evidence bundle, review
   package.
T003b-iii (the reviewer's fallback-branch tiering) stays deferred per
DECISION F108 D4, unchanged. No PR yet.
