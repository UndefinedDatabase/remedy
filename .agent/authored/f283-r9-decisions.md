
DECISION F283 D4 (2026-09-21, round 9) — AN UPPERCASE `ERROR: ` REFUSAL IS MIGRATED LIKE A
`Error: ` ONE, AND GAINS THE CASE EVERY OTHER REFUSAL USES.

CONTEXT. `apps/cli/commands/project.py` writes its refusals in two spellings: `Error: ...` at
some sites and `ERROR: ...` at others — `invalid project UUID`, `project not found`, `is not a
git repository`, and an ambiguous project selector among them. `fail()` writes `Error: ` and has
no switch for the case, by DECISION F277 D8 part (b)'s ruling against a per-call-site prefix. The
migration rule this feature's blocks state reaches only a `print` that begins with `Error: `, so
as written it would leave every uppercase site in prose. Measured before this decision: no test
under `tests/` asserts the string `ERROR:` at all.

CHOSEN. A pair whose `print` begins with `ERROR: ` is migrated exactly like one that begins with
`Error: `: the message passed to `fail()` is the text after the prefix, and the operator now
reads `Error: ` where the line read `ERROR: `. This is the second deliberate text change of its
kind, after D8 part (b)'s two unprefixed `job context` lines, and for the same reason: an
operator grepping for the prefix every other refusal in the CLI uses was missing these. Nothing
else in any message changes. A `print(str(exc), file=sys.stderr)` with NO prefix at all is still
not reached by the rule; it stays and is counted, because giving it a prefix is a wording choice
about a message the exception composes, not a case normalisation.

ALTERNATIVES. Leave the uppercase sites in prose until a later round — rejected: they are
refusals of `supports_json` commands like the rest, and deferring them is deferring the defect.
Give `fail()` a case switch — rejected by D8 part (b)'s own reasoning; it preserves the
inconsistency it exists to remove.

REVERSE by deleting this paragraph and restoring `apps/cli/commands/project.py` from git history
at the parent of the commit that lands this decision's patch.
