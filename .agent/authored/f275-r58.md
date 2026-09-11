── STEP T003 / round 58 — F275 ────────────────────────────────
Goal:        Record what building DECISION F275 D32's FIRST retype rule family measured,
             rule the task-id half it turned on, and register the defect the run exposed in
             the ruled site set itself. The artefact is the reviewer's dry run, transported
             as a whole file. NO LINE UNDER `packages/`, `apps/`, `tests/`, `docs/` OR
             `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r58.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r58-artefact.md`
             C0c  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN58, whole-file replacement
             C2   `.agent/live_review.md` <- slices RECORD58 then FIND58, both appended
             C3   `.agent/prose_slips.md` <- slice SLIPS58 appended
             C4   `.agent/f275_t003_flip_residue_r58.md` <- a copy of the C0b blob
             C5   `.agent/decisions.md` <- slice DEC58 appended
             C6   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r58.md                NEW
               .agent/authored/f275-r58-artefact.md       NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               .agent/f275_t003_flip_residue_r58.md       NEW
               .agent/decisions.md
               .agent/handoff.md
             The three paths marked NEW do not exist at the base: `git ls-tree bf5ec6a4 --`
             over all three prints nothing, so each is an ADDITION and not a rewrite.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r58.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. The artefact is a WHOLE FILE: copy it with `shutil.copyfile`
     and never open it in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 57 across
     C0a, C0b and C0c and becomes current at C1, which is the first SUBSTANTIVE commit and
     is what item 23 of §3 of `docs/agents/planner_reviewer_prompt.md` requires of a round
     that registers a finding.
  4. This round creates NO `git worktree` and runs nothing destructive.
  5. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  6. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  7. Re-read `.agent/STOP` FROM DISK before the first commit and again before C6, and
     report both readings literally. It does not exist at the reviewer's base reading.
  8. This block is 260 lines TOTAL and 187 PROSE, measured on its final bytes.
  9. EXACTLY ONE finding id is registered this round and none is resolved. The open set is
     87 by distinct id at the base and must read 88 at C5, with `R-0879` the only id added.
     `R-0878` keeps its `Landed:` line and gains no `Done:` here — the reviewer's
     resolution text for it is owed at a later gate and is not part of this round.

