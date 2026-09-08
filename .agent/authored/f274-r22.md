STEP — F274 ROUND 22 — CLOSURE ROUND A: book round 21, rotate the ledger, and build the evidence job and the review zip

Goal: produce the two artifacts F274's closure cannot happen without — a feature-scoped evidence
bundle and a FRESH review zip that reaches `PACKAGE_STATUS=READY_FOR_REVIEW` — with the mandated
ledger rotation as its own commit in between. This is a CLOSURE-SEQUENCE round, which
docs/agents/self_drive_protocol.md names as the one exception to the ban on bookkeeping rounds, so
its first commits are verdict bookings by design and not by drift.

Base commit for every reading in this block: `6b5387ae`.

THE REVIEWER DRY-RAN THIS ENTIRE SEQUENCE BEFORE AUTHORING IT, in a disposable worktree, at the
post-rotation head — not the producer alone, which is the mistake round 20 made and round 21 paid
for. Rotating the ledger, building the bundle and running `make_review_zip.sh` end to end gave:
`PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`,
`tombstone_count 1`, and a producer verdict of `PASS_WITH_RISKS`. THE COUNTS THAT DRY RUN PRODUCED
ARE NOT GATED BELOW and no done-when asserts one, because this round's own commits change the
commit chain and the working tree that the authority set is read from; what IS gated is every
value that must hold whatever the counts turn out to be.

THE ROTATION, MEASURED AFTER THIS ROUND'S OWN LEDGER APPEND rather than before it. The reviewer
simulated `scripts/rotate_live_review.py` against a scratch copy of the post-C2 ledger: 32 gate
records and 5 finding pairs move, the ledger goes 663083 to 496375 bytes and the archive 2535031 to
2701739, and the commit is 88 insertions against 88 deletions. THAT IS UNDER THE CAP, so this
rotation needs NO oversize exception: DECISION F272 D18 reserves a feature's one allowance for a
rotation on the ground that a rotation cannot be split, and F272's own was 1612 insertions, but
F274's is 88 because a ledger record is one long line. The reviewer measured rather than inherited
the figure.

ONE READING THAT LOOKS LIKE A CONTRADICTION AND IS NOT, so that no one spends a round on it. The
rotation script prints `open findings before: 63` and `open findings after: 63`, while the record's
own distinct-id reading — every `^- R-\d+ — ` id minus every `^Done: R-\d+ — ` id — is 65 both
before and after. The two counters have differed by exactly 2 for several features, and the
property the gate needs from either is that it is IDENTICAL ACROSS THE ROTATION, which both are.
Report both; do not reconcile them, and do not open anything about it.

FIVE HIGH FINDINGS ARE OPEN AT THIS BASE, and the reviewer names them rather than leaving the
integrity gate to be believed: R-0803, R-0804, R-0806 and R-0807, all of them F273's rather than
this feature's per DECISION F272 D12, plus R-0837, which is FIXED at both sites but NOT YET
RESOLVED because only reviewer-authored `Done:` text resolves anything. R-0837's own resolution
condition demands a closure package that reaches READY_FOR_REVIEW, which only THIS round can make
true, so its `Done:` paragraph is authored in closure round B and this round deliberately writes
none. §3 item 31 is the reason: an authored text may state a gate's result only when that gate ran
at a strictly earlier commit.

