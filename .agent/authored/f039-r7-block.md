STEP F039 R7 — BOOK ROUND 6 WITH R-1101's RESOLUTION, REPAIR R-1102, AND LAND T003's DATA: the story payload the export writes and the reader the player reads it with

GOAL
Round 6 is reviewed PASS at `622ec045`. Book its gate entry and R-1101's resolution, register finding
R-1102 and record DECISION F039 D7 with the plan. Repair R-1102: the cockpit's dashboard mapping
replaces every minted task id with `task-<n>`, so a finished `remedy do` job never reaches Finalized
on the phase bar and its story never reaches The finish. Then land the data half of T003: a NEW
module `packages/orchestration/story_export.py` building one job's story payload from the cockpit's
own builders, and a NEW module `apps/ui/src/components/story/storyExport.ts` reading it back, with a
guard holding the payload's schema to one string in both languages. No command, page, route,
configuration key or event name changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
code, its tests and the mutation tool yourself against S1 to S4. Only the `.agent/` records travel
as payloads. Read R-1102 and DECISION F039 D7 in the records diff before you write code. Before you
write anything, read whole: `normalizeDashboardPayload` in `apps/ui/src/api/remedyApi.ts` and the
test file beside it; `scrubUiText` in `apps/ui/src/copy/humanCopy.ts`; `dashboardBrainSeeds` in
`apps/ui/src/components/graph/brainView.ts` and `brainView.test.ts`; `_build_dashboard`,
`_load_events`, `_safe_event_summary` and `_build_events_since_json` in
`packages/orchestration/ui_server.py`; `ownership_view` in `packages/orchestration/ownership_phrases.py`;
`feedRowOf` in `apps/ui/src/api/feedRow.ts`; `decodeOwnershipView` in `apps/ui/src/api/ownership.ts`;
`BRAIN_DEMO_FRAMES` in `apps/ui/src/components/graph/brainDemoRecording.ts`; `ALLOWED_UNWIRED` in
`tests/test_no_orphan_modules.py`; `tests/ui_server/test_budget_final_section.py` for how a test
patches `_load_events`; and your round 4 tool `.agent/authored/f039-r4-mutations.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r7-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r7/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r7-dry/`, `.remedy-wt/f039-r7-sim/`, `.remedy-wt/f039-review/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f039-r7-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the file.
Set environment variables for a child process inside a Python script. Never run npm or npx. Never
`git reset` a commit: a commit made out of order is declared, not rewritten.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f039-story-replay-mode`, and `git log --oneline -1` must read `622ec0451`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r7/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r7-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 30 | 1074 | a88fd3959b4387bf4984f6f060982c8e22e9022cf57c86d0e38c506921559667 |
| records.diff | 61 | 11701 | ef131c1b4fd720e0622122eba37122a2793c1dbcf9de58cc625088425ee47968 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `622ec045`. It appends to `.agent/live_review.md`
round 6's gate entry, R-1101's `Done:` paragraph and the registration of R-1102, and to
`.agent/decisions.md` DECISION F039 D7.

THE SPECIFICATION. No `except Exception` and no `# noqa: BLE001`; the TypeScript is pure.
S1 R-1102. In `normalizeDashboardPayload`, a task item's `id` becomes the item's own `id` as a
   string, falling back to `task-<idx>` as today only when the item carries none, never passed
   through `scrubUiText`, under a two-line comment naming R-1102 and saying the id is an identifier every seed, focus rule
   and door compares with a raw task id, never text a person reads; labels are scrubbed as before
   and nothing else in the file changes. `apps/ui/src/api/remedyApi.test.ts` gains one test: a
   dashboard whose task has the id `0123456789abcdef` and the title `abcdef012345` maps to the id
   `0123456789abcdef` while its label is not `abcdef012345`. `brainView.test.ts` gains one
   `describe` naming R-1102: tasks from `normalizeDashboardPayload` of one task `0123456789abcdef`
   keep that id; `dashboardBrainSeeds` seeds it under that id, and seeds it `paused`, `vetoed` and
   with `specVersion` 2 when those lists and that map name it; and `readPhases` over its seeds and
   the rows `task_run_started` at 0, a passing `task_round_completed` at 1 and a passing
   `task_run_completed` at 2 of that task reads `finalized`. In C3, append to
   `.agent/live_review.md` one blank line and one line beginning `Landed: R-1102 — ` saying in one
   sentence what changed; it names no commit. Never write a `Done:` line.
