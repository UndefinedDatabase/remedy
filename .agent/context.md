# Context

## Active Branch
feature/steps-74_1-79-ux-precision

## PR
#33 (open — covers Steps 74.1-100)

## Scope
Steps 91-100: Directional Semantic Brain UX + Live Autorun + Autocoder Foundation.

New files:
- packages/orchestration/autorun.py (remedy do orchestrator)
- packages/orchestration/source_context.py (dynamic file selection for builder)
- packages/orchestration/structured_patch.py (file_ops/unified_diff parser)
- packages/orchestration/source_apply.py (safe patch application)
- apps/cli/commands/do_cmd.py (remedy do CLI handler)
- tests/test_steps_91_100.py (48 tests)

Modified:
- packages/orchestration/ui_view_model.py: v2 schema, ELK layout, 7 zoom levels, explainable edges
- packages/orchestration/ui_server.py: live-state, events-since endpoints
- packages/orchestration/timeline.py: append_run_event convenience function
- apps/ui/src/brain/renderer.ts: HTML overlay labels, arrowheads, edge hover, live merge
- apps/ui/src/brain/detail.ts: v2 compact card (title, status_text, why_this_matters, evidence, copy_command)
- apps/ui/src/main.ts: v2 types, live polling, edge tooltip
- apps/ui/index.html: edge tooltip element, compact detail styling
- apps/ui/package.json: elkjs replaces d3-force
- apps/cli/command_catalog.py: do group + do.run command
- apps/cli/commands/__init__.py: do_cmd import
- apps/cli/grouped.py: --repo, --dry-run, --fixture-builder, --ui arg handlers
- tests/test_steps_83_90.py: updated for v2 schema compatibility

## Key facts (Steps 91-100)
- View model v2: layout_engine=elk-layered, direction=RIGHT, 7 zoom levels (0-6)
- _ZOOM_NAMES replaces _LAYER_NAMES (7 entries)
- Nodes have x/y directly (not nested position dict), rank, zone, is_origin, is_primary_chain, is_attention
- Edges have kind, label, meaning, is_primary_chain, strength, direction
- Node detail v2: title, status_text, why_this_matters, evidence_summary, next_safe_action, copy_command, advanced
- Live state: view_model_hash for change detection, events-since with cursor
- Autorun: autonomy levels 0-7, dry-run mode, fixture builder
- Source context: deny lists, budget-aware, 3-level walk
- Structured patch: JSON file_ops, unified diff, narrative fallback
- Source apply: path safety (traversal, symlink, deny list), snapshot/revert, no delete in v1
- 2994 tests pass
