── STEP T003 / F275 — ROUND 43 — the flip's last measurement, and the record pair it closes ──

Goal:
  DECISION F275 D22 found, one round before the widen, that the two TASK records share two
  field names of seven and twenty-three, and it reached that by IMPORTING both shipped
  classes instead of reading DECISION F272 D15's sentence about them. Nobody has run that
  same reading for the JOB records, which is the pair the flip actually moves. This round
  runs it, together with the shape readings a name comparison cannot give, and records the
  result as DECISION F275 D24. No production line moves.

  The answer is the one the flip needed and nobody had: the JOB pair is CLEAN. `Job`
  declares 15 fields and `JobPlan` 65, they share 13 names, and the only two `Job`-only
  names are `id` and `name` — the two renames this chain has tracked since F272. There is
  NO third unmeasured record pair, so F272 D15's sentence holds for the JOB record exactly
  where D22 disproved it for the TASK record.

Bundle:
  C0a  save this block verbatim as `.agent/authored/f275-r43.md`
  C0b  mirror that file into `.agent/last_block.md`
  C1   the plan — slice PLAN43, whole-file replacement
  C2   the record — slices RECORD43, SLIPS43 and DECISION43, three appends
  C3   the measurement artefact — run the INSTRUMENT43 slice and commit what it printed
  C4   the handback

Change: exactly these paths and nothing else.
  .agent/authored/f275-r43.md              (new, C0a)
  .agent/last_block.md                     (C0b)
  .agent/plan.md                           (C1)
  .agent/live_review.md                    (C2)
  .agent/prose_slips.md                    (C2)
  .agent/decisions.md                      (C2)
  .agent/f275_t003_record_shapes.md        (new, C3)
  .agent/handoff.md                        (C4)

NO PATH UNDER `packages/`, `apps/`, `tests/`, `docs/` OR `scripts/` MOVES IN THIS ROUND.
It is a measurement, exactly as rounds 36, 38, 39 and 40 were, and it flips nothing.

HOW C3 IS BUILT, and why it is built this way. The artefact is MACHINE-GENERATED: you
extract the INSTRUMENT43 slice from the committed `.agent/authored/f275-r43.md`, run it,
and paste what it printed. You do not retype a figure and you do not edit one. Write the
file as exactly three parts in this order:

  1. the BANNER43 slice, verbatim — it ends with the heading `## The instrument`;
  2. a line reading ```python, then the INSTRUMENT43 slice verbatim, then a line reading ```;
  3. a blank line, then a line reading `## What it printed`, then a blank line, then a line
     reading ```, then the instrument's CAPTURED STDOUT verbatim, then a line reading ```.

Nothing else goes in the file: no commentary of your own, no summary of the output, and no
figure retyped outside the captured block. The artefact is the banner, the instrument and
what the instrument said.

Run the instrument WITHOUT writing it to a tracked file, by piping the extracted slice to
the interpreter's standard input — in Python,
`subprocess.run([sys.executable, "-"], input=<the slice bytes>, capture_output=True,
cwd="/home/decodeux/Repos/remedy")`. Its `REPO` constant is `"."`, so the working
directory is what decides which tree it measures, and it must be the primary checkout.

THE FIGURES THE RUN MUST REPRODUCE. The reviewer ran this exact instrument at `7f8724c3`
before authoring this block. Report each of these as reproduced or as differing, and if one
differs, report YOUR number and do not edit the instrument to chase it — a difference is a
reading, not a fault.

  the JOB pair       `Job` 15 fields · `JobPlan` 65 · shared 13 · `Job`-only 2 · ORPHANS 0
  `created_at`       6 accepted sites, 4 production and 2 test, every one `.isoformat()`
                     6 rejected sites, which are project records and one proposal
  `budget`           1 dereference site, production, already guarded by `if job.budget`
  `Job` type sites   582 constructions · 345 imports · 367 annotations · 1294 lines ·
                     201 files · 46 production · 155 test
  `Task` type sites  246 constructions · 142 imports · 40 annotations · 428 lines ·
                     112 files · 15 production · 97 test
  the two unioned    1583 lines in 208 files, overlap 139

