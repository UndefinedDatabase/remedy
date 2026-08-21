# Handback — F255 Teacher role · R20 (closure evidence, REPAIRED)

R19's SEVEN commits are all correct and none was redone; R19's GOAL was unmet
because the reviewer's EVIDENCESCRIPT slice was defective. R20 registers that as
R-0611 at C2, records the R19 verdict at C3, and rebuilds both closure artifacts.
R-0607, R-0608, R-0609 and R-0611 remain OPEN. R20 ITSELF IS THE ROUND WHOSE
VERDICT IS NOT ON DISK. No pull request is open (`gh pr list --state open` → `[]`).

| Item | Status | Reason |
|------|--------|--------|
| C0a `.agent/authored/f255-r20.md` | done | |
| C0b `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` | done | first substantive commit |
| C2 `.agent/live_review.md` (R-0611) | done | |
| C3 `.agent/live_review.md` (R19 verdict) | done | |
| C4 `.agent/handoff.md` | done | this file |

## Range
Review of b42cab39..c96f82c3 (C4 adds `.agent/handoff.md` on top).

## Commits
### 09eb818b chore(state): save the F255 R20 step block
| Path | +/- | Reason |
| `.agent/authored/f255-r20.md` | 401/0 | C0a, block saved byte-equal |
### 304b4002 chore(state): mirror the F255 R20 step block
| Path | +/- | Reason |
| `.agent/last_block.md` | 230/270 | C0b, same file mirrored (with `-B`: 401/441) |
### eaffcc07 chore(plan): advance the plan to F255 R20
| Path | +/- | Reason |
| `.agent/plan.md` | 18/16 | C1, PLAN255R20 verbatim, 43 lines |
### ec6dbcb8 docs(review): register finding R-0611
| Path | +/- | Reason |
| `.agent/live_review.md` | 2/0 | C2, FIND0611 appended |
### c96f82c3 docs(review): record the R19 verdict
| Path | +/- | Reason |
| `.agent/live_review.md` | 2/0 | C3, RECORDR19 appended |
### C4 — this handback
| Path | +/- | Reason |
| `.agent/handoff.md` | in the round report | R-0149: a handoff cannot table its own commit |

## External actions
- `git push origin feature/f255-teacher-role` after C3 → exit 0, `b42cab39..c96f82c3`;
  tree clean and branch pushed BEFORE the zip build. Pushed again after C4.
- EVIDENCE JOB `python3 .remedy-wt/.cache/r20_evidence.py` (cwd repo root) → exit 0.
  Dir did not pre-exist. Bundle `.remedy-wt/f255_closure_evidence/remedy-job-evidence-f255-closure`,
  27 entries, NOT committed. Summary: job_id `f255-closure`, head c96f82c3…7a08,
  total_passed 141, commit_count 136, authority_count 25, manual_completion true,
  T001/T002/T003 = 9/9/7, `verdict: PASS_WITH_RISKS`. `final_verifier_report.json`
  also reads `verdict: PASS_WITH_RISKS`; the string `READY` appears nowhere in it.
- REVIEW ZIP `bash scripts/make_review_zip.sh --evidence-dir <bundle>` → exit 0.
  package `remedy-review-20260821-051015-READY_FOR_REVIEW.zip`, SHA-256
  `f142a9935d2730c01a80d98a619d2b297899c144f29ad16fd5c01aa1f493fcc2`, PACKAGE_STATUS
  `READY_FOR_REVIEW`, 10646 members, EVIDENCE_AUTHORITATIVE true, ALIGNMENT PASS.
  Manifest `committed_review_subject`: base b35d350b84b1d371064a1f44e43f40da3ccfa540,
  head c96f82c3372520bfd0545c7ce640886479197a08 — that head IS the commit C3 created.
- `gh pr list --state open` → `[]`. No PR created; no CI run waited on.

