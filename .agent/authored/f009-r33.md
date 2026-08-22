── STEP CLOSURE-ONE — F009 ──
Goal:        Produce the two artefacts the F009 STATUS line quotes: the closure
             EVIDENCE BUNDLE and a FRESH REVIEW ZIP, both covering the accepted
             HEAD this round creates. The R32 verdict is recorded first. NO
             STATUS line, NO README edit and NO pull request happen here —
             docs/roadmap/STATUS_closure_protocol.md puts those in the closure
             commit that FOLLOWS a READY zip, and DECISION F085 D9 is why
             closure is two rounds and not one.

Fortschritt: ~100 % (T001 gebaut · T002 gebaut · T003 gebaut und verifiziert ·
             Integrations-Gate BESTANDEN · Evidence-Job und Review-Zip in
             dieser Runde; danach bleiben nur STATUS-Zeile, README-Sync und der
             Pull Request) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R32 verdict
             and the accepted HEAD · then, at C2 with a clean tree and in this
             order, the push, the evidence job, the integrity check and the zip
             · C3 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r33.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/handoff.md` (C3). NOTHING under `packages/`, `apps/`,
             `docs/` or `tests/` is touched — in particular NOT
             `docs/roadmap/STATUS.md` and NOT `README.md`, which belong to the
             NEXT round. The evidence bundle, the evidence script and the zip
             are written under the gitignored `.remedy-wt/` and are NEVER
             committed: a committed evidence dir puts evidence files inside the
             review subject and the package builds BLOCKED_EVIDENCE (the F147
             attempt-2 lesson, recorded in the closure protocol).

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. C1 precedes the
    ledger commit because the plan must be current before it (checklist item
    23). C2 is the LAST commit before the artefacts and its SHA is the ACCEPTED
    HEAD that both the bundle and the zip must record; C3 writes the handback
    and is created only after both artefacts exist.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `- R-`
    entry, no `Done:` line and no `Landed:` line. The next free id is R-0648
    when the round ends, exactly as it was when the round began. Anything you
    notice is reported in the handback as an OBSERVATION with no id spent —
    findings raised during a closure review are candidates, per the closure
    protocol's "Closure-candidate findings" section.
 4. ONE APPEND AND ONE WHOLE-FILE REPLACEMENT. PLANF009R33 replaces
    `.agent/plan.md` at C1 in full. LEDGER33 appends to `.agent/live_review.md`
    at C2 based on the ROUND BASE. EVIDENCESCRIPT is neither: it is COPIED byte
    for byte to `.remedy-wt/r33_evidence.py` and executed, never committed as
    itself — its bytes reach the permanent record inside the C0a blob. There is
    NO FROM/TO pair in this round; order no containment reading and no FROM
    count anywhere.
 5. The reviewer measured the targets at the round base
    `1dc72f82333f681fe61af0b75712ac8ff7e34c39`: `.agent/live_review.md` is
    584339 bytes over 1144 lines and ends in exactly ONE newline;
    `.agent/plan.md` is 2029 bytes over 38 lines. So the append is one newline
    followed by its slice.
 6. EVERY reading at a revision other than the one your shell is on is taken
    with `git show <sha>:<path>` into memory or into a scratch file under the
    gitignored `.remedy-wt/`. NEVER write a base blob over a tracked file and
    restore it: docs/agents/self_drive_protocol.md guardrail G5 forbids
    mutating the primary checkout (finding R-0594).
 7. Count LEDGER33's paragraphs with your script rather than from any sentence
    in this block.
 8. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
 9. NEVER invoke an artefact build through a pipe. `bash script | tail -60`
    returns `tail`'s status and the script's own exit code becomes
    unmeasurable, which cost the F008 R35 round a declared deviation and a
    second zip build at the same head. Run each build under a wrapper that
    captures the real exit code, and report that code.
10. SIZE, measured at emission by reading it back out of the assembled bytes
    and computing PROSE as TOTAL minus the slices' CONTENT lines, with marker
    lines counted as prose per DECISION F085 D5: this block is 462 lines TOTAL
    against DECISION F085 D6's 490 cap, 276 of them PROSE against D5's 400.
    Re-measure both from the committed C0a blob; a disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C3: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1 and C2 and again immediately before each
     artefact build. Report the round base SHA you read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r33.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for all three. C0b is written FROM the committed
     C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 10's two numbers from that same blob — TOTAL, and PROSE as
     TOTAL minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R33 — report `cmp` exit
     and both sha256, with a negative control against another file exiting
     non-zero. Report `wc -l` for the plan against the 50-line cap of
     AGENTS.md. Line-anchored in the plan, `^## Goal$` and `^## Next Steps$`
     each read 1, and the plan matches `\bF\d{3}\b` with `F009`.
 G5  THE APPEND, under TWO independent readers, with a negative control on the
     FIRST appended paragraph (finding R-0631). LEDGER33 at C2 based on the
     round base. (a) the base blob is a byte-exact PREFIX and the remainder
     equals a newline plus that slice — report its sha256, bytes and lines;
     (b) N is counted BY YOUR SCRIPT and the last N blank-line-separated units
     equal the slice's N paragraphs IN ORDER. Then flip one printable byte in
     the FIRST appended paragraph, at equal length, and report that BOTH
     readers REJECT the flip while both ACCEPT the true file. Report
     before/after bytes and lines.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base
     AND at C2: a leading `- R-` id with every captured id DISTINCT at each; a
     leading `Done: R-` id; a leading `Landed: `; a leading `Gate: R` key over
     that many DISTINCT keys; and the `Gate: R33` key. Report EVERY one of
     those five readings at BOTH points — none of them belongs in a round
     report, because a reading routed there dies with the session (finding
     R-0494). The reviewer's base readings, which yours must reproduce:
     entries 213 all DISTINCT, `Done:` 3, `Landed: ` 0, `Gate: R` keys 32 over
     32 DISTINCT, `Gate: R33` 0. Constraint 3 fixes that entries read 213 all
     DISTINCT at C2 as well — the reading that shows this round minted nothing
     — and that `Gate: R33` reads 1 at C2.
 G7  THE ANCHORING CONTROL, ordered as a DIFFERENCE and never as a maximum
     (finding R-0647), and ordered with its SCAN SHAPE NAMED, because "an
     unanchored occurrence of `Gate: R`" has two readings that differ by
     dozens of hits and the R32 worker had to declare the ambiguity — an
     instance of open R-0630. Over `.agent/live_review.md` at the round base
     and again at C2, report all five: leading `- R-` ids; DISTINCT strings
     matching `R-\d{4}` anywhere; how many of those distinct strings were NEVER
     registered as a leading id; leading `Gate: R\d+` keys; and unanchored
     occurrences under BOTH scans, stated separately — the KEY-SHAPED scan
     `Gate: R\d` and the LITERAL substring `Gate: R`. The reviewer's base
     readings, which yours must reproduce: 213 anchored ids, 273 distinct
     unanchored strings, 60 never registered, 32 anchored keys, 84 key-shaped
     and 131 literal. Report the C2 numbers as MEASURED — this block predicts
     none of them.
 G8  Report the max REGISTERED id, read line-anchored, and the open count by
     DECISION F009 D10's rule at the round base and at C2. This reading fixes
     the next round's id ceiling and is NOT an anchoring control; G7 is the
     control. The reviewer's base readings: max REGISTERED id R-0647, open 210.
     Constraint 3 fixes both are UNCHANGED at C2.
 G9  RANGE: the range from the round base to C2 lists EXACTLY the declared
     paths other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `packages/`, `apps/`, `docs/` or
     `tests/` — report that `docs/roadmap/STATUS.md` and `README.md` are both
     absent from that list, since this round's whole discipline is that they
     belong to the next one. Each commit has ONE parent; `git show --numstat`
     and `git diff --numstat` AGREE on every cell — invoke `git show` WITHOUT a
     `--` before the SHA, which turns it into a pathspec and prints nothing;
     every cell equals the `+/-` column of the handback's `## Commits` table
     (checklist item 28), compared cell by cell. Note that for a whole-file
     rewrite `git commit`'s own summary and `--numstat` legitimately differ;
     the tables use the `--numstat` cells the two `git` readings agree on.
     Report each pre-handback commit's insertions against the 500 cap; the
     handback commit's own numbers belong in the round report (item 14).
     Leading `<<<SLICE ` and `<<<END ` read 0 LINES in every file a slice lands
     in, which are `.agent/plan.md` and `.agent/live_review.md` — read that
     count LINE-ANCHORED and not as a substring, because LEDGER33 legitimately
     QUOTES both marker strings mid-line. `git ls-files .remedy-wt` reads 0.
     Classify THIS ROUND's reflog rows by the operation before the first `:`
     and report `amend`, `rebase` and `cherry` each 0; assert no total over the
     whole reflog (R-0601).
 G10 CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q -rf` in the
     PRIMARY checkout, serially, with no other pytest process alive (finding
     R-0518). Report its REAL exit code and the count IT printed. No docs gate
     is owed: this round's change set holds no `docs/` path. The reviewer ran
     the canary at the round base before ordering it — it exits 0 at 42 passed,
     so it can fail honestly (R-0364).
 G11 THE EVIDENCE JOB, at C2, with `git status --porcelain` printing 0 lines
     first and after `git push` has run. Write EVIDENCESCRIPT byte for byte to
     `.remedy-wt/r33_evidence.py`, report that file's sha256 EQUALS the slice's,
     and run it with `python3` from the repository root. Report its REAL exit
     code and the producer's own summary: `authority_count`, `commit_count`,
     `head_commit`, `job_id`, `manual_completion`, `operator_attested_tasks`,
     `total_passed` and `verdict`. Report that the bundle directory did NOT
     pre-exist — read that BEFORE the run — and how many entries it holds
     after. Report the script's own per-run line for each of its five runs, and
     the `OUTPUT_HASH` line it prints for each, which re-reads
     `verification_tests.json` from disk and re-derives sha256 over
     `stdout_summary` EXACTLY. `head_commit` MUST equal C2's SHA; if it does
     not, STOP — something was committed after C2.
     Three producer pitfalls are already handled inside the slice and you only
     need to report what it prints. Node ids come from `--collect-only -q` and
     never from a `-v` log (R-0611), and `len(node_ids) == selected` is
     asserted per run. Whitespace is deliberately NOT asserted away: two suites
     carry one parametrized id each ending `[has space]`, and the reviewer ran
     `scripts/build_review_manifest._unsafe_text` over both of those exact ids
     to `None` — spaces are not what that scan rejects. The third is why three
     runs carry `-k "not escape"`: the parametrization `[../escape]` occurs once
     each in the channel, nonce and audit suites, and that scanner reads
     `../escape` as a local path, so those ids CANNOT be packaged. The slice
     deselects them at run time rather than deleting them from a list, which
     keeps `len(node_ids) == selected` true and records `deselected` honestly,
     and it re-runs the scanner over every packaged id and command with a red
     control before the bundle is written. Report the `SCAN` lines it prints:
     `SCAN rejected strings: 0` and a red control reading `a local absolute
     path`. This is not a prediction — the reviewer executed the whole pipeline
     at the round base, and G13 records both colours it produced.
     Expected per-run values, which the slice also asserts: vr-0001 99 selected
     with 1 deselected, vr-0002 4 with 0, vr-0003 27 with 1, vr-0004 16 with 1,
     vr-0005 11 with 0; `total_passed` 157 and `verdict` PASS_WITH_RISKS.
     The three deselected tests are not lost evidence: they ran green in this
     round's own suites and in the integration gate, and the closure protocol's
     F080 R4 lesson (d) is exactly this — record the clean scoped suites and let
     the rest ride in the integration-gate evidence.
 G12 THE INTEGRITY CHECK, closure precondition 3, run as
     `from packages.orchestration.integrity_gate import run_integrity_checks`
     then `run_integrity_checks()` — the `remedy` CLI is denied by this
     session's command guard, so the F255 R20 and F008 R35 precedent applies.
     Report `passed`, `fail_count` and the name plus status of every check. The
     reviewer ran it at the round base: `passed` True, `fail_count` 0, five
     checks all PASS. Report it AT C2.
 G13 THE REVIEW ZIP, closure algorithm step 2, at C2 with `git status
     --porcelain` printing 0 lines immediately before the build and the branch
     already pushed. Run, from the repository root and NOT through a pipe
     (constraint 9):
     `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f009_closure_evidence/remedy-job-evidence-f009-closure`
     Report its REAL exit code, the package filename and the `final_sha256` the
     script printed, and report that `sha256sum` over the file on disk
     RECOMPUTES the same value. Report `PACKAGE_STATUS`, `member_count`
     cross-checked against `zipfile.namelist()`, `EVIDENCE_AUTHORITATIVE` and
     `REVIEW_SUBJECT_ALIGNMENT`. Then, from `.review_zip_manifest.json` INSIDE
     the package, report `committed_review_subject.base_commit`,
     `head_commit`, `base_is_ancestor`, `commit_count`, `file_count`,
     `packaged_evidence_job_id`, `ready_gate_matrix.ok` with its
     `blocking_reasons`, and `review_subject_evidence_alignment.verdict` with
     its issue and hash-mismatch counts. `base_commit` MUST be the full
     40-character `ce49348b8f5b0374417f5b6c47d8c04966e7108e` and `head_commit`
     MUST equal C2's SHA. PACKAGE_STATUS other than `READY_FOR_REVIEW` is a
     CLOSURE BLOCKER: stop, report it, change nothing to make it pass. The
     package containing `.remedy-wt/` scratch is the already-registered R-0403
     and is NOT a new condition.
     This gate has been shown to produce BOTH colours at the round base, so it
     can fail honestly and a green means something (R-0364, and checklist item
     12's red control). The reviewer built the package twice from a throwaway
     bundle at `1dc72f82`: once with the full node-id lists, which exited 0 and
     produced `PACKAGE_STATUS=BLOCKED_EVIDENCE` with
     `EVIDENCE_AUTHORITATIVE=false` and blocking reasons naming
     `runs[0].node_ids[57]`, `runs[2].node_ids[12]` and `runs[3].node_ids[7]`
     as carrying a local absolute path, plus the consequent
     "VerificationTests total is missing or invalid"; and once with the `-k`
     filter G11 describes, which produced `PACKAGE_STATUS=READY_FOR_REVIEW`,
     `EVIDENCE_AUTHORITATIVE=true` and `REVIEW_SUBJECT_ALIGNMENT=PASS`. Note
     that the EXIT CODE was 0 in BOTH cases: exit 0 is not the reading, and a
     round that reports only the exit code has not run this gate.
     Both throwaway artefacts were deleted before this block was emitted, so
     the bundle directory G11 names does not pre-exist.
 G14 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2 and C3, the round base SHA, one line per gate, and this block's
     `Fortschritt:` line VERBATIM across all four of its lines. Where a gate
     ordered a reading AT SEVERAL POINTS, every point's value appears in the
     file and not only the first (R-0494). Report its `wc -l` against the
     100-line cap AGENTS.md allows for a per-commit table of more than five
     commits; this round has FIVE commits, so the plain 60-line cap applies
     unless a DECISION D15 "Deviations, declared" line names the actual count
     and the mandated content that caused the overage — and given the closure
     values this round must carry, an overage IS expected, so declare it rather
     than dropping a section. The file additionally carries a
     `## Closure values` table with exactly these four rows, which is the sole
     input the NEXT round's STATUS line is authored from: `Evidence job`,
     `package`, `SHA-256`, `accepted HEAD`. Its `## Next` section states that
     the next round is the closure commit — the authored STATUS `[x]` line and
     the README capability sync in ONE commit (R-0154), then the pull request
     — and that no PR exists yet.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C2 and
             again after C3. Create NO pull request: that is the next round.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R33
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R33 is closure round one. It records the R32 verdict, then builds the two
artefacts the STATUS line quotes: the closure evidence bundle for job
`f009-closure` and a FRESH review zip, both covering the accepted HEAD this
round creates. No STATUS line, no README edit and no pull request happen here.

