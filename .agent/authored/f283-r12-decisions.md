
DECISION F283 D7 (2026-09-21, round 12) — A REFUSAL IN A `--json` HANDLER THAT `fail()` CANNOT
WRITE BYTE FOR BYTE ANSWERS THE ENVELOPE UNDER `--json` AND KEEPS ITS TEXT.

CONTEXT. The migration rule reaches a refusal whose text is one `Error: `-prefixed line, because
that is the line `fail()` writes. Measured at `e964343b`, the refusals left in `supports_json`
handlers outside `runtime_cmd.py` include ones whose text is something else: a bare
`print(str(exc))` in `project current` and in `config set`, a bare sentence in `config get` and
`config init`, and two lines in `patch approve-hunks`. Under `--json` each answers prose on stderr,
or a hand-written object without `schema_version` and `ok` — `config` writes `{"error": <the
sentence>}` and `patch approve-hunks` writes `{"code": ..., "message": ..., "hunk_ids": ...}`. D4
normalised a prefix's CASE; it gave no ruling on a line with no prefix, and said so. One more
shape exists: `apps/cli/commands/worker_facade_cmd.py::_err` writes `{"error": <msg>}` to STDERR in
both modes, reached only by `mission run` with an empty id.

CHOSEN. Such a site takes the envelope under `--json` — `fail(<token>, <the text the line
printed>, json_output=True[, exit_code=<n>], <kept keys>)` guarded by the handler's flag — and
its text branch stays exactly as it is, however many lines it prints. The tokens: `project
current` gives `project_not_found` for `ProjectNotFoundError` and `invalid_project_selector` for
`InvalidProjectSelectorError`, at exit 3; `config get` gives `unknown_config_key`, `config init`
`config_file_exists` and `config set` `invalid_config_value`; `patch approve-hunks` gives the
decision core's own refusal code as the token, keeping `hunk_ids`, so the old `code` key becomes
the envelope's `error` and is not repeated. `_err` is deleted and its one caller calls
`fail("missing_argument", "run_id required", json_output=<flag>)`, so that line's text becomes
`Error: run_id required` — the third deliberate text change of this kind, after D8 part (b) and
D4, because a JSON object on stderr is a shape no reader of either stream expects. The
cost-preview refusal in `apps/cli/cost_preview_confirm.py`, whose text is already the line
`fail()` writes, collapses to one `fail()` call with no change to either branch.

ALTERNATIVES. Give each of these lines an `Error: ` prefix so the plain rule reaches them —
rejected: it rewords messages an operator reads for no gain to a machine, which is D4's own
reason for leaving unprefixed lines alone. Leave them in prose until T002 — rejected: they are
refusals of `supports_json` commands and T002's sweep would find them red.

REVERSE by deleting this paragraph and restoring the named handlers from git history at the
parent of the commit that lands this decision's patch.
