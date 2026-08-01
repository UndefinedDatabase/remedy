# Handoff — F061 R3 (R-0165 + dod_v1 registration + integration gate)

Review of `ef60758b..HEAD` (branch `feature/f061-dod-compiler`), HEAD `c8905920`.

All ordered gates green. The integration gate ran on branch AND base: both
sides are fully green, so there are no branch-only failures to attribute and
no base-only failures to explain. No closure artifacts were produced — no
STATUS edit, no README edit, no evidence job, no zip.

---

## Commits

### 1 — `0665728e` chore(f061): persist R2 verdict + register R-0165

| path | +/- | reason |
| --- | --- | --- |
| `.agent/authored/f061-r3-1.md` | +73/-0 | authored live_review text |
| `.agent/authored/f061-r3-2.md` | +34/-0 | authored plan text |
| `.agent/authored/f061-r3-3.md` | +60/-0 | authored context text |
| `.agent/context.md` | +33/-34 | full replacement, byte copy of f061-r3-3 |
| `.agent/last_block.md` | +192/-212 | this round's block recorded verbatim |
| `.agent/live_review.md` | +59/-39 | full replacement, byte copy of f061-r3-1 |
| `.agent/plan.md` | +22/-22 | full replacement, byte copy of f061-r3-2 |

### 2 — `d5604c51` fix(f061): compile-time runtime_flow step validation (R-0165)

| path | +/- | reason |
| --- | --- | --- |
| `packages/orchestration/dod_schema.py` | +59/-6 | `_validate_flow_step`: action, path, closed key set, typed expectations |
| `tests/orchestration/test_dod_compiler.py` | +63/-1 | one negative test per rule, plus the index-naming and still-legal pins |
| `tests/orchestration/test_dod_runners.py` | +20/-3 | three runner tests now build a pre-rule stored DoD (see deviation 2) |

### 3 — `491448fb` chore(f061): mark R-0165 done in the finding ledger

| path | +/- | reason |
| --- | --- | --- |
| `.agent/live_review.md` | +1/-0 | the ordered `Done: R-0165 (commit d5604c51).` line, nothing else |

### 4 — `aebc3c11` feat(f061): register dod_v1 in SCHEMA_REGISTRY

| path | +/- | reason |
| --- | --- | --- |
| `packages/orchestration/structured_base.py` | +39/-0 | `_Strict`/`_Structured` moved here so the registration is not a cycle (see deviation 1) |
| `packages/orchestration/schemas/models.py` | +15/-20 | bases re-exported from the new leaf; `DOD_SCHEMA_V: DoD` added to the registry |
| `packages/orchestration/dod_schema.py` | +6/-5 | bases imported from the leaf; the stale R1 "not registered" note replaced |
| `tests/orchestration/schemas/test_schemas.py` | +17/-0 | registry entry + the deliberate `dod_draft_v1` absence |

### 5 — `c8905920` chore(f061): record the R3 integration-gate evidence

| path | +/- | reason |
| --- | --- | --- |
| `.agent/gate_f061_r3/README.md` | +61/-0 | the gate's own account: runs, comparison, parity, teardown |
| `.agent/gate_f061_r3/{branch,base}_failed.txt` | +0/-0 | both empty — the raw failure sets |
| `.agent/gate_f061_r3/{branch,base}_only.txt` | +0/-0 | both empty — the two `comm` outputs |
| `.agent/gate_f061_r3/{branch,base}_tail.txt` | +2/-0 each | the run tails and wall clock |

Every commit is under the 500-line limit.

---

## The `dod_draft_v1` decision (as ordered)

**Registered: `dod_v1` only. `dod_draft_v1` is deliberately NOT registered.**

Decided by reading `schemas/models.py` and its test:

