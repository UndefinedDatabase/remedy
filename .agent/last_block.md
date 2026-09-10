── STEP T003 (4 of n) — F275 ─────────────────────────────────
Goal:        Repair the last instance of R-0870's class, so the finding can be
             resolved at the next gate, and record DECISION F275 D21 — the flip's
             COMPLETE measured floor across its three enumerable parts, and what
             that figure does and does not change about the route.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 38
             verdict and two prose slips · C3 the last R-0870 repair · C4 the
             DECISION · C5 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r39.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `.agent/decisions.md`,
             `tests/orchestration/test_event_name_coupling.py`,
             plus `.agent/handoff.md` at C5.
Constraints: the numbered list below.
Done when:   gates G1 to G8 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end of frame; the single pure rule line below is exactly 62 `─` characters
──────────────────────────────────────────────────────────────

## Base

This round's base is `d341806e`. THE REPAIR WAS APPLIED AND GATED and EVERY
FIGURE IN THE DECISION WAS MEASURED by the reviewer in a disposable worktree at
that base before this block was authored.

## What this round is

THE LAST INSTANCE. `tests/orchestration/test_event_name_coupling.py` opens by
explaining what it guards, and names `tests/orchestration/test_cluster_deletion_map.py`
in the past tense without saying that DECISION F275 D15 retired that file at round
25. A reader following the path lands on nothing, which is R-0870's instance-one
shape exactly. After C3 both sweeps return only hits of the pattern this repository
wants — a sentence that names a deleted thing AND says it is gone — and the
reviewer resolves R-0870 at the next gate. It is NOT resolved here and the worker
writes no `Done:` paragraph.

WHY NO GUARD IS ADDED FOR THE CLASS, measured rather than preferred, and recorded
because the obvious next question is why R-0870 is closed by a sweep instead of by
a test. The reviewer measured at the base what a guard over `packages/`, `apps/`,
`tests/` and `scripts/` would have to accept: 1116 source files name 320 module
paths that do not resolve on disk, in 94 files, and almost every one is a TEST
FIXTURE — `packages/widget.py`, `tests/a.py`, `docs/guide.md` — invented by a test
to exercise a path-handling code path. That is the same measurement by which
DECISION F275 D16 rejected widening `tests/docs/test_named_source_paths.py` beyond
the two operator-facing trees, arriving from the other side. A guard there would
need an allowlist longer than the property it guards.

THE DECISION. DECISION F275 D17 ruled the flip's route on the `.id`/`.name` union
alone and said in its own words that the union is "a FLOOR on the flip's size and
not a ceiling", giving the remainder no numeral because none was measured. Rounds
36 and 38 enumerated two further parts. C4 records the union of all three, which
is larger than D17's figure by more than a factor of two, and rules what that
changes: the ROUTE is unchanged and the DECLARATION is not.

## Constraints

1. APPLY EVERY SLICE BYTE FOR BYTE. Extract each by its delimiter lines from the
   committed `.agent/authored/f275-r39.md` and apply with `shutil.copyfile`
   semantics — never by retyping, never reflowed. If anything does not fit,
   DECLARE it in the handback and apply the rest.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, exactly — seven commits, no
   extra, none dropped, no reordering. C1 is the first substantive commit and
   makes `.agent/plan.md` current before any other change, per §3 item 23.
3. THE APPEND BASELINES, read by the reviewer at the base: `.agent/live_review.md`
   is 839359 bytes, `.agent/prose_slips.md` is 230672 bytes and
   `.agent/decisions.md` is 1044462 bytes, each ending in a newline. An append is
   pre-blob, then ONE newline, then the slice as extracted. C2 makes two appends
   and each later append re-baselines on the state the one before it left.
4. C3 IS THE ONLY COMMIT THAT TOUCHES ANYTHING OUTSIDE `.agent/`. No path under
   `packages/`, `apps/`, `docs/` or `scripts/` moves in this round at all.
