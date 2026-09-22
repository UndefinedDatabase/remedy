
DECISION F283 D9 (2026-09-22, round 14) — THE CATALOG HALF EMPTIES THE READ-ONLY SET BY
TEACHING EACH COMMAND `--json`, AND A COMMAND THAT GAINS THE FLAG ANSWERS IN THE ENVELOPE
FROM ITS FIRST COMMIT.

CONTEXT. The derived rule of DECISION F277 D7 calls a command read-only when it declares
neither `may_mutate_repo` nor `may_execute_commands`. Measured at `dc4c1e60` by that rule, the
catalog holds 132 read-only commands and 33 of them do not declare `supports_json`: `init run`,
`dev status`, `dev smoke-help`, `memory store` and the five memory card mutations, `blocker
resolve`, `patch show`, `patch approve`, `patch reject`, `job plan`, the seven `brain` report
and viewer commands, `decision resolve`, `decision explain`, the five `ui` commands and the
five `project` create and attach commands. Two of them, `init run` and `dev status`, already
carry `--json` and honour it; that is D7's false declaration. The rest print text only, and
several print a report that a function under `packages/` renders as one string, with no
structured exporter beside it.

CHOSEN. (1) The set is emptied by making each command answer `--json`, and never by changing
`may_mutate_repo` or `may_execute_commands`: those two flags say what a command does, and
setting one to shrink a list would make the catalog lie. (2) A command that gains `--json` in
this half answers success with `emit_ok(**payload)` and every refusal with
`fail(..., json_output=json_output)`. It writes no raw `json.dumps` document and no `version`
key, because `schema_version` is the envelope's. The payload holds the values the handler
already has: the ids it resolved, the paths it wrote, the records it changed and the counts it
printed. Where the text output is a report that a `packages/` function returns as one string,
the payload carries that string under `text` beside the ids; splitting a report into keys is
not this feature's scope, and a later feature may add keys without bumping `schema_version`.
(3) Nothing but the output changes under `--json`: an opener still opens, a server still
serves, a record is still written, and the envelope says what was done. Warnings stay on
stderr, so stdout under `--json` carries exactly one envelope. The one exception is `ui
start`, which runs until it is stopped: it prints its one envelope once the server is bound,
and then serves. (4) `init run` and `dev status` gain only the declaration here, together with
the `--json` branch of `init run`'s not-a-repository refusal moving onto `fail()` with its exit
code 4 and the reused token `not_a_git_repo`, its text branch kept under DECISION F283 D7. Their success documents are raw `json.dumps` sites like the others
T002's success half converts, and they are converted there, with the others, by one rule. (5) A
handler lambda reads the flag as `getattr(args, "json", False)`, because the UI command door
builds its own argument namespace for the one command of this set it exposes, `decision
resolve`. (6) A ratchet in `tests/test_command_catalog.py` pins the commands still missing the
declaration by EQUALITY, so a command can neither leave the set unannounced nor join it. Each
round that lands a group removes that group from the ratchet, and the round that lands the last
group asserts the set is empty and deletes the constant. The groups land in this order: `init`,
`dev`, `memory`, `blocker` and `patch` first; then `decision`, `job plan` and `brain`; then
`ui` and `project`.

ALTERNATIVES. Mark `ui start`, `ui open` and `brain open` as `may_execute_commands` so that they
leave the set — rejected, because they start a server or an opener rather than executing a
command the operator named, and a flag set to satisfy a test is the false declaration D7 found.
Emit a raw document now and let T002 wrap it later — rejected, because it writes the output
of the same thirty-one commands twice. Give every report its own structured keys now — rejected, because it
reaches into `packages/` renderers the acceptance list does not ask for.

REVERSE by deleting this paragraph, restoring each named command's catalog entry and handler
from git history at `dc4c1e60`, and deleting the ratchet.
