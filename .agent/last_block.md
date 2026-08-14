── STEP R16/19 — F082 Self-benchmark ─────────────────────────────────────────
Goal:        Record the R15 verdict, register the two defects it surfaced, and
             pin F082's last unpinned acceptance criterion — "the bench never
             runs implicitly" — in the form that will still be true after the
             fake-provider run exists (DECISION F082 D9).

Bundle:      C0a save this block · C0b mirror it · C1 GATE-R15 + FINDINGS-R427-428
             + DECISION-D9 appended to the review record · C2 the Q7 pin, a NEW
             test file authored from the contract below · C3 plan and context
             re-sync · C4 handback.

Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r16.md                          (C0a, new)
             - .agent/last_block.md                                 (C0b)
             - .agent/live_review.md                                (C1 append)
             - tests/orchestration/test_bench_never_runs_implicitly.py (C2, NEW)
             - .agent/plan.md                                       (C3 whole-file)
             - .agent/context.md                                    (C3, three pairs)
             - .agent/handoff.md                                    (C4)
             NOT in scope: `docs/**`, `apps/**`, `packages/**`, `scripts/**`,
             every gauntlet module, and every PRE-EXISTING test file. This round
             writes NO production code — gate 11 proves it.

Constraints:
 1. THIS ROUND BUILDS NO DRIVER. The fake-provider bench run is R17's whole
    deliverable and nothing here anticipates it. R16 pins the criterion; R17
    lands the entry point and amends the allowlist by one name.
 2. THE PIN MUST NOT BE VACUOUS. An absence test that passes because it looked
    at nothing, or because the symbol it guards was renamed, is worse than no
    test — it reports green forever. Properties 1 and 5 of the contract exist
    only to make a vacuous pass impossible, and gate 9 proves the pin can go
    red by making it go red.
 3. THE ALLOWLIST IS EMPTY TODAY AND THAT IS A MEASURED FACT, not an assumption.
    The reviewer grepped `append_bench_run` and `dry_run_from_order_set` across
    `apps/`, `packages/` and `scripts/` before this block was written: the only
    matches in that tree are their own two `def` lines, zero call sites. The
    contract's AST rule is what keeps that distinction honest, because a
    substring grep cannot tell a definition from a call.
 4. `.agent/plan.md` stays UNDER 50 lines and keeps `## Goal` and `## Next
    Steps`. The PLAN slice was measured at 48 lines before emission (R-0423).
 5. Apply every REWRITE-PAIR slice DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r16.md`. No `--- BEGIN SLICE` / `--- END SLICE`
    marker line may reach any target file. No target file gains a
    trailing-whitespace line. C2 is authored by YOU from the contract, not
    transported.
 6. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    Insertions per commit stay under 500. No commit trailer.
 7. Apply every slice VERBATIM. If a slice is wrong on arrival, apply it as
    ordered and DECLARE it — do not silently repair it (R-0419). Reporting a
    reviewer's error is the behaviour this round exists to reward.
 8. DECISION F082 D7, D8 and every prior gate entry ARE NOT REWRITTEN. They are
    time-stamped history. D9 is APPENDED and supersedes nothing.

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE GATE-R15 --- (append to .agent/live_review.md, C1, ONE physical line)
Gate: R15 — PASS, with two new findings, both of them the reviewer's, and one of the two found by the worker before the reviewer saw it. Verification tier: round gate plus the canary; the round changed executable lines in two bench modules, and every suite that reaches them was re-run, so the additive claim is measured rather than argued. All eighteen ordered gates were re-executed by the REVIEWER against the disk rather than read out of the handback, and every reported value reproduces. Transport is proven at PRIMARY strength: the committed `.agent/authored/f082-r15.md`, the same file on disk, `.agent/last_block.md` and the emitted scratch block are all byte-identical under python3 `read_bytes()`, sha256 `8640cc245e246ce2af166923f1b63bd92d5cb4afa59ffdc7bafddf14e886114c`, 31724 bytes, and the measured line count is 399 — exactly the number the block stated before emission, so R-0420's rule held for a second consecutive round. The C1 append is a PROPERTY: over the committed `434d0763^` to `434d0763` the reviewer re-derived that `post` equals `pre` followed by a newline, the GATE-R14 slice, a blank line, the FINDINGS-R423-426 slice and a closing newline, TRUE byte-wise, with `pre` a prefix of `post`, the added region 8274 bytes and the numstat deletion column 0. Record counts at HEAD are `^Gate: R14 — PASS` 1, `^- R-0423 — ` 1, `^- R-0424 — ` 1, `^- R-0425 — ` 1, `^- R-0426 — ` 1, `^## DECISION F082 D8` 1, `^## DECISION F082 D7` 1, `^Landed: ` 0 and `^Done: ` 0, and the open set recomputed mechanically is FIFTY-SIX with no duplicate, max R-0426 and next free R-0427. The C2 read half was proven as two per-file composites exactly as R-0422 demands: `pre` with all five replacements applied EQUALS `post` for `capability_bench.py` and with both replacements for `bench_history.py`, and each of the seven pairs shows FROM 1x to 0x, TO 0x to 1x and `FROM in TO` False. C3 is an extension and not a rewrite: `^def test_` goes 8 to 14, every test name present at BASE is still present at HEAD, and the numstat is 104 insertions against 0 deletions. `.agent/plan.md` byte-equals the PLAN slice as a whole file at sha256 `70694566f1c08630bb39e47b4bc4eae0e69804b45f073e72a2349531a791e6ea`, 48 lines — back UNDER the AGENTS.md fifty-line cap that R-0423 recorded as broken, so the finding registered in this same round is also repaired on disk by it. The change set is nine paths, every one inside the block's Change list, and the range restricted to apps, docs and scripts is EMPTY. Marker lines reaching any target: 0. Trailing-whitespace lines gained in any target: 0. Suites re-run by the reviewer at the branch head: `test_bench_model_context.py` `14 passed` exit 0, risen from the BASE of 8 by exactly the six new pins; the gauntlet's seven `276 passed` exit 0 and the pre-existing bench five `61 passed` exit 0, both UNCHANGED from their base values, which is the additivity claim measured on the axis that matters; the canary plus the three contract readers `184 passed` exit 0; scoped `ruff check` `All checks passed!` exit 0; and `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with `handler_import` still `handlers=337`. Insertions per commit are 399, 326, 10, 27, 104, 39 and 103, none over 500, `git status --porcelain` is empty, `git worktree list` is the single primary checkout, `.agent/STOP` is absent and `gh pr list --state open` is `[]`. The reviewer went past the ordered gates twice, because a gate list is a floor and R-0220 is the finding that says a green gate is not a working feature. First, CALLER COVERAGE: every caller of the two changed functions — `apps/cli/commands/bench_cmd.py:336` for `load_bench_history` and `packages/orchestration/bench_dry_run.py:115` for `build_bench_record` — is exercised by a suite that ran green, so the changed code is reached and not merely compiled. Second, BACK-COMPAT ON PRODUCTION GOLDENS: the four real fixtures under `tests/orchestration/fixtures/bench_history/` were read and carry no `models` key at all, and they load clean through the real reader returning `models is None` — which is stronger evidence than the hand-written row C3 property 6 pins, because a golden nobody wrote for this change cannot have been shaped to pass it. The round's decisive quality was that NO slice was wrong on arrival for the first time in several rounds: all seven code FROMs, all three context FROMs and the whole-file PLAN slice matched at exactly 1x, so the two findings below are the reviewer's own and neither cost the worker a wasted commit. No block condition was hit: no fabricated data, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R15 ---

