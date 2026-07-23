# Live Review — split-workflow v3 finalization

Per-feature ledger. Findings are authored by the reviewer (Window 1) and
applied here verbatim by the worker. R-XXXX IDs continue monotonically
across features. History lives in git and in each feature's evidence zip.

### R-0071: handoff.md not rewritten at handback
- **Status**: Resolved
- **Reviewer**: conditional resolution authored 2026-07-23 — clean-tree package with current handoff verified mechanically (dirty:0).
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
- **Status**: Resolved
- **Reviewer**: verified in zip 20260723-165711 (lines 33/52).
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
- **Status**: Resolved
- **Reviewer**: plan.md verified current.
- Done: R-0073 — plan.md rewritten to cover full branch scope
- **Severity**: Low
- **Area**: .agent/plan.md
- **Details**: Plan says DONE for the docs goal only; the evidence-pipeline
  repair (Work Item C/D) is absent.
- **Evidence**: .agent/plan.md (zip 20260723-161744)
- **Expected fix**: Rewrite plan.md to cover the full branch scope incl.
  this finalization round.

### R-0074: legacy parallel-review subagent still present
- **Status**: Resolved
- **Reviewer**: deletion verified; audit-doc reference handled as R-0076.
- Done: R-0074 — .claude/agents/remedy-reviewer.md deleted; decision recorded
- **Severity**: Low
- **Area**: .claude/agents/remedy-reviewer.md
- **Details**: Subagent from the retired parallel-review system; risks a
  second, conflicting reviewer path next to the split workflow.
- **Evidence**: .claude/agents/remedy-reviewer.md exists (zip 20260723-161744)
- **Expected fix**: See Step 2.5 (retire or align; deletion preferred).

### R-0075: handback package built mid-round from dirty tree
- **Status**: Resolved
- **Reviewer**: zip-last ordering codified and proven by this package.
- **Severity**: Medium
- **Area**: packaging order (split_workflow.md, STATUS_closure_protocol.md)
- **Details**: Zip 20260723-165711 was built before the final commits and
  the handoff rewrite (manifest dirty:1; handoff.md shows prior-round state,
  "Open findings: 0" contradicting 4 Open ledger entries). Partly caused by
  the reviewer prompt listing zip-build before commits — the protocol lacked
  an explicit ordering rule.
- **Evidence**: .review_zip_manifest.json review_subject.dirty_file_count_total=1;
  .agent/handoff.md content in that zip
- **Expected fix**: Protocol amendment (Step 2.1) + rebuild as last action.

### R-0076: stale subagent reference in agent-tooling audit
- **Status**: Resolved
- **Reviewer**: annotation verified present.
- **Severity**: Low
- **Area**: docs/system/agent-tooling-audit.md
- **Details**: Line lists .claude/agents/remedy-reviewer.md, deleted this
  branch.
- **Evidence**: docs/system/agent-tooling-audit.md:35
- **Expected fix**: Annotate that line: "(removed 2026-07-23 — superseded by
  docs/agents/split_workflow.md Window 1)". No other edits to that file.
