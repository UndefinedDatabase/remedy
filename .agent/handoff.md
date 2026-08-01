# Handoff — F061 R1 (T001 + T002)

Review of `1869d89a..8e3f50dc` (branch `feature/f061-dod-compiler`).
Base: `main` after PR #171 merge (F056).

Both slice gates pass. Nothing was left blocked; no gate went red at any
point in the round.

---

## Phase 0 — Open PR Gate

```
$ git status --porcelain
(no output)
EXIT=0

$ gh pr list --state open --json number,headRefName,baseRefName,isDraft
[{"baseRefName":"main","headRefName":"feature/f056-missions","isDraft":false,"number":171}]
```

Exactly one open PR, from `feature/*` into `main`, not a draft — merge is the
gate's prescribed action.

```
$ gh pr merge 171 --merge --delete-branch
! Pull request UndefinedDatabase/remedy#171 was already merged
From github.com:UndefinedDatabase/remedy
 * branch              main       -> FETCH_HEAD
   78f5f608..1869d89a  main       -> origin/main
Updating 78f5f608..1869d89a
Fast-forward
 [...39 files changed, 3780 insertions(+), 175 deletions(-)]
EXIT=0
```

Deviation, declared: the FIRST invocation of `gh pr merge 171` merged the PR
remotely and then failed on its own local step, because saving this round's
block to `.agent/last_block.md` (ordered as the first action of the block) had
left that tracked file modified:

```
failed to run git: error: Your local changes to the following files would be overwritten by checkout:
	.agent/last_block.md
Please commit your changes or stash them before you switch branches.
Aborting
EXIT=1
```

Recovery, no content lost: the block copy was parked in the session scratchpad,
`git checkout -- .agent/last_block.md` restored the tracked file, `git status
--porcelain` was empty again, and the merge command was re-run (reporting
"already merged" and completing the local fast-forward to `1869d89a`). The
parked copy was then restored onto the new branch and committed in commit 1.
Net effect on the repository is exactly what the gate ordered.

---

## Commits

### 1 — `bd1c6da2` chore(f061): claim F061 — STATUS [~] + state reset

| path | +/- | reason |
| --- | --- | --- |
| `.agent/authored/f061-r1-1.md` | +4/-0 | authored STATUS FROM/TO text, saved verbatim |
| `.agent/authored/f061-r1-2.md` | +23/-0 | authored live_review text |
| `.agent/authored/f061-r1-3.md` | +32/-0 | authored plan text |
| `.agent/authored/f061-r1-4.md` | +55/-0 | authored context text |
| `.agent/context.md` | +40/-35 | full replacement, byte copy of f061-r1-4 |
| `.agent/last_block.md` | +239/-117 | this round's block recorded verbatim |
| `.agent/live_review.md` | +16/-71 | full replacement, byte copy of f061-r1-2 |
| `.agent/plan.md` | +24/-20 | full replacement, byte copy of f061-r1-3 |
| `docs/roadmap/STATUS.md` | +1/-1 | the F061 claim line only |

### 2 — `b85bd07c` feat(f061): DoD schema

| path | +/- | reason |
| --- | --- | --- |
| `packages/orchestration/dod_schema.py` | +260/-0 | versioned DoD schema, draft/compiled split, compile-time spec validation |

### 3 — `4611c146` feat(f061): DoD compiler

| path | +/- | reason |
| --- | --- | --- |
| `packages/orchestration/dod_compiler.py` | +450/-0 | three-source merge, traceability rule, deterministic fallback, standard-check registry seam |

### 4 — `ce9a573b` test(f061): three long-goal DoD fixtures

| path | +/- | reason |
| --- | --- | --- |
| `tests/orchestration/fixtures/dod/api_service.json` | +172/-0 | fixture mission: fully covered by the provider, uses all five kinds |
| `tests/orchestration/fixtures/dod/cli_tool.json` | +128/-0 | fixture mission: partial coverage, non-blocking check, selector collapse |
| `tests/orchestration/fixtures/dod/docs_site.json` | +137/-0 | fixture mission: one acceptance line left for the compiler to cover |

### 5 — `1da138a0` test(f061): schema round-trip and nonsense-spec rejection

| path | +/- | reason |
| --- | --- | --- |
| `tests/orchestration/test_dod_compiler.py` | +230/-0 | `TestSchema`, `TestNonsenseSpecRejection` |

### 6 — `8ca9a422` test(f061): traceability, goldens, fallback, registry

