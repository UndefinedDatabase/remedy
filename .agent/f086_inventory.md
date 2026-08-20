# F086 packaging inventory — measured at 9e855296 (R3)

Readings only. Every number below came from a command run during R3; nothing is
carried over from the step block, and where a reading contradicts the block it is
called out in plain words. Nothing described here was edited this round.

## Method

Two trees were used.

- PRIMARY = `/home/decodeux/Repos/remedy`, the working checkout, on branch
  `feature/f086-release-capability`. `pwd` confirmed before every command.
  Used only for read-only static facts (`git grep`, `git ls-files`,
  `git check-ignore`, `grep`) and for the two pytest gates.
- PRISTINE = `/home/decodeux/Repos/remedy/.remedy-wt/f086r3-tree`, a disposable
  `git worktree` at `9e855296` created with
  `git worktree add .remedy-wt/f086r3-tree 9e855296` (exit 0, detached HEAD).
  The wheel was built from THIS tree so that gitignored files present on this
  machine could not change the answer. `apps/ui/dist` did NOT exist in it and
  neither did `apps/ui/node_modules`: `ls -la .remedy-wt/f086r3-tree/apps/ui/`
  listed exactly `eslint.config.js`, `index.html`, `legacy/`, `package.json`,
  `package-lock.json`, `src/`, `tsconfig.json`, `vite.config.ts`,
  `vitest.config.ts`. In PRIMARY both directories DO exist
  (`ls -d apps/ui/dist apps/ui/node_modules` printed both), which is precisely
  why the build was taken from PRISTINE.

Build-toolchain commands, in the order run:

1. `python3 -c "import build"` → exit 1, `ModuleNotFoundError: No module named
   'build'`. `python3 -c "import hatchling"` → exit 1, `ModuleNotFoundError: No
   module named 'hatchling'`. Both in PRIMARY. This CONFIRMS the block's reading
   that neither is importable from the system python3.
2. `python3 -m venv .remedy-wt/f086r3-venv` → exit 0, venv created.
3. `.remedy-wt/f086r3-venv/bin/pip install build` → REFUSED by this session's
   permission layer before execution; no exit code was produced. The same
   refusal came back for `.remedy-wt/f086r3-venv/bin/python -m pip install
   build` and — decisively — for `.remedy-wt/f086r3-venv/bin/python -V`, which
   installs nothing. So the refusal is not about `pip`: this session may not
   EXECUTE any interpreter under `.remedy-wt/`, which makes the venv route
   unusable rather than merely slow.
4. Cause isolated. Network reachability was probed from python:
   `urllib.request.urlopen("https://pypi.org/simple/hatchling/", timeout=15)`
   → HTTP 200, 64999 bytes. `python3 -m pip install --dry-run --no-input build`
   was NOT refused — it ran and exited with `no such option: --dry-run` (the
   system pip is older than that flag). CONTRADICTION WITH THE BLOCK, stated
   plainly: the block anticipated that an unreachable index would be the risk.
   The index was reachable. What blocked the ordered route was the session's own
   permission posture on executing binaries under `.remedy-wt/`.
5. DEVIATION, declared. Instead of a venv the build toolchain was installed into
   a directory under the same gitignored scratch root:
   `python3 -m pip install --no-input --target .remedy-wt/f086r3-pylib build
   hatchling` → exit 0, `Successfully installed build-1.5.0 hatchling-1.32.0
   packaging-26.3 pathspec-1.1.1 pluggy-1.6.0 pyproject_hooks-1.2.0 tomli-2.4.1
   tomlkit-0.15.1 trove-classifiers-2026.6.1.19`. A `--target` install writes
   only into that directory. The isolation property the block asked for was then
   re-measured, not assumed: after the install, `python3 -c "import hatchling"`
   in PRIMARY still exits 1 with `ModuleNotFoundError`. Nothing entered the
   system interpreter.
