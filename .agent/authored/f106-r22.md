── STEP CLOSURE-EVIDENCEZIP/1 — F106 ────────────────────────────────────
Goal: Book the reviewer's own pending verdicts for rounds 18-21 into the
permanent record (amend0827-process-diet rule 1 — a pushed handback is a
durable carrier, booked in the first commit of the round that is
happening anyway), then execute STATUS_closure_protocol.md Algorithm
steps 1 (evidence job) and 2 (review zip). This round does NOT close the
feature: no STATUS `[x]` edit, no README sync, no `consumed_by` edit, no
PR.

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r22.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 22 (PLAN22 below)
  C2  — append FOUR paragraphs to .agent/live_review.md, IN ORDER:
        GATE18, GATE19, GATE20, GATE21
  C3  — (after evidence+zip build, below) rewrite .agent/handoff.md for
        round 22 handback

Change: exactly the .agent/** paths of C0a/C0b, .agent/plan.md,
.agent/live_review.md and .agent/handoff.md. No path under packages/,
apps/, tests/, docs/, scripts/. Neither the evidence directory nor the
review zip is a tracked path — they must NOT be committed
(STATUS_closure_protocol.md, "Evidence dir is not committed").

Constraints:
1. C0a/C0b verbatim single-.agent-state-file saves (shutil.copyfile, never
   cp, never retyped), exempt from the 500-line cap.
2. C1 — PLAN22 is a REWRITE of .agent/plan.md, applied via shutil.copyfile
   from .remedy-wt/f106-r22-plan.md (36 lines, < 50, holds `## Goal`/
   `## Next Steps`, sha256
   28a4456454e32457dddcae639be95408889c1537d4108519ada7b7f27b81ab04, 1676
   bytes).
3. C2 — a FOUR-PARAGRAPH append to .agent/live_review.md, never retyped,
   IN ORDER, each via shutil.copyfile: GATE18
   (.remedy-wt/f106-r22-gate18.txt, 2052 bytes, sha256
   bf3f34591e6840972be8edb5b95417c49750a6399ec4650d090517b78787dac8),
   GATE19 (.remedy-wt/f106-r22-gate19.txt, 2340 bytes, sha256
   a0f26a42093482e058d4df25762cb8d7a3c462b7e0d6773dbcc4884d5b63d06c),
   GATE20 (.remedy-wt/f106-r22-gate20.txt, 2597 bytes, sha256
   17a4dff4cb32400ae27934217cadba8c81231ed8e7f243bcc5a84795eada50e8),
   GATE21 (.remedy-wt/f106-r22-gate21.txt, 2198 bytes, sha256
   a42b8d47bd2fdf3110d62d52b077740ee9325ef7ef046c04619a99b56a178f11).
   Re-measure the file's own base length before appending: at this
   round's base the file is 1904795 bytes and does NOT end in a trailing
   newline, so every separator is "\n\n". Expected total: base + 2 + 2052
   + 2 + 2340 + 2 + 2597 + 2 + 2198 = 1913990 bytes, sha256
   e7b2107082db04079cef15976d7bb623da884876402732e3e3e7cc5b9e6d55fd. (If
   your own measured total differs from this arithmetic, recompute the sum
   yourself rather than trusting either number blindly, and state which
   number you land on and why.)
4. AFTER C2 is committed and pushed, build the evidence bundle and review
   zip from that clean, pushed tree (mirrors the F258 R11 precedent at
   `.agent/authored/f258-r11.md`). Do NOT invent an evidence script: run
   the ALREADY-AUTHORED, reviewer-verified script verbatim from
   .remedy-wt/f106_evidence.py (136 lines, sha256
   e5eb096e48a91da00196dc9484cb4e45cb8986fb385c44c367a3920801de11c4 —
   verify this yourself before running it; if it differs, STOP and report
   rather than proceeding). It builds
   `.remedy-wt/f106_closure_evidence/remedy-job-evidence-f106-closure` via
   `packages.orchestration.job_evidence.create_manual_completion_bundle`
   (`job_id="f106-closure"`, `base_commit=811c2d7e96b4719b8c76e6fc59ec6d926847a026`,
   8 scoped verification suites, 244 tests total, all passing at this
   script's own last dry run). Confirm your own run reproduces
   `total_passed=244` and `verdict="PASS_WITH_RISKS"` (R-0761 is the OPEN
   Medium risk this reflects) — if either differs, STOP and report rather
   than proceeding to the zip. Then build the zip:
   `bash scripts/make_review_zip.sh --evidence-dir
   .remedy-wt/f106_closure_evidence/remedy-job-evidence-f106-closure`,
   wrapped `bash -c '...; echo REAL_EXIT=$?'` to capture the real exit
   code. Confirm `PACKAGE_STATUS=READY_FOR_REVIEW`,
   `EVIDENCE_AUTHORITATIVE=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, and that
   the manifest's `committed_review_subject.head_commit` equals this
   round's own HEAD at C2 (`git rev-parse HEAD` right after the C2 push,
   before this build). Record the printed `ZIP_PATH` and its `final_sha256`
   (also printed by the script's own JSON summary line) — these are the
   package filename and SHA-256 the next round's STATUS line needs.
5. C3 — .agent/handoff.md rewrite per AGENTS.md's handoff contract: state,
   SESSION 6, branch, commit SHAs, a changed-files table, this round's
   real gates (below), the evidence job's real result (`job_id`,
   `total_passed`, `verdict`, `authority_count`, `commit_count`), the
   review zip's real result (filename, SHA-256, archived path, accepted
   HEAD), open-findings count (322 registered, 60 resolved, 21 decisions
   — unmoved this round, no new id), and next expected action: round 23
   authors the STATUS line and the closure commit (STATUS.md, README.md,
   `scripts/self_use_queue.json` SU-003 `consumed_by=F106`, final
   `.agent/` state, plus the DECISION F106 D2 candidates.md-only
   follow-up commit), then the PR.

Done when (run every command yourself; record REAL exit codes and REAL
values, never the word "green" or an assumed number):
G1 TRANSPORT — .agent/authored/f106-r22.md and .agent/last_block.md both
   sha256-equal to this block as saved (single digest comparison).
G2 THE PLAN — .agent/plan.md sha256
   28a4456454e32457dddcae639be95408889c1537d4108519ada7b7f27b81ab04, 36
   lines (`wc -l`), holds `## Goal` and `## Next Steps`.
G3 THE LEDGER APPEND — .agent/live_review.md's real post-commit bytes and
   sha256 (compute and report; constraint 3 gives the expected arithmetic
   but you verify it, not assume it); the file's last FOUR `\n\n`-delimited
   units, in order, are byte-equal to GATE18, GATE19, GATE20 and GATE21
   respectively; negative control — flip one byte inside a SCRATCH copy of
   GATE18 (the FIRST appended paragraph) and confirm the flipped copy no
   longer byte-equals the file's own fourth-from-last unit (never mutate
   the tracked file itself).
G4 THE LEDGER COUNTS — over .agent/live_review.md at HEAD (after C2):
   `grep -cE '^- R-[0-9]{4} — '` reads 322 (unmoved — no new finding id
   this round); `grep -cE '^Done: R-[0-9]{4} — '` reads 60 (unmoved);
   `grep -cE '^DECISION F[0-9]+ D[0-9]+ — '` reads 21 (unmoved); `grep -oE
   'Gate: F106 R[0-9]+ — ' | sort -u | wc -l` reads 21 distinct round
   numbers (up from 17 before this round's C2 — GATE18 through GATE21
   added).
G5 THE EVIDENCE BUNDLE — the script's own printed JSON result:
   `job_id="f106-closure"`, `total_passed=244`, `verdict="PASS_WITH_RISKS"`,
   `manual_completion=true`; all 8 `verification_runs` entries have
   `len(node_ids) == selected` and `failed == 0`; the `_unsafe_text` scan
   over every node id and command rejects nothing (report the real
   rejected count, expect 0).
G6 THE REVIEW ZIP — `PACKAGE_STATUS=READY_FOR_REVIEW`,
   `EVIDENCE_AUTHORITATIVE=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS`; the
   manifest's `committed_review_subject.head_commit` equals the HEAD you
   recorded right after C2's push; report the real zip filename and
   `final_sha256`.
G7 THE TREE — `git status --porcelain` empty (the evidence dir and zip
   are both outside the tracked tree — confirm with
   `git status --porcelain` showing nothing for either); every commit's
   insertions under 500 (C0a/C0b exempt as verbatim `.agent/**`
   state-file saves); canary (`pytest tests/cli/test_golden_path.py -q`)
   REAL exit 0; HEAD (at C3, after the handoff commit) pushed and equal
   to `origin/feature/f106-session-resume`.

Handback: completion report + rewrite .agent/handoff.md (C3 above). State
the real numbers for every gate above, not the word "green". Name every
deviation, however small.
─────────────────────────────────────────────────────────────────────────
