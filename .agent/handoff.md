# Handback — F275 round 50

## Session

SESSION 20 of feature F275 · round 50 · rounds so far 50

Context self-assessment (amend0905-throughput): context is comfortable — this round
read AGENTS.md in full, verified and copied a 41409-byte block, applied six slices,
and spent the rest on seven gate runs including a 12529-byte artefact whose embedded
instrument was extracted from its own committed blob and executed; there is room for
at least one more round this session.

F275 stands at 50 rounds and 20 sessions against the operator's soft limit of 60 rounds
and 20 SESSIONS (amend0908-f275-finish rule 1). THE SESSION LIMIT IS REACHED. The SCOPE
REPORT that rule obliges is owed by the SESSION and is written into the handback of the
LAST round of this session, not by this round — the block states this explicitly. Rule 2
forbids the amend0905-throughput split-and-close default here BY NAME: the session writes
the report and CONTINUES. This round closed nothing, registered no follow-up feature and
did not touch `docs/roadmap/STATUS.md`.

## Range

Review of `020b1d57`..C5, where C4 is `69d1e673` and C5 is the commit that writes this
file. C5's own SHA is NOT stated here: it does not exist while this file is being
written, and no SHA is written that was not measured.

## Commits

### 801c3e90 F275 R50 C0a: save the round 50 step block verbatim.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r50.md` | +477 / -0 | the round 50 block, saved by `shutil.copyfile` from `.remedy-wt/f275-r50.block.md`, never retyped; every slice this round applies is extracted from THIS file's committed blob |

### c7439c12 F275 R50 C0b: mirror the round 50 block into the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +413 / -250 | written from `git cat-file blob 801c3e90:.agent/authored/f275-r50.md` read into memory, not retyped; replaces the round 49 block |

### 1f131ef2 F275 R50 C1: advance the plan to round 50, the flip re-run and its three prerequisites.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +22 / -22 | whole-file replacement by slice PLAN50; Current Step becomes round 50, Next Steps put P1/P2/P3 BEFORE the flip, Risks re-state the open set at 86 and the session limit |

### 591c3050 F275 R50 C2: book the round 49 PASS verdict, resolve R-0876 and record one reviewer slip.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | appends RECORD50 (the round 49 PASS verdict) then DONE50 (the authored `Done: R-0876` resolution), in that order |
| `.agent/prose_slips.md` | +2 / -0 | appends SLIPS50, one dated line on the round 49 block's G6(b) range-versus-commit slip |

### e938607c F275 R50 C3: record the flip re-run against the migrated id shape and its instrument.
| Path | +/- | Reason |
|---|---|---|
| `.agent/f275_t003_flip_residue_r50.md` | +224 / -0 | NEW file, whole-file write of slice ARTEFACT50; the reviewer's controlled dry run at `020b1d57`, its residue classification and the embedded instrument that reproduces half of it. `.agent/f275_t003_flip_residue.md` is NOT edited — it records the run at `978046fe` and stays as written |

### 69d1e673 F275 R50 C4: rule DECISION F275 D29, the three prerequisites the flip still has.
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +14 / -0 | appends DEC50 — DECISION F275 D29: the id-shape migration did exactly what it was performed to do, the flip still does not converge, and P1/P2/P3 precede it |

### C5 (SHA unmeasurable from inside itself) F275 R50 C5: the round 50 handback.
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
| R-0876 | resolved | `Done:` booked at C2; the `Landed: R-0876` line from round 49 survives beside it |
| DECISION F275 D29 | done | appended at C4, 1 occurrence at C4 and 0 at C3 |

## External actions

| Command | Outcome |
|---|---|
| `git worktree list` | ONE entry: `/home/decodeux/Repos/remedy 020b1d57 [feature/f275-one-world-completion-part-three]` at the start of the round. No worktree was created or removed this round |
| `git push -u origin feature/f275-one-world-completion-part-three` | ordered and executed immediately AFTER C5. Its outcome is by construction unrecordable here — a handback cannot report a push that follows it — so no outcome is claimed; the reviewer reads it from `git log origin/feature/f275-one-world-completion-part-three` |

