── STEP T001 (round 21 of n) — F275 ──────────────────────────
Goal:        Move the five redaction names that seven SURVIVING modules import out of the
             dying `provider_trust.py` and into a new `packages/common/public_text_redaction.py`
             BYTE-IDENTICALLY, repoint every importer, and discharge two fix clauses that
             bind this round. No file is deleted. The pair itself dies in round 22.
Bundle:      C0a save the block · C0b mirror the block · C1 the plan · C2 the record ·
             C3 DECISION F275 D10 · C4 the move, the repoints, the pin and the two fix
             clauses · C5 the handback.
Handback:    completion report + rewrite `.agent/handoff.md`.
(the line below is the box rule: the character U+2500 repeated 62 times, nothing else)
──────────────────────────────────────────────────────────────

BASE. This round's base is `3949f3c698fe5cef089ff0bd455fffac0fdd1f5a`, short `3949f3c6`.
Every reading below was taken by the reviewer at that commit, in an applied dry run inside
a disposable worktree, and none of it is a prediction unless it says so.

WHY THIS ROUND EXISTS RATHER THAN GOING STRAIGHT TO THE DELETION. Round 22 deletes
`packages.orchestration.provider_trust` and `packages.orchestration.provider_trust_verification`,
the last component of `.agent/f275_deletion_order.md`. Seven modules that SURVIVE that
deletion import `_scrub_public` from the dying module and three of them also import
`_safe_path_label`; the DECISION21 slice below names all seven, measured by an `ast` sweep.
Those helpers mask secrets, home-ish absolute paths and tracebacks in every publicly
surfaced string, so deleting the call sites
would REMOVE REDACTION from seven survivors — a weakening in the unsafe direction and the
opposite of round 20's fail-safe degradation. Operator RULE 3 forbids a stub, a shim or a
copy, so the answer is DECISION F275 D1's precedent: a byte-identical MOVE, done in its own
round so the deletion commit stays a deletion.

# ============================ THE CHANGE SET ============================
# Nothing outside this list is edited, created or deleted. G8 compares the set you measure
# against it; the block states no total, so the numeral in your handback is yours.
#
# NEW
#   packages/common/public_text_redaction.py            composed, see C4 step 1
#
# REPOINTED — one import line each unless noted
#   packages/orchestration/orchestrator_brain.py        1/1
#   packages/orchestration/self_dogfood.py              1/1
#   packages/orchestration/self_dogfood_execution.py    1/1
#   packages/orchestration/repair_request_builder.py    1/1
#   packages/orchestration/real_test_execution.py       1/1
#   packages/orchestration/provider_patch_material.py   1/2   block import split
#   packages/orchestration/provider_trust_verification.py 1/2 block import split
#   packages/orchestration/token_economy.py             1/2   repoint + R-0855 fix clause
#   packages/orchestration/provider_trust.py            8/31  the three chunks leave
#
# RATCHETS AND THE PIN
#   tests/orchestration/cluster_deletion_map.txt        0/3   REGENERATED, never line-edited
#   tests/orchestration/import_reachability_allowlist.txt 1/0
#   tests/orchestration/test_orchestrator_brain.py      22/0  the TEST21 slice
#
# STATE
#   .agent/plan.md .agent/live_review.md .agent/prose_slips.md .agent/decisions.md
#   .agent/authored/f275-r21.md .agent/last_block.md .agent/handoff.md
#
# Over the TRACKED paths above — that is, every path listed except the new file, which is
# untracked at the base — the reviewer's applied dry run measured 39 insertions against 45
# deletions. The insertion figures
# for the two block-import splits and for `provider_trust.py` are PREDICTIONS about
# wording, not measurements you can be held to; every deletion figure is fixed by its
# anchor. Report what you measure.

# ============================ CONSTRAINTS ============================
1. Apply every authored slice BYTE FOR BYTE, extracted from the COMMITTED C0a blob between
   its marker lines with the markers EXCLUDED. Never retype a slice, never edit one. If a
   slice is wrong, apply it as given and say so in the handback.
2. The three MOVED CHUNKS are NOT retyped either. They are extracted BY LINE SPAN from the
   committed base blob `3949f3c6:packages/orchestration/provider_trust.py`, which is how
   byte-identity is proved mechanically rather than claimed.
3. C3 commits DECISION F275 D10 BEFORE C4 touches any production file, exactly as round
   20's D9 preceded its first `git rm`.
4. NO FILE IS DELETED THIS ROUND, and no command, catalog entry or cockpit section is
   removed. `git rm` does not appear in this round.
5. Two pre-existing dangling `related=` references in `apps/cli/command_catalog.py` —
   `mission.run -> dogfood.run-loop` and `repo.status -> readiness.show` — are held by
   R-0859 and are NOT repaired here. This round must add none.