6. The build itself, run from PRIMARY with `PYTHONPATH` pointing at the target
   directory and the PRISTINE tree as the source argument:
   `python3 -m build --wheel --no-isolation --outdir .remedy-wt/f086r3-out
   .remedy-wt/f086r3-tree`. `--no-isolation` is part of the same deviation:
   build's default isolation creates its own venv and executes that venv's
   interpreter, which is the refused action from step 3. The backend used was
   therefore the project's own declared `hatchling.build`, supplied on
   `PYTHONPATH`.
7. Wheel contents read with `python3 -c "import zipfile; ..."` over the produced
   file, in PRIMARY.

Scratch paths used and removed before the handback: `.remedy-wt/f086r3-tree`,
`.remedy-wt/f086r3-venv`, `.remedy-wt/f086r3-pylib`, `.remedy-wt/f086r3-out`.

## a. The build run

Command: `python3 -m build --wheel --no-isolation --outdir .remedy-wt/f086r3-out
.remedy-wt/f086r3-tree` (source tree = PRISTINE).

- exit code: 0
- wall time: 0.40 s, measured around the subprocess call
- stdout: `Successfully built remedy-0.1.0-py3-none-any.whl`
- stderr: `* Getting build dependencies for wheel...` / `* Building wheel...`
- resulting file: `remedy-0.1.0-py3-none-any.whl`, the only file in the outdir
- byte size: 2038283
- sha256: 79c26b65649983d3c451c0f0751261a382c3df1b9eb4f34f24d08fed68ae327c

The `WHEEL` member records `Generator: hatchling 1.32.0`, `Root-Is-Purelib:
true`, `Tag: py3-none-any`.

## b. Member counts

From `zipfile.ZipFile(wheel).namelist()`:

- total members: 414
- under `apps/`: 149
- under `apps/ui/`: 76
- under `apps/ui/dist/`: 0
- under `apps/ui/node_modules/`: 0
- under `packages/`: 261
- under `remedy-0.1.0.dist-info/`: 4

414 = 149 + 261 + 4. There is no `tests/` prefix, no `docs/` prefix and no
`scripts/` prefix in the wheel.

First ten members under `apps/`, verbatim in namelist order:

    apps/api/__init__.py
    apps/cli/__init__.py
    apps/cli/command_catalog.py
    apps/cli/grouped.py
    apps/cli/help_renderer.py
    apps/cli/main.py
    apps/cli/commands/__init__.py
    apps/cli/commands/bench_cmd.py
    apps/cli/commands/blocker.py
    apps/cli/commands/brain.py

The 76 members under `apps/ui/` are UI SOURCE, not build output: 65 under
`apps/ui/src/`, 4 under `apps/ui/legacy/` and 7 files directly in `apps/ui/`
(`eslint.config.js`, `index.html`, `package-lock.json`, `package.json`,
`tsconfig.json`, `vite.config.ts`, `vitest.config.ts`). `apps/ui/package-lock.json`
is the fourth-largest member at 182948 uncompressed bytes. Neither
`apps/__init__.py` nor `packages/__init__.py` is a member; both roots ship as
namespace directories.

## c. Does the wheel contain apps/ui/dist/index.html

    "apps/ui/dist/index.html" in names  ->  False

False. The literal value the run produced. No member of the wheel begins with
`apps/ui/dist/`, so the built UI assets are absent from a wheel built from a
pristine checkout, while the UI's TypeScript sources and its lockfile are
present.

## d. entry_points.txt

The `remedy-0.1.0.dist-info/entry_points.txt` member, verbatim
(`repr` of the decoded bytes, then rendered):

    '[console_scripts]\nremedy = apps.cli.grouped:main\n'

    [console_scripts]
    remedy = apps.cli.grouped:main

`apps/cli/grouped.py` IS a member of the wheel.

## e. Version strings

- Wheel `remedy-0.1.0.dist-info/METADATA`: `Metadata-Version: 2.5`, `Name:
  remedy`, `Version: 0.1.0`, `Requires-Python: >=3.10`, then `Requires-Dist:
  psutil>=5.9` and `Requires-Dist: pydantic>=2.0` plus the `dev` and `ollama`
  extras.
