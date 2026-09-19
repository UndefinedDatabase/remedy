
## DECISION F273 D3 (2026-09-19, reviewer, round 3) — T003 closes on one clause and a deletion; T016 renders the run state as its value on every interpreter, reads the ledger through its canonical reader, and emits tombstones both producers agree on
CONTEXT: T2_F273.md orders T003 (R-0396, R-0445, R-0645, R-0736) and T016 (items (a) and (b) mint
their ids at the round that takes them; (c) is R-0839). Measured by the reviewer at `a5e3b9ce`:
`docs/agents/integration_gate.md` no longer holds a base run or a parity copy since `e1686236`
(amend0917-throughput), so R-0396, R-0445 and R-0736 describe a recipe that is gone, while step 1
still turns one run's FAILED list into the branch's failure set without saying so (R-0645). T016
(a), (b) and (c) are live as the ledger's R-0984, R-0985 and R-0839 describe, and building (c) found
R-0983: the provider-run producer's tombstones are dicts the strict schema refuses.
CHOSEN: (1) T003. Step 1 of `docs/agents/integration_gate.md` gains one clause: the FAILED list is
one run's sample, an empty one is evidence and never proof, and a node a later run finds red is
attributed by step 3. R-0396, R-0445 and R-0736 are resolved by that deletion, not by a new clause.
(2) T016 (a). `RunState` gains `__str__` returning its value; `ArtifactKind`, the file's other
`(str, Enum)`, stays out because no renderer formats a member of it. A guard asserts `str()`,
`format()` and the f-string of every member equal its value, which is red on 3.10 at the base,
since `str()` there reads `RunState.X`. The `ci` job of `.github/workflows/ci.yml` becomes a matrix
over `'3.10'` and `'3.12'` with `fail-fast: false`, pinned by a test in
`tests/orchestration/test_ci_workflow.py`. The 3.12 column's colour exists only on hosted CI, which
runs on a pull request into `main`: R-0984's resolution reads it on F273's closure pull request.
(3) T016 (b). `scripts/rotate_live_review.py` becomes the ledger's one reader: `open_finding_ids`
(registered ids minus ids with at least one `Done:` line, sorted), `count_open_findings` as its
length, and `latest_gate_verdict` (the first `VERDICT <TOKEN>` of the last `Gate:` record whose
token is one of PASS, PASS_WITH_RISKS, FAIL, NEEDS_REPAIR, BLOCKED; `absent` or `unparsed`
otherwise). The rotation's before-and-after equality is kept and now counts distinct ids.
`scripts/build_review_manifest.py` loads that sibling file by path, because `scripts` is a namespace
package another installed checkout could answer for, and the review-packaging tests that copy the
pipeline scripts into a temporary repository copy it too; it leaves `ALLOWED_UNWIRED` in
`tests/test_no_orphan_modules.py` now that a script imports it. The manifest tests that pinned the
dead `## Verdict (reviewer-owned)` format are rewritten to the `Gate:` format, and one reads the
real ledger. (4) T016 (c), R-0839. `create_manual_completion_bundle` writes a tombstone
`path -> base_sha256` for each deleted attestable path. Because a tombstone joins the proof's
authority set, the packager's `_assert_authority_equality` now binds every tombstone to a deleted
subject path with the same base blob and holds the subject, final-verifier and change-provenance
coverage sets to the LIVE authority, and the manifest's manual-completion union and gate-matrix
`proof_authority` read `file_hashes` only; without that, emitting the tombstones R-0839 orders
would refuse every deletion package R-0837 made packageable. (5) R-0983. `export_job_evidence`
writes the same `path -> base_sha256` shape and refuses the proof when a deleted path carries no
base blob, since no honest tombstone exists for it; the manual producer skips such a path instead,
a case neither producer can reach from a coherent review subject, left as it is.
ALTERNATIVES: a new clause in the deleted parity step, rejected because nothing runs it; `__str__` on
`ArtifactKind` too, rejected for want of a renderer; importing `scripts.rotate_live_review` by
package name, rejected because an editable install elsewhere answered for it in a measured run; a
tombstone kept out of the authority set, rejected because `ContentProofV1.authority_paths()` is
defined as the union and R-0839 names it; requiring a tombstone for EVERY subject deletion,
rejected because bundles written before this carry `{}` and would be refused.
REVERSE: restore `integration_gate.md`, `ci.yml`, `models.py`, `rotate_live_review.py`,
`build_review_manifest.py`, `build_review_zip.py` and `job_evidence.py` from `a5e3b9ce`, drop the
tests this round added or rewrote, and delete this paragraph.
