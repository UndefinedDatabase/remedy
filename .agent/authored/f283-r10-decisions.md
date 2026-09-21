
DECISION F283 D5 (2026-09-21, round 10) — `remedy do --json` ANSWERS IN ONE ENVELOPE, AND A
FAILED WALK CARRIES ITS WHOLE RESULT DOCUMENT INSIDE THE FAILURE ENVELOPE.

CONTEXT. `apps/cli/commands/do_cmd.py::_cmd_do_order` prints its result document under `--json`
unconditionally and then, when a step failed, prints `Error: <step> failed: <detail>` on stderr and
exits 1. Round 8 declined to move that last line onto `fail()`, correctly: a `fail()` after the
document puts a second JSON object on stdout. The document itself carries neither `schema_version`
nor `ok`, so a consumer cannot tell a failed walk from a finished one without reading the exit code.
Measured at `859f883c`: the only programmatic reader outside `tests/` is
`scripts/remedy_smoke.sh`, which reads `mission_id`, `job_ids` and `stopped_before_apply` as
top-level keys of one object.

CHOSEN. Under `--json` the handler builds the same document with the same keys and emits exactly
one object: `emit_ok(**document)` when no step failed, and
`fail("step_failed", "<step> failed: <detail>", json_output=True, failed_step=<step>, **document)`
when one did — so the failure envelope carries `ok` false, the token, the sentence, the name of the
step and every key the document carried before, at exit 1. Every key stays top-level, so a reader
of the old object keeps working. The object is written by the envelope's own writer, compact and
with sorted keys, where the old one was indented; its content is unchanged. The text branch is
byte-identical, its failure line now written by `fail(..., json_output=False)`.

ALTERNATIVES. Print the failure envelope after the document — rejected: two objects on stdout is the
defect. Nest the document under one key — rejected: it breaks every reader of the old top-level
keys for no gain. Keep the old object and add `ok` by hand — rejected: that is a second envelope
writer, which is what F277 T002 removed.

REVERSE by deleting this paragraph and restoring `_cmd_do_order` from git history at the parent
of the commit that lands this decision's patch.

DECISION F283 D6 (2026-09-21, round 10) — A USAGE REFUSAL THE PARSER RAISES ANSWERS IN THE
ENVELOPE WHEN `--json` IS ON THE COMMAND LINE.

CONTEXT. `apps/cli/grouped.py::main` refuses an unknown group, an unknown subcommand, an
unrecognized argument and a usage error on a known subcommand before any handler runs, in prose on
stderr — or, for the last, with the command's help text — and exits 2. Under `--json` a parser then
reads an empty stdout, or help text, which is the failure shape this feature exists to remove, and
T002's sweep fires exactly these refusals with its deliberately invalid argument. One refusal there
already answers in JSON, a conflicting-options object written by hand without `schema_version`.
`_dispatch` already asks `_wants_json(raw)` — whether `--json` appears in the arguments — before
it answers in the envelope, because no handler has parsed the flag yet.

CHOSEN. Each of those refusals asks `_wants_json(raw)`. When it holds, the answer is one failure
envelope on stdout, written by `emit_error`, and the exit code is unchanged: `conflicting_options`
for the conflicting pair (the token that object already used), `unknown_command` for an unknown
group or subcommand, `unrecognized_arguments` for an argument the parser did not consume, and for a
usage error on a known subcommand `missing_argument` when the parser's message begins "the
following arguments are required" and `invalid_argument` otherwise, the parser's own message being
the envelope's `message`. When it does not hold, stderr and stdout are byte-identical to today,
help text included. The text branch is `render_error`'s, which `fail()` cannot write, so these
sites call `emit_error` and exit themselves rather than calling `fail()`. The two internal
refusals after the parse — a missing command id and a missing handler — are ordinary
`Error: `-prefixed pairs and move onto `fail()` with `json_output=_wants_json(raw)`, as
`unknown_command` and `no_handler`.

ALTERNATIVES. Leave parse-level refusals in prose and let T002's sweep exclude them — rejected: the
sweep's invalid-argument half is the half F277 found broken. Give `fail()` a way to write
`render_error`'s text — rejected: `fail`'s signature is F277's contract and this feature's file
forbids changing it.

REVERSE by deleting this paragraph and restoring `apps/cli/grouped.py::main` from git history at
the parent of the commit that lands this decision's patch.
