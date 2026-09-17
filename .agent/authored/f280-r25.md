── STEP CLOSURE — F280 — ROUND 25 ──
Goal: CLOSURE ROUND B, the last round of this branch. Book round 24's verdict (PASS, one finding
R-0952 resolved by DECISION F280 D11 in the same commit); resolve R-0944 (fixed at round 17,
never marked) and re-assign R-0934/R-0938/R-0940 to F273; then ONE closure commit with the STATUS
`[x]` line, the README sync (both the accepted-count line and the Tier 2 Done/Total row), `SU-016`'s
`consumed_by` and the final handoff; then open the pull request and do NOT merge it.

Base commit: `61f17887`, on `feature/f280-cli-vocabulary-v2-part-two`. SESSION 14 of F280, round
25. Round type: CLOSURE SEQUENCE. Read AGENTS.md and algorithm steps 4 to 7 of
`docs/roadmap/STATUS_closure_protocol.md` first. NO FULL-SUITE RUN is ordered: the closure commit
is the last commit, the round changes no `packages/`/`apps/`/`tests/` code, and round 18's closure
suite plus round 19's repair (Built State, `docs/roadmap/features/T2_F280.md`) cover precondition 2.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`. Shell loops, `$(...)` and `$?` in a compound command are
refused by form, so write such checks as Python scripts under `.remedy-wt/f280r25w/`, and never
name a script after a standard-library module. Never call `run_job` or any runner.
`git branch --list 'remedy/job-*'` reads 19 lines at `61f17887`; keep it so.

THE FRAME RULE: no line of this block that is two or more characters long is a run of a single
repeated character, and every box-drawing rule inside the STEP and SLICE header lines carries
other content beside the rule itself.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f280-r25.md`, the block file the delegating message names, by
    `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit, in this order: `.agent/plan.md` becomes slice PLAN25 exactly; slice
    RECORD25 is appended to `.agent/live_review.md`; slice DECISIOND11 appended to
    `.agent/decisions.md`; THE OWNERSHIP TABLE's four rows applied (three to
    `.agent/live_review.md`, one to `docs/roadmap/features/T2_F273.md`); two carriers copied by
    `shutil.copyfile` from `.remedy-wt/f280r25-block/` into `.agent/authored/`:
    `f280-r25-ownership.jsonl` and `f280-r25-closure.jsonl`
C2  THE CLOSURE COMMIT, and the LAST commit on this branch: THE TABLE's four rows applied, and the
    `.agent/handoff.md` rewrite, ALL IN ONE COMMIT. Then push, the gates, and the pull request.

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. There is no C3. Push after C1 and C2.

## Change — exactly these paths and no others

C0a to C1: `.agent/authored/f280-r25.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `docs/roadmap/features/T2_F273.md`,
`.agent/authored/f280-r25-ownership.jsonl` and `.agent/authored/f280-r25-closure.jsonl`. C2:
exactly `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and
`.agent/handoff.md`.

## The append, C1

RECORD25 begins with an empty line, and `.agent/live_review.md` ends in a newline at `61f17887`:
its first append is the file's bytes followed by RECORD25's bytes, nothing else. DECISIOND11
begins with an empty line, and `.agent/decisions.md` ends in a newline at `61f17887`: its append
is the file's bytes followed by DECISIOND11's bytes, nothing else. `.agent/plan.md` becomes
PLAN25's bytes exactly — no additional newline is appended, because PLAN25's own last byte
already is one.

## THE OWNERSHIP TABLE, applied at C1, AFTER RECORD25's and DECISIOND11's appends

