STEP CLOSURE 6/6 — F272 — round 31 — the closure commit and the pull request

Base commit for every reading in this block: `e388c603`, the round 30 handback commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

THIS IS THE LAST ROUND ON THIS BRANCH. Closure algorithm steps 4 and 5 of
`docs/roadmap/STATUS_closure_protocol.md`: the STATUS `[x]` line the reviewer authors and
you apply verbatim, the README capability sync that must land in the SAME commit as it
(R-0154 — README and STATUS may never disagree in any committed state), SU-012's
`consumed_by`, the final handoff, and then the pull request.

THE PULL REQUEST IS NOT MERGED THIS SESSION. It merges at the next feature's start through
the AGENTS.md Open PR Gate, and that gap is the operator's manual-review window. Creating it
and merging it in the same session is forbidden by self_drive_protocol.md guardrail G1.

EVERY VALUE IN THE STATUS LINE WAS MEASURED IN ROUND 30 AND RE-VERIFIED BY THE REVIEWER,
who recomputed the package's sha256 from the file on disk and read the packaged manifest
itself rather than the worker's report of it: evidence job `abf14422b1badab6`; package
`remedy-review-20260907-173909-READY_FOR_REVIEW.zip` at 25675030 bytes hashing to
`8bbce2fa27ddd6c68398d381d1367e6e509b49cbacac0a29ff06329d9aebb706`; archived at
`/home/decodeux/Repos/remedy-history/zips`; `PACKAGE_STATUS` READY_FOR_REVIEW with
`packaging_warnings` and `external_paths_detected` both empty; and the manifest's
`committed_review_subject` spanning `b18fad576252f7f2739a5807b6408031da8fcde6` to
`7f71b30ac3b2f1fefb2da6063f0453d650d3835a`, which is the ACCEPTED HEAD.

THE CLOSE IS `PASS_WITH_RISKS` AND IT NAMES ITS RISKS. Five High findings are open —
R-0803, R-0804, R-0806, R-0807 and R-0827 — and DECISION F272 D17 rules why that is the
honest close rather than a stop. `remedy integrity check` passes while its
`high_blockers_open` check reports "no open blocker/high findings", which is false and is
the already-open R-0648; the PR body says so rather than leaning on it.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r31.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R31
C2   `.agent/live_review.md` — append RECORDR31, the round 30 PASS gate entry
C3   `.agent/prose_slips.md` — append SLIPSR31, one dated line
C4   `.agent/decisions.md` — append D18SLICE
C5   THE CLOSURE COMMIT — `docs/roadmap/STATUS.md`, `README.md`,
     `scripts/self_use_queue.json` and `.agent/handoff.md`, ALL IN ONE COMMIT, and it is
     the LAST commit on this branch
THEN the pull request, created but NOT merged.

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r31.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/decisions.md
    docs/roadmap/STATUS.md
    README.md
    scripts/self_use_queue.json
    .agent/handoff.md

NOTHING under `packages/`, `apps/`, `tests/` or `docs/` other than `docs/roadmap/STATUS.md`
changes. No production line moves, so no red-proof is ordered or possible. The last four
paths belong to C5 and to no other commit. If a measurement forces a path outside this list,
APPLY IT AND DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice or a pair is wrong, apply it as written and
   declare the disagreement; never silently correct it.
