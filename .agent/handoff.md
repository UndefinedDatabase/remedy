# Handback — F039, round 8: book round 7's PASS and R-1102's resolution, record D8, land T003's export

## Session

SESSION 2 of feature F039 · round 8 · rounds so far 8. This session ran round 8 only: booking
round 7's PASS gate and R-1102's resolution into the ledger, recording DECISION F039 D8, and
landing T003's export — the story player built a second time as one script and one style sheet
under `apps/ui/dist/story/`, `remedy job story <id> --export <file>`, and its size budget key
`story.export_max_bytes`. Context self-assessment: a comfortable margin remained through the
whole round, including reading every named file before writing code, the real `vite build`, the
full G4 pytest selection (~3.5 minutes, 3223 passed), and the mutation tool's one complete run
over 10 mutations; the work was not near its limit.

For the operator, in plain words: round 7 is booked PASS and R-1102 is booked resolved. This
round lands the export half of the story feature: `apps/ui/vite.config.ts` gains a plugin that
runs a second, focused `vite build` once the cockpit's own build finishes, producing exactly
`story-player.js` and `story-player.css` under `dist/story/` — a single script and a single
style sheet with no `import()`, no `fetch()` and no closing tag hidden inside them, because a
page opened straight from disk (`file://`) can load no module chunk at all. A new page entry
(`storyPlayerMain.tsx`) reads a job's story out of the exported page's own embedded JSON rather
than any route, and mounts the same phase bar and story panel the cockpit uses, with no heading
and no Close button (there is nothing to close). `remedy job story <id> --export <file>` writes
one self-contained HTML file — the built player, the job's own story payload, and a content
security policy that allows no network request of any kind — refusing to write anything at all
when the page would be larger than the new `story.export_max_bytes` key (default 5,000,000
bytes; refuses whole, never cuts). Ten mutations were made and every one was caught red by
either the TypeScript or the Python test suite, and each was restored byte-identical afterwards.

## Range

Review of 73102551c..92593133d

## Commits

### 8d0a0fa1d F039 R8 C1a: copy round 8 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r8-block.md | +321/-0 | verbatim copy of the block |
| .agent/authored/f039-r8-plan.md | +28/-0 | verbatim copy of the plan payload |

### 81b36fcc0 F039 R8 C1b: copy round 8 records diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r8-records.diff | +61/-0 | verbatim copy of the records payload |