No PR created, edited or merged. No force-push, no history rewrite, no branch deleted.
No `remedy` CLI command was run.

## Verification

SEVEN gates run, G1 through G7 — the number is the worker's own count; the block
states none. Every one run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`.

**G1 TRANSPORT, at C0b — PASS, exit 0.** The chain the proof walked has four links
and no retyped byte: `.remedy-wt/f275-r50.block.md` → (`shutil.copyfile`) →
`.agent/authored/f275-r50.md` on disk → (`git commit`) → the committed blob at
`801c3e90` → (`git show <blob>` into memory) → `.agent/last_block.md`. Both committed
blobs read at C0b:
```
authored   bytes=41409 sha256=9dce5f36949d1e3995281ee5d0de18b19376224fcfd8c2ab4079ee153e025fcf
last_block bytes=41409 sha256=9dce5f36949d1e3995281ee5d0de18b19376224fcfd8c2ab4079ee153e025fcf
delegated  sha256=9dce5f36949d1e3995281ee5d0de18b19376224fcfd8c2ab4079ee153e025fcf
authored == delegated digest : True
mirror    == authored blob   : True
both byte counts equal       : True
G1 OK: True
REAL_EXIT=0
```
The block carries `BEGIN-`/`END-` marker lines for its SLICES only and no BEGIN marker
of its own, so the digest is the whole identity. Nothing is claimed about the bytes
emitted into the worker's prompt — the proof never reads them.

**G2 THE PLAN, at C1 — PASS, exit 0.**
```
PLAN50 slice bytes=2578 sha256=9b9d56341fc2aca44a1af2d56257fa6d33e606c812be2031e24fd6cd4a3a9fee
plan.md   C1 bytes=2578 sha256=9b9d56341fc2aca44a1af2d56257fa6d33e606c812be2031e24fd6cd4a3a9fee
byte-equal: True
line count=45 against the AGENTS.md cap of 50 : True
^## Goal$ count=1 (must be 1)
^## Next Steps$ count=1 (must be 1)
G2 OK: True
REAL_EXIT=0
```

**G3 THE RECORD AND THE SLIPS, at C2 — PASS, exit 0.** Every pre and post blob read
with `git show <sha>:<path>` INTO MEMORY; no non-current revision was ever written over
a tracked file.
```
(i) .agent/live_review.md <- RECORD50 then DONE50
  (a) reader A: pre=898808 + slices=6251 -> 905059 vs post=905059 | identical: True
  (b) reader B: N COUNTED from the slices = 2; last 2 blank-line units equal them IN ORDER: True
  (c) negative control: flipped byte at offset 900707, inside the FIRST appended paragraph
  (c)A reader A: pre=898808 + slices=6251 -> 905059 vs post=905059 | identical: False
  (c)B reader B: N COUNTED from the slices = 2; last 2 blank-line units equal them IN ORDER: False
  (c) reader A rejects: True | reader B rejects: True
(ii) .agent/prose_slips.md <- SLIPS50, reading (a) alone
  (a) reader A: pre=241765 + slices=964 -> 242729 vs post=242729 | identical: True
