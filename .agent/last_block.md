── STEP R11/14 — F082 Self-benchmark ─────────────────────────────────────────
Goal:        Record the R10 verdict, register the reviewer-block defect R-0418,
             retire the sentence R10's own change made half-stale, and ANSWER
             the T003b inventory in writing — what "model/routing context is
             recorded per run" can actually mean against this harness — so the
             build round after it orders a change set over known ground.
Bundle:      C0a save this block · C0b mirror it · C1 GATE-R10 + FINDING-R418 +
             DECISION-D6 appended to the review record · C2 the CTXSCOPE pair
             · C3 the inventory answers · C4 plan and step-map re-sync
             · C5 handback.
Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r11.md   (C0a, new)
             - .agent/last_block.md          (C0b)
             - .agent/live_review.md         (C1 append)
             - .agent/context.md             (C2 CTXSCOPE pair, C4 CTXSTEPS pair)
             - docs/roadmap/features/T2_F082.md  (C3, Built State section ONLY)
             - .agent/plan.md                (C4)
             - .agent/handoff.md             (C5)
             NOT in scope: `apps/**`, `packages/**`, `tests/**`. This round
             writes NO code and NO test. `git diff --name-only <BASE>..HEAD --
             apps/ packages/ tests/` must be EMPTY. It is an inventory round:
             it buys the next round's precision and nothing else.

