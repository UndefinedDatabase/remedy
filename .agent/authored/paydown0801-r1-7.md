
## 2026-08-01: paydown-0801 — closure-candidate carrier + two F056 candidates settled

Operator finding (accepted 2026-08-01): the two CANDIDATES parked at the
F056 closure were silently dropped by the next session — the
closure-candidate rule mandated a carry but defined no DISK vehicle;
candidates lived only in the closing session's chat brief, which a fresh
window never reads. Three DECISIONs, applied in a single-session
micro-round (round type per planner_reviewer_prompt.md §3), each
reversible by any later relay:

1. Disk vehicle: closure candidates are ALSO written to
   .agent/candidates.md inside the closure commit; the Window-1
   bootstrap reads it; a non-empty file at feature-claim time is a
   block condition. Amended: STATUS_closure_protocol.md
   (Closure-candidate findings) + planner_reviewer_prompt.md §1
   step 4. Alternative considered: keep brief-only carry — rejected,
   it is exactly what lost the F056 pair.
2. Evidence-protocol drift (F056 candidate a, resolved inline, no
   R-id spent): the protocol ordered an evidence-dir commit after the
   READY zip while .gitignore excludes remedy-job-evidence-*/ and the
   F050–F061 closures committed none. Amended the protocol to match
   standing practice: the evidence dir is NOT committed; the durable
   pointer is package name + SHA-256 + evidence job id in the STATUS
   line. Alternative considered: start committing evidence dirs —
   rejected: contradicts .gitignore, the F147 attempt-2 lesson, and
   six closures of precedent.
3. PR-number reporting (F056 candidate b, resolved inline, no R-id
   spent): handback_template.md "External actions" now states that PR
   create entries include the resulting PR number — settles the F056
   miss (that closure handoff omitted the PR number).
