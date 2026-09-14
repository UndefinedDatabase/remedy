── STEP T001 (round 22 of n) — F275 ──────────────────────────
Goal:        Delete the LAST component of `.agent/f275_deletion_order.md` — the strongly
             connected pair `provider_trust` and `provider_trust_verification` — with its
             handler, its whole `provider` command group, its ContractAction members, four
             whole test files, two documentation pages, and the survivor edits operator
             RULE 3 forces. T001's module list becomes EMPTY.
Bundle:      C0a save the block · C0b mirror the block · C1 the plan · C2 the record ·
             C3 DECISION F275 D11 · C4 the deletion, in ONE commit · C5 the handback.
Handback:    completion report + rewrite `.agent/handoff.md`.
(the line below is the box rule: the character U+2500 repeated 62 times, nothing else)
──────────────────────────────────────────────────────────────

BASE. `5178df03`, the round 21 handback commit. Every figure below was measured by the
reviewer in an APPLIED dry run at that commit, inside a disposable worktree, and taken to
a GREEN full suite there. Nothing below is a prediction unless it says so.

WHAT MAKES THIS ROUND HARD, STATED UP FRONT. The pair is not a leaf. Deleting it removes
`remedy provider intake-repair`, and that command is the ONLY route by which an external
candidate ever entered Remedy. THREE surviving things are built on that route: the
self-dogfood attempt rail, which parks at `awaiting_external_candidate` and can no longer
leave it; `repair_request_builder.py`, which prepares a package whose own printed
instructions told the operator to import the answer; and `provider_patch_material.py`,
which loses four imported names and most of its tests. DECISION F275 D11, committed at C3
before the first `git rm`, rules all three, and the ruling is NOT "delete them": operator
"Do not touch" forbids deleting a module outside F260's Design list, and DECISION F260 D3
already maps the external builder to "none, deliberately". They degrade, honestly, and
three findings record what was lost.

# ============================ THE CHANGE SET ============================
# Nothing outside this list is edited, created or deleted. G8 compares the set you measure
# against it; the block states no total, so the numeral in your handback is yours.
#
# DIES WHOLE — `git rm`, step 1. Line counts at the base, for orientation only.
#   packages/orchestration/provider_trust.py 1058 · provider_trust_verification.py 1020
#   apps/cli/commands/provider_cmd.py 170
#   tests/orchestration/test_provider_trust.py 348 · test_provider_trust_verification.py 359
#   tests/cli/test_provider_trust_cli.py 136 · test_provider_material_cli.py 125
#   tests/cli/test_provider_verification_cli.py 118
#   docs/system/provider-trust-gate-v0.md 97 · provider-trust-verification-v1.md 132
#
# EDITED. Deletion figures are fixed by their anchors; insertion figures are the
# reviewer's dry run and are EXPECTATIONS about wording, not numbers you owe.
#   packages/orchestration/orchestrator_brain.py            8/83   step 2
#   packages/orchestration/self_dogfood_execution.py       24/40   step 3
#   packages/orchestration/repair_request_builder.py       19/33   step 4
#   packages/orchestration/provider_patch_material.py       6/24   step 5
#   packages/orchestration/self_dogfood.py 0/13 · run_contract.py 0/19    step 6
#   apps/cli/command_catalog.py 3/97 · commands/__init__.py 1/2           step 7
#   apps/cli/commands/repair_cmd.py                         0/1    step 4
#   pyproject.toml                                          0/1    step 8
#   tests/orchestration/test_provider_patch_material.py     9/176  step 5
#   tests/orchestration/test_repair_request_builder.py     11/68   step 4
#   tests/orchestration/test_self_dogfood_execution.py     11/79   step 3
#   tests/cli/test_repair_request_cli.py 7/3 · test_self_dogfood_execution_cli.py 2/1
#   tests/orchestration/cluster_deletion_map.txt 0/5 · test_cluster_deletion_map.py 1/4
#   tests/orchestration/import_reachability_allowlist.txt 0/3              step 8
#   .agent/f275_deletion_order.md                           0/1    step 8
#   docs/README.md 0/4 · system/orchestrator-brain-v0.md 6/8              step 9
#   docs/system/self-dogfood-execution-v0.md 19/18 · provider-patch-materialization-v0.md 1/3
#   docs/system/repair-request-builder-v0.md 0/2 · quality-baseline-v0.md 0/1
#   docs/archive/candidate-generator-adapter-future.md      0/1    step 9
#
# STATE
#   .agent/plan.md .agent/live_review.md .agent/prose_slips.md .agent/decisions.md
#   .agent/authored/f275-r22.md .agent/last_block.md .agent/handoff.md
#
# The reviewer's applied dry run measured 128 insertions against 4253 deletions over the
# non-`.agent/` paths. Deletions carry no insertions, so the DECISION F104 D1 cap of 500
# insertions is not in play for C4.

# ============================ CONSTRAINTS ============================
1. Apply every authored slice BYTE FOR BYTE, extracted from the COMMITTED C0a blob between
   its marker lines with the markers EXCLUDED. Never retype a slice, never edit one.
2. C3 commits DECISION F275 D11 BEFORE the first `git rm`. That ordering is the whole
   reason C3 exists.
3. C4 IS ONE COMMIT. Operator RULE 1 in `docs/roadmap/features/T2_F275.md` T001 makes one
   module group atomic and forbids splitting it; a half-deleted pair is the state this work
   must not leave behind. The insertion count is small, so no cap forces a split.
4. R-0855's fix clause binds every remaining deletion round of this feature, and this is
   one: for EVERY definition you delete, sweep the neighbourhood in the SAME commit — the
   callers, the constants left with no reader, and the section comment above it. Step 3
   names one such constant the reviewer found (`_self_provider_label`) and step 7 names an
   orphaned section comment; report anything else you find.
