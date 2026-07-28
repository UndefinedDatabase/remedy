**Duplicate-block guard (PH v3, operator ruling 2026-07-28):** on
receiving a paste block, the worker's bookkeeping FIRST ACTION also
writes `.agent/last_block.md` (overwrite; committed with the round
bookkeeping): line 1 is `OUTCOME: pending`, followed by the full
received block VERBATIM. At round end the worker updates the OUTCOME
line in place: `executed`, `refused-hash-gate`, or
`stopped-duplicate`. BEFORE executing anything, compare the received
block with the stored block portion of the previous last_block.md:
- Byte-identical and previous OUTCOME `executed` (its
  commits/artifacts are on disk) → STOP immediately, execute nothing,
  and reply only
  `##### SAME PROMPT AGAIN — PROBABLY A RELAY MISTAKE #####`
  plus one line of evidence (e.g. the existing commit shas).
- Byte-identical and previous OUTCOME `refused-hash-gate` → a LOOP:
  resending the same bytes cannot clear a hash failure. STOP with the
  same banner plus the recorded refusal evidence; do NOT re-run the
  failing verification. Absence of effects has two causes — never
  delivered, or delivered and refused — and last_block.md's OUTCOME
  line exists precisely to tell them apart.
- Byte-identical with NO previous record, or effects absent with no
  refusal recorded (a relay gap — the F048 case) → deliberate
  re-issue: proceed normally and note the re-issue in the handback.
