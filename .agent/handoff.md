# Handback — F272 One world completion, round 8

## Session

SESSION 4 of feature F272 · round 8 · rounds so far 8.
Context self-assessment (amend0905-throughput): context is comfortable — this
round wrote five small targets and one new test file, the only long-running
readings were the three suites, and nothing about the remaining T002 work needs a
fresh session. F272's soft limit is 12 sessions and 40 rounds (amend0906-triage-
throughput), so 4 and 8 are well inside it and no scope report is owed.

## Range

Review of `b5cde726`..HEAD, where HEAD is the C6 commit this file is written in.
The last SHA this file can honestly name is C5, `a6567261`; a handoff cannot name
the commit that writes it, and no SHA is written here that was not measured.

## Commits

### 36affca5 f272: save the round 8 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r8.md` | +400/-0 | C0a — `shutil.copyfile` of the reviewer's own `.remedy-wt/f272-r8-block.md`, a byte copy and never a retype |

### ef748ca2 f272: mirror the round 8 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +301/-268 | C0b — the same byte copy over the mirror; full-file rewrite, so the file's 400 lines and the diff's 301 insertions correctly diverge |

### 801f124d f272: point the plan at the state collapse move one
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17/-20 | C1 — REPLACED by exactly the PLANF272R8 slice bytes (constraint 5) |

### d007c046 f272: book the round 7 gate entry and the R-0819 recurrence
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | C2 — the RECORDR8 slice appended, `post == pre + NL + slice` |

### dda824d1 f272: rule the required job key and the state collapse as D4 and D5
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F272.md` | +80/-0 | C3 — the DECISIONR8 slice appended, adding DECISION F272 D4 and D5 |

### 7bcfbf68 f272: widen RunState with the blocked and stopped members
| Path | +/- | Reason |
|---|---|---|
| `packages/core/models.py` | +4/-0 | C4 (SPEC, not a slice) — `BLOCKED = "blocked"` and `STOPPED = "stopped"` after `CANCELLED`, above them the WHY comment |

### a6567261 f272: pin RunState coverage of the six job status values
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_run_state_covers_job_status.py` | +108/-0 | C5 (SPEC, not a slice) — 21 tests: the six `JOB_*` values covered, the seven survivors, their order, the six round-trips, the non-vacuity control |

### C6 (SHA not nameable here) f272: hand back round 8 with the enum readings and the mutation proof
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | (self-reference) | C6 — this file; a handoff cannot table the commit that writes it (R-0149 pattern) |

Per-commit insertion counts, from `git diff --numstat <parent> <commit>`, every
commit single-parent, every one under the DECISION F104 D1 cap of 500:
C0a 400, C0b 301, C1 17, C2 4, C3 80, C4 4, C5 108. Those are the same numbers
that fill the `+/-` column above, confirmed cell by cell. C6 is excluded because
it cannot count its own insertions.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror | done | |
| C1 the plan | done | |
| C2 the round 7 gate entry and the R-0819 recurrence | done | |
| C3 the two DECISIONs | done | |
| C4 the two RunState members | done | |
| C5 the coverage test | done | |
| C6 the handback | done | |

No commit was made beyond the ordered sequence, so no extra `## Commits` row and
no extra item-status row exist. Nothing was reordered, added or dropped.

## External actions

