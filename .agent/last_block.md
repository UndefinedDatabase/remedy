── STEP T003/8 — F008 SSE event stream — ROUND 34 ────────────────────────────
Round base — the SHA every range gate in this block measures from: 88c55f5d
 (R33's handback, re-read from `git log` at emission, per R-0368.)
Goal:
 Record the R33 verdict — PASS, every gate re-run by the reviewer out of the
 committed blobs — retire the one claim R33's own change set left standing in
 shipped code, and RUN THE INTEGRATION GATE per docs/agents/integration_gate.md:
 the full suite once on this branch and once at the merge base, compared and
 attributed id by id. This is the last round before closure.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r34.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R34, applied whole
 C2   `.agent/live_review.md` <- R0593FROM replaced by R0593TO, a REWRITE
 C3   `.agent/live_review.md` <- LEDGER34, appended
 C4   `apps/ui/src/components/panels/LiveStatusPill.tsx` <- PILLFROM replaced
      by PILLTO, a REWRITE
 C5   `.agent/gate_f008_r34/` <- the integration gate's evidence files
 C6   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r34.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`,
 `apps/ui/src/components/panels/LiveStatusPill.tsx`,
 `.agent/gate_f008_r34/` and the files inside it, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r34.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r34.md` for C0a. Never retype it. If
 the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are delimited by a line beginning `<<<SLICE <name>`
 and one beginning `<<<END <name>`; marker lines are NOT part of a slice. Every
 slice is newline-terminated with no trailing whitespace on any line, none
 begins with a blank line, and every count this block orders over a slice is
 taken over those newline-INCLUDED bytes.

Pair shape (§3 item 15). Each line below is the OUTPUT of the reviewer's
containment test over the final newline-INCLUDED bytes; the label is derived
from that output beside it and is never written on its own (R-0522):
 R0593FROM/R0593TO      TO contains FROM: false  -> REWRITE
 PILLFROM/PILLTO        TO contains FROM: false  -> REWRITE
 R0593FROM reads as an append by eye and is not one, because it is
 newline-TERMINATED while its TO continues that sentence on the same line. Both
 pairs therefore owe the FROM-0x / TO-1x count a rewrite owes, and neither owes
 the §4.9 append obligation.
 FROM uniqueness, each counted by the reviewer's own script IN the file the
 pair edits, at the round base, and reported as that script's output (item 25):
 R0593FROM occurs 1x in `.agent/live_review.md`; PILLFROM occurs 1x in
 `apps/ui/src/components/panels/LiveStatusPill.tsx`, and the count of LINES in
 that file containing `no caller holds one yet` is also 1 — the two readings
 agree, which is the reading R-0629's widened fix asks for.
 PLANF008R34 is a whole-file write and LEDGER34 an append, so neither is a pair
 and neither carries a containment reading.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23), C2 precedes C3 so each
    ledger proof reads against a single-purpose commit, and C4 precedes the
    runs of G9 and G10 so the full suite measures the tree this feature will
    close with. R0593TO's sentence "the fix is this round's C4" is made true by
    this constraint and by nothing else (§4 item 20, the R-0524 carve-out).
 3. Nothing outside the change set is touched. No dependency is added, no
    `apps/ui/**` file other than `LiveStatusPill.tsx` is opened for writing,
    and PILLTO changes a COMMENT only: the component's code, its props and its
    three returns are left byte-identical, which is why G8 can order the two
    contract files that read this component to stay green without a single
    assertion changing.
 4. NO FINDING ID IS MINTED: R-0630 stays free. R-0593 is AMENDED, not
    resolved, and stays OPEN, as do R-0368, R-0429, R-0553, R-0622, R-0628 and
    R-0629. Write no `Done:` and no `Landed:` line for any of them. The
    reviewer searched the ledger for the DEFECT before routing it here (item
    30), and R-0593's subject — a production comment denying code the same
    feature had already built — is this defect exactly, so it takes the
    amendment rather than a second id.
 5. END EVERY COMMIT MESSAGE of this round with the trailer line
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, preceded by a
    blank line. G13 measures the result. Never repair a missing trailer by
    amending — protocol G2 forbids it and G13 gates it at 0.
 6. The post-C6 porcelain, `git worktree list` and push output belong to the
    ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 7. Two test processes never run at once. G9's branch run happens in the
    PRIMARY checkout (R-0518); G10's base run happens in a disposable worktree
    and is the ONLY thing running while it runs; G11's serial re-runs happen
    after both have exited.
 8. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH other than
    the throwaway `tmp/base-gate-r34` G10 names, which is deleted in the same
    gate. Push `feature/f008-sse-event-stream` and leave it open;
    `gh pr list --state open` returned `[]` at the reviewer's Phase 0 probe.
 9. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there; commit nothing
    from it. Never `cd` into a worktree and leave the shell there — a later
    gate then silently measures the wrong tree (R-0463).
 10. THE HANDBACK QUANTIFIES NOTHING IT DID NOT COUNT (R-0553). Any handback
    sentence stating "every", "no", "all" or "none" over commits, files, ids or
    rounds names the command that produced the number. State the particular you
    measured, or nothing. This binds the attribution of G11 hardest: "all
    base-only ids are environmental" is a claim about a set, and it is written
    only beside the per-id evidence that produced it.
 11. THE HANDBACK'S `## Next` SECTION states, in this order: that the next
    session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and
    its SECOND the Open PR Gate (Phase 1 rule 2); that R34 is PENDING REVIEW
    and its verdict is owed by the next round's ledger commit; that the next
    free finding id is R-0630; that R-0368, R-0429, R-0553, R-0593, R-0622,
    R-0628 and R-0629 are OPEN; and that R35's work is the CLOSURE ROUND per
    docs/roadmap/STATUS_closure_protocol.md — evidence job, a FRESH review zip,
    the authored STATUS line and the pull request — unless G11 named a BLOCKER,
    in which case it names the blocker and the repair round instead.

