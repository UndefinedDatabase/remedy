# Documentation Index

> Entry point for all Remedy documentation.
> `docs/` describes the **built** system; `docs/roadmap/` describes the **target** plan.

## Quick-Find Table

| Keyword | File | Category |
|---------|------|----------|
| ADR / decision record | [0001-raise-cycle-safety-cap.md](adr/0001-raise-cycle-safety-cap.md) | adr |
| agent conventions | [worker_conventions.md](agents/worker_conventions.md), [reviewer_conventions.md](agents/reviewer_conventions.md), [teacher_conventions.md](agents/teacher_conventions.md) | agents |
| handback template | [handback_template.md](agents/handback_template.md) | agents |
| integration gate | [integration_gate.md](agents/integration_gate.md) | agents |
| orchestrator protocol | [orchestrator_protocol.md](agents/orchestrator_protocol.md) | agents |
| closure protocol | [STATUS_closure_protocol.md](roadmap/STATUS_closure_protocol.md) | roadmap |
| planner prompt | [planner_reviewer_prompt.md](agents/planner_reviewer_prompt.md) | agents |
| split workflow | [split_workflow.md](agents/split_workflow.md) | agents |
| self-drive | [self_drive_protocol.md](agents/self_drive_protocol.md) | agents |
| self-use track | [self-use-track-v1.md](system/self-use-track-v1.md) | system |
| architecture | [architecture.md](system/architecture.md) | system |
| autocoder | [autocoder-usage.md](guides/autocoder-usage.md) | guide |
| brain | [orchestrator-brain-v0.md](system/orchestrator-brain-v0.md) | system |
| brain | [project-brain.md](system/project-brain.md) | system |
| chat | [grounded-chat-spec.md](roadmap/design/grounded-chat-spec.md) | roadmap |
| candidate eval | [candidate-quality-evaluation-v1.md](system/candidate-quality-evaluation-v1.md) | system |
| CI self-check | [ci-self-check-v1.md](system/ci-self-check-v1.md) | system |
| candidate gen | [local-candidate-generator-v0.md](system/local-candidate-generator-v0.md) | system |
| cockpit | [operator-cockpit-v1.md](system/operator-cockpit-v1.md) | system |
| context | [context-inspector.md](system/context-inspector.md) | system |
| cost report | [cost-report-user-guide-v0.md](guides/cost-report-user-guide-v0.md) | guide |
| diff-only repair | [diff-only-repair-v1.md](system/diff-only-repair-v1.md) | system |
| do continue | [do-continue-v1.md](guides/do-continue-v1.md) | guide |
| do run | [do-run-v1.md](guides/do-run-v1.md) | guide |
| dogfood | [dogfood-run-user-guide.md](guides/dogfood-run-user-guide.md) | guide |
| exec guard | [exec-guard-limitations-v0.md](system/exec-guard-limitations-v0.md) | system |
| external builder | [external-builder-sandbox-v0.md](system/external-builder-sandbox-v0.md) | system |
| external builder | [external-builder-worker-contract-v0.md](system/external-builder-worker-contract-v0.md) | system |
| external builder | [managed-external-builder-execution-v1.md](system/managed-external-builder-execution-v1.md) | system |
| hunk approval | [hunk-approval-user-guide-v1.md](guides/hunk-approval-user-guide-v1.md) | guide |
| job budget | [job-budget-enforcement-v0.md](system/job-budget-enforcement-v0.md) | system |
| job context | [job-context-view-user-guide-v0.md](guides/job-context-view-user-guide-v0.md) | guide |
| model advisor | [local-model-advisor-v0.md](system/local-model-advisor-v0.md) | system |
| model defaults / dead models | [model-defaults-and-dead-model-check-v0.md](system/model-defaults-and-dead-model-check-v0.md) | system |
| project scoping | [project-scoping-v0.md](system/project-scoping-v0.md) | system |
| plan / roadmap mirror | [roadmap-mirror-v1.md](system/roadmap-mirror-v1.md) | system |
| prompt cache ordering | [cache-optimal-prompt-ordering-v1.md](system/cache-optimal-prompt-ordering-v1.md) | system |
| proof chain | [proof-chain.md](system/proof-chain.md) | system |
| provider trust | [provider-trust-gate-v0.md](system/provider-trust-gate-v0.md) | system |
| provider trust | [provider-trust-verification-v1.md](system/provider-trust-verification-v1.md) | system |
| quickstart | [simple-operator-quickstart-v0.md](guides/simple-operator-quickstart-v0.md) | guide |
| release / packaging | [release-capability-v1.md](system/release-capability-v1.md) | system |
| remedy.toml | [remedy-toml-configuration-system-v0.md](system/remedy-toml-configuration-system-v0.md) | system |
| remedy.toml | [remedy-toml-user-guide.md](guides/remedy-toml-user-guide.md) | guide |
| repair | [repair-loop-v1.md](system/repair-loop-v1.md) | system |
| repair | [repair-request-builder-v0.md](system/repair-request-builder-v0.md) | system |
| resume | [resume.md](guides/resume.md) | guide |
| review bundle | [review-bundle-v1.md](system/review-bundle-v1.md) | system |
| routing | [expensive-builder-routing-v0.md](system/expensive-builder-routing-v0.md) | system |
| runtime harness | [runtime-harness-v1.md](system/runtime-harness-v1.md) | system |
| routing policy | [model_routing_policy.md](agents/model_routing_policy.md) | agents |
| routing | [worker-registry-route-policy-v0.md](system/worker-registry-route-policy-v0.md) | system |
| self-dogfood | [self-dogfood-v0.md](system/self-dogfood-v0.md) | system |
| self-dogfood | [self-dogfood-execution-v0.md](system/self-dogfood-execution-v0.md) | system |
| semantic dedupe | [semantic-dedupe-v1.md](system/semantic-dedupe-v1.md) | system |
| session resume | [session-resume-v1.md](system/session-resume-v1.md) | system |
| snapshot | [snapshot-rollback-v1.md](system/snapshot-rollback-v1.md) | system |
| test execution | [real-test-execution-v1.md](system/real-test-execution-v1.md) | system |
| test lanes | [test-lanes-v0.md](system/test-lanes-v0.md) | system |
| token economy | [token-economy-context-budget-optimizer-v0.md](system/token-economy-context-budget-optimizer-v0.md) | system |
| token economy | [token-economy-user-guide-v0.md](guides/token-economy-user-guide-v0.md) | guide |
| tournament | [model-route-tournament-harness-v0.md](system/model-route-tournament-harness-v0.md) | system |
| UI | [ui-target.md](archive/ui-target.md) | archive |
| watchdog | [autonomy-watchdog-v1.md](system/autonomy-watchdog-v1.md) | system |
| worker | [worker.md](system/worker.md) | system |

