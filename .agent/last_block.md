── STEP R14/17 — F082 Self-benchmark ─────────────────────────────────────────
Goal:        Record the R13 verdict, register the three reviewer-block defects
             R13 surfaced — two of which the WORKER found and the reviewer
             confirmed — and bring both mirrors back to true. No code.

Bundle:      C0a save this block · C0b mirror it · C1 GATE-R13 + FINDINGS-R420-422
             appended to the review record · C2 plan and context re-sync · C3
             handback.

Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r14.md   (C0a, new)
             - .agent/last_block.md          (C0b)
             - .agent/live_review.md         (C1 append)
             - .agent/plan.md                (C2 whole-file)
             - .agent/context.md             (C2, two pairs)
             - .agent/handoff.md             (C3)
             NOT in scope: `apps/**`, `packages/**`, `tests/**`, `scripts/**`,
             `docs/**`. This round writes no code, no test and no doc.
             `git diff --name-only a03b4164..HEAD -- apps/ packages/ tests/
             scripts/ docs/` must be EMPTY.

Constraints:
 1. DECISION F082 D7 and D8 ARE NOT REWRITTEN, and neither is any prior gate
    entry. They are time-stamped history. R-0421 corrects D8's numeral by
    APPENDING a finding that quotes the false clause, exactly as R-0419
    corrected D6 — a reader who lands on D8 must be able to find R-0421.
 2. `.agent/plan.md` and `.agent/context.md` ARE NOT HISTORY. They are live
    mirrors and must be TRUE at every commit, so the stale Scope sentence and
    the stale step map are replaced by the pairs below.
 3. NO NUMERAL WITHOUT A COUNT. Every count in this block was taken
    mechanically by the reviewer before the block was written. If you restate
    any of them in the handback, re-measure rather than copy.
 4. `.agent/plan.md` stays under 50 lines and keeps `## Goal` and
    `## Next Steps`. `.agent/context.md` keeps `## Active Branch` with its
    `feature/` slug, the substring `Steps`, a roadmap F-id, and `pytest` or
    `resource`.
 5. Apply every slice DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r14.md`. No `--- BEGIN SLICE` / `--- END SLICE`
    marker line may reach any target file. No target file gains a
    trailing-whitespace line.
 6. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    Insertions per commit stay under 500. No commit trailer.
 7. Apply every slice VERBATIM. If a slice is wrong on arrival, apply it as
    ordered and DECLARE it — do not silently repair it (R-0419). Reporting a
    reviewer's error is the behaviour this round exists to reward.

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE GATE-R13 --- (append to .agent/live_review.md, C1, ONE physical line)
Gate: R13 — PASS, with three new findings, ALL of them the reviewer's, and two of the three found by the worker before the reviewer saw them. Verification tier: round gate plus the canary plus a scoped-ruff gate and a red-proof; no full-suite claim is made and none is owed. Every ordered gate was re-executed by the reviewer against the disk rather than read out of the handback. The deliverable is real and was checked as behaviour, not as bytes: `git diff b0ea45c9..HEAD -- packages/` shows the six runner pairs and the intake pair applied exactly as authored, and the write half of T003b now works — a gauntlet run records which model served which role in its own `run.json`. DECISION F082 D7's three conditions are met and each was measured rather than asserted. ADDITIVITY: the emitted body's key set is the sixteen base keys plus `models` and nothing else, pinned by `test_bench_model_context.py::test_the_emitted_body_is_the_base_key_set_plus_models`, whose `BASE_BODY_KEYS` the reviewer verified name-by-name against `_evidence_body` at BASE rather than trusting the constant. THE SEVEN STAY GREEN UNMODIFIED: `276 passed`, exactly the reviewer's BASE measurement, and `git diff --name-only b0ea45c9..HEAD` restricted to those seven paths is EMPTY, so the additive claim is proven on both axes — the tests pass AND none of them was edited to make them pass. ABSENCE STAYS ABSENT: an unlabelled call_fn and a null call_fn both record `None`, never a default name, and the run's own bytes carry no `llama` and no `muse-glimmer:latest`. The transport is proven at PRIMARY strength — `.agent/authored/f082-r13.md` and `.agent/last_block.md` are byte-identical at sha256 `51e9713974d636e82af7ac28896c1328ce05191d139fb739c3ef3a74ae4ad9c2` — and the C1 append is a PROPERTY, `post == pre + add` TRUE byte-wise over the committed `3450762a^`→`3450762a` with the appended region 7955 bytes and the numstat deletion column 0. The record counts are `^Gate: R12 — PASS` 1, `^## DECISION F082 D8` 1, `^## DECISION F082 D7` 1 still standing, `^Landed: ` 0 and `^Done: ` 0, and the open set recomputed mechanically is FORTY-NINE with no duplicate and max R-0419, exactly as ordered for a round that registers nothing. The reviewer re-proved the slice pairs itself rather than accepting the worker's composite: every one of the six runner FROMs goes 1x to 0x and every TO lands 1x, `FROM in TO` is False for all eight pairs, the INTAKE and CTXSTEPS4 single-pair equalities hold, and the composite `pre` with all six replacements applied in block order EQUALS `post` — so the worker's declared gate-7 deviation is exactly what the disk shows and is a defect in the reviewer's gate, not in the work. Suites re-run by the reviewer at the branch head: the gauntlet seven `276 passed`, the new `test_bench_model_context.py` plus both intake suites plus `test_stats_bench.py` `76 passed` together, the canary plus the three contract readers `184 passed` and therefore UNMOVED by a change to a shared factory, `ruff check` over the three owned files `All checks passed!`, and `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with `handler_import` still `handlers=337`. The change set is nine paths, every one inside the block's Change list, `-- docs/ apps/ scripts/` is EMPTY, insertions per commit are 457, 364, 59, 40, 245, 20 and 92 with none over 500, `git status --porcelain` is empty, `git worktree list` is the single primary checkout so the red-proof worktree was really removed, `.agent/STOP` is absent and `gh pr list --state open` is `[]`. The round's most valuable act was the same one R12 was praised for, and it is becoming this branch's strongest habit: Constraint 7 ordered verbatim application, the block was wrong twice, and the worker applied it as ordered and declared both rather than quietly fixing them — which is right twice over, because a silent repair would have broken the byte-equality that makes transport provable and would have hidden a reviewer defect that is now written down as R-0420 and R-0421. No block condition was hit: no fabricated data, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R13 ---

