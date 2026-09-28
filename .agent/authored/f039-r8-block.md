STEP F039 R8 — BOOK ROUND 7 WITH R-1102's RESOLUTION, AND LAND T003's EXPORT: the story player built as one script and one style sheet, and `remedy job story <id> --export <file>` with its size budget

GOAL
Round 7 is reviewed PASS at `73102551`. Book its gate entry and R-1102's resolution and record
DECISION F039 D8 with the plan. Then land the export DECISION F039 D8 chooses: the UI build makes the
story player a second time as ONE script and ONE style sheet under `apps/ui/dist/story/`; a page entry
reads the story from the page's own inline JSON; and `remedy job story <id> --export <file>` writes one
HTML page inlining the player and the job's story payload, refusing a file larger than the new key
`story.export_max_bytes`. No event name, route or existing command changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you write the
code, its tests and the mutation tool yourself against S1 to S5. Only the `.agent/` records travel
as payloads. Read DECISION F039 D8 in the records diff before you write code. Before you write
anything, read whole: `apps/ui/vite.config.ts`, `apps/ui/src/main.tsx`, `apps/ui/tsconfig.json`;
`StoryPanel.tsx`, `storyExport.ts` and `storyExport.test.ts` under `apps/ui/src/components/story/`;
`PhaseTimeline.tsx` and `useTimelineScrub.ts` under `apps/ui/src/components/timeline/`;
`ReducedMotionProvider.tsx`; `tests/ui_contracts/test_story_panel_contract.py` and
`tests/ui_contracts/test_raw_colour_ratchet.py`; `packages/orchestration/story_export.py` and
`tests/orchestration/test_story_export.py`; the `story.*` keys in `packages/orchestration/config.py`
and `render_environment_guide`; `durable_write` in `packages/common/secure_fs.py`;
`apps/cli/commands/job_ownership_cmd.py`, `tests/cli/test_job_ownership.py`, the `job.ownership`
entry of `apps/cli/command_catalog.py` and `apps/cli/commands/__init__.py`; `tests/cli/test_exit_codes.py`
(its reader resolves only LITERAL exit codes and named module constants); `docs/guides/exit-codes.md`;
`tests/orchestration/import_reachability_allowlist.txt`; `ALLOWED_UNWIRED` in
`tests/test_no_orphan_modules.py`; `tests/docs/test_vocabulary.py`; and your round 7 tool
`.agent/authored/f039-r7-mutations.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f039-r8-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f039-r8/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f039-r8-sim/`, `.remedy-wt/f039-r8-rec/`, `.remedy-wt/f039-review/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f039-r8-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `ln`, `sed`, process substitution, command substitution, `cd <dir> &&
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`); run a program in another
directory from a Python script with `subprocess.run(..., cwd=...)`. A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the file.
Set environment variables for a child process inside a Python script. Never run npm or npx. Never
`git reset` a commit: a commit made out of order is declared, not rewritten.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f039-story-replay-mode`, and `git log --oneline -1` must read `73102551c`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f039-r8/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f039-r8-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 28 | 978 | 685af5cc9907ee97f112f755f9b5baeff065cf4b78f6e7b98f726409f228e952 |
| records.diff | 61 | 10360 | c478e03b0ac8180ce0cf5bb4745296c3ce96f101ea3d724554579aab8a23a7b9 |

`plan.md` is a REWRITE of `.agent/plan.md`. `records.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `73102551`. It appends to `.agent/live_review.md`
round 7's gate entry and R-1102's `Done:` paragraph, and to `.agent/decisions.md` DECISION F039 D8.

THE SPECIFICATION. No `except Exception` and no `# noqa: BLE001`. Every new CSS rule uses
`--remedy-*` tokens only, and no new `.tsx` carries a raw colour.
S1 THE BUILD. `apps/ui/vite.config.ts` gains, under a comment naming F039 T003 and DECISION F039 D8
   and saying a page opened from `file://` can load no chunk, `export const STORY_PLAYER_OUT_DIR =
   "dist/story";` and a plugin `storyPlayerBuild()` with `name: "remedy-story-player"`,
   `apply: "build"` and an async `closeBundle()` that awaits vite's own `build({...})` with
   `configFile: false`, `root: "."`, `base: "./"`, `logLevel: "warn"`, `plugins: [react()]` and
   `build: { outDir: STORY_PLAYER_OUT_DIR, emptyOutDir: true, sourcemap: false, copyPublicDir: false,
   cssCodeSplit: false, modulePreload: false, rollupOptions: { input: "src/storyPlayerMain.tsx",
   output: { entryFileNames: "story-player.js", assetFileNames: "story-player[extname]",
   inlineDynamicImports: true } } }`. The existing config gains the plugin after `react()`; nothing
   else in it changes. `apps/ui/package.json` is NOT touched.
