# STEP R1/F258 — CLAIM THE FEATURE, DISCHARGE THE F040 CLOSURE CANDIDATE, MEASURE THE SEAMS

Goal: open F258 on its own branch, settle the one candidate F040's closure gate
left in `.agent/candidates.md` so the block condition lifts, and MEASURE the
queue/planner/execution/budget/ledger seams T001-T003 compose over — recording
what is there, and what is not.

Base: `18ae71293cde9b1157aca35d3d02c3a8f4265813`, the merge commit of pull
request 225 and the current tip of `main`. Cut the branch from it.

Branch: `feature/f258-self-use-v2`

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f258-r1.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN1
- C2  append slice RECORD1 to `.agent/live_review.md`
- C3  rewrite `.agent/candidates.md` from slice CAND1
- C4  apply pair PAIR-STATUS to `docs/roadmap/STATUS.md`
- C5  rewrite `.agent/context.md` from slice CONTEXT1
- C6  write `.agent/f258_inventory.md` — YOUR measurement, per the SPEC below
- C7  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f258-r1.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/candidates.md
    docs/roadmap/STATUS.md
    .agent/context.md
    .agent/f258_inventory.md
    .agent/handoff.md

No file under `packages/`, `apps/`, `tests/`, `docs/guides/`, `docs/system/` or
`docs/roadmap/features/` changes this round. This round writes NO production code
and NO test.

## Constraints

1. Apply every slice BYTE FOR BYTE. Do not fix, rewrap, retitle or improve a
   slice. If a slice looks wrong, apply it as given and DECLARE the problem in
   the handback's deviations — that is the honest route and it costs nothing.
2. C0a is a COPY, never a retype: the block is on disk at
   `.remedy-wt/f258-r1-block.md`. Use `shutil.copyfile` for C0a and again for
   C0b. Its sha256 is stated in gate G1; verify BEFORE saving.
3. C1 is the FIRST substantive commit, ahead of C2, because this round touches
   the finding ledger and AGENTS.md's Commit Gate requires `.agent/plan.md` to
   match the current work before every commit.
4. The record is APPEND-ONLY. C2 appends RECORD1 and revises NOTHING already in
   `.agent/live_review.md`. R-0570's landed paragraph is NOT edited.
5. NO NEW R-ID IS MINTED THIS ROUND and NO DECISION ID IS MINTED THIS ROUND. The
   count of distinct `^- R-\d+ — ` ids is the same before and after C2, and the
   count of distinct `^DECISION F258 D\d+ — ` ids is zero before and after.
   R-0570 stays OPEN — do not write a `Done:` or `Landed:` line for it.
6. `.agent/plan.md` stays under 50 lines (AGENTS.md). PLAN1 is authored to fit;
   do not add to it.
7. Every exit code you report is REAL, taken from `subprocess.run(...).returncode`
   inside a script under the gitignored `.remedy-wt/`. Never read an exit code
   through a pipe, and never report a colour you did not run.
8. Destructive verification — if any — runs ONLY inside a disposable
   `git worktree`, never in the primary checkout, which satisfies
   `git status --porcelain` empty at every reading. This round mints no G3
   negative control byte-flip requirement beyond the standard record-append
   readings below; if you choose to run one anyway, isolate it the same way.
9. The `remedy` console script is DENIED in this sandbox. Where you need it, use
   `python3 -m apps.cli.grouped ...` and say so.
10. Commit subjects carry no leading-slash token, no absolute path and no
    secret-like string. Match the branch convention: no `Co-Authored-By` trailer.
11. Push the branch after C7 and open NO pull request. This is round 1 of the
    feature; the PR is created at closure.
12. Pair shape, measured not asserted — PAIR-STATUS: `TO contains FROM: false`,
    so it is a REWRITE, and the FROM-zero / TO-one count applies to it.
13. The inventory (C6) is a MEASUREMENT, not a design. Where something is
    ABSENT, say so and say how you searched — an absence is only as wide as the
    search that looked for it. Cite every claim with a `file:line` and the exact
    command that produced it.

## Slices

The authored units below are PLAN1, RECORD1, CAND1, CONTEXT1 and the two halves
of PAIR-STATUS. Each is delimited by its own BEGIN and END marker line; the
marker lines are NOT part of the slice, and the slice's own bytes start on the
line after BEGIN and end with the newline before END.

<<<BEGIN PLAN1
# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 1, opening the feature.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 closure candidate | done | this round; no id spent |
| the F258 claim and the branch | done | this round |
| the seam inventory | done | this round, `.agent/f258_inventory.md` |
| T001 the self-replenishing generator | open | next round, ordered from the inventory |
| T002 consumed means executed | open | |
| T003 findings flow back | open | |