5. PAIR G IS A REWRITE AND NOT AN APPEND, and the containment test was RUN before
   emission rather than judged by eye: `TO contains FROM: false`. Its FROM spans
   the WHOLE PARAGRAPH rather than the sentences that change, which is what
   R-0870's widened fix clause asks for and what lets the replacement rewrap
   without leaving a ragged line; both sides are whole lines ending in a newline,
   and NEITHER carries trailing whitespace, measured. Order no "FROM 0x"
   whole-file count; the obligation is FROM exactly 1x before the edit and 0x
   after, which G5 states.
6. IDS REGISTERED THIS ROUND: none. IDS RESOLVED THIS ROUND: none. The open set
   is 87 by distinct id at the base and must read 87 at C4.
7. THE ROUND GATE IS TIER 1: the scoped commands in G6 and the canary. The full
   suite is NOT run this round.
8. NO NUMERAL IN THE DECISION IS RE-DERIVED BY THE WORKER. AMEND39 is a slice and
   lands byte for byte; G7 re-measures the figures it states and reports any
   difference rather than editing either side.

## SLICE PLAN39 → whole-file replacement of `.agent/plan.md`

<<<PLAN39
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 39 repairs the last instance of R-0870's class — a guard docstring that names the
retired cluster-deletion-map ratchet without saying it was retired — so that both sweeps
return only the pattern this repository wants and the reviewer can resolve the finding at
the next gate. The same round records DECISION F275 D21: the flip's COMPLETE measured floor
over its three enumerable parts, which is 3771 changed lines across 263 files, more than
double the figure DECISION F275 D17 ruled the route on. R-0870 STAYS OPEN until the
reviewer's `Done:` text lands.

## Next Steps

1. The flip itself, applied from the round 36 site enumeration and the round 38 seam list,
   as the one declared-oversize commit AGENTS.md permits per feature, with the
   inseparability reason AND the real size stated in the handback BEFORE review.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take. DECISION F275 D21 measures
  it at 7.5 times the per-commit cap rather than the 3.5 D17's figure implied, and it spends
  the one declared-oversize allowance AGENTS.md rations per feature.
- The open set is 87 by distinct id at this round's base `d341806e`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
PLAN39

## SLICE RECORD39 → append to `.agent/live_review.md`, in C2