Done when:   the seven gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C6.

  G1 TRANSPORT. For each of the two authored blobs, compare the COMMITTED blob against the
     reviewer's scratch original by size and sha256:
       .agent/authored/f275-r58.md          @C0a  vs  .remedy-wt/f275-r58.block.md
       .agent/authored/f275-r58-artefact.md @C0b  vs  .remedy-wt/f275-r58-artefact.md
     Then `.agent/last_block.md` @C0c against the C0a blob. Report all three EQUAL
     verdicts. Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of the
     five slices BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report
     both numerals beside constraint 8's and say whether they agree.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN58: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. Both appends, each proved by TWO readers and a negative control. C2
     appends RECORD58 and then FIND58 into one file in one commit, so treat the two slices
     as one appended region in that order.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed, for each slice in order, by one newline and that slice's body.
            .agent/live_review.md   pre 956303 at the base, RECORD58 7015, FIND58 3369
            .agent/prose_slips.md   pre 250959 at the base, SLIPS58 1099
          Report each pre size, each post size and each delta.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the appended slices' N paragraphs IN ORDER,
          where N is a value your script COUNTS from the slices. Report the N for each.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter inside the FIRST
          appended paragraph and report that BOTH readers reject it.
     (iv) RECORD58 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0. FIND58 must begin with `- R-0879 — ` and carry no second line
          beginning with `- R-`; report both readings. Report also `^Done: R-0878 ` at C2,
          which must be 0, and `^Landed: R-0878 `, which must be 1 and untouched.
     (v)  Report RECORD58's first line beside every line in `.agent/live_review.md` at
          `bf5ec6a4` already matching `^Gate: F275 R5\d — the F275 round \d+ entry\.`, and
          whether the new first line matches that same pattern. Report the number your
          script counted; this block states none.

  G4 THE ARTEFACT IS THE AUTHORED BLOB AND NOTHING ELSE.
     `.agent/f275_t003_flip_residue_r58.md` at C4 must be byte-identical to the
     `.agent/authored/f275-r58-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show bf5ec6a4:.agent/f275_t003_flip_residue_r58.md`, which must be non-zero,
     because that is what makes C4 an ADDITION. Report the artefact's line count against
     the DECISION F104 D1 cap of 500 insertions.

  G5 THE ARTEFACT'S CLAIMS ABOUT THE SHIPPED CODE ARE STILL TRUE AT THIS COMMIT. The
     artefact's section 1 rests on two readings of the repository, and both are cheap to
     re-take. Run, from the repository root:
     (a) `python3 -B -c "from packages.orchestration.data_paths import mint_job_id;
         v = mint_job_id(); print(repr(v), len(v))"` and report its output. The artefact
         states this is the sixteen-hex shape.
     (b) `python3 -B -c "import dataclasses;
         from packages.orchestration.pingpong_job import TaskEntry;
         print([f.type for f in dataclasses.fields(TaskEntry) if f.name == 'task_id'])"`
         and report its output.
     (c) Report the literal lines of `packages/orchestration/pingpong_job.py` that contain
         `Deterministic ID by parse order` and `T001, T002`, with their line numbers. Those
         two comments are the whole basis on which DEC58 rules a task id an ORDINAL, so a
         round that records that ruling reads them rather than citing them.

  G6 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `bf5ec6a4` and at C5, and whether all five are EQUAL.
     (b) THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`. It reads
         42 passed at exit 0 at the base.
     (c) `python3 -m ruff check . --output-format concise`. Its exit code is 1 whenever
         any finding remains, so the GATE IS THE COUNT: report the number of rows matching
         `^\S+:\d+:\d+: `, which is 26 at the base and is the ceiling
         `tests/orchestration/test_ci_budgets.py` freezes. Report rows under `.remedy-wt/`
         separately. Do not use `grep -c` for a count you expect to be zero.

  G7 NOTHING ELSE MOVED.
     (a) Report whether `.agent/STOP` exists on disk, the literal output of
         `git status --porcelain`, and the literal output of `git worktree list`. The
         first must be absent and the second the empty string. The third is REPORTED, not
         gated: state instead whether THIS ROUND created or removed any worktree, which
         constraint 4 fixes at neither.
     (b) The changed-path set over `bf5ec6a4`..C5 must be exactly the Change section's
         paths other than `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `docs/`, `scripts/`, `packages/`,
         `apps/` or `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `bf5ec6a4` and at C5. Report both, the ids registered
         and the ids resolved. Registered must be exactly `R-0879` and resolved must be
         empty. Report the highest id in the record at each end.
     (d) Per-commit insertions from `git show --numstat <sha>` for C0a through C5, each
         against the AGENTS.md DECISION F104 D1 cap of 500, and the maximum over them.
         C6's own numbers are NOT ordered here: they cannot exist while C6 is being
         written, and the reviewer records them at the next gate.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 22 of F275 and
             round 58, the one-sentence context self-assessment amend0905-throughput
             requires, the changed-files table with every `+/-` taken from
             `git show --numstat` and no other source, one line per gate with its REAL
             exit code, the item-status table covering every C and every G exactly once,
             and the authored-text proofs. State the SCOPE REPORT position: F275 stands
             past the soft limit amend0908-f275-finish rule 1 names, the report written in
             round 51's handback STANDS and is not restated, rule 2 forbids the
             split-and-close default BY NAME, and this round closes nothing, registers no
             feature and does not touch `docs/roadmap/STATUS.md`. Carry the operator
             banner exactly as `docs/agents/self_drive_protocol.md` spells it. THIS IS THE
             LAST DELEGATED ROUND OF SESSION 22: say so in the Session section, and state
             that the reviewer's round 58 verdict and the session close are appended to
             this file afterwards, so the next session reads them there. Then push.
──────────────────────────────────────────────────────────────

The three separators in this block carry runs of the box-drawing character U+2500, whose
lengths are stated here because a run of one character has no length a reader recovers by
eye. The STEP line that opens the frame is 63 characters holding 34 of them, in two runs
either side of its text. The rule that closes the frame, directly above this paragraph, is
62 of them and nothing else. The slice rule below is 10, the word SLICES between single
spaces, and 10 more.

────────── SLICES ──────────

BEGIN-PLAN58 sha256=71c3b75fca3fc9d695efa5f1f2ff1a68245abd2c5dd94bb7748827babc6b9cb0
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

ROUND 58 builds the FIRST of DECISION F275 D32's three retype rule families, the id VALUE
at a target construction, and measures it against a control at the same commit. The job
half is the shipped minter; the task half is an ORDINAL, which DECISION F275 D34 rules
after enumerating all fifteen sites. The run also found the defect the round is really
about: the ruled site set is keyed by LINE NUMBER and round 57's own migration drifted 54
of its sites, which is finding `R-0879`. The artefact is
`.agent/f275_t003_flip_residue_r58.md`. The round 57 PASS verdict and one dated prose slip
are booked here.

## Next Steps

1. Re-key the ruled site set off line numbers as DECISION F275 D34 orders, give the
   transform its refuse-on-stale precondition, and re-run the dry run with its control.
2. Resolve the `.status` field by type, in a round of round 53's shape — the descriptor
   probe run twice, unioned with a static sweep — because its 76 sites sit on ten receiver
   names and five of them decide nothing by name. Then D32's remaining rule family.
3. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, registering
   the `acceptance_checks` finding DECISION F275 D22 places with it.
4. The resolver collapse DECISION F260 D5 places in T003, with the classic store, then the
   closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- Re-keying recovers the SITES; no run has yet shown it recovers the residue.
- The residue is classified, not exhausted, and the 42 errors are undiagnosed.
- The open set is 88 by distinct id, with `R-0878` and `R-0879` both awaiting a reviewer
  `Done:`. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION
  F272 D12.
END-PLAN58

BEGIN-RECORD58 sha256=150b317bb549b1069d67f9151cbb42b5bddf688e06a1b18129b1e7653b5ea992
Gate: F275 R57 — the F275 round 57 entry. VERDICT PASS. Written by the planner and reviewer of session 22 after reading the committed range `00b88a2f`..`bf5ec6a4` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. THIS IS THE FIRST ROUND OF THIS SESSION TO MOVE A PRODUCTION LINE, and it moved thirty-five of them across seven modules without one being typed by hand. G1: all three authored blobs are byte-identical to the reviewer's own scratch originals — the block at 27790 bytes and sha256 `48abea6e03bd3d989071e694a3c23373a103ea261952b1bee9313f3ea0b45f62`, the migrator wrapper at 9392 and the ratchet wrapper at 7793 — `.agent/last_block.md` equals the block blob, and all four slices matched the sha256 on their own BEGIN markers. Re-measured on the committed blob the block is 294 lines TOTAL and 235 PROSE, agreeing with its own constraint 9. G2: `.agent/plan.md` byte-identical to PLAN57 at 2659 bytes over 46 lines, both headings exactly once.

G3: three appends, all exact under reader A — `.agent/live_review.md` 949132 to 955452 for RECORD57, `.agent/prose_slips.md` 250044 to 250959 for SLIPS57, and `.agent/live_review.md` again 955452 to 956303 for LANDED57 at C11 — with reader B true at N counted from each slice, 6, 1 and 1, and all three negative controls rejected by BOTH readers. `^Landed: R-0878 ` goes 0 at C10 to 1 at C11 while `^Done: R-0878 ` is 0 at both, which is the append-only record holding an unreviewed fix in exactly the shape §4 item 4 requires: the worker wrote no `Done:` of its own, and the reviewer's is owed at the next gate.

G4 IS THE GATE THIS ROUND EXISTS FOR AND IT PROVES MORE THAN THAT THE EDITS WERE MADE. All seven production files at C11 are byte-identical to the size and sha256 the block STATED IN ADVANCE — `verifier.py` 13383, `long_run_executor.py` 69768, `task_runner.py` 19989, `dag_schedule.py` 7437, `agent_loop.py` 16708, `project_brain.py` 47386 and `workspace.py` 3918 — and those seven values are the ones the REVIEWER's own dry run produced before the block was authored, running the same migrator over a disposable worktree. So the committed tree is byte-for-byte a tree the reviewer had already run the FULL SUITE against at 18386 passed and exit 0, which is a stronger statement than any gate the round itself could make. The landed ratchet equals the C0c fenced body exactly at 7283 bytes, and exactly seven files under `packages/` changed over the range.

G5 AND G6 ARE WHAT MAKE THE SEVEN COMMITS A SEQUENCE RATHER THAN A BATCH. Six of the seven DELETE a now-orphaned `from uuid import UUID`, and a module with a surviving use of that name fails at import and at no earlier point, so each commit's module was imported and the canary run before the next was made: fourteen readings, every one exit 0. G6 is the red-proof, and THE REVIEWER RE-RAN IT IN ITS OWN DISPOSABLE WORKTREE detached at `00b88a2f`: the ratchet reads `2 failed, 5 passed`, the two being exactly `test_no_uuid_typed_job_or_task_id_survives` and `test_no_uuid_only_method_is_read_off_a_job_or_task_id`, while both discriminators, the exemption test and both allowlist tests stay GREEN — which is what distinguishes an absent property from a broken matcher. The worker also proved the worktree imported its own tree rather than the primary checkout, by printing `packages.__path__`, the resolved module path and the live annotation before running; the editable install puts the primary checkout on `sys.path` unconditionally and that is a live route to a false green. The reviewer reproduced the same two-failure reading independently.

G7: the reviewer re-ran the scoped selection itself at `742 passed` exit 0, which is the base's 735 plus the ratchet's 7 and nothing else; `ruff check .` reads 26 finding rows, the frozen ceiling, with 0 in the new file; and `tests/orchestration/test_ci_budgets.py` passes, which is the test that ceiling belongs to and without which the 26 is a number rather than a gate. The full suite was deliberately NOT ordered — verification tier 3 reserves it for the integration gate and closure — and the reviewer's own pre-authoring run over the identical tree stands in its place. G8: the changed-path set over `00b88a2f`..C11 is exactly fifteen paths with MISSING and EXTRA both empty and ZERO under `apps/`, `docs/` or `scripts/`; the open set is 87 by distinct id at both ends with nothing registered and nothing resolved; and per-commit insertions over C0a..C11 are 294, 172, 167, 200, 21, 12, 2, 3, 11, 7, 9, 1, 1, 160 and 2, every one under the AGENTS.md DECISION F104 D1 cap of 500, so F275's one declared-oversize allowance is still UNSPENT at 57 rounds. All sixteen cells of the handback's `## Commits` table match `git show --numstat`.