6. The 24 pre-existing repo-wide `ruff` errors are NOT repaired here. This round must add
   none.
7. You write NO verdict, NO `Done:` paragraph and NO finding. R-0862 is RESOLVED by C4, so
   C4 writes exactly one line `Landed: R-0862 — <one line: what changed, which commit>` and
   nothing else; the reviewer replaces it with the authored `Done:` text at the next gate.
   R-0855 is NOT resolved — its fix clause binds every remaining deletion round of this
   feature and this round discharges only one instance of it, so write no `Landed:` line
   for it.
8. All disposable work lives under the gitignored `.remedy-wt/`. `/tmp` is denied in this
   environment. Remove every worktree and every scratch `.py` file before the final
   `git status --porcelain`.
9. The full suite runs in the PRIMARY CHECKOUT, serially, never `-n auto` and never in a
   worktree: under `-n auto` the `ui_server` command-channel tests race for a port, and in
   a fresh worktree `apps/ui/node_modules` is cold, which is the only reason the reviewer's
   dry run reddened `TestVitestFrontendTestFoundation::test_vitest_passes` on a first pass
   there — it passed on the second pass in that same tree.

# ============================ C4 — THE ORDERED WORK ============================

STEP 1 — CREATE `packages/common/public_text_redaction.py` BY COMPOSITION.
The file is exactly, with no other bytes:

    HEADER21  +  span(530,540)  +  "\n\n"  +  span(516,523)  +  "\n\n"  +  span(601,606)

where HEADER21 is the authored slice below and `span(a,b)` is lines a to b INCLUSIVE,
1-indexed, of the committed blob `3949f3c6:packages/orchestration/provider_trust.py`, read
with `git show` and split with `splitlines(keepends=True)`. The three spans are, at that
commit: 530-540 the three pattern constants (580 bytes), 516-523 `_scrub_public` (416
bytes), 601-606 `_safe_path_label` (234 bytes). Composed, the file is 2965 bytes at sha256
`24d64ed1b093dc1e3c190164c1e85f5ae672d22adead20c30b5b680b22226d9c`. The reviewer ran this
exact composition and it reproduced the dry run's file byte for byte.

STEP 2 — THE SINGLE-LINE REPOINTS. Each FROM occurs EXACTLY ONCE in its file at
`3949f3c6`; the reviewer counted each one. Every pair below is a REWRITE, not an append:
the containment test was run per pair and printed `TO contains FROM: false` for each, so
§4.9's append obligation does not apply and a FROM-zero count after the edit does.

  (a) packages/orchestration/orchestrator_brain.py
  (b) packages/orchestration/self_dogfood.py
  (c) packages/orchestration/self_dogfood_execution.py
  (d) packages/orchestration/repair_request_builder.py
      FROM (identical in all four, four leading spaces, one line):
          from packages.orchestration.provider_trust import _scrub_public
      TO:
          from packages.common.public_text_redaction import _scrub_public

  (e) packages/orchestration/real_test_execution.py
  (f) packages/orchestration/token_economy.py
      FROM (identical in both, column zero, one line):
      from packages.orchestration.provider_trust import _safe_path_label, _scrub_public
      TO:
      from packages.common.public_text_redaction import _safe_path_label, _scrub_public

STEP 3 — THE BLOCK-IMPORT SPLITS. In each file the existing parenthesised
`from packages.orchestration.provider_trust import (...)` block loses `_safe_path_label`
and `_scrub_public` from its name list and KEEPS every other name in place and in order; a
new single line
`from packages.common.public_text_redaction import _safe_path_label, _scrub_public`
is inserted DIRECTLY ABOVE the surviving block — where `ruff`'s isort rules put it, because
`packages.common` sorts before `packages.orchestration`.
  (g) packages/orchestration/provider_patch_material.py — the block keeps
      `Severity`, `TrustStatus`, `validate_paths`.
  (h) packages/orchestration/provider_trust_verification.py — the block keeps
      `ProviderCandidateRepair`, `Severity`, `_is_docs_path`, `_is_test_path`,
      `_read_quarantined_raw`, `parse_candidate`, `scan_secrets`.

STEP 4 — `packages/orchestration/provider_trust.py` LOSES THE MOVED CHUNKS AND GAINS ONE
IMPORT. Delete span(516,523), span(530,540) and span(601,606) TOGETHER WITH the two blank
lines that follow each of them, so the surrounding section comments keep their usual two
blank lines above and below and no triple blank line is created. The module still USES all
five names — `scan_secrets` reads the three patterns, `_safe_text` calls `_scrub_public`,
`validate_paths` calls `_safe_path_label` — so insert directly after the line
`from uuid import UUID, uuid4`, separated from it by one blank line:

    from packages.common.public_text_redaction import (
        _ABS_PATH_RE,
        _SECRET_PATTERNS,
        _TRACEBACK_RE,
        _safe_path_label,
        _scrub_public,
    )

