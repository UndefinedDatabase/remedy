── STEP R17-VERDICT — F082 Self-benchmark ────────────────────────────────────
Goal:        Persist the R17 verdict and its three findings to the review record
             before this session ends. This is the C1 half of the next round,
             pulled forward so the reviewer's findings reach disk rather than
             dying with the session (self_drive_protocol.md: the handoff is the
             only return channel).

Bundle:      C0 save this block · C1 GATE-R17 + FINDINGS-R431-433 appended to
             `.agent/live_review.md` · C2 handoff Next-section update.

Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r17-verdict.md   (C0, new)
             - .agent/live_review.md                 (C1 append)
             - .agent/handoff.md                     (C2, one pair)
             NOT in scope: every other file in the repository. This round writes
             NO code, NO test and NO plan/context change — gate 5 proves it.

Constraints:
 1. R18 IS NOT STARTED HERE. This round only records. The integration gate
    remains R18's whole deliverable and nothing here anticipates it.
 2. `.agent/last_block.md` IS NOT TOUCHED. It holds the R17 block, which is the
    block the recorded verdict is about; overwriting it would destroy the
    subject of the record.
 3. Apply both slices DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r17-verdict.md`. No `--- BEGIN SLICE` / `--- END
    SLICE` marker line may reach any target file, and no target gains a
    trailing-whitespace line.
 4. Apply every slice VERBATIM. If a slice is wrong on arrival, apply it as
    ordered and DECLARE it (R-0419).
 5. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    No commit trailer. Push after every commit. Create NO PR.
 6. Prior gate entries and DECISIONS D1-D9 ARE NOT REWRITTEN. This appends.

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE GATE-R17 --- (append to .agent/live_review.md, C1, ONE physical line)
Gate: R17 — PASS, with three new findings, ALL THREE the reviewer's own defects in the block it authored, and two of the three found by the worker and declared before the reviewer read the diff. Verification tier: round gate plus the canary; the round added a production module, so every suite reaching it was re-run and the additive claim is measured rather than argued. All twenty-two ordered gates were re-executed by the REVIEWER against the disk rather than read out of the handback, and every reported value reproduces. Transport is proven at the strongest level this protocol allows: the committed `.agent/authored/f082-r17.md`, `.agent/last_block.md` AND the reviewer's own pre-delegation original under `.remedy-wt/` are all three byte-identical under python3 `read_bytes()`, sha256 `990fa83f927e9a575533bffc36ca0eac5ed7e5b40ebf76c0d1889b3632ed4ba5`, 33591 bytes, 399 lines — matching the count declared before emission, so R-0420's rule held for a fourth consecutive round, and the base was re-derived at delegation time per R-0428 and still equalled `c044cb18`. The C1 append is a PROPERTY: over the committed `983a897c^` to `983a897c`, `post` equals `pre + NL + GATE-R16 + NL + FINDINGS-R429-430` byte-wise, TRUE, `pre` a prefix, the added region 8564 bytes, deletion column 0. Record counts at HEAD, line-anchored: `^Gate: R16 — PASS` 1, `^- R-0429 — ` 1, `^- R-0430 — ` 1, `^## DECISION F082 D9` 1, `^Landed: ` 0, `^Done: ` 0; the open set recomputed mechanically is SIXTY with no duplicate, max R-0430, next free R-0431. C6's context edit holds as ONE composite with all three pairs at FROM 1x to 0x and `FROM in TO` False; `.agent/plan.md` byte-equals the PLAN slice whole-file at sha256 `d5a5ffb8eac253fe310b8cc0abfbe5a804a6eecc75103017cea920c5d20dd141`, 47 lines, under the fifty-line cap. C4 and C5 each hold as `pre.replace(FROM, TO) == post`. Marker lines reaching any target: 0. Trailing-whitespace lines gained: 0, checked across all seven touched files. The change set is ten paths, every one inside the Change ceiling, with `docs/`, `apps/`, `scripts/` and all five gauntlet modules EMPTY — the additive constraint measured rather than asserted. Suites re-run by the reviewer at the branch head: the new `test_bench_run.py` `7 passed` exit 0; the pin `6 passed` exit 0, unchanged by its one new allowlist name; the gauntlet seven `276 passed` and the pre-existing bench five `61 passed`, both exit 0 and both UNCHANGED from base; `test_bench_model_context.py` `14 passed`; the canary plus three contract readers `184 passed`; scoped `ruff check` `All checks passed!`; `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with `handler_import` still `handlers=337`, confirming no CLI handler key was added. Insertions per commit are 399, 327, 6, 86, 264, 6, 5, 29 and 166, none over 500. `git status --porcelain` empty, `git worktree list` the single primary checkout, `.agent/STOP` absent, `gh pr list --state open` `[]`. The RED-PROOF was re-run by the reviewer in its own disposable worktree: deleting the ONE allowlisted name while leaving `bench_run.py` in place turned the pin RED, failing `test_only_allowlisted_modules_call_the_bench_write_entry_points` with a message naming `packages/orchestration/bench_run.py` as calling BOTH `append_bench_run` and `dry_run_from_order_set` — which incidentally proves Constraint 6's premise that the one name is legitimate, since an allowlisted module calling nothing would fail the same test's other branch. The reviewer then went PAST the ordered gates (R-0220): the gate list proved only ONE direction of the pin's equality, so the reviewer probed the other by adding an allowlist entry for a module that calls nothing, and the pin went RED there too with "Allowlisted modules that call nothing". The criterion is therefore a genuine EQUALITY and not a one-sided containment — an over-broad allowlist is caught as loudly as a missing one, which is what makes the D9 form safe to carry to closure. Both probes were confirmed by `pwd` and `git rev-parse --show-toplevel` to have run inside the worktree (R-0337), and the worktree was removed with the list back to one line. On substance the round is sound: `bench_run.py` is 86 lines that do exactly the four ordered steps in order, hold no fake, no clock and no test-only branch, and make both roots REQUIRED keyword arguments so R11 Q6's fourth blocker is closed by construction rather than by convention; `test_bench_run.py` drives the REAL frozen order set through nine doubled seams and carries an anti-vacuous guard the contract never asked for, asserting the mission double actually ran before concluding that nothing escaped `tmp_path` — without it that property would pass over a run that never happened. R-0427 is REPAIRED on disk by C5, which now names the GAUNTLET set it quantifies over and states that `BenchRecord` did change. The worker declared five deviations, applied every defective slice verbatim as Constraint 8 requires rather than silently repairing it, and reported three stale sentences it was forbidden to touch — conduct that converted three reviewer defects into findings instead of into silent corrections. No block condition was hit: no fabricated data, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R17 ---

