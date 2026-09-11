# Handback — F275 round 51

## Session

SESSION 20 of feature F275 · round 51 · rounds so far 51

Context self-assessment (amend0905-throughput): context is comfortable — this round read
AGENTS.md in full, verified and copied a 40562-byte block, applied twenty-five slices
(PLAN51, RECORD51, FIND51, ten FROM/TO pairs, GUARD51, LANDED51) and spent the rest on
eight gate runs including a four-run red proof in a disposable worktree; there is room for
at least one more round in a fresh session.

    SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F275 stands at 51 rounds and 20 sessions against the operator's soft limit of 60 rounds and
20 SESSIONS (amend0908-f275-finish rule 1). THE SESSION LIMIT IS REACHED and the SCOPE
REPORT that rule obliges is written below, under `## Scope report`. Rule 2 forbids the
amend0905-throughput split-and-close default here BY NAME: the session writes the report and
CONTINUES. This round closed nothing, registered no follow-up feature and did not touch
`docs/roadmap/STATUS.md`.

`.agent/STOP` was re-read FROM DISK before the first commit and again at C4: it does not
exist (`cat .agent/STOP` → `No such file or directory`, exit 1) at both readings.

## Range

Review of `17d3f513`..C5, where C4 is `769fc2f805b2d2d82865399ec4ae4b202aec02f2` and C5 is
the commit that writes this file. C5's own SHA is NOT stated here: it does not exist while
this file is being written, and no SHA is written that was not measured.

## Commits

### 02b8bfd5a080734c78a2f3c62d64b319f9083203 F275 R51 C0a: save the round 51 step block verbatim.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r51.md` | +465 / -0 | the round 51 block, saved by `shutil.copyfile` from `.remedy-wt/f275-r51.block.md`, never retyped; every slice this round applies is extracted from THIS file's committed blob by its `BEGIN-`/`END-` marker-line prefix |

### 63baabf6dea05c30d7f3bb250d2b9da63e2dab4f F275 R51 C0b: mirror the round 51 block into last_block from the committed blob.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +381 / -393 | written from `git cat-file blob 02b8bfd5:.agent/authored/f275-r51.md` read into memory, not retyped; replaces the round 50 block |

### a90bf0abb9dead8c77acc34f01121d7cdb85ff15 F275 R51 C1: advance the plan to round 51.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +16 / -17 | whole-file replacement by slice PLAN51; Current Step becomes round 51 and the first group of DECISION F275 D29's P2, Next Steps put P2's remaining groups first, Risks re-state the open set at 87 and the session limit |

### 359807a039d13fac13227ebeb28c0d7f759dc3d7 F275 R51 C2: book the round 50 PASS verdict and register R-0877.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | appends RECORD51 (the round 50 PASS verdict) then FIND51 (the registration of `R-0877`, Medium), in that order |

### 133ccd530eda159ba1c01fa7e3ddba68c781d162 F275 R51 C3: join the job id verbatim in the run-log writer pair and guard both halves.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/timeline.py` | +11 / -5 | P51A drops the now-unused module-level `from uuid import UUID`; P51B and P51D narrow both `job_id` annotations to `str`; P51C replaces the `UUID(str(job_id))` coercion with a verbatim `str(job_id)` join and states in the docstring why |
| `packages/orchestration/run_log.py` | +2 / -2 | P51G drops `UUID` from `from uuid import UUID, uuid4`; P51H narrows `RunLogWriter.__init__`'s `job_id` to `str`, which the body (`str(job_id)`) already assumed |
| `packages/orchestration/test_failure_artifact.py` | +2 / -2 | P51E narrows `emit_failure_events`'s `job_id` to `str`; P51F replaces the coercion with `str(job_id)`. The module-level `UUID` import STAYS — line 324 still calls `UUID(failure.task_id)` |
| `packages/orchestration/safe_points.py` | +5 / -5 | P51I — prose only, inside `_emit_budget_tick`'s docstring. Its stated CAUSE was the coercion this commit removes; DECISION F022 D2 clause one is NOT reversed and no line of code moves |
| `tests/orchestration/test_budget_tick.py` | +6 / -4 | P51J — prose only, inside the T6 regression test's docstring, same reason. The assertion is untouched |
| `tests/test_timeline.py` | +52 / -0 | GUARD51, a CODE APPEND: class `TestRunEventsAcceptTheShippedJobIdShape` with three tests, one per half of `R-0877` plus the round trip, each constructing through the REAL function |

