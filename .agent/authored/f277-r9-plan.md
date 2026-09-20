# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

T001 and T002 are finished; T003 is running. Round 9 books round 7's PASS and
round 8's correct stop — the block carried a digest measured one edit before
the payload it described, and the worker refused to consume it — then lands
what round 8 was ordered to land: the five command groups whose handlers
already thread `json_output` end to end (`job context`, `worker`, `change`,
`blocker`, `contract`), one group per commit, 19 call sites. DECISION F277 D8
makes the error token a vocabulary rather than a free string, and records the
two `job context` messages that gain the `Error: ` prefix they alone lacked.

## Next Steps

1. T003 continues over the modules that need threading first, measured by
   `sys.exit` site: `job` (44), `decision` (31), `project` (25), `brain` (24),
   `do` (19), `patch` (18), `mission` (12), `memory` (9), `grouped` (8),
   `test_cmds` (7), then the tail. `runtime_cmd.py` is its own round: its local
   `_fail` prototype dies onto the shared helper, 27 sites, exit codes 2 to 5.
2. T003 closes with the catalog half: the 33 read-only commands that do not
   declare `supports_json` — `init run` and `dev status` among them, which
   honour `--json` and declare `False` — and the catalog test asserting the
   set is empty.
3. T004: the exit-code taxonomy under `docs/guides/`, asserted from the
   catalog rather than from prose; `tests/cli/test_json_contract.py` sweeping
   every `supports_json` command on success AND on an invalid argument; and
   the error-token vocabulary of D8 becoming a declaration a test reads.
4. Closure: the §3 checklist consolidation pass, where `R-1014`'s fix clause
   lands — merged into item 12, never appended; then the integration gate (the
   full suite, once), the evidence job, the review zip and the STATUS flip.

## Risks

The remaining T003 modules are the ones where threading `json_output` is real
work, and threading is where a behaviour change hides. Every group's round
carries a test proving the text branch is byte-identical to the line the CLI
printed before, and the reviewer red-proves the threading by pinning a call
site to `json_output=False`.
