## What and why

F038 makes the chat a grounded control stand for a running job. A question is answered only from
the job's and the project's own records: every sentence ends with the numbers of the records it
restates, a sentence that cannot be traced is marked unsupported, and a question the records do not
answer gets "Not in evidence." instead of a guess. A request (stop, pause, resume, a note to the
builder, veto, rerun) becomes a card that says exactly what would be done, and it is sent through
the cockpit's one audited write door only when a person confirms it. The same chat turn serves the
command line (`remedy chat ask`) and the cockpit (the Chat tab of a run's evidence panel).

## Key decisions (all in `.agent/decisions.md`)

- D1, D3: evidence is numbered one-line items with anchors; a node scope per task and a project
  scope per registry project, capped at 4000 estimated tokens, redacted before composition.
- D4, D5: every answer is checked sentence by sentence; the summary model writes answers only when
  `chat.model_written` is switched on, and a failed or unsupported reply falls back to the
  mechanical answer.
- D6, D8: requests map only to exposed door commands; the model reads only what the mechanical
  parse calls unknown, and every argument it returns is grounded.
- D7, D10: a confirmed card is posted to the running cockpit's write door, so its token check,
  replay check, rate limit and audit line apply; `remedy chat ask` sends only on `--yes` or a typed
  `y`.
- D9, D11: one module runs a chat turn for both doors; the cockpit asks through a read route,
  `GET /api/jobs/<job_id>/chat`, and no second POST route exists.
- D12, D13: the chat lives in the evidence panel's Chat tab; each answer says how it was written.
- D2: the fifth findings paydown, F286, waits behind F038 because no finding was open at the claim.

## How to review

1. `docs/roadmap/features/T5_F038.md`, its Built State and its spec-conformance review.
2. `packages/orchestration/chat_turn.py`, then the modules it calls: `chat_evidence.py`,
   `chat_answer.py`, `chat_intent.py`, `chat_intent_model.py` and `chat_door.py`.
3. `apps/cli/commands/chat_cmd.py` (`remedy chat ask`) and `_build_chat_turn_json` in
   `packages/orchestration/ui_server.py`.
4. `apps/ui/src/api/chatTurn.ts` and `apps/ui/src/components/graph/EvidenceChatTab.tsx`.
5. The proofs: `tests/ui_server/test_chat_e2e_live.py` (ask, answer, stop card, confirm, one audit
   line), the canary suite in `tests/orchestration/test_chat_answer.py`, and the DOM audit
   `apps/ui/src/components/graph/evidenceChatAudit.test.ts`.

## Changed files, `fec08a5b` to the accepted head `2fe5345e` and its handoff

| area | files | lines |
|---|---|---|
| packages/orchestration | 12 | +1646 / -4 |
| apps/cli | 3 | +196 / -0 |
| apps/ui | 9 | +1302 / -17 |
| tests | 16 | +3152 / -5 |
| docs | 9 | +183 / -10 |
| .agent (records, blocks, handoffs) | 72 | +9332 / -212 |

The closing commit adds the STATUS line and the README's accepted count, Tier 5 row and paragraph.

## Verdict and evidence

- Latest live review verdict: PASS. Rounds 1 to 14 were each re-derived by the reviewer's own
  runs and mutation red-proofs; this closing round's verdict is booked by the next session.
- Open findings: 0. F038 registered seven (R-1091 High, R-1092 to R-1097 Low) and repaired all.
- Closure suite: `python3 -m pytest -n auto -q`, 20542 passed and 20 skipped, exit 0, no bad node
  (`.agent/authored/f038-closure-suite.txt`).
- Evidence job `f038r14e1001`; package `remedy-review-20260928-194656-READY_FOR_REVIEW.zip`,
  SHA-256 `98bc29b2c6aa67360bf61f1a85fb4f5583f6552100c2615c918a5b54b426bab4`, in
  `/home/decodeux/Repos/remedy-history/zips`; accepted head
  `2fe5345e08ad4b013b8d5a9395e5b1a83b7415f5`.
- Self-use: NONE (queue exhausted).

## Runtime actuals

- Rounds: 15, over three sessions (rounds 1 to 5, 6 to 8, and 9 to 15).
- Models: Claude Opus 5.5 as planner and reviewer, and as each round's worker.
- Wall clock, tokens and cost: not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
