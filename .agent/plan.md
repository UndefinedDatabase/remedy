# Plan — F111 Diff-only repair (CLOSED)

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Last reviewed SHA: 35329dec (R21 PASS, integration gate). Next free
finding ID: R-0320. Open findings: 32 — 44 registered minus 12
resolved. None is High; each is an accepted risk at closure.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md). DONE.

## Current Step
Closed. T001, T002 and T003 are complete and gated; the ist-doc
`docs/system/diff-only-repair-v1.md` is registered in docs/README.md;
the integration gate in `.agent/gate_f111_r21/` shows zero branch-only
failures against the merge base; STATUS.md carries the `[x]` line and
the closure PR is open and UNMERGED by design.

## Next Steps
1. The closure PR merges at the NEXT feature's start via the AGENTS.md
   Open PR Gate — that gap is the operator's manual-review window. The
   operator may also merge it manually at any time.
2. Next feature per Rule A5 and STATUS order: F115 — Prompt breakdown
   & cost report. New session, new branch, nothing carried over but
   `.agent/candidates.md`.
3. That first reviewed round MUST register or resolve every entry in
   `.agent/candidates.md` and empty the file
   (docs/roadmap/STATUS_closure_protocol.md).

## Risks
- The suite is RED at the merge base with five known ids (R-0286),
  unrelated to F111 and unfixed here on purpose.
- The saving is measured in CHARACTERS, not tokens (DECISION F111 D9).
- All-or-nothing rests entirely on source_apply's durable snapshot;
  a failed rollback is reported, not hidden (R-0316).

Fortschritt: 100 % (T001 ✅ · T002 ✅ · T003 ✅ · Doku ✅ ·
Integration Gate ✅ · Closure ✅) — Schätzung
