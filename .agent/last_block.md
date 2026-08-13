── STEP R5/n — F115 Prompt breakdown & cost report · Round 5 ─────────
Goal:        Persist what the R4 gate produced: register the reviewer's own
             gate-arithmetic error as R-0323, and record the planner call
             site's shape as DECISION F115 D2 so the next session orders its
             wiring from disk instead of re-deriving it.
Bundle:      C1a save this block · C1b mirror it · C2 register R-0323 ·
             C3 record DECISION F115 D2 · C4 plan + handback
Change:      EXACTLY these paths:
               .remedy-wt/f115-r5-1.md     (source, gitignored, NOT committed)
               .agent/authored/f115-r5-1.md (new, C1a)
               .agent/last_block.md         (rewrite, C1b)
               .agent/live_review.md        (C2: append)
               .agent/decisions.md          (C3: append)
               .agent/plan.md               (C4: full replace)
               .agent/handoff.md            (C4: rewrite)
             NO source file and NO test file this round.
Constraints:
  - TEXT-A, TEXT-B and TEXT-C are AUTHORED text. Apply them byte for byte. Do
    not reword, rewrap or re-punctuate. No placeholder slots: substitute
    nothing.
  - Do NOT write a `Done:` paragraph and do NOT mark R-0323 resolved. It is
    registered OPEN in the same round it is discovered; only reviewer-authored
    text at a later gate may resolve it
    (docs/agents/planner_reviewer_prompt.md §4.4).
  - Do NOT fix R-0320 or R-0322. Both are inherited from before this branch and
    neither is an F115 defect; AGENTS.md bars mixing an unrelated fix into a
    feature branch.
  - Do NOT touch `apps/cli/commands/job.py`, `packages/orchestration/
    llm_planner.py` or `packages/orchestration/structured_planner.py` this
    round. C3 RECORDS the decision; the wiring is a later round.
  - Never force-push. Never commit on main. Push after EVERY commit (R-0289).
  - Do NOT create a pull request this round.