## System Documentation (`docs/system/`)

Specifications and design documents for the built system.

| File | Description |
|------|-------------|
| [agent-tooling-audit.md](system/agent-tooling-audit.md) | Audit of agent tooling (Pi.dev, Claude Code, VS Code MCP) |
| [architecture.md](system/architecture.md) | High-level Remedy architecture |
| [autonomy-watchdog-v1.md](system/autonomy-watchdog-v1.md) | Mission tripwires (no-progress, burn anomaly, goal drift), the pause-only action, and the mission watchdog/resume/show surface |
| [bounded-overnight-executor-v0.md](system/bounded-overnight-executor-v0.md) | Bounded overnight executor *(overnight superseded)* |
| [cache-optimal-prompt-ordering-v1.md](system/cache-optimal-prompt-ordering-v1.md) | Ranked prompt-segment composition, the measured before/after cacheable prefix, and why the provider-side cache share is unmeasured |
| [candidate-quality-evaluation-v1.md](system/candidate-quality-evaluation-v1.md) | Scoring and evaluation of candidate patches |
| [ci-self-check-v1.md](system/ci-self-check-v1.md) | Remedy's own CI: the stage table, the measured runtime budgets, the hosted workflow, and what CI deliberately never runs |
| [context-inspector.md](system/context-inspector.md) | Context window inspection and debugging |
| [controlled-claude-code-operator-path-v0.md](system/controlled-claude-code-operator-path-v0.md) | Controlled operator path for Claude Code sessions |
| [core-product-spine-v0.md](system/core-product-spine-v0.md) | Core product architecture spine |
| [development-artifact-boundary-v0.md](system/development-artifact-boundary-v0.md) | Boundaries between dev artifacts and production |
| [diff-only-repair-v1.md](system/diff-only-repair-v1.md) | Diff-only repair: hunk selection, unified-diff response, strict apply, full-file fallback |
| [exec-guard-limitations-v0.md](system/exec-guard-limitations-v0.md) | What the F085 stage-1 execution guard does NOT prevent |
| [execution-approval-policy-v0.md](system/execution-approval-policy-v0.md) | Human approval gates for execution |
| [expensive-builder-routing-v0.md](system/expensive-builder-routing-v0.md) | Local-first routing to expensive external builders |
| [external-builder-sandbox-v0.md](system/external-builder-sandbox-v0.md) | Sandbox for external builder execution |
| [external-builder-worker-contract-v0.md](system/external-builder-worker-contract-v0.md) | Contract for external builder workers |
| [feature-planner-v0.md](system/feature-planner-v0.md) | Feature planning and decomposition |
| [first-fulfilled-job-demo-v0.md](system/first-fulfilled-job-demo-v0.md) | First fulfilled job demo milestone |
| [first-perfect-job-demo-v0.md](system/first-perfect-job-demo-v0.md) | First perfect job demo milestone |
| [job-budget-enforcement-v0.md](system/job-budget-enforcement-v0.md) | Per-job budget limits, the reactive and predictive stop paths, and `remedy job budget` |
| [local-candidate-generator-v0.md](system/local-candidate-generator-v0.md) | Local candidate generation adapter |
| [local-model-advisor-v0.md](system/local-model-advisor-v0.md) | Local model advisory critique adapter |
| [main-builder-adapter-v0-token-controlled-session-rail.md](system/main-builder-adapter-v0-token-controlled-session-rail.md) | Token-controlled session rail for main builder |
| [managed-external-builder-execution-v1.md](system/managed-external-builder-execution-v1.md) | Managed external builder execution + observability |
| [managed-external-builder-execution-v1-1-hardening.md](system/managed-external-builder-execution-v1-1-hardening.md) | Approval hardening for managed external builders |
| [mission-run-loop-morning-report-v0.md](system/mission-run-loop-morning-report-v0.md) | Mission run loop + morning report *(overnight superseded)* |
| [model-defaults-and-dead-model-check-v0.md](system/model-defaults-and-dead-model-check-v0.md) | Built-in model alias table, the shipped dead-model list, and the `remedy doctor core` warning |
| [model-route-tournament-harness-v0.md](system/model-route-tournament-harness-v0.md) | Model/route tournament comparison harness |
| [open-ended-dogfood-run-orchestrator-replay-analyzer-v0.md](system/open-ended-dogfood-run-orchestrator-replay-analyzer-v0.md) | Open-ended dogfood run + replay analysis |
| [operator-cockpit-v1.md](system/operator-cockpit-v1.md) | Operator cockpit UI spec |
| [orchestrator-brain-v0.md](system/orchestrator-brain-v0.md) | Main orchestrator brain (decision engine) |
| [orchestrator-loop.md](system/orchestrator-loop.md) | Orchestrator loop contract |
| [overnight-mission-contract-review-repair-spine-v0.md](system/overnight-mission-contract-review-repair-spine-v0.md) | Overnight mission contract + review/repair *(overnight superseded)* |
| [progress-ledger-v1.md](system/progress-ledger-v1.md) | Progress ledger for tracking feature/task state |
| [project-brain.md](system/project-brain.md) | Project brain knowledge graph |
| [project-scoping-v0.md](system/project-scoping-v0.md) | Project-scoped job listings and creation guard |
| [proof-chain.md](system/proof-chain.md) | Proof chain for file provenance |
| [provider-patch-materialization-v0.md](system/provider-patch-materialization-v0.md) | Materializing accepted provider patches into intents |
| [provider-trust-gate-v0.md](system/provider-trust-gate-v0.md) | Provider trust gate + external repair intake |
| [provider-trust-verification-v1.md](system/provider-trust-verification-v1.md) | Second-stage verification of trusted candidates |
| [quality-baseline-v0.md](system/quality-baseline-v0.md) | Quality baseline definitions |
| [real-test-execution-snapshot-rollback-proof-v1.md](system/real-test-execution-snapshot-rollback-proof-v1.md) | Test execution + snapshot/rollback proof spec |
| [real-test-execution-v1.md](system/real-test-execution-v1.md) | Real test execution service |
| [release-capability-v1.md](system/release-capability-v1.md) | What the wheel carries, what `remedy --version` reports, every reason the release gate refuses, and what F086 leaves unproven |
| [remedy-toml-configuration-system-v0.md](system/remedy-toml-configuration-system-v0.md) | remedy.toml configuration system |
| [repair-loop-v0.md](system/repair-loop-v0.md) | Repair loop v0 (legacy) |
| [repair-loop-v1.md](system/repair-loop-v1.md) | Repair loop v1 (bounded, approval-gated) |
| [repair-request-builder-v0.md](system/repair-request-builder-v0.md) | Provider-agnostic repair request builder |
| [review-bundle-structured-error-reporting-v1.md](system/review-bundle-structured-error-reporting-v1.md) | Structured error reporting in review bundles |
| [review-bundle-v1.md](system/review-bundle-v1.md) | Review bundle format and contents |
| [reviewer-safety.md](system/reviewer-safety.md) | Reviewer and test safety constraints |
| [roadmap-mirror-v1.md](system/roadmap-mirror-v1.md) | One-way roadmap mirror, `remedy plan status`/`next`, feature→mission adapter |
| [run-contract-v1.md](system/run-contract-v1.md) | Run contract (apply/test gates, budgets) |
| [run-replay-to-self-repair-proposal-v0.md](system/run-replay-to-self-repair-proposal-v0.md) | Replay analysis to self-repair proposal pipeline |
| [self-dogfood-execution-v0.md](system/self-dogfood-execution-v0.md) | Self-dogfood execution (bounded self-improvement) |
| [self-dogfood-v0.md](system/self-dogfood-v0.md) | Self-dogfood readiness + improvement planner |
| [self-use-track-v1.md](system/self-use-track-v1.md) | Self-use track: the curated queue, the job-file format, one item consumed per feature close |
| [semantic-dedupe-v1.md](system/semantic-dedupe-v1.md) | Semantic dedupe inside a resumed session: the sent-hash index, the marker hook, the kill switch, and the measured savings |
| [session-resume-v1.md](system/session-resume-v1.md) | Provider session resume + delta-prompt shrink: capability surface, resume threading, fallback-once, and the measured reduction |
| [snapshot-rollback-v1.md](system/snapshot-rollback-v1.md) | Snapshot/rollback proof system |
| [test-lanes-v0.md](system/test-lanes-v0.md) | Test lane isolation and routing |
| [token-aware-repair-loop-v1-v2.md](system/token-aware-repair-loop-v1-v2.md) | Token-aware repair loop architecture |
| [token-economy-context-budget-optimizer-v0.md](system/token-economy-context-budget-optimizer-v0.md) | Token economy + context budget optimizer |
| [worker.md](system/worker.md) | Worker architecture and guide |
| [worker-registry-route-policy-v0.md](system/worker-registry-route-policy-v0.md) | Worker registry + route policy |

