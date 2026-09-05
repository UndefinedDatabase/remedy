── STEP T001 (part 1 of 2) — F260 ────────────────────────────
Goal:        Claim F260 on a new branch, book the F259 R10 verdict into the
             record, and put the MEASURED inventory of Remedy's job/run storage
             on disk — including the collision that makes this feature file's
             "renamed to runs/" sentence unbuildable as written.
Bundle:      C0a save this block · C0b mirror it · C1 plan + context · C2 the
             record (re-head + the R10 gate entry) · C3 the STATUS claim ·
             C4 the inventory · C5 the feature-file amendment · C6 the handback
(the rule line below is 62 copies of U+2500, per §3 item 37)
──────────────────────────────────────────────────────────────

## Before anything: the branch

The Open PR Gate has already run in the reviewer's session. Pull request 240 was
merged with `gh pr merge 240 --merge --delete-branch` at merge commit
`b5cd6c20`, `main` was pulled, and `gh pr list --state open` returns an empty
list. Do NOT re-run the gate and do NOT merge anything this round.

Start on `main` at `b5cd6c20` with a clean tree, then:

    git checkout -b feature/f260-one-world

Every commit of this round lands on that branch. Never work on `main` (G3).

## Change set — nothing outside this list

    .agent/authored/f260-r1.md          (new, C0a)
    .agent/last_block.md                (C0b)
    .agent/plan.md                      (C1)
    .agent/context.md                   (C1)
    .agent/live_review.md               (C2)
    docs/roadmap/STATUS.md              (C3)
    .agent/f260_inventory.md            (new, C4)
    docs/roadmap/features/T2_F260.md    (C5)
    .agent/handoff.md                   (C6)

Scratch you may create freely under the gitignored `.remedy-wt/`; it must stay
untracked, and `git ls-files .remedy-wt` must return nothing at the end.

## C0a — save this block

This block is on disk at `.remedy-wt/f260-r1-block.md`. The prompt that
delegated this round states that file's sha256; call it BLOCK_SHA. A file
cannot carry its own digest, so BLOCK_SHA is named there and never here.

COPY that file to `.agent/authored/f260-r1.md` (`shutil.copyfile`, never a
retype, never a text round-trip) and commit it alone.

## C0b — mirror

Copy the same bytes to `.agent/last_block.md` and commit it alone. This is one
indivisible `.agent/**` state rewrite (AGENTS.md DECISION F104 D1 exemption), so
its insertion count is not split.

## C1 — plan and context

Write `.agent/plan.md` from the PLANF260R1 slice and `.agent/context.md` from
the CONTEXTF260 slice, each byte-for-byte plus exactly one trailing newline, and
commit the two together. This is the round's FIRST substantive commit because
the round touches the finding ledger (planner_reviewer_prompt.md §3 item 23).

## C2 — the record

Two edits to `.agent/live_review.md`, one commit.

FIRST, the re-head. The file contains the separator `"\n## Steps\n"` exactly
once (measured by the reviewer at `b5cd6c20`: 1 occurrence). Partition on it and
replace only the head:

    text = path.read_text(encoding="utf-8")
    assert text.count("\n## Steps\n") == 1
    head, sep, tail = text.partition("\n## Steps\n")
    new = REHEADTO + sep + tail

where REHEADTO is the slice below WITHOUT a trailing newline (the separator
supplies it). At `b5cd6c20` the head is 1299 bytes over 18 lines and the tail is
854531 bytes; the tail carries 298 `^- R-\d{4} — ` registrations against 4
`^Done: R-\d{4} — ` lines, and NOT ONE BYTE of it may change.

SECOND, the append. To the result of the re-head, append exactly
`"\n" + GATE_R10 + "\n"`, where GATE_R10 is the slice below with no trailing
newline. The file ends with exactly one newline before and after.

## C3 — the STATUS claim

One replacement in `docs/roadmap/STATUS.md`, applied with
`str.replace(FROM, TO, 1)` after asserting the FROM occurs exactly once.
Measured by the reviewer at `b5cd6c20`: FROM occurs 1x, TO occurs 0x, and
`TO contains FROM: false` — so this is a REWRITE and the FROM-zero count is
attainable.

    <<<BEGIN STATUSPAIR_FROM>>>
- [ ] F260 — One world: mission → job → run
    <<<END STATUSPAIR_FROM>>>

    <<<BEGIN STATUSPAIR_TO>>>
- [~] F260 — One world: mission → job → run
    <<<END STATUSPAIR_TO>>>