## Next Steps
1. Closure round two: the authored STATUS `[x]` line and the README capability
   sync in the SAME commit (R-0154), then the pull request.
2. The PR is NOT merged in this session; it merges at the next feature's start
   via the Open PR Gate, which is the operator's manual-review window.

## Risks
- The zip is a closure BLOCKER, not a formality: a PACKAGE_STATUS other than
  READY_FOR_REVIEW stops closure rather than being worked around.
- Two open High findings, R-0495 from F085 and R-0574 from F086, are inherited
  from closed features and are documented risks, not F009 defects. F008 closed
  the same way one feature ago, so the F009 verdict is PASS_WITH_RISKS.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R33

<<<SLICE LEDGER33
Gate: R33 — the R32 entry. R32 PASSED. Every one of the eleven gates was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r32.md` at `fc470f84`, `.agent/last_block.md` at `5c47adf5` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f009-r32.md`, are all sha256 3e56e730ad693a0a5dcffce43e006bb4d9bcc0159cabd5c3f78944b0670f3319 over 23131 bytes and 250 lines, and that digest is the one the block named before the round began. The reviewer's own extraction out of the committed C0a blob prints an aggregate of 4 slices over 55 CONTENT lines, and constraint 9's numerals re-measure as 250 TOTAL and 195 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `df1cc995` is BYTE-EQUAL to PLANF009R32 at 38 lines against the 50-line cap with `^## Goal$` and `^## Next Steps$` each reading 1, and `.agent/candidates.md` at `17303fb9` is BYTE-EQUAL to CANDIDATES32; each negative control differs. THE CARRIER IS EMPTY AND THE READING THAT SHOWS IT DISCRIMINATES: line-anchored over `.agent/candidates.md`, a leading `- ` goes 2 to 0, `^NON-EMPTY\.` goes 1 to 0 and `^EMPTY\.` goes 0 to 1, while the UNANCHORED substring `EMPTY.` reads 1 at BOTH points because `NON-EMPTY.` contains it — the block named that trap in its own gate text and ordered the anchored form, which is R-0646 applied in the round that registered it. BOTH APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS, each with its own negative control: FINDINGS at `11ac72e1` is based on the round base, 576883 to 580011 bytes and 1138 to 1142 lines, N counted at 2; LEDGER32 at `7e5bf4b9` is based on C2 rather than on the round base, exactly as constraint 4 fixed, 580011 to 584339 bytes and 1142 to 1144 lines, N counted at 1; for each append separately, an equal-length printable-byte flip in the FIRST appended paragraph is REJECTED by both readers while both ACCEPT the true file. THE SETS HELD line-anchored at line start at all THREE points: at the round base entries 211 all DISTINCT, `Done:` 3, `Landed: ` 0, `Gate: R` keys 31 over 31 DISTINCT, `Gate: R32` 0, max REGISTERED id R-0645, 208 open; at C2 entries 213 all DISTINCT with max R-0647 and 210 open and `Gate: R32` still 0; at C3 entries UNCHANGED at 213 with `Gate: R` reaching 32 over 32 DISTINCT and `Gate: R32` at 1. THE TWO CARRIED DEFECTS ARE NOW REGISTERED: R-0646 records a gate that counted a markdown construct its named target does not contain, and R-0647 records an anchoring control ordered as a maximum, which coincides precisely when the round's own new id is the ceiling; `.agent/candidates.md` was emptied in the same round, which is what docs/roadmap/STATUS_closure_protocol.md's disk-vehicle rule and docs/agents/planner_reviewer_prompt.md §1 item 4 require of the first reviewed round of a session that starts with a non-empty carrier. THE ANCHORING CONTROL WAS ORDERED AS A DIFFERENCE, applying R-0647 in the round that registered it: at the round base 211 anchored ids against 271 distinct unanchored strings of which 60 were never registered, and 31 anchored `Gate: R` keys; at C3 213, 273, 60 and 32. THE RANGE HELD: base→`17303fb9` lists exactly the five declared paths, set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/`, `docs/` or `tests/`; every one of the round's seven commits has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own table, at 250/0, 160/152, 6/8, 4/0, 2/0, 5/40 and 52/58; pre-handback insertions 250, 160, 6, 4, 2 and 5, each under the 500 cap, and the handback commit's own 52 is under it as well; zero leading `<<<SLICE ` and `<<<END ` LINES in all three slice targets; `git ls-files .remedy-wt` 0; the round's seven reflog rows all classify as `commit`, with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog. THE CANARY IS THE REVIEWER'S OWN, re-run serially in the primary checkout: it exits 0 at 42 passed. THE HANDBACK IS 94 LINES against the 100 AGENTS.md allows a per-commit table of more than five commits, carries every mandated section and an item-status row for each of C0a, C0b, C1, C2, C3, C4 and C5, and repeats the block's four-line `Fortschritt:` VERBATIM. ONE DEVIATION WAS DECLARED AND IT WAS THE RIGHT CALL: G7 ordered "unanchored occurrences of `Gate: R`" without naming the scan, and the two available readings differ by dozens — the KEY-SHAPED scan `Gate: R` followed by a digit reads 81 at the base and 84 at C3, which is the reading the reviewer had measured and ordered, while the LITERAL substring reads 124 and 131, the extra hits being backticked prose mentions with no round number after them. The worker reported BOTH readings, adjusted nothing to make a number agree, and named the discriminator; the reviewer reproduces all four values. That is an instance of OPEN R-0630, whose rule is that a count gate over this file must name the anchor it is read under because the file legitimately quotes its own gate headers, so per checklist item 30 the evidence is added to R-0630 here rather than minted as a second id — and the R33 block that follows names the scan shape for both readings.
<<<END LEDGER33

<<<SLICE EVIDENCESCRIPT
"""F009 closure evidence bundle. Run with python3 from the repository root."""
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone

REPO = os.path.abspath(".")
EVIDENCE_DIR = os.path.join(
    REPO, ".remedy-wt", "f009_closure_evidence", "remedy-job-evidence-f009-closure"
)
BASE = "ce49348b8f5b0374417f5b6c47d8c04966e7108e"
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


def mkrun(rid, path, expect, kexpr=None, expect_deselected=0):
    """One verification record. Node ids come from --collect-only, never from a
    -v log: a parametrized id can contain whitespace and a regex over -v output
    splits it (finding R-0611). Two of this feature's ids legitimately end in
    `[has space]` and nothing here asserts their absence — the packaging scan
    rejects secrets, local paths and control characters, not spaces.

    THREE ids do have to go, and `-k` is how they go honestly. The
    parametrization `[../escape]` appears once in each of the channel, nonce and
    audit suites, and `build_review_manifest._unsafe_text` reads `../escape` as
    a local path, so a bundle carrying those ids packages BLOCKED_EVIDENCE. This
    is the F080 R4 lesson (d) class: an id that is path-traversal torture BY
    DESIGN. `len(node_ids) == selected` forbids deleting an id from the list, so
    the test is DESELECTED at run time instead and both halves of the record
    stay true — the run really selected what the list holds, and `deselected`
    says how many it did not. `--deselect` is not usable here because the id it
    would take contains `../` and the command string is scanned too.
    """
    assert re.match(r"^vr-\d{4,}$", rid), rid
    sel = [path, "-q"] + (["-k", kexpr] if kexpr else [])
    cmd = "python3 -m pytest " + path + " -q" + (' -k "' + kexpr + '"' if kexpr else "")
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
    assert desel == expect_deselected, (rid, desel, expect_deselected)
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
    mkrun("vr-0001", "tests/ui_server/test_command_channel.py", 99, "not escape", 1),
    mkrun("vr-0002", "tests/ui_server/test_command_dispatch.py", 4),
    mkrun("vr-0003", "tests/orchestration/test_command_nonce.py", 27, "not escape", 1),
    mkrun("vr-0004", "tests/orchestration/test_command_audit.py", 16, "not escape", 1),
    mkrun("vr-0005", "tests/orchestration/test_secure_fs.py", 11),
]
for r in runs:
    print(r["run_id"], "selected", r["selected"], "node_ids", len(r["node_ids"]),
          "deselected", r["deselected"], "files", len(r["test_files"]),
          "dur", r["duration_seconds"])

# Every packaged string is scanned; prove the ids and commands pass BEFORE the
# bundle is written, so a rejection is a red here and not a BLOCKED zip later.
import sys  # noqa: E402
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
    job_id="f009-closure",
    job_title="F009 The single write channel - closure",
    step_range="T001-T003",
    prior_job_ids=["f008-closure"],
    verification_runs=runs,
    timestamp=now.replace(microsecond=0).isoformat(),
    generated_at=now.isoformat(),
    num_tasks=3,
    note_prefix="operator-attested manual completion - F009 closure",
    review_feature_id="f009",
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
<<<END EVIDENCESCRIPT