### 7414c17f3 F039 R8 C2: book round 7 and R-1102, record D8
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +41/-0 | DECISION F039 D8 (the player's second build and the export page) |
| .agent/live_review.md | +4/-0 | F039 R7 gate entry (PASS) and R-1102's `Done:` line |
| .agent/plan.md | +6/-8 | rewritten to round 8's current step |

### 5eea9119c F039 R8 C3: build the story player as one script and read the story from its page
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/story/StoryPanel.tsx | +3/-3 | S2 (d): `onClose` optional, Escape calls `onClose?.()`, Close button conditional |
| apps/ui/src/components/story/StoryPlayerApp.module.css | +11/-0 | NEW: S2 (b), the exported page's own root style |
| apps/ui/src/components/story/StoryPlayerApp.tsx | +20/-0 | NEW: S2 (b), the whole exported app over one `useTimelineScrub` |
| apps/ui/src/components/story/storyExport.test.ts | +19/-1 | S5 (d): `readEmbeddedStory` tests |
| apps/ui/src/components/story/storyExport.ts | +24/-0 | S2 (a): `STORY_DATA_ELEMENT_ID`, `readEmbeddedStory` |
| apps/ui/src/storyPlayerMain.tsx | +23/-0 | NEW: S2 (c), the exported page's own entry |
| apps/ui/vite.config.ts | +40/-2 | S1: `STORY_PLAYER_OUT_DIR`, `storyPlayerBuild()` plugin |
| tests/ui_contracts/test_story_player_contract.py | +81/-0 | NEW: S5 (a), the build/page/panel contract |

### 0ac5b802f F039 R8 C4: write a job's story as one self-contained page within a size budget
| Path | +/- | Reason |
|---|---|---|
| docs/guides/environment.md | +1/-0 | regenerated: `story.export_max_bytes` row |
| packages/orchestration/config.py | +10/-0 | `story.export_max_bytes` key, directly after `story.chapter_pause_ms` |
| packages/orchestration/story_export.py | +125/-2 | S3: `STORY_DATA_ELEMENT_ID`, `STORY_PLAYER_DIR`, `StoryExportError`, `read_story_player`, `render_story_html`, `export_story_html` |
| tests/orchestration/test_story_export.py | +109/-0 | S5 (b): the player read, the page, the budget, the key |

### 62ade331d F039 R8 C5: add remedy job story --export
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +16/-0 | `job.story` entry, directly after `job.ownership` |
| apps/cli/commands/__init__.py | +2/-1 | `job_story_cmd` imported and looped over (see Deviations) |
| apps/cli/commands/job_story_cmd.py | +74/-0 | NEW: S4, `_cmd_job_story` |
| docs/guides/exit-codes.md | +1/-0 | `remedy job story` row, after the ownership row |
| tests/cli/test_job_story.py | +129/-0 | NEW: S5 (c) |
| tests/orchestration/import_reachability_allowlist.txt | +2/-0 | `job_story_cmd` and `story_export` allowlisted |
| tests/test_no_orphan_modules.py | +0/-2 | `ALLOWED_UNWIRED` entry for `story_export.py` removed (now wired) |

### 92593133d F039 R8 C6: add the mutation tool for the story export
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r8-mutations.py | +188/-0 | NEW: mutation tool for m1-m10 |

## External actions

- `git worktree add --detach .remedy-wt/f039-r8-mut 92593133d` — created for G5. Outcome:
  success, `HEAD is now at 92593133d`.
- `git worktree remove .remedy-wt/f039-r8-mut` — outcome: success (no output).
- `git worktree prune` — outcome: success (no output).
- `git push origin feature/f039-story-replay-mode` — outcome reported in the reply (per the
  block, G6's readings, including this one, go in the reply rather than this file).
- No PR created (the block forbids it this round).

## Verification

### BEFORE ANYTHING ELSE (block steps 1-4)
```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f039-story-replay-mode
$ git log --oneline -1
73102551c F039 R7 C7: rewrite handoff for round 7
```
Block bytes (R-0954): measured line count 321 / given 321; measured sha256
`dd2fd06b4fdeb5aa61077005d0052311cae7a9f949b570095030dcdda8d0fc7f` / given the same — MATCH.
`git worktree list | wc -l` at step 4: 62.

### PAYLOADS table
| file | lines measured/given | bytes measured/given | sha256 match |
|---|---|---|---|
| plan.md | 28/28 | 978/978 | match |
| records.diff | 61/61 | 10360/10360 | match |

### G1 TRANSPORT
- plan.md: 28 lines, 978 bytes, sha256 `685af5cc9907ee97f112f755f9b5baeff065cf4b78f6e7b98f726409f228e952` — matches PAYLOADS table.
- records.diff: 61 lines, 10360 bytes, sha256 `c478e03b0ac8180ce0cf5bb4745296c3ce96f101ea3d724554579aab8a23a7b9` — matches PAYLOADS table.
- `git show 8d0a0fa1d:.agent/authored/f039-r8-block.md` == `.remedy-wt/f039-r8/block.md`: byte-identical (sha256 `dd2fd06b...` both sides).
- `git show 8d0a0fa1d:.agent/authored/f039-r8-plan.md` == `.remedy-wt/f039-r8-payloads/plan.md`: byte-identical (sha256 `685af5cc...` both sides).
- `git show 81b36fcc0:.agent/authored/f039-r8-records.diff` == `.remedy-wt/f039-r8-payloads/records.diff`: byte-identical (sha256 `c478e03b...` both sides).

### G2 THE RECORDS
```
$ git apply --check .remedy-wt/f039-r8-payloads/records.diff
REAL_EXIT=0
$ git apply .remedy-wt/f039-r8-payloads/records.diff
REAL_EXIT=0
```
At C2 (`7414c17f3`):
| path | bytes | sha256 | matches table |
|---|---|---|---|
| .agent/decisions.md | 2441634 | a80ec1dfa82bf138db1cbb1808d6cb8acd578874038e71ad0da586baf328fc0d | yes |
| .agent/live_review.md | 355852 | 1042df3558e251cdf35f251a7a70540525c094dc4f866527aac144329fc9d4ed | yes |
| .agent/plan.md | 978 | 685af5cc9907ee97f112f755f9b5baeff065cf4b78f6e7b98f726409f228e952 | yes |

`open_finding_ids(text)` over the ledger at C2 = `[]`; `latest_gate_verdict(text)` = `PASS` —
both match the reviewer's stated readings.

`git diff --name-only 81b36fcc0 7414c17f3`:
```
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Exactly the table's three paths.

### G3 THE CODE
```
$ python3 -m ruff check packages/orchestration/story_export.py packages/orchestration/config.py apps/cli/commands/job_story_cmd.py apps/cli/commands/__init__.py apps/cli/command_catalog.py tests/ui_contracts/test_story_player_contract.py tests/orchestration/test_story_export.py tests/cli/test_job_story.py .agent/authored/f039-r8-mutations.py
All checks passed!
REAL_EXIT=0
```

The plugin of S1, quoted from the commit (`5eea9119c`):
```ts
// F039 T003, DECISION F039 D8 — a page opened from `file://` can load no chunk: the story
// player is built a second time, once the cockpit's own build closes, as ONE script and ONE
// style sheet under fixed names, so the export can inline both into a page that needs no
// server and no module loader.
export const STORY_PLAYER_OUT_DIR = "dist/story";

function storyPlayerBuild(): Plugin {
  return {
    name: "remedy-story-player",
    apply: "build",
    async closeBundle() {
      await build({
        configFile: false,
        root: ".",
        base: "./",
        logLevel: "warn",
        plugins: [react()],
        build: {
          outDir: STORY_PLAYER_OUT_DIR,
          emptyOutDir: true,
          sourcemap: false,
          copyPublicDir: false,
          cssCodeSplit: false,
          modulePreload: false,
          rollupOptions: {
            input: "src/storyPlayerMain.tsx",
            output: {
              entryFileNames: "story-player.js",
              assetFileNames: "story-player[extname]",
              inlineDynamicImports: true,
            },
          },
        },
      });
    },
  };
}
```

`readEmbeddedStory`, quoted from the commit (`5eea9119c`):
```ts
export function readEmbeddedStory(
  text: string | null,
): { ok: true; story: StoryExport } | { ok: false; message: string } {
  if (text === null) {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
  try {
    return decodeStoryExport(JSON.parse(text));
  } catch {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
}
```

`render_story_html` and `export_story_html`, quoted from the commit (`0ac5b802f`):
```python
def render_story_html(payload: dict[str, Any], script: str, style: str) -> str:
    """The exported page of DECISION F039 D8 (3): one HTML document with no request of its
    own. The content security policy allows no `default-src` at all, inline script and style
    only; the payload is written as JSON with every `<` replaced by `\\u003c`, so a story
    string that itself reads `</script>` can never close the element early; the built
    player's script and style are inlined verbatim (`read_story_player` already refused a
    built player carrying its own closing tag).
    """
    job_id = html.escape(str(payload.get("job_id", "")))
    payload_json = json.dumps(payload, ensure_ascii=False, sort_keys=True).replace("<", "\\u003c")
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
        "script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:\">\n"
        f"<title>Remedy story of job {job_id}</title>\n"
        f"<style>{style}</style>\n"
        "</head>\n"
        "<body>\n"
        '<div id="root" data-ui="remedy-story"></div>\n'
        f'<script type="application/json" id="{STORY_DATA_ELEMENT_ID}">{payload_json}</script>\n'
        f'<script type="module">{script}</script>\n'
        "</body>\n"
        "</html>\n"
    )


def export_story_html(job: Any, *, max_bytes: int, player_dir: Path | None = None) -> bytes:
    """The whole export (DECISION F039 D8): `build_story_payload(job)` rendered around the
    built player, as UTF-8 bytes. Refuses whole — never cuts a story — when the page is
    larger than `max_bytes` (`story.export_max_bytes`), naming both numbers, the key and
    that nothing was written.
    """
    script, style = read_story_player(player_dir)
    payload = build_story_payload(job)
    page = render_story_html(payload, script, style)
    data = page.encode("utf-8")
    if len(data) > max_bytes:
        raise StoryExportError(
            "story_too_large",
            f"The story is {len(data)} bytes, over the `story.export_max_bytes` budget of "
            f"{max_bytes} bytes; nothing was written.",
        )
    return data
```

`_cmd_job_story`, quoted from the commit (`62ade331d`):
```python
def _cmd_job_story(job_id_str: str, export_path: str, *, json_output: bool = False) -> None:
    from packages.orchestration.pingpong_job import load_job_plan

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    job = load_job_plan(job_id)
    if job is None:
        fail("job_not_found", f"The record of job {job_id} cannot be read.",
             json_output=json_output, exit_code=EXIT_NOT_READY, job_id=job_id)

    budget = get_config().get("story.export_max_bytes")
    try:
        data = export_story_html(job, max_bytes=budget)
    except StoryExportError as exc:
        if exc.error == "story_player_missing":
            fail(exc.error, exc.message, json_output=json_output, exit_code=EXIT_NOT_READY,
                 job_id=job_id)
        fail(exc.error, exc.message, json_output=json_output, job_id=job_id)

    target = Path(export_path)
    try:
        durable_write(target, data, mode=0o644)
    except OSError as exc:
        fail("story_write_failed", f"The story could not be written to {target}: {exc.strerror}",
             json_output=json_output, job_id=job_id)

    if json_output:
        emit_ok(job_id=job_id, path=str(target), bytes=len(data), budget_bytes=budget)
        return

    print(f"Wrote the story of job {job_id} to {target} ({len(data)} bytes). Open it in any "
          f"browser; it needs no network and no Remedy.")
```

### G4 THE BUILD AND THE TESTS
```
$ python3 <script running apps/ui/node_modules/.bin/vite build with cwd=apps/ui>
EXIT= 0
LAST 12 LINES:
rendering chunks...
computing gzip size...
dist/index.html                                  0.41 kB │ gzip:   0.28 kB
dist/assets/index-D5WfmfJG.css                  69.45 kB │ gzip:  12.82 kB
dist/assets/diffHighlightGrammars-o9XqnLhb.js    1.70 kB │ gzip:   0.79 kB
dist/assets/index-345NClaD.js                  722.52 kB │ gzip: 234.18 kB
✓ built in 2.17s

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.

STORY DIR CONTENTS (apps/ui/dist/story/):
story-player.css 10644 bytes — </script:0 </style:0 import(:0 fetch(:0
story-player.js 257567 bytes — </script:0 </style:0 import(:0 fetch(:0
```
Exactly the two expected files, both counts zero across the board on both. The reviewer's own
dry run read `story-player.css` at 10671 bytes and `story-player.js` at 257582 bytes; this real
build in this environment reads 10644 and 257567 — a normal minifier/timestamp variance, not a
shape difference, and the pass condition (no other file, zero of all four patterns) holds exactly.

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_story_export.py tests/cli/test_job_story.py tests/cli/test_exit_codes.py tests/test_command_catalog.py tests/test_command_discovery.py tests/test_help_renderer.py tests/test_grouped_cli.py tests/orchestration/test_dead_command_check.py tests/orchestration/test_env_registry.py tests/orchestration/test_config.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252)
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252)
3223 passed, 5 skipped in 215.27s (0:03:35)
REAL_EXIT=0
```
None of the 5 skips names `node_modules`, `dist` or `vitest` — all five are the pre-existing
D3/D12 quarantine skips, exactly the five the block names.

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=169"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
All six checks pass, `fail_count` 0, exit 0 — R-1102 is resolved, so `high_blockers_open` passes.

### G5 THE RED PROOFS
```
$ bash -c 'git worktree add --detach .remedy-wt/f039-r8-mut 92593133d; echo "REAL_EXIT=$?"'
Preparing worktree (detached HEAD 92593133d)
HEAD is now at 92593133d F039 R8 C6: add the mutation tool for the story export
REAL_EXIT=0

$ bash -c 'python3 -B .agent/authored/f039-r8-mutations.py .remedy-wt/f039-r8-mut; echo "REAL_EXIT=$?"'
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f039-r8-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=6 | guard exit=0 failed=0 passed=31
m1 (render_story_html no longer writes < as <): vitest exit=0 failed=0 passed=6 | guard exit=1 failed=1 passed=30 | caught=True restored byte-identical=True
m2 (the budget refuses at exactly its size (> becomes >=)): vitest exit=0 failed=0 passed=6 | guard exit=1 failed=1 passed=30 | caught=True restored byte-identical=True
m3 (read_story_player no longer refuses a closing script tag): vitest exit=0 failed=0 passed=6 | guard exit=1 failed=1 passed=30 | caught=True restored byte-identical=True
m4 (the page carries no content security policy): vitest exit=0 failed=0 passed=6 | guard exit=1 failed=1 passed=30 | caught=True restored byte-identical=True
m5 (the command answers a missing player at exit 1): vitest exit=0 failed=0 passed=6 | guard exit=1 failed=1 passed=30 | caught=True restored byte-identical=True
m6 (the file is written with mode 0o600): vitest exit=0 failed=0 passed=6 | guard exit=1 failed=1 passed=30 | caught=True restored byte-identical=True
m7 (readEmbeddedStory parses with no try): vitest exit=1 failed=1 passed=5 | guard exit=0 failed=0 passed=31 | caught=True restored byte-identical=True
m8 (the TypeScript STORY_DATA_ELEMENT_ID reads remedy-story): vitest exit=0 failed=0 passed=6 | guard exit=1 failed=1 passed=30 | caught=True restored byte-identical=True
m9 (StoryPanel shows Close when no onClose is given): vitest exit=0 failed=0 passed=6 | guard exit=1 failed=1 passed=30 | caught=True restored byte-identical=True
m10 (the plugin drops inlineDynamicImports): vitest exit=0 failed=0 passed=6 | guard exit=1 failed=1 passed=30 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=6 | guard exit=0 failed=0 passed=31
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0

$ bash -c 'git worktree remove .remedy-wt/f039-r8-mut; echo "REAL_EXIT=$?"'
REAL_EXIT=0
$ bash -c 'git worktree prune; echo "REAL_EXIT=$?"'
REAL_EXIT=0
$ git worktree list | wc -l
62
$ git status --porcelain
(empty)
```
All 10 mutations caught (every one red in at least one runner), all restored byte-identical, no
skip.

## Authored-text proofs

| payload | committed at | disk-to-disk vs source | result |
|---|---|---|---|
| block.md copy | 8d0a0fa1d | `.agent/authored/f039-r8-block.md` vs `.remedy-wt/f039-r8/block.md` | byte-identical |
| plan.md copy | 8d0a0fa1d | `.agent/authored/f039-r8-plan.md` vs `.remedy-wt/f039-r8-payloads/plan.md` | byte-identical |
| records.diff copy | 81b36fcc0 | `.agent/authored/f039-r8-records.diff` vs `.remedy-wt/f039-r8-payloads/records.diff` | byte-identical |
| records.diff application | 7414c17f3 | `git apply` of the reviewer's diff, C2's three files' sha256 vs the G2 table | all three match |

## Item Status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | this handback |
| G1 transport | done | |
| G2 records | done | |
| G3 code (ruff + quotes) | done | |
| G4 build and tests | done | |
| G5 red proofs | done | all 10 mutations caught |
| G6 tree and push | done | reported in the reply |

## Deviations & assumptions

1. **`apps/cli/commands/__init__.py`'s import of `job_story_cmd` is not immediately adjacent to
   `job_steer_cmd`.** The block says the module "imports and loops over `job_story_cmd` after
   `job_steer_cmd`." The import block is `ruff`'s `I001`-sorted (this file is in G3's ruff set),
   and alphabetically `job_stop_cmd` sorts between `job_steer_cmd` and `job_story_cmd`
   (`steer` < `stop` < `story`), so the literal instruction is satisfied — `job_story_cmd` comes
   after `job_steer_cmd` — with `job_stop_cmd` between them rather than adjacent. The loop tuple
   at the bottom of the file (not import-sorted) places `job_story_cmd` directly after
   `job_steer_cmd`, matching the block's ordering exactly there.
2. No other departure from the block's ordered commit sequence (C1a, C1b, C2, C3, C4, C5, C6,
   C7). No commit reached the 500-line cap; none was split.
3. No test this round wrote was found wrong and corrected before C7 (constraint 4 did not
   trigger).

## Next

Phase 1 rule 1: read `.agent/STOP` from disk before anything else. Then the review of round 8 —
DECISION F039 D8's build plugin, the exported page, and `remedy job story --export` with its
budget. Then, once round 8 is booked, T003 closed: the clean-browser test from `file://` with
zero network requests over an exported demo story, and the docs. Open-findings count: 0.
Operator-questions count: 1.
