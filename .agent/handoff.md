# Handback — F272 round 7

## Session

SESSION 3 of feature F272 · round 7 · rounds so far 7

Context self-assessment (amend0905-throughput): context is comfortable — this
round read three protocol files, one production module and one reference test
file, and spent most of its wall clock inside two multi-minute suites, so there
is ample room for further rounds this session.

## Range

Review of `df955058`..`HEAD` (8 commits, C0a through C6).

## Commits

### 1ee0e807 f272: save the round 7 step block under agent authored
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r7.md` | +367/-0 | C0a, `shutil.copyfile` of `.remedy-wt/f272-r7-block.md`, a byte copy and never a retype |

### 5202f369 f272: mirror the round 7 block into last block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +272/-236 | C0b, same source, same `shutil.copyfile`, byte-identical mirror |

### da15d721 f272: retarget the plan onto T002 and the eight administrative fields
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +24/-19 | C1, REPLACED by exactly the PLANF272R7 slice bytes |

### 353bcb0c f272: book the round 6 gate entry, finding R-0819 and the two prose slips
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | C2, RECORDR7 appended — the R6 gate record and R-0819 |
| `.agent/prose_slips.md` | +4/-0 | C2, SLIPSR7 appended — the two dated reviewer-prose lines |

### 630fd860 f272: add the eight administrative fields to the JobPlan dataclass
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | +31/-0 | C3, the eight fields at the END of the field list plus the module-level `Artifact, Budget, JobFences` import |

### c2b34ae3 f272: wire the eight administrative fields through export and import
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | +23/-0 | C4, eight export keys beside `run_refs` and eight defaulting import reads |

### 7cb6652e f272: pin the eight administrative fields through both writers and the real file
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_administrative_fields.py` | +210/-0 | C5, NEW FILE, 8 tests |

### C6 (this commit) f272: hand back round 7 with the field readings and the mutation proof
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C6, this file. A handoff cannot table the commit that writes it (R-0149 pattern). |

## Item status

| Item | Status | Reason |
|------|--------|--------------------------------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | deviated | item 3's `_import_job({})` clause is unmeetable at the base; see deviation 1 |
| C6 | done | |

## External actions