5. R-0843's counter-measure, in the same commit: sweep EVERY surviving file of this change
   set for PROSE the deletion falsified — in each file's own words, not in the deleted
   modules' identifiers — and report the result INCLUDING "nothing" where that is the
   answer. Steps 3, 4, 5 and 9 already order the prose the reviewer found; a second reading
   is the point.
6. NO stub, NO shim, NO copy of deleted code into a survivor, and no compatibility reader.
   AGENTS.md Scope Control forbids them by name.
7. You write NO verdict, NO `Done:` paragraph and NO finding. R-0866, R-0867 and R-0868 are
   REGISTERED by the reviewer's LEDGER22 slice at C2, not by you. No finding is resolved
   this round, so write NO `Landed:` line at all.
8. Do not repair the 24 pre-existing repo-wide `ruff` findings. The dry run ends at exactly
   24, the base figure, and G7 compares the two distributions.
9. All disposable work lives under the gitignored `.remedy-wt/`; `/tmp` is denied. Use a
   worktree name nothing else will collide with. Remove and prune every worktree and delete
   every scratch file before the final `git status --porcelain`.
10. The full suite runs in the PRIMARY CHECKOUT, serially, never `-n auto`, never in a
    worktree. A fresh worktree has no vitest under `apps/ui/node_modules`, and
    `TestVitestFrontendTestFoundation::test_vitest_passes` fails there for that reason
    alone — the reviewer measured it and deselected it from the dry run for that reason.

# ============================ C4 — THE ORDERED WORK ============================

STEP 1 — `git rm` every file listed under DIES WHOLE. Three are test files the reviewer's
first token sweep did NOT find, because they drive the commands through a
`run_grouped_cli(["provider", ...])` helper that splits the command name across arguments:
`tests/cli/test_provider_trust_cli.py`, `test_provider_material_cli.py` and
`test_provider_verification_cli.py`. The applied suite found them. If your own sweep finds
a further such file, STOP and report it rather than widening the change set.

STEP 2 — `packages/orchestration/orchestrator_brain.py`. Delete, each anchor unique at
`5178df03`: the `IMPORT_CANDIDATE` and `PROVIDER_TRUST_VERIFICATION` members of
`OptionKind`; their two entries in `_BASE_SCORE`; the `"trust_accepted"` and
`"trust_rejected"` keys from the `sig` defaults; the whole `# Provider trust + materials +
requests.` try-block that reads `load_trust_reports` (KEEP the `load_materials` block that
follows it — `provider_patch_material` survives, and re-title the comment so it no longer
promises trust); the whole `# Provider Trust Verification v1 signals (Step 1554).`
try/except block; the `# Self attempt awaiting candidate.` option block, which is the LIVE
dead advertisement of `remedy provider intake-repair`; the two verification option blocks
and the repeated-rejection block that follow `# Provider Trust Verification v1 (Step
1554).`; the two trust fields in the evidence fingerprint; and the `trust_rejected >= 2`
BLOCK branch of `_loop_guard`.
THEN, in `_routing_plan`, NARROW `needs_candidate` to its second disjunct only — drop
`sig.get("self_attempts_awaiting", 0) > 0` — and rewrite the tier's reason string, which
currently promises "but only through the Trust Gate, never applied directly" and is false
the moment the gate is gone. KEEP the `EXTERNAL_BUILDER_NEEDED` tier itself: it is pinned
by `TestModelRouting::test_candidate_generation_external_builder`, which the reviewer
confirmed still passes.
KEEP `self_attempts_awaiting` everywhere else. Its store survives, so the signal, the
`self_awaiting_candidate` situation key and the fingerprint field are all still true.

STEP 3 — `packages/orchestration/self_dogfood_execution.py` AND its two test files. This is
the survivor DECISION F275 D11 part (a) rules.
  (a) Delete, in `reconcile_self_attempt`, the local `load_trust_reports` import and the
      whole `if not a.patch_intent_id:` candidate-linking block beneath the comment
      beginning `# Link a materialized provider intent`. Replace the block with a
      deliberate-absence comment naming what is gone, why, and R-0866. Do NOT touch the
      `if a.patch_intent_id:` block that follows: it still runs for an attempt whose intent
      is already on disk, so it is degraded reachability, not dead code.
  (b) `_self_provider_label` loses its last production reader when (a) lands and the two
      advertisements in (c) go. DELETE the function — this is constraint 4's readerless
      definition, and the reviewer verified no other file calls it.
  (c) TWO next-safe-action strings advertise the deleted command, and both are
      user-facing: the assignment in `start_self_execution` and the
      `AWAITING_EXTERNAL_CANDIDATE` branch of `_next_action_for`. Replace both with
      `"remedy self status --json"`, which is catalog-backed and already used by this
      module's attempt-not-found branch.
  (d) Rewrite the head-docstring pipeline so it ENDS at `awaiting_external_candidate`, and
      the docstring of `reconcile_self_attempt`, which lists "provider trust reports" among
      the durable truths it reads.
  (e) In `tests/orchestration/test_self_dogfood_execution.py`: delete
      `TestEndToEnd::test_full_self_improvement_flow` and
      `test_reconcile_does_not_mislink_foreign_intent` — both drive the deleted route, and
      the second is R-0084's mislink guard, which is now held BY CONSTRUCTION because no
      linking code remains. Re-pin `test_execute_awaits_candidate` and
      `test_next_actions_catalog_backed` on the SURVIVING next action; the second is worth
      strengthening while you are there, because it currently validates a string the test
      itself supplies rather than the one the attempt reports.
  (f) In `tests/cli/test_self_dogfood_execution_cli.py`, re-pin the one assertion on
      `next_safe_action`.