FRAME CONVENTION. Every slice is delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>`
and a line reading `END <NAME>`. THE SLICE IS THE BYTES STRICTLY BETWEEN THOSE TWO LINES — the
BEGIN line's own terminating newline belongs to the BEGIN line, and the slice's final byte is the
newline immediately preceding the END line. Marker lines never reach any file. No line of this
block's FRAME is a run of a single repeated character.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r22.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN22 slice.
C2   Append the RECORD22 slice to `.agent/live_review.md` — one paragraph, round 21's PASS verdict.
C3   THE LEDGER ROTATION, its OWN commit, touching `.agent/live_review.md` and
     `.agent/live_review_archive.md` and nothing else.
     Then, with NOTHING further committed: the evidence job (G5) and the review zip (G6). Neither
     writes a tracked file; the evidence directory is NEVER committed.
C4   Rewrite `.agent/handoff.md` and hand back.

C3 IS THE ACCEPTED HEAD. The package covers it, closure round B's STATUS line will name it, and C4
is the handback that reports what the package said — which is why nothing between them may commit
a tracked file.


## Change — the exact set; nothing outside it is touched

    .agent/authored/f274-r22.md          (new, C0a)
    .agent/last_block.md                 (rewrite, C0b)
    .agent/plan.md                       (rewrite, C1)
    .agent/live_review.md                (append at C2, rotated at C3)
    .agent/live_review_archive.md        (append by the rotation script, C3)
    .agent/handoff.md                    (rewrite, C4)

NO file under `docs/`, `packages/`, `apps/`, `tests/` or `scripts/` is edited this round. In
particular `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` are NOT touched
here — all three belong to closure round B's single closure commit.


## Constraints

1.  Apply every slice BYTE FOR BYTE. If a slice looks wrong, apply it anyway and say so in the
    handback under deviations.
2.  The change set above is exhaustive for TRACKED files. The evidence directory and the review
    package are untracked artifacts and are covered by G5 and G6 instead.
3.  ONE worker, this round only. Follow AGENTS.md in full.
4.  NEVER work on `main`, never force-push, never rewrite history, and delete no branch.
5.  The rotation is run by the SCRIPT and never by hand: `python3 -B scripts/rotate_live_review.py`
    with no path arguments, from the primary checkout. It verifies each moved record's sha256
    before and after and REFUSES on any mismatch; if it refuses, STOP and report its stderr
    verbatim. Do not edit either file yourself.
6.  The primary checkout satisfies `git status --porcelain` == EMPTY at the end of every commit,
    and — this is the one that decides whether the package is valid — it is EMPTY at the moment the
    evidence job and the zip are run. The authority set is read from the WORKING TREE, so an
    untracked file under the repository root joins it. Put the evidence directory under the
    gitignored `.remedy-wt/`, and prune every disposable worktree before G5.
7.  If ANY gate below comes back red, STOP: commit what is honestly finished, write the handback
    with the raw output, and hand back. A failing zip is a CLOSURE BLOCKER, never something to work
    around.
8.  Report every gate's REAL exit code and REAL output. "Green" as a word is a finding.
9.  Do NOT flip the STATUS line, do NOT touch `README.md`, do NOT set any `consumed_by`, do NOT
    write a `Done:` paragraph and do NOT open a pull request. All of those are closure round B's.
10. Do NOT delete anything by glob. The evidence directory and any package are removed, if at all,
    by their exact absolute paths — and the package is NOT removed, because it is the operator's
    review window.


## Done when — eight gates, each RUN and each REPORTED with its real output

G1  TRANSPORT, at C0b. `sha256sum` of `.remedy-wt/f274-r22-FINAL.md`, of the committed
    `.agent/authored/f274-r22.md`, and of the committed `.agent/last_block.md`. Report all three
    digests and byte counts; the three digests must be EQUAL. The chain proved is scratch-original
    to saved copy to mirror, and nothing is claimed about the emitted bytes, per §3 item 37.

G2  THE PLAN, at C1. Report `wc -c` and `wc -l` of `.agent/plan.md`; it must be byte-identical to
    the PLAN22 slice at 3043 bytes and 49 lines, which is under the AGENTS.md cap of 50. Report
    that `## Goal` and `## Next Steps` each occur in it.

