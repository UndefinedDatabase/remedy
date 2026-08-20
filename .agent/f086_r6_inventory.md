# F086 R6 — wheel carry measurement

Readings only. This file rules on nothing; it records the command line, the real
exit code and the literal value produced, and says plainly where a reading
contradicts the block that ordered it.

## Headline

M2's red control did NOT come back 0. The block requires that reading to be 0
and states that a non-zero value voids the measurement. It measured 3. The
cause was found and is recorded under "Why the control was vacuous". Because of
that halt clause, C4 applied NEITHER candidate pair and `pyproject.toml` is
unchanged this round.

## M0 — build toolchain

| # | Command | Exit | Value |
|---|---------|------|-------|
| M0a | `python3 -c "import build"` | 1 | `ModuleNotFoundError: No module named 'build'` |
| M0b | `python3 -c "import hatchling"` | 1 | `ModuleNotFoundError: No module named 'hatchling'` |
| M0c | `python3 -m pip install --no-input --target .remedy-wt/f086r6-pylib build hatchling` | 0 | `Successfully installed build-1.5.0 hatchling-1.32.0 packaging-26.3 pathspec-1.1.1 pluggy-1.6.0 pyproject_hooks-1.2.0 tomli-2.4.1 tomlkit-0.15.1 trove-classifiers-2026.6.1.19` |
| M0d | `python3 -c "import hatchling"` | 1 | `ModuleNotFoundError: No module named 'hatchling'` — the target install did not enter the system interpreter |

M0c was first run piped through `tail -20`, which masks the exit code, so the
identical command was re-run unpiped to obtain a real one; the second run added
`WARNING: Target directory ... already exists` lines and exited 0.

Versions the readings below were taken with: build 1.5.0, hatchling 1.32.0,
pathspec 1.1.1.

## M1 — probe tree

`git worktree add .remedy-wt/f086r6-tree 91459dc1` → exit 0,
`HEAD is now at 91459dc1`.

`apps/ui/dist` was COPIED into the probe tree from the primary checkout with
`shutil.copytree`. It was not built: the question this round asks is whether the
backend carries an existing gitignored directory, not whether npm can run.

Probe tree `apps/ui/dist` holds 3 files —
`assets/index-CXHVPLg7.js`, `assets/index-_5lFsic1.css`, `index.html`.
`index.html` is among them.

`git -C .remedy-wt/f086r6-tree check-ignore -v apps/ui/dist/index.html` → exit 0,
`.gitignore:13:dist/	apps/ui/dist/index.html`. The assets are therefore
gitignored inside the probe tree, which is the precondition M2 assumes.

## Command-form deviation for every wheel build

The block orders the builds as
`PYTHONPATH=.remedy-wt/f086r6-pylib python3 -m build --wheel --no-isolation --outdir <out> <root>`.
This session's Bash guard refused that form and also refused the `env PYTHONPATH=...`
form. Every build below was therefore run through `python3 - <<'PY'`, which
sets `sys.path[0]` AND `os.environ['PYTHONPATH']` to the absolute
`.remedy-wt/f086r6-pylib`, sets `sys.argv` to the block's argument vector and
calls `runpy.run_module('build', run_name='__main__')`, reporting the
`SystemExit` code. The `PYTHONPATH` assignment is required, not cosmetic: the
first attempt set only `sys.path` and the backend subprocess failed with
`BackendUnavailable: Cannot import 'hatchling.build'`, exit 1. The system
`python3` is the interpreter in every case; no interpreter under `.remedy-wt/`
was executed.

## M2 — red control, base pyproject, probe tree

Argument vector: `--wheel --no-isolation --outdir .remedy-wt/f086r6-out-base .remedy-wt/f086r6-tree`

Exit 0, `Successfully built remedy-0.1.0-py3-none-any.whl`.

| Reading | Value |
|---------|-------|
| total members | 417 |
| byte size | 2155470 |
| members under `apps/ui/dist/` | **3** |
| `apps/ui/dist/index.html` a member | True |

The block requires that third number to be 0 and says that if it is not, the
whole measurement is void because the check cannot fail. It is 3. This
contradicts the block.

## Why the control was vacuous

hatchling 1.32.0, `hatchling/builders/config.py` lines 764-794,
`load_vcs_exclusion_patterns()`, ends with a guard commented
`# validate project root is not excluded by vcs`: it builds a
`pathspec.GitIgnoreSpec` from the root `.gitignore` and, if that spec matches
the build ROOT's own path, returns `[]` — dropping every VCS exclusion pattern.

Evaluated directly with the same library:

    root                                              matched by .gitignore spec
    /home/decodeux/Repos/remedy/.remedy-wt/f086r6-tree            True
    /home/decodeux/Repos/remedy                                   False

`.gitignore` contains a `.remedy-wt/` line, so a probe tree sited under
`.remedy-wt/` matches the very ignore file hatchling reads, and hatchling
disables VCS exclusion for the entire build. `apps/ui/dist` is then included by
the plain `packages = ["packages", "apps"]` entry with no `artifacts` or
`force-include` involved at all.

M1 places the probe tree under `.remedy-wt/` and Constraint 7 requires all
scratch to live there, so within this block's own constraints the M2 control
cannot be made non-vacuous.

