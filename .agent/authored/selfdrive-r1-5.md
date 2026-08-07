Target: docs/roadmap/STATUS_closure_protocol.md
Operation: replace FROM with TO. FROM occurs exactly 1x (verify first).

FROM
<<<FROM
   VerificationTests document yields `vt_passed = None`, which
   fails the final-verifier confirmation.
FROM>>>

TO
<<<TO
   VerificationTests document yields `vt_passed = None`, which
   fails the final-verifier confirmation.
   A fourth, from the F080 R4 attempt (94 rejected node ids, packaged
   BLOCKED_EVIDENCE): (d) a verification record can NEVER carry a
   FULL-SUITE node-id list. `len(node_ids) == selected` forbids
   filtering, and the packaging metadata scan correctly rejects the
   redaction-torture parametrizations whose ids embed fake secrets and
   absolute paths by design. The working shape: record the clean
   SCOPED suites in the bundle and let the full-suite proof ride in
   the committed integration-gate evidence and the reviewer's own
   re-run. The package still covers the accepted HEAD, and nothing
   green is claimed that was not run.
TO>>>
