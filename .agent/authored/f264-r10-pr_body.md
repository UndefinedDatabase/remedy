## What

F264 — Steering channel (`remedy chat`). An operator can now correct a running job without
stopping it. One short message, sent with `remedy chat <job_id> "<message>"` or typed into the
input at the bottom of the cockpit's activity card, is recorded as sealed evidence. The job reads
it at the start of its next round, never inside a model call that is already running, and carries
it word for word in every later builder prompt. The job then answers with what it understood and
from which round it applies; `remedy chat show <job_id>` lists that answer, and the cockpit shows
it as its own line in the activity feed. For a job that belongs to a mission, the message is also
added to the mission's contract.

## Why

Watching a job go the wrong way used to leave one button, stop, which throws away the rounds that
were fine. A steering message turns the usual one-sentence correction into the cheapest possible
intervention, and the acknowledgement makes sure a message the job ignored cannot pass unnoticed.

## Key decisions (in `.agent/decisions.md`)

- F264 D1 — a message is a sealed, job-keyed record certified into the run log; `remedy chat` is its
  first route.
- F264 D2 — the cockpit's route is the `chat.send` command on the existing single write channel; it
  records and never reaches a call.
- F264 D3 — the cockpit input is live in the activity card and sends through one pure module that
  says what became of each message.
- F264 D4 — a message is consumed at the top of the next ping-pong round, exactly once, and stays in
  every later builder prompt of the job.
- F264 D5 — a consumed message of a mission's job amends the mission's contract once, before its
  consumption marker is published.
- F264 D6 — the consumption event is the acknowledgement: the message verbatim plus the round, on
  the stream and in `remedy chat show`.
- F264 D7 — the cockpit shows the acknowledgement as its own activity-feed line through one checked
  reader.

## How to review

Start with `docs/guides/steering-user-guide-v1.md` for the behaviour, then
`packages/orchestration/steering.py` (accept, seal, consume, acknowledge), the consumption call in
`run_pingpong` in `packages/orchestration/pingpong_loop.py`, `apps/cli/commands/chat_cmd.py`, the
`chat.send` dispatch in `packages/orchestration/ui_server.py`, and the cockpit modules
`apps/ui/src/api/steeringSend.ts` and `apps/ui/src/api/steeringAck.ts`. The acceptance proofs are
named test by test in the Built State of `docs/roadmap/features/T5_F264.md`; the central one is
`tests/orchestration/test_steering_consumption.py`, which compares the builder prompts of round N
and round N+1 with and without a message sent during round N.

## Changed files

| Path | +/- |
|---|---|
| `README.md` | +12/-2 |
| `apps/cli/command_catalog.py` | +41/-4 |
| `apps/cli/commands/__init__.py` | +2/-1 |
| `apps/cli/commands/chat_cmd.py` | +116/-0 |
| `apps/cli/grouped.py` | +2/-1 |
| `apps/ui/src/api/feedRow.test.ts` | +22/-0 |
| `apps/ui/src/api/feedRow.ts` | +6/-1 |
| `apps/ui/src/api/humanizeCatalog.ts` | +2/-0 |
| `apps/ui/src/api/steeringAck.test.ts` | +41/-0 |
| `apps/ui/src/api/steeringAck.ts` | +50/-0 |
| `apps/ui/src/api/steeringSend.test.ts` | +179/-0 |
| `apps/ui/src/api/steeringSend.ts` | +182/-0 |
| `apps/ui/src/components/panels/ActivityFeedCard.tsx` | +27/-8 |
| `apps/ui/src/components/panels/ChatInput.tsx` | +59/-23 |
| `apps/ui/src/components/panels/RightLivePanel.module.css` | +12/-0 |
| `apps/ui/src/components/panels/RightLivePanel.tsx` | +1/-1 |
| `docs/README.md` | +2/-0 |
| `docs/agents/planner_reviewer_prompt.md` | +6/-0 |
| `docs/guides/exit-codes.md` | +2/-0 |
| `docs/guides/steering-user-guide-v1.md` | +91/-0 |
| `docs/roadmap/STATUS.md` | +1/-1 |
| `docs/roadmap/features/T5_F264.md` | +57/-0 |
| `docs/system/operator-cockpit-v1.md` | +5/-2 |
| `docs/ui/design_reference/assumption_log.md` | +5/-1 |
| `packages/orchestration/event_names.py` | +2/-0 |
| `packages/orchestration/mission_contract.py` | +4/-2 |
| `packages/orchestration/pingpong_loop.py` | +32/-0 |
| `packages/orchestration/steering.py` | +417/-0 |
| `packages/orchestration/ui_server.py` | +93/-3 |
| `tests/cli/test_chat_cmd.py` | +114/-0 |
| `tests/cli/test_cli_ux.py` | +5/-4 |
| `tests/cli/test_golden_path.py` | +1/-1 |
| `tests/orchestration/import_reachability_allowlist.txt` | +2/-0 |
| `tests/orchestration/test_steering.py` | +227/-0 |
| `tests/orchestration/test_steering_consumption.py` | +121/-0 |
| `tests/orchestration/test_steering_mission.py` | +104/-0 |
| `tests/test_command_catalog.py` | +2/-2 |
| `tests/ui_contracts/test_brain_stream_ring.py` | +23/-21 |
| `tests/ui_contracts/test_steering_send_contract.py` | +76/-0 |
| `tests/ui_server/test_command_channel.py` | +14/-2 |
| `tests/ui_server/test_command_dispatch.py` | +109/-0 |
| `tests/ui_server/test_sse_stream.py` | +14/-0 |

Everything else is the loop's own record under `.agent/`: the review ledger and its archive, the
decisions, the plan, the handoffs and the verbatim copies of every round's step block.

## Verdict and evidence

- Live review: every round PASS, rounds 1 to 9 booked in `.agent/live_review.md`; the closing
  round's verdict is written in its handoff.
- The one full suite (round 8): `18852 passed, 20 skipped` at exit 0, no bad node, in
  `.agent/authored/f264-closure-suite.txt`.
- Evidence job `f264r9e1001`; package `remedy-review-20260924-062629-READY_FOR_REVIEW.zip`,
  SHA-256 `7d07e5a59233f424dfe9cc60f9afbf7a1e1eb76d20906d111f8e1a619b43d47c`, in
  `/home/decodeux/Repos/remedy-history/zips`; accepted HEAD
  `2c91712595e069f7f0c7781008d14f07693b8dd9`.
- Self-use track: NONE — the queue holds no pending item and the generator found no eligible
  open finding.
- Open findings: 3 (R-0499, R-0950, R-1008), none raised by this feature, all owned by the next
  findings-paydown feature, F284.

## Runtime actuals

10 delegated rounds over 2 sessions, both on 2026-09-24. Wall clock, tokens and cost:
not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
