STEP T001/round 18 — F275 — the overnight_executor module group

Goal: Delete component 1 of `.agent/f275_deletion_order.md` — the module group
`packages.orchestration.overnight_executor` — after ruling, as a dated DECISION,
what happens to the live-review parser three SURVIVING production modules import
out of it. Book round 17's PASS verdict, the R-0861 resolution and the round 17
prose slip from `.agent/handoff.md`, which carried them as the durable carrier
amend0827-process-diet rule 1 names.

WHAT THE REVIEWER MEASURED BEFORE AUTHORING THIS BLOCK. Every numeral below comes
from an APPLIED dry run in a disposable worktree at base `c4c314c2`: the whole
deletion was performed, ruff and the affected suites were run, the full suite was
run serially to completion, and three mutation probes were executed control-first.
The worktree was removed and pruned before this block was written. You are not
being asked to rediscover any of it, but you ARE being asked to re-measure it.

Bundle, in this commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r18.md`
  C0b  mirror the same bytes into `.agent/last_block.md`
  C1   advance `.agent/plan.md` to round 18 — PLAN18, replaced WHOLE
  C2   the record — LEDGER18 appended to `.agent/live_review.md`, SLIPS18
       appended to `.agent/prose_slips.md`
  C3   DECISION18 appended to `.agent/decisions.md`, BEFORE the first `git rm`
  C4   THE MODULE GROUP, one commit, never split
  C5   the handback, rewriting `.agent/handoff.md`

Change — C4, the module group. Exactly these paths, nothing beyond them.

DELETED WHOLE (4 files):
  packages/orchestration/overnight_executor.py            1119 lines
  tests/orchestration/test_overnight_executor.py           394 lines
  tests/cli/test_overnight_executor_cli.py                 137 lines
  docs/system/bounded-overnight-executor-v0.md             112 lines

EDITED — the handler and the catalog:
  apps/cli/commands/overnight_cmd.py
      Delete `_cmd_overnight_run` whole and its `"overnight.run"` line in
      COMMAND_HANDLERS. THE FILE SURVIVES: its other three commands
      (`overnight.readiness`, `overnight.plan`, `overnight.report`) import
      `packages.orchestration.overnight_readiness`, which is component 3 of the
      order file and NOT this round. Measured at `c4c314c2` by reading every
      import in the file. Do not delete this file.
  apps/cli/command_catalog.py
      Delete the `overnight.run` CommandEntry whole. Measured at `c4c314c2`:
      NO `related=` tuple anywhere in the catalog names `overnight.run`, so no
      other entry needs repair. Re-measure this yourself — R-0859 records that
      nothing resolves `related=` against the catalog automatically.

EDITED — the three SURVIVING consumers. DECISION18 rules this; RULE 3 of
`docs/roadmap/features/T2_F275.md` T001 requires the survivor to lose the call
site and forbids a stub, a shim or a copy of the parser into a survivor.
  packages/orchestration/self_dogfood.py
      Delete `_review_findings`, `_detect_review` whole, the
      `_detect_review(items, blockers, risks)` call, and the capability rule
      whose predicate is `has("overnight_executor.py")`.
  packages/orchestration/self_dogfood_execution.py
      Delete `_review_blocks` whole and the review-gate call site in
      `evaluate_self_execution_eligibility` (the block from the comment
      `# Review must not be PENDING/FAIL/open blocker-high.` through its
      `return elig`). Every OTHER gate in that function survives untouched.
  packages/orchestration/orchestrator_brain.py
      Delete `_review_state` whole and its call site with the evidence-ref and
      blocker append that consume it. THEN unthread the two values that call
      site produced, which ruff surfaces as F821 if you stop early:
        `_generate_options`  drop the `review_blocks` parameter — measured at
                             `c4c314c2` to be UNUSED in that function's body.
        `_score_options`     drop the parameter AND the branch guarded by
                             `review_blocks`.
        `_evidence_fingerprint` drop the `verdict` parameter and its `"verdict"`
                             key from the hashed dict.
        `_routing_plan`      drop the parameter and remove `review_blocks` from
                             its `if`, leaving the loop-guard condition alone.
                             Its message loses the review clause.

