STEP T001/round 19 — F275 — the overnight_readiness module group

Goal: Delete the module group `packages.orchestration.overnight_readiness`, now
the first line of `.agent/f275_deletion_order.md`. This is the round that takes
the WHOLE `overnight` command group — its GroupDef, its three remaining commands,
its handler file and its two test files — because `mission_readiness.py` already
carries the same capability under the names DECISION F274 D2 reserved. Book round
18's PASS verdict, register R-0864 and record two prose slips.

WHAT THE REVIEWER MEASURED BEFORE AUTHORING THIS BLOCK. Every numeral below comes
from an APPLIED dry run in a disposable worktree at base `c878073e`: the deletion
was performed, ruff was run at base and at HEAD, the affected guards and then the
full suite were run to completion, and the token sweep was run over the applied
tree. THE DRY RUN FOUND SIX THINGS A READING OF THE IMPORT GRAPH DID NOT, and each
is in the change set below because of it. The worktree was removed before this
block was written.

WHY THIS ROUND IS SAFER THAN ROUND 18 AND MUST STILL BE SWEPT BY HAND. Nothing
here loses a capability: `mission_readiness.py` is a byte-identical carry-over of
this module's definitions, landed by rounds 1 and 2, and `remedy mission
readiness` and `remedy mission report` already serve every reader. The cockpit's
readiness section reads `mission_readiness` too — measured, it does not touch the
dying module. What makes the round dangerous is R-0847: deleting a whole GROUP
removes it from the advertised-command guard's `GROUPS`, so that guard goes BLIND
to every `remedy overnight <sub>` advertisement at exactly the moment those
advertisements go dead. The guard passed at exit 0 in the dry run WHILE three live
advertisements survived. Sweep by hand; do not trust the guard here.

Bundle, in this commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r19.md`
  C0b  mirror the same bytes into `.agent/last_block.md`
  C1   advance `.agent/plan.md` to round 19 — PLAN19, replaced WHOLE
  C2   the record — LEDGER19 appended to `.agent/live_review.md`, SLIPS19
       appended to `.agent/prose_slips.md`
  C3   THE MODULE GROUP, one commit, never split
  C4   the handback, rewriting `.agent/handoff.md`

There is no DECISION commit this round: DECISION F275 D1 already ruled the
carry-over and DECISION F274 D2 already ruled the naming. Nothing new is decided.

Change — C3, the module group. Exactly these paths, nothing beyond them.

DELETED WHOLE:
  packages/orchestration/overnight_readiness.py
  apps/cli/commands/overnight_cmd.py
  tests/orchestration/test_overnight_readiness.py
  tests/cli/test_overnight_cli.py
The handler file dies ENTIRELY this round. Round 18 deleted its fourth command
and left the file alive because its other three imported the module this round
deletes; all three go now, so nothing is left in it.

EDITED — the catalog and the dispatcher:
  apps/cli/command_catalog.py
      Delete the `"overnight": GroupDef(...)` line and the three `CommandEntry`
      blocks for `overnight.readiness`, `overnight.plan` and `overnight.report`,
      with the section comment that introduces them. MEASURED at `c878073e`: the
      only `related=` tuples naming these three ids are the three entries' own,
      so they die together and NO surviving entry needs repair. R-0859 records
      that nothing in the repository resolves `related=` against the catalog, so
      re-measure this by hand rather than trusting a guard.
  apps/cli/commands/__init__.py
      Delete `overnight_cmd` from the sorted import block AND from the dispatcher
      tuple. Both, or the module fails to import.

EDITED — the surviving twin's docstring. `packages/orchestration/mission_readiness.py`
      Its module docstring states, in the present tense, that
      `packages/orchestration/overnight_readiness.py` is "still on disk and is
      deleted with its cluster group". This round makes that false. Rewrite those
      two sentences in the PAST tense, naming F275 round 19 as the round that
      deleted it, and keep every other sentence of that docstring byte-identical
      — in particular the sentence explaining that the carried symbols keep their
      `overnight_` spelling because F261 owns renames. This is the only edit to a
      surviving `packages/` file in the round and it changes no behaviour.

EDITED — the tests that outlive the module:
  tests/orchestration/test_job_fulfillment.py
      THREE imports read `_integrity_status` out of the dying module. Re-point all
      three to `packages.orchestration.mission_readiness`, which carries a
      definition of that name — measured at `c878073e`. Do not copy the function.
  tests/orchestration/test_cluster_deletion_map.py
      Delete the `"packages.orchestration.overnight_readiness"` entry from
      CLUSTER_MODULES **and** the `"apps/cli/commands/overnight_cmd.py"` entry
      from CLUSTER_COMMAND_HANDLERS. Both. The dry run confirmed the map ratchet
      stays GREEN with the handler entry still present, so no gate will catch it
      for you.

