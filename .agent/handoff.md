# Handoff — F260 One world: mission → job → run, round 7

## Session

`SESSION 2 of feature F260 · round 7 · rounds so far 7`

Well inside the 25-round / 7-session soft limit, so no scope report is owed.

Open findings: **295** (299 `^- R-\d{4} — ` registrations minus 4
`^Done: R-\d{4} — ` lines) — unchanged, because this round registers and
resolves nothing. Maximum id in use: **R-0814**. R-0814's root cause is what
this round's code finishes addressing — "one spelling per concept" failing
across modules — but the finding itself is resolved in the T002 writer round,
against the fix clause it already carries.

Branch `feature/f260-one-world`, resumed at `99ca6406`. No branch created, no
merge, no pull request touched — the pull request belongs to the closure
sequence.

## Range

Review of `99ca6406..HEAD`.

## Commits

### 7afe3056 f260: save the round 7 step block as authored input (C0a, +294)

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r7.md | +294 / -0 | the round 7 block, copied with `shutil.copyfile`, never retyped |

### f9c648ac f260: mirror the round 7 step block into last_block (C0b, +197)

| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +197 / -267 | same bytes as C0a; the round 6 block it replaces was longer |

### adc66ae4 f260: book the round 6 gate record into the live review ledger (C1, +2)

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | `"\n"` + the 6674-byte GATE_R6 slice + `"\n"`; 887129 → 893805 bytes |

### 36c4c375 f260: append the round 6 reviewer recipe slip (C2, +2)

| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 / -0 | `"\n"` + the 2127-byte SLIP6 slice + `"\n"`; 92673 → 94802 bytes |

### 1ad4c238 f260: point the plan at the remaining evidence path swaps (C3, +17)

| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +17 / -19 | replaced entirely with the PLANF260R7 slice plus one trailing newline; 46 lines |

### 246efbb9 f260: put the last four evidence paths on data_paths and widen the guard (C4, +96)

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/job_evidence.py | +4 / -4 | two sites: `ev_base` in the attestation-snapshot reader and `src_task` in the task-stream export, both onto `job_evidence_dir`; each function-scoped import moved with its site |
| packages/orchestration/repair_attest.py | +2 / -2 | `base` onto `job_evidence_dir`; its import is MODULE-LEVEL and moved in place, keeping the module's existing import style |
| apps/cli/commands/do_cmd.py | +2 / -2 | `_task_ev_dir` in the task-stream trace reader onto `job_evidence_dir`; function-scoped import moved with it |
| tests/test_data_paths.py | +88 / -13 | the round 6 guard widened from one module to the semantically-defined set of four, parametrized, plus two non-vacuity tests |

### C5 f260: hand back round 7 (this file)

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | this rewrite | a handoff cannot table the commit that writes it (R-0149 pattern) |

Largest commit this round is 294 insertions, a single `.agent/**` state write;
the largest code commit is 96. Both are under the AGENTS.md 500-insertion cap.

## External actions

| Action | Outcome |
|---|---|
| `git worktree add .remedy-wt/f260-r7-mut 246efbb9` | created, detached at `246efbb9`; name confirmed not to exist beforehand |
| `git worktree remove --force .remedy-wt/f260-r7-mut` | removed; `git worktree list` then holds only the primary checkout and eleven PRE-EXISTING `job-*` worktrees, none created this round |
| `git push origin feature/f260-one-world` | run after C5; never force-pushed |

No branch created, no merge, no pull request created, edited or merged. No `gh`
command run.

## Verification

One line per gate, with its real exit code.

| Gate | Exit | Result |
|---|---|---|
| G1 TRANSPORT | 0 | one digest `dcc306d01cc944bf8b03993c76882ff8ccb30881909cd2855160c573e66de8c0` across all three artefacts, equal to BLOCK_SHA |
| G2 THE RECORD | 0 | 887129 → 893805, growth 6676 = `"\n"` + 6674 + `"\n"`; prefix, remainder and last-unit all exact; both region-disjoint controls reject in their own region; 424 → 425 units; 299 / 4 / 16 distinct `Gate:` headers |
| G3 THE PROSE FILES | 0 | terminal byte before the append was `\n`; 92673 → 94802; units 128 → 129, a rise of EXACTLY ONE; plan == slice + one newline, 46 lines |
| G4 THE SWAPS ARE VALUE-PRESERVING | 0 | all four migrated expressions equal their hand-built forms, paths reported below |
| G5 THE CODE | 0 | ruff clean; AST counts 0/0/0/0 migrated and 2/2 excluded; range numstat exactly four code paths |
| G6 THE MUTATION RED-PROOF | 0 | control exit 0 at 40 passed before and after each; three mutations each exit 1 |
| G7 THE SUITES | 0 | eight suites serially, every one exit 0, 603 tests |
| G8 THE TREE AND THE CHANGE SET | 0 | porcelain empty, `ls-files .remedy-wt` empty, no STOP, no worktree left; integrity `passed: true`, `fail_count: 0` |

