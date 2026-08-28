# STEP — F037 Rendered diff viewer, round 27 — THE CLOSURE

## Who you are and what binds you

You are the WORKER of a self-drive round (docs/agents/self_drive_protocol.md).
AGENTS.md is the highest authority and nothing here weakens it. You are the only
actor in this round that writes anything; the reviewer re-runs every gate itself
before issuing a verdict.

BASE. This round starts from commit `6a32be79`, the tip of branch
`feature/f037-rendered-diff-viewer`. Read `.agent/STOP` from disk before your
first commit; if it exists, write the handback and end without doing anything
else.

SESSION. Session 8 of F037, round 27. This session's rounds are R25 (PASSED),
R26 (PASSED) and R27, this one, which ends the session and the feature. Carry
"SESSION 8 of feature F037 · round 27 · rounds so far 27" in the handback.

WHAT THIS ROUND IS. Steps 4 and 5 of docs/roadmap/STATUS_closure_protocol.md —
the STATUS line, the README sync that must travel in the SAME commit, and the
closure PR. THE PR IS NOT MERGED, by anyone, in this session: it merges at the
next feature's start through the Open PR Gate, and that gap is the operator's
manual-review window.

## Goal

Close F037: flip its STATUS line to `[x]` with the package the R26 round built,
sync the four README pins that must agree with the ledger, and open the closure
PR.

## Bundle, in this commit order

- C0a — save the block verbatim to `.agent/authored/f037-r27.md`.
- C0b — mirror the same bytes into `.agent/last_block.md`.
- C1 — rewrite `.agent/plan.md` from the PLANF037R27 slice.
- C2 — append GATER26 to `.agent/live_review.md`.
- C3 — THE CLOSURE COMMIT: all four CLOSUREEDITS pairs plus the handback
  rewrite, in ONE commit. It is the LAST commit on this branch.
- Then push and create the PR. No commit follows C3.

## Change set — these paths and nothing else

- `.agent/authored/f037-r27.md`
- `.agent/last_block.md`
- `.agent/plan.md`
- `.agent/live_review.md`
- `docs/roadmap/STATUS.md` (C3)
- `README.md` (C3)
- `.agent/handoff.md` (C3)

Nothing under `apps/`, `packages/` or `tests/` is touched, and no test is
edited, added, deleted or skipped. `docs/roadmap/features/T5_F037.md` is NOT
touched: its Built State section is already current from R26, which is what
closure precondition 4 requires.

## Slice convention

The authored texts below are delimited by lines beginning `<<<SLICE ` and
`<<<END `, each naming its own label. Delimiter lines never reach a target file.
Apply each slice BYTE FOR BYTE including its trailing newline. The labels are
PLANF037R27, GATER26 and CLOSUREEDITS. CLOSUREEDITS is not applied as a whole
text: it CARRIES four FROM/TO pairs, each introduced by a line beginning `[P`,
and you apply the pairs it names.

<<<SLICE PLANF037R27
# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D11.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse and
virtual scrolling. `docs/roadmap/features/T5_F037.md` holds Goal & Done, the task
slicing, the binding CSS, the design amendments A1 through A6 and the Built State
section recording what actually shipped.

## Current Step
R27 is the CLOSURE round, the last of F037's closure sequence and the last round
of this branch. Every closure precondition is met: the integration gate PASSED at
R25 with no branch-only failure reaching feature code, the R26 package is
READY_FOR_REVIEW at accepted head `5e557a1c`, the integrity gate passes with zero
failures, and F037 carries no open finding of its own. This round books the R26
verdict, flips the STATUS line to `[x]`, syncs the four README pins in that same
commit, and opens the PR — which is NOT merged here.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R26 verdict | ordered | record first |
| C3 STATUS, README and the handback | ordered | one commit, last on the branch |
| the closure PR | ordered | created, never merged |

## Next Steps
1. A fresh session claims the next feature by Rule A5 — `F033 Hunk-level diff
   approval` — and its Open PR Gate merges this feature's PR first.
2. The split-off scope of amendment A6 wants its own STATUS line before F033.
   That remains a PROPOSAL to the operator and is executed by no session.

