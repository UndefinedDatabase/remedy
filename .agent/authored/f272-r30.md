STEP CLOSURE 5/6 — F272 — round 30 — rotate the ledger, build the evidence job and the review zip

Base commit for every reading in this block: `c286fd92`, the round 29 handback commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

CLOSURE ALGORITHM STEPS 1 AND 2 of `docs/roadmap/STATUS_closure_protocol.md`, plus the
LEDGER ROTATION operator amendment amend0905-throughput makes a step of that sequence. This
is the last round before the closure commit itself: after it, the only work left is the
STATUS `[x]` line, the README sync, SU-012's `consumed_by` and the PR.

THE ORDER IS FIXED AND IT MATTERS. The rotation runs AFTER the verdict booking and BEFORE
the STATUS flip, which is what amend0905-throughput requires, and it runs BEFORE the zip so
that the package carries the rotated ledger rather than a 1.2 MB predecessor the next
session would have to re-explain. That is also what F260's closure did at `6cebdce6`. The
evidence job and the zip are then built from a CLEAN tree at the last content commit, and
the handback commit follows them — so the ACCEPTED HEAD this closure records is C4's sha,
not the branch tip.

THE BASE IS THE FORK POINT AND IT IS PROVED BEFORE IT IS USED. `base_commit` is
`b18fad576252f7f2739a5807b6408031da8fcde6`, the first commit `git rev-list --first-parent`
of this branch shares with `main`. It is NOT `git merge-base`, which on this branch answers
`148fbd0b` because `main` has been merged in. The reviewer measured both at `412ce673`: at
the fork point `rev-list --ancestry-path <base>..<head>` and plain `rev-list <base>..<head>`
both answer 213; at the merge-base they answer 184 and 205. That inequality is precisely
what packaged F260's round 22 attempt as BLOCKED_EVIDENCE with 58 unexplained source paths,
and G5 re-proves it at THIS round's head before the producer is called.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r30.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R30
C2   `.agent/live_review.md` — append RECORDR30, the round 29 PASS gate entry
C3   `.agent/prose_slips.md` — append SLIPSR30, one dated line
C4   THE LEDGER ROTATION — `python3 scripts/rotate_live_review.py`, its own commit, whose
     path set is EXACTLY `.agent/live_review.md` and `.agent/live_review_archive.md`
C5   `.agent/handoff.md` rewritten

THE EVIDENCE JOB AND THE ZIP ARE GATES, NOT COMMITS. Neither the evidence directory nor
the package is committed — see constraint 6.

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r30.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    .agent/live_review_archive.md
    .agent/handoff.md

NOTHING under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/` changes this round.
`docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` are named NOWHERE
in this round's diff — all three belong to the closure commit, which is the NEXT round. No
production line moves, so no red-proof is ordered or possible. If a measurement forces a
path outside this list, APPLY IT AND DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice is wrong, apply it as written and declare the
   disagreement; never silently correct it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r30.md`. The BEGIN marker line begins `<<<BEGIN <NAME> ` and
   CARRIES A `target=` ATTRIBUTE AFTER THE NAME; the END marker line is exactly
   `<<<END <NAME>>>`. Match the BEGIN by that PREFIX, not by an exact-line equality —
   round 29's worker correctly declared that earlier blocks described these markers as if
   BEGIN carried no attribute, and this constraint is the corrected wording. A slice is read
   exclusive of both marker lines and INCLUSIVE of the newline ending its last content line.
   This round carries no FROM/TO pair. Never retype a slice.
3. C0a and C0b are `shutil.copyfile` of `.remedy-wt/f272-r30-block.md`.
4. BOTH PROSE APPENDS ARE `post == pre + b"\n" + slice`. Each target ends in EXACTLY ONE
   newline at the base, measured per file: three consecutive newlines at `c286fd92` occur 0
   times in `.agent/live_review.md` and 1 time in `.agent/prose_slips.md` (offset 39213,
   pre-existing). Neither is load-bearing and neither is repaired.
5. C4 IS THE SCRIPT'S OWN OUTPUT AND IS NEVER HAND-EDITED. Run
   `python3 scripts/rotate_live_review.py` with no arguments and commit exactly what it
   writes. Do not reformat either file, do not move a record by hand, and do not repair the
   pre-existing double blank line in `.agent/prose_slips.md`. The script verifies every
   moved record by sha256 before and after and refuses on any mismatch; if it refuses, STOP
   and hand back with its output.
