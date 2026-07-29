# Handback — F252 R4b (closure, corrected ordering) — CLOSED

## Range
Review of d9a146a..HEAD · feature/f252-standing-red-paydown · preconditions PASS ·
evidence job + READY zip · README + STATUS `[x]` in ONE final commit (R-0154) · PR open,
not merged.

## Commits
### d543d44 chore(f252): persist the R4 stop verdict + R-0154 resolution
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f252-r4b-1/2.md · live_review.md · plan.md · last_block.md | +236/-63 | authored texts sha256-verified, applied by copy; R4b block |
### 25eb5bd chore(f252): commit closure evidence (after READY zip)
| Path | +/- | Reason |
|---|---|---|
| .data/evidence_exports/d9a16173-…/ (83 files) | +new | the closure bundle, `git add -f` past `.gitignore:211 .data/` (F251 precedent); committed only after the READY zip existed (F147 lesson) |
### final commit chore(f252): close F252 — STATUS [x] + README sync
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md · README.md | +4/-4 | the authored line with its four placeholders substituted, plus the three ordered README edits — together, so the ledger pin never sees a disagreement |
| .agent/handoff.md · last_block.md | rewrite · +1/-1 | this handback; OUTCOME → executed |

## External actions
3 pushes to origin/feature/f252-standing-red-paydown; `make_review_zip.sh --evidence-dir
.data/evidence_exports/d9a16173-…` → READY_FOR_REVIEW; `gh pr create` right after the
final commit (number in the handback message). NOT merged. No worktree.

## Verification
- Preconditions `integrity check --json` → exit 0, `"passed": true, "fail_count": 0,
  "check_count": 5` (handler_import 312, live_review_verdict, plan_consistency 0,
  relevant_untracked 0/0, high_blockers none). Tree clean, branch synced.
- Evidence job **d9a16173-0283-40a1-957a-1ee9b7b39343** via
  `create_manual_completion_bundle(review_feature_id="f252", …)`, base 7baff1dd… → head
  d543d445…: PASS_WITH_RISKS, 46 authority files, 25 commits, 3 attested tasks, 334
  passed; gate matrix `ok: True`, `validate_manual_completion() == []`, candidate valid.
- Zip **remedy-review-20260729-153036-READY_FOR_REVIEW.zip**, SHA-256
  **7dfb5a511f2a4110997910e24d64ff09ea1d4c3ddf894623edf2569d6a58c6d8** (script output,
  `sha256sum` agrees): READY_FOR_REVIEW, ALIGNMENT=PASS, AUTHORITATIVE=true, 1588
  members, authoritative 46; manifest `committed_review_subject` 7baff1dd… → d543d445…;
  `testzip()` → None. **accepted HEAD = d543d445cd1f9ecb6d092e64fe670881bc6fff67**.
- Applied STATUS line, verbatim:
  `- [x] F252 — Standing-red paydown (154 ids, 13 classes) (R1–R3 complete; accepted 2026-07-29 · live review PASS — ACCEPTED · Evidence job d9a16173-0283-40a1-957a-1ee9b7b39343 · package remedy-review-20260729-153036-READY_FOR_REVIEW.zip · SHA-256 7dfb5a511f2a4110997910e24d64ff09ea1d4c3ddf894623edf2569d6a58c6d8 · accepted HEAD d543d445cd1f9ecb6d092e64fe670881bc6fff67)`
  `grep -cF` new = **1**, old `- [~] …` = **0**; `cmp` on-disk vs substituted template → 0.
- Pre-commit gate on these exact bytes: `pytest tests/docs/ -q` → 0, "292 passed";
  canary → 0, "42 passed". Post-commit re-run in the handback message.

## Authored-text proofs
f252-r4b-1 `f91bd529…`, f252-r4b-2 `d2d810d5…`: on-disk `sha256sum` matched the BEGIN
markers BEFORE any commit; applied by copy, `cmp` exit 0 both. f252-r4-4 re-verified to
`79db25a5…` immediately before substitution (one line, 222 chars). Provenance: `<JOB_ID>`
from the producer output; `<ZIP_FILENAME>`/`<ZIP_SHA256>` from make_review_zip.sh's JSON
(`final_path`, `final_sha256`); `<HEAD_SHA>` from the manifest's
`committed_review_subject.head_commit`. Nothing else in the line was touched.

## Deviations & assumptions
- A first bundle was discarded before any commit: `output_hash` hashed unstripped stdout
  while `stdout_summary` was stored stripped → `output_hash does not match
  sha256(stdout_summary)`. Rebuilt with a fresh job id over the stored bytes; the
  discarded directory removed.
- Evidence dir needed `git add -f` (`.gitignore:211`) and the zip is not committed
  (`remedy-review-*` ignored) — F251 / F048 precedent.
- The PR number is not in this file: the handoff is written inside the last commit
  (Rule A4), the PR is created after it — as in F251.

## Next
Reviewer closure review + feature-done banner; PR merges at the next feature's start via
the Open PR Gate. Next per Rule A5: F050, fresh window.
