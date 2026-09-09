── STEP T001 (module group 14 of the prototype cluster) — F275 ────────────────
ROUND 20 · SESSION 11 · base `0d18e58a` · branch feature/f275-one-world-completion-part-three

Goal: delete the `packages.orchestration.worker_registry` module group — the module,
its handler, its whole `route-policy` command group, its three `worker.registry-*`
commands, its cockpit section, its four `ContractAction` members, its two
documentation pages and its tests — and degrade the ONE surviving consumer that
does more than import a helper, `packages/orchestration/token_economy.py`, to a
FAIL-SAFE state in the same commit. This is component 1 of two in
`.agent/f275_deletion_order.md`.

THIS IS NOT A PURE DELETION ROUND under amend0906-triage-throughput. That
paragraph's four-measurement shortcut covers a round whose change set holds no
EDITED line under `packages/`, and this round rewrites the approval logic of a
surviving production module. The mutation red-proof is therefore ordered in full,
and G5 is that proof.

Bundle, in this order, one commit each:

  C0a  save this block verbatim to `.agent/authored/f275-r20.md`
  C0b  mirror the same bytes into `.agent/last_block.md`
  C1   advance `.agent/plan.md` — the PLAN20 slice, replacing the file WHOLE
  C2   the record: LEDGER20 appended to `.agent/live_review.md`, SLIPS20
       appended to `.agent/prose_slips.md`
  C3   DECISION F275 D9 — the DECISION20 slice appended to `.agent/decisions.md`.
       THIS COMMIT PRECEDES THE FIRST `git rm`, because the ruling it records is
       what authorises the survivor's degradation.
  C4   THE MODULE GROUP, in ONE commit, never split (T001 RULE 1)
  C5   the handback

Change — the C4 path set is EXACTLY these 23 paths, nothing added and nothing
dropped. The `+/-` figures beside them are what the reviewer's applied dry run
measured at base `0d18e58a`; report your own and declare any difference.

  DELETED WHOLE (5 files)
    packages/orchestration/worker_registry.py                     0/1035
    apps/cli/commands/route_policy_cmd.py                         0/196
    tests/orchestration/test_worker_registry.py                   0/380
    tests/cli/test_route_policy_cli.py                            0/107
    tests/orchestration/test_worker_route_integration.py          0/27

  DELETED WHOLE — documentation (2 files)
    docs/guides/worker-route-policy-user-guide-v0.md              0/88
    docs/system/worker-registry-route-policy-v0.md                0/106

  EDITED — production (5 files)
    apps/cli/command_catalog.py                                   0/79
    apps/cli/commands/__init__.py                                 1/2
    packages/orchestration/ui_server.py                           1/48
    packages/orchestration/token_economy.py                       22/62
    packages/orchestration/run_contract.py                        0/12

  EDITED — tests and ratchets (7 files)
    tests/cli/test_cli_ux.py                                      1/1
    tests/orchestration/test_token_economy.py                     7/11
    tests/orchestration/test_token_economy_integration.py         4/30
    tests/ui_server/test_dashboard_cockpit_truth.py               0/15
    tests/orchestration/test_cluster_deletion_map.py              1/3
    tests/orchestration/cluster_deletion_map.txt                  0/2
    tests/orchestration/import_reachability_allowlist.txt         0/2

  EDITED — documentation and state (4 files)
    docs/README.md                                                0/3
    docs/system/token-economy-context-budget-optimizer-v0.md      10/8
    docs/system/quality-baseline-v0.md                            0/1
    .agent/f275_deletion_order.md                                 0/1

  TOTAL 47 insertions, 2219 deletions, 23 paths.

