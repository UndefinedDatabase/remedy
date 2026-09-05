── STEP T001 (part 1 of 2, resumed) — F260 ───────────────────
Goal:        Repair the one byte round 1's block cost the record, book round 1's
             verdict and my two authoring slips, then finish the three commits
             round 1 could not reach: the STATUS claim, the measured inventory,
             and the feature-file amendment.
Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the record
             (blank-line repair + the R1 gate entry) · C3 prose slips ·
             C4 the STATUS claim · C5 the inventory · C6 the amendment ·
             C7 the handback
(the rule line below is 62 copies of U+2500, per §3 item 37)
──────────────────────────────────────────────────────────────

## Where this round starts

You are continuing on `feature/f260-one-world` at `4b704705`, which is already
pushed. Do NOT create a branch, do NOT merge, do NOT create a pull request.
Round 1 stopped at a red gate and was RIGHT to stop: both causes were defects in
MY block, not in your work. Your four commits `3085576d`, `dcabd38e`,
`026cfe41` and `a0b43fb6` are byte-correct and are KEPT. Nothing is reverted.

Two things I got wrong, both now measured and both repaired by this round:

1. Gate G2(d) demanded the region from `## Findings` to end of file be
   sha256-identical across a commit that appends a gate record INTO that region.
   Measured at `4b704705`: 0 `Gate:` records sit above that heading and 10 below
   it, so no round that books a verdict can ever satisfy it. It is replaced
   below by the reading it was reaching for.
2. The REHEADTO slice ended without the blank line that separated the header
   from `## Steps`, so applying it byte-for-byte — which is what you were
   required to do — merged two blank-line units and made N = 0. C2 restores that
   single byte.

## Change set — nothing outside this list

    .agent/authored/f260-r2.md          (new, C0a)
    .agent/last_block.md                (C0b)
    .agent/plan.md                      (C1)
    .agent/live_review.md               (C2)
    .agent/prose_slips.md               (C3)
    docs/roadmap/STATUS.md              (C4)
    .agent/f260_inventory.md            (new, C5)
    docs/roadmap/features/T2_F260.md    (C6)
    .agent/handoff.md                   (C7)

`.remedy-wt/` scratch stays untracked; `git ls-files .remedy-wt` returns nothing.

## C0a — save this block

The block is on disk at `.remedy-wt/f260-r2-block.md`. The prompt that delegated
this round states its sha256; call that BLOCK_SHA. A file cannot carry its own
digest, so it is named there and never here. COPY the file to
`.agent/authored/f260-r2.md` with `shutil.copyfile` — never a retype, never a
text round-trip — and commit it alone.

## C0b — mirror

Copy the same bytes to `.agent/last_block.md`, commit alone. One indivisible
`.agent/**` state rewrite (AGENTS.md DECISION F104 D1 exemption).

## C1 — the plan

Write `.agent/plan.md` from the PLANF260R2 slice, byte-for-byte plus exactly one
trailing newline. FIRST substantive commit, because this round touches the
finding ledger (planner_reviewer_prompt.md §3 item 23).

## C2 — the record: repair, then append

Both edits to `.agent/live_review.md`, one commit, in this order.

FIRST the repair. Measured at `4b704705`: `"\n## Steps\n"` occurs exactly once
and the head before it ends `by id, never at session start.` with no blank line
after it. Restore that one byte:

    text = path.read_text(encoding="utf-8")
    assert text.count("\n## Steps\n") == 1
    head, sep, tail = text.partition("\n## Steps\n")
    repaired = head + "\n" + sep + tail

This adds exactly one byte (860937 → 860938 at `4b704705`) and exactly one
blank-line unit (417 → 418). Legitimate because the header region is what round
1 itself rewrote; nothing below `## Findings` is touched, and no landed finding
or gate text is altered — planner_reviewer_prompt.md §3 item 20 forbids
rewriting landed record text and this edit does not do that.

SECOND the append. To the repaired text append exactly `"\n" + GATE_R1 + "\n"`,
where GATE_R1 is the slice below with no trailing newline.

## C3 — the prose slips

