STEP F025 R6 — BOOK ROUND 5, THEN THE REST OF THE PAUSE ON THE PAGE: THE BANNER, THE NOWCARD'S "PAUSED BY YOU", AND THE PAUSE AND RESUME BUTTONS

GOAL
Round 5 PASSED; the payload `ledger.md` books that verdict and resolves R-1051 and R-1052. Then land
DECISION F025 D4 — the payload `d4.md`, read it whole before writing code: a request module that
reads the door's answer, a pure pause view, the pause banner in the graph's chrome, the NowCard's
"Paused by you", and the pause and resume buttons for the job and for a task.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, write the handback. You never
issue a verdict, never merge, and never write a `Done:` line. THE PRODUCTION CHANGE IS SPECIFIED,
NOT SLICED: you write the code and tests against U1 to U7. Read first, in `apps/ui/src/`:
`api/steeringSend.ts` with its test (the pattern U1 follows), `api/decisionSubmit.ts`,
`api/decisionAnswer.ts` (`jobCommandsPath`, `isUsableCommandNonce`), `api/decisionOutcome.ts`,
`api/types.ts` (`RemedyPause`), `components/panels/ChatInput.tsx`, `AgentNowCard.tsx`,
`RightLivePanel.tsx` with `RightLivePanel.module.css`, `components/detail/DetailPopover.tsx`,
`components/graph/BrainGraphStage.tsx` with its `.module.css`, `components/shell/RemedyShell.tsx`,
and `cockpitLogic.ts`; in Python, `pause_job_command` and `unpause_job_command` in
`packages/orchestration/pause_control.py` (the answer words), the door's `job.pause` clause in
`packages/orchestration/ui_server.py`, and `tests/ui_contracts/test_steering_send_contract.py`
(the pattern T3 follows); `docs/ui/design_reference/component_spec.md` and `assumption_log.md`;
and `.agent/authored/f025-r5-mutations.py`, whose two runner routes you reuse.

THE DIRECTORIES
  `.remedy-wt/f025-r6/`          READ-ONLY. This block, its payloads and the reviewer's scripts.
  `.remedy-wt/f025-r6-worker/`   YOURS for logs and scripts; create it if absent. Both gitignored.

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
   `git log --oneline -1` must read `0cd5e9f2`.
3. Measure this block's line count and sha256 (`.remedy-wt/f025-r6/block.md`) and compare both
   with your delegation message's readings; stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f025-r6/`, lines = newline count; verify each BEFORE use:
| file | lines | bytes | sha256 |
|---|---|---|---|
| d4.md | 45 | 3967 | 74d5ec7e57ab9e87080710334bc4986e63757884cf4b27c444ab547dba33b405 |
| ledger.md | 6 | 4352 | 400448b2b230e3ab26cb250caf3f1dec26aea4e3215a998d4f17cd04ced55af3 |
| plan.md | 30 | 1048 | 364b06f5ea05dea385b00a1560f6d9b925af08d457e4106e82751dd1af8f8718 |
`ledger.md` is appended to `.agent/live_review.md` and `d4.md` to `.agent/decisions.md` (each
starts with its own blank line); `plan.md` REWRITES `.agent/plan.md`.

THE SPECIFICATION
U1 THE SEND, NEW `apps/ui/src/api/pauseSend.ts`, built as `steeringSend.ts` is (pure builder, pure
   mapping, one flow with injectable `mintNonce`, `submit` and `deadline`, the same 20-second
   deadline). The builder takes the target, the command (`job.pause` or `job.unpause`), an optional
   task id and a nonce, and returns `null` for an empty job id, token or task id given as `""`, or
   an unusable nonce; otherwise the steering headers and a body of `command`, `client_nonce` and
   `args` — `{ task }` for a task, `{}` for the job. Its OWN submit, with an injected send whose
   reply offers `ok`, `status` and `json()`, answers `{ outcome, status, body }`: `body` is the
   parsed object, or `null` when it is not an object or fails to parse; it never throws or retries.
   The mapping gives one `{ tone, sentence }` per answer: on 200 by the body's `outcome` —
   `requested` "Pause requested. The job stops before its next step; the step that is running
   finishes first.", `paused` "This task is paused. It will not start until you resume it, and the
   rest of the job keeps going.", `released` "This task is released. The job picks it up at its
   next safe point.", `withdrawn` "The pause was taken back before the job reached it.", `parked`
   "This job is paused and saved. To continue it, run: " followed by the body's `next`, `not_paused`
   "Nothing was paused, so nothing changed.", anything else "The job answered, but not in a way this
   page understands."; on a refusal by status as `describeChatSendResult` maps them, with 409 "This
   job has ended, so it cannot be paused or resumed." and the other sentences about a pause rather
   than a message; unreachable as steering's.
