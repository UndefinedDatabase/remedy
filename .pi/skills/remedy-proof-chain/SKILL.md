---
name: remedy-proof-chain
description: Use for Remedy proof_chain, file_provenance, change_set, file why, change proof, and proof_status work.
---

# Remedy Proof Chain

## Checklist
1. Read `AGENTS.md`, `.agent/plan.md`, and `.agent/live_review.md`.
2. Verify the current reviewer status before claiming PASS.
3. Preserve Proof Chain truth:
   - not tested never verifies
   - unlinked generic tests never verify multi-change jobs
   - sole-change generic tests require test time at or after apply time
   - unknown ordering is incomplete
   - explicit `test_not_required` must be intent-linked
4. `file why` and `change proof --path` must agree on `proof_status`.
5. File provenance must not show unlinked/global tests as proof.

## Tests
Use `scripts/remedy_pytest.sh` with targeted proof/file/CLI tests.
