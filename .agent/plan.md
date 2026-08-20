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
R29: record R28's verdict and write the packaging ist-doc. `docs/system/` has had
no page for what F086 built and AGENTS.md requires one; it was drafted for R27 and
again for R28 and cut both times on the block cap, so DECISION F085 D5 gives it a
round of its own. It lands with its two `docs/README.md` rows in the SAME commit
as the file they point at, which is the first change R28's repaired link gate
judges.

## Next Steps
1. CLOSURE is the next round and the last, per docs/roadmap/STATUS_closure_protocol.md
   — evidence job, FRESH review zip, the STATUS line, the README capability sync in
   that SAME commit, the PR. Precondition 4 is met: `## Built State` landed at
   `d420e8e5` and R28 corrected one sentence of it. The open set closes
   PASS_WITH_RISKS, as F083 and F085 both did. That round CREATES the PR, so it is
   the branch terminator §4 item 13 describes, and its verdict lives in the handoff
   and the PR rather than in a later gate entry.
2. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN; no
   round of this workflow can do either. Both are human actions, and closure names
   them as unproven rather than counting a skipped test as coverage.

## Risks
- Closure needs a FRESH review zip and a zip failure is a closure blocker; the zip
  packages `.remedy-wt/`, which R-0403 registered and which no round has paid down.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; this round
  touches no Python at all, so it gates ruff nowhere.
- `remedy integrity check` is denied to this session class, so closure precondition
  3 is met through the underlying module or declared unmet — never assumed.
