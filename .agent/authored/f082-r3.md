── STEP R3/7 — F082 Self-benchmark (record R2, then the T001 foundation) ──
Goal:        Record the R2 gate, register R-0405 to R-0407 and DECISION F082
             D1, repair the token-key mismatch the inventory found, and build
             the bench record schema as a pure function over what a gauntlet
             run already produces.
Bundle:      C0a/C0b save this block · C1 the R2 verdict, three findings, the
             decision and the plan re-sync, findings persisted FIRST · C2 the
             `measure_tokens` repair · C3 the bench record schema and its
             pure builder · C4 handback.
Change:      .agent/live_review.md, .agent/decisions.md, .agent/plan.md,
             .agent/context.md, packages/orchestration/gauntlet_runner.py,
             packages/orchestration/capability_bench.py (NEW),
             tests/orchestration/test_capability_bench.py (NEW),
             .agent/authored/f082-r3.md, .agent/last_block.md,
             .agent/handoff.md. NOTHING else. In particular
             `tests/orchestration/test_gauntlet_runner.py` and the other six
             gauntlet test files are NOT edited — gate 12 proves it.
Constraints: Findings persist FIRST, in their own commit, before any code
             (planner_reviewer_prompt.md §4 item 4). Never write a `Done:` or
             `Landed:` paragraph of your own. Every authored slice is applied
             disk-to-disk out of the COMMITTED block file, never retyped.
             Push after every commit. Never merge, never force-push, never
             work on main. The gauntlet's pass definition, its routing and
             visual judgment are untouchable (F082 Do-not-touch).
Done when:   the gates at the end of this block all pass, with their real
             values reported.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────────────

── C0 — save the block, in TWO commits ───────────────────────────────
The reviewer's scratchpad original is at `.remedy-wt/f082-r3-scratchpad.md`.
Saving it to both targets in ONE commit costs roughly twice its line count in
insertions and crowds the 500-insertion cap (AGENTS.md Commit Discipline;
findings R-0381 and R-0399). Split it unconditionally, and retype neither:

C0a. Copy the scratchpad byte for byte to `.agent/authored/f082-r3.md`.
     Commit that file ALONE.
     Subject: `chore(f082): save the R3 foundation block verbatim`
C0b. Copy the COMMITTED `.agent/authored/f082-r3.md` — not the scratchpad —
     byte for byte to `.agent/last_block.md`. Commit that file ALONE.
     Subject: `chore(f082): mirror the R3 block into last_block`

── C1 — the R2 verdict, three findings, DECISION D1, plan ────────────
ONE commit, and it is the FIRST commit after C0.
  Subject: `docs(f082): record the R2 verdict and register R-0405 to R-0407`

C1a. `.agent/live_review.md`. APPEND ONLY, in this order, each separated by
exactly one blank line and each exactly ONE physical line: FINDING-R405,
FINDING-R406, FINDING-R407, then GATE-R2. Nothing above the append may move —
prove it with `cmp` against the pre-C1 revision over the file's existing 95
lines. Extract with a script; if your editor wraps any of the four, the round
is wrong.

C1b. `.agent/decisions.md`. APPEND ONLY the DECISION-D1 slice at the end of
the file, preceded by exactly one blank line. Do not touch any existing entry.

C1c. `.agent/plan.md`. FULL REPLACEMENT with the PLAN slice.

C1d. `.agent/context.md`. REWRITE pair CTXSCOPE — FROM and TO are disjoint —
so the scope list names the two production files this feature now owns.

