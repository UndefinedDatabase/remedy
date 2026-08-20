# Release Capability v1

> How Remedy ships: what the wheel carries, what `remedy --version` reports, and
> every reason the release gate refuses a release. Built by F086 — T001 packaging
> and the asset carry, T002 the version report, T003 the gate. The target plan is
> [T2_F086.md](../roadmap/features/T2_F086.md); this page describes what is BUILT,
> and its last section states what is NOT proven.

## Overview

Six files carry this capability and no seventh. `pyproject.toml` declares the
distribution, the console entrypoint and the carry that puts the built UI into the
wheel. `hatch_build.py` is the build hook: it refuses a wheel with no UI and
embeds the revision that wheel was built from. `apps/cli/version_report.py` reads
that revision back for `remedy --version`.
`packages/orchestration/release_gate.py` decides whether a release may proceed,
`scripts/release_gate_check.py` observes the real artifact and asks it, and
`.github/workflows/release.yml` runs that pair on a manual trigger. The split is
deliberate: the gate DECIDES and runs nothing, the script OBSERVES, so every value
judged comes from the artifact under release rather than from a second declaration
that could drift away from it.

## The wheel

`[project.scripts]` maps `remedy` to `apps.cli.grouped:main`, so installing the
wheel puts the CLI on PATH. The wheel target packages `packages` and `apps`.

The built UI is carried explicitly by `artifacts = ["apps/ui/dist/**"]`, and it
has to be named: `apps/ui/dist` is build output, untracked, and matched by the
generic `dist/` entry in `.gitignore`, so a VCS-aware backend omits it otherwise.
DECISION F086 D3 chose that mechanism by measurement at `72e07381`, from a probe
worktree outside the repository — `pyproject.toml` as committed produced 414
members and no files under `apps/ui/dist/`; `artifacts` produced 417 members,
2155470 bytes and 3 UI files; a `force-include` table produced 417 members,
2155479 bytes and the same 3. `artifacts` won because it needs no
source-to-target path mapping and is the smaller of the two.

The carry is NOT a guard. Measured at that same commit, a build with `artifacts`
applied and no `apps/ui/dist` present exits 0 and ships the same 414-member wheel
with no UI in it at all. That is what the build hook exists for.

## The build hook

`hatch_build.py` declares ONE hook class, `RemedyBuildHook`, because hatchling's
`load_plugin_from_script` refuses a script defining two. Its `initialize` does two
things. It calls `assert_frontend_assets_built`, which raises `ValueError` naming
`apps/ui/dist/index.html` and telling the caller to build the frontend first — so
DECISION F086 D1 part (b), never ship an empty UI silently, is enforced at build
time instead of discovered by a user. And it merges `build_revision_metadata`
into the build's `extra_metadata`.

Both rules live in plain module-level functions, so the test suite exercises them
without the build backend installed. The revision is written to a temporary
staging directory and never into the source tree: a generated file there would
survive the build and report a revision nobody built.

## Asset resolution has one mode, deliberately

Remedy deliberately does NOT carry a two-mode asset resolver. DECISION F086 D3
withdrew the one that was planned, after measurement: three `.parent` hops from
`packages/orchestration/ui_server.py` land on the wheel ROOT, and `apps/` is a
sibling of `packages/` at that root — the identical geometry a checkout has, so a
single expression already satisfies both modes. A second resolution path would
have been untested surface added to satisfy a premise that turned out false.

The property is still pinned per mode, because a regression would otherwise stay
invisible until a user's first serve: `TestFrontendDistResolution` in
`tests/test_packaging_smoke.py` asserts wheel-root mode, checkout mode, and that a
layout with no `index.html` resolves to `None`.

## Version and build info