--- BEGIN SLICE FINDINGS-R427-428 --- (append to .agent/live_review.md, C1, after GATE-R15, one blank line between the gate and this slice)
- R-0427 — Low, STALE CLAIM IN SHIPPED CODE, found by the worker under the standing staleness gate and confirmed by the reviewer by reading the file. The module docstring of `packages/orchestration/bench_history.py`, at lines 16 to 18, reads "ADDITIVE by construction (F082 inventory Q11): `BenchRecord` and `projects_dir` are IMPORTED. No symbol moves out of a bench or gauntlet module and none is edited." R15 edited `BenchRecord`: it gained the `models` field. Under the sentence's present-tense reading — no symbol is edited — the claim is now false in shipped code. Under the narrower reading the paragraph's own heading suggests — no GAUNTLET module is edited, which is the additivity the F082 inventory Q11 actually ruled on — it still holds, and that reading is the one every round on this branch has enforced. The ambiguity is the defect: a docstring that states an invariant has to state which invariant, because the next reader will apply whichever reading is convenient. Low, because no behaviour depends on it and the additive design itself is intact and measured. The worker did exactly the right thing under gate 18 — reported it and left it, since no ordered slice covered that file — and that conduct is why it is on the record instead of being quietly rewritten inside an unrelated commit. Repaired at R17, which touches that module anyway for the run: the sentence is rewritten to name the gauntlet reading explicitly, or it is deleted, and no third option is invented. Standing rule from here: an invariant sentence in a module docstring names the set it quantifies over, because "no symbol is edited" and "no gauntlet symbol is edited" are different promises and only one of them is kept.

