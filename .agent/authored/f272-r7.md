── STEP T002 (the eight administrative fields) — F272 ─
Goal:        Give `JobPlan` the EIGHT administrative fields of DECISION F260 D1
             that have no counterpart on it today, wired through `_export_job`
             AND `_import_job` so they survive a persist/resume cycle, with a
             test file that pins each one and a mutation red-proof that shows
             the pins can fail.
Bundle:      C0a save the block · C0b mirror · C1 the plan · C2 the round 6
             gate entry, finding R-0819 and the two prose slips · C3 the eight
             fields on the dataclass · C4 the export and import wiring ·
             C5 the test file · C6 the handback.
Change:      EXACTLY the paths listed under "The change set" below and nothing
             else.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 1, and
this line carries one run of 2. Both readings were measured, not recalled.

## Where this round stands

T001 is COMPLETE. Round 6 moved the last 132 test-side callers onto `run_dir`
and `runs_dir` and deleted both ping-pong spellings; the reviewer re-measured
every gate independently and neither spelling occurs anywhere in the tree.

T002 is "the rest of the unified record". DECISION F260 D1 names ELEVEN
administrative fields for the one job record: `artifacts`, `budget`, `fences`,
`flight_plan`, `intake`, `mission`, `name`, `project_id`, `state`,
`user_prompt`, and `id`. THREE of them already have a spelling on `JobPlan` and
are NOT this round's work — `id` is the 16-hex `job_id` D2 rules, `name` is
`job_title`, and `state` collides with `status`, which D1 rules must become ONE
field of type `RunState` with the bare string spelling dropped. That collapse is
a type change with wide reach and it is the NEXT round, not this one.

This round adds the other EIGHT, which are pure additions and collide with
nothing.

## What the reviewer read before ordering this (§3 item 34)

Read at `df955058`, and each of these is a fact the round depends on:

- `_export_job` (`packages/orchestration/pingpong_job.py:629`) and `_import_job`
  (same file, line 739) are EXPLICIT field-by-field functions. There is no
  `asdict` and no `**data` splat. A field added to the dataclass and to neither
  of them is a Python-only attribute that VANISHES on the first persist/resume
  cycle — the trap the `metadata` field's own comment at line 374 warns about.
  Wiring both is therefore the substance of this round, not an afterthought.
- `run_refs`, which F272 round 1 added, IS correctly wired into both: line 696
  in the exporter and line 794 in the importer. Copy that field's shape.
- NO test pins `JobPlan`'s field set as a closed collection. The reviewer
  searched `tests/` for `__dataclass_fields__`, `fields(JobPlan)` and
  `set(asdict(` : the hits are over `PromotionAssertionResults`,
  `RepositoryRevertResult`, `SnapshotCreateResult`, `SnapshotVerification`,
  `DurableApplyRecord` and `PingPongResult`, and none over `JobPlan`. Additive
  fields are therefore safe and no existing guard goes red.
- No test counts a string over `pingpong_job.py` as a whole-file `count(...)`
  or `== 1` assertion, so nothing here is made unsatisfiable by a source guard
  (§3 item 7).
- `tests/orchestration/test_job_run_refs.py` is the shape to follow: it imports
  `JobPlan`, `_export_job`, `_import_job` and `load_job_plan`, and pins the
  field, its default, its persistence and its defaulted read for a record
  written without the key.

## The change set

C3 and C4: `packages/orchestration/pingpong_job.py`.
C5: `tests/orchestration/test_job_administrative_fields.py` (NEW FILE).
C0a/C0b/C1/C2/C6: `.agent/authored/f272-r7.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/prose_slips.md`,
`.agent/handoff.md`.

Those are the paths of this round and there are no others. Nothing under
`docs/`, nothing under `apps/`, no other file under `packages/`.

## C3 — the administrative fields, a SPEC and not a slice

