── STEP T003/8 — F008 SSE event stream — ROUND 36 · CLOSURE COMMIT ───────────
Round base — the SHA every range gate in this block measures from: 3035bc2a
 (R35's handback, re-read from `git log` at emission, per R-0368.)
Goal:
 Close F008. Record the R35 verdict — PASS, bundle and package both re-verified
 by the reviewer — then write the authored STATUS `[x]` line, the README sync
 and the closure-candidate carrier in ONE commit, and open the pull request,
 which is NOT merged this session: it merges at the next feature's Open PR Gate,
 the operator's manual-review window.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r36.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R36, applied whole
 C2   `.agent/live_review.md` <- LEDGER36, appended
 C3   `tests/docs/test_docs_consistency.py` <- PINFROM replaced by PINTO, the
      one pin that hard-codes which feature is claimed, made independent of it
 C4   THE CLOSURE COMMIT, one commit carrying all three:
      `docs/roadmap/STATUS.md` <- STATUSFROM replaced by STATUSTO
      `README.md` <- RMCOUNT, RMTIER and RMLIST applied as three pairs
      `.agent/candidates.md` <- CANDIDATES, applied whole
 then, with NO commit between them: push, then `gh pr create` with PRBODY
 C5   `.agent/handoff.md`, the handback — which NAMES the pull request number,
      because the pull request exists before this commit is written (R-0449)

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r36.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `tests/docs/test_docs_consistency.py`,
 `docs/roadmap/STATUS.md`, `README.md`, `.agent/candidates.md`,
 `.agent/handoff.md`.

WHY C3 EXISTS, and why it is NOT part of the closure commit.
`tests/docs/test_docs_consistency.py` at `3035bc2a` asserts `^- \[~\] F008 —`
and that EXACTLY one feature is in progress, so closing F008 breaks it: the claim
it names disappears and the count goes to 0. The reviewer found this by running
the docs suite against the closure edits in a disposable worktree before emitting
this block, where it failed 1 of 295. Two standing rules meet here and only one
ordering satisfies both — R-0151 forbids a ledger change from landing without the
pin that reads it, R-0154 fixes the closure commit's path set. PINTO asserts the
invariant instead of the holder — AT MOST one `[~]` line, true WITH the claim and
WITHOUT it — so the suite is green at C3 and at C4, no commit is ever red, and
the closure commit's three paths stay three. R-0387's class one step later: that
finding fixed a pin naming the NEXT feature by naming the CURRENT one, moving the
breakage from every claim to every closure.

Rule A4, read against this sequence: the STATUS edit is the last SUBSTANTIVE
commit and the handback follows it — the F255 R21 precedent, and the only
reading under which the handback can name the pull request number at all.

Transport:
 This block is on disk at `.remedy-wt/f008-r36.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r36.md` for C0a. Never retype it. If
 the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are delimited by a line beginning `<<<SLICE <name>`
 and one beginning `<<<END <name>`; marker lines are NOT part of a slice. Every
 slice is newline-terminated with no trailing whitespace on any line, none begins
 with a blank line, and every count this block orders over a slice is taken over
 those newline-INCLUDED bytes.

Pair shape (§3 item 15). Each line below is the OUTPUT of the reviewer's
containment test over the final newline-INCLUDED bytes; the label is derived
from that output beside it and is never written on its own (R-0522):
 PINFROM/PINTO          TO contains FROM: false  -> REWRITE
 STATUSFROM/STATUSTO    TO contains FROM: false  -> REWRITE
 RMCOUNT-FROM/TO        TO contains FROM: false  -> REWRITE
 RMTIER-FROM/TO         TO contains FROM: false  -> REWRITE
 RMLIST-FROM/TO         TO contains FROM: true   -> APPEND
 The four REWRITEs owe the FROM-0x / TO-1x count. RMLIST is APPEND-shaped —
 its TO is the existing Tier 5 entry plus a new one — so a FROM-zero reading is
 unattainable there by construction and G8 orders instead that its FROM reads 1
 at BOTH the base and C4 while its TO goes 0 to 1, plus the one-pass
 substitution equality that covers all three README pairs at once.
 FROM uniqueness, each counted by the reviewer's own script IN the file the pair
 edits, at the round base, and reported as that script's output (item 25):
 PINFROM 1x in `tests/docs/test_docs_consistency.py`, where the count of LINES
 matching `\[~\] F008` is also 1; STATUSFROM 1x in `docs/roadmap/STATUS.md`,
 where the count of LINES matching `^- \[~\] ` is also 1; and RMCOUNT-FROM,
 RMTIER-FROM and RMLIST-FROM 1x each in `README.md`. Both pairs of readings
 agree, which is what item 25 asks for.
 PLANF008R36 and CANDIDATES are whole-file writes, LEDGER36 an append and
 PRBODY a new file in gitignored scratch, so none of the four is a pair.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit. C1
    is the first substantive commit (§3 item 23). C3 lands BEFORE C4, which is
    the whole point of splitting them. C4 carries STATUS, README and the
    carrier TOGETHER — README and STATUS may never disagree in any committed
    state, which is the R-0154 ledger cross-check pin — and the pull request is
    created after C4 and before C5.
 3. Nothing outside the change set is touched. No file under `packages/`, `apps/`
    or `docs/roadmap/features/` is edited: the code is final at `870f198e`, the
    accepted head the package covers. The ONE test file in the change set is
    edited by C3 alone and its edit changes an assertion's SHAPE, never its
    subject.
 4. NO FINDING ID IS MINTED and none is resolved: R-0630 stays free, and
    R-0368, R-0429, R-0553, R-0593, R-0622, R-0628 and R-0629 all stay OPEN.
    Write no `Done:` and no `Landed:` line. The one defect this closure review
    surfaced is carried as a CANDIDATE in `.agent/candidates.md`, per
    docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings": a
    finding raised during a closure review spends no id and is registered or
    resolved by the NEXT feature's first reviewed round.
 5. END EVERY COMMIT MESSAGE of this round with the trailer line
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, preceded by a
    blank line. G11 measures the result. Never repair a missing trailer by
    amending — protocol G2 forbids it.
 6. NEVER MERGE THE PULL REQUEST, never enable auto-merge, and wait on no CI
    run. It merges at the NEXT feature's Open PR Gate, the operator's
    manual-review window (closure protocol step 6). Create no branch, delete none.
 7. Commit subjects carry no leading-slash token, no absolute path and no
    secret-like string: the evidence-packaging metadata scanner rejects such
    subjects and blocks closure (AGENTS.md Commit Discipline).
 8. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there; commit nothing
    from it.
 9. THE HANDBACK QUANTIFIES NOTHING IT DID NOT COUNT (R-0553). Any handback
    sentence stating "every", "no", "all" or "none" over commits, files, ids or
    lines names the command that produced the number.
 10. THE HANDBACK'S `## Next` SECTION states, in this order: that this is the
    LAST round of this branch and its verdict therefore has no on-disk gate
    entry by construction (§4 item 13 — that absence is the terminator, not a
    missing gate); that the next session's FIRST action is the `.agent/STOP`
    re-read and its SECOND the Open PR Gate, at which THIS pull request is the
    one to merge; that the next free finding id is R-0630; that the seven ids
    of constraint 4 are OPEN and `.agent/candidates.md` carries one candidate
    the next feature's first reviewed round must register or resolve; and that
    Rule A5 proposes F009 — The single write channel — as the next feature,
    it being the first `[ ]` line this ledger carries top to bottom.

The reviewer's OWN readings, produced by RUNNING the tool at the round base
`3035bc2a`, in the PRIMARY checkout, not recalled (R-0625): `tests/docs/` EXITS
0 at 295 passed and 0 skipped, the golden-path canary EXITS 0 at 42 and 0, and
`run_integrity_checks()` returns passed True with 5 of 5 checks PASS. The
package was re-verified FROM DISK — sha256 recomputed to 1d827ac7…, `testzip()`
None over 12126 members, manifest READY_FOR_REVIEW with ready_gate_matrix.ok
true, empty blocking_reasons, alignment PASS at 0 issues and 0 hash mismatches,
and committed_review_subject base 7c03adfa… head 870f198e…, the full values
being in LEDGER36 and the STATUS line. The reviewer also DRY-RAN the closure
edits (item 12): in a throwaway worktree at the base, `tests/docs/` failed 1 of
295 on the claim pin — which is why C3 exists — and both red controls behaved,
the stale count failing `test_the_readme_accepted_count_equals_the_status_count`
and the stale tier row failing
`test_the_readme_tier_table_done_column_matches_the_ledger`. The reviewer has
NOT run `gh` and does not predict the pull request: G12 orders readings.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2, C3 and C4.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r36.md`
     as received, of `.agent/authored/f008-r36.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt (R-0371: this text cannot carry
     its own).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r36.md` with `git show`, by their marker lines, take
     the COUNT from that listing and report it — this block states no numeral
     for it (item 11) — plus each slice's newline-INCLUDED sha256 prefix, bytes
     and lines, that none carries trailing whitespace on any line, and that
     none begins with a blank line.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R36. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists.
 G5  The append at C2, against the round base, two ways that must agree. Read
     the base bytes with `git show 3035bc2a:.agent/live_review.md` into scratch
     — never over the tracked file (item 29). (a) the base blob is a byte-exact
     PREFIX of the C2 blob and the remainder equals a newline plus LEDGER36 —
     report its sha256 prefix, bytes and lines; (b) an INDEPENDENT blank-line
     split of the WHOLE C2 file, its terminating newline normalised first, has
     LEDGER36's paragraph as its LAST unit. NEGATIVE CONTROL: flip one
     PRINTABLE ASCII byte of the remainder to another printable one; BOTH
     readings must reject it and both accept the unflipped.
 G6  The sets in `.agent/live_review.md`, LINE-ANCHORED, reported at the round
     base AND at C2: `^- R-\d+ — ` reads 201 at both — this round mints no id —
     `^- R-0630 — ` 0 at both, `^- R-0593 — `, `^- R-0629 — `, `^- R-0429 — `,
     `^- R-0553 — `, `^- R-0628 — ` and `^- R-0368 — ` 1 each at both,
     `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0 at both, and `^Gate: R\d+ — `
     35 at the base and 36 at C2, over that many DISTINCT keys. HEADER SWEEP at
     C2 (item 26): report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, and the text of each non-match to its first
     period. Report the R36 pair's count TWICE and label both: LINE-ANCHORED
     over `^Gate: ` lines, which is the entry-key reading and must be 1, and as
     a bare substring anywhere in the file, which may legitimately exceed 1
     because findings QUOTE gate headers — R-0600 quotes another feature's
     round-35 header verbatim, and that is a quotation, not an entry.
 G7  The STATUS edit at C4. Report the count of STATUSFROM at the round base
     (expected 1) and at C4 (expected 0), of STATUSTO at the base (expected 0)
     and at C4 (expected 1), and that the base blob with that substitution
     applied ONCE is BYTE-EQUAL to the C4 blob — which is also the proof that
     no other line of that file changed. Report `^- \[x\] F\d{3} — ` at the
     base (expected 53) and at C4 (expected 54), and `^- \[~\] ` at the base
     (expected 1) and at C4 (expected 0).
 G8  The README sync at C4, one commit carrying three pairs. Report, for each
     pair separately, the count of its FROM at the round base and at C4 and of
     its TO at C4: RMCOUNT-FROM and RMTIER-FROM each go 1 to 0 with their TOs 0
     to 1, while RMLIST-FROM reads 1 at BOTH — its TO contains it — with
     RMLIST-TO 0 at the base and 1 at C4. Then report the reading that covers
     all three at once: the round-base blob of `README.md` with RMCOUNT, RMTIER
     and RMLIST each substituted ONCE, in that order, is BYTE-EQUAL to the C4
     blob. Report the file's line count at the base and at C4.
 G9  The pin at C3 and the carrier at C4. Report the count of PINFROM at the
     round base (expected 1) and at C3 (expected 0), of PINTO at the base
     (expected 0) and at C3 (expected 1), and that the base blob of
     `tests/docs/test_docs_consistency.py` with that substitution applied ONCE
     is BYTE-EQUAL to the C3 blob. Report also that C3 touches that ONE path
     and no other. Then report the sha256, bytes and lines of
     `.agent/candidates.md` at C4, whether it is byte-equal to CANDIDATES, and
     that the three paths of C4 are the ONLY paths that commit touches.
 G10 THE DOCS GATE, TWICE, AND THE CANARY ONCE — in the PRIMARY checkout,
     SERIALLY, never two test processes alive at once. Run
     `python3 -m pytest tests/docs/ -q -rf` at C3, where the claim is still
     `[~]`, and AGAIN at C4, where it is gone. BOTH must EXIT 0, and that pair
     of readings is the whole proof that PINTO is independent of which feature
     is claimed — one green run proves only the state it ran in. Then run
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf` at C4. Report each
     command's EXIT CODE and its passed and skipped numbers SEPARATELY as well
     as their sum. The reviewer's base readings are 295 and 42, and the docs
     suite is the one that goes red if the count, the tier table, the accepted
     list or the claim pin disagrees with the ledger — so if either docs run
     fails, report the real failure list and STOP: that is a repair, not a
     closure.
 G11 The range, measured from the round base this block's header names and from
     no other SHA. Report `git diff --name-only 3035bc2a..C4` and that it
     equals the Change set MINUS `.agent/handoff.md` exactly, with none on
     either side alone. Walk `git rev-list --reverse 3035bc2a..C4` and report
     ONE reading per commit: that it has exactly ONE parent, and BOTH numstat
     cells per path from `git show --numstat`, cross-checked against
     `git diff --numstat`, every insertion under 500 and every cell equal to
     the `+/-` column of your `## Commits` table, cell by cell (item 28). C5's
     own numbers cannot exist while C5 is being written, so they belong to the
     round report (item 14). Count LINES BEGINNING with `<<<SLICE ` or
     `<<<END ` in the plan at C1, the ledger at C2, the test file at C3, and
     STATUS.md, README.md and `.agent/candidates.md` at C4 — each is 0. Measure
     constraint 5 with
     `git log --format=%H%x09%(trailers:key=Co-Authored-By,valueonly) 3035bc2a..HEAD`
     before C5, reporting how many commits it lists and how many return a
     NON-EMPTY value, and classify this round's own reflog entries by the
     OPERATION before the first `:` in `%gs`: how many classified, `amend`,
     `rebase` and `cherry` at 0 (R-0601).
 G12 THE PULL REQUEST, after C4 and before C5. In order:
     (a) `git status --porcelain` EMPTY, then
         `git push -u origin feature/f008-sse-event-stream` — report exit+output.
     (b) `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
         — report it verbatim; this is the pre-check, not the gate.
     (c) Write PRBODY byte for byte to `.remedy-wt/f008-pr-body.md`, then
         `gh pr create --base main --head feature/f008-sse-event-stream
         --title 'F008 — SSE event stream (Tier 5)'
         --body-file .remedy-wt/f008-pr-body.md`. Report the exit code, the PR
         NUMBER and the URL.
     (d) `gh pr view <n> --json state,mergeable,isDraft,autoMergeRequest` —
         report it verbatim, and state that the pull request was NOT merged and
         auto-merge NOT enabled (constraint 6).
     If any `gh` command is refused by the session guard, report the refusal
     verbatim, write the handback naming the pull request as NOT CREATED with
     the exact command for the operator to run, and STOP — an unopened pull
     request is an honest handback, not a failure to hide.
 G13 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 10
     names in that order, an item-status table holding exactly one row for each
     of C0a, C0b, C1, C2, C3, C4 and C5, the pull request number from G12(c),
     and the four closure values the STATUS line quotes — evidence job, package,
     SHA-256 and the accepted head — so the record survives without the ledger.
     Measure its line count with `wc -l` BEFORE committing it; this round's
     commit count is seven, so the cap is 100, and an overage carries a DECISION
     D15 stated-cause line naming the real count and the mandated content that
     caused it. One line per gate here; raw transcripts go in the ROUND REPORT
     (R-0582). Push once more after C5 so the pull request shows the handback;
     that push belongs to the round report.

Handback: completion report + rewrite `.agent/handoff.md`, whose state block repeats verbatim:
 100 % (T001 ✅ · T002 ✅ · T003 ✅ · Integrations-Gate PASSED · Evidence-Job und READY_FOR_REVIEW-Paket verifiziert · STATUS `[x]`, README-Sync und Pull Request gelandet — F008 GESCHLOSSEN, der PR merged am Open PR Gate des nächsten Features) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R36
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint streaming the event ledger from a cursor — the ledger's
own monotonic seq carried and never renumbered, a 15 s heartbeat, Last-Event-ID
resume replaying exactly the missed span — plus a client hook with reconnect
backoff, gap detection and an honest polling fallback that labels itself
delayed. DONE when a fake job streams into a test client with zero gaps across
forced disconnects, the transcript byte-equals the ledger's envelope sequence,
the heartbeat holds cadence, and the fallback engages on a disabled EventSource
and recovers to live.

## Current Step
R36 CLOSES F008. It records the R35 verdict — PASS, with the evidence bundle and
the READY_FOR_REVIEW package re-verified from disk by the reviewer — makes the
one docs pin that hard-codes the claimed feature independent of it, then lands
the authored STATUS `[x]` line, the README sync and the closure-candidate
carrier in ONE commit and opens the pull request. That pull request is NOT
merged this session: it merges at the next feature's Open PR Gate.

## Next Steps
1. The next session starts at Phase 1: the `.agent/STOP` re-read, then the Open
   PR Gate, where this feature's pull request is the one to merge.
2. Rule A5 then proposes F009 — The single write channel — the first `[ ]` line
   this ledger carries top to bottom. That feature's first reviewed round
   registers or resolves the entry `.agent/candidates.md` carries.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a paydown
  branch.
<<<END PLANF008R36

<<<SLICE LEDGER36
Gate: R36 — the R35 entry. R35 PASSED, AND ITS TWO ARTEFACTS ARE RE-VERIFIED FROM DISK RATHER THAN READ BACK. The round recorded the R34 verdict, wrote this feature's Built State into `docs/roadmap/features/T5_F008.md`, and produced the evidence bundle and the review zip that closure cannot happen without. TRANSPORT EQUAL THREE WAYS: `.agent/authored/f008-r35.md` at `67deb26f` and `.agent/last_block.md` at `5ec8fbe3` are both sha256 ddba2900a2b9fce4020c83b5ef53d18c5161a70f64479bdcd07bb78ec0795f37 over 32543 bytes and 469 lines, EQUAL to the digest the reviewer emitted and under the 490-line budget DECISION F085 D6 rules. FOUR SLICES by the reviewer's own ordered extraction out of the committed C0a blob — EVIDENCESCRIPT fef5dd76 at 120 lines, BUILTSTATE 1b0d8baf at 49, PLANF008R35 b4341d7c at 37 and the single-line LEDGER35 6d50bb39 — none carrying trailing whitespace on any line, none beginning with a blank line, and each newline-terminated. THE PLAN LANDED FIRST at `c7871ec8`, byte-equal at 37 lines under the 50-line cap. THE LEDGER APPEND at `c5ebf179` is proved twice over: the base blob is a byte-exact prefix with a 4987-byte remainder equal to a newline plus LEDGER35, and an INDEPENDENT split of the whole file gives 246 units whose LAST is LEDGER35's paragraph, with a one-byte printable flip REJECTED by BOTH readings and the unflipped value ACCEPTED by both. THE BUILT STATE APPEND at `870f198e` is the same shape — base blob a byte-exact prefix, remainder a newline plus BUILTSTATE over 3284 bytes and 50 lines — with `^## Built State` going 0 to 1 in that file. THE SETS HELD: 201 findings at the base and at C2 with NO id minted and R-0630 still 0, the seven open ids 1 each, `Done:` 6, `Landed:` 0, and `Gate: R` 34 to 35 over that many DISTINCT keys, 34 of 35 headers matching the shape with `Gate: R1 — the F255 R21 entry.` the single non-match. THE GATES ARE THE REVIEWER'S OWN: `tests/docs/` EXITS 0 at 295 passed, the golden-path canary EXITS 0 at 42, and `run_integrity_checks()` returns passed True with all five checks PASS — handler_import, live_review_verdict, plan_consistency, relevant_untracked and high_blockers_open. THE EVIDENCE BUNDLE is 27 entries at job id `f008-closure`, head `870f198e`, total_passed 97 over six verification runs whose node ids come from `--collect-only` and never from a regex over a `-v` log (R-0611), each with `len(node_ids) == selected`, sorted `test_files` that are all files, a `^vr-\d{4,}` run id, and `output_hash` equal to the sha256 of `stdout_summary` EXACTLY — the pitfall that blocked the F083 closure. THE PACKAGE IS RE-VERIFIED FROM DISK BY THE REVIEWER, not quoted: `remedy-review-20260821-193052-READY_FOR_REVIEW.zip` recomputes to sha256 1d827ac756433f3be73f02947d9b1410e7759c4fc9ef6dfd95f5032924b9a366, `zipfile.testzip()` returns None over 12126 members, and its own manifest reads PACKAGE_STATUS READY_FOR_REVIEW, `ready_gate_matrix.ok` true with an EMPTY blocking_reasons, alignment PASS with 0 issues and 0 hash mismatches, `packaged_evidence_job_id` f008-closure, and committed_review_subject base 7c03adfa58519d484df685d38b950c49afaf70a8 with head 870f198ea9c0e4b51075f3386d1025cce805811a, which is R35's own Built State commit — the one the STATUS line records under its `accepted HEAD` field, a field whose value is an absolute SHA and never a re-resolving label. THE ROUND DECLARED TWO THINGS IT COULD HAVE BURIED. The zip was built TWICE because the first invocation was piped through `tail` and lost the exit code the gate ordered; the round reported both attempts and claimed no value of the first. And it flagged, without spending an id, that the manifest's `dirty_file_count_total` reads 1 while `git status --porcelain` printed 0 lines at the same head. THE REVIEWER RESOLVED THAT SECOND ONE rather than leaving it open: `dirty_file_count_total` counts `git status` records taken DURING the build, `.review_zip_manifest.json` is written to the repository root by the packager itself and is matched by no `.gitignore` rule — `.data/` is ignored at line 211 and `remedy-review-*` at line 223, but that path is not — so the single record is the packager's own manifest, which is why `dirty_source_test_files` is empty and the alignment verdict is PASS. ONE DEFECT IS CARRIED AS A CLOSURE CANDIDATE, and it is the reviewer's: the R35 block's G6 ordered "the R35 pair occurs EXACTLY ONCE" without saying LINE-ANCHORED, and `.agent/live_review.md` already contained that byte string a second time inside R-0600, which quotes the F086 record's identically-worded round-35 header. The worker read it line-anchored, which is the entry-key reading item 26 exists for, and reported 1 correctly; under a whole-file substring reading the same gate is unmeetable, and every future round whose header a finding has quoted inherits it. NO FINDING IS REGISTERED AGAINST THE WORKER: every value it reported reproduced, including all four slice digests, the transport digest, both append proofs, the three suite readings and the package's own sha256.
<<<END LEDGER36

<<<SLICE PINFROM
        # ...and nothing after F012 has been started except F017 (accepted) and
        # the ONE feature currently claimed. R-0387 recurrence, F008 R1: this pin
        # read `[ ]` F008, so it asserted that NO feature was in progress and the
        # next claim had to break it. The invariant this workflow really holds is
        # that exactly one `[~]` entry exists (planner_reviewer_prompt.md §1), so
        # pin that and name its holder instead.
        in_progress = re.findall(r"^- \[~\] F\d{3} —", text, re.M)
        assert len(in_progress) == 1, f"exactly one feature is in progress, found {in_progress}"
        assert re.search(r"^- \[~\] F008 —", text, re.M)
        assert re.search(r"^- \[x\] F017 —", text, re.M)
<<<END PINFROM

<<<SLICE PINTO
        # ...and nothing after F012 has been started except F017 (accepted) and
        # whatever feature is claimed at the time. R-0387, F008 R1: this pin read
        # `[ ]` F008, so it asserted that NO feature was in progress and the next
        # claim had to break it. Naming the holder instead moved the same defect
        # from every claim to every CLOSURE — closing F008 removes the only `[~]`
        # line, taking the count to 0 (measured at 3035bc2a against the closure
        # edits in a throwaway worktree: 1 failed, 294 passed, this test). The
        # invariant the workflow holds is AT MOST one claim
        # (planner_reviewer_prompt.md §1), true in both states, so this pin
        # survives a claim and a closure alike.
        in_progress = re.findall(r"^- \[~\] F\d{3} —", text, re.M)
        assert len(in_progress) <= 1, f"at most one feature is in progress, found {in_progress}"
        assert re.search(r"^- \[x\] F017 —", text, re.M)
<<<END PINTO

<<<SLICE STATUSFROM
- [~] F008 — SSE event stream
<<<END STATUSFROM

<<<SLICE STATUSTO
- [x] F008 — SSE event stream (T001–T003 complete; accepted 2026-08-21 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f008-closure · package remedy-review-20260821-193052-READY_FOR_REVIEW.zip · SHA-256 1d827ac756433f3be73f02947d9b1410e7759c4fc9ef6dfd95f5032924b9a366 · accepted HEAD 870f198ea9c0e4b51075f3386d1025cce805811a)
<<<END STATUSTO

<<<SLICE RMCOUNT-FROM
53 of 255 registered items accepted. Next: F008 (SSE event stream).
<<<END RMCOUNT-FROM

<<<SLICE RMCOUNT-TO
54 of 255 registered items accepted. Next: F009 (The single write channel).
<<<END RMCOUNT-TO

<<<SLICE RMTIER-FROM
| 5 | Operator Cockpit | 1 | 29 |
<<<END RMTIER-FROM

<<<SLICE RMTIER-TO
| 5 | Operator Cockpit | 2 | 29 |
<<<END RMTIER-TO

<<<SLICE RMLIST-FROM
F255 teacher role (`remedy teach narrate`, `remedy teach ask`, teacher spend
reported as its own role in the token ledger).
<<<END RMLIST-FROM

<<<SLICE RMLIST-TO
F255 teacher role (`remedy teach narrate`, `remedy teach ask`, teacher spend
reported as its own role in the token ledger).
F008 sse event stream (per-job SSE endpoint with heartbeat and Last-Event-ID
resume, a cockpit client with reconnect backoff and a polling fallback that
labels itself delayed instead of pretending to be live).
<<<END RMLIST-TO

<<<SLICE CANDIDATES
# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- A UNIQUENESS GATE OVER `.agent/live_review.md` MUST SAY LINE-ANCHORED, BECAUSE
  THAT FILE LEGITIMATELY QUOTES ITS OWN GATE HEADERS. · source F008, raised by
  the reviewer during the R35 gate · 2026-08-21. The R35 block's G6 ordered "the
  R35 pair occurs EXACTLY ONCE" for the entry `Gate: R35 — the R34 entry.` The
  worker read it line-anchored over `^Gate: ` lines, reported 1, and was right:
  measured by the reviewer at `c5ebf179`, that byte string occurs TWICE in the
  file, the second inside finding R-0600, which quotes the F086 record's
  identically-worded round-35 header. Header strings repeat across features by
  construction, so any round whose header a finding has quoted inherits an
  unmeetable gate the moment the count is read as a substring. Nothing false
  landed and the ledger is healthy — 35 `Gate: ` lines under 35 distinct keys at
  that commit. Counter-measure, beside §3 item 26 which produced this gate class:
  a uniqueness or count gate over a file that quotes its own record format states
  the anchor it is read under, and a block ordering such a count orders BOTH
  readings and labels each — as R-0586 already requires backtick-quoted spans to
  be deleted before a token is counted. The fix edits
  `docs/agents/planner_reviewer_prompt.md`, which F008 does not own, so it routes
  to the paydown branch carrying the reviewer-text findings.
<<<END CANDIDATES

<<<SLICE PRBODY
## What

A per-job SSE event stream, end to end.

- **Server** (`packages/orchestration/ui_server.py`) — streams the ledger's OWN
  monotonic seq as the SSE event id and never assigns one, so a resume is a span
  of the ledger rather than a renumbering of it. Heartbeat at cadence,
  `Last-Event-ID` replays exactly the missed span, and a connection cap answers
  over-subscription with 429 instead of an unbounded thread count.
- **Client** (`apps/ui/src/api/brainStream*.ts`) — reconnect backoff, gap
  detection against the carried seq, and a polling fallback for a runtime with no
  EventSource. Deliberately NOT React, so the node-environment vitest reaches
  every rule it has.
- **Cockpit** (`useBrainStream.ts`, `RemedyShell.tsx`, `LiveStatusPill.tsx`) —
  the shell subscribes with its loaded dashboard's job id, and the transport's
  status reaches the badge, which says DELAYED rather than pretending to be live.

## Why

The cockpit could show a job's state but not its motion: every panel polled. The
acceptance condition this feature was registered under is that the fallback
labels itself visibly instead of claiming liveness it does not have — which is
why the badge reads the TRANSPORT's status and treats the dashboard's own
liveness as the fallback arm.

## Key decisions

- **DECISION F008 D3** — the subscription lives in `RemedyShell`, not
  `RemedyApp`: the shell renders only once a dashboard has loaded, so
  `dashboard.jobId` is always a real job, where `RemedyApp` would open a stream
  against an empty id on every URL that carries none.
- `makeDeps` is read through a ref, not a hook dependency: a caller writing its
  deps inline hands a new function every render, and a memo honouring that
  identity would reopen the EventSource on every parent render.

## How to review

No DOM environment here, so React is gated by reading COMMENT-STRIPPED source
(`tests/ui_contracts/`); the logic lives under `apps/ui/src/api/` where vitest
exercises it, and server behaviour under `tests/ui_server/`.

## Verification

- **Integration gate (R34)** — full suite twice, `pytest -n auto -q`: branch run
  exit 0 at 17412 passed / 20 skipped, base run at the merge base exit 0 at 17315
  / 20, **0 branch-only and 0 base-only failures**. The branch side was re-run
  independently by the reviewer with identical counts.
- **Latest verdict** — R35 PASS. Every round was gated by a reviewer who re-ran
  the round's commands out of the committed blobs.
- **Evidence job** `f008-closure` · 27-entry bundle · 97 tests over six runs.
- **Package** `remedy-review-20260821-193052-READY_FOR_REVIEW.zip` · SHA-256
  `1d827ac756433f3be73f02947d9b1410e7759c4fc9ef6dfd95f5032924b9a366` ·
  READY_FOR_REVIEW, alignment PASS, 0 blocking reasons · accepted head
  `870f198ea9c0e4b51075f3386d1025cce805811a`.
- 76 files at `870f198e`, +16468 / -509, of which the `.agent/` round record is
  most of the count.

## Open findings

Seven ids are open on this branch: R-0368, R-0429, R-0553, R-0593, R-0622,
R-0628 and R-0629. Six are defects in reviewer or process text; R-0622 is the
`apps/ui` lint configuration, which installs no TypeScript parser and is RED at
this branch's base — not a gate here, and routed to a paydown branch like the
other six. None is a defect in the streaming code this feature ships.

## Runtime actuals

36 rounds. Wall clock and token cost across the feature: not-measured — the
ledger does not carry them per round, and a guess is worse than the gap.
<<<END PRBODY