--- BEGIN SLICE FINDING-R405 ---
- R-0405 — Low — the R2 block's own gate 10 contradicts the same block's C1c, so the gate could not be satisfied as written and the worker was right to answer it with an explanation instead of a number. Gate 10 orders `git diff --name-only 35838c5e..HEAD` and says the result "must equal the block's Change list", a list of seven paths; C1c of the same block orders the worker to leave `.agent/context.md` untouched when two stated checks hold, which they did, so the real diff is six paths and equality is unreachable by construction. This is the reviewer's defect, not the worker's: it is the R-0331 clause-versus-clause class, where two clauses of one block are each defensible and jointly impossible, and it is the same failure the reviewer charged the worker for in R-0404 one round earlier — a numeral asserted beside an enumeration that the block's own rules change. Nothing on disk is wrong and no verdict moves: the property the gate exists to protect, that no path appears OUTSIDE the Change list, was checked and holds at six of seven. The counter-measure, binding from R3 on: a change-set gate states the Change list as a CEILING — every path in the diff appears in the list, and paths the block conditionally exempts may be absent — never as an equality, unless the block contains no conditional write. R3's gate 10 is worded that way. OPEN.
--- END SLICE FINDING-R405 ---

--- BEGIN SLICE FINDING-R406 ---
- R-0406 — Medium — `.agent/live_review.md` carries a "Next free id" claim in its header that the record below it contradicts, and a session that trusts the header will reuse an id that already exists. The header line reads "monotonic R-XXXX series across the reset. Next free id: R-0404." while the record now contains a registered `- R-0404 — ` paragraph, so the next free id is R-0405 and the header understates it by one. The cause is structural rather than careless: the header was authored at the R1 reset when R-0404 genuinely was free, the record is APPEND-ONLY by the convention every round applies, and no round since has been permitted to rewrite a line above the append — the R2 worker noticed the staleness and correctly declined to touch it, reporting it as an observation. That is the right conduct and the wrong outcome. The claim is also redundant: `docs/agents/planner_reviewer_prompt.md` §3 checklist item 10 already requires the open set and therefore the id ceiling to be recomputed MECHANICALLY from the record at every emission and never carried forward, so a stored next-free-id is a second source of truth for a value the rule says to derive. The fix is to stop storing it: the header sentence naming a next free id is removed at the next feature's reset, and until then every consumer derives the ceiling with `max` over `^- R-\d+ — `. R3 does not rewrite the header, because doing so would break the append-only property for a cosmetic gain mid-feature; it is fixed at F082's own closure or at the next reset, whichever comes first. OPEN.
--- END SLICE FINDING-R406 ---

--- BEGIN SLICE FINDING-R407 ---
- R-0407 — Medium — `packages/orchestration/gauntlet_runner.py::measure_tokens` reads two token keys that no writer in this repository produces, so every gauntlet run records a MEASURED ZERO for tokens instead of the truth, which is exactly what that function's own docstring forbids. It sums `usage.get("prompt_tokens")` and `usage.get("completion_tokens")`, while the only producer of the `cost.usage` body it reads is `packages/orchestration/orchestrator_loop.py::measure_call_cost`, which writes `input_tokens`, `output_tokens`, `cache_read`, `cache_creation` and `total_cost_usd`; the reviewer linked writer to reader end to end — `orchestrator_loop.py` calls `measure_call_cost(call)` and passes the result into `_record`, the ledger entry carries it as `cost`, and `gauntlet_runner.py` feeds those entries to `measure_tokens` to fill `run.json`. Because `usage` IS a dict on a measured run, the function sets `measured = True` and then sums nothing, returning `{"in": 0, "out": 0}` rather than `None` — so `run.json` gets a `tokens` key of zeros and never gets `tokens_source: unmeasured`. The docstring above those lines states the opposite invariant in as many words, "``None`` is not zero. A run whose provider reported no usage did not spend nothing", and cites R-0178, "the matrix must not understate cost"; the defect is that the invariant is enforced against the wrong key names. The suite never caught it because `tests/orchestration/test_gauntlet_runner.py` builds its own fixture usage body with `prompt_tokens`/`completion_tokens` — a shape production has never written — so the test pins the reader against itself rather than against a real writer, which is the R-0391 "count the writers" class seen from the test side. F082 owns this repair rather than deferring it: the bench's `cost` field reads this exact function, and a feature may not build its headline metric on a number known to be a false zero (DECISION F082 D1). The repair is additive and keeps every gauntlet test green unmodified. OPEN.
--- END SLICE FINDING-R407 ---

