── STEP R6/10 — F082 Self-benchmark (record R5, then close T001 with the dry run) ──
Goal:        Record the R5 gate, register R-0412 and R-0413, retire the two
             superseded regions of `.agent/context.md`, then close T001 with a
             dry run that turns an order file plus RECORDED evidence into rows.
Bundle:      C0a/C0b save this block · C1 the R5 verdict and two findings,
             persisted FIRST · C2 the state repair · C3 the dry-run module and
             its tests · C4 handback.
Change:      .agent/live_review.md, .agent/context.md, .agent/plan.md,
             .agent/authored/f082-r6.md, .agent/last_block.md,
             .agent/handoff.md, packages/orchestration/bench_dry_run.py (NEW),
             tests/orchestration/test_bench_dry_run.py (NEW). NOTHING else.
             No gauntlet module, no gauntlet test file, no order file, no
             manifest, no existing bench module is edited.
Constraints: Findings persist FIRST (planner_reviewer_prompt.md §4 item 4).
             Never write a `Done:` or `Landed:` paragraph of your own. Every
             authored slice is applied disk-to-disk out of the COMMITTED block
             file, never retyped. Push after every commit. Never merge, never
             force-push, never work on main. Create NO pull request: F082 is
             mid-feature and its PR is created at closure, not before.
             ADDITIVE only (F082 inventory Q11): every gauntlet and bench symbol
             the new module needs is IMPORTED, none is moved or edited.
             `capability_bench.py` stays PURE — its docstring claims no disk
             read, no network, no clock, and that claim must remain true, which
             is why the dry run is a NEW module and not a function added there.
Done when:   the gates at the end of this block all pass, with their real
             values reported.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────────────

── C0 — save the block, in TWO commits ───────────────────────────────
The reviewer's scratchpad original is at `.remedy-wt/f082-r6-scratchpad.md`.
Saving it to both targets in ONE commit costs roughly twice its line count in
insertions and crowds the 500-insertion cap (findings R-0381, R-0399). Split it
unconditionally, and retype neither target:

C0a. Copy the scratchpad byte for byte to `.agent/authored/f082-r6.md`.
     Commit that file ALONE.
     Subject: `chore(f082): save the R6 block verbatim`
C0b. Copy the COMMITTED `.agent/authored/f082-r6.md` — not the scratchpad —
     byte for byte to `.agent/last_block.md`. Commit that file ALONE.
     Subject: `chore(f082): mirror the R6 block into last_block`

── C1 — the R5 verdict and two findings ──────────────────────────────
ONE commit, the FIRST after C0. `.agent/live_review.md`, APPEND ONLY, in this
order, separated by exactly one blank line, each exactly ONE physical line:
FINDING-R412, FINDING-R413, then GATE-R5. Nothing above the append may move —
prove it against the pre-C1 revision over the file's existing 115 lines.
  Subject: `docs(f082): record the R5 verdict and register R-0412 and R-0413`

── C2 — retire the two superseded regions of context.md ──────────────
ONE commit. Two REWRITE pairs in `.agent/context.md` and one full replacement
of `.agent/plan.md`. The two FROM slices are disjoint from each other and from
both TO slices.
  C2a. Pair CTXSTILL — deletes the stale second "Still to come" clause. The
       file already carries a current one nine lines above it, written by R5's
       CTXSCOPE2 pair; this one still says five order files are owed when three
       are built and the missing two wait on DECISION F082 D3.
  C2b. Pair CTXSTEPS — replaces the round map written at R1, which has never
       been updated and now disagrees with `.agent/plan.md` about which round
       does what. Do NOT touch the `## Steps` heading above it: the dashboard
       contract test asserts that substring.
  C2c. `.agent/plan.md`. FULL REPLACEMENT with the PLAN slice.
  Subject: `docs(f082): retire the superseded context regions and re-sync plan`