Add these eight fields to the `JobPlan` dataclass
(`packages/orchestration/pingpong_job.py`, the class beginning at line 293),
placed together as one block at the END of the field list, directly after
`metadata`, under one comment naming F272 T002 and DECISION F260 D1 as their
source. Keep `JobPlan`'s OWN conventions, which the reviewer read off the
existing fields rather than inventing:

| field | type and default |
|---|---|
| `mission` | `str = ""` |
| `user_prompt` | `str = ""` |
| `project_id` | `str = ""` |
| `intake` | `dict \| None = None` |
| `flight_plan` | `dict \| None = None` |
| `artifacts` | `list[Artifact] = field(default_factory=list)` |
| `budget` | `Budget \| None = None` |
| `fences` | `JobFences \| None = None` |

Two conventions are being followed here rather than chosen, and the round says
so: `JobPlan` spells an absent string `""` and never `None` (see `job_title`,
`error`, `worktree_branch` and every other string field), and it spells an
absent structured value `None` (see `target_guard`, `execution_config`,
`budgets`, `budget_actuals`). The classic `Job` in `packages/core/models.py`
spells `mission`, `user_prompt` and `project_id` as `str | None`; the empty
string is the spelling that survives here, because this is the record that
survives, and a reader that must distinguish "unset" from "empty" for these
three does not exist yet — if T003 finds one, it is a finding and a ruling, not
a silent change.

`Artifact`, `Budget` and `JobFences` are Pydantic models in
`packages.core.models`. Import them at MODULE level in `pingpong_job.py` if that
module does not already import them; if ruff's `I001` reorders the import block
as a consequence, that is a consequence of the ordered lint gate and not a
choice — apply it with `python3 -m ruff check --fix --select I001` on that file
alone and declare it.

`budget` is `Budget | None` and NOT a `Budget()` default factory, even though
the classic `Job` defaults it to `Budget()`. Reason, stated so it is not read as
a slip: an empty `Budget` and an absent one are indistinguishable on disk once
exported, and `JobPlan` already carries `budgets` for the F018 limits, so a
defaulted second budget object would put a meaningless `{}` into every job
record ever written. `None` means absent and says so.

## C4 — the export and import wiring

In `_export_job`, add one key per field, in the SAME ORDER as the dataclass
block, beside the existing `"run_refs": job.run_refs` entry. The three
model-valued fields are dumped to plain JSON data, never left as model objects:
`[a.model_dump(mode="json") for a in job.artifacts]`,
`job.budget.model_dump(mode="json") if job.budget else None`, and
`job.fences.model_dump(mode="json") if job.fences else None`. The five others
are exported verbatim.

In `_import_job`, add the matching reads, each DEFAULTING when the key is
absent, in the same manner as `run_refs=list(data.get("run_refs") or [])` —
a job record written before this round must still load. The model-valued three
are reconstructed: `[Artifact(**a) for a in (data.get("artifacts") or [])]`,
`Budget(**b) if (b := data.get("budget")) else None`, and
`JobFences(**f) if (f := data.get("fences")) else None`. If a walrus inside the
argument list reads badly against the surrounding code, use a plain local — the
requirement is the DEFAULTING BEHAVIOUR, not the spelling.

C3 and C4 are two commits over one file on purpose: the dataclass change alone
is a record that cannot persist its new fields, and reading that intermediate
state in isolation is what makes the C4 diff legible.

## C5 — the test file

NEW FILE `tests/orchestration/test_job_administrative_fields.py`, following
`tests/orchestration/test_job_run_refs.py`'s shape and its module docstring
convention. It pins, at minimum:

1. **Defaults.** A bare `JobPlan()` has each of the eight at its documented
   default, and the two mutable ones (`artifacts`) are NOT shared between two
   instances — the `default_factory` property, tested as
   `first.artifacts is not second.artifacts`.
2. **Round trip, all eight at once.** Build a `JobPlan` with every one of the
   eight set to a distinguishable non-default value, including at least one
   real `Artifact`, a `Budget` with a set field and a `JobFences` with a
   non-empty `allow` list. Pass it through
   `_import_job(json.loads(json.dumps(_export_job(plan))))` — the `json` round
   trip is REQUIRED and not decoration, because it is what proves the exporter
   emitted JSON-serialisable data rather than model objects. Assert each of the
   eight equals what went in, field by field, with eight separate assertions so
   a failure names the field.
