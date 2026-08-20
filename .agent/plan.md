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
R23, the INTEGRATION GATE: record R22's verdict, resolve R-0588 — whose
counter-measure landed at `72640273` and which R22's own G13 then met — and run
the tier-3 full suite twice per docs/agents/integration_gate.md, branch and merge
base, with `apps/ui/node_modules` and `apps/ui/dist` parity restored by COPY, then
attribute every id in both comm outputs.

## Next Steps
1. CLOSURE per docs/roadmap/STATUS_closure_protocol.md — evidence job, FRESH
   review zip, the STATUS line, the PR. The packaging ist-doc is written there,
   when the built state stops moving.
2. The install smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a budget
   AGENTS.md forbids raising by hand.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN and NO INSTALL HAS EVER BEEN PROVEN;
   no round of this workflow can do either. Both are human actions, and closure
   names them as unproven rather than counting a skipped test as coverage.

## Risks
- A branch-only failure the gate reproduces serially and couples to feature code
  is a BLOCKER whose repair is its own reviewer-gated round, never this one's.
- The base worktree lacks build outputs, so parity is restored by COPY and never
  by symlink; `apps/ui/dist` is read by DIGEST AND BY MTIME before and after that
  run, because at F085 R72 the digest held still while the mtime moved (R-0565).
  Either reading moving voids the parity claim and forces per-id attribution.
- `tests/test_install_smoke.py` SKIPS everywhere it currently runs. Its unit
  coverage is real; its install coverage is zero until the variable is set.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
