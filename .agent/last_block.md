── STEP R2/7 — F082 Self-benchmark (record R1, then the T001 inventory) ──
Goal:        Record the R1 gate and register R-0404, then inventory the
             gauntlet harness read-only so R3 knows exactly what it may
             reuse, what it must derive, and what it may not move.
Bundle:      C0a/C0b save this block · C1 the R1 verdict, R-0404 and the plan
             re-sync, findings persisted FIRST · C2 the inventory · C3 handback.
Change:      .agent/live_review.md, .agent/plan.md, .agent/context.md,
             .agent/f082_inventory.md (NEW), .agent/authored/f082-r2.md,
             .agent/last_block.md, .agent/handoff.md. NOTHING under packages/,
             apps/, tests/ or docs/. This round READS production code and
             writes no line of it.
Constraints: Findings persist FIRST, in their own commit, before the inventory
             (planner_reviewer_prompt.md §4 item 4). Never write a `Done:` or
             `Landed:` paragraph of your own. Every authored slice is applied
             disk-to-disk out of the COMMITTED block file, never retyped.
             Push after every commit. Never merge, never force-push, never
             work on main. Answer only what you VERIFIED in the source; an
             honest "not present" is a valid answer and a guess is a finding.
Done when:   the gates at the end of this block all pass, with their real
             values reported.
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────────────

── C0 — save the block, in TWO commits ───────────────────────────────
The reviewer's scratchpad original is at `.remedy-wt/f082-r2-scratchpad.md`.
Saving it to both targets in ONE commit costs roughly twice its line count in
insertions and crowds the 500-insertion cap (AGENTS.md Commit Discipline;
findings R-0381 and R-0399). Split it unconditionally — the split is never
wrong and costs one cheap commit — and retype neither target:

C0a. Copy the scratchpad byte for byte to `.agent/authored/f082-r2.md`.
     Commit that file ALONE.
     Subject: `chore(f082): save the R2 inventory block verbatim`

C0b. Copy the COMMITTED `.agent/authored/f082-r2.md` — not the scratchpad —
     byte for byte to `.agent/last_block.md`. Commit that file ALONE; it is
     the verbatim rewrite of a single `.agent/**` state file, exempt from the
     churn reading under DECISION F104 D1.
     Subject: `chore(f082): mirror the R2 block into last_block`

── C1 — the R1 verdict, R-0404, and the plan re-sync ─────────────────
All three in ONE commit, and it is the FIRST commit after C0.
  Subject: `docs(f082): record the R1 verdict and register R-0404`

C1a. `.agent/live_review.md`. APPEND ONLY. Append, in this order, to the end
of the file: one blank line, the FINDING-R404 slice as ONE physical line, one
blank line, the GATE-R1 slice as ONE physical line. Nothing above the append
may move: prove it with `cmp` against the pre-C1 revision over the file's
existing line count. Both slices are single lines — if your editor wraps
either one, the round is wrong; extract them with a script, never by hand.

C1b. `.agent/plan.md`. FULL REPLACEMENT with the PLAN slice below.

C1c. `.agent/context.md` is named in this change set under R-0377's widened
counter-measure, which binds any round whose outcome changes what a state
mirror asserts. Check it rather than rewriting it: `.agent/context.md` states
NO finding count and NO next-free id — those live in `.agent/plan.md` and
`.agent/live_review.md` — and its `## Steps` line already carries R2 as the
inventory round. If both checks hold, leave the file untouched and say so in
the handback; that is a re-sync with an empty delta, not a skipped item. If
either check fails, STOP and hand back rather than inventing an edit.

--- BEGIN SLICE FINDING-R404 ---
- R-0404 — Low — the R1 handback states a file count that the branch's own diff contradicts, one round after the identical class was registered as R-0402. `.agent/handoff.md` gate line 14 reads "Branch touches 7 files, all under `.agent/` plus the one STATUS line", while `git diff --name-only 668d40f7..HEAD` returns EIGHT paths: `.agent/authored/f082-r1.md`, `.agent/candidates.md`, `.agent/context.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and `docs/roadmap/STATUS.md`. Exactly seven of those sit under `.agent/`, so the sentence is recoverable under the reading "seven `.agent/` files, plus the one STATUS line" — but its plain reading is a total, and as a total seven is wrong; the two clauses do not agree, which is the R-0331 class as much as the R-0402 one. Nothing downstream is affected and no verdict changes: the gate the sentence decorates is `git diff --stat 668d40f7..HEAD -- packages/ apps/ tests/`, the reviewer re-ran it independently and it is EMPTY, so no production file was touched and the change set really is the one the block named. It is registered rather than corrected in passing because R-0402 recorded this exact failure — a numeral written beside an enumeration without counting the enumeration — at the close of the previous feature, and a recurrence in the very next round is evidence that the lesson has not landed. The counter-measure, binding from R2 on: any sentence in a handback or block that pairs a numeral with an enumeration either counts that enumeration mechanically first, or states no numeral at all. OPEN.
--- END SLICE FINDING-R404 ---

