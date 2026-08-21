── STEP R14/1 — F008 SSE event stream · T002 DISCONNECT HAMMER ────
Goal:        Close T002 with the acceptance test the feature file calls its
             heart, verbatim: a client that keeps losing its connection
             reconnects carrying the id of the last frame it kept, and its
             FINAL TRANSCRIPT BYTE-EQUALS the ledger's envelope sequence — no
             duplicate, no gap, at every disconnect cadence from one drop per
             frame to none at all. This is a TEST-ONLY round: T002's resume
             decision landed at R13, so R14 proves it rather than building it,
             and a mutation control shows the hammer going red when resume
             exactness is broken. R14 also records the R13 verdict (PASS),
             registers R-0620 and widens R-0371 with its second instance.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 widen R-0371 · C3 register R-0620 and record the R13 verdict ·
             C4 the disconnect hammer · C5 the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r14.md        (C0a, new)
             - .agent/last_block.md               (C0b, rewrite)
             - .agent/plan.md                     (C1, rewrite)
             - .agent/live_review.md              (C2 pair, C3 append)
             - tests/ui_server/test_sse_stream.py (C4, append)
             - .agent/handoff.md                  (C5, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r14.md, extracted by its marker lines — never
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback. R0371FROM
    occurs EXACTLY ONCE in its target at C1; if it does not, stop and say so
    rather than choosing an occurrence. Your last two rounds each caught a
    real reviewer defect this way — keep doing exactly that.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines strictly
    between its `<<<SLICE X` and `<<<END X` markers. PLANF008R14 is applied
    with its trailing newline INCLUDED and is the ENTIRE content of its file.
    R0371FROM and R0371TO are each ONE line with its trailing newline; the
    replacement is in place and changes no other byte of the file, so
    `.agent/live_review.md` has the SAME line count at C2 as at C1. LEDGER14
    is applied as a newline plus its body, appended after exactly one blank
    line. TESTS14 is appended to the test file after exactly TWO blank lines —
    PEP 8 for a top-level definition, and NOT a property ruff will catch here:
    E301-E306 are preview-only rules and this repository does not run ruff in
    preview, so G8 gates those blank lines as bytes. Every file ends with
    exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5. `.agent/plan.md`
    advances at C1, ahead of both ledger commits (§3 checklist item 23). C2
    and C3 are SEPARATE commits on the same file on purpose: C2 edits an
    existing finding in place and C3 appends, and keeping them apart is what
    lets G5 prove the edit constructively and G6 prove the append as a byte
    prefix. Collapsing them would make both proofs unavailable.
 4. LEDGER14 carries TWO paragraphs, blank-line separated, applied together in
    C3: the R-0620 registration and the `Gate: R14` entry holding the R13
    verdict. R-0620 is the only id minted, so the next free id becomes R-0621.
    R-0371 is WIDENED, not re-registered: item 30 forbids a second id for a
    defect the open set already describes, and R-0371 already describes it.
 5. NO PRODUCTION CODE. No path under packages/, apps/ or docs/ is touched.
    T002's behaviour already exists; this round proves it. If the hammer fails
    against the current source, that is a real defect — STOP and report it,
    and do not adjust the test to make it pass.
 6. `git status --porcelain` is empty after every commit and at the handback.
    `git worktree list` names the primary checkout alone at the handback: the
    mutation control at G10 runs in a disposable worktree under `.remedy-wt/`,
    which is gitignored, and that worktree is REMOVED before the handback is
    written. Base bytes reach a tool by `git show <sha>:<path>`, never by
    overwrite-and-restore in the primary checkout (self_drive_protocol G5).
 7. Two pytest processes never run at once, and G9's counting suites run in
    the PRIMARY checkout — a fresh worktree has no `apps/ui/node_modules` and
    its pass counts are untrustworthy in both directions (R-0518).
 8. The reviewer's own readings at `c8beb250`, RE-DERIVED by the gates below
    rather than trusted: `tests/ui_server/test_sse_stream.py` exits 0 at 57,
    the combined state-reader suite exits 0 at 457, `tests/docs/` exits 0 at
    295, and `ruff check` over the test file exits 0 with an EMPTY multiset.
    Count by passed-plus-skipped, never by a bare passed count.
 9. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. T003 is
    unbuilt, so the branch is not closeable. It is pushed and left open.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback, where `git worktree list` names the
     primary checkout alone. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block the worker was given, of `.agent/authored/f008-r14.md` at C0a and
     of `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r14.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256, bytes and
     lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R14. Its line count is under 50,
     `## Goal` and `## Next Steps` each occur exactly once line-anchored, and
     `F008` occurs at least once.
 G5  The R-0371 widening, proved CONSTRUCTIVELY. Report that R0371FROM occurs
     EXACTLY ONCE in `.agent/live_review.md` at C1, replace that one
     occurrence with R0371TO, and report whether the result is BYTE-EQUAL to
     that file at C2, giving the sha256 of both sides. Report the LINE COUNT
     of the file at C1 and at C2: they are EQUAL, because a one-line slice
     replaced a one-line slice. Report also that `- R-0371 — ` occurs exactly
     once at C2 and that the C2 line ENDS with ` OPEN.`
 G6  The ledger append, C3 against C2, measured two ways that must agree.
     (a) the C2 blob is a byte-exact PREFIX of the C3 blob and the remainder
     equals a newline plus LEDGER14 — report its sha256, bytes and lines;
     (b) an INDEPENDENT blank-line split of the C3 file, its terminating
     newline normalised first, has as its LAST TWO units, in order, the two
     paragraphs of LEDGER14. NEGATIVE CONTROL: flip one byte of the remainder
     and report BOTH readings reject it, the unflipped accepted by both.
 G7  The sets, at THREE commits. Report line-anchored counts in
     `.agent/live_review.md` at C1, C2 and C3: `^- R-\d+ — ` reads 191, 191,
     192 — C2 edits and only C3 mints — `^Done: R-\d+ — ` is 0 at all three,
     `^Landed: ` is 0 at all three, `^Gate: R\d+ — ` reads 13, 13, 14 with the
     fourteen keys DISTINCT, `^- R-0620 — ` reads 0, 0, 1 and `^- R-0621 — `
     is 0 at all three. Report that LEDGER14's `Gate:` header matches the
     shape of the entries already in the file, as a pattern match over
     `^Gate: R(\d+) — the R(\d+) entry\.` requiring the second number to be
     one less than the first and the R14 pair to occur exactly once (§3 item
     26). Report the number of `^Gate: ` lines that do NOT match; it is 1, and
     that line is `Gate: R1 — the F255 R21 entry.`
 G8  The test append. Report that the `c8beb250` blob of
     `tests/ui_server/test_sse_stream.py` is a byte-exact PREFIX of that
     file's C4 blob and that the remainder is TWO newlines followed by
     TESTS14 — two, not one, that being constraint 2's blank-line rule
     measured as bytes because no lint rule here can see it. Report that the
     lines `git diff c8beb250..C4 -- tests/ui_server/test_sse_stream.py` ADDS
     are the two blank lines followed by TESTS14's lines IN ORDER, that the
     added-line count equals TESTS14's line count plus two, and that the diff
     REMOVES nothing.
 G9  The suites are green in the PRIMARY checkout, run SERIALLY, never two
     pytest processes at once. Report the exit code and `passed + skipped` of
     each, at C4:
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf` exits 0.
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf` exits 0.
     `python3 -m pytest tests/docs/ -q -rf` exits 0 and sums to 295.
     RECONCILE THE ARITHMETIC RATHER THAN ASSERTING A BARE TOTAL: report the
     number of lines matching `^    def test_` in TESTS14, and report that the
     first sum equals 57 plus that number and the second equals 457 plus the
     same number, 57 and 457 being constraint 8's base readings. If any of the
     three identities fails, report the real values and stop.
 G10 MUTATION CONTROL — the colour, never a count, and NOT a red proof. The
     behaviour this round tests already exists, so reverting a file proves
     nothing; instead the hammer must go RED when resume EXACTNESS is broken,
     or it is not testing what it claims. In a DISPOSABLE worktree under
     `.remedy-wt/`, created with `git worktree add --detach` at C4 and removed
     before the handback, apply each of these two single-line mutations to
     `packages/orchestration/ui_server.py` IN THE WORKTREE ONLY, each from the
     unmutated file, and report the exit code of
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf -k DisconnectHammer`
     after each:
       A  replace `        return int(text) + 1` with `        return int(text)`
       B  replace `    if text.isdigit():` with `    if False:`
     Each EXITS NON-ZERO. Report which hammer tests failed under each and
     which SURVIVED; a survivor is expected and is reported, not explained
     away — a single clean connection never resumes, so no mutation of the
     resume rule can reach it. Then restore the unmutated file and report that
     the same command EXITS 0. The PRIMARY checkout is never touched.
 G11 Ruff, scoped to the one touched file and compared as a MULTISET of rule
     codes rather than as an exit code. Run
     `python3 -m ruff check --output-format concise tests/ui_server/test_sse_stream.py`
     at C4, and at `c8beb250` by feeding the base blob through
     `git show c8beb250:<path> | python3 -m ruff check --output-format concise --stdin-filename <path> -`
     so `per-file-ignores` still resolves by path and no file is overwritten
     (§3 item 29). Report both multisets; they are EQUAL and both EMPTY.
     CONTROL, through the SAME extractor: feed a deliberately unused import to
     ruff on stdin and report that the extractor yields a NON-EMPTY multiset
     at a non-zero exit (R-0463).
 G12 Range, and NOT self-referential. With BASE `c8beb250`:
     `git diff --name-only BASE..C4` equals the Change list above MINUS
     `.agent/handoff.md`, with no path on either side alone — the range stops
     at C4 precisely because a reading over a range that includes the handback
     commit cannot be written inside the handback, which is finding R-0371 as
     widened by this very round's C2. The full `BASE..C5` name-only reading,
     which equals the whole Change list, belongs to the round report. Every
     commit in BASE..C5 has exactly one parent. For every commit BEFORE C5
     report BOTH numstat figures per path — insertions AND deletions — from
     `git show --numstat`, report that every insertion count is under 500, and
     compare EVERY CELL against the `+/-` column of the handback's
     `## Commits` table, both sides read from `git diff --numstat` and never
     from a file's line counts before and after. Both cells, not the insertion
     alone: that half-width reading is finding R-0619.
 G13 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C3,
     `tests/ui_server/test_sse_stream.py` at C4 and `.agent/handoff.md` at C5.
     Every count is 0.
 G14 History. Over this round's OWN reflog entries, report the count whose
     OPERATION — the text before the first `:` in `git reflog --format=%gs` —
     is `amend`, `rebase` or `cherry`; it is 0. Count by operation, never by
     substring; no total is asserted.
 G15 The branch is pushed and NO pull request exists. Report the real output
     of `git push` and of
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
     which returns an empty list. Nothing is merged this round.
 G16 Handback. `.agent/handoff.md` at C5 carries the sections
     docs/agents/handback_template.md mandates and an item-status table naming
     C0a, C0b, C1, C2, C3, C4 and C5 exactly once each. Report its line count;
     the cap is 100, this round having more than five commits, and an overage
     carries a DECISION D15 stated-cause line naming the mandated content that
     caused it. Its `## Next` section states that the next session's FIRST
     action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the
     Open PR Gate (Phase 1 rule 2), and that the next round is R15, whose work
     is T003's client hook.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 62 % (F008 beansprucht · vierzehn Urteile im Ledger ·
            T001 KOMPLETT · T002 KOMPLETT: Resume-Entscheidung in R13, in R14
            der Trennungs-Hammer, dessen Transkript byteweise der
            Ledger-Sequenz gleicht, plus Mutationskontrolle · T003 Client-Hook,
            Backoff, Lueckenerkennung und Polling-Fallback folgen ab R15 ·
            danach das Integrationstor vor dem Abschluss) — Schaetzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R14
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
R14 CLOSES T002 with the acceptance test the feature file calls its heart: a
client that keeps losing its connection reconnects with the id of the last
frame it kept, and its final transcript must BYTE-EQUAL the ledger's envelope
sequence — no duplicate, no gap, at every disconnect cadence from one drop per
frame to none at all. The hammer is a test-only round: T002's resume decision
landed at R13, so this round proves it rather than building it, and a mutation
control shows the hammer goes red when resume exactness is broken. R14 also
records the R13 verdict, registers R-0620 and widens R-0371.