Constraints:
 1. THIS ROUND CHANGES NO BEHAVIOUR. Every answer below is a READ plus a
    citation. If answering one seems to require an edit, the answer is "it
    requires an edit, here is which one" — write that down instead of making
    it.
 2. EVERY ANSWER CARRIES A FILE-AND-SYMBOL CITATION, in the form
    `path.py::symbol`, naming what you actually read. NEVER a bare line
    number: this branch's own rounds move lines, and a number that has drifted
    reads as a fabricated citation (R-0353). An answer with no citation is
    worth less than no answer, because it looks like evidence.
 3. AN HONEST "NO" IS THE MOST VALUABLE ANSWER HERE. If the harness carries no
    role→model binding at all, say exactly that and cite where you looked. Do
    not describe what a reasonable harness would do. R2's inventory settled
    T001 by answering Q5 and Q7 with absences (`total_cost_usd` never reaches
    `run.json`; `repair_rounds_used` is dropped at the `JobExecution`
    boundary), and both absences are why T001's schema is honest today.
 4. The answers land in the Built State section of
    `docs/roadmap/features/T2_F082.md` — the feature file's own record of what
    IS. Do not touch its Goal & Done, Design, Task slicing, Acceptance, Edge
    cases, Orchestrator brief or Do-not-touch sections, and do not touch
    `docs/roadmap/ROADMAP.md` at all (AGENTS.md, Documentation Structure:
    agents must not edit ROADMAP.md unless the operator asks).
 5. Because the change set includes `docs/roadmap/**`, the docs-round gate
    binds: `python3 -m pytest tests/docs/ -q` runs in addition to the canary
    (planner_reviewer_prompt.md §3, verification tier 5).
 6. `.agent/plan.md` stays under 50 lines and keeps `## Goal` and
    `## Next Steps`. `.agent/context.md` keeps `## Active Branch` with its
    `feature/` slug, the substring `Steps`, a roadmap F-id, and `pytest` or
    `resource`.
 7. Apply every slice DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r11.md`, never by retyping and never from the
    prompt after C0a. No `--- BEGIN SLICE` / `--- END SLICE` marker line may
    reach any target file. No target file gains a trailing-whitespace line.
 8. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    Insertions per commit stay under 500. No commit trailer.

────────────────── THE INVENTORY — answer all seven ──────────────────
Answer each in two to five sentences, in the Built State section, each with its
citation. These are the questions whose answers decide T003b's SHAPE; the build
round cannot be authored precisely until they are on disk.

Q1. Does anything in the harness carry a role→model binding for MORE THAN ONE
    role at run time? `gauntlet_runner.py` reads `orchestrator.model` from
    config for the orchestrator move; is there a second role anywhere with its
    own model, or is one role the whole truth today? Name every role you find
    and the symbol that binds each to a model.
Q2. Does a gauntlet `run.json` record any model identity at all? Read what
    WRITES that file, not only what reads it, and say which keys exist. If no
    model name reaches it, say so — that is the T003b-shaping answer.
Q3. Where does the token ledger record its model, and is that record reachable
    from a bench run's evidence directory? `token_ledger` groups by `model`
    among its `COST_GROUP_KEYS`; state whether a bench row could join to it and
    what the join key would be.
Q4. What is the smallest honest shape for "model context per run"? Given Q1-Q3,
    say whether it is (a) a field on the existing `BenchRecord`, (b) a
    run-level header row in the history file beside the per-order rows, or
    (c) not recordable today without a change to a gauntlet module — which
    F082's Do-not-touch and the ADDITIVE constraint would forbid. Recommend
    ONE and give the reason. A recommendation is required; "it depends" is not
    an answer.
Q5. Is there a fake/recorded provider this repo already runs end to end?
    `pingpong_provider.py` and `evidence_mode.py` both exist; state what each
    one actually provides, whether either can drive a gauntlet run without a
    network, and which one a bench end-to-end run would use.
Q6. What would a "fake-provider bench run end to end" actually EXECUTE? Name
    the entry point a bench run would call and say whether it is reachable
    without a network, without a clock dependency and without writing outside
    a temp data root. If it is not reachable, name the blocker.
Q7. What does the ACCEPTANCE criterion still owe? The feature file requires
    "changing an order file without bumping its version fails validation" and
    "the bench never runs implicitly". State, with citations, whether each is
    already pinned by a test today, and name the test if so. An unpinned
    acceptance criterion at closure is a closure blocker, so this answer is
    the one that protects R13.

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE GATE-R10 --- (append to .agent/live_review.md, C1, ONE physical line)
Gate: R10 — PASS, with one new finding, the reviewer's. Verification tier: round gate plus the catalog and grouped-CLI contract guards plus the canary; no full-suite claim is made and none is owed. All twenty ordered gates were re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces at its reported value. Transport is proven at PRIMARY strength this time — the scratchpad `.remedy-wt/f082-r10-scratchpad.md` survived into the reviewing session, so the proof is scratchpad against `.agent/authored/f082-r10.md` against `.agent/last_block.md`, all three byte-identical at shared sha256 `415841817bbb53313cdf57b2abb766c0d46416d7fb75057ddb7b5c39ea385431`, 27229 bytes and 377 lines, inside the 400-line cap. The C1 append was proven as a PROPERTY: `post == pre + add` holds byte-wise over the committed `b1b93185^`→`b1b93185` where `add` is GATE-R9 and DECISION-D5 joined as committed, the 138-line pre-file is an exact prefix of the 169-line result, and the numstat is `31 0` with the deletion column zero. All five FROM→TO pairs were re-proven as properties over their own committed revisions, each in the shape the block DECLARED for it: LRSTEPS, CTXSTEPS, INIT1 and INIT2 are rewrites and each FROM went 1x to 0x with its TO landing 1x, while CATALOG is append-shaped, its TO genuinely contains its FROM, and its FROM correctly stayed 1x — demanding 0x there would have been unmeetable by construction, which is why the block declared the shape at authoring time. `.agent/plan.md` byte-equals the PLAN slice as a whole file at 41 lines, `.agent/context.md` keeps every contract reader at 61 lines, and `stats.bench` went 0x to 1x in the catalog. The record counts are `^Gate: R9 — PASS` 1, `^## DECISION F082 D5` 1, `^Landed: ` 0 and `^Done: ` 0, so the worker authored no resolution of its own; the open set recomputed mechanically is exactly FORTY-SEVEN with no duplicate, max R-0417 and next free R-0418. The change set is ten paths, every one inside the block's Change list, and `git diff --name-only d08250ed..HEAD -- packages/` is EMPTY, so the promise that this round adds a READER and changes no bench module holds exactly. Suites re-run by the reviewer at the branch head: the new `tests/cli/test_stats_bench.py` `25 passed`; the eleven-file orchestration suite `294 passed`, unchanged because R10 adds no test there; the canary plus the three contract readers `184 passed`; the catalog and grouped-CLI guard bundle `634 passed` with all five guard files UNMODIFIED, which is the gate that would have caught a catalog entry bought by editing its own guard; scoped ruff over all four paths `All checks passed!`; `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with `handlers=337`, exactly the 336 measured at d08250ed plus the one ordered key and not a second. Insertions per commit are 377, 328, 31, 8, 425, 372, 16 and 146, none over 500, and `gh pr list --state open` is `[]`. The load-bearing gate is 18 and the reviewer ran the red-proof ITSELF in a disposable worktree rather than accepting the handback: replacing the body of `_render_bench_human`'s `elif warnings:` branch with a raise fails 6 of 25 tests including `test_the_warnings_are_exactly_what_bench_regressions_produced`, the import path was proven to resolve inside the worktree copy rather than the primary checkout (R-0337), and the worktree was removed and pruned leaving the primary checkout clean. Beyond the ordered gates the reviewer ran the command FOR REAL against a registered project and a history written by the real writer, because a green suite is not a working feature (R-0220): three runs of one series, the third degraded, print all three warning kinds naming the order `bench-01-cold-start` and both numbers — 9000.0 against a trailing median of 1000.0, 400.0 against 40.0, and a pass drop from 1.0 — while the unmeasured order prints the word `unmeasured` in every column and never a zero, no repair-round column exists and its absence is explained in one sentence, and raising the multiplier to 50 silences both threshold warnings while correctly keeping the pass drop, which is not a threshold comparison. That is F082's acceptance criterion "degrading run warns with order and numbers" demonstrated live rather than asserted. The worker-authored tests are non-vacuous where it matters: `test_the_warnings_are_exactly_what_bench_regressions_produced` asserts the corpus produces all three kinds BEFORE comparing the rendering, so a fixture that flattened would fail loudly instead of going blind, and the history fixture asserts its own path sits under `tmp_path` so a broken data-root monkeypatch cannot write the real data root. Five deviations, all declared and all accepted: the handoff at 200 lines under the DECISION D15 stated-cause allowance with no section dropped, the denied-command routes per R-0408, no commit trailer, plan currency at C5 per the block's own bundle order, and the missing Fortschritt line, which is the new finding and charges the reviewer rather than the worker. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R10 ---

