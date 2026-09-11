# Handback — F275 round 49

## Session

SESSION 19 of feature F275 · round 49 · rounds so far 49

Context self-assessment (amend0905-throughput): context is comfortable — this round
read AGENTS.md, the 280-line self-drive protocol and the 105-line handback template,
copied and verified a 28474-byte block, applied nine slices, and spent the rest on
eight gate runs including a two-mutation red proof in a disposable worktree; there is
room for at least one more round this session.

F275 stands at 49 rounds and 19 sessions against the operator's soft limit of 60 rounds
and 20 sessions (amend0908-f275-finish rule 1). The limit is NOT reached; no scope
report is owed by this round. The NEXT session is the twentieth.

## Range

Review of `70d6c8e6`..C5, where C4 is `31e37b27` and C5 is the commit that writes this
file. C5's own SHA is NOT stated here: it does not exist while this file is being
written, and no SHA is written that was not measured.

## Commits

### 67209157 F275 R49 C0a: save the round 49 block as the authored source of every slice.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r49.md` | +314 / -0 | the round 49 block, saved by `shutil.copyfile` from `.remedy-wt/f275-r49.block.md`, never retyped; every slice this round applies is extracted from THIS file's committed blob |

### 17d602ad F275 R49 C0b: mirror the round 49 block into the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +247 / -358 | written from `git cat-file blob 67209157:.agent/authored/f275-r49.md`, not retyped; replaces the round 48 block |

### 365c4cf4 F275 R49 C1: the round 49 plan.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17 / -17 | whole-file replacement by slice PLAN49; Current Step becomes round 49, Risks re-state the open set at 87 and the nullability rule |

### 509f3180 F275 R49 C2: book the round 48 FAIL verdict, register R-0876 and record one reviewer slip.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | appends RECORD49 (the round 48 FAIL verdict) then FIND49 (the `R-0876` registration), in that order |
| `.agent/prose_slips.md` | +2 / -0 | appends SLIPS49, one dated line on DECISION F275 D28's unmeasured attribution |

### 9df09805 F275 R49 C3: keep task_id absent when there is no task, and guard both sites.
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/do_run.py` | +1 / -1 | PAIR49A — the `str(...)` moves inside the conditional's true branch in `_run_build_phase`, so a job with no tasks yields `task_id=None` |
| `packages/orchestration/test_failure_artifact.py` | +1 / -1 | PAIR49B — the same move in `persist_failure_artifact`, so an empty `failure.task_id` yields `task_id=None` |
| `tests/orchestration/test_do_run.py` | +21 / -0 | GUARD49A appended — `TestSystemArtifactKeepsTaskIdAbsent` over `_run_build_phase` |
| `tests/orchestration/test_test_failure_repair.py` | +26 / -0 | GUARD49B appended — `TestSystemArtifactKeepsTaskIdAbsent` over `persist_failure_artifact` |

### 31e37b27 F275 R49 C4: book the R-0876 landing line.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | appends LANDED49, the `Landed: R-0876` line, AFTER the fix it describes is committed |

### C5 (SHA unmeasurable from inside itself) F275 R49 C5: the round 49 handback.
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
| G6 | deviated | (a) and (c) exactly as stated; (b)'s "exactly four rows" is FALSE for the range the gate names — see Deviations |
| G7 | done | |
| G8 | done | |
| R-0876 | registered | resolved by nobody this round; only reviewer-authored text sets a resolution |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r49-wt 9df09805` | exit 0 — "HEAD is now at 9df09805" |
| `git worktree remove --force .remedy-wt/r49-wt` | exit 0 |
| `git worktree prune` | exit 0 |
| `git worktree list` | ONE entry: `/home/decodeux/Repos/remedy 9df09805 [feature/f275-one-world-completion-part-three]` |
| `git push -u origin feature/f275-one-world-completion-part-three` | ordered and executed immediately AFTER C5. Its outcome is by construction unrecordable here — a handback cannot report a push that follows it — so no outcome is claimed; the reviewer reads it from `git log origin/feature/f275-one-world-completion-part-three` |

No PR created, edited or merged. No force-push, no history rewrite, no branch deleted.

## Verification

