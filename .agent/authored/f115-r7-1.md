── STEP R7/n — F115 Prompt breakdown & cost report · Round 7 ─────────
Goal:        Clear the two Low findings the R6 gate produced, then put the T001
             persistence FACTS on disk — the ledger row is one finalized task
             run while a manifest is per call, so the next session decides that
             mapping from a record instead of re-deriving it mid-flight.
Bundle:      C1a save block · C1b mirror · C2 register R-0325 + R-0326 ·
             C3 fix R-0325 · C4 fix R-0326 · C5 T001 inventory · C6 plan + handback
Change:      EXACTLY these paths:
               .remedy-wt/f115-r7-1.md      (source, gitignored, NOT committed)
               .agent/authored/f115-r7-1.md (new, C1a)
               .agent/last_block.md         (rewrite, C1b)
               .agent/live_review.md        (C2: append)
               tests/test_llm_planner.py    (C3)
               packages/orchestration/llm_planner.py (C4)
               .agent/f115_inventory.md     (C5: append)
               .agent/plan.md               (C6: full replace)
               .agent/handoff.md            (C6: rewrite)
Constraints:
  - TEXT-A … TEXT-E are AUTHORED text: apply byte for byte, no rewording,
    rewrapping or re-punctuation, and no slots to substitute.
  - C5 records FACTS ONLY. Do not decide the persistence shape, do not design a
    column, do not write code. Every answer carries a `path:line` citation you
    read yourself; an answer you cannot cite is written as "not found" with the
    command you ran. A guessed answer is a finding against this round.
  - Do NOT write a `Done:` paragraph and do NOT mark anything resolved
    (docs/agents/planner_reviewer_prompt.md §4.4). C3 and C4 land the fixes; the
    reviewer authors their `Done:` text at the next gate. If you want to record
    that a fix landed, the only permitted line is
    `Landed: R-XXXX — <one line: what changed, which commit>`.
  - Do NOT fix R-0320, R-0322, R-0323 or R-0324. The first two predate this
    branch; the last two are reviewer-arithmetic records with no on-disk fix.
  - Do NOT touch `apps/cli/commands/job.py`, `prompt_segments.py`,
    `prompt_trace.py`, `token_ledger.py` or any test beyond the one C3 names.
  - Never force-push. Never commit on main. Push after EVERY commit (R-0289).
  - Do NOT create a pull request this round.
