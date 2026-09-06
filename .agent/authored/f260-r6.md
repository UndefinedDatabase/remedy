── STEP T001 close / T002 open — F260 ────────────────────────
Goal:        Rule the resolver's ordering as DECISION F260 D4, and ship the ONE
             spelling of DECISION F260 D1's layout — `job_dir`, `job_record_path`,
             `job_evidence_dir`, `run_dir` in `data_paths` — then put
             `pingpong_job`'s two hand-built evidence paths onto it.
Bundle:      C0a save this block · C0b mirror it · C1 the record (the R5 gate
             entry) · C2 two reviewer slips · C3 the plan · C4 DECISION F260 D4
             · C5 the path functions, the two call sites and their tests · C6
             the handback
(§3 item 37: the STEP line above is 62 characters ending in a run of U+2500,
 and the rule line below is 62 copies of U+2500 and nothing else)
──────────────────────────────────────────────────────────────

## Where this round starts

Continuing on `feature/f260-one-world` at `3aaeb042`, already pushed. Do NOT
create a branch, do NOT merge, do NOT open a pull request.

Round 5 PASSED. The reviewer re-ran all eight gates itself, reproduced the ledger
arithmetic, re-ran the three mutations in its own disposable worktree and re-ran
all seven suites. BOTH of your deviations are UPHELD and both are recorded — C2
below carries them as dated lines in `.agent/prose_slips.md`, which is where
operator amendment amend0827-process-diet rule 2 puts a reviewer-prose
inaccuracy that left nothing wrong on disk. You were right about the slice
boundary and you were right that G2(c) could not do what it said.

## Change set — nothing outside this list

    .agent/authored/f260-r6.md                   (new, C0a)
    .agent/last_block.md                         (C0b)
    .agent/live_review.md                        (C1)
    .agent/prose_slips.md                        (C2)
    .agent/plan.md                               (C3)
    docs/roadmap/features/T2_F260.md             (C4)
    packages/orchestration/data_paths.py         (C5)
    packages/orchestration/pingpong_job.py       (C5)
    tests/test_data_paths.py                     (C5)
    .agent/handoff.md                            (C6)

`.remedy-wt/` scratch stays untracked; `git ls-files .remedy-wt` returns nothing.

## C0a / C0b — save and mirror

The block is at `.remedy-wt/f260-r6-block.md`; the delegating prompt states its
sha256 (BLOCK_SHA — a file cannot carry its own digest). COPY it to
`.agent/authored/f260-r6.md` with `shutil.copyfile`, commit alone; copy the same
bytes to `.agent/last_block.md`, commit alone. Do not retype either.

## C1 — the record

APPEND to `.agent/live_review.md`, in one commit of its own, exactly the bytes
`"\n"` + the GATE_R5 slice + `"\n"`. The GATE_R5 slice is everything between its
marker lines EXCLUDING the newline that ends the last content line — the reading
you derived from the R3 precedent last round and stated in your deviation 1 is
correct and is now the block's own rule. The file is 881955 bytes at `3aaeb042`
and ends with a single newline; it still ends with a single newline afterwards.

## C2 — the slips

APPEND to `.agent/prose_slips.md`, in one commit of its own, exactly the bytes
`"\n"` + the SLIP4 slice + `"\n"` + the SLIP5 slice + `"\n"`. This file is
append-only: nothing already in it changes by one byte.

## C3 — the plan

REPLACE `.agent/plan.md` entirely with the PLANF260R6 slice plus one trailing
newline. Commit alone.

## C4 — the DECISION

Apply the D4PAIR FROM/TO pair to `docs/roadmap/features/T2_F260.md`, which is
22955 bytes at `3aaeb042`. The reviewer ran the containment test at emission:

    TO contains FROM: false

so this pair is a REWRITE, and the §4.9 "FROM 0x, TO 1x" reading IS attainable and
IS ordered in G4. It reads as an insertion by eye — both anchors survive — but the
FROM's bytes are contiguous and the inserted paragraph splits them, which is why
the shape is decided by the test and never by the eye (§3 item 15). Measured at
`3aaeb042`: FROM occurs 1x before and 0x after, TO 0x before and 1x after. Commit
alone.

## C5 — what to build