* The registry's own docstring says it is "the single source of truth for which
  contract a tag means" — its job is resolving a tag a READER encounters. A
  `dod_v1` payload is persisted (`<job evidence>/dod.json`) and therefore has
  to be resolvable from its tag alone. A `dod_draft_v1` payload never leaves
  `dod_compiler.compile_dod`'s own provider call: it is validated, converted to
  `DoDCheck`s, and discarded. Nothing ever loads one back.
* No existing entry is a draft or intermediate shape. `ReviewVerdict`,
  `PlannerPlan`, `JobIntake` and `FlightPlan` are each the FINAL contract of
  their step, and `DesignSpec` is a prepared placeholder — so the registry's
  conventions do not include provider-facing draft schemas. The block's
  condition for registering it is therefore not met.
* The registry's compactness test caps tags at 6 characters with a documented
  exemption list (`flight_plan_v1`, itself persisted in job JSON). `dod_v1` is
  exactly 6 and needs no exemption; `dod_draft_v1` is 12 and would have forced
  a documented guard to be widened for a tag nobody resolves.

`test_the_provider_facing_dod_draft_is_not_registered` pins the absence with
that reasoning, so a later round changes it deliberately rather than by drift.

---

## Verification transcripts (raw)

### Phase 1 gate — state-file readers

```
$ python3 -m pytest tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py -q
........................................................................ [100%]
72 passed in 13.94s
EXIT=0
```

### Phase 3 gate

```
$ python3 -m pytest tests/orchestration/test_dod_compiler.py tests/orchestration/test_dod_runners.py tests/orchestration/test_dod_gate.py -q
........................................................................ [ 46%]
........................................................................ [ 93%]
..........                                                               [100%]
154 passed in 8.16s
EXIT=0

$ python3 -m pytest tests/orchestration/schemas -q
..............................................                           [100%]
46 passed in 0.12s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 15.06s
EXIT=0
```

### Phase 4 — integration gate (`docs/agents/integration_gate.md`)

Merge base: `git merge-base HEAD main` → `1869d89a`. Branch HEAD at run time:
`aebc3c11`.

**Step 1 — branch run**, from the repo root:

```
$ python3 -m pytest -n auto -q
........................................................................ [ 99%]
...............                                                          [100%]
14900 passed, 19 skipped in 140.76s (0:02:20)
EXIT=0
WALL=141.20 s

$ grep '^FAILED' branch_run.log | sort > branch_failed.txt
$ wc -l < branch_failed.txt
0
```

**Step 2 — base run**, identical command, throwaway worktree ON a throwaway
branch (a detached base worktree fails the self-dogfood branch guard by design,
DECISION D3):

```
$ git worktree add -b tmp/base-gate <path> 1869d89a
Preparing worktree (new branch 'tmp/base-gate')
HEAD is now at 1869d89a Merge pull request #171 from UndefinedDatabase/feature/f056-missions

$ cp -r apps/ui/node_modules <path>/apps/ui/node_modules
$ cp -r apps/ui/dist        <path>/apps/ui/dist

$ cd <path> && git rev-parse HEAD && git branch --show-current
1869d89a22718dce0f16c25289f927e8374571bb
tmp/base-gate

$ REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q
........................................................................ [ 99%]
...                                                                      [100%]
14744 passed, 19 skipped in 137.49s (0:02:17)
EXIT=0
WALL=137.94 s

$ grep '^FAILED' base_run.log | sort > base_failed.txt
$ wc -l < base_failed.txt
0
```

Parity was RESTORED before the base run (COPIED, never symlinked — the UI
auto-build runs npm install and writes through a symlink into the primary
checkout, F053 R3 evidence), which is the first of the two options the gate
doc's R-0155 amendment allows. That is why the base run has no UI
build-artifact failures to attribute.

**Step 3 — compare:**

```
$ comm -13 base_failed.txt branch_failed.txt      # branch-only failures
(no output)  — 0 lines

$ comm -23 base_failed.txt branch_failed.txt      # failures the branch fixed
(no output)  — 0 lines
```

