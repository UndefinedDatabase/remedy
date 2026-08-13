── STEP T001a/n — F115 Prompt breakdown & cost report · Round 2 ──────
Goal:        Make the feature's central premise TRUE at the builder call site:
             register finding R-0321, amend the feature file with DECISION D1
             (the premise is false as written and this is the chosen repair),
             then route the builder prompt through `compose_builder_prompt` so
             its trace entry carries a real segment manifest instead of an
             empty one — with the sent bytes provably unchanged.
Bundle:      C1a save this block · C1b mirror it · C2 register R-0321 ·
             C3 feature-file DECISION D1 · C4 wire the builder site ·
             C5 the manifest test + red-proof · C6 plan + handback
Change:      EXACTLY these paths:
               .agent/authored/f115-r2-1.md          (new, C1a)
               .agent/last_block.md                  (rewrite, C1b)
               .agent/live_review.md                 (C2: one append)
               docs/roadmap/features/T2_F115.md      (C3: one appended section)
               packages/orchestration/pingpong_loop.py (C4: the builder site)
               tests/orchestration/test_prompt_trace.py (C5: new tests)
               .agent/plan.md                        (C6: full replace)
               .agent/handoff.md                     (C6: rewrite)
             Do NOT touch the reviewer site, `job.py`, the ledger, the CLI, or
             any golden fixture. Do NOT edit `_build_builder_prompt` itself.
Constraints:
  - TEXT-A, TEXT-B and TEXT-C are AUTHORED text. Apply them byte for byte. Do
    not reword, rewrap or re-punctuate. No placeholder slots: substitute
    nothing, anywhere. If one looks wrong, apply it anyway and declare it.
  - Do NOT write a `Done:` or `Landed:` paragraph of your own.
  - THE SENT BYTES MUST NOT CHANGE. `compose_builder_prompt(...).text` is
    exactly what `_build_builder_prompt(...)` returns — the suite already pins
    that equivalence at
    `tests/orchestration/test_builder_prompt_golden.py:254`. The builder
    provider must receive the identical string it receives today, and
    `result.builder_prompt_chars` / `repair_prompt_chars` must be computed from
    that same string. A change in emitted bytes is a failed round, not a
    trade-off.
  - `_build_builder_prompt` stays exactly as it is and keeps its callers. You
    are changing ONE call site, not the helper. Its docstring already names
    this exact caller: "a caller that needs the segment manifest calls that
    instead of re-splitting this string" (`pingpong_loop.py:955-957`).
  - The red-proof in gate (f) is DESTRUCTIVE. Run it ONLY inside a disposable
    `git worktree`, never in the primary checkout, and remove the worktree
    before handback (AGENTS.md; planner_reviewer_prompt.md §4.10). The primary
    checkout satisfies `git status --porcelain` == empty at handback.
  - Never force-push. Never commit on main. Push after EVERY commit (R-0289).
  - Do NOT create a pull request this round.
Done when: every command has been RUN for real and its TRUE output recorded. A
           guessed, expected or remembered value is a finding.
  a. `cmp .agent/authored/f115-r2-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. After C2: `grep -c '^- R-0321' .agent/live_review.md` prints 1,
     `grep -c '^- R-0' .agent/live_review.md` prints 2,
     `grep -c '^Done:' .agent/live_review.md` prints 0.
  c. After C3: `grep -c 'DECISION F115 D1' docs/roadmap/features/T2_F115.md`
     prints 2 — TEXT-B carries the marker twice on purpose, in its heading and
     at the decision itself, and the file contained it zero times before this
     round. Also `python3 -m pytest tests/docs/ -q` is green (the change set
     includes docs/roadmap/**, so this gate is mandatory). Record tail and exit.
  d. After C4, the BYTES-UNCHANGED proof, which is the round's load-bearing
     gate. Run the two prompt goldens and the builder-loop suites:
     `python3 -m pytest tests/orchestration/test_builder_prompt_golden.py
     tests/orchestration/test_reviewer_prompt_golden.py
     tests/orchestration/test_builder_repair_loop.py -q`.
     Record tail and exit code. Then confirm by reading the diff that the
     string handed to the provider and the string measured by
     `builder_prompt_chars` are the SAME object or the same `.text` value —
     quote the three relevant lines of your own diff in the handback.
  e. After C5: the new tests pass. TWO tests are required, because they prove
     two different things and one cannot cover the other.
     e1 BEHAVIOUR — on a real `compose_builder_prompt` result,
        `build_trace_entry` produces an entry whose `segment_manifest` is
        NON-EMPTY, whose entries carry
        `name`/`rank`/`sha256`/`chars`/`tokens_estimated`, and whose
        `segment_manifest_chars` equals the sum of the entries' `chars`.
     e2 WIRING GUARD — that the builder call site itself is wired. Follow the
        precedent already in this file:
        `test_every_cli_call_site_hands_its_composition_down`
        (`tests/orchestration/test_prompt_trace.py:336`) and
        `test_the_replan_path_records_and_appends_its_traces` (`:327`) both
        read `inspect.getsource(<module>)` and assert on the call site. Do the
        same for `packages.orchestration.pingpong_loop`: assert the builder
        site composes ONCE and hands that composition to `build_trace_entry`.
        e1 alone cannot fail when the call site is unwired — it never touches
        `pingpong_loop` — which is exactly why e2 exists.
     Add both to `tests/orchestration/test_prompt_trace.py`. Record the node
     ids you added and the real pass count.
  f. RED-PROOF, in a disposable worktree only, run as a PROBE — report the
     real colour, do not assume it. Inside the worktree, revert the C4 call
     site to `_build_builder_prompt` (drop the `composed_prompt=` argument),
     then run BOTH new tests and record, separately for each, whether it
     FAILED or PASSED:
       - e2 is expected to FAIL. If it passes, the guard does not guard and
         you must say so plainly rather than dress it up.
       - e1 is expected to PASS unchanged, because it tests the function and
         not the call site. That is not a defect; record it as the reason e2
         is required.
     Then remove the worktree and record `git worktree list` showing only the
     primary checkout.
  g. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q`. Record tail
     and exit code.
  h. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real number.
  i. `git status --porcelain` empty; `git diff --name-only 0d6c97aa..HEAD`
     lists ONLY the nine R1 paths plus this round's four new ones and nothing
     else; `git rev-list --left-right --count
     origin/feature/f115-prompt-cost-report...HEAD` prints 0 and 0 after the
     final push.
  j. REPORT, do not fix: the reviewer call site (`pingpong_loop.py:2982-3031`)
     wraps its composed text in `_reviewer_effective_prompt`
     (`pingpong_loop.py:2088`), which can append a hint, so the traced text is
     not always the composed text. State in the handback, with line numbers,
     whether the hint is empty on the first attempt and where a non-empty hint
     comes from. This is R3's decision and you must NOT wire the reviewer site
     this round.
