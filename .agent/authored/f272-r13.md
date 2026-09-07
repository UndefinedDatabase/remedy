── STEP T002 (move three readiness) — F272 ─
Goal:        Book the round 12 verdict and resolve R-0821, and land the measured
             readiness inventory for DECISION F272 D6's move three — the retype
             of `JobPlan.state` to `RunState` — so the next session authors that
             round from readings on disk rather than re-deriving them.
Bundle:      C0a save the block · C0b mirror · C1 the plan · C2 the round 12
             verdict and the R-0821 resolution · C3 the readiness inventory ·
             C4 the handback.
Change:      EXACTLY the paths listed under "The change set" and nothing else.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 1, and
this line one run of 2 — both measured, not recalled.

## Why this round is a measurement and not the retype

Round 12 PASSED and landed R-0821's fix. The next step in the plan is move three
of DECISION F272 D6, and this session is NOT authoring it. The reason is
operator amendment amend0905-throughput's own early-end signal: it names "the
reviewer noticing its own authoring errors accumulating (a run of
`.agent/prose_slips.md` lines in one session is that signal)", and this session
booked FIVE such lines, every one recording a defect in the reviewer's own block
text — round 10's unreachable empty-log gate and its unmeetable ruff gate, a
wrong SESSION number, round 11's "FIX, LANDED BY THIS ROUND" clause that a STOP
condition falsified, and round 11's G4 ordering a suite green that a third
guard made unreachable. Move three is the largest remaining change of T002 and
touches 27 files; authoring it against that run of slips is how round 9 was
lost. So this round puts the measurements on disk and the next session, with a
cold context, writes the block.

This is a MEASUREMENT round, not a bookkeeping round: C3 lands an artifact that
did not exist, of the same class as `.agent/f272_state_rename_inventory.md`.
The verdict and the resolution ride in C2 because C2 is a commit that is
happening anyway, which is what amend0827-process-diet rule 1 requires.

## What the reviewer MEASURED before ordering this (§3 item 34)

Every reading below was taken BY ME at `a9aa8fa7`, and C3's job is to put them
on disk verbatim. None is inferred.

- THE STR-ENUM SEMANTICS, measured by importing the SHIPPED
  `packages/core/models.py` on this interpreter, for `RunState.BLOCKED`:
  `str()` is `'RunState.BLOCKED'`; the f-string is `'blocked'`;
  `json.dumps({'s': b})` is `{"s": "blocked"}` and `json.dumps(b)` is
  `"blocked"`; `b == 'blocked'` is True; `isinstance(b, str)` is True; `.value`
  is `'blocked'`; `'%s' % b` is `'RunState.BLOCKED'`; and `b` works as a dict
  key reachable by `'blocked'`. So a retype changes EXACTLY TWO renderings,
  `str()` and `%s`, and changes no comparison, no JSON and no f-string.
- THE HAZARD IS THEREFORE COUNTABLE, AND I COUNTED IT by `ast` over the 1065
  tracked `.py` files from `git ls-files`: `'%s' % <x>.state` sites — ZERO.
  `str(<x>.state)` sites — TWELVE, at `apps/cli/commands/job.py:1201`, `:1650`,
  `:1769` and `:1808`, `packages/orchestration/project_summary.py:78`,
  `packages/orchestration/ui_server.py:1525`, `:1697` and `:2635`,
  `packages/orchestration/ui_view_model.py:638`, `:769` and `:994`, and
  `tests/orchestration/test_dod_gate.py:305`.
- ALL TWELVE ARE ALREADY SAFE, AND NONE IS A `JobPlan`. Every one is the
  defensive idiom `job.state.value if hasattr(job.state, "value") else
  str(job.state)`, which takes `.value` when the object IS an enum and falls
  back to `str()` only when it is not — so the retype makes the `.value` branch
  live and the `str()` branch dead, which is the safe direction. Each also
  reads `job.id`, the CLASSIC `Job`'s primary key; a `JobPlan` has `job_id`.
  So the twelve are classic-`Job` sites that were already carrying a `RunState`
  before F272 began.
