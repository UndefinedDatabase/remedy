── STEP T001 (part 4) — F260 ─────────────────────────────────
Goal:        Move the four inline id mints that name a JOB, a RUN or an EPISODE
             onto the functions round 4 shipped, so DECISION F260 D2's "one
             minting function per kind" is true of the call sites and not only
             of `data_paths`. Second production-code round of this feature.
Bundle:      C0a save this block · C0b mirror it · C1 the record (the R4 gate
             entry) · C2 the plan · C3 the four call sites, both import blocks
             and the new guard test · C4 the handback
(§3 item 37: the STEP line above is 62 characters ending in a run of U+2500,
 and the rule line below is 62 copies of U+2500 and nothing else)
──────────────────────────────────────────────────────────────

## Where this round starts

Continuing on `feature/f260-one-world` at `c5da84cb`, already pushed. Do NOT
create a branch, do NOT merge, do NOT open a pull request: the Open PR Gate ran
at session start and found no open pull request, and this branch's own pull
request belongs to the closure sequence.

Round 4 PASSED. The reviewer re-ran every gate itself, ran the three shipped
functions 1000 times each in a disposable worktree, and reproduced the mutation
red-proof independently. That verdict is carried in `.agent/handoff.md` at
`c5da84cb` and is booked into the record by C1 below — operator amendment
amend0827-process-diet rule 1, the first commit of the next round that is
happening anyway. This round is NOT a bookkeeping round: C3 is production code.

Checklist item 23 is not triggered here — C1 registers no finding, resolves
none and renumbers none, it appends a gate record — so amend0827 rule 1 fixes
C1 as the first substantive commit and the plan follows at C2.

This is a SPLIT round over production code (planner_reviewer_prompt.md §3,
Round types). The code in C3 is DESCRIBED, not supplied as a byte slice: you
write it, in the repository's own idiom, and the gates prove it.

## Change set — nothing outside this list

    .agent/authored/f260-r5.md                      (new, C0a)
    .agent/last_block.md                            (C0b)
    .agent/live_review.md                           (C1)
    .agent/plan.md                                  (C2)
    packages/orchestration/pingpong_job.py          (C3)
    packages/orchestration/pingpong_loop.py         (C3)
    tests/orchestration/test_mint_call_sites.py     (new, C3)
    .agent/handoff.md                               (C4)

`.remedy-wt/` scratch stays untracked; `git ls-files .remedy-wt` returns nothing.

## C0a / C0b — save and mirror

The block is at `.remedy-wt/f260-r5-block.md`; the delegating prompt states its
sha256 (BLOCK_SHA — a file cannot carry its own digest). COPY it to
`.agent/authored/f260-r5.md` with `shutil.copyfile`, commit alone; copy the same
bytes to `.agent/last_block.md`, commit alone. Do not retype either.

## C1 — the record

APPEND to `.agent/live_review.md`, in one commit of its own, exactly the bytes
`"\n"` + the GATE_R4 slice + `"\n"`. Nothing in the file before the append
changes by one byte. The file is 877435 bytes at `c5da84cb` and ends with a
single newline.

## C2 — the plan

REPLACE `.agent/plan.md` entirely with the PLANF260R5 slice plus one trailing
newline. Commit alone.

## C3 — what to build

Four call sites mint an id inline with `uuid4().hex[:16]` and each of them names
one of the three KINDS DECISION F260 D2 rules. They move onto the shipped
functions. What the reviewer read at `c5da84cb`, so you are not reading it cold:

    packages/orchestration/pingpong_job.py:290
        job_id: str = field(default_factory=lambda: uuid4().hex[:16])   → mint_job_id
    packages/orchestration/pingpong_job.py:2268   (the F018 pre-budget allocation)
        job.active_episode_id = uuid4().hex[:16]                        → mint_episode_id
    packages/orchestration/pingpong_job.py:2291   (the F012 real-episode allocation)
        job.active_episode_id = uuid4().hex[:16]                        → mint_episode_id
    packages/orchestration/pingpong_loop.py:122
        run_id: str = field(default_factory=lambda: uuid4().hex[:16])   → mint_run_id

Re-grep each site before editing: these are line numbers read at `c5da84cb` and
a symbol survives an edit above it where a number does not (§3 item 9). The
enclosing symbols are `JobPlan`, `run_job` (both episode sites) and
`PingPongResult`.