--- BEGIN SLICE FINDINGS-R431-433 --- (append to .agent/live_review.md, C1, after GATE-R17, one blank line between the gate and this slice)
- R-0431 — Low, REVIEWER-SLICE DEFECT, THREE FAULTS IN ONE REWRITE PAIR, two of them declared by the worker as deviations D2 and D3 before the reviewer read the diff and the third found by the reviewer reading the applied result. The R17 block's `CTXIMPLICIT-R17` pair rewrote only the TAIL of a `.agent/context.md` bullet, and the bullet's surviving head still says "The allowlist is EMPTY today and gains exactly one name at R17" while the new tail says "R17, which spent it on `packages/orchestration/bench_run.py`" — so one sentence now asserts the allowlist is empty and that it has been spent, and both halves were authored by the same reviewer in the same round. The pair also had two mechanical faults: its TO slice's second line carries no two-space continuation indent, so `deliberate act, not a repair.` sits at column 0 and dedents out of the `- ` bullet it belongs to, and the `CTXSCOPE-R17-TO` slice's first line joins an existing sentence tail to produce a 94-character line inside a paragraph wrapped at about 79. Low, because nothing executable reads `.agent/context.md` and all three faults are text. The CAUSE is one habit and worth naming once: a REWRITE pair was scoped to the smallest span that made the new claim true, instead of to the span whose MEANING the new claim changes. The reviewer measured the FROM at 1x, confirmed `FROM in TO` was False and confirmed the composite reproduced — every ordered property passed — and none of those properties can see that the sentence CONTAINING the replaced tail now contradicts itself, because they compare bytes and not claims. Standing rule from here, binding the reviewer: a REWRITE pair extends to the whole sentence, bullet or paragraph whose truth value the edit changes, never to the minimal matching span; and a TO slice landing inside an indented block reproduces that block's continuation indent and wrap width, because a slice is applied into a shape it cannot see. R18 repairs the bullet whole.

