# Plan — F080 Machine-readable roadmap mirror & STATUS.md (R4)

Branch: feature/f080-roadmap-mirror — R1 PASS, R2 PASS with the
integration gate, R3 PASS on the executed work with closure blocked by
R-0206 (LAST_REVIEWED_SHA 0362e19c). History stays as it is: no reword,
no rebase, no force-push.

## Goal
F080 R4 (SPLIT, REPAIR): register R-0206 and persist the R3 verdict,
then fix the false positive in the detector itself —
packages/common/path_redaction.py ABS_PATH_RE accepts a zero-length
tail, so the prose delimiter " / " scrubs to "[path]/path" and blocks
the review zip. One-character change (`/{PATH_TAIL}+`) plus regression
tests that pin both halves: prose with a lone slash survives, every
real path is still redacted. Then re-confirm the full suite at the new
HEAD, rebuild the evidence bundle there, and build the FRESH review
zip. No STATUS.md edit, no README edit, no PR — those are R5.

## Operator constraint (verbatim)
From 2026-08-13 the operator reaches this machine ONLY via SSH from a
phone. Starting Claude Code and invoking ONE skill must be the only
required touchpoint. Target: operational and rehearsed by 2026-08-12.

## Sequence
1. F080 — R4 repair + closure part 1 retry (this round), then R5
   closure part 2 (STATUS [x] + README sync + PR, merged at the next
   feature's Open PR Gate).
2. S1+S2 — build skill /build-remedy-self per the package: one-session
   Window-1 discipline (state probe -> decide -> rounds in-session),
   hard guardrails (PR-only merges at Open PR Gate, no force-push,
   explicit gates, .agent/STOP / session-limit / ambiguity ->
   F079 handoff + clean end).
3. S4 — rehearsal: F254 built through the skill, operator present;
   success = accepted with zero operator edits beyond starting it.
4. Normal feature flow through the skill (S5: review-zip stays the
   operator's remote window).

## Next Steps
- Part B: the one-line ABS_PATH_RE fix + the regression class appended
  to tests/orchestration/test_failure_postmortem.py; prove it across
  the scrubber's reader suites and the run_manifest suites.
- Part C: clean tree, push, integrity check, full `-n auto` suite at
  the new HEAD as the closure confirmation run; attribute any red id
  per integration_gate.md step 4.
- Part D: rebuild the bundle at the new HEAD with this round's real
  numbers (evidence dir outside the repo), then the fresh zip; record
  filename + SHA-256 + job id + accepted HEAD for R5.

## Risks
- Hard date: self-drive operational and rehearsed by 2026-08-12.
- ADR-0001 (CYCLE_SAFETY_CAP) awaits human application; blocks
  multi-cycle loop delegation (S3 experiment lane), not the skill.
- The fix touches a SECURITY scrubber: the regression tests must keep
  real-path redaction intact, which is what the second half of the
  appended class pins.
- A failing zip is still a closure BLOCKER: record the raw error plus
  the failing element and hand back, never improvise, never rewrite.