EIGHT gates run, G1 through G8 — the number is the worker's own count; the block
states none. Every one run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`.

**G1 TRANSPORT, at C0b — PASS, exit 0.** The chain the proof walked has four links
and no retyped byte: `.remedy-wt/f275-r49.block.md` → (`shutil.copyfile`) →
`.agent/authored/f275-r49.md` on disk → (`git commit`) → the committed blob at
`67209157` → (`git cat-file blob`/`git show`) → `.agent/last_block.md`. All four read
**28474 bytes** at sha256
`37081bec7b73c5e7d4de0fbf52ac2dc249a2dccc62ace4d6f92f7b37afadb113`, which is the digest
the delegation message states; `all four identical: True`. The block carries
`BEGIN-`/`END-` marker lines for its SLICES only and no BEGIN marker of its own, so the
digest is the whole identity. Nothing is claimed about the bytes emitted into the
worker's prompt — the proof never reads them.

**G2 THE PLAN, at C1 — PASS, exit 0.**
```
PLAN49  slice: bytes=2557 sha256=abf50111b70af3357478ee0f27cf582d9642a9f2097552a6b37c1e23bf3d2ea6
plan.md  disk: bytes=2557 sha256=abf50111b70af3357478ee0f27cf582d9642a9f2097552a6b37c1e23bf3d2ea6
byte-equal: True
line count: 45 | AGENTS.md cap 50 | under cap: True
^## Goal$ count: 1
^## Next Steps$ count: 1
```

**G3 THE RECORD AND THE SLIPS — PASS, exit 0.** Every pre and post blob read with
`git show <sha>:<path>` INTO MEMORY; no non-current revision was ever written over a
tracked file.

(i) `.agent/live_review.md` ← RECORD49 then FIND49, inside C2:
```
pre  @C1: 892396 649d06a2b9e0a0ad0f61b9bd1a7129315c3bb20e5e8e48501df8866223ffef23
post @C2: 898518 a75524fd81467897219cb4726412575cc7e08abafa0083ca3df3980da360bd04
RECORD49 bytes: 3921   FIND49 bytes: 2201
(a) reader A  identical: True
(b) reader B  N counted from the slices: 2   last-N units equal, in order: True
(c) negative control: one byte flipped inside the FIRST appended paragraph
    reader A on mutated: False (must be False)
    reader B on mutated: False (must be False)  N: 2
    re-run against the ORIGINAL slices -> reader A: True  reader B: True
```
N = 2 is COUNTED by the script across the two slices (one blank-line-separated
paragraph each); no number from the block was asserted.

(ii) `.agent/prose_slips.md` ← SLIPS49, inside C2, reading (a) alone:
```
pre  @C1: 240453 1dc6ccf4cecd90b5d0d1e6685c0d5b00f5ccd2219f6e5f3dae6baaa0d42b06fc
post @C2: 241765 b8e2e3f9107755d751d9c7ad3819f4524d2df6344ce65bab2dc5beaac1c3b5d9
SLIPS49 bytes: 1312
(a) reader A  identical: True
```

(iii) `.agent/live_review.md` ← LANDED49, pre at C3 and post at C4, reading (a) alone:
```
pre  @C3: 898518 a75524fd81467897219cb4726412575cc7e08abafa0083ca3df3980da360bd04
post @C4: 898808 fe28f08b0f9b76869bb4b5a5117514da36c5a8aae08cc4821a777ef6f7e3fb14
LANDED49 bytes: 290 sha256=1c64b978b69282cbffd68f1d489807451f80f7b90e4e6393c4161b5e30a61231
(a) reader A identical: True
```
All four appends are `old_bytes + slice_bytes`; each slice's own leading blank line
is inside the slice, all pre-blobs ended in a newline and none was added.

**G4 THE TWO PAIRS, at C3, against COMMITTED blobs — PASS, exit 0.**
```
--- PAIR49A  packages/orchestration/do_run.py
    containment test output: TO contains FROM: false
    FROM count in base blob 70d6c8e6: 1   (block states 1)
    FROM count in C3 blob   9df09805: 0   (must be 0)
    TO   count in C3 blob   9df09805: 1   (must be 1)
    REBUILD base+pair == C3 blob: True  (both 22986 B, sha256 61630d22f64d30423b5efee4ebd80911da2cf584afe0c17e28e47886ba7de198)
--- PAIR49B  packages/orchestration/test_failure_artifact.py
    containment test output: TO contains FROM: false
    FROM count in base blob 70d6c8e6: 1   (block states 1)
    FROM count in C3 blob   9df09805: 0   (must be 0)
    TO   count in C3 blob   9df09805: 1   (must be 1)
    REBUILD base+pair == C3 blob: True  (both 15581 B, sha256 4ee467981534ea3032e42e874ec5d9545e211550dee91ece476120d37e0fedbd)