EDITED — the tests of the deleted behaviour. Each named below is DELETED because
what it pins is what RULE 3 removes, except the ONE marked RE-BASED, which is
kept because it pins a SURVIVING branch that merely happened to be reached
through a review blocker.
  tests/orchestration/test_orchestrator_brain.py
      DELETE `TestDecisionQuality::test_open_blocker_forces_human_review` and
      `TestModelRouting::test_open_blocker_high_human_review`.
  tests/orchestration/test_self_dogfood.py
      DELETE `TestInspection::test_pending_review_is_blocker` and
      `TestInspection::test_open_blocker_finding`.
      RE-BASE `TestPlanAndPropose::test_propose_ambiguous_requires_selection`.
      It asserts `stop_reason == "ambiguous_selection"`, which
      `propose_self_improvement` raises when MORE THAN ONE item is BLOCKER or
      HIGH. The review detector was one such producer. Measured at `c4c314c2`
      in the applied worktree: after the deletion exactly ONE producer of a
      BLOCKER/HIGH item remains in `self_dogfood.py`, the per-failure
      EVIDENCE_GAP item in `_detect_evidence_gaps`, and it emits ONE item PER
      unresolved failure artifact. So give the fixture TWO unresolved failures
      and the branch is reached with no review file involved. Widen the `_job`
      helper with a count rather than writing a second helper. The reviewer ran
      this re-based test against a mutation that downgrades that item's
      priority and it went RED — see G5 probe P3, which you must reproduce.
  tests/orchestration/test_self_dogfood_execution.py
      DELETE `TestEligibility::test_pending_review_blocks`.

EDITED — the ratchets, the allowlists and the order file:
  tests/orchestration/test_development_artifact_boundary.py
      Delete the `"packages/orchestration/overnight_executor.py"` entry from
      `_ALLOWED_LEGACY`. THIS IS LOAD-BEARING: `TestAllowlistCompleteness`
      asserts every allowlisted path EXISTS, so deleting the module without
      this edit turns that guard RED. Leave the other five entries alone —
      measured at `c4c314c2`, each of those files still references the ledger.
  docs/system/development-artifact-boundary-v0.md
      Delete the single table row naming `overnight_executor.py`.
  tests/orchestration/test_cluster_deletion_map.py
      Delete the `"packages.orchestration.overnight_executor"` CLUSTER_MODULES entry.
  tests/orchestration/cluster_deletion_map.txt
      Delete the three lines beginning `packages.orchestration.overnight_executor <-`.
  tests/orchestration/import_reachability_allowlist.txt
      Delete the `packages.orchestration.overnight_executor` line.
  .agent/f275_deletion_order.md
      REGENERATE, do not line-edit. Removing this component REORDERS the
      remainder: the condensation the ratchet measures becomes, in order,
      `overnight_readiness`, then `worker_registry`, then the
      `provider_trust, provider_trust_verification` cycle. Deleting only the
      first line leaves `worker_registry` ahead of `overnight_readiness` and
      `test_cluster_deletion_order.py` goes RED with both lists printed. The
      reviewer hit exactly that in the dry run.

EDITED — the advertisements. R-0861's fix clause is BINDING on this round: read
the sweep's RAW list, not only its stripped count, and name every `docs/` page
the sweep reaches. Deleting `docs/system/bounded-overnight-executor-v0.md` breaks
every inbound reference listed here, measured at `c4c314c2`:
  docs/README.md                             the index row for the deleted page
  docs/system/repair-loop-v1.md              one cross-link bullet
  docs/system/provider-trust-gate-v0.md      one cross-link bullet
  docs/guides/do-continue-v1.md              one cross-link bullet
  docs/archive/self-dogfood-overnight-future.md   one cross-link bullet
  docs/archive/bounded-overnight-prep-v0.md  TWO references, one prose sentence
                                             and one cross-link bullet
