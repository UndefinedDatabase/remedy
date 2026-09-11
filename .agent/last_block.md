── STEP T003 / round 51 — F275 ───────────────────────────────
Goal:        Land the first group of DECISION F275 D29's P2 and register `R-0877`, the
             defect it repairs. `timeline.append_run_event` and
             `test_failure_artifact.emit_failure_events` coerce their `job_id` with
             `UUID(str(job_id))`, which rejects the sixteen hex characters
             `data_paths.mint_job_id` produces, and for an unhyphenated 32-hex id write a
             directory the reader in the same module never looks in. Both join the id
             verbatim instead. Guard all three halves with tests that go red without it.

Bundle:      C0a  save this block verbatim as `.agent/authored/f275-r51.md`
             C0b  mirror it into `.agent/last_block.md` from the committed blob
             C1   slice PLAN51 — whole-file replacement of `.agent/plan.md`
             C2   slices RECORD51 and FIND51 — the round 50 PASS verdict and the
                  registration of `R-0877`
             C3   THE FIX — pairs P51A through P51J, then the code append GUARD51
             C4   slice LANDED51 — the `Landed: R-0877` line, appended after the fix
             C5   the handback, rewriting `.agent/handoff.md`

Change:      EXACTLY these paths and nothing else.
             `.agent/authored/f275-r51.md`  (new) · `.agent/last_block.md` ·
             `.agent/plan.md` · `.agent/live_review.md` ·
             `packages/orchestration/timeline.py` ·
             `packages/orchestration/test_failure_artifact.py` ·
             `packages/orchestration/run_log.py` ·
             `packages/orchestration/safe_points.py` ·
             `tests/orchestration/test_budget_tick.py` · `tests/test_timeline.py` ·
             `.agent/handoff.md`
             NO path under `apps/`, `docs/` or `scripts/` moves this round, and
             `.agent/decisions.md` is NOT touched — DECISION F275 D29 already rules this
             work and this round performs it rather than re-deciding it.
             `.agent/prose_slips.md` is NOT touched: no reviewer-prose inaccuracy is owed.

Constraints:
 1. Apply every slice BYTE FOR BYTE; extract each mechanically from the COMMITTED blob of
    `.agent/authored/f275-r51.md` by its `BEGIN-<name> ` / `END-<name> ` marker-line
    PREFIX. Never retype, reflow or edit one. A slice that looks wrong is applied as given
    and DECLARED.
 2. The commit order C0a, C0b, C1, C2, C3, C4, C5 is FIXED — none merged, none reordered.
    C1 precedes C2 because a round that books into the finding ledger advances the plan
    first (planner_reviewer_prompt.md §3 item 23). C4 comes AFTER C3 because a `Landed:`
    line may only be written once the fix it describes is committed.
 3. EVERY length is `len(<bytes>)` from `read_bytes()` or a `git show` byte stream, never
    `len()` over a decoded `str`.
 4. The three appends — RECORD51, FIND51, LANDED51 — are `old_bytes + slice_bytes` in
    Python. Each owns its leading blank line. All pre-blobs end in a newline; add none.
    GUARD51 is a CODE append and obeys the same rule.
 5. This round REGISTERS `R-0877` and RESOLVES nothing. Write the `Landed: R-0877` line at
    C4 and NO `Done:` paragraph — only reviewer-authored text sets a resolution. The open
    set goes 86 at the base to 87 at C4.
 6. ALL TEN PAIRS ARE REWRITES, established by the containment test rather than by eye:
    for each, the test's own output reads `TO contains FROM: false`. P51A is the one whose
    TO is a PREFIX of its FROM — an import line loses a name — so for that pair the
    FROM-count reading is the discriminating one and a TO count proves nothing, which G4
    says in its own text.
 7. Destructive verification — the red proof in G7 — runs ONLY inside a disposable
    `git worktree` under the gitignored `.remedy-wt/`, removed and pruned before the
    handback. The primary checkout satisfies `git status --porcelain` == empty at every
    commit.
 8. Re-read `.agent/STOP` FROM DISK before the first commit and report what you found.

