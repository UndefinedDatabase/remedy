# F275 T003 — the three largest residue classes are ONE seam, and no rewrite rule closes it

> Measured by the reviewer at `93063ec4`, this round's base, in two disposable `git
> worktree`s under the gitignored `.remedy-wt/`, both removed and pruned before this text
> was authored. THIS FILE RECORDS A DIAGNOSIS; IT FLIPS NOTHING AND FIXES NOTHING. No line
> under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote
> it. It replaces none of the earlier residue artefacts, which record the runs at
> `978046fe`, `020b1d57`, `08feacae`, `bf5ec6a4`, `bf692757` and `5dfeeae6` and stay as
> written.
>
> PROVENANCE, STATED SO NO READER HAS TO GUESS. Every figure in sections 2, 3, 4, 6 and 7
> is re-derived by the committed instrument `.agent/authored/f275-r63-diag.py.md`, which
> reads the four dry-run logs and the tree and is what this round's gate runs. TWO readings
> are NOT in that instrument's output and are the reviewer's own, taken at `93063ec4`: the
> seam diff quoted in section 5, which needs the transform re-run in a worktree, and the
> "49 calls in 17 files" the candidate rule rewrote in section 6, which needs the worktree
> that rule was applied to. Both worktrees were removed before this text was authored.

## 1. The question this round was given

`.agent/plan.md` at the base names it in one sentence: the three largest residue classes
are reads of an id whose SHAPE changed rather than renames, and the round must rule whether
they are a FOURTH rule family of DECISION F275 D32's kind or a consequence of records
already written to disk under the classic shape — which would be a data-migration question
and not a transform question.

The answer is NEITHER, and it was measured from both directions rather than argued.

## 2. What the three classes actually are

Attributed out of `.remedy-wt/r61_flipped.log`, the round 61 flipped run, by pairing each
`E   <Exc>: <msg>` line with the frame `--tb=line` prints for it and with the `Error:` text
the handler captured in between:

| class | E-lines | the frame that raises it |
|---|---:|---|
| `SystemExit: 1` | 337 | 193 at `packages/orchestration/data_paths.py:324` |
| `ValueError: badly formed hexadecimal UUID string` | 223 | 87 at `/usr/lib/python3.10/uuid.py:177` |
| `TypeError: unsupported operand type(s) for /` | 90 | ALL 90 at `packages/orchestration/data_paths.py:200` |

The captured stderr is what turns three classes into one story. Of the 337 `SystemExit`
lines, 316 carry an `Error:` line and every one of them carries an ID SHAPE:

    180  no job matches prefix 'X'   [arg=16hex]
    123  invalid job ID: 'X'         [arg=16hex]
     13  no job matches prefix 'X'   [arg=8hex]

The `unsupported operand` message is not normalised in the log at all. All 90 read
literally `unsupported operand type(s) for /: 'PosixPath' and 'UUID'`.

## 3. The mechanism, reproduced by CALLING the shipped functions

Each of the three reproduces on its own, and each is printed beside a CONTROL on the shape
the unified store mints, because a probe that cannot succeed proves nothing by failing:

    mint_job_id() len 16 hyphens 0 | str(uuid4()) len 36 hyphens 4
    UUID(mint_job_id()) -> ValueError: badly formed hexadecimal UUID string
    job_dir(UUID, root) -> TypeError: unsupported operand type(s) for /: 'PosixPath' and 'UUID'
    load_job_plan(UUID, root) -> TypeError: unsupported operand type(s) for /: 'PosixPath' and 'UUID'
    JobPlan(job_id=uuid4()).job_id is a UUID — the dataclass does not coerce
    CONTROL job_dir(minted, root) -> <root>/jobs/<16hex>
    CONTROL load_job_plan(minted, root) -> None

`JobPlan` is a DATACLASS and not a pydantic model, so `job_id: str` is an annotation that
validates nothing: a `UUID` handed to that keyword is stored as a `UUID` and travels
unchanged into `job_dir`, where `jobs_dir(root) / job_id` has no `__truediv__` for it.

THE FAILURE NEEDS NO RECORD ON DISK. Both `TypeError` lines above were raised against a
root that does not exist, before any file was opened, and `UUID(mint_job_id())` is a
stdlib parse of a freshly minted string. So this is NOT a consequence of records written
under the classic shape, and the data-migration reading of the question is answered NO by
a probe rather than by an opinion.

## 4. The resolver half, run against a store holding BOTH shapes

A synthetic data root was built under the gitignored scratch with one classic record
(`<uuid>.json`) and one unified record (`<16hex>/job.json`), `REMEDY_DATA_DIR` pointed at
it, and the SHIPPED `resolve_job_id` called on a prefix of each:

| input | `_classic_job_id_matches` | `_task_job_id_matches` | `resolve_job_id` |
|---|---|---|---|
| the classic record's 8-hex prefix | finds it | `[]` | returns the canonical id |
| the unified record's 8-hex prefix | `[]` | finds it | `SystemExit: 1` |
| the unified record's WHOLE id | `[]` | finds it | `SystemExit: 1` |

The record is ON DISK and the sibling function FINDS it; `resolve_job_id` still exits 1,
because it searches the classic store by construction and its own docstring says so. No
rewrite of any call site changes that, and no migration of any record changes it either —
a unified record is exactly what it cannot see.

## 5. Why the transform cannot reach the seam, shown by its own output

The transform was re-run at `93063ec4` in a disposable worktree and its log is BYTE-
IDENTICAL to round 61's, which is what licenses reading this round's seam diff as a
property of the same transform. At the handler seam it produces:

    -        job = load_job(job_id)
    +        job = load_job_plan(job_id)
             job_id = UUID(job_id_str)          <- UNCHANGED

and in `apps/cli/commands/readiness.py` one single line carries both halves at once:

    -            j = load_job(UUID(jid))
    +            j = load_job_plan(UUID(jid))

The callee is renamed onto the unified store and the `UUID` argument is carried straight
in. The reason is structural rather than accidental: rule T7, the only rule in the
transform that knows about `UUID(...)` at all, is reached only from `rewrite_id_value`,
which the transform calls on a CONSTRUCTOR KEYWORD. `job_id = UUID(job_id_str)` is a bare
assignment, so no rule keyed on a constructor can see it.

## 6. The candidate fourth rule was BUILT, APPLIED and RUN — and it does not close them

The narrowest rule that could close the seam by rewriting is T7's unwrap widened from a
constructor keyword to any call position: `UUID(<expr>)` becomes `<expr>` under
`apps/cli/`. It was applied to the flipped worktree — 49 calls in 17 files, none skipped,
none left unparsable — and the same scoped selection was run three times:

| run | REAL exit | result | `SystemExit` | hex UUID | operand `/` |
|---|---:|---|---:|---:|---:|
| CONTROL, base worktree | 0 | 1345 passed | 0 | 0 | 0 |
| FLIPPED | 1 | 263 failed, 1082 passed | 62 | 3 | 17 |
| FLIPPED + the candidate rule | 1 | 249 failed, 1096 passed | 52 | 1 | 16 |

THE CONTROL IS A REAL EXIT 0 AT 1345 PASSED, so the selection can pass and the reading is
a difference rather than a constant.

    the candidate rule FIXED 16 and BROKE 2; 247 survive
      BROKE  tests/cli/test_context_inspect_cli.py::test_handler_invalid_job_id
      BROKE  tests/cli/test_propose_cli.py::TestProposeMaterializeHandler::test_materialize_non_approved_fails

THE TWO IT BROKE ARE THE RULING. Both assert the "invalid job ID" guard, and the unwrap
DELETES that guard: `UUID(job_id_str)` in a handler is a VALIDATION, not a coercion, and a
rewrite that removes it trades a wrong id shape for no check at all. A rule family of
DECISION F275 D32's kind renames a field and changes no behaviour; this one cannot be
written without changing behaviour, which is the definition of the thing it is not.

And it barely moves the number. 247 of 263 survive, every surviving `SystemExit` is at
`data_paths.py:324` under `no job matches prefix`, and every surviving `unsupported
operand` is at `data_paths.py:200`.

## 7. The seam, counted

Over 328 tracked `.py` files under `apps/` and `packages/`, by `ast` and keyed by
enclosing SCOPE rather than by line number, per finding `R-0879`:

    every `UUID(...)` call                     : 105
    sites that BIND a UUID and pass it on      :  75  over 39 scopes in 18 files
      under apps/cli/                          :  58
      outside apps/cli/                        :  17
    the callees that RECEIVE a UUID object     :  load_job 29 · load_run_events 14 · str 12 · _emit 9

The 17 outside `apps/cli/` are why the candidate rule left 16 `unsupported operand` lines
standing: three of them pass a `UUID` into `load_job` and two into `load_job_safe`, in
`test_execution_service.py`, `proposed_tasks.py`, `mission_state.py` and `ui_server.py`,
and a rule scoped to the handler layer never reaches them.

## 8. What this settles, and what it does not

SETTLED: the three classes are not a fourth rule family and not a data migration. They are
ONE id-SHAPE seam with two halves — a resolver that searches only the classic store, and a
handler layer that parses its argument into a `uuid.UUID` and hands the OBJECT to the
store. Both halves are BEHAVIOUR, so both are production-code work and neither is
reachable by the transform. That work already has a home: the resolver collapse DECISION
F260 D5 places in T003, which F275's own feature file carries and which no round has
started.

NOT SETTLED, and stated so rather than implied. The 650 is a count of E-LINES and not of
distinct failures: a `-q --tb=line` run prints no per-test header, so this artefact cannot
attribute an E-line to a node id and does not claim to — the one place a distinct-failure
count exists here is the scoped table of section 6, where it is 263. The scoped selection
is `tests/cli/` alone and is not the suite; it was chosen because it holds the handler
layer, and the whole-suite figures stay round 61's. The 42 errors are still undiagnosed and
were not touched. And nothing here says the flip is ready — it says the remaining blockers
are a known piece of T003's own scope rather than an unknown fourth rule.