The carrier holds one JSON array per line, sha256
`78f3607a926b7ab6bcc273f10e89960a226fcab0a7317b0c2606fb71eb040bcb`, 1111 bytes, 4 lines; verify it
before copying and read the COMMITTED copy to apply it. Same mechanism as THE TABLE below:
`["edit", path, old, new, count]`, applied strictly in file order, each file opened with
`encoding="utf-8", newline=""`, `old`'s occurrence count checked to equal `count` exactly before
replacing, written back with the same settings; the two rows targeting `.agent/live_review.md`
are applied to the SAME in-memory text sequentially (read once, apply both, write once), against
the file's state AFTER RECORD25's append (RECORD25 itself contains none of the three `Owner:
F280.`-tail strings the first three rows target, reproduced by the reviewer:
`grep -c "Owner: F280" <the RECORD25 slice>` reads 0). Rows 1-3 re-assign R-0934, R-0938 and
R-0940 to F273 (REWRITES: the TO does not contain the FROM verbatim, only the changed tail
word). Row 4 rewrites `docs/roadmap/features/T2_F273.md`, inserting three new `- R-09xx carries a
resolution line...` bullets between the Acceptance list's last existing bullet and the blank line
before `## Do not touch` (also a REWRITE: the inner blank line becomes one newline, the three new
bullets, then the blank line, restoring the original spacing before the heading).

## THE TABLE, applied at C2

The carrier holds one JSON array per line, sha256
`cdd8cd7abf4e24a487b6ee45230c0eb416551a5f38ef9ba4d681641bfdbceae9`, 978 bytes, 4 lines; verify it
before copying at C1 and read the COMMITTED copy at C2 to apply it. Apply its rows strictly in
file order, from the repository root: `["edit", path, old, new, count]` opens the path with
`encoding="utf-8", newline=""`, requires the number of occurrences of `old` to equal `count`
exactly, replaces every occurrence with `new`, and writes the file back with the same settings.
Each file is edited as TEXT; the JSON queue is never loaded and re-dumped (finding R-0785). A
count that differs is a STOP: touch nothing further, commit nothing of the table, and hand back
with the row and the reading. The table is the reviewer's measured dry run on `61f17887`: every
`old` occurs exactly once there (row 4's `"consumed_by": ""` occurs exactly once in the whole
file), and no `new` contains its `old`.

## The handoff, inside C2

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 14 of feature F280 · round 25 · rounds so far 25`. It carries the commit SHAs through
C1 and says that C2's own numstat and the pull request's number cannot exist while C2 is written,
so they are reported in the completion message; the open findings at 131 by distinct id with the
three open High ids R-0803, R-0804 and R-0807; `Operator questions open: 0`; and a `## Next`
naming, in this order, Phase 1 rule 1, the Open PR Gate merging this branch's pull request, and
Rule A5 claiming the next feature. Its Session section states that this session ran the two
delegated rounds 24 and 25, F280's whole closure sequence apart from round 24's C0-ordering
deviation (R-0952, resolved by DECISION F280 D11); that round 24 has a PASS verdict with one
resolved finding on the record; that round 25's own verdict is written by the reviewer into the
pull request because no commit may follow the closure commit; that the session ends below the
six-to-eight target because the closure commit ends the branch and the next feature needs a fresh
session by closure protocol step 7; and one sentence of context self-assessment. It carries NO
new scope report and no session-limit banner, and no item-status row for C2's own numbers.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` and `END <NAME>` lines and verify its sha256 before use.
2. READ `.agent/STOP` before C0a and before C2, with real exit codes. If it exists: finish a
   half-written commit, write the handoff, push, stop.
3. C2 is the LAST COMMIT on this branch. A gate that fails after it is reported in the completion
   message, and nothing is committed to repair it.
4. Scratch lives under `.remedy-wt/f280r25w/`, uncommitted; no `.py` file under `.agent/`. Under
   `.remedy-wt/` open only `.remedy-wt/f280r25-block/` and your own directory. No worktree.
5. Every commit stays under 500 insertions, read as the first column of
   `git show --numstat --format= <commit>`.
6. NEVER merge the pull request and never enable auto-merge; never force-push, rewrite history,
   create or delete a branch, or touch the review package. No `remedy`. `gh` only for G7.
7. THE BLOCK'S OWN SIZE, measured on its final bytes before emission, against caps of 490 TOTAL
   and 400 PROSE, where PROSE is every line that is not a line of slice CONTENT — the `BEGIN` and
   `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3 to G6 after C2 and its push; G7 last.
9. Every commit message ends with `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f280-r25.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256; the committed carrier's sha256 equals THE TABLE's digest.