TWO OF THOSE FIGURES DISAGREE WITH A LANDED DECISION, and the disagreement is the point of
reporting them rather than a reason to hide them. DECISION F275 D21 records its part (c) at
582, 345 and 368 over 1294 lines in 201 files, 46 production and 155 test: every figure
reproduces EXCEPT the annotation count, where this instrument reads 367, and the UNION is
identical at 1294 — which is what you would see if one annotation shares a `(path, line)`
with a construction or an import. DECISION F275 D22 records the `Task` sites at 246, 142
and 40 over 427 lines in 111 files, 15 production and 96 test: the three component counts
reproduce EXACTLY and the union reads one line and one file higher. The reviewer re-ran the
instrument in a disposable worktree at `6537ece6`, D22's OWN base, and read 428 and 112
there too, so the difference is in the union arithmetic of that decision and not in the
tree having moved. DECISION43 records this; no landed text is rewritten.

Constraints:
  1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Extract each one MECHANICALLY by its
     `BEGIN-`/`END-` marker lines from the COMMITTED `.agent/authored/f275-r43.md`, read
     with `git cat-file blob`, and apply it by file write or byte concatenation in Python.
     Never retype a slice, never reflow one, and never edit one even where you believe it
     wrong — declare it instead. A marker line is never part of a slice's content.
  2. AN EOF-APPEND IS PURE CONCATENATION. Each append slice's content already begins with
     the blank line that separates it from what precedes it, so the operation is exactly
     `old_bytes + slice_bytes` with nothing inserted between them. Every target named in C2
     ends with a newline at this round's base; do not add one.
  3. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and nothing is reordered, merged or
     added. C1 precedes C2 because the plan must be current before the round touches the
     finding ledger (planner_reviewer_prompt.md §3 item 23).
  4. THE CHANGE SET IS EXACTLY THE PATHS the Change list names. Nothing else is touched,
     created or deleted, and no tracked file holds the instrument.
  5. THIS ROUND REGISTERS NO FINDING AND RESOLVES NONE. The open set is 86 by distinct id
     at this base and 86 at C3. The next free id is R-0875 and it stays free.
  6. NEVER `cd` INTO A WORKTREE, for any purpose. This round needs no worktree at all; if
     you create one, address its files by ABSOLUTE path, run commands with
     `subprocess.run([...], cwd=<abs worktree>)`, and remove and prune it before C4.
  7. RUN `python3 -m pytest`, never bare `pytest`. The `remedy` console script is
     sandbox-blocked in these sessions; if a CLI reading is needed use
     `python3 -m apps.cli.grouped <group> <cmd>` and say which form you ran.
  8. THIS BLOCK IS CAPPED AT 490 LINES TOTAL AND 400 LINES OF PROSE, where PROSE is TOTAL
     minus the summed content lines of every slice and the marker lines count as prose
     (DECISION F085 D6 and D5). Measure BOTH from the committed
     `.agent/authored/f275-r43.md` blob, report both, and say plainly if either is
     exceeded. Do not fix an overage — declare it.
  9. READ `.agent/STOP` FROM DISK before the first commit and again before C3. If it
     exists, finish the commit in hand, write the handback and stop.