### G1 TRANSPORT — exit 0

    $ sha256sum .remedy-wt/f260-r7-block.md .agent/authored/f260-r7.md .agent/last_block.md
    dcc306d01cc944bf8b03993c76882ff8ccb30881909cd2855160c573e66de8c0  .remedy-wt/f260-r7-block.md
    dcc306d01cc944bf8b03993c76882ff8ccb30881909cd2855160c573e66de8c0  .agent/authored/f260-r7.md
    dcc306d01cc944bf8b03993c76882ff8ccb30881909cd2855160c573e66de8c0  .agent/last_block.md

ONE value, equal to the BLOCK_SHA the delegating prompt stated. Per §3 item 37
this chain covers those three artefacts on disk and is NOT a claim about the
bytes emitted into the worker's prompt.

### G2 THE RECORD — exit 0

    pre  bytes (99ca6406): 887129
    post bytes (246efbb9): 893805
    growth: 6676 | appended byte count: 6676 | equal: True
    slice bytes: 6674
    (a) pre-image is a byte-exact PREFIX      : True
    (b) remainder is exactly \n + slice + \n  : True
    (c) last blank-line unit == GATE_R6 slice : True

    -- negative controls, in scratch copies, one per region --
    control 1 flip INSIDE appended paragraph at offset 890467
       (c) last-unit reading rejects : True   [(a) still True ]
    control 2 flip INSIDE pre-image region at offset 443564
       (a) prefix reading rejects    : True   [(c) still True ]

    blank-line units before: 424  after: 425
    post ends with exactly one newline: True
    ^- R-[0-9]{4} — matches      : 299 (expected 299)
    ^Done: R-[0-9]{4} — matches  : 4 (expected 4)
    ^Gate:  headers              : 16
    Gate headers all distinct    : True

The controls are region-disjoint as the round 5 deviation earned: a flip in the
appended paragraph is caught ONLY by the last-unit reading and leaves the prefix
reading true, and a flip in the pre-image region is caught ONLY by the prefix
reading and leaves the last-unit reading true. Neither reading subsumes the
other. Sixteen `Gate:` headers, one more than round 6's fifteen, which is this
round's C1 append and nothing else.

### G3 THE PROSE FILES — exit 0

THE READING THIS ROUND EXISTS FOR, reported before the append as ordered:

    LAST BYTE BEFORE THE APPEND: b'\n' = newline
      tail before: b'end0827-process-diet rule 2).\n'
    bytes before: 92673  after: 94802
    growth: 2129 | appended: 2129 | equal: True
    pre-image is a byte-exact PREFIX     : True
    remainder is exactly \n + SLIP6 + \n : True
    blank-line units before: 128  after: 129  rise: 1
    RISES BY EXACTLY ONE, to 129        : True
    bytes at the seam: b'\n\n' -> blank line present: True
    last unit == SLIP6: True
    ends with exactly one newline: True

`.agent/prose_slips.md` NOW ENDS WITH A NEWLINE, so the block's C2 paragraph is
correct and the leading `"\n"` created a real blank-line separator. The file
gained that terminal newline precisely because round 6's malformed append
terminated the previous line — the defect repaired its own precondition. The
structural count is the reading that proves it: 128 → 129, and the two bytes at
the seam are `\n\n`. Under the round 6 recipe against the round 6 pre-image this
number would not have moved, which is exactly what the counter-measure is for.

    .agent/plan.md
    equals PLANF260R7 + exactly one trailing newline: True
    line count: 46  under 50: True

### G4 THE SWAPS ARE VALUE-PRESERVING — exit 0