Done when:   the gates below, each run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`,
             one line per gate in the handback, EVERY reading taken at C4 or earlier.
             Report the number of gates YOU ran; this block states none.

 G1  TRANSPORT, at C0b. sha256 over the bytes of `.agent/authored/f275-r51.md` equals the
     digest the delegation message states — this block carries marker lines for its SLICES
     only and no BEGIN marker of its own. `.agent/last_block.md` is written from
     `git cat-file blob <C0a-sha>:<that path>` and never retyped. Report both byte counts
     and both digests, and state the chain the proof walked. Claim nothing about the bytes
     emitted into your prompt.

 G2  THE PLAN, at C1. `.agent/plan.md` BYTE-EQUAL to slice PLAN51: both byte counts, both
     sha256 digests, the line count against the AGENTS.md cap of 50, `^## Goal$` exactly 1x
     and `^## Next Steps$` exactly 1x.

 G3  THE RECORD, at C2, then again at C4. Read every pre and post blob with
     `git show <sha>:<path>` INTO MEMORY — never write a non-current revision over a
     tracked file.
     (i)  `.agent/live_review.md` ← RECORD51 then FIND51, applied in that order inside C2,
          pre at C1 and post at C2, all three readings:
          (a) reader A: pre_bytes + RECORD51 + FIND51 == post_bytes, `identical: True`.
          (b) reader B, structural: N is the number of blank-line-separated paragraphs your
              script COUNTS across the two slices — never a number this block asserts — and
              the LAST N blank-line units of the post blob equal those N paragraphs IN
              ORDER, stripped.
          (c) negative control: flip ONE byte inside the FIRST appended paragraph of the
              IN-MEMORY copy; reader A rejects AND reader B rejects, each re-run against
              the ORIGINAL slices.
     (ii) `.agent/live_review.md` ← LANDED51, pre at C3 and post at C4, reading (a) alone.

 G4  THE TEN PAIRS, at C3, against COMMITTED blobs. For EACH pair report, in one table row:
     the containment test's own output, which reads `TO contains FROM: false`; the FROM
     count in the base blob `17d3f513`, which is 1; and the FROM count in the C3 blob,
     which must be 0. Report the TO count in the C3 blob for every pair EXCEPT P51A, whose
     TO already occurs inside its own FROM so that count discriminates nothing; say so on
     that row rather than omitting it silently. Then REBUILD each edited file
     from its base blob by applying ONLY the pairs this block assigns to that file, in the
     order they are listed, and report byte-identity against the C3 blob.

 G5  THE GUARD, at C3, as a CODE APPEND and therefore by ORDERED EQUALITY, not by a
     per-line count — a code slice repeats blank lines and `assert` lines structurally, so
     multiplicity is unattainable by construction. For `tests/test_timeline.py` ← GUARD51,
     all three: the base blob at `17d3f513` is a byte-exact PREFIX of the C3 blob; the
     slice is a byte-exact SUFFIX of the C3 blob; and the lines that C3's diff ADDS for
     that path are exactly the slice's lines IN ORDER.

 G6  THE FIX WORKS AND NOTHING NEAR IT MOVED, at C3.
     (a) `git rev-parse C3:packages` must equal `6d2ec62e10948175e3c338aa951f3bca3cb4ddc5`
         and `git rev-parse C3:tests` must equal
         `b104a5acd66ce6c1c1482e7deaf4c862b0bcda52`. At the base `17d3f513` the same two
         read `1f1a040413f8045a9e53ec8dece733ddb1d0c0ac` and
         `b33e3ac3ed64ebd1d6fa4e0b86c9f8614c4d07ee`. These are the reviewer's own
         measurement of this fix applied to a clean checkout; a digest that differs means
         your tree is not the tree that was measured, so report it and stop.
     (b) `git diff --numstat <C3-sha>^..<C3-sha>` — C3's OWN range, never a range that
         starts at the base, which would also carry C0a..C2's `.agent/` rows — reads
         exactly six rows: 2/2 `run_log.py`, 5/5 `safe_points.py`, 2/2
         `test_failure_artifact.py`, 11/5 `timeline.py`, 6/4 `test_budget_tick.py`, 52/0
         `test_timeline.py`. Report every row you measured.
     (c) THE RUFF CEILING, because this round deletes two imports and
         `tests/orchestration/test_ci_budgets.py` freezes the repository's count.
         `python3 -m ruff check . --output-format concise` at C3 and at the base
         `17d3f513` — read the base with a disposable worktree under `.remedy-wt/`, never
         by writing base bytes over a tracked file. Report the finding COUNT at both; both
         are 26.
     (d) The SCOPED round gate, in the primary checkout at C3:
         `python3 -m pytest tests/test_timeline.py tests/test_run_log.py
         tests/test_run_log_cli.py tests/orchestration/test_test_failure_repair.py
         tests/orchestration/test_failure_wiring.py
         tests/orchestration/test_failure_postmortem.py
         tests/orchestration/test_ci_budgets.py tests/orchestration/test_budget_tick.py
         tests/ui_server/test_budget_tick_envelope.py
         tests/orchestration/test_source_apply.py -q`
         and the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. Report both
         last lines and both exit codes.

 G7  THE RED PROOF, at C3, in a disposable worktree under `.remedy-wt/` detached at C3,
     never `cd`-ed into: run every command as `subprocess.run([...], cwd=<abs worktree>)`
     under `python3 -B` with `-p no:cacheprovider`, purge `__pycache__` first, and PRINT
     the resolved `__file__` of `packages.orchestration.timeline` before believing any
     result — it must lie inside the worktree, not in the primary checkout or an install.
     Selection for EVERY run, all three node ids together:
     `tests/test_timeline.py::TestRunEventsAcceptTheShippedJobIdShape::test_append_run_event_takes_the_shipped_job_id_shape`,
     `::test_emit_failure_events_takes_the_shipped_job_id_shape` and
     `::test_a_run_event_is_readable_by_the_reader_in_its_own_module` on the same class.
     Run the UNMUTATED control FIRST and report its exit code beside every mutated one.
     M1 reverts P51C's writer statement alone — restore the coercion, importing `UUID`
     locally since P51A removed the module-level import. M2 reverts P51F. Record each
     file's sha256 BEFORE its mutation and prove the revert byte-exact against that
     recorded digest. Report the FAILED node ids as a SET per run, parsing a node id as
     what follows the FIRST space of a `FAILED <nodeid> - <msg>` line. TWO MUTATIONS ARE
     ORDERED AND THEIR SETS ARE NOT DISJOINT: M1 reddens all three and M2 reddens only
     `test_emit_failure_events_takes_the_shipped_job_id_shape`, so report the containment
     rather than a disjointness that does not hold. What M2 establishes is that the
     `emit_failure_events` fix is independently necessary — with `timeline.py` already
     fixed, that one node is still red without it. Finish with the control again.

 G8  NOTHING ELSE MOVED, at C4.
     (a) `.agent/STOP` re-read from disk: report the literal result. `git status
         --porcelain` == `''`: report the literal string.
     (b) The changed-path set over `17d3f513..C4` equals the paths the Change section
         lists, other than `.agent/handoff.md` which C5 writes. Resolve that expectation
         against the Change section itself, not against a number stated anywhere in this
         block. Report MISSING and EXTRA as lists, and the count of paths in that set
         under `apps/`, `docs/` or `scripts/`, which must be 0.
     (c) THE OPEN SET, BY DISTINCT ID over `.agent/live_review.md`: distinct `^- R-\d+ — `
         minus distinct `^Done: R-\d+ — `, at the base `17d3f513` and at C4. It reads 86 at
         the base and must read 87 at C4. Report the ids registered and the ids resolved
         this round as lists. Report `^Landed: R-0877 ` at C3 and at C4, which are 0 and 1,
         and `^Done: R-0877 ` at both, which is 0 at both.
     (d) Each of C0a..C4's own insertion count against the F104 D1 cap of 500, derived ONCE
         from `git show --numstat <sha>` and used both here and in the `+/-` column of the
         handback's `## Commits` table.

