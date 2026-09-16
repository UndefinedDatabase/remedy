── STEP CLOSURE — F261 — ROUND 28 ──
Goal: CLOSURE ROUND B, the last round of this branch. Book round 27's verdict; then ONE closure
commit with the STATUS `[x]` line, the README sync, `SU-015`'s `consumed_by` and the final
handoff; then open the pull request and do NOT merge it.

Base commit: `7a97e74d`, on `feature/f261-cli-vocabulary-v2`. SESSION 7 of F261. Round type:
CLOSURE SEQUENCE. Read AGENTS.md and algorithm steps 4 to 7 of
`docs/roadmap/STATUS_closure_protocol.md` first. NO FULL-SUITE RUN is ordered: the closure commit
is the last commit, the round changes no code, and the integration gate and the reviewer's run at
`7a97e74d` cover the accepted head.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is
two or more characters long is a run of a single repeated character, and every box-drawing rule
inside the STEP and SLICE header lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`. Shell loops, `$(...)` and `$?` in a compound command are
refused by form, so write such checks as Python scripts under `.remedy-wt/f261r28w/`, and never
name a script after a standard-library module. Never call `run_job` or any runner.
`git branch --list 'remedy/job-*'` reads 17 lines at `7a97e74d`; keep it so.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f261-r28.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN28; slice RECORD28 is appended to
    `.agent/live_review.md`; `.remedy-wt/f261-block/f261-r28-closure.jsonl` is copied to
    `.agent/authored/f261-r28-closure.jsonl`
C2  THE CLOSURE COMMIT, and the LAST commit on this branch: the table applied per THE TABLE, and
    the `.agent/handoff.md` rewrite, ALL IN ONE COMMIT. Then push, the gates, and the pull request.

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. There is no C3. Push after C1 and C2.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f261-r28.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md` and `.agent/authored/f261-r28-closure.jsonl`. C2: exactly
`docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`.

## The append

RECORD28 begins with an empty line, and `.agent/live_review.md` ends in a newline at `7a97e74d`:
the append is the file's bytes followed by the slice's bytes, and nothing else.

## THE TABLE

The carrier holds one JSON array per line, sha256
`6c9a60ebd06e973d53c77b669a605fbb19d7ac905a2f93bae597b4388fcb6417`; verify it before copying and read the
COMMITTED copy at C1 to apply it. Apply its rows strictly in file order, from the repository root:
`["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`, requires the
number of occurrences of `old` to equal `count` exactly, replaces every occurrence with `new`, and
writes the file back with the same settings. Each file is edited as TEXT; the JSON queue is never
loaded and re-dumped (finding R-0785). A count that differs is a STOP: touch nothing further,
commit nothing of the table, and hand back with the row and the reading. The table is the
reviewer's measured dry run on `7a97e74d`: every `old` occurs exactly once there, and no `new`
contains its `old`.

## The handoff, inside C2

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 7 of feature F261 · round 28 · rounds so far 28`. It carries the commit SHAs through C1
and says that C2's own numstat and the pull request's number cannot exist while C2 is written, so
they are reported in the completion message; the five closure values of RECORD28's round, which
are the ones round 27's handback at `7a97e74d` carries; the open findings at 125 with the three
open High ids, R-0803, R-0804 and R-0807; `Operator questions open: 1`; and a `## Next` naming, in
this order, Phase 1 rule 1, the Open PR Gate merging this branch's pull request, and Rule A5
claiming F280. Its Session section states that this session ran the three delegated rounds 26 to
28, F261's whole closure sequence; that rounds 26 and 27 have PASS verdicts on the record; that
round 28's verdict is written by the reviewer into the pull request because no commit may follow
the closure commit; that the session ends below the six-to-eight target because the closure
commit ends the branch and the next feature needs a fresh session by closure protocol step 7; and
one sentence of context self-assessment. It carries NO new scope report and no session-limit
banner, for the reason round 26's handback gave, and no item-status row for C2's own numbers.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a and before C2, with real exit codes. If it exists: finish a
   half-written commit, write the handoff, push, stop.
3. C2 is the LAST COMMIT on this branch. A gate that fails after it is reported in the completion
   message, and nothing is committed to repair it.
4. Scratch lives under `.remedy-wt/f261r28w/`, uncommitted; no `.py` file under `.agent/`. Under
   `.remedy-wt/` open only `.remedy-wt/f261-block/` and your own directory. No worktree.
5. Every commit stays under 500 insertions, read as the first column of
   `git show --numstat --format= <commit>`. The append of C1 has a zero deletion column.
