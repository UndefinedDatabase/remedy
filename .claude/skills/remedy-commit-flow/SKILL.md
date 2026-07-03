---
description: Use for Remedy commit and PR workflow. Enforces AGENTS.md commit gate, self-review loop, plan.md sync, Open PR Gate, and push discipline.
---

# Remedy Commit Flow Skill

## Pre-Work Gate (Open PR Gate)
Before creating branch or starting new task:
```bash
gh pr list --state open --json number,headRefName,baseRefName,isDraft
```
- 0 open PRs → proceed
- 1 non-draft feature/* → main → merge first: `gh pr merge <n> --merge --delete-branch`
- Multiple / draft / non-main target → STOP, report

## Branch Rules
- Always `feature/<short-kebab-description>`
- Never work on main
- Never mix unrelated features in same branch
- If >500 line diff → split before committing

## Commit Gate Checklist (before EVERY commit)
1. `.agent/plan.md` reflects current work (update if not)
2. Self-review: `git diff --stat && git diff`
   - No bugs, debug leftovers, broken imports, formatting noise
   - No unrelated changes or scope drift
   - Diff matches plan
3. Check if `docs/` needs update
4. Check if `.agent/context.md` or `.agent/decisions.md` need update

## Commit Style
- Small, logically scoped (one step per commit)
- Clear messages explaining WHY not just WHAT
- Never mix refactoring with features
- Stage specific files (no `git add -A`)

## After Commit
```bash
git push -u origin <branch>
```

## PR Creation
```bash
gh pr create --title "<short title>" --body "$(cat <<'EOF'
## Summary
- bullet points

## Test plan
- [ ] verification steps

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## State Files
- `.agent/plan.md` — goal, current step, completed steps, remaining (<50 lines)
- `.agent/context.md` — scope boundaries, assumptions, constraints
- `.agent/decisions.md` — non-obvious implementation choices
- Rewrite plan.md, don't append. Remove completed items.
