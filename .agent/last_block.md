── STEP T001 (part 2) — F260 ─────────────────────────────────
Goal:        Rule DECISION F260 D1 and D2 from round 2's measured inventory,
             register the storage defect that inventory found, and book round
             2's verdict. Design only — no production line moves this round.
Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the record
             (R-0814 registration + the R2 gate entry) · C3 the two rulings ·
             C4 the handback
(the rule line below is 62 copies of U+2500, per §3 item 37)
──────────────────────────────────────────────────────────────

## Where this round starts

Continuing on `feature/f260-one-world` at `bd42e0bc`, already pushed. Do NOT
create a branch, do NOT merge, do NOT create a pull request. Round 2 PASSED: the
reviewer re-ran every gate and reproduced every number, including the record
arithmetic 860937 → 860938 → 865153 and the region digest `0d32b1f4…`, which
independently matches the reviewer's own round-1 reading.

## Change set — nothing outside this list

    .agent/authored/f260-r3.md          (new, C0a)
    .agent/last_block.md                (C0b)
    .agent/plan.md                      (C1)
    .agent/live_review.md               (C2)
    docs/roadmap/features/T2_F260.md    (C3)
    .agent/handoff.md                   (C4)

`.remedy-wt/` scratch stays untracked; `git ls-files .remedy-wt` returns nothing.

## C0a / C0b — save and mirror

The block is at `.remedy-wt/f260-r3-block.md`; the delegating prompt states its
sha256 (BLOCK_SHA — a file cannot carry its own digest). COPY it to
`.agent/authored/f260-r3.md` with `shutil.copyfile`, commit alone; copy the same
bytes to `.agent/last_block.md`, commit alone. The mirror is one indivisible
`.agent/**` state rewrite (AGENTS.md DECISION F104 D1 exemption).

## C1 — the plan

`.agent/plan.md` from the PLANF260R3 slice, byte-for-byte plus exactly one
trailing newline. FIRST substantive commit, because this round touches the
finding ledger (§3 item 23).

## C2 — the record: register, then book

One commit, appending BOTH paragraphs to `.agent/live_review.md` in one write:

    appended = "\n" + R0814 + "\n" + "\n" + GATE_R2 + "\n"

The finding paragraph comes FIRST, per planner_reviewer_prompt.md §4 item 4.
Measured at `bd42e0bc`: the file is 865153 bytes, ends with exactly one newline,
holds 298 `^- R-\d{4} — ` registrations against 4 `^Done: R-\d{4} — ` lines, and
its maximum finding id is R-0813 — so R-0814 is the next free id. Findings and
gate records are interleaved chronologically at the tail of this file; both new
paragraphs go at the END, which is that convention.

Per §3 item 30 the open set was searched for the DEFECT before this id was
minted, not merely for a free number: `resolve_any_job_id`, `task_jobs`,
`jobs_dir`, `evidence` and `shadow` over `.agent/live_review.md` return no open
finding describing the split storage root R-0814 names.

## C3 — the two rulings

Two REWRITE pairs in `docs/roadmap/features/T2_F260.md`, applied with
`str.replace(FROM, TO, 1)` after asserting each FROM occurs exactly once.
Measured at `bd42e0bc`: D1's heading is at line 63 and D2's at line 68; for both
pairs `TO contains FROM: false`, so both are REWRITES and the FROM-zero count
after is attainable. Apply D1PAIR first, then D2PAIR, to the same file in one
commit.

Strip exactly one trailing newline from each extracted slice before replacing —
the markers sit on their own lines, so a raw extraction carries the newline that
precedes the END marker.

## C4 — the handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. No length cap.
Mandated sections, the changed-files table with `+/-` from `git diff --numstat`
(NOT before/after line counts — §3 item 28), one line per gate with real exit
code and real output, the item-status table, every deviation, and:

    SESSION 1 of feature F260 · round 3 · rounds so far 3

plus one sentence of context self-assessment (self_drive_protocol.md G7). The
state block repeats this line verbatim:

    ~18 % (T001 ✅ inkl. D1/D2 · T002–T005 offen) — Schätzung

C4 is the LAST commit. Then `git push origin feature/f260-one-world`. No pull
request, no merge.

## Constraints

1. Apply every authored slice BYTE FOR BYTE. If one looks wrong, apply it as
   written and declare the problem — never silently repair it.