3. **The defaulted read.** `_import_job({})` and `_import_job` over a dict
   holding only the pre-existing keys both return a `JobPlan` whose eight fields
   are at their defaults, and neither raises. This is the old-record path.
4. **Through the real writer and reader.** `save_job_plan` then
   `load_job_plan(job_id)` with an isolated data root, asserting the eight
   survive the actual file. Use the same data-root isolation
   `test_job_run_refs.py` uses; do NOT write into the configured data root
   (open finding R-0803).

Every test carries a one-sentence docstring saying WHAT it pins and why that
could break, per this repository's convention.

## Constraints

1. NO SLICE IS EDITED. Apply the authored texts byte for byte between their
   markers. If one looks wrong, apply it anyway and say so in the handback.
   C3, C4 and C5 are a SPEC, not slices: write the code yourself to the
   description above.
2. The paths listed under "The change set" are the whole change set.
3. Commit order C0a, C0b, C1, C2, C3, C4, C5, C6, nothing reordered. C1 is the
   first substantive commit (§3 item 23).
4. APPEND CONVENTION for `.agent/live_review.md` and `.agent/prose_slips.md`:
   `post == pre + b"\n" + slice`, the slice being the lines between the markers
   each carrying its own terminating newline, and the post-image ending in
   exactly one `\n`.
5. PLAN CONVENTION: `.agent/plan.md` is REPLACED by exactly the PLANF272R7 slice
   bytes and nothing else.
6. Behaviour changes: NONE for any existing field, any existing caller or any
   existing record. Every job record already on disk must load unchanged, which
   is what gate G4's defaulted-read half measures.
7. Mint NO finding id of your own and write NO `Done:` paragraph of your own.
   R-0819 is authored below and is applied verbatim; it is NOT resolved this
   round.
8. Destructive verification goes in a disposable `git worktree` under the
   gitignored `.remedy-wt/`, never in the primary checkout (protocol G5).
   Remove and prune it before the handback, BY EXACT PATH and never by glob.
9. Read `.agent/STOP` with `os.path.exists` three times — before C0a, before C3
   and before C6 — and table all three. If it appears, finish only the
   half-written commit, then hand off (protocol G6).
10. `python3 -B` for every run; purge `__pycache__` in any worktree before a run.
11. Report each gate's REAL exit code. "Green" as a word is a finding (G4).

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r7.md` and `.agent/last_block.md`; both equal each other
and the BLOCK_SHA and length the delegation names. Per §3 item 37 this covers
the saved copy and its mirror, not the bytes emitted into your prompt; say so.

**G2 THE RECORD, at C2.** Four readers over `.agent/live_review.md`, readers (a)
and (b) over `.agent/prose_slips.md`.
(a) BYTE: pre and post lengths; pre a byte-exact prefix; `post == pre + b"\n" +
slice`; pre's terminal byte asserted to be exactly one `\n` BEFORE writing; post
ends in exactly one `\n`.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`, with N COUNTED BY YOUR SCRIPT from the slice's own paragraphs and never
taken from this block: units before, after, delta; the last N units equal the
slice's paragraphs IN ORDER; the units before an unchanged prefix.
(c) NEGATIVE CONTROL in memory on a `bytes` object, never on disk: flip a byte
inside the FIRST appended paragraph, asserting the offset lies inside it before
flipping; readers (a) and (b) must BOTH reject; restore and require both to
accept and the restored image to equal the disk image.
(d) COUNTS before → after C2: distinct `^- R-\d{4} — ` ids 302 → 303; distinct
`^Done: R-\d{4} — ` ids 247 → 247; open set BY DISTINCT ID 55 → 56;
`^- R-0819 — ` 0 → 1; `^Gate: ` 28 → 29; `^Gate: F272 R6 ` 0 → 1.