THE WORKER DECLARED SIX DEVIATIONS AND THE SECOND IS THE REVIEWER'S. G8(b) called the Change section's enumeration "fifteen paths" where it lists SIXTEEN, the sixteenth being `.agent/handoff.md` — a hand-counted numeral beside a list, which is item 16's class and the third time this reviewer has spent one in five rounds. The worker re-derived the set from the block's own text instead of from the numeral, so the substantive reading is exactly right and unaffected: fifteen changed paths, MISSING and EXTRA empty. It is a dated line in `.agent/prose_slips.md`, not an id. The other five are sustained and three of them improve on their order: the plan named round 56 across the block-save commits, which constraint 5 requires and which the worker MEASURED rather than assumed; the seven imports were each run twice, once pre-commit as AGENTS.md's File Editing Safety Rules require and once as G5 orders; a malformed inline probe that wrote nothing was declared anyway, because that shape CAN hide a partial write and the porcelain was read back before proceeding; C12's 711 insertions are the verbatim rewrite of a single `.agent/**` state file, which DECISION F104 D1 exempts entirely and which therefore spends no allowance; and the first `git worktree remove` exited 128 on the untracked ratchet copy the gate itself had placed, which the worker cleared by EXACT PATH and never by glob before removing without `--force`.

WHAT ROUND 57 ACHIEVED. Finding `R-0878` is fixed on disk: the seven records DECISION F275 D26's pydantic-only premise could not see now spell their job and task ids as `str`, the six imports that retype orphaned are gone, and the one behaviour change in the whole migration — `result.task_id.hex[:8]` becoming `str(result.task_id)[:8]` — is correct for a `UUID` today and for a `str` after the flip, which the reviewer measured over 10000 `uuid4()` samples and red-proved as 15 reddened tests. The ratchet that lands with it is the reason this is a migration rather than seven edits: it reads the live class objects, carries its own discriminator, and checks each allowlist entry still matches something, so the eighth such record cannot arrive the way these seven did.
END-RECORD58