## Next Steps
1. R15 begins T003: the `useBrainStream` client hook, EventSource with
   reconnect backoff, gap detection via seq discontinuity, and the status
   surface live | reconnecting | delayed.
2. R16 adds T003's polling fallback on the same hook interface and the
   fixture live-job end-to-end.
3. Then the integration gate before closure.

## Risks
- The hammer drives `_send_sse_stream` directly rather than over a socket, so
  it proves the resume CONTRACT and not the transport. The transport is
  covered separately by the framing golden and the drain tests.
- `resolve_sse_start` narrows a non-string `Last-Event-ID` to the cursor
  because `str(x or "")` reads an integer 0 as absent. Registered as R-0620;
  the HTTP path only ever passes strings, so it is latent.
- No open finding is a code defect of F008 reachable from the HTTP path.
  R-0403, R-0607 through R-0609, R-0611 and R-0613 through R-0620 stay routed
  to a paydown branch.
<<<END PLANF008R14

<<<SLICE R0371FROM
- R-0371 — Low — a block ordered a value that cannot exist at the moment the text carrying it is written. The R5 block told the worker to append to `.agent/live_review.md` "a single line of your own of exactly this shape, with your real commit SHA: `Landed: R-0370 — <one line: what changed, which commit>`" and, six lines later, that "that live_review.md edit belongs to C2, the same commit as the test". A commit's SHA is a hash over a tree that already contains every byte of that commit, so a line inside C2 can never name C2. No correct application of the bundle could satisfy both clauses. The worker was right to declare the deviation, name the commit by its role — "R5's C2, the same commit as this line, whose SHA the handback reports" — and let the handback carry the real value `a01e8a9712aead26eb88888db352d0bb72492cb9`; nothing was fabricated and nothing was edited toward a number. This is the seventh reviewer-gate defect of this feature, after R-0363's unmeasured block length, R-0364's unexecuted ruff gate, R-0367's unreachable numstat, R-0368's wrong-base range gate and R-0369's self-counting string gate, and it is a class none of their counter-measures reach: R-0364 makes the reviewer EXECUTE every gate it orders, but a self-referential SHA is not a gate at all — it is appliable CONTENT whose required value the act of applying it destroys, so there is nothing for the reviewer to execute in advance. `docs/agents/planner_reviewer_prompt.md` §4 item 4 supplies the template verbatim, including the words "which commit", and the template is fine; the defect is pairing it with "your real commit SHA" and "the same commit as the test". Counter-measure, binding from R6 on and additive to all of the above: before ordering any text to be written into a file, the reviewer checks that every value that text must contain already exists at the moment of writing. Commit SHAs, `git show --numstat` outputs and every other post-hoc measurement are ordered into the HANDBACK, which is written after the commits exist, and never into the committed text itself; where a committed line must identify its own commit it names it by its ROLE in the bundle. OPEN.
<<<END R0371FROM