G3 OK: True
REAL_EXIT=0
```
N = 2 is COUNTED by the script across RECORD50 and DONE50 (one blank-line-separated
paragraph each); no number from the block was asserted. Both `(c)` readers were re-run
against the ORIGINAL slices — the mutated blob is the post side in both, never the
slices. Slice byte counts: RECORD50 3798, DONE50 2453, SLIPS50 964; each leading byte
is `\n` and each trailing byte is `\n`, both pre-blobs ended in a newline and none was
added.

**G4 THE ARTEFACT, at C3 — PASS, exit 0.**
```
ARTEFACT50 slice bytes=12529 sha256=3d03d5d2969589f190c3dd7f68ef3388dca790d64ff15314ddf9e0c1dcb6506e
.agent/f275_t003_flip_residue_r50.md C3 bytes=12529 sha256=3d03d5d2969589f190c3dd7f68ef3388dca790d64ff15314ddf9e0c1dcb6506e
byte-equal: True
git show 591c3050:.agent/f275_t003_flip_residue_r50.md -> exit 128 (non-zero => the path does not exist at C2, so C3 is an ADDITION)
fenced blocks between the marker and the close: 1 (must be 1)
instrument bytes=2741 sha256=6b4075877f968b22d4b1c314f8e410c0442a7a1930a23a23e4d63b193f36da59 -> .remedy-wt/r50_instrument.py
instrument exit=0
recorded lines=26 actual lines=26
recorded == actual : True
G4 OK: True
REAL_EXIT=0
```
The exit code that makes this an addition rather than a rewrite is **128**. The
instrument was extracted from the COMMITTED C3 blob — the single fenced `python` block
following the `<!-- INSTRUMENT -->` line, marker line and both fence lines excluded —
written under the gitignored `.remedy-wt/` and run as `python3 -B .remedy-wt/r50_instrument.py .`
from the repository root. Its stdout was compared LINE BY LINE against the indented
block the artefact records after `complete and untrimmed:`, four leading spaces
stripped from each line: all 26 lines equal, so no diff is printed because there is
none. The reproduced output is:
```
tracked .py: 993 | scanned after the transform's exclusions: 989
D1 T2 JOB-FIELD edits: 1896 over 19 distinct receiver names
     1802  job
       33  j
        6  parent_job
        6  job_one
        6  plan_less
        5  job_node
        5  _Job
        4  job_stub
        4  cli_job
        4  job_two
D1 T3 TASK-FIELD edits: 532 over 11 distinct receiver names
      272  task
      235  t
        8  fix_task
        6  pending_task
        3  repair_task
        3  task_node
        1  verify_task
        1  real_task
        1  ptask
        1  awaiting_task
D2   637  uuid4                  in 144 files, production 34
D2   169  UUID(job/task arg)     in 65 files, production 39
D2    49  UUID(other arg)        in 21 files, production 14
```

**G5 THE DECISION, at C4 — PASS, exit 0.**
```
reader A: pre=1085053 + DEC50=4976 -> 1090029 vs post=1090029 | identical: True
reader B: N COUNTED from the slice = 7; last 7 blank-line units equal them IN ORDER: True
negative control: flipped byte at offset 1085164, inside the FIRST appended paragraph
  reader A rejects: True | reader B rejects: True
^## DECISION F275 D29 ' at C4 = 1 (must be 1), at C3 = 0 (must be 0)
G5 OK: True
REAL_EXIT=0
```
N = 7 is COUNTED from DEC50 itself; the block asserts no number for it.

**G6 THE SCOPED ROUND GATE AND THE CANARY, in the PRIMARY checkout at C4 — PASS,
both exit 0.** `git status --porcelain` was read IMMEDIATELY BEFORE EACH and was empty
both times (`PORCELAIN_EXIT=0` with no output).
```
$ python3 -m pytest tests/ui_server/test_dashboard_contract.py \
    tests/orchestration/test_development_artifact_boundary.py \
    tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py \
    tests/orchestration/test_test_runner.py -q
