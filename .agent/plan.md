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
R27: record R26's verdict, register R-0594 — a gate that ordered a reading at a
base revision without naming a non-writing mechanism, so the worker overwrote a
tracked path to take it — and land item 29, where a rule has to live to bind the
next block.

## Next Steps
1. THE PACKAGING IST-DOC is owed and is the next round's FIRST work: `docs/system/`
   has no page for what F086 built and AGENTS.md requires one. It was drafted for
   R27 and cut when the block measured 418 lines against the 400 cap. It must land
   BEFORE the closure commit, whose path set R-0154 fixes at STATUS.md, README.md
   and `.agent/`; an earlier commit in the closure round satisfies that.
2. CLOSURE then follows, per docs/roadmap/STATUS_closure_protocol.md — evidence
   job, FRESH review zip, the STATUS line, the README capability sync in that SAME
   commit, the PR. Precondition 4 is already met: `## Built State` landed at
   `d420e8e5`. The open set closes PASS_WITH_RISKS, as F083 and F085 both did.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- Closure needs a FRESH review zip and a zip failure is a closure blocker; the zip
  packages `.remedy-wt/`, which R-0403 registered and which no round has paid down.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
- `remedy integrity check` is denied to this session class, so closure precondition
  3 is met through the underlying module or declared unmet — never assumed.