BEGIN-FIND58 sha256=e24d6df760b16a0fd7a38d367ace8057567a749df260f32c6c31dcf05837d662
- R-0879 — Medium. THE RULED SITE SET THE FLIP CONSUMES IS KEYED BY LINE NUMBER, SO EVERY LATER COMMIT OF THIS BRANCH SILENTLY UNPICKS PART OF IT — AND ONE ALREADY HAS. Raised by the reviewer at `bf5ec6a4` from a dry run, not from a reading of the artefact. THE DEFECT: `.agent/f275_t003_descriptor_sites.md` records the ruled set R as 2198 sites keyed by `(path, line, col, attr)`, measured at `a815c9a3`, and DECISION F275 D30 rules that set as what the transform consumes. A line number is not an identity. Round 57's migration — ordered by DECISION F275 D33 and correct in itself — deleted six now-orphaned `from uuid import UUID` lines and rewrote thirty-five lines across seven modules under `packages/orchestration/`, so every ruled site BELOW one of those deletions moved and the transform then renamed nothing there. MEASURED, by re-resolving every ruled site against the tree at `bf5ec6a4`: 2144 still resolve, 54 DRIFTED, and all 54 are in five of the seven files round 57 edited — `long_run_executor.py` 21, `task_runner.py` 12, `agent_loop.py` 11, `dag_schedule.py` 7, `verifier.py` 3 — with ZERO drifted anywhere else. THE CONSEQUENCE IS NOT HYPOTHETICAL AND IS THE LARGEST CLASS OF THAT RUN: the flip dry run recorded in `.agent/f275_t003_flip_residue_r58.md` produced 255 attribute-error lines on a `JobPlan` receiver, of which 235 are attributed to a source line inside three of those five files — 109 at `long_run_executor.py:1355`, 65 at `task_runner.py:127` and 53 spread over five lines of `agent_loop.py` — and the `AttributeError` class went from 127 at the previous run to 424. Fifty-four unrenamed reads in code every test exercises is what that costs. WHY NO GATE SAW IT: every gate this chain has run over the site set measured the set's own internal consistency — its counts, its reproducibility across two probe runs, its agreement with a heuristic control — and none of them asked whether its keys still RESOLVE against the tree the transform is about to edit. The set was generated once, three rounds ago, and has been consumed at three different commits since. THE FIX, and it is measured rather than proposed: re-key each site by `(path, enclosing function, attr, occurrence index of that attr within that function)`, a key that carries no line number. Re-keyed at `a815c9a3` and resolved at `bf5ec6a4` it recovers 2198 of 2198 with NONE lost, against the line key's 2144 and 54 on the same two trees — the line key run as the control, which is what makes the first number a reading. THE GUARD THIS NEEDS: the transform REFUSES TO RUN when any ruled site fails to resolve at the commit it is running on, reporting the count and the files; a site set that has gone stale must stop a run rather than quietly edit less of the tree than it says it does. That guard is the whole finding, because the defect is not that a key drifted — keys drift — but that nothing noticed. THE RULE THIS LEAVES BEHIND, and it is item 9 of `docs/agents/planner_reviewer_prompt.md` §3 arriving through a DATA FILE instead of through a block's prose: a `file:line` citation is re-measured against this branch's own edits before it is used, and that binds a generated site set exactly as it binds a sentence in a block — a set of two thousand line numbers is two thousand citations, and it goes stale the same way and more quietly.
END-FIND58

