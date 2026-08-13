# Live Review — F115 Prompt breakdown & cost report

> Round-by-round review record for F115, reset at the feature claim. The F111
> record is preserved in git history at its closure commit 98a49b5c. Finding
> IDs continue monotonically across features and are never renumbered.

## Steps
R1 claim, state reset and shape inventory → T001 manifest-alongside-actuals
persistence with backfill tolerance → T002 aggregation queries, the pure
renderer and its goldens → T003 CLI, period comparison and json schema →
integration gate → closure.

## Findings

- R-0320 — Low — carried forward from the F111 closure-candidates file under
  the disk-vehicle rule (docs/roadmap/STATUS_closure_protocol.md,
  "Closure-candidate findings"). A stop reason no code can ever emit:
  `STOP_REASONS` in `packages/orchestration/builder_bridge.py` declares
  `stale_diff_context`, and a repo-wide grep over every `.py` file finds that
  string in exactly one place — the frozenset itself. Nothing raises it,
  nothing tests it, nothing reads it. It predates the F111 branch (it is
  present at the merge base 4e0b762e), so it was not an F111 defect and was
  deliberately not fixed there. It is not fixed in F115 either: AGENTS.md bars
  mixing an unrelated fix into a feature branch, and F115 opens the token
  ledger and the report renderer, not the builder bridge. The remedy — wire it
  to the condition it names, or delete it — is a one-commit change that
  belongs to whichever feature next has a legitimate reason to open
  `builder_bridge.py`. Recording it here keeps it findable after
  `.agent/candidates.md` is emptied, which is the whole point of the
  carry-forward rule. OPEN.

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

- R-0322 — Medium — the suite is RED at this branch's merge base. Five ids in
  `tests/orchestration/test_role_conventions.py` fail, every one a
  `[reviewer]` parametrization, each raising `PromptSegmentError: prompt
  segment 'reviewer_conventions' is over its token cap: 954 tokens estimated,
  cap 800` before any assertion in the test runs. Measured by the reviewer at
  the R2 gate: `5 failed, 21 passed in 0.14s`. It is NOT an F115 defect —
  `docs/agents/reviewer_conventions.md` was last touched at a85e82f5 on
  2026-08-12, before this branch existed, and
  `git diff --name-only 0d6c97aa..HEAD` over that path and over
  `prompt_facts.py` is empty. It is the same class F111 recorded as R-0286 and
  attributed at its integration gate in both trees. It is registered here
  rather than inherited silently because F115's own integration gate will meet
  it, and a gate that has to rediscover a known red spends a round proving
  something already known. It is deliberately NOT fixed on this branch:
  AGENTS.md bars mixing an unrelated fix into a feature branch. The fix
  belongs to a round that legitimately opens the conventions document or the
  cap. OPEN.

Done: R-0321 — RESOLVED at the R4 gate. Verified against the disk, not the report: `grep -c 'four of the eight' .agent/f115_inventory.md` prints 0 and `grep -c 'four of the seven'` prints 1, the enumeration below that sentence still names four wired call sites and three unwired, and `git show --numstat 8412f20c` shows the C3 commit of R3 changed exactly one line of that file. The R3 round as a whole is PASS: gates (a)-(g) were re-run by the reviewer and every value matched the handback, and the R3 diff touched only `.agent/**` and `docs/agents/planner_reviewer_prompt.md`, as its block declared.

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

- R-0324 — Low — reviewer spec arithmetic, self-registered, caught before the
  round it would have broken. DECISION F115 D2 (R5) fixed the planner segment
  ranks as "the job prompt at TASK rank, the recalled memory section at
  JOB_CONTEXT rank". Composition sorts by rank ASCENDING
  (`compose_prompt_segments`, `prompt_segments.py:182-188`) and JOB_CONTEXT is 3
  against TASK's 4, so that assignment composes the MEMORY SECTION FIRST, while
  the code it must reproduce concatenates the other way round —
  `prompt = f"{prompt}\n\n{memory_section}"`, `llm_planner.py:107-109`. D2's own
  byte-identity gate, the one it calls the round's first gate, was therefore
  unmeetable by construction — reading the rank names as semantic labels rather
  than as the sort key they are is what produced the slip. Corrected before
  emission as DECISION F115 D3, by checklist item 8
  (`docs/agents/planner_reviewer_prompt.md`) — compute a gate's expected value
  from the code that PRODUCES it. Fourth of the reviewer-arithmetic class after
  R-0282, R-0321 and R-0323, and the first caught before a worker paid. OPEN.

- R-0325 — Low — the R6 authored import block left `tests/test_llm_planner.py`
  ruff-dirty. TEXT-G placed `from packages.orchestration.prompt_segments import
  (...)` ABOVE the existing `planner_models` import, so the block is no longer
  alphabetically sorted and `python3 -m ruff check tests/test_llm_planner.py`
  reports `I001` (un-sorted import block) at line 7 — measured by the reviewer
  at the R6 gate, against a file that printed `All checks passed!` one commit
  earlier. `I` is an enabled rule class (`pyproject.toml:50`), so this is a real
  regression this branch introduced, not a pre-existing style debt; it is Low
  because no suite test and no CI workflow runs ruff (the repository has no
  `.github/workflows/`), so nothing turns red today. The worker was right to
  report it rather than edit an authored slice to fix it. Fix: move the
  `prompt_segments` import below `planner_models`. OPEN.

- R-0326 — Low — the R6 authored docstring carries a live escape sequence. The
  `compose_planner_prompt` docstring is a normal (non-raw) string containing the
  characters backslash-n twice, so Python turns them into two real newlines and
  the rendered `__doc__` breaks its own sentence mid-clause — the text meant to
  NAME the delimiter instead BECOMES it. The source file reads correctly and
  ruff stays silent (backslash-n is a valid escape, so no W605), which is why
  the R6 gate did not catch it; `help(compose_planner_prompt)` is where it
  shows. Reviewer-authoring defect, same class as R-0325: the authored bytes
  were correct as bytes and wrong as Python. Fix: name the delimiter in words
  instead of spelling it. OPEN.
