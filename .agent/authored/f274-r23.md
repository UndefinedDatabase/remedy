STEP — F274 ROUND 23 — CLOSURE ROUND B: resolve R-0837, register R-0839, flip the STATUS line and open the pull request

Goal: close F274. This is the LAST ROUND OF THIS BRANCH. Its ledger commit books round 22's PASS
verdict, writes the authored `Done: R-0837` and registers R-0839; its closure commit then applies
the STATUS `[x]` line, the README capability sync and the one `consumed_by` edit in ONE commit, as
docs/roadmap/STATUS_closure_protocol.md's Rule A4 requires; then the pull request is opened and NOT
merged.

Base commit for every reading in this block: `a9ca53da`.

WHAT THE REVIEWER DID BEFORE AUTHORING, because a closure commit is the one commit that cannot be
followed by a repair. The STATUS line, both README edits and the `consumed_by` edit below were
APPLIED IN A DISPOSABLE WORKTREE at `a9ca53da` and `python3 -B -m pytest tests/docs/ -q
-p no:randomly` was run against the result: EXIT 0, 303 passed. The docs gate that these very edits
must satisfy runs AFTER the last permitted commit, so pre-verifying it is the only way the round is
safe; that reading is why the counters below are 76 and 19 rather than a guess. The self-use suites
were run against the same worktree as well: exit 0, 93 passed.

THE CLOSURE VALUES, all of them measured by round 22 and re-verified by the reviewer against the
bundle on disk rather than against the handback:

    Evidence job   a19161d4ff0df836
    package        remedy-review-20260908-083448-READY_FOR_REVIEW.zip
    SHA-256        a96911ffe68f7ab371bd23a5ebcb8f3844f9934c6ec1a3f87c7f0dfe1ded8103
    package path   /home/decodeux/Repos/remedy-history/zips
    accepted HEAD  5d329d2009108073dd91546ab9da0dc30cef73c7

The bundle's own `review_subject.json` records base `13dfaabd93d7b6452a1d23ca698e29ed47ecf035` and
head `5d329d20`, so the package covers exactly that accepted head, and the reviewer re-measured the
ancestry equality the closure protocol's pitfall (e) demands: 174 against 174.

THE OPEN SET DOES NOT MOVE THIS ROUND, and that is arithmetic rather than luck: R-0839 is
registered and R-0837 is resolved, so 65 stays 65. FOUR HIGH FINDINGS REMAIN OPEN — R-0803, R-0804,
R-0806 and R-0807, every one of them F273's rather than this feature's, per DECISION F272 D12 —
which is why the close is PASS_WITH_RISKS and why DECISION F272 D17 requires this round to name
them rather than rest on the integrity gate, whose `high_blockers_open` check says "no open
blocker/high findings" and is wrong about it (finding R-0648).