Remove each reference so no surviving page links a deleted file. Where a
sentence is left dangling by the removal, delete the sentence, never invent a
replacement target. Registering the page in `docs/README.md` is an AGENTS.md
Documentation-Updates obligation and its REMOVAL is the same obligation.

Constraints:
 1. Apply every authored slice BYTE FOR BYTE, extracted from your committed C0a
    blob between its marker lines, markers excluded. Never retype a slice. If a
    slice contradicts this block's prose, follow the slice and DECLARE it.
 2. Touch NO path this block does not name. If the suite reds on a path not
    named here, STOP, declare the red gate, and do not widen scope — that is the
    sanctioned move and round 16 was right to take it.
 3. C4 is ONE commit and is never split: F275 T001 RULE 1 makes one module group
    the atomic unit, and a half-deleted module is the state this must not leave.
 4. C3 lands BEFORE any `git rm`. F275 T001 and round 17's handback both require
    the ruling on disk before the deletion it authorises.
 5. You write NO verdict, NO `Done:` paragraph and NO finding of your own. Where
    a fix lands before the reviewer has authored its resolution, write one
    `Landed: R-XXXX — <what changed, which commit>` line and nothing else.
 6. Destructive verification runs ONLY in a disposable `git worktree`, never in
    the primary checkout, which satisfies `git status --porcelain` empty at the
    handback. Remove and prune the worktree before C5.
 7. Run the full suite SERIALLY and in the PRIMARY checkout. Under `pytest -n
    auto` the `ui_server` command-channel tests race for a port, and the vitest
    node needs `apps/ui/node_modules`, which no fresh worktree carries.
 8. EVERY gate below runs at or after C4 and BEFORE C5, because C5 writes the
    handback that quotes each gate's exit code, and a gate ordered after the
    commit that quotes it can only be reported by a number nobody has seen —
    §3 item 31. The single exception is G2's block line count, which is a
    property of the bytes you save at C0a.

Done when — the gates below. Execute every one and record its REAL exit code with
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. "Green" as a word is a finding.

G1 TRANSPORT — one digest comparison, per amend0827 rule 5. Report sha256 and
   byte length of `.remedy-wt/f275-r18.md`, of the committed
   `.agent/authored/f275-r18.md` and of the committed `.agent/last_block.md`,
   and state whether ALL THREE are byte-equal. Per §3 item 37 this covers those
   three artefacts and claims nothing about the bytes the reviewer emitted.

G2 THE PLAN AND THE DECISION SLICE. Report this block's TOTAL line count against
   its cap of 490. Report `.agent/plan.md` at C1: byte length, sha256, and
   whether it is byte-identical to the PLAN18 slice extracted from your
   committed C0a blob; its line count against the AGENTS.md cap of 50; and that
   `## Goal` and `## Next Steps` each occur exactly once. Report that the
   DECISION18 slice occurs EXACTLY ONCE in `.agent/decisions.md` at C3 and that
   the bytes at that site re-hash to the slice's own digest.

G3 THE RECORD, over TWO appends — full byte forensics, which amend0827 rule 5
   reserves for exactly this target. For `.agent/live_review.md` <- LEDGER18 and
   for `.agent/prose_slips.md` <- SLIPS18, report all four readings:
   (a) BYTE READER: pre length and sha256, post length and sha256, growth equal
       to 1 + slice length, pre a byte-exact PREFIX of post, the slice a
       byte-exact SUFFIX of post, and the joining byte read back as `b'\n'`.
   (b) STRUCTURAL READER: N COUNTED BY YOUR SCRIPT from the slice, never a
       number this block asserts; then the last N blank-line units of the WHOLE
       post-file compared against the slice's N paragraphs IN ORDER, with a
       per-unit sha256 on both sides. Per §3 item 36 this reader covers the
       WHOLE appended region, not its tail.
   (c) NEGATIVE CONTROL: flip one byte IN MEMORY inside the FIRST appended
       paragraph and report that BOTH readers REJECT the mutant and BOTH accept
       the truth; then re-read the file from disk and confirm it is byte-equal
       to the committed post-blob.
   (d) COUNT PATTERNS in the post-blob: the rise in `^Gate: `, and that
       `^Gate: F275 R17 `, `^Done: R-0861 — `, `^- R-0862 — ` and `^- R-0863 — `
       each occur exactly once.
   (e) THE OPEN SET BY DISTINCT ID, `Landed:` lines never subtracted. At base
       `c4c314c2` the reviewer measured registered 90, done 5, open 85, with 34
       distinct `Landed:` ids present and not subtracted. Report the same three
       figures at C2 and confirm the base reproduces.