WHAT EACH EDIT IS, described rather than sliced, because production code is
specified and never pasted:

 1. `apps/cli/command_catalog.py` — remove the `"route-policy"` GroupDef line; the
    two-line `# Worker Registry v0 (Step 1725)` section comment with the three
    `worker.registry-list`, `worker.registry-show` and `worker.registry-integrity`
    CommandEntry blocks beneath it; and the `# ── route-policy` section comment
    with the three `route-policy.show`, `route-policy.set` and
    `route-policy.evaluate` blocks beneath it. Touch no other entry.

 2. `apps/cli/commands/__init__.py` — drop `route_policy_cmd` from BOTH the sorted
    import block and the dispatcher tuple. Both, not one.

 3. `packages/orchestration/ui_server.py` — delete `_build_worker_registry_section`
    entirely with its two trailing blank lines, and the
    `"worker_registry": _build_worker_registry_section(job),` line of the dashboard
    dict. SEPARATELY, inside the SURVIVING `_build_token_economy_section`, delete
    the `from packages.orchestration.worker_registry import get_worker_spec,
    is_placeholder` line with the `oll = get_worker_spec("ollama.placeholder")`
    line under it, the `"ollama_placeholder_available"` key in the success return,
    and the same key in the except-branch return. That second edit is a
    user-observable loss in a surviving section and is why R-0865 exists.

 4. `packages/orchestration/token_economy.py` — the survivor's degradation, ruled
    by DECISION F275 D9 in C3. Delete all three `worker_registry` import
    statements and the whole function `estimate_route_token_band`, which has NO
    production caller and cannot have one once no worker spec exists; delete its
    line from the module's `Public API::` block. In
    `compute_token_economy_decision`, delete the `load_worker_registry` /
    `evaluate_worker_selection` / `get_worker_spec` block and the
    `classify_route_cost` import, leave `recommended_worker_id` at its empty
    default, set `estimated_cost_band` to `TokenBand.UNKNOWN`, and replace the
    approval disjunction with an UNCONDITIONAL `d.requires_human_approval = True`
    carrying a comment naming the pre-deletion `or not spec` term it replaces.
    Collapse the four-branch reason/next-action ladder to two: the
    `unknown_context` branch UNCHANGED, and an else-branch whose reason says no
    route spec is available and whose `next_safe_action` names only SURVIVING
    commands — `remedy token economy-report <job_id> --json` and
    `remedy token budget-show <job_id> --json`. NO string anywhere in the module
    may still name `remedy route-policy` or `remedy worker registry-`; the base
    carries four such strings and all four die. Rewrite the two head-docstring
    paragraphs that build the module on the Worker Registry so they state the
    degradation in the past tense and name F275 round 20.

 5. `packages/orchestration/run_contract.py` — delete the four-line Step 1726
    comment with the four members `WORKER_REGISTRY_SHOW`, `ROUTE_POLICY_SHOW`,
    `ROUTE_POLICY_SET` and `ROUTE_POLICY_EVALUATE`, and their four lines in the
    safe-action tuple below.

 6. `tests/cli/test_cli_ux.py` — remove `"route-policy"` from `_INTERNAL_GROUPS`.
    THIS FILE IS NAMED BECAUSE THE APPLIED DRY RUN FOUND IT AND NOTHING ELSE
    WOULD HAVE. It is a hand-maintained set that three tests iterate, it names no
    module and no command id, and every repo-wide grep for the module name misses
    it. Omitting this edit leaves the branch RED at 3 failed.

 7. `tests/orchestration/test_token_economy.py` — delete
    `test_route_band_unknown_stays_unknown` with the function it tests; narrow
    `test_unknown_context_requires_approval`'s last assertion from the two-way
    `"context inspect" in ... or "route-policy" in ...` to `"context inspect"`
    alone, since the second disjunct can never hold again; and REPLACE
    `test_local_route_no_approval_when_cheap` — which asserts
    `requires_human_approval is False` and is the one test the degradation turns
    red — with a test of the fail-safe that asserts the empty
    `recommended_worker_id`, the UNKNOWN cost band and `requires_human_approval
    is True`, under a name saying so.

 8. `tests/orchestration/test_token_economy_integration.py` — delete the whole
    `TestPlaceholderHardening` class, all three of whose tests import the deleted
    module, and rewrite the module docstring's last sentence as a deliberate
    absence in this repository's idiom.

 9. `tests/ui_server/test_dashboard_cockpit_truth.py` — delete
    `test_worker_registry_section_present`, the only test of the deleted section.

10. `tests/orchestration/test_cluster_deletion_map.py` — drop
    `packages.orchestration.worker_registry` from `CLUSTER_MODULES` and
    `apps/cli/commands/route_policy_cmd.py` from `CLUSTER_COMMAND_HANDLERS`, and
    re-point the `_cluster_module_of` docstring's example, which uses this module
    as its illustration, at a module that still exists.

11. `tests/orchestration/cluster_deletion_map.txt` — delete BOTH
    `packages.orchestration.worker_registry <- ` lines, the `token_economy.py` one
    and the `ui_server.py` one.

12. `tests/orchestration/import_reachability_allowlist.txt` — delete BOTH
    `apps.cli.commands.route_policy_cmd` and
    `packages.orchestration.worker_registry`.

13. `.agent/f275_deletion_order.md` — REGENERATE from the live import graph using
    `measured_order()` from `tests/orchestration/test_cluster_deletion_order.py`,
    keeping the 26 header lines byte-identical. Never line-edit it. One component
    line must remain.

14. `docs/README.md` — delete the three index rows naming the two deleted pages:
    one in the quick-find table and one in each of the system and guides tables.
    The dry run confirmed those are the ONLY inbound references outside `.agent/`.

