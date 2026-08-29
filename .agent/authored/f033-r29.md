# STEP 29 — F033 Hunk-level diff approval (SESSION 7, round 29; THE CLOSURE COMMIT AND THE PULL REQUEST)

Goal: book the round 28 PASS, then close the feature — the STATUS `[x]` line and
the README capability sync in ONE commit, which is the LAST commit on this
branch, followed by the pull request. That PR is NOT merged in this session: it
merges at the next feature's start via the Open PR Gate, and the gap is the
operator's manual-review window.

## Bundle — the list that is executed

1. C0a: save this block verbatim to `.agent/authored/f033-r29.md`.
2. C0b: mirror the same bytes into `.agent/last_block.md`.
3. C1: rewrite `.agent/plan.md` from slice PLAN29.
4. C2: append slice RECORD29 to `.agent/live_review.md` — books the round 28
   PASS. It registers and resolves nothing.
5. C3: THE CLOSURE COMMIT. Apply pairs PAIR-STATUS, PAIR-COUNT and PAIR-TIER,
   and rewrite `.agent/handoff.md` as the handback, ALL IN ONE COMMIT. This is
   the last commit on the branch (Rule A4).
6. Then create the pull request. That is not a commit.

## Change set — exactly these paths, nothing else

    .agent/authored/f033-r29.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    docs/roadmap/STATUS.md
    README.md
    .agent/handoff.md

## What the reviewer measured before writing this block, and where

Every reading below was taken by the reviewer at `35481fc5`, this round's base.

