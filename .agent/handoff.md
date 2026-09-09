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

## Reviewer verdict on round 17 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 17: **PASS.** Written by the planner and reviewer of SESSION 9 AFTER reading the
committed range `12dd60ad`..`f5509039` and RE-RUNNING every one of the five gates independently
against the committed blobs; the worker's report was not taken as evidence for any line below.
It is carried here because under `docs/agents/self_drive_protocol.md` a verdict that stays in
the session is lost, and it is booked into `.agent/live_review.md` by the FIRST substantive
commit of round 18, per amend0827-process-diet rule 1.

WHAT THE REVIEWER RE-MEASURED. Six single-parent commits C0a `10034ac5`, C0b `bc2cca93`, C1
`97f71317`, C2 `d7e71e1d`, C3 `ee86115a` and C4 `f5509039`, per-commit insertions 254, 162, 18,
10 and 8 for the five before the handback commit, every one far under the AGENTS.md DECISION
F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the
reviewer's own delegation source and both committed copies are 28529 bytes at
`05bf237e16c1bb54e3ae5bf5003d47512baf87ee0d528eeede51b46520473c42` and compare BYTE-EQUAL; per
§3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes.
G2: `.agent/plan.md` at C1 is byte-identical to the PLAN17 slice at 2537 bytes and
`e2f68029…`, 44 lines against the cap of 50, both mandated headings present; the block is 254
lines against its cap of 490; and the SPINE17 slice — the one slice this round SUBSTITUTES into
a documentation body rather than appending to a record — occurs EXACTLY ONCE in the committed
`docs/system/core-product-spine-v0.md` and is byte-identical there. G3, over two appends:
`.agent/live_review.md` 650049 to 659974, growth 9925 = 1 + 9924; `.agent/prose_slips.md`
189111 to 191891, growth 2780 = 1 + 2779; for both the prefix and suffix are byte-exact and the
joining byte was read back as a newline; N was COUNTED from each slice by the reviewer's own
reader as 2 and 3, ordered equality held over the WHOLE appended region, and BOTH negative
controls, flipped IN MEMORY inside the FIRST appended paragraph per §3 item 36, were REJECTED
by BOTH readers, with both files re-read from disk and byte-equal to their committed
post-blobs. `^Gate: ` 38 to 39, and `^Gate: F275 R16 ` and `^- R-0861 — ` exactly 1 each; THE
OPEN SET 84 TO 85 BY DISTINCT ID against registrations 89 to 90 and resolutions 5 to 5.

G4 IS THE GATE ROUND 16 FAILED AND IT IS NOW GREEN, re-run by the reviewer with its own script
over 29 tokens and the 1676 tracked files outside `.agent/` and `.data/` at C3. RAW 11,
STRIPPED 3. Both binding conditions hold with EMPTY violation sets: every RAW line outside
`docs/roadmap/features/` lies in a path this block's change set names — there is exactly one,
`docs/system/core-product-spine-v0.md:51`, which is the deliberate-absence note this round ADDS
and which quotes the deleted command names on purpose — and every STRIPPED line lies in
`docs/roadmap/features/`, those three being `T2_F262.md`, `T2_F267.md` and `T8_F151.md`. The
three quickstart sections, the three quickstart table rows, the spine's two taxonomy rows and
the morning report's five-step `## How Claude Code fits` section are all GONE.

G5: the documentation gate 851 passed and the canary 42 passed, both exit 0; THE FULL SUITE WAS
RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18603 passed, 23
skipped and ZERO failed, with 18603 + 23 = 18626 equal to the C3 collection — identical to
round 16's figures, which is what a round touching no `.py` file must produce; and the tree gate
holds with `.agent/STOP` absent, porcelain empty, ONE worktree, the branch correct, and the C3
path set an EXACT MATCH on three paths with the missing and extra sets both EMPTY. The
per-path numstat at C3 reads 0/32, 8/8 and 0/11, matching the block's prediction cell for cell.

THE WORKER'S FIVE DECLARED DEVIATIONS ARE ALL SUSTAINED, and the load-bearing one is the
reviewer's again. The block's SPINE17 order said the slice replaces the body "between the
heading line and the blank line preceding `## What a report is`", which read strictly spans
seven lines and would have produced 8/9 for that file — contradicting the same block's own
measured `8 / 8` in its change set. The worker kept the blank line after the heading, replaced
the two prose paragraphs, and landed exactly 8/8 with the slice byte-identical at the site;
the reviewer confirms both the count and the byte identity independently. That is the worker
resolving a contradiction internal to the reviewer's text in the direction the measured numeral
fixed, which is the correct reading. Its other four are sound: a stale opening git snapshot
correctly diagnosed as stale rather than treating the block's base as wrong; the ten
`builder.<sub>` ids resolved mechanically from the catalog rather than by a grep that also
matches `builder.py` and `builder.name`; three stale-looking spans INSIDE change-set files left
untouched because no G4 token matches them and constraint 2 binds — declared, not widened,
which is exactly right; and the block's fixed bundle order requiring C0a and C0b to be
committed while `plan.md` still described round 16.