This is a genuine use, not a re-export shim: nothing outside this file imports those names
from it after step 3.

STEP 5 — R-0855's FIX CLAUSE ON `packages/orchestration/token_economy.py`, which binds the
round that next edits this file, and step 2(f) does. DELETE the single line, which occurs
exactly once at `3949f3c6` and carries four leading spaces:

    # Approval: unknown context OR hard-safety floor OR over-budget OR over the approval threshold.

Not one of the four disjuncts it names is a term of the expression beneath it since round
20. The round-20 comment two lines below it already states the truth, and `over_threshold`
directly beneath keeps its reader. THEN RUN R-0843's COUNTER-MEASURE over the OTHER eight
surviving production files of this change set: sweep each for PROSE the move falsified — in
the file's own words, not in the moved identifiers — and report what you found, INCLUDING
"nothing" where that is the answer. The reviewer's dry run found nothing outside this one
line; a second reading is the point.

STEP 6 — THE TEST PIN, R-0862's FIX CLAUSE. Apply the TEST21 slice into
`tests/orchestration/test_orchestrator_brain.py`, inserted so that it sits between
`test_candidate_generation_external_builder` and `test_routing_never_executes` inside
`class TestModelRouting`. The insertion point is the line `    def test_routing_never_executes(self, env):`
which occurs exactly once in that file at `3949f3c6`; the slice goes DIRECTLY ABOVE it and
the slice's own trailing blank line supplies the separation.

STEP 7 — THE RATCHETS.
  `tests/orchestration/cluster_deletion_map.txt` is REGENERATED from the live import graph,
  never line-edited: import `measured_edges()` from `tests/orchestration/test_cluster_deletion_map.py`,
  keep the file's comment header verbatim, and write one `<module> <- <consumer path>` line
  per edge in sorted order. At `3949f3c6` the file holds EIGHT edges; after steps 2 to 4 the
  reviewer measured FIVE, the three that leave being `provider_trust <- real_test_execution.py`,
  `<- repair_request_builder.py` and `<- token_economy.py`. Those three modules import
  nothing else from the dying pair; the other four still do.
  `tests/orchestration/import_reachability_allowlist.txt` gains the single line
  `packages.common.public_text_redaction`, in sorted position between
  `packages.common.path_redaction` and `packages.common.secure_fs`. The new module is
  reachable from the D11 (c) entry points through seven importers, so assertion (b) reds
  without this line.

# ============================ DONE WHEN ============================
Run every gate as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL exit code.
Report ONE line per gate in the handback. Every gate below runs at or before C4, so the
handback C5 writes can quote all of them.

G1 TRANSPORT — one digest comparison and nothing else. The delegation source
`.remedy-wt/f275-r21.md`, the committed `.agent/authored/f275-r21.md` and the committed
`.agent/last_block.md` are all the same byte length at the same sha256 and compare
BYTE-EQUAL. C0a copies with `shutil.copyfile`; C0b takes its bytes from the COMMITTED C0a
blob via `git show`, never from the scratch file. State that per §3 item 37 this chain
covers those three artefacts and claims nothing about the emitted bytes.

G2 THE PLAN AND THE SLICES — `.agent/plan.md` at C1 is BYTE-IDENTICAL to the PLAN21 slice,
under the AGENTS.md cap of 50 lines, with `## Goal` and `## Next Steps` each occurring
exactly once. EVERY slice this block carries occurs EXACTLY ONCE in its own target, and a
grep for every one of this block's marker strings over every one of those targets returns
ZERO for each target. Report the slice count and the marker count YOU measured.

G3 THE RECORD — the three appends, each with a byte reader, a structural reader and a
negative control. For LEDGER21, SLIPS21 and DECISION21: the committed post-blob equals
`pre + newline + slice + newline` exactly; the structural reader COUNTS N from the slice
itself and compares the LAST N blank-line units of the whole post-file IN ORDER against the
slice's N paragraphs with a per-unit sha256 on both sides; the unit BEFORE that region lies
inside the pre blob; and ONE byte is flipped in memory inside the FIRST appended paragraph
of each append, which BOTH readers must REJECT while BOTH ACCEPT the truth. Then report
`^Gate: ` before and after, `^Gate: F275 R20 ` exactly once, `^Note: F275 R21 ` exactly
once, `^## DECISION F275 D10 ` exactly once, and THE OPEN SET BY DISTINCT ID at the base
and at C2 with `Landed:` never subtracted.

G4 THE MOVE IS BYTE-IDENTICAL — the load-bearing gate of this round. Re-read the three
spans from `3949f3c6:packages/orchestration/provider_trust.py`, and show that each occurs
EXACTLY ONCE in the new `packages/common/public_text_redaction.py` at C4 and ZERO TIMES in
`packages/orchestration/provider_trust.py` at C4. Show that the composition of step 1
reproduces the committed new file byte for byte. Report the committed file's byte length
and sha256 beside the two figures this block states.

