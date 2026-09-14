STEP T001 round 14 — F275 one world completion, part three
SESSION 8 of F275 · round 14 · rounds so far 13 · soft limit 20 sessions and 60 rounds by
operator amendment amend0908-f275-finish RULE 1, so no scope report is owed.

Goal: delete the NINTH module group of F260's prototype cluster,
packages/orchestration/local_model_advisor.py, whole, together with everything that exists
only for it, and remove the call sites from the three survivors that lose code.

THIS IS A PRODUCTION-CODE ROUND, NOT A DELETION ROUND. Operator amendment
amend0906-triage-throughput defines a deletion round as one whose change set holds no EDITED
line under packages/, apps/ or tests/. This round edits six such files, and one of the edits
changes an exported JSON contract, so the four-measurement shortcut does NOT apply and the
gate-budget bullet of docs/agents/planner_reviewer_prompt.md §3 keeps mutation red-proofs
mandatory in full. G6 is that proof.

EVERY NUMERAL IN THIS BLOCK WAS MEASURED BY THE REVIEWER FROM AN APPLIED DRY RUN of this exact
change in a disposable worktree at 16494bbd, with the full suite run to completion, not from
reading the source. Where the reviewer's own environment could not reproduce the worker's, the
block orders the worker to REPORT its measurement instead of asserting a number.

Bundle, in commit order:
  C0a  save this block verbatim to .agent/authored/f275-r14.md
  C0b  mirror the same bytes to .agent/last_block.md
  C1   .agent/plan.md replaced WHOLE by the PLAN14 slice
  C2   append LEDGER14 to .agent/live_review.md and SLIPS14 to .agent/prose_slips.md
  C3   the deletion and the survivor edits, all 24 paths, ONE commit
  C4   .agent/handoff.md rewritten whole

CHANGE SET — EXACTLY these 24 paths at C3, nothing else, measured 14 insertions against 1845
deletions. The +/- column is the reviewer's dry-run numstat and the worker reports its own.

  DELETED WHOLE, five files:
    packages/orchestration/local_model_advisor.py            0/947   the module
    apps/cli/commands/local_advisor_cmd.py                   0/101   its handler file; BOTH
                                                                     handlers drive it
    tests/orchestration/test_local_model_advisor.py          0/396   the module's tests
    tests/cli/test_local_advisor_cli.py                      0/96    the handler's tests
    docs/system/local-model-advisor-v0.md                    0/96    describes the adapter

  SURVIVORS THAT LOSE CODE — this is what makes the round a production round:
    packages/orchestration/orchestrator_brain.py             0/127
    packages/orchestration/run_contract.py                   0/8
    apps/cli/commands/orchestrator_cmd.py                    1/10
    apps/cli/grouped.py                                      0/2
    apps/cli/command_catalog.py                              1/33
    apps/cli/commands/__init__.py                            1/2
    packages/orchestration/provider_trust_verification.py    1/1

  RATCHETS AND PACKAGING:
    pyproject.toml                                           0/2
    tests/orchestration/import_reachability_allowlist.txt    0/2
    tests/orchestration/cluster_deletion_map.txt             0/1
    tests/orchestration/test_cluster_deletion_map.py         0/2
    .agent/f275_deletion_order.md                            0/1   REGENERATED, never edited

  DOCS THE DELETION FALSIFIES — every one LINKS the deleted page or claims it is built:
    docs/README.md                                           0/2
    docs/system/orchestrator-brain-v0.md                     5/7
    docs/system/provider-trust-verification-v1.md            2/3
    docs/system/self-dogfood-execution-v0.md                 0/1
    docs/system/bounded-overnight-executor-v0.md             0/1
    docs/archive/expensive-builder-routing-future.md         2/3
    docs/archive/expensive-builder-routing-v0-plan.md        1/1

