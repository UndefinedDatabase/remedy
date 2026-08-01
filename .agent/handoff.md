# Handoff — F061 R2 (R-0164 + T003 + T004)

Review of `785f8cbd..HEAD` (branch `feature/f061-dod-compiler`), HEAD `d76a8f32`.

The feature's build work is complete: T001–T004 all landed. Every ordered gate
ran green; no gate went red at any point, so the block ran to the end.

---

## Commits

### 1 — `67c9253d` chore(f061): persist R1 verdict + register R-0164

| path | +/- | reason |
| --- | --- | --- |
| `.agent/authored/f061-r2-1.md` | +52/-0 | authored live_review text |
| `.agent/authored/f061-r2-2.md` | +34/-0 | authored plan text |
| `.agent/authored/f061-r2-3.md` | +61/-0 | authored context text |
| `.agent/context.md` | +37/-31 | full replacement, byte copy of f061-r2-3 |
| `.agent/last_block.md` | +200/-171 | this round's block recorded verbatim |
| `.agent/live_review.md` | +34/-5 | full replacement, byte copy of f061-r2-1 |
| `.agent/plan.md` | +18/-16 | full replacement, byte copy of f061-r2-2 |

### 2 — `af5c39d7` fix(f061): refuse flag-shaped selector, tool and argv[0] (R-0164)

| path | +/- | reason |
| --- | --- | --- |
| `packages/orchestration/dod_schema.py` | +20/-2 | `_reject_flag_shaped` applied to the three named fields |
| `tests/orchestration/test_dod_compiler.py` | +41/-0 | one negative test per field, plus the whitespace and the still-legal cases |

### 3 — `b1013412` chore(f061): mark R-0164 done in the finding ledger

| path | +/- | reason |
| --- | --- | --- |
| `.agent/live_review.md` | +1/-0 | the ordered `Done: R-0164 (commit af5c39d7).` line, nothing else |

### 4 — `09a8597e` feat(f061): runtime_flow runner on the F007 harness

| path | +/- | reason |
| --- | --- | --- |
| `packages/orchestration/dod_runners.py` | +331/-35 | flow runner; registry now dispatches executors, `ARGV_BUILDERS` keeps the argv kinds |
| `tests/orchestration/fixtures/dod/flow_app.py` | +57/-0 | the tiny harness-startable fixture app (stdlib only) |

### 5 — `5aefa675` test(f061): runtime_flow proven red and green

| path | +/- | reason |
| --- | --- | --- |
| `tests/orchestration/fixtures/dod/api_service.json` | +5/-5 | api-smoke steps moved to the v1 action vocabulary (draft + golden together) |
| `tests/orchestration/test_dod_runners.py` | +217/-14 | the flow suite; the loud-unsupported-kind class rewritten around a kind with no runner |

### 6 — `52cc9ff9` feat(f061): job-end DoD gate

| path | +/- | reason |
| --- | --- | --- |
| `packages/orchestration/dod_gate.py` | +289/-0 | the gate rule, evidence-area storage, the matrix |
| `packages/orchestration/job_fulfillment.py` | +33/-0 | the ONE seam + three additive record fields |

### 7 — `43b29c62` feat(f061): report check matrix and `remedy job dod`

| path | +/- | reason |
| --- | --- | --- |
| `apps/cli/command_catalog.py` | +11/-0 | the `job.dod` catalog entry |
| `apps/cli/commands/job.py` | +79/-0 | `_cmd_job_dod` + its dispatch entry |
| `packages/orchestration/run_report.py` | +77/-0 | `DoDCheckRow`, the matrix section, the collection side |
| `tests/orchestration/test_run_report.py` | +12/-0 | the three report goldens gain the new section |

### 8 — `d76a8f32` test(f061): gate rule, matrix, end-to-end, CLI

| path | +/- | reason |
| --- | --- | --- |
| `tests/orchestration/test_dod_gate.py` | +481/-0 | gate rule, storage, matrix, report section, end-to-end hold/release, CLI |

Every commit is under the 500-line limit; no oversize exception is claimed for
this feature.

---

## The T004 seam (declared, as ordered)

**Chosen seam: `job_fulfillment.run_job_fulfill`, immediately after
`JobFulfillmentContract.check()` and before `if passed and
record.staging_promoted:`** (`packages/orchestration/job_fulfillment.py:996`).

Why this one, and why only this one:

* `job.state = RunState.COMPLETED` is written in exactly one place in the
  fulfillment spine — inside the branch this line guards. Nothing can reach
  terminal green without passing the gate first, so the interception is
  provable by reading the branch rather than by hoping the call sites were all
  found.
* It sits AFTER promotion, so the checks run against the code as it will
  actually be, not against a pre-promotion snapshot.
* Holding is expressed by setting `passed = False` and appending one blocker,
  which routes into the EXISTING blocked branch: `record.status = BLOCKED`,
  staging discarded, `next_safe_action` set, and `job.state` left untouched.
  No second "blocked" mechanism was invented, and no lifecycle behaviour
  outside this one branch changed.
* `run_job_gate` returns `None` when the job has no stored DoD, so every
  existing job and every existing test behaves exactly as before. The gate can
  only ever turn a green job blocked — never the reverse.

`dod_gate.py` holds all the decision logic; the seam is 33 lines including the
three additive record fields and the timeline event.

---

## Verification transcripts (raw)

### Phase 1 gate — state-file readers

```
$ python3 -m pytest tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py -q
........................................................................ [100%]
72 passed in 13.92s
EXIT=0
```

### Phase 2 — R-0164, re-running the R1 gate

```
$ python3 -m pytest tests/orchestration/test_dod_compiler.py tests/orchestration/test_dod_runners.py -q
........................................................................ [ 75%]
.......................                                                  [100%]
95 passed in 1.97s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 14.92s
EXIT=0
```

### T003 gate

```
$ python3 -m pytest tests/orchestration/test_dod_compiler.py tests/orchestration/test_dod_runners.py -q
........................................................................ [ 66%]
....................................                                     [100%]
108 passed in 6.07s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 15.11s
EXIT=0
```

### T004 gate

```
$ python3 -m pytest tests/orchestration/test_dod_gate.py -q
................................                                         [100%]
32 passed in 2.06s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 15.40s
EXIT=0
```

### Done-when set (at `d76a8f32`)

```
$ python3 -m pytest tests/orchestration/test_dod_compiler.py tests/orchestration/test_dod_runners.py tests/orchestration/test_dod_gate.py -q
........................................................................ [ 51%]
....................................................................     [100%]
140 passed in 8.18s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 15.40s
EXIT=0

$ python3 -m pytest tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py -q
........................................................................ [100%]
72 passed in 13.56s
EXIT=0

$ git status --porcelain
(no output)
```

### Beyond the ordered gates — the suites this round's seam touches

Run because T004 edits `job_fulfillment.py`, `run_report.py` and the CLI, and a
gate that only proves its own tests green would prove very little:

```
$ python3 -m pytest tests/orchestration/test_job_fulfillment.py tests/orchestration/test_fence_production_e2e.py tests/orchestration/test_run_report.py -q
........................................................................ [ 36%]
........................................................................ [ 73%]
.....................................................                    [100%]
197 passed in 7.87s
EXIT=0

$ python3 -m pytest tests/cli/ -q
[...]
1231 passed in 197.06s (0:03:17)
EXIT=0

$ python3 -m pytest tests/docs/ -q
........................................................................ [ 98%]
.....                                                                    [100%]
293 passed in 0.19s
EXIT=0
```

The full-suite integration gate remains its own later round.

### Two reds seen during authoring, both fixed before the gates above

Recorded because they changed real files.

1. Adding the report section broke four goldens in `test_run_report.py`:

```
$ python3 -m pytest tests/orchestration/test_run_report.py -q
E       AssertionError: assert '# Run report...g is open)_\n' == '# Run report...g is open)_\n'
E         + ## Definition of Done
E         + Definition of Done: not recorded....
4 failed, 64 passed in 0.10s
```

The first repair attempt dropped a blank line and the same four stayed red;
the second inserted the section with the section spacing the renderer actually
produces. Now `68 passed`. See deviation 5 for why the goldens were edited at
all rather than the section suppressed.

2. The timeline reader is named `load_run_events`, not `read_run_events`:

```
E       ImportError: cannot import name 'read_run_events' from 'packages.orchestration.timeline'
1 failed, 31 passed in 2.14s
```

Fixed in the test.

### Lint (not an ordered gate; recorded as evidence)

