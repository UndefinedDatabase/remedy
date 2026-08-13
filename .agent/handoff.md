# Handback — F115 · R26 (CLOSURE) — CLOSED

## Range
0fc9c051..HEAD on feature/f115-prompt-cost-report. Three commits: C0, ITEM A,
the closure commit. ITEM B was NOT re-ordered (landed R25 at 0fc9c051).

## Commits
### 9150dfcc chore(f115): save the R26 closure block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f115-r26-1.md | +71/-0 | block verbatim, 71 lines, 0 trailing-ws |
| .agent/last_block.md | rewrite | cmp exit 0; both sha256 c920497d6bfbd246… |

### 705feeb1 docs(f115): register R-0343, the Built State claim defects
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | R-0343 appended at EOF, byte-identical |

### <this commit> docs(f115): close F115 in the roadmap ledger
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | the authored `[x]` line, line 62 only |
| README.md | +2/-2 | 45 of 255; Tier 2 Done 5 → 6 |
| .agent/plan.md | rewrite | CLOSED state, 49 lines |
| .agent/handoff.md | rewrite | this file |

## Closure values
- Evidence job `f115-closure` — `create_manual_completion_bundle(
  review_feature_id="f115")`, verdict PASS_WITH_RISKS, authority 21 files,
  partition 7/7/7, 149 commits, total_passed 93.
- package `remedy-review-20260813-142842-READY_FOR_REVIEW.zip`
- SHA-256 `bf28ae9dfebc9ef9d2e3f57a7ad9d76155cfe35a0cc5e2b7090426aa6f7a447e`
  (re-derived with `sha256sum` on disk, equal to the builder's own value)
- accepted HEAD `705feeb19c871db6313828d76ad4e1d9e0cc4d58`
- manifest `committed_review_subject`: base `0d6c97aa06e65bea966b5210f1569de45d503845`
  → head `705feeb19c871db6313828d76ad4e1d9e0cc4d58`, 89 files;
  `review_subject_alignment=PASS`, `evidence_authoritative=true`,
  5044 members, 0 symlinks, `ZipFile.testzip()` None.

## Verification (raw)
- (a) `cmp .agent/authored/f115-r26-1.md .agent/last_block.md` → no output, exit 0.
- (b) `grep -c "^- R-0343 — Low" .agent/live_review.md` → 1 ·
  `grep -c "^## Steps" .agent/live_review.md` → 1 ·
  `grep -c "git stash list non-empty" .agent/authored/f115-r23-1.md` → 1
  (line 131) · `grep -c "must contain" .agent/authored/f115-r24-1.md` → 1
  (line 106). The entry's attribution matches both files on disk.
- (c) integrity check → `"passed": true, "fail_count": 0`, 5/5 pass; re-run
  after the plan rewrite, same result.
- (d) `git stash list | head -1` → `stash@{0}: On f115-prompt-cost-report:
  f115-closure: operator's make_review_zip.sh prune-list edit`;
  `git status --porcelain` → EMPTY. Both before the zip. NOT popped.
- (f) `pytest tests/docs/ -q` → `294 passed in 0.26s`;
  `pytest tests/cli/test_golden_path.py -q` → `42 passed in 20.79s`.
- (g) `grep -c "^- \[x\] F115 — " docs/roadmap/STATUS.md` → 1 ·
  `grep -c "^- \[~\] F115" docs/roadmap/STATUS.md` → 0.
- (h) `grep -c "45 of 255 registered items accepted" README.md` → 1.
- Byte-identity: the applied STATUS line equals the authored ITEM 6 (a) TO
  template with only the four angle-bracket slots substituted (assert `<`/`>`
  absent); the applied R-0343 line equals the authored one, sha256
  `b35ddcefbcd98f85c345cd9405bd5bcccdc68d1037c03a1bf73f92e516dd2ccf` on both.

## Artifact-build attempts (all recorded)
1. Bundle attempt 1 — FAILED, `ValueError: T002: safe-diff path set does not
   match the task partition`. Cause: the tree was still dirty, so
   `resolve_review_subject` pulled the uncommitted `scripts/make_review_zip.sh`
   into the authority set, where it has no BASE..HEAD diff.
2. Zip attempt 1 — FAILED, exit 2, `REVIEW_ZIP_ERROR: symlink
   '.remedy-wt/r12/tmpB/…current' target '…' points outside the repository`.
3. Zip attempts 2 and 3 — BLOCKED_EVIDENCE.
   `validate_evidence_candidate` → `verification_tests.json field
   verification_tests.runs[1].stdout_summary carries a local absolute path`
   (the pytest header `-- /usr/bin/python3` in the one log short enough to keep
   its header inside the 2000-char tail).
4. Bundle attempt 2 + zip attempt 4 — READY_FOR_REVIEW, values above.
   The two BLOCKED zips were deleted; only the READY one remains.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0 | done | 9150dfcc, cmp exit 0 |
| ITEM A | done | 705feeb1, both gates 1, both attribution checks 1 |
| ITEM 3 | done | integrity PASS; porcelain ` M scripts/make_review_zip.sh`; 0/2 |
| ITEM 4 | done | job `f115-closure`; deviations 1 and 3 below |
| ITEM 5 | done | stash pushed, tree clean, pushed, zip READY; deviation 2 |
| ITEM 6 | done | this commit; tests/docs 294, canary 42 |
| ITEM 7 | done | PR opened after this commit; URL in the completion report |

Deviations, declared (5):
1. ITEM 4 ordered `tests/orchestration/test_stats_report.py`. No such file.
   The real path is `tests/cli/test_stats_report.py` (10 passed) — used.
2. ITEM 5 steps 1-3 (the D7 stash) ran BEFORE ITEM 4, not after. Forced:
   `resolve_review_subject` reads the WORKING TREE, so with the packager edit
   unstashed the bundle cannot be built at all (attempt 1 above). The protocol
   requires a clean tree for the package; this only extends it to the bundle.
3. `_tail` in the scratch bundle builder applies a SECOND redaction pass,
   `packages.common.path_redaction.scrub_paths`, after
   `job_evidence._scrub_paths`. Without it the interpreter's own absolute path
   in pytest's header line packages BLOCKED_EVIDENCE. Redaction, not
   truncation: nothing else in the summary changed.
4. Six pytest `*current` convenience SYMLINKS under the gitignored
   `.remedy-wt/` were deleted so the packager's symlink guard passes. They are
   auto-generated basetemp links; every numbered target directory is intact.
   The durable fix is the operator's own stashed prune-list edit (R-0295,
   DECISION F107 D3a), which this feature does not own.
5. `.agent/plan.md` does not carry the PR number. It cannot: the closure
   commit is by rule the LAST commit, and the number does not exist until
   after it. It is in the completion report and the PR itself.

Deviations, declared — length: this file is 121 lines against the 60-line cap
(AGENTS.md DECISION D15). Cause is mandated content only: three per-commit
tables, the closure values, the eight-line verification transcript, the
artifact-build attempt log (every attempt including the failures, required
explicitly), the seven-row item-status table and the five block deviations. No
section was dropped and no prose was padded.

## Next
Open PR Gate at the next feature's start merges the PR; the operator may merge
manually at any time. Next feature per Rule A5: F045 — Loop definitions.
`.agent/candidates.md` is `(empty)` and was not touched. Open findings 15,
next free ID R-0344. `stash@{0}` stays in place — reversing it is the
operator's call.