BEGIN-SLIPS58 sha256=79fae069b37f8745559baf04a6695ce336c397d23f3161343f2c596cccebc818
2026-09-11 · F275 R57 · The round 57 block's G8(b) ordered the changed-path set to be "exactly the Change section's fifteen paths minus `.agent/handoff.md`", while that section enumerates SIXTEEN — the sixteenth being `.agent/handoff.md` itself, so the numeral is wrong by one in the clause that then subtracts it. This is item 16 of `docs/agents/planner_reviewer_prompt.md` §3, a hand-counted numeral standing beside a list the reader can count, and it is the third such numeral this reviewer has spent in five rounds. The worker re-derived the set from the block's own enumeration rather than from the numeral and reported fifteen changed paths with MISSING and EXTRA both empty, so the substantive reading is exactly right and nothing on disk is wrong. THE RULE THAT FOLLOWS, and it is narrower than "do not count": where a gate must subtract one named item from a list, it says "the Change section's paths other than `X`" and gives NO cardinality at all — the subtraction is the instruction, the count adds nothing a worker needs, and it is the half that goes stale when a path is added.
END-SLIPS58

BEGIN-DEC58 sha256=36e28e548a250c75cb1ca5529444e9d22c9b1958d997602213597bdba431e15a
## DECISION F275 D34 (2026-09-11, F275 round 58) — a unified task id is an ORDINAL and the mapping is mechanical after all; and the ruled site set is re-keyed off line numbers before the flip consumes it again

CONTEXT. DECISION F275 D32 named three retype rule families and left one question under the first of them that no decision in this chain had asked: what does `Task(id=uuid4())` become? For a JOB the answer was already on disk — `data_paths.mint_job_id()` returns `uuid4().hex[:16]`, the sixteen-hex shape DECISION F260 D2 rules — and this round implemented it at 74 direct sites, 11 through a local bound to `uuid4()`, and 6 by unwrapping a `UUID(x)` coercion, with rule I5 carrying the minter's import exactly as I3 carries the seam's. For a TASK there is no minter at all. `TaskEntry.task_id` is assigned `f"T{parse_idx + 1:03d}"` in `packages/orchestration/pingpong_job.py`, under a comment reading "Deterministic ID by parse order, not heading number", and the field's declaration carries `# T001, T002, ... (by parse order)`. The unified task id is an ORDINAL SCOPED TO ITS JOB. The flip is therefore not retyping a value there; it is replacing an identity with a position.

