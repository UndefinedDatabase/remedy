── STEP T001/3 — F275 ROUND 13 — the EIGHTH module group: `external_builder_sandbox` ──

Goal:
Delete `packages/orchestration/external_builder_sandbox.py` and everything that exists only for
it, in ONE commit under operator amendment amend0908-f275-finish RULE 1; book round 12's PASS
and one prose slip; register R-0852; and add the two instances round 12 measured to the open
finding R-0843 as a NOTE rather than minting a second id for a defect the record already holds.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r13.md`
  C0b  mirror the same bytes to `.agent/last_block.md`
  C1   `.agent/plan.md` replaced WHOLE by the PLAN13 slice
  C2   append LEDGER13 to `.agent/live_review.md` and SLIPS13 to `.agent/prose_slips.md`
  C3   the deletion — all 13 paths, ONE commit
  C4   `.agent/handoff.md` rewritten whole

THE NUMERALS BELOW ARE MEASURED, NOT ESTIMATED. The reviewer applied this whole deletion in a
disposable worktree at the base `053a25a7` and ran the suite before authoring a line of this
block: 18888 passed with the only two failures being the two artefacts a worktree always
produces — `test_vitest_passes`, because `apps/ui/node_modules` is gitignored and absent from any
fresh worktree, and `test_evidence_index.py::TestPorcelainParsing::test_every_enumerated_path_exists_in_this_repo`,
which failed only while the change was UNCOMMITTED and PASSED once committed, both proved rather
than assumed. In the PRIMARY checkout, where `node_modules` exists and your change IS committed,
the suite must be FULLY GREEN. That worktree and its commit `6c2a9850` have since been removed.

BLOCK SIZE, DECLARED BY THE REVIEWER. Measured on these final bytes: 232 lines TOTAL and 181 of
PROSE, against DECISION F085 D6's 490 and DECISION F085 D5's 400; the LEDGER13 record slice is 5
lines against D6's budget of 140. It exceeds the sixty-line guidance
`docs/roadmap/features/T2_F275.md` gives a deletion-round block, for the reason rounds 11 and 12
recorded; one dated `.agent/prose_slips.md` line covers the class and no id, per amend0827 rule 2.

WHAT MAKES THIS ROUND SIMPLE, stated because the last two were not. The handler file dies WHOLE.
Round 11 measured that `apps/cli/commands/external_builder_cmd.py` held eight handlers of which
exactly one imported `candidate_quality`; that one, `external-builder.evaluate`, died in round 11
and R-0849 registered it. The seven that remain ALL drive `external_builder_sandbox`, so the file
has no surviving reason to exist and the `external-builder` group dies whole with it. No survivor
loses a call site in this round and no cockpit section is involved.

Change set — 13 paths. DELETED WHOLE, 6, each followed by its line count at `053a25a7`:
  packages/orchestration/external_builder_sandbox.py · 560
  apps/cli/commands/external_builder_cmd.py · 161
  tests/orchestration/test_external_builder_sandbox.py · 269
  tests/cli/test_external_builder_cli.py · 153
  docs/system/external-builder-sandbox-v0.md · 70
  docs/system/external-builder-worker-contract-v0.md · 94

`docs/system/external-builder-worker-contract-v0.md` goes WHOLE and not surgically: its subject
is the contract between Remedy and an external builder worker, the whole of which is the deleted
sandbox's ingress. Round 11 already cut its `## 5. Quality is judged later, from evidence`
section when `external-builder.evaluate` died; what remains describes a pipeline that no longer
exists.