<<<SLICE R0371TO
- R-0371 — Low — a block ordered a value that cannot exist at the moment the text carrying it is written. The R5 block told the worker to append to `.agent/live_review.md` "a single line of your own of exactly this shape, with your real commit SHA: `Landed: R-0370 — <one line: what changed, which commit>`" and, six lines later, that "that live_review.md edit belongs to C2, the same commit as the test". A commit's SHA is a hash over a tree that already contains every byte of that commit, so a line inside C2 can never name C2. No correct application of the bundle could satisfy both clauses. The worker was right to declare the deviation, name the commit by its role — "R5's C2, the same commit as this line, whose SHA the handback reports" — and let the handback carry the real value `a01e8a9712aead26eb88888db352d0bb72492cb9`; nothing was fabricated and nothing was edited toward a number. This is the seventh reviewer-gate defect of this feature, after R-0363's unmeasured block length, R-0364's unexecuted ruff gate, R-0367's unreachable numstat, R-0368's wrong-base range gate and R-0369's self-counting string gate, and it is a class none of their counter-measures reach: R-0364 makes the reviewer EXECUTE every gate it orders, but a self-referential SHA is not a gate at all — it is appliable CONTENT whose required value the act of applying it destroys, so there is nothing for the reviewer to execute in advance. `docs/agents/planner_reviewer_prompt.md` §4 item 4 supplies the template verbatim, including the words "which commit", and the template is fine; the defect is pairing it with "your real commit SHA" and "the same commit as the test". Counter-measure, binding from R6 on and additive to all of the above: before ordering any text to be written into a file, the reviewer checks that every value that text must contain already exists at the moment of writing. Commit SHAs, `git show --numstat` outputs and every other post-hoc measurement are ordered into the HANDBACK, which is written after the commits exist, and never into the committed text itself; where a committed line must identify its own commit it names it by its ROLE in the bundle. SECOND INSTANCE, F008 R13, and it lands inside this counter-measure's own escape hatch. The counter-measure routes every post-hoc measurement "into the HANDBACK, which is written after the commits exist" — but the handback IS a commit in the range, so a reading over a range that INCLUDES the handback commit is still unwritable at the moment that file is written. R13's G12 ordered `git diff --name-only BASE..C6` where C6 is the handback commit itself, and the Change list it had to equal contains `.agent/handoff.md`: no pre-C6 reading could match it and no post-C6 reading could be placed inside C6. The worker declared the impossibility rather than fudging it, put the pre-C6 reading in the file and the full BASE..C6 reading in the round report — the R-0149 carve-out applied by hand to a clause that never named it. THE NEAR MISS IS THE INSTRUCTIVE PART: R13's G12 did name that carve-out, but only for the numstat half of the gate ("C6's own numbers belong to the round report") and not for the name-only half three sentences earlier, so one reviewer sentence knew the rule while its neighbour did not. COUNTER-MEASURE WIDENED: a range gate whose range ends at the handback commit either states the carve-out for EVERY reading it orders, or ends its range at the commit BEFORE the handback and names the handback's own path separately. OPEN.
<<<END R0371TO