EDITED — the ratchets and the order file:
  tests/orchestration/cluster_deletion_map.txt
      Delete every line beginning `packages.orchestration.overnight_readiness <-`.
  tests/orchestration/import_reachability_allowlist.txt
      Delete TWO lines, not one: `packages.orchestration.overnight_readiness` and
      `apps.cli.commands.overnight_cmd`. The dry run went RED on exactly this —
      `test_every_allowlist_entry_still_resolves_to_a_file_on_disk` named the
      handler entry after the module entry had already been removed.
  .agent/f275_deletion_order.md
      REGENERATE from the graph rather than line-editing, as round 18 did. Report
      the resulting component lines; `test_cluster_deletion_order.py` holds the
      file against the live import graph and prints both lists when they differ.

EDITED — the advertisements. R-0861's fix clause binds this round and R-0847 is
why it matters more here than anywhere:
  docs/archive/bounded-overnight-prep-v0.md
      Delete the three-line fenced command block advertising
      `remedy overnight readiness`, `remedy overnight plan` and
      `remedy overnight report`, together with the "Commands (all read-only):"
      line that introduces it. The page STAYS — it is archive, it documents
      history, and its remaining prose describes a preparation block rather than
      a command. Delete only what instructs a reader to run a command that will
      not exist.
  docs/system/quality-baseline-v0.md
      Delete the single coverage-table row whose path column is
      `apps/cli/commands/overnight_cmd.py`.

NOT TOUCHED, DELIBERATELY, and each is declared here so you do not widen scope:
  packages/orchestration/proposed_tasks.py ships a SURVIVING function literally
      named `overnight_readiness`. It is unrelated to the dying module, imports
      nothing from it, and is not part of this group. Leave it alone. This is why
      G4 below sweeps the DOTTED module path and the FILENAME and never the bare
      token — a zero-gate on the bare word is unmeetable by construction.
  tests/cli/test_mission_cmd.py asserts
      `"packages.orchestration.overnight_readiness" not in source`, a ratchet
      that keeps `mission_cmd` off the cluster. After this round it can never
      fire again. It stays GREEN, it is not in this change set, and it is the
      same vacuous-guard class as R-0864 — the reviewer will route it there.

Constraints:
 1. Apply every authored slice BYTE FOR BYTE, extracted from your committed C0a
    blob between its marker lines, markers excluded. Never retype a slice. If a
    slice contradicts this block's prose, follow the slice and DECLARE it.
 2. Touch NO path this block does not name. A red gate on an unnamed path is
    declared, not fixed — that is the sanctioned move.
 3. C3 is ONE commit and is never split; F275 T001 RULE 1 makes one module group
    the atomic unit.
 4. You write NO verdict, NO `Done:` paragraph and NO finding of your own. Use a
    single `Landed: R-XXXX — ` line where a fix lands before its resolution.
 5. Destructive verification runs ONLY in a disposable `git worktree`, removed
    and pruned before C4, so the primary checkout's `git status --porcelain` is
    empty at the handback.
 6. Run the full suite SERIALLY in the PRIMARY checkout.
 7. Every gate below runs at or after C3 and BEFORE C4, because C4 writes the
    handback that quotes each gate's exit code — §3 item 31.

Done when — the gates below. Execute every one and record its REAL exit code with
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. "Green" as a word is a finding.

G1 TRANSPORT — one digest comparison. Report sha256 and byte length of
   `.remedy-wt/f275-r19.md`, of the committed `.agent/authored/f275-r19.md` and of
   the committed `.agent/last_block.md`, and whether ALL THREE are byte-equal.
   Per §3 item 37 that chain covers those three artefacts and nothing else.

G2 THE PLAN AND THE SURVIVOR'S DOCSTRING. Report this block's TOTAL line count
   against its cap of 490. Report `.agent/plan.md` at C1: byte length, sha256,
   byte-identity against the PLAN19 slice extracted from your committed C0a blob,
   its line count against the AGENTS.md cap of 50, and `## Goal` and
   `## Next Steps` each exactly once. Then, for `mission_readiness.py`, report the
   numstat of your docstring edit and confirm by a line-by-line comparison that
   NO line outside the module docstring changed.

