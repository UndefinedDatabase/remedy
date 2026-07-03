---
description: Use at session start or after context reset. Reads AGENTS.md, plan.md, docs index, and git state to reconstruct working context. Enforces Session Resume protocol from AGENTS.md.
---

# Remedy Session Bootstrap Skill

## Session Resume Protocol (from AGENTS.md)

Run these steps in order at every session start:

### 1. Read Rules + State
```
Read: AGENTS.md
Read: .agent/plan.md
Read: docs/README.md (quick-find table for locating relevant docs)
```

### 2. For Roadmap Work, Also Read
```
Read: docs/roadmap/ROADMAP.md (Teil A — orchestrator protocol)
Read: docs/roadmap/features/T?_F???.md (active feature files only)
```

### 3. Git Context
```bash
git log --oneline -n 5
git diff main...HEAD
git status --short
```

### 4. Reconstruct + Continue
- Identify current step from plan.md
- Check if branch matches expected work
- Continue from current step

## Key Project Paths
- `apps/cli/` — CLI app
- `packages/orchestration/` — core orchestration
- `scripts/` — build/review scripts
- `tests/` — pytest suite
- `docs/` — system docs (index: `docs/README.md`)
- `.agent/` — runtime state (plan.md, live_review.md)

## If Plan Missing
Recreate `.agent/plan.md` before proceeding:
- Goal (what this branch does)
- Current Step
- Completed Steps
- Remaining Steps

## Common Test Commands
```bash
python3 -m pytest tests/ -q                     # full suite
python3 -m pytest tests/orchestration/ -q        # orchestration only
python3 -m py_compile <file>                     # compile check
ruff check <file>                                # lint
bash scripts/make_review_zip.sh                  # review zip
```
