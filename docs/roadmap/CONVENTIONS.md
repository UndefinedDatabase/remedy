# CONVENTIONS — verbindliches Namensregister (v1.0)

## CLI (apps/cli/, Einstieg `remedy`)
- `remedy` — Projektstatus (F147) · `remedy do "…"` — Golden Path (F147)
- `remedy ui` — Cockpit öffnen · `remedy init` (F081) · `remedy study` (F149)
- `remedy jobs list|show <id>|resume <id>|stop <id>`
- `remedy queue add <goal.md|"text">|list|rm <id>` (F048)
- `remedy do repair-attest <job> <task>` (F002)
- `remedy runtime serve|stop|probe` (F007)
- `remedy memory list|show <id>|compact|promote <id>|attach <id> <task>|detach` (T6)
- `remedy stats cost|report|failures|autonomy|ladder|churn [--since 7d]`
- `remedy plan status` (F080) · `remedy demo` (F084) · `remedy feedback` (F099-Analogon T3)
- Globale Flags: `--budget-usd`, `--budget-tokens`, `--deadline`, `--max-cycles`,
  `--rehearse` (F055), `--shadow` (F137), `--design <png>` (F087),
  `--timeout-profile fast|normal|patient` (F001), `--stream-evidence` (F004)

## HTTP-API (packages/orchestration/ui_server.py; Port 8787 Default)
- GET  `/api/state` · `/api/layers` (bestehend)
- GET  `/api/projects` (F148) · `/api/projects/{pid}/jobs`
- GET  `/api/jobs/{jid}/graph` — Ontologie-Graph (H2) für das Cockpit
- GET  `/api/jobs/{jid}/events/stream` — SSE (F008), Event-Envelope s. u.
- POST `/api/jobs/{jid}/commands` — DER eine Schreibkanal (F009)
  Body: `{"command": str, "args": {...}, "client_nonce": str}`
  Header: `Authorization: Bearer <token>`, `X-Remedy-CSRF: <token>`
- GET  `/api/jobs/{jid}/tasks/{tid}` · `/runs/{rid}` · `/runs/{rid}/diff`
- GET  `/api/memory/cards` · POST via commands (`attach_card`, …)

## Command-Katalog (F009/F065; packages/orchestration/command_catalog.py)
`pause_job, resume_job, stop_job, set_budget, approve_decision, reject_decision,
veto_task, edit_task, inject_task, rerun_subtree, steer_task, approve_hunks,
add_task, approve_idea, deny_idea, reprioritize_idea, pin_card, attach_card,
detach_card, approve_card, archive_card`

## SSE-Event-Envelope (F008; packages/orchestration/event_stream.py)
`{"seq": int, "ts": iso8601, "job_id": str, "type": str, "payload": {...}}`
Event-Typen (H2-Ontologie): `job.started, plan.task_created, run.started,
run.tool_call, run.token_delta, run.finished, task.state_changed,
artifact.created, decision.requested, decision.resolved, budget.tick,
job.finished, mission.job_linked`

## Modul-Landkarte (neu zu schaffende Dateien)
- packages/core/project_identity.py (F146) · apps/cli/golden.py (F147)
- packages/orchestration/{provider_timeouts, repair_attest, token_actuals,
  stream_evidence, worktrees, failure_postmortem, kill_switch, determinism,
  event_stream, command_gateway, flight_plan, scope_fences, loop_spec,
  long_run_executor, mission_state, idea_engine, dod_compiler, orchestrator_loop,
  mission_dossier, spec_sync, planner_calibration, vision_planner}.py
- packages/runtimes/dev_server.py (F007) · packages/verification/{visual_check,
  interaction_check, security_gate, mutation_probe}.py
- packages/memory/{cards, card_selection, card_value, harvesting, study}.py
- apps/ui/src/components/brain/{GrowingBrain.tsx, NodeGlyphs.tsx, BrainLegend.tsx,
  useSemanticZoom.ts, brainOntology.ts, useBrainStream.ts}
- apps/ui/src/components/{rail/AgentNowCard.tsx, rail/ActivityFeed.tsx,
  rail/TaskList.tsx, phasebar/PhaseTimeline.tsx, flightplan/FlightPlan.tsx,
  cards/CardCollection.tsx, diff/DiffViewer.tsx}

## Design-Tokens (aus docs/ui/design_reference/ux_design.png; apps/ui/src/styles/tokens.css)
```css
:root{
  --rm-bg:#E9EDF6; --rm-bg-2:#F3F6FC; --rm-card:rgba(255,255,255,.72);
  --rm-ink:#25324F; --rm-ink-2:#5B6B8C; --rm-line:#D7DEEF;
  --rm-accent:#4C6EF5; --rm-accent-deep:#3B5BDB; --rm-glow:#9DB8FF;
  --rm-open:#9775FA; --rm-planned:#C5CEE8; --rm-progress:#4DABF7;
  --rm-done:#38D9A9; --rm-warn:#F76707; --rm-live:#37B24D;
  --rm-r-card:18px; --rm-r-pill:999px;
  --rm-shadow:0 10px 30px rgba(59,91,219,.10),0 2px 6px rgba(37,50,79,.06);
  --rm-shadow-inset:inset 0 1px 0 rgba(255,255,255,.9);
  --rm-font:'Manrope','Inter',system-ui,sans-serif;
}
```
Labels: Uppercase, letter-spacing .12em, Farbe var(--rm-ink-2), 11px.
Karten: var(--rm-card) + backdrop-filter:blur(14px) + var(--rm-shadow).

## Verzeichnisse & Daten
- Projekt (im Repo): `.remedy/{config.toml, memory/cards/, ledger.md, STOP}`
- Global: `~/.remedy/{projects.json, projects/<pid>/{jobs/, cache/, ledger.sqlite}}`
- Evidence bleibt unter bestehender Struktur (`evidence/current/...`), + `project_id`-Feld.
