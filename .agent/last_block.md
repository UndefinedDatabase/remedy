── STEP T003 (5 of n) — F275 ─────────────────────────────────
Goal:        Resolve R-0870, and record the SECOND TYPE PAIR the flip carries —
             `Task` to `TaskEntry` — which no decision in this chain has
             measured and which DECISION F275 D21, written one round ago, does
             not name among the reasons its own union is still a floor.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 39
             verdict and two prose slips · C3 the R-0870 resolution · C4 the
             task-pair measurement · C5 the DECISION · C6 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r40.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `.agent/decisions.md`,
             `.agent/f275_t003_task_pair.md` (NEW),
             plus `.agent/handoff.md` at C6.
Constraints: the numbered list below.
Done when:   gates G1 to G8 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end of frame; the single pure rule line below is exactly 62 `─` characters
──────────────────────────────────────────────────────────────

## Base

This round's base is `6537ece6`. EVERY FIGURE BELOW WAS MEASURED by the reviewer
at that base, by importing the two shipped record types and by `ast` over the
tracked `.py` files, before this block was authored.

## What this round is, and why it is not a bookkeeping round

TWO THINGS. R-0870 is RESOLVED, by the reviewer's own re-run of both sweeps
against the committed tree — every hit either repaired across rounds 23, 36, 37,
38 and 39, or in the pattern this repository wants. And the flip gains a
measurement no decision in this chain has taken.

WHY THIS IS NOT THE ROUND amend0827-process-diet RULE 1 FORBIDS, stated because
the change set is entirely under `.agent/` and the rule deserves an answer rather
than a silence. Rule 1 forbids a round "whose whole change set is verdicts,
registrations or corrections". This round's substance is a MEASUREMENT taken this
round and a RULING drawn from it — the same shape as round 31, whose C3 wrote the
flip inventory and whose C4 recorded DECISION F275 D17 with no line outside
`.agent/` either, and which passed review on exactly that reading. The resolution
and the verdict booking ride with it rather than buying a round of their own,
which is what rule 1 asks for.