S2 THE PAGE. (a) `storyExport.ts` gains `export const STORY_DATA_ELEMENT_ID = "remedy-story-data";`
   alone on its line, and `readEmbeddedStory(text: string | null)`, returning what
   `decodeStoryExport` returns: `null` → the unreadable line; text `JSON.parse` throws on → the
   unreadable line, inside a `try` whose `catch` binds nothing; else `decodeStoryExport` of the
   parsed value. (b) A NEW FILE at `apps/ui/src/components/story/StoryPlayerApp.tsx` exporting
   `StoryPlayerApp({ story }: { story: StoryExport })`, header naming F039 T003 and DECISION F039 D8
   and saying Remedy deliberately exports only this subset, not the cockpit: one
   `useTimelineScrub(story.dashboard.jobId, story.dashboard.tasks, story.rows)`, then
   `<main data-ui="story-player" className={styles.page}>` holding `<PhaseTimeline scrub={scrub} />`
   and, on one line, `<StoryPanel dashboard={story.dashboard} rows={story.rows}
   ownership={story.ownership} scrub={scrub} />` with no `onClose` and no heading. A NEW FILE at
   `apps/ui/src/components/story/StoryPlayerApp.module.css` gives `.page` `min-height: 100vh`, a flex column from the top,
   `padding: 24px`, `box-sizing: border-box`, `background: var(--remedy-bg)` and
   `color: var(--remedy-ink)`, under a comment naming DECISION F039 D8. (c) A NEW FILE at
   `apps/ui/src/storyPlayerMain.tsx`, header naming F039 T003 and DECISION F039 D8 and saying the
   story is read from the page and never from a route: it imports `./styles/globals.css`, decodes
   `readEmbeddedStory(document.getElementById(STORY_DATA_ELEMENT_ID)?.textContent ?? null)` once, and
   renders into `#root`, inside `React.StrictMode` and `ReducedMotionProvider`, either
   `<StoryPlayerApp story={decoded.story} />` or `<p data-ui="story-export-error">` holding the
   message. (d) In `StoryPanel.tsx`, `onClose` becomes `onClose?: () => void;`, Escape calls
   `onClose?.()`, and the Close button renders only as
   `{onClose && <button type="button" onClick={onClose}>Close story</button>}`; nothing else there
   changes, and the shell's own mount keeps passing `onClose`.
S3 THE FILE. `packages/orchestration/story_export.py`: the docstring sentence "`build_story_payload`
   is the ONE function here." is replaced by one saying `build_story_payload` builds the payload
   (DECISION F039 D7) and `export_story_html` writes it into ONE page around the built player
   (DECISION F039 D8), the next sentence then beginning "`build_story_payload` imports" and
   the rest of that paragraph kept; `__all__` gains the new public names; and it
   gains `STORY_DATA_ELEMENT_ID = "remedy-story-data"`; `STORY_PLAYER_DIR`, the repository's
   `apps/ui/dist/story` resolved from `__file__`; `class StoryExportError(Exception)` carrying
   `error` and `message`; `read_story_player(player_dir: Path | None = None) -> tuple[str, str]`,
   reading `STORY_PLAYER_DIR` AT CALL TIME when given `None`, raising `story_player_missing` when
   `story-player.js` or `story-player.css` is not a file (message naming
   `cd apps/ui && npm install && npm run build`) and `story_player_unsafe` when the script holds
   `</script` or the style `</style`, either case; `render_story_html(payload, script, style) -> str`,
   the page of D8 (3) — doctype, `lang="en"`, UTF-8, viewport, the meta
   `Content-Security-Policy` `default-src 'none'; script-src 'unsafe-inline'; style-src
   'unsafe-inline'; img-src data:`, the title `Remedy story of job <job_id>` through `html.escape`,
   `<style>` holding the style, `<div id="root" data-ui="remedy-story"></div>`, the payload as
   `json.dumps(payload, ensure_ascii=False, sort_keys=True)` with every `<` replaced by `<`
   inside `<script type="application/json" id="remedy-story-data">`, then
   `<script type="module">` holding the script; and `export_story_html(job, *, max_bytes: int,
   player_dir: Path | None = None) -> bytes`, the page of `build_story_payload(job)` as UTF-8,
   raising `story_too_large` when its length is GREATER than `max_bytes`, with a sentence naming both
   numbers, the key and that nothing was written. `packages/orchestration/config.py` gains, directly
   after `story.chapter_pause_ms`, `story.export_max_bytes` (`REMEDY_STORY_EXPORT_MAX_BYTES`, `int`,
   default `5_000_000`), described as the largest story file `remedy job story --export` writes
   (F039), a larger story refused whole, never cut; then `docs/guides/environment.md` :=
   `render_environment_guide()` of the edited registry.