Strip exactly one trailing newline from each extracted slice before replacing;
the markers sit on their own lines, so a raw extraction carries the newline that
precedes the END marker and the FROM would then match zero times.

## C4 — the inventory (the round's real work)

Write `.agent/f260_inventory.md`. This file is a MEASUREMENT, not prose: every
claim in it is produced by a command you run, and every path and symbol it names
is one you resolved on disk at `b5cd6c20`. Cite `file:line` for each. It must
answer, at minimum:

1. **Every on-disk area that stores a job, a run, or a run's evidence**, with
   its path template, what KEY the directory or file is named by (job id or run
   id), the writer module and function, and the reader modules. The reviewer
   measured four such areas at `b5cd6c20` and expects your independent reading
   to confirm or correct each; report what YOU measure, and where you disagree
   with this list say so explicitly rather than reproducing it:
   - `<data_root>/jobs/<uuid>.json` — `storage.save_job` (storage.py:75),
     `packages.core.models.Job`.
   - `<data_root>/task_jobs/<16hex>/job.json` — `pingpong_job._persist_job`
     (pingpong_job.py:381), `JobPlan`; the directory is keyed by JOB id.
   - `<data_root>/runs/<job_id>/*.jsonl` — `run_log.RunLogWriter`
     (run_log.py:114 via `data_paths.runs_dir`), read by
     `timeline.load_run_events` (timeline.py:75). Keyed by JOB id.
   - `<data_root>/pingpong_runs/<run_id>/` — `pingpong_loop._persist_run`
     (pingpong_loop.py:4234) via `_pingpong_runs_dir` (pingpong_loop.py:4228).
     Keyed by RUN id.
2. **The field-by-field shape of both job records** — `packages.core.models.Job`
   against `pingpong_job.JobPlan` — as a table: field name, type, which record
   has it, and whether the two spellings mean the same thing. This is the
   evidence DECISION F260 D1 will be ruled from; do not rule it here.
3. **Every id shape actually minted**, with the minting call site, and every
   parse or validation path that constrains it — including
   `data_paths._SHORT_HEX_RE` (data_paths.py:150) and the `UUID(raw)` branch of
   `resolve_job_id` (data_paths.py:205). This is the evidence for D2; do not
   rule it here either.
4. **Every consumer named under "Design" in `docs/roadmap/features/T2_F260.md`**,
   re-grepped at `b5cd6c20`, as a table of path, the symbol it actually calls,
   and the line where it calls it — with a column saying whether the feature
   file's cited line number still resolves. The feature file's citations were
   taken on 2026-09-05 and this branch has moved nothing yet, so a mismatch is a
   defect of the feature file and must be reported, not silently corrected.
5. **The `runs/` collision, stated as a measurement.** The feature file says the
   `task_jobs/` directory "is renamed to `runs/`". `data_paths.runs_dir`
   (data_paths.py:78) already returns `<data_root>/runs` and the run log already
   writes `<data_root>/runs/<job_id>/`. Report both readings and say plainly
   whether the ordered rename lands on an occupied path.

Do NOT rule D1, D2 or D3, do not rename anything, do not delete anything, and do
not change a single line under `packages/` or `apps/` this round. This round
measures; the next round rules.

## C5 — the feature-file amendment

Append the AMENDF260D0 slice to `docs/roadmap/features/T2_F260.md`, immediately
after the line `### DECISION F260 D2 — the one id shape (to be recorded in T001)`
paragraph and before the `### DECISION F260 D3` heading — that is, the new
heading becomes the last DECISION before D3. Apply it as an insertion and prove
it by whole-file reconstruction: the post-edit file equals the pre-edit file with
exactly the slice inserted at that point, and nothing else moves.

## C6 — the handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has no
length cap (AGENTS.md, amend0827 rule 3). It carries the mandated sections, the
changed-files table with the `+/-` column taken from `git diff --numstat` (NOT
from before/after line counts — planner_reviewer_prompt.md §3 item 28), one line
per gate below with its real exit code and real output, the item-status table,
and the Session line:

    SESSION 1 of feature F260 · round 1 · rounds so far 1

plus one sentence of context self-assessment (self_drive_protocol.md G7).
The state block repeats this line verbatim:

    ~5 % (T001 Inventar ✅ · D1/D2 offen · T002–T005 offen) — Schätzung

C6 is the LAST commit of the round. Push after it:

    git push -u origin feature/f260-one-world

Do NOT create a pull request and do NOT merge anything this round.

## Constraints