| path | +/- | reason |
| --- | --- | --- |
| `tests/orchestration/test_dod_compiler.py` | +281/-0 | `TestTraceability`, `TestGoldenFixtures`, `TestFallbackLabeling`, `TestProviderContract`, `TestStandardCheckRegistry` |

### 7 — `d64c344a` feat(f061): DoD runners

| path | +/- | reason |
| --- | --- | --- |
| `packages/orchestration/dod_runners.py` | +308/-0 | per-check execution and evidence, named red reasons, loud unsupported kind |

### 8 — `8e3f50dc` test(f061): runner kinds red and green

| path | +/- | reason |
| --- | --- | --- |
| `tests/orchestration/test_dod_runners.py` | +356/-0 | four kinds red+green, tool_unavailable, evidence shape, runtime_flow loud failure |

Every commit is under the 500-line limit. The test module
`tests/orchestration/test_dod_compiler.py` (511 lines total) was therefore
landed in two commits along a real seam — schema-level proofs first, then the
compiler-level proofs — and the intermediate state passed on its own
(`29 passed`). No oversize-commit exception is claimed for this feature.

---

## Verification transcripts (raw)

### Commit 1 gate — docs round + canary

```
$ python3 -m pytest tests/docs/ -q
........................................................................ [ 49%]
........................................................................ [ 73%]
........................................................................ [ 98%]
.....                                                                    [100%]
293 passed in 0.19s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 15.16s
EXIT=0
```

### T001 gate (run at `8ca9a422`, before starting T002)

```
$ python3 -m pytest tests/orchestration/test_dod_compiler.py -q
..........................................................               [100%]
58 passed in 0.12s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 14.95s
EXIT=0
```

One test failed during authoring and was fixed before the gate run above —
recorded because it changed the test, not the module:

```
$ python3 -m pytest tests/orchestration/test_dod_compiler.py -q
.............................F............................               [100%]
_ TestTraceability.test_rule_text_is_verbatim_from_the_feature_file _
>       assert TRACEABILITY_RULE in FEATURE_FILE.read_text(encoding="utf-8")
E       AssertionError: assert 'every plan acceptance line traceable to a check id' in '# T1_F061 ...'
1 failed, 57 passed in 0.15s
```