15. `docs/system/token-economy-context-budget-optimizer-v0.md` — rewrite the
    local-route paragraph and the "Expensive route justification" section so they
    state that approval is now UNCONDITIONAL and that the floor survives by
    degradation, and remove the `hard_safety_requires_approval` reference. Say
    plainly that Remedy no longer recommends a worker and name F110 as the
    inheritor.

16. `docs/system/quality-baseline-v0.md` — delete the one coverage-table row for
    `apps/cli/commands/route_policy_cmd.py`.

Constraints:

 1. Apply every authored slice BYTE FOR BYTE from the committed C0a blob, between
    its marker lines and excluding them. Never retype a slice, never edit one, and
    never let a marker line reach a target file.
 2. C4 is ONE commit. T001 RULE 1 makes a half-deleted module group the one state
    this work must not leave behind. It may not be split for size: it carries 47
    insertions against the DECISION F104 D1 cap of 500, which counts insertions
    only.
 3. C3 precedes C4. A ruling that authorises a deletion is worth nothing if it
    lands after it.
 4. NO STUB, NO SHIM, NO COPY. T001 RULE 3 is absolute: `token_economy` loses the
    call sites and gains no local reimplementation of `hard_safety_requires_approval`,
    `evaluate_worker_selection` or any spec type. If you find yourself writing a
    worker spec dataclass, stop and hand back.
 5. Do not repair the two PRE-EXISTING dangling `related=` references
    (`mission.run -> dogfood.run-loop`, `repo.status -> readiness.show`). R-0859
    holds them and binds them to the DECISION F260 D3 round. This round must add
    NO new one; G7 measures that.
 6. Do not repair the 24 pre-existing repo-wide ruff errors. None is in a file
    this round touches.
 7. Every gate figure you report is measured with the round's commits ALREADY
    COMMITTED, except where a gate names a base explicitly.
 8. Destructive verification runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, removed and pruned before C5. `/tmp` is denied in this
    environment. Leave no scratch `.py` file in the tree: an untracked script at
    the repository root is linted by `tests/orchestration/test_ci_budgets.py` and
    reds the lint ceiling.
 9. Write no verdict, no `Done:` paragraph and no finding of your own. If a fix
    lands that a finding asked for, write `Landed: R-XXXX — <one line>` and
    nothing else. R-0831 gets NO `Landed:` line this round: its resolution needs
    BOTH the knobs deleted and DECISION F260 D3 naming it, and D3 is not written
    until a later round.
10. Push ONCE, after C5. Create no pull request, merge nothing, run no `gh`
    command.

Done when — eight gates, each run with
`bash -c '<cmd>; echo "REAL_EXIT=$?"'` and each reported with its REAL exit code:

G1 TRANSPORT. One digest comparison over three artefacts and nothing else: the
   delegation source `.remedy-wt/f275-r20.md`, the committed
   `.agent/authored/f275-r20.md` and the committed `.agent/last_block.md`. Report
   the byte length and sha256 of each and whether all three are byte-equal. Per
   §3 item 37 this chain covers those three artefacts and claims nothing about
   the bytes that were emitted.

G2 THE PLAN AND THE SLICES. `.agent/plan.md` at C1 byte-identical to the PLAN20
   slice extracted from the committed C0a blob, with its line count against the
   AGENTS.md cap of 50 and `## Goal` and `## Next Steps` each present exactly
   once. Then, for all four slices, report that each occurs EXACTLY ONCE in its
   target and that a grep for every marker string over the four target files
   returns zero for each file.

G3 THE RECORD, over three appends — `.agent/live_review.md`, `.agent/prose_slips.md`
   and `.agent/decisions.md`. For EACH: (a) a byte reader — pre length and
   sha256, post length and sha256, slice length and sha256, growth equal to
   1 plus the slice length, pre a byte-exact PREFIX, slice a byte-exact SUFFIX,
   and the joining byte read back; (b) a STRUCTURAL reader — N counted BY YOUR
   SCRIPT from the slice, never asserted by this block, comparing the LAST N
   blank-line units of the whole post-file against the slice's N paragraphs IN
   ORDER with a per-unit sha256 on both sides, plus the sha256 of the unit before
   them shown to lie inside the PRE blob; (c) a NEGATIVE CONTROL flipping one
   byte IN MEMORY inside the FIRST appended paragraph, which BOTH readers must
   REJECT while both ACCEPT the truth, with the file re-read from disk afterwards
   and equal to the committed post-blob. Then the counts: `^Gate: ` before and
   after, and `^Gate: F275 R19 `, `^- R-0865 — `, `^Note: F275 R20 ` and
   `^## DECISION F275 D9 ` each exactly once. Then THE OPEN SET BY DISTINCT ID,
   `Landed:` never subtracted, measured at base `0d18e58a` AND at C3.