--- BEGIN SLICE FINDING-R412 ---
- R-0412 — Medium — `.agent/context.md` carries statements from superseded plans in TWO places, because every F082 block rewrote only the clause it was pointing at and none grepped the file for the same claim elsewhere — the R-0394 "retire the claim everywhere" class, now inside a single file rather than across two. The first instance the R5 worker found and correctly declared rather than silently repaired: the sentence "Still to come: the five frozen order files with per-order version tags, the append-only history under the data root's project area, and the `stats bench` CLI surface" sits nine lines below the R5 CTXSCOPE2 pair's statement that THREE orders are built and that the missing two wait on a bench-owned fixture per DECISION F082 D3, so the file asserts both that three orders exist and that five are owed. The second instance nobody has declared and no block has ordered: the `## Steps` section still holds the seven-round map authored at R1 in commit f7f1f57e — "R3 T001 factoring, the five orders and the record schema → R4 T002 history, trend and regression rules → R5 T003 CLI, model context and a fake-provider run → R6 the integration gate → R7 closure" — which is wrong about rounds that have already happened (R3 built the pure record builder and the R-0407 token repair, R4 built the frozen order set, R5 recorded and closed) and contradicts `.agent/plan.md`, which maps R6 to T001's dry run, R7 to T002, R8 to T003, R9 to the integration gate and R10 to closure. Two state files that the bootstrap reads therefore give a resuming session two different round maps. The precedent is that this section IS maintained: F077's own `## Steps` was extended round by round with a ✅ per closed round, out to R17, and F082's has stood untouched since the claim. This is the REVIEWER's defect and not the worker's — the R5 block's Goal was in as many words "re-sync the state mirrors", and it ordered exactly one rewrite pair in this file while leaving two contradictions standing. The counter-measure, binding from R6 on: before ordering a rewrite pair in any `.agent/**` state file, grep that WHOLE file for the claim being changed and retire every instance in the same pair set, and a block whose Goal names a state re-sync re-reads the target files end to end rather than only the region it means to touch. R6 retires both instances. OPEN.
--- END SLICE FINDING-R412 ---

--- BEGIN SLICE FINDING-R413 ---
- R-0413 — Low — the R5 block's own header contradicted the plan text the same block carried, which is the R-0331 clause-versus-clause class for the fourth time in this feature and the first time it recurred in the very block that registered the counter-measure against it. The header line reads "── STEP R5/9 — F082 Self-benchmark", putting the feature at nine rounds, while the PLAN slice inside that same block ends "4. R9 the integration gate, R10 closure", putting it at ten; the denominator has moved 7, 7, 7, 8, 9 across `.agent/authored/f082-r1.md` through `f082-r5.md` while the plan it summarises grew, and at R5 it was already one short of the block's own arithmetic. Nothing on disk is wrong and no verdict moves: the denominator is an estimate and every round's real sequence is carried by `.agent/plan.md`, which was correct. It is registered rather than corrected forward because R-0409, authored and applied in that same block, states the rule it breaks — "an authored state slice never states a count or an outcome that a stop clause, a survey or any other conditional step in the SAME block could falsify" — and a counter-measure that its own block violates on emission is worth one id to stop. The counter-measure, binding from R6 on: the step header's denominator is read from the CURRENT `.agent/plan.md` Next Steps at emission and matched against the block's own PLAN slice as part of pre-emission checklist item 10, or the header carries the round number alone with no denominator. R6's header is measured against its own PLAN slice and both say ten. OPEN.
--- END SLICE FINDING-R413 ---