G4 THE SWEEP IS CLEAN, and R-0861's fix clause binds it. Over every tracked file
   outside `.agent/` and `.data/`, sweep for `overnight_executor`,
   `run_overnight_executor`, `parse_review_findings`,
   `review_findings_block_execution`, `render_overnight_run_report_markdown`,
   `bounded-overnight-executor-v0` and the command id `overnight.run` in both
   its dotted and its spaced form. PRINT THE RAW LIST IN FULL AND NEVER TRUNCATE
   IT, then state which lines survive stripping and why each is legitimate. The
   reviewer's applied run left exactly one class of survivor: prose in
   `docs/roadmap/features/` naming the deletion as history, which is correct and
   stays. A hit anywhere else is a violation. Then run
   `python3 -B -m pytest tests/cli/test_advertised_commands.py -q` and report its
   exit code: in the dry run this guard was the ONLY suite failure caused by the
   change, and it named `docs/system/bounded-overnight-executor-v0.md:14`
   advertising `remedy overnight run`.

G5 THE RED-PROOFS, in a disposable worktree at your C4 commit. For each probe run
   the UNMUTATED CONTROL FIRST over the SAME node set, then the mutation, then
   revert and re-run; report all three exit codes and the last summary line of
   each. Name the revert target by PATH and confirm the mutated bytes occur
   exactly once in that file before you change them.
   P2 — in `packages/orchestration/self_dogfood_execution.py` replace the
        condition `task.status != ProposedTaskStatus.APPROVED_FOR_BUILD` with a
        constant false, over
        `tests/orchestration/test_self_dogfood_execution.py::TestEligibility`.
        PROPERTY: the approval gate SURVIVES this round untouched and is still
        pinned, so the control is exit 0 and the mutation is exit 1. The
        reviewer measured 6 passed, then 1 failed and 5 passed.
   P3 — in `packages/orchestration/self_dogfood.py` downgrade the per-failure
        EVIDENCE_GAP item from `Priority.HIGH` to `Priority.LOW`, over the
        RE-BASED node
        `tests/orchestration/test_self_dogfood.py::TestPlanAndPropose::test_propose_ambiguous_requires_selection`.
        PROPERTY: the re-based test genuinely BITES rather than passing
        vacuously, so the control is exit 0 and the mutation is exit 1. The
        reviewer measured 1 passed, then 1 failed.
   P1 — THIS ONE IS ORDERED AS A PROBE AND NOT AS A COLOUR, per §3 item 5. In
        `packages/orchestration/orchestrator_brain.py` replace the surviving
        loop-guard condition in `_routing_plan` with a constant false, over
        `tests/orchestration/test_orchestrator_brain.py::TestAntiLoop` and
        `::TestModelRouting`. REPORT THE COLOUR; DO NOT ASSERT IT. The reviewer
        measured control exit 0 at 5 passed and the MUTATION ALSO EXIT 0 — the
        branch is not pinned once this round's two routing tests are deleted,
        which is the coverage loss finding R-0862 records. A green mutation here
        is the expected reading and is not a failure of your round.

