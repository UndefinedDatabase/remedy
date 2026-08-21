── STEP R13/1 — F008 SSE event stream · T002 LAST-EVENT-ID RESUME ────
Goal:        Build T002's resume decision and pin it. `resolve_sse_start`
             turns the two things a reconnecting client can send into ONE
             ledger position: `Last-Event-ID` names the last frame it already
             holds, so the missed span starts one PAST it, while the query
             cursor names the position to start AT. Conflating them replays an
             event or skips one, and the feature's acceptance test forbids
             both. The stream branch resolves before entering the writer, and
             a header that is absent, blank or mangled falls back to the
             cursor rather than refusing the stream. This round also records
             the R12 verdict (PASS) and registers R-0619.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 register R-0619 and record the R12 verdict · C3 prepare the
             test handlers for a `headers` attribute · C4 the resolver and the
             route · C5 the resume tests · C6 the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r13.md        (C0a, new)
             - .agent/last_block.md               (C0b, rewrite)
             - .agent/plan.md                     (C1, rewrite)
             - .agent/live_review.md              (C2, append)
             - tests/ui_server/test_sse_stream.py (C3 pairs, C5 append)
             - packages/orchestration/ui_server.py (C4 pairs)
             - .agent/handoff.md                  (C6, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r13.md, extracted by its marker lines — never
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback. Each FROM
    occurs EXACTLY ONCE in its target at the base; if one does not, stop and
    say so rather than choosing an occurrence.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines strictly
    between its `<<<SLICE X` and `<<<END X` markers. PLANF008R13 is applied
    with its trailing newline INCLUDED and is the ENTIRE content of its file.
    LEDGER13 is applied as a newline plus its body, appended to
    `.agent/live_review.md` after exactly one blank line. TESTS13 is appended
    to `tests/ui_server/test_sse_stream.py` after exactly TWO blank lines —
    PEP 8 for a top-level definition, and NOT a property ruff will catch for
    you: E301-E306 are preview-only rules and this repository does not run
    ruff in preview, so G8 gates the blank lines as bytes instead. Every
    FROM/TO half carries its own trailing newline. Every file ends with
    exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5, C6.
    `.agent/plan.md` advances at C1, ahead of the ledger append at C2 (§3
    checklist item 23). C3 lands BEFORE C4 on purpose: it gives the two
    socketless handlers a `headers` attribute they do not yet need, so the
    suite is green at C3, green at C4 when the route starts reading it, and
    green at C5. No commit in this round leaves the suite red.
 4. LEDGER13 carries TWO paragraphs, blank-line separated, applied together in
    C2: the R-0619 registration and the `Gate: R13` entry holding the R12
    verdict. R-0619 is the only id minted, so the next free id becomes R-0620.
 5. NO NEW FILE and no path outside the Change list. No POST surface, no
    client-side code, no docs change: T003 owns the hook and the write channel
    belongs to the next feature, which the feature file's Orchestrator brief
    tells this round to reject.
 6. `git status --porcelain` is empty after every commit and at the handback.
    `git worktree list` names the primary checkout alone at the handback: the
    red proof at G10 runs in a disposable worktree under `.remedy-wt/`, which
    is gitignored, and that worktree is REMOVED before the handback is
    written. The primary checkout is never mutated to read a base revision —
    base bytes reach a tool by `git show <sha>:<path>` or by that worktree,
    never by overwrite-and-restore (self_drive_protocol G5, §3 item 29).
 7. Two pytest processes never run at once, and G9's counting suites run in
    the PRIMARY checkout — a fresh worktree has no `apps/ui/node_modules` and
    its pass counts are untrustworthy in both directions (R-0518). The red
    proof at G10 runs in the worktree because it must mutate a source file,
    and it orders a COLOUR, never a count, for exactly that reason.
 8. The reviewer's own readings at `a76ea1e7`, taken before this block was
    emitted and RE-DERIVED by the gates below rather than trusted: the
    combined state-reader suite exits 0 with `passed + skipped` equal to 440,
    `tests/docs/` exits 0 at 295, `tests/ui_server/test_sse_stream.py` exits 0
    at 40, and `ruff check` over the two touched files exits 0 with an EMPTY
    finding multiset. Count by passed-plus-skipped, never by a bare passed
    count — data-dependent `pytest.skip(...)` calls in
    `test_brain_view_model.py` and `test_dashboard_contract.py` move the split
    at an unchanged tree.
 9. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. F008 is
    mid-feature: T002 is only begun here and T003 is unbuilt, so the branch is
    not in a closeable state and no pull request is owed. It is pushed and
    left open.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback, where `git worktree list` names the
     primary checkout alone. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block the worker was given, of `.agent/authored/f008-r13.md` at C0a and
     of `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r13.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256, bytes and
     lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R13. Its line count is under 50,
     `## Goal` and `## Next Steps` each occur exactly once line-anchored, and
     `F008` occurs at least once.
 G5  The ledger append, measured two ways that must agree. C2 against C1:
     (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder
     equals a newline plus LEDGER13 — report its sha256, bytes and lines;
     (b) an INDEPENDENT blank-line split of the C2 file, its terminating
     newline normalised first, has as its LAST TWO units, in order, the two
     paragraphs of LEDGER13. NEGATIVE CONTROL: flip one byte of the remainder
     and report BOTH readings reject it, the unflipped accepted by both.
 G6  The sets. Report line-anchored counts in `.agent/live_review.md` at C1
     and C2: `^- R-\d+ — ` reads 190 then 191 — constraint 4, one id is
     minted — `^Done: R-\d+ — ` is 0 at both, `^Landed: ` is 0 at both, and
     `^Gate: R\d+ — ` reads 12 then 13 with the thirteen keys DISTINCT.
     `^- R-0619 — ` reads 0 then 1 and `^- R-0620 — ` is 0 at both. Report
     also that LEDGER13's `Gate:` header matches the shape of the entries
     already in that file, as a pattern match over
     `^Gate: R(\d+) — the R(\d+) entry\.` requiring the second number to be
     one less than the first and the R13 pair to occur exactly once (§3 item
     26). Report the number of `^Gate: ` lines that do NOT match that pattern;
     it is 1, and that line is `Gate: R1 — the F255 R21 entry.`, which gated
     the PREVIOUS feature's last round and has no F008 predecessor.
 G7  The source pairs, proved CONSTRUCTIVELY and not merely counted. Take the
     `a76ea1e7` blob of `packages/orchestration/ui_server.py` by
     `git show a76ea1e7:packages/orchestration/ui_server.py`, verify that
     RESOLVEFROM and ROUTEFROM each occur EXACTLY ONCE in it, replace each
     with its TO, and report whether the result is BYTE-EQUAL to that file's
     blob at C4. Report the sha256 of both sides.
 G8  The test-file pairs and the append, the same way. From the `a76ea1e7`
     blob of `tests/ui_server/test_sse_stream.py`, verify HELPERFROM and
     RAISEFROM each occur EXACTLY ONCE, replace each with its TO, and report
     whether the result is BYTE-EQUAL to that file's blob at C3. Then report
     that the C3 blob is a byte-exact PREFIX of the C5 blob and that the
     remainder is TWO newlines followed by TESTS13 — two, not one: that is
     constraint 2's blank-line rule measured as bytes, because no lint rule in
     this repository's configuration can see it. Report also that the lines
     `git diff C3..C5 -- tests/ui_server/test_sse_stream.py` ADDS are the two
     blank lines followed by TESTS13's lines IN ORDER, that the added-line
     count equals TESTS13's line count plus two, and that the diff REMOVES
     nothing.
 G9  The suites are green in the PRIMARY checkout, run SERIALLY, never two
     pytest processes at once. Report the exit code and `passed + skipped` of
     each, at C5:
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf` exits 0.
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf` exits 0.
     `python3 -m pytest tests/docs/ -q -rf` exits 0 and sums to 295.
     RECONCILE THE ARITHMETIC RATHER THAN ASSERTING A BARE TOTAL: report the
     number of lines matching `^    def test_` in TESTS13, and report that the
     first sum equals 40 plus that number and the second equals 440 plus the
     same number, 40 and 440 being constraint 8's base readings. If any of the
     three identities fails, report the real values and stop.
 G10 RED PROOF — the colour, never a count. In a DISPOSABLE worktree under
     `.remedy-wt/`, created with `git worktree add --detach` at C5 and removed
     before the handback: write the `a76ea1e7` blob of
     `packages/orchestration/ui_server.py` into that worktree's copy with
     `git show`, leaving the tests at C5, and report the exit code of
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf` run THERE.
     It EXITS NON-ZERO. Report how many tests failed and name two of them, but
     no count is ordered. Then restore that file to its C4 blob the same way
     and report that the same command EXITS 0. Some new tests SURVIVE the
     revert by design — the ones asserting the query-cursor fallback, which
     the old route already served — so the colour is the claim and the
     survivors are reported, not explained away. The PRIMARY checkout is never
     touched by this gate.
 G11 Ruff, scoped to the two touched files and compared as a MULTISET of rule
     codes rather than as an exit code, base against head. Run
     `python3 -m ruff check --output-format concise` over
     `packages/orchestration/ui_server.py` and
     `tests/ui_server/test_sse_stream.py` at C5, and over the SAME two paths
     at `a76ea1e7` by feeding each base blob through
     `git show a76ea1e7:<path> | python3 -m ruff check --output-format concise --stdin-filename <path> -`
     so `per-file-ignores` still resolves by path and no file is overwritten
     (§3 item 29). Report both multisets; they are EQUAL and both EMPTY.
     CONTROL, through the SAME extractor: feed a deliberately unused import to
     ruff on stdin and report that the extractor yields a NON-EMPTY multiset
     at a non-zero exit. A multiset reader that cannot show a finding has not
     been shown to read findings (R-0463).
 G12 Range. With BASE `a76ea1e7`, `git diff --name-only BASE..C6` equals the
     Change list above with no path on either side alone. Every commit in
     BASE..C6 has exactly one parent. For every commit BEFORE C6 report BOTH
     numstat figures per path — insertions AND deletions — from
     `git show --numstat`, report that every insertion count is under 500, and
     compare EVERY CELL against the `+/-` column of the handback's
     `## Commits` table, both sides read from `git diff --numstat` and never
     from a file's line counts before and after. BOTH cells of each row are
     compared, not the insertion alone: that half-width reading is finding
     R-0619, registered by this very round, and a gate that repeats it would
     be the third instance of the same class. C6's own numbers belong to the
     round report (R-0149).
 G13 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2,
     `tests/ui_server/test_sse_stream.py` at C5,
     `packages/orchestration/ui_server.py` at C4 and `.agent/handoff.md` at
     C6. Every count is 0.
 G14 History. Over this round's OWN reflog entries, report the count whose
     OPERATION — the text before the first `:` in `git reflog --format=%gs` —
     is `amend`, `rebase` or `cherry`; it is 0. Count by operation, never by
     substring; no total is asserted.
 G15 The branch is pushed and NO pull request exists. Report the real output
     of `git push` and of
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
     which returns an empty list. Nothing is merged this round.
 G16 Handback. `.agent/handoff.md` at C6 carries the sections
     docs/agents/handback_template.md mandates and an item-status table naming
     C0a, C0b, C1, C2, C3, C4, C5 and C6 exactly once each. Report its line
     count; the cap is 100, this round having more than five commits, and an
     overage carries a DECISION D15 stated-cause line naming the mandated
     content that caused it. Its `## Next` section states that the next
     session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and
     its SECOND the Open PR Gate (Phase 1 rule 2), and that the next round is
     R14, whose work is T002's forced-disconnect hammer.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 55 % (F008 beansprucht · dreizehn Urteile im Ledger ·
            T001 KOMPLETT · T002 BEGONNEN: die Resume-Entscheidung als eigene
            Funktion, Header schlaegt Cursor, Header ist exklusiv und Cursor
            inklusiv, Fallback statt Ablehnung bei kaputtem Header · R14 bringt
            den Trennungs-Hammer · dann T003 Client-Hook und Fallback) —
            Schaetzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R13
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
R13 begins T002 with the resume decision itself. `Last-Event-ID` names the last
frame a client ALREADY holds, so the span it missed starts one PAST it, while
the query cursor names the position to start AT; conflating the two yields a
duplicate or a gap, and the acceptance test forbids both. `resolve_sse_start`
holds that rule alone, the stream branch resolves both inputs before entering
the writer, and a header that is absent, blank or mangled falls back to the
cursor rather than refusing the stream. R13 also records the R12 verdict and
registers R-0619.

## Next Steps
1. R14 adds T002's forced-disconnect hammer: kill the connection mid-stream N
   times and require the client transcript to byte-equal the ledger's envelope
   sequence.
2. Then T003's client hook, backoff, gap detection and polling fallback, then
   the integration gate before closure.

## Risks
- The slot registry is process-global mutable state. Every test that acquires a
  slot clears it first and the release runs in a `finally`; if either
  discipline lapses, a leaked slot makes a later round's 429 test pass for the
  wrong reason.
- A `_RemedyHandler` built with `__new__` carries no `headers`, so every test
  driving `do_GET` into the stream branch must set it. R13 sets it in the
  shared `_dispatch` helper and in the one test that builds its own handler.
- No open finding is a code defect of F008. R-0403, R-0607 through R-0609,
  R-0611 and R-0613 through R-0619 stay routed to a paydown branch, with the
  fix clauses of R-0387 and R-0573 promoted into the §3 checklist.
<<<END PLANF008R13

<<<SLICE LEDGER13
- R-0619 — Low — A GATE ORDERED A TWO-COLUMN COMPARISON AND SUPPLIED ONE COLUMN, SO HALF THE VALUE §3 ITEM 28 EXISTS TO PROTECT WENT UNREAD. G8 of the F008 R12 block, saved at `4f3ae2f7`, orders each pre-handback commit's INSERTION count read from `git show --numstat` and then "compare them cell by cell against the `+/-` column of the handback's `## Commits` table, reporting agreement". That column carries TWO figures per row and the ordered reading supplies one, so the deletion cells are unreachable by construction: the handback could have stated any deletion figure at all and the gate would still have reported agreement, because there was no second value to disagree with. Item 28 exists precisely for this column — it was added as the counter-measure to R-0592, where a `## Commits` row read `+380/-334` against a real numstat of `270 224`, a row whose BOTH cells were wrong — and item 28's own text requires the two readings compared "cell by cell", so this is item 28 applied at half width rather than a gap in item 28. WHY LOW, and the reason is a measurement rather than a hope: the reviewer re-derived both columns itself at `a76ea1e7` and the four measurable commits read insertions 194, 109, 12 and 4 against deletions 0, 379, 10 and 0, while the table states `+194/-0`, `+109/-379`, `+12/-10` and `+4/-0` — every cell agrees, deletions included, so nothing downstream consumed a wrong number. THE R12 WORKER FOUND IT: it applied G8 exactly as written, reported the insertion agreement it was asked for, and declared in `## Deviations & assumptions` that the deletion cells were unchecked by construction rather than quietly widening the gate to cover the reviewer — the same behaviour that turned a reviewer slip into R-0618 one round earlier, and the second consecutive round in which the worker's declaration is the only reason a reviewer-text defect is on the record at all. THE COUNTER-MEASURE IS APPLIED BY THIS ROUND RATHER THAN DEFERRED: G12 below orders EVERY cell the handback column carries, insertion and deletion per path, each stated as the tool's own output. The checklist edit that generalises it — a gate comparing a handback column against a tool reads every cell that column carries — routes to a paydown branch with the other reviewer-text findings, because `docs/agents/planner_reviewer_prompt.md` is outside this feature's path set.

Gate: R13 — the R12 entry. R12 PASSED with NO finding against its work, and R-0619 above is against the reviewer's own block text rather than the round. R12 was the session-closing state round: it recorded the R11 verdict, registered R-0618 and wrote the handback that ended that session at its round cap, writing no production code. THE REVIEWER RE-DERIVED EVERY GATE ITSELF at `a76ea1e7`, from its own runs, rather than reading the handback's numbers back. TRANSPORT EQUAL across both committed copies — `.agent/authored/f008-r12.md` at `4f3ae2f7` and `.agent/last_block.md` at `4710ab5c` — at sha256 c9a76da738e79f6af016b201ab12bcd793fb597fd235718b35a21420ce4ded35 over 18179 bytes and 194 lines; the scratch original died with the session that authored it, so two copies are the most any later reader can compare and the handback's third reading is not re-derivable by construction. TWO SLICES by the reviewer's own ordered extraction out of the committed C0a file, newline-included, both digests matching: PLANF008R12 4be6110c and LEDGER12 61291f86. THE PLAN LANDED FIRST at `91b46c86`, byte-equal to PLANF008R12 at 45 lines under the 50-line cap, `## Goal` and `## Next Steps` once each and `F008` twice, which is §3 checklist item 23 met rather than claimed. THE LEDGER APPEND at `4f75a7bd` is a byte-exact prefix plus a 6098-byte remainder equal to a newline plus LEDGER12, agreed by an INDEPENDENT blank-line split into 206 units whose LAST TWO equal LEDGER12's two paragraphs in order, with a one-byte flip REJECTED by both readings and the unflipped value ACCEPTED by both. The registered set moved 189 to 190 with zero `Done:` and zero `Landed:` lines at both commits, `Gate: R` going 11 to 12 over twelve DISTINCT keys R1 through R12, R-0618 appearing exactly once and R-0619 nowhere, so exactly the one ordered id was minted; the header sweep matches eleven of the twelve against `^Gate: R(\d+) — the R(\d+) entry\.` with the second number one less than the first and the R12 pair exactly once, the single non-match being `Gate: R1 — the F255 R21 entry.`, which gated the previous feature's last round and has no F008 predecessor by construction. FIVE single-parent commits whose insertions read 194, 109, 12 and 4 before the handback commit, every one under the 500-line cap, agreeing cell by cell with the handback's `## Commits` column on the insertion figure — and, re-derived beyond what G8 ordered, on the deletion figure too at 0, 379, 10 and 0, which is finding R-0619 above. ZERO marker lines in any of the three targets, a reflog whose operations over this round's own entries carry `amend`, `rebase` and `cherry` at 0 each, a 64-line handback carrying every mandated section, an item-status table naming C0a through C3 once each and a DECISION D15 stated-cause line for the four lines by which five per-commit tables push it past the 60-line cap. THE RUNS ARE THE REVIEWER'S OWN, serially in the primary checkout: the state readers exit 0 at 440 passed plus 0 skipped and `tests/docs/` exits 0 at 295 plus 0, both sums equal to the ordered values. The tree is clean with the primary checkout the only worktree, the branch is pushed at `a76ea1e7` and `gh pr list --state open` returns an empty list.
<<<END LEDGER13

<<<SLICE RESOLVEFROM
        live = _SSE_SLOTS_PER_JOB.get(job_id, 0) - 1
        if live > 0:
            _SSE_SLOTS_PER_JOB[job_id] = live
        else:
            _SSE_SLOTS_PER_JOB.pop(job_id, None)
<<<END RESOLVEFROM

<<<SLICE RESOLVETO
        live = _SSE_SLOTS_PER_JOB.get(job_id, 0) - 1
        if live > 0:
            _SSE_SLOTS_PER_JOB[job_id] = live
        else:
            _SSE_SLOTS_PER_JOB.pop(job_id, None)


#: The header a reconnecting EventSource sends back. Named once so the wire
#: spelling and the code that reads it cannot drift apart.
SSE_LAST_EVENT_ID_HEADER = "Last-Event-ID"


def resolve_sse_start(last_event_id: Any, cursor: str) -> int:
    """The ledger position a stream resumes at: header first, query second.

    The two inputs do NOT mean the same thing, which is the whole reason this
    is a function. `Last-Event-ID` names the last frame the client ALREADY
    holds, so the span it missed begins at that position PLUS ONE, while
    `cursor` names the position to start AT. Reading them as one number
    replays the client's last event on every reconnect or skips the first
    unseen one — a duplicate or a gap, and the acceptance test for this
    feature forbids both. A header that is absent, blank or not a position
    falls back to the cursor rather than refusing the stream: a proxy that
    mangled the header must not cost a client its connection.
    """
    text = str(last_event_id or "").strip()
    if text.isdigit():
        return int(text) + 1
    return int(cursor) if cursor.isdigit() else 0
<<<END RESOLVETO

<<<SLICE ROUTEFROM
                self._send_sse_stream(job, (qs.get("cursor") or ["0"])[0])
            finally:
                release_sse_slot(str(job.id))
<<<END ROUTEFROM

<<<SLICE ROUTETO
                # Resolved BEFORE the writer is entered: header-versus-query
                # precedence is a routing question, and `_send_sse_stream`
                # takes ONE start position rather than two candidate ones.
                start = resolve_sse_start(
                    self.headers.get(SSE_LAST_EVENT_ID_HEADER),
                    (qs.get("cursor") or ["0"])[0],
                )
                self._send_sse_stream(job, str(start))
            finally:
                release_sse_slot(str(job.id))
<<<END ROUTETO

<<<SLICE HELPERFROM
def _dispatch(monkeypatch: Any, path: str, job: Any, err: Any) -> tuple[list, list]:
    """Drive `do_GET` on a socketless handler and record what it answered."""
    monkeypatch.setattr(mod, "_load_job", lambda jid: (job, err))
    handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
    handler.server_token = "tok"
    handler.target_job_id = ""
    handler.path = path
<<<END HELPERFROM

<<<SLICE HELPERTO
def _dispatch(monkeypatch: Any, path: str, job: Any, err: Any,
              headers: dict[str, str] | None = None) -> tuple[list, list]:
    """Drive `do_GET` on a socketless handler and record what it answered."""
    monkeypatch.setattr(mod, "_load_job", lambda jid: (job, err))
    handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
    handler.server_token = "tok"
    handler.target_job_id = ""
    handler.path = path
    # A real handler always carries `headers`; one built with `__new__` does
    # not, and the stream branch now reads it.
    handler.headers = headers or {}
<<<END HELPERTO

<<<SLICE RAISEFROM
        handler.path = "/api/jobs/J/events/stream?token=tok"
        handler._send_json = lambda code, data: None
        handler._send_sse_stream = boom
<<<END RAISEFROM

<<<SLICE RAISETO
        handler.path = "/api/jobs/J/events/stream?token=tok"
        handler.headers = {}
        handler._send_json = lambda code, data: None
        handler._send_sse_stream = boom
<<<END RAISETO

<<<SLICE TESTS13
class TestResumeStart:
    """T002's resolver: the ledger position a reconnecting client resumes at."""

    def test_a_last_event_id_resumes_one_past_the_event_it_names(self):
        # The header names what the client ALREADY has, so starting AT it
        # would hand the same event over twice.
        assert mod.resolve_sse_start("4", "0") == 5

    def test_the_header_beats_the_query_cursor(self):
        # A reconnect carries the stale query string it first connected with
        # and a header the browser keeps current.
        assert mod.resolve_sse_start("9", "3") == 10

    def test_event_id_zero_is_a_position_and_not_an_absence(self):
        # The first event is 0; a truthiness test here would resume at 0 and
        # replay it for ever.
        assert mod.resolve_sse_start("0", "7") == 1

    def test_an_absent_header_falls_back_to_the_cursor(self):
        assert mod.resolve_sse_start(None, "6") == 6

    def test_a_blank_header_falls_back_to_the_cursor(self):
        assert mod.resolve_sse_start("   ", "6") == 6

    def test_a_mangled_header_falls_back_rather_than_refusing(self):
        assert mod.resolve_sse_start("not-a-seq", "6") == 6

    def test_a_negative_header_is_not_a_position(self):
        assert mod.resolve_sse_start("-1", "6") == 6

    def test_the_cursor_is_a_start_and_is_never_incremented(self):
        # Only the header is exclusive; conflating the two is the defect this
        # whole function exists to prevent.
        assert mod.resolve_sse_start(None, "7") == 7

    def test_neither_input_starts_at_the_beginning(self):
        assert mod.resolve_sse_start(None, "junk") == 0

    def test_surrounding_whitespace_is_tolerated(self):
        assert mod.resolve_sse_start(" 4 ", "0") == 5


class TestResumeSpan:
    def test_the_replayed_span_is_exactly_the_events_the_client_missed(self):
        # Six in the ledger and two already delivered: 3, 4 and 5 are owed.
        # Neither a duplicate of 2 nor a gap at 3 is acceptable.
        start = mod.resolve_sse_start("2", "0")
        frames = _run(lambda: _events(6), start, 1, _Clock())
        assert [_parse(f)["id"] for f in frames] == ["3", "4", "5"]

    def test_a_client_that_is_current_is_owed_no_event(self):
        start = mod.resolve_sse_start("5", "0")
        frames = _run(lambda: _events(6), start, 1, _Clock())
        assert [f for f in frames if not f.startswith(b":")] == []


class TestResumeRoute:
    def setup_method(self):
        mod._SSE_SLOTS_PER_JOB.clear()

    def test_the_header_reaches_the_writer_as_the_next_position(self, monkeypatch):
        _answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None,
            headers={"Last-Event-ID": "4"})
        assert streamed[0][1] == "5"

    def test_without_a_header_the_query_cursor_still_decides(self, monkeypatch):
        _answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok&cursor=7", _Job(), None)
        assert streamed[0][1] == "7"

    def test_the_header_overrides_the_cursor_on_the_wire(self, monkeypatch):
        _answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok&cursor=7", _Job(), None,
            headers={"Last-Event-ID": "1"})
        assert streamed[0][1] == "2"

    def test_a_mangled_header_still_serves_the_stream(self, monkeypatch):
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok&cursor=3", _Job(), None,
            headers={"Last-Event-ID": "??"})
        assert answered == []
        assert streamed[0][1] == "3"

    def test_the_header_name_is_the_one_the_browser_sends(self):
        # EventSource sends exactly this spelling; a rename breaks resume in
        # silence, because the fallback path still serves a valid stream.
        assert mod.SSE_LAST_EVENT_ID_HEADER == "Last-Event-ID"
<<<END TESTS13