Done when: six gates. Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the real
exit code and the real numbers — one line per gate in the handback. Every gate's reading is
taken at a commit EARLIER than C4, the commit that writes the handback.

  G1  TRANSPORT, at C0b. `.agent/authored/f275-r43.md` and `.agent/last_block.md` have the
      SAME sha256 and the same byte count, and the mirror was written from
      `git cat-file blob <C0a>:.agent/authored/f275-r43.md` rather than retyped. Report both
      digests and the byte count. This covers the two committed artefacts and claims nothing
      about the bytes emitted into your prompt (planner_reviewer_prompt.md §3 item 37).
  G2  THE PLAN, at C1. `.agent/plan.md` is BYTE-EQUAL to the PLAN43 slice as extracted;
      report its byte count, its sha256, its line count against the AGENTS.md cap of 50, and
      the count of `^## Goal$` and `^## Next Steps$`, each of which must read exactly 1.
  G3  THE RECORD, at C2, for EACH of the three appends, against COMMITTED blobs only — pre
      at C1 and post at C2, read with `git show <rev>:<path>`.
      (a) Reader A, bytes: the post blob EQUALS the pre blob followed by the slice, exactly,
          with nothing between them. Report pre bytes, slice bytes, post bytes and whether
          the reconstruction is identical.
      (b) Reader B, structural: count N as the number of blank-line-separated paragraphs IN
          THE SLICE — count it, do not take a number from this block — then compare the LAST
          N such paragraphs of the post blob against the slice's N paragraphs IN ORDER.
          COMPARE THEM WITH THEIR LEADING AND TRAILING WHITESPACE STRIPPED: constraint 2 puts
          the separating blank line inside the slice, so the slice's first paragraph owns a
          leading newline the post blob spends as a separator, and a raw comparison therefore
          reads FALSE on correct bytes. Round 42 measured exactly that and declared it.
      (c) A negative control per append: flip ONE byte inside the FIRST appended paragraph
          and confirm that BOTH readers REJECT it. Report four outcomes per append: A and B
          on the true bytes, A and B on the control.
      (d) `^Gate: F275 R42 ` reads 0 at C1 and exactly 1 at C2; `^## DECISION F275 D24 `
          reads 0 at C1 and exactly 1 at C2.
      Where a formula in this block and the ORDERED OPERATION disagree, the operation wins
      and you declare the disagreement.
  G4  THE OPEN SET, at C3. By DISTINCT ID: the count of distinct ids matching `^- R-\d+ — `
      minus the count of distinct ids matching `^Done: R-\d+ — `, read from
      `git show <rev>:.agent/live_review.md` into memory and never by writing over the
      tracked file. Report the three numbers at this round's base `7f8724c3` and again at C3,
      plus the list of ids registered this round and the list resolved. Both lists must be
      empty and both readings must be 86.
  G5  THE ARTEFACT IS WHAT THE INSTRUMENT PRINTED, at C3.
      (a) The INSTRUMENT43 slice as extracted from the committed authored file appears
          BYTE-IDENTICALLY inside `.agent/f275_t003_record_shapes.md`: report the slice's
          sha256 and the sha256 of the region you pasted, and state that they match.
      (b) Re-run the instrument a SECOND time and compare its stdout to the stdout already
          in the file, byte for byte. Report whether the two runs agree. A difference here
          means the instrument is not deterministic and is a reading to declare, not to
          smooth over.
      (c) Report, one line each, every figure in the block's reproduction table as
          `reproduced` or as `differs, mine reads <x>`.
      (d) `python3 -m pytest tests/cli/test_golden_path.py -q` is green — the canary every
          handback owes. No wider suite is ordered, because no line under `packages/`,
          `apps/` or `tests/` moves this round.
  G6  NOTHING ELSE MOVED, at C3. `.agent/STOP` read FROM DISK is ABSENT.
      `git status --porcelain` is EMPTY. `git worktree list` reads exactly ONE entry.
      `git diff --name-only 7f8724c3..<C3>` is an EXACT SET MATCH against the Change list
      minus `.agent/handoff.md`: report the MISSING set and the EXTRA set, both of which must
      be empty. Report ZERO paths under `packages/`, `apps/`, `tests/`, `docs/` or
      `scripts/`. Report each commit's INSERTION count for C0a, C0b, C1, C2 and C3 against
      the AGENTS.md DECISION F104 D1 cap of 500 insertions; C4's own numbers are not ordered
      here, because its text cannot count itself.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, carrying the
mandated sections — the state block with the SESSION NUMBER of this feature, the range, a
per-commit changed-files table with a reason per path, external actions, one line per gate
with its REAL exit code and real numbers, the item-status table, the open-findings count,
and your deviations. This is SESSION 18 of F275 and round 43; F275 stands at 43 rounds
against the operator's soft limit of 60 rounds and 20 sessions (amend0908-f275-finish rule
1), so no scope report is owed. Add the one sentence of context self-assessment
amend0905-throughput requires. State the measured TOTAL and PROSE line counts constraint 8
orders. Then push the branch. Create no pull request, merge nothing, force-push nothing and
rewrite no history.

--- BEGIN SLICE PLAN43 ---
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

ROUND 43 takes the reading DECISION F275 D22 took for the TASK records and nobody had taken
for the JOB records: both shipped classes IMPORTED and compared field by field, plus the
shape readings a name comparison cannot give. The pair is CLEAN — 13 shared names and the
only two `Job`-only names are the renames `id` and `name` — so there is no third unmeasured
record pair, and DECISION F272 D15's sentence holds for the job record where D22 disproved
it for the task record. DECISION F275 D24 records that, the `created_at` shape change at six
sites, and `budget`'s already-guarded nullability. No production line moves.

