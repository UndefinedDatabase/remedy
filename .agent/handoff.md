# Handback — F275 round 31

## Session

SESSION 15 of feature F275 · round 31 · rounds so far 31

Context self-assessment (amend0905-throughput): the worker's context is comfortable,
though this round is the most expensive one F275 has run — three full serial suites of
about 21 minutes each, one of them discarded as a pilot — and the reading budget went
almost entirely into instrument output rather than prose. F275's soft limit is 20
sessions and 60 rounds by amend0908-f275-finish, so at session 15 and round 31 the limit
is not in sight and no scope report is owed.

## Range

Review of `0b009325`..`HEAD`.

## Commits

### 817ba547 F275 R31 C0a: save the round 31 step block verbatim as the authored text of record for T002.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r31.md` | +381 / -0 | the round 31 block saved byte-verbatim by `shutil.copyfile`, 33235 bytes |

### 184f1edc F275 R31 C0b: mirror the committed round 31 block into the last-block carrier.
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +326 / -365 | the COMMITTED C0a blob `3deba3d5` written out with `git cat-file blob`, never a retype |

### a53343c8 F275 R31 C1: point the plan at round 31 and T002.
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17 / -19 | whole-file replacement by the PLAN31 slice |

### 293b54d3 F275 R31 C2: book the round 30 PASS verdict and append the round 29 to 31 prose slips.
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | RECORD31 appended: the round 30 PASS verdict |
| `.agent/prose_slips.md` | +6 / -0 | SLIPS31 appended: the R29, R30 and R31 lines (the two R27 drafts were already on disk, per block constraint 10) |

### 123554a5 F275 R31 C3: measure the T002 flip site set with a descriptor probe and an ast sweep, and record the inventory.
| Path | +/- | Reason |
|---|---|---|
| `.agent/f275_t002_flip_inventory.md` | +498 / -0 | the generated inventory: both instrument sources, both run summaries, the reproducibility comparison, the route-B and alternative-route tables, the two set differences with the 11 unexecuted sites enumerated in full, and the construction/import/annotation counts |

### 0ce086ae F275 R31 C4: record DECISION F275 D17, the T002 ruling on the flip route and its one declared-oversize commit.
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +16 / -0 | DECISION31 appended |

### C5 — this handback (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | the round 31 handback; a handoff cannot table the commit that writes it |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r31wt 0b009325` | created, detached HEAD at `0b009325` |
| `ln -s` (via a python script) of `node_modules` into the worktree root | created; without it `TestVitestFrontendTestFoundation::test_vitest_passes` fails on an unresolvable `vitest/config` — a known worktree condition, not a probe effect |
| `git worktree remove --force .remedy-wt/r31wt` | removed |
| `git worktree prune` | pruned; `git worktree list` reads exactly ONE entry |
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C5 |

No PR was created; this round is not a closure sequence. No `gh` command was run.

## Verification

ONE LINE PER GATE, real exit codes and real numbers. Every gate was run as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`.

- **G1 TRANSPORT (at C0b) — PASS, REAL_EXIT=0.** Scratch `.remedy-wt/f275-r31-block.md`,
  committed `.agent/authored/f275-r31.md` and committed `.agent/last_block.md` are all
  33235 bytes at `cbd927e5268daac8557291e99fc6b50dd99ece78adf448e6bb133036f8b2bf19`;
  `ALL THREE EQUAL: True`.
- **G2 THE PLAN (at C1) — PASS, REAL_EXIT=0.** Committed `.agent/plan.md` and the PLAN31
  slice are both 1918 bytes at `4d6578b0e38c2924dc878bdb92a1a7d6ebaceb6ee6209b0675aac6e4c3a8581d`,
  `written == slice: True`; 37 lines against the cap of 50; `^## Goal$` = 1 and
  `^## Next Steps$` = 1.