### 769fc2f805b2d2d82865399ec4ae4b202aec02f2 F275 R51 C4: book the R-0877 landing line.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | appends LANDED51, the `Landed: R-0877` line. NO `Done:` paragraph — only reviewer-authored text sets a resolution |

### C5 (SHA unmeasurable from inside itself) F275 R51 C5: the round 51 handback.
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | whole-file rewrite | this file; a handoff cannot table the commit that writes it, nor state its own insertion count (R-0149 pattern). AGENTS.md exempts a single-`.agent/` state-file rewrite from the 500-line counting rule by construction |

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | |
| G7 | done | |
| G8 | done | |
| R-0877 | registered | FIND51 at C2, `Landed:` at C4; NOT resolved — the reviewer's authored `Done:` is owed at the next gate |
| P51A–P51J | done | all ten applied, all ten rebuilt byte-identically from the base blob under G4 |
| GUARD51 | done | proved by ordered equality under G5 |
| Scope report | done | written below; no closure, no follow-up feature, `docs/roadmap/STATUS.md` untouched |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/base51 17d3f513` | created for G6(c)'s base ruff reading; removed and pruned before the handback |
| `git worktree add --detach .remedy-wt/rp51 133ccd53` | created for G7's red proof; never `cd`-ed into, every command run as `subprocess.run([...], cwd=<abs worktree>)`; removed and pruned before the handback |
| `git worktree list` | after the removals: ONE entry, `/home/decodeux/Repos/remedy 133ccd53 [feature/f275-one-world-completion-part-three]` (read before C4) |
| `git push -u origin feature/f275-one-world-completion-part-three` | ordered and executed immediately AFTER C5. Its outcome is by construction unrecordable here — a handback cannot report a push that follows it — so no outcome is claimed; the reviewer reads it from `git log origin/feature/f275-one-world-completion-part-three` |

No PR created, edited or merged. No force-push, no history rewrite, no branch deleted.
No `remedy` CLI command was run. `/tmp` was not written; all scratch lives under the
gitignored `.remedy-wt/`.

## Verification

EIGHT gates run, G1 through G8 — the number is the worker's own count; the block states
none. Every one run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`.

**G1 TRANSPORT, at C0b — PASS, exit 0.** The chain the proof walked has four links and no
retyped byte: `.remedy-wt/f275-r51.block.md` → (`shutil.copyfile`) →
`.agent/authored/f275-r51.md` on disk → (`git commit`) → the committed blob at `02b8bfd5` →
(`git cat-file blob` into memory) → `.agent/last_block.md`.
```
committed blob bytes 40562 sha256 b1601e968082383db0712420c1a136b28542f6260b14b59f3f5184a722de8e8a
last_block bytes 40562 sha256 b1601e968082383db0712420c1a136b28542f6260b14b59f3f5184a722de8e8a
scratch bytes 40562 sha256 b1601e968082383db0712420c1a136b28542f6260b14b59f3f5184a722de8e8a
scratch==committed: True  committed==mirror: True
```
The digest the delegation message states is
`b1601e968082383db0712420c1a136b28542f6260b14b59f3f5184a722de8e8a` and both byte counts are
40562, so authored == delegated and mirror == authored. The block carries `BEGIN-`/`END-`
marker lines for its SLICES only and no BEGIN marker of its own, so the digest is the whole
identity. Nothing is claimed about the bytes emitted into the worker's prompt — the proof
never reads them.

**G2 THE PLAN, at C1 — PASS, exit 0.**
```
slice bytes 2531 sha256 a792e691ba6bf348a0a6f9f4ff79e8e549284a94b326b2deb1be5401ab92dda2
C1 blob bytes 2531 sha256 a792e691ba6bf348a0a6f9f4ff79e8e549284a94b326b2deb1be5401ab92dda2
byte-equal: True
line count: 44 cap 50 ok: True
^## Goal$ count: 1
^## Next Steps$ count: 1
REAL_EXIT=0
```