161 passed in 18.25s
REAL_EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 18.79s
REAL_EXIT=0
```
`161 passed` and `42 passed` are exactly the figures the block's "WHAT THE REVIEWER
ALREADY MEASURED" paragraph states. The only claim made for the selection is the one
the block makes: it is the tests that READ the four `.agent/` files this round writes,
it reaches the state contracts and no production behaviour, and this round changes no
production behaviour to reach.

**G7 NOTHING ELSE MOVED, at C4 — PASS, exit 0.**

(a) `.agent/STOP` re-read FROM DISK and the porcelain:
```
os.path.exists('.agent/STOP') = False  -> .agent/STOP is ABSENT from disk; no stop order is in force
git status --porcelain == '' : True
```
The literal porcelain string is `''`.

(b) the changed-path set over `020b1d57..69d1e673`, with the expectation resolved
against the Change section of the committed authored blob itself and not against any
number:
```
Change section lines 18..22 of the authored blob; declared paths = ['.agent/authored/f275-r50.md', '.agent/last_block.md', '.agent/plan.md', '.agent/live_review.md', '.agent/prose_slips.md', '.agent/f275_t003_flip_residue_r50.md', '.agent/decisions.md', '.agent/handoff.md']
expected (declared minus .agent/handoff.md, which C5 writes) = ['.agent/authored/f275-r50.md', '.agent/decisions.md', '.agent/f275_t003_flip_residue_r50.md', '.agent/last_block.md', '.agent/live_review.md', '.agent/plan.md', '.agent/prose_slips.md']
actual   = ['.agent/authored/f275-r50.md', '.agent/decisions.md', '.agent/f275_t003_flip_residue_r50.md', '.agent/last_block.md', '.agent/live_review.md', '.agent/plan.md', '.agent/prose_slips.md']
MISSING = []
EXTRA   = []
paths under packages/ apps/ tests/ docs/ scripts/ = 0 (must be 0) []
```
The parser reads the backticked tokens of the `Change:` region only, stopping at the
`NO path under` line, so `.agent/f275_t003_flip_residue.md` — named in the following
sentence as the file NOT edited — is correctly excluded from the expectation, and it is
absent from the actual set.

(c) THE OPEN SET, BY DISTINCT ID over `.agent/live_review.md`:
```
base 020b1d57: registered distinct=105 resolved distinct=18 open=87 (must be 87)
C2   591c3050: registered distinct=105 resolved distinct=19 open=86 (must be 86)
ids REGISTERED this round: []
ids RESOLVED   this round: ['R-0876']
^Done: R-0876 '  at C1 = 0 (must be 0), at C2 = 1 (must be 1)
^Landed: R-0876 ' at C1 = 1 (must be 1), at C2 = 1 (must be 1)  -- the landed line survives beside its resolution
```

(d) per-commit insertions, derived ONCE from `git show --numstat <sha>` and reused in
the `+/-` column of the `## Commits` tables above:
```
C0a 801c3e90 insertions=477 <=500: True | .agent/authored/f275-r50.md +477/-0
C0b c7439c12 insertions=413 <=500: True | .agent/last_block.md +413/-250
C1 1f131ef2 insertions=22 <=500: True | .agent/plan.md +22/-22
C2 591c3050 insertions=6 <=500: True | .agent/live_review.md +4/-0 ; .agent/prose_slips.md +2/-0
C3 e938607c insertions=224 <=500: True | .agent/f275_t003_flip_residue_r50.md +224/-0
C4 69d1e673 insertions=14 <=500: True | .agent/decisions.md +14/-0
G7 OK: True
REAL_EXIT=0
```
No commit is oversize; no oversize declaration is made or needed this round. F275's one
declared-oversize allowance remains UNSPENT at 50 rounds.

**No mutation red proof was run and none is owed** (constraint 7). The change set holds
no production line, no test line and no import, so there is no code whose colour a
mutation could establish. This is stated rather than left out, because an absent red
proof is normally a finding.

**Push.** Ordered after C5, so its exit code cannot be recorded inside the file C5
commits. No outcome is claimed; the reviewer reads it from
`git log origin/feature/f275-one-world-completion-part-three`.

## Authored-text proofs

Every slice was extracted MECHANICALLY from the COMMITTED blob of
`.agent/authored/f275-r50.md`, by its `BEGIN-<name> ` / `END-<name> ` marker-line
PREFIX, with the marker lines excluded and each body line carrying its own trailing
newline. The extractor asserts exactly one BEGIN and one END per name and that BEGIN
precedes END. No slice was retyped, reflowed or edited.

