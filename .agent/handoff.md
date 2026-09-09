# Handback — F275 round 17

## Session

SESSION 9 of feature F275 · round 17 · rounds so far 17

F275's soft limit is 20 sessions and 60 rounds by operator amendment
amend0908-f275-finish rule 1, and it travels to no other feature. This round is
well inside it, so no scope report is owed.

This was a REPAIR round. Round 16's gate G4 went red at exit 1 because the
reviewer's exhaustive change set never named
`docs/guides/simple-operator-quickstart-v0.md`; round 16's worker declared the
red gate rather than widening its scope, which is the sanctioned move. This
round sweeps the RAW list rather than only the stripped count, as R-0861's fix
clause binds.

## Range

Review of `12dd60ad`..`HEAD`

## Commits

### 10034ac5 F275 R17 C0a: save the round 17 authored block.
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f275-r17.md | +254 / -0 | The delegation source copied byte for byte with `shutil.copyfile`, never retyped. |

### bc2cca93 F275 R17 C0b: mirror the round 17 block into the last-block state file.
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +162 / -303 | The same bytes mirrored; a single `.agent/**` state-file rewrite. |

### 97f71317 F275 R17 C1: advance the plan to round 17.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18 / -19 | Replaced WHOLE by the PLAN17 slice extracted from the committed C0a blob. |

### d7e71e1d F275 R17 C2: book the round 16 FAIL verdict, register R-0861, record three prose slips.
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4 / -0 | LEDGER17 appended: the round 16 FAIL entry and the R-0861 registration. |
| .agent/prose_slips.md | +6 / -0 | SLIPS17 appended: three dated round 16 lines. |

### ee86115a F275 R17 C3: sweep the operator-facing advertisements of the deleted worker commands.
| Path | +/- | Reason |
|---|---|---|
| docs/guides/simple-operator-quickstart-v0.md | +0 / -32 | Three whole `###` sections (`Check worker readiness`, `Add a worker` with its `Known workers:` line, `Disable a worker`) and three "Advanced equivalent(s)" table rows deleted. `### Check core health` and the `job status`, `job report`, `job run-loop` and `doctor core` rows survive untouched. |
| docs/system/core-product-spine-v0.md | +8 / -8 | The `## What a worker is` body replaced by the SPINE17 deliberate-absence note (heading kept); the `worker doctor <name>` and `worker add <name>` taxonomy rows deleted. |
| docs/system/mission-run-loop-morning-report-v0.md | +0 / -11 | The `## How Claude Code fits` section deleted whole — every one of its five steps named a rail rounds 13, 15 or 16 deleted. |

The `+/-` column above was read from `git show --numstat` per commit and compared
cell by cell against the Verification lines below; every cell agrees. C3's totals
are +8 / -51 over three paths, matching the block's predicted "8 insertions
against 51 deletions" and its three predicted per-file numstats (0/32, 8/8, 0/11)
exactly.

The final handoff commit C4, which writes this file, cannot table itself
(R-0149 pattern); its numbers belong to the next round's ledger entry per §3
item 31.

## External actions

- `git push -u origin feature/f275-one-world-completion-part-three` — ONCE, after C4. Outcome recorded below.
- No PR created, edited or merged. No `gh` command run. No worktree added or removed.

## Verification

Five gates, every one EXECUTED, real exit codes captured with
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`.

- **G1 TRANSPORT — exit 0.** One digest comparison over three artefacts.
  `.remedy-wt/f275-r17.md`, the committed `.agent/authored/f275-r17.md` and the
  committed `.agent/last_block.md` are each 28529 bytes at sha256
  `05bf237e16c1bb54e3ae5bf5003d47512baf87ee0d528eeede51b46520473c42`;
  ALL THREE BYTE-EQUAL: True. Per §3 item 37 this covers those three artefacts
  and claims nothing about any other bytes.

- **G2 THE PLAN, THE BLOCK AND THE SPINE SLICE — exit 0.** C0a blob TOTAL 254
  lines against the cap of 490. `.agent/plan.md` at C1 is 2537 bytes, sha256
  `e2f6802970279070d19f28c02739714149d1fb068c8d6d8ba852deaefc9150e1`, BYTE-IDENTICAL
  to the PLAN17 slice extracted from the committed C0a blob between its marker
  lines; 44 lines against the AGENTS.md cap of 50; `## Goal` 1 occurrence and
  `## Next Steps` 1 occurrence. The SPINE17 slice (551 bytes, sha256
  `337d4871b586bc6d98c060a707a68f83cb2fd293d77a09f52d41b103ba6775b2`) occurs
  EXACTLY ONCE in `docs/system/core-product-spine-v0.md` at C3, and the bytes at
  that site re-hash to the same digest — byte-identical.

