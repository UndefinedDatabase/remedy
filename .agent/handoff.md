# Handback — F275 round 35

## Session

SESSION 16 of feature F275 · round 35 · rounds so far 35

Context self-assessment (amend0905-throughput): context is comfortable — the
round's only long run was the 12-minute scoped orchestration suite and no
production file was read for editing, so there is ample room for further rounds
this session.

## Range

Review of `df5d527f`..`1e65661a`, plus the C4 commit that writes this file — a
handoff cannot name its own SHA (the R-0149 self-reference exception), so the
range is stated to C3 and C4 is called out in the commit table below.

## Commits

### 36123491 F275 R35 C0a: save the round 35 step block verbatim.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f275-r35.md | +382/-0 | the block saved with `shutil.copyfile`, byte-verbatim |

### 569b30d4 F275 R35 C0b: mirror the committed step block into the last-block pointer.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +323/-329 | written from `git cat-file blob` of the committed C0a blob, never a retype |

### 02b90479 F275 R35 C1: the round 35 plan.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +20/-18 | whole-file replacement by the PLAN35 slice |

### c0de8e51 F275 R35 C2: book the round 34 verdict and two prose slips.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | RECORD35 appended — the round 34 PASS verdict |
| .agent/prose_slips.md | +4/-0 | SLIPS35 appended — the two round 34 prose slips |

### 1e65661a F275 R35 C3: add the event-name coupling ratchet, the second measurement R-0832 asks for.
| Path | +/- | Reason |
|------|-----|--------|
| tests/orchestration/test_event_name_coupling.py | +145/-0 | NEW file, the GUARD35 slice byte for byte |

### C4 (this commit) F275 R35 C4: the round 35 handback.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | this file; a handoff cannot table the commit that writes it (R-0149) |

## External actions

- `git worktree add .remedy-wt/r35wt 1e65661a` — created for G6; the five
  mutations and the base collection count ran only inside it.
- `git worktree remove --force .remedy-wt/r35wt` then `git worktree prune` —
  removed before this handback; `git worktree list` reads exactly ONE entry.
- `git push -u origin feature/f275-one-world-completion-part-three` — after C4.
- No `gh` command run. NO PR created, none edited, none merged: this round is
  not a closure sequence.

## Verification

Every gate was run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. One line per gate,
real exit codes, real numbers.

- **G1 TRANSPORT (at C0b) — exit 0.** `.remedy-wt/f275-r35-block.md` is 26187
  bytes at sha256 `e7fd8ff1efb71ded013ff68347b7b27a1e1e8ece9c673755b958539281e8729b`;
  the committed `.agent/authored/f275-r35.md` and `.agent/last_block.md` are both
  26187 bytes at that same digest, and both resolve to ONE shared git blob
  `f2293206c9256476487937970a031e4eae4092d7`. `.agent/last_block.md` was produced
  by `git cat-file blob HEAD:.agent/authored/f275-r35.md`, never retyped. THE
  CHAIN COVERS THREE ON-DISK ARTEFACTS — the scratch original, the authored copy
  and the pointer — and makes NO claim about bytes emitted into a prompt.
- **G2 THE PLAN (at C1) — exit 0.** PLAN35 slice 2417 bytes and committed
  `.agent/plan.md` 2417 bytes, both at sha256
  `5b8e91b2ff2858751f28f9c338ee48c3abd2ecb326bae39aa62fa5e1af64d34c`, BYTE-EQUAL.
  43 lines against the cap of 50. `^## Goal$` exactly 1, `^## Next Steps$`
  exactly 1.
