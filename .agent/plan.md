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
R3, this round: record the R2 verdict in the review ledger, then MEASURE the
packaging shape by building a real wheel in a disposable virtualenv from a
pristine worktree and reading what is inside it. Nothing about the packaging is
changed this round; the inventory is what fixes the T001 order.

## Next Steps
1. R4 — rule the packaging shape and the version single-source as a DECISION in
   `.agent/decisions.md`, from what the R3 inventory actually measured rather
   than from the feature file's assumptions, and author the T001 order against
   it. The open question the inventory exists to settle is whether a wheel built
   from a pristine tree carries `apps/ui/dist` at all: that directory is
   gitignored at `.gitignore:13` and untracked, while the wheel target is a bare
   `packages = ["packages", "apps"]` with no artifacts or force-include rule.

## Risks
- If the wheel omits the UI assets, T001 is not a small packaging tweak: it needs
  a build step that produces the assets and a package-data rule that carries
  them, plus the dual-mode resolver, and the feature file's "fail loudly if
  assets are missing" line becomes the acceptance test.
- `apps/ui/node_modules` is 305 MB and sits under a path the wheel target names.
  Whether it reaches the wheel is measured by R3, not assumed, and the answer
  sets the wheel-size budget T003 wants.
- Building a wheel spawns npm. That spawn is what F085's guard bounds, so a
  packaging round that bypasses the seam would silently undo stage-1
  containment.
