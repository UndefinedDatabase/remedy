STEP F039 R9 — BOOK ROUND 8 AND CLOSE T003: the player build following `outDir`, the zero-network test from `file://` over the exported demo story, and the story guide

GOAL
Round 8 is reviewed PASS at `83afaaae`. Book its gate entry and record DECISION F039 D9 with the plan.
Then close T003 under D9: the player's second build follows the resolved `outDir` of the cockpit's
build; a NEW suite test runs the demo job on the fake providers, exports its story around a player
built into its own temporary folder, and drives headless Chrome over `--remote-debugging-pipe`,
requiring the demo's chapters, the keyboard, and no request but the file itself; and the story guide
lands with its two index rows and its assumption-log row. No product behaviour changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE CHANGE IS SPECIFIED, NOT SLICED, except the `.agent/` records
and the docs, which travel as payloads. Read DECISION F039 D9 in the records diff before you write
code. Before you write anything, read whole: `apps/ui/vite.config.ts`;
`tests/ui_contracts/test_story_player_contract.py`; `tests/ui_server/test_brain_demo_recording_live.py`
(its `CLI`, `ORDER`, `_env`, `_git_repo` and `_run` are yours to import); `packages/orchestration/story_export.py`;
`apps/ui/src/components/story/StoryPanel.tsx`, `storyPlayer.test.ts` beside it, and
`apps/ui/src/components/timeline/PhaseTimeline.tsx`; `tests/docs/test_named_source_paths.py`; and your
round 8 tool `.agent/authored/f039-r8-mutations.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r9-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r9/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r9-sim/`, `.remedy-wt/f039-r9-rec/`, `.remedy-wt/f039-review/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f039-r9-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `ln`, `sed`, process substitution, command substitution, `cd <dir> &&
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing, copying (`shutil.copyfile`) and linking (`os.symlink`); run a
program in another directory from a Python script with `subprocess.run(..., cwd=...)`. A heredoc
containing a dollar-brace is refused: write such a script to a file under your own directory and run
the file. Never run npm or npx. Never `git reset` a commit: a commit made out of order is declared,
not rewritten.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f039-story-replay-mode`, and `git log --oneline -1` must read `83afaaaea`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r9/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r9-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 28 | 979 | 4be4c6a6f0f0b9fa0bec72dce768df62d0c1964a18b68afae7642458f1fa58b5 |
| records.diff | 54 | 10484 | a5ebd425b534450f90a3118113c212788931b783894aaa814b45bbd74c3f3a08 |
| docs.diff | 128 | 11516 | d154d964eb1b646faad6d800b78b4dd4f4c009f78b3fbd4627c1da235dbfe382 |

`plan.md` is a REWRITE of `.agent/plan.md`. Both diffs go on with `git apply`; the reviewer generated
them with `git diff HEAD` from trees at `83afaaae`. `records.diff` appends to `.agent/live_review.md`
round 8's gate entry and to `.agent/decisions.md` DECISION F039 D9. `docs.diff` adds a NEW FILE at
`docs/guides/story-user-guide-v1.md`, which names the test of S2 by its path, adds its two rows to
`docs/README.md`, and appends one row to `docs/ui/design_reference/assumption_log.md`.

THE SPECIFICATION.
S1 THE BUILD FOLLOWS `outDir`. In `apps/ui/vite.config.ts`: `import path from "node:path";` as the
   first import; `export const STORY_PLAYER_OUT_DIR = "dist/story";` becomes
   `export const STORY_PLAYER_SUBDIR = "story";` under a two-line comment saying the player lands in
   that subdirectory of whatever `outDir` the cockpit's own build resolved, `dist/story` by default;
   `storyPlayerBuild()` gains `let outDir = "dist";` before its `return`, and the plugin gains, after
   `apply: "build",`, `configResolved(config) { outDir = path.resolve(config.root,
   config.build.outDir); },`; and the nested build's `outDir` becomes
   `path.join(outDir, STORY_PLAYER_SUBDIR)`. Nothing else in the file changes. In
   `tests/ui_contracts/test_story_player_contract.py` the literal `'STORY_PLAYER_OUT_DIR = "dist/story"'`
   is replaced by three: `'STORY_PLAYER_SUBDIR = "story"'`, `"configResolved(config)"` and
   `"path.join(outDir, STORY_PLAYER_SUBDIR)"`.
S2 THE TEST, a NEW FILE at `tests/ui_server/test_story_export_file_live.py`, docstring naming F039
   T003 and DECISIONS F039 D7, D8 and D9 and saying Remedy deliberately proves the export in a real
   browser rather than by reading the file. (a) A class `ChromePipe` driving headless Chrome over
   `--remote-debugging-pipe`: Chrome reads commands on file descriptor 3 and writes replies on 4, each
   message one JSON object ended by one NUL byte. Start it with `subprocess.Popen(["bash", "-c",
   'exec "$0" "$@" 3<&<r> 4>&<w>', chrome, *args], pass_fds=(<r>, <w>), stdout=DEVNULL,
   stderr=DEVNULL)`, where `<r>` and `<w>` are the child's ends of two `os.pipe()`s, closed in the
   parent afterwards, and `args` are `--headless=new`, `--remote-debugging-pipe`,
   `--user-data-dir=<tmp_path>/profile`, `--no-first-run`, `--no-default-browser-check`,
   `--window-size=1280,800` and `about:blank`. Reads wait with `select.select` against a deadline and
   raise on timeout or end of file; `send(method, params)` numbers each command, adds the session id
   once one is set, keeps every message that is not its reply as an event, and fails on an `error`
   reply; `close()` terminates Chrome, waits at most 10 seconds, kills it if needed, and closes both
   parent pipe ends. (b) A module-scoped fixture that skips ONLY when
   `apps/ui/node_modules/.bin/vite` is not a file, naming it, and otherwise runs `<vite> build
   --outDir <temp>/dist --emptyOutDir` with `cwd` `apps/ui` and `timeout=300`, requires exit 0 and
   exactly `story-player.css` and `story-player.js` in `<temp>/dist/story`, and answers that folder.
   (c) ONE test, skipping ONLY when neither `google-chrome` nor `chromium` is on the path: it runs
   `init`, `do ORDER --no-llm --plan-only --json` and `job run <id> --builder-provider fake
   --reviewer-provider fake --json` in a scratch repository exactly as the demo test does, sets
   `REMEDY_DATA_DIR` with `monkeypatch`, writes `export_story_html(load_job_plan(id),
   max_bytes=<the key's default>, player_dir=<the fixture's folder>)` to `<tmp_path>/story.html`, and
   over the pipe: `Target.createTarget` on `about:blank`, `Target.attachToTarget` with
   `flatten: true`, enable `Network`, `Page`, `Runtime` and `Log`, and navigate to the file's
   `file://` URL; then, polling for at most 15 seconds, the chapter buttons read exactly
   `["The build", "The review", "The finish"]`; the position reads `Chapter 3 of 3: The finish`; the
   `[role="slider"]` element's `aria-valuenow` reads `9`, and after focusing it and one
   `Input.dispatchKeyEvent` ArrowLeft (keyDown and keyUp, code 37) reads `8`; clicking the second
   chapter button makes the position read `Chapter 2 of 3: The review`; after blurring the active
   element, one Space (code 32, text " ") makes the panel's buttons hold `Pause`, and a second one
   `Play`, never `Close story`. After Chrome is closed: the URLs of every `Network.requestWillBeSent`
   event equal exactly `[<the file's URL>]`; no `Runtime.exceptionThrown` event and no
   `Log.entryAdded` of level `error` occurred; and the file's size is at most the budget.
