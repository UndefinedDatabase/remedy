── STEP T003/7 — F008 SSE event stream — ROUND 27 ────────────────────────────
Round base — the SHA every range gate in this block measures from: a86231c0
 (R26's handback, re-read from `git log` at emission. R-0368 exists because a
 block carried the previous round's base forward; the R26 block did exactly
 that, and this header is the half of its counter-measure that was missing.)
Goal:
 Land the React hook. `useBrainStream.ts` is thin over the session R26 landed —
 subscribe, start, close on unmount — and a new `tests/ui_contracts/` source
 contract gates it by reading its source, the style every React component here
 is gated by, since no DOM environment can render it. This round also records
 the R26 PASS and appends the F008 R26 instance to the OPEN finding R-0368.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r27.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R27, applied whole
 C2a  `.agent/live_review.md` <- R0368FROM replaced by R0368TO, a REWRITE
 C2b  `.agent/live_review.md` <- LEDGER27, appended
 C3   `apps/ui/src/api/useBrainStream.ts` <- HOOK and
      `tests/ui_contracts/test_brain_stream_hook.py` <- CONTRACT, both NEW
 C4   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r27.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/api/useBrainStream.ts`,
 `tests/ui_contracts/test_brain_stream_hook.py`, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r27.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r27.md` for C0a. Never retype it.
 If the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are PLANF008R27, R0368FROM, R0368TO, LEDGER27, HOOK
 and CONTRACT, each delimited by a line beginning `<<<SLICE <name>` and one
 beginning `<<<END <name>`; marker lines are NOT part of a slice. Every slice
 is newline-terminated with no trailing whitespace on any line.

Pair shape, measured and not asserted (§3 item 15):
 R0368FROM/R0368TO is the block's ONLY pair. The containment test the reviewer
 ran on the final bytes printed `TO contains FROM: false`, so the pair is a
 REWRITE and the §4.9 obligation is the FROM-0x / TO-1x count of G6, never an
 append reading. R0368FROM occurs EXACTLY ONCE in `.agent/live_review.md` at
 the round base by the reviewer's own count; report your own before applying.
 The other slices are not pairs: two create a file that does not exist, one
 replaces a file whole and one is appended.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23). C2a precedes C2b so each
    ledger proof reads against a single-purpose commit.
 3. Nothing outside the change set is touched. NO EXISTING SOURCE FILE IS
    EDITED and NO DEPENDENCY IS ADDED: both code paths are NEW files, and
    `apps/ui/package.json` and `apps/ui/package-lock.json` are not opened.
    `.agent/live_review.md` is the one existing file this round edits.
 4. NO FINDING ID IS MINTED: R-0630 stays free. R-0368 is AMENDED, not
    resolved, and stays OPEN, as do R-0628, R-0629 and R-0622. Write no
    `Done:` and no `Landed:` line for any of them. R-0628 names this hook, so
    it is resolved by the round that REVIEWS this one — only reviewer-authored
    text sets Resolved (§4.4).
 5. The post-C4 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 6. Two test processes never run at once. G9's four runs happen SERIALLY in
    the PRIMARY checkout (R-0518). G10's mutations are destructive and run
    ONLY in a disposable worktree under `.remedy-wt/` (protocol G5), removed
    and pruned before the handback. That worktree needs `apps/ui/node_modules`:
    SYMLINK it from the primary checkout with `os.symlink`, never a copy —
    `shutil.copytree` defaults to `symlinks=False` and dereferences npm's bin
    shims, which caused seven false failures at F085 R23 (R-0591). The
    reviewer took G10's own readings that way.
 7. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    R26 gate and nothing since has created one.
 8. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there, as R26 did;
    commit nothing from that directory.

