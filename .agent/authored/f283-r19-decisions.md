
DECISION F283 D11 (2026-09-22, round 19) — TWO SHAPES DECISION F283 D10 DID NOT RULE, TAKEN AS
ROUND 18 TOOK THEM.

CONTEXT. Round 18 met two cases D10 names no rule for, and its worker decided both and declared
them. First, `SnapshotProof.to_dict()` in `packages/orchestration/real_test_execution.py` carries
its own `schema_version`, the record schema's version string, which collides by name with the
envelope's reserved key, so `emit_ok` refuses the document as it stands. Second, `patch revert
--json` on a revert that was refused or failed names its condition through the result's
`block_reason`, else its terminal `state`, and not through one fixed token; measured at
`5d1510ca`, the `block_reason` values are string literals the revert path of
`packages/orchestration/repository_snapshot.py` sets, among them `no_apply_record`,
`no_snapshot`, `permission_denied`, `contract_denied`, `verify_failed` and `post_apply_drift`.

CHOSEN. (1) A document key that collides with one of the envelope's reserved keys,
`schema_version` or `ok`, is renamed with the prefix `record_`, so `record_schema_version` and
`record_ok`, by one helper in the module that writes the document, and its value is unchanged.
This is the one place a D10 conversion is not additive, because the envelope's own key is the
contract every consumer is entitled to assume. (2) Where a module already names a failure
condition in a closed set of literals of its own, that literal is the token: `patch revert`
passes its `block_reason`, else its `state`, else `revert_failed`. DECISION F277 D8 rules that a
token is named for the condition, and those literals are the condition's name.

ALTERNATIVES. Nest the snapshot record under one key — rejected: it breaks every reader of the
record's other keys to save one. Drop the record's version string — rejected: it removes
information a reader may use. One fixed `revert_failed` token for every failed revert —
rejected: it discards the condition the module already names.

REVERSE by deleting this paragraph and restoring `_envelope_safe` in
`apps/cli/commands/real_test_execution_cmd.py` and `_cmd_revert_patch_intent` in
`apps/cli/commands/patch.py` from git history at `9f36956f`.
