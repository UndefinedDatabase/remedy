── STEP T003 / round 55 — F275 ────────────────────────────────
Goal:        Record what the flip dry run measured once all three of DECISION F275 D29's
             prerequisites were implemented, and rule the cause it exposed. The reviewer
             built the transform, ran it against a control at this round's base and
             measured the residue; this round COMMITS that reading and its ruling. NO LINE
             UNDER `packages/`, `apps/`, `tests/`, `docs/` OR `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r55.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r55-artefact.md`
             C0c  save the instrument verbatim as `.agent/authored/f275-r55-instr.py.md`
             C0d  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN55, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD55 appended
             C3   `.agent/prose_slips.md` <- slice SLIPS55 appended
             C4   `.agent/f275_t003_flip_residue_r55.md` <- a copy of the C0b blob
             C5   `.agent/decisions.md` <- slice DEC55 appended
             C6   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r55.md              NEW
               .agent/authored/f275-r55-artefact.md     NEW
               .agent/authored/f275-r55-instr.py.md     NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/prose_slips.md
               .agent/f275_t003_flip_residue_r55.md     NEW
               .agent/decisions.md
               .agent/handoff.md
             The four paths marked NEW do not exist at the base: `git ls-tree 08feacae --`
             over all four prints nothing, so each is an ADDITION and not a rewrite.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character of any of them, including text you believe is
     wrong. A slice you disagree with is applied as written and the disagreement goes in
     the handback's deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r55.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. The artefact and the instrument are WHOLE FILES: copy them
     with `shutil.copyfile` and never open them in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 54 across
     C0a, C0b, C0c and C0d, and becomes current at C1 — declare that, as round 54 did. It
     is the earliest commit at which the plan can be current, because C0a through C0d
     write only this block and the two blobs it transports, and item 23 of §3 of
     `docs/agents/planner_reviewer_prompt.md` requires the plan named and advanced first
     among the SUBSTANTIVE commits, which C1 is.
  4. The instrument is RUN and NEVER EDITED. If it raises, report the traceback verbatim
     and fix nothing in it; a defect in the reviewer's instrument is the reviewer's.
  5. This round creates NO `git worktree` and runs nothing destructive. Do not remove any
     worktree you did not create: the round 54 slip in SLIPS55 rules that a gate over
     `git worktree list` asserts what THIS ROUND created and removed, never the absolute
     contents of a list that also carries the reviewer's scratch.
  6. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  7. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  8. Re-read `.agent/STOP` FROM DISK before the first commit and again before C6, and
     report both readings literally. It does not exist at the reviewer's base reading.
  9. This block is 284 lines TOTAL and 213 PROSE, measured on its final bytes.
 10. No finding id is registered or resolved this round. The open set is 86 by distinct id
     at the base and must read 86 at C5. `TaskEntry.acceptance_checks` is NOT minted here:
     DECISION F275 D22 already places that finding with the FLIP round, and §3 item 30
     forbids a second id for a defect the record already routes.

