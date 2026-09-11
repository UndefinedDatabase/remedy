── STEP T003 / round 57 — F275 ────────────────────────────────
Goal:        Perform finding `R-0878`'s fix as DECISION F275 D33 rules it: the seven
             production records that still declare a UUID-typed job or task id are
             retyped to `str`, ONE RECORD PER COMMIT, and the last of the seven brings the
             ratchet that stops an eighth arriving unseen. This round DOES move production
             lines — seven modules under `packages/orchestration/` and one new file under
             `tests/` — and nothing under `apps/`, `docs/` or `scripts/`.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r57.md`
             C0b  save the migrator verbatim as `.agent/authored/f275-r57-migrate.py.md`
             C0c  save the ratchet verbatim as `.agent/authored/f275-r57-ratchet.py.md`
             C0d  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN57, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD57 appended
             C3   `.agent/prose_slips.md` <- slice SLIPS57 appended
             C4   retype `VerificationResult`      (packages/orchestration/verifier.py)
             C5   retype `TaskAttempt`             (packages/orchestration/long_run_executor.py)
             C6   retype `RunTaskResult`           (packages/orchestration/task_runner.py)
             C7   retype `TaskNode`                (packages/orchestration/dag_schedule.py)
             C8   retype `AgentLoopState`          (packages/orchestration/agent_loop.py)
             C9   retype `ProjectBrainGraph`       (packages/orchestration/project_brain.py)
             C10  retype `Workspace` (packages/orchestration/workspace.py) AND add the
                  ratchet at `tests/orchestration/test_uuid_record_ratchet.py`
             C11  `.agent/live_review.md` <- slice LANDED57 appended
             C12  `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r57.md                        NEW
               .agent/authored/f275-r57-migrate.py.md             NEW
               .agent/authored/f275-r57-ratchet.py.md             NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               packages/orchestration/verifier.py
               packages/orchestration/long_run_executor.py
               packages/orchestration/task_runner.py
               packages/orchestration/dag_schedule.py
               packages/orchestration/agent_loop.py
               packages/orchestration/project_brain.py
               packages/orchestration/workspace.py
               tests/orchestration/test_uuid_record_ratchet.py    NEW
               .agent/handoff.md
             The four paths marked NEW do not exist at the base: `git ls-tree 00b88a2f --`
             over all four prints nothing. `.agent/decisions.md` is NOT in this set:
             DECISION F275 D33 already rules this migration and no new decision is owed.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r57.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. The migrator and the ratchet are WHOLE FILES: copy each with
     `shutil.copyfile` and never open either in an editor.
  3. NO PRODUCTION LINE IS EDITED BY HAND. Every one of the seven retype commits is the
     output of running the migrator, extracted from its COMMITTED blob at C0b, once with
     the record's name as its only argument. It applies only edits whose FROM matches the
     target line byte for byte, reports any that miss, writes nothing when any misses and
     exits non-zero. If it reports a miss, STOP, report it, and edit nothing by hand.
  4. The ratchet file is the migrator's counterpart and is likewise NOT retyped: extract
     it from its COMMITTED blob at C0c and copy it to
     `tests/orchestration/test_uuid_record_ratchet.py`.
  5. The commit order above is FIXED. `.agent/plan.md` therefore names round 56 across
     C0a through C0d and becomes current at C1, which is the first SUBSTANTIVE commit.
  6. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
     The ONE `git worktree` this round may create is G6's, and it is removed and pruned
     before C12; report both the creation and the removal.
  7. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  8. Re-read `.agent/STOP` FROM DISK before the first commit and again before C12, and
     report both readings literally. It does not exist at the reviewer's base reading.
  9. This block is 294 lines TOTAL and 235 PROSE, measured on its final bytes.
 10. NO finding id is registered or resolved this round. `R-0878` is marked `Landed:` by
     slice LANDED57 and nothing else; the reviewer's `Done:` is owed at the next gate, per
     §4 item 4 of `docs/agents/planner_reviewer_prompt.md`, which reserves `Done:` for
     reviewer-authored text. The open set is 87 by distinct id at the base and at C11.