SCOPE. Many other `uuid4().hex[:16]` sites live under `packages/orchestration/`
— promotion, package, session, plan, quarantine, advisor-run, test-run ids and
more. They name OTHER kinds of thing and DECISION F260 D2 does not reach them.
Touch none of them. `safe_points.new_request_id` is the fourth ruled kind and
stays where the stop request lives.

A DATACLASS DEFAULT TAKES THE FUNCTION, NOT A LAMBDA. `field(default_factory=
mint_job_id)` — the mint functions are argument-free precisely so this works, and
a `lambda: mint_job_id()` wrapper would pass every behavioural test while
defeating the identity guard C3's test uses. Same for `run_id`.

THE IMPORTS. Four readings the reviewer took at `c5da84cb`, because each one
changes what you must write:

  (a) `uuid4` is used at exactly three places in `pingpong_job.py` and at exactly
      ONE place in `pingpong_loop.py` — the sites above and nothing else. After
      this change both modules stop using it, so `from uuid import uuid4` must be
      REMOVED from both or ruff reports an unused import. Verify the count
      yourself before removing.
  (b) `packages/orchestration/data_paths.py` has ZERO module-level imports of any
      `packages.` module — the reviewer listed them by AST at `c5da84cb`: only
      `__future__`, `os`, `re`, `sys`, `pathlib` and `uuid`. Its one
      `packages.orchestration.config` import is inside `resolve_data_root`. So a
      module-level import of `data_paths` into either module CANNOT create a
      cycle, and the reviewer confirmed both modules still import by running them.
  (c) The import MUST be module-level, not function-scoped. `pingpong_job.py`
      currently imports `data_paths` only inside function bodies (five places),
      but a `field(default_factory=...)` is evaluated when the class body runs,
      so a function-local import cannot reach it. Leave those five existing local
      imports exactly as they are — they are out of this change set.
  (d) `pingpong_job.py` today has NO module-level `packages.` import outside its
      `if TYPE_CHECKING:` block, so the new import starts a first-party block and
      ruff's `I001` requires a BLANK LINE between the stdlib block and it. The
      reviewer hit exactly this in its own dry run. `pingpong_loop.py` already has
      a first-party block; `data_paths` sorts between `artifact_summary` and
      `exec_guard`.

THE GUARD TEST — new file `tests/orchestration/test_mint_call_sites.py`. It exists
because this refactor changes no behaviour: a site that drifts back to an inline
mint still produces a correct-looking 16-hex id, so nothing goes red on its own.
The readers it needs, and why each is the shape it is:

  * the two dataclass defaults are pinned by OBJECT IDENTITY —
    `SomeClass.__dataclass_fields__["<field>"].default_factory is
    data_paths.mint_job_id` — which runs the shipped function and, unlike any
    text check, is NOT satisfied by a look-alike lambda that calls it;
  * the two `active_episode_id` assignments are inside a function body, where no
    object exists to compare, so they are read by parsing the module. Parse
    `Path(pingpong_job.__file__).read_text(...)` rather than a path spelled in the
    test, so the test reads the module that was actually imported and still works
    inside a disposable worktree — the pattern
    `tests/orchestration/test_pingpong_job_hunk_ledger.py` already uses;
  * a fourth test asserts neither module still NAMES `uuid4`, as `ast.Name` nodes
    and never as a substring: a docstring or comment that DISCUSSES `uuid4` is not
    a call site, and a guard that cannot tell the two apart forbids the prose.

Give the episode test a non-vacuity assertion — a walk that found nothing would
make its real assertion trivially true. Write the tests in the repository's own
idiom: a module docstring saying why the file exists, one class, and the one-line
WHY comment above anything a reader would otherwise have to reconstruct.

## Constraints

1. Apply every authored slice BYTE FOR BYTE. If a slice looks wrong, apply it
   anyway and say so in the handback's deviations — do not repair it.
2. Nothing outside the change set above is created, edited or deleted. In
   particular no other `uuid4().hex[:16]` site moves, and the five existing
   function-scoped `data_paths` imports in `pingpong_job.py` stay as they are.
