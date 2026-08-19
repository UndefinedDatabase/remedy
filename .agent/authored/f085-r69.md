── STEP T003 acceptance — the denied fetch — F085 — R69 ──────────────────────

Goal: measure T2_F085's last open acceptance line — a network access from a guarded `test`-class
command fails under the default-deny posture — against a loopback server that is REALLY listening,
with the control that measurement needs, and record the R68 PASS. This is the last build item before
the integration gate; T003's document, its README link and the posture itself already landed.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md` ·
C2 record the R68 PASS and resolve R-0563 · C3 the acceptance tests · C4 handback.

CONVENTION, binding on every count here, carried verbatim in force from the R68 block. A line count is
the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and NO
joiner and NO terminator byte is ever added. THIS BLOCK'S FROM/TO PAIRS ARE PLAN23 AND IMPORTS. ITS
END-OF-FILE APPENDS, WHICH HAVE NO FROM AT ALL, ARE NETTEST AND RECORD37 — listed rather than counted,
per §3 checklist item 11. Each append slice CARRIES ITS OWN LEADING BLANK LINES, so the separation its
target's convention requires is a property of bytes that were measured and never of a join shape that
was reasoned about.

## Change

C1 applies PLAN23F→PLAN23T to `.agent/plan.md`, rewriting the `## Current Step` section and the WHOLE
`## Next Steps` list — the whole list, per §3 checklist item 17, so no surviving item can keep a stale
label. C2 appends RECORD37 to the END of `.agent/live_review.md`. C3 makes BOTH of its edits to
`tests/orchestration/test_exec_guard.py` IN ONE COMMIT and IN THIS ORDER: first apply IMPORTSF→IMPORTST
to the module's stdlib import block, THEN append NETTEST to the END of the file. That order is
load-bearing — NETTEST uses `contextlib`, `http.server` and `threading`, which IMPORTST is what brings
in — and G3 gates the two together by reconstructing the post-commit blob from the pre-commit blob.

