── STEP T001 — F275 ROUND 6 — THE FIRST git rm ──────────────
Every horizontal rule line of this block is exactly 62 U+2500 BOX DRAWINGS LIGHT
HORIZONTAL characters, and the header line above ends in a run of 14 of them,
stated here because a run of one repeated character has no length a reader
recovers by eye (§3 item 37). Three lines of C3 QUOTE a comment banner out of a
source file; each of those is identified below by a PREFIX that occurs exactly
once in its file, so no U+2500 run has to be retyped to find it. The banners
themselves are never edited and never re-drawn.

Goal:
  Book round 5's PASS, and DELETE the first prototype-cluster module group —
  `packages.orchestration.context_optimizer` — as one commit that leaves the tree
  green. This is the first `git rm` of F275 and of the three features that carried
  this deletion before it.

Base: a1df5d70b09cf30e2519a44d8c4686f06f6e9a6b

Bundle, in this order, and no commit is added, dropped or reordered:
  C0a  save this block verbatim to `.agent/authored/f275-r6.md`
  C0b  mirror the same bytes to `.agent/last_block.md`
  C1   replace `.agent/plan.md` whole with PLAN6
  C2   append RECORD6 to `.agent/live_review.md` and SLIPS6 to
       `.agent/prose_slips.md` — ONE commit, two files
  C3   THE DELETION — the context_optimizer module group, ONE commit
  C4   run every gate G1..G7. Writes no file. Has no commit.
  C5   rewrite `.agent/handoff.md` and commit it last

Change: the paths below and nothing else. Resolve the count from this list; the
block states no numeral for it.
  `.agent/authored/f275-r6.md`                              C0a  added
  `.agent/last_block.md`                                    C0b  replaced
  `.agent/plan.md`                                          C1   replaced
  `.agent/live_review.md`                                   C2   appended
  `.agent/prose_slips.md`                                   C2   appended
  `packages/orchestration/context_optimizer.py`             C3   DELETED
  `apps/cli/commands/context_optimizer_cmd.py`              C3   DELETED
  `apps/cli/commands/__init__.py`                           C3   edited
  `apps/cli/command_catalog.py`                             C3   edited
  `apps/ui/src/api/humanizeCatalog.ts`                      C3   edited
  `tests/orchestration/test_project_brain.py`               C3   edited
  `tests/orchestration/import_reachability_allowlist.txt`   C3   edited
  `tests/orchestration/test_cluster_deletion_map.py`        C3   edited
  `.agent/f275_deletion_order.md`                           C3   regenerated
  `.agent/handoff.md`                                       C5   replaced

──────────────────────────────────────────────────────────────
WHAT THE REVIEWER MEASURED BEFORE WRITING THIS BLOCK

The reviewer APPLIED this entire deletion in a disposable worktree at the base
above, committed it there, and ran the suites, before authoring a line of C3.
Three traps were found that way and each is ordered explicitly below. None of the
three is visible by reading the deletion order file or the deletion map.

TRAP 1 — THE ORDER FILE MUST BE REGENERATED, NOT LINE-EDITED. Deleting the module
removes its edges, and `measured_order()` in
`tests/orchestration/test_cluster_deletion_order.py` then puts the SURVIVING
components in a different order: `worker_recommend` moves from the fourth line to
the second and `context_pack` from the sixth to the third. Striking only the
`packages.orchestration.context_optimizer` line reds
`test_the_recorded_order_equals_the_measured_condensation`, which the reviewer
reproduced: `1 failed, 8 passed`, the failure naming index 1. C3 therefore rewrites
the file's BODY from the live graph and leaves its comment header byte-identical.

TRAP 2 — THE HUMANIZE CATALOG IS PINNED TO THE PYTHON EMITTERS. `context_budget_optimized`
is emitted by `_cmd_context_optimize` and by nothing else, and
`tests/ui_contracts/test_humanize_catalog.py::TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary`
derives the emitter set with an AST walk and compares it to the catalog's keys.
Deleting the handler while leaving the catalog entry ships the branch RED; the
reviewer reproduced exactly that — `in the catalog but NOT emitted (1):
['context_budget_optimized']` — and confirmed the whole `tests/ui_contracts/`
suite green once the entry goes. Historical events do not lose their rendering:
that file's own header states that a kind absent from the map is rendered
generically by `humanize.ts`.

