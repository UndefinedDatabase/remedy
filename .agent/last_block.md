STEP CLOSURE 1/4 — F272 — round 26 — the soft limit is reached: book round 25, register F274, and record the split

Base commit for every reading in this block: `9f99f286`, the round 25 verdict commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

SESSION 12 REACHES F272'S SOFT LIMIT. Operator amendment amend0906-triage-throughput
rule 2 sets that limit at 12 SESSIONS and 40 ROUNDS for this feature by name, and this is
session 12. Under operator amendment amend0905-throughput the standing default at that
limit is SPLIT-AND-CLOSE, EXECUTED BY THE SESSION on its own authority — not a question to
the operator, and not another round of building. This round performs the SPLIT half: it
registers the remaining scope as a new feature F274, placed directly after F272 per
operator order amend0906-split-placement, and records the move as a dated DECISION. The
CLOSE half — F272's Built State section, the integration gate, the self-use precondition,
the evidence job, the review zip, the ledger rotation and the STATUS flip — follows in
this session's later rounds.

WHAT IS BEING SPLIT, measured rather than estimated. F272's T001, T002 and T003 are
COMPLETE. Its T004 is part-done: rounds 20 to 22 deleted `job run-loop`, its handler, its
tests and its two prose advertisements. What remains of T004 is the classic-to-unified
record flip, which DECISION F272 D15 measured at round 25 and ruled ATOMIC over the
consumer graph, and T005, the deletion round, has not begun. So F272 cannot reach its own
DONE inside its limit, and F274 inherits exactly that remainder.

THE ROUND ALSO PAYS WHAT ROUND 25's VERDICT LEFT OWED under amend0827 rule 1: the
`Gate: F272 R25` PASS entry and the three dated prose-slip lines that verdict named. They
ride in this round's first commits, as that rule requires, and are not a round of their
own.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r26.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R26
C2   `.agent/live_review.md` — append RECORDR26, the round 25 PASS gate entry
C3   `.agent/prose_slips.md` — append SLIPSR26, three dated lines
C4   THE REGISTRATION COMMIT, atomic and indivisible — the new feature file, the STATUS
     line, the ledger pin, the two README figures and the six dependency lines, all in
     ONE commit. Splitting it leaves an intermediate RED state; see constraint 5.
C5   `.agent/decisions.md` — append D16SLICE, the dated DECISION recording the split
C6   `.agent/handoff.md` rewritten

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r26.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    docs/roadmap/features/T2_F274.md          (NEW FILE, created by C4)
    docs/roadmap/STATUS.md
    tests/docs/test_docs_consistency.py
    README.md
    docs/roadmap/features/T2_F261.md
    docs/roadmap/features/T2_F263.md
    docs/roadmap/features/T2_F268.md
    docs/roadmap/features/T2_F269.md
    docs/roadmap/features/T2_F270.md
    docs/roadmap/features/T2_F271.md
    .agent/decisions.md
    .agent/handoff.md

`docs/roadmap/features/T2_F272.md` is NOT in this set: its Built State section is a later
round's commit. NOTHING under `packages/`, `apps/` or `scripts/` changes. The ONE file
under `tests/` that changes is `tests/docs/test_docs_consistency.py`, and the only change
to it is the ledger pin and its comment — no assertion, no test body, no import moves. No
production line moves, so no red-proof is ordered or possible. If a measurement forces a
path outside this list, APPLY IT AND DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice or a pair is wrong, apply it as written and
   declare the disagreement; never silently correct it.