The reviewer's OWN readings, each produced by RUNNING the tool and not recalled
(R-0625). At the round base in the primary checkout: typecheck exits 0 silently,
`npx vitest run` exits 0 at 9 files and 137 tests, `tests/ui_contracts/` exits 0
at 397 passed-plus-skipped and the state readers plus canary at 465 — that split
moves run to run, so a bare passed count is never a gate. In a worktree at the
round base with node_modules symlinked and both code slices applied, every value
G9 and G10 order was measured at the value stated, each control seen red,
restored and re-measured byte-identical. `npm run lint` in `apps/ui` is RED at
base, which is R-0622 and NOT a gate (R-0364).

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2a, C2b and C3. Per constraint 5 the post-C4
     readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r27.md`
     as received, of `.agent/authored/f008-r27.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r27.md` with `git show`, by their marker lines, take
     the COUNT from that listing, and report each slice's newline-INCLUDED
     sha256, bytes and lines and that none carries trailing whitespace.
     Expected: PLANF008R27 4e8555ca at 40 lines, R0368FROM
     432fdc8e at 1, R0368TO 8e234582 at 1, LEDGER27 5528f762 at 1,
     HOOK 362a9d56 at 36, CONTRACT 0565e0be at 87.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R27. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The REWRITE at C2a. Read the base bytes with
     `git show <round base>:.agent/live_review.md` into scratch or memory —
     never by writing over the tracked file, which protocol G5 forbids
     (§3 item 29). Report the count of R0368FROM in
     `.agent/live_review.md` at the round base (expected 1) and at C2a
     (expected 0), and of R0368TO at the round base (expected 0) and at C2a
     (expected 1) — the FROM-0x / TO-1x proof the pair's shape owes. Report
     also that the C2a blob differs from the base blob ONLY inside the
     paragraph beginning `- R-0368 — `: the file's `^- R-\d+ — ` paragraph
     COUNT is unchanged and every other paragraph is byte-identical, compared
     as an ordered list of blank-line-separated units.
 G6  The append at C2b, against C2a, two ways that must agree. (a) the C2a blob
     is a byte-exact PREFIX of the C2b blob and the remainder equals a newline
     plus LEDGER27 — report its sha256, bytes and lines; (b) an INDEPENDENT
     blank-line split of the WHOLE C2b file, its terminating newline normalised
     first, has as its LAST unit LEDGER27's paragraph. NEGATIVE CONTROL: flip
     one ASCII byte of the remainder and report that BOTH readings reject it
     and both accept the unflipped.
 G7  The sets, at C2a and C2b, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 201 at BOTH — this round mints no id — `^- R-0630 — `
     0 at both, `^- R-0629 — ` 1 at both, `^- R-0628 — ` 1 at both,
     `^- R-0368 — ` 1 at both, `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0 at
     both, `^Gate: R\d+ — ` 26 then 27 over that many DISTINCT keys. HEADER
     SWEEP at C2b: report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of every non-match to its first period,
     and that the R27 pair occurs EXACTLY ONCE.
 G8  The two code files. For EACH: `git ls-tree` at the round base is EMPTY for
     it, so the round ADDS it and edits nothing; its blob at C3 is BYTE-EQUAL
     to its slice; and its `git show --numstat` cell reads that slice's own
     line count with ZERO deletions.
 G9  The green runs, in the PRIMARY checkout, SERIALLY, AT C3 — the commit at
     which both code files are final. Report each exit code and its counts:
     `npm run --silent typecheck` in `apps/ui` exits 0 with NO output;
     `npx vitest run` in `apps/ui` exits 0 at 9 files and 137 tests — UNCHANGED
     from the base, because the hook carries no vitest test and cannot: that is
     what the contract exists for;
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 406
     passed-plus-skipped, nine more than the base's 397; and
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped. If any fails, report the values and STOP.
 G10 Three red controls, in a disposable worktree at C3 per constraint 6, ONE
     mutation at a time, each restored afterwards and proved byte-identical to
     its pre-mutation sha256. All three mutate
     `apps/ui/src/api/useBrainStream.ts`, where the reviewer counted each
     ordered byte string at exactly 1 occurrence (§3 item 25); report your own
     count before mutating, and report the failing test NAME, because two of
     the three go red in the same file and only the name tells them apart
     (R-0629). Note that the same byte string also occurs in CONTRACT, which
     ASSERTS it — the count that matters is the one in the file named here.
     (a) DELETE the one line `    return () => { session.close(); };`:
         `python3 -m pytest tests/ui_contracts/test_brain_stream_hook.py -q -rf`
         EXITS 1 at 1 failed and 8 passed, the failure being
         `TestBrainStreamHookContract::test_hook_closes_the_session_on_unmount`.
     (b) REPLACE `useSyncExternalStore(session.subscribe, session.view, session.view)`
         with `session.view()`: that same command EXITS 1 at 1 failed and 8
         passed, the failure being
         `TestBrainStreamHookContract::test_hook_reads_the_runner_as_an_external_store`.
     (c) REPLACE `latestMakeDeps.current(jobId)` with `latestMakeDeps.current()`:
         `npm run --silent typecheck` EXITS 2 — tsc's real code for a compile
         error, not 1 — naming `error TS2554` in `useBrainStream.ts`. Report the
         exit code you actually observe.
 G11 The range, measured from the round base named in this block's header and
     from no other SHA. Report `git diff --name-only <round base>..C3` and that
     it equals the Change set MINUS `.agent/handoff.md` exactly — six paths,
     none on either side alone; the full reading to C4 belongs to the ROUND
     REPORT (constraint 5). Report that every commit in the range has exactly
     ONE parent, and BOTH numstat cells per path from `git show --numstat`,
     cross-checked against `git diff --numstat`, every insertion under 500 and
     every cell equal to the `+/-` column of your `## Commits` table, cell by
     cell (§3 item 28).
 G12 Marker leak and reflog. Count LINES BEGINNING with `<<<SLICE ` or `<<<END `
     in each file this round writes outside `.agent/authored/` — the plan at
     C1, the ledger at C2a and C2b, the two code files at C3 and the handback
     at C4 — each is 0. Then count THIS round's own reflog entries by the
     OPERATION before the first `:` in `%gs`: all six pre-C4 entries are
     `commit`; report `amend`, `rebase` and `cherry` at 0, and assert no total.
 G13 The handback carries every mandated section of
     docs/agents/handback_template.md and an item-status table holding exactly
     one row for each of C0a, C0b, C1, C2a, C2b, C3 and C4 — "exactly one row"
     scoping to that TABLE. Its `## Next` states that the next session's FIRST
     action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the
     Open PR Gate (Phase 1 rule 2); that R27 is PENDING REVIEW; that the next
     free id is R-0630; that R-0628, R-0629, R-0622 and R-0368 are OPEN; and
     that R28 puts the delayed badge on a visible surface and wires the hook's
     deps to the endpoint T001 and T002 built. Measure its line count with
     `wc -l` BEFORE committing it; seven commits make the cap 100, and an
     overage carries a DECISION D15 stated-cause line naming the real count and
     the mandated content that caused it. One line per gate here; raw
     transcripts go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~97 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store+Host+Seam+Hook ✅, Badge offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R27
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the transcript byte-equals the ledger's
envelope sequence, the heartbeat holds cadence, and the fallback engages on a
disabled EventSource and recovers to live.