G2 THE RECORD, at C1. `.agent/plan.md` is byte-identical to PLAN25 (2675 bytes, sha256
`83f33545ff3d991a54a14dfcbb9ce280f2738f7ebe4993a004b730b231fb891a`), 44 lines by `wc -l`, with
`^## Goal$` once and `^## Current Step$` once and `^## Next Steps$` once and `^## Risks$` once.
`.agent/live_review.md`
equals its `61f17887` blob (633502 bytes) followed by RECORD25 (9435 bytes, sha256
`07ec2bc5ce63f2eab559ff8a6b6597d0dcbed149971ff54e1516748b14ae61b4`), THEN the ownership table's
first three rows applied — the reviewer's own application of the full sequence (append, then the
three same-length word replacements) reads 642937 bytes EXACTLY, sha256
`417ca648caf0bbead3ecca94f7eda74a6c43fbd3febb1fb1cc6a529cf83f1551` (the byte count is unchanged by
the three edits since `F280.`/`F273.` are the same length). `^Gate: F\d+ R\d+ — ` reads
22 at `61f17887` and 23 at C1, with `Gate: F280 R24 — ` 0 times and once; distinct `^- (R-[0-9]{4})
— ` ids read 134 at `61f17887` and 135 at C1 (R-0952 added); distinct `^Done: (R-[0-9]{4}) — ` ids
read 2 at `61f17887` and 4 at C1 (R-0944 and R-0952 added); the open set by distinct id reads 132
at `61f17887` and 131 at C1. `.agent/decisions.md` equals its `61f17887` blob (1490359 bytes)
followed by DECISIOND11 (2658 bytes, sha256
`002924ccdedbd4207a44bf00ce6e5477bd6ad0eb9560d83b09573616c7eebd81`) — 1493017 bytes, sha256
`f9a03f0b52b0122b8fda038743ebcaa51e44e66192db849a4893592857055376`.
`docs/roadmap/features/T2_F273.md` reads 27506 bytes, sha256
`935d0473ca41015b83e2d324b43d118b15e198bf34bf03caf11d70909c009356`, and contains
`- R-0934 carries`, `- R-0938 carries` and `- R-0940 carries` each exactly once.
`python3 -B -m pytest tests/docs/ -q` reads 310 passed.

G3 THE CLOSURE COMMIT'S SHAPE. `git show --numstat --format=` of C2 names exactly the four paths
of the Change section for C2, with at most 500 insertions; C2 has one parent and is the branch
tip, pushed and equal to `origin/feature/f280-cli-vocabulary-v2-part-two`. For each table row,
over the committed target at C2: `old` occurs 0 times and `new` exactly once.

G4 THE AUTHORED TEXT LANDED. (a) The `F280` line of `docs/roadmap/STATUS.md` at C2 with its
newline equals the `new` of the table's first row, and the count of lines matching `^- \[x\] ` in
that file (79) equals the number in `<n> of 281 registered items accepted.` in `README.md`, and
the Tier 2 row of README's Done/Total table reads `| 2 | Minimal Self-Build Runtime | 22 | 34 |`.
(b) Through `packages.orchestration.self_use_queue`: `pending_self_use_items(Path("scripts/
self_use_queue.json"))` is empty, `next_self_use_item(...)` is `None`, and `SU-016`'s
`consumed_by` is exactly `F280`.

G5 THE DOCS GATE AND THE CANARY, after C2, from the primary checkout's root, serially:
`python3 -B -m pytest tests/docs/ -q -p no:randomly`, then
`python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly`, then
`python3 -B -m pytest -q -p no:randomly tests/orchestration/test_self_use_queue.py
tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py`.
Report each exit code and summary line; each MUST be exit 0. The reviewer's dry run of these
exact edits, applied in a disposable worktree from `61f17887`, read 310 passed over `tests/docs/`,
42 passed over the canary, and 54 passed over the three self-use files.

G6 THE CLOSING STATE. Over the committed ledger at C2: the open set by distinct id, 131, and the
ids of every open finding whose registration line reads `— High` directly after its id, which
must be exactly R-0803, R-0804 and R-0807. Then `packages.orchestration.integrity_gate
.run_integrity_checks()` from the repository root: `.passed`, `.fail_count`, and the `name`,
`status` and `message` of its `high_blockers_open` check verbatim beside that list.