3. Commit order is C0a, C0b, C1, C2, C3, C4, each its own commit. C3 is ONE
   commit: the sources and the test that guards them land together, because a
   test-only commit would be red and a source-only commit would be unguarded.
4. Every destructive check — every mutation of G5 — runs ONLY inside a disposable
   `git worktree` under `.remedy-wt/`, never in the primary checkout
   (self_drive_protocol.md G5). Remove it with `git worktree remove --force`
   before C4, and never `git checkout --` a mutated primary file to undo one.
5. Purge `__pycache__` or run `python3 -B` for every mutation run: a stale cached
   module is how a mutation silently fails to reach the test.
6. Gates G1 through G8 are all run AT C3, before C4 is written, so the handback
   can quote each one's real exit code (§3 item 31). The handback commit's own
   numbers are not owed by anyone: the reviewer measures the branch tip itself.
7. `git status --porcelain` is empty at C4. Re-read `.agent/STOP` from disk before
   C3; if it exists, finish the commit in hand, write the handback and stop.
8. Push after C4: `git push origin feature/f260-one-world`. Never force-push.

## Done when — eight gates, each run and its real exit code recorded

G1 TRANSPORT (one digest). `sha256sum` over `.remedy-wt/f260-r5-block.md`,
   `.agent/authored/f260-r5.md` and `.agent/last_block.md` returns ONE value, and
   it equals BLOCK_SHA from the delegating prompt. Report the digest.

G2 THE RECORD. At C1: `.agent/live_review.md` grew from 877435 bytes to a new
   length; report both, and report that the growth equals the appended byte count
   exactly. Prove all four: (a) the 877435-byte pre-image is a byte-exact PREFIX
   of the new file; (b) the remainder is exactly `"\n"` + the GATE_R4 slice +
   `"\n"`; (c) the file's LAST blank-line-separated unit equals the GATE_R4 slice,
   and as a NEGATIVE CONTROL flip one byte inside that unit in a scratch copy and
   report that both (a) and (c) then REJECT it — the slice is one paragraph, so
   this is §3 item 36 at N=1; (d) `^- R-[0-9]{4} — ` still matches 299 and
   `^Done: R-[0-9]{4} — ` still matches 4, which is right because this round
   registers and resolves nothing. Report the count of `^Gate: ` headers and that
   they are all distinct.

G3 THE PLAN. At C2, `.agent/plan.md` equals the PLANF260R5 slice plus exactly one
   trailing newline — one byte-equality reading, nothing more. Report its line
   count, which must be under 50 (AGENTS.md).

G4 THE CODE, READ AND RUN. At C3, all five readings:
   (a) `python3 -m ruff check packages/orchestration/pingpong_job.py
       packages/orchestration/pingpong_loop.py` exits 0;
   (b) parsing each module, the number of `ast.Name` nodes with `id == "uuid4"`
       is 0 in both;
   (c) `packages.orchestration.pingpong_job.JobPlan.__dataclass_fields__["job_id"]
       .default_factory is packages.orchestration.data_paths.mint_job_id` is True,
       and the same holds for `PingPongResult`'s `run_id` against `mint_run_id`;
   (d) parsing `pingpong_job.py`, every `Assign` whose target is an attribute named
       `active_episode_id` has a value that is a call to the name
       `mint_episode_id`, and there are 2 such assignments;
   (e) `git diff --numstat c5da84cb..C3 -- packages/` reports two paths and no
       more. Report both rows.

G5 THE MUTATION RED-PROOF (production code — mandatory in full). In a disposable
   worktree at C3, run the UNMUTATED CONTROL FIRST and report its exit code and
   pass count; then, one at a time, restoring between each, break these three
   PROPERTIES and report each run's exit code and the failing node id:
   (i) the job-id default is the mint function ITSELF — break it by wrapping it in
       a lambda that calls the same function, which is the drift the identity
       reading exists to catch;
   (ii) the run-id default, the same way;
   (iii) one episode site mints through `mint_episode_id` — break it by putting an
       inline `uuid4().hex[:16]` back at that one site.
   Each mutation must turn `tests/orchestration/test_mint_call_sites.py` RED, and
   the control must be GREEN before and after each. Report `git worktree list`
   after the removal.

