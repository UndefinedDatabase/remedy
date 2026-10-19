# Plan — agent-state data hygiene

## Goal
Keep development-only `.agent` content out of review packages and reject newly staged sensitive
agent-state additions before commit; preserve required workflow state and Git history. This is
outside the roadmap queue; F078 remains next.

## Current Step
Complete: implementation, review, final fast gate, push, and PR 367.

## Next Steps
- Operator: review PR 367.
- Operator: decide separately whether a coordinated history rewrite is warranted; this change keeps
  historical records out of new packages without rewriting them.

## Risks
- Historical committed records remain in Git history and cannot be rewritten under current rules.
- Required append-only workflow records cannot be destructively sanitized; prevention applies to new
  staged lines, while package exclusion prevents their distribution.