2. Nothing outside the change set is created, edited or deleted.
3. NO file under `packages/`, `apps/` or `tests/` changes this round. This is a
   design round; the code that implements D1 and D2 is round 4's work.
4. Commit order C0a, C0b, C1, C2, C3, C4 — no extra, none dropped, none
   reordered.
5. Every commit single-parent, every insertion count under 500 (the `+` column
   only — DECISION F104 D1).
6. Destructive checks only inside a disposable `git worktree`; the primary
   checkout is `git status --porcelain` empty at the end.
7. `.agent/plan.md` stays under 50 lines.
8. Commit subjects carry no leading-slash token, no absolute path, no
   secret-like string.

## Done when — the gates

Every one runs for real; report its true exit code and true output.

- **G1 TRANSPORT.** `sha256sum .remedy-wt/f260-r3-block.md
  .agent/authored/f260-r3.md .agent/last_block.md` prints ONE digest three
  times, equal to the BLOCK_SHA the delegating prompt states. A COPY chain over
  scratch, saved copy and mirror; per §3 item 37 it is not a claim about bytes
  emitted into a prompt.
- **G2 THE RECORD.** Copy the pre-edit bytes to scratch first, then prove:
  (a) the post-edit file equals the pre-edit bytes plus exactly
  `"\n" + R0814 + "\n" + "\n" + GATE_R2 + "\n"` — the pre-image is a byte-exact
  PREFIX and the remainder is that string, two booleans;
  (b) THE FINDINGS REGION GROWS ONLY BY THE APPEND. Locate the heading with the
  anchored pattern `^## Findings\s*$`, NOT with a plain substring search — the
  header blockquote mentions the same token in backticks and a substring search
  finds a mention instead of the heading. Assert exactly one anchored match,
  then prove `region_post == region_pre + appended`;
  (c) an independent structural reader: split pre and post on blank lines,
  report N = post units − pre units as a number your script COUNTS, and compare
  the LAST N units of the post-image against the appended slices in order —
  R0814 first, GATE_R2 second. Report the unit totals you measure;
  (d) a negative control on reading (c): flip one byte inside the FIRST appended
  paragraph — that is R0814, not GATE_R2 — and confirm (c) REJECTS it, in
  scratch, never on the tracked file;
  (e) `grep -c '^- R-0814 — '` goes 0 → 1 and `grep -c '^Gate: R2 — the F260'`
  goes 0 → 1; the registration count goes 298 → 299 while the `Done:` count
  stays 4; no two `^Gate: R` headers in the file are byte-identical.
- **G3 THE TWO RULINGS.** For EACH pair independently: FROM occurs 1x before and
  0x after; TO occurs 0x before and 1x after; and print the containment test's
  own output, the words `TO contains FROM: false`, beside each. Then whole-file
  reconstruction: the committed file equals the pre-edit bytes with ONLY these
  two replacements applied, one boolean, and the file still ends with exactly
  one newline. Finally `grep -c '^### DECISION F260 D'` is 4 (D-A is not in that
  pattern) and each of D0, D1, D2, D3 occurs exactly once.
- **G4 THE STATE CONTRACTS.** `.agent/plan.md` holds `## Goal`, `## Next Steps`
  and a `\bF\d{3}\b` match, and is under 50 lines. `.agent/context.md` holds
  `Steps`, `## Active Branch`, `feature/`, a `\bF\d{3}\b` match, and `resource`
  or `pytest` case-insensitively, and none of `steps-74_1-79`, `Steps 91-100`,
  `allow repo_test_run`, `synthetic_count: 4`, `job=None source_apply bypass`.
  `.agent/live_review.md` holds `Steps`.
- **G5 THE SUITES, RUN SERIALLY, one at a time, in the primary checkout.**
  Report exit code and passed count for each:

      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/orchestration/test_roadmap_index.py -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q

  Rounds 1 and 2 both measured 303, 30, 515, 52, 21, 16 and 42, every one exit 0.
  A different number is not automatically a failure — report what you get and,
  if it differs, name the node ids that account for the difference.
