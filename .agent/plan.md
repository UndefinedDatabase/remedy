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
R28: record R27's verdict, and register and fix R-0595 — a false test location in
the F086 feature file's Built State — and R-0596 — the documentation link gate
never evaluated the documentation index, because it parametrised by filename and
two primary docs are both named README.md. The gate is repaired HERE so that R29's
index rows are judged by a gate that works.

## Next Steps
1. THE PACKAGING IST-DOC is R29's work and its FIRST work: `docs/system/` has no
   page for what F086 built and AGENTS.md requires one. It was drafted for R27 and
   again for R28, and cut each time on the block cap; DECISION F085 D5 requires the
   design to change, so it now gets a round of its own. It lands with its two
   `docs/README.md` rows in the SAME commit as the file they point at, and it must
   land BEFORE the closure commit, whose path set R-0154 fixes at STATUS.md,
   README.md and `.agent/`.
2. CLOSURE then follows, per docs/roadmap/STATUS_closure_protocol.md — evidence
   job, FRESH review zip, the STATUS line, the README capability sync in that SAME
   commit, the PR. Precondition 4 is met: `## Built State` landed at `d420e8e5` and
   R28 corrects one sentence of it. The open set closes PASS_WITH_RISKS, as F083
   and F085 both did. That round CREATES the PR, so it is the branch terminator §4
   item 13 describes and its verdict lives in the handoff and the PR.
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
