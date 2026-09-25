STEP F025 R5 — REPAIR R-1051 AND R-1052, THEN THE PAUSE ON THE PAGE: THE DASHBOARD'S `pause` AND THE GRAPH'S `paused` NODE STATE

GOAL
Round 4 PASSED with two findings against its own specification, which the payload `ledger.md`
registers: read both whole, their FIX clauses are this round's first spec. Persist them, repair
them, then land DECISION F025 D3 — the payload `d3.md`, read it whole before writing code: the
dashboard's `pause` object, and the node state `paused` from the reducer through its seed, its
treatment, its new `pause` mark and the design reference's two rows.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS SPECIFIED,
NOT SLICED: you write the code and tests against the FIX clauses and U1 to U7. Read first:
`packages/orchestration/pause_control.py` (the R4 effects), `_build_dashboard` in
`packages/orchestration/ui_server.py`, and in `apps/ui/src/`: `components/graph/brainOntology.ts`,
`brainReducer.ts`, `brainView.ts` (`dashboardBrainSeeds`, `BRAIN_FILTER_STATES`),
`renderers/nodeStates.ts`, `renderers/glyphPaths.ts`, `renderers/glyphConformance.ts`,
`runDetailModel.ts`, `api/types.ts` and `api/remedyApi.ts` (`normalizeDashboardPayload`), with the
tests that pin them; `docs/ui/design_reference/assets_spec.md` §4 and `assumption_log.md`; and
`.agent/authored/f024-r1-mutations.py`, whose route for running vitest against a worktree you reuse.

THE DIRECTORIES
  `.remedy-wt/f025-r5/`          READ-ONLY. This block, its payloads and the reviewer's scripts.
  `.remedy-wt/f025-r5-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`, and
multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <path>`, never `cd` your shell into a worktree.
Copy and hash with python (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write
such a script under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit ends with exactly this line:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop.
2. In the primary checkout `/home/decodeux/Repos/remedy`: report `pwd`; `git status --porcelain`
   must be empty, `git branch --show-current` must read `feature/f025-pause-resume`, and
   `git log --oneline -1` must read `db496696`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r5/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f025-r5/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| d3.md | 47 | 4039 | 84e4d79e839c373c26d6c4e1552789afa14b65394a342569b6e628d5a47230e7 |
| ledger.md | 6 | 6480 | 393efd0aae8dc5ad5867249528fc5d85c922639103bdc861f365881bc38294a2 |
| plan.md | 34 | 1236 | b8918a99b856da122f1e8fdce542d554bb64ff7f83f4cddfd5f4ee445b451174 |
| slip.txt | 1 | 342 | b606248040beff21fd81b78a8c1ca4726e7488c0a6b407f628533702d82274f1 |
`ledger.md` is appended to `.agent/live_review.md`, `d3.md` to `.agent/decisions.md` (each starts
with its own blank line), `slip.txt` to `.agent/prose_slips.md`; `plan.md` REWRITES `.agent/plan.md`.

THE SPECIFICATION FOR THE PAGE
U1 THE DASHBOARD. `_build_dashboard` adds `pause`: `record` (the job's pause record while its state
   is `paused`, else `{}`), `requested` (a pending job pause, `pause_control.pause_requested` is not
   None), `paused_task_ids` (the ids `pause_control.paused_tasks` names whose task is pending, in
   plan order), and `error` (`""`, or the text of a `PauseControlError` or `StopControlError` met
   while reading, in which case the other three keep their empty values). It never raises for them.
U2 THE CLIENT TYPE. `RemedyDashboard` gains `pause: { record, requested, pausedTaskIds, error }`,
   normalized by `normalizeDashboardPayload` so a payload without it reads as not paused.
U3 THE STATE. `NodeState` gains `"paused"`. Every `Record<NodeState, ...>` gains its key:
   `NODE_STATE_TREATMENTS` (legend name "Paused", placed after `planned`), `BINDING_STATE_MARKS`,
   and `runDetailModel.ts`'s state words ("Paused"); `BRAIN_FILTER_STATES` groups it with planned.
U4 THE TREATMENT, D3 clause (3): the planned node's fill, ink, line, size, ring and no halo, pulse
   or branch glow, plus the mark `pause`.
U5 THE MARK. `StateMark` gains `"pause"` and `STATE_MARK_PATHS` its geometry: two upright bars
   inside the status dot's box, x 17 to 23 and y 1.5 to 7.5, as a fill path of two rectangles with
   a visible gap between them; its paint is `--remedy-orange-400` outlined
   `--remedy-graph-node-ring`, both tokens already defined in both token sheets.
U6 THE REDUCER AND THE SEED, D3 clause (2): `task_paused`, `task_resumed`, `job_paused` and
   `job_resumed` get their cases in `applyBrainEvent` and leave `ignored`; replaying a seq stays a
   no-op; `dashboardBrainSeeds` seeds `pause.pausedTaskIds` as `paused`.
U7 THE RECORDS, D3 clause (4): `docs/ui/design_reference/assets_spec.md` §4's table gains the pause
   mark's row in its existing shape, and `docs/ui/design_reference/assumption_log.md` gains one row,
   last, in its seven-column shape, citing DECISION F025 D3.
Every `Record<NodeState>` that is complete by construction gains the key, and every existing vitest
that pins the state set (`nodeStates.test.ts`, `glyphConformance.test.ts`, `legendModel.test.ts`,
`glyphMatrix.test.ts`, `paintNode.test.ts`) is widened to the new state, never loosened; the only
state sharing a look stays `fail` with `blocked`.

THE TESTS
T1 For R-1051 and R-1052, in `tests/cli/test_job_pause.py`: a parked job given a new pause answers
   `withdrawn` and nothing stays pending; a job paused by the task cap answers `not_paused`; a
   `task_paused` write that fails once is written by the retry, exactly once; a `task_resumed` write
   that fails leaves the task paused, and the retry writes the event once and releases it.
T2 For U1, in `tests/ui_server/test_dashboard_contract.py` or a NEW FILE at
   `tests/ui_server/test_dashboard_pause.py`: each of `record`, `requested`, `paused_task_ids` (a
   done task's pause omitted, plan order kept) and `error` read from a real control root.
T3 For U2 to U6, vitest beside the modules: the reducer's four cases, the seed, the treatment and
   the mark, the normalization of a payload with and without `pause`.

BUNDLE — commits in this order; split any that would reach 500 insertions and say so.
C1a COPIES: `.agent/authored/f025-r5-block.md` := this block and each payload as
    `.agent/authored/f025-r5-<name>`. Subject `F025 R5 C1a: copy round 5 block and payloads`.
    Expected by `git show --numstat`: this block's line count plus 88, that is the block copy's own lines and 47/0 `.agent/authored/f025-r5-d3.md`, 6/0 `.agent/authored/f025-r5-ledger.md`, 34/0 `.agent/authored/f025-r5-plan.md`, 1/0 `.agent/authored/f025-r5-slip.txt`.
C1b RECORDS, one commit, the findings persisted FIRST: the three appends and the plan rewrite.
    Subject `F025 R5 C1b: book round 4, register R-1051 and R-1052, record D3`. Expected:
    47/0 `.agent/decisions.md`, 6/0 `.agent/live_review.md`, 13/12 `.agent/plan.md`, 1/0 `.agent/prose_slips.md`.
C2 R-1051's FIX with its tests. C3 R-1052's FIX with its tests. C4 U1 with T2. C5 U2 to U6 with
    their widened and new vitest. C6 U7. C7 THE MUTATION TOOL, `.agent/authored/f025-r5-mutations.py`.
    Subjects are yours, each beginning `F025 R5 C<n>: `.
C8 THE HANDBACK, `.agent/handoff.md`. Subject `F025 R5 C8: rewrite handoff for round 5`. Then
    `git push origin feature/f025-pause-resume`.

CONSTRAINTS
1. Never edit or retype a payload. Append by python, bytes to bytes.
2. Every commit under 500 insertions by `git show --numstat`. No `# noqa: BLE001` is added, and no
   raw colour is added to any `.css`, `.ts` or `.tsx` file.
3. The round's tracked path set is: the `.agent/authored/f025-r5-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `.agent/handoff.md`, `packages/orchestration/pause_control.py`,
   `packages/orchestration/ui_server.py`, `tests/cli/test_job_pause.py`, the dashboard test of T2,
   the `apps/ui/src/` modules U2 to U6 name with their `.test.ts` files, the two design-reference
   files U7 names, and any EXISTING test whose only edit widens a set it pins to the new state,
   mark or dashboard key — each named in the handback with what it widened. Never weaken an
   assertion or delete a test. Do NOT touch `safe_points.py`, `pingpong_job.py`, `pingpong_loop.py`,
   `long_run_executor.py`, `_safe_event_summary`, `tokens.css` in either place, `graph_spec.md`, or
   `docs/roadmap/`.