The reviewer's OWN readings, each produced by RUNNING the tool at the round base
`88c55f5d`, serially, in the PRIMARY checkout, not recalled (R-0625): the
five-target state reader plus canary EXITS 0 at 465 passed and 0 skipped;
`python3 -m pytest tests/ui_contracts/ -q -rf` EXITS 0 at 417 passed plus 4
skipped = 421; and in `apps/ui`, `npm run --silent typecheck` EXITS 0 with a
zero-byte output stream while `npx vitest run` EXITS 0 at 10 files and 152
tests. `npm run lint` is RED at base, which is R-0622 and NOT a gate (R-0364).
The reviewer also DRY-RAN PILLTO (item 12): in a disposable worktree at
`88c55f5d` with `apps/ui/node_modules` SYMLINKED for a read-only typecheck and
the primary checkout never written to, G8's exact pytest command EXITS 0 at 98
passed plus 1 skipped both BEFORE and AFTER the substitution, `npm run --silent
typecheck` EXITS 0 in both states, and the RED CONTROL — the pill's rendered
`DELAYED` replaced by another word — EXITS 1 failing exactly
`TestLiveStatusPillVariants::test_a_delayed_stream_says_delayed`, so the gate
can fail and its green means something.
The reviewer has NOT run the full suite at this base: the run IS this round, and
a colour it has not measured is one it may not order (G4 of the protocol). G9
and G10 therefore order READINGS — exit code, failure list, wall time — and
never a colour.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2, C3, C4 and C5. Per constraint 6 the post-C6
     readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r34.md`
     as received, of `.agent/authored/f008-r34.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r34.md` with `git show`, by their marker lines, take
     the COUNT from that listing and report it — this block states no numeral
     for it (item 11) — plus each slice's newline-INCLUDED sha256 prefix, bytes
     and lines, that none carries trailing whitespace on any line, and that
     none begins with a blank line.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R34. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The REWRITE at C2. Read the base bytes with
     `git show 88c55f5d:.agent/live_review.md` into scratch or memory — never
     by writing over the tracked file, which protocol G5 forbids (item 29).
     Report the count of R0593FROM at the round base (expected 1) and at C2
     (expected 0), and of R0593TO at the base (expected 0) and at C2 (expected
     1) — the FROM-0x / TO-1x proof a rewrite owes. Report also that the base
     blob with that substitution applied ONCE is BYTE-EQUAL to the C2 blob, the
     blank-line paragraph COUNT unchanged, and EXACTLY ONE paragraph differing,
     the one beginning `- R-0593 — `.
 G6  The append at C3, against C2, two ways that must agree. (a) the C2 blob is
     a byte-exact PREFIX of the C3 blob and the remainder equals a newline plus
     LEDGER34 — report its sha256 prefix, bytes and lines; (b) an INDEPENDENT
     blank-line split of the WHOLE C3 file, its terminating newline normalised
     first, has LEDGER34's paragraph as its LAST unit. NEGATIVE CONTROL: flip
     one PRINTABLE ASCII byte of the remainder to another printable one; BOTH
     readings must reject it and both accept the unflipped.
 G7  The sets in `.agent/live_review.md`, line-anchored, each reported at the
     round base, at C2 AND at C3: `^- R-\d+ — ` reads 201 at all three — this
     round mints no id — `^- R-0630 — ` 0 at all three, `^- R-0593 — `,
     `^- R-0629 — `, `^- R-0429 — `, `^- R-0553 — `, `^- R-0628 — ` and
     `^- R-0368 — ` 1 each at all three, `^Done: R-\d+ — ` 6 at all three,
     `^Landed: ` 0 at all three, and `^Gate: R\d+ — ` 33 at the base and at C2
     and 34 at C3, over that many DISTINCT keys. HEADER SWEEP at C3 (item 26):
     report how many `Gate: ` lines match `^Gate: R(\d+) — the R(\d+) entry\.`
     with the second numeral one below the first, how many do not, the text of
     each non-match to its first period, and that the R34 pair occurs EXACTLY
     ONCE.
 G8  The comment retirement at C4. Report the count of PILLFROM at the round
     base (expected 1) and at C4 (expected 0), of PILLTO at the base (expected
     0) and at C4 (expected 1), that the base blob with that substitution
     applied ONCE is BYTE-EQUAL to the C4 blob, and the file's line count at
     both — 21 at the base, and 24 in the reviewer's dry run of this same
     slice. Then, from the repository root at C4,
     `python3 -m pytest tests/ui_contracts/test_live_status_pill.py tests/ui_contracts/test_responsive.py -q -rf`
     EXITS 0 at a passed-plus-skipped SUM of 99, reported as passed and skipped
     SEPARATELY as well as their sum — THE SUM IS THE GATE, a bare passed count
     is not — and in `apps/ui`, `npm run --silent typecheck` EXITS 0 with a
     zero-byte output stream. Those two test files are the ones that read this
     component: the first asserts over COMMENT-STRIPPED source and the second
     asserts `LIVE` in the raw text, so a comment-only edit leaves both true —
     but the reviewer MEASURED that rather than reasoning it, and the gate is
     the run and not this sentence.
 G9  THE BRANCH RUN, integration_gate.md step 1, from the repository root in
     the PRIMARY checkout, AT C4. `python3 -m pytest -n auto -q`, with the raw
     log written to `.remedy-wt/.cache/gate_r34/branch_run.log` — OUTSIDE the
     tracked tree, because a log growing inside the repo during a run changes
     the worktree digest mid-run and fails the manifest-identity ids as false
     positives (R-0176). Report the exit code, the wall seconds, the summary
     line verbatim, and the sorted list of `^FAILED` lines as
     `branch_failed.txt`. An EMPTY failure list is a reading: report it as 0
     and say which command produced the 0. Over ~5 minutes wall clock, note a
     perf pass (integration_gate.md step 5).
 G10 THE BASE RUN, integration_gate.md step 2, at the merge base. Report that
     `git merge-base main HEAD` and `git rev-parse main` both print
     7c03adfa58519d484df685d38b950c49afaf70a8. Create the worktree ON A BRANCH,
     never detached — the self-dogfood branch guard refuses a detached HEAD by
     design (DECISION D3): `git worktree add -b tmp/base-gate-r34
     .remedy-wt/base-r34 7c03adfa`. Then, in this order:
     (a) PARITY, restored not assumed. Copy `apps/ui/node_modules` and
         `apps/ui/dist` from the primary checkout with
         `shutil.copytree(src, dst, symlinks=True)`. The `symlinks=True`
         argument is the ORDER and not a detail: `copytree` defaults to
         `symlinks=False`, which dereferences npm's bin shims and itself causes
         the base-only failures parity exists to prevent (R-0591). Report for
         each destination that it exists, is a directory and is NOT a symlink.
     (b) THE STALENESS THE COPY CREATES, closed deliberately.
         `_frontend_is_stale` in `packages/orchestration/ui_server.py` decides
         by MTIME, not by digest (R-0565), and `git worktree add` writes
         `apps/ui/src` fresh while `copytree` preserves the primary's older
         mtime on `apps/ui/dist/index.html` — which is exactly why the F255 R18
         gate recorded nine base-only failures. Report the newest mtime under
         the base worktree's `apps/ui/src` and the mtime of its
         `apps/ui/dist/index.html` BEFORE any repair; then set every copied
         `apps/ui/dist` file's mtime to now, report the two readings again, and
         report which of the two comparisons holds each time. This preparation
         step MOVES the mtime on purpose, and it is reported as preparation:
         the readings that decide the parity claim are the ones taken AFTER it.
     (c) THE RUN. From that worktree's root, `python3 -m pytest -n auto -q`,
         with `REMEDY_UI_NO_AUTO_BUILD=1` passed through the `env=` parameter
         of `subprocess.run` as a copy of `os.environ` with that one key added
         — never as a `VAR=value` shell prefix, which constraint 9's guard
         rejects — and the raw log at `.remedy-wt/.cache/gate_r34/base_run.log`.
         Report the exit code, wall seconds, the summary line and the sorted
         `^FAILED` lines as `base_failed.txt`.
     (d) THE NEUTRALISATION, VERIFIED RATHER THAN TRUSTED. Report, for BOTH the
         primary checkout and the base worktree, BEFORE and AFTER the run: a
         sha256 folded over `apps/ui/dist` (each file's path and bytes, sorted),
         the count of regular files under it, and `index.html`'s `st_mtime_ns`.
         State `PARITY_CLAIM=HELD` only if, across the RUN, every digest, every
         file count and every mtime is unchanged on both sides; otherwise
         `PARITY_CLAIM=VOID`. Report also how many lines of the base log match
         `auto-build (`, which is what a launched npm build would print.
     (e) Remove the worktree, delete `tmp/base-gate-r34`, prune, and report
         `git worktree list` naming only the primary checkout and
         `git branch --list tmp/base-gate-r34` printing nothing.
 G11 COMPARE AND ATTRIBUTE, integration_gate.md steps 3 and 4. Report
     `comm -13 base_failed.txt branch_failed.txt` as the BRANCH-ONLY set and
     `comm -23 base_failed.txt branch_failed.txt` as the BASE-ONLY set, each
     with its count, and an empty set reported as 0 rather than omitted.
     (a) For EVERY branch-only id: re-run that exact node id SERIALLY in the
         primary checkout at C4 and report the result. Serial-pass is the
         xdist-flake class — record it, it is not a blocker. Serial-fail is
         reproduced at the merge base BEFORE the feature is blamed. A
         reproducible branch-only failure coupled to this feature's code is a
         BLOCKER: STOP, write the handback naming it, and do not proceed to
         C5's evidence claim or to closure — the fix is its own reviewed round.
     (b) For EVERY base-only id: attribute it by DIRECT evidence, naming per id
         the artifact or mechanism that produced it. This obligation is
         UNCONDITIONAL and does not depend on the parity verdict: a gate that
         discharges itself when its guard passes protects nothing, which is
         finding R-0590 and cost the R23 gate 23 unattributed ids.
     (c) State the branch-only and base-only counts as the numbers `comm`
         printed, and write no sentence about either set that those numbers do
         not carry (constraint 10).
 G12 THE EVIDENCE, at C5, in `.agent/gate_f008_r34/`, whose file names and
     shape follow `.agent/gate_f255_r18/`, on disk at the round base: the
     branch run's meta and tail, `branch_failed.txt`, `base_parity.txt`,
     `base_failed.txt`, the two `comm` files and `attribution.txt`, plus a
     provenance file naming where each raw log lives. EVERY member is `.txt`
     and never `.log`: `.gitignore` drops `*.log` silently and the review-zip
     guard rejects any `\.log$` member (R-0169). Report the file list with
     sizes, that 0 of them match `\.log$`, and that `git status --porcelain` is
     empty after C5.
 G13 The range, measured from the round base this block's header names and from
     no other SHA. Report `git diff --name-only 88c55f5d..C5` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly, with none on either side
     alone; the full reading to C6 belongs to the ROUND REPORT (constraint 6).
     Walk `git rev-list --reverse 88c55f5d..C5` and report ONE reading per
     commit: that it has exactly ONE parent, and BOTH numstat cells per path
     from `git show --numstat`, cross-checked against `git diff --numstat`,
     every insertion under 500 and every cell equal to the `+/-` column of your
     `## Commits` table, cell by cell (item 28). C6's own numbers cannot exist
     while C6 is being written, so they belong to the round report (item 14).
     Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in the plan at C1, the
     ledger at C2 and at C3, the pill at C4 and the handback at C6 — each is 0;
     `.agent/last_block.md` is NOT in that list, being the block's own mirror.
     Measure constraint 5 with
     `git log --format=%H%x09%(trailers:key=Co-Authored-By,valueonly) 88c55f5d..HEAD`
     before C6 and report how many commits it lists and how many return a
     NON-EMPTY value — state it as that measurement and never as a universal.
     Report this round's own reflog entries classified by the OPERATION before
     the first `:` in `%gs`: how many you classified, and `amend`, `rebase` and
     `cherry` at 0. Assert no total over the whole reflog (R-0601).
 G14 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 11
     names in that order, and an item-status table holding exactly one row for
     each of C0a, C0b, C1, C2, C3, C4, C5 and C6 — "exactly one row" scoping to
     that TABLE. Measure its line count with `wc -l` BEFORE committing it; this
     round's commit count is above five, so the cap is 100, and an overage
     carries a DECISION D15 stated-cause line naming the real count and the
     mandated content that caused it. One line per gate here; raw transcripts
     go in the ROUND REPORT (R-0582) and the gate's own numbers in C5's files.

Handback: completion report + rewrite `.agent/handoff.md`, whose state block repeats verbatim:
 ~99 % (T001 ✅ · T002 ✅ · T003 ✅ — Client, Badge, Deps-Factory, Browser-Env und Cockpit-Wiring komplett; Integrations-Gate in dieser Runde) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R34
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
R34 records the R33 verdict — PASS, every gate re-run by the reviewer out of the
committed blobs — retires the stale claim in `LiveStatusPill.tsx` that R33's own
change set could not reach, and RUNS THE INTEGRATION GATE per
docs/agents/integration_gate.md: the full suite once on this branch and once at
the merge base `7c03adfa`, compared, with every branch-only and every base-only
id attributed by direct evidence.

## Next Steps
1. R35 is the closure round per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, a FRESH review zip, the authored STATUS line and the pull
   request — unless the gate names a blocker, which is its own repair round.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The base worktree's copied `apps/ui/dist` looks STALE by mtime to
  `_frontend_is_stale`, which is what produced nine base-only failures at the
  F255 R18 gate. This round repairs the mtime before the base run and reports
  both readings, so a base-only failure is evidence rather than furniture.
<<<END PLANF008R34

<<<SLICE R0593FROM
COUNTER-MEASURE, applied by this round's C3 and C4 rather than asserted here: both comments are retired at their source, each naming the commit that falsified it, and the next block that adds a capability an existing comment calls absent is the one that owes the sweep.
<<<END R0593FROM

<<<SLICE R0593TO
COUNTER-MEASURE, applied by this round's C3 and C4 rather than asserted here: both comments are retired at their source, each naming the commit that falsified it, and the next block that adds a capability an existing comment calls absent is the one that owes the sweep. F008 R33 INSTANCE, AND IT IS THIS FINDING'S OWN COUNTER-MEASURE GOING UNSERVED IN THE ROUND THAT OWED IT — BY THE REVIEWER, IN A CHANGE SET, RATHER THAN BY A WORKER. `apps/ui/src/components/panels/LiveStatusPill.tsx` documents its own optional prop with the sentence that `streamStatus` is optional because no caller holds one yet and that `useBrainStream` reaches the cockpit at R30 through RightLivePanel. F008 R33's C4, `a8965b2d`, is the commit that gave it a caller: `RemedyShell` now passes `streamStatus={stream.status}` to `RightLivePanel`, which passes it to the pill. Measured by the reviewer at `88c55f5d`: that comment sentence occurs 1x in the pill, `RemedyShell` is the only caller of `RightLivePanel` anywhere under `apps/ui/src` and `RightLivePanel` the only caller of the pill, so the comment denies a caller that the one call chain reaching it does contain — and its round number is wrong in the same breath, the wiring having landed at R33 rather than at the R30 the sentence predicts. WHY NO WORKER COULD FIX IT: the R33 block's change set named six paths and that file is not one of them, so its constraint 3 forbade the edit; the worker applied every slice byte for byte and declared no objection, correctly, because the defect is not in any slice. It is in the change set — the reviewer added the capability an existing comment called absent and did not owe itself the sweep this counter-measure has required since it was written. THE FIX IS THIS ROUND'S C4, which retires the claim at its source and names `a8965b2d` as the commit that falsified it, in the order constraint 2 of the R34 block fixes. WHAT THE CLASS NOW COSTS: this is the second feature in which a comment left standing by the commit that falsified it had to be found by a reader rather than by a gate, so the sweep is owed BY THE BLOCK THAT ADDS THE CAPABILITY, and a block that adds a caller for a prop, a caller for a module, or a first use of anything an existing comment calls absent names that comment's file in its own change set.
<<<END R0593TO

<<<SLICE LEDGER34
Gate: R34 — the R33 entry. R33 PASSED. It recorded the R32 verdict, amended R-0629 with a defect in the reviewer's own block text, and WIRED THE COCKPIT — `RemedyShell` now subscribes to its dashboard's job and hands the transport status to the badge R29 built — and EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs, the suites in the primary checkout and the red control in the reviewer's OWN disposable worktree, rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.agent/authored/f008-r33.md` at `7cb8b381` and `.agent/last_block.md` at `b6485523` are both sha256 a955dd3da8daa659104584fe479687128b071060240266d6daa53fd4fc43ca44 over 32437 bytes and 428 lines, EQUAL to the digest the reviewer emitted and under the 490-line budget DECISION F085 D6 rules. ELEVEN SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R33 a768146d at 39 lines, CONTRACT d13c2a38 at 90, SHSIGTO 9c39d503 at 7, SHIMPTO cc831ab7 at 3, and single-line slices for R0629FROM 836d856d, R0629TO 3e9f1830, LEDGER33 db6779e4, SHIMPFROM cd08d314, SHSIGFROM a88ea7bf, SHCALLFROM 85d765c3 and SHCALLTO 26ec012b — none carrying trailing whitespace on any line, none beginning with a blank line, and each newline-terminated. THE PLAN LANDED FIRST at `2befe139`, byte-equal to PLANF008R33 at 39 lines under the 50-line cap, with `## Goal` and `## Next Steps` once each and `F008` its first `\bF\d{3}\b` match. THE REWRITE at `cc40975f` reads R0629FROM 1 at the base and 0 at C2 with R0629TO 0 and 1, the base blob with that one substitution is BYTE-EQUAL to the C2 blob, and the blank-line paragraph count is 243 on both sides with EXACTLY ONE paragraph differing, index 234, beginning `- R-0629 — `. THE LEDGER APPEND at `f112538f` is proved twice over: the C2 blob is a byte-exact prefix of it with a 5470-byte remainder equal to a newline plus LEDGER33, and an INDEPENDENT split of the whole file gives 244 units whose LAST is LEDGER33's paragraph, with a one-byte printable flip REJECTED by BOTH readings and the unflipped value ACCEPTED by both. THE SETS HELD — 201 findings at the round base, at C2 and at C3 with NO id minted and R-0630 still 0, `- R-0368`, `- R-0429`, `- R-0553`, `- R-0622`, `- R-0628` and `- R-0629` 1 each and all OPEN, `Done:` 6, `Landed:` 0, `Gate: R` 32 at the base and at C2 and 33 at C3 over 33 DISTINCT keys, 32 of 33 headers matching the shape with `Gate: R1 — the F255 R21 entry.` the single non-match, and the R33 pair occurring exactly once. THE WIRING at `a8965b2d` carries three pairs in ONE commit and each is proved in the shape it owes: SHIMP and SHSIG are APPEND-shaped, their TOs containing their FROMs, so each FROM reads 1 at the base AND 1 at C4 while its TO goes 0 to 1 — a FROM-zero count being unattainable by construction there — and SHCALL is a REWRITE going 1 to 0 with its TO 0 to 1; covering all three at once, the base blob with SHIMP, SHSIG and SHCALL each substituted ONCE in that order is BYTE-EQUAL to the C4 blob, 2782 bytes and 50 lines becoming 3378 and 58. THE CONTRACT at `9ee1e9a9` is a CREATION — `git ls-tree 9f14a79e` printed a zero-byte output for that path — and its blob is sha256 d13c2a3849164b163dfc22e6acf8b8d1899133f5ce9cdad02e34cc8073336762 over 3855 bytes, byte-equal to the CONTRACT slice extracted from the committed C0a blob. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npm run --silent typecheck` EXITS 0 with a zero-byte output stream, `npx vitest run` EXITS 0 at 10 files and 152 tests, `python3 -m pytest tests/ui_contracts/ -q -rf` EXITS 0 at 417 passed plus 4 skipped = 421 where the base sum was 413 and CONTRACT's 8 tests are the difference, and the five-target state readers plus canary EXIT 0 at 465 passed plus 0 skipped. THE RED CONTROL DISCRIMINATES, measured by the reviewer in its own disposable worktree at `9ee1e9a9` with NO `node_modules` linked into it and the primary checkout never written to: the 29-byte target containing no backtick occurs EXACTLY ONCE as a substring while the count of LINES containing `streamStatus` is also 1 — the two numbers agreeing, which is the reading R-0629's widened fix asks for — deleting that one occurrence EXITS 1 at 1 failed and 7 passed, failing exactly `TestShellSubscribesToTheStream::test_shell_passes_the_stream_status_to_the_live_panel` and no other, and the restored file returns to sha256 9e6de55c and EXITS 0 at 8 passed, after which `git worktree list` named only the primary checkout and its porcelain read 0 lines. EIGHT single-parent commits over `9f14a79e`..`88c55f5d`, insertions 428, 299, 13, 1, 2, 9, 90 and 42 in commit order — every one under 500, 428 the maximum — with `git show --numstat` and `git diff --numstat` AGREEING for all eight and every cell equal to the `## Commits` column for the seven rows that table gives numbers for; the path set exactly the seven the Change set names; 0 marker lines in all six committed targets; 8 of 8 commits carrying `Co-Authored-By`; and an 83-line handback within the 100 eight commits allow. ONE FINDING, AND IT IS THE REVIEWER'S: registered against R-0593 rather than a new id after the open set was searched for the DEFECT (item 30), because the R33 change set omitted `apps/ui/src/components/panels/LiveStatusPill.tsx`, whose comment still denies the caller C4 gave it — the amendment is above and this round's C4 is the repair. NO FINDING IS REGISTERED AGAINST THE WORKER: every value it reported reproduced, including the three-way transport digest, all eleven slice digests and every count in G5 through G13.
<<<END LEDGER34

<<<SLICE PILLFROM
 *  `streamStatus` is optional because no caller holds one yet — `useBrainStream`
 *  reaches the cockpit at R30, through RightLivePanel. */
<<<END PILLFROM

<<<SLICE PILLTO
 *  `streamStatus` is optional because the pill outlived the rounds that had no
 *  transport to give it, not because nothing supplies one: at `a8965b2d`
 *  RemedyShell began passing a real status down the one chain that reaches
 *  this pill — RemedyShell to RightLivePanel to here — and at `88c55f5d` that
 *  was still the only chain either component had. */
<<<END PILLTO