- THE PACKAGE EXISTS AT THE PATH THE HANDBACK NAMES, and the reviewer opened it
  rather than trusting the report.
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260829-154912-READY_FOR_REVIEW.zip`
  is 20486078 bytes at sha256
  `3b646ca5a18f10ae21f3218a753be00970762ba0fe4513ef53a3f60a9f711ccc`, which is
  the digest the round-28 handback states. Its `.review_zip_manifest.json` reads
  `package_status` `READY_FOR_REVIEW`, `ready_gate_matrix.ok` true with an EMPTY
  `blocking_reasons`, `packaging_warnings` empty, `external_paths_detected`
  empty, `source_root_containment` PASS, `git_status_snapshot` OK,
  `packaged_evidence_job_id` `f033-closure`, and a
  `committed_review_subject` of base `bd8d952942d8ec1d243d787ccfe16e0ad04360d2`,
  head `8738c5f1643b2bd667bc796257a4ddc502f36191`, `base_is_ancestor` true over
  237 commits. All EIGHT gate documents are present with verdicts.
- THE ACCEPTED HEAD IS `8738c5f1643b2bd667bc796257a4ddc502f36191`, which is C3
  of round 28 — the last CONTENT commit, the head the zip actually covers. It is
  NOT this round's head, and the STATUS line says so deliberately: the segment
  names the reviewed head the verdict and the package cover.
- `integrity check` PASSES, re-run by the reviewer through
  `python3 -m apps.cli.grouped integrity check --json` at REAL exit 0:
  `passed` true, `fail_count` 0 over 5 checks, and `high_blockers_open` reads
  "no open blocker/high findings", which is closure precondition 3.
- THE THREE ANCHORS ARE UNIQUE, and the second one is a WHOLE LINE rather than
  the sentence the test regex matches. `- [~] F033 — Hunk-level diff approval`
  occurs exactly once in `docs/roadmap/STATUS.md`; the README line
  `62 of 257 registered items accepted. Next: F033 (Hunk-level diff approval).`
  and the row `| 5 | Operator Cockpit | 10 | 31 |` each occur exactly once in
  `README.md`.
- THAT README LINE ALSO NAMES F033 AS THE NEXT FEATURE, and this closure is what
  falsifies it. The reviewer's first draft of PAIR-COUNT spanned only the
  sentence `tests/docs` pins and would have left "Next: F033" standing beside an
  accepted F033 — the same shape as R-0747 through R-0750, caught before
  emission by the pair's own containment measurement rather than after landing.
  DECISION F033 D6 in RECORD29 rules what replaces it and why. No test pins the
  `Next:` text: `git grep -n -F "Next: F"` over `tests`, `docs`, `scripts`,
  `packages` and `apps` returns NOTHING, and the only pin on that line is the
  regex `^(\d+) of (\d+) registered items accepted\.`, which PAIRCOUNT-TO still
  satisfies because the sentence stays at the line's start.
- THE TWO README NUMBERS ARE DERIVED THE WAY THE TESTS DERIVE THEM, not guessed.
  `^- \[x\] F\d{3} — ` matches 62 lines in STATUS.md now, so the prose count
  goes to 63. Resolving every accepted id through its feature file's tier prefix
  gives Tier 5 exactly 10 now, and `docs/roadmap/features/T5_F033.md` puts F033
  in Tier 5, so that row's Done cell goes to 11. Both pins are in
  `tests/docs/test_docs_consistency.py` and both are ledger-count changes, so
  they land in the SAME commit as the STATUS edit — the docs-round rule and the
  R-0154 pin say the same thing from two directions.
- THE STATUS GRAMMAR IS COPIED FROM THE LIVING PRECEDENT, the accepted F037,
  F256 and F257 lines. Note the EN DASH in `T001–T003`: those lines use `–`,
  not a hyphen, and PAIR-STATUS carries the same byte.
- THE SELF-USE QUEUE IS EXHAUSTED — one item, zero pending — so no
  `consumed_by` edit is owed and `scripts/self_use_queue.json` is NOT touched.
  The closure records `self-use NONE (queue exhausted)`.
- THIS ROUND'S OWN VERDICT WILL HAVE NO GATE ENTRY ON DISK, by construction:
  docs/agents/planner_reviewer_prompt.md §4 item 13 rules that the last round of
  a branch cannot record a gate on itself. That absence is the branch
  TERMINATOR, not a missing gate. RECORD29 books round 28 and stops.

## Slice PLAN29 — the FULL new bytes of `.agent/plan.md`

The slice is every byte BETWEEN the two marker lines, exclusive. The markers are
not part of any file.

<<<BEGIN PLAN29
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 7, closing the feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001, T002 and T003 | done | rounds 1-24 |
| the operator guide and its index rows | done | round 26 |
| the integration gate | done | round 27, PASS WITH RISKS |
| the Built State, evidence job and review zip | done | round 28 |
| the STATUS line, the README sync and the PR | done | this round |
| R-0745 and R-0750, carried as documented risks | open | see Risks |

## Next Steps
1. This round books the round 28 PASS, flips the STATUS line to `[x]` with the
   README capability sync in the SAME commit, and opens the pull request.
2. THE PR IS NOT MERGED IN THIS SESSION. It merges at the next feature's start
   through the Open PR Gate, which is the operator's manual-review window; the
   operator may also merge it by hand at any time.
3. The next session starts a NEW feature: read `.agent/STOP` first, then run the
   Open PR Gate, which will find this PR and merge it before any new branch.
4. Nothing further is owed on this branch. Its last round has no on-disk gate
   entry by construction, and that absence is the terminator rather than a
   missing review.

## Risks
- R-0745 (Low) and R-0750 (Medium) stay OPEN at closure, which is why the STATUS
  line reads PASS_WITH_RISKS. Neither is reachable from this feature's
  Acceptance: the first hardens an import guard over the write door, the second
  is a reviewer's gate wording that ordered a full run log where the canonical
  integration-gate procedure asks for a tail.
<<<END PLAN29

## Slice RECORD29 — appended to `.agent/live_review.md`

Two paragraphs, blank-line separated: the LAST gate entry this branch receives,
and the DECISION that entry refers to. Neither begins with `- R-`, so no id
moves this round.

<<<BEGIN RECORD29
Gate: F033 R28 — THE CLOSURE PREPARATION. THE ROUND PASSED. Every gate was re-executed by the reviewer at `35481fc5`. TRANSPORT: the reviewer's own pre-emission original, `.agent/authored/f033-r28.md` and `.agent/last_block.md` are all 25853 bytes at sha256 `49ac004e…17f275` and BYTE-EQUAL. THE PLAN is byte-EQUAL to PLAN28 at 2197 bytes over 42 lines. THE RECORD APPEND at `24ea131f` reconstructs 1625403 plus one newline plus 8596 to 1634000, base a byte PREFIX, slice an exact SUFFIX, N COUNTED at 3, the last three units equal to the slice's paragraphs IN ORDER, and a negative control at byte 1628405 — the reviewer's own offset, inside the FIRST appended paragraph — REJECTED by both readers, which accepted the unflipped bytes. THE LEDGER: registered 310 distinct going to 311 with the ADDED id exactly `R-0750`; `Done:` 55 lines over 53 distinct UNMOVED; `Landed:` 22 UNMOVED; `^Gate: F033 R27 — ` 0 before and exactly 1 after; `^R-0736 EXTENSION — ` exactly 1 with `^- R-0736 — ` still exactly 1, so the extension spent no id; and the open set 257 to 258. THE BUILT STATE satisfies ORDERED EQUALITY: `docs/roadmap/features/T5_F033.md` goes 6358 to 9936 bytes, the pre-commit blob is a byte PREFIX, the slice an exact SUFFIX, the reconstruction exact, and the 54 lines C3's diff ADDS are exactly one blank separator followed by the slice's 53 lines IN ORDER with ZERO deleted lines. `python3 -m pytest tests/docs/ -q` is a REAL exit 0 at 295 passed, equal to the figure this branch measured at round 26. THE INTEGRITY CHECK was re-run by the reviewer through `python3 -m apps.cli.grouped integrity check --json` at REAL exit 0: `passed` true, `fail_count` 0 over 5 checks, `high_blockers_open` reading "no open blocker/high findings". THE PACKAGE WAS OPENED, NOT TAKEN ON REPORT: the archived zip is 20486078 bytes at the sha256 the handback states, its `.review_zip_manifest.json` reads `package_status` READY_FOR_REVIEW with `ready_gate_matrix.ok` true and EMPTY `blocking_reasons`, no packaging warnings, no external paths, containment PASS, evidence job `f033-closure`, and a `committed_review_subject` whose head is `8738c5f1` — C3 of that round, the last CONTENT commit — over base `bd8d9529` with `base_is_ancestor` true across 237 commits. All eight gate documents are present. THE STRUCTURE: six single-parent commits over `f13134fe`..`35481fc5` of 302, 231, 22, 6, 54 and 336 insertions, every one under 500 — which is the number R-0750 exists about, and this round has no evidence log to commit and therefore no exception to declare; `git status --porcelain` EMPTY; zero untracked paths; and the path set to C3 EQUALS the declared change set minus `.agent/handoff.md` in BOTH directions. THE BUNDLE WAS SIX COMMITS RATHER THAN SEVEN and the block anticipated it: C4 produced nothing committable, because the evidence directory is gitignored by design and the package is written outside the repository, and the worker declared that rather than manufacturing a commit. THE WORKER'S BEST DEVIATION IS ITS THIRD: it observed that of the two readers G3 orders, a BASE-PREFIX reader is structurally incapable of rejecting a flip that lies beyond the base blob's last byte, and reported that reader's unmoved result rather than hiding it. The reviewer's own reading (a) — reconstructing base plus separator plus slice and comparing the whole to the committed file — DOES reject the flip, so the two-reader obligation is met in substance; but the worker was right that a prefix check alone cannot be the second reader, and a later block ordering this gate should say which reading it means.

DECISION F033 D6 — THE README'S `Next:` FIELD NAMES THE LEDGER INSTEAD OF A FEATURE ID. Raised by the reviewer while writing the closure block, under docs/agents/planner_reviewer_prompt.md §4 item 7, because a silent re-plan is forbidden and this changes a field every closure has maintained by hand. CONTEXT, measured at `35481fc5`: `README.md` carries the single line `62 of 257 registered items accepted. Next: F033 (Hunk-level diff approval).`, and this closure accepts F033, so the second sentence becomes false in the same commit that makes the first one true. `tests/docs/test_docs_consistency.py` pins only the first sentence, through the regex `^(\d+) of (\d+) registered items accepted\.`; `git grep -n -F "Next: F"` over `tests`, `docs`, `scripts`, `packages` and `apps` returns nothing, so the `Next:` half is maintained by hand and guarded by no test at all. CHOSEN: the sentence becomes `Next: the first unchecked item in docs/roadmap/STATUS.md.` — it names the RULE that selects the next feature rather than the instance the rule currently returns, so it is true by construction at every commit and cannot go stale. ALTERNATIVES CONSIDERED: (a) name the next id, which STATUS order gives as F040, "Completion/return digest" — rejected because Rule A5 selects the next feature at the NEXT session's claim and "proposes, never starts", so a forecast written here is a claim this session has no authority to make and would be stale the moment the operator claims differently; (b) delete the sentence — rejected because a reader arriving at the README's Status section is asking exactly this question and deserves the pointer, and an empty field invites the next closure to reinvent the hand-maintained form. WHY IT IS RECORDED AS A DECISION rather than done quietly: it retires a convention every prior closure followed, and the operator's veto is any later relay. HOW TO REVERSE: restore the hand-maintained form by writing `Next: F<id> (<name>).` in that line and updating it at each closure, which is what `bd8d9529` and every closure before it did. THIS IS THE SAME DEFECT CLASS AS R-0747 THROUGH R-0750, arriving one last time at the closure itself: a sentence true when written, falsified by a later round that completed the thing it named. The difference is that this one was caught BEFORE emission, by the pair's own containment measurement rather than by a reader a round later, and the fix is structural rather than another instance repair.
<<<END RECORD29

## Pair PAIR-STATUS — `docs/roadmap/STATUS.md`

Containment test run by the reviewer at `35481fc5`: `TO contains FROM: false`.
It is therefore a REWRITE, and the gate is PAIRSTATUS-FROM 0x and PAIRSTATUS-TO
exactly 1x after the commit. The FROM occurs exactly once at this base. Touch no
other line of that file.

<<<BEGIN PAIRSTATUS-FROM
- [~] F033 — Hunk-level diff approval
<<<END PAIRSTATUS-FROM

<<<BEGIN PAIRSTATUS-TO
- [x] F033 — Hunk-level diff approval (T001–T003 complete; accepted 2026-08-29 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f033-closure · package remedy-review-20260829-154912-READY_FOR_REVIEW.zip · SHA-256 3b646ca5a18f10ae21f3218a753be00970762ba0fe4513ef53a3f60a9f711ccc · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 8738c5f1643b2bd667bc796257a4ddc502f36191)
<<<END PAIRSTATUS-TO

## Pair PAIR-COUNT — the accepted-count line of `README.md`

Containment test run by the reviewer at `35481fc5`: `TO contains FROM: false`.
A REWRITE; the gate is PAIRCOUNT-FROM 0x and PAIRCOUNT-TO exactly 1x after the
commit. The FROM occurs exactly once at this base.

<<<BEGIN PAIRCOUNT-FROM
62 of 257 registered items accepted. Next: F033 (Hunk-level diff approval).
<<<END PAIRCOUNT-FROM

<<<BEGIN PAIRCOUNT-TO
63 of 257 registered items accepted. Next: the first unchecked item in docs/roadmap/STATUS.md.
<<<END PAIRCOUNT-TO

## Pair PAIR-TIER — the Tier 5 row of the README status table

Containment test run by the reviewer at `35481fc5`: `TO contains FROM: false`.
A REWRITE; the gate is PAIRTIER-FROM 0x and PAIRTIER-TO exactly 1x after the
commit. The FROM occurs exactly once at this base. Change no other row: the
other seventeen rows are already equal to what the ledger derives for them.

<<<BEGIN PAIRTIER-FROM
| 5 | Operator Cockpit | 10 | 31 |
<<<END PAIRTIER-FROM

<<<BEGIN PAIRTIER-TO
| 5 | Operator Cockpit | 11 | 31 |
<<<END PAIRTIER-TO

## Constraints

1. Apply every slice and every pair BYTE FOR BYTE. If one looks wrong, apply it
   as written and declare the problem; never silently repair it. PAIRSTATUS-TO
   contains an EN DASH in `T001–T003` and MIDDLE DOTS between its segments,
   matching the accepted F037, F256 and F257 lines; do not substitute ASCII.
2. PLAN29 is a FULL REWRITE. RECORD29 is an APPEND. Measured by the reviewer at
   `35481fc5`, `.agent/live_review.md` is 1634000 bytes and ends with a newline,
   so the append is one blank-line separator then the slice. RE-MEASURE it
   yourself at the commit you append at.
3. Do NOT delete or edit any landed `Landed:`, `Done:` or `Gate:` text.
4. C3 IS THE LAST COMMIT ON THIS BRANCH — Rule A4. Its path set is EXACTLY
   `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`. The STATUS
   edit and the README sync land TOGETHER: the R-0154 pin is that README and
   STATUS may never disagree in any committed state, and the two README numbers
   are ledger counts whose test pins must move in the same commit as the ledger.
5. Do NOT touch `scripts/self_use_queue.json`. Its queue is exhausted, so no
   `consumed_by` edit is owed and an edit would be a false record.
6. Do NOT rebuild the review zip, re-run the evidence job, or edit any manifest.
   Round 28 built the package from a clean tree at the accepted head and this
   round consumes those values verbatim.
7. Touch no path outside the change set. This round changes NO file under
   `packages/`, `apps/`, `tests/`, `docs/guides/` or `docs/roadmap/features/`.
8. AFTER C3, create the pull request with `gh pr create`, base `main`, head
   `feature/f033-hunk-approval-v2`, NOT a draft. DO NOT MERGE IT and do not
   merge anything else. Never force-push. The description carries what changed
   and why, the key decisions, how to review, the changed-files summary, the
   latest verdict, the open-findings count and the runtime actuals — and it
   states plainly that R-0745 and R-0750 are open and carried as documented
   risks. Its subject and body contain no leading-slash token, no absolute path
   outside the two the STATUS line already carries, and no secret-like string.
9. The `remedy` console script is denied in this sandbox; use
   `python3 -m apps.cli.grouped ...` and say so.
10. The sandbox denies `VAR=x cmd`, `env`, `export`, `cp`, `$(...)` inside a
    compound, process substitution, a heredoc nested in `bash -c`, and a shell
    line containing a brace with a quote inside it. Write scripts under
    `.remedy-wt/` and run them as `python3 -B <path>`. REAL exit codes come from
    `subprocess.run(...).returncode`, never from a pipe.
11. Re-read `.agent/STOP` before starting. If it exists, stop and hand off.
12. G1 through G7 run at C3. G8 runs after the pull request exists. Remove any
    scratch you wrote under `.remedy-wt/` BY EXACT PATH, never by glob.

## Done when — G1 through G8

G1 TRANSPORT. Report `sha256` and byte length of the committed
`.agent/authored/f033-r29.md`, and the same two readings for
`.agent/last_block.md`. One digest comparison.

G2 THE PLAN. `.agent/plan.md` byte-EQUAL to PLAN29, under 50 lines, holding
`## Goal` and the substring `Steps`. Report the byte length and the line count.