TRAP 3 — TWO NEIGHBOURS OF THAT ENTRY MUST NOT BE TOUCHED, and the reason is
measured rather than argued. `packages/orchestration/event_schemas.py` keeps its
`"context_budget_optimized"` entry, because
`tests/orchestration/test_event_ledger.py` asserts that key is PRESENT in
`EVENT_METADATA_SCHEMAS` and deleting it reds that suite.
`apps/ui/src/api/actionClass.ts` keeps its `BOOKKEEPING_KINDS` entry, because
nothing pins that list to the emitters and it classifies events already written to
disk. After C3 those are the only two occurrences of the kind left in the tree.

ONE MORE READING, so the worker is not surprised by it: while the deletion is
UNCOMMITTED, `tests/orchestration/test_evidence_index.py::TestPorcelainParsing::test_every_enumerated_path_exists_in_this_repo`
fails, because `dirty_source_test_files` enumerates the deleted paths out of
`git status --porcelain` and then asserts each exists. It passes the moment C3 is
committed and the tree is clean. The reviewer verified both halves. Do not "fix"
that test.

WITH ALL OF THE ABOVE APPLIED AND COMMITTED, the reviewer's worktree ran the FULL
suite at EXIT 0 with 19768 passed and 23 skipped, and a base control at the same
commit showed no failure that the deletion introduced.

──────────────────────────────────────────────────────────────
C3 — THE DELETION, IN FULL

(1) `git rm` both files whole:
      packages/orchestration/context_optimizer.py
      apps/cli/commands/context_optimizer_cmd.py

(2) `apps/cli/commands/__init__.py` — two sites, both losing the same name:
    (a) delete the whole line `        context_optimizer_cmd,` from the import
        block. It occurs exactly once.
    (b) in the single long `for mod in (...)` tuple, delete the substring
        `, context_optimizer_cmd,` and put back `,` — that is, the tuple loses
        exactly the one element and keeps its separators well formed. The
        substring occurs exactly once.

(3) `apps/cli/command_catalog.py` — two sites:
    (a) the SURVIVING `context.inspect` entry loses one member of its `related`
        tuple: the line `        related=("context.pack", "context.explain"),`
        becomes `        related=("context.pack",),`. It occurs exactly once.
    (b) delete the two `CommandEntry(...)` blocks whose `command_id` values are
        `"context.explain"` and `"context.optimize"`, together with the banner
        comment that heads them — the unique line whose prefix is
        `    # ── context (additional)`, 72 characters long — and the blank line
        that follows the second entry. What must remain immediately after the
        `dashboard.project` entry's closing `    ),` is the blank line and then
        the unique line whose prefix is `    # ── guide`. Both banners are located
        by those prefixes and NEITHER is retyped or re-drawn. Nothing else in the
        file moves.

(4) `apps/ui/src/api/humanizeCatalog.ts` — delete the single line
    `  "context_budget_optimized": "The context budget was optimized to fit the prompt.",`.
    It occurs exactly once. Leave every other key and the header comment alone.

(5) `tests/orchestration/test_project_brain.py` — delete the whole
    `class TestContextOptimizer:` block: from the start of the line
    `class TestContextOptimizer:` up to but NOT including the start of the unique
    banner line whose prefix is `# ── Brain Integration`, which is 74 characters
    long and is neither retyped nor re-drawn. That span is 2791 bytes and takes
    the class's five test methods with it. No other class in the file changes,
    and the file keeps its imports.

(6) `tests/orchestration/import_reachability_allowlist.txt` — delete the two whole
    lines `apps.cli.commands.context_optimizer_cmd` and
    `packages.orchestration.context_optimizer`. Each occurs exactly once. Do not
    re-sort the file.