| Action | Outcome |
|---|---|
| `git worktree add .remedy-wt/f272-r8-g5 a6567261 --detach` | created, detached HEAD at `a6567261` |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f272-r8-g5 --force` | removed BY EXACT PATH, never by glob |
| `git worktree prune` | EXIT 0 |
| removal of this round's own scratch helpers under `.remedy-wt/` | eight files removed BY EXACT PATH; the reviewer's original `.remedy-wt/f272-r8-block.md` deliberately left in place |
| `git push -u origin feature/f272-one-world-completion` | run after C6 |
| PR create / edit / merge | None — this round creates no pull request |

## Verification

**G1 TRANSPORT — EXIT 0.** Per §3 item 37 this covers the SAVED COPY and its
MIRROR, on disk and as committed blobs; it is not a claim about the bytes emitted
into the worker's prompt. Because the reviewer's own scratch original survived on
disk, the chain has three artefacts and not two.

    reviewer original  .remedy-wt/f272-r8-block.md          31197  eb35a343...b7bcf0
    saved copy   C0a   .agent/authored/f272-r8.md           31197  eb35a343...b7bcf0
    mirror       C0b   .agent/last_block.md                 31197  eb35a343...b7bcf0
    saved copy   C0a   36affca5:.agent/authored/f272-r8.md  31197  eb35a343...b7bcf0
    mirror       C0b   ef748ca2:.agent/last_block.md        31197  eb35a343...b7bcf0

All five lengths equal BLOCK_LENGTH 31197: True. All five sha256 equal BLOCK_SHA
`eb35a3437340e705d700ffe0ef406c6feb7ef8253af81ce7173c7d485f7bbcf0`: True. The
delegation's third reading, BLOCK_LINES 400, also matched before any action.

**G2 THE RECORD, at C2 — EXIT 0.**
(a) BYTE. pre 1097162, post 1104989; pre is a byte-exact prefix TRUE; `post == pre
+ b"\n" + slice` TRUE; pre's terminal byte asserted to be exactly one `\n` BEFORE
writing TRUE; post ends in exactly one `\n` TRUE.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`. N was COUNTED BY THE SCRIPT from the slice's own paragraphs, not taken
from the block: N = 2. Units 696 → 698, delta 2; the last 2 units equal the
slice's paragraphs IN ORDER TRUE; the units before an unchanged prefix TRUE.
(c) NEGATIVE CONTROL, in memory on a `bytes` object and never on disk. Offset
1099782 asserted to lie inside the FIRST appended paragraph [1097163, 1102401)
before flipping. Mutated: reader (a) rejects TRUE, reader (b) rejects TRUE.
Restored: reader (a) accepts TRUE, reader (b) accepts TRUE, restored image equals
the disk image TRUE.
(d) COUNTS before → after C2, each matching the block's expectation exactly:

    distinct ^- R-\d{4} —        303 → 303   (expected 303 → 303)
    distinct ^Done: R-\d{4} —    247 → 247   (expected 247 → 247)
    open set BY DISTINCT ID       56 →  56   (expected  56 →  56)
    ^Gate:                        29 →  30   (expected  29 →  30)
    ^Gate: F272 R7                 0 →   1   (expected   0 →   1)
    ^Recurrence: R-0819            0 →   1   (expected   0 →   1)

**G3 THE PLAN at C1, AND THE FEATURE FILE at C3 — EXIT 0.**
The plan: `.agent/plan.md` equals the PLANF272R8 slice bytes exactly TRUE; slice
2279 bytes, file 2279 bytes; 44 lines against the AGENTS.md cap of 50; `## Goal`
present TRUE, `## Next Steps` present TRUE.
The feature file: reader (a) — pre 19325, post 24461, pre a byte-exact prefix
TRUE, `post == pre + NL + slice` TRUE, post ends in exactly one `\n` TRUE.
Reader (b) — N counted by the script from the slice's own paragraphs = 13; units
37 → 50, delta 13; the last 13 units equal the slice's paragraphs IN ORDER TRUE;
the units before an unchanged prefix TRUE. No negative control, per the gate
budget. Over the post-image the count I measure of lines matching
`^### DECISION F272 D\d+ ` is 5, naming in order D1, D2, D3, D4, D5.

**G4 THE ENUM, at C4 — EXIT 0.** Measured by IMPORTING the shipped modules, never
from source text. `packages.core.models.__file__ =
/home/decodeux/Repos/remedy/packages/core/models.py` and
`packages.orchestration.pingpong_job.__file__ =
/home/decodeux/Repos/remedy/packages/orchestration/pingpong_job.py`.

(i) The full ordered member list of `RunState`:

    0 PENDING   = 'pending'      5 FAILED    = 'failed'
    1 PLANNED   = 'planned'      6 CANCELLED = 'cancelled'
    2 RUNNING   = 'running'      7 BLOCKED   = 'blocked'
    3 PAUSED    = 'paused'       8 STOPPED   = 'stopped'
    4 COMPLETED = 'completed'

(ii) The six `JOB_*` constants, MY reading beside the base reading at `b5cde726`
that the block states:

    JOB_PLANNED   = 'planned'    is a RunState value: True   [base b5cde726: True]
    JOB_RUNNING   = 'running'    is a RunState value: True   [base b5cde726: True]
    JOB_BLOCKED   = 'blocked'    is a RunState value: True   [base b5cde726: FALSE]
    JOB_COMPLETED = 'completed'  is a RunState value: True   [base b5cde726: True]
    JOB_PAUSED    = 'paused'     is a RunState value: True   [base b5cde726: True]
    JOB_STOPPED   = 'stopped'    is a RunState value: True   [base b5cde726: FALSE]

Every one TRUE after C4, and the two the base read FALSE are exactly the two C4
adds. The gate discriminates: it was measurably red at its own base.