Handback:    completion report + rewrite `.agent/handoff.md`. Carry SESSION 20 of F275,
             round 51, the item-status table with every ordered item exactly once, the
             deviations, and one sentence of context self-assessment. THIS HANDBACK ALSO
             CARRIES THE SESSION'S SCOPE REPORT — see the closing section of this block.
──────────────────────────────────────────────────────────────

WHAT THE REVIEWER ALREADY MEASURED, so that no gate above re-derives it. This fix was
applied to a clean checkout at `17d3f513` in a disposable worktree and run. `ruff check .`
reads 26 findings there and 26 at the base. The scoped selection in G6(d) reads `481 passed`
at exit 0 and the canary `42 passed` at exit 0. THE FULL SUITE was run too, which a round
gate does not require and which is reported here rather than ordered: `1 failed, 18369
passed, 29 skipped` at exit 1, the single failure being
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`,
which needs the gitignored `apps/ui/node_modules` and fails in every fresh worktree — it is
the same node id the round 50 control failed on. The red proof in G7 was run in full: the
control reads `3 passed` at exit 0, M1 `3 failed`, M2 `1 failed, 2 passed`, both reverts
byte-exact and the control green again.

WHY THE NEIGHBOURHOOD MOVES IN THE SAME COMMIT, because two of the ten pairs touch files the
Goal does not name. `packages/orchestration/safe_points.py` and
`tests/orchestration/test_budget_tick.py` each carry a paragraph whose stated CAUSE is the
coercion this round removes; leaving them would put two false explanations on disk beside a
correct fix. Neither pair changes a line of code or an assertion — P51I and P51J are prose
inside a docstring — and DECISION F022 D2 clause one is NOT reversed here: the budget tick
still writes through `RunLogWriter`, and its regression test still holds it there.

SESSION 20 IS PAST F275's SOFT LIMIT AND THIS HANDBACK OWES THE SCOPE REPORT. Operator
amendment amend0908-f275-finish rule 1 sets that limit at 20 sessions and 60 rounds; this is
session 20 and round 51. Rule 2 forbids the amend0905-throughput split-and-close default here
BY NAME: the session writes the report and CONTINUES. Write, in `.agent/handoff.md`, a
section headed `## Scope report` carrying (a) WHAT IS FINISHED, (b) WHAT IS MISSING and
(c) A PROPOSAL, each drawn from `.agent/plan.md` as this round leaves it, from
`docs/roadmap/features/T2_F275.md`'s three task slices, and from DECISION F275 D29's three
prerequisites — every claim a reading you took, none carried from this block. Put this line
on its own, verbatim, in the handback and in your completion report:

    SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

