── STEP T001/F280 — round 14 ────────────────────────────────────────
Goal: Book round 13's independently-reviewed PASS, author DECISION F280
D9, and land the rest of the `flight_plan` rename DECISION
amend0917-throughput D3 ordered — widened to the DAG-key construction
sites and the identifier residue the reviewer's own disposable-worktree
dry run measured before authoring — as one pre-tested mechanical patch.

Bundle:
1. Book Gate: F280 R13 (PASS, one prose slip, no new R-id).
2. Append the R13 prose slip (stale, copy-pasted commit-subject text).
3. Author DECISION F280 D9 and its T2_F280.md amendment.
4. Replace .agent/plan.md with the round-14 plan.
5. Apply the pre-tested rename patch (61 files, 339 insertions / 339
   deletions): the DAG-scheduling key `inputs["flight"]` (access,
   construction and membership sites) becomes `inputs["plan"]`; the
   decision-id prefix `fp:` (quoted, backtick-cited, or bare before
   `approval`) becomes `plan:`, `apps/ui/src` included; the residue of
   bare identifiers still spelled `flight_plan`/`FlightPlan`/
   `FLIGHT_PLAN` (one local variable, one abbreviated local, two
   parameters, one production function, one stale test class name, 22
   more test class/function names, six module-qualified comment
   citations) becomes `task_plan`/`TaskPlan`/`TASK_PLAN`; the English
   prose noun "flight plan"/"flight-plan" under the six named
   directories plus `apps/ui/src` becomes "task plan"/"task-plan".
6. Write the handback and rewrite .agent/handoff.md.

Change: exactly the paths named in `.remedy-wt/f280-r14-rename.patch`
(sha256 `0fa44a865accace59b24254bf90115de55a7179f70d3a0a42eef3a8f934ab710`)
plus `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/decisions.md`,
`docs/roadmap/features/T2_F280.md` and `.agent/plan.md`. Nothing else.

Constraints:
- EXCLUDED, explicitly, and NOT in the patch: `job_plan.py`'s
  `_PLAN_SYSTEM_SEGMENT` prompt-template literal ("a flight plan: a DAG
  of tasks..."), `dod_compiler.py`'s `_DOD_PROMPT_TEMPLATE` two lines,
  `docs/system/vocabulary.md` (historical DECISION quotations),
  `tests/docs/test_docs_consistency.py:74` (quotes T2_F280.md's own
  out-of-scope title verbatim) and `tests/docs/test_vocabulary.py:52`'s
  `RETIRED_SYNONYMS` entry `"flight plan"` (names the retired word to
  check FOR — do not rename it to the current word). Accepted `[x]`
  feature files and `.data/evidence_exports/` stay byte-identical.
  `docs/roadmap/**` and `docs/agents/**` are out of scope for this
  patch's prose sweep (D3 names six directories plus `apps/ui/src`;
  those two are not among them).
- No migration shim for any renamed key, prefix or identifier (DECISION
  D-A, `T2_F261.md`).
- Commit sequence: C0a (write authored block as
  `.agent/authored/f280-r14.md`) → C0b (mirror to `.agent/last_block.md`)
  → C1 (append Gate:F280 R13 + prose slip + DECISION F280 D9 + T2_F280.md
  amendment + replace plan.md, ONE commit) → C2 (apply the patch,
  `git add -A`, ONE commit) → C3 (handback commit).

Done when (exact verification commands; run each, record real exit
codes and trimmed output):

G1 TRANSPORT — `sha256sum .agent/authored/f280-r14.md .agent/last_block.md`
reads two identical digests, matching this block's own sha256 stated in
the BEGIN marker.