G3 THE RECORD APPEND, at C2. Reconstruct the MEASURED base plus one newline plus
the byte length of RECORD29 to the committed size. Prove the pre-commit blob a
byte PREFIX and the slice an exact SUFFIX. COUNT N in the script. Compare the
file's LAST N blank-line units against the slice's paragraphs IN ORDER. Flip one
byte inside the FIRST appended paragraph, report the offset, and show that BOTH
of these reject it while accepting the unflipped bytes: reading (a) is the WHOLE
reconstruction — base plus separator plus slice compared to the committed file,
not a prefix test, which the round-28 handback correctly observed cannot see a
flip past the base's last byte — and reading (b) is the paragraph comparison.

G4 THE LEDGER, at `35481fc5` and at C2: `^- R-\d+ — ` 311 distinct UNMOVED;
`^Done: R-\d+ — ` 55 lines over 53 distinct UNMOVED; `^Landed: ` 22 UNMOVED;
`^Gate: F033 R28 — ` 0 before and exactly 1 after; and the open set 258 UNMOVED.
This round registers and resolves nothing. Report also that distinct
`^DECISION F033 D\d+ — ` ids go 5 to 6 with the ADDED one exactly `D6`.

G5 THE CLOSURE COMMIT, at C3. In `docs/roadmap/STATUS.md`, PAIRSTATUS-FROM
occurs 0 times and PAIRSTATUS-TO exactly 1 time. In `README.md`, PAIRCOUNT-FROM
and PAIRTIER-FROM each occur 0 times and PAIRCOUNT-TO and PAIRTIER-TO each
exactly 1 time. Report all six counts. Then report `git diff --name-only` for C3
alone: it must be EXACTLY `docs/roadmap/STATUS.md`, `README.md` and
`.agent/handoff.md`, in both directions. Confirm C3 is the branch tip.