G6 THE GUARDS, THE SUITE AND THE TREE.
   (a) `python3 -B -m pytest tests/orchestration/test_development_artifact_boundary.py
       tests/orchestration/test_cluster_deletion_map.py
       tests/orchestration/test_import_reachability.py
       tests/orchestration/test_cluster_deletion_order.py
       tests/orchestration/test_orchestrator_brain.py
       tests/orchestration/test_self_dogfood.py
       tests/orchestration/test_self_dogfood_execution.py -q`
       The reviewer's applied run gave 69 passed, exit 0.
   (b) the canary, `python3 -B -m pytest tests/cli/test_golden_path.py -q`.
   (c) `python3 -B -m pytest tests/docs/ -q`, because this round's change set
       includes `docs/` pages and the index — verification tier 5.
   (d) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY
       checkout with C4 committed. Report passed, skipped, failed and the
       collection count from a separate `--collect-only`, and confirm
       passed + skipped equals collected. At base the suite was 18603 passed and
       23 skipped against 18626 collected. This round deletes two whole test
       files and five test functions and re-bases one, so the count MUST fall;
       report the new figures and the arithmetic, and do not reconcile them
       against the base by hand-waving. In the reviewer's worktree run the only
       failures were `test_advertised_commands` — which this round's doc
       deletions fix — plus two worktree artefacts that do not arise in the
       primary checkout: the vitest node, which needs `apps/ui/node_modules`,
       and `test_evidence_index`, which reads `git status --porcelain` and was
       reacting to the uncommitted deletion.
   (e) `python3 -B -m ruff check` over every `.py` path in this round's change
       set. Report exit 0. The base carries 13 pre-existing ruff errors in files
       this round does not touch; do not fix them and do not count them.
   (f) THE TREE: `.agent/STOP` re-read from disk, `git status --porcelain`,
       `git worktree list`, the branch name, and
       `git diff --name-only <C3>..<C4>` compared against this block's C4 path
       set with the MISSING and EXTRA sets both stated. Then a per-commit table
       of insertions for every commit BEFORE C5, each against the AGENTS.md
       DECISION F104 D1 cap of 500 insertions, with parent counts. Per §3 item
       14 C5's own numbers are not yours to report; the reviewer books them.
   (g) Compare the `+/-` column of your `## Commits` table cell by cell against
       `git show --numstat` per commit and state that they agree — §3 item 28.

G7 THE RATCHETS AGREE WITH THE DISK. Report that
   `.agent/f275_deletion_order.md` now holds exactly three component lines in the
   regenerated order, that `tests/orchestration/cluster_deletion_map.txt` holds
   no line naming `overnight_executor`, and that the reachability allowlist and
   `CLUSTER_MODULES` no longer name it. These are the four measurements
   amend0906-triage-throughput requires of a deletion, restated against this
   round's own artefacts.

Handback: the completion report, and rewrite `.agent/handoff.md` at C5. Carry
the SESSION NUMBER — this is SESSION 10 of F275 — the round number, the branch,
the commit SHAs, the changed-files table with `+/-` per path and a REASON per
path, one line per gate with its real exit code, the item-status table AGENTS.md
mandates with every ordered item appearing exactly once, the open-findings count
by distinct id, and the next expected action. It has NO length cap. Declare every
deviation; a declared deviation costs nothing and an undeclared one is a finding.
Push ONCE, after C5, with `git push -u origin feature/f275-one-world-completion-part-three`.
Create no PR, merge nothing, and run no `gh` command.

--- BEGIN-PLAN18 ---
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 18 deletes the `overnight_executor` module group, the first component of the recorded
deletion order. It first books round 17's PASS verdict, the R-0861 resolution and one prose
slip, then rules as DECISION F275 D8 what becomes of the live-review parser that three
SURVIVING modules import out of the dying one. Measured before the ruling: that parser cannot
read this repository's own ledger format, so the gate it feeds blocks unconditionally rather
than reading review state. The three survivors lose the call site, per T001 RULE 3.

## Next Steps

1. The `overnight_readiness` component. The order file is REGENERATED by round 18 and this
   component moves to its first line, ahead of `worker_registry`. It also holds the three
   surviving `overnight` commands and their handler file.
2. Then `worker_registry`, then the `provider_trust` / `provider_trust_verification` pair,
   which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and the
   open ids named among the ideas deleted rather than inherited. That round also discharges
   R-0843's widened sweep, R-0858's repair of F267 and R-0859's referential-closure test.