Done when:   the eight gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C6, which is the
             commit that must quote them.

  G1 TRANSPORT. For each of the three authored blobs, compare the COMMITTED blob against
     the reviewer's scratch original by size and sha256:
       .agent/authored/f275-r55.md          @C0a  vs  .remedy-wt/f275-r55.block.md
       .agent/authored/f275-r55-artefact.md @C0b  vs  .remedy-wt/f275-r55-artefact.md
       .agent/authored/f275-r55-instr.py.md @C0c  vs  .remedy-wt/f275-r55-instr.py.md
     Then `.agent/last_block.md` @C0d against the C0a blob. Report all four EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of the four
     slices BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report
     both numerals beside constraint 9's and say whether they agree.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN55: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. Both appends, each proved by TWO readers and a negative control.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline followed by the slice body, exactly.
            .agent/live_review.md   pre 931514 at the base, RECORD55 body 6023
            .agent/prose_slips.md   pre 246973 at the base, SLIPS55 body 2153
          Report each pre size, each post size and each delta.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N it counted for each file.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter inside the FIRST
          appended paragraph and report that BOTH readers reject it. The first paragraph,
          not the last.
     (iv) RECORD55 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0.
     (v)  Report RECORD55's first line beside every line in `.agent/live_review.md` at
          `08feacae` already matching `^Gate: F275 R5\d — the F275 round \d+ entry\.`, and
          whether the new first line matches that same pattern. Report the number your
          script counted; this block states none.

  G4 THE ARTEFACT IS THE AUTHORED BLOB AND NOTHING ELSE.
     `.agent/f275_t003_flip_residue_r55.md` at C4 must be byte-identical to the
     `.agent/authored/f275-r55-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show 08feacae:.agent/f275_t003_flip_residue_r55.md`, which must be non-zero,
     because that is what makes C4 an ADDITION. Report the artefact's line count against
     the DECISION F104 D1 cap of 500 insertions.

  G5 THE INSTRUMENT RUNS, AND THE ARTEFACT'S CLAIMS RECONCILE AGAINST WHAT IT PRINTS.
     Extract the instrument from the COMMITTED `.agent/authored/f275-r55-instr.py.md` blob
     at C0c, taking the lines strictly between the only two lines that BEGIN with three
     backticks — report the two line numbers your script found — write it under
     `.remedy-wt/`, and report its size and sha256. RUN it from the repository root with
     `python3 -B` and report its REAL exit code and its COMPLETE stdout, untrimmed. Then
     check every one of these fifteen strings is PRESENT in that stdout, and report the
     count of any that are not, which must be 0:
       `job id       classic <class 'uuid.UUID'>`
       `task status  classic <enum 'RunState'>`
       `created at   classic <class 'datetime.datetime'>`
       `JobPlan is a dataclass: True`
       `JobPlan.model_dump       exists: False`
       `JobPlan.model_dump_json  exists: False`
       `JobPlan.model_copy       exists: False`
       `TaskEntry declares acceptance_checks: False`
       `16  Assign -> Dict`
       `11  AnnAssign -> Dict`
       `9  Assign -> dict(...)`
       `sees 16 of 37 binding sites`
       `73  Job.id = uuid4()`
       `6  Job.id = UUID()`
       `tracked .py from git ls-files: 993`
     These fifteen are exactly what the artefact's section 8 claims the instrument
     reproduces. The instrument writes nothing; confirm `git status --porcelain` is the
     empty string immediately after the run.

  G6 THE DECISION. `.agent/decisions.md` pre 1100262 at the base, DEC55 body 5727. Prove
     the append by the same two readers and the same negative control as G3, with N
     counted from the slice and the control inside the FIRST appended paragraph. Then
     report the count of lines matching `^## DECISION F275 D32 ` at C4 and at C5, which
     must be 0 and 1.

  G7 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `08feacae` and at C5, and whether all five are EQUAL. At the base
         they read `ff6cebaf9e41cbcd813399fb022940c47ca7180b`,
         `1dd43398c371aa88e16fa8aba95bead4c131c2ac`,
         `1d425fe0f1a27848b0cec31fce0c92077ce28d12`,
         `48fd2e4c9ffe468071e3e9dbe056db6e4e1dd792` and
         `53331effaa68e4e30ece33a0acd66e077813b2c5`.
     (b) THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`. It reads
         42 passed at exit 0 at the base.
     (c) `python3 -m ruff check . --output-format concise`. Its exit code is 1 whenever
         any finding remains, so the GATE IS THE COUNT: report the number of rows matching
         `^\S+:\d+:\d+: `, which is 26 at the base and is the ceiling
         `tests/orchestration/test_ci_budgets.py` freezes. Report rows under `.remedy-wt/`
         separately; that directory is gitignored, so ruff should see none.

  G8 NOTHING ELSE MOVED.
     (a) Report whether `.agent/STOP` exists on disk, the literal output of
         `git status --porcelain`, and the literal output of `git worktree list`. The
         first must be absent and the second the empty string. The third is REPORTED, not
         gated: state instead whether THIS ROUND created or removed any worktree, which
         constraint 5 fixes at neither.
     (b) The changed-path set over `08feacae`..C5 must be exactly the Change section's ten
         paths minus `.agent/handoff.md`. Report MISSING and EXTRA, both of which must be
         empty, and the count of paths under `docs/`, `scripts/`, `packages/`, `apps/` or
         `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `08feacae` and at C5. Both must read 86. Report the
         ids registered and the ids resolved this round; both lists must be empty.
     (d) Per-commit insertions from `git show --numstat <sha>` for C0a through C5, each
         against the AGENTS.md DECISION F104 D1 cap of 500, and the maximum over them.
         C6's own numbers are NOT ordered here: they cannot exist while C6 is being
         written, and the reviewer records them at the next gate.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 22 of F275 and
             round 55, the one-sentence context self-assessment amend0905-throughput
             requires, the changed-files table with every `+/-` taken from
             `git show --numstat` and no other source, one line per gate with its REAL
             exit code, the item-status table covering every C and every G exactly once,
             and the authored-text proofs. State the SCOPE REPORT position: F275 stands
             past the soft limit amend0908-f275-finish rule 1 names, the report written in
             round 51's handback STANDS and is not restated, rule 2 forbids the
             split-and-close default BY NAME, and this round closes nothing, registers no
             feature and does not touch `docs/roadmap/STATUS.md`. Carry the line
             `SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER UEBERGABE` with the
             umlaut written as the single character it is. Then push the branch.