--- BEGIN SLICE FINDING-R418 --- (append to .agent/live_review.md, C1, after GATE-R10, blank line between)
- R-0418 — Low, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer. The R10 block's Handback paragraph ordered the handoff to "repeat the Fortschritt line verbatim", but no Fortschritt line exists anywhere in the R10 block: its only occurrence of the word is that instruction itself. This is the R-0371 class — ordering a value that cannot exist at the moment the text is written — and it arises specifically from self-drive. Under the split workflow the Fortschritt line lives in the operator brief that the paste relay carries alongside the block, so a worker reading the relay sees it; under docs/agents/self_drive_protocol.md there IS no relay, the worker is a delegated subagent that never sees the reviewer's brief, and any instruction to repeat something from that brief is unsatisfiable by construction. The worker did the right thing: it declared the deviation and invented nothing, which is exactly the behaviour planner_reviewer_prompt.md §3 item 8 predicts of an honest worker facing an unmeetable gate. The fix binds the REVIEWER, not the worker: in self-drive every block that requires the handoff to carry the Fortschritt line must CONTAIN that line as authored text, or must not order it. R11 carries it as an authored slice, which is the standing form from here.
--- END SLICE FINDING-R418 ---

--- BEGIN SLICE DECISION-D6 --- (append to .agent/live_review.md, C1, after FINDING-R418, blank line between)
## DECISION F082 D6 — T003b is inventoried before it is built

Chosen: R11 answers the T003b inventory in writing and changes no code. The
build round becomes R12, the integration gate R13 and closure R14.

Why: "Model/routing context is recorded per run (which models served which
roles)" cannot be turned into a change set today, because nobody has
established that this harness HAS more than one role→model binding. The
reviewer grepped the bench modules and found no `model_context` symbol of any
kind, and found exactly one role bound to a model — `orchestrator.model`, read
from config in `gauntlet_runner.py`. Whether T003b is a one-field addition or a
cross-cutting change to a module F082's Do-not-touch list protects turns
entirely on that answer. Ordering the build blind is how a block acquires a
gate the code contradicts, and six of the last eight findings on this branch
are already reviewer-block defects of exactly that family.

This is the SECOND re-plan in two rounds (D5 split T003; D6 now inserts an
inventory before its second half), and that is worth naming rather than
hiding: the pattern says T003 was under-specified in the feature file, not
that the rounds are drifting. R2 set the precedent on this same branch by
inventorying T001 before building it, and T001's schema is honest today
BECAUSE that inventory answered two of its questions with absences.

Alternatives considered: (a) build T003b now against the reviewer's guess at
the shape — rejected, that is the defect class above, and the guess would be
load-bearing on the honesty of a recorded field; (b) drop model-context
recording from F082 and close on T003a — rejected, it is an explicit Design
bullet and later routing features are named as its consumers, so dropping it
silently would move work into a feature that has not been claimed.

