# Plan — Process-hardening v3 (relay ergonomics, R1)

## Goal
Persist the five PH v3 operator rulings (2026-07-28) into the process
docs: planner paste-block output format, worker duplicate-block guard
(.agent/last_block.md), docs-round gate for docs/roadmap/** changes,
handback write-once rule, and the authored-state contract rule
(## Steps in live_review, ## Goal + ## Next Steps in plan). Docs only.

## Next Steps

- [ ] Open PR Gate: merge PR #158 (F251), main pulled clean
- [ ] Branch chore/process-hardening-v3
- [ ] Commit A: authored files + live_review (phv3-r1-7) + this plan
      (phv3-r1-8) + .agent/last_block.md written (first use of the
      new guard, self-applied)
- [ ] Commit B: planner_reviewer_prompt.md — §2 paste-block format
      (r1-1), §3 docs-round gate (r1-2), §4 authored-state contract
      rule (r1-3)
- [ ] Commit C: split_workflow.md — duplicate-block guard (r1-4) +
      worker bootstrap bullet (r1-5)
- [ ] Commit D: handback_template.md — write-once rule (r1-6)
- [ ] Verify: containment proofs; the four .agent contract tests
      green (live_review + plan now carry the required substrings);
      canary; docs-only diff
- [ ] Push, PR into main (NOT merged until the reviewer's PASS),
      handback per template — drafted in scratchpad, written once

## Risks
- Docs only: any non-docs diff besides .agent/ bookkeeping is scope
  drift — stop and report.
- AGENTS.md wins on any conflict — STOP and surface, never weaken.