G4 THE SWEEP, READ BY HAND. Over every tracked file outside `.agent/` and
   `.data/`, for exactly these fifteen ordered tokens:
   `packages.orchestration.worker_registry`, `worker_registry`,
   `route_policy_cmd`, `worker.registry-list`, `worker.registry-show`,
   `worker.registry-integrity`, `route-policy.show`, `route-policy.set`,
   `route-policy.evaluate`, `remedy route-policy`, `remedy worker registry-`,
   `hard_safety_requires_approval`, `estimate_route_token_band`,
   `WORKER_REGISTRY_SHOW` and `ROUTE_POLICY_`. PRINT THE RAW LIST IN FULL AND
   NEVER TRUNCATE IT, then classify every line. The applied dry run measured
   RAW 6 at C4, every one history prose under `docs/roadmap/features/` — three in
   `T2_F260.md`, one each in `T2_F262.md`, `T2_F267.md` and `T8_F151.md`. Report
   your own RAW and reconcile any difference line by line.
   `tests/cli/test_advertised_commands.py` is NOT evidence for this gate: deleting
   the whole `route-policy` group removes it from that guard's `GROUPS` and the
   guard skips what it cannot resolve, which is finding R-0847. Run it, report its
   exit code, and state plainly that the pass is not evidence for this round.

G5 THE FAIL-SAFE IS PINNED, NOT MERELY WRITTEN. This is the round's load-bearing
   gate, because a surviving production module lost an approval-forcing
   invariant. Inside a disposable worktree at C4, over the node set
   `tests/orchestration/test_token_economy.py
   tests/orchestration/test_token_economy_integration.py
   tests/ui_server/test_dashboard_cockpit_truth.py`, with `__pycache__` purged
   and `python3 -B` for every run:
     (a) name the revert target by PATH and report how many times the exact
         mutated bytes occur in THAT file; the count must be 1;
     (b) prove the worktree is not shadowed by the editable install — report the
         `__file__` that `import packages.orchestration.token_economy` resolves to;
     (c) the CONTROL first, unmutated, over that node set;
     (d) the MUTATION: `d.requires_human_approval = True` in
         `compute_token_economy_decision` changed to `False`;
     (e) REVERT by path, purge, re-run, and show the worktree porcelain empty.
   The dry run measured control exit 0 at 72 passed, mutation exit 1 at 5 failed
   and 67 passed, and post-revert exit 0 at 72 passed. STOP CONDITION: if the
   mutation is GREEN, the fail-safe is unpinned, DECISION F275 D9's premise is
   false, and you hand back without committing C4.

G6 THE GUARDS, THE SUITE AND RUFF.
   (a) `python3 -B -m pytest tests/orchestration/test_cluster_deletion_map.py
       tests/orchestration/test_cluster_deletion_order.py
       tests/orchestration/test_import_reachability.py
       tests/orchestration/test_token_economy.py
       tests/orchestration/test_token_economy_integration.py
       tests/ui_server/test_dashboard_cockpit_truth.py
       tests/cli/test_advertised_commands.py tests/test_grouped_cli.py
       tests/cli/test_cli_ux.py -q` — the dry run gave 548 passed.
   (b) the canary, `python3 -B -m pytest tests/cli/test_golden_path.py -q` — 42.
   (c) `python3 -B -m pytest tests/docs/ -q` — 303; this round edits `docs/`.
   (d) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY
       checkout with C4 committed. Never `-n auto`: the `ui_server`
       command-channel tests race for a port. The dry run gave 18454 passed, 23
       skipped, ZERO failed, and a separate `--collect-only` of 18477, which is
       18454 plus 23. THE ARITHMETIC AGAINST THE BASE, which you must close by a
       node-id SET DIFFERENCE of `--collect-only` and not by counting functions:
       base `0d18e58a` collects 18538, so the fall is 61, and it is 62 ids removed
       against 1 added. The dry run attributes the 62 as 48 across the three
       deleted test files (36 + 11 + 1), 8 parametrized `[route-policy]` cases in
       `tests/test_grouped_cli.py` which are GENERATED from the catalog `GROUPS`
       and die with the GroupDef, 3 in `TestPlaceholderHardening`, 2 in
       `test_token_economy.py` and 1 in `test_dashboard_cockpit_truth.py`. The 1
       added id is the replacement fail-safe test. Report your own numbers and
       reconcile any difference.
   (e) `python3 -B -m ruff check` over every `.py` path in the change set, then
       PARITY over `packages`, `apps` and `tests` at base `0d18e58a` and at C4.
       Read the base in a DISPOSABLE WORKTREE or via `git show <sha>:<path>` —
       never by writing the base blob over a tracked file. The dry run measured
       `Found 24 errors.` at BOTH revisions with an IDENTICAL per-file
       distribution and not one error in a file this round touches.