## Next Steps
1. This round claims F258, discharges the one candidate F040's closure gate
   raised (new evidence on the already-open R-0570, no new id), and measures
   the queue/planner/job-execution/budget/approval seams T001-T003 compose
   over.
2. The round after it orders T001 — the generator's source-priority logic and
   its `provenance` field — from what the inventory measured; there is
   currently NO code caller of `plan_next_self_use_item` at any closure point,
   so the inventory names exactly what today's manual precondition-6 step
   does instead.
3. T002 depends on T001 producing a real item to run against; T003 is largely
   wiring existing finding-ledger machinery once T002 exists.

## Risks
- R-0570 (Low) stays OPEN and is deliberately NOT repaired here — same reason
  as F040's own round 1: the fix edits `README.md` and a test neither F258
  owns, and AGENTS.md forbids mixing an unrelated fix into a feature branch.
- The queue's `consumed_by`-is-closure-only invariant (DECISION F257 D2) binds
  T001: the generator may APPEND a new pending item but must never be the
  thing that marks one consumed.
<<<END PLAN1

<<<BEGIN RECORD1
Note: F258 — A THIRD OCCURRENCE OF THE SAME OPEN DEFECT, R-0570, IS DISCHARGED AS NEW EVIDENCE AND THE CANDIDATE FILE THAT CARRIED IT IS EMPTIED; NO ID IS SPENT. F040's own closure round (C3, commit `0ec9bb37`) recorded exactly one candidate: the README's "Accepted in Tier 5 so far:" prose list was one paragraph short of the ledger's Tier 5 accepted count, F033 named in neither. THE NEW EVIDENCE, measured by the reviewer at `18ae7129` (the merged tip of `main`, pull request 225): the Tier 5 prose block still names exactly eleven ids — F255, F008, F009, F021, F022, F031, F032, F037, F256, F257 and now F040 — while `docs/roadmap/STATUS.md`'s Tier 5 block carries TWELVE lines matching `^- \[x\] F\d{3} — `, F033 still the omitted twelfth, and the tier table at `README.md` line 28 reads `| 5 | Operator Cockpit | 12 | 32 |`. This is the same shape R-0570 already describes — a list pinned in the list→ledger direction only, per `test_the_readme_reports_the_accepted_foundation_and_no_later_feature` in `tests/docs/test_docs_consistency.py`, which iterates the ids the README LISTS and asserts each is accepted, so an accepted feature the README omits stays invisible to it. R-0570 STAYS OPEN and its routing is unchanged: the fix edits `README.md` and that test, neither of which F258 owns, so it belongs to the same paydown branch R-0570's own text names.
<<<END RECORD1

<<<BEGIN CAND1
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

EMPTY — no candidate is open.

The one entry F040's closure gate raised was discharged in F258 round 1 as new
evidence on the already-open finding `R-0570` in `.agent/live_review.md`; no id
was spent. The two entries F033's closure gate raised before it were discharged
the same way in F040 round 1.
<<<END CAND1

<<<BEGIN CONTEXT1
# Context — F258 Self-use track v2

## Active Branch
feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge commit of
pull request 225, which is the commit that accepted F040 into the ledger.

## Scope
Feature F258, `docs/roadmap/features/T5_F258.md` — a self-replenishing queue
generator that fires at the closure consumption point whenever the queue is
empty (T001), executing the consumed item through the real job path under a
small dedicated budget to the normal approval gate rather than only planning
it (T002), and routing any defect a run surfaces into the standard finding
ledger (T003).

## Do not touch
The scope-fence builtin deny list (F017), the normal approval gate, and STATUS
semantics — a job must never check itself off — per the feature file's own
Do-not-touch. The v1 queue schema's existing fields (`id`, `title`, `why`,
`job_markdown`, `consumed_by`) are extended, never replaced, so
`packages/orchestration/self_use_queue.py`'s existing readers keep working
against a v2 queue file.

## Assumptions
- `next_self_use_item`/`plan_next_self_use_item` currently have NO production
  caller anywhere in `packages/` or `apps/`: precondition 6
  (`docs/roadmap/STATUS_closure_protocol.md`) today is a manual step a session
  performs by hand at every closure. What T001's generator hooks INTO is
  decided from the round-1 inventory's measurement, not assumed here.