G3 THE RECORD, over TWO appends — full byte forensics. For
   `.agent/live_review.md` <- LEDGER19 and `.agent/prose_slips.md` <- SLIPS19:
   (a) BYTE READER: pre length and sha256, post length and sha256, growth equal
       to 1 + slice length, pre a byte-exact PREFIX, the slice a byte-exact
       SUFFIX, the joining byte read back as `b'\n'`.
   (b) STRUCTURAL READER: N COUNTED BY YOUR SCRIPT from the slice, never a number
       this block asserts; the last N blank-line units of the WHOLE post-file
       compared against the slice's N paragraphs IN ORDER, per-unit sha256 on
       both sides — §3 item 36, whole region, not the tail.
   (c) NEGATIVE CONTROL: flip one byte IN MEMORY inside the FIRST appended
       paragraph; BOTH readers must REJECT the mutant and accept the truth; then
       re-read from disk and confirm byte-equality with the committed post-blob.
   (d) COUNT PATTERNS: the rise in `^Gate: `, and `^Gate: F275 R18 ` and
       `^- R-0864 — ` each exactly once.
   (e) THE OPEN SET BY DISTINCT ID, `Landed:` never subtracted. At base
       `c878073e` the reviewer measured registered 92, done 6, open 86, with 34
       distinct `Landed:` ids. Report the same three figures at C2 and confirm
       the base reproduces.

G4 THE SWEEP IS CLEAN, and the guard is BLIND here. Over every tracked file
   outside `.agent/` and `.data/`, sweep for these tokens and no others:
   `packages.orchestration.overnight_readiness`, `overnight_readiness.py`,
   `overnight_cmd`, `overnight.readiness`, `overnight.plan`, `overnight.report`,
   and the spaced form `remedy overnight`. PRINT THE RAW LIST IN FULL AND NEVER
   TRUNCATE IT. Then state, line by line, which survivors are legitimate and why.
   The reviewer's applied run left these classes and no others: history prose in
   `docs/roadmap/features/`; the two `mission_readiness.py` docstring sentences
   THIS ROUND REWRITES; and the `test_mission_cmd.py` ratchet declared above. A
   hit outside those classes is a violation. ALSO run
   `python3 -B -m pytest tests/cli/test_advertised_commands.py -q` and report its
   exit code — and state plainly in the handback that its PASS is NOT evidence
   for this round, because deleting the group removed it from that guard's
   `GROUPS` and the guard skips what it cannot resolve.

G5 THE SURVIVOR IS STILL PINNED — one red-proof, in a disposable worktree at C3.
   Run the UNMUTATED CONTROL FIRST over the same node set, then the mutation,
   then revert and re-run; report all three exit codes and each last summary
   line. Name the revert target by PATH and confirm the mutated bytes occur
   exactly once in that file first.
   RECIPE: in `packages/orchestration/mission_readiness.py`, make
   `build_overnight_readiness` raise immediately.
   NODE SET: `tests/orchestration/test_mission_readiness.py` and
   `tests/cli/test_mission_cmd.py`.
   PROPERTY: the carried module — not the deleted one — is what serves
   `mission readiness` and `mission report`, and it is genuinely covered after
   its twin is gone, so the control is exit 0 and the mutation is exit 1. A green
   mutation here would mean the carry-over is unpinned and is a STOP condition:
   declare it and do not proceed to C4.

G6 THE GUARDS, THE SUITE AND THE TREE.
   (a) `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py
       tests/orchestration/test_cluster_deletion_order.py
       tests/orchestration/test_import_reachability.py
       tests/orchestration/test_job_fulfillment.py
       tests/orchestration/test_mission_readiness.py tests/cli/test_mission_cmd.py
       tests/cli/test_advertised_commands.py tests/test_grouped_cli.py
       tests/cli/test_cli_ux.py -q`
       The reviewer's applied run gave 716 passed, exit 0.
   (b) the canary, `python3 -B -m pytest tests/cli/test_golden_path.py -q`.
   (c) `python3 -B -m pytest tests/docs/ -q` — this round's change set includes
       `docs/` pages, so verification tier 5 applies.
   (d) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY
       checkout with C3 committed. Report passed, skipped, failed and a separate
       `--collect-only` count, and confirm passed + skipped equals collected. At
       base the suite was 18552 passed, 23 skipped, 18575 collected. This round
       deletes two whole test files, so the count MUST fall; report the new
       figures and the arithmetic that reconciles them to the base.
   (e) `python3 -B -m ruff check` over every `.py` path in this round's change
       set: report exit 0. Then, for parity, run ruff over `packages/`, `apps/`
       and `tests/` at BOTH `c878073e` and your C3 and report both totals. The
       reviewer measured 24 errors at the base, none of them in a file this round
       touches; the round must ADD none. Do not fix the pre-existing ones.
   (f) THE TREE: `.agent/STOP` re-read from disk, `git status --porcelain`,
       `git worktree list`, the branch name, and `git diff --name-only <C2>..<C3>`
       compared against this block's C3 path set, stating the MISSING and EXTRA
       sets. Then a per-commit insertion table for every commit BEFORE C4 against
       the DECISION F104 D1 cap of 500, with parent counts. Per §3 item 14 C4's
       own numbers are not yours to report.
   (g) Compare the `+/-` column of your `## Commits` table cell by cell against
       `git show --numstat` per commit and state that they agree — §3 item 28.

