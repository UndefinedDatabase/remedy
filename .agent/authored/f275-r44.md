── STEP T003 / F275 — ROUND 44 — forty construction keywords that do nothing, and the guard ──

Goal:
  A dry run of the flip, applied in a disposable worktree at `c0e9dd10` and RUN, stopped on
  a defect that has nothing to do with the flip and everything to do with the tree it runs
  over. FORTY keyword arguments passed to `Job(...)` and `Task(...)` name no field on either
  model. pydantic v2 defaults to `extra="ignore"`, so every one of them constructs happily
  and is DROPPED, and forty call sites have therefore never done what they say. This round
  removes them, repoints the five that plainly meant `user_prompt`, and lands a guard so the
  class cannot return silently. It registers the defect as R-0875 and records DECISION F275
  D25, which also carries the two mechanical rules the dry run had to learn before the flip
  can be written at all.

  FOUR OF THE FORTY ALSO BLOCK THE FLIP, which is how they were found:
  `Task(title=..., description=...)` becomes `TaskEntry(title=..., title=...)` once
  `description` maps onto `title`, and that does not compile. The flip cannot be authored
  over a tree holding them.

Bundle:
  C0a  save this block verbatim as `.agent/authored/f275-r44.md`
  C0b  mirror that file into `.agent/last_block.md`
  C1   the plan — slice PLAN44, whole-file replacement
  C2   the record — slices RECORD44, REG44 and DECISION44, three appends
  C3   the cleanup AND the guard, in ONE commit, plus slice LANDED44
  C4   the handback

Change: exactly these paths and nothing else.
  .agent/authored/f275-r44.md                      (new, C0a)
  .agent/last_block.md                             (C0b)
  .agent/plan.md                                   (C1)
  .agent/live_review.md                            (C2 and again C3)
  .agent/decisions.md                              (C2)
  tests/test_model_construction_keywords.py        (new, C3)
  the 24 test files the sweep names                (C3)
  .agent/handoff.md                                (C4)

WHY THE CLEANUP AND THE GUARD ARE ONE COMMIT, measured and not preferred. The guard is a
source sweep, so against the UNCLEANED tree it fails with all forty offenders: the reviewer
ran it there and read `1 failed, 4 passed` at exit 1. Landing the guard first would leave
the branch RED at a commit boundary, and landing it second would leave one commit in which
the cleanup is unguarded. One commit is the only ordering with neither property.

THE FORTY, measured by `ast` over the files `git ls-files '*.py'` names, at `c0e9dd10`.
Every one is in a TEST file and not one is in production.

  `Job(permissions=...)`   6 sites  `Job` has no `permissions` field of any spelling
  `Job(prompt=...)`        5 sites  `Job` has `user_prompt`; `prompt` is the near miss
  `Task(task_type=...)`   17 sites  `Task` has no task-type field at all
  `Task(type=...)`         8 sites  the same intent, spelled shorter
  `Task(title=...)`        4 sites  `Task` has `description`; these four ALSO pass it

SPECIFICATION — THE CHANGE IS DESCRIBED, NOT SLICED, except the guard, which is slice
GUARD44 and is applied byte for byte. Write the rest under AGENTS.md's Mandatory Self-Review
Loop.

  S1  DELETE, from every `Job(...)` and `Task(...)` call in the tracked tree, each keyword
      argument whose name is not a field the model declares — with ONE exception, S2. Read
      the declared set by IMPORTING `packages.core.models.Job` and `...Task` and reading
      `model_fields`; never from a list you keep. Delete the whole `name=value` span and the
      comma that joins it to its neighbour, leaving the call's remaining arguments and its
      formatting otherwise untouched. The expected total is 35 deletions: the six
      `permissions`, the seventeen `task_type`, the eight `type` and the four `title`.
  S2  REPOINT, never delete, the five `Job(prompt=...)` keywords: the field they meant is
      `user_prompt`, which `Job` declares, so rename the keyword and keep its value. This
      CHANGES behaviour — the job now carries the prompt the test always believed it carried
      — and it is ordered because the reviewer ran it: with the repoint applied the 24
      touched files read `1083 passed, 10 skipped` at exit 0.
  S3  APPLY THE EDITS IN BYTES. `ast` reports `col_offset` as a UTF-8 BYTE offset while
      Python string slicing counts CHARACTERS, and this repository writes `—`, `…` and `✅`
      into its strings, so a site to the RIGHT of one on the same line has a column that
      character slicing cannot use. The dry run sliced by character first and left
      `packages/orchestration/trust_report.py` unparsable. Encode the line, edit, decode.
      Then re-parse every file you wrote and refuse to keep an edit that made one
      unparsable.
  S4  The guard is slice GUARD44, applied byte for byte to the new file
      `tests/test_model_construction_keywords.py`. Do not reformat it and do not add to it.