## Current Step
R27 lands `useBrainStream.ts`, the last piece of T003's client and the only
part of it React owns: it subscribes to the session R26 landed through
`useSyncExternalStore`, starts it in an effect and closes it in that effect's
cleanup, so a remounting cockpit cannot leak one EventSource per mount. It
keys the session on the job id alone and reads its dependency factory through
a ref, because a caller writing deps inline would otherwise tear the stream
down on every parent render. A new `tests/ui_contracts/` source contract gates
it, on comment-stripped source so a WHY comment cannot satisfy a guard.

## Next Steps
1. R28 puts the delayed badge on a visible surface and wires the hook's deps
   to the endpoint T001 and T002 built — the first round in which the server
   half and the client half of this feature meet.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge is a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  the contract gates its source, and the session beneath it carries the logic.
<<<END PLANF008R27

<<<SLICE R0368FROM
so the range and the round agree by construction rather than by the reviewer's memory. OPEN.
<<<END R0368FROM

<<<SLICE R0368TO
so the range and the round agree by construction rather than by the reviewer's memory. F008 R26 INSTANCE, in the shape this counter-measure's own words name: the R26 block's G10 ordered `git diff --name-only 6e39f19d..C3` and required it to equal the Change set minus `.agent/handoff.md`, but `6e39f19d` is R24's handback and R26's base is `369fd39e`, R25's — the reviewer carried the PREVIOUS block's base into the new one, which is exactly what "never carried over from the previous block" forbids, and the R26 block prints no round-base header at all, which is the other half of the counter-measure and the half that would have caught it. The ordered range therefore also spanned R25's five commits, so the real reading at `931ed066` was EIGHT paths and no correct application of the R26 bundle could have made it six. The worker ran the command exactly as ordered, reported the eight-path output, ALSO reported the `369fd39e..931ed066` reading — the six paths, none on either side alone — and edited nothing toward the ordered number; the reviewer re-measured both at `a86231c0` and confirms them, and R26 PASSED on every other gate. NO SECOND ID IS MINTED: §3 item 30 routes a defect the open set already describes to the finding that describes it, and searching the ledger for the defect rather than for an id is what found this entry. WHY IT RECURRED IS ALREADY ON RECORD AND THAT IS THE POINT: R-0376 registered the same class and closed with the mechanical fix — the last pre-emission act on a block is to grep its own bytes for every SHA-shaped token, each of which must be either the declared round base or a base whose deviation the gate states inline. That rule has lived in a finding BODY since F057 and bound nothing, which is the R-0452 and R-0454 class; the R26 block would have failed that grep on its first hit had anyone run it. THE FIX IS THEREFORE A PROMOTION, not another sentence here: the grep belongs in the §3 pre-emission checklist of `docs/agents/planner_reviewer_prompt.md`, and it routes to a paydown branch with the other checklist promotions `.agent/context.md` already names, because no round of this feature may reach that path. OPEN.
<<<END R0368TO