2. Every authored text is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r26.md`, between its `<<<BEGIN NAME>>>` and `<<<END NAME>>>`
   lines, exclusive of both marker lines. Never retype one. TWO EXTRACTION CONVENTIONS,
   and which applies is decided by the NAME: a WHOLE TEXT — `PLANF272R26`, `RECORDR26`,
   `SLIPSR26`, `D16SLICE`, `F274FILE` — is read INCLUSIVE of the newline ending its last
   content line. A PAIR HALF — every name ending `_FROM` or `_TO` — is read with that
   final newline STRIPPED, because three of the five pairs match a substring INSIDE a
   line and a trailing newline would make the FROM match nothing. The reviewer measured
   both conventions; under this one every FROM occurs exactly once in every target it is
   applied to, as the pairs table below records.
3. C0a and C0b are `shutil.copyfile` of `.remedy-wt/f272-r26-block.md`.
4. EVERY APPEND IN THIS ROUND IS `post == pre + b"\n" + slice`, and the block states those
   bytes rather than leaving them to be inferred. Each of the three append targets —
   `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` — ends in
   EXACTLY ONE newline at the base commit, measured, and that single property is what the
   relation rests on. A MEASUREMENT TAKEN PER FILE RATHER THAN GENERALISED, because round
   25's block generalised the same claim and was wrong: occurrences of THREE consecutive
   newlines at `9f99f286` are 0 in `.agent/live_review.md`, 1 in `.agent/prose_slips.md`
   (offset 39213) and 5 in `.agent/decisions.md` (offsets 411259, 500136, 689970, 715876
   and 845071). All six are pre-existing, none is load-bearing here, and none is repaired
   by this round.
5. C4 IS ONE COMMIT AND MUST NOT BE SPLIT. `tests/docs/test_docs_consistency.py` pins the
   feature ids contiguous from 1 to `TOTAL_FEATURES` across BOTH the STATUS lines and the
   feature filenames, and `README.md`'s accepted-count line is pinned equal to
   `TOTAL_FEATURES`. The reviewer MEASURED the intermediate state in a disposable worktree
   at `9f99f286`: with the STATUS line, the file, the README and the dependency lines
   applied but the pin left at 273, `tests/docs/` is RED at exactly 3 failed and 300
   passed — `test_there_are_250_unique_feature_detail_files`,
   `test_there_are_250_unique_status_entries` and
   `test_the_readme_accepted_count_equals_the_status_count`. With the pin at 274 the same
   suite is 303 passed. No split of C4 satisfies the commit gate.
6. THE STATUS LINE'S PLACEMENT IS LOAD-BEARING, not cosmetic. It goes IMMEDIATELY after
   F272's line and INSIDE the same `## Tier 2` heading, because
   `test_the_filename_tier_matches_the_status_tier` derives a line's tier from the nearest
   preceding `## Tier <n>` heading and cross-checks it against the `T<n>_` filename
   prefix, and because Rule A5 must propose F274 before any other unchecked feature.
7. THIS ROUND MINTS NO FINDING ID. Round 25 PASSED, and the three gaps its verdict named
   are the reviewer's own block prose, which reached no file, so under amend0827 rule 2
   each is a dated `.agent/prose_slips.md` line and never an id. `R-0826` must still be
   free when the round ends: it occurs TWICE in `.agent/live_review.md` at the base
   commit, both times as prose saying the id is free, and ZERO times as a `^- R-0826 `
   registration; RECORDR26 adds no occurrence of it at all.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before C6, and
   report all three readings.
9. NO WORKTREE IS NEEDED OR PERMITTED THIS ROUND. `git status --porcelain` is empty at
   every commit boundary, and `git worktree list` is 13 entries at the base — the primary
   plus twelve pre-existing `remedy/job-*` — and must still be 13 at the end.
10. THE DOCS GATE APPLIES because the change set includes `docs/roadmap/**`, and a
    ledger-count change and its test pin land in the SAME commit, which is C4.

====================
The pairs — each classified by a containment test the reviewer RAN
====================

The reviewer ran `TO.find(FROM) >= 0` on the final bytes under constraint 2's pair
convention; each output is recorded below and the APPEND or REWRITE label is DERIVED from
it on the same line. A `true` pair carries the §4.9 append obligation and NEVER a
FROM-zero count; a `false` pair carries FROM 0x / TO 1x.

    STATUSPAIR  TO contains FROM: true   -> APPEND-shaped   docs/roadmap/STATUS.md
    DEPPAIR     TO contains FROM: true   -> APPEND-shaped   the SIX dependency files
    PINPAIR     TO contains FROM: false  -> REWRITE         tests/docs/test_docs_consistency.py
    READMEPAIR  TO contains FROM: false  -> REWRITE         README.md
    TIERPAIR    TO contains FROM: false  -> REWRITE         README.md

Every FROM was counted in every target it is applied to and occurs EXACTLY ONCE in each,
DEPPAIR's included, in all six of its files.

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between the command
and the echo, in the PRIMARY checkout. Report ONE LINE PER GATE with the transcripts
below it. Every gate runs before C6, the commit that writes the handback.