G3  THE RECORD APPEND, at C2, with full byte forensics because it is the record. (a) BYTES: the
    reviewer measured 658562 before at `6b5387ae` and the RECORD22 slice at 4521 bytes, so after
    must be 663083. (b) EXACT APPEND: the pre-commit blob is a byte-exact PREFIX and the slice an
    exact SUFFIX — report both booleans. (c) ORDERED EQUALITY by an independent reader: split the
    post-commit file on blank lines, COUNT the slice's paragraphs into N rather than taking N from
    this block, and compare the file's LAST N units against the slice's N paragraphs IN ORDER;
    report N and the boolean. (d) NEGATIVE CONTROL on the FIRST appended paragraph: flip one byte
    inside it, in scratch and never in the tracked file, and report that BOTH readers REJECT it.
    (e) COUNTS over the post-commit file: blank-line units 252 to 253; `^Gate: ` 52 to 53;
    `^Gate: F274 R21 ` 0 to 1; distinct `^- R-\d+ — ` ids 72 to 72; distinct `^Done: R-\d+ — ` ids
    7 to 7; OPEN SET BY DISTINCT ID 65 to 65. (f) Report the count of unquoted `\bHEAD\b` in the
    RECORD22 slice with every backtick-quoted span deleted first; it must be 0.

G4  THE ROTATION, at C3. Report the script's FULL stdout. It must report 32 gate records moved and
    5 finding pairs, the ledger 663083 to 496375 bytes, the archive 2535031 to 2701739, and its own
    open-findings count IDENTICAL before and after. Then, independently of the script: report the
    record's own distinct-id open set over the post-rotation ledger, which must still be 65, and
    report that `R-0837` and `R-0784` are both still present as registrations — a rotation that
    archived an OPEN finding would be a defect and this is how it would show. Report
    `git show --numstat C3` for that commit; its path set must be exactly `.agent/live_review.md`
    and `.agent/live_review_archive.md`, and its insertions must be at most 500. Report that the
    archive's pre-rotation bytes are a byte-exact PREFIX of its post-rotation bytes, which is what
    "append-only" means here.

G5  THE EVIDENCE JOB, at C3, in the primary checkout. FIRST, THE BASE, and STOP if it fails: with
    base `13dfaabd93d7b6452a1d23ca698e29ed47ecf035` — the full 40-character FORK POINT, never
    abbreviated and never `git merge-base` — report the count of
    `git rev-list --ancestry-path <base>..<C3>`, the count of `git rev-list <base>..<C3>`, and the
    boolean THE TWO ARE EQUAL. If they differ, STOP: that inequality is what packaged F260's round
    22 as BLOCKED_EVIDENCE. Report also that the base is an ancestor of `origin/main`, and that
    `git status --porcelain` is EMPTY.
    THEN THE VERIFICATION RECORD, built from a REAL run at C3 of
    `python3 -B -m pytest tests/docs/ -q -p no:randomly` and a REAL `--collect-only` over the SAME
    selection. Node ids are every output line containing `::`. Build ONE entry with these fields
    and no others: `run_id` `vr-0001`, which matches `^vr-\d{4,}$`; `command`, the exact command
    string; `exit_code`; `passed`; `failed`; `skipped`; `deselected`; `selected` EQUAL to
    passed+failed+skipped; `node_ids`, whose LENGTH must EQUAL `selected` — the reviewer measured
    303 collected against 303 passed at `6b5387ae`; `test_files`, the actual FILE paths SORTED and
    never a directory, which resolve to `tests/docs/test_docs_consistency.py` and
    `tests/docs/test_vocabulary.py`; `stdout_summary`, the run's own stdout under 4000 characters;
    `output_hash`, the sha256 hex of EXACTLY that `stdout_summary` string; `head_sha`;
    `duration_seconds`. BEFORE calling the producer, pre-scan every node id and every test_file
    with `_unsafe_text` from `build_review_manifest`, which lives in `scripts/` and NOT under
    `packages.orchestration`, and report that it flags NONE of them.
    THEN CALL `packages.orchestration.job_evidence.create_manual_completion_bundle` with:
    `evidence_dir` a FRESH directory under the gitignored `.remedy-wt/`; `repo_root` the primary
    checkout; `base_commit` the fork point above; `head_commit` the full sha of C3; `job_id` 16
    lowercase hex characters from `secrets.token_hex(8)`; `job_title` `F274 one world completion
    part two closure evidence`; `step_range` `T001-T003`; `prior_job_ids` the empty list;
    `review_feature_id` `f274`; `timestamp` and `generated_at` ISO-8601 UTC.
    Report the returned summary dict IN FULL, the job id, and the verdict it names. Do NOT record a
    full-suite node-id list anywhere: `len(node_ids) == selected` forbids filtering, and the
    packaging metadata scan rejects the redaction-torture ids by design.

