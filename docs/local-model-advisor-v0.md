# Local Model Advisor Adapter v0

An **optional** local-model advisory layer for orchestrator decisions. When the
deterministic orchestrator is uncertain (close options, weak evidence), it **may** ask a
local advisor model to critique a **safe summary** of the decision. The advisor can flag
concerns, alternatives, or missing evidence — but it **never** controls anything.

    remedy local-advisor status [--json]            # enabled/availability (loopback only)
    remedy local-advisor run [--job-id <id>] [--new]  # advise on the latest decision
    remedy orchestrator decide --use-local-advisor    # decide, then optionally consult

## Core principle

**LLMs advise. The orchestrator controls. Evidence is truth. Local cheap advisor first.**
Expensive/external builders are reserved for justified, targeted candidate generation
(future). The advisor's output is **critique, not truth** and is never executed.

## Disabled by default; loopback only

The advisor is **off** unless explicitly opted in, and only ever talks to a **loopback**
endpoint:

| Variable | Meaning | Default |
|---|---|---|
| `REMEDY_LOCAL_ADVISOR_ENABLED` | `1`/`true` to opt in | unset (disabled) |
| `REMEDY_LOCAL_ADVISOR_ENDPOINT` | loopback Ollama URL | unset |
| `REMEDY_LOCAL_ADVISOR_MODEL` | model name | unset |
| `REMEDY_LOCAL_ADVISOR_TIMEOUT_SECONDS` | request timeout (clamped ≤ 30) | 8 |
| `REMEDY_LOCAL_ADVISOR_MAX_RUNS` | per-scope advisor budget | 20 |

The config is **effectively enabled only** when enabled **and** the endpoint is loopback
(`127.0.0.1` / `localhost` / `::1`) **and** a model is set. External hosts, `https` to an
external host, `file://`, and HTTP redirects are rejected. A missing/unavailable local
model **never breaks** deterministic orchestration — every path degrades to a safe
`unavailable` result.

## What it sends and stores

The prompt contains **only** a safe summary: phase, top deterministic options (labels +
scores), the selected option, rejected alternatives, safe evidence refs, risk/blocker
counts, loop-guard state, and the routing tier — never raw source, diffs, logs, finding
bodies, provider/test output, secrets, or absolute paths. Raw prompt/response are written
**privately** (`.data/workspaces/orchestrator/local_advisor_runs/<id>/`, `0o700` dir,
`0o600` files, atomic, bounded). Public surfaces carry only hashes, counts, labels, and
scrubbed text.

The model must answer JSON only:

```json
{"summary": "...", "concerns": [{"severity": "low|medium|high", "message": "...",
 "evidence_ref": "..."}], "missing_evidence": ["..."], "alternative_action":
 {"label": "...", "reason": "..."}, "loop_risk": "none|low|medium|high",
 "confidence_hint": "low|medium|high"}
```

Unparseable output → `advisor_unparseable` (ignored). Code/diff content is stripped and
flagged a **high** concern. Secrets/absolute paths/tracebacks are scrubbed; unknown
severities are normalised.

## How it affects a decision

The orchestrator builds its **deterministic** decision first. The advisor can only:

- **lower** confidence,
- add safe **missing-evidence** hints,
- **escalate to human review** when it flags high loop/evidence risk **and** the
  deterministic evidence is already weak/unknown.

The advisor can **never**: create or change the next command, approve/apply/propose,
mark evidence complete, override a blocker/high-review, bypass budget/contract, or mark
success/failure. The final `next_safe_action` always stays **deterministic, catalog-backed,
and entity-backed**.

## Anti-loop

Identical evidence (same `prompt_hash` + model + endpoint + scope) **reuses** a prior run
instead of re-calling (use `--new` to force). Repeated unavailability for the same evidence
is **suppressed** after two attempts until the evidence changes. At most one retry per call;
the local-advisor budget is **separate** from the external provider budget — exhausting it
blocks the advisor only, never deterministic orchestration.

## Preparing for expensive builder routing

The deterministic routing plan already distinguishes `deterministic_only`,
`local_advisor_preferred`, `external_builder_needed`, and `human_review_required`. This
block fills in the cheap **local advisor** tier. Expensive/external builders remain a
future block — see [expensive-builder-routing-future.md](expensive-builder-routing-future.md):
they must pass the Trust Gate, carry a budget/usage policy, never apply or auto-approve, and
have their output verified.

## See also

- [orchestrator-brain-v0.md](orchestrator-brain-v0.md)
- [provider-trust-gate-v0.md](provider-trust-gate-v0.md)
- [expensive-builder-routing-future.md](expensive-builder-routing-future.md)
- [provider-trust-verification-v1.md](provider-trust-verification-v1.md) — an optional advisor critique of the safe verification summary is a documented forward seam (deferred); if implemented it may only lower confidence / add a human-review concern, never pass or reject a candidate.
- [expensive-builder-routing-v0.md](expensive-builder-routing-v0.md) — routing recommends the local advisor *before* any expensive external builder, and never loops the advisor once it has run for the current evidence.