--- BEGIN SLICE GATE-R5 ---
Gate: R5 — PASS, with two new findings, both the reviewer's. Verification tier: round gate plus the state-file contract readers plus the canary; no full-suite claim is made, and this round changed no production file so none is owed. Every one of the sixteen ordered gates was re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces. Transport: the scratchpad, `.agent/authored/f082-r5.md` and `.agent/last_block.md` are byte-identical at shared sha256 `024306e6caac75369ba1bd576f86f170de3c574fb83ec80fa203e80609e81985`, 221 lines, inside the 400-line cap — the gate was stated as a PROPERTY and the worker satisfied it with `sha256sum` plus a `python3` byte compare after `cmp` and `cp` were denied to it, which is the conduct R-0408's counter-measure exists to permit. The append was proven as `post == pre + add` rather than by grep alone: the reviewer re-extracted all four slices from the COMMITTED block file, joined them with the separator the block ordered, and the resulting region is byte-identical to the region C1 added, at sha256 `228a5c479efa27c449961e80cbc99e307c7f8ace0d53086010d89a9cd18092d9`, with the whole 107-line pre-C1 file an exact prefix of the 115-line result, the C1 numstat for that path `8 0` with deletion column 0, and FINDING-R409, FINDING-R410, FINDING-R411 and GATE-R4 each exactly ONE physical line occurring exactly once. The record's counts re-measured by the reviewer are `^Gate: R4 — PASS` 1, `^- R-0409 — ` 1, `^- R-0410 — ` 1, `^- R-0411 — ` 1, `^## Steps` 1, `^Landed: ` 0 and `^Done: ` 0, so the worker authored no resolution of its own; the open set recomputed mechanically is exactly FORTY-ONE with no duplicate, max id R-0411 and next free R-0412. `^## DECISION F082 D3` is 1 with deletion column 0 on that path and the file's tail equals the authored slice exactly; `.agent/plan.md` equals the PLAN slice as a whole file at 37 lines, under the 50-line cap; the CTXSCOPE2 rewrite measures FROM 0x and TO 1x with `.agent/context.md` at 54 lines. The change set is seven paths counted mechanically, every one inside the block's Change list and none outside it, the seventh being the handoff added by the commit that writes it (R-0149). The round-scoped `git diff --stat cae52438..HEAD -- packages/ apps/ tests/ scripts/ docs/` is EMPTY — base `cae52438` is the R4 handback commit, the SHA of the handback this round started from, per R-0368 — so the no-code promise held exactly. Suites re-run by the reviewer at the branch head: the canary `tests/cli/test_golden_path.py` `42 passed` and the three state-file contract readers `142 passed`, each exactly the baseline the block named; `python3 -m apps.cli.main integrity check --json` returns `passed: true`, `fail_count: 0` over 5 checks with `high_blockers_open` reporting no open blocker/high findings. `git status --porcelain` is empty and `git worktree list` is one line at HEAD; a marker scan finds zero BEGIN/END lines in all five non-block files, a trailing-whitespace scan finds none in any of the seven, and every file ends with a newline. Insertions per commit are 221, 164, 75 and 85, none over 500. Two deviations, both declared and both accepted: the handback is 115 lines against the 60-line cap carrying its DECISION D15 stated cause with no section dropped, and the commit messages carry no trailer, matching this repository's history. One observation costs no id: the worker's per-slice byte lengths are each one greater than the reviewer's because it measured each slice including its terminating newline where the reviewer measured without it — the property proven, that the applied region equals the authored bytes, is identical under either convention and holds on both sides, which is the same separator-convention difference already noted at R1 and is not spent as a finding. Both new findings are the REVIEWER's and neither charges the worker: R-0412 for two superseded regions left standing in `.agent/context.md` by a block whose Goal was to re-sync the state mirrors — the worker declared the one it was in a position to see and correctly refused to repair it outside its ordered slice, which is the R-0406 conduct this repository asks for — and R-0413 for the block header's round denominator contradicting the block's own PLAN slice. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R5 ---

--- BEGIN SLICE CTXSTILL-FROM ---
DECISION F082 D1 because the bench's cost field reads it (R-0407). Still to
come: the five frozen order files with per-order version tags, the append-only
history under the data root's project area, and the `stats bench` CLI surface.
--- END SLICE CTXSTILL-FROM ---

--- BEGIN SLICE CTXSTILL-TO ---
DECISION F082 D1 because the bench's cost field reads it (R-0407).
--- END SLICE CTXSTILL-TO ---

--- BEGIN SLICE CTXSTEPS-FROM ---
R1 claim F082, reset the record carrying the F077 open set forward, register
R-0403 ✅ → R2 the T001 gauntlet-harness inventory → R3 T001 factoring, the five
orders and the record schema → R4 T002 history, trend and regression rules → R5
T003 CLI, model context and a fake-provider run → R6 the integration gate → R7
closure.
--- END SLICE CTXSTEPS-FROM ---