- THE THREE BOUNDARIES WHERE A STATE LEAVES THE RECORD, read from
  `packages/orchestration/pingpong_job.py`: line 667 `"status": job.state,` in
  `_export_job`, line 2968 `"status": job.state,` in `export_job_report`, and
  line 3026 `f"Status: {job.state}",` in `format_job_report_text`. The first two
  are the ones move three must spell `.value`; the third is an f-string and is
  already correct, which is exactly what round 10's rendering guard pins.
- THE SIX CONSTANTS, at `packages/orchestration/pingpong_job.py` lines 65 to 73:
  `JOB_PLANNED`, `JOB_RUNNING`, `JOB_BLOCKED`, `JOB_COMPLETED`, `JOB_PAUSED` and
  `JOB_STOPPED`, each a plain `str` today. `git grep -l` over `packages/`,
  `apps/` and `tests/` names 27 files referencing at least one of them.
- THE TWO ASSERTIONS MOVE THREE MUST INVERT, both in
  `tests/orchestration/test_job_state_field.py`, which round 10 shipped:
  `test_nothing_was_retyped` asserts `type(JobPlan().state).__name__ == "str"`,
  and G4(v)'s companion reading `isinstance(..., RunState)` is False. That test's
  own docstring says "Move two renames; move THREE retypes", so inverting them is
  the intended move and not a weakening.
- `RunState` HAS NINE MEMBERS at this tree, in declaration order PENDING,
  PLANNED, RUNNING, PAUSED, COMPLETED, FAILED, CANCELLED, BLOCKED, STOPPED.
- THE BASE SUITE READINGS, each run by me: `tests/ui_contracts/` EXIT 0 at 809
  passed and 4 skipped at `a9aa8fa7`; `tests/docs/` EXIT 0 at 303 and the canary
  EXIT 0 at 42 at `a9aa8fa7`; `tests/orchestration/test_test_runner.py` EXIT 0
  at 52 at `a9aa8fa7`; and `tests/orchestration/` EXIT 0 at 12847 passed and 10
  skipped and `tests/cli/` EXIT 0 at 1537 passed, both at `1bfb1cd9`, which
  still stand because rounds 11 and 12 changed no file under `packages/`,
  `apps/cli/` or `tests/orchestration/`.
- THE APPEND TARGETS at `a9aa8fa7`: `.agent/live_review.md` 1132490 bytes / 705
  units, registrations 305, resolutions 247, open BY DISTINCT ID 58, `^Gate: `
  34, `^Landed: R-0821 ` 1, `^Done: R-0821 ` 0. Its terminal byte is exactly one
  newline.
- THE `Landed:` LINE IS NOT REWRITTEN. Three ids in this record already carry
  BOTH a `Landed:` line and a `Done:` paragraph — R-0725, R-0757 and R-0818 —
  so appending the resolution beside the surviving line is this record's own
  practice and is what §3 item 20 requires of an append-only file.

## What the OPEN SET binds on this block (§3 item 34, last clause)

"BINDING ON THE NEXT BLOCK THAT ORDERS A HANDBACK" — APPLIED, same words, in the
Handback section. R-0821's clause, that a block changing a state vocabulary
NAMES `tests/ui_contracts/` in its gate list — NOT APPLICABLE HERE, because this
round changes no vocabulary, and it is carried forward into C3's inventory so
move three inherits it. R-0819's shadow-property clause and R-0820's
same-predicate clause — NOT APPLICABLE, no such gate here; both are carried into
C3 for move three.

## The change set

C2: `.agent/live_review.md`. C3: `.agent/f272_retype_readiness.md` (NEW).
C0a/C0b/C1/C4: `.agent/authored/f272-r13.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/handoff.md`.

No `.py`, no `.ts` and no `docs/` file changes this round.

## C3 — the readiness inventory, a SPEC and not a slice

Write `.agent/f272_retype_readiness.md`. It is EVIDENCE for the next session's
block author and states only what was measured, never a prediction or a plan.
Its content is the eight readings listed above, reproduced faithfully, under
these headings and in this order:

1. **What the retype changes** — the eight str-Enum readings, as a table of
   expression against result, naming the interpreter version you measure on.
   RE-MEASURE them yourself by importing the shipped `packages/core/models.py`
   and report YOUR readings; if any differs from mine, report both and say so,
   because a difference there is the whole finding.
2. **The rendering hazard, counted** — the `%s` count and the `str()` count with
   every site by path and line, each classified as classic `Job` or `JobPlan`
   WITH the evidence that settles it, and the defensive idiom quoted once.
3. **The three record boundaries** — the two `"status": job.state` sites that
   need `.value` and the one f-string that does not.
4. **The six constants and their blast radius** — the lines they sit on and the
   count of files referencing them, with the command that produced the count.
5. **The two assertions move three inverts** — by test name and file.
6. **What must NOT change** — the stored JSON key stays `"status"` under
   DECISION F272 D5; the six constants keep their NAMES and VALUES even as
   their type changes; `f"{job.state}"` must still render the plain word, which
   is the guard round 10 shipped.
7. **The open clauses move three inherits** — R-0821's, that a block changing a
   state vocabulary names `tests/ui_contracts/` in its gate list; R-0820's, that
   a gate must not be computed from the same predicate as the change set; and
   R-0819's shadow-property clause, still owed by T003 and T004.
8. **The method** — DECISION F272 D7's probe is the instrument for finding sites
   a retype breaks, exactly as it was for the rename, and
   `.agent/f272_state_rename_inventory.md` records how it is driven.

Every figure in the file is one YOU measured in this round. Where you reproduce
one of mine, say that you reproduced it and give your own reading beside it.

## Constraints

1. NO SLICE IS EDITED — apply the authored texts byte for byte between their
   markers; if one looks wrong, apply it anyway and say so. C3 is a SPEC: write
   that file yourself.
2. The paths listed under "The change set" are the whole change set.
3. Commit order C0a, C0b, C1, C2, C3, C4, nothing reordered; C1 is the first
   substantive commit (§3 item 23).
4. APPEND CONVENTION for `.agent/live_review.md`: `post == pre + b"\n" + slice`,
   the slice being the marker-delimited lines each with its terminating newline,
   and the post-image ending in exactly one `\n`. PLAN CONVENTION:
   `.agent/plan.md` is REPLACED by exactly the PLANF272R13 slice.
5. Behaviour changes: NONE. No `.py` or `.ts` file is touched, so no test count
   anywhere may move.
6. Mint NO finding id of your own and write NO `Done:` paragraph of your own —
   the `Done: R-0821` paragraph in RECORDR13 is the reviewer's authored text and
   is the only one. Do NOT delete or edit the existing `Landed: R-0821` line.
7. Destructive verification goes in a disposable `git worktree` under the
   gitignored `.remedy-wt/`, never the primary checkout (protocol G5); remove
   and prune it before the handback, BY EXACT PATH and never by glob. This round
   is not expected to need one; say so if you make none.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C3 and before C4,
   and table all three; if it appears, finish only the half-written commit, then
   hand off (protocol G6).
9. `python3 -B` for every run; report each gate's REAL exit code, "green" as a
   word being a finding.

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r13.md` and `.agent/last_block.md`; both equal each other
and the BLOCK_SHA and length the delegation names. Per §3 item 37 this covers
the saved copy and its mirror, not the bytes emitted into your prompt — say so.

**G2 THE RECORD, at C2.** Readers (a) to (d) over `.agent/live_review.md`.
(a) BYTE: pre and post lengths; pre a byte-exact prefix; `post == pre + b"\n" +
slice`; pre's terminal byte asserted to be exactly one `\n` BEFORE writing; post
ends in exactly one `\n`.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`, with N COUNTED BY YOUR SCRIPT from the slice's own paragraphs and
never taken from this block: units before, after, delta; the last N units equal
the slice's paragraphs IN ORDER; the units before an unchanged prefix.
(c) NEGATIVE CONTROL in memory on a `bytes` object, never on disk: flip a byte
inside the FIRST appended paragraph, asserting the offset lies inside it first;
(a) and (b) must BOTH reject; restore and require both to accept and the
restored image to equal the disk image.
(d) COUNTS before → after C2: `^- R-\d{4} — ` distinct ids 305 → 305; `^Done:
R-\d{4} — ` distinct 247 → 248; open set BY DISTINCT ID 58 → 57; `^Gate: ` 34 →
35; `^Gate: F272 R12 ` 0 → 1; `^Done: R-0821 ` 0 → 1; and `^Landed: R-0821 `
1 → 1, UNCHANGED, which is the reading that proves the landed line was not
rewritten.