Do NOT close F275, do NOT register a follow-up feature, and do NOT touch
`docs/roadmap/STATUS.md`. The report is a report.

────────── SLICES ──────────
The authored texts follow, in the order their commits apply them: PLAN51, RECORD51, FIND51,
the ten pairs P51A through P51J each as a `_FROM` and a `_TO` slice, GUARD51 and LANDED51.
Each is delimited by its own `BEGIN-`/`END-` marker lines; the marker lines are NOT part of
any slice and never reach a target file. Every rule line in this block's frame is a run of
U+2500 BOX DRAWINGS LIGHT HORIZONTAL, and no rule LENGTH is load-bearing: markers are matched
by PREFIX and the frame carries no appliable bytes.

Slice shapes, mechanically. PLAN51 is a WHOLE-FILE REPLACEMENT. RECORD51, FIND51 and
LANDED51 are prose APPENDS applied as `old_bytes + slice_bytes`, each carrying its own
leading blank line. GUARD51 is a CODE APPEND, proved by ordered equality under G5. The ten
pairs are REWRITES under G4, and each pair's `_FROM` and `_TO` slices carry their own
trailing newlines because every one of them is a whole-line span.

Pair-to-file assignment, which G4's rebuild step needs. `packages/orchestration/timeline.py`
takes P51A, P51B, P51C and P51D in that order. `packages/orchestration/run_log.py` takes
P51G then P51H. `packages/orchestration/test_failure_artifact.py` takes P51E then P51F.
`packages/orchestration/safe_points.py` takes P51I alone.
`tests/orchestration/test_budget_tick.py` takes P51J alone.

BEGIN-PLAN51 ─────────────────────────────────────────────────
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

ROUND 51 lands the first group of DECISION F275 D29's P2 and registers `R-0877`, the defect
it repairs. `timeline.append_run_event` and `test_failure_artifact.emit_failure_events`
coerced their `job_id` with `UUID(str(job_id))`, which rejects the sixteen hex characters
`data_paths.mint_job_id` produces — and for an unhyphenated 32-hex id wrote a directory the
reader in the same module never looked in. Both now join the id verbatim, as
`data_paths.run_log_dir` already did. The round 50 PASS verdict is booked here.