--- BEGIN SLICE GATE-R2 ---
Gate: R2 — PASS, with three new findings, two of which the round itself discovered and one of which is the reviewer's. Verification tier: round gate plus the state-file contract readers plus the canary; no full-suite claim is made, and this round changed no production file so none is owed. Every one of the sixteen ordered gates was re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces. Transport: `cmp` holds twice at shared sha256 `e3a5c888df9021c9559956f9269ac902c266241fd45bbadd9c0a48dde49b13bd`, 227 lines, inside the 400-line cap, and that digest equals the one the reviewer measured on its own bytes before emitting, so nothing mutated in delegation. The append is clean: the record's first 91 lines are byte-identical to the pre-C1 revision by `cmp`, the C1 numstat for that path is `4 0` with deletion column 0, and both appended slices are exactly ONE physical line each, which is the property the record's line-anchored greps depend on. The record's counts are `^Gate: R1 — PASS` 1, `^- R-0404 — ` 1, `^## Steps` 1 and `^Landed: ` 0, each re-measured by the reviewer, and the open set recomputed mechanically from the record is exactly THIRTY-FOUR with no duplicate and max id R-0404. Suites re-run by the reviewer at the branch head: the canary with the three state-file contract readers together `184 passed`, which is exactly the 42 and 142 baselines measured before authoring; `python3 -m apps.cli.main integrity check --json` returns `passed: true`, `fail_count: 0` over 5 checks. `wc -l .agent/plan.md` is 36, under the cap; `git status --porcelain` is empty and `git worktree list` is one line reading the branch at handback, which is the wording R2 corrected forward from R1. The round-scoped range `git diff --stat 35838c5e..HEAD -- packages/ apps/ tests/ docs/` is EMPTY — base `35838c5e` is the R1 handback commit, the SHA of the handback this round started from, per R-0368 — so the read-only promise held exactly. The inventory was audited against the source rather than accepted, and the answers that change the build plan hold. Q5 is correct and is the round's most valuable output: the reviewer confirmed writer-to-reader that `measure_call_cost` writes `input_tokens`/`output_tokens` into `cost.usage` while `measure_tokens` sums `prompt_tokens`/`completion_tokens`, that these are the only two writers and the single reader, and that the mismatch yields a measured zero rather than the documented `None` — registered above as R-0407 and repaired by this round under DECISION F082 D1. Q3 is correct in substance: `GauntletOrder` carries a per-file `sha256` and the module carries a set-level version constant, but no PER-ORDER version tag exists, so F082's acceptance rule that changing an order without bumping its version must fail validation is not met by anything on disk today and T001 owes it. Q11's conclusion that the factoring must be ADDITIVE is the conservative reading and is adopted: seven test files were listed and counted as seven, and R3 accordingly adds a new module rather than moving a symbol out of any gauntlet file. Q2's honest "no source" for `series` and `repair_rounds` is confirmed as the right answer rather than a gap in the inventory — `series` is a bench-level concept no run can know, and Q7 correctly traces `repair_rounds_used` to its drop at the `JobExecution` boundary. Two deviations, both declared and both accepted: the handback is 114 lines against the 60-line cap carrying its DECISION D15 stated cause with no section dropped, and the commit messages carry no trailer, matching this repository's history. The worker's third item, that the header's "Next free id" is stale and that append-only forbade fixing it, is exactly right in conduct and is registered as R-0406 so the contradiction is not merely observed. One finding is the REVIEWER's and is registered as R-0405: the block's gate 10 demanded an equality its own C1c made unreachable. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R2 ---

--- BEGIN SLICE DECISION-D1 ---
## DECISION F082 D1 (2026-08-14) — F082 repairs `measure_tokens` rather than recording around it

CONTEXT. The R2 inventory established, and the reviewer confirmed writer to
reader, that `gauntlet_runner.py::measure_tokens` sums `prompt_tokens` and
`completion_tokens` while the only producer of the `cost.usage` body it reads,
`orchestrator_loop.py::measure_call_cost`, writes `input_tokens` and
`output_tokens`. A measured run therefore yields `{"in": 0, "out": 0}` and
`run.json` never gets `tokens_source: unmeasured`. Registered as R-0407.
F082's per-order record carries a `cost` field, and that field reads this
function.