**G3 THE PLAN at C1.** `.agent/plan.md` equals the PLANF272R13 slice bytes
exactly; report the equality, both byte lengths, the line count against the
AGENTS.md cap of 50, and that `## Goal` and `## Next Steps` are present.

**G4 THE INVENTORY IS MEASURED, NOT COPIED, at C3.** Re-derive the two counts of
its section 2 YOURSELF, by `ast` over every tracked `.py` file enumerated from
`git ls-files`, and report the file total you enumerated beside them: the `%s`
count and the `str(<x>.state)` count with their sites. Re-derive section 1's
eight readings by importing the shipped `packages/core/models.py`. State beside
each whether it REPRODUCES the reviewer's reading above or DIFFERS, and where it
differs give both. An inventory that agrees with me because it copied me is
worth nothing to the session that reads it.

**G5 THE THREE BOUNDARIES RESOLVE, at C3.** For each of
`packages/orchestration/pingpong_job.py` lines 667, 2968 and 3026, print the
line as it stands at `a9aa8fa7` and confirm it is the text this block quotes.
A citation that has drifted is a finding of this round, not a detail.

**G6 NOTHING MOVED.** `tests/ui_contracts/` EXIT 0 at 809 passed and 4 skipped,
`tests/docs/` EXIT 0 at 303, and the canary EXIT 0 at 42 — the same three
readings as the base, because this round changes no code. Report each exit code
and summary line. The full `tests/orchestration/` and `tests/cli/` are NOT
ordered: no `.py` file changes, so neither is reachable as a gate; state that
reasoning rather than reporting a suite you did not run.

**G7 LINT AND INTEGRITY.** No `.py` file changes, so `ruff`'s ordered file set is
EMPTY — say so plainly rather than reporting a pass.
`python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`,
`"fail_count": 0`.

**G8 THE TREE.** `git status --porcelain` EMPTY when C4 is staged;
`git ls-files .remedy-wt` EMPTY; `git worktree list` naming every worktree you
created and confirming its removal by exact path, or stating that you created
none. Per commit C0a through C3 — NOT C4, which cannot count its own insertions
(§3 item 14) — the insertion count from `git diff --numstat <parent> <commit>`,
each single-parent and under the F104 D1 cap of 500; those same numbers fill the
handback's `## Commits` `+/-` column, so report both readings side by side and
confirm each row cell by cell (§3 item 28). Marker sweep: the number YOU measure
of LINES BEGINNING `<<<BEGIN ` or `<<<END ` in every written non-block file,
zero in each — line-anchored, because this record already carries those tokens
mid-line inside earlier findings that quote the syntax. The three `.agent/STOP`
readings as a table.

## The slices

<<<BEGIN PLANF272R13>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 12 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE;
T002 has landed the eight administrative fields, widened `RunState`, renamed
`JobPlan.status` to `state` at the 234 measured sites of DECISION F272 D7, and
given `blocked` and `stopped` their place in the cockpit.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the eleven consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

Readiness for move three. The measurements that round need — what a str-Enum
retype does and does not change, the counted rendering hazard, the three record
boundaries, the six constants and their blast radius — land as
`.agent/f272_retype_readiness.md`, and R-0821 is resolved. The retype itself is
the next session's first round, authored from that file.

## Next Steps