THE MEASUREMENT, AND WHY IT MATTERS MORE THAN ITS SIZE. `Job.tasks` is
`list[Task]` and `JobPlan.tasks` is `list[TaskEntry]`, so a consumer moved from
the classic record to the unified one moves BOTH types. DECISION F272 D15
measured the two JOB records as differing in `id` and `name` alone and wrote that
"the task vocabularies already agree because `TaskEntry(...).status ==
RunState.PENDING` evaluates True" — which is true of the STATUS field and says
nothing about the record SHAPE. Imported at this base, `Task` declares seven
fields and `TaskEntry` twenty-three, and they share exactly two names: `inputs`
and `status`. THREE `Task` FIELDS HAVE NO COUNTERPART OF THE SAME MEANING:
`budget`, `output_artifact_ids` and `acceptance_checks`, the last of which is a
list of structured checks against `TaskEntry.acceptance`, a single string. So the
flip is not a rename over this pair; it is a lossy record migration with an open
question inside it, and `output_artifact_ids` is READ at 35 sites on task-named
receivers, 15 of them production, including `packages/orchestration/task_runner.py`
and the cockpit's `packages/orchestration/brain_detail.py`.

WHAT THIS ROUND DOES NOT DO. It changes no production line and it does not widen
`TaskEntry`. The widen is the NEXT round's work and this decision specifies it,
because F272's own D5, D6 and D7 staged a record collapse as widen, then rename,
then retype, and the widen is the half that is green by construction.

## Constraints

1. APPLY EVERY SLICE BYTE FOR BYTE. Extract each by its delimiter lines from the
   committed `.agent/authored/f275-r40.md` and apply with `shutil.copyfile`
   semantics — never by retyping, never reflowed. If anything does not fit,
   DECLARE it in the handback and apply the rest.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6, exactly — eight commits,
   no extra, none dropped, no reordering. C1 is the first substantive commit and
   makes `.agent/plan.md` current before any other change, per §3 item 23. C3 is
   the RESOLUTION and stands in its own commit, per §4 item 4.
3. THE APPEND BASELINES, read by the reviewer at the base: `.agent/live_review.md`
   is 844533 bytes, `.agent/prose_slips.md` is 231842 bytes and
   `.agent/decisions.md` is 1049788 bytes, each ending in a newline. An append is
   pre-blob, then ONE newline, then the slice as extracted. Each later append
   re-baselines on the state the one before it left.
4. NO PATH OUTSIDE `.agent/` MOVES IN THIS ROUND AT ALL — not under `packages/`,
   `apps/`, `tests/`, `docs/` or `scripts/`.
5. THE TASK-PAIR FILE IS GENERATED, NEVER RETYPED. TASKTOOL is written to the
   gitignored `.remedy-wt/` scratch — never to a repository root, where
   `ruff check .` would collect it — run from the repository root, and its output
   is what C4 commits, with the tool's source embedded in the file so the
   measurement is reproducible from the artefact alone.
6. IDS REGISTERED THIS ROUND: none. IDS RESOLVED THIS ROUND: exactly one,
   `R-0870`. The open set is 87 by distinct id at the base and must read 86 at C5.
   That fall of one is the ONLY change to the set this round makes.
7. THE ROUND GATE IS TIER 1: the canary, plus the guard-file gate in G6. No
   production line moves, so no scoped suite beyond that is owed.
8. NO NUMERAL IN THE DECISION OR THE RESOLUTION IS RE-DERIVED BY THE WORKER. Both
   are slices and land byte for byte; G7 re-measures the figures they state and
   reports any difference rather than editing either side.

## SLICE PLAN40 → whole-file replacement of `.agent/plan.md`

<<<PLAN40
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 40 resolves R-0870 — every instance repaired across rounds 23, 36, 37, 38 and 39, and
both sweeps re-run by the reviewer against the committed tree — and records DECISION F275
D22: the flip carries a SECOND type pair, `Task` to `TaskEntry`, which no decision in this
chain has measured. The two share two field names of seven and twenty-three, and three
`Task` fields have no counterpart of the same meaning, one of them read at 35 sites.

## Next Steps

1. WIDEN `TaskEntry` with the fields DECISION F275 D22 names, in the shape F272's D5, D6
   and D7 staged a record collapse: widen first, because that half is green by construction
   and it shrinks the atomic commit that follows.
2. The flip itself, applied from the round 36 site enumeration, the round 38 seam list and
   the round 40 task-pair list, as the one declared-oversize commit AGENTS.md permits per
   feature, with the inseparability reason AND the real size stated in the handback BEFORE
   review.
3. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 2 is the largest single commit this repository will take, and each round that
  measures it has found it larger: DECISION F275 D17 sized it at 1766 changed lines, D21 at
  3771 across 263 files, and D22 adds a type pair worth 427 more across 111 files.
- The open set is 87 by distinct id at this round's base `6537ece6` and 86 after this round
  resolves R-0870. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per
  DECISION F272 D12.
PLAN40

## SLICE RECORD40 → append to `.agent/live_review.md`, in C2

<<<RECORD40
Gate: F275 R39 — the F275 round 39 entry. VERDICT PASS, written by the planner and reviewer of session 17 after reading the committed range `d341806e`..`6537ece6` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Seven single-parent commits C0a `846c42d8`, C0b `565c3775`, C1 `fa741579`, C2 `959b09dd`, C3 `a53234a3`, C4 `c39fc43a` and C5 `6537ece6`, per-commit insertions 341, 248, 16, 6, 11 and 68 for the six before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1: the reviewer's delegation source was written AND HASHED BEFORE delegation at `c4029f5ef7e84672c28b69fbbe4899d225ada084b82809afa25b130c3bf8e931`, and both committed copies are 27292 bytes at that digest as ONE shared git blob; per §3 item 37 that chain covers three on-disk artefacts and claims nothing about bytes emitted into a prompt. G2: `.agent/plan.md` byte-identical to PLAN39 at 2342 bytes, 42 lines against the cap of 50, both mandated headings exactly once. G3 OVER ALL FOUR APPENDS, each re-derived by the reviewer as a reconstruction from one COMMITTED blob to the next: `.agent/live_review.md` 839359 to 843601 at C2 and 843601 to 844533 at C3, `.agent/prose_slips.md` 230672 to 231842, `.agent/decisions.md` 1044462 to 1049788; every reconstruction byte-identical to the committed blob and every joining byte a newline; `^Gate: F275 R38 ` exactly 1 and `^## DECISION F275 D21 ` exactly 1. G4: THE OPEN SET IS 87 BY DISTINCT ID at the base and at C4; `R-0870` is in it with ZERO `Done:` lines and FIVE `Landed:` lines. G5: PAIR G reconstructs exactly — FROM 599 bytes over 8 lines at `ad158a65…` occurring 1x before and 0x after, TO 823 bytes over 11 lines at `e12b310f…` occurring 1x after, no trailing whitespace on either side, and the committed post-blob equal to the pre-blob with the paragraph replaced; `ruff` printed `All checks passed!`. G6: the guard's own four tests and the canary re-run by the reviewer together at 46 passed, exit 0. G7 EVERY FIGURE DECISION F275 D21 STATES REPRODUCED AT THIS BASE when the reviewer re-ran its own instrument: part (a) 1751 lines in 184 files, part (b) 820 in 152, part (c) 1294 in 201, the union 3771 lines across 263 files with 94 lines in more than one part and 79 files part (a) alone cannot see, and 7.5 times the DECISION F104 D1 cap. G8: the change set is an EXACT set match over eight paths with MISSING and EXTRA both empty, porcelain EMPTY, ONE worktree, `.agent/STOP` absent. THE WORKER'S THREE DEVIATIONS ARE ALL SUSTAINED AND THE FIRST IS THE VALUABLE ONE. G7's wording for part (c) left two definitional choices open — whether an `Attribute`-form `Job` call counts and whether annotation OCCURRENCES or annotated LINES are counted — and the worker measured BOTH readings rather than picking one, reporting 581/345/367 with a union of 3770 under the narrow reading and 582/345/368 with 3771 under the wide one, which is the reading the slice carries. It edited neither side, which constraint 8 required and which is why the difference is visible at all. SECOND, G3's clause about two appends sharing a commit was vacuous this round because C2's two appends hit two different files, and the worker declared that rather than reporting a proof it did not need to take. THIRD, no worktree was created because nothing destructive was ordered. ONE READING THE WORKER SURFACED AND THIS GATE CONFIRMS: the ledger holds EIGHTEEN `Done:` lines over SIXTEEN distinct ids, `R-0721` and `R-0725` each appearing twice, so the distinct-id arithmetic this workflow uses is what makes 103 minus 16 equal 87, and a line count would read 85. NO FINDING IS REGISTERED BY THIS GATE.
RECORD40