G6 THE SUITES, run SERIALLY in the primary checkout at C3, each exit code
   recorded separately — never through a pipe, which reports the pipe's status:
   `tests/orchestration/test_mint_call_sites.py`, `tests/test_data_paths.py`,
   `tests/orchestration/test_pingpong_cli.py`, `tests/test_do_job_flow.py`,
   `tests/orchestration/test_pingpong_job_hunk_ledger.py`,
   `tests/orchestration/test_job_evidence.py`, and the canary
   `tests/cli/test_golden_path.py`. Report each suite's count and exit code.

G7 THE TREE. At C3: `git status --porcelain` empty, `git ls-files .remedy-wt`
   empty, `.agent/STOP` absent, and `git worktree list` holds no worktree this
   round created. Also report `python3 -m apps.cli.grouped integrity check --json`
   with its `passed` and `fail_count` values.

G8 THE CHANGE SET. `git diff --name-only c5da84cb..C3` lists exactly the seven
   paths of the change set above other than `.agent/handoff.md`, which C4 adds.
   Report the list as the command printed it.

## Handback

Rewrite `.agent/handoff.md` in C4 per docs/agents/handback_template.md: feature
and round, `SESSION 2 of feature F260`, branch, the per-commit SHAs with each
commit's insertion count from `git diff --numstat` (the `+` column — not a line
count of the file), the changed-files table, ONE LINE PER GATE G1 to G8 carrying
its real exit code, the open-findings count, the item-status table, and the next
expected action. It has no length cap. Declare every deviation, including any
place this block is wrong — the reviewer would rather read a correction than a
silent repair.

<<<BEGIN PLANF260R5>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, the merge commit of
pull request 240 (F259). Rounds 1 to 4 are reviewed; 2, 3 and 4 PASSED. T001's
inventory is on disk, DECISION F260 D1 and D2 are ruled, and the three minting
functions ship in `packages/orchestration/data_paths.py`.

## Goal

One job model on disk. The classic store `<data_root>/jobs/<uuid>.json` and the
ping-pong store `<data_root>/task_jobs/<16hex>/job.json` become one record with
one id shape minted by one function per kind; a Run becomes the evidence case a
Job points at; `resolve_any_job_id`, the "TWO job stores" paragraph and every
which-store branch are deleted. Task slicing per T2_F260.md: T001 inventory and
id shape, T002 records and writers, T003 consumers, T004 the classic runner,
T005 the reachability test and the cluster deletion.

## Current Step

Finish T001's minting half at the CALL SITES. The four inline `uuid4().hex[:16]`
mints that name a job, a run or an episode move onto the shipped functions:
`JobPlan.job_id` and both `active_episode_id` assignments in `pingpong_job.py`,
and `PingPongResult.run_id` in `pingpong_loop.py`. Both modules stop naming
`uuid4` at all. A new guard test pins the two dataclass defaults by OBJECT
IDENTITY, which a look-alike lambda cannot satisfy, and parses the module for
the two episode sites, which have no object to compare.

## Next Steps

- The ONE resolver D2 rules, replacing `resolve_job_id` and `resolve_any_job_id`,
  written while both stores still exist and deleted from its predecessors only in
  T004.
- T002: the extended Mission record, the unified Job record under
  `jobs/<16hex>/` with its evidence beside it, and `runs/<run_id>/` keyed by run
  id. Finding R-0814 is fixed there, because that layout removes the split root.
- T003 consumer by consumer, T004 the classic runner, T005 the reachability test
  and the cluster deletion, in that order.

## Risks

- D1 changes what `<data_root>/runs/` is keyed by, from job id to run id. Every
  reader of the old shape must move in the same commit as its writer, or a run
  log becomes unreadable between two commits.
- The T005 cluster deletion is large and reversible in one direction only. It
  runs last, behind a reachability test green BEFORE the first `git rm`.
<<<END PLANF260R5>>>

