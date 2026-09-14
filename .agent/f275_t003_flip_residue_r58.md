# F275 T003 — the id VALUE family, and the defect it exposed in the ruled site set itself

> Measured by the reviewer at `bf5ec6a4`, this round's base, in three disposable `git
> worktree`s under the gitignored `.remedy-wt/`, all removed and pruned before this text
> was authored. THIS FILE RECORDS A DRY RUN; IT FLIPS NOTHING. No line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it. It replaces
> none of `.agent/f275_t003_flip_residue.md`, `_r50.md` or `_r55.md`, which record the runs
> at `978046fe`, `020b1d57` and `08feacae` and stay as written.

## 1. What this round implemented, and the one thing it could not

DECISION F275 D32 names three retype rule families. This round built the FIRST — the id
VALUE at a target construction — in both its halves, and deliberately built neither of the
other two. The reason for stopping at one is in section 5: the `.status.value` family
cannot be resolved by any reading this round had, and guessing it by receiver name is the
heuristic DECISION F275 D29's P1 was written to kill.

**THE JOB HALF IS MECHANICAL.** `data_paths.mint_job_id()` returns `uuid4().hex[:16]`,
which is the sixteen-hex shape DECISION F260 D2 rules, so `Job(id=uuid4())` becomes
`JobPlan(job_id=mint_job_id())` and nothing else changes. Three shapes carry the value and
all three are rewritten: the direct call at 74 sites, a local bound to `uuid4()` and then
passed at 11, and a `UUID(x)` coercion unwrapped to `x` at 6. One site is left alone and
reported.

**THE TASK HALF IS NOT A MINT AT ALL, AND THAT IS THE ROUND'S FIRST FINDING OF METHOD.**
`TaskEntry.task_id` is assigned `f"T{parse_idx + 1:03d}"` in
`packages/orchestration/pingpong_job.py` under a comment reading "Deterministic ID by parse
order, not heading number", and the field's own declaration carries `# T001, T002, ... (by
parse order)`. So a task's unified id is an ORDINAL SCOPED TO ITS JOB, and a `uuid4()` has
no counterpart in it — the flip is not retyping a value here, it is replacing an identity
with a position. That is rulable only because the position turned out to be VISIBLE:

    `Task(id=...)` sites: 15  — 14 in test helper factories, 1 in production
      12  a list literal          the element index IS the position
       2  a comprehension         `for i in range(task_count)`, so the index is `i`
       1  a lone append           the only task its function builds, so position 1
    every one of the 15 has exactly ONE `Task(id=)` construction in its enclosing function

The production site is `packages/orchestration/continue_from_node.py`, which builds a child
job holding a single task, so its ordinal is `T001` and is not a judgement call. DECISION
F275 D34 rules the mapping; this artefact measured it.

## 2. What the transform did

| reading | measured |
|---|---:|
| files rewritten | 262 |
| files left unparsable by the edit | 0 |
| `git diff --shortstat` insertions | 5182 |
| `git diff --shortstat` deletions | 5009 |
| changed files under `packages/` or `apps/` | 99 |
| changed files under `tests/` | 163 |
| `pytest tests/ -q --co` collected | 18409 |
| collection errors | 0 |

New or changed since the run at `08feacae`: T7 job id minted 74, T7 job id minted via a
local 11, T7 job id `UUID()` unwrapped 6, T7 job id left alone 1, T7 task ordinal from a
literal 12, from a comprehension 2, from a lone construction 1, and I5 minter import added
39. Rule I5 is the seam rule I3 arriving through a VALUE: rewriting a construction to call
`mint_job_id()` while leaving the name unbound is the same `NameError` I3 records for
`save_job_plan`, so the import travels with the minter. T2 reads 1759 and T3 384, against
1786 and 411 at `08feacae` — section 4 is why those two numbers FELL, and it is not a
better reading.

## 3. The run, against a control at the same commit

    $ python3 -B -m pytest tests/ -q --tb=line -p no:randomly -p no:cacheprovider
    CONTROL  1 failed, 18379 passed, 29 skipped, 1 warning in 1299.14s       REAL_EXIT=1
    FLIPPED  1476 failed, 16862 passed, 29 skipped, 1 warning,
             42 errors in 1249.19s                                           REAL_EXIT=1

The control's one failure is the `test_vitest_passes` node that needs the gitignored
`apps/ui/node_modules`, and it is the ONE failure shared by both runs. Differencing the
node-id sets gives 1475 failures and all 42 errors caused by the flip.

| class | R55 | R58 |
|---|---:|---:|
| `TypeError: JobPlan.__init__() got an unexpected keyword argument 'X'` | 0 | 0 |
| `AttributeError: 'X' object has no attribute 'X'` | 127 | 424 |
| `TypeError: unsupported operand type(s) for /: 'X' and 'X'` | 379 | 90 |
| `ValueError: badly formed hexadecimal UUID string` | 194 | 223 |
| `SystemExit: N` | 306 | 337 |
| `TypeError: TaskEntry.__init__() got an unexpected keyword argument 'X'` | 25 | 25 |

THE TWO COLUMNS ARE NOT TAKEN AT THE SAME BASE and the table says so rather than implying
otherwise: R55 ran at `08feacae` and R58 at `bf5ec6a4`, with round 57's seven-record
retype between them. The comparison is honest for the classes section 4 attributes and is
offered as a direction, not as a difference.

THE RULE FAMILY DID WHAT IT WAS BUILT TO DO. The `unsupported operand` class falls from
379 to 90, which is the `PosixPath / UUID` join at `data_paths.py` no longer being handed
a `UUID`. The errors fall from 79 to 42. AND THE TOTAL WENT UP, from 1331 failures to
1475, which section 4 explains in full.

## 4. THE DEFECT THIS RUN FOUND, and it is in the method rather than in the flip

**THE RULED SITE SET IS KEYED BY LINE NUMBER, AND THIS BRANCH'S OWN LATER COMMITS MOVE THE
LINES.** `.agent/f275_t003_descriptor_sites.md`'s set R is 2198 sites keyed by
`(path, line, col, attr)` and was measured at `a815c9a3`. Round 57's migration — ordered by
DECISION F275 D33, and correct — deleted six import lines and rewrote thirty-five lines
across seven modules. Every ruled site BELOW one of those deletions moved, and the
transform then renamed nothing there.

    ruled sites 2198 | still resolving at `bf5ec6a4` 2144 | DRIFTED 54
      21  packages/orchestration/long_run_executor.py
      12  packages/orchestration/task_runner.py
      11  packages/orchestration/agent_loop.py
       7  packages/orchestration/dag_schedule.py
       3  packages/orchestration/verifier.py
    of the drifted, in the seven files round 57 edited: 54
    of the drifted, anywhere else:                       0

The attribution is not a suspicion. Of the 255 `JobPlan`-receiver attribute-error lines the
run produced, 235 are attributed to a source line inside three of those five files —
`long_run_executor.py` at 112, of which 109 are its line 1355; `task_runner.py` at 69, of
which 65 are its line 127; and `agent_loop.py` at 53, spread over five lines. The remaining
20 are elsewhere and are not claimed for this cause. Fifty-four unrenamed reads in code
every test exercises is what took the `AttributeError` class from 127 to 424.

**A KEY THAT DOES NOT MOVE WITH THE LINES RECOVERS ALL OF THEM, AND THAT WAS MEASURED
BOTH WAYS RATHER THAN ASSERTED.** Re-keying each ruled site by
`(path, enclosing function, attr, occurrence index of that attr within that function)` at
`a815c9a3` and resolving it at `bf5ec6a4`:

    by (line, col, attr)         : 2144 recovered, 54 lost
    by (scope, attr, occurrence) : 2198 recovered,  0 lost

The line key is the control and it loses exactly the 54 the drift measurement found, which
is what makes the second row a reading rather than a hope.

## 5. Why the other two rule families were NOT built

**THE `.status.value` FAMILY CANNOT BE RESOLVED BY ANYTHING THIS ROUND HAD.** 76 sites, 46
of them production, over ten distinct receiver names: `t` 39, `record` 18, `task` 10,
`latest` 2, an unnamed expression 2, and `c`, `proposed`, `ptask`, `held` and `released` at
one each. `record`, `latest`, `c`, `held` and `released` decide nothing by name, and the
ruled site set covers `id`, `name` and `description` only — `status` was never in it. So
this family needs its own type resolution, of exactly the shape round 53 built for the
other three fields: the DECISION F272 D7 descriptor probe over every candidate receiver,
run twice, unioned with a static sweep. That is a round, and pretending otherwise would
reintroduce the receiver-name heuristic D29's P1 exists to have killed.

**THE `.hex`/`.int` FAMILY IS SMALLER THAN IT LOOKED AND IS ALREADY PARTLY DONE.** Round
57 removed the one production reader it had, `task_runner.py`'s `result.task_id.hex[:8]`,
and added a ratchet that keeps the shape out. What remains is three sites in tests, all of
them lines the flip rewrites anyway.

## 6. What this reading does NOT settle

THE RESIDUE IS CLASSIFIED, NOT EXHAUSTED. The six classes above account for 1099 of the
1469 matched E-lines, and 1469 is itself smaller than 1475 failures plus 42 errors, because
a failure whose line the pattern did not match is not counted. That remainder is given NO
numeral beyond the two totals, because none was measured.

WHETHER RE-KEYING RECOVERS THE RUN IS NOT ESTABLISHED. Section 4 proves the key recovers
the SITES; nothing here re-ran the suite against a re-keyed transform, so the claim stops
at the site count and does not reach the residue.

THE 42 ERRORS ARE NOT DIAGNOSED. They fell from 79 without this round attributing the
fall, and an unattributed improvement is reported as unattributed.

NOTHING HERE RULES THE ROUTE. Whether the set is re-keyed, re-derived at the flip's own
base, or both, is a choice and belongs in `.agent/decisions.md`.
