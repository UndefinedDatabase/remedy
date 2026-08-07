# Context — F080 machine-readable roadmap mirror (R4, repair + closure retry)

## Active Branch
feature/f080-roadmap-mirror — R3 PASS on the executed work, closure
blocked by R-0206 (LAST_REVIEWED_SHA 0362e19c), cut from main 1da1b07a.
The history is FROZEN: no reword, no rebase, no force-push. No PR yet —
the closure PR is R5's.

## Scope
F080 R4: persist the R3 verdict and register R-0206, fix the false
positive in packages/common/path_redaction.py (one line: ABS_PATH_RE
requires at least one tail character after the slash), append the
regression class to tests/orchestration/test_failure_postmortem.py,
re-confirm the full suite at the new HEAD, rebuild the evidence bundle
there, and build the fresh review zip. T001-T003 are landed and
untouched; no F080 product code changes this round.

## Constraints
- NOT this round: the STATUS.md [x] edit, the README capability sync
  and the PR. They are R5's single closure commit (Rule A4, R-0154).
- The fix is a SECURITY scrubber change: real paths (/etc/passwd,
  /home/..., file:// URIs, quoted Windows paths) must stay redacted.
  The appended tests pin both directions, and the reviewer already ran
  this exact change green in a disposable worktree (1271 + 137).
- Receipts are committed with the commit that applies them, staged by
  exact path — never `git add -A` (the declared R3 deviation).
- The evidence dir stays OUTSIDE the repo in session scratch and is
  never committed (closure DECISION 2026-08-01); the zip is built from
  a CLEAN tree after all content commits.
- Bundle discipline unchanged: create_manual_completion_bundle with
  review_feature_id="f080", run ids matching ^vr-\d{4,}$, full-length
  base_commit, node ids from --collect-only with len(node_ids) ==
  selected, test_files that are files. This round's real numbers only.
- Test runner is pytest: the scoped repair-proof suites, then ONE full
  `-n auto` run as the closure confirmation (the dedicated integration
  gate already PASSed in R2).

## Steps
Verdict + R-0206 registration (Part A) → detector fix + regression
tests (Part B) → clean tree, push, integrity check, full suite at the
new HEAD (Part C) → bundle rebuild + fresh zip (Part D) → handoff
rewrite carrying the zip name, SHA-256, evidence job id and the full
accepted-HEAD sha for R5.