Done when:   the eight gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C12.

  G1 TRANSPORT. For each of the three authored blobs, compare the COMMITTED blob against
     the reviewer's scratch original by size and sha256:
       .agent/authored/f275-r57.md            @C0a  vs  .remedy-wt/f275-r57.block.md
       .agent/authored/f275-r57-migrate.py.md @C0b  vs  .remedy-wt/f275-r57-migrate.py.md
       .agent/authored/f275-r57-ratchet.py.md @C0c  vs  .remedy-wt/f275-r57-ratchet.py.md
     Then `.agent/last_block.md` @C0d against the C0a blob. Report all four EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of the four
     slices BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report both
     numerals beside constraint 9's and say whether they agree.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN57: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. Three appends, each proved by TWO readers and a negative control.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline followed by the slice body.
            .agent/live_review.md   pre 949132 at the base, RECORD57 body 6319
            .agent/prose_slips.md   pre 250044 at the base, SLIPS57 body 914
            .agent/live_review.md   again at C11, LANDED57 body 850
          Report each pre size, each post size and each delta.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N it counted for each.
     (iii) NEGATIVE CONTROL, one per append: flip a single ASCII letter inside the FIRST
          appended paragraph and report that BOTH readers reject it.
     (iv) RECORD57 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0. Report the count of `^Landed: R-0878 ` and of `^Done: R-0878 `
          at C10 and at C11: the first must go 0 to 1 and the second must be 0 at both.
     (v)  Report RECORD57's first line beside every line in `.agent/live_review.md` at
          `00b88a2f` already matching `^Gate: F275 R5\d — the F275 round \d+ entry\.`, and
          whether the new first line matches that same pattern. Report the number your
          script counted; this block states none.

  G4 THE SEVEN COMMITS ARE THE MIGRATOR'S OUTPUT AND NOTHING ELSE. Extract the migrator
     from the COMMITTED blob at C0b, taking the lines strictly between the only two lines
     that BEGIN with three backticks — report the two line numbers your script found — and
     report its size and sha256. Report the COMPLETE stdout of each of the seven runs,
     untrimmed, and each REAL exit code, every one of which must be 0. Then report, for
     each of the seven files below, its size and sha256 at the commit that last touched
     it, beside the value this block states. All seven must match.
       packages/orchestration/verifier.py            13383  eeff5eaf14d0ff9adc2d50958ed95730da4c0ef88c99cc724a5be370d7682080
       packages/orchestration/long_run_executor.py   69768  8b28e8717a445cd6c09852bbc0857f1683742f174b236b0fe4769ca182980561
       packages/orchestration/task_runner.py         19989  6a19c4ece88af639fbc770f8ccdfd3d3dda21dcbefb9e01e1711925737331714
       packages/orchestration/dag_schedule.py         7437  205d8b2f46053395126608e0cfe1ed5a6ae705b25a235a875ff0e27f6d1464ed
       packages/orchestration/agent_loop.py          16708  10d5ecfc90a2a6d99cb3968879ad581272f18ea35088ada4e639cacb2e0b3a8c
       packages/orchestration/project_brain.py       47386  22d8cc09a6a0c6efc6918f2901fcdf9b37d3df75ca15d266fdf786570942a672
       packages/orchestration/workspace.py            3918  543e2fddafee875587b13792dd1187c1092ae63d1def22b323eec1b155002716
     Report also `tests/orchestration/test_uuid_record_ratchet.py` at C10 against the
     ratchet BODY extracted from the C0c blob: 7283 bytes, sha256
     `06ac8ca858de114b65582d2a570f2076aed1031b4769e202e2d369489ad8a9e4`. And report the
     total `git diff --numstat 00b88a2f..C10` over `packages/`, which must be 7 files.

  G5 EVERY INTERMEDIATE STATE IS GREEN, NOT ONLY THE LAST. After EACH of the seven retype
     commits, and before making the next, import that commit's module and run the canary:
       C4  `python3 -B -c 'import packages.orchestration.verifier'`
       C5  `python3 -B -c 'import packages.orchestration.long_run_executor'`
       C6  `python3 -B -c 'import packages.orchestration.task_runner'`
       C7  `python3 -B -c 'import packages.orchestration.dag_schedule'`
       C8  `python3 -B -c 'import packages.orchestration.agent_loop'`
       C9  `python3 -B -c 'import packages.orchestration.project_brain'`
       C10 `python3 -B -c 'import packages.orchestration.workspace'`
     and `python3 -m pytest tests/cli/test_golden_path.py -q` after each. Report all
     fourteen REAL exit codes and the canary's summary line each time. The import check is
     there because six of the seven commits DELETE a now-orphaned `from uuid import UUID`,
     and a module with a surviving use of that name would fail at import and at no earlier
     point. It reads 42 passed at exit 0 at the base.

  G6 THE RATCHET IS RED WITHOUT THE MIGRATION AND GREEN WITH IT. Inside ONE disposable
     `git worktree` detached at `00b88a2f`, copy the ratchet body there and run
     `python3 -B -m pytest tests/orchestration/test_uuid_record_ratchet.py -q --tb=line
     -p no:randomly`. Report the REAL exit code, the summary line, and WHICH test ids
     failed. Exactly two must fail — the record test and the read test — and the other
     five must pass, because a red-proof in which the discriminator also fails proves the
     matcher is broken rather than the property absent. Then run the same file in the
     PRIMARY checkout at C10 and report its REAL exit code and summary line. Remove and
     prune that worktree before C12 and report both actions.

  G7 THE SUITE AND THE CEILING, SCOPED. The full suite is NOT ordered here — verification
     tier 3 of `docs/agents/planner_reviewer_prompt.md` §3 reserves it for the integration
     gate and closure, and the reviewer has its own full-suite reading of this change.
     Run at C11:
     (a) `python3 -B -m pytest tests/orchestration/test_dag_schedule.py
         tests/orchestration/test_long_run_executor.py
         tests/orchestration/test_job_task_runner.py
         tests/orchestration/test_project_brain.py tests/test_agent_loop.py
         tests/test_project_brain.py tests/test_task_runner.py tests/test_verifier.py
         tests/test_verifier_profiles.py tests/test_workspace.py
         tests/orchestration/test_uuid_record_ratchet.py -q --tb=line -p no:randomly`.
         This selection is every test file named after one of the seven modules, plus the
         ratchet. It reads 735 passed at the base without the ratchet file.
     (b) `python3 -m ruff check . --output-format concise`. Its exit code is 1 whenever
         any finding remains, so the GATE IS THE COUNT: report the number of rows matching
         `^\S+:\d+:\d+: `, which is 26 at the base and is the ceiling
         `tests/orchestration/test_ci_budgets.py` freezes. Report rows in the new ratchet
         file separately. Do not use `grep -c` for a count you expect to be zero.
     (c) `python3 -B -m pytest tests/orchestration/test_ci_budgets.py -q`, because that is
         the test the ruff ceiling belongs to and (b) is a number without it.

  G8 NOTHING ELSE MOVED.
     (a) Report whether `.agent/STOP` exists on disk, the literal output of
         `git status --porcelain`, and the literal output of `git worktree list`. The
         first must be absent and the second the empty string. State separately which
         worktrees THIS ROUND created and removed, which constraint 6 fixes at exactly
         G6's one.
     (b) The changed-path set over `00b88a2f`..C11 must be exactly the Change section's
         fifteen paths minus `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `apps/`, `docs/` or `scripts/`, which
         must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `00b88a2f` and at C11. Both must read 87. Report the
         ids registered and the ids resolved; both lists must be empty.
     (d) Per-commit insertions from `git show --numstat <sha>` for C0a through C11, each
         against the AGENTS.md DECISION F104 D1 cap of 500, and the maximum over them.
         C12's own numbers are NOT ordered here: they cannot exist while C12 is being
         written, and the reviewer records them at the next gate.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 22 of F275 and
             round 57, the one-sentence context self-assessment amend0905-throughput
             requires, the changed-files table with every `+/-` taken from
             `git show --numstat` and no other source, one line per gate with its REAL
             exit code, the item-status table covering every C and every G exactly once,
             and the authored-text proofs. State the SCOPE REPORT position: F275 stands
             past the soft limit amend0908-f275-finish rule 1 names, the report written in
             round 51's handback STANDS and is not restated, rule 2 forbids the
             split-and-close default BY NAME, and this round closes nothing, registers no
             feature and does not touch `docs/roadmap/STATUS.md`. Carry the operator
             banner exactly as `docs/agents/self_drive_protocol.md` spells it. Then push
             the branch.
──────────────────────────────────────────────────────────────

The three separators in this block carry runs of the box-drawing character U+2500, whose
lengths are stated here because a run of one character has no length a reader recovers by
eye. The STEP line that opens the frame is 63 characters holding 34 of them, in two runs
either side of its text. The rule that closes the frame, directly above this paragraph, is
62 of them and nothing else. The slice rule below is 10, the word SLICES between single
spaces, and 10 more.

────────── SLICES ──────────

BEGIN-PLAN57 sha256=aeff47efe7991a094d74177a5b408577ea303e91e63b8929ce29537a1b90ca2a
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

ROUND 57 performs the migration DECISION F275 D33 rules, which is finding `R-0878`'s fix:
the seven production records that still declare a UUID-typed job or task id are retyped to
`str`, ONE RECORD PER COMMIT, and the last of the seven brings the ratchet that stops an
eighth arriving unseen. The one behaviour change in the whole migration is a single line —
a `.hex[:8]` read becomes `str(...)[:8]`, which is correct before and after the flip. The
round 56 PASS verdict and one dated prose slip are booked here.

## Next Steps

1. Build DECISION F275 D32's three retype rule families — the id VALUE at a target
   construction, a `.hex` or `.int` read on a now-`str` id, and a `.value` read on a
   now-`str` status — and re-run the flip dry run with its control at the same commit.
   The task-id half needs a ruling first: the unified task id is an ORDINAL, not a minted
   identifier, so a `Task(id=uuid4())` site has no mechanical counterpart.
2. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, declared with
   its inseparability reason before review, registering the `acceptance_checks` finding
   DECISION F275 D22 places with it.
3. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- A retype changes an ANNOTATION, which Python does not enforce, so a green suite after
  this round proves the migration harmless and not that every reader was found.
- Three of the seven records are fed only by code the suite never executes.
- The open set is 87 by distinct id, with `R-0878` landed here and its resolution owed at
  the next gate. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per
  DECISION F272 D12.
END-PLAN57

BEGIN-RECORD57 sha256=5367dc8fb654dc5ec8b085242f67e09cbba197e53229e119e76cd9250f73dc79
Gate: F275 R56 — the F275 round 56 entry. VERDICT PASS. Written by the planner and reviewer of session 22 after reading the committed range `62d4bbe7`..`00b88a2f` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. Nine single-parent commits, verified with `git rev-list --parents`. G1 is the PRIMARY cmp-against-scratchpad proof: the block travelled as a FILE the worker verified by size and sha256 before opening, so both authored blobs are byte-identical to the reviewer's own scratch originals — the block at 36176 bytes and sha256 `1ce7f5d8d4fb681c0c7cd101d9458698624bc55cc3092ed6d1592c948d4447a5`, the generator wrapper at 8725 — and `.agent/last_block.md` equals the block blob exactly. All five slices also matched the sha256 on their own BEGIN markers. Re-measured on the committed blob the block is 293 lines TOTAL and 219 PROSE, agreeing with its own constraint 9 and inside both DECISION F085 D6 caps. G2: `.agent/plan.md` byte-identical to PLAN56 at 2574 bytes over 46 lines, both mandated headings exactly once.

G3: `.agent/live_review.md` goes 937538 to 949132 bytes across RECORD56 and FIND56 as one appended region in that order, and `.agent/prose_slips.md` 249127 to 250044, both exact under reader A; reader B holds for both at N counted from the slices, 7 and 1; both negative controls, each flipping one ASCII letter inside the FIRST appended paragraph of its file, are rejected by BOTH readers; RECORD56 carries no interior line that would split it into a second ledger record; FIND56 begins `- R-0878 — ` and carries exactly one such line; and the header matches the five entries above it, a count the block ordered the worker to measure and stated no numeral for.

G4 IS THE GATE THIS ROUND EXISTS FOR AND IT IS STRONGER THAN A DIGEST COMPARISON. `.agent/f275_t003_uuid_records.md` is GENERATED, and the reviewer regenerated it: the generator was extracted from the committed blob at `9faa15d0`, between the only two lines beginning with three backticks — file lines 11 and 190, exactly as the worker reported — giving 8030 bytes, and run TWICE. Both runs and the committed artefact are one blob at 5322 bytes and sha256 `fa302156e7681549…`. THE DESIGN THAT BOUGHT THAT EXACTNESS IS WORTH RECORDING: this generator takes its measurement base as an ARGUMENT instead of reading the repository tip, so a reproduction is exact at any later commit — round 54's generator embedded the tip it ran at, and its reproduction had to be taken before the commit that stored it and still differed in one line of 87. One design change removed a whole class of gate friction. G5: the four header lines read back from the committed artefact, and all seven of the record pairs the block gave as literals hold on both sides, with zero false; the not-fed tag occurs twice and FIND56 names both records it covers. G6: `.agent/decisions.md` goes 1105990 to 1112364 with reader A exact, reader B true at N counted as 8, the control rejected by both, and `^## DECISION F275 D33 ` reading 0 at C4 against 1 at C5.

