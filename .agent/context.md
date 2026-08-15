# Context — F082 Self-benchmark

## Active Branch
feature/f082-self-benchmark, cut from main after PR #200 merged. F082 is
claimed `[~]` in docs/roadmap/STATUS.md and stays claimed until closure. No PR
exists for this branch yet; one is created at closure, not before.

## Scope
In: the capability bench built on the gauntlet harness. Built so far:
`capability_bench.py` with the pure record builder, `bench_orders.py` with the
version-bound freeze, THREE frozen orders under `scripts/bench_orders/` — three
and not five, because the shared sample project has no HTTP surface and no web
asset (R-0411), and the missing two wait on a bench-owned fixture per DECISION
F082 D3 rather than an edit to the gauntlet's template — `bench_dry_run.py`
with the join from an order file to a row over recorded evidence, and
`bench_history.py` with the append-only history, the trend and the regression
rules. T003a landed the `stats bench` read view at R10 — a new
`bench_cmd.py` under `apps/cli/commands/`, its catalog entry and its own test
file, adding exactly one handler key and changing no bench module. T003b's
WRITE half landed at R13 under DECISION F082 D7 and D8: a run's `run.json` now
carries a `models` key naming which model served which role, fed by a
`resolved_model` attribute on the callable
`intake.py::make_structured_call_fn` returns, with the builder recorded as a
permanent absence because `orchestrator_loop.py::execute_dispatched_job`
constructs `OllamaBuilder()` where no seam can observe it. T003b's READ half
landed at R15: `BenchRecord` carries a defaulted `models` field that
`build_bench_record` reads straight off the evidence body and that survives the
history file. No gauntlet module is touched and no additive ruling was needed —
`RunEvidence` is not on that path at all, and R-0426 registers the reviewer's
earlier claim that it was. R16 pinned F082's last unpinned acceptance criterion
— "the bench never runs implicitly" — as an enumerated allowlist of explicit
callers rather than as a total absence, under DECISION F082 D9, because the run
that completes the feature is itself the first legitimate caller. R17 landed the run itself as
`packages/orchestration/bench_run.py`, a NEW module joining the frozen order set
to a campaign, the campaign's evidence to bench rows, and the rows to a history
file — the entry point R11's Q6 found missing. It carries no fake and no clock:
the no-network deps are the test's, and `wall_s` stays clock-derived from the
runner. Its data root and history path are REQUIRED arguments, which closes Q6's
fourth blocker — history resolving through `data_paths.projects_dir` to the
operator's real root. It is the one name in the D9 allowlist. R18 registered
R-0434 and R-0435 and repaired four prose-and-typing defects, landing no
capability: R-0435 records that R17's doubles left `job_links` empty, so no
`dod_result.json` was ever written, every row the run produced was a FAILURE row,
and the suite was green over it. R19 owns that repair — a stored `GateResult`
through `dod_gate.py::save_gate_result` inside the isolated root, plus the
properties that assert what the rows SAY — and is the round that first measured
the Goal's three DONE conditions together. R20 recorded that PASS. The round map
is stated once, in the Steps section below, and is not restated here — a map
quoted in two places is the contradiction R-0447 records.
R2's inventory settled the shape: the factoring is ADDITIVE, so every bench
module is NEW and no symbol moves out of any gauntlet module — R3's
`capability_bench.py`, R4's `bench_orders.py`, R6's `bench_dry_run.py` and R7's
`bench_history.py`, each with its own test file under `tests/orchestration/`.
R3 additionally owns
`packages/orchestration/gauntlet_runner.py::measure_tokens`, repaired under
DECISION F082 D1 because the bench's cost field reads it (R-0407).
Plus `.agent/f082_inventory.md` and `.agent/**` round state and the one claimed
STATUS line.

Out: the gauntlet's pass definition, routing decisions — this feature only
RECORDS model context — and visual judgment, which is the F082 feature file's
Do-not-touch list. The gauntlet's own seven test files stay green UNMODIFIED;
a change that needs one of them edited is a finding, not a fix.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/. Destructive and red-proof checks run only inside a disposable
  git worktree under .remedy-wt/, so resource safety stays intact.
- Repository-wide `ruff check` is RED on main with pre-existing errors and is
  NOT a round gate (R-0364); ruff is gated scoped to the files F082 owns.
- The reviewer measures its block mechanically on the final bytes before
  emission and keeps it under 400 lines (DECISION F105 D5), with 240 the
  preferred target so the block-save commit stays inside the 500-insertion
  limit (R-0381).
- The bench never runs implicitly — on demand only, an F082 acceptance rule,
  pinned at R16 by `tests/orchestration/test_bench_never_runs_implicitly.py` as
  an allowlist of modules permitted to call the bench's write entry points
  (DECISION F082 D9). The allowlist holds EXACTLY ONE name, R17's
  `packages/orchestration/bench_run.py`. Adding to it is a deliberate act, not a
  repair.

## Steps
R1 claim F082, reset the record carrying the F077 open set forward, register
R-0403 ✅ → R2 the T001 gauntlet-harness inventory ✅ → R3 T001 the pure record
builder and the R-0407 token repair ✅ → R4 T001 the frozen order set and its
version freeze ✅ → R5 record the R4 verdict, register R-0409 to R-0411 and
DECISION F082 D3 ✅ → R6 record the R5 verdict, retire two superseded context
regions and close T001 with the dry run ✅ → R7 T002 the append-only history,
the trend and the regression rules ✅ → R8 complete the context sweep and pin
the regression threshold ✅ → R9 record the R8 verdict and retire the last
stale claim ✅ → R10 T003a the stats bench read view ✅ → R11 the T003b
inventory ✅ → R12 record the R11 verdict, register R-0419 and rule on the
gauntlet key at D7 ✅ → R13 T003b the write half, every run recording which model
served which role ✅ → R14 record the R13 verdict and register R-0420 to R-0422 ✅
→ R15 record the R14 verdict, register R-0423 to R-0426 and build T003b's read
half ✅ → R16 record the R15 verdict, register R-0427 and R-0428 and pin the Q7
criterion ✅ → R17 record the R16 verdict, register R-0429 and R-0430 and land
the fake-provider run ✅ → R18 register R-0434 and R-0435, rule at D10 and repair
R-0431 to R-0434 ✅ → R19 the acceptance proof for R-0435 ✅ → R20 record the R19
verdict, register R-0438 and R-0439 and rule at D11 ✅ → R21 the integration
gate ✅ → R22 record R21, register R-0443 to R-0445 and bring Built State
current ✅ → R23 closure, per DECISION F082 D12.
T003 split at DECISION F082 D5, its second half inventoried at D6, unblocked at
D7 and split in two at D8, R15 split the read half off from the run, and D9
splits the Q7 pin off from the run because a total-absence pin would not survive
the run's own driver; each round marks the PREVIOUS one done and never itself.