STEP 4 — `packages/orchestration/repair_request_builder.py`, its CLI and its two test
files. DECISION F275 D11 part (b). FIVE live advertisements sit here, and one of them is
inside the request text a human is handed:
  (a) the head docstring's `remedy provider intake-repair ... → Trust Gate → ...` pipeline;
  (b) `_import_next_steps`, whose steps 3 and 4 name `provider intake-repair` and
      `provider trust-show`;
  (c) the `intake_cmd` and `trust_cmd` locals and the `output_intake_command` /
      `trust_gate_command` fields they fill — those fields exist on BOTH result dataclasses
      and in BOTH `to_dict` bodies, and they are REMOVED rather than emptied, because
      `apps/cli/commands/repair_cmd.py` PRINTS `output_intake_command` to the operator and
      an empty print is a worse surface than none;
  (d) the `safe_summary` that ends "import the response via provider intake-repair";
  (e) the `CandidateGeneratorExecutionUnavailable` message that tells the caller to
      "import it via 'remedy provider intake-repair'".
  Delete the print line in `apps/cli/commands/repair_cmd.py`. In
  `tests/orchestration/test_repair_request_builder.py` delete the whole simulated
  end-to-end section at the tail of the file and re-pin
  `TestArchitectureGuards::test_next_action_catalog_backed` so it asserts the ABSENCE of
  both dead commands and validates every command the surviving steps still name. In
  `tests/cli/test_repair_request_cli.py` re-pin the two assertions, one on the JSON shape
  and one on the TEXT surface.

STEP 5 — `packages/orchestration/provider_patch_material.py` and its test file. DECISION
F275 D11 part (c). Delete the top-level `Severity, TrustStatus, validate_paths` import
block and, inside `verify_provider_patch_material`, the local `get_trust_report` and
`storage` imports together with the two checks they feed — `paths_safe` and
`trust_report_accepted`. Put a deliberate-absence comment in their place naming R-0867: the
function is left STRICTLY WEAKER, its `ok` strictly easier to satisfy, and that is stated
rather than hidden. The reviewer measured that it has NO production caller anywhere under
`packages/` or `apps/` once the pair dies, which is why RULE 3's removal is defensible here
and why R-0867 names the feature that should reap the module.
In `tests/orchestration/test_provider_patch_material.py`, everything that reached its
subject through `_intake` dies with the route: `TestMaterialization`,
`TestApplyCompatibility`, `TestRedaction` and
`TestArchitectureGuards::test_accepted_intent_resolvable_and_catalog_backed`, plus the
`env` fixture and the `_job` / `_intake` helpers they used. `TestConversion` and the three
source-reading guards SURVIVE untouched. Rewrite the module docstring, which currently
promises the coverage that just left.

STEP 6 — the two files that lose a block each.
`packages/orchestration/self_dogfood.py`: delete the whole `# Provider trust accepted but
not materialized.` try-block, which is the only place it touches the pair.
`packages/orchestration/run_contract.py`: delete the SIX provider members of
`ContractAction` with their two comment blocks, and their six lines in the safe-action
tuple. The reviewer resolved every one of the six against the whole tree: not one is
referenced outside `run_contract.py` and the dying files.

STEP 7 — `apps/cli/command_catalog.py` and `apps/cli/commands/__init__.py`.
Delete the `"provider"` GroupDef and the WHOLE provider section, which runs from the
comment line beginning `# ── provider (trust gate` up to but NOT including the comment line
beginning `# ── self (self-dogfood planner`. It yields exactly five ids —
`provider.intake-repair`, `provider.trust-show`, `provider.material-show`,
`provider.verify`, `provider.verification-show`. DIRECTLY ABOVE that section sits an
ORPHANED section comment, `# ── overnight mission contract (Review/Repair Spine v0)`, with
no entries under it at all — a leftover from an earlier round. Delete it and its blank line
too; that is constraint 4.
THEN REPAIR THE THREE `related=` TUPLES that would otherwise become the FIRST dangling
references this feature has created, which R-0859 forbids by name: two on the `repair.*`
entries and one on a `self.*` entry, each naming `provider.intake-repair`. Drop only that
member and keep the tuple.
Drop `provider_cmd` from BOTH the sorted import block and the dispatcher tuple in
`apps/cli/commands/__init__.py`.

STEP 8 — the ratchets, the order file and one line of `pyproject.toml`.
`tests/orchestration/cluster_deletion_map.txt` is REGENERATED from the live import graph,
never line-edited, and comes out with its comment header and NO edge lines.
`CLUSTER_MODULES` in `tests/orchestration/test_cluster_deletion_map.py` becomes the EMPTY
tuple — annotate it so the type is still readable. `.agent/f275_deletion_order.md` loses its
last component line, leaving its 26-line header byte-identical.
`tests/orchestration/import_reachability_allowlist.txt` loses exactly three entries.
`pyproject.toml` carries a `per-file-ignores` entry for
`packages/orchestration/provider_trust_verification.py`; delete that line, because a
per-file ignore for a file that does not exist is a rule nothing can ever apply.

STEP 9 — the documentation. R-0861's fix clause binds every remaining deletion round, so
these are named as PAGES rather than left to a consumer map.
`docs/README.md` loses FOUR index rows: the two deleted pages appear in both the quick-find
table and the system table. `docs/system/quality-baseline-v0.md` loses the coverage row for
the deleted handler. `docs/system/repair-request-builder-v0.md`,
`docs/system/provider-patch-materialization-v0.md` and
`docs/archive/candidate-generator-adapter-future.md` lose the links that point at the two
deleted pages; in the materialization page the FIRST sentence carries one of them inline.
`docs/system/orchestrator-brain-v0.md` loses the trust signals from its situation list, its
loop-guard list, its anti-loop paragraph, its Future bullet and its two See-also links.
`docs/system/self-dogfood-execution-v0.md` is the one that needs real prose: its Flow block,
its "candidate output re-enters only through the existing Provider Trust Gate" rule, its
States paragraph and its See-also link all describe a round trip that no longer exists.
Write the deliberate absence AGENTS.md's Code Discoverability Conventions require — a
reader will look for the import step exactly there — and name R-0866.