**G3 THE RECORD, at C2 and again at C4 — PASS, exit 0 both times.** Every pre and post blob
was read with `git show <sha>:<path>` INTO MEMORY; no non-current revision was ever written
over a tracked file.

(i) `.agent/live_review.md` ← RECORD51 then FIND51, pre at C1, post at C2:
```
pre bytes 905059 sha256 cdc5e09211910ab74a6516b17e2d0f1ae0d08165e3c9d1db3f760454b6df4124
post bytes 912592 sha256 6054a13849d881ae4e76c6de720310e900d82a63afd2395bf64300fd96afce7b
RECORD51 bytes 3669 FIND51 bytes 3864
(a) reader A identical: True
(b) reader B N counted from slices: 2 ordered tail equal: True
(c) control flipped at offset 905065 byte b' ' -> b'!'
(c) reader A on control: False (expect False)
(c) reader B on control: False (expect False)
REAL_EXIT=0
```
N = 2 is COUNTED by the script across RECORD51 and FIND51 (one blank-line-separated
paragraph each); no number from the block was asserted. The control byte at offset 905065
lies 6 bytes into the FIRST appended paragraph (the pre-blob ends at 905059, RECORD51's
leading blank line occupies 905059, the paragraph `Gate: F275 R50 — …` starts at 905060).
Both `(c)` readers were re-run against the ORIGINAL slices — the mutated blob is the post
side in both, never the slices.

(ii) `.agent/live_review.md` ← LANDED51, pre at C3, post at C4, reading (a) alone:
```
pre bytes 912592 sha 6054a13849d881ae4e76c6de720310e900d82a63afd2395bf64300fd96afce7b
post bytes 912896 sha a86397a3be9df2c076a6c495640b2d14c222e8353f8ca565803ce297b2abe0f8
LANDED51 bytes 304 sha 19cce4590d0655ce8cac9209b6e965ed28cc3743fdbe5bdb78ef1ba5d67e6621
(a) reader A identical: True
REAL_EXIT=0
```
All three appends are `old_bytes + slice_bytes` in Python; each slice's leading byte is
`\n` and each pre-blob already ended in a newline, so none was added. Every length is
`len(<bytes>)` over a byte stream, never `len()` over a decoded `str`.

**G4 THE TEN PAIRS, at C3, against COMMITTED blobs — PASS, exit 0.**
```
pair   file                               containment              FROM@base  FROM@C3   TO@C3
P51A   timeline.py                        TO contains FROM: false  1          0         n/a — TO is a PREFIX of FROM
P51B   timeline.py                        TO contains FROM: false  1          0         1
P51C   timeline.py                        TO contains FROM: false  1          0         1
P51D   timeline.py                        TO contains FROM: false  1          0         1
P51G   run_log.py                         TO contains FROM: false  1          0         1
P51H   run_log.py                         TO contains FROM: false  1          0         1
P51E   test_failure_artifact.py           TO contains FROM: false  1          0         1
P51F   test_failure_artifact.py           TO contains FROM: false  1          0         1
P51I   safe_points.py                     TO contains FROM: false  1          0         1
P51J   test_budget_tick.py                TO contains FROM: false  1          0         1

REBUILD from base by the assigned pairs, in order:
  packages/orchestration/timeline.py               rebuilt 16948 bytes sha 1573d844816bb124 | C3 16948 bytes sha 1573d844816bb124 | identical: True
  packages/orchestration/run_log.py                rebuilt 6355 bytes sha 540f5e39f6421360 | C3 6355 bytes sha 540f5e39f6421360 | identical: True
  packages/orchestration/test_failure_artifact.py  rebuilt 15524 bytes sha f33abd4ef9404600 | C3 15524 bytes sha f33abd4ef9404600 | identical: True
  packages/orchestration/safe_points.py            rebuilt 30401 bytes sha d59b08fe18ac990f | C3 30401 bytes sha d59b08fe18ac990f | identical: True
  tests/orchestration/test_budget_tick.py          rebuilt 13178 bytes sha dff9cbe2295ce407 | C3 13178 bytes sha dff9cbe2295ce407 | identical: True
REAL_EXIT=0
```
Every one of the ten is a REWRITE by the containment test's own output, `TO contains FROM:
false`, not by eye. The base is `17d3f513`. P51A's TO count is stated as `n/a` rather than
omitted: its TO (`from typing import Any\n`) already occurs inside its own FROM
(`from typing import Any\nfrom uuid import UUID\n`), so a TO count of 1 would be true before
and after the edit and discriminates nothing; the FROM count going 1 → 0 is the reading that
carries the pair. The rebuild applies ONLY the pairs the block assigns to each file, in the
listed order, and each rebuilt file is byte-identical to the C3 blob — so no other edit
reached those five paths.

**G5 THE GUARD, at C3, by ORDERED EQUALITY — PASS, exit 0.**
```
base bytes 35021 C3 bytes 37184 slice bytes 2163
(1) base is byte-exact PREFIX of C3: True
(2) slice is byte-exact SUFFIX of C3: True
    len(base)+len(slice)==len(C3): True
