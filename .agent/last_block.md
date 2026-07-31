Round f053-r6 — CLOSURE per docs/roadmap/STATUS_closure_protocol.md (v4);
that file wins over the block summary. Never merge anything this round.
f053-r6-5 is ONE ~200-char line that arrives hard-wrapped: rejoin the
fragments with a single space, re-hash, use only after the hash matches
(known recoverable class, 4th instance). f053-r6-6's EDIT-1 TO-line may
wrap the same way — same recovery.

STEP 1 — COMMIT A: in .agent/live_review.md replace the R5 "In progress."
Steps bullet with f053-r6-1, append f053-r6-2 to "## Verdicts" after the
R4 entry, replace the block from "- Open: R-0162 (process, Low," through
"- Next free ID: R-0163." with f053-r6-3; append f053-r6-4 at the END of
docs/roadmap/features/T1_F053.md. cmp proofs for all four. Record the
commit's FULL sha — it is the expected accepted HEAD. Touches
docs/roadmap/** → docs gate now: tests/docs 293, exit 0.

STEP 2 — PRECONDITIONS (abort closure on any failure):
integrity check --json → PASS, fail_count 0 (raw JSON summary recorded);
git status --porcelain empty; push; git rev-list --left-right --count
@{u}...HEAD → "0 0". R-0160 is a documented Low risk, not a blocker.

STEP 3 — EVIDENCE JOB: create_manual_completion_bundle(
review_feature_id="f053", ...), fresh job id, base commit FULL sha
15105dbe070c722f0e7cd44aff065b6fed6e1635, head = commit A. Four REAL
verification runs executed now with exit codes: test_run_report 68,
test_run_report_hook 22, test_job_report 30, canary 42. Producer
pitfalls per the protocol's step-1 list, incl. (c) run_id ^vr-\d{4,}$;
node_ids via --collect-only with len(node_ids) == selected; test_files
are FILES; output_hash = sha256 of the EXACT stored stdout_summary
bytes; full-length base_commit; full closed-schema gate set.

STEP 4 — READY ZIP from the clean tree, BEFORE any evidence commit:
bash scripts/make_review_zip.sh --evidence-dir <path> (or --job-id).
Requires PACKAGE_STATUS=READY_FOR_REVIEW, EVIDENCE_AUTHORITATIVE=true,
validation_errors empty, committed_review_subject spanning
15105dbe070c722f0e7cd44aff065b6fed6e1635..<commit A>, base_is_ancestor
true, ZipFile.testzip() → None. Record filename + SHA-256 (script JSON
AND independent sha256sum). accepted HEAD := manifest
committed_review_subject.head_commit, must equal commit A. A failing zip
build is a closure BLOCKER: record the raw error and STOP.

STEP 5 — EVIDENCE COMMIT (only after the READY zip exists): git add -f
the evidence export dir.

STEP 6 — FINAL COMMIT = exactly STATUS.md + README.md + .agent/.
Substitute into a COPY of f053-r6-5 (each placeholder exactly once,
grep -c 1→0 each, original untouched): <JOB_ID>, <ZIP_FILENAME>,
<ZIP_SHA256>, <HEAD_SHA> = manifest head_commit. Replace the unique
STATUS.md line "- [~] F053 — Final & interim report" with it (old 1→0,
new 1; cmp of the grepped line against the substituted copy → 0). Apply
the three README edits from f053-r6-6 exactly (each FROM 1→0, each TO
present). Provenance table per substituted value in the handback.
Rewrite .agent/handoff.md + flip OUTCOME to executed. Post-edit gates:
tests/docs 293 exit 0 (count pin 29==29), canary 42;
grep -c '^- \[x\]' docs/roadmap/STATUS.md → 29.

STEP 7 — PR, NOT merged: gh pr create --base main --title "F053 — Final
& interim report (T001–T002)", body per AGENTS.md: what/why, DECISIONS
D2 + D3, changed-files table, verdicts R1–R5 (R3+R4 FAIL honestly named,
gate PASS at R5), open findings 1 (R-0160, Low, routed to paydown),
runtime actuals (observed; not-measured beats a guess), evidence job +
package + SHA-256. Report the PR number. Then await the reviewer.
Authored texts f053-r6-{1..6} (sha256 verified before use, saved
verbatim under .agent/authored/, applied by copy).
OUTCOME: pending