`REMEDY_DATA_DIR` = `/tmp/f260r7-g4-s2c8nxx3`, job id `0123456789abcdef`, task
id `T001`. Paths reported, not just booleans:

    job_evidence.py / attestation-snapshot  ev_base
      new  : /tmp/f260r7-g4-s2c8nxx3/jobs/0123456789abcdef/evidence
      old  : /tmp/f260r7-g4-s2c8nxx3/jobs/0123456789abcdef/evidence
      equal: True

    job_evidence.py / task-stream export    src_task
      new  : /tmp/f260r7-g4-s2c8nxx3/jobs/0123456789abcdef/evidence/task_runs/T001/streams
      old  : /tmp/f260r7-g4-s2c8nxx3/jobs/0123456789abcdef/evidence/task_runs/T001/streams
      equal: True

    repair_attest.py                        base
      new  : /tmp/f260r7-g4-s2c8nxx3/jobs/0123456789abcdef/evidence
      old  : /tmp/f260r7-g4-s2c8nxx3/jobs/0123456789abcdef/evidence
      equal: True

    do_cmd.py / trace reader                _task_ev_dir
      new  : /tmp/f260r7-g4-s2c8nxx3/jobs/0123456789abcdef/evidence/task_runs/T001
      old  : /tmp/f260r7-g4-s2c8nxx3/jobs/0123456789abcdef/evidence/task_runs/T001
      equal: True

    ALL FOUR VALUE-PRESERVING: True

This is the no-behaviour-change property the four swaps rest on.

### G5 THE CODE — exit 0, all three readings

(a) ruff:

    $ python3 -m ruff check packages/orchestration/job_evidence.py \
        packages/orchestration/repair_attest.py apps/cli/commands/do_cmd.py
    All checks passed!            [exit 0]

    $ python3 -m ruff check tests/test_data_paths.py
    All checks passed!            [exit 0]

The second command is beyond the gate; the guard file changed, so it was read.

(b) AST references resolving to exactly `jobs_dir` — all six numbers:

    pingpong_job.py       0  lines=[]
    job_evidence.py       0  lines=[]
    repair_attest.py      0  lines=[]
    do_cmd.py             0  lines=[]
    checkpoints.py        2  lines=[225, 227]
    storage.py            2  lines=[25, 49]

The migrated set is 0 across the board; the excluded pair is NON-ZERO, which is
the non-vacuity half — a guard reading zero everywhere would be measuring
nothing. `job_evidence.py` still names `_jobs_dir` at lines 1149 and 1160 and
`pingpong_job.py` names it at seven sites; that is a DIFFERENT symbol which
merely contains the same substring, it is correctly invisible to the AST
reading, and it was left alone as ordered.

(c) `git diff --numstat 99ca6406..246efbb9` over code, exactly four rows:

    2   2   apps/cli/commands/do_cmd.py
    4   4   packages/orchestration/job_evidence.py
    2   2   packages/orchestration/repair_attest.py
    88  13  tests/test_data_paths.py

### G6 THE MUTATION RED-PROOF — exit 0

Disposable worktree `.remedy-wt/f260-r7-mut` at `246efbb9`. An editable install
`remedy 0.1.0 -> /home/decodeux/Repos/remedy` exists and COULD have shadowed the
worktree, so resolution was probed before any mutation was trusted:

    data_paths -> /home/decodeux/Repos/remedy/.remedy-wt/f260-r7-mut/packages/orchestration/data_paths.py

Every run purges `__pycache__` inside the worktree and uses `python3 -B` and
`-p no:cacheprovider`. Restores write back the captured original bytes; no
`git checkout --` was used on any file.

    UNMUTATED CONTROL (before):
      exit=0  passed=40  failed=0

    MUTATION (i)   job_evidence.py spells the evidence path itself again
      exit=1  passed=39  failed=1
         FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_no_module_that_owns_job_evidence_spells_the_path_itself[packages.orchestration.job_evidence]
      restored; control again: exit=0  passed=40  failed=0

    MUTATION (ii)  repair_attest.py spells the evidence path itself again
      exit=1  passed=39  failed=1
         FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_no_module_that_owns_job_evidence_spells_the_path_itself[packages.orchestration.repair_attest]
      restored; control again: exit=0  passed=40  failed=0

    MUTATION (iii) data_paths.job_evidence_dir returns jobs_dir(root)/"evidence"/job_id
      exit=1  passed=38  failed=2
         FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_the_record_and_the_evidence_share_one_root
         FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_the_root_override_is_honoured_by_all_four
      restored; control again: exit=0  passed=40  failed=0

Mutations (i) and (ii) each fail ONLY their own parametrized case, which is the
discriminator: the parametrization is real, and a regression in one module
cannot be masked by another module being clean. Mutation (iii) is the one the
block predicted — breaking the layout function reddens the ROUND 6 value tests,
not the widened guard, proving the guard did not replace them and that both
readings still ship. `git worktree list` after the removal holds the primary
checkout plus eleven pre-existing `job-*` worktrees; the round created one
worktree and removed it, and deleted nothing it did not create.

