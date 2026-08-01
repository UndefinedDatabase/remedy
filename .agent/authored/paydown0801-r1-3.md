<<<FROM docs/roadmap/STATUS_closure_protocol.md (exact block, occurs once)
**Evidence-dir commit ordering:** the evidence dir is committed
AFTER the READY zip exists, never before. A pre-committed
evidence dir puts evidence files into the base..HEAD review
subject and the package builds BLOCKED_EVIDENCE ("evidence is
not authoritative") — F147 attempt-2 lesson.
FROM>>>
<<<TO
**Evidence dir is not committed (DECISION 2026-08-01, settling the
F056 closure candidate "evidence-protocol drift"):** `.gitignore`
excludes `remedy-job-evidence-*/`, and the F050–F061 closures
committed no evidence dir. The durable pointer is the package name
+ SHA-256 + evidence job id in the STATUS line — exactly what every
closure since F050 records. Keep the dir outside the review subject
(session scratch is fine): a pre-committed evidence dir puts
evidence files into the base..HEAD review subject and the package
builds BLOCKED_EVIDENCE ("evidence is not authoritative") — F147
attempt-2 lesson.
TO>>>