G6  THE REVIEW ZIP — closure algorithm step 2, MANDATORY and never skipped. `git status
    --porcelain` EMPTY first, and the branch pushed. Then
        bash scripts/make_review_zip.sh --evidence-dir <the directory from G5>
    Report: the FULL stdout; `PACKAGE_STATUS`, which MUST be `READY_FOR_REVIEW`;
    `REVIEW_SUBJECT_ALIGNMENT`, which must be `PASS`; `EVIDENCE_AUTHORITATIVE`, which must be
    `true`; the package FILENAME; its SHA-256 as the script printed it AND as you RECOMPUTE it from
    the file on disk, which must agree; the package's ABSOLUTE directory, which DECISION amend0827
    D1 requires recorded because it is the operator's review window; `member_count`,
    `authoritative_count` and `tombstone_count`, of which the last must be at least 1 because this
    branch deletes a source file and the tombstone is how that deletion is attested; and the
    manifest's `committed_review_subject` base and head, which must span the fork point to C3. If
    `PACKAGE_STATUS` is anything other than `READY_FOR_REVIEW`, report `validation_errors` VERBATIM
    and in full, then STOP per constraint 7. Do NOT delete the package.

G7  THE PRECONDITIONS, at C3, in the primary checkout, run SERIALLY:
        python3 -B -m pytest tests/docs/ -q -p no:randomly
        python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    The reviewer measured 303 and 42 at `6b5387ae`; report both exit codes and both counts lines.
    Then, in Python, `packages.orchestration.integrity_gate.run_integrity_checks()` — report
    `.passed` and `.fail_count`, which are ATTRIBUTES and never dict keys, and the reviewer
    measured True and 0. Then walk its `.checks` list and report the `name`, `status` and `message`
    of the check named `high_blockers_open` VERBATIM. The reviewer measured that check reporting
    `IntegrityStatus.PASS` with the message `no open blocker/high findings`, WHICH IS FALSE: five
    High findings are open — R-0803, R-0804, R-0806, R-0807 and R-0837. That is finding R-0648, and
    DECISION F272 D17 requires the close to say it out loud and to rest on the named list instead
    of on the check. Report the list you measure yourself beside the check's own message.

G8  THE TREE, readings taken at C3 and reported in the handback. `git status --porcelain` EMPTY;
    `git ls-files .remedy-wt` EMPTY; `git worktree list | wc -l`; the change set of
    `git diff --name-only 6b5387ae..C3`, which must be exactly the five tracked paths of the Change
    section other than `.agent/handoff.md`; and the INSERTION count of each of C0a, C0b, C1, C2 and
    C3 separately, each at most 500 per AGENTS.md DECISION F104 D1. C4's own numbers belong to the
    next round's ledger entry.


## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO length cap. Beyond its
mandated sections — feature and round, SESSION 8 of F274, branch, commit SHAs, changed-files table
with real `git diff --numstat` columns, one line per gate G1 through G8, open-findings count,
item-status table, deviations — it MUST carry, in one clearly headed block, the five values closure
round B's STATUS line is authored from, because the STATUS line is the durable carrier and this is
the only round that knows them:

    Evidence job   <job_id>
    package        <zip filename>
    SHA-256        <hash>
    package path   <absolute directory>
    accepted HEAD  <full 40-character sha of C3>