- R-0432 — Low, A CONSTRAINT FROZE THE FILE THE ROUND ITSELF MADE STALE, found by the worker under the standing staleness gate, reported and correctly NOT repaired, then confirmed by the reviewer by reading the file. The R17 block's Constraint 6 said the allowlist gains exactly one name and "Touch no other line of the pin file", and gate 22 said to repair only what the ordered slices cover. Both were obeyed exactly. The consequence is that `tests/orchestration/test_bench_never_runs_implicitly.py` now carries three sentences that were true when R16 wrote them and are false at HEAD: the module docstring's "which is empty today and gains exactly one name at R17" at line 13, the allowlist constant's "EMPTY today, which is a measured fact and not an assumption" at line 63, and the section header "callers equal the allowlist, which is empty today" at line 180. A fourth, the `MIN_SCANNED_FILES` comment "File counts measured at R16 against this repository: apps 73, packages 256, scripts 29", is NOT a defect and is deliberately left: it is explicitly time-stamped to R16, so it remains true as history, and the observed count is now packages 257 exactly as the block predicted. Low, because the code is correct and only its prose lies. The CAUSE is structural rather than careless: a block that changes a file's state MUST carry the repair for that file's own description of its state, and a "touch nothing else" constraint written to protect a pin from drive-by edits also forbade the one edit the round made necessary. Standing rule from here: when a block spends a value a file describes in its own prose, the same block carries the pair that updates that prose; a freeze constraint names the lines it freezes rather than the whole file. R18 repairs all three sentences.

- R-0433 — Low, AN ENUMERATION MEANT AS A CALL LIST WAS READ AS AN IMPORT WHITELIST, declared by the worker as deviation D1 and confirmed by the reviewer. The R17 block's Constraint 1 said `bench_run.py` "is NEW and only IMPORTS `run_campaign`, `RunnerDeps`, `load_bench_order_set`, `dry_run_from_order_set` and `append_bench_run`", intending to describe the product verbs the join calls and to forbid reaching into anything else. The worker read "only IMPORTS ... " as exhaustive, which is what it literally says, and therefore could not import `gauntlet_runner.OrderOutcome` or `capability_bench.BenchRecord` for the return type — so `BenchRunResult.outcomes` and `.rows` are typed `tuple[Any, ...]` with the concrete types named only in field comments. The worker chose obedience over silent widening, which Constraint 8 demands and which is the correct call; the defect is the constraint's wording, not the reading. Low, because the runtime behaviour is identical and the types are documented one line away. The CAUSE is that a scope fence and a type-import are different things and the sentence conflated them: forbidding a module to CALL new product surface is a real constraint, forbidding it to NAME a type it already returns is an accident. Standing rule from here: a constraint enumerating imports says what the list is FOR — the product verbs this module may call — and states explicitly that importing a type for a signature is not a call. R18 restores the concrete annotations.
--- END SLICE FINDINGS-R431-433 ---

--- BEGIN SLICE HANDOFFNEXT --- (in .agent/handoff.md, C2 — REWRITE pair)
## Next

Review R17 over c044cb18..HEAD, then R18 — the integration gate. THE NEXT
--- END SLICE HANDOFFNEXT ---

--- BEGIN SLICE HANDOFFNEXT-TO --- (C2)
## Reviewer verdict — recorded after this handback was written

R17 is PASS. The reviewer re-executed all twenty-two gates against the disk and
every value reproduced; the verdict line and three findings, R-0431 to R-0433,
are appended to `.agent/live_review.md`. All three are the REVIEWER's own block
defects, two of them the deviations declared above. Open findings are now
SIXTY-THREE, max R-0433, next free R-0434.