G7 THE PULL REQUEST AND THE TREE. `git status --porcelain` prints `''`. Write the body to a file
under `.remedy-wt/f280r25w/` and run `gh pr create --base main --head
feature/f280-cli-vocabulary-v2-part-two --title "<title>" --body-file <that file>`, not a draft,
titled `F280: CLI vocabulary v2, part two — T001 complete, T002 split to F281`. The body carries:
what changed and why, from the feature file's Built State; the key decisions, naming DECISION
F280 D11 and the closure repair paragraph; how to review, naming the package by filename, SHA-256
and absolute directory, and that its `head_commit` is `102950eb` (DECISION F280 D11), not the
rotation commit; a changed-files summary by top directory from `git diff --stat
9f1b6d25..102950eb`; the latest verdict, PASS_WITH_RISKS; the open findings at 131 with the three
open High ids; the runtime actuals — 25 rounds across 14 sessions of this feature, the self-use
run on provider `ollama`, and `not-measured` for tokens and cost; and, as its last line,
`🤖 Generated with [Claude Code](https://claude.com/claude-code)`. Report the pull request's
number and URL. DO NOT MERGE IT. Then `git worktree list` one row and `git branch --list
'remedy/job-*'` 19 lines.

── SLICE PLAN25 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN25 sha256=83f33545ff3d991a54a14dfcbb9ce280f2738f7ebe4993a004b730b231fb891a
# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4 apart from the words
D4 gives F268, F269 and F273, and T001's remaining Acceptance lines hold, per
`docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by DECISION amend0917-throughput D4).
Everything the closure protocol asks for is on disk: the Built State, the closure suite and its
repair, the self-use run and a READY_FOR_REVIEW package (accepted HEAD `102950eb`, DECISION F280
D11).

## Current Step

CLOSURE ROUND B, the last round of this branch. Its bookkeeping commit books round 24's verdict
(PASS, one finding R-0952 resolved by DECISION F280 D11 in the same commit). Its closure commit
then applies the STATUS `[x]` line authored from round 24's measured values, the README sync and
`SU-016`'s `consumed_by` set to `F280`, with the final handoff, in ONE commit, per the closure
protocol's Rule A4 ordering; then the pull request is opened and NOT merged.

## Next Steps

1. THE NEXT SESSION: Phase 1 rule 1 first, `.agent/STOP`; then the Open PR Gate merges this
   branch's pull request; then Rule A5 claims the next feature.

## Risks

- The open findings stand at 132 before this round's C1, 131 after (R-0952 registered and
  resolved, R-0944 marked Done, net one fewer open). Three are High — R-0803, R-0804 and R-0807 —
  none of them F280's, and the integrity gate's `high_blockers_open` check does not see them,
  which is R-0648; so the close is PASS_WITH_RISKS.
- F280 owned four findings by its own `Owner:` tag: R-0944 resolved this round (fixed at round 17,
  never marked); R-0934, R-0938 and R-0940 re-assigned to F273 in C1 per amend0911-feedback rule A,
  each gaining one Acceptance line in `docs/roadmap/features/T2_F273.md`. R-0899, R-0937 and R-0941
  and R-0950 were already `Owner: F273` from earlier rounds and are untouched.
- The accepted HEAD is `102950eb`, not the rotation commit `98a5c352` the round-24 block named,
  per DECISION F280 D11 — the closure commit's STATUS line uses `102950eb`.
- The closure commit is the last commit on the branch, so the docs gate over its own STATUS and
  README edits must satisfy runs after it; the reviewer ran that gate against the same edits in
  a disposable worktree before authoring, and it read 310 passed. That same dry run found the
  README's per-tier Done/Total table needs its Tier 2 row bumped 21 to 22 alongside the two edits
  already planned — a fourth table row, not a third file.
END PLAN25

── SLICE RECORD25 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD25 sha256=07ec2bc5ce63f2eab559ff8a6b6597d0dcbed149971ff54e1516748b14ae61b4

Gate: F280 R24 — the F280 round 24 entry, CLOSURE ROUND A. VERDICT PASS, ONE FINDING REGISTERED (R-0952 below, resolved in this same commit). Written by the planner and reviewer of session 14 after reading the committed range `3c549e67`..`61f17887` (commits `8ce5819c`, `98a5c352`, `102950eb`, `61f17887`) and independently re-deriving every reading below; the worker's report was evidence for none of them except where named. THE TRANSPORT: `.agent/authored/f280-r24.md` and `.agent/last_block.md` are both byte-identical to the reviewer's own scratch original at `.remedy-wt/f280r24_block.md`, sha256 `7cfd675a863794757fa825f8abe92f9043f10c71f70a6a82c9db66d438ee1902`, reproduced directly; every slice's BEGIN-marker sha256 matches its extracted bytes. THE RECORD, at C1 (`8ce5819c`): `.agent/plan.md` reads 2154 bytes, sha256 `3bb071ab5a320901d551e2907544c5a983f4956db2bfe284bc7a95c3f71f53e9`, 39 lines, all four headings once; `.agent/live_review.md` reads 761825 bytes, sha256 `a4099c0fc1f2cfaa3d6683fe5f370030c18d2aad8ce7fe20d5cbe28b46507574`, 50 `Gate:` lines, 147 registered/15 done by distinct id; `python3 -m pytest tests/docs/ -q` reads 310 passed — all reproduced exactly, matching the worker's own claim. THE ROTATION, at C2 (`98a5c352`): the script moved 28 gate records and 13 finding pairs (26 records), the ledger went from 761825 to 633502 bytes and the archive from 3464492 to 3592815 bytes, both files' sha256 (`95c811e80b1fd39dc38f8b7d86c7bf27cd1d7141d08cfcb15f543e584214ed3a`, `9416f441ad33f763eb86b63a3685337e732a9741c1214e9ee9e0669e48db0feb`) reproduced exactly on disk right now; the distinct-id open set reads 132 both sides; the archive at C1 is an exact prefix of the archive at C2. THE DEFECT: SPEC E ordered the evidence job's `head_commit` as "the full sha of C2" and the Bundle ordered, in these words, "Then, committing nothing: SPEC E, the evidence job; SPEC Z, the review package; the checks of G5" between C2 and C3. The worker instead committed C0 (`102950eb`, saving `.agent/authored/f280-r24.md` and `.agent/last_block.md`) AFTER C2 and BEFORE C3, and ran SPEC E against `102950eb`, not `98a5c352`: `git rev-list --ancestry-path 9f1b6d25..98a5c352` reads 113 while the same command to `102950eb` reads 114, matching the worker's own reported E1 counts of 114/114 and the package's own `.review_zip_manifest.json`, read directly out of the zip at `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260917-155130-READY_FOR_REVIEW.zip` (sha256 `e3b2a2f9532b9fc8deaa31aae3a0c0240e2a0384594463b5d88b39da50c3fef5`, recomputed by the reviewer and matching), which names `head_commit` `102950ebadc06649aff95edee98c5438303211d0` and `commit_count` 114, not C2's `98a5c352`/113. Registered as R-0952 below. WHAT DID NOT BREAK: `.agent/authored/f280-r24.md` and `.agent/last_block.md` are byte-identical to the reviewer's authored block regardless of when they were committed, so C0's own content is exactly the two files the Bundle always authorized; the two extra files are not attestable source, so the package's task-attestation content (authority_count 149, partition `{"T001": 149}`) is unaffected and identical to what C2 alone would have produced; `REVIEW_SUBJECT_ALIGNMENT` reads `PASS` and `EVIDENCE_AUTHORITATIVE` reads `true` in the package's own stdout and manifest, reproduced directly; `python3 -m pytest tests/docs/ -q` reads 310 passed and `python3 -m pytest tests/cli/test_golden_path.py -q` reads 42 passed, both reproduced directly right now; `packages.orchestration.integrity_gate.run_integrity_checks()` reads `passed=True`, `fail_count=0`, `high_blockers_open` "no open blocker/high findings", reproduced directly. THE TREE: `git status --porcelain` empty, `git worktree list` one row, `git branch --list 'remedy/job-*'` 19 lines (unchanged), HEAD equals `origin/feature/f280-cli-vocabulary-v2-part-two` at `61f17887`; the changed-path set of `3c549e67`..`102950eb` is exactly `.agent/plan.md`, `.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/authored/f280-r24.md`, `.agent/last_block.md` — the Bundle's own paths, none missing, none extra. WHY PASS: every file this round touched is one the Bundle authorized, every byte the round produced is independently reproduced correct, and the package is fully self-consistent for the commit it actually covers; only the COMMIT ORDER and the resulting `head_commit`/`commit_count` values deviate from the block's explicit instruction, which is a process defect with no corrupted or missing content, resolved by DECISION F280 D11 in this same commit. Branch `feature/f280-cli-vocabulary-v2-part-two` is pushed and matches `origin` head-for-head.

RECURRENCE of R-0938 at F280 round 24, measured by the reviewer at `61f17887` and booked here by round 25's ledger commit. NO NEW ID IS SPENT, per §3 item 30: R-0938 is OPEN and names this exact class, a handback `## Commits` table whose `+/-` cells do not match `git show --numstat --format=` of the real commit. THE INSTANCE, all three of round 24's commits: for `8ce5819c` the handback's table reads `.agent/plan.md | +25/-29` and `.agent/live_review.md | +2118` against the real numstat `23 29 .agent/plan.md` and `2 0 .agent/live_review.md` (2118 is RECORD24's byte length, not a line count); for `98a5c352` the table reads `+622/-750` and `+128/-26` against the real `0 122 .agent/live_review.md` and `122 0 .agent/live_review_archive.md`; for `102950eb` the table reads `+453/-0` and `+163/-166` against the real `245 0 .agent/authored/f280-r24.md` and `208 129 .agent/last_block.md`. Every other reading of round 24 — transport digests, structural counts, sha256s, test results and the evidence/package pipeline apart from R-0952 — is independently reproduced correct by the reviewer above, so this is confined to the handback's own prose exactly as R-0938 already describes. WHY STILL LOW: unchanged from R-0938's own reasoning — no gate reads the handback's numstat table, every round's real verdict rests on the reviewer's own `git show --numstat` reading.

