── STEP R20/22 — F082 Self-benchmark — record the R19 verdict, rule at D11 ───

Goal:
  Persist the R19 gate on disk. R19 was REVIEWED and PASSED: the reviewer
  re-ran every one of the seventeen gates against the committed tree and every
  value reproduced. This round writes that verdict into the record, registers
  the two block defects the round exposed — both the reviewer's own — converts
  the two `Landed:` lines R19 wrote into reviewer-authored `Done:` resolutions,
  and rules the remaining round map at DECISION F082 D11. It changes no code
  and no test.

Bundle, in commit order:
  C0a  save this block verbatim as `.agent/authored/f082-r20.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R19 + R-0438 + R-0439 + DECISION-D11,
       appended at EOF in ONE commit. Findings persist FIRST
       (planner_reviewer_prompt §4.4), before anything else this round touches.
  C2   `.agent/live_review.md` — the two Landed→Done conversions
  C3   `.agent/context.md` — CTXSTEPS-R20
  C4   `.agent/plan.md` — the PLAN slice, whole file
  C5   rewrite `.agent/handoff.md`

BASE: 418ee838. Re-derive `git rev-parse HEAD` before the first commit and
report whether it equals 418ee838 (R-0428). If it does NOT, stop and hand off.

SLICE CONVENTION (R-0437): every FROM and TO body below is the lines between
its markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. All three FROM/TO pairs below are REWRITES with
FROM and TO disjoint. Two EOF appends (GATE-R19-BLOCK, which carries the gate,
both findings and the decision as one body) and one whole-file replacement
(PLAN). Four named units, counted by listing them.

C2's TWO FROM STRINGS ARE NOT RETYPED IN THIS BLOCK. Derive each DISK-TO-DISK
from the COMMITTED `.agent/authored/f082-r19.md`: extract its `LR-LANDED` slice
body, whose first line is the `Landed: R-0435 …` line and whose second line is
the `Landed: R-0436 …` line. Each of those two lines, with its trailing
newline, IS the FROM. Retyping either is forbidden — a 475-character line is
exactly what transport loses (R-0147 class).

Constraints:
  1. Change set: `.agent/authored/f082-r20.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/context.md`, `.agent/plan.md`,
     `.agent/handoff.md`. Nothing else. `packages/`, `apps/`, `scripts/`,
     `docs/` and `tests/` all stay EMPTY in the range diff — this round touches
     no code and no test, and gate 8 measures that as a restriction.
  2. Apply every slice BYTE-VERBATIM, including one you believe is wrong. A
     defect in my text is a declared deviation, never a silent repair.
  3. C1 lands BEFORE C2. If the session dies between them, the findings must
     already be on disk; a resolution that outlives its finding is worse than
     an unresolved one.
  4. No destructive verification is ordered this round, so add NO worktree.
     `git worktree list` must be one line throughout.
  5. Create NO pull request. F082's PR is created at closure, now R22.

--- BEGIN SLICE GATE-R19-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R19 — PASS. Verification tier: round gate plus the canary; no full-suite claim is made or implied. The reviewer re-executed all seventeen ordered gates against the committed tree and every value reproduced. Transport is PRIMARY strength: `.agent/authored/f082-r19.md` and `.agent/last_block.md` are byte-identical to the reviewer's own pre-emission original, 22165 bytes, 398 lines, sha256 a3e579954d55bd6d8d2daff26c3c7c8021ca05e2c7ffb30b8b2973fbc8d4a8b2, and the block's declared 398 equals its measured 398 (R-0420 held for a fourth consecutive round). The strongest proof this round admits is a byte identity the reviewer could only compute because it built and RAN the composite before emitting the block: `tests/orchestration/test_bench_run.py` at HEAD is byte-identical to the reviewer's independently assembled composite, sha256 4fc0420c5ea0f8638736ebd18b4de96af5dfe936d9f9ddd52ae40d397787c3df, so every one of the nine slices applied verbatim and nothing drifted between authoring and disk. R-0435 is REPAIRED IN SUBSTANCE, not merely in text: the reviewer's own probe at HEAD, run through the module's own `_run` helper, prints `[('b01-cli-report-width', True), ('b02-config-lookup-bugfix', True), ('b03-cli-render-refactor', True)]`, where the same probe at BASE printed three `False`. F082's FIRST Done condition — the bench runs green on fixtures — is therefore MEASURED for the first time in this feature's history, and its THIRD — a deliberately degraded run warns — is reachable at last, because `bench_regressions` emits `pass_drop` only against a trailing pass rate above zero. The red-proof reproduces exactly: deleting the single line `self._store_gate_verdict()` inside a disposable worktree turns the two NEW properties red and leaves the seven older ones green, which is R-0435 stated as an experiment rather than as prose. The round's additive claim is measured as a restriction and holds — the range `418ee838..26dc94d2` reversed, restricted to `packages/`, `apps/`, `scripts/` and `docs/`, is EMPTY, and the gauntlet's seven test files are untouched. Insertions per commit: 398 · 365 · 124 · 1 · 15 · 3 · 207, none over 500. The handback is complete: every mandated section present, the item-status table covering every C-item and every gate exactly once, the Fortschritt line byte-identical to the block's, and the 246-line length declared under AGENTS.md DECISION D15 with its cause named. TWO findings are registered below and BOTH are the reviewer's own block defects; both were found by the WORKER and declared before the reviewer read the diff, which is now the third consecutive round in which that happened and is the healthiest signal in this feature.

- R-0438 — Medium, A GATE THAT NAMED A PATH THAT DOES NOT EXIST, so the check it stood for never ran. Found by the WORKER while executing R19's gate 10 and declared as deviation 1. The gate ordered the canary "plus the `.agent`-state contract readers `tests/dashboard`, `tests/test_test_runner.py` and `tests/regression/test_resource_safety.py`". There is no `tests/dashboard` directory in this repository; pytest exits 4 with "no tests ran" and reports no failure, so the gate is not merely wrong, it is SILENTLY vacuous — the one failure mode this repository spends the most effort refusing. The dashboard contract reader is `tests/ui_server/test_dashboard_contract.py`, and the reviewer confirmed the absence and the real location after the handback: `ls tests/` has no `dashboard` entry, and `rg -l 'context.md' tests/` returns `tests/ui_server/test_dashboard_contract.py`. Medium, not Low, because a vacuous gate reports green for the wrong reason and had this round changed `.agent/context.md` in a way the dashboard contract rejects, nothing in the ordered gate list would have caught it — and this round DID change `.agent/context.md`. Not High, because the property was in fact intact: the reviewer ran `pytest tests/test_test_runner.py tests/regression/test_resource_safety.py tests/ui_server -q` at HEAD and got 324 passed, exit 0. The CAUSE is precise and is NOT a typo. `docs/agents/planner_reviewer_prompt.md` §4.11 names the contract READERS in prose — "the dashboard contract asserts the substring Steps plus ## Active Branch" — and the reviewer turned that prose into a PATH without ever resolving it against the disk. §4.11's own instruction, in the same paragraph, is to grep every test that reads the file (`rg -ln '<filename>' tests/`); the reviewer cited the rule and skipped the command it prescribes. This is R-0353's class — a citation that does not resolve — in the form that checklist item 9 does not cover, because item 9 re-measures `file:line` citations against the branch's own edits and this path was never valid on any branch. Standing rule from here, binding the reviewer: every path a gate names is resolved on disk at emission — `ls` or `test -e` — and a gate that names a test target additionally states the count that target is expected to collect, because a path that exists but collects nothing fails the same way. A gate whose target cannot be shown to exist is not ordered.

- R-0439 — Low, A PER-LINE COUNT ORDERED OVER LINES THAT CANNOT BE UNIQUELY COUNTED. Found by the WORKER while proving R19's gate 4 and declared as deviation 3. For the two append-shaped pairs the gate ordered "the per-line count of each TO-ONLY line among the lines that commit's diff ADDS". Applied literally to EVERY TO-only line, that includes blank lines and the `# ---…---` rule comments the file uses as section separators, which the same commit adds many times over — the worker measured 2x, 4x and 20x and REPORTED those real numbers rather than the 1x the gate's phrasing implies. Both readings are defensible and the worker chose the honest one. Low, because the composite proof at the same gate settles application byte-for-byte and no wrong conclusion was drawn. What makes it worth registering is that this is the THIRD form of one recurring mistake: R-0253 established that whole-file counts are unsatisfiable when a TO legitimately repeats an existing sentence, R-0437 established that a pair's SHAPE is undefined without its newline convention, and this one establishes that a per-line count is undefined without saying WHICH lines it ranges over. Each time, the rule was written down for the instance in front of it and not for the measurement class it belongs to. Standing rule from here, binding the reviewer: a per-line count over a diff's added lines NAMES the specific distinguishing lines to be counted — lines unique to the TO by inspection — and never says "each TO-only line". Blank lines, separator comments and repeated structural lines are excluded by construction and the gate says so.