### G7 THE SUITES — every suite exit 0

Run serially, one process per suite, exit code captured per process — never
through a pipe.

| Suite | Exit | Passed |
|---|---|---|
| tests/test_data_paths.py | 0 | 40 |
| tests/orchestration/test_job_evidence.py | 0 | 93 |
| tests/orchestration/test_repair_attest.py | 0 | 37 |
| tests/orchestration/test_stream_export_e2e.py | 0 | 7 |
| tests/orchestration/test_evidence_index.py | 0 | 33 |
| tests/test_do_job_flow.py | 0 | 178 |
| tests/orchestration/test_pingpong_cli.py | 0 | 173 |
| tests/cli/test_golden_path.py | 0 | 42 |

603 tests, all green. `tests/test_data_paths.py` went 35 → 40: the single guard
became four parametrized cases (+3) and two non-vacuity tests were added (+2).
The other seven suites are unchanged in count, which is the no-behaviour-change
claim read from the consumers of all four migrated call sites.

### G8 THE TREE AND THE CHANGE SET — exit 0

    $ git status --porcelain          -> empty
    $ git ls-files .remedy-wt         -> empty
    $ ls .agent/STOP                  -> No such file or directory (absent)
    $ git check-ignore -v .remedy-wt/f260-r7-block.md
      .gitignore:235:.remedy-wt/	.remedy-wt/f260-r7-block.md

`git diff --name-only 99ca6406..246efbb9`, as the command printed it:

    .agent/authored/f260-r7.md
    .agent/last_block.md
    .agent/live_review.md
    .agent/plan.md
    .agent/prose_slips.md
    apps/cli/commands/do_cmd.py
    packages/orchestration/job_evidence.py
    packages/orchestration/repair_attest.py
    tests/test_data_paths.py

NINE paths, not eight — see deviation 1. The SET is exactly the block's change
set minus `.agent/handoff.md`, verified by set comparison, not by eye.

    $ python3 -m apps.cli.grouped integrity check --json
    "passed": true, "fail_count": 0, "check_count": 5
      handler_import       pass  handlers=342
      live_review_verdict  pass
      plan_consistency     pass  unchecked=0, context_complete=False
      relevant_untracked   pass  untracked=0, relevant=0
      high_blockers_open   pass  no open blocker/high findings

## Authored-text proofs

Re-extracted from the COMMITTED `.agent/authored/f260-r7.md`, not from the
scratch original, so the proof runs disk to disk across the transport:

| Slice | Bytes | Target | Result |
|---|---|---|---|
| GATE_R6 | 6674 | .agent/live_review.md | prefix exact, remainder `\n`+slice+`\n` exact, last unit == slice |
| SLIP6 | 2127 | .agent/prose_slips.md | prefix exact, remainder `\n`+slice+`\n` exact, last unit == slice |
| PLANF260R7 | 2408 | .agent/plan.md | file == slice + exactly one trailing newline |

No slice carries trailing whitespace on any line. No slice was retyped: C0a and
C0b used `shutil.copyfile`, and every application read the slice out of the
block file's bytes programmatically.

## Deviations & assumptions

**1. The block's G8 says "eight paths"; the correct number is NINE. Measured,
not estimated.** The block's own change-set list holds TEN entries, so minus
`.agent/handoff.md` it is nine, and `git diff --name-only 99ca6406..246efbb9`
prints nine. Counted mechanically rather than by eye:

    change-set entries in the block (10)
    change set MINUS .agent/handoff.md: 9 paths
    block's G8 asserts: eight
    actual cardinality : 9
    git diff --name-only reports 9 paths
    range set == change set minus handoff: True

The numeral is wrong; the SET is right and complete. Nothing outside the change
set was created, edited or deleted. This is the "count your own enumeration"
class: a gate that states a cardinality it never counted. Applied as ordered and
declared here rather than repaired.

**2. "Last blank-line unit equals the slice" needs a stated convention, and the
raw comparison is False without it.** A blank-line unit split on `\n[ \t]*\n`
gives a FINAL unit that carries the file's own terminating newline, so it is
slice + `"\n"` and one byte longer than the slice, which by the block's own
definition excludes the newline ending its last content line. Measured:

    raw last unit len: 6675 slice len: 6674
    raw last == slice: False
    raw last rstripped of \n == slice: True
    diff is exactly one trailing newline: True

G2(c) and G3 are therefore evaluated with the file's terminating newline
stripped from the final unit. This is a reading convention, not a change to what
landed; the bytes on disk are exactly `"\n"` + slice + `"\n"` as G2(b) proves
independently. Flagged because a reviewer running the naive comparison will get
False on a correct file.