(3) diff ADDS 52 lines; slice has 52 lines; ordered equal: True
REAL_EXIT=0
```
Not a per-line multiplicity count: GUARD51 repeats blank lines and `assert` lines
structurally, so multiplicity is unattainable by construction. The three clauses together
pin the append exactly — a prefix, a suffix, and the added-line sequence IN ORDER, read from
`git diff --unified=0 133ccd53^..133ccd53 -- tests/test_timeline.py`.

**G6 THE FIX WORKS AND NOTHING NEAR IT MOVED, at C3 — PASS.**

(a) Tree digests, exit 0. ALL FOUR MATCH the reviewer's own measurement of this fix applied
to a clean checkout, so this tree IS the tree that was measured:
```
C3:packages  6d2ec62e10948175e3c338aa951f3bca3cb4ddc5
C3:tests     b104a5acd66ce6c1c1482e7deaf4c862b0bcda52
base:packages 1f1a040413f8045a9e53ec8dece733ddb1d0c0ac
base:tests    b33e3ac3ed64ebd1d6fa4e0b86c9f8614c4d07ee
```

(b) `git diff --numstat 133ccd53^..133ccd53` — C3's OWN range, exit 0. Exactly six rows,
every one as stated, and no `.agent/` row (which a range starting at the base would have
carried):
```
2	2	packages/orchestration/run_log.py
5	5	packages/orchestration/safe_points.py
2	2	packages/orchestration/test_failure_artifact.py
11	5	packages/orchestration/timeline.py
6	4	tests/orchestration/test_budget_tick.py
52	0	tests/test_timeline.py
```

(c) THE RUFF CEILING, exit 1 at both readings (ruff exits 1 whenever findings remain; the
gate is the COUNT, not the exit code). At C3 in the primary checkout:
```
tests/ui_contracts/test_graph_architecture.py:6:1: I001 [*] Import block is un-sorted or un-formatted
Found 26 errors.
[*] 25 fixable with the `--fix` option.
REAL_EXIT=1
```
At the base `17d3f513`, read in the disposable worktree `.remedy-wt/base51` — never by
writing base bytes over a tracked file:
```
Found 26 errors.
[*] 25 fixable with the `--fix` option.
REAL_EXIT=1
```
**26 at both.** The two deleted imports (`UUID` from `timeline.py`, `UUID` from
`run_log.py`) do not move the count `tests/orchestration/test_ci_budgets.py` freezes,
because they were deleted rather than left unused.

(d) THE SCOPED ROUND GATE, in the primary checkout at C3:
```
481 passed in 1.98s
REAL_EXIT=0
```
and the canary `python3 -m pytest tests/cli/test_golden_path.py -q`:
```
42 passed in 18.79s
REAL_EXIT=0
```
Both figures equal the reviewer's pre-measured readings exactly.

**G7 THE RED PROOF, at C3 — PASS, exit 0.** Run in the disposable worktree
`.remedy-wt/rp51`, detached at `133ccd53`, NEVER `cd`-ed into: every command ran as
`subprocess.run([...], cwd="/home/decodeux/Repos/remedy/.remedy-wt/rp51")` under
`python3 -B` with `-p no:cacheprovider`, and `__pycache__` was purged before every run.
The module resolution was printed and checked BEFORE any result was believed:
```
worktree detached at 133ccd530eda159ba1c01fa7e3ddba68c781d162
purged __pycache__ dirs: 0
resolved timeline.__file__ = /home/decodeux/Repos/remedy/.remedy-wt/rp51/packages/orchestration/timeline.py
inside worktree: True
```
It lies inside the worktree, not in the primary checkout and not in an install. Selection for
EVERY run was all three node ids together. FAILED node ids are parsed as what follows the
FIRST space of a `FAILED <nodeid> - <msg>` line, and reported as a SET:
```
[CONTROL (unmutated)] exit=0  last='3 passed in 0.21s'
[CONTROL (unmutated)] FAILED node id SET (0):