G1 TRANSPORT. One digest comparison: `.remedy-wt/f272-r26-block.md` as delivered against
   the committed `.agent/authored/f272-r26.md` and the committed `.agent/last_block.md`.
   Report sha256, byte length and line count for each of the three.

G2 THE FINDING RECORD, over the single append at C2, against its own pre-image.
   (a) BYTE: report pre_len, pre_sha256, post_len, post_sha256, the terminal twelve bytes
       and trailing-newline run of each, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and
       `POST_EQUALS_PRE_NL_SLICE`. At the base the pre-image is 1212690 bytes, 2131
       lines, sha256 beginning `57a35edca4ea83a2`.
   (b) STRUCTURAL: strip the single terminal newline, split on blank lines, compare the
       LAST N units against the slice's paragraphs IN ORDER, where N is COUNTED BY YOUR
       SCRIPT from the slice and never taken from this block. Report N, units before,
       units after and `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST paragraph the append adds, in memory only, never on
       disk: flip one byte, require BOTH readers to reject it, then re-read the file and
       confirm it is byte-identical to the real post-image.
   (d) COUNTS, each measured, none adjusted to agree:
           ^- R-\d{4} distinct        309 -> 309
           ^Done: R-\d{4} distinct    252 -> 252
           open set BY DISTINCT ID     57 ->  57
           ^Gate:                      48 ->  49
           ^Gate: F272 R25              0 ->   1
           ^- R-0826                    0 ->   0
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic.

G3 THE DECISION RECORD, over the single append at C5. Report pre_len, pre_sha256,
   post_len, post_sha256, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and
   `POST_EQUALS_PRE_NL_SLICE`. At the base the pre-image is 860210 bytes and 10857 lines.
   Then report the count of lines matching `^## DECISION F272 D` before and after, and
   confirm `D16` heads exactly one section. A duplicated D16 is a STOP, not a note.

G4 THE TWO PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R26; report its bytes,
   its line count against the AGENTS.md cap of 50, and that `## Goal` and `## Next Steps`
   are both present. `.agent/prose_slips.md` gets the byte append check only — pre_len
   149432 and pre_lines 557 at the base, and `POST_EQUALS_PRE_NL_SLICE` for SLIPSR26.
   Report the line count it gains.

G5 THE REGISTRATION COMMIT, C4, the one commit this round cannot get wrong.
   (a) `git diff --name-only <C3> <C4>` lists EXACTLY these ten paths and nothing else:
       the six dependency files, `docs/roadmap/STATUS.md`,
       `tests/docs/test_docs_consistency.py`, `README.md`, and the NEW
       `docs/roadmap/features/T2_F274.md`.
   (b) `docs/roadmap/features/T2_F274.md` is byte-equal to the F274FILE slice. Report its
       byte length, line count and sha256. The reviewer's own copy measures 8056 bytes at
       116 lines, sha256 beginning `c880e0e119e6c3c9`; REPORT WHAT YOU MEASURE, and a
       mismatch is a DECLARED DEVIATION rather than a stop, because §3 item 37 rules the
       emitted bytes unmeasurable and only G1's saved-copy chain is a proof.
   (c) The F274 STATUS line's nearest preceding `^## Tier ` heading BEGINS `## Tier 2 —`,
       and the line IMMEDIATELY above F274's is F272's. Print the heading and both lines.
   (d) `TOTAL_FEATURES = 274` occurs exactly once, `TOTAL_FEATURES = 273` zero times, and
       each of the six dependency files contains `F274 (` exactly once.
   (e) `README.md` contains `74 of 274 registered items accepted.` and the row
       `| 2 | Minimal Self-Build Runtime | 17 | 27 |`. The Done column stays 17: F272 is
       still `[~]`, and the `[x]` flip with its README sync belongs to the closure round.

G6 THE DOCS GATE AND THE LINT. In the primary checkout at C5, run serially and report
   each exit code and count:
       python3 -B -m pytest tests/docs/ -q -p no:randomly
       python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
       python3 -m ruff check tests/docs/test_docs_consistency.py
   The reviewer ran the first two and the ruff command in a disposable worktree with C4's
   exact edits applied, measuring 303, 30 and exit 0 "All checks passed!" (ruff 0.15.17).
   The canary was NOT re-run this round; 42 is round 25's figure. REPORT WHAT YOU MEASURE.