- **G3 THE RECORD (at C2) — exit 0.** `.agent/live_review.md` pre 814121 bytes
  (constraint 4's figure), slice 5288, post 819410 == pre + 1 + slice; the
  joining byte READ BACK at offset 814121 is `b'\n'`. `.agent/prose_slips.md` pre
  223959 (constraint 4's figure), slice 1523, post 225483 == pre + 1 + slice;
  joining byte at offset 223959 is `b'\n'`. Independent structural reader, with N
  counted from each SLICE and not from the block: N=1 for RECORD35 and N=2 for
  SLIPS35, and the last N blank-line units of each post-blob match the slice's N
  paragraphs IN ORDER. Negative controls, one per append, each flipping a byte
  INSIDE THE FIRST appended paragraph (offset 814162 `b'r'`→`b'R'`; offset 224000
  `b'l'`→`b'L'`): REJECTED by BOTH readers in both files. `^Gate: F275 R34 `
  exactly 1.
- **G4 THE OPEN SET (at C3) — exit 0.** BY DISTINCT ID, every `^- R-\d+ — ` id
  minus every `^Done: R-\d+ — ` id: at the base `df5d527f` 103 registered and 16
  resolved for an OPEN SET OF 87; at C3 `1e65661a` 103 registered and 16 resolved
  for an OPEN SET OF 87. Ids registered this round: `[]`. Ids resolved this
  round: `[]`. Both EMPTY, per constraint 8. Reported separately as the block
  requires: **`R-0832` IS IN THE OPEN SET AT C3** and carries NO `Done:` line —
  its absence was examined, not assumed.
- **G5 THE GUARD IS THE AUTHORED BYTES (at C3) — exit 0.** GUARD35 slice 5951
  bytes at sha256
  `95997b5602ec6cc9576004f06dfbdfd75e350b2a2cefc1bf6e1068edade7f0b8`; the
  committed `tests/orchestration/test_event_name_coupling.py` is 5951 bytes at
  the same sha256, BYTE-EQUAL. The path did NOT exist at the base —
  `git cat-file -e df5d527f:<path>` exits 128. `python3 -m ruff check
  tests/orchestration/test_event_name_coupling.py` printed exactly
  `All checks passed!` at exit 0.
- **G6 THE GUARD BITES — RED PROOF (at C3) — driver exit 0.** In the disposable
  worktree `.remedy-wt/r35wt` at C3 with `__pycache__` purged (0 dirs found —
  the worktree was fresh) and every run under `python3 -B`. CONTROL, unmutated:
  exit 0, `4 passed in 4.12s`. Each anchor was counted in its named revert target
  and read exactly 1 before the mutation was applied, and each was reverted
  byte-exactly (sha256 re-read) before the next.
  - **M1** delete `    "context_budget_optimized",` from
    `KNOWN_DEAD_EVENT_COUPLINGS` — target the guard, anchor count 1. RED, exit 1,
    `1 failed, 3 passed`. ASSERTION FIRED:
    `TestEventNameCouplingRatchet::test_every_dead_coupling_is_declared`. Revert
    verified back to `95997b5602ec6cc9…`.
  - **M2** insert `    "no_such_event_name",` as the first entry — target the
    guard, anchor count 1. RED on TWO assertions as ordered, exit 1,
    `2 failed, 2 passed`. ASSERTIONS FIRED:
    `…::test_the_declared_set_only_ever_shrinks` (the ceiling) AND
    `…::test_no_declared_entry_is_stale` (the staleness check). Revert verified.
  - **M3** replace the two-line `return {name: sorted(rs) …}` comprehension
    ending `dead_event_couplings` with `    return {}` — target the guard, anchor
    count 1. RED, exit 1, `1 failed, 3 passed`. ASSERTION FIRED:
    `…::test_no_declared_entry_is_stale` — blinding the instrument does NOT read
    as a clean tree, which is the anti-blindness direction. Revert verified.
  - **M4** weaken the floor `assert len(deleted_modules()) >= 40` to `>= 0` —
    target the guard, anchor count 1. **GREEN, exit 0, `4 passed`.** THIS IS THE
    HONEST NEGATIVE RESULT THE BLOCK PREDICTED AND ORDERED ANYWAY, reported as
    such and NOT treated as a failure and NOT "fixed": a test cannot detect the
    weakening of its own assertion, which is precisely why the floor is a
    separate test rather than a clause inside another one. Revert verified.
  - **M5** the real-world direction, revert target a DIFFERENT FILE — insert
    `    "context_pack_created": frozenset({"chars"}),` immediately above
    `    "context_budget_optimized": frozenset({` in
    `packages/orchestration/event_schemas.py`, anchor count 1 in that file. RED,
    exit 1, `1 failed, 3 passed`. ASSERTION FIRED:
    `…::test_every_dead_coupling_is_declared` — a survivor that starts reading an
    event only a deleted module ever emitted IS caught. Reverted, and the CONTROL
    IS GREEN AGAIN: exit 0, `4 passed in 4.13s`.
  - After all five reverts `git status --porcelain` in the worktree was EMPTY,
    which is the git-level confirmation that every revert was byte-exact.
- **G7 NOTHING ELSE MOVED (at C3) — exit 0.** `.agent/STOP` read from disk:
  ABSENT. `git status --porcelain`: EMPTY (`''`). `git worktree list`: exactly
  ONE entry, the primary checkout. Branch
  `feature/f275-one-world-completion-part-three`.
  `git diff --name-only df5d527f..1e65661a` returns 6 paths and is an EXACT SET
  MATCH against the header's `Change:` list — MISSING `[]`, EXTRA `[]`.
  **ZERO paths under `packages/`, `apps/`, `docs/` or `scripts/` appear in that
  diff** (constraint 5). Per-commit insertions, every commit before the handback,
  each under the DECISION F104 D1 cap of 500: C0a +382, C0b +323, C1 +20, C2 +6,
  C3 +145. Canary `python3 -m pytest tests/cli/test_golden_path.py -q`: exit 0,
  `42 passed in 19.02s`. Scoped set `python3 -m pytest tests/orchestration/ -q`,
  serial: exit 0, `11826 passed, 10 skipped, 1 warning in 726.21s (0:12:06)`.
  Collection `python3 -B -m pytest tests/ -q --collect-only`: **18362 tests
  collected at the base** `df5d527f` (measured in the disposable worktree) and
  **18366 at C3** — a delta of exactly 4, the four tests this file adds, matching
  the reviewer's reading exactly.

The full serial suite was NOT run this round, per constraint 7: the change set
holds one new test file and no production line, so the round gate is the scoped
set plus the canary — verification tier 1.

## Authored-text proofs

Four slices, each extracted mechanically from `.agent/authored/f275-r35.md`'s
scratch original by delimiter line and applied with `shutil.copyfile` semantics,
never retyped and never reflowed:

| Slice | Target | Bytes | sha256 (slice == applied) | Result |
|-------|--------|-------|---------------------------|--------|
| PLAN35 | `.agent/plan.md` (whole-file) | 2417 | `5b8e91b2ff2858…` | BYTE-EQUAL |
| RECORD35 | `.agent/live_review.md` (append) | 5288 | `1e2f4ba9ebb060…` | BYTE-EQUAL |
| SLIPS35 | `.agent/prose_slips.md` (append) | 1523 | `d3c86f61a32c97…` | BYTE-EQUAL |
| GUARD35 | `tests/orchestration/test_event_name_coupling.py` (NEW) | 5951 | `95997b5602ec6c…` | BYTE-EQUAL |

The block file itself was verified on arrival at 26187 bytes and sha256
`e7fd8ff1…8729b`, matching the delegating reviewer's stated digest before any
work began.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 the plan | done | |
| C2 the record and the slips | done | |
| C3 the guard | done | |
| C4 the handback | done | this commit |
| G1 transport | done | exit 0 |
| G2 the plan | done | exit 0 |
| G3 the record | done | exit 0 |
| G4 the open set | done | exit 0; 87 at base and 87 at C3 |
| G5 the authored bytes | done | exit 0; ruff `All checks passed!` |
| G6 the red proof | done | 4 of 5 mutations RED with named assertions; M4 GREEN as ordered |
| G7 nothing else moved | done | exit 0; zero production paths |
| R-0832 | deviated | DELIBERATELY NOT RESOLVED — see below |

## Open findings

**87 by distinct id** at C3, unchanged from the base `df5d527f`. This round
registered NO finding and resolved NONE. Four are High — R-0803, R-0804, R-0806
and R-0807 — all F273's, per DECISION F272 D12. The next free id is R-0875 and
this round did not spend it.

## Deviations & assumptions

1. **R-0832 IS DELIBERATELY LEFT OPEN and no `Done:` or `Landed:` line was
   written for it.** This is the block's own instruction, not a shortfall: the
   finding's fix clause has two halves and this round lands only the FIRST, the
   second measurement. The second half — ruling how each dead coupling is
   disposed of — belongs to the round that drafts DECISION F260 D3, because the
   one dead coupling that exists, `context_budget_optimized`, survives as a
   run-log SCHEMA entry and a UI action-class entry, and DECISION F275 D18 ruled
   that a schema for an event historical run logs still carry is KEPT. Which
   reading governs is a ruling and D3 owns it. G4 gates that R-0832 is still in
   the OPEN set at C3, and it is.
2. **M4 of the G6 red proof came back GREEN.** Reported as the honest negative
   result the block predicted, not repaired and not re-specified. Weakening
   `assert len(deleted_modules()) >= 40` to `>= 0` cannot be detected by the
   suite, because that assertion IS the detector; the mutation removes the
   instrument rather than breaking something the instrument watches. The design
   answer already in the file is that the floor lives in its own test
   (`test_the_instrument_sees_the_deleted_modules_at_all`) rather than as a
   clause inside another, so that deleting it changes the collected test count —
   which the G7 collection reading (18362 → 18366) makes visible.
3. **The commit sequence was C0a, C0b, C1, C2, C3, C4 — SIX commits, exactly as
   constraint 2 ordered.** No extra commit, none dropped, no reordering. Stated
   here explicitly because the template requires any departure to appear in this
   section, and the absence of one is worth recording where a reader auditing the
   round will look.
4. **Scratch-file note, no repo effect.** The gate driver scripts were written
   into the gitignored `.remedy-wt/` scratch directory, and two early ones
   (`g3.py`, `g4.py`) reused generic names that a previous round had also used
   there, overwriting that round's scratch. Nothing under version control was
   touched; the remaining drivers were named `r35_g5.py`, `r35_g6.py` and
   `r35_g7.py` to avoid the collision. Recorded only so a later reader does not
   mistake a prior round's scratch for a lost artefact.
5. **No pull request was created and nothing was merged**, per the delegation:
   this round is not a closure sequence. The Open PR Gate was therefore not
   exercised and no `gh` command was run.

## Next

Review the committed range `df5d527f`..`HEAD` (C0a through C4) and issue the
round 35 verdict.
The next round's work order is `.agent/plan.md` Next Step 1: DECISION F260 D3 —
name all 43 deleted modules and the feature that inherited each, rule the
disposal of every dead event coupling this round's ratchet reports, and delete
what that ruling condemns. That discharges the second half of R-0832 and is the
last thing T001 owes. Phase 1 rule 1 first: re-read `.agent/STOP` from disk
before authoring.
