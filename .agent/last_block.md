── STEP R12/15 — F082 Self-benchmark ─────────────────────────────────────────
Goal:        Record the R11 verdict, register R-0419 against the reviewer, make
             the record TRUE where R11's inventory proved it false, and rule on
             the one question the inventory opened but could not answer: whether
             T003b may add a key to a gauntlet module at all.
Bundle:      C0a save this block · C0b mirror it · C1 GATE-R11 + FINDING-R419 +
             DECISION-D7 appended to the review record · C2 plan and step-map
             re-sync · C3 handback.
Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r12.md   (C0a, new)
             - .agent/last_block.md          (C0b)
             - .agent/live_review.md         (C1 append)
             - .agent/plan.md                (C2 whole-file)
             - .agent/context.md             (C2 CTXSTEPS3 pair)
             - .agent/handoff.md             (C3)
             NOT in scope: `apps/**`, `packages/**`, `tests/**`,
             `docs/roadmap/**`. This round writes no code, no test and no doc.
             `git diff --name-only <BASE>..HEAD -- apps/ packages/ tests/ docs/`
             must be EMPTY.

Constraints:
 1. DECISION F082 D6 IS NOT REWRITTEN. It is a time-stamped historical record
    and this branch does not edit those in place; the same rule that leaves
    superseded gate entries standing. D7 supersedes its factual clause and
    says so in its own text. The correction is APPENDED, never retro-fitted —
    a reader who lands on D6 must be able to find D7, which is why D7 names D6
    explicitly in its first line.
 2. `.agent/plan.md` IS NOT HISTORY. It is a live mirror and it must be TRUE
    at every commit, so its three false risk sentences are replaced wholesale
    by the PLAN slice below. That asymmetry — history appended, mirrors
    corrected — is the whole of this round's editing policy.
 3. NO NUMERAL WITHOUT A COUNT. The PLAN slice deliberately states no count of
    reviewer-block defects, because the previous plan's "seven of the last
    nine" was arithmetic nobody had done. If a later text wants that number it
    counts it mechanically first (R-0402, R-0404 class).
 4. `.agent/plan.md` stays under 50 lines and keeps `## Goal` and
    `## Next Steps`. `.agent/context.md` keeps `## Active Branch` with its
    `feature/` slug, the substring `Steps`, a roadmap F-id, and `pytest` or
    `resource`.
 5. Apply every slice DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r12.md`, never by retyping and never from the prompt
    after C0a. No `--- BEGIN SLICE` / `--- END SLICE` marker line may reach any
    target file. No target file gains a trailing-whitespace line.
 6. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    Insertions per commit stay under 500. No commit trailer.

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE GATE-R11 --- (append to .agent/live_review.md, C1, ONE physical line)
Gate: R11 — PASS, with one new finding, the reviewer's again. Verification tier: round gate plus the docs-round gate plus the canary; no full-suite claim is made and none is owed. All seventeen ordered gates were re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces at its reported value. Transport is proven at PRIMARY strength: the scratchpad `.remedy-wt/f082-r11-scratchpad.md`, `.agent/authored/f082-r11.md` and `.agent/last_block.md` are byte-identical at shared sha256 `5e59957b1d87982ddb4d2eb542e244c4e88794bfe39ef38362b6ab30b918a060`, 25835 bytes and 308 lines, and that digest equals the one the reviewer ordered in the delegation, so the block that ran is provably the block that was authored. The C1 append is a PROPERTY: `post == pre + add` holds byte-wise over the committed `7dd4f605^`→`7dd4f605` where `add` is GATE-R10, FINDING-R418 and DECISION-D6 joined as committed, the 174-line pre-file is an exact prefix of the 213-line result, and the numstat is `39 0` with the deletion column zero. Both context pairs re-proven as properties over their own committed revisions, each a REWRITE with its FROM going 1x to 0x and its TO landing 1x; `.agent/plan.md` byte-equals the PLAN slice as a whole file at 42 lines; `.agent/context.md` keeps every contract reader at 67 lines. The record counts are `^Gate: R10 — PASS` 1, `^- R-0418 — ` 1, `^## DECISION F082 D6` 1, `^Landed: ` 0 and `^Done: ` 0; the open set recomputed mechanically is FORTY-EIGHT with no duplicate, max R-0418 and next free R-0419. The change set is seven paths, every one inside the block's Change list, and `git diff --name-only 9f2ab66d..HEAD -- apps/ packages/ tests/` is EMPTY, which is the promise an inventory round exists to keep. Suites re-run by the reviewer at the branch head: `tests/docs/` `295 passed`, the canary plus the three contract readers `184 passed`, `tests/cli/test_stats_bench.py` `25 passed` so R10's work still stands untouched, and `integrity check --json` `passed: true`, `fail_count: 0` over 5 checks with `handlers=337` unchanged, proving this round touched no registration. Insertions per commit are 308, 242, 39, 6, 144, 23 and 118, none over 500, and `gh pr list --state open` is `[]`. C3 was verified as a PURE APPEND into the feature file — `post.startswith(pre)` is TRUE — and `## Built State` provably did not exist at 9f2ab66d, so the worker's declared deviation is exactly what the disk shows and the section it created touches none of the sections Constraint 4 protects. The inventory itself is the deliverable and the reviewer spot-checked it rather than accepting it: Q1's claim that THREE roles bind a model is true — `ollama_planner/provider.py::_resolve_model` and `ollama_builder/provider.py::_resolve_model` are two more bindings beside the orchestrator's config read, and `role_config.py::KNOWN_ROLES` is a seven-role table whose `_FIELDS` include `model`; Q7's claim that "the bench never runs implicitly" is UNPINNED is true, since `append_bench_run` and `dry_run_from_order_set` have no caller anywhere under `apps/`, `packages/` or `scripts/`, so the criterion holds today by absence and no test would notice if it stopped holding; Q7's other half is pinned exactly where it says, at `test_bench_orders.py::test_editing_an_order_without_bumping_its_version_fails_validation`; and Q4's correction to the reviewer is upheld — `docs/roadmap/features/T2_F082.md`'s Do-not-touch section names the gauntlet's pass definition, routing decisions and visual judgment, which are BEHAVIOURS, and does not name `gauntlet_runner.py` as a file at all. The round's most valuable act was refusing to silently repair the reviewer: Constraint 7 ordered verbatim application, two ordered slices were false on arrival, and the worker applied them as ordered and declared them rather than correcting them in place — which is correct twice over, because a worker that had "fixed" them would have broken the byte-equality gates that make transport provable, and the fabrication would have been invisible. That is finding R-0419, and it charges the reviewer. No block condition was hit — no fabricated data by the worker, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R11 ---