S2 THE PAYLOAD, a NEW FILE at `packages/orchestration/story_export.py`, docstring naming F039 T003 and
   DECISION F039 D7 and saying Remedy deliberately exports nothing the cockpit's own routes do not
   already serve. `STORY_EXPORT_SCHEMA = "remedy.story.v1"`; `STORY_DASHBOARD_SECTIONS = ("tasks",
   "live", "story")`; and `build_story_payload(job) -> dict[str, Any]`, importing inside the function
   `ownership_view` and, from `ui_server`, `_build_dashboard`, `_load_events` and
   `_safe_event_summary`, and answering `{"schema": STORY_EXPORT_SCHEMA, "job_id": str(job.job_id),
   "dashboard": <those three sections of _build_dashboard(job)>, "frames": [{"seq": seq, "event":
   _safe_event_summary(seq, event)} for every event of _load_events(job), seq counted from 0],
   "ownership": ownership_view(job)}`. `ALLOWED_UNWIRED` gains, before the `scripts/` entries,
   `("packages/orchestration/story_export.py", "F039's story export data; the export command wires
   it in a later round (DECISION F039 D7) and removes this line")`, split as its neighbours are.
S3 THE READER, a NEW FILE at `apps/ui/src/components/story/storyExport.ts`, header naming T5_F039.md
   T003 and DECISION F039 D7 and saying Remedy deliberately refuses another schema rather than guess
   at its shape. `export const STORY_EXPORT_SCHEMA = "remedy.story.v1";` alone on its line;
   `STORY_EXPORT_UNREADABLE_LINE = "This story's data could not be read."`;
   `storyExportVersionLine(schema)` answering
   `This story was written by a version of Remedy this player does not read (<schema>).`;
   `interface StoryExport { dashboard: RemedyDashboard; rows: FeedRow[]; ownership: OwnershipView |
   null }`; and `decodeStoryExport(raw: unknown)` answering `{ ok: true, story }` or
   `{ ok: false, message }`, never throwing: not a plain object → the unreadable line; a string
   `schema` other than the constant → the version line for it; a missing or non-string schema, a
   `job_id` that is not a string, a `dashboard` that is not a plain object, or `frames` that is not an
   array → the unreadable line; any frame that is not a plain object with a number `seq` → the
   unreadable line; else `dashboard` is `normalizeDashboardPayload(job_id, dashboard)`, `rows` each
   frame through `feedRowOf(frame, 0)` in order, and `ownership` `decodeOwnershipView(ownership)`.
S4 THE TESTS. A NEW FILE at `tests/orchestration/test_story_export.py`, patching `_load_events` of
   `ui_server` to three events — a `task_run_started` naming `t1` with `metadata.attempt_id`, a
   `budget.tick` whose metadata holds `spent_usd` 0.5 and `api_key` `sk-secret`, and a passing
   `task_run_completed` of `t1`: the payload's keys are exactly the five; its schema and job id; its
   dashboard equals the three sections of `_build_dashboard` of the same job; its frames equal
   `_safe_event_summary(i, event)` for each with seqs 0, 1 and 2; its ownership's schema is
   `remedy.ownership.v1`; `sk-secret` and `api_key` occur nowhere in its `repr`; and the TypeScript
   constant, read from `storyExport.ts`, equals `STORY_EXPORT_SCHEMA`. A NEW FILE at
   `apps/ui/src/components/story/storyExport.test.ts`, HAND-DERIVED: a payload of
   `BRAIN_DEMO_FRAMES`, the demo job id, the demo's two tasks by id and title with status
   `completed`, live `{running: false}`, story `{step_ms: 300, chapter_pause_ms: 900}` and an empty
   ownership view reads `ok` with rows equal to `brainDemoRows()`, the job id, the two task ids and
   titles, live not running, the story section and the decoded ownership view; `remedy.story.v2` is
   refused with its version line; `null`, `[]`, a string and payloads with no schema, a number job id,
   an array dashboard, an object for frames and a frame with no seq each read the unreadable line;
   and an unreadable ownership view reads `ok` with ownership `null`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6 and C7, in this order.
C1a — `.agent/authored/f039-r7-block.md` := this block and `.agent/authored/f039-r7-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F039 R7 C1a: copy round 7 block and plan into
  .agent/authored/`. Its insertions are this block's line count plus 30; STOP rather than
  commit at 500 or more.
C1b — `.agent/authored/f039-r7-records.diff` := records.diff. Subject: `F039 R7 C1b: copy round 7
  records diff into .agent/authored/`. Expected insertions: 61.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md. Subject: `F039 R7 C2: book
  round 6 and R-1101, register R-1102, record D7`. Expected by `git show --numstat`:
  39/0 decisions.md, 6/0 live_review.md, 9/8 plan.md.
C3 — S1. Subject: `F039 R7 C3: keep a task's own id in the dashboard mapping (R-1102)`.
C4 — S2 with `tests/orchestration/test_story_export.py`. Subject: `F039 R7 C4: build a job's story
  payload from the cockpit's own builders`.
C5 — S3 with `storyExport.test.ts`. Subject: `F039 R7 C5: read an exported story back, refusing
  another schema`.
