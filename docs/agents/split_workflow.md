# Split Workflow — Two-Window Feature Life Cycle (v1)

> How one feature travels from `[ ]` to `[x]` using two agent sessions on
> the same repository (e.g. two `claude` CLI windows in tmux over SSH, or a
> chat-based reviewer). Manual, human-relayed precursor of the F070
> orchestrator loop: every rule here must be internalizable by Remedy
> later. AGENTS.md remains the highest authority.

## Scope boundary (read first)
STATUS.md, docs/roadmap/, .agent/ and this workflow exist ONLY to develop
Remedy. Remedy-the-product never reads or writes these files at runtime;
its own runs live exclusively in its internal data-root filesystem (see
docs/system/development-artifact-boundary-v0.md). Nothing in this workflow
may leak into product behavior. This scaffolding retires when Remedy builds
itself (F070/F075).

## Roles
| Window | Session | Role | Writes |
|---|---|---|---|
| 1 | top-tier model + docs/agents/planner_reviewer_prompt.md | Planner & live reviewer, one feature per session | **NOTHING. Fully read-only.** Authors exact text (steps, findings, STATUS lines) that the worker applies. |
| 2 | worker model + the bootstrap block below | Sole implementer and sole writer | All code, docs, .agent/ state, all commits — incl. STATUS lines and live_review findings authored by Window 1, applied verbatim. |
| operator | human | Message bus + final authority | Relays prompts 1→2 and handbacks 2→1; merges PRs; may pull a review zip at any time. |
| external (optional) | e.g. GPT web | Second-opinion reviewer via review zip | Findings return through the operator; Window 1 folds them into authored live_review entries. |

**Single-writer rule (load-bearing):** Window 2 is the only writer, period.
It hands back only with a clean, committed, pushed feature branch. Window 1
reads committed state only, never a working tree mid-edit. Reviewer-
authored text is applied verbatim by the worker; only reviewer-authored
text may set a finding to Resolved.

**Routing rule:** reviewer never weaker than the paired worker
(model_routing_policy.md hard rule 1).

## Transport: git, not zips
Code moves between windows exclusively via commits on the feature branch.
The review zip (scripts/make_review_zip.sh) is NOT transport — it stays a
frozen, manifest-verified evidence package: mandatory at closure
(referenced in the STATUS line, SHA-256 recorded), and on demand
mid-feature whenever the operator wants an external second opinion.

## Round life cycle (repeat 10–40×)
1. Window 1 turn: OPERATOR BRIEF (progress %, momentum, "Remedy kann
   jetzt/als Nächstes") + exactly one paste block. Operator pastes it into
   Window 2.
2. Window 2 implements exactly that block: AGENTS.md self-review loop,
   one-step-one-commit discipline, .agent/plan.md updated, tree clean,
   push. Applies any reviewer-authored live_review/STATUS text verbatim.
3. Window 2 ends with the completion report (worker_conventions.md fields,
   changed-files table mandatory) + "Handing back for review of
   <sha..sha>".
4. Operator pastes the report into Window 1.
5. Window 1 reviews bottom-up, issues the verdict, authors findings if
   needed. PASS → next step; FAIL → repair block. Back to 1.
6. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Window 2 — worker bootstrap block (paste at session start)
```
You are the Remedy worker (Window 2) for feature <Fxxx>. Rules, in priority
order: AGENTS.md, then docs/agents/worker_conventions.md, then this block.
- Read docs/roadmap/STATUS.md and the <Fxxx> feature file so you know the
  plan you execute — but Window 1 owns sequencing. Implement ONLY the
  pasted block, nothing beyond it.
- Branch per AGENTS.md: Open PR Gate first (report the result), then work
  on feature/<name>. Never touch main.
- One step = one small commit set (<500-line diffs). Full self-review loop
  and Commit Gate before every commit. Push after committing.
- No sub-agent fan-out: direct tool calls; at most one narrowly scoped
  delegated task. /background is fine; silent scope growth is not — out-of-
  scope needs become report items (A9), assumptions → assumption_log.
- Reviewer-authored text (STATUS lines, live_review findings/verdicts):
  apply VERBATIM in the commit the block assigns it to. Mark your fixes
  with `Done: R-XXXX — <summary>`. Never set Resolved yourself.
- Hand back ONLY when: block implemented, verification commands run with
  real output, .agent/plan.md current, tree clean, branch pushed. Emit the
  completion report (outcome ≤6 lines, changed-files table, real
  verification output, assumption_log entries, deviations) and end with:
  "Handing back to Window 1 for review of <LAST_SHA>..<HEAD>."
- Never fabricate data, never imply live state over mocks, never claim
  green you did not observe. "Should work" is not a status.
```

## Session hygiene
- One feature per Window-1 session; closure ends it, Rule A5 picks the
  next in a fresh one. Window 2 may live longer but re-reads truth files
  at every step (A1: repository state over session memory).
- .agent/live_review.md is a PER-FEATURE ledger: reset at feature start
  (via a reviewer-authored step); R-XXXX IDs count monotonically across
  features; history lives in git and each feature's evidence zip.
- Crash/compact recovery: all state survives in the repo (.agent/plan.md,
  live_review.md, feature-file Built State, branch commits). A restarted
  window re-bootstraps from disk; nothing is reconstructed from memory.
- Blocked: worker follows AGENTS.md If-Blocked; reviewer authors a finding
  routed to planning; feature may go `[!]` with reason — authored by
  Window 1, committed by Window 2.

## Sunset
F070 (orchestrator loop inside Remedy) replaces the operator-as-message-
bus; F075 (10 flawless self-runs) is where the operator moves from
relaying to testing. When F070 lands, this round life cycle becomes the
orchestrator's reference behavior and the paste blocks become prompt
segments. Do not let this file drift from docs/agents/ conventions.