(iii) NON-VACUITY CONTROL: `"no_such_state"` is a `RunState` value → False, as
required. The TRUEs above are therefore not a reading that answers TRUE for
everything.

(iv) THE SEVEN SURVIVE, one per line:

    pending    still a RunState value: True
    planned    still a RunState value: True
    running    still a RunState value: True
    paused     still a RunState value: True
    completed  still a RunState value: True
    failed     still a RunState value: True
    cancelled  still a RunState value: True

The member list's first seven entries are still
`['pending', 'planned', 'running', 'paused', 'completed', 'failed', 'cancelled']`
in that order: True.

**G5 THE PIN CAN FAIL — MUTATION RED-PROOF — EXIT 0 overall.** In a disposable
worktree `.remedy-wt/f272-r8-g5` at `a6567261`, the commit C5 creates.
`__pycache__` purged first (0 directories found in a fresh worktree), and
`packages.core.models` confirmed to resolve from INSIDE the worktree:
`/home/decodeux/Repos/remedy/.remedy-wt/f272-r8-g5/packages/core/models.py`.
Command throughout:
`python3 -B -m pytest tests/orchestration/test_run_state_covers_job_status.py -q -p no:randomly`.

    UNMUTATED CONTROL, before any mutation   EXIT 0   21 passed in 0.23s
    delete BLOCKED member line               EXIT 1   2 failed, 19 passed in 0.26s   names 'blocked': True
    control after restore                    EXIT 0   21 passed in 0.28s
    delete STOPPED member line               EXIT 1   2 failed, 19 passed in 0.26s   names 'stopped': True
    control after restore                    EXIT 0   21 passed in 0.28s
    ADD member NO_SUCH_STATE = "no_such_state"  EXIT 1   1 failed, 20 passed in 0.24s   names 'no_such_state': True
    control after removal                    EXIT 0   21 passed in 0.23s

Each deleted byte string was counted in that file first and occurred exactly once
(`    BLOCKED = "blocked"\n` → 1, `    STOPPED = "stopped"\n` → 1), so no longer
unique string was needed. The addition anchor `    STOPPED = "stopped"\n` also
occurred exactly once. The target file was byte-identical to its committed state
at the end: True. A member's deletion and an unexpected member's addition are
BOTH visible, so the test pins both directions and item 4 of the C5 spec is not
decoration.

**G6 THE SUITES, at C5, run SERIALLY, each its own invocation — every one EXIT 0.**

    python3 -B -m pytest tests/orchestration/test_run_state_covers_job_status.py -q -p no:randomly
      EXIT 0   21 passed in 0.28s
    python3 -B -m pytest tests/orchestration/ -q -p no:randomly
      EXIT 0   12838 passed, 10 skipped, 1 warning in 763.70s (0:12:43)
    python3 -B -m pytest tests/docs/ -q -p no:randomly
      EXIT 0   303 passed in 0.49s
    python3 -B -m pytest tests/cli/ -q -p no:randomly
      EXIT 0   1537 passed in 305.47s (0:05:05)
    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
      EXIT 0   42 passed in 21.08s

Against the `b5cde726` readings the block states: `tests/orchestration/` 12817 →
12838, a rise of exactly 21, which is the 21 tests C5 adds and nothing else, with
skips unchanged at 10; `tests/docs/` 303 → 303; `tests/cli/` 1537 → 1537; the
canary 42 → 42. No count falls anywhere.

**G7 LINT AND INTEGRITY, at C5 — EXIT 0 both.**

    python3 -m ruff check packages/core/models.py tests/orchestration/test_run_state_covers_job_status.py
      EXIT 0   All checks passed!
    python3 -m apps.cli.grouped integrity check --json
      EXIT 0   "passed": true, "fail_count": 0, "check_count": 5

A repo-wide `ruff check .` was NOT run: the block does not order it and it is
EXIT 1 on base under OPEN finding R-0468.

**G8 THE TREE — EXIT 0.** `git status --porcelain` EMPTY when C6 was staged.
`git ls-files .remedy-wt` EMPTY. `git worktree list` after removal names the
primary checkout and exactly the twelve pre-existing `remedy/job-*` entries, all
older than this round; the one worktree this round created,
`.remedy-wt/f272-r8-g5`, is gone. Per-commit insertion counts and single-parent
readings are in the `## Commits` section above and were confirmed cell by cell
against the same `git diff --numstat` output; `.agent/last_block.md` is the
full-file rewrite where the file's 400 lines and the diff's 301 insertions
correctly diverge. Marker sweep — lines beginning `<<<BEGIN ` or `<<<END ` in
every written non-block file, measured by me:

    .agent/plan.md                                            0
    .agent/live_review.md                                     0
    docs/roadmap/features/T2_F272.md                          0
    packages/core/models.py                                   0
    tests/orchestration/test_run_state_covers_job_status.py   0