- **G3 THE RECORD, three append targets — PASS, REAL_EXIT=0.** Pre-sizes read 790277,
  215418 and 1017073, each `same` as the block. `.agent/live_review.md` 790277→793191,
  `.agent/prose_slips.md` 215418→217298, `.agent/decisions.md` 1017073→1024587; every
  post-blob equals pre + ONE newline + slice, and the joining byte READ BACK at
  offset len(pre) is `b'\n'` in all three. The independent structural reader counted
  N from each slice — 1, 3 and 8 paragraphs — and matched the last N blank-line units
  IN ORDER. Three negative controls, each flipping one byte INSIDE THE FIRST appended
  paragraph, were REJECTED by BOTH readers. `^Gate: F275 R30 ` = 1 and
  `^## DECISION F275 D17 ` = 1.
- **G4 THE OPEN SET (at C4) — PASS, REAL_EXIT=0.** BY DISTINCT ID the ledger reads 87
  open at the base `0b009325` and 87 at HEAD, over 102 distinct registered ids against
  15 distinct resolved ids; ids registered this round `[]`, resolved this round `[]`.
  Beside it, `scripts/rotate_live_review.py` prints `open findings before: 85` and that
  reading is reproduced mechanically: 102 registration LINES minus 17 `Done:` LINES = 85,
  the two extra `Done:` lines being the second records `R-0721` and `R-0725` each carry.
  The block's third cause — `R-0831`'s second registration-shaped line — is consistent
  with the measurement rather than visible in it: registration LINES and distinct
  registered ids are both 102, which is exactly what "the em-dash pattern excludes it"
  predicts.
- **G5 THE PROBE IS BEHAVIOUR-NEUTRAL (at C3) — PASS, REAL_EXIT=0.**
  `python3 -B -m pytest tests/ -q -p r31probe`, serially, in the disposable worktree:
  `18350 passed, 23 skipped, 1 warning in 1303.84s (0:21:43)`, exit 0 — the reviewer's
  numbers exactly. ZERO tests failed, so the "re-run any failure without `-p`" branch had
  no input. The golden-path canary `pytest tests/cli/test_golden_path.py -q` was re-run
  independently: `42 passed in 19.12s`, exit 0.
- **G6 THE MEASUREMENT REPRODUCES (at C3) — PASS, REAL_EXIT=0.** Second full suite run
  under the probe: `18350 passed, 23 skipped, 1 warning in 1312.01s (0:21:52)`, exit 0.
  Compared as sets of `(owner, field, mode, path, line, function)`: run 1 holds **2734**,
  run 2 holds **2734**, and the SYMMETRIC DIFFERENCE IS **EMPTY** — printed in full,
  `<empty>`, not summarised. THE PROBE REPRODUCED EXACTLY ACROSS THE TWO RUNS.
- **G7 THE INVENTORY'S NUMERALS ARE THE RUN'S (at C3) — PASS with 11 declared
  differences, REAL_EXIT=0.** Every figure in the inventory is produced by the two
  instruments; none is retyped. 33 figures were compared against the block, 22 read
  `same` and 11 read `differs`. All eleven are listed under "Deviations" below and are
  marked `differs` in the inventory's own tables.
- **G8 NOTHING ELSE MOVED (at C4) — PASS, REAL_EXIT=0.** `.agent/STOP` absent (read from
  disk), `git status --porcelain` EMPTY, `git worktree list` exactly ONE entry, branch
  `feature/f275-one-world-completion-part-three`. `git diff --name-only 0b009325..0ce086ae`
  is an EXACT SET MATCH over 7 paths against the change set minus `.agent/handoff.md`:
  MISSING `[]`, EXTRA `[]`. ZERO paths under `packages/`, `apps/`, `tests/`, `docs/` or
  `scripts/` appear in that diff — T002's "no production line moves" holds. Per-commit
  insertions before the handback: 381, 326, 17, 8, 498, 16, every one under the
  DECISION F104 D1 cap of 500.

## Authored-text proofs

Every slice was extracted from the COMMITTED C0a blob `3deba3d5` with
`git cat-file blob`, never from a retype, and every one is a WHOLE-LINE slice owning its
terminating newline. Disk-to-disk results:

| Slice | Bytes | sha256 | Result |
|---|---|---|---|
| the block itself | 33235 | `cbd927e5…f8b2bf19` | scratch, `.agent/authored/f275-r31.md` and `.agent/last_block.md` all BYTE-EQUAL |
| PLAN31 | 1918 | `4d6578b0…c3a8581d` | committed `.agent/plan.md` BYTE-EQUAL to the slice |
| RECORD31 | 2913 | `6835af0e…fb88ae57` | appended verbatim; both G3 readers accept, both reject the control |
| SLIPS31 | 1879 | `43de122a…4b8bf388` | appended verbatim; both G3 readers accept, both reject the control |
| DECISION31 | 7513 | `0ca4ead6…516eb996` | appended verbatim; both G3 readers accept, both reject the control |