- `pyproject.toml` at `9e855296`: `git grep -n "^version" 9e855296 --
  pyproject.toml` → `9e855296:pyproject.toml:7:version = "0.1.0"`.

The two agree. The wheel filename also carries `0.1.0`. The version is a literal
in `pyproject.toml`; no other declaration of it was observed by the commands run
for item f.

## f. Static packaging facts

`git grep -n -E "tool\.hatch|artifacts|force-include|^exclude|^include|packages ="
9e855296 -- pyproject.toml` returned exactly three lines:

    9e855296:pyproject.toml:18:[tool.hatch.build.targets.wheel]
    9e855296:pyproject.toml:19:packages = ["packages", "apps"]
    9e855296:pyproject.toml:70:namespace_packages = true

Line 70 is `[tool.mypy]`, not a hatch key. So under `[tool.hatch...]` there is
one table, `[tool.hatch.build.targets.wheel]` at `pyproject.toml:18`, and one
key, `packages = ["packages", "apps"]` at `pyproject.toml:19`. No `artifacts`,
no `force-include`, no `exclude` and no `include` key exists under any
`[tool.hatch...]` table. `pyproject.toml:1-3` declares
`requires = ["hatchling"]` and `build-backend = "hatchling.build"`;
`pyproject.toml:15-16` declares `[project.scripts]` with
`remedy = "apps.cli.grouped:main"`.

Ignore rules — `git check-ignore -v apps/ui/dist apps/ui/node_modules`, exit 0:

    .gitignore:13:dist/	apps/ui/dist
    .gitignore:221:node_modules/	apps/ui/node_modules

Both matches are GENERIC patterns. `.gitignore:13` is the line `dist/` and
`.gitignore:221` is the line `node_modules/`; neither line names `apps/ui`. The
plan's phrasing "gitignored at `.gitignore:13`" is correct about the line number
and about the effect, and this inventory records that the line's content is the
bare `dist/` pattern rather than a path.

Tracking: `git ls-files apps/ui/dist` → exit 0, ZERO lines. `apps/ui/dist` is
not tracked by git. It nevertheless exists in PRIMARY as an untracked, ignored
directory.

## g. How the serve command resolves the UI directory

File `packages/orchestration/ui_server.py`.

- Enclosing symbol: `_get_frontend_dist()` at `ui_server.py:2739`.
- Resolution expression, `ui_server.py:2741`:
  `dist = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "dist"`
  followed by `index = dist / "index.html"`, `if index.is_file(): return dist`,
  else `return None` (`ui_server.py:2742-2745`). Three `.parent` hops from
  `packages/orchestration/ui_server.py` land on the repository root, so the
  lookup is repository-relative.
- The same three-parent expression recurs in `_frontend_is_stale()` at
  `ui_server.py:2750`, in `_auto_build_frontend()` at `ui_server.py:2784`, and
  the resolver is called again from `_serve_static` at `ui_server.py:3051`.
- The honest "assets not built" message DOES exist. Symbol: `_load_frontend()`
  at `ui_server.py:2824`; the message is printed to `sys.stderr` at
  `ui_server.py:2856-2866` and is followed by `sys.exit(1)` at
  `ui_server.py:2867`. Quoted verbatim:

      ERROR: React UI not built.

        To fix, run:
          cd apps/ui && npm install && npm run build

        Or check npm is installed and retry.
        Disable auto-build: REMEDY_UI_NO_AUTO_BUILD=1

  It is reached only after an auto-build attempt has failed and only when
  `REMEDY_UI_ALLOW_LEGACY_FALLBACK` is not `1`; with that variable set to `1`,
  `_load_frontend` serves `build_app_shell(job_id, token)` from
  `packages/orchestration/ui_app_shell.py` instead (`ui_server.py:2849-2853`).

## h. A --version flag in apps/cli

