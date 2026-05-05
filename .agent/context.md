# Context

## Active Branch
feature/step19-approval-queue-v1

## PR
(open — see GitHub)

## Scope
Step 19: Approval Queue v1 — metadata-only approval decisions for patch intents.
Read-only: no repo files modified. No apply step implemented.

New files:
- packages/orchestration/approval_queue.py: list_patch_intents, get_patch_intent,
  set_approval_state, make_intent_id, format_intent_list, format_intent_detail
- tests/test_patch_intent_approval.py: 57 tests

Modified:
- apps/cli/main.py: 4 new commands + subparsers + dispatch
- packages/orchestration/cockpit.py: approval-aware attention + next action
- docs/architecture.md: Approval Queue v1 section

## Key facts
- Approval states: pending (default), approved, rejected. Latest decision wins.
- Intent ID format: "<artifact_short_id>-<idx>" (e.g. "a1b2c3d4-0")
- Storage: artifact.metadata["patch_intent_approvals"][intent_id] → approval dict
- Run log events: patch_intent_approved / patch_intent_rejected
  Metadata: intent_id, target_path, risk, reason_present (bool). NO raw reason text.
- Invalid stored risk coerced to RISK_UNKNOWN — never propagated silently.
- Cockpit: pending approval + medium/high/unknown risk → attention item.
  All approved + no pending tasks → next action notes apply not implemented.
- 826 tests pass