## Finding resolution drafted by session 9, to be booked by round 18's FIRST substantive commit

Done: R-0861 — RESOLVED at C3 `ee86115a`, verified by the reviewer of session 9 by re-running
the completeness sweep itself rather than reading the worker's report. All three pages the
finding names are repaired. `docs/guides/simple-operator-quickstart-v0.md` loses its
`### Check worker readiness`, `### Add a worker` and `### Disable a worker` sections with their
fenced `bash` blocks, and the three table rows that mapped those commands onto the equally
deleted `builder adapter-*` commands; `### Check core health` survives untouched, because
`remedy doctor core` is not deleted. `docs/system/core-product-spine-v0.md` loses its two
command-taxonomy rows, and the body of its `## What a worker is` section is replaced by the
deliberate-absence note AGENTS.md's Code Discoverability Conventions require — the heading
stays, so a reader searching for worker onboarding lands on the sentence saying Remedy
deliberately ships no such command and naming `packages/orchestration/exec_guard.py` and F085
as where the surviving capability lives. `docs/system/mission-run-loop-morning-report-v0.md`
loses its `## How Claude Code fits` section whole, every step of which named a rail rounds 13,
15 or 16 deleted. THE MEASUREMENT that closes it: the sweep at C3 reads RAW 11 and STRIPPED 3
with both violation sets EMPTY, against RAW 16 and STRIPPED 6 with three violations at the base.
The finding's FIX CLAUSE remains BINDING on every remaining deletion round of this feature and
is NOT discharged by this resolution: the completeness sweep is read as its RAW list and not
only as its stripped count, and the block names every `docs/guides/` and `docs/system/` page the
sweep reaches rather than only the pages a consumer map predicted. R-0847 is NOT resolved and
gains a third measured instance here — `tests/cli/test_advertised_commands.py` passed at exit 0
over the state this round found broken, both before and after the repair.

## Prose slip drafted by session 9, to be appended by round 18's ledger commit

2026-09-09 · F275 R17 · The round 17 block described the SPINE17 substitution region as lying "between the heading line and the blank line preceding `## What a report is`", which read strictly spans seven lines and implies a numstat of 8/9, while the same block's own change set gave the measured figure 8/8. The worker resolved the contradiction toward the measured numeral — keeping the blank line after the heading and replacing the two prose paragraphs — landed exactly 8/8 with the slice byte-identical at the site, and declared it. Nothing landed wrong. The lesson is that a block substituting a slice into the MIDDLE of a file states the region by its two anchor lines and by the numstat it measured, and the reviewer reads those two statements against each other before emission exactly as §3 item 18 requires of a probe's recipe and its property, because here both halves were individually sound and only their agreement was not checked.

## THE ROUND 18 MAP — MEASURED AT `f5509039`, AND WHY THIS ROUND NEEDS ITS OWN SESSION

THE MODULE: `packages/orchestration/overnight_executor.py`, 1119 lines, component line 1 of
`.agent/f275_deletion_order.md`, a SINGLE module. Its handler
`apps/cli/commands/overnight_cmd.py` is 109 lines and carries FOUR commands —
`overnight.readiness`, `overnight.plan`, `overnight.report` and `overnight.run` — all four
resolved through the shipped readers by import, not by grep.

THIS ROUND IS NOT MECHANICAL, AND THE REASON WAS MEASURED RATHER THAN GUESSED. Three SURVIVING
modules import two functions out of the dying module, and both functions are a safety
mechanism rather than a convenience:

  packages/orchestration/orchestrator_brain.py:303      parse_review_findings,
                                                        review_findings_block_execution
  packages/orchestration/self_dogfood_execution.py:422  parse_review_findings,
                                                        review_findings_block_execution
  packages/orchestration/self_dogfood.py:235            parse_review_findings

`parse_review_findings` reads `.agent/live_review.md` and `review_findings_block_execution`
turns its verdict into a BLOCK on execution, returning `OvernightStopReason.REVIEW_FINDINGS_OPEN`
when the record carries an open blocker or a High finding. `self_dogfood.py` line 234 states the
dependency in its own words — "Reuse the safe live-review parser from the overnight executor".
So `orchestrator_brain._review_state` and `self_dogfood_execution._review_blocks` are gates that
stop work when the review record says stop, and this deletion removes the thing they call.

WHY THAT NEEDS A DATED DECISION BEFORE THE FIRST `git rm`, and why the next session should make
it unhurried. F275 T001 RULE 3 is explicit — "A SURVIVING CONSUMER LOSES THE CALL SITE, NEVER
GAINS A COPY... No stub, no shim, no copy of cluster code into a survivor" — so the surviving
three must lose the gate rather than inherit the parser. But unlike round 15's deletion, which
was fail-safe because it removed a capability, THIS ONE REMOVES A RESTRICTION: after it,
`orchestrator_brain` and `self_dogfood_execution` no longer consult the live-review record before
allowing work, which is strictly LESS conservative. DECISION F275 D7's fail-safe argument does
not reach it and must not be copied onto it. A second reading is available and must be measured
rather than assumed: `docs/system/development-artifact-boundary-v0.md` already rules that product
modules must NOT depend on `.agent/live_review.md`, and these three do exactly that through this
parser, so deleting the dependency may be discharging a boundary violation rather than removing a
safeguard. Which of those two readings is right decides whether the round registers a capability
loss under RULE 3 or records a boundary repair, and it is the round's real planning work.