S4 THE COMMAND, a NEW FILE at `apps/cli/commands/job_story_cmd.py` modelled on
   `job_ownership_cmd.py`, docstring naming F039 T003, DECISIONS F039 D7 and D8 and every exit code:
   `_cmd_job_story(job_id_str, export_path, *, json_output=False)` resolves the id; an unreadable job
   → `job_not_found` at `EXIT_NOT_READY` (3); reads `story.export_max_bytes` through `get_config()`;
   calls `export_story_html`; on `StoryExportError`, `story_player_missing` → `fail(...,
   exit_code=EXIT_NOT_READY, ...)` and every other code → `fail(...)` at its default 1, each a
   LITERAL call; writes with `durable_write(target, data, mode=0o644)`, an `OSError`
   → `story_write_failed` at 1 naming the path and `exc.strerror`; `--json` → `emit_ok(job_id=...,
   path=str(target), bytes=len(data), budget_bytes=budget)`; text → exactly
   `Wrote the story of job <id> to <path> (<n> bytes). Open it in any browser; it needs no network and no Remedy.`
   `COMMAND_HANDLERS` maps `"job.story"` from `args.job_id`, `args.export` and `args.json`.
   `apps/cli/commands/__init__.py` imports and loops over `job_story_cmd` after `job_steer_cmd`.
   `command_catalog.py` gains, directly after `job.ownership`, a banner comment naming F039 T003 and
   D7/D8 and `CommandEntry(command_id="job.story", group_id="job", subcommand="story",
   description=<below>, action_class="read_only", args=(_JOB_ID, ArgDef("--export", "The HTML file to
   write", required=True, is_option=True), _JSON_OPT), supports_json=True, related=("job.show",
   "job.ownership"), exit_codes=(0, 1, 2, 3))`, the description reading exactly `Write the story of a
   job under its mission as one HTML file that plays in any browser from the file itself, with no
   network and no Remedy: its chapters, narration and phase bar, read from the job's own records
   (F039).` (`tests/docs/test_vocabulary.py` requires "mission" beside "job"). Also:
   `docs/guides/exit-codes.md` gains a row for `remedy job story` and 3 after the ownership row; the
   allowlist gains `apps.cli.commands.job_story_cmd` after `apps.cli.commands.job_stop_cmd` and
   `packages.orchestration.story_export` after `packages.orchestration.stop_reasons`; and the
   `ALLOWED_UNWIRED` entry for `story_export.py` is deleted, both of its lines.