## Next Steps

1. P2's remaining groups — the surviving `UUID(...)` coercions over a job or task id that
   are NOT dual-shape normalisers, landed one assignment-connected component per commit as
   DECISION F275 D28 rules for an id widen.
2. P1 — replace the transform's receiver-NAME heuristic with the DECISION F272 D7
   raising-property probe `docs/roadmap/features/T2_F275.md` T002 already orders. The probe
   and its site set exist at `0b009325` in `.agent/f275_t002_flip_inventory.md`; T003
   re-derives them at its own base, as that file says it must.
3. P3 — the `**` splat call-graph pass over the test helper factories.
4. Re-run the dry run, then THE FLIP as the one declared-oversize commit AGENTS.md permits
   per feature, declared with its inseparability reason before review.
5. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
6. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: the session writes the scope report and CONTINUES.
- The open set is 87 by distinct id once this round registers `R-0877`. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END-PLAN51 ───────────────────────────────────────────────────

BEGIN-RECORD51 ───────────────────────────────────────────────

Gate: F275 R50 — the F275 round 50 entry. VERDICT PASS. Written by the planner and reviewer of session 20 after reading the committed range `020b1d57`..`69d1e673` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line below. G1 is the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: the reviewer's scratch original, the saved copy at C0a `801c3e90` and the mirror at C0b `c7439c12` are one blob at 41409 bytes and sha256 `9dce5f36949d1e3995281ee5d0de18b19376224fcfd8c2ab4079ee153e025fcf`. G2: `.agent/plan.md` byte-identical to slice PLAN50 at 2578 bytes over 45 lines, both mandated headings exactly once. G3: `.agent/live_review.md` 898808 to 905059 across RECORD50 and DONE50 together and `.agent/prose_slips.md` 241765 to 242729 for SLIPS50, reader A identical in both, reader B true at N counted from the slices — 2 and 1 — and the negative control flipped at offset 898829, inside the FIRST appended paragraph, rejected by BOTH readers. G4 IS THE GATE THIS ROUND EXISTS FOR: `.agent/f275_t003_flip_residue_r50.md` is byte-identical to slice ARTEFACT50 at 12529 bytes and sha256 `3d03d5d2969589f190c3dd7f68ef3388dca790d64ff15314ddf9e0c1dcb6506e`; `git show 591c3050:<that path>` exits 128, which is what makes C3 an ADDITION rather than a rewrite; and the reviewer EXTRACTED the artefact's own embedded instrument from the committed C3 blob — 2741 bytes, sha256 `6b4075877f968b22d4b1c314f8e410c0442a7a1930a23a23e4d63b193f36da59` — ran it, and compared its 26 output lines against the 26 the artefact records, `recorded == actual: True`. An artefact that reproduces its own numerals is the only kind this record should carry. G5: `.agent/decisions.md` 1085053 to 1090029 for DEC50, reader A identical, reader B true at N counted as 7, the control flipped at 1085084 in the FIRST paragraph and rejected by both, and `^## DECISION F275 D29 ` reading 1 at C4 against 0 at C3. G6: the reviewer re-ran the scoped selection itself at `161 passed` and the canary at `42 passed`, both exit 0, porcelain empty before each. G7: the changed-path set over `020b1d57`..C4 is exactly the seven paths the Change section names with MISSING and EXTRA both empty and ZERO under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`; the open set goes 87 at the base to 86 at C2 with `R-0876` the only id resolved and none registered; `^Done: R-0876 ` reads 0 at C1 and 1 at C2 while `^Landed: R-0876 ` reads 1 at both, which is the append-only record keeping the fix's own line beside its resolution; and per-commit insertions are 477, 413, 22, 6, 224 and 14, every one under the AGENTS.md DECISION F104 D1 cap of 500, so F275's one oversize allowance is still unspent at 51 rounds. THE HANDBACK'S EIGHT SHA-256 TOKENS WERE AUDITED AND ALL EIGHT ARE MEASURED — the six slices, the block itself and the extracted instrument — which matters because the worker declared that its own first draft of that table carried three invented digests, caught them in its self-review before C5 was committed, re-extracted and re-hashed, and added a verifier that every 64-hex token in the file is a measured value. Nothing false was committed, and a worker that audits its own arithmetic before the reviewer does is the behaviour this split exists to produce. THE ONE DECLARED DEVIATION IS SOUND: G4's instrument ran against the working tree rather than a checkout of `020b1d57`, and the reading is identical because G7 measures the round's changed-path set as seven paths all under `.agent/` with zero tracked `.py` among them — the reviewer re-ran the same extraction and got the same 26 lines.
END-RECORD51 ─────────────────────────────────────────────────

BEGIN-FIND51 ─────────────────────────────────────────────────

- R-0877 — Medium. THE RUN-LOG WRITER REJECTS THE ID SHAPE THE SHIPPED MINTER PRODUCES, AND FOR THE ONE STRING SHAPE IT DOES ACCEPT IT WRITES WHERE ITS OWN READER DOES NOT LOOK. Raised by the reviewer at `17d3f513` while sizing DECISION F275 D29's P2, from a behaviour probe over the SHIPPED functions rather than from a reading of the source. TWO SITES, both production, both annotated `job_id: UUID | str` and both coercing: `packages/orchestration/timeline.py` in `append_run_event`, and `packages/orchestration/test_failure_artifact.py` in `emit_failure_events`. An `ast` sweep over the 993 tracked `.py` files at `17d3f513` finds exactly these two — a parameter annotated `UUID | str` whose body calls `UUID()` — beside sixteen further `UUID | str` parameters whose bodies do NOT coerce and are therefore already shape-agnostic. THE FIRST HALF, MEASURED BY CALLING THE SHIPPED CODE: `data_paths.mint_job_id()` returns sixteen hex characters, which is the shape DECISION F260 D2 rules, and `append_run_event(d, mint_job_id(), event=...)` raises `ValueError: badly formed hexadecimal UUID string` at `uuid.py:177`; `emit_failure_events(d, mint_job_id(), failure)` raises identically. THE SECOND HALF IS THE ONE NO ANNOTATION SHOWS: `run_log_dir` joins `str(job_id)` VERBATIM, so for the unhyphenated 32-hex string the coercion does accept, the writer creates `job_logs/00000000-0000-0000-0000-000000000000/` while `load_run_events` — in the same module, four lines below — reads `job_logs/00000000000000000000000000000000/`. Measured: one event written, `load_run_events` returns 0 for the id it was written under and 1 for the hyphenated form. A write that its own module cannot read back is worse than a raise, because nothing reports it. THIS REPOSITORY HAS KNOWN THE FIRST HALF SINCE F022 AND ROUTED AROUND IT ONCE: `packages/orchestration/safe_points.py` `_emit_budget_tick` carries a six-line docstring paragraph explaining that it writes through `RunLogWriter` and NOT through `append_run_event` for exactly this reason, and `tests/orchestration/test_budget_tick.py::TestTickCadenceAndShape::test_a_pingpong_shaped_job_id_still_emits` is its regression test. The workaround is local to that one emission; every other caller holding a one-world id still raises. THE FIX: both functions stop coercing and join the id verbatim, which is what `run_log_dir` and `RunLogWriter.__init__` — whose body is already `str(job_id)` — have always done, and the annotations become `str`. For a caller passing a `UUID` object nothing changes, because `str(UUID)` is the same value the old route produced; for an unhyphenated string the write moves to where the reader looks, which is the defect being repaired and is declared rather than incidental. The now-unused `UUID` imports go in the same commit, because leaving them takes the repository's ruff count from 26 to 28 and `tests/orchestration/test_ci_budgets.py` freezes it at 26 — measured, not predicted. THE NEIGHBOURHOOD GOES WITH IT, per the rule a deletion round already binds: the `safe_points` paragraph and the `test_budget_tick` docstring state a CAUSE that this fix removes, so both are corrected in the same commit. DECISION F022 D2 clause one is NOT reversed — the route stays direct and the test still holds it there — only its stated reason is brought back into agreement with the code. THE GUARD: three tests in `tests/test_timeline.py`, one per half of the defect plus the round trip, each constructing through the REAL function. THE RULE THIS LEAVES BEHIND, binding on the next round that reads an id at a seam: a parameter annotated `A | B` states what it ACCEPTS, and a body that narrows to one of them makes the annotation a promise the function does not keep — so where two shapes meet, the seam is measured by CALLING it with each shape, never by reading its signature.
END-FIND51 ───────────────────────────────────────────────────

BEGIN-P51A_FROM ──────────────────────────────────────────────
from typing import Any
from uuid import UUID
END-P51A_FROM ────────────────────────────────────────────────

BEGIN-P51A_TO ────────────────────────────────────────────────
from typing import Any
END-P51A_TO ──────────────────────────────────────────────────

BEGIN-P51B_FROM ──────────────────────────────────────────────
    job_id: UUID | str,
END-P51B_FROM ────────────────────────────────────────────────

BEGIN-P51B_TO ────────────────────────────────────────────────
    job_id: str,
END-P51B_TO ──────────────────────────────────────────────────

BEGIN-P51C_FROM ──────────────────────────────────────────────
    Convenience wrapper around RunLogWriter for one-shot event recording.
    ``data_dir`` is the Remedy data root (e.g. ``.data/``).
    """
    jid = job_id if isinstance(job_id, UUID) else UUID(str(job_id))
    writer = RunLogWriter(jid, run_id=_PROCESS_RUN_ID, data_root=Path(data_dir))
END-P51C_FROM ────────────────────────────────────────────────

BEGIN-P51C_TO ────────────────────────────────────────────────
    Convenience wrapper around RunLogWriter for one-shot event recording.
    ``data_dir`` is the Remedy data root (e.g. ``.data/``).

    ``job_id`` is a STRING and is joined VERBATIM, because ``data_paths.run_log_dir``
    joins ``str(job_id)`` and :func:`load_run_events` below reads from exactly there.
    This function used to coerce with ``UUID(str(job_id))``, which rejected the
    sixteen hex characters ``data_paths.mint_job_id`` produces and, for an
    unhyphenated 32-hex id, wrote a directory its own reader never looked in
    (F275, finding R-0877).
    """
    writer = RunLogWriter(str(job_id), run_id=_PROCESS_RUN_ID,
                          data_root=Path(data_dir))
END-P51C_TO ──────────────────────────────────────────────────

BEGIN-P51D_FROM ──────────────────────────────────────────────
def load_run_events(data_dir: Path, job_id: UUID | str) -> list[dict[str, Any]]:
END-P51D_FROM ────────────────────────────────────────────────

BEGIN-P51D_TO ────────────────────────────────────────────────
def load_run_events(data_dir: Path, job_id: str) -> list[dict[str, Any]]:
END-P51D_TO ──────────────────────────────────────────────────

BEGIN-P51E_FROM ──────────────────────────────────────────────
    data_dir: Path, job_id: UUID | str,
END-P51E_FROM ────────────────────────────────────────────────

BEGIN-P51E_TO ────────────────────────────────────────────────
    data_dir: Path, job_id: str,
END-P51E_TO ──────────────────────────────────────────────────

BEGIN-P51F_FROM ──────────────────────────────────────────────
    jid = UUID(str(job_id)) if not isinstance(job_id, UUID) else job_id
END-P51F_FROM ────────────────────────────────────────────────

BEGIN-P51F_TO ────────────────────────────────────────────────
    jid = str(job_id)
END-P51F_TO ──────────────────────────────────────────────────

BEGIN-P51G_FROM ──────────────────────────────────────────────
from uuid import UUID, uuid4
END-P51G_FROM ────────────────────────────────────────────────

BEGIN-P51G_TO ────────────────────────────────────────────────
from uuid import uuid4
END-P51G_TO ──────────────────────────────────────────────────

BEGIN-P51H_FROM ──────────────────────────────────────────────
        job_id: UUID,
END-P51H_FROM ────────────────────────────────────────────────

BEGIN-P51H_TO ────────────────────────────────────────────────
        job_id: str,
END-P51H_TO ──────────────────────────────────────────────────

BEGIN-P51I_FROM ──────────────────────────────────────────────
    The writer is `RunLogWriter` and NOT `timeline.append_run_event` (DECISION F022
    D2, clause one): `append_run_event` resolves its id with `UUID(str(job_id))`,
    while a JobPlan's `job_id` is `uuid4().hex[:16]` — sixteen hex characters, which
    `UUID()` rejects. The short route would raise on every ping-pong safe point and
    the soft failure below would swallow it, leaving the ticker silently dead on the
    one job shape that runs long enough to need it.
END-P51I_FROM ────────────────────────────────────────────────

BEGIN-P51I_TO ────────────────────────────────────────────────
    The writer is `RunLogWriter` and NOT `timeline.append_run_event` (DECISION F022
    D2, clause one). The CAUSE D2 recorded is gone: `append_run_event` resolved its
    id with `UUID(str(job_id))`, which rejects the sixteen hex characters a
    JobPlan's `job_id` carries, and F275's finding R-0877 removed that coercion, so
    the short route no longer raises. The ruling stands on its other reason — this
    writer names its own run id — and the route is not changed here.
END-P51I_TO ──────────────────────────────────────────────────

BEGIN-P51J_FROM ──────────────────────────────────────────────
        A JobPlan's `job_id` is `uuid4().hex[:16]`, which `UUID()` rejects. Routing
        this emission through `timeline.append_run_event` would raise `ValueError`
        before the write, the soft failure would swallow it, and the ticker would be
        silently dead on the one job shape that runs long enough to need it.
END-P51J_FROM ────────────────────────────────────────────────

BEGIN-P51J_TO ────────────────────────────────────────────────
        A JobPlan's `job_id` is `uuid4().hex[:16]`, which `UUID()` rejects. Until
        F275's finding R-0877 removed the coercion, routing this emission through
        `timeline.append_run_event` raised `ValueError` before the write, the soft
        failure swallowed it, and the ticker was silently dead on the one job shape
        that runs long enough to need it. The route is still the direct one and this
        test still holds it there.
END-P51J_TO ──────────────────────────────────────────────────

BEGIN-GUARD51 ────────────────────────────────────────────────


class TestRunEventsAcceptTheShippedJobIdShape:
    """The run-log pair takes the id shape `mint_job_id` actually produces.

    DECISION F260 D2 rules a job id sixteen hex characters, and `mint_job_id`
    produces exactly that. `append_run_event` and `emit_failure_events` used to
    coerce with `UUID(str(job_id))`, which rejects it — a defect
    `safe_points._emit_budget_tick` documents and routes around rather than fixes.
    """

    def test_append_run_event_takes_the_shipped_job_id_shape(self, tmp_path):
        from packages.orchestration.data_paths import mint_job_id
        from packages.orchestration.timeline import append_run_event, load_run_events

        job_id = mint_job_id()
        assert len(job_id) == 16

        append_run_event(str(tmp_path), job_id, event="probe", metadata={"k": "v"})

        assert len(load_run_events(tmp_path, job_id)) == 1

    def test_emit_failure_events_takes_the_shipped_job_id_shape(self, tmp_path):
        from packages.orchestration.data_paths import mint_job_id
        from packages.orchestration.test_failure_artifact import (
            TestFailureArtifact,
            emit_failure_events,
        )
        from packages.orchestration.timeline import load_run_events

        job_id = mint_job_id()
        failure = TestFailureArtifact(job_id=job_id, safe_summary="one failing test")

        emit_failure_events(tmp_path, job_id, failure)

        events = load_run_events(tmp_path, job_id)
        assert [e["event"] for e in events] == ["test_failure_artifact_created"]

    def test_a_run_event_is_readable_by_the_reader_in_its_own_module(self, tmp_path):
        """The writer and the reader must name the SAME directory.

        `run_log_dir` joins `str(job_id)` verbatim, so a writer that normalises an
        unhyphenated 32-hex id to its canonical form writes where this module's own
        reader does not look.
        """
        from packages.orchestration.timeline import append_run_event, load_run_events

        job_id = "0" * 32

        append_run_event(str(tmp_path), job_id, event="probe", metadata={})

        assert len(load_run_events(tmp_path, job_id)) == 1
END-GUARD51 ──────────────────────────────────────────────────

BEGIN-LANDED51 ───────────────────────────────────────────────

Landed: R-0877 — both coercions removed and the id joined verbatim; the neighbourhood's two stale cause paragraphs corrected in the same commit; three guards added in `tests/test_timeline.py`, each red without the fix. All in this round's C3. The reviewer's authored `Done:` is owed at the next gate.
END-LANDED51 ─────────────────────────────────────────────────