--- BEGIN SLICE GATE-R1 ---
Gate: R1 — PASS, with one new finding. Verification tier: round gate plus the docs gate plus the state-file contract readers plus the canary; no full-suite claim is made. Every one of the fifteen ordered gates was re-executed by the reviewer against the disk rather than read out of the handback, and every one reproduces. The Open PR Gate is correct: this session's Phase 1 merged PR #200 as `668d40f7ca691ba25e5293157651ddca853bbd4f`, `gh pr list --state open` now returns `[]`, and that same SHA is both the current `main` head and `git merge-base main HEAD`, so the branch is cut from the merge and no history was rewritten; A0 was confirmation only and the worker merged nothing. Transport: `cmp` holds twice, scratchpad to `.agent/authored/f082-r1.md` and that file to `.agent/last_block.md`, at shared sha256 `654ab8c91bbc43adf2a8b6af13f65dd5a3e682cb4227680c44210f4c9dda0eb3`, 297 lines, inside the 400-line cap, and the digest equals the one the reviewer measured on its own bytes before emitting, so nothing mutated in delegation. All four whole-file slices were re-extracted by the reviewer from the COMMITTED block file and each applied target is byte-equal — CANDIDATES, PLAN and CONTEXT compare equal as whole files and LIVE-REVIEW-HEAD is the exact prefix of the new record — while the STATUS pair is a REWRITE and measures FROM 0x, TO 1x, with `^- \[~\]` totalling exactly 1 across the whole ledger. The carry was audited independently rather than accepted: the reviewer re-extracted the open set from `780d4181:.agent/live_review.md` with its own paragraph terminator, computed 32 open from 37 paragraph starts minus 5 `^Done:` ids, and every one of the 32 carried paragraphs is byte-identical in the new record with zero mismatches, no open id dropped and no unexpected id added; the five ids F077 resolved are correctly absent. The reviewer's own join digest is `1aeda83502244129f876a87e72b240db31e308a7286cea38957795cf2cf46a3d` over 56503 bytes against the worker's `6b154bc9c177db78c46da925e97ead90486dc46654b7a1471aef00ba7721f17f` over 56565 bytes; the two differ only in the separator each used to join the paragraphs, each is internally consistent across both sides of its own comparison, and the property proven — pre-reset equals post-reset — is identical, so no finding is spent on it. The open set recomputed from the new record is exactly THIRTY-THREE, the 32 carried plus R-0403, with zero `^Done:` and zero `^Landed:` lines, so the worker authored no resolution of its own, and no id appears twice. Suites re-run by the reviewer at the branch head: `tests/docs/` `295 passed`, the three state-file contract readers `142 passed` and the canary `tests/cli/test_golden_path.py` `42 passed` — each exactly the baseline the reviewer measured at `668d40f7` BEFORE authoring the block, so every ordered gate was known runnable and green at base and could have failed honestly. `python3 -m apps.cli.main integrity check --json` returns `passed: true`, `fail_count: 0` over 5 checks with `high_blockers_open` reporting no open blocker/high findings, and its `live_review_verdict` message now quotes the F082 header line, which independently confirms the reset landed and did not flip that check. `wc -l .agent/plan.md` is 37, under the 50-line cap; `git diff --stat 668d40f7..HEAD -- packages/ apps/ tests/` is EMPTY; `git status --porcelain` is empty and `git worktree list` is one line; a marker scan over all six edited files finds zero BEGIN/END and zero `>>>`/`<<<` lines, a trailing-whitespace scan finds none, and every file ends with a newline. Insertions per commit are 297, 288, 20, 58 and 59, none over 500 — the C0 split the block ordered is what kept the pair inside the cap, and R-0381's structural finding is the reason the split exists. Three deviations, all declared and all accepted: the handback is 89 lines against the 60-line cap carrying its DECISION D15 stated cause with no section dropped; the handoff's own commit row says "rewrite" rather than a numstat under the R-0149 exception, and the reviewer measured that commit independently at `+59/-92`; and the commit messages carry no trailer, matching every commit in this repository's history. One further observation costs no id: gate 1 reports `git worktree list` as it stood at ROUND START, showing `main 668d40f7`, where the gate asked for the value at handback — the property gated, exactly one worktree, holds at both moments and the reviewer verified it at HEAD, and the value is labelled with its moment rather than misrepresented, so it is corrected forward by wording R2's gate "at handback" instead of registering it. One finding IS registered against this round, R-0404 above, and it is the worker's: a file count in the handback's verification section that the branch's own diff contradicts. No block condition was hit — no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R1 ---

