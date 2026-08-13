# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 916b997e (R18 PASS).
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
T001, T002 and T003 are complete and gated. The build is done; what
remains is proving it against the whole repository and closing it.
R19 registered R-0318 and recorded the R18 gate so no finding lives
only in a session that has ended.

## Next Steps
1. Resolve R-0318 in the next round that touches builder_bridge.py
   for another reason. Do not open a round for it alone.
2. Integration gate per docs/agents/integration_gate.md: full suite
   with `-n auto`, base against branch, every branch-only failure
   attributed rather than assumed (R-0286: five known base failures).
3. The feature's documentation update, registered in docs/README.md
   in the same PR.
4. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job,
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

Fortschritt: ~93 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration Gate offen ·
Doku offen · Closure offen) — Schätzung