4. T002, the atomic record flip, alone, because every later commit's size depends on it.

## Risks

- The open set is 85 by distinct id at this round's base `c4c314c2`. Round 18 resolves one
  and registers two, so it ends at 86. Four are High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12.
- R-0847's blindness is unfixed, so every deletion round reads the RAW sweep list by hand.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel
  tests race for a port, and the vitest node needs `apps/ui/node_modules`.
--- END-PLAN18 ---

--- BEGIN-LEDGER18 ---
Gate: F275 R17 — the F275 round 17 entry. VERDICT PASS, written by the planner and reviewer of session 9 after reading the committed range `12dd60ad`..`f5509039` and re-running all five gates independently against the committed blobs, and booked here by round 18's first substantive commit per amend0827-process-diet rule 1. Six single-parent commits, insertions 254, 162, 18, 10 and 8 for the five before the handback, every one far under the DECISION F104 D1 cap of 500. G1 transport: the reviewer's own delegation source and both committed copies are 28529 bytes at `05bf237e16c1bb54e3ae5bf5003d47512baf87ee0d528eeede51b46520473c42` and compare byte-equal; per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` byte-identical to PLAN17 at 2537 bytes and `e2f68029…`, 44 lines against the cap of 50; the block 254 lines against 490; the SPINE17 slice occurring exactly once in `docs/system/core-product-spine-v0.md` and byte-identical there. G3 over two appends: `.agent/live_review.md` 650049 to 659974 and `.agent/prose_slips.md` 189111 to 191891, both with byte-exact prefix and suffix, the joining byte read back as a newline, N counted by the reader as 2 and 3, ordered equality over the whole appended region, and both negative controls flipped inside the FIRST appended paragraph rejected by BOTH readers. The open set 84 to 85 by distinct id against registrations 89 to 90. G4, the gate round 16 failed, was green: RAW 11 and STRIPPED 3 over 29 tokens and 1676 tracked files, both binding conditions holding with EMPTY violation sets. G5: the documentation gate 851 passed, the canary 42 passed, and the full suite green at 18603 passed, 23 skipped and ZERO failed against 18626 collected. All five worker deviations sustained, the load-bearing one being the reviewer's own: the block's SPINE17 region description spanned seven lines while the same block's change set measured 8/8, and the worker resolved toward the measured numeral, landed exactly 8/8 with the slice byte-identical at the site, and declared it.

Done: R-0861 — RESOLVED at C3 `ee86115a`, verified by the reviewer of session 9 by re-running the completeness sweep itself rather than reading the worker's report. All three pages the finding names are repaired. `docs/guides/simple-operator-quickstart-v0.md` loses its `### Check worker readiness`, `### Add a worker` and `### Disable a worker` sections with their fenced `bash` blocks, and the three table rows that mapped those commands onto the equally deleted `builder adapter-*` commands; `### Check core health` survives untouched, because `remedy doctor core` is not deleted. `docs/system/core-product-spine-v0.md` loses its two command-taxonomy rows, and the body of its `## What a worker is` section is replaced by the deliberate-absence note AGENTS.md's Code Discoverability Conventions require. `docs/system/mission-run-loop-morning-report-v0.md` loses its `## How Claude Code fits` section whole. THE MEASUREMENT that closes it: the sweep at C3 reads RAW 11 and STRIPPED 3 with both violation sets EMPTY, against RAW 16 and STRIPPED 6 with three violations at the base. The finding's FIX CLAUSE remains BINDING on every remaining deletion round of this feature and is NOT discharged by this resolution: the completeness sweep is read as its RAW list and not only as its stripped count, and the block names every `docs/guides/` and `docs/system/` page the sweep reaches rather than only the pages a consumer map predicted. R-0847 is NOT resolved and gains a third measured instance here — `tests/cli/test_advertised_commands.py` passed at exit 0 over the state this round found broken, both before and after the repair.

