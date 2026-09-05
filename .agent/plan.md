# Plan — amend0905-throughput (operator amendment, Part 2)

Branch: feature/amend0905-throughput, cut from `main` after F262's
closure pull request merged.

## Goal

Land the operator's 2026-09-05 Part 2: sessions run six to eight rounds
while context suffices (2a); the soft-limit default is split-and-close
executed by the session (2b); `scripts/rotate_live_review.py` rotates
`[x]` Gate records and resolved finding pairs into the append-only
`.agent/live_review_archive.md` as a step of every closure sequence, and
the first rotation runs on this branch (2c).

## Current Step

The single amendment round: four rule paragraphs (C1), the script and its
tests (C2), the first rotation (C3), the DECISION entry and this plan
(C4), the handoff and the pull request (C5). No feature is in progress;
Rule A5 proposes the next feature once this merges.

## Next Steps

- The reviewer reads the PR's hosted checks and merges under the
  operator's 2026-09-05 authorization; end state 0 open PRs.
- Follow-up proposal (handoff): rotate `.agent/decisions.md`.

## Risks

- The rotation commit is large by construction (a verbatim move of one
  state-file pair) — declared under AGENTS.md DECISION F104 D1's exemption.
- Readers of `.agent/live_review.md` (integrity check, self-use generator,
  dashboard contract) must stay green after rotation — gated in G4.