Constraints:
  1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Extract each one MECHANICALLY by its
     `BEGIN-`/`END-` marker lines from the COMMITTED `.agent/authored/f275-r44.md`, read
     with `git cat-file blob`, and apply it by file write or byte concatenation in Python.
     Never retype a slice, never reflow one, and never edit one even where you believe it
     wrong — declare it instead. A marker line is never part of a slice's content.
  2. AN EOF-APPEND IS PURE CONCATENATION. Each append slice's content already begins with
     the blank line that separates it from what precedes it, so the operation is exactly
     `old_bytes + slice_bytes` with nothing inserted between them. Every target named in C2
     and C3 ends with a newline at the commit you append to; do not add one.
  3. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and nothing is reordered, merged or
     added. C1 precedes C2 because the plan must be current before the round touches the
     finding ledger (planner_reviewer_prompt.md §3 item 23), and C2 precedes C3 because a
     finding persists BEFORE its fix (§4 item 4).
  4. THE FINDING IS REGISTERED, NOT RESOLVED, BY THIS ROUND. C2 appends REG44, which
     registers `R-0875`. C3 appends LANDED44, a `Landed:` line and nothing else — the
     worker never writes a `Done:` paragraph, because only the reviewer's authored text sets
     Resolved (§4 item 4), and a surviving `Landed:` line is exactly what an unreviewed fix
     should look like. The open set is 86 at this base and 87 from C2 onward.
  5. THE CHANGE SET IS the paths the Change list names. The 24 test files are whatever S1
     and S2 actually reach — report the list you touched — and NO path under `packages/`,
     `apps/`, `docs/` or `scripts/` moves. If S1 reaches a production file, STOP and
     declare it: the reviewer measured zero and a production hit means the two measurements
     disagree.
  6. NEVER `cd` INTO A WORKTREE, for any purpose. Address a worktree's files by ABSOLUTE
     path, run commands there with `subprocess.run([...], cwd=<abs worktree>)`, run
     `git status --porcelain` in the PRIMARY checkout in the same command sequence as any
     mutation, and revert with a sha256 re-read. Remove and prune before the handback.
  7. RUN `python3 -m pytest`, never bare `pytest`. The `remedy` console script is
     sandbox-blocked; if a CLI reading is needed use `python3 -m apps.cli.grouped`.
  8. THIS BLOCK IS CAPPED AT 490 LINES TOTAL AND 400 LINES OF PROSE, where PROSE is TOTAL
     minus the summed content lines of every slice and the marker lines count as prose
     (DECISION F085 D6 and D5). Measure BOTH from the committed blob, report both, and say
     plainly if either is exceeded. Do not fix an overage — declare it.
  9. READ `.agent/STOP` FROM DISK before the first commit and again before C3.