--- BEGIN SLICE FINDINGS-R420-422 --- (append to .agent/live_review.md, C1, after GATE-R13, one blank line between the gate and this slice)
- R-0420 — Medium, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer by measuring the committed block. The R13 block is FOUR HUNDRED AND FIFTY-SEVEN lines against the four-hundred-line cap that DECISION F105 D5 sets and that `.agent/context.md` restates with 240 as the preferred target (R-0381). The reviewer never measured it. This is the third distinct member of the same family on this branch — R-0402 and R-0404 were miscounted enumerations, R-0417 was a staleness sweep claimed rather than run — and they share one root cause: the reviewer states a quantity about its OWN text without executing a count on the final bytes. No downstream cap was breached, because C0a's 457 insertions are still inside the 500-insertion commit limit, which is the only reason this is Medium and not High; the cap exists precisely to keep that distance, and spending it unknowingly is the defect. Standing rule from here, binding the reviewer: the block's line count is MEASURED on the final bytes immediately before emission, and the measured number is stated in the delegation so the worker can contradict it. A cap that is only remembered is not a cap.

- R-0421 — Medium, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer with a repository-wide grep. DECISION F082 D8 states that `packages/orchestration/intake.py::make_structured_call_fn` "has six call sites" and then, in the very same sentence, enumerates seven of them — one in `intake.py` itself, two in `gauntlet_runner.py`, two in `apps/cli/commands/mission_cmd.py` and two in `apps/cli/commands/do_cmd.py`. The enumeration is CORRECT and the numeral is wrong: the real count is SEVEN, at `intake.py:324`, `gauntlet_runner.py:216` and `:225`, `mission_cmd.py:227` and `:385`, and `do_cmd.py:246` and `:2864`. This is the R-0402 and R-0404 class recurring for the third time, and the aggravating detail is that D8's own preceding sentence claims the count "was taken with a repository-wide grep before this decision was written" — the grep WAS run and did return seven; the numeral was then written from memory rather than from the grep's output, which is the exact failure the rule was written to stop. It is Medium rather than Low because it sits inside a DECISION, the most durable record this branch keeps, where a wrong number outlives every round that could have caught it. The decision's substance is untouched: the exception it grants is safe at seven call sites for precisely the reason it gives, that none of them is affected. Standing rule from here, binding the reviewer: a numeral that introduces a list is written by COUNTING that list after the list is final, never before and never from the search that produced it.