ONE GATE-SHAPED TRAP, DEFUSED HERE SO NOBODY GATES IT WRONGLY: the STATUS23 slice contains the
token `HEAD` once, unquoted, because the closure protocol's own STATUS template ends with
`accepted HEAD <full sha>`. The zero-count that §3 item 20 requires applies to slices bound for the
APPEND-ONLY RECORD, and RECORD23 carries 0 of them. G3 counts it over RECORD23 only, and no gate
below counts it over STATUS23.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`. THE SLICE IS THE BYTES STRICTLY BETWEEN THOSE TWO LINES — the
BEGIN line's own terminating newline belongs to the BEGIN line, and the slice's final byte is the
newline immediately preceding the END line. Marker lines never reach any file. No line of this
block's FRAME is a run of a single repeated character.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r23.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN23 slice.
C2   THE LEDGER: append the RECORD23 slice to `.agent/live_review.md` — three paragraphs, round
     22's PASS verdict, the `Done: R-0837` resolution and the R-0839 registration — and append the
     SLIPS23 slice to `.agent/prose_slips.md`.
C3   THE CLOSURE COMMIT, and the LAST commit on this branch: the STATUS `[x]` line, both README
     edits, the one `consumed_by` edit and the `.agent/handoff.md` rewrite, ALL IN ONE COMMIT.
     Then, with nothing further committed: the gates below, and the pull request.

There is no C4. Rule A4 makes the STATUS edit the last commit, and the closure protocol puts the
final `.agent/` state — the handoff rewrite included — inside it.


## Change — the exact set; nothing outside it is touched

    .agent/authored/f274-r23.md      (new, C0a)
    .agent/last_block.md             (rewrite, C0b)
    .agent/plan.md                   (rewrite, C1)
    .agent/live_review.md            (append, C2)
    .agent/prose_slips.md            (append, C2)
    docs/roadmap/STATUS.md           (C3)
    README.md                        (C3)
    scripts/self_use_queue.json      (C3)
    .agent/handoff.md                (rewrite, C3)

Nothing under `packages/`, `apps/`, `tests/` or `docs/` other than `docs/roadmap/STATUS.md` is
edited. No file is created or deleted beyond `.agent/authored/f274-r23.md`.

THE FIVE PAIRS OF C3. Each FROM occurs EXACTLY ONCE in its target at `a9ca53da`, which the reviewer
measured, and for each the containment test printed `TO contains FROM: false`, so ALL FIVE ARE
REWRITES and none is an append — apply each by replacing its single occurrence.

  P1  `docs/roadmap/STATUS.md`. FROM is the single line
      `- [~] F274 — One world completion, part two — the atomic record flip and the cluster deletion`
      with its terminating newline. TO is the STATUS23 slice.
  P2  `README.md`. FROM is the twelve-byte-boundary anchor beginning `feature the STATUS ledger
      registers directly after it).` and running through the blank line to the line `Accepted in
      Tier 3 so far:` INCLUDING that line's terminating newline. TO is the README23 slice, which
      restates that anchor with `it),` in place of `it).`, inserts the F274 paragraph, and ends
      with the same `Accepted in Tier 3 so far:` line and its newline.
  P3  `README.md`. FROM `75 of 275 registered items accepted.` TO `76 of 275 registered items
      accepted.`
  P4  `README.md`. FROM `| 2 | Minimal Self-Build Runtime | 18 | 28 |` TO
      `| 2 | Minimal Self-Build Runtime | 19 | 28 |`
  P5  `scripts/self_use_queue.json`. FROM `"consumed_by": ""` TO `"consumed_by": "F274"`. That FROM
      occurs exactly once in the whole file, because `SU-013` is the only unconsumed entry. Edit it
      as TEXT, never by loading and re-dumping the JSON: `json.dump` at its default `ensure_ascii`
      would escape every em dash in content this round never touched, which is finding R-0785.
      Upper-case `F274` is deliberate — all twelve consumed entries use the `F###` form.


## Constraints

1.  Apply every slice and every pair BYTE FOR BYTE. If something looks wrong, apply it anyway and
    say so in the handback under deviations.
2.  The change set above is exhaustive.
3.  ONE worker, this round only. Follow AGENTS.md in full.
4.  NEVER work on `main`, never force-push, never rewrite history, and delete no branch.
5.  C3 is the LAST COMMIT on this branch. Nothing is committed after it — not a fix, not a
    correction, not a state file. If a gate below fails AFTER C3, do NOT commit a repair: stop,
    report it in full in your completion message, and leave the branch as it stands. A repair after
    the closure commit is a new round's work and the next session's decision.
6.  The primary checkout satisfies `git status --porcelain` == EMPTY at the end of every commit.
7.  Report every gate's REAL exit code and REAL output. "Green" as a word is a finding.
8.  DO NOT MERGE THE PULL REQUEST, and do not enable auto-merge. It merges at the next feature's
    start through the Open PR Gate; that gap is the operator's manual-review window.
9.  Do NOT delete anything by glob, and do NOT delete or move the review package.
10. Do not touch `.agent/candidates.md`. It is EMPTY and this closure raises no candidate; if a
    gate below makes you believe one exists, report it in your completion message instead.


## Done when — eight gates, each RUN and each REPORTED with its real output

G1  TRANSPORT, at C0b. `sha256sum` of `.remedy-wt/f274-r23-FINAL.md`, of the committed
    `.agent/authored/f274-r23.md`, and of the committed `.agent/last_block.md`. Report all three
    digests and byte counts; the three must be EQUAL. The chain proved is scratch-original to saved
    copy to mirror, and nothing is claimed about the emitted bytes, per §3 item 37.

