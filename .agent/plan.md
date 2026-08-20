# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1, the merge
commit of PR #206. `.agent/live_review.md` is the source of truth for the open
set, for the next free finding id and for the round map; this file repeats none
of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R2, this round: repair the R1 carry. R1 reset the live-review record and
truncated every multi-line finding paragraph to its headline; this round
registers that defect and the gate defect that let it pass, restores the lost
paragraphs verbatim from the pre-reset blob, and proves the restoration with a
check that is required to fail on the corrupt state. No production code.

## Next Steps
1. R3 — the packaging-shape inventory in `.agent/f086_inventory.md`, MEASURED
   from a real `python -m build` rather than read off the metadata: what the
   built wheel actually contains, whether the UI assets are in it, how the serve
   command resolves that directory, and where a version string could be
   single-sourced from. The reviewer read four starting facts at 76661dc1 —
   `pyproject.toml` declares `version = "0.1.0"` literally, its wheel target
   lists `packages = ["packages", "apps"]` with no package-data rule,
   `apps/cli` defines no `--version` flag, and `ui_server._get_frontend_dist`
   resolves `apps/ui/dist` by walking three parents up from its own `__file__`.
   R3 confirms or refutes each rather than inheriting it.

## Risks
- The finding record is the repository's own memory, and a carry that loses part
  of it is invisible to every existing gate: the four state readers, the docs
  suite and the canary were all green over the truncated file. Until a paragraph
  integrity check exists somewhere durable, every future reset carries the same
  risk.
- `packages = ["packages", "apps"]` collects `apps/ui` wholesale, and
  `apps/ui/node_modules` lives under that path. Whether a built wheel already
  carries that tree is a MEASUREMENT R3 must take.
- Building a wheel spawns npm. That spawn is exactly what F085's guard now
  bounds, so a packaging round that bypasses the seam would silently undo
  stage-1 containment.