1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it as
   written and declare the problem in the handback — never silently repair it.
2. Nothing outside the change set above is created, edited or deleted.
3. No file under `packages/`, `apps/` or `tests/` changes this round.
4. Commit in the order C0a, C0b, C1, C2, C3, C4, C5, C6. No extra commit, no
   dropped commit, no reordering.
5. Every commit is single-parent and stays under the AGENTS.md 500-INSERTION cap
   (insertions only, the `+` column — DECISION F104 D1).
6. Destructive verification, if you do any, runs only inside a disposable
   `git worktree`; the primary checkout satisfies `git status --porcelain` empty
   at the end of the round (G5).
7. `.agent/plan.md` stays under 50 lines (AGENTS.md).
8. Commit subjects carry no leading-slash token, no absolute path and no
   secret-like string (AGENTS.md Commit Discipline).

## Done when — the gates

Run every one and report its real exit code and real output. "Green" as a word
is a finding (G4).

- **G1 TRANSPORT.** `sha256sum .remedy-wt/f260-r1-block.md
  .agent/authored/f260-r1.md .agent/last_block.md` prints ONE digest three
  times, equal to the BLOCK_SHA the delegating prompt states. This is a COPY
  chain over the scratch
  original, the saved copy and the mirror; per §3 item 37 it is not a claim
  about bytes emitted into a prompt.
- **G2 THE RECORD.** Take the pre-edit bytes of `.agent/live_review.md` at
  `b5cd6c20` into scratch first. Then, after C2, prove all of:
  (a) the post-edit file equals `REHEADTO + "\n## Steps\n" + tail + "\n" +
  GATE_R10 + "\n"` where `tail` is the partition tail of the PRE-edit bytes —
  one boolean, byte-exact reconstruction;
  (b) an independent structural reader: split both pre- and post-edit files on
  blank lines, report N = (post units − pre units) as a number your script
  COUNTS, and compare the LAST N units of the post-edit file against GATE_R10's
  paragraphs in order;
  (c) a negative control on reading (b): flip one byte inside the FIRST appended
  paragraph and confirm reading (b) REJECTS it, in scratch, never on the tracked
  file;
  (d) the region from `## Findings` to end of file has an identical sha256
  before and after the whole commit;
  (e) `grep -c '^Gate: R10 — '` goes 0 → 1, and no two `^Gate: R` headers in the
  file are byte-identical.
- **G3 THE STATUS PAIR.** FROM occurs 1x before and 0x after; TO occurs 0x
  before and 1x after; whole-file reconstruction from the pre-edit bytes with
  only this replacement applied is byte-equal to the committed file; the file
  still ends with exactly one newline. Then `^- \[~\] F` = 1 and its id is F260,
  and `^- \[x\] F` = 73 (unchanged by this round).
- **G4 THE INVENTORY IS MEASURED.** For EVERY `path:line` citation in
  `.agent/f260_inventory.md`, run a script that opens that file at that line and
  prints the line, and assert the cited symbol occurs in it. Report the total
  number of citations checked and the number that resolved; a citation that does
  not resolve is a red gate, not a footnote. Also confirm each of the four store
  paths is named in the file, and that item 5 of C4 states explicitly whether
  the rename lands on an occupied path.
- **G5 THE STATE CONTRACTS.** `.agent/plan.md` holds `## Goal`, `## Next Steps`
  and a `\bF\d{3}\b` match, and is under 50 lines. `.agent/context.md` holds
  `Steps`, `## Active Branch`, `feature/`, a `\bF\d{3}\b` match, and `resource`
  or `pytest` case-insensitively, and holds none of `steps-74_1-79`,
  `Steps 91-100`, `allow repo_test_run`, `synthetic_count: 4`,
  `job=None source_apply bypass`. `.agent/live_review.md` holds `Steps`.
- **G6 THE SUITES, RUN SERIALLY, one at a time, in the primary checkout.**
  Report exit code and the passed count for each:

      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/orchestration/test_roadmap_index.py -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q

  The reviewer measured these at `b5cd6c20` before this block was emitted:
  303, 30, 515, 52, 21, 16 and 42 passed, every one exit 0. A DIFFERENT number
  is not automatically a failure — report the number you get and, if it differs,
  name the node ids that account for the difference.