EDITED, 7 — the spec per path, with the measured numstat as `+/-`:
  apps/cli/command_catalog.py · 0/82 · the seven `CommandEntry(` blocks whose `command_id` is
      `external-builder.package-create`, `external-builder.package-show`,
      `external-builder.package-list`, `external-builder.submit`,
      `external-builder.submission-show`, `external-builder.submission-list` or
      `external-builder.integrity`, plus the one `"external-builder": GroupDef(…)` line. The
      group dies WHOLE. Leave every surviving entry's `related=(...)` tuple alone, for the reason
      rounds 11 and 12 give: the field has no reader anywhere in the repository.
  apps/cli/commands/__init__.py · 1/2 · the `external_builder_cmd` import and its name inside the
      `for mod in (…)` tuple.
  docs/README.md · 0/4 · every row whose LINK TARGET is one of the two deleted pages — two
      quick-find rows and two index rows. KEY THE REMOVAL ON THE LINK TARGET, never on the slug:
      `external-builder-sandbox` is a substring of the SURVIVING
      `archive/external-builder-sandbox-future.md`, whose own index row at `docs/README.md` line
      167 STAYS.
  docs/archive/external-builder-sandbox-future.md · 1/1 · its DEPRECATED banner line reads
      `> **Status: DEPRECATED** — Built as \`docs/system/external-builder-sandbox-v0.md\`.` and
      that page no longer exists, so the banner claims a built page that is gone. It becomes
      `> **Status: DEPRECATED** — Was built, then DELETED with the prototype cluster (F275).`
      This is the ONE archive page this feature has edited, and it is edited because this round's
      own deletion falsified it, not as a sweep of the archive.
  tests/orchestration/import_reachability_allowlist.txt · 0/2 · the module and its handler
  tests/orchestration/test_cluster_deletion_map.py · 0/2 · the `CLUSTER_MODULES` row and the
      handler-path row
  .agent/f275_deletion_order.md · 0/1 · REGENERATED from `measured_order()` in
      `tests/orchestration/test_cluster_deletion_order.py`, never hand-edited, with the 26-line
      comment header carried byte for byte. EIGHT components become SEVEN. Unlike rounds 11 and
      12 this IS a pure deletion — no surviving component reorders — so the measured numstat is
      `0 1`.

Constraints:
  1. Apply every BEGIN/END slice BYTE FOR BYTE. Never edit, reflow or renumber one. If a slice
     looks wrong, apply it anyway and DECLARE it in the handback.
  2. Write NO verdict, NO `Done:` paragraph, NO finding and NO registration of your own.
  3. The change set is exactly the 13 paths above plus the five `.agent/` paths of C0a, C0b, C1,
     C2 and C4. If a gate shows a 14th is needed, STOP and report it rather than widening.
  4. C2 precedes C3.
  5. `.agent/plan.md` is advanced at C1, the first substantive commit, per §3 item 23.
  6. Read `.agent/STOP` from disk before C0a. If it exists, write the handback and stop.
  7. Every destructive check runs ONLY in a disposable `git worktree` under `.remedy-wt/`, never
     in the primary checkout. Read a base revision with `git show <sha>:<path>` or in such a
     worktree, never by overwrite-and-restore (§3 item 29).
  8. C3 is ONE commit carrying all 13 paths. Its measured shape is 2 insertions against 1401
     deletions.