DECISION F260 D1 rules one root per job: the record at
`<data_root>/jobs/<16hex>/job.json` and that job's evidence at
`<data_root>/jobs/<16hex>/evidence/`, with runs keyed by RUN id under
`<data_root>/runs/<run_id>/`. Today that layout is spelled BY HAND at six call
sites in five modules, which is finding R-0814's root cause — "one spelling per
concept" failing inside a file and then across them. `data_paths` already owns
every other "where does this live" answer, so it owns these.

ADD to `packages/orchestration/data_paths.py`, between `mint_episode_id` and
`_SHORT_HEX_RE`, four functions, each taking an optional `root: Path | None = None`
exactly as `jobs_dir` and `runs_dir` already do, and each built on the one above it
rather than re-deriving the root:

    job_dir(job_id, root=None)          -> jobs_dir(root) / job_id
    job_record_path(job_id, root=None)  -> job_dir(...) / "job.json"
    job_evidence_dir(job_id, root=None) -> job_dir(...) / "evidence"
    run_dir(run_id, root=None)          -> runs_dir(root) / run_id

Give the group ONE comment above it naming DECISION F260 D1 and why `data_paths`
owns the answer, and each function a first-line docstring naming WHAT the path
holds. Extend the module docstring's `Public API::` block with the four names, in
the shape the existing entries use.

STATE THE TRANSIENT HONESTLY, in `job_record_path`'s docstring: nothing writes
there YET. The live ping-pong record is still at
`<data_root>/task_jobs/<16hex>/job.json` via `pingpong_job._persist_job`, and
T002 moves that writer. A reader who takes `job_record_path` for a live path
today finds nothing, so the docstring says which task moves the writer. Do NOT
move the writer in this round — `data_paths._task_job_id_matches` is the only
thing that finds a ping-pong job, and moving the record without the resolver
breaks `remedy teach narrate` for every one of them.

THEN, in `packages/orchestration/pingpong_job.py`, put its two hand-built
evidence paths onto the new function. Both already return exactly what
`data_paths.job_evidence_dir` returns, so this changes no path and no behaviour:

  * `job_evidence_dir` (`pingpong_job.py:3055` at `3aaeb042`) — its body becomes a
    call to `data_paths.job_evidence_dir`. Keep the function-scoped import style
    the surrounding code uses. Its docstring says that `data_paths` owns the
    layout and that this NAME survives only until T004 moves its remaining
    callers, so a reader does not mistake it for a second answer.
  * `_task_stream_dir` (`pingpong_job.py:3568` at `3aaeb042`) — same, then
    `/ "task_runs" / task_id`.

Re-grep both symbols before editing; those line numbers were read at `3aaeb042`.
Change NOTHING else in that module. In particular `_jobs_dir`, `_persist_job` and
`load_job_plan` are out of scope — they move in T002, and the four remaining
hand-built evidence paths (`job_evidence.py` twice, `repair_attest.py`,
`do_cmd.py`) move in the round after this one.

TESTS — extend `tests/test_data_paths.py` with ONE new class. What the reviewer
proved bites, in its own dry run at `3aaeb042`, so you know these are worth having:
the record and the evidence share one root; `job_dir` is `jobs_dir` keyed by the
job id; the record is `job.json`; `run_dir` is under `runs_dir` and NOT under
`jobs_dir`; the `root` override is honoured by all four; `pingpong_job`'s two
paths EQUAL the `data_paths` ones; and no `jobs_dir() / job_id / "evidence"`
expression survives in `pingpong_job.py`. That last one is a text reading and the
one before it a value reading, and BOTH are needed: the hand-built path is EQUAL
to the new one, so the equality test alone cannot see a regression to it.

## Constraints

1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it
   anyway and say so in the handback's deviations — do not repair it.
2. Nothing outside the change set above is created, edited or deleted.
3. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6, each its own commit. C5 is
   ONE commit: the functions, the two call sites and the tests land together.
4. Every mutation of G6 runs ONLY inside a disposable `git worktree` under
   `.remedy-wt/` (self_drive_protocol.md G5), removed with
   `git worktree remove --force` before C6. Never `git checkout --` a mutated
   primary file to undo one.
5. Purge `__pycache__` or run `python3 -B` for every mutation run.
6. Gates G1 through G8 all run AT C5, before C6 is written, so the handback can
   quote each one's real exit code (§3 item 31). The handback commit's own
   numbers are owed by no one; the reviewer measures the branch tip itself.
7. `git status --porcelain` is empty at C6. Re-read `.agent/STOP` from disk before
   C5; if it exists, finish the commit in hand, write the handback and stop.
8. Push after C6: `git push origin feature/f260-one-world`. Never force-push.