<<<SLICE LEDGER27
Gate: R27 — the R26 entry. R26 PASSED. It landed `brainStreamSession.ts`, the composition seam, and recorded the R25 verdict, and EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.remedy-wt/f008-r26.md`, `.agent/authored/f008-r26.md` at `b00a42f0` and `.agent/last_block.md` at `abef185b` are all sha256 a3c93663a29902caa1d59081b5806a87020d864b29a472a9728ee38e4cc8244d over 22565 bytes and 376 lines, equal to the digest the reviewer emitted. FOUR SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R26 4ce0503e at 2210 bytes and 41 lines, LEDGER26 8a9d2ef6 at 2923 bytes and 1 line, SESSION 1935909b at 1683 bytes and 38 lines, SESSIONTESTS 5a2d6cef at 3842 bytes and 111 lines — none carrying trailing whitespace on any line. THE PLAN LANDED FIRST at `433e59eb`, byte-equal at 41 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and the F-id `F008`. THE APPEND at `f683ab43` is a byte-exact prefix of the `433e59eb` blob plus a 2924-byte remainder equal to a newline plus LEDGER26, agreed by an INDEPENDENT blank-line split of the whole file into 237 units whose LAST unit is LEDGER26's paragraph, with a one-ASCII-byte flip REJECTED by BOTH readings and the unflipped ACCEPTED by BOTH. THE SETS HELD — findings 201 at both revisions with NO id minted, `- R-0630` 0 at both, `- R-0629` and `- R-0628` 1 at both and both still OPEN, `Done:` 6 at both, `Landed:` 0 at both, `Gate: R` 25 to 26 over that many DISTINCT keys, twenty-five of twenty-six headers matching the `Gate: R<n> — the R<n-1> entry.` shape with the F255 entry the single non-match, and the R26 pair occurring exactly once. THE TWO CODE FILES ARE PROVED BY CONSTRUCTION: `git ls-tree 369fd39e` is EMPTY for both, each blob at `931ed066` is BYTE-EQUAL to its slice, and their numstat cells are 38 and 111 insertions with ZERO deletions, so the round ADDED the seam and edited nothing around it. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npm run --silent typecheck` exits 0 with no output, `npx vitest run` exits 0 at 9 files and 137 tests, `tests/ui_contracts/` exits 0 at 393 passed plus 4 skipped, and the state readers including the canary exit 0 at 465 passed-plus-skipped. BOTH RED CONTROLS DISCRIMINATE, measured by the reviewer in a disposable worktree before the block was written and by the worker at `931ed066`, agreeing: deleting `      host.close();` fails ONLY `closes the socket when the caller closes the session` and deleting `      runner.stop();` fails ONLY `performs nothing more once it is closed`, each at exit 1 with 136 passing, each restored byte-identical — and the first of those two controls is the reason the seam's test suite is trustworthy at all, because the reviewer's FIRST draft of that test passed the mutation and was rewritten before it was ordered. SIX single-parent commits, insertions 376, 299, 15, 2 and 149, every one under 500 and every cell equal to the `## Commits` column; zero marker lines in all five targets; five reflog operations all `commit`; a 69-line handback within the 100 six commits allow; the tree clean and the primary checkout the only worktree. THE ROUND'S ONE SUBSTANTIVE DEVIATION IS A DEFECT OF THIS REVIEWER'S BLOCK AND NOT OF ITS WORK — G10's base SHA — and it is recorded above against R-0368, the OPEN finding that already describes it, rather than under a new id.
<<<END LEDGER27