```
FROM and TO were each extracted as their own slice from the committed authored blob;
neither side was retyped. FROM/TO byte counts and digests: PAIR49A 61 B
`66917cd9…` → 61 B `21832456…`; PAIR49B 73 B `28ecd8ba…` → 73 B `25448b6d…`.

**G5 THE TWO GUARDS, at C3, by ORDERED EQUALITY — PASS, exit 0.**
```
--- GUARD49A  tests/orchestration/test_do_run.py
    base blob 70d6c8e6 is a byte-exact PREFIX of the C3 blob: True  (base 25968 B, C3 26829 B)
    slice is a byte-exact SUFFIX of the C3 blob: True  (slice 861 B sha256 e1f8019398900197dd28341b28d9fe9aa8a87c55860c1cfd40095b37be4f7c6c)
    C3 diff ADDS 21 lines for this path; slice has 21; equal IN ORDER: True
    whole-blob identity base+slice == C3: True
--- GUARD49B  tests/orchestration/test_test_failure_repair.py
    base blob 70d6c8e6 is a byte-exact PREFIX of the C3 blob: True  (base 33134 B, C3 34242 B)
    slice is a byte-exact SUFFIX of the C3 blob: True  (slice 1108 B sha256 c6947d4803d90fa1e9dc9e298500c41e42d17416aff433b306e86815de4f6eb4)
    C3 diff ADDS 26 lines for this path; slice has 26; equal IN ORDER: True
    whole-blob identity base+slice == C3: True
```
No per-line multiplicity count was attempted; both slices repeat blank lines and
`assert` lines structurally, so multiplicity is unattainable by construction.

**G6 THE REPAIR WORKS AND NOTHING NEAR IT MOVED, at C3 — (a) PASS, (b) CONTRADICTION
DECLARED, (c) PASS.**

(a) exit 0, all four digests equal the reviewer's own measurement:
```
C3   packages: 1f1a040413f8045a9e53ec8dece733ddb1d0c0ac   (block: 1f1a0404…)
C3   tests:    b33e3ac3ed64ebd1d6fa4e0b86c9f8614c4d07ee   (block: b33e3ac3…)
BASE packages: 18aadcb1ca69b2aa25a14044750bbe2e0883d2d0   (block: 18aadcb1…)
BASE tests:    67b33dc0be4345b55badd92b1af6b1af105cfffd   (block: 67b33dc0…)
```

(b) exit 0, but the reading CONTRADICTS the block — every row measured is reported:
```
$ git diff --numstat 70d6c8e6..9df09805        # the command the gate names
314   0   .agent/authored/f275-r49.md
247 358   .agent/last_block.md
  4   0   .agent/live_review.md
 17  17   .agent/plan.md
  2   0   .agent/prose_slips.md
  1   1   packages/orchestration/do_run.py
  1   1   packages/orchestration/test_failure_artifact.py
 21   0   tests/orchestration/test_do_run.py
 26   0   tests/orchestration/test_test_failure_repair.py
                                               # NINE rows, not four
$ git diff --numstat 9df09805^..9df09805       # C3's OWN diff
  1   1   packages/orchestration/do_run.py
  1   1   packages/orchestration/test_failure_artifact.py
 21   0   tests/orchestration/test_do_run.py
 26   0   tests/orchestration/test_test_failure_repair.py
                                               # exactly the four rows, with the four stated numerals
```
Nothing was edited to make the two agree. See Deviations.

(c) the SCOPED round gate and the canary, in the PRIMARY checkout at C3, porcelain
empty before both:
```
$ python3 -m pytest tests/orchestration/test_do_run.py tests/orchestration/test_test_failure_repair.py \
    tests/orchestration/test_repair_loop_v1.py tests/cli/test_repair_runtime.py \
    tests/orchestration/test_ci_budgets.py -q