--- BEGIN SLICE FINDING-R419 --- (append to .agent/live_review.md, C1, after GATE-R11, blank line between)
- R-0419 — Medium, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer against the code. The R11 block asserted a fact about this repository that a wider grep refutes: DECISION-D6 states the reviewer "found exactly one role bound to a model — `orchestrator.model`", and the PLAN slice repeated it as "only one role is bound to a model". Both are FALSE. `packages/providers/ollama_planner/provider.py::_resolve_model` and `packages/providers/ollama_builder/provider.py::_resolve_model` each bind a second and third role to a model, and `packages/orchestration/role_config.py::KNOWN_ROLES` is a seven-name table whose resolvable `_FIELDS` include `model`. The cause is precise and worth naming rather than generalising: the reviewer grepped ONE file, `gauntlet_runner.py`, and wrote the result as a property of the whole repository. That is the R-0391 class — "an invariant is not established by the first file you look in; grep every writer before authoring a claim against it" — recurring here in its authored-block form rather than its finding form. The claim was also load-bearing, which is what makes this Medium rather than Low: the scarcity of role→model bindings was the stated reason DECISION F082 D6 inserted an inventory round, so a false fact was carrying a real planning decision. The decision survives its bad reason — the inventory was worth running, and it is precisely what caught this — but the reason is corrected in DECISION F082 D7 rather than left standing. Standing rule from here, binding the reviewer: a block may state a repository-wide absence ("nothing does X", "only one Y exists") only after a repository-wide search, and the block names the search it ran. An absence claimed from a single file is an unrun claim.
--- END SLICE FINDING-R419 ---

--- BEGIN SLICE DECISION-D7 --- (append to .agent/live_review.md, C1, after FINDING-R419, blank line between)
## DECISION F082 D7 — T003b may add one key to the gauntlet's evidence body

This decision SUPERSEDES the factual clause of DECISION F082 D6 (that clause
is corrected by finding R-0419, not deleted; D6 stands as the record of why
R11 ran) and rules on the question R11's inventory opened but could not close.

The inventory's finding: recording "which models served which roles" is
answer (c) — not recordable today without a change to a gauntlet module. A
gauntlet `run.json` carries no model identity at all
(`gauntlet_runner.py::_evidence_body`, sixteen keys, none a model), and the
token ledger's `model` column cannot be joined to a bench row because the only
run-time writer of that ledger is off the gauntlet path and `run.json` carries
no correlating id.

Chosen: T003b MAY add a `models` key to `gauntlet_runner.py::_evidence_body`,
as a SECOND declared exception to the ADDITIVE constraint R2's inventory set,
on three conditions. First, the key is ADDITIVE — no existing key changes
name, type or meaning, so every existing reader keeps working. Second, the
gauntlet's own seven test files stay green UNMODIFIED; if any needs an edit,
the change is not additive and the round stops. Third, an absent binding is
recorded as absent, never as a default model name — an invented model is
precisely the class of lie F082 exists to prevent, and the same reason
`repair_rounds` is `None` rather than 0.