- R-0422 — Low, REVIEWER-GATE DEFECT, found by the worker and confirmed by the reviewer by re-deriving the property. R13's gate 7 ordered, for each of eight slice pairs, that `post == pre.replace(FROM, TO)` hold "over its own COMMITTED revision" — while the same block's Bundle put six of those eight pairs into ONE commit, C2. The property is therefore structurally unreachable for those six: applying a single replacement to `pre` can never reproduce a `post` that carries six, so a truthful worker must report False six times for a change that is entirely correct. The worker did the right thing and reported the composite instead — `pre` with all six replacements applied in block order EQUALS `post`, which the reviewer independently re-derived — but it had to invent the correct gate at handback time, which is the reviewer's job. This is the R-0371 family, a gate that cannot be satisfied as written, in its arithmetic form rather than its self-reference form. Standing rule from here, binding the reviewer: when N pairs share one commit, the block orders the COMPOSITE property over that commit plus the per-pair FROM 1x-to-0x and TO 0x-to-1x counts, which ARE individually measurable, and never a per-pair whole-file equality.
--- END SLICE FINDINGS-R420-422 ---

--- BEGIN SLICE CTXSCOPE-FROM --- (in .agent/context.md, C2 — REWRITE pair)
file, adding exactly one handler key and changing no bench module. Still to
come, T003b alone: the
model-context recording and a fake-provider bench run end to end, inventoried
at R11 before it is built.
--- END SLICE CTXSCOPE-FROM ---

--- BEGIN SLICE CTXSCOPE-TO --- (C2)
file, adding exactly one handler key and changing no bench module. T003b's
WRITE half landed at R13 under DECISION F082 D7 and D8: a run's `run.json` now
carries a `models` key naming which model served which role, fed by a
`resolved_model` attribute on the callable
`intake.py::make_structured_call_fn` returns, with the builder recorded as a
permanent absence because `orchestrator_loop.py::execute_dispatched_job`
constructs `OllamaBuilder()` where no seam can observe it. Still to come,
T003b's read half — those models into the bench record — and the fake-provider
bench run end to end, inventoried at R11 before either is built.
--- END SLICE CTXSCOPE-TO ---

--- BEGIN SLICE CTXSTEPS5-FROM --- (in .agent/context.md, C2 — REWRITE pair)
gauntlet key at D7 ✅ → R13 T003b the write half, every run recording which model
served which role → R14 T003b the read half and the fake-provider run → R15 the
integration gate → R16 closure. T003 split at DECISION F082 D5, its second half
inventoried at D6, unblocked at D7 and split in two at D8; each round marks the
PREVIOUS one done and never itself.
--- END SLICE CTXSTEPS5-FROM ---

--- BEGIN SLICE CTXSTEPS5-TO --- (C2)
gauntlet key at D7 ✅ → R13 T003b the write half, every run recording which model
served which role ✅ → R14 record the R13 verdict and register R-0420 to R-0422
→ R15 T003b the read half and the fake-provider run → R16 the integration gate
→ R17 closure. T003 split at DECISION F082 D5, its second half inventoried at
D6, unblocked at D7 and split in two at D8; each round marks the PREVIOUS one
done and never itself.
--- END SLICE CTXSTEPS5-TO ---

