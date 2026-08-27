STEP CLOSURE 2 OF 3 / F031 — DECISION INBOX
Goal:        Record the CLOSURE 1 verdict, then produce the two artifacts closure
             cannot be authored without: a fresh feature-scoped evidence bundle
             and a FRESH review zip built from a clean tree at the reviewed head.
             A failing zip build is a closure BLOCKER, never a thing to work
             around. NOTHING about `docs/roadmap/STATUS.md` or `README.md`
             happens this round — CLOSURE 3 writes those from the evidence job
             id, the package filename and the package SHA-256 that only THIS
             round can produce. No production code, no tests, no docs.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the CLOSURE 1 verdict · then the EVIDENCE JOB · then the
             REVIEW ZIP · then C3 the handback · then push. The bundle and the
             zip are ARTIFACTS, not commits: both paths are gitignored and
             neither is ever committed, per the closure protocol's "Evidence dir
             is not committed".
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r68.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G14 orders a push, the
             evidence job writes under `.remedy-wt/`, and the zip writes a
             gitignored archive. NOTHING under `apps/`, `packages/`, `tests/` or
             `docs/`; `.agent/decisions.md` is not in it either.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f031-r68.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f031-r68.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own, because a digest
    written inside the text it measures cannot be true; G2 has you measure four
    points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations — a corrected slice destroys the transport proof.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3. The EVIDENCE JOB and the
    ZIP run AFTER C2 and BEFORE C3, in that order, because the protocol requires
    the package to be built from a clean tree at the head carrying every CONTENT
    commit, and because C3 must quote the package filename and its SHA-256 —
    values that do not exist until the zip has been built.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES CLOSURE 1. That is
    ordered: the plan becomes current at C1.
 5. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph of
    your own and never mint a finding id. LEDGER68 carries ONE paragraph: the
    CLOSURE 1 gate entry. NO FINDING IS RESOLVED AND NONE IS REGISTERED THIS
    ROUND. If you find a defect, report it in the handback under Deviations and
    let the reviewer rule on it; do not repair it and do not name it with an id.
 6. THE LEDGER SETS MOVE ONCE. Across C2 `^Gate: F\d+ R\d+ — ` moves 48 to 49
    with the ADDED key exactly `F031 R67`. `^- R-\d+ — ` stays 268,
    `^Done: R-\d+ — ` stays 17, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. The open set is 251 before C2 and 251 after C2.
 7. THE ZIP IS A BLOCKER, NOT A BEST EFFORT. If the build fails, or if the
    package status is anything other than `READY_FOR_REVIEW`, STOP: do not turn
    C3 into a success report. Record the RAW error and the real status in the
    handback and hand back with the failure stated plainly. A closure package
    that does not exist is a closure that does not happen.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C3. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 9. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree. The primary
    checkout reads `git status --porcelain` 0 lines at every commit AND
    immediately before the zip build — the protocol invalidates a package built
    from a dirty tree, and a gitignored artifact is not a dirty tree.
10. YOUR HANDBACK FITS THE TIER ITS BUNDLE EARNS. Read the `### handoff.md`
    section of AGENTS.md, count the commits this Bundle orders, and derive your
    own cap from that rule — do not take a number from this block. Write NO
    BLANK LINE between a `###` commit heading and its table, none between a
    `##` heading and its first line, and none between one commit block and the
    next. Declare DECISION D15 only if the MANDATED content still does not fit
    in that shape, and name what actually caused it.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, `cd x && y`,
    file redirects, and every form of environment assignment. Route anything
    that counts, hashes or compares through a quoted python heredoc, read real
    exit codes from `subprocess.run(...).returncode`, and pass `cwd=` rather
    than `cd`. Run pytest SERIALLY — never two pytest processes alive at once.
    `--timeout` IS NOT AVAILABLE to pytest here: passing it exits 4 and reports
    no failure. `bash scripts/make_review_zip.sh` is a single command and is
    allowed as one.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `a6384213` was produced
    by a reviewer script or tool run at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING. ONE EXCEPTION IS NAMED WHERE IT OCCURS: G7's
    full-suite reading was taken at `44fd8df9`, which differs from the round base
    in `.agent/handoff.md` ALONE.
13. THIS IS NOT THE LAST ROUND OF ITS SESSION. Write no SESSION line. The next
    expected action is CLOSURE 3 OF 3 and you name it by that label and by no
    round number, because §3 item 35 forbids numbering a round that has not
    begun.