Why this is allowed at all: `gauntlet_runner.py` is NOT on F082's Do-not-touch
list. That list names the gauntlet's pass definition, routing decisions and
visual judgment — behaviours, not files — and this change decides no pass and
routes nothing; it records what already happened. DECISION F082 D1 already
excepted this same module once, at `::measure_tokens`, which makes this the
second exception and not the first. That D1 exists is also the reason this
needs a decision rather than a shrug: the ADDITIVE constraint is real, and a
second exception granted silently would retire it by attrition.

Alternatives considered: (a) a run-level header row in the bench history
carrying the models — rejected, the bench would be recording what it did not
observe, since the models are the gauntlet's and the bench only reads its
evidence; (b) drop model-context recording from F082 — rejected for the reason
D6 gave, it is an explicit Design bullet with named downstream consumers; (c)
join through the token ledger — rejected, the inventory showed the join key
does not exist.

How to reverse: delete this decision and T003b records no model context; the
feature then closes with a Design bullet unbuilt and an assumption_log entry
saying so, which is a worse but legitimate outcome.
--- END SLICE DECISION-D7 ---

--- BEGIN SLICE CTXSTEPS3-FROM --- (in .agent/context.md, C2 — REWRITE pair)
stale claim ✅ → R10 T003a the stats bench read view ✅ → R11 record the R10
verdict and answer the T003b inventory → R12 T003b model context and a
fake-provider run → R13 the integration gate → R14 closure. T003 split at
DECISION F082 D5 and its second half inventoried first at D6; each round marks
the PREVIOUS one done and never itself.
--- END SLICE CTXSTEPS3-FROM ---

--- BEGIN SLICE CTXSTEPS3-TO --- (C2)
stale claim ✅ → R10 T003a the stats bench read view ✅ → R11 the T003b
inventory ✅ → R12 record the R11 verdict, register R-0419 and rule on the
gauntlet key at D7 → R13 T003b model context and a fake-provider run → R14 the
integration gate → R15 closure. T003 split at DECISION F082 D5, its second half
inventoried at D6 and unblocked at D7; each round marks the PREVIOUS one done
and never itself.
--- END SLICE CTXSTEPS3-TO ---

--- BEGIN SLICE FORTSCHRITT --- (the Fortschritt line; the handoff repeats it VERBATIM, R-0418)
Fortschritt: ~78 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b inventoriert und entsperrt, nicht gebaut) — Schätzung
--- END SLICE FORTSCHRITT ---

--- BEGIN SLICE PLAN --- (WHOLE-FILE replacement of .agent/plan.md, C2)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0420. Open findings: forty-nine — the thirty-two carried from F077, plus
R-0403 to R-0419 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R12 records the R11 gate, registers the reviewer-block defect R-0419, corrects
the false role-binding claim this file itself carried, and rules at DECISION
F082 D7 that T003b may add one additive `models` key to the gauntlet's evidence
body. It writes no code.

## Next Steps
1. R13 — T003b: the `models` key on `gauntlet_runner.py::_evidence_body` under
   D7's three conditions, model context carried into the bench record, and a
   fake-provider bench run end to end. R11's Q6 names four blockers for that
   run — no entry point, local-Ollama reach, a `time.monotonic()` call in
   `::run_order`, and history resolving to the real data root — and the round
   must clear or route around each before claiming an end-to-end run.
2. R14 the integration gate, R15 closure.

## Risks
- "The bench never runs implicitly" is an ACCEPTANCE criterion that NO test
  pins (R11 Q7). It holds today only by absence: `append_bench_run` and
  `dry_run_from_order_set` have no caller under `apps/`, `packages/` or
  `scripts/`. An unpinned criterion found at closure is a closure blocker, so
  R13 or R14 pins it.
- T003b needs the D7 exception to the ADDITIVE constraint. If the gauntlet's
  seven test files cannot stay green unmodified, the change is not additive
  and the round stops rather than widening.
- The delivered order set is three, not the Design's five (R-0411). Closure
  may not quote five, and DECISION F082 D3 binds the recovery to a
  bench-owned fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the acceptance criterion whole.
- Reviewer-block defects, not worker defects, are the dominant finding class on
  this branch. No count is stated here because none has been taken; R-0417's
  staleness gate, R-0418's Fortschritt rule and R-0419's grep-every-writer
  rule are the counter-measures, and all three bind every block from here.
--- END SLICE PLAN ---