DECISION. F082 repairs the key reading inside T001, additively: the function
accepts BOTH spellings, preferring the production one, and continues to return
`None` when nothing was measured. AGENTS.md forbids mixing an unrelated fix
into a feature branch, and this one is not unrelated — it is the source of the
feature's headline metric, and a bench that reports a known-false zero as a
measured cost would be a fabricated live indicator, which is a block condition
in its own right.

ALTERNATIVES CONSIDERED. (a) Leave it and label the bench's cost basis
UNKNOWN: rejected, because the wrong number would still be written into
`run.json` for every gauntlet run, and F082 would be knowingly building on it.
(b) Route it to a paydown branch and block F082 until that lands: rejected as
disproportionate for a two-line additive repair whose blast radius is one
function, and it would leave the defect live meanwhile. (c) Change
`measure_call_cost` to write the older spelling instead: rejected, because that
writer feeds consumers beyond the gauntlet and the newer spelling is the one
the rest of the token machinery uses.

HOW TO REVERSE. Restore the two summing lines in `measure_tokens` to read only
`prompt_tokens`/`completion_tokens` and delete the regression test in
`tests/orchestration/test_capability_bench.py` that names `input_tokens`.
Nothing else depends on this decision.
--- END SLICE DECISION-D1 ---

--- BEGIN SLICE CTXSCOPE-FROM ---
In: the capability bench built on the gauntlet harness — a runner module under
`packages/orchestration/`, the five frozen order files, the per-run record
schema, the append-only history under the data root, and the `stats bench` CLI
surface; plus `.agent/f082_inventory.md`, the read-only T001 inventory,
`.agent/**` round state and the one claimed STATUS line. The exact file set is
NOT fixed until R2 has inventoried the harness: the feature file requires
inspecting the current shape before building, and its orchestrator brief names
the T001 factoring as the risky part.
--- END SLICE CTXSCOPE-FROM ---

--- BEGIN SLICE CTXSCOPE-TO ---
In: the capability bench built on the gauntlet harness. R2's inventory settled
the shape: the factoring is ADDITIVE, so the bench lands as a NEW
`packages/orchestration/capability_bench.py` with
`tests/orchestration/test_capability_bench.py`, and no symbol moves out of any
gauntlet module. R3 additionally owns
`packages/orchestration/gauntlet_runner.py::measure_tokens`, repaired under
DECISION F082 D1 because the bench's cost field reads it (R-0407). Still to
come: the five frozen order files with per-order version tags, the append-only
history under the data root's project area, and the `stats bench` CLI surface.
Plus `.agent/f082_inventory.md` and `.agent/**` round state and the one claimed
STATUS line.
--- END SLICE CTXSCOPE-TO ---

