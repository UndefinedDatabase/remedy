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
R44, this round: record the R43 PASS and apply DECISION F085 D4 to
`packages/orchestration/ci_run.py` with five tests. The three findings R43's worker declared
are stated in the record and take ids at R45; the block cap took the half already safe on
disk rather than deferring the code a third time.

## Next Steps
1. R45 — register the three findings RECORD12 states as owed, then migrate
   `packages/orchestration/builder_bridge.py`, the last `test`-class site on a bare spawn,
   which at c3201976 overlays `PYTHONDONTWRITEBYTECODE` onto a copy of `os.environ` and is
   unblocked by the same `extra_env` overlay `ci_run.py` needed (DECISION F085 D3). R45 also
   owes two checklist promotions this branch has measured and not made: widening item 16 to
   any sentence that counts what follows it, and a stated budget for a record slice.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
