── STEP T003/8 — F008 SSE event stream — ROUND 29 ────────────────────────────
Round base — the SHA every range gate in this block measures from: 4afe1936
 (R28's handback, re-read from `git log` at emission, per R-0368.)
Goal:
 Record the R28 verdict, amend the OPEN finding R-0553 with the F008 R28
 instance, and put the DELAYED badge on a visible surface: `LiveStatusPill`
 learns the transport's status and says DELAYED or RECONNECTING instead of
 LIVE, with `RightLivePanel` passing it down and a `tests/ui_contracts/`
 source contract gating it — the acceptance condition the feature file states
 in its own words, the fallback "labels itself visibly ('delayed') instead of
 pretending to be live".

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r29.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R29, applied whole
 C1b  `.agent/decisions.md` <- DECISION2, appended
 C2a  `.agent/live_review.md` <- R0553FROM replaced by R0553TO, a REWRITE
 C2b  `.agent/live_review.md` <- LEDGER29, appended
 C3   the badge and its contract, one commit: `LiveStatusPill.tsx` <- PILL
      applied whole; `RightLivePanel.module.css` <- PILLCSS appended;
      `RightLivePanel.tsx` <- three pairs; `test_live_status_pill.py` <- PILLTEST
 C4   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r29.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/decisions.md`, `.agent/live_review.md`, `.agent/handoff.md`,
 `apps/ui/src/components/panels/LiveStatusPill.tsx`,
 `apps/ui/src/components/panels/RightLivePanel.module.css`,
 `apps/ui/src/components/panels/RightLivePanel.tsx`,
 `tests/ui_contracts/test_live_status_pill.py`.

Transport:
 This block is on disk at `.remedy-wt/f008-r29.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r29.md` for C0a. Never retype it. If
 the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are delimited by a line beginning `<<<SLICE <name>`
 and one beginning `<<<END <name>`; marker lines are NOT part of a slice. Every
 slice is newline-terminated with no trailing whitespace on any line, and every
 count this block orders over a slice is taken over those newline-INCLUDED
 bytes.

Pair shapes (§3 item 15). These lines are the OUTPUT of the reviewer's
containment test over the final newline-INCLUDED bytes, one reading per pair,
none generalised; each label is derived from the output beside it (R-0522):
 R0553FROM/R0553TO      TO contains FROM: false  -> REWRITE
 PANELIMPORTFROM/TO     TO contains FROM: true   -> APPEND
 PANELSIGFROM/TO        TO contains FROM: false  -> REWRITE
 PANELCALLFROM/TO       TO contains FROM: false  -> REWRITE
 R0553TO and PANELCALLTO both OPEN with their FROM's words and are rewrites
 anyway, each FROM being newline-TERMINATED where its TO continues that line —
 the eye reads append, the test reads rewrite, and the test decides.
 PANELIMPORT alone reads true, keeping the anchor import whole and adding a
 second beneath it: the append-shaped import pair R-0508 names.
 FROM uniqueness, counted by the reviewer's own script IN the named file at the
 round base and reported as its output (item 25): R0553FROM occurs 1x in
 `.agent/live_review.md`; PANELIMPORTFROM, PANELSIGFROM and PANELCALLFROM each
 occur 1x in `apps/ui/src/components/panels/RightLivePanel.tsx`.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23). C1b precedes C3 because
    DECISION2 rules the design C3 builds. C2a precedes C2b so each ledger
    proof reads against a single-purpose commit.
 3. Nothing outside the change set is touched. NO DEPENDENCY IS ADDED:
    `apps/ui/package.json` and `apps/ui/package-lock.json` are not opened.
    `RemedyApp.tsx` is NOT edited — R30's work; PILL and the panel signature
    both take `streamStatus` OPTIONAL so no caller lacking one must change.
 4. NO FINDING ID IS MINTED: R-0630 stays free. R-0553 is AMENDED, not
    resolved, and stays OPEN, as do R-0368, R-0622, R-0628 and R-0629. Write
    no `Done:` and no `Landed:` line for any of them. The reviewer searched the
    ledger for the DEFECT before routing it here (item 30): grepping the whole
    record at `fcea57b5` for `Co-Authored` and `trailer` returned ZERO lines,
    and R-0553's subject is this defect exactly.
 5. The post-C4 porcelain, `git worktree list` and push output belong to the
    ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 6. Two test processes never run at once. G10's COUNTING suites run in the
    PRIMARY checkout and never a worktree, a fresh worktree having neither
    `apps/ui/node_modules` nor `apps/ui/dist`, both of which move the counts
    (R-0518; the `dist` half the reviewer measured this round). G11's
    destructive proofs run ONLY in a disposable worktree, as protocol G5
    requires, so this clause does not bind them.
 7. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    reviewer's Phase 0 probe and nothing since has created one.
 8. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there, as R28 did;
    commit nothing from it.
 9. THE HANDBACK QUANTIFIES NOTHING IT DID NOT COUNT — the finding this round
    registers, so the round is bound by it. Any handback sentence stating
    "every", "no", "all" or "none" over commits, files or rounds names the
    command that produced the number; G12 orders the one such reading this
    round has cause to write. State the particular you measured, or nothing.

The reviewer's OWN readings, each produced by RUNNING the tool at the round
base `4afe1936` in the primary checkout, serially, not recalled (R-0625):
`npm run --silent typecheck` in `apps/ui` EXITS 0 with NO output; `npx vitest
run` EXITS 0 at 9 files and 137 tests; `python3 -m pytest tests/ui_contracts/
-q -rf` EXITS 0 at 402 passed plus 4 skipped = 406; G10's five-target state
reader EXITS 0 at 465 passed plus 0 skipped. `npm run lint` in `apps/ui` is RED
at base, which is R-0622 and NOT a gate (R-0364).
THE WHOLE OF C3 WAS DRY-RUN before this block was written, in a disposable
worktree at that base with `apps/ui/node_modules` and `apps/ui/dist` SYMLINKED
— never copied, `shutil.copytree` defaulting to `symlinks=False` and
dereferencing npm's bin shims (R-0591). Every C3 slice below is the byte string
that run applied, re-extracted from this block after its last edit. With C3 in
place that tree gives typecheck EXIT 0 silent and `tests/ui_contracts/` EXIT 0
at 409 passed plus 4 skipped = 413, the skipped SET identical to the base's
four ids, and both G11 proofs discriminate. The worktree was removed and pruned
before emission; `git worktree list` shows the primary checkout alone.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C1b, C2a, C2b and C3. Per constraint 5 the post-C4
     readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r29.md`
     as received, of `.agent/authored/f008-r29.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r29.md` with `git show`, by their marker lines, take
     the COUNT from that listing, and report it — this block states no numeral
     for it (item 11) — plus each slice's newline-INCLUDED sha256 prefix, bytes
     and lines, and that none carries trailing whitespace on any line.
 G4  Plan at C1 and decisions at C1b. Report the sha256, bytes and lines of
     `.agent/plan.md` at C1 and whether it is byte-equal to PLANF008R29; its
     line count is UNDER 50, `Steps` occurs, `## Goal` and `## Next Steps` each
     occur exactly once line-anchored and a `\bF\d{3}\b` match exists — the four
     properties `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about that file. Then
     `.agent/decisions.md` by the ordered equality an append owes: the
     round-base blob is a byte-exact PREFIX of the C1b blob and the remainder
     equals a newline plus DECISION2 — report its sha256 prefix, bytes and
     lines, plus `^## DECISION F008 D2 ` line-anchored 0 at the round base and
     1 at C1b and `^## DECISION F008 D1 ` 1 at both, so the append added a key
     rather than duplicating one (item 26).
 G5  The REWRITE at C2a. Read the base bytes with
     `git show 4afe1936:.agent/live_review.md` into scratch or memory — never
     by writing over the tracked file, which protocol G5 forbids (item 29).
     Report the count of R0553FROM at the round base (expected 1) and at C2a
     (expected 0), and of R0553TO at the base (expected 0) and at C2a
     (expected 1) — the FROM-0x / TO-1x proof a rewrite owes, over the
     newline-INCLUDED bytes the slice convention defines. Report also that the
     base blob with that substitution applied is BYTE-EQUAL to the C2a blob,
     the paragraph COUNT unchanged, and EXACTLY ONE paragraph differing, the
     one beginning `- R-0553 — `.
 G6  The append at C2b, against C2a, two ways that must agree. (a) the C2a blob
     is a byte-exact PREFIX of the C2b blob and the remainder equals a newline
     plus LEDGER29 — report its sha256 prefix, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2b file, terminating newline
     normalised first, has LEDGER29's paragraph as its LAST unit. NEGATIVE
     CONTROL: flip one PRINTABLE ASCII byte of the remainder to another
     printable one; BOTH readings must reject it and both accept the unflipped.
 G7  The sets, at C2a and C2b, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 201 at BOTH — this round mints no id — `^- R-0630 — `
     0 at both, `^- R-0553 — `, `^- R-0629 — `, `^- R-0628 — ` and
     `^- R-0368 — ` 1 each at both, `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0
     at both, `^Gate: R\d+ — ` 28 then 29 over that many DISTINCT keys. HEADER
     SWEEP at C2b (item 26): report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of each non-match to its first period,
     and that the R29 pair occurs EXACTLY ONCE.
 G8  The three RightLivePanel pairs at C3, each reported SEPARATELY. FROM count
     at the round base: 1 each. For PANELSIG and PANELCALL — the two whose
     containment test printed false — also the FROM count at C3 (0 each) and
     the TO count at C3 (1 each), the FROM-0x / TO-1x count a rewrite owes.
     For PANELIMPORT report the TO count at C3 (1) and NO FROM-0x reading: it
     is unattainable for an append by construction and none is ordered (§4.9,
     R-0522). Then report that the round-base blob with all three
     replacements applied in one pass is BYTE-EQUAL to the C3 blob, and the
     file's line count at both revisions.
 G9  The three other files C3 writes. `LiveStatusPill.tsx` at C3 is BYTE-EQUAL
     to PILL and `tests/ui_contracts/test_live_status_pill.py` at C3 is
     BYTE-EQUAL to PILLTEST — report both blobs' sha256 prefixes, bytes and
     lines. For `RightLivePanel.module.css`, the ORDERED EQUALITY a code append
     owes (R-0531): the round-base blob is a byte-exact PREFIX of the C3 blob,
     PILLCSS an exact SUFFIX of it, and the lines that commit's diff ADDS
     exactly PILLCSS's lines IN ORDER. No per-line count is ordered: CODE.
 G10 The suites, in the PRIMARY checkout, SERIALLY, never two test processes at
     once, at C3 — the commit at which every edited file is final. Report each
     one's passed and skipped numbers SEPARATELY as well as their sum, that
     split moving run to run so a bare passed count is never a gate:
     `npm run --silent typecheck` in `apps/ui` EXITS 0 with no output;
     `npx vitest run` in `apps/ui` EXITS 0 at 9 files and 137 tests, UNCHANGED,
     because no file vitest covers is touched;
     `python3 -m pytest tests/ui_contracts/ -q -rf` EXITS 0 at 413
     passed-plus-skipped, which is the base's 406 plus exactly the tests
     PILLTEST adds; report that reconciliation, not just the total; and
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     EXITS 0 at 465. If any fails, report the real values and STOP.
 G11 Both red proofs, ONLY inside a disposable `git worktree` at C3 with
     `apps/ui/node_modules` and `apps/ui/dist` SYMLINKED into it — never copied
     (R-0591) — and never in the primary checkout (protocol G5). Each byte
     string below the reviewer counted IN `LiveStatusPill.tsx` at the dry run,
     1x each; report YOUR OWN count before each mutation, and report the exit
     code AND the NAME of every failing test, never merely the colour (R-0327).
     (a) DELETE the three lines beginning `  if (streamStatus === "delayed") {`
         through the `  }` that closes it. EXPECT EXIT 1 naming BOTH
         `test_a_delayed_stream_says_delayed` and
         `test_the_transport_status_is_read_before_the_dashboard_liveness`.
     (b) REPLACE the byte string `/>RECONNECTING</div>` with `/>LIVE</div>`.
         EXPECT EXIT 1 naming `test_a_reconnecting_stream_says_so_rather_than_live`.
     Restore each byte-identically, confirm by digest, then report
     `python3 -m pytest tests/ui_contracts/test_live_status_pill.py -q` EXIT 0
     there. Remove and prune the worktree before the handback; report
     `git worktree list`.
 G12 The one quantifying reading constraint 9 binds, taken from a TOOL and not
     from the writer, because the finding this round registers is a sentence of
     exactly that shape written from memory. Run
     `git log --format=%H%x09%(trailers:key=Co-Authored-By,valueonly) 7c03adfa..C3`
     and report (i) how many commits it lists, (ii) how many return a NON-EMPTY
     trailer value, and (iii) the trailer value of each of this round's OWN
     commits. Whatever the handback then says about trailers, it says in those
     numbers. The reviewer's reading over `7c03adfa..4afe1936` was 180 commits
     with 19 non-empty; yours spans this round's too.
 G13 The range, measured from the round base this block's header names and from
     no other SHA. Report `git diff --name-only 4afe1936..C3` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly, none on either side
     alone; the full reading to C4 belongs to the ROUND REPORT (constraint 5).
     Report that every commit in the range has exactly ONE parent, and BOTH
     numstat cells per path from `git show --numstat`, cross-checked against
     `git diff --numstat`, every insertion under 500 and every cell equal to
     the `+/-` column of your `## Commits` table, cell by cell (item 28).
 G14 Marker leak and reflog. Count LINES BEGINNING with `<<<SLICE ` or `<<<END `
     in the plan at C1, the decisions file at C1b, the ledger at C2a and C2b,
     each of the four files C3 writes, and the handback at C4 — each is 0.
     `.agent/last_block.md` is NOT in that list and is not expected to be 0,
     being the block's own mirror. Then count THIS round's own reflog entries
     by the OPERATION before the first `:` in `%gs`: every pre-C4 entry reads
     `commit`; report how many you classified and `amend`, `rebase` and
     `cherry` at 0. Assert no total over the whole reflog (R-0601).
 G15 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 10
     names in that order, and an item-status table holding exactly one row for
     each of C0a, C0b, C1, C1b, C2a, C2b, C3 and C4 — "exactly one row"
     scoping to that TABLE. Measure its line count with `wc -l` BEFORE
     committing it; this round's commit count is above five, so the cap is 100,
     and an overage carries a DECISION D15 stated-cause line naming the real
     count and the mandated content that caused it. One line per gate here; raw
     transcripts go in the ROUND REPORT (R-0582).

Constraint 10 — THE HANDBACK'S `## Next` SECTION states, in this order: that
the next session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1)
and its SECOND the Open PR Gate (Phase 1 rule 2); that R29 is PENDING REVIEW
and its verdict is owed by the next round's ledger commit; that the next free
finding id is R-0630; that R-0368, R-0553, R-0622, R-0628 and R-0629 are OPEN;
and that R30's work is the real `BrainStreamHostDeps` factory over the T001 and
T002 endpoint plus wiring `useBrainStream` into `RemedyApp` and passing its
status down to the badge this round built — the round in which this feature's
two halves finally meet.