G2  THE PLAN, at C1. Report `wc -c` and `wc -l` of `.agent/plan.md`; it must be byte-identical to
    the PLAN23 slice at 2602 bytes and 43 lines, under the AGENTS.md cap of 50, with `## Goal` and
    `## Next Steps` each occurring once.

G3  THE APPENDS, at C2, with full byte forensics because it is the record. (a) BYTES: the reviewer
    measured `.agent/live_review.md` at 496375 before at `a9ca53da` and the RECORD23 slice at 9942
    bytes, so after must be 506317. (b) EXACT APPEND: pre-commit blob a byte-exact PREFIX, slice an
    exact SUFFIX — report both booleans. (c) ORDERED EQUALITY by an independent reader: split the
    post-commit file on blank lines, COUNT the slice's paragraphs into N rather than taking N from
    this block, compare the file's LAST N units against the slice's N paragraphs IN ORDER; report N
    and the boolean. (d) NEGATIVE CONTROL on the FIRST appended paragraph: flip one byte inside it,
    in scratch and never in the tracked file, and report that BOTH readers REJECT it. (e) COUNTS
    over the post-commit file: blank-line units 209 to 212; `^Gate: ` 21 to 22; `^Gate: F274 R22 `
    0 to 1; `^Done: R-0837 ` 0 to 1; `^- R-0839 ` 0 to 1; distinct `^- R-\d+ — ` ids 67 to 68;
    distinct `^Done: R-\d+ — ` ids 2 to 3; and the OPEN SET BY DISTINCT ID 65 to 65 — one
    registered and one resolved, so the total does not move. (f) THE SLIPS:
    `.agent/prose_slips.md` an exact append of SLIPS23, 165972 to 166737 bytes, gaining exactly two
    units. (g) unquoted `\bHEAD\b` in the RECORD23 slice, backtick-quoted spans deleted first,
    must be 0. Do NOT run that count over STATUS23; the block explains why above.

G4  THE CLOSURE COMMIT'S SHAPE, at C3. Report `git show --numstat C3`: its path set must be exactly
    `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md` —
    four paths, no more — and its insertions must be at most 500. Report that C3 is the branch tip
    and that `git log --format=%p C3` shows a single parent. For EACH of the five pairs report,
    counted over THAT COMMIT'S ADDED AND REMOVED LINES rather than over the whole file, that the
    FROM occurs 0 times in the post-commit target and the TO occurs exactly once — the proof shape
    §4 item 9 prescribes for a REWRITE, which the containment test above showed all five to be.

G5  THE AUTHORED TEXT LANDED BYTE-IDENTICALLY, at C3 — the grep proof the closure protocol requires
    of every piece of reviewer-authored applied text. (a) Extract the STATUS line from the
    committed `docs/roadmap/STATUS.md` and report that it is BYTE-IDENTICAL to the STATUS23 slice,
    by sha256 of both. (b) Report that the committed `README.md` contains the README23 slice
    verbatim, and that `docs/roadmap/STATUS.md` and `README.md` AGREE: the count of `^- \[x\] `
    lines in STATUS.md and the number in `<n> of 275 registered items accepted.` must be the SAME
    number, which is the ledger cross-check pin R-0154 exists for. (c) Read the queue back THROUGH
    THE SHIPPED LOADER rather than from the JSON: report `packages.orchestration.self_use_queue`'s
    `next_self_use_item()`, which must now be `None`, and `pending_self_use_items()`, which must
    now be 0, and report `SU-013`'s `consumed_by`, which must be exactly `F274`. Report also that
    the file still contains no `\u2014` escape introduced by this round.

G6  THE DOCS GATE AND THE CANARY, at C3, in the primary checkout, run SERIALLY — this is the tier-5
    docs-round gate, and it runs AFTER the closure commit because that commit is the one carrying
    the ledger edits it checks:
        python3 -B -m pytest tests/docs/ -q -p no:randomly
        python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    Report both exit codes and both counts lines. The reviewer measured 303 against the applied
    closure edit in a worktree, and 42 for the canary at `a9ca53da`. If either is red, constraint 5
    binds: report it, commit nothing.

