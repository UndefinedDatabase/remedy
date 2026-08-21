── STEP R6/1 — F008 SSE event stream · SESSION CLOSE ─────────
Goal:        Record the R5 verdict and close this session cleanly. The
             session reaches its stated round cap here, so this round
             writes no code: it lands the verdict R5 would otherwise
             strand, refreshes the branch context to the state a fresh
             reader would need, and writes the handoff that is the only
             return channel. A session that ends at its limit with a
             written handoff is a SUCCESS, not a failure (self-drive
             protocol G7).

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 record the R5 verdict · C3 refresh the branch context ·
             C4 write the session-closing handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r6.md      (C0a, new)
             - .agent/last_block.md            (C0b, rewrite)
             - .agent/plan.md                  (C1, rewrite)
             - .agent/live_review.md           (C2, append)
             - .agent/context.md               (C3, rewrite)
             - .agent/handoff.md               (C4, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r6.md, extracted by its marker lines. No slice is
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines
    strictly between its `<<<SLICE X` and `<<<END X` markers. PLANF008R6
    and CONTEXTR6 are applied with their trailing newline INCLUDED and are
    the ENTIRE content of their files. RECORDR5 is applied as `\n` plus
    its single line, appended to the end of `.agent/live_review.md` after
    exactly one blank line. Every file ends with exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4.
    `.agent/plan.md` is advanced at C1, the first substantive commit.
 4. NO NEW FINDING IS REGISTERED. R5 passed with none against it, and the
    one defect its worker surfaced — a lint gate comparing two multisets
    produced by ONE extractor, which agrees with itself when the extractor
    is broken — is fresh recurrence evidence for R-0573, which is already
    OPEN and already carries that fix. Minting a second id for a defect
    the open set holds is what checklist item 30 forbids. So
    `.agent/live_review.md` gains exactly one `Gate:` paragraph and no
    `- R-` line, and the next free id stays R-0614.
 5. NO PRODUCTION CODE. No path under packages/, apps/, tests/ or docs/ is
    touched. This round writes only `.agent/` state.
 6. `git status --porcelain` is empty after every commit and at the
    handback, and `git worktree list` names the primary checkout alone.
    No worktree is created this round: nothing here is destructive.
 7. Two pytest processes never run at once, and every suite runs in the
    PRIMARY checkout.
 8. The reviewer's readings at `1fae37bf`, taken before this block was
    emitted, which the gates below re-derive rather than trust: the
    combined suite of `tests/ui_server/`, `test_test_runner.py`,
    `test_resource_safety.py`, `test_integrity_gate.py` and
    `tests/cli/test_golden_path.py` exits 0 with `passed + skipped` equal
    to 400. Count by passed-plus-skipped and never by a bare passed count:
    three pre-existing data-dependent `pytest.skip(...)` calls in
    `test_brain_view_model.py` and `test_dashboard_contract.py` make the
    split between the two numbers vary run to run at an unchanged tree.
 9. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. F008
    is mid-feature: T001's endpoint does not exist yet, so the branch is
    not in a closeable state and no PR is owed. The branch is pushed and
    left open for the next session.

Done when:
 G1  `.agent/STOP` is absent, checked immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback; `git worktree list` names the
     primary checkout alone. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of
     .remedy-wt/f008-r6.md, of .agent/authored/f008-r6.md at C0a and of
     .agent/last_block.md at C0b, and state whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     .agent/authored/f008-r6.md by their marker lines, take the COUNT from
     that listing, and report per slice its newline-INCLUDED sha256, byte
     count and line count.
 G4  Plan. Report the sha256, byte count and line count of .agent/plan.md
     at C1 and whether it is byte-equal to PLANF008R6. Its line count is
     under 50. `## Goal` and `## Next Steps` each occur exactly once as
     line-anchored headings and `F008` occurs at least once.
 G5  The verdict append, measured two ways that must agree. For C2 against
     C1: (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the
     remainder equals `\n` plus RECORDR5 — report its sha256, byte count
     and line count; (b) split the C2 file on blank lines with an
     INDEPENDENT extractor and report that its LAST unit equals RECORDR5.
     Normalise the file's single terminating newline before comparing.
     Then run a NEGATIVE CONTROL: flip a byte of the remainder in memory
     and report that BOTH readings reject it while the unflipped value is
     accepted by both.
 G6  The sets. Report line-anchored counts in .agent/live_review.md at C1
     and C2: `^- R-\d+ — ` is 185 at BOTH — constraint 4, no finding is
     registered — `^Done: R-\d+ — ` is 0 at both, `^Landed: ` is 0 at
     both, and `^Gate: R\d+ — ` reads 5 then 6 with the six keys DISTINCT.
     `^- R-0614 — ` occurs 0 times at both.
 G7  Context. Report the sha256, byte count and line count of
     .agent/context.md at C3 and whether it is byte-equal to CONTEXTR6. In
     that file `## Active Branch` occurs exactly once, the token
     `feature/` occurs at least once, and the substrings `Steps`, `F008`,
     `pytest` and `resource` each occur at least once — those are the four
     assertions the live state readers make about this path.
 G8  The state readers still pass, in the primary checkout, run SERIALLY:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     Report the exit code and `passed + skipped`. It exits 0 and sums to
     400. Per constraint 8, do not report a bare passed count and do not
     treat a skip as a failure. This suite is named rather than
     `tests/docs/` because this round's change set holds no docs path; run
     `python3 -m pytest tests/docs/ -q -rf` as well and report it, since
     `.agent/` state is what several of these readers parse.
 G9  Range. With BASE `1fae37bf`, run `git diff --name-only BASE..C4` and
     report that its output equals the Change list above with no path on
     either side alone. Every commit in BASE..C4 has exactly one parent.
     Report each commit's INSERTION count from `git show --numstat`, all
     under 500, and compare those numbers cell by cell against the `+/-`
     column of the handback's `## Commits` table, reporting that the two
     readings agree. C4's own numbers belong to the round report, not to
     its own table cell (finding R-0149).
 G10 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     .agent/plan.md at C1, .agent/live_review.md at C2, .agent/context.md
     at C3 and .agent/handoff.md at C4. Every count is 0.
 G11 History. Over this round's OWN reflog entries, report the count whose
     OPERATION — the text before the first `:` in `git reflog --format=%gs`
     — is `amend`, `rebase` or `cherry`; it is 0. Count by operation and
     never by substring (R-0613). Do not order that every entry read
     `commit:` (R-0601), do not count an unstage as a rewrite (R-0608),
     and state NO entry total.
 G12 The branch is pushed and NO pull request exists. Report the real
     output of `git push` and of
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
     which returns an empty list. Nothing is merged this round.
 G13 Handback. .agent/handoff.md at C4 carries the sections
     docs/agents/handback_template.md mandates and an item-status table
     naming C0a, C0b, C1, C2, C3 and C4 exactly once each. Report its line
     count; the cap is 100, this round having more than five commits. Its
     `## Next` section states, in this order, that the next session's FIRST
     action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND is
     the Open PR Gate (Phase 1 rule 2), which finds no open pull request
     and therefore continues on this branch at R7 rather than cutting a
     new one.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 20 % (F008 beansprucht · sechs Urteile im Ledger ·
            DECISION F008 D1 vollständig umgesetzt — Server nebenläufig,
            Ledger-Position als `seq` sichtbar · der Stream-Endpunkt selbst
            ist noch nicht gebaut · Session endet an ihrem Rundenlimit mit
            geschriebenem Handoff) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R6
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, for the next free finding id and for the round map; this file
repeats none of them.

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
R6 records the R5 verdict and closes this session at its stated round cap. Both
prerequisites DECISION F008 D1 named are now landed and reviewed: the cockpit
server serves concurrent requests, and the events reader exposes each event's
ledger position as `seq`. No endpoint exists yet. This round writes no code.

## Next Steps
1. R7 begins T001's endpoint: `GET /api/jobs/<jid>/events/stream`, SSE framing
   with `seq` as the event id, a 15 s heartbeat comment frame, and 404 for an
   unknown job before any streaming starts. The route seam is a six-part path
   branch beside the existing `events-since` handler in `_RemedyHandler.do_GET`.
2. R8 adds the per-job connection cap answering 429 beyond it and the framing
   golden the feature file names as T001's contract test.
3. R9 onward builds T002 — Last-Event-ID resume and the forced-disconnect
   hammer whose transcript must byte-equal the ledger — then T003's client
   hook and fallback, then the integration gate before closure.

## Risks
- A streaming handler holds a socket open. Every test that opens one needs a
  hard timeout and a guaranteed close, or a hung test will cost a round; the
  barrier pattern R4 used is the model — assert a fact, never a duration.
- The 50-event cap in the reader bounds the RESPONSE, not the numbering, so
  T002's resume from an ancient cursor must page rather than assume one
  response covers the span.
- 185 findings are open and none is a code defect of F008. R-0403, R-0607,
  R-0608, R-0609, R-0611 and R-0613 stay routed to a paydown branch, together
  with promoting R-0387's and R-0573's fix clauses into the §3 checklist.
<<<END PLANF008R6

<<<SLICE RECORDR5
Gate: R6 — the R5 entry. R5 PASSED with NO finding against its work and none against its block, and with it BOTH halves of DECISION F008 D1 are landed and reviewed. The events reader now carries each event's own ledger position as `seq` instead of leaving a caller to infer it, which is the value F008's stream will use as its SSE event id. THE RED PROOF IS REAL AND THE REVIEWER RE-RAN IT ITSELF at `0b1abd81` in a disposable worktree, never in the primary checkout: with the pair reverted the suite EXITS 1 at 6 failed and 1 passed with `KeyError` naming `seq` in its output; with the pair restored the file is byte-identical to C3's blob and the same command EXITS 0 at 7 passed. THE ONE TEST THAT SURVIVES THE REVERT IS HONEST AND WORTH NAMING: `test_a_cursor_past_the_end_returns_nothing_and_invents_no_seq` asserts an EMPTY event list, so it reads no `seq` key and passes in both directions by construction — a 7-of-7 red would have meant the tests were coupled to the field rather than to the behaviour, and the worker reported the 6-and-1 split rather than rounding it. THE TESTS PIN THE PROPERTY AND NOT THE IMPLEMENTATION: they assert that the position is ABSOLUTE rather than relative to the cursor, that one event answers to one `seq` across different cursors, that the returned cursor is one past the last `seq` so nothing is skipped or repeated, and that the 50-event response cap bounds the RESPONSE without ever restarting the numbering — which is exactly what "the stream must not renumber" protects, expressed as something a future refactor must keep true. THE CHANGE IS FIVE INSERTIONS AND ONE DELETION on that path, a numstat the reviewer MEASURED by applying the pair to the base blob and diffing rather than deriving it from the slices' line counts, because two of the seven replacement lines are unchanged context; the block was corrected from a wrong prediction of seven before it was emitted, which is the R-0336 rule applied to the reviewer's own arithmetic. THE SHARED PATH IS UNHARMED: the combined suite of `tests/ui_server/`, `test_test_runner.py`, `test_resource_safety.py`, `test_integrity_gate.py` and the canary exits 0 at 400 passed, and the reviewer measured 351 without this round's change and new file against 358 with them in one worktree, so 351 plus 7 reconciles exactly and no existing test moved. THE ROUND'S OWN SHAPE HOLDS, re-measured off disk: transport byte-equal three ways at sha256 67489603142f567411b9c370351d8e3595cb9f9bcb951de067faa7c6a3e7b23b over 23217 B and 349 lines; FIVE slices by the reviewer's own ordered extraction, the test file among them byte-equal at 0b9c7605 to the bytes the reviewer had already run red and green before the block was emitted, so what landed is what was proven rather than a retype of it; `.agent/plan.md` at `627ab499` byte-equal to its slice at 43 lines under the cap; the verdict append at `f00360c0` a byte-exact prefix-plus-remainder agreed by an independent 194-unit blank-line split with a one-byte flip rejected by both readings; the registered set unmoved at 185 with 0 resolved and 0 `Landed:`, `Gate: R` going 4 to 5 with distinct keys, and no id minted, exactly as the block's constraint 5 required; six single-parent commits with insertions all under the 500 cap; zero marker lines in any target; ruff multisets EQUAL across the change and empty on the new file; a 92-line handback under its cap with every mandated section and an item table naming C0a through C4 exactly once; and the tree clean with the primary checkout the only worktree. NO DEVIATION WAS DECLARED AND NONE WAS OWED. ONE DEFECT IN THE BLOCK IS RECORDED HERE AS RECURRENCE EVIDENCE FOR R-0573 RATHER THAN AS A NEW ID, the open set having been searched for the DEFECT before any id was considered, as item 30 requires. G12 ordered the base and head rule-code MULTISETS compared and called them equal — but both readings come from ONE extractor, so a broken extractor returns an empty multiset on both sides and the equality holds no matter what the files contain. That is precisely R-0573's sentence, "running one broken extractor on both sides of an equality yields agreement no matter what the files contain", arriving through a lint gate instead of through a paragraph comparison, and R-0573 is OPEN and already carries the fix. IT WAS NOT HYPOTHETICAL THIS TIME: the worker's first extractor assumed a `path:line:col: CODE` shape that this ruff does not emit, returned an empty multiset on known-BAD input, and would have reported an equality it had not measured. The worker caught it, rewrote the extractor, validated it against a deliberately broken file that yielded a three-code multiset, and only then took the three real readings — a control the block never ordered. A future lint gate orders that control: a multiset comparison is believed only once the extractor has been shown to produce a NON-EMPTY reading on input known to be red.
<<<END RECORDR5

<<<SLICE CONTEXTR6
# Context — F008 SSE event stream

## Active Branch
feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge commit
of pull request #208, which R1 merged at the Open PR Gate. Self-drive session
per docs/agents/self_drive_protocol.md: the main session plans and reviews and
writes nothing in the work tree, one delegated worker per round makes every
commit. The branch is mid-feature and carries no pull request.

## Scope
In: a per-job SSE endpoint served by the existing UI server, carrying the
Part E envelope with the ledger's own position as the event id, a 15 s
heartbeat frame, Last-Event-ID resume replaying the missed span out of the
ledger, 404 for an unknown job and a max-connections-per-job guard answering
429 beyond it; plus a client hook with reconnect backoff, gap detection, a
polling fallback on the same interface, and the status surface live,
reconnecting or delayed.

Out, per the feature file's Do not touch: command and write paths, the event
content and schema (Part E owns them) and the ledger format. Any POST surface
belongs to the NEXT feature and is rejected here.

## Constraints
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/ and tests/orchestration/test_roadmap_index.py — the second by
  R-0493, tests/docs/ asserting nothing about a feature file's body — and a
  round rewriting `.agent/` state or touching the UI server also gates
  tests/ui_server/, tests/orchestration/test_test_runner.py,
  tests/regression/test_resource_safety.py and
  tests/orchestration/test_integrity_gate.py. Destructive and red-proof checks
  run only inside a disposable git worktree under .remedy-wt/, so resource
  safety stays intact. Two pytest processes never run at once.
- COUNT BY PASSED-PLUS-SKIPPED. Three data-dependent `pytest.skip(...)` calls
  in tests/ui_server/test_brain_view_model.py and test_dashboard_contract.py
  make the split vary run to run at an unchanged tree, so a bare passed count
  is not a stable gate value and a skip is not a failure.
- DECISION F008 D1 IS FULLY LANDED as of R5 and both its rulings are reviewed:
  the server is threaded, so a long-lived response no longer blocks the
  cockpit, and the events reader exposes the ledger position as `seq` rather
  than assigning a counter. T001's endpoint itself is NOT built yet.
- This is a UI feature: docs/ui/design_reference/ is binding for every visual
  surface and assets_spec.md is the asset authority. Any deviation needs an
  assumption_log entry carrying a technical reason.
- Repository-wide `ruff check .` is RED and is NOT a gate (R-0364): 26 errors
  measured at the claim — 20 I001, 4 F401, 1 UP035 and 1 F821. Ruff is gated
  scoped to the files a round touches, measured against the SAME files at the
  base, so a pre-existing error is never read as a new one.
- 185 findings are open and none is a code defect of F008. R-0403, R-0607,
  R-0608, R-0609, R-0611 and R-0613 stay routed to a paydown branch, together
  with promoting the fix clauses of R-0387 and R-0573 into the §3 checklist —
  both are rules that live in a finding body, and both recurred in this
  feature because a finding body binds no later block.

## Steps
Stated once, in `.agent/plan.md`. This file tracks scope and constraints only.
<<<END CONTEXTR6