## SLICE SLIPS40 → append to `.agent/prose_slips.md`, in C2

<<<SLIPS40
2026-09-10 · F275 R39 · The round 39 block's G7 ordered part (c) of the flip measurement re-derived by "an `ast` pass counting `Job(...)` constructions, `Job` imports and `Job` annotations" and left two definitional choices open that change the answer: whether a call reached through an attribute — `models.Job(...)` — counts as a construction, and whether an annotation contributes one site per OCCURRENCE or one per LINE. The worker measured both readings, 3770 and 3771, and edited neither side. A gate that re-derives a figure states the DEFINITION the figure was measured under, not only the tool and the population, because two honest readings of the same corpus differ and the block cannot tell afterwards which one it meant.

2026-09-10 · F275 R39 · The round 39 block's G3 carried a clause telling the worker how to prove two appends that share one commit, and C2's two appends went to two different files, so every proof ran committed-blob to committed-blob and the clause governed nothing. It was written for round 38's shape and carried forward without re-reading the round's own append table. A conditional clause in a gate is checked against THIS round's change set before it is emitted, or it is one more sentence that reads as care and measures nothing — the same shape as the inert stem exclusion the round before it.
SLIPS40

## SLICE DONE40 → append to `.agent/live_review.md`, in C3

<<<DONE40
Done: R-0870 — RESOLVED at F275 round 40, by the reviewer of session 17, after re-running BOTH sweeps itself against the committed tree at `6537ece6` rather than accepting any worker reading. R-0870 recorded a claim falsified by a deletion in a place no gate can see, and it grew from two instances to ten across four `Landed:` batches and one widening. WHAT WAS REPAIRED, and by which round: `packages/common/public_text_redaction.py` and `packages/orchestration/decision_evidence.py` at round 23; the same redaction docstring's second, contradicting sentence and `tests/cli/test_mission_cmd.py`, whose test name and docstring argued for an assertion an earlier pair had removed, at round 36; `docs/system/test-lanes-v0.md`, which advertised two deleted suites as lanes, `docs/system/development-artifact-boundary-v0.md`, which said a deleted handler READS a file, and `tests/conftest.py`, which carried a deleted test file in `SUBPROCESS_FILES`, at round 37; that same page's "Planned migration path", which offered an operator the deleted `progress` command and listed the deleted `approval` group among the ones already using structured state, at round 38; and `tests/orchestration/test_event_name_coupling.py`, whose opening named the cluster-deletion-map ratchet without saying DECISION F275 D15 had retired it, at round 39. THE RESOLUTION READING, taken by the reviewer at `6537ece6` with two independent instruments. The MODULE-STEM sweep, over 90 deleted stems and 2255 tracked files outside `.agent/`, `docs/roadmap/` and `docs/archive/`, returns 42 hits of which 27 are inside `.data/evidence_exports/`, an archive of past runs this repository does not rewrite; every one of the remaining 15 is in a correct pattern — a sentence that names a deleted thing and says in the same breath that it is gone (`README.md`, both `docs/system/quality-baseline-v0.md` rows, `packages/orchestration/mission_readiness.py` twice, `packages/orchestration/provider_patch_material.py`, `packages/orchestration/token_policy.py`, `tests/cli/test_mission_cmd.py`, `tests/orchestration/test_event_name_coupling.py`, `docs/system/development-artifact-boundary-v0.md`), a landed DECISION paragraph in `docs/system/vocabulary.md` that records its own deletion, or a SURVIVING symbol whose name merely collides with a deleted module stem (`packages/orchestration/proposed_tasks.py` and its test). The COMMAND-SURFACE sweep, over the fifteen groups DECISION F260 D3 records as deleted whole, across 569 tracked files under `docs/`, `packages/` and `apps/`, returns 28 hits and NONE of them treats a dead group as live: the class that did held two at round 38's base and zero after C3 of that round. WHY NO GUARD CLOSES THIS CLASS, measured rather than preferred, because a resolution that leaves the obvious counter-measure unexplained invites the next reader to build it. A guard over `packages/`, `apps/`, `tests/` and `scripts/` asserting that every module path a source file names resolves on disk would have to accept 320 non-resolving paths in 94 of 1116 files, and almost every one is a TEST FIXTURE — `packages/widget.py`, `tests/a.py`, `docs/guide.md` — invented to exercise a path-handling code path. That is the same measurement by which DECISION F275 D16 refused to widen `tests/docs/test_named_source_paths.py` past the two operator-facing trees, arriving from the other side, and the allowlist such a guard would need is longer than the property it guards. The two sweeps stay as the instrument, their recipes are on the record in the `Note: F275 R24` and `Note: F275 R38` entries, and the widened fix clause both notes carry binds every remaining round of this feature.
DONE40

