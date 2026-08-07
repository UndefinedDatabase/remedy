# Plan — F080 Machine-readable roadmap mirror & STATUS.md (R3)

Branch: feature/f080-roadmap-mirror — R1 PASS, R2 PASS with the
integration gate and the full suite green (LAST_REVIEWED_SHA 84cd2797).
R3 is closure part 1; R4 is the closure commit + PR.

## Goal
F080 R3 (SPLIT), closure part 1 per docs/roadmap/STATUS_closure_protocol.md:
persist the R2 PASS verdict, route R-0205's class to T2_F083, make the
feature file's Built State current (precondition 4), re-confirm the
closure preconditions, then produce the evidence job and a FRESH review
zip from a clean tree. No STATUS.md edit, no README edit, no PR — those
are R4's closure commit.

## Operator constraint (verbatim)
From 2026-08-13 the operator reaches this machine ONLY via SSH from a
phone. Starting Claude Code and invoking ONE skill must be the only
required touchpoint. Target: operational and rehearsed by 2026-08-12.

## Sequence
1. F080 — R3 closure part 1 (this round), then R4 closure part 2
   (STATUS [x] + README sync + PR, merged at the next feature's Open
   PR Gate).
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
- Part B: Built State appended to docs/roadmap/features/T1_F080.md.
- Part C: closure preconditions 1-5, each recorded with its evidence.
- Part D: evidence job via create_manual_completion_bundle (evidence
  dir OUTSIDE the repo — never committed) + fresh review zip from the
  clean tree; record filename + SHA-256 + job id + accepted HEAD.
- Handback for R4: the reviewer authors the STATUS [x] line from those
  values.

## Risks
- Hard date: self-drive operational and rehearsed by 2026-08-12.
- ADR-0001 (CYCLE_SAFETY_CAP) awaits human application; blocks
  multi-cycle loop delegation (S3 experiment lane), not the skill.
- A failing zip build is a closure BLOCKER: record the raw error and
  hand back, never close without the package.
- Evidence-producer pitfalls (protocol step 1) must be satisfied at
  authoring time: sha256-hex output_hash, full-length base_commit,
  node ids matching `selected`, test_files as files, run_id ^vr-\d{4,}$.