- **G7 STRUCTURE AND PUSH.** Every commit single-parent
  (`git log --format='%h %p' b5cd6c20..HEAD` — one parent each) and every
  insertion count under 500, reported per commit for C0a through C5. C6's own
  numbers cannot exist while C6 is being written, and self-drive has no round
  report to route them to, so do NOT state them anywhere: the reviewer measures
  them at the next gate and records them in that round's ledger entry
  (§3 item 31). `git status --porcelain` empty. `git ls-files .remedy-wt` empty. The push
  result reported. `python3 -m apps.cli.grouped integrity check --json` prints
  `"passed": true` with `"fail_count": 0`.

## Handback

Completion report plus the rewrite of `.agent/handoff.md` described at C6.
Declare every deviation. If a gate goes red, STOP at that gate, do not route
around it, and report the exact output — a red gate ends the round honestly and
is worth more than a green one that was reached by widening scope.

────────────────────────── authored slices ──────────────────────────

<<<BEGIN PLANF260R1>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). F259 is accepted and its page
`docs/system/vocabulary.md` is binding for every name this feature introduces.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function; a Run becomes the evidence case a Job
points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 the records and writers, T003 the consumers, T004 the classic
runner, T005 the reachability test and the cluster deletion.

## Current Step

Round 1 claims F260, books the F259 R10 verdict into the review record, and
writes `.agent/f260_inventory.md` — the measured reading of every job, run and
evidence area on disk, both job record shapes, every id shape minted, and the
re-grepped consumer list. It rules nothing: DECISION F260 D1 and D2 are ruled in
round 2 from this measurement.

## Next Steps

- Rule DECISION F260 D1 (where the classic job fields live) and D2 (the one id
  shape) from the inventory, and settle where a Run's evidence lives now that
  `<data_root>/runs/` is measured as already occupied by the run log.
- Write the one minting and resolving function, and move every job-taking
  command onto it while both stores still exist (T001, part 2).
- T002: the extended Mission record, the unified Job record, the run directory.

## Risks

- The feature file orders `task_jobs/` "renamed to `runs/`" onto a path the run
  log already writes. Round 1 records the collision; round 2 must rule it before
  any directory moves, or the rename silently merges two keyspaces — one keyed
  by job id, one by run id.
- The prototype cluster deletion (T005) is large and irreversible in one
  direction only. It runs last, behind a reachability test that is green BEFORE
  the first `git rm`.
<<<END PLANF260R1>>>

<<<BEGIN CONTEXTF260>>>
# Context — F260 One world: mission → job → run

## Active Branch
feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of pull
request 240.

## Scope
F260 (Tier 2, depends on F259's binding vocabulary page; blocks F261, F266,
F268, F269, F270, F271 and F263): make DECISION amend0905-vocab D2 real on disk
— one Mission record, one Job record, one Run evidence case, one id shape minted
by one function. Task slicing per T2_F260.md: T001 inventory and id shape, T002
the records and their writers, T003 the consumer list, T004 the classic runner's
deletion, T005 the reachability test and the prototype cluster deletion.

## Do not touch
The scope-fence builtin deny list (F017), the approval gate, STATUS semantics.
No command is RENAMED here — F261 owns renames; this feature changes what a job
IS, not what it is called. No module outside the T2_F260.md lists is deleted,
and a module that turns out to be reachable is reported, never deleted.

## Assumptions
- Cleanliness before compatibility (DECISION D-A): no migration shim, no
  compatibility reader, no alias. Old `.data` content is deleted by the
  developer, not converted.
- The inventory on disk as `.agent/f260_inventory.md` is the evidence D1 and D2
  are ruled from; no later round reconstructs those readings from memory.
- `<data_root>/runs/` is ALREADY the run-log area keyed by job id, so the
  feature file's "renamed to runs/" needs a ruling before any directory moves.
- Deletion is proved before it is performed: the T005 reachability test is green
  with the doomed modules absent from the reachable set BEFORE the first
  `git rm`.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in
  the primary checkout, which satisfies `git status --porcelain` empty at every
  verdict.
- `ruff check` is DENIED to this session's reviewer. A round of F260 that ships
  a `.py` file gates `python3 -m py_compile <path>` instead, and the worker
  attempts `ruff check` itself, reporting success or the exact refusal.
- `remedy` (the built CLI) is DENIED to this session's reviewer session-wide,
  subagents included; a round needing it delegates the run to the worker and
  reports the exact output.
- This session's shell guard refuses some command FORMS outright — shell loops,
  `$(...)` substitution, a `$` inside a `sed` range — so checks of that shape
  are re-expressed in Python and the re-expression is reported.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status Table"
section requires of every completion report. This file deliberately does not
restate it.
<<<END CONTEXTF260>>>

