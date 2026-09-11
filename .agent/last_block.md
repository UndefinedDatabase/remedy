── STEP T003 / round 60 — F275 ────────────────────────────────
Goal:        Land the measurement that resolves DECISION F275 D32's third retype rule
             family BY TYPE, and the decision that rules it. The family is nine sites
             rather than the seventy-six a receiver name suggests, and the artefact and
             the probe instrument are reviewer texts transported as whole files. The round
             59 verdict is booked. NO LINE UNDER `packages/`, `apps/`, `tests/`, `docs/`
             OR `scripts/` MOVES.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r60.md`
             C0b  save the artefact text verbatim as `.agent/authored/f275-r60-artefact.md`
             C0c  save the probe instrument verbatim as
                  `.agent/authored/f275-r60-probe.py.md`
             C0d  mirror the C0a blob into `.agent/last_block.md`
             C1   `.agent/plan.md` <- slice PLAN60, whole-file replacement
             C2   `.agent/live_review.md` <- slice RECORD60 appended
             C3   `.agent/decisions.md` <- slice DEC60 appended
             C4   `.agent/f275_t003_flip_residue_r60.md` <- a copy of the C0b blob
             C5   `.agent/handoff.md` rewritten — the handback

Change:      EXACTLY these paths and nothing else.
               .agent/authored/f275-r60.md                NEW
               .agent/authored/f275-r60-artefact.md       NEW
               .agent/authored/f275-r60-probe.py.md       NEW
               .agent/last_block.md
               .agent/plan.md
               .agent/live_review.md
               .agent/decisions.md
               .agent/f275_t003_flip_residue_r60.md       NEW
               .agent/handoff.md
             The four paths marked NEW do not exist at the base: `git ls-tree abc9b8a9 --`
             over all four prints nothing at exit 0, so each is an ADDITION and not a
             rewrite. `.agent/prose_slips.md` is NOT in this set: the reviewer spent no
             slip on round 59, and RECORD60 says so in its own text rather than leaving
             the absence to be inferred.

Constraints:
  1. EVERY authored slice is applied BYTE FOR BYTE. Do not reflow, re-wrap, correct,
     improve or re-indent one character, including text you believe is wrong. A slice you
     disagree with is applied as written and the disagreement goes in the deviations.
  2. Extract each slice from the COMMITTED blob of `.agent/authored/f275-r60.md` at C0a by
     its `BEGIN-`/`END-` marker-line prefix, marker lines EXCLUDED, never from this prompt
     and never from memory. A slice's BODY is the bytes from the start of the line after
     its BEGIN marker to the first byte of its END marker line, INCLUDING the terminal
     newline of the body's last line — this is stated because round 59's worker had to
     derive it by probing six candidate conventions, and the derivation need not be paid
     for twice. Each BEGIN marker carries its slice's own sha256; check it.
     The artefact and the instrument are WHOLE FILES: copy each with `shutil.copyfile`
     and never open either in an editor.
  3. The commit order above is FIXED. `.agent/plan.md` therefore names round 59 across
     C0a, C0b, C0c and C0d and becomes current at C1, which is the first SUBSTANTIVE
     commit and is what item 23 of §3 of `docs/agents/planner_reviewer_prompt.md` requires
     of a round that touches the finding ledger.
  4. This round creates NO `git worktree` and runs nothing destructive. The reviewer's own
     worktree was created, used and removed BEFORE this block was written, and
     `git worktree list` shows the primary checkout alone at the base.
  5. Nothing is written to `/tmp`. All scratch lives under the gitignored `.remedy-wt/`.
  6. No `remedy` CLI command and no `gh` command is run. No pull request is created,
     edited or merged.
  7. Re-read `.agent/STOP` FROM DISK before the first commit and again before C5, and
     report both readings literally. It does not exist at the reviewer's base reading.
  8. This block is 289 lines TOTAL and 216 PROSE, measured on its final bytes.
  9. NO finding id is registered this round and NONE is resolved. The open set is 88 by
     distinct id at the base and must read 88 at C4, with the registered set and the
     resolved set BOTH EMPTY and no id de-registered. A round may book a verdict without
     spending an id, and this is one.
 10. `.agent/authored/f275-r60-probe.py.md` is a `.md` and its extension is load-bearing:
     a `.py` file anywhere `ruff check .` scans is counted by
     `tests/orchestration/test_ci_budgets.py`, whose ceiling G6(c) reads. Do not rename it,
     and do not land a runnable copy of it anywhere in the tree. The reviewer reproduced
     that failure once this round by doing exactly that, which is why the constraint is
     here and why the artefact reports it.

Done when:   the seven gates below, each run for real as `bash -c '<cmd>; echo
             "REAL_EXIT=$?"'`, with the REAL exit code and the real output reported. A
             gate whose command you did not run is a finding, and the word "green" is not
             a reading. Every gate runs at a commit STRICTLY EARLIER than C5.

  G1 TRANSPORT. For each of the three authored blobs, compare the COMMITTED blob against
     the reviewer's scratch original by size and sha256:
       .agent/authored/f275-r60.md           @C0a  vs  .remedy-wt/f275-r60.block.md
       .agent/authored/f275-r60-artefact.md  @C0b  vs  .remedy-wt/f275-r60-artefact.md
       .agent/authored/f275-r60-probe.py.md  @C0c  vs  .remedy-wt/f275-r60-probe.py.md
     Then `.agent/last_block.md` @C0d against the C0a blob. Report all four EQUAL verdicts.
     Re-measure on the COMMITTED C0a blob: TOTAL lines, the summed lines of every slice's
     BODY, PROSE = TOTAL - BODY, and whether either exceeds 490 and 400. Report both
     numerals beside constraint 8's and say whether they agree. The block states no count
     of its own slices: the extraction is the sweep and its cardinality is your output.

  G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to slice PLAN60: report both sizes
     and both sha256. Report its line count against the AGENTS.md cap of 50, and the count
     of `^## Goal$` and of `^## Next Steps$`, each of which must be 1.

  G3 THE RECORD. Two appends in two commits, each proved by TWO readers and a negative
     control.
     (i)  READER A, over a BYTE stream: the post-commit blob equals the pre-commit blob
          followed by one newline and the slice's body.
            .agent/live_review.md   pre  978010 at the base, slice RECORD60
            .agent/decisions.md     pre 1118078 at C2,       slice DEC60
          Report each pre size, each post size and each delta. The slice body sizes are
          NOT stated here: each is the length of what you extracted.
     (ii) READER B, structural and independent: the LAST N blank-line-separated units of
          the whole post-commit file equal the slice's N paragraphs IN ORDER, where N is a
          value your script COUNTS from the slice. Report the N for each.
     (iii) NEGATIVE CONTROL, one per file: flip a single ASCII letter — a byte b with
          `b < 128 and chr(b).isalpha()` — inside the FIRST appended paragraph, and report
          that BOTH readers reject it. Report ALSO that both readers ACCEPT the unmutated
          region, because a reader that rejects everything proves nothing by rejecting.
     (iv) RECORD60 must carry no interior line beginning with any of `Gate: `, `- R-`,
          `Done: R-`, `Landed: R-`, `Recurrence: R-` or `DECISION F`; report that count,
          which must be 0. Report the count of `^- R-` and of `^Done: R-` lines that C2
          ADDS, both of which must be 0, since constraint 9 fixes this round at no id
          either way.
     (v)  Report RECORD60's first line beside the count of lines in `.agent/live_review.md`
          at `abc9b8a9` already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.`,
          and whether the new first line matches that pattern and duplicates none of them.
          Report the number your script counted; this block states none.
     (vi) DEC60 must begin `## DECISION F275 D35 ` and `.agent/decisions.md` at the base
          must contain NO line matching `^## DECISION F275 D35`. Report both readings, and
          report the highest existing `^## DECISION F275 D\d+` heading at the base.

  G4 THE ARTEFACT AND THE INSTRUMENT ARE THE AUTHORED BLOBS AND NOTHING ELSE.
     `.agent/f275_t003_flip_residue_r60.md` at C4 must be byte-identical to the
     `.agent/authored/f275-r60-artefact.md` blob at C0b — report both sizes and both
     sha256. Report the exit code of
     `git show abc9b8a9:.agent/f275_t003_flip_residue_r60.md`, which must be non-zero.
     Report the artefact's line count and the instrument blob's line count, each against
     the DECISION F104 D1 cap of 500 insertions.

  G5 THE CLAIMS THE ARTEFACT AND THE DECISION REST ON ARE STILL TRUE AT THIS COMMIT.
     Four readings, all cheap, all from the repository root.
     (a) Report whether `packages.core.models.Job` has a field named `status` and whether
         it has one named `state`, and report the annotation of `state` on BOTH
         `packages.core.models.Job` and `packages.orchestration.pingpong_job.JobPlan`.
         Section 2 of the artefact turns on `Job` having no `status` and on the two
         `state` fields being the same enum.
     (b) Report the annotation of `status` on each of `packages.core.models.Task`,
         `packages.orchestration.job_fulfillment.JobFulfillmentRecord`,
         `packages.orchestration.proposed_tasks.ProposedTask`,
         `packages.orchestration.integrity_gate.IntegrityCheck` and
         `packages.orchestration.pingpong_job.TaskEntry`, reading the LIVE classes. The
         artefact states the first four are enums and the fifth is `str`.
     (c) For each of the nine sites DEC60 names — `apps/cli/commands/job.py:655`,
         `packages/orchestration/brain_detail.py` at 353, 366, 372 and 380,
         `packages/orchestration/project_brain.py:317`,
         `packages/orchestration/trust_report.py:118`,
         `tests/orchestration/test_final_audit_evidence.py:261` and
         `tests/orchestration/test_resume_kill.py:261` — report the literal line at that
         number and whether it contains `.status.value`. Report what you found even where
         it differs; a site list that does not resolve is the `R-0879` defect arriving in
         a new artefact, and this gate exists to catch that before it lands.
     (d) Report the number of `<expr>.status.value` chains in the tracked tree that sit in
         AST STORE context, which the artefact states is 8, counting them with `ast` and
         never with a text search. Report the files they are in.

  G6 THE TREE DID NOT MOVE.
     (a) Report the git object id of each of `packages`, `apps`, `tests`, `docs` and
         `scripts` at `abc9b8a9` and at C4, and whether all five are EQUAL.
     (b) THE CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q`. It reads
         42 passed at exit 0 at the base.
     (c) `python3 -m ruff check . --output-format concise`. Its exit code is 1 whenever
         any finding remains, so the GATE IS THE COUNT: report the number of rows matching
         `^\S+:\d+:\d+: `, which is 26 at the base and is the ceiling
         `tests/orchestration/test_ci_budgets.py` freezes. Report rows under `.remedy-wt/`
         separately, and report rows whose path ends `.py` under `.agent/`, which
         constraint 10 is the reason to expect at zero. Do not use `grep -c` for a count
         you expect to be zero.

  G7 NOTHING ELSE MOVED.
     (a) Report whether `.agent/STOP` exists on disk, the literal output of
         `git status --porcelain` piped through `cat -A`, and the literal output of
         `git worktree list`. The first must be absent and the second the empty string.
         The third is REPORTED, not gated: state instead whether THIS ROUND created or
         removed any worktree, which constraint 4 fixes at neither.
     (b) The changed-path set over `abc9b8a9`..C4 must be exactly the Change section's
         paths other than `.agent/handoff.md`. Report MISSING and EXTRA, both of which
         must be empty, and the count of paths under `docs/`, `scripts/`, `packages/`,
         `apps/` or `tests/`, which must be 0.
     (c) The open set BY DISTINCT ID, derived as every `^- R-\d+ — ` paragraph minus every
         `^Done: R-\d+ — ` line, at `abc9b8a9` and at C4. Report both, the ids registered
         and the ids resolved, BOTH of which must be empty, and the ids de-registered,
         which must also be empty. Report the highest id in the record at each end.
     (d) Per-commit insertions from `git show --numstat <sha>` for C0a through C4, each
         against the AGENTS.md DECISION F104 D1 cap of 500, and the maximum over them.
         C5's own numbers are NOT ordered here: they cannot exist while C5 is being
         written, and the reviewer records them at the next gate.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 23 of F275 and
             round 60, the one-sentence context self-assessment amend0905-throughput
             requires, the changed-files table with every `+/-` taken from
             `git show --numstat` and no other source, one line per gate with its REAL
             exit code, the item-status table covering every C and every G exactly once,
             and the authored-text proofs. State the SCOPE REPORT position: F275 stands
             past the soft limit amend0908-f275-finish rule 1 names, the report written in
             round 51's handback STANDS and is not restated, rule 2 forbids the
             split-and-close default BY NAME, and this round closes nothing, registers no
             feature and does not touch `docs/roadmap/STATUS.md`. Carry the operator
             banner exactly as `docs/agents/self_drive_protocol.md` spells it. Then push.
──────────────────────────────────────────────────────────────

The three separators in this block carry runs of the box-drawing character U+2500, whose
lengths are stated here because a run of one character has no length a reader recovers by
eye. The STEP line that opens the frame is 63 characters holding 34 of them, in two runs
either side of its text. The rule that closes the frame, directly above this paragraph, is
62 of them and nothing else. The slice rule below is 10, the word SLICES between single
spaces, and 10 more.

────────── SLICES ──────────

BEGIN-PLAN60 sha256=a1e0ebd2262b6be49d49de51e843520a5f967a1f8aaaf9f7ea5fcfd105c42a5d
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

ROUND 60 resolves the `.status.value` family BY TYPE, in the round of round 53's shape
DECISION F275 D34 ordered, and DECISION F275 D35 rules the result. The descriptor probe
ran twice with symmetric difference 0. The family is NINE sites, not seventy-six: eight
chains are mock writes, twenty-nine already carry a shape guard, twenty-eight belong to
three records the flip does not touch, and both undecided chains are inside the guarded
class and so cost nothing. The artefact is `.agent/f275_t003_flip_residue_r60.md`. The
round 59 verdict is booked here.

## Next Steps

1. Build DECISION F275 D32's third rule family against the nine named sites, and re-run
   the dry run with its control to see whether it removes the 61 attributed lines.
2. Bound `R-0880` statically: read the ruled set's owner verdicts against the live record
   classes, and give the transform the refusal `R-0879` already gave it for stale keys.
3. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, registering
   the `acceptance_checks` finding DECISION F275 D22 places with it.
4. The resolver collapse DECISION F260 D5 places in T003, with the classic store, then the
   closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The three largest residue classes are attributed to an id SHAPE change rather than to a
  rename, and no rule family this chain has written covers them.
- `R-0880`'s over-selected sites are a floor from one run, not a bounded set.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN60

BEGIN-RECORD60 sha256=d04b7677bb10f229658c59cd053d5558a1be810d89d45238d2b5aefc8ee3baab
Gate: F275 R59 — the F275 round 59 entry. VERDICT PASS. Written by the planner and reviewer of session 23 after reading the committed range `bf692757`..`abc9b8a9` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 60, per operator amendment amend0827-process-diet rule 1. The round's subject was the defect `R-0879` names, and the round both fixed the instrument and measured that the fix holds.

G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: all three authored blobs are byte-identical to the reviewer's own scratch originals — the block at 30550 bytes and sha256 `b940b14f789c0b027c24847793207330589d70b9ec2b34f6e285080bdc5ed649`, the artefact at 12128 and the re-key instrument at 6090 — and `.agent/last_block.md` equals the block blob. Each slice additionally matched the sha256 on its own BEGIN marker, re-derived by the reviewer from the committed C0a blob. Re-measured there the block is 277 lines TOTAL and 220 PROSE, agreeing with its own constraint 8. G2: `.agent/plan.md` is byte-identical to PLAN59 at 2627 bytes over 45 lines, both mandated headings exactly once, and it satisfies all three assertions of `test_plan_md_current`, which the reviewer read before authoring rather than after.

G3: `.agent/live_review.md` goes 966689 to 978010, a delta of 11321 across RECORD59, DONE59 and FIND59 taken as ONE ordered region, and `.agent/prose_slips.md` 252059 to 253122; both exact under reader A. Reader B holds for both at N COUNTED from the slices, 7 and 1. The reviewer ran its own negative controls rather than reading the worker's: flipping one ASCII letter in the FIRST appended paragraph of each file is REJECTED by both readers, while the UNMUTATED region is ACCEPTED by both — so the readers were shown to be capable of passing as well as failing, which is what makes the rejection evidence. `R-0878` keeps its `Landed:` line byte-identical to the base and gains its `Done:` beside it, 0 to 1, which is the append-only record holding both halves of a fix rather than overwriting the first.

G4: the artefact at C4 is byte-identical to the C0b blob at 12128 bytes, the path does not resolve at the base, and the artefact and the instrument are 210 and 140 lines against the 500 cap. G5: the reviewer re-took all four readings itself — the seven retyped records read five `str` and two `str | None`, exactly as DONE59 states and with the nullability preserved rather than widened; the uuid-record ratchet reads 7 passed at exit 0; `Mission` carries `id` and does NOT carry `job_id`, which is what FIND59 turns on. G6: all five of `packages`, `apps`, `tests`, `docs` and `scripts` are byte-identical trees at the base and at C4, the canary reads 42 passed at exit 0, and `ruff check .` reads 26 finding rows at the frozen ceiling with ZERO under `.remedy-wt/` and ZERO `.py` rows under `.agent/` — the last of those being constraint 10's `.md` extension working as it was ordered to. G7: eight changed paths with MISSING and EXTRA both empty and ZERO production paths; the open set reads 88 at both ends with `R-0880` the only id added and `R-0878` the only id resolved and none de-registered, which is the membership check the block ordered BECAUSE the count does not move; per-commit insertions are 277, 210, 140, 172, 18, 14, 2 and 210, every one under the cap, so F275's one declared-oversize allowance is STILL UNSPENT at 59 rounds. The handback commit's own insertion count, which no gate of that round could reach, is 432.

THE WORKER DECLARED FIVE DEVIATIONS AND THE FIRST AND FIFTH BOTH IMPROVED ON THE ORDER. Its first extraction of the five slices joined lines without a terminal newline and missed ALL FIVE marker digests; rather than proceed on text that did not verify, it probed six candidate conventions, found that exactly one matched all five without exception — the body including its terminal newline — corrected, and re-ran. That is a transport proof doing its job: a worker that had shrugged and applied the text anyway would have applied the same bytes and proved nothing. The fifth is sharper still. G5(d) asked which of lines 285 and 286 holds the `link_job_to_mission` call, and the worker answered that the CALL SPANS BOTH: the call token and the two receiver expressions FIND59 names are on 285, and 286 carries the continuation `MISSION_ROLE_INITIAL, root=root)`. FIND59's quoted excerpt ends in a trailing comma, so the elision is visible and no sentence of it is false, but the worker was right to say that a two-line call quoted as one line is a reader's trap rather than a measurement. The remaining three deviations are sustained and are the standing ones: the plan named round 58 across the block-save commits as constraint 3 requires, ruff exits 1 by design while the gate is the count, and G4's absence probe exits 128 with a stderr clause describing the working tree rather than the base.

THE REVIEWER SPENT NO PROSE SLIP THIS ROUND AND SAYS SO RATHER THAN LEAVING THE ABSENCE TO BE INFERRED. The one candidate was the line-number citation in the artefact and in FIND59, and it was caught BEFORE emission by running every gate at the base as finding `R-0364` and item 12 of `docs/agents/planner_reviewer_prompt.md` §3 require: the traceback frame reads 286 because rule I5 inserts an import above the line, the base file reads 285, and both numbers went into both texts with the reason. A citation corrected before it lands is not a slip; it is the pre-emission check working, and this is the first round of this session in which that check caught something.
END-RECORD60

BEGIN-DEC60 sha256=393bbc0ebb7d1a1498bd7aa4c6bab35f4e5cef07855f3a4568fdebaa5c7179cd
## DECISION F275 D35 (2026-09-11, F275 round 60) — the `.status.value` family is NINE sites, not seventy-six: it is resolved by TYPE, and two of the three things it was thought to contain are not records at all

CONTEXT. DECISION F275 D32 named three retype rule families. Two are built. The third — a read of `.value` on a status that is a `str` after the flip — was deferred twice: round 58 declined to build it and DECISION F275 D34 recorded the reason, that its 76 sites sit on ten receiver names of which `record` at 18, `latest`, `c`, `held` and `released` decide nothing by name, and that resolving them by name would reintroduce the exact heuristic DECISION F275 D29's P1 was written to kill. D34 ordered a round of round 53's shape. This is that round, and the measurement is in `.agent/f275_t003_flip_residue_r60.md`.

THE FIRST FACT NARROWED THE QUESTION BEFORE ANY PROBE RAN. `Job` has no `status` field at all — it has `state`, and `JobPlan.state` is `RunState` on the unified record exactly as `Job.state` is on the classic one, so `job.state.value` reads the same enum on both sides of the flip and was never in this family. A sweep over the live class objects of every class kind under `packages.` and `apps.`, 328 modules walked with ZERO skipped on import, finds 61 classes declaring a `status` field and only FOUR whose `status` is an enum: `Task` (`RunState`), `JobFulfillmentRecord` (`JobFulfillmentStatus`), `ProposedTask` (`ProposedTaskStatus`) and `IntegrityCheck` (`IntegrityStatus`). The other 57 declare it `str`, and `TaskEntry.status` — the unified record's own — is one of those. So `.status.value` is meaningful on exactly four records and the flip retypes exactly one of them.

CHOSEN, PART ONE: THE FAMILY IS RESOLVED BY FOUR READINGS IN ORDER, AND A SITE IS CLAIMED ONLY WHERE ONE OF THEM DECIDES IT. The DECISION F272 D7 descriptor probe, run twice over the full suite with its descriptor tuple narrowed to `Task.status` and every other line of round 53's instrument unchanged, decides 26; a compared string literal belonging to exactly one of the four enums decides 19; the module that DEFINES a record decides 13; the receiver's own binding inside its function — `latest = records[-1]` out of `list_fulfillment_records`, `for task in job.tasks`, `held = self._fulfill(...)` — decides 8. Two are left UNDECIDED and are reported rather than guessed. The two runs agree as SETS of `(owner, field, mode, path, line, func)` with symmetric difference 0 over 219 rows each, which is the reproducibility reading round 53 established and this round repeats rather than re-argues.

CHOSEN, PART TWO: TWO OF THE THREE THINGS THE FAMILY WAS THOUGHT TO CONTAIN ARE NOT REWRITE TARGETS, AND BOTH WERE FOUND BY READINGS THAT COST NOTHING TO TAKE. EIGHT chains are in STORE context — `t.status.value = "completed" if i == 0 else "pending"` — and a `RunState` member is immutable, so such a statement cannot execute against a real enum and its receiver is necessarily a mock. Three independent readings agree on all eight: the AST context is Store, the receiver is bound to `MagicMock()` in the same file, and the probe recorded none of them as a `Task.status` read. Rewriting them would change what the mock holds while the code under test still reads it back through `.value`. TWENTY-NINE more are already shape-agnostic, written `t.status.value if hasattr(t.status, "value") else str(t.status)`, and they read an enum today and a `str` after the flip with no edit at all. A rule that touched either group would be churn wearing a fix's clothes.

CHOSEN, PART THREE: THE RULE FAMILY REWRITES NINE SITES, AND THEY ARE NAMED. Every one is a BARE `.status.value` read whose owner is `Task`: `job.py:655`, `brain_detail.py` at 353, 366, 372 and 380, `project_brain.py:317`, `trust_report.py:118`, `test_final_audit_evidence.py:261` and `test_resume_kill.py:261`, all at `abc9b8a9`. THE CROSS-CHECK THAT MAKES THIS MORE THAN AN INVENTORY: the previous round's dry run attributed 61 `str.value` exception lines to two source frames, `project_brain.py:317` at 54 and `trust_report.py:119` at 7, and both are in the nine — the `trust_report` line differing by one because rule I5 inserts an import above it in the transformed tree. The residue found the same sites from the opposite direction.

WHY THE UNDECIDED RESIDUE COSTS NOTHING, which is a ruling and not a hope. Both undecided chains are `ui_server.py:1025` and `ui_server.py:1071`, and BOTH carry the `hasattr` guard, so they read correctly whichever of the four records they hold. The two sites this round could not name are inside the class that needs no rewrite, so the answer is complete for the purpose the measurement exists to serve even though it is incomplete as an attribution.

ALTERNATIVES CONSIDERED. (i) Resolve the family by receiver name — rejected, and this decision records what that would have cost rather than only restating D29's P1: `t` is the most common receiver name at 39 occurrences and 8 of them are mocks, `task` covers both `Task` and `ProposedTask`, and `record` at 18 is `JobFulfillmentRecord` and never a job record. (ii) Resolve it by the set of records each FILE imports or names — TRIED AND REJECTED ON EVIDENCE, which is why it is listed here rather than omitted: `ui_server.py` names only `ProposedTask` while the probe records SEVEN of its chains as `Task.status` reads, so a file-level reading mis-assigns them, and it does so silently and in the confident direction. (iii) Rewrite all 76 and let the suite find the mistakes — rejected: 28 of them belong to three records the flip does not touch, and the flip is the one commit in this feature that cannot be split. (iv) Widen the 29 guarded sites to a single helper — rejected as out of scope: they are correct as they stand, AGENTS.md's Scope Control forbids the "while I'm here" edit by name, and a helper is a compatibility reader in the shape D32 already refused.

WHAT THIS DECISION DOES NOT RULE. It does not build the rule: the nine sites are named, no transform consumes them yet, and whether rewriting exactly these nine removes exactly the 61 attributed lines is the next dry run's reading. It settles nothing about the 1453 `<expr>.status` nodes that do NOT continue into `.value`; `TaskEntry.status` is already `str`, so a bare `task.status` read should be flip-safe by construction, but that is an inference from the field types and was not measured site by site. And it does not ratchet the four-record enumeration: a record introduced later with an enum `status` would not be in it.

HOW TO REVERSE: delete this decision. The third rule family then has no site set, and the next session re-derives it from two twenty-one-minute probe runs, one live-class sweep and the four readings above — which is roughly a session, and is what this round spent.
END-DEC60
