# Handback — F272 round 1

## Session

SESSION 1 of feature F272 · round 1 · rounds so far 1

Context self-assessment: this is the feature's first round on a fresh branch;
the worker's context was comfortable throughout and nothing was abbreviated.

## Range

Review of b18fad576252f7f2739a5807b6408031da8fcde6..HEAD (the branch point of
`feature/f272-one-world-completion`, i.e. the merge commit of pull request 242).

## Item status — C0a through C6

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | |
| C6   | done   | this commit |

## Commits

### 4e524d0b f272: save the round 1 block as the authored original
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f272-r1.md | +488/-0 | C0a — the round's block, copied with `shutil.copyfile` |

### a23c3748 f272: mirror the round 1 block into the last-block slot
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +472/-382 | C0b — same bytes, one indivisible `.agent/**` state rewrite |

### 9b5312b2 f272: point the plan and the context at the F272 branch
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +43/-34 | C1 — PLANF272R1 slice, whole file |
| .agent/context.md | +14/-13 | C1 — CONTEXTF272 slice, whole file |

### 5b14f469 f272: re-head the live review record at the F272 claim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +28/-22 | C2 — HEAD1 and STEPS pairs only; nothing below `## Findings` moved |

### 754bd14e f272: claim F272 in the roadmap ledger
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | +1/-1 | C3 — STATUS pair, `[ ]` → `[~]` on F272 |

### 6955a197 f272: give the job record the plural run list run_refs
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/pingpong_job.py | +10/-0 | C4 — the field (a), the export/import (b), the population in `run_job` (c) |

### c16ad23d f272: pin the plural run list with four tests
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_job_run_refs.py | +122/-0 | C5 — the four tests, new file |

### C6 — this commit (a handoff cannot table the commit that writes it, R-0149)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | C6 — this handback |

Per-commit insertion counts (`git diff --numstat <parent> <commit>`, the `+`
column only, AGENTS.md DECISION F104 D1), each commit single-parent:

    C0a 4e524d0b insertions=488 parents=1
    C0b a23c3748 insertions=472 parents=1
    C1  9b5312b2 insertions=57  parents=1
    C2  5b14f469 insertions=28  parents=1
    C3  754bd14e insertions=1   parents=1
    C4  6955a197 insertions=10  parents=1
    C5  c16ad23d insertions=122 parents=1

## External actions

    git checkout -b feature/f272-one-world-completion      -> on main at b18fad57, clean tree
    git worktree add .remedy-wt/f272-g7-wt c16ad23d        -> detached HEAD c16ad23d (G7 only)
    git worktree remove --force .remedy-wt/f272-g7-wt      -> removed
    git worktree prune                                     -> ok; `git worktree list` no longer lists it
    git push -u origin feature/f272-one-world-completion    (run immediately after this commit)

No `gh pr merge`, no `gh pr create`, no merge, no force-push. The Open PR Gate
was NOT re-run: the block records that it already ran in the reviewer's session
and that pull request 242 was merged at b18fad57.

## Verification

**G1 TRANSPORT** — exit 0.

    sha256      = 229900f50fc6cf7dfc85d54ab2e6631cc6e8ec5cf08be54db92bf13f627e0165
    byte length = 27393
    filecmp source-vs-saved  (shallow=False) = True
    filecmp source-vs-mirror (shallow=False) = True
    committed C0a  .agent/authored/f272-r1.md  sha256 229900f5...627e0165  bytes 27393
    committed C0b  .agent/last_block.md        sha256 229900f5...627e0165  bytes 27393

That digest equals BLOCK_SHA as stated in the delegating prompt; it was verified
against the source file BEFORE any other step of this round.

**G2 THE RECORD**, at C2 5b14f469.

(a) BYTE. pre 955525 bytes → post 955908 bytes; disk image == committed image.
An independent reconstruction, built from the C1 pre-image with ONLY
HEAD1_FROM→HEAD1_TO and STEPS_FROM→STEPS_TO applied, is 955908 bytes and
compares EQUAL to the committed post-image. The file ends in exactly one
newline. Per-pair containment at apply time: HEAD1 FROM 1→0, TO 0→1;
STEPS FROM 1→0, TO 0→1.

(b) THE CARRIED REGION, before and after:

    reviewer's convention (region starts at the newline terminating the
    line before `## Findings`):
      before  953408 bytes  147ce009557d42bc81def2249853ed1a8fccd60676077a08e9532aea0bc0f8dc
      after   953408 bytes  147ce009557d42bc81def2249853ed1a8fccd60676077a08e9532aea0bc0f8dc
    the strictly-from-the-`#` reading, reported for completeness:
      before  953407 bytes  447b08c3937da2d0c600f4f20f1e8736b24913022cc28c7a1f68f4ae7ec5a45a
      after   953407 bytes  447b08c3937da2d0c600f4f20f1e8736b24913022cc28c7a1f68f4ae7ec5a45a