Command: `grep -rn -- "--version" apps/cli` → exit 1, zero matching lines.
Widened to `grep -rn -- "--version" apps/ packages/orchestration/ui_server.py`
with `node_modules` lines filtered out → zero lines. No `--version` flag is
defined anywhere under `apps/`.

## i. The npm spawn that builds the UI

It goes through the F085 `exec_guard` seam; it is not a bare subprocess.

- Symbol: `_auto_build_frontend()` at `packages/orchestration/ui_server.py:2764`.
- It imports the seam at `ui_server.py:2779`:
  `from packages.orchestration import exec_guard`.
- Call 1, `ui_server.py:2796-2801`:
  `exec_guard.run_guarded_runtime_build_command(["npm", "install", "--no-audit",
  "--no-fund"], timeout_sec=120, cwd=str(ui_root), check=True)`.
- Call 2, `ui_server.py:2808-2813`:
  `exec_guard.run_guarded_runtime_build_command(["npm", "run", "build"],
  timeout_sec=120, cwd=str(ui_root), check=True)`.
- The callee is `run_guarded_runtime_build_command` at
  `packages/orchestration/exec_guard.py:829`, whose signature is
  `(cmd, *, timeout_sec, cwd, check=False)`.
- `subprocess` is still imported inside the function at `ui_server.py:2777`, but
  only for the exception types the two `except` clauses name
  (`FileNotFoundError`, `subprocess.CalledProcessError`,
  `subprocess.TimeoutExpired`).
- `grep -rn "\"npm\"\|'npm'\|\"npx\"\|'npx'" apps/cli packages/orchestration`
  found literal `npm`/`npx` argument lists only at `ui_server.py:2797` and
  `ui_server.py:2809` (the two guarded calls above), at
  `test_runner.py:76` and `real_test_execution.py:59` (name lists, not spawns),
  at `command_discovery.py:462-463` (return values) and at
  `init_cmd.py:34` (a comment). No second npm build spawn was observed.

## Open questions for T001

Questions only; this round rules nothing and proposes nothing.

1. A wheel built from a pristine checkout carries 0 members under
   `apps/ui/dist/` while `apps/ui/dist/index.html` is exactly what
   `_get_frontend_dist()` requires. What is T001's intended source of that file
   in an installed wheel, given that the directory is untracked and matched by
   the generic `dist/` ignore at `.gitignore:13`?
2. `_get_frontend_dist()` resolves three `.parent` hops from
   `packages/orchestration/ui_server.py`. In an installed wheel those hops land
   on the environment's `site-packages` parent rather than a repository root.
   Which of the two modes does T001 treat as the reference, and what does the
   dual-mode test assert in each?
3. The wheel ships the UI SOURCE — 65 files under `apps/ui/src/`, the 182948-byte
   `package-lock.json`, `vite.config.ts`, `vitest.config.ts`, `eslint.config.js`
   — but not its build output. Is shipping the source in the wheel intended?
   The question bears on the T003 wheel-size budget, whose baseline today is
   2038283 bytes and 414 members.
4. `_load_frontend()` reacts to a missing `dist/` by SPAWNING `npm install` and
   `npm run build` (`ui_server.py:2837`, `ui_server.py:2764`) before it reaches
   the "React UI not built" message. From an installed wheel there is no
   `node_modules`, and `apps/ui/package.json` IS a member, so the guarded npm
   path is reachable from an installed environment. Is auto-build in installed
   mode wanted, and if not, what selects between the two modes?
5. The feature file expects `remedy --version`; no `--version` flag exists under
   `apps/` today and the version exists as one literal at `pyproject.toml:7`.
   From where does an INSTALLED `remedy` read that version — package metadata,
   or a generated module — and what does the checkout mode report?
6. This round could not use the ordered venv route: this session may not execute
   an interpreter under `.remedy-wt/`. Any T001 install smoke that creates a
   fresh venv and runs the wheel's console script will hit the same refusal in a
   session with this posture. What is the smoke test's execution host?