G7  THE CLOSING STATE, at C3. Report, over the committed ledger: the open set BY DISTINCT ID, which
    must be 65; the ids of every OPEN finding whose severity token is `High`, which must be exactly
    R-0803, R-0804, R-0806 and R-0807 — R-0837 having just been resolved — derived by anchoring the
    severity to the FIRST token after the em dash rather than by searching the word `High` anywhere
    in the paragraph, which over-counts. Then `packages.orchestration.integrity_gate.
    run_integrity_checks()`: report `.passed` and `.fail_count`, which are ATTRIBUTES, and the
    `name`, `status` and `message` of its `high_blockers_open` check VERBATIM beside your own list,
    because DECISION F272 D17 requires the close to record that the check disagrees with the truth.

G8  THE PULL REQUEST AND THE TREE. `git status --porcelain` EMPTY, branch pushed and in sync. Then
    `gh pr create` against `main` from this branch, NOT a draft. The description carries: what
    changed and why; the key decisions, naming DECISION F274 D8 as the split ruling and DECISION
    F272 D17 as the ruling that lets a close carry open High findings; how to review, naming the
    package by filename and SHA-256 and its absolute directory; the changed-files table; the latest
    verdict, PASS_WITH_RISKS; the open-findings count of 65 with the four open High ids named; and
    the runtime actuals — 23 rounds across 8 sessions, the self-use run on provider `ollama` with
    model `muse-glimmer:latest`, and `not-measured` for tokens and cost, which beats a guess.
    Report the PR NUMBER and its URL. DO NOT MERGE IT. Then report `git worktree list | wc -l` and
    `git ls-files .remedy-wt`, which must be empty.


## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md, inside C3. It has NO length cap.
It carries the feature and round; SESSION 8 of F274; the branch; the commit SHAs; the changed-files
table with real `git diff --numstat` columns; the open-findings count with the four open High ids
named; the item-status table with every ordered item exactly once; the deviations; and the five
closure values above. Two of its lines cannot exist when it is written and it must say so rather
than guess: C3's own numstat and the PR number are reported in your completion message instead,
which is where §3 item 14 puts a value the writing commit cannot know. Its state block repeats this
line verbatim:

BEGIN FORTSCHRITT sha256=f777a357fd4cdcfa621c26f109381df20dcc2d08ecb48731b6002dba509e6281 bytes=292
Fortschritt: F274 ABGESCHLOSSEN und als [x] gebucht — Paket READY_FOR_REVIEW, PR offen und NICHT gemergt (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · F275 ✅ · Gate ✅ · Self-Use ✅ · R-0837 ✅ · Paket ✅ · STATUS ✅ · Merge = nächste Sitzung) — Schätzung
END FORTSCHRITT


Then push. Open the pull request. Do NOT merge it.

BEGIN PLAN23 sha256=6b710f34d0c7d3ac2b1d570e2d55ae2a2a50637e0e9b798049785cc54ea644d4 bytes=2602
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8. Everything the closure protocol asks for
is now on disk: F275 registered, the integration gate PASSED, the self-use item run, R-0837 fixed
at both sites, and a package that reaches READY_FOR_REVIEW.

## Current Step

CLOSURE ROUND B, the last round of this branch. Its ledger commit books round 22's PASS verdict,
writes the authored `Done: R-0837` — whose condition needed a package that actually reached
READY_FOR_REVIEW, which round 22 produced — and registers R-0839. Its closure commit then applies
the STATUS `[x]` line, the README capability sync and the one `consumed_by` edit in ONE commit, per
the closure protocol's Rule A4, after which the pull request is opened. THE PULL REQUEST IS NOT
MERGED in this session: it merges at the next feature's start through the Open PR Gate, and that
gap is the operator's manual-review window.

## Next Steps

1. The next session opens at Phase 1 rule 1 of `docs/agents/self_drive_protocol.md` — read
   `.agent/STOP` from disk — and then rule 2 finds this feature's pull request open and MERGES it
   before any new branch is cut. That merge is the next session's first action, not this one's.
2. F275 is registered and placed directly after F274 inside the same tier heading, so Rule A5
   proposes it first once the Open PR Gate has merged this branch. It inherits a bounded,
   machine-checked work list and seven dated rulings rather than a fresh investigation.

## Risks