No slice was repaired, reflowed or re-typed.

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly:
no extra commit, no dropped commit, no reordering.

**D1 — ELEVEN MEASURED FIGURES DIFFER FROM THE BLOCK, all declared, none repaired.**
G7 asks for the number actually measured; these are they, and each is marked `differs`
in the inventory's own tables:

| Figure | measured | block |
|---|---|---|
| static: provably `Job`, sites | 322 | 325 |
| static: provably `Job`, lines | 322 | 325 |
| executed but not statically provable | 1446 | 1443 |
| `Job(...)` constructions | 587 | 586 |
| `Job(...)` constructions, test | 575 | 574 |
| alternative route: sites | 977 | 1201 |
| alternative route: distinct changed lines | 976 | 1087 |
| alternative route: production lines | 106 | 109 |
| alternative route: production files | 10 | 9 |
| alternative route: test lines | 870 | 978 |
| alternative route: test files | 53 | 61 |

Three readings put them in proportion, and the middle one is the important one.
(a) THE RULED SITE SET IS NOT AMONG THEM: all twelve probe and union figures read
exactly as the block states — probe 1757 sites over 1755 lines, 349 production in 68
files and 1406 test in 115 files; UNION 1768 sites over 1766 lines, 357 production in
68 files and 1409 test in 117 files; 11 sites provably `Job` and never executed; 92 of
the executed-but-unprovable sites called something OTHER than `Job`. The static sweep's
three-site difference falls ENTIRELY inside the probe's own set, since both readings put
11 in `provably Job but never executed`, so it moves the union by nothing.
(b) THE CONSTRUCTION DIFFERENCE IS ONE REAL SITE: this sweep counts a call whose callee
is an attribute named `Job` as well as a bare `Job(...)`, which adds
`tests/test_patch_apply.py:177`,
`__import__("packages.core.models", fromlist=["Job"]).Job(name="symlink test")` — a
genuine construction the bare-name reading misses.
(c) THE ALTERNATIVE ROUTE IS THE LARGE DIFFERENCE AND IT IS NOT DEFINITIONAL. No
counting variant of this probe's own rows reproduces 1201 and 1087: raw rows,
`(path, line, field)`, that key plus `mode`, that key plus `function`, and
`(path, line)` read 977, 977, 977, 977 and 976. DECISION F275 D17's rejection of that
route is unaffected — it turns on the line count being far over the 500-insertion cap,
and 976 is as far over it as 1087 — but the figure the decision quotes is not the figure
this run produced, and T003 must re-derive it rather than inherit either number.

**D2 — DECISION F275 D17's "ZERO commits exceed 500 insertions" NEEDS A QUALIFIER.**
Walking `a5bf8949..0b009325` and summing the insertion column of `git diff --numstat`
against each commit's first parent, the range holds 235 commits, of which 2 are MERGES.
Over the 233 SINGLE-PARENT commits the claim is TRUE and the maximum is 490 insertions
at `05cdebe2`. Over the range as `git rev-list` returns it the claim is FALSE: `b6e0f257`
carries 804 insertions and `a1df5d70` carries 805, both merges of `main` bringing
operator amendment amend0908 onto this branch. Neither is authored work this feature's
commit discipline measures, so D17's conclusion — F275's one declared-oversize allowance
is unspent — stands unchanged. The slice was applied verbatim and this is declared, not
repaired; the qualifier is also recorded in the inventory's section 9.