# ============================ DONE WHEN ============================
Run every gate as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL exit code.
Report ONE line per gate in the handback. Every gate runs at or before C4, so the handback
C5 writes can quote all of them.

G1 TRANSPORT — one digest comparison and nothing else. The delegation source
`.remedy-wt/f275-r22.md`, the committed `.agent/authored/f275-r22.md` and the committed
`.agent/last_block.md` are the same byte length at the same sha256 and compare BYTE-EQUAL.
C0a copies with `shutil.copyfile`; C0b takes its bytes from the COMMITTED C0a blob via
`git show`. State that per §3 item 37 this chain covers those three artefacts and claims
nothing about the emitted bytes.

G2 THE PLAN AND THE SLICES — `.agent/plan.md` at C1 is BYTE-IDENTICAL to the PLAN22 slice,
under the AGENTS.md cap of 50 lines, with `## Goal` and `## Next Steps` each exactly once.
EVERY slice this block carries occurs EXACTLY ONCE in its own target, and a grep for every
one of this block's marker strings over every one of those targets returns ZERO for each
target. Report the slice count and the marker count YOU measured.

G3 THE RECORD — the three appends, each with a byte reader, a structural reader and a
negative control. For LEDGER22, SLIPS22 and DECISION22: the committed post-blob equals the
pre-blob, then ONE newline, then the slice exactly as extracted — read the joining byte
back from the post blob at offset `len(pre)` and report it, rather than assuming it. The
structural reader COUNTS N from the slice itself and compares the LAST N blank-line units
of the whole post-file IN ORDER against the slice's N paragraphs with a per-unit sha256 on
both sides; the unit BEFORE that region lies inside the pre blob; and ONE byte is flipped
in memory inside the FIRST appended paragraph of each append, which BOTH readers must
REJECT while BOTH ACCEPT the truth. Then report `^Gate: ` before and after,
`^Gate: F275 R21 `, `^Note: F275 R22 `, `^- R-0866 — `, `^- R-0867 — `, `^- R-0868 — ` and
`^## DECISION F275 D11 ` each exactly once, and THE OPEN SET BY DISTINCT ID at the base and
at C2, with `Landed:` never subtracted.

G4 THE DELETION IS COMPLETE AND THE SWEEP IS READ AS ITS RAW LIST — R-0861's fix clause,
and the gate this round's own guard cannot answer. Over every tracked file outside
`.agent/` and `.data/`, sweep for the module names `provider_trust`,
`provider_trust_verification`, `provider_cmd`, the five deleted command ids, the six deleted
`ContractAction` values, and the SPACED advertisement forms `remedy provider intake-repair`,
`remedy provider trust-show`, `remedy provider material-show`, `remedy provider verify` and
`remedy provider verification-show`. PRINT THE RAW LIST IN FULL AND DO NOT TRUNCATE IT, and
classify every line. The reviewer's dry run leaves survivors only under
`docs/roadmap/features/`, which is history prose about `[x]` features and is the legitimate
survivor class this feature has had since round 19; ANY hit under `docs/guides/`,
`docs/system/`, `packages/`, `apps/`, `scripts/` or `tests/` is a defect of this round.
The spaced forms must return ZERO everywhere.
RUN `tests/cli/test_advertised_commands.py` separately and report it, then STATE PLAINLY
that its pass is NOT evidence for this round: deleting the whole `provider` group removes it
from that guard's `GROUPS` and the guard skips what it cannot resolve, which is R-0847.

G5 THE SURVIVORS STILL REFUSE — the mutation red-proof, in a disposable worktree created at
C4, `__pycache__` purged and `python3 -B` before every run. This round REMOVES safety checks
from a survivor, so the colour that matters is that the checks which REMAIN still bite.
  (a) Show the import of `packages.orchestration.self_dogfood_execution` resolves INSIDE
      that worktree, so no editable install shadows it.
  (b) CONTROL, unmutated, over `tests/orchestration/test_self_dogfood_execution.py` and
      `tests/orchestration/test_repair_request_builder.py` — report exit code and count.
  (c) MUTATION, by PATH, in `<worktree>/packages/orchestration/self_dogfood_execution.py`:
      make `_transition` accept an illegal transition — return without raising instead of
      rejecting. The bytes you change must occur EXACTLY ONCE in that file; report the
      count before you change them. `TestStartAndIdempotency::test_transition_rejects_illegal`
      must go RED. NAME the tests that went red.
  (d) REVERT BY PATH, purge, re-run, and show the control figure returns and the worktree
      porcelain is EMPTY.
STOP CONDITION: if (c) comes out GREEN, do not push. Reset the unpushed C4, hand back with
the transcript, and say so — a green mutation there means the state machine this round
leaves in place is not guarded at all.

G6 THE CATALOG AND THE REFERENTIAL CLOSURE — read the SHIPPED catalog by importing
`_BASE_CATALOG` and `GROUPS` from `apps.cli.command_catalog`, never by grepping the source,
and read the base the same way inside a READ-ONLY disposable worktree at `5178df03`. Report,
at BOTH revisions: the command count, the group count, whether `"provider"` is in `GROUPS`,
the ids beginning `provider.`, and the duplicate-id count. Then DISCHARGE R-0859's STANDING
OBLIGATION: resolve EVERY `related=` tuple in the catalog against the LIVE id set at both
revisions and report the dangling references at each. TWO are pre-existing —
`mission.run -> dogfood.run-loop` and `repo.status -> readiness.show` — and constraint 8's
sibling rule leaves them alone; this round must add NONE, and step 7 repairs the three it
would otherwise have created.