--- BEGIN SLICE PLAN ---
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0408. Open findings: thirty-seven — the thirty-two carried from F077,
R-0403 at the claim, R-0404 at the R1 gate, and R-0405 to R-0407 at the R2
gate. `.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R3: the R2 gate recorded, R-0405 to R-0407 and DECISION F082 D1 registered,
`measure_tokens` repaired, and the bench record schema built as a pure
function over what a gauntlet run already produces.

## Next Steps
1. R4 — T001 finished: the five frozen order files with per-order version
   tags, the validation that a changed order without a bump FAILS, and the
   dry run against recorded fixture evidence.
2. R5 — T002: history append, trend computation, the regression rules and the
   improving, flat and degrading goldens.
3. R6 — T003: the `stats bench` CLI, model-context recording and a
   fake-provider bench run end to end.
4. R7 the integration gate, R8 closure.

## Risks
- `series` and `repair_rounds` have no source in the harness (R2 Q2, Q7).
  Both are recorded as explicitly-unmeasured rather than invented; a zero
  standing in for an unknown is the R-0178 mistake R-0407 just registered.
- Thirty-seven open findings is the largest carry any feature has started with.
--- END SLICE PLAN ---

── C2 — repair `measure_tokens` (DECISION F082 D1) ───────────────────
File: `packages/orchestration/gauntlet_runner.py`, function `measure_tokens`
ONLY. Commit alone.
  Subject: `fix(f082): count the token keys the loop actually writes`

Change the two summing lines so each accepts BOTH spellings, preferring the
production one: input is `input_tokens` when present, else `prompt_tokens`;
output is `output_tokens` when present, else `completion_tokens`. A key that is
present but `None` counts as absent, matching the existing `or 0` handling.
Everything else stays exactly as it is: `measured` is still set by the presence
of a `usage` dict, the function still returns `None` when nothing was measured,
and the docstring's invariant is unchanged because this restores it rather than
altering it. Add one line to the docstring naming both spellings and citing
R-0407 — the one-line WHY sits directly above what it explains (AGENTS.md Code
Discoverability). Touch no other function in the file.

── C3 — the bench record schema ──────────────────────────────────────
Files: `packages/orchestration/capability_bench.py` (NEW) and
`tests/orchestration/test_capability_bench.py` (NEW). Commit together.
  Subject: `feat(f082): add the capability bench record schema`

Build the record as a PURE function over data a gauntlet run already produced —
no disk read, no network, no clock — so it is testable from a fixture body:

- A frozen dataclass `BenchRecord` with exactly the fields the feature file
  names: `order_id`, `series`, `passed`, `cost`, `wall_s`, `repair_rounds`,
  `postmortem_classes`. Use `passed` rather than `pass`, which is a Python
  keyword; note that renaming in a one-line comment so the next reader does not
  think the schema drifted.
- `build_bench_record(*, evidence_body, series, verdict)` returning one
  `BenchRecord`, reading ONLY what R2's inventory proved exists: `order_id` and
  `wall_seconds` off the evidence body, `tokens` for cost, and the postmortem
  `failure_class` values for `postmortem_classes`.
- Unmeasured is `None`, never zero — the R-0178 invariant this feature just
  had to repair. `cost` is `None` when the body carries no `tokens` key;
  `repair_rounds` is `None` always for now, because R2 Q7 proved the counter is
  dropped at the `JobExecution` boundary and no source exists. Say that in a
  comment naming Q7, so the next reader does not read `None` as an oversight.
- `series` is supplied by the CALLER: R2 Q2 proved no run can know it.
- A `to_json()` returning a plain dict with sorted keys, for the append-only
  history R5 will write.

Tests in the new file, each pinning one behaviour: a fully-populated body
produces every field; a body with no `tokens` key gives `cost is None`; a body
whose postmortems carry two distinct `failure_class` values yields both, in a
deterministic order; `repair_rounds is None`; `to_json()` round-trips. Plus the
R-0407 regression test: `measure_tokens` over one entry whose `cost.usage`
carries `input_tokens`/`output_tokens` returns those numbers rather than zeros,
and over an entry carrying the older spelling still returns those — one test
per spelling, both named for R-0407.

── C4 — handback ─────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Under 60
lines, or carry a DECISION D15 stated-cause line naming the real count and the
mandated content that caused it. Commit and push.
  Subject: `chore(f082): handback R3`

── Gates — run every one, report the REAL value ──────────────────────
1.  `git status --porcelain` → EMPTY at handback. `git worktree list` → 1 line,
    as it reads AT HANDBACK.
2.  `cmp` scratchpad↔`.agent/authored/f082-r3.md` and that↔
    `.agent/last_block.md` → both exit 0. Report shared sha256 and line count;
    at or under 400.
3.  `.agent/STOP` — ABSENT or PRESENT, at round start AND at handback.
4.  Append proof: `cmp` the pre-C1 `.agent/live_review.md` against the first 95
    lines of the new one → exit 0. Report the C1 numstat for that path; its
    DELETION column must be 0. Report the physical line count of each of the
    four appended slices; each must be exactly 1.
5.  `grep -c "^Gate: R2 — PASS" .agent/live_review.md` → 1. Same for
    `^- R-0405 — `, `^- R-0406 — `, `^- R-0407 — ` → 1 each.
    `grep -c "^## Steps" .agent/live_review.md` → 1.
    `grep -c "^Landed: " .agent/live_review.md` → 0.
6.  Open set recomputed mechanically — every `^- R-[0-9]\+ — ` paragraph minus
    every `^Done: R-[0-9]\+ — ` line. Expect THIRTY-SEVEN; name every id;
    report duplicates as none or name them; report max and next free.
7.  `grep -c "^## DECISION F082 D1" .agent/decisions.md` → 1. Report the C1
    numstat for that path; its DELETION column must be 0.
8.  `wc -l .agent/plan.md` → under 50. Report it.
9.  CTXSCOPE pair: FROM 0x and TO 1x in `.agent/context.md` after the edit.
    Report `wc -l .agent/context.md`.
10. `git diff --name-only 13953c5f..HEAD` → report every path and COUNT them
    mechanically, stating the count you counted. The Change list is a CEILING:
    every path reported must appear in it, and a path the block exempts may be
    absent. Name any path present that the list does not contain — there must
    be none (finding R-0405).
11. R-0407 red-proof, in a DISPOSABLE worktree under `.remedy-wt/` and never in
    the primary checkout: at HEAD, revert `measure_tokens`' two summing lines
    to read only the old spellings, run the two R-0407 regression tests, and
    report which FAIL. The `input_tokens` test must go RED; if it stays green
    the test does not pin the repair and that is a finding, not a pass. From
    inside that worktree, first run `python3 -c "import
    packages.orchestration.gauntlet_runner as g; print(g.__file__)"` and report
    the path — it must be under `.remedy-wt/`, proving the mutated copy is the
    one imported (R-0337). Remove and prune the worktree; `git worktree list`
    is one line again at handback.
