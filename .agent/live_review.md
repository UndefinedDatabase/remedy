# Live Review — split-workflow v3 finalization

Per-feature ledger. Findings are authored by the reviewer (Window 1) and
applied here verbatim by the worker. R-XXXX IDs continue monotonically
across features. History lives in git and in each feature's evidence zip.

### R-0071: handoff.md not rewritten at handback
- **Status**: Open
- Done: R-0071 — handoff.md rewritten to real state at this handback (final commit)
- **Severity**: Medium
- **Area**: .agent/handoff.md
- **Details**: File still contains the initial template (Feature: none
  active, Branch: main) although the v3 branch has commits and a handback
  occurred. Violates the rewrite-at-every-handback rule on its first use.
- **Evidence**: .agent/handoff.md in zip 20260723-161744 vs manifest
  review_subject.branch = feature/split-workflow-v3-evidence-repair @ bd93397
- **Expected fix**: Rewrite to real current state at THIS handback and every
  future one.

### R-0072: review_protocol.md contradicts the zero-write reviewer model
- **Status**: Open
- Done: R-0072 — process rule 1 + reviewer resolution rewording applied verbatim
- **Severity**: Medium
- **Area**: .agent/review_protocol.md
- **Details**: Header says findings are authored by the reviewer and applied
  by the worker, but Process Rule 1 ("Reviewer writes findings...") and the
  Reviewer Resolution section ("the reviewer updates the finding") still
  describe a writing reviewer.
- **Evidence**: .agent/review_protocol.md lines 33, 51 (zip 20260723-161744)
- **Expected fix**: See Step 2.2 exact wording.

### R-0073: plan.md stale — evidence-repair work not reflected
- **Status**: Open
- Done: R-0073 — plan.md rewritten to cover full branch scope
- **Severity**: Low
- **Area**: .agent/plan.md
- **Details**: Plan says DONE for the docs goal only; the evidence-pipeline
  repair (Work Item C/D) is absent.
- **Evidence**: .agent/plan.md (zip 20260723-161744)
- **Expected fix**: Rewrite plan.md to cover the full branch scope incl.
  this finalization round.

### R-0074: legacy parallel-review subagent still present
- **Status**: Open
- Done: R-0074 — .claude/agents/remedy-reviewer.md deleted; decision recorded
- **Severity**: Low
- **Area**: .claude/agents/remedy-reviewer.md
- **Details**: Subagent from the retired parallel-review system; risks a
  second, conflicting reviewer path next to the split workflow.
- **Evidence**: .claude/agents/remedy-reviewer.md exists (zip 20260723-161744)
- **Expected fix**: See Step 2.5 (retire or align; deletion preferred).
