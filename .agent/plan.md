# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 1e90e89f (R20 PASS).
Next free finding ID: R-0320. Open findings: 32 — 44 registered minus
12 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
T001, T002 and T003 are complete and gated, and the ist-doc
`docs/system/diff-only-repair-v1.md` is registered in docs/README.md.
R21 ran the integration gate: the full suite on the branch against the
full suite at the merge base, with every branch-only failure attributed
by evidence in `.agent/gate_f111_r21/`.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: the evidence
   job, a FRESH review zip (a zip failure is a closure blocker), the
   reviewer-authored STATUS line committed LAST on the branch, then
   the PR — which is NOT merged in that session.
2. Nothing else. Any new work is a new feature and a new branch.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286), so the gate compares base against branch and never reads
  a red branch run as a branch defect on its own.
- The saving is measured in CHARACTERS, not tokens (DECISION F111
  D9). Any doc, STATUS line or PR body calling them tokens turns an
  honest measurement into a fabricated one.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own, and R-0316's fix
  means a failed rollback is now reported rather than hidden.
- 32 findings stay open at closure, none above Medium, each carried
  as an accepted risk exactly as F107 carried its own.

Fortschritt: ~98 % (T001 ✅ · T002 ✅ · T003 ✅ · Doku ✅ ·
Integration Gate ✅ · Closure offen) — Schätzung