Done when — run every gate yourself and record its REAL exit code, ONE LINE per
gate in the handback with transcripts kept out of it. G1 through G13 all run
BEFORE C3, so the handback can quote every one of them. G14 is the single
exception and its own text states how it is treated. The round base is
`a6384213` throughout. Read every non-current revision with
`git show <rev>:<path>` into memory; never write a past blob over a tracked file.
 G1. BRANCH, CLEANLINESS, STOP. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2,
     and again immediately BEFORE the zip build. `.agent/STOP` read from disk
     before C0a and before C3, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f031-r68.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C2 — all four must be EQUAL — and say whether C0a and
     C0b are the same git blob. Report whether any line of the block as saved is
     a run of a single repeated character, which must come back as none. THEN
     STATE IN ONE SENTENCE WHAT THIS PROOF COVERS: the scratch file, the saved
     copy, its mirror and the working copy, and NOT the bytes of any prompt.
 G3. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES. Report how many slices your extractor printed, each
     slice's own line count, the CONTENT total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE at most 400, TOTAL at most
     490.
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R68 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G5. THE LEDGER APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus LEDGER68. The reviewer measured the base blob at
     `a6384213` itself: 991374 bytes over 397 blank-line units. If it reads
     differently before C2, something moved this round did not order — stop and
     hand back. Report both byte counts and the sum. Then the SECOND, INDEPENDENT
     reader: split the whole file on blank lines, let N be the number of
     paragraphs YOUR SCRIPT COUNTS in that slice — never a number this block
     asserts — and compare the LAST N units against the slice's N paragraphs IN
     ORDER. Report N and the unit count before and after. THE NEGATIVE CONTROL
     GOES ON THE FIRST APPENDED PARAGRAPH, AT A BYTE OFFSET, NOT A CHARACTER
     OFFSET — the file carries multi-byte em dashes and a character offset lands
     outside the appended region where the control proves nothing. Flip ONE byte
     IN MEMORY and report that BOTH readers REJECT it. Never mutate the tracked
     file.
 G6. THE LEDGER SETS. Report at two points — before C2 and after C2 — the
     line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the finding ids, the
     RESOLVED ids and the gate keys ADDED and REMOVED as SETS, whether all ids
     are DISTINCT, and the maximum id, which is `R-0707` at both points. Every
     movement constraint 6 names is checked here, INCLUDING the ones that must
     NOT move. Report the open set at both points.
 G7. THE FULL SUITE — CLOSURE PRECONDITION 2, run by YOU in the PRIMARY checkout
     at C2 from the repository root: `python3 -m pytest -n auto -q`. Report the
     REAL exit code, the summary line verbatim, the wall clock, and the COUNT of
     lines matching `^FAILED`. PROVE YOUR `^FAILED` EXTRACTOR IS NOT BLIND by
     running it over a string you know contains such a line and reporting that it
     matched — a zero from an extractor that cannot match is not a reading.
     FIRST, WARM THE FRONTEND BUILD, AND REPORT THAT YOU DID: confirm
     `apps/ui/dist/index.html` EXISTS and its mtime is GREATER than the mtime of
     every file under `apps/ui/src`, and report both readings. THE REVIEWER RAN
     THIS GATE TWICE AT `44fd8df9`, WHICH DIFFERS FROM THE ROUND BASE IN
     `.agent/handoff.md` ALONE, AND GOT TWO DIFFERENT COLOURS, so you are
     told both. With `apps/ui/dist` ABSENT the run is RED at exit 1: one test,
     `tests/ui_server/test_live_state.py::TestUIServerIntegration::test_api_invalid_token_403`,
     fails with `Failed: Server did not start in time` because the server's
     auto-build is still running when that test's 5-second wait expires, and the
     captured stderr says `React UI not built` — 1 failed, 17816 passed, 20
     skipped. With `apps/ui/dist` PRESENT AND NEWER THAN `apps/ui/src` the run is
     GREEN at a REAL exit 0, 17817 passed and 20 skipped with ZERO `^FAILED`
     lines, reproducing the R65 integration gate exactly. THE SECOND READING IS
     THE PRECONDITION'S, and the first is a cold-start race in the test harness,
     not an F031 defect: the reviewer is carrying it to CLOSURE 3 as a closure
     CANDIDATE, and you neither register it nor repair it. If your own run is RED
     for ANY OTHER reason, or red with a warm dist, STOP and hand back.
 G8. INTEGRITY — CLOSURE PRECONDITION 3. The `remedy` CLI is NOT available in
     this session; call the module instead:
     `packages.orchestration.integrity_gate.run_integrity_checks()`, with the
     repository root as the working directory. Report every check's name and
     status, plus `.passed` and `.fail_count`. The reviewer ran it at `a6384213`
     and measured all five of `handler_import`, `live_review_verdict`,
     `plan_consistency`, `relevant_untracked` and `high_blockers_open` at PASS.
     REPORT, DO NOT RELY: open finding R-0648 records that the
     `high_blockers_open` check cannot parse this repository's ledger and
     therefore always passes, so its PASS is a tool reading and not evidence
     about findings. Report also `git status --porcelain` at that moment, which
     must be 0 lines.
 G9. THE EVIDENCE JOB. Write EVIDENCESCRIPT to `.remedy-wt/f031_evidence.py`
     byte for byte plus one newline, then run it with `python3` FROM THE
     REPOSITORY ROOT and report its REAL exit code and its full stdout. It
     asserts, BEFORE writing anything, every precondition that has historically
     produced a BLOCKED_EVIDENCE package: `len(node_ids) == selected`, zero
     deselected, `test_files` sorted and all real files, a `^vr-\d{4,}$` run id,
     a 40-character base commit, and `output_hash` equal to sha256 of
     `stdout_summary` exactly. It scans every packaged string with the packager's
     OWN `_unsafe_text` and carries a red control proving that scanner bites. If
     any assertion fires the bundle is NOT written: report the failure and STOP,
     per constraint 7. The reviewer ran the four scoped suites at `a6384213` and
     measured 35, 4, 41 and 7 selected with 0 deselected, node ids equal to
     selected in every case, 0 rejected strings and the red control truthy.
 G10. THE REVIEW ZIP. With `git status --porcelain` at 0 lines, run
     `bash scripts/make_review_zip.sh --evidence-dir <the directory G9 wrote>`
     and report its REAL exit code, the final package FILENAME, its SHA-256 and
     its PACKAGE_STATUS. Then report, from the manifest INSIDE that package,
     `committed_review_subject.base_commit` and `.head_commit`, and require the
     head to equal the commit C2 created and the base to equal
     `6325ac2fad76ca94e23f7bd02c80427d28e05f1f`. Compute the SHA-256 YOURSELF
     over the published file rather than quoting the script's own line, and
     report both so they can be compared. A status other than
     `READY_FOR_REVIEW`, or a non-zero exit, is a BLOCKER under constraint 7.
 G11. STRUCTURE, ARTIFACTS AND MARKERS, reported for the commits BEFORE C3.
     Compare the path set of `git diff --name-only a6384213..C2` BOTH WAYS
     against this round's expected set — the Change line's list MINUS
     `.agent/handoff.md`, which C3 writes — and report both residues EMPTY.
     Report `git diff --stat a6384213..C2` restricted to `apps/`, `packages/`,
     `tests/` and `docs/` — the last WHOLE — and confirm each EMPTY. Report each
     commit's insertions from `git diff --numstat` for C0a through C2, confirm
     each single-parent and under 500. Line-anchored `^<<<SLICE ` and `^<<<END `
     are 0 and 0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C2,
     against a CONTROL over the C0a blob which is not 0. THEN PROVE NEITHER
     ARTIFACT ENTERED THE REPOSITORY: `git ls-files` over the evidence directory
     and over the published zip each 0 lines, `git ls-files .remedy-wt` 0 lines,
     `git status --porcelain` 0 lines, `git worktree list` 1 line, and
     `git branch --list "tmp/*"` 0 lines.
 G12. THE OPEN PR GATE, READ AND NOT ACTED ON.
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft` —
     report it verbatim. CREATE NO PR AND MERGE NOTHING. The closure protocol
     creates the PR itself at CLOSURE 3, after the STATUS line is authored from
     the values G10 produces.
 G13. STALENESS. Every sentence C1 and C2 land that states a fact about a file
     is re-measured at C2; any that has gone stale is REPORTED as a residual and
     never repaired by editing a slice. Report explicitly that you checked and
     name any residual.
 G14. PUSH. After C3, run `git push origin feature/f031-decision-inbox`. No
     `--force`, no `--force-with-lease`, no history rewrite, no branch deletion.
     ITS OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: C3 is authored
     before the push exists, so `.agent/handoff.md` states the push only as an
     INTENT under `## External actions`, with NO exit code and NO remote tip.
     Report the real exit code and the resulting remote tip in your completion
     report to the reviewer instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C3, in the shape constraint 10 orders: feature and round, branch,
             the round base SHA, the per-commit changed-files table with the
             `+/-` column taken from `git diff --numstat` ITSELF and agreeing
             cell for cell with G11, an item-status row for EVERY Bundle item
             INCLUDING the evidence job and the zip, ONE LINE PER GATE for G1
             through G13 with its real exit code, the open-findings count after
             this round, and the next expected action. THE THREE VALUES CLOSURE 3
             CANNOT BE AUTHORED WITHOUT GET THEIR OWN SECTION, `## Closure
             values`, stating the evidence job id, the package FILENAME, the
             package SHA-256 you computed yourself, the PACKAGE_STATUS, and the
             manifest's `committed_review_subject.head_commit` in full. SAY
             PLAINLY THAT NO FINDING MOVED IN EITHER DIRECTION and that nothing
             under `apps/`, `packages/`, `tests/` or `docs/` changed. Make the
             next-action section CLOSURE 3 OF 3 — the reviewer authors the STATUS
             line from those three values, the worker commits it LAST with the
             README capability sync in the SAME commit, writes any candidates to
             `.agent/candidates.md`, and creates the PR, which is NOT merged this
             session — and name no round number for it.