Done when — EIGHT gates, every one RUN, every exit code read from the process object and never
through a pipe. Report ONE line per gate in the handback.

  G1 TRANSPORT. `.agent/authored/f275-r13.md` at C0a and `.agent/last_block.md` at C0b are each
     byte-identical to the delegation's source file, by `shutil.copyfile` and a re-read sha256.
     Report the byte count, the digest, and that all three compare equal.
  G2 THE PLAN. `.agent/plan.md` at C1 is byte-identical to the PLAN13 slice. Report its byte
     count, sha256 and line count against the AGENTS.md cap of 50.
  G3 THE RECORD, from the COMMITTED blobs at C1 (pre) and C2 (post), never the worktree.
     (a) For `.agent/live_review.md` and `.agent/prose_slips.md`: growth == 1 + len(slice), the
     pre-blob a byte-exact PREFIX and the slice a byte-exact SUFFIX, the joining byte re-read as
     `b'\n'`.
     (b) N COUNTED BY YOUR SCRIPT from each slice — never a number this block asserts — and the
     file's last N blank-line-separated units equal the slice's N paragraphs IN ORDER, with a
     per-unit sha256 printed for both sides.
     (c) NEGATIVE CONTROL: flip one byte IN MEMORY inside the FIRST appended paragraph of each of
     the two files and require BOTH readers to REJECT it; then re-read both tracked files from
     disk and show them byte-equal to the committed post-blobs.
     (d) `^Gate: ` 34 → 35; and `^Gate: F275 R12 `, `^Note: F275 R13 ` and `^- R-0852 — `
     exactly 1 each.
     (e) THE OPEN SET BY DISTINCT ID, by DECISION F085 D7: 80/4/76 before, 81/4/77 after.
  G4 THE DELETION IS COMPLETE. `git ls-tree -r <C3> --name-only` prints False for all 6 deleted
     paths. Then a whole-word sweep for `external_builder_sandbox` over every tracked file
     EXCLUDING `.agent/` and `.data/`, printing EVERY remaining line IN FULL and never
     truncating, run TWICE. RAW: the reviewer measured exactly TWO lines,
     `docs/roadmap/features/T2_F260.md:337` and `docs/roadmap/features/T2_F272.md:744`, both
     must-not-touch spec files; a line outside `docs/roadmap/features/` and `docs/archive/` is a
     real miss that ends the round. STRIPPED, with backtick-quoted spans DELETED from each line
     before matching: the reviewer measured ZERO lines anywhere, and that count is the binding
     zero-gate. Zero-gated symbols, quoted spans deleted first: `get_external_submission`,
     `load_external_packages` and `external_builder_integrity` must each be 0.
  G5 THE FOUR MEASUREMENTS OF A DELETION ROUND, at C3.
     (a) RATCHETS: `python3 -B -m pytest tests/orchestration/test_import_reachability.py
         tests/orchestration/test_cluster_deletion_map.py
         tests/orchestration/test_cluster_deletion_order.py tests/docs/
         tests/cli/test_advertised_commands.py tests/cli/test_cli_ux.py
         tests/cli/test_product_spine.py -q` → exit 0. The reviewer measured 442 passed.
     (b) THE SHIPPED READERS, through `apps.cli.command_catalog` and `apps.cli.commands`, never
         by grep: `len(_BASE_CATALOG)` 276 → 269, `len(collect_all_handlers())` 276 → 269,
         `len(GROUPS)` 51 → 50, duplicate command ids 0. All seven deleted ids ABSENT from both
         readers and `external-builder` absent from `GROUPS`, printed one per line; and
         `provider.verify`, `patch.approve`, `do.continue` and `worker.registry-list` PRESENT in
         both, because the trust, verification and human-approval path this round does NOT touch
         is what R-0852 turns on.
     (c) THE ORDER FILE: `.agent/f275_deletion_order.md` holds SEVEN components against eight at
         the base; its 26-line comment header is unchanged; the body equals
         `", ".join(component)` over `measured_order()`, and you REGENERATE it rather than
         editing it. Its numstat is `0 1`, a pure deletion.
     (d) THE CANARY: `python3 -B -m pytest tests/cli/test_golden_path.py -q` → exit 0.
  G6 RUFF AND BASH. `python3 -m ruff check` over exactly the `.py` files that
     `git diff --name-only 053a25a7..<C3>` names and that still exist at C3 → `All checks
     passed!`, exit 0. Then repo-wide `python3 -m ruff check .` at C3 AND at the base `053a25a7`
     read in a disposable worktree: both must read `Found 26 errors.`, the ceiling
     `tests/orchestration/test_ci_budgets.py` holds. `bash -n scripts/remedy_test_fast.sh` →
     exit 0. `scripts/remedy_test_fast.sh` names NO deleted test file this round — the reviewer
     checked — so it is not in the change set.
  G7 THE FULL SUITE, `python3 -B -m pytest tests/ -q` SERIALLY — no `-n auto` — in the PRIMARY
     CHECKOUT, exit code from the process object. It must be GREEN; a single failure is a red
     gate and ends the round. CLOSE THE ARITHMETIC BY THE ID SET: take the base-side collection
     in a disposable worktree at `053a25a7`, the tip-side at C3, and report the fall and the
     number of ids GAINED, which must be 0. The reviewer measured 18958 at the base and 18919 at
     the tip, a fall of 39. Report the fall you measure and attribute it per file; if it differs,
     say so rather than restating this number.
  G8 THE TREE. `.agent/STOP` re-read from disk: absent. `git status --porcelain`: empty.
     `git worktree list`: the primary checkout ALONE. Branch:
     `feature/f275-one-world-completion-part-three`. `git diff --name-only <C2>..<C3>` names
     EXACTLY the 13 paths of the change set — report it as a set comparison, nothing extra and
     nothing missing. Every commit C0a through C3 single-parent with its insertion count under
     500. C4's own numbers belong to the next round's ledger entry and are not claimed here.