<<<RECORD39
Gate: F275 R38 — the F275 round 38 entry. VERDICT PASS, written by the planner and reviewer of session 17 after reading the committed range `4921e117`..`d341806e` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Seven single-parent commits C0a `a8ab166e`, C0b `4e106fe8`, C1 `1bd549a9`, C2 `30d9479c`, C3 `a4251786`, C4 `850b0346` and C5 `d341806e`, per-commit insertions 401, 295, 17, 10, 8 and 322 for the six before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1: the reviewer's delegation source was written AND HASHED BEFORE delegation at `56b91f784c509be69ce354621eea8d1867af0c8e64560aa094640ce717169814`, and both committed copies are 30463 bytes at that digest as ONE shared git blob; per §3 item 37 that chain covers three on-disk artefacts and claims nothing about bytes emitted into a prompt. G2: `.agent/plan.md` byte-identical to PLAN38 at 2646 bytes, 46 lines against the cap of 50, both mandated headings exactly once. G3 OVER ALL FOUR APPENDS, each re-derived by the reviewer by reconstructing the post-blob from the pre-blob and the extracted slice: `.agent/live_review.md` 839359 at C3 after RECORD38 and NOTE38 at C2 and LANDED38 at C3, and `.agent/prose_slips.md` 230672 after SLIPS38; every reconstruction byte-identical to the committed blob, `^Gate: F275 R37 ` exactly 1 and `^Note: F275 R38 ` exactly 1. THE ONE PROOF THE WORKER COULD NOT TAKE AGAINST A COMMITTED BLOB IS DECLARED AND THE REVIEWER TOOK IT ANOTHER WAY: RECORD38 and NOTE38 share commit C2, so no committed state sits between them, and the worker re-baselined the second append in memory and anchored the final state to the committed C2 blob. The reviewer verified the pair as one chained reconstruction from the BASE blob through both slices to the committed C2 blob, which is the same property proved without an intermediate. G4: THE OPEN SET IS 87 BY DISTINCT ID at the base and at C4, over 103 registrations against 16 resolutions; `R-0870` is in it, carries ZERO `Done:` lines and FOUR `Landed:` lines. G5: PAIR F reconstructs exactly — FROM 1x before and 0x after, TO 1x after, post-blob equal to the pre-blob with the span replaced; and the property the repair exists for was measured through the SHIPPED catalog rather than by grep, 44 groups with `worker` and `mission` PRESENT and `approval` and `progress` ABSENT. G6: `tests/docs/` with `tests/cli/test_product_spine.py` reads 371 passed, re-run by the reviewer together with the canary at 413 passed total. G7 THE COMMAND-SURFACE SWEEP IS THE GATE THIS ROUND EXISTED FOR AND ITS READING IS THE ONE THAT MATTERS: 569 files, 28 hits at the base and 28 at C4, and the count is IDENTICAL BY DESIGN because the repaired sentence still names both groups — what changed is the CLASS, from "treats a dead group as live" to "names it and says it is gone", and the worker classified every hit and reported class D at ZERO at C4 against TWO at the base. A sweep whose count cannot move is measured by its classification or not at all. G8: the change set is an EXACT set match over eight paths with MISSING and EXTRA both empty, ZERO paths under `packages/`, `apps/`, `tests/` or `scripts/`, porcelain EMPTY, ONE worktree, `.agent/STOP` absent. THE COMMITTED SEAM ENUMERATION REPRODUCED THE REVIEWER'S OWN MEASUREMENT EXACTLY: 152 rows over 152 distinct paths in sorted order, 821 seam sites counted from the committed file itself, 52 production files and 100 test files, and the per-function split 513, 262, 6 and 40. THREE DEVIATIONS, ALL SUSTAINED AND ALL THE REVIEWER'S. FIRST, G8 ordered `ruff check .` "at 26" and named no exit code, and ruff exits non-zero whenever any error exists; the worker recorded the real exit 1 beside the count of 26 and the shipped ceiling comparison at exit 0. SECOND, SPEC-SEAM listed five sections without saying whether the banner was one of them, and the worker titled it so the headings match the spec's own numbering — the opposite choice from round 36, and the better one. THIRD, the worker flagged that G7's count could not move and said so before anyone could misread 28 against 28. NO FINDING IS REGISTERED AND NONE IS RESOLVED BY THIS GATE.
RECORD39

## SLICE SLIPS39 → append to `.agent/prose_slips.md`, in C2

<<<SLIPS39
2026-09-10 · F275 R38 · The round 38 block's G8 ordered `python3 -m ruff check .` and stated the reviewer's reading as "26", naming no exit code, while ruff exits non-zero whenever it finds anything at all and this repository's baseline is a RATCHET of 26 rather than a zero. The worker recorded the real exit 1 beside the count and beside the shipped ceiling comparison, which is the honest reading of all three. A gate over a tool that signals by EXIT CODE and reports by COUNT says which of the two it reads, because "the reviewer read 26" and "REAL_EXIT=0" are not the same claim and only one of them is true here.

2026-09-10 · F275 R38 · The round 38 block's SPEC-SEAM listed the generated file's sections in a numbered list beginning with a banner, and did not say whether the banner was section 1 or sat above the numbering. Round 36's worker read the same shape the other way and had to declare a one-off offset; round 38's titled the banner so the headings match the spec's own numbers. Both were right, which is the problem: a generation spec that numbers sections says explicitly whether its first item is a heading in the artefact or a preamble to it.
SLIPS39

## PAIR G → `tests/orchestration/test_event_name_coupling.py`

FROM is 599 bytes over 8 lines, sha256 `ad158a6503e6d06b…`; TO is 823 bytes over
11 lines, sha256 `e12b310f56d03fd3…`; TO's longest line is 81 characters and no
line on either side carries trailing whitespace. The FROM was EXTRACTED from the
file rather than retyped: the reviewer's first attempt at this pair was retyped,
ended one line early, and matched zero times, which is why the span is stated as
the whole paragraph and read out of the target.

<<<PAIRG_FROM
WHAT THIS GUARDS. `tests/orchestration/test_cluster_deletion_map.py` built its
edge set from `import` statements parsed with `ast`, and DECISION F274 D2 ruled
the prototype-cluster deletion bounded by those edges. Finding R-0832 records
what that shape cannot see: a consumer coupled to a deleted module by EVENT NAME
holds no import of it, so the map correctly records no edge and the consumer
survives the deletion as dead code. R-0832's fix clause asks for a SECOND
measurement beside the map rather than a wider import walker, because a run-log
event name is a string literal and not an import.
PAIRG_FROM