(7) `tests/orchestration/test_cluster_deletion_map.py` — three sites:
    (a) delete the line `    "packages.orchestration.context_optimizer",` from
        `CLUSTER_MODULES`.
    (b) delete the line `    "apps/cli/commands/context_optimizer_cmd.py",` from
        `CLUSTER_COMMAND_HANDLERS`.
    (c) the comment above `CLUSTER_COMMAND_HANDLERS` names a file this commit
        deletes, so it is repaired in the same commit rather than left false:
        the two lines
          `# `context_pack_cmd.py`, `context_optimizer_cmd.py` and`
          `# `worker_recommend_cmd.py` for exactly that reason.`
        become the one line
          `# `context_pack_cmd.py` and `worker_recommend_cmd.py` for exactly that reason.`

(8) `.agent/f275_deletion_order.md` — REGENERATE the body, header untouched.
    Keep every line beginning with `#` exactly as it is, in order, and replace
    everything after them with one line per component of `measured_order()`,
    members joined by `, `, in the order that function returns. Run the SHIPPED
    function; do not re-implement it and do not hand-sort the result:

        import pathlib, sys
        sys.path.insert(0, str(pathlib.Path.cwd()))
        from tests.orchestration.test_cluster_deletion_order import ORDER_PATH, measured_order
        lines = ORDER_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
        header = [ln for ln in lines if ln.startswith("#")]
        body = "".join(", ".join(c) + "\n" for c in measured_order())
        ORDER_PATH.write_text("".join(header) + body, encoding="utf-8")

    Run it AFTER steps (1) to (7) are applied on disk, or it regenerates the old
    order. The reviewer's own run of this exact recipe produced a body whose first
    three lines are `packages.orchestration.review_bundle`, then
    `packages.orchestration.worker_recommend`, then
    `packages.orchestration.context_pack`; report the body you get and let G5
    judge it rather than editing it toward that.

──────────────────────────────────────────────────────────────
Constraints:

 1. Apply every authored slice BYTE FOR BYTE. Do not reflow, re-wrap, re-sort or
    tidy any of them. If a slice contradicts a gate, apply the slice, run the
    gate, and DECLARE the disagreement in the handback — never repair it silently.
 2. `.agent/` scratch and the two disposable-worktree rules stand: destructive
    verification runs ONLY inside a `git worktree` you create and remove BY ITS
    EXACT PATH, never in the primary checkout, and `git status --porcelain` is
    empty at every commit boundary and at the handback.
 3. Bare `ruff` is denied to this session; the spelling every gate orders is
    `python3 -m ruff check <path>`.
 4. Append convention for C2, used by BOTH files: the new content is the existing
    bytes, then ONE `\n`, then the slice's own bytes, which already end in a
    newline. Nothing else is inserted and nothing existing is rewritten.
 5. C2's two appends are ONE commit. C3 is ONE commit and contains no `.agent/`
    path except `.agent/f275_deletion_order.md`, which is part of the deletion.
 6. Nothing under `docs/` changes this round. `docs/roadmap/features/T2_F260.md`
    names `context_optimizer.py` in its Design list and KEEPS that name: it is the
    specification of what is to be deleted, not residue, and F260's file is kept
    unedited on purpose.
 7. No finding is minted and none is resolved this round. RECORD6 is a `Gate:`
    entry and matches neither the registration nor the resolution pattern, so the
    open set does not move.
 8. G7 runs LAST, after G1..G6, and C5 is committed after it.

──────────────────────────────────────────────────────────────
Done when — SEVEN GATES, every one RUN, every real exit code reported:

G1 TRANSPORT. sha256 and byte count of the committed `.agent/authored/f275-r6.md`
   and of the committed `.agent/last_block.md`. Both must be ONE value. Per §3
   item 37 this chain covers the saved copy and its mirror and claims nothing
   about the bytes that were emitted.