Handback: rewrite `.agent/handoff.md` WHOLE — the state block with `SESSION 7 of feature F275 ·
round 13 · rounds so far 13`, the one-sentence context self-assessment amend0905-throughput
requires, the per-commit changed-files table, one line per gate with its real exit code, the
deviations, the item-status table over the bundle above, the open-findings count, and the next
expected action. It has NO length cap. Then push once.

BEGIN-PLAN13 — the whole new text of `.agent/plan.md`, replacing it entirely
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 13 books round 12's PASS and one prose slip, adds two measured instances to the open
finding R-0843 as a NOTE rather than minting a duplicate id, registers R-0852, and deletes the
EIGHTH module group: `packages/orchestration/external_builder_sandbox.py`, whole, in ONE commit.
Its handler file `apps/cli/commands/external_builder_cmd.py` dies WITH it rather than losing a
handler, because the one handler of the eight that did not drive the sandbox died in round 11.
Seven commands, the `external-builder` group WHOLE, two test files and two doc pages go too. No
survivor loses a call site and no cockpit section is involved.

## Next Steps

1. The `local_model_advisor` component, which this round's regeneration makes the order file's
   first line. It is a SINGLE module.
2. The remaining components in the recorded order — every one a single module except the
   `provider_trust` / `provider_trust_verification` pair, which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849, R-0851 and R-0852 named among the
   ideas deleted rather than inherited.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 76 by distinct id at this round's base `053a25a7`; the ledger commit this
  block fixes as C2 registers one, taking it to 77. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0847 stays OPEN and binds every remaining deletion round: `test_advertised_commands.py`
  cannot see an advertisement whose group has been deleted, so a round that deletes a group
  WHOLE must sweep the spaced `remedy <group> <sub>` form by hand.
- R-0843 now holds three measured instances of one class — a docs page still naming a command
  or a page a deletion round removed. Every remaining deletion round should expect one.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
END-PLAN13

