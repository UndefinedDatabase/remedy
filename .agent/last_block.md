── STEP T002 — F275 — ROUND 31 ──
(The rule line above is exactly 33 characters and the one at the end exactly 32;
every section divider below carries a run of exactly 8 box-drawing dashes on
each side of its title, and no line of this block is a bare run. Per §3 item 37,
which asks that a run's length be recoverable rather than eyeballed.)

Goal: Perform T002. Turn DECISION F272 D15's receiver-name BOUND on the
classic-to-unified record flip into a REAL site set by running the DECISION F272
D7 descriptor probe, and then rule, as a dated and operator-visible DECISION,
the question D15 left open: how a change that is atomic by construction lands
under a per-commit cap of 500 insertions that forbids it. T002 IS NOT THE FLIP.
No line under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moves in this
round, and a round that starts flipping sites repeats DECISION F272 D14 part 2's
mistake by name.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r31.md`
  C0b  mirror the COMMITTED C0a blob into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN31
  C2   the record: RECORD31 into `.agent/live_review.md`, SLIPS31 into
       `.agent/prose_slips.md`
  C3   build the probe and the static sweep in a disposable worktree, run the
       measurement, and write `.agent/f275_t002_flip_inventory.md`
  C4   DECISION31 into `.agent/decisions.md`
  C5   the handback

Change set — exactly these paths, nothing else:
  .agent/authored/f275-r31.md            (C0a, new file)
  .agent/last_block.md                   (C0b)
  .agent/plan.md                         (C1)
  .agent/live_review.md                  (C2, append)
  .agent/prose_slips.md                  (C2, append)
  .agent/f275_t002_flip_inventory.md     (C3, new file)
  .agent/decisions.md                    (C4, append)
  .agent/handoff.md                      (C5)

No `docs/README.md` row is owed: the one new file lives under `.agent/`, and
AGENTS.md's Documentation Updates rule registers `docs/` pages.

Constraints:
 1. Every slice is applied BYTE FOR BYTE. If a slice looks wrong, apply it anyway
    and DECLARE the doubt in the handback. Never repair a reviewer slice.
 2. Marker lines never reach a target file. Extract slices from the COMMITTED C0a
    blob, never from a retype.
 3. SLICE SHAPES, from the reviewer's own containment test, one reading per
    slice. PLAN31 is a WHOLE-FILE REPLACEMENT: `TO contains FROM: false`, and its
    proof is byte equality against the extracted slice, not a count. RECORD31,
    SLIPS31 and DECISION31 are APPENDS into append-only records; no FROM-zero
    count is ordered for any of them, and their proof is the §4.9 append
    obligation under G3.
 4. EVERY ONE of RECORD31, SLIPS31 and DECISION31 is a WHOLE-LINE slice, so each
    OWNS its terminating newline and the extractor's trailing newline IS content.
    This block ships no mid-line slice, which is the distinction round 30's W1
    turned on.
 5. `.agent/STOP` is re-read FROM DISK before the FIRST commit and again before
    C3.
 6. The probe, the static sweep and every suite run happen ONLY inside a
    disposable `git worktree` under the gitignored `.remedy-wt/`, never in the
    primary checkout, per self_drive_protocol G5. Neither instrument is ever
    committed as a file; their SOURCE is embedded in the inventory at C3 so the
    measurement is reproducible. Remove and prune the worktree before C5.
 7. Commit subjects carry NO leading-slash token or absolute path. C3's and C4's
    subjects name T002.
 8. No file outside the change set is edited, and no test is deleted, skipped or
    weakened to make a gate green.
 9. Do not re-verify rounds 27 through 30.
10. THE TWO R27 PROSE SLIPS DRAFTED IN `.agent/handoff.md` ARE ALREADY ON DISK
    AND ARE NOT BOOKED AGAIN. The reviewer compared the four drafted lines
    against `.agent/prose_slips.md` at `0b009325` mechanically: the two R27
    drafts each have a counterpart already present sharing their first fifty
    characters and differing later in wording, and the R29 and R30 drafts have
    none. SLIPS31 therefore carries the R29 and R30 lines and a third line
    recording this, and booking all four would have duplicated a landed lesson.

──────── WHAT THE REVIEWER ALREADY MEASURED, by RUNNING all of it ────────

Every numeral below was produced at the base `0b009325` in a disposable worktree
by APPLYING the instruments this block specifies, not by reading code. They are
the numbers the gates re-derive. Where the worker's run differs, the worker
reports ITS number and DECLARES the difference; a difference is a result, not a
failure, and G7 exists to capture it.

THE INSTRUMENT WORKS AND IS BEHAVIOUR-NEUTRAL. With all four descriptors
installed, `python3 -B -m pytest tests/ -q` in the worktree exits 0 at 18350
passed and 23 skipped, in about 21 minutes. Both facts were earned rather than
assumed, and each cost a correction:

  (a) A GETTER-ONLY property is WRONG. `Job` is a pydantic model whose
      `model_config` sets no `validate_assignment`, so assignment writes
      straight through to `__dict__`; a property with no setter instead raises
      `AttributeError: can't set attribute` at every write site. Measured: with
      a getter-only probe, `tests/orchestration/test_test_execution_service.py`
      goes RED at exactly two tests — `TestExecuteTestRunGates::
      test_concurrent_run_blocked` and `TestCatalogValidation::
      test_lease_blocked_next_action_references_catalog_command` — which are
      GREEN both without the probe and with the both-halves probe. A probe that
      reddens a test measures a SMALLER set than the truth, because the test
      dies before reaching its remaining sites.
  (b) A FIXED FRAME DEPTH mis-attributes every WRITE. Pydantic dispatches
      assignment through its own `__setattr__` and a lambda, so the caller two
      frames out is `pydantic/main.py`, not the line that performed the write.
      Measured: under a fixed depth the only write the suite executes is
      attributed to `pydantic/main.py:1089`; under the outward walk this block
      specifies it is attributed to
      `tests/orchestration/test_test_execution_service.py:577`, which is where
      `job.id = job_id` really is.

THE SITE SET, at `0b009325`. A site is one `(path, line, field)` triple; a
changed line is one `(path, line)` pair, and the two differ only where one line
carries two fields.

  ROUTE-B SET — reads and writes of `Job.id` and `Job.name`:
    probe, executed by the suite      1757 sites / 1755 lines
                                      349 production in 68 files
                                      1406 test in 115 files
    static, provably `Job`             325 sites / 325 lines
    UNION, the ruled site set         1768 sites / 1766 lines
                                      357 production in 68 files
                                      1409 test in 117 files
    provably `Job` but never executed    11
    executed but not statically provable 1443

  THE REST OF THE SAME ATOMIC COMMIT, by `ast` over 991 tracked `.py`:
    `Job(...)` constructions           586   production 12   test 574
    `Job` imports                      346   production 47   test 299
    `Job` annotations                  374   production 155  test 219

  THE ALTERNATIVE ROUTE'S SET — reads and writes of `JobPlan.job_id` and
  `JobPlan.job_title`, measured in the SAME run because one probe can carry four
  descriptors:
                                      1201 sites / 1087 lines
                                      109 production in 9 files
                                      978 test in 61 files

WHY THE UNION AND NOT THE PROBE ALONE. A descriptor probe sees exactly what the
suite EXECUTES, which is the blindness `.agent/live_review_archive.md` records
against R-0822: a site no test reaches cannot raise and cannot record. The
static sweep supplies the other side, and the two disagree in BOTH directions —
11 sites are provably `Job` and never executed, while 1443 executed sites no
static rule can attribute, of which the sweep calls 92 something OTHER than
`Job`. That second number is the one that settles the method question: a static
selection would have silently EXCLUDED 92 real sites and left the tree red, which
is precisely the failure DECISION F272 D7 was written after. What neither
instrument sees is a site that is both unexecuted and unprovable; that remainder
is named in DECISION31 as a limit and is deliberately given no numeral.

THE TWO FACTS THE ROUTE RULING TURNS ON, both measured rather than inherited:

  (i) F275'S ONE DECLARED-OVERSIZE ALLOWANCE IS UNSPENT. Walking
      `a5bf8949..0b009325` commit by commit and summing the insertion column of
      `git diff --numstat`, ZERO commits on this branch exceed 500 insertions.
 (ii) THE MANDATED CLOSURE ROTATION DOES NOT NEED THAT ALLOWANCE, contradicting
      the "by construction" clause of DECISION F272 D18 at F275's size.
      `python3 scripts/rotate_live_review.py` applied in a worktree moves 23
      gate records and 13 finding pairs and produces a diff of 106 insertions
      against 106 deletions — far under the cap. So the flip and the closure do
      not compete for the one allowance, and no operator amendment is owed for
      that collision.

AN ASIDE THAT IS MEASURED, NOT ASSUMED, and that spends no id. That same script
prints `open findings before: 85` where the ledger's own convention reads 87.
The difference is exact and benign: the script subtracts `Done:` LINES from
registration LINES, and `R-0721` and `R-0725` each carry TWO `Done:` records
while `R-0831` carries a second registration-shaped line that its em-dash
pattern excludes. As an INVARIANT — identical before and after — the script's
reading is sound, and the count it prints is simply a different reading from the
one this workflow books. G4 records both so the next session does not rediscover
it.

──────── PLAN31 — the whole of `.agent/plan.md` ────────

<<<BEGIN PLAN31>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 31 performs T002. The DECISION F272 D7 descriptor probe is run over both records the
flip spans, in one suite run, turning DECISION F272 D15's receiver-name bound into a measured
site set. The inventory records that set and the instruments that produced it; DECISION F275
D17 rules the route by which an atomic change lands under a per-commit cap that forbids it.
No production line moves in this round.

## Next Steps

1. T003, the classic runner and the classic store, which DECISION F275 D17 makes landable and
   which the T003 paragraph of the feature file scopes. The flip itself lands there, as the
   one declared-oversize commit AGENTS.md permits per feature, with its inseparability reason
   stated in the handback BEFORE review.
2. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- The open set is 87 by distinct id at this round's base `0b009325`, over 102 registrations
  against 15 resolutions. This round registers none and resolves none, so it stays 87. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per
  DECISION F272 D12.
- The flip is the largest single commit this repository will have taken. Its size is now
  measured rather than bounded, and the route is ruled, but T003 still has to land it.
<<<END PLAN31>>>

──────── RECORD31 — appended to `.agent/live_review.md` ────────

<<<BEGIN RECORD31>>>
Gate: F275 R30 — the F275 round 30 entry. VERDICT PASS, written by the planner and reviewer of session 14 after reading the committed range `fa2279da`..`c88fbca6` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Seven single-parent commits, per-commit insertions 420, 345, 15, 18, 5 and 108 for the six before the handback, every one under the DECISION F104 D1 cap of 500. G1: the reviewer's scratch original and both committed copies are 32134 bytes at `b3e08e81191c32743b217230af6b5d5f317c3dc81a9ad78b6a38c6b4fa8ff44d` and compare BYTE-EQUAL. G2: `.agent/plan.md` byte-identical to PLAN30 at 2050 bytes and 39 lines against the cap of 50. G3 over BOTH append targets: `.agent/live_review.md` 783650 to 790277 and `.agent/decisions.md` 1012375 to 1017073, each post-blob equal to its pre-blob then ONE newline then the slice, the joining byte READ BACK at offset len(pre) and reading a newline in both, the structural reader counting N from each slice — 2 and 7 paragraphs — and matching the last N blank-line units IN ORDER, with both negative controls flipped INSIDE THE FIRST appended paragraph and REJECTED by BOTH readers. THE OPEN SET FELL 88 TO 87 BY DISTINCT ID. G5 is the gate the round existed to pass: the committed blob of `tests/docs/test_named_source_paths.py` and the GUARD30 slice are both 4774 bytes at one sha256 and compare BYTE-EQUAL, and through the reviewer's OWN import `collect_named_source_paths()` reads 244 paths named and an EMPTY missing list. G6 was re-run in the reviewer's own disposable worktree and all three mutations bite: reinstating a deleted module path goes RED, emptying the corpus goes RED on the anti-blindness floor rather than passing silently with zero findings, and reversing the extension alternation so `.tsx` reads as `.ts` goes RED — that third one guarding the FALSE MISS direction, which is the opposite of the other two and is why the round ordered it. G7: `tests/docs/ tests/cli/` GREEN at 1651 passed run serially in the primary checkout, being round 29's 1648 plus exactly the three tests the new file adds; the shipped catalog UNCHANGED at 222 commands, 44 groups and ZERO dangling `related=` references; the advertisement guard still reading ZERO unresolved on BOTH corpora; no `.agent/STOP`, porcelain EMPTY, ONE worktree, and `fa2279da..c88fbca6` an EXACT set match over ten paths. THE WORKER'S FIRST DEVIATION IS A REVIEWER ERROR AND WAS RE-MEASURED RATHER THAN ACCEPTED: W1's FROM span ends MID-LINE while the block's extractor appends a terminating newline, so W1's FROM as extracted occurs ZERO times in `docs/system/vocabulary.md` and the same span without that newline occurs exactly once; the worker stripped one terminal newline from W1's FROM and its TO, applied every other slice verbatim, and declared it, which is the minimal correct repair and is sustained.
<<<END RECORD31>>>

──────── SLIPS31 — appended to `.agent/prose_slips.md` ────────

The blank line between entries is part of this file's record format, so this
slice is three paragraphs separated by single blank lines and G3's structural
reader counts N from the slice itself.

<<<BEGIN SLIPS31>>>
2026-09-10 · F275 R29 · The round 29 block's rename table gave a bracketed occurrence count for each of its 22 mappings, and those counts were POST-V1 readings — taken after the sentence V1 rewrites had been masked out — while the block never said so. The worker measured `remedy create-job` at 2 before V1 and 1 after, reported both, and declared the difference rather than quietly reconciling to the bracket. A count a block states about a file is a reading taken at a moment, and the block has to name the moment when its own ordered edits move it.

2026-09-10 · F275 R30 · The round 30 block's W1 slice was a MID-LINE span, and the block's marker convention appends a terminating newline to every extracted slice, so W1's FROM as extracted occurred ZERO times in its target while the same span without that newline occurred once. The reviewer's dry run never met the distinction because it used a Python literal with no trailing newline, so the applied run and the emitted slice differed in exactly the byte the recipe turns on. The lesson is that a slice's terminal byte is part of the slice: a whole-line FROM owns its newline and a mid-line FROM does not, and a block that ships both shapes says which is which.

2026-09-10 · F275 R31 · Session 14's handoff drafted four prose slips for round 31 to book, and TWO of them were already on disk: both R27 lines had been appended by the round they describe, and the drafts were re-wordings rather than new entries. The reviewer caught it only by comparing the drafted lines against `.agent/prose_slips.md` mechanically before authoring, which §3 item 34 requires of every file a block orders a change against and which the drafting session had not done for its own carrier. A durable carrier is a place text WAITS, not a place text has necessarily not landed, so a booking round reads its target before it appends.
<<<END SLIPS31>>>

──────── DECISION31 — appended to `.agent/decisions.md` ────────

<<<BEGIN DECISION31>>>
## DECISION F275 D17 (2026-09-10, F275 round 31) — the classic-to-unified flip is measured over BOTH records by one descriptor probe, and it lands as F275's ONE declared-oversize commit inside T003

CONTEXT. DECISION F272 D15 ruled the classic-to-unified record flip ATOMIC and bounded it with a receiver-name heuristic at 468 `<job-ish>.id` reads in 74 production files and 1545 in 137 test files over 1068 tracked `.py`, recording in its own terms that this is an UPPER BOUND and NOT a probe measurement because `.id` is polymorphic in this repository exactly as `.status` was. Its CONSEQUENCE clause left one question that neither F272 nor F274 answered: how is a change that is atomic by construction landed under a per-commit cap of 500 insertions that forbids it. F275's T002 orders the DECISION F272 D7 probe over every candidate receiver and then a dated ruling on the route. This is that measurement and that ruling. No production line moves in the round that records it.

THE INSTRUMENT, and the two ways it was wrong before it was right. D7 established that a polymorphic attribute's site set is settled by RUNTIME PROBE and never by static classification, because only a running object knows its own type. D7's disposition was a RAISING property, which suits a rename being PERFORMED and converges by iteration; a rename being SIZED needs the sites ENUMERATED in one pass, so this round installs the same class-level data descriptor in a RECORDING disposition — it attributes the access to the calling frame and returns the real value. Two corrections were forced by running it. FIRST, a getter-only property is wrong: `Job` is a pydantic model with no `validate_assignment`, so assignment writes through to `__dict__`, and a property with no setter raises `AttributeError: can't set attribute` at every write site — measured, it turned exactly two tests of `tests/orchestration/test_test_execution_service.py` red, and a probe that reddens a test measures a smaller set than the truth because the test dies before reaching its remaining sites. SECOND, a fixed frame depth mis-attributes every write, because pydantic dispatches assignment through its own `__setattr__` and a lambda: the sole executed write reads as `pydantic/main.py:1089` at a fixed depth and as `tests/orchestration/test_test_execution_service.py:577` under an outward walk to the innermost repository frame. With both corrections the full suite is GREEN under the probe at 18350 passed and 23 skipped, so the instrument distorts nothing it measures.

THE MEASUREMENT, taken at `0b009325`. Counting a site as one `(path, line, field)` triple: the probe executes 1757 `Job.id`/`Job.name` sites, and an `ast` sweep over 991 tracked `.py` files proves 325 more-or-less independently; their UNION, which is the set this ruling uses, is 1768 sites over 1766 distinct changed lines — 357 in production across 68 files and 1409 in tests across 117 files. Beside those, the same atomic commit carries 586 `Job(...)` constructions, 346 `Job` imports and 374 `Job` annotations. The two instruments disagree in BOTH directions and that is the method's whole point: 11 sites are provably `Job` and never executed, while 1443 executed sites no static rule attributes, of which the sweep positively calls 92 something OTHER than `Job`. A static selection would therefore have EXCLUDED 92 real sites and left the tree red at a commit boundary, which is the failure R-0820 recorded and D7 was written after. The bound D15 stated is confirmed as a bound and replaced: the honest figure is larger in tests than D15's reachable guess and smaller in production, and it is now a list rather than an estimate.

CHOSEN. THE FLIP LANDS AS ONE COMMIT, DECLARED OVERSIZE UNDER AGENTS.md'S COMMIT DISCIPLINE, INSIDE T003 AND NOT IN A ROUND OF ITS OWN. Three facts fix this. The change is atomic — D15 ruled it so, the only way to stage it is a helper accepting both records, and AGENTS.md's Scope Control forbids precisely that with no attic, no deprecated alias and no compatibility reader — so every intermediate commit of any split is RED, which no rule here permits. The allowance exists and is FREE: walking `a5bf8949..0b009325` and summing the insertion column, ZERO commits on this branch exceed 500 insertions, and the DECISION F274 ruling that reserved F275's one allowance for exactly this flip is honoured rather than spent elsewhere. And the allowance is NOT contested by the closure, contradicting the "by construction" clause of DECISION F272 D18 at this feature's size: `scripts/rotate_live_review.py` applied in a worktree moves 23 gate records and 13 finding pairs for a diff of 106 insertions, so the mandated rotation needs no exception at all. The commit is placed inside T003 because T003 deletes the classic store and runner that PRODUCE `Job`, the feature file already makes this ruling T003's prerequisite, and a flip landing anywhere else would be a change with no consumer waiting for it.

ALTERNATIVES CONSIDERED, each rejected on a measurement rather than a preference. (a) One commit under the cap — impossible: 1766 changed lines before constructions, imports and annotations is more than three times 500, and no reading of the cap reaches it. (b) An operator amendment raising or suspending the cap — not sought, because AGENTS.md already provides the declared-oversize route and an amendment obtained where an existing rule applies weakens the rule it bypasses. (c) RENAME `JobPlan.job_id` AND `JobPlan.job_title` TO `id` AND `name` FIRST, so both records agree and the 1721 `.id` reads need no edit at all. This was measured in the SAME probe run rather than argued about — one probe carries four descriptors — and it is the alternative that came closest: `JobPlan`'s two fields are read and written at 1201 executed sites over 1087 distinct lines, and the record's persisted format is decoupled from its field names by explicit `_export_job`/`_import_job` functions rather than `asdict`, so the rename would not touch a single job file on disk. It is rejected on arithmetic: 1087 lines is itself far over the cap, so this route spends TWO oversize commits where AGENTS.md permits ONE per feature, and it buys a smaller flip at the price of a rule violation the first route does not need. If the operator ever permits two, this is the better route and it is recorded here in enough detail to be taken.

WHAT THIS RULING DOES NOT SETTLE, stated because a measurement's limits are part of its result. A descriptor probe sees what the suite EXECUTES and a static sweep sees what a reader can PROVE; a site that is both unexecuted and unprovable is invisible to both, and this ruling gives that remainder NO numeral because none was measured. The union is therefore a floor on the flip's size and not a ceiling, and T003 re-derives the set at its own base before it commits rather than inheriting these figures — every count here names `0b009325`, and the tree moves between now and then. The declared-oversize commit's inseparability reason is owed in T003's handback BEFORE review, per AGENTS.md, and this decision does not discharge that obligation in advance.

HOW TO REVERSE. Delete this paragraph and the ruling above it; the measurement paragraphs are a record of what was run and stay true whatever route is later chosen. Reversing the route without reversing the measurement means choosing (c) above, which requires the operator to permit a second oversize commit in this feature and nothing else.
<<<END DECISION31>>>

──────── SPEC-PROBE — the instrument C3 builds, runs and embeds ────────

The worker builds this in the disposable worktree. It is NOT committed as a
file; its exact source is embedded in the inventory. Behaviour required:

 (a) A pytest plugin module at the worktree root, loaded with `-p <name>`. The
     repository's `pyproject.toml` sets `pythonpath = ["."]`, so a root-level
     module is importable that way.
 (b) On import it installs a class-level `property` over FOUR fields: `id` and
     `name` on `packages.core.models.Job`, and `job_id` and `job_title` on
     `packages.orchestration.pingpong_job.JobPlan`.
 (c) Each property carries BOTH a getter and a setter. The getter records the
     access and returns `self.__dict__[<field>]`. The setter records the access,
     writes `self.__dict__[<field>] = value`, and — for the pydantic model only
     — adds the field name to `self.__pydantic_fields_set__`, which is what
     pydantic's own no-`validate_assignment` path does. A getter-only property is
     the defect measured above and may not be shipped.
 (d) Recording attributes the access to the INNERMOST STACK FRAME WHOSE FILENAME
     LIES UNDER THE WORKTREE ROOT, walking outward from the caller, falling back
     to the innermost frame of all when no frame qualifies. It records whether
     the innermost frame already qualified, so attributed and direct accesses
     stay distinguishable.
 (e) The record key is `(owner, field, mode, direct, repo-relative path, line,
     function)` where mode is `read` or `write`; the value is the access count.
 (f) At `pytest_sessionfinish` every record is written as JSON.

──────── SPEC-STATIC — the second instrument, same treatment ────────

An `ast` reading over every tracked `.py` from `git ls-files '*.py'` — enumerated
from git and never from a shell glob, per DECISION F272 D2. Per function scope it
binds each local NAME to a verdict on whether it holds a `Job`: `job` when a
parameter annotation, an `AnnAssign` annotation or an assignment from a `Job(...)`
call names `Job`; `other` when an annotation names something else; `unknown`
otherwise. It then records every `Attribute` node whose `attr` is `id` or `name`
and whose `value` is a bare `Name`, carrying that name's verdict, the path, the
line and whether the context is a load or a store.

──────── SPEC-INVENTORY — `.agent/f275_t002_flip_inventory.md` ────────

Generated from the two runs, never retyped. It carries, in this order: the base
SHA the measurement was taken at; the full source of BOTH instruments; the pytest
summary line and exit code of BOTH probe runs; the reproducibility comparison G6
orders; the route-B table and the alternative-route table in the shapes given
above; the two set differences with `provably Job but never executed` enumerated
BY PATH AND LINE IN FULL, since it is small enough to list and a count alone
would hide which sites they are; and the constructions, imports and annotations
counts. Every figure DECISION31 also states appears here beside the reviewer's
reading of it and a `same` or `differs` verdict.

──────── Done when ────────

Done when — the gates below, G1 to G8, at the amend0827 rule 5 budget of eight.
Each is run with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, with real exit codes and
real numbers in the handback, ONE LINE PER GATE. G1 to G7 are ordered at commits
strictly before C5, per §3 item 31.

G1 TRANSPORT (at C0b). `sha256sum` of the scratch original at
   `.remedy-wt/f275-r31-block.md`, of the committed `.agent/authored/f275-r31.md`
   and of the committed `.agent/last_block.md` are ONE comparison and must be
   equal.

G2 THE PLAN (at C1). `.agent/plan.md` byte-identical to PLAN31; report
   `written == slice`. Line count under the AGENTS.md cap of 50. `^## Goal$` and
   `^## Next Steps$` each exactly 1.

G3 THE RECORD, full byte forensics, THREE append targets — `.agent/live_review.md`
   and `.agent/prose_slips.md` at C2, `.agent/decisions.md` at C4. Pre-sizes at
   `0b009325` are 790277, 215418 and 1017073 bytes. For EACH: post == pre + ONE
   newline + slice, with the joining byte READ BACK from the committed post-blob
   at offset len(pre) and shown to be a newline; plus an INDEPENDENT structural
   reader comparing the LAST N blank-line units against the slice's N paragraphs
   IN ORDER, N COUNTED BY THE SCRIPT from the slice and never taken from this
   block; plus a negative control flipping one byte inside the FIRST appended
   paragraph, which BOTH readers must REJECT while both accept the truth. Then
   `^Gate: F275 R30 ` == 1 and `^## DECISION F275 D17 ` == 1.

G4 THE OPEN SET (at C4, after every record commit). BY DISTINCT ID it reads 87 at
   the base `0b009325`, over 102 distinct registered ids against 15 distinct
   resolved ids; this round registers none and resolves none, so it must still
   read 87. Report BESIDE it the reading `scripts/rotate_live_review.py` prints,
   which is 85, and the reason the two differ — that reading subtracts `Done:`
   LINES from registration LINES while `R-0721` and `R-0725` each carry two
   `Done:` records and `R-0831` carries a second registration-shaped line.

G5 THE PROBE IS BEHAVIOUR-NEUTRAL (at C3, in the disposable worktree). The full
   suite under the probe, `python3 -B -m pytest tests/ -q -p <name>`, run
   SERIALLY. Report the summary line and the real exit code. IT MUST BE GREEN;
   the reviewer measured 18350 passed and 23 skipped at exit 0. Independently of
   whether anything fails, re-run the golden-path canary
   `pytest tests/cli/test_golden_path.py -q` and report it. For ANY test that
   fails under the probe, re-run THAT node id WITHOUT `-p` and report both
   colours: a test red under the probe and green without it is a PROBE DEFECT,
   and the round stops and declares it rather than reporting the smaller site set
   the broken probe produced.

G6 THE MEASUREMENT REPRODUCES (at C3). Run the full suite under the probe a
   SECOND time and compare the two site sets as sets of
   `(owner, field, mode, path, line, function)`. Report the size of each set and
   the FULL symmetric difference, never truncated and never summarised as a
   count alone. Determinism is measured here, not assumed: the reviewer observed
   the same 1757 `Job` sites across two runs whose pytest skip counts differed,
   so a non-empty difference is a real result to record in the inventory rather
   than a failure of the round.

G7 THE INVENTORY'S NUMERALS ARE THE RUN'S (at C3, before C4). Every figure in
   `.agent/f275_t002_flip_inventory.md` is produced by the two instruments and
   none is retyped from this block. For each figure DECISION31 also states,
   report `same` or `differs` against the reviewer's reading, and DECLARE every
   difference with the number you measured. A difference does not stop the round;
   an undeclared one is a finding.

G8 NOTHING ELSE MOVED (at C4, before C5).
   - `.agent/STOP` absent (read from disk), `git status --porcelain` EMPTY,
     `git worktree list` exactly ONE entry after the pruning constraint 6
     requires, branch correct.
   - `git diff --name-only 0b009325..<C4>` an EXACT SET MATCH against the change
     set minus `.agent/handoff.md`; report MISSING and EXTRA explicitly.
   - No path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` appears
     in that diff at all, which is T002's own "no production line moves".
   - Per-commit insertions for every commit BEFORE the handback commit, against
     the DECISION F104 D1 cap of 500.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
feature and round, SESSION 15 of F275, branch, per-commit changed-files table
with `+/-` from `git diff --numstat` and not from file line counts (§3 item 28),
one line per gate G1 to G8, every deviation declared, the open-findings count,
the one-sentence context self-assessment amend0905-throughput requires, and the
next expected action. State plainly whether the probe reproduced across the two
runs, because that is the property T003 will rely on.
── END STEP T002 — F275 — R31 ──