## Guides (`docs/guides/`)

User-facing guides, quickstarts, and usage documentation.

| File | Description |
|------|-------------|
| [autocoder-usage.md](guides/autocoder-usage.md) | How to use the autocoder |
| [cost-report-user-guide-v0.md](guides/cost-report-user-guide-v0.md) | Reading `remedy stats report` |
| [do-continue-v1.md](guides/do-continue-v1.md) | `remedy do --continue` one-cycle apply flow |
| [do-run-v1.md](guides/do-run-v1.md) | `remedy do` cohesive flow |
| [dogfood-run-user-guide.md](guides/dogfood-run-user-guide.md) | Running dogfood jobs *(overnight superseded)* |
| [hunk-approval-user-guide-v1.md](guides/hunk-approval-user-guide-v1.md) | Recording a hunk-level approve and reject decision over a job's diff |
| [job-context-view-user-guide-v0.md](guides/job-context-view-user-guide-v0.md) | What one task's compiled context carries and what was omitted |
| [main-builder-adapter-user-guide-v0.md](guides/main-builder-adapter-user-guide-v0.md) | Main builder adapter usage |
| [managed-external-builder-execution-user-guide-v1.md](guides/managed-external-builder-execution-user-guide-v1.md) | Managed external builder usage |
| [model-route-tournament-user-guide-v0.md](guides/model-route-tournament-user-guide-v0.md) | Comparing routes with tournament harness |
| [overnight-mission-user-guide-v0.md](guides/overnight-mission-user-guide-v0.md) | Overnight missions *(overnight superseded)* |
| [real-test-execution-snapshot-rollback-user-guide-v1.md](guides/real-test-execution-snapshot-rollback-user-guide-v1.md) | Test execution + snapshot/rollback usage |
| [remedy-toml-user-guide.md](guides/remedy-toml-user-guide.md) | remedy.toml configuration guide |
| [resume.md](guides/resume.md) | Resuming interrupted jobs |
| [self-repair-proposal-user-guide-v0.md](guides/self-repair-proposal-user-guide-v0.md) | Self-repair proposal workflow |
| [simple-operator-quickstart-v0.md](guides/simple-operator-quickstart-v0.md) | Quickstart for new operators |
| [token-aware-repair-loop-user-guide-v1.md](guides/token-aware-repair-loop-user-guide-v1.md) | Token-aware repair loop usage |
| [token-economy-user-guide-v0.md](guides/token-economy-user-guide-v0.md) | Token budgets and context packs |
| [worker-route-policy-user-guide-v0.md](guides/worker-route-policy-user-guide-v0.md) | Choosing workers and routes |

