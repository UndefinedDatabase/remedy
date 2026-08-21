── STEP R15/1 — F008 SSE event stream · T002 PAYDOWN ──────────
Goal:        Pay down T002's two authored defects instead of only recording
             them. R-0620: `resolve_sse_start` guards with `str(x or "")`, so
             the INTEGER 0 — the first ledger position — is read as an absent
             header and falls through to the cursor, which is the opposite of
             what the same function's docstring promises. The guard becomes an
             explicit None test and three tests pin the integer forms.
             R-0621: the grown-ledger test started its second client from
             scratch, so the boundary its name promised was never crossed by a
             resume; the hammer helper gains a starting last-event-id and the
             test is rewritten to resume ACROSS the growth. R15 also records
             the R14 verdict (PASS) and widens R-0371 a third time.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 widen R-0371 · C3 register R-0621 and record the R14 verdict ·
             C4 fix the resume guard · C5 repair the grown-ledger test ·
             C6 pin the integer header forms · C7 the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r15.md        (C0a, new)
             - .agent/last_block.md               (C0b, rewrite)
             - .agent/plan.md                     (C1, rewrite)
             - .agent/live_review.md              (C2 pair, C3 append)
             - packages/orchestration/ui_server.py (C4, pair)
             - tests/ui_server/test_sse_stream.py (C5 pairs, C6 append)
             - .agent/handoff.md                  (C7, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r15.md, extracted by its marker lines — never
    retyped, rewrapped, reflowed or edited. Each FROM occurs EXACTLY ONCE in
    its target at the commit named below; if one does not, stop and say so
    rather than choosing an occurrence. A slice that looks wrong is APPLIED AS
    WRITTEN and the objection goes in the handback. Each of your last three
    rounds caught a real reviewer defect exactly that way, and two of them are
    what this round exists to fix — keep doing it.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines strictly
    between its `<<<SLICE X` and `<<<END X` markers. PLANF008R15 is applied
    with its trailing newline INCLUDED and is the ENTIRE content of its file.
    R0371FROM and R0371TO are each ONE line with its trailing newline,
    replaced in place, changing no other byte, so `.agent/live_review.md` has
    the SAME line count at C2 as at C1. LEDGER15 is a newline plus its body,
    appended after exactly one blank line. TESTS15 is appended to the test
    file after exactly TWO blank lines — PEP 8 for a top-level definition, and
    NOT a property this repository's ruff will catch, E301-E306 being
    preview-only rules that are not enabled here, so G10 gates those blank
    lines as bytes. Every file ends with exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5, C6, C7.
    `.agent/plan.md` advances at C1, ahead of both ledger commits (§3 item
    23). C2 and C3 stay SEPARATE: C2 edits a line in place and C3 appends, and
    that separation is what lets G5 prove the edit constructively and G6 prove
    the append as a byte prefix. C4 precedes C6 because the tests C6 adds FAIL
    without C4's fix — that is this round's red proof, and inverting the order
    would land a knowingly red commit.
 4. LEDGER15 carries TWO paragraphs, blank-line separated, applied together in
    C3: the R-0621 registration and the `Gate: R15` entry holding the R14
    verdict. R-0621 is the only id minted, so the next free id becomes R-0622.
    R-0371 is WIDENED, not re-registered: §3 item 30 forbids a second id for a
    defect the open set already describes, and this is its third instance.
 5. SCOPE. The only production change is the ONE line of `resolve_sse_start`
    that FIXFROM names. No other behaviour changes, no new endpoint, no client
    code, no docs. T003 is the next round's work and any POST surface belongs
    to the next feature.
 6. `git status --porcelain` is empty after each of C0a through C6, and
    `git worktree list` names the primary checkout alone once G9's worktree is
    removed. READINGS OF STATE AT OR AFTER C7 GO IN THE ROUND REPORT, NEVER IN
    THE HANDBACK FILE: the tree state after the handback commit cannot be
    recorded inside that commit, and a gate that orders it anyway is finding
    R-0371, whose third instance this round's own C2 registers. Base bytes
    reach a tool by `git show <sha>:<path>` or a disposable worktree under the
    gitignored `.remedy-wt/`, never by overwrite-and-restore in the primary
    checkout (self_drive_protocol G5).
 7. Two pytest processes never run at once, and G8's counting suites run in
    the PRIMARY checkout — a fresh worktree has no `apps/ui/node_modules` and
    its pass counts are untrustworthy in both directions (R-0518).
 8. The reviewer's own readings at `305bc30c`, RE-DERIVED by the gates below
    rather than trusted: `tests/ui_server/test_sse_stream.py` exits 0 at 62,
    the combined state-reader suite exits 0 at 462, `tests/docs/` exits 0 at
    295. Count by passed-plus-skipped, never by a bare passed count.
 9. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. T003 is
    unbuilt, so the branch is not closeable. It is pushed and left open.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     each of C0a through C6. Report each reading. Per constraint 6 the
     post-C7 porcelain and the final `git worktree list` belong to the ROUND
     REPORT, not to `.agent/handoff.md`.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block the worker was given, of `.agent/authored/f008-r15.md` at C0a and
     of `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r15.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256, bytes and
     lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R15. Its line count is under 50,
     `## Goal` and `## Next Steps` each occur exactly once line-anchored, and
     `F008` occurs at least once.
 G5  The R-0371 widening, proved CONSTRUCTIVELY. Report that R0371FROM occurs
     EXACTLY ONCE in `.agent/live_review.md` at C1, replace that one
     occurrence with R0371TO, and report whether the result is BYTE-EQUAL to
     that file at C2, giving both sha256s. Report the LINE COUNT at C1 and at
     C2: they are EQUAL. Report that `- R-0371 — ` occurs exactly once at C2
     and that the line ENDS with ` OPEN.`
 G6  The ledger append, C3 against C2, two ways that must agree. (a) the C2
     blob is a byte-exact PREFIX of the C3 blob and the remainder equals a
     newline plus LEDGER15 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the C3 file, its terminating newline
     normalised first, has as its LAST TWO units, in order, the two paragraphs
     of LEDGER15. NEGATIVE CONTROL: flip one byte of the remainder and report
     BOTH readings reject it, the unflipped accepted by both.
 G7  The sets, at THREE commits. Report line-anchored counts in
     `.agent/live_review.md` at C1, C2 and C3: `^- R-\d+ — ` reads 192, 192,
     193 — C2 edits and only C3 mints — `^Done: R-\d+ — ` is 0 at all three,
     `^Landed: ` is 0 at all three, `^Gate: R\d+ — ` reads 14, 14, 15 with the
     fifteen keys DISTINCT, `^- R-0621 — ` reads 0, 0, 1 and `^- R-0622 — ` is
     0 at all three. Report that LEDGER15's `Gate:` header matches the shape
     of the entries already in the file, as a pattern match over
     `^Gate: R(\d+) — the R(\d+) entry\.` requiring the second number to be
     one less than the first and the R15 pair to occur exactly once (§3 item
     26). Report the number of `^Gate: ` lines that do NOT match; it is 1, and
     that line is `Gate: R1 — the F255 R21 entry.`
 G8  The code pairs, proved CONSTRUCTIVELY and not counted. From the
     `305bc30c` blob of `packages/orchestration/ui_server.py`, verify FIXFROM
     occurs EXACTLY ONCE, replace it with FIXTO, and report whether the result
     is BYTE-EQUAL to that file's blob at C4. From the `305bc30c` blob of
     `tests/ui_server/test_sse_stream.py`, verify HAMMERFROM and GROWFROM each
     occur EXACTLY ONCE, replace each with its TO, and report whether the
     result is BYTE-EQUAL to that file's blob at C5. Report the sha256 of both
     sides of both comparisons.
 G9  The suites are green in the PRIMARY checkout, run SERIALLY, never two
     pytest processes at once. Report the exit code and `passed + skipped` of
     each, at C6:
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf` exits 0.
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf` exits 0.
     `python3 -m pytest tests/docs/ -q -rf` exits 0 and sums to 295.
     RECONCILE THE ARITHMETIC RATHER THAN ASSERTING A BARE TOTAL: report the
     number of lines matching `^    def test_` in TESTS15, and report that the
     first sum equals 62 plus that number and the second equals 462 plus the
     same number, 62 and 462 being constraint 8's base readings. If any of the
     three identities fails, report the real values and stop.
 G10 The test append. Report that the C5 blob of
     `tests/ui_server/test_sse_stream.py` is a byte-exact PREFIX of the C6
     blob and that the remainder is TWO newlines followed by TESTS15 — two,
     not one, that being constraint 2's blank-line rule measured as bytes.
     Report that the lines `git diff C5..C6 -- <that path>` ADDS are the two
     blank lines followed by TESTS15's lines IN ORDER, that the added-line
     count equals TESTS15's line count plus two, and that the diff REMOVES
     nothing.
 G11 RED PROOF — the colour, never a count. The tests C6 adds exist to pin the
     defect C4 fixes, so they MUST fail without it. In a DISPOSABLE worktree
     under `.remedy-wt/`, created with `git worktree add --detach` at C6 and
     removed before the handback: write the `305bc30c` blob of
     `packages/orchestration/ui_server.py` into that worktree's copy with
     `git show`, leaving the tests at C6, and report the exit code of
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf -k ResumeStartTypes`
     run THERE. It EXITS NON-ZERO. Report which tests failed; two of the three
     SURVIVE by design, because a string header and an absent header already
     behaved correctly and only the integer-zero case was broken. Then restore
     the file to its C4 blob and report that the same command EXITS 0.
 G12 MUTATION CONTROL — the repaired grown-ledger test must still have teeth.
     In the SAME disposable worktree, replace `        return int(text) + 1`
     with `        return int(text)` in that worktree's copy of
     `packages/orchestration/ui_server.py` and report the exit code of
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf -k DisconnectHammer`.
     It EXITS NON-ZERO and the failures INCLUDE
     `test_a_resume_crosses_a_ledger_that_grew_between_connections`. Restore
     and report EXIT 0. A repaired test that stopped failing under the
     mutation would have been repaired into a tautology.
 G13 Ruff, scoped to the two touched files, compared as a MULTISET of rule
     codes and NEVER as an exit code, base against head, in BOTH the default
     configuration and under `--preview`. Run
     `python3 -m ruff check --output-format concise` over the two paths at C6
     and over the SAME two paths at `305bc30c` by feeding each base blob
     through `git show 305bc30c:<path> | python3 -m ruff check --output-format concise --stdin-filename <path> -`
     so `per-file-ignores` resolves by path and no file is overwritten (§3
     item 29); then repeat both sides with `--preview` added. Report all four
     multisets. The default pair is EQUAL and both EMPTY. The preview pair is
     EQUAL at `{'E306': 3}` — those three are PRE-EXISTING in
     `packages/orchestration/ui_server.py` and this round neither adds nor
     removes one, so the preview side EXITS NON-ZERO on both sides and that
     exit code is NOT the gate; equality of the multisets is. CONTROL, through
     the SAME extractor: feed a deliberately unused import to ruff on stdin
     and report a NON-EMPTY multiset at a non-zero exit (R-0463).
 G14 Range, and NOT self-referential. With BASE `305bc30c`,
     `git diff --name-only BASE..C6` equals the Change list above MINUS
     `.agent/handoff.md`, with no path on either side alone. The full
     `BASE..C7` reading belongs to the ROUND REPORT (constraint 6). Every
     commit in BASE..C7 has exactly one parent. For every commit BEFORE C7
     report BOTH numstat figures per path — insertions AND deletions — from
     `git show --numstat`, report that every insertion count is under 500, and
     compare EVERY CELL against the `+/-` column of the handback's
     `## Commits` table, both sides read from `git diff --numstat`. Both
     cells, not the insertion alone: that half-width reading is R-0619.
 G15 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C3,
     `packages/orchestration/ui_server.py` at C4,
     `tests/ui_server/test_sse_stream.py` at C6 and `.agent/handoff.md` at C7.
     Every count is 0.
 G16 History, push and handback. Over this round's OWN reflog entries report
     the count whose OPERATION — the text before the first `:` in
     `git reflog --format=%gs` — is `amend`, `rebase` or `cherry`; it is 0,
     counted by operation and never by substring, with no total asserted.
     Report the real output of `git push` and of
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
     which returns an empty list; nothing is merged. `.agent/handoff.md` at C7
     carries the sections docs/agents/handback_template.md mandates and an
     item-status table naming C0a, C0b, C1, C2, C3, C4, C5, C6 and C7 exactly
     once each; report its line count, the cap being 100 for a round of more
     than five commits, an overage carrying a DECISION D15 stated-cause line.
     Its `## Next` section states that the next session's FIRST action is the
     `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the Open PR Gate
     (Phase 1 rule 2), that R15 IS PENDING REVIEW and its verdict is owed by
     the next round's ledger commit, and that R16's work is T003's client
     hook.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 68 % (F008 beansprucht · fuenfzehn Urteile im Ledger ·
            T001 KOMPLETT · T002 KOMPLETT und abbezahlt: Resume-Entscheidung,
            Trennungs-Hammer, und in R15 die beiden selbst gefundenen Defekte
            R-0620 und R-0621 wirklich behoben statt nur notiert · T003
            Client-Hook, Backoff, Lueckenerkennung und Polling-Fallback ab R16
            · danach das Integrationstor) — Schaetzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R15
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map; this file repeats
none of them.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat, and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the client transcript byte-equals the
ledger's envelope sequence, the heartbeat holds cadence, and the fallback
engages on a disabled EventSource and recovers to live.

## Current Step
R15 PAYS DOWN T002's two authored defects rather than only recording them.
R-0620: `resolve_sse_start` guarded with `str(x or "")`, which reads the
integer 0 — the first ledger position — as an absent header; the guard becomes
an explicit None test and three tests pin the integer forms. R-0621: the
grown-ledger test started its second client from scratch, so the boundary its
name promised was never crossed by a resume; the hammer helper now accepts a
starting last-event-id and the test resumes across the growth. R15 also
records the R14 verdict and widens R-0371 a third time.

## Next Steps
1. R16 begins T003: the `useBrainStream` client hook, EventSource with
   reconnect backoff, gap detection via seq discontinuity, and the status
   surface live | reconnecting | delayed.
2. R17 adds T003's polling fallback on the same hook interface and the
   fixture live-job end-to-end.
3. Then the integration gate before closure.

## Risks
- The hammer drives `_send_sse_stream` directly rather than over a socket, so
  it proves the resume CONTRACT and not the transport. The transport stays
  covered by the framing golden and the drain tests.
- Repository-wide `ruff check .` is RED and is not a gate (R-0364), and
  `--preview` reports three pre-existing E306 in
  `packages/orchestration/ui_server.py`. Ruff is gated scoped to the touched
  files as a rule-code MULTISET, base against head, so a pre-existing finding
  is never read as a new one.
- No open finding is a code defect of F008 reachable from the HTTP path.
  R-0403, R-0607 through R-0609, R-0611 and R-0613 through R-0621 stay routed
  to a paydown branch, R-0620 and R-0621 being closed by this round's own
  commits.
<<<END PLANF008R15

<<<SLICE R0371FROM
- R-0371 — Low — a block ordered a value that cannot exist at the moment the text carrying it is written. The R5 block told the worker to append to `.agent/live_review.md` "a single line of your own of exactly this shape, with your real commit SHA: `Landed: R-0370 — <one line: what changed, which commit>`" and, six lines later, that "that live_review.md edit belongs to C2, the same commit as the test". A commit's SHA is a hash over a tree that already contains every byte of that commit, so a line inside C2 can never name C2. No correct application of the bundle could satisfy both clauses. The worker was right to declare the deviation, name the commit by its role — "R5's C2, the same commit as this line, whose SHA the handback reports" — and let the handback carry the real value `a01e8a9712aead26eb88888db352d0bb72492cb9`; nothing was fabricated and nothing was edited toward a number. This is the seventh reviewer-gate defect of this feature, after R-0363's unmeasured block length, R-0364's unexecuted ruff gate, R-0367's unreachable numstat, R-0368's wrong-base range gate and R-0369's self-counting string gate, and it is a class none of their counter-measures reach: R-0364 makes the reviewer EXECUTE every gate it orders, but a self-referential SHA is not a gate at all — it is appliable CONTENT whose required value the act of applying it destroys, so there is nothing for the reviewer to execute in advance. `docs/agents/planner_reviewer_prompt.md` §4 item 4 supplies the template verbatim, including the words "which commit", and the template is fine; the defect is pairing it with "your real commit SHA" and "the same commit as the test". Counter-measure, binding from R6 on and additive to all of the above: before ordering any text to be written into a file, the reviewer checks that every value that text must contain already exists at the moment of writing. Commit SHAs, `git show --numstat` outputs and every other post-hoc measurement are ordered into the HANDBACK, which is written after the commits exist, and never into the committed text itself; where a committed line must identify its own commit it names it by its ROLE in the bundle. SECOND INSTANCE, F008 R13, and it lands inside this counter-measure's own escape hatch. The counter-measure routes every post-hoc measurement "into the HANDBACK, which is written after the commits exist" — but the handback IS a commit in the range, so a reading over a range that INCLUDES the handback commit is still unwritable at the moment that file is written. R13's G12 ordered `git diff --name-only BASE..C6` where C6 is the handback commit itself, and the Change list it had to equal contains `.agent/handoff.md`: no pre-C6 reading could match it and no post-C6 reading could be placed inside C6. The worker declared the impossibility rather than fudging it, put the pre-C6 reading in the file and the full BASE..C6 reading in the round report — the R-0149 carve-out applied by hand to a clause that never named it. THE NEAR MISS IS THE INSTRUCTIVE PART: R13's G12 did name that carve-out, but only for the numstat half of the gate ("C6's own numbers belong to the round report") and not for the name-only half three sentences earlier, so one reviewer sentence knew the rule while its neighbour did not. COUNTER-MEASURE WIDENED: a range gate whose range ends at the handback commit either states the carve-out for EVERY reading it orders, or ends its range at the commit BEFORE the handback and names the handback's own path separately. OPEN.
<<<END R0371FROM

<<<SLICE R0371TO
- R-0371 — Low — a block ordered a value that cannot exist at the moment the text carrying it is written. The R5 block told the worker to append to `.agent/live_review.md` "a single line of your own of exactly this shape, with your real commit SHA: `Landed: R-0370 — <one line: what changed, which commit>`" and, six lines later, that "that live_review.md edit belongs to C2, the same commit as the test". A commit's SHA is a hash over a tree that already contains every byte of that commit, so a line inside C2 can never name C2. No correct application of the bundle could satisfy both clauses. The worker was right to declare the deviation, name the commit by its role — "R5's C2, the same commit as this line, whose SHA the handback reports" — and let the handback carry the real value `a01e8a9712aead26eb88888db352d0bb72492cb9`; nothing was fabricated and nothing was edited toward a number. This is the seventh reviewer-gate defect of this feature, after R-0363's unmeasured block length, R-0364's unexecuted ruff gate, R-0367's unreachable numstat, R-0368's wrong-base range gate and R-0369's self-counting string gate, and it is a class none of their counter-measures reach: R-0364 makes the reviewer EXECUTE every gate it orders, but a self-referential SHA is not a gate at all — it is appliable CONTENT whose required value the act of applying it destroys, so there is nothing for the reviewer to execute in advance. `docs/agents/planner_reviewer_prompt.md` §4 item 4 supplies the template verbatim, including the words "which commit", and the template is fine; the defect is pairing it with "your real commit SHA" and "the same commit as the test". Counter-measure, binding from R6 on and additive to all of the above: before ordering any text to be written into a file, the reviewer checks that every value that text must contain already exists at the moment of writing. Commit SHAs, `git show --numstat` outputs and every other post-hoc measurement are ordered into the HANDBACK, which is written after the commits exist, and never into the committed text itself; where a committed line must identify its own commit it names it by its ROLE in the bundle. SECOND INSTANCE, F008 R13, and it lands inside this counter-measure's own escape hatch. The counter-measure routes every post-hoc measurement "into the HANDBACK, which is written after the commits exist" — but the handback IS a commit in the range, so a reading over a range that INCLUDES the handback commit is still unwritable at the moment that file is written. R13's G12 ordered `git diff --name-only BASE..C6` where C6 is the handback commit itself, and the Change list it had to equal contains `.agent/handoff.md`: no pre-C6 reading could match it and no post-C6 reading could be placed inside C6. The worker declared the impossibility rather than fudging it, put the pre-C6 reading in the file and the full BASE..C6 reading in the round report — the R-0149 carve-out applied by hand to a clause that never named it. THE NEAR MISS IS THE INSTRUCTIVE PART: R13's G12 did name that carve-out, but only for the numstat half of the gate ("C6's own numbers belong to the round report") and not for the name-only half three sentences earlier, so one reviewer sentence knew the rule while its neighbour did not. COUNTER-MEASURE WIDENED: a range gate whose range ends at the handback commit either states the carve-out for EVERY reading it orders, or ends its range at the commit BEFORE the handback and names the handback's own path separately. THIRD INSTANCE, F008 R14 — and it is inside the very round that wrote the widening above, which is the proof the widening was too narrow. That R14 block's G1 ordered `git status --porcelain` to be empty "after every commit AND AT THE HANDBACK". Neither half can be recorded where it was ordered: the state after C5 cannot appear inside C5, and at the instant `handoff.md` is written the tree necessarily holds an uncommitted file, so the honest reading at that moment is not empty at all. The widening one sentence earlier reached only "a range gate whose range ends at the handback commit", and G1 is a HYGIENE gate rather than a range gate, so the counter-measure written to stop this defect failed to cover the next instance of it in its own block. The worker declared it and applied the R-0149 carve-out by hand for the third round running. COUNTER-MEASURE WIDENED AGAIN, this time by the PROPERTY instead of by the gate's genre, which is why the first two attempts kept missing: ANY clause ordering a reading of repository state at or after the handback commit — a range, a porcelain status, a worktree list, a reflog, a push result — names where that reading lands, and the default landing place is the ROUND REPORT and never the handback file. A gate is not exempt because it is short, and a counter-measure scoped to one genre of gate will be evaded by the next genre. OPEN.
<<<END R0371TO

<<<SLICE LEDGER15
- R-0621 — Low — A TEST NAMED FOR A PROPERTY ITS BODY NEVER EXERCISES, IN THE ROUND THAT EXISTED TO PROVE THAT PROPERTY. `test_a_ledger_that_grows_between_connections_still_arrives_whole`, the TESTS14 slice of the F008 R14 block authored by the reviewer and applied byte for byte at `3c758702`, drives one client over a six-event ledger, extends the ledger to ten, and then calls `_hammer` a SECOND time — but that second call takes no starting last-event-id, so it begins with `last_event_id = None`, resolves to position 0 and replays the grown ledger from the beginning. The growth boundary is therefore never crossed by a resume, which is the one thing the test's name promises. RE-MEASURED BY THE REVIEWER, not read: wrapping `resolve_sse_start` in a spy and running the test body prints the second client's resolve calls as `(None, '0', 0)`, `('2', '0', 3)`, `('5', '0', 6)`, `('8', '0', 9)` — the FIRST is the giveaway, a fresh start rather than a resume from the id `first` kept. WHY IT IS ONLY LOW: the test is not vacuous. Its later reconnects do exercise resume, so it fails under both of the mutations G10 applies, and the property it actually proves — a grown ledger arrives whole — is worth having. The defect is that a reader trusts the NAME, and the name claims coverage of the resume-across-growth case that nothing in the suite then holds. THE FIX, applied by this round rather than deferred: `_hammer` gains a `last_event_id` parameter so a caller can hand it a client that already holds part of the ledger, and the test is renamed `test_a_resume_crosses_a_ledger_that_grew_between_connections` and asserts the second client receives exactly ids 2 through 9 — no duplicate of 1, no gap at 6 — with the two transcripts concatenated byte-equal to the whole ledger. FOUND BY THE WORKER, which applied the slice unedited as constraint 1 required and declared the mismatch; that is the third consecutive round in which a worker's declaration, not a gate, is what put a reviewer-authored defect on the record, and the second in which the defect was invisible to every gate because the gates compared bytes and the bytes were exactly what the reviewer wrote.

Gate: R15 — the R14 entry. R14 PASSED. Its three objections are all against the reviewer's own authored text and none is a defect in the round's work: R-0621 above, R-0371's third instance recorded this round, and an observation on G1 that became that third instance. R14 CLOSED T002 with the disconnect hammer the feature file calls its acceptance heart — a client that keeps losing its connection, reconnecting with the id of the last frame it kept, whose final transcript BYTE-EQUALS the ledger's envelope sequence at every drop cadence from one frame to twelve. THE REVIEWER RE-DERIVED EVERY GATE ITSELF at `305bc30c`, from its own runs. TRANSPORT EQUAL THREE WAYS — the reviewer's scratch file, `.agent/authored/f008-r14.md` at `70f3a3e6` and `.agent/last_block.md` at `3de27ff2` — at sha256 974788f0fe8aedcfbc667dd029d7528ad87bab977483e9968c55dba52acbfe2d over 33050 bytes and 364 lines. FIVE SLICES by the reviewer's own ordered extraction from the committed C0a file, every digest matching: PLANF008R14 058d3d22, R0371FROM 8c1880a0, R0371TO d999949c, LEDGER14 7a7990b0 and TESTS14 9c084fdd. THE PLAN LANDED FIRST at `6acca2a4`, byte-equal at 45 lines under the 50-line cap. THE R-0371 WIDENING IS PROVED CONSTRUCTIVELY, not counted: R0371FROM occurs exactly once in the C1 file, and replacing that one occurrence with R0371TO yields a file BYTE-EQUAL to the C2 blob at 8ae3c4a3, with the line count 1026 at both commits because a one-line slice replaced a one-line slice. THE APPEND at `f02742f9` is a byte-exact prefix plus a 6119-byte remainder equal to a newline plus LEDGER14, agreed by an INDEPENDENT blank-line split into 210 units whose LAST TWO equal LEDGER14's two paragraphs in order, with a one-byte flip REJECTED by both readings and the unflipped ACCEPTED by both. THE SETS MOVED AS ORDERED ACROSS THREE COMMITS — 191, 191, 192 registered, `Done:` and `Landed:` 0 at all three, `Gate: R` 13, 13, 14 over fourteen DISTINCT keys, R-0620 nowhere then once, R-0621 nowhere — so the edit minted nothing and only the append did. THE TEST APPEND at `3c758702` is a byte-exact prefix whose remainder is TWO newlines plus TESTS14 and NOT one, the diff adding 92 lines and removing none, 92 being TESTS14's 90 plus the two blank lines PEP 8 costs — a property no rule in this configuration can see, which is why it was gated as bytes. SEVEN single-parent commits, insertions 364, 278, 23, 1, 4 and 92 before the handback, all under 500, and EVERY CELL of the handback's `+/-` column agreed with `git diff --numstat`, deletions 0, 372, 23, 1, 0 and 0 included. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: the SSE file exits 0 at 62, the state readers exit 0 at 462 and `tests/docs/` exits 0 at 295, reconciling 57 + 5 and 457 + 5 exactly. THE MUTATION CONTROL IS THE RIGHT INSTRUMENT AND THE REVIEWER RE-RAN IT in its own disposable worktree: a test-only round over behaviour that already exists cannot be red-proved by reverting a file, so instead dropping the `+ 1` from `resolve_sse_start` and separately making its digit test unreachable each drive the hammer to EXIT 1 with the same four failures, and the unmutated file EXITS 0 — the single survivor being the one-clean-connection test, which never resumes and so cannot be reached by any mutation of the resume rule. RUFF EQUAL ACROSS THE CHANGE, empty multiset at base and head through a `--stdin-filename` read that never touched the checkout, behind a control shown non-empty at exit 1. Zero marker lines in all four targets, a reflog with `amend`, `rebase` and `cherry` at 0, an 80-line handback under its 100-line cap naming C0a through C5 once each, the tree clean with one worktree, the branch pushed and `gh pr list` empty.
<<<END LEDGER15

<<<SLICE FIXFROM
    text = str(last_event_id or "").strip()
<<<END FIXFROM

<<<SLICE FIXTO
    text = "" if last_event_id is None else str(last_event_id).strip()
<<<END FIXTO

<<<SLICE HAMMERFROM
def _hammer(monkeypatch: Any, events: list, drop_after: int,
            reconnects: int = 40) -> list[bytes]:
    """Reconnect until the ledger is drained, dropping every `drop_after` frames.

    This is the acceptance shape the feature file names: a client that keeps
    losing its connection must end up with the ledger and nothing else. Each
    reconnect carries the id of the last frame it kept, exactly as an
    EventSource sends `Last-Event-ID`, and the server decides the span.
    """
    monkeypatch.setattr(mod, "_load_events", lambda job: events)
    transcript: list[bytes] = []
    last_event_id: str | None = None
<<<END HAMMERFROM

<<<SLICE HAMMERTO
def _hammer(monkeypatch: Any, events: list, drop_after: int,
            reconnects: int = 40, last_event_id: str | None = None) -> list[bytes]:
    """Reconnect until the ledger is drained, dropping every `drop_after` frames.

    This is the acceptance shape the feature file names: a client that keeps
    losing its connection must end up with the ledger and nothing else. Each
    reconnect carries the id of the last frame it kept, exactly as an
    EventSource sends `Last-Event-ID`, and the server decides the span.
    `last_event_id` seeds that state, so a caller can hand this helper a client
    that ALREADY holds part of the ledger — which is what makes a resume across
    a ledger that grew between connections expressible (finding R-0621).
    """
    monkeypatch.setattr(mod, "_load_events", lambda job: events)
    transcript: list[bytes] = []
<<<END HAMMERTO

<<<SLICE GROWFROM
    def test_a_ledger_that_grows_between_connections_still_arrives_whole(self, monkeypatch):
        # The stream is a reader over a file that is still being appended to.
        events = _events(6)
        first = _hammer(monkeypatch, events, 2, reconnects=1)
        events.extend(_events(10)[6:])
        rest = _hammer(monkeypatch, events, 3)
        assert b"".join(rest) == _ledger_bytes(events)
        assert [_parse(f)["id"] for f in first] == ["0", "1"]
<<<END GROWFROM

<<<SLICE GROWTO
    def test_a_resume_crosses_a_ledger_that_grew_between_connections(self, monkeypatch):
        # The stream reads a file that is still being appended to, so the span
        # a client misses can straddle the growth. R-0621: the version of this
        # test written at R14 started its second client from scratch, so the
        # boundary it is named for was never crossed by a resume at all.
        events = _events(6)
        first = _hammer(monkeypatch, events, 2, reconnects=1)
        assert [_parse(f)["id"] for f in first] == ["0", "1"]
        events.extend(_events(10)[6:])
        rest = _hammer(monkeypatch, events, 3,
                       last_event_id=_parse(first[-1])["id"])
        # 2 through 9: everything after the frame the client kept, across the
        # boundary, with no duplicate of 1 and no gap at 6.
        assert [_parse(f)["id"] for f in rest] == [str(i) for i in range(2, 10)]
        assert b"".join(first + rest) == _ledger_bytes(events)
<<<END GROWTO

<<<SLICE TESTS15
class TestResumeStartTypes:
    """R-0620: the guard reads a POSITION, and zero is a position."""

    def test_an_integer_zero_is_a_position_and_not_an_absence(self):
        # The string "0" is truthy and the integer 0 is not, so a truthiness
        # guard passes the string form and silently fails this one.
        assert mod.resolve_sse_start(0, "7") == 1

    def test_an_integer_header_resumes_one_past_it(self):
        assert mod.resolve_sse_start(4, "7") == 5

    def test_none_is_the_only_absence(self):
        # Everything else is data; only a missing header falls back.
        assert mod.resolve_sse_start(None, "7") == 7
<<<END TESTS15