<<<BEGIN REHEADTO>>>
# Live Review — F260 One world: mission → job → run

> Round-by-round review record, re-headed at the F260 claim per
> docs/agents/planner_reviewer_prompt.md §1. The heading this replaces named
> F259, which is accepted: its STATUS line went `[x]` at `1e7ecf90` and its pull
> request 240 merged at `b5cd6c20`. Only the heading and this paragraph are
> rewritten. Every finding record below `## Findings` is carried forward
> BYTE-IDENTICAL — the block that ordered this re-head gates that region's
> sha256 equal before and after the edit, as its gate G2(d) — and finding ids
> continue the monotonic R-XXXX series across the re-head. Measured by the
> reviewer at `b5cd6c20`, the branch point: 298 lines matching `^- R-\d{4} — `
> against 4 matching `^Done: R-\d{4} — `, so 294 findings are open, and the
> maximum id in use is R-0813 — the next id this feature mints is R-0814.
> Records belonging to features already marked `[x]` in docs/roadmap/STATUS.md
> are not here at all: `scripts/rotate_live_review.py` moves them byte-verbatim
> into the append-only `.agent/live_review_archive.md` in every closure
> sequence, under operator amendment amend0905-throughput, and that archive is
> read on demand by id, never at session start.
<<<END REHEADTO>>>

<<<BEGIN GATE_R10>>>
Gate: R10 — the F259 R10 entry, CLOSURE PART 3, and the terminator of that branch. VERDICT PASS. Range aba15f08..1e7ecf90, five commits, all single-parent, insertions 300, 251, 19, 2 and 253 — every one far under the AGENTS.md 500-insertion cap, and the last of them is the closure commit whose 253 are the handback plus the three content paths at 9, 1 and 1. This entry is written by the FIRST round of F260 rather than by F259 itself, because the round that writes a record cannot record the gate on itself (planner_reviewer_prompt.md §4 item 13) and self-drive has no second window to carry it (§3 item 31); operator amendment amend0827-process-diet rule 1 routes it to the first commit of the next round that was happening anyway, which is this one. THE REVIEWER RE-RAN EVERY GATE ITSELF and reproduced every number the handback stated. TRANSPORT: one digest `3c9ece83b1b4f46af15c9bc280d9f24ec8e0e61604793d03eb8958b5e9853ae5` across `.agent/authored/f259-r10.md` and `.agent/last_block.md`, equal to the digest the round's own order stated; per §3 item 37 that covers the saved copy and its mirror and is not a claim about bytes emitted into a prompt. THE RECORD APPEND at `df26cab3`: pre 851727 bytes, post 855840, delta 4113, and the pre-image is a byte-exact PREFIX of the post-image with the remainder equal to `"\n" + GATE_R9 + "\n"` for a 4111-byte slice — all four readings true. The independent structural reader agrees: 416 blank-line units before and 417 after, N = 1, every unit preceding the append byte-identical, the appended header `Gate: R9 — the F259 R9 entry, CLOSURE PART 2`, and no two `Gate: R` headers in the file byte-identical, so the item-26 duplicate-header class did not recur. The landed slice carries zero unquoted matches of the token this record forbids outside backticks (R-0586). THE FIVE PAIRS at `1e7ecf90` reconstruct: `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` each rebuild byte-exactly from their pre-edit bytes with only their own replacements applied, and each still ends with exactly one newline. THE LEDGER AND THE README AGREE: `^- \[x\] F` = 73, `^- \[~\] F` = 0, the README numeral reads 73 of 271, the Tier 2 row reads Done 16 of 24, and the per-tier accepted counts derived from the STATUS headings are Tier 0 16, Tier 1 22, Tier 2 16, Tier 3 6 and Tier 5 13, summing to 73. THE R-0797 TOKEN SWEEP, the point of that round, reproduces exactly and is reported as tokens rather than as a count: the narrow form over the `Accepted in Tier N so far:` blocks finds 4 blocks, 33 occurrences and 32 distinct ids — F008 F009 F013 F014 F016 F021 F022 F031 F032 F034 F037 F046 F047 F048 F050 F051 F052 F053 F086 F103 F104 F105 F106 F107 F251 F252 F254 F255 F256 F257 F259 F262 — and the wide form over the pinning test's own `Accepted[^\n]*:` regex finds 5 blocks, 49 occurrences and 48 distinct, adding F001 F002 F003 F004 F005 F006 F007 F010 F011 F012 F017 F018 F081 F146 F147 F148. In BOTH forms every id is `[x]` in docs/roadmap/STATUS.md and none is absent from it; the count of ids not `[x]` is zero either way, which is what discharges R-0797. THE SELF-USE ITEM is consumed: SU-010 `consumed_by` = `F259`, entries with an empty `consumed_by` = 0, total entries 10, and the `—` escape count is 53 before and 53 after, which is the evidence the file was edited as TEXT and never round-tripped through `json.dump` — the standing shape of open finding R-0785. THE EIGHT SUITES were re-run by the reviewer serially and all eight matched their expected counts at exit 0: tests/docs/ 303, test_roadmap_index.py 30, test_self_use_generator.py 20, tests/ui_server/ 515, test_test_runner.py 52, test_resource_safety.py 21, test_integrity_gate.py 16 and tests/cli/test_golden_path.py 42. THE CLOSURE PRECONDITIONS hold: `integrity check --json` returns `"passed": true` with `"fail_count": 0` over 5 checks at handlers=342, the open-finding count is 294 (298 registrations minus 4 `Done:` lines) unchanged across the round, `.agent/candidates.md` is untouched by the range and remains EMPTY, and the working tree is clean with no tracked file under `.remedy-wt`. THE THREE VALUES THE HANDBACK COULD NOT CARRY, because the commit that writes it is the last on the branch (the R-0449 shape that round declared rather than faked), are recorded here as §3 item 31 requires: the push succeeded, the pull request was number 240, and it was NOT merged by that session — it was merged by THIS session's Open PR Gate with `gh pr merge 240 --merge --delete-branch` at merge commit `b5cd6c20`, after its CI run 33997545989 completed with conclusion success, leaving `gh pr list --state open` empty. Two declared deviations were checked and both are sound: stripping one trailing newline from each pair slice before `str.replace` is newline-neutral and was forced by the block's own marker convention, and running `tests/docs/`, G4 and G5 both before and after the closure commit on byte-identical content is the only way to satisfy a go/no-go gate on a commit nothing may follow. Nothing in that round is owed a repair round, and no closure candidate was raised.
<<<END GATE_R10>>>