Its state block repeats this line verbatim:

BEGIN FORTSCHRITT sha256=ff2a85b8c433513bae3d9842a1c4905936493b66ff9031a47372d948e3828d17 bytes=303
Fortschritt: F274 im Abschluss — R-0837 an beiden Stellen behoben, Ledger rotiert, Evidenzjob und Review-Zip als READY_FOR_REVIEW gebaut (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · F275 ✅ · Gate ✅ · Self-Use ✅ · R-0837 ✅ · Paket ✅ · STATUS-Flip offen) — Schätzung
END FORTSCHRITT


Then push the branch. Do NOT open a pull request this round and do NOT merge anything.

BEGIN PLAN22 sha256=85fbbe0421ec6033ecef952538ffc7fbf46e4409139b691638f23751895f0594 bytes=3043
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8. F275 is registered, the integration gate
has PASSED, the self-use precondition is met, and R-0837 is fixed at BOTH sites, so the closure
package now builds.

## Current Step

CLOSURE ROUND A. It books round 21's PASS verdict, then rotates the ledger by
`scripts/rotate_live_review.py` as its own commit — the step operator amendment amend0905-throughput
places after the verdict bookings and before the STATUS flip — and then RUNS the closure evidence
job and the fresh review zip from a clean tree. The reviewer dry-ran this whole sequence at the
post-rotation head before authoring it: the producer returns `PASS_WITH_RISKS` and the package
builds `READY_FOR_REVIEW`. Nothing is committed after the zip except the handback, so the accepted
HEAD is the rotation commit.

## Next Steps

1. CLOSURE ROUND B, in two commits. FIRST the ledger: round 22's PASS verdict, and the authored
   `Done: R-0837` — its resolution condition requires a closure package that reaches
   READY_FOR_REVIEW, so it can only be written AFTER round A has built one. THEN the closure
   commit: the STATUS `[x]` line the reviewer authors from round A's measured values, the README
   capability sync and the one `consumed_by` edit setting `SU-013` to `f274`, all three in ONE
   commit per the closure protocol's Rule A4 ordering; then the pull request. The PR is NOT merged
   this session — it merges at the next feature's start through the Open PR Gate, which is the
   operator's manual-review window.
2. F275 is registered and placed directly after F274, so Rule A5 proposes it first in the next
   session, AFTER that Open PR Gate has merged this branch.

## Risks

- The package's `base_commit` is the FORK POINT `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose
  ancestry-path and plain `rev-list` counts the reviewer measured EQUAL. NEVER `git merge-base`,
  which names `origin/main`'s tip `d0d8b24d` here, gives unequal counts, and is the defect that
  packaged F260's round 22 as BLOCKED_EVIDENCE.
- The authority set is read from the WORKING TREE, and `pytest` has no `norecursedirs` here, so an
  untracked file or a leftover worktree changes what is packaged and what is collected. The tree is
  clean and the worktrees pruned before the evidence job.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12. The integrity gate's `high_blockers_open` check reports "no
  open blocker/high findings" and is WRONG while those four are open — that is R-0648, and
  DECISION F272 D17 requires the close to say so and to rest on the named list instead.
END PLAN22

BEGIN RECORD22 sha256=cb0d211052313b7ca1aaae2f9fe38f46a7f4f12d7cba72f288c8f8c70a6dc1c2 bytes=4521