Done when: seven gates. Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the
real exit code and the real numbers — one line per gate. Every reading is taken at a commit
EARLIER than C4.

  G1  TRANSPORT, at C0b. `.agent/authored/f275-r44.md` and `.agent/last_block.md` have the
      SAME sha256 and byte count, and the mirror was written from
      `git cat-file blob <C0a>:.agent/authored/f275-r44.md`. Report both digests. This
      covers the two committed artefacts and claims nothing about the bytes emitted into
      your prompt (planner_reviewer_prompt.md §3 item 37).
  G2  THE PLAN, at C1. `.agent/plan.md` is BYTE-EQUAL to PLAN44 as extracted; report bytes,
      sha256, line count against the AGENTS.md cap of 50, and `^## Goal$` and
      `^## Next Steps$` each exactly 1.
  G3  THE RECORD, for the three appends at C2 (pre C1, post C2) and the one at C3 (pre C2,
      post C3), against COMMITTED blobs read with `git show <rev>:<path>`.
      (a) Reader A: the post blob EQUALS the pre blob followed by the slice. Report pre,
          slice and post bytes and whether the reconstruction is identical.
      (b) Reader B: count N as the blank-line-separated paragraphs IN THE SLICE — count it,
          do not take a number from this block — and compare the LAST N paragraphs of the
          post blob against the slice's N IN ORDER, WITH LEADING AND TRAILING WHITESPACE
          STRIPPED. Constraint 2 puts the separating blank line inside the slice, so a raw
          comparison reads FALSE on correct bytes; round 42 measured that and declared it.
      (c) One negative control per append: flip ONE byte inside the FIRST appended paragraph
          and confirm BOTH readers REJECT it. Report four outcomes per append.
      (d) `^Gate: F275 R43 ` 0 at C1 and 1 at C2. `^- R-0875 — ` 0 at C1 and 1 at C2.
          `^## DECISION F275 D25 ` 0 at C1 and 1 at C2. `^Landed: R-0875 ` 0 at C2 and 1 at
          C3. `^Done: R-0875 ` 0 at C3 — this round resolves nothing.
      Where a formula here and the ORDERED OPERATION disagree, the operation wins and you
      declare the disagreement.
  G4  THE OPEN SET. By DISTINCT ID: distinct `^- R-\d+ — ` minus distinct
      `^Done: R-\d+ — `, read from `git show <rev>:.agent/live_review.md` into memory and
      never by writing over the tracked file. Report at the base `c0e9dd10`, at C2 and at
      C3, plus the ids registered and resolved this round. Expect 86, then 87, then 87;
      registered exactly `['R-0875']`; resolved `[]`.
  G5  THE CLEANUP IS COMPLETE AND BEHAVIOUR-PRESERVING, at C3.
      (a) Re-run the S1 sweep at C3 and report the number of remaining undeclared-keyword
          sites. It must be ZERO, and report the number you DELETED and the number you
          REPOINTED separately — the reviewer measured 35 and 5.
      (b) `python3 -m pytest <every test file this round changed, including the new guard> -q`
          and report the figure. The reviewer read `1083 passed, 10 skipped` at exit 0 over
          the 24 changed files before the guard existed.
      (c) `python3 -m pytest tests/cli/test_golden_path.py -q` — the canary.
      (d) `python3 -m ruff check` over every file this round changed.
      (e) The premise, through the SHIPPED class: in one `python3 -c`, construct
          `Task(description="d", type="x")`, print whether the instance has a `type`
          attribute and what `model_extra` reads, and print the file `packages.core.models`
          was imported FROM.
  G6  THE GUARD BITES — RED PROOF, at C3, in a DISPOSABLE worktree detached at C3 under
      constraint 6, `__pycache__` purged before every run, every run under `python3 -B`,
      the selection scoped to `tests/test_model_construction_keywords.py`. Print the
      imported module's file path before believing any result. Run the UNMUTATED control
      FIRST, then the mutation, then the control again after the revert. The mutation: put
      ONE deleted keyword back — `type="write_readme"` into the `Task(...)` call in
      `tests/ui_server/test_command_channel.py` — counting the anchor before you apply it
      (it must read 1). Report the real exit code and WHICH NODE IDS FAILED, read from the
      `FAILED ` lines where the node id is the token after the FIRST space, never inferred
      from the exit code. DO NOT REPORT A PREDICTED COUNT. A mutation that stays GREEN is
      the honest answer to declare: it would mean the guard does not reach the line.
      Report the revert's sha256 against the pristine digest.
  G7  NOTHING ELSE MOVED, at C3. `.agent/STOP` read FROM DISK is ABSENT.
      `git status --porcelain` is EMPTY. `git worktree list` reads exactly ONE entry.
      Report `git diff --name-only c0e9dd10..<C3>` in full, state that every path is one
      the Change list allows, and report ZERO paths under `packages/`, `apps/`, `docs/` or
      `scripts/`. Report each commit's INSERTION count for C0a, C0b, C1, C2 and C3 against
      the AGENTS.md DECISION F104 D1 cap of 500; C4's own numbers are not ordered here,
      because its text cannot count itself.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md with its mandated