How to reverse: delete this decision, restore the R11 line of the step map in
`.agent/context.md`, and order T003b whole. The inventory answers stay useful
either way — they land in the feature file's Built State, which is where the
closure round reads from.
--- END SLICE DECISION-D6 ---

--- BEGIN SLICE CTXSCOPE-FROM --- (in .agent/context.md, C2 — REWRITE pair)
rules. Still to come, both T003: the `stats bench` CLI surface and the
model-context recording.
--- END SLICE CTXSCOPE-FROM ---

--- BEGIN SLICE CTXSCOPE-TO --- (C2)
rules. T003a landed the `stats bench` read view at R10 — a new
`bench_cmd.py` under `apps/cli/commands/`, its catalog entry and its own test
file, adding exactly one handler key and changing no bench module. Still to
come, T003b alone: the
model-context recording and a fake-provider bench run end to end, inventoried
at R11 before it is built.
--- END SLICE CTXSCOPE-TO ---

--- BEGIN SLICE CTXSTEPS2-FROM --- (in .agent/context.md, C4 — REWRITE pair)
stale claim ✅ → R10 T003a the stats bench read view → R11 T003b model context
and a fake-provider run → R12 the integration gate → R13 closure. T003 split
into two halves at DECISION F082 D5; R10 marks R9 done and never itself.
--- END SLICE CTXSTEPS2-FROM ---

--- BEGIN SLICE CTXSTEPS2-TO --- (C4)
stale claim ✅ → R10 T003a the stats bench read view ✅ → R11 record the R10
verdict and answer the T003b inventory → R12 T003b model context and a
fake-provider run → R13 the integration gate → R14 closure. T003 split at
DECISION F082 D5 and its second half inventoried first at D6; each round marks
the PREVIOUS one done and never itself.
--- END SLICE CTXSTEPS2-TO ---

--- BEGIN SLICE FORTSCHRITT --- (the Fortschritt line; the handoff repeats it VERBATIM, R-0418)
Fortschritt: ~76 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b inventoried, not built) — Schätzung
--- END SLICE FORTSCHRITT ---

--- BEGIN SLICE PLAN --- (WHOLE-FILE replacement of .agent/plan.md, C4)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0419. Open findings: forty-eight — the thirty-two carried from F077, plus
R-0403 to R-0418 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R11 records the R10 gate, registers the reviewer-block defect R-0418, retires
the scope sentence R10's own change made half-stale, and answers the seven
T003b inventory questions in the feature file's Built State. It writes no code.

## Next Steps
1. R12 — T003b: model-context recording and a fake-provider bench run end to
   end, ordered against R11's answers rather than against a guess.
2. R13 the integration gate, R14 closure.

## Risks
- T003b's shape is UNKNOWN until R11's Q1-Q4 are answered. No `model_context`
  symbol exists in any bench module today, and only one role is bound to a
  model. If Q4 answers (c), T003b cannot be built additively and the feature
  file's Design bullet needs an operator-visible amendment.
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- Two acceptance criteria may be unpinned by any test (R11 Q7). An unpinned
  criterion discovered at closure is a closure blocker, which is why Q7 is
  asked three rounds early.
- Seven of the last nine findings are reviewer-block defects, not worker
  defects. R-0417's standing staleness gate and R-0418's Fortschritt rule are
  the counter-measures; both now bind every block.
--- END SLICE PLAN ---