6. THE EVIDENCE DIRECTORY AND THE PACKAGE ARE NEVER COMMITTED. Put the evidence directory in
   a FRESH directory under the gitignored `.remedy-wt/`. A pre-committed evidence dir puts
   evidence files into the reviewed range and the package builds BLOCKED_EVIDENCE — the F147
   attempt-2 lesson. The zip lands in the repo root, which `.gitignore` already matches, so
   it never dirties the tree; confirm that rather than assume it.
7. A FAILING ZIP BUILD IS A CLOSURE BLOCKER, NOT SOMETHING TO WORK AROUND. Record the raw
   error and the full `validation_errors` list, commit the handback saying so, and stop; the
   reviewer decides. NEVER change the base, an evidence field or any source file to make the
   package go READY.
8. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. No `- R-XXXX` line, no `Done:`
   paragraph, no `Landed:` line. `R-0829` is the next free id and must still be free at the
   end. The open set must read the SAME before and after the rotation.
9. NO WORKTREE IS CREATED OR REMOVED. `git worktree list` is 14 entries at the base — the
   primary plus thirteen `remedy/job-*`, the newest being `remedy/job-020c1ef366af4f07`
   from round 28's product run — and must still be 14 at the end.
10. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before C5, and report
    all three readings.
11. Commit subjects are `f272: <what>` and carry no leading-slash token, no absolute path and
    no secret-like string: the evidence metadata scanner rejects such subjects and would
    block this very closure.

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, NO PIPE between the command and
the echo. Report ONE LINE PER GATE with the transcripts below it. Every gate runs at or
before C4, so the handback can quote all of them.

G1 TRANSPORT. One digest comparison: `.remedy-wt/f272-r30-block.md` as delivered against the
   committed `.agent/authored/f272-r30.md` and the committed `.agent/last_block.md`. Report
   sha256, byte length and line count for each of the three.

G2 THE FINDING RECORD, over the single append at C2, against its own pre-image.
   (a) BYTE: pre_len, pre_sha256, post_len, post_sha256, the terminal twelve bytes and
       trailing-newline run of each, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and
       `POST_EQUALS_PRE_NL_SLICE`. At `c286fd92` the pre-image is 1238279 bytes, 2145 lines,
       sha256 beginning `3b6622ba52c6b814`.
   (b) STRUCTURAL: strip the single terminal newline, split on blank lines, compare the LAST
       N units against the slice's paragraphs IN ORDER, where N is COUNTED BY YOUR SCRIPT
       from the slice. Report N, units before, units after and `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST paragraph the append adds, in memory only, never on
       disk: flip one byte, require BOTH readers to reject it, then re-read the file and
       confirm it is byte-identical to the real post-image.
   (d) COUNTS: `^- R-\d{4}` distinct 312 -> 312, `^Done: R-\d{4}` distinct 252 -> 252, open
       set BY DISTINCT ID 60 -> 60, `^Gate:` 52 -> 53, `^Gate: F272 R29 ` 0 -> 1,
       `^- R-0829 ` 0 -> 0.

G3 THE TWO PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R30; report its bytes, its
   line count against the AGENTS.md cap of 50, and that `## Goal` and `## Next Steps` are
   both present. `.agent/prose_slips.md` gets the byte append check only — pre_len 153118 and
   pre_lines 569 at `c286fd92`, and `POST_EQUALS_PRE_NL_SLICE` for SLIPSR30.

