
DECISION F277 D7 (2026-09-20, round 7) — `fail()` IS SPELLED `fail(error, message, *,
json_output, exit_code=1, **payload)`, AND T003's PLANNING NUMBERS ARE RE-MEASURED.

CONTEXT. `docs/roadmap/features/T2_F277.md` T003 reads: "A shared `fail(code, message, *,
json_output)` replaces the `print(...); sys.exit(1)` pairs". That signature names two different
things with one word. The envelope this helper writes into already has a key called `error`
holding a stable machine token, and the same function has to be able to set the process exit
code, because `runtime_cmd.py` alone exits 2, 3, 4 and 5 by a documented contract. A call site
reading `fail("invalid_job_id", ...)` beside one reading `fail(2, ...)` would be two different
functions wearing one name. Separately, every number T003 was planned against was measured at
`a5bf8949`, before F261 deleted two thirds of the CLI surface.

CHOSEN, part (a) — the signature. `error` first, because that is what the envelope's key is
called and what `emit_error`'s own first parameter is called, so the concept keeps one spelling
from the call site to the wire (AGENTS.md, Code Discoverability Conventions). `message` second,
unchanged. `json_output` keyword-only, unchanged, and spelled as the handlers already spell the
flag they thread. `exit_code` keyword-only with a default of 1, because all but a handful of the
237 migrated sites exit 1 and the handful that do not are exactly the ones that should have to
say so. `**payload` carried through to the envelope, so a call site can attach the job id or the
error class it already holds without building the envelope itself. The return annotation is
`NoReturn`: a call site that writes a statement after `fail()` is then a type error rather than
unreachable code, and the round asserts that annotation from the module rather than trusting it.
The text branch prints `f"Error: {message}"` to stderr, which is byte-for-byte the line this CLI
already printed at those 237 sites, so a migration changes nothing an operator sees and only the
`--json` branch gains a shape it did not have.

CHOSEN, part (b) — the numbers. Measured at `62b40261` and written into T003 so no later round
plans against the old ones: the catalog holds 145 commands, not 339; 132 are read-only by the
derived rule `not may_mutate_repo and not may_execute_commands` and 33 of those do not declare
`supports_json`, not 49; there are 237 `print(...); sys.exit(...)` pairs across 28 files under
`apps/cli/`. Of the three commands T2_F277 says accept `--json` and ignore it, the file only
ever named two: `remedy readiness job`, whose whole group F261 deleted at `2f46e267`, and
`remedy do plan`, which still answers a failure with a JSON body on stdout followed by a bare
`Error: ...` line on stderr. The slice therefore stops chasing a list of three and repairs the
failure path at every site it reaches, with T004's sweep as the proof over the whole surface.
Found while measuring that: `init run` and `dev status` each carry a `--json` argument and each
honours it, yet both declare `supports_json = False` — a false declaration, fixed with the
read-only set rather than as its own item.

ALTERNATIVES. Keep `code` as the feature file spells it and let the exit code be positional —
rejected: it makes the ambiguity permanent at 237 call sites, which is the population that has
to be readable. Name it `error_code` — rejected: it reads as a number, which is the confusion
being removed. Put `fail()` in a new module beside the envelope — rejected: `json_envelope.py`'s
own docstring already announces `fail()` as the helper that emits and exits, written in round 6,
and a second module would split one contract across two files. Let `fail()` take the whole
envelope dict — rejected: the two-token shape is what makes a consumer able to branch without
reading prose, and a dict parameter invites a call site to reshape it.

REVERSE: delete this paragraph, restore T003's paragraph from git history at `62b40261`, and
rename the parameters at every migrated call site. Reversing part (b) alone means re-adopting
counts that describe a CLI surface F261 deleted, which is how a later round plans work that does
not exist.
