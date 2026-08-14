── STEP T003 (bookkeeping + ground survey) — F045 ──────────────
Goal:        Close the three findings whose fixes are already on disk and
             verified, then survey the fake-provider pipeline so the NEXT round
             can author the end-to-end fixture test from measured facts.

Bundle:      C0a save this block · C0b point last_block at it · C1 the three
             reviewer-authored `Done:` lines · C2 the pipeline inventory ·
             C3 plan.md and the handoff.

Change:      Exactly these files, nothing beyond them:
             - `.agent/authored/f045-r12.md` (NEW, C0a)
             - `.agent/last_block.md` (C0b)
             - `.agent/live_review.md` (C1)
             - `.agent/f045_e2e_inventory.md` (NEW, C2)
             - `.agent/plan.md` and `.agent/handoff.md` (C3)
             NO production code. NO test files. If you believe a production
             change is required, STOP and report it instead of making it.

Insertion budget, per commit, measured or reasoned (finding R-0350):
             C0a and C0b are each the verbatim rewrite of a SINGLE `.agent/**`
             state file and are cap-EXEMPT by DECISION F104 D1.
             C1 adds exactly 6 lines — three authored lines plus one blank
             separator before each — measured from the authored text below.
             C2's size is deliberately NOT predicted: a survey's length follows
             what it finds, so no number is asserted here. If C2 alone exceeds
             500 insertions, split it by section and declare the split.
             C3 is two `.agent/**` files, both far under the cap.

── C0a ────────────────────────────────────────────────────────
Write `.agent/authored/f045-r12.md` with the bytes described above.
Commit alone. Subject: `chore(f045): save the R12 block verbatim`

── C0b ────────────────────────────────────────────────────────
Copy `.agent/authored/f045-r12.md` to `.agent/last_block.md` so the two are
byte-identical. Commit alone.
Subject: `chore(f045): point last_block at the R12 block`
Ordered as its own commit because two small commits review better than one and
splitting removes a cap question from commit time — not for a size reason.

── C1 — the three `Done:` lines ───────────────────────────────
APPEND to `.agent/live_review.md`, at the very END of the file, in this order:
a blank line, then DONE-353; a blank line, then DONE-355; a blank line, then
DONE-356. Each DONE text is ONE physical line — do not re-wrap it, do not
insert newlines into it, do not add trailing whitespace. Take the bytes from
your saved `.agent/authored/f045-r12.md`, not from a retype.

These are REVIEWER-AUTHORED texts. You may not edit them, shorten them, or
write any `Done:` paragraph of your own (planner_reviewer_prompt.md §4.4).
If any of them is wrong, do NOT correct it — stop and report it.

>>> DONE-353 >>>
Done: R-0353 — RESOLVED at the R12 gate. Verified against the disk, not the report: the counter-measure is ON DISK rather than in reviewer habit, which is what finally closed R-0347 and what this finding's own text asked for. `docs/agents/planner_reviewer_prompt.md` §3 carries checklist item 9, "Citations re-measured against this branch's own edits", which orders every `file:line` a block cites for a file the CURRENT feature branch has already modified to be re-grepped at emission, and prefers the SYMBOL plus its distinguishing text over a bare number because a symbol survives an edit above it and a line number does not — the exact remedy the finding names. The stale intro count that governs the list moved from six to ten in the same commit `c59b5187`, so the checklist's header no longer under-counts the checks a reviewer must run. The reviewer re-derived the count mechanically at this gate rather than reading it: the numbered run in §3 is 1 through 10 with no gap and no repeat, and the intro line reads "ten checks mechanically".
<<< DONE-353 <<<

>>> DONE-355 >>>
Done: R-0355 — RESOLVED at the R12 gate. Verified against the disk, not the report: `remedy loop list` no longer borrows the RUN notice. `apps/cli/commands/loop_cmd.py` defines its own `INERT_TRIGGER_LEGEND`, "cannot fire until the scheduler exists; run such a loop manually", and the comment directly above it records why a listing deliberately does not reuse `loop_spec.INERT_TRIGGER_NOTICE` — that sentence reports a RUN, and a listing runs nothing. `INERT_TRIGGER_NOTICE` is itself untouched at "scheduler not yet available; ran on demand" and stays `remedy loop run`'s to display, printed off `outcome.notice` rather than off the constant. The pin is NEGATIVE, so the defect cannot drift back unnoticed: `test_a_schedule_trigger_loop_is_listed_and_marked_inert` in `tests/cli/test_loop_cmd.py` asserts `INERT_TRIGGER_NOTICE not in out` over the WHOLE listing output, while `test_running_an_inert_loop_prints_the_run_notice_and_still_stops_at_planned` still asserts the notice IS present on the run path — the two claims the feature actually distinguishes. The reviewer red-proved the pin in its own disposable worktree at a85a92d9 instead of trusting the colour: an import probe printed the module under `.remedy-wt/f045_r12_rev`, so the probe cannot have imported the fixed code (finding R-0337), and with the legend set back to the notice's literal text the listing test failed at its own `assert INERT_TRIGGER_NOTICE not in out`, reaching that assertion rather than dying earlier on something else. The worktree was removed and pruned before this verdict.
<<< DONE-355 <<<