<<<SLICE PLANF031R68
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1-D26.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
CLOSURE 2 of 3. This round records the CLOSURE 1 verdict, then builds the two
artifacts closure cannot be authored without: a fresh feature-scoped evidence
bundle and a FRESH review zip built from a clean tree at the reviewed head. It
builds no product code. T001, T002 and T003 are complete, the integration gate
PASSED, and the Built State section landed last round, so closure preconditions
1 through 5 are all either met or re-confirmed by this round's own gates.

## Next Steps
1. CLOSURE 3 of 3 — the reviewer authors the STATUS line from the evidence job
   id, the package filename and the package SHA-256 this round produces; the
   worker commits it LAST with the README capability sync in the SAME commit,
   writes any candidates to `.agent/candidates.md`, and creates the PR. The PR
   is NOT merged in this session: the gap is the operator's review window.

## Risks
- A FAILING ZIP BUILD IS A CLOSURE BLOCKER, never a thing to work around. The
  feature does not close without the package, and a package built from a dirty
  tree is invalid.
- THE STATUS LINE CANNOT BE AUTHORED BEFORE THE PACKAGE EXISTS. Its evidence
  job id, filename and SHA-256 do not exist until this round produces them, so
  splitting closure across two rounds is forced by the record, not chosen.
- R-0693 IS RESOLVED and was the only open High this feature raised. R-0495 and
  R-0574 are inherited standing Highs from the already-closed F085 and F086,
  documented risks rather than F031 defects, and they rode through six prior
  closures on the same footing.