<<<SLICE HOOK
// The React half of the brain stream, and deliberately the ONLY part of it that
// is React at all: every rule this client has lives in brainStream.ts,
// brainStreamDriver.ts, brainStreamRunner.ts and brainStreamSession.ts, where
// the node-environment vitest can reach it. What is left here — subscribe to a
// store, start it, close it on unmount — is gated by a tests/ui_contracts/
// source contract, the style this repository uses for every React component.
import { useEffect, useMemo, useRef, useSyncExternalStore } from "react";
import { createBrainStreamSession } from "./brainStreamSession";
import type { BrainStreamHostDeps } from "./brainStreamHost";
import type { BrainStreamView } from "./brainStreamRunner";

/** Subscribe the cockpit to one job's event stream.
 *
 *  The session is keyed on `jobId` ALONE. `makeDeps` is read through a ref
 *  instead of a dependency, because a caller that writes its deps inline hands
 *  a new function every render, and a memo that honoured that identity would
 *  tear down the stream and open a fresh EventSource on every parent render. */
export function useBrainStream(
  jobId: string,
  makeDeps: (jobId: string) => BrainStreamHostDeps,
): BrainStreamView {
  const latestMakeDeps = useRef(makeDeps);
  useEffect(() => { latestMakeDeps.current = makeDeps; }, [makeDeps]);

  const session = useMemo(() => createBrainStreamSession(latestMakeDeps.current(jobId)), [jobId]);

  // Closing on unmount is the whole reason the session exposes `close`: React
  // remounts components freely, and a cleanup that only forgot the session
  // would leave its EventSource open for the lifetime of the page.
  useEffect(() => {
    session.start();
    return () => { session.close(); };
  }, [session]);

  return useSyncExternalStore(session.subscribe, session.view, session.view);
}
<<<END HOOK

<<<SLICE CONTRACT
"""Contract tests for the useBrainStream hook and the session it is thin over.

The hook is the one piece of the SSE client React owns, and this repository has
no DOM environment, so it is gated the way every other component here is gated:
by reading its source. Every assertion runs against COMMENT-STRIPPED source —
these files carry a WHY comment above each definition, and a guard that counted
a token inside a comment would be satisfied by the prose describing the code
rather than by the code (finding R-0584).
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
API_DIR = REPO_ROOT / "apps" / "ui" / "src" / "api"
HOOK = API_DIR / "useBrainStream.ts"
SESSION = API_DIR / "brainStreamSession.ts"


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments. These files contain no string literal holding
    either marker, which is what lets so plain a scanner be trustworthy here."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


class TestCommentStripping:
    def test_stripper_removes_a_comment_the_file_really_carries(self):
        raw = HOOK.read_text()
        assert "// The React half" in raw, "the hook must keep its WHY comment"
        assert "The React half" not in strip_ts_comments(raw), "stripper must remove it"


class TestBrainStreamHookContract:
    def test_hook_file_exists(self):
        assert HOOK.is_file(), "useBrainStream.ts not found"

    def test_hook_is_exported_under_its_own_name(self):
        code = strip_ts_comments(HOOK.read_text())
        assert "export function useBrainStream(" in code, "the hook must be exported"

    def test_hook_reads_the_runner_as_an_external_store(self):
        code = strip_ts_comments(HOOK.read_text())
        assert "useSyncExternalStore(" in code, (
            "the hook must subscribe to the runner store rather than hold state"
        )

    def test_hook_closes_the_session_on_unmount(self):
        code = strip_ts_comments(HOOK.read_text())
        assert "session.close()" in code, (
            "the hook must close the session, or a remount leaks one EventSource"
        )
        assert "return () => { session.close(); };" in code, (
            "the close must be an effect CLEANUP, which is what unmount runs"
        )

    def test_hook_does_not_compose_the_transport_itself(self):
        code = strip_ts_comments(HOOK.read_text())
        assert "createBrainStreamHost" not in code, (
            "composition belongs to brainStreamSession.ts, where vitest can test it"
        )


class TestBrainStreamSessionContract:
    def test_session_file_exists(self):
        assert SESSION.is_file(), "brainStreamSession.ts not found"

    def test_session_is_exported_under_its_own_name(self):
        code = strip_ts_comments(SESSION.read_text())
        assert "export function createBrainStreamSession(" in code

    def test_session_close_stops_the_runner_and_the_socket(self):
        code = strip_ts_comments(SESSION.read_text())
        assert "runner.stop();" in code, "close must stop the runner"
        assert "host.close();" in code, "close must also close the socket"
<<<END CONTRACT