- Consumption stays closure-only (DECISION F257 D2): T001 may append a new
  pending item to the queue but must never be the thing that sets
  `consumed_by`, and T002's execution must never auto-promote past the
  existing `--approve` barrier.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced. They are not this feature's, and
deleting them with the rest of a rewrite is what cost an earlier round a red
CI run.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in
  the primary checkout, which satisfies `git status --porcelain` empty at every
  verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract those
  readers hold over the three state files, so a rewrite is checked against it
  directly rather than rediscovered from a red: this file carries
  `## Active Branch`, a `feature/` branch name, a roadmap feature id matching
  `\bF\d{3}\b` and the word `Steps`; `.agent/plan.md` carries `## Goal`,
  `## Next Steps` and a feature id; `.agent/live_review.md` carries `Steps`.
- A new module under `packages/orchestration/` is swept by repo-wide guards that
  name no path: the `REMEDY_DATA_DIR` single-reader invariant, the path-utils
  single-implementation invariant, the bare-`except: pass` ban, and the
  development-artifact boundary.

This feature is NOT UI work — no design-reference binding applies. The
Do-not-touch above carries the two constraints specific to F258 itself: no
self-consumption-marking, no auto-promotion past `--approve`.

## Steps
The item-status table for this feature lives in the `## Current Step` section
of `.agent/plan.md`. This file deliberately does not restate it — a second copy
of the map is what fell out of step and cost F022 a finding.
<<<END CONTEXT1

<<<BEGIN PAIRSTATUS-FROM
- [ ] F258 — Self-use track v2 (self-replenishing queue & executed items)
<<<END PAIRSTATUS-FROM

<<<BEGIN PAIRSTATUS-TO
- [~] F258 — Self-use track v2 (self-replenishing queue & executed items)
<<<END PAIRSTATUS-TO

## SPEC for C6 — `.agent/f258_inventory.md`, YOUR measurement

This file is NOT authored above and must not be invented. MEASURE the repository
at C5 and write what you find, with a `file:line` for every claim and the exact
command beside every count. Where something is ABSENT, say so and say how you
searched. Six sections, in this order:

1. THE QUEUE SCHEMA AND ITS V1 CONTRACT. `packages/orchestration/self_use_queue.py`:
   the exact fields of `SelfUseQueueEntry` and `_ITEM_KEYS`, `SELF_USE_QUEUE_SCHEMA_VERSION`,
   the id regex, and the signatures and return types of `load_self_use_queue`,
   `pending_self_use_items` and `next_self_use_item`. Quote the exact validation
   code that would reject an unknown key (e.g. a new `provenance` field) today,
   and state what a schema-version bump would need to touch for v2 to add one.

2. THE PLANNER SEAM. `packages/orchestration/self_use_job.py`: the signatures of
   `write_self_use_job_file`, `plan_self_use_item` and `plan_next_self_use_item`.
   `packages/orchestration/pingpong_job.py`'s `plan_job_from_file`: what it
   requires as input and the exact shape of the `JobPlan` (or equivalent) it
   returns.

3. THE CLOSURE CONSUMPTION POINT TODAY — SEARCH FOR IT AND REPORT THE RESULT.
   Grep `plan_next_self_use_item` and `next_self_use_item` across `packages/`
   and `apps/`, excluding test files, and report every call site your own
   commands find. Quote `docs/roadmap/STATUS_closure_protocol.md` precondition
   6's exact text and state plainly whether it names a code hook or a manual,
   by-hand step performed once per session at closure.

4. THE JOB EXECUTION PATH TO "A REAL RUN". `apps/cli/commands/job.py`: name
   every subcommand between job creation and the approval gate a self-use
   item's execution would pass through — creation, repo-attach, permission
   setting, the run-loop/run-cycles entry point — and quote each one's
   registration line in `apps/cli/command_catalog.py`. Name where
   `packages/orchestration/job_promote.py`'s `promote_job` sits as the manual
   `--approve` barrier, and name the worktree-isolation seam (F006) a self-use
   run would need for "an isolated worktree".

5. THE BUDGET MACHINERY FOR "A SMALL DEDICATED BUDGET". Name the module and
   CLI surface (`_cmd_job_budget` and whatever it calls) that sets a per-job
   budget limit, and the F104 hard-enforcement module. State the exact
   flag/field a caller sets to keep a self-use run small.