G7 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the real output
   each time. `git ls-files .remedy-wt` empty. `git worktree list` 13 entries, unchanged
   from the base. Per-commit insertions from `git diff --numstat <parent> <commit>` for
   C0a through C5 — C6 excluded, because a commit cannot count its own insertions while
   it is being written — each under the DECISION F104 D1 cap of 500. The three
   `.agent/STOP` readings.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely: `SESSION 12 of feature F272 · round 26 · rounds
so far 26`; the soft-limit reading under amend0906-triage-throughput, which is 12 sessions
and 40 rounds and whose SESSION half THIS SESSION REACHES; one sentence of context
self-assessment; the range; a per-commit changed-files table whose `+/-` column comes from
`git diff --numstat` and is compared cell for cell against G7's figures; the item-status
table for C0a through C6; one line per gate with the transcripts below it; every deviation
and assumption. It has no length cap. It ALSO carries, in its own section, this line
exactly:

    SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

followed by the SCOPE REPORT amend0905-throughput requires at the limit: what is finished
(F272's T001, T002, T003 and the `run-loop` half of T004), what is missing (the atomic
record flip, the rest of T004, and all of T005), and the statement that the session has
EXECUTED the split-and-close default on its own authority rather than asking. Do not
re-derive the figures; they are in DECISIONs F272 D14 and D15 and in
`.agent/f272_t004_staging.md`.

<<<BEGIN PLANF272R26 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 25 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002
and T003 are COMPLETE. T004 is part-done and its remainder is being split off.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the unified model,
and the classic runner, its resolver and the prototype cluster deleted. Task slicing per
`docs/roadmap/features/T2_F272.md`. Session 12 reaches the soft limit of 12 sessions, so
this session's goal is the SPLIT-AND-CLOSE default, not more building.

## Current Step

Round 26, the split half: register the remaining scope as F274 directly after F272 per
amend0906-split-placement, in ONE atomic ledger commit, and record the move as DECISION
F272 D16 in `.agent/decisions.md`.

## Next Steps

1. F272's own Built State section, naming which slices moved to F274. Closure
   precondition 4 needs it and this file has no such section yet.
2. The integration-gate round — the full suite on the branch and at the fork point, per
   `docs/agents/integration_gate.md`. Closure precondition 2 needs it and F272 has never
   run one.
3. The self-use round closure precondition 6 requires: generate an item, since the queue
   holds no pending one, plan it, run it, register every defect string it returns.
4. The closure sequence: evidence job, fresh review zip, ledger rotation, the STATUS `[x]`
   flip with the README sync in the same commit, then the PR.
5. F274 owns the atomic record flip and the cluster deletion. None of that work starts on
   this branch.

## Risks

- Four open findings are High — R-0803, R-0804, R-0806 and R-0807. All four are booked to
  F273's T001 by the 2026-09-06 triage, so the close is PASS_WITH_RISKS and names them
  rather than pretending the set is empty.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops rather
  than closing.
<<<END PLANF272R26>>>

