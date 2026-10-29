# Review Scope — d683a4014c3d4cb1: Replace hand-built (i) with InfoButton in Memory.tsx: Remove the local info/setInfo state, Sheet import, and hand-built (i) button element from Memory.tsx, and render the shared InfoButton component in their place, with an aria-label key that matches the naming pattern used by every other InfoButton in the app.

**Recommended scope:** `cross_file`

_4 files changed with import/call relationships._

## Summary

| Field | Value |
| --- | --- |
| Schema version | 1.0.0 |
| Changed files | 4 |
| Repair rounds | 0 |
| Tests | not run — 0 passed, 0 failed |
| Open findings | 0 |
| Est. review tokens | 3607 |

## Changed Files

### `src/screens/KnowledgeNet.tsx`
- Line ranges: 15–21, 157–166, 244–250
- Symbols: `KnowledgeNet`
- Risk tags: `new_function`

### `src/screens/Memory.tsx`
- Line ranges: 26–32, 52–58, 282–287, 346–353, 377–385
- Symbols: `infoButton`
- Risk tags: `new_function`

### `src/screens/net/NetHeader.tsx`
- Line ranges: 5–17, 19–25, 30–36, 49–55, 64–70
- Symbols: `NetHeader`, `others`
- Risk tags: `new_function`

### `src/styles/knowledge-net.css`
- Line ranges: 231–242
- Symbols: —
- Risk tags: —

## Related Tests

_None found._

## Open Findings

_None._

## Evidence

- `task_runs/d683a4014c3d4cb1/safe.diff`
- `task_runs/d683a4014c3d4cb1/tests.txt`
- `task_runs/d683a4014c3d4cb1/review.json`
- `task_runs/d683a4014c3d4cb1/repair_loop.json`

Prompt hashes: `9ce4d4894ec3d0d60fea9eb1f0775e40f8875e0571df61c275cf4916c15c0015`, `d1bbfdc4f85ca351b5e42c8f94b41225857e138e8dd8a5ec72c3721a8f70b02f`