Handback:  completion report + rewrite `.agent/handoff.md`. Item-status table
           (C1a, C1b, C2, C3, C4, C5, C6 — each exactly once), commit table
           with real SHAs and insertions, changed-files table, every result
           a-j as a REAL value. Repeat the Fortschritt line verbatim. Over 60
           lines ⇒ carry a "Deviations, declared" line naming the count and the
           mandated content that caused it (AGENTS.md DECISION D15).
──────────────────────────────────────────────────────────────────────

PROCEDURE

C1a `chore(f115): save the R2 step block verbatim` — copy the reviewer's
    scratchpad original `.remedy-wt/f115-r2-1.md` to
    `.agent/authored/f115-r2-1.md`. Copy the FILE; do not retype it.
C1b `chore(f115): mirror the R2 block into last_block` — copy that same file to
    `.agent/last_block.md`. Run gate (a).

C2 `chore(f115): register R-0321 from the R1 gate`
    Append TEXT-A to the END of `.agent/live_review.md`. Run gate (b).

C3 `docs(f115): correct the manifest premise and record DECISION D1`
    Append TEXT-B to the END of `docs/roadmap/features/T2_F115.md`, after the
    last existing section, separated by one blank line. Run gate (c).

C4 `feat(f115): give the builder trace entry its segment manifest`
    ONE change at ONE call site in `packages/orchestration/pingpong_loop.py`.
    Read `compose_builder_prompt` (`:851`), `_build_builder_prompt` (`:942`),
    the call site (`:2792`), the char accounting (`:2815-2819`) and the trace
    entry (`:2824-2840`) before you touch anything.
    Replace the `_build_builder_prompt(...)` call at `:2792` with
    `compose_builder_prompt(...)` — the argument list is the same — bind the
    result to a clearly named local (e.g. `builder_composed`), and derive the
    prompt string from it ONCE (`builder_prompt = builder_composed.text`).
    Everything downstream keeps using `builder_prompt` unchanged. Add
    `composed_prompt=builder_composed,` to the `build_trace_entry(...)` call.
    That is the whole change: one new local, one changed callee, one new
    keyword argument. Run gate (d).

C5 `test(f115): pin the builder trace manifest and its wiring`
    Add BOTH tests (e1 behaviour, e2 wiring guard) to
    `tests/orchestration/test_prompt_trace.py` per gate (e). Read the file's
    existing style first and follow it — inline constants, no new fixture
    files; the two `inspect.getsource` guards at `:327` and `:336` are the
    pattern for e2. Then run the red-proof probe, gate (f), in a disposable
    worktree.

C6 `chore(f115): refresh the plan and write the R2 handoff`
    `.agent/plan.md` ← TEXT-C in full, then rewrite `.agent/handoff.md`.
    Run gates (g), (h), (i).

TEXT-A — append to the END of .agent/live_review.md

