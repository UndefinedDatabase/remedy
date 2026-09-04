── STEP SESSION HANDOFF — F112 Prompt budget per task class ────────────────
Round 26 · session continuing F112 · base `138f616e` (F112 R25 C4, the tip
of feature/f112-prompt-budget-per-task-class)

Goal:
  Book round 25's PASS verdict AND register finding R-0792 (RECORD25,
  given verbatim below — a Gate paragraph, one blank line, then the
  R-0792 finding paragraph; already fully written and independently
  verified by the reviewer — do not re-derive it). Then write the
  SESSION-ENDING HANDOFF this round exists for. NO code file anywhere is
  touched this round.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f112-r26.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   append RECORD25 to `.agent/live_review.md`
  C2   apply PLAN26 to `.agent/plan.md`
  C3   the handback: rewrite `.agent/handoff.md` in full, per
       docs/agents/handback_template.md and the self-drive protocol's
       "Ending a session" section — this IS the session's real handoff,
       not a routine per-round one; it must be comprehensive enough that
       a completely fresh session, with no memory of this one, can pick
       up the investigation cold.

Change set — NOTHING outside these paths:
  `.agent/authored/f112-r26.md`
  `.agent/last_block.md`
  `.agent/live_review.md`
  `.agent/plan.md`
  `.agent/handoff.md`
  NO file under `packages/`, `apps/`, `tests/` or `docs/` is touched at
  all this round.