175 passed in 2.93s
REAL_EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 18.83s
REAL_EXIT=0
```
`175 passed` and `42 passed` are exactly the figures the block's "WHAT THE REVIEWER
ALREADY MEASURED" paragraph states. `test_ci_budgets.py` is inside the green
selection, so the ruff count is still at its frozen ceiling of 26.

**G7 THE RED PROOF, at C3, in a disposable worktree — PASS, exit 0, TWO MUTATIONS,
NODE-ID SETS DISJOINT.** Worktree `.remedy-wt/r49-wt`, detached at `9df09805`, never
`cd`-ed into: every command ran as `subprocess.run([...], cwd=<abs worktree>)` under
`python3 -B` with `-p no:cacheprovider`, `__pycache__` purged before every run (0 dirs
found each time — the worktree was freshly checked out and `-B` writes none), and the
imported module path PRINTED before any result was believed. It resolved to the
WORKTREE, not to an install or to the primary checkout:
```
do_run                -> /home/decodeux/Repos/remedy/.remedy-wt/r49-wt/packages/orchestration/do_run.py
test_failure_artifact -> /home/decodeux/Repos/remedy/.remedy-wt/r49-wt/packages/orchestration/test_failure_artifact.py
```
Selection for EVERY run, both node ids together:
`tests/orchestration/test_do_run.py::TestSystemArtifactKeepsTaskIdAbsent` and
`tests/orchestration/test_test_failure_repair.py::TestSystemArtifactKeepsTaskIdAbsent`.

| # | Run | Exit | Last line | FAILED node ids |
|---|---|---|---|---|
| 1 | CONTROL, unmutated | 0 | `2 passed in 1.08s` | `[]` |
| 2 | M1 — PAIR49A TO→FROM in `do_run.py` (TO count in THAT FILE first: **1**) | 1 | `1 failed, 1 passed in 0.34s` | `tests/orchestration/test_do_run.py::TestSystemArtifactKeepsTaskIdAbsent::test_the_build_phase_on_a_task_less_job_leaves_task_id_absent` |
| 3 | REVERT M1 | — | sha256 before `61630d22f64d30423b5efee4ebd80911da2cf584afe0c17e28e47886ba7de198`, after `61630d22f64d30423b5efee4ebd80911da2cf584afe0c17e28e47886ba7de198` | byte-exact: True |
| 4 | M2 — PAIR49B TO→FROM in `test_failure_artifact.py` (TO count in THAT FILE first: **1**) | 1 | `1 failed, 1 passed in 0.33s` | `tests/orchestration/test_test_failure_repair.py::TestSystemArtifactKeepsTaskIdAbsent::test_a_failure_without_a_task_leaves_task_id_absent` |
| 5 | REVERT M2 | — | sha256 before `4ee467981534ea3032e42e874ec5d9545e211550dee91ece476120d37e0fedbd`, after `4ee467981534ea3032e42e874ec5d9545e211550dee91ece476120d37e0fedbd` | byte-exact: True |
| 6 | CONTROL again | 0 | `2 passed in 0.31s` | `[]` |

Both digests were recorded BEFORE their mutation, against the file on disk, and the
revert was proved against that recorded digest.
```
intersection : []
DISJOINT     : True
```
M1 reddens the `test_do_run.py` guard and M2 the `test_test_failure_repair.py` guard,
each and only its own — which is what makes TWO mutations necessary: neither alone
proves the other fix. The assertion both go red on, captured from a run with BOTH
sites mutated, is the defect in the assertion's own words:
```
E       AssertionError: assert 'None' is None
E        +  where 'None' = Artifact(… name='fixture-build-output' …).task_id
E       AssertionError: assert 'None' is None
E        +  where 'None' = Artifact(… name='test-failure-temp' …).task_id
2 failed in 0.36s
```
Worktree removed and pruned before this handback; `git worktree list` reads ONE entry.

**G8 NOTHING ELSE MOVED, at C4 — PASS, exit 0.**
```
.agent/STOP exists on disk (re-read from disk, not remembered): False
git status --porcelain == '' : True   literal: ''
changed-path set over 70d6c8e6..31e37b27, size: 9
MISSING: []
EXTRA  : []
paths under apps/ docs/ scripts/: []
.agent/decisions.md in set: False
```
THE OPEN SET, BY DISTINCT ID over `.agent/live_review.md` — distinct `^- R-\d+ — `
minus distinct `^Done: R-\d+ — `:
```
base 70d6c8e6: 104 - 18 = 86
C4   31e37b27: 105 - 18 = 87
ids registered this round: ['R-0876']
ids resolved  this round: []
C3: ^Landed: R-0876  count = 0    ^Done: R-0876  count = 0
C4: ^Landed: R-0876  count = 1    ^Done: R-0876  count = 0
```
Per-commit insertions against the F104 D1 cap of 500, derived ONCE from
`git show --numstat <sha>` and reused in the `## Commits` tables above:
```
C0a 67209157: insertions=314 deletions=0    under 500: True
C0b 17d602ad: insertions=247 deletions=358  under 500: True
C1  365c4cf4: insertions=17  deletions=17   under 500: True
C2  509f3180: insertions=6   deletions=0    under 500: True
C3  9df09805: insertions=49  deletions=2    under 500: True
C4  31e37b27: insertions=2   deletions=0    under 500: True
```
No commit is oversize; no oversize declaration is made or needed this round.

**Push.** Ordered after C5, so its exit code cannot be recorded inside the file C5
commits. No outcome is claimed; the reviewer reads it from
`git log origin/feature/f275-one-world-completion-part-three`.

## Authored-text proofs

Every slice was extracted MECHANICALLY from the COMMITTED blob of
`.agent/authored/f275-r49.md` at `67209157`, by its `BEGIN-<name> ` / `END-<name> `
marker-line PREFIX, with the marker lines excluded and each body line carrying its own
trailing newline. The extractor asserts exactly one BEGIN and one END per name and
that BEGIN precedes END. No slice was retyped, reflowed or edited.

