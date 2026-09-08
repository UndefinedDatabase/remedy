── STEP T001 — F275 ROUND 7 — THE SECOND MODULE GROUP ───────
Every horizontal rule line of this block is exactly 62 U+2500 BOX DRAWINGS LIGHT
HORIZONTAL characters, and the header line above ends in a run of 7 of them,
stated because a run of one repeated character has no length a reader recovers
by eye (§3 item 37). No other line of this block contains a run of U+2500.

Goal:
  Book round 6's PASS, rule the deletion order a CERTIFICATE rather than a queue,
  and DELETE the `worker_recommend` module group as one commit that leaves the
  tree green.

Base: d4402dc268f0786d25d5da341db08c7884efc807

Bundle, in this order; no commit is added, dropped or reordered:
  C0a  save this block verbatim to `.agent/authored/f275-r7.md`
  C0b  mirror the same bytes to `.agent/last_block.md`
  C1   replace `.agent/plan.md` whole with PLAN7
  C2   append RECORD7 to `.agent/live_review.md` and SLIPS7 to
       `.agent/prose_slips.md` — ONE commit, two files
  C3   append DECISION7 to `.agent/decisions.md`
  C4   THE DELETION — the worker_recommend module group, ONE commit
  C5   run every gate G1..G8. Writes no file. Has no commit.
  C6   rewrite `.agent/handoff.md` and commit it last

C3 precedes C4 on purpose: DECISION F275 D3 is what authorises C4 to take this
group ahead of the order file's first line, so the ruling lands before the act.

Change: the paths below and nothing else. Resolve the count from this list; the
block states no numeral for it.
  `.agent/authored/f275-r7.md`                              C0a  added
  `.agent/last_block.md`                                    C0b  replaced
  `.agent/plan.md`                                          C1   replaced
  `.agent/live_review.md`                                   C2   appended
  `.agent/prose_slips.md`                                   C2   appended
  `.agent/decisions.md`                                     C3   appended
  `packages/orchestration/worker_recommend.py`              C4   DELETED
  `apps/cli/commands/worker_recommend_cmd.py`               C4   DELETED
  `apps/cli/commands/__init__.py`                           C4   edited
  `apps/cli/command_catalog.py`                             C4   edited
  `docs/system/worker-registry-route-policy-v0.md`          C4   edited
  `scripts/remedy_smoke.sh`                                 C4   edited
  `tests/orchestration/import_reachability_allowlist.txt`   C4   edited
  `tests/orchestration/test_cluster_deletion_map.py`        C4   edited
  `tests/orchestration/test_command_discovery.py`           C4   edited
  `tests/storage/test_persistence.py`                       C4   edited
  `tests/test_remedy_smoke_script.py`                       C4   edited
  `.agent/f275_deletion_order.md`                           C4   regenerated
  `.agent/handoff.md`                                       C6   replaced

──────────────────────────────────────────────────────────────
WHAT THE REVIEWER MEASURED BEFORE WRITING THIS BLOCK

The reviewer APPLIED this entire deletion in a disposable worktree at the base
above, committed it there, and ran the suites, before authoring a line of C4.

C4's per-file `git diff --numstat` in that worktree was, and yours should be:

      1   2   .agent/f275_deletion_order.md
      0  22   apps/cli/command_catalog.py
      1   2   apps/cli/commands/__init__.py
      0 109   apps/cli/commands/worker_recommend_cmd.py
      2   2   docs/system/worker-registry-route-policy-v0.md
      0 170   packages/orchestration/worker_recommend.py
      1  23   scripts/remedy_smoke.sh
      0   2   tests/orchestration/import_reachability_allowlist.txt
      1   3   tests/orchestration/test_cluster_deletion_map.py
      0  24   tests/orchestration/test_command_discovery.py
      0  39   tests/storage/test_persistence.py
      0  15   tests/test_remedy_smoke_script.py

Report YOUR columns beside these and DECLARE any cell that differs rather than
editing toward the table: it is the reviewer's reading of one possible correct
application, not a target to hit. A different but green application is a
declared deviation, not a failure.