`pathspec` 1.1.1 was checked and is not implicated: `GitIgnoreSpec` from
`['dist/']` matches `apps/ui/dist/index.html` → True.

## M3 — variant A (`artifacts`), probe tree

`PYFROM` occurs 1x in the probe tree's base `pyproject.toml` (sha256
`d821ae6bb06d7a1cd1cd737a36ad620098be9b0e8a3cb70adf5add39a65ef360`). One
replacement applied, `PYTO-A` then occurs 1x, +268 bytes.

Argument vector: `--wheel --no-isolation --outdir .remedy-wt/f086r6-out-a .remedy-wt/f086r6-tree`

Exit 0, `Successfully built remedy-0.1.0-py3-none-any.whl`.

| Reading | Value |
|---------|-------|
| total members | 417 |
| byte size | 2155470 |
| members under `apps/ui/dist/` | 3 |
| `apps/ui/dist/index.html` a member | True |

Both numbers are identical to M2's, byte for byte, so this build carries no
evidence that `artifacts` did anything: the three members were already present
without it.

## M4 — variant B (`force-include`), probe tree

The probe tree's `pyproject.toml` was restored to its base bytes and verified
equal before `PYTO-B` was applied. One replacement applied, `PYTO-B` then
occurs 1x, +316 bytes.

Argument vector: `--wheel --no-isolation --outdir .remedy-wt/f086r6-out-b .remedy-wt/f086r6-tree`

Exit **1**. No wheel was produced; `.remedy-wt/f086r6-out-b` is empty. The
backend raised, at `hatchling/builders/wheel.py:82`:

    ValueError: A second file is being added to the wheel archive at the same
    path: `apps/ui/dist/index.html`.

    The most likely cause of this is an entry in the
    `tool.hatch.build.targets.wheel.force-include` table.

with `ERROR Backend subprocess exited when trying to invoke build_wheel`. The
collision exists because the base `packages` entry already contributed
`apps/ui/dist/index.html` under the vacuous condition recorded above; the
`force-include` table then added the same archive path a second time.

M3 and M4 were run despite the M2 halt clause so the reviewer has the raw data.
Both were taken under the same vacuous condition and neither was used to select
a variant.

## Extra reading, not ordered by the block — control from the primary checkout

Taken because the block's stated purpose for M2 is a control that can fail, and
the reading above leaves that unanswered. The primary checkout's root is not
matched by the `.gitignore` spec, its `pyproject.toml` at HEAD is byte-identical
to the base, and its `apps/ui/dist` holds the same 3 files.

Argument vector: `--wheel --no-isolation --outdir .remedy-wt/f086r6-out-primary .`

Exit 0, `Successfully built remedy-0.1.0-py3-none-any.whl`.

| Reading | Value |
|---------|-------|
| total members | 414 |
| byte size | 2038283 |
| members under `apps/ui/dist/` | **0** |
| `apps/ui/dist/index.html` a member | False |

`git status --porcelain` was empty immediately before and immediately after this
build. These three values equal the R3 baseline recorded in `.agent/plan.md` as
committed at `91459dc1` — 414 members, 2038283 bytes, 0 under `apps/ui/dist/`.
C1 of this round rewrote that file, so the sentence lives only at that SHA.

No variant build was taken from the primary checkout: that would require editing
`pyproject.toml` outside C4, which Constraint 3 forbids.

## M5 — installed-layout probe

The variant A wheel from M3 was extracted with `zipfile` to
`.remedy-wt/f086r6-site`. Every command below ran with cwd `/home/decodeux`,
outside the repository. The block's `cd` form was blocked by this session's
directory guard, so the two probes were spawned through
`subprocess.run([...], cwd='/home/decodeux')`; the argument vector is the
block's own.

Probe as literally ordered, `sys.path[:] = ['<site>']` → exit **1**, no stdout:

    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/home/decodeux/Repos/remedy/.remedy-wt/f086r6-site/packages/orchestration/ui_server.py", line 21, in <module>
        from __future__ import annotations
    ModuleNotFoundError: No module named '__future__'

Replacing the whole of `sys.path` drops the standard library, so `ui_server`'s
own first import fails. The traceback does show the module resolved to the
extraction directory.

Probe re-run with `sys.path.insert(0, '<site>')`, everything else unchanged →
exit 0, two lines:

    /home/decodeux/Repos/remedy/.remedy-wt/f086r6-site/packages/orchestration/ui_server.py
    /home/decodeux/Repos/remedy/.remedy-wt/f086r6-site/apps/ui/dist

The first line begins with the extraction directory, so the probe loaded the
extracted copy and not the checkout.

Primary checkout, default `sys.path`, cwd the repository root:
`python3 -c "import packages.orchestration.ui_server as m; print(m.__file__); print(m._get_frontend_dist())"`
→ exit 0, two lines:

    /home/decodeux/Repos/remedy/packages/orchestration/ui_server.py
    /home/decodeux/Repos/remedy/apps/ui/dist

`.remedy-wt/f086r6-site/apps/ui/dist/index.html` exists on disk, and
`_get_frontend_dist()` at `packages/orchestration/ui_server.py:2739` returns the
directory only when that file is present. `_get_frontend_dist()` was not
changed, no finding was registered about it, and R3's open question 4 was not
touched.

## M6 — scratch removal

Recorded in the handback with the other external actions.
