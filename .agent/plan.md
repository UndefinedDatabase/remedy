# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 2, round 5.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 (a/b/c): capability surface, all 3 adapters, tests | done | rounds 2-4 |
| T002a: Builder repair call resumes when earned | done | this round |
| T002b: Reviewer resume + F111 delta prompt shrink | open | next |
| T002c: expired-session fallback-once rule (verbatim) | open | |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002a wires the Builder side only: a repair round's `build()` call now
   passes `resume=<prior round's captured session id>` exactly when the
   Builder provider's `supports_resume` is true and a prior session id was
   actually captured — never guessed, never sent otherwise. `resume_used`/
   `resume_session_ref` land on the per-round `BuilderOutput` only;
   surfacing them into the closed-schema `provider_evidence.json` is
   deliberately deferred, not part of this slice.
2. T002b: the same threading on the Reviewer's `review()` call, plus the
   delta-prompt shrink via F111's existing diff-repair hunk selection.
3. T002c: the fallback-once rule verbatim (Orchestrator brief) — a resume
   attempt that errors or loses context falls back ONCE to full context
   within the same round, evidenced, never a task failure by itself.
4. T003 follows once T002 is fully closed.

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor override, ever resumes.
  T002a changes no observable behavior for `ClaudeProvider`/
  `ClaudeCliProvider`, and none for a default-constructed `FakeProvider`.