## Risks
- `R-0714` closes OPEN as a documented Medium risk: a ui_server test runs a real
  frontend build from inside the suite, which F037 does not own and did not
  cause. Closure precondition 1 admits exactly this case.
- The STATUS and README edits must land in ONE commit or the ledger pins in
  `tests/docs/` go red; the reviewer measured that red as the control.
<<<END PLANF037R27

<<<SLICE GATER26
Gate: F037 R26 — the EVIDENCE-AND-ZIP round, the second of F037's closure sequence. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran each independently at `6a32be79`. TRANSPORT AGAIN COVERS THE EMISSION AND NOT MERELY THE WORKER'S SELF-CONSISTENCY: the reviewer's own scratch original `.remedy-wt/f037-r26-block.md` existed before the worker did, and the committed `.agent/authored/f037-r26.md` blob is BYTE EQUAL to it at 31847 bytes, 490 lines, sha256 `e784cecccecd0bf90632583400fa0086e55e027f5f11951d4ddbc39707cdf0da`; at `82cc2579` that path and `.agent/last_block.md` are ONE blob `a6223fec105af40eb6c19c6b4a797978c82a7e0a`.

EVERY SLICE WAS RE-EXTRACTED FROM THE COMMITTED BLOB AND RE-APPLIED BY THE REVIEWER. `.agent/plan.md` at `77cec858` is byte equal to PLANF037R26 including its trailing newline, the control dropping that newline is False, and the file is 44 lines with exactly one `## Goal` and one `## Next Steps`. The append at `514e2991` satisfies reader (a) byte for byte with a control flipped inside the FIRST appended paragraph REJECTED, and the pre-round blob is a byte PREFIX at 1322142 bytes growing to 1329032; reader (b) counted 6 blank-line units matching the slice's 6 paragraphs IN ORDER. BUILTSTATE at `5e557a1c` is proved the same way: the C2 blob of `docs/roadmap/features/T5_F037.md` is a byte PREFIX of the C3 blob, 12982 growing to 15880, prefix plus slice equals the C3 blob exactly, the negative control is False, and over the C3 blob the lines starting `## Built State` and `**A6` are exactly one each. THE RECORD MOVED AS PREDICTED: registrations UNMOVED at 292 and all DISTINCT, `^Done: R-\d+ — ` UNMOVED at 43, `^Landed: R-` UNMOVED at 11, `^Gate: F\d+ R\d+ — ` 95 to 96, and the OPEN SET computed AS A SET UNMOVED at 251, with `Gate: F037 R25` occurring exactly once.

THE PACKAGE WAS VERIFIED BY THE REVIEWER ON DISK AND NOT READ OUT OF THE HANDBACK, which is the whole point of a closure package. `remedy-review-20260828-142213-READY_FOR_REVIEW.zip` exists at `/home/decodeux/Repos/remedy-history/zips` at 19342216 bytes, and its sha256 recomputed by the reviewer over the file is `c3755b73a6cbaf21cd0547ce590aafee244d4143ace6ca1833bc93b50c87ef26`, EQUAL to the figure the handback records and to the pipeline's own `final_sha256`. Read from `.review_zip_manifest.json` INSIDE the archive rather than from the build log: `package_status` is `READY_FOR_REVIEW`, `current_evidence.evidence_freshness.evidence_authoritative` is True, and `committed_review_subject` runs from base `9dde54956afbe5f432bfd429bf4ba0bb272f6d07` to head `5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e`, which is C3 exactly as ordered. The evidence job is `f037-closure`, its nine verification runs total 137 passed with every `selected` equal to its own `node_ids` length, every `OUTPUT_HASH` line True, and the packaging scan rejected no string while its red control read True. The integrity gate — run through `packages.orchestration.integrity_gate` because the `remedy` CLI is denied in this session — answered `passed=True` with `fail_count=0` across all five checks, which is closure precondition 3.