G2 THE PLAN. `.agent/plan.md` byte-identical to PLAN6: 2244 bytes, 40 lines,
   sha256 `8e92db53362f3bc2997b384704ba67d329fe1dcdd9737e4953035eb475c586c7`.
   Report the line count against the AGENTS.md cap of 50, and that `^## Goal$`
   occurs once and `^## Next Steps$` occurs once.

G3 THE RECORD. Over `.agent/live_review.md` and `.agent/prose_slips.md`, report:
   (a) BYTES. live_review 533079 -> 536113, gain 3034 = 1 + 3033.
       prose_slips 169429 -> 171102, gain 1673 = 1 + 1672.
   (b) EDGES. For each file the pre-commit blob is a byte-exact PREFIX of the
       committed file, and the ONE `\n` plus the slice is a byte-exact SUFFIX.
   (c) ORDERED EQUALITY. Count N from the SLICE with your own reader, never from
       this block, and compare the file's last N blank-line units against the
       slice's N paragraphs IN ORDER. Report the N you counted.
   (d) NEGATIVE CONTROL, IN MEMORY ONLY, on the FIRST appended paragraph of EACH
       file: flip one byte inside it and confirm the readers of (b) and (c) both
       REJECT the mutant. Re-read the tracked file afterwards and report that its
       size is unchanged, so the control provably touched no disk state.
   (e) COUNTS in live_review: blank-line units 220 -> 221; `^Gate: ` 27 -> 28;
       `^Gate: F275 R5 ` 0 -> 1. In prose_slips: units 237 -> 242.
   (f) THE OPEN SET DOES NOT MOVE. Distinct `^- R-\d+ — ` ids 69 -> 69; distinct
       `^Done: R-\d+ — ` ids 3 -> 3; OPEN BY DISTINCT ID 66 -> 66. Subtract
       DISTINCT IDS, never raw `Done:` lines.

G4 THE DELETION IS COMPLETE. Report each:
   - `git ls-tree` at the round's tip finds NEITHER
     `packages/orchestration/context_optimizer.py` NOR
     `apps/cli/commands/context_optimizer_cmd.py`.
   - a repo-wide grep, excluding `.git/`, `.data/`, `.agent/` and `.remedy-wt/`,
     returns ZERO for each of `explain_context`, `optimize_context`,
     `context.explain`, `context.optimize`, `_cmd_context_explain` and
     `_cmd_context_optimize`.
   - the same grep for `context_optimizer` returns EXACTLY ONE hit, and it is
     `docs/roadmap/features/T2_F260.md`. Print the line.
   - the same grep for `context_budget_optimized` returns EXACTLY THREE hits, in
     `packages/orchestration/event_schemas.py`, `apps/ui/src/api/actionClass.ts`
     and `tests/orchestration/test_event_ledger.py`. Print them.

G5 THE RATCHETS AND THE DISPATCH TABLE, in the PRIMARY checkout:
   - `python3 -m pytest tests/orchestration/test_import_reachability.py
     tests/orchestration/test_cluster_deletion_map.py
     tests/orchestration/test_cluster_deletion_order.py -q` — the reviewer measured
     9 passed at the base and again with the deletion applied.
   - `python3 -m pytest tests/ui_contracts/ -q` — the reviewer measured 808 passed
     and 5 skipped with the deletion applied.
   - through the SHIPPED reader `apps.cli.commands.collect_all_handlers`, report the
     table size and whether each of `context.explain`, `context.optimize`,
     `context.inspect` and `context.pack` resolves. The reviewer measured 340 at
     the base and 338 after, with the first two absent and the last two present.
   - T001's done-condition names `remedy --all-commands`. Attempt it and report
     EITHER its real output OR the exact denial or error, verbatim — the
     reviewer's shell is denied that binary and yours may be too. This clause is
     satisfied by an honest denial, and the BINDING reading of the same property
     is the catalog one directly above it, which is ordered unconditionally: run
     `apps.cli.command_catalog` and report whether any surviving entry still
     carries `context.explain` or `context.optimize` in a `command_id` or in a
     `related` tuple. The reviewer measured ZERO of both after the deletion.
   - print the regenerated body of `.agent/f275_deletion_order.md` in full.