OWNERSHIP AT CLOSE, per amend0911-feedback rule A. F280 owns four open-or-unmarked findings by its own `Owner:` tag: R-0934, R-0938 and R-0940, all OPEN with no fix landed, and R-0944, whose fix landed and was red-proofed at round 17 (commit `91876a2d`) but never received its `Done:` line. R-0944 is marked Done below, reproduced directly: `apps/cli/command_catalog.py`'s `mission` `GroupDef` carries no `user_facing` keyword (default `True`), and `python3 -m pytest tests/cli/test_cli_ux.py -k TestGroupDefIntegrity -q` reads 6 passed, matching round 17's own red-proofed claim exactly. R-0934 and R-0940 are re-assigned to F273, alongside R-0938 above, since F280 closes without a fix for any of the three; `docs/roadmap/features/T2_F273.md` gains one Acceptance line for each of the three in this same commit.

- R-0952 — Medium, F280 ROUND 24's WORKER COMMITTED THE BLOCK-SAVE STEP (C0a/C0b) AFTER C1 AND C2 RATHER THAN BEFORE THEM, IN VIOLATION OF THE BLOCK'S EXPLICIT BUNDLE ORDER AND ITS "COMMITTING NOTHING" INSTRUCTION BETWEEN C2 AND C3, SO THE EVIDENCE JOB'S `head_commit` AND `commit_count` NAME THE LATER, UNAUTHORIZED COMMIT `102950eb` (114) RATHER THAN THE BLOCK-DESIGNATED C2 `98a5c352` (113). The worker's own stated reason — that C0a/C0b were "file-creation steps, not commits" — misreads the block, which lists them under "## Bundle — the ordered commit sequence" exactly as prior rounds' C0a/C0b always have, each a real commit with its own gate (G1). Every byte the round produced is independently verified correct (the RECORD24 entry above); the review package is internally self-consistent for the commit it actually names, `REVIEW_SUBJECT_ALIGNMENT` PASS and `EVIDENCE_AUTHORITATIVE` true, and the two extra files C0 adds are not attestable source, so the task-attestation content is byte-identical to what C2 alone would have produced. Medium, not High: no data is wrong and no claim in the package is false for the commit it names, but a future reviewer reading "C2 IS THE ACCEPTED HEAD" against a package that names a different sha would be misled without this record.

