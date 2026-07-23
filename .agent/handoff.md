# Handoff — latest worker state (rewrite, never append)
Feature: roadmap learnings + closure-loop fixes (gap work after F081)
Round: Part 1 DONE
Branch: feature/roadmap-learnings-and-loop-fixes
Base: 364e356 (main after PR #139 F081 merge)
HEAD: f7f01af

Commits on branch:
  b3c8971  docs(roadmap): enrich feature specs with F081 learnings (E1-E6)
  622d59f  feat(workflow): add build-remedy-large and review-remedy-large commands (E7)
  f7f01af  docs(workflow): close F081 communication holes (E8-E12)

Edits applied (E1-E12):
  E1 F105 stale-fact (conventions v1 exists, not "extract")
  E2 F075 host-state isolation criterion (earned F081)
  E3 F053 milestone distance + momentum + capability lines
  E4 F227 golden seed provenance (split-workflow prompts)
  E5 F034 conditional answers (predicated resolutions)
  E6 F070 split-workflow back-pointer
  E7 build-remedy-large + review-remedy-large commands + decisions entry
  E8 handoff carries OUTCOMES (split_workflow.md + bootstrap block)
  E9 reviewer audits handoff as return channel (planner_reviewer_prompt)
  E10 canonical producer + deadlock rule + zip outcome (closure protocol)
  E11 commit-subject hygiene (AGENTS.md)
  E12 history-rewrite safe sequence (split_workflow.md Session hygiene)

SKIPs: none (all 12 edits applied; no pre-existing coverage found)

Open findings: 0
Next: PR create + operator-instructed merge, then Part 2 scanner fix
(Rules: rewritten at every handback; ≤60 lines.)