G6 RUFF AND THE FULL SUITE.
   - `python3 -m ruff check apps/cli/commands/__init__.py apps/cli/command_catalog.py
     tests/orchestration/test_project_brain.py tests/orchestration/test_cluster_deletion_map.py`
     — the reviewer measured "All checks passed!".
   - the FULL suite in the PRIMARY checkout, `python3 -m pytest tests/ -q`. Report
     the real counts and exit code. A failure in
     `tests/orchestration/test_test_runner.py`'s vitest node or in
     `tests/ui_server/test_command_channel.py` is the known environment class only
     if you SHOW it failing the same way at the base; otherwise it is a result.

G7 THE TREE, run LAST.
   - `.agent/STOP` does not exist; `git status --porcelain` is empty; the branch is
     `feature/f275-one-world-completion-part-three`; `git worktree list` shows only
     the primary checkout.
   - `git diff --name-only a1df5d70..<tip>` equals the block's path list exactly.
   - every commit in the range is single-parent, in the ordered sequence C0a, C0b,
     C1, C2, C3, C5, with no C4 commit.
   - report each commit's insertion count against the DECISION F104 D1 cap of 500.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — the
state block with the SESSION NUMBER (this is SESSION 3 of F275) and the round, the
changed-files table with real `git diff --numstat` columns, ONE LINE PER GATE with
its real exit code, the item-status table covering C0a, C0b, C1, C2, C3, C4, C5 and
G1..G7, the deviations, and the Fortschritt line. C5 cannot table its own numstat
columns; report them to the reviewer instead of writing a guess into the file.
It has no length cap.
──────────────────────────────────────────────────────────────

=== BEGIN PLAN6 sha256=8e92db53362f3bc2997b384704ba67d329fe1dcdd9737e4953035eb475c586c7 bytes=2244 ===
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 6 books round 5's PASS and performs THE FIRST `git rm` of this feature: the
`context_optimizer` module group — the module, its handler, its two catalog entries, the
`related` tuple naming one of them, its tests, its allowlist and cluster-map lines, and the
humanize-catalog entry for the event only that handler emitted. The deletion order file is
REGENERATED from the live graph rather than line-edited, because removing the module reorders
the condensation.

## Next Steps

1. The `review_bundle` group, the order file's new first line, in its own commit.
2. The remaining components in the recorded order, the multi-module ones as single commits
   because their members import each other.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831
   and R-0840 named among the ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- 66 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12.
- R-0832 records that the map measures IMPORT edges only, so a consumer coupled to the cluster
  by EVENT NAME is invisible to both the map and the deletion order. Round 6 measured that
  coupling for real: `tests/ui_contracts/test_humanize_catalog.py` pins the UI catalog's keys
  to the Python emitters, so every group whose module emits an event edits that catalog too.
- The full suite runs in the PRIMARY checkout: a fresh worktree may lack `apps/ui/node_modules`
  or a built `apps/ui/dist`, and both failure classes are the environment rather than the change.
=== END PLAN6 ===