>>> DONE-356 >>>
Done: R-0356 — RESOLVED at the R12 gate. Verified against the disk, not the report: `docs/agents/planner_reviewer_prompt.md` §3 carries checklist item 10, "The open-finding set is recomputed, never carried forward", which orders the set derived mechanically from `.agent/live_review.md` at emission — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — and names each finding explicitly rather than by position. Its load-bearing clause is the one that separates it from R-0354's counter-measure and is the whole reason this finding existed: naming findings explicitly is NOT sufficient on its own, because two consecutive blocks did exactly that and were both still wrong, each having taken its set from the PREVIOUS block instead of from the record. The reviewer applied item 10 before authoring the R12 block rather than after: the recomputed set at this gate is R-0350, R-0353, R-0354, R-0355 and R-0356 — five, not the three the R9 block carried forward.
<<< DONE-356 <<<

Commit C1 alone. Subject: `docs(f045): close R-0353, R-0355 and R-0356 at the R12 gate`

── C2 — the pipeline inventory ────────────────────────────────
Write a NEW file `.agent/f045_e2e_inventory.md`. It is a SURVEY: it records
what the code already does. It answers the six questions below, and for each
one it records the REAL command you ran and its REAL output (trimmed to what
is load-bearing, never invented, never paraphrased as "green"). Where the
answer is "nothing does this", say so and show the command whose empty output
proves it.

  Q1. How does a job that is in state PLANNED actually get EXECUTED through
      the standard pipeline? Name the entry-point function and its module, and
      name ONE existing test that drives a job through it end to end.
  Q2. What is the fake provider? Name its module and the exact mechanism a
      test uses to select it instead of a real provider (env var, fixture,
      argument — whichever it really is).
  Q3. Where, if anywhere, does `job.metadata` reach EVIDENCE? Name the writer
      function, its module, and the on-disk artifact path it produces.
  Q4. Where, if anywhere, does `job.metadata` reach the REPORT? Name the
      function in `packages/orchestration/run_report.py` that would carry it.
  Q5. Does anything today carry `loop_ref` into evidence or into the report?
      Show the grep and its real output.
  Q6. What is the SMALLEST change that would make `loop_ref` visible in
      evidence and in the report — which file, which function, roughly what
      shape? Describe it only. Write NO code and change NO production file.

Constraints on C2: every `file:line` you cite must be produced by a command in
this round, not remembered. Prefer naming the SYMBOL plus its distinguishing
text over a bare line number. Do not speculate about behaviour you did not run
or read; "not determined" is an acceptable answer and is better than a guess.

Commit C2 alone. Subject: `docs(f045): inventory the pipeline for the loop e2e round`

── C3 — plan and handoff ──────────────────────────────────────
Replace `.agent/plan.md` ENTIRELY with the authored text between the PLAN
markers, byte for byte, from your saved copy. It is 48 lines; the AGENTS.md cap
is 50.

>>> PLAN >>>
# Plan — F045 Loop definitions