TRAP 1 — AN AST IMPORTER SWEEP IS NECESSARY AND NOT SUFFICIENT. Two of this
group's consumers never import it. `scripts/remedy_smoke.sh` drives
`remedy worker recommend` and `remedy worker explain` as SHELL COMMANDS, and
`tests/test_remedy_smoke_script.py` reads that script as TEXT and asserts both
strings are in it; `tests/orchestration/test_command_discovery.py` runs
`python -m apps.cli.grouped worker explain --help` in a SUBPROCESS. The reviewer
found the last of these only by running the suite: pruning by import alone left
`TestWorkerExplain::test_explain_cli_help` red at `1 failed, 580 passed`.

TRAP 2 — THE COMMENT ROUND 6 REPAIRED IS STALE AGAIN. Round 6 rewrote the comment
above `CLUSTER_COMMAND_HANDLERS` in `tests/orchestration/test_cluster_deletion_map.py`
to read "`context_pack_cmd.py` and `worker_recommend_cmd.py` for exactly that
reason." This round deletes the second of those two files, so the same sentence
is falsified a second time and is repaired again in the same commit.

TRAP 3 — THE ORDER FILE IS REGENERATED, NEVER LINE-EDITED, exactly as in round 6.
After this group it holds THIRTEEN components and `context_pack` is first, because
`worker_recommend` was its only remaining cluster importer.

WHAT MUST NOT BE TOUCHED, each for a measured reason. `README.md` line 111 and
`docs/roadmap/features/T2_F260.md`, `T2_F272.md` and `T2_F274.md` all name
`worker_recommend`: the first is a closed feature's narrative and the other three
are the SPECIFICATION of what is to be deleted, kept unedited on purpose.
`packages/orchestration/token_policy.py` carries a comment saying DECISION F274 D7
moved a function out of `worker_recommend`, "which dies" — that sentence stays TRUE
after this round and is not edited. `tests/STEP_TEST_MIGRATION.md` is a historical
migration table and is not maintained against live class names.

WITH ALL OF THE ABOVE APPLIED AND COMMITTED, the reviewer's worktree ran the full
suite SERIALLY over the families that had failed under `-n auto` and measured
EXIT 0 at 121 passed. Under `-n auto` the same tree gives 12 failures — the
`ui_server` command-channel tests racing for a server port, the vitest node, and
one subprocess-cleanup test — and all 12 are the runner, not the change. THE FULL
SUITE OF G7 IS THEREFORE RUN SERIALLY.

──────────────────────────────────────────────────────────────
C4 — THE DELETION, IN FULL

(1) `git rm` both files whole:
      packages/orchestration/worker_recommend.py
      apps/cli/commands/worker_recommend_cmd.py

(2) `apps/cli/commands/__init__.py` — two sites, as in round 6: delete the whole
    line `        worker_recommend_cmd,` from the import block, and in the single
    long `for mod in (...)` tuple delete the substring `, worker_recommend_cmd,`
    and put back `,`. Each occurs exactly once.

(3) `apps/cli/command_catalog.py` — delete the two `CommandEntry(...)` blocks
    whose `command_id` values are `"worker.recommend"` and `"worker.explain"`,
    each together with the ONE blank line that follows it. They are NOT adjacent —
    the surviving `worker.show` entry sits between them — so this is two separate
    deletions. No SURVIVING entry references either id: the only `related` tuple
    naming `worker.recommend` belongs to the `worker.explain` entry being deleted,
    which the reviewer measured. `worker.list`, `worker.show` and `worker.resources`
    all stay.

(4) `scripts/remedy_smoke.sh` — remove both steps the deleted commands drove:
    (a) the `# Worker recommend` block: its comment line, the `WORKER_JSON=` line
        and the whole `python3 -c "..."` heredoc that validates the JSON, ending
        at the line `" "${WORKER_JSON}"`, plus the blank line that preceded the
        comment.
    (b) the `12w` section: its `_SMOKE_SECTION` assignment, its `echo` line and
        the `remedy worker explain` line, plus the blank line that preceded it.
    (c) the surviving heading above section `12v` reads `# Step 64: Worker show +
        explain` and must become `# Step 64: Worker show`, because the explain
        half no longer exists.
    Section `12v` (`Worker show ollama`) SURVIVES untouched.

