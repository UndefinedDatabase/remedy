── STEP R22/23 — F082 Self-benchmark — record R21, bring Built State current ──

Goal:
  Persist the R21 gate on disk, register the three defects the integration gate
  exposed — one of them a standing defect in `docs/agents/integration_gate.md`
  itself — rule the closure split at DECISION F082 D12, and bring the feature
  file's Built State section current so the closure round can start from a
  settled precondition instead of establishing one. It changes no code and no
  test.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f082-r22.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R21 + R-0443 + R-0444 + R-0445 +
       DECISION-D12, appended at EOF in ONE commit. Findings persist FIRST
       (planner_reviewer_prompt §4.4), before anything else this round touches.
  C2   `docs/roadmap/features/T2_F082.md` — the two rewrite pairs and the
       Built State append
  C3   `.agent/plan.md` and `.agent/context.md` — the PLAN slice and the
       CTXSTEPS-R22 pair, one commit
  C4   rewrite `.agent/handoff.md`

WHY THIS IS NOT THE CLOSURE ROUND. DECISION F082 D11 ruled R22 the closure. D12
below moves closure to R23 and states the reason there; the short form is that
docs/roadmap/STATUS_closure_protocol.md precondition 4 requires the feature
file's Built State to be current ALREADY, from an earlier commit, and a round
that establishes its own precondition and then consumes it is the shape D11
itself rejected.

BASE: c536123b. Re-derive `git rev-parse HEAD` before the first commit and
report whether it equals c536123b (R-0428). If it does NOT, stop and hand off.

TRANSPORT (the R21 shape, which proved out — planner_reviewer_prompt §4.9
primary proof): the reviewer's scratchpad original of THIS block is on disk at
`.remedy-wt/.cache/r22/f082-r22.md`, which `.gitignore` drops (line 235,
`.remedy-wt/`). C0a is a byte COPY of that file — do not retype it, do not
reflow it, do not strip anything.

SLICE CONVENTION (R-0437): every FROM and TO body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The block's authored units are, listed: two EOF
appends (GATE-R21-BLOCK into `.agent/live_review.md`, BUILTSTATE into
`docs/roadmap/features/T2_F082.md`); three REWRITE pairs with FROM and TO
disjoint (FEATHEAD and Q7TAIL in the feature file, CTXSTEPS-R22 in
`.agent/context.md`); and one whole-file replacement (PLAN). No numeral is
stated for that list — the list IS the statement (R-0402, R-0441).