<<<SLICE LEDGER14
- R-0620 — Low — A GUARD WRITTEN TO PROVE THAT ZERO IS A POSITION USES THE ONE PYTHON IDIOM THAT READS ZERO AS ABSENT. `resolve_sse_start`, authored by the reviewer as the RESOLVETO slice of the F008 R13 block and applied byte for byte at `245d8651`, opens with `text = str(last_event_id or "").strip()`. Its parameter is annotated `Any`, so an integer is admitted, and for the integer `0` the expression `0 or ""` evaluates to `""` — the function then falls through to the cursor and returns the cursor's position. That is precisely the behaviour the same slice's docstring forbids in writing ("the first event is 0; a truthiness test here would resume at 0 and replay it for ever") and that TESTS13 believes it has pinned in `test_event_id_zero_is_a_position_and_not_an_absence`. THE TEST CANNOT SEE IT: it passes the STRING `"0"`, which is truthy, so the guard is never exercised with a falsy position and the suite is green at 57. RE-MEASURED BY THE REVIEWER by importing the module and calling the function: `resolve_sse_start("0", "7")` returns 1, `resolve_sse_start(0, "7")` returns 7, `resolve_sse_start(4, "7")` returns 5 — so the defect is specific to the falsy value and not to integers as such, which is what makes it survive casual reading. WHY LOW AND NOT MEDIUM: the only production caller is the stream branch, which passes `self.headers.get(SSE_LAST_EVENT_ID_HEADER)`, and an HTTP header value is a string or `None`; both are handled correctly, so nothing reachable over the wire is wrong today. It is registered rather than waved away because the annotation invites the unreachable call, the docstring promises the opposite of the behaviour, and a T003 client hook passing a parsed integer is a plausible next caller. THE FIX, one line: replace the truthiness test with an explicit None test — `text = "" if last_event_id is None else str(last_event_id).strip()` — and add a test that calls the function with the INTEGER 0. FOUND BY THE WORKER, not the gates: the R13 worker applied the slice unedited as constraint 1 required and declared the contradiction in its handback, which is the third consecutive round in which a worker's declaration is the only reason a reviewer-authored defect is on the record. No gate of that block could have caught it, because every gate compared bytes and the bytes were exactly what the reviewer wrote.