The block's stated figures (953408 / 147ce009…) reproduce exactly under the
first convention and are UNCHANGED across C2. Both readings are unchanged.

(c) COUNTS, before → after:

    distinct ids '^- R-\d{4} — '     301 → 301
    distinct ids '^Done: R-\d{4} — '   3 → 3
    open set BY DISTINCT ID          298 → 298
    '^Gate: ' lines                   23 → 23

(d) NEGATIVE CONTROL, on in-memory `bytes` objects only, nothing written to
disk: one byte flipped at offset 20, inside the HEAD1_TO span (0..1650) —
reader (a) ACCEPTS = False. Restored — reader (a) ACCEPTS = True, and the
restored image == the disk image.

**G3 THE PLAN AND THE CONTEXT**, at C1 9b5312b2.

    .agent/plan.md    bytes=2097  equals PLANF272R1 + exactly one trailing newline = True
    .agent/context.md bytes=3366  equals CONTEXTF272 + exactly one trailing newline = True
    .agent/plan.md line count = 43 (< 50 = True); '## Goal' = True; '## Next Steps' = True

    $ python3 -m pytest tests/ui_server/ -q -p no:randomly
    exit = 0 ; 515 passed in 33.42s
    $ python3 -m pytest tests/orchestration/test_test_runner.py \
        tests/regression/test_resource_safety.py \
        tests/orchestration/test_integrity_gate.py -q -p no:randomly
    exit = 0 ; 89 passed in 17.13s

**G4 THE STATUS CLAIM**, at C3 754bd14e.

    '^- \[~\] F272 — '        = 1  (expected 1)
    '^- \[ \] F272 — '        = 0  (expected 0)
    '^- \[x\] F\d{3} — '      = 74 (expected 74)
    '^- \[[ x~!]\] F\d{3} — ' = 272 (expected 272)
    '^- \[~\] F\d{3} — '      = 1  (the at-most-one-claim invariant)

    $ git diff --name-only HEAD~1 HEAD   -> exit 0
    docs/roadmap/STATUS.md
    $ python3 -m pytest tests/docs/ -q -p no:randomly
    exit = 0 ; 303 passed in 0.66s
    $ python3 -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
    exit = 0 ; 30 passed in 0.36s

**G5 THE CODE**, at C4 6955a197.

    $ python3 -m ruff check packages/orchestration/pingpong_job.py
    exit = 0 ; All checks passed!

    SHIPPED dataclass, two constructed JobPlan() objects:
      a.run_refs = []   b.run_refs = []   both empty lists = True
      a.run_refs is b.run_refs = False  -> distinct list objects
    occurrences of the string 'run_refs' in the file = 7 (was 0 at b18fad57; >= 4 required)

    $ git diff --name-only HEAD~1 HEAD   -> exit 0
    packages/orchestration/pingpong_job.py

**G6 THE NEW TESTS**, at C5 c16ad23d.

    $ python3 -m pytest tests/orchestration/test_job_run_refs.py -q -p no:randomly
    exit = 0 ; 4 passed in 0.73s
    $ python3 -m pytest tests/test_do_job_flow.py -q -p no:randomly
    exit = 0 ; 178 passed in 28.02s
    $ python3 -m pytest tests/orchestration/test_job_budgets.py -q -p no:randomly
    exit = 0 ; 135 passed in 30.61s

**G7 THE RED PROOF**, inside the disposable worktree `.remedy-wt/f272-g7-wt`
created at c16ad23d; never in the primary checkout.

Shadow probe first, because an editable install of `remedy` points at the
primary checkout:

    $ python3 -B -c "import packages.orchestration.pingpong_job as m; print(m.__file__)"  (cwd=worktree)
    exit 0 ; /home/decodeux/Repos/remedy/.remedy-wt/f272-g7-wt/packages/orchestration/pingpong_job.py

so the worktree's own module is the one under test. `__pycache__` purge before
each run removed 0 directories, and every run used `python3 -B`.

(i) UNMUTATED CONTROL

    $ python3 -B -m pytest tests/orchestration/test_job_run_refs.py -q -p no:randomly
    exit = 0 ; 4 passed in 1.08s

(ii) THE MUTATION — the two lines C4(c) inserted were deleted; occurrences of
`job.run_refs.append` in that file went 1 → 0.

    $ python3 -B -m pytest tests/orchestration/test_job_run_refs.py -q -p no:randomly
    exit = 1 ; 1 failed, 3 passed in 1.11s
    FAILED tests/orchestration/test_job_run_refs.py::TestJobRunRefsEndToEnd::test_run_refs_names_every_task_run_in_order
    E  AssertionError: assert [] == ['c23c4080058...103b8ee94132']

The failing test is the C5 item 4 end-to-end test, as required.

(iii) WHAT WAS MUTATED

    $ git -C <worktree> diff --name-only   -> exit 0
    packages/orchestration/pingpong_job.py