────────────────────────── DONE WHEN ──────────────────────────
Run every gate. Record its REAL output. "Green" as a word is a finding.
BASE is the SHA this round starts from: 9f2ab66d.

 1. `git status --porcelain` EMPTY at handback; `git worktree list` back to
    exactly the primary checkout. Report both verbatim.
 2. TRANSPORT AS A PROPERTY: sha256 and byte length of
    `.remedy-wt/f082-r11-scratchpad.md`, `.agent/authored/f082-r11.md` and
    `.agent/last_block.md`. All three EQUAL. `cp`/`cmp` are denied to this
    session class (R-0408) — use `sha256sum` plus a python3 `read_bytes()`
    equality. Report the shared digest and the line count; it must be ≤ 400.
 3. `.agent/STOP` — report presence at round START and at handback. Absent
    both times. If it appears, finish the current commit and hand off.
 4. C1 APPEND PROOF: over the COMMITTED `<C1>^` and `<C1>`, report whether
    `post == pre + add` holds BYTE-WISE, where `add` is GATE-R10,
    FINDING-R418 and DECISION-D6 joined exactly as committed. Report the C1
    `--numstat`; its DELETION column must be 0.
 5. RECORD COUNTS in `.agent/live_review.md` at HEAD: `^Gate: R10 — PASS` 1 ·
    `^- R-0418 — ` 1 · `^## DECISION F082 D6` 1 · `^Landed: ` 0 · `^Done: ` 0.
    Report each real number.
 6. OPEN SET RECOMPUTED MECHANICALLY: every `^- R-\d+ — ` paragraph minus
    every `^Done: R-\d+ — ` line. Report the count, the max id, the next free
    id, and any duplicate. R11 registers exactly one finding, R-0418, so the
    expected count is FORTY-EIGHT and the next free id becomes R-0419 —
    report the real numbers whatever they are.
 7. BOTH CONTEXT PAIRS AS PROPERTIES: report whether
    `post == pre.replace(CTXSCOPE_FROM, CTXSCOPE_TO)` holds byte-wise over
    the committed C2, and whether
    `post == pre.replace(CTXSTEPS2_FROM, CTXSTEPS2_TO)` holds byte-wise over
    the committed C4. Both are REWRITES: each FROM 1x before and 0x after,
    each TO 1x after.
 8. `.agent/plan.md` at HEAD BYTE-EQUALS the PLAN slice as a WHOLE FILE.
    Report its sha256 and `wc -l`; under 50. Report `wc -l` for
    `.agent/context.md`. Contract readers of `.agent/context.md`:
    `## Active Branch` followed by a `feature/` slug · substring `Steps` ·
    a roadmap F-id · `pytest` or `resource`. Plan keeps `## Goal` and
    `## Next Steps`.
 9. STANDING STALENESS GATE (R-0417, third run). Re-read every sentence in
    the files this round touched that states a COUNT, a module list, a
    round→step map, or a completion claim, and report for each whether it
    still holds at HEAD. Repair ONLY what the ordered pairs cover; report
    everything else and leave it. State how many sentences you checked.
10. CHANGE SET: `git diff --name-only 9f2ab66d..HEAD` — report every path,
    COUNT them, and state whether you measured before or after C5. The Change
    list is a CEILING. Report
    `git diff --name-only 9f2ab66d..HEAD -- apps/ packages/ tests/`
    separately; it MUST be EMPTY. This round writes no code.
11. THE INVENTORY IS THE DELIVERABLE. Report, for each of Q1 to Q7, the
    answer's first sentence and the citation it carries. Seven questions,
    seven answers, seven citations — state the count you actually wrote. An
    answer without a `path.py::symbol` citation is not an answer; say so
    rather than padding it.
12. `python3 -m pytest tests/docs/ -q` → exit 0. The docs-round gate binds
    because the change set includes `docs/roadmap/**`
    (planner_reviewer_prompt.md §3, tier 5). The reviewer ran this suite at
    9f2ab66d today: 295 passed. This round adds no docs test, so 295 is the
    expected total. Report the real number; any other is a finding.
13. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer baseline at
    9f2ab66d: 184 passed. This round changes no code, so 184 is expected.
14. `python3 -m pytest tests/cli/test_stats_bench.py -q` → exit 0, 25 passed.
    R10's work must still stand; this round may not disturb it.
15. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `handler_import` message; it
    must still be `handlers=337`. A different number means this round touched
    registration, which its Change list forbids.
16. `gh pr list --state open --json number,headRefName` → report verbatim.
    Must be `[]`.
17. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it with the inseparability reason BEFORE review. C5
    cannot state its own numstat; report it in the completion report.
No mutation red-proof is ordered and none is owed: R11 changes no executable
line. Ordering a colour over unchanged code is what R-0364 and R-0252 forbid.

Handback:    Completion report + rewrite `.agent/handoff.md` per
             docs/agents/handback_template.md: feature and round, branch, the
             per-commit changed-files tables, the real verification values
             above, the item-status table with every C0a–C5 item and every
             gate 1–17 appearing exactly once, open-findings count, and the
             next expected action. Declare every deviation with its cause.
             The handoff repeats the FORTSCHRITT slice above VERBATIM — that
             slice exists because R-0418 was raised for its absence. Push
             after every commit. Create NO pull request.
──────────────────────────────────────────────────────────────────────────────