(5) `tests/test_remedy_smoke_script.py` — delete the three test functions that
    assert the script still calls the deleted commands:
    `test_smoke_has_worker_recommend`, `test_smoke_worker_recommend_checks_schema`
    and `test_smoke_has_worker_explain`. Delete each whole, decorators included.

(6) `tests/orchestration/test_command_discovery.py` — delete the whole
    `class TestWorkerExplain:` and, in the rest of the file, every import of
    `packages.orchestration.worker_recommend` together with the whole enclosing
    test function of every use of a name that import bound. A class left with an
    empty body is a syntax error, so a class whose every method dies goes whole.

(7) `tests/storage/test_persistence.py` — the same treatment: the imports of
    `packages.orchestration.worker_recommend` and the whole enclosing test
    function of every use, with an emptied class going whole. The reviewer's
    application removed 39 lines here and 24 in (6), both counts including the
    class removals.

(8) `tests/orchestration/import_reachability_allowlist.txt` — delete the two whole
    lines `apps.cli.commands.worker_recommend_cmd` and
    `packages.orchestration.worker_recommend`. Do not re-sort the file.

(9) `tests/orchestration/test_cluster_deletion_map.py` — three sites: delete
    `    "packages.orchestration.worker_recommend",` from `CLUSTER_MODULES`,
    delete `    "apps/cli/commands/worker_recommend_cmd.py",` from
    `CLUSTER_COMMAND_HANDLERS`, and repair TRAP 2's comment — the line
    "# `context_pack_cmd.py` and `worker_recommend_cmd.py` for exactly that reason."
    becomes "# `context_pack_cmd.py` for exactly that reason."

(10) `docs/system/worker-registry-route-policy-v0.md` — one stale sentence. It
     lists a pre-existing group as `worker_adapters.py` / `worker_recommend.py` /
     `worker_queue.py`; the middle member is being deleted, so the list loses it
     and the sentence keeps its meaning. Change nothing else in that file, and add
     no status banner: the page's subject is the Worker Registry, not this module.

(11) `.agent/f275_deletion_order.md` — REGENERATE the body, header untouched, by
     the SAME recipe round 6 used and after (1) to (10) are applied on disk:

         import pathlib, sys
         sys.path.insert(0, str(pathlib.Path.cwd()))
         from tests.orchestration.test_cluster_deletion_order import ORDER_PATH, measured_order
         lines = ORDER_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
         header = [ln for ln in lines if ln.startswith("#")]
         body = "".join(", ".join(c) + "\n" for c in measured_order())
         ORDER_PATH.write_text("".join(header) + body, encoding="utf-8")

──────────────────────────────────────────────────────────────
Constraints:

 1. Apply every authored slice BYTE FOR BYTE. Do not reflow, re-wrap, re-sort or
    tidy any of them. If a slice contradicts a gate, apply the slice, run the
    gate, and DECLARE the disagreement — never repair it silently.
 2. Destructive verification runs ONLY inside a `git worktree` you create and
    remove BY ITS EXACT PATH; `git status --porcelain` is empty at every commit
    boundary and at the handback.
 3. Bare `ruff` is denied to this session; every gate orders
    `python3 -m ruff check <path>`.
 4. Append convention for C2 and C3, used by every appended file: the existing
    bytes, then ONE `\n`, then the slice's own bytes, which already end in a
    newline. Nothing else is inserted and nothing existing is rewritten.
 5. C2's two appends are ONE commit. C3 is ONE commit and one file. C4 is ONE
    commit and contains no `.agent/` path except `.agent/f275_deletion_order.md`.
 6. No finding is minted and none is resolved. RECORD7 is a `Gate:` entry and
    matches neither the registration nor the resolution pattern, so the open set
    does not move. The next free id is R-0841 and this round does not spend it.
 7. C4 touches `docs/`, so G6 gates `tests/docs/` and
    `tests/orchestration/test_roadmap_index.py` beside the ratchets.
 8. G8 runs LAST, after G1..G7. Its commit-sequence clause names commits up to
    and including C4 — the reading it can honestly take before C6 exists — and
    the range readings over the FULL round are re-taken after C6 and reported
    beside the first set, which is the two-readings answer §3 item 14 prescribes.