G4 THE ROTATION at C4. Report the script's FULL stdout and its real exit code. Then, measured
   yourself and not read from that stdout:
   (a) `.agent/live_review.md` byte length before and after, and
       `.agent/live_review_archive.md` byte length before and after. The reviewer's
       `--dry-run` AT THE BASE COMMIT `c286fd92` reported 1238279 -> 483477 for the ledger,
       1780229 -> 2535031 for the archive, and 23 gate records plus 250 finding pairs moved.
       THOSE FIGURES CANNOT BE YOUR TARGET AND MUST NOT BE TREATED AS ONE: that dry run was
       taken BEFORE this round's own C2 appended a record, so your pre-image is larger by
       exactly RECORDR30's length plus one newline, and the moved-record counts may differ
       too. REPORT WHAT YOU MEASURE, and report the pre-image delta against 1238279 so the
       difference is visible rather than silent.
   (b) THE ARCHIVE IS APPEND-ONLY: the pre-rotation archive is a byte-exact PREFIX of the
       post-rotation archive. Report the boolean.
   (c) THE OPEN SET IS UNCHANGED, BY BOTH FORMULAS, and report both with their arithmetic:
       BY DISTINCT ID — distinct `^- R-\d{4} ` minus distinct `^Done: R-\d{4} ` — which is
       60 before and must be 60 after; and BY THE SCRIPT'S OWN LINE FORMULA, registration
       lines minus `Done:` lines, which is 58 before and must be 58 after. The two differ
       because R-0721 and R-0725 each carry a two-paragraph resolution, so there are 254
       `Done:` LINES against 252 distinct ids; both readings are correct for what they
       measure and the closure reports the DISTINCT-ID one.
   (d) `^Gate: F272 R` count in the ledger before and after. F272 is still `[~]`, so NONE of
       its own gate records may move; report the count and confirm it is unchanged.
   (e) The commit's path set is EXACTLY `.agent/live_review.md` and
       `.agent/live_review_archive.md`.

G5 THE EVIDENCE JOB — closure algorithm step 1.
   FIRST, THE BASE PROOF, before the producer is called: with base
   `b18fad576252f7f2739a5807b6408031da8fcde6` and head the full sha of C4, report the count
   of `git rev-list --ancestry-path <base>..<head>`, the count of
   `git rev-list <base>..<head>`, and the boolean THE TWO ARE EQUAL; also that the base is an
   ancestor of `main`. IF THE COUNTS DIFFER, STOP — that inequality is the defect that
   blocked F260's round 22. Then `git status --porcelain` EMPTY. Then call, in Python,
   `packages.orchestration.job_evidence.create_manual_completion_bundle` with:
       evidence_dir       a FRESH directory under the gitignored `.remedy-wt/`
       repo_root          the primary checkout
       base_commit        b18fad576252f7f2739a5807b6408031da8fcde6 — the full
                          40-character fork point, NEVER abbreviated
       head_commit        the full sha of C4, measured
       job_id             16 lowercase hex characters from `secrets.token_hex(8)`
       job_title          F272 one world completion closure evidence
       step_range         T001-T004
       prior_job_ids      the empty list
       review_feature_id  f272
       timestamp / generated_at   ISO-8601 UTC
       verification_runs  ONE run, built from a REAL run of
         `python3 -m pytest tests/docs/ -q` at C4, with these fields and no others:
         `run_id` matching `vr-` followed by four or more digits; `command` the exact command
         string; `exit_code`; `passed`; `failed`; `skipped`; `deselected`; `selected` EQUAL to
         passed+failed+skipped; `node_ids` from a real `--collect-only` of the SAME selection,
         whose length must EQUAL `selected` — the reviewer measured 303 collected against 303
         passed at `c286fd92`, so those two agree today; `test_files` the actual FILE paths,
         SORTED, never a directory; `stdout_summary` the run's own stdout under 4000
         characters; `output_hash` the sha256 hex of EXACTLY that `stdout_summary` string;
         `head_sha`; `duration_seconds`.
   BEFORE calling the producer, pre-scan every node id and every test_file with
   `packages.orchestration.build_review_manifest._unsafe_text` and report that it flags NONE
   of them; an absolute path or a secret-like token in a node id is what packaged F080's
   round 4 attempt as BLOCKED_EVIDENCE. Do NOT record a full-suite node-id list anywhere.
   Report the returned summary dict in full, the job id, and the verdict it names.

G6 THE REVIEW ZIP — closure algorithm step 2, MANDATORY and never skipped. `git status
   --porcelain` EMPTY first, branch pushed. Then
       bash scripts/make_review_zip.sh --evidence-dir <the directory from G5>
   Report: the FULL stdout; the package FILENAME; its SHA-256 as the script printed it AND as
   you recompute it from the file on disk; the package's ABSOLUTE directory; `PACKAGE_STATUS`;
   and the manifest's `committed_review_subject` base and head, which must span
   `b18fad576252f7f2739a5807b6408031da8fcde6`..C4. If `PACKAGE_STATUS` is not
   READY_FOR_REVIEW, report `validation_errors` VERBATIM and in full, then stop per
   constraint 7.

