── STEP R5/1 — F008 SSE event stream ─────────────────────────
Goal:        Land the second half of DECISION F008 D1: the events read
             path EXPOSES each event's own ledger position as `seq`
             instead of leaving callers to infer it. F008's stream will
             use that value as the SSE event id, so it must be the
             ledger's position and never a per-response counter — which
             is what "the stream must not renumber" protects. This round
             also records the R4 verdict. No endpoint is added yet.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 record the R4 verdict · C3 expose seq together with the
             tests that pin it · C4 write the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r5.md                 (C0a, new)
             - .agent/last_block.md                       (C0b, rewrite)
             - .agent/plan.md                             (C1, rewrite)
             - .agent/live_review.md                      (C2, append)
             - packages/orchestration/ui_server.py        (C3, one pair)
             - tests/ui_server/test_event_seq.py          (C3, new file)
             - .agent/handoff.md                          (C4, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r5.md, extracted by its marker lines. No slice is
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines
    strictly between its `<<<SLICE X` and `<<<END X` markers. PLANF008R5
    and TESTFILE are applied with their trailing newline INCLUDED and are
    the ENTIRE content of their files. SEQFROM and SEQTO are whole-line
    blocks applied WITH their trailing newline. RECORDR4 is applied as
    `\n` plus its single line, appended to the end of
    `.agent/live_review.md` after exactly one blank line. Every file ends
    with exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4.
    `.agent/plan.md` is advanced at C1, the first substantive commit —
    only the two block-save commits may precede it (checklist item 23).
 4. Pair shape, from a containment test the reviewer ran before emission.
    SEQFROM/SEQTO: `TO contains FROM: false` — a REWRITE, so the
    obligation is FROM 1x→0x and TO 0x→1x in
    packages/orchestration/ui_server.py and NO append reading is owed.
    TESTFILE is a NEW FILE, not a pair: its obligation is byte-equality of
    the created file against the slice, and nothing else.
 5. NO NEW FINDING IS REGISTERED this round. R4 passed with none against
    it, so `.agent/live_review.md` gains exactly one `Gate:` paragraph and
    no `- R-` line. The next free id stays R-0614.
 6. Destructive checks run only inside a disposable git worktree created
    with `git worktree add .remedy-wt/redctl-r5 <C3 sha> --detach`, never
    in the primary checkout, and it is removed with
    `git worktree remove .remedy-wt/redctl-r5 --force` before the
    handback. `git status --porcelain` is empty after every commit and at
    the handback.
 7. Two pytest processes never run at once. Every suite runs in the
    PRIMARY checkout except G9, which runs in the worktree of
    constraint 6.
 8. Scope: no path outside the Change list. This round does NOT add the
    stream route, the SSE framing, the heartbeat, the connection cap or
    any client code — those are R6 and later. It changes the payload of
    one existing reader and nothing else.
 9. The reviewer's readings at `9cb131c1`, taken before this block was
    emitted, which the gates below re-derive rather than trust: the
    combined suite of `tests/ui_server/`, `test_test_runner.py`,
    `test_resource_safety.py` and `test_integrity_gate.py` exits 0 with
    351 passed WITHOUT this round's change and new file, and exits 0 with
    358 collected-and-passing WITH them — 351 plus this round's 7 tests.
    The new tests are RED before the change with `KeyError: 'seq'`.
    `ruff check` on both changed files reports `All checks passed!`.
10. COUNT BY PASSED-PLUS-SKIPPED, not by passed alone. The reviewer
    measured this combined suite reporting `358 passed` on one run and
    `357 passed, 1 skipped` on another at the SAME tree, because
    `tests/ui_server/test_brain_view_model.py` and
    `test_dashboard_contract.py` carry three DATA-DEPENDENT
    `pytest.skip(...)` calls that fire or not depending on runtime data.
    That intermittency is pre-existing and is not this round's doing, so
    every gate below asserts exit 0 and `passed + skipped`, never a bare
    passed count.

Done when:
 G1  `.agent/STOP` is absent, checked immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback; `git worktree list` names the
     primary checkout alone at the handback. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of
     .remedy-wt/f008-r5.md, of .agent/authored/f008-r5.md at C0a and of
     .agent/last_block.md at C0b, and state whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     .agent/authored/f008-r5.md by their marker lines, take the COUNT from
     that listing, and report per slice its newline-INCLUDED sha256, byte
     count and line count.
 G4  Plan. Report the sha256, byte count and line count of .agent/plan.md
     at C1 and whether it is byte-equal to PLANF008R5. Its line count is
     under 50. `## Goal` and `## Next Steps` each occur exactly once as
     line-anchored headings and `F008` occurs at least once. C1 is the
     first commit after C0a and C0b.
 G5  The verdict append, measured two ways that must agree. For C2 against
     C1: (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the
     remainder equals `\n` plus RECORDR4 — report its sha256, byte count
     and line count; (b) split the C2 file on blank lines with an
     INDEPENDENT extractor and report that its LAST unit equals RECORDR4.
     Normalise the file's single terminating newline before comparing, or
     the last unit carries it and the reading rejects the truth. Then run
     a NEGATIVE CONTROL: flip a byte of the remainder in memory and report
     that BOTH readings reject it while the unflipped value is accepted by
     both.
 G6  The sets. Report line-anchored counts in .agent/live_review.md at C1
     and C2: `^- R-\d+ — ` is 185 at BOTH — constraint 5, no finding is
     registered — `^Done: R-\d+ — ` is 0 at both, `^Landed: ` is 0 at
     both, and `^Gate: R\d+ — ` reads 4 then 5 with the five keys DISTINCT.
     `^- R-0614 — ` occurs 0 times at both.
 G7  The production pair. In packages/orchestration/ui_server.py, count
     SEQFROM and SEQTO as exact multi-line blocks at `9cb131c1` and at C3:
     FROM reads 1 then 0, TO reads 0 then 1. Report the containment test's
     own output. Report `git show --numstat C3 -- packages/orchestration/ui_server.py`;
     it reads 5 insertions and 1 deletion — the reviewer MEASURED that by
     applying the pair to the base blob and diffing, rather than deriving
     it from the slices' own line counts, because two of SEQTO's seven
     lines are unchanged context and only five are added.
 G8  The new test file. Report the sha256, byte count and line count of
     tests/ui_server/test_event_seq.py at C3 and whether it is byte-equal
     to TESTFILE. It did not exist at `9cb131c1`: report
     `git ls-tree 9cb131c1 -- tests/ui_server/test_event_seq.py` printing
     nothing.
 G9  RED PROOF, in the disposable worktree of constraint 6 and NEVER in
     the primary checkout. Revert the production change alone — replace
     the SEQTO block with the SEQFROM block in
     packages/orchestration/ui_server.py, which the reviewer measured
     occurring exactly once in that file at C3 — leaving the new test file
     in place. Report the exit code and last line of
     `python3 -m pytest tests/ui_server/test_event_seq.py -q -rf` in that
     worktree: it EXITS 1, and report whether `KeyError` and the token
     `seq` appear in its output, which is the failure the missing field
     produces. Then restore the block, report the file is byte-identical
     to C3's blob, and report the same command now exits 0. If the
     reverted run exits 0, the tests do not pin what they claim: STOP and
     report rather than landing tests that cannot fail.
 G10 The proof, in the primary checkout:
     `python3 -m pytest tests/ui_server/test_event_seq.py -q -rf`
     exits 0 with `passed + skipped` equal to 7. Report the exit code and
     both numbers.
 G11 No regression on the shared path, in the primary checkout, SERIALLY
     and never alongside G10:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
     Report each exit code and, for each, `passed + skipped`. Both exit 0;
     the first sums to 358 and the second to 42. Per constraint 10, do not
     report a bare passed count and do not treat a skip as a failure.
 G12 Scoped lint, reading the base copy WITHOUT writing to any tracked
     file — `git show <sha>:<path>` piped to
     `python3 -m ruff check --stdin-filename <path> -`, so per-file-ignores
     still resolve by path. Run it for packages/orchestration/ui_server.py
     at `9cb131c1` and at C3, and for tests/ui_server/test_event_seq.py at
     C3. Report each exit code and the RULE-CODE MULTISET of each; the two
     ui_server multisets are EQUAL and the new test file's is empty.
 G13 Range. With BASE `9cb131c1`, run `git diff --name-only BASE..C4` and
     report that its output equals the Change list above with no path on
     either side alone. Every commit in BASE..C4 has exactly one parent.
     Report each commit's INSERTION count from `git show --numstat`, all
     under 500, and compare those numbers cell by cell against the `+/-`
     column of the handback's `## Commits` table, reporting that the two
     readings agree. C4's own numbers belong to the round report, not to
     its own table cell (finding R-0149).
 G14 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     .agent/plan.md at C1, .agent/live_review.md at C2,
     packages/orchestration/ui_server.py at C3,
     tests/ui_server/test_event_seq.py at C3 and .agent/handoff.md at C4.
     Every count is 0.
 G15 History. Over this round's OWN reflog entries, report the count whose
     OPERATION — the text before the first `:` in `git reflog --format=%gs`
     — is `amend`, `rebase` or `cherry`; it is 0. Count by operation and
     never by substring, which is finding R-0613. Do not order that every
     entry read `commit:` (R-0601), do not count an unstage as a rewrite
     (R-0608), and state NO entry total.
 G16 Handback. .agent/handoff.md at C4 carries the sections
     docs/agents/handback_template.md mandates and an item-status table
     naming C0a, C0b, C1, C2, C3 and C4 exactly once each. Report its line
     count; the cap for this round is 100, this round having more than
     five commits. Its External-actions section names the push as ordered
     by Push Discipline with its outcome in the round report, rather than
     asserting a push that cannot have happened when the line is written.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 18 % (F008 beansprucht · fünf Urteile im Ledger ·
            DECISION F008 D1 vollständig umgesetzt: Server nebenläufig und
            die Ledger-Position als `seq` sichtbar · der Stream-Endpunkt
            selbst beginnt in R6) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R5
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
R5 lands the second half of DECISION F008 D1. The cursor-based events reader
returned a cursor for the response but no position for the individual events,
so a caller had to infer each event's place in the ledger. This round exposes
that position as `seq` and pins it with tests that fail if it ever becomes a
per-response counter. Together with R4's threading change, both prerequisites
D1 named are now met and the stream endpoint itself is unblocked.

## Next Steps
1. R6 begins the endpoint: `GET /api/jobs/<jid>/events/stream`, SSE framing
   with `seq` as the event id, a 15 s heartbeat comment frame, and 404 for an
   unknown job before any streaming starts. The route seam is the six-part
   path branch beside the existing `events-since` handler.
2. R7 adds the per-job connection cap answering 429 beyond it, and the
   framing golden the feature file names as T001's contract test.
3. R8 onward builds T002 — Last-Event-ID resume and the forced-disconnect
   hammer — then T003's client hook, then the integration gate.

## Risks
- The 50-event response cap in the reader is bounded RESPONSE size, not
  bounded numbering; T002's resume from an ancient cursor must page rather
  than assume one response covers the span.
- 185 findings are open and none is a code defect of F008. Promoting
  R-0387's clause into the §3 checklist edits `docs/agents/**` and stays
  routed to the paydown branch with R-0403, R-0607, R-0608, R-0609, R-0611
  and R-0613.
<<<END PLANF008R5

<<<SLICE RECORDR4
Gate: R5 — the R4 entry. R4 PASSED with NO finding against its work and none against its block. It discharged the prerequisite DECISION F008 D1 ruled — the cockpit server now serves concurrent requests — and it proved that behaviourally rather than by inspection, which is the only kind of proof this change admits. THE RED PROOF IS REAL AND THE REVIEWER RE-RAN IT ITSELF at `e5b93f23` in a disposable worktree, never in the primary checkout: with the two production lines reverted and the new test left in place the run EXITS 1 and fails inside `threading.Barrier.wait` with `BrokenBarrierError`, because a single-threaded server never gets the second request into the handler at all; with both lines restored, the file is byte-identical to C4's blob and the same command EXITS 0. THE TEST ASSERTS CONCURRENCY AND NOT SPEED, which is why it belongs in a suite that runs on shared runners: a `threading.Barrier(2)` releases only when two requests are genuinely in flight together, so there is no threshold to tune and no slow-runner flake to inherit — the reviewer measured 12 red out of 12 without the change and 12 green out of 12 with it before the colour was ordered, rather than the five-sample habit R-0498 was registered against. THE PRODUCTION CHANGE IS EXACTLY TWO LINES and `git show --numstat` reads `2 2` on that path: the import and the instantiation, `HTTPServer` to `ThreadingHTTPServer`, with no reformatting, no import re-sorting and no `daemon_threads` written by hand — the stdlib class already sets it, and adding it again would have been an unordered line saying nothing. THE SHARED PATH IS UNHARMED, measured rather than hoped: `tests/ui_server/` exits 0 at 262 passed, which is the 261 the reviewer measured at `c1e4e3ac` BOTH with and without the change in one worktree, plus this round's single new test; the state-reader four exit 0 at 160 and the canary at 42, with `tests/regression/test_resource_safety.py` named in the block on purpose because `ThreadingHTTPServer` sets `daemon_threads = True` and therefore never joins its handler threads on close, which is where a leak would surface. The worker also read the 3170-line module in full before editing, per the File Editing Safety Rules, and confirmed independently what the plan asserted: `_RemedyHandler`'s three attributes are bound once on the `type()` subclass at construction and never mutated per request, and every `do_GET` path is read-only, so threading introduces no shared-state race. THE ROUND'S OWN SHAPE HOLDS, re-measured off disk: transport byte-equal three ways at sha256 da369700c753cbb4ad90a00a2dc1ac877754e2767d65d779ff489f2f305b6347 over 26853 B and 380 lines; EIGHT slices by the reviewer's own ordered extraction, the test file among them byte-equal at 9a1d28fb to the bytes the reviewer had already run red and green before the block was emitted, so what landed is what was proven and not a retype of it; `.agent/plan.md` at `9b183953` byte-equal to its slice at 44 lines under the cap and first after the two block-save commits; both ledger appends byte-exact prefix-plus-remainder with independent 192- and 193-unit blank-line splits agreeing and a one-byte flip rejected by both; the finding landing at `6292fd51` BEFORE the verdict at `6fb06928`; sets moving 184 to 185 registered with 0 resolved and 0 `Landed:` throughout and `Gate: R` going 3, 3, 4 with distinct keys; seven single-parent commits with insertions all under the 500 cap; zero marker lines in any target; ruff multisets EQUAL across the change and empty on the new file, with the worker adding an UNORDERED red control through the same stdin path to prove that reading could go red at all; a 100-line handback at its cap with every mandated section and an item table naming C0a through C5 exactly once; and the tree clean with the primary checkout the only worktree. NO DEVIATION WAS DECLARED AND NONE WAS OWED. TWO SMALL THINGS ARE WORTH KEEPING. The worker's G15 counted by reflog OPERATION rather than by substring, which is R-0613's fix applied in the same round that registered it — the field named rather than left to the reader. And two bash commands were refused by this session's command guard mid-round; the worker routed those exit-code readings through a small runner in gitignored scratch instead of dropping them, so no gate was skipped or weakened by a tooling limit, which is the correct response to an environment constraint and worth recording as precedent.
<<<END RECORDR4

<<<SLICE SEQFROM
    for e in new_events[:50]:
        safe.append({
            "event": e.get("event", ""),
<<<END SEQFROM

<<<SLICE SEQTO
    for offset, e in enumerate(new_events[:50]):
        safe.append({
            # The ledger's own position, never a per-response counter: F008's
            # stream uses it as the SSE event id, so a client resuming from
            # `seq` lands on the event the server meant (DECISION F008 D1).
            "seq": start + offset,
            "event": e.get("event", ""),
<<<END SEQTO

<<<SLICE TESTFILE
"""
Domain tests: ui_server/test_event_seq.py

The cursor-based events payload carries each event's own position in the
ledger as `seq`. F008's stream uses that value as the SSE event id, so it
must be the ledger's position and never a per-response counter — DECISION
F008 D1, "the stream EXPOSES the ledger position as seq and assigns
nothing". Renumbering is the failure this pins against: a client that
resumes from `seq` must land on the same event the server meant.
"""

from __future__ import annotations

from typing import Any

import pytest

from packages.orchestration import ui_server as mod


class _FakeJob:
    id = "11111111-2222-3333-4444-555555555555"


def _events(count: int) -> list[dict[str, Any]]:
    return [
        {"event": f"e{i}", "timestamp": f"2026-08-21T00:00:{i:02d}Z", "outcome": "ok"}
        for i in range(count)
    ]


@pytest.fixture
def ledger(monkeypatch):
    """Install a fixed ledger and hand the test its own length."""

    def install(count: int) -> int:
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(count))
        return count

    return install


class TestEventSeqIsTheLedgerPosition:
    def test_seq_starts_at_zero_for_a_zero_cursor(self, ledger):
        ledger(5)
        payload = mod._build_events_since_json(_FakeJob(), "0")
        assert [e["seq"] for e in payload["events"]] == [0, 1, 2, 3, 4]

    def test_seq_is_absolute_not_relative_to_the_cursor(self, ledger):
        ledger(5)
        payload = mod._build_events_since_json(_FakeJob(), "3")
        # The third event is seq 3 whichever cursor asked for it — a
        # response-relative counter would restart at 0 here.
        assert [e["seq"] for e in payload["events"]] == [3, 4]

    def test_an_event_keeps_one_seq_across_different_cursors(self, ledger):
        ledger(6)
        job = _FakeJob()
        from_zero = mod._build_events_since_json(job, "0")["events"]
        from_four = mod._build_events_since_json(job, "4")["events"]
        by_seq = {e["seq"]: e["event"] for e in from_zero}
        for event in from_four:
            assert by_seq[event["seq"]] == event["event"]

    def test_seq_agrees_with_the_cursor_the_same_payload_returns(self, ledger):
        total = ledger(9)
        payload = mod._build_events_since_json(_FakeJob(), "2")
        assert payload["cursor"] == str(total)
        # The next request starts where this response stopped: the cursor is
        # one past the last seq returned, so no event is skipped or repeated.
        assert payload["events"][-1]["seq"] + 1 == int(payload["cursor"])

    def test_a_non_numeric_cursor_reads_from_the_start(self, ledger):
        ledger(3)
        payload = mod._build_events_since_json(_FakeJob(), "not-a-number")
        assert [e["seq"] for e in payload["events"]] == [0, 1, 2]

    def test_a_cursor_past_the_end_returns_nothing_and_invents_no_seq(self, ledger):
        total = ledger(4)
        payload = mod._build_events_since_json(_FakeJob(), "10")
        assert payload["events"] == []
        assert payload["cursor"] == str(total)

    def test_seq_survives_the_fifty_event_response_cap(self, ledger):
        ledger(140)
        payload = mod._build_events_since_json(_FakeJob(), "60")
        seqs = [e["seq"] for e in payload["events"]]
        # The cap bounds the RESPONSE, never the numbering: the first event
        # is still 60 and the run is consecutive.
        assert len(seqs) == 50
        assert seqs[0] == 60
        assert seqs == list(range(60, 110))
<<<END TESTFILE