2. Every authored text is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r31.md`. The BEGIN marker line begins `<<<BEGIN <NAME> ` and
   CARRIES a `target=` attribute after the name, so match it by that PREFIX and never by an
   exact-line equality; the END marker line is exactly `<<<END <NAME>>>`. A WHOLE TEXT —
   `PLANF272R31`, `RECORDR31`, `SLIPSR31`, `D18SLICE` — is read INCLUSIVE of the newline
   ending its last content line. A PAIR HALF, every name ending `_FROM` or `_TO`, is read
   with that final newline STRIPPED. Never retype a slice.
3. C0a and C0b are `shutil.copyfile` of `.remedy-wt/f272-r31-block.md`.
4. EVERY PROSE APPEND IS `post == pre + b"\n" + slice`. Each target ends in EXACTLY ONE
   newline at the base, measured per file: three consecutive newlines at `e388c603` occur 0
   times in `.agent/live_review.md`, 1 time in `.agent/prose_slips.md` and 5 times in
   `.agent/decisions.md`. All pre-existing, none load-bearing, none repaired.
5. C5 IS ONE COMMIT AND IT IS THE LAST ON THE BRANCH. Rule A4 and closure algorithm step 5
   both require the STATUS edit to be the final commit, and R-0154 requires the README
   capability sync to sit in the SAME commit as it, because README and STATUS may never
   disagree in any committed state. Do NOT split C5, and do NOT add a commit after it. The
   handoff rewrite belongs INSIDE C5 as the closure protocol's "final .agent/ state".
6. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. `R-0829` is the next free id and must
   still be free at the end. The open set must read 60 by distinct id at every commit.
7. NO WORKTREE IS CREATED OR REMOVED. `git worktree list` is 14 entries and must still be 14
   at the end.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C5 and before the PR is
   created, and report all three readings.
9. THE PULL REQUEST IS CREATED AND NEVER MERGED. `gh pr create` targeting `main` from this
   branch. Do NOT run `gh pr merge`. Do NOT force-push, rewrite history, delete a branch or
   commit on `main`.
10. Commit subjects are `f272: <what>` and carry no leading-slash token, no absolute path and
    no secret-like string. THE STATUS LINE ITSELF CONTAINS AN ABSOLUTE PATH — the package
    path segment — and that is required by the closure template and is fine INSIDE the file;
    it must not appear in a commit SUBJECT.

====================
The pairs — each classified by a containment test the reviewer RAN
====================

The reviewer ran `TO.find(FROM) >= 0` on the final bytes under constraint 2's pair
convention; each output is recorded below and the label is DERIVED from it on the same line.
All five are REWRITES, so each carries the FROM 0x / TO 1x obligation and none carries an
append obligation.

    STATUSPAIR      TO contains FROM: false  -> REWRITE   docs/roadmap/STATUS.md
    READMECOUNTPAIR TO contains FROM: false  -> REWRITE   README.md
    READMETIERPAIR  TO contains FROM: false  -> REWRITE   README.md
    READMECAPPAIR   TO contains FROM: false  -> REWRITE   README.md
    QUEUEPAIR       TO contains FROM: false  -> REWRITE   scripts/self_use_queue.json

Every FROM occurs EXACTLY ONCE in its target at `e388c603`; the reviewer counted each.

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, NO PIPE between the command and
the echo. Report ONE LINE PER GATE with the transcripts below it. Every gate runs at or
before C5, so the handback inside C5 can quote all of them.

G1 TRANSPORT. One digest comparison: `.remedy-wt/f272-r31-block.md` as delivered against the
   committed `.agent/authored/f272-r31.md` and the committed `.agent/last_block.md`. Report
   sha256, byte length and line count for each of the three.

G2 THE FINDING RECORD, over the single append at C2, against its own pre-image.
   (a) BYTE: pre_len, pre_sha256, post_len, post_sha256, the terminal twelve bytes and
       trailing-newline run of each, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and
       `POST_EQUALS_PRE_NL_SLICE`. At `e388c603` the pre-image is 487792 bytes, 535 lines,
       sha256 beginning `90bb842f424f8dea` — it is SMALL because round 30 rotated it.
   (b) STRUCTURAL: strip the single terminal newline, split on blank lines, compare the LAST
       N units against the slice's paragraphs IN ORDER, N COUNTED BY YOUR SCRIPT from the
       slice. Report N, units before, units after and `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST paragraph the append adds, in memory only, never on
       disk: flip one byte, require BOTH readers to reject it, then re-read the file and
       confirm it is byte-identical to the real post-image.
   (d) COUNTS: `^- R-\d{4}` distinct 62 -> 62, `^Done: R-\d{4}` distinct 2 -> 2, open set BY
       DISTINCT ID 60 -> 60, `^Gate:` 30 -> 31, `^Gate: F272 R30 ` 0 -> 1, `^- R-0829 `
       0 -> 0. Report the open-set arithmetic.

