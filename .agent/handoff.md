# Handback — F275 round 41

## Session

SESSION 17 of feature F275 · round 41 · rounds so far 41

Context self-assessment (amend0905-throughput): context is comfortable — this
round read AGENTS.md, one 280-line protocol doc, a 105-line template, one
26383-byte block and the two edit targets, and spent the rest of its cost on
the six gate scripts and their runs rather than on reading, so there is room for
further rounds this session.

F275 stands at 41 rounds and 17 sessions against the operator's soft limit of 60
rounds and 20 sessions (amend0908-f275-finish rule 1), so no scope report is
owed.

## Range

Review of `bbede92f`..`HEAD` — C0a through C4. C4 is the commit that writes this
file, so the range is measured to C3 in full and C4 is called out in the commit
table below (the R-0149 self-reference exception).

## Commits

### addded9d F275 R41 C0a: save the round 41 step block as authored text.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f275-r41.md | +421/-0 | the delegation block saved with `shutil.copyfile`, byte-verbatim at 26383 bytes |

### f0894ab7 F275 R41 C0b: mirror the round 41 block into the last-block state file.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +356/-395 | written from `git cat-file blob HEAD:.agent/authored/f275-r41.md`, never retyped; the two paths resolve to ONE git blob |

### 83904d14 F275 R41 C1: the round 41 plan.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +15/-17 | whole-file replacement by the PLAN41 slice; the plan is current before any other change, per §3 item 23 |

### 82d36d9d F275 R41 C2: book the round 40 verdict and the two round 40 prose slips.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | the RECORD41 slice appended — the round 40 PASS verdict |
| .agent/prose_slips.md | +4/-0 | the SLIPS41 slice appended — two round 40 prose slips, the wrapper claim and the GFM pipe |

### 17be0eb4 F275 R41 C3: widen TaskEntry with output_artifact_ids and a per-task budget.
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/pingpong_job.py | +13/-0 | pairs H, I and J: the two fields on the dataclass, then symmetrically through `_export_job` and `_import_job` |
| tests/orchestration/test_job_administrative_fields.py | +85/-0 | pair L imports `TaskEntry`, then append K adds `TestTheTwoTaskFieldsWidenedInBeforeTheFlip` with its four tests |

### C4 — the commit that writes this file
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | (self-reference) | this handback; its own numbers are not ordered, per §3 item 14 |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/r41-wt 17be0eb4` | created, detached at C3, for G6 only |
| `git worktree remove --force …/r41-wt` then `git worktree prune` | removed; `git worktree list` reads exactly ONE entry |
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C4; see below |

No PR was created, edited or merged. No `remedy` command was run. Nothing was
force-pushed and no history was rewritten.

## Verification

Each gate was run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Real exit codes and
real numbers, one line per gate.

**G1 TRANSPORT (at C0b) — REAL_EXIT=0.** `.agent/authored/f275-r41.md` and
`.agent/last_block.md` are both 26383 bytes at sha256
`0c3a56c2fee41894378b9fa042dd6493d6962641652d876783f9e818539419d4`, identical to
the reviewer's delegation source as stated in the delegation, and
`git rev-parse` resolves both committed paths to the ONE blob
`1aa34ec1874015a6eefeedca2a4ace269b3d5f9d`. `.agent/last_block.md` was written
from `git cat-file blob HEAD:.agent/authored/f275-r41.md`. This chain covers
three ON-DISK artefacts — the block file under `.remedy-wt/`, the authored copy
and the mirror — and claims nothing whatever about the bytes emitted into a
prompt.

**G2 THE PLAN (at C1) — REAL_EXIT=0.** `.agent/plan.md` is 2441 bytes at sha256
`ff04470a1cf1ebe8c5c9b535e20af28a924d333b01bed688317f867d3105251d`, BYTE-EQUAL
to the PLAN41 slice as extracted (`True`). 42 lines against the AGENTS.md cap of
50. `^## Goal$` = 1, `^## Next Steps$` = 1.