## Next Steps

1. THE FLIP. Its target API now exists (round 42) and its record shapes are now measured
   (this round), so it applies: `.agent/f275_t003_flip_sites.md` for the `.id` and `.name`
   sites, `.agent/f275_t003_flip_seam.md` for the classic store seam, and
   `.agent/f275_t003_record_shapes.md` for the type sites and the `created_at` rewrite. It
   lands as the one declared-oversize commit AGENTS.md permits per feature, with the
   inseparability reason AND the real size stated in the handback BEFORE review, and it
   registers `Task.acceptance_checks`'s structured form as a finding naming the feature that
   owns acceptance criteria, per amend0908-f275-finish rule 4.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take. Four rounds have now
  measured it and three found it larger: D17 sized it at 1766 changed lines, D21 at 3771
  across 263 files, D22 added a type pair, D23 found three pieces of its target API
  missing, and D24 is the first to find NOTHING new.
- The open set is 86 by distinct id at this round's base `7f8724c3`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
--- END SLICE PLAN43 ---

--- BEGIN SLICE RECORD43 ---

Gate: F275 R42 — the F275 round 42 entry. VERDICT PASS, written by the planner and reviewer of session 18 after reading the committed range `77a7d840`..`c4cdc4ce` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Booked here by round 43 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier was the round 42 handback committed at `7f8724c3`. Six single-parent commits C0a `9c4f39c6`, C0b `bc90d257`, C1 `6e885b61`, C2 `03a3048e`, C3 `c4cdc4ce` and C4 `7f8724c3`, per-commit insertions 362, 333, 18, 18 and 379 for the five before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500 — so F275's ONE declared-oversize allowance is STILL UNSPENT and still reserved for the flip. THIS ROUND EXISTS BECAUSE A DRY RUN FOUND THE FLIP UNEXECUTABLE AS RULED. The reviewer applied the flip's own premise in a disposable worktree before authoring and measured three capabilities the classic store has and the unified store lacked: a jobs-root override that 186 classic call sites pass, 83 by keyword and 103 as a positional, 56 of them production, which `data_paths.job_record_path` already accepted and the three unified functions never passed on; corruption visibility, which `storage.load_job_safe` returns and four production sites act on while `load_job_plan` collapsed missing and unreadable into one `None`; and listing, which 17 call sites use and the unified store had no function of any spelling for. Moving a consumer onto an API that lacks the parameter it passes is not a migration but the invention of that API, so the one commit this feature may declare oversize would have carried new production functions and their tests — which AGENTS.md's Commit Discipline forbids mixing and which that commit cannot be split to repair. DECISION F275 D23 records the route, on the precedent DECISION F275 D22 set for `TaskEntry` and DECISION F272 D5, D6 and D7 set for the `state` collapse. G1 IS THE PRIMARY cmp-AGAINST-SCRATCHPAD PROOF AND NOT THE §4.9 DIGEST FALLBACK: the reviewer's own scratch original survived the session, was hashed BEFORE delegation at `da92b95ac2d0f35d4ed31f73d31468a5fafc0df2d1560bc55f944e739ef374ed`, and is byte-identical to both committed copies at 33858 bytes, which `git rev-parse` resolves to ONE shared blob `ea23f07e`; per §3 item 37 that chain covers three on-disk artefacts and claims nothing about bytes emitted into a prompt. G2: `.agent/plan.md` byte-identical to PLAN42 at 2720 bytes, 47 lines against the cap of 50, both mandated headings exactly once. G3 over THREE appends, each re-derived as a reconstruction from the committed C1 blob to the committed C2 blob: `.agent/live_review.md` 855619 to 860378, `.agent/prose_slips.md` 234601 to 235493, `.agent/decisions.md` 1055728 to 1061618; every reader A identical, every reader B true with N counted FROM THE SLICE at 1, 1 and 7, and all three negative controls REJECTED BY BOTH READERS with the flipped byte inside the FIRST appended paragraph, which is the region §3 item 36 requires a control to sit in; `^Gate: F275 R41 ` and `^## DECISION F275 D23 ` each 0 at C1 and exactly 1 at C2. G4: the open set is 86 BY DISTINCT ID at the base, at C3 and at C4, over 103 registrations against 17 resolutions, with no id registered and none resolved. G5: the reviewer re-ran the scoped suites at `125 passed` over four files, `ruff` at `All checks passed!`, and the shipped-signature probe printing all six widened signatures from the work-tree files; the widen's behaviour was then exercised through the SHIPPED functions, where an explicit root redirects the write, a record under one root is invisible under another, the default root is untouched, missing reads `(None, False)`, corrupt reads `(None, True)` where the plain reader answers `None` to both, the listing is newest-first with the unreadable record named by its job id, and a FILE named `jobs` returns `([], False, [])` instead of raising — which the worker's `is_dir()` earns and the reviewer's own draft, written with `exists()`, did not. G6: the reviewer's own four-mutation red proof in a disposable worktree at C3 reproduced the worker's readings EXACTLY — control `18 passed` at exit 0, M1 dropping the root from the read at 2 failed, M2 flipping the degraded answer at 3, M3 deleting the sort at 1, M4 widening the layout glob to the classic shape at 6, each naming node ids read from the `FAILED` lines and never inferred from an exit code, every revert byte-exact by sha256, the control green again, and the PRIMARY checkout's porcelain read EMPTY in the same command sequence as every mutation. G7: `tests/test_data_paths.py` green and an `ast` reading of `pingpong_job.py` at C3 reporting ZERO references to `jobs_dir` — the guard whose RED reading is what moved the layout glob into `data_paths` in the first place, quoted in the block from the reviewer's own failed first draft. G8: the change set is an EXACT set match over nine paths with MISSING and EXTRA both empty and ZERO paths under `apps/`, `docs/` or `scripts/`, porcelain EMPTY, ONE worktree, `.agent/STOP` absent. THE WORKER DECLARED SIX DEVIATIONS AND THE REVIEWER SUSTAINS ALL SIX, two of them correcting the reviewer. The fourth is the one that matters: G3's structural reader as WORDED reads FALSE on the TRUE bytes for all three appends, because constraint 2 puts the separating blank line inside the slice and the post blob spends it as a separator, so the slice's first paragraph carries a leading newline its landed copy does not. The reviewer reproduced that — raw equality false for all three, stripped equality true for all three, the difference exactly one leading newline — and the gate is corrected in the round 43 block rather than here. No slice was edited, which constraint 1 required and which is why a false-reading gate cost a declaration instead of a repair. The first deviation is the round improving on the block: S6 shipped 18 tests where the ordered list named 14, and two of the four extra are what make the ordered mutations reachable at all — without `test_m3` a store holding only unified records has no top-level `*.json`, so M4 would have left every listing test green, and without `test_f2` the widened `ValueError`/`TypeError` clause would have been decorative. The third declares that the first G6 worktree was created INSIDE the repository and ungitignored, read as `?? .agent-wt-r42/` by porcelain, and was removed and pruned before any mutation ran. The fifth and sixth are measurements the worker took rather than assumed: 31 internal `_persist_job` call sites of which exactly 1 passes a second argument, corrected from a remembered 38 before committing, and `ruff`'s `select` carrying no `B`, so the deliberately redundant exception tuple is not flagged. NO FINDING IS REGISTERED BY THIS GATE AND NONE IS RESOLVED.
--- END SLICE RECORD43 ---