- **G3 THE RECORD, over TWO appends — exit 0.**
  - `.agent/live_review.md` <- LEDGER17. (a) BYTE READER: pre 650049 sha256
    `a7c801a7…`, post 659974 sha256 `81bb7a48…`, growth 9925 == 1 + 9924; pre a
    byte-exact PREFIX; slice a byte-exact SUFFIX; joining byte read back `b'\n'`.
    (b) STRUCTURAL READER: N COUNTED from the slice by the script = 2; the last 2
    blank-line units of the whole post-file equal the slice's 2 paragraphs in
    order, per-unit sha256 `112aaaf3cbec0f31` and `09187da105d565d2` on both
    sides. (c) NEGATIVE CONTROL: byte 653300 flipped `r` -> `R` IN MEMORY inside
    the FIRST appended paragraph — reader (a) REJECTS and reader (b) REJECTS,
    both accept the truth; file re-read from disk is 659974 bytes at `81bb7a48…`,
    byte-equal to the committed post-blob.
  - `.agent/prose_slips.md` <- SLIPS17. (a) pre 189111 sha256 `b821af02…`, post
    191891 sha256 `efe99ef7…`, growth 2780 == 1 + 2779; prefix, suffix and
    joining byte `b'\n'` all confirmed. (b) N COUNTED = 3; units
    `62176e3a21ad5091`, `9cdcb0bd813b8d50`, `3afe9989c706d99e` equal in order.
    (c) byte 189604 flipped `t` -> `T` inside the FIRST appended paragraph —
    BOTH readers REJECT the mutant and BOTH accept the truth; disk re-read
    byte-equal to the committed post-blob.
  - (d) COUNT PATTERNS in the post-blob: `^Gate: ` 38 -> 39, rise exactly 1;
    `^Gate: F275 R16 ` exactly 1; `^- R-0861 — ` exactly 1.
  - (e) THE OPEN SET BY DISTINCT ID, `Landed:` lines never subtracted —
    BEFORE at base `12dd60ad`: registered 89, done 5, open 84.
    AFTER at C2 `d7e71e1d`: registered 90, done 5, open 85.
    The base figures reproduce the reviewer's measured 89 / 5 / 84 exactly.
    (34 distinct `Landed:` ids exist and were not subtracted.)