6. NEVER merge the pull request and never enable auto-merge; never force-push, rewrite history,
   create or delete a branch, or touch the review package. No `remedy`. `gh` only for G7.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 204 lines TOTAL and 158 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice
   CONTENT — the `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3 to G6 after C2 and its push; G7 last.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and no
   subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r28.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; the committed carrier's sha256 equals THE TABLE's digest.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN28, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once. `.agent/live_review.md` equals its `7a97e74d` blob
followed by RECORD28, which the reviewer's own application reads as 623791 bytes with sha256
`2000394aeac3ba2d1f420ddd7db5687d184110b4a4d2f40ae7b83409c7a84628`. `^Gate: F\d+ R\d+ — ` reads 26 at `7a97e74d` and 27 at C1, with
`Gate: F261 R27 — ` 0 times and once; the open set by distinct id reads 125 at both with identical
membership.

G3 THE CLOSURE COMMIT'S SHAPE. `git show --numstat --format=` of C2 names exactly the four paths
of the Change section for C2, with at most 500 insertions; C2 has one parent and is the branch
tip, pushed and equal to `origin/feature/f261-cli-vocabulary-v2`. For each table row, over the
committed target at C2: `old` occurs 0 times and `new` exactly once.

G4 THE AUTHORED TEXT LANDED. (a) The `F261` line of `docs/roadmap/STATUS.md` at C2 with its
newline equals the `new` of the table's first row, and the count of lines matching `^- \[x\] ` in
that file equals the number in `<n> of 280 registered items accepted.` in `README.md`: the
reviewer read 78 for both in its dry run. (b) Through `packages.orchestration.self_use_queue`:
`pending_self_use_items(Path("scripts/self_use_queue.json"))` is empty, `next_self_use_item(...)`
is `None`, and `SU-015`'s `consumed_by` is exactly `F261`; the count of the six-character text
`—` in the queue file is the same at `7a97e74d` and at C2, which the reviewer read as 94 and 94.

G5 THE DOCS GATE AND THE CANARY, after C2, from the primary checkout's root, serially:
`python3 -B -m pytest tests/docs/ -q -p no:randomly`, then
`python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly`, then
`python3 -B -m pytest -q -p no:randomly tests/orchestration/test_self_use_queue.py
tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py`.
Report each exit code and summary line; each MUST be exit 0. The reviewer's dry run of these edits
read 364 passed over `tests/docs/` and the three self-use files together, and with the count edit
withheld read `tests/docs/` exit 1 on the accepted-count pin alone.

G6 THE CLOSING STATE. Over the committed ledger at C2: the open set by distinct id, 125, and the
ids of every open finding whose registration line reads `— High` directly after its id, which must
be exactly R-0803, R-0804 and R-0807. Then `packages.orchestration.integrity_gate
.run_integrity_checks()` from the repository root: `.passed`, `.fail_count`, and the `name`,
`status` and `message` of its `high_blockers_open` check verbatim beside that list.

G7 THE PULL REQUEST AND THE TREE. `git status --porcelain` prints `''`. Write the body to a file
under `.remedy-wt/f261r28w/` and run `gh pr create --base main --head
feature/f261-cli-vocabulary-v2 --title "<title>" --body-file <that file>`, not a draft, titled
`F261: CLI vocabulary v2 (rename & prune) — split at the soft limit, the rest is F280`. The body
carries: what changed and why, from the feature file's Built State; the key decisions, naming
DECISION F261 D25 and D26 and operator question Q3; how to review, naming the package by filename,
SHA-256 and absolute directory; a changed-files summary by top directory from
`git diff --stat 7cdde89b..<C2>`; the latest verdict, PASS_WITH_RISKS; the open findings at 125
with the three open High ids; the runtime actuals — 28 rounds across 7 sessions of this feature,
the self-use run on provider `ollama`, and `not-measured` for tokens and cost; and, as its last
line, `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. Report the pull request's
number and URL. DO NOT MERGE IT. Then `git worktree list` one row and `git branch --list
'remedy/job-*'` 17 lines.