──────────────────────────────────────────────────────────────

The three separators in this block carry runs of the box-drawing character U+2500, whose
lengths are stated here because a run of one character has no length a reader recovers by
eye. The STEP line that opens the frame is 63 characters holding 34 of them, in two runs
either side of its text. The rule that closes the frame, directly above this paragraph, is
62 of them and nothing else. The slice rule below is 10, the word SLICES between single
spaces, and 10 more.

────────── SLICES ──────────

BEGIN-PLAN55 sha256=efbbc00ba8c52463a51c4da06715ff461f7d71ac1e2744669657468e87437b11
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

ROUND 55 records the flip dry run DECISION F275 D29's CONSEQUENCE clause places after all
three of its prerequisites, now that all three are landed — P1 at round 53, P2 at rounds 51
and 52, P3 at round 54. The transform consumed the ruled site set and the splat rules, the
run was taken against a control at the same commit, and the residue fell from 2557
attributed failures to 1331. The artefact is `.agent/f275_t003_flip_residue_r55.md` and the
ruling is DECISION F275 D32: the flip is a RENAME AND A RETYPE, the two records disagree
about field TYPES, and the classic record cannot hold the unified id shape, so the change
stays one commit and the transform gains the retype rules. The round 54 PASS verdict and its
dated prose slip are booked here.

## Next Steps

1. Build the three retype rule families DECISION F275 D32 names — the id VALUE at a target
   construction, a `.hex` or `.int` read on a now-`str` id, and a `.value` read on a
   now-`str` status — and re-run the dry run with its control at the same commit.
2. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, declared with
   its inseparability reason before review, registering the `acceptance_checks` finding
   DECISION F275 D22 places with it.
3. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- Nothing proves the type table exhausts the cause; only another dry run can say so.
- The ruled site set is line-granular on its probe half, so a line holding two owners is
  resolved by receiver name and one site by nothing at all.
- The open set is 86 by distinct id. Four are High — R-0803, R-0804, R-0806 and R-0807 — all
  F273's, per DECISION F272 D12.
END-PLAN55

BEGIN-RECORD55 sha256=a6137fade82abf106fe158301847ae4ca077323eab1d62ab218094f1d31bddac
Gate: F275 R54 — the F275 round 54 entry. VERDICT PASS. Written by the planner and reviewer of session 21 after reading the committed range `7e2e92e3`..`fc749c9b` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. Carried across the session boundary in the pushed `.agent/handoff.md` at `08feacae` as operator amendment amend0827-process-diet rule 1 permits, and booked here by the first substantive commit of round 55. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: both authored blobs are byte-identical to the reviewer's own scratch originals, the block at 26668 bytes and sha256 `01c7b9b78013b00caadf39e8af7c1fd41519e52a5ac517554d0ae4638e9b9024` and the instrument wrapper at 16078 bytes, and `.agent/last_block.md` equals the C0a blob exactly. Re-measured on the committed blob the block is 246 lines TOTAL and 172 PROSE, inside both DECISION F085 D6 caps and matching its own constraint 9. G2: `.agent/plan.md` byte-identical to slice PLAN54 at 2524 bytes over 45 lines, both mandated headings exactly once. G3: `.agent/live_review.md` goes 926541 to 931514 bytes and `.agent/prose_slips.md` 243843 to 246973, both exact under reader A; reader B holds for BOTH files at N counted from the slices, 5 and 4; BOTH negative controls, each flipping one ASCII letter inside the FIRST appended paragraph of its file, are rejected by BOTH readers; RECORD54 carries no interior line that would split it into a second ledger record; and its header matches the entries above it.