- R-0862 — Medium, DELETING THE LIVE-REVIEW GATE LEAVES `RoutingTier.HUMAN_REVIEW_REQUIRED` WITH NO POSITIVE TEST PIN. Round 18 deletes `orchestrator_brain._review_state` and, with it, the two tests that pinned the human-review routing tier — `TestDecisionQuality::test_open_blocker_forces_human_review` and `TestModelRouting::test_open_blocker_high_human_review`. That tier survives in the product and is still reachable through the loop guard, but nothing asserts it any more. THE MEASUREMENT, taken by the reviewer at base `c4c314c2` in an applied worktree: with the deletion applied, replacing the surviving loop-guard condition in `_routing_plan` with a constant false leaves `TestAntiLoop` and `TestModelRouting` at exit 0 and 5 passed — the mutation does not go red, so the branch is unpinned. A repo-wide search of `tests/` for `HUMAN_REVIEW_REQUIRED` after the deletion returns exactly one line, and it is a permissive membership assertion rather than a pin. FIX CLAUSE, binding on the round that next touches `orchestrator_brain.py`: add one test that drives the loop guard to BLOCK or REQUIRE_HUMAN_REVIEW and asserts `_routing_plan` returns the human-review tier with `allow_external` false, and prove it with the mutation above going red. The behaviour is NOT lost and no capability is inherited by another feature; only its guard is, which is why this is Medium and not High.

- R-0863 — Medium, THREE SURVIVING MODULES LOSE THE REVIEW-STATE STOP, AND THE CAPABILITY IS INHERITED BY NO FEATURE. Per T001 RULE 3 a surviving consumer loses the call site and never gains a copy, so `orchestrator_brain`, `self_dogfood_execution` and `self_dogfood` lose the ability to refuse work because the development review record says stop. The user-observable losses are three: `remedy self inspect` no longer reports a blocker when the review verdict is PENDING or FAIL; self-execution eligibility no longer stops with `REVIEW_FINDINGS_OPEN`; and the orchestrator's option scoring no longer suppresses execution-like options in favour of self-inspect and human-review. DECISION F275 D8 rules the deletion and records why the loss is smaller than it reads: measured at `c4c314c2` against the real `.agent/live_review.md`, the parser returns `source='malformed'` and all counts zero while 85 findings are open, so the gate blocked UNCONDITIONALLY and never once discriminated on review state in production. NO FEATURE INHERITS THIS IDEA, which is the honest answer rather than a routing to a convenient id: the capability as built was a parser for a ledger format this repository no longer writes, and re-creating it belongs to whatever feature next decides the development ledger needs a machine reader. The surviving stops in that eligibility path — approval, contract, target repo and branch safety — are untouched, and round 18's red-proof P2 pins the approval gate by mutation.
--- END-LEDGER18 ---

--- BEGIN-SLIPS18 ---
2026-09-09 · F275 R17 · The round 17 block described the SPINE17 substitution region as lying "between the heading line and the blank line preceding `## What a report is`", which read strictly spans seven lines and implies a numstat of 8/9, while the same block's own change set gave the measured figure 8/8. The worker resolved the contradiction toward the measured numeral — keeping the blank line after the heading and replacing the two prose paragraphs — landed exactly 8/8 with the slice byte-identical at the site, and declared it. Nothing landed wrong. The lesson is that a block substituting a slice into the MIDDLE of a file states the region by its two anchor lines and by the numstat it measured, and the reviewer reads those two statements against each other before emission exactly as §3 item 18 requires of a probe's recipe and its property, because here both halves were individually sound and only their agreement was not checked.
--- END-SLIPS18 ---

--- BEGIN-DECISION18 ---
## DECISION F275 D8 (2026-09-09) — the live-review parser dies with its module; the three surviving consumers lose the gate rather than inheriting the parser

CONTEXT. Round 18 deletes `packages/orchestration/overnight_executor.py`, component 1 of
`.agent/f275_deletion_order.md`. Three SURVIVING production modules import out of it:
`orchestrator_brain.py` and `self_dogfood_execution.py` take both `parse_review_findings`
and `review_findings_block_execution`, and `self_dogfood.py` takes the parser alone. Those
functions read `.agent/live_review.md` and turn its verdict into a refusal to execute. This
is the first deletion of this feature that removes a RESTRICTION rather than a capability,
so DECISION F275 D7's fail-safe argument does not reach it and is not copied onto it.

