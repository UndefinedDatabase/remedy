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
R22, this session's last: record R21's verdict, register R-0588 — a done-when that
bounded a file measurable only after the last commit while demanding the
declaration be written into the commit before it — and promote that rule onto the
§3 pre-emission checklist, item 14, where a rule has to live to bind the next block.

## Next Steps
1. THE INTEGRATION GATE is the next substantive round and belongs to a session
   with room for it: the full suite per docs/agents/integration_gate.md, branch
   run and base run with `apps/ui/node_modules` and `apps/ui/dist` parity
   restored by COPY, then per-id attribution of every branch-only failure.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH
   review zip, the STATUS line, the PR. The packaging ist-doc is written there,
   when the built state stops moving.
3. The install smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a budget
   AGENTS.md forbids raising by hand.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- The base worktree of the integration gate lacks build outputs, so parity is
  restored by COPY and never by symlink, and `apps/ui/dist` is hashed before and
  after that run or the parity claim is void.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
