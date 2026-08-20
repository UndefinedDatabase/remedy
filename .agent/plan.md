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
R24: record R23's verdict, register the three defects R23 exposed — R-0589 a
constant stated twice and corrected once, R-0590 a gate whose conditional
discharged itself, R-0591 an ordered recipe whose default broke the parity it was
meant to restore — and promote all three counter-measures onto the §3 checklist,
where a rule has to live to bind the next block.

## Next Steps
1. THE INTEGRATION GATE IS DONE and it is GREEN: at R23 the branch full suite ran
   17192 passed / 20 skipped / 0 failed, the branch-only failure set was EMPTY, and
   all 23 base-only ids were attributed to the throwaway worktree's missing build
   artefacts by demonstration at `76661dc1`. Evidence: `.agent/gate_f086_r23/`.
2. CLOSURE is the next substantive round, per docs/roadmap/STATUS_closure_protocol.md
   — evidence job, FRESH review zip, the STATUS line, the PR. The packaging ist-doc
   is written there, when the built state stops moving.
3. The install smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a budget
   AGENTS.md forbids raising by hand.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- Closure needs a FRESH review zip and a zip failure is a closure blocker; the zip
  packages `.remedy-wt/`, which R-0403 registered and which no round has yet paid
  down.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