Gate: R14 — the R13 entry. R13 PASSED. Its two objections are both against the reviewer's own authored text and neither is a defect in the round's work: R-0620 above, and the R-0371 widening also recorded this round. R13 BEGAN T002 — `resolve_sse_start` holding the header-versus-cursor rule alone, the stream branch resolving both inputs before entering the writer, and seventeen tests pinning the decision. THE REVIEWER RE-DERIVED EVERY GATE ITSELF at `c8beb250`, from its own runs. TRANSPORT EQUAL THREE WAYS this time, the scratch block having survived on disk: the reviewer's own scratch file, `.agent/authored/f008-r13.md` at `7fc5046d` and `.agent/last_block.md` at `13ac3e84` all at sha256 4aaaafb36a773dbf9a4e9fd24772602d45e039e41566144c413d12a032d07415 over 30793 bytes and 458 lines. ELEVEN SLICES by the reviewer's own ordered extraction out of the committed C0a file, every digest matching: PLANF008R13 8d41b66d, LEDGER13 51cf1279, RESOLVEFROM 62776105, RESOLVETO 97981379, ROUTEFROM 897b674c, ROUTETO e8297527, HELPERFROM 1ea7c575, HELPERTO 134bca15, RAISEFROM f46d77d3, RAISETO 6e50d886 and TESTS13 8766b87d. THE PLAN LANDED FIRST at `390d6d10`, byte-equal to PLANF008R13 at 45 lines under the 50-line cap. THE LEDGER APPEND at `540bd0d3` is a byte-exact prefix plus a 5629-byte remainder equal to a newline plus LEDGER13, agreed by an INDEPENDENT blank-line split into 208 units whose LAST TWO equal LEDGER13's two paragraphs in order, with a one-byte flip REJECTED by both readings and the unflipped ACCEPTED by both; the set moved 190 to 191, `Done:` and `Landed:` 0 at both, `Gate: R` 12 to 13 over thirteen DISTINCT keys, R-0619 exactly once and R-0620 nowhere. BOTH SOURCE CHANGES ARE PROVED CONSTRUCTIVELY, not counted: applying RESOLVEFROM/RESOLVETO and ROUTEFROM/ROUTETO to the `a76ea1e7` blob of `packages/orchestration/ui_server.py`, each FROM occurring exactly once, yields a file BYTE-EQUAL to the C4 blob at b5149772; applying HELPERFROM/HELPERTO and RAISEFROM/RAISETO to the base test blob yields the C3 blob exactly; and the C3 blob is a byte-exact prefix of the C5 blob whose remainder is TWO newlines plus TESTS13, the diff adding 90 lines and removing none, 90 being TESTS13's 88 plus the two blank lines the PEP 8 separation costs — a property no lint rule in this configuration can see, which is why it was gated as bytes. EIGHT single-parent commits, insertions 458, 387, 17, 4, 6, 32 and 90 before the handback, all under 500, and EVERY CELL of the handback's `+/-` column agreed with `git diff --numstat` — deletions 0, 123, 17, 0, 1, 1 and 0 included, which is finding R-0619's counter-measure working on its first application. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: the SSE file exits 0 at 57, the state readers exit 0 at 457 and `tests/docs/` exits 0 at 295, reconciling 40 + 17 and 440 + 17 exactly against the base readings. THE RED PROOF IS REAL AND RE-RUN BY THE REVIEWER in its own disposable worktree, never the primary checkout: with `packages/orchestration/ui_server.py` alone written back to its `a76ea1e7` blob the SSE file EXITS 1 in five runs out of five, and restored to its C4 blob EXITS 0 at 57; the 42 survivors are the query-cursor fallbacks the old route already served, which is why the block ordered the colour and never a count. RUFF EQUAL ACROSS THE CHANGE, empty multiset at base and at head through a `--stdin-filename` read that never touched the checkout, behind a control shown non-empty at exit 1. Zero marker lines in all five targets, a reflog carrying `amend`, `rebase` and `cherry` at 0, an 84-line handback under its 100-line cap naming C0a through C6 once each, the tree clean with one worktree, the branch pushed and `gh pr list` empty.
<<<END LEDGER14