**D3 — A FIRST FULL-SUITE RUN WAS DISCARDED AS A PILOT AND IS REPORTED HERE.** The very
first `-p r31probe` suite run ended `2 failed, 18342 passed, 29 skipped` at exit 1.
NEITHER failure was a probe defect and both were re-run to prove it.
`tests/orchestration/test_ci_budgets.py::test_this_repository_really_is_at_or_below_the_lint_ceiling`
was red because the two untracked instrument files at the worktree root carried 7 `UP031`
violations, pushing `ruff check .` past the frozen ceiling of 26; the instruments were
made lint-clean (`All checks passed!` on both) and the repository then read exactly 26.
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
was red because a fresh worktree has no `node_modules`, so `npx vitest run` could not
resolve `vitest/config`; after linking `node_modules` the whole class re-ran GREEN
WITHOUT the probe (`4 passed`, exit 0), which is the G5-ordered control. Both G5 and G6
above are the runs taken AFTER those two environment repairs, and both are exit 0 at
18350 passed and 23 skipped. No test was deleted, skipped or weakened.

**D4 — THE INVENTORY WAS TRIMMED TO FIT THE 500-INSERTION CAP, AND THE STATIC INSTRUMENT
WAS COMPACTED TO MAKE THAT POSSIBLE.** SPEC-INVENTORY mandates the full source of BOTH
instruments; at first authoring the file was 569 lines, which as a new file is 569
insertions and would have breached DECISION F104 D1 — and spending F275's one
declared-oversize allowance here is exactly what DECISION F275 D17 reserves it against.
`r31probe.py` was NOT touched, because it had already run both suites and the source
embedded in the inventory must be the source that ran. `r31_static.py` was compacted from
206 to the 180 lines the inventory embeds, and its `With`-statement binding clause — an
addition of mine that SPEC-STATIC does not order, and that contributed zero `job`
verdicts — was removed; the sweep was re-run after every edit and
its JSON output compared with `cmp` against the pre-compaction output, reading
BYTE-IDENTICAL each time, so no measured number moved. The remaining reduction came out
of my own prose. The committed file is 498 lines. The tension is real and belongs to the
block rather than to this round: two mandated instrument sources plus the mandated tables
leave under 170 lines for everything else.

**D5 — CONSTRAINT 10 WAS CHECKED BEFORE IT WAS TRUSTED.** The two R27 prose slips the
block says are already on disk are the last two entries of `.agent/prose_slips.md` at
`0b009325`, read directly. SLIPS31 was applied as written and books three lines, not four.

**Assumption, stated because a reviewer will re-derive it.** "Production" means any
tracked path not under `tests/`. Every production/test split in the inventory uses that
rule, and it reproduces all six of the block's own probe and union splits exactly, so it
is the rule the block used too.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the block verbatim | done | |
| C0b mirror the committed blob | done | |
| C1 PLAN31 | done | |
| C2 RECORD31 + SLIPS31 | done | |
| C3 build, run, and record the measurement | done | |
| C4 DECISION31 | done | |
| C5 the handback | done | |
| G1 transport | done | PASS |
| G2 the plan | done | PASS |
| G3 the record | done | PASS over all three targets |
| G4 the open set | done | PASS, 87 by distinct id |
| G5 probe behaviour-neutral | done | PASS, 18350 passed / 23 skipped, exit 0 |
| G6 the measurement reproduces | done | PASS, symmetric difference EMPTY |
| G7 the inventory's numerals | done | PASS with 11 declared differences |
| G8 nothing else moved | done | PASS |

## State

- Open findings: **87** by distinct id, unchanged from the base `0b009325`. This round
  registered none and resolved none. Four are High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12.
- THE PROBE REPRODUCED ACROSS THE TWO RUNS. The symmetric difference of the two site sets
  is EMPTY at 2734 records each. That is the property T003 relies on, and it is measured
  rather than assumed.
- The ruled site set for the flip is **1768 sites over 1766 distinct changed lines** —
  357 production lines in 68 files and 1409 test lines in 117 files — beside 587
  `Job(...)` constructions, 346 `Job` imports and 374 `Job` annotations. It is a FLOOR
  and not a ceiling: a site both unexecuted and unprovable is invisible to both
  instruments and is deliberately given no numeral.
- No line under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moved. T002 is a
  measurement and a ruling, not the flip.

## Next

The reviewer books the round 31 verdict, and then T003 lands the classic runner and the
classic store with the flip as F275's one declared-oversize commit — re-deriving the site
set at its own base rather than inheriting the figures above, and stating the
inseparability reason in its handback BEFORE review, per AGENTS.md.