U2 THE VIEW, NEW `apps/ui/src/api/pauseView.ts`, pure functions of a `RemedyDashboard`:
   `PAUSE_OWNER_SOURCES = ["cli", "ui"]`; parked is `pause.record` non-empty; "by you" is a
   `record.source` in that list. `pauseBanner` answers `null` or `{ badge, text, command, tone }`,
   first match wins: `error` non-empty → badge "PAUSE", text "The pause state could not be read: "
   plus the error, tone warn; parked → "PAUSED", "Paused by you. Nothing runs until you resume it."
   (or "Paused. Nothing runs until it is resumed." when not by you), `command` `remedy job run `
   plus the job id; `requested` → "PAUSING", "Pause requested. The job stops before its next
   step."; paused tasks → "PAUSED", "1 task is paused by you. The rest of the job keeps going." or
   "<n> tasks are paused by you. The rest of the job keeps going."; else `null`. `command` is `""`
   except when parked. `nowCardPause` answers `{ status: "Paused", detail }` with detail "Paused by
   you" — or "Paused" when parked and not by you — when the job is parked, or when it is not
   running and has paused tasks; else `null`. `jobPauseAction` answers `resume` when parked,
   `take_back` when requested, `pause` while `live.running`, else `null`; `taskPauseAction(dashboard,
   taskId, taskState)` answers `resume` when the id is in `pausedTaskIds`, `pause` when the state is
   not `done`, else `null`. Each action has its label: "Pause job", "Take back pause", "Resume",
   "Pause task", "Resume task".
U3 THE CONTROL, NEW `apps/ui/src/components/panels/PauseControl.tsx`: given the target, a scope
   (`job`, or a task id), and an action from U2, it renders nothing for `null`; otherwise one
   `type="button"` labelled by U2, disabled while a send is in flight, which sends `job.pause` for
   `pause` and `job.unpause` for `take_back`, `resume` and a task's `resume` through U1's flow, and
   the sentence below it in `aria-live="polite"`, toned as `ChatInput.tsx` tones its outcome. It
   holds only in-flight and the last sentence; it calls no `fetch`.
U4 THE MOUNTS: `RightLivePanel.tsx` renders the job's control on the line directly after
   `<AgentNowCard dashboard={dashboard} recent={recent} />`, which stays byte-identical; the
   popover gains an optional `serverToken` and renders the selected task's control only when it has
   one, and `RemedyShell.tsx`'s `<DetailPopover` gains `serverToken={serverToken}` beside
   `onOpenDiff`; `BrainGraphStage.tsx` renders the banner AFTER the scrub banner's closing `)}` as a
   `role="status"` element with `data-ui="pause-banner"`, the badge, the text, and the command in
   a `<code>` when present. `AgentNowCard.tsx` shows `nowCardPause`'s status and detail when it is
   not `null`, keeping `liveAction ? liveAction.line : detail` for the other case;
   `deriveAgentStatus` is unchanged.
U5 THE STYLES: new classes only, in `BrainGraphStage.module.css` (the banner, patterned on the scrub
   banner, its badge on `--remedy-orange-400`) and `RightLivePanel.module.css` (the control); every
   colour a `var(--remedy-...)` token already defined under `apps/ui/src`. No raw colour anywhere.
U6 THE RECORD: `docs/ui/design_reference/assumption_log.md` gains one row, last, in its seven-column
   shape, citing DECISION F025 D4 — the reference names no pause banner and no pause button.
U7 THE GUARD, T3 below.

THE TESTS
T1 `apps/ui/src/api/pauseSend.test.ts`: the builder's two scopes and each `null` case; the submit's
   body read, a body that fails to parse, a send that rejects; every sentence of the mapping, the
   `parked` sentence naming `next`; the flow's deadline answering unreachable.
T2 `apps/ui/src/api/pauseView.test.ts`: each banner case, the first-match order (a parked job with a
   pending request shows parked; an error hides the rest), "by you" true only for `cli` and `ui`,
   the singular and plural task text; `nowCardPause`'s three answers; every action case.
