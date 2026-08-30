# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 4, round 11.

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
| T002a: Builder repair call resumes when earned | done | round 5 |
| T002b-i: Reviewer repair call resumes when earned | done | round 6 |
| T002c (i+ii): fallback-once, both sides | done | rounds 7-8 |
| T002b-ii step 1: hoist resume-ref before prompt build | done | round 9 |
| R-0758: fix `test_provider_retry.py`'s `resume`-kwarg gap | done | round 10 |
| T002b-ii step 2a: freeze the hunk-rendering convention | done | this round |
| T002b-ii step 2b: wire the shrink into compose_*_prompt | open | next |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002b-ii step 2b: add `resume_ref: str | None = None` to
   `compose_builder_prompt`/`compose_reviewer_prompt` (pingpong_loop.py);
   when set and a diff segment would fire, replace the full diff with
   `render_repair_hunks(select_repair_hunks(repo_root,
   parse_diff_line_ranges(repair_diff), ...))` (frozen this round);
   thread the round-9 hoisted `*_resume_ref` into the call sites; add a
   resume-active fixture shape to `test_builder_prompt_golden.py`/
   `test_reviewer_prompt_golden.py` (existing shapes stay unchanged).
2. T003 follows once T002 is fully closed (after step 2b lands).

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor overrides, ever resumes
  or fails a resume. `render_repair_hunks` (this round) has no caller
  yet; zero behavior change held by construction, not test coverage.
- DECISION F106 D1's D1-compatibility reading (reusing F111's pure hunk
  functions for prompt content, never the diff-apply channel) governs
  step 2b's design; step 2b must not widen it further without a new
  DECISION.