── SLICE PLAN28 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN28 sha256=ee505a589a738878b1fef32a3f657e9b7b2d4e2c7ee26f2fe400f4ebccbdc92a
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md` — as far as this feature reaches it; DECISION F261 D25
moves the rest to F280. Everything the closure protocol asks for is on disk: the Built State,
the integration gate, the self-use run, the rotated ledger and a READY_FOR_REVIEW package.

## Current Step

CLOSURE ROUND B, the last round of this branch. Its bookkeeping commit books round 27's verdict.
Its closure commit then applies the STATUS `[x]` line authored from round 27's measured values,
the README sync and `SU-015`'s `consumed_by` set to `F261`, with the final handoff, in ONE
commit, per the closure protocol's Rule A4 ordering; then the pull request is opened and NOT
merged.

## Next Steps

1. THE NEXT SESSION: Phase 1 rule 1 first, `.agent/STOP`; then the Open PR Gate merges this
   branch's pull request; then Rule A5 claims F280.

## Risks

- The open findings stand at 125 by distinct id. Three are High — R-0803, R-0804 and R-0807 —
  none of them F261's, and the integrity gate's `high_blockers_open` check does not see them,
  which is R-0648; so the close is PASS_WITH_RISKS.
- F261 closes with the Goal & Done sentence not met, and says so in its Built State; the
  operator may reverse the split through operator question Q3.
- The closure commit is the last commit on the branch, so the docs gate its own STATUS and
  README edits must satisfy runs after it; the reviewer ran that gate against the same edits in
  a disposable worktree before authoring.
END PLAN28

── SLICE RECORD28 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD28 sha256=dce1486fd115a77de343bab0c60faae072266c9f6fd403074e9ce81bbbff506c

Gate: F261 R27 — the F261 round 27 entry, CLOSURE ROUND A. VERDICT PASS. Written by the planner and reviewer of session 42 after reading the committed range `f2872a33`..`7a97e74d` and re-deriving every reading that bears on the verdict, the package read out of the archive file itself; the worker's report and its transcripts were evidence for no line below. It is booked here by the first commit of round 28 that writes the record, per operator amendment amend0827-process-diet rule 1.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/f261-r27.md` at `417ba82e` and `.agent/last_block.md` at `f8f8be60` equal the reviewer's scratch original at 19913 bytes; `.agent/plan.md` at `fb510ca7` equals PLAN27; `.agent/live_review.md` there equals its blob at `f2872a33` followed by RECORD27, 1135907 bytes.

THE ROTATION. `30343f92` changes exactly `.agent/live_review.md` and `.agent/live_review_archive.md`, 762 insertions against 762 deletions, the ledger going from 1135907 to 620380 bytes and the archive from 2948965 to 3464492, and both files there carry the sha256 digests the reviewer's own dry run of the script on the same appended ledger produced. The archive at `fb510ca7` is an exact prefix of the archive at `30343f92`; the 110 `Gate:` records the rotation removed all belong to features that are `[x]` in `docs/roadmap/STATUS.md`, and each is present in the archive's appended bytes; none of F261's 26 `Gate:` records moved; and the open set is 125 by distinct id on both sides with identical membership. The commit is the declared-oversize commit of this feature under DECISION F272 D18, declared in the handback at `7a97e74d`, and walking every non-merge commit from `7cdde89b` to `7a97e74d` finds no other commit reaching 500 insertions.

THE EVIDENCE AND THE PACKAGE. The accepted head is `30343f927800784c464eaf56706d5b82ece39c81`, and only the handback follows it. The evidence job `234c8e6f18905013` was produced by `create_manual_completion_bundle` against the fork point `7cdde89b5d0dc8ef1fb96980105870e956699873`, whose ancestry-path and plain chain counts to the accepted head are equal at 183, with one verification record of `tests/docs/` at 310 passed and 310 node ids, and its verdict is `PASS_WITH_RISKS`, which the reviewer's dry run on a throwaway head had predicted. The package `remedy-review-20260916-151540-READY_FOR_REVIEW.zip` in `/home/decodeux/Repos/remedy-history/zips` hashes, recomputed by the reviewer from the file, to `8bc443e91657986bcbb83ad3b6d81cb55afd4b111ff7d4e6930983606f545275`; its manifest `.review_zip_manifest.json`, read out of the archive, records `package_status` `READY_FOR_REVIEW`, the evidence job `234c8e6f18905013`, and a `committed_review_subject` from the fork point to the accepted head over 183 commits. `run_integrity_checks()` returned `passed` True with no failure, in the worker's run at `30343f92` and in the reviewer's at `f2872a33`, and its `high_blockers_open` check read `no open blocker/high findings`, which is false while R-0803, R-0804 and R-0807 are open, the gap R-0648 records.

THE SUITE, closure precondition 2. The reviewer's run of `python3 -m pytest -n auto -q -rfE` in the primary checkout at `7a97e74d`, which differs from the accepted head only in `.agent/handoff.md`, read exit 0 with 17653 passed and 23 skipped and no failed node, re-confirming the integration gate booked above.
END RECORD28
