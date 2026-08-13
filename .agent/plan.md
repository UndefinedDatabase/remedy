# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: ed7eaeef (R19 PASS).
Next free finding ID: R-0319. Open findings: 32 — 43 registered minus
11 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
T001, T002 and T003 are complete and gated. R20 shipped the feature's
ist-doc `docs/system/diff-only-repair-v1.md`, registered it in
docs/README.md, cleared R-0318 and recorded the R19 gate. What remains
is proving the build against the whole repository and closing it.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md: full suite
   with `-n auto`, base against branch, every branch-only failure
   attributed rather than assumed (R-0286: five known base failures).
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job,
   FRESH review zip, the authored STATUS line committed last, the PR
   created and NOT merged in that session.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- The saving is measured in CHARACTERS, not tokens (DECISION F111
  D9). Any doc, STATUS line or PR body calling them tokens turns an
  honest measurement into a fabricated one.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own, and R-0316's fix
  means a failed rollback is now reported rather than hidden.
- 32 findings stay open at closure, none above Medium, each carried
  as an accepted risk exactly as F107 carried its own.

Fortschritt: ~95 % (T001 ✅ · T002 ✅ · T003 ✅ · Doku ✅ ·
Integration Gate offen · Closure offen) — Schätzung