G7 THE RATCHETS AND THE CATALOG AGREE WITH THE DISK. Read the SHIPPED catalog by
   importing `_BASE_CATALOG` and `GROUPS` from `apps.cli.command_catalog` — never
   by grepping the source. Read the BASE revision in a READ-ONLY disposable worktree at
   `0d18e58a`, never by writing a base blob over a tracked file. Report the total
   command count and group count at that base and at C4 (the dry run measured 233
   to 227 commands and 46 to 45 groups), that
   `"route-policy"` is absent from `GROUPS`, that the sets of ids beginning
   `route-policy.` and `worker.registry-` are both EMPTY, and that there are zero
   duplicate ids. THEN, discharging R-0859's standing obligation on every deletion
   round of this feature until its closure test exists: resolve EVERY `related=`
   tuple in the catalog against the live id set and report the dangling
   references at BOTH revisions. The dry run measured exactly 2 at each,
   `mission.run -> dogfood.run-loop` and `repo.status -> readiness.show`, both
   pre-existing; this round must ADD NONE. Finally report the component lines now
   in `.agent/f275_deletion_order.md`, that the file equals a fresh regeneration
   from the live graph, that its 26-line header is unchanged, and that neither
   `cluster_deletion_map.txt`, the reachability allowlist, `CLUSTER_MODULES` nor
   `CLUSTER_COMMAND_HANDLERS` still names this group's module or handler.

G8 THE TREE. Re-read `.agent/STOP` from disk and report whether it exists.
   `git status --porcelain` EMPTY. `git worktree list` holding ONE entry. The
   branch name. `git diff --name-only <C3>..<C4>` compared as a SET against the
   23 paths above, reporting the MISSING and EXTRA sets explicitly, both of which
   must be empty. Per-commit insertions for every commit BEFORE C5 against the
   cap of 500, with each commit's parent count. Then compare the `+/-` cells of
   your `## Commits` table CELL BY CELL against `git show --numstat` per commit
   and state that they agree — §3 item 28.

Handback: the completion report, and rewrite `.agent/handoff.md` at C5. Carry the
SESSION NUMBER — this is SESSION 11 of F275 — the round number, the branch, the
commit SHAs, the changed-files table with `+/-` and a REASON per path, one line
per gate with its real exit code, the item-status table with every ordered item
appearing exactly once, the open-findings count by distinct id, and the next
expected action. It has NO length cap. Declare every deviation.

--- BEGIN-PLAN20 ---
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 20 deletes the `worker_registry` module group — the module, its handler, the whole
`route-policy` command group, the three `worker.registry-*` commands, its cockpit section,
four `ContractAction` members and two documentation pages. DECISION F275 D9, committed
before the first `git rm`, rules that the surviving `token_economy.py` degrades FAIL-SAFE
rather than dying: no route spec resolves, so approval becomes unconditional and the R-0095
hard-safety floor holds by degradation. The round books round 19's PASS verdict and
registers R-0865.

## Next Steps

1. The `provider_trust` / `provider_trust_verification` pair, which is the last cycle and
   the last component of the deletion order.
2. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and the
   open ids named among the ideas deleted rather than inherited. That round also discharges
   R-0843's widened sweep, R-0858's repair of F267 and R-0859's referential-closure test.
3. T002, the atomic record flip, alone, because every later commit's size depends on it.
4. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 87 by distinct id at this round's base `0d18e58a`. Round 20 registers one,
  taking it to 88. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather
  than this feature's, per DECISION F272 D12.
- Worst on this round: a surviving production module loses an approval-forcing invariant.
  The mutation red-proof is ordered in full and its STOP condition blocks the commit.
- R-0847 again: deleting a whole command group removes it from the advertised-command
  guard's `GROUPS`, so the guard goes blind exactly when the group's advertisements go
  dead. The sweep is read by hand, as its RAW list.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel
  tests race for a port.
--- END-PLAN20 ---