S5 THE TESTS. (a) A NEW FILE at `tests/ui_contracts/test_story_player_contract.py`, docstring naming
   F039 T003 and DECISION F039 D8, reading COMMENT-STRIPPED source with `strip_ts_comments`:
   `vite.config.ts` holds `apply: "build"`, `configFile: false`, `input: "src/storyPlayerMain.tsx"`,
   `inlineDynamicImports: true`, `entryFileNames: "story-player.js"`,
   `assetFileNames: "story-player[extname]"` and `STORY_PLAYER_OUT_DIR = "dist/story"`, and
   `story_export.STORY_PLAYER_DIR` equals the repository's `apps/ui` joined with that value;
   `storyPlayerMain.tsx` holds `readEmbeddedStory(` and `getElementById(STORY_DATA_ELEMENT_ID)` and
   none of `fetch(`, `EventSource`, `WebSocket`, `XMLHttpRequest`; `StoryPlayerApp.tsx` holds
   `useTimelineScrub(` once and `<PhaseTimeline scrub={scrub} />`, and its one `<StoryPanel` line
   holds `scrub={scrub}` and not `onClose`; `StoryPanel.tsx` holds `onClose?: () => void;` and the
   conditional Close button of S2 (d); and the TypeScript `STORY_DATA_ELEMENT_ID` equals the Python
   one. (b) `tests/orchestration/test_story_export.py` gains: the page's embedded JSON parses back to
   the payload; a payload string holding `</script><b>` appears in the page only as `</script>`
   and the page holds exactly two `</script` (any case); the style and the script appear verbatim
   inside their elements; the policy holds `default-src 'none'`; a job id `<j&1>` titles the page
   `Remedy story of job &lt;j&amp;1&gt;`; a missing player, a script holding `</SCRIPT>` and a style
   holding `</STYLE>` each raise their code; with `_load_events` patched as the file already does,
   the export at exactly its own length returns the same bytes and at one byte less raises
   `story_too_large`; and `get_key_spec("story.export_max_bytes").default == 5_000_000`.
   (c) A NEW FILE at `tests/cli/test_job_story.py`, modelled on `test_job_ownership.py`, patching
   `story_export.STORY_PLAYER_DIR` to a temporary player and calling `reset_config()` around each
   test: `--json` exits 0 with `ok`, `job_id`, `path`, `bytes` equal to the file's size and
   `budget_bytes` 5000000, and the file equals `export_story_html(job, max_bytes=5_000_000)`; the
   file's mode is `0o644`; the text form prints exactly S4's line; an unknown uuid exits 3
   `job_not_found`; a missing player exits 3 `story_player_missing`; `REMEDY_STORY_EXPORT_MAX_BYTES`
   of 10 exits 1 `story_too_large`; a path in a missing directory exits 1 `story_write_failed`; and
   no refused case leaves a file. (d) `storyExport.test.ts` gains `readEmbeddedStory`:
   `JSON.stringify` of its demo payload reads equal to `decodeStoryExport` of the payload; `null` and
   `{not json` read the unreadable line.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6 and C7, in this order.
C1a — `.agent/authored/f039-r8-block.md` := this block and `.agent/authored/f039-r8-plan.md` :=
  plan.md, by `shutil.copyfile`. Subject: `F039 R8 C1a: copy round 8 block and plan into
  .agent/authored/`. Its insertions are this block's line count plus 28; STOP rather than
  commit at 500 or more.
C1b — `.agent/authored/f039-r8-records.diff` := records.diff. Subject: `F039 R8 C1b: copy round 8
  records diff into .agent/authored/`. Expected insertions: 61.