G7 THE RATCHETS AGREE WITH THE DISK. Report the component lines now in
   `.agent/f275_deletion_order.md`, that `cluster_deletion_map.txt` holds no line
   naming `overnight_readiness`, and that neither the reachability allowlist,
   CLUSTER_MODULES nor CLUSTER_COMMAND_HANDLERS still names this group's module
   or its handler. Also report the catalog's total command count and confirm no
   id begins `overnight.`.

Handback: the completion report, and rewrite `.agent/handoff.md` at C4. Carry the
SESSION NUMBER — this is SESSION 10 of F275 — the round number, the branch, the
commit SHAs, the changed-files table with `+/-` and a REASON per path, one line
per gate with its real exit code, the item-status table with every ordered item
appearing exactly once, the open-findings count by distinct id, and the next
expected action. It has NO length cap. Declare every deviation. Push ONCE, after
C4, with `git push -u origin feature/f275-one-world-completion-part-three`.
Create no PR, merge nothing, run no `gh` command.

--- BEGIN-PLAN19 ---
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 19 deletes the `overnight_readiness` module group, the first line of the regenerated
deletion order. It takes the WHOLE `overnight` command group with it — the GroupDef, the
three remaining read-only commands, the handler file round 18 left alive, and two test
files — because `mission_readiness.py` has carried the same capability since rounds 1 and 2
and `remedy mission readiness` and `remedy mission report` already serve every reader. It
also books round 18's PASS verdict and registers R-0864.

## Next Steps

1. `worker_registry`, the next component of the order file.
2. Then the `provider_trust` / `provider_trust_verification` pair, which is the last cycle
   and the last component.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and the
   open ids named among the ideas deleted rather than inherited. That round also discharges
   R-0843's widened sweep, R-0858's repair of F267 and R-0859's referential-closure test.
4. T002, the atomic record flip, alone, because every later commit's size depends on it.

## Risks

- The open set is 86 by distinct id at this round's base `c878073e`. Round 19 registers one,
  taking it to 87. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather
  than this feature's, per DECISION F272 D12.
- R-0847 is worst on this round: deleting a whole command group removes it from the
  advertised-command guard's `GROUPS`, so the guard goes blind exactly when the group's
  advertisements go dead. The sweep is read by hand, as its RAW list.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel
  tests race for a port, and the vitest node needs `apps/ui/node_modules`.
--- END-PLAN19 ---

--- BEGIN-LEDGER19 ---
Gate: F275 R18 — the F275 round 18 entry. VERDICT PASS, written by the planner and reviewer of session 10 after reading the committed range `c4c314c2`..`c878073e` and RE-RUNNING every gate independently against the committed blobs; the worker's report was not taken as evidence for any line here. Seven single-parent commits, insertions 430, 409, 20, 10, 66 and 27 for the six before the handback, every one under the DECISION F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own delegation source and both committed copies are 35020 bytes at `4322efd9bed4c28b059739c9b391fb773362278e19782875e5f8d5bbaafc6a36` and compare BYTE-EQUAL; per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` byte-identical to the PLAN18 slice at 41 lines against the cap of 50, and the DECISION18 slice occurring EXACTLY ONCE in `.agent/decisions.md`; the reviewer confirmed all four slices land byte-exact and that no marker line reached any target file. G3 over two appends, both with byte and structural readers and both negative controls flipped inside the FIRST appended paragraph and rejected by BOTH readers; `^Gate: ` rose 39 to 40, and `^Gate: F275 R17 `, `^Done: R-0861 — `, `^- R-0862 — ` and `^- R-0863 — ` each exactly once; THE OPEN SET 85 TO 86 BY DISTINCT ID against registrations 90 to 92 and resolutions 5 to 6. G4: the reviewer re-ran the completeness sweep with its own script and reproduced RAW 76 at the base against RAW 9 at C4 — a reduction of 67 — and read the RAW list in full as R-0861's fix clause requires; of the nine survivors, three are history prose in `docs/roadmap/features/`, five are ordinary English containing the phrase "overnight run" and every one of them is byte-identical at the base, and the ninth is the stale guard entry this entry registers as R-0864. G5: the two ordered colours behaved as measured — the approval gate's control exit 0 at 6 passed against mutation exit 1, and the RE-BASED ambiguity test's control exit 0 against mutation exit 1, which proves that test bites rather than passing vacuously — and probe P1's mutation stayed GREEN exactly as the block predicted, which is the measurement R-0862 records. G6: the affected guards 74 passed, and THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18552 passed, 23 skipped and ZERO failed, with a separately measured collection of 18575 equal to 18552 plus 23; ruff clean over the change set; the C4 path set an EXACT MATCH on 24 paths with the MISSING and EXTRA sets both EMPTY. THE FIVE DECLARED DEVIATIONS ARE ALL SUSTAINED. Two are the reviewer's own prose failing and are recorded as slips rather than findings: the block predicted ONE survivor class for the sweep where three exist, and it stated a ruff baseline of 13 without naming the scope that figure was measured over, which repo-wide is 24. The other three are the worker reading correctly — three readerless leftovers swept inside paths the block already named, per R-0855's fix clause, including an `_agent_dir` helper whose only caller was the deleted `_review_state` and which the reviewer confirmed has no remaining reference; the `StopReason.REVIEW_FINDINGS_OPEN` enum member deliberately KEPT as a serialized contract value rather than removed, declared and routed to the `overnight_readiness` round; and the re-based ambiguity test's new path to its branch, which red-proof P3 pins.

