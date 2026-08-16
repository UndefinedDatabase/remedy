# Plan — F085 Sandbox hardening (stage 1)

Branch: feature/f085-sandbox-hardening, cut from origin/main at a5a70621 after
the F083 closure PR #202 and the amendment PR #203 merged.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
Builder-spawned commands stop relying on prompted discipline: every builder,
test and DoD subprocess gets POSIX resource limits, a per-command wall timeout,
output-size caps, a cwd pinned inside the worktree, an environment allowlist and
a default-deny network posture — with a document that says EXACTLY what stage 1
does and does not prevent. DONE when the limits provably kill a runaway fixture
(cpu, memory, oversized output, endless sleep) and classify it `resource_limit`
with the tripped limit named, an off-scope write attempt fails, well-behaved
commands behave identically under the guard, a secret-like parent env var never
reaches a child, and the limitations document exists and is linked from the
README.

## Current Step
R5, this round: record the R4 PASS, register R-0494, then build T001 — the new
module `packages/orchestration/exec_guard.py` with rlimit, wall-timeout and
output-cap mechanics, plus `tests/orchestration/test_exec_guard.py` with the four
runaway fixtures. The module gets NO callers this round.

## Next Steps
1. T002a — builder class, 5 sites, the first seam migration, with
   behaviour-equality goldens for well-behaved commands.
2. T002b-d — test (12 sites), DoD (2) and runtime (5, no wall timeout) classes,
   one ordered sub-slice each, plus environment scrubbing with the allowlist test
   that carries R-0202.
3. T003 — network posture, per-class policy table, the limitations document and
   its README link.

## Risks
- The address-space limit is enforced but NOT attributable from `wait4` data:
  the child raises `MemoryError`, exits 1 with no signal, and its `ru_maxrss`
  stays below the limit. R6 rules on whether stage 1 can name that trip at all.
- 24 in-scope call sites in 18 modules and 22 enclosing functions is a far wider
  migration than the feature file assumed. None of T002's sub-slices may widen
  into the git, packaging or other classes.
