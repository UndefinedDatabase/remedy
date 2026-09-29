# Handback — F039, round 9: book round 8's PASS, record D9, close T003 (outDir, the zero-network live test, the guide)

## Session

SESSION 2 of feature F039 · round 9 · rounds so far 9. This session ran round 9 only: booking
round 8's PASS gate into the ledger, recording DECISION F039 D9, making the story player's
second build follow the resolved `outDir` of the cockpit's own build instead of a fixed path,
proving the exported demo story plays from `file://` with zero network requests over a real
headless-Chrome session driven through `--remote-debugging-pipe`, and landing the story guide.
Context self-assessment: a comfortable margin remained through the whole round — reading every
named file before writing code, deriving the ChromePipe protocol from the block's literal
description, getting the new live test to pass on its first real run, the full G4 pytest
selection (~3 minutes, 2249 passed), and the mutation tool's one complete run over 5 mutations —
the work was not near its limit.

For the operator, in plain words: round 8 is booked PASS. This round makes the story player's
second build write into whatever folder the cockpit's own build was told to use (so a test can
build it into its own private temporary folder instead of the shared `apps/ui/dist`), adds a new
suite test that actually opens an exported demo story in a real, invisible Chrome window and
checks that the only network request Chrome makes is the page file itself — no telemetry, no
tracking pixel, nothing — while also exercising the chapter buttons, the keyboard, and the
Play/Pause toggle, and adds the user-facing guide for the whole story feature. T003 is closed.

## Range

Review of 83afaaaea..a97dbcad1

## Commits

### e38646976 F039 R9 C1a: copy round 9 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r9-block.md | +241/-0 | verbatim copy of the block |
| .agent/authored/f039-r9-plan.md | +28/-0 | verbatim copy of the plan payload |

Measured insertions: 269 (241 + 28), matching the block's expectation exactly.

### 3779f2d7e F039 R9 C1b: copy round 9 records and docs diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r9-records.diff | +54/-0 | verbatim copy of the records payload |
| .agent/authored/f039-r9-docs.diff | +128/-0 | verbatim copy of the docs payload |

Measured insertions: 182 (54 + 128), matching the block's expected 182.

### b538a4b22 F039 R9 C2: book round 8, record D9
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +36/-0 | DECISION F039 D9 (outDir-following build, the zero-network live test, headless Chrome) |
| .agent/live_review.md | +2/-0 | F039 R8 gate entry (PASS) |
| .agent/plan.md | +6/-6 | rewritten to round 9's current step |

Measured: 36/0, 2/0, 6/6 — matching the block's expectation exactly.

### 4e000ec17 F039 R9 C3: build the story player into the resolved outDir
| Path | +/- | Reason |
|---|---|---|
| apps/ui/vite.config.ts | +9/-6 | S1: `STORY_PLAYER_SUBDIR`, `let outDir`, `configResolved`, `path.join(outDir, STORY_PLAYER_SUBDIR)` |
| tests/ui_contracts/test_story_player_contract.py | +3/-1 | S1: the three replacement literals for the retired `STORY_PLAYER_OUT_DIR` one |

No insertion count was ordered for this commit; measured above.

### 1d580ea40 F039 R9 C4: prove the exported demo story plays from file with no request
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_story_export_file_live.py | +281/-0 | NEW: S2, `ChromePipe`, the module-scoped player-build fixture, and the one live test |

No insertion count was ordered for this commit; measured above (under the 500-line cap).

### 5a4663fbd F039 R9 C5: add the story guide, its index rows and its assumption-log row
| Path | +/- | Reason |
|---|---|---|
| docs/README.md | +2/-0 | quick-find row and the guides-table row for the story guide |
| docs/guides/story-user-guide-v1.md | +93/-0 | NEW: S3, the story guide |
| docs/ui/design_reference/assumption_log.md | +1/-0 | S3, the 2026-09-29 F039 row |

Measured: 2/0, 93/0, 1/0 — matching the block's expectation exactly.

### a97dbcad1 F039 R9 C6: add the mutation tool for the zero-network test
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f039-r9-mutations.py | +180/-0 | NEW: mutation tool for m1-m5 |

No insertion count was ordered for this commit; measured above.

