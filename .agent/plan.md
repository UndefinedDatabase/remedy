# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

T001 and T002 are finished; T003 is running. Round 10 books round 9's PASS and
migrates the `mission` group — twelve refusal sites, two of them in the helpers
`_resolve_project_id` and `_load_mission_or_exit` that eight mission commands
AND `mission contract` share, so threading them reaches two modules. DECISION
F277 D9 rules how a catch-all exception is tokenised: `mission_error`, named
for the layer that refused, because `MissionError` carries a dozen conditions
distinguished only by prose and inventing one would be a parser over it.

## Next Steps

1. T003 continues, by `sys.exit` site: `job` (44), `decision` (31), `project`
   (25), `brain` (24), `do` (19), `patch` (18), `memory` (9), `grouped` (8),
   `test_cmds` (7), then the tail. Not in scope, and measured so: `integrity`
   and `ci` exit on a computed code with no message, which is not a pair.
2. `runtime_cmd.py` is its own round and is the hardest: 27 sites behind a
   local `_fail` prototype, exit codes 2 to 5, and an `error_class` key that
   is a contract with the supervisor SUBPROCESS and with `dev_server.py` — so
   it survives the migration rather than folding into the envelope's token.
3. T003 closes with the catalog half: the 33 read-only commands that do not
   declare `supports_json`, and the catalog test asserting the set is empty.
4. T004: the exit-code taxonomy under `docs/guides/`, asserted from the
   catalog; `tests/cli/test_json_contract.py` sweeping every `supports_json`
   command on success AND on an invalid argument; and the token vocabulary of
   D8 and D9 becoming a declaration a test reads.
5. Closure: the §3 consolidation pass, where `R-1014`'s fix clause lands —
   merged into item 12, never appended; then the integration gate (the full
   suite, once), the evidence job, the review zip and the STATUS flip.

## Risks

A migration that threads a flag into a helper another MODULE imports changes
nothing for that module until its own call sites are threaded too. Round 10's
first mutation set left both of `contract_cmd.py`'s threaded arguments green
and the covering tests were added before emission; every later round touching
a shared helper red-proves each importing module separately.