TWO READINGS WERE ON DISK AND DISAGREED. Both are now measured rather than argued.

READING A, that the deletion discharges a boundary violation, is FALSE. It rests on
`docs/system/development-artifact-boundary-v0.md` ruling that product modules must not
depend on the development ledger. Measured at `c4c314c2`: that document's "Allowed
development uses" table EXPLICITLY ALLOWLISTS all four modules — `self_dogfood.py`,
`self_dogfood_execution.py`, `overnight_executor.py` and `orchestrator_brain.py` — and its
disallowed list names only `worker_facade_cmd.py`. The guard
`tests/orchestration/test_development_artifact_boundary.py` carries the same allowlist.
These reads are sanctioned, not violations, and no boundary is repaired by removing them.

READING B, that the deletion removes a safeguard, is TRUE, and the measurement makes the
loss much smaller than the sentence suggests. Run at `c4c314c2` against the repository's
real `.agent/live_review.md`, `parse_review_findings` returns `source='malformed'`,
`verdict='unknown'` and every open-finding count zero, while the record holds 85 open
findings by distinct id. `review_findings_block_execution` therefore returns
`(True, 'review_findings_open')` UNCONDITIONALLY. The parser expects a `## Verdict` heading
and `### R-XXXX` blocks carrying `**Status**` and `**Severity**` fields; this repository's
ledger uses `- R-XXXX — ` registration paragraphs, `Done:` lines and `Gate:` entries, and
has none of those shapes. Every test that exercises the gate writes a SYNTHETIC file in the
old format, through `REMEDY_REVIEW_FILE` or a temporary agent directory, so the suite has
been green over a production path that never once read real review state.

CHOSEN. Delete the parser with its module, and remove the call site from each of the three
survivors, per T001 RULE 3, which forbids a stub, a shim or a copy of cluster code into a
survivor. The gate as built is a constant, not a discriminator: it answers "block" for every
possible state of the real record, so removing it does not trade a working safeguard for
convenience. It removes a jammed one.

CONSEQUENCES, stated plainly rather than minimised. Self-execution eligibility loses its
`REVIEW_FINDINGS_OPEN` stop; the orchestrator's `_score_options` no longer suppresses
execution-like options; `_routing_plan` reaches the human-review tier only through the loop
guard; and `remedy self inspect` no longer reports a review verdict blocker. Because the old
gate blocked unconditionally, the direction of the change is from "always refuses" to
"proceeds subject to the other gates", which is a real loosening and is registered as
R-0863. The other gates in that eligibility path are measured to survive untouched —
approval, run contract, attached target repo and branch safety — and round 18's red-proof P2
pins the approval gate by mutation rather than by assertion. F275's "Do not touch" keeps the
approval gate out of this feature's reach, so that layer is not weakened here.

ALTERNATIVES CONSIDERED. (1) Move the parser into a surviving module. Rejected: T001 RULE 3
forbids exactly this, and it would preserve a reader that cannot read the file it is aimed
at. (2) Repair the parser to the current ledger format and then move it. Rejected twice
over: building new capability inside a deletion round is the scope widening AGENTS.md
forbids, and the development ledger's format is not this feature's to freeze. (3) Keep
`overnight_executor.py` alive for the parser alone. Rejected: it is component 1 of an order
the operator ruled PERFORMED rather than prepared, and a module kept for one helper is the
attic AGENTS.md Scope Control refuses.

HOW TO REVERSE. Restore `packages/orchestration/overnight_executor.py` from `c4c314c2`,
restore the three call sites and the four unthreaded parameters in `orchestrator_brain.py`,
restore the six deleted tests, and re-add the module to the boundary allowlist, the
reachability allowlist, `CLUSTER_MODULES` and the deletion map. Reversing this decision
without also repairing the parser restores a gate that blocks unconditionally, which is the
state this decision ends.
--- END-DECISION18 ---
