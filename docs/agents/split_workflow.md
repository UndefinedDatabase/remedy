# Split Workflow — Two-Window Feature Life Cycle (v3)

> How one feature travels from `[ ]` to `[x]` using two agent sessions on
> the same repository (CLI windows via tmux/SSH, or a chat-based reviewer).
> Manual precursor of the F070 orchestrator loop: every rule here must be
> internalizable by Remedy later. AGENTS.md remains the highest authority.

## Scope boundary (read first)
STATUS.md, docs/roadmap/, .agent/ and this workflow exist ONLY to develop
Remedy. Remedy-the-product never reads or writes these files at runtime;
its runs live exclusively in its internal data-root filesystem (see
docs/system/development-artifact-boundary-v0.md). Nothing here may leak
into product behavior. This scaffolding retires at F070/F075.

## Roles
| Window | Session | Role | Writes |
|---|---|---|---|
| 1 | top-tier model + docs/agents/planner_reviewer_prompt.md | Planner & live reviewer, one feature per session | **NOTHING — fully read-only.** Authors exact text (steps, findings, STATUS lines) applied by the worker; instructs merges. |
| 2 | worker model + bootstrap block below | Sole implementer, sole writer, executes merges via Open PR Gate on instruction | All code, docs, .agent/ state, all commits, instructed merges. |
| operator | human | Message bus + final authority | Relays prompts and handbacks; MAY manually review/merge the closure PR in the window between two features; may pull a review zip anytime. |
| external (optional) | e.g. GPT web | Second opinion via review zip | Findings return through the operator; Window 1 folds them into authored entries. |

**Single-writer rule (load-bearing):** Window 2 is the only writer, period.
It hands back only with a clean, committed, pushed branch. Window 1 reads
committed state only. Reviewer-authored text is applied verbatim; only
reviewer-authored text may set a finding to Resolved.

**Merge policy:** a closure PR is never merged in the same session that
created it. It merges at the START of the next feature via the AGENTS.md
Open PR Gate, on Window 1's instruction — the gap between features is the
operator's manual-review window. The operator may always merge manually
instead.

## Transport: git, not zips
Code moves between windows exclusively via commits on the feature branch.
The review zip (see STATUS_closure_protocol.md for the canonical build
sequence) is NOT transport — it is a frozen, manifest-verified evidence
package: mandatory at closure (referenced in the STATUS line, SHA-256
recorded), and on demand mid-feature for external second opinions.

## Round life cycle (repeat, ~1 relay per hour)
1. Window 1 turn: OPERATOR BRIEF table + exactly one paste block
   (a bundled ~45–90-min step, or a repair round). Operator relays it.
2. Window 2 implements exactly that block: AGENTS.md self-review loop,
   small commits, .agent/plan.md updated, tree clean, push. Applies any
   reviewer-authored live_review/STATUS text verbatim — findings FIRST,
   as their own commit, before fixing them.
3. Window 2 finishes in this exact order: (a) final work commits,
   (b) rewrite .agent/handoff.md to the true end-of-round state + commit,
   (c) ONLY IF a package is requested this round: build the review zip
   from the now-clean tree — the zip is always the LAST action, and
   packaging from a dirty tree or before the handoff rewrite is a finding,
   (d) emit the completion report + "Handing back for review of
   <sha..sha>".
4. Operator relays the report to Window 1.
5. Window 1 reviews bottom-up, verdict, next block. On closure: banner,
   session ends, PR waits for the next feature's Open PR Gate.

## .agent/handoff.md — the fast-resume file
Rewritten (never appended) by the worker at EVERY handback. Contains only
the latest state, ≤60 lines: feature + round, branch, last commit SHAs,
changed-files table, verification results (real output, trimmed), open
findings count, next expected action. Purpose: a restarted Window 1
bootstraps from STATUS.md + feature file + handoff.md + plan.md +
live_review.md instead of re-reading the project. Git history is the
archive of past handoffs.

## Window 2 — worker bootstrap block (paste at session start)
```
You are the Remedy worker (Window 2) for feature <Fxxx>. Rules, in priority
order: AGENTS.md, then docs/agents/worker_conventions.md, then this block.
- Read docs/roadmap/STATUS.md and the <Fxxx> feature file so you know the
  plan you execute — Window 1 owns sequencing. Implement ONLY the pasted
  block, nothing beyond it.
- Branch per AGENTS.md: Open PR Gate first (merge an eligible open PR only
  when the pasted block instructs it; report raw output), then work on
  feature/<name>. Never touch main directly.
- Steps arrive as ~1-hour bundles: multiple commits expected, each small
  (<500-line diffs), full self-review loop + Commit Gate before each. Push
  after committing.
- No sub-agent fan-out: direct tool calls; at most one narrowly scoped
  delegated task. /background is fine; silent scope growth is not (A9) —
  out-of-scope needs become report items, assumptions → assumption_log.
- Reviewer-authored text (STATUS lines, live_review findings/verdicts):
  apply VERBATIM. In repair rounds: persist the findings to
  .agent/live_review.md as the FIRST commit, then fix, marking
  `Done: R-XXXX`. Never set Resolved yourself.
- At every handback: rewrite .agent/handoff.md (latest state only), in
  this order: commits → handoff rewrite + commit → (zip if requested) →
  report. Emit the completion report (outcome ≤6 lines, changed-files
  table, real verification output, assumption_log entries, deviations)
  ending with:
  "Handing back to Window 1 for review of <LAST_SHA>..<HEAD>."
- Never fabricate data, never imply live state over mocks, never claim
  green you did not observe. "Should work" is not a status.
```

## Session hygiene
- One feature per Window-1 session; the done-banner ends it; Rule A5 picks
  the next feature in a fresh session (token/context economy).
- .agent/live_review.md is a PER-FEATURE ledger, reset at feature start via
  an authored step; R-XXXX IDs count monotonically across features.
- Crash/compact recovery: all state survives in the repo (handoff.md,
  plan.md, live_review.md, feature-file Built State, branch commits).
  A restarted window re-bootstraps from disk; nothing from memory.
- Blocked: worker follows AGENTS.md If-Blocked; reviewer authors a finding
  routed to planning; feature may go `[!]` with reason — authored by
  Window 1, committed by Window 2.
- Autonomous multi-part blocks contain exactly ONE handback instruction —
  at the very end. Intermediate parts end with checkpoint notes inside the
  final completion report, never with a handback.

## Sunset
F070 replaces the operator-as-message-bus; F075 (10 flawless self-runs) is
where the operator moves from relaying to testing. When F070 lands, this
round life cycle becomes the orchestrator's reference behavior and the
paste blocks become prompt segments. Do not let this file drift from
docs/agents/ conventions.