1. Move three: retype `JobPlan.state` to `RunState`, make the six `JOB_*`
   constants `RunState` members keeping their names and values, and put `.value`
   at the two record boundaries `.agent/f272_retype_readiness.md` names. Gate it
   on that file's readings, on round 10's rendering guard, and on
   `tests/ui_contracts/` per R-0821's clause.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A str-Enum changes `str()` and `%s` and nothing else; both are counted in the
  readiness file, and the count is what makes move three a bounded change rather
  than the open-ended one D5 assumed.
<<<END PLANF272R13>>>

<<<BEGIN RECORDR13>>>
Gate: F272 R12 — the F272 round 12 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ. Range `fcde1983`..`a9aa8fa7`, nine commits, every one single-parent, in exactly the bundle's ordered sequence C0a through C7 with nothing added, dropped or reordered, and C4 landing before C5 as constraint 3 required. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r12-block.md` was written and hashed BEFORE delegation, and it, the committed `.agent/authored/f272-r12.md` and the committed `.agent/last_block.md` are all 29750 bytes at 395 lines and all hash to `bac95d441478084ec6cc29c60adc7b17fc571d82b689e0ea11600fa3845a238a`. G2 THE RECORD reproduces byte for byte under the reviewer's own readers: `.agent/live_review.md` 1127168 to 1132490 at N counted 2 and units 703 to 705, `.agent/prose_slips.md` 139621 to 141124 at N counted 2 and units 177 to 179, each pre-image a byte-exact prefix with `post == pre + NL + slice` TRUE; registrations 305 unchanged, resolutions 247 unchanged, open set BY DISTINCT ID 58 unchanged, `^Gate: ` 33 to 34, `^Gate: F272 R11 ` 0 to 1, and after C6 `^Landed: R-0821 ` 0 to 1 with `^Done: R-0821 ` correctly still 0. G3 THE PLAN is 2284 bytes byte-equal to its slice at 44 lines against the cap of 50, and THE FEATURE FILE appended 32918 to 35898 at N counted 7 and units 70 to 77, headings D1 through D9 in order. C4 IS EXACTLY THE THREE ORDERED EDITS AND NOTHING ELSE, read from the diff: `assert len(phrases) == 7` became `>= 7`, and the two numerals left the docstrings at lines 128 and 225 — while the failure message, the `restated == []` assertion the test exists for, and the discriminator `test_the_phrase_restatement_scan_can_see_a_restated_phrase` are all untouched, so the floor was loosened and no protection was removed. C5 IS CORRECT AND MINIMAL: `blocked` and `stopped` join `SETTLED_STATES` in `apps/ui/src/api/digestVisibility.ts` and gain `"Blocked"` and `"Stopped"` in `DIGEST_STATE_LABELS` in `apps/ui/src/api/digestCardCopy.ts`, every stale numeral in both modules' comments is replaced by prose that names the set instead of counting it, and `DIGEST_CTA_RULE_IDS`, `UNREADABLE_STATE_LABEL` and the unknown class are untouched exactly as ordered. G4 and G5 RE-RUN BY THE REVIEWER: `tests/ui_contracts/` reads EXIT 0 at 809 passed and 4 skipped, against a base this reviewer measured at EXIT 1 with 2 failed, 807 passed and 4 skipped — passed risen by exactly 2, failed 0, skipped unchanged, and the two tests red on this branch since round 8 are green. G6: the vitest node `tests/orchestration/test_test_runner.py` EXIT 0 at 52 passed, `tests/docs/` EXIT 0 at 303, the canary EXIT 0 at 42. G7: ruff EXIT 0 at `All checks passed!` over the one changed `.py` file, and integrity EXIT 0 with `"passed": true` and `"fail_count": 0`. G8 THE TREE: `git status --porcelain` EMPTY, `git ls-files .remedy-wt` EMPTY, thirteen worktree entries being the primary and the twelve pre-existing `remedy/job-*`, and the line-anchored marker sweep 0 in all five written non-block files. THE WORKER'S SIX DEVIATIONS ARE ACCEPTED AND TWO OF THEM ARE THE ROUND'S BEST CONDUCT: it caught its own reader (b) mis-splitting units, reverted with `git checkout --` and re-ran from the clean pre-image so that no wrong byte ever reached a commit; and it noticed that `.remedy-wt/` holds 42 pre-existing `r12_*` files from other features, so a glob cleanup would have destroyed all 42, and removed only its own six named paths — which is the exact hazard the never-by-glob rule exists for, met by measurement rather than by luck. Deviation 5, the multi-line reformat of `SETTLED_STATES`, is ratified: the worker verified first that the contract test scans the whole file rather than a single line, so the formatting is free. Deviation 2 is a correct reading of this block's own wording: `.agent/live_review.md` already carried `<<<BEGIN` and `<<<END` substrings mid-line inside earlier findings that quote the transport syntax, and the ordered sweep counts LINES BEGINNING with them, which is 0 before and after.