ALSO OWED AND NOT YET MEASURED: `overnight.report` is the current holder of the name F260's
Design carries over to `mission report`, and DECISION F274 D2 rules that the carry-over and this
deletion are ONE commit. `mission.report` already exists in the catalog and survives, so the next
session must measure whether D1's carry-over already discharged this and say so, rather than
inferring it. `overnight.readiness` names a command whose module `overnight_readiness` is a
SEPARATE component, line 3 of the order file, while its handler sits in the file this round
deletes — so the four commands do not all die together and the split must be measured before the
block is authored.

## Session 9 ends here — THREE delegated rounds, one FAIL and its repair, all independently re-gated

This is stated plainly rather than dressed up. `docs/agents/self_drive_protocol.md` G7, as
amended by amend0905-throughput, targets six to eight delegated rounds per session with FOUR as
the floor, and this session ran THREE. The reason amend0905 sanctions and that applies here is
the one measured above — round 18 is a round that explicitly needs a fresh session — and it is
offered as a MEASUREMENT, not a preference: three surviving product modules call a live-review
safety gate out of the dying module, the deletion is the first of this feature that makes Remedy
LESS conservative rather than more, two independent readings of it are on disk and disagree, and
a carry-over ruled by DECISION F274 D2 to be part of the same commit has not been measured.
Beginning that round on the remainder of this session would mean authoring its block against an
unmeasured boundary and an unmade ruling, which this feature's record shows costs a round.

A SECOND OBSERVATION IS RECORDED BUT IS EXPLICITLY NOT CITED AS THE REASON, because operator
amendment amend0908-f275-finish rule 5 permits "authoring errors accumulating" to end a session
only after at least FOUR delegated rounds and this session ran three. It belongs in the record
anyway: this session's blocks produced NINE prose slips — five from round 15, three from round
16 and one from round 17 — and one omission that turned a gate genuinely RED. Every one was
caught by a worker or by the reviewer's own re-gate and none reached disk uncorrected, but the
trend is the signal amend0905 names and the next session should treat this paragraph as a
warning about its own authoring rather than as a complaint about this one.

WHAT THIS SESSION LANDED. Round 15, the TENTH module group `managed_builder_execution` at 1694
module lines, 30 paths, 42 insertions against 4802 deletions, taking seventeen commands, the
`execution` group and fourteen `ContractAction` members, with DECISION F275 D7 ruling the
approval-gate question from a repo-wide measurement — PASS. Round 16, the ELEVENTH group
`main_builder_adapter` at 964 module lines, 24 paths, 13 insertions against 2519 deletions,
taking the `builder` group's ten commands, six actions and the three `worker` commands R-0857
ordered deleted rather than narrowed twice — FAIL on G4 alone, for a documentation file the
reviewer's change set never named. Round 17, the repair, which swept every surviving
advertisement across three pages and turned G4 green — PASS. Findings R-0855 through R-0861
were registered across the three rounds and two of them, R-0855 and R-0861, are resolved by
reviewer-authored text. The full suite is green at 18603 passed, 23 skipped and ZERO failed,
and eleven of F260's prototype-cluster module groups are now gone with four components left in
`.agent/f275_deletion_order.md`.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: the reviewer's
context was NOT the binding constraint and remained comfortable throughout — this session ran
eleven full serial suites, three of them establishing round boundaries by execution and three
of them independent re-gates — and the session ends with round 18's boundary measured by
reading every call site rather than inferred from a map.

## What the next session owes, in order

FIRST, Phase 1 rule 1: re-read `.agent/STOP` from disk before the Open PR Gate. It does not
exist as this session ends and was measured absent at the Phase 0 probe, again before each of
the three rounds, and again now. Then the Open PR Gate: no pull request is open, and none is
owed until the closure sequence.

SECOND, round 18's FIRST substantive commit books, from this file as the durable carrier under
amend0827-process-diet rule 1: the ROUND 17 PASS verdict above as a `Gate: F275 R17` entry in
`.agent/live_review.md`, the `Done: R-0861` resolution, and the prose slip as a dated line in
`.agent/prose_slips.md`. The open set is 85 by distinct id and the next free id is R-0862;
after the R-0861 resolution is booked it is 84.

THIRD, round 18 itself: rule the live-review-parser question as a dated DECISION in
`.agent/decisions.md` BEFORE the first `git rm`, measure the `overnight.report` carry-over
against DECISION F274 D2 and the `overnight.readiness` handler split, complete an applied dry
run to a green suite before authoring anything, and order the mutation red-proofs in full
because three surviving production modules lose code.