G3 THE TWO PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R31; report its bytes, its
   line count against the AGENTS.md cap of 50, and that `## Goal` and `## Next Steps` are
   both present. `.agent/prose_slips.md` gets the byte append check only — pre_len 153776 and
   pre_lines 571 at `e388c603`, and `POST_EQUALS_PRE_NL_SLICE` for SLIPSR31.

G4 THE DECISION RECORD at C4. Report pre_len, pre_sha256, post_len, post_sha256,
   `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`. At `e388c603` the
   pre-image is 869442 bytes and 10887 lines. Report `^## DECISION F272 D` 2 -> 3 and confirm
   `^## DECISION F272 D18 ` heads exactly one section.

G5 THE CLOSURE COMMIT, C5 — the one commit this feature cannot get wrong.
   (a) `git diff --name-only <C4> <C5>` lists EXACTLY these four paths and nothing else:
       `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json`,
       `.agent/handoff.md`.
   (b) For each of the five pairs report, in this order: the FROM count BEFORE the edit,
       which is 1; the FROM count AFTER, which is 0; the TO count AFTER, which is 1; and the
       boolean that the post-commit file equals the pre-commit file with that ONE replacement
       applied and NOTHING else.
   (c) The F272 STATUS line in the post-image is BYTE-EQUAL to the STATUSPAIR_TO slice.
       Report its byte length and print the whole line.
   (d) `^- \[~\] ` occurs ZERO times in `docs/roadmap/STATUS.md` after C5 — F272 was the only
       `[~]` line and it is now `[x]`. Report the count and the count of `^- \[x\] F272 `,
       which is 1.
   (e) `README.md` reads `75 of 274 registered items accepted.` and the row
       `| 2 | Minimal Self-Build Runtime | 18 | 27 |`, and the string `F272` occurs in the
       "Accepted in Tier 2 so far:" block exactly once. Every F-id inside every
       `Accepted...:` block is `[x]` in STATUS — report any that is not, which must be none.
   (f) SU-012's `consumed_by` is `F272` and EVERY other item's `consumed_by` is unchanged;
       `pending_self_use_items()` is now EMPTY, read through the shipped reader. Report the
       item count, which is still 12, and `schema_version`, which is still 2.
   (g) The file still parses: `json.loads` succeeds on `scripts/self_use_queue.json`.

G6 THE LEDGER GATES, run SERIALLY in the primary checkout at C5:
       python3 -B -m pytest tests/docs/ -q -p no:randomly
       python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
       python3 -B -m pytest tests/orchestration/test_self_use_queue.py -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   The reviewer applied these exact five edits in a disposable worktree at `e388c603` and
   measured 303, 30 and 23 for the first three, and 42 for the canary at `b865f001`. It also
   confirmed BOTH README pins can FAIL: putting the Tier 2 Done cell back to 17 while F272 is
   `[x]` reddens `test_the_readme_tier_table_done_column_matches_the_ledger`, and putting the
   accepted count back to 74 reddens `test_the_readme_accepted_count_equals_the_status_count`
   — one failure each, so neither pin is a gate that cannot fail. REPORT WHAT YOU MEASURE.