Then `git worktree remove --force <worktree>` and `git worktree prune`;
`git worktree list` afterwards no longer contains `f272-g7-wt` (only the primary
checkout and twelve pre-existing, unrelated `remedy/job-*` worktrees).

**G8 THE CANARY, INTEGRITY AND THE TREE**, primary checkout, after C5 and before
C6 was staged.

    $ python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    exit = 0 ; 42 passed in 22.95s
    $ python3 -m apps.cli.grouped integrity check --json
    exit = 0 ; "passed" = True ; "fail_count" = 0
    $ git status --porcelain   -> exit 0 ; output '' (EMPTY)
    $ git ls-files .remedy-wt  -> exit 0 ; output '' (nothing tracked)

Per-commit insertions and single-parent readings for C0a..C5 are in the Commits
section above. Marker lines (prefix `<<<BEGIN` or `<<<END`) per changed file:

    .agent/plan.md                            0
    .agent/context.md                         0
    .agent/live_review.md                     0
    docs/roadmap/STATUS.md                    0
    packages/orchestration/pingpong_job.py    0
    tests/orchestration/test_job_run_refs.py  0

**Constraint 11 — the block's own size, re-measured on the committed
`.agent/authored/f272-r1.md`:**

    TOTAL lines            = 488  (budget 490, DECISION F085 D6)
    slice BODY lines       = 174
    PROSE = TOTAL - slices = 314  (cap 400, DECISION F105 D5)

Both figures agree with the block's own statement; no drift.

**`.agent/STOP` readings (constraint 10), read with `os.path.exists`:**

    before C0a : False
    before C4  : False
    before C6  : False

## Authored-text proofs

| Slice | Target | Result |
|-------|--------|--------|
| the whole block | .agent/authored/f272-r1.md, .agent/last_block.md | `filecmp.cmp(shallow=False)` True against the source for both; one sha256 229900f5…627e0165, 27393 bytes |
| PLANF272R1 | .agent/plan.md | equals slice + exactly one trailing newline (2097 bytes) |
| CONTEXTF272 | .agent/context.md | equals slice + exactly one trailing newline (3366 bytes) |
| HEAD1_FROM/TO | .agent/live_review.md | FROM 1→0, TO 0→1; independent reconstruction equals the committed image |
| STEPS_FROM/TO | .agent/live_review.md | FROM 1→0, TO 0→1; same reconstruction |
| STATUS_FROM/TO | docs/roadmap/STATUS.md | FROM 1→0, TO 0→1 |

Every slice was extracted by exact-position marker matching, asserting exactly
one BEGIN and one END line per name, and applied byte for byte. No slice was
edited.

## Deviations & assumptions

1. **G2(b) region-boundary convention — a reading difference, not an edit.**
   Taking "the bytes from and including the line `## Findings` to end of file"
   literally from the `#` character yields 953407 bytes hashing to
   `447b08c3…a45a`, one byte short of the block's stated 953408 /
   `147ce009…f8dc`. Including the newline that terminates the preceding line
   reproduces the block's figures exactly. BOTH readings are byte-identical
   before and after C2, so the carried region is unchanged under either
   convention; both are reported above. Nothing was changed to make either
   match.
2. **C0a and C0b precede the plan advance.** AGENTS.md requires `.agent/plan.md`
   to reflect the current state before every commit; at C0a and C0b it still
   named F260. This follows the block's ordered bundle, which names C1 the
   round's FIRST SUBSTANTIVE commit and puts the two transport commits ahead of
   it, and matches the standing pattern of this repository's rounds. Declared
   rather than silently reordered.
3. **No objection to any slice.** No slice was believed wrong; none was edited.
4. **No commit was added, dropped or reordered.** The committed sequence is
   exactly C0a, C0b, C1, C2, C3, C4, C5, C6, each single-parent.
5. **No finding was minted, resolved or renumbered** (constraint 4). The open
   set is 298 by distinct id before and after C2; R-0818 remains the next free
   id and this round did not spend it. No `Gate:` paragraph was appended: this
   round's verdict is written by the NEXT round's first commit.
6. **The change set was not widened.** `README.md`,
   `docs/roadmap/features/T2_F272.md` and `docs/roadmap/features/T2_F260.md`
   were not touched.
7. **Assumption, declared:** `git worktree list` still shows twelve pre-existing
   `remedy/job-*` worktrees under `.remedy-wt/`. They predate this round, were
   not created or removed by it, and were left alone.

## Next

The planner/reviewer re-runs G1–G8 against `b18fad57..HEAD` on
`feature/f272-one-world-completion` and issues the round 1 verdict; that verdict
is booked into `.agent/live_review.md` by the FIRST commit of round 2, which
then lands the run re-key — `run_log_dir` and `pingpong_run_dir` collapsing onto
the one `run_dir` keyed by RUN id — as the second half of T001.