## SLICE TASKTOOL → written to `.remedy-wt/r40_task_pair.py`, run, and EMBEDDED in the file C4 commits

<<<TASKTOOL
"""F275 T003 — the SECOND type pair, measured: `Task` against `TaskEntry`.

`Job.tasks` is `list[Task]` and `JobPlan.tasks` is `list[TaskEntry]`, so a
consumer moved from the classic record to the unified one moves both types. This
reads the two shipped classes rather than their source, then counts the `Task`
type sites the flip must carry, then asks whether the fields with no counterpart
are READ anywhere — which is what decides whether the flip owes a finding under
operator amendment amend0908-f275-finish rule 4.
"""
import ast
import collections
import dataclasses
import subprocess

from packages.core.models import Task
from packages.orchestration.pingpong_job import TaskEntry

ORPHANS = ("budget", "output_artifact_ids", "acceptance_checks")


def annotation_names(node, depth=0):
    out = set()
    if node is None or depth > 3:
        return out
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            try:
                out |= annotation_names(ast.parse(n.value, mode="eval").body, depth + 1)
            except SyntaxError:
                pass
    return out


def params(n):
    a = n.args
    return (list(a.posonlyargs) + list(a.args) + list(a.kwonlyargs)
            + [x for x in (a.vararg, a.kwarg) if x is not None])