sections — the state block carrying the SESSION NUMBER, the range, a per-commit
changed-files table with a reason per path, external actions, one line per gate with its
REAL exit code and real numbers, the item-status table, the open-findings count, and your
deviations. This is SESSION 18 of F275 and round 44; F275 stands at 44 rounds against the
operator's soft limit of 60 rounds and 20 sessions (amend0908-f275-finish rule 1), so no
scope report is owed. Add the one sentence of context self-assessment amend0905-throughput
requires. State the measured TOTAL and PROSE counts constraint 8 orders. Then push the
branch. Create no pull request, merge nothing, force-push nothing, rewrite no history.

--- BEGIN SLICE PLAN44 ---
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

ROUND 44 clears the tree the flip has to run over. A dry run of the flip found FORTY keyword
arguments passed to `Job(...)` and `Task(...)` that name no field on either model: pydantic
drops them silently, so forty test call sites have never done what they say, and four of them
make the flip's own rewrite produce `TaskEntry(title=..., title=...)`, which does not compile.
This round deletes 35, repoints the 5 that meant `user_prompt`, lands a source guard so the
class cannot return, and registers R-0875. DECISION F275 D25 carries the ruling and the two
mechanical rules the dry run had to learn: edits at `ast` columns are BYTE offsets, and the
flip must rewrite an import's MODULE PATH and not only the name it imports.

## Next Steps

1. THE FLIP, now that its target API exists (round 42), its record shapes are measured
   (round 43) and its tree is clean (this round). The dry run at `c0e9dd10` measured it at
   284 files and 4856 insertions once construction keywords are included, against DECISION
   F275 D21's 3771 changed lines — it is DECLARED at what the round itself measures, before
   review, as the one oversize commit AGENTS.md permits per feature. It also registers
   `Task.acceptance_checks`'s structured form as a finding naming the feature that owns
   acceptance criteria, per amend0908-f275-finish rule 4.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take, and the dry run's 4856
  insertions is higher than every earlier estimate. The route is unchanged because AGENTS.md
  permits exactly one declared-oversize commit per feature and every alternative needs two.
- The open set is 86 by distinct id at this round's base `c0e9dd10` and 87 from C2, where
  R-0875 is registered. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per
  DECISION F272 D12.
--- END SLICE PLAN44 ---

--- BEGIN SLICE RECORD44 ---