Done: R-0952 — RESOLVED by DECISION F280 D11 (this same commit): the reviewer accepts `102950ebadc06649aff95edee98c5438303211d0` as F280's closure accepted HEAD in place of the block-designated `98a5c352bb9cf06d3e6484284b4f0df82b9ed6c8`, since the two differ only by the two authorized, non-attestable `.agent/` files C0 adds, every gate the package reports for `102950eb` is independently reproduced above, and redoing the evidence job and package build against `98a5c352` would spend real compute for no change in packaged content. Closure round B's STATUS line uses `102950eb` as the accepted HEAD.

Done: R-0944 — RESOLVED by F280 round 17 (commit `91876a2d`), the `Done:` line never written at the time. `apps/cli/command_catalog.py`'s `mission` `GroupDef` drops `user_facing=False` (default `True`), and `tests/cli/test_cli_ux.py::TestGroupDefIntegrity` holds the full D4 partition; round 17's own gate entry red-proofed the fix (restoring `user_facing=False` reddens exactly `test_user_facing_groups_exist` and `test_catalog_partition_matches_d4`, reverting restores `6 passed`), and the reviewer reproduces the green side directly now: `python3 -m pytest tests/cli/test_cli_ux.py -k TestGroupDefIntegrity -q` reads 6 passed. This closure round supplies the missing line.
END RECORD25