--- BEGIN SLICE PLAN ---
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0405. Open findings: thirty-four — the thirty-two carried from F077, plus
R-0403 registered at the claim and R-0404 registered at the R1 gate.
`.agent/live_review.md` is the source of truth for that ledger; this file
mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R2: the R1 gate is recorded, R-0404 registered, and the T001 gauntlet-harness
inventory is written read-only into `.agent/f082_inventory.md`.

## Next Steps
1. R3 — T001: the factoring the inventory justifies, the five frozen orders
   with their version tags, the record schema, and a dry run against recorded
   fixture evidence. The gauntlet's own seven test files stay UNMODIFIED.
2. R4 — T002: history append, trend computation, the regression rules and the
   improving, flat and degrading goldens.
3. R5 — T003: the `stats bench` CLI, model-context recording and a
   fake-provider bench run end to end.
4. R6 the integration gate, R7 closure.

## Risks
- The factoring in T001 is the feature file's own named risk. R2 answers what
  may move before anything moves; an answer of "cannot move without editing a
  gauntlet test" is a finding against the plan, not a licence to edit the test.
- Thirty-four open findings is the largest carry any feature has started with.
--- END SLICE PLAN ---

── C2 — the T001 inventory ───────────────────────────────────────────
File: `.agent/f082_inventory.md`, NEW. Read-only round: you may read any
source file, and you may write no line of production code.
  Subject: `docs(f082): inventory the gauntlet harness for the T001 factoring`

Answer each question below in its own section, in this order. Each answer's
heading is a level-two heading beginning with the question id and nothing
before it — `## Q1`, `## Q2`, … `## Q12` — because gate 15 counts them.
EVERY answer cites the file and the SYMBOL it rests on — `path.py::symbol` —
and quotes at most the two or three lines that settle it. Cite symbols, not
bare line numbers: a symbol survives an edit above it and a line number does
not (finding R-0353). Where a thing does NOT exist, say "not present" and name
where you looked; that is the most valuable answer in this file and a guess in
its place is a finding. Close the file with a short "What this means for R3"
section: what the bench REUSES unchanged, what it must FACTOR out, what it must
BUILD new, and what it must not touch.

Q1.  `packages/orchestration/gauntlet_runner.py::run_order` — its full
     signature, what it returns, and every field of `OrderOutcome` and
     `RunnerDeps`. This is the seam the bench runs through.
Q2.  Of the record the feature file requires — `{order_id, series, pass, cost,
     wall_s, repair_rounds, postmortem_classes}` — which fields already exist
     on `OrderOutcome` verbatim, which are derivable from what it returns, and
     which have no source at all today? Answer field by field.
Q3.  `packages/orchestration/gauntlet_orders.py::GauntletOrder` — its fields,
     how the order set is declared, and where the order files live. Is there
     any version or freeze tag on an order today? F082 requires one and
     requires that changing an order without bumping it FAILS validation.
Q4.  The pass definition in `packages/orchestration/gauntlet_evaluator.py` —
     name the symbol that decides pass/fail. F082's Do-not-touch list forbids
     changing it; the bench must call it or record around it. Which is
     possible without editing it?
Q5.  `gauntlet_runner.py::measure_tokens` — what it returns, and where cost in
     money or tokens actually comes from. Name the basis labels the repo
     already uses, since F082 compares cost only within the same basis.
Q6.  `gauntlet_runner.py::collect_postmortems` — its return shape, and what a
     postmortem "class" is called in that data. This feeds
     `postmortem_classes`.
Q7.  `repair_rounds`: does anything in the repo count repair rounds for a run
     today? If yes, name it. If not, say not present and name the nearest
     signal that could stand in.
Q8.  `wall_s`: does any existing outcome or evidence record carry wall-clock
     duration for an order? Name it or say not present.