- **G4 THE SWEEP IS CLEAN — exit 0.** This is the gate round 16 failed; it is
  now green. 29 tokens swept over 1676 tracked files outside `.agent/` and
  `.data/` (4563 tracked in total; 1 file skipped as undecodable, non-UTF-8).
  The ten `builder.<sub>` command ids were resolved mechanically from the
  catalog at `876dc89e` (the parent of round 16's C3) rather than assumed:
  `builder.adapter-enable`, `builder.adapter-list`, `builder.adapter-show`,
  `builder.integrity`, `builder.package-create`, `builder.session-create`,
  `builder.session-intake`, `builder.session-list`,
  `builder.session-record-output`, `builder.session-show`.
  **RAW 11, printed in full, never truncated:**
  ```
  docs/roadmap/features/T2_F085.md:152  managed_builder_execution
  docs/roadmap/features/T2_F085.md:254  managed_builder_execution
  docs/roadmap/features/T2_F085.md:264  managed_builder_execution
  docs/roadmap/features/T2_F260.md:344  main_builder_adapter
  docs/roadmap/features/T2_F260.md:345  managed_builder_execution
  docs/roadmap/features/T2_F262.md:75   builder.adapter-list
  docs/roadmap/features/T2_F262.md:79   builder.session-list
  docs/roadmap/features/T2_F267.md:14   builder.session-list
  docs/roadmap/features/T2_F267.md:27   builder.adapter-list
  docs/roadmap/features/T8_F151.md:22   main_builder_adapter
  docs/system/core-product-spine-v0.md:51  worker doctor, worker add, worker disable
  ```
  **STRIPPED 3:** `docs/roadmap/features/T2_F262.md:79`,
  `docs/roadmap/features/T2_F267.md:14`, `docs/roadmap/features/T8_F151.md:22`.
  BINDING CONDITION 1 — the only RAW path outside `docs/roadmap/features/` is
  `docs/system/core-product-spine-v0.md`, which this block's change set NAMES;
  the not-in-change-set set is EMPTY. That single line is the deliberate-absence
  note this round ADDS, which quotes the deleted command names on purpose.
  BINDING CONDITION 2 — all three STRIPPED lines lie in
  `docs/roadmap/features/`; the outside set is EMPTY.
  RAW 11 and STRIPPED 3 reproduce the reviewer's applied-dry-run figures
  exactly, in the three files it named.

- **G5 THE GUARDS, THE SUITE AND THE TREE — exit 0 on all four parts.**
  - (a) `python3 -B -m pytest tests/docs/ tests/cli/test_advertised_commands.py tests/cli/test_product_spine.py tests/cli/test_cli_ux.py tests/test_grouped_cli.py -q`
    → `851 passed in 36.59s`, REAL_EXIT=0. This is the §3 verification-tier-5
    documentation gate.
  - (b) canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`
    → `42 passed in 20.38s`, REAL_EXIT=0.
  - (c) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the
    PRIMARY checkout with C3 committed →
    `18603 passed, 23 skipped, 1 warning in 1333.60s (0:22:13)`, REAL_EXIT=0.
    ZERO FAILED. Collection at C3 measured separately with
    `pytest tests/ -q --collect-only` → `18626 tests collected`, REAL_EXIT=0.
    18603 + 23 = 18626 equals the C3 collection. These are the round 16 figures
    unchanged, as expected for a round with no `.py` file in its change set; no
    difference to report.
  - (d) `.agent/STOP` re-read from disk: ABSENT. `git status --porcelain`: empty.
    `git worktree list`: ONE entry, `/home/decodeux/Repos/remedy ee86115a
    [feature/f275-one-world-completion-part-three]`. Branch correct.
    `git diff --name-only d7e71e1d..ee86115a` is an EXACT MATCH on this block's
    three C3 paths — MISSING set EMPTY, EXTRA set EMPTY.
    Per-commit, every commit BEFORE C4, against the AGENTS.md DECISION F104 D1
    cap of 500 insertions:

    | Commit | SHA | Parents | +/- | Under cap |
    |---|---|---|---|---|
    | C0a | 10034ac5 | 1 | +254 / -0 | yes |
    | C0b | bc2cca93 | 1 | +162 / -303 | yes |
    | C1 | 97f71317 | 1 | +18 / -19 | yes |
    | C2 | d7e71e1d | 1 | +10 / -0 | yes |
    | C3 | ee86115a | 1 | +8 / -51 | yes |

    Every commit is single-parent. No commit is oversize, so no inseparability
    declaration is owed.

No mutation red-proof is reported because none is owed: this round's change set
touches only `docs/` and `.agent/`, and the block orders the verification-tier-5
documentation gate (G5a) in its place.

## Authored-text proofs

| Slice | Applied to | Bytes | sha256 | Proof |
|---|---|---|---|---|
| SPINE17 | `docs/system/core-product-spine-v0.md`, body of `## What a worker is` | 551 | `337d4871b586bc6d98c060a707a68f83cb2fd293d77a09f52d41b103ba6775b2` | Occurs EXACTLY ONCE at C3; bytes at the site re-hash to the slice digest (G2). Spliced programmatically from the extracted slice file, never retyped. |
| PLAN17 | `.agent/plan.md`, replaced WHOLE | 2537 | `e2f6802970279070d19f28c02739714149d1fb068c8d6d8ba852deaefc9150e1` | Committed blob at C1 BYTE-IDENTICAL to the slice (G2). 44 lines, cap 50. |
| SLIPS17 | `.agent/prose_slips.md`, appended | 2779 | — | Byte reader + structural reader (N counted = 3) + negative control, all in G3. |
| LEDGER17 | `.agent/live_review.md`, appended | 9924 | — | Byte reader + structural reader (N counted = 2) + negative control, all in G3. |

All four slices were extracted from the COMMITTED C0a blob between their
`--- BEGIN-<NAME> ---` / `--- END-<NAME> ---` marker lines, markers excluded, and
applied without retyping. No marker line reached any target file. Every slice was
applied BYTE FOR BYTE; none was edited.

## Deviations & assumptions

1. **The SPINE17 substitution region — declared reading, not a repair.** The
   change set says the SPINE17 slice is applied "between the heading line and the
   blank line preceding `## What a report is`". Read strictly, that region is 7
   lines (the blank line after the heading plus two prose paragraphs), and
   replacing it with the slice's 8 lines would have yielded a numstat of +8 / -9
   for this file once the two taxonomy rows are counted — contradicting the
   block's own measured `8 / 8`. I therefore kept the blank line immediately
   after the heading and replaced the two prose paragraphs (6 lines) with the
   slice's 8 lines, which yields exactly the measured +8 / -8 and produces
   well-formed markdown. The slice itself was applied byte for byte and is
   unedited; only the boundary of the region it replaced was resolved. Both
   readings satisfy G2's "occurs exactly once, byte-identical" condition.
   The applied result reads: heading, blank line, SPINE17, blank line,
   `## What a report is`.

2. **The block's `12dd60ad` base disagreed with this session's opening git
   snapshot, which showed `fadf4715`.** I re-read the branch from disk: HEAD was
   `12dd60ad`, matching the block. The snapshot was stale, not the block. No
   action taken beyond verifying it.

3. **The ten `builder.<sub>` command ids in G4 are not enumerated by the block.**
   I resolved them mechanically from the catalog at `876dc89e`, the parent of
   round 16's C3, by matching quoted `"builder.<sub>"` ids under `packages/` and
   `apps/cli/` — exactly ten, listed in the G4 transcript. I did not guess them
   and did not use the looser `builder.<word>` grep, which also matches
   `builder.py`, `builder.name`, `builder.num`, `builder.model`,
   `builder.provider`, `builder.temperature`, `builder.build` — attribute and
   filename spellings, not command ids.

4. **Two stale-looking spans inside a change-set file were NOT touched, per
   constraint 2.** In `docs/system/core-product-spine-v0.md` the "What Remedy is
   today" prose still says Remedy helps operators "manage builder workers", the
   terminology table still defines **Worker**, and the Advanced-operator-path
   table still carries the row `` `builder adapter-show/enable/list` | Direct
   adapter management | Debugging adapter state ``. None of these matches any G4
   token — the spaced form `builder adapter-show` is not in the token list, only
   the dotted command ids are — so none is a gate condition, and the block's
   change set does not order them changed. I am declaring them rather than
   widening scope. This is an observation for the reviewer, not a finding of
   mine.

5. **Commit-gate ordering.** C0a and C0b were committed while `.agent/plan.md`
   still described round 16, because the block fixes C1 as the commit that
   advances the plan and places it after them. This follows the block's ordered
   bundle and the established pattern of rounds 14 through 16; it is noted here
   because AGENTS.md's Commit Gate reads on every commit.

No departure from the block's ordered commit sequence: six commits C0a, C0b, C1,
C2, C3, C4, in that order, none added, none dropped, none reordered.

I wrote no verdict, no `Done:` paragraph and no finding of my own.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the authored block | done | |
| C0b mirror to last_block.md | done | |
| C1 advance the plan | done | |
| C2 the record — LEDGER17 + SLIPS17 | done | |
| C3 sweep the advertisements — three paths | done | |
| C4 the handback | done | |
| SPINE17 slice | done | Substituted, not appended; region boundary declared as deviation 1. |
| PLAN17 slice | done | |
| SLIPS17 slice | done | |
| LEDGER17 slice | done | |
| G1 transport | done | exit 0 |
| G2 plan, block and spine slice | done | exit 0 |
| G3 the record, two appends | done | exit 0 |
| G4 the sweep is clean | done | exit 0 — RAW 11, STRIPPED 3 |
| G5 guards, suite and tree | done | exit 0 — 851 / 42 / 18603+23 |
| R-0861 | done | Swept; see the `Landed:` line below. The reviewer authors the resolution. |

Landed: R-0861 — the three operator-facing pages no longer advertise `worker doctor`, `worker add` or `worker disable`, and the sweep's stripped result outside `docs/roadmap/features/` is now empty.

## Open findings

85 by distinct id at C2 `d7e71e1d` (registered 90, done 5), up from 84 at the
base `12dd60ad` by this round's registration of R-0861. `Landed:` lines are never
subtracted. Four remain High — R-0803, R-0804, R-0806 and R-0807 — all F273's
rather than this feature's, per DECISION F272 D12.

R-0847, the advertised-commands guard's blindness, is measured a THIRD time by
this round: `tests/cli/test_advertised_commands.py` passed at exit 0 over the
state that G4 found red in round 16, and it passes again now. Until R-0847 is
fixed, every deletion round of this feature must read the RAW sweep list by hand
and not only the stripped count.

## Next

The reviewer independently re-runs all five gates against the committed blobs
over `12dd60ad`..`ee86115a` and issues the round 17 verdict, resolving or
re-opening R-0861 on its own authority. Phase 1 rule 1 first: re-read
`.agent/STOP` from disk before authoring round 18.

Round 18 is then the `overnight_executor` component, the regenerated order
file's first line and a SINGLE module.