## DECISION F082 D11 — the integration gate moves to R21 and closure to R22

Chosen: R20 is this verdict-recording round; R21 is the integration gate per
docs/agents/integration_gate.md; R22 is closure. The denominator moves from 21
to 22 in `.agent/plan.md`, `.agent/context.md` and every later block header.

Why: DECISION F082 D10 bundled the R19 verdict INTO the integration-gate round,
which is the pattern every earlier round on this branch used and which is
correct when the reviewer has the capacity to gate both. It does not hold here.
The integration gate is a full-suite branch run plus a base-worktree run with
node-modules parity restoration plus per-id attribution, and the reviewer must
re-run all of it to gate it — a worker's suite result is not a verdict. A
reviewer that authors that round without the capacity to gate it produces
exactly the state this protocol forbids: new work planned over an ungated
round (self_drive_protocol.md Phase 1 rule 4). Splitting costs one round and
keeps every round gated.

Rejected: bundling the verdict into R21 anyway and letting the next session
gate both. That leaves R19's PASS unrecorded on disk, so the next session reads
a handback awaiting review and re-reviews a round that was already fully
verified — the verdict would exist only in a dead session's memory, which is
the A1 trap that planner_reviewer_prompt.md §0 names.

How to reverse: delete this decision, renumber R21 back to R20, and restore the
denominator to 21. Nothing executable depends on the numbering.
--- END SLICE GATE-R19-BLOCK ---

