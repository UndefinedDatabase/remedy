
DECISION F283 D12 (2026-09-22, round 20) — THE EXIT-CODE TAXONOMY: ONE MEANING PER CODE FOR
THE CLI, THE RUNTIME GROUP'S OWN CONTRACT BESIDE IT, AND EVERY COMMAND'S CODES DECLARED IN THE
CATALOG.

CONTEXT. No document gave any exit code a meaning. Measured at `98a85b67` by an AST scan of
`apps/cli/` over `sys.exit(...)`, `SystemExit(...)` and `fail(..., exit_code=...)`: literal
code 1 at 193 sites, 2 at 25, 3 at 17 and 4 at 2, plus 28 sites that name a module constant
or a computed value, and those constants resolve to 1 to 5. The code 3 already meant one thing
wherever it was written (no project, an unknown job or task, a plan awaiting approval or
rejected, worktree drift), 4 meant "not a git repository" in `init`, and the `runtime` group
used 2 to 5 for a contract of its own, keyed on `error_class`, that the supervisor subprocess
and `packages/runtimes/dev_server.py` read (the feature file's T001). Round 19's reviewer also
observed that `job resume --checkpoint` answers `ok` true at exit 0 in branches that did not
resume, and left the ruling to this decision.

CHOSEN. (1) The CLI's meanings. 0 `ok`: the command did what it was asked, including finding
nothing to do or honouring a pending stop request. 1 `failed`: the command ran and did not do
what was asked — a refusal, a failed operation, a red check, drift found; it is the general
failure and the code of every refusal no narrower meaning claims. 2 `usage`: the invocation
itself is wrong — an unknown command, or a missing, invalid, unrecognised or conflicting
argument — and nothing was attempted. 3 `not_ready`: the invocation is well formed, but what it
names is absent or not in a state the command can act on. 4 `environment`: the machine lacks a
prerequisite the command cannot supply, such as a git repository.
(2) The `runtime` group keeps its contract, because a process outside the CLI reads it: 2
`config`, the runtime configuration is missing or invalid; 3 `start`, the server did not
start; 4 `ready`, it started and never answered ready; 5 `state`, a lifecycle or state failure
such as a failed stop, surviving processes or an unreadable state file. 0 and 1 mean what they
mean everywhere, and a malformed invocation of a runtime command still exits 2.
(3) The meanings are written once, as two tables in a new module `apps/cli/exit_codes.py`.
The guide `docs/guides/exit-codes.md` carries both tables and one row per command that
declares more than the floor below, and a test asserts all of it equal to the module and to
the catalog, so the guide is read from the catalog and never from prose.
(4) Every catalog entry declares its codes in a new field, `CommandEntry.exit_codes`, whose
default `(0, 1, 2)` is the floor every command reaches: the parser exits 2 on a malformed
invocation and the dispatch boundary exits 1 on an unhandled exception. A command declares a
code above the floor exactly when its handler reaches it. `tests/cli/test_exit_codes.py` reads
each handler statically — its own body, the same-module functions it calls, the `apps.cli`
functions it imports, and a code passed into a helper's `exit_code` parameter at the call site
— and asserts, per command, that the codes above the floor it reaches EQUAL the codes above the
floor it declares, and that every declared code has a meaning in its group's table. A site
whose code that reading cannot resolve is named in the test with the codes a reader verified
by hand, and an unnamed unresolved site fails the test.
(5) No existing site is renumbered. A code is a contract with every script that reads it, so an
older site that answers a not-ready condition with 1 stays at 1, which (1) permits.
(6) Round 19's observation. `_cmd_resume` in `apps/cli/commands/job.py` answered a success
envelope at exit 0 in two branches that did not resume: a `from_apply` continuation refused by
its own validation, and a resume mode with no implementation. The second is unreachable at
`98a85b67`, since `packages/orchestration/event_replay.py` marks only `from_apply` checkpoints
safe to resume, and is converted so that adding a mode cannot make it a silent success. Both
now refuse through `fail("resume_blocked", ...)` at exit 1 with `resumed` false and the
`blocked_reason` and `worktrees` keys, the token, code and keys the two sibling refusals of
`_cmd_resume` already use. A resume that ran and whose tests came out red still exits 0: it
did what it was asked, and the outcome is its data, `tests_passed`.

ALTERNATIVES. Document the codes in the guide alone — rejected: the feature file asks for the
documentation to be asserted from the catalog, and prose drifts. Declare codes per group
instead of per command — rejected: one `project` command reaching 3 would license 3 for every
`project` command, so the declaration would say nothing. Renumber the older not-ready sites to
3 — rejected: it breaks shell callers for a tidier table. Fold the runtime codes into the CLI
table — rejected: it changes a contract a subprocess reads.

REVERSE by deleting this paragraph, `apps/cli/exit_codes.py`, `docs/guides/exit-codes.md` with
its two rows in `docs/README.md`, `tests/cli/test_exit_codes.py` and the `exit_codes` field
with its declarations in `apps/cli/command_catalog.py`, and by restoring `_cmd_resume` in
`apps/cli/commands/job.py` from git history at `98a85b67`.
