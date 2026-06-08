---
description: Use for Remedy Proof Chain, file provenance, change proof, and proof_status work. Enforces linked evidence and no-overclaim rules.
---

# Remedy Proof Chain Skill

Use this skill when changing or reviewing:
- `packages/orchestration/proof_chain.py`
- `packages/orchestration/file_provenance.py`
- `packages/orchestration/change_set.py`
- `apps/cli/commands/change.py`
- `apps/cli/commands/file.py`

## Required workflow
1. Read `AGENTS.md`, `.agent/plan.md`, and `.agent/live_review.md` first.
2. Treat reviewer findings as authoritative until resolved in code and tests.
3. Preserve the truth rule: a change is verified only with approval + apply + proof + linked passed/not-required test evidence.
4. Generic tests link only for a sole applied change and only when the test timestamp is at or after apply.
5. Unknown timing is incomplete, not verified.
6. `file why` must agree with `change proof --path` and must not display unlinked/global tests as proof.

## Safety
- No raw diffs, artifacts, source content, stdout/stderr, command output, or secrets in final summaries.
- No direct pytest; use `scripts/remedy_pytest.sh`.