G7 THE TREE AND THE PULL REQUEST. `git status --porcelain` EMPTY at every commit boundary
   with the real output each time. `git ls-files .remedy-wt` empty. `git worktree list` 14
   entries, unchanged. Every commit single-parent. Per-commit insertions from
   `git diff --numstat <parent> <commit>` for C0a through C4 — C5 excluded, because it
   carries the handoff that would have to count itself — each under the DECISION F104 D1 cap
   of 500. Push. Then `gh pr create` and report the PR NUMBER and URL, and `gh pr list
   --state open --json number,headRefName,baseRefName,isDraft` showing it open, targeting
   `main`, from this branch and NOT a draft. Report that `gh pr merge` was NOT run. The three
   `.agent/STOP` readings.

====================
The pull request — its body is ordered, not left to you
====================

Title: `F272 — One world completion: the run re-key, the unified record and the migrated consumers`

The body carries, under headings of your choosing: WHAT CHANGED and WHY; the KEY DECISIONS,
naming DECISION F272 D1 through D18 and saying that D16 split the remainder into F274, D17
rules the PASS_WITH_RISKS close and D18 rules the rotation commit's size; HOW TO REVIEW,
naming the package filename, its SHA-256, its absolute directory and the accepted HEAD; a
CHANGED-FILES table for the whole branch from `git diff --stat b18fad57..<C5>`; the LATEST
VERDICT, `PASS_WITH_RISKS`; the OPEN-FINDINGS COUNT of 60 by distinct id WITH the five open
High ids named — R-0803, R-0804, R-0806, R-0807, R-0827 — and F273 named as their owner; the
statement that `remedy integrity check` passes while its `high_blockers_open` check reports
"no open blocker/high findings" and that this is the open finding R-0648, so the close rests
on the named list and not on that check; and RUNTIME ACTUALS — 31 rounds across 12 sessions,
the integration gate at 19786 passed and 23 skipped in 115.98s on the branch against 126
attributed environment-class failures at the fork point, the self-use run at six ollama
`muse-glimmer:latest` provider calls in 251.76s, and wall clock and cost `not-measured`,
which beats a guess.

Say plainly in the body that the PR is NOT to be merged by this session and merges at the
next feature's start through the Open PR Gate.

<<<BEGIN PLANF272R31 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 30 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004's remainder and T005 are F274's, split off in round 26 by DECISION
F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Every closure precondition
of `docs/roadmap/STATUS_closure_protocol.md` is now met: the integration gate ran in round
27 with zero branch-only failures, the self-use item was run in round 28 and its defects
registered in round 29, and round 30 rotated the ledger and built a READY_FOR_REVIEW package.

## Current Step

Round 31, the last round on this branch: the closure commit — the STATUS `[x]` line, the
README capability sync and SU-012's `consumed_by` in ONE commit, with the final handoff —
and then the pull request, which is NOT merged this session.

## Next Steps

1. The PR merges at the NEXT feature's start through the AGENTS.md Open PR Gate. That gap is
   the operator's manual-review window, and guardrail G1 forbids this session merging a PR
   it created.
2. Rule A5 then proposes F274, which sits directly after F272 by amend0906-split-placement
   and owns the atomic record flip and the cluster deletion.
3. F274's first slice is the DECISION F272 D7 raising-property probe and a ruling on the
   per-commit cap, NOT the flip itself.

## Risks

- Five open High findings — R-0803, R-0804, R-0806, R-0807 and R-0827 — all owned by F273,
  whose own Done clause covers "anything registered after 2026-09-06". DECISION F272 D17
  rules why the close names them rather than waiting.
- `remedy integrity check` passes while its `high_blockers_open` check is vacuous; that is
  the open R-0648 and the PR body states it.
<<<END PLANF272R31>>>