C2 — `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md. Subject: `F039 R8 C2: book
  round 7 and R-1102, record D8`. Expected by `git show --numstat`: 41/0 decisions.md,
  4/0 live_review.md, 6/8 plan.md.
C3 — S1, S2 and S5 (a) and (d). Subject: `F039 R8 C3: build the story player as one script and read
  the story from its page`.
C4 — S3 with S5 (b). Subject: `F039 R8 C4: write a job's story as one self-contained page within a
  size budget`.
C5 — S4 with S5 (c). Subject: `F039 R8 C5: add remedy job story --export`.
C6 — your mutation tool as `.agent/authored/f039-r8-mutations.py`. Subject: `F039 R8 C6: add the
  mutation tool for the story export`.
C7 — `.agent/handoff.md`, rewritten per `docs/agents/handback_template.md`. Subject: `F039 R8 C7:
  rewrite handoff for round 8`. Then `git push origin feature/f039-story-replay-mode` and report
  its real outcome. Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split one that
   would reach it into lettered parts with their own subjects, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f039-r8-*` files,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `apps/ui/vite.config.ts`,
   `apps/ui/src/storyPlayerMain.tsx`, `apps/ui/src/components/story/StoryPanel.tsx`,
   `storyExport.ts`, `storyExport.test.ts`, `StoryPlayerApp.tsx` and `StoryPlayerApp.module.css`
   under `apps/ui/src/components/story/`, `packages/orchestration/story_export.py`,
   `packages/orchestration/config.py`, `docs/guides/environment.md`, `docs/guides/exit-codes.md`,
   `apps/cli/commands/job_story_cmd.py`, `apps/cli/commands/__init__.py`,
   `apps/cli/command_catalog.py`, `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/test_no_orphan_modules.py`, `tests/ui_contracts/test_story_player_contract.py`,
   `tests/orchestration/test_story_export.py`, `tests/cli/test_job_story.py` and
   `.agent/handoff.md`. Report the list `git diff --name-only 73102551c` measures after C7. Touch
   nothing else.
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
 the PAYLOADS table; then compare each `.agent/authored/f039-r8-*` payload copy byte for byte with
 its source (the block copy against `.remedy-wt/f039-r8/block.md`), read back with `git show
 <commit>:<path>` from the commit that added it. One reading each.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its records tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2441634 | a80ec1dfa82bf138db1cbb1808d6cb8acd578874038e71ad0da586baf328fc0d |
 | .agent/live_review.md | 355852 | 1042df3558e251cdf35f251a7a70540525c094dc4f866527aac144329fc9d4ed |
 | .agent/plan.md | 978 | 685af5cc9907ee97f112f755f9b5baeff065cf4b78f6e7b98f726409f228e952 |
 Also: `open_finding_ids` and `latest_gate_verdict` from `scripts/rotate_live_review.py` over the
 ledger's TEXT at C2, which the reviewer read as `[]` and `PASS`; and `git diff --name-only <C1b>
 <C2>`, which must name exactly the paths of the table.

G3 THE CODE — `python3 -m ruff check packages/orchestration/story_export.py
 packages/orchestration/config.py apps/cli/commands/job_story_cmd.py apps/cli/commands/__init__.py
 apps/cli/command_catalog.py tests/ui_contracts/test_story_player_contract.py
 tests/orchestration/test_story_export.py tests/cli/test_job_story.py
 .agent/authored/f039-r8-mutations.py` at C6, with its real exit code. Then report, quoted from the
 commits, the plugin of S1, `readEmbeddedStory`, `render_story_html`, `export_story_html` and
 `_cmd_job_story`.

G4 THE BUILD AND THE TESTS — in the primary checkout at C6, SERIALLY, with real exit codes. FIRST
 run `apps/ui/node_modules/.bin/vite build` with `cwd` `apps/ui` from a Python script, report its
 exit code and last 12 output lines, and report for `apps/ui/dist/story/` every file name with its
 byte count and, for each, the counts of `</script` and `</style` (any case), `import(` and
 `fetch(` — the reviewer's dry run read `story-player.css` 10671 and `story-player.js` 257582 bytes
 and zero of all four; any other file there, or a count above zero, is red. THEN:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_story_export.py tests/cli/test_job_story.py tests/cli/test_exit_codes.py tests/test_command_catalog.py tests/test_command_discovery.py tests/test_help_renderer.py tests/test_grouped_cli.py tests/orchestration/test_dead_command_check.py tests/orchestration/test_env_registry.py tests/orchestration/test_config.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially in its simulation tree, which carries its own version of
 C3 to C5 and the primary's `node_modules`, and read `3207 passed, 5 skipped` at real exit code 0,
 the five being the D3 and D12 quarantine skips. Report every `SKIPPED` line; a skip naming
 `node_modules`, `dist` or vitest is red. Then `python3 -m apps.cli.main integrity check --json`:
 all six checks `pass`, `fail_count` 0 and exit code 0, because C2 resolves R-1102.

G5 THE RED PROOFS — your tool `.agent/authored/f039-r8-mutations.py`, following your round 7 tool's
 route, runs vitest over the WORKTREE's `storyExport.test.ts`, and `pytest` over the worktree's
 `tests/ui_contracts/test_story_player_contract.py`, `tests/orchestration/test_story_export.py` and
 `tests/cli/test_job_story.py`, under `python3 -B`, printing one line per mutation with each
 runner's exit code and failed count, controls first and last, `restored byte-identical: True` and
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`:
  m1 `render_story_html` no longer writes `<` as `<`;
  m2 the budget refuses at exactly its size (`>` becomes `>=`);
  m3 `read_story_player` no longer refuses a closing tag;
  m4 the page carries no content security policy;
  m5 the command answers a missing player at exit 1;
  m6 the file is written with mode `0o600`;
  m7 `readEmbeddedStory` parses with no `try`;
  m8 the TypeScript `STORY_DATA_ELEMENT_ID` reads `remedy-story`;
  m9 `StoryPanel` shows Close when no `onClose` is given;
  m10 the plugin drops `inlineDynamicImports`.
 Run it on `git worktree add --detach .remedy-wt/f039-r8-mut <C6>` and report its whole output.
 EVERY mutation must be red in at least one runner; a green one is reported as green, and you then
 add the test that catches it before C7 and re-run. Then remove the worktree, `git worktree prune`,
 and report `git worktree list | wc -l` and `git status --porcelain`, which must be empty.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C7 to C1a and `73102551c` in order (more lines if a
 commit was split); `git worktree list | wc -l`, equal to your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must
 be EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count you
MEASURED beside the one this block expected (none is expected for C3 to C6 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Your Session section reads SESSION 2 of feature F039, round 8, and says in one sentence how much
context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 8,
then T003 closed: the clean-browser test from `file://` with zero network requests over an exported
demo story, and the docs. State the open-findings count, 0, and the operator-questions count, 1.