| Slice | Bytes | sha256 | Applied to | Disk-to-disk result |
|---|---|---|---|---|
| PLAN49 | 2557 | `abf50111b70af3357478ee0f27cf582d9642a9f2097552a6b37c1e23bf3d2ea6` | `.agent/plan.md` (whole-file) | byte-equal: True |
| RECORD49 | 3921 | `814f40b17b1f05c42a23a6502cdd4f11278d85fc3da733517d7fa6baceba500a` | `.agent/live_review.md` (append) | reader A + reader B True, control rejected |
| FIND49 | 2201 | `30a39a40433a4f49f82f5751be98b3ac41678fc92a516cfbd8e75625221dc499` | `.agent/live_review.md` (append) | reader A + reader B True, control rejected |
| SLIPS49 | 1312 | `1b7c5ece0821d95f73b3d933c84d2342f1053ef5fadf68b059687ae3efb7784f` | `.agent/prose_slips.md` (append) | reader A True |
| PAIR49A_FROM | 61 | `66917cd91aa615c8baef94b9360b71b2d3e867145f6a3ab587d93e28ebee4790` | `packages/orchestration/do_run.py` | FROM 1 → 0 |
| PAIR49A_TO | 61 | `21832456e7a4e1911d351f1be92035ab0532f43d7b41804212c47d7bb69e31e7` | `packages/orchestration/do_run.py` | TO 0 → 1, rebuild identical |
| PAIR49B_FROM | 73 | `28ecd8baf68fae0e8a8749ffc9d612523dcdc889b8ee5778b882f626f9ba9431` | `packages/orchestration/test_failure_artifact.py` | FROM 1 → 0 |
| PAIR49B_TO | 73 | `25448b6dbd68d16f938667191dc3b86ccce87d0189f480654febcdda41e23f65` | `packages/orchestration/test_failure_artifact.py` | TO 0 → 1, rebuild identical |
| GUARD49A | 861 | `e1f8019398900197dd28341b28d9fe9aa8a87c55860c1cfd40095b37be4f7c6c` | `tests/orchestration/test_do_run.py` (code append) | prefix + suffix + ordered-line equality True |
| GUARD49B | 1108 | `c6947d4803d90fa1e9dc9e298500c41e42d17416aff433b306e86815de4f6eb4` | `tests/orchestration/test_test_failure_repair.py` (code append) | prefix + suffix + ordered-line equality True |
| LANDED49 | 290 | `1c64b978b69282cbffd68f1d489807451f80f7b90e4e6393c4161b5e30a61231` | `.agent/live_review.md` (append) | reader A True |

Transport of the block itself: `.agent/authored/f275-r49.md` and
`.agent/last_block.md` are both 28474 bytes at
`37081bec7b73c5e7d4de0fbf52ac2dc249a2dccc62ace4d6f92f7b37afadb113`, identical to
`.remedy-wt/f275-r49.block.md` and to the ordered digest.

## Deviations & assumptions

1. **G6(b) contradicts its own reading — declared, nothing edited.** The gate says
   "`git diff --numstat 70d6c8e6..C3` reads exactly four rows". It reads NINE. The
   range `70d6c8e6..C3` spans C0a, C0b, C1, C2 AND C3, so it necessarily also carries
   the five `.agent/` state rows those four commits wrote. Both readings are reported
   in full in Verification. The gate's SUBSTANCE holds exactly as stated: C3's own
   diff (`9df09805^..9df09805`) is exactly four rows and exactly the four stated
   numerals — 1/1 `do_run.py`, 1/1 `test_failure_artifact.py`, 21/0 `test_do_run.py`,
   26/0 `test_test_failure_repair.py`. Only the COMMAND and its row count disagree.
   Per the order, no file was changed to make the two agree.
2. **`.agent/STOP` re-read from disk before the first commit (constraint 8):** ABSENT.
   `ls .agent/STOP` → "No such file or directory"; re-read again at G8 via
   `Path(...).exists()` → False.
3. **The commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly** — none
   merged, none reordered, none added, none dropped. C4 was written only after C3 was
   committed, as constraint 2 requires of a `Landed:` line.
4. **A worker-side probe defect, found and fixed inside the round, no file affected.**
   The first G7 run parsed a pytest node id as `line.split(" ")[0]`, which yields the
   literal token `FAILED` for every failure and therefore reported the two mutation
   sets as NON-disjoint. The parser was corrected to take what follows the FIRST space
   of a `FAILED <nodeid> - <msg>` line and G7 was re-run in full from the control. Both
   runs are real; only the corrected one is reported as the gate, and the defect was in
   the throwaway probe under `.remedy-wt/`, never in a committed file.