<<<PAIRG_TO
WHAT THIS GUARDS. `tests/orchestration/test_cluster_deletion_map.py` built its
edge set from `import` statements parsed with `ast`, and DECISION F274 D2 ruled
the prototype-cluster deletion bounded by those edges. THAT FILE NO LONGER
EXISTS: DECISION F275 D15 retired it at round 25, together with the deletion map
and the order ratchet, once `CLUSTER_MODULES` emptied and every assertion in the
three of them quantified over nothing. Finding R-0832 records what its shape
could not see: a consumer coupled to a deleted module by EVENT NAME holds no
import of it, so the map correctly recorded no edge and the consumer survives the
deletion as dead code. R-0832's fix clause asks for a SECOND measurement beside
the map rather than a wider import walker, because a run-log event name is a
string literal and not an import.
PAIRG_TO

## SLICE LANDED39 → append to `.agent/live_review.md`, in C3

<<<LANDED39
Landed: R-0870 — the tenth and last instance the two sweeps find is repaired in C3 of F275 round 39, and the four `Landed:` lines above are left untouched because each names the batch it covers. `tests/orchestration/test_event_name_coupling.py` opened by naming `tests/orchestration/test_cluster_deletion_map.py` in the past tense without saying that DECISION F275 D15 retired it at round 25, so a reader following the path landed on nothing; the docstring now names the retirement and its decision. AFTER THIS COMMIT BOTH SWEEPS RETURN ONLY THE PATTERN THIS REPOSITORY WANTS — a sentence that names a deleted thing and says in the same breath that it is gone, a landed DECISION paragraph that records its own deletion, or a surviving symbol whose NAME collides with a deleted module stem. NOT RESOLVED HERE: the reviewer's `Done:` text is owed at the next gate, after it re-runs both sweeps itself against the committed tree.
LANDED39

## SLICE AMEND39 → append to `.agent/decisions.md`, in C4

<<<AMEND39
## DECISION F275 D21 (2026-09-10, F275 round 39) — the flip's COMPLETE measured floor: the route DECISION F275 D17 chose is unchanged, and the size it must be declared at is not

WHAT THIS AMENDS AND WHAT IT DOES NOT. DECISION F275 D17 ruled at round 31 that the
classic-to-unified flip lands as F275's ONE declared-oversize commit inside T003, and
measured it with a descriptor probe and an `ast` sweep over `Job.id` and `Job.name` alone.
Its closing clause says so in its own words: the union is "a FLOOR on the flip's size and
not a ceiling", the remainder is given "NO numeral because none was measured", and "T003
re-derives the set at its own base before it commits". This is that re-derivation, widened
to the parts D17 did not measure. D17's landed text is NOT rewritten, per
planner_reviewer_prompt.md §3 item 20; this paragraph is its dated extension.

THE MEASUREMENT, taken by the reviewer at `d341806e` over the two committed enumerations and
one `ast` pass, counting a changed line as one `(path, line)` pair so the three parts can be
unioned without double-counting. Part (a), the `.id` and `.name` sites of
`.agent/f275_t003_flip_sites.md`: 1751 lines in 184 files, 68 production and 116 test. Part
(b), the classic store seam of `.agent/f275_t003_flip_seam.md` — every call of `save_job`,
`load_job`, `load_job_safe` and `resolve_job_id`: 820 lines in 152 files, 52 production and
100 test. Part (c), the `Job` TYPE sites, re-derived here because no committed file
enumerates them — 582 constructions, 345 imports and 368 annotations: 1294 lines in 201
files, 46 production and 155 test. THE UNION IS 3771 CHANGED LINES ACROSS 263 FILES, 103
production and 160 test, with 94 lines belonging to more than one part and 79 files that
part (a) alone cannot see at all. Against the DECISION F104 D1 cap of 500 insertions per
commit, that is 7.5 times the cap, where D17's own figure implied 3.5.