--- BEGIN SLICE CTXSTEPS-TO ---
R1 claim F082, reset the record carrying the F077 open set forward, register
R-0403 ✅ → R2 the T001 gauntlet-harness inventory ✅ → R3 T001 the pure record
builder and the R-0407 token repair ✅ → R4 T001 the frozen order set and its
version freeze ✅ → R5 record the R4 verdict, register R-0409 to R-0411 and
DECISION F082 D3 ✅ → R6 record the R5 verdict, retire the superseded context
regions and close T001 with the dry run against recorded evidence → R7 T002
history, trend and regression rules → R8 T003 the stats bench CLI, model context
and a fake-provider run → R9 the integration gate → R10 closure.
--- END SLICE CTXSTEPS-TO ---

--- BEGIN SLICE PLAN ---
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0414. Open findings: forty-three — the thirty-two carried from F077, plus
R-0403 to R-0413 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R6 records the R5 gate, registers R-0412 and R-0413, retires the two superseded
regions of `.agent/context.md`, and closes T001 with `bench_dry_run.py` — the
join from a frozen order file to a bench row over RECORDED fixture evidence.

## Next Steps
1. R7 — T002: history append under the data root's project area, trend
   computation, the regression rules, and the improving, flat and degrading
   goldens.
2. R8 — T003: the `stats bench` CLI, model-context recording, and a
   fake-provider bench run end to end.
3. R9 the integration gate, R10 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
--- END SLICE PLAN ---

── C3 — the dry run: order file to row over recorded evidence ────────
ONE commit, both files together — the module and its tests are one logical
step and neither is meaningful alone.
  Subject: `feat(f082): add the bench dry run over recorded evidence`

Write `packages/orchestration/bench_dry_run.py`, NEW. It closes T001's last
item: "a dry-run against recorded fixture evidence". It executes nothing and
runs no order — it reads evidence that already exists and produces rows.

Design, and the reasons, which belong in the module docstring in your own words:
  * It is a NEW module rather than a function in `capability_bench.py` because
    that module's docstring promises "no disk read, no network, no clock" and
    the dry run reads directories. Keeping the promise true is worth a file.
  * ADDITIVE: import `run_dirs` and `RUN_FILENAME` from
    `packages.orchestration.gauntlet_evidence`, `evaluate_evidence_dir` from
    `packages.orchestration.gauntlet_evaluator`, `BenchRecord` and
    `build_bench_record` from `packages.orchestration.capability_bench`, and
    `load_bench_order_set` from `packages.orchestration.bench_orders`. Move
    nothing, edit none of them.
  * Pass is NOT re-decided here. Each row's `passed` comes from the verdict
    `evaluate_evidence_dir` already produced for that run directory —
    `gauntlet_evaluator.PASS_CRITERIA` is on F082's do-not-touch list.

Public surface, named per the AGENTS.md discoverability conventions:
  * `EVIDENCE_MISSING_CLASS = "evidence_missing"` — the postmortem class a row
    carries when the order has no recorded run. One spelling, defined once.
  * `dry_run_rows(*, order_ids, evidence_dir, series) -> tuple[BenchRecord, ...]`
    — one row per id in `order_ids`, IN THAT ORDER, never in directory order.
    Build the id→body map by reading each `run_dirs(evidence_dir)` entry's
    `RUN_FILENAME` as JSON and keying on the body's own `order_id`; index the
    verdicts from `evaluate_evidence_dir(evidence_dir).runs` by `run_dir`. An
    id with a body becomes `build_bench_record(evidence_body=…, series=…,
    verdict=…)`. An id with none becomes `BenchRecord(order_id=<id>,
    series=<series>, passed=False, cost=None, wall_s=None, repair_rounds=None,
    postmortem_classes=(EVIDENCE_MISSING_CLASS,))` — the feature file's A9 rule
    that a partial run is "recorded as failed rows with the class, series
    continues", so an absent order is a row and never an omission.
  * `dry_run_from_order_set(*, evidence_dir, series, orders_dir=None)` — loads
    the frozen set with `load_bench_order_set(orders_dir)` and calls
    `dry_run_rows` with `tuple(o.id for o in …)`. This is the "order file to
    row" path; the freeze runs first, so a tampered set refuses before any row
    exists.