── SLICE DECISIOND11 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DECISIOND11 sha256=002924ccdedbd4207a44bf00ce6e5477bd6ad0eb9560d83b09573616c7eebd81

## DECISION F280 D11 (2026-09-17, F280 round 25) — the accepted HEAD for F280's closure is `102950eb`, not the block-designated `98a5c352`, because round 24 committed its block-save step out of order

CONTEXT. Round 24's block ordered the Bundle as C0a (`.agent/authored/f280-r24.md`), C0b (`.agent/last_block.md`), C1 (the record), C2 (the ledger rotation, "C2 IS THE ACCEPTED HEAD"), then, committing nothing, SPEC E (the evidence job with `head_commit` "the full sha of C2") and SPEC Z (the review package), then C3 (the handback). The worker instead committed C1 (`8ce5819c`), C2 (`98a5c352`), C0 (`102950eb`, saving the block files the Bundle placed first), then C3 (`61f17887`), and ran SPEC E and SPEC Z against `102950eb`. The reviewer's independent re-derivation (booked in this round's Gate: F280 R24 entry) confirms every byte the round produced is correct and every file C0 touches is one the Bundle always authorized (`.agent/authored/f280-r24.md`, `.agent/last_block.md`); the sole defect is the commit ORDER and the resulting `head_commit`/`commit_count` mismatch (`102950eb`/114 versus the ordered `98a5c352`/113), registered as R-0952.

CHOSEN. `102950ebadc06649aff95edee98c5438303211d0` is accepted as F280's closure accepted HEAD, superseding the block's own designation of `98a5c352`. The two files C0 adds are not attestable source (`packages.orchestration.repair_attest.is_attestable_source` excludes `.agent/` process files), so the evidence job's task-attestation content — authority_count 149, partition `{"T001": 149}`, every file hash — is byte-identical to what evidencing `98a5c352` would have produced; only the metadata fields `head_commit` and `commit_count` differ, and both are recorded correctly for the commit the package actually names. `REVIEW_SUBJECT_ALIGNMENT` reads PASS and `EVIDENCE_AUTHORITATIVE` reads true for `102950eb`, independently reproduced.

ALTERNATIVE. Discard the built package and re-run SPEC E and SPEC Z against `98a5c352` in a repair round, rejected because it would spend a second full evidence-job run and a second ~25 MB zip build to change two metadata fields with no effect on the packaged content or its correctness, against a package that already, honestly, evidences exactly the commit it names.

CONSEQUENCE. Closure round B's STATUS `[x]` line for F280 names `accepted HEAD 102950ebadc06649aff95edee98c5438303211d0`. R-0952 is Done in this same commit. HOW TO REVERSE: re-run SPEC E and SPEC Z of round 24's block against `98a5c352bb9cf06d3e6484284b4f0df82b9ed6c8`, replace the package and its manifest, and correct the STATUS line's accepted HEAD before the closure commit lands.
END DECISIOND11

