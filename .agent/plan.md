# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists yet: it belongs to R31, the closure commit.
`.agent/live_review.md` is the source of truth for the open set, for the next free
finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R30: record R29's verdict, re-confirm the full suite, and build the two artifacts
closure cannot proceed without — the feature-scoped evidence bundle and a FRESH
review zip from a clean tree. It commits no `docs/` change and creates no PR.

## Next Steps
1. R31 IS THE CLOSURE COMMIT and the branch terminator. It is a round of its own
   because the STATUS line quotes the package filename, its SHA-256 and the
   accepted HEAD, and none of those exists before R30 measures them — ordering a
   value that cannot exist when the text is written is the R-0371 defect. R31
   authors the `[x]` STATUS line, the README capability sync in the SAME commit
   (R-0154: README and STATUS may never disagree in any committed state), any
   closure candidates into `.agent/candidates.md`, and the final `.agent` state,
   then creates the PR. Its path set is exactly those four areas.
2. THE PR IS NOT MERGED THIS SESSION. It merges at the next feature's start via
   the Open PR Gate, which is the operator's manual-review window; the operator
   may merge manually at any time instead.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- The review zip packages `.remedy-wt/`, registered as R-0403 and never paid
  down; it makes the package larger and is not a build failure.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs, so it is
  deliberately NOT one of the evidence bundle's verification runs.
- The open set closes PASS_WITH_RISKS, as F083 and F085 both did.
- `remedy integrity check` is denied to this session class, so precondition 3 is
  met through `packages.orchestration.integrity_gate` and reported as such.