timeline.py sha256 BEFORE M1: 1573d844816bb1242ec94ec05113daea9d960d614652a59439b6f27763dab67f 16948 bytes

[M1 (coercion restored in timeline.append_run_event)] exit=1  last='3 failed in 0.27s'
[M1 (coercion restored in timeline.append_run_event)] FAILED node id SET (3):
    tests/test_timeline.py::TestRunEventsAcceptTheShippedJobIdShape::test_a_run_event_is_readable_by_the_reader_in_its_own_module
    tests/test_timeline.py::TestRunEventsAcceptTheShippedJobIdShape::test_append_run_event_takes_the_shipped_job_id_shape
    tests/test_timeline.py::TestRunEventsAcceptTheShippedJobIdShape::test_emit_failure_events_takes_the_shipped_job_id_shape
M1 revert byte-exact vs recorded digest: True

test_failure_artifact.py sha256 BEFORE M2: f33abd4ef94046002c7ae9d7e7b1228cc879e464578d9742d594eb47bfd6127d 15524 bytes

[M2 (coercion restored in emit_failure_events)] exit=1  last='1 failed, 2 passed in 0.24s'
[M2 (coercion restored in emit_failure_events)] FAILED node id SET (1):
    tests/test_timeline.py::TestRunEventsAcceptTheShippedJobIdShape::test_emit_failure_events_takes_the_shipped_job_id_shape
M2 revert byte-exact vs recorded digest: True

[CONTROL again (after both reverts)] exit=0  last='3 passed in 0.21s'
[CONTROL again (after both reverts)] FAILED node id SET (0):

--- ordering ---
control set empty: True | final control set empty: True
M1 set size: 3 M2 set size: 1
M2 set is a SUBSET of M1 set (containment, NOT disjointness): True
M2 set: ['tests/test_timeline.py::TestRunEventsAcceptTheShippedJobIdShape::test_emit_failure_events_takes_the_shipped_job_id_shape']
worktree status clean: ''
REAL_EXIT=0
```
The UNMUTATED control ran FIRST at exit 0, and its exit code stands beside both mutated
runs. M1 reverted P51C's writer statement ALONE, restoring
`jid = job_id if isinstance(job_id, UUID) else UUID(str(job_id))` with a LOCAL
`from uuid import UUID` because P51A removed the module-level one; M2 reverted P51F.
THE TWO SETS ARE NOT DISJOINT and the containment is reported rather than a disjointness
that does not hold: M2's set is a strict SUBSET of M1's. What M2 establishes is that the
`emit_failure_events` fix is INDEPENDENTLY NECESSARY — with `timeline.py` already fixed,
that one node is still red without it. Each file's sha256 was recorded BEFORE its mutation
and both reverts are byte-exact against the recorded digest; the worktree's own
`git status --porcelain` is `''` at the end. Both worktrees were removed and pruned before
this handback, leaving one entry in `git worktree list`.

**G8 NOTHING ELSE MOVED, at C4 — PASS, exit 0.**
```
--- (a) ---
.agent/STOP exists on disk: False
git status --porcelain == ''

--- (b) ---
expected (Change section minus handoff.md): 10
actual over 17d3f513..C4: 10
MISSING: []
EXTRA  : []
paths under apps/ docs/ scripts/: 0 []

