# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists: this feature is mid-flight and its PR belongs to
its closure round. `.agent/live_review.md` is the source of truth for the open set,
for the next free finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R26: closure PREPARATION. Record R25's verdict, register R-0593 — two stale
absence claims left in production text by the very rounds that built the thing
each says does not exist — retire both at their source, and add the feature
file's `## Built State` section, which the closure protocol's precondition 4
requires and which R-0154 forbids the closure commit from touching.

## Next Steps
1. THE PACKAGING IST-DOC is still owed: `docs/system/` has no page for what F086
   built, and AGENTS.md requires one. It plus its `docs/README.md` row is the
   next round's first work, and it must land BEFORE the closure commit, whose
   path set R-0154 fixes at STATUS.md, README.md and `.agent/`.
2. CLOSURE follows, per docs/roadmap/STATUS_closure_protocol.md — evidence job,
   FRESH review zip, the STATUS line, the README capability sync in that SAME
   commit, the PR. Precedent for the open set: F083 and F085 both closed
   PASS_WITH_RISKS.
3. THE INTEGRATION GATE IS DONE and GREEN: at R23 the branch full suite ran
   17192 passed / 20 skipped / 0 failed, the branch-only failure set was EMPTY,
   and all 23 base-only ids were attributed by demonstration at `76661dc1`.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- Closure needs a FRESH review zip and a zip failure is a closure blocker; the zip
  packages `.remedy-wt/`, which R-0403 registered and which no round has paid down.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