Handback: completion report + rewrite `.agent/handoff.md`, whose state block repeats verbatim:
 ~98 % (T001 ✅ · T002 ✅ · T003 Client ✅ + Badge ✅, Endpoint-Wiring offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R29
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
R29 records the R28 verdict, amends R-0553 with the F008 R28 instance — a
handback that corrected an unmeasured universal and wrote a fresh one in the
same sentence — and puts the DELAYED badge on a visible surface. The pill now
reads the transport's status ahead of the dashboard's liveness, so a client on
the polling fallback says DELAYED rather than LIVE, this feature's own
acceptance condition. `streamStatus` is optional on both the pill and the panel
because no caller holds one until R30.

## Next Steps
1. R30 builds the real `BrainStreamHostDeps` factory over the endpoint T001 and
   T002 shipped, wires `useBrainStream` into `RemedyApp` and passes its status
   down to the badge: the round in which this feature's two halves meet.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge reuses the pill's documented variant mechanism and an existing
  token, so no assumption_log entry is owed; DECISION F008 D2 in
  `.agent/decisions.md` records that reading and how to reverse it.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
<<<END PLANF008R29

<<<SLICE DECISION2

## DECISION F008 D2 — the delayed badge is a pill VARIANT, and the endpoint wiring is its own round (2026-08-21)

CHOSEN, two rulings the R29 block depends on.
1. DELAYED and RECONNECTING are VARIANTS of the existing `LiveStatusPill`, not
   a new visual language, so no assumption_log entry is owed. The design
   reference already gives this component variants — `component_spec.md` reads
   "LiveStatusPill (exists) — pulse dot; REPLAY variant (violet) for scrub
   state" — so a label swap plus an accent dot is the mechanism it documents.
   The accent `--remedy-orange-400` already exists in
   `apps/ui/src/styles/tokens.css` and in the reference's own `tokens.css`; no
   token, font, icon, glyph or asset source is added, leaving `assets_spec.md`
   untouched.
2. R29 ships the badge and R30 the wiring, where R28's handback proposed one
   round for both. `BrainStreamHostDeps` needs four real adapters —
   `openSource`, `readSnapshotSeq`, `readTail`, `schedule` — over the endpoint
   T001 and T002 built, and owes its own vitest tests. Bundling them would put
   a new transport adapter and a new visual surface in one diff, where a
   regression could not be attributed to the right half.

ALTERNATIVES REJECTED. An assumption_log entry anyway — no such file exists
here, so it would CREATE the register rather than append to it. A fourth
`BrainStreamStatus` member — rejected at R19, and R-0624 records why. A
REQUIRED `streamStatus` — `RemedyApp` holds none until R30, so it would force
callers to invent one.

CONSEQUENCE. The badge is reachable and gated at R29 while nothing yet supplies
a live value, which the pill's WHY comment states where a reader would look for
the absence. R30 then changes one prop at one call site.

Reverse ruling 1 by writing that assumption_log entry and citing this section
as the reading it overrides; ruling 2 by folding R30 back into one round.
<<<END DECISION2

<<<SLICE R0553FROM
at. Found and registered by the reviewer while gating R49.
<<<END R0553FROM

<<<SLICE R0553TO
at. Found and registered by the reviewer while gating R49. F008 R28 INSTANCE, IN A
WORKER'S HANDBACK RATHER THAN A REVIEWER'S SLICE, AND WRITTEN INSIDE THE VERY SENTENCE
THAT WAS CORRECTING THE SAME DEFECT. R28's `.agent/handoff.md` at `4afe1936` objected —
correctly, and the reviewer re-measured it — that R27's handback claimed "these seven
subjects carry a `Co-Authored-By: Claude Opus 5` trailer, as R26's did" while all seven
commits of `a86231c0..c768cf03` return an EMPTY trailer list. In the same breath it wrote
of its own six commits that they "carry NO `Co-Authored-By` trailer, as no commit on this
branch does". Measured at `4afe1936` over `7c03adfa..4afe1936`, 19 of this branch's 180
commits DO carry that trailer, among them all six of R26's — `b00a42f0`, `abef185b`,
`433e59eb`, `f683ab43`, `931ed066` and `a86231c0` — so the half of R27's sentence the
objection did not dispute was the TRUE half, and the correction shipped a fresh universal
nobody counted. THE PARTICULAR IS MEASURED AND TRUE: R28's own six commits carry no
trailer, which the reviewer confirms by the same command; only the clause beside it is
false, which is this finding's shape exactly and the R-0486 shape too — a correction is
where the next wrong claim lands. LOW: no gate consumed the sentence, every R28 gate is
reproducible and this reviewer reproduced all of them out of the committed blobs, and
`.agent/handoff.md` is rewritten every round, so the false clause is already off disk and
survives only in git history. THE FIX IS WIDENED FROM A REVIEWER'S SLICES TO THE HANDBACK,
which this counter-measure has never reached: it has bound authored slices since F085 and
binds nothing a worker writes, yet the handback is the map AGENTS.md's Session Resume tells
the next session to read SECOND. A handback sentence quantifying over commits, files or
rounds — "every", "no", "all", "as none does" — names the command that produced its number,
or states only the particular it measured. R29 carries that as constraint 9, gated at G12.
<<<END R0553TO

<<<SLICE LEDGER29
Gate: R29 — the R28 entry. R28 PASSED. It recorded the R27 verdict, amended R-0629 with the F008 R27 instance and changed no code, and EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.remedy-wt/f008-r28.md`, `.agent/authored/f008-r28.md` at `e301b8c3` and `.agent/last_block.md` at `234a4e94` are all sha256 a7ad435632c7e37a69f77b314509722b1e1cf347a8acb2cc25f89007f94b33b5 over 19687 bytes and 228 lines, equal to the digest the reviewer emitted. FOUR SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R28 23eed56c at 39 lines, R0629FROM 64428337, R0629TO f6653cda and LEDGER28 c64702c1 at 1 line each — none carrying trailing whitespace on any line. THE PLAN LANDED FIRST at `4d766cf4`, byte-equal at 39 lines under the 50-line cap, with `## Goal` and `## Next Steps` once each. THE REWRITE at `1cf2280b` IS PROVED ON THE UNIT ITS OWN BLOCK DEFINED, and that distinction is the whole reading: the block's slice convention makes a slice its newline-TERMINATED bytes, its containment test printed false on those bytes, and on those bytes R0629FROM counts 1 then 0 and R0629TO 0 then 1 — the FROM-0x/TO-1x count a rewrite owes. Counted newline-STRIPPED the same FROM reads 1 at BOTH revisions, because R0629TO opens with R0629FROM's words; the reviewer measured both readings and the handback's numbers are correct under the one the block states, which is what R-0437 asks a pair shape to declare. Independently, the base blob with that one substitution applied is BYTE-EQUAL to the C2a blob, with 238 blank-line paragraphs before and after, exactly ONE differing, and that one the `- R-0629 — ` paragraph at index 234. THE APPEND at `fcea57b5` is a byte-exact prefix of the C2a blob plus a 3856-byte remainder equal to a newline plus LEDGER28, agreed by an INDEPENDENT split of the whole file into 239 units whose LAST is LEDGER28's paragraph, with a one-byte printable flip REJECTED by BOTH readings and the unflipped accepted by both. THE SETS HELD — findings 201 at both revisions with NO id minted, `- R-0630` 0, `- R-0629`, `- R-0628` and `- R-0368` 1 each and all OPEN, `Done:` 6, `Landed:` 0, `Gate: R` 28 to 29 over that many DISTINCT keys, twenty-seven of twenty-eight headers matching the shape with `Gate: R1 — the F255 R21 entry.` the single non-match, and the R28 pair occurring exactly once. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout at `fcea57b5`: the five-target state-reader command EXITS 0 at 465 passed and 0 skipped, and `tests/ui_contracts/` EXITS 0 at 402 passed plus 4 skipped. SIX single-parent commits; the numstat cells 228/0, 129/295, 11/12, 1/1 and 2/0 each equal to the `## Commits` column cell by cell, every insertion under 500; zero marker lines in the plan, the ledger at both commits and the handback; six reflog operations all `commit` with amend, rebase and cherry at 0; a 68-line handback within the 100 six commits allow; the tree clean and the primary checkout the only worktree. THE ROUND'S OBJECTION WAS SOUND AND IS WHY THIS ENTRY IS NOT UNQUALIFIED: R28 declined to edit LEDGER28 as constraint 1 required, applied it byte for byte and objected in its deviations that R27's handback had claimed a `Co-Authored-By` trailer on seven commits that carry none. The reviewer re-measured and confirms it. The objection's own closing clause then asserted that no commit on this branch carries that trailer, and 19 of 180 do — registered above against R-0553, Low, and the reason R29's block gates the reading by command.
<<<END LEDGER29

<<<SLICE PILL
import type { BrainStreamStatus } from "../../api/brainStream";
import styles from "./RightLivePanel.module.css";

/** The cockpit's one honest word about its own freshness, and why the
 *  TRANSPORT's status outranks the dashboard's: a client on the polling
 *  fallback is NOT live however active the job is, and saying so plainly is
 *  this feature's acceptance condition (T5_F008 — the fallback "labels itself
 *  visibly ('delayed') instead of pretending to be live"). That is also why
 *  the dashboard arm is LAST: it is the fallback, not the rule.
 *
 *  `streamStatus` is optional because no caller holds one yet — `useBrainStream`
 *  reaches the cockpit at R30, through RightLivePanel. */
export function LiveStatusPill({ live, streamStatus }: { live: boolean; streamStatus?: BrainStreamStatus | null }) {
  if (streamStatus === "delayed") {
    return <div className={styles.livePill} data-state="delayed"><span className={styles.delayedDot} />DELAYED</div>;
  }
  if (streamStatus === "reconnecting") {
    return <div className={styles.livePill} data-state="reconnecting"><span className={styles.reconnectingDot} />RECONNECTING</div>;
  }
  return <div className={styles.livePill} data-state={live ? "live" : "idle"}><span className={live ? styles.liveDot : styles.idleDot} />{live ? "LIVE" : "IDLE"}</div>;
}
<<<END PILL

<<<SLICE PILLCSS
.delayedDot { width: 9px; height: 9px; border-radius: 50%; background: var(--remedy-orange-400); box-shadow: 0 0 8px rgba(245,163,78,.6); }
.reconnectingDot { width: 9px; height: 9px; border-radius: 50%; background: var(--remedy-orange-400); opacity: .55; }
<<<END PILLCSS

<<<SLICE PANELIMPORTFROM
import type { RemedyDashboard } from "../../api/types";
<<<END PANELIMPORTFROM

<<<SLICE PANELIMPORTTO
import type { RemedyDashboard } from "../../api/types";
import type { BrainStreamStatus } from "../../api/brainStream";
<<<END PANELIMPORTTO

<<<SLICE PANELSIGFROM
export function RightLivePanel({ dashboard, onSelectNode }: { dashboard: RemedyDashboard; onSelectNode: (nodeId: string | null) => void }) {
<<<END PANELSIGFROM

<<<SLICE PANELSIGTO
export function RightLivePanel({ dashboard, onSelectNode, streamStatus }: { dashboard: RemedyDashboard; onSelectNode: (nodeId: string | null) => void; streamStatus?: BrainStreamStatus | null }) {
<<<END PANELSIGTO

<<<SLICE PANELCALLFROM
      <LiveStatusPill live={liveIsActive(dashboard)} />
<<<END PANELCALLFROM

<<<SLICE PANELCALLTO
      <LiveStatusPill live={liveIsActive(dashboard)} streamStatus={streamStatus} />
<<<END PANELCALLTO

<<<SLICE PILLTEST
"""Contract tests for the LiveStatusPill's transport-status variants.

The pill is the surface this feature's acceptance condition names: the polling
fallback must label itself visibly instead of pretending to be live. There is no
DOM environment here, so the pill is gated as every other component is — by
reading its COMMENT-STRIPPED source, since a guard counting a token inside a
comment is satisfied by the prose describing the code rather than by the code
(R-0584). The stripper is the hook contract's, so the concept is spelled once.
"""
from __future__ import annotations

from pathlib import Path

from .test_brain_stream_hook import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PANELS = REPO_ROOT / "apps" / "ui" / "src" / "components" / "panels"
PILL = PANELS / "LiveStatusPill.tsx"
PANEL = PANELS / "RightLivePanel.tsx"
PANEL_CSS = PANELS / "RightLivePanel.module.css"


class TestLiveStatusPillVariants:
    def test_a_delayed_stream_says_delayed(self):
        code = strip_ts_comments(PILL.read_text())
        assert '"DELAYED"' not in code, "the label is rendered text, not a string prop"
        assert "DELAYED" in code, "the fallback must label itself visibly"
        assert 'streamStatus === "delayed"' in code, "DELAYED is reached by the transport status"

    def test_a_reconnecting_stream_says_so_rather_than_live(self):
        code = strip_ts_comments(PILL.read_text())
        assert "RECONNECTING" in code
        assert 'streamStatus === "reconnecting"' in code

    def test_the_transport_status_is_read_before_the_dashboard_liveness(self):
        code = strip_ts_comments(PILL.read_text())
        delayed = code.index('streamStatus === "delayed"')
        dashboard = code.index("liveDot")
        assert delayed < dashboard, "a delayed client must not fall through to LIVE"

    def test_the_pill_still_reports_the_dashboard_liveness(self):
        code = strip_ts_comments(PILL.read_text())
        assert "LIVE" in code and "IDLE" in code, "the fallback arm must survive"

    def test_each_variant_lights_its_own_dot(self):
        css = PANEL_CSS.read_text()
        assert ".delayedDot" in css, "DELAYED needs a dot rule or it renders unstyled"
        assert ".reconnectingDot" in css


class TestRightLivePanelPassesTheStatusDown:
    def test_the_panel_hands_the_pill_a_stream_status(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "streamStatus={streamStatus}" in code, "or the pill can never see one"

    def test_the_panel_accepts_the_status_from_its_own_caller(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "streamStatus?: BrainStreamStatus | null" in code
<<<END PILLTEST