<<<BEGIN AMENDF260D0>>>
### DECISION F260 D0 (2026-09-06, F260 round 1) — the run directory the feature file names is already taken

RECORDED BEFORE D1 AND D2 BECAUSE BOTH DEPEND ON IT. The "Goal & Done" section
above says a Run "is the evidence-case folder that today is
`<data_root>/task_jobs/<16hex>/`" and that "the directory is renamed to
`runs/`". Measured at `b5cd6c20`, before any line of this feature was written,
that sentence is wrong twice over and the rename it orders lands on an occupied
path:

- `<data_root>/task_jobs/<16hex>/` is keyed by JOB id and holds `job.json`,
  written by `pingpong_job._persist_job`. It is a JOB record, not a run's
  evidence case.
- `<data_root>/runs/` already exists and is already written: `data_paths.runs_dir`
  returns it and `run_log.RunLogWriter` files run logs at
  `<data_root>/runs/<job_id>/*.jsonl`, which `timeline.load_run_events` reads.
  It too is keyed by JOB id.
- The folder actually keyed by RUN id is `<data_root>/pingpong_runs/<run_id>/`,
  written by `pingpong_loop._persist_run`.

So a plain rename of `task_jobs/` to `runs/` would merge two directories keyed
by the same job id but holding different things, and would still leave the one
directory keyed by run id outside the model — while the vocabulary page F259
made binding gives a Job MANY runs, which no job-keyed directory can express.

CHOSEN: this feature does not perform that rename as written. Round 1 records
the four measured areas in `.agent/f260_inventory.md`; DECISION F260 D1 is
widened to rule the RUN directory as well as the job fields, and must state, for
each of the four areas, whether it survives, moves or is deleted, and what the
surviving directory is keyed by. Nothing moves on disk until D1 is recorded.

ALTERNATIVES CONSIDERED. Renaming `task_jobs/` to `runs/` as written and letting
the run log share the directory — rejected: it merges a job-keyed and a
job-keyed store whose contents answer to different concepts, and leaves
`pingpong_runs/` stranded. Keeping `task_jobs/` under its present name —
rejected: the whole point of the feature is that the name lies about what the
directory holds.

REVERSE by deleting this paragraph and restoring the "Goal & Done" sentence as
the binding order, at which point the rename becomes a required slice and the
collision above becomes a defect to be repaired inside it.
<<<END AMENDF260D0>>>