4. A red gate: STOP, commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no `git stash`.
5. Leave every existing worktree alone; the one G5 adds is removed as that step's last action.
6. DO NOT run the full suite (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C8 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r5-*` payload copy byte-equal to its source by `git show <C1a>:<path>`
   (the block copy against `.remedy-wt/f025-r5/block.md`); at C1b the three appended files equal
   their `db496696` bytes plus their payloads and `.agent/plan.md` equals plan.md; and
   `open_finding_ids` over the ledger at C1b — the reviewer's simulation read
   `['R-1008', 'R-1051', 'R-1052']`.
G2 THE CODE: `python3 -m ruff check` over every Python file C2 to C7 changed; `git diff --stat
   db496696 <C7> -- packages/orchestration/safe_points.py packages/orchestration/pingpong_job.py
   packages/orchestration/pingpong_loop.py packages/orchestration/long_run_executor.py
   apps/ui/src/styles/tokens.css docs/ui/design_reference/tokens.css
   docs/ui/design_reference/graph_spec.md` empty; the count of `noqa: BLE001` marks the range adds
   under `packages`, `apps` and `scripts`, which must be 0; and `git diff --name-only <C1b> <C7>`,
   every path inside constraint 3.
G3 THE TESTS NEAREST THE CHANGE, serially: `python3 -m pytest -q -p no:cacheprovider
   tests/cli/test_job_pause.py tests/ui_server/test_dashboard_contract.py
   tests/ui_contracts/test_node_glyph_tokens.py tests/ui_contracts/test_graph_legend_contract.py
   tests/ui_contracts/test_ui_lint.py tests/orchestration/test_test_runner.py` plus the T2 file if
   new — exit 0, with the tsc node in the dashboard contract, the eslint node and the vitest node
   PASSING, not skipped; report the summary line and every `SKIPPED` line.
G4 THE NEIGHBOURS: `python3 .remedy-wt/f025-r5/run_sel.py /home/decodeux/Repos/remedy 8` in the
   primary checkout at C7 — round 4's selection plus `tests/ui_contracts` whole, with 8 xdist
   workers. At `db496696` the reviewer read `9679 passed, 13 skipped` at exit 0. Report its output;
   re-run any failing node's file alone, serially, and report both readings (six nodes of
   `tests/cli/test_study_cmd.py` are known to fail in some orderings of this combined run and pass
   alone at `49624d5c` too). Then `python3 -m apps.cli.main integrity check --json`: six `pass`,
   `fail_count` 0.
G5 THE RED PROOFS: your tool takes a worktree path, edits the named file INSIDE that worktree
   (asserting each FROM occurs exactly once), and for a Python mutation runs `python3 -B -m pytest
   -q -p no:cacheprovider` over the T1 and T2 files from the worktree root after purging
   `__pycache__`; for a TypeScript mutation it runs vitest over the worktree's changed `.test.ts`
   files by the route `.agent/authored/f024-r1-mutations.py` uses. It restores, and prints per
   mutation its label, runner, exit code, failed count and failing test names, with an unmutated
   control of BOTH runners first and last, `restored byte-identical: True` per file, and a final
   `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Mutations:
    m1 `unpause_job_command` answers `parked` before it looks for a pending pause;
    m2 a job in state `paused` with an EMPTY pause record answers `parked`;
    m3 `task_paused` is written only when the call created the entry;
    m4 a release removes the entry before it writes `task_resumed`;
    m5 the dashboard's `paused_task_ids` keeps a paused task that is done;
    m6 the dashboard raises on a `PauseControlError` instead of reporting `error`;
    m7 the reducer ignores `task_paused`;
    m8 `task_resumed` leaves the node `paused`;
    m9 `job_paused` leaves in-progress run nodes `in_progress`;
    m10 the `paused` treatment drops the `pause` mark;
    m11 the seed ignores `pausedTaskIds`.
   `git worktree add --detach .remedy-wt/f025-r5-mut <C7>`, run
   `python3 -B .agent/authored/f025-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r5-mut`,
   report the whole output. EVERY mutation must be red; one that stays green is reported green, the
   catching test is added in a further commit before C8, and the tool re-run. Then
   `git worktree remove --force .remedy-wt/f025-r5-mut`, `git worktree prune`, `git worktree list`.
G6 AFTER C8 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f025-pause-resume`, `git log --oneline -n 14`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured (compared with
C1a's and C1b's expectations above), every gate's real output, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations — including
every file constraint 3 led you to widen — and the next action. Session section: SESSION 1 of
feature F025, round 5, plus one sentence on how much context you had left. `## Next`: Phase 1 rule
1, the review of round 5, then T003's second part — the door client, the stage banner, the
NowCard's line and the pause and resume buttons. State the open-findings count as the script reads
it at C1b, and "Operator questions open: <the count of `### Q` headings in the file at C1b>".