T3 NEW `tests/ui_contracts/test_pause_controls_contract.py`: `PAUSE_OWNER_SOURCES` equals the set of
   the `--source` default of `job.pause` in `apps/cli/command_catalog.py` and
   `COMMAND_EFFECT_SOURCE` in `ui_server.py`; the two command ids in `pauseSend.ts` equal
   `JOB_PAUSE_COMMAND_ID` and `JOB_UNPAUSE_COMMAND_ID`; `PauseControl.tsx`, `RightLivePanel.tsx`,
   `DetailPopover.tsx`, `BrainGraphStage.tsx` and `AgentNowCard.tsx` hold no `fetch(`; the panel's
   `<PauseControl` follows the NowCard's line; the popover's control is passed the task's id; the
   stage renders `pauseBanner(` output under `data-ui="pause-banner"`.

BUNDLE — commits in this order; split any that would reach 500 insertions and say so.
C1a COPIES: `.agent/authored/f025-r6-block.md` := this block and each payload as
    `.agent/authored/f025-r6-<name>`. Subject `F025 R6 C1a: copy round 6 block and payloads`.
    Expected by `git show --numstat`: this block's line count plus 81, that is the block copy's own lines and 45/0 `.agent/authored/f025-r6-d4.md`, 6/0 `.agent/authored/f025-r6-ledger.md`, 30/0 `.agent/authored/f025-r6-plan.md`.
C1b RECORDS, one commit: the ledger and decisions appends and the plan rewrite. Subject
    `F025 R6 C1b: book round 5, resolve R-1051 and R-1052, record D4`. Expected: 45/0 `.agent/decisions.md`, 6/0 `.agent/live_review.md`, 8/12 `.agent/plan.md`.
C2 U1 with T1. C3 U2 with T2. C4 U3 to U5. C5 U6 and T3. C6 THE MUTATION TOOL,
    `.agent/authored/f025-r6-mutations.py`. Subjects are yours, each beginning `F025 R6 C<n>: `.
C7 THE HANDBACK, `.agent/handoff.md`. Subject `F025 R6 C7: rewrite handoff for round 6`. Then
    `git push origin feature/f025-pause-resume`.

CONSTRAINTS
1. Never edit or retype a payload. Append by python, bytes to bytes.
2. Every commit under 500 insertions by `git show --numstat`. No `# noqa: BLE001` is added, and no
   raw colour is added to any `.css`, `.ts` or `.tsx` file.
3. The round's tracked path set is: the `.agent/authored/f025-r6-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/handoff.md`, the new
   files U1 to U3 and T1 to T3 name, `AgentNowCard.tsx`, `RightLivePanel.tsx`,
   `RightLivePanel.module.css`, `DetailPopover.tsx`, `BrainGraphStage.tsx`,
   `BrainGraphStage.module.css`, `RemedyShell.tsx`, `assumption_log.md`, and any EXISTING test
   whose only edit widens a set it pins to the new files — each named in the handback with what it
   widened. Never weaken an assertion or delete a test. Do NOT touch `packages/`, `apps/cli/`,
   `cockpitLogic.ts`, `decisionSubmit.ts`, `steeringSend.ts`, `tokens.css` in either place,
   `graph_spec.md`, or `docs/roadmap/`.
4. These existing guards bind the files you edit, read each before editing: in
   `tests/ui_contracts/`, `test_brain_stream_ring.py` (the NowCard line and text it pins),
   `test_timeline_scrub_wiring.py` (the scrub banner slice; no timers in the panel, shell or stage),
   `test_run_detail_wiring.py`, `test_diff_viewer_mount.py`, `test_digest_mount.py` (the shell's
   anchor counts), `test_main_layout_guard.py` (four components in `<main>`),
   `test_raw_colour_ratchet.py` (exact per-file counts), `test_design_drift.py` (every token
   resolves; "Idle" stays in `cockpitLogic.ts`), `test_ux_quality.py` (the popover's forbidden
   words, among them `rank` and `zone` as substrings), and `test_ui_lint.py`.
5. A red gate: STOP, commit and push what is verified, write the handoff under AGENTS.md "If
   Blocked". Nothing is merged; no `gh pr create`; no force-push; no `git stash`.
