# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 329-334: Final Ollama CLI truth fix, stop-reason JSON repair, docs contract closure.

## Completed
- stop_reason JSON corruption fixed (R-10001 resolved)
- Memory injection import fixed (N-10002 resolved)
- unsafe_path/path_traversal restored to docs (N-10001 resolved)
- Docs updated: pipeline overview, VRAM free, patch inspect/approve/reject/apply, test run
- do_cmd.py uses _BOOL_EVENTS whitelist, no blanket boolean conversion
- autorun.py memory uses correct module (context_summary), explicit degradation metadata
- 9 CLI path regression tests exercising real handler path
- Docs command contract validated against catalog
- Full baseline: 3886 passed, 7 skipped, Vitest 21, TypeScript clean, build OK

## Constraints
- No mutation endpoints, no shell=True, no 0.0.0.0
- UI remains read-only
- source_apply requires job + intent_id (approved) before mutation
- No unittest.mock in production packages
- Ollama only runs when explicitly requested via --builder-provider ollama
- Default provider is none (safe, deterministic)

## Remaining Risks
- Model quality varies by Ollama model
- Structured patch prompt may need further iteration
- Parser strictness: first-block-wins vs reject-multiple (documented)

## Recommended Next Block
If real Ollama path is now truthful:
  Steps 335-342 — Operator Cockpit v2
If Ollama output quality is poor:
  Steps 335-342 — Builder Prompt Quality And Parser Hardening
Alternative:
  Steps 335-342 — Event-Ledger Replay And Checkpoint Resume