──────────────────────────────────────────────────────────────
Done when — EIGHT GATES, every one RUN, every real exit code reported:

G1 TRANSPORT. sha256 and byte count of the committed `.agent/authored/f275-r7.md`
   and `.agent/last_block.md`. Both must be ONE value. Per §3 item 37 this chain
   covers the saved copy and its mirror and claims nothing about emitted bytes.

G2 THE PLAN. `.agent/plan.md` byte-identical to PLAN7: 2394 bytes, 41 lines,
   sha256 `eccc004fb785bd65b6f416ba5c69ff50d959afcd8888f508021d060d5ab191d0`.
   Report the line count against the AGENTS.md cap of 50, and that `^## Goal$`
   and `^## Next Steps$` each occur once.

G3 THE RECORD. Over `.agent/live_review.md` and `.agent/prose_slips.md`:
   (a) BYTES. live_review 536113 -> 541694, gain 5581 = 1 + 5580.
       prose_slips 171102 -> 172799, gain 1697 = 1 + 1696.
   (b) EDGES. For each, the pre-commit blob is a byte-exact PREFIX and the ONE
       `\n` plus the slice is a byte-exact SUFFIX.
   (c) ORDERED EQUALITY. Count N from the SLICE with your own reader, never from
       this block, and compare the file's last N blank-line units against the
       slice's N paragraphs IN ORDER. Report the N you counted.
   (d) NEGATIVE CONTROL, IN MEMORY ONLY, on the FIRST appended paragraph of EACH
       file: flip one byte inside it, confirm the readers of (b) and (c) both
       REJECT the mutant, then re-read the tracked file and report its size
       unchanged.
   (e) COUNTS. live_review units 221 -> 222, `^Gate: ` 28 -> 29,
       `^Gate: F275 R6 ` 0 -> 1. prose_slips units 242 -> 246.
   (f) THE OPEN SET DOES NOT MOVE. Distinct `^- R-\d+ — ` ids 69 -> 69; distinct
       `^Done: R-\d+ — ` ids 3 -> 3; OPEN BY DISTINCT ID 66 -> 66. Subtract
       DISTINCT IDS, never raw `Done:` lines.

G4 THE DECISION. `.agent/decisions.md` 947292 -> 953044, gain 5752 = 1 + 5751;
   pre-image a byte-exact PREFIX and the newline plus DECISION7 a byte-exact
   SUFFIX; a negative control in memory on the FIRST appended paragraph rejected
   by both readers with the tracked size unchanged; `^## DECISION F275 D` 2 -> 3
   and `^## DECISION F275 D3 ` heading exactly one section.

G5 THE DELETION IS COMPLETE. Report each, using `git grep` over the TRACKED tree
   so that build caches and ignored artefacts cannot answer for the source:
   - `git ls-tree` at the tip finds neither
     `packages/orchestration/worker_recommend.py` nor
     `apps/cli/commands/worker_recommend_cmd.py`.
   - `recommend_worker`, `worker.recommend` and `worker.explain` are each at ZERO
     over tracked files outside `.agent/`.
   - `worker recommend` and `worker explain` as SHELL strings are each at ZERO in
     `scripts/` and `tests/`.
   - `worker_recommend` survives ONLY in `README.md`,
     `docs/roadmap/features/T2_F260.md`, `T2_F272.md`, `T2_F274.md`,
     `packages/orchestration/token_policy.py`,
     `tests/orchestration/test_cluster_deletion_map.py` and
     `tests/STEP_TEST_MIGRATION.md`. Print every hit and confirm the set.