Cause: the feature file hard-wraps that sentence across two lines
("…traceable to a\ncheck id."). The constant is the feature file's sentence;
the FILE is wrapped. Fix was in the test — it now unwraps the document
(whitespace only, `" ".join(text.split())`) before the containment check, so
every non-whitespace character must still match. The feature file was not
edited (out of this round's change scope).

### T002 gate (run at `8e3f50dc`)

```
$ python3 -m pytest tests/orchestration/test_dod_runners.py -q
...............................                                          [100%]
31 passed in 2.00s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 15.70s
EXIT=0
```

### Done-when set (run at `8e3f50dc`)

```
$ python3 -m pytest tests/orchestration/test_dod_compiler.py tests/orchestration/test_dod_runners.py -q
........................................................................ [ 80%]
.................                                                        [100%]
89 passed in 2.01s
EXIT=0

$ python3 -m pytest tests/docs/ -q
........................................................................ [ 98%]
.....                                                                    [100%]
293 passed in 0.19s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 15.70s
EXIT=0

$ git status --porcelain
(no output)
```

### Lint (not an ordered gate; recorded as evidence)

```
$ python3 -m ruff check packages/orchestration/dod_schema.py packages/orchestration/dod_compiler.py tests/orchestration/test_dod_compiler.py
All checks passed!

$ python3 -m ruff check packages/orchestration/dod_runners.py tests/orchestration/test_dod_runners.py
All checks passed!
```

### Worktrees

No disposable worktree was created this round: no mutation red-proof was run.
The red proofs the order asks for are real failing processes driven by the
tests themselves (a genuinely failing pytest file, non-zero exits, an absent
binary, a timeout), all inside `tmp_path`.

```
$ git worktree list
/home/decodeux/Repos/remedy  8e3f50dc [feature/f061-dod-compiler]
```

---

## Authored-text proofs

```
$ sha256sum .agent/authored/f061-r1-1.md .agent/authored/f061-r1-2.md .agent/authored/f061-r1-3.md .agent/authored/f061-r1-4.md
d362fe36dec188aaf5df2ec355272d69f4d723078a31df7f2692ee63989ede0f  .agent/authored/f061-r1-1.md
552f4d6643a097d35db839b284dd85fda657706de8874a9250b92220e1b0d9e8  .agent/authored/f061-r1-2.md
d204ac1ed3ced002a8ee785e0ef27774da71ebf2ab6d57fcd79b55a3c5725992  .agent/authored/f061-r1-3.md
fb02aa8585cd73ee4cbed9e74d2015007d038ea2fbfde526897b557927dd9175  .agent/authored/f061-r1-4.md
```

All four match their BEGIN-marker hashes exactly. The payloads arrived indented
by two spaces from the transport; the unindented form hashes to the marker
value and the indented form does not, so the unindented text is the authored
text (same transport-wrap resolution as R-0148: resolved in favour of the
hash).

```
$ cmp .agent/authored/f061-r1-2.md .agent/live_review.md ; echo EXIT=$?
EXIT=0
$ cmp .agent/authored/f061-r1-3.md .agent/plan.md ; echo EXIT=$?
EXIT=0
$ cmp .agent/authored/f061-r1-4.md .agent/context.md ; echo EXIT=$?
EXIT=0
```

STATUS line occurrence counts, `docs/roadmap/STATUS.md`:

```
BEFORE  FROM '- [ ] F061 — Definition-of-Done compiler' : 1
BEFORE  TO   '- [~] F061 — Definition-of-Done compiler' : 0
AFTER   FROM '- [ ] F061 — Definition-of-Done compiler' : 0
AFTER   TO   '- [~] F061 — Definition-of-Done compiler' : 1

$ grep -nF -- '- [~] F061' docs/roadmap/STATUS.md
41:- [~] F061 — Definition-of-Done compiler
```

The FROM/TO strings were read out of the saved authored file at apply time
(`Path('.agent/authored/f061-r1-1.md').read_text().splitlines()[1]` and
`[3]`) and never retyped. `git diff` for that commit shows exactly one changed
line in the file.

---

## What was built

**T001 — `packages/orchestration/dod_schema.py`**

`DoD` (schema `dod_v1`) and `DoDDraft` (schema `dod_draft_v1`) follow the F005
conventions: `extra="forbid"`, a `SCHEMA_V` class constant, and a required
`schema_v` Literal with no default. The two models are deliberately distinct —
the provider answers in `DoDDraft`, which has no `source` field, so a provider
cannot label a check's own provenance. `DoD` carries `compiled: bool` and
`origin: "provider"|"deterministic"`, cross-validated: `compiled` is True
exactly when `origin == "provider"`. A deterministic DoD presented as compiled
does not validate, so that honesty rule cannot be broken by a later refactor.

`validate_check_spec` refuses detectably unrunnable specs at compile time:
empty pytest selector, empty `tool`, empty or empty-element `argv`, a
`runtime_flow` with no steps or a step with no action, unknown spec keys, and
a `cwd` that is absolute or contains `..`. Unknown kinds are refused by the
`CheckKind` Literal.

**T001 — `packages/orchestration/dod_compiler.py`**

`compile_dod(intake, plan, call_fn)` merges the three ordered sources:
provider-proposed checks (`source="compiled"`, via `run_structured_call` — the
same schema-enforced, single-parse-retry discipline as intake and the flight
plan), then one generated check per acceptance line the compiled checks do not
already claim (`source="plan_acceptance"`), then the registered standard checks
(`source="standard"`). Generated checks group by resolved pytest selector, so
lines that resolve to the same selector share one check rather than spawning
duplicate identical processes — the rule asks for at least one check id per
line, not one process per line.

`TRACEABILITY_RULE` is the feature file's own sentence, and a test asserts it
still occurs in `docs/roadmap/features/T1_F061.md`, so the constant cannot
drift from the document that orders it. `trace_acceptance` reports the mapping
for any DoD; `assert_acceptance_traceable` raises `DoDTraceabilityError` naming
the uncovered lines. Both the positive case (all three fixtures) and the
violation case are tested.

`deterministic_dod` builds the no-provider DoD from the plan's acceptance
lines, labeled `compiled=False` / `origin="deterministic"`. Every route into
the fallback is tested: no `call_fn`, a `call_fn` that raises, a `call_fn`
returning prose, and a near-miss payload that omits `schema_v`.

`register_standard_check_provider(name, fn)` is the extension seam the
product-smoke feature plugs into — a named ordered mapping, with duplicate
registration an error rather than a silent overwrite.

**T002 — `packages/orchestration/dod_runners.py`**

`run_check` executes one check through the subprocess discipline already used
by `test_runner.run_tests_local`, reused rather than reinvented: argv list,
never `shell=True`, cwd inside the worktree, inherited environment, an
always-applied timeout, captured output truncated to a tail. `CheckEvidence`
records command, argv, cwd, exit code, duration and output tail.

A check is green only on exit 0. Every other outcome is red with a named
reason: `nonzero_exit`, `tool_unavailable` (the missing-linter case — proven
red, never a pass), `timeout`, `executable_not_allowed`,
`cwd_outside_worktree`, `cwd_missing`.

`runtime_flow` is absent from `RUNNER_REGISTRY` on purpose; `runner_for` raises
`UnsupportedCheckKindError`, and `run_checks` propagates it, so a DoD
containing one produces no partial evidence that could read as a completed
run. The runner lands in T003.

---

## Deviations & assumptions (A9)

1. **The DoD tag is not registered in `SCHEMA_REGISTRY`.** `dod_schema.py`
   imports the F005 base classes and follows every convention, but does not add
   `dod_v1` to `schemas/models.py`'s registry: that file is outside this
   round's declared change scope, and mutating the registry from an importing
   module would make its contents depend on import order. `DOD_SCHEMA_V` and
   `DoD` are exported so a later round can register the tag in one line. The
   registry currently has no production consumer — only tests assert it.

2. **The provider proposes checks, not a DoD.** The feature file's design
   sketch says `compile(intake, plan) -> DoD via provider call`. The provider
   is given the narrower `DoDDraft` contract instead, and the compiler builds
   the `DoD`. Rationale: `source` and `compiled` are honesty fields, and a
   provider that can set them can lie about them.

3. **Generated acceptance checks are grouped by selector.** N acceptance lines
   that resolve to the same pytest selector produce ONE check carrying N
   `acceptance_refs`, not N identical checks. The rule ("at least one check
   id") still holds for every line; this avoids running the same command
   repeatedly. Fixture `cli_tool` pins the behaviour.

4. **A compiled check that claims an acceptance line is taken at its word.**
   No `plan_acceptance` check is generated for a line a compiled check already
   names in `acceptance_refs`. Fixture `api_service` (fully covered) and
   fixture `docs_site` (partially covered) pin both sides.

5. **The deterministic fallback is coarse by design.** An acceptance line that
   names a test path becomes a check on that path; a prose line falls back to
   the `tests` selector (`DEFAULT_TEST_SELECTOR`, overridable per call). It is
   runnable and honest rather than clever — and it is labeled
   `compiled=false`, so it is never presented as reasoning it did not do.

6. **Executable allowlist for provider-named tools.** `lint`, `build` and
   `custom_cmd` name their own executable, which in this feature can originate
   from an LLM, so that executable must appear in an allowlist — by default the
   same closed `_EXECUTION_SAFE_EXECUTABLES` list `test_runner` already guards
   with. A refused executable is red with reason `executable_not_allowed` and
   nothing is run. `pytest` is exempt because its argv is a fixed template and
   only the selector comes from the check. Callers can pass a different set
   explicitly; the tests use that to exercise the `tool_unavailable` path
   deterministically.

7. **`custom_cmd` fencing is interpreted as execution location.** F017 fences
   govern which paths a change set may WRITE; they do not gate process
   execution. The runner therefore enforces the location: cwd is the resolved
   worktree, or a declared subdirectory of it, validated after symlink
   resolution immediately before exec. The schema refuses absolute and `..`
   paths at compile time; the runner re-checks. Both layers are tested.

8. **`run_checks` returns evidence and no verdict.** Deciding what a red
   blocking check MEANS for a job is the job-end gate — T004, its own round.
   Nothing in this round touches the job lifecycle or the terminal-green path.

9. **`PYTEST_PYTHON` resolves to `sys.executable`**, not the literal
   `python3`: inside a virtualenv the interpreter on PATH is not necessarily
   the one running Remedy.

10. **No mutation red-proofs were run**, so no disposable worktree was created
    or removed. The order permits mutation proofs only in a throwaway
    worktree; none were needed, because each red path is proven by a real
    failing process rather than by mutating the module.

---

## Open items for the next round

- T003: the `runtime_flow` runner on the runtime harness plus a fixture app
  flow. The schema kind, the fixture (`api_service`'s `api-smoke` check) and
  the loud registry failure are already in place and tested.
- T004: the job-end gate and the report matrix. `DoD.blocking_checks` exists
  and is tested; nothing consumes it yet.
- Registering `dod_v1` in `SCHEMA_REGISTRY` (deviation 1), if the reviewer
  wants it.