G7 THE SUITE, THE GUARDS AND RUFF.
  (a) The guards — under `tests/orchestration/`: `test_cluster_deletion_map.py`,
      `test_cluster_deletion_order.py`, `test_import_reachability.py`,
      `test_orchestrator_brain.py`, `test_self_dogfood_execution.py`,
      `test_repair_request_builder.py`, `test_provider_patch_material.py`,
      `test_self_dogfood.py`, `test_evidence_index.py`; plus `tests/docs/`,
      `tests/test_grouped_cli.py`, `tests/cli/test_cli_ux.py`.
  (b) The canary `tests/cli/test_golden_path.py`.
  (c) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY CHECKOUT,
      with C4 committed. Close the arithmetic against the base by a NODE-ID SET DIFFERENCE
      of two `--collect-only` runs — take the WHOLE line as the node id, because a
      parametrized id may contain a space and splitting on it collapses distinct ids into
      one. The reviewer measured, as an expectation: 105 ids REMOVED and 2 ADDED against a
      base of 18478. Report the sets you measure and attribute the removals by file.
  (d) `python3 -B -m ruff check` over every surviving `.py` path of the change set, and the
      repo-wide PARITY reading over `packages`, `apps` and `tests` at BOTH the base and C4 —
      the base taken in a DISPOSABLE READ-ONLY worktree, NEVER by writing a base blob over a
      tracked file. Both revisions read `Found 24 errors.` in the dry run. Report a `diff`
      of the two per-file distributions, and say how many findings your parser actually
      parsed, so a silent parse failure cannot pass for agreement.

G8 THE TREE — `.agent/STOP` re-read from disk; `git status --porcelain` EMPTY;
`git worktree list` holding ONE entry; the branch correct; `git diff --name-only <C3>..<C4>`
compared AS A SET against the C4 paths this block's change set names, with MISSING and EXTRA
both reported and the size of each set the numeral YOU measured; and the per-commit insertion
count with its parent count for every commit BEFORE C5, each against the DECISION F104 D1 cap
of 500. Compare every `+/-` cell of your `## Commits` tables CELL BY CELL against
`git show --numstat` for its commit and say whether they agree.

# ============================ THE AUTHORED SLICES ============================
# Each slice lies between its BEGIN and END marker line; the marker lines themselves are
# EXCLUDED from the slice and never reach any file. G2 asks you for their number.

<<<BEGIN PLAN22>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 22 deletes the LAST component of `.agent/f275_deletion_order.md` — the strongly
connected pair `provider_trust` and `provider_trust_verification` — with its handler, the
whole `provider` command group, six `ContractAction` members, four whole test files and two
documentation pages. `CLUSTER_MODULES` becomes the EMPTY tuple and T001's module list is
exhausted. DECISION F275 D11, committed before the first `git rm`, rules the three surviving
consumers that lose their outlet, and R-0866, R-0867 and R-0868 record what each one lost.

## Next Steps

1. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it. That round
   also discharges R-0843, R-0858, R-0859's closure test, R-0860, R-0864 and R-0868's
   scaffolding question, and retires the now-vacuous cluster map and order ratchets.
2. T002, the atomic record flip, alone, because every later commit's size depends on it.
3. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 88 by distinct id at this round's base `5178df03`. Round 22 registers
  three and resolves none, taking it to 91. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- Worst on this round: a surviving module loses a safety check and nothing notices.
  `verify_provider_patch_material` genuinely does lose two of its seven checks, which
  R-0867 records; the reviewer measured that it has no production caller.
- The cluster map and order ratchets become VACUOUS the moment `CLUSTER_MODULES` empties.
  R-0868 records it with a fix clause; this round does not widen to retire them.
- The full suite runs SERIALLY in the PRIMARY checkout. A fresh worktree has no vitest.
<<<END PLAN22>>>