--- BEGIN-LEDGER20 ---
Gate: F275 R19 — the F275 round 19 entry. VERDICT PASS, written by the planner and reviewer of session 10 after reading the committed range `c878073e`..`e3879c82` and RE-RUNNING every gate independently against the committed blobs, and booked here by round 20 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, carried from the pushed `.agent/handoff.md` at `0d18e58a`. The worker's report was evidence for no line of it. Six single-parent commits, per-commit insertions 310, 246, 15, 8 and 7 for the five before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS THE PRIMARY PROOF OF §4 ITEM 9 AND NOT THE DIGEST FALLBACK: the reviewer's own delegation source and both committed copies are 25581 bytes at `8b40fbd855485160db7aef589b2c49f51a8bcf1f543ae375280d8e5e82afdee8` and compare BYTE-EQUAL; per §3 item 37 that chain covers those three artefacts and claims nothing about the emitted bytes. G2: `.agent/plan.md` at C1 byte-identical to the PLAN19 slice at 41 lines against the cap of 50 with both mandated headings present, all three slices occurring EXACTLY ONCE in their targets, no marker line reaching any file, and the `mission_readiness.py` edit measured at THREE lines every one of which lies inside the module docstring, rewriting the two sentences that claimed the deleted module was "still on disk" into the past tense. G3, over two appends with byte and structural readers and both negative controls flipped inside the FIRST appended paragraph and rejected by BOTH readers: `^Gate: ` rose 40 to 41, `^Gate: F275 R18 ` and `^- R-0864 — ` each exactly once, and THE OPEN SET WENT 86 TO 87 BY DISTINCT ID against registrations 92 to 93 and resolutions 6 to 6, with 34 distinct `Landed:` ids present and never subtracted. G4 IS THE GATE THIS ROUND'S OWN GUARD COULD NOT ANSWER, AND IT IS CLEAN: the reviewer re-ran the sweep with its own script over the 1668 tracked files outside `.agent/` and `.data/` and measured RAW 6, printed in full and not truncated, against RAW 11 in the applied dry run before the round; three are history prose in `docs/roadmap/features/`, and the other three are exactly the classes the block declared legitimate in advance. The spaced form `remedy overnight` returns ZERO hits, so no page anywhere still instructs an operator to run a command that round deleted — the property R-0861's fix clause exists to protect and the one `tests/cli/test_advertised_commands.py` CANNOT establish here, because deleting the whole group removed it from that guard's `GROUPS` and the guard skips what it cannot resolve. The worker ran that guard, got exit 0, and stated in its own handback that the pass is not evidence for the round, which is R-0847 being handled correctly rather than relied on. G5's STOP CONDITION DID NOT FIRE, the round's most load-bearing single reading: mutating `build_overnight_readiness` in the SURVIVING `mission_readiness.py` moved its node set from a control of 128 passed to 16 failed and 112 passed and back to 128 on revert, so the carry-over is genuinely pinned by tests after its twin's deletion rather than merely still present. G6: the affected guards 716 passed, the canary 42, the documentation gate 303, and THE FULL SUITE WAS RE-RUN BY THE REVIEWER SERIALLY IN THE PRIMARY CHECKOUT and was GREEN at 18515 passed, 23 skipped and ZERO failed, with a separately measured collection of 18538 equal to 18515 plus 23; ruff clean over the change set and 24 pre-existing errors at BOTH the base and C3, none in a file that round touched. The catalog read 233 commands in 46 groups with ZERO ids beginning `overnight.`. THE SEVEN DECLARED DEVIATIONS ARE ALL SUSTAINED, and the two load-bearing ones are the reviewer's own errors rather than the worker's: the block ordered the deletion of lines in `tests/orchestration/cluster_deletion_map.txt` that the file does not contain and never did, so the ordered edit was a NO-OP and the worker correctly declined to manufacture a change; and the block's suite arithmetic predicted a fall of 29 where the real fall is 37, because eight parametrized `[overnight]` cases in `tests/test_grouped_cli.py` are GENERATED from the catalog `GROUPS` and disappear with the group, which the worker closed by a node-id set difference showing 22 plus 7 plus 8 equals 37 with NO node id added — a stronger reading than the one the block asked for. NO FINDING IS RESOLVED BY THIS GATE.