--- BEGIN SLICE FORTSCHRITT --- (the Fortschritt line; the handoff repeats it VERBATIM, R-0418)
Fortschritt: ~82 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b Schreibhälfte gebaut und gegated · Lesehälfte und Fake-Provider-Lauf offen) — Schätzung
--- END SLICE FORTSCHRITT ---

--- BEGIN SLICE PLAN --- (WHOLE-FILE replacement of .agent/plan.md, C2)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0423. Open findings: fifty-two — the thirty-two carried from F077, plus
R-0403 to R-0422 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R14 records the R13 gate and registers R-0420, R-0421 and R-0422 — a block over
its line cap, a numeral that contradicted its own enumeration, and a gate that
could not be satisfied as written. All three charge the reviewer; the worker
found two of them. It writes no code.

## Next Steps
1. R15 — T003b the read half and the run: carry `models` from
   `gauntlet_evidence.py::RunEvidence` into the bench record, which needs its
   own additive ruling because that is a third gauntlet module; then the
   fake-provider bench run, clearing R11's Q6 four blockers — no entry point,
   local-Ollama reach, a `time.monotonic()` call in `::run_order`, and history
   resolving to the real data root; and the Q7 pin for "the bench never runs
   implicitly".
2. R16 the integration gate, R17 closure.

## Risks
- "The bench never runs implicitly" is an ACCEPTANCE criterion that NO test
  pins (R11 Q7). It holds today only by absence: `append_bench_run` and
  `dry_run_from_order_set` have no caller under `apps/`, `packages/` or
  `scripts/`. An unpinned criterion found at closure is a closure blocker, so
  R15 pins it.
- The builder's model stays unobservable, because making it visible means
  reaching into `orchestrator_loop.py::execute_dispatched_job`. Closure states
  that absence rather than implying three roles were recorded.
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- Reviewer-block defects are the dominant finding class on this branch, and
  three more landed at R13. No count of the class is stated here because none
  has been taken. The counter-measures now standing are R-0417's staleness
  gate, R-0418's Fortschritt rule, R-0419's grep-every-writer rule, R-0420's
  measure-the-block rule, R-0421's count-the-list rule and R-0422's
  composite-property rule, and all six bind every block from here.
--- END SLICE PLAN ---