G5 REDACTION STILL BITES FROM ITS NEW HOME — a mutation red-proof, inside a disposable
worktree created at C4, with `__pycache__` purged and `python3 -B` before every run.
  (a) Show `import packages.common.public_text_redaction` resolves to the file INSIDE that
      worktree, so no editable install shadows it.
  (b) The revert target BY PATH is `<worktree>/packages/common/public_text_redaction.py`.
      The mutation inserts the line `    return text` directly above the line
      `    scrubbed = text`, which occurs exactly once in THAT file.
  (c) CONTROL, unmutated, over this node set — the reviewer measured exit 0, 261 passed:
      tests/orchestration/test_real_test_execution.py tests/orchestration/test_token_economy.py
      tests/orchestration/test_repair_request_builder.py tests/orchestration/test_self_dogfood.py
      tests/orchestration/test_self_dogfood_execution.py tests/orchestration/test_provider_patch_material.py
      tests/orchestration/test_orchestrator_brain.py tests/orchestration/test_provider_trust.py
      tests/test_trust_report.py
  (d) MUTATION over the SAME node set — the reviewer measured exit 1, 5 failed, 256 passed,
      and the five reach three different modules: two in `test_real_test_execution.py`, one
      in `test_orchestrator_brain.py` and two in `test_provider_trust.py`. NAME the tests
      that went red. `test_token_economy.py` does NOT go red and is not expected to.
  (e) REVERT BY PATH, purge, re-run, and show the control figure returns and the worktree
      porcelain is EMPTY.
STOP CONDITION: if (d) comes out GREEN, do not push. Reset the unpushed C4, hand back with
the transcript, and say so — a green mutation there means seven survivors lost their
masking silently.

G6 THE HUMAN-REVIEW TIER IS PINNED — R-0862's fix clause requires the colour, not just the
test. In the same disposable worktree: the CONTROL over
`tests/orchestration/test_orchestrator_brain.py::TestModelRouting` and
`::TestAntiLoop` is exit 0 at 6 passed. The MUTATION replaces, in
`<worktree>/packages/orchestration/orchestrator_brain.py`, the two-line condition opening
`_routing_plan` — `    if s.loop_guard.status in (LoopGuardStatus.BLOCK,` and its
continuation line ending `LoopGuardStatus.REQUIRE_HUMAN_REVIEW):` — with `    if False:`.
That two-line form occurs EXACTLY ONCE in that file at `3949f3c6`; the similar one-line
form near the option-scoring code is a DIFFERENT string and must not be touched. The
reviewer measured exit 1 with EXACTLY ONE failure,
`TestModelRouting::test_loop_guard_forces_human_review_tier`, reading
`assert 'local_advisor_preferred' == 'human_review_required'`. Revert and show 6 passed
again. REVERT BY THE EXACT FROM/TO STRINGS, not with `git checkout --`: at the moment this
gate runs the file also carries this round's own repoint, and a checkout would silently
discard it — the reviewer's dry run did exactly that and had to re-apply.

G7 THE GUARDS, THE SUITE AND RUFF.
  (a) The ratchets and the pin — all under `tests/orchestration/`, so pass that prefix with
      each of: `test_cluster_deletion_map.py`, `test_cluster_deletion_order.py`,
      `test_import_reachability.py`, `test_orchestrator_brain.py`, `test_provider_trust.py`,
      `test_provider_trust_verification.py`, `test_token_economy.py`,
      `test_self_dogfood_execution.py`.
  (b) The canary `tests/cli/test_golden_path.py`.
  (c) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY CHECKOUT,
      with C4 committed. Close the arithmetic against the base by a NODE-ID SET DIFFERENCE
      of two `--collect-only` runs, not by counting functions. The reviewer's expectation,
      stated as an expectation: exactly ONE id is ADDED,
      `tests/orchestration/test_orchestrator_brain.py::TestModelRouting::test_loop_guard_forces_human_review_tier`,
      and NONE is removed. Report the measured sets.
  (d) `python3 -B -m ruff check` over every `.py` path of the change set — the
      reviewer measured `All checks passed!` — and the repo-wide PARITY reading over
      `packages`, `apps` and `tests` at BOTH the base and C4, taken in a DISPOSABLE
      READ-ONLY worktree for the base and NEVER by writing a base blob over a tracked file.
      The per-file distributions must be identical; report a `diff` of them.

G8 THE TREE — `.agent/STOP` re-read from disk; `git status --porcelain` EMPTY;
`git worktree list` holding ONE entry; the branch correct; `git diff --name-only <C3>..<C4>`
compared AS A SET against the C4 paths this block's change set names, with MISSING and
EXTRA both reported and the size of each set the numeral YOU measured; and
the per-commit insertion count with its parent count for every commit BEFORE C5, each
against the DECISION F104 D1 cap of 500. Compare every `+/-` cell of your `## Commits`
tables CELL BY CELL against `git show --numstat` for its commit and say whether they agree.