- R-0865 — Medium, DELETING THE WORKER REGISTRY TAKES A CAPABILITY OUT OF A SURVIVING MODULE AND A SURVIVING COCKPIT SECTION, AND NEITHER LOSS IS VISIBLE FROM THE DELETED FILES. Raised by the reviewer at the F275 round 20 authoring, from the applied dry run, and registered under T001 RULE 3, which orders a finding naming the behaviour and the feature that inherits the idea wherever a survivor's lost call site takes away something a user could observe. THE MEASUREMENT, taken at `0d18e58a` before the round: `packages/orchestration/token_economy.py` does not merely import a helper from the dying module, it builds its routing recommendation out of it — `load_worker_registry`, `evaluate_worker_selection`, `get_worker_spec`, `hard_safety_requires_approval` and `WorkerSelectionRequest` at line 584, `estimate_token_cost_band` at line 166 and `classify_route_cost` at line 613. THE THREE LOSSES. FIRST, `compute_token_economy_decision` stops naming a worker: `recommended_worker_id` was `local.candidate_generator` for a small cheap repository and is now always empty, and `estimated_cost_band` is now always UNKNOWN, so a user who could previously read which route Remedy suggested reads nothing. SECOND, that decision's `requires_human_approval` becomes UNCONDITIONALLY true, so the cheap-local-route-without-approval path is gone; that direction is strictly safer and is the whole reason DECISION F275 D9 permits the degradation, but it is still a behaviour a user could observe and it is recorded here rather than left to be discovered from a deleted file. THIRD, the SURVIVING cockpit section `_build_token_economy_section` loses its `ollama_placeholder_available` key, which is the only place the dashboard reported whether the Ollama placeholder route existed. WHY THIS IS ONE ID AND NOT THREE, per §3 item 30: it is one defect — the registry was the only source of a worker spec — with three instances, which is the same reading R-0831 records for its own eight knobs. WHY IT IS NOT R-0831: that finding is about user-settable route-policy KNOBS having no equivalent in F110's configuration, and this one is about a RECOMMENDATION Remedy no longer makes and a cockpit key it no longer publishes; resolving one does not resolve the other and the two must not be resolved in contradictory directions. THE INHERITING FEATURE IS F110, model routing, which F260's Design already names for routing; nothing here asks for a rebuild, and T001 RULE 3 forbids a stub, a shim or a copy. WHAT WOULD RESOLVE IT: DECISION F260 D3, the deletion paragraph, naming the routing recommendation and the placeholder-readiness key among the ideas DELETED rather than inherited, and naming this id — the same round R-0831 is bound to, so that the two are ruled together.

Note: F275 R20 — new evidence for the OPEN finding R-0858, added rather than given an id of its own per §3 item 30. R-0858 records that `docs/roadmap/features/T2_F267.md` is `[ ]` in `docs/roadmap/STATUS.md` while its own text names `execution.approval-list` and `execution.template-list`, two commands F275 deleted, so a session that one day claims F267 will plan against commands that cannot exist. MEASURED at `0d18e58a` by the reviewer's round 20 sweep: that file's line 28 ALSO names `worker.registry-list`, which round 20 deletes, so the count of dead commands in F267's plan rises from two to three. `docs/roadmap/features/T2_F262.md` line 76 carries the same string and is deliberately NOT included, because F262 is `[x]` and a closed feature's account of what it built is a historical record rather than an open plan — the same reading R-0858 already applies to `T2_F085.md`. R-0858's fix clause is unchanged and still binds the round that drafts DECISION F260 D3; this note only widens what that repair must reach.
--- END-LEDGER20 ---

--- BEGIN-SLIPS20 ---
2026-09-09 · F275 R19 · The round 19 block ordered the worker to delete every line of `tests/orchestration/cluster_deletion_map.txt` beginning `packages.orchestration.overnight_readiness <-`, and that file holds no such line and names that module nowhere. The order was carried over by shape from round 18, whose module DID have three such lines, without measuring the file for round 19's module. The reviewer's own dry-run script hid it: the script filtered the lines and printed a completion message unconditionally, so removing zero lines looked exactly like removing three. Nothing landed wrong — the worker declined the no-op and declared it, which left one MISSING path in the round's path set. The lesson is that a filter used as a measurement prints the COUNT it removed, never a fixed message, and that a change-set entry carried over from the previous round's shape is re-measured against this round's subject before it is ordered.

2026-09-09 · F275 R19 · The round 19 block told the worker the suite count "MUST fall" because the round deletes two whole test files, and the real fall was 37 against the 29 those two files hold. The other eight are parametrized `[overnight]` cases in `tests/test_grouped_cli.py` generated from the catalog `GROUPS`, so deleting a command GROUP deletes tests in a file the change set never names. The worker closed the gap by a node-id set difference rather than by arithmetic and showed no node id was added, which is the stronger reading. The lesson is that a round deleting a catalog GROUP predicts its suite delta from the generated cases as well as from the deleted files, because a parametrized suite couples test count to production data and the coupling is invisible in a change set.
--- END-SLIPS20 ---

--- BEGIN-DECISION20 ---
## DECISION F275 D9 — `token_economy` degrades FAIL-SAFE when the Worker Registry is deleted; its routing recommendation is not cluster surface that dies with it (2026-09-09, F275 round 20)

