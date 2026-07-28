# Handback — F251 CLOSURE (protocol v3): STATUS [x], READY package, PR open

## Range
Review of `39c33ad..HEAD` — `feature/f251-suite-stabilization`, pushed, PR open, NOT
merged. ACCEPTED_HEAD = `86a0df39ee0928742add7ef457dbd3d1e4efb7f2`.

## Commits
### b375b32 R5 verdict + closure plan · 5b5b271 authored STATUS line
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r5-1.md, -r5-3.md | +41, +36 | verdict f90d18e7…, plan 2f01d2bb… (cmp 0) |
| .agent/authored/f251-r5-2.md | +1 | STATUS skeleton, sha256 0b3bbef5… |
| .agent/{live_review,plan}.md | rewrite | full replaces from r5-1 / r5-3 |

### ab22589 Built State · 86a0df3 final plan state before packaging
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T1_F251.md | +62 | ab22589 — Built State: seams, evidence, result, risks |
| .agent/plan.md | +12 −6 | 86a0df3 — pre-packaging state; the head the package covers |

### this commit — closure (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1 −1 | authored `[x]` line, four slots filled |
| .data/evidence_exports/b680f05b-…/ | ~90 files | evidence dir, committed AFTER the READY zip |
| .agent/{plan,handoff}.md | rewrite | final state; this file |

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 Commit A (r5-1, r5-3) | done | b375b32, both sha256 + cmp 0 |
| 2 Commit B Built State | done | ab22589 |
| 3 Preconditions | done | porcelain empty; integrity passed=true, fail_count=0 |
| 4 Evidence job | done | b680f05b-2cda-468f-a8c5-95dbe9636044 |
| 5 Review zip | done | READY_FOR_REVIEW on attempt 3 |
| 6 Commit C STATUS `[x]` | done | blank-back proof byte-identical |
| 7 PR into main, NOT merged | done | see External actions |

## Preconditions (raw)
    git status --porcelain        → (empty)
    remedy integrity check --json → passed=true, fail_count=0, check_count=5
      handler_import=pass handlers=312 · plan_consistency=pass · high_blockers_open=pass
      relevant_untracked=pass untracked=0,relevant=0
      live_review_verdict=warn "no verdict found" — known matcher backlog, a warn
      and not a fail (F048 precedent)

## Evidence job + package
    job         b680f05b-2cda-468f-a8c5-95dbe9636044 (create_manual_completion_bundle,
                review_feature_id="f251", zero-provider, attested T001–T003)
    runs        9 runs, ALL exit_code 0 / failed 0, 682 passed; validated BEFORE
                packaging: authoritative=true, is_valid_current_run=true, issues=[]
    package     remedy-review-20260728-190328-READY_FOR_REVIEW.zip
    SHA-256     95af04c380da89879bbf4f10cd2529279553a571c5c72b3870a190a90641af2f
    subject     d8ac7fa…..86a0df3… (32 commits) · members 1560 · testzip() → None

**Two zip attempts failed first and are recorded, not hidden.**
1. Bundle built at 5b5b271, then I committed plan.md, so staging refused:
   `REVIEW_ZIP_ERROR: member '.agent/plan.md' hashes to c00079db1ed2 but the plan
   declared 2f01d2bb4ea1` (the verbatim r5-3 hash the bundle had recorded). My
   ordering error: the bundle must be built at the final pre-zip head. Deleted,
   rebuilt at 86a0df3.
2. Packaged BLOCKED_EVIDENCE with one validation error:
   `verification_tests.json field verification_tests.runs[7].node_ids[11] carries
   a local absolute path`. The id is the legitimate parametrize case
   `test_every_field_changes_the_fingerprint[health_path-/healthz]` — the scanner
   reads the `/healthz` PARAMETER as a local path — a packaging false positive, not
   a defect in the run. Resolved by recording two other green modules instead
   (test_runtime_cmd, test_runtime_cli_process_boundary — both also patched by the
   port seam, 0 slash-bearing ids). Blocked zip and bundle deleted, nothing kept.

## STATUS-line proofs
    blank-back: the four measured values replaced by <JOB_ID> / <ZIP_FILENAME> /
      <ZIP_SHA256> / <ACCEPTED_HEAD_FULL_SHA> yields sha256
      0b3bbef5751813004bdfda4aefccb54bb14ed5230ffd1223af251d441d9892b2
      == f251-r5-2 authored skeleton, byte-identical
    grep "^- \[~\] F251 " docs/roadmap/STATUS.md → exit 1 (old line GONE)
    git diff --numstat -- docs/roadmap/STATUS.md → 1 1 (no other line touched)

## External actions
Pushes after every commit. `gh pr create` into main — PR **#158**, NOT merged
(the next feature's Open PR Gate merges it; the gap is the operator's
manual-review window). No merges this session.

## Deviations & assumptions
- **accepted HEAD = 86a0df3, not ab22589.** The step named Commit B's sha; protocol
  v3 defines accepted HEAD as the manifest's `committed_review_subject.head_commit`,
  and the package covers 86a0df3. Naming ab22589 would cite a head the package does
  not cover, so protocol and measured truth won. Flagged, not silent.
- **churn-gate runs are NOT in verification_runs.** The producer refuses any run with
  `exit_code != 0`, and those carry the 154 standing red. They evidence
  churn-freedom, in `.agent/f251_baseline/` and Built State — not a green-suite claim.
- Precondition 2 ("full relevant suite green") is met in its Ruling-A form per the
  R5 verdict: churn-free identical sets, standing red owned by F252.
- Package not committed (gitignored; F048 precedent). Open findings: 0.
- Runtime actuals: 5 rounds (R1–R5) + closure; models/tokens **not-measured**
  (zero-provider manual bundle, provider_call_count=0).

## Next
Window 1 closure review + feature-done banner.
**full suite: 0 quarantined, 0 churning, 154 standing red (catalogued → F252)**
