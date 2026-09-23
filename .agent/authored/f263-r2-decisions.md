
DECISION F263 D2 (2026-09-23, round 2) — A HUMAN CHANGE RECORD IS A READY GATE OF THE REVIEW
PACKAGE: THE BUNDLE CARRIES EVERY RECORD, VERIFIES THE COPY, AND A RECORD THAT DOES NOT VERIFY
BLOCKS.

CONTEXT. T2_F263.md's Design gives the record "the same standing as any other evidence
artifact". Measured by the reviewer at `a34cc4b0`: the export (`job_evidence.export_job_evidence`)
copies nothing from `jobs/<id>/evidence/human_changes/`, so a package never shows the human's
edit. The bundle has two integrity artifacts of the same kind — `postmortem_integrity.json` and
`manifest_integrity.json`, each carrying `ok` and a `failures` list — whose failures the final
verifier turns into BLOCKED, and `scripts/build_review_manifest.py` requires both as closed-schema
READY gates. The closure's own producer, `manual_attestation.build_manual_completion_gates`,
writes both with empty failure lists.

CHOSEN. (1) `human_change.export_human_change_records` copies each record and its diff into
`human_changes/` of the bundle and runs `verify_human_change_record` on the COPY, the bytes a
reviewer reads; `export_job_evidence` writes the result as `human_change_integrity.json`,
`{schema_version, ok, records, failures}`, where `records` names every record id and each failure
is one string naming its record. A job with no record exports an intact empty set. (2) The final
verifier reads the file, reports `human_change_integrity_blocked`, and a non-empty failure list
makes the verdict BLOCKED, exactly as the two integrity artifacts above do. (3) The review
manifest adds the file to its ok-gates with a closed schema, adds the new verifier field to the
verifier's closed field set and schema, and requires it to read false for READY. (4) The manual
completion producer writes an intact empty set, so a closure package stays READY. (5) The
closure protocol's list of the gates that producer emits names the new one. (6) The review zip's
early binding list is left alone: its loader binds any gate on first read, so the entry would
change nothing a test or a package can observe.

ALTERNATIVES. Fold record failures into `postmortem_integrity.json` — rejected: that file means a
post-mortem could not be written, and a reader of a BLOCKED package would be sent to the wrong
place. Verify the records in the job's own evidence directory rather than in the bundle —
rejected: the bundle is what a reviewer reads, and a copy that went wrong would pass. Make the
file optional for READY — rejected: an absent integrity file would read as intact.

REVERSE by deleting this paragraph and `tests/orchestration/test_human_change_evidence.py`,
removing `export_human_change_records` and `INTEGRITY_FILE` from
`packages/orchestration/human_change.py`, the export block in
`packages/orchestration/job_evidence.py`, `human_change_integrity_blocked` from
`packages/orchestration/final_verifier.py`, the file's lines in
`packages/orchestration/manual_attestation.py` and `scripts/build_review_manifest.py`, the two
fixture lines in `tests/orchestration/test_review_authoritative_e2e.py` and
`tests/orchestration/test_review_package_status.py`, and the name in
`docs/roadmap/STATUS_closure_protocol.md`.