G7 THE PRECONDITIONS, run SERIALLY in the primary checkout at C4:
       python3 -B -m pytest tests/docs/ -q -p no:randomly
       python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
   The reviewer measured 303 and 42. Then, in Python,
   `packages.orchestration.integrity_gate.run_integrity_checks()` — report `.passed` and
   `.fail_count`, which are ATTRIBUTES and not dict keys. The reviewer measured passed True
   and fail_count 0 at `c286fd92`, AND measured that its `high_blockers_open` check reports
   "no open blocker/high findings" while five High findings are in fact open; report that
   check's own message verbatim, because the closure states it rather than leaning on it.

G8 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the real output
   each time, and EMPTY immediately before the evidence job and again before the zip. `git
   ls-files .remedy-wt` empty. `git worktree list` 14 entries, unchanged. Every commit
   single-parent. Per-commit insertions from `git diff --numstat <parent> <commit>` for C0a
   through C4 — C5 excluded, because a commit cannot count its own insertions while it is
   being written — each against the DECISION F104 D1 cap of 500. C4 is expected to be far
   over that cap and is EXEMPT BY NAME, being the verbatim rewrite of `.agent/**` state
   files produced by a script; report its number and say which exemption you are claiming.
   Report the push result and that NO pull request was created. The three `.agent/STOP`
   readings.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely. It is the durable carrier for the closure round, so
it MUST record, in a section a later reader can find BY NAME, each of these:

    EVIDENCE JOB ID
    PACKAGE FILENAME
    PACKAGE SHA-256
    PACKAGE ABSOLUTE DIRECTORY   (or the literal NOT ARCHIVED if left where built)
    ACCEPTED HEAD                (the full sha of C4, and the head the manifest recorded)
    PACKAGE_STATUS
    OPEN FINDINGS BY DISTINCT ID, with its arithmetic

The next round authors the STATUS line from those values, so a missing one costs a round.
Beyond that: `SESSION 12 of feature F272 · round 30 · rounds so far 30`; the range; a
per-commit changed-files table whose `+/-` cells come from `git diff --numstat` and are
compared cell for cell against G8's figures; the item-status table for C0a through C5; one
line per gate with its real reading; every deviation and assumption; one sentence of context
self-assessment. It has no length cap.

