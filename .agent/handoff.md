# Handoff — F272 One world completion

## Session

`SESSION 10 of feature F272 · round 20 · rounds so far 20`

Soft limit under amend0906-triage-throughput is 12 sessions and 40 rounds; at
session 10 and round 20 the feature is inside it and no scope report is owed.

Context self-assessment: context is comfortable — this round read the catalog,
five one-line repair sites and one prior test for idiom, and ran the full suite
once; nothing was dropped or re-read for want of room.

## Range

Review of `8bcdc4dc`..HEAD, where HEAD is the C6 commit that writes this file.
Seven commits precede it — C0a, C0b, C1, C2, C3, C4, C5, in exactly that order,
every one single-parent, with no reordering and no extra or dropped commit.

## Commits

### 7f759a64 f272: save the round 20 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r20.md` | +463/-0 | C0a — the step block saved verbatim by `shutil.copyfile` |

### 7c55af84 f272: mirror the round 20 block into the last block slot
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +438/-154 | C0b — the same bytes mirrored by `shutil.copyfile` |

### 328cddfd f272: point the plan at the stale advertisement repair
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +22/-20 | C1 — replaced byte-for-byte with the PLANF272R20 slice |

### 652a29f3 f272: book the round 19 PASS verdict and register the stale advertisement finding
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4/-0 | C2 — RECORDR20 appended as `pre + NL + slice`; the R19 gate entry and R-0823 |

### d16c7285 f272: append the round 19 prose slips
| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +6/-0 | C3 — SLIPSR20 appended as `pre + NL + slice`, three slips |

### a333617b f272: repair the stale command advertisements and guard the class
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_advertised_commands.py` | +110/-0 | C4 — the new guard test, written to GUARDSPEC (S1–S5) |
| `apps/cli/commands/decision.py` | +1/-1 | C4 — P1, `remedy job run-loop` → `remedy job run` |
| `apps/cli/commands/job.py` | +1/-1 | C4 — P2, `_cmd_job_status`'s `next_action` |
| `packages/orchestration/autonomy_readiness.py` | +1/-1 | C4 — P3, level-4 hint → `remedy dev agent-loop` |
| `packages/orchestration/model_route_tournament.py` | +1/-1 | C4 — P4, `remedy guide next` → `guide job` / `job list` |
| `packages/orchestration/worker_registry.py` | +1/-1 | C4 — P5, same replacement |

### 79b45aa3 f272: rule that a command advertisement dies with its command
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F272.md` | +74/-0 | C5 — DECISION F272 D13 appended as `pre + NL + slice` |

### C6 — this commit
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C6 — a handoff cannot table the commit that writes it (R-0149 pattern) |