Reading NEVER raises. Wrap each `run.json` read in `try/except (OSError,
ValueError)`; a directory whose body is unreadable or is not a JSON object
contributes no entry to the map, so its order takes the missing row. That
mirrors `gauntlet_evidence.load_run`'s own documented promise — a gauntlet that
threw on unreadable evidence would lose the run instead of failing it.

Deliberate absence, documented in the module where a reader would search for it
(AGENTS.md, Code Discoverability Conventions): a recorded run whose `order_id`
matches NO id in `order_ids` produces no row. Remedy deliberately does not
record foreign runs as bench rows, because a row asserts membership in this
series and a run from another order set is not a member of it.

Write `tests/orchestration/test_bench_dry_run.py`, NEW. Point it at the
existing recorded set — `Path(__file__).resolve().parent / "fixtures" /
"gauntlet" / "recorded"` — which is the same directory
`tests/orchestration/test_gauntlet_evidence.py` names as `RECORDED_DIR` and the
same one the evaluator's own dry-run proof runs against. Cover at least:
  1. Nine recorded runs, order_ids taken from the bodies themselves, produce
     nine rows in the order the ids were passed. Assert ONE spot value read off
     the real bytes rather than recomputed: the row for
     `fx-04-provider-api-error-mid-move` has `cost == {"in": 133900, "out":
     30400}` and `wall_s == 803.75`, which is what
     `recorded/run-04-injection-provider-api-error/run.json` records.
  2. Each row's `passed` equals the `flawless` the evaluator itself reports for
     that run directory — derive the expectation from
     `evaluate_evidence_dir(RECORDED_DIR)` inside the test, so the assertion
     proves the wiring rather than restating a table.
  3. The REAL frozen bench set against that same directory: every one of its
     ids is absent from the recorded evidence, so `dry_run_from_order_set`
     returns one failed row per order, in manifest order, each with
     `postmortem_classes == (EVIDENCE_MISSING_CLASS,)`, `passed is False` and
     `cost is None`. Do not hard-code the count three — read it from
     `load_bench_order_set()` — so the test survives the two orders DECISION
     F082 D3 still owes.
  4. A `tmp_path` directory holding one good run dir and one whose `run.json`
     is not valid JSON: the call returns rows and raises nothing, the good id
     gets its real values, the other id gets the missing row.
  5. Rows follow `order_ids`, not the directory sort: pass two recorded ids
     reversed and assert the returned ids come back reversed.

If any of this cannot be built as described — a symbol is not where this block
says, a signature differs, the evaluator refuses the directory — STOP, commit
what is green, and report the exact blocker in the handback. Do not invent a
different design and do not edit any gauntlet or bench file to make it fit.

── C4 — handback ─────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Name, as the
FIRST action of the next session, `docs/agents/self_drive_protocol.md` Phase 1
rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR Gate. State
that F082 is MID-FEATURE, that no PR exists for this branch and none is created
until closure, and that the next round is R7. Under 60 lines, or carry a
DECISION D15 stated-cause line naming the real count and the mandated content
that caused it. Commit and push.
  Subject: `chore(f082): handback R6`

── Gates — run every one, report the REAL value ──────────────────────
1.  `git status --porcelain` → EMPTY at handback. `git worktree list` → 1 line,
    as it reads AT HANDBACK.
2.  Transport, as a PROPERTY (R-0408): prove the scratchpad,
    `.agent/authored/f082-r6.md` and `.agent/last_block.md` are byte-identical
    and report the shared sha256 and the line count, which must be at or under
    400. Any means; report the digest.
3.  `.agent/STOP` — ABSENT or PRESENT, at round start AND at handback.
4.  Append proof: the first 115 lines of the new `.agent/live_review.md` equal
    the pre-C1 file. Report the C1 numstat for that path; DELETION column 0.
    Report the physical line count of FINDING-R412, FINDING-R413 and GATE-R5;
    each must be exactly 1.
5.  `grep -c "^Gate: R5 — PASS" .agent/live_review.md` → 1; `^- R-0412 — ` and
    `^- R-0413 — ` → 1 each; `^## Steps` → 1; `^Landed: ` → 0; `^Done: ` → 0.
6.  Open set recomputed mechanically — `^- R-[0-9]\+ — ` paragraphs minus
    `^Done: R-[0-9]\+ — ` lines. Expect FORTY-THREE; name every id; report
    duplicates as none or name them; report max and next free.
