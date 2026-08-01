<<<FROM docs/roadmap/STATUS_closure_protocol.md (exact block, occurs once)
   Build order (wording aligned with accepted F252/F050 practice,
   2026-07-30): the zip is built from a clean tree after all CONTENT
   commits — the reviewed head the manifest records as accepted HEAD.
   The evidence-dir commit and the final closure commit (STATUS/README/
   final .agent state) follow the READY zip. A package built from a
   dirty tree is invalid.
FROM>>>
<<<TO
   Build order (wording aligned with accepted F252/F050 practice,
   2026-07-30; evidence-dir rule per DECISION 2026-08-01): the zip is
   built from a clean tree after all CONTENT commits — the reviewed
   head the manifest records as accepted HEAD. The final closure
   commit (STATUS/README/final .agent state) follows the READY zip;
   the evidence dir itself is NEVER committed (see "Evidence dir is
   not committed" below). A package built from a
   dirty tree is invalid.
TO>>>