## Done when — eight gates, each run and its real exit code recorded

G1 TRANSPORT (one digest). `sha256sum` over `.remedy-wt/f260-r6-block.md`,
   `.agent/authored/f260-r6.md` and `.agent/last_block.md` returns ONE value equal
   to BLOCK_SHA. Report the digest.

G2 THE RECORD. At C1: report `.agent/live_review.md` before and after and that the
   growth equals the appended byte count exactly. Prove (a) the 881955-byte
   pre-image is a byte-exact PREFIX; (b) the remainder is exactly `"\n"` + the
   GATE_R5 slice + `"\n"`; (c) the file's LAST blank-line unit equals the GATE_R5
   slice. Then TWO negative controls, in a scratch copy, because (a) and (c) cover
   different regions and neither alone is total — this is the half of last round's
   G2 you correctly reported as unmeetable, now split: flip a byte INSIDE the
   appended paragraph and report that (c) rejects it, and flip a byte inside the
   PRE-IMAGE region and report that (a) rejects it. Finally report that
   `^- R-[0-9]{4} — ` still matches 299 and `^Done: R-[0-9]{4} — ` still matches 4,
   the count of `^Gate: ` headers, and that they are all distinct.

G3 THE PROSE FILES. At C2, `.agent/prose_slips.md` is its pre-image plus exactly
   `"\n"` + SLIP4 + `"\n"` + SLIP5 + `"\n"`, and its pre-image is a byte-exact
   prefix. At C3, `.agent/plan.md` equals the PLANF260R6 slice plus exactly one
   trailing newline; report its line count, which must be under 50.

G4 THE DECISION. At C4, `docs/roadmap/features/T2_F260.md` reconstructs BYTE-EXACTLY
   from its 22955-byte pre-image with the single D4PAIR substitution applied and no
   other change. Report the new byte length. Because the pair is a REWRITE, report
   also the §4.9 counts over the whole file: D4PAIR_FROM 1x before and 0x after,
   D4PAIR_TO 0x before and 1x after. Report that `^### DECISION F260 D` matches five
   times with D0, D1, D2, D3 and D4 each appearing exactly once, and that the file
   still ends with exactly one newline.

G5 THE CODE, READ AND RUN. At C5, all four readings:
   (a) `python3 -m ruff check packages/orchestration/data_paths.py
       packages/orchestration/pingpong_job.py` exits 0;
   (b) with `REMEDY_DATA_DIR` set to a temporary directory, print all four new
       paths and report that `job_record_path(x).parent`,
       `job_evidence_dir(x).parent` and `job_dir(x)` are the same path, and that
       `run_dir(y)` has `runs_dir()` as its parent and `jobs_dir()` nowhere in its
       parents;
   (c) `pingpong_job.job_evidence_dir(x) == data_paths.job_evidence_dir(x)` and
       `pingpong_job._task_stream_dir(x, "t1") == data_paths.job_evidence_dir(x) /
       "task_runs" / "t1"` are both True — the no-behaviour-change property;
   (d) `git diff --numstat 3aaeb042..C5 -- packages/ tests/` reports exactly three
       paths. Report all three rows.

G6 THE MUTATION RED-PROOF (production code — mandatory in full). In a disposable
   worktree at C5, run the UNMUTATED CONTROL FIRST and report its exit code and
   pass count; then break these four PROPERTIES one at a time, restoring between
   each, and report each run's exit code and every failing node id:
   (i) a RUN hangs under `runs_dir` — break it by keying `run_dir` under
       `jobs_dir` instead, the copy-paste this layout invites;
   (ii) the evidence sits BESIDE the record — break it by returning
        `jobs_dir(root) / "evidence" / job_id` from `job_evidence_dir`;
   (iii) the `root` argument is honoured — break it by ignoring `root` in
         `job_dir`;
   (iv) `pingpong_job` no longer spells the evidence path by hand — break it by
        putting the old hand-built expression back in `job_evidence_dir`'s body.
   The control must be GREEN before and after each. Note for (iv): the equality
   reading CANNOT go red, because the hand-built path is equal — only the text
   reading fires, and that is exactly why the block orders both. Report
   `git worktree list` after the removal.

