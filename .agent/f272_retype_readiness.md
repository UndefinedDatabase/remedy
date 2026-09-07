# F272 T002 — readiness for move three: retyping `JobPlan.state` to `RunState`

> EVIDENCE, not a prediction and not a plan. Every figure below was measured in
> F272 round 13 by the worker, on this machine, at `a9aa8fa7` (the tree the
> round started from; no `.py` file changed in round 13, so every reading also
> stands at the round's HEAD). Where the round 13 step block stated a reading,
> this file says whether the re-derivation REPRODUCES it or DIFFERS from it —
> an inventory that agrees with the block because it copied the block is worth
> nothing to the session that reads it.
>
> Companion file: `.agent/f272_state_rename_inventory.md`, the same class of
> artifact for move two.

## 1. What the retype changes

Measured by importing the SHIPPED module rather than by reading it:
`sys.path.insert(0, REPO)` then `import packages.core.models`, which resolved to
`/home/decodeux/Repos/remedy/packages/core/models.py`.

- Interpreter: **CPython 3.10.12 (main, Mar 3 2026, 11:56:32) [GCC 11.4.0]**.
- `RunState.__mro__` reads `RunState, str, Enum, object` — a str-mixin Enum, not
  a 3.11 `StrEnum`. The mixin is why almost nothing moves.

All readings are for `b = RunState.BLOCKED`.

| expression | result | vs the block |
|---|---|---|
| `str(b)` | `'RunState.BLOCKED'` | REPRODUCES |
| `f"{b}"` | `'blocked'` | REPRODUCES |
| `json.dumps({'s': b})` | `'{"s": "blocked"}'` | REPRODUCES |
| `json.dumps(b)` | `'"blocked"'` | REPRODUCES |
| `b == 'blocked'` | `True` | REPRODUCES |
| `isinstance(b, str)` | `True` | REPRODUCES |
| `b.value` | `'blocked'` | REPRODUCES |
| `'%s' % b` | `'RunState.BLOCKED'` | REPRODUCES |
| `{b: 'hit'}['blocked']` | `'hit'` — the member works as a dict key reachable by the plain word | REPRODUCES |

**So a retype changes EXACTLY TWO renderings, `str()` and `%s`.** It changes no
comparison, no `json.dumps` output, no f-string and no dict lookup. That is the
whole reason move three is a bounded change.

`RunState` has **nine** members at this tree, in declaration order: `PENDING`,
`PLANNED`, `RUNNING`, `PAUSED`, `COMPLETED`, `FAILED`, `CANCELLED`, `BLOCKED`,
`STOPPED`. REPRODUCES.

## 2. The rendering hazard, counted

Counted by `ast` — not by grep — over every tracked `.py` file enumerated from
`git ls-files -z '*.py'`. **1066 files enumerated, 0 of them unparseable.**

> DIFFERS: the block states 1065 tracked `.py` files. The count is 1066, and it
> is 1066 both at `a9aa8fa7` and at HEAD, cross-checked three ways —
> `git ls-files '*.py'`, `git ls-tree -r --name-only a9aa8fa7`, and
> `git ls-tree -r --name-only HEAD`. Round 13 changed no `.py` file, so the
> difference is not this round's. The direction is harmless: the sweep below
> read a superset of the block's file set, so the two counts it produces are, if
> anything, better supported than the block's.

**COUNT A — `'%s' % <x>.state` sites: ZERO.** REPRODUCES. Predicate: a `BinOp`
with a `Mod` operator whose left operand is a `str` `Constant` containing `%s`
and whose right operand subtree contains an `Attribute` named `state`.

**COUNT B — `str(<x>.state)` sites: TWELVE.** REPRODUCES, at exactly the twelve
paths and line numbers the block names. Predicate: a `Call` whose callee is the
bare `Name` `str`, with one positional argument and no keywords, that argument
being an `Attribute` named `state`.

| # | site | receiver | enclosing def | defensive idiom | enclosing def reads `job.id` |
|---|---|---|---|---|---|
| 1 | `apps/cli/commands/job.py:1201` | `job` | `_cmd_job_summary` | yes | yes |
| 2 | `apps/cli/commands/job.py:1650` | `job` | `_cmd_job_status` | yes | yes |
| 3 | `apps/cli/commands/job.py:1769` | `job` | `_cmd_job_run_report` | yes | yes |
| 4 | `apps/cli/commands/job.py:1808` | `job` | `_cmd_job_report` | yes | yes |
| 5 | `packages/orchestration/project_summary.py:78` | `job` | `build_project_summary` | yes | yes |
| 6 | `packages/orchestration/ui_server.py:1525` | `job` | `_build_job_plan_dashboard` | yes | yes |
| 7 | `packages/orchestration/ui_server.py:1697` | `job` | `_build_dashboard` | yes | yes |
| 8 | `packages/orchestration/ui_server.py:2635` | `job` | `_build_live_state_json` | yes | yes |
| 9 | `packages/orchestration/ui_view_model.py:638` | `job` | `build_next_action` | yes | yes |
| 10 | `packages/orchestration/ui_view_model.py:769` | `job` | `build_story` | yes | yes |
| 11 | `packages/orchestration/ui_view_model.py:994` | `job` | `build_checklist` | yes | yes |
| 12 | `tests/orchestration/test_dod_gate.py:305` | `job` | `_job_state` | yes | no — see below |

**ALL TWELVE ARE ALREADY SAFE, AND NONE IS A `JobPlan`.** REPRODUCES. The
evidence, in two parts:

*The idiom.* Every one of the twelve is the same defensive expression, quoted
once with the receiver normalised:

    <x>.state.value if hasattr(<x>.state, "value") else str(<x>.state)

Measured as three distinct tightest statements — eleven bind it to a local
(`state = …`, once `state_val = …`) and one returns it — but ONE expression
shape, in all twelve. It takes `.value` when the object IS an enum and falls
back to `str()` only when it is not, so the retype makes the `.value` branch
live and the `str()` branch dead. That is the safe direction: these sites get
*more* correct, not less.

*The receiver.* A `JobPlan` has no `id`; its primary key is `job_id` (measured:
`JobPlan`'s annotated fields include `job_id` and do not include `id`). Eleven
of the twelve sit in a function that reads `job.id` and none reads `job.job_id`,
so their receiver is the classic `packages/core/models.Job`, whose `state` field
is annotated `RunState` and which therefore already carried a `RunState` before
F272 began. The twelfth needed a caller to settle it:
`tests/orchestration/test_dod_gate.py:305` is the one-line helper
`def _job_state(self, job_id: str, tmp_path: Path) -> str`, which builds its
receiver as `load_job(UUID(job_id), tmp_path)` from
`packages.orchestration.storage`, and whose six call sites in that same file all
pass `str(job.id)`. Classic `Job` as well.

## 3. The three record boundaries

The three places a state leaves the record, in
`packages/orchestration/pingpong_job.py` (3650 lines at `a9aa8fa7`). Each line
was printed from `git show a9aa8fa7:…` and compared to the block's quotation;
all three REPRODUCE verbatim once leading indentation is stripped.

| line | enclosing def | text at `a9aa8fa7` | move three |
|---|---|---|---|
| 667 | `_export_job` | `"status": job.state,` | spell `.value` |
| 2968 | `export_job_report` | `"status": job.state,` | spell `.value` |
| 3026 | `format_job_report_text` | `f"Status: {job.state}",` | leave alone — an f-string already renders the plain word |

**A MEASUREMENT THE BLOCK DID NOT ORDER AND THE NEXT ROUND NEEDS.** Round 10's
rendering guard, `test_a_blocked_job_renders_and_exports_as_the_plain_word_blocked`
in `tests/orchestration/test_job_state_field.py:80-90`, does **not** bite on a
missing `.value` at lines 667 and 2968. Measured in memory by standing
`RunState.BLOCKED` where `_export_job(job)["status"]` would put it and evaluating
the guard's own three assertions:

| the guard's assertion | with a bare `RunState.BLOCKED` |
|---|---|
| `f"{job.state}" == "blocked"` (line 88) | True |
| `_export_job(job)["status"] == "blocked"` (line 89) | True |
| `isinstance(_export_job(job)["status"], str)` (line 90) | True |
| and `json.dumps` round-trips it to the plain word | True |

So the `.value` at those two boundaries is required by DECISION F272 D5's
intent — the stored record holds a plain `str` — and **not** by any assertion
that exists today. A block ordering move three must either add the assertion
that discriminates (`type(_export_job(job)["status"]) is str`, which is False
for a `RunState` member and True for `.value`) or state plainly that the two
`.value` edits are ungated. Ordering the existing guard as the proof that the
boundaries were spelled correctly would be a gate that cannot fail.

## 4. The six constants and their blast radius

At `packages/orchestration/pingpong_job.py`, read from the parsed module — each
is a module-level `Assign` to a bare `Name` whose value is a `str` `Constant`:

| constant | line | value |
|---|---|---|
| `JOB_PLANNED` | 65 | `'planned'` |
| `JOB_RUNNING` | 66 | `'running'` |
| `JOB_BLOCKED` | 67 | `'blocked'` |
| `JOB_COMPLETED` | 68 | `'completed'` |
| `JOB_PAUSED` | 69 | `'paused'` |
| `JOB_STOPPED` | 73 | `'stopped'` |

`JOB_STOPPED` sits at 73 rather than 70 because a three-line F011 comment
separates it. The block's "lines 65 to 73" is the correct span. REPRODUCES.

Blast radius, by this exact command:

    git grep -l -E "JOB_PLANNED|JOB_RUNNING|JOB_BLOCKED|JOB_COMPLETED|JOB_PAUSED|JOB_STOPPED" \
        a9aa8fa7 -- packages/ apps/ tests/

**29 files.** The same command with `-w` (word-boundary) returns the same 29, so
no hit is a substring of a longer identifier.

> DIFFERS: the block states 27. The measured figure is 29, and the list is given
> in full below so the next block author can gate on a set rather than on a
> number. Nothing under `apps/` matches at all — the whole radius is six
> `packages/orchestration/` modules and 23 test modules.

Production (6):
`packages/orchestration/job_evidence.py`,
`packages/orchestration/job_promote.py`,
`packages/orchestration/long_run_executor.py`,
`packages/orchestration/pingpong_job.py`,
`packages/orchestration/self_use_findings.py`,
`packages/orchestration/self_use_runner.py`.

Tests (23):
`tests/cli/test_job_rerun_manifest.py`,
`tests/cli/test_job_stop.py`,
`tests/orchestration/test_episode_snapshot_lifecycle.py`,
`tests/orchestration/test_escalation.py`,
`tests/orchestration/test_f018_authority_integration.py`,
`tests/orchestration/test_f018_package_pipeline_e2e.py`,
`tests/orchestration/test_job_evidence.py`,
`tests/orchestration/test_job_promote_consistency.py`,
`tests/orchestration/test_job_state_field.py`,
`tests/orchestration/test_job_stop_integration.py`,
`tests/orchestration/test_job_task_runner.py`,
`tests/orchestration/test_job_worktree_handoff.py`,
`tests/orchestration/test_job_worktree_integration.py`,
`tests/orchestration/test_job_worktree_integrity.py`,
`tests/orchestration/test_long_run_executor.py`,
`tests/orchestration/test_pingpong_integration.py`,
`tests/orchestration/test_predictive_budget.py`,
`tests/orchestration/test_run_manifest_reference_coverage.py`,
`tests/orchestration/test_run_manifest_runtime_truth.py`,
`tests/orchestration/test_run_manifest_terminal_consistency.py`,
`tests/orchestration/test_run_manifest_zero_call_expectations.py`,
`tests/orchestration/test_run_state_covers_job_status.py`,
`tests/orchestration/test_self_use_runner.py`.

The three files in this list that move two never touched —
`long_run_executor.py`, `test_long_run_executor.py`, `test_escalation.py` — are
exactly the ones a reader of `.agent/f272_state_rename_inventory.md` would not
expect, because they reference the constants without reading `JobPlan.state`.

## 5. The assertions move three inverts

In `tests/orchestration/test_job_state_field.py` at `a9aa8fa7` (90 lines):

| test | line | assertion | after the retype |
|---|---|---|---|
| `test_nothing_was_retyped` | 53 | `assert type(JobPlan().state).__name__ == "str"` | goes RED — invert it to `"RunState"` |

Its own docstring reads *"Move two renames; move THREE retypes. A ``RunState``
here means they merged."* — so inverting it is the intended move and not a
weakening.

> DIFFERS, in kind rather than in number: the block says "THE TWO ASSERTIONS
> MOVE THREE MUST INVERT, **both in** `tests/orchestration/test_job_state_field.py`",
> naming `test_nothing_was_retyped` and "G4(v)'s companion reading
> `isinstance(..., RunState)` is False". Read line by line, that file contains
> exactly ONE assertion move three must invert — line 53. The companion is a
> READING taken by round 10's gate G4(v), not a line in the file; nothing in the
> file asserts `isinstance`, and the only `isinstance` there is line 90's
> `isinstance(_export_job(job)["status"], str)`, which stays TRUE after the
> retype (see section 3) and must NOT be inverted. A block that orders "invert
> the two assertions in that file" would send its worker looking for a line that
> does not exist.

Every other assertion in that file survives the retype unchanged, measured
against the str-mixin readings of section 1: line 44/45 (`status` is gone) is
about the NAME; line 49 (`JobPlan().state == JOB_PLANNED == "planned"`) holds
because a str-Enum member equals its value; lines 88-90 hold for the reason
section 3 gives.

## 6. What must NOT change

- **The stored JSON key stays `"status"`** — DECISION F272 D5. `_export_job`
  emits `"status"` and `_import_job` reads `data.get("status", JOB_PLANNED)`, so
  every record already on disk still loads. Pinned by
  `test_the_exporter_still_writes_status_and_never_state` (line 57) and
  `test_the_importer_reads_the_old_key_into_the_new_field` (line 63).
- **The six `JOB_*` constants keep their NAMES and their VALUES** even as their
  type changes. `JOB_BLOCKED` must still equal `"blocked"`; because a str-Enum
  member compares equal to its value, every `== JOB_BLOCKED` comparison in the
  29 files above survives without an edit.
- **`f"{job.state}"` must still render the plain word.** That is the guard round
  10 shipped, line 88, and section 1 shows an f-string is one of the renderings
  a retype does not move.
- **Nothing merely CONTAINING `status`** — `TaskEntry.status`,
  `ApplyManifest.status`, `job_status`, `final_status`,
  `worktree_cleanup_status` — is in scope. That boundary is
  `.agent/f272_state_rename_inventory.md`'s and it still holds.

## 7. The open clauses move three inherits

Three counter-measures in `.agent/live_review.md` bind a block that orders move
three. None is discharged by round 13.

1. **R-0821 (RESOLVED at round 12, clause survives).** A block changing
   `RunState`, the `JOB_*` constants or any state vocabulary NAMES
   `tests/ui_contracts/` in its gate list, because that suite is the only reader
   in this repository that checks the enum against the cockpit. Move three
   changes the `JOB_*` constants, so the clause fires.
2. **R-0820 (OPEN).** Binding on any block that orders a mechanical edit over a
   set the block itself defines: *the gate MUST NOT be computed from the same
   predicate as the change set*, and where it is, the block says so and adds an
   independent gate that can see what the predicate misses. Move three's change
   set is defined by a predicate over `JobPlan` receivers; its gate must not be
   the same predicate. Section 3's finding is the same hazard in a second place:
   the existing rendering guard cannot see the `.value` edits at all.
3. **R-0819 (OPEN, owed by T003 and T004).** The shadow-property gate is to be
   stated as "zero call sites whose callee is a bare `Name` of `run_dir` or
   `runs_dir` and whose line number is strictly less than the first binding of
   that name in the enclosing function scope", measured by `ast` over every
   tracked `.py` file from `git ls-files`, and RUN AT THE BASE BEFORE BEING
   ORDERED. That last clause — run every gate at its base first — is what move
   three most needs, given section 3.

## 8. The method

The site set of a polymorphic attribute is not derivable from the source; it is
derivable from a RUN. DECISION F272 D7's probe is the instrument, and
`.agent/f272_state_rename_inventory.md` records exactly how it is driven — the
field replaced by a property whose getter, setter and constructor path log the
CALLING frame, run in `forward` mode to enumerate and in `raise` mode to prove
convergence at EXIT 0 with an empty site log, plus the receiver-TYPE sweep and
the stand-in reading for the sites no run reaches.

For move three that instrument is *cheaper than it was for move two*, and this
file says why: sections 1 and 2 show the retype has only two rendering effects,
that neither occurs on a `JobPlan` anywhere in 1066 tracked files, and that the
twelve `str()` sites are classic-`Job` sites already guarded by the `hasattr`
idiom. The expensive part of move two was finding an unbounded site set. Move
three's site set is the three lines of section 3, the six constants of section 4
and the one assertion of section 5 — bounded, and listed here by path and line.

What the probe is still needed for is the direction this file cannot close: a
site that *constructs* a `JobPlan` with a plain string, or that compares
`job.state is JOB_BLOCKED` by identity rather than by equality. Identity
comparison is the one shape a str-Enum breaks silently, because `==` keeps
working while `is` stops. No count of that shape was ordered by round 13's
block and none is claimed here.