- R-0648 IS OPEN AND THIS ROUND'S G8 SHOWS IT: the `high_blockers_open` check
  cannot parse this ledger, so its PASS is a tool reading and not evidence
  about findings. The High question is answered by the record above, not by it.
- R-0403 IS OPEN AND THIS PACKAGE WILL SHOW IT: `.remedy-wt/` scratch is a large
  share of every review zip built on this machine. It routes to a paydown
  branch and is not an F031 defect.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 and this round
  moves it by nothing.
<<<END PLANF031R68

<<<SLICE LEDGER68
Gate: F031 R67 — the F031 CLOSURE 1 OF 3 entry. THE ROUND PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF. ITS SUBSTANCE IS THAT TWO CLOSURE PRECONDITIONS WERE MET IN ONE ROUND: `docs/roadmap/features/T5_F031.md` carries a `## Built State` section for the first time, which is precondition 4, and R-0693 — the ONLY open High this feature raised — is resolved, which is what precondition 1 asks of a feature's own findings. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own scratch original at `.remedy-wt/f031-r67.md`, the committed C0a blob, the committed C0b blob and the working copy are ALL sha256 `a951f18adedb9a754696574a5040704118cd24f6577220405851f8a8956ea165` over 26203 bytes and 310 lines, with C0a and C0b the SAME git blob `b3f1bce99b0e` and no line that is a run of one repeated character — and the reviewer had MEASURED that digest BEFORE delegating, so the chain is closed at both ends rather than only at the worker's. EXTRACTION re-measured from the committed C0a blob printed 3 slices at 45, 3 and 75 content lines, CONTENT 123, TOTAL 310 and PROSE 187, both caps met. THE PLAN at C1 is byte-equal to PLANF031R67 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 45. THE LEDGER APPEND at C2 proves twice: 986008 + 1 + 5365 = 991374 against a committed 991374, and the second reader counted N 2 with units 395 before and 397 after, the last 2 units EQUAL IN ORDER to the slice's 2 paragraphs, with a one-byte flip in the first appended paragraph REJECTED by both readers. THE BUILT STATE APPEND at C3 proves the same way: 11452 + 1 + 5163 = 16616 against a committed 16616, N 5, units 24 before and 29 after, equal in order, both readers rejecting the flip; `^## Built State$` went 0 to 1 while `^## Design amendments` stayed at 4 and every pre-existing line of that file is preserved in its original order — the section was APPENDED and nothing was edited, which is what let a docs commit touch a roadmap file without disturbing the four amendment sections that record how the design moved. THE SETS MOVED EXACTLY TWICE AND ONLY TWICE: `^Gate: F\d+ R\d+ — ` 47 to 48 adding exactly `F031 R66`, and `^Done: R-\d+ — ` 16 to 17 adding exactly `R-0693`, while `^- R-\d+ — ` stayed 268, `^Landed: R-` stayed 0 and `^Gate: R\d+ — ` stayed 19; no finding id was added or removed; all ids DISTINCT at both points with maximum `R-0707`; the open set went 252 to 251. NOTHING ELSE MOVED: both path residues EMPTY over the five-path set, `apps/`, `packages/`, `tests/`, `docs/roadmap/STATUS.md` and `README.md` each EMPTY, `.agent/gate_f031_r65/` 0 lines, markers 0 and 0 in all three edited files against a CONTROL of 3 and 3 over the C0a blob, insertions 310, 252, 22, 4 and 76, each commit single-parent and under 500, and the worktree, scratch and untracked readings all clean. THE READERS ARE UNMOVED, re-run serially by the reviewer with never two pytest processes alive at once, every one a REAL exit 0 with zero `^FAILED` lines: the canary 42, `tests/ui_contracts/` 566 passed and 4 skipped, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, `tests/docs/` 295 and `tests/orchestration/test_roadmap_index.py` 30 — the last two ordered because the round edits `docs/roadmap/**`, and every count EQUAL to the reading at `eed7e010`. THE RESOLUTION IS EVIDENCE-BACKED RATHER THAN ASSERTED: the reviewer read all three parts of the DECISION F031 D19 repair on disk before authoring the `Done:` text — the `fp:` dispatch to `flight_plan.resolve_flight_plan_approval` in the write door, the third endpoint key computed from the door's own predicate in `decision_inbox._answerable_by_decision_resolve`, and `decisionCard.ts` line 229 gating the posting button on that key — so the ledger and the code now agree about what this feature ships. THE HANDBACK IS HONEST ABOUT ITS OWN SHAPE: 59 lines against the 100 its six-commit bundle earns, every mandated section present, every `+/-` cell agreeing with `git diff --numstat`, and no DECISION D15 declaration made or needed. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER68