<<<BEGIN RECORDR31 target=.agent/live_review.md mode=append>>>
Gate: F272 R30 — the F272 round 30 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `e388c603`. THIS IS THE ROUND THAT ROTATED THE LEDGER AND BUILT THE CLOSURE PACKAGE. Range `c286fd92`..`e388c603`, seven commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, with `git diff --name-only` naming exactly the seven declared paths and — the reviewer checked this specifically — naming NONE of `docs/roadmap/STATUS.md`, `README.md` or `scripts/self_use_queue.json`, all three of which belong to the closure commit in round 31. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r30-block.md` and the committed `.agent/authored/f272-r30.md` and `.agent/last_block.md` are all 23472 bytes at 304 lines and all hash to `6a94bb428eb5d56377b8aa688fd242fa8c5afd040e89b4c6f6e7ea24c01ccf05`; per §3 item 37 that chain covers those artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD: 1238279 to 1242594 bytes, prefix and ordered equality true, structural N counted from the slice as 1 with units 738 to 739, a byte flipped in the first appended paragraph rejected by both readers, registrations 312 unchanged, resolutions 252 unchanged, open set 60 unchanged, `^Gate: ` 52 to 53 and `^Gate: F272 R29 ` 0 to 1. G4 THE ROTATION IS THE ROUND'S CENTRAL ACT AND IT IS CLEAN: the ledger went 1242594 to 487792 bytes and the archive 1780229 to 2535031, and the reviewer independently confirms the archive's pre-image is a BYTE-EXACT PREFIX of its post-image, that the archive gained EXACTLY the 754802 bytes the ledger lost, that the commit's path set is exactly the two ledger files, and that the open set is 60 before and 60 after by distinct id and 58 before and 58 after by the script's own line formula — the two differing only because R-0721 and R-0725 each carry a two-paragraph resolution, so the file holds 254 `Done: ` LINES against 252 distinct ids. All thirty `^Gate: F272 R` records STAYED, which is correct because F272 is still `[~]` and the script moves only a `[x]` feature's records; total `^Gate: ` went 53 to 30. G5 THE BASE PROOF WAS RE-DERIVED BY THE REVIEWER AND NOT ACCEPTED ON REPORT: at the fork point `b18fad576252f7f2739a5807b6408031da8fcde6`, `rev-list --ancestry-path <base>..<head>` and plain `rev-list <base>..<head>` both answer 243 and the base is an ancestor of `main`, while `git merge-base` answers `148fbd0b` and is NOT the fork point — the inequality that packaged F260's round 22 as BLOCKED_EVIDENCE. G6 THE PACKAGE WAS VERIFIED BY THE REVIEWER FROM THE ARTEFACT ITSELF: the zip on disk is 25675030 bytes and the reviewer recomputed its sha256 as `8bbce2fa27ddd6c68398d381d1367e6e509b49cbacac0a29ff06329d9aebb706`, matching the worker's reading; reading `.review_zip_manifest.json` out of the archive gives `package_status` READY_FOR_REVIEW, `packaging_warnings` empty, `external_paths_detected` empty, `final_verifier_reproducible` true, `packaged_evidence_job_id` `abf14422b1badab6`, and a `committed_review_subject` whose base is the fork point and whose head is `7f71b30ac3b2f1fefb2da6063f0453d650d3835a` with `base_is_ancestor` true. G8 THE TREE: porcelain empty at every boundary, `git ls-files .remedy-wt` empty, worktrees 14 and unchanged, no pull request created. THE WORKER MADE THREE DECLARATIONS AND THE REVIEWER SUSTAINS TWO AND OVERTURNS ONE. SUSTAINED: the block's G5 named `packages.orchestration.build_review_manifest`, which raises `ModuleNotFoundError` — the real module is `scripts/build_review_manifest.py`, carrying `_unsafe_text` at line 1767 and `_VT_RUN_ID_RE` at line 2120, both confirmed by the reviewer — and the worker used the real one and proved the failed import in the same script; that is the reviewer's error and is a dated prose-slip line. SUSTAINED: C4, the rotation, is 1612 insertions against the DECISION F104 D1 cap of 500, and the worker was right that D1's exemption names the rewrite of a SINGLE `.agent/**` state file while the rotation necessarily touches TWO, so the clean route is AGENTS.md's declared-oversize exception, which the worker took and declared with its inseparability reason before review; the reviewer measured every commit on this branch since the fork point and confirms this is the ONLY commit needing that exception, so condition (b) of the exception holds — the two merge commits are merges rather than authored diffs, and the two handback commits at 637 and 570 insertions are single-file `.agent/**` rewrites D1 exempts by name. OVERTURNED, AND THE REVIEWER MEASURED IT RATHER THAN ASSERTING IT: the worker reported that the single triple-newline in `.agent/prose_slips.md` sits at byte offset 38927 and not the 39213 the block stated. `re.finditer(rb"\n\n\n", ...)` over the file returns exactly one match and its start offset is 39213, with the surrounding bytes reading `o R-id spent (amend0827-process-diet rule 2).` immediately before it, while offset 38927 falls in the middle of an unrelated word. THE BLOCK'S FIGURE WAS RIGHT AND SO IS THE LANDED PROSE-SLIP LINE THAT CARRIES IT; no correction is owed and none is made. The worker also declared a stale numeral inside its own committed handback, 563 where the final count is 570, which is a non-load-bearing inaccuracy in a handback and under amend0827 rule 2 is a deviation rather than a round or an id.
<<<END RECORDR31>>>

<<<BEGIN SLIPSR31 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 30 — the block's G5 ordered a pre-scan through `packages.orchestration.build_review_manifest._unsafe_text`, and that module does not exist: the importable one is `scripts/build_review_manifest.py`, whose `_unsafe_text` is at line 1767. The reviewer took the dotted path from `docs/roadmap/STATUS_closure_protocol.md`, which names `build_review_manifest._VT_RUN_ID_RE` with no package prefix, and supplied a prefix by analogy with the neighbouring `packages.orchestration.job_evidence` rather than by resolving it. A module path in a gate is an IMPORT the worker must execute, so it is resolved by importing it before emission, never inferred from a sibling's namespace.
<<<END SLIPSR31>>>

<<<BEGIN D18SLICE target=.agent/decisions.md mode=append>>>
## DECISION F272 D18 — the mandated ledger rotation exceeds the per-commit insertion cap by construction, and travels under the declared-oversize exception once per feature (2026-09-07)

CONTEXT. Operator amendment amend0905-throughput makes `scripts/rotate_live_review.py` a step of EVERY closure sequence, run as its OWN commit whose path set is exactly `.agent/live_review.md` and `.agent/live_review_archive.md`. At F272's closure that commit moved 754802 bytes and counted 1612 insertions, against the AGENTS.md DECISION F104 D1 cap of 500 insertions per commit. The two rules cannot both be satisfied: the rotation is atomic by construction — the script verifies every moved record by sha256 on both sides and refuses on any mismatch — and splitting it would leave records in neither file or in both, corrupting the append-only record the step exists to preserve.

D1's OWN EXEMPTION DOES NOT REACH IT, AND THIS IS THE PART WORTH WRITING DOWN. D1 exempts "a commit whose diff is the verbatim rewrite of a SINGLE `.agent/**` state file", naming five files. The rotation touches TWO of them, so a reader who claims that exemption for it is stretching the word "single" — which is exactly what F272's round 30 worker declined to do, flagging the gap instead of quietly invoking the wrong clause.

CHOSEN. THE ROTATION COMMIT TRAVELS UNDER AGENTS.md's DECLARED-OVERSIZE EXCEPTION, not under D1's single-file exemption. That exception permits a diff over 500 lines when the worker declares it in the handback WITH the inseparability reason before review, and when it is the only such commit in its feature. Both conditions held at F272: the worker declared it with the reason above before the reviewer gated it, and the reviewer measured every commit on the branch since the fork point `b18fad57` and found no other authored commit needing it — the two merge commits are merges rather than authored diffs, and the handback commits at 637 and 570 insertions are single-file `.agent/**` rewrites D1 exempts by name. The fit is exact rather than lucky: the exception allows ONE such commit per feature, and the rotation happens ONCE per feature, so a closure can always afford it and can never afford a second.

CONSEQUENCE, AND IT IS WHY THIS IS A DECISION RATHER THAN A DEVIATION. Every closure from here meets this same wall, and without a standing ruling each one re-argues it or quietly claims an exemption that does not fit. The standing answer: declare the rotation commit oversize with the inseparability reason, cite this decision, and spend the feature's single allowance on it. A feature that has already spent that allowance elsewhere must split THAT other commit instead, because the rotation cannot be split at all. REVERSE by deleting this section, at which point the next closure decides for itself; reverse the underlying tension instead by raising D1's cap or by widening its exemption from a single `.agent/**` file to a set of them, either of which is an operator change to AGENTS.md and not a reviewer's to make.
<<<END D18SLICE>>>

<<<BEGIN STATUSPAIR_FROM target=docs/roadmap/STATUS.md>>>
- [~] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion
<<<END STATUSPAIR_FROM>>>

<<<BEGIN STATUSPAIR_TO target=docs/roadmap/STATUS.md>>>
- [x] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion (T001–T003 complete and the `run-loop` half of T004; accepted 2026-09-07 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job abf14422b1badab6 · package remedy-review-20260907-173909-READY_FOR_REVIEW.zip · SHA-256 8bbce2fa27ddd6c68398d381d1367e6e509b49cbacac0a29ff06329d9aebb706 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 7f71b30ac3b2f1fefb2da6063f0453d650d3835a)
<<<END STATUSPAIR_TO>>>

<<<BEGIN READMECOUNTPAIR_FROM target=README.md>>>
74 of 274 registered items accepted.
<<<END READMECOUNTPAIR_FROM>>>

<<<BEGIN READMECOUNTPAIR_TO target=README.md>>>
75 of 274 registered items accepted.
<<<END READMECOUNTPAIR_TO>>>

<<<BEGIN READMETIERPAIR_FROM target=README.md>>>
| 2 | Minimal Self-Build Runtime | 17 | 27 |
<<<END READMETIERPAIR_FROM>>>

<<<BEGIN READMETIERPAIR_TO target=README.md>>>
| 2 | Minimal Self-Build Runtime | 18 | 27 |
<<<END READMETIERPAIR_TO>>>

<<<BEGIN READMECAPPAIR_FROM target=README.md>>>
belong to the follow-up feature the STATUS ledger registers directly after
it).

Accepted in Tier 3 so far:
<<<END READMECAPPAIR_FROM>>>

<<<BEGIN READMECAPPAIR_TO target=README.md>>>
belong to the follow-up feature the STATUS ledger registers directly after
it),
F272 one world completion (the plural run list `Job.run_refs` and the run
re-key onto one `run_dir` keyed by RUN id; the rest of the unified record —
the administrative fields, the Mission extension, `job_id` settled as the one
required key, and the `state` collapse staged as widen, rename and retype with
the rename set found by runtime probe rather than by static classification;
every named consumer moved onto the unified model; and `job run-loop` deleted
together with its advertisements. The classic-to-unified record flip was
measured ATOMIC over the consumer graph — `.id` is the last gap and it sits on
helpers with seven and six call sites — and was split off with the prototype
cluster deletion at the twelve-session soft limit; both belong to the follow-up
feature the STATUS ledger registers directly after it).

Accepted in Tier 3 so far:
<<<END READMECAPPAIR_TO>>>

<<<BEGIN QUEUEPAIR_FROM target=scripts/self_use_queue.json>>>
      "consumed_by": "",
      "provenance": "generated (self-use-generator tier 1, ledger scan, R-0445)"
<<<END QUEUEPAIR_FROM>>>

<<<BEGIN QUEUEPAIR_TO target=scripts/self_use_queue.json>>>
      "consumed_by": "F272",
      "provenance": "generated (self-use-generator tier 1, ledger scan, R-0445)"
<<<END QUEUEPAIR_TO>>>