The three `.agent/STOP` readings of constraint 9, each by `os.path.exists`:

| When | Reading |
|---|---|
| before C0a | False |
| before C4 | False |
| before C6 | False |

## Authored-text proofs

Disk-to-disk, each slice re-extracted from the COMMITTED
`.agent/authored/f272-r8.md` and compared against the applied region:

| Slice | Applied region | Result | sha256 of both sides |
|---|---|---|---|
| PLANF272R8 | `.agent/plan.md`, whole file, 2279 bytes | IDENTICAL | `f15607599a5f19b5…` |
| RECORDR8 | `.agent/live_review.md`, terminal 7826 bytes | IDENTICAL | `379cb0cf1892a5e1…` |
| DECISIONR8 | `docs/roadmap/features/T2_F272.md`, terminal 5135 bytes | IDENTICAL | `813a94c832f2980d…` |

Full digests:
PLANF272R8 `f15607599a5f19b57174c23fadd182251c0dace70d02a2bc3a85ccc05739727a`;
RECORDR8 `379cb0cf1892a5e13386f44edae5b43d9e91cd29240c91dc73e0a6cd0ae9fa04`;
DECISIONR8 `813a94c832f2980d1793ba5d75ecbd38275b56d5b31987ff5bbfb2108794f795`.
C4 and C5 were a SPEC and not slices, so they have no authored-text row.

## Deviations & assumptions

1. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   C3, C4, C5, C6 were committed in exactly that order, nothing added, nothing
   dropped, nothing reordered. No commit was made beyond the ordered sequence, so
   no extra `## Commits` row and no extra item-status row exist — stated here in
   those same words, as the fix clause OPEN in the record and binding on the next
   block that orders a handback requires.
2. **No slice was edited.** Nothing in PLANF272R8, RECORDR8 or DECISIONR8 looked
   wrong; all three were applied byte for byte and the marker lines reached no
   target file.
3. **The C4 WHY comment is one sentence on two physical lines.** The block orders
   "a one-sentence WHY comment"; the sentence is one sentence but does not fit
   this file's line width, so it is wrapped across two `#` lines. No third
   sentence was added.
4. **C5 ships 21 tests, not the four the spec numbers.** The spec says "pins at
   minimum" four properties. Items 1, 2 and 3 are parametrized — one test case
   per constant and per surviving member, so a failure names the constant it lost
   rather than an index, which is what the spec's "one assertion per constant"
   asks for. That gives 6 + 7 + 6 = 19 cases, plus the non-vacuity control (item
   4) and one extra test that the seven pre-existing members are still the enum's
   FIRST SEVEN IN ORDER — that ordering is explicitly measured by gate G4(iv) but
   not otherwise pinned by any test, so leaving it to the gate alone would have
   made a gate reading nothing enforced. 19 + 1 + 1 = 21.
5. **The commit gate's plan check across C0a and C0b.** AGENTS.md requires
   `.agent/plan.md` to reflect the current work before every commit, and the
   block's own ordering makes C1 the plan commit, third. C0a and C0b were
   therefore committed while the plan still described round 7. This is the
   block's stated ordering (constraint 3, "C1 is the first substantive commit"),
   not a worker deviation, and it is declared rather than passed over.
6. **The reviewer's original block file was left on disk.** `.remedy-wt/` is
   gitignored and `git ls-files .remedy-wt` is EMPTY, so the file is invisible to
   the tree gate; it is left in place deliberately because it is the reviewer's
   scratch and the first link of this round's transport chain. This round's own
   scratch helpers under the same directory were removed by exact path.
7. **No finding id was minted and no `Done:` paragraph was written** by me, per
   constraint 7. The RECORDR8 slice was applied verbatim and is the only text
   entering the record this round.
8. **Nothing was worked around.** No gate went red, so no gate needed a reading
   declined; every exit code above is a real one and none of them is the word
   "green".

## Next

The reviewer re-runs G1 to G8 over `b5cde726`..HEAD and issues a verdict on
round 8. On PASS the next round is DECISION F272 D5's move two: replace
`JobPlan.status: str` with `state: RunState` across every call site in ONE
commit, exporting `job.state.value` into the unchanged `"status"` JSON key so
records already on disk load unchanged. Before authoring it, Phase 1 rule 1 —
read `.agent/STOP` from disk — comes first.
