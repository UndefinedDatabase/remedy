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
R4, this round: record the R3 PASS, then apply amendment F085 D1 to
`docs/roadmap/features/T2_F085.md` — correct the falsified premise, re-slice
T002 per class, and rule the stage-1 command classes and their policies. No
production code and no test file is touched.

## Next Steps
1. T001 — `exec_guard.py` with rlimit, wall-timeout and output-cap mechanics
   plus the runaway fixtures (cpu, memory, output, sleep), each killed and each
   classified `resource_limit`. The wall timeout is the guard's OWN supervision:
   six of the seven timeout-less in-scope sites are `Popen`, which takes no
   `timeout=` keyword.
2. T002a-d — seam migration, one order per class, with behaviour-equality
   goldens and the environment-allowlist test.

## Risks
- 24 in-scope call sites in 18 modules and 22 enclosing functions is a far wider
  migration than the feature file assumed. T002 is four ordered sub-slices and
  none of them may widen into git, packaging or other.
- R-0202 has one reader and exactly two seams that drop the variable
  (`managed_builder_execution.py`:1160, `test_execution_service.py`:323). Naming
  them is not fixing them, and no round may fix them outside T002.