Q9.  `gauntlet_matrix.py` and `gauntlet_evidence.py` — what evidence artefact
     a campaign produces today, and which function writes it. F082 wants "a
     full evidence bundle per run": can that be reused as-is?
Q10. `packages/orchestration/data_paths.py` — which helper yields the data
     root's PROJECT area, where the feature file puts `bench_history.jsonl`.
     Name any existing append-only `.jsonl` writer in the repo the bench
     should follow instead of inventing one.
Q11. The factoring risk, and the most important question here. For each of the
     SEVEN test files matching `tests/orchestration/test_gauntlet_*.py` and
     `tests/orchestration/test_self_run_gauntlet.py`, list which symbols it
     imports directly from the gauntlet modules. Then state plainly which
     symbols CANNOT be moved or renamed without editing one of those files.
     Count the files you actually list and state that count.
Q12. Model and routing context: where does the repo record which model served
     which role for a run? Name the symbol, or say not present. F082 only
     RECORDS this — changing routing is on the Do-not-touch list.

── C3 — handback ─────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Under 60
lines, or carry a DECISION D15 stated-cause line naming the real count and the
mandated content that caused it. Commit and push.
  Subject: `chore(f082): handback R2`

── Gates — run every one, report the REAL value ──────────────────────
1.  `git status --porcelain` → EMPTY at handback. `git worktree list` → 1 line;
    report the line AS IT READS AT HANDBACK, not at round start.
2.  `cmp` scratchpad↔`.agent/authored/f082-r2.md` and that file↔
    `.agent/last_block.md` → both exit 0. Report the shared sha256 and the
    line count; it must be at or under 400.
3.  `.agent/STOP` — report ABSENT or PRESENT at round start AND at handback.
4.  C1a append proof: `git show <pre-C1 SHA>:.agent/live_review.md` into a
    scratch file and `cmp` it against the first 91 lines of the new
    `.agent/live_review.md` → exit 0, proving nothing above the append moved.
    Report the C1 numstat for that path; its DELETION column must be 0.
5.  `grep -c "^Gate: R1 — PASS" .agent/live_review.md` → 1.
    `grep -c "^- R-0404 — " .agent/live_review.md` → 1.
    `grep -c "^## Steps" .agent/live_review.md` → 1.
    Report the physical line count of the GATE-R1 line and of the
    FINDING-R404 line; each must be exactly 1 line.
6.  Open set recomputed mechanically from the record — every
    `^- R-[0-9]\+ — ` paragraph minus every `^Done: R-[0-9]\+ — ` line. Expect
    exactly THIRTY-FOUR; name every id; report duplicates as none or name
    them. Report max id and next free id.
7.  `grep -c "^Landed: " .agent/live_review.md` → 0.
8.  `wc -l .agent/plan.md` → report it; must be under 50.
9.  C1c checks, reported as real greps: the count of "thirty-three",
    "thirty-four" and "R-040" in `.agent/context.md`, and its `## Steps` line
    quoted verbatim. State whether the file needed an edit and why.
10. `git diff --name-only 35838c5e..HEAD` → report every path. It must equal
    the block's Change list and contain no eighth path outside it. COUNT the
    paths mechanically and state the count you counted (finding R-0404).
11. `git diff --stat 35838c5e..HEAD -- packages/ apps/ tests/ docs/` → EMPTY.
    The base of this range is 35838c5e, the R1 handback commit — the SHA of
    the handback this round starts from, never the merge base (R-0368).
12. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0.
    Planner baseline at 35838c5e today: 42 passed. Report the real number.
13. `python3 -m pytest tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Planner baseline at
    that same commit today: 142 passed. Report the real number.
14. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`. Report the `high_blockers_open`
    message. The `remedy` entry point is denied to this session class.
15. Inventory completeness: `grep -c "^## Q" .agent/f082_inventory.md` → 12.
    Report the number of answers containing a `::` symbol citation and the
    number that answer "not present". Both are honest values, not targets.
16. Report each commit's `git show --numstat <sha>` insertion total. If any
    commit exceeds 500 insertions, declare it in the handback with the reason
    (AGENTS.md Commit Discipline) — do not silently pass it.

Transport proof: state, for each of FINDING-R404, GATE-R1 and PLAN, that it was
extracted from the COMMITTED `.agent/authored/f082-r2.md` and applied
disk-to-disk, with the slice's sha256 and byte length, and the proof that the
applied region equals it. Confirm no BEGIN/END marker line reached any target
file. Scan every file you touched for trailing whitespace and report the result.