G7 THE SUITES, run SERIALLY in the primary checkout at C5, each exit code recorded
   separately — never through a pipe: `tests/test_data_paths.py`,
   `tests/orchestration/test_checkpoints.py`,
   `tests/orchestration/test_repair_attest.py`,
   `tests/orchestration/test_job_evidence.py`,
   `tests/orchestration/test_mint_call_sites.py`, `tests/test_do_job_flow.py`,
   the docs-round gate `tests/docs/` (this round's change set holds a
   `docs/roadmap/` path, verification tier 5), and the canary
   `tests/cli/test_golden_path.py`. Report each suite's count and exit code.

G8 THE TREE AND THE CHANGE SET. At C5: `git status --porcelain` empty,
   `git ls-files .remedy-wt` empty, `.agent/STOP` absent, and `git worktree list`
   holds no worktree this round created. `git diff --name-only 3aaeb042..C5` lists
   exactly the nine paths of the change set above other than `.agent/handoff.md`,
   which C6 adds; report the list as the command printed it. Report
   `python3 -m apps.cli.grouped integrity check --json` with its `passed` and
   `fail_count`.

## Handback

Rewrite `.agent/handoff.md` in C6 per docs/agents/handback_template.md: feature
and round, `SESSION 2 of feature F260`, branch, the per-commit SHAs with each
commit's insertion count from `git diff --numstat` (the `+` column), the
changed-files table, ONE LINE PER GATE G1 to G8 with its real exit code, the
open-findings count, the item-status table, and the next expected action. It has
no length cap. Declare every deviation, including any place this block is wrong.

<<<BEGIN PLANF260R6>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 5 are reviewed; 2, 3, 4 and 5 PASSED. T001
is CLOSED: the inventory, DECISION F260 D1 and D2, the three minting functions
and their four call sites are all on disk.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Open T002 with the LAYOUT, ruling first why the resolver is not in T001.
DECISION F260 D4 records that measurement. Then `data_paths` gains the one
spelling of DECISION F260 D1's layout — `job_dir`, `job_record_path`,
`job_evidence_dir` and `run_dir` — and `pingpong_job`'s two hand-built evidence
paths are built from it. Nothing moves on disk yet: the paths are the target
spelling every T002 writer will use.

## Next Steps

- The four remaining hand-built evidence paths — `job_evidence.py` twice,
  `repair_attest.py` and `do_cmd.py` — onto `data_paths.job_evidence_dir`, with
  a guard that no module outside `data_paths` spells that path again.
- The unified Job record and its writer under `jobs/<16hex>/job.json`, which
  moves `_persist_job` off `task_jobs/` and DELETES `pingpong_job._jobs_dir`.
  Finding R-0814 is resolved there, against the fix clause it already carries.
- The ONE resolver, in the same round group as that writer, because 40 of the
  42 job-taking call sites take a `UUID` today (DECISION F260 D4).
- Then `runs/<run_id>/`, T003 consumer by consumer, T004 the classic runner,
  T005 the reachability test and the cluster deletion, in that order.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer, or a run
  log becomes unreadable between two commits.
- `job_record_path` names a path nothing writes yet. Its docstring says so and
  T002's writer round is what makes it live.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLANF260R6>>>

<<<BEGIN D4PAIR_FROM>>>
Nothing is deleted before this paragraph is drafted.

## Design
<<<END D4PAIR_FROM>>>

<<<BEGIN D4PAIR_TO>>>
Nothing is deleted before this paragraph is drafted.

### DECISION F260 D4 (2026-09-06, F260 round 6) — the one resolver lands with the store it resolves over, not before it
T001 orders the one minting/resolving function AND that every job-taking command
"resolve through it while both stores still exist". The minting half is done
(rounds 4 and 5). The resolving half cannot be done in T001, and the reviewer
measured why at `3aaeb042` before ruling it:

- `resolve_job_id` (`data_paths.py:222`) returns a `UUID` and has forty call sites
  across nine `apps/cli/commands/` modules. Every one of them feeds
  `storage.load_job(job_id: UUID, ...)` (`storage.py:83`) or `load_job_safe`
  (`storage.py:100`). A `str`-returning resolver cannot replace it until that
  loader reads the unified record, which is what T002 builds.
- `resolve_any_job_id` (`data_paths.py:250`) returns `str` and has exactly two call
  sites, both in `apps/cli/commands/teach_cmd.py`.
- The ping-pong record is found ONLY by `data_paths._task_job_id_matches`
  (`data_paths.py:195`), which globs `<data_root>/task_jobs/`. Moving that record
  to D1's `jobs/<16hex>/` before the resolver moves would make every ping-pong job
  unresolvable and break `remedy teach narrate` — the exact regression
  `resolve_any_job_id` was written to fix (operator dogfooding, 2026-08-25).