CHOSEN: THE ROUTE IS UNCHANGED. One commit, declared oversize under AGENTS.md's Commit
Discipline, inside T003. The reasoning D17 gave survives the larger number intact and is not
restated here except for the part the number could have broken: AGENTS.md permits exactly
ONE declared-oversize commit per feature, and every alternative route needs two. Re-measured
rather than recalled: D17's alternative (c), renaming `JobPlan.job_id` and `JobPlan.job_title`
to `id` and `name` so that part (a) needs no edit, was measured by D17 at 1087 changed lines
and still owes parts (b) and (c) afterwards, which this decision measures together at 2114
lines minus their overlap. Two commits, each far over the cap, against one. The change also
remains atomic for the reason DECISION F272 D15 gave and this measurement does not touch:
the only way to stage it is a helper accepting both records, which AGENTS.md's Scope Control
forbids by name.

WHAT DOES CHANGE, AND IT IS THE POINT OF RECORDING THIS. The DECLARATION. AGENTS.md requires
the worker to declare an oversize commit WITH its inseparability reason in the handback
BEFORE review, and a declaration is a statement of size. The round that lands the flip
declares 3771 changed lines across 263 files, not the 1766 D17's arithmetic implied, and it
states the three parts separately so the reviewer can gate each against its own enumeration.
A declaration that understates by a factor of two is not a declaration.

WHAT IS STILL NOT ENUMERATED, stated as a bound because that is what was measured. The
classic `Job.id` is a `UUID` and the unified `JobPlan.job_id` is a 16-hex `str`, so a site
that treats a job id AS a UUID changes SHAPE and not only spelling. The reviewer measured
three token populations at this base and every one of them is a BOUND from a token
heuristic rather than a probe: `str(<job-ish>.id)` at 1337 occurrences in 150 files,
`uuid4()` at 648 in 148, and `UUID(...)` at 222 in 81. Most of the first population already
sits inside part (a), and the other two include every non-job UUID in the repository, so no
site set is claimed and none is offered. The union above is therefore still a FLOOR, and
this decision reduces the unmeasured remainder rather than closing it.

ALTERNATIVES CONSIDERED. (i) Seek an operator amendment raising or suspending the cap for
this commit — not sought, for the reason D17 gave and this measurement does not weaken: an
amendment obtained where an existing rule already provides a route weakens the rule it
bypasses, and AGENTS.md's declared-oversize route is that route. (ii) Split the flip by PART
— (a) in one commit, (b) and (c) in another — rejected on the atomicity D15 measured rather
than on size: a tree with the seam flipped and the field spellings not yet flipped is red at
that commit boundary, which every gate in this workflow exists to prevent. (iii) Land the
flip behind a temporary reader that accepts both records and remove it afterwards — rejected
by name: that is the compatibility reader AGENTS.md's Scope Control forbids, and the two
spellings of job identity are exactly what this chain of features exists to remove.

HOW TO REVERSE: delete this decision. DECISION F275 D17's route stands either way; what is
lost by deleting this is the measured size, and the flip round would then declare D17's
figure, which this measurement shows to be low by more than a factor of two.
AMEND39

## Done when — GATES G1 to G8

Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL exit code
and the real numbers. "Green" as a word is a finding. One line per gate in the
handback. Where a gate names both a COUNT and an EXIT CODE, report both.

**G1 TRANSPORT (at C0b).** The committed `.agent/authored/f275-r39.md` and
`.agent/last_block.md` have the SAME sha256 as the reviewer's delegation source,
and resolve to ONE shared git blob. `.agent/last_block.md` is written from
`git cat-file blob HEAD:.agent/authored/f275-r39.md`, never retyped. State that
the chain covers those on-disk artefacts and claims nothing about emitted bytes.

**G2 THE PLAN (at C1).** `.agent/plan.md` is BYTE-EQUAL to the PLAN39 slice as
extracted — same length, same sha256. Report its line count against the
AGENTS.md cap of 50, and `^## Goal$` and `^## Next Steps$` each exactly 1.