| Action | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f272-r7-base df955058` | created, for the read-only BASE measurement of G4(iii) |
| `git worktree remove .remedy-wt/f272-r7-base --force` + `git worktree prune` | removed |
| `git worktree add --detach .remedy-wt/f272-r7-g5 7cb6652e` | created, for the G5 mutation red-proof |
| `git worktree remove .remedy-wt/f272-r7-g5 --force` + `git worktree prune` | removed; `git worktree list` then showed only the primary checkout and the twelve pre-existing `remedy/job-*` entries |
| `git push -u origin feature/f272-one-world-completion` | run as this round's last action, 8 commits |
| PR create / merge | None. No PR created, none merged, nothing merged into `main`. |

## Verification

**G1 TRANSPORT — EXIT 0.** Covers the SAVED COPY and its MIRROR, not the bytes
emitted into the prompt (§3 item 37).

    .agent/authored/f272-r7.md   29940 bytes  e2b406be6fcbcf7cc55d19c2f5dc42976c955df56c1ca7d0896f9b8a86e956a1
    .agent/last_block.md         29940 bytes  e2b406be6fcbcf7cc55d19c2f5dc42976c955df56c1ca7d0896f9b8a86e956a1
    the two are byte-identical: True
    both equal BLOCK_SHA:       True
    both equal BLOCK_LENGTH 29940: True

The delegation's own BLOCK_SHA / BLOCK_LENGTH / BLOCK_LINES were verified
against `.remedy-wt/f272-r7-block.md` BEFORE any other action: sha
`e2b406be…6e956a1`, 29940 bytes, 367 lines — all three matched.

**G2 THE RECORD, at C2 — all readers accept.**

`.agent/live_review.md`:

    (a) pre terminal byte is exactly one NL: True   repr b'.\n'
    (a) pre bytes 1088550 -> post bytes 1097162 | disk bytes 1097162 | disk == post True
    (a) pre is a byte-exact prefix of post: True
    (a) post == pre + NL + slice: True
    (a) post ends in exactly one NL: True
    (a) READER A ACCEPTS: True
    (b) N counted by the script from the slice's own paragraphs: 2
    (b) units before 694 after 696 delta 2
    (b) last 2 units equal the slice paragraphs IN ORDER: True
    (b) the units before are an unchanged prefix: True
    (b) READER B ACCEPTS: True
    (c) flip offset 1090849 lies inside the FIRST appended paragraph [1088551,1093147): True
    (c) MUTATED -> reader A accepts False | reader B accepts False
    (c) RESTORED -> reader A accepts True | reader B accepts True | restored == disk image True

`.agent/prose_slips.md`:

    (a) pre terminal byte is exactly one NL: True   repr b'.\n'
    (a) pre bytes 134816 -> post bytes 135900 | disk bytes 135900 | disk == post True
    (a) pre is a byte-exact prefix of post: True
    (a) post == pre + NL + slice: True
    (a) post ends in exactly one NL: True
    (a) READER A ACCEPTS: True
    (b) N counted by the script from the slice's own paragraphs: 2
    (b) units before 171 after 173 delta 2
    (b) last 2 units equal the slice paragraphs IN ORDER: True
    (b) the units before are an unchanged prefix: True
    (b) READER B ACCEPTS: True
    (c) flip offset 135065 lies inside the FIRST appended paragraph [134817,135313): True
    (c) MUTATED -> reader A accepts False | reader B accepts False
    (c) RESTORED -> reader A accepts True | reader B accepts True | restored == disk image True

The negative control ran in memory on a `bytes` object; the disk image was never
mutated. Reader (b) was computed by splitting the WHOLE image on `\n{2,}`, with
N counted by the script from the slice's own paragraphs.

(d) COUNTS over `.agent/live_review.md`, before → after C2, every one as ordered:

| Reading | before | after | ordered |
|---|---|---|---|
| distinct `^- R-\d{4} — ` ids | 302 | 303 | 302 → 303 |
| distinct `^Done: R-\d{4} — ` ids | 247 | 247 | 247 → 247 |
| open set BY DISTINCT ID | 55 | 56 | 55 → 56 |
| `^- R-0819 — ` | 0 | 1 | 0 → 1 |
| `^Gate: ` | 28 | 29 | 28 → 29 |
| `^Gate: F272 R6 ` | 0 | 1 | 0 → 1 |

**G3 THE PLAN, at C1 — equality True.**

    .agent/plan.md == PLANF272R7 slice bytes: True
    slice bytes 2401 | disk bytes 2401
    lines 47, under the AGENTS.md cap of 50
    '## Goal' present: True | '## Next Steps' present: True

**G4 THE FIELDS EXIST AND SURVIVE A ROUND TRIP, at C4.** Measured by IMPORTING
the shipped module, never from its source text.

    module under test: /home/decodeux/Repos/remedy/packages/orchestration/pingpong_job.py

(i) `name in JobPlan.__dataclass_fields__`:

    mission True | user_prompt True | project_id True | intake True
    flight_plan True | artifacts True | budget True | fences True
    NON-VACUITY CONTROL run_refs (must be True):                     True
    NON-VACUITY CONTROL no_such_administrative_field (must be False): False

(ii) `_import_job(json.loads(json.dumps(_export_job(plan))))`, one reading per
row of the C3 table:

| field | survived | value after the round trip |
|---|---|---|
| `mission` | True | `'ship the one world record'` |
| `user_prompt` | True | `'make the job carry its mission'` |
| `project_id` | True | `'proj-f272'` |
| `intake` | True | `{'source': 'cli', 'answers': [1, 2]}` |
| `flight_plan` | True | `{'steps': ['plan', 'build'], 'version': 3}` |
| `artifacts` | True | `[Artifact(id=UUID(...), name='plan.md', content='hello', mime_type='text/plain', task_id=None, kind=<ArtifactKind.UNKNOWN: 'unknown'>, metadata={})]` |
| `budget` | True | `Budget(max_tokens=4242, max_cost_usd=1.5, max_steps=7)` |
| `fences` | True | `JobFences(allow=['packages/**'], deny=['secrets/**'])` |

(iii) THE DEFAULTED READ — the literal wording DOES NOT HOLD, and did not hold
at the base either. Both readings, as measured:

    LITERAL WORDING, _import_job({}):
      raised: KeyError "'job_id'"
    BASE df955058, measured in a disposable worktree, module resolved from
    /home/decodeux/Repos/remedy/.remedy-wt/f272-r7-base/packages/orchestration/pingpong_job.py:
      BASE _import_job({}) raised: KeyError "'job_id'"
      BASE _import_job({'job_id': ...}) returned ok

`job_id=data["job_id"]` has been a REQUIRED read since long before this round;
nothing C3 or C4 did touched it. See deviation 1. The corrected reading, which
is the old-record path the gate means:

    CORRECTED, _import_job({"job_id": "test123"}): raised False
    mission '' True | user_prompt '' True | project_id '' True | intake None True
    flight_plan None True | artifacts [] True | budget None True | fences None True

    A FULL OLD RECORD, every pre-existing key present and the eight keys popped:
    mission '' True | user_prompt '' True | project_id '' True | intake None True
    flight_plan None True | artifacts [] True | budget None True | fences None True

**G5 THE PINS CAN FAIL — MUTATION RED-PROOF.** In the disposable worktree
`.remedy-wt/f272-r7-g5` at C5 `7cb6652e`, never in the primary checkout.

    purged __pycache__ dirs before the control: 0
    pingpong_job resolves from INSIDE the worktree:
      /home/decodeux/Repos/remedy/.remedy-wt/f272-r7-g5/packages/orchestration/pingpong_job.py
    UNMUTATED CONTROL: exit 0 | 8 passed in 0.23s

One export line deleted at a time from the worktree's own copy, each exact byte
string counted in that file first (every count was 1), each followed by a
restore and a re-run of the control:

| field deleted from `_export_job` | occurrences of the byte string | EXIT | output names the field | summary line |
|---|---|---|---|---|
| `mission` | 1 | 1 | True | `3 failed, 5 passed in 0.25s` |
| `user_prompt` | 1 | 1 | True | `3 failed, 5 passed in 0.25s` |
| `project_id` | 1 | 1 | True | `3 failed, 5 passed in 0.25s` |
| `intake` | 1 | 1 | True | `3 failed, 5 passed in 0.25s` |
| `flight_plan` | 1 | 1 | True | `3 failed, 5 passed in 0.25s` |
| `artifacts` | 1 | 1 | True | `4 failed, 4 passed in 0.25s` |
| `budget` | 1 | 1 | True | `4 failed, 4 passed in 0.25s` |
| `fences` | 1 | 1 | True | `4 failed, 4 passed in 0.25s` |

    after every single restore, control exit 0 | 8 passed in 0.23s
    all eight exit 1: True
    all eight name their field: True
    worktree file restored byte-identical at the end: True

NO field's deletion left the run at exit 0. The worktree was removed by exact
path and pruned before this handback.

**G6 THE SUITES, run SERIALLY, each its own invocation.**

| command | EXIT | summary line, verbatim |
|---|---|---|
| `python3 -B -m pytest tests/orchestration/test_job_administrative_fields.py -q -p no:randomly` | 0 | `8 passed in 0.28s` |
| `python3 -B -m pytest tests/orchestration/ -q -p no:randomly` | 0 | `12817 passed, 10 skipped, 1 warning in 740.49s (0:12:20)` |
| `python3 -B -m pytest tests/cli/ -q -p no:randomly` | 0 | `1537 passed in 306.84s (0:05:06)` |
| `python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly` | 0 | `42 passed in 21.15s` |

Against the reviewer's `df955058` measurements: `tests/orchestration/` rose
12809 → 12817, a rise of EXACTLY 8, which is the eight tests C5 adds and nothing
else; skips unchanged at 10. `tests/cli/` 1537 → 1537, unchanged. Canary 42 →
42, unchanged. No count fell anywhere.

**G7 LINT AND INTEGRITY, at C5.**

    EXIT 0 | python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_administrative_fields.py
            All checks passed!
    EXIT 0 | python3 -m apps.cli.grouped integrity check --json
            "passed": true, "fail_count": 0, "check_count": 5, 5 of 5 pass

A repo-wide `ruff check .` was NOT run; it is not ordered and is red on base
under OPEN finding R-0468.

**G8 THE TREE.**

    git status --porcelain: '' (EMPTY, with C6 staged)
    git ls-files .remedy-wt: '' (EMPTY)

`git worktree list` after removal named only the primary checkout at
`feature/f272-one-world-completion` and the twelve pre-existing `remedy/job-*`
entries, which predate this round and stay. Both worktrees this round created
were removed BY EXACT PATH, never by glob.

Per commit, C0a through C5 (NOT C6, which cannot count its own insertions, §3
item 14), from `git diff --numstat <parent> <commit>`, cross-checked cell by
cell against the `## Commits` table above:

| commit | single-parent | + | - | under the F104 D1 cap of 500 | matches the table |
|---|---|---|---|---|---|
| 1ee0e807 C0a | True | 367 | 0 | True | yes |
| 5202f369 C0b | True | 272 | 236 | True | yes |
| da15d721 C1 | True | 24 | 19 | True | yes |
| 353bcb0c C2 | True | 8 | 0 | True | yes (4+4 across two files) |
| 630fd860 C3 | True | 31 | 0 | True | yes |
| c2b34ae3 C4 | True | 23 | 0 | True | yes |
| 7cb6652e C5 | True | 210 | 0 | True | yes |

THE FULL-FILE REWRITE, where the file's line counts and the diff's columns
diverge exactly as the block predicted: `.agent/last_block.md` is 29940 bytes
and 367 newline-terminated lines on disk, while its diff reads +272/-236,
because git matched 95 lines shared with the round 6 block. The table carries
the DIFF numbers, not the file numbers. `.agent/authored/f272-r7.md` is a new
file, so its two readings agree at 367.

Marker sweep, lines beginning `<<<BEGIN ` or `<<<END ` in every written
non-block file:

    .agent/plan.md 0 | .agent/live_review.md 0 | .agent/prose_slips.md 0
    packages/orchestration/pingpong_job.py 0
    tests/orchestration/test_job_administrative_fields.py 0
    .agent/handoff.md 0