<<<BEGIN RECORDR26 target=.agent/live_review.md mode=append>>>
Gate: F272 R25 — the F272 round 25 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `85074909`. Range `4491ec9e`..`85074909`, seven commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, with `git diff --stat` naming exactly the seven declared paths and nothing under `packages/`, `apps/`, `tests/` or `scripts/`. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r25-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r25.md` and `.agent/last_block.md` are all 23414 bytes at 280 lines and all hash to `b9dda40e327c491305014c62b16058997f6c475298407004fa0aca3a3ea9ee92`; per §3 item 37 that chain covers those artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD: 1209111 to 1212690 bytes with the pre-image a byte-exact prefix, registrations 309 unchanged, resolutions BY DISTINCT ID 252 unchanged, open set 57 unchanged, `^Gate: ` 47 to 48, `^Gate: F272 R24 ` 0 to 1 and `^- R-0826 ` 0 to 0 — the exact shape a round that mints and resolves nothing must have. G3 THE PLAN is 2545 bytes at 47 lines against the cap of 50 and byte-equal to its slice. G4 THE FEATURE FILE went 58026 to 62897 bytes with the pre-image a byte-exact prefix, the DECISION headings 14 to 15, the numbers reading exactly 1 through 15 each once and in order, and D14's own body byte-unchanged. G5 THE DOCS GATE is EXIT 0 at 375 passed — 303, 30 and 42 — matching the reviewer's pre-measured figures cell for cell. G6 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, per-commit insertions at a maximum of 280 against the DECISION F104 D1 cap of 500. ALL THREE OF THE WORKER'S DECLARED DISAGREEMENTS ARE UPHELD AND ALL THREE ARE THE REVIEWER'S ERRORS RATHER THAN THE WORKER'S, each applied verbatim and declared instead of silently corrected: constraint 4's claim that all three append targets hold ZERO occurrences of three consecutive newlines is FALSE for `.agent/prose_slips.md`, which holds one at byte offset 39213; G4's order to compare D14's span "against the same span at the base commit" is not literally satisfiable, because at the base there is no D15 heading, so the two spans differ by exactly the newline the append itself contributes; and the PLANF272R25 slice opened "Rounds 1 to 25 PASSED" while round 25 was the round applying it and had no verdict, which is the §3 item 20 class, that item's carve-out reaching a claim about the round's own COMMITS and not one about its own VERDICT. Under amend0827 rule 2 all three are reviewer prose that left nothing wrong on disk, so each is one dated line in `.agent/prose_slips.md` with no id, no severity and no correction round, and they are the three lines the round 26 SLIPSR26 slice appends. THE FIRST OF THEM IS ALREADY DISCHARGED BY THE ROUND THAT BOOKS THIS ENTRY: round 26's block measured the triple-newline count PER FILE for each of its three append targets rather than generalising from one, and found 0, 1 and 5, the 5 being in `.agent/decisions.md`, a file round 25 never touched.
<<<END RECORDR26>>>

<<<BEGIN SLIPSR26 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 25 — the block's constraint 4 stated that all three append targets contain zero occurrences of three consecutive newlines; `.agent/prose_slips.md` contains one, at byte offset 39213, and the reviewer had measured that very count earlier in the same session before generalising from the other two files. A property asserted over a SET of files is measured over every member of the set, never over the members that were convenient to read.

2026-09-07, F272 round 25 — G4 ordered a section's bytes compared "against the same span at the base commit" where the span's end anchor is a heading THIS ROUND creates, so at the base the span can only run to end of file and the two differ by the separator the append itself contributes. A span whose end anchor the round introduces cannot be delimited the same way before and after; name the anchor that exists at both commits, or compare to end of file deliberately and say so.

2026-09-07, F272 round 25 — the PLANF272R25 slice opened "Rounds 1 to 25 PASSED" while round 25 was the round applying it and had no verdict; §3 item 20's carve-out covers a claim about the round's own COMMITS and not one about its own VERDICT, which only the reviewer writes. A state slice describes the round it is written for in the present tense and never books its outcome in advance.
<<<END SLIPSR26>>>

<<<BEGIN D16SLICE target=.agent/decisions.md mode=append>>>
## DECISION F272 D16 — F272 closes at a self-consistent scope and its remainder becomes F274 (2026-09-07)

CONTEXT. Session 12 of F272 reaches the soft limit operator amendment amend0906-triage-throughput rule 2 set for this feature by name: 12 SESSIONS and 40 ROUNDS. The session half is reached at session 12; the round half is not, this being round 26 of 40. Operator amendment amend0905-throughput makes the standing default at that limit SPLIT-AND-CLOSE, EXECUTED BY THE SESSION on its own authority, with the whole move recorded as a dated DECISION the operator may reverse afterwards. This is that DECISION. It is not a question and it does not wait for an answer.

WHAT IS FINISHED, from the ledger rather than from recollection. F272's T001 (the plural run list and the run re-key), T002 (the rest of the unified record) and T003 (the consumer list) are COMPLETE across rounds 1 to 19, every round PASSED except round 2, whose premise DECISION F272 D2 corrected, and round 21, repaired by round 22. Of T004, rounds 20 to 22 deleted `job run-loop`, its handler, its tests and its two prose advertisements.

WHAT IS NOT FINISHED, and why it cannot be finished here. The rest of T004 is the classic-to-unified record flip, which DECISION F272 D15 measured at round 25 by RUNNING the shipped functions: `Job` and `JobPlan` now differ in `id` and `name` alone, and `.id` sits on `assess_job_readiness` (seven call sites in seven modules) and `recommend_worker` (six in six), so moving any one consumer forces those helpers to accept a `JobPlan` and forces every other caller of them to pass one — a closure that does not terminate before it has taken in the whole consumer graph. A helper accepting both records is the compatibility reader AGENTS.md's Scope Control forbids by name. The flip is therefore ATOMIC, and an `ast` bound of 468 production and 1545 test `.id` reads exceeds the DECISION F104 D1 cap of 500 insertions for one commit, while a half-flipped tree is red at a commit boundary. T005, the deletion round, has not begun, and its Orchestrator brief forbids splitting it.

CHOSEN. F272 CLOSES AT T001, T002, T003 AND THE `run-loop` HALF OF T004 — a scope that is self-consistent because every slice in it is complete and green, and nothing in it depends on the flip. The remainder becomes F274, "One world completion, part two — the atomic record flip and the cluster deletion", registered in this same round in ONE atomic ledger commit: the STATUS line directly after F272's and inside the same `## Tier 2` heading per operator order amend0906-split-placement, the feature file `docs/roadmap/features/T2_F274.md`, the `TOTAL_FEATURES` pin at 274, the README accepted-count line and the Tier 2 Total cell, and the "Depends on" line of every open feature file that names F272 — F261, F263, F268, F269, F270 and F271. F274's file names the parent, points at F272's own accepted STATUS line for the closure evidence it starts from rather than copying it, and carries F272's T004 remainder and T005 as slices copied from the parent rather than re-planned.