--- BEGIN SLICE DONE-R435-TO --- (in .agent/live_review.md, C2 — REWRITE pair; the FROM is the FIRST line of the committed .agent/authored/f082-r19.md LR-LANDED slice, extracted disk-to-disk, WITH its trailing newline)
Done: R-0435 — the mission double now stores a real `GateResult` through the product's own `dod_gate.py::save_gate_result`, written from inside `run_order`'s isolated environment so nothing resolves to the operator's root, and `FakeMission` carries the `job_links` entry `latest_gate_result` reads. Verified by the reviewer at HEAD, not accepted from the handback: a probe through the module's own `_run` helper prints `passed=True` for all three frozen orders where the same probe at BASE printed three `False`. Two new properties assert what the rows SAY rather than that they exist — `test_every_row_passes_on_a_clean_fixture_run` and `test_a_deliberately_degraded_run_triggers_the_pass_drop_warning` — and a red-proof in a disposable worktree confirms both go RED when the stored verdict is removed while the seven older properties stay green, which is the vacuity R-0435 reported, demonstrated. No production code changed: the range restricted to `packages/`, `apps/`, `scripts/` and `docs/` is EMPTY. The finding's standing rule — that a contract for a test driving a product path to a RECORD asserts what the record SAYS — is now enforced by a test rather than by a rule, which is the only enforcement that survives a session ending.
--- END SLICE DONE-R435-TO ---

--- BEGIN SLICE DONE-R436-TO --- (in .agent/live_review.md, C2 — REWRITE pair; the FROM is the SECOND line of that same LR-LANDED slice, extracted disk-to-disk, WITH its trailing newline)
Done: R-0436 — `.agent/plan.md`'s counter-measure risk now reads "the standing counter-measures binding every block are R-0417 through R-0437, stated as a range and deliberately WITHOUT a count". Verified by the reviewer against the committed file, which byte-equals the R19 PLAN slice as a whole file, sha256 a3da81c8fb32b7ddd3881382b2fe18608b03970944ebbf48a42f388ec340054e. The repair is the form the finding's own standing rule prescribes: a range and a count are two statements that drift independently, and the numeral adds nothing a reader cannot get from the range. The range is re-stated at every plan rewrite and its endpoint moves with the record, so the sentence cannot go stale in the way the numeral did.
--- END SLICE DONE-R436-TO ---