G6 THE RATCHETS, THE DOCS AND THE DISPATCH TABLE, in the PRIMARY checkout:
   - `python3 -m pytest tests/orchestration/test_import_reachability.py
     tests/orchestration/test_cluster_deletion_map.py
     tests/orchestration/test_cluster_deletion_order.py -q` — reviewer measured
     9 passed.
   - `python3 -m pytest tests/docs/ tests/test_test_categories.py
     tests/orchestration/test_roadmap_index.py -q` — reviewer measured 345 passed.
   - through the SHIPPED readers `apps.cli.commands.collect_all_handlers` and
     `apps.cli.command_catalog._BASE_CATALOG`, report both sizes and whether
     `worker.recommend`, `worker.explain`, `worker.list` and `worker.show`
     resolve. The reviewer measured 338 and 338 at the base, 336 and 336 after,
     with the first two absent and the last two present.
   - print the regenerated body of `.agent/f275_deletion_order.md` in full and
     report its component count.

G7 RUFF AND THE FULL SUITE.
   - `python3 -m ruff check apps/cli/commands/__init__.py apps/cli/command_catalog.py
     tests/orchestration/test_command_discovery.py tests/storage/test_persistence.py
     tests/orchestration/test_cluster_deletion_map.py tests/test_remedy_smoke_script.py`
     — the reviewer measured "All checks passed!".
   - the FULL suite in the PRIMARY checkout, SERIALLY: `python3 -m pytest tests/ -q`,
     with NO `-n auto`. Report the real counts and exit code. The base at
     `d4402dc2` measured 19768 passed and 23 skipped; this round removes tests, so
     the number MUST fall — report what it is and do not adjust anything to reach
     a prediction, because the reviewer states none.

G8 THE TREE, run LAST.
   - `.agent/STOP` does not exist; `git status --porcelain` is empty; the branch is
     `feature/f275-one-world-completion-part-three`; `git worktree list` shows only
     the primary checkout.
   - `git diff --name-only d4402dc2..<tip>` equals the block's path list exactly.
   - every commit in the range is single-parent, in the ordered sequence C0a, C0b,
     C1, C2, C3, C4, C6, with no C5 commit.
   - report each commit's insertion count against the DECISION F104 D1 cap of 500.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — the
state block naming SESSION 3 of F275 and round 7, the changed-files table with
real `git diff --numstat` columns, ONE LINE PER GATE with its real exit code, the
item-status table covering C0a, C0b, C1, C2, C3, C4, C5, C6 and G1..G8, the
deviations, and the Fortschritt line. Name `review_bundle` as the DEFERRED group,
per DECISION F275 D3, so no later session reads the deferral as an oversight.
C6 cannot table its own numstat columns; report them to the reviewer instead of
writing a guess into the file. The handback has no length cap.
──────────────────────────────────────────────────────────────

=== BEGIN PLAN7 sha256=eccc004fb785bd65b6f416ba5c69ff50d959afcd8888f508021d060d5ab191d0 bytes=2394 ===
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 7 books round 6's PASS and deletes the SECOND module group, `worker_recommend` — the
module, its handler, its two catalog entries, the two smoke-script steps that drove them and
the guards asserting those steps, the surviving test call sites, and one stale sentence in an
ist-doc. DECISION F275 D3 rules that the recorded order is a valid topological order rather
than a mandated sequence, which is why this group is taken before `review_bundle`.

## Next Steps

1. `context_pack`, which this round's regeneration makes the order file's first line.
2. `review_bundle`, deferred by DECISION F275 D3 and needing a session of its own: 2254 lines,
   sixteen surviving test importers, eight `docs/system/` pages, `pyproject.toml` and a script.
3. The remaining components in the recorded order, the multi-module ones as single commits
   because their members import each other.
4. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831
   and R-0840 named among the ideas deleted rather than inherited.
5. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- 66 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only. Rounds 6 and 7 both measured that
  gap for real: a UI catalog pinned to the Python emitters, and a smoke script plus its guards
  that drive a command by STRING. An AST importer sweep is necessary and not sufficient.
- The full suite is run SERIALLY. Under `pytest -n auto` the `ui_server` command-channel tests
  race for a server port and the vitest node needs `apps/ui/node_modules`; round 7 measured 12
  such failures in parallel and 0 in the same worktree run serially.
=== END PLAN7 ===