**G3 THE PLAN, at C1.** `.agent/plan.md` equals the PLANF272R7 slice bytes
exactly; report the equality and both byte lengths. Line count under the
AGENTS.md cap of 50. `## Goal` and `## Next Steps` both present.

**G4 THE FIELDS EXIST AND SURVIVE A ROUND TRIP, at C4.** Measured from the
SHIPPED module by importing it, never from its source text.
(i) For each field name in the C3 table, report `name in
JobPlan.__dataclass_fields__` — every one TRUE. NON-VACUITY CONTROL beside them:
report the same reading for `run_refs` (must be TRUE) and for a name that does
not exist, `no_such_administrative_field` (must be FALSE), so those TRUEs are not
measuring a membership test that answers TRUE for everything.
(ii) Build a `JobPlan` with every field of the C3 table set to a non-default
value, run it through
`_import_job(json.loads(json.dumps(_export_job(plan))))`, and report per field
whether the value survived — one reading per row of that table, printed one per
line.
(iii) THE DEFAULTED READ: `_import_job({})` returns without raising and its
fields from that table equal a bare `JobPlan()`'s. Report each comparison.

**G5 THE PINS CAN FAIL — MUTATION RED-PROOF, in a disposable worktree at the
commit C5 creates.** Purge `__pycache__` first and confirm `pingpong_job`
resolves from INSIDE the worktree by printing its `__file__`.
FIRST the UNMUTATED CONTROL, in that same worktree and BEFORE any mutation:
`python3 -B -m pytest tests/orchestration/test_job_administrative_fields.py -q
-p no:randomly` must be EXIT 0; report its summary line. A colour with no
baseline is not evidence (§3 item 33).
THEN, for EACH field of the C3 table separately, delete that field's single
export line from `_export_job` in the worktree's own copy of
`packages/orchestration/pingpong_job.py` — counting those exact bytes IN THAT
FILE first, where the count must be 1, and choosing a longer unique byte string
if it is not (§3 item 25) — re-run the same command, and require EXIT 1 with the
failure naming that field. Restore the line and confirm the control is EXIT 0
again before moving to the next field. Report one exit code per row of that
table and the field each names. A field whose deletion leaves the run GREEN is a
test that pins nothing, and it is a finding of this round rather than something
to fix quietly.

**G6 THE SUITES, at C5, run SERIALLY, each its own invocation.**
`tests/orchestration/test_job_administrative_fields.py`, then
`tests/orchestration/`, then `tests/cli/`, then the canary
`tests/cli/test_golden_path.py`. Every one EXIT 0. Report each exit code and
each summary line verbatim. The reviewer measured at `df955058`:
`tests/orchestration/` 12809 passed and 10 skipped, `tests/cli/` 1537 passed,
canary 42 passed. A LOWER count in any of them is a finding, not a rounding;
`tests/orchestration/` is expected to RISE by exactly the tests C5 adds.

**G7 LINT AND INTEGRITY, at C5.** `python3 -m ruff check` over exactly the two
changed `.py` files in ONE invocation: EXIT 0. If it goes red, report the codes
and do NOT fix anything outside the change set. A repo-wide `ruff check .` is NOT
ordered: it is EXIT 1 at 26 errors on base and on `main` under OPEN finding
R-0468. `python3 -m apps.cli.grouped integrity check --json`: EXIT 0,
`"passed": true`, `"fail_count": 0`.

**G8 THE TREE.** `git status --porcelain` EMPTY when C6 is staged.
`git ls-files .remedy-wt` EMPTY. `git worktree list` naming any worktree you
created and confirming its removal; the twelve pre-existing `remedy/job-*`
entries predate this round and stay. Per commit for C0a through C5 — NOT C6,
which cannot count its own insertions (§3 item 14) — the insertion count from
`git diff --numstat <parent> <commit>`, each under the DECISION F104 D1 cap of
500, each single-parent. Those same per-commit numbers are what the handback's
`## Commits` table must carry in its `+/-` column, so report the two readings
side by side and confirm each row's insertion figure against
`git diff --numstat` cell by cell (§3 item 28): a full-file rewrite is where the
file's line counts and the diff's columns diverge, and `.agent/last_block.md` is
exactly such a rewrite this round. Marker sweep: zero lines beginning
`<<<BEGIN ` or `<<<END ` in every written non-block file. The three
`.agent/STOP` readings of constraint 9, as a table.