Gate: F275 R43 — the F275 round 43 entry. VERDICT PASS, written by the planner and reviewer of session 18 after reading the committed range `7f8724c3`..`cb2032b6` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Booked here by round 44 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, whose durable carrier was the round 43 handback committed at `c0e9dd10`. Six single-parent commits C0a `7cbacbe1`, C0b `d0be7797`, C1 `c04c77c8`, C2 `cdad37b4`, C3 `cb2032b6` and C4 `c0e9dd10`, per-commit insertions 458, 403, 20, 16 and 261 for the five before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500, so F275's one declared-oversize allowance remains unspent. G1 IS AGAIN THE PRIMARY cmp-AGAINST-SCRATCHPAD PROOF AND NOT THE §4.9 DIGEST FALLBACK: the reviewer's scratch original survived, was hashed BEFORE delegation at `8645934b147eae32a7ca600863fb5643fb34f6f2e09532f160fc15f873c209fa`, and is byte-identical to both committed copies at 38161 bytes, which `git rev-parse` resolves to ONE shared blob `b96489bb`; per §3 item 37 that chain covers three on-disk artefacts and claims nothing about bytes emitted into a prompt. G2: `.agent/plan.md` byte-identical to PLAN43 at 2884 bytes, 48 lines against the cap of 50, both mandated headings exactly once. G3 over three appends, each re-derived from the committed C1 blob to the committed C2 blob: `.agent/live_review.md` 860378 to 867326, `.agent/prose_slips.md` 235493 to 236456, `.agent/decisions.md` 1061618 to 1067057; every reader A identical, every reader B true with N counted FROM THE SLICE at 1, 1 and 6, and all three negative controls REJECTED BY BOTH READERS with the flipped byte inside the FIRST appended paragraph, the region §3 item 36 requires; `^Gate: F275 R42 ` and `^## DECISION F275 D24 ` each 0 at C1 and 1 at C2. G4: the open set is 86 BY DISTINCT ID at the base, at C3 and at C4, over 103 registrations against 17 resolutions, none registered and none resolved. G5 IS THE GATE THIS ROUND EXISTS FOR AND IT HOLDS IN ITS STRONGEST FORM: the artefact is MACHINE-GENERATED, and the reviewer ran the committed INSTRUMENT43 slice itself and found its own stdout present VERBATIM in the committed `.agent/f275_t003_record_shapes.md` — so the file is reproducible by a second actor and not merely by its author, which is more than the gate ordered. The instrument slice appears byte-identically in the artefact at sha256 `2e7cbc4d…`, the artefact carries exactly one `## What it printed` heading over 261 lines, and the canary read `42 passed`. G6: the change set is an EXACT set match over seven paths with MISSING and EXTRA both empty, ZERO paths outside `.agent/`, porcelain EMPTY, ONE worktree, `.agent/STOP` absent, and every one of C0a through C3 under the insertion cap. THE MEASUREMENT THIS ROUND EXISTS FOR IS THE ONE THE FLIP NEEDED AND NOBODY HAD TAKEN. The JOB record pair is CLEAN: `Job` declares 15 fields and `JobPlan` 65, they share 13 names, and the only two `Job`-only names are `id` and `name`, the renames this chain has tracked since F272 — so the ORPHAN SET IS EMPTY and DECISION F272 D15's sentence HOLDS for the job record exactly where DECISION F275 D22 disproved it for the task record. There is no third unmeasured record pair. `created_at` is the one shape change beyond the id, at six sites, four production and two test, every one `.isoformat()`; `budget`'s nullability flip has ONE dereference site and it is already guarded. DECISION F275 D25 is recorded. THE WORKER DECLARED NINE DEVIATIONS AND THE REVIEWER SUSTAINS THEM. The second is the one that corrects the reviewer and it does so by testing the BLOCK's claim rather than its own implementation: the worker's paragraph splitter absorbs the slice's leading newline, so reader B read true RAW as well as stripped, and rather than reporting that as agreement it re-ran the NAIVE `split("\n\n")` form the round 42 block's wording implies and reproduced raw-false for all three. The reviewer then ran three splitter forms over all three appends and reads the same: the naive form and a blank-line-run regex both read raw FALSE, and only a form that strips the slice's leading newline first reads raw TRUE. So the round 42 gate was unsatisfiable as worded, the round 43 gate's explicit stripping requirement is the right fix because it makes the reading splitter-INDEPENDENT, and the prose slip booked at C2 states it correctly. The fifth declares four `comm` scratch files left in `/dev/shm`, outside the repository, which `rm` is sandbox-blocked from removing — no tracked path is affected and the reviewer confirms porcelain EMPTY. NO FINDING IS REGISTERED BY THIS GATE AND NONE IS RESOLVED.
--- END SLICE RECORD44 ---

--- BEGIN SLICE REG44 ---

- R-0875 — Medium, FORTY CONSTRUCTION KEYWORDS NAME NO FIELD ON THE MODEL THEY ARE PASSED TO, AND PYDANTIC DROPS THEM SILENTLY. Measured by `ast` over the tracked `.py` files at `c0e9dd10`: `Job(permissions=...)` at 6 sites, `Job(prompt=...)` at 5, `Task(task_type=...)` at 17, `Task(type=...)` at 8 and `Task(title=...)` at 4 — forty in total, every one in a file under `tests/` and not one in production. `packages.core.models.Job` declares none of `permissions` or `prompt`, and `packages.core.models.Task` declares none of `task_type`, `type` or `title`; pydantic v2 defaults to `extra="ignore"`, so `Task(description="d", type="write_readme")` constructs without complaint and the instance has no `type` attribute and a `model_extra` of `None`, measured through the shipped class rather than inferred. The product effect is that forty call sites do not establish the state their own keyword names, so any assertion downstream of one is passing for a reason its author did not write: `Job(prompt=...)` is the clearest, five sites in an authority-integration test that believed they set a prompt and set nothing, where `Job` declares `user_prompt`. The class is invisible at runtime BY CONSTRUCTION, which is why it survived; it surfaced only because the classic-to-unified flip maps `Task.description` onto `TaskEntry.title`, which turns the four `Task(title=..., description=...)` sites into `TaskEntry(title=..., title=...)` and makes two files fail to compile. FIX, binding on the round that resolves this: delete the 35 keywords that name nothing, REPOINT the five `prompt` keywords onto `user_prompt` rather than deleting them, and land a SOURCE sweep as a guard in the same commit — the defect cannot be caught at runtime, so a runtime test would be vacuous, and the guard must read the declared field set by importing the shipped model rather than from a list of its own, which would be a second place a field has to be added.
--- END SLICE REG44 ---