DECISION F086 D2 keeps ONE version number, in `pyproject.toml`, and reads it back
through package metadata, so no second literal exists to drift out of sync.
`remedy --version` prints four lines — the distribution version, the build
revision, the Python version and the platform — and `handle_version_flag` runs
before the help pre-scan, so `--version` answers from anywhere in the command tree
rather than being swallowed by `--help` or by argparse.

In a checkout the distribution is usually not installed and no revision was
embedded at build time, and both fields then report `dev`. That is a requirement
and not a fallback: a version command reporting a fabricated revision is worse
than one that admits it is looking at a working tree. For the same reason Remedy
deliberately does not generate a `_version.py` at build time — a stale generated
file in a checkout would outrank the metadata.

The revision is read from `extra_metadata/REVISION` rather than `REVISION`,
because hatchling prefixes every hook-supplied extra-metadata entry with
`extra_metadata/` inside `.dist-info`. That was measured on a built wheel, not
inferred from the API.

## The release gate

`release_gate.py` decides and runs nothing, which is what makes each refusal
testable without a tag, a wheel or a CI run existing. `refuse_release` evaluates
every rule and returns ALL the reasons rather than the first, so a release broken
four ways is fixed once rather than four times.

| Refusal | The rule behind it |
|---|---|
| CI is not green | the observed conclusion is not `success` |
| the tag does not match the version | `normalise_tag` drops a leading `v`, then compares |
| there is no changelog section | `changelog_section` finds no `## [<version>]` heading |
| the changelog section is empty | the heading exists and its body is blank |
| the wheel is too big | its size exceeds `WHEEL_SIZE_BUDGET_BYTES` |

A missing section and an empty one are distinguished on purpose: a caller refuses
on both but must be able to say which. The budget is 8 MiB, measured rather than
guessed — a wheel carrying a stand-in `index.html` was 2040197 B at F086 R12 and
one carrying the built `apps/ui/dist` was 2155470 B at F086 R7 — so it is roughly
four times the real artifact. It admits a UI bundle's growth while still refusing
what it exists to catch: a wheel that swallowed `node_modules`, `.git` or the test
corpus.

`scripts/release_gate_check.py` supplies the values the gate judges. It reads the
version out of the built wheel's own FILENAME, the changelog off disk and the size
from the file itself, so a wheel built from some other version cannot pass by
agreeing with a declaration the build never read. It prints one
`REFUSED: <reason>` line per reason to stderr and exits 1, or reports that the
release may proceed and exits 0.

`.github/workflows/release.yml` fires on `workflow_dispatch` only — cutting a
release is a human decision, so nothing there runs on a push, a tag or a schedule.
It holds `contents: read` and `actions: read` and writes nothing back. It builds
the UI, builds the wheel, reads the conclusion of THIS commit's `ci.yml` run and
hands both to the checker. When no such run exists the step reports `missing`,
which is not `success`, so an absent answer is refused rather than counted as a
green one. The tag reaches the runner through the environment and is never
interpolated into a shell line, so a crafted tag cannot become a command.

Remedy deliberately does not publish from CI. That workflow has no upload step and
holds no index credential, because T2_F086's Do-not-touch keeps the final upload a
HUMAN command in v1.

## CHANGELOG.md is data

The changelog is not decoration — the gate parses it. Bumping the version in
`pyproject.toml` without adding a section for it fails the release rather than
shipping an unexplained one. The format follows Keep a Changelog, and the gate
reads only enough of it to check that the version's section exists and is not
empty.

## What is NOT proven

Two of this feature's DONE conditions are human actions, and no round of the build
workflow has performed either. They are listed here rather than left to be
inferred from a passing suite.

- No wheel has been installed into a fresh virtualenv.
  `tests/test_install_smoke.py` self-skips unless `REMEDY_INSTALL_SMOKE` is set,
  so its install coverage is zero wherever it currently runs (DECISION F086 D4).
  Its unit-level coverage of the surrounding helpers is real.
- `.github/workflows/release.yml` has never been dispatched, so the hosted gate
  has never judged a real release.