- R-0428 — Low, REVIEWER-BLOCK DEFECT, found by the reviewer at the start of the round while re-verifying the carried block, and corrected before any worker saw it. The R15 block was authored in one session and delegated in the NEXT one, and it named `BASE is 22ef2427` in four places — the handback SHA that was HEAD when it was written. By the time it was delegated, HEAD was 56635794, because the authoring session's own handoff commit landed AFTER the block was finished. Every range gate in the block therefore addressed a base one commit behind the commit the round actually started from, and `git diff --name-only 22ef2427..HEAD` would have attributed a prior session's `.agent/handoff.md` change to R15. The reviewer re-derived the base from HEAD at delegation time, replaced all four occurrences, and re-measured the block: the substitution is length-preserving, so the line count stayed at 399 and only the digest moved, from `8f5eddfc…` to `8640cc24…`. Low, because no round was ever gated against the stale base and no measured value was affected. It is registered anyway because the CAUSE is structural and new: this is R-0368's family — a range gate's base is the SHA the round starts from — recurring in the shape that only self-drive produces. Under the split workflow a block is authored and delegated inside one relay, so its base cannot move between the two; under `docs/agents/self_drive_protocol.md` a session can end at a STOP or a limit with a block authored and unapplied, and the handoff commit that ends that session is itself the commit that invalidates the base. The handoff's own instruction made it worse by naming the block's sha256 as the thing to verify, which the reviewer did — it matched, and matching proved only that the file had not been touched, not that its base was still current. Standing rule from here, binding the reviewer: a block carried across a session boundary re-derives its BASE from HEAD at DELEGATION time and re-states it, and a handoff that carries an unapplied block says so next to the sha256 it quotes. A digest that still matches is evidence about the file, never about the repository around it.
--- END SLICE FINDINGS-R427-428 ---

--- BEGIN SLICE DECISION-D9 --- (append to .agent/live_review.md, C1, after FINDINGS-R427-428, one blank line before it)
## DECISION F082 D9 — the Q7 criterion is pinned as an enumerated allowlist, not as a total absence

Chosen 2026-08-15 by the reviewer under docs/agents/planner_reviewer_prompt.md
§4 item 7, which routes a wrong plan into the current block as a loud,
persisted, reversible decision rather than a question. The plan carried by R11's
Q7 and repeated in `.agent/plan.md` said a later round "owes a test that asserts
the absence of an implicit caller", and R15's plan bundled that pin with the
fake-provider run in one round, R16. Both readings are unsafe together, and the
reason is arithmetic rather than taste: the criterion "the bench never runs
implicitly" holds TODAY because `bench_history.py::append_bench_run` and
`bench_dry_run.py::dry_run_from_order_set` have no caller anywhere under
`apps/`, `packages/` or `scripts/` — the reviewer re-measured that before
writing this, and the only matches in that tree are the two `def` lines
themselves. The fake-provider run's whole deliverable is a driver that CALLS
both. A pin written as a total absence would therefore be falsified by the very
round that completes the feature, and a gate that the feature's own completion
breaks is the R-0424 class — a gate that cannot be satisfied as written, found
one round before it fires instead of one round after.