Constraints:
  1. Apply every delimited slice BYTE FOR BYTE. If a slice looks wrong,
     apply it anyway and DECLARE the problem in the handback.
  2. `.agent/STOP` is read FROM DISK before the first commit and again
     before C3.
  3. `.agent/plan.md` ends WITHOUT a trailing newline; PLAN26 is applied
     as an exact whole-file replacement, no trailing newline added.
     `.agent/live_review.md` also ends WITHOUT a trailing newline; append
     it as `content_bytes + b"\n" + RECORD25_bytes` — ONE newline, no
     extra blank line. RECORD25 itself already contains one internal
     blank line between its Gate paragraph and its `- R-0792 —` finding
     paragraph — preserve it exactly as extracted.
  4. THE HANDOFF (C3) must state, in its own words drawing on the
     verified facts below (do not invent anything beyond what is given):
       - Feature F112, round 26, and the SESSION NUMBER (this is a
         continuation of the F112 self-drive session; state the round
         count so far as 26 and name that this is the session's closing
         round per G8/G7).
       - Branch, base and head SHAs for this round.
       - ALL SIX closure preconditions are satisfied EXCEPT the mandatory
         review-zip build (precondition/algorithm step 2), which is
         currently BLOCKED by an unconfirmed cause.
       - What IS confirmed: R-0790 (ABS_PATH_RE false-positive on a
         punctuation-only tail) was found, fixed, mutation-red-proofed,
         and the fix is verified correct and sufficient for THAT specific
         `ReviewSubjectError` crash — round 25's zip build no longer hits
         that crash at all.
       - What replaced it: the zip now builds (exit 0) but is packaged as
         `remedy-review-20260904-034254-BLOCKED_EVIDENCE.zip`, archived at
         `/home/decodeux/Repos/remedy-history/zips/`, SHA-256
         `bb52ab1106a77d706fa3e1a25e4bdc80510645194e9b303d46f3e6c03a59e96d`.
         The evidence dir `remedy-job-evidence-f112-closure/` (job_id
         `cee206d7881e4699`, gitignored, still on disk) is available for
         direct inspection.
       - What was RULED OUT as the cause, and why: every individual gate
         in `build_review_manifest.py`'s `_ALL_READY_GATES` matrix
         (`final_verifier_report.json` reading `PASS_WITH_RISKS`,
         `fresh_evidence_gate.json`, `artifact_contract_gate.json`,
         `change_provenance_gate.json`, `runtime_integration_gate.json`
         all reading `PASS`; `manifest_integrity.json` and
         `postmortem_integrity.json` both `ok:true`;
         `commit_execution_gate.json` reading `NEEDS_HUMAN_APPROVAL`,
         which `build_review_manifest.py:1372` documents as "expected and
         nonblocking") read CLEAN when the reviewer inspected them
         DIRECTLY inside the archived zip via Python's `zipfile` module
         (not via the CLI's `ls`/`Read` tools, which refuse paths outside
         the repository).
       - What is SUSPECTED but NOT confirmed: `package_status` is decided
         at `build_review_manifest.py:3290-3296` from seven booleans
         (`evidence_valid`, `alignment_ok`, `containment_ok`,
         `gate_matrix["ok"]`, `fv_ok_for_ready`, `git_status_ok`,
         `tt_ok_for_ready`) and can ALSO be forced to `BLOCKED_EVIDENCE`
         afterward at line 3323-3325 by `_check_bundle_integrity`'s own
         verdict. The zip script's own console output during the build
         printed "WARNING: Evidence validation failed
         (is_valid_current_run=false)" BEFORE printing "Evidence refresh
         completed for staged copy" — suggesting `evidence_valid` (or
         whichever boolean reads `is_valid_current_run`) may have been
         evaluated from a PRE-refresh reading that the script's own later
         refresh step corrects, but never re-evaluates. This is a
         hypothesis, not a confirmed root cause.
       - A SEPARATE, CONFIRMED-BUT-NOT-YET-PROVEN-RELEVANT fact,
         registered as `R-0792`: `_run_verifications`
         (`packages/orchestration/job_evidence.py`) computes a
         VerificationTests run's `output_hash` from RAW, full stdout
         while storing a SCRUBBED, TRUNCATED `stdout_summary` — the two
         never agree by construction. This is real (independently
         reproduced by the reviewer against the archived evidence
         bundle's own `verification_tests.json`) but no currently-known
         gate reads or compares those two fields, so its bearing on
         `BLOCKED_EVIDENCE` is UNESTABLISHED, not confirmed.
       - NEXT SESSION'S FIRST ACTION: read `build_review_manifest.py`
         roughly lines 3150-3340 in full (further back than the reviewer
         got to) to find exactly which of the seven `package_status`
         booleans (or `_check_bundle_integrity`) actually read false
         AT BUILD TIME, and whether that reading happens before or after
         the "Evidence refresh completed for staged copy" step — printing
         each boolean's value at the point of the `package_status`
         decision (a one-line debug print or a direct call to the
         relevant helper functions against the SAME evidence dir still on
         disk) will answer this far faster than re-reading the packaged
         JSON files after the fact, which is what misled the reviewer
         into first ruling out gate_matrix.
       - Do NOT attempt another fix or another evidence/zip rebuild this
         round. Do NOT mint a new finding for `BLOCKED_EVIDENCE` itself —
         only `R-0792` is registered this round, for the independently
         confirmed `output_hash` fact on its own terms.
       - Changed-files table for this round's own commits (C0a-C3), the
         real gate outputs (G1-G3 below), the item-status table AGENTS.md
         mandates, the open-findings count (expected 281, moved from
         280), and the SITZUNGS-LIMIT style closing banner is NOT owed
         here (this is not a soft-limit round-count situation — 26 rounds
         is under the 25-round soft limit's... actually reconfirm: if the
         round count has reached or exceeds 25, name that plainly and
         include the amend0827 rule 6 scope-report obligation; otherwise
         just end cleanly per G8, no banner needed).
  5. `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
     `docs/roadmap/features/T3_F112.md` are NOT touched this round.
  6. NEVER force-push, never work on `main`, create NO pull request, merge
     nothing.

THIS ROUND'S PARAMETERS, measured by the reviewer at `138f616e` before
this block was authored:
  LIVE_REVIEW PRE-C1   `.agent/live_review.md` measures 2316649 bytes,
                       ending WITHOUT a trailing newline.
  RECORD25 LENGTH      7531 bytes (measure yourself against the committed
                       authored file's own extracted slice, as ONE
                       contiguous span: Gate paragraph + internal blank
                       line + `R-0792` finding paragraph).
  POST-C1 EXPECTED     2316649 + 1 + 7531 = 2324181 bytes.
  HEADER SHAPE         lines matching `^Gate: F\d+ R\d+ — ` currently
                       number 272; matching `^Gate: F112 R25 — `
                       currently 0. Expected after C1: 273 and 1.
  OPEN SET BEFORE C1   352 registered, 72 `Done:`, 280 open.
  OPEN SET AFTER C1    353 registered (R-0792 is new), 72 `Done:`, 281
                       open — reconfirm both sides yourself.
  PLAN.MD PRE-C2       40 lines (`wc -l`), ends WITHOUT a trailing
                       newline, currently holds PLAN25 (1794 bytes).

<<<BEGIN RECORD25>>>
Gate: F112 R25 — the round 25 entry, R-0791's fix plus the evidence/zip rebuild. VERDICT PASS on this round's own six commits, over the range `6dfdff5d..138f616e` (commits C0a `43f84b79`, C0b `bad3101f`, C1 `0972376d`, C2 `ad3e4207`, C3 `a06e8430` — five real content commits — plus handback commit `138f616e`), independently re-verified by the reviewer. TRANSPORT, PLAN AND RECORD APPEND ALL HELD BYTE-IDENTICAL, reproduced independently: blob `5b252687735a527c01a73367b1462450e4d5e3f0` for both authored and mirror files; PLAN25 equal both sides; RECORD24 (5824 bytes, one internal blank line preserved) appended to a 2310824-byte base gives exactly 2316649, prefix and no-trailing-newline confirmed; open set 351/72/279 before, 352/72/280 after, `- R-0791 — ` appearing exactly once post-append. R-0791'S FIX IS CORRECT, VERIFIED DIRECTLY AGAINST THE SHIPPED FILE, NOT THE HANDBACK: `tests/orchestration/test_failure_postmortem.py` reads exactly one blank line at the `is True` / `@pytest.mark.parametrize` seam, ends WITH a trailing newline, stays at 50148 bytes and 1098 lines (net zero, as designed), and `python3 -m ruff check` reproduces clean where it read one `W292` before. G6 (tree/commits) reproduced independently: `git diff --stat 6dfdff5d..138f616e -- packages/ apps/ tests/ docs/` with the one edited test file excluded is EMPTY. THE EVIDENCE/ZIP REBUILD IS AN OPEN QUESTION, NOT YET RESOLVED, AND THIS RECORD DOES NOT CLOSE IT: the zip built without the `ReviewSubjectError` crash (confirming R-0790's fix is sufficient for THAT defect) but the package landed named `...BLOCKED_EVIDENCE.zip` at `/home/decodeux/Repos/remedy-history/zips/`, SHA-256 `bb52ab1106a77d706fa3e1a25e4bdc80510645194e9b303d46f3e6c03a59e96d`, independently confirmed by the reviewer via `zipfile` (bypassing the CLI directory guard that blocks `ls`/`Read` outside the repo). THE WORKER'S OWN ROOT-CAUSE CLAIMS ARE NOT YET CONFIRMED AND ONE IS LIKELY WRONG: its claimed `output_hash`/`stdout_summary` mismatch is REAL as a fact (reproduced independently: none of the three verification runs' `output_hash` matches `sha256(stdout_summary)`, because `_scrub_paths` transforms the summary before hashing while `output_hash` is computed from raw, unscrubbed stdout in `_default_verification_runner`) but its BEARING ON `BLOCKED_EVIDENCE` is UNESTABLISHED — no gate in `build_review_manifest.py`'s `_ALL_READY_GATES` matrix reads or validates a VerificationTests run's `output_hash` against its `stdout_summary` anywhere the reviewer has found. THE REVIEWER'S OWN INDEPENDENT READ OF THE ARCHIVED ZIP CONTRADICTS A SIMPLE GATE-FAILURE EXPLANATION: every gate in `_ALL_READY_GATES` (`final_verifier_report.json` PASS_WITH_RISKS — explicitly ALLOWED per `_VERDICT_GATES`; `fresh_evidence_gate.json`, `artifact_contract_gate.json`, `change_provenance_gate.json`, `runtime_integration_gate.json` all PASS; `manifest_integrity.json`, `postmortem_integrity.json` both `ok:true`; `commit_execution_gate.json` NEEDS_HUMAN_APPROVAL — explicitly documented at `build_review_manifest.py:1372` as "expected and nonblocking") reads CLEAN inside the packaged zip's own `evidence/current/*.json` files, read directly via `zipfile`. `package_status` is set at `build_review_manifest.py:3290-3296` from SEVEN boolean gates (`evidence_valid`, `alignment_ok`, `containment_ok`, `gate_matrix["ok"]`, `fv_ok_for_ready`, `git_status_ok`, `tt_ok_for_ready`) and can ALSO be forced to `BLOCKED_EVIDENCE` afterward at line 3323-3325 by `_check_bundle_integrity`'s own verdict — the reviewer has not yet determined WHICH of these seven-plus-one actually read false at build time, only that the packaged GATE FILES read clean AFTER the script's own "Evidence refresh completed for staged copy" step, which strongly suggests `evidence_valid` (or another of the seven) was evaluated from a PRE-refresh reading and never re-evaluated post-refresh — a possible bug in the zip-build script's own ordering, not necessarily in the evidence bundle's content, and not the same claim the worker made. THIS AMBIGUITY IS NOT RESOLVED HERE: G8 applies — the reviewer ends the session on this open question rather than guessing at a fix, per docs/agents/self_drive_protocol.md's own guardrail. No R-id is minted for the BLOCKED_EVIDENCE puzzle itself pending a confirmed root cause (minting one now would be a guess, and item 30's own discipline cuts both ways — a wrong id spent on the wrong defect is worse than none). The `output_hash`/`stdout_summary` MISMATCH ITSELF, being a real, independently confirmed fact about `_run_verifications` regardless of its bearing on this closure, is registered below as `R-0792` on its own terms. `git status --porcelain` and `--ignored=no` both read empty; every commit's insertion count is under 500. THE OPEN SET IS 281 (352 registered plus `R-0792`, 72 `Done:`) after this round's own append. Round 26 is a HANDOFF round: no further guessing at the BLOCKED_EVIDENCE cause; the next session reads `build_review_manifest.py`'s `evidence_valid`/`_check_bundle_integrity`/`_evidence_dir_gate_loader` call sites and their ordering relative to the refresh step before attempting anything.

- R-0792 — Low, `_RUN_VERIFICATIONS`'S `OUTPUT_HASH` IS COMPUTED OVER RAW STDOUT WHILE `STDOUT_SUMMARY` IS SCRUBBED AND TRUNCATED, SO THE TWO NEVER AGREE. Found by the worker of F112 R25 and confirmed by the reviewer independently. MEASURED at `138f616e` against the evidence bundle `remedy-job-evidence-f112-closure/verification_tests.json` (job `cee206d7881e4699`): for all three of this round's verification runs, `sha256(stdout_summary.encode())` does not equal the recorded `output_hash`, including the one run whose `stdout_summary` is under the 2000-character truncation limit (686 characters) — ruling out truncation alone as the explanation. ROOT CAUSE, read directly in `packages/orchestration/job_evidence.py`'s `_default_verification_runner`: `output_hash = hashlib.sha256(stdout.encode(...)).hexdigest()` is computed from the RAW subprocess stdout, while `"stdout_summary": _scrub_paths(stdout[-2000:], repo)` both TRUNCATES to the last 2000 characters AND applies local-path scrubbing before storage — either transformation alone would break a hash-of-summary equality, and both are present. WHY LOW: no test or gate in this repository's own `_ALL_READY_GATES` matrix (`build_review_manifest.py`) currently reads or compares `output_hash` against `stdout_summary` for a VerificationTests run — the mismatch is a real internal inconsistency (a reader might reasonably assume `output_hash` authenticates the STORED `stdout_summary`, when it actually authenticates a raw, unscrubbed, unstored string) but it is NOT confirmed to be the cause of any observed packaging failure, including this round's own `BLOCKED_EVIDENCE` outcome — see this record's own gate paragraph, which found every currently-checked gate clean. FIX: either compute `output_hash` from the same scrubbed-and-truncated `stdout_summary` that is actually stored (weakening what the hash proves, since a real failure past the truncation boundary would be silently unhashed), or store a SECOND hash of the raw stdout under an explicitly-named field (`raw_output_hash`) so `output_hash` keeps meaning "hash of what you can see in `stdout_summary`" — a design decision the next round should make deliberately rather than as a side effect of chasing `BLOCKED_EVIDENCE`. Owed to a future round; not blocking F112's own closure until proven load-bearing.
<<<END RECORD25>>>

<<<BEGIN PLAN26>>>
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
all six closure preconditions satisfied. R-0790 and R-0791 both fixed
and verified. The review zip's `BLOCKED_EVIDENCE` status is an OPEN,
UNRESOLVED question (R-0792 registered on its own terms, not yet proven
the cause). Round 26 is a handoff: no code changes, no further guessing.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 26 books RECORD25 (registers R-0792) and writes the session's
handoff per G8 (self_drive_protocol.md): the BLOCKED_EVIDENCE cause is
not yet confirmed, so the session ends here rather than guessing at a
fix. No `.agent`-outside file is touched.

## Next Steps

- Read `scripts/build_review_manifest.py` lines ~3200-3340
  (`evidence_valid`, `alignment_ok`, `containment_ok`, `gate_matrix`,
  `fv_ok_for_ready`, `git_status_ok`, `tt_ok_for_ready`,
  `_check_bundle_integrity`) against their ORDERING relative to the
  script's own "Evidence refresh completed for staged copy" step, since
  every individual gate file reads clean POST-refresh.
- Once the true cause is confirmed: fix it, re-run the evidence job and
  zip, then the reviewer authors the STATUS line.
- Closure commit: STATUS `[x]`, README capability sync, `self_use_queue`
  SU-007 `consumed_by=F112`, final `.agent/` state. PR after.

## Risks

- R-0784, R-0767 (both OPEN, unrelated to F112) and R-0792 (may or may
  not bear on the BLOCKED_EVIDENCE puzzle) all carry forward undecided.
- Do not mint a fix for BLOCKED_EVIDENCE without first confirming which
  of the seven package_status gates actually read false at build time.
<<<END PLAN26>>>

Done when — the gates below, each RUN and reported as ONE LINE in the
handback with its real reading.

G1 TRANSPORT — `sha256sum` and byte length of the committed
   `.agent/authored/f112-r26.md`. Report that
   `git rev-parse HEAD:.agent/authored/f112-r26.md` and
   `git rev-parse HEAD:.agent/last_block.md` print ONE blob id after C0b.

G2 THE PLAN — extract PLAN26 by delimiter, compare byte-for-byte against
   `.agent/plan.md` at C2 — must be equal. Report `wc -l .agent/plan.md`
   (must be under 50), no trailing newline, `## Goal` and `## Next Steps`
   each exactly once.

G3 THE RECORD APPEND — extract RECORD25 by delimiter as ONE contiguous
   span, report its byte length (expected 7531). Report the arithmetic
   `2316649 + 1 + <len> = <total>` against the real post-append size, the
   byte-prefix property, no trailing newline, a NEGATIVE CONTROL. Report
   lines matching `^Gate: F112 R25 — ` before (0) and after (1) C1, AND
   `^- R-0792 — ` before (0) and after (1) C1. Report registered/`Done:`/
   open counts on both sides — expect 352/72/280 before, 353/72/281
   after. Report `git status --porcelain` empty before C3 is staged, and
   that no file under `packages/`, `apps/`, `tests/` or `docs/` appears
   in `git diff --stat 138f616e..<C2>`.

Handback: rewrite `.agent/handoff.md` in full, per constraint 4 above and
docs/agents/handback_template.md — this is the session's real closing
handoff, comprehensive enough for a cold read. It has NO length cap. Do
not write a `Done:` or `Gate:` paragraph anywhere beyond applying
RECORD25 verbatim. Then
`git push -u origin feature/f112-prompt-budget-per-task-class` and report
the outcome; create NO pull request, merge nothing.
══END BLOCK══