Append to `.agent/prose_slips.md` exactly `"\n\n" + SLIP1 + "\n\n" + SLIP2`.
Measured at `4b704705`: the file is 85098 bytes, holds 112 dated lines and ends
WITHOUT a trailing newline; it must still end without one. This file is
append-only: nothing already in it is rewritten or renumbered.

These are recorded as slips and NOT as R-ids because operator amendment
amend0827-process-diet rule 2 reserves an id for a defect with product effect —
wrong state under `packages/`, `apps/`, `tests/` or `docs/`, or a gate over
PRODUCTION CODE shown blind or unmeetable. Both of mine were gates over an
`.agent/` prose file and left nothing wrong outside `.agent/`.

## C4 — the STATUS claim

Measured at `4b704705`: FROM occurs 1x, TO occurs 0x, `TO contains FROM: false`
⇒ REWRITE, so the FROM-zero count after is attainable. Apply with
`str.replace(FROM, TO, 1)` after asserting FROM occurs exactly once.

    <<<BEGIN STATUSPAIR_FROM>>>
- [ ] F260 — One world: mission → job → run
    <<<END STATUSPAIR_FROM>>>

    <<<BEGIN STATUSPAIR_TO>>>
- [~] F260 — One world: mission → job → run
    <<<END STATUSPAIR_TO>>>

Strip exactly one trailing newline from each extracted slice before replacing.
The STATUSPAIR markers are indented four spaces and the other markers are not;
extract by marker line regardless of indentation, as you did in round 1.

## C5 — the inventory (the round's real work)

Write `.agent/f260_inventory.md`. It is a MEASUREMENT, not prose: every claim is
produced by a command you run, and every path and symbol it names is one you
resolved on disk at `4b704705`, cited as `file:line`. It must answer:

1. **Every on-disk area storing a job, a run, or a run's evidence** — path
   template, what KEY it is named by (job id or run id), writer module and
   function, reader modules. I measured four at `b5cd6c20`; confirm or CORRECT
   each from your own reading, and say where you disagree rather than copying:
   - `<data_root>/jobs/<uuid>.json` — `storage.save_job` (storage.py:75),
     record `packages.core.models.Job`.
   - `<data_root>/task_jobs/<16hex>/job.json` — `pingpong_job._persist_job`
     (pingpong_job.py:381), record `JobPlan`; keyed by JOB id.
   - `<data_root>/runs/<job_id>/*.jsonl` — `run_log.RunLogWriter`
     (run_log.py:114, via `data_paths.runs_dir` at data_paths.py:78), read by
     `timeline.load_run_events` (timeline.py:75). Keyed by JOB id.
   - `<data_root>/pingpong_runs/<run_id>/` — `pingpong_loop._persist_run`
     (pingpong_loop.py:4234) via `_pingpong_runs_dir` (pingpong_loop.py:4228).
     Keyed by RUN id.
2. **The field-by-field shape of both job records** — `packages.core.models.Job`
   against `pingpong_job.JobPlan` — as a table: field, type, which record has
   it, and whether the two spellings mean the same thing. This is the evidence
   DECISION F260 D1 will be ruled from. Do NOT rule it here.
3. **Every id shape actually minted**, with its minting call site, and every
   parse or validation path constraining it — including `data_paths._SHORT_HEX_RE`
   (data_paths.py:150) and the `UUID(raw)` branch of `resolve_job_id`
   (data_paths.py:205). Evidence for D2. Do NOT rule it here.
4. **Every consumer named under "Design" in `docs/roadmap/features/T2_F260.md`**,
   re-grepped at `4b704705`: path, the symbol it actually calls, the line it
   calls it at, and a column saying whether the feature file's cited line still
   resolves. Those citations were taken 2026-09-05 and this branch has moved no
   production file, so a mismatch is a defect OF THE FEATURE FILE — report it,
   do not silently correct it.
5. **The `runs/` collision, stated as a measurement.** The feature file says
   `task_jobs/` "is renamed to `runs/`". Report what `data_paths.runs_dir`
   returns and what the run log already writes there, and state plainly whether
   the ordered rename lands on an occupied path.

Rule NOTHING. Rename nothing. Delete nothing. Do not change one line under
`packages/`, `apps/` or `tests/` this round. This round measures; round 3 rules.

## C6 — the feature-file amendment

