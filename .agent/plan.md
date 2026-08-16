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
R12, this round: record the R11 PASS, resolve R-0501 and register R-0502 and
R-0503 — two gate defects the reviewer wrote into its own R11 block. Pure record
round: no code, no tests, no behaviour, `.agent/` state only.

## Next Steps
1. T002a's migration half: the five builder sites of amendment F085 D1 —
   `managed_builder_execution.py`:1160, `pingpong_provider.py`:952, 1075, 1208
   and `stream_evidence.py`:595 — move to `run_guarded` with a builder policy
   and behaviour-equality goldens.
2. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
3. T002b-d, then T003 — network posture, limitations document, README link.

## Risks
- An allowlist bounds what the PARENT hands over, never what the child's runtime
  adds back: a CPython child sets `LC_CTYPE` itself under PEP 538. T003's
  limitations document must say so rather than claim a sealed environment.
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading
  a recycled fd after a later `open()`, so the leak is the cheaper wrong.