F274 CARRIES ONE ADDITION AND IT IS DELIBERATE: its first slice is not the flip but the DECISION F272 D7 raising-property probe that turns D15's receiver-name BOUND into a real site set, followed by an operator-visible ruling on how an atomic change is landed under a per-commit cap that forbids it. D15's CONSEQUENCE clause names that question as the one F272 cannot answer on its own authority, and a feature that starts flipping sites before it is answered repeats the mistake D14 part 2 made.

ALTERNATIVES CONSIDERED. Running F272 past its limit to finish T004 — rejected: amend0906 set 12-and-40 for this feature after measuring it as the largest of its block, and that amendment says in terms that a second split would only mint another id with the same remainder, so the limit is a ruling and not a suggestion. Stopping with an operator question instead of executing the default — rejected: amend0905-throughput reserves that for the case where no self-consistent close is possible, and F262's round 23 already spent a session waiting for a ruling the default supplies. Closing F272 as `[!] blocked` — rejected: nothing is blocked; three task slices are complete and shippable, and `[!]` would misdescribe a feature that delivered them. Folding the remainder into F273 (findings paydown) or F271 (no more legacy) — rejected: neither owns the record boundary, and amend0906-split-placement requires the remainder of F<p> to sit directly after F<p> so Rule A5 proposes it next.

CONSEQUENCE. F272 becomes `[x]` at a scope its own Built State section states in terms, naming which slices moved to F274, and Rule A5 proposes F274 as the next feature. The atomic flip is not attempted anywhere on this branch. REVERSE by deleting this section, the F274 STATUS line, `docs/roadmap/features/T2_F274.md`, the six dependency additions and F272's Built State section, and returning the ledger pin to 273 with the two README figures, at which point F272 is `[~]` again with its remainder unowned.
<<<END D16SLICE>>>

<<<BEGIN STATUSPAIR_FROM target=docs/roadmap/STATUS.md>>>
- [~] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion
<<<END STATUSPAIR_FROM>>>

<<<BEGIN STATUSPAIR_TO target=docs/roadmap/STATUS.md>>>
- [~] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion
- [ ] F274 — One world completion, part two — the atomic record flip and the cluster deletion
<<<END STATUSPAIR_TO>>>

<<<BEGIN DEPPAIR_FROM target=SIX_DEPENDENCY_FILES>>>
F272 (one world completion — the run re-key, the consumers, the classic runner and the cluster deletion)
<<<END DEPPAIR_FROM>>>

<<<BEGIN DEPPAIR_TO target=SIX_DEPENDENCY_FILES>>>
F272 (one world completion — the run re-key, the consumers, the classic runner and the cluster deletion), F274 (one world completion part two — the atomic record flip and the cluster deletion)
<<<END DEPPAIR_TO>>>

<<<BEGIN PINPAIR_FROM target=tests/docs/test_docs_consistency.py>>>
#: .agent/triage_2026-09-06.md.
TOTAL_FEATURES = 273
<<<END PINPAIR_FROM>>>