Chosen instead: the pin asserts that the set of modules calling either write
entry point equals an ALLOWLIST enumerated in the test, and that the allowlist
is EMPTY today. R17 adds exactly one name to it when the driver lands. The
criterion survives the run because "never implicitly" was never a claim that
nothing calls the bench — it is a claim that nothing calls it as a SIDE EFFECT
of doing something else, and an enumerated caller is the opposite of an implicit
one. The allowlist edit is the visible, reviewable act that says the bench
gained an explicit entry point, which is exactly the event an acceptance
criterion should force into the diff.

Two alternatives were considered and rejected. Pinning the total absence now and
editing the test at R17 was rejected because a test whose failure is the
EXPECTED outcome of the next round teaches the next worker to edit tests to
green, which is the habit this repository spends the most effort refusing.
Deferring the pin to closure was rejected because R11's Q7 already establishes
that an unpinned acceptance criterion is a closure blocker, and moving a blocker
closer to the closure it blocks is not a plan.

Consequence for the round map: the Q7 pin and the fake-provider run separate.
R16 is the pin, R17 the run, R18 the integration gate, R19 closure — one round
longer than the map R15 carried, and the denominator moves from 18 to 19 in
`.agent/plan.md`, `.agent/context.md` and every later block header.

How to reverse: delete this decision and the file
`tests/orchestration/test_bench_never_runs_implicitly.py`, and fold the pin back
into the run's round. Nothing else depends on it; the allowlist constant is
referenced by no production code by construction.
--- END SLICE DECISION-D9 ---

--- BEGIN SLICE CTXSCOPE-R16 --- (in .agent/context.md, C3 — REWRITE pair)
earlier claim that it was. Still to come, the fake-provider bench run end to
end, inventoried at R11 before it is built.
--- END SLICE CTXSCOPE-R16 ---

--- BEGIN SLICE CTXSCOPE-R16-TO --- (C3)
earlier claim that it was. R16 pinned F082's last unpinned acceptance criterion
— "the bench never runs implicitly" — as an enumerated allowlist of explicit
callers rather than as a total absence, under DECISION F082 D9, because the run
that completes the feature is itself the first legitimate caller. Still to come,
the fake-provider bench run end to end, inventoried at R11 before it is built.
--- END SLICE CTXSCOPE-R16-TO ---

--- BEGIN SLICE CTXIMPLICIT --- (in .agent/context.md, C3 — REWRITE pair)
- The bench never runs implicitly — on demand only, an F082 acceptance rule.
--- END SLICE CTXIMPLICIT ---

--- BEGIN SLICE CTXIMPLICIT-TO --- (C3)
- The bench never runs implicitly — on demand only, an F082 acceptance rule,
  pinned at R16 by `tests/orchestration/test_bench_never_runs_implicitly.py` as
  an allowlist of modules permitted to call the bench's write entry points
  (DECISION F082 D9). The allowlist is EMPTY today and gains exactly one name at
  R17. Adding to it is a deliberate act, not a repair.
--- END SLICE CTXIMPLICIT-TO ---

--- BEGIN SLICE CTXSTEPS-R16 --- (in .agent/context.md, C3 — REWRITE pair)
→ R15 record the R14 verdict, register R-0423 to R-0426 and build T003b's read
half → R16 the fake-provider run and the Q7 pin → R17 the integration gate →
R18 closure. T003 split at DECISION F082 D5, its second half inventoried at D6,
unblocked at D7 and split in two at D8, and R15 splits the read half off from
the run because they are independent deliverables; each round marks the
PREVIOUS one done and never itself.
--- END SLICE CTXSTEPS-R16 ---

--- BEGIN SLICE CTXSTEPS-R16-TO --- (C3)
→ R15 record the R14 verdict, register R-0423 to R-0426 and build T003b's read
half ✅ → R16 record the R15 verdict, register R-0427 and R-0428 and pin the Q7
criterion → R17 the fake-provider run → R18 the integration gate → R19 closure.
T003 split at DECISION F082 D5, its second half inventoried at D6, unblocked at
D7 and split in two at D8, R15 split the read half off from the run, and D9
splits the Q7 pin off from the run because a total-absence pin would not survive
the run's own driver; each round marks the PREVIOUS one done and never itself.
--- END SLICE CTXSTEPS-R16-TO ---