CHOSEN, PART ONE: THE TASK ORDINAL IS RESOLVED FROM THE CONSTRUCTION'S OWN POSITION, AND THE CLASS IS SMALL ENOUGH TO HAVE BEEN READ IN FULL. All 15 `Task(id=...)` sites were enumerated, 14 in test helper factories and one in production, and every one has exactly ONE such construction in its enclosing function. Twelve sit in a list literal, where the element index IS the position; two sit in a comprehension over `range(task_count)`, where the loop variable is the position; and one is a lone `append` in `packages/orchestration/continue_from_node.py`, which builds a child job holding a single task and is therefore `T001` by construction and not by judgement. The transform resolves all fifteen and reports, rather than guesses, anything it cannot. NOTHING HERE INVENTS A MINTER: a task id that is an ordinal stays an ordinal, and this chain does not add a `mint_task_id` the unified record has no place for.

CHOSEN, PART TWO: THE RULED SITE SET IS RE-KEYED BEFORE IT IS CONSUMED AGAIN, AND THE TRANSFORM REFUSES TO RUN ON A STALE ONE. This is finding `R-0879`. The set is 2198 sites keyed by `(path, line, col, attr)`, measured at `a815c9a3`, and round 57's migration moved 54 of them — all 54 inside the seven files that round edited, none anywhere else. The transform renamed nothing at those 54, and 235 of the run's 255 `JobPlan`-receiver attribute errors are attributed to three of the five affected files. The remedy was measured with its own control: re-keyed by `(path, enclosing function, attr, occurrence index within that function)` the set recovers 2198 of 2198 across the same two trees, where the line key recovers 2144. The transform gains a precondition — every ruled site must RESOLVE at the commit it is running on, or the run stops and names the count and the files — because the defect is not that a key drifted but that nothing noticed for three rounds.

WHY ONLY ONE OF D32'S THREE FAMILIES WAS BUILT. The `.status.value` family is 76 sites over ten receiver names, of which `record` at 18, `latest`, `c`, `held` and `released` decide nothing by name, and `status` was never in the ruled set, which covers `id`, `name` and `description` only. Resolving it by receiver name is the heuristic D29's P1 exists to have killed, so it needs its own descriptor-probe round of exactly round 53's shape. The `.hex`/`.int` family turned out smaller than it looked: round 57 already removed its one production reader and added a ratchet keeping the shape out, and what remains is three test sites the flip rewrites anyway. Building one family properly is worth more than three approximately, and the run this decision rests on could attribute its residue only because the other two did not move.

ALTERNATIVES CONSIDERED. (i) Give a flipped task a fresh unique string rather than its ordinal — rejected: it would put a value in the field that the unified record's own parser never produces, so a reader that assumes ordinals would be wrong in a way no test constructs, which is the class `.agent/f275_t003_descriptor_sites.md` already records as undecidable by execution. (ii) Drop the task id keyword and let `TaskEntry.task_id` default to the empty string — rejected on the measurement: task ids are compared with `==` at 308 sites and used as dict keys at 16, so an empty id collides across every task in a job. (iii) RE-DERIVE the ruled site set at the flip's own base instead of re-keying it — not rejected, and explicitly still open: it costs the two twenty-one-minute probe runs `.agent/f275_t003_descriptor_sites.md` section 3 records, and it is the stronger answer wherever the set must also pick up sites that did not exist when it was measured. Re-keying is what this decision ORDERS because it is cheap, measured, and sufficient for a tree whose edits so far only MOVE sites; the moment a round adds a candidate receiver, re-derivation becomes owed and this clause is the record of that condition. (iv) Pin the site set to a commit and forbid any intervening production commit — rejected as unworkable: D33's migration was correctly ordered between the measurement and its use, and a rule that forbids necessary work to protect a stale artefact protects the wrong thing.

HOW TO REVERSE: delete this decision and `R-0879`'s registration. The task-id half of D32's first rule family then has no ruling and the next dry run reproduces the 54-site drift, at a cost of roughly 235 exception lines it cannot attribute — which is what this round spent two suite runs learning.
END-DEC58
