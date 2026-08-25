# Model Defaults and the Dead-Model Check v0

Built-in model defaults and the `remedy doctor core` check that tells an
operator when one of them is known to be retired. Built state as of F254.

## One alias table

`packages/orchestration/model_aliases.py` holds every concrete model id
Remedy ships as a BUILT-IN default. Callers name a logical alias
(`claude-flagship`, `claude-workhorse`, `ollama-default`, `fake`,
`fixture`) and resolve it; no other module spells a concrete id.

Why one table: the same dated id used to be retyped into every module
that needed a fallback, so "which ids does this repo ship?" had no answer
short of a full-text search, and upgrading one meant finding all of them.
Now an upgrade repoints one line.

The rule is enforced, not merely intended: a test in
`tests/orchestration/test_model_aliases.py` parses every `.py` file under
`packages/` and `apps/` with `ast` and fails if any string constant
outside the alias module equals a table value. Because `ast` discards
comments, and docstrings are excluded explicitly, an illustrative id in
prose is out of scope by construction rather than by an allow-list.

A configured value still outranks the table. Built-in defaults are what
Remedy falls back to when nothing is configured.

## The known-dead list

`scripts/dead_models.json` is shipped, operator-editable data listing ids
known to be retired, each with a reason and an optional replacement.
`packages/orchestration/dead_model_list.py` reads and validates it.

The `doctor.dead_models` config key (env `REMEDY_DOCTOR_DEAD_MODELS`)
EXTENDS that list; it never replaces it, so an id Remedy already ships as
dead cannot be configured away. An unreadable or malformed shipped list
raises rather than degrading to "nothing is dead" — those are opposite
answers and must never look alike.

## What `remedy doctor core` reports

One hard check plus advisory warnings:

- `dead_model_list` is a normal check. It fails, and lands in `blockers`,
  only when the list cannot be read. Its detail counts shipped ids and
  config-only ids (ids config added that were not shipped already).
- Each dead id found among the built-in defaults or among the resolved
  `*.model` config keys produces a WARNING. Warnings never change `ready`
  and never enter `blockers`: a shipped default landing on the list is
  the expected state between a provider retiring an id and an operator
  repointing the alias, and reporting NOT READY on a fresh clone would
  teach operators to ignore the word. That was the live state until
  2026-08-25, when an operator decision repointed `claude-flagship` and
  `claude-workhorse` off the two retired May-2025 ids; a fresh clone now
  warns about none of its own defaults, and will again the next time a
  provider retires one.

Every warning names the id, where it came from (the alias to repoint, or
the config key to change), and the fix. Text mode prints one compact line
per warning; `--json` adds the entry's full recorded reason under
`detail` alongside that compact `summary`.

Both modes state the provenance: the verdict comes from
operator-maintained data and **no provider is queried**. Remedy does not
know a model is retired — it knows a file says so, and the check is
exactly as fresh as that file. Choosing a successor id is out of scope
here (see `docs/roadmap/features/T15_F232.md`).
