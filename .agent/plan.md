# Plan — Steps 1335-1364: Trusted Provider Patch Materialization v0

## Goal
Materialize ACCEPTED provider candidates into REAL applyable Repair Patch Intents
that flow through approval → `do continue` → snapshot → apply → test → proof, while
raw provider output + raw diffs stay PRIVATE. No provider execution, no network, no
auto-apply, no auto-approval. Apply only via existing `do continue`.

## Key constraint
Existing apply path (`apply_patch_intent`) is `.md`-only (create writes file, modify
appends a "Proposed Changes" section). So a materialized intent is genuinely
apply-compatible ONLY for a single `.md` target. Source/binary/delete/rename/multi-
file → `unsupported_patch_shape` (accepted_but_not_materialized; no intent).

## Current Step
1357 — full pytest once (post targeted green)

## Steps
- [x] 1335: Mainline reconciliation + clean branch (PR #57 merged; scope→1335-1364)
- [ ] 1336: Material models (Material/Entry/Result/Verification/IntentLink)
- [ ] 1337: Private material storage (0o700/0o600, atomic, hashed, no public raw)
- [x] 1338: verify_provider_patch_material (manifest/hash/paths/report-accepted/one-candidate)
- [x] 1339: unified diff → structured patch (modify/create text; no delete/rename/binary)
- [x] 1340: JSON structured_operations materialization (same restrictions)
- [x] 1341: applyable provider repair intent (real/resolvable/pending; linked; safe metadata)
- [x] 1342: approve + do_continue compatibility (existing apply path; snapshot mandatory)
- [x] 1343: trust report state updates (accepted/materialized/failed/pending/approved/applied/tested)
- [x] 1344: CLI provider material-show (+ optional materialize)
- [x] 1345: command catalog (material-show/materialize; no mutate/exec)
- [x] 1346: RunContract (provider_materialize_patch/create_provider_repair_intent)
- [x] 1347: RepairAttempt linkage (idempotent by candidate_hash; no dup)
- [x] 1348: Progress Ledger integration
- [x] 1349: Feature Planner integration (no auto approve/retry)
- [x] 1350: Review Bundle provider_material_summary.json
- [x] 1351: Cockpit read-only material counts
- [x] 1352: Retention policy docs
- [x] 1353: Redaction tests
- [x] 1354: CLI runtime tests
- [x] 1355: Architecture guards
- [x] 1356: Docs (materialization-v0 + cross-links)
- [ ] 1357: Targeted tests + full pytest once
- [ ] 1358: Live review
- [ ] 1359: PR discipline
- [ ] 1360: Product readiness update
- [x] 1361: Apply compatibility proof (approve→do continue fixture, snapshot, no overclaim)
- [ ] 1362: Integrity gate
- [ ] 1363: Final handoff
- [ ] 1364: Hard completion criteria

## Hard rules
- NO provider/Ollama/Claude SDK, NO network, NO subprocess, NO shell=True.
- Raw patch material ONLY in private workspace storage (0o700/0o600); NEVER public.
- No raw diff/source/stdout/stderr/artifact-body/secrets/tracebacks/abs paths public.
- Patch Intent exposes safe metadata only. Apply ONLY later via approved `do continue`.
- No auto-apply, no auto-approval. accepted ≠ materialized ≠ applied ≠ verified.
- Materialize ONLY supported shapes (single .md create/modify, bounded); else no intent.
- Idempotent by candidate_hash (no dup Fix Task / Repair Artifact / Intent).
- Every next safe action catalog-backed + entity-backed; no fake intent IDs.

## Next block
Provider-backed Repair Builder v0.