BEGIN-LEDGER13 — appended to `.agent/live_review.md` after one blank-line separator
Gate: F275 R12 — the F275 round 12 entry. VERDICT PASS, booked by round 13 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, and carried from the pushed `.agent/handoff.md` at `053a25a7`. EVERY ONE OF THE EIGHT GATES WAS RE-RUN BY THE REVIEWER ITSELF against the committed blobs; the worker's report was evidence for nothing. Range `21c90fe5`..`053a25a7`, seven commits C0a `40025405`, C0b `86e4f226`, C1 `31a7ec06`, C2 `9dd6666b`, C3 `76354fc5`, C4 `6411bcf4` and C5 `053a25a7`, each parent read from `git log --format=%p`, per-commit insertions 320, 244, 24, 12, 56, 6 and 433, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own scratchpad original and both committed copies are 35556 bytes at `bc4e736d5ff0a479848485b63711b44538a4f72b640f38e6a04d79e3f813a22f` and compare BYTE-EQUAL. G2: `.agent/plan.md` byte-identical to PLAN12 at 2836 bytes, 47 lines against the cap of 50, with both mandated headings. G3, over THREE appends: `.agent/live_review.md` 586275 to 597513, growth 11238 = 1 + 11237; `.agent/prose_slips.md` 181173 to 182696, growth 1523 = 1 + 1522; `.agent/decisions.md` 962212 to 966757, growth 4545 = 1 + 4544. For each the byte reader held with the joining byte read back as a newline; N was COUNTED from the slice by the reviewer's own reader as 3, 3 and 7, ordered equality held over the WHOLE appended region with a per-unit sha256 printed for all thirteen units on both sides; and all three negative controls — flipped IN MEMORY inside the FIRST appended paragraph, per §3 item 36 — were REJECTED by BOTH readers, with every tracked file re-read from disk afterwards and byte-equal to its committed post-blob. `^Gate: ` 33 to 34; `^Gate: F275 R11 `, `^- R-0850 — `, `^- R-0851 — ` and `^## DECISION F275 D6 ` exactly 1 each; THE OPEN SET 74 TO 76 BY DISTINCT ID against registrations 78 to 80 and resolutions 4 to 4. G4: all three whole-file removals absent from `git ls-tree` at C4 over 4583 tracked files; the sweep for `execution_approval_policy` over the 1701 tracked files outside `.agent/` and `.data/` printed IN FULL read ONE line RAW — `docs/roadmap/features/T2_F260.md:345`, a must-not-touch spec file — and ZERO with backtick-quoted spans stripped, which is the binding count; all three zero-gated symbols read 0. G5: the ratchets and the canary 542 passed at exit 0; through the SHIPPED readers `_BASE_CATALOG` and `collect_all_handlers()` both fell 282 to 276 and `GROUPS` 52 to 51 with zero duplicate ids, all six deleted `approval.policy-*` ids ABSENT from both and `approval` gone from `GROUPS`; AND THE PROPERTY THIS ROUND TURNED ON HELD — `doctor.core` is PRESENT in both readers and `doctor` is still in `GROUPS`, so `remedy doctor`, a USER-FACING command whose handler shares a file with the six that died, survives having lost only a diagnostic `_try_import` probe. The regenerated order file holds EIGHT components against nine, its 26-line header sha256 unchanged at `aff913e6…`, and the file compares EQUAL to a fresh regeneration from the live import graph. G6: ruff `All checks passed!` over the six edited Python files still existing at C4, and repo-wide `Found 26 errors.` at BOTH the base — read in a disposable worktree — and the tip; `bash -n` exit 0. G7: THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18935 passed, 23 skipped and ZERO failed, and the arithmetic closes BY THE ID SET: 19005 ids at the base against 18890 at C4, a fall of EXACTLY 115 with ZERO gained, attributed 82 to the deleted test file, 16 to `test_worker_facade_cmd.py`, 8 to `tests/test_grouped_cli.py` — which parametrises over the catalog and is in no change set — 7 to `test_development_artifact_boundary.py` and 2 to `test_product_spine.py`. G8: `.agent/STOP` absent, porcelain empty, ONE worktree, branch correct, and `76354fc5..6411bcf4` naming the 16 paths in an EXACT SET MATCH. WHAT THE ROUND ACHIEVED: the seventh module group, `execution_approval_policy` at 957 module lines, in ONE commit at 6 insertions against 2844 deletions over 16 paths, taking a 1197-line test file, a doc page, six commands and the `approval` group WHOLE with it. THE ROUND CARRIED A RULING AS WELL AS A DELETION: DECISION F275 D6 records that the "approval gate" F275's Do-not-touch protects is F017's HUMAN gate — `patch approve`, `do continue`, the `approval_required` truth — and not this prototype policy module, which F260's own Design section lists by name in the cluster deletion list thirty lines above the Do-not-touch clause that appears to protect it. NO NUMERIC DEVIATION WAS DECLARED AND NONE WAS FOUND: all sixteen per-path numstats matched the block exactly, including the two the round 11 block got wrong, which is the block-authoring method working as intended after a round that measured its own dry run more carefully. NO FINDING IS RESOLVED BY THIS GATE.

Note: F275 R13 — TWO FURTHER INSTANCES ARE ADDED TO THE OPEN FINDING R-0843 RATHER THAN MINTING A SECOND ID, per docs/agents/planner_reviewer_prompt.md §3 item 30, which requires the open set to be searched for the DEFECT before an id is spent and the evidence added to the existing finding when one already describes it. R-0843 registers that a docs page still advertises a command a deletion round removed, measured on `docs/system/architecture.md` and the `context.pack` command. THE SAME DEFECT WAS MEASURED TWICE MORE, both by the round 12 worker in its own handback rather than by any gate, and both re-read by the reviewer at `053a25a7` before this paragraph was written. FIRST, `docs/system/development-artifact-boundary-v0.md` line 39 reads "Guard tests enforce this boundary (see `test_execution_approval_policy.py::TestNoLiveReviewDependency` …)" and that test file was deleted by round 12's own C4, so the page cites a guard that does not exist. SECOND, line 52 of the same page reads "Core operator commands (`worker`, `mission`, `approval`) already use structured state" and line 53 names the development command `progress`; the `approval` group died in round 12 and the `progress` group died in round 10, so a surviving page names two command groups that Remedy no longer has. NEITHER TRIPS ANY GATE, and the reason is worth recording because it is the same blindness R-0847 names from another direction: both are backtick-quoted, so a sweep that strips quoted spans cannot see them, and `\b` does not fire on `test_execution_approval_policy` inside a longer dotted node id. WHY THE ROUND 12 WORKER WAS RIGHT NOT TO FIX THEM: its block specified that file as a pure `0/4` deletion and constraint 3 bound its change set, so either edit would have widened the round on the worker's own authority, which AGENTS.md Scope Control forbids. THE FIX CLAUSE ON R-0843 IS WIDENED BY THIS PARAGRAPH: the round that drafts DECISION F260 D3 sweeps EVERY page under `docs/system/` for the name of every command group and every module this feature has deleted, with backtick-quoted spans INCLUDED in the search rather than stripped, and repairs each hit in that same commit. Stripping is right for a zero-gate over live code and wrong for a docs sweep, because in prose the quoted form IS the advertisement.