| Slice | Bytes | sha256 | Applied to | Disk-to-disk result |
|---|---|---|---|---|
| PLAN50 | 2578 | `9b9d56341fc2aca44a1af2d56257fa6d33e606c812be2031e24fd6cd4a3a9fee` | `.agent/plan.md` (whole-file) | byte-equal: True |
| RECORD50 | 3798 | `326883e3f82ffd936a35f3cca21fd8b0f1efd26ec3373b70d24d6e5cc565cfbf` | `.agent/live_review.md` (append) | reader A + reader B True, control rejected by both |
| DONE50 | 2453 | `a310d03e22b11c5731ce4d31e021364c0ffc868c51c53e3a1ae6f34acf2177ea` | `.agent/live_review.md` (append) | reader A + reader B True, control rejected by both |
| SLIPS50 | 964 | `2b1678cf521061f9d2a662c7c639e0a35070cc94ba531d4995b074d179c3eb93` | `.agent/prose_slips.md` (append) | reader A True |
| ARTEFACT50 | 12529 | `3d03d5d2969589f190c3dd7f68ef3388dca790d64ff15314ddf9e0c1dcb6506e` | `.agent/f275_t003_flip_residue_r50.md` (NEW, whole-file) | byte-equal: True; absent at C2, `git show` exit 128 |
| DEC50 | 4976 | `e9c55fb0e3c61de198346eb6fa9206d8190bfb5bb07b576866b47859b246bc67` | `.agent/decisions.md` (append) | reader A + reader B True, control rejected by both |

Every byte count and digest in that table was MEASURED by re-extracting the slice from
the committed authored blob and hashing the extracted bytes — none was copied from a
gate's prose and none was predicted. No FROM/TO pair was authored this round, so no
containment test is owed and no FROM-zero count is reported.

Transport of the block itself: `.agent/authored/f275-r50.md` and `.agent/last_block.md`
are both 41409 bytes at
`9dce5f36949d1e3995281ee5d0de18b19376224fcfd8c2ab4079ee153e025fcf`, identical to
`.remedy-wt/f275-r50.block.md` and to the ordered digest.

## Deviations & assumptions

1. **`.agent/STOP` re-read from disk before the first commit (constraint 8):** ABSENT.
   `ls -la .agent/STOP` → "No such file or directory", exit 2; re-read again at G7(a)
   via `os.path.exists(...)` → False. No stop order is in force.
2. **The commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly** — none
   merged, none reordered, none added, none dropped. C1 precedes C2 as constraint 2
   requires.
3. **The G4 instrument was run against the WORKING TREE at C4, not against a checkout
   of `020b1d57`.** The block orders `python3 -B <that file> .` from the repository
   root, which is what ran. The reading is nevertheless the reading the artefact
   records for `020b1d57`, because G7(b) measures the changed-path set over
   `020b1d57..C4` as seven paths ALL under `.agent/` and ZERO under `packages/`,
   `apps/`, `tests/`, `docs/` or `scripts/` — so not one tracked `.py` file differs
   between the two trees, and the instrument resolves its corpus from
   `git ls-files '*.py'`. Its own file lives under the gitignored `.remedy-wt/` and is
   therefore not in that corpus, which the unchanged `tracked .py: 993` confirms.
4. **No mutation red proof, as constraint 7 states.** The change set is eight `.agent/`
   paths and nothing else; there is no production line, test line or import whose
   colour a mutation could establish.
5. **`.agent/f275_t003_flip_residue.md` was NOT edited**, per the Change section and
   planner_reviewer_prompt.md §3 item 20: it records the run at `978046fe` and stays as
   written. The new file is `.agent/f275_t003_flip_residue_r50.md`, a separate path.