Gate: F274 R21 — the F274 round 21 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the COMMITTED blobs, in the primary checkout, at `6b5387ae`. Booked by round 22's ledger commit out of `.agent/handoff.md`, which operator amendment amend0827-process-diet rule 1 makes a durable carrier. RANGE `630f22b9`..`6b5387ae`, six commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, branch pushed and in sync. G1 TRANSPORT: the scratch original `.remedy-wt/f274-r21-FINAL.md` and both committed copies are all 29142 bytes at `79d0ecbc1dc301d570e6c6ce31045c9db330c1a5f862ba3df0fac9f79bfce6ca`; the chain walked is scratch-original to saved copy to mirror, and nothing is claimed about the emitted bytes. G2 THE PLAN at `22c9042e`: byte-equal to its slice at 2869 bytes and 45 lines against the cap of 50. G3 THE APPENDS at `3bc758fc`: `.agent/live_review.md` 650874 to 658562 bytes, pre-commit blob an exact PREFIX and the slice an exact SUFFIX, N counted as 2 from the slice, ordered equality true, and the negative control on the FIRST appended paragraph at offset 650875 REJECTED by BOTH readers; units 250 to 252, `^Gate: ` 51 to 52, `^Gate: F274 R20 ` 0 to 1, `^SECOND SITE of R-0837 ` 0 to 1, registrations 72 to 72, distinct resolutions 7 to 7, OPEN SET 65 TO 65 BY DISTINCT ID — this round deliberately registered NOTHING, because §3 item 30 forbids a second id for a defect the set already holds; `.agent/prose_slips.md` 165189 to 165972 with exactly two units gained; unquoted `\bHEAD\b` in the RECORD21 slice 0. G4 THE GUARD at `45c17555`: numstat 2 insertions and 1 deletion, `attestable_subject = {f.path for f in subject.files` occurring once, `is_attestable_source(f.path)` once, and the guarded form `is_attestable_source(f.path) and f.current_sha256` once where it was zero; `ruff check` exit 0 over both changed files. G5 THE RED-PROOF, RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE: the module resolved inside that worktree rather than to the editable install, the revert target was unique, the UNMUTATED control exited 0 at 2 passed, and with the conjunct deleted the same module exited 1 at EXACTLY 1 failed and 1 passed — the failing test being the regression `test_a_deleted_path_does_not_block_the_package` and the PASSING one the discriminator, which is what proves the mutation repaired-versus-deleted distinction the gate was written for. G6 THE SCOPED SUITE: exit 0 at exactly 69 passed against the 67 the reviewer measured for the same selection without the new module. G7 THE FULL SUITE: exit 0 at 19770 passed and 23 skipped with an EMPTY failing list, and the reviewer's own independent run returned the identical figures — unlike round 20, where the two runs disagreed by one xdist flake. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, 14 worktrees, the range path set exactly the seven declared paths, per-commit insertions 295, 193, 19, 8 and 99 for C0a through C3, every one under the cap of 500, and no oversize commit declared. TEN DEVIATIONS WERE DECLARED AND THE REVIEWER SUSTAINS ALL TEN; one needs the record. THE WORKER AMENDED C3 ONCE, and it was RIGHT to. Its first G5(d) run returned 2 failed rather than the ordered 1 failed and 1 passed, because its own discriminator carried a third assertion about what the error message says of the DELETED path — an assertion that is itself guard-dependent and therefore goes red under the mutation, which is exactly the failure the two-sided count exists to catch. The worker diagnosed it as its own over-specification beyond what the block described, removed it, left a comment in the test saying why it must not be asserted there, and amended rather than adding a seventh commit. THE REVIEWER VERIFIED THAT NO PUBLISHED HISTORY WAS REWRITTEN rather than accepting the claim: the reflog shows `750e61e9` amended to `45c17555`, and `git branch -r --contains 750e61e9` returns EMPTY, so the discarded commit never reached the remote and protocol guardrail G2 — which forbids force-pushing and rewriting history — is untouched. An amend of an unpushed commit is not a rewrite of anything anyone else can see. The remaining deviations are the established ones: `ruff` through `python3 -m ruff` because the session guard denies the bare executable, exit codes captured through an explicit-argv `subprocess.run` wrapper because the guard rejects `$?` by form, and the G5 mutation restoring only the CONDITION while leaving the WHY comment in place.
END RECORD22
