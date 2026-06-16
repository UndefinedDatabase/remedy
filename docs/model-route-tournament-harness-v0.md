# Model/Route Tournament Harness v0 (Steps 1797-1836)

## Why this exists

Remedy is becoming the Mission Control OS for agentic software work. The Tournament lets Remedy
compare available worker **routes** without trusting hype — purely from durable evidence:

- Which route produced useful candidates?
- Which route had proof?
- Which route passed verification?
- Which route got rejected?
- Which route burned fewer estimated tokens?
- Which route fit context better?
- Which route needed human approval?
- Which route should be suggested next? Which avoided for this task type?

> Workers execute. Remedy governs. **Tournament compares and recommends — it does not run workers.**

## Concepts

- **TournamentSpec** — the comparison setup: job/task/task_type, candidate routes, worker ids,
  policy id. Built from the Worker Registry + Route Policy.
- **TournamentCompetitor** — one route (= one registry worker): kind, enabled, eligible,
  blocked_reason, cost/risk tier, capability flags, approval_required, is_placeholder.
- **TournamentEvidence** — safe durable summaries per competitor (candidate quality, token economy,
  trust, verification, approval, proof, test, submissions) + `evidence_status`.
- **TournamentScore** — a deterministic `score_band` + rank + strengths/weaknesses/risk notes +
  recommendation + catalog-valid next action.
- **TournamentReport** — competitors + evidence + scores + winner (only if evidence-backed) +
  confidence + warnings + safe next actions + a human-readable safe reason.

## Evidence-only scoring

Score bands: `excellent`, `strong`, `usable`, `weak`, `blocked`, `insufficient_evidence`. The
scorer reads only existing safe summary APIs — it never reads raw candidate/prompt/output content,
and **no self-claim becomes truth**.

Hard ceilings (enforced + integrity-checked):

- No proof/test evidence → **cannot be excellent**.
- Rejected / unverified history → **blocked or weak** (a cheaper token cost cannot lift it).
- Unknown evidence → **insufficient_evidence** (or usable at most).
- High/unknown-risk route without required approval → **blocked**.
- Unknown context/budget → **approval required**.
- Placeholder (Ollama/cloud, non-executable) → **cannot be a winner band**; usable-for-planning only.
- **Insufficient evidence never produces a winner** — `winner_competitor_id` stays empty and status
  is `insufficient_evidence`.

## No execution

Tournament reads durable evidence and writes a safe report. It never runs a worker/model/provider,
generates a candidate, calls the external builder, or applies/approves/tests anything. The routing
integration is read-only metadata; the recommended next action for a placeholder route points to
**configuration/planning**, and for an external route to `remedy external-builder package-create`.

## Relationships

- **Worker Registry** — competitors are discovered from the registry; eligibility + the hard-safety
  approval floor come from `worker_registry`.
- **Token Economy** — estimated token/cost bands feed the token/cost tradeoff (estimates only).
- **Candidate Quality** — proof/verification/rejection rates are the core positive/negative signal
  (evidence-only ceilings reused).
- **External Builder Sandbox** — submission history is evidence for the external route.
- **Future Ollama/provider adapters** — once a real adapter exists, its route can compete for real;
  today Ollama/cloud are non-executable placeholders.
- **Future MemPalace project memory** — repeated tournament learnings are exactly what a memory
  layer would retain across runs; nothing is persisted as memory in this block.

## CLI

```
remedy tournament report <job_id> [--task-id ID] [--task-type TYPE] --json
remedy tournament show <tournament_id> --json
remedy tournament list <job_id> --json
remedy tournament integrity --json
```

`report` writes a safe metadata report; `show`/`list`/`integrity` are read-only. None carry
`may_execute_commands`. None execute a worker.

## Anti-goals (explicit)

- **No provider/model/Ollama/cloud/local execution.** No network, browser, subprocess, shell, MCP.
- **No self-claim becomes truth.** Unknown evidence remains unknown.
- No candidate generation, external-builder auto-call, auto-apply/approve/test/repair/PR.
- No MemPalace, no real provider pricing sync, no UI redesign.
- No fake winner when evidence is insufficient; cheap cost never beats failed trust/verification.