- The open findings stand at 65 by distinct id, of which four are High — R-0803, R-0804, R-0806 and
  R-0807, all F273's rather than this feature's, per DECISION F272 D12. The integrity gate's
  `high_blockers_open` check reports "no open blocker/high findings" and is WRONG about them; that
  is R-0648, and DECISION F272 D17 requires this close to say so and to rest on the named list.
  This is why the close is PASS_WITH_RISKS and not PASS.
- The closure commit is the LAST commit on the branch (Rule A4). The docs gate that its own STATUS
  and README edits must satisfy therefore runs AFTER it; the reviewer pre-verified that edit in a
  disposable worktree and `tests/docs/` returned 303 passed against it before the round was
  authored.
END PLAN23

BEGIN RECORD23 sha256=baccf49171e9d9e926845556a55f8c37da18b000351c4c1b886a0432b71e540c bytes=9942

Gate: F274 R22 — the F274 round 22 entry, CLOSURE ROUND A. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs, in the primary checkout, at `a9ca53da`. RANGE `6b5387ae`..`a9ca53da`, six commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4. G1 TRANSPORT: the scratch original and both committed copies are all 24470 bytes at `30bb0397abbe8ebc057aacb126cffecf731f1f7abf6a277ee469c48bc63bb616`. G2 THE PLAN at `2bcbc711`: byte-equal to its slice at 3043 bytes and 49 lines against the cap of 50. G3 THE RECORD APPEND at `31073828`: 658562 to 663083 bytes, prefix and suffix both exact, N counted as 1, ordered equality true, the negative control on the appended paragraph rejected by BOTH readers; units 252 to 253, `^Gate: ` 52 to 53, `^Gate: F274 R21 ` 0 to 1, registrations 72 to 72, distinct resolutions 7 to 7, OPEN SET 65 TO 65 BY DISTINCT ID. G4 THE ROTATION at `5d329d20`, run by the script and never by hand: 32 gate records and 5 finding pairs moved, the ledger 663083 to 496375 bytes and the archive 2535031 to 2701739, 88 insertions against 88 deletions and therefore NO oversize exception spent, the archive's pre-rotation bytes a byte-exact PREFIX of its post-rotation bytes, and the path set exactly the two files. THE OPEN SET SURVIVED THE ROTATION UNCHANGED at 65 by distinct id — 67 registrations against 2 resolutions where it had been 72 against 7 — and `R-0837` and `R-0784` are both still present as OPEN registrations, which is the property that matters, because a rotation that archived an open finding would silently shrink the work. G5 THE EVIDENCE JOB: the base is the FORK POINT `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, and the reviewer re-measured the equality the closure protocol's pitfall (e) demands — `rev-list --ancestry-path` 174 against plain `rev-list` 174, EQUAL — with the base an ancestor of `origin/main`; the bundle's own `review_subject.json` records that base and the head `5d329d20`, so the package covers exactly the accepted head; the verification record carries 303 node ids from a real `--collect-only` against 303 passed, its two `test_files` are real files rather than a directory, and `_unsafe_text` flagged none of the 305 strings; the producer returned job `a19161d4ff0df836`, `verdict PASS_WITH_RISKS`, `authority_count 60`, `commit_count 174` and a three-way partition of 20, 20 and 20. G6 THE REVIEW ZIP: `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`, 4135 members, `authoritative_count 60`, and the script's printed SHA-256 agreeing with the worker's recomputation from the file on disk. G7 THE PRECONDITIONS: `tests/docs/` exit 0 at 303 passed and `tests/cli/test_golden_path.py` exit 0 at 42 passed, both re-run by the reviewer; `run_integrity_checks()` returning `.passed` True and `.fail_count` 0 as ATTRIBUTES; and its `high_blockers_open` check reporting `IntegrityStatus.PASS` with the message `no open blocker/high findings`, WHICH IS FALSE, as R-0648 records and DECISION F272 D17 requires this close to say out loud. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, the range path set exactly the five tracked paths, and per-commit insertions 290, 223, 26, 2 and 88, every one under the cap of 500. SEVEN DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL SEVEN; two need the record. FIRST, THE WORKER REMOVED THIRTEEN PRE-EXISTING WORKTREES, taking the count from 14 to 1, reading this round's constraint 6 — prune every disposable worktree before the evidence job — as reaching the `remedy/job-*` checkouts left behind by earlier features. That reading is within the constraint's words and the reviewer sustains it, having VERIFIED the consequence rather than accepted the claim: all fifteen `remedy/job-*` BRANCHES still exist, so no commit and no branch was lost, and what went was uncommitted scratch inside disposable checkouts that their own rounds should have removed. The constraint meant the worktrees THIS round created, and that imprecision is the reviewer's; it is appended to `.agent/prose_slips.md` by this same commit. SECOND, THE WORKER REPORTED A DISAGREEMENT IT WAS NOT ASKED ABOUT AND WAS RIGHT TO: the package's tombstone reading is not uniform across its own documents. The reviewer measured the bundle itself rather than taking the report — `current_change_content_proof.json` carries `tombstone_count` 0 with an EMPTY `tombstones` map and no entry for the deleted path, while `review_subject.json` carries that path with its `base_sha256` set and `current_sha256` null, and the packaging summary reports `tombstone_count` 1. That is a real defect and it is registered below as R-0839, on the reviewer's own measurement and not on the worker's report.