THE SURVIVOR EDITS, each by anchor. Read every file whole before editing it, per AGENTS.md.

 (1) packages/orchestration/orchestrator_brain.py — delete the CONTIGUOUS span that begins at
     the line `def _lower_confidence(level: str) -> str:` and ends immediately before the
     banner line whose next line is `# Report (Step 1476) + exports`. That span is three
     top-level definitions — `_lower_confidence`, `_evidence_is_weak` and
     `consult_local_advisor_for_decision`. The two helpers die with it because, measured at
     16494bbd, their ONLY call sites are inside the third. Then delete the dataclass line
     `    advisor: dict[str, Any] | None = None  # optional local-advisor critique (Step 1509)`
     and, in `export_decision_json`, the line `        "advisor": d.advisor,`.

     TWO ENUM MEMBERS SURVIVE, AND THIS IS A MEASUREMENT RATHER THAN AN OMISSION.
     `RoutingTier.LOCAL_ADVISOR_PREFERRED` is the FALLTHROUGH RETURN of the surviving
     `_model_routing_plan` and is asserted by the surviving
     `tests/orchestration/test_orchestrator_brain.py` line 210, so deleting it would change a
     survivor's behaviour and turn a surviving test red. `OptionKind.LOCAL_ADVISOR_NEEDED` and
     its `_BASE_SCORE` weight are ALREADY dead at 16494bbd — nothing anywhere constructs an
     option of that kind — so they are dead independently of this deletion and removing them
     would be the "while I'm here" edit AGENTS.md Scope Control forbids. Leave both. The note
     at the fallthrough that calls the adapter "not built" BECOMES TRUE at this round and is
     also left alone.

 (2) packages/orchestration/run_contract.py — delete the four-line comment beginning
     `    # Local Model Advisor Adapter v0 (Step 1515)` together with the two members
     `LOCAL_ADVISOR_STATUS` and `LOCAL_ADVISOR_RUN` directly beneath it, and delete the two
     lines `    ContractAction.LOCAL_ADVISOR_STATUS,` and `    ContractAction.LOCAL_ADVISOR_RUN,`
     from `_DEFAULT_ALLOWED_ACTIONS`. `ALL_KNOWN_ACTIONS` is derived from `vars(ContractAction)`
     and shrinks by itself; do not edit it.

 (3) apps/cli/commands/orchestrator_cmd.py — in `_cmd_orchestrator_decide`, drop
     `consult_local_advisor_for_decision` and `persist_decision` from the import, delete the
     `use_advisor` local and the whole `if use_advisor:` branch, and make the remaining call
     read `d = select_orchestrator_decision(s, persist=True)`. `persist_decision` leaves the
     import because its only call was inside the deleted branch.

 (4) apps/cli/grouped.py — delete the two-line `elif arg.name == "--use-local-advisor":` branch.
     The `--new` branch two branches above it STAYS: two surviving commands still declare it.

 (5) apps/cli/command_catalog.py — delete the `"local-advisor": GroupDef(...)` line; delete the
     two `local-advisor.status` and `local-advisor.run` CommandEntry blocks together with their
     `# ── local-advisor` section comment and the blank line that separates them from the next
     section; and on the SURVIVING `orchestrator.decide` entry delete the `--use-local-advisor`
     and `--new` ArgDefs and drop `"local-advisor.run"` from its `related` tuple. Both those
     ArgDefs are advisor-only: the `--new` help text reads "Force a fresh advisor run".

 (6) apps/cli/commands/__init__.py — delete `local_advisor_cmd` from the import block and its
     name from the `for mod in (…)` tuple.

 (7) packages/orchestration/provider_trust_verification.py — one docstring line. Replace
     `  - Model/local-advisor output, if consulted, is critique ONLY and can never pass or`
     with
     `  - Model output, if consulted, is critique ONLY and can never pass or`.
     The safety invariant is unchanged; only the name of a product that no longer exists goes.

THE DOC PAIRS. Each is a REWRITE or a pure deletion — the containment test was run on every
one and NOT ONE TO CONTAINS ITS FROM, so no append obligation arises and no FROM-zero count is
ordered over a file that legitimately repeats prose.

 (8) docs/system/orchestrator-brain-v0.md, FROM the five lines beginning
     `Deterministic decisioning is preferred whenever evidence is sufficient. The optional`
     and ending `never change the deterministic action. Expensive/external builders remain reserved for`
     TO these five lines:
Deterministic decisioning is preferred whenever evidence is sufficient. Remedy
deliberately has NO local model advisory adapter: the optional loopback critique that once
sat behind the routing plan was deleted with F260's prototype cluster, so the
`local_advisor_preferred` routing tier is a plan label and nothing consults a model for it.
Expensive/external builders remain reserved for
     Then delete the two-line Future bullet beginning
     `- [Local Model Advisor Adapter v0](local-model-advisor-v0.md) — **built**: optional cheap`.

 (9) docs/system/provider-trust-verification-v1.md — replace `An optional local-advisor critique`
     with `An optional local model critique` on its one line, and delete the trailing
     ` See` plus the following whole line `[local-model-advisor-v0.md](local-model-advisor-v0.md).`
     so the paragraph ends `keeping the hard safety invariant trivially true.`

 (10) docs/system/self-dogfood-execution-v0.md and docs/system/bounded-overnight-executor-v0.md
      — delete the one `- [local-model-advisor-v0.md](…)` bullet in each.

 (11) docs/archive/expensive-builder-routing-future.md — unlink, do not rewrite history:
      `   [local model advisor](../system/local-model-advisor-v0.md) may *critique* the deterministic plan`
      becomes `   local model advisor may *critique* the deterministic plan`; `the local-advisor budget.`
      becomes `the local advisor budget.`; and the See-also bullet
      `- [local-model-advisor-v0.md](../system/local-model-advisor-v0.md)` is deleted.

 (12) docs/archive/expensive-builder-routing-v0-plan.md —
      `3. The **local advisor** ([local-model-advisor-v0.md](../system/local-model-advisor-v0.md)) was tried`
      becomes `3. The **local advisor** was tried`.

 (13) docs/README.md — delete the quick-find row and the index row for the deleted page,
      matching on the LINK TARGET `system/local-model-advisor-v0.md`, never on a slug.

 (14) .agent/f275_deletion_order.md — REGENERATE from `measured_order()` in
      tests/orchestration/test_cluster_deletion_order.py. Keep the 26-line comment header
      BYTE-VERBATIM; its sha256 is
      aff913e6eedb4d9c7e5ab6e76578be881ffffa3612018cf58b5a48ad508b0cc2 and must be unchanged.
      The body is `", ".join(component)` per component, one per line. Seven components become
      SIX and the new first line is `packages.orchestration.managed_builder_execution`.

TWO FILES THAT NAME THE DYING GROUP ARE DELIBERATELY NOT TOUCHED, and this is the round's one
scope ruling. docs/system/core-product-spine-v0.md line 129 and docs/system/vocabulary.md line
155 advertise `local-advisor` among a list of command groups. Both are instances of the OPEN
finding R-0843, whose fix clause — booked at Note: F275 R13 and quoted in LEDGER14 below —
routes the whole `docs/system/` group-name sweep into the round that drafts DECISION F260 D3,
with quoted spans INCLUDED rather than stripped, and forbids the instance-fix. Repairing one
group name there now is exactly the staleness-family error that clause exists to prevent.

Constraints:
 1. Apply every authored slice BYTE FOR BYTE. Do not edit, reflow, renumber or "fix" a slice.
    If a slice looks wrong, apply it anyway and DECLARE it in the handback.
 2. The BEGIN and END marker lines are delimiters and never reach a target file. A slice is
    the bytes STRICTLY BETWEEN them.
 3. The change set above bounds WRITES at C3. No twenty-fifth path.
 4. Each of C1, C2 and C3 is ONE commit. Commit subjects carry no leading-slash token and no
    absolute path — the evidence metadata scanner rejects those and blocks closure.
 5. .agent/plan.md is replaced WHOLE by PLAN14 at C1, the FIRST substantive commit, per §3
    item 23, because this round's C2 touches the finding ledger.
 6. Both appends at C2 are `post = pre + b"\n" + slice`. Both targets end WITH a newline at
    16494bbd, so the joining byte adds one blank separator line. Base sizes, measured:
    .agent/live_review.md 608189 bytes, .agent/prose_slips.md 183299 bytes.
 7. Destructive verification runs ONLY inside a disposable git worktree, per
    docs/agents/self_drive_protocol.md G5. The primary checkout satisfies
    `git status --porcelain` == empty at the handback.
 8. Run the full suite SERIALLY. Under `-n auto` the ui_server command-channel tests race for
    a port. Run it in the PRIMARY checkout, where apps/ui/node_modules exists.
 9. This block is at most 490 lines TOTAL and at most 400 lines PROSE, where PROSE is TOTAL
    minus the body lines of the three slices. G2 orders both re-measured from the committed
    blob; report either overage plainly rather than repairing it.
 10. Every rule and separator in this block is ordinary prose. No line is a run of a repeated
    character, so nothing in the frame has a length a reader must recover by eye (§3 item 37).