<<<BEGIN GATE_R4>>>
Gate: R4 — the F260 R4 entry. R4 WAS THE FIRST PRODUCTION-CODE ROUND OF THIS FEATURE: THE THREE ID-MINTING FUNCTIONS DECISION F260 D2 RULES, THEIR TESTS, AND A MUTATION RED-PROOF. VERDICT PASS. Range 599b3df0..fc36ab21, seven commits, all single-parent, pushed to `origin/feature/f260-one-world`, no pull request created; the largest commit is 308 insertions, well under the AGENTS.md 500-insertion cap, which DECISION F104 D1 reads as the `+` column only. THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback's numbers. TRANSPORT: one digest `ab4c1b77b317bd7dc6a4bcb6ad45c68cb3eecb48ea5362a1803b0105c7d06ca0` across the reviewer's scratch original, the worker's saved copy at `.agent/authored/f260-r4.md` and the mirror at `.agent/last_block.md`; per §3 item 37 that chain covers those three artefacts, all of them the worker's or the reviewer's own files, and it is NOT a claim about the bytes emitted into the worker's prompt. THE RECORD: `.agent/live_review.md` went 873291 to 877435 bytes, growth 4144 equal to the appended length exactly; the pre-image is a byte-exact PREFIX and the remainder is `"\n" + GATE_R3 + "\n"`; registrations stayed 299 and the `Done:` count stayed 4, which is correct because round 4 registered and resolved nothing; thirteen `Gate:` headers, all distinct. THE SHIPPED CODE WAS RUN, NOT READ: in a disposable worktree at `fc36ab21` the reviewer imported the three functions and called each 1000 times, and the returned lengths form the set {16} exactly, 1000 of 1000 values are distinct per function, every character across all 3000 values is lowercase hex, every value matches `data_paths._SHORT_HEX_RE`, and `uuid.UUID(mint_job_id())` raises `ValueError: badly formed hexadecimal UUID string` — the probe D2 rests on. The three names are three DISTINCT function objects with distinct `__qualname__`s, so D2's "one shape is not one function" clause is satisfied by the objects and not merely by the source. `resolve_job_id` and `resolve_any_job_id` both still import and are unchanged, which is what T004 needs to still be true. NO INSTALL SHADOWED THAT WORKTREE: the imported module resolved from `.remedy-wt/rev-r4/packages/orchestration/data_paths.py`, so those readings and the red-proof below describe the branch's own bytes and not an editable install's. THE MUTATION RED-PROOF REPRODUCES INDEPENDENTLY: in that worktree the unmutated control is exit 0 at 28 passed, and changing `[:16]` to `[:32]` inside the body of `mint_job_id` ONLY — verified by grep, the other two bodies untouched — gives exit 1 at 2 failed and 26 passed, at the node ids `tests/test_data_paths.py::TestMintIds::test_each_mints_sixteen_lowercase_hex_chars` and `tests/test_data_paths.py::TestMintIds::test_a_minted_job_id_is_not_a_uuid`. The second failure is the valuable one: widening the slice to 32 hex makes the value a VALID UUID hex, so `UUID()` accepts it and the test that pins D2's own premise fires. The worktree was discarded with `git worktree remove --force` rather than reverted, and the primary checkout satisfies `git status --porcelain` empty. THE SUITES, re-run serially by the reviewer, all exit 0: `tests/test_data_paths.py` at 28 — 23 before, plus exactly the 5 tests the new class adds — `tests/docs/` at 303, `test_roadmap_index.py` at 30, `tests/ui_server/` at 515, `test_test_runner.py` at 52, `test_resource_safety.py` at 21, `test_integrity_gate.py` at 16, and the canary `tests/cli/test_golden_path.py` at 42; `integrity check --json` returned `"passed": true` with `"fail_count": 0` over 5 checks at handlers=342. THE CODE IS IDIOMATIC AND SCOPED: three separate `def`s between `control_dir` and `_SHORT_HEX_RE`, one D2 rationale comment above the group, a first-line docstring per function naming WHAT KIND of thing the id names, `uuid4` added to the existing `from uuid import UUID` line with `UUID` retained, and the module docstring's `Public API::` block extended; nothing else in the file moved. THE WORKER'S DEVIATION 2 IS UPHELD, and it is a fair criticism of the reviewer's block: gate G4 ordered the mutation into the BODY of `mint_job_id`, which forced three literal function bodies and foreclosed the shared private helper the same block's C4 text had explicitly permitted. The outcome is correct and D2's intent is met, but that gate CONSTRAINED the implementation rather than MEASURING it, and a later block ordering a red-proof names the PROPERTY to break and never the line — which is how G5 of the round-5 block is written.
<<<END GATE_R4>>>