6. Leave every existing worktree alone; the one G5 adds is removed as that step's last action.
7. DO NOT run the full suite (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. G1 to G5 run
before C7 is written.
G1 TRANSPORT: each payload's measured lines, bytes and sha256 against the table; each
   `.agent/authored/f025-r6-*` payload copy byte-equal to its source by `git show <C1a>:<path>`
   (the block copy against `.remedy-wt/f025-r6/block.md`); at C1b the appended files equal
   their `0cd5e9f2` bytes plus their payloads and `.agent/plan.md` equals plan.md; and
   `open_finding_ids` over the ledger at C1b — the reviewer's simulation read ``['R-1008']``.
G2 THE CODE: `python3 -m ruff check` over every Python file C2 to C6 changed; `git diff --stat
   0cd5e9f2 <C6> -- packages apps/cli apps/ui/src/cockpitLogic.ts apps/ui/src/api/decisionSubmit.ts
   apps/ui/src/api/steeringSend.ts apps/ui/src/styles/tokens.css docs/ui/design_reference/tokens.css
   docs/ui/design_reference/graph_spec.md docs/roadmap` empty; and `git diff --name-only <C1b>
   <C6>`, every path inside constraint 3.
G3 THE TESTS NEAREST THE CHANGE, serially: `python3 -m pytest -q -p no:cacheprovider
   tests/ui_contracts/test_pause_controls_contract.py tests/ui_contracts/test_brain_stream_ring.py
   tests/ui_contracts/test_timeline_scrub_wiring.py tests/ui_contracts/test_run_detail_wiring.py
   tests/ui_contracts/test_diff_viewer_mount.py tests/ui_contracts/test_digest_mount.py
   tests/ui_contracts/test_main_layout_guard.py tests/ui_contracts/test_raw_colour_ratchet.py
   tests/ui_contracts/test_design_drift.py tests/ui_contracts/test_ux_quality.py
   tests/ui_contracts/test_ui_lint.py tests/ui_server/test_dashboard_contract.py
   tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py` — exit 0, with the tsc
   node in the dashboard contract, the eslint node and the vitest node PASSING, not skipped; report
   the summary line and every `SKIPPED` line.
G4 THE NEIGHBOURS: first `python3 -m pytest -q -p no:cacheprovider
   tests/ui_server/test_command_channel.py` alone, serially, so the UI bundle is rebuilt once
   before the parallel run; then `python3 .remedy-wt/f025-r6/run_sel.py /home/decodeux/Repos/remedy
   8` in the primary checkout at C6 — round 5's selection plus the golden path, with 8 xdist
   workers. At `0cd5e9f2` the reviewer read `9691 passed, 13 skipped in 196.28s (0:03:16)` (files 144 exit 0 wall 197 s). Report its output; re-run any failing node's
   file alone, serially, and report both readings. Then `python3 -m apps.cli.main integrity check
   --json`: six `pass`, `fail_count` 0.
G5 THE RED PROOFS: your tool takes a worktree path, edits the named file INSIDE that worktree
   (asserting each FROM occurs exactly once), and runs `python3 -B -m pytest -q -p no:cacheprovider`
   over T3 from the worktree root after purging `__pycache__` for a mutation T3 must catch, or
   vitest over T1 and T2 by the route `.agent/authored/f025-r5-mutations.py` uses for one they must.
   It restores, and prints per mutation its label, runner, exit code, failed count and failing test
   names, with an unmutated control of BOTH runners first and last, `restored byte-identical: True`
   per file, and a final `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Mutations:
    m1 the builder drops `task` from `args` [vitest];
    m2 the submit answers `body: null` for every reply [vitest];
    m3 a 409 maps to the generic refusal sentence [vitest];
    m4 "by you" accepts any source [vitest];
    m5 the banner checks `requested` before parked [vitest];
    m6 `jobPauseAction` answers `pause` whatever `live.running` reads [vitest];
    m7 `taskPauseAction` answers `pause` for a done task [vitest];
    m8 `PAUSE_OWNER_SOURCES` gains `"system"` [pytest];
    m9 the panel's `<PauseControl` mount is deleted [pytest];
    m10 the stage's pause banner is deleted [pytest].
   `git worktree add --detach .remedy-wt/f025-r6-mut <C6>`, run
   `python3 -B .agent/authored/f025-r6-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r6-mut`,
   report the whole output. EVERY mutation must be red; one that stays green is reported green, the
   catching test is added in a further commit before C7, and the tool re-run. Then
   `git worktree remove --force .remedy-wt/f025-r6-mut`, `git worktree prune`, `git worktree list`.
G6 AFTER C7 AND THE PUSH, in your final reply only: `git status --porcelain` empty, the local tip
   equal to `origin/feature/f025-pause-resume`, `git log --oneline -n 12`, the push's real outcome,
   and `gh pr list --state open --json number` EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the `git show --numstat` counts you measured (compared with
C1a's and C1b's expectations above), every gate's real output, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations — including
every existing test constraint 3 led you to widen — and the next action. Session section: SESSION 2
of feature F025, round 6, plus one sentence on how much context you had left. `## Next`: Phase 1
rule 1, the review of round 6, then T003's end-to-end. State the open-findings count as the script
reads it at C1b, and "Operator questions open: <the count of `### Q` headings in the file at C1b>".