G7: all five of `packages`, `apps`, `tests`, `docs` and `scripts` are byte-identical trees at the base and at C5, read by the reviewer itself; the canary reads 42 passed at exit 0 and `ruff check .` reads 26 finding rows with 0 under `.remedy-wt/`, the ceiling `tests/orchestration/test_ci_budgets.py` freezes. G8: the changed-path set over `62d4bbe7`..C5 is exactly the eight paths the Change section names with MISSING and EXTRA both empty and ZERO under `docs/`, `scripts/`, `packages/`, `apps/` or `tests/`; the open set goes 86 to 87 by distinct id with `R-0878` the only id registered and none resolved, the highest id moving from `R-0877` to `R-0878`; and per-commit insertions are 293, 190, 163, 20, 14, 2, 103, 16 and 356, every one under the AGENTS.md DECISION F104 D1 cap of 500, so F275's one declared-oversize allowance is still UNSPENT at 56 rounds. Every cell of the handback's `## Commits` table matches `git show --numstat`, and the item-status table covers all nine C items and all eight G items exactly once.

THE WORKER DECLARED FOUR DEVIATIONS AND THE SECOND IS THE REVIEWER'S. G4 ordered the generator RUN TWICE, and the round necessarily runs it THREE times: the artefact has to exist before it can be committed, and the block forbids typing it, so the committing run is a third the gate did not count. The worker ran it three times, said so, and observed correctly that G4's property holds regardless of provenance because the committed artefact and both ordered runs are the same 5322 bytes. Nothing on disk is wrong; it is a dated line in `.agent/prose_slips.md` and not an id, per amend0827-process-diet rule 2. The other three are sustained and each is the round improving on its order: `.agent/plan.md` named round 55 across the block-save commits, which the block's constraint 3 requires and which the worker MEASURED rather than assumed; G3 was re-run after the two readers were factored into one module so that G6 imports the same code instead of a copy, which is a stronger reading of "the same two readers" than the block asked for; and no `grep -c` was used in G7(c), which repairs the round 55 slip where a zero-row reading arrived as a non-zero exit.