--- BEGIN SLICE SLIPS43 ---

2026-09-10 · F275 R43 · The round 42 block's G3(b) ordered a structural reader that CANNOT PASS on correct bytes: constraint 2 of that same block puts the separating blank line inside each append slice, so the slice's first paragraph owns a leading newline that the landed copy spends as a paragraph separator, and a raw paragraph comparison therefore reads FALSE for every one of the three appends. The worker declared it rather than editing a slice, ran the reader with boundary whitespace stripped, and got TRUE for all three with all six control readings still rejecting; the reviewer reproduced both readings independently. Nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is wrong and the property the gate exists for was established by the ordered operation plus the corrected reader, so this is a dated line and not an id, per operator amendment amend0827-process-diet rule 2. The round 43 block states the stripping requirement inline.
--- END SLICE SLIPS43 ---

--- BEGIN SLICE DECISION43 ---

## DECISION F275 D24 (2026-09-10, F275 round 43) — the JOB record pair is CLEAN: the flip has no third unmeasured record, and the one shape change beyond the id is `created_at`

WHY THIS READING WAS OWED. DECISION F272 D15 measured the two JOB records as differing in `id` and `name` alone. DECISION F275 D22 proved that same sentence wrong about the TASK records — `Task` and `TaskEntry` share two names of seven and twenty-three — and it got there by IMPORTING both shipped classes rather than by reading their source or trusting the earlier sentence. That correction left an obvious question nobody then asked: if D15's claim was wrong about the task record, is it wrong about the JOB record, which is the record the flip actually moves? This decision is that reading. D15's and D22's landed text is NOT rewritten, per planner_reviewer_prompt.md §3 item 20.