**Step 4 — attribution:** nothing to attribute. `comm -13` is EMPTY, so the
branch introduces no failure and no per-id serial re-run is required. `comm
-23` is EMPTY, so there is no base failure needing an environment-class
attribution either — an unattributed `comm -23` id would have blocked the
verdict, and there are none.

Test-count delta 14900 − 14744 = **+156**, which is F061's own additions across
R1–R3 and nothing else.

**Teardown:**

```
$ git worktree remove --force <path>
$ git worktree prune
$ git branch -D tmp/base-gate
Deleted branch tmp/base-gate (was 1869d89a).

$ git worktree list
/home/decodeux/Repos/remedy  aebc3c11 [feature/f061-dod-compiler]

$ ls -d <path>
ls: cannot access '<path>': No such file or directory
```

**Step 5 — budget:** 140.76s branch, 137.49s base. Neither run crosses the
gate doc's ~5 min note threshold. The verdict itself is the reviewer's.

### Final state

```
$ git status --porcelain
(no output)
```

### Lint

```
$ python3 -m ruff check packages/orchestration/ tests/orchestration/schemas/
UP035 [*] Import from `collections.abc` instead: `Iterable`, `Mapping`, `Sequence`
  --> packages/orchestration/dag_schedule.py:36:1
Found 1 error.
```

PRE-EXISTING and untouched by this round — `git stash` + re-run reproduces the
same single error at base. `dag_schedule.py` is not in this round's scope, so
it was left alone rather than swept up in a feature commit. Every file this
round touched is ruff-clean.

---

## Authored-text proofs

```
$ sha256sum .agent/authored/f061-r3-1.md .agent/authored/f061-r3-2.md .agent/authored/f061-r3-3.md
afdddec6f97e2ceb59783c34fb17d2b3a65bd2a49ccf008af47a26cfdd1b4339  .agent/authored/f061-r3-1.md
0ff1ba92934894f37735f412fae47fc66e9e92746e71693db58dfd9b273b8a46  .agent/authored/f061-r3-2.md
4501430fe7acd484b3a260eda414ebe62b9fe5bcd0b84c8d9307739350f6f250  .agent/authored/f061-r3-3.md
```

All three match their BEGIN-marker hashes exactly. As in R1/R2 the payloads
arrived two-space indented from the transport; the unindented form hashes to
the marker value and the indented form does not, so the unindented text is the
authored text (R-0148 transport-wrap guard, resolved in favour of the hash).

```
$ cmp .agent/authored/f061-r3-2.md .agent/plan.md ; echo EXIT=$?
EXIT=0
$ cmp .agent/authored/f061-r3-3.md .agent/context.md ; echo EXIT=$?
EXIT=0
```

`live_review.md` differs from its authored file by EXACTLY the one ordered
line:

```
$ diff .agent/authored/f061-r3-1.md .agent/live_review.md
41a42
>   Done: R-0165 (commit d5604c51).
```

`docs/` untouched, as ordered:

```
$ git diff --stat ef60758b..HEAD -- docs/
(no output)
```

---

## What was built

**R-0165 — compile-time runtime_flow step validation.** `_validate_flow_step`
enforces the v1 vocabulary where the feature file says detectable nonsense
belongs — at compile time: the action must be `open`, `path` must be a
non-empty string starting with `/`, the step key set is closed to
`{action, path, expect_status, expect_text}`, `expect_status` must be an
integer status code (a bool is refused explicitly — `True` is an `int` in
Python but is not a status), and `expect_text` must be a string. Every message
names the step INDEX, because a flow can carry a dozen steps and "invalid step"
would send a reader through all of them.