**G3 THE RECORD (at C2, C3 and C4).** For each of the four appends — RECORD39 and
SLIPS39 at C2, LANDED39 at C3, AMEND39 at C4 — post-blob equals pre-blob then ONE
newline then the slice, with constraint 3's baselines and each later append
re-baselining on the state the one before it left. WHERE TWO APPENDS SHARE A
COMMIT, prove the pair as ONE CHAINED RECONSTRUCTION from the last committed blob
through both slices to the next committed blob, rather than inventing an
intermediate: that is the same property and it rests on committed bytes at both
ends. READ BACK the joining byte at each offset and report it. Then an INDEPENDENT
structural reader with N COUNTED FROM EACH SLICE and not from this block. Then one
negative control per append, flipping a byte INSIDE THE FIRST appended paragraph,
which BOTH readers must REJECT. `^Gate: F275 R38 ` exactly 1 at C4 and
`^## DECISION F275 D21 ` exactly 1 at C4.

**G4 THE OPEN SET (at C4).** BY DISTINCT ID, every `^- R-\d+ — ` id minus every
`^Done: R-\d+ — ` id, read at THIS round's base `d341806e` with
`git show d341806e:.agent/live_review.md` into memory — never by writing over the
tracked file — and again at C4. Report both. Ids registered this round and ids
resolved this round must both be `[]`. Report SEPARATELY that `R-0870` IS STILL IN
the open set at C4 and carries NO `Done:` line — examined, not assumed.

**G5 PAIR G IS THE AUTHORED BYTES (at C3).** The FROM occurs EXACTLY 1x in
`tests/orchestration/test_event_name_coupling.py` before the edit and EXACTLY 0x
after; the TO occurs EXACTLY 1x after; and the applied file's post-blob equals its
pre-blob with the FROM span replaced by the TO span and nothing else, proved by
reconstructing the post-blob from the pre-blob and comparing sha256. Report the
extracted FROM's and TO's byte lengths and line counts, and report whether any
line on either side carries trailing whitespace — the reviewer measured none, and
a slice whose whitespace moved in transit would match nothing. Then
`python3 -m ruff check tests/orchestration/test_event_name_coupling.py` — the
reviewer read `All checks passed!` at exit 0.

**G6 THE SCOPED GATE (at C3).** `python3 -B -m pytest tests/orchestration/test_event_name_coupling.py -q`,
which the reviewer read at `4 passed` at exit 0 with the repair applied — the
guard's own tests, because the repair is inside the file that carries them. Then
the canary `python3 -m pytest tests/cli/test_golden_path.py -q`.

**G7 THE DECISION'S FIGURES (at C4).** Re-measure the three parts AMEND39 states,
each from the source it names, and report every figure beside the slice's:
part (a) from `.agent/f275_t003_flip_sites.md`, part (b) from
`.agent/f275_t003_flip_seam.md`, part (c) by an `ast` pass over `git ls-files
'*.py'` counting `Job(...)` constructions, `Job` imports and `Job` annotations.
Report the union of the three by `(path, line)`, the file count, the production
and test split, the lines belonging to more than one part, and the files part (a)
alone cannot see. Per constraint 8 the slice is NOT edited if a figure differs —
report both sides and say so in the handback. The reviewer's readings are the ones
AMEND39 carries.

**G8 NOTHING ELSE MOVED (at C4).** `.agent/STOP` read FROM DISK: report present
or absent. `git status --porcelain`: EMPTY. `git worktree list`: exactly ONE
entry. `git diff --name-only d341806e..C4` is an EXACT SET MATCH against the
`Change:` list above minus `.agent/handoff.md` — report MISSING and EXTRA
explicitly. Per-commit insertions for C0a through C4, each under the DECISION
F104 D1 cap of 500; the handback commit's own numbers are NOT ordered here,
per §3 item 14.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
SESSION 17 of F275 and round 39, the per-commit table with `git diff --numstat`
values in the `+/-` column, one line per gate G1 to G8 with real exit codes, the
item-status table, the open-findings count by distinct id, and the deviations.
State explicitly that R-0870 is NOT resolved, that its fix is marked `Landed:` in
C3 and that the reviewer's `Done:` text is owed at the next gate. Add the one
sentence of context self-assessment amend0905-throughput requires. No PR is
created and nothing is merged: this round is not a closure sequence.