Done when: every command has been RUN for real and its TRUE output recorded. A
           guessed, expected or remembered value is a finding.
  a. `cmp .agent/authored/f115-r5-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. After C2: `grep -c '^- R-0323' .agent/live_review.md` prints 1 ·
     `grep -c '^- R-0' .agent/live_review.md` prints 4 (it was 3) ·
     `grep -c '^Done:' .agent/live_review.md` prints 1 (unchanged) ·
     `grep -c '^## Steps' .agent/live_review.md` prints 1 (the §4.11 contract
     substring survives the append).
  c. After C3: `grep -c '^## DECISION F115 D2' .agent/decisions.md` prints 1.
  d. Canary and docs: `python3 -m pytest tests/cli/test_golden_path.py -q`
     (measured baseline at this branch head: `42 passed`) and
     `python3 -m pytest tests/docs/ -q` (baseline `294 passed`). Record both
     tails and exit codes. Neither should move; if either does, STOP and hand
     back rather than adjusting an authored text to suit a test.
  e. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real number.
  f. `git status --porcelain` empty; `git diff --name-only 0d6c97aa..HEAD`
     lists the SIXTEEN paths present at R4 plus this round's ONE new path
     (`.agent/authored/f115-r5-1.md`) and `.agent/decisions.md`, which is NOT
     yet among them — EIGHTEEN in total. Count them with
     `git diff --name-only 0d6c97aa..HEAD | wc -l` and record the real number;
     if it is not 18, report the real number and the actual list rather than
     changing anything. `.remedy-wt/**` must NOT appear.
     `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
     prints 0 and 0 after the final push.
Handback:  completion report + rewrite `.agent/handoff.md`. Item-status table
           (C1a, C1b, C2, C3, C4 — each exactly once), commit table with real
           SHAs and insertions, changed-files table, every result a-f as a REAL
           value. Repeat the Fortschritt line verbatim. Over 60 lines ⇒ carry a
           "Deviations, declared" line naming the count and the mandated
           content that caused it (AGENTS.md DECISION D15).

           THIS IS THE LAST ROUND OF THE SESSION. The handoff is the only
           return channel, so make it the one a cold reader can resume from:
           name the branch, the head SHA, the last reviewed SHA (19b59ccc, R4
           PASS), the open findings and their state, and that the PLANNER call
           site is the next work with DECISION F115 D2 already recording its
           shape. Do NOT create a PR.
──────────────────────────────────────────────────────────────────────

PROCEDURE

C1a `chore(f115): save the R5 step block verbatim` — copy the reviewer's
    scratchpad original `.remedy-wt/f115-r5-1.md` to
    `.agent/authored/f115-r5-1.md`. Copy the FILE; do not retype it.
C1b `chore(f115): mirror the R5 block into last_block` — copy that same file to
    `.agent/last_block.md`. Run gate (a).

C2 `chore(f115): register R-0323 for the R4 gate arithmetic`
    Append TEXT-A to the END of `.agent/live_review.md`. Run gate (b).

C3 `docs(f115): record the planner call site shape as DECISION D2`
    Append TEXT-B to the END of `.agent/decisions.md`. Run gate (c).

C4 `chore(f115): refresh the plan and write the R5 handoff`
    `.agent/plan.md` ← TEXT-C in full, then rewrite `.agent/handoff.md`.
    Run gates (d), (e), (f).

TEXT-A — append to the END of .agent/live_review.md

- R-0323 — Low — reviewer gate arithmetic, self-registered. The R4 block's gate
  (f) demanded that `git diff --name-only 0d6c97aa..HEAD` list SEVENTEEN paths
  — "the fifteen of R1-R3 plus this round's two new ones
  (`.agent/authored/f115-r4-1.md`, `tests/orchestration/test_prompt_trace.py`)".
  `tests/orchestration/test_prompt_trace.py` was ALREADY one of those fifteen:
  R2 added the builder behaviour test and its wiring guard to that same file,
  and `git diff --name-only 0d6c97aa..8601e276` lists it. Only one path was new
  in R4, so the reachable total was SIXTEEN and the ordered seventeen was
  unmeetable by construction. The worker measured 16, reported it, changed
  nothing to meet the number, and declared the deviation — the correct
  behaviour, and the round cost one declared deviation to prove a reviewer
  slip. Same class as R-0282 (F107 R11, "exactly these nine paths" over a list
  of eight) and R-0321 (F115 R1, "four of the eight" over a list of seven);
  three instances now, all of them a count stated in prose that the reviewer
  never re-derived from the list beside it. The standing counter-measure is
  already on disk as checklist item 8
  (`docs/agents/planner_reviewer_prompt.md`, added at 43763bf4) — it says to
  compute a gate's expected value from the source that PRODUCES it. A path
  count's source is the previous round's own `git diff --name-only` output,
  which the reviewer had already run in that same session and did not re-read.
  No fix is possible on disk: the block is committed verbatim by design and
  R4's verdict already stands as PASS. It is registered so the pattern is
  countable rather than forgotten. OPEN.

TEXT-B — append to the END of .agent/decisions.md

## DECISION F115 D2 (2026-08-13) — the planner call site needs a COMPOSER built, not a composition threaded

Context: F115 D1 committed to wiring the three unwired `build_trace_entry` call
sites through the prompt-segment registry so live ledger rows stop resolving to
an empty manifest. Two are done — the builder at `pingpong_loop.py:2795` (R2)
and the reviewer at `pingpong_loop.py:2987` (R4). Both were mechanical: a
`compose_*_prompt` function already existed beside the call site, the legacy
`_build_*_prompt` wrapper already returned `compose_*_prompt(...).text`, and
the round only had to compose at the call site and hand the `ComposedPrompt`
to the trace entry. The sent bytes could not change, and the goldens proved it.

The planner site is NOT that shape, and this is recorded before it is ordered
so no round discovers it mid-flight. The facts, read at the F115 R5 gate:

* The trace entry is built at `apps/cli/commands/job.py:236`, inside the
  `_record_plan_call` callback, from an `effective_prompt` STRING.
* That string arrives through `make_structured_planner`
  (`packages/orchestration/structured_planner.py:59`), whose contract is
  `on_call(attempt, schema_v, is_parse_retry, effective_prompt)`
  (`structured_planner.py:68`) — a string, by design, because the engine is
  provider-agnostic and driven by an injected `call_fn`.
* The prompt itself is built in `plan_job_with_llm` at
  `packages/orchestration/llm_planner.py:107-109`: `prompt = job.user_prompt or
  job.name`, then `prompt = f"{prompt}\n\n{memory_section}"` when recalled
  memory exists. It is two concatenated parts and nothing else.
* There is NO composer to reuse: `grep -c 'ComposedPrompt'
  packages/orchestration/llm_planner.py` prints 0. Unlike the builder and the
  reviewer, no registry-backed function exists to call.

Chosen: a later round BUILDS `compose_planner_prompt` in `llm_planner.py` over
the two parts that already exist — the job prompt at TASK rank and the recalled
memory section at JOB_CONTEXT rank — and threads the resulting `ComposedPrompt`
out to `_record_plan_call` through an explicit optional hook on
`plan_job_with_llm`, leaving `call_planner` still receiving the same string.
The sent bytes stay identical because `compose_prompt_segments` joins with the
two-character `PROMPT_SEGMENT_DELIMITER` (`prompt_segments.py:188`), which is
exactly the `\n\n` the current concatenation already uses — that identity is
the round's first gate, not an assumption, and if it does not hold the round
stops rather than changing what the planner sends.

Alternatives considered: (a) widen `on_call` to carry a `ComposedPrompt` —
rejected, it changes a provider-agnostic engine contract for one caller's
telemetry; (b) compose in `job.py` instead, duplicating the prompt assembly at
the CLI — rejected, two places would build the planner prompt and could drift,
which is the exact failure `_build_reviewer_prompt` was collapsed into
`compose_reviewer_prompt` to prevent; (c) accept a permanently empty planner
manifest and report those rows "unattributed" — rejected as the default, but it
remains the honest fallback if the byte-identity gate fails, and F115 already
owes "unattributed" rendering for historical rows regardless.

Reverse this decision by deleting this entry. Nothing in the tree depends on it
yet: it is a plan for a round that has not run.

TEXT-C — the complete new .agent/plan.md

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged at the Open PR Gate. Last reviewed SHA: 19b59ccc (R4 PASS).
Next free finding ID: R-0324. Open findings: 3 — R-0320 (Low, carried
from F111), R-0322 (Medium, inherited suite red, not an F115 defect),
R-0323 (Low, reviewer gate arithmetic, no fix possible on disk).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R5 done — housekeeping only, no source or test file touched. R-0323 is
registered and the planner call site's shape is on disk as DECISION
F115 D2, so the next round orders its wiring from the record.

## Next Steps
1. The PLANNER call site, per DECISION F115 D2: build
   `compose_planner_prompt` in `llm_planner.py` over the two existing
   parts, thread the `ComposedPrompt` to `_record_plan_call` through an
   optional hook, and gate on byte-identity of the sent prompt FIRST.
2. T001 proper — persist the manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
3. T002 — aggregation queries plus the pure renderer, with goldens;
   follow `gauntlet_matrix.py` and `tests/cli/test_stats_cost.py:49-128`.
4. T003 — CLI, prior-period comparison, json schema; then the
   integration gate and closure.

## Risks
- The per-role breakdown has one bucket until `role` stops being
  hardcoded, and per-task-class has no source at all. Both are recorded
  in the feature file; F115 must report "no data", never a fake bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 30 % (R1 ✅ · T001a ✅ · Reviewer-Site ✅ · Planner-Site · T001 · T002 · T003 offen) — Schätzung