- **G6 STRUCTURE AND PUSH.** Every commit single-parent
  (`git log --format='%h %p' bd42e0bc..HEAD`) and every insertion count under
  500, reported per commit for C0a through C3. C4's own numbers cannot exist
  while C4 is being written and self-drive has no round report to route them to,
  so do NOT state them anywhere: the reviewer measures them at the next gate
  (§3 item 31). `git status --porcelain` empty. `git ls-files .remedy-wt` empty.
  The push result reported. `python3 -m apps.cli.grouped integrity check --json`
  prints `"passed": true`, `"fail_count": 0`.

## Handback

Completion report plus the `.agent/handoff.md` rewrite described at C4. Declare
every deviation. If a gate goes red, STOP there, do not route around it, and
report the exact output — as you correctly did in rounds 1 and 2.

────────────────────────── authored slices ──────────────────────────

<<<BEGIN PLANF260R3>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 and 2 are reviewed; round 2 PASSED and put the
measured inventory on disk as `.agent/f260_inventory.md`.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function; a Run becomes the evidence case a Job
points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Round 3 closes T001 by ruling DECISION F260 D1 (the record layout, and where a
Run's evidence lives) and D2 (the one id shape) from round 2's inventory, and
registers finding R-0814 — the split storage root that inventory measured, where
one ping-pong job files its record under `task_jobs/<16hex>/` and its evidence
under the classic store's `jobs/<16hex>/evidence/`. It changes no production
line; the code that implements the rulings is round 4.

## Next Steps

- T001 part 3: the one minting and resolving function, with its mutation
  red-proof, and every job-taking command moved onto it while both stores still
  exist.
- T002: the extended Mission record, the unified Job record under
  `jobs/<16hex>/`, and the run directory keyed by run id. R-0814 is fixed here,
  because the layout D1 rules is what removes the split root.
- T003 consumer by consumer, T004 the classic runner, T005 the reachability test
  and the cluster deletion, in that order.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as the writer, or a run
  log becomes unreadable between two commits.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLANF260R3>>>

<<<BEGIN R0814>>>
- R-0814 — Medium, ONE PING-PONG JOB FILES ITS RECORD AND ITS EVIDENCE UNDER TWO DIFFERENT DATA ROOTS, BECAUSE A MODULE-LOCAL `_jobs_dir` SHADOWS THE IMPORTED `jobs_dir`. Found by the WORKER of F260 R2 while writing the measured inventory `.agent/f260_inventory.md`, and confirmed independently by the reviewer at `bd42e0bc` by reading the four call sites. In `packages/orchestration/pingpong_job.py` the module-local `_jobs_dir()` (pingpong_job.py:374) returns `task_jobs_dir()` (pingpong_job.py:378) and is what `_persist_job` uses to write `task_jobs/<16hex>/job.json` (pingpong_job.py:382); but `job_evidence_dir` (pingpong_job.py:3050) imports the CLASSIC `jobs_dir` from `data_paths` (pingpong_job.py:3052) and returns `jobs_dir() / job_id / "evidence"` (pingpong_job.py:3053), as does `_task_stream_dir` (pingpong_job.py:3566-3567). So a single ping-pong job writes its record under `<data_root>/task_jobs/<16hex>/` and its evidence under `<data_root>/jobs/<16hex>/evidence/` — the CLASSIC store's root, keyed by a non-classic id shape. PRODUCT EFFECT, which is why this spends an id rather than a `.agent/prose_slips.md` line under operator amendment amend0827-process-diet rule 2: the wrong state is on disk under `packages/`, and it is wrong in two ways that compound. First, `<data_root>/jobs/` ends up holding BOTH `<uuid>.json` FILES and `<16hex>/` DIRECTORIES, two different shapes in one store. Second, `data_paths._classic_job_id_matches` (data_paths.py:153) globs `*.json` and therefore cannot see those directories at all, so the evidence root of a ping-pong job is invisible to every id resolver in the repository — which is the same blindness `resolve_any_job_id` exists to paper over, arriving through a second door nobody had named. Medium rather than High because nothing is lost or corrupted: both paths are written and read consistently by their own callers, and the defect surfaces as unfindable evidence rather than as a crash. Searched before minting per §3 item 30: `grep` over the open set for `resolve_any_job_id`, `task_jobs`, `jobs_dir`, `evidence` and `shadow` returns no open finding describing this split root; the nearest neighbours are the two-store findings this feature exists to close, and none of them names the evidence directory. ROOT CAUSE, stated so the class is visible: a module-local helper was given the name of an imported function it does not agree with, so both spellings read correctly at their own call sites and only a whole-module reading shows they disagree — the AGENTS.md "one spelling per concept" rule failing inside a single file rather than across the repository. FIX: DECISION F260 D1 rules the unified layout that removes the split — the job record and its evidence share one root `<data_root>/jobs/<16hex>/` — and the local `_jobs_dir` is deleted with the store it names. Resolved when `packages/orchestration/pingpong_job.py` contains no module-local `_jobs_dir`, every evidence path is built from the same directory function as the record path, and a test asserts that a job's record and its evidence resolve under one root.
<<<END R0814>>>

<<<BEGIN GATE_R2>>>
Gate: R2 — the F260 R2 entry. R2 REPAIRED THE RECORD BYTE ROUND 1 COST, BOOKED ROUND 1'S VERDICT AND THE REVIEWER'S TWO SLIPS, CLAIMED F260 IN THE LEDGER, AND WROTE THE MEASURED T001 INVENTORY. VERDICT PASS. Range 4b704705..bd42e0bc, nine commits, all single-parent, pushed, no pull request; largest commit 384 insertions, so no commit approached the AGENTS.md 500-insertion cap. THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback for it, and reproduced every number the worker reported. TRANSPORT: one digest `a413a4b676098eb77b07f2b2e19d321ae00ca9b7ce7e34049dfca6972c7b389a` across the scratch original, the saved copy and the mirror; per §3 item 37 that is a COPY chain and not a claim about bytes emitted into a prompt. THE RECORD: 860937 bytes before, 860938 after the one-byte blank-line repair, 865153 after the append; the append is 4215 bytes and the total growth 4216, exactly one more, which is the arithmetic that proves the repair and the append are the only two changes. The repaired image is a byte-exact PREFIX of the post-image; the blank line before `## Steps` is restored; blank-line units run 417, 418, 419 so the append's N counts 1. The anchored heading `^## Findings\s*$` matches exactly once where a plain substring search matches 7 times — the R-0584 quoted-token hazard the round-1 block walked into and this block named — and `region_post == region_pre + appended` is true with `region_pre` hashing `0d32b1f4…`, which is the SAME digest the reviewer independently measured as round 1's post-image, so the two rounds' readings agree across a session boundary. Eleven `Gate:` headers, all distinct; the finding population is unchanged at 298 registrations against 4 `Done:` lines. THE SLIPS: `.agent/prose_slips.md` grew 85098 to 88132, the post-image starts with the pre-image byte-for-byte, it still ends WITHOUT a trailing newline, and its dated-line count went 112 to 114. THE STATUS CLAIM: exactly one `^- \[~\] F` line and its id is F260; `^- \[x\] F` is 73, unchanged; the old unchecked F260 line is gone. THE INVENTORY, which was the round's real work and is the reason this round is not bookkeeping: the reviewer re-resolved every `file:line` citation in `.agent/f260_inventory.md` against the committed tree — 98 distinct citations, ZERO unresolvable and ZERO ambiguous basenames — and spot-checked eight of them against the symbol each names, all eight landing on the right line, including `storage.save_job` at storage.py:75, `pingpong_job._persist_job` at pingpong_job.py:381, `run_log.RunLogWriter` at run_log.py:94, `timeline.load_run_events` at timeline.py:68 and `pingpong_loop._persist_run` at pingpong_loop.py:4234. THE INVENTORY CORRECTED THE REVIEWER TWICE AND THE FEATURE FILE TWICE, and all four corrections were verified: `RunLogWriter` is at run_log.py:94 and not the 114 the round-2 block cited, and `load_run_events` at timeline.py:68 and not 75 — in both cases the block had cited a line INSIDE the symbol rather than the symbol's own statement, which is §3 item 9 asking for the symbol over the number and getting the number; `bench_run.py` accesses no job at all, so the feature file's Design bullet grouping it with `gauntlet_runner.py` is unsupported; and the `decision_inbox.py` bullet has its direction inverted, since that module receives an already-loaded job rather than loading one. It also found a FIFTH storage area the reviewer's own list of four had missed — `<data_root>/jobs/<16hex>/evidence/` — which the reviewer confirmed at the four call sites and which is registered by this round as R-0814. THE SUITES were re-run by the reviewer serially and all matched: 303, 30, 515, 52, 21, 16 and 42, every one exit 0, plus `test_self_use_generator.py` at 20. `integrity check --json` returns `"passed": true` with `"fail_count": 0` over 5 checks at handlers=342, the working tree is clean, and nothing under `.remedy-wt` is tracked. SEVEN DEVIATIONS WERE DECLARED AND ALL ARE SOUND; three deserve the record. The worker's own G2(c) probe went red twice before the file did, both times a trailing-newline artifact of its splitter rather than a defect of the append, and it normalised the splitter rather than the gate — the right repair, and it kept the ordered clause and the non-vacuity check. Its first G3 pattern miscounted the slips because one existing line uses an em dash rather than the separator the pattern assumed; the block's figure of 112 was correct and the probe was not. And it caught two defects in its OWN inventory draft before committing: fifteen `models.py:N` citations were ambiguous across three tracked files of that name and its checker had silently resolved them to the wrong one, so it qualified every path and made the checker FAIL on ambiguity instead of guessing — which is why the reviewer's independent re-resolution found zero ambiguous citations. That is a worker strengthening a gate against itself, and it is the reason this round's inventory can be trusted as evidence for D1 and D2.
<<<END GATE_R2>>>

    <<<BEGIN D1PAIR_FROM>>>
### DECISION F260 D1 — where the classic job fields live (to be recorded in T001)
Read both writers before deciding. Record: which fields of the classic `Job`
(`packages/core/models.py`) move into the unified job record, which are dropped, and
the resulting file layout under `<data_root>/`.
    <<<END D1PAIR_FROM>>>

    <<<BEGIN D1PAIR_TO>>>
### DECISION F260 D1 (2026-09-06, F260 round 3) — the unified record layout, ruled from the measured inventory
Ruled from `.agent/f260_inventory.md`, written and gated in round 2 and re-verified
by the reviewer at `bd42e0bc`. That inventory measured the classic `Job`
(`packages/core/models.py:222`) at 15 fields and `pingpong_job.JobPlan`
(`pingpong_job.py:288`) at 56, sharing exactly four NAMES — `budgets`,
`created_at`, `metadata`, `tasks` — and not one shared name with a matching type.
The split is not arbitrary: the classic record is ADMINISTRATIVE (mission,
project, fences, budget, intake, flight plan, order text) and `JobPlan` is
EXECUTIONAL (workspace, worktree, stop episode, run manifest, result diff).

CHOSEN — one record, three areas, each keyed by exactly one kind of id:

- `<data_root>/jobs/<16hex>/job.json` — THE JOB. It carries `JobPlan`'s execution
  fields plus the eleven classic-only administrative fields (`artifacts`,
  `budget`, `fences`, `flight_plan`, `intake`, `mission`, `name`, `project_id`,
  `state`, `user_prompt`, and `id` as the 16-hex `job_id` of D2). The job's own
  evidence lives beside its record, under `<data_root>/jobs/<16hex>/evidence/`.
- `<data_root>/runs/<run_id>/` — THE RUN, keyed by RUN id and not by job id. It
  inherits what `<data_root>/pingpong_runs/<run_id>/` holds today plus the
  run-log `.jsonl` that today sits at `<data_root>/runs/<job_id>/`. This is the
  change that makes `Job.run_refs` plural and truthful: F259's binding
  vocabulary gives a Job MANY runs, which no job-keyed directory can express.
- `<data_root>/missions/<project>/<id>.json` — THE MISSION, unchanged by this
  decision beyond the F056 extension the feature file's T002 already orders.

The four shared names are resolved toward the typed spelling, because a type is
recoverable from a string and a string is not recoverable from a type:
`tasks` is `list[TaskEntry]`, `created_at` is `datetime` serialised as ISO-8601,
`budgets` is the `JobBudgets` model rather than a `model_dump` dict, and
`metadata` stays `dict[str, Any]`. `status` and `state` are ONE field, the
`RunState` enum; the bare string spelling is dropped.

DELETED by this ruling, with no attic, alias or compatibility reader (DECISION
D-A and AGENTS.md "Replacing is deleting"): `<data_root>/jobs/<uuid>.json`,
`<data_root>/task_jobs/`, `<data_root>/pingpong_runs/`, and the module-local
`pingpong_job._jobs_dir`. This is also the FIX for finding R-0814 — the record
and its evidence share one root, so the shadowed spelling has nothing left to
disagree with.

ALTERNATIVES CONSIDERED. Keeping `runs/` keyed by JOB id and nesting runs beneath
it — rejected: it preserves the very ambiguity D0 recorded, since `runs/<job_id>/`
and a renamed `task_jobs/<job_id>/` are then the same path, and it still cannot
express many runs per job. Moving the administrative fields into the Mission and
leaving the Job purely executional — rejected: `job_context`, `job show` and the
cockpit all read budgets and fences per JOB, so the fields would have to be
re-joined at every read.

REVERSE by deleting this paragraph, at which point D1 returns to its unruled form
and the layout above becomes one option among the alternatives listed.
    <<<END D1PAIR_TO>>>

    <<<BEGIN D2PAIR_FROM>>>
### DECISION F260 D2 — the one id shape (to be recorded in T001)
16-hex (`uuid4().hex[:16]`) unless the writers prove otherwise; the minting function
is named here once it exists, and every job-taking command resolves through it.
    <<<END D2PAIR_FROM>>>

    <<<BEGIN D2PAIR_TO>>>
### DECISION F260 D2 (2026-09-06, F260 round 3) — the one id shape is 16-hex, and ids of different KINDS are minted by different functions
Ruled from `.agent/f260_inventory.md` §3, which measured THREE shapes actually
minted today — a 36-character canonical UUID, a 32-hex string and a 16-hex string
— and found the 16-hex shape already naming FOUR different kinds of thing: a
ping-pong job (`pingpong_job.py:290`), a ping-pong run (`pingpong_loop.py:122`),
a run episode (`pingpong_job.py:2268`) and a stop request (`safe_points.py:153`).

CHOSEN: 16-hex, `uuid4().hex[:16]`, as the feature file proposed — the writers
did not prove otherwise. The evidence for it rather than the UUID: 16-hex is
already the shape of the store that SURVIVES D1; `data_paths._SHORT_HEX_RE`
(`data_paths.py:150`) accepts `[0-9a-fA-F]{4,32}` and so accepts it already;
`safe_points.validate_job_id` (`safe_points.py:137`) accepts all three shapes; and
the probe recorded in the inventory settles the other direction — `UUID(
'a1b2c3d4e5f60718')` raises `ValueError: badly formed hexadecimal UUID string`,
which is exactly why `resolve_job_id` can never resolve a ping-pong job id. A
UUID cannot hold a 16-hex id; a 16-hex field can hold neither more nor less than
what it is minted with, and everything already mints it.

AND, because the same shape names four kinds of thing, ONE SHAPE IS NOT ONE
FUNCTION. Each kind gets its own minting function with a domain word in its name,
so a swapped argument is greppable and reviewable even though it is not a type
error: `mint_job_id()`, `mint_run_id()`, `mint_episode_id()` and the existing
`safe_points.new_request_id`. All live in ONE module, and `data_paths` is that
module because it already owns every other "where does this live" answer. This is
AGENTS.md's "distinct ID/value types where an argument swap is plausible" applied
at the weakest form the language allows for free — a name — and it is why this
decision does not simply say "16-hex" and stop.

RESOLUTION: `resolve_job_id` and `resolve_any_job_id` are both deleted and
replaced by ONE resolver over the one store D1 rules, returning `str`. The `UUID`
parse path goes with them, and so does `data_paths._SHORT_HEX_RE`'s role as a
job-id validator — it is not the id's definition, only a prefix filter.
`run_log.new_run_id`'s 32-hex remains as the name of one run-log SESSION file,
which is not an id any command takes.

ALTERNATIVES CONSIDERED. The canonical UUID for everything — rejected on the
probe above plus the migration it would force on every 16-hex writer, against
DECISION D-A's no-migration rule. One `mint_id()` for all kinds — rejected: it
makes the four kinds indistinguishable at every call site, which is the defect
R-0814 is an instance of, arriving through ids instead of directories.

REVERSE by deleting this paragraph; the shape then returns to the feature file's
unruled proposal and the four minting functions collapse back to whatever each
writer does today.
    <<<END D2PAIR_TO>>>