<<<SLICE TESTS14
class _FlakyPeer:
    """A socket that accepts `until` frames and then drops the connection."""

    def __init__(self, until: int) -> None:
        self.frames: list[bytes] = []
        self.until = until

    def write(self, frame: bytes) -> None:
        if len(self.frames) >= self.until:
            raise BrokenPipeError
        self.frames.append(frame)

    def flush(self) -> None:
        return None


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
    for _ in range(reconnects):
        peer = _FlakyPeer(drop_after)
        handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
        handler.send_response = lambda code: None
        handler.send_header = lambda key, value: None
        handler.end_headers = lambda: None
        handler.wfile = peer
        clock = _Clock()
        start = mod.resolve_sse_start(last_event_id, "0")
        handler._send_sse_stream(_Job(), str(start), now=clock.now, sleep=clock.sleep)
        for frame in peer.frames:
            # A heartbeat carries no id, so a resuming client never asks to
            # replay one and it never enters the transcript.
            if frame.startswith(b":"):
                continue
            transcript.append(frame)
            last_event_id = _parse(frame)["id"]
        if last_event_id is not None and int(last_event_id) == len(events) - 1:
            break
    return transcript


def _ledger_bytes(events: list) -> bytes:
    """The envelope sequence the client's transcript must byte-equal."""
    return b"".join(
        mod.sse_event_frame(seq, mod._safe_event_summary(seq, events[seq]))
        for seq in range(len(events))
    )


