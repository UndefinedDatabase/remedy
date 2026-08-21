── STEP R4/1 — F008 SSE event stream ─────────────────────────
Goal:        Discharge the prerequisite DECISION F008 D1 ruled: make the
             cockpit server serve concurrent requests, and prove it
             behaviourally. Today one open connection blocks every other
             request, so T001's stream would deadlock the dashboard. This
             round also records the R3 verdict and registers R-0613
             against the R3 block's own reflog gate.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 register R-0613 · C3 record the R3 verdict · C4 the
             threading change together with the test that proves it ·
             C5 write the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r4.md                     (C0a, new)
             - .agent/last_block.md                           (C0b, rewrite)
             - .agent/plan.md                                 (C1, rewrite)
             - .agent/live_review.md                          (C2 and C3, appends)
             - packages/orchestration/ui_server.py            (C4, two pairs)
             - tests/ui_server/test_server_concurrency.py     (C4, new file)
             - .agent/handoff.md                              (C5, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r4.md, extracted by its marker lines. No slice is
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines
    strictly between its `<<<SLICE X` and `<<<END X` markers. PLANF008R4
    and TESTFILE are applied with their trailing newline INCLUDED and are
    the ENTIRE content of their files. IMPORTFROM, IMPORTTO, SERVERFROM
    and SERVERTO are single whole lines applied WITH their trailing
    newline, so the surrounding file structure is untouched. FIND0613 and
    RECORDR3 are each applied as `\n` plus their single line, appended to
    the end of `.agent/live_review.md` after exactly one blank line. Every
    file ends with exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5.
    `.agent/plan.md` is advanced at C1, the first substantive commit —
    only the two block-save commits may precede it (checklist item 23).
    R-0613 is registered at C2 BEFORE the verdict lands at C3, per §4.4.
 4. Pair shapes, from containment tests the reviewer ran before emission.
    IMPORTFROM/IMPORTTO: `TO contains FROM: false` — a REWRITE.
    SERVERFROM/SERVERTO: `TO contains FROM: false` — a REWRITE. Both
    therefore owe FROM 1x→0x and TO 0x→1x in
    packages/orchestration/ui_server.py, and NEITHER owes an append
    reading. TESTFILE is a NEW FILE, not a pair: its obligation is
    byte-equality of the created file against the slice, and nothing else.
 5. The production change is exactly two lines. Do not reformat, re-sort
    imports, or touch any other line of ui_server.py. In particular do NOT
    set `daemon_threads` by hand: the reviewer measured that
    `http.server.ThreadingHTTPServer` already defines
    `daemon_threads = True`, so writing it again would add an unordered
    line that says nothing.
 6. Destructive checks run only inside a disposable git worktree created
    with `git worktree add .remedy-wt/redctl-r4 <C4 sha> --detach`, never
    in the primary checkout, and it is removed with
    `git worktree remove .remedy-wt/redctl-r4 --force` before the
    handback. `git status --porcelain` is empty after every commit and at
    the handback.
 7. Two pytest processes never run at once. Every suite runs in the
    PRIMARY checkout except G10, which runs in the worktree of
    constraint 6.
 8. Scope: no path outside the Change list. This round does NOT add the
    stream endpoint, a route, an envelope or a client hook — T001 begins
    next round, and DECISION F008 D1 exists precisely to keep the
    blocking-server fix and the new endpoint in separate diffs so a
    regression in either can be attributed to the right half.
 9. The reviewer's readings at `c1e4e3ac`, taken before this block was
    emitted, which the gates below re-derive rather than trust:
    `tests/ui_server/` exits 0 at 261 passed BOTH with and without the
    two-line change, measured in the same disposable worktree so the
    comparison controls for worktree conditions; the state-reader four
    exit 0 at 160 passed with the change applied; the new test is RED
    12 times out of 12 without the change and GREEN 12 times out of 12
    with it; `ruff check` on the new test file reports
    `All checks passed!`.

Done when:
 G1  `.agent/STOP` is absent, checked immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback; `git worktree list` names the
     primary checkout alone at the handback. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of
     .remedy-wt/f008-r4.md, of .agent/authored/f008-r4.md at C0a and of
     .agent/last_block.md at C0b, and state whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     .agent/authored/f008-r4.md by their marker lines, take the COUNT from
     that listing, and report per slice its newline-INCLUDED sha256, byte
     count and line count.
 G4  Plan. Report the sha256, byte count and line count of .agent/plan.md
     at C1 and whether it is byte-equal to PLANF008R4. Its line count is
     under 50. `## Goal` and `## Next Steps` each occur exactly once as
     line-anchored headings and `F008` occurs at least once. C1 is the
     first commit after C0a and C0b.
 G5  The two appends, each measured the same two ways, which must agree.
     For C2 against C1, and then for C3 against C2: (a) the earlier blob is
     a byte-exact PREFIX of the later one and the remainder equals `\n`
     plus the slice — report each remainder's sha256, byte count and line
     count; (b) split the later file on blank lines with an INDEPENDENT
     extractor and report that its LAST unit equals that slice. Normalise
     the file's single terminating newline before comparing, or the last
     unit carries it and the reading rejects the truth. Then run a
     NEGATIVE CONTROL on ONE of them: flip a byte of the remainder in
     memory and report that BOTH readings reject it while the unflipped
     value is accepted by both.
 G6  The sets. Report line-anchored counts in .agent/live_review.md at C1,
     C2 and C3: `^- R-\d+ — ` reads 184, 185, 185; `^Done: R-\d+ — ` is 0
     at all three; `^Landed: ` is 0 at all three; `^Gate: R\d+ — ` reads 3,
     3, 4. The four `Gate: R` keys at C3 are DISTINCT. `^- R-0613 — `
     occurs 0 times at C1 and exactly 1 time at C2 and C3.
 G7  The two production pairs. In packages/orchestration/ui_server.py,
     count each FROM and each TO as an exact whole line at `c1e4e3ac` and
     at C4: every FROM reads 1 then 0 and every TO reads 0 then 1. Report
     the containment test's own output for each pair. Report also that
     `git show --numstat C4 -- packages/orchestration/ui_server.py` reads
     exactly 2 insertions and 2 deletions — the change is two lines and no
     more.
 G8  The new test file. Report the sha256, byte count and line count of
     tests/ui_server/test_server_concurrency.py at C4 and whether it is
     byte-equal to TESTFILE. It did not exist at `c1e4e3ac`: report
     `git ls-tree c1e4e3ac -- tests/ui_server/test_server_concurrency.py`
     printing nothing.
 G9  The proof, in the primary checkout:
     `python3 -m pytest tests/ui_server/test_server_concurrency.py -q -rf`
     exits 0 at 1 passed. Then the whole suite it joins:
     `python3 -m pytest tests/ui_server/ -q -rf`
     exits 0 at 262 passed — the 261 the reviewer measured at `c1e4e3ac`
     plus this round's one new test. Run SERIALLY. Report both exit codes
     and both counts.
 G10 RED PROOF, in the disposable worktree of constraint 6 and NEVER in the
     primary checkout. Revert the production change alone — replace the
     single line IMPORTTO with IMPORTFROM and the single line SERVERTO with
     SERVERFROM in packages/orchestration/ui_server.py, each of which the
     reviewer measured occurring exactly once in that file at C4 — leaving
     the new test file in place. Report the exit code and last line of
     `python3 -m pytest tests/ui_server/test_server_concurrency.py -q -rf`
     in that worktree: it EXITS 1, the reviewer having measured this red
     12 times out of 12 and the green 12 out of 12, so the colour is
     ordered rather than probed. Then restore both lines, report the file
     is byte-identical to C4's blob, and report the same command now exits
     0. If the reverted run exits 0, the test does not prove what it
     claims: STOP and report rather than landing a test that cannot fail.
 G11 No regression on the shared path, in the primary checkout, SERIALLY
     and never alongside G9:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
     Report each exit code and each passed count. Both exit 0, at 160 and
     42. The resource-safety suite is named here deliberately:
     `ThreadingHTTPServer` sets `daemon_threads = True`, so `server_close`
     does not join its handler threads, and that suite is the one that
     would show a leak.
 G12 Scoped lint, reading the base copy WITHOUT writing to any tracked
     file — `git show <sha>:<path>` piped to
     `python3 -m ruff check --stdin-filename <path> -`, so per-file-ignores
     still resolve by path. Run it for packages/orchestration/ui_server.py
     at `c1e4e3ac` and at C4, and for
     tests/ui_server/test_server_concurrency.py at C4. Report each exit
     code and the RULE-CODE MULTISET of each; the two ui_server multisets
     are EQUAL, and the new test file's is empty.
 G13 Range. With BASE `c1e4e3ac`, run `git diff --name-only BASE..C5` and
     report that its output equals the Change list above with no path on
     either side alone. Every commit in BASE..C5 has exactly one parent.
     Report each commit's INSERTION count from `git show --numstat`, all
     under 500, and compare those numbers cell by cell against the `+/-`
     column of the handback's `## Commits` table, reporting that the two
     readings agree. C5's own numbers belong to the round report, not to
     its own table cell (finding R-0149).
 G14 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     .agent/plan.md at C1, .agent/live_review.md at C3,
     packages/orchestration/ui_server.py at C4,
     tests/ui_server/test_server_concurrency.py at C4 and
     .agent/handoff.md at C5. Every count is 0.
 G15 History. Over this round's OWN reflog entries, report the count whose
     OPERATION — the text before the first `:` in `git reflog --format=%gs`
     — is `amend`, `rebase` or `cherry`; it is 0. The field is named here
     because R-0613, which this round registers, is exactly the defect of
     leaving it unnamed: a commit SUBJECT containing one of those words is
     not an operation. Do not order that every entry read `commit:`
     (R-0601), do not count an unstage as a rewrite (R-0608), and state NO
     entry total.
 G16 Handback. .agent/handoff.md at C5 carries the sections
     docs/agents/handback_template.md mandates and an item-status table
     naming C0a, C0b, C1, C2, C3, C4 and C5 exactly once each. Report its
     line count; the cap for this round is 100, this round having more
     than five commits. Its External-actions section names the push as
     ordered-and-reported-in-the-round-report rather than asserting a push
     that cannot have happened when the line is written.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 14 % (F008 beansprucht · vier Urteile im Ledger ·
            Findings-Order gemessen, DECISION F008 D1 verankert · der
            Cockpit-Server bedient jetzt nebenläufige Requests, mit
            Barrier-Beweis statt Stoppuhr · T001 beginnt in R5) —
            Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R4
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
R4 discharges the prerequisite DECISION F008 D1 ruled. The cockpit server
instantiated `HTTPServer` bare and served one request at a time, so a single
long-lived SSE response would have blocked every other cockpit request for its
whole life. This round changes two lines to `ThreadingHTTPServer` and lands the
test that proves it: a `threading.Barrier` both requests must reach, which is a
fact about concurrency rather than a threshold about speed.

## Next Steps
1. R5 begins T001 proper: the stream endpoint, its 15 s heartbeat, 404 for an
   unknown job and 429 beyond the per-job connection cap, with seq read from
   the ledger position per DECISION F008 D1 and the framing golden as the
   contract test.
2. R6 builds T002: Last-Event-ID resume, gap-replay exactness and the
   forced-disconnect hammer whose transcript must byte-equal the ledger.
3. R7 onward builds T003 — the client hook, the fallback and the status
   states — and then the integration gate before closure.

## Risks
- Threading is live on a path every existing cockpit feature shares. The
  handler's three attributes are set once at construction and never mutated
  per request, so there is no shared-state race, but the state-reader four and
  the dashboard contract are the suites that would show a regression.
- 185 findings are open once R-0613 lands and none is a code defect of F008.
  Promoting R-0387's clause into the §3 checklist edits `docs/agents/**` and
  stays routed to the paydown branch with R-0403, R-0607, R-0608, R-0609,
  R-0611 and now R-0613.
<<<END PLANF008R4

<<<SLICE FIND0613
- R-0613 — Low — A GATE FORBIDDING THREE OPERATION WORDS IN THE REFLOG NEVER NAMED THE FIELD, AND A COMMIT SUBJECT CARRYING ONE OF THEM SATISFIES IT. G15 of the F008 R3 block, saved at `e0310a72`, orders "over this round's OWN reflog entries only, report the count containing `amend`, `rebase` or `cherry`; it is 0". `git reflog --format=%gs` returns ONE string per entry holding BOTH the operation and the commit subject, so the answer depends entirely on which half is searched and the block named neither. R3's own C4 carries the subject `docs(roadmap): amend F008 with the measured server and ledger state`, so over that round's nine entries the OPERATION-scoped count is 0 while a literal SUBSTRING count is 1, and both are honest answers to the sentence as written — which is the defect, a gate having exactly one correct reading and this one having two. Re-measured by the reviewer at `c1e4e3ac`: all nine entries of R3 are `commit:` operations and exactly one carries `amend` inside its subject, so the round rewrote no history and the operation-scoped 0 is the true reading. THE WORKER RESOLVED IT CORRECTLY AND PAID A COMMIT FOR IT: it reported the operation-scoped 0, noticed the ambiguity itself, and spent a further commit rewriting the G15 line to carry BOTH readings rather than leave a sentence whose truth depends on an unstated scope — the same instinct that made it correct its own handback rather than let a false line stand. THIS IS NEITHER R-0601 NOR R-0608, and the open set was searched for the DEFECT before this id was minted, as item 30 requires. R-0601 is the universal "every entry reads `commit:`" being unmeetable for any round that navigates branches; R-0608 is the clause forbidding `reset` when a bare unstage rewrites nothing. Both are about WHICH operations a gate may name, and both would still read correctly once the field were fixed; this one is about WHERE IN THE LINE the gate looks, which neither reaches. It is the R-0584 class arriving through a reflog rather than through a source comment: a text guard that cannot tell structure from content is satisfied by the content, and this repository's commit subjects deliberately discuss amends, rebases and resets because that is what its findings are about — so the collision is not a coincidence and will recur. FIX, applied in the SAME round that registers this finding, as its G15: a gate over reflog output names the FIELD it reads — the text before the first `:` in `git reflog --format=%gs` is the operation — and a forbid-a-token clause is evaluated against that operation alone, never against the whole line. WHY LOW: nothing false reached disk, no history was rewritten, the worker caught it inside its own round, and the permanent record is now more precise than the gate that produced it asked for.
<<<END FIND0613

<<<SLICE RECORDR3
Gate: R4 — the R3 entry. R3 PASSED. It discharged the findings order the F008 feature file's Orchestrator brief dispatches before anything is built, and it discharged it the way that brief intended: by MEASURING the source rather than reading the feature file's own prediction back. BOTH PREDICTIONS WERE FALSE AND THE ROUND SAID SO. The feature file stated that the stdlib server "may need a threading confirmation" and that ledger entries "already carry an index — they do by construction"; the confirmation is that the server is NOT threaded, and the entries carry NO index. The reviewer re-derived both independently at `c1e4e3ac` rather than accepting the round's word: `packages/orchestration/ui_server.py` imports `HTTPServer` at line 29 and instantiates it bare at line 3122 with a plain `type()` subclass carrying three bound attributes and no mixin; `grep -rn 'ThreadingMixIn\|ThreadingHTTPServer\|daemon_threads' packages/ apps/` prints nothing and exits 1; and `LedgerEvent`, read from the dataclass rather than counted by eye, has exactly the eight fields `event_id`, `event_type`, `job_id`, `run_id`, `timestamp`, `scope`, `outcome` and `metadata`, none of them a seq. THE ROUND MADE THE WORKER RE-DERIVE ALL THREE as its own G12 and the worker did, reporting agreement in each case, which is what keeps a slice in the permanent record from resting on the reviewer's word alone. R-0612 IS REGISTERED and the amendment landed: `docs/roadmap/features/T5_F008.md` at `b6a39da6` replaces the two predictions with the measured state, its line 1 and the `## How it fits` heading both unchanged, and DECISION F008 D1 rules the consequence in `.agent/decisions.md` — the threading change becomes a prerequisite ROUND before T001 rather than a step inside it, and the stream EXPOSES the ledger position as seq rather than assigning one. THE GATE THAT COULD HAVE BEEN VACUOUS WAS PROVED NOT TO BE: R-0493 records that `tests/docs/` asserts nothing whatever about a feature file's BODY, so this round additionally gated `tests/orchestration/test_roadmap_index.py` and ran a red control for it inside a disposable worktree — line 2 of the feature file replaced by a single word gives exit 1 at 11 failed and 19 passed, and the restored line gives exit 0 at 30 passed. A gate that cannot fail proves nothing when it passes, and this one was made to fail on purpose before it was believed. THE ROUND'S OWN SHAPE HOLDS, re-measured off disk: transport byte-equal three ways at sha256 b747d2ddabee9594cfbfd49f06f1d8f1fea784d1f06acabd519f76ee9d023cf7 over 27314 B and 334 lines; SIX slices by the reviewer's own ordered extraction — PLANF008R3 a27c392e, FIND0612 a0834654, RECORDR2 858e3116, FEATFROM 5ec91637, FEATTO a7bee3f3 and DECISION1 ff723630; `.agent/plan.md` at `65f0f845` byte-equal to its slice at 43 lines under the cap and first after the two block-save commits; BOTH ledger appends byte-exact prefix-plus-remainder with independent blank-line splits of 190 and 191 units agreeing, and a one-byte flip rejected by both readings; the finding landing at `a1720fd1` BEFORE the verdict at `0a9f495a`, which is the order §4.4 requires and not a stylistic preference; sets moving 183 to 184 registered with 0 resolved and 0 `Landed:` throughout and `Gate: R` going 2, 2, 3 as a finding paragraph and a gate paragraph each add one line of their own kind and none of the other; the DECISION heading 0 at base and 1 at C4; `tests/docs/` and `tests/orchestration/test_roadmap_index.py` exit 0 at 295 and 30, the state-reader four at 160 and the canary at 42, all serial in the primary checkout; nine single-parent commits with insertions all under the 500 cap; zero marker lines in any target; and the tree clean with the primary checkout the only worktree. TWO TRAILING CORRECTIONS ARE DECLARED AND BOTH ARE THE RIGHT CALL. The first replaces a handback line reading "No push, no PR" — a sentence C5 could not make true, because AGENTS.md Push Discipline mandates a push that necessarily follows the commit writing about it, the R-0149 shape reaching the External-actions section instead of the commits table. The second replaces the G15 line, which had reported only its operation-scoped reading; that ambiguity is the reviewer's gate defect and is registered as R-0613 in the entry above this one. In both cases the worker replaced a false sentence rather than leaving it standing or quietly correcting a numeral into a second wrong one, and each correction touches `.agent/handoff.md` alone, a path already in the round's change set. A round that spends two commits to keep its own record true is behaving exactly as this workflow is built to reward.
<<<END RECORDR3

<<<SLICE IMPORTFROM
from http.server import BaseHTTPRequestHandler, HTTPServer
<<<END IMPORTFROM

<<<SLICE IMPORTTO
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
<<<END IMPORTTO

<<<SLICE SERVERFROM
    server = HTTPServer((host, port), handler_class)
<<<END SERVERFROM

<<<SLICE SERVERTO
    server = ThreadingHTTPServer((host, port), handler_class)
<<<END SERVERTO

<<<SLICE TESTFILE
"""
Domain tests: ui_server/test_server_concurrency.py

The cockpit server must serve two requests at once. F008 streams a long-lived
SSE response from this same process, so a server that handles one request at a
time would block every other cockpit request for the life of one stream.
DECISION F008 D1 makes that a prerequisite of T001 rather than part of it.
"""

from __future__ import annotations

import json
import secrets
import threading
import time
import urllib.request
from pathlib import Path

import pytest

from packages.core.models import Job, Task


def _make_job(**overrides: object) -> Job:
    defaults = dict(
        name="test-concurrency-job",
        user_prompt="Test prompt for concurrency",
        tasks=[Task(type="write_readme", description="Write a README")],
    )
    defaults.update(overrides)
    return Job(**defaults)


class TestServerServesConcurrentRequests:
    """A blocking server cannot host an SSE stream — proven, not assumed."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job

        self.job = _make_job()
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path

    def _start_server(self) -> tuple[int, str]:
        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = secrets.token_urlsafe(16)

        def run():
            try:
                start_ui_server(
                    self.job_id,
                    host="127.0.0.1",
                    port=0,
                    token=token,
                    open_browser=False,
                    info_file=info_file,
                )
            except (SystemExit, KeyboardInterrupt):
                pass

        threading.Thread(target=run, daemon=True).start()

        for _ in range(50):
            if Path(info_file).exists():
                return json.loads(Path(info_file).read_text())["port"], token
            time.sleep(0.1)
        pytest.fail("Server did not start in time")

    def test_two_requests_are_in_flight_at_once(self, monkeypatch):
        # A barrier, not a stopwatch: both requests must be inside the handler
        # simultaneously or the barrier breaks. That is a fact about
        # concurrency rather than a threshold about speed, so it cannot flake
        # on a slow runner.
        from packages.orchestration import ui_server as mod

        port, token = self._start_server()
        barrier = threading.Barrier(2, timeout=8)
        build_dashboard = mod._build_dashboard

        def gated(job):
            barrier.wait()
            return build_dashboard(job)

        monkeypatch.setattr(mod, "_build_dashboard", gated)

        url = f"http://127.0.0.1:{port}/api/state?job_id={self.job_id}&token={token}"
        outcomes: list[object] = []

        def hit():
            try:
                with urllib.request.urlopen(url, timeout=20) as resp:
                    outcomes.append(resp.status)
            except Exception as exc:  # noqa: BLE001 — the failure mode is the evidence
                outcomes.append(type(exc).__name__)

        threads = [threading.Thread(target=hit) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=25)

        assert outcomes == [200, 200], (
            f"both concurrent requests must be served, got {outcomes} — "
            "a single-threaded server breaks the barrier instead"
        )
<<<END TESTFILE
