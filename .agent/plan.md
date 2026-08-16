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
R7, this round: record the R6 PASS, register R-0498, and fix R-0496 — the
boundary assertion that made the T001 suite a coin flip. R-0495 is untouched
here; it gets its own round because its fix rewrites the stream pumps.

## Next Steps
1. R8 repairs R-0495: the wall timeout must bound `run_guarded`'s own return and
   not only the process group it can reach, and the result must say whether the
   streams were complete. The docstring's "no descendant outlives this call"
   narrows to the group the kill actually reaches.
2. T002a — builder class, 5 sites, the first seam migration. BLOCKED until R-0495
   is fixed: migrating a seam onto a guard whose timeout does not bound wall time
   would make hangs harder to see, not easier.
3. T002b-d, then T003 — network posture, limitations document, README link.

## Risks
- R-0495 is the feature's central promise failing in its central case. Until it
  is fixed, no round may describe `exec_guard` as bounding runtime, and a green
  T001 suite is not evidence to the contrary: no test covers R-0495 yet.
- The address-space limit is enforced but NOT attributable from `wait4` data;
  R5's G16 probe confirmed it. Whether stage 1 can name that trip stays open.