<<<BEGIN PINPAIR_TO target=tests/docs/test_docs_consistency.py>>>
#: .agent/triage_2026-09-06.md. One more, F274 (one world completion part
#: two: the atomic record flip and the cluster deletion), was registered on
#: 2026-09-07 by DECISION F272 D16, which split it off F272 at the
#: amend0906-triage-throughput soft limit of 12 sessions and placed it
#: directly after its parent per amend0906-split-placement; see T2_F274.md.
TOTAL_FEATURES = 274
<<<END PINPAIR_TO>>>

<<<BEGIN READMEPAIR_FROM target=README.md>>>
74 of 273 registered items accepted.
<<<END READMEPAIR_FROM>>>

<<<BEGIN READMEPAIR_TO target=README.md>>>
74 of 274 registered items accepted.
<<<END READMEPAIR_TO>>>

<<<BEGIN TIERPAIR_FROM target=README.md>>>
| 2 | Minimal Self-Build Runtime | 17 | 26 |
<<<END TIERPAIR_FROM>>>

<<<BEGIN TIERPAIR_TO target=README.md>>>
| 2 | Minimal Self-Build Runtime | 17 | 27 |
<<<END TIERPAIR_TO>>>

<<<BEGIN F274FILE target=docs/roadmap/features/T2_F274.md mode=create>>>
# T2_F274 — One world completion, part two — the atomic record flip and the cluster deletion
**Tier 2 · Depends on: F259 (the binding concept model, `docs/system/vocabulary.md`), F260 (the one job record and the one id shape it closed at), F272 (the run re-key, the rest of the unified record and the migrated consumer list it closed at) · Blocks/used by: F261, F266, F268, F269, F270, F271, F263 — everything later that names a job, a run or a command**

> Registered 2026-09-07 by DECISION F272 D16 in `.agent/decisions.md`, which split the
> remaining scope off F272 at the amend0906-triage-throughput soft limit of 12 sessions
> and 40 rounds, and placed this line directly after its parent per operator order
> amend0906-split-placement. The closure evidence this feature starts from — the accepted
> HEAD, the evidence job, the package name and its SHA-256 — is recorded on F272's own
> accepted line in `docs/roadmap/STATUS.md` and deliberately not copied here, because a
> second copy of a value drifts and the ledger line is the durable carrier.
> REGISTRATION ONLY — nothing in this file has been implemented.

## Goal & Done
Finish what F272 could not reach inside its own limit. F272 spent F260's settlement: the
plural run list and the run re-key landed, the rest of the unified record landed, the
consumer list moved, and `job run-loop` was deleted with its advertisements. What is left
is the part DECISION F272 D15 measured and ruled ATOMIC — the classic-to-unified record
flip — and the deletion round F272's Orchestrator brief forbade splitting.

DONE when the three task slices below hold, and when DECISION F260 D3, the deletion
paragraph, exists and names every deleted module and the feature that inherited its idea.
That paragraph is still owed, because the deletion round it belongs to is carried here.

## Why this exists
Not because F272 was wrong, and not because anything it built is being redone. F272
reached the soft limit of 12 sessions with its T004 still open, and the
amend0905-throughput split-and-close default closed it at a self-consistent scope rather
than running past the limit or attempting a change its own budget forbids. Every ruling
F272 recorded stays binding here and is NOT restated: read
`docs/roadmap/features/T2_F272.md`, whose DECISIONs are kept unedited for exactly this
purpose, and whose Built State section records what is already on disk. Three of them are
this feature's starting conditions, named here so a reader finds them without a search:

- **DECISION F272 D13** — a command's ADVERTISEMENTS are deleted in the same commit as
  the command.
- **DECISION F272 D14 parts 1 and 3** — the twelve cluster-bound consumers are never
  migrated, and `job.run-next` dies WITH the rails rather than ahead of them. Part 2 of
  D14 is superseded by D15 and does not bind here.
- **DECISION F272 D15** — the classic-to-unified flip is ATOMIC over the consumer graph,
  because `.id` is the last gap between `Job` and `JobPlan` and it sits on helpers with
  seven and six call sites. It is not stageable by caller, and a helper accepting both
  records is the compatibility reader AGENTS.md's Scope Control forbids by name.