--- BEGIN SLICE LANDED44 ---

Landed: R-0875 — the 35 undeclared keywords deleted, the 5 `Job(prompt=...)` keywords repointed onto `user_prompt`, and `tests/test_model_construction_keywords.py` added as the source guard, all in this round's C3; the reviewer's authored `Done:` is owed at the next gate.
--- END SLICE LANDED44 ---

--- BEGIN SLICE DECISION44 ---

## DECISION F275 D25 (2026-09-10, F275 round 44) — the flip's construction mapping is ruled on evidence, and the two mechanical rules a dry run had to learn before the flip can be written

WHAT THIS SETTLES. DECISION F275 D22 ruled the `Task` to `TaskEntry` pair landed by widening first, and left one question open in its own words: "`Task.description` has TWO candidates on the unified record, `TaskEntry.title` and `TaskEntry.body`, and this decision does not choose between them." Every one of the 247 `Task(...)` constructions passes `description=`, so the flip cannot begin until it is chosen. This decision chooses it, on readings rather than on the shape of the names, and records two mechanical rules the dry run of the flip had to discover by failing.

`Task.description` MAPS ONTO `TaskEntry.title`. Three readings, taken at `c0e9dd10`. FIRST, length: of the 247 construction sites, 186 pass a string literal, and those literals have a median length of 6 characters and a maximum of 28 — not one of the 186 exceeds 80. They are labels: "Fix auth bug", "fix stuff", "some work", "d". SECOND, what the unified record's own parser fills the two fields with: `pingpong_job` builds `TaskEntry(title=planned.title, body=planned.goal, ...)`, so `body` is a task's GOAL and `title` is its label — and `description`'s values are labels. THIRD, who reads it: 43 task-ish `.description` reads, 31 production, in the cockpit detail panel, the run report, the trust report and the task runner, every one rendering a short row rather than a paragraph. `title` is the field those readers want. The 61 non-literal `description=` expressions are not separately ruled: they are whatever the caller computed, and the same mapping carries them.

`Task(type=...)` AND `Task(task_type=...)` MAP ONTO NOTHING IN THIS ROUND. All 25 sites pass a keyword `Task` does not declare, so they have never set anything, and deleting them changes no behaviour — which finding R-0875 registers and this round's C3 performs. `TaskEntry` DOES declare `task_class`, so the intent those 25 sites express becomes expressible for the first time after the flip; restoring it is a deliberate act for the round that owns those tests and is NOT smuggled in here, because a keyword that has never had an effect cannot be "preserved" by giving it one.

THE TWO MECHANICAL RULES, each learned by a dry run that failed and is recorded so the flip round does not rediscover them. FIRST, `ast` REPORTS COLUMNS AS UTF-8 BYTE OFFSETS. A surgical rewrite that slices the line as a Python string therefore mis-edits every site to the RIGHT of a non-ASCII character on that line, and this repository writes `—`, `…` and `✅` into its output strings freely. The dry run's first pass sliced by character and left three files unparsable, `packages/orchestration/trust_report.py` among them, whose line 117 holds three `task.description` reads with a `…` between the first and the second. Encoding the line, editing, and decoding reduced the unparsable count from three to ZERO over 284 rewritten files. SECOND, THE FLIP MUST REWRITE AN IMPORT'S MODULE PATH AND NOT ONLY THE NAME IT IMPORTS. Renaming `Job` to `JobPlan` inside `from packages.core.models import Job` produces an import of a name that module does not have, and the dry run read 74 collection-time `ImportError`s saying exactly that: the unified record lives in `packages.orchestration.pingpong_job`, so the module path moves with the name. Neither rule is a judgement and both are reproducible by re-running the dry run.