Done: R-0821 — RESOLVED at F272 round 12, commits `a39dfe52` and `dd51f8a6`, verified by the reviewer at `a9aa8fa7`. The cockpit can now name and classify the two states round 8 added to `RunState`: `blocked` and `stopped` are members of `SETTLED_STATES` in `apps/ui/src/api/digestVisibility.ts`, so `digestStateClass` answers `"settled"` for both instead of `"unknown"`, and `DIGEST_STATE_LABELS` in `apps/ui/src/api/digestCardCopy.ts` carries `"blocked": "Blocked"` and `"stopped": "Stopped"`, so `digestStateLabel` answers those words instead of `UNREADABLE_STATE_LABEL`. The two tests red on this branch since round 8 are green, and the reviewer measured the whole suite at EXIT 0 with 809 passed and 4 skipped against a base of 2 failed, 807 passed and 4 skipped — a rise of exactly the two tests the finding named, with no other count moving. THE FIX NEEDED A RULING THE FINDING DID NOT ANTICIPATE, and that is the part worth keeping: a THIRD reader of the same label map, `tests/ui_contracts/test_digest_hero_card.py:230`, pinned its arity with `assert len(phrases) == 7`, so no correct fix could land while it stood. It was invisible until round 11 tried to land the change, and DECISION F272 D9 ruled it back to the floor its own failure message describes and its two siblings already use. No second id was minted for it, per §3 item 30: it is this same defect — a hard-coded seven that goes stale when the enum widens — one layer further out. THE COUNTER-MEASURE SURVIVES THIS RESOLUTION AND IS STILL OWED: a block changing `RunState`, the `JOB_*` constants or any state vocabulary NAMES `tests/ui_contracts/` in its gate list, because that suite is the only reader in this repository that checks the enum against the cockpit. Move three of DECISION F272 D6 is the next such round and `.agent/f272_retype_readiness.md` carries the clause forward to it.
<<<END RECORDR13>>>

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
`SESSION 6 of feature F272 · round 13`, the one-sentence context self-assessment
amend0905-throughput requires, branch, the range, a per-commit changed-files
table with real `+/-`, the item-status table covering C0a through C4 with every
item present exactly once, one line per gate G1 to G8 with its real exit code,
G4's re-derived counts stated as REPRODUCES or DIFFERS against the block's, the
authored-text proof table, deviations and the next expected action.

THE NEXT EXPECTED ACTION IS EXPLICIT AND IS THE SESSION'S CLOSING STATEMENT:
this session ends here, at four delegated rounds, for the reason the "Why this
round is a measurement" section states — amend0905-throughput's authoring-error
signal, five prose-slip lines in one session. The next session runs Phase 0,
checks `.agent/STOP` under Phase 1 rule 1 BEFORE the Open PR Gate under rule 2,
and its first round is move three of DECISION F272 D6, authored from
`.agent/f272_retype_readiness.md`. Say in the handoff that no PR exists for this
branch and that none was created.

No length cap. Per the fix clause OPEN in the record and binding on the next
block that orders a handback: any commit beyond the ordered sequence receives
its OWN `## Commits` row and its OWN item-status row, and the Deviations section
says so in those same words rather than beside a clause that denies it.