- R-0321 — Low — `.agent/f115_inventory.md` says "only four of the eight
  `build_trace_entry` call sites pass `composed_prompt`". The count of
  non-test call sites is SEVEN, not eight: `intake.py:135`,
  `flight_plan.py:181`, `orchestrator_loop.py:920`, `mission_compiler.py:280`,
  `pingpong_loop.py:2824`, `pingpong_loop.py:3010` and
  `apps/cli/commands/job.py:236`. The inventory's own enumeration names four
  that pass and three that do not, which is seven, so the number contradicts
  the list directly above it. Every individual citation is correct and the
  round's conclusion is unaffected — this is an arithmetic slip in prose, not
  a bad reading of the source, and it is registered rather than waved through
  because a wrong total in an inventory is exactly the kind of number a later
  round quotes without re-counting. Fix: change "eight" to "seven" in that
  sentence and nothing else. OPEN.

TEXT-B — append to the END of docs/roadmap/features/T2_F115.md

## Correction — the manifest premise, and DECISION F115 D1 (2026-08-13)

This file's premise is false as written. "How it fits" says the prompt-segment
registry "records a manifest ... into call evidence" and the Goal assumes
"every call already records its segment manifest". The registry does build the
manifest and `PromptTraceEntry` does carry it, but only four of the seven
non-test `build_trace_entry` call sites pass `composed_prompt` —
`intake.py:145`, `flight_plan.py:191`, `orchestrator_loop.py:930` and
`mission_compiler.py:290`. The three that produce the prompts behind every
real ledger row do not: the builder (`pingpong_loop.py:2824`), the reviewer
(`pingpong_loop.py:3010`) and the planner (`apps/cli/commands/job.py:236`).
On live data the manifest is therefore EMPTY for exactly the calls this
feature exists to explain. Evidence: `.agent/f115_inventory.md` (F115 R1),
Q3 and Q4.

DECISION F115 D1 — wire the missing sites through the registry before building
the report, starting with the builder site. Chosen because the alternative
(accept current rows as permanently "unattributed" and build only the
backfill-tolerant path) ships a report whose headline breakdown is 100 %
unattributed on real data — a feature that passes its goldens on fixtures and
explains nothing about an actual run, which is the failure mode P1 and P6
exist to prevent. The cost is low and the risk is bounded: `_build_builder_prompt`
is a thin wrapper that already returns `compose_builder_prompt(...).text`, and
the suite already pins that equivalence
(`tests/orchestration/test_builder_prompt_golden.py:254`), so the sent bytes do
not change. Alternatives considered: (a) accept unattributed — rejected above;
(b) re-split the prompt string after the fact to recover segments — rejected
because it re-derives what the composer already knows and would drift from it
silently. Reverse this decision by deleting this section and dropping the
`composed_prompt=` argument at the wired call sites; the manifest returns to
empty and nothing else changes.

Two limits this correction does NOT remove, both recorded here so the report's
scope stays honest. The ledger's `role` column takes its value from
`token_accounting.json`, which hardcodes `"role": "builder"` for a whole task
run (`pingpong_loop.py:4011`), so the "per-role breakdown" this file asks for
has ONE bucket until that is fixed — the existing CLI already says so in its
own output (`_ROLE_LIMIT_NOTE`, `stats_ledger_cmd.py:334-339`). And the "by
task class" breakdown has no source at all: there is no task-class column on a
ledger row and `task_granularity.py:5` states that Remedy has no per-task-class
cost history yet. Both belong to their own features; F115 reports what exists
and says "no data" for what does not, rather than inventing a bucket.

TEXT-C — the complete new .agent/plan.md

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged at the Open PR Gate. Last reviewed SHA: a414c0c6 (R1 PASS).
Next free finding ID: R-0322. Open findings: 2 — R-0320 (Low, carried
forward from F111) and R-0321 (Low, an inventory miscount).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R2 (T001a) — make the premise true at the builder call site. The R1
inventory proved the segment manifest is EMPTY on live ping-pong data
because the builder, reviewer and planner trace entries never receive a
`composed_prompt` (DECISION F115 D1). This round wires the builder site
and pins the result with a test, with the sent bytes provably unchanged.

## Next Steps
1. R3 — the reviewer site, which needs a decision first: its traced text
   is wrapped by `_reviewer_effective_prompt` and is not always the
   composed text. Then the planner site in `apps/cli/commands/job.py`.
2. T001 proper — persist the manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
3. T002 — aggregation queries plus the pure renderer, with goldens over
   a fixture ledger; follow `gauntlet_matrix.py` and
   `tests/cli/test_stats_cost.py:49-128`.
4. T003 — CLI, prior-period comparison, json schema; then the
   integration gate and closure.

## Risks
- The per-role breakdown has one bucket until `role` stops being
  hardcoded, and per-task-class has no source at all. Both are recorded
  in the feature file; F115 must report "no data", never a fake bucket.
- Report generation must touch nothing (read-only, state snapshot equal).

Fortschritt: 15 % (R1 Inventar ✅ · T001a läuft · T001 · T002 · T003 offen) — Schätzung