=== BEGIN RECORD7 sha256=47fb88c19ae47b0b5f353376f3e8052393fd9f36e755e92c3c82eea7bf3798d7 bytes=5580 ===
Gate: F275 R6 — the F275 round 6 entry. VERDICT PASS, booked by round 7 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1. THIS ROUND PERFORMED THE FIRST `git rm` OF THE PROTOTYPE-CLUSTER DELETION, which F260, F272 and F274 each carried as their last slice and each closed before reaching. EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF against the committed blobs, in the primary checkout, and not one number below is taken from the worker's report. The range is `a1df5d70b09cf30e2519a44d8c4686f06f6e9a6b`..`d4402dc268f0786d25d5da341db08c7884efc807`, six commits — C0a `3bad8eea`, C0b `e16aff01`, C1 `717fd1e4`, C2 `9b698482`, C3 `57caf5a0`, C5 `d4402dc2` — every one single-parent by `git rev-list --parents`, with no C4 commit, and `git diff --name-status` over that range naming exactly the fifteen declared paths. G1 TRANSPORT: the reviewer's own scratch original `.remedy-wt/f275-r6-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f275-r6.md` and `.agent/last_block.md` are all 26012 bytes at `689b75aba03bfa19730fb9cace7495290cc9341fbd48046d99a62b2b0748be99`; per §3 item 37 that chain covers those three artefacts and claims nothing about emitted bytes. G2: `.agent/plan.md` byte-identical to the authored PLAN6 at 2244 bytes and 40 lines. G3 THE RECORD, re-derived from the committed blobs: `.agent/live_review.md` 533079 to 536113, gain 3034 = 1 + 3033, the pre-image a byte-exact PREFIX and one newline plus the slice a byte-exact SUFFIX, units 220 to 221, `^Gate: ` 27 to 28, `^Gate: F275 R5 ` 0 to 1; `.agent/prose_slips.md` 169429 to 171102, gain 1673 = 1 + 1672, units 237 to 242; N counted from each slice by the reviewer's own reader as 1 and 5, ordered equality holding for both; and THE OPEN SET UNCHANGED AT 66 BY DISTINCT ID, 69 registrations against 3 resolutions. G4 THE DELETION IS COMPLETE: `packages/orchestration/context_optimizer.py` and `apps/cli/commands/context_optimizer_cmd.py` are absent from `git ls-tree` at the tip, and `explain_context`, `optimize_context`, `context.explain`, `context.optimize`, `_cmd_context_explain` and `_cmd_context_optimize` are each at ZERO over the tracked tree outside `.agent/`. G5: the three ratchets 9 passed, `tests/ui_contracts/` 809 passed and 4 skipped, and through the shipped reader `apps.cli.commands.collect_all_handlers` the dispatch table is 338 where the base measured 340, with `context.explain` and `context.optimize` absent and `context.inspect` and `context.pack` present; the catalog carries ZERO surviving `command_id` or `related` references to either dead id, and `context.inspect` now reads `related=('context.pack',)`. The regenerated `.agent/f275_deletion_order.md` holds 14 components, produced by the SHIPPED `measured_order()`. G6: ruff "All checks passed!" on the four touched Python files, and the FULL SUITE RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT is EXIT 0 at 19768 passed and 23 skipped with ZERO failures, against the reviewer's own pre-emission dry run of the identical deletion which measured the same 19768 and 23. G7: `git status --porcelain` empty, `git worktree list` showing only the primary checkout, `.agent/STOP` absent, and every commit's insertion count — 352, 322, 16, 12, 5, 342 — under the DECISION F104 D1 cap of 500. THE REVIEWER'S PRE-EMISSION DRY RUN IS WHY THIS ROUND PASSED FIRST TIME, and it is recorded here because the three traps it caught are invisible to the deletion map and would each have shipped the branch RED. FIRST, the deletion order file must be REGENERATED and not line-edited: removing the module removes its edges and `measured_order()` then moves `worker_recommend` from fourth place to second and `context_pack` from sixth to third, so striking one line reds `test_the_recorded_order_equals_the_measured_condensation`. SECOND, `tests/ui_contracts/test_humanize_catalog.py` pins the UI humanize catalog's keys to the Python emitters by an AST walk, so deleting the only emitter of `context_budget_optimized` while leaving its catalog entry fails with "in the catalog but NOT emitted"; the entry went with the emitter, and historical events still render because that file's own header rules an absent kind rendered generically. THIRD, two neighbours of that entry MUST NOT be touched and the reason is measured rather than argued: `packages/orchestration/event_schemas.py` keeps its schema key because `tests/orchestration/test_event_ledger.py` asserts that key is present, and `apps/ui/src/api/actionClass.ts` keeps its bookkeeping entry because nothing pins that list to the emitters and it classifies events already written to disk. SEVEN DEVIATIONS WERE DECLARED AND ALL SEVEN ARE SUSTAINED; four are the reviewer's own block prose and are dated `.agent/prose_slips.md` lines rather than ids, per amend0827 rule 2, because not one put anything wrong on disk. Two deserve the record because the worker's instrument was better than the one ordered: G4's grep exclusion set did not exclude build caches, so the worker answered the question with `git grep` over the TRACKED tree and classified the residue with `git check-ignore`, finding exactly one non-ignored hit, `docs/roadmap/features/T2_F260.md`, which constraint 6 keeps as the specification of what is to be deleted; and G4's "exactly three hits" for `context_budget_optimized` counted FILES while the real reading is six line hits in those three files. NO FINDING IS MINTED BY THIS GATE and none is resolved; the open set stands at 66 by distinct id and the next free id is R-0841.
=== END RECORD7 ===

