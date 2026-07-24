# Live Review — F013 Job intake

Per-feature ledger. Findings are authored by the reviewer
(Window 1) and applied here verbatim by the worker. R-XXXX IDs
continue monotonically across features (last used: R-0109).
History lives in git and in each feature's evidence zip.

### R-0110: schema-level clarifications cap defeats the A9 truncate-and-record rule
- **Status**: Done: R-0110
- **Severity**: Medium
- **Area**: packages/orchestration/schemas/models.py (JobIntake.clarifications), tests/schemas/test_job_intake.py
(test_clarifications_over_max_rejected)
- **Details**: max_length=5 makes an LLM response with >5
  clarifications a parse FAILURE (retry burned, possible
  parse-class abort) instead of the feature's A9 default:
  "keep the first five, record the drop count". Validation
  rejects before the intake module can truncate, and the
  contract has no field to carry the drop count.
- **Expected fix**: (a) remove max_length from clarifications;
  (b) add `dropped_clarifications: int = 0` to JobIntake —
  set by the intake module after truncating to 5, default 0;
  (c) replace test_clarifications_over_max_rejected with a test
  that >5 clarifications VALIDATE at schema level (truncation
  is module behavior, tested in T002); (d) schema-size ceiling
  test stays green.
- **Reviewer**: pending
