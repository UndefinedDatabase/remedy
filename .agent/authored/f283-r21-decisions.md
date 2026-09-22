
DECISION F283 D13 (2026-09-22, round 21) — WHAT THE `--json` SWEEP RUNS, WHAT IT ASSERTS, AND WHAT
IT DELIBERATELY DOES NOT PREPARE.

CONTEXT. T002's last line asks for a sweep over every `supports_json` command reachable without a
positional argument, asserting a parseable envelope on success AND on a deliberately invalid
argument, with catalog-to-dispatch parity in the same file. Two things had to be measured before
that could be ordered, and the reviewer measured both at `a100a48a` by running the commands. First,
an invalid argument is refused at PARSE level, before any handler runs, so that half is safe for
every command in the catalog and not only for the ones without a positional: all 144
`supports_json` commands answer an envelope with `ok` false at exit 2 when given an unrecognised
option. Second, a command that RUNS is only safe when it neither mutates the repository nor
executes anything, and the catalog's own classification is not enough on its own — `ui stop`
declares `read_only` while it stops every running UI session (finding R-1034).

CHOSEN. (1) The sweep lives in `tests/cli/test_json_contract.py` and has two halves. The INVALID
half runs every `supports_json` command in the catalog with one unrecognised option and `--json`.
The SUCCESS half runs every `supports_json` command that needs no positional argument, whose
action class is `read_only`, which neither mutates the repository nor executes commands, and which
is not excluded by name: 33 commands at `a100a48a`.
(2) Both halves assert the same three properties of what the command wrote to standard output: it
parses as ONE JSON object; that object carries `schema_version` 1 and a boolean `ok`; and the exit
code is 0 if and only if `ok` is true. The third is the join between this feature's two halves —
the envelope says what happened and DECISION F283 D12 (1) says the number must agree with it — and
it is the assertion that would have caught a success envelope shipped at a failing exit code.
(3) Exclusions are BY NAME with their reason in the test, never by a silent filter. At `a100a48a`
there is one: `ui.stop`, which stops live sessions on the machine running the suite, under finding
R-1034.
(4) Both halves run IN PROCESS, calling the grouped CLI's own entry point with an argument list,
under the suite's isolated data root (`_isolated_data_root` in `tests/conftest.py`, which points
`REMEDY_DATA_DIR` at a temporary directory for every test). Measured by the reviewer: the success
half takes about three seconds in that environment, against seventeen seconds for `data usage`
alone when it reads a real data root.
(5) PARITY: every catalog `command_id` has exactly one handler in the dispatch table and every
dispatch key is a catalog `command_id`. Measured at `a100a48a`: 145 entries and 145 handlers.
(6) DELIBERATE ABSENCE. The sweep prepares no project, no job and no token ledger, so a command
that needs one answers a REFUSAL envelope rather than a success envelope, and the sweep asserts the
envelope and the exit-code agreement rather than the contents. Preparing a full world for 33
commands would make the sweep a fixture suite whose failures are about the fixture, and the
per-command tests this feature has been landing since round 14 are where the CONTENT is pinned.
The gap that absence leaves is real and this round shows it: `stats report --json` answers an
envelope in an empty data root, because it refuses without a project, and answers a document that
is not an envelope when a ledger exists (finding R-1033), which only a test with a ledger reaches.
That is the shape of what the sweep can and cannot see, stated here rather than discovered later.

ALTERNATIVES. Sweep only the commands without a positional argument in the invalid half too —
rejected: the parse level refuses before any handler runs, so the wider half is free and covers
every command. Derive the safe set from `action_class` alone — rejected, R-1034 is the
counter-example. Prepare a project and a ledger for the success half — rejected under (6). Assert
only that the output parses — rejected: the exit-code agreement in (2) is the property a machine
consumer actually depends on.

REVERSE by deleting this paragraph and `tests/cli/test_json_contract.py`.
