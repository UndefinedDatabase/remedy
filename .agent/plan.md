# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

T001 and T002 are finished. Round 7 books round 6's PASS and opens T003: the
shared `fail(error, message, *, json_output, exit_code=1, **payload)` in
`apps/cli/json_envelope.py`, and the first two command groups migrated onto it
— `event` and `file`, which are the two whose handlers already thread
`json_output` end to end, so the migration is the pairs themselves and nothing
else. DECISION F277 D7 fixes the helper's parameter spellings and records that
T003's planning numbers are stale: 145 commands, not 339; 33 read-only without
`supports_json`, not 49; 237 `print(...); sys.exit(...)` pairs across 28 files.

## Next Steps

1. T003 continues, one command group per commit, over the remaining 26 files:
   the large groups (`job`, `decision`, `project`, `brain`, `do`, `patch`) are
   a round each, the small ones bundle. `runtime_cmd.py`'s local `_fail`
   prototype is deleted onto the shared helper in that group's own round.
2. T003 closes with the catalog half: the 33 read-only commands that do not
   declare `supports_json` — including `init run` and `dev status`, which
   honour `--json` and declare `False` — and the catalog test that asserts the
   set is empty.
3. T004: the exit-code taxonomy under `docs/guides/`, asserted from the
   catalog rather than from prose, plus `tests/cli/test_json_contract.py`
   sweeping every `supports_json` command on success AND on an invalid
   argument, with catalog-to-dispatch parity in the same file.
4. Closure: the §3 checklist consolidation pass, which is where `R-1014`'s fix
   clause lands — merged into item 12, never appended, because the list may
   not grow; then the integration gate (the full suite, once), the evidence
   job, the review zip and the STATUS flip.

## Risks

T003 is the largest slice of this feature and its size was measured only in
round 7: 237 call sites. A round that migrates a group whose handlers do NOT
already thread `json_output` has to thread it first, and threading is where a
behaviour change can hide — so each group's round carries at least one test
proving the text branch is byte-identical to the line the CLI printed before.