**G3 THE RECORD (at C2) — REAL_EXIT=0.** Two readers plus a negative control per
append, all against COMMITTED blobs (pre = C1 `83904d14`, post = C2 `82d36d9d`).
`.agent/live_review.md`: pre 851931 (baseline matched) + 1 + slice 3687 = 855619
= post; reader A byte reconstruction `True`; joining byte at offset 851931 read
back as `b'\n'`; reader B structural, N=1 counted FROM THE SLICE, `True`; post
sha256 `3fc10665…`. `.agent/prose_slips.md`: pre 233188 (baseline matched) + 1 +
slice 1412 = 234601 = post; reader A `True`; joining byte at offset 233188 read
back as `b'\n'`; reader B structural, N=2 counted FROM THE SLICE, `True`; post
sha256 `a68b2c74…`. Negative control, one byte flipped INSIDE THE FIRST APPENDED
PARAGRAPH — offset 851972 and offset 233229 respectively — both readers REJECTED
both controls (A `False`, B `False`, four rejections). `^Gate: F275 R40 ` reads
exactly 1 at C2.

**G4 THE OPEN SET (at C3) — REAL_EXIT=0.** By distinct id, `^- R-\d+ — ` minus
`^Done: R-\d+ — `, read from `git show <rev>:.agent/live_review.md` into memory
and never by writing over the tracked file. Base `bbede92f`: 103 distinct
registrations, 17 distinct resolutions, OPEN **86**. C3 `17be0eb4`: 103, 17,
OPEN **86**. Ids registered this round `[]`; ids resolved this round `[]`. Both
readings are the ones the block predicted.

**G5 THE WIDEN IS THE AUTHORED BYTES (at C3) — REAL_EXIT=0.** ONE chained
reconstruction per file, from the committed BASE blob to the committed C3 blob,
applying that path's slices in the constraint-5 order.
`packages/orchestration/pingpong_job.py`: base 164734 bytes; PAIRH, PAIRI and
PAIRJ each read FROM 1x before, and for each `TO contains FROM: True`, so NO
FROM-zero count was taken or claimed — all three are append-shaped; each TO reads
exactly 1x in the committed C3 blob; reconstruction 165637 bytes sha256
`8aadab4b…` IDENTICAL to the committed C3 blob 165637 sha256 `8aadab4b…`.
`tests/orchestration/test_job_administrative_fields.py`: base 8785 bytes; PAIRL
is a REWRITE — FROM 1x before / 0x after, TO 0x before / 1x after; APPEND K's
obligation is ORDERED EQUALITY and no per-line count was taken — the state pair L
leaves (8800 bytes) is a byte-exact PREFIX of the committed C3 blob (`True`) and
K (3681 bytes) is an exact SUFFIX of it (`True`), 8800 + 3681 = 12481 = the
committed blob; reconstruction sha256 `7c5ad7f9…` IDENTICAL to the committed C3
blob 12481 sha256 `7c5ad7f9…`. Every reviewer length reproduced exactly: 164734 →
165637 and 8785 → 12481.
`python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_administrative_fields.py`
→ `All checks passed!`, REAL_EXIT=0, the reviewer's reading.

**G6 THE WIDEN BITES — RED PROOF (at C3) — REAL_EXIT=0.** In a DISPOSABLE
worktree detached at C3, `__pycache__` purged before every run, every run under
`python3 -B`, selection scoped to the target file. The import was resolved
first and reads
`/home/decodeux/Repos/remedy/.remedy-wt/r41-wt/packages/orchestration/pingpong_job.py`,
so no editable install shadowed the worktree.

| Run | Anchor count before | REAL_EXIT | Reading | Reviewer's reading |
|---|---|---|---|---|
| CONTROL unmutated | — | 0 | `12 passed` | exit 0, `12 passed` |
| M1 — export line DELETED | 1 | 1 | `2 failed, 10 passed` | exit 1, `2 failed, 10 passed` |
| M2 — import line DELETED | 1 | 1 | `2 failed, 10 passed` | exit 1, `2 failed, 10 passed` |
| CONTROL AGAIN after both reverts | — | 0 | `12 passed` | exit 0, `12 passed` |