Change set, named rather than counted: `.agent/authored/f085-r69.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `tests/orchestration/test_exec_guard.py`,
`.agent/handoff.md`. Nothing else. NO `docs/**` path is in that set, so no docs suite is ordered and
Rule A4 is untouched. ONE `.py` path is in it, so a lint gate IS ordered, over that path. Every
tracked path named in a gate below was resolved on disk at 1df91b27 with `git ls-tree`, one call per
path, before emission, per checklist item 24, and all of them exist; `.agent/authored/f085-r69.md` is
the one path no gate reads at the base, because C0a creates it.

WHAT IS BEING MEASURED, and why the control is inside the test rather than beside it. Stage 1's deny
is a PROXY posture and never a kernel one: `exec_guard` points a denied child's proxy variables at
`DENIED_NETWORK_PROXY_URL`, the closed port `http://127.0.0.1:9`, and empties `NO_PROXY` so no host is
exempt. A fetch that fails against a port where nothing listens therefore proves nothing whatever,
which is the one way this measurement can lie. NETTEST's first test runs the SAME argv against the
SAME url twice — once as a plain child that must be SERVED, once through `run_guarded_test_command`
that must FAIL — so the posture is the only difference between them and a harness that never came up
turns the test red instead of green. The reviewer ran this at 1df91b27 before ordering it, per
R-0364: with the deny in place both new tests pass and the whole file reads `44 passed`; with
`deny_network` flipped to `False` in the `test` policy both new tests FAIL, and the guarded child
comes back `returncode=0` carrying the served body — the exact opposite reading, which is what makes
the green attributable. G8 orders that same red control back from the worker's own hand.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r69.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C4; if it exists, finish the commit in
   flight, write the handback and stop. `git status --porcelain` is empty at round start and after
   every commit.
3. PAIR SHAPES. The reviewer ran the containment test at emission against each target's blob at
   1df91b27 and prints its own output here per checklist item 15, one reading per pair:
   PLAN23F→PLAN23T `TO contains FROM: false`; IMPORTSF→IMPORTST `TO contains FROM: false`. Both are
   therefore REWRITES and each owes the FROM 0x / TO 1x reading over its own post-commit file. Each
   FROM occurs EXACTLY 1x in its target at 1df91b27 — the reviewer measured both.
4. NETTEST AND RECORD37 HAVE NO FROM. Do not invent one for either and do not report a FROM count for
   either. RECORD37 is appended at the END of `.agent/live_review.md` and owes the ORDERED EQUALITY of
   §4.9 as R-0531 narrows it: pre-commit blob a byte-exact PREFIX, slice an exact SUFFIX, and that
   commit's ADDED lines exactly the slice's lines IN ORDER. NETTEST owes a DIFFERENT obligation and
   not that one, because it is CODE and because its own commit edits the same file twice: code repeats
   lines structurally, so a per-line ADDED count is not the property (R-0531). Its obligation is
   BYTE-EXACT RECONSTRUCTION, which G3 states.
5. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of the tests. Only C0a and C0b
   may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
6. NOTHING IN `.agent/live_review.md` THAT ALREADY EXISTS AT 1df91b27 IS EDITED, MOVED OR DELETED, and
   nothing already in `tests/orchestration/test_exec_guard.py` at 1df91b27 is edited, moved or deleted
   EXCEPT the IMPORTSF bytes the pair replaces. No existing test is renamed, retitled or removed.
7. Every sentence in RECORD37 that states a reading of a file names the SHA it was read at in the same
   clause, per checklist item 20 as R-0521 and R-0534 narrow it — the qualifier attaches to EVERY
   reading in the clause, not only the first. RECORD37 states readings of R68's range and of this
   round's base only, all of which are prior state, so every SHA it names already exists when it is
   written.
8. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD37 is reviewer text and carries the R68 gate
   entry and the one resolution inside it. Do not add a `Landed:` line, do not add a `Done:` paragraph
   of your own, and do not edit RECORD37 to reconcile it with anything you measure. A disagreement
   between RECORD37 and your own reading is a finding to REPORT in the handback, never to fix — the
   rule that caught R66 and R67, in the third round it has been relied on.
9. THIS ROUND REGISTERS NOTHING AND RESOLVES ONE. Registered stays 178, done moves 30 → 31, landed
   stays 0, open moves 148 → 147, and the next free id stays R-0564. RECORD37 therefore carries
   exactly one `Done:` line and no `- R-` registration line; G6 proves it.
10. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as its correction section fixes the ruled figure:
   490 lines TOTAL, PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all
   three on the final bytes at emission. The worker re-measures all three from the committed
   `.agent/authored/f085-r69.md`; a mismatch is a finding against this block, not the worker.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and its
   output, and push what is committed. Never edit a slice to make a gate green, and never widen the
   change set to route around a red. In particular, if NETTEST does not pass, do NOT adjust NETTEST.
12. RUN THE SUITES SERIALLY, one pytest process at a time, never alongside another in any checkout or
   worktree. These suites spawn real supervisors and real children that bind ports, so two concurrent
   runs redden each other on tests neither touched. NETTEST binds an EPHEMERAL loopback port it asks
   the kernel for, so it collides with nothing, but it is still a real server and still serial.
13. THE RED CONTROL RUNS ONLY INSIDE A DISPOSABLE `git worktree` AND NEVER IN THE PRIMARY CHECKOUT
   (G5 of docs/agents/self_drive_protocol.md). Create it, mutate there, read the colour, remove it,
   and confirm `git worktree list` is one line again at the end. The primary checkout must satisfy
   `git status --porcelain` empty at every commit, which a mutation in it would break.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit. G8 creates and removes ONE disposable worktree; `git worktree
list` is one line at round start and one line at the end, and no worktree exists at any commit.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r69.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report sha256, byte count, line count
and marker-line count for each. Also report the block's TOTAL, PROSE and RECORD37 line counts read
from that committed file, against constraint 10's 490 / 400 / 140, where PROSE is TOTAL minus the
slice lines.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - PLAN23F→PLAN23T is a REWRITE over `.agent/plan.md` at C1: report FROM 0x and TO exactly 1x over the
   post-commit blob, and re-applying the extracted FROM→TO to the pre-commit blob must reproduce the
   post-commit blob BYTE-EXACTLY.
 - RECORD37 at C2 over `.agent/live_review.md`: report the ordered-equality readings constraint 4
   names — PREFIX, SUFFIX, `pre + slice` equal byte for byte, and that commit's ADDED lines exactly the
   slice's lines IN ORDER.
 - C3 over `tests/orchestration/test_exec_guard.py` owes ONE reconstruction covering both its edits:
   take the PRE-commit blob, apply `IMPORTSF`→`IMPORTST` with `bytes.replace`, then concatenate
   `NETTEST`, and report that the result equals the POST-commit blob BYTE-EXACTLY. Report as well
   IMPORTSF 1x pre-commit and 0x post-commit with IMPORTST exactly 1x post-commit, and that NETTEST is
   an exact SUFFIX of the post-commit blob. Do NOT report an ADDED-line count for NETTEST.
 - Plus `git show --numstat` for each path and commit, plus the count of lines matching
   `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0. Count marker LINES, never the
   substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each EXIT 0, and serially per
constraint 12. Report each run's passed count; the counts are reported, never predicted, and only the
exit code is ordered. The reviewer took every base reading below itself, in the primary checkout, at
1df91b27.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf` — base `42 passed`; this is the
   file C3 edits, and the base reading is the count BEFORE NETTEST's tests exist.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf -k "really_listening or
   closed_proxy_port"` — the two tests NETTEST adds, selected by name. Exit 0, and report how many
   were selected and how many passed.
 - `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
   tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
   base `160 passed`; these read `.agent/plan.md` and `.agent/live_review.md`, which C1 and C2 write.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 PLAN CONTRACT, on `.agent/plan.md` after C1: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 39 lines by applying the pair to that blob at 1df91b27 — one shorter than the
round before, because PLAN23T's `## Next Steps` list carries one item fewer than PLAN23F's.

G6 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
1df91b27 and at HEAD, from the line-start patterns for a registration, a resolution and a landed line.
The reviewer's base reading is 178 / 30 / 0, 148 open, max registered R-0563, max resolved R-0562. At
HEAD the reading must be 178 / 31 / 0, 147 open, max registered still R-0563 and max resolved R-0563,
because constraint 9 rules this round registers nothing and resolves one. The registered and landed
symmetric differences must both be EMPTY and the done symmetric difference EXACTLY `{R-0563}`. Next
free id R-0564. Report all three symmetric differences, the duplicate-id count and the count of
resolutions naming an unregistered id, at both SHAs.

G7 LINT, over the one `.py` path this round edits, run from the repository root with the repository's
OWN configuration — no `--isolated`, per §3 checklist item 12. BOTH halves are green at the base, so
both are ordered GREEN rather than compared as multisets; the reviewer executed both at 1df91b27
itself, per R-0364, and both printed `All checks passed!`.
 - `python3 -m ruff check tests/orchestration/test_exec_guard.py` — exit 0.
 - `python3 -m ruff check --preview tests/orchestration/test_exec_guard.py` — exit 0. The preview half
   is ordered separately because ruff is preview-blind to the E301-E306 class (R-0500, R-0558).

G8 THE RED CONTROL, the gate this round exists for, run ONLY in a disposable worktree per constraint
13 and only AFTER C3 is committed. A test that cannot fail proves nothing when it passes, and both
NETTEST tests assert an ABSENCE of network reach, which is the shape most likely to pass for the wrong
reason.
 - Create the worktree from HEAD: `git worktree add --detach .remedy-wt/redctl-r69 HEAD`.
 - In THAT worktree only, in `packages/orchestration/exec_guard.py`, replace the single occurrence of
   this byte string — count it in that file first and report the count, which must be 1 —
   `            TEST_COMMAND_ENV_ALLOWLIST + tuple(extra_env_keys) + tuple(sorted(overlay))` followed
   by the next two lines `        ),` and `        deny_network=True,` — changing ONLY `deny_network=True`
   to `deny_network=False` in that occurrence. The longer string is ordered because
   `deny_network=True,` alone occurs more than once in that file and the other occurrence belongs to
   the `dod-process` policy, which this control must not touch (§3 checklist item 25).
 - Run `python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf -k "really_listening or
   closed_proxy_port"` IN THAT WORKTREE. It must go RED: report the exit code, the failed count, and
   the failing test names. The reviewer's own reading at 1df91b27 was both tests FAILED with the
   guarded child returning `returncode=0` and the served body in its stdout.
 - Remove the worktree with `git worktree remove --force .remedy-wt/redctl-r69` and report that
   `git worktree list` is one line again and `git status --porcelain` in the primary checkout is empty.
 - Do NOT commit the mutation anywhere. If the control comes out GREEN, that is a STOP under
   constraint 11: report it and do not touch NETTEST.

G9 HYGIENE. `git diff --name-only 1df91b27..HEAD` measured BEFORE C4 holds exactly the change set
above minus `.agent/handoff.md`, which C4 writes, and nothing else — and in particular holds no path
under `packages/`, `apps/`, `docs/` or `scripts/`, and exactly one path under `tests/`. Report the
list. Report per-commit insertions for every commit BEFORE C4 — C4 cannot measure itself, so its own
go in the round report — and confirm none exceeds 500. This branch spent the AGENTS.md declared-oversize
allowance at d4473f85, so a second oversize commit is a STOP under constraint 11, never a declaration.
Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base SHA
1df91b27, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3 and
C4, the real G1-G9 results with exit codes, the open-findings count and the next expected action. The
Bundle above holds more than five commits, so the ≤100-line cap AGENTS.md allows when a per-commit
table needs it applies; drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~100 % der Bauarbeit (T001 gebaut · T002 KOMPLETT · T003 KOMPLETT: Netz-Posture
verdrahtet und gepinnt, Limitations-Dokument steht, verlinkt und inhaltlich korrekt, und die letzte
Akzeptanzzeile ist jetzt am echt lauschenden Server gemessen, mit Kontrolle · R66 und R67 FAIL, beide
Fehler des Reviewers, beide repariert) — offen bleiben nur noch Integration Gate und Closure.
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: R70 is the
INTEGRATION GATE — the full suite per docs/agents/integration_gate.md, the first of the two
full-suite runs this feature owes; closure per docs/roadmap/STATUS_closure_protocol.md follows it.
TWO: R69 carries no verdict of its own, because the round that records a verdict cannot record one on
itself (docs/agents/planner_reviewer_prompt.md §4 item 13); R70 carries it. THREE: a standalone
closing line stating the open findings count and the next free id. FOUR:
`Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires every
handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN23F
## Current Step
R68, this round: the ledger. R67's two repairs are correct and re-read, so R-0561 and R-0562 are
marked done — but R67 FAILED on its own record: RECORD35 closes R-0562 by naming further
repository hits for `spawn unsupervised` that do not exist. That claim is registered as R-0563
and retracted by an APPENDED correction, never by rewriting landed text. No source file, no test
and no document is touched.

## Next Steps
1. The remaining acceptance measurement: a guarded test command is refused against a loopback
   server that is really listening, where the same child without the posture is served.
2. The integration gate: the full suite per docs/agents/integration_gate.md, the first of the two
   full-suite runs this feature owes.
3. Then closure per docs/roadmap/STATUS_closure_protocol.md.
END-PLAN23F

BEGIN-PLAN23T
## Current Step
R69, this round: T003's last acceptance line. A guarded `test`-class command is refused against a
loopback server that IS listening, while the same argv without the posture is served and the
server keeps serving afterwards — the control lives in the test body, so a harness that never
came up turns the measurement red rather than green. R68 PASSED and R-0563 is marked done. This
completes the build work; only the integration gate and closure remain.

## Next Steps
1. The integration gate: the full suite per docs/agents/integration_gate.md, the first of the two
   full-suite runs this feature owes.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH review zip, the
   STATUS line authored by the reviewer, and the PR the operator merges at the next Open PR Gate.
END-PLAN23T

BEGIN-IMPORTSF
import io
import os
import subprocess
import sys
import time
END-IMPORTSF

BEGIN-IMPORTST
import contextlib
import http.server
import io
import os
import subprocess
import sys
import threading
import time
END-IMPORTST

BEGIN-RECORD37

Gate: R69 — the R68 entry. R68 PASSED. All eight ordered gates were re-executed by the reviewer over
a8ba453d..1df91b27, not read, and every measured value equals the one the handback reports. LINE
COUNTS ARE `splitlines` COUNTS. TRANSPORT HELD, disk-to-disk with no digest fallback and with the
reviewer's OWN pre-emission original in the comparison: the committed `.agent/authored/f085-r68.md`,
the committed `.agent/last_block.md` at 1df91b27, both working copies at 1df91b27 and the reviewer's
original are all five byte-EQUAL at sha256
f064a5dee523d030e4477585eea3e54fa31731e6741ad5ca1499fbae7c7cfcac, 27537 B, 344 lines, 6 marker lines;
TOTAL 344 against the 490 cap, PROSE 230 against 400, RECORD36 88 against 140. THE SHAPES HELD:
PLAN22F→PLAN22T over `.agent/plan.md` at e9d4eca6 reads `TO contains FROM: false`, FROM 1x pre-commit
and 0x post-commit with TO exactly 1x post-commit, and re-applied reproduces the post-commit blob
BYTE-EXACTLY. RECORD36 over `.agent/live_review.md` at ea2a458f satisfies ORDERED EQUALITY on every
clause — PREFIX, SUFFIX, `pre + slice` equal byte for byte, ADDED lines equal to the slice's lines IN
ORDER, 88 and 88 — with a numstat deletion column of 0. Marker LINES at 1df91b27 are 0 in both edited
files. THE SUITES WERE RE-RUN, NOT READ, in the primary checkout, serially, each exit 0: `160 passed`
for the four state readers and the canary `42 passed`, each equal to its base. THE PLAN CONTRACT HELD
at 1df91b27: 40 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id all
present. THE ARITHMETIC MOVED AS THAT BLOCK'S CONSTRAINT 9 REQUIRED: 177 registered / 28 done / 0
landed and 149 open at a8ba453d against 178 / 30 / 0 and 148 open at 1df91b27, the registered
symmetric difference exactly {R-0563}, the done symmetric difference exactly {R-0561, R-0562}, the
landed difference EMPTY, and 0 duplicate ids and 0 orphan resolutions at both SHAs. THE TRUTH GATE
HELD on all four of its readings, which is what resolves R-0563 below. The history over that range is
five single-parent commits with no amend, rebase, reset or force-push in the reflog, and the branch is
in sync with its remote.

Done: R-0563 — Resolved at R68, commit ea2a458f, and the resolution is a RETRACTION rather than an
edit. The false clause registered as R-0563 still stands byte-for-byte where it was committed at
60057260, and RECORD36 appends the correction beneath it, which is what
docs/agents/planner_reviewer_prompt.md §3 checklist item 20 rules and what DECISION F085 D6's own
correction section does in `.agent/decisions.md`. The reviewer proved BOTH halves mechanically at
1df91b27: the whole of `.agent/live_review.md` as it stood at a8ba453d is a byte-exact PREFIX of the
file at 1df91b27, so nothing landed was overwritten, and the string `and an example sentence in`
occurs exactly 1 time at each of those two SHAs rather than dropping to 0. The counter-measure the
finding names was applied in the same round that registered it: R68's G7 read every clause of the
sweep back from the sweep's own output rather than its total alone — the two hits AND the path each
one lands in at a8ba453d and at 1df91b27, no match for `unsupervised` in
`docs/agents/planner_reviewer_prompt.md` at either SHA with the exit code reported alongside the empty
output, and the bare word matching 4 lines of `packages/runtimes/dev_server.py` at a8ba453d while the
phrase matches none there. That last reading is the word-for-phrase confusion R-0563 exists to name,
measured in the file that produced it.
END-RECORD37

BEGIN-NETTEST


#: A child that fetches one URL and handles nothing, so an unreachable server makes
#: the COMMAND fail instead of merely printing about it — which is the shape
#: `docs/roadmap/features/T2_F085.md` states its acceptance in. `urllib` honours
#: `http_proxy`/`HTTP_PROXY`, which is the posture stage 1 actually sets; the URL is
#: `argv[2]` because `_child` puts MARKER at `argv[1]`.
_FETCH_URL = (
    "import sys, urllib.request\n"
    "sys.stdout.write(urllib.request.urlopen(sys.argv[2], timeout=5).read().decode())\n"
)

#: Served to any GET, so a successful fetch is proved by CONTENT and not by an exit
#: code that a dozen other outcomes would also produce.
_SERVED_BODY = b"REMEDY_EXEC_GUARD_SERVED_BODY"


class _ServesOneBody(http.server.BaseHTTPRequestHandler):
    """Answer every GET with `_SERVED_BODY`, and keep pytest's output clean."""

    def do_GET(self):  # noqa: N802 — BaseHTTPRequestHandler names the hook
        self.send_response(200)
        self.send_header("Content-Length", str(len(_SERVED_BODY)))
        self.end_headers()
        self.wfile.write(_SERVED_BODY)

    def log_message(self, *_args):
        """Silence the default stderr access log."""


@contextlib.contextmanager
def _really_listening():
    """A loopback HTTP server on an ephemeral port, answering for real.

    Stage 1's deny is a PROXY posture and never a kernel one, so a fetch that fails
    against a port where nothing listens proves nothing whatever. This harness
    exists so the denied fetch is measured against a server that IS answering, and
    the port is ephemeral so two concurrent runs cannot collide on it.
    """
    server = http.server.HTTPServer(("127.0.0.1", 0), _ServesOneBody)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}/"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.mark.subprocess
def test_a_guarded_test_command_cannot_reach_a_server_that_is_really_listening():
    """T2_F085's remaining acceptance line, with its control in the same body.

    The control runs FIRST and unguarded and must be SERVED. That is what makes the
    guarded failure attributable to the deny posture rather than to a harness that
    never came up: both children run the SAME argv against the SAME url, so the
    posture is the only difference between them. A test that asserted only the
    failure would stay green if this server stopped listening altogether, which is
    the one way this measurement can lie.
    """
    with _really_listening() as url:
        served = subprocess.run(
            _child(_FETCH_URL) + [url], capture_output=True, timeout=30,
        )
        assert served.returncode == 0, served.stderr
        assert _SERVED_BODY in served.stdout

        denied = run_guarded_test_command(
            _child(_FETCH_URL) + [url], timeout_sec=30, cwd=None,
        )

        assert denied.returncode != 0
        assert _SERVED_BODY not in denied.stdout
        assert b"URLError" in denied.stderr

        # The deny stopped the CHILD and not the server: T003's "the harness still
        # serves" half, measured after the refusal rather than assumed from it.
        again = subprocess.run(
            _child(_FETCH_URL) + [url], capture_output=True, timeout=30,
        )
        assert again.returncode == 0
        assert _SERVED_BODY in again.stdout


@pytest.mark.subprocess
def test_the_refusal_a_denied_child_sees_names_the_closed_proxy_port():
    """WHY the fetch failed, so a future unrelated breakage cannot pass for the deny.

    `denied.returncode != 0` above is satisfied by any crash at all. This pins the
    refusal to the posture: the child reports a connection refusal, and the proxy it
    was pointed at is the closed port `DENIED_NETWORK_PROXY_URL` names.
    """
    with _really_listening() as url:
        denied = run_guarded_test_command(
            _child(_FETCH_URL) + [url], timeout_sec=30, cwd=None,
        )

    assert b"Connection refused" in denied.stderr
    assert exec_guard.DENIED_NETWORK_PROXY_URL == "http://127.0.0.1:9"
    assert exec_guard.test_command_exec_policy(30, None).deny_network is True
END-NETTEST