```
$ python3 -m ruff check packages/orchestration/dod_schema.py packages/orchestration/dod_runners.py packages/orchestration/dod_gate.py packages/orchestration/run_report.py packages/orchestration/job_fulfillment.py apps/cli/commands/job.py apps/cli/command_catalog.py
All checks passed!
```

### Worktrees

No disposable worktree was created: no mutation red-proof was run this round.
Every red path is proven by a real failing process, a real 500 response, or a
real unreadable file — not by mutating a module.

```
$ git worktree list
/home/decodeux/Repos/remedy  d76a8f32 [feature/f061-dod-compiler]
```

---

## Authored-text proofs

```
$ sha256sum .agent/authored/f061-r2-1.md .agent/authored/f061-r2-2.md .agent/authored/f061-r2-3.md
47c01f1e8de3a1eb39cf9b69fc40fb57bc0a2b817c8ae91460eabefa958e7d6f  .agent/authored/f061-r2-1.md
a762a076567ea05419052e469b78f256768ba80458a8e98ad765c3c71b88162f  .agent/authored/f061-r2-2.md
3b808727fb2ec4412a9c24277dcd3fcd8328771c31909311adf15c48b10f23a3  .agent/authored/f061-r2-3.md
```

All three match their BEGIN-marker hashes exactly. As in R1 the payloads
arrived two-space indented from the transport; the unindented form hashes to
the marker value and the indented form does not, so the unindented text is the
authored text (R-0148 transport-wrap guard, resolved in favour of the hash).

```
$ cmp .agent/authored/f061-r2-2.md .agent/plan.md ; echo EXIT=$?
EXIT=0
$ cmp .agent/authored/f061-r2-3.md .agent/context.md ; echo EXIT=$?
EXIT=0
```

`live_review.md` differs from its authored file by EXACTLY the one line the
block ordered appended, and by nothing else:

```
$ diff .agent/authored/f061-r2-1.md .agent/live_review.md
30a31
>   Done: R-0164 (commit af5c39d7).
```

`docs/roadmap/` was not touched this round, as ordered:

```
$ git diff --stat 785f8cbd..HEAD -- docs/
(no output)
```

---

## What was built

**R-0164** — `validate_check_spec` now refuses a value whose first
non-whitespace character is `-` in the three positions that name a THING
rather than an option: a pytest `selector`, a lint/build `tool`, and
`custom_cmd` `argv[0]`. The message names the field and quotes the offending
value. A dash elsewhere is untouched: `npm-run`, `tests/test_a-b.py` and an
`args` list of `["-x"]` all still validate, and a test pins that.

**T003 — the runtime_flow runner.** A flow check drives the F007 harness:
`runtime_config.resolve_spec` answers how this project starts (explicit
`.remedy/config.toml` `[runtime]`, else exactly one detected runtime, else it
blocks honestly), `choose_port` picks the port without evicting a squatter, the
app is launched with the supervisor's own discipline (argv list, never a shell,
`start_new_session=True` so the family can be killed whole), `http_probe`
answers readiness, the declarative steps run in order, and
`stop_process_tree` stops the family in a `finally` — on success, on a red
step, and on an exception alike. A survivor is red with reason
`app_stop_failed`, so a leaked process can never read as a clean run.

v1 has exactly one action: `open` a path, optionally asserting `expect_status`
and/or `expect_text`. Anything else is red with `unknown_flow_action` — an
unrecognised action is never treated as satisfied. Named reds:
`runtime_not_configured`, `app_start_failed`, `app_not_ready`,
`flow_step_failed`, `unknown_flow_action`, `app_stop_failed`, `timeout`.

The registry now dispatches EXECUTORS (all five kinds); `ARGV_BUILDERS` keeps
the four single-process kinds. The loud-failure guarantee moved with it: a kind
with no runner still raises `UnsupportedCheckKindError`, now proven with a
synthetic kind rather than with `runtime_flow`, so the guarantee protects the
NEXT kind added instead of expiring with this round.

**T004 — the gate.** `evaluate_dod` runs every check (never stopping at the
first red — a partial matrix hides work) and applies one rule: any red BLOCKING
check holds; non-blocking reds are recorded in `reported_red` and gate nothing.
An unrunnable kind is red with reason `no_runner` and holds if blocking — the
gate degrades to honest, never to green. An unreadable stored DoD holds too:
fail closed.