G6 THE PINS THE FLIP MOVES, at C3. `python3 -m pytest tests/docs/ -q` at a REAL
exit 0, with its pass count reported. Then run these three by name and report
each REAL exit code separately, because they are the pins the closure moves and
a green suite total can hide which one ran:
`tests/docs/test_docs_consistency.py::TestRoadmapLedgerIsConsistent::test_the_readme_accepted_count_equals_the_status_count`,
`::TestRoadmapLedgerIsConsistent::test_the_readme_tier_table_done_column_matches_the_ledger`
and
`::TestRoadmapLedgerIsConsistent::test_the_readme_reports_the_accepted_foundation_and_no_later_feature`.
If a node id does not resolve, report the resolution error and find the correct
class name with `--collect-only` rather than skipping the pin.

G7 THE STATE AT CLOSURE, at C3. `python3 -m pytest tests/cli/test_golden_path.py -q`
at a REAL exit 0 with its pass count. `python3 -m apps.cli.grouped integrity
check --json` at a REAL exit 0 with `passed` true. `git status --porcelain`
EMPTY. Per-commit insertions from C0a through C3 each under 500. And
`git ls-files --others --exclude-standard` reported as a count.

G8 THE PULL REQUEST, after C3 is pushed.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` must
show EXACTLY ONE entry: head `feature/f033-hunk-approval-v2`, base `main`,
`isDraft` false. Report the raw JSON and the PR number and URL. Report that you
merged NOTHING and that `git log --oneline -n 1 main` is unchanged from its
value at this round's base.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md, IN C3, as the
feature's closing handback: feature and round, SESSION 7 of F033, branch, commit
SHAs, changed-files table, one line per gate G1 through G7 with its REAL exit
code, the open-findings count, an item-status table covering every Bundle item,
every deviation, and the next expected action. No length cap. G8's readings go
in your completion report rather than the handback, because the PR does not
exist when C3 is written. Carry these as their own labelled lines: the accepted
HEAD, the package filename, its SHA-256, its archived path, the evidence job id,
`self-use NONE (queue exhausted)`, and the two open findings R-0745 and R-0750
named as carried risks. Also carry the grep proof the closure protocol requires:
that the applied STATUS line is byte-identical to PAIRSTATUS-TO. If any gate is
RED, do not repair on your own initiative: report it and stop.
