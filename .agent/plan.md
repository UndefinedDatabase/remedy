# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 6a93ee1c (R17 PASS).
Next free finding ID: R-0318. Open findings: 31 — 42 registered minus
11 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R18 closes T003 with the measurement the feature's DONE line asks
for. `_repair_payload_chars` computes what the full-file path WOULD
have sent for the same paths, the diff round records it beside the
`total_chars` it actually sent, and a large-file fixture test proves
the diff payload is a fraction of it. Per DECISION F111 D9 these are
CHARACTER counts, never tokens: this repository has no tokenizer.
T001, T002 and T003's prompt and apply halves are complete and gated.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md — the full
   suite, base against branch, with the five known base failures
   (R-0286) attributed rather than assumed.
2. The feature's documentation update, then closure under
   docs/roadmap/STATUS_closure_protocol.md: evidence job, FRESH
   review zip, the authored STATUS line, and the PR.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch and
  attributes every branch-only failure before any closure claim.
- The saving is measured in characters, not tokens. Any later doc or
  STATUS line that calls these numbers tokens turns an honest
  measurement into a fabricated one.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own, and R-0316's fix
  means a failed rollback is now reported rather than hidden.

Fortschritt: ~92 % (T001 ✅ · T002 ✅ · T003 ✅ komplett · Integration Gate
offen · Closure offen) — Schätzung