`.agent/STOP` readings, constraint 9, by `os.path.exists`, all three:

| when | exists |
|---|---|
| before C0a | False |
| before C3 | False |
| before C6 | False |

## Authored-text proofs

| Slice | Target | Proof |
|---|---|---|
| PLANF272R7 | `.agent/plan.md` | disk bytes == slice bytes, 2401 == 2401, byte-equal True |
| RECORDR7 | `.agent/live_review.md` | `post == pre + NL + slice` True; readers (a) and (b) both accept; negative control rejects and the restore re-accepts |
| SLIPSR7 | `.agent/prose_slips.md` | `post == pre + NL + slice` True; readers (a) and (b) both accept; negative control rejects and the restore re-accepts |
| the block itself | `.agent/authored/f272-r7.md`, `.agent/last_block.md` | both 29940 bytes, both sha256 `e2b406be…6e956a1`, both equal to `.remedy-wt/f272-r7-block.md` |

Exactly one `<<<BEGIN name>>>` and one `<<<END name>>>` line was asserted for
each of the three slice names before extraction. No slice was edited; marker
lines reached no target file.

## Deviations & assumptions

**1. G4(iii) AND C5 ITEM 3 ARE UNMEETABLE AS LITERALLY WORDED, AND WERE ALREADY
UNMEETABLE AT THE BASE. This is the ONLY substantive deviation and it is the
same class as the R-0819 this round just booked.** Both order
`_import_job({})` to "return a `JobPlan` … and not raise". It raises
`KeyError('job_id')`, because `_import_job`'s very first argument is
`job_id=data["job_id"]` — a required subscript, not a `.get`. Measured at the
base `df955058` in a disposable worktree, before this round's code existed:
identical `KeyError "'job_id'"`. So the gate could not have passed on any commit
of this feature, and no edit inside this round's change set could make it pass.