<<<BEGIN LEDGER22>>>
Gate: F275 R21 — the F275 round 21 entry. VERDICT PASS, written by the planner and reviewer of session 12 after reading the committed range `3949f3c6`..`5178df03` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Seven single-parent commits, per-commit insertions 489, 467, 22, 10, 66 and 98 for the six before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own delegation source and both committed copies are 41462 bytes at `77a872f3e49783abf951a5a6e84a589d85900f326c491d8ffd80b3db906f7954` and compare BYTE-EQUAL; per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` at C1 is 2422 bytes byte-identical to the PLAN21 slice, 44 lines against the cap of 50, with `## Goal` and `## Next Steps` each exactly once; all SIX slices occur EXACTLY ONCE in their targets and a sweep for all twelve marker strings over the six target files returns ZERO for every file. G3 HELD OVER THREE APPENDS: for `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` the committed post-blob equals `pre` plus ONE newline plus the slice EXACTLY, with the joining byte read back from the post blob rather than assumed; the structural reader counted N from the slice itself — 2, 3 and 7 paragraphs — and matched the last N blank-line units of each whole post-file IN ORDER; all three NEGATIVE CONTROLS were flipped inside the FIRST appended paragraph per §3 item 36 and BOTH readers rejected all three while accepting all three truths. The reviewer's FIRST byte reader used the wrong append formula and could not fail, which made its control vacuous; it was rewritten and re-run before this verdict was written, and the figures above are from the reader that can fail. `^Gate: ` rose 42 to 43; `^Gate: F275 R20 `, `^Note: F275 R21 ` and `^Landed: R-0862 ` each occur EXACTLY ONCE, and `^## DECISION F275 D10 ` exactly once in `.agent/decisions.md`. THE OPEN SET WAS 88 BY DISTINCT ID AT BOTH the base and C4 — registrations 94, resolutions 6 — with distinct `Landed:` ids rising 34 to 35 and never subtracted, which is the correct reading of a round that resolves a finding by a `Landed:` line the reviewer has not yet converted to `Done:`. G4, THE ROUND'S LOAD-BEARING GATE: the three moved spans are 580, 416 and 234 bytes at `b2b0a497…`, `be206d7b…` and `f05b4d33…`, each occurring EXACTLY ONCE in the new `packages/common/public_text_redaction.py` at C4 and ZERO TIMES in `packages/orchestration/provider_trust.py`, and the block's own composition recipe — the HEADER21 slice followed by the three spans read from the base blob by line number — reproduces the committed file byte for byte at 2965 bytes and `24d64ed1b093dc1e3c190164c1e85f5ae672d22adead20c30b5b680b22226d9c`, the two figures the block stated. All five moved names are defined exactly once in the new module and zero times in the old, and a sweep of every tracked `.py` file confirms no file outside `provider_trust.py` still imports them from it, so the move is byte-identical and complete rather than a copy. G5: the redaction still bites from its new home — control exit 0 at 261 passed, the mutated `_scrub_public` exit 1 at 5 failed and 256 passed reaching THREE different modules, revert exit 0 at 261 passed, worktree porcelain empty. G6 DISCHARGES R-0862's FIX CLAUSE WITH THE COLOUR IT ASKS FOR: control exit 0 at 6 passed, and forcing the loop-guard branch of `_routing_plan` unreachable gives exit 1 with EXACTLY ONE failure, the new `test_loop_guard_forces_human_review_tier`, reading `assert 'local_advisor_preferred' == 'human_review_required'`. G7: the guards 151 passed, the canary 42, and THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18455 passed, 23 skipped and ZERO failed; the arithmetic closes by the ID SET at 18477 to 18478, EXACTLY ONE id ADDED and NONE removed, the added id being the new pin, and 18455 plus 23 equals 18478. Ruff is clean over the eleven `.py` paths of the change set and reads `Found 24 errors.` at BOTH revisions with an IDENTICAL per-file distribution over 16 files, none of them touched by this round; the reviewer's first parser matched nothing and made that comparison vacuous, so it was rewritten to parse ruff's arrow-form output and paired with a RED CONTROL that confirms the comparison can fail. G8: no `.agent/STOP`, porcelain EMPTY, ONE worktree, the branch correct, and the C3..C4 path set matching the block's change set plus `.agent/live_review.md`, whose second write in the same round the worker declared. ALL EIGHT DECLARED DEVIATIONS ARE SUSTAINED. Three are the reviewer's own and are recorded as slips rather than findings: the block's G3 append formula admits two parses, its gate listing implied G2 could run at C1 when two of its slices land at C4, and its G5 node-set note named `token_economy.py` among the modules whose tests go red when they do not. The worker's own five are sound, and the best of them is a refusal: R-0843's prose sweep turned up a comment in `real_test_execution.py` about "parity with the rest of the orchestration package", which the worker examined, judged still true because nine orchestration modules still reference those helpers, declined to edit as scope drift, and flagged for the reviewer to overrule — which is what a second reading is for. NO FINDING IS RESOLVED BY THIS GATE; R-0862's `Landed:` line awaits the reviewer's `Done:` text.

- R-0866 — Medium, DELETING THE PROVIDER TRUST GATE TAKES THE ONLY ROUTE BY WHICH AN EXTERNAL CANDIDATE ENTERS A SELF-IMPROVEMENT ATTEMPT, AND THE SURVIVING RAIL PARKS IN A STATE IT CANNOT LEAVE. Raised by the reviewer while authoring F275 round 22 and registered by that round's ledger commit, because operator RULE 3 in `docs/roadmap/features/T2_F275.md` T001 requires a deletion that takes away a behaviour a user could observe to register a finding naming the behaviour and the feature that inherited the idea. THE MEASUREMENT, taken at `5178df03` in an applied worktree. `packages/orchestration/self_dogfood_execution.py` SURVIVES — it is not on F260's Design list — and it is reachable from the CLI through `apps/cli/commands/self_cmd.py`, which calls both `start_self_execution` and `reconcile_self_attempt`. Its documented rail runs `approved → request_prepared → awaiting_external_candidate → [human relays the request; the candidate re-enters via provider intake-repair] → Trust Gate → materialized PENDING intent → approval → apply → proof → completed`. Round 22 deletes `remedy provider intake-repair` with the gate behind it, and the ONE piece of code that moved an attempt past `awaiting_external_candidate` was the candidate-linking block in `reconcile_self_attempt`, which read `load_trust_reports` from the dying module. After this round an attempt that reaches `awaiting_external_candidate` STAYS there: the states beyond it are not dead code, because they still run for an attempt whose `patch_intent_id` is already on disk, but no NEW attempt can acquire one. THE INHERITING FEATURE IS NONE, DELIBERATELY, and that is not this round's improvisation — DECISION F260 D3's mapping in `docs/roadmap/features/T2_F260.md` reads "external builder → none, deliberately", so the loss is what F260 planned rather than a surprise this round created. What is NOT covered by that mapping, and is why this finding exists, is the residue: a surviving, CLI-reachable state machine now has a terminal state its own vocabulary calls transitional, and two user-facing `next_safe_action` strings had to stop naming a command that no longer exists. FIX CLAUSE, binding on the round that drafts DECISION F260 D3: name this id in that paragraph, and rule whether `AttemptState`'s post-`AWAITING_EXTERNAL_CANDIDATE` members and the `self_awaiting_candidate` situation key in `orchestrator_brain.py` are kept as a degraded rail or retired with a second dated decision — this round deliberately keeps them, because retiring a surviving module's vocabulary is a product change and not a deletion.