THE ANSWER, measured at `7f8724c3` by importing `packages.core.models.Job` and `packages.orchestration.pingpong_job.JobPlan` and comparing `model_fields` against `dataclasses.fields`. `Job` declares 15 fields and `JobPlan` 65. They SHARE 13 NAMES — `artifacts`, `budget`, `budgets`, `created_at`, `fences`, `flight_plan`, `intake`, `metadata`, `mission`, `project_id`, `state`, `tasks` and `user_prompt`. The `Job`-only names are exactly TWO, `id` and `name`, and both are the renames this chain has tracked since F272: `id` to `job_id` and `name` to `job_title`. THE ORPHAN SET IS EMPTY. So DECISION F272 D15's sentence HOLDS for the JOB record, precisely where D22 disproved it for the TASK record, and the flip has no third unmeasured record pair waiting in it. This is the first round of four to measure the flip and find NOTHING new to carry, which is the result that makes the next round the flip itself.

THE SHAPE CHANGES A NAME COMPARISON CANNOT SEE, because a shared name is not a shared type. Two are real and the rest are repr noise — pydantic resolves an annotation to its module path while a dataclass keeps the source string, so `list[packages.core.models.Artifact]` and `list[Artifact]` are the same type rendered twice, and a string comparison over these 13 names reports 13 differences where the truth is 2. FIRST, `created_at` is a `datetime` on `Job` and an ISO-8601 `str` on `JobPlan`. Measured by `ast` with a receiver filter whose rejections are listed in the artefact so the narrowing is auditable: SIX sites call a datetime-only method on a job-ish `created_at`, FOUR production and TWO test, and every one of the six is `.isoformat()` — `apps/cli/commands/job.py` at three sites, `packages/orchestration/job_fulfillment.py` at one, and `tests/cli/test_loop_cmd.py` at two. The flip's rewrite for each is therefore the simplest possible one: `<job>.created_at.isoformat()` becomes `<job>.created_at`, because the method's output IS the unified record's stored value. No job-ish site COMPARES the field, and the three comparison sites an unfiltered sweep first reported are between two run manifests, not two jobs — which is why the filter exists and why its rejections are published. Lexicographic order over the unified record's own format was measured to agree with chronological order anyway, so a later comparison site is safe. SECOND, `budget` is a `Budget` on `Job` and `Budget | None` on `JobPlan`, a nullability flip in the unsafe direction. Exactly ONE site dereferences it on a job-ish receiver, `packages/orchestration/pingpong_job.py` inside `_export_job`, and it already reads `job.budget.model_dump(mode="json") if job.budget else None`. So the flip owes this field nothing, and that is a measurement rather than an assumption.

WHAT IS DELIBERATELY NOT COMMITTED, recorded because a later reader will look for it. No per-SITE enumeration of the `Job` and `Task` TYPE sites is committed. Three reasons, in the order they decide it: the figures reproduce — 582 constructions, 345 imports and 1294 distinct lines in 201 files, 46 production and 155 test, which is DECISION F275 D21's part (c) exactly; the transformation at those sites is a TYPE-NAME rewrite, `Job` to `JobPlan` and `Task` to `TaskEntry`, which an `ast`-guided pass performs without consulting a list; and the artefact embeds the instrument, so the flip round regenerates the list at its own base in one run, which `.agent/f275_t003_flip_sites.md` section 5 already requires of it. Two component counts differ from their landed decisions by one and the artefact reports both rather than smoothing them: this instrument reads 367 annotations where D21 records 368, with the UNION identical at 1294, which is the shape of one annotation sharing a `(path, line)` with another kind; and it reads the `Task` union at 428 lines in 112 files where D22 records 427 in 111, with all three of D22's component counts reproducing EXACTLY. The reviewer re-ran the instrument in a disposable worktree at `6537ece6`, D22's own base, and read 428 and 112 there as well, so the difference belongs to that decision's union arithmetic and not to the tree having moved under it. Neither difference changes the flip's declared size materially, and neither is an id: both are the reviewer's own prose, which amend0827-process-diet rule 2 routes to `.agent/prose_slips.md`.

