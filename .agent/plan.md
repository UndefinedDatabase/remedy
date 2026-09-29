# Plan — F041 Artifact preview

Branch: feature/f041-artifact-preview, cut from `main` at `45c584e6`,
the merge commit of pull request 294 (F286 Findings paydown v5).

## Goal

Make a job's results tangible in the cockpit: its README as sanitized
markdown, its screenshots in a lightbox, and an app card that shows a live
link only after a probe passes (`docs/roadmap/features/T5_F041.md`,
DECISION F041 D1).

## Current Step

ROUND 1 BLOCKED at C3. C1a/C1b/C1c/C2 are committed and pushed. S1-S6 are
written, pass the reviewer's whole corpus (106+20+5 = 131) unedited, and
are red-proved against all 9 named mutations, but staging S1-S6 plus
`allowlist.diff` in ONE commit (as C3's own clause requires) measures 542
insertions — over the 500 cap — and the block orders "stop and report
rather than split it" for exactly this case. C3-C6 are therefore NOT
committed; the validated code, the three test files and the mutation tool
sit uncommitted in the working tree for the next session.

## Next Steps

1. Resume round 1: get a ruling on how C3 splits (or whether the 500 cap
   bends for this one declared case) and land C3-C6, then G1-G5, then C7.
2. The file route for screenshot bytes and the full README, with its
   headers, and the start of T002.
3. T002: the preview commands, the supervisor intent, the probe-gated link
   and its failure fixtures.
4. T003: the panel, the lightbox, the idle stop and the end-to-end run.
5. The closure sequence.

## Risks

Open findings: 0. C3 oversize is a blocker, not a finding.