Insert the AMENDF260D0 slice into `docs/roadmap/features/T2_F260.md` so the new
`### DECISION F260 D0` heading and its body sit immediately BEFORE the line
`### DECISION F260 D3 — the deletion paragraph (to be recorded in T005)`,
separated from the paragraph above and below it by exactly one blank line each.
Prove it by whole-file reconstruction: the post-edit file equals the pre-edit
file with exactly this slice inserted at that point and nothing else moved.

## C7 — the handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. No length cap.
Mandated sections, the changed-files table with `+/-` from `git diff --numstat`
(NOT before/after line counts — §3 item 28), one line per gate with real exit
code and real output, the item-status table, every deviation, and:

    SESSION 1 of feature F260 · round 2 · rounds so far 2

plus one sentence of context self-assessment (self_drive_protocol.md G7). The
state block repeats this line verbatim:

    ~10 % (T001 Inventar ✅ · D1/D2 offen · T002–T005 offen) — Schätzung

C7 is the LAST commit. Then `git push origin feature/f260-one-world`. No pull
request, no merge.

## Constraints

1. Apply every authored slice BYTE FOR BYTE. If one looks wrong, apply it as
   written and declare the problem — never silently repair it.
2. Nothing outside the change set is created, edited or deleted.
3. No file under `packages/`, `apps/` or `tests/` changes this round.
4. Commit order C0a, C0b, C1, C2, C3, C4, C5, C6, C7 — no extra, none dropped,
   none reordered.
5. Every commit single-parent, every insertion count under 500 (the `+` column
   only — DECISION F104 D1).
6. Destructive checks only inside a disposable `git worktree`; the primary
   checkout is `git status --porcelain` empty at the end.
7. `.agent/plan.md` stays under 50 lines.
8. Commit subjects carry no leading-slash token, no absolute path, no
   secret-like string.

## Done when — the gates

Every one runs for real; report its true exit code and true output.

- **G1 TRANSPORT.** `sha256sum .remedy-wt/f260-r2-block.md
  .agent/authored/f260-r2.md .agent/last_block.md` prints ONE digest three
  times, equal to the BLOCK_SHA the delegating prompt states. A COPY chain over
  scratch, saved copy and mirror; per §3 item 37 it is not a claim about bytes
  emitted into a prompt.
- **G2 THE RECORD.** Copy the pre-edit bytes to scratch first, then prove:
  (a) the post-edit file equals `head + "\n" + "\n## Steps\n" + tail + "\n" +
  GATE_R1 + "\n"`, where `head` and `tail` are the partition of the PRE-edit
  bytes — one boolean, byte-exact reconstruction;
  (b) the FINDINGS REGION GROWS ONLY BY THE APPEND. Locate the heading with the
  anchored pattern `^## Findings\s*$` and NOT with a plain substring search —
  the header blockquote mentions the same token in backticks 4 times at
  `4b704705`, and a substring search finds a mention instead of the heading.
  Assert exactly one anchored match, then prove `region_post ==
  region_pre + appended` where `appended` is `"\n" + GATE_R1 + "\n"`. This
  replaces round 1's G2(d), which demanded that region be IDENTICAL and was
  unmeetable for any round that books a verdict.
  (c) an independent structural reader, baselined on the REPAIRED INTERMEDIATE
  and not on the pre-image, because the repair itself adds a blank-line unit and
  only the append is what this reader is testing. Hold the repaired text in
  memory before appending; split it and the final post-image on blank lines;
  report N = post units − repaired units as a number your script COUNTS; and
  compare the LAST N units of the post-image against GATE_R1's paragraphs in
  order. Report the unit totals of all three images — pre, repaired, post — as
  measured numbers, and state them rather than any number you expected.
  (d) a negative control on reading (c): flip one byte inside the FIRST appended
  paragraph and confirm (c) REJECTS it — in scratch, never on the tracked file.
  (e) `grep -c '^Gate: R1 — the F260'` goes 0 → 1; no two `^Gate: R` headers in
  the file are byte-identical; the blank line before `## Steps` is present after
  C2 and the file grew by exactly one byte more than the append itself.
- **G3 THE SLIPS.** `.agent/prose_slips.md` post-image equals its pre-image plus
  exactly `"\n\n" + SLIP1 + "\n\n" + SLIP2`; it still ends WITHOUT a trailing
  newline; its dated-line count goes 112 → 114.
