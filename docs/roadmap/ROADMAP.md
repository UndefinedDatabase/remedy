# REMEDY ROADMAP — Unified Master Plan (250 Features)

> **Version 4.0 (UNIFIED, ENGLISH) · 2026-07-03**
> **Replaces:** ROADMAP.md v3.0 (F001–F150, German) and ROADMAP_151_250.md v1.0 (F151–F250, German).
> **Location in repo:** `docs/roadmap/ROADMAP.md` · **Execution state:** `docs/roadmap/STATUS.md`
> **Feature detail files:** `docs/roadmap/features/T{tier}_F{nnn}.md` (one per feature)

**Prime objective of this reordering:** reach *self-build capability* as fast as
possible. Tier 0 and Tier 1 are built conventionally (human + coding agent).
From Tier 2 onward, Remedy develops itself: it reads this file plus STATUS.md
and works through the remaining tiers, while humans review and approve.

**Feature IDs are stable.** F-numbers never change; only tier assignment and
execution order changed versus v3.0. Cross-references in older documents remain
valid by ID.

---

## PART A — OPERATING PROTOCOL

Applies to whoever orchestrates (a web GPT today, Remedy itself from Tier 2).

- **A1 Position.** Determine the current position exclusively from repo state:
  STATUS.md (execution order truth) + `.agent/MASTERPLAN_LEDGER.md` (narrative
  log) + the latest review bundle. Never from session memory.
- **A2 Review discipline.** Every block ends with a final review: PASS or
  FINDINGS. No new feature is started while findings are open.
- **A3 Task sizing.** Mix medium and deliberately LARGE tasks; every second
  block should contain one large task as a stress test. Decompose only AFTER a
  post-mortem shows it was too large, never preemptively.
- **A4 Definition of DONE.** Tests green + reviewer PASS + orchestrator
  sign-off + the result is usable and committed. STATUS.md updated in the same
  PR. Nothing else counts as done.
- **A5 Execution order.** The next feature is the FIRST unchecked entry in
  STATUS.md, top to bottom. STATUS.md lists features grouped by tier in the
  order of this document. (This replaces the old lowest-F-number rule.)
- **A6 Meta-work freeze.** No new gates, taxonomies, manifest formats or
  evidence schemas unless a feature explicitly says so. Reuse what exists.
- **A7 Self-dissolution clause.** Once Tier 1 is DONE and the F075 gauntlet has
  passed, the external orchestrator hands over: Remedy runs the loop itself
  (F070/F080). Humans keep approvals.
- **A8 UI prompts.** Builders cannot see visual references; UI tasks therefore
  carry written style specs. The canonical written form lives in
  `docs/ui/design_reference/` (Part I) — UI prompts cite its relevant sections
  and quote only the CSS/TSX excerpts the task needs, plus feature-specific
  deltas. Until the design pipeline exists (Tier 6), those excerpts must be
  complete enough to build from.
- **A9 No runtime questions.** The reference (screenshot, spec) is law. Real
  ambiguities are bundled into ONE clarification block in the Flight Plan
  (F034); at runtime the builder documents assumptions in the assumption_log
  instead of asking. There is no time-of-day mechanic anywhere in Remedy:
  "overnight" only ever means "a run that continues while nobody watches".

## PART B — THE SELF-BUILD MODEL

**The canonical mission prompt** (what the human types once Tier 1 is done):

```
In docs/roadmap you will find ROADMAP.md and STATUS.md, which tracks which
roadmap items are already done. Work through all Tier <N> features in
STATUS.md order. Follow Part A of the roadmap. Do not stop until the tier is
complete or a limit/decision stops you.
```

Roles from that moment on:
- **Remedy** compiles each feature detail file into a mission (F080 adapter),
  plans, builds, tests, reviews, writes the ledger and updates STATUS.md.
- **Humans** approve plans and decisions (Flight Plan, decision queue, PR
  merges). Merging to main is always a human act.
- **Parallel human track:** Tier 5 (Operator Cockpit) touches mostly
  `apps/ui/` and can be built by humans with a coding agent at any time,
  concurrently with Remedy's self-build of Tiers 2–4 — the path sets are
  disjoint enough (worktrees + fences enforce it).
- **Gate:** unattended multi-cycle self-build is unlocked only after F075
  (10 clean self-runs). Until then max_cycles stays at 1.
- **CLI-first approvals:** until Tier 5 exists, decisions and plan approvals
  are answered via `remedy decisions list|answer <id> approve|reject` and the
  CLI plan confirmation. The decision queue is the same one the UI write
  channel (F009) later feeds — F009 becomes another producer, not a rework.

## PART C — STATUS.md SPECIFICATION

Location: `docs/roadmap/STATUS.md`. One line per feature, grouped by tier,
in execution order. Line grammar:

```
- [ ] F013 — Job intake
- [~] F014 — Flight Plan            (in progress: <branch>)
- [x] F001 — Provider timeouts      (PR #12 · evidence: <path-or-link>)
- [!] F062 — Product smoke          (blocked: <one-line reason>)
```