HOW TO REVERSE: delete this decision. What is lost is the knowledge that the job record pair is closed, and the next round would owe the reading again before it could honestly declare the flip complete.
--- END SLICE DECISION43 ---

--- BEGIN SLICE BANNER43 ---
# F275 T003 — the RECORD SHAPES the flip moves, MEASURED

> Measured at `7f8724c3`, this round's base, over the tracked tree at that commit.
> THIS FILE MEASURES; IT FLIPS NOTHING. No line under `packages/`, `apps/`, `tests/`,
> `docs/` or `scripts/` moved in the round that wrote it.

DECISION F275 D22 compared the two TASK records by IMPORTING both shipped classes and
found them sharing two field names of seven and twenty-three, which disproved DECISION
F272 D15's sentence about them. Nobody had run that reading for the JOB records — the pair
the flip actually moves. This file is that reading, together with the shape readings a
name comparison cannot give, and DECISION F275 D24 carries its ruling.

The instrument's source is embedded below so the measurement is reproducible from this
artefact alone, which is the convention `.agent/f275_t002_flip_inventory.md` set and
`.agent/f275_t003_flip_seam.md` kept. A site is one `(path, line)` pair resolved by `ast`
over the files `git ls-files '*.py'` names, never by grep, so a name inside a comment or a
string is not a site. Every receiver-name filter PRINTS ITS REJECTED RECEIVERS beside the
accepted ones, because a count is only as wide as its predicate and a narrowing nobody can
audit is a narrowing nobody can trust.

No per-SITE list of the type sites is committed, and DECISION F275 D24 records the three
reasons: the figures reproduce DECISION F275 D21's part (c), the transformation there is a
type-NAME rewrite that needs no list, and this artefact regenerates the list in one run.

## The instrument
--- END SLICE BANNER43 ---

--- BEGIN SLICE INSTRUMENT43 ---
"""F275 T003 — the flip's last measurements, in one pass.

Produces, at the commit it is run at: the two JOB records compared field by field; the
shape changes on the names they share; the sites that use `created_at` as a DATETIME and
the sites that dereference `budget`; and a re-derivation of the two TYPE-site figures no
committed file holds — DECISION F275 D21's part (c) and the `Task` sites D22 counted.

A site is one `(path, line)` pair resolved by `ast` over the files `git ls-files '*.py'`
names, never by grep. Every receiver-name filter prints its REJECTED receivers beside the
accepted ones, because a count is only as wide as its predicate.
"""
import ast
import collections
import dataclasses
import subprocess
import sys

REPO = "."
sys.path.insert(0, REPO)
JOBISH = ("job", "plan", "record")
SHORT = ("j", "stored")
DT_ONLY = {"isoformat", "strftime", "timestamp", "date", "time", "astimezone",
           "toordinal", "weekday", "utcoffset", "tzname"}


def tracked():
    out = subprocess.run(["git", "ls-files", "*.py"], capture_output=True, text=True,
                         cwd=REPO).stdout
    return [p for p in out.split() if p]


def trees():
    for path in tracked():
        try:
            yield path, ast.parse(open(f"{REPO}/{path}", "rb").read(), filename=path)
        except (SyntaxError, OSError):
            continue


def recv(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call):
        f = node.func
        return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
    return ""


def jobish(name):
    low = name.lower()
    return low in SHORT or any(t in low for t in JOBISH)


def type_sites(name):
    kinds = collections.defaultdict(set)
    for path, tree in trees():
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                f = n.func
                called = f.id if isinstance(f, ast.Name) else (
                    f.attr if isinstance(f, ast.Attribute) else None)
                if called == name:
                    kinds["construction"].add((path, n.lineno))
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                for a in n.names:
                    if a.name == name:
                        kinds["import"].add((path, n.lineno))
            elif isinstance(n, (ast.AnnAssign, ast.arg)):
                if n.annotation is not None:
                    for sub in ast.walk(n.annotation):
                        if (isinstance(sub, ast.Name) and sub.id == name) or \
                           (isinstance(sub, ast.Constant) and sub.value == name):
                            kinds["annotation"].add((path, n.lineno))
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.returns:
                for sub in ast.walk(n.returns):
                    if (isinstance(sub, ast.Name) and sub.id == name) or \
                       (isinstance(sub, ast.Constant) and sub.value == name):
                        kinds["annotation"].add((path, n.lineno))
    return kinds