G4 THROUGH G6 WERE RE-DERIVED BY REGENERATING THE ARTEFACT FROM THE COMMITTED INSTRUMENT, which is a stronger reading than re-running the gates. The reviewer extracted the instrument from the committed blob of `.agent/authored/f275-r54-splat.py.md`, confirmed it byte-identical to its own scratch original, and ran it. The output differs from the committed `.agent/f275_t003_splat_sites.md` in EXACTLY ONE LINE of 87 — the measurement-base line, which names `903bf6ba` in the committed artefact because C4 generated it at C3's tip and `fc749c9b` in the reviewer's regeneration because the reviewer ran it at the branch tip — and is byte-identical everywhere else, including every bucket line, every key disposition and both halves of rule I4's call-graph pass. The count of the literal string `UNRULED` in the committed artefact is ZERO, which is the reading DECISION F275 D31 turns on. G7: all five of `packages`, `apps`, `tests`, `docs` and `scripts` are byte-identical trees at the base and at C5, which is how a round claiming to move no production line proves it rather than asserting it; the canary reads 42 passed at exit 0 and `ruff check .` reads 26 finding rows, the ceiling `tests/orchestration/test_ci_budgets.py` freezes.

G8 IS RED AS WRITTEN AND THE FAULT IS THE REVIEWER'S, NOT THE ROUND'S. Clause (a) required `git worktree list` to hold the primary checkout alone, and it held three entries: the primary plus `.remedy-wt/v53-wt-a` and `.remedy-wt/v53-wt-b`, both created by the REVIEWER while verifying round 53 and both still present when round 54 began. `docs/agents/planner_reviewer_prompt.md` §4 item 10 requires the reviewer's throwaway worktrees removed and pruned BEFORE the verdict, and they were not. The worker declined to remove them, correctly and on two grounds it stated: the removal is destructive and the block ordered it nowhere, and the paths sit outside the round's change set. That refusal is the round behaving exactly as it should when a reviewer's gate contradicts a reviewer's constraint. The reviewer removed both worktrees after the verdict was derived. Clauses (b), (c) and (d) hold on the reviewer's own reading: nine changed paths, every one under `.agent/`, MISSING and EXTRA both empty; the open set is 86 by distinct id at both ends with nothing registered and nothing resolved; and per-commit insertions are 246, 343, 176, 20, 10, 8, 87, 14 and 415, every one under the AGENTS.md DECISION F104 D1 cap of 500, so F275's one declared-oversize allowance is STILL UNSPENT at 54 rounds. The underlying property clause (a) exists to protect — this round created no worktree and left the primary checkout clean — holds and was measured; what failed is the reviewer's own housekeeping, which is why this is a PASS with a dated slip rather than a FAIL.

THE WORKER DECLARED FIVE DEVIATIONS AND TWO MORE OF THEM ARE ALSO THE REVIEWER'S. G3(v) named "the two" ledger headers where three match at `7e2e92e3`; the worker applied the gate as written and reported all three, which is the same hand-counted-numeral-beside-a-measured-category class as round 53's header-line slip, one round later and under the rule written to stop it. The remaining three are sustained and are not defects: `.agent/plan.md` described round 53 across the block-save commits, which the block's own fixed order requires; both instrument runs were taken at the identical tip before C4, which buys an exact byte equality instead of a one-line exemption and is better than what the gate asked for; and the worker's own probe script raised once and was fixed by the worker, while the reviewer's instrument was run and never edited and raised nothing.