# ============================ THE AUTHORED SLICES ============================
# Each slice lies between its BEGIN and END marker line; the marker lines themselves are
# EXCLUDED from the slice and never reach any file. G2 asks you for their number.

<<<BEGIN PLAN21>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 21 prepares the last deletion instead of performing it. The five redaction names that
seven SURVIVING modules import from the dying `provider_trust.py` — `_scrub_public`,
`_safe_path_label` and the three patterns they read — move BYTE-IDENTICALLY into the new
`packages/common/public_text_redaction.py` under DECISION F275 D10, and nine importers
repoint. Nothing is deleted. The round also discharges R-0862's fix clause with a positive
pin on the human-review routing tier and R-0855's clause on `token_economy.py`, and books
round 20's PASS verdict.

## Next Steps

1. The `provider_trust` / `provider_trust_verification` pair itself, the last component of
   `.agent/f275_deletion_order.md`. Its first commit is a dated DECISION on the self-dogfood
   external-candidate rail, which loses its only entry point when `provider intake-repair`
   dies.
2. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it. That round
   also discharges R-0843, R-0858, R-0859, R-0860 and R-0864.
3. T002, the atomic record flip, alone, because every later commit's size depends on it.
4. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 88 by distinct id at this round's base `3949f3c6`. This round registers
  none and resolves R-0862. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's
  rather than this feature's, per DECISION F272 D12.
- Worst on this round: seven surviving production modules keep a redaction call whose
  definition moves, so a silent breakage removes masking from public strings. The mutation
  red-proof over the moved definition is ordered in full and its STOP condition blocks the
  push.
- The full suite runs SERIALLY in the PRIMARY checkout. A fresh worktree has a cold
  `apps/ui/node_modules` and reddens the vitest foundation test on a first pass only.
<<<END PLAN21>>>