**3. The widened guard was RENAMED, and two tests were added beyond the block.**
The block named `test_pingpong_job_no_longer_spells_the_evidence_path_itself` to
identify what to widen. Since it now ranges over four modules, that name would
falsely claim single-module scope, so it is
`test_no_module_that_owns_job_evidence_spells_the_path_itself`, parametrized
over `_JOB_EVIDENCE_OWNING_MODULES`. Constraint 1 binds authored SLICES byte for
byte; the guard is described in prose, not shipped as a slice, so naming is mine.
The block ordered parametrization, which changes node ids regardless. Verified
first that no code depends on the old node id — the only references are frozen
prose in `.agent/live_review.md`, `.agent/last_block.md` and the previous
handoff. Two tests were added beyond the ordered non-vacuity assertion:

  * `test_the_job_evidence_owning_module_set_is_real` — the ordered one: the set
    is non-empty, duplicate-free, and every member imports with a readable
    source file.
  * `test_the_classic_store_modules_still_call_jobs_dir` — NOT ordered. It makes
    G5(b)'s non-vacuity half permanent: if `jobs_dir` were simply deleted
    everywhere, the absence guard would pass for the wrong reason. Measured 2
    references in each of `checkpoints.py` and `storage.py` before asserting it,
    rather than assuming the block's claim.

**4. `repair_attest.py`'s import is module-level and one swap retired the whole
import in three modules.** Each of the four sites was the LAST use of `jobs_dir`
in its module, so each import had to move to `job_evidence_dir` in the same edit
or ruff would report an unused import. Verified per module by AST both before
and after — the block's claim that these modules reference `jobs_dir` at exactly
those four sites is confirmed, not assumed. Each module's existing import style
was kept: module-level in `repair_attest.py`, function-scoped in the other three.

**5. Line numbers were re-grepped, not trusted, and the block's were correct.**
The block warned they might be stale after round 6's deviation 2. At `99ca6406`
they resolve as `repair_attest.py:34` import / `:153` site,
`job_evidence.py:1346` import / `:1348` site and `:2885` import / `:2892` site,
`do_cmd.py:2414` import / `:2458` site. All four matched the block's description
exactly; the one line number the block asserted, `repair_attest.py:34`, is right.

**6. `checkpoints.py` and `storage.py` were not touched**, as ordered, and the
reason is now written into the guard's docstring and the module-set comment so a
later reader can justify the exclusion instead of deleting it.

**7. No deviation from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4,
C5, each its own commit, in order, with C4 as ONE commit carrying the four swaps
and the widened guard together. No extra commit, none dropped, none reordered.

Assumption: none load-bearing. Every number in this handback was measured this
round; nothing was carried forward from the round 6 record.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | 7afe3056, +294, `shutil.copyfile` |
| C0b mirror the block | done | f9c648ac, +197 |
| C1 the record | done | adc66ae4, +2 |
| C2 the slip | done | 36c4c375, +2; terminal byte was `\n`, units rose by exactly one |
| C3 the plan | done | 1ad4c238, +17, 46 lines |
| C4 the four call sites and the widened guard | done | 246efbb9, one commit, +96 |
| C5 the handback | done | this file |
| G1 TRANSPORT | done | exit 0, one digest = BLOCK_SHA |
| G2 THE RECORD | done | exit 0, both region-disjoint controls behave as split |
| G3 THE PROSE FILES | done | exit 0, 128 → 129, the round 6 counter-measure holds |
| G4 THE SWAPS ARE VALUE-PRESERVING | done | exit 0, all four paths equal |
| G5 THE CODE | done | exit 0, all three readings, six AST numbers |
| G6 THE MUTATION RED-PROOF | done | control exit 0 at 40, three mutations each exit 1 |
| G7 THE SUITES | done | eight suites, all exit 0, 603 tests |
| G8 THE TREE AND THE CHANGE SET | done | exit 0, integrity passed; block's "eight" is nine — deviation 1 |

DECISION F260 D1 now has ONE spelling in every module that owns a job's
evidence. T002's layout consolidation is finished; what remains in T002 is the
unified record and its writer.

## Next

The reviewer independently re-runs G1 through G8 and reads the real diff of
`99ca6406..HEAD` before any verdict. The next build round is the unified Job
record and its writer under `jobs/<16hex>/job.json`, moving `_persist_job` and
`load_job_plan` off `task_jobs/` and DELETING `pingpong_job._jobs_dir`, with
finding R-0814 resolved there against the fix clause it already carries.
