# Automated Local Candidate Generator Adapter v0 (Steps 1609–1644)

The FIRST adapter that asks an explicitly-configured **local loopback** model to generate a repair
/ self-improvement candidate from a SAFE request package. The output is treated as **UNTRUSTED**
and is IMMEDIATELY routed through the existing intake pipeline.

## Core principle

> Local model may generate candidates. The orchestrator controls. Trust + Verification judge.
> Human approves. `do_continue` applies. Model output is UNTRUSTED.

## Flow

```
local generation (loopback model)
  → quarantine (raw output, private 0o600)        [provider_trust intake]
  → Trust Gate                                     [provider_trust]
  → Provider Trust Verification v1                 [provider_trust_verification]
  → Materialization (only if verification PASSED)  [provider_patch_material]
  → pending repair intent (only if supported)
  → approval_required (human)
  → do continue (apply, separate)
```

The adapter NEVER parses the model output into an intent directly — it writes the raw output to
the existing intake bridge (`intake_provider_repair`, provider label
`local_candidate_generator:<model>`) and links the resulting quarantine / trust / verification /
material / intent IDs to the generation run.

## Disabled by default · explicit opt-in · loopback only

Config (env), all required to enable:

```
REMEDY_LOCAL_CANDIDATE_GENERATOR_ENABLED=1
REMEDY_LOCAL_CANDIDATE_GENERATOR_ENDPOINT=http://127.0.0.1:11434
REMEDY_LOCAL_CANDIDATE_GENERATOR_MODEL=<model>
REMEDY_LOCAL_CANDIDATE_GENERATOR_TIMEOUT_SECONDS=20   # optional, bounded
```

`enabled` is False by default; the endpoint must be loopback (127.0.0.1 / localhost / ::1) —
external hosts, `https`-external, `file://`, and redirects are rejected (never echoed raw). A
missing/unavailable model NEVER breaks deterministic orchestration (returns `unavailable`).

## Routing gate (no bypass)

Generation runs ONLY when **Builder Routing** selects the `local_candidate_generator` tier. If a
`--routing-id` is given, that decision's tier is checked; otherwise the adapter builds a routing
decision (with local candidate generation enabled, since it is being explicitly invoked) and
requires the selected tier to be `local_candidate_generator`. Generation is additionally gated by:
contract (`local_candidate_generate`), a present request package, no pending intent/approval,
Trust Gate + Verification available, attempt-budget, and (via routing) low loop risk + no open
review blocker/high.

## Budget / idempotency

Attempt caps per request / failure / self item (config). Idempotent by
`(request_package_id, model, prompt_hash)` — a repeated identical call REUSES the prior run unless
`--new`. Token/cost is never invented (`tokens_used="unknown"`). Exhausted generation budget blocks
generation only, not deterministic flow.

## Private run storage

`.data/workspaces/orchestrator/local_candidate_runs/<generation_id>/` holds `prompt.md`,
`raw_output.txt`, and `run_manifest.json` (0o700 dir / 0o600 files, atomic, bounded). The raw
prompt/output live ONLY here; public surfaces carry hashes / counts / statuses / safe IDs.

## CLI

- `remedy local-candidate status [--job-id <id>] --json` — read-only (enabled/available/budget/latest).
- `remedy local-candidate generate --request-package-id <id> [--job-id <id>] [--routing-id <id>]
  [--failure-artifact-id <id>] [--self-attempt-id <id>] [--new] --json` — metadata-only; runs the
  model only if allowed, then routes output through Trust Gate + Verification. Never approves/applies.

Both `may_mutate_repo=false`, `may_execute_commands=false`. Contract actions
`local_candidate_generator_status` (read-only) / `local_candidate_generate` (metadata), allowed by
default but the real switch is the disabled-by-default config + routing gate. Distinct from
`cloud_provider` / external builder execution.

## Integrations

Builder Routing emits `remedy local-candidate generate --request-package-id … --json` as the
next action for the `local_candidate_generator` tier (only when a request package exists).
Surfaced in Progress Ledger / Feature Planner / Review Bundle (`local_candidate_summary.json`,
25→26 sections) / Cockpit — safe counts/statuses/IDs only; no buttons, no raw output.

## No real Ollama required in CI

The HTTP client uses an injectable `Transport` seam (shared with the local advisor). Tests pass a
fake transport returning a deterministic response; the disabled path and an unreachable loopback
port are also exercised. No subprocess, no dependency additions.

## What this block does NOT do

No cloud/provider API execution, no external network, no expensive external builder execution, no
browser, no automatic approval/apply/test/repair-loop/PR/merge/git-commit-gate/background
orchestration/UI mutation/MCP/dep upgrades. The adapter never creates an intent before Trust Gate
+ Verification, never approves/applies, and never loops generation without new evidence.

## Next

- **Local Candidate Quality Evaluation v1** — score/compare generated candidates safely.
- **External Builder Sandbox v0** — see [external-builder-sandbox-future.md](external-builder-sandbox-future.md).