## The slices

<<<BEGIN PLANF272R7>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1, 3, 4, 5 and 6 PASSED; round
2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE: the run
re-key, the repository-wide spelling sweep and the name collapse have all landed.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

T002 begins. This round gives `JobPlan` the eight administrative fields of
DECISION F260 D1 that have no counterpart on it today — `mission`,
`user_prompt`, `project_id`, `intake`, `flight_plan`, `artifacts`, `budget` and
`fences` — wired through both `_export_job` and `_import_job`, which are
explicit field-by-field functions, so the fields survive a persist/resume cycle
rather than existing only in memory. A new test file pins each field, the whole
round trip through JSON, and the defaulted read that keeps older records
loadable.

## Next Steps

1. The three administrative fields that COLLIDE with an existing spelling:
   `id` is already the 16-hex `job_id`, `name` is `job_title`, and `state` must
   absorb `status` as one `RunState` field with the bare string dropped. The
   last of those is a type change with wide reach and needs its own ruling.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each with a test that proves it works on a job created
   through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A field added to the dataclass and to neither writer is a Python-only
  attribute that vanishes on the first persist/resume cycle. That is why the
  round trip through `json.dumps` is the gate rather than a field-presence read.
- Older job records on disk carry none of the new keys and must still load, so
  every import reads through a default.
<<<END PLANF272R7>>>