12. The gauntlet's own tests, UNMODIFIED and green:
    `git diff --name-only 13953c5f..HEAD -- tests/orchestration/` must NOT
    contain any `test_gauntlet_*.py` or `test_self_run_gauntlet.py` — report
    the real list. Then run all seven:
    `python3 -m pytest tests/orchestration/test_gauntlet_orders.py
    tests/orchestration/test_gauntlet_runner.py
    tests/orchestration/test_gauntlet_evaluator.py
    tests/orchestration/test_gauntlet_matrix.py
    tests/orchestration/test_gauntlet_evidence.py
    tests/orchestration/test_gauntlet_injection.py
    tests/orchestration/test_self_run_gauntlet.py -q` → exit 0. The planner
    measured 276 passed at 13953c5f today; report the real number.
13. `python3 -m pytest tests/orchestration/test_capability_bench.py -q` →
    exit 0. Report the count; there is no baseline, the file is new.
14. `python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q` →
    exit 0. The planner measured 196 passed at 13953c5f today; report the real
    number. This is the writer side of R-0407 and must not move.
15. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0.
    Planner baseline at 13953c5f today: 42 passed.
16. `python3 -m pytest tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Planner baseline at
    that commit today: 142 passed.
17. `python3 -m ruff check packages/orchestration/capability_bench.py
    packages/orchestration/gauntlet_runner.py
    tests/orchestration/test_capability_bench.py` → exit 0. Repository-wide
    ruff is RED on main and is NOT a gate (R-0364); this is scoped to the three
    files R3 owns.
18. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `high_blockers_open` message.
19. Purity of the new module: `grep -n "open(\|Path(\|requests\|time\.\|datetime"
    packages/orchestration/capability_bench.py` → report every hit. A pure
    record builder should have none; if a hit is legitimate, name why.
20. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it in the handback with the reason.

Transport proof: state, for each of FINDING-R405, FINDING-R406, FINDING-R407,
GATE-R2, DECISION-D1, PLAN, CTXSCOPE-FROM and CTXSCOPE-TO, that it was
extracted from the COMMITTED `.agent/authored/f082-r3.md` and applied
disk-to-disk, with its sha256 and byte length, and the proof that the applied
region equals it. Confirm no BEGIN/END marker line reached any target file.
Scan every file you touched for trailing whitespace and report the result.