--- (c) THE OPEN SET, BY DISTINCT ID ---
base 17d3f513: registered 105, resolved 19, OPEN 86
C4      : registered 106, resolved 19, OPEN 87
ids REGISTERED this round: ['R-0877']
ids RESOLVED  this round: []
C3: ^Landed: R-0877  = 0   ^Done: R-0877  = 0
C4: ^Landed: R-0877  = 1   ^Done: R-0877  = 0
```
The expectation in (b) was resolved against the block's Change section itself — the ten paths
it names other than `.agent/handoff.md`, which C5 writes — and NOT against any number stated
anywhere in the block. The `.agent/STOP` literal result is `cat: .agent/STOP: No such file or
directory`, exit 1; the porcelain literal string is `''`.

(d) Per-commit insertions against the AGENTS.md DECISION F104 D1 cap of 500, derived ONCE
from `git show --numstat <sha>` and used both here and in the `+/-` column of `## Commits`
above:
```
C0a  02b8bfd5  +465  -0     cap500 ok: True
C0b  63baabf6  +381  -393   cap500 ok: True
C1   a90bf0ab  +16   -17    cap500 ok: True
C2   359807a0  +4    -0     cap500 ok: True
C3   133ccd53  +78   -18    cap500 ok: True
C4   769fc2f8  +2    -0     cap500 ok: True
REAL_EXIT=0
```
Every one is under 500, so F275's one oversize allowance is STILL UNSPENT at 51 rounds.

## Open findings

**87 by distinct id at C4**, up from 86 at the base `17d3f513`. `R-0877` is the only id
registered this round and NOTHING was resolved. Four of the 87 are High — R-0803, R-0804,
R-0806 and R-0807 — all F273's, per DECISION F272 D12.

## Scope report

Written because amend0908-f275-finish rule 1 sets F275's soft limit at 20 sessions and 60
rounds and this is session 20, round 51. Rule 2 forbids the amend0905-throughput
split-and-close default here BY NAME. Every claim below is a reading this round took, from
`.agent/plan.md` as this round leaves it, from `docs/roadmap/features/T2_F275.md`'s three
task slices, and from DECISION F275 D29's three prerequisites. Nothing is carried from the
step block.

### (a) WHAT IS FINISHED

- **T001 — reachability-gated cluster deletion: DONE.** `.agent/plan.md` records T001 and
  T002 as done and the operator ruling amend0908-f275-finish as ordering T001 PERFORMED
  rather than prepared.
- **T002 — measure the flip, then rule the cap: DONE as the slice defines it.** The slice's
  own text says "No production line moves in this slice" and requires the probe plus a dated
  DECISION choosing the route. DECISION F275 D29 (2026-09-11, round 50) is that ruling and is
  present in `.agent/decisions.md` at 1 occurrence.
- **T003's command surface: the classic runner's commands are gone.** `git grep -n -- run-next
  -- apps packages tests docs scripts` returns 61 lines, and I read every live one: they are
  `run-next-task-local` — a DIFFERENT command — plus one prose line at
  `apps/cli/commands/job.py:693`. No `job run-next` handler survives.
- **DECISION F275 D29's P2, first group: LANDED this round.** An `ast` sweep over the 993
  tracked `.py` files at the C4 tip finds **0** parameters whose annotation names both `UUID`
  and `str` and whose body still calls `UUID()`; **15** such parameters remain and none of
  them coerces. The class `R-0877` names is closed.

### (b) WHAT IS MISSING

From `.agent/plan.md`'s Next Steps as this round leaves them, each re-measured here:

1. **P2's remaining groups.** An `ast` sweep at the C4 tip counts **167** `UUID(<job/task
   argument>)` call sites across **64** files, **38** of them under `packages/` or `apps/`.
   DECISION F275 D29 recorded 169 in 65 files / 39 production at `020b1d57`; this round's C3
   removed two of them. Landed one assignment-connected component per commit, per D28.
2. **P1 — the type-resolved field rename.** NOT STARTED. `docs/roadmap/features/T2_F275.md`
   T002 already orders the DECISION F272 D7 raising-property probe, and D29 attributes 551
   exception lines over 22 receiver-and-attribute pairs to the receiver-NAME heuristic every
   dry run has used instead.
3. **P3 — the `**` splat call-graph pass** over the test helper factories. NOT STARTED; D29
   records the class unchanged at 867.
4. **The dry run re-run, then THE FLIP** as the one declared-oversize commit AGENTS.md
   permits per feature. D29's CONSEQUENCE clause makes the re-run mandatory after P1–P3.
5. **T003's remainder — the resolver collapse (DECISION F260 D5) with the classic store.**
   `resolve_any_job_id` is still live at 4 files and 17 occurrences:
   `apps/cli/commands/job_context_cmd.py` 2, `apps/cli/commands/teach_cmd.py` 5,
   `packages/orchestration/data_paths.py` 4, `tests/test_data_paths.py` 6. T003's own text
   makes the atomic flip the prerequisite for all of it.
6. **The closure sequence** — the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR. NONE started.
7. **The finding ledger** stands at 87 open by distinct id, four of them High.

### (c) A PROPOSAL

The remaining work is item 1 through item 6 above and it will NOT fit in the nine rounds left
inside amend0908-f275-finish rule 1's 60-round limit: P1 alone is a probe, a site set and a
transform-rule change, and the flip after it is the single largest commit this feature has
ever planned. My proposal, for the operator to rule on:

1. Continue the present ordering — P2's remaining groups first, because they are the cheapest
   and each is independently landable one component per commit, and because each one removed
   is one fewer site that survives the flip and then rejects its value.
2. Then P1, as the largest measured residue class and the one T002 already ordered.
3. Then P3, then the dry-run re-run, and only then the flip.
4. **Ask the operator to choose between an EXTENSION of the round limit and a SPLIT** that
   carries the flip and T003's remainder into a successor feature. This round may not make
   that choice — rule 2 forbids the split-and-close default by name, and a round that closed
   F275 here would leave the classic store and `resolve_any_job_id` alive beside the new
   mechanism, which AGENTS.md's "Replacing is deleting" rules is not a closure.

F275 is NOT closed by this round, no follow-up feature was registered, and
`docs/roadmap/STATUS.md` was not touched. The report is a report.

## Deviations

1. **A numeral inside FIND51 does not reproduce under my own sweep, and the slice was applied
   BYTE FOR BYTE anyway**, per constraint 1, which orders a slice that looks wrong applied as
   given and DECLARED. FIND51 says the two coercing sites sit "beside sixteen further `UUID |
   str` parameters whose bodies do NOT coerce". My `ast` sweep over the 993 tracked `.py`
   files counts **15** remaining parameters whose annotation names both `UUID` and `str`
   (7 if the annotation must be exactly `UUID | str` or `str | UUID`), all non-coercing.
   15 remaining + the 2 this round narrowed to `str` = 17 at the base, against the 18 the
   slice's "two plus sixteen" implies. The load-bearing halves of the finding — TWO coercing
   sites, both repaired, zero remaining — reproduce exactly. Nothing on disk is wrong; this is
   a reviewer-prose numeral and is raised here rather than as an id, per amend0827 rule 2.
2. **G6(c)'s ruff runs exit 1, not 0**, at BOTH readings. Ruff exits non-zero whenever any
   finding remains, and 26 remain at the base and at C3; the gate measures the COUNT and the
   count is equal, so this is the expected exit and not a failure. Reported rather than
   silently normalised.
3. **`python3 -m compileall` was run over the six edited files during the C3 self-review**,
   before `git add`. It writes `__pycache__`, which is gitignored; `git status --porcelain`
   was re-read and showed only the six tracked modifications. No committed byte came from it.

Nothing else deviates. All twenty-five slices were extracted mechanically from the COMMITTED
blob of `.agent/authored/f275-r51.md` by their `BEGIN-`/`END-` marker-line PREFIX, marker
lines excluded, and none was retyped or reflowed. The commit order C0a, C0b, C1, C2, C3, C4,
C5 was kept exactly: none merged, none reordered. `.agent/decisions.md` and
`.agent/prose_slips.md` were NOT touched, as the Change section requires.

## Next expected action

The planner and reviewer of the next session re-derive every gate above against the committed
range `17d3f513`..C5 and write the round 51 verdict, and — if that verdict is PASS — the
authored `Done: R-0877` paragraph, which only reviewer-authored text may set. The
`Landed: R-0877` line committed at C4 survives beside it. The operator's ruling on the scope
report's item (c) is owed before the next session plans past P2.