- R-0867 — Medium, `verify_provider_patch_material` LOSES TWO OF ITS SEVEN CHECKS AND ITS `ok` BECOMES STRICTLY EASIER TO SATISFY, AND THE MODULE AROUND IT IS LEFT WITH ONE REACHABLE FUNCTION AND A THIRD OF ITS TESTS. Raised by the reviewer while authoring F275 round 22, under the same operator RULE 3. THE MEASUREMENT, taken at `5178df03`. `packages/orchestration/provider_patch_material.py` SURVIVES — it is not on F260's Design list — and takes exactly FOUR names from the dying pair, measured by resolving its import statements rather than counted from an earlier session's note, which had six because it was taken before F275 round 21 moved two redaction helpers out. All four feed checks inside `verify_provider_patch_material`: `validate_paths` with `Severity` gives `paths_safe`, and `get_trust_report` with `TrustStatus` gives `trust_report_accepted`. `v.ok` is `all(checks.values())`, so removing two checks makes it EASIER to satisfy — a weakening in the UNSAFE direction, and the opposite of the fail-safe degradation DECISION F275 D9 installed one round earlier. It is nonetheless the right move under RULE 3, because the alternative is copying the deleted module's code into a survivor, and because the function is UNREACHABLE: walking every call site in the surviving tree gives NO caller under `packages/` or `apps/`, only its own tests. The same walk shows `materialize_provider_repair`, `load_material_manifest`, `revoke_material`, `read_material_patch` and `export_materialization_result_json` have no caller at all, and that `load_materials` — called by `orchestrator_brain.py` and `ui_server.py`, and a pure read of material already on disk — is the ONE reachable function left, because the command that created material dies with the handler. Round 22 additionally deletes three of that module's five test classes, because every one of them reached its subject through `provider intake-repair`. FIX CLAUSE, binding on the round that drafts DECISION F260 D3: name this id and rule which feature reaps `provider_patch_material.py`, whose remaining job is reading material that nothing can now create; until that ruling lands, no round may treat `verify_provider_patch_material`'s weakened `ok` as a safety property.

- R-0868 — Low, THE CLUSTER DELETION MAP AND ORDER RATCHETS BECOME GATES THAT CANNOT FAIL THE MOMENT `CLUSTER_MODULES` EMPTIES, AND THE REPAIR-REQUEST BUILDER IS LEFT PREPARING A PACKAGE NO COMMAND CAN IMPORT. Two consequences of round 22 that share one cause — the deletion finishing — and one id, per `docs/agents/planner_reviewer_prompt.md` §3 item 30. FIRST, THE VACUOUS GATES, measured by the reviewer at `5178df03` with the deletion applied: with `CLUSTER_MODULES` set to the empty tuple, `tests/orchestration/test_cluster_deletion_map.py` and `tests/orchestration/test_cluster_deletion_order.py` pass at 4 and 2 tests, and every one of those six assertions quantifies over an empty set, so not one of them can ever go red again. That is the R-0438 class arriving through success rather than through a typo: the scaffolding F274 built to BOUND this deletion has no work left, and DECISION F274 D1's ruling that the reachability test is a RATCHET does not reach these two, which measure the cluster rather than the product. SECOND, `packages/orchestration/repair_request_builder.py` SURVIVES and its purpose is to prepare a package for an external actor whose answer re-entered through `provider intake-repair`; round 22 removes five advertisements of that command from it, including the numbered steps inside the request text a human is handed and a line `apps/cli/commands/repair_cmd.py` printed to the terminal, and what remains is a package builder with no importer. FIX CLAUSE, binding on the round that drafts DECISION F260 D3, which is the last round of this feature whose change set already contains `tests/orchestration/` and a roadmap file: retire `cluster_deletion_map.txt`, `test_cluster_deletion_map.py`, `test_cluster_deletion_order.py` and `.agent/f275_deletion_order.md` together, or record a dated decision saying why an empty ratchet is kept; and name the feature that reaps `repair_request_builder.py`. Low rather than Medium because nothing on disk is WRONG — the gates pass honestly and the builder still builds — and what is missing is only their reason to exist.

Note: F275 R22 — new evidence for the OPEN finding R-0864, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30. R-0864 records that a guard's negative assertion names a test file that no longer exists, so that entry can never fail again. MEASURED AT `5178df03` by the reviewer: `CLUSTER_COMMAND_HANDLERS` in `tests/orchestration/test_cluster_deletion_map.py` names seven handler paths and FIVE of them have no file on disk — `dogfood_cmd.py`, `overnight_mission_cmd.py`, `progress_cmd.py`, `repair_loop_v2_cmd.py` and `self_repair_cmd.py`, each deleted by an earlier round of this feature. The tuple is used only as an EXCLUSION set by `_excluded_paths()`, so a stale entry never matches and nothing goes red; unlike `CLUSTER_MODULES`, which has `test_every_cluster_module_still_resolves_to_a_file_on_disk` to hold it honest, no test asserts these paths resolve. Round 22 does not repair it, because the same round's R-0868 asks whether the whole file should be retired and repairing a tuple that may be deleted is work spent twice. The fix travels with R-0868's clause on the DECISION F260 D3 round.
<<<END LEDGER22>>>