6. THE FINDING LEDGER'S OWN SHAPE, for T003. Count, with the exact commands you
   ran, the current distinct `^- R-\d+ — ` and `^Done: R-\d+` lines in
   `.agent/live_review.md`, and quote one OPEN Medium or Low finding's exact
   severity-and-status text so a future "self-contained, repo-scoped,
   repairable as one small job" filter has a real string shape to grep for.
   Name `tests/orchestration/test_self_use_queue.py` and
   `tests/orchestration/test_self_use_job.py` as the fixture style T001-T003's
   own tests should follow, quoting one existing test function's name from
   each.

Report every ABSENCE explicitly. A section that says "not found, searched with
<command>" is worth more than a confident guess, and this inventory is the
evidence the T001 order is built from.

## Done when — the gates

Run each gate and report ONE line per gate in the handback with its REAL exit
code. Every gate below runs at a commit STRICTLY EARLIER than C7, which writes
the handback; C7's own numbers are measured by the reviewer at the next gate and
are not owed here.

G1 TRANSPORT, at C0b. Compute sha256 over THREE files: the scratch original
   `.remedy-wt/f258-r1-block.md`, the committed `.agent/authored/f258-r1.md`,
   and the committed `.agent/last_block.md`. Report the one digest and the byte
   length, and state that all three are equal. This block deliberately states no
   expected digest — a file cannot carry its own sha256, and the reviewer holds
   the original and checks your reported value against its own measurement at
   the gate.

G2 THE PLAN, at C1. `.agent/plan.md` is BYTE-EQUAL to slice PLAN1 (report both
   sha256 values), its line count is under 50, and it holds `## Goal` and
   `## Next Steps`.

G3 THE RECORD APPEND, at C2. The MEASURED pre-commit byte length of
   `.agent/live_review.md` plus one separator newline plus RECORD1's byte length
   equals the committed length — re-measure the base yourself at the commit you
   append at; the reviewer read 1751668 at `18ae7129`. Then TWO independent
   readings: (a) WHOLE RECONSTRUCTION — base + separator + slice compared to the
   entire committed file; (b) PARAGRAPH ORDER — the last blank-line unit of the
   committed file equals RECORD1 exactly (N=1, one dense paragraph). NEGATIVE
   CONTROL, inside a disposable worktree: flip one printable byte inside the
   appended paragraph and report that BOTH readings reject the flipped file and
   accept the unflipped one; remove the worktree after.

G4 THE LEDGER, at C1 and at C2. Report, for each of the two commits: distinct
   `^- R-\d+ — ` ids, distinct `^Done: R-\d+ — ` ids, and the open count. The
   ADDED registered ids and the ADDED resolved ids must BOTH be the empty list.
   Report the distinct `^DECISION F258 D\d+ — ` ids before and after; both must
   be empty — this round mints no decision. Report whether `R-0570` still has
   zero `^Done: R-0570` lines.

G5 THE CANDIDATES FILE, at C3. `.agent/candidates.md` is BYTE-EQUAL to slice
   CAND1 (report both sha256 values), and the string `· F040 · 2026-08-30`
   occurs 0 times in it. Report its byte length before and after.

G6 THE CLAIM AND THE DOCS PINS, at C4. In `docs/roadmap/STATUS.md`:
   PAIRSTATUS-FROM occurs 0 times and PAIRSTATUS-TO occurs exactly 1 time;
   `git diff --numstat` for C4 alone reads exactly one insertion and one
   deletion over that one path; and the count of lines matching
   `^- \[~\] F\d{3} — ` in the whole file is 1. Then, at C4:
   `python3 -m pytest tests/docs/ -q` and
   `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`, each its
   own REAL exit code. The reviewer measured both green at the base, 295 passed
   and 30 passed; report YOUR numbers.

G7 THE STATE READERS AND THE CANARY, at C6. Each its own REAL exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and the
   canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer
   measured these at the base at 515, 52, 21, 16 and 42 passed; report YOURS.

G8 THE INVENTORY AND THE TREE, at C6. `.agent/f258_inventory.md` exists and
   carries all six SPEC sections — report the heading line of each. Report the
   `file:line` count it cites and confirm every cited path resolves with
   `git ls-tree HEAD -- <path>`. Then `git status --porcelain` is EMPTY,
   `git ls-files --others --exclude-standard` has count 0, and the per-commit
   insertion counts for C0a through C6 from `git diff --numstat`, every one
   under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
state block, the `## Commits` table with a `+/-` column taken from
`git diff --numstat` (not from file line counts — those differ on a full-file
rewrite), the deviations, the item-status table with every bundle item and every
gate appearing exactly once, and the next steps. It states `SESSION 1` of F258
and round 1. It has NO length cap. Report the one candidate as discharged and
name R-0570 as OPEN and routed away from this branch.