### (this commit) F039 R9 C7: rewrite handoff for round 9
| Path | Reason |
|---|---|
| .agent/handoff.md | rewritten per the template (self-reference exception, R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f039-r9-mut a97dbcad1` — created for G5. Outcome:
  success, `HEAD is now at a97dbcad1`.
- `git worktree remove --force .remedy-wt/f039-r9-mut` — outcome: success (no output).
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
83afaaaea F039 R8 C7: rewrite handoff for round 8
```
Block bytes (R-0954): measured line count 241 / given 241; measured sha256
`5f88d82c94fc7bce6d66e378262228ad2952acdaaff220d34f029680ff1bda05` / given the same — MATCH.
`git worktree list | wc -l` at step 4: 62.

### PAYLOADS table
| file | lines measured/given | bytes measured/given | sha256 match |
|---|---|---|---|
| plan.md | 28/28 | 979/979 | match |
| records.diff | 54/54 | 10484/10484 | match |
| docs.diff | 128/128 | 11516/11516 | match |

### G1 TRANSPORT
- plan.md: 28 lines, 979 bytes, sha256 `4be4c6a6f0f0b9fa0bec72dce768df62d0c1964a18b68afae7642458f1fa58b5` — matches PAYLOADS table.
- records.diff: 54 lines, 10484 bytes, sha256 `a5ebd425b534450f90a3118113c212788931b783894aaa814b45bbd74c3f3a08` — matches PAYLOADS table.
- docs.diff: 128 lines, 11516 bytes, sha256 `d154d964eb1b646faad6d800b78b4dd4f4c009f78b3fbd4627c1da235dbfe382` — matches PAYLOADS table.
- `git show e38646976:.agent/authored/f039-r9-block.md` == `.remedy-wt/f039-r9/block.md`: byte-identical (sha256 `5f88d82c...` both sides).
- `git show e38646976:.agent/authored/f039-r9-plan.md` == `.remedy-wt/f039-r9-payloads/plan.md`: byte-identical (sha256 `4be4c6a6...` both sides).
- `git show 3779f2d7e:.agent/authored/f039-r9-records.diff` == `.remedy-wt/f039-r9-payloads/records.diff`: byte-identical (sha256 `a5ebd425...` both sides).
- `git show 3779f2d7e:.agent/authored/f039-r9-docs.diff` == `.remedy-wt/f039-r9-payloads/docs.diff`: byte-identical (sha256 `d154d964...` both sides).

### G2 THE RECORDS AND THE DOCS
```
$ git apply --check .remedy-wt/f039-r9-payloads/records.diff
REAL_EXIT=0
$ git apply .remedy-wt/f039-r9-payloads/records.diff
REAL_EXIT=0
$ git apply --check .remedy-wt/f039-r9-payloads/docs.diff
REAL_EXIT=0
$ git apply .remedy-wt/f039-r9-payloads/docs.diff
REAL_EXIT=0
```
At C2 (`b538a4b22`) and C5 (`5a4663fbd`):
| path | bytes | sha256 | matches table |
|---|---|---|---|
| .agent/decisions.md | 2444903 | a0101f2808fea563ddf7ff824dcf0e15224a902d87aa20e15703c6f9213f99fb | yes |
| .agent/live_review.md | 358804 | f78932248cfcd84484368be8056bef0db7aec4a01087fb94b03ad69caffdfc62 | yes |
| .agent/plan.md | 979 | 4be4c6a6f0f0b9fa0bec72dce768df62d0c1964a18b68afae7642458f1fa58b5 | yes |
| docs/README.md | 20901 | 7a4249bcfb957166ebf958ff6d35b5b7f804e8574738039b908efc01c5967498 | yes |
| docs/guides/story-user-guide-v1.md | 5325 | 6fdaf8fb8e8a247da02611453d3a692ddd238e59512fdb0966ce36577e0768df | yes |
| docs/ui/design_reference/assumption_log.md | 27315 | c0b849ed4f46d70a3b10615d1d9c068bebdfe7e79cf6fe0a5f0f9de162de66ab | yes |

`open_finding_ids(text)` over the ledger at C2 = `[]`; `latest_gate_verdict(text)` = `PASS` —
both match the reviewer's stated readings.

### G3 THE CODE
```
$ python3 -m ruff check tests/ui_server/test_story_export_file_live.py tests/ui_contracts/test_story_player_contract.py .agent/authored/f039-r9-mutations.py
All checks passed!
REAL_EXIT=0
```

The plugin of S1, quoted from the commit (`4e000ec17`):
```ts
function storyPlayerBuild(): Plugin {
  let outDir = "dist";
  return {
    name: "remedy-story-player",
    apply: "build",
    configResolved(config) {
      outDir = path.resolve(config.root, config.build.outDir);
    },
    async closeBundle() {
      await build({
        configFile: false,
        root: ".",
        base: "./",
        logLevel: "warn",
        plugins: [react()],
        build: {
          outDir: path.join(outDir, STORY_PLAYER_SUBDIR),
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

`ChromePipe`, quoted whole from the commit (`1d580ea40`):
```python
class ChromePipe:
    """Drives headless Chrome over ``--remote-debugging-pipe``: Chrome reads commands on file
    descriptor 3 and writes replies on file descriptor 4, each message one JSON object ended
    by one NUL byte. No websocket-client, no Node driver — the two pipes this class opens are
    the whole transport.
    """

    def __init__(self, chrome: str, profile_dir: Path) -> None:
        cmd_r, cmd_w = os.pipe()
        reply_r, reply_w = os.pipe()
        script = f'exec "$0" "$@" 3<&{cmd_r} 4>&{reply_w}'
        args = [
            "--headless=new",
            "--remote-debugging-pipe",
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=1280,800",
            "about:blank",
        ]
        self._proc = subprocess.Popen(
            ["bash", "-c", script, chrome, *args],
            pass_fds=(cmd_r, reply_w),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        os.close(cmd_r)
        os.close(reply_w)
        self._cmd_w = cmd_w
        self._reply_r = reply_r
        self._buffer = b""
        self._next_id = 1
        self.session_id: str | None = None
        self.events: list[dict[str, Any]] = []

    def _read_message(self, deadline: float) -> dict[str, Any]:
        while b"\0" not in self._buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("timed out waiting for a reply from Chrome's pipe")
            ready, _, _ = select.select([self._reply_r], [], [], remaining)
            if not ready:
                continue
            chunk = os.read(self._reply_r, 1 << 16)
            if not chunk:
                raise EOFError("Chrome's reply pipe closed before answering")
            self._buffer += chunk
        raw, _, self._buffer = self._buffer.partition(b"\0")
        return json.loads(raw.decode("utf-8"))

    def send(self, method: str, params: dict[str, Any] | None = None, *, timeout: float = 15.0) -> dict[str, Any]:
        message_id = self._next_id
        self._next_id += 1
        payload: dict[str, Any] = {"id": message_id, "method": method, "params": params or {}}
        if self.session_id is not None:
            payload["sessionId"] = self.session_id
        os.write(self._cmd_w, json.dumps(payload).encode("utf-8") + b"\0")
        deadline = time.monotonic() + timeout
        while True:
            message = self._read_message(deadline)
            if message.get("id") == message_id:
                if "error" in message:
                    raise RuntimeError(f"{method} failed: {message['error']}")
                return message.get("result", {})
            self.events.append(message)

    def close(self) -> None:
        self._proc.terminate()
        try:
            self._proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self._proc.kill()
            self._proc.wait(timeout=10)
        os.close(self._cmd_w)
        os.close(self._reply_r)
```

### G4 THE BUILD AND THE TESTS
```
$ python3 <script running apps/ui/node_modules/.bin/vite build with cwd=apps/ui>
EXIT 0
LAST 12 LINES:
rendering chunks...
computing gzip size...
dist/index.html                                  0.41 kB │ gzip:   0.28 kB
dist/assets/index-D5WfmfJG.css                  69.45 kB │ gzip:  12.82 kB
dist/assets/diffHighlightGrammars-o9XqnLhb.js    1.70 kB │ gzip:   0.79 kB
dist/assets/index-345NClaD.js                  722.52 kB │ gzip: 234.18 kB
✓ built in 2.21s

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.

$ ls -la apps/ui/dist/story/
story-player.css 10644 bytes
story-player.js 257567 bytes
```
Exactly the two expected files, nothing else.

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server tests/orchestration/test_story_export.py tests/cli/test_job_story.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252)
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252)
2249 passed, 5 skipped in 176.10s (0:02:56)
REAL_EXIT=0
```
Exactly the reviewer's own dry-run reading of 2249 passed, 5 skipped at exit 0; none of the 5
skips names `node_modules`, `dist`, vite, vitest or Chrome — all five are the pre-existing
D3/D12 quarantine skips.

```
$ bash -c 'python3 -m pytest -q -rA tests/ui_server/test_story_export_file_live.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
PASSED tests/ui_server/test_story_export_file_live.py::test_the_exported_demo_story_plays_from_file_with_no_request
1 passed in 6.27s
REAL_EXIT=0
```

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
All six checks pass, `fail_count` 0, exit 0.

### G5 THE RED PROOFS
```
$ bash -c 'git worktree add --detach .remedy-wt/f039-r9-mut a97dbcad1; echo "REAL_EXIT=$?"'
Preparing worktree (detached HEAD a97dbcad1)
HEAD is now at a97dbcad1 F039 R9 C6: add the mutation tool for the zero-network test
REAL_EXIT=0

$ bash -c 'python3 -B .agent/authored/f039-r9-mutations.py .remedy-wt/f039-r9-mut; echo "REAL_EXIT=$?"'
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f039-r9-mut
node_modules linked: True
CONTROL FIRST: exit=0 passed=7 failed=0 errors=0 skipped=0
m1 (the plugin's configResolved sets nothing, so the player lands in dist/story whatever the outDir): exit=1 passed=6 failed=0 errors=1 skipped=0 | caught=True restored byte-identical=True
m2 (render_story_html drops its content security policy and writes an off-machine image before the root element): exit=1 passed=6 failed=1 errors=0 skipped=0 | caught=True restored byte-identical=True
m3 (storyPlayerMain.tsx reads the element remedy-story instead of STORY_DATA_ELEMENT_ID): exit=1 passed=5 failed=2 errors=0 skipped=0 | caught=True restored byte-identical=True
m4 (StoryPanel's Space branch no longer toggles play): exit=1 passed=6 failed=1 errors=0 skipped=0 | caught=True restored byte-identical=True
m5 (PhaseTimeline's slider no longer hands its keys to scrub.onKey): exit=1 passed=6 failed=1 errors=0 skipped=0 | caught=True restored byte-identical=True
CONTROL LAST: exit=0 passed=7 failed=0 errors=0 skipped=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0

$ bash -c 'git worktree remove --force .remedy-wt/f039-r9-mut; echo "REAL_EXIT=$?"'
REAL_EXIT=0
$ bash -c 'git worktree prune; echo "REAL_EXIT=$?"'
REAL_EXIT=0
$ git worktree list | wc -l
62
$ git status --porcelain
(empty)
```
All 5 mutations caught — m1 as an ERROR in the live test's fixture setup (exactly as the block
predicted), m2-m5 as FAILED — every control (7 = 6 contract tests + 1 live test, 0 skipped)
green, every file restored byte-identical.

## Authored-text proofs

| payload | committed at | disk-to-disk vs source | result |
|---|---|---|---|
| block.md copy | e38646976 | `.agent/authored/f039-r9-block.md` vs `.remedy-wt/f039-r9/block.md` | byte-identical |
| plan.md copy | e38646976 | `.agent/authored/f039-r9-plan.md` vs `.remedy-wt/f039-r9-payloads/plan.md` | byte-identical |
| records.diff copy | 3779f2d7e | `.agent/authored/f039-r9-records.diff` vs `.remedy-wt/f039-r9-payloads/records.diff` | byte-identical |
| docs.diff copy | 3779f2d7e | `.agent/authored/f039-r9-docs.diff` vs `.remedy-wt/f039-r9-payloads/docs.diff` | byte-identical |
| records.diff application | b538a4b22 | `git apply` of the reviewer's diff, C2's three files' sha256 vs the G2 table | all three match |
| docs.diff application | 5a4663fbd | `git apply` of the reviewer's diff, C5's three files' sha256 vs the G2 table | all three match |

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
| G2 records and docs | done | |
| G3 code (ruff + quotes) | done | |
| G4 build and tests | done | |
| G5 red proofs | done | all 5 mutations caught |
| G6 tree and push | done | reported in the reply |

## Deviations & assumptions

1. **S1's comment above `STORY_PLAYER_SUBDIR`.** The block asks for "a two-line comment saying
   the player lands in that subdirectory of whatever `outDir` the cockpit's own build resolved,
   `dist/story` by default." The previous four-line comment (naming DECISION F039 D8 and
   describing why a second build exists at all) was replaced by a new two-line comment naming
   DECISION F039 D9 and stating the subdirectory behaviour, since the block's own wording is a
   description of new comment TEXT, not an instruction to keep the old one verbatim while adding
   to it — and "nothing else in the file changes" binds the rest of the file, not this text the
   block itself specifies.
2. **m4's mutation `TO` value.** `StoryPanel.tsx`'s Space branch calls `togglePlaying();` on one
   line; the mutation tool replaces it with `/* toggle disabled */;` (a no-op statement) rather
   than deleting the line outright, so the file stays syntactically valid TypeScript with the
   FROM/TO substitution applying to a single self-contained statement.
3. No other departure from the block's ordered commit sequence (C1a, C1b, C2, C3, C4, C5, C6,
   C7). No commit reached the 500-line cap; none was split.
4. No test this round wrote was found wrong and corrected before C7 (constraint 4 did not
   trigger). No existing test went red.

## Next

Phase 1 rule 1: read `.agent/STOP` from disk before anything else. Then the review of round 9 —
DECISION F039 D9's outDir-following build, the zero-network live-Chrome test, and the story
guide. Then, once round 9 is booked, the closure sequence of F039: the one full-suite run, the
evidence package, the STATUS flip with the ledger rotation, and the pull request. Open-findings
count: 0. Operator-questions count: 1.