=== BEGIN RECORD6 sha256=34981eb5318f569395af5967d640cee931add8318a393204cc747aedf4df09d3 bytes=3033 ===
Gate: F275 R5 — the F275 round 5 entry. VERDICT PASS, booked by round 6 rather than by a round of its own, under operator amendment amend0827-process-diet rule 1, from the committed and pushed `.agent/handoff.md` that carried it across the session boundary. The verdict was authored by the session 2 planner/reviewer after reading the committed range `a040b60c`..`77c0ae11` and re-running that round's verification independently; this booking adds the readings that round could not take of itself and changes none of its findings. THE RANGE IS `a040b60caeda4a9b3b01a3227f36c424fe88ef99`..`250c908957699d29e1bde23b42d30eac4bb82f53`, eight commits — C0a `351058ea`, C0b `807a3fc5`, C1 `83ac6563`, C2 `36704924`, C3 `98c297e0`, C4 `f347dfb0`, C6 `77c0ae11` and the verdict append `250c9089` — every one single-parent, verified by `git rev-list --parents` at the round 6 base `a1df5d70b09cf30e2519a44d8c4686f06f6e9a6b`. THE TWO NUMBERS ROUND 5 COULD NOT TABLE OF ITSELF ARE RECORDED HERE, which is where §3 item 31 routes them under self-drive because a round report ends with its session: `git show --numstat 77c0ae116dda636952b6a328ca00af61c11288d7` reads `285	390	.agent/handoff.md`, so C6 is 285 insertions and 390 deletions over one file — the DECISION F104 D1 exemption for a verbatim rewrite of a single `.agent/**` state file, and under the 500-insertion cap in any case — and `git show --numstat 250c908957699d29e1bde23b42d30eac4bb82f53` reads `114	0	.agent/handoff.md` for the verdict append. Both were re-measured by the round 6 reviewer from the committed blobs and both match what the round 5 handback predicted for them. WHAT ROUND 5 ACHIEVED: the deletion acquired a derived, recorded and RATCHETED order, which operator RULE 2 requires before the first `git rm`, and the derivation surfaced a fact three previous features never recorded — the cluster's internal import graph is CYCLIC in three places, so RULE 2's "leaf modules first" is unsatisfiable at module granularity. DECISION F275 D2 rules the atomic unit to be the strongly connected component and records the measurement, making the deletion fifteen group commits over twenty-four modules rather than twenty-four. THE OPEN SET DID NOT MOVE: 69 distinct registrations against 3 distinct resolutions, 66 OPEN BY DISTINCT ID, and the `- R-0831 CONFIRMED` paragraph round 5 appended is a confirmation matching neither the registration nor the resolution pattern. SIX DEVIATIONS WERE DECLARED AND ALL SIX SUSTAINED; five are the reviewer's own block prose and are dated `.agent/prose_slips.md` lines rather than ids, per amend0827 rule 2, because not one put anything wrong on disk. SESSION 2 ENDED AT GUARDRAIL G6 with three delegated rounds, below the four-round floor, on an operator `.agent/STOP` placed while the round's gates were green; the sentinel was deliberately left on disk for the operator to clear, and session 3 measured it ABSENT at its Phase 0 probe and again before authoring round 6, which is the only reason this feature continued.
=== END RECORD6 ===

=== BEGIN SLIPS6 sha256=32d5fcb4a58323127474214e1b78d7c30b253aa58e9c00bb36e4c7cd6e1ad0fd bytes=1672 ===
2026-09-08 · F275 R5 · The round 5 block's `Change:` line opened "EXACTLY these eleven paths and nothing else" over an enumeration of nine, and stated the correct figure two lines later; "eleven" was round 4's number carried forward, the worker applied the enumeration as constraint 1 requires, and nothing on disk was wrong.

2026-09-08 · F275 R5 · The round 5 block's C4 called the DECISION5 slice "ONE blank-line unit" when it is EIGHT — a heading plus seven paragraphs at 5946 bytes — a figure the reviewer's own pre-emission reader had printed and the reviewer did not read back against the slice's own sentence; the ordered OPERATION was performed as written and every G5 reading passed on the result.

2026-09-08 · F275 R5 · The round 5 block's gate G6 ordered "Report all four exit codes" while enumerating only three measurements, and its own base sentence also listed three; the worker resolved it by running control 2's ordered restore as a fourth measurement and reporting four.

2026-09-08 · F275 R5 · The round 5 block's gate G6 said the reviewer "measured all four at `a040b60c`" for readings actually taken in a worktree based on that commit WITH the round's own not-yet-committed artefacts applied, which G4's correct "both paths absent at the base" reading contradicts on its face; G4's reading is the true one and no result changed.

2026-09-08 · F275 R5 · The round 5 block's constraint 6 wrote "all three of those files" in a sentence naming two, `cluster_deletion_map.txt` and `import_reachability_allowlist.txt`; G8's own enumeration supplied the third, `packages/orchestration/overnight_readiness.py`, and the worker gated all three.
=== END SLIPS6 ===