G2 THE RECORD — after C1: `grep -cE '^Gate: F\d+ R\d+ — ' .agent/live_review.md`
reads 40; `grep -oE '^- (R-[0-9]{4}) — ' .agent/live_review.md | grep -oE 'R-[0-9]{4}' | sort -u | wc -l`
reads 136 (unchanged); `grep -oE '^Done: (R-[0-9]{4}) — ' .agent/live_review.md | grep -oE 'R-[0-9]{4}' | sort -u | wc -l`
reads 7 (unchanged); `grep -cE '^## DECISION F280 D' .agent/decisions.md`
reads 9; `wc -l < .agent/prose_slips.md` reads 1031; `wc -l < .agent/plan.md`
reads 39 with exactly one each of `## Goal`, `## Current Step`,
`## Next Steps`, `## Risks`.

G3 THE PATCH — after C2: `git diff --numstat <C1-sha>..<C2-sha>` reads
exactly 61 paths, 339 insertions / 339 deletions total, and
`diff <(git diff <C1-sha>..<C2-sha>) .remedy-wt/f280-r14-rename.patch`
produces ZERO output (byte-identical to the reviewer's own pre-tested
patch — confirm `.remedy-wt/f280-r14-rename.patch`'s own sha256 still
reads `0fa44a865accace59b24254bf90115de55a7179f70d3a0a42eef3a8f934ab710`
before diffing against it).

G4 THE BOUNDARY — after C2: `git grep -niE 'flight_?plan' -- apps/ packages/ tests/ scripts/ docs/system/ docs/guides/ apps/ui/src`
reads exactly 4 lines, all inside `docs/system/vocabulary.md` and
`tests/orchestration/test_plan_prompt_golden.py`; `git grep -n '"flight"' -- apps/ packages/ tests/ scripts/`
reads zero; `git grep -n '"fp:approval"\|startswith("fp:")' -- apps/ packages/ tests/ scripts/ docs/system/ docs/guides/ apps/ui/src`
reads zero.

G5 TARGETED TESTS + LINT — after C2, in the primary checkout:
`python3 -m pytest tests/cli/test_decision_answers.py tests/cli/test_golden_path.py tests/cli/test_job_context_cmd.py tests/cli/test_mission_cmd.py tests/cli/test_plan_approval.py tests/cli/test_scoped_listings.py tests/docs/test_vocabulary.py tests/docs/test_docs_consistency.py tests/orchestration/test_bundled_clarification.py tests/orchestration/test_dag_schedule.py tests/orchestration/test_decision_evidence.py tests/orchestration/test_decision_inbox.py tests/orchestration/test_escalation.py tests/orchestration/test_job_plan.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_mission_compiler.py tests/orchestration/test_mission_state.py tests/orchestration/test_prompt_cache_prefix.py tests/orchestration/test_prompt_trace.py tests/orchestration/test_task_granularity.py tests/schemas/test_job_plan_schema.py tests/test_no_interactive_guard.py tests/ui_contracts/test_decision_answer_wiring.py tests/ui_server/test_command_channel.py tests/ui_server/test_command_dispatch.py -q`
reads `1460 passed`; `python3 -m ruff check` over every touched `.py`
file reads clean except the one pre-existing `UP035` at
`packages/orchestration/dag_schedule.py:36` (present at base, untouched
by this round's edits to lines 9/23/27/69-72 of that file).

G6 RED-PROOF — in a disposable worktree (removed after, `git worktree
list` proof): (a) mutate `map_task_plan_to_tasks`'s dict key back from
`"plan"` to `"flight"` in `job_plan.py` — `test_job_plan.py`'s
`TestMapTaskPlanToTasks` reddens exactly 2 nodes
(`test_three_tasks_in_order`, `test_depends_on_preserved`), reverting
restores green; (b) mutate `decision_inbox.py`'s
`str(decision_id).startswith("plan:")` back to `"fp:"` —
`test_decision_inbox.py::test_answerable_key_matches_what_the_write_door_accepts[task_plan_approval]`
reddens, reverting restores green.

Handback: completion report + rewrite .agent/handoff.md.
──────────────────────────────────────────────────────────────────────