────────────────────────── DONE WHEN ──────────────────────────
Run every gate. Record its REAL output. "Green" as a word is a finding.
BASE is a03b4164.

 1. `git status --porcelain` EMPTY at handback; `git worktree list` back to
    exactly the primary checkout. Report both verbatim.
 2. TRANSPORT AS A PROPERTY: sha256 and byte length of
    `.agent/authored/f082-r14.md` and `.agent/last_block.md`. EQUAL, proven by
    python3 `read_bytes()` equality as well as by digest. Report the shared
    digest AND the measured line count. The reviewer measured this block at
    246 lines before emission (R-0420's new rule). Report the REAL number and
    say whether it matches; a mismatch is the reviewer's defect to own, not
    yours to fix.
 3. `.agent/STOP` — report presence at round START and at handback. Absent
    both times. If it appears, finish the current commit and hand off.
 4. C1 APPEND PROOF: over the COMMITTED `<C1>^` and `<C1>`, report whether
    `post == pre + add` holds BYTE-WISE, where `add` is GATE-R13 and
    FINDINGS-R420-422 joined exactly as committed. Report the C1 `--numstat`;
    its DELETION column must be 0.
 5. RECORD COUNTS in `.agent/live_review.md` at HEAD: `^Gate: R13 — PASS` 1 ·
    `^- R-0420 — ` 1 · `^- R-0421 — ` 1 · `^- R-0422 — ` 1 ·
    `^## DECISION F082 D8` 1 (still there — D8 is history and is NOT
    rewritten) · `^Landed: ` 0 · `^Done: ` 0. Report each real number.
 6. OPEN SET RECOMPUTED MECHANICALLY: every `^- R-\d+ — ` paragraph minus
    every `^Done: R-\d+ — ` line. Report the count, the max id, the next free
    id, and any duplicate. R14 registers exactly three findings, so the
    expected count is FIFTY-TWO and the next free id becomes R-0423 — report
    the real numbers whatever they are.
 7. BOTH CONTEXT PAIRS AS PROPERTIES, over the COMMITTED C2. The two pairs
    share one commit, so report the COMPOSITE — `pre` with BOTH replacements
    applied EQUALS `post` — plus, per pair, FROM going 1x to 0x and TO going
    0x to 1x, and `FROM in TO`. This is R-0422's own rule applied to the block
    that registers it.
 8. `.agent/plan.md` at HEAD BYTE-EQUALS the PLAN slice as a WHOLE FILE.
    Report its sha256 and `wc -l`; under 50. Report `wc -l` for
    `.agent/context.md`. Contract readers of `.agent/context.md`:
    `## Active Branch` followed by a `feature/` slug · substring `Steps` ·
    a roadmap F-id · `pytest` or `resource`. Plan keeps `## Goal` and
    `## Next Steps`.
 9. THE CORRECTION LANDED WHERE IT WAS OWED, AND ONLY THERE. Count
    `Still to come, T003b alone` in `.agent/context.md` at HEAD: it must be 0.
    Count `has six call sites` in `.agent/live_review.md`: it must be exactly
    1 — the ORIGINAL inside DECISION F082 D8, which Constraint 1 forbids
    rewriting. R-0421 deliberately does NOT quote that phrase verbatim, so a 2
    here means the record was edited or the finding was rewritten; report
    which.
10. CHANGE SET: `git diff --name-only a03b4164..HEAD` — report every path,
    COUNT them, and state whether you measured before or after C3. The Change
    list is a CEILING. Report
    `git diff --name-only a03b4164..HEAD -- apps/ packages/ tests/ scripts/
    docs/` separately; it MUST be EMPTY.
11. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer baseline at
    BASE: 184 passed. This round changes no code, so 184 is expected.
12. `python3 -m pytest tests/orchestration/test_bench_model_context.py
    tests/orchestration/test_gauntlet_runner.py -q` → exit 0. R13's work must
    still stand. Report the real number.
13. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `handler_import` message; it
    must still be `handlers=337`.
14. `gh pr list --state open --json number,headRefName` → report verbatim.
    Must be `[]`.
15. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it with the inseparability reason BEFORE review. C3
    cannot state its own numstat; report it in the completion report.
16. STANDING STALENESS GATE (R-0417, sixth run). Re-read every sentence in the
    files this round touched that states a COUNT, a module list, a round→step
    map, or a completion claim, and report for each whether it still holds at
    HEAD. Repair ONLY what the ordered slices cover; report everything else and
    leave it. State how many sentences you checked.
No mutation red-proof is ordered and none is owed: R14 changes no executable
line. The docs-round gate does NOT bind: `docs/**` is outside this round's
Change list, and gate 10 proves it.

Handback:    Completion report + rewrite `.agent/handoff.md` per
             docs/agents/handback_template.md: feature and round, branch, the
             per-commit changed-files tables, the real verification values
             above, the item-status table with every C0a–C3 item and every
             gate 1–16 appearing exactly once, open-findings count, and the
             next expected action. Declare every deviation with its cause.
             The handoff repeats the FORTSCHRITT slice above VERBATIM (R-0418).
             Push after every commit. Create NO pull request.

             THE NEXT SESSION'S FIRST ACTION is self_drive_protocol.md Phase 1
             rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR
             Gate. Say so in the handoff's Next section. F082 is MID-FEATURE
             and no PR exists. The next round is R15, T003b's read half and the
             fake-provider run.
──────────────────────────────────────────────────────────────────────────────