<<<BEGIN LEDGER21>>>
Gate: F275 R20 — the F275 round 20 entry. VERDICT PASS, written by the planner and reviewer of session 11 after reading the committed range `0d18e58a`..`d991ecaa` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs, and booked here by round 21 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, carried from the pushed `.agent/handoff.md` at `3949f3c6`. The worker's report was evidence for no line of it. Seven single-parent commits, per-commit insertions 483, 446, 20, 10, 72 and 45 for the six before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own delegation source and both committed copies are 40139 bytes at `1b8d1b0bf7892a84ec83b3a581267bd557de89118b5df0dfa49cbe95db84cc61` and compare BYTE-EQUAL; per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` at C1 is 2442 bytes byte-identical to the PLAN20 slice, 44 lines against the cap of 50, with `## Goal` and `## Next Steps` each exactly once; all four slices occur EXACTLY ONCE in their targets and a sweep for all eight marker strings over the four target files returns ZERO for every file. G3 HELD OVER THREE APPENDS AND WAS PROVED BY WHOLE-FILE IDENTITY RATHER THAN BY ARITHMETIC ALONE: for `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` the committed post-blob equals `pre + newline + slice + newline` EXACTLY; the structural reader counted N from the slice itself — 3, 2 and 7 paragraphs — and matched the last N blank-line units of each whole post-file IN ORDER; all three NEGATIVE CONTROLS were flipped inside the FIRST appended paragraph per §3 item 36 and BOTH readers rejected all three while accepting all three truths. `^Gate: ` rose 41 to 42; `^Gate: F275 R19 `, `^- R-0865 — `, `^Note: F275 R20 ` and `^## DECISION F275 D9 ` each occur EXACTLY ONCE. THE OPEN SET WENT 87 TO 88 BY DISTINCT ID against registrations 93 to 94 and resolutions 6 to 6, with 34 distinct `Landed:` ids present and never subtracted. G4 IS AGAIN THE GATE THIS ROUND'S OWN GUARD COULD NOT ANSWER, AND IT IS CLEAN: the reviewer re-ran the fifteen-token sweep with its own script over the tracked files outside `.agent/` and `.data/`, measured RAW 6, printed the list in full and not truncated, and every one of the six is history prose under `docs/roadmap/features/` — three in `T2_F260.md`, one each in `T2_F262.md`, `T2_F267.md` and `T8_F151.md`. The spaced forms `remedy route-policy` and `remedy worker registry-` return ZERO hits, so no page anywhere still instructs an operator to run a command that round deleted — the property R-0861's fix clause exists to protect and the one `tests/cli/test_advertised_commands.py` CANNOT establish here, because deleting the whole `route-policy` group removed it from that guard's `GROUPS` and the guard skips what it cannot resolve. The worker ran that guard, got exit 0, and said in its own handback that the pass is not evidence for the round — R-0847 handled correctly rather than relied on. G5's STOP CONDITION DID NOT FIRE, AND IT IS THE ROUND'S MOST LOAD-BEARING READING: in a disposable worktree at C4 the mutated bytes occur exactly ONCE in the named path, the unmutated CONTROL is exit 0 at 72 passed, forcing `d.requires_human_approval` to `False` is exit 1 at 5 failed and 67 passed, and the revert returns exit 0 at 72 passed with the worktree porcelain empty; the five named failures include `TestIntegrity::test_real_unknown_decision_is_safe_under_audit`, that module's own R-0099 audit invariant, so the fail-safe DECISION F275 D9 installs is held by tests that bite rather than by a comment, and approval is now UNCONDITIONAL, which is strictly stricter than the hard-safety floor it replaces. G6: the affected guards 548 passed, the canary 42, the documentation gate 303, and THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18454 passed, 23 skipped and ZERO failed, with a separately measured collection of 18477 equal to 18454 plus 23; THE ARITHMETIC CLOSES BY THE ID SET, 18538 at the base against 18477 at the tip, a fall of exactly 61 being 62 ids REMOVED against 1 ADDED, the 62 being 48 across three deleted test files, 8 parametrized `[route-policy]` cases in `tests/test_grouped_cli.py` generated from the catalog `GROUPS`, 3 in `TestPlaceholderHardening`, 2 in `test_token_economy.py` and 1 in `test_dashboard_cockpit_truth.py`. Ruff is clean over the change set and reads `Found 24 errors.` at BOTH revisions with an IDENTICAL per-file distribution, none in a file that round touched. G7: the SHIPPED catalog reader gives 227 commands in 45 groups against 233 and 46 at the base, `"route-policy"` absent from `GROUPS`, the id sets beginning `route-policy.` and `worker.registry-` both EMPTY, zero duplicate ids, and exactly TWO dangling `related=` references at BOTH revisions, both pre-existing and both held by R-0859, so that round ADDED NONE. G8: no `.agent/STOP`, porcelain EMPTY, ONE worktree, the branch correct, and the C4 path set an EXACT SET MATCH on 23 paths with MISSING and EXTRA both empty. THE SEVEN DECLARED DEVIATIONS ARE ALL SUSTAINED, and the three load-bearing ones are the reviewer's own errors rather than the worker's: the block predicted `token_economy.py` at 22 insertions and 62 deletions against a real 20 and 61; the block's item 4 named only "the two head-docstring paragraphs" while the docstring of `compute_token_economy_decision` asserted Worker Registry facts the same commit falsified, so the worker rewrote it and declared the widening; and G5 ordered the proof "inside a disposable worktree at C4" while its STOP condition ordered a handback "without committing C4", which cannot both hold literally, and the worker resolved it by committing C4, proving at `1abe8ac2` and holding the option of resetting an unpushed commit the red mutation made unnecessary. NO FINDING IS RESOLVED BY THIS GATE.

Note: F275 R21 — new evidence for the OPEN finding R-0855, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30, which orders the open set searched for the DEFECT before an id is minted. R-0855 records that an ordered anchor deletes a definition without sweeping the neighbourhood that definition served, and names three instances. THIS IS A FOURTH, MEASURED BY THE REVIEWER AT `1abe8ac2` while re-gating round 20 and re-confirmed at `3949f3c6`: `packages/orchestration/token_economy.py` still carries a line reading `# Approval: unknown context OR hard-safety floor OR over-budget OR over the approval threshold.` directly above `d.requires_human_approval = True`. Not one of the four disjuncts that comment names is a term of the expression beneath it any more — `hard_safety_requires_approval` does not occur anywhere in the module after round 20, and `unknown_context` is not part of the approval expression at all — while the round's own correct comment sits two lines below it saying the opposite, so the file carries two adjacent comments about one assignment and only the lower one is true. NO GATE COULD SEE IT: `ruff` is clean, the full suite is green, and round 20's fifteen-token sweep does not match the words `hard-safety floor`, because a deletion sweep hunts IDENTIFIERS and this is prose. It is wrong state on disk under `packages/`, which amend0827-process-diet rule 2 reserves an id for, and it is folded into R-0855 rather than given one because the defect, the cause and the fix are the same. THE FIX LANDS IN ROUND 21, whose change set contains that file, together with R-0843's counter-measure — a sweep of EVERY surviving file of that change set for PROSE the change falsified, read in each file's own words rather than in the moved module's identifiers.
<<<END LEDGER21>>>