6. **This round RESOLVES and registers nothing.** `Done: R-0876` is booked at C2 and
   the `Landed: R-0876` line round 49 wrote is neither deleted nor rewritten — G7(c)
   measures both present at C2. The open set goes 87 → 86. The next free id is `R-0877`.
7. **Nothing under `docs/roadmap/` was touched**, no feature was closed and no
   follow-up feature was registered, as the block's SESSION 20 paragraph orders.
8. **Scratch.** All probe scripts live under the gitignored `.remedy-wt/`
   (`r50_lib.py`, `r50_g1.py`, `r50_g2.py`, `r50_g3.py`, `r50_g4.py`, `r50_g5.py`,
   `r50_g7.py`, `r50_instrument.py`). Nothing under `.remedy-wt/` is committed;
   `git status --porcelain` is empty.
9. **No SHA is written that was not measured.** C5's own SHA and the push result do not
   exist while this file is being written, so the Range line, the C5 commit table
   heading and the push row all name the fact instead of a numeral. Every other SHA in
   this handback came from `git rev-parse`, `git show` or `git log`.

## Open findings

86 by distinct id (105 registrations − 19 `Done:`), down one from the base's 87:
`R-0876` resolved this round, none registered. Four are High — R-0803, R-0804, R-0806
and R-0807 — all F273's, per DECISION F272 D12.

## Next

The reviewer re-derives round 50's seven gates from the committed range
`020b1d57`..C5 and issues its verdict. Before authoring anything it re-reads
`.agent/STOP` from disk (Phase 1 rule 1) and then runs the Open PR Gate (rule 2); no
pull request is open, and none is owed until the closure sequence.

THE SESSION OWES A SCOPE REPORT. amend0908-f275-finish rule 1's soft limit of 20
SESSIONS is reached with this one. The report — what is finished, what is missing, and
a proposal — belongs in the handback of the LAST round of session 20, together with the
line `SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE`. Rule 2 forbids the
split-and-close default BY NAME: write the report, then keep going.

THE WORK ITSELF is now the three prerequisites DECISION F275 D29 rules, in order, and
the flip is no longer the next production commit:

1. **P1 — replace the transform's receiver-NAME heuristic with the DECISION F272 D7
   raising-property probe** that `docs/roadmap/features/T2_F275.md` T002 already orders,
   and measure the real site set. This is the `AttributeError` class: 551 exception
   lines over 22 receiver-and-attribute pairs, led by 191 `PlannedTask.task_id`,
   99 `TaskEntry.id`, 48 `ProposedTask.title` and 6 `PosixPath.job_title`.
2. **P2 — migrate the surviving `UUID(...)` coercions** over a job or task id, one
   assignment-connected component per commit as DECISION F275 D28 rules for an id
   widen. `UUID(<job/task argument>)` sits at 169 sites in 65 files, 39 of them
   production; `uuid4()` at 637 sites in 144 files, 34 production.
3. **P3 — the `**` splat call-graph pass over the test helper factories**, the 867-line
   constructor-keyword class rule I4 already names.

Then re-run the dry run — the honest test of whether three fixes exhaust the
prerequisites is another measurement — and only then THE FLIP, still as the one
declared-oversize commit AGENTS.md permits per feature, declared with its
inseparability reason before review.

## What this round measured, for the reviewer's convenience

The migration D26, D27 and D28 performed removed 369 exception lines and nothing else.
Against a CONTROL taken at the same commit in a second fresh worktree — the reading R46
did not have — the flip still causes 2557 failures and all 106 errors:
`1 failed, 18366 passed, 29 skipped` unflipped against
`2558 failed, 15703 passed, 29 skipped, 106 errors` flipped, the one shared failure
being the vitest foundation test that needs the gitignored `apps/ui/node_modules`.
`.agent/f275_t003_flip_residue_r50.md` carries the classification and the instrument;
DECISION F275 D29 carries the ruling.