--- BEGIN SLICE CTXSTEPS-R20 --- (in .agent/context.md, C3 — REWRITE pair)
R-0431 to R-0434 ✅ → R19 the acceptance proof for R-0435 → R20 the integration
gate → R21 closure, per DECISION F082 D10.
--- BEGIN SLICE CTXSTEPS-R20-TO --- (C3)
R-0431 to R-0434 ✅ → R19 the acceptance proof for R-0435 ✅ → R20 record the R19
verdict, register R-0438 and R-0439 and rule at D11 → R21 the integration gate
→ R22 closure, per DECISION F082 D11.
--- END SLICE CTXSTEPS-R20-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C4)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0440. Open findings: sixty-seven — the thirty-two carried from F077, plus
R-0403 to R-0439 registered on this branch, less R-0435 and R-0436 resolved at
R20. `.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R20 records the R19 PASS verdict, registers R-0438 and R-0439 — both reviewer
block defects — converts R-0435 and R-0436 from `Landed:` to reviewer-authored
`Done:`, and rules at DECISION F082 D11 that the integration gate is R21 and
closure R22. It changes no code and no test.

## Next Steps
1. R21 the integration gate, per docs/agents/integration_gate.md.
2. R22 closure: STATUS line, Built State, closure candidates, the PR.

## Risks
- All three DONE conditions are now MEASURED by the suite, not argued: R19's
  two new properties cover green-on-fixtures and the degraded-run warning, and
  the history property already covered survival across runs. Closure states
  they were measured under DOUBLES, never under a live provider.
- The delivered order set is three, not the Design's five (R-0411), the freeze
  holds against a file-side edit only (R-0410), and the builder's model stays
  unobservable — closure states all three absences rather than implying five
  orders and three recorded roles.
- `wall_s` is clock-derived and every row's `cost` is `None` under doubles, so
  pass rate is the only trend a real run can prove; the R19 warning property is
  scoped to `pass_drop` for exactly that reason.
- Reviewer defects remain the dominant finding class: the standing
  counter-measures binding every block are R-0417 through R-0439, stated as a
  range and deliberately WITHOUT a count (R-0436).
--- END SLICE PLAN ---

Done when — run every gate and record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and after the last.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round
    start and again at handback (R-0347).
 2. TRANSPORT: byte equality of `.agent/authored/f082-r20.md` and
    `.agent/last_block.md`, read as bytes in Python rather than through a shell
    utility; report sha256, byte count and `wc -l` of both, and whether the
    measured line count equals the count this block declares in its footer.
 3. BASE: `git rev-parse HEAD` before the first commit; report it and whether
    it equals 418ee838.
 4. C1 is an APPEND and is proven as a PREFIX PROPERTY, not by counting lines:
    over `<C1>^..<C1>`, report that `pre` is a prefix of `post` and that
    `post[len(pre):]` equals `b"\n" + GATE-R19-BLOCK` byte-for-byte. Report the
    numstat for the file and confirm its deletion column is 0.
 5. C2, both pairs: report for each the FROM count in `pre`, FROM count in
    `post`, TO count in `post`, and `FROM in TO`. Report also that each FROM
    was extracted from the committed `.agent/authored/f082-r19.md` and NOT
    retyped — state the sha256 of the extracted LR-LANDED slice body. Then the
    COMPOSITE: `pre` with both replacements equals `post`, byte-wise.
 6. C3: same four numbers for CTXSTEPS-R20, plus the composite.
 7. Line-anchored counts in `.agent/live_review.md` at HEAD: `^- R-0438 — ` 1x,
    `^- R-0439 — ` 1x, `^## DECISION F082 D11` 1x, `^Gate: R19 ` 1x,
    `^Done: R-0435 ` 1x, `^Done: R-0436 ` 1x, `^Landed: R-0435` 0x,
    `^Landed: R-0436` 0x. Report every one of the eight measured values.
 8. CHANGE SET, measured BEFORE C5: `git diff --name-only 418ee838..HEAD`.
    Report the full list and its count. Restricted to `packages/`, `apps/`,
    `scripts/`, `docs/` and `tests/` it must be EMPTY — this round's claim to
    change nothing executable, measured as a restriction rather than asserted.
 9. OPEN SET recomputed mechanically at HEAD: count `^- R-\d+ — ` paragraphs,
    count `^Done: R-\d+ — ` lines, report both, their difference, the max id,
    the next free id, and the count of remaining `^Landed: ` lines. Report any
    duplicate id. The expected shape after this round is 69 registered and 2
    resolved; report what you MEASURE, and if it differs say so rather than
    reconciling it.
10. `.agent/plan.md` byte-equals the PLAN slice as a WHOLE FILE; report sha256
    and `wc -l` (must be under 50), and that `## Goal` and `## Next Steps` are
    both present.
11. CONTRACT READERS — the repair of R-0438, run in the same round that
    registers it. `python3 -m pytest tests/test_test_runner.py
    tests/regression/test_resource_safety.py tests/ui_server -q`. These paths
    were resolved on disk before this block was emitted; report the collected
    count and the exit code. Then the canary,
    `python3 -m pytest tests/cli/test_golden_path.py -q`.
12. Insertions (`+` column only) per commit — report each; none over 500.
13. STALENESS GATE, standing since R-0417. READ — do not grep — every
    claim-bearing sentence in `.agent/context.md` and `.agent/plan.md` at HEAD.
    Report the number READ, the number that HOLD, and name separately those
    that do NOT hold and those this round's gates never measured. Repair
    nothing outside Constraint 1; report it for R21.
14. `gh pr list --state open --json number,headRefName` — report it. Create NO
    PR.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
feature and round, branch, per-commit changed-files tables, the fourteen gate
values above, the item-status table covering every C-item and every gate, open
findings with max and next free id, and the next expected action. THE NEXT
SESSION'S FIRST ACTION is self_drive_protocol.md Phase 1 rule 1, re-read
`.agent/STOP` from disk, BEFORE rule 2's Open PR Gate. Repeat this line
verbatim as the Fortschritt line:

Fortschritt: ~97 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b ✅ · Q7-Kriterium gepinnt · Fake-Provider-Lauf gelandet · alle drei DONE-Bedingungen erstmals gemessen · R-0435 und R-0436 aufgelöst · Integrationsgate R21 + Closure R22 offen) — Schätzung

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, and end. Do
not widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 219 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