ONE READING IS RECORDED BECAUSE IT CONTRADICTS AN OPEN FINDING'S PREDICTION, and a verdict that only records agreements is not a measurement. The archive holds 3465 entries and ZERO of them lie under `.remedy-wt`, while finding `R-0403` describes `scripts/make_review_zip.sh` packaging that directory at roughly half of every zip. Nothing is concluded about `R-0403`'s status from one observation and no resolution is authored here — the symptom is simply ABSENT at this commit, and the fact is recorded so a later session inherits the measurement rather than the assumption.

THE ROUND'S ONE SUBSTANTIVE DEVIATION IS CORRECT AND WAS CHECKED. The block ordered the package MOVED to the archive directory, and the worker reported the move as a no-op because `make_review_zip.sh` writes to `REVIEW_PACKAGE_DIR`, which already IS that directory — so the package was born at its archived path. The reviewer confirmed the file is really there rather than accepting the explanation, which is the only thing that distinguishes a correct no-op from an omitted step. The block's own order was the avoidable defect, not the worker's handling of it.

RE-RUN BY THE REVIEWER, primary checkout, ONE pytest process at a time, each exit 0: `tests/orchestration/test_test_runner.py` with `tests/docs/` 347 passed — the docs-round gate this round's `docs/roadmap/**` path requires — and the canary `tests/cli/test_golden_path.py` 42 passed. THE STRUCTURE IS CLEAN: six single-parent commits with insertions 490, 416, 21, 12, 49 and 305, each under 500 and each equal to the corresponding cell of the handback's `## Commits` table; the path residue is EMPTY IN BOTH DIRECTIONS; `git diff --stat` restricted to `apps/`, to `packages/` and to `tests/` prints NOTHING in all three; the transport-marker sweep is 0 in all three real targets against the block blob as its non-zero control; the build-output glob sweep `R-0677` binds totals 0; `git ls-files .remedy-wt` is 0; and `gh pr list --state open` is `[]`.
<<<END GATER26

