OUTCOME: pending
── STEP R3 — F051 CLOSURE (docs/roadmap/STATUS_closure_protocol.md v4) ──
Block id: f051-r3
Goal:        Close F051: persist the R2 verdict, run the closure
             protocol end to end, finish with the single final commit
             (STATUS [x] + README sync + final .agent state) and the
             updated, unmerged PR #165.
Bundle:      1 guard · 2 authored texts · 3 persist commit + docs gate ·
             4 preconditions · 5 evidence job · 6 READY zip ·
             7 evidence commit · 8 FINAL commit · 9 push + PR update ·
             10 handback
Change:      .agent/**, docs/roadmap/features/T1_F051.md (one-line
             Built State update, item 3 only), then EXACTLY
             docs/roadmap/STATUS.md + README.md + .agent/** in the
             final commit. The evidence dir in its own commit. Nothing
             else, no code.
Constraints: Follow docs/roadmap/STATUS_closure_protocol.md exactly —
             zip from a clean tree AFTER the content commits (the
             reviewed head = accepted HEAD), evidence-dir commit and
             final commit AFTER the READY zip. A failing zip build is a
             closure BLOCKER: record the raw error in the handoff and
             hand back — never close without the package. Any
             precondition failure: STOP, hand back.
Done when:   READY_FOR_REVIEW zip exists with recorded SHA-256, STATUS
             line applied with grep 1/0 + cmp proofs, README edits
             applied with grep proofs, docs gate + canary green after
             the final commit, PR #165 updated, NOT merged.
Handback:    Completion report + rewrite .agent/handoff.md (raw
             transcripts for every proof, provenance table for the four
             substituted placeholders, zip outcome recorded BEFORE
             handback).

AUTHORED-TEXT PROTOCOL (all four blocks below): bytes = the lines
strictly BETWEEN the BEGIN and END marker lines, joined with LF, plus
one final LF. Save to .agent/authored/<name>.md, verify sha256sum
against the BEGIN-marker hash BEFORE any use. Mismatch: rejoin
hard-wrapped lines with a single space and re-verify; if still
mismatched, STOP that item, record received bytes + computed hash in
the handoff, hand back. Never apply an unverified text.

1. Guard: record this block in .agent/last_block.md (id f051-r3,
   OUTCOME pending; note transport faults).

2. Save and verify the four authored texts:
   .agent/authored/f051-r3-1.md … f051-r3-4.md.
   Record the sha256sum lines verbatim.

3. Commit A — persist + Built State current (the content head):
   - .agent/live_review.md := full replace with f051-r3-1.md (cmp).
   - docs/roadmap/features/T1_F051.md: apply f051-r3-2.md — verify the
     FROM block occurs exactly once (grep the first FROM line -> 1),
     replace those exact lines with the TO lines. After: grep -c
     "integration gate PASS" in the file -> 1.
   - .agent/last_block.md guard from item 1.
   git add those + .agent/authored/f051-r3-*.md
   Commit message: chore(f051): persist R2 verdict (integration gate PASS); Built State current
   Then: python3 -m pytest tests/docs/ -q  (exit 0) and
   python3 -m pytest tests/cli/test_golden_path.py -q  (exit 0).
   On red: STOP, hand back.

4. Preconditions (protocol section 1) — raw outputs into the handoff:
   python3 -m apps.cli.grouped integrity check --json   (expect PASS)
   git status --porcelain                               (empty)
   git push && git rev-list --left-right --count @{u}...HEAD  (0 0)

5. Evidence job (protocol step 1): fresh bundle via
   packages.orchestration.job_evidence.create_manual_completion_bundle(
   review_feature_id="f051", …), base_commit =
   894375e40f2d88c3d2cd2859073423faa2b17120 (FULL 40 chars).
   verification_runs = 4 REAL runs, each executed now, exit codes
   recorded: tests/orchestration/test_escalation.py -q (66) ·
   tests/cli/test_open_decisions_view.py -q (26) ·
   tests/cli/test_golden_path.py -q (42) · tests/docs/ -q (292).
   Producer pitfalls (F050/F252 lessons): pre-truncate each
   stdout_summary to the producer's last-2000-char window and leave
   output_hash EMPTY so the producer derives it from exactly the
   stored bytes; valid VerificationTests totals; `selected` ==
   len(node_ids). Record the job id.

6. Review zip (protocol step 2) — AFTER commit A is pushed, tree
   clean, and BEFORE any evidence commit:
   bash scripts/make_review_zip.sh --evidence-dir <path-to-evidence-dir>
   Verify: PACKAGE_STATUS READY_FOR_REVIEW, manifest
   committed_review_subject spans base..HEAD with head = commit A's
   sha, base_is_ancestor true, ZipFile.testzip() -> None.
   Record: package filename, SHA-256 (script output AND independent
   sha256sum), accepted HEAD = manifest head_commit.
   Failure = closure blocker: record raw error, hand back.

7. Commit B — evidence dir only, AFTER the READY zip exists
   (`git add -f` past .gitignore .data/):
   Commit message: chore(f051): commit closure evidence (after READY zip)

8. Commit C — FINAL, touches EXACTLY docs/roadmap/STATUS.md, README.md,
   .agent/** (R-0154 / protocol step 5):
   - STATUS: re-verify f051-r3-3.md's sha256 immediately before use;
     substitute its four placeholders — <JOB_ID> from item 5,
     <ZIP_FILENAME> and <ZIP_SHA256> from item 6's script output,
     <HEAD_SHA> = the manifest's committed_review_subject.head_commit —
     each placeholder occurs exactly once; replace the line
     "- [~] F051 — Escalate instead of block (unattended)" with the
     substituted line. Proofs: new line grep -cF 1, old grep -cF 0,
     `grep -F <line> STATUS.md | cmp - <substituted template>` exit 0,
     provenance table (placeholder -> value -> source) in the handoff.
   - README: apply f051-r3-4.md — three ordered edits, each FROM
     verified grep -cF 1 before, 0 after; each TO grep -cF 1 after.
   - .agent: handoff rewrite + last_block OUTCOME executed.
   Commit message: chore(f051): close F051 — STATUS [x] + README sync
   Post-commit: python3 -m pytest tests/docs/ -q (exit 0) ·
   python3 -m pytest tests/cli/test_golden_path.py -q (exit 0) ·
   grep -c '^- \[x\]' docs/roadmap/STATUS.md -> 27.

9. git push. Update PR #165 body: what/why, key decisions (derived
   queue branch, awaiting derived not stored, td: resolve branch,
   --unattended flag), changed-files table, latest verdict "R2 PASS —
   INTEGRATION GATE PASS; R3 closure", open findings: 2 documented
   risks (R-0155 Low, R-0156 Medium), runtime actuals: 3 rounds
   (R1 LARGE / R2 / R3) on 2026-07-30, models as configured,
   tokens/cost not-measured. Do NOT merge — PR #165 merges at the
   next feature's start via the Open PR Gate.

10. Hand back with the completion report.

TRANSPORT NOTES (worker, f051-R3):
(1) f051-r3-3 arrived HARD-WRAPPED: the one-line STATUS template was
    split across three lines (after "live review" and after
    "accepted HEAD"). Rejoining the fragments with a single space
    reproduced the authored bytes exactly — sha256
    7e90d44b22e537ba6bc84c186e729ca0ab27037bb1567535b2048516a70511be
    verified BEFORE any use. Same recoverable wrap class as f050-r3-2,
    r0154-r1-1 and the R2 step-13 command. The template is ONE line and
    all four <PLACEHOLDERS> survived intact.
(2) f051-r3-1, -2 and -4 arrived CLEAN; all three hashes matched on
    first computation.
(3) Cosmetic wraps in the block's own instruction text (item-3 and
    item-8 commit-message lines, the item-6 script invocation) are
    recorded above rejoined. No authored bytes affected.