<<<BEGIN SLIPS21>>>
2026-09-10 · F275 R20 · The round 20 block stated `packages/orchestration/token_economy.py` at 22 insertions and 62 deletions, taken from the reviewer's own applied dry run, and the worker measured 20 and 61, which made the block's bundle totals 47 and 2219 against a real 45 and 2218. Production code is SPECIFIED rather than sliced in this workflow precisely so the worker writes the prose, so a per-file insertion figure quoted from the reviewer's dry run is a PREDICTION about wording and not a measurement the worker can reproduce. The other 22 paths matched to the line, because every one of them is a deletion or a mechanical edit with no prose in it. The lesson is that a block quoting per-file `+/-` for a SPECIFIED production file quotes it as an approximate expectation and says so, or omits the insertion column for that file and keeps only the deletion count, which is determined by the anchors.

2026-09-10 · F275 R20 · The round 20 block's item 4 ordered the two module-docstring paragraphs of `token_economy.py` rewritten and never named the docstring of `compute_token_economy_decision` itself, although that docstring asserted that the function combines "the Worker Registry route policy" and that "a cheap small task under the local-preference threshold recommends a local route" — both falsified by the same commit. The reviewer's own applied dry run HAD rewritten it, as part of the same anchor that removed the imports, so the block's stated deletion figure was only reachable with it included and the worker had to widen the order to meet the number. The worker declared the widening and was right. The lesson is that when a block SPECIFIES a production edit by naming the docstrings it rewrites, it enumerates every docstring the applied dry run touched, and the surest way to enumerate them is to read the dry run's own diff rather than the reviewer's memory of it.

2026-09-10 · F275 R20 · The round 20 block's G5 ordered the red-proof run "inside a disposable worktree at C4" and, in the same gate, ordered the worker to "hand back without committing C4" if the mutation came out green. Those two clauses cannot both be obeyed: a worktree at C4 requires C4 to exist. The worker committed C4, proved in a worktree at `1abe8ac2`, and kept the option of resetting an unpushed commit, which the red mutation made unnecessary; it declared the contradiction rather than silently picking a half. The lesson is that a STOP condition attached to a gate which itself runs at a named commit is written as an instruction to RESET that commit, not to withhold it, because the gate's own recipe already presupposes the commit exists.
<<<END SLIPS21>>>

<<<BEGIN DECISION21>>>
## DECISION F275 D10 (2026-09-10) — the shared redaction helpers MOVE to `packages/common/public_text_redaction.py`, byte-identically, in their own round

CONTEXT. Round 22 deletes `packages.orchestration.provider_trust` and
`packages.orchestration.provider_trust_verification`, the last component of
`.agent/f275_deletion_order.md`. Measured by the reviewer at `3949f3c6` with an `ast` sweep
over `packages/`, `apps/`, `tests/` and `scripts/`: SEVEN modules that survive that deletion
import `_scrub_public` from the dying module — `orchestrator_brain.py`,
`provider_patch_material.py`, `real_test_execution.py`, `repair_request_builder.py`,
`self_dogfood.py`, `self_dogfood_execution.py` and `token_economy.py` — and three of those
seven also import `_safe_path_label`. `_scrub_public` masks secret-like material, home-ish
absolute paths and stack traces in strings that reach public surfaces, which is why R-0083
put it there in the first place.

THE PROBLEM. Operator RULE 3 in `docs/roadmap/features/T2_F275.md` T001 says a surviving
consumer LOSES THE CALL SITE and never gains a copy. Applied literally to these seven, that
would delete REDACTION from seven survivors — a weakening in the unsafe direction, and the
exact opposite of the fail-safe direction DECISION F275 D9 established one round earlier.
RULE 3 exists to stop cluster CAPABILITY being smuggled into survivors under another name;
these are shared safety utilities that happen to live in a cluster file, and the rule was
never aimed at them.

CHOSEN. A BYTE-IDENTICAL MOVE into a new module `packages/common/public_text_redaction.py`,
performed in its own round BEFORE the deletion, following the precedent DECISION F275 D1
already set for shared code in a dying file. Five names move: `_scrub_public`,
`_safe_path_label`, `_SECRET_PATTERNS`, `_ABS_PATH_RE` and `_TRACEBACK_RE`. No name is
renamed, no body is edited, and every call site is unchanged; the move is proved by
extracting the three source spans from the committed base blob rather than by retyping them.
The dying module itself imports them back for the one round it has left, which is a genuine
use — `scan_secrets`, `_safe_text` and `validate_paths` all still call them — and not a
re-export shim, because after the repoints nothing outside that file imports those names
from it.

ALTERNATIVES CONSIDERED, AND WHY EACH LOSES.
(1) Delete the call sites, per a literal RULE 3. Rejected: it removes masking from seven
    survivors. Safety before rule-shape.