<<<SLICE CLOSUREEDITS
[P1] docs/roadmap/STATUS.md · REWRITE · TO contains FROM: false · FROM occurs 1x
[P1-FROM]
- [~] F037 — Rendered diff viewer
[P1-TO]
- [x] F037 — Rendered diff viewer (T001–T003 complete; accepted 2026-08-28 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f037-closure · package remedy-review-20260828-142213-READY_FOR_REVIEW.zip · SHA-256 c3755b73a6cbaf21cd0547ce590aafee244d4143ace6ca1833bc93b50c87ef26 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e)
[P2] README.md · REWRITE · TO contains FROM: false · FROM occurs 1x
[P2-FROM]
59 of 255 registered items accepted. Next: F037 (Rendered diff viewer).
[P2-TO]
60 of 255 registered items accepted. Next: F033 (Hunk-level diff approval).
[P3] README.md · REWRITE · TO contains FROM: false · FROM occurs 1x
[P3-FROM]
| 5 | Operator Cockpit | 7 | 29 |
[P3-TO]
| 5 | Operator Cockpit | 8 | 29 |
[P4] README.md · APPEND · TO contains FROM: true · FROM occurs 1x
[P4-FROM]
own outcome and downside under the answer it belongs to).
[P4-TO]
own outcome and downside under the answer it belongs to).
F037 rendered diff viewer (a unified diff parsed server-side into structured
JSON — files, hunks, lines and intraline spans — served per job and per task run,
and rendered in the client with a file sidebar, hunk collapse beyond a size
threshold and virtual scrolling past two thousand rows; syntax highlighting is
modelled and deliberately not wired, per this feature's amendment A6).
<<<END CLOSUREEDITS

## Constraints

1. Apply every slice and every pair byte for byte. A slice you believe is wrong
   is applied as written and the problem is declared in the handback.
2. The change set above is exhaustive. `apps/`, `packages/` and `tests/` are
   untouched by every commit.
3. `.agent/plan.md` is rewritten at C1, before the record commit.
4. You author no `Done:`, `Gate:` or `Landed:` paragraph of your own. GATER26 is
   the only thing entering `.agent/live_review.md`.
5. THE FOUR PAIRS AND THE HANDBACK LAND IN ONE COMMIT, C3. The R-0154 ledger pin
   is that README and STATUS may never disagree in any committed state, and
   `tests/docs/` enforces it — the reviewer measured the partial edit as 2 failed
   and 293 passed, and the complete edit as 295 passed.
6. C3 IS THE LAST COMMIT ON THIS BRANCH (Rule A4). Nothing follows it. If the
   closure gate raises a candidate, a `.agent/candidates.md`-ONLY commit after C3
   is the one permitted successor (DECISION amend0827 D2) and is declared as such.
7. CREATE THE PR; DO NOT MERGE IT, and do not merge any other PR. Never
   force-push, never rewrite history, never work on `main`.
8. `git status --porcelain` is 0 at every commit boundary.
9. This session's shell guard rejects some command FORMS — shell loops, command
   substitution, indexed expansions, inline environment assignments, and brace
   literals containing quotes. Re-express through `python3 - <<'PY'` and pass
   `env=` to `subprocess.run`. A rejected form never justifies weakening a gate;
   report every re-expression in the handback.

## Done when — the gates

Run every gate and record its real exit code and real output. G1 through G7 run
at or before C3 and strictly before the PR is created, so the handback can quote
them.

G1 HYGIENE. `.agent/STOP` read from disk and reported ABSENT before C0a and again
before C3. `git rev-parse HEAD` before C0a equals the BASE `6a32be79`.
`git branch --show-current` is `feature/f037-rendered-diff-viewer`.
`git status --porcelain | wc -l` is 0 after each of C0a, C0b, C1, C2 and C3.

G2 TRANSPORT. Report the sha256 of the committed `.agent/authored/f037-r27.md`
blob and of the reviewer's own original at `.remedy-wt/f037-r27-block.md`, and
assert they are EQUAL; that file existed before you did, so this covers the
emission. Then report that `git rev-parse` of `HEAD:.agent/authored/f037-r27.md`
and of `HEAD:.agent/last_block.md` at C0b name ONE blob, and give that blob id.

G3 THE PLAN AT C1. PLANF037R27, re-extracted from the COMMITTED C0a blob, is
BYTE EQUAL to `.agent/plan.md` at C1 including its trailing newline. Report
`wc -l`, strictly under 50, and the counts of lines exactly `## Goal` and exactly
`## Next Steps`, each 1.

G4 THE RECORD AT C2, both readers. (a) The `6a32be79` blob of
`.agent/live_review.md`, plus a newline, plus GATER26, equals the C2 blob — with
a NEGATIVE CONTROL flipping one byte inside the FIRST appended paragraph, which
must be REJECTED. (b) Split the C2 blob on blank lines; let N be the number of
paragraphs your own script COUNTS in the slice, and compare the LAST N units
against them IN ORDER. Report N as measured, and report that the pre-round blob
is a byte PREFIX with both byte lengths.

G5 THE LEDGER. Over the C2 blob, base figures RE-MEASURED at `6a32be79`:
`^- R-\d+ — ` 292 and UNMOVED, all DISTINCT; `^Done: R-\d+ — ` 43 and UNMOVED;
`^Landed: R-` 11 and UNMOVED; `^Gate: F\d+ R\d+ — ` 96, rising by exactly ONE;
the OPEN SET computed AS A SET 251 and UNMOVED. Report that `Gate: F037 R26`
occurs exactly once, and that `R-0714` is present as a registration with NO
`Done:` line — the documented Medium risk F037 closes with.

G6 THE CLOSURE EDITS AT C3. For each of the four pairs report, from the C3 blob
of its file: the FROM string's occurrence count, which must be 0 for P1, P2 and
P3 because each is a REWRITE, and exactly 1 for P4 because it is APPEND-shaped
and its TO contains it; and the TO string's occurrence count, which must be
exactly 1 for all four. Then prove the STATUS line landed byte-identically:
extract `[P1-TO]`'s text from the COMMITTED C0a blob and assert it is present in
`docs/roadmap/STATUS.md` at C3 as a whole line — this is the grep proof the
closure protocol's step 5 requires of reviewer-authored applied text. Report that
`docs/roadmap/STATUS.md` at C3 contains exactly 60 lines matching `^- \[x\] F\d{3} — `
and ZERO lines matching `^- \[~\]`.

G7 THE CLOSURE PRECONDITIONS, re-confirmed at C3, ONE pytest process at a time.
`python3 -m pytest tests/docs/ -q` — the reviewer measured 295 passed with all
four edits applied, against 2 failed and 293 passed with the README left
untouched, so this gate demonstrably bites. `python3 -m pytest -n auto -q` from
the repository root, output captured IN MEMORY, reporting exit code, wall time
and the FULL `FAILED` list — this is precondition 2's confirmation run and the
second of the feature's two full-suite runs; the reviewer measured 18119 passed
and 20 skipped at exit 0 at `38966bf3`, and R25 measured one serial-pass flake,
so report what you get and attribute any `FAILED` id by a serial re-run rather
than re-running the suite until it is green. Then the integrity check through
`from packages.orchestration.integrity_gate import run_integrity_checks`,
reporting `.passed`, `.fail_count` and the five check statuses.

G8 STRUCTURE AND THE PR. `git diff --name-only 6a32be79..<C3>` equals the change
set above, with the RESIDUE reported EMPTY IN BOTH DIRECTIONS, each printed.
`git diff --stat 6a32be79..<C3>` restricted to `apps/`, to `packages/` and to
`tests/` prints nothing in all three, and restricted to
`docs/roadmap/features/T5_F037.md` also prints nothing. Every commit from C0a
through C3 is single-parent; report each one's insertion count from
`git diff --numstat`, assert each is under 500, and report those same numbers in
the handback's `## Commits` table so the two readings agree cell by cell.
`git grep -c` for `^<<<SLICE ` and for `^<<<END ` is 0 in `.agent/plan.md`, in
`.agent/live_review.md`, in `docs/roadmap/STATUS.md` and in `README.md`, against
the non-zero control of `.agent/authored/f037-r27.md`; also report that no line
beginning `[P1`, `[P2`, `[P3` or `[P4` reached `README.md` or
`docs/roadmap/STATUS.md`. `git ls-files .remedy-wt | wc -l` is 0. Finally push
and report `git rev-parse HEAD` against `origin/feature/f037-rendered-diff-viewer`.

## The pull request

After C3 and the push, create the PR with `gh pr create` into `main`. Title:
`F037 — Rendered diff viewer`. The description carries, per the AGENTS.md Pull
Request Workflow and closure-protocol step 5: what changed and why; the key
decisions F037 D1 through D11 by name with a pointer to `.agent/decisions.md`;
how to review, naming the package and its SHA-256; the changed-files table for
`9dde5495..HEAD` restricted to `apps/`, `packages/` and `tests/`; the latest
verdict, which is the R26 PASS this round books plus this round's own result; the
open-findings count with `R-0714` named as the documented Medium risk; and the
runtime actuals, which are 27 rounds across 8 sessions with model and token cost
`not-measured` — write `not-measured` rather than an estimate. DO NOT MERGE IT.
Report the PR number and URL.

## Handback

Rewrite `.agent/handoff.md` INSIDE C3 per docs/agents/handback_template.md. It
has NO length cap. It carries: the Session section with the number and roster
above; the range `6a32be79..HEAD`; a per-commit `## Commits` table whose `+/-`
cells are G8's `git diff --numstat` readings; the External actions including the
push and the PR creation; a Verification section with ONE LINE PER GATE, G1
through G8; the Authored-text proofs including the STATUS grep proof; the
Deviations, including every re-expressed command form; the item-status table
covering every C and every G exactly once; the open-findings count; and a Next
section stating that F037 is CLOSED, that its PR awaits the next feature's Open
PR Gate, and that the A6 split-off scope remains an operator proposal. The PR
number cannot be known when C3 is written, so the handback says the PR is created
after C3 and does not name a number — report the number in your reply instead.

ANY COMMIT BEYOND THE ORDERED SEQUENCE gets its OWN `## Commits` row and its OWN
item-status row, and the Deviations section states its existence rather than
sitting beside a clause denying it. Where the sequence was followed exactly, say
that and nothing more. This is the fix clause `R-0675` binds on the next block
ordering a handback.
