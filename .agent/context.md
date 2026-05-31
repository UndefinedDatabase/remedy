# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 247-252: Data-Honest Mission Control Contract.

Core principle: "truth before beauty" — no fake tasks, no synthetic live state, no invented metrics.

## Key Changes

### Step 247: Repo + handoff truth hygiene
- Fix stale .agent/context.md (was referencing Steps 91-100)
- Update .agent/plan.md for new step range

### Step 248: Dashboard truth contract v1
- Add `source_kind` (real | derived | placeholder) to dashboard fields
- Add `synthetic_count` to dashboard response
- Add `demo_mode` flag
- Honest defaults when data missing

### Step 249: No-fake UI state pass
- Remove DISPLAY_ROWS fake tasks from TaskChecklistCard.tsx
- Show honest empty state when no real tasks
- Fix optimistic live state in AgentNowCard

### Step 250: Real graph source contract
- Add `source_kind` to ForceBrainNode (real_brain | layout_only | demo_fixture)
- Particle nodes explicitly marked layout_only
- Graph model distinguishes real vs synthetic

### Step 251: Event ledger → live activity
- Derive activity feed from real run-log events
- Honest idle/stale states instead of fake "Builder is working"

### Step 252: Operator summary + smoke alignment
- `remedy job summary` CLI command
- Smoke assertions for truth contract fields
- Test coverage for data-honesty invariants

## Constraints
- No backend mutation endpoints
- No CDN/external deps
- No shell=True, no 0.0.0.0
- React 19 + TypeScript + MUI + CSS Modules
