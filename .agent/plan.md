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
R15, this round: record the R14 PASS, register R-0507, and give the claude CLI seam
its guarded runner — `_cli_exec_policy`, `_decode_cli_stream`, `_guarded_cli_run` —
migrating `_resolve_version`, the one site no test's mock reaches, with goldens that
spawn a real fake CLI instead of mocking the stdlib.

## Next Steps
1. R16 migrates the coupled unit of R-0507: `_call`, `_call_reviewer_structured` and
   the envelope test's mock, which must move together, plus R-0506's fix — the stale
   absence claims in `exec_guard.py` and `managed_builder_execution.py`.
2. `stream_evidence.py`:595 is T002a's last site and is NOT a `subprocess.run` swap:
   it streams incrementally where `run_guarded` buffers, so its shape is decided first.
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
