# REMEDY STATUS — Execution-Order Truth

> Grammar: see ROADMAP.md Part C. States: `[ ]` todo · `[~]` in progress · `[x]` done (PR/evidence ref REQUIRED) · `[!]` blocked (reason).
> Rule A5: the next feature is the first unchecked line, top to bottom. Update this file in the same PR as the work (A4).

## Tier 0 — Foundation & Trust Core

- [x] F001 — Adaptive provider timeouts + retry (PR #123 · commit 4856006 · external transition PASS)
- [x] F002 — Operator repair as a valid evidence path (PR #123 · evidence: remedy-review-20260706-143206-READY_FOR_REVIEW.zip · external PASS_WITH_RISKS)
- [x] F003 — Real token/cost measurement (PR #123 · implementation evidence: remedy-review-20260708-211448-READY_FOR_REVIEW.zip · runtime actuals: job 231d28005af344a1 / run 2ece61689cc046c3 · external PASS_WITH_RISKS)
- [x] F004 — Raw stream evidence (PR #124 · implementation evidence: remedy-review-20260709-225052-READY_FOR_REVIEW.zip · manual job 621369b56e834cd4 · runtime smoke job f22d69ed4c1f491b / run 54d4adc45d964812 · external PASS_WITH_RISKS)
- [x] F005 — Enforced structured outputs (PR #125 · evidence: remedy-review-20260711-132104-READY_FOR_REVIEW.zip · manual job e943e67937ef4124 · external PASS_WITH_RISKS)
- [x] F006 — Worktree isolation per run (PR #126 · evidence: remedy-review-20260712-000713-READY_FOR_REVIEW.zip · manual job 7fa740042a7e4561 · external PASS_WITH_RISKS)
- [x] F007 — Runtime harness (PR #127 · merge 7733a1d · follow-up d0a08a1 · persistent supervisor · accepted 2026-07-13 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job 2e820a4dbf9842cf · package remedy-review-20260713-115439-READY_FOR_REVIEW.zip)
- [x] F010 — Automatic failure post-mortems (classifier + call/task/job post-mortems + `remedy stats failures` · accepted 2026-07-14 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job 01363c70e13046e2 · package remedy-review-20260714-135557-READY_FOR_REVIEW.zip)
- [x] F011 — Kill switch (`remedy job stop` + safe points + STOPPED state + `job_stopped` event + stopped post-mortem · accepted 2026-07-14 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job 49955e41c49f41bc · package remedy-review-20260714-223538-READY_FOR_REVIEW.zip)
- [x] F012 — Deterministic runs (RunManifestV1 + `on_call_finalized` seam + `remedy job rerun --check-manifest` · accepted 2026-07-20 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job r40_authority_contract_closure · package remedy-review-20260720-211130-READY_FOR_REVIEW.zip)
- [x] F017 — Scope fences (T001–T003 built + repaired + cleanup; accepted 2026-07-21 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job da34f448-ad80-49ae-b8eb-8c4e7ec46645 · package remedy-review-20260721-132745-READY_FOR_REVIEW.zip · SHA-256 a6fab50307b1db62fc7491943ba68975757f4177d2f1f1047c9528c9e30b81c4 · accepted HEAD c8c72f5370249ad3239ebd9eecbd65dd252a9d5c)
- [x] F018 — Budgets & stop conditions (T001–T004 complete; accepted 2026-07-22 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job f018_final_closure_684c4eaf027e · package remedy-review-20260722-175112-READY_FOR_REVIEW.zip · SHA-256 41a77d46e5f48c1120937061d33e2c505cee00633f0f31147c14a054fc4aeaad · accepted HEAD 30dd4a8107bf6346e046d2faa098ee8a23f4191a)
- [x] F146 — Project identity & repo autodetection (T001–T003 complete; accepted 2026-07-23 · external verdict PASS_WITH_RISKS — ACCEPTED · Evidence job f146_project_identity_r4_c5d6e32f7a84 · package remedy-review-20260723-141827-READY_FOR_REVIEW.zip · SHA-256 7d5da77ca555e55f5a969e03340e3cdcd9292f413eedd0490eb53d2d739df16a · accepted HEAD c4d4e476e6057c9ebaf30dad5ce48eb158fbc6f7)
- [x] F081 — remedy init (T001–T003 complete; accepted 2026-07-23 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f081-closure · package remedy-review-20260723-231507-READY_FOR_REVIEW.zip · SHA-256 79dc8682bba602d475b1aca212c52854f3cfb51a38471f5420a92b2fae758a87 · accepted HEAD 68a2df68ed9873d71f1780d8402205d4cbb6f534)
- [x] F147 — Golden-path CLI (T001–T003 complete; accepted 2026-07-24 · live review PASS — ACCEPTED · Evidence job f147-closure · package remedy-review-20260724-121604-READY_FOR_REVIEW.zip · SHA-256 953410ab4c6aa0d4b639f96d797b7e66e93e36378338a6f9885e736d0e26ea17 · accepted HEAD 6869d82ffb68385d563f1c17d6f86c6590698ea9)
- [x] F148 — Project scoping everywhere (T001–T004 complete; accepted 2026-07-24 · live review PASS — ACCEPTED · Evidence job cf7ca6e8-8d5a-4b0a-ab4b-8f946bcdd42a · package remedy-review-20260724-180532-READY_FOR_REVIEW.zip · SHA-256 d81e54b4ea5716ab3f2c00593a3911457fff79121532bf63e3231c142496e7a9 · accepted HEAD 6799d12ed2b9f2c96b3410b150b09695c551691e)

## Tier 1 — Self-Build Bootstrap

- [x] F013 — Job intake (T001–T003 complete; accepted 2026-07-25 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f013_job_intake_closure · package remedy-review-20260725-184236-READY_FOR_REVIEW.zip · SHA-256 098bb64f72a8d08120852d280227d0805871ec41a0430b8d4c4ed7ee4509b9f1 · accepted HEAD ba6e6fe6d05e97197ca45c201a7914dc4ef20396)
- [x] F014 — Flight Plan (T001–T004 complete; accepted 2026-07-26 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job 9b0a8b6d-f03f-46d2-9dba-7584da178cd9 · package remedy-review-20260726-001936-READY_FOR_REVIEW.zip · SHA-256 bc75040080964f67e3c2a19623f6626ecc7d73df891592c083d56f3c81b997d7 · accepted HEAD 162553a5f175965aa0c51baa6769efc8f9b727f1)
- [x] F016 — Scaling task granularity (T001–T003 complete; accepted 2026-07-26 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job 1cc3b1c0-fd59-4884-9252-f8a8e79b5a59 · package remedy-review-20260726-165629-READY_FOR_REVIEW.zip · SHA-256 0a147595147fa300d0b6b7257e626394b365d689e3af540c536a0c477fb5a991 · accepted HEAD 85004253705e5eae15d969812af84738373e5453)
- [~] F034 — Bundled clarification in the Flight Plan (never at runtime)
- [ ] F046 — Multi-cycle loop
- [ ] F047 — Checkpoint & resume (kill-proof)
- [ ] F048 — Job queue
- [ ] F050 — DAG scheduling
- [ ] F051 — Escalate instead of block (unattended)
- [ ] F052 — Self-healing test rounds
- [ ] F053 — Final & interim report
- [ ] F056 — Missions: persistent goal, jobs as execution units
- [ ] F061 — Definition-of-Done compiler
- [ ] F062 — Product smoke as the closing gate
- [ ] F069 — Mission compiler
- [ ] F070 — Orchestrator loop inside Remedy
- [ ] F071 — Mission dossier
- [ ] F075 — MILESTONE GATE: 10 flawless self-runs
- [ ] F079 — Context handoffs
- [ ] F080 — Machine-readable roadmap mirror & STATUS.md

## Tier 2 — Minimal Self-Build Runtime

- [ ] F103 — Token ledger (SQLite)
- [ ] F104 — Hard budget enforcement
- [ ] F105 — Cache-optimal prompt ordering
- [ ] F107 — Context compiler v2
- [ ] F111 — Diff-only repair
- [ ] F115 — Prompt breakdown & cost report
- [ ] F045 — Loop definitions
- [ ] F057 — Rate-limit-aware scheduler
- [ ] F077 — Autonomy watchdog
- [ ] F082 — Self-benchmark
- [ ] F083 — CI self-check
- [ ] F085 — Sandbox hardening (stage 1)
- [ ] F086 — Release capability

## Tier 3 — Full Token Economy & Autonomy Extension

- [ ] F106 — Session resume instead of rebuild
- [ ] F108 — Tiered artifact summaries
- [ ] F109 — Semantic dedupe
- [ ] F110 — Model routing by task class
- [ ] F112 — Prompt budget per task class
- [ ] F113 — Local models for side roles
- [ ] F114 — Cost preview per command
- [ ] F116 — Cost anomaly alarm
- [ ] F049 — Parallelism
- [ ] F054 — Auto-revert proposal
- [ ] F055 — Rehearsal (dry check)
- [ ] F058 — Model failover chain
- [ ] F059 — Notifications
- [ ] F060 — Long-run certificate
- [ ] F063 — Idea engine v1
- [ ] F064 — Idea queue UI/CLI
- [ ] F065 — Idea engine v2 (continuous, opt-in)
- [ ] F066 — Idea provenance
- [ ] F067 — Routine missions
- [ ] F068 — Autonomy balance (on demand)
- [ ] F072 — Spec-first (living specification)
- [ ] F073 — Post-mortem miner → playbook proposals
- [ ] F074 — Estimate calibration
- [ ] F076 — Vision-capable planner
- [ ] F078 — Autonomy levels
- [ ] F084 — Demo mode

## Tier 4 — Memory & Learning

- [ ] F117 — Card format & store
- [ ] F118 — Deterministic card attachment
- [ ] F119 — Card UI: the collection
- [ ] F120 — Automatic card harvesting
- [ ] F121 — Decision cards from ADRs
- [ ] F122 — Project dossier card
- [ ] F123 — Effectiveness KPI
- [ ] F124 — Card hygiene (manual + periodic)
- [ ] F125 — Card scopes & inheritance
- [ ] F126 — Cards in the graph
- [ ] F127 — Optional retrieval above threshold
- [ ] F128 — Memory as a detachable module
- [ ] F144 — Capability ladder
- [ ] F145 — Playbook distillation
- [ ] F149 — remedy study (initial analysis as a card draw)
- [ ] F150 — Card value & exploration chance

## Tier 5 — Operator Cockpit (parallel human track)

- [ ] F008 — SSE event stream
- [ ] F009 — The single write channel
- [ ] F015 — Interactive plan editing
- [ ] F019 — Live node materialization
- [ ] F020 — Node lifecycle & glyph language
- [ ] F021 — Live activity feed + "agent is doing now"
- [ ] F022 — Live cost ticker
- [ ] F023 — Semantic zoom L0–L3
- [ ] F024 — Phase timeline with scrubber
- [ ] F025 — Pause/resume (global & per node)
- [ ] F026 — Task edit at runtime
- [ ] F027 — Task veto
- [ ] F028 — Task injection
- [ ] F029 — Subtree rerun
- [ ] F030 — Steering messages
- [ ] F031 — Decision inbox
- [ ] F032 — Approval with the evidence triple
- [ ] F037 — Rendered diff viewer
- [ ] F033 — Hunk-level diff approval
- [ ] F035 — Ownership ledger
- [ ] F036 — Guided result tour
- [ ] F038 — Grounded chat & intent dispatch
- [ ] F039 — Story/replay mode
- [ ] F040 — Completion/return digest
- [ ] F041 — Artifact preview
- [ ] F042 — Multi-project cockpit
- [ ] F043 — Explanation layer
- [ ] F044 — Command palette, keyboard, performance budget

## Tier 6 — Design-to-Code

- [ ] F087 — design_reference as job input
- [ ] F088 — Reference image to the builder
- [ ] F089 — Design decomposition
- [ ] F090 — Screenshot capability
- [ ] F091 — Visual self-comparison
- [ ] F092 — Visual reviewer
- [ ] F093 — Fidelity loop
- [ ] F094 — Interaction verification
- [ ] F095 — Responsive verification
- [ ] F096 — Design token extraction
- [ ] F097 — Component catalog
- [ ] F098 — Baseline guard (visual regression)
- [ ] F099 — Design feedback channel
- [ ] F100 — Multi-reference consistency
- [ ] F101 — Reference fidelity rule
- [ ] F102 — Long-run × design

## Tier 7 — Quality & Trust

- [ ] F129 — TDD gate (optional per job)
- [ ] F130 — Mutation sampling
- [ ] F131 — Adversarial second review
- [ ] F132 — Review tournament
- [ ] F133 — Provider trust score
- [ ] F134 — Security gate
- [ ] F135 — Flaky detector
- [ ] F136 — Time-travel checkpoints
- [ ] F137 — Shadow mode
- [ ] F138 — ADR automation
- [ ] F139 — Code churn metric
- [ ] F140 — Bit-exact evidence replay
- [ ] F141 — Permission matrix per autonomy level
- [ ] F142 — Trust dashboard
- [ ] F143 — Genesis run: one prompt → one product

## Tier 8 — Worker Ecosystem & Neutrality

- [ ] F151 — Worker adapter contract v2
- [ ] F152 — Worker config isolation
- [ ] F153 — Codex CLI adapter
- [ ] F154 — Gemini CLI adapter
- [ ] F155 — Local full builder
- [ ] F156 — Worker certification suite
- [ ] F157 — Capability matrix & honest degradation
- [ ] F158 — Cost normalization & price catalog
- [ ] F159 — Cross-vendor benchmark & scoreboard
- [ ] F160 — Cross-vendor failover v2
- [ ] F161 — MCP passthrough with policy
- [ ] F162 — Sandbox profiles per adapter

## Tier 9 — Evidence & Compliance Product

- [ ] F163 — Prompt->code lineage (audit trail v2)
- [ ] F164 — AI labeling in commits (standard)
- [ ] F165 — Signed certificates
- [ ] F166 — Retention & archive export
- [ ] F167 — SIEM / audit event export
- [ ] F169 — Human-oversight proof
- [ ] F168 — Technical dossier generator
- [ ] F170 — License & SBOM gate
- [ ] F171 — Secret hygiene v2 & vault
- [ ] F172 — Policy packs
- [ ] F173 — Air-gap mode
- [ ] F174 — Data classification in the context compiler

## Tier 10 — Team & Multi-User

- [ ] F175 — Identities & roles
- [ ] F176 — SSO/OIDC for the cockpit
- [ ] F177 — Multi-user write channel
- [ ] F178 — Decision assignment & delegation
- [ ] F179 — Node comments
- [ ] F180 — Human reviews as a gate
- [ ] F181 — Team ownership & contribution view
- [ ] F182 — Presence display
- [ ] F183 — Per-person notification routing
- [ ] F184 — Shared card curation
- [ ] F185 — Per-project permissions
- [ ] F186 — Human-to-human handoff package

## Tier 11 — Verification v2

- [ ] F187 — Property-based test generator
- [ ] F188 — API compatibility guard
- [ ] F189 — Service contract tests
- [ ] F190 — Test environment provisioning
- [ ] F191 — Migration safety
- [ ] F192 — Performance budgets for product code
- [ ] F193 — Accessibility gate
- [ ] F194 — i18n checks
- [ ] F195 — Budgeted fuzzing
- [ ] F196 — Flake-resistant E2E discipline

## Tier 12 — Observability & Operations

- [ ] F197 — OpenTelemetry export (GenAI conventions)
- [ ] F198 — Prometheus metrics endpoint
- [ ] F199 — Self-health & crash reports
- [ ] F200 — Daemon mode (remedy serve)
- [ ] F201 — Remote access & mobile view
- [ ] F202 — Backup/restore & schema migrations
- [ ] F203 — Structured logging & correlation
- [ ] F204 — Update channel & change transparency

## Tier 13 — Multi-Repo & Organization

- [ ] F205 — Multi-repo missions
- [ ] F206 — Repo dependency catalog
- [ ] F207 — Coordinated PR trains
- [ ] F208 — Monorepo workspaces
- [ ] F209 — Org conventions with inheritance
- [ ] F210 — Organization dashboard
- [ ] F211 — Card federation
- [ ] F212 — Release train view

## Tier 14 — Productization & Distribution

- [ ] F213 — Licensing & activation
- [ ] F214 — Editions & honest feature gating
- [ ] F215 — Distribution & signed binaries
- [ ] F216 — Docs site generator
- [ ] F217 — Templates & example gallery
- [ ] F218 — Trial mode
- [ ] F219 — Telemetry strictly opt-in
- [ ] F220 — Feedback funnel
- [ ] F221 — Release quality gate & channels
- [ ] F222 — Customer cost calculator

## Tier 15 — Intelligence v2

- [ ] F223 — Best-of-N builds
- [ ] F224 — Repo archaeology as a context source
- [ ] F225 — Reverse-DoD from legacy
- [ ] F226 — Classic risk prediction
- [ ] F227 — Prompt regression tests
- [ ] F228 — Counterfactual cost replay
- [ ] F229 — Adaptive task-size recommendation
- [ ] F230 — Mission portfolio optimizer
- [ ] F231 — Playbooks v2 with value ranking
- [ ] F232 — Model upgrade playbook

## Tier 16 — Cockpit v2

- [ ] F233 — Growing Brain stage 2 (GPU renderer)
- [ ] F234 — Organism overview (L-1)
- [ ] F235 — Diff ghosting on the timeline
- [ ] F236 — Live output stream in the node
- [ ] F237 — Embedded runtime console
- [ ] F238 — Cockpit plugin API
- [ ] F239 — Theming & white-label
- [ ] F240 — Power keyboard & vim navigation
- [ ] F241 — Story export as video
- [ ] F242 — Accessibility of the cockpit itself

## Tier 17 — Self-Improvement & Ecosystem

- [ ] F243 — Public benchmark participation
- [ ] F244 — Security self-audit routine
- [ ] F245 — Evidence schema registry & versioning
- [ ] F246 — Verification gate plugin API
- [ ] F247 — Community import with provenance
- [ ] F248 — Remedy builds Remedy: the full loop
- [ ] F249 — Anonymized research exports
- [ ] F250 — Long-term consolidation into a project handbook