- **G4 THE STATUS PAIR.** FROM 1x before / 0x after; TO 0x before / 1x after;
  whole-file reconstruction from the pre-edit bytes with only this replacement
  applied is byte-equal to the committed file; the file still ends with exactly
  one newline; then `^- \[~\] F` = 1 and its id is F260, and `^- \[x\] F` = 73.
- **G5 THE INVENTORY IS MEASURED.** For EVERY `path:line` citation in
  `.agent/f260_inventory.md`, open that file at that line, print it, and assert
  the cited symbol occurs in it. Report the number of citations checked and the
  number that resolved. A citation that does not resolve is a RED gate, not a
  footnote. Confirm all four store paths are named, and that item 5 states
  explicitly whether the rename lands on an occupied path.
- **G6 THE STATE CONTRACTS.** `.agent/plan.md` holds `## Goal`, `## Next Steps`
  and a `\bF\d{3}\b` match, and is under 50 lines. `.agent/context.md` holds
  `Steps`, `## Active Branch`, `feature/`, a `\bF\d{3}\b` match, and `resource`
  or `pytest` case-insensitively, and none of `steps-74_1-79`, `Steps 91-100`,
  `allow repo_test_run`, `synthetic_count: 4`, `job=None source_apply bypass`.
  `.agent/live_review.md` holds `Steps`.
- **G7 THE SUITES, RUN SERIALLY, one at a time, in the primary checkout.**
  Report exit code and passed count for each:

      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/orchestration/test_roadmap_index.py -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q

  Round 1 measured 303, 30, 515, 52, 21, 16 and 42, every one exit 0. A
  different number is not automatically a failure — report what you get and, if
  it differs, name the node ids that account for the difference.
- **G8 STRUCTURE AND PUSH.** Every commit single-parent
  (`git log --format='%h %p' 4b704705..HEAD`) and every insertion count under
  500, reported per commit for C0a through C6. C7's own numbers cannot exist
  while C7 is being written and self-drive has no round report to route them to,
  so do NOT state them anywhere: the reviewer measures them at the next gate
  (§3 item 31). `git status --porcelain` empty. `git ls-files .remedy-wt` empty.
  The push result reported. `python3 -m apps.cli.grouped integrity check --json`
  prints `"passed": true`, `"fail_count": 0`.

## Handback

Completion report plus the `.agent/handoff.md` rewrite described at C7. Declare
every deviation. If a gate goes red, STOP there, do not route around it, and
report the exact output — as you correctly did in round 1.

────────────────────────── authored slices ──────────────────────────

<<<BEGIN PLANF260R2>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Round 1 committed C0a, C0b, C1 and C2 correctly and
stopped at a red gate whose two causes were both defects in the reviewer's own
block; those commits are kept and round 2 repairs the record and finishes the
work round 1 could not reach.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function; a Run becomes the evidence case a Job
points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Round 2 restores the one byte round 1's block cost the review record, books
round 1's verdict and the reviewer's two authoring slips, claims F260 in the
STATUS ledger, and writes `.agent/f260_inventory.md` — the measured reading of
every job, run and evidence area on disk, both job record shapes, every id shape
minted, and the re-grepped consumer list. It rules nothing.

## Next Steps

- Rule DECISION F260 D1 (where the classic job fields live) and D2 (the one id
  shape) from the inventory, and settle where a Run's evidence lives now that
  `<data_root>/runs/` is measured as already occupied by the run log.
- Write the one minting and resolving function and move every job-taking command
  onto it while both stores still exist (T001, part 2).
- T002: the extended Mission record, the unified Job record, the run directory.

## Risks

- The feature file orders `task_jobs/` "renamed to `runs/`" onto a path the run
  log already writes. The collision is recorded before anything moves; ruling it
  is round 3's first job.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLANF260R2>>>