<<<SLICE EVIDENCESCRIPT
"""F031 closure evidence bundle. Run with python3 from the repository root."""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO = os.path.abspath(".")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f031_closure_evidence", "remedy-job-evidence-f031-closure"
)
BASE = "6325ac2fad76ca94e23f7bd02c80427d28e05f1f"
assert len(BASE) == 40, BASE

HEAD = subprocess.run(
    ["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True
).stdout.strip()
assert len(HEAD) == 40, HEAD


def _tail(text):
    """The last 2000 chars on a WHOLE-LINE boundary, path-scrubbed TWICE.

    job_evidence._scrub_paths only relativises paths under REPO. A pytest header
    line can end in the interpreter's own absolute path, which
    build_review_manifest._unsafe_text correctly rejects as a local absolute
    path -> BLOCKED_EVIDENCE.
    """
    from packages.common.path_redaction import scrub_paths
    from packages.orchestration.job_evidence import _scrub_paths

    cut = text[-2000:]
    if len(text) > 2000 and "\n" in cut:
        cut = cut[cut.index("\n") + 1:]
    return scrub_paths(_scrub_paths(cut, REPO))


def mkrun(rid, path, expect):
    """One verification record.

    Node ids come from --collect-only, never from a -v log: a parametrized id
    can contain whitespace and a regex over -v output splits it (R-0611).
    NOTHING is deselected here. All four of F031's scoped suites were scanned
    with build_review_manifest._unsafe_text at 44fd8df9 and none of their ids
    was rejected, so this feature needs no -k filter. A FULL-SUITE node-id list
    is never recorded: len(node_ids) == selected forbids filtering, and the
    packaging metadata scan rejects the redaction-torture ids by design.
    """
    assert re.match(r"^vr-\d{4,}$", rid), rid
    sel = [path, "-q"]
    cmd = "python3 -m pytest " + path + " -q"
    collect = subprocess.run(
        ["python3", "-m", "pytest"] + sel + ["--collect-only"],
        cwd=REPO, capture_output=True, text=True,
    )
    assert collect.returncode == 0, (rid, collect.returncode)
    ids = [ln for ln in collect.stdout.split("\n") if ln.startswith("tests/")]
    run = subprocess.run(
        ["python3", "-m", "pytest"] + sel, cwd=REPO, capture_output=True, text=True,
    )
    text = run.stdout + run.stderr
    assert run.returncode == 0, (rid, run.returncode, text[-400:])
    passed = sum(int(x) for x in re.findall(r"(\d+) passed", text))
    failed = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", text))
    skipped = sum(int(x) for x in re.findall(r"(\d+) skipped", text))
    desel = sum(int(x) for x in re.findall(r"(\d+) deselected", text))
    dur = float(re.findall(r"in ([\d.]+)s", text)[-1])
    assert (passed, failed, skipped) == (expect, 0, 0), (rid, passed, failed, skipped)
    assert desel == 0, (rid, desel)
    selected = passed + failed + skipped
    assert len(ids) == selected, (rid, len(ids), selected)
    files = sorted({i.split("::")[0] for i in ids})
    for f in files:
        assert os.path.isfile(os.path.join(REPO, f)), f
    return {
        "run_id": rid, "command": cmd,
        "exit_code": 0, "passed": passed, "failed": failed, "skipped": skipped,
        "selected": selected, "deselected": desel, "node_ids": ids,
        "test_files": files, "duration_seconds": dur,
        "head_sha": HEAD, "stdout_summary": _tail(text),
    }


runs = [
    mkrun("vr-0001", "tests/orchestration/test_decision_inbox.py", 35),
    mkrun("vr-0002", "tests/ui_server/test_decisions_endpoint.py", 4),
    mkrun("vr-0003", "tests/ui_contracts/test_decision_answer_wiring.py", 41),
    mkrun("vr-0004", "tests/ui_server/test_command_dispatch.py", 7),
]
for r in runs:
    print(r["run_id"], "selected", r["selected"], "node_ids", len(r["node_ids"]),
          "deselected", r["deselected"], "files", len(r["test_files"]),
          "dur", r["duration_seconds"])

# Every packaged string is scanned; prove the ids and commands pass BEFORE the
# bundle is written, so a rejection is a red here and not a BLOCKED zip later.
sys.path.insert(0, os.path.join(REPO, "scripts"))
from build_review_manifest import _unsafe_text  # noqa: E402

rejected = [(r["run_id"], v) for r in runs for v in r["node_ids"] + [r["command"]]
            if _unsafe_text(v)]
print("SCAN rejected strings:", len(rejected), rejected[:3])
assert not rejected, rejected
print("SCAN red control:", _unsafe_text("/home/user/repo/tests/x.py::t"))

now = datetime.now(timezone.utc)
from packages.orchestration.job_evidence import create_manual_completion_bundle  # noqa: E402

result = create_manual_completion_bundle(
    EVIDENCE_DIR,
    repo_root=REPO,
    base_commit=BASE,
    head_commit=HEAD,
    job_id="f031-closure",
    job_title="F031 Decision inbox - closure",
    step_range="T001-T003",
    prior_job_ids=["f022-closure"],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F031 closure",
    review_feature_id="f031",
)
print(json.dumps(result, indent=2, sort_keys=True))

# The output_hash preimage rule: sha256 over stdout_summary EXACTLY. This is the
# pitfall that blocked the F083 closure and it is not in the protocol's list.
vt = os.path.join(EVIDENCE_DIR, "verification_tests.json")
if os.path.isfile(vt):
    with open(vt, encoding="utf-8") as fh:
        doc = json.load(fh)
    for row in doc.get("runs", []):
        want = hashlib.sha256(row.get("stdout_summary", "").encode()).hexdigest()
        print("OUTPUT_HASH", row.get("run_id"), "matches sha256(stdout_summary):",
              row.get("output_hash") == want)
else:
    print("OUTPUT_HASH no verification_tests.json at", vt)
print("EVIDENCE_DIR", EVIDENCE_DIR)
<<<END EVIDENCESCRIPT