def main():
    task_fields = dict(Task.model_fields)
    entry_fields = {f.name: f for f in dataclasses.fields(TaskEntry)}
    print("Task fields:", len(task_fields))
    for name, f in task_fields.items():
        print(f"    {name} :: {f.annotation}")
    print("TaskEntry fields:", len(entry_fields))
    for name, f in entry_fields.items():
        print(f"    {name} :: {f.type}")
    shared = sorted(set(task_fields) & set(entry_fields))
    print("shared names:", shared)
    print("Task-only names:", sorted(set(task_fields) - set(entry_fields)))

    files = subprocess.run(["git", "ls-files", "*.py"],
                           capture_output=True, text=True).stdout.split()
    kinds = collections.Counter()
    lines = set()
    reads = collections.defaultdict(list)
    for path in files:
        try:
            tree = ast.parse(open(path, "rb").read(), filename=path)
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                    and n.func.id == "Task":
                kinds["constructions"] += 1
                lines.add((path, n.lineno))
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                if any(a.name.split(".")[-1] == "Task" for a in n.names):
                    kinds["imports"] += 1
                    lines.add((path, n.lineno))
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in params(n):
                    if "Task" in annotation_names(arg.annotation):
                        kinds["annotations"] += 1
                        lines.add((path, arg.lineno))
                if "Task" in annotation_names(n.returns):
                    kinds["annotations"] += 1
                    lines.add((path, n.lineno))
            elif isinstance(n, ast.AnnAssign) and "Task" in annotation_names(n.annotation):
                kinds["annotations"] += 1
                lines.add((path, n.lineno))
            if isinstance(n, ast.Attribute) and n.attr in ORPHANS:
                recv = n.value.id if isinstance(n.value, ast.Name) else None
                reads[n.attr].append((path, n.lineno, recv))

    hit = {p for p, _ in lines}
    prod = {p for p in hit if not p.startswith("tests/")}
    print("Task type sites:", dict(kinds))
    print(f"distinct changed lines {len(lines)} in {len(hit)} files,"
          f" production {len(prod)}, test {len(hit) - len(prod)}")
    for f in ORPHANS:
        h = reads[f]
        p = [x for x in h if not x[0].startswith("tests/")]
        t = [x for x in h if x[2] and "task" in x[2].lower()]
        print(f"{f}: {len(h)} attribute reads, {len(p)} production,"
              f" {len(t)} on a receiver named *task*")
        for x in sorted(set(t)):
            print(f"    {x[0]}:{x[1]}  receiver {x[2]}")


if __name__ == "__main__":
    main()
TASKTOOL

## SPEC-TASK → the NEW file `.agent/f275_t003_task_pair.md`, GENERATED at C4

Write TASKTOOL to `.remedy-wt/r40_task_pair.py`, run it from the repository root,
and build the file from its real output.