Branch: feature/f045-loop-definitions, cut from main at cb3ef34f. No PR open;
nothing merged this round. Next free finding ID: R-0357. Open findings: 2 —
R-0350 and R-0354 — RECOMPUTED this round from `.agent/live_review.md` (every
`^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line), never carried
forward from the previous plan. R-0353, R-0355 and R-0356 were closed at the
R12 gate by reviewer-authored `Done:` text.

## Goal
Recurring work gets a declarative, versionable form: a LOOP defines trigger,
scope, action, budget and stop rules in the project's config file, and
`remedy loop run` executes one as a completely normal job/mission with loop
provenance in evidence. DONE when a fixture loop validates, runs through the
standard pipeline unchanged, and an invalid spec fails validation with precise
messages before anything runs (docs/roadmap/features/T2_F045.md).

## Current Step
R12, bookkeeping plus the ground survey T003's last item needs. The CLI is
complete — `loop list`, `loop validate`, `loop run <name> [--yes]` — and
`loop_ref` reaches `job.metadata`, but it appears in no evidence writer and no
report builder, so the feature file's Acceptance line "loop_ref visible in
evidence and report" is NOT met yet. This round writes no production code: it
closes three findings and inventories the fake-provider pipeline into
`.agent/f045_e2e_inventory.md` so the next round can author the end-to-end
fixture test from measured facts instead of from assumptions.

## Next Steps
1. R13: the end-to-end fixture loop through the fake-provider pipeline, built
   on the inventory — a loop materializes a job, the job runs, and `loop_ref`
   is visible in evidence and in the report.
2. The integration gate (docs/agents/integration_gate.md).
3. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Loops are parsed from a config file that does not exist in this repo (no
  ./remedy.toml). Every test builds its own tmp config; nothing may depend on
  a repo-level config file appearing.
- Schedule and event triggers are parsed and validated but INERT until the
  scheduler feature. `loop run` says so off `LoopRunOutcome.notice`.
- `loop run` writes to the REAL job store unless given `root`, so every test
  isolates through `REMEDY_DATA_DIR` or an explicit root.
- Surfacing `loop_ref` in evidence and report may need production changes in
  modules F045 has not touched; R13 must size that before ordering it.
- This branch has carried no PR across several sessions. Whether to open one is
  the operator's call; this session did not make it either way.

Fortschritt: ~65 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
<<< PLAN <<<

Then rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It is
YOURS to write, not authored here. It must carry: feature and round, branch,
base SHA (a85a92d9), the per-commit table, the gate table below with REAL exit
codes and REAL output, the item-status table (AGENTS.md), the open-findings
count, and the next expected action. Its last line repeats the Fortschritt line
from the plan verbatim. Cap is 60 lines; if the MANDATED content genuinely does
not fit, exceed it and carry a "Deviations, declared" line naming the actual
line count and the specific mandated content that caused it. Never drop a
section to meet the cap.

Commit C3 alone. Subject: `docs(f045): hand back R12 with the pipeline inventory`

── Constraints ────────────────────────────────────────────────
- AGENTS.md governs everything here. Self-review loop before EVERY commit.
- Push after each commit: `git push -u origin feature/f045-loop-definitions`.
- Never work on main. Never force-push. Never merge. Never create a PR.
- Any destructive or mutation check runs ONLY inside a disposable
  `git worktree` under `.remedy-wt/`, never in the primary checkout, and the
  worktree is removed and pruned before you hand back. Writes to /tmp are
  denied in this environment.
- The authored texts (DONE-353, DONE-355, DONE-356, PLAN) are applied byte for
  byte from your saved `.agent/authored/f045-r12.md`. No trailing whitespace on
  any line you write.
- If a gate goes red, or you find a contradiction, or something here is
  ambiguous: STOP, commit nothing further, and report it in full. Do not guess
  and do not widen scope to route around it. A round that halts with an honest
  report is a success.
- Do not write a `Done:` paragraph of your own for anything. If a fix of yours
  lands that needs recording, use `Landed: R-XXXX — <one line>` instead.

── Done when ──────────────────────────────────────────────────
Run every gate below and record its REAL exit code and REAL output.
Re-run (d), (g) and (h) AFTER the final commit.

  (a) cmp .agent/authored/f045-r12.md .agent/last_block.md
      → exit 0, byte-identical.
  (b) The open-finding set, recomputed from the record after C1:
      python3 - <<'EOF'
      import re
      lines=open('.agent/live_review.md').read().splitlines()
      reg=[m.group(1) for l in lines if (m:=re.match(r'^- (R-\d+) — ',l))]
      done=[m.group(1) for l in lines if (m:=re.match(r'^Done: (R-\d+) — ',l))]
      print("OPEN",sorted(set(reg)-set(done)))
      EOF
      → must print exactly: OPEN ['R-0350', 'R-0354']
  (c) The three authored lines land intact: each of DONE-353, DONE-355 and
      DONE-356 appears EXACTLY ONCE among the lines C1's diff ADDS
      (`git show --numstat` for the total, plus a per-line count over that
      diff's added lines). C1's numstat for `.agent/live_review.md` is
      6 insertions, 0 deletions.
  (d) git diff --name-only a85a92d9..HEAD
      → exactly the five files named in Change, and nothing else.
  (e) python3 -m pytest tests/ui_server/test_dashboard_contract.py -q
      → the `.agent` state-file contract, which reads live_review.md and
      plan.md. Report the real counts.
  (f) python3 -m pytest tests/cli/test_loop_cmd.py tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q
      → the F045 suite. Report the real counts.
  (g) python3 -m pytest tests/cli/test_golden_path.py -q   (the canary)
      → report the real counts.
  (h) git status --porcelain  → EMPTY.
  (i) git worktree list       → exactly ONE line, the primary checkout.
  (j) No trailing whitespace on any line of the files this round writes:
      grep -rn ' $' .agent/authored/f045-r12.md .agent/live_review.md .agent/plan.md .agent/f045_e2e_inventory.md .agent/last_block.md .agent/handoff.md
      → no output.
  (k) gh pr list --state open --json number,headRefName  → [].

Handback:    the completion report plus the rewritten `.agent/handoff.md`.
             The report states, for each gate, the command, the exit code and
             the real output. "Green" as a word is not a result.
──────────────────────────────────────────────────────────────