## Next

R18 — the integration gate, which also repairs R-0431, R-0432 and R-0433 and is
the round that measures the Goal's three DONE conditions together. THE NEXT
--- END SLICE HANDOFFNEXT-TO ---

────────────────────────── DONE WHEN ──────────────────────────
Run every gate. Record its REAL output. "Green" as a word is a finding.
BASE is b9dbca9b — re-derive it from HEAD before you start and say whether it
still equals this value (R-0428).

 1. `git status --porcelain` EMPTY at handback; `git worktree list` exactly the
    primary checkout. Report both verbatim.
 2. TRANSPORT: python3 `read_bytes()` equality of
    `.agent/authored/f082-r17-verdict.md` against
    `.remedy-wt/f082-r17-verdict.md`, plus the shared sha256, byte length and
    REAL line count. `.agent/last_block.md` is NOT part of this round.
 3. C1 APPEND PROOF over the COMMITTED `<C1>^` to `<C1>`: report whether `post`
    equals `pre + NL + GATE-R17 + NL + FINDINGS-R431-433` BYTE-WISE, using the
    join convention prior rounds proved — each extracted slice already carries
    its own trailing newline. State the exact expression. Report the C1
    `--numstat`; its DELETION column must be 0.
 4. RECORD COUNTS in `.agent/live_review.md` at HEAD, LINE-ANCHORED only:
    `^Gate: R17 — PASS` 1 · `^- R-0431 — ` 1 · `^- R-0432 — ` 1 ·
    `^- R-0433 — ` 1 · `^Landed: ` 0 · `^Done: ` 0. Report each real number.
 5. OPEN SET RECOMPUTED MECHANICALLY: every `^- R-\d+ — ` paragraph minus every
    `^Done: R-\d+ — ` line. Report count, max id, next free id, duplicates.
    This round registers exactly three, so expect SIXTY-THREE and next free
    R-0434 — report the real numbers regardless. Also report
    `git diff --name-only b9dbca9b..HEAD` in full: it must name exactly the
    three files in the Change list and nothing else.
 6. C2 PAIR: report `pre.replace(FROM, TO) == post` over the COMMITTED `<C2>^`
    to `<C2>`, and FROM 1x in `pre`, 0x in `post`. NOTE: `## Next` occurs in
    `.agent/handoff.md` — if it occurs more than once, STOP and report it
    rather than applying a replacement that would hit the wrong one.
 7. `python3 -m pytest tests/orchestration/test_bench_run.py
    tests/orchestration/test_bench_never_runs_implicitly.py -q` → exit 0.
    Reviewer's BASE measurement: 7 passed and 6 passed, 13 together.
 8. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`, `handler_import` `handlers=337`.
 9. `gh pr list --state open --json number,headRefName` → verbatim, must be
    `[]`. Create NO pull request.
10. Report each commit's insertion total. None may exceed 500.
Marker lines reaching any target: report the count, which must be 0. Trailing-
whitespace lines gained in any target: report the count, which must be 0.
BLOCK-SIZE DECLARATION (R-0420): 121 lines, under the 400 cap (DECISION F105 D5).

Handback:    Rewrite `.agent/handoff.md`'s verification and item-status content
             ONLY as far as the C2 pair specifies — this round does NOT rewrite
             the whole handoff, because the R17 handback it contains is the
             record of the round being certified. Report the ten gate values in
             your completion report instead. If the handoff's line count moves,
             say so and name the new numeral (R-0430). Push after every commit.
             Create NO PR. THE NEXT SESSION'S FIRST ACTION is
             self_drive_protocol.md Phase 1 rule 1 — re-read `.agent/STOP` from
             disk — BEFORE rule 2's Open PR Gate. F082 is MID-FEATURE, no PR
             exists, and the next round is R18, the integration gate, which also
             repairs R-0431, R-0432 and R-0433.
──────────────────────────────────────────────────────────────────────────────