def report(name, kinds):
    union = set()
    for s in kinds.values():
        union |= s
    files = {p for p, _ in union}
    prod = sorted(f for f in files if not f.startswith("tests/"))
    print(f"\n### `{name}` TYPE sites")
    for k in ("construction", "import", "annotation"):
        print(f"  {k:13s} {len(kinds[k])}")
    print(f"  DISTINCT CHANGED LINES {len(union)} in {len(files)} files — "
          f"{len(prod)} production, {len(files) - len(prod)} test")
    per_file = collections.defaultdict(set)
    for p, ln in union:
        per_file[p].add(ln)
    print(f"  files carrying a site: {len(per_file)}")
    return union


def main():
    from packages.core.models import Job
    from packages.orchestration.pingpong_job import JobPlan

    jf = {n: str(f.annotation) for n, f in Job.model_fields.items()}
    pf = {f.name: str(f.type) for f in dataclasses.fields(JobPlan)}
    shared = sorted(set(jf) & set(pf))
    job_only = sorted(set(jf) - set(pf))
    print("## 1. THE JOB RECORD PAIR, by IMPORTING both shipped classes")
    print(f"  Job fields {len(jf)} | JobPlan fields {len(pf)}")
    print(f"  shared names {len(shared)}: {shared}")
    print(f"  `Job`-only names {len(job_only)}: {job_only}")
    print(f"  ORPHANS (no counterpart, not a known rename): "
          f"{[f for f in job_only if f not in ('id', 'name')]}")

    print("\n## 2. THE ANNOTATIONS ON THE SHARED NAMES, side by side")
    print("  The two reprs differ even where the TYPE does not — pydantic resolves an")
    print("  annotation to its module path and a dataclass keeps the source string — so")
    print("  these are read by MEANING and a string comparison is NOT used.")
    for n in shared:
        print(f"  {n:14s} Job {jf[n]:44s} JobPlan {pf[n]}")

    print("\n## 3. `created_at` USED AS A DATETIME, by receiver")
    acc, rej = [], []
    for path, tree in trees():
        for n in ast.walk(tree):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)):
                continue
            inner = n.func.value
            if not (isinstance(inner, ast.Attribute) and inner.attr == "created_at"):
                continue
            if n.func.attr not in DT_ONLY:
                continue
            r = recv(inner.value)
            (acc if jobish(r) else rej).append((path, n.lineno, r, n.func.attr))
    ap = [r for r in acc if not r[0].startswith("tests/")]
    print(f"  ACCEPTED {len(acc)} — production {len(ap)}, test {len(acc) - len(ap)}")
    for row in sorted(acc):
        print(f"    {row[0]}:{row[1]} receiver {row[2]} .{row[3]}()")
    print(f"  REJECTED {len(rej)}, listed so the filter is auditable:")
    for row in sorted(rej):
        print(f"    {row[0]}:{row[1]} receiver {row[2]} .{row[3]}()")

    print("\n## 4. `budget` DEREFERENCED on a job-ish receiver")
    deref = []
    for path, tree in trees():
        for n in ast.walk(tree):
            if (isinstance(n, ast.Attribute) and isinstance(n.value, ast.Attribute)
                    and n.value.attr == "budget" and jobish(recv(n.value.value))):
                deref.append((path, n.lineno, recv(n.value.value), n.attr))
    dp = [d for d in deref if not d[0].startswith("tests/")]
    print(f"  sites {len(deref)} — production {len(dp)}, test {len(deref) - len(dp)}")
    for row in sorted(deref):
        print(f"    {row[0]}:{row[1]} receiver {row[2]} .budget.{row[3]}")

    print("\n## 5. THE TYPE-SITE FIGURES, re-derived at this commit")
    j = report("Job", type_sites("Job"))
    t = report("Task", type_sites("Task"))
    both = j | t
    print(f"\n## 6. THE TWO TYPE-SITE SETS UNIONED")
    print(f"  union {len(both)} lines in {len({p for p, _ in both})} files; "
          f"overlap {len(j & t)}")


if __name__ == "__main__":
    main()
--- END SLICE INSTRUMENT43 ---