5. **No `Done:` paragraph was written** (constraint 5). This round REGISTERS `R-0876`
   and RESOLVES nothing: the open set goes 86 → 87. The `Landed: R-0876` line at C4 is
   the worker's record that the fix is committed; the reviewer's authored `Done:` is
   owed at the next gate.
6. **`.agent/decisions.md` was not touched**, and no path under `apps/`, `docs/` or
   `scripts/` moved. This round makes no new decision — it repairs a defect an existing
   one caused.
7. **Scratch.** All probe scripts live under the gitignored `.remedy-wt/r49/`, and the
   G7 worktree lived under `.remedy-wt/r49-wt`. Nothing under `.remedy-wt/` is
   committed; `git status --porcelain` is empty.
8. No PR was created, edited or merged. No `remedy` CLI command was run.
9. **No SHA is written that was not measured.** C5's own SHA and the push result do
   not exist while this file is being written, so the Range line, the C5 commit table
   heading and the push row all name the fact instead of a numeral. Every other SHA in
   this handback came from `git log`, `git rev-parse` or `git show`.

## Open findings

87 by distinct id (105 registrations − 18 `Done:`), up one from the base's 86:
`R-0876` registered this round, none resolved. Four are High — R-0803, R-0804,
R-0806 and R-0807 — all F273's, per DECISION F272 D12.

## Next

The reviewer re-derives round 49's eight gates from the committed range
`70d6c8e6`..C5 and issues its verdict, which includes the authored `Done:
R-0876` paragraph this round is forbidden to write. Before authoring anything it
re-reads `.agent/STOP` from disk (Phase 1 rule 1) and then runs the Open PR Gate
(rule 2). The next production step is plan step 1: RE-RUN THE FLIP DRY RUN against a
tree whose id shape is now one spelling, and re-classify the residue
`.agent/f275_t003_flip_residue.md` records at 2714 failures.

## Reviewer verdict on round 49 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 49: **PASS.** Written by the planner and reviewer of SESSION 19 after reading the committed
range `70d6c8e6`..`31e37b27` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the
worker's report was evidence for no line below. It is carried here because under
`docs/agents/self_drive_protocol.md` a verdict that stays in the session is lost, and it is booked into
`.agent/live_review.md` by the FIRST SUBSTANTIVE COMMIT of round 50, per amend0827-process-diet rule 1.

THE REPAIR IS RIGHT AND BOTH HALVES ARE PROVED SEPARATELY. G1 is the PRIMARY cmp-against-scratchpad proof
and not the §4.9 digest fallback: the reviewer's scratch original survived and the saved copy, its mirror and
that original are one blob at 28474 bytes and sha256
`37081bec7b73c5e7d4de0fbf52ac2dc249a2dccc62ace4d6f92f7b37afadb113`. G2: `.agent/plan.md` byte-identical to
PLAN49 at 2557 bytes over 45 lines. G3: all four appends reconstruct exactly — `.agent/live_review.md`
892396 to 898518 across RECORD49 and FIND49 together, `.agent/prose_slips.md` 240453 to 241765, and
`.agent/live_review.md` again 898518 to 898808 for LANDED49 at C4 — with reader B true at N counted from the
slices, N being 2, and the negative control rejected by BOTH readers with the flipped byte inside the FIRST
appended paragraph. G4: both pairs are REWRITES on the containment test's own output, FROM reads 1 in each
base blob and 0 in each C3 blob, TO reads 1, and the reviewer rebuilt each C3 blob from its base blob by
applying that pair alone — byte-identical both times. G5: both guards are CODE APPENDS proved by ordered
equality rather than by a multiplicity count — each base blob is a byte-exact PREFIX of its C3 blob, each
slice a byte-exact SUFFIX, and `base + slice == C3` exactly at 25968+861 and 33134+1108. G6: both subtree
digests equal the reviewer's own replay of this repair on a clean checkout — `packages` at
`1f1a040413f8045a9e53ec8dece733ddb1d0c0ac` and `tests` at `b33e3ac3ed64ebd1d6fa4e0b86c9f8614c4d07ee` — and
C3's own diff is exactly the four ordered rows. The reviewer re-ran the scoped selection itself at
`175 passed` and the canary at `42 passed`, both exit 0. G8: the changed-path set matches exactly with
MISSING and EXTRA both empty, `.agent/decisions.md` untouched, zero paths under `apps/`, `docs/` or
`scripts/`, the open set 86 to 87 with `R-0876` the only id registered and none resolved, and
`^Landed: R-0876 ` 0 at C3 and 1 at C4 against `^Done: R-0876 ` 0 at both.