- R-0852 — Medium, DELETING `external_builder_sandbox` REMOVES THE WHOLE EXTERNAL-BUILDER INGRESS — SEVEN COMMANDS AND THE `external-builder` GROUP — SO REMEDY CAN NO LONGER ACCEPT WORK FROM A WORKER THAT RUNS OUTSIDE IT. Raised by the reviewer while authoring F275 round 13, because operator RULE 3 in `docs/roadmap/features/T2_F275.md` T001 requires a deletion that takes away a behaviour a user could observe to register a finding naming the behaviour and the feature that inherits the idea. THE MEASUREMENT, taken at `053a25a7` by an APPLIED dry run of the whole deletion in a disposable worktree, through the SHIPPED readers rather than by grep: `len(_BASE_CATALOG)` and `len(collect_all_handlers())` both fall 276 to 269 and `len(GROUPS)` falls 51 to 50. The seven ids are `external-builder.package-create`, `external-builder.package-show`, `external-builder.package-list`, `external-builder.submit`, `external-builder.submission-show`, `external-builder.submission-list` and `external-builder.integrity` — the whole of the group, which loses its `GroupDef` too. THE HANDLER FILE DIES WHOLE, WHICH IT COULD NOT HAVE DONE ONE ROUND EARLIER: round 11 measured eight handlers in `apps/cli/commands/external_builder_cmd.py` of which exactly one imported `candidate_quality`, kept the file and deleted that one handler, and R-0849 registered the loss. The seven that remained all drive this module, so the file now has no surviving reason to exist. WHAT A USER LOSES: the whole quarantined ingress path for work produced OUTSIDE Remedy — packaging a safe request for an external worker, relaying it, submitting the returned candidate into quarantine, listing and inspecting packages and submissions, and the integrity scan over that store. WHAT IS EXPLICITLY NOT LOST, and this is why the severity is Medium rather than High: NOTHING THAT GUARDED THE INGRESS IS TOUCHED. The Trust Gate, Verification, materialization into a human-approvable intent, and the human approval itself — `provider.verify`, `patch.approve`, `do.continue` — all survive this round's change set untouched, and G5(b) gates exactly that. The deletion removes a DOOR, not a lock, and Remedy is strictly more closed afterwards rather than more permissive. TWO DOC PAGES DIE WITH IT and that is deliberate: `docs/system/external-builder-sandbox-v0.md` describes the deleted store, and `docs/system/external-builder-worker-contract-v0.md` describes the contract an external worker was to satisfy, a contract no command can now receive. WHICH FEATURE INHERITS THE IDEA, as RULE 3 requires and without rebuilding anything: F085 owns the release-capability path and is named in the surviving `docs/archive/external-builder-sandbox-future.md` as the future direction for this idea, so external-worker ingress goes there; and the quality scoring of an external submission already went to F082 under R-0849. THE FIX CLAUSE, binding on the round that drafts DECISION F260 D3: that paragraph names all seven ids and the `external-builder` group among the ideas DELETED rather than inherited, names F085 as the inheritor of external-worker ingress, and records that Remedy deliberately accepts no externally produced candidate today. A stub, a shim, an alias or a compatibility reader is forbidden by AGENTS.md Scope Control by name, and this finding is not resolved by providing one.
END-LEDGER13

BEGIN-SLIPS13 — appended to `.agent/prose_slips.md` after one blank-line separator
2026-09-09 · F275 R13 · The round 12 block specified `docs/system/development-artifact-boundary-v0.md` as "the two table rows and the two bullets naming the deleted module" at a numstat of 0/4, and the file holds more than two candidate bullets, so the worker had to infer which pair the reviewer meant and confirmed its reading only by hitting the stated numstat exactly. A spec that names a COUNT of units plus a predicate should name the units, or state the predicate precisely enough that only one set satisfies it; the numstat rescued this one and is not a substitute for saying what was meant.
END-SLIPS13