WHAT ROUND 54 ACHIEVED, and it is the last of DECISION F275 D29's three prerequisites. P3, the `**` splat class, was resolved by CONSTRUCTING both records rather than by reading either: `Job` is a pydantic model whose `extra` is left at its default and so ACCEPTS `permissions=` and `description=` while storing nothing, and `JobPlan` is a dataclass that raises `TypeError` naming the keyword on the same input. DECISION F275 D31 rules every resolved key into renamed, carried or dropped, on both halves rule I4 names, and the count of keys left unruled is ZERO. Round 55's dry run then measured that ruling's REACH, and found it silent about three binding shapes it does not model — the round 55 entry carries that reading, and it takes nothing away from this one.
END-RECORD55

BEGIN-SLIPS55 sha256=a52b451ec8b0c28156a38caeaa196401571191b38b78dc250928b63966be97e1
2026-09-11 · F275 R54 · The round 54 block's G8(a) required `git worktree list` to hold the primary checkout alone, and it held three entries: the two disposable worktrees the REVIEWER created while verifying round 53 and never removed, contrary to `docs/agents/planner_reviewer_prompt.md` §4 item 10, which requires them removed and pruned before the verdict. The gate was therefore unmeetable by any correct round, and the worker was right to report it red as written and to refuse the removal as destructive, unordered and outside its change set. Nothing on disk is wrong and the property the clause protects — the round created no worktree and left the primary checkout clean — was measured and holds; the reviewer removed both worktrees after deriving the verdict. THE RULE THAT FOLLOWS: a gate over `git worktree list` asserts what THIS ROUND created and removed, never the absolute contents of the list, because that list also carries the reviewer's own verification scratch and a round cannot be held to the state of a window it does not control.

2026-09-11 · F275 R54 · The session 21 handoff told the next session that the flip transform "does not exist as committed source anywhere, only as rules spread across DECISIONs", and concluded from that reading that round 55 had to rebuild it and therefore needed a whole session's budget to itself — which is the reason that handoff gives for ending session 21 at two delegated rounds, below the four-round floor. The first clause is true and the conclusion does not follow: `.remedy-wt/r46_flip_transform.py` was on disk throughout, gitignored rather than absent, and round 50 had already re-run it unchanged and said so in `.agent/f275_t003_flip_residue_r50.md` section 3. Session 22 reused it and spent its effort on the two rules D29 actually ordered. Nothing on disk was wrong and no round was lost, but a session boundary was bought on a premise one `ls` would have corrected. THE RULE THAT FOLLOWS: a handoff that calls an artefact absent states WHERE it looked, and "not committed" is not "not on disk" in a repository whose whole verification scratch is gitignored by design.
END-SLIPS55

BEGIN-DEC55 sha256=8ac772c6a472dc066e91cc8225f629da6445736f5978fec86b5b3f99366f92b3
## DECISION F275 D32 (2026-09-11, F275 round 55) — the flip is a RETYPE and not a rename: DECISION F272 D15's atomicity SURVIVES, and what was wrong was the belief that the atomic change is a rename

CONTEXT. DECISION F275 D29 ruled three prerequisites before the flip, each the diagnosed cause of a measured class, and all three are now landed: P1 the type-resolved field rename at round 53, P2 the `UUID(...)` coercions at the seam at rounds 51 and 52 as `R-0877`, P3 the `**` splat class at round 54. D29's CONSEQUENCE clause places a dry run after all three, and `.agent/f275_t003_flip_residue_r55.md` records it, measured at `08feacae` in two disposable worktrees with a control at the same commit. THE PREREQUISITES DID WHAT THEY WERE ORDERED TO DO. The `JobPlan` constructor-keyword class, 867 exception lines and unmoved across both earlier dry runs, is ZERO. The `AttributeError` class falls from 517 to 127. The attributed residue falls from 2557 failures and 106 errors to 1331 and 79.

