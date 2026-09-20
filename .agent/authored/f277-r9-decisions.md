
DECISION F277 D8 (2026-09-20, round 8) — THE ERROR TOKEN IS A VOCABULARY, NOT A FREE STRING,
AND TWO MIGRATED MESSAGES GAIN THE `Error: ` PREFIX THEY NEVER HAD.

CONTEXT. `fail(error, message, ...)` puts a token on the wire that a machine consumer is
invited to branch on, and T2_F277's Acceptance asks for a parseable envelope on every
`--json` command. A token a call site invents locally is worth nothing to that consumer: two
commands answering the same condition under two spellings is the same defect as no token at
all. Measured while migrating: `apps/cli/commands/job.py` already raises
`ShowSectionError("no_target_repo", ...)` and `ShowSectionError("target_repo_missing", ...)`
for exactly the two conditions `job context` refuses on, with the same message text, and
`apps/cli/commands/test_cmds.py` and `apps/cli/commands/patch.py` each already write
`"error": "no_target_repo"` into their own JSON. A vocabulary therefore already exists in the
product, unevenly, and the migration either joins it or forks it.

CHOSEN, part (a) — ONE TOKEN PER CONDITION, REPO-WIDE, AND THE EXISTING SPELLING WINS. Where
the product already spells a condition, the migration adopts that spelling: `no_target_repo`
and `target_repo_missing` in `job context` are the two `job show` already raises. Where
it does not, the token is named for the CONDITION and never for the command, so the same
condition reads the same in every group — `invalid_job_id` for an id that resolves to nothing,
`job_not_found` for a store that has no such job, `invalid_list_option` for every refusal
`apply_list_options` raises, `missing_argument` for an omitted required flag. Tokens landed so
far, across the seven migrated groups: `invalid_job_id`, `job_not_found`, `invalid_list_option`,
`event_not_found`, `no_target_repo`, `target_repo_missing`, `task_not_resolvable`,
`unknown_provider`, `unsupported_provider`, `missing_argument`, `change_not_found`,
`invalid_path`, `blocker_not_found`, `invalid_contract`, and `unhandled_command_error` from
the round 6 boundary. T004's sweep is where this list becomes a thing a test reads rather than
a thing a decision lists; until then this paragraph is the register, and a round that mints a
token checks it here first.

CHOSEN, part (b) — THE TWO UNPREFIXED MESSAGES ARE PREFIXED, DELIBERATELY. `job context`
printed `Job abcdef01 has no target_repo attached` and `Target repo does not exist: <path>`
with no `Error: ` prefix, alone among the CLI's refusals. Migrating them onto `fail()` gives
them the prefix, because `fail()`'s text branch is one line by construction and a helper with
a per-call-site prefix switch would be a helper that does not unify anything. This is a
user-visible change to two lines and it is the smaller inconsistency: an operator grepping for
`Error: ` was missing exactly these two refusals. No test pinned either string — checked
before the change, not after — and the round's own tests pin the new text. The two exit codes,
2 and 3, are unchanged and are now asserted, which they were not before.

ALTERNATIVES. Let each call site pick its own token and reconcile at T004 — rejected: T004
asserts a sweep, and a sweep cannot invent the vocabulary it is meant to check; reconciling
fifteen spellings after the fact is a rename across every migrated group. Put the vocabulary in
a module now, as a frozen set with a guard, the way T001 did for event names — rejected for
this round only, not on the merits: the set is still growing one group per round and a guard
over a moving set buys a round of churn per round of migration. It is the right shape and T004
is where it lands. Keep the two unprefixed messages byte-identical by giving `fail()` a
`prefix` parameter — rejected: that is a switch whose only caller is the inconsistency it
preserves.

REVERSE: delete this paragraph. Part (a) reverses by nothing on disk — it is a rule the next
round reads, and abandoning it means the next group mints its own spellings. Part (b) reverses
by restoring the two `print(...)` lines in `apps/cli/commands/job_context_cmd.py` from git
history at `a8e2e565` and dropping the two message assertions the round's tests carry.