Done when — EIGHT gates. Run every one, record its REAL exit code from the process object,
never through a pipe and never inferred. One line per gate in the handback.

 G1 TRANSPORT. The delegation source file, the C0a blob and the C0b blob are byte-identical.
    Report all three sizes and sha256 values. Per §3 item 37 this chain covers those three
    artefacts and claims NOTHING about the bytes the reviewer emitted.

 G2 THE PLAN AND THE BLOCK. .agent/plan.md at C1 is byte-identical to PLAN14; report bytes,
    sha256 and line count against the AGENTS.md cap of 50, and confirm `## Goal` and
    `## Next Steps` are both present. Re-measure this block's TOTAL and PROSE from the C0a
    blob and state both against constraint 9.

 G3 THE RECORD, from the COMMITTED blobs at C1 (pre) and C2 (post), all five parts:
    (a) byte arithmetic — growth == 1 + slice length for each file, prefix and suffix exact,
        joining byte re-read and shown to be a newline;
    (b) ordered unit equality — compare the LAST N blank-line units of the whole file against
        the slice's N paragraphs IN ORDER, where N is COUNTED by your script from the slice
        and is never a number this block asserts;
    (c) negative control — flip ONE byte IN MEMORY inside the FIRST appended paragraph of each
        file, per §3 item 36, and show BOTH readers REJECT it; then re-read both files from
        disk and show them byte-equal to their committed post-blobs;
    (d) count gates — `^Gate: ` 35 to 36; and `^Gate: F275 R13 `, `^Note: F275 R14 `,
        `^- R-0853 — ` and `^- R-0854 — ` exactly 1 each;
    (e) the open set BY DISTINCT ID, DECISION F085 D7, OPEN = REGISTERED minus DONE with a
        `Landed:` line NEVER subtracted: 81/4/77 before, 83/4/79 after.

 G4 THE DELETION IS COMPLETE. All five deleted paths absent from `git ls-tree -r <C3>`.
    Then sweep the tracked files OUTSIDE .agent/ and .data/ for these tokens:
    local_model_advisor, local_advisor_cmd, consult_local_advisor_for_decision,
    run_local_advisor, load_local_advisor_config, export_local_advisor_response_json,
    list_local_advisor_runs, LocalAdvisorRequest, LocalAdvisorStatus,
    LocalAdvisorDecisionImpact, LOCAL_ADVISOR_STATUS, LOCAL_ADVISOR_RUN, local_advisor_status,
    local_advisor_run, use-local-advisor, use_local_advisor, local-advisor,
    local-model-advisor-v0, REMEDY_LOCAL_ADVISOR.
    NEUTRALISE THE FOUR SURVIVING TOKENS FIRST — LOCAL_ADVISOR_PREFERRED, LOCAL_ADVISOR_NEEDED,
    local_advisor_preferred, local_advisor_needed — by removing them from each line before
    matching, or every survivor reads as a hit.
    Print the RAW result IN FULL; truncating it is a finding. Then delete every
    backtick-quoted span from each line and count again: THAT STRIPPED COUNT IS THE BINDING
    GATE and it must be EXACTLY 1, the single line docs/system/vocabulary.md:155, which the
    scope ruling above leaves to R-0843. The reviewer measured RAW 4 and STRIPPED 1 on the
    applied dry run; the other three RAW lines are docs/roadmap/features/T2_F260.md lines 338
    and 339, must-not-touch spec, and docs/system/core-product-spine-v0.md line 129.

 G5 THE SHIPPED READERS AND THE ORDER FILE. Read `apps.cli.command_catalog._BASE_CATALOG`,
    `apps.cli.commands.collect_all_handlers()`, `apps.cli.command_catalog.GROUPS` and
    `packages.orchestration.run_contract.ALL_KNOWN_ACTIONS` BY IMPORT, never by grep, at the
    base and at C3. PIN sys.path or PYTHONPATH to the tree you mean and PRINT the resolved
    `__file__` before trusting any number: an editable install shadows a worktree otherwise.
    Expected, measured by the reviewer: _BASE_CATALOG 269 to 267, collect_all_handlers 269 to
    267, GROUPS 50 to 49, ALL_KNOWN_ACTIONS 122 to 120, duplicate ids 0 at both ends.
    Show `local-advisor.status` and `local-advisor.run` ABSENT from both readers at C3 and
    `local-advisor` gone from GROUPS. Show `orchestrator.decide`, `orchestrator.inspect`,
    `orchestrator.report`, `provider.verify`, `patch.approve` and `do.continue` PRESENT in
    both readers at C3 — the human approval path R-0853 turns on is untouched.
    Show `orchestrator.decide` args falling from `('--job-id', '--use-local-advisor', '--new',
    '--json')` to `('--job-id', '--json')`.
    Show the exported decision key set falling from 20 keys to 19 with `advisor` gone.
    Show the regenerated order file at SIX components against seven, its 26-line header sha256
    unchanged, and the file EQUAL to a fresh regeneration from the live import graph.

 G6 THE RED-PROOFS, MANDATORY IN FULL for a production round, ALL inside a disposable
    worktree at C3. Run the UNMUTATED control FIRST and report its exit code beside every
    mutated one; a colour with no baseline is not evidence. Restore each file byte-identically
    and prove it by sha256. Four probes, and TWO OF THEM ARE EXPECTED GREEN — report the
    colour you measure, never the colour named here:
      A  add `packages.orchestration.local_model_advisor` back to
         tests/orchestration/import_reachability_allowlist.txt, then run
         tests/orchestration/test_import_reachability.py. Reviewer measured exit 1.
      B  add `"packages.orchestration.local_model_advisor"` back to CLUSTER_MODULES in
         tests/orchestration/test_cluster_deletion_map.py, then run that file and
         test_cluster_deletion_order.py. Reviewer measured exit 1, 2 failed.
      C  put the `"local-advisor": GroupDef(...)` line back with NO command and NO handler
         behind it, then run tests/cli/test_advertised_commands.py, tests/test_grouped_cli.py
         and tests/cli/test_cli_ux.py. Reviewer measured exit 0 at 507 passed — an ORPHAN
         GROUP IS INVISIBLE to every catalog guard. That green is the finding LEDGER14 books
         as a Note on R-0847, not a failure of this round.
      D  add a line `        "advisor": None,` back into `export_decision_json`, then run
         tests/orchestration/test_orchestrator_brain.py and tests/cli/test_golden_path.py.
         Reviewer measured exit 0 at 61 passed — NOTHING PINS the exported decision key set.
         That green is R-0854's measurement.

 G7 RUFF, THE RATCHETS AND THE FULL SUITE.
    (a) `python3 -m ruff check` over the EIGHT edited .py files that still exist at C3 —
        expect `All checks passed!`, exit 0.
    (b) `python3 -m ruff check .` repo-wide at C3 AND at the base 16494bbd, the base read in a
        disposable worktree or via `git show`, NEVER by writing to the primary checkout. Both
        must read the SAME count; the reviewer measured `Found 26 errors.` at both. Exit 1 on
        those two runs is ruff reporting the pre-existing 26 and is the expected reading at
        both ends — the gate is the EQUALITY, not the exit code.
    (c) `python3 -B -m pytest` over test_import_reachability.py, test_cluster_deletion_map.py,
        test_cluster_deletion_order.py, tests/docs/, test_advertised_commands.py,
        test_cli_ux.py and test_product_spine.py — reviewer measured 442 passed, exit 0.
    (d) the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`, exit 0.
    (e) THE FULL SUITE, `python3 -B -m pytest tests/ -q`, SERIALLY, in the PRIMARY checkout,
        with the change COMMITTED. REPORT THE NUMBERS YOU MEASURE. This block asserts no pass
        count for it, because the reviewer's own run was an UNCOMMITTED dry run in a worktree
        with no apps/ui/node_modules and read 18836 passed, 29 skipped and 2 failed — both
        failures artefacts of that environment, both controlled at the base: the vitest node
        fails at the base worktree too for a missing node_modules, and the porcelain node
        `test_every_enumerated_path_exists_in_this_repo` PASSES at the base and fails only
        because a dry run is uncommitted. The BINDING conditions are: ZERO failed, and
        passed + skipped == the C3 collection.
    (f) THE ARITHMETIC, BY THE ID SET. Collect at the base and at C3 in the SAME environment
        as each other and report `--collect-only` totals, the FALL and the GAINED count. The
        reviewer measured, both sides in matched worktrees, base 18919 and tip 18867, a fall
        of 52 with ZERO gained, attributed 38 to tests/orchestration/test_local_model_advisor.py,
        8 to tests/test_grouped_cli.py, which parametrises over the catalog and is in no
        change set, and 6 to tests/cli/test_local_advisor_cli.py.

 G8 THE TREE. Re-read .agent/STOP from disk and show it absent. `git status --porcelain`
    empty. `git worktree list` naming the primary checkout ALONE. Branch correct.
    `git diff --name-only <C2>..<C3>` compared as a SET against the 24 paths above: report the
    count, the missing set, the extra set and whether the match is exact. Report each commit's
    parent count and insertion count against the AGENTS.md DECISION F104 D1 cap of 500, for
    C0a through C3; C4's own numbers belong to the next round's ledger entry, per §3 item 31.

Handback: rewrite .agent/handoff.md WHOLE at C4, per docs/agents/handback_template.md. It has
NO length cap. Carry the mandated sections: SESSION 8 of F275 and the round, the range, a
per-commit changed-files table with a +/- column read from `git diff --numstat` and NOT from
file line counts, external actions, one line per gate with its real exit code, the
authored-text proofs, deviations and assumptions, the item-status table, the open-findings
count, and the next expected action. Push ONCE, after C4. Create NO pull request: under
docs/roadmap/STATUS_closure_protocol.md the PR belongs to this feature's closure sequence.
Write NO verdict, NO `Done:` paragraph and NO finding of your own — only the reviewer's text
sets those. If a fix lands that the reviewer has not yet resolved, write a `Landed:` line.

--- BEGIN-PLAN14 ---
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 14 books round 13's PASS and one prose slip, registers R-0853 and R-0854, adds one
measured instance to the open finding R-0847 as a NOTE, and deletes the NINTH module group,
`packages/orchestration/local_model_advisor.py`, whole. This is a PRODUCTION round rather than
a deletion round: `orchestrator_brain.py` loses the adapter entry point, two private helpers,
the `advisor` dataclass field and the `advisor` key of the exported decision JSON;
`run_contract.py` loses two `ContractAction` members; and `orchestrator_cmd.py`, `grouped.py`
and `command_catalog.py` lose the `--use-local-advisor` path. Two enum members SURVIVE by
measurement rather than by omission.

## Next Steps

1. The `managed_builder_execution` component, which this round's regeneration makes the
   order file's first line. It is a SINGLE module.
2. The remaining components in the recorded order — every one a single module except the
   `provider_trust` / `provider_trust_verification` pair, which is the last cycle.
3. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831,
   R-0840, R-0842, R-0844 through R-0846, R-0848, R-0849 and R-0851 through R-0854 named among
   the ideas deleted rather than inherited. That round also discharges R-0843's widened sweep.
4. T002, the atomic record flip, alone, because every later commit's size depends on its ruling.

## Risks

- The open set is 77 by distinct id at this round's base `16494bbd`; the ledger commit this
  block fixes as C2 registers two, taking it to 79. Four are High — R-0803, R-0804, R-0806 and
  R-0807 — all F273's rather than this feature's, per DECISION F272 D12.
- R-0847 stays OPEN and now holds a second face, measured at this round's dry run: a `GroupDef`
  left behind with no command and no handler passes every catalog guard at exit 0.
- The exported orchestrator decision JSON has NO test pinning its key set, so R-0854's contract
  change is invisible to the suite. That was measured by probe, not assumed.
- The full suite is run SERIALLY: under `pytest -n auto` the `ui_server` command-channel tests
  race for a port, and the vitest node needs `apps/ui/node_modules`.
--- END-PLAN14 ---

--- BEGIN-LEDGER14 ---
Gate: F275 R13 — the F275 round 13 entry. VERDICT PASS, booked by round 14 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, and carried from the pushed `.agent/handoff.md` at `16494bbd`, which that rule makes a durable carrier. THE VERDICT WAS ISSUED BY THE PLANNER AND REVIEWER OF SESSION 7, which re-ran every one of the eight gates itself against the COMMITTED blobs over the range `053a25a7`..`21d6268b`; that session's own account is the handback text this entry books, and session 8 does not restate those readings as if it had taken them. Six single-parent commits C0a `3a9ebc38`, C0b `ca833831`, C1 `a991c91c`, C2 `8a688931`, C3 `04ca209c` and C4 `21d6268b`, per-commit insertions 232, 150, 16, 8, 2 and 287, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 was the PRIMARY proof of §4 item 9 and not the digest fallback: source and both committed copies 27171 bytes at `5b3ad1d125cdb0bf55a47e73c601b0cf005d087aa73b1bcaaf32324123df5010`, byte-equal. G2: `.agent/plan.md` byte-identical to PLAN13 at 2697 bytes, 45 lines against the cap of 50. G3: `.agent/live_review.md` 597513 to 608189, growth 10676 = 1 + 10675; `.agent/prose_slips.md` 182696 to 183299, growth 603 = 1 + 602; N counted from each slice as 3 and 1, ordered equality over the whole appended region, both negative controls flipped in the FIRST appended paragraph and REJECTED by both readers; `^Gate: ` 34 to 35; THE OPEN SET 76 TO 77 BY DISTINCT ID. G4: six whole-file removals absent at C3, the sweep run TWICE over 1695 tracked files reading exactly TWO lines RAW — `T2_F260.md:337` and `T2_F272.md:744`, both must-not-touch spec — and ZERO stripped. G5: ratchets and canary 484 passed; through the SHIPPED readers `_BASE_CATALOG` and `collect_all_handlers()` both fell 276 to 269 and `GROUPS` 51 to 50; the regenerated order file held SEVEN components at a `0 1` numstat, a PURE deletion. G6: ruff clean over three files, `Found 26 errors.` at both ends. G7: the full suite re-run SERIALLY IN THE PRIMARY CHECKOUT, GREEN at 18896 passed, 23 skipped, ZERO failed, and 18896 + 23 = 18919 equals the tip collection against 18958 at the base. G8: STOP absent, porcelain empty, ONE worktree, 13 paths in an EXACT SET MATCH. WHAT THE ROUND ACHIEVED: the EIGHTH module group, `external_builder_sandbox` at 560 module lines, in ONE commit at 2 insertions against 1401 deletions over 13 paths, taking its handler file WHOLE, seven commands, the `external-builder` group, two test files and two doc pages. TWO NON-DEFECT DEVIATIONS WERE DECLARED AND BOTH ARE SUSTAINED: the block's `18888 passed` was its own worktree dry run against an ordered run reading 18896, and `docs/README.md` line 167 was the POST-deletion position of a surviving archive row that sits at 171 at the base. NO FINDING IS RESOLVED BY THIS GATE.

Note: F275 R14 — A SECOND FACE OF THE OPEN FINDING R-0847 IS MEASURED AND ADDED HERE RATHER THAN MINTING A NEW ID, per docs/agents/planner_reviewer_prompt.md §3 item 30, which requires the open set to be searched for the DEFECT before an id is spent. R-0847 registers that `tests/cli/test_advertised_commands.py` cannot see an advertisement whose command GROUP has been deleted, because its scanner skips every match whose group is not in `GROUPS`. THE SECOND FACE IS THE OPPOSITE CONDITION AND IS WORSE, because it is silent in the other direction: a group that IS in `GROUPS` but has NO command and NO handler behind it passes every catalog guard this repository owns. THE MEASUREMENT, taken by the reviewer at `16494bbd` inside a disposable worktree as probe C of round 14's red-proof: with the whole `local-advisor` deletion applied, the `"local-advisor": GroupDef(...)` line was put BACK ALONE — no `CommandEntry`, no handler module, no handler function — and `tests/cli/test_advertised_commands.py`, `tests/test_grouped_cli.py` and `tests/cli/test_cli_ux.py` ran to EXIT 0 at 507 passed, against an unmutated control of exit 0 at 470 passed in the same worktree. So a whole-group deletion that forgot its `GroupDef` would ship an empty group to an operator and no gate in the suite would say so. WHY THIS IS NOT A SECOND ID: R-0847's own headline is that "every whole-group deletion widens a blind spot", and this is that same blind spot read from the other side — the same guard file, the same `GROUPS` membership test, and one fix serves both. THE FIX CLAUSE ON R-0847 IS WIDENED BY THIS PARAGRAPH: whatever repairs the scanner must ALSO assert that every id in `GROUPS` has at least one `CommandEntry` in `_BASE_CATALOG` and at least one handler in `collect_all_handlers()`, which is a one-expression ratchet over the two shipped readers and needs no new machinery. Round 14 itself removes the `GroupDef` correctly, so nothing is wrong on disk today and this paragraph records a gate that cannot fail rather than a defect that landed.

- R-0853 — Medium, DELETING `local_model_advisor` REMOVES THE WHOLE LOCAL-MODEL ADVISORY CRITIQUE — the `local-advisor` group, both its commands, AND the `--use-local-advisor` path on the SURVIVING `orchestrator decide` — so Remedy can no longer have a cheap local model critique any decision. Raised by the reviewer while authoring F275 round 14, because operator RULE 3 in `docs/roadmap/features/T2_F275.md` T001 requires a deletion that takes away a behaviour a user could observe to register a finding naming the behaviour and the feature that inherits the idea. THE MEASUREMENT, taken at `16494bbd` by an APPLIED dry run of the whole deletion in a disposable worktree, through the SHIPPED readers rather than by grep: `len(_BASE_CATALOG)` and `len(collect_all_handlers())` both fall 269 to 267, `len(GROUPS)` falls 50 to 49, and `len(ALL_KNOWN_ACTIONS)` in `packages/orchestration/run_contract.py` falls 122 to 120 as the two `ContractAction` members `local_advisor_status` and `local_advisor_run` go with the adapter they gated. The two command ids are `local-advisor.status` and `local-advisor.run` — the whole of the group, which loses its `GroupDef` too. WHAT A USER LOSES BEYOND THOSE TWO COMMANDS, and this is why the finding is not merely "a group died": the surviving `orchestrator decide` loses its `--use-local-advisor` and `--new` flags, measured as its `ArgDef` tuple falling from `('--job-id', '--use-local-advisor', '--new', '--json')` to `('--job-id', '--json')`, so the advisory critique disappears from a command that SURVIVES and keeps its name. The capability itself was loopback-only, opt-in, disabled by default, and by its own design could only ever LOWER confidence, add missing-evidence hints or escalate weak evidence to human review — it could never strengthen a decision, execute, apply or approve. WHAT IS EXPLICITLY NOT LOST, which is why the severity is Medium rather than High: the deterministic decision path is untouched and was never allowed to depend on the advisor, and the human approval path is untouched — `orchestrator.decide`, `orchestrator.inspect`, `orchestrator.report`, `provider.verify`, `patch.approve` and `do.continue` are all PRESENT in both shipped readers at the round's tip. `RoutingTier.LOCAL_ADVISOR_PREFERRED` also survives, so an orchestrator decision can still SAY that a cheap local critique would help; there is simply nothing left that provides one, and the fallthrough note in `_model_routing_plan` calling the adapter "not built" becomes true again rather than stale. THE FEATURE THAT INHERITS THE IDEA IS F110, model routing, which owns which model tier a task class routes to and is the only surviving home for "consult a cheap local model". WHAT WOULD RESOLVE IT: DECISION F260 D3, the deletion paragraph, naming this id and the `local-advisor` group among the ideas DELETED rather than inherited, naming F110 as the inheritor of local-model advisory critique, and recording that Remedy deliberately consults no model when deciding today. A stub, a shim, an alias or a compatibility reader is forbidden by AGENTS.md Scope Control by name, and this finding is not resolved by providing one.

- R-0854 — Medium, THE EXPORTED ORCHESTRATOR DECISION LOSES ITS `advisor` KEY, WHICH IS A USER-OBSERVABLE JSON CONTRACT CHANGE, AND NO TEST IN THE SUITE PINS THE EXPORTED KEY SET, SO THE CHANGE IS INVISIBLE TO EVERY GATE. Raised by the reviewer while authoring F275 round 14 and registered SEPARATELY from R-0853 because the defect, the file and the fix all differ: R-0853 is about commands and a group disappearing from the catalog, and this one is about the SHAPE of a document a surviving command still emits. THE FIRST MEASUREMENT, taken at `16494bbd` by importing `packages.orchestration.orchestrator_brain` at both ends of an applied dry run: `export_decision_json` returns 20 keys at the base and 19 at the tip, the missing one being `advisor`, and `remedy orchestrator decide --json` is the surviving command that prints it. Anything that parsed that key — an operator script, a dashboard, a stored decision document written by an earlier version — reads `None` where it read a dict, and no deprecation window exists because AGENTS.md Scope Control forbids a compatibility reader by name. THE SECOND MEASUREMENT IS THE ONE THAT MAKES THIS AN ID RATHER THAN A NOTE, and it was taken as probe D of round 14's red-proof inside a disposable worktree: with the deletion applied, a line `"advisor": None,` was put BACK into `export_decision_json`, and `tests/orchestration/test_orchestrator_brain.py` together with `tests/cli/test_golden_path.py` ran to EXIT 0 at 61 passed. So the exported key set of an orchestrator decision is pinned by NOTHING — not by a golden file, not by a contract test, not by a schema — and a future round could add, remove or rename a key of this document without one test going red. That is a gate over production code shown to be blind, which is exactly what operator amendment amend0827-process-diet rule 2 reserves an R-id for. WHY THE ROUND STILL SHIPS THE REMOVAL: keeping the key while deleting everything that could populate it would leave a permanently-null field describing a capability that no longer exists, which is the "attic" AGENTS.md Scope Control forbids; the honest move is to remove it and record the loss here. WHAT WOULD RESOLVE IT, and both halves are owed: DECISION F260 D3 naming this id among the contract changes the deletion makes, and a test pinning the exported key set of `export_decision_json` — a single frozen set compared against the exported keys, which is the cheapest possible guard and would have caught this round's change on its own.
--- END-LEDGER14 ---

--- BEGIN-SLIPS14 ---
2026-09-09 · F275 R14 · The round-14 consumer map the session-7 handback carried was incomplete, and the reviewer of session 8 re-measured rather than trusting it: the map named `orchestrator_brain.py`, `orchestrator_cmd.py`, `grouped.py` and `command_catalog.py` but not `packages/orchestration/run_contract.py`, whose two `ContractAction` members exist only for the adapter, not the enum USE SITES at `orchestrator_brain.py` lines 687 and 807 that decide whether the two enum members may die, not the surviving assertion at `tests/orchestration/test_orchestrator_brain.py` line 210 that would have gone red had they been deleted, and not the See-also link at `docs/archive/expensive-builder-routing-future.md` line 40. Nothing landed wrong on disk, because the map was never applied — §3 item 34's "read every file the block orders a change against" is what caught it, and a handback map is a lead rather than a change set.
--- END-SLIPS14 ---