M1 and M2 named the SAME two assertions the block named, read from the `FAILED`
lines and not from the exit code:
`tests/orchestration/test_job_administrative_fields.py::TestTheTwoTaskFieldsWidenedInBeforeTheFlip::test_both_survive_the_round_trip_through_json`
and
`…::TestTheTwoTaskFieldsWidenedInBeforeTheFlip::test_both_survive_the_real_job_record_file`.
Each mutation's anchor was counted and read 1 before it was applied; each was
reverted byte-exactly with the sha256 re-read — module pristine
`8aadab4b…`, M1 mutated `fd05f416…`, reverted `8aadab4b…`, M2 mutated
`058981ba…`, reverted `8aadab4b…`, final `8aadab4b…` equal to pristine.

**G7 THE SCOPED GATE (at C3) — REAL_EXIT=0.**
`python3 -B -m pytest tests/orchestration/test_job_administrative_fields.py tests/cli/test_golden_path.py -q`
→ `54 passed in 18.91s`, REAL_EXIT=0 — the reviewer's figure, the target file's
own 12 plus the canary. The property through the SHIPPED functions rather than by
grep, REAL_EXIT=0: `dataclasses.fields(TaskEntry)` reads 25 fields and BOTH
`output_artifact_ids` and `budget` are present; a bare `TaskEntry(task_id="x")`
reads `[]` and `None` for them; `_export_job`'s task dict has 25 keys and carries
BOTH `output_artifact_ids` and `budget`.

**G8 NOTHING ELSE MOVED (at C3) — REAL_EXIT=0.** `.agent/STOP` read FROM DISK:
**ABSENT**. `git status --porcelain`: **EMPTY**. `git worktree list`: exactly
**ONE** entry. `git diff --name-only bbede92f..17be0eb4` reads 7 paths and is an
EXACT SET MATCH against the block's `Change:` list minus `.agent/handoff.md` —
**MISSING `[]`, EXTRA `[]`**. **ZERO** paths under `apps/`, `docs/` or
`scripts/`. The only two paths outside `.agent/` are the C3 pair, so constraint 4
holds. Per-commit insertions against the DECISION F104 D1 cap of 500: C0a +421,
C0b +356, C1 +15, C2 +6, C3 +98 — every one under the cap. No oversize commit is
declared this round.

## Authored-text proofs

Every slice was extracted MECHANICALLY by its delimiter lines from the COMMITTED
`.agent/authored/f275-r41.md` — read via `git cat-file blob`, never from the
working tree — and applied with `shutil.copyfile` semantics or by byte
concatenation. Nothing was retyped and nothing was reflowed. Extracted lengths
and digests, every one matching the block's stated figure where the block stated
one:

| Slice | Bytes | sha256 | Block's stated figure |
|---|---|---|---|
| PLAN41 | 2441 | `ff04470a…` | not stated |
| RECORD41 | 3687 | `bbb58579…` | not stated |
| SLIPS41 | 1412 | `8f9ac6c6…` | not stated |
| PAIRH_FROM | 67 | `d76d8b99…` | 67 bytes, `d76d8b990df61ef5…` — MATCH |
| PAIRH_TO | 762 | `4090a79a…` | 762 bytes, `4090a79a9f21a35c…` — MATCH |
| PAIRI_FROM | 60 | `998e62f1…` | 60 bytes, `998e62f123c2856e…` — MATCH |
| PAIRI_TO | 158 | `9a0133e6…` | 158 bytes, `9a0133e60bbcdea2…` — MATCH |
| PAIRJ_FROM | 64 | `8b6b6f21…` | 64 bytes, `8b6b6f21c7d6ac2f…` — MATCH |
| PAIRJ_TO | 174 | `66053bbe…` | 174 bytes, `66053bbe27714841…` — MATCH |
| PAIRL_FROM | 137 | `151806bf…` | 137 bytes, `151806bf94f6c9fb…` — MATCH |
| PAIRL_TO | 152 | `15c90d5d…` | 152 bytes, `15c90d5db522173a…` — MATCH |
| APPENDK | 3681 | `e1fe7a11…` | 3681 bytes, `e1fe7a11a1db651a…` — MATCH |

The disk-to-disk comparison the fidelity protocol asks for is stronger here than
a `cmp` of one file: G5 rebuilt each committed C3 blob from its committed BASE
blob out of those extracted slices alone and compared sha256, and both matched.

