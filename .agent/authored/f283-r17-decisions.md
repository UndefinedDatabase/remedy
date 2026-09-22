
DECISION F283 D10 (2026-09-22, round 17) — EVERY `--json` SUCCESS PATH WRITES ITS DOCUMENT
THROUGH THE ENVELOPE, ADDITIVELY, AND A RESULT THAT FAILED IS A FAILURE ENVELOPE.

CONTEXT. The acceptance list asks every `supports_json` command for a parseable envelope with
`schema_version` and `ok` on success. Measured at `488fd05a` by the scanner
`.remedy-wt/f283-r17-scratch/raw_sites.py`, 122 calls under `apps/cli/` still write a raw JSON
document to stdout, `print(<json>.dumps(...))` or `<json>.dump(..., sys.stdout)`, across 34
modules. A mechanical conversion of all of them in a disposable worktree turned 43 tests red in
the round's selection, and every one of those reads the old document's exact shape. DECISION
F283 D5 already rules this for `remedy do`; this decision takes its rule to every command.

CHOSEN. (1) A `--json` success path writes `emit_ok(**document)`. The conversion is ADDITIVE:
every top-level key of the old document stays, with the same name and the same value, including
a `version` key where one exists, and the envelope adds `schema_version` and `ok`. Adding keys
breaks no reader by the envelope's own contract, and a later decision may retire `version`. The
envelope's writer is compact with sorted keys, where some old documents were indented; the
content is unchanged. (2) A document that carries its own `ok`: when it is true it is dropped,
because the envelope's `ok` says the same; when it is false the path is a failure and follows
(3). (3) A path that prints a result document and then exits non-zero answers ONE failure
envelope instead, as D5 rules: `fail(<token>, <sentence>, json_output=True, exit_code=<the same
code>, **document)`, the token named for the condition by DECISION F277 D8. Where the document
carries a key named like one of `fail()`'s own parameters — `error`, `message`, `json_output` or
`exit_code` — the path writes `emit_error(<token>, <sentence>, **document)` followed by its
existing `sys.exit(<code>)`, as the four result-shaped exits of `runtime_cmd.py` already do under
DECISION F283 D8. (4) A top-level document that is not an object is carried under one named key,
and every reader of it inside the repository changes in the same commit. (5) A raw document
printed WITHOUT `--json`, in a text branch, is out of scope and stays as it is. (6) A ratchet in
`tests/cli/test_json_envelope.py` counts the raw-document sites per module with the scanner's
rule and pins them by EQUALITY; each conversion commit lowers it, and when the conversion is done
it names only the text-branch survivors of (5), each with its reason.

ALTERNATIVES. Nest the old document under one key such as `data` — rejected: it breaks every
reader of the old top-level keys, which D5 already rejected for the same reason. Drop `version`
while converting — rejected: removing a key can break a reader, and the envelope promises only
that adding one cannot. Leave result documents that exit non-zero as they are — rejected: a
parser would read `ok` true beside a failing exit code.

REVERSE by deleting this paragraph and restoring each converted module and the ratchet from git
history at `488fd05a`.
