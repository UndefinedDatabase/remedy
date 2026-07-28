# Plan — Planning amendment: flake-debt reorder + F070/F075 corpus (R1)

## Goal
Persist three operator decisions (2026-07-27) into the roadmap docs so
the plan carries them itself: register F251 (full-suite stabilization)
as the next open item before F050; add the ledger-fixture corpus and
integrity-pattern requirements to T1_F070.md; add the corpus inheritance
rule to T1_F075.md. Docs only — no production code, no tests, no
process-doc changes.

## Checklist
- [ ] Open PR Gate: merge PR #156 (F048), main pulled clean
- [ ] Branch chore/plan-amendment-flake-debt from main
- [ ] Commit A: authored files saved + live_review.md reset (r1-1)
- [ ] Commit B: docs/roadmap/features/T1_F251.md created (r1-2)
- [ ] Commit C: STATUS.md F251 line before F050 (r1-3) + ROADMAP.md
      Tier-1 entry after F048 (r1-4)
- [ ] Commit D: T1_F070.md Design (r1-5) + Acceptance (r1-6) additions
- [ ] Commit E: T1_F075.md Acceptance addition (r1-7)
- [ ] Verify: byte-identity proofs per authored file; docs-only diff
      vs main; canary tests/cli/test_golden_path.py
- [ ] Push, PR into main (NOT merged), handback per template

## Current Step
Apply in order; every authored text via .agent/authored/ with sha256
check BEFORE committing.

## Risks
- Docs only: any non-docs diff is scope drift — stop and report.
- STATUS.md grammar is parsed later by F080: exactly one new line, no
  other line touched.
- ROADMAP.md edit is operator-authorized for this ordering entry only.