C6 — your mutation tool as `.agent/authored/f039-r7-mutations.py`. Subject: `F039 R7 C6: add the
  mutation tool for R-1102 and the story payload`.
C7 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F039 R7 C7:
  rewrite handoff for round 7`. Then `git push origin feature/f039-story-replay-mode` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f039-r7-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `apps/ui/src/api/remedyApi.ts`,
   `apps/ui/src/api/remedyApi.test.ts`, `apps/ui/src/components/graph/brainView.test.ts`,
   `packages/orchestration/story_export.py`, `tests/test_no_orphan_modules.py`,
   `tests/orchestration/test_story_export.py`, the two new files under
   `apps/ui/src/components/story/` and `.agent/handoff.md`. Report the list
   `git diff --name-only 622ec0451` measures after C7. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C7, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`, no `git reset`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree listed at
   your step 4, and every stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed as
   that gate's last action, and `git worktree list | wc -l` is reported afterwards.
7. DO NOT run the full suite: it belongs to F039's closure (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table; then compare each `.agent/authored/f039-r7-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f039-r7/block.md`), read back with `git show
 <commit>:<path>` from the commit that added it. One reading each.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2437905 | 567b16b449ad759474723ef38a0a888e99a459c5aaa5819b8385f8651ee10edb |
 | .agent/live_review.md | 352058 | c2098229bc892b0572ac38cac005842ab10020f811220e583fe3776a0976235f |
 | .agent/plan.md | 1074 | a88fd3959b4387bf4984f6f060982c8e22e9022cf57c86d0e38c506921559667 |
 Also: `open_finding_ids` and `latest_gate_verdict` from `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2, which the reviewer read as `['R-1102']` and `PASS`; `git diff --name-only
 <C1b> <C2>`, which must name exactly the paths of the table; and at C3, the ledger at C2 is a
 byte-exact prefix of the ledger at C3 and what C3 adds to it is exactly "\n" plus one line
 beginning `Landed: R-1102 — ` and ending in "\n".

G3 THE CODE — `python3 -m ruff check packages/orchestration/story_export.py
 tests/orchestration/test_story_export.py tests/test_no_orphan_modules.py
 .agent/authored/f039-r7-mutations.py` at C6, with its real exit code. Then report, quoted from the
 commits, the id line of S1 with its comment, the whole of `story_export.py` and of
 `decodeStoryExport`.

G4 THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_story_export.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C1a to C2 of
 this round and the reviewer's own version of C3 to C5, and read `2267 passed, 10 skipped` at real exit code
 0. Every skip of that run which names `node_modules`, `dist` or vitest is a toolchain node a fresh
 worktree lacks, and in the primary checkout each must PASS rather than skip; the vitest node runs
 the whole UI unit suite, the new and grown test files with it. Report every `SKIPPED` line and the
 node count of `tests/orchestration/test_story_export.py`. Then
 `python3 -m apps.cli.main integrity check --json`: five checks `pass` and `high_blockers_open`
 `fail` with the message `1 open blocker/high: R-1102`, at `fail_count` 1 and exit code 1, because
 R-1102 stays open until the reviewer resolves it. Any other reading is red.

G5 THE RED PROOFS — your tool `.agent/authored/f039-r7-mutations.py`, following your round 4 tool's
 route, runs vitest over the WORKTREE's `storyExport.test.ts`, `brainView.test.ts` and
 `remedyApi.test.ts`, and `pytest` over `tests/orchestration/test_story_export.py`, printing one line
 per mutation with each runner's exit code and failed count, controls first and last,
 `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  m1 the task's id goes through `scrubUiText` again, R-1102's own proof;
  m2 the frames' seqs are counted from 1;
  m3 each frame carries the raw event instead of `_safe_event_summary`'s envelope;
  m4 `STORY_DASHBOARD_SECTIONS` gains `metrics`;
  m5 `decodeStoryExport` no longer refuses another schema by name;
  m6 a frame is taken as a row without `feedRowOf`;
  m7 the ownership view is taken without `decodeOwnershipView`;
  m8 the TypeScript constant reads `remedy.story.v2`;
  m9 a frame with no number `seq` is accepted.
 Run it on `git worktree add --detach .remedy-wt/f039-r7-mut <C6>` and report its whole output.
 EVERY mutation must be red in at least one runner; a green one is reported as green, and you then
 add the test that catches it before C7 and re-run. Then remove the worktree, `git worktree prune`,
 and report `git worktree list | wc -l` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C7 to C1a and `622ec0451` in order (more lines if a
 commit was split); `git worktree list | wc -l`, equal to your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must
 be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3 to C6 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 1 of feature F039, round 7, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 7
with the resolution of R-1102, then T003 continued: the story player as a second page of the UI
build and `remedy job story <id> --export <file>` with its size budget. State the open-findings
count, 1 (R-1102, High, landed and awaiting review), and the operator-questions count, 1.