HOW TO REVERSE: delete this decision. The `description` mapping then reverts to the open question D22 left, and the flip round owes the three readings again before it can write its first construction rewrite.
--- END SLICE DECISION44 ---

--- BEGIN SLICE GUARD44 ---
"""Every keyword passed to a core model is a field that model declares.

pydantic v2 defaults to ``extra="ignore"``, so ``Task(type="write_readme")`` constructs
happily and DROPS the keyword. A test that writes one believes it set something and did
not. F275 round 44 measured forty such keywords across the suite — `Job(permissions=...)`
and `Job(prompt=...)`, `Task(task_type=...)`, `Task(type=...)` and `Task(title=...)`, every
one in a test file and none in production — and four of them also blocked the
classic-to-unified record flip, because `Task(title=..., description=...)` becomes
``TaskEntry(title=..., title=...)`` once `description` maps onto `title`, which does not
compile.

This guard exists so the class cannot come back silently. It is deliberately a SOURCE sweep
rather than a runtime check: the defect is invisible at runtime by construction, which is
what made it survive.
"""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# The models whose constructions are swept, by the name a caller writes. Each maps to the
# import path that owns it, so the declared-field set is read from the SHIPPED class and
# never from a list kept here — a list would be the second place a field has to be added.
SWEPT_MODELS = {
    "Job": ("packages.core.models", "Job"),
    "Task": ("packages.core.models", "Task"),
}


def _declared_fields(module_path: str, class_name: str) -> set[str]:
    import importlib

    model = getattr(importlib.import_module(module_path), class_name)
    return set(model.model_fields)


def _tracked_python_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.py"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=True,
    ).stdout
    return [line for line in out.split() if line]


def _called_name(node: ast.Call) -> str | None:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _undeclared_keyword_sites() -> list[str]:
    declared = {
        name: _declared_fields(*target) for name, target in SWEPT_MODELS.items()
    }
    offenders: list[str] = []
    for rel in _tracked_python_files():
        try:
            source = (REPO_ROOT / rel).read_bytes()
            tree = ast.parse(source, filename=rel)
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            called = _called_name(node)
            if called not in declared:
                continue
            for keyword in node.keywords:
                if keyword.arg and keyword.arg not in declared[called]:
                    offenders.append(
                        f"{rel}:{node.lineno} {called}({keyword.arg}=...) "
                        f"is not a field of {called}"
                    )
    return sorted(offenders)


class TestEveryConstructionKeywordIsADeclaredField:
    def test_no_tracked_file_passes_an_undeclared_keyword(self) -> None:
        offenders = _undeclared_keyword_sites()
        assert offenders == [], (
            "these constructions pass a keyword the model does not declare, so pydantic "
            "drops it silently and the call does not do what it says:\n  "
            + "\n  ".join(offenders)
        )

    @pytest.mark.parametrize("model_name", sorted(SWEPT_MODELS))
    def test_the_sweep_reads_a_nonempty_field_set_for_each_model(
        self, model_name: str
    ) -> None:
        """A guard over an empty field set would pass by looking at nothing."""
        fields = _declared_fields(*SWEPT_MODELS[model_name])
        assert fields, f"{model_name} declares no fields; the sweep above is vacuous"

    def test_the_sweep_actually_reads_files(self) -> None:
        """And a guard over an empty file list would pass the same way."""
        assert len(_tracked_python_files()) > 500

    def test_an_undeclared_keyword_really_is_dropped_rather_than_rejected(self) -> None:
        """The premise, pinned: this is why the defect is invisible at runtime."""
        from packages.core.models import Task

        task = Task(description="d", type="write_readme")
        assert not hasattr(task, "type")
        assert task.model_extra is None
--- END SLICE GUARD44 ---