--- BEGIN SLICE FORTSCHRITT --- (the Fortschritt line; the handoff repeats it VERBATIM, R-0418)
Fortschritt: ~88 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b ✅ · Q7-Kriterium gepinnt · Fake-Provider-Lauf offen) — Schätzung
--- END SLICE FORTSCHRITT ---

--- BEGIN SLICE PLAN --- (WHOLE-FILE replacement of .agent/plan.md, C3)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0429. Open findings: fifty-eight — the thirty-two carried from F077, plus
R-0403 to R-0428 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R16 records the R15 gate, registers R-0427 and R-0428, and pins F082's last
unpinned acceptance criterion — "the bench never runs implicitly" — as an
allowlist of modules permitted to call the bench's write entry points, EMPTY
today, under DECISION F082 D9. It writes no production code.

## Next Steps
1. R17 — the fake-provider bench run end to end, clearing R11's Q6 four
   blockers: the missing entry point, the local-Ollama reach through
   `RunnerDeps.plan_call_fn`/`::move_call_fn`/`::execute_fn`, the
   `time.monotonic()` call in `::run_order`, and history resolving through
   `data_paths.projects_dir` to the operator's real root. It adds one name to
   the D9 allowlist and repairs R-0427's docstring in the module it touches.
2. R18 the integration gate, R19 closure.

## Risks
- The delivered order set is three, not the Design's five (R-0411). Closure may
  not quote five, and DECISION F082 D3 binds the recovery to a bench-owned
  fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the criterion whole.
- The builder's model stays unobservable: making it visible means reaching into
  `orchestrator_loop.py::execute_dispatched_job`. Closure states that absence
  rather than implying three roles were recorded.
- R17 is the largest remaining slice and the only one that runs a campaign. Its
  four blockers are named in the feature file's Q6, not rediscovered.
- Reviewer defects remain the dominant finding class. Eleven standing
  counter-measures now bind every block: R-0417 staleness, R-0418 Fortschritt,
  R-0419 grep-every-writer, R-0420 measure-the-block, R-0421 count-the-list,
  R-0422 composite-property, R-0423 measure-the-slice, R-0424
  count-your-own-contribution, R-0425 read-back-the-line-number, R-0427
  name-the-quantified-set, R-0428 re-derive-the-base-at-delegation.
--- END SLICE PLAN ---

────────────────── C2 — THE Q7 PIN, BY CONTRACT ──────────────────
CREATE `tests/orchestration/test_bench_never_runs_implicitly.py`. It is a NEW
file; touch no existing test file. Give it a module docstring saying what the
criterion is, that DECISION F082 D9 chose the allowlist form over a total
absence, and why an absence test is dangerous when it is the only guard.

Define ONE module-level constant holding the allowlist — the set of repo-relative
module paths permitted to call the bench's write entry points — and set it EMPTY,
with a comment stating that R17 adds exactly one name and that adding to it is a
deliberate act rather than a repair.

Find callers by parsing each file with `ast`, NOT by substring search: walk every
`ast.Call` node and take the called name from `ast.Name.id` or
`ast.Attribute.attr`. A `def` line, a docstring mention, an import and a comment
must NOT count as calls — that distinction is the whole reason the AST is used,
and property 4 proves the parser makes it.

Pin exactly these five properties:

 1. ANTI-VACUOUS, SYMBOLS. Both guarded names are importable and callable TODAY:
    `bench_history.append_bench_run` and `bench_dry_run.dry_run_from_order_set`.
    A rename must break this test loudly rather than empty its own search space.
 2. ANTI-VACUOUS, SCAN. The scan visits a non-zero number of `.py` files under
    each of `apps/`, `packages/` and `scripts/`, and the assertion names the real
    counts. A scanner that silently found nothing would otherwise pass forever.
 3. THE CRITERION. The set of modules under those three trees containing a CALL
    to either guarded name equals the allowlist — empty today. On failure the
    message must name the offending module and the symbol it called, because a
    bare `False` tells the next reader nothing about what to do.
 4. THE PARSER TELLS A DEF FROM A CALL. `packages/orchestration/bench_history.py`
    DEFINES `append_bench_run` and `packages/orchestration/bench_dry_run.py`
    DEFINES `dry_run_from_order_set`, and neither is reported as a caller. Pin
    this against those two real files, not against a synthetic string.
 5. NO IMPORT-TIME SIDE EFFECT. Importing both bench modules in a fresh
    subprocess whose CWD is a `tmp_path` writes no file and creates no directory
    there, and the subprocess exits 0. Running at import is the purest form of
    running implicitly, and it is the one form the caller scan cannot see.