Done when: every command RUN for real, its TRUE output recorded — a guessed,
           expected or remembered value is a finding.
  a. `cmp .agent/authored/f115-r7-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. After C2, over `.agent/live_review.md`: `grep -c '^- R-0325'` = 1 ·
     `grep -c '^- R-0326'` = 1 · `grep -c '^- R-0'` = 7 (was 5) ·
     `grep -c '^Done:'` = 1 (unchanged) · `grep -c '^## Steps'` = 1.
  c. After C3: `python3 -m ruff check tests/test_llm_planner.py` prints
     `All checks passed!` with exit 0 — measured before the fix it reports
     `Found 1 error.` (I001, un-sorted import block, line 7). Also run
     `python3 -m ruff check packages/orchestration/llm_planner.py apps/cli/commands/job.py tests/orchestration/test_structured_planner_cli.py`
     and record its real output; those three measured clean at R6.
  d. After C4: `grep -c 'this module$' packages/orchestration/llm_planner.py` = 0
     — measured before the fix it is 1, and line 7 of that file also contains
     "this module" but does not END with it, so the count reaches 0 exactly when
     the retired docstring line is gone. Then
     `grep -c 'the same blank-line separator' packages/orchestration/llm_planner.py`
     = 1.
  e. After C4: `python3 -m pytest tests/test_llm_planner.py -q` — measured
     baseline at R6 `38 passed`; C3 and C4 add no test, so 38 is expected.
  f. After C5: `grep -c '^## T001 persistence inventory (R7)' .agent/f115_inventory.md`
     = 1 · `grep -c '^Q[1-6]\.' .agent/f115_inventory.md` = 6.
  g. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` — measured baseline `42 passed`, must not move.
  h. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real one.
  i. `git status --porcelain` empty; `git diff --name-only 0d6c97aa..HEAD | wc -l`
     — the TWENTY-THREE paths present after R6 plus ONE new one
     (`.agent/authored/f115-r7-1.md`); every other path this round touches is
     already among the 23, so 24 is expected. If it is not 24, report the real
     number and the actual list and change nothing; `.remedy-wt/**` must NOT
     appear. Finally
     `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
     prints 0 and 0.
Handback:  completion report + rewrite `.agent/handoff.md`: item-status table
           (C1a, C1b, C2, C3, C4, C5, C6 — each exactly once), commit table with
           real SHAs and insertions, changed-files table, every result a-i as a
           REAL value, the Fortschritt line verbatim. Over 60 lines ⇒ a
           "Deviations, declared" line naming the count and the mandated content
           that caused it (AGENTS.md DECISION D15).

           THIS IS THE LAST ROUND OF THE SESSION. The handoff is the only return
           channel: name the branch, the head SHA, the last reviewed SHA
           (139b5c48, R6 PASS), every open finding with its state, and that the
           next work is T001's persistence shape, decided from the C5 inventory.
           Do NOT create a PR.
──────────────────────────────────────────────────────────────────────

PROCEDURE

C1a `chore(f115): save the R7 step block verbatim` — copy the reviewer's
    scratchpad original `.remedy-wt/f115-r7-1.md` to
    `.agent/authored/f115-r7-1.md`. Copy the FILE; do not retype it.
C1b `chore(f115): mirror the R7 block into last_block` — copy that same file to
    `.agent/last_block.md`. Run gate (a).

C2 `chore(f115): register R-0325 and R-0326 from the R6 gate`
    Append TEXT-A to the END of `.agent/live_review.md`. Run gate (b).

C3 `fix(f115): sort the planner test imports`
    Apply the TEXT-B pair to `tests/test_llm_planner.py`. Run gate (c).

C4 `docs(f115): keep the composer docstring free of an escape`
    Apply the TEXT-C pair to `packages/orchestration/llm_planner.py`. Run gates
    (d) and (e).

C5 `docs(f115): inventory the T001 persistence facts`
    Append TEXT-D to the END of `.agent/f115_inventory.md`, then answer Q1-Q6
    IN THAT FILE, each directly under its question, in prose with `path:line`
    citations. Read the code; do not infer from names. Run gate (f).

C6 `chore(f115): refresh the plan and write the R7 handoff`
    `.agent/plan.md` ← TEXT-E in full, then rewrite `.agent/handoff.md`.
    Run gates (g), (h) and (i).

TEXT-A — append to the END of .agent/live_review.md

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

TEXT-B — REWRITE pair for tests/test_llm_planner.py

FROM:
from packages.orchestration.prompt_segments import (
    PROMPT_SEGMENT_DELIMITER,
    SegmentStabilityRank,
)
from packages.orchestration.planner_models import PlannerOutput, ProposedTask
TO:
from packages.orchestration.planner_models import PlannerOutput, ProposedTask
from packages.orchestration.prompt_segments import (
    PROMPT_SEGMENT_DELIMITER,
    SegmentStabilityRank,
)

TEXT-C — REWRITE pair for packages/orchestration/llm_planner.py

FROM:
    Byte identity with the pre-F115 concatenation is the whole contract: the
    join string is `PROMPT_SEGMENT_DELIMITER`, which IS the `\n\n` this module
    used by hand, and an absent memory section registers NO segment rather than
    an empty one — so a one-segment composition is the bare job prompt.
TO:
    Byte identity with the pre-F115 concatenation is the whole contract: the
    join string is `PROMPT_SEGMENT_DELIMITER`, the same blank-line separator
    this module concatenated by hand, and an absent memory section registers NO
    segment rather than an empty one — so one segment composes to the bare job
    prompt, with no separator anywhere in it.

TEXT-D — append to the END of .agent/f115_inventory.md

## T001 persistence inventory (R7)

Facts only, each with a `path:line` citation read at this round. The shape
question T001 has to answer is already visible: `token_ledger.py` documents that
A ROW IS ONE FINALIZED TASK RUN keyed `"<job_id>:<task_id>"` (DECISION F103
D16), while a segment manifest belongs to ONE PROVIDER CALL — so "the manifest
alongside the ledger row" is a one-to-many mapping, not a column copy. Answer
each question directly below it; write "not found" plus the command you ran
rather than an inference.

Q1. The ledger row: every column of the table a task run writes, taken from the
CREATE TABLE statement itself, with its `path:line`. Name which columns are
NULLable and which carry a default.

Q2. The write path: the ONE call site the module names
(`pingpong_evidence.write_evidence_bundle`) — its `path:line`, what it receives,
and specifically whether the prompt-trace entries (or anything carrying a
`segment_manifest`) are in scope AT THAT POINT or only reachable from disk.

Q3. The trace file: the exact path pattern `prompt_trace.jsonl` is written to,
its writer's `path:line`, and whether anything deletes, rotates or truncates it
after a run — quote the code you checked, or state that a search found no
deleter and name the search.

Q4. Schema versioning: how the module versions its schema (the `meta` row), its
`path:line`, and whether an ADDITIVE column has ever been migrated there before.
If yes, cite that migration; if no, say so — that absence is the fact T001 needs.

Q5. Readers: every place that SELECTs from the ledger today, with `path:line`,
and how each behaves when a column is NULL or a row is missing. Note any
existing "unattributed"/"no data" rendering precedent.

Q6. Correlation: whether a prompt-trace entry can be tied to a ledger row from
the data alone — check which of `job_id`, `task_id`, `run_id` a trace entry
actually carries at the planner, builder and reviewer call sites (a field that
exists in the dataclass but is left empty at a call site is NOT a correlation
key; cite the call site).

TEXT-E — the complete new .agent/plan.md

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: 139b5c48 (R6 PASS). Next free finding
ID: R-0327. Open findings: 6 — R-0320 (Low, from F111), R-0322 (Medium,
inherited suite red), R-0323 + R-0324 (Low, reviewer arithmetic),
R-0325 + R-0326 (Low, R6 authoring defects, fixed this round, awaiting
the reviewer's resolution text).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R7 cleared the two R6 authoring defects and put the T001 persistence
facts on disk in `.agent/f115_inventory.md`: a ledger row is one
finalized task run, a manifest is one provider call, so T001 has a
one-to-many mapping to decide before it writes anything.

## Next Steps
1. T001 — decide the manifest-to-row mapping from the R7 inventory
   (aggregate column vs trace reference vs per-call table), record it as
   a DECISION, then persist additively with backfill tolerance: old rows
   render "unattributed", never guessed.
2. T002 — aggregation queries plus the pure renderer, with goldens;
   follow `gauntlet_matrix.py` and `tests/cli/test_stats_cost.py:49-128`.
3. T003 — CLI, prior-period comparison, json schema.
4. Integration gate (docs/agents/integration_gate.md), then closure.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 45 % (R1 ✅ · T001a ✅ · alle drei Call-Sites ✅ · T001-Shape ✅ · T001 · T002 · T003 offen) — Schätzung