THE FILE'S SECTIONS, numbered so that the banner IS section 1 and no offset is
left for a reader to resolve.
  1. A banner naming the base SHA and stating that no line under `packages/`,
     `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.
  2. The instrument: TASKTOOL's source embedded verbatim in one fenced python
     block, and the exact command line used.
  3. The two record shapes, field by field, as the tool prints them, with the
     shared names and the `Task`-only names called out.
  4. The `Task` type sites: the three kinds, the distinct changed lines, the file
     count and the production and test split.
  5. The orphan fields: for each, the attribute-read count, the production count
     and the full list of reads on a receiver named `*task*`, never truncated.
  6. A figures table with a `measured` column, a `reviewer` column carrying the
     numbers below, and a `verdict` column reading `same` or `differs (<n>)`.

THE REVIEWER'S FIGURES, measured at `6537ece6`:
  `Task` fields 7 · `TaskEntry` fields 23 · shared names 2 (`inputs`, `status`)
  `Task`-only names 5 — `acceptance_checks`, `budget`, `description`, `id`,
  `output_artifact_ids`
  `Task` type sites — constructions 246, imports 142, annotations 40
  distinct changed lines 427 in 111 files — production 15, test 96
  `budget` 45 attribute reads, 24 production, 0 on a `*task*` receiver
  `output_artifact_ids` 58 attribute reads, 15 production, 35 on a `*task*` receiver
  `acceptance_checks` 5 attribute reads, 3 production, 1 on a `*task*` receiver

## SLICE AMEND40 → append to `.agent/decisions.md`, in C5

<<<AMEND40
## DECISION F275 D22 (2026-09-10, F275 round 40) — the flip carries a SECOND type pair, `Task` to `TaskEntry`, which no decision in this chain has measured; and it is landed by WIDENING first

WHAT THIS AMENDS. DECISION F275 D21, recorded one round ago, measured the flip's floor over
three parts and named ONE reason that floor is still a floor: the sites that treat a job id
as a UUID. It did not name this one, and this paragraph is its dated correction rather than
a rewrite, per planner_reviewer_prompt.md §3 item 20. DECISION F272 D15 is the origin of the
gap and is also not rewritten: it measured the two JOB records as differing in `id` and
`name` alone and wrote that "the task vocabularies already agree because `TaskEntry(...).status
== RunState.PENDING` evaluates True". That sentence is TRUE of the `status` FIELD and was
read, by every decision after it, as a statement about the task RECORD. It is not one.

THE MEASUREMENT, taken by the reviewer at `6537ece6` by IMPORTING the two shipped classes
rather than reading their source, and by `ast` over the tracked `.py` files. `Job.tasks` is
`list[Task]` and `JobPlan.tasks` is `list[TaskEntry]`, so a consumer moved from the classic
record to the unified one moves BOTH types. `Task` declares seven fields and `TaskEntry`
twenty-three, and they share exactly TWO names: `inputs` and `status`. The `Task` type sites
the flip must carry are 246 constructions, 142 imports and 40 annotations over 427 distinct
changed lines in 111 files, 15 production and 96 test — which the union DECISION F275 D21
states does not contain, because that union was computed over `Job` alone.

THE THREE FIELDS WITH NO COUNTERPART OF THE SAME MEANING, and this is why the pair is a
migration rather than a rename. `Task.budget` is a `Budget` and `TaskEntry` has no per-task
budget at all. `Task.output_artifact_ids` is a `list[UUID]` and `TaskEntry` has no artifact
list; it is READ at 35 sites on task-named receivers, 15 of them production, including
`packages/orchestration/task_runner.py`, which is the live runner, and
`packages/orchestration/brain_detail.py`, which is the cockpit's detail panel. And
`Task.acceptance_checks` is a `list[AcceptanceCheck]` against `TaskEntry.acceptance`, which
is a single `str` — a structured list against a sentence, which is a lossy mapping and not a
rename. `Task.id` maps onto `TaskEntry.task_id`, a `str` where `Task.id` is a `UUID`, which
is the same shape change D21 records for the job id. `Task.description` has TWO candidates
on the unified record, `TaskEntry.title` and `TaskEntry.body`, and this decision does not
choose between them: that is a reading of what each field means to its consumers, the widen
does not need it, and the flip round makes it against the sites it is actually moving.

CHOSEN: THE PAIR IS LANDED BY WIDENING `TaskEntry` FIRST, IN ITS OWN COMMIT, BEFORE THE
FLIP. `TaskEntry` gains the fields it lacks with defaults, and `_export_job` and `_import_job`
gain them symmetrically, so an older job file loads unchanged and a newer one round-trips.
That commit is GREEN BY CONSTRUCTION — nothing reads the new fields yet, no classic consumer
moves, and the record on disk gains keys rather than losing them — and it SHRINKS the atomic
commit that follows by everything it carries. The precedent is this chain's own: DECISION
F272 D5, D6 and D7 staged the `state` collapse as WIDEN, then RENAME, then RETYPE, for
exactly this reason. A widen is not the compatibility reader AGENTS.md's Scope Control
forbids: the classic record still dies in the flip, and nothing is left alive beside its
replacement.

WHAT THE WIDEN MUST CARRY, and what it must NOT. It carries `output_artifact_ids`, because
35 sites read it and 15 of those are production, so deleting it is a user-observable loss
that operator amendment amend0908-f275-finish rule 4 would otherwise force this feature to
register as a finding against an inheriting feature that does not exist. It carries the
per-task `budget`, whose absence would silently remove a limit rather than a display. It
does NOT carry `acceptance_checks` as a structured list: `TaskEntry.acceptance` already
holds the acceptance text and the mapping is lossy in the direction the flip travels. The
measurement behind that, stated as what was counted rather than as a conclusion: the name is
read as an ATTRIBUTE at five sites, three of them production, and NOT ONE of those three is
on a receiver named `*task*` — they read a planner output — while the single task-named
attribute read is in a test. Its other production occurrences are keyword arguments at sites
that CONSTRUCT a `Task`, and those die with the classic record rather than consuming the
unified one. So the flip round registers the structured form as a finding naming the feature
that owns acceptance criteria, per rule 4, rather than inventing a home for it here.

ALTERNATIVES CONSIDERED. (i) Carry the pair inside the one oversize flip commit — rejected
on arithmetic and on risk: it adds 427 lines to a commit DECISION F275 D21 already measures
at 7.5 times the cap, and it puts a lossy record migration inside the one commit in this
feature that cannot be split. (ii) Map `Task.output_artifact_ids` onto an existing
`TaskEntry` field — rejected on the measurement: `safe_diff_files` and `apply_manifest` are
about the DIFF a task produced, not about artifacts it registered, and re-pointing a reader
at a differently-meaning field is the gate-that-lies class this record exists to prevent.
(iii) Delete the three fields and register three findings — rejected for
`output_artifact_ids` on its 35 readers, accepted for `acceptance_checks` alone, which is
what the clause above rules.

HOW TO REVERSE: delete this decision. DECISION F275 D21's union then stands as the flip's
stated size, understating it by 427 lines and by a lossy record migration, which is the
state this measurement was taken to end.
AMEND40

## Done when — GATES G1 to G8

Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL exit code
and the real numbers. "Green" as a word is a finding. One line per gate in the
handback. Where a gate names both a COUNT and an EXIT CODE, report both.

**G1 TRANSPORT (at C0b).** The committed `.agent/authored/f275-r40.md` and
`.agent/last_block.md` have the SAME sha256 as the reviewer's delegation source,
and resolve to ONE shared git blob. `.agent/last_block.md` is written from
`git cat-file blob HEAD:.agent/authored/f275-r40.md`, never retyped. State that
the chain covers those on-disk artefacts and claims nothing about emitted bytes.

**G2 THE PLAN (at C1).** `.agent/plan.md` is BYTE-EQUAL to the PLAN40 slice as
extracted — same length, same sha256. Report its line count against the
AGENTS.md cap of 50, and `^## Goal$` and `^## Next Steps$` each exactly 1.