Reuse whatever helpers the existing `tests/orchestration/` files already provide
rather than inventing new ones; read two or three of them first. The repo root
is resolved from `__file__`, never from the CWD.

────────────────────────── DONE WHEN ──────────────────────────
Run every gate. Record its REAL output. "Green" as a word is a finding.
BASE is 014996ed — re-derive it from HEAD before you start and say whether it
still equals this value (R-0428).

 1. `git status --porcelain` EMPTY at handback; `git worktree list` back to
    exactly the primary checkout. Report both verbatim.
 2. TRANSPORT AS A PROPERTY: python3 `read_bytes()` equality of
    `.agent/authored/f082-r16.md` and `.agent/last_block.md`, plus the shared
    sha256 and byte length. The reviewer measured this block at 373 lines before
    emission (R-0420). Report the REAL line count and say whether it matches; a
    mismatch is the reviewer's defect to own, not yours to fix.
 3. `.agent/STOP` — report presence at round START and at handback.
 4. C1 APPEND PROOF over the COMMITTED `<C1>^` to `<C1>`: report whether `post`
    equals `pre` + newline + GATE-R15 + blank + FINDINGS-R427-428 + blank +
    DECISION-D9 + a closing newline, BYTE-WISE, using the SAME join convention
    R15 proved: each extracted slice already carries its own trailing newline,
    so the expression is `pre + NL + GATE + NL + FINDINGS + NL + DECISION`.
    State the exact expression you evaluated. Report the C1 `--numstat`; its
    DELETION column must be 0.
 5. RECORD COUNTS in `.agent/live_review.md` at HEAD, LINE-ANCHORED only:
    `^Gate: R15 — PASS` 1 · `^- R-0427 — ` 1 · `^- R-0428 — ` 1 ·
    `^## DECISION F082 D9` 1 · `^## DECISION F082 D8` 1 · `^## DECISION F082 D7`
    1 · `^Landed: ` 0 · `^Done: ` 0. Report each real number. No unanchored
    substring count is ordered this round (R-0424).
 6. OPEN SET RECOMPUTED MECHANICALLY: every `^- R-\d+ — ` paragraph minus every
    `^Done: R-\d+ — ` line. Report the count, max id, next free id and any
    duplicate. R16 registers exactly two, so the expected count is FIFTY-EIGHT
    and the next free id becomes R-0429 — report the real numbers regardless.
 7. C3 CONTEXT AS ONE COMPOSITE over the COMMITTED `<C3>^` to `<C3>` (R-0422:
    three pairs share `.agent/context.md`, so per-pair whole-file equality is
    unreachable and is NOT ordered). Report `pre` with ALL THREE replacements
    applied `== post`; per pair report FROM 1x to 0x, TO 0x to 1x and
    `FROM in TO`. The reviewer measured all three FROMs at 1x against the disk
    before emission; report the real values.
 8. C2 IS A NEW FILE AND THE ONLY TEST TOUCHED. Report `git diff --name-only`
    for the range restricted to `tests/` — it must name exactly
    `tests/orchestration/test_bench_never_runs_implicitly.py`. Report that
    file's C2 `--numstat`; its DELETION column must be 0 because the file is
    new. Report its `^def test_` count.
 9. RED-PROOF, ISOLATED (G5). In a DISPOSABLE `git worktree` under `.remedy-wt/`
    — never in the primary checkout — add a single line to a scratch module
    under `packages/` that CALLS `append_bench_run`, then run the new pin test
    there. Report the COLOUR: it MUST fail, and report which test function
    failed and the first line of its assertion message. Do NOT report a passed
    or failed COUNT as the proof (R-0327). Then remove the worktree and show
    `git worktree list` back to one line. A pin that cannot be made red has not
    been shown to guard anything.