IT STILL DOES NOT CONVERGE, AND THE REMAINING CAUSE IS NOT A FOURTH MISSING RULE OF THE SAME KIND. The two records disagree about FIELD TYPES as well as about field names, read by importing the shipped classes at `08feacae`: a job id and a task id are `uuid.UUID` on the classic record and `str` on the unified one, a task status is `RunState` against `str`, and `created_at` is `datetime.datetime` against `str`. A rename carries the NAME and leaves every producer and every reader of the old TYPE standing. `JobPlan` is a dataclass, so it neither coerces nor complains: the transform rewrites `Job(id=uuid4())` to `JobPlan(job_id=uuid4())`, a `UUID` object is stored in a field declared `str`, and it travels until something uses it. 73 target constructions still hand `job_id` a `uuid4()` call and 6 hand it a `UUID(...)`; 342 of the 379 `unsupported operand` lines are attributed to `packages/orchestration/data_paths.py:200`, which is `jobs_dir(root) / job_id`; 176 of the 306 `SystemExit` lines to `data_paths.py:324`, the `no job matches prefix` exit, which is a record written under one spelling and read under the other. On the reading side, 46 lines are `task.status.value` at `project_brain.py:317` against a `status` that is no longer an enum and 23 are `result.task_id.hex[:8]` at `task_runner.py:480` against an id that is no longer a `UUID`.

CHOSEN: THE FLIP STAYS ONE COMMIT, AND THE TRANSFORM GAINS THE RETYPE RULES. The retype cannot be staged BEFORE the flip, and that is a measurement rather than a preference: `data_paths.mint_job_id()` returns sixteen hex characters, and constructing the classic record with it raises `pydantic ValidationError` on `id`, because `Job.id` is a `uuid.UUID`. So the classic record cannot hold the shipped id shape, the value and the field must change in the same instant, and DECISION F272 D15's ATOMIC ruling is confirmed rather than weakened — what this measurement corrects is the belief, never stated but acted on by every dry run of this chain, that the atomic change is a RENAME. It is a rename AND a retype, and the transform's own stated premise that no rule of it touches a CALL is what has to go. Three rule families are owed, each named by the class it closes: the id VALUE at a target construction becomes the shipped minter rather than `uuid4()`; a read of `.hex` or `.int` on a now-`str` id becomes a read of the string; and a read of `.value` on a now-`str` status becomes a read of the status. The next round builds them, and the honest test is another dry run with its control, because nothing here proves a further cause does not appear once the types are carried.

ALTERNATIVES CONSIDERED. (i) WIDEN THE UNIFIED RECORD to accept both shapes, or coerce in a `__post_init__` — rejected, and not on taste: that is the compatibility reader AGENTS.md's Scope Control forbids by name, it would leave the classic shape alive beside its replacement, and it would hide exactly the defect `R-0877` was spent finding, where a writer and its own reader disagreed silently. (ii) SPLIT the flip into a RENAME commit and a RETYPE commit — rejected on the measurement above: the classic record rejects the unified id shape, so a retype-first commit cannot be green and a rename-first commit leaves the tree at 1331 failures, which is not a landable state either. (iii) Declare the flip blocked and hand the question to the operator — rejected because operator amendment amend0908-f275-finish rule 2 permits that only when a module group is genuinely undeletable, and this is a transform with three more rules to write, not an impossibility. (iv) Carry the retype by hand at the attributed sites — rejected on arithmetic: the sites are 79 constructions and the read sites of four field types across 261 files, which is what a transform is for.

WHAT THIS DECISION DOES NOT RULE. It does not rule `TaskEntry.acceptance_checks`, which DECISION F275 D22 already placed with the flip round as a finding naming the inheriting feature, and this dry run only confirms that ruling's premise. It does not rule the `model_dump`, `model_dump_json` and `model_copy` calls the pydantic-to-dataclass change strands, which are 13 attributed lines and a smaller, separate cause. And it sets no size for the flip commit: DECISION F275 D17's declared-oversize route is unchanged and F275's one allowance is still unspent at 55 rounds.

HOW TO REVERSE: delete this decision. D29's three prerequisites and their landings stand either way; what is lost is the type table, the attribution of the four largest classes to it, and the measured reason the flip cannot be split — and the next session would re-derive them from two twenty-minute runs and one `pydantic ValidationError`.
END-DEC55