WHAT I DID NOT DO: I did not give `job_id` a default. That is a behaviour change
to an EXISTING field, which constraint 6 forbids outright ("Behaviour changes:
NONE for any existing field"), and it is a real design question — whether a job
record may exist without an id — that wants its own ruling rather than a silent
edit smuggled in to turn a gate green.

WHAT I DID INSTEAD: reported BOTH readings above, and wrote the C5 defaulted-read
tests against the smallest record that CAN load, `{"job_id": "0123456789abcdef"}`
— which is exactly the shape `test_job_run_refs.py::test_record_without_run_refs_key_imports_empty`
already uses for the same purpose — plus a second test over a FULL old record
with every pre-existing key present and only the eight new keys popped, which is
the realistic old-record path. I additionally pinned the measured truth in
`test_job_id_stays_the_one_required_key`, whose docstring names this gate and
the base measurement, so the next reader cannot mistake the KeyError for damage
this round did. That test goes red if `job_id` ever becomes optional, which is
the ruling this deviation is really asking for.

I am declaring this as a defect in the BLOCK, not in the product: G4(iii) was
ordered without being run at its base, which is precisely the counter-measure
R-0819's own FIX clause makes binding on the next block of this feature. I mint
no id for it (constraint 7) and leave the classification to the reviewer.

**2. C5 item 1 says "the two mutable ones (`artifacts`)" — a numeral standing
over a list of one.** Among the eight, exactly ONE field has a mutable default
and therefore a `default_factory`: `artifacts`. `intake` and `flight_plan`
default to `None`, which is immutable and shares nothing. I applied the
ENUMERATION and pinned `first.artifacts is not second.artifacts`, and pinned
nothing for the other seven, because there is nothing to pin. This is the same
§3 item 16 class the block's own SLIPSR7 slice describes twice, so I note it
rather than silently absorbing it. Nothing wrong reached disk.

**3. The C3 `I001` contingency did not arise.** The block said that if ruff's
`I001` reorders the import block as a consequence of the new module-level
import, apply the fix and declare it. It did not: I placed
`from packages.core.models import Artifact, Budget, JobFences` in sorted position
above the existing `packages.orchestration.data_paths` import, and
`python3 -m ruff check packages/orchestration/pingpong_job.py` was EXIT 0
immediately. `ruff check --fix --select I001` was never run and no import line
was combined or moved by a tool.

**4. C0a and C0b precede C1, so `.agent/plan.md` is not yet retargeted when the
first two commits land.** This is the block's own ordered commit sequence
(constraint 3, which names C1 "the first substantive commit"), not a departure
from it, and it matches the accepted precedent of round 6's deviation 6. Noted
here because AGENTS.md's Commit Gate asks for a current plan before EVERY
commit, and C0a/C0b are transport saves of the block that retargets it.

**5. The C4 walrus was kept, with named locals.** The block offered "a plain
local" as an alternative if a walrus inside the argument list read badly. I kept
the walrus but bound `_budget` and `_fences` rather than one-letter names, so
the two lines read as ordinary conditionals. Ruff EXIT 0. The requirement the
block stated — the DEFAULTING BEHAVIOUR — is what G4(iii)'s corrected reading and
C5's two defaulted-read tests measure.

**6. Assumption, stated because it is load-bearing for the `artifacts` pin.**
`Artifact.id` is a `UUID` and `kind` an enum, so `model_dump(mode="json")` emits
strings and `Artifact(**a)` coerces them back. Equality after the round trip is
therefore real Pydantic equality on identical values, not a string comparison —
measured True in G4(ii) and again through the real file in C5's last test.

No other deviation. No `Done:` paragraph was written and no finding id was
minted (constraint 7). No file outside the block's change set was touched.

## Next

The reviewer re-runs G1 to G8 independently against `df955058`..`7cb6652e` plus
this handback commit, and rules on deviation 1: whether `_import_job({})`
raising `KeyError('job_id')` is a defect to register against the block's G4(iii)
wording, and whether `job_id` should stay a required key. Then round 8, which
the plan's Next Steps name: the three administrative fields that COLLIDE with an
existing spelling, of which `state` absorbing `status` as one `RunState` field is
the type change with wide reach that needs its own ruling first.