## T001 — Measure the flip, then rule the cap
THE FIRST SLICE IS NOT THE FLIP, because DECISION F272 D15's CONSEQUENCE clause leaves one
question F272 could not answer on its own authority: **how is a change that is atomic by
construction landed under a per-commit cap of 500 insertions that forbids it?** D15
measured the bound — an `ast` sweep over 1068 tracked `.py` files gives 468 `<job-ish>.id`
reads in 74 production files and 1545 in 137 test files — and recorded in terms that this
is an UPPER BOUND from a receiver-name heuristic and NOT a probe measurement, `.id` being
polymorphic here exactly as `.status` was.

So: the DECISION F272 D7 raising-property probe over every candidate `.id` receiver,
giving the real site set rather than the bound; then a dated DECISION in
`.agent/decisions.md` choosing the route, with alternatives considered and how to reverse,
per planner_reviewer_prompt.md §4 item 7. Three routes exist and none may be chosen by
assumption: the real set proves small enough for one commit; the one oversize commit
AGENTS.md's Commit Discipline permits per feature is declared, with the inseparability
reason stated in the handback before review; or an operator amendment is obtained. A
feature that starts flipping sites before that ruling lands repeats exactly the mistake
DECISION F272 D14 part 2 made. No production line moves in this slice.

## T002 — Delete the classic runner (carried over from F272's T004)
The text below is F272's T004 verbatim:

> `job.run --cycles`, `job.run-next`, `job.run-loop`, their handlers and tests; the
> resolver collapse DECISION F260 D5 placed here, in the SAME commit range that
> deletes the classic store, because the collapse is a behaviour change to a shared
> error path and is harmless only once that store is gone; `resolve_any_job_id`, the
> "TWO job stores" paragraph, every which-store branch, and the absence test.

ALREADY LANDED IN F272 and therefore NOT owed here: `job run-loop`, its handler, its tests
and its two prose advertisements, deleted across F272's rounds 20 to 22 (ledger
`Gate: F272 R20` to `Gate: F272 R22`). Everything else in that paragraph is owed here, and
the atomic flip T001 rules is the prerequisite for all of it.

## T003 — Reachability test and cluster deletion (carried over from F272's T005; last, never split)
The text below is F272's T005 verbatim; nothing in it landed in F272:

> The D11c reachability test in `tests/`, run and green BEFORE deletion; the two
> carry-overs F260's Design section names; DECISION F260 D3 drafted; then the
> deletion of every module, handler, catalog entry, `ui_server.py` section and test
> that section lists, one commit per module group. A module that turns out to be
> REACHABLE is reported with its import chain, never deleted.
> Resolve every finding tagged deletion-bound for this feature in the same commit
> as the deletion (`.agent/triage_2026-09-06.md` lists them). At that triage's own
> sweep the list for this feature was EMPTY — no open finding's repair is
> discharged by these deletions — so the sentence binds any finding tagged later
> rather than describing work owed today.

## Acceptance
THE ACCEPTANCE LIST OF THIS FEATURE IS THE ONE IN
`docs/roadmap/features/T2_F260.md`, IN FULL AND UNCHANGED, minus the items F272's Built
State section records as reached at its close. It is referenced rather than copied for the
reason F272's own Acceptance section gives: a second copy of a contract is a copy that
drifts, and F260's file keeps that section unedited on purpose. The five ids that section
names — R-0803, R-0804, R-0807, R-0810 and R-0812 — are F273's and NOT this feature's, per
DECISION F272 D12, which the split leaves unchanged and which binds here identically.

## Do not touch
Everything F272's own "Do not touch" section names, unchanged: the scope-fence builtin
deny list (F017), the approval gate, STATUS semantics. No command is RENAMED here — F261
owns renames. No module outside F260's Design lists is deleted.

## Orchestrator brief
T001 FIRST AND ALONE, because every later commit's size depends on its ruling. Then T002,
then T003 LAST as the deletion round with the reachability test run before the first
`git rm`. F260's brief prohibition binds here unchanged and is the one hard rule of the
sequencing: NEVER SPLIT INSIDE T003. A half-performed deletion is the single state this
work must not leave behind, so a session reaching its own soft limit splits between T002
and T003, and never within T003.

T002 and T003 are deletion rounds under amend0906-triage-throughput, so each is verified by
that paragraph's four measurements and nothing else. This feature's soft limit is the
standing 7 sessions and 25 rounds: amend0906 granted 12-and-40 to F272 BY NAME, on a
measurement of F272's scope, and such a grant does not travel with a split.
<<<END F274FILE>>>