class TestDisconnectHammer:
    def test_the_transcript_byte_equals_the_ledger_envelope_sequence(self, monkeypatch):
        # The feature's acceptance heart, verbatim: bytes, not a summary.
        events = _events(12)
        assert b"".join(_hammer(monkeypatch, events, 3)) == _ledger_bytes(events)

    def test_no_event_arrives_twice_and_none_is_missing(self, monkeypatch):
        # Spelled out as ids too: a byte comparison that failed would not say
        # WHICH of the two failure modes happened.
        ids = [_parse(f)["id"] for f in _hammer(monkeypatch, _events(12), 3)]
        assert ids == [str(i) for i in range(12)]

    def test_every_disconnect_cadence_yields_the_same_transcript(self, monkeypatch):
        # One drop per frame is the worst case and a single clean connection
        # the best; the transcript may not depend on which one happened.
        events = _events(12)
        for drop_after in (1, 2, 3, 5, 7, 12):
            got = b"".join(_hammer(monkeypatch, events, drop_after))
            assert got == _ledger_bytes(events), drop_after

    def test_a_ledger_that_grows_between_connections_still_arrives_whole(self, monkeypatch):
        # The stream is a reader over a file that is still being appended to.
        events = _events(6)
        first = _hammer(monkeypatch, events, 2, reconnects=1)
        events.extend(_events(10)[6:])
        rest = _hammer(monkeypatch, events, 3)
        assert b"".join(rest) == _ledger_bytes(events)
        assert [_parse(f)["id"] for f in first] == ["0", "1"]

    def test_a_single_clean_connection_needs_no_resume(self, monkeypatch):
        events = _events(4)
        assert b"".join(_hammer(monkeypatch, events, 4)) == _ledger_bytes(events)
<<<END TESTS14