7.  Both context pairs: CTXSTILL-FROM 0x and CTXSTILL-TO 1x; CTXSTEPS-FROM 0x
    and CTXSTEPS-TO 1x. Note, so you do not read more into it than it carries:
    CTXSTILL-TO is a prefix of CTXSTILL-FROM's first line, so its count is 1
    BEFORE the edit as well and that count alone proves nothing (checklist item
    6). The discriminating gates for that pair are CTXSTILL-FROM 0x and
    `grep -c "the five frozen order files" .agent/context.md` → 0, which the
    planner measured as 1 before and 0 after. Run both and report both.
    Report `wc -l .agent/context.md`. Then re-read the file end to end and
    report whether any OTHER sentence in it still says five orders are owed or
    maps a round to work a different round did — if one does, report it, do not
    repair it outside these pairs.
8.  `wc -l .agent/plan.md` → under 50. Report it.
9.  The `.agent/context.md` contract readers, which is why gate 13 exists: it
    must still carry `## Active Branch` with a `feature/` slug, the substring
    `Steps`, a roadmap F-id and the word `pytest` or `resource`. Report each.
10. `git diff --name-only d0b2152d..HEAD` → report every path and COUNT them
    mechanically, stating the count. The Change list is a CEILING: every path
    reported appears in it. Name any path present that it does not contain —
    there must be none.
11. `git diff --name-only d0b2152d..HEAD -- tests/orchestration/` → exactly ONE
    path, `tests/orchestration/test_bench_dry_run.py`. The gauntlet's own test
    files stay byte-unmodified.
12. `python3 -m pytest tests/orchestration/test_bench_dry_run.py
    tests/orchestration/test_capability_bench.py
    tests/orchestration/test_bench_orders.py
    tests/orchestration/test_gauntlet_runner.py
    tests/orchestration/test_gauntlet_evaluator.py
    tests/orchestration/test_gauntlet_evidence.py
    tests/orchestration/test_gauntlet_matrix.py
    tests/orchestration/test_gauntlet_injection.py
    tests/orchestration/test_self_run_gauntlet.py
    tests/orchestration/test_verification_matrix.py -q` → exit 0. The planner
    measured those files WITHOUT the new one at `d0b2152d` today: 279 passed.
    Report the real total and the arithmetic — it must be 279 plus the number
    of tests you wrote, and no pre-existing test may be lost.
13. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Planner baselines at
    `d0b2152d` today: 42 for the canary and 142 for the three readers, so 184.
14. `python3 -m ruff check packages/orchestration/bench_dry_run.py
    tests/orchestration/test_bench_dry_run.py` → exit 0. Repository-wide ruff
    is RED on main and is NOT a gate (R-0364); this is scoped to the two files
    R6 owns. The planner ran the same command over the three existing F082
    files at `d0b2152d` today and it printed `All checks passed!`.
15. Red-proof, in a DISPOSABLE worktree under `.remedy-wt/` only (G5, §4 item
    10), never in the primary checkout: make `dry_run_rows` return rows in
    directory order instead of `order_ids` order, and report which test fails
    and its assertion. Order the PROPERTY, not a colour: if NO test fails, say
    so plainly — that is a real finding about test 5 and the planner wants it,
    not a green word. Remove and prune the worktree; `git worktree list` must
    read one line afterwards.
16. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `high_blockers_open` message.
17. `gh pr list --state open --json number,headRefName` → report it verbatim.
    It must be `[]`: no PR is created for this branch until closure.
18. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it in the handback with the reason.

Transport proof: state, for each of FINDING-R412, FINDING-R413, GATE-R5,
CTXSTILL-FROM, CTXSTILL-TO, CTXSTEPS-FROM, CTXSTEPS-TO and PLAN, that it was
extracted from the COMMITTED `.agent/authored/f082-r6.md` and applied
disk-to-disk, with its sha256 and byte length, and the proof that the applied
region equals it. State the shape of each pair — both context pairs are
REWRITES, their FROM and TO are disjoint. Confirm no BEGIN/END marker line
reached any target file. Scan every file you touched for trailing whitespace
and report the result.
