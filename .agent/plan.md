# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

T001 and T002 are finished; T003 is running. Round 11 books round 10's PASS and
two reviewer slips, and migrates the `memory` group: nine refusal sites, six of
which say "memory card not found" and five of those byte-identically, so the
same condition now carries one token. Five of the six card commands carry no
`--json` in the catalog yet — they are in the set T003 empties at the end — so
their handlers are threaded and proved at the handler, and a guard test says so
out loud rather than leaving the reason to be inferred.

## Next Steps

1. T003 continues, by `sys.exit` site: `job` (44), `decision` (31), `project`
   (25), `brain` (24), `do` (19), `patch` (18), `grouped` (8), `test_cmds` (7),
   then the tail. Not in scope, and measured so: `integrity` and `ci` exit on a
   computed code with no message, which is not a pair.
2. `runtime_cmd.py` is its own round and is the hardest: 27 sites behind a
   local `_fail` prototype, exit codes 2 to 5, and an `error_class` key that is
   a contract with the supervisor SUBPROCESS and with `dev_server.py` — so it
   survives the migration rather than folding into the envelope's token.
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

Four rounds of this feature have now lost a number to the same cause: a value
measured before an edit and used after it. The counter-measure is in force from
round 11 — every number a block states about the tree comes from one script run
as the last action before emission — and the next round that states a numeral
it did not just generate is the one to watch.