<<<BEGIN PLANF272R30 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 29 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004's remainder and T005 are F274's, split off in round 26 by DECISION
F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Session 12 reached the soft
limit of 12 sessions, so the remaining work is the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md` and no further building.

## Current Step

Round 30: rotate the ledger, then build the evidence job and a FRESH review zip from a clean
tree at the last content commit. The rotation runs after the verdict booking and before the
STATUS flip, as amend0905-throughput requires, and before the zip so the package carries the
rotated ledger. `base_commit` is the FORK POINT `b18fad57`, proved equal-count before use.

## Next Steps

1. THE CLOSURE COMMIT, and it is the last one on this branch: the STATUS `[x]` line, the
   README capability sync and SU-012's `consumed_by` set to `F272`, all in ONE commit, from
   the values this round's handback records. Then the pull request.
2. The PR is NOT merged this session. It merges at the next feature's start via the Open PR
   Gate, which is the operator's manual-review window.
3. F274 owns the atomic record flip and the cluster deletion. None of that work starts here.

## Risks

- Five open High findings — R-0803, R-0804, R-0806, R-0807 and R-0827. The close is
  PASS_WITH_RISKS and names every one with its owner; DECISION F272 D17 rules why.
- `remedy integrity check` PASSES while its `high_blockers_open` check reports "no open
  blocker/high findings" and five are open. That is the already-open R-0648, and the closure
  states it rather than leaning on it.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops and hands
  back rather than adjusting a field to make the package go READY.
<<<END PLANF272R30>>>

<<<BEGIN RECORDR30 target=.agent/live_review.md mode=append>>>
Gate: F272 R29 — the F272 round 29 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `c286fd92`. THIS IS THE ROUND THAT REGISTERED WHAT THE SELF-USE RUN FOUND AND RULED CLOSURE PRECONDITION 1. Range `f321fefc`..`c286fd92`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with `git diff --name-only` naming exactly the seven declared paths and nothing under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/`. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r29-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r29.md` and `.agent/last_block.md` are all 31158 bytes at 259 lines and all hash to `96cac5e8428eda1c76f4230aa1171ab1f997c7ed5c5786febc69114524642a89`; per §3 item 37 that chain covers those artefacts and is not a claim about the bytes emitted into a prompt. G2 THE FINDINGS APPEND at C2: 1225920 to 1233736 bytes, pre-image a byte-exact prefix, `POST_EQUALS_PRE_NL_SLICE` true, structural N counted from the slice as 3 with units 734 to 737 and everything before unchanged; the reviewer confirms the FIRST appended paragraph is R-0826's and that a byte flipped inside IT — not inside the last — is rejected by BOTH readers, which is the §3 item 36 shape and the reason the control sits where it does. Registrations 309 to 312, resolutions BY DISTINCT ID 252 unchanged, open set 57 to 60, `^Done: ` LINES 254 to 254 so not one resolution line was added, and `^- R-0826 `, `^- R-0827 `, `^- R-0828 ` each 0 to 1 with `^- R-0829 ` still 0. G3 THE GATE ENTRY at C3 was proved against C2's POST-IMAGE and not against the base, which is the arithmetic this round could most easily have got wrong: the reviewer independently confirms the C3 pre-image is byte-equal to the C2 post-image and is NOT the base image, 1233736 to 1238279 bytes with the prefix and ordered-equality both true, `^Gate: ` 51 to 52, `^Gate: F272 R28 ` 0 to 1, the three registrations unchanged at one apiece, and the open set 60 on both sides. G4 THE DECISION RECORD: 865296 to 869442 bytes, prefix and ordered equality true, `^## DECISION F272 D` 1 to 2, and `## DECISION F272 D17` heads exactly one section. G5 THE PROSE FILES: the plan is 1934 bytes at 38 lines against the cap of 50 and byte-equal to its slice. G6 THE CANARY is exit 0 at 42 passed. G7 THE TREE: porcelain empty at every boundary, `git ls-files .remedy-wt` empty, worktrees 14 and unchanged, per-commit insertions 259, 172, 15, 6, 2, 14 and 2 for C0a through C5, every one far under the DECISION F104 D1 cap of 500. THE THREE FINDINGS THIS ROUND REGISTERED ARE THE POINT OF IT, and each was searched for BY DEFECT before it was minted, per §3 item 30: R-0826 Medium, that the self-use track's own defect reporter reads only `error` fields and so answered the empty tuple for a run that exhausted its budget and published no manifest; R-0827 High, that `pingpong_provider` stamps `mode="ollama-legacy"` while `run_manifest.VALID_CALL_MODES` holds only five other values, so no run manifest can be published for the provider this repository's own role config returns; and R-0828 Medium, that a budget-stopped job is left recorded as `RUNNING` with a blank `finished_at` although `RunState.STOPPED` exists and `job_evidence` treats only completed and stopped as terminal. A FOURTH OBSERVATION WAS DELIBERATELY GIVEN NO ID: six real provider calls measured zero tokens, which is the defect R-0807 and R-0753 already hold, so the corroboration was recorded against those two ids instead of minting a duplicate. THE WORKER'S FOUR DECLARATIONS ARE ALL ACCEPTED AND TWO DESERVE NAMING. It declared that constraint 2's description of the BEGIN marker omits the `target=` attribute the real markers carry, so a literal matcher would find none — the reviewer's error, corrected in the next block's own constraint 2 and recorded as a dated prose-slip line. And it declared, unprompted, that its G1 re-reading re-ran a `shutil.copyfile` and was therefore a probe with a persistence side effect, reporting that the bytes were identical and the tree clean immediately after; declaring that rather than letting it pass silently is the standard this workflow is trying to hold.
<<<END RECORDR30>>>

<<<BEGIN SLIPSR30 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 29 — the block's constraint 2 said each authored slice lies between `<<<BEGIN NAME>>>` and `<<<END NAME>>>`, and every real BEGIN line carries a `target=` attribute after the name, so a worker matching that description literally would find zero markers; the END description was correct. Rounds 26, 27 and 28 carried the same wrong wording and no worker raised it, which is what makes it worth a line: a delimiter description is the one part of a block that is read by a machine the worker writes, so it is stated as the PREFIX or the pattern actually matched, never as an idealised whole line. Corrected in round 30's constraint 2.
<<<END SLIPSR30>>>