## Archive (`docs/archive/`)

Deprecated or future-only design documents kept for historical context.

| File | Description | Status |
|------|-------------|--------|
| [bounded-overnight-prep-v0.md](archive/bounded-overnight-prep-v0.md) | Bounded overnight preparation | DEPRECATED |
| [candidate-generator-adapter-future.md](archive/candidate-generator-adapter-future.md) | Candidate generator adapter future direction | DEPRECATED |
| [expensive-builder-routing-future.md](archive/expensive-builder-routing-future.md) | Expensive builder routing future plan | DEPRECATED |
| [expensive-builder-routing-v0-plan.md](archive/expensive-builder-routing-v0-plan.md) | Design plan for expensive builder routing | DEPRECATED |
| [external-builder-sandbox-future.md](archive/external-builder-sandbox-future.md) | External builder sandbox future design | DEPRECATED |
| [model-route-tournament-future.md](archive/model-route-tournament-future.md) | Model/route tournament future design | DEPRECATED |
| [self-dogfood-overnight-future.md](archive/self-dogfood-overnight-future.md) | Self-dogfood overnight future direction | DEPRECATED |
| [ui-target.md](archive/ui-target.md) | UI target direction | DEPRECATED |

## Agent Conventions (`docs/agents/`)

Canonical, model-agnostic role conventions and routing policy. The worker,
reviewer and teacher files are the conventions prompt segments (token-capped);
the routing policy seeds F110.

