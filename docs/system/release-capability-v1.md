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

The wheel carries no UI. Until 2026-10-15 it carried the built `apps/ui/dist` through
`artifacts = ["apps/ui/dist/**"]` (DECISION F086 D3), and the build hook refused a build with no
built frontend (DECISION F086 D1 part (b)). The UI was deleted with the old cockpit, and
amend1015f D3 reverses F086 D1: the carry and the guard are gone, and the wheel holds only
`packages` and `apps`.

## The build hook

`hatch_build.py` declares ONE hook class, `RemedyBuildHook`, because hatchling's
`load_plugin_from_script` refuses a script defining two. Its `initialize` merges
`build_revision_metadata` into the build's `extra_metadata`, so `remedy --version` names the
revision the wheel was built from.

The rule lives in plain module-level functions, so the test suite exercises them
without the build backend installed. The revision is written to a temporary
staging directory and never into the source tree: a generated file there would
survive the build and report a revision nobody built.

The rule does not bind the EDITABLE target. `build_target_embeds_revision` answers
that question and `initialize` returns before the rule when the answer is no.
`pip install -e` writes a path hook into the checkout and builds nothing, so the
embedding has nothing to write there; a checkout reports the build `dev`. A failing hook
there once broke the dev install every fresh clone starts with — including this repository's own first CI step, which is
how R-0598 was found, on run 32402941541.

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
four times the real artifact; the wheel without the UI is smaller still. It keeps refusing
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