S3 THE DOCS: `docs.diff`, applied as it is.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6 and C7, in this order.
C1a — `.agent/authored/f039-r9-block.md` := this block and `.agent/authored/f039-r9-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F039 R9 C1a: copy round 9 block and plan into
  .agent/authored/`. Its insertions are this block's line count plus 28; STOP rather than
  commit at 500 or more.
C1b — `.agent/authored/f039-r9-records.diff` := records.diff and `.agent/authored/f039-r9-docs.diff`
  := docs.diff. Subject: `F039 R9 C1b: copy round 9 records and docs diffs into .agent/authored/`.
  Expected insertions: 182.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md. Subject: `F039 R9 C2: book
  round 8, record D9`. Expected by `git show --numstat`: 36/0 decisions.md, 2/0 live_review.md,
  6/6 plan.md.
C3 — S1. Subject: `F039 R9 C3: build the story player into the resolved outDir`.
C4 — S2. Subject: `F039 R9 C4: prove the exported demo story plays from file with no request`.
C5 — `git apply` docs.diff. Subject: `F039 R9 C5: add the story guide, its index rows and its
  assumption-log row`. Expected: 2/0 docs/README.md, 93/0 the guide, 1/0 assumption_log.md.
C6 — your mutation tool as `.agent/authored/f039-r9-mutations.py`. Subject: `F039 R9 C6: add the
  mutation tool for the zero-network test`.
C7 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F039 R9 C7:
  rewrite handoff for round 9`. Then `git push origin feature/f039-story-replay-mode` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f039-r9-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `apps/ui/vite.config.ts`,
   `tests/ui_contracts/test_story_player_contract.py`, `tests/ui_server/test_story_export_file_live.py`,
   `docs/README.md`, `docs/guides/story-user-guide-v1.md`,
   `docs/ui/design_reference/assumption_log.md` and `.agent/handoff.md`. Report the list
   `git diff --name-only 83afaaaea` measures after C7. Touch nothing else.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C7, and the correction is declared. An
   EXISTING test that goes red is never edited to pass, apart from S1's ordered literal; report it
   and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`, no `git reset`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree listed at
   your step 4, and every stash alone. The worktree G5 adds goes under `.remedy-wt/`, gains the link
   G5 orders, is removed as that gate's last action with `git worktree remove --force` (the link is
   untracked), and `git worktree list | wc -l` is reported afterwards.