**G3 THE RECORD (at C2, C3 and C5).** For each of the four appends — RECORD40 and
SLIPS40 at C2, DONE40 at C3, AMEND40 at C5 — post-blob equals pre-blob then ONE
newline then the slice, with constraint 3's baselines and each later append
re-baselining on the state the one before it left; every pre-blob and post-blob in
this round is a COMMITTED blob, because no two of the four share both a commit and
a file. READ BACK the joining byte at each offset and report it. Then an
INDEPENDENT structural reader with N COUNTED FROM EACH SLICE and not from this
block. Then one negative control per append, flipping a byte INSIDE THE FIRST
appended paragraph, which BOTH readers must REJECT. `^Gate: F275 R39 ` exactly 1,
`^Done: R-0870 ` exactly 1 and `^## DECISION F275 D22 ` exactly 1 at C5.

**G4 THE OPEN SET (at C5).** BY DISTINCT ID, every `^- R-\d+ — ` id minus every
`^Done: R-\d+ — ` id, read at THIS round's base `6537ece6` with
`git show 6537ece6:.agent/live_review.md` into memory — never by writing over the
tracked file — and again at C5. The reviewer read 87 at the base and expects 86 at
C5. Report both, and report the ids registered this round — which must be `[]` —
and the ids resolved this round — which must be exactly `['R-0870']`. Report
SEPARATELY that `R-0870` is ABSENT from the open set at C5 and that the count of
`^Done: R-0870 ` lines is 1, so the resolution is present exactly once.