## Verification
- G1 `.agent/STOP` ABSENT before C0a; branch correct; porcelain EMPTY after all 5 commits, pre-zip and here; one worktree.
- G2 block, `.agent/authored/f255-r20.md`, `.agent/last_block.md` all sha256 6d54e410…a25e, 31253 B, 401 L — all three EQUAL.
- G3 4 slices counted from the listing: PLAN255R20 69bfe9d8… 2435 B/43 L, FIND0611 053d0d93… 3246 B/1 L, RECORDR19 254af30f… 4339 B/1 L, EVIDENCESCRIPT2 f8acb4a1… 4200 B/109 L, newline-INCLUDED; `r20_evidence.py` byte-equals EVIDENCESCRIPT2.
- G4 plan.md at C1 byte-equals PLAN255R20 (69bfe9d8…, 2435 B, 43 L < 50), `## Goal` 1x, `## Next Steps` 1x, F255 present; C1 first after C0a/C0b.
- G5 C2/C3: prior blob a byte-exact PREFIX; remainders 3247 B and 4340 B, each == one LF + slice, next byte `-` / `G`; independent paragraph reader's LAST unit == the slice under BOTH newline conventions; one-byte mutation rejected by both readings.
- G6 b42cab39 186/4/182/0 · C2 187/4/183/0 · C3 187/4/183/0; R-0611 0x at base; `Gate: R20 — the R19 entry.` line-anchored 1x at C3 and LAST of 20 such headers, all distinct.
- G7 twelve captures SERIAL, all exit 0: 18/19/5/38/19/42 passed, 0 failed and 0 skipped throughout; each `--collect-only -q` id count EQUALS its suite's passed count; the vr0002 listing DOES carry a space-bearing id.
- G8 evidence job exit 0, 27 bundle entries, verdict PASS_WITH_RISKS — External actions.
- G9 zip exit 0 from a clean, pushed tree — External actions.
- G10 exit 0 / 160 passed (canary four) and exit 0 / 42 passed (golden path), serially in the primary checkout.
- G11 `run_integrity_checks()` passed=True, fail_count=0, all 5 checks `pass`: handler_import, live_review_verdict, plan_consistency, relevant_untracked, high_blockers_open.
- G12 range == Change list minus `.agent/handoff.md`, nothing on either side alone; STATUS.md and README.md absent; the 5 named paths present at base, absent from the range; every commit one parent; max insertions 401 < 500; 5 reflog `commit` entries at c96f82c3 against 5 commits made — equal; 0 amend/rebase/cherry and 0 reset entries in this round's window.
- G13 marker LINES 0 in plan.md at C1, live_review.md at C3, handoff.md at C4.

## Authored-text proofs
PLAN255R20, FIND0611 and RECORDR19 were extracted programmatically from the COMMITTED
`.agent/authored/f255-r20.md` by marker line and applied byte for byte; every
disk-to-disk comparison returned EQUAL (digests under G3–G5). EVIDENCESCRIPT2 was
saved and run UNEDITED. Nothing was retyped.

## Deviations & assumptions
None. The ordered sequence C0a, C0b, C1, C2, C3, evidence job, zip, C4 was followed
exactly, with no extra, dropped or reordered commit. Assumption, stated: the `+/-`
cells use plain `git diff --numstat`; C0b also reads 401/441 under break-rewrite
detection (`-B`), the form `git commit`'s own summary printed. Both are under 500.

## Next
FIRST: Phase 1 rule 1 — re-read `.agent/STOP` from disk.
SECOND: R21, THE CLOSURE COMMIT. The reviewer authors the STATUS `[x]` line from the
values THIS round reports (package, SHA-256, evidence job `f255-closure`, accepted
HEAD c96f82c3372520bfd0545c7ce640886479197a08); the worker applies it verbatim in the
SAME commit as the README capability sync (R-0154), writes any closure candidates to
`.agent/candidates.md`, and opens the pull request — NOT merged in its own session.

Fortschritt: ~97 % (T001 through T004 COMPLETE and REVIEWED · the
integration gate PASSED with 0 branch-only failures · evidence job
and review zip built at this round · only the STATUS line, the README
sync and the pull request remain) — Schätzung