Constraints:
  1. Change set: `.agent/authored/f082-r22.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `docs/roadmap/features/T2_F082.md`,
     `.agent/plan.md`, `.agent/context.md`, `.agent/handoff.md`. Nothing else.
     `packages/`, `apps/`, `scripts/` and `tests/` all stay EMPTY in the range
     diff, and `docs/` contains EXACTLY ONE file — gate 10 measures both as
     restrictions.
  2. Apply every slice BYTE-VERBATIM, including one you believe is wrong. A
     defect in my text is a declared deviation, never a silent repair.
  3. C1 lands BEFORE C2.
  4. This round adds NO worktree and runs no destructive check.
     `git worktree list` is one line throughout.
  5. Create NO pull request and touch NEITHER `docs/roadmap/STATUS.md` NOR
     `README.md`. Both belong to R23's closure commit, which is bound by the
     R-0154 exact-paths rule.
  6. This round's change set includes `docs/roadmap/**`, so the docs-round gate
     applies (planner_reviewer_prompt §3, verification tier 5): gate 7 runs
     `tests/docs/` in addition to the canary.

--- BEGIN SLICE GATE-R21-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R21 — PASS. Verification tier: INTEGRATION GATE — the full suite, and this is the one round of this feature entitled to that claim (planner_reviewer_prompt §3 tier 3). Every one of the sixteen ordered gates was re-executed by the reviewer against the committed tree and every value reproduced. The reviewer additionally ran the whole suite ITSELF at the final HEAD c536123b, two commits later than the worker's run at ae84e2cf, and got `16988 passed, 19 skipped in 150.21s`, exit 0, zero `^FAILED` and zero `^ERROR` — the same counts the worker measured, from a different commit and a different process, so the green covers C3, C4 and C5 as well. TRANSPORT is the round's structural improvement and it held: the block travelled scratchpad → authored → last_block and all THREE files are sha256 3c001e651bc0ff1571c0c199ced23f5c08b4989b71c0ddcb1a3bc9b08d4551a1, 24778 bytes, 280 lines, byte-equal to one another, with the footer's declared 280 equal to the measured 280 — the first round of this feature whose transport proof reaches back to the reviewer's own pre-emission bytes rather than stopping at the worker's copy of them. C1's prefix property, C2's two pairs and their composite, all four live_review line-anchored counts and all three context.md counts reproduce exactly as ordered; `.agent/plan.md` byte-equals the PLAN slice at sha256 f8b98857eec5849e9979fd3d38a364679349307b5fb5bcdd9fcc1c9659b72b32, 42 lines. The OPEN SET recomputed at HEAD is 72 registered, 2 resolved, 70 open, max R-0442, next free R-0443, 4 `Landed:` lines, no duplicate id — expected 72 and 2, measured 72 and 2. Insertions 280 · 206 · 8 · 5 · 235 · 20 · 81, none over 500. The change set restricted to `packages/`, `apps/`, `scripts/`, `docs/` and `tests/` is EMPTY at 0 files. THE GATE ITSELF: branch run exit 0 with 17007 collected — exactly the count the block declared at emission, which is R-0438's new rule paying for itself on its first use — against a base run at merge base 668d40f7 that failed 8. Branch-only failures: ZERO, so there is nothing to attribute on the side that could block, and no F082 code is implicated by anything. The 8 base-only failures are all `tests/ui_server/test_live_state.py::TestUIServerIntegration` and every one is attributed to the environment class by a proof stronger than the procedure requires: the worker did not merely name the missing artifact, it ran the experiment in BOTH directions inside the disposable worktree — the same 8 ids pass (`8 passed in 1.07s`) once `apps/ui/dist/index.html` is newer than `apps/ui/src`, and fail again (`8 failed in 40.57s`) when only that one mtime is set back, same commit, same environment variable, same code. The reviewer confirmed the mechanism independently by reading the base worktree's own code rather than accepting the account: `ui_server.py::_frontend_is_stale` returns True when any file under `apps/ui/src` is newer than `dist/index.html`, `::_auto_build_frontend` returns None under `REMEDY_UI_NO_AUTO_BUILD=1`, and `::_load_frontend` then prints "ERROR: React UI not built." and calls `sys.exit(1)`; the reviewer also recomputed the sha256 of all four uncommitted raw logs and all four match the committed provenance file. Teardown is proven: one worktree line, no `tmp/*` branch, clean tree. THREE findings are registered below and NONE of them is a defect of this round's work: one is the reviewer's gate shape, one is a scratch-directory hazard, and one is a standing defect in `docs/agents/integration_gate.md` that this round is the first to prove rather than suspect. That the worker found and declared all three before the reviewer read the diff is now the fifth consecutive round in which that happened.

- R-0443 — Medium, A GATE SCRATCH DIRECTORY REUSED ACROSS FEATURES, SO A STALE FILE CAN BE READ AS THIS ROUND'S MEASUREMENT. Found by the WORKER and declared as R21 deviation 3. The R21 block ordered raw logs into `.remedy-wt/.cache/gate_r21/` on the assumption it was fresh. It was not: it already held 2026-08-13 artifacts of a DIFFERENT feature's R21 — `branch_meta.txt`, `branch_failed.txt`, `comm_*.txt`, three `.sh` scripts and a handoff draft — because the directory is named after the round number only and round numbers repeat across features. Every colliding name was overwritten by this round's real measurement before it was read, and the reviewer confirmed the committed evidence is this round's throughout, so nothing false was published. Medium rather than Low because the failure mode it exposes is the vacuous-gate class R-0438 names: a wait-loop in the worker DID briefly read the stale `branch_meta.txt` as this round's, and had the round died between that read and the overwrite, a previous feature's numbers would have been reported as this gate's with nothing in the evidence chain able to detect it — the file would have had the right name, the right shape and the wrong provenance. Not High because the two suite runs write their own logs unconditionally and the reviewer can re-derive every committed number from the branch and base logs, as it did. Standing rule from here, binding the reviewer: a gate scratch directory is named for the FEATURE and the round, never the round alone, and the block orders it created fresh — the worker asserts the directory did not exist before this round, or reports what it found and deletes it before writing. A path that outlives the round that owns it is not scratch.

- R-0444 — Medium, A PARITY GATE WHOSE MEASUREMENT CANNOT SEE THE THING IT WAS ORDERED TO DETECT. Found by the WORKER and declared as R21 deviation 4; the defective gate is the reviewer's own. R21's gate 8 ordered a CONTENT digest of `apps/ui/dist` before and after the base run to verify that `REMEDY_UI_NO_AUTO_BUILD=1` had neutralised the auto-build. The digests are equal and the gate reads GREEN, but the flag did NOT neutralise every build path: `apps/ui/node_modules` (mtime 2026-08-15T11:39:47.807) and `apps/ui/dist/index.html` (11:39:49.669) were both rewritten INSIDE the base-run window 11:38:41–11:41:10, against the 11:36:04 the parity copy had left. The rebuild happened to be byte-identical, so a content digest is blind to it by construction — the gate would report GREEN for a rewrite of any content, identical or not, and only luck made those two the same case. This is R-0169 recurring, and the earlier fix (set the flag, then hash the content) is precisely the counter-measure this instance defeats. Medium: nothing was mismeasured this round because the content really was identical, but the neutralisation claim the gate exists to support was never actually tested. Standing rule from here, binding the reviewer: a gate that asserts something did NOT HAPPEN measures the event, not the outcome. For the build-neutralisation check that means recording mtimes — or a directory-state stamp covering mtime and inode — before and after, and reporting the window; a content digest may accompany it but never stands alone, because equal content is consistent with both "no rebuild" and "an identical rebuild".

- R-0445 — Medium, A STANDING DEFECT IN THE CANONICAL INTEGRATION-GATE PROCEDURE THAT MANUFACTURES EIGHT FALSE BASE FAILURES ON EVERY RUN AND MASKS REAL ONES. Found by the WORKER and declared as R21 deviation 5; proven in both directions before it was believed. `docs/agents/integration_gate.md` step 3 orders environment parity restored by COPYING `apps/ui/node_modules` and `apps/ui/dist` into the base worktree, and explicitly forbids symlinking for a good reason of its own. But a copy preserves the SOURCE mtime while `git worktree add` stamps the freshly checked-out sources with the checkout time, so the copied build is ALWAYS older than the sources it was built from. `ui_server.py::_frontend_is_stale` therefore returns True, `::_auto_build_frontend` returns None under the flag the same procedure sets, and `::_load_frontend` calls `sys.exit(1)`; the server thread dies and all eight `tests/ui_server/test_live_state.py::TestUIServerIntegration` ids fail with "Server did not start in time". The procedure cannot restore freshness by copying, so this recurs on EVERY gate run for EVERY feature — the same eight ids appear in `.agent/gate_f077_r16/base_failed.txt` from the previous feature, which is the recurrence already on disk and unrecognised at the time. Medium and not Low because integration_gate.md step 3 states in its own words that a genuine base failure in those same files WOULD BE MASKED by the environment-class attribution, and eight permanently-failing ids in the UI server's integration tests are exactly the place a real regression would hide. Not High because it produces no false GREEN — the branch side is unaffected, and every gate run so far has attributed the ids rather than ignoring them. The repair is one line of procedure and belongs to `docs/agents/integration_gate.md`, NOT to this feature branch: after the parity copy, touch `apps/ui/dist/index.html` forward of every file under `apps/ui/src` (or build in the worktree), and have the procedure verify `_frontend_is_stale()` is False before the base run rather than discovering it afterwards. Routed to a follow-up rather than repaired here, because a process-doc fix inside a feature branch is scope drift and F082's closure states it as a known open finding.

## DECISION F082 D12 — closure moves to R23; a round may not establish the precondition it consumes

Chosen: R22 is this verdict-and-Built-State round; R23 is closure per
docs/roadmap/STATUS_closure_protocol.md. The denominator moves from 22 to 23 in
`.agent/plan.md`, `.agent/context.md` and every later block header.

Why: the closure protocol's precondition 4 requires the feature file's Built
State to be current, and its step 5 requires that the closure commit touch
EXACTLY `docs/roadmap/STATUS.md`, `README.md` and the final `.agent/` state
(R-0154). F082's Built State section still describes the R11 T003b INVENTORY —
seven questions asked before T003b was built — so it must be rewritten, and that
rewrite cannot ride in the closure commit without breaking the exact-paths rule.
Bundling it into the closure ROUND instead would mean the round establishes
precondition 4 and then consumes it a commit later, which is the same
self-certifying shape D11 rejected for the R19 verdict, and it would put an
authored Built State rewrite, an evidence job, a review-zip build and the STATUS
edit in one block — over the 400-line cap (DECISION F105 D5) before the gates
are written.

Rejected: closing at R22 anyway and calling the Built State "current enough".
The section's last paragraph says a later round OWES a test that R16 has since
delivered, so the file on disk understates what was built; closing over that
would publish a Built State that the branch's own history contradicts.

How to reverse: delete this decision, renumber R23 back to R22, and restore the
denominator to 22. Nothing executable depends on the numbering.
--- END SLICE GATE-R21-BLOCK ---

--- BEGIN SLICE FEATHEAD --- (in docs/roadmap/features/T2_F082.md, C2 — REWRITE pair, FROM and TO disjoint)
## Built State — the T003b inventory (R11)
--- BEGIN SLICE FEATHEAD-TO --- (C2)
## Inventory — the T003b questions (R11)
--- END SLICE FEATHEAD-TO ---

--- BEGIN SLICE Q7TAIL --- (in docs/roadmap/features/T2_F082.md, C2 — REWRITE pair, FROM and TO disjoint)
VIEW as read-only rather than the bench as never-implicit. An unpinned
acceptance criterion is a closure blocker, so a later round owes a test that
asserts the absence of an implicit caller.
--- BEGIN SLICE Q7TAIL-TO --- (C2)
VIEW as read-only rather than the bench as never-implicit. An unpinned
acceptance criterion is a closure blocker, so a later round owed a test that
asserts the absence of an implicit caller. R16 delivered it — see Built State.
--- END SLICE Q7TAIL-TO ---

--- BEGIN SLICE BUILTSTATE --- (APPEND to docs/roadmap/features/T2_F082.md, C2, with exactly one blank line between the file's current last line and the first line of this slice)
## Built State — what F082 delivered

Six new modules, all ADDITIVE: no symbol moved out of any gauntlet module, and
the gauntlet's own seven test files are green UNMODIFIED. Each carries its own
test file under `tests/orchestration/`, except the CLI view, whose test sits
under `tests/cli/`.

- `packages/orchestration/capability_bench.py` — `BenchRecord` and the pure
  record builder. Carries a defaulted `models` field.
- `packages/orchestration/bench_orders.py` — `load_bench_order_set` over THREE
  frozen orders under `scripts/bench_orders/`, with the version freeze:
  editing an order without bumping its version raises `BenchOrderSetError`.
- `packages/orchestration/bench_dry_run.py` — the join from an order file to a
  row over recorded evidence.
- `packages/orchestration/bench_history.py` — the append-only history, the
  trend, and the regression rules including the `pass_drop` warning.
- `packages/orchestration/bench_run.py` — the run itself, joining the frozen
  order set to a campaign, the campaign's evidence to bench rows, and the rows
  to a history file. Its data root and history path are REQUIRED arguments, so
  a run cannot append into the operator's real data root.
- `apps/cli/commands/bench_cmd.py` — the `remedy stats bench` read view, one
  new handler key, changing no bench module.

One gauntlet module was edited, under DECISION F082 D1: `gauntlet_runner.py`
gained `measure_tokens` (R-0407) and, under D7/D8, a `models` key in
`_evidence_body` naming which model served which role.

Acceptance, measured rather than argued. The bench runs green on fixtures and a
deliberately degraded run raises the warning — both asserted at R19 by
`test_every_row_passes_on_a_clean_fixture_run` and
`test_a_deliberately_degraded_run_triggers_the_pass_drop_warning`, with a
red-proof in a disposable worktree confirming both go red when the stored gate
verdict is removed. History survives across runs. "The bench never runs
implicitly" is pinned at R16 by
`tests/orchestration/test_bench_never_runs_implicitly.py` as an enumerated
allowlist of permitted callers under DECISION F082 D9 — the allowlist holds
EXACTLY ONE name, `bench_run.py` — rather than as a total absence, because the
run that completes the feature is itself the first legitimate caller.

Four absences, stated rather than implied:

- THREE frozen orders, not the Design's five (R-0411). The shared sample project
  has no HTTP surface and no web asset, so the API-endpoint and frontend-widget
  orders have nothing to probe; they wait on a bench-owned fixture per
  DECISION F082 D3, not on an edit to the gauntlet's template.
- The version freeze holds against a file-side edit only (R-0410). A
  coordinated edit that also rewrites the digest recorded under the version the
  file still claims is not refused.
- The BUILDER's model stays unobservable (R11 Q1, Q4).
  `orchestrator_loop.py::execute_dispatched_job` constructs `OllamaBuilder()`
  where no seam can observe it, so `models` records the orchestrator and the
  planner and is honest about the third being absent.
- Every acceptance measurement was taken under DOUBLES, never under a live
  provider, and every row's `cost` is `None` under doubles while `wall_s` is
  clock-derived from the runner. Pass rate is therefore the only trend a real
  run can prove today, which is why the R19 warning property is scoped to
  `pass_drop`.
--- END SLICE BUILTSTATE ---

--- BEGIN SLICE CTXSTEPS-R22 --- (in .agent/context.md, C3 — REWRITE pair, FROM and TO disjoint)
verdict, register R-0438 and R-0439 and rule at D11 ✅ → R21 the integration
gate → R22 closure, per DECISION F082 D11.
--- BEGIN SLICE CTXSTEPS-R22-TO --- (C3)
verdict, register R-0438 and R-0439 and rule at D11 ✅ → R21 the integration
gate ✅ → R22 record R21, register R-0443 to R-0445 and bring Built State
current → R23 closure, per DECISION F082 D12.
--- END SLICE CTXSTEPS-R22-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C3)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0446. Open findings: seventy-three — the thirty-two carried from F077,
plus R-0403 to R-0445 registered on this branch, less R-0435 and R-0436
resolved at R20. `.agent/live_review.md` is the source of truth; this file
mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R22 records the R21 integration-gate PASS, registers R-0443 to R-0445 — a
scratch-directory hazard, a parity gate blind to what it was ordered to detect,
and a standing defect in `docs/agents/integration_gate.md` — rules the closure
split at DECISION F082 D12, and rewrites the feature file's Built State section
so R23 starts from a settled closure precondition.

## Next Steps
1. R23 closure per docs/roadmap/STATUS_closure_protocol.md: the evidence job,
   a FRESH review zip, the STATUS line, the README count and Tier-2 row,
   `.agent/candidates.md`, and the PR.

## Risks
- The integration gate PASSED: zero branch-only failures, and the eight
  base-only failures are attributed to the environment class in both
  directions. Closure claims full-suite green on that evidence and on the
  reviewer's own run at c536123b, and on nothing else.
- Closure preconditions are met but not yet re-measured at the closure head:
  no Blocker or High finding is open (73 open, all Medium or Low) and the
  integrity gate passes today. R23 re-runs both rather than carrying them.
- The review zip is the closure BLOCKER of record — a failing build stops the
  closure, and R-0403 already records that the zip packages `.remedy-wt/`.
- Every acceptance measurement was taken under DOUBLES, never a live provider;
  the delivered order set is three, not five (R-0411); the freeze holds against
  a file-side edit only (R-0410); the builder's model stays unobservable.
  Closure states all four absences rather than implying otherwise.
- Reviewer and handback text defects remain the dominant finding class: the
  standing counter-measures binding every block are R-0417 through R-0445,
  stated as a range and deliberately WITHOUT a count (R-0436).
--- END SLICE PLAN ---

Done when — run every gate and record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and after the last.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and again at handback (R-0347).
 2. TRANSPORT, bytes read in Python rather than through a shell utility: report
    sha256, byte count and line count of `.remedy-wt/.cache/r22/f082-r22.md`,
    `.agent/authored/f082-r22.md` and `.agent/last_block.md`, and whether all
    three byte strings are EQUAL. Report whether the measured line count equals
    the count this block declares in its footer.
 3. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals c536123b.
 4. C1 is an APPEND and is proven as a PREFIX PROPERTY, not by counting lines:
    over `<C1>^..<C1>`, report that `pre` is a prefix of `post` and that
    `post[len(pre):]` equals `b"\n" + GATE-R21-BLOCK` byte-for-byte. Report the
    numstat for the file and confirm its deletion column is 0.
 5. C2 carries two REWRITE pairs and one APPEND into the SAME file, so prove it
    as one composite: report for FEATHEAD and for Q7TAIL the FROM count in
    `pre`, the FROM count in `post`, the TO count in `post`, and `FROM in TO`;
    then report that
    `pre.replace(F1,T1).replace(F2,T2) + b"\n" + BUILTSTATE == post`
    byte-wise. That single equality settles both rewrites AND the append
    together; report it as True or False, not as prose.
 6. C3's CTXSTEPS-R22 pair: the same four numbers, plus the composite
    `pre.replace(F,T) == post` over `.agent/context.md`.
 7. VERIFICATION. This round's change set includes `docs/roadmap/**`, so the
    docs-round gate applies: `python3 -m pytest tests/docs/ -q`, which the
    reviewer measured at emission as collecting 295 tests. Then the canary,
    `python3 -m pytest tests/cli/test_golden_path.py -q`, 42 collected. Report
    the collected count and the real exit code for EACH, separately (R-0438).
 8. Line-anchored counts, each reported with the exact pattern and the file it
    was counted in (R-0442). In `.agent/live_review.md` at HEAD: `^- R-0443 — `
    1x, `^- R-0444 — ` 1x, `^- R-0445 — ` 1x, `^Gate: R21 ` 1x,
    `^## DECISION F082 D12` 1x. In `docs/roadmap/features/T2_F082.md` at HEAD:
    the literal `## Built State` 1x, the literal `## Inventory — the T003b`
    1x, and the literal `a later round owes a test` 0x.
 9. `.agent/plan.md` at HEAD byte-equals the PLAN slice as a WHOLE FILE; report
    sha256 and line count (must be under 50), and that `## Goal` and
    `## Next Steps` are both present.
10. CHANGE SET, measured BEFORE C4: `git diff --name-only c536123b..HEAD`.
    Report the full list and its count. Restricted to `packages/`, `apps/`,
    `scripts/` and `tests/` it must be EMPTY; restricted to `docs/` it must be
    EXACTLY ONE file, `docs/roadmap/features/T2_F082.md`. Report both
    restrictions as measured lists, not as assertions.
11. OPEN SET recomputed mechanically at HEAD: count `^- R-\d+ — ` paragraphs,
    count `^Done: R-\d+ — ` lines, report both, their difference, the max id,
    the next free id, and the count of remaining `^Landed: ` lines. Report any
    duplicate id. The expected shape after this round is 75 registered and 2
    resolved; report what you MEASURE, and if it differs say so rather than
    reconciling it.
12. CLOSURE PRECONDITIONS, measured now so R23 starts from known ground, and
    reported as values rather than as a verdict. (a) Severity census of the
    OPEN set: count open findings whose severity word is Blocker, High, Medium
    and Low, reading the word that follows `^- R-\d+ — ` up to the first comma;
    report all four counts. (b) The integrity gate, invoked in Python because
    the `remedy` CLI is denied in this session class (R-0408 — gate the
    property, not the tool):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"`.
    Report `passed`, `fail_count`, and the status of every named check.
13. Insertions (`+` column only) per commit — report each; none over 500.
14. STALENESS GATE, standing since R-0417. READ — do not grep — every
    claim-bearing sentence in `.agent/context.md` and `.agent/plan.md` at HEAD.
    Report the number READ, the number that HOLD, and name separately those that
    do NOT hold and those this round's gates never measured. Repair nothing
    outside Constraint 1; report it for R23.
15. `gh pr list --state open --json number,headRefName` — report it. Create NO
    PR.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and every gate, open findings
with max and next free id, and the next expected action. THE NEXT SESSION'S
FIRST ACTION is self_drive_protocol.md Phase 1 rule 1, re-read `.agent/STOP`
from disk, BEFORE rule 2's Open PR Gate. Repeat this line verbatim as the
Fortschritt line:

Fortschritt: ~99 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b ✅ · alle drei DONE-Bedingungen gemessen · Integrationsgate R21 ✅ PASS, null branch-only Failures · Built State aktuell · nur noch Closure R23 offen) — Schätzung

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, and end. Do
not widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 324 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