<<<BEGIN SLIPS22>>>
2026-09-10 · F275 R21 · The round 21 block's G3 ordered the committed post-blob to equal `pre + newline + slice + newline`. An authored slice extracted between marker lines already ENDS in a newline, so that formula admits two parses and only one of them reproduces the repository's actual append convention. The worker picked the correct parse, verified it against round 20's landed append at `85379a77` before applying anything, and declared the ambiguity; the reviewer then made the SAME wording bite in its own re-gate, where a byte reader built on the literal parse could never accept the truth, which made its negative control vacuous until it was rewritten. The lesson is that an append formula names the joining byte and the slice as extracted — "post equals pre, then one newline, then the slice exactly as extracted" — and orders the joining byte read back from the post blob rather than asserted.
2026-09-10 · F275 R21 · The round 21 block listed its gates in the order G1 to G8 and required "every gate runs at or before C4", while its G2 covered six slices of which two, HEADER21 and TEST21, only land at C4. G2 therefore could not run at C1 as the ordering implied, and the worker ran it after C4 and declared the reordering. Nothing was measured wrongly, because G2 reads committed blobs either way. The lesson is that a gate covering slices that land at different commits names the LAST commit it can honestly run at, rather than inheriting a position from the order the gates happen to be written in.
2026-09-10 · F275 R21 · The round 21 block's G5 said the mutation's red set "reaches at least `real_test_execution.py` and `token_economy.py`", carried over from the previous session's handoff. The reviewer's own applied dry run had already measured the five red tests and none of them is in `test_token_economy.py`; the modules that actually go red are `real_test_execution.py`, `orchestrator_brain.py` and `provider_trust.py`. The worker reproduced the correct set and the block's own later sentence named it correctly, so the round lost nothing. The lesson is that a sentence inherited from a prior session's prose is re-measured before it is repeated, even when the same block already carries the measured version of it two lines away.
<<<END SLIPS22>>>

<<<BEGIN DECISION22>>>
## DECISION F275 D11 (2026-09-10) — the three survivors of the Provider Trust Gate degrade, and none of them is deleted, stubbed or copied into

CONTEXT. Round 22 deletes `packages.orchestration.provider_trust` and
`packages.orchestration.provider_trust_verification`, the last component of
`.agent/f275_deletion_order.md`, together with `apps/cli/commands/provider_cmd.py` and the
whole `provider` command group. That group carries `remedy provider intake-repair`, and the
reviewer measured at `5178df03` that it is the ONLY command anywhere in the product by which
an external candidate enters Remedy. Three surviving modules are built on it, and none of
them is on F260's Design list, so "Do not touch" forbids deleting any of them.

THE RULING, in three parts. Each is RULE 3 applied literally — the survivor loses the call
site and never gains a copy — with a finding for what the user can no longer do.

(a) `self_dogfood_execution.py`. Its `reconcile_self_attempt` loses the candidate-linking
    block that read the dying module's trust reports, and with it the only code that moved
    an attempt past `AWAITING_EXTERNAL_CANDIDATE`. The states beyond that one are KEPT, not
    stubbed: they still run for an attempt whose `patch_intent_id` is already on disk, so
    this is degraded reachability rather than dead code. Two user-facing `next_safe_action`
    strings stop naming the deleted command and report a read instead. R-0866 records the
    loss; DECISION F260 D3 already maps the external builder to "none, deliberately", so
    there is no inheriting feature to name and that is deliberate rather than an omission.

(b) `repair_request_builder.py`. It prepares a package for an external actor and printed
    five instructions to import the answer, one of them inside the request text a human is
    handed and one of them printed to the terminal by `apps/cli/commands/repair_cmd.py`. All
    five go, and the `output_intake_command` and `trust_gate_command` fields are REMOVED
    rather than emptied, because a printed label with nothing after it is a worse surface
    than no label. The package still packages evidence; what it no longer claims is a round
    trip. R-0868 records that it now has no importer.

(c) `provider_patch_material.py`. `verify_provider_patch_material` loses `paths_safe` and
    `trust_report_accepted`, which makes its `ok` STRICTLY EASIER to satisfy. That is a
    weakening in the unsafe direction and it is accepted here only because the reviewer
    measured that the function has NO caller under `packages/` or `apps/` once the pair
    dies, and because the alternative — copying `validate_paths` and the trust reader into a
    survivor — is what RULE 3 and AGENTS.md's Scope Control forbid by name. R-0867 records
    it and forbids any later round from treating that weakened `ok` as a safety property.

ALTERNATIVES CONSIDERED, AND WHY EACH LOSES.
(1) Delete the three survivors too. Rejected: none is on F260's Design list and "Do not
    touch" says no module outside it is deleted. It would also be the largest unplanned
    scope increase this feature has taken.
(2) Keep the deleted checks by copying `validate_paths` and the trust reader into
    `provider_patch_material.py`. Rejected: that is the copy RULE 3 exists to prevent, and
    it would resurrect a dying module's code under a new name.
(3) Make the lost checks permanently False so `verify_provider_patch_material` refuses —
    the fail-safe shape DECISION F275 D9 used for `token_economy.py`. Rejected here, and the
    difference from D9 is worth stating: D9's survivor was REACHABLE and its degraded answer
    was consulted, so refusing was the safe answer to a live question. This function has no
    caller, so a permanently-False check would be dead weight that reads like a guard.
(4) Stop `start_self_execution` before `AWAITING_EXTERNAL_CANDIDATE`, so no attempt ever
    parks in a state it cannot leave. Rejected: that is a product redesign of a surviving
    module, not a deletion, and it would silently change what `remedy self execute` does.
    R-0866's fix clause routes the question to the DECISION F260 D3 round instead.

CONSEQUENCE. Round 22 is NOT a deletion round under amend0906-triage-throughput: its change
set edits lines under `packages/`, `apps/` and `tests/`, so the four-measurement shortcut
does not apply and a mutation red-proof is ordered in full. Three findings are registered
and none is resolved. `CLUSTER_MODULES` becomes the empty tuple, which exhausts T001's
module list and makes two ratchets vacuous — recorded as R-0868 rather than repaired here,
because retiring them is bookkeeping that belongs with DECISION F260 D3.

REVERSE THIS DECISION by restoring the two modules and their handler from git history and
re-pointing the three survivors at them; the findings would then be resolved as obsolete
rather than fixed.
<<<END DECISION22>>>