## Item-status table

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a save this block | done | |
| C0b mirror it | done | |
| C1 the plan | done | |
| C2 the round 40 verdict and two prose slips | done | |
| C3 the widen | done | pairs H, I, J, then L, then append K — the constraint-5 order |
| C4 the handback | done | this file |
| G1 transport | done | REAL_EXIT=0 |
| G2 the plan | done | REAL_EXIT=0 |
| G3 the record | done | REAL_EXIT=0 |
| G4 the open set | done | REAL_EXIT=0, 86 at the base and 86 at C3 |
| G5 the authored bytes | done | REAL_EXIT=0, both reconstructions identical |
| G6 red proof | done | REAL_EXIT=0, control 12 passed, both mutations 2 failed / 10 passed |
| G7 the scoped gate | done | REAL_EXIT=0, 54 passed |
| G8 nothing else moved | done | REAL_EXIT=0, exact set match |

## Open findings

**86 by distinct id**, unchanged from this round's base `bbede92f` — 103 distinct
registrations against 17 distinct resolutions, at the base and again at C3. This
round registered none and resolved none, exactly as constraint 7 ordered. Four
are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.

## Deviations & assumptions

**None.** The six commits ran in the block's exact order — C0a, C0b, C1, C2, C3,
C4 — with no extra commit, none dropped and no reordering. Every slice applied
byte for byte; nothing in the block failed to fit; no gate went red; no gate was
substituted, widened or narrowed; and no reading disagreed with the reviewer's
own. Two readings are worth stating explicitly because they are absences rather
than numbers, and an absence is easy to mistake for an omission:

- NO FROM-ZERO COUNT was taken for pairs H, I or J. Constraint 6 forbids it and
  the reason was re-measured here rather than assumed: each pair's `TO contains
  FROM` reads `True`, so a zero count is unattainable by construction. What was
  measured instead is FROM exactly 1x before and TO exactly 1x in the committed
  C3 blob.
- NO PER-LINE COUNT was taken for append K. It is a CODE append, so its
  obligation is ORDERED EQUALITY (§4.9 as finding R-0531 narrowed it), and that
  is what G5 proves: prefix, suffix and a whole-blob sha256 match.

One assumption is recorded because it was checked rather than believed: the
comment applied by PAIRH_TO asserts that `JobPlan.budgets` is already a
serialized dict on this same record. The dataclass was read to confirm it —
`budgets: dict | None = None` at `packages/orchestration/pingpong_job.py`, under
the comment "F018: job budget limits (serialized dict from
`JobBudgets.model_dump`, or None)". The claim the authored comment makes is true,
and `budgets` is a different field from the F272 T002 administrative `budget`.

## Next

The reviewer reads `bbede92f`..`HEAD` and issues the round 41 verdict. The next
round is step 1 of the plan: the flip itself, as the one declared-oversize commit
AGENTS.md permits per feature, with the inseparability reason AND the real size
stated in the handback BEFORE review. Per Phase 1 of the self-drive protocol,
rule 1 is checked before rule 2 — `.agent/STOP` read from disk first.

## Reviewer verdict on round 41 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 41: **PASS.** Written by the planner and reviewer of SESSION 17 after reading the committed
range `bbede92f`..`17be0eb4` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the
worker's report was evidence for no line below. It is carried here because under
`docs/agents/self_drive_protocol.md` a verdict that stays in the session is lost, and it is booked into
`.agent/live_review.md` by the FIRST SUBSTANTIVE COMMIT of round 42, per amend0827-process-diet rule 1.

WHAT THE REVIEWER RE-MEASURED. Six single-parent commits C0a `addded9d`, C0b `f0894ab7`, C1 `83904d14`,
C2 `82d36d9d`, C3 `17be0eb4` and C4 `a75d72d1`, per-commit insertions 421, 356, 15, 6 and 98 for the five
before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1: the delegation
source was written AND HASHED BEFORE delegation at
`0c3a56c2fee41894378b9fa042dd6493d6962641652d876783f9e818539419d4`, and both committed copies are 26383
bytes at that digest as ONE shared git blob. G2: `.agent/plan.md` byte-identical to PLAN41 at 2441 bytes,
42 lines against the cap of 50. G3: `.agent/live_review.md` 851931 to 855619 and `.agent/prose_slips.md`
233188 to 234601, each post-blob equal to its pre-blob then ONE newline then the slice, both joining bytes
newlines, and `^Gate: F275 R40 ` exactly 1. G4: the open set is 86 BY DISTINCT ID at the base and at C3,
over 103 registrations against 17 resolutions. G8: the change set is an EXACT set match over eight paths
with MISSING and EXTRA both empty.

G5 IS THE GATE THIS ROUND TURNED ON AND IT HOLDS AS ONE CHAINED RECONSTRUCTION PER FILE, committed blob to
committed blob. `packages/orchestration/pingpong_job.py` rebuilds from 164734 bytes to the committed 165637
by applying pairs H, I and J in order, byte-identical at
`8aadab4b…`; all three are APPEND-SHAPED, re-measured rather than assumed — each FROM still reads 1x AFTER
the edit, which is why no FROM-zero count was ordered or taken, per §4.9 and §3 item 15.
`tests/orchestration/test_job_administrative_fields.py` rebuilds from 8785 to 12481 by applying pair L and
then appending K, with the post-L state a byte-exact PREFIX of the committed blob and K an exact SUFFIX —
the ORDERED EQUALITY that binds a CODE append, never the per-line count that binds prose, per finding
R-0531. `ruff` printed `All checks passed!` on both files, re-run by the reviewer.

THE WIDEN WAS BUILT AND RED-PROVED BY THE REVIEWER BEFORE DELEGATION AND THE WORKER'S READINGS REPRODUCE IT
IN ALL FOUR. Control 12 passed at exit 0; M1, deleting the export key, and M2, deleting the import keyword,
each exit 1 at `2 failed, 10 passed` naming the SAME two assertions —
`test_both_survive_the_round_trip_through_json` and `test_both_survive_the_real_job_record_file` — read from
the `FAILED` lines rather than inferred from the exit code; both reverts byte-exact by sha256; control green
again. The reviewer additionally ran the WHOLE orchestration suite with the widen applied before authoring
and read `11879 passed, 10 skipped` with one failure,
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`, which was
then measured to fail IDENTICALLY at the unmodified base in the same worktree — the known fresh-worktree
artefact, not this change. G7's shipped-function probe re-run by the reviewer: `TaskEntry` now declares 25
fields, both new ones present, a bare instance reads `[]` and `None`, and the scoped gate plus the canary
read 54 passed.