G7 IS THE GATE THIS ROUND EXISTS FOR AND THE REVIEWER RE-RAN IT AT THE COMMITTED C3. The control reads
`2 passed` at exit 0; M1 reverting PAIR49A reddens ONLY the `test_do_run.py` guard; M2 reverting PAIR49B
reddens ONLY the `test_test_failure_repair.py` guard; THE TWO NODE-ID SETS ARE DISJOINT, which is why two
mutations were ordered rather than one — neither fix's proof covers the other. Both reverts are byte-exact by
sha256, the control is green again, and the PRIMARY checkout's porcelain read empty in the same command
sequence as every mutation.

THE WORKER DECLARED ONE CONTRADICTION AND IT WAS THE REVIEWER'S. G6(b) named the command
`git diff --numstat 70d6c8e6..C3` and asserted it "reads exactly four rows"; that range spans C0a through C3,
so it necessarily also carries the five `.agent/` rows those earlier commits wrote, and it reads NINE. The
worker reported both readings, measured C3's OWN diff at exactly the four stated rows with exactly the four
stated numerals, and edited nothing. It also found and fixed a node-id parser defect in its own throwaway
probe before reporting G7, which is the difference between a gate and a number. Nothing on disk is wrong, so
the reviewer's range error is a dated line in `.agent/prose_slips.md` and not an id.

## Authored text for round 50 to book — the resolution of R-0876

Done: R-0876 — RESOLVED at F275 round 49's C3 `9df09805`. THE DEFECT: round 48's slice WIDEN48 wrapped every construction keyword it rewrote in `str(...)` unconditionally, because `ast` gives a generator no way to know whether an expression is nullable, and at two production sites the wrapped expression could evaluate to `None` — `packages/orchestration/do_run.py` in `_run_build_phase`, where a job with no tasks has no task to attribute its artifact to, and `packages/orchestration/test_failure_artifact.py` in `persist_failure_artifact`, where `TestFailureArtifact.task_id` defaults to the empty string. Both wrote the string `"None"` where `packages/core/models.py` documents an absence in the `Artifact` docstring itself, and `artifact_index.task_artifacts_by_kind` matches that field by equality, so the stored value was a truthy string no lookup could ever match. THE FIX moves the `str(...)` inside each conditional's true branch, so the false branch yields `None` again; it is one line per site and it changes nothing on the populated branch, where `str(UUID)` is what the widened field already required. THE GUARD, and why there are two: each site gained a test that constructs the artifact through the REAL function on the absent branch and asserts `task_id is None`, and the two are red-proved SEPARATELY because one mutation cannot establish two fixes — reverting the `do_run.py` line reddens only `tests/orchestration/test_do_run.py::TestSystemArtifactKeepsTaskIdAbsent`, reverting the `test_failure_artifact.py` line reddens only `tests/orchestration/test_test_failure_repair.py::TestSystemArtifactKeepsTaskIdAbsent`, and the reviewer measured the two FAILED node-id sets DISJOINT in its own disposable worktree at `9df09805`. Both guards fail on `assert 'None' is None`, which states the defect in the assertion's own words. THE RULE THIS LEAVES BEHIND, and it is the reason the finding was worth an id rather than a quiet fix: a mechanical rewrite that wraps an expression states what it assumes about that expression's NULLABILITY, and where the generator cannot know, the BLOCK sweeps for the conditional form before emission. No gate round 48 ordered could see this — the subtree digests matched, the scoped suite read 480 passed and the canary 42 passed — because no test reached either branch, which is exactly the class `.agent/f275_t003_flip_sites.md` section 3 names as invisible to both of the flip's instruments.

## Authored text for round 50 to book — one dated line for `.agent/prose_slips.md`

2026-09-11 · F275 R49 · The round 49 block's G6(b) named the command `git diff --numstat 70d6c8e6..C3` and asserted that it "reads exactly four rows". That range spans C0a, C0b, C1, C2 AND C3, so it necessarily also carries the five `.agent/` state rows those earlier commits wrote, and it reads NINE. The four production rows and all four of their numerals are correct — they are C3's OWN diff, which the worker measured at `9df09805^..9df09805` and reported beside the nine-row reading, editing nothing. This is §3 item 22's class, a sentence quantifying across COMMITS that was written against the commit it meant rather than the range it named, and it is the second range-versus-commit slip of this session after round 46's G8. THE RULE THAT FOLLOWS: a gate that means ONE commit's diff names that commit's own range as `<sha>^..<sha>`, and a gate that means the round's cumulative change says so and states the row count it expects for the whole of it.

## Session 19 ends here — FOUR delegated rounds, three PASS and one FAIL

Rounds 46, 47, 48 and 49. THE FAIL WAS THE REVIEWER'S OWN SLICE, not the round that executed it, and it was
found by the worker rather than by any gate the block ordered.