WHAT ROUND 56 ACHIEVED, and it is a correction to a premise three decisions rested on. DECISION F275 D26's P2 selected records with `issubclass(obj, BaseModel)`, so it saw six pydantic models and D27 and D28 migrated three, in the belief the class was enumerated. A sweep over the LIVE objects of every class kind reads 328 modules walked with ZERO skipped on import and 13 records carrying a UUID-typed field, EIGHT of them dataclasses, and seven of those are fed by the flip — which is `R-0878`, and which the round 55 dry run had already measured the consequence of without attributing it, at 39 exception lines in `project_brain.py` and 22 in `task_runner.py`. DECISION F275 D33 rules the seven migrated one record per commit BEFORE any of D32's retype rule families is written, with a ratchet as the last of them, because a rule family written against records that are still `UUID` would make the transform's output disagree with the tree it runs on and the next dry run could not tell a rule defect from a record defect.
END-RECORD57

BEGIN-SLIPS57 sha256=d0e06d492bb9a7e26bebd62456c9478b1578fba438d01506979519e41797ff14
2026-09-11 · F275 R56 · The round 56 block's G4 ordered the artefact generator "RUN it twice" and reported the two runs as the reproduction proof, while a round that COMMITS a generated artefact necessarily runs it three times: the artefact has to exist on disk before it can be committed, the same block's constraint forbids typing it, and that committing run is one the gate did not count. The worker ran it three times, declared the third, and observed correctly that the gate's property holds regardless of provenance, since the committed artefact and both ordered runs are one 5322-byte blob. Nothing on disk is wrong. THE RULE THAT FOLLOWS: a gate over a GENERATED artefact counts the run that produced the committed bytes as one of its runs, or says plainly that it is checking reproduction and not provenance — because "run it twice" reads as a total when the round's own first run is invisible to it.
END-SLIPS57

BEGIN-LANDED57 sha256=8bc198773b843055182504b3651b864636a891e6d28c3af30ce2516cd70a04eb
Landed: R-0878 — all seven records retyped to `str`, one per commit in the order `VerificationResult`, `TaskAttempt`, `RunTaskResult`, `TaskNode`, `AgentLoopState`, `ProjectBrainGraph`, `Workspace`, by running the instrument committed at `.agent/authored/f275-r57-migrate.py.md` once per record; the six `UUID` imports that retype orphaned removed with them, `project_brain.py`'s kept because line 582 parses external input; the one behaviour change is `task_runner.py`'s `result.task_id.hex[:8]` becoming `str(result.task_id)[:8]`, correct for a `UUID` today and for a `str` after the flip; and the ratchet `tests/orchestration/test_uuid_record_ratchet.py` added in the last of the seven commits, with its own discriminator and its allowlist entries each checked to still match something. The reviewer's authored `Done:` is owed at the next gate.
END-LANDED57