THE WORKER DECLARED NO DEVIATION AND THE REVIEWER FOUND NONE. It stated two ABSENCES explicitly rather than
leaving them to be read as omissions — no FROM-zero count for the three append-shaped pairs, and no per-line
count for the code append — and it CHECKED a claim this block made rather than believing it, confirming
against the source that `JobPlan.budgets` really is a serialized dict on the same record and that it is a
distinct field from the administrative `budget` F272 T002 added. That is the round auditing the block.

## Session 17 ends here — SIX delegated rounds, six PASS verdicts, and the reason it stops

Rounds 36, 37, 38, 39, 40 and 41, every one a PASS, against the amend0905-throughput target of SIX TO EIGHT
and its floor of four. THE TARGET IS MET, not merely the floor. F275 stands at 41 rounds and 17 sessions
against the operator's soft limit of 60 rounds and 20 sessions under amend0908-f275-finish, so no scope
report is owed.

WHY IT STOPS HERE, and the reason is the second of the two amend0905-throughput sanctions — the next round
explicitly needs a fresh session — now backed by a measurement rather than by a feeling. THE NEXT ROUND IS
THE FLIP, and this session's whole arc was finding out how big it actually is. DECISION F275 D17 sized it at
1766 changed lines from the `.id` and `.name` half alone and said in its own words that the figure was a
FLOOR. Round 36 re-derived that half at its own base and ENUMERATED it, 1753 sites over 184 files. Round 38
enumerated the classic store seam, 821 calls over 152 files, 44 of which the first list cannot see. Round 39
recorded DECISION F275 D21: the union is 3771 changed lines across 263 files, 7.5 times the per-commit cap
rather than the 3.5 D17 implied, and the route is unchanged because AGENTS.md permits exactly one declared
oversize commit per feature and every alternative needs two. Round 40 then found what none of that had
counted — DECISION F275 D22, a SECOND type pair, `Task` to `TaskEntry`, sharing two field names of seven and
twenty-three, with three `Task` fields having no counterpart of the same meaning and one of them read at 35
sites. Round 41 widened two of those three in, green by construction, which takes 427 lines back out of the
flip. Planning the flip against a context that already carries six rounds of measurement is how the
one-per-feature oversize allowance gets spent badly, and it can only be spent once.