<<<BEGIN GATE_R1>>>
Gate: R1 — the F260 R1 entry. VERDICT FAIL — THE ROUND'S BUNDLE IS INCOMPLETE, AND BOTH CAUSES ARE DEFECTS IN THE REVIEWER'S OWN BLOCK RATHER THAN IN THE WORKER'S EXECUTION. Range b5cd6c20..4b704705, five commits, all single-parent, insertions 457, 445, 53, 20 and the handback commit's own, every one far under the AGENTS.md 500-insertion cap. The worker executed C0a, C0b, C1 and C2 exactly as ordered, reached gate G2, measured it RED, stopped there, and declared both causes instead of routing around either — which is the behaviour planner_reviewer_prompt.md §3 item 8 predicts of an honest worker facing an unmeetable gate, and it is why those four commits are KEPT rather than reverted. The three remaining commits of the bundle — the STATUS claim, the inventory and the feature-file amendment — were not reached and move to round 2. THE FIRST DEFECT: gate G2(d) demanded that the region from `## Findings` to end of file carry an identical sha256 before and after the very commit ordered to append a gate record. Re-measured independently by the reviewer at `4b704705`: the anchored heading matches exactly once, 0 `Gate:` records sit above it and 10 below it, so the append necessarily lands INSIDE the region the gate required to be unchanged and no round that books a verdict can ever satisfy it. That is the unmeetable-gate class of R-0438 arriving through a region boundary rather than through a missing path, and §3 item 8 is the item that should have caught it. The reading the gate was reaching for does hold and was verified: `region_post == region_pre + appended`, true, with `appended` equal to `"\n" + GATE_R10 + "\n"`; the region digests are `9343bcc2…` before and `0d32b1f4…` after, reproducing the worker's two readings exactly. THE SECOND DEFECT: the authored REHEADTO slice ended without the blank line that had separated the header from `## Steps`, and the block ordered it applied as `REHEADTO + "\n## Steps\n" + tail`, so applying it byte-for-byte — which constraint 1 required — merged two blank-line units. Measured: the boundary went from `session start.\n\n## Steps\n` to `session start.\n## Steps\n`, unit totals ran 417 to 416 to 417, and N came out 0, which made the ordered "last N units" reader vacuous rather than wrong. Isolated to the append alone the same reader agrees perfectly at N = 1. Round 2 restores that single byte, which is legitimate because round 1 itself rewrote that header region and nothing below `## Findings` is touched by it — §3 item 20 forbids rewriting landed record text and this repair does not do that. NEITHER DEFECT SPENDS AN R-ID. Operator amendment amend0827-process-diet rule 2 reserves an id for a defect with product effect — wrong state under `packages/`, `apps/`, `tests/` or `docs/`, or a gate over PRODUCTION CODE shown blind or unmeetable — and both of these are gates over an `.agent/` prose file that left nothing wrong outside `.agent/`. They are recorded instead as two dated lines in `.agent/prose_slips.md` by the round that also repairs the byte. WHAT DID LAND IS SOUND, and the reviewer re-ran it rather than reading the handback for it: the transport digest `be04f05b0666b6078010c967410c2e2e28fd1cbd604c52006481ec3263bba9a7` appears once across the scratch original, the saved copy and the mirror; the re-head landed with the file's first line reading the F260 heading; the R10 gate entry landed; the finding population is unchanged at 298 registrations against 4 `Done:` lines, so 294 open, with the maximum id still R-0813; the seven ordered suites all ran exit 0 at 303, 30, 515, 52, 21, 16 and 42, every count equal to the reviewer's own pre-emission measurement; `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks at handlers=342; and the working tree is clean with nothing tracked under `.remedy-wt`. The state line the block ordered repeated verbatim was false when written — it claimed an inventory that C4 never reached — and the worker wrote it as ordered and set the correction directly beneath it, which is the right resolution of a byte-for-byte constraint against a false slice and is recorded here so the next reader is not misled by the file.
<<<END GATE_R1>>>

