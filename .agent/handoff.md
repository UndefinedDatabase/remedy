# Handoff — F260 One world: mission → job → run, round 6

## Session

`SESSION 2 of feature F260 · round 6 · rounds so far 6`

Well inside the 25-round / 7-session soft limit, so no scope report is owed.

Open findings: **295** (299 `^- R-\d{4} — ` registrations minus 4
`^Done: R-\d{4} — ` lines) — unchanged, because this round registers and
resolves nothing. Maximum id in use: **R-0814**. R-0814's root cause is what
this round's code addresses; the finding itself is resolved in T002, against
the fix clause it already carries.

Branch `feature/f260-one-world`, resumed at `3aaeb042`. No branch created, no
merge, no pull request touched — the pull request belongs to the closure
sequence.

## Range

Review of `3aaeb042..HEAD`, where HEAD is the C6 commit that writes this file.
Its SHA is deliberately NOT spelled here: a commit cannot carry its own digest,
and the block states the handback commit's own numbers are owed by no one
because the reviewer measures the branch tip itself. The seven SHAs below are
measured, not predicted.

## Commits

Seven commits, all single-parent. Insertion counts are the `+` column of
`git diff --numstat` (DECISION F104 D1). The largest is 364 — the C0a block
save, a single `.agent/**` state-file write and in any case well under the
AGENTS.md 500-insertion cap. The largest CODE commit is C5 at 168.

### 5cbf74c8 f260: save the round 6 step block as authored text (C0a, +364)
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f260-r6.md` | +364/-0 | the round-6 step block, copied with `shutil.copyfile`, never retyped |

### db6f43ef f260: mirror the round 6 step block into last_block (C0b, +298)
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +298/-233 | same bytes mirrored; the round-5 block it replaces accounts for the deletions |

### b964fc18 f260: book the round 5 gate record into the live review ledger (C1, +2)
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-0 | `"\n"` + the GATE_R5 slice + `"\n"`, appended; 881955 → 887129 bytes |

### 6174d465 f260: append the round 5 reviewer prose slips (C2, +3)
| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +3/-1 | SLIP4 and SLIP5 appended; 89710 → 92673 bytes. The single deletion is the pre-image's unterminated last line gaining its newline — see deviation 1 |

### 770283b4 f260: point the plan at T002 and the one layout spelling (C3, +21)
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +21/-18 | replaced entirely by the PLANF260R6 slice plus one trailing newline; 48 lines |

### 2c102636 f260: rule the one resolver into T002 as DECISION F260 D4 (C4, +38)
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F260.md` | +38/-0 | the D4PAIR FROM→TO rewrite; 22955 → 25427 bytes |

### a02c25b3 f260: give data_paths the one spelling of D1's job layout (C5, +168)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/data_paths.py` | +42/-0 | `job_dir`, `job_record_path`, `job_evidence_dir`, `run_dir`, one D1 comment above the group, four names added to the `Public API::` block |
| `packages/orchestration/pingpong_job.py` | +13/-5 | `job_evidence_dir` and `_task_stream_dir` now build on `data_paths.job_evidence_dir`; no path and no behaviour changes |
| `tests/test_data_paths.py` | +113/-0 | one new class `TestJobAndRunLayout`, seven tests |