=== BEGIN SLIPS7 sha256=bae8cbc2f5f6297cddce70a59b4fdac0e4bacedc04d70eb912fe91784cb65060 bytes=1696 ===
2026-09-08 · F275 R6 · The round 6 block's gate G4 ordered a repo-wide grep "excluding `.git/`, `.data/`, `.agent/` and `.remedy-wt/`" and named no build cache, so run literally it also reads `__pycache__`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `.coverage_reports/` and `.brain/`, which hold stale artefacts of the very code being deleted; the worker answered the question with `git grep` over the TRACKED tree and classified the residue with `git check-ignore`, which is the instrument the gate should have named.

2026-09-08 · F275 R6 · The round 6 block's gate G4 predicted `context_budget_optimized` at "EXACTLY THREE hits" while its own sentence enumerated three FILES; the real reading is six LINE hits in those three files, four of them in `tests/orchestration/test_event_ledger.py`, so the numeral counted the wrong unit and the property it stood for held exactly as written.

2026-09-08 · F275 R6 · The round 6 block's gate G5 predicted `tests/ui_contracts/` at "808 passed and 5 skipped", a reading the reviewer had taken in its own dry worktree; the primary checkout the gate orders reads 809 passed and 4 skipped, the same total of 813, the difference being one legacy-`.tsx` quarantine skip that resolves differently in a fresh worktree.

2026-09-08 · F275 R6 · The round 6 block's gate G7 was ordered to "run LAST, after G1..G6" and before C5, while its own sequence clause required it to see the commit sequence "C0a, C0b, C1, C2, C3, C5" — a commit that does not exist when the gate runs; the worker obeyed the ordering, reported the reading at C3, and re-ran the two range readings after C5, which is the two-readings answer §3 item 14 already prescribes.
=== END SLIPS7 ===

=== BEGIN DECISION7 sha256=09959a2495842786523270b3dd422bb92474289a279841471c2ed593bac3a9cd bytes=5751 ===
## DECISION F275 D3 — `.agent/f275_deletion_order.md` is a VALID TOPOLOGICAL ORDER, not a mandated sequence; a component no surviving cluster module imports may be deleted in any round, and `review_bundle` is deferred on measured size (2026-09-08)

CONTEXT. DECISION F275 D2 ruled the atomic unit of the deletion to be the strongly connected component and had the order generated from the live import graph into `.agent/f275_deletion_order.md`. That file's own header says "Lines are executed top to bottom", and after round 6 its first line was `packages.orchestration.review_bundle`. Read strictly, that sentence orders round 7 to delete `review_bundle` next. The question this decision settles is whether the recorded order BINDS the sequence or merely CERTIFIES that the sequence is safe.