Done: R-0837 — RESOLVED in F274 rounds 20 and 21, and confirmed by the closure package round 22 built. The finding's resolution condition had TWO clauses and both are now met, which is stated here because the second clause is the only reason this finding was not closed a round early. CLAUSE ONE, the guard with a regression test that goes red without it, at BOTH sites: `packages/orchestration/job_evidence.py` at `cacd42af`, where the attestation authority set gained the conjunct `and f.current_sha256`, and `scripts/build_review_zip.py` at `45c17555`, where `_assert_authority_equality`'s independent recomputation gained the same conjunct. Each shipped its own regression test and each was proved by MUTATION IN A DISPOSABLE WORKTREE, RE-RUN BY THE REVIEWER ITSELF: for the producer the control exited 0 and the mutant exited 1 with `ValueError: T002: safe-diff path set does not match the task partition`; for the coordinator the control exited 0 at 2 passed and the mutant exited 1 at EXACTLY 1 failed and 1 passed, the failing test being the regression and the PASSING one the discriminator that proves the mutation repaired a guard rather than deleted a check. CLAUSE TWO, that ONE CLOSURE PACKAGE BUILDS READY_FOR_REVIEW FROM A BRANCH THAT DELETES A SOURCE FILE: round 22 built it. This branch deletes `apps/cli/commands/feature_cmd.py`, and the package `remedy-review-20260908-083448-READY_FOR_REVIEW.zip` covers head `5d329d20` with `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS` and `EVIDENCE_AUTHORITATIVE=true`. WHY THAT SECOND CLAUSE EARNED ITS KEEP, recorded because the lesson is the point: after round 20 the producer succeeded and the reviewer called the closure unblocked, and the zip still refused the branch — the closure is a TWO-STEP algorithm and only step 1 had been run. A resolution condition written as an OBSERVABLE END STATE rather than as a list of edits is what caught that, and it cost one round instead of a failed close. What this finding does NOT claim is that a deleted path is fully attested everywhere in the package: it is attested by `review_subject.json`'s `base_sha256` and counted by the packaging summary, while the content proof carries no tombstone at all — that residue is R-0839 below, registered rather than folded in here, because it is a different defect with a different fix.

