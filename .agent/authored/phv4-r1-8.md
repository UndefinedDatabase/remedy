- FIRST bookkeeping action of every round: write .agent/last_block.md
  (overwrite): line 1 `OUTCOME: pending`, then the received paste
  block VERBATIM; update OUTCOME at round end (executed /
  refused-hash-gate / stopped-duplicate). If the received block is
  byte-identical to the stored one: previous OUTCOME executed → STOP,
  reply `##### SAME PROMPT AGAIN — PROBABLY A RELAY MISTAKE #####` +
  one evidence line; previous OUTCOME refused-hash-gate → STOP
  likewise (a loop — the same bytes cannot pass the gate), never
  re-run the failed check; no record / relay gap → deliberate
  re-issue: proceed and note it in the handback. On ANY refusal or
  duplicate STOP: COMMIT AND PUSH .agent/last_block.md — OUTCOME set,
  plus one evidence line (expected vs computed hash, or the
  duplicate's commit shas) — as the round's only commit; a refusal
  with no disk trace is a handback defect.