**G5 THE RESOLUTION IS THE AUTHORED BYTES (at C3).** The committed
`.agent/live_review.md` at C3 ends with the DONE40 slice byte for byte, and the
FIVE `^Landed: R-0870` lines that precede it are UNCHANGED — count them at the
base and at C3 and report both, because §3 item 20 forbids rewriting landed text
and a resolution that quietly tidied its own history would be the worse failure.

**G6 NOTHING BROKE (at C5).** The canary
`python3 -m pytest tests/cli/test_golden_path.py -q`, and
`python3 -B -m pytest tests/orchestration/test_event_name_coupling.py -q`, which
the reviewer read at 42 and 4 passed. No production line moves this round, so no
wider suite is owed; say so rather than running one.

**G7 THE DECISION'S FIGURES (at C4 and C5).** Re-measure everything SPEC-TASK
states, from the tool's own output, and report every figure beside the reviewer's
with a `same` or `differs (<n>)` verdict. Per constraint 8 the slices are NOT
edited if a figure differs — report both sides and say so in the handback. Then
three properties of the committed task-pair file: its section numbering runs 1 to
6 with the banner AS section 1; its orphan-field lists are untruncated; and every
path it names resolves on disk at C4.

**G8 NOTHING ELSE MOVED (at C5).** `.agent/STOP` read FROM DISK: report present
or absent. `git status --porcelain`: EMPTY. `git worktree list`: exactly ONE
entry. `git diff --name-only 6537ece6..C5` is an EXACT SET MATCH against the
`Change:` list above minus `.agent/handoff.md` — report MISSING and EXTRA
explicitly, and report that ZERO paths outside `.agent/` appear in it, which is
constraint 4. Per-commit insertions for C0a through C5, each under the DECISION
F104 D1 cap of 500; the handback commit's own numbers are NOT ordered here,
per §3 item 14.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
SESSION 17 of F275 and round 40, the per-commit table with `git diff --numstat`
values in the `+/-` column, one line per gate G1 to G8 with real exit codes, the
item-status table, the open-findings count by distinct id, and the deviations.
State explicitly that R-0870 IS resolved by this round and that the open set falls
from 87 to 86. Add the one sentence of context self-assessment
amend0905-throughput requires. No PR is created and nothing is merged: this round
is not a closure sequence.
