# Handoff — F272 One world completion, round 16

## Session

SESSION 8 of feature F272 · round 16 · rounds so far 16

Context self-assessment: this is session 8's second delegated round; the worker's
context is comfortable, the round was small and nothing about it argues for a
fresh session. F272's soft limit is 12 sessions and 40 rounds
(amend0906-triage-throughput), so the limit is not reached and no scope report is
owed.

## Range

Review of `c80f32ce`..`HEAD` (branch `feature/f272-one-world-completion`).

## Commits

### 042ae9f2 f272: save the round 16 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r16.md` | +306/-0 | C0a — `shutil.copyfile` of `.remedy-wt/f272-r16-block.md`, a byte copy, never a retype |

### c5bfd259 f272: mirror the round 16 block into the last-block slot
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +218/-391 | C0b — `shutil.copyfile` of the same source; the counts are the churn against round 15's block |

### 0b8a9ef3 f272: point the plan at T003 and the surviving rename site
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +19/-19 | C1 — REPLACED by the PLANF272R16 slice, byte for byte |

### 8cdb287c f272: book the round 15 verdict and register R-0822
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | C2 — RECORDR16 appended as `pre + NL + slice`; the round 15 PASS record and the R-0822 registration, BEFORE the fix, per §4 item 4 |

### 880d824a f272: record the round 15 reviewer prose slips
| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +4/-0 | C3 — SLIPSR16 appended; two dated lines, no id spent |

### ee17bb25 f272: read the run state, not a field the rename removed, in the stop error JSON
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job_stop_cmd.py` | +1/-1 | C4 — the single FROM/TO pair at line 167; `job.status` becomes `job.state` and nothing else on the line moves |

### 1240a6c5 f272: pair the completed-job stop error with its JSON guard
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_job_stop.py` | +19/-0 | C5 — GUARDR16 INSERTED inside `TestItRefusesToLie`, immediately before the unwritable-control-area test; no existing test edited, deleted or weakened |

### 6c4a9c9f f272: record R-0822 as landed on the branch
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | C6 — LANDEDR16 appended as `pre + NL + slice`, proved against its OWN pre-image, which C2 left. A `Landed:` line only; no `Done:` was written |

### (this commit) f272: hand back round 16 on the surviving rename site
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C7 — this file. A handoff cannot table the commit that writes it (R-0149 pattern), and its sha is unmeasurable at authoring time |

## Item status