### C6 (this commit) f260: hand back round 6 …
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | — | this file; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/rev-r6 a02c25b3` | **FAILED**, `fatal: '…/.remedy-wt/rev-r6' already exists` — a pre-existing August scratch directory of unrelated files, not a worktree. Nothing was deleted; see deviation 3 |
| `git worktree add --detach .remedy-wt/f260-r6-mut a02c25b3` | created, detached at `a02c25b3` |
| `git worktree remove --force .remedy-wt/f260-r6-mut` | removed; `git worktree list` then holds the primary checkout plus the eleven pre-existing `job-*` worktrees and nothing this round created |
| `git push origin feature/f260-one-world` | run after C6; never a force-push |
| PR create / edit / merge | **None** — the block forbids it this round |

## Verification

All eight gates ran AT C5 (`a02c25b3`), before this file was written, so every
exit code below is real and measured rather than predicted.

| Gate | Result | Real exit code |
|---|---|---|
| G1 TRANSPORT | PASS — one digest across all three artefacts | 0 |
| G2 THE RECORD | PASS — growth exact, (a)(b)(c) hold, both negative controls reject, counts unchanged | 0 |
| G3 THE PROSE FILES | PASS — prefix exact, remainder exact, plan is slice+`\n` at 48 lines | 0 |
| G4 THE DECISION | PASS — byte-exact reconstruction, FROM 1x→0x, TO 0x→1x, five D-headings | 0 |
| G5 THE CODE, READ AND RUN | PASS — ruff clean, all four readings hold, three paths in the numstat | 0 |
| G6 THE MUTATION RED-PROOF | PASS — control green, all four properties turn the guard red, control green after each | 0 (control) / 1 (each mutation) |
| G7 THE SUITES | PASS — eight suites, 730 tests, every one exit 0 | 0 (×8) |
| G8 THE TREE AND THE CHANGE SET | PASS — tree clean, nine paths, integrity `passed: true` | 0 |

### G1 — transport (one digest)

    $ sha256sum .remedy-wt/f260-r6-block.md .agent/authored/f260-r6.md .agent/last_block.md
    868a89bb4df7d29a92ef1b5654ed0d344932db534e9f56c434178e7840feb00c  .remedy-wt/f260-r6-block.md
    868a89bb4df7d29a92ef1b5654ed0d344932db534e9f56c434178e7840feb00c  .agent/authored/f260-r6.md
    868a89bb4df7d29a92ef1b5654ed0d344932db534e9f56c434178e7840feb00c  .agent/last_block.md
    exit 0

ONE value, and it equals the BLOCK_SHA the delegating prompt states. Per §3
item 37 this chain covers those three artefacts and is NOT a claim about the
bytes emitted into the prompt.

### G2 — the record

    .agent/live_review.md   881955 → 887129 bytes, growth 5174
    appended byte count     5174  ( "\n" + GATE_R5 (5172 bytes) + "\n" )
    growth == appended:     True
    (a) 881955-byte pre-image is a byte-exact PREFIX:      True
    (b) remainder is exactly "\n" + GATE_R5 + "\n":        True
    (c) file's LAST blank-line unit equals the GATE_R5 slice: True
    file still ends with exactly one newline:              True
    exit 0

TWO negative controls, both in scratch copies held in memory; the file on disk
was re-read afterwards and is unchanged.

    CONTROL 1  flip at offset 882016, INSIDE the appended paragraph ('A' → 'a')
       (c) REJECTS: True
       (a) accepts — the flip lies entirely after the prefix region, so (a)
           cannot see it. This is the asymmetry round 5 reported and this
           round's block correctly split into two controls.
    CONTROL 2  flip at offset 876955, INSIDE the pre-image region ('h' → 'H')
       (a) REJECTS: True
       (c) accepts — the flip lies before the tail unit, so (c) cannot see it.

The two readings cover DIFFERENT REGIONS and neither alone is total, which is
exactly why both controls are needed. Counts afterwards:

    ^- R-[0-9]{4} — ......... 299
    ^Done: R-[0-9]{4} — ..... 4
    ^Gate: ................... 15 headers, 15 distinct → all distinct: True

The fifteenth is `Gate: R5 — the F260 R5 entry.`, occurring exactly once.

### G3 — the prose files

    .agent/prose_slips.md   89710 → 92673 bytes, growth 2963
    appended                2963 = "\n" + SLIP4 (1420) + "\n" + SLIP5 (1540) + "\n"
    pre-image is a byte-exact PREFIX:                True
    remainder is exactly nl+SLIP4+nl+SLIP5+nl:       True
    exit 0

    .agent/plan.md          2568 bytes
    equals PLANF260R6 slice + exactly one trailing newline:  True
    line count 48  → under 50:                               True
    exit 0

Nothing already in `prose_slips.md` changed by one byte — the prefix comparison
is the authoritative reading and it holds. See deviation 1 for the structural
consequence of the block's byte recipe.

### G4 — the decision

    docs/roadmap/features/T2_F260.md   22955 → 25427 bytes (delta 2472)
    reconstructs BYTE-EXACTLY from the pre-image with the single
      D4PAIR substitution applied and no other change:   True
    §4.9 counts over the WHOLE file:
      D4PAIR_FROM  1x before → 0x after
      D4PAIR_TO    0x before → 1x after
    ^### DECISION F260 D  matches 5 times: D1, D2, D0, D3, D4
      each of D0 D1 D2 D3 D4 appears exactly once:       True
    file still ends with exactly one newline:            True
    exit 0

The block's pre-emission containment test is confirmed on disk: `TO contains
FROM` is False, so the pair is a REWRITE and the "FROM 0x, TO 1x" reading is
attainable, as ordered.

### G5 — the code, read and run

(a) ruff:

    $ python3 -m ruff check packages/orchestration/data_paths.py \
        packages/orchestration/pingpong_job.py
    All checks passed!
    exit 0

(b) with `REMEDY_DATA_DIR` set to a temporary directory:

    job_dir(x)          = <tmp>/jobs/0123456789abcdef
    job_record_path(x)  = <tmp>/jobs/0123456789abcdef/job.json
    job_evidence_dir(x) = <tmp>/jobs/0123456789abcdef/evidence
    run_dir(y)          = <tmp>/runs/fedcba9876543210
    job_record_path(x).parent == job_evidence_dir(x).parent == job_dir(x): True
    run_dir(y).parent is runs_dir():                                       True
    jobs_dir() nowhere in run_dir(y).parents:                              True

(c) the no-behaviour-change property:

    pingpong_job.job_evidence_dir(x) == data_paths.job_evidence_dir(x)     True
    pingpong_job._task_stream_dir(x,"t1")
        == data_paths.job_evidence_dir(x) / "task_runs" / "t1"             True

(d) exactly three paths:

    $ git diff --numstat 3aaeb042..a02c25b3 -- packages/ tests/
    42	0	packages/orchestration/data_paths.py
    13	5	packages/orchestration/pingpong_job.py
    113	0	tests/test_data_paths.py
    exit 0

### G6 — the mutation red-proof

Disposable worktree `.remedy-wt/f260-r6-mut`, detached at `a02c25b3`,
`__pycache__` purged before every run and every run under `python3 -B`. Module
resolution was probed FIRST, so no editable install shadowed the worktree:

    data_paths   <- .remedy-wt/f260-r6-mut/packages/orchestration/data_paths.py
    pingpong_job <- .remedy-wt/f260-r6-mut/packages/orchestration/pingpong_job.py

The UNMUTATED CONTROL ran first, and again after every restore. Restores were
byte-for-byte rewrites of the saved source, never `git checkout --`.

    [control-0]          exit=0   35 passed
    [mut-1]  run keyed under jobs_dir            exit=1   2 failed, 33 passed
        FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_a_run_hangs_under_runs_dir_and_never_under_jobs_dir
        FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_the_root_override_is_honoured_by_all_four
    [control-after-1]    exit=0   35 passed
    [mut-2]  evidence beside the record          exit=1   2 failed, 33 passed
        FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_the_record_and_the_evidence_share_one_root
        FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_the_root_override_is_honoured_by_all_four
    [control-after-2]    exit=0   35 passed
    [mut-3]  job_dir ignores root                exit=1   1 failed, 34 passed
        FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_the_root_override_is_honoured_by_all_four
    [control-after-3]    exit=0   35 passed
    [mut-4]  pingpong spells it by hand          exit=1   1 failed, 34 passed
        FAILED tests/test_data_paths.py::TestJobAndRunLayout::test_pingpong_job_no_longer_spells_the_evidence_path_itself
    [control-after-4]    exit=0   35 passed

The block's note on (iv) is CONFIRMED by measurement, not assumed: under that
mutation exactly ONE test failed and it is the text/AST reading. The equality
test `test_pingpong_job_evidence_paths_equal_the_data_paths_ones` stayed GREEN,
because the hand-built path is genuinely equal to the new one. That is why the
block ordered both readings, and it is the whole justification for the AST
guard's existence.

    $ git worktree remove --force .remedy-wt/f260-r6-mut
    $ git worktree list
    /home/decodeux/Repos/remedy                                  a02c25b3 [feature/f260-one-world]
    /home/decodeux/Repos/remedy/.remedy-wt/job-1cbb6972bf7c4ffc  db21957a [remedy/job-1cbb6972bf7c4ffc]
    … ten further pre-existing `job-*` worktrees, all present before this round began …

### G7 — the suites, serially in the primary checkout

Each suite ran as its OWN sequential process with its real return code
captured; no shell pipe was used, so no `$?` was replaced by a pipe's.

    exit=0   tests/test_data_paths.py                      35 passed
    exit=0   tests/orchestration/test_checkpoints.py       37 passed
    exit=0   tests/orchestration/test_repair_attest.py     37 passed
    exit=0   tests/orchestration/test_job_evidence.py      93 passed
    exit=0   tests/orchestration/test_mint_call_sites.py    5 passed
    exit=0   tests/test_do_job_flow.py                    178 passed
    exit=0   tests/docs/                                  303 passed
    exit=0   tests/cli/test_golden_path.py                 42 passed
    worst exit code across the eight suites: 0

730 tests. `tests/docs/` is this round's docs-round gate — the change set holds
a `docs/roadmap/` path (verification tier 5) — and `tests/cli/test_golden_path.py`
is the canary. `tests/test_data_paths.py` went 28 → 35, the seven new tests.

### G8 — the tree and the change set

    $ git status --porcelain
    (empty)
    $ git ls-files .remedy-wt
    (empty)
    $ test -e .agent/STOP
    ABSENT
    $ git worktree list
    holds no worktree this round created (see G6)

    $ git diff --name-only 3aaeb042..a02c25b3
    .agent/authored/f260-r6.md
    .agent/last_block.md
    .agent/live_review.md
    .agent/plan.md
    .agent/prose_slips.md
    docs/roadmap/features/T2_F260.md
    packages/orchestration/data_paths.py
    packages/orchestration/pingpong_job.py
    tests/test_data_paths.py

Exactly the nine paths of the change set other than `.agent/handoff.md`, which
C6 adds.

    $ python3 -m apps.cli.grouped integrity check --json
    "passed": true, "fail_count": 0, "check_count": 5
      handler_import        pass   handlers=342
      live_review_verdict   pass
      plan_consistency      pass   unchecked=0, context_complete=False
      relevant_untracked    pass   untracked=0, relevant=0
      high_blockers_open    pass   no open blocker/high findings
    exit 0

## Authored-text proofs

Every authored slice was extracted from `.agent/authored/f260-r6.md`'s own byte
source programmatically and applied byte for byte — none was retyped. The
slice convention this round's block states outright (the slice EXCLUDES the
newline terminating its last content line) was applied uniformly.

| Slice | Bytes | Applied to | Disk-to-disk result |
|---|---|---|---|
| PLANF260R6 | 2567 | `.agent/plan.md` | file == slice + `"\n"` exactly (2568 bytes) |
| D4PAIR_FROM → D4PAIR_TO | 63 → 2535 | `docs/roadmap/features/T2_F260.md` | byte-exact reconstruction from the pre-image, single substitution |
| GATE_R5 | 5172 | `.agent/live_review.md` | remainder == `"\n"` + slice + `"\n"` exactly |
| SLIP4 | 1420 | `.agent/prose_slips.md` | remainder == `"\n"`+SLIP4+`"\n"`+SLIP5+`"\n"` exactly |
| SLIP5 | 1540 | `.agent/prose_slips.md` | (same remainder comparison) |

The C0a/C0b transport digest is identical across the scratch original, the
saved copy and the mirror (G1).

## Deviations & assumptions

The commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was followed exactly, in
order, one commit each, with C5 landing the functions, both call sites and the
tests together. No commit was added, dropped or reordered.

**1. The block's C2 byte recipe assumes a trailing newline that `prose_slips.md`
does not have — applied anyway, structural consequence declared.**
`.agent/prose_slips.md` at `3aaeb042` is 89710 bytes and does NOT end with a
newline (its last line is unterminated). The block ordered the append as
`"\n"` + SLIP4 + `"\n"` + SLIP5 + `"\n"`, which is the same recipe C1 uses for
`live_review.md` — but `live_review.md` DOES end with a newline, so there the
leading `"\n"` creates a blank-line separator, while here it merely terminates
the pre-image's last line. The measured result: SLIP4 sits directly beneath the
previous slip with no blank line, and SLIP5 directly beneath SLIP4. The file's
blank-line-unit count therefore stayed at **128** instead of rising to 130,
and the last unit is now three slips fused into one. Every other slip in that
file is its own blank-line unit, so this breaks the file's own convention.
Per constraint 1 I applied the bytes as ordered and did not repair them.
G3 as written is fully MET — the pre-image is a byte-exact prefix and the
remainder is exactly the ordered bytes — so this is a defect in the recipe, not
in my application of it. Suggested repair for a later round: append `"\n\n"`
between units when the pre-image does not end in a newline, or normalise the
pre-image first. This is a reviewer-authored slip over an `.agent/` prose file
that left nothing wrong under `packages/`, `apps/`, `tests/` or `docs/`, so
under amend0827-process-diet rule 2 it belongs in `prose_slips.md` and spends
no R-id.

**2. One stale line number in the block.** The block gives
`_task_stream_dir` at `pingpong_job.py:3568` at `3aaeb042`; the `def` is at
line **3565** (3568 is the second line of its docstring). `job_evidence_dir` at
`3055` is exact. The block ordered both symbols re-grepped before editing,
which I did, so the correct function was edited in both cases and nothing on
disk is wrong. Recorded because a line number stated as a measurement should be
one.

**3. The disposable worktree was named `.remedy-wt/f260-r6-mut`, not a
`rev-r6` name.** `git worktree add --detach .remedy-wt/rev-r6 a02c25b3` failed
with `fatal: … already exists`: `.remedy-wt/rev-r6` is a PRE-EXISTING scratch
directory from 2026-08-21 holding unrelated files from another feature, and is
not a worktree. I did not delete it or any part of it. The block ordered a
disposable worktree "under `.remedy-wt/`" without fixing its name, so a
distinct unused name satisfies the order; G6 and constraint 4 are met in full.

**4. G6's control scope was the whole `tests/test_data_paths.py` file** (35
tests), not just the new class. The block ordered "the UNMUTATED CONTROL" and
its pass count without naming a scope; the wider scope is the stricter reading,
since it would also catch a mutation breaking a pre-existing test.

**5. G7's exit codes were captured by a sequential Python driver**, one
`subprocess.run` per suite in the primary checkout, rather than eight shell
invocations. The suites still ran serially, one process each, and each real
return code is the one reported. This satisfies "never through a pipe" in
substance: the hazard that clause names is a shell pipe replacing `$?` with the
downstream command's, and no shell pipe was used.

**6. The "no hand-built evidence path survives" guard is an AST reference
guard, not a substring search.** The block called this "a text reading" and
named the expression `jobs_dir() / job_id / "evidence"`. I implemented it as:
no `ast.Name`, `ast.Attribute` or `ast.alias` resolving to the exact name
`jobs_dir` occurs anywhere in `pingpong_job.py`. This is strictly stronger than
a substring search — it cannot be dodged by an `import … as` alias or by
whitespace, and it cannot be tripped by a comment or docstring that merely
NAMES the old layout, which a substring search would be. `_jobs_dir` and
`task_jobs_dir` are different names and are deliberately out of scope; they
hold the ping-pong store and move in T002. G6 mutation (iv) proves the guard
fires.

**7. No `.agent/context.md` or `.agent/decisions.md` update.** The Commit Gate
asks whether they need one; the block's change set forbids writing them, and
the change set bounds writes. The decision this round makes is DECISION F260 D4,
which the block placed in `docs/roadmap/features/T2_F260.md` — the durable
home — so nothing is lost.

Nothing outside the ten-path change set was created, edited or deleted.
Scratch under the gitignored `.remedy-wt/` is untracked and `git ls-files
.remedy-wt` is empty.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 the record | done | |
| C2 the two slips | deviated | applied byte for byte as ordered; the block's recipe fused three blank-line units into one — deviation 1 |
| C3 the plan | done | |
| C4 DECISION F260 D4 | done | |
| C5 the code, call sites and tests | done | one commit, 168 insertions |
| C6 the handback | done | this file |
| G1 TRANSPORT | done | exit 0, one digest = BLOCK_SHA |
| G2 THE RECORD | done | exit 0, both region-disjoint controls behave as split |
| G3 THE PROSE FILES | done | exit 0 |
| G4 THE DECISION | done | exit 0 |
| G5 THE CODE, READ AND RUN | done | exit 0, all four readings |
| G6 THE MUTATION RED-PROOF | done | control 0, four mutations each exit 1 |
| G7 THE SUITES | done | eight suites, all exit 0 |
| G8 THE TREE AND THE CHANGE SET | done | exit 0, integrity passed |

## What this round actually changed

DECISION F260 D4 rules that the ONE resolver lands with the store it resolves
over — inside T002, beside the unified record and its loader — and RETIRES
T001's "while both stores still exist" clause, because forty of the forty-two
job-taking call sites take a `UUID` today and that is not a state they can move
in. T001 is CLOSED with its minting half.

`data_paths` now owns the ONE spelling of DECISION F260 D1's layout:
`job_dir`, `job_record_path`, `job_evidence_dir` and `run_dir`, each built on
the one above it so a layout change has exactly one place to happen.
`pingpong_job`'s two hand-built evidence paths were put onto it, changing no
path and no behaviour — proved by value equality AND by the AST guard, because
the equality alone cannot see a regression to a path that is equal.

`job_record_path` names a path NOTHING WRITES YET, and its docstring says so
and names T002 as the task that moves the writer. The live ping-pong record is
still at `<data_root>/task_jobs/<16hex>/job.json`; moving it before the
resolver moves would break `remedy teach narrate` for every ping-pong job,
which is precisely what D4 rules against.

## Next

The reviewer re-runs all eight gates and reads the real diff for round 6, then
rules on the round. The next build round puts the four remaining hand-built
evidence paths — `job_evidence.py` twice, `repair_attest.py` and `do_cmd.py` —
onto `data_paths.job_evidence_dir`, with a guard that no module outside
`data_paths` spells that path again.