| File | Description |
|------|-------------|
| [worker_conventions.md](agents/worker_conventions.md) | Worker/builder role rules (F105 conventions segment) |
| [reviewer_conventions.md](agents/reviewer_conventions.md) | Reviewer role rules + block conditions (F105 conventions segment) |
| [teacher_conventions.md](agents/teacher_conventions.md) | Teacher role rules: read-only stance, grounding sources (F255 conventions segment) |
| [model_routing_policy.md](agents/model_routing_policy.md) | Class→tier seed map, promotion rule, hard rules (seeds F110) |
| [planner_reviewer_prompt.md](agents/planner_reviewer_prompt.md) | Window 1 bootstrap: planner & live reviewer prompt |
| [split_workflow.md](agents/split_workflow.md) | Two-window feature lifecycle (v3), roles, round protocol, handoff |
| [handback_template.md](agents/handback_template.md) | Mandatory skeleton of every handoff.md handback rewrite |
| [integration_gate.md](agents/integration_gate.md) | Canonical full-suite integration-gate procedure |
| [orchestrator_protocol.md](agents/orchestrator_protocol.md) | F070 orchestrator role contract — the source of the loop's system prompt |
| [self_drive_protocol.md](agents/self_drive_protocol.md) | One-session build discipline: roles, state probe, round loop, guardrails |

## Architecture Decision Records (`docs/adr/`)

Numbered decision records for changes that need a human's explicit approval
rather than a machine's. A record is `PROPOSED` until a human applies it and
edits the status line themselves; each proposed record ships with a
ready-to-apply unified diff beside it, and applying that diff is always a
human action.

| File | Description | Status |
|------|-------------|--------|
| [0001-raise-cycle-safety-cap.md](adr/0001-raise-cycle-safety-cap.md) | Raise `CYCLE_SAFETY_CAP` 1 → 8 on the F075 10/10 gate evidence; the shipped default stays 1 | ACCEPTED & APPLIED 2026-08-07 |

## Roadmap (`docs/roadmap/`)

The target plan for the product. See [ROADMAP.md](roadmap/ROADMAP.md) for the full 258-feature
plan and [STATUS.md](roadmap/STATUS.md) for execution-order truth.

Individual feature detail files live in `docs/roadmap/features/T{tier}_F{nnn}.md`.
Target design annexes live in `docs/roadmap/design/` (currently: [grounded-chat-spec.md](roadmap/design/grounded-chat-spec.md) for F038).
Closure process: [STATUS_closure_protocol.md](roadmap/STATUS_closure_protocol.md) — the only path from `[~]` to `[x]`.

## UI Reference (`docs/ui/`)

Design reference material for the Remedy UI.

| File | Description |
|------|-------------|
| [REMEDY_UI_REBUILD_SPEC.md](ui/REMEDY_UI_REBUILD_SPEC.md) | Full UI rebuild specification (layout, components, interactions) |
| [RICHTIG_PIXEL_LOCK_SPEC.md](ui/RICHTIG_PIXEL_LOCK_SPEC.md) | Pixel-lock specification for design fidelity verification |

Visual mockups live in `docs/ui/design_reference/`.