Every ordered item of the bundle, exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f272-r16.md` written by `shutil.copyfile`; sha256, byte length and line count all equal the source's (G1) |
| C0b | done | `.agent/last_block.md` written by `shutil.copyfile` from the same source; same three readings (G1) |
| C1 | done | `.agent/plan.md` REPLACED by PLANF272R16; byte-equality proved in G3 |
| C2 | done | RECORDR16 appended to `.agent/live_review.md`; G2 readers (a), (b), (c) and (d) all pass, and all seven of (d)'s figures match the block |
| C3 | done | SLIPSR16 appended to `.agent/prose_slips.md`; two dated lines, no id |
| C4 | done | The one FROM/TO pair applied over `job_stop_cmd.py` only; FROM 1→0, TO 0→1, `"job_status"` 4→4; proved against the RUNNING handler in G4(iii) and red-proved in G5 |
| C5 | done | GUARDR16 INSERTED before the stated anchor, inside `TestItRefusesToLie`; +19/-0, one test added by AST count, none edited |
| C6 | done | LANDEDR16 appended to `.agent/live_review.md` against its own freshly-read pre-image; `Landed: R-0822` 0→1, `Done: R-0822` still 0 |
| C7 | done | This handoff, rewritten per `docs/agents/handback_template.md` |

No item was skipped and none deviated. Nothing was added, dropped or reordered.

## Open findings

**58**, BY DISTINCT ID: 306 distinct `^- R-\d{4}` registrations minus 248 distinct
`^Done: R-\d{4}` resolutions. The round opened at 57 and closes at 58 because
exactly ONE id was minted, **R-0822**, as constraint 5 orders. R-0822 is LANDED,
not resolved — only the reviewer writes `Done:`, and `^Done: R-0822 ` measures 0.
The next free id is **R-0823**.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/f272-r16-redproof 1240a6c5` | created, detached at `1240a6c5` (C5's commit) — G5 only, never the primary checkout |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f272-r16-redproof` | removed BY EXACT PATH, exit 0; the directory no longer exists; `git worktree list` then shows the primary plus the twelve pre-existing `remedy/job-*` entries and nothing else |
| `git push -u origin feature/f272-one-world-completion` | pushed |

No PR was created. Nothing was merged. No force-push. Five scratch artifacts were
written under the gitignored `.remedy-wt/` — `r16_slices.py`, `r16_append.py`,
`r16_redproof.py`, `r16_suites.py` and the `__pycache__/r16_slices.cpython-310.pyc`
that importing the first of them produced — and all five plus the now-empty
`__pycache__` directory were removed BY EXACT PATH, never by glob.
`git ls-files .remedy-wt` is empty.

## Verification

All eight gates were run and their REAL exit codes are below. One line per gate.
G5 ran only in its disposable worktree; every other gate ran in the primary
checkout, and all eight ran BEFORE C7.

**G1 TRANSPORT — PASS.** One digest comparison; all three artefacts share one
sha256, one byte length and one line count:

    .remedy-wt/f272-r16-block.md   3ac45e7eeef9ed166ebd01b912423e45fdddc600e114bf4ed4dc02b8223c9c8b  24740 bytes  306 lines
    .agent/authored/f272-r16.md    3ac45e7eeef9ed166ebd01b912423e45fdddc600e114bf4ed4dc02b8223c9c8b  24740 bytes  306 lines
    .agent/last_block.md           3ac45e7eeef9ed166ebd01b912423e45fdddc600e114bf4ed4dc02b8223c9c8b  24740 bytes  306 lines

    ONE sha256 across all three: True   ONE byte length: True   ONE line count: True

The block file was hashed on arrival, BEFORE any work began, and matched the
three figures the delegation stated. No transport fault.

**G2 THE RECORD — PASS on all four readers, for BOTH appends, each proved against
its OWN pre-image.**

*C2 — RECORDR16 (8158 bytes, sha256 `1b8d3bb3…bebc0ff38`)*

* (a) BYTE — PRE 1149219 bytes, sha256 `41597506…8b07e9c1`, terminal twelve bytes
  `b'rong lines.\n'`, trailing-newline run exactly 1. POST 1157378 bytes, sha256
  `986528d7…b87fbc00`. Pre is a byte-exact PREFIX of post: TRUE.
  `post == pre + b"\n" + slice`: TRUE.
* (b) STRUCTURAL — the file's single terminal newline WAS STRIPPED before
  splitting on blank lines, and this states so explicitly. N was COUNTED BY THE
  WORKER'S SCRIPT from the slice's own blank-line paragraphs: **N = 2** (the
  `Gate: F272 R15 …` verdict paragraph and the `- R-0822 …` registration). Units
  712 → 714. The last 2 units equal the slice's 2 paragraphs IN ORDER: TRUE.
  Everything before them unchanged: TRUE.
* (c) NEGATIVE CONTROL — byte 40 of the FIRST appended paragraph flipped in
  memory and never on disk (`b'r'` → `b's'`). Reader (a): prefix still True but
  exact False → (a) REJECTS: TRUE. Reader (b): tail False, head True → (b)
  REJECTS: TRUE. Both ACCEPT once restored: TRUE. The on-disk sha256 is identical
  before and after the control: TRUE.

*C6 — LANDEDR16 (405 bytes, sha256 `6f809da6…bc6f81cfc`)*

* (a) BYTE — its pre-image was READ, not assumed: PRE 1157378 bytes, sha256
  `986528d7…b87fbc00`, terminal twelve bytes `b'ands today.\n'`, trailing-newline
  run exactly 1 — that is what C2 left. POST 1157784 bytes, sha256
  `e25c3ba5…43da008b`. Pre is a byte-exact PREFIX of post: TRUE.
  `post == pre + b"\n" + slice`: TRUE.
* (b) STRUCTURAL — terminal newline STRIPPED before splitting, again stated. N
  COUNTED FROM THE SLICE: **N = 1**. Units 714 → 715. The last 1 unit equals the
  slice's 1 paragraph: TRUE. Everything before unchanged: TRUE.
* (c) The block orders the negative control on the C2 append only; it was run
  there and is reported above.

* (d) COUNTS over the WHOLE ROUND, before C2 → after C6. Every one measured;
  ALL SEVEN MATCH the block:

      ^- R-\d{4} distinct        305 -> 306    block says 305 -> 306   MATCH
      ^Done: R-\d{4} distinct    248 -> 248    block says 248 -> 248   MATCH
      open set BY DISTINCT ID     57 ->  58    block says  57 ->  58   MATCH
      ^Gate:                      38 ->  39    block says  38 ->  39   MATCH
      ^Gate: F272 R15              0 ->   1    block says   0 ->   1   MATCH
      ^- R-0822                    0 ->   1    block says   0 ->   1   MATCH
      ^Landed: R-0822              0 ->   1    block says   0 ->   1   MATCH

  The two figures round 15 got wrong were the `^Gate: ` pair, and the cause was a
  two-paragraph record slice. RECORDR16 is also two paragraphs, but only ONE of
  them begins at the line anchor with `Gate: `; the second begins `- R-0822 `.
  The block's 38 → 39 is therefore right, and the measurement confirms it. No
  figure needed adjusting and none was adjusted.

**G3 THE PLAN — PASS.** `.agent/plan.md` byte-equals the PLANF272R16 slice: TRUE
(both sha256 `4df5af1d…1c6ae513`). **1907 bytes**, **39 lines**, under the
AGENTS.md cap of 50: TRUE. `## Goal` present: TRUE. `## Next Steps` present: TRUE.

**G4 THE FIX IS REAL — PASS, all three readings.**

    (i)   the C4 REWRITE counts, over apps/cli/commands/job_stop_cmd.py:
            FROM string                    1 -> 0
            TO string                      0 -> 1
            'job.status'                   1 -> 0
            'job.state}, indent=2))'       0 -> 1
          The containment test was RUN, not asserted: TO contains FROM -> False,
          so this is a REWRITE and the post-edit FROM count of 0 is attainable,
          exactly as the block states.
          One line differs between before and after; ast.parse OK; 200 lines both
          sides; 7512 -> 7511 bytes.

    (ii)  the external JSON key "job_status": 4 occurrences BEFORE, 4 occurrences
          AFTER. The key did not move.

    (iii) against the RUNNING handler, not the text. Provenance printed first:
          apps.cli.commands.job_stop_cmd.__file__ =
            /home/decodeux/Repos/remedy/apps/cli/commands/job_stop_cmd.py
          _load_job pointed at JobPlan(job_id="a1b2c3d4e5f60718",
          state=RunState.COMPLETED); hasattr(plan, "status") is False.
          _cmd_job_stop(job_id, json_output=True):
            raised SystemExit with code 1        -> True
            any other exception                  -> None (NO AttributeError)
            stdout:
              {
                "ok": false,
                "error": "job_not_stoppable",
                "job_id": "a1b2c3d4e5f60718",
                "job_status": "completed"
              }
            payload["error"] == "job_not_stoppable"  -> True
            payload["job_status"] == "completed"     -> True
            payload["ok"] is False                   -> True

**G5 RED-PROOF — PASS, and it reproduces the reviewer's measurement exactly.** Run
ONLY in the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/f272-r16-redproof`, added detached at
`1240a6c5` (C5's commit), never in the primary checkout. `__pycache__` directories
found under the worktree: 0 before each run (a fresh `git worktree add` carries
none, and the purge was re-run after every edit); `python3 -B` and
`PYTHONDONTWRITEBYTECODE=1` throughout, so none was written. Provenance probed
FIRST, before any edit:

    apps.cli.commands.job_stop_cmd.__file__ =
      /home/decodeux/Repos/remedy/.remedy-wt/f272-r16-redproof/apps/cli/commands/job_stop_cmd.py
    resolves INSIDE the worktree: True   (no editable install shadows it)

ORDERED COLOUR: C4 reverted → red, C4 restored → green.

    TO string count in that exact file BEFORE reverting: 1   (unique, as ordered)
    C4 REVERTED ALONE by replacing that one TO with its FROM, in
      .remedy-wt/f272-r16-redproof/apps/cli/commands/job_stop_cmd.py
      after revert: job.status = 1, 'job.state}, indent=2))' = 0
      C5's guard left in place, untouched.

    CMD: python3 -B -m pytest tests/cli/test_job_stop.py -q -p no:randomly
    EXIT: 1
    1 failed, 26 passed in 0.54s     (reviewer measured EXIT 1, 1 failed, 26 passed — MATCH)
    FAILED BY NAME (1):
      FAILED tests/cli/test_job_stop.py::TestItRefusesToLie::test_a_completed_job_says_so_in_json_too
    (exactly the one test the reviewer named — MATCH)
    The failure carries the real defect, not a substitute assertion:
      >   print(_json.dumps({"ok": False, "error": "job_not_stoppable",
      >                      "job_id": job_id, "job_status": job.status}, indent=2))
      E   AttributeError: 'JobPlan' object has no attribute 'status'. Did you mean: 'state'?
      apps/cli/commands/job_stop_cmd.py:167: AttributeError

    C4 RESTORED: job.status = 0, 'job.state}, indent=2))' = 1
    CMD: python3 -B -m pytest tests/cli/test_job_stop.py -q -p no:randomly
    EXIT: 0
    27 passed in 0.51s               (reviewer measured EXIT 0 at 27 passed — MATCH)

    ORDERED COLOUR: reverted EXIT 1 -> restored EXIT 0.

Worktree removed BY EXACT PATH, never by glob. `git worktree list` afterwards
shows 13 entries: the primary plus the twelve pre-existing `remedy/job-*`
worktrees and nothing else.

**G6 THE SUITES — PASS, EXIT 0 on all six.** Run SERIALLY, each its own
invocation, each `-q -p no:randomly`, all in the primary checkout. The four state
readers were run AS FOUR:

    python3 -B -m pytest tests/cli/ -q -p no:randomly                                 EXIT 0  1538 passed in 307.19s
    python3 -B -m pytest tests/ui_server/ -q -p no:randomly                           EXIT 0   515 passed in 36.81s
    python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly    EXIT 0    52 passed in 6.71s
    python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly   EXIT 0    21 passed in 11.60s
    python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly EXIT 0    16 passed in 0.34s
    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly              EXIT 0    42 passed in 22.61s

RECONCILIATION of `tests/cli/`. The tests C5 adds were COUNTED with `ast` over
`tests/cli/test_job_stop.py` at `ee17bb25` (before C5) and at HEAD (after C5), not
taken from the block: 23 test functions before, 24 after, so C5 adds **1**.
Arithmetic: **1537 + 1 = 1538**, and 1538 is what ran. Difference: **0**. The
reviewer's own AST count was also 1 and its predicted total 1538 — both MATCH.

**G7 LINT AND INTEGRITY — PASS, both EXIT 0.**

    python3 -m ruff check apps/cli/commands/job_stop_cmd.py tests/cli/test_job_stop.py
    EXIT: 0    stdout: All checks passed!    stderr: (empty)

    python3 -m apps.cli.grouped integrity check --json
    EXIT: 0    "passed": true    "fail_count": 0    "check_count": 5

The block's warning was checked directly rather than inferred: the newly
registered OPEN Medium R-0822 did NOT turn the blocker check red —
`{"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}`.
No finding was edited.

**G8 THE TREE — PASS.** `git status --porcelain` was run at EVERY commit boundary
and its real output was empty every time, and it is empty now (`''`).
`git ls-files .remedy-wt` is empty (`''`). `git worktree list` shows 13 entries:
the primary plus the twelve pre-existing `remedy/job-*` entries and nothing else.

Per-commit insertions from `git diff --numstat <parent> <commit>`, C7 excluded
because it cannot count its own insertions. Every commit is single-parent, touches
exactly one path, is under the DECISION F104 D1 cap of 500, and matches the
`## Commits` table above cell for cell:

    C0a  042ae9f2  +306  -0     .agent/authored/f272-r16.md
    C0b  c5bfd259  +218  -391   .agent/last_block.md
    C1   0b8a9ef3   +19  -19    .agent/plan.md
    C2   8cdb287c    +4  -0     .agent/live_review.md
    C3   880d824a    +4  -0     .agent/prose_slips.md
    C4   ee17bb25    +1  -1     apps/cli/commands/job_stop_cmd.py
    C5   1240a6c5   +19  -0     tests/cli/test_job_stop.py
    C6   6c4a9c9f    +2  -0     .agent/live_review.md

**`.agent/STOP` readings, the three constraint 6 orders, all by `os.path.exists`:**

    before C0a: os.path.exists('.agent/STOP') -> False
    before C4:  os.path.exists('.agent/STOP') -> False
    before C7:  os.path.exists('.agent/STOP') -> False

## Authored-text proofs

**Five** marker-delimited slices were found in `.agent/authored/f272-r16.md` and
all five were EXTRACTED PROGRAMMATICALLY between their `<<<BEGIN NAME>>>` and
`<<<END NAME>>>` lines and applied byte for byte. None was retyped, reflowed or
corrected, and none looked wrong. The block deliberately states no count of its
own parts; the count the worker measured is **5**.

| Slice | Bytes | sha256 (head) | Target | Applied as | Disk-to-disk result |
|---|---|---|---|---|---|
| PLANF272R16 | 1907 | `4df5af1d` | `.agent/plan.md` | whole-file REPLACE | byte-equals the slice: TRUE |
| RECORDR16 | 8158 | `1b8d3bb3` | `.agent/live_review.md` | `pre + b"\n" + slice` | `post == pre + NL + slice`: TRUE; last 2 units equal its 2 paragraphs: TRUE |
| SLIPSR16 | 1108 | `7b263a0c` | `.agent/prose_slips.md` | `pre + b"\n" + slice` | `post == pre + NL + slice`: TRUE; last 2 units equal its 2 paragraphs: TRUE |
| GUARDR16 | 738 | `1e9e7787` | `tests/cli/test_job_stop.py` | INSERT before the anchor | see below |
| LANDEDR16 | 405 | `6f809da6` | `.agent/live_review.md` | `pre + b"\n" + slice` | `post == pre + NL + slice`: TRUE; last 1 unit equals its 1 paragraph: TRUE |

Constraint 4 discharged, measured rather than eyeballed. The anchor line
`    def test_an_unwritable_control_area_is_loud_and_requests_nothing(self, job, capsys):`
occurred **exactly 1x** before the edit and exactly 1x after. GUARDR16 ends with
its own blank line (`slice.endswith(b"\n\n")`: TRUE) and carries no trailing
whitespace on any line, so the anchor follows it directly and no separator was
inserted. The insertion is PURE in both directions:

    post == pre with the slice inserted before the anchor and nothing else : TRUE
    removing the slice again recovers the pre-image byte for byte           : TRUE
    bytes 11382 -> 12120 (delta 738, exactly the slice)                     : TRUE
    lines 283 -> 302 (delta 19, exactly the slice)                          : TRUE

Placement verified by AST, not by line number: `TestItRefusesToLie`'s methods in
order are `test_an_unknown_job_exits_3`,
`test_an_unknown_job_exits_3_in_json_mode_too`,
`test_status_for_an_unknown_job_exits_3`,
`test_a_malformed_job_id_is_a_usage_error`,
`test_a_completed_job_is_not_told_that_work_will_stop`,
**`test_a_completed_job_says_so_in_json_too`**,
`test_an_unwritable_control_area_is_loud_and_requests_nothing`,
`test_an_unwritable_control_area_says_so_in_json_too` — so the new test is INSIDE
that class and immediately precedes the anchor, as ordered. Constraint 3 holds:
the commit is +19/-0, so no existing test could have been edited, deleted or
weakened.

Constraint 2 discharged on the LINE-ANCHORED reading that round 14's accepted
deviation 2 established: `^<<<(BEGIN|END) …>>>$` occurs **0** times in
`.agent/live_review.md`, and the appended regions of C2 and C6 contain **0** `<<<`
substrings each. The 15 `<<<` substrings that file contains are all PRE-EXISTING
and MID-LINE — prose quoting the marker token inside older records — and their
count is 15 before and 15 after. `.agent/prose_slips.md` and
`tests/cli/test_job_stop.py` contain 0 `<<<` after their edits. No marker reached
any file but the two C0 copies.

C4's pair, extracted programmatically from the block's own fenced blocks rather
than retyped:

    FROM repr: '                               "job_id": job_id, "job_status": job.status}, indent=2))'
    TO   repr: '                               "job_id": job_id, "job_status": job.state}, indent=2))'
    leading spaces: FROM 31, TO 31 — identical, and identical to the target line's own
    TO contains FROM: False  (RUN, not asserted — the block's stated output MATCHES)
    FROM occurrences at c80f32ce: 1, exactly as the block states

## Deviations & assumptions

The block's ordered commit sequence was followed exactly: C0a, C0b, C1, C2, C3,
C4, C5, C6, C7 — nine commits, none added, none dropped, none reordered. No path
outside the eight-path change set was edited. No existing test was edited, deleted
or weakened. Exactly one id was minted, R-0822, as constraint 5 orders. Every gate
went green on its first run; nothing was weakened, no expected number was adjusted
to match a measurement, and no test was touched to make anything pass.

**No deviation from the block was necessary, and no contradiction between the
block and AGENTS.md was found.** All seven of G2(d)'s figures matched, so the
"report the difference rather than adjusting anything" clause never had to fire.
Three items are recorded below as assumptions, not deviations, because the block
left them unstated.

**Assumption 1 — C3's separator.** The block orders SLIPSR16 "APPENDED" to
`.agent/prose_slips.md` without stating a separator and orders no byte gate over
it. `pre + b"\n" + slice` was chosen from that file's own on-disk convention: it
ended in exactly one newline (144204 bytes, trailing-newline run 1) and its
existing entries are blank-line separated. The result was proved with the same two
readers G2 orders for the record — `post == pre + NL + slice`: TRUE; N counted
from the slice = 2; the last 2 units equal its 2 paragraphs in order and
everything before is unchanged: TRUE. The seam reproduces the spacing already used
between that file's entries.

**Assumption 2 — the commit gate's plan.md clause at C0a and C0b.** AGENTS.md's
Commit Gate asks that `.agent/plan.md` match the current work before EVERY commit,
while the block orders the plan rewrite at C1, after the two block-save commits.
The conservative reading was taken: the block's ordering is the branch's standing
sequence, C1 follows immediately, and no work outside `.agent/` had landed at
either boundary, so the stale plan described no code that existed. Recorded here
because a reader auditing the round against AGENTS.md would otherwise have to
re-derive it.

**Assumption 3 — where `RunState` lives.** R-0822's registration text says round
14 retyped `JobPlan.state` onto `RunState` without naming the module. Measured:
`JobPlan.__dataclass_fields__['state'].type` is `RunState` and its default
`RunState.PLANNED` comes from `packages.core.models`, not from any
`packages.orchestration.run_state` — that module does not exist. G4(iii) imports
it from `packages.core.models` accordingly. This contradicts nothing the block
says; it is stated so the reviewer's re-run of G4(iii) uses the same import.

**Note, not a deviation — `RunState` serializes correctly through `_json.dumps`.**
`job.state` is now an enum member, not a `str`, so the fixed line's behaviour
under `json.dumps` is worth naming rather than assuming: `RunState` is a
str-subclassing enum (`RunState.COMPLETED == "completed"` is True) and the emitted
payload carries `"job_status": "completed"`, a plain JSON string. G4(iii) shows
the real bytes. The external contract is unchanged in value as well as in key.

## Reviewer verdict — round 16

VERDICT PASS. Every gate was RE-RUN by the reviewer rather than read, in the primary
checkout at `d6e5f5e7`.

- Range `c80f32ce`..`d6e5f5e7`, nine commits, every one single-parent, in exactly the
  ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7, with the change set exactly
  the eight ordered paths and nothing else. `git status --porcelain` empty.
- G1 TRANSPORT is a REAL chain, not merely self-consistent: the reviewer's own scratch
  original `.remedy-wt/f272-r16-block.md`, written and hashed BEFORE delegation, and the
  committed `.agent/authored/f272-r16.md` and `.agent/last_block.md` are all 24740 bytes
  at 306 lines and all hash to
  `3ac45e7eeef9ed166ebd01b912423e45fdddc600e114bf4ed4dc02b8223c9c8b`. Per §3 item 37
  this covers the saved copy and its mirror, not the bytes emitted into a prompt.
- G2 THE RECORD: `.agent/live_review.md` 1149219 to 1157784 across TWO appends, the
  pre-image a byte-exact prefix of the final image. ALL SEVEN ORDERED COUNTS REPRODUCE
  EXACTLY — registrations 305 to 306, resolutions 248 unchanged, open set BY DISTINCT ID
  57 to 58, `^Gate: ` 38 to 39, `^Gate: F272 R15 ` 0 to 1, `^- R-0822 ` 0 to 1 and
  `^Landed: R-0822 ` 0 to 1 — and `^Done: R-0822 ` is 0, so the worker wrote the
  `Landed:` line and left `Done:` to the reviewer, exactly as §4 item 4 requires.
- G3 THE PLAN is 1907 bytes byte-equal to its slice at 39 lines against the cap of 50.
- G4 THE FIX reproduces against the SHIPPED handler, run rather than read: with
  `_load_job` returning a completed `JobPlan`, `_cmd_job_stop(job_id, json_output=True)`
  now raises SystemExit with code 1 and prints `"error": "job_not_stoppable"` with
  `"job_status": 'completed'` as a plain `str` — no AttributeError. `job.status` in that
  file is 0 and the external JSON key `"job_status"` is still 4, so the contract did not
  move while the Python field did.
- G5 THE RED-PROOF was re-run by the reviewer in its own disposable worktree at
  `1240a6c5`, provenance confirmed inside the worktree and the worktree removed
  afterwards by exact path: with C4 alone reverted the run is EXIT 1 with EXACTLY
  `TestItRefusesToLie::test_a_completed_job_says_so_in_json_too` failing and 26 passing,
  carrying the real `AttributeError: 'JobPlan' object has no attribute 'status'`; with
  C4 restored it is EXIT 0 at 27 passed. The mutation here is the SHIPPED DEFECT itself
  rather than an invented one, which is the strongest form this gate takes.
- G6 THE SUITES, re-run serially: `tests/cli/` EXIT 0 at 1538 passed, which is the base
  of 1537 plus exactly the one test C5 adds; `tests/ui_server/` EXIT 0 at 515;
  `test_test_runner.py` EXIT 0 at 52; `test_resource_safety.py` EXIT 0 at 21;
  `test_integrity_gate.py` EXIT 0 at 16 — the last four all identical to round 15's
  readings, so nothing regressed.
- G7 ruff EXIT 0 `All checks passed!` over both changed files; integrity EXIT 0 with
  `"passed": true`, `"fail_count": 0`, and `high_blockers_open` PASS despite the newly
  registered open Medium, which is the behaviour the block predicted.
- G8 THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, thirteen
  worktree entries being the primary plus the twelve pre-existing `remedy/job-*`, and
  the guard slice landed byte-identical to the block's own bytes.

THE WORKER DECLARED NO DEVIATIONS AND NONE IS OWED — the reviewer looked for them
independently and found the block's own arithmetic correct on every count this time.
Its three stated ASSUMPTIONS are accepted as assumptions rather than deviations: the C3
separator was read from the target's own convention and proved with both readers; the
Commit Gate reading at C0a/C0b is the conservative one; and naming `RunState`'s real
home, `packages.core.models`, is a correction the registration text should have carried
and the reviewer used that same import when re-running G4.

R-0822 IS FIXED ON DISK AND ITS `Done:` IS OWED BY ROUND 17, not by this session: the
`Landed:` line is on the record with its commits, which is precisely the "unreviewed
fix" state §4 item 4 wants visible, and DECISION F272 D10 rules that the line SURVIVES
beside the `Done:` paragraph that will supersede it.

## Next

**SESSION 8 OF F272 ENDS HERE**, after two delegated rounds (15 and 16), both PASS at
the first attempt with no repair round. F272's soft limit under operator amendment
amend0906-triage-throughput is 12 sessions and 40 rounds, so at session 8 and round 16
the feature is inside it and NO SCOPE REPORT IS OWED.

Why the session ends below the six-to-eight round target, in one sentence as amend0906
rule 3 requires: the reviewer's own authoring errors accumulated — round 15's block
carried TWO defects, a count gate never resolved against its own slice's paragraph count
and a containment claim written in a measurement's format without the measurement being
run — which is exactly the signal operator amendment amend0905-throughput names as an
honest early end, and the next slice is a design change that deserves a fresh context
rather than the tail of this one.

THE NEXT SESSION'S FIRST ACTION: run Phase 0, the state probe; then check `.agent/STOP`
under Phase 1 rule 1 BEFORE the Open PR Gate under rule 2, in that order. No PR exists
for this branch and none was created.

Round 17's FIRST COMMIT owes the bookings persisted here and not yet in the ledger, per
amend0827 rule 1 — exactly two, and nothing else:

1. the round 16 `Gate: F272 R16` PASS entry recorded in the verdict section above; and
2. `Done: R-0822`, the reviewer's resolution, APPENDED BESIDE the existing
   `Landed: R-0822` line and never over it, per DECISION F272 D10.

No id is minted for either.

T001 AND T002 ARE COMPLETE. Round 16 opened T003 and closed its first consumer.

ROUND 17 IS THE NEXT T003 CONSUMER, and the re-grep this session performed is the thing
to start from rather than F260's 2026-09-05 list, which is measurably stale. Measured at
`c80f32ce` over the eleven consumers F260's Design section names, the classic-store
surface that actually survives is FOUR modules, not eleven:

- `apps/cli/commands/job_context_cmd.py:223` — `load_job(resolve_job_id(job_id_str))`,
  the classic store ONLY, so `job context <ping-pong-job-id>` cannot work. F260's Design
  says this one "must work for every job". THIS IS THE RECOMMENDED ROUND 17: it is a real
  behaviour change with a provable red, and the pattern to follow is `ui_server._load_job`,
  which already tries both stores.
- `packages/orchestration/ui_server.py` — `_JobPlanTaskAdapter` at line 99, wrapped over
  `plan.tasks` at line 149. CAUTION: this is finding R-0804's subject, and the
  2026-09-06 triage in `.agent/live_review.md` routes R-0803 through R-0812 to F273
  T001 as "BOOK, do not build". See the unsettled question below before touching it.
- `apps/cli/commands/teach_cmd.py` — `resolve_any_job_id` at five sites. DO NOT move
  these in T003: DECISION F260 D5 places the resolver collapse in T004, with the store
  that makes it true.
- `apps/cli/commands/job_stop_cmd.py` — `_CoreJobAdapter` survives on purpose. It exists
  solely to adapt `storage.load_job`, so it dies in T004 WITH the classic store; deleting
  it earlier would break `job stop` for classic jobs while they still exist.

Every other consumer on F260's list — `orchestrator_loop.py`, `mission_state.py`,
`self_use_runner.py`, `self_use_job.py`, `gauntlet_runner.py`, `bench_run.py`,
`decision_inbox.py`, `checkpoints.py` — reads ZERO classic-store symbols at `c80f32ce`;
their `load_job_plan` hits are the unified reader and are the TARGET state, not work.
Re-grep before writing a slice anyway: that instruction is F260's own, and this
paragraph is a reading taken at one commit.

AN UNSETTLED QUESTION THAT MUST BE RULED BEFORE F272 CAN CLOSE, and that no round should
guess at. `docs/roadmap/features/T2_F272.md` names five tests.md finding ids — R-0803,
R-0804, R-0807, R-0810 and R-0812 — inside its Acceptance section, while the
2026-09-06 triage recorded in `.agent/live_review.md` routes those same ten ids to
**F273 T001** with the words "BOOK, do not build". F273 — Findings paydown v1 — is
registered at `docs/roadmap/STATUS.md:40` and its file `docs/roadmap/features/T2_F273.md`
exists. So F272's Acceptance currently requires items another feature owns, and F272
cannot be closed self-consistently until that is ruled. The recommended ruling, to be
recorded as DECISION F272 D12 under §4 item 7 rather than referred to the operator: the
triage is the LATER and more specific instrument and it wins, so those five ids are
F273's and F272's Acceptance is read as not requiring them, with F272's file gaining one
sentence saying so. This session did not execute that ruling because it belongs with the
round that acts on it, and because a round whose whole change set is a DECISION is the
pure-bookkeeping round amend0827 rule 1 forbids.

CONTEXT SELF-ASSESSMENT (amend0905-throughput): the context was spent on two complete
round cycles in which the reviewer applied BOTH production changes in disposable
worktrees and ran the suites BEFORE authoring either block, then independently re-ran
all sixteen gates after delegation, including two full `tests/orchestration/` runs at
roughly twelve minutes each and two `tests/cli/` runs at roughly five.