THE MEASUREMENT, taken by the reviewer at `d4402dc268f0786d25d5da341db08c7884efc807` by running the SHIPPED `internal_dependencies()` and `measured_order()` rather than by reading the file. `measured_order()` builds the condensation and then repeatedly appends the whole SORTED SET of components that nothing remaining imports — it is a layered order, so every component in one layer is free SIMULTANEOUSLY and their relative positions are an alphabetical tie-break carrying no dependency meaning. At that commit `review_bundle` is imported by NO cluster module and imports nineteen of them; `worker_recommend` is imported by NO cluster module and imports only `context_pack`; `context_pack` imports nothing and is imported by `worker_recommend` alone. So `review_bundle` and `worker_recommend` are both free, neither imports the other, and deleting either first leaves no dangling import. The sizes are not comparable: `review_bundle.py` is 2254 lines with SIXTEEN surviving test importers, eight `docs/system/` pages, a `pyproject.toml` per-file ignore, a `pyproject.toml` list entry and a shell script naming its runtime test; `worker_recommend.py` is 170 lines with TWO surviving test importers and one stale ist-doc sentence.

CHOSEN. The recorded order is a CERTIFICATE, not a queue. A round may delete any component that no surviving cluster module imports — which is exactly the set `measured_order()` puts in its first layer — and the file is REGENERATED in that same commit, so the certificate stays true after every group. `review_bundle` is therefore DEFERRED to a session that can carry it whole, and round 7 takes `worker_recommend`. The order file's header sentence "Lines are executed top to bottom" is left UNEDITED, because it is still the right instruction for a reader with no reason to choose otherwise, and this decision is the recorded reason.

WHY, and why this is a ruling rather than a question to the operator. Operator RULE 2 states its own purpose in the same sentence that states the order — "so that each group commit leaves no dangling import" — and that property is a fact about the import graph, not about line numbers in a generated file. Any first-layer component satisfies it. Reading the file as a queue would additionally forbid something RULE 1 explicitly permits, since RULE 1 makes ONE MODULE GROUP the atomic unit and lets sessions and rounds end between group commits; a queue reading would make the largest group block every smaller one behind it. And the alternative to deferring `review_bundle` is worse than a reordering: its group would have to be split across sessions to fit, and "never split" binds INSIDE a group commit by RULE 1 and by the F274 Orchestrator brief, so a session that starts it without being able to finish it is the one state this work must not leave behind. Deferring costs nothing measurable — the certificate is regenerated either way — while starting it half-prepared costs the invariant.

ALTERNATIVES CONSIDERED AND REJECTED. (1) Delete `review_bundle` in round 7 as the file's first line orders. Rejected on the measurement above: its group reaches sixteen surviving test files, eight ist-docs whose subject is the mechanism being deleted, `pyproject.toml` and `scripts/remedy_test_runtime.sh`, and the docs question alone is a round's work. (2) Re-sort the order file so the cheapest free component is always first. Rejected because the file is GENERATED and a hand-imposed tie-break would be the "prose inventory that nothing re-measures" its neighbour `test_cluster_deletion_map.py` exists to prevent; the tie-break belongs in the ROUND's choice, not in the artefact. (3) Change `measured_order()` to sort each layer by size. Rejected as production churn for a reviewer's convenience, and it would make the order depend on line counts that every deletion changes. (4) Ask the operator. Rejected under docs/agents/planner_reviewer_prompt.md §4 item 7: the rules answer this, so the decision is loud, persisted and reversible rather than a question that costs a session.

CONSEQUENCE. Round 7 deletes `worker_recommend`. After its regeneration the order file holds THIRTEEN components with `context_pack` first, because `worker_recommend` was its only remaining cluster importer. `review_bundle` remains in the certificate and is taken by the first session that can carry it whole; the handback names it as the deferred group so that no later session mistakes the deferral for an oversight. Nothing about RULE 2, DECISION F275 D2 or the ratchet changes, and `tests/orchestration/test_cluster_deletion_order.py` continues to hold the file against the graph in both directions after every group commit.

REVERSE by deleting this section. The order file is regenerated by every group commit regardless, so reversal restores the queue reading without leaving any artefact inconsistent; a session reversing it deletes `review_bundle` next and takes the size with it.
=== END DECISION7 ===