(2) Move into the existing `packages/common/path_redaction.py`. Rejected on a measurement:
    that module already defines a module-level `ABS_PATH_RE`, and this move brings an
    `_ABS_PATH_RE` with a different and much narrower regex. Two absolute-path patterns
    whose names differ by one underscore, in one file, with different jobs, is precisely the
    synonym drift AGENTS.md's Code Discoverability Conventions forbid, and the next reader to
    edit the wrong one pays for it. The two modules also do different things: that one
    reduces every path to its bare file name, this one replaces a narrow class of tokens
    with `[redacted-...]` markers.
(3) Move into `packages/orchestration/redaction_patterns.py`. Rejected on a measurement: it
    already defines `_TRACEBACK_RE`, with a looser case-insensitive regex, so a
    byte-identical move would collide and a rename would stop the move being byte-identical.
(4) Rename the five to public names while moving them. Rejected: it changes call sites in
    seven surviving modules, and AGENTS.md forbids mass renames as their own activity.
(5) Do the move inside the deletion commit. Rejected: it would put a new file, nine
    repoints and a two-thousand-line deletion in one commit, and RULE 1's "never split"
    binds the deletion, not the preparation for it.

CONSEQUENCE. Round 21 is not a deletion round under amend0906-triage-throughput: its change
set edits lines under `packages/` and `tests/`, so the four-measurement shortcut does not
apply and a mutation red-proof over the moved definition is mandatory. `packages/common/`
gains one module and `tests/orchestration/import_reachability_allowlist.txt` gains one line,
because the new module is reachable from the D11 (c) entry points through its seven
importers. Three of the eight edges in `tests/orchestration/cluster_deletion_map.txt`
disappear, because `real_test_execution.py`, `repair_request_builder.py` and
`token_economy.py` import nothing else from the dying pair.

REVERSE THIS DECISION by moving the five names back into `packages/orchestration/provider_trust.py`
and deleting `packages/common/public_text_redaction.py` — which is only possible while that
file still exists, so reversing it after round 22 means choosing a different destination
rather than restoring the old one.
<<<END DECISION21>>>

<<<BEGIN HEADER21>>>
"""Secret, absolute-path and traceback masking for strings Remedy surfaces publicly.

WHY THIS IS HERE. These three patterns and the two helpers over them were written for
the Provider Trust Gate (`packages/orchestration/provider_trust.py`, R-0083: never echo
a secret value or an absolute path out of untrusted provider text). Seven modules that
have nothing to do with provider trust came to import them anyway, because masking a
public-facing string is a repository-wide obligation rather than a trust-gate one. F275
round 21 deletes the trust gate, so the helpers move here BYTE-IDENTICALLY — one
implementation, no copy, no shim — and the former host's importers repoint at this
module. DECISION F275 D10 records the move and why this file rather than an existing one.

NOT `packages/common/path_redaction.py`, and the distinction is load-bearing. That module
reduces every absolute path and `file:` URI to its bare file name, for shareable runtime
state and post-mortems; it is about PATHS and it rewrites all of them. This module masks
SECRET-LIKE material, a narrow set of home-ish absolute paths and stack traces, and it
replaces them with `[redacted-...]` markers rather than shortening them. Both would have
carried a module-level constant spelled `ABS_PATH_RE` over two different regexes with two
different jobs, which is exactly the synonym drift AGENTS.md's Code Discoverability
Conventions forbid.

Remedy deliberately does not re-export these under public names: the leading underscore is
the original spelling, every call site already uses it, and renaming five names across
seven modules is the mass rename those same conventions forbid as its own activity.
"""
from __future__ import annotations

import re

<<<END HEADER21>>>

<<<BEGIN TEST21>>>
    def test_loop_guard_forces_human_review_tier(self, env):
        """R-0862: the human-review tier had no positive pin after round 18.

        Round 18 deleted `_review_state` and the two tests that pinned this tier. The
        tier still ships and is still reachable through the loop guard, so it is pinned
        here through the surviving durable-failure signal rather than through the
        deleted review state."""
        d, _ = env
        job = _job(d)
        from packages.orchestration import repair_loop as RL
        j = load_job(UUID(str(job.id)), d)
        for i in range(2):
            att = RL.RepairAttempt(attempt_id=f"h{i}", job_id=str(job.id),
                                   failure_artifact_id=f"f{i}", status="tested_failed",
                                   source="cli_v1", created_at="t")
            RL.save_repair_attempt(j, att)
        s = OB.build_orchestrator_situation(str(job.id), d)
        # The precondition, asserted so this test cannot pass vacuously.
        assert s.loop_guard.status == OB.LoopGuardStatus.REQUIRE_HUMAN_REVIEW
        assert s.model_routing_plan.tier == OB.RoutingTier.HUMAN_REVIEW_REQUIRED
        assert s.model_routing_plan.allow_external is False

<<<END TEST21>>>

# HEADER21 and TEST21 each END with a blank line, which steps 1 and 6 rely on as the
# separator before the moved chunk and before `test_routing_never_executes`. Keep it.
