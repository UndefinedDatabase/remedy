## F271 — No more legacy: ownership, reachability, replace-is-delete

Closes F271 (Tier 2) at PASS. Accepted head `b54c7fb9`, evidence job `f271r5e1001`, review package `remedy-review-20260919-025357-READY_FOR_REVIEW.zip` (SHA-256 `078c50ba…39dc`).

### What it builds
- **Ownership and reach on every command group (T001).** `GroupDef` gains `feature` and `reach`. Every group of the catalog names its owning feature and the product path that reaches it. `TestGroupOwnership` refuses a group missing either, and a feature id with no STATUS line (D1).
- **No orphan modules (Design (c)).** `tests/test_no_orphan_modules.py`, in the `budgets` CI stage, fails on any module under `packages/`, `apps/` or `scripts/` that nothing outside the tests imports and no entry point runs. The exception is a module that `ALLOWED_UNWIRED` lists with its reason, and that list can only shrink. A synthetic tree keeps the scanner's red proof standing (D2).
- **Replacing is deleting.** Five unreached modules are deleted with the tests that served only them: `builder_eval.py` with its script, `diagnostic_comparison.py`, `task_plan_evidence.py`, `execution_config_evidence.py` and `patch_revert.py` (D1, D2, D3).
- **T002.**
  - Closure precondition 7 requires the reachability and orphan-module tests green in the closure transcript, and cites the AGENTS.md rule.
  - `doctor core`'s dead-command section is proved by a test that plants a command nothing references and sees it listed (D3).

### How to review
Read `.agent/decisions.md` D1 to D3 first. Then read the catalog diff, `tests/test_no_orphan_modules.py`, and the deletions commit by commit. The closure suite read `17945 passed` with no failures.

### Findings
- Resolved here: R-0893 (its module has a production importer) and R-0982 (`patch_revert.py` deleted).
- Found here and owned by F273: R-0980 (a smoke-script section requires an event no product path emits) and R-0981 (the role conventions segment is registered by no prompt builder).
- 130 findings stay open by distinct id; none is owned by F271.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