The DoD and the gate result live in the job's evidence area under the data root
(`dod.json`, `dod_result.json`), never in the user's repo — asserted in a test.
The report renders the matrix from the recorded evidence and says `not
recorded` for a job that was never gated. `remedy job dod <id>` prints the same
matrix and is strictly read-only — a test asserts that invoking it does not
produce a gate result.

---

## Deviations & assumptions (A9)

1. **The app spec comes from the project's runtime configuration, not from the
   check.** The flow spec carries steps only; `resolve_spec(worktree)` answers
   how to start the app. Rationale: the DoD should not re-invent what F007
   already owns, and it keeps the schema unchanged (see 3). Consequence: a
   runtime_flow check on a project with no runtime configuration is red with
   `runtime_not_configured` rather than unrunnable-by-schema.

2. **The v1 action vocabulary is enforced by the RUNNER, not the schema.** The
   block scoped `dod_schema.py` to the R-0164 guard, so `validate_check_spec`
   still only requires a step to be an object with a non-empty `action`. An
   unknown action is therefore caught at run time, red and named, rather than
   at compile time. If the reviewer prefers compile-time rejection, that is a
   small follow-up in `_SPEC_KEYS`/step validation.

3. **The `api_service` fixture's api-smoke steps were rewritten** from the R1
   placeholders (`{"action": "start service"}`, `{"action": "GET /health"}`) to
   the v1 vocabulary, in the provider draft and the golden DoD together. The
   block ordered that flow proven red and green, which is only possible against
   a concrete vocabulary. The fixture's `note` was updated to match.

4. **The flow's application log goes to a private temporary directory**, not to
   a pipe and not to the evidence area. A pipe would need a log-pump thread to
   avoid a chatty app blocking on a full buffer; an ephemeral flow does not
   have the supervisor's lifetime to run one. The tail is folded into the
   evidence `output_tail` and the temporary directory is removed. A test
   asserts the worktree is byte-for-byte unchanged by a flow run.

5. **Four report goldens in `tests/orchestration/test_run_report.py` were
   updated.** Adding an ordered section to `run_report.py` necessarily changes
   every golden. The alternative — rendering the section only when a DoD
   exists — would have left existing goldens untouched but would break the
   module's own documented rule that every absent source renders `not
   recorded`, which is what lets a reader tell "no DoD" from "DoD forgotten".
   The convention was kept and the goldens updated; each gains exactly the
   three-line `not recorded` section.

6. **The gate holds via the existing blocked branch** rather than a new
   terminal state: `passed = False` plus one `dod_blocking_red:<ids>` blocker.
   This is why "held open" and "contract failed" look the same to every
   existing reader, and why the blocker string carries a distinguishing prefix.

7. **Three additive fields on `JobFulfillmentRecord`** (`dod_released`,
   `dod_blocking_red`, `dod_reported_red`). `dod_released` is `None` for a job
   that was never gated, which is distinct from `False`; records written before
   this feature load unchanged.

8. **A blocking check that holds the job discards staging**, because that is
   what the existing blocked branch does with a contract failure. "Releases
   after the fix" therefore means re-running fulfillment, which the end-to-end
   test does explicitly on the same job.

9. **`remedy job dod` shows the LAST recorded run and never runs checks.** A
   command that silently started a test suite would be a surprise from a read
   command; a test pins the read-only behaviour. A job whose gate has not run
   lists its checks as `not run` rather than printing an empty table.

10. **`run_checks` still returns evidence without a verdict.** All the deciding
    lives in `dod_gate.evaluate_dod`. That separation is what let T002's runners
    be proven red and green with no job anywhere near them, and it is preserved.

11. **No mutation red-proofs were run**, so no disposable worktree was created
    or pruned.

---

## Open items for the next round

- The integration gate round (`docs/agents/integration_gate.md`) — the full
  suite has not been run this round; the scoped and adjacent suites above have.
- Closure per `docs/roadmap/STATUS_closure_protocol.md`; `docs/roadmap/` is
  untouched so far and STATUS still reads `[~]`.
- Still open from R1: registering `dod_v1` in `SCHEMA_REGISTRY` (a one-line
  follow-up the reviewer accepted deferring), and — new — deciding whether the
  flow action vocabulary should move into compile-time validation (deviation 2).
- Nothing compiles a `runtime_flow` check yet: the compiler emits pytest checks
  for uncovered acceptance lines, and a provider may propose a flow. Generated
  flow specs written into the evidence area are therefore not yet a surface
  this feature touches.
