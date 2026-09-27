STEP F288 R5 — THE FIRST HALF OF T003: prompts as `synapse` nodes of the live model, children of their task, drawn at graph_spec's synapse radius, and a click on one selecting the prompt itself

GOAL
Round 4 passed and R-1075 is resolved. Book both, record DECISION F288 D5, and land it: a pure
`withPromptNodes` composes the dashboard's prompt-trace items onto the live model as `synapse`
nodes; the layout draws them at graph_spec §4's radius on §6's link width; and a click on one
selects the prompt item, whose selection ring follows it. The simple view does not change.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE CHANGE IS SPECIFIED, NOT SLICED: you write the code
and its tests yourself against S1 to S6. Only the `.agent/` records travel as payloads. Read
DECISION F288 D5 in the records diff first: it is the design.

THE DIRECTORIES
  `.remedy-wt/f288-r5-payloads/` and `.remedy-wt/f288-r5/` are READ-ONLY; every other
  `.remedy-wt/f288-*` directory and `.remedy-wt/f288-review/` belongs to the reviewer.
  `.remedy-wt/f288-r5-worker/` is YOURS; create it if absent. All are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the file.
Never run npm or npx; the one Node binary you may run is
`/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest`, from
`/home/decodeux/Repos/remedy/apps/ui`, as `vitest run <files>` while you work and as G5 orders.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f288-event-stream-completeness`, and `git log --oneline -1` must read `a5ee2dc8`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f288-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` and `git stash list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f288-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 70 | 15367 | bbeb1c63325b84676f19b966ac20544b4de8a6eb3b19e27452e59880779f18d3 |
| plan.md | 29 | 1056 | 25d4fd0efb47e045a29bd9bae3574c551f823ea5781bb3359a6ecc385c14d954 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `a5ee2dc8`. In `.agent/live_review.md` it replaces
R-1075's `Landed:` line with the reviewer's `Done:` paragraph and appends round 4's gate entry; it
appends DECISION F288 D5 to `.agent/decisions.md`.

THE SPECIFICATION
S1 THE BIRTH. A new module `apps/ui/src/components/graph/promptNodes.ts` exports
   `promptNodeId(itemId: string): string` answering `prompt:<itemId>`, and
   `withPromptNodes(model: BrainModel, items: readonly RemedyPromptTraceItem[]): BrainModel`, pure
   and total: for each item in order whose task node `task:<item.taskId>` is in `model.nodes` and
   whose `promptNodeId` is not, it appends a node `{ id: promptNodeId(item.id), kind: "synapse",
   state: <that task node's state>, parentId: "task:<item.taskId>", seq: 0, meta: { promptId:
   item.id, role: item.role, promptKind: item.promptKind, round: item.round, attemptId: item.runId }
   }` and one link built the way the reducer builds its links (`id` `<parent>-><child>`, `source`
   the task node, `target` the prompt node). Other items are skipped, and a call that appends
   nothing returns the SAME model object. The module's header comment names DECISION F288 D5 and
   graph_spec §2 and §3, and says the parent is the task for the reason D5 (3) gives.
S2 THE STAGE. In `apps/ui/src/components/graph/BrainGraphStage.tsx`, a memoized
   `promptItems` read from `dashboard.promptTrace?.items`, falling back to one module-level empty
   array so its identity is stable while the dashboard is; the `liveModel` line becomes
   `const liveModel = useMemo(() => withPromptNodes(rebuildBrainModel(dashboard.jobId, seeds, rows), promptItems), [dashboard.jobId, seeds, rows, promptItems]);`
   and `const model = scrub.scrubbedModel ?? liveModel;` stays exactly as it is, so a scrubbed model
   draws no prompt; and `selectedId` becomes
   `selectedPromptNodeId(promptItems, selectedNodeId ?? null) ?? selectedBrainNodeId(dashboard.tasks, selectedNodeId ?? null)`.
   Nothing else in the stage changes.
S3 THE LOOK. In `apps/ui/src/components/graph/buildForceBrainModel.ts`, `BRAIN_SYNAPSE_RADIUS = 2`
   and `BRAIN_SYNAPSE_LINK_WIDTH = 1`, each with a comment quoting graph_spec §4 and §6 as the
   existing constants do; a `synapse` layout node gets that radius, and a link whose target is a
   `synapse` gets that width. Its depth, its position rule and every other node and link stay as
   they are.
S4 THE MOUSE. In `apps/ui/src/components/graph/brainView.ts`, `selectionIdOf(node)` answers the
   prompt item id for a `synapse` whose id starts with `prompt:` (the id without that prefix) and
   `selectionTaskIdOf(node)` for every other node; and `selectedPromptNodeId(items, selectedNodeId)`
   answers `promptNodeId(selectedNodeId)` when an item's id equals `selectedNodeId`, and `null`
   otherwise. `selectionTaskIdOf` is unchanged. In `ForceBrainGraph.tsx`, the click handler's
   `const id = selectionTaskIdOf(n);` becomes `const id = selectionIdOf(n);`; its first line and its
   `if (isZoomRunKind(n.kind)) return;` stay, in the same order, and nothing else in that file changes.
S5 THE COMMENTS. The doc comment of `NodeKind` and the header of `brainOntology.ts` say that
   `synapse` is born by `withPromptNodes` from the dashboard's prompt trace (DECISION F288 D5), not
   by the reducer, and that `artifact` is still born by nothing.
S6 THE CONTRACT. In `tests/ui_contracts/test_timeline_scrub_wiring.py`, the one assertion that
   pins `const liveModel = useMemo(() => rebuildBrainModel(dashboard.jobId, seeds, rows)` is changed
   to pin S2's new line up to `rows), promptItems)` — the only edit of an existing test this round
   makes. In `tests/ui_contracts/test_brain_stage_mount.py`, a new test asserts that the stage source
   holds `withPromptNodes(` exactly once and inside the `liveModel` line, holds
   `const model = scrub.scrubbedModel ?? liveModel;`, and that ForceBrainGraph's click body — sliced
   the way `tests/ui_contracts/test_run_detail_wiring.py` slices it — calls `selectionIdOf(n)` and
   not `selectionTaskIdOf(n)`.

THE TESTS (vitest, beside the code)
`promptNodes.test.ts`: a synapse per item whose task exists, with the id, kind, parent, seq, meta
and link S1 names; its state equal to its task node's for at least three different task states; an
item whose task is absent skipped; an item repeated skipped the second time; item order kept; and
the same object answered for no items and for items that are all skipped.
`brainView.test.ts`: `selectionIdOf` for a synapse, a task, a run and the core, and
`selectedPromptNodeId` for a matching id, an unknown id and `null`.
`buildForceBrainModel.test.ts`: a model with two synapses under one task lays them out at radius 2
on links of width 1, positioned as that task's children, and the layout's node and link ids equal
the model's in order (the truth rule over a model holding prompts).

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.
C1 — `.agent/authored/f288-r5-block.md` := this block, `.agent/authored/f288-r5-records.diff` :=
  records.diff, `.agent/authored/f288-r5-plan.md` := plan.md, all by `shutil.copyfile`.
  Subject: `F288 R5 C1: copy round 5 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 99; STOP rather than commit if that is 500 or more.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F288 R5 C2: book round 4's PASS and R-1075's resolution, record D5 and the round 5 plan`
  Expected by `git show --numstat`: 48/0 decisions.md, 3/1 live_review.md, 8/8 plan.md.
C3 — THE MODEL AND THE LOOK: S1, S3 and S5 with `promptNodes.test.ts` and the
  `buildForceBrainModel.test.ts` additions.
  Subject: `F288 R5 C3: compose the prompt trace onto the live model as synapse nodes at graph_spec's radius`
C4 — THE STAGE AND THE MOUSE: S2, S4 and S6 with the `brainView.test.ts` additions.
  Subject: `F288 R5 C4: draw the prompts on the live stage and let a click select the prompt`
C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f288-r5-mutations.py`.
  Subject: `F288 R5 C5: add the mutation tool for the round's red proofs`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, per `docs/agents/handback_template.md`.
  Subject: `F288 R5 C6: rewrite handoff for round 5`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f288-r5-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `apps/ui/src/components/graph/promptNodes.ts`, `apps/ui/src/components/graph/promptNodes.test.ts`,
   `apps/ui/src/components/graph/BrainGraphStage.tsx`,
   `apps/ui/src/components/graph/buildForceBrainModel.ts`,
   `apps/ui/src/components/graph/buildForceBrainModel.test.ts`,
   `apps/ui/src/components/graph/brainView.ts`, `apps/ui/src/components/graph/brainView.test.ts`,
   `apps/ui/src/components/graph/ForceBrainGraph.tsx`,
   `apps/ui/src/components/graph/brainOntology.ts`,
   `tests/ui_contracts/test_timeline_scrub_wiring.py`, `tests/ui_contracts/test_brain_stage_mount.py`,
   and `.agent/handoff.md`. Report the list you measure with `git diff --name-only a5ee2dc8` at the
   branch tip after C6. `BrainGraphCanvas.tsx` (the simple view) is NOT in it.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. A test this round itself wrote that is wrong may be
   corrected before C6, and the correction is declared. An EXISTING test that goes red is never
   edited to pass, S6's one assertion excepted: report it, name it, and stop.
5. NOTHING IS MERGED, AND THE PRIMARY CHECKOUT NEVER LEAVES THE BRANCH: no `gh pr merge` or
   `gh pr create`, no `git checkout` or `git switch` in the primary checkout, no branch deletion,
   no force-push, no `git stash` of any kind. Read an older commit with `git show <sha>:<path>`.
6. Leave every existing worktree, branch and stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: F288's one run belongs to its closure.

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C6 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the table; then each
 `.agent/authored/f288-r5-*` payload copy compared byte for byte with its source (the block copy
 against `.remedy-wt/f288-r5/block.md`), read back with `git show <C1>:<path>`.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2240433 | 2d4a36d905e7109ec3386b181d22fae21bb165eef110f0f7b14f957f3f7986a9 |
 | .agent/live_review.md | 315776 | cc66f3145d66d16c1c6ece52f4dae86809c3a85d2542d8040761c32fabc635a0 |
 | .agent/plan.md | 1056 | 25d4fd0efb47e045a29bd9bae3574c551f823ea5781bb3359a6ecc385c14d954 |
 Also the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT at C2 (the reviewer read it empty).

G3 THE CODE — `python3 -m ruff check tests/ui_contracts/test_timeline_scrub_wiring.py
 tests/ui_contracts/test_brain_stage_mount.py` at C4 with its real exit code; then quote from the
 diff the whole of `withPromptNodes`, `selectionIdOf`, `selectedPromptNodeId`, and the stage's
 `promptItems`, `liveModel` and `selectedId` lines.

G4 THE TESTS — in the primary checkout at C5, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_self_healing_cycles.py tests/orchestration/test_long_run_executor.py tests/ui_server/test_sse_stream.py tests/ui_server/test_budget_tick_envelope.py tests/ui_contracts tests/ui_server/test_brain_demo_recording_live.py tests/ui_server/test_semantic_zoom_live.py tests/ui_server/test_timeline_scrub_live.py tests/ui_server/test_live_state.py tests/orchestration/test_event_names.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_ble001_ratchet.py tests/test_imports.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it at `a5ee2dc8` and read `1825 passed, 5 skipped` at real exit code 0: four D3
 quarantines in `tests/ui_contracts/test_graph_architecture.py` and `tests/ui_contracts/test_ux_quality.py`
 and the D12 one in `tests/test_agent_tooling.py`, which stay skipped. The vitest suite, the
 TypeScript compiler and the UI lint run inside it. Report every `SKIPPED` line and the Python
 nodes the round adds (`--collect-only -q` on the two edited Python test files at `a5ee2dc8` and at
 C5), and account for any other difference from 1825. Also `vitest run` over the whole suite from
 `/home/decodeux/Repos/remedy/apps/ui`, whose `Test Files` and `Tests` lines you report (the
 reviewer read 74 files and 1439 tests passed, 5 skipped, at `a5ee2dc8`); count the `it(` blocks
 the round adds from the diff and account for the difference. Then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f288-r5-mutations.py` takes a worktree path, and
 for each mutation edits the named file INSIDE that worktree (asserting its FROM text occurs exactly
 once), runs the named tests, restores the bytes, and prints per mutation its label, exit code,
 failed count and failing test names, with an unmutated control first and last for each runner,
 `restored byte-identical: True` per file and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Python mutations run
 `python3 -B -m pytest -q -p no:cacheprovider tests/ui_contracts/test_brain_stage_mount.py
 tests/ui_contracts/test_timeline_scrub_wiring.py` from the worktree's root after purging its
 `__pycache__` directories. TypeScript mutations run
 `/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vitest run --config <scratch config>` from
 `/home/decodeux/Repos/remedy/apps/ui`, where the scratch config under your own directory exports a
 PLAIN OBJECT with `root` the primary `apps/ui`, `cacheDir` under `.remedy-wt/`, and
 `test: { environment: "node", include: [<the worktree's promptNodes.test.ts, brainView.test.ts and
 buildForceBrainModel.test.ts by absolute path>] }`; before the mutations, prove the route reads the
 worktree's sources by one mutation that cannot pass whatever the tests import, and report it. The
 mutations:
  m1 `withPromptNodes` births an item whose task the model lacks, under the core;
  m2 a synapse's state is always `pass`;
  m3 a synapse's parent is the core instead of its task;
  m4 `withPromptNodes` answers a new object when it appends nothing;
  m5 a repeated item is born twice;
  m6 `selectionIdOf` answers the parent task id for a synapse;
  m7 `selectedPromptNodeId` answers `null` for a matching id;
  m8 a synapse is laid out at `BRAIN_RUN_RADIUS`;
  m9 the stage composes the prompts onto `model` instead of `liveModel`;
  m10 ForceBrainGraph's click calls `selectionTaskIdOf(n)` again.
 Run it in `git worktree add --detach .remedy-wt/f288-r5-mut <C5>` and report its whole output.
 EVERY mutation must be red; a green one is reported as green, never papered over: you then say
 whether a test can see the behaviour, add the test that catches it if one can, and re-run the
 tool. Then remove the worktree, `git worktree prune`, and report `git worktree list | wc -l`; and
 `git status --porcelain` must be empty, a stray `.vite/` included.

G6 TREE AND PUSH — after C6: `git status --porcelain` empty; `git log --oneline a5ee2dc8..HEAD`;
 `git worktree list | wc -l` and `git stash list | wc -l`, equal to your step 4 readings; the push's
 real outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected (none is expected for C3 to C5), every gate's real output and exit code, the authored-text
proofs, the item-status table AGENTS.md requires (one row per commit and per gate), the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F288, round 5, and
says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
5, then the second half of T003 — the keyboard's parallel list of the live picture's prompt nodes
and a rendered proof in a headless browser. State the open-findings count, 0, and the
operator-questions count, 0.