────────────────────────── DONE WHEN ──────────────────────────
Run every gate. Record its REAL output. "Green" as a word is a finding.
BASE is the SHA this round starts from: e6c18d89.

 1. `git status --porcelain` EMPTY at handback; `git worktree list` back to
    exactly the primary checkout. Report both verbatim.
 2. TRANSPORT AS A PROPERTY: sha256 and byte length of
    `.remedy-wt/f082-r12-scratchpad.md`, `.agent/authored/f082-r12.md` and
    `.agent/last_block.md`. All three EQUAL. `cp`/`cmp` are denied to this
    session class (R-0408) — use `sha256sum` plus a python3 `read_bytes()`
    equality. Report the shared digest and the line count; ≤ 400.
 3. `.agent/STOP` — report presence at round START and at handback. Absent
    both times. If it appears, finish the current commit and hand off.
 4. C1 APPEND PROOF: over the COMMITTED `<C1>^` and `<C1>`, report whether
    `post == pre + add` holds BYTE-WISE, where `add` is GATE-R11,
    FINDING-R419 and DECISION-D7 joined exactly as committed. Report the C1
    `--numstat`; its DELETION column must be 0.
 5. RECORD COUNTS in `.agent/live_review.md` at HEAD: `^Gate: R11 — PASS` 1 ·
    `^- R-0419 — ` 1 · `^## DECISION F082 D7` 1 · `^## DECISION F082 D6` 1
    (still there — D6 is history and is NOT rewritten) · `^Landed: ` 0 ·
    `^Done: ` 0. Report each real number.
 6. OPEN SET RECOMPUTED MECHANICALLY: every `^- R-\d+ — ` paragraph minus
    every `^Done: R-\d+ — ` line. Report the count, the max id, the next free
    id, and any duplicate. R12 registers exactly one finding, R-0419, so the
    expected count is FORTY-NINE and the next free id becomes R-0420 — report
    the real numbers whatever they are.
 7. CTXSTEPS3 PAIR AS A PROPERTY: report whether
    `post == pre.replace(CTXSTEPS3_FROM, CTXSTEPS3_TO)` holds byte-wise over
    the committed C2. REWRITE: FROM 1x before and 0x after, TO 1x after.
 8. `.agent/plan.md` at HEAD BYTE-EQUALS the PLAN slice as a WHOLE FILE.
    Report its sha256 and `wc -l`; under 50. Report `wc -l` for
    `.agent/context.md`. Contract readers of `.agent/context.md`:
    `## Active Branch` followed by a `feature/` slug · substring `Steps` ·
    a roadmap F-id · `pytest` or `resource`. Plan keeps `## Goal` and
    `## Next Steps`.
 9. THE CORRECTION LANDED WHERE IT WAS OWED, AND ONLY THERE.
    (a) Count `only one role is bound to a model` in `.agent/plan.md`: it must
        be 0 at HEAD. The mirror is corrected.
    (b) Count `found exactly one role bound to a model` in
        `.agent/live_review.md`: it must be exactly 2, and BOTH sites are
        expected. One is inside DECISION F082 D6, where it is history and
        Constraint 1 forbids rewriting it; the other is inside FINDING-R419,
        which QUOTES the false clause on purpose so a reader of the finding
        sees exactly what was wrong. A 1 here would mean either the finding
        dropped its quote or history was edited — report which.
    Both numbers are the point of this round: the mirror goes to 0, the record
    goes to 2, and neither file is edited the way the other was.
10. STANDING STALENESS GATE (R-0417, fourth run). Re-read every sentence in
    the files this round touched that states a COUNT, a module list, a
    round→step map, or a completion claim, and report for each whether it
    still holds at HEAD. Repair ONLY what the ordered slices cover; report
    everything else and leave it. State how many sentences you checked.
11. CHANGE SET: `git diff --name-only e6c18d89..HEAD` — report every path,
    COUNT them, and state whether you measured before or after C3. The Change
    list is a CEILING. Report
    `git diff --name-only e6c18d89..HEAD -- apps/ packages/ tests/ docs/`
    separately; it MUST be EMPTY.
12. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer baseline at
    e6c18d89: 184 passed. This round changes no code, so 184 is expected.
13. `python3 -m pytest tests/cli/test_stats_bench.py -q` → exit 0, 25 passed.
    R10's work must still stand.
14. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `handler_import` message; it
    must still be `handlers=337`.
15. `gh pr list --state open --json number,headRefName` → report verbatim.
    Must be `[]`.
16. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it with the inseparability reason BEFORE review. C3
    cannot state its own numstat; report it in the completion report.
No mutation red-proof is ordered and none is owed: R12 changes no executable
line. The docs-round gate does NOT bind: `docs/roadmap/**` is outside this
round's Change list, and gate 11 proves it.

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
             and no PR exists.
──────────────────────────────────────────────────────────────────────────────