7. DO NOT run the full suite: it belongs to F039's closure (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a word
is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured against
 the PAYLOADS table; then compare each `.agent/authored/f039-r9-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f039-r9/block.md`), read back with `git show
 <commit>:<path>` from the commit that added it. One reading each.

G2 THE RECORDS AND THE DOCS — the sha256 of each file below, read with `git show <C2>:<path>` for the
 first three and `git show <C5>:<path>` for the rest, equals the reviewer's reading, printed from its
 records and simulation trees:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2444903 | a0101f2808fea563ddf7ff824dcf0e15224a902d87aa20e15703c6f9213f99fb |
 | .agent/live_review.md | 358804 | f78932248cfcd84484368be8056bef0db7aec4a01087fb94b03ad69caffdfc62 |
 | .agent/plan.md | 979 | 4be4c6a6f0f0b9fa0bec72dce768df62d0c1964a18b68afae7642458f1fa58b5 |
 | docs/README.md | 20901 | 7a4249bcfb957166ebf958ff6d35b5b7f804e8574738039b908efc01c5967498 |
 | docs/guides/story-user-guide-v1.md | 5325 | 6fdaf8fb8e8a247da02611453d3a692ddd238e59512fdb0966ce36577e0768df |
 | docs/ui/design_reference/assumption_log.md | 27315 | c0b849ed4f46d70a3b10615d1d9c068bebdfe7e79cf6fe0a5f0f9de162de66ab |
 Also: `open_finding_ids` and `latest_gate_verdict` from `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2, which the reviewer read as `[]` and `PASS`.

G3 THE CODE — `python3 -m ruff check tests/ui_server/test_story_export_file_live.py
 tests/ui_contracts/test_story_player_contract.py .agent/authored/f039-r9-mutations.py` at C6, with its
 real exit code. Then report, quoted from the commits, the plugin of S1 whole and `ChromePipe` whole.

G4 THE BUILD AND THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes. FIRST
 run `apps/ui/node_modules/.bin/vite build` with `cwd` `apps/ui` from a Python script, report its
 exit code and last 12 output lines, and list `apps/ui/dist/story/` with byte counts: exactly
 `story-player.css` and `story-player.js`, or red. THEN:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_story_export.py tests/cli/test_job_story.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in its simulation tree, which carries its own version of
 C3 to C5 and the primary's `node_modules`, and read `2249 passed, 5 skipped` at real exit code 0,
 the five being the D3 and D12 quarantine skips. Report every `SKIPPED` line; a skip naming
 `node_modules`, `dist`, vite, vitest or Chrome is red. Then run the new test alone with `-q -rA`
 and report its PASSED line and its duration. Then `python3 -m apps.cli.main integrity check --json`:
 all six checks `pass`, `fail_count` 0 and exit code 0.

G5 THE RED PROOFS — your tool `.agent/authored/f039-r9-mutations.py`, following your round 8 tool's
 route, links the worktree's `apps/ui/node_modules` to the primary's with `os.symlink` BEFORE its
 first control, and runs `pytest` under `python3 -B` over the worktree's
 `tests/ui_server/test_story_export_file_live.py` and `tests/ui_contracts/test_story_player_contract.py`,
 printing one line per mutation with the exit code and the passed, failed, errors and skipped
 counts (m1 goes red as an ERROR in the fixture's setup), controls first and last, `restored byte-identical: True` and `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY:
 <bool>`. Each control must read the live test PASSED, not skipped:
  m1 the plugin's `configResolved` sets nothing, so the player lands in `dist/story` whatever the
     `outDir`;
  m2 `render_story_html` drops its content security policy and writes
     `<img src="http://127.0.0.1:9/pixel.png" alt="">` before the root element;
  m3 `storyPlayerMain.tsx` reads the element `remedy-story` instead of `STORY_DATA_ELEMENT_ID`;
  m4 `StoryPanel`'s Space branch no longer toggles play;
  m5 `PhaseTimeline`'s slider no longer hands its keys to `scrub.onKey`.
 Run it on `git worktree add --detach .remedy-wt/f039-r9-mut <C6>` and report its whole output.
 EVERY mutation must be red; a green one is reported as green, and you then add the check that
 catches it before C7 and re-run. Then remove the worktree as constraint 6 orders, `git worktree
 prune`, and report `git worktree list | wc -l` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C7 to C1a and `83afaaaea` in order (more lines if a
 commit was split); `git worktree list | wc -l`, equal to your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must
 be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3, C4 and C6 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 2 of feature F039, round 9, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 9,
then the closure sequence of F039: the one full-suite run, the evidence package, the STATUS flip with
the ledger rotation, and the pull request. State the open-findings count, 0, and the
operator-questions count, 1.