WHAT THIS SESSION LANDED. R-0870 IS RESOLVED — the finding grew from two instances to ten across five rounds
of repair, and it is closed on the reviewer's own re-run of BOTH sweeps against the committed tree, with the
reason no guard replaces them recorded in the resolution: 320 of the module paths named under `packages/`,
`apps/`, `tests/` and `scripts/` do not resolve, and almost every one is a test fixture. DECISION F260 D3
gained the nineteen deleted CLI handler modules it never named, mapped from git rather than from their
names, so the feature's DONE condition is met on a reading instead of an inference. Two enumerations and two
decisions now describe the flip. `TaskEntry` carries the two fields the classic record would otherwise have
taken with it. The open set fell from 87 to 86, the only movement this session made to it.

FOUR INSTRUMENTS THIS SESSION ADDED TO HOW THIS REPOSITORY MEASURES ITSELF, each found by RUNNING something
rather than by reasoning about it. A command-surface sweep, because every sweep this feature had run looked
for deleted MODULE STEMS and a page can advertise a dead capability without naming one — which is how a
"Planned migration path" came to offer an operator a command deleted twenty rounds earlier. A seam
enumerator, because a rename-shaped measurement cannot see a file that calls the store without reading the
renamed field. A type-pair reader that imports both shipped classes instead of parsing them. And the
arithmetic that unions three enumerations by `(path, line)` so the parts can be added without double
counting.

CONTEXT SELF-ASSESSMENT, as amend0905-throughput requires in one sentence: the reviewer's context is long
but not exhausted, and exhaustion is expressly NOT the reason this session ends — it ends because the flip
is a single unsplittable commit of measured size that deserves a session built around it.

## What the next session owes, in order

FIRST, Phase 1 rule 1: re-read `.agent/STOP` from disk before the Open PR Gate. It did not exist at this
session's Phase 0 probe, was measured absent before every round's first commit, and is absent as this
session ends. Then the Open PR Gate: no pull request is open, and none is owed until the closure sequence.

SECOND, round 42's FIRST SUBSTANTIVE COMMIT books, from this file as the durable carrier under
amend0827-process-diet rule 1, the ROUND 41 PASS verdict above as a `Gate: F275 R41` entry in
`.agent/live_review.md`. No prose slip is owed for round 41: the worker declared no deviation and the
reviewer found none. The open set is 86 and the next free id after R-0874 is R-0875; that booking registers
nothing and resolves nothing, so it stays 86. A round whose WHOLE change set is that booking is forbidden,
so it rides with the round that is happening anyway.

THIRD, THE FLIP. It is applied from three committed lists — `.agent/f275_t003_flip_sites.md` for the `.id`
and `.name` sites, `.agent/f275_t003_flip_seam.md` for the classic store seam, and
`.agent/f275_t003_task_pair.md` for the second type pair — as the ONE declared-oversize commit AGENTS.md
permits per feature. The declaration states the REAL size, which DECISION F275 D21 measures and D22
corrects, and it states it in the handback BEFORE review, which is what AGENTS.md's Commit Discipline
requires of an oversize commit. That round also registers `Task.acceptance_checks`'s structured form as a
finding naming the feature that owns acceptance criteria, per operator amendment amend0908-f275-finish rule
4, because the widen deliberately did not carry it. THE REVIEWER OF THAT SESSION SHOULD EXPECT TO SPEND
MOST OF IT ON THE DRY RUN: this session's own attempt at a mechanical transformation established that the
flip is not a rename — the classic `Job.id` is a `UUID` where `JobPlan.job_id` is a 16-hex `str`, and the
store functions differ in name, in return type and in whether they can return `None`.

FOURTH, the resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO job stores"
paragraph, every which-store branch and the absence test — with the classic store, which is the same commit
range by that decision's own terms. Then the closure sequence: the integration gate, the evidence job, a
fresh review zip, the ledger rotation, the STATUS line and the PR.