10. `.agent/plan.md` at HEAD BYTE-EQUALS the PLAN slice as a WHOLE FILE. Report
    its sha256 and `wc -l`; it must be UNDER 50 (the reviewer measured the slice
    at 48 lines; report the real number), and it keeps `## Goal` and `## Next
    Steps`. Report `wc -l` for `.agent/context.md` and its contract readers:
    `## Active Branch` then a `feature/` slug · substring `Steps` · a roadmap
    F-id · `pytest` or `resource`.
11. CHANGE SET: `git diff --name-only 014996ed..HEAD` — report every path, COUNT
    them, and state whether you measured before or after C4. The Change list is
    a CEILING. `git diff --name-only 014996ed..HEAD -- docs/ apps/ packages/
    scripts/` MUST be EMPTY — this round writes no production code, and that
    restriction is the proof.
12. THE GUARDED TREES ARE UNTOUCHED, so the pin is measured against the same
    repository the reviewer measured. Report `git diff --name-only 014996ed..HEAD`
    restricted to the gauntlet seven (`tests/orchestration/test_gauntlet_*.py`
    plus `tests/orchestration/test_self_run_gauntlet.py`) and to the
    pre-existing bench five (`tests/orchestration/test_bench_dry_run.py`,
    `test_bench_history.py`, `test_bench_orders.py`, `test_capability_bench.py`,
    `tests/cli/test_stats_bench.py`) — both MUST be EMPTY.
13. `python3 -m pytest tests/orchestration/test_bench_never_runs_implicitly.py -q`
    → exit 0. This file is new, so no BASE exists; report the real number and
    make no prediction (R-0336).
14. STILL GREEN, run each set together: the gauntlet seven — reviewer's BASE
    measurement `276 passed` — and the pre-existing bench five — BASE
    `61 passed`. Report both real numbers and both exit codes.
15. `python3 -m pytest tests/orchestration/test_bench_model_context.py -q` →
    exit 0. Reviewer's BASE measurement `14 passed`.
16. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer's BASE
    measurement: 184 passed.
17. `python3 -m ruff check tests/orchestration/test_bench_never_runs_implicitly.py`
    → exit 0. The reviewer ran scoped ruff over the bench files at BASE and it
    was `All checks passed!`, so a red result here is THIS round's doing.
    Repository-wide ruff is red on main and is NOT gated (R-0364).
18. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`, `handler_import` message `handlers=337`.
19. `gh pr list --state open --json number,headRefName` → report verbatim. Must
    be `[]`. Create NO pull request.
20. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it with the inseparability reason BEFORE review. C4
    cannot state its own numstat; report it in the completion report.
21. STANDING STALENESS GATE (R-0417, eighth run). Re-read every sentence in the
    files this round touched that states a COUNT, a module list, a
    round-to-step map, or a completion claim, and report for each whether it
    still holds at HEAD. Repair ONLY what the ordered slices cover; report
    everything else and leave it. State how many sentences you checked. Known
    open items to re-check rather than repair: `.agent/context.md` still names
    240 as the preferred block target; `packages/orchestration/bench_history.py`
    lines 16–18 carry the R-0427 sentence, which R17 repairs and this round
    MUST NOT touch — that file is outside the Change ceiling.
The docs-round gate does NOT bind; gate 11 proves `docs/**` is untouched.
BLOCK-SIZE DECLARATION (R-0420): 373 lines, under the 400 cap (DECISION F105 D5)
and OVER the 240 preference, because one verdict line, two findings, a decision
and a five-property contract cannot be carried in less. C0a's insertions stay
inside the 500 limit.

Handback:    Completion report + rewrite `.agent/handoff.md` per
             docs/agents/handback_template.md: feature and round, branch,
             per-commit changed-files tables, the real verification values
             above, an item-status table with every C0a–C4 item and every gate
             1–21 exactly once, open-findings count, next expected action.
             Declare every deviation with its cause. Repeat the FORTSCHRITT
             slice VERBATIM (R-0418). Push after every commit. Create NO PR.
             THE NEXT SESSION'S FIRST ACTION is self_drive_protocol.md Phase 1
             rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR
             Gate; say so in the Next section. F082 is MID-FEATURE and no PR
             exists. The next round is R17, the fake-provider run, which also
             adds one name to the D9 allowlist and repairs R-0427.
──────────────────────────────────────────────────────────────────────────────