Every `+/-` cell above is taken from `git diff --numstat <parent> <commit>` and
matches the G8 per-commit figures cell for cell.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `shutil.copyfile` to `.agent/authored/f272-r20.md`, digest verified |
| C0b | done | `shutil.copyfile` of the same bytes to `.agent/last_block.md` |
| C1 | done | `.agent/plan.md` byte-equal to PLANF272R20 |
| C2 | done | RECORDR20 appended; all six counts match the block |
| C3 | done | SLIPSR20 appended |
| C4 | done | guard test + P1–P5 in ONE commit |
| C5 | done | DECISION F272 D13 appended to the feature file |
| C6 | done | this file |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r20-g4 a333617b` | exit 0 — the G4 disposable worktree |
| `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r20-g4` | exit 0 — removed BY EXACT PATH; 13 entries remain, the primary plus the twelve pre-existing `remedy/job-*` |
| `git push -u origin feature/f272-one-world-completion` | run after this commit; see the push line below |

No PR was created, no merge, no force-push, no `gh` command.

## Verification — one line per gate

| Gate | Real exit | Reading |
|---|---|---|
| G1 TRANSPORT | 0 | all three artefacts 32027 bytes, 463 lines, sha256 `9a48d5ad…9a83f` |
| G2 THE RECORD | 0 | byte, structural, negative control and all six counts as the block predicted |
| G3 THE PROSE FILES | 0 | plan 2213 bytes / 45 lines ≤ 50; slips 146054 → 147269 |
| G4 THE GUARD IS REAL | 0 / 1 / 0 | control green, one-line revert red naming ONE path, restore green |
| G5 SWEEP ZERO, SCAN NOT BLIND | 0 | 4 passed; 738 advertisements seen; 0 unresolved |
| G6 THE FULL SUITE | 0 | 19784 passed, 23 skipped, 0 `^FAILED` |
| G7 RUFF + DOCS + CANARY | 0 / 0 / 0 | `All checks passed!`; 303 passed; 42 passed |
| G8 THE TREE | 0 | clean at every boundary; `.remedy-wt` untracked; max insertions 463 < 500 |

## Verification — transcripts

### G1 TRANSPORT

    .remedy-wt/f272-r20-block.md    bytes=32027 lines=463 sha256=9a48d5ad812eaa278d703be4c29fd416a168d25f3f5e0fc50b3d79d323a9f83f
    .agent/authored/f272-r20.md     bytes=32027 lines=463 sha256=9a48d5ad812eaa278d703be4c29fd416a168d25f3f5e0fc50b3d79d323a9f83f
    .agent/last_block.md            bytes=32027 lines=463 sha256=9a48d5ad812eaa278d703be4c29fd416a168d25f3f5e0fc50b3d79d323a9f83f
    REAL_EXIT=0

The delivered digest was verified against disk BEFORE the block was trusted.

### G2 THE RECORD

    SLICE RECORDR20 bytes=6309 lines=3 sha256=4092dfc7e3b02fc6a0e7fe50a39a5004a57f7713a2863b1e9ded977b89cbcf7a
    G2a pre_len=1173866
    G2a pre_sha256=8363661be8b7dbb9ebc0982b1e60fffab1cefbedb70c6a603a3a299d332b3236
    G2a pre_terminal_12=b'obe output.\n'      pre_trailing_newline_run=1
    G2a post_len=1180176
    G2a post_sha256=a8a4a67b628e6cf2ec9dda440965beaab39a8b0fd099422d6b0a661804c73b3c
    G2a post_terminal_12=b'satisfy it.\n'     post_trailing_newline_run=1
    G2a PRE_IS_BYTE_EXACT_PREFIX_OF_POST: True
    G2a POST_EQUALS_PRE_NL_SLICE: True
    G2b N_COUNTED_FROM_SLICE=2   units_before=719 units_after=721
    G2b LAST_N_EQUAL_SLICE_PARAS_IN_ORDER: True
    G2b EVERYTHING_BEFORE_UNCHANGED: True
    G2c flipped_byte_offset=1173907 in_first_appended_paragraph=True
    G2c BYTE_READER_REJECTS: True
    G2c STRUCTURAL_READER_REJECTS: True
    G2c DISK_UNTOUCHED_BY_CONTROL: True True
    REAL_EXIT=0

The block's pre-image prediction was met exactly: 1173866 bytes, that sha256,
terminal twelve bytes `b'obe output.\n'`, trailing-newline run 1.

G2(d), each figure measured and none adjusted to agree:

    reg_distinct         306 -> 307   block_said 306 -> 307   AGREES=True
    done_distinct        249 -> 249   block_said 249 -> 249   AGREES=True
    open_by_distinct_id   57 -> 58    block_said  57 -> 58    AGREES=True
    gate_lines            42 -> 43    block_said  42 -> 43    AGREES=True
    gate_f272_r19          0 -> 1     block_said   0 -> 1     AGREES=True
    r0823                  0 -> 1     block_said   0 -> 1     AGREES=True

OPEN FINDINGS BY DISTINCT ID, with its arithmetic: pre `306 − 249 = 57`;
post `307 − 249 = 58`. Ids minted this round: `['R-0823']` — exactly one, as
the block said. New `Done:` ids: none.

### G3 THE PROSE FILES

    PRE  bytes=2179 lines=43 sha256=1a0bf72c…
    SLICE PLANF272R20 bytes=2213 lines=45 sha256=1ad5f4cc…
    POST bytes=2213 lines=45 sha256=1ad5f4cc…
    G3 PLAN_BYTE_EQUAL_TO_SLICE: True
    G3 PLAN_LINE_COUNT: 45 CAP: 50 UNDER_CAP: True
    G3 HAS_GOAL_HEADING: True
    G3 HAS_NEXT_STEPS_HEADING: True

    SLICE SLIPSR20 bytes=1214 lines=5 sha256=ef25d8db…
    G3 slips pre_len=146054  post_len=147269
    G3 slips POST_EQUALS_PRE_NL_SLICE: True
    G3 slips PRE_IS_BYTE_EXACT_PREFIX_OF_POST: True
    G3 slips block_said_base_pre_len=146054 AGREES=True
    REAL_EXIT=0

### G4 THE GUARD IS REAL — ordered colour, CONTROL FIRST

Worktree path `/home/decodeux/Repos/remedy/.remedy-wt/r20-g4`, detached at
`a333617b` (C4). `__pycache__` purge under it removed 0 directories (a fresh
worktree carries none). Resolution confirmed INSIDE the worktree before any
colour was trusted — no editable install shadowed it:

    catalog __file__ = /home/decodeux/Repos/remedy/.remedy-wt/r20-g4/apps/cli/command_catalog.py
    INSIDE_WORKTREE = True
    test REPO_ROOT  = /home/decodeux/Repos/remedy/.remedy-wt/r20-g4

(i) control — `python3 -B -m pytest tests/cli/test_advertised_commands.py -q -p no:randomly`

    4 passed in 0.28s
    REAL_EXIT=0

(ii) revert of EXACTLY ONE line, in
`/home/decodeux/Repos/remedy/.remedy-wt/r20-g4/packages/orchestration/autonomy_readiness.py`:

    replacing b'        _check("agent_loop", "remedy dev agent-loop <job_id>")\n'
    with      b'        _check("agent_loop", "remedy job run-loop <job_id>")\n'
    OCCURRENCES_OF_SOURCE_BEFORE_WRITE=1 (must be 1)
    AFTER: source=0 dest=1

(iii) the same command is now red, and the FULL unresolved list the assertion
printed is one entry naming that file AND NO OTHER PATH:

    E  AssertionError: production code advertises commands the catalog does not carry —
    E  delete a command's advertisements in the same commit as the command:
    E    packages/orchestration/autonomy_readiness.py:315: remedy job run-loop
    1 failed, 3 passed in 0.28s
    REAL_EXIT=1

(iv) restore, re-run:

    4 passed in 0.30s
    REAL_EXIT=0

`git status --porcelain` inside the worktree was EMPTY after the restore, so the
restore was byte-exact. Removal command, BY EXACT PATH:
`git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r20-g4` — exit 0.

### G5 THE SWEEP IS ZERO AND THE SCAN IS NOT BLIND

Primary checkout at C4:

    4 passed in 0.33s
    REAL_EXIT=0

The advertisement figure, printed from the SHIPPED functions rather than
asserted from the block:

    G5 shipped module REPO_ROOT      = /home/decodeux/Repos/remedy
    G5 tracked production .py files  = 367
    G5 ADVERTISEMENTS THE SCAN SAW   = 738
    G5 UNRESOLVED ADVERTISEMENTS     = 0 []

738 is unchanged from the base reading, as it must be: P1–P3 replace one
advertisement with one, and P4/P5 each carry two before and two after.

### G6 THE FULL SUITE — primary checkout

    python3 -B -m pytest -n auto -q -p no:randomly
    19784 passed, 23 skipped, 1 warning in 136.76s (0:02:16)
    REAL_EXIT=0
    grep -c '^FAILED' -> 0

RECONCILIATION, and it closes exactly: the reviewer measured the base at
`8bcdc4dc` as 19780 passed; an `ast` count of the new file gives four test
functions —

    TEST_FUNCTIONS= 4 ['test_every_advertised_command_exists_in_the_catalog',
    'test_scanner_reports_a_command_the_catalog_does_not_carry',
    'test_scanner_ignores_prose_that_merely_starts_with_a_group_name',
    'test_scanner_finds_a_real_next_action_f_string']

— and 19780 + 4 = 19784, the figure measured. Nothing was changed to make it
agree. Skips are 23, unchanged.

### G7 RUFF AND THE DOCS GATE

    python3 -m ruff check <the five edited .py files> tests/cli/test_advertised_commands.py
    All checks passed!
    REAL_EXIT=0

    python3 -B -m pytest tests/docs/ -q -p no:randomly
    303 passed in 0.49s
    REAL_EXIT=0

    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    42 passed in 20.98s
    REAL_EXIT=0

### G8 THE TREE

`git status --porcelain` was EMPTY and printed empty at every one of the seven
commit boundaries C0a…C5 and at the final boundary; `git ls-files .remedy-wt`
is EMPTY. Per-commit insertions from `git diff --numstat <parent> <commit>`,
C6 excluded:

    C0a  7f759a64  insertions=463  deletions=0    UNDER_500=True
    C0b  7c55af84  insertions=438  deletions=154  UNDER_500=True
    C1   328cddfd  insertions=22   deletions=20   UNDER_500=True
    C2   652a29f3  insertions=4    deletions=0    UNDER_500=True
    C3   d16c7285  insertions=6    deletions=0    UNDER_500=True
    C4   a333617b  insertions=115  deletions=5    UNDER_500=True
    C5   79b45aa3  insertions=74   deletions=0    UNDER_500=True

The three `.agent/STOP` readings by `os.path.exists`, all False:
before C0a `False`, before C4 `False`, before C6 `False`.

Feature file `docs/roadmap/features/T2_F272.md` across C5:
47484 bytes / 662 lines → 52485 bytes / 736 lines. DECISION headings D1 through
D13 each occur exactly once; D13 is new and unique.

## Authored-text proofs

Every applied slice was extracted PROGRAMMATICALLY from the committed
`.agent/authored/f272-r20.md` between its `<<<BEGIN NAME>>>` and `<<<END NAME>>>`
lines by one shared extractor, inclusive of the newline ending the last content
line. Nothing was retyped.

| Slice | Bytes | sha256 | Disk-to-disk result |
|---|---|---|---|
| PLANF272R20 | 2213 | `1ad5f4cc…` | `.agent/plan.md` byte-EQUAL to the slice |
| RECORDR20 | 6309 | `4092dfc7…` | `post == pre + NL + slice` TRUE |
| SLIPSR20 | 1214 | `ef25d8db…` | `post == pre + NL + slice` TRUE |
| DECISIONR20 | 5000 | `6695df96…` | `post == pre + NL + slice` TRUE |
| P1…P5 FROM/TO | — | — | each FROM 1x→0x and TO 0x→1x in its file |

C4's production test is the one artefact NOT sliced: GUARDSPEC describes it, and
it was written in this repository's idiom per constraint 5.

## Deviations & assumptions

**No deviation from the block's ordered commit sequence.** The eight commits are
C0a, C0b, C1, C2, C3, C4, C5, C6 in exactly that order; no commit was added,
dropped, split or reordered. The change set is exactly the thirteen declared
paths and nothing else — no measurement forced a path outside the list, so the
escape clause the block offers was not used.

1. **Assumption — the scanner's "followed by" test admits an intervening
   space.** GUARDSPEC S1 requires the pair to be "followed by" a placeholder,
   an option, a quote or end of string. Read literally as the very next
   character, `remedy job run <job_id>` would fail to match, because a space
   separates `run` from `<`. I implemented it as: skip spaces, then require
   `<`, `{`, `--`, `"` or `'`, or end of string. This reading is what reproduces
   the reviewer's own numbers — 738 advertisements and exactly the seven
   occurrences at the five listed sites, with all three prose probes rejected —
   so I take it as the intended one. Recorded because it is a genuine
   interpretation of the spec, not a transcription.

2. **Assumption — the scan is line-based.** S2 requires the failure message to
   name `path:line:`, so the module scans each file line by line and hands one
   line at a time to the scanner. "The end of the string" therefore means the
   end of a line. All four S4 discriminators are single strings and are
   unaffected.

3. **Assumption — G5's advertisement figure is reported from the shipped
   functions.** G5 asks for the passed count and, "separately", the number the
   scan saw, printed rather than asserted. Rather than add a bare `print` to a
   shipped test, the count is produced by importing the shipped
   `collect_command_advertisements` and printing its return value. The figure is
   therefore the shipped code's own, not a re-implementation.

4. **Note — the guard's own docstring contains the strings it forbids.** The new
   test file spells out `remedy job run-loop` and `remedy guide next` in its
   module docstring to explain the class. This is safe by construction and not
   by luck: S2 scopes the sweep to tracked `.py` under `packages/` and `apps/`,
   and the file lives under `tests/`. Flagged so a future round that widens the
   sweep to `tests/` knows this file will trip it.

5. **Note — `grep -c '^FAILED'` exits 1, and that is grep's semantics, not a
   suite failure.** The count is 0 and grep exits non-zero when it matches
   nothing. The suite's own real exit code is 0.

6. **Verification beyond the block, none of it contradicting it.** I re-ran the
   two premises the block asserts rather than accepting them: the shipped
   `_has_agent_loop([{"event": "agent_loop_inspected"}])` is `True` and
   `_has_agent_loop([])` is `False`, so P3's new hint is satisfiable and the
   predicate is not vacuous; and `('dev','agent-loop')`, `('guide','job')`,
   `('job','list')` and `('job','run')` are all real catalog pairs, so no repair
   introduced a second stale advertisement. I also checked D13's load-bearing
   measurements: `remedy job run-next` occurs 16 times across exactly the eight
   named modules, twice in `scripts/remedy_smoke.sh`, six test `.py` files carry
   the spaced form `job run-next`, both `tests/cli/test_plan_approval.py`
   shell-outs are at lines 372 and 716, and `job.run` is the catalog's only
   `is_expensive` command. Every one of these confirms the block. **No
   disagreement with the block was found anywhere in this round.**

7. **Note — RED at base was additionally observed in the primary checkout**
   before P1–P5 were applied, as a sanity check on the guard: 1 failed, 3
   passed, the failure naming exactly the seven occurrences at the five sites
   and nothing else, matching GUARDSPEC's own measurement. G4 remains the
   binding destructive proof and ran in the disposable worktree as ordered.

## Next

Delete the `job.run-next` command surface per DECISION F272 D13 — its catalog
entry, its handler entry and its test pin, TOGETHER WITH the sixteen
advertisements across the eight `packages/orchestration/` modules, the two in
`scripts/remedy_smoke.sh`, the six test files carrying the spaced form, and the
two `tests/cli/test_plan_approval.py` shell-outs, all in the same commit, with
`tests/cli/test_advertised_commands.py` now standing as the gate that proves no
advertisement was left behind.