<<<BEGIN SLIP1>>>
2026-09-06 · F260 R1 (reviewer) · The round-1 block's gate G2(d) ordered the region from `## Findings` to end of file to carry an identical sha256 before and after the commit that C2 was separately ordered to APPEND a gate record into. Measured at `4b704705`: the anchored heading `^## Findings\s*$` matches exactly once, 0 `Gate:` records sit above it and 10 below it, so every gate record the ledger has ever held lives inside the region the gate demanded be unchanged, and no round that books a verdict can satisfy it. The worker measured it red and stopped, which cost the round its last three commits. THE LESSON: §3 item 8 asks whether the code makes a gate's asserted value impossible, and a REGION boundary is that same question asked about bytes — before ordering an identity over a region, locate the region and check whether the same commit writes into it. The reading the gate was reaching for is `region_post == region_pre + appended`, which measures true; identity was never the property, only the shortest thing to write. A second hazard sits in the same gate and is worth the sentence: locating that heading with a plain substring search finds one of the 4 backticked mentions of the token in the header blockquote rather than the heading itself, the R-0584 quoted-token class, so the anchored pattern is part of the fix and not a detail of it. Reviewer-authored gate defect over an `.agent/` prose file; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP1>>>

<<<BEGIN SLIP2>>>
2026-09-06 · F260 R1 (reviewer) · The round-1 block's REHEADTO slice was ordered applied as `REHEADTO + "\n## Steps\n" + tail` and ended without the blank line that had separated the review record's header from its `## Steps` heading, so a byte-for-byte application — which the block's own constraint 1 required — deleted that blank line and merged two blank-line units. The boundary went from `session start.\n\n## Steps\n` to `session start.\n## Steps\n` and the file's unit total ran 417 to 416 and back to 417 across the append, so the same block's structural reader computed N = 0 and its ordered "compare the LAST N units" clause became vacuous rather than false. The worker applied the slice as written, declared the consequence, and was right on both counts. THE LESSON: when a block orders a slice applied around a SEPARATOR it also names, the slice's own trailing bytes are part of the pair and are measured with it — the partition that produced `head` kept a trailing newline the replacement text did not restore, and nothing in the block compared the two. Reconstruct the intended post-image once at emission and diff it against the pre-image; a one-byte difference in a boundary is invisible by eye and fully visible to `==`. Reviewer-authored slice defect in an `.agent/` prose file, repaired in round 2 by restoring the single byte; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP2>>>

<<<BEGIN AMENDF260D0>>>
### DECISION F260 D0 (2026-09-06, F260 round 2) — the run directory the feature file names is already taken

RECORDED BEFORE D1 AND D2 BECAUSE BOTH DEPEND ON IT. The "Goal & Done" section
above says a Run "is the evidence-case folder that today is
`<data_root>/task_jobs/<16hex>/`" and that "The directory is renamed to
`runs/`". Measured at `b5cd6c20`, before any production line of this feature was
written, that sentence is wrong twice over and the rename it orders lands on an
occupied path:

- `<data_root>/task_jobs/<16hex>/` is keyed by JOB id and holds `job.json`,
  written by `pingpong_job._persist_job`. It is a JOB record, not a run's
  evidence case.
- `<data_root>/runs/` already exists and is already written: `data_paths.runs_dir`
  returns it and `run_log.RunLogWriter` files run logs at
  `<data_root>/runs/<job_id>/*.jsonl`, which `timeline.load_run_events` reads.
  It too is keyed by JOB id.
- The directory actually keyed by RUN id is `<data_root>/pingpong_runs/<run_id>/`,
  written by `pingpong_loop._persist_run`.

A plain rename of `task_jobs/` to `runs/` would therefore merge two directories
keyed by the same job id but holding different things, and would still leave the
one directory keyed by run id outside the model — while the vocabulary page F259
made binding gives a Job MANY runs, which no job-keyed directory can express.

CHOSEN: this feature does not perform that rename as written. Round 2 records
the measured areas in `.agent/f260_inventory.md`; DECISION F260 D1 is widened to
rule the RUN directory as well as the job fields, and must state, for each area
the inventory finds, whether it survives, moves or is deleted, and what the
surviving directory is keyed by. Nothing moves on disk until D1 is recorded.

ALTERNATIVES CONSIDERED. Renaming `task_jobs/` to `runs/` as written and letting
the run log share the directory — rejected: it merges two job-keyed stores whose
contents answer to different concepts, and leaves `pingpong_runs/` stranded.
Keeping `task_jobs/` under its present name — rejected: the whole point of the
feature is that the name lies about what the directory holds.

REVERSE by deleting this paragraph and restoring the "Goal & Done" sentence as
the binding order, at which point the rename becomes a required slice and the
collision above becomes a defect to be repaired inside it.
<<<END AMENDF260D0>>>