States: `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked.
Rules: exactly one `[~]` at a time per executor; a `[x]` line MUST carry a PR
or evidence reference; STATUS.md is updated in the same PR as the work (A4);
the file is parsed by F080 — do not change the grammar without updating F080.

## PART D — PRINCIPLES

- **P1 Evidence over claims.** Every "it works" has an artifact.
- **P2 Humans decide.** No auto-decisions, no auto-merge, ever.
- **P3 One write door.** All writes from the UI go through the single command
  channel (F009). No second POST route, no free-form shell channel.
- **P4 Token honesty & thrift.** Measure real usage; spend deliberately.
- **P5 Worker neutrality.** No feature may depend on a single vendor; declare
  capabilities, degrade honestly (F157).
- **P6 Honest labels.** estimated is never shown as actual; degraded is never
  shown as full; trial is never hidden.
- **P7 Questions up front.** All clarification lives in the Flight Plan block;
  the run itself never asks.

## PART E — NAMING & CONVENTIONS REGISTRY (binding, condensed)

**CLI** — `remedy do "…"` (golden path) · `remedy` (status) · `remedy ui` ·
`remedy init` · `remedy study` · `remedy jobs list|show|resume|stop|report|certificate` ·
`remedy queue add|list|rm` · `remedy loop run|list|validate|install` ·
`remedy memory list|show|compact|promote|attach|detach|approve` ·
`remedy stats cost|report|failures|autonomy|ladder|churn|trust|bench|team|quote|whatif` ·
`remedy plan status|next` · `remedy decisions list|answer <id>` · `remedy demo` · `remedy worker list|certify|scoreboard|pricing|onboard` ·
`remedy audit lineage|commits` · `remedy export dossier|archive|research` ·
`remedy policy apply|check` · `remedy serve` · `remedy doctor` · `remedy migrate` ·
`remedy backup create|restore` · `remedy update check` · `remedy license show|install` ·
`remedy telemetry enable|disable|show|purge` · `remedy release check` ·
`remedy plugin install|list|remove` · `remedy import` · `remedy bundle create` ·
`remedy handbook build` · `remedy handoff human` · `remedy feedback` · `remedy keys init`
Global flags: `--budget-usd --budget-tokens --deadline --max-cycles --rehearse
--shadow --design <png> --timeout-profile --stream-evidence --tdd --best-of N --yes`

**HTTP API** (ui_server, default port 8787) — GET `/api/state`, `/api/projects`,
`/api/projects/{pid}/jobs|digest|organisms|trust`, `/api/jobs/{jid}/graph`,
`/api/jobs/{jid}/events/stream` (SSE), `/api/jobs/{jid}/tasks/{tid}`,
`/runs/{rid}`, `/runs/{rid}/diff`, `/api/jobs/{jid}/ghost?seq=`,
`/api/memory/cards`, `/api/runtime/{h}/logs/stream`, `/metrics`.
POST — exactly ONE route: `/api/jobs/{jid}/commands`
`{"command", "args", "client_nonce"}` + Bearer + `X-Remedy-CSRF`.

**Command catalog** — pause_job, resume_job, stop_job, set_budget,
approve_plan, approve_decision, reject_decision, veto_task, edit_task,
inject_task, rerun_subtree, steer_task, approve_hunks, add_task, approve_idea,
deny_idea, reprioritize_idea, pin_card, attach_card, detach_card, approve_card,
archive_card, explain_run, design_feedback, start_preview, restart_preview,
stop_preview, assign_decision, delegate_decision, add_comment,
human_review_verdict.

**SSE envelope** — `{"seq","ts","job_id","type","payload"}`; types:
job.started, plan.task_created, run.started, run.tool_call, run.token_delta,
run.finished, task.state_changed, artifact.created, decision.requested,
decision.resolved, budget.tick, job.finished, mission.job_linked,
worker.failover, presence.changed.

**Module map (key new packages)** — `packages/core/project_identity.py` ·
`packages/orchestration/{provider_timeouts, repair_attest, token_actuals,
stream_evidence, schemas/, worktrees, failure_postmortem, kill_switch,
determinism, event_stream, command_gateway, flight_plan, scope_fences,
loop_spec, long_run_executor, checkpoints, worker_queue, mission_state,
idea_engine, dod_compiler, mission_compiler, orchestrator_loop,
mission_dossier, planner_calibration, vision_planner}.py` ·
`packages/runtimes/dev_server.py` · `packages/verification/{visual_check,
interaction_check, security_gate, mutation_probe, property_gen, api_compat,
contracts, compose_env, migration_safety, perf_budget, fuzz_probe}.py` ·
`packages/memory/{cards, card_selection, card_value, harvesting, study,
memory_api}.py` · `packages/workers/{adapter_api, certify, capability_matrix,
pricing, scoreboard, sandbox_profiles, *_adapter}.py` ·
`packages/enterprise/{lineage, signing, retention, audit_export, dossier,
oversight, sbom_gate, policy_packs}.py` · `packages/org/…` ·
`packages/telemetry/{otel, metrics, doctor, migrate, logging_setup}.py` ·
`packages/intel/…` · `packages/product/…` · `packages/ecosystem/…` ·
`apps/cli/golden.py` · `apps/server/daemon.py` ·
`apps/ui/src/components/brain/{GrowingBrain.tsx, NodeGlyphs.tsx,
useSemanticZoom.ts, brainOntology.ts, useBrainStream.ts, renderers/}`.

**Design tokens** — canonical file: `docs/ui/design_reference/tokens.css`,
namespace **`--remedy-*`** (implemented in `apps/ui/src/styles/tokens.css`).
Groups: ink/surfaces, blue ramp, status palette `--remedy-state-*` (single
source of truth for done/current/open/planned/blocked), graph tokens
`--remedy-graph-*`, spacing `--remedy-space-*`, motion `--remedy-dur-*`/
`--remedy-ease-*`, z-layers `--remedy-z-*`, radii, shadows, focus.
The former `--rm-*` palette is **deprecated**; migration map (left = legacy,
right = canonical):
--rm-card→--remedy-card · --rm-ink→--remedy-ink · --rm-ink-2→--remedy-ink-soft ·
--rm-line→--remedy-line · --rm-accent→--remedy-blue · --rm-accent-deep→--remedy-blue-strong ·
--rm-open/--rm-progress/--rm-done→--remedy-state-open/current/done ·
--rm-warn→--remedy-orange-400 (accents) / --remedy-state-blocked (fail states) ·
--rm-planned→--remedy-blue-100 · --rm-glow→--remedy-glow · --rm-live→--remedy-live ·
--rm-focus→--remedy-focus · --rm-font→--remedy-font-ui · --rm-r-card→--remedy-radius-lg ·
--rm-r-pill→--remedy-radius-pill · --rm-shadow→--remedy-shadow-soft ·
--rm-bg/--rm-bg-2→--remedy-bg/--remedy-bg-2.
No active feature or spec may instruct builders to use `--rm-*`.
Label/card styling rules: `docs/ui/design_reference/ux_spec.md`.

**Data layout** — per repo: `.remedy/{config.toml, memory/cards/, loops/,
policy/, dod/, playbooks/, ledger.md, STOP}`; global:
`~/.remedy/{projects.json, users.toml, org/, workers/, plugins/, missions/,
projects/<pid>/{jobs/, cache/, ledger.sqlite, locks/, runtime.log}}`.

---

## PART F — THE 250 FEATURES BY TIER

### TIER 0 — FOUNDATION & TRUST CORE (16 features)
*Built conventionally. Everything unattended work stands on: honest evidence, isolation, hard stops, project identity — and the init/golden-path pair F081/F147 belongs together.*

**F001 Adaptive provider timeouts + retry** — Timeouts computed per role/task
size (`provider_timeouts.py`, profiles fast|normal|patient, cap), up to 2
retries with backoff before `provider_unavailable`; retries never triggered by
review rejects. Evidence: timeout_s_effective, retries_used. → 10 self-runs
without a timeout block; every attempt separately in the ledger.

**F002 Operator repair as a valid evidence path** — `remedy do repair-attest
<job> <task>` writes provider_evidence (execution_mode=manual_operator_repair),
operator review verdict, manual_repair_provenance (diff hash, note). Verifier
accepts it as PASS-equivalent with a visible "operator-attested" badge. → A
manually repaired task passes the final verifier; the historic blocked-evidence
class of failures cannot recur.

**F003 Real token/cost measurement** — Provider calls run with JSON output;
`token_actuals.py` parses usage, cache counters, cost, session_id. Fallback to
heuristic only with honest flag. → token_truth shows actual_available=true;
job sum equals CLI sums; nothing estimated is ever labeled actual.

**F004 Raw stream evidence** — Opt-in `--stream-evidence`: stream-json output
teed to raw_stream.jsonl and parsed to normalized run_events (tool calls,
api_retry, token deltas) — the source for the live graph and replay. Redaction
before tee. → Agent traces show the real tool-call sequence, each event
traceable to a raw offset.

**F005 Enforced structured outputs** — Planner/reviewer responses validated
against JSON schemas (pydantic models in `schemas/`, schema_v everywhere);
parse failures become a classified error with max 1 retry. → 0 parse failures
across 10 runs; every call logs its schema_v.

**F006 Worktree isolation per run** — Every run works in its own
`git worktree` (`.remedy-wt/<job>`, branch `remedy/<job>`), file locks against
double claims, result handed over as branch + diff. → Two parallel runs never
collide; the main checkout stays clean; no auto-merge to main, ever.

**F007 Runtime harness** — `dev_server.py` starts/stops the target project's
dev server (cmd/port/health from `.remedy/config.toml [runtime]`,
autodetection at init), captures logs, kills process trees cleanly. →
`remedy runtime probe` brings the UI up and reports ready; no zombies.

**F010 Automatic failure post-mortems** — Every failed run writes
failure_postmortem.json with a deterministic class (timeout|parse|
review_reject|infra|budget|fence|unknown) + advice key; aggregated in
ledger.sqlite; `remedy stats failures`. → Retry cascades become countable
classes; unknown <10% on the benchmark.

**F011 Kill switch** — `.remedy/STOP` (global) and `STOP.<job>` (targeted) are
checked before every provider call, after every task, every cycle; stop writes
a checkpoint and a resumable state. UI stop button goes through the command
channel. → Stop takes effect within one cycle; resume continues exactly.

**F012 Deterministic runs** — Pinned env (TZ, locale, hash seed), injectable
clock in all evidence writers, path normalization, seeded fake provider;
determinism.json per run. → Two fake-provider runs are bit-identical; honest
docs on what is NOT deterministic for real LLM runs.

**F017 Scope fences** — Per job: protected paths, forbidden actions
(dependency_change, delete_file, network, schema_migration), must-touch paths;
enforced by prompt injection + post-run diff checks; violation = hard task
fail (class fence). → A builder touching a protected path fails with a precise
repair hint.

**F018 Budgets & stop conditions** — Every job declares BUDGET (€/tokens),
STOP (all-green | N cycles | deadline), REPORT level; the budget guard checks
at the same safe points as the kill switch; SSE budget.tick carries
basis=actual|estimated. → The first limit reached stops cleanly at a
checkpoint; the ticker never lies about its basis.


**F146 Project identity & repo autodetection** — Stable project_id detected
from cwd (`.remedy/` or `.git`, registered in `~/.remedy/projects.json`);
per-repo data in `.remedy/`, machine data in `~/.remedy/projects/<pid>/`;
every evidence artifact carries project_id (legacy shim for old evidence). →
Two repos have cleanly separated jobs, memory and ledgers.
**F081 remedy init** — Interaction-free scaffolding (.remedy/config with
provider/fence/runtime defaults, .gitignore entries, example loop), idempotent,
`--relink`. → Fresh repo: init + do runs in under 2 minutes; gaps become TODO
comments, never questions.

**F147 Golden-path CLI** — Three-command mental model: `remedy do "…"`,
`remedy` (one-screen status), `remedy ui`. Config cascade project→global;
help fits one screen. → Fresh clone: init + do = running job in under 2
minutes; no interactive wizards (P7).

**F148 Project scoping everywhere** — project_id dimension in cockpit, memory,
ledger, queues, ideas, ladder; server-side filtering; cross-project leak test
as a property over all read APIs. → No API with pid=A ever returns B data.

### TIER 1 — SELF-BUILD BOOTSTRAP (20 features)
*Built conventionally. The goal tier: after it, Remedy executes the canonical mission prompt (Part B) and develops the remaining tiers itself. Approvals in this era are CLI-first (Part B); the UI write channel arrives with Tier 5.*

**F013 Job intake** — Prose + attachments → structured job (schema: goal,
context, constraints, anti_goals, size_hint, mission_candidate); attachments
hashed and stored; missing essentials become clarification items, never
interactive questions. → `remedy do "…"` produces a valid job object without
hand-editing.

**F014 Flight Plan** — Before execution: task DAG with honest cost/duration
BANDS (labeled by estimate basis), risks, touched paths, the bundled
clarification block; persisted + hash-checked; start only after approval
(`--yes` skips). → Every job has a plan; drift from the approved hash aborts
with a clear message.

**F016 Scaling task granularity** — Task count scales with job size by
explicit rules (target input budget per task, max_tasks cap, size_hint
steering, plan_rationale per task); micro-task splitting is forbidden in the
planner prompt (A3 spirit). → Three job-size fixtures yield expected task
counts within tolerance.

**F034 Bundled clarification in the Flight Plan (never at runtime)** — Gap
classifier: blockers → numbered clarification block answered once in the plan;
defaults → assumption_log entries with source (reference|convention|token).
Builder prompt header forbids questions. → 3 ambiguities produce 1 block and 0
runtime questions; a lint over prompt traces proves it.

**F046 Multi-cycle loop** — `long_run_executor.py` replaces the max_cycles=1
limiter: plan_delta → execute → verify → checkpoint, until a Part-F018 limit
or all-green; cycle = coherent task batch. Default stays 1 cycle until F075
passes (controlled rollout). → A 5-cycle fixture run ends exactly at its
limit with a consistent workspace.

**F047 Checkpoint & resume (kill-proof)** — Atomic checkpoint per cycle
(job state, worktree head, queue cursor, budget spent, test digest, next
intent); `remedy jobs resume` loads the newest valid one and continues. →
kill -9 mid-cycle then resume equals an uninterrupted run (fake-provider
comparison); checkpoints contain no secrets.

**F048 Job queue** — SQLite queue with atomic claiming, priorities;
`remedy queue add|list|rm`; the executor consumes it when capacity is free —
immediately or while nobody watches. → 3 entries, one run, 3 results; no
double claim under parallel access.

**F251 Full-suite stabilization (flake-debt paydown)** — Registered work
item (operator decision 2026-07-27); executes before F050 (STATUS.md
order; detail: features/T1_F251.md). Restore gate discriminability before
the self-run phase: three consecutive `-n auto` full-suite runs with
identical failure sets, empty except explicitly quarantined tests. →
Deliverable baseline the F075 gauntlet inherits: "full suite on main:
N quarantined, 0 churning".

**F252 Standing-red paydown (154 ids, 13 classes)** — Registered work
item (operator ruling A, 2026-07-28); executes before F050 (STATUS.md
order; detail: features/T1_F252.md). The 154 deterministic standing-red
ids catalogued by F251 reach explicit terminal states class by class —
product bugs first, then product change, test rewrites, doc drift,
operator decisions; includes the two stopped F-A ids and the D4
fixture-vs-live design decision. → Full suite: identical sets, empty
except explicit quarantines; F251's quarantine rules unchanged.

**F050 DAG scheduling** — Topological ready-set from depends_on; a blocked
branch (awaiting decision / failed) blocks only its downstream; recompute per
task end. → Diamond fixture: B,C parallel after A; D waits for both; a block
in B still lets C finish.

**F051 Escalate instead of block (unattended)** — decision.requested pauses
only its branch; the executor pulls the next ready task; the report lists open
decisions prominently; notification hook fires. → An unattended run with 1
approval task + 2 free tasks delivers 2 results + 1 waiting decision. No
auto-decisions, ever.

**F052 Self-healing test rounds** — After a cycle verify with failing tests:
up to 2 auto-repair rounds reusing the existing repair loop with the test
digest as findings; then the cycle fails with a post-mortem. → A trivial
injected break heals unattended; a stubborn one stops after 2 rounds, counted
in the cycle report.

**F053 Final & interim report** — ONE markdown per run (final at end, interim
on demand while running): built / blocked+why / costs (basis-labeled) /
decisions / diff links / recommended next action. → Golden tests for both
modes; the interim clearly labels itself as a snapshot.

**F056 Missions: persistent goal, jobs as execution units** — Credo: an order
is always a job first; it becomes a mission only when Remedy shall plan
follow-up jobs itself. Mission = persistent goal, job = execution unit; the
entry point stays `remedy do`; Remedy decides internally and makes it
transparent in the Flight Plan. Every follow-up job starts by verifying the
previous state. The cockpit chains a mission's jobs visibly (lineage thread).
→ A long goal yields a mission with 3 chained jobs; a simple order stays a
single job without mission overhead.

**F061 Definition-of-Done compiler** — User intent + plan → CHECKABLE checks
(pytest | playwright_flow | lint | build | visual | custom_cmd; blocking
flags); generated flow specs under `.remedy/dod/`; the job only ends all-green
over blocking checks; the report shows the check matrix. → A fixture order
("CLI tool with --json flag") yields ≥4 meaningful checks; a deliberately
missing feature keeps the job open.

**F062 Product smoke as the closing gate** — Standard DoD block: app starts
(runtime probe), core flows clickable (generated smoke), zero console errors.
→ A deliberately broken start path keeps the job open with a precise smoke
finding.

**F069 Mission compiler** — Prose long-goal → MissionPlan{milestones with
compiled DoD each, draft jobs}; no autostart of drafts. → A fixture long-goal
yields ≥2 milestones with checkable DoDs.

**F070 Orchestrator loop inside Remedy** — THE heart: per mission iteration —
load the dossier, pick/shape the next job (Flight Plan), execute (F046),
evaluate against the milestone DoD, update dossier, write the ledger (Part A
rules as a generated system-prompt block). This is exactly the external
orchestrator's role, internalized. → A 2-milestone mission runs without a
human shaping prompts; ledger entries match the template; the A2 rule
(no new feature while findings are open) is provably enforced.

**F071 Mission dossier** — A maintained document ≤3000 tokens (goal, state per
milestone, risks, last decisions, next step) kept as a cache-friendly prompt
PREFIX; delta-rewritten each iteration under a hard budget. → Stays ≤3000
tokens over 5 iterations; stable prefix position (cache-hit test).

**F075 MILESTONE GATE: 10 flawless self-runs** — Definition of flawless: no
operator command except start, verifier PASS, DoD green, 0 unclassified
failures. A gauntlet harness runs 10 curated orders; the result matrix is
archived, failures stay visible. → 10/10 green unlocks multi-cycle defaults
and the self-build handover (A7). No cherry-picking.

**F079 Context handoffs** — On session/context switches: package of dossier +
latest checkpoint + open decisions, rendered as a prompt block; measured by a
10-fact recall eval. → ≥9/10 facts survive a handoff.

**F080 Machine-readable roadmap mirror & STATUS.md** — `masterplan_sync.py`
parses THIS file + `features/*.md` into `.remedy/masterplan.yaml`; STATUS.md
(Part C grammar) is the execution-order truth; `remedy plan status` shows the
next open feature and its blockers, `remedy plan next` proposes it; the
feature→mission adapter turns a detail file into a mission (its Context
section becomes a context segment). Remedy validates STATUS.md grammar and
updates it as part of A4. → `remedy plan next` names the correct next feature
from a fixture STATUS.md; the adapter compiles a detail file into a runnable
mission; a malformed STATUS.md line is rejected with a precise error.

### TIER 2 — MINIMAL SELF-BUILD RUNTIME (13 features)
*First self-build tier, deliberately slim: just enough economy (ledger, hard budgets, cache ordering, context compiler, diff-only repair, cost report), just enough safety (loops, rate governor, watchdog, sandbox stage 1) and just enough measurement (self-benchmark, CI, release capability) for cheap, safe, measurable unattended self-build. The full token economy follows in Tier 3.*

**F103 Token ledger (SQLite)** — calls table per project (job, task, role,
model, tokens, cache counters, cost, basis) fed by F003; views per job/class;
`remedy stats cost`. → Ledger sum == token_truth == ticker (triangle test);
no second truth.

**F104 Hard budget enforcement** — The guard reads ledger actuals; predictive
stop: if the next task's class P80 would break the limit, checkpoint +
decision instead of overrun. → Overrun in tests ≤ P80 tolerance; the
predictive stop produces a decision with the evidence triple.

**F105 Cache-optimal prompt ordering** — Stable prefixes first (system,
conventions, dossier, cards) then volatile parts; a segment registry with
stability ranks; cache_read share measured per role. Canonical conventions
content per role: `docs/agents/worker_conventions.md` and
`docs/agents/reviewer_conventions.md` (each ≤800 tokens, lint-enforced);
the orchestrator keeps the generated Part A block (F070). → Cache quota
measurably rises vs. the recorded baseline; golden prompts guard semantics;
worker/reviewer prompts provably carry their conventions segment at a stable
prefix position.

**F107 Context compiler v2** — Relevance instead of everything: allowed paths
+ direct import neighbors + signatures of distant dependencies;
omitted_context.json lists what was left out and why. → ≥40% input reduction
at equal PASS on the benchmark pair.

**F111 Diff-only repair** — Repair prompts carry only failing hunks + finding
+ minimal context; answer format is a schema-enforced unified diff; apply +
verify; conflict → full-file fallback. → Large-file repair with sharply
reduced input; the fix lands.

**F115 Prompt breakdown & cost report** — Token composition per call by
segment class; `remedy stats report --since` with cost curve, priciest
classes, cache quota, prior-period comparison — on demand, no fixed rhythm. →
Report correct for arbitrary ranges; per-task breakdown available.

**F045 Loop definitions** — LoopSpec (trigger, scope, action, budget, stop,
report) as TOML in `.remedy/loops/`; `remedy loop run|list|validate`; a loop
starts a normal job with loop_ref evidence. → An invalid file fails with a
line-precise message; no cron engine (external schedulers call in).

**F057 Rate-limit-aware scheduler** — Token bucket per provider fed by 429/
api_retry signals; waiting (visible state) instead of failing; parallelism
throttled. → A simulated limit delays, never blocks; wait time counted.

**F077 Autonomy watchdog** — Detects loop patterns (same task 3× without
progress), burn anomalies, goal drift; reaction: pause + decision with the
evidence triple. The watchdog stops, it never repairs. → A simulated
always-fail loop pauses after 3 with a clean decision.

**F082 Self-benchmark** — 5 frozen standard orders; metrics PASS rate, cost,
wall time, repair rounds; history + trend CLI with regression warnings. →
Reproducible (F012); fixtures frozen with versioning.

**F083 CI self-check** — Unit+integration (fake provider), determinism suite,
UI build + smoke, bundle/perf budgets; live-provider tests excluded. → Green
on a clean checkout; a deliberate budget breach fails.

**F085 Sandbox hardening (stage 1)** — Process limits, network deny for
builder subprocesses, FS scope = worktree; honest docs on what stage 1 does
NOT prevent; container stage optional later. → Escape fixtures are blocked and
logged; no security claims beyond tests.

**F086 Release capability** — pip-installable package with bundled UI assets,
semver + changelog gate, `remedy --version` with build info. → Fresh venv:
install → demo runs; versions consistent everywhere.

### TIER 3 — FULL TOKEN ECONOMY & AUTONOMY EXTENSION (26 features)
*Self-built. The remaining economy (resume, tiered summaries, dedupe, routing, per-class budgets, local side roles, cost previews, anomaly alarms) plus the autonomy extension: parallelism, failover, notifications, certificates, the idea engine, calibration, vision planning, autonomy levels, demo mode.*

**F106 Session resume instead of rebuild** — Repair rounds resume the provider
session instead of resending full context; honest fallback flag when a session
expired; token delta measured. → A resumed repair uses measurably fewer input
tokens at equal fixture quality; never across task boundaries.

**F108 Tiered artifact summaries** — Large diffs/logs get L1 (200 tokens) +
L2 sections + full reference path; prompts receive L1 + relevant L2; cheap
model generates. → Follow-up prompts use tiers instead of full text (trace
proof) at unchanged fixture quality.

**F109 Semantic dedupe** — Segment hashing: identical blocks appear once per
resumed session, then as reference markers — only where prior context is
guaranteed. → Marker replacement inside resume sessions, never in fresh ones.

**F110 Model routing by task class** — format/extract → cheap, standard
build/review → mid, architecture/mission/vision → top; per-project overrides;
routed_model + reason in evidence. Seed map, promotion thresholds
(F082-gated) and hard rules in `docs/agents/model_routing_policy.md`;
reviewer never routed weaker than the paired worker. → Benchmark: costs drop
at equal PASS rate; no silent downgrade of security-relevant roles; a
below-threshold promotion is rejected with benchmark evidence.

**F112 Prompt budget per task class** — Class input caps with a documented
drop cascade (distant signatures first) and omitted-context disclosure; if
undroppable, a task-split proposal (decision). → An artificially tight budget
holds with PASS and full disclosure; mid-file truncation is forbidden.

**F113 Local models for side roles** — Ollama/vLLM endpoint for summaries,
humanize drafts, idea raw drafts; quality-gated by benchmark spot checks; core
roles whitelisted out. → Summaries run at cost 0 (basis=local); core roles
untouched.

**F114 Cost preview per command** — Expensive UI actions (rerun subtree,
explain) show a class-based estimate band and confirm above a threshold. →
Bands honest (calibration-based); low-cost actions stay frictionless.

**F116 Cost anomaly alarm** — Burn-rate window per job vs. class expectation;
outliers warn (SSE + notify) and can throttle parallelism or pause via
decision on unattended runs. → Simulated outlier warns in <60 s; throttling is
documented; no auto-stop below the hard threshold.

**F049 Parallelism** — Up to N workers, each in its own worktree, shared
thread-safe budget guard, dynamic throttling by rate signals; only
path-disjoint tasks run in parallel. → Measurably shorter wall time; zero
collisions.

**F054 Auto-revert proposal** — Test digest start vs. end of a run; on
regression, a revert_proposal.diff + analysis in the report — NEVER applied.
→ A simulated regression yields proposal + analysis, nothing applied.

**F055 Rehearsal (dry check)** — `--rehearse`: pipeline up to Flight Plan +
estimate bands + fence simulation; zero builder calls; planner cost shown
honestly. → Structurally identical to a real plan; 0 builder calls asserted.

**F058 Model failover chain** — Per-role chains, triggered ONLY by
availability after F001 retries; configured vs. actual model in evidence +
mandatory report line. → Documented failover; quality problems never trigger
it.

**F059 Notifications** — Hooks on decision.requested & job.finished to
webhook/ntfy/mail; compact payload; delivery failure never blocks a run. → A
test run notifies; a dead channel is harmless; no inbound channels.

**F060 Long-run certificate** — Reuses the existing review bundle:
certificate.zip = report + token truth + verdicts + ownership + determinism +
hash manifest; `remedy verify` checks it; <5 MB (diffs linked). → Verifiable
on a foreign machine; tampering fails verification.

**F063 Idea engine v1** — After job end: idea generator (schema with title,
rationale, effort band, benefit, MANDATORY evidence refs) into a per-project
ideas queue, status proposed. → A demo job yields ≥3 ideas, each with a
resolvable reference; unreferenced ideas are dropped.

**F064 Idea queue UI/CLI** — approve/deny/reprioritize commands; approve
creates a DRAFT Flight Plan (no autostart); denied idea hashes are never
re-proposed. → Approve yields a startable draft; dedupe proven.

**F065 Idea engine v2 (continuous, opt-in)** — As a loop: TODO scanner,
coverage gaps, failure-class clusters, ownership corrections as sources; same
evidence duty. → The periodic run writes ONLY to the queue (side-effect
assertion); never default-on.

**F066 Idea provenance** — Typed evidence refs (file#line, failure class,
coverage, decision id); resolver checks existence at creation AND display;
missing sources mark ideas stale, never delete them. → Every queued idea has
≥1 resolving ref.

**F067 Routine missions** — Library of ready loops: dependency updates
(major bumps → decision), lint debt, doc sync, test gaps, card cleanup;
`remedy loop install`. → The dependency loop produces a proposal PR diff and a
decision for majors; routine loops run with maximal fences.

**F068 Autonomy balance (on demand)** — `remedy stats autonomy --since`:
autonomous share, interrupts per 1000 tasks, decision latency, success rate —
pulled whenever needed, no fixed reporting rhythm. → Correct against ledger
and audit for arbitrary ranges.

**F072 Spec-first (living specification)** — SPEC.md per job/mission generated
from plan + DoD; three-way drift check (spec vs. tests vs. code) after each
task; drift = finding, not auto-fix. → A deliberate scope creep produces a
drift finding with file references.

**F073 Post-mortem miner → playbook proposals** — Recurring failure patterns
(same class+module ≥3) become playbook PROPOSALS with evidence refs; approved
ones land in `.remedy/playbooks/`. → A synthetic cluster yields exactly one
referenced proposal.

**F074 Estimate calibration** — Rolling distributions per task class from
ledger actuals; Flight-Plan bands become P20–P80 with basis labels
(class_default → calibrated(n)). → After 20 fixture jobs the bands measurably
shift and the label switches.

**F076 Vision-capable planner** — PNG attachments go into planner/intake calls
as images (capability-gated, honest fallback to a structured description);
plan tasks get design-region hints. → A screenshot order yields a plan naming
visible regions.

**F078 Autonomy levels** — L2 (every start manual) … L5 (idea drafts may start
under budget caps); level changes only manual + ADR; all gates/fences apply at
every level. → The enforcement matrix proves each level's allowed start paths.

**F084 Demo mode** — `remedy demo`: a recorded deterministic fake job plays
the full cockpit showcase offline in <60 s with a permanent DEMO banner. →
Runs without keys; synthetic data always labeled.

### TIER 4 — MEMORY & LEARNING (16 features)
*Self-built. Remedy starts compounding: cards, values, playbooks, a ladder of
proven capability — all measured, nothing vibes-based.*

**F117 Card format & store** — Markdown+frontmatter cards in
`.remedy/memory/cards/` (id, type architecture|convention|lesson|decision|
risk|component, scope, status, value, uses, origin); schema-validated loader;
byte-stable roundtrip. → Diffable, hand-editable; no vector store, no DB.

**F118 Deterministic card attachment** — select(task): scope match, role-type
relevance, value ranking with an exploration quota, ~2000-token budget, stable
prefix slot; attached_cards in evidence; deterministic at equal state. → Same
state → same selection; budget never breached; no LLM selection.

**F119 Card UI: the collection** — Professional trading-card look (type color
band, title, value rank Bronze/Silver/Gold/Platinum as a subtle corner, uses
counter, origin chip); detail sheet with body, usage history, actions
edit/archive/pin/attach/detach via the command catalog. → Edits land in the
file; attach shows in the next trace; no sounds, no confetti — gamification is
information.

**F120 Automatic card harvesting** — Candidates from repeated review findings,
post-mortem patterns and ownership corrections; status proposed with mandatory
evidence refs; approve via UI/CLI. → A repeat-finding fixture yields exactly
one referenced candidate; nothing activates without approval.

**F121 Decision cards from ADRs** — Every ADR auto-generates a decision card
(summary + link, scoped to affected paths); a builder proposal contradicting
it becomes a reviewer finding citing the ADR. → The rejected alternative in a
fixture triggers the finding.

**F122 Project dossier card** — One pinned architecture card per project
(stack, structure, conventions digest, start commands), initially filled by
`remedy study`, maintenance proposals via the cleanup loop; hard ≤800 tokens.
→ The first builder prompt in a foreign fixture repo contains it.

**F123 Effectiveness KPI** — attached_cards per call in the ledger; PASS/
repair statistics with vs. without a card (matched by class); A/B mode in the
benchmark; correlation honestly labeled. → KPI available after an A/B phase,
reproducible from the ledger.

**F124 Card hygiene (manual + periodic)** — `remedy memory compact` (merge
proposals, archive not delete, budget check, conflict → decision) plus an
LLM-assisted periodic cleanup loop that checks active cards against current
code and files archive/update PROPOSALS — never silent deletion. → An obsolete
fixture card is proposed, not removed.

**F125 Card scopes & inheritance** — Global cards under `~/.remedy/`; priority
paths > project > global on collision; `remedy memory promote`. → Project
beats global in the fixture; promotion keeps history; no auto-promotion.

**F126 Cards in the graph** — L1 task nodes show a card count badge; the L2
popover lists attached cards with ranks; click-through to the detail sheet. →
A 3-card fixture task shows "3"; the path to detail works.

**F127 Optional retrieval above threshold** — Only above 200 active cards: a
local embedding index as a PRE-filter before the deterministic ranking; below
the threshold behavior is bit-identical. → Regression test proves identity
below; same top-k above.

**F128 Memory as a detachable module** — `[memory] enabled=false` empties the
selector, the UI shows module-off, nothing breaks; the core imports memory
only through memory_api (import-linter rule). → Core benchmark unchanged when
off; boundary violations fail lint.

**F144 Capability ladder** — Order sizes S/M/L/XL with success criteria per
rung (PASS without operator, cost and wall time in band); history per rung;
`remedy stats ladder`; planner hints when an order exceeds the proven rung
("propose a mission of M jobs"). → The ladder warns, it never forbids.

**F145 Playbook distillation** — After ≥3 similar orders (class + keyword
heuristic): a distilled playbook proposal (proven task slicing, typical traps,
reference cards); planner uses matched playbooks as prompt blocks; efficacy
measured like cards. → 3 similar fixture jobs yield 1 proposal; a follow-up
job provably uses it.

**F149 remedy study (initial analysis as a card draw)** — On an EXISTING
project: structure scan, convention detection, test/CI state, risk hotspots,
UI component inventory → card CANDIDATES (origin=study, mandatory evidence
ref) presented as a "card draw" in the collection (staggered reveal, subtle);
runs as a normal job visible in the graph; `--limit` ranks by evidence
strength. → ≥10 referenced candidates on a fixture repo; zero cards active
without approval; the dossier card is proposed filled.

**F150 Card value & exploration chance** — Value changes ONLY through
measurable signals (attach+PASS without repair +w1, with repair +w2, FAIL in
scope −w3, periodic A/B correction); exponential smoothing, rank tiers; the
selector reserves an exploration share (default 20%) for new/low cards, drawn
deterministically from the job seed. Never an LLM judgment. → Selection
distribution ≈ 80/20 over 100 fixture tasks; a property test proves no other
code path writes value.

---

### TIER 5 — OPERATOR COCKPIT: THE GROWING BRAIN (28 features)
*Parallel human track (Part B): may be built alongside Remedy's self-build at
any time. The visible product — living graph, full control, total
explainability. Reference: Part I + docs/ui/design_reference/ux_design.png.*

**F008 SSE event stream** — `/api/jobs/{jid}/events/stream` from the event
cursor + run_events; monotonic seq, heartbeat, Last-Event-ID resume; client
hook with reconnect and honest polling fallback badge. → State changes reach
the UI in <1 s; reconnect loses nothing; no websocket (stdlib server stays).

**F009 The single write channel** — Exactly ONE POST `/commands` validating
against the command catalog (Bearer + CSRF + rate limit + nonce idempotency),
which only ENQUEUES into the decision/approval queues; audit log for every
command. → Any other POST stays 405; replays are marked duplicates; no command
reaches files or shell directly.

**F015 Interactive plan editing** — Edit/delete/reorder/merge/split tasks and
acceptance criteria before approval; edit log, DAG revalidation (cycles,
orphans); executed exactly as edited (user_edited_plan evidence). → Any edit
sequence yields a valid DAG or a clear error.

**F019 Live node materialization** — The graph grows live per the node
ontology: task nodes sprout at planning, run/synapse/artifact nodes during
execution, in event order, each traceable to an SSE seq. Tech decision
(binding, staged): stage 1 keeps react-force-graph-2d (already a dependency;
nodeCanvasObject for custom glyphs/glow, linkDirectionalParticles for active
calls, zoom API); stage 2 = PixiJS v8 only if the 60 fps budget measurably
fails (F233). Growth animation: spring from parent, 420 ms, glow pulse;
reduced-motion fallback. → Appearance order equals event order; 100 tool
calls/s throttle to ≤4 synapse nodes/s with aggregation.

**F020 Node lifecycle & glyph language** — 8 node kinds × states drawn as
canvas paths from ONE glyph source (no fonts/emoji): job_core/builder `</>`,
reviewer head-and-shoulders, test flask, repair `</>`+ring, artifact doc
corner, cluster count; colors from tokens (open violet, planned pale,
in_progress pulsing blue, done green, fail warn, vetoed struck); active edges
carry particles; legend uses the same paths as SVG. → Snapshot matrix 8×7
green; motion-off shows no particles.

**F021 Live activity feed + "agent is doing now"** — Humanized event catalog
("reads file X", "reviewer: 3 findings"), live card for the newest action,
feed rows carry seq and jump to their node; steering input renders but stays
honestly disabled until F030. → 1:1 traceability; the card switches in <1 s.

**F022 Live cost ticker** — budget.tick drives a COST metric with bar,
basis-labeled ("~" + tooltip when estimated), warning color at 85%. → Final
ticker equals the ledger to the cent; the basis label is always visible.

**F023 Semantic zoom L0–L3** — One state machine: L0 organism (job core +
tasks, run clusters as branch glow), L1 focused task expanded (siblings
dimmed), L2 run popover (verdict, tokens, duration, retries, diff/why/rerun),
L3 evidence side panel (diff | prompt trace | chat tabs); wheel thresholds
with hysteresis, clicks are the same transitions, breadcrumbs, Esc walks back,
clusters above 8 children; 60 fps at 500 nodes. → The full transition matrix
is tested; cluster "+12" expands correctly.

**F024 Phase timeline with scrubber** — Job→Planning→Build→Test→Review→
Finalized with event sub-glyphs; the scrubber rebuilds graph state from the
event prefix (memoized snapshots every 200 seq); LIVE toggle returns like a
video player. → Scrub to seq s equals replay of events[0..s] (property test).

**F025 Pause/resume (global & per node)** — Pause halts before the next
provider call (running calls finish), resume continues exactly (session ids
persisted); node-level pause via context menu. → Pause+resume equals an
uninterrupted run (deterministic comparison).

**F026 Task edit at runtime** — Waiting/paused/failed nodes are editable
(prompt/scope/criteria) with spec versioning; old runs stay in the graph as
history; the new run provably carries the patch. → v2 prompt contains the
patch; history preserved.

**F027 Task veto** — Forbid a not-yet-applied node with a mandatory reason;
downstream becomes unreachable; a replan proposal lands in the decision inbox,
never auto-executed. → Diamond fixture computes the exact unreachable set.

**F028 Task injection** — Add a node at runtime ("+ Add Task"); planner
validates fences and remaining budget (shortfall → clarification); scheduled
into the DAG. → The injected node runs in the same job.

**F029 Subtree rerun** — Reset the workspace to the snapshot before task X
(stash-based snapshots per task end), downstream back to planned, run history
preserved as a fan; optional model override. → No file corpses after reset
(diff assertion).

**F030 Steering messages** — Free-text hints into a per-task steering inbox,
injected as a binding operator note at the next round (volatile prompt tail);
the feed shows the user line; no fake dialog — the builder's "answer" is its
next real action. → The trace contains the hint exactly once per round.

**F031 Decision inbox** — Decisions block only their branch (scheduler pulls
independent ready tasks); inbox cards with badge counter driven by SSE. → 1
blocked + 2 free tasks yield 2 results + 1 clean request.

**F032 Approval with the evidence triple** — Every approval card MUST show:
evidence refs (clickable into the panel), expected outcome, downside — schema
enforced at the producer. → No approval without the three fields (test per
producer).

**F037 Rendered diff viewer** — Structured diff JSON (files/hunks/lines),
client highlighting (only needed languages bundled), file sidebar, hunk
collapse, virtual scrolling above 2k lines. → A 1 MB diff renders <300 ms.

**F033 Hunk-level diff approval** — Stable hunk ids; approve/reject per hunk
with reasons; approved hunks apply, rejected ones become precise repair
feedback. → A mixed approval yields exactly the approved patch plus a repair
round quoting the rejected hunk.

**F035 Ownership ledger** — Chronicle of all user interventions and inputs
(commands audit + clarification answers + reference-sourced assumptions),
rendered humanly ("You vetoed T004 — reason: …") in report and UI. → Complete
against the audit log.

**F036 Guided result tour** — Generated walkthrough of what was built (≤8
stops with paths, why, how to run); overlay in the UI, `--tour` in the CLI. →
Every stop path exists; an outsider finds the entry point.


**F038 Grounded chat & intent dispatch** — Chat as one input inside the
cockpit (PART J stands); target design: `docs/roadmap/design/grounded-chat-spec.md`.
Read path: node scope answered ONLY from that node's evidence; project scope
ONLY from the defined evidence set (project brain aggregate, progress ledger,
decision queue, STATUS.md position, latest reports; F071/F103 join when
built); citation chips anchor into artifacts; uncited claims render
"unsupported"; canary answers "not in evidence". Write path: free text parses
(F005 schema) into exactly one existing verb (F013 do, F030 steer, decision
answer, pause/resume) as a confirmable action card; nothing executes
unconfirmed; dispatch runs through the normal audited write channel (F009).
CLI-first delivery (`remedy chat`, Part B), cockpit surface second; chat
classes route cheap/mid per F110 (local-capable, F113). → All anchors
resolve; canary honest in both scopes; intent fixtures map to correct
verb+args or honest rejection; an unconfirmed card executes nothing; a
chat-dispatched action is audit-identical to the same action via UI/CLI.

**F039 Story/replay mode** — Chapters from phases + key events; autoplay scrub
with narration cards; export as a self-contained HTML file. → Opens standalone
in a browser; chapters jump correctly.

**F040 Completion/return digest** — Hero card at job end or first UI open
after absence: state/result, costs (basis-labeled), top ownership entries,
open decisions, one primary action. → Server-side digest endpoint; aggregates
match sources.

**F041 Artifact preview** — Rendered README (sanitized), screenshots lightbox,
"open app" starts the runtime and links the live port only after a successful
probe. → XSS corpus green; no dead preview links.

**F042 Multi-project cockpit** — Home grid over projects with mini digests;
project switcher everywhere. → Card A never shows B numbers (leak property).

**F043 Explanation layer** — One tooltip catalog as the single source; every
metric/status term has one; audit test (no term without tooltip, no dead
keys); a 6-step first-run tour with a prominent skip. → Copy audit green.

**F044 Command palette, keyboard, performance budget** — Cmd+K palette over
catalog + node jump; j/k/Enter/Esc navigation; CI-enforced budgets: first
paint <1.5 s, 60 fps at 200 nodes, bundle cap. → Budget violations fail CI.

---

### TIER 6 — DESIGN-TO-CODE (16 features)
*Self-built. Screenshot in, faithful product out — verified, not vibed.*

**F087 design_reference as job input** — `--design shot.png` (multiple,
numbered R1..Rn, optional scope note); hashed, shown in the Flight Plan;
originals preserved. → Reference with hash in evidence and plan.

**F088 Reference image to the builder** — UI task prompts carry the image
directly where the worker supports it, plus ALWAYS the written style block
(A8); prompt trace records image_attached honestly. → No "builder saw it"
claim without the flag.

**F089 Design decomposition** — Vision call → design_spec.json (layout grid,
regions with bboxes, tokens, components with states); feeds plan tasks and
token extraction; the screenshot stays law on conflict. → Fixture
decomposition names all main regions; colors within delta-E tolerance.

**F090 Screenshot capability** — Playwright capture(url, viewport) with ready
strategy; desktop + mobile viewports; deterministic within AA tolerance. →
Runtime-down yields a clean infra failure.

**F091 Visual self-comparison** — compare(ref, shot) → SSIM, pixel diff, per-
region scores, heatmap overlay; known deviations produce plausible localized
scores. → SSIM alone is never sold as fidelity truth (always paired with
F092).

**F092 Visual reviewer** — Multimodal review against reference+shot+heatmap+
spec → findings in exactly four criteria (layout, colors, typography,
component completeness) with region, expected/actual, fix hint; schema forbids
verdicts without criteria. → Bad fixture produces findings in the right
criteria/regions; good fixture passes.

**F093 Fidelity loop** — build → capture → compare+review → repair until
target (SSIM ≥0.90 AND zero high findings, configurable) or max rounds; every
round documented (shot_n, findings_n) — the visible improvement path is sales
material. → Fixture converges in 2 rounds; honest residue report on abort.

**F094 Interaction verification** — Playwright flows generated from spec
components and DoD (hover/click/input per declared state); failures include a
screenshot of the failing moment. → An unwired button is caught.

**F095 Responsive verification** — Capture+compare per viewport; without a
mobile reference only honest heuristics (no horizontal scroll, tap targets,
min font) reported separately from comparisons. → A mobile overflow bug is
caught; no invented mobile fidelity.

**F096 Design token extraction** — spec.tokens → generated tokens.css
(in the target project's own token namespace) + stylelint rule: no hex outside tokens; builder prompts mandate
token variables. → Hex in component CSS fails lint; reference beats builder
taste.

**F097 Component catalog** — PASS components extracted (TSX+CSS+screenshot+
props doc) into `.remedy/design_system/components/`; gallery route; follow-up
jobs get the catalog index as a stable prompt block. → The second UI job
provably reuses instead of rebuilding.

**F098 Baseline guard (visual regression)** — Golden screenshots per route/
component; CI compares with tolerance; breaks fail CI with heatmap artifacts;
updates only via an explicit command showing the diff. → Agents cannot update
baselines (protected path).

**F099 Design feedback channel** — Draw rectangles + comments on a fidelity
screenshot; the next repair round receives the cropped images + comments. →
Marked feedback lands as image crops in the repair prompt (trace proof).

**F100 Multi-reference consistency** — Token fusion across references with a
conflict report (same role, different color → upfront clarification item, no
silent averaging); page↔reference mapping in the plan. → A contradiction
yields exactly one clarification.

**F101 Reference fidelity rule** — Central prompt block: "the screenshot is
law; deviations only on technical impossibility, then an assumption_log entry
with reason"; the reviewer flags unlogged deviations as high findings. → An
unlogged deviation in the fixture is flagged; the builder never 'improves' the
reference unasked.

**F102 Long-run × design** — `--design` + multi-cycle: fidelity loops as
cycles; the final report carries a before/after gallery and the heatmap
trajectory. → An unattended proof run: PNG in, feature-complete UI out, path
visible.

---

### TIER 7 — QUALITY & TRUST (15 features)
*Self-built. From "tests green" to "provably robust" — ending in the Genesis
flagship.*

**F129 TDD gate (optional per job)** — `--tdd` enforces test-task-before-
impl-task pairs with a red proof in evidence; DoD requires green. → Order
enforced; red→green documented.

**F130 Mutation sampling** — Budgeted mutmut sample on touched modules;
survivors listed as "tests that catch nothing" + optional test-task proposal.
→ A weak fixture test is exposed; runtime budget holds.

**F131 Adversarial second review** — A red-review role ("find ways this diff
breaks") for XL/security-labeled/--paranoid tasks; findings enter the normal
repair flow. → A hidden edge-case gap in the fixture is found.

**F132 Review tournament** — Same diff to 2–3 reviewer models against curated
ground truth; precision/recall calibrate reviewer routing per class; benchmark
only. → Tournament report + routing recommendation.

**F133 Provider trust score** — Rolling PASS quota, repair need, format error
rate, cost per PASS per model+role; `remedy stats trust`; feeds routing as a
RECOMMENDATION (change = config + ADR). → No auto-rerouting.

**F134 Security gate** — Curated semgrep + bandit + npm audit (high) on
touched files as review findings; a DoD block for sensitive orders; <60 s on
benchmark repos. → An injection fixture blocks until repaired; false-positive
budget observed.

**F135 Flaky detector** — Test result history at equal SHA; flakes get
quarantine markers + fix ideas; quarantine is visible in reports, never
silent. → A flickering fixture test lands in quarantine with its history.

**F136 Time-travel checkpoints** — Timeline markers; "return here + hint"
resets the worktree and seeds a steering message; the old future stays as a
grayed fossil (audit — never rewritten). → Jumping back creates a new branch;
fossils remain.

**F137 Shadow mode** — `--shadow`: full run in a throwaway worktree, result
only as diff+report with a SHADOW banner; one click adopts it into a real
branch; shadow metrics never pollute production KPIs. → Discard leaves
nothing.

**F138 ADR automation** — Architectural-decision heuristics (new dependency,
new core module, schema change, tech choice) draft an ADR for confirmation;
confirmed ADRs become decision cards. → A new-dependency fixture yields a
correct draft; no card without confirmation.

**F139 Code churn metric** — Remedy-authored lines rewritten within 7/30 days
(blame on trailer-marked commits); `remedy stats churn`; high churn per class
feeds planner hints; refactor orders exempt via label. → Reproducible on a
fixture history.

**F140 Bit-exact evidence replay** — `remedy verify --replay`: fake-provider
runs replay from recorded streams and must reproduce artifact hashes; for real
runs, all deterministic pipeline steps replay + LLM outputs hash-verify —
honest docs on what that does and does not prove. → Tampering is caught.

**F141 Permission matrix per autonomy level** — Actions (read, write worktree,
commit, push, dependency change, destructive, expensive, external) × levels
enforced at ONE point require(action); matrix visible in docs and UI; no
bypass flags. → Every forbidden cell fails cleanly with a decision offer.

**F142 Trust dashboard** — Cockpit route with tiles: autonomy share, PASS
trend, cost per feature, card effectiveness, model trust, churn — every tile
links its raw data query. Proof over claims as a UI principle. → Every number
is click-traceable to raw data.

**F143 Genesis run: one prompt → one product** — Flagship composition: empty
folder → scaffold (stack choice as ADR) → mission → multi-cycle until DoD
green + product smoke → certificate + tour + story. The 60-second sales
moment. → A real proof run: one paragraph + one screenshot before walking
away; a startable, green, clickable product (or an honest interim report)
when you return.

---

### TIER 8 — WORKER ECOSYSTEM & NEUTRALITY (12 features)
*Self-built. The structural moat: any worker pluggable, certifiable,
comparable, replaceable. F151–F162 as specified in their detail files:
adapter contract v2 (F151), worker config isolation with A/B proof (F152),
Codex adapter (F153), Gemini adapter (F154), local full builder (F155),
certification suite gating router classes (F156), capability matrix with
honest degradation (F157), cost normalization & price catalogs (F158),
cross-vendor scoreboard (F159), cross-vendor failover v2 (F160), MCP
passthrough with allowlist policy (F161), per-adapter sandbox profiles
(F162).*

### TIER 9 — EVIDENCE & COMPLIANCE PRODUCT (12 features)
*Self-built. Audits become a feature: prompt→code lineage (F163), AI commit
labeling standard (F164), signed certificates (F165), retention & archive
export (F166), SIEM/audit event export (F167), human-oversight proof (F169), technical
dossier generator with explicit "not legal advice" framing (F168), license & SBOM gate (F170), secret hygiene v2 + vault (F171), policy
packs (F172), air-gap mode with zero-egress proof (F173), data classification
in the context compiler (F174).*

### TIER 10 — TEAM & MULTI-USER (12 features)
*Identities & roles (F175), OIDC login (F176), per-user write channel (F177),
decision assignment & delegation — event-based escalation, never
time-of-day (F178), node comments (F179), human reviews as a DoD gate (F180),
team ownership view without surveillance metrics (F181), presence (F182),
per-person notification routing (F183), shared card curation (F184),
per-project permissions (F185), human→human handoff package (F186).*

### TIER 11 — VERIFICATION V2 (10 features)
*Property-based test generation (F187), API compatibility guard (F188),
service contract tests (F189), compose test environments (F190), migration
safety ritual (F191), performance budgets for product code (F192),
accessibility gate (F193), i18n checks (F194), budgeted fuzzing (F195),
flake-resistant E2E discipline (F196).*

### TIER 12 — OBSERVABILITY & OPERATIONS (8 features)
*OpenTelemetry export per the GenAI semantic conventions (F197), Prometheus
metrics (F198), self-health & local-only crash reports (F199), daemon mode
`remedy serve` with the direct mode staying first-class (F200), remote access
& mobile PWA — user-exposed, no cloud relay (F201), backup/restore & schema
migrations (F202), structured logging with job/task/run correlation (F203),
update channel — check only, never auto-update (F204).*

### TIER 13 — MULTI-REPO & ORGANIZATION (8 features)
*Multi-repo missions with strictly per-project evidence (F205), repo
dependency catalog (F206), coordinated PR trains — merges stay human (F207),
monorepo workspaces with honestly labeled scoped tests (F208), org conventions
with explicit overrides (F209), org dashboard reusing project truths (F210),
card federation with project-local values (F211), release train view (F212).*

### TIER 14 — PRODUCTIZATION & DISTRIBUTION (10 features)
*Offline license files — never bricking, never data hostage (F213), editions
with honest gating (F214), signed distribution channels (F215), docs site
generated from docs/README structure (F216), templates & a gallery of real
verified certificates (F217), trial mode with cryptographically honest
watermarks (F218), telemetry strictly opt-in with a public field catalog
(F219), feedback funnel with shown-before-send redaction (F220), release
quality gate & channels (F221), customer cost calculator with n-basis labels
(F222).*

### TIER 15 — INTELLIGENCE V2 (10 features)
*Best-of-N builds selected by deterministic verification (F223), repo
archaeology as a cited context source (F224), reverse-DoD from legacy with
property-test confirmation (F225), classic explainable risk prediction (F226),
prompt regression tests (F227), counterfactual cost replay with estimate
labels (F228), adaptive task-size recommendations (F229), mission portfolio
optimizer with an open formula (F230), playbooks v2 with measured value
(F231), model upgrade playbook — certify, benchmark, ADR draft, humans switch
(F232).*

### TIER 16 — COCKPIT V2 (10 features)
*Growing Brain stage 2 GPU renderer behind a measurement gate (F233), organism
overview L-1 (F234), diff ghosting on the timeline (F235), redacted live
output stream per node (F236), embedded read-only runtime console (F237),
cockpit plugin API in sandboxed iframes with confirm-to-command (F238),
theming & white-label with unremovable provenance (F239), full keyboard/vim
coverage with confirm overlays (F240), story export as video with an honesty
end card (F241), accessibility of the cockpit itself incl. a full list
alternative to the canvas graph (F242).*

### TIER 17 — SELF-IMPROVEMENT & ECOSYSTEM (8 features)
*Public benchmark participation with unpolished results (F243), scheduled
security self-audit routine (F244), evidence schema registry, versioning &
compat suite (F245), verification gate plugin API with a determinism admission
test (F246), community bundle import with provenance and mandatory curation
(F247), Remedy-builds-Remedy full loop over this unified roadmap — the M16
proof run (F248), anonymized research exports with k-anonymity (F249),
long-term consolidation into a sourced project handbook (F250).*

---

## PART G — MILESTONES

| # | Name | Features | Proof |
|---|---|---|---|
| M1 | "Solid ground" | Tier 0 | 10 self-runs without infra blocks; two projects cleanly separated |
| M2 | "It builds itself" | Tier 1 | F075 gauntlet 10/10 + Remedy completes its FIRST roadmap feature end-to-end from STATUS.md, humans only approving |
| M3 | "Cheap, safe, measurable" | Tier 2 | Benchmark + CI reproducible, a simulated runaway is stopped by the watchdog, benchmark cost per PASS drops ≥25% vs. the M2 baseline |
| M4 | "It runs long & cheap" | Tier 3 | A large order before walking away — finished or honestly still working on return, with certificate; cost per PASS ≥40% below the M2 baseline |
| M5 | "It learns" | Tier 4 | Card A/B shows measurable effect; study on a foreign repo yields an approved collection |
| M6 | "You can see it" | Tier 5 | The Growing Brain live demo: graph grows, zoom L0–L3, an intervention round-trips |
| M7 | "It sees" | Tier 6 | Screenshot in → UI ≥90% fidelity, unattended |
| M8 | "Genesis" | Tier 7 | One paragraph → running product, fully unattended, with certificate |
| M9 | "Any worker" | Tier 8 | The same order passes with 3 vendors + 1 local worker, scoreboard publishable |
| M10 | "Audit-proof" | Tier 9 | Simulated audit answered from lineage+dossier in <5 min; certificate verified externally |
| M11 | "Team" | Tier 10 | 3 people run a project a week with roles, assignments, human review gates |
| M12 | "Operable" | Tier 11+12 | Daemon over 50 consecutive jobs, OTel visible in a customer stack, one restore drill |
| M13 | "Organization" | Tier 13 | A mission lands a coordinated change across 2 repos with a clean train |
| M14 | "Product" | Tier 14 | A stranger installs from an official channel and reaches a first signed certificate without support |
| M15 | "Sharper" | Tier 15+16 | Best-of-N wins a measured quality delta; cockpit v2 at 2000 nodes 60 fps or a documented non-need |
| M16 | "Flywheel" | Tier 17 | Remedy completes a Tier-17 feature fully itself AND a public benchmark report is published |

## PART H — KEY DEPENDENCIES (excerpt)

F013/F014 ← F005 · F046/F047 ← F011/F018/F006 · F070 ← F069+F056+F046 ·
F080 ← F070 (adapter) but its parser/status parts have no deps — build early ·
F075 ← all of Tier 0 + F070 · Tier 2 ← F003/F103 chain (F103 first) ·
F118 ← F105/F112 · F150 ← F118+F103+F123 · F019 ← F008+F004+F014 ·
F023 ← F019/F020 · F093 ← F090/F091/F092 · F151 ← Tier 0 · F156 ← F082+F151 ·
F163 ← F004+F033+F139/F164 · F200 ← F011/F047/F048/F009 · F233 ← F019 ADR +
F044 measurements · F248 ← F080+F070+F230.

## PART I — DESIGN AUTHORITY & NODE ONTOLOGY (binding)

**Canonical UI design source: `docs/ui/design_reference/`.** The checked-in
`ux_design.png` (2174×1206, measured; equals the 1678×926 design frame at
≈1.295×) is the visual authority for the cockpit. The written specs in that
folder — `ux_spec.md`, `component_spec.md`, `graph_spec.md`, `motion_spec.md`,
`tokens.css` + `tokens_rules.md`, **`assets_spec.md` (fonts, icons, graph
glyphs, logo — the asset authority)**, `acceptance_criteria.md`,
`graph_tech_recommendation.md` — are **binding** for all UI work: cockpit
shell, Growing Brain graph (nodes, edges, clusters, semantic zoom), phase
timeline, activity feed, task list, command bar, metrics bar, right panel,
evidence/detail panels, story/replay, memory-card UI, dashboards, and the
Design-to-Code tier's visual verification tooling. Builders must not invent a
new visual language. Any visual deviation requires an assumption_log entry
with a technical reason (A9/F101 discipline). All UI uses the shared token
system (`--remedy-*`). Where any wording elsewhere in this roadmap conflicts
with the design reference on visual matters, **the design reference wins**;
feature files define behavior, the design reference defines appearance.

Node ontology (8 kinds): job_core, task, builder_run, review_run, repair_run,
test_run, synapse, artifact (+cluster; +non-semantic decor per graph_spec §8).
States: open (`--remedy-state-open` #a78bfa), planned (white + ring #9db9ee,
smaller), in_progress (`--remedy-state-current` #4c83ff, pulsing), pass
(`--remedy-state-done` #34c27e), fail/blocked (`--remedy-state-blocked`
#ef6363), vetoed (struck gray). Geometry, layers, semantic zoom L0–L3,
event mapping, animation and performance strategy: `graph_spec.md` §4–§13 is
authoritative. Budgets live once, in `acceptance_criteria.md` §5.

## PART J — DELIBERATELY NOT BUILT

No own foundation model or hosting · no mandatory SaaS (local-first is law;
any cloud bridge would be a separate future decision) · no auto-merge to main
at any autonomy level · no time-of-day mechanics anywhere · no vendor-locked
feature (capability matrix + honest degradation instead) · no chat assistant
as the product surface (the cockpit is a control stand; grounded chat is one
input inside it and dispatches only existing verbs — F038) · no push-button
legal compliance claims (we ship proofs, not verdicts) · no engagement
gamification (streaks, usage badges) — gamification stays information ·
no number without a raw-data link.