THE QUESTION. `packages/orchestration/worker_registry.py` is component 1 of
`.agent/f275_deletion_order.md` and is deleted by this round under T001 RULE 1. The
SURVIVING module `packages/orchestration/token_economy.py` does not merely import a helper
from it: its routing recommendation is built out of it. One of the imported symbols is not a
convenience. `hard_safety_requires_approval` describes itself in its own docstring as a "HARD
safety invariant (R-0095)" and states that a user policy "may add stricter approval but must
NEVER weaken this"; it forces human approval for expensive or unknown cost, for high, blocked
or unknown risk, for the external-builder and cloud kinds, for the cloud execution mode and
for every placeholder route. F275's own "Do not touch" section names THE APPROVAL GATE among
the things this feature may not touch. So the deletion removes an approval-forcing invariant
from a surviving module, and T001 RULE 3 — the survivor loses the call site and never gains a
copy — points straight into that collision. Session 10's handback recorded the collision as
unresolved anywhere on disk and ruled that round 20 must settle it before the first `git rm`.

THE MEASUREMENT THAT SETTLES IT, taken at `0d18e58a`. The approval disjunction in
`compute_token_economy_decision` already ended in `or not spec`. That term is not decoration:
before this deletion, a job whose route policy left no eligible worker resolved `spec` to
`None` and required human approval for that reason alone, independently of the hard-safety
call. Deleting the registry makes `spec` unresolvable for EVERY job, so the term that was
reached occasionally is now reached always and `requires_human_approval` is unconditionally
true. The invariant is therefore preserved by DEGRADATION and is strictly STRICTER than the
floor it replaces: the deleted check forced approval for a named set of risky routes, and
what replaces it forces approval for all of them. Nothing that previously required approval
stops requiring it, which is the only property F275's "Do not touch" clause protects.

THAT THE DEGRADATION IS PINNED BY TESTS RATHER THAN MERELY WRITTEN was measured BY THE
REVIEWER'S APPLIED DRY RUN OF THIS ROUND, before this block was authored, in a disposable
worktree at `0d18e58a` with the whole change set applied, over the node set
`tests/orchestration/test_token_economy.py`,
`tests/orchestration/test_token_economy_integration.py` and
`tests/ui_server/test_dashboard_cockpit_truth.py`: the unmutated control is exit 0 at 72
passed, forcing `requires_human_approval` to `False` is exit 1 at 5 failed and 67 passed, and
the revert returns exit 0 at 72 passed. The five named failures include
`TestIntegrity::test_real_unknown_decision_is_safe_under_audit`, which is this module's own
R-0099 audit invariant, so the safety property is held by a test that bites and not by a
comment.

CHOSEN. `token_economy` survives the deletion in a FAIL-SAFE form. It loses all three
`worker_registry` import statements, the whole of `estimate_route_token_band` — which has no
production caller and can never acquire one once no worker spec exists anywhere — and the
registry consultation inside `compute_token_economy_decision`. `recommended_worker_id` stays
empty, `estimated_cost_band` stays UNKNOWN, approval becomes unconditional, and the
reason/next-action ladder collapses to two branches whose `next_safe_action` strings name only
surviving commands. No worker spec type, no local reimplementation of
`hard_safety_requires_approval`, no compatibility reader: T001 RULE 3 and AGENTS.md's Scope
Control forbid all three by name. The capability genuinely lost — a named recommended worker,
a real cost band, and the cockpit's `ollama_placeholder_available` key — is registered as
finding R-0865 naming F110 as the inheriting feature, exactly as T001 RULE 3 orders.

ALTERNATIVES CONSIDERED. (1) Copy `hard_safety_requires_approval` into `token_economy`.
Rejected: T001 RULE 3 forbids it in terms, and a copy of a check whose only input is a worker
spec is dead code the moment no worker spec exists. (2) Rule the whole routing recommendation
cluster surface and delete `compute_token_economy_decision` with the registry. Rejected: that
is a claim about a SURVIVING module's purpose rather than about the cluster, F275's own scope
says no module outside F260's Design lists is deleted, and the function's other three inputs —
the budget profile, the context estimate and the pack recommendation — are unrelated to the
cluster and are read by `remedy token economy-report`, the cockpit and `routing_token_hint`.
Establishing it would need a measurement of every consumer of `token_economy` that this round
has no reason to open. (3) Keep `worker_registry.py` alive for this one consumer. Rejected: it
is a component of an order the operator ruled PERFORMED rather than prepared, and a module
kept for one caller is the attic AGENTS.md Scope Control refuses.

HOW TO REVERSE. Restore `packages/orchestration/worker_registry.py` from `0d18e58a`, restore
the three import statements, `estimate_route_token_band` and the registry consultation in
`compute_token_economy_decision`, restore the deleted `token_economy` tests, and re-add the
module to the reachability allowlist, `CLUSTER_MODULES` and the deletion map. Reversing this
decision restores a WEAKER approval rule than the one it installs, because the unconditional
floor becomes conditional again; a reversal that intends to keep the stricter behaviour must
keep `d.requires_human_approval = True` as well.
--- END-DECISION20 ---