WHAT THIS SESSION LANDED, and the through-line is that a DRY RUN THAT IS ACTUALLY RUN decides the plan.
Session 18 closed naming THE FLIP as the next round's work and calling it "a mechanical transformation with
every prerequisite measured". Before authoring it the reviewer applied it in a disposable worktree at
`978046fe` and ran it. IT CONVERGES AS AN EDIT AND NOT AS A CHANGE: 282 files rewritten, 5388 insertions,
zero left unparsable, 18394 tests collected with zero collection errors — and then 2714 failed, 15551 passed
and 106 errors at exit 1. `.agent/f275_t003_flip_residue.md` records that run with its instrument and its
classification. The largest class no decision had ruled was THE ID SHAPE: `Job.id` and `Task.id` are
`uuid.UUID` while the unified record spells both `str`, and three models the flip never touches — `Artifact`,
`TaskExecutionContext` and `PatchIntentSet` — declare that type on fields the flip feeds. DECISION F275 D26
ruled the shape migrated first. D27 ruled it landed one model at a time and measured the order. D28 corrected
D27's unit: `PatchIntentSet.task_id` is assigned FROM `Artifact.task_id` at one production site, so the two
are one commit and not two, and the atomic unit of an id-shape widen is the assignment-connected component
rather than the model. ALL FOUR FIELDS THE FLIP FEEDS NOW HOLD ONE SPELLING, and R-0876 — the one defect that
migration landed — is fixed and guarded twice over.

THE BRANCH IS GREEN AT A READING THIS SESSION TOOK AND NOTHING ON IT HAD TAKEN BEFORE: the FULL suite at
`013e5517` reads `18371 passed, 23 skipped, 1 warning` at exit 0, and the same figure holds on the round 47
and round 48 trees. That reading is the control every dry-run figure in this session is quoted against, and it
is why the four `tests/test_grouped_cli.py` failures D27 records could be called caused rather than flake.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: the reviewer's context is
comfortable and exhaustion is expressly NOT why this session ends — it ends at the four-round floor because
the next step is a full re-run of the flip dry run against the new id shape, which is a fresh measurement
rather than a continuation of this session's, and because two of this session's four blocks carried a
range-versus-commit slip, which is the authoring signal amend0908-f275-finish rule 5 permits F275 to cite only
after four delegated rounds — exactly where this session is.

## What the next session owes, in order

FIRST, Phase 1 rule 1: re-read `.agent/STOP` from disk before the Open PR Gate. It did not exist at this
session's Phase 0 probe, was measured absent before every round's first commit, and is absent as this session
ends. Then the Open PR Gate: no pull request is open, and none is owed until the closure sequence.

SECOND, round 50's FIRST SUBSTANTIVE COMMIT books, from this file as the durable carrier under
amend0827-process-diet rule 1, the ROUND 49 PASS verdict above as a `Gate: F275 R49` entry in
`.agent/live_review.md`, the authored `Done: R-0876` paragraph, and the one dated line above into
`.agent/prose_slips.md`. Booking that resolution takes the open set from 87 to 86 by distinct id; the next
free id is `R-0877`.

THIRD, SESSION 20 IS F275's TWENTIETH AND THE SOFT LIMIT amend0908-f275-finish rule 1 names is 20 SESSIONS
and 60 ROUNDS. The session therefore owes a SCOPE REPORT in its handback — what is finished, what is missing,
and a proposal — and it carries the unmissable line `SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER
ÜBERGABE`. That same rule 2 forbids the amend0905-throughput split-and-close default here BY NAME: on
reaching the limit the session writes the report and CONTINUES, and the only permitted early close is the old
hard stop with an operator question, and only when a module group is genuinely undeletable under the three
rules in `docs/roadmap/features/T2_F275.md` T001. Write the report, then keep going.

FOURTH, THE WORK ITSELF: re-run the flip dry run against a tree whose id shape is one spelling, and
re-classify the residue. `.agent/f275_t003_flip_residue.md` records 2714 failures in six classes measured
BEFORE the migration; the 256 hexadecimal-UUID failures and the 369 model-validation failures against
`Artifact` and `TaskExecutionContext` are the ones the migration was performed to remove, and whether they
are gone is a measurement and not a prediction — take it before authoring anything. What remains after that
are transform rules, and section 3 of that artefact enumerates four of them already: the type imports move
their MODULE PATH, a MIXED import is SPLIT rather than moved, the seam's own imports move with the seam, and
a construction whose keywords arrive through a `**` splat is invisible to a keyword rewrite. Round 48 found a
fifth by failing: a generator that resolves a constructor by its CALLED NAME is blind to an import ALIAS.
Then THE FLIP, still as the one declared-oversize commit AGENTS.md permits per feature, declared with its
inseparability reason before review — and F275's one such allowance is still unspent at 49 rounds.