- R-0839 — Medium, THE CLOSURE BUNDLE'S CONTENT PROOF CARRIES NO TOMBSTONE FOR A DELETED PATH, SO THE ONE DOCUMENT THE PACKAGER CALLS THE AUTHORITY SOURCE CANNOT TELL 'DELETED' FROM 'NEVER IN SCOPE', AND THREE DOCUMENTS IN ONE PACKAGE DISAGREE ABOUT WHETHER A TOMBSTONE EXISTS. Offered unprompted by the WORKER of round 22 as an observation it was not asked for, and MEASURED INDEPENDENTLY BY THE REVIEWER against the round 22 bundle itself rather than taken from that report. §3 item 30 was performed FIRST: the open set was searched for `tombstone`, `current_change_content_proof` and `content proof`, and no open registration holds this defect, so the id is not a duplicate. MEASURED, in the bundle for job `a19161d4ff0df836` at head `5d329d20`, whose branch deletes `apps/cli/commands/feature_cmd.py`: `current_change_content_proof.json` reports `file_count` 60, `tombstone_count` 0 and an EMPTY `tombstones` map, and the deleted path is absent from its `file_hashes`; `review_subject.json` DOES carry that path, with `base_sha256` set and `current_sha256` null; and the packaging summary reports `tombstone_count` 1, computed downstream from the review subject. THE MECHANISM: `create_manual_completion_bundle` writes `"tombstones": {}` and `"tombstone_count": 0` as LITERAL CONSTANTS, so no run of the producer can ever emit a tombstone, although `ContentProofV1.authority_paths()` is the union of files AND tombstones and `ReviewFileV1.base_sha256` exists precisely to hold one. WHY THIS MATTERS RATHER THAN BEING TIDINESS: `tests/orchestration/test_review_subject_deletions.py`'s own module docstring names this exact failure — "No entry is indistinguishable from never looked, and a removed file is emphatically part of a change" — and the tombstone machinery was built in answer to it, so the producer is defeating a guarantee the repository already implemented and tests. WHY MEDIUM AND NOT HIGH: the deletion is not lost, because `review_subject.json` carries it and the packaging summary counts it, so no package is wrong about WHAT changed and none of this blocked the F274 close; and why not Low, because F275 is a deletion feature by construction and every package it produces will under-attest its central act. WHY IT IS NOT FOLDED INTO R-0837: that finding is that a deletion feature cannot be packaged AT ALL, and it is resolved; this one is that a deletion feature packages successfully while under-attesting, and its fix is to emit the tombstones the schema already accepts rather than to guard a comprehension. Resolved when the producer emits a tombstone for every deleted attestable path, with a test asserting that the content proof's tombstone set equals the deleted set and that `ContentProofV1.authority_paths()` therefore covers the deleted path.
END RECORD23

BEGIN SLIPS23 sha256=76b9fbc5e526a7a02a90098750e6fa3690655cef8dbd3f19f1895b54b5be2b75 bytes=765

2026-09-08 · F274 R22 · The round 22 block's constraint 6 said to prune every disposable worktree before the evidence job, meaning the ones that round created, and the worker reasonably read it as reaching the thirteen pre-existing `remedy/job-*` checkouts and removed them, taking the worktree count from 14 to 1; all fifteen `remedy/job-*` branches survive, so nothing committed was lost and only uncommitted scratch went.

2026-09-08 · F274 R22 · The PLAN22 slice said the closure commit sets `SU-013`'s `consumed_by` to `f274` in lower case, while every one of the twelve consumed entries in `scripts/self_use_queue.json` uses the upper-case `F###` form; the closure commit uses `F274`, which is the one spelling AGENTS.md's discoverability rule asks for.
END SLIPS23

BEGIN STATUS23 sha256=52f63c6000d1217312cfc04e301c36be71caa25fa9b9aedf9a9789aed92b8a2e bytes=597
- [x] F274 — One world completion, part two — the atomic record flip and the cluster deletion (the generated cluster-deletion map, the import-reachability ratchet and the cockpit and command-layer edge cuts complete; T001-T003 moved to F275; accepted 2026-09-08 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job a19161d4ff0df836 · package remedy-review-20260908-083448-READY_FOR_REVIEW.zip · SHA-256 a96911ffe68f7ab371bd23a5ebcb8f3844f9934c6ec1a3f87c7f0dfe1ded8103 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 5d329d2009108073dd91546ab9da0dc30cef73c7)
END STATUS23

BEGIN README23 sha256=ecdc0427f2d9e7dfda1c9afc7856f9185f3252b9c5aad4c0923ff61cecd02564 bytes=852
feature the STATUS ledger registers directly after it),
F274 one world completion, part two (the prototype-cluster deletion map,
GENERATED from the live import graph rather than typed and held against it
in BOTH directions, so a re-inserted edge reddens a test instead of passing
unnoticed; the import-reachability ratchet, ruled a ratchet rather than a
one-shot gate; the cockpit and command-layer edge cuts, with `ui_server.py`
losing 458 lines and gaining none and the `feature` command group deleted
whole; and the retirement of `worker_recommend`. Nothing was deleted from
the prototype cluster here, only made SAFE to delete: that deletion, the
atomic record flip and the classic runner were split off at the
eight-session soft limit and belong to the follow-up feature the STATUS
ledger registers directly after it).

Accepted in Tier 3 so far:
END README23