<<<BEGIN RECORDR7>>>
Gate: F272 R6 — the F272 round 6 entry. VERDICT PASS, AND T001 IS COMPLETE; THE ONE DEFECT OF THE ROUND IS THE REVIEWER'S OWN GATE TEXT AND IS REGISTERED BELOW AS R-0819. Range `61c4bd2e`..`df955058`, ten commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8 with nothing added, dropped or reordered; `git diff --name-only` over the range lists exactly 33 paths, which is the block's own ENUMERATION and not the numeral 29 that stood beside it. THE COLLAPSE IS TOTAL AND THE REVIEWER MEASURED IT RATHER THAN READING IT. Over all 1063 tracked `.py` files enumerated from `git ls-files` in Python, `\bpingpong_runs?_dir\b` occurs ZERO times, including inside `data_paths.py`; importing the SHIPPED `packages.orchestration.data_paths` from `/home/decodeux/Repos/remedy/packages/orchestration/data_paths.py` gives `hasattr` FALSE for both deleted names and TRUE for `run_dir` and `runs_dir`, which is the non-vacuity control that distinguishes a deletion from an import failure. THE SHAPE ASSIGNMENT RECONCILES INDEPENDENTLY. Counting over the 27 changed `.py` files, the base image carries 137 occurrences of the two ping-pong spellings — 132 test-side plus the 5 inside `data_paths.py` — and the round's own image carries exactly 34 call sites spelled `data_paths.run_dir(` or `data_paths.runs_dir(`, which is the shadowed count the block predicted; the per-file split 46/23, 9/1, 8/4, 3/2, 2/1, 2/1, 2/1 and 2/1 reproduces the block's table cell for cell. NO COVERAGE WAS LOST AND THE REVIEWER CHECKED THE SURVIVING PINS BY READING THEM. `tests/test_data_paths.py` collects 51 at `61c4bd2e` and 50 at `df955058`, the difference being exactly the deleted alias test, and the four surviving pins really do carry all four properties that test asserted: `test_runs_dir_explicit_root` pins the explicit root, `test_runs_dir_default` the default root, `test_a_run_hangs_under_runs_dir_and_never_under_jobs_dir` the `run_dir(rid) == runs_dir() / rid` identity and its `.parent`, and `test_the_root_override_is_honoured_by_all_four` the env-root-versus-argument guard the deleted test spelled out. Those four run EXIT 0 at 4 passed. THE SUITES WERE RE-RUN BY THE REVIEWER, NOT READ: `tests/test_data_paths.py` EXIT 0 at 50 passed, `tests/orchestration/` EXIT 0 at 12809 passed and 10 skipped in 749.15s, the canary EXIT 0 at 42 passed, `python3 -m ruff check` over the 27 changed files in one invocation EXIT 0 at `All checks passed!`, and `integrity check --json` EXIT 0 with `"passed": true` and `"fail_count": 0`. TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r6-block.md` survived the session boundary, and it, the committed `.agent/authored/f272-r6.md` and the committed `.agent/last_block.md` are all 26278 bytes and all hash to `5d1e0e2a62e049e9cf87f613f3be9b20f92c39a7b09d428c2fb59efc6b903c13`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. THE RECORD at C2 and THE PLAN at C1 both reproduce byte for byte: `.agent/live_review.md` 1081516 to 1088550 and `.agent/prose_slips.md` 134136 to 134816, both with the pre-image a byte-exact prefix and `post == pre + NL + slice` TRUE, registrations 302 unchanged, resolutions 247 unchanged, open set 55 unchanged, `^Gate: ` 27 to 28 and `^Gate: F272 R5 ` 0 to 1; the plan is 2126 bytes byte-equal to its slice at 42 lines against the cap of 50. THE WORKER'S DEVIATION 2 IS UPHELD IN FULL AND IS THE ROUND'S MOST VALUABLE OUTPUT. It declined to meet gate G4(iii) as literally worded, measured why, and reported both readings instead of producing a number; the reviewer reproduced that measurement independently and registers the defect as R-0819 below. Deviation 1 — the block's "29 paths" standing over its own enumeration of 33 — and deviation 3 — clause (c) of C6 being vacuous because all ten AST sites in `tests/test_data_paths.py` sat inside the test the round deletes whole — are reviewer-prose inaccuracies that left nothing wrong on disk, so per operator amendment amend0827-process-diet rule 2 they are dated lines in `.agent/prose_slips.md` and spend no id. Deviations 4, 5 and 6 are accepted as declared: ruff's `I001` forcing two import lines to combine is a consequence of the ordered G7 gate rather than a choice, the worker's "34 shadowed" is a count of CALL sites and its 63 is the count of occurrences in shadowed scopes so the two figures are not a disagreement, and C0a and C0b preceding C1 is the block's own ordered sequence.

- R-0819 — Medium, A GATE OVER PRODUCTION CODE DEMANDED ZERO OF A CONDITION THAT IS ALREADY NON-ZERO AT ITS OWN BASE AND THAT THE ROUND'S CORRECT FIX MAKES MORE COMMON. The defect is the reviewer's, in the F272 round 6 block's gate G4(iii), and the WORKER found it, measured it and declared it as deviation 2 rather than meeting it. G4(iii) ordered "zero function scopes that BOTH bind a local named `run_dir` or `runs_dir` AND contain a call whose callee is a bare `Name` of that same identifier", over every tracked `.py` file, and required the count to be 0. A function-local `from packages.orchestration.data_paths import run_dir` followed by `run_dir(...)` satisfies that wording exactly — the import binds the name in that scope and the call is a bare `Name` of it — and that is this repository's correct and pervasive idiom, the very shape DECISION F272 D3 rules as Shape A. MEASURED INDEPENDENTLY BY THE REVIEWER, by `ast` over every tracked `.py` file enumerated from `git ls-files`, 1063 files at each commit, counting each call site whose callee is a bare `Name` of `run_dir` or `runs_dir` inside a function scope that binds that identifier: 16 at `61c4bd2e` and 31 at `df955058`. ELEVEN of those are production sites and are identical at both commits — `apps/cli/commands/do_cmd.py::_load_prompt_trace_index`, `packages/orchestration/job_evidence.py` at `export_job_evidence`, `_linked_job_summary`, `_read_run_json`, `_write_task_run_evidence` and `_write_job_prompt_trace_summary`, `packages/orchestration/pingpong_evidence.py::export_evidence`, `packages/orchestration/pingpong_promote.py::load_promotion`, `packages/orchestration/repair_attest.py::_prior_provider_call_count`, and `packages/orchestration/worktree_resume.py` at `_run_dir` and `find_recoverable_runs`. The worker's own reading of the same wording gives 21 and 36; the two definitions differ by a constant and agree on the load-bearing fact, which is that the count is NON-ZERO AT THE BASE and RISES across the round precisely because the round moved its shape-A callers onto the new spelling correctly. THE GATE IS THEREFORE UNMEETABLE, which is the class operator amendment amend0827-process-diet rule 2 spends an id on — a gate over production code demonstrably unmeetable — and it is worse than a vacuous gate rather than better: the only edit that could have driven it to 0 is one that hoists or aliases correct function-local imports across those eleven production functions, which AGENTS.md's Scope Control section forbids as its own activity and whose alias form its Code Discoverability section forbids by name. A worker obeying this gate literally would have been driven into a wrong change to production code, and only the worker's decision to measure instead of comply prevented it. THE PROPERTY THE GATE MEANT is the one DECISION F272 D3 describes and round 5's three `pingpong_loop.run_pingpong` sites exhibited: a bare-`Name` call that EXECUTES BEFORE its scope's first binding of that name, which is the `UnboundLocalError` the whole two-shape rule exists to prevent. Measured by the reviewer under that reading over the same 1063 files at each commit: 0 at `61c4bd2e` and 0 at `df955058`. FIX, BINDING ON THE NEXT BLOCK OF THIS FEATURE THAT GATES THE SHADOW PROPERTY — T003 and T004 both move further callers, so this is owed rather than historical. State the gate as "zero call sites whose callee is a bare `Name` of `run_dir` or `runs_dir` and whose line number is strictly less than the first binding of that name in the enclosing function scope", measure it by `ast` over every tracked `.py` file enumerated from `git ls-files`, and RUN IT AT THE BASE BEFORE ORDERING IT. That last clause is the counter-measure that reaches the cause rather than the instance: §3 item 12 and finding R-0364 already require a gate to be executed at its base before it is ordered, and this block did not do it for G4(iii). A gate that cannot pass and a gate that cannot fail are the same defect wearing two faces.
<<<END RECORDR7>>>

<<<BEGIN SLIPSR7>>>
2026-09-06 · F272 R6 block (reviewer) · The change-set paragraph closed with "That is 29 paths and no others" while its own enumeration listed 33 — 17 + 1 + 7 + 1 + 1 code paths plus the six `.agent/` files. The worker applied the ENUMERATION, which is the change set, and touched exactly those 33 paths, so nothing wrong reached disk. This is the §3 item 16 class: a sentence quantifying a list it names, where the numeral is the half nobody re-reads. Prefer naming the list to counting it.

2026-09-06 · F272 R6 block (reviewer) · Clause (c) of the C6 instructions anticipated that "the remaining sites in that file take SHAPE A or B by the scope test like any other", and there were none: all ten AST sites in `tests/test_data_paths.py` sat inside the alias test clause (a) deletes whole, and the file's other three occurrences are the two failure-message strings clause (b) retargets. The clause was vacuous rather than wrong. Reading the target file's sites against the clauses already ordered over it would have shown the residue was empty before the block was emitted.
<<<END SLIPSR7>>>

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
`SESSION 3 of feature F272 · round 7`, the one-sentence context self-assessment
amend0905-throughput requires, branch, the range, a per-commit changed-files
table with real `+/-` from `git diff --numstat`, the item-status table covering
C0a through C6 with every item present exactly once, one line per gate G1 to G8
with its real exit code, the eight per-field readings G4(ii) asks for, the eight
mutation exit codes G5 asks for, the authored-text proof table, deviations and
assumptions, and the next expected action. There is no length cap.