CHOSEN: T001 closes with its minting half. The ONE resolver is built inside T002,
in the same round group as the unified record and its loader, and both
predecessors are deleted in T004 exactly as the feature file already orders.
T001's clause "while both stores still exist" is RETIRED by this ruling: forty of
the forty-two job-taking call sites take a `UUID` today, so that is not a state in
which they can move. This changes no scope and no deliverable — only the round in
which the resolver is written.

ALTERNATIVES CONSIDERED. A third resolver now, over both stores, migrating only
`teach_cmd` — rejected: it leaves THREE resolvers alive at once and hands T004
more to delete, against AGENTS.md "Replacing is deleting", and the good name stays
occupied until T004 either way. Changing `resolve_job_id` in place to return `str`
now — rejected: it forces `storage.load_job`'s signature and forty call sites into
one round, which no 500-insertion commit holds, and T002's record change would
immediately redo the same work.

REVERSE by deleting this paragraph; the resolver then returns to T001 and the
feature file's original T001 sentence binds again unamended.

## Design
<<<END D4PAIR_TO>>>

<<<BEGIN GATE_R5>>>
Gate: R5 — the F260 R5 entry. R5 FINISHED T001'S MINTING HALF AT THE CALL SITES: THE FOUR INLINE `uuid4().hex[:16]` MINTS THAT NAME A JOB, A RUN OR AN EPISODE NOW GO THROUGH THE FUNCTIONS ROUND 4 SHIPPED. VERDICT PASS. Range c5da84cb..3aaeb042, six commits, all single-parent, pushed to `origin/feature/f260-one-world`, no pull request created; the largest commit is 299 insertions, well under the AGENTS.md 500-insertion cap. THE REVIEWER RE-RAN ALL EIGHT GATES ITSELF rather than reading the handback's numbers. TRANSPORT: one digest `277b68dd70a61a529e4a2db37d1e1e6f5e6ed6821f1ccdd3aa8266aa4d9c59ee` across the reviewer's scratch original, the worker's saved copy at `.agent/authored/f260-r5.md` and the mirror at `.agent/last_block.md`; per §3 item 37 that chain covers those three artefacts and is NOT a claim about the bytes emitted into the worker's prompt. THE RECORD: `.agent/live_review.md` went 877435 to 881955 bytes, growth 4520 equal to the appended length exactly, the appended bytes being `"\n"` + a 4518-byte slice + `"\n"`; the pre-image is a byte-exact PREFIX, the last blank-line unit equals the slice, registrations stayed 299 and the `Done:` count stayed 4, and there are now fourteen `Gate:` headers, all distinct, with `Gate: R4 — the F260 R4 entry.` occurring exactly once. THE SHIPPED CODE WAS RUN, NOT READ: at `3aaeb042` the reviewer read `JobPlan.__dataclass_fields__["job_id"].default_factory is data_paths.mint_job_id` as True and the same for `PingPongResult`'s `run_id` against `mint_run_id` — OBJECT IDENTITY, which no look-alike lambda satisfies — and parsed both modules to zero `ast.Name` nodes named `uuid4`. `ruff check` over both modules exits 0. NOTHING ELSE MOVED: `git diff --numstat` over the range reports `pingpong_job.py` at 9/4, `pingpong_loop.py` at 3/2 and the new `tests/orchestration/test_mint_call_sites.py` at 95/0, and the whole range's path set is the eight files the block named. The five function-scoped `data_paths` imports in `pingpong_job.py` are untouched, and no other `uuid4().hex[:16]` site — promotion, package, session, plan, quarantine, advisor-run, test-run — moved, which is what DECISION F260 D2's scope requires. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY: in a disposable worktree at `40fd11fd`, module resolving from `.remedy-wt/rev-r5/packages/orchestration/pingpong_job.py` so no install shadowed it, the unmutated control is exit 0 at 5 passed, and each of the three ordered properties turns the guard RED — wrapping the job-id default in `lambda: mint_job_id()` fails `tests/orchestration/test_mint_call_sites.py::TestMintCallSites::test_job_plan_job_id_default_is_the_mint_function_itself`, the same wrapper on `run_id` fails its own identity test, and reverting one episode site to an inline mint fails the AST test — with the control green again after each restore. THE LOOK-ALIKE LAMBDA IS THE POINT: it produces correct 16-hex ids and passes every behavioural test in the repository, so identity is the only reading that sees it, and the block ordered identity for exactly that reason. THE SUITES, re-run serially by the reviewer, all exit 0 at 5, 28, 173, 178, 10, 93 and 42 — 529 tests — and `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks at handlers=342. THE WORKER CORRECTED THE REVIEWER TWICE AND BOTH CORRECTIONS ARE UPHELD. Its deviation 1 caught the block's slice-boundary wording as ambiguous about the trailing newline, measured the R3 precedent to settle it — that paragraph is 4143 bytes with its trailing newline and 4142 without, against a recorded growth of 4144 — and applied the convention that reading implies; the reviewer's own pre-emission arithmetic had assumed the same convention and the two agree exactly at 4520, so the ambiguity cost nothing on disk and the round-6 block states the rule outright. Its deviation 2 is the better catch: G2(c) ordered a byte flipped inside the last appended unit to be REJECTED BY BOTH reading (a) and reading (c), and reading (a) is a prefix comparison over the 877435-byte pre-image while the flip lies entirely AFTER it, so (a) can never reject it — the gate demanded a result no honest run could produce. The worker reported the true asymmetry and ran the companion control the clause was reaching for, a flip inside the pre-image region, which does make (a) reject. The reviewer reproduced both readings and confirms the asymmetry: this is a reviewer-authored gate defect over an `.agent/` prose file, so under operator amendment amend0827-process-diet rule 2 it is a dated line in `.agent/prose_slips.md` and spends no R-id, and the round-6 block splits the control into the two regions it should always have named. Its deviation 3 records that ruff's `I001` forced the D2 rationale comment in `pingpong_loop.py` off the import and onto the `run_id` field, which is a better home for it anyway; deviation 4 records that it caught itself about to write the handback commit's own SHA as a predicted value and amended the unpushed commit rather than shipping an unmeasured digit — the §3 rule against an unmeasured SHA, applied by the worker to itself.
<<<END GATE_R5>>>

<<<BEGIN SLIP4>>>
2026-09-06 · F260 R5 (reviewer) · The round-5 delegation wrapper defined an authored slice as "everything strictly between those two marker lines" without saying which side of the boundary the final newline falls on, and the block's C1 then ordered the append as `"\n"` + the slice + `"\n"`. Read literally the two sentences disagree by one byte, and applying the literal reading would have left `.agent/live_review.md` ending in two newlines, contradicting the block's own statement that the file ends with a single newline and making the last-blank-line-unit reading unsatisfiable. The worker measured the R3 precedent to settle it — 4143 bytes with the trailing newline, 4142 without, against the growth of 4144 the R4 record states — and applied the convention that arithmetic implies. It landed on exactly the bytes the reviewer's own pre-emission measurement had assumed, so the two agree at 4520 and nothing on disk is wrong. THE LESSON: a boundary is a fact about bytes, and a wrapper that describes one in prose has stated a measurement without measuring it. The round-6 block states the rule outright — the slice excludes the newline that ends its last content line — rather than leaving it to be derived from a precedent. Reviewer-authored ambiguity in a delegation wrapper; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP4>>>

<<<BEGIN SLIP5>>>
2026-09-06 · F260 R5 (reviewer) · Gate G2(c) of the round-5 block ordered a negative control that no honest run could satisfy: it required a byte flipped inside the LAST appended blank-line unit to be rejected by BOTH reading (a) and reading (c), where reading (a) compares the first 877435 bytes of the new file against the pre-image. The flipped byte lies entirely after that region, so reading (a) cannot see it and can never reject it. The worker reported the true asymmetry rather than a convenient number, and additionally ran the companion control the clause was plainly reaching for — a flip inside the pre-image region, which does make (a) reject — so the round lost nothing. The reviewer reproduced both readings independently and confirms the asymmetry exactly. THE LESSON: §3 item 36 requires a multi-paragraph append's negative control to sit on the FIRST appended paragraph, and at N=1 that paragraph is also the last, which is what made a single control look sufficient; but the two readings cover DIFFERENT REGIONS — a prefix comparison and a tail comparison — so no single flip can exercise both, and a control has to be written per reading rather than per paragraph. The round-6 block splits it into two controls, one per region, and says which region each is for. Reviewer-authored unmeetable gate half over an `.agent/` prose file, declared by the worker and measured by the reviewer; nothing under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result; no R-id spent (amend0827-process-diet rule 2).
<<<END SLIP5>>>