The runner's own guard is untouched (`git status --porcelain
packages/orchestration/dod_runners.py` was empty across the fix commit): it
remains the defence for DoDs stored before this rule existed.

The fixtures and their goldens needed NO edit — `git status --porcelain
tests/orchestration/fixtures/` stayed empty throughout, as the block required.

**dod_v1 registration.** `SCHEMA_REGISTRY` now maps `dod_v1 -> DoD`, in
`schemas/models.py`, by that module importing `dod_schema` — not as an import
side effect from `dod_schema`. See deviation 1 for the cycle that had to be
broken to make that possible, which is the same cycle that caused R1 to defer
this item.

---

## Deviations & assumptions (A9)

1. **The registration required extracting the shared bases into a new leaf
   module, `packages/orchestration/structured_base.py`.** This is more than the
   "one line" the block anticipated, and it is why R1 deferred the item.

   The cycle is real and I proved it before working around it: `dod_schema`
   imported `_Strict`/`_Structured` from `schemas.models`, so `models`
   importing `DoD` closed a loop. Importing `dod_schema` first produced:

   ```
   ImportError: cannot import name 'DOD_SCHEMA_V' from partially initialized
   module 'packages.orchestration.dod_schema' (most likely due to a circular
   import)
   ```

   A `schemas/base.py` does NOT fix it — importing any module under that
   package runs `schemas/__init__.py`, which imports `models`, re-entering the
   same loop (I tried it, and it failed the same way). The base module has to
   sit OUTSIDE the package, which is why it landed at
   `packages/orchestration/structured_base.py`. `models` re-exports both names,
   so every existing `from ...schemas.models import _Strict` still works, and
   the dependency is now one-directional:
   `structured_base ← dod_schema ← models`.

   Verified from all four entry points (`dod_schema`, `schemas`,
   `schemas.models`, `dod_compiler` imported first): each resolves and
   `SCHEMA_REGISTRY['dod_v1'] is DoD`.

2. **Three tests in `test_dod_runners.py` were adjusted** — a file not named in
   this round's scope. R-0165 makes their inputs unconstructible: they built
   flow checks with an unknown action or a missing path through the validating
   `DoDCheck(...)` constructor, which now refuses them.

   The runner code is untouched. What changed is how those tests obtain their
   input: a new `legacy_flow()` helper builds the check via `model_construct`,
   with a docstring saying it represents a DoD STORED before R-0165 — which is
   exactly what the runner's surviving guard defends. The tests now prove the
   guard against the only input that can still reach it. The third test simply
   uses a valid step, since it only needed *a* runtime_flow check.

3. **One R2 parametrize case in `test_dod_compiler.py` was re-pointed.** The
   case `{"steps": [{"expect": "200"}]}` asserted the "non-empty 'action'"
   message; with a closed key set it is now caught one rule earlier, by the
   unknown-key check. The step is still refused — with a more specific message.
   The case now uses `{"path": "/x"}`, which has only legal keys and still
   proves the missing-action rule. No fixture or golden was involved, so the
   block's STOP condition (which is scoped to fixtures and goldens) did not
   fire.

4. **`expect_status` accepts an int-valued float** (`200.0`), because JSON
   round-trips can produce one; a non-integral float (`200.5`) and a bool are
   both refused. Pinned by tests either way.

5. **The pre-existing ruff error in `dag_schedule.py` was left alone.** It
   reproduces at base and the file is outside this round's scope; fixing it
   inside a feature commit would mix an unrelated cleanup into the diff.

6. **No mutation red-proofs were run**, so the only worktree created was the
   integration gate's, and it was removed, pruned, and its branch deleted —
   proven with `git worktree list`.

---

## Open items for the next round

- **Closure** per `docs/roadmap/STATUS_closure_protocol.md` — its own round:
  Built State in the feature file, preconditions, evidence job, fresh review
  zip, STATUS `[x]` + README sync as the last commit, PR. `docs/roadmap/` is
  still untouched and STATUS still reads `[~]`.
- Nothing compiles a DoD at job creation yet: the gate is wired and proven, but
  production wiring that CALLS `compile_dod` is downstream scope (F062
  registers standard checks into the seam; F069/F070 consume it). Worth naming
  explicitly in the Built State so the feature is not read as claiming more
  than it does.