- R-0864 — Low, A GUARD'S NEGATIVE ASSERTION NAMES A TEST FILE THAT NO LONGER EXISTS, SO THAT ENTRY CAN NEVER FAIL AGAIN. `tests/cli/test_product_spine.py`, in `test_fast_lane_no_heavy_runtime_smoke`, asserts that `scripts/remedy_test_fast.sh` does not name any of four heavy runtime test files. One of the four is `test_overnight_executor_cli.py`, which F275 round 18 deleted at `ead50596`. The assertion still passes, and it will pass for every possible future state of the fast-lane script, because a name that exists nowhere cannot appear in it. THE MEASUREMENT, taken by the reviewer at `c878073e` while re-running the round 18 sweep: the string is byte-identical to its form at the base, so no round CHANGED it — round 18 changed what it MEANS by deleting its referent, which is why no gate anywhere went red and why the completeness sweep's RAW list was the only thing that could surface it. This is the vacuous-guard class of R-0438 arriving through a deletion rather than through a typo. It is Low because the other three entries in the same list still bind and the fast lane is genuinely protected against them. FIX CLAUSE, binding on the round that next edits `tests/cli/test_product_spine.py` and on F275's DECISION F260 D3 round at the latest: remove the dead entry from the `heavy` list, and while there resolve the same class in `tests/cli/test_mission_cmd.py`, whose ratchet asserting `"packages.orchestration.overnight_readiness" not in source` becomes vacuous the moment F275 round 19 deletes that module. A deletion round that removes a module SEARCHES THE SUITE FOR NEGATIVE ASSERTIONS NAMING IT, not only for imports of it, because an import goes red and a negative assertion goes quiet.
--- END-LEDGER19 ---

--- BEGIN-SLIPS19 ---
2026-09-09 · F275 R18 · The round 18 block's G4 predicted that the completeness sweep would leave "exactly one class of survivor", history prose in `docs/roadmap/features/`, and the applied run left three: that class, five ordinary English sentences containing the phrase "overnight run", and one stale guard entry. The prediction was too narrow because the block put the SPACED form of the command id into the token list, and `overnight run` is also an ordinary English phrase that four surviving docstrings and prose lines already contained at the base. Nothing landed wrong; the worker declared the wider survivor set and the reviewer's own re-run reproduced it. The lesson is that a sweep token derived from a command id by replacing its dot with a space stops being an identifier and becomes a phrase, so the block states the expected survivor CLASSES from the base measurement rather than predicting a single one, and it measures the token at the BASE before promising what the round will leave.

2026-09-09 · F275 R18 · The round 18 block told the worker that "the base carries 13 pre-existing ruff errors in files this round does not touch" without naming the paths that figure was measured over. The reviewer had measured it across `packages/orchestration/`, `apps/cli/` and `tests/orchestration/`; run over the whole repository the figure is 24. The worker measured 24, could not reconcile it with the block, and correctly declared the discrepancy rather than assuming either number. The binding condition — exit 0 over the change set, zero errors added — held throughout and was verified independently. The lesson is the ordinary one this checklist keeps relearning in new clothes: a numeral about a measurement carries the SCOPE the measurement was taken at, because a bare count invites the worker to reproduce it over a different set and find a contradiction that was never real.
--- END-SLIPS19 ---